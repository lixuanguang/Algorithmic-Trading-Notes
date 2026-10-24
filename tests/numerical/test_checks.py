"""Tests of the per-check reports, the numerical checks and the numerical demonstrations.

The numerical assertions themselves are the checks' own; these tests only confirm how a run
is reported, that each run starts fresh and leaves shared state alone, and that a failure
reaches the exit status. A demonstration prints values and asserts nothing, so only its runs,
not a failure contract, are tested here.

Run: make test (uv run --frozen --no-editable pytest)
"""

# standard library imports
import contextlib
import datetime as dt
import functools
import io
import pkgutil
import py_compile
import random
import re
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Final, Never, Self
from unittest import mock

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
import trading_notes.numerical
from tests.import_probe import HEAVY, dependency_reads, import_effects
from trading_notes.numerical import (
    active_management,
    afml,
    alternatives_allocation,
    amm_pool,
    asset_pricing_factor_models,
    backtest_design,
    bitemporal,
    black_litterman,
    bond_valuation_risk,
    bsm_svi,
    capital_market_expectations,
    cartea_jaimungal,
    cash_flow_linkage,
    cme_allocation,
    commodity_latency,
    commodity_returns,
    concentrated_position,
    contract_statistics,
    correlation_independence,
    counterparty_capital,
    counterparty_xva,
    country_risk_premium,
    covariance_shrinkage,
    covariance_volatility,
    credit_cds_securitisation,
    credit_portfolios,
    cross_currency_basis,
    currency_management,
    dealer_queue_information,
    default_correlation,
    derivative_overlays,
    digital_assets,
    dividend_tree_swaption,
    drawdown_resampling,
    economic_growth,
    equal_risk_contribution,
    equity_portfolio_management,
    erc_sharpe,
    etf_mechanics,
    exotic_options,
    expected_shortfall,
    extreme_value,
    filing_deadlines,
    filing_timestamps,
    financial_labels,
    financial_ml_methods,
    fixed_income_portfolio,
    forecast_scaling,
    forward_swap_valuation,
    fra_settlement,
    funding_repo,
    fx_mechanics,
    fx_panel_inference,
    garch_ewma,
    gips,
    hedge_funds,
    index_construction,
    inference_simulation,
    institutional_portfolios,
    intercorporate_fx_institutions,
    investment_planning,
    kelly_growth,
    linear_projection,
    linear_regression,
    liquidity_market_design,
    lob_model_derivations,
    lob_models,
    lookback_options,
    macro_policy_trade,
    macro_pricing_risk,
    macro_valuation,
    manager_selection,
    margin_purchase,
    margin_spiral,
    market_estimators_rules,
    market_risk_measurement,
    market_structure,
    mean_cvar,
    monte_carlo_greeks,
    multicurve,
    multiple_testing,
    negative_hedge_ratio,
    numerical_pricing,
    option_models,
    option_strategies,
    option_valuation,
    order_flow,
    order_reconciliation,
    order_routing_fragmentation,
    performance_evaluation,
    perpetual_funding,
    portfolio_moments,
    private_capital,
    private_wealth,
    purged_cv,
    rate_tree_embedded_options,
    real_assets,
    risk_parity,
    seasoned_variance_swap,
    sharpe_conditions,
    sharpe_statistics,
    sharpe_zero,
    statement_analysis,
    statistics_probability,
    stochastic_calculus,
    strategic_asset_allocation,
    synthetic_short,
    time_value_returns,
    trade_execution,
    transaction_cost_hedging,
    var_backtest,
    volatility_mismatch_hedging,
    yield_shift,
)
from trading_notes.numerical.perpetual_funding import FundingReport
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.synthetic_short import ShortReport

ARTEFACTS = Path(__file__).resolve().parents[2] / "notes" / "artefacts"
# A reported check line of CheckReport, of the ok/FAIL reports of perpetual_funding,
# synthetic_short and lob_model_derivations, and of the modules that print failed conditions
# only: covariance_shrinkage, drawdown_resampling, multiple_testing, dealer_queue_information,
# liquidity_market_design, order_flow, order_routing_fragmentation and macro_pricing_risk.
CHECK_LINE = re.compile(r"^  (ok |BAD) ", re.M)
OK_FAIL_LINE = re.compile(r"^(ok  |FAIL) ", re.M)
# fx_panel_inference prints PASS or FAIL lines and no summary.
PASS_FAIL_LINE = re.compile(r"^(PASS|FAIL)  ", re.M)
BAD_ONLY_LINE = re.compile(r"^(BAD) ", re.M)
# At most this many example processes run at once, whatever the number of examples.
MAX_PROCESSES: Final = 4


def forced_failure(report: CheckReport, *_: object) -> None:
    """Stand in for a check function, recording one failed check."""
    report.ok("forced failure", False)


def forced_funding_failure(report: FundingReport, *_: object) -> None:
    """Stand in for a perpetual_funding check function, recording one failed check."""
    report.check("forced failure", 1.0, 0.0)


def forced_short_failure(report: ShortReport, *_: object) -> None:
    """Stand in for a synthetic_short check function, recording one failed check."""
    report.check("forced failure", 1.0, 0.0)


def forced_derivation_failure(failures: list[str], *_: object) -> None:
    """Stand in for a lob_model_derivations check function, recording one failed check."""
    lob_model_derivations.check(failures, "forced failure", False, "forced")


def forced_panel_failure(failures: list[str], *_: object) -> None:
    """Stand in for a fx_panel_inference check function, recording one failed check."""
    fx_panel_inference.check(failures, "forced failure", False, "forced")


def forced_condition_failure(*_: object) -> list[str]:
    """Stand in for a failed_conditions function, reporting one failed condition."""
    return ["forced failure"]


def prepared_drawdown_failure(*_: object) -> drawdown_resampling.DrawdownComparison:
    """Stand in for drawdown_resampling.simulate with percentiles that fail one condition.

    The shuffled percentile is within 15% of the reference, while blocks still come closer,
    so only "shuffle does not understate" fails, without running the simulation.
    """
    return drawdown_resampling.DrawdownComparison(reference=1.0, shuffle=0.9, stationary=0.95)


@dataclass(frozen=True)
class NumericalCheck:
    """A numerical check module and what its tests expect of it.

    Attributes:
        module: The implementation module, with `main()`, run as `python -m <module>`.
        script: Its entrypoint under notes/artefacts/.
        replaced: A function that the tests replace to force one failure.
        summary: The end of its output after that one forced failure: the failure summary,
            or the BAD line itself for a script that prints none.
        checks: The number of check lines a passing run prints; 0 for a module that prints
            only its failures.
        line: Matches each reported check line; group 1 is its status.
        forced: The stand-in for `replaced`, a function of this test module.
        passed: The end of a passing run's output.
        imports: The modules it imports for its heavy dependencies (of `HEAVY`), as it
            imports them. Importing it must load exactly their packages, and open no file
            beyond those they open when imported alone.
        solver: A slow, pure function of one matrix that the module calls by name, which
            bookkeeping tests may answer from earlier results instead of solving again.
        cwd: The folder that the module's default paths are relative to, for a module that
            reads a compendium file; its in-process runs and package commands start there. None
            for a module that reads nothing.
    """

    module: ModuleType
    script: Path
    replaced: str
    summary: str
    checks: int
    line: re.Pattern[str] = CHECK_LINE
    forced: Callable[[Never], object] = forced_failure
    passed: str = "\nall checks passed\n"
    imports: tuple[str, ...] = ()
    solver: Callable[[NDArray[np.float64]], NDArray[np.float64]] | None = None
    cwd: Path | None = None


@dataclass(frozen=True)
class Demonstration:
    """A numerical module that prints values to be read and asserts nothing.

    Its `main()` always returns 0, so it has no failure contract to test.

    Attributes:
        module: The implementation module, with `main()`, run as `python -m <module>`.
        script: Its entrypoint under notes/artefacts/.
        lines: The number of lines a run prints.
        imports: The modules it imports for its heavy dependencies (of `HEAVY`), as it
            imports them. Importing it must load exactly their packages, and open no file
            beyond those they open when imported alone.
    """

    module: ModuleType
    script: Path
    lines: int
    imports: tuple[str, ...] = ()


LIST_SUMMARY = "\nFAILED: ['forced failure']\n"
# bitemporal-check.py, black-litterman-check.py and var-backtest-check.py print no failure
# summary, so nothing follows the BAD line.
NO_SUMMARY = "  BAD forced failure\n"
# The summary of the scripts that print their failures joined by commas.
JOINED_SUMMARY = "\nFAILED: forced failure\n"
# The summary of the scripts that print their failure count and list.
COUNTED_SUMMARY = "\n1 check(s) failed: ['forced failure']\n"
NUMPY = ("numpy",)
# scipy.stats imports NumPy itself, so even a module that imports only scipy.stats loads both.
SCIPY_STATS = ("numpy", "scipy.stats")
# statsmodels imports NumPy, pandas and SciPy itself, so a module that imports any part of it
# loads all four; they are listed before the statsmodels modules it imports.
STATSMODELS = ("numpy", "pandas", "scipy", "statsmodels")
CHECKS = [
    NumericalCheck(
        funding_repo,
        ARTEFACTS / "short-term-funding" / "funding-repo-checks.py",
        "check_margin_call",
        "\n1 check(s) failed: ['forced failure']\n",
        11,
    ),
    NumericalCheck(
        fra_settlement,
        ARTEFACTS / "rates-credit-mortgages" / "fra-settlement-check.py",
        "check_convexity",
        LIST_SUMMARY,
        11,
    ),
    NumericalCheck(
        multicurve,
        ARTEFACTS / "rates-credit-mortgages" / "multicurve-check.py",
        "check_two_curves",
        LIST_SUMMARY,
        6,
    ),
    NumericalCheck(
        amm_pool,
        ARTEFACTS / "crypto-perpetuals" / "amm-checks.py",
        "check_concentrated_position",
        LIST_SUMMARY,
        12,
    ),
    NumericalCheck(
        country_risk_premium,
        ARTEFACTS / "corporate-finance" / "country-risk-premium-check.py",
        "check_zero_limit",
        "FAILED: forced failure\n",
        23,
    ),
    NumericalCheck(
        cash_flow_linkage,
        ARTEFACTS / "financial-statement-analysis" / "cash-flow-linkage-check.py",
        "check_cash_tax",
        "\nFAILED: forced failure\n",
        34,
    ),
    NumericalCheck(
        bsm_svi,
        ARTEFACTS / "volatility-options" / "bsm-svi-checks.py",
        "check_svi",
        LIST_SUMMARY,
        23,
    ),
    NumericalCheck(
        time_value_returns,
        ARTEFACTS / "time-value-returns" / "time-value-return-checks.py",
        "check_share_forward",
        "\nFAILED: forced failure\n",
        114,
    ),
    NumericalCheck(
        bitemporal,
        ARTEFACTS / "point-in-time-data" / "bitemporal-check.py",
        "check_split_correction",
        NO_SUMMARY,
        4,
    ),
    NumericalCheck(
        filing_deadlines,
        ARTEFACTS / "point-in-time-data" / "filing-checks.py",
        "check_deadlines",
        LIST_SUMMARY,
        8,
    ),
    NumericalCheck(
        filing_timestamps,
        ARTEFACTS / "point-in-time-data" / "filing-timestamp-checks.py",
        "check_holiday_cutoff",
        LIST_SUMMARY,
        18,
    ),
    NumericalCheck(
        margin_spiral,
        ARTEFACTS / "funding-crowding" / "spiral-checks.py",
        "check_amplification",
        LIST_SUMMARY,
        4,
    ),
    NumericalCheck(
        cme_allocation,
        ARTEFACTS / "execution-market-making" / "cme-allocation-checks.py",
        "check_fifo",
        LIST_SUMMARY,
        12,
    ),
    NumericalCheck(
        perpetual_funding,
        ARTEFACTS / "crypto-mm-microstructure" / "funding_checks.py",
        "check_sign_convention",
        "FAIL forced failure: got 1, want 0\n1 check(s) failed: ['forced failure']\n",
        17,
        OK_FAIL_LINE,
        forced_funding_failure,
    ),
    NumericalCheck(
        commodity_latency,
        ARTEFACTS / "execution-market-making" / "commodity-production-latency-checks.py",
        "check_latency_calibration",
        LIST_SUMMARY,
        7,
    ),
    NumericalCheck(
        contract_statistics,
        ARTEFACTS / "execution-market-making" / "contract-specifications-statistics-checks.py",
        "check_ism_calendar",
        LIST_SUMMARY,
        38,
    ),
    NumericalCheck(
        synthetic_short,
        ARTEFACTS / "synthetic-equity-cfd-trs" / "synthetic_short_checks.py",
        "check_rebate",
        "FAIL forced failure: got 1.000000, want 0.000000\n1 check(s) failed\n",
        37,
        OK_FAIL_LINE,
        forced_short_failure,
    ),
    NumericalCheck(
        order_reconciliation,
        ARTEFACTS / "model-governance-controls" / "reconciliation-check.py",
        "check_day_order",
        LIST_SUMMARY,
        22,
        passed="\nall checks passed (offline synthetic illustration)\n",
    ),
    NumericalCheck(
        black_litterman,
        ARTEFACTS / "portfolio-construction" / "black-litterman-check.py",
        "check_posterior",
        NO_SUMMARY,
        4,
        imports=NUMPY,
    ),
    NumericalCheck(
        equal_risk_contribution,
        ARTEFACTS / "portfolio-construction" / "erc-check.py",
        "check_unequal_correlations",
        LIST_SUMMARY,
        10,
        imports=NUMPY,
        solver=equal_risk_contribution.minvar_long_only,
    ),
    NumericalCheck(
        erc_sharpe,
        ARTEFACTS / "portfolio-construction" / "erc-sharpe-check.py",
        "check_unequal_correlations",
        LIST_SUMMARY,
        7,
        imports=NUMPY,
    ),
    NumericalCheck(
        expected_shortfall,
        ARTEFACTS / "risk-tail-systemic" / "es-discrete-check.py",
        "check_historical_simulation",
        LIST_SUMMARY,
        14,
    ),
    NumericalCheck(
        covariance_shrinkage,
        ARTEFACTS / "portfolio-construction" / "shrinkage-check.py",
        "failed_conditions",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        imports=NUMPY,
    ),
    NumericalCheck(
        risk_parity,
        ARTEFACTS / "risk-parity-vol-targeting" / "risk-parity-checks.py",
        "check_two_asset_erc",
        LIST_SUMMARY,
        3,
        imports=NUMPY,
    ),
    NumericalCheck(
        garch_ewma,
        ARTEFACTS / "risk-tail-systemic" / "garch-ewma-check.py",
        "check_ewma_against_garch",
        LIST_SUMMARY,
        3,
        imports=NUMPY,
    ),
    NumericalCheck(
        sharpe_zero,
        ARTEFACTS / "backtest-inference" / "sharpe-zero-check.py",
        "check_three_point",
        LIST_SUMMARY,
        4,
        imports=NUMPY,
    ),
    # The forced failure replaces the 5-second simulation with prepared percentiles, so the
    # real failure rule runs without a new simulation.
    NumericalCheck(
        drawdown_resampling,
        ARTEFACTS / "backtest-inference" / "drawdown-resampling-checks.py",
        "simulate",
        "\nBAD shuffle does not understate\n",
        0,
        BAD_ONLY_LINE,
        prepared_drawdown_failure,
        passed="; blocks come closer\nall checks passed\n",
        imports=NUMPY,
    ),
    NumericalCheck(
        linear_projection,
        ARTEFACTS / "equity-long-short-construction" / "projection-checks.py",
        "check_joint_normality",
        LIST_SUMMARY,
        5,
        imports=NUMPY,
    ),
    NumericalCheck(
        var_backtest,
        ARTEFACTS / "risk-tail-systemic" / "var-backtest-check.py",
        "check_clustering",
        NO_SUMMARY,
        3,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        multiple_testing,
        ARTEFACTS / "backtest-inference" / "multiple-testing-checks.py",
        "failed_conditions",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        sharpe_statistics,
        ARTEFACTS / "backtest-inference" / "sharpe-checks.py",
        "check_deflated_sharpe",
        LIST_SUMMARY,
        23,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        forecast_scaling,
        ARTEFACTS / "equity-long-short-construction" / "forecast-checks.py",
        "check_table_10_1",
        LIST_SUMMARY,
        16,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        purged_cv,
        ARTEFACTS / "statistical-learning-foundations" / "cv-checks.py",
        "check_purged_kfold",
        LIST_SUMMARY,
        7,
        imports=NUMPY,
    ),
    NumericalCheck(
        concentrated_position,
        ARTEFACTS / "private-wealth" / "concentrated-position-check.py",
        "check_exchange_fund",
        JOINED_SUMMARY,
        8,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        lob_model_derivations,
        ARTEFACTS / "market-making-lob" / "model-derivations-checks.py",
        "check_roll",
        "FAIL forced failure: forced\n",
        11,
        OK_FAIL_LINE,
        forced_derivation_failure,
        passed="lag 2 -0.00005\n",
        imports=("numpy", "scipy.optimize"),
    ),
    NumericalCheck(
        sharpe_conditions,
        ARTEFACTS / "backtest-inference" / "sharpe-conditions-checks.py",
        "check_compounding",
        LIST_SUMMARY,
        8,
        imports=NUMPY,
    ),
    NumericalCheck(
        dividend_tree_swaption,
        ARTEFACTS / "option-valuation" / "dividend-tree-swaption-checks.py",
        "check_swaptions",
        JOINED_SUMMARY,
        6,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        lob_models,
        ARTEFACTS / "market-making-lob" / "model-checks.py",
        "check_free_entry",
        LIST_SUMMARY,
        37,
        imports=("numpy", "scipy.integrate", "scipy.optimize"),
    ),
    NumericalCheck(
        margin_purchase,
        ARTEFACTS / "short-term-funding" / "margin-purchase-check.py",
        "check_levered_return",
        JOINED_SUMMARY,
        7,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        cross_currency_basis,
        ARTEFACTS / "forward-swap-valuation" / "cross-currency-basis-check.py",
        "check_final_exchange",
        JOINED_SUMMARY,
        16,
        imports=NUMPY,
    ),
    NumericalCheck(
        seasoned_variance_swap,
        ARTEFACTS / "derivative-overlays" / "seasoned-variance-swap-check.py",
        "check_simulation",
        JOINED_SUMMARY,
        8,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats"),
    ),
    NumericalCheck(
        covariance_volatility,
        ARTEFACTS / "high-dimensional-estimation" / "covariance-volatility-checks.py",
        "check_har",
        LIST_SUMMARY,
        11,
        imports=NUMPY,
    ),
    NumericalCheck(
        etf_mechanics,
        ARTEFACTS / "etf-mechanics" / "etf-checks.py",
        "check_cost_of_ownership",
        LIST_SUMMARY,
        13,
        imports=NUMPY,
    ),
    NumericalCheck(
        trade_execution,
        ARTEFACTS / "trade-execution" / "trade-execution-checks.py",
        "check_evaluation",
        COUNTED_SUMMARY,
        14,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        macro_valuation,
        ARTEFACTS / "macro-asset-valuation" / "macro-valuation-checks.py",
        "check_multiples_and_property",
        COUNTED_SUMMARY,
        16,
        imports=("numpy", "scipy"),
    ),
    NumericalCheck(
        commodity_returns,
        ARTEFACTS / "commodity-investment" / "commodity-return-checks.py",
        "check_swaps",
        LIST_SUMMARY,
        15,
        imports=NUMPY,
    ),
    NumericalCheck(
        correlation_independence,
        ARTEFACTS / "inference-simulation" / "correlation-independence-checks.py",
        "check_size",
        JOINED_SUMMARY,
        13,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        counterparty_capital,
        ARTEFACTS / "counterparty-xva" / "counterparty-capital-check.py",
        "check_worked_example",
        JOINED_SUMMARY,
        13,
        imports=("numpy", "scipy", "scipy.integrate"),
    ),
    NumericalCheck(
        volatility_mismatch_hedging,
        ARTEFACTS / "option-valuation" / "volatility-mismatch-hedging-check.py",
        "check_gamma_condition",
        JOINED_SUMMARY,
        10,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        alternatives_allocation,
        ARTEFACTS / "alternatives-allocation" / "alternatives-allocation-checks.py",
        "check_liquidity",
        LIST_SUMMARY,
        13,
        imports=NUMPY,
    ),
    NumericalCheck(
        market_structure,
        ARTEFACTS / "firms-market-structure" / "market-structure-checks.py",
        "check_concentration",
        LIST_SUMMARY,
        13,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        hedge_funds,
        ARTEFACTS / "hedge-funds" / "hedge-fund-checks.py",
        "check_allocation",
        LIST_SUMMARY,
        17,
        imports=NUMPY,
    ),
    NumericalCheck(
        gips,
        ARTEFACTS / "performance-presentation-standards" / "gips-checks.py",
        "check_composite_report",
        COUNTED_SUMMARY,
        25,
        imports=NUMPY,
    ),
    NumericalCheck(
        stochastic_calculus,
        ARTEFACTS / "stochastic-calculus" / "stochastic-calculus-checks.py",
        "check_feynman_kac",
        JOINED_SUMMARY,
        23,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        index_construction,
        ARTEFACTS / "market-index-construction" / "index-construction-checks.py",
        "check_bond_index",
        COUNTED_SUMMARY,
        30,
        imports=NUMPY,
    ),
    NumericalCheck(
        monte_carlo_greeks,
        ARTEFACTS / "numerical-pricing" / "monte-carlo-greeks-check.py",
        "check_fd_variance",
        "\nFAILED:forced failure\n",
        17,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        currency_management,
        ARTEFACTS / "currency-management" / "currency-management-checks.py",
        "check_active_strategies",
        COUNTED_SUMMARY,
        21,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        option_models,
        ARTEFACTS / "option-pricing-models" / "option-model-checks.py",
        "check_sabr",
        LIST_SUMMARY,
        20,
        imports=NUMPY,
    ),
    NumericalCheck(
        economic_growth,
        ARTEFACTS / "economic-growth" / "growth-checks.py",
        "check_endogenous_growth",
        COUNTED_SUMMARY,
        22,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        derivative_overlays,
        ARTEFACTS / "derivative-overlays" / "overlay-checks.py",
        "check_endowment_case",
        COUNTED_SUMMARY,
        25,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        active_management,
        ARTEFACTS / "active-management-analysis" / "active-management-checks.py",
        "check_risk_decomposition",
        COUNTED_SUMMARY,
        30,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        credit_portfolios,
        ARTEFACTS / "credit-portfolios" / "credit-portfolio-checks.py",
        "check_structured",
        LIST_SUMMARY,
        25,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        fx_mechanics,
        ARTEFACTS / "fx-mechanics-determination" / "fx-checks.py",
        "check_flows",
        COUNTED_SUMMARY,
        27,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        manager_selection,
        ARTEFACTS / "manager-selection" / "manager-selection-checks.py",
        "check_shrinkage",
        COUNTED_SUMMARY,
        26,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        transaction_cost_hedging,
        ARTEFACTS / "option-valuation" / "transaction-cost-hedging-check.py",
        "check_nonadditivity",
        JOINED_SUMMARY,
        16,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        capital_market_expectations,
        ARTEFACTS / "capital-market-expectations" / "cme-checks.py",
        "check_reweighting",
        COUNTED_SUMMARY,
        28,
        imports=("numpy", "scipy"),
    ),
    NumericalCheck(
        portfolio_moments,
        ARTEFACTS / "portfolio-risk-return" / "portfolio-moments-checks.py",
        "check_conditional_correlation",
        JOINED_SUMMARY,
        29,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats"),
    ),
    NumericalCheck(
        digital_assets,
        ARTEFACTS / "digital-assets" / "digital-asset-checks.py",
        "check_custody",
        LIST_SUMMARY,
        21,
        imports=NUMPY,
    ),
    NumericalCheck(
        numerical_pricing,
        ARTEFACTS / "numerical-pricing" / "numerical-pricing-checks.py",
        "check_bermudan",
        JOINED_SUMMARY,
        18,
        imports=("numpy", "scipy", "scipy.stats", "scipy.linalg"),
    ),
    # Its last check reads a compendium figure relative to the entry's folder; the entrypoint
    # passes the figure's location instead.
    NumericalCheck(
        asset_pricing_factor_models,
        ARTEFACTS / "asset-pricing-factor-models" / "asset-pricing-checks.py",
        "check_factor_models",
        JOINED_SUMMARY,
        39,
        imports=(*STATSMODELS, "statsmodels.api"),
        cwd=ARTEFACTS / "asset-pricing-factor-models",
    ),
    NumericalCheck(
        backtest_design,
        ARTEFACTS / "backtest-inference" / "backtest-design-checks.py",
        "check_survivorship",
        LIST_SUMMARY,
        19,
        imports=NUMPY,
    ),
    NumericalCheck(
        bond_valuation_risk,
        ARTEFACTS / "bond-valuation-risk" / "bond-valuation-checks.py",
        "check_treasury_formulas",
        COUNTED_SUMMARY,
        94,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        credit_cds_securitisation,
        ARTEFACTS / "corporate-credit-capital" / "credit-cds-securitisation-checks.py",
        "check_migration",
        "\n49 checks executed\nFAILED: ['forced failure']\n",
        52,
        imports=("numpy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        counterparty_xva,
        ARTEFACTS / "counterparty-xva" / "counterparty-xva-checks.py",
        "check_collateral",
        JOINED_SUMMARY,
        32,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats"),
    ),
    # Part 3's correlation searches take most of its 30 seconds; the forced failure replaces it.
    NumericalCheck(
        default_correlation,
        ARTEFACTS / "default-correlation" / "default-correlation-checks.py",
        "check_base_correlation",
        JOINED_SUMMARY,
        18,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        statistics_probability,
        ARTEFACTS / "descriptive-probability" / "statistics-probability-checks.py",
        "check_bayesian",
        JOINED_SUMMARY,
        64,
        imports=("numpy", "scipy.integrate", "scipy.stats"),
    ),
    # The capacity part takes nearly all of its minute; the forced failure replaces it.
    NumericalCheck(
        equity_portfolio_management,
        ARTEFACTS / "equity-portfolio-management" / "equity-portfolio-checks.py",
        "check_capacity_structure",
        COUNTED_SUMMARY,
        26,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        dealer_queue_information,
        ARTEFACTS / "execution-market-making" / "dealer-queue-information-checks.py",
        "check_power_and_inference",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        liquidity_market_design,
        ARTEFACTS / "execution-market-making" / "liquidity-market-design-checks.py",
        "check_capacity",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        imports=NUMPY,
    ),
    NumericalCheck(
        market_estimators_rules,
        ARTEFACTS / "execution-market-making" / "market-estimators-rules-checks.py",
        "check_model_i",
        "\nFAILURES: ['forced failure']\n",
        45,
        passed="\nFAILURES: none\n",
        imports=NUMPY,
    ),
    NumericalCheck(
        exotic_options,
        ARTEFACTS / "exotic-options" / "exotic-option-checks.py",
        "check_barrier",
        JOINED_SUMMARY,
        21,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        lookback_options,
        ARTEFACTS / "exotic-options" / "lookback-option-check.py",
        "check_monitoring",
        JOINED_SUMMARY,
        19,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    # Its 24 seconds are diagnostics that take no report, so the forced failure still runs them.
    NumericalCheck(
        extreme_value,
        ARTEFACTS / "extreme-value" / "extreme-value-checks.py",
        "check_rmfi",
        JOINED_SUMMARY,
        8,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        financial_ml_methods,
        ARTEFACTS / "financial-ml-methods" / "ml-methods-checks.py",
        "check_classifier",
        LIST_SUMMARY,
        23,
        imports=("numpy", "scipy", "scipy.cluster.hierarchy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        intercorporate_fx_institutions,
        ARTEFACTS / "financial-statement-analysis" / "intercorporate-fx-institutions-checks.py",
        "check_classification",
        LIST_SUMMARY,
        54,
        imports=NUMPY,
    ),
    NumericalCheck(
        statement_analysis,
        ARTEFACTS / "financial-statement-analysis" / "statement-analysis-checks.py",
        "check_leases",
        LIST_SUMMARY,
        138,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        fixed_income_portfolio,
        ARTEFACTS / "fixed-income-portfolio" / "fixed-income-portfolio-checks.py",
        "check_indexes",
        COUNTED_SUMMARY,
        40,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        forward_swap_valuation,
        ARTEFACTS / "forward-swap-valuation" / "forward-swap-checks.py",
        "check_option_payoffs",
        COUNTED_SUMMARY,
        69,
        imports=NUMPY,
    ),
    NumericalCheck(
        inference_simulation,
        ARTEFACTS / "inference-simulation" / "inference-simulation-checks.py",
        "check_discretisation",
        JOINED_SUMMARY,
        52,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        institutional_portfolios,
        ARTEFACTS / "institutional-portfolios" / "institutional-checks.py",
        "check_endowment",
        LIST_SUMMARY,
        28,
        imports=NUMPY,
    ),
    NumericalCheck(
        investment_planning,
        ARTEFACTS / "investment-planning" / "investment-planning-checks.py",
        "check_behaviour",
        COUNTED_SUMMARY,
        41,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        macro_policy_trade,
        ARTEFACTS / "macro-policy-trade" / "macro-policy-trade-checks.py",
        "check_trade",
        COUNTED_SUMMARY,
        25,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        market_risk_measurement,
        ARTEFACTS / "market-risk-measurement" / "market-risk-checks.py",
        "check_sensitivity_scenarios",
        COUNTED_SUMMARY,
        27,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        order_flow,
        ARTEFACTS / "market-simulation" / "order-flow-checks.py",
        "check_trade_signing",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        passed="Hawkes gaps: CV = 1.365; E[X^2]/(2E[X]) = 0.579 against the mean wait 0.594 from"
        " uniform start times (the stationary inversion formula, Palm moments)\n",
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats"),
    ),
    NumericalCheck(
        order_routing_fragmentation,
        ARTEFACTS / "market-structure-execution-quality" / "order-routing-fragmentation-checks.py",
        "check_learner",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        passed="  a1=100.0, b2=100.01, all-in cost k=0.02: profit per unit -0.01 -> none\n",
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        macro_pricing_risk,
        ARTEFACTS / "multi-asset-systematic-macro" / "macro-pricing-risk-checks.py",
        "check_duration",
        "\nBAD forced failure\n",
        0,
        BAD_ONLY_LINE,
        forced_condition_failure,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        option_strategies,
        ARTEFACTS / "option-strategies" / "option-strategy-checks.py",
        "check_selection",
        COUNTED_SUMMARY,
        31,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        option_valuation,
        ARTEFACTS / "option-valuation" / "option-valuation-checks.py",
        "check_greeks",
        COUNTED_SUMMARY,
        44,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        performance_evaluation,
        ARTEFACTS / "performance-evaluation" / "performance-evaluation-checks.py",
        "check_skill",
        COUNTED_SUMMARY,
        41,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats"),
    ),
    NumericalCheck(
        kelly_growth,
        ARTEFACTS / "portfolio-construction" / "kelly-check.py",
        "check_levered_ruin",
        JOINED_SUMMARY,
        23,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats"),
    ),
    # Twenty linear programmes take most of its two minutes; their solver is answered from the
    # reference run, and the forced failure replaces a quick part.
    NumericalCheck(
        mean_cvar,
        ARTEFACTS / "portfolio-construction" / "mean-cvar-check.py",
        "check_mean_variance",
        JOINED_SUMMARY,
        8,
        imports=(
            "numpy",
            "scipy",
            "scipy.optimize",
            "scipy.sparse",
            "scipy.special",
            "scipy.stats",
        ),
        solver=mean_cvar.cvar_weights,
    ),
    NumericalCheck(
        private_capital,
        ARTEFACTS / "private-capital" / "private-capital-checks.py",
        "check_valuation",
        LIST_SUMMARY,
        38,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        private_wealth,
        ARTEFACTS / "private-wealth" / "private-wealth-checks.py",
        "check_residence",
        LIST_SUMMARY,
        59,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        rate_tree_embedded_options,
        ARTEFACTS / "rate-tree-embedded-options" / "rate-tree-checks.py",
        "check_paths",
        COUNTED_SUMMARY,
        46,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        real_assets,
        ARTEFACTS / "real-assets" / "real-asset-checks.py",
        "check_reit",
        LIST_SUMMARY,
        37,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        strategic_asset_allocation,
        ARTEFACTS / "strategic-asset-allocation" / "saa-checks.py",
        "check_goals_heuristics",
        COUNTED_SUMMARY,
        40,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats"),
    ),
    NumericalCheck(
        fx_panel_inference,
        ARTEFACTS / "fx-determination-forecasting" / "fx-panel-inference-check.py",
        "check_empty_months",
        "FAIL  forced failure: forced\n",
        11,
        PASS_FAIL_LINE,
        forced_panel_failure,
        passed="\nPASS  empty months stay on the calendar grid: -1.0789\n",
        imports=NUMPY,
    ),
    NumericalCheck(
        linear_regression,
        ARTEFACTS / "linear-regression" / "regression-checks.py",
        "check_functional_forms",
        JOINED_SUMMARY,
        44,
        imports=(
            *STATSMODELS,
            "statsmodels.api",
            "statsmodels.formula.api",
            "scipy.integrate",
            "scipy.stats",
            "statsmodels.regression.linear_model",
            "statsmodels.stats.anova",
        ),
    ),
]
DEMONSTRATIONS = [
    Demonstration(
        cartea_jaimungal,
        ARTEFACTS / "reinforcement-learning-trading" / "cartea_jaimungal_checks.py",
        22,
    ),
    Demonstration(
        negative_hedge_ratio,
        ARTEFACTS / "volatility-options" / "negative-hedge-ratio-check.py",
        6,
        imports=NUMPY,
    ),
    Demonstration(
        yield_shift,
        ARTEFACTS / "rates-credit-mortgages" / "yield-shift-check.py",
        9,
        imports=("numpy", "scipy.optimize"),
    ),
    Demonstration(
        financial_labels,
        ARTEFACTS / "statistical-learning-foundations" / "financial-labels-capital-checks.py",
        39,
        imports=NUMPY,
    ),
    Demonstration(
        afml,
        ARTEFACTS / "statistical-learning-foundations" / "afml-checks.py",
        84,
        imports=(*STATSMODELS, "statsmodels.tsa.stattools"),
    ),
]
EXAMPLES: list[NumericalCheck | Demonstration] = [*CHECKS, *DEMONSTRATIONS]
# Package modules that are not examples, with the heavy dependencies each imports (of `HEAVY`).
SUPPORT: dict[str, tuple[str, ...]] = {
    "trading_notes": (),
    "trading_notes.numerical": (),
    "trading_notes.numerical.report": (),
    "trading_notes.numerical.newey_west": NUMPY,
}


def run_main(example: NumericalCheck | Demonstration) -> int:
    """Run the example's `main()` in process, from its `cwd` when it has one."""
    folder = example.cwd if isinstance(example, NumericalCheck) else None
    with contextlib.chdir(folder) if folder else contextlib.nullcontext():
        status: int = example.module.main()
    return status


def captured(run: Callable[[], int]) -> tuple[int, str]:
    """Return a run's exit status and everything it printed."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        status = run()
    return status, out.getvalue()


@dataclass(frozen=True)
class GlobalState:
    """The process-wide state that a numerical run must leave as it found it.

    Attributes:
        python_random: The shared `random` generator's state, its cached Gaussian included.
        numpy_random: NumPy's legacy generator as (kind, key bytes, position, has cached
            Gaussian, cached Gaussian).
        printoptions: NumPy's print options.
        errors: NumPy's floating-point error handling.
    """

    python_random: tuple[object, ...]
    numpy_random: tuple[str, bytes, int, int, float]
    printoptions: dict[str, object]
    errors: dict[str, object]

    @classmethod
    def now(cls) -> Self:
        """Return the current state, copied so that later changes cannot reach it."""
        legacy = np.random.get_state(legacy=True)
        assert isinstance(legacy, tuple)
        kind, key, position, has_gauss, gauss = legacy
        return cls(
            random.getstate(),
            (kind, key.tobytes(), position, has_gauss, gauss),
            dict(np.get_printoptions()),
            dict(np.geterr()),
        )


@contextlib.contextmanager
def restored_global_state() -> Iterator[None]:
    """Restore the shared random generators and NumPy's settings afterwards, even on failure."""
    python_random, numpy_random = random.getstate(), np.random.get_state(legacy=True)
    try:
        with np.printoptions(**np.get_printoptions()), np.errstate(**np.geterr()):
            yield
    finally:
        random.setstate(python_random)
        np.random.set_state(numpy_random)


def prime_global_random(seed: int) -> None:
    """Seed both shared generators and leave each holding a cached Gaussian draw."""
    random.seed(seed)
    random.gauss(0, 1)
    np.random.seed(seed)
    np.random.standard_normal()


# Results of the checks' slow solvers, by solver and matrix, from runs of the real solver.
SOLVED: dict[tuple[str, bytes], NDArray[np.float64]] = {}


@contextlib.contextmanager
def solved_once(example: NumericalCheck | Demonstration) -> Iterator[None]:
    """Answer the check's slow solver, if any, from `SOLVED`, solving only unseen matrices.

    The solver is pure, so a copy of an earlier result is exactly what it would return.
    """
    solver = example.solver if isinstance(example, NumericalCheck) else None
    if solver is None:
        yield
        return

    def solve(S: NDArray[np.float64]) -> NDArray[np.float64]:
        key = (solver.__qualname__, S.tobytes())
        if key not in SOLVED:
            SOLVED[key] = solver(S)
        return SOLVED[key].copy()

    with mock.patch.object(example.module, solver.__name__, solve):
        yield


@functools.cache
def reference_run(example: NumericalCheck | Demonstration) -> tuple[int, str]:
    """Return the exit status and output of one in-process run, made once per test session.

    Comparisons with other runs reuse it, so a slow example (equal_risk_contribution's solver
    takes seconds) is not rerun for each comparison. It runs the real solver and records its
    results for `solved_once`. The shared random generators are left unseeded, as the process
    started them.
    """
    with solved_once(example):
        return captured(functools.partial(run_main, example))


def run_concurrently(
    commands: Sequence[tuple[Sequence[str], Path]],
) -> list[subprocess.CompletedProcess[str]]:
    """Run independent commands, each from its working directory; results in command order.

    The processes share nothing, so running a few together only saves waiting for the slow
    examples one after another. At most `MAX_PROCESSES` run at once.
    """

    def run(command: tuple[Sequence[str], Path]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(command[0], cwd=command[1], capture_output=True, text=True)

    with ThreadPoolExecutor(max_workers=MAX_PROCESSES) as pool:
        return list(pool.map(run, commands))


class Reporting(unittest.TestCase):
    """CheckReport prints each check and keeps the failures of its own run."""

    def test_passing_checks_print_ok_lines(self) -> None:
        """Passing checks print `ok`, with a detail when one is given, and record nothing."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.ok("first", True)
            report.ok("second", True, "1.00")
        self.assertEqual(out.getvalue(), "  ok  first\n  ok  second: 1.00\n")
        self.assertEqual(report.failures, [])

    def test_failures_accumulate_in_order(self) -> None:
        """Failures print `BAD`, accumulate in run order and never end the process."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.ok("x", False)
            report.ok("y", True)
            report.ok("z", False, "detail")
        self.assertEqual(out.getvalue(), "  BAD x\n  ok  y\n  BAD z: detail\n")
        self.assertEqual(report.failures, ["x", "z"])
        self.assertEqual(report.count, 3)

    def test_failures_belong_to_one_report(self) -> None:
        """The failure list is a copy, and a new report starts empty."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            report.ok("x", False)
        report.failures.append("tampered")
        self.assertEqual(report.failures, ["x"])
        self.assertEqual((CheckReport().failures, CheckReport().count), ([], 0))

    def test_same_prints_got_and_want(self) -> None:
        """`same` compares with ==, prints both values with str and records a mismatch."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.same("date", dt.date(2026, 11, 26), dt.date(2026, 11, 26))
            report.same("unknown", None, None)
            report.same("factor", 1.0, 7.0)
        self.assertEqual(
            out.getvalue(),
            "  ok  date: 2026-11-26 (want 2026-11-26)\n"
            "  ok  unknown: None (want None)\n"
            "  BAD factor: 1.0 (want 7.0)\n",
        )
        self.assertEqual(report.failures, ["factor"])
        self.assertEqual(report.count, 3)


class SharedStateHelpers(unittest.TestCase):
    """The helpers that compare and restore shared state see every part of it."""

    def test_snapshot_sees_cached_gaussians(self) -> None:
        """Using up only a cached Gaussian, with no new draw, still changes the snapshot."""
        with restored_global_state():
            prime_global_random(1)
            before = GlobalState.now()
            random.gauss(0, 1)
            np.random.standard_normal()
            after = GlobalState.now()
        self.assertEqual(after.python_random[:2], before.python_random[:2])
        self.assertNotEqual(after.python_random, before.python_random)
        self.assertEqual(after.numpy_random[:3], before.numpy_random[:3])
        self.assertNotEqual(after.numpy_random[3:], before.numpy_random[3:])

    def test_restores_after_a_failure(self) -> None:
        """Generators, print options and error handling are restored when the body raises."""
        before = GlobalState.now()
        with self.assertRaises(ZeroDivisionError), restored_global_state():
            prime_global_random(2)
            np.set_printoptions(precision=3)
            np.seterr(all="raise")
            _ = 1 / 0
        self.assertEqual(GlobalState.now(), before)


class NumericalChecks(unittest.TestCase):
    """The numerical checks and demonstrations, in process, as modules and as scripts."""

    def test_successive_runs_repeat_identically(self) -> None:
        """Each run has its own state, so two runs print the same thing, whatever came before.

        The reference run finds the shared generators as the process seeded them; the second
        finds them seeded differently and each holding a cached Gaussian. The second run must
        leave both generators, NumPy's print options and its error handling exactly as it
        found them.
        """
        for example in EXAMPLES:
            with self.subTest(example.module.__name__):
                first = reference_run(example)
                with restored_global_state():
                    prime_global_random(20261023)
                    before = GlobalState.now()
                    second = captured(functools.partial(run_main, example))
                    self.assertEqual(GlobalState.now(), before)
                self.assertEqual(first, second)
                self.assertEqual(first[0], 0)
                if isinstance(example, Demonstration):
                    self.assertEqual(first[1].count("\n"), example.lines)
                    continue
                statuses = example.line.findall(first[1])
                self.assertEqual(len(statuses), example.checks)
                self.assertFalse([s for s in statuses if s in ("BAD", "FAIL")])
                self.assertTrue(first[1].endswith(example.passed))

    def test_failure_returns_1_and_does_not_leak(self) -> None:
        """A failed check gives status 1 and its summary; the next run is clean.

        Only the report's bookkeeping is tested, so slow solvers are answered from the
        reference run's results.
        """
        for check in CHECKS:
            with self.subTest(check.module.__name__), solved_once(check):
                reference_run(check)
                with mock.patch.object(check.module, check.replaced, check.forced):
                    status, out = captured(functools.partial(run_main, check))
                self.assertEqual(status, 1)
                self.assertTrue(out.endswith(check.summary), out[-200:])
                self.assertNotIn("all checks passed", out)
                failed = [s for s in check.line.findall(out) if s in ("BAD", "FAIL")]
                self.assertEqual(len(failed), 1, out)
                self.assertEqual(captured(functools.partial(run_main, check)), reference_run(check))

    def test_entrypoints_run_from_any_directory(self) -> None:
        """Each script runs, isolated, from its own folder and from an unrelated one."""
        with tempfile.TemporaryDirectory() as elsewhere:
            runs = [
                (example, cwd)
                for example in EXAMPLES
                for cwd in (example.script.parent, Path(elsewhere))
            ]
            results = run_concurrently(
                [
                    ([sys.executable, "-I", "-W", "error", str(example.script)], cwd)
                    for example, cwd in runs
                ]
            )
            for (example, cwd), done in zip(runs, results, strict=True):
                with self.subTest(example.script.name, cwd=cwd.name):
                    self.assertEqual((done.returncode, done.stderr), (0, ""))
                    self.assertEqual(done.stdout, reference_run(example)[1])
            self.assertEqual(list(Path(elsewhere).iterdir()), [])

    def test_entrypoint_propagates_failure_status(self) -> None:
        """A failed check makes the script exit 1, with no traceback."""
        # Replace one check, then execute the script as `python <script>` would.
        codes = [
            f"import runpy, {check.module.__name__} as m\n"
            "import tests.numerical.test_checks as t\n"
            f"m.{check.replaced} = t.{check.forced.__name__}\n"
            f"runpy.run_path({str(check.script)!r}, run_name='__main__')\n"
            for check in CHECKS
        ]
        root = Path(__file__).resolve().parents[2]
        results = run_concurrently([([sys.executable, "-c", code], root) for code in codes])
        for check, done in zip(CHECKS, results, strict=True):
            with self.subTest(check.script.name):
                self.assertEqual(done.returncode, 1, done.stderr)
                self.assertTrue(done.stdout.endswith(check.summary))
                self.assertEqual(done.stderr, "")

    def test_modules_run_as_package_commands(self) -> None:
        """`python -m <module>` runs, isolated, from an unrelated folder, as `main()` does.

        A module whose default paths are relative to a folder (`cwd`) runs from that folder.
        """
        with tempfile.TemporaryDirectory() as elsewhere:
            results = run_concurrently(
                [
                    (
                        [sys.executable, "-I", "-W", "error", "-m", example.module.__name__],
                        (example.cwd if isinstance(example, NumericalCheck) else None)
                        or Path(elsewhere),
                    )
                    for example in EXAMPLES
                ]
            )
            for example, done in zip(EXAMPLES, results, strict=True):
                with self.subTest(example.module.__name__):
                    self.assertEqual((done.returncode, done.stderr), (0, ""))
                    self.assertEqual(done.stdout, reference_run(example)[1])
                    source = Path(example.module.__file__ or "").read_text()
                    self.assertTrue(
                        source.endswith('\n\nif __name__ == "__main__":\n    sys.exit(main())\n')
                    )
            self.assertEqual(list(Path(elsewhere).iterdir()), [])

    def test_every_package_module_is_covered(self) -> None:
        """Each module of trading_notes.numerical is one listed check, demonstration or support."""
        found = {
            module.name
            for module in pkgutil.iter_modules(
                trading_notes.numerical.__path__, "trading_notes.numerical."
            )
        }
        checks = {check.module.__name__ for check in CHECKS}
        demonstrations = {demonstration.module.__name__ for demonstration in DEMONSTRATIONS}
        self.assertEqual(checks & demonstrations, set())
        self.assertEqual(len(checks) + len(demonstrations), len(EXAMPLES))
        listed = checks | demonstrations | set(SUPPORT)
        self.assertEqual(found, listed - {"trading_notes", "trading_notes.numerical"})

    def test_imports_have_no_side_effects(self) -> None:
        """Importing a module alone prints nothing, reads no data and runs no example.

        Each module is imported in its own fresh process, so one module's dependencies cannot
        hide another's. It loads exactly its declared heavy dependencies and never the
        structural checkers, and leaves Python's shared generator as it was. It opens no file
        beyond those its dependencies open when imported alone, cold, in the same kind of
        process: none for the standard library or NumPy, and for SciPy the platform and
        package metadata that SciPy reads as it starts. A module with dependencies is imported
        again with them loaded first, so that NumPy's legacy generator is compared too. Support
        modules are held to the same rules.
        """
        imports = SUPPORT | {example.module.__name__: example.imports for example in EXAMPLES}
        watched = [*HEAVY, "trading_notes.structure"]
        with tempfile.TemporaryDirectory() as elsewhere:
            allowed = {(): frozenset[str]()} | {
                dependencies: dependency_reads(dependencies, Path(elsewhere))
                for dependencies in set(imports.values()) - {()}
            }
            # The standard-library and NumPy modules stay held to opening nothing at all, and
            # no dependency's own reads reach the notes, where the research data is kept.
            self.assertEqual(allowed[NUMPY], frozenset())
            notes = ARTEFACTS.parent
            self.assertFalse(
                [p for r in allowed.values() for p in r if Path(p).is_relative_to(notes)]
            )
            for name, dependencies in imports.items():
                with self.subTest(name):
                    effects = import_effects([name], watched, Path(elsewhere))
                    self.assertEqual(effects.returncode, 0, effects.stderr)
                    self.assertEqual(
                        (
                            effects.reads_beyond(allowed[dependencies]),
                            effects.printed,
                            effects.loaded,
                            effects.stderr,
                        ),
                        ([], "", sorted({d.partition(".")[0] for d in dependencies}), ""),
                    )
                    self.assertTrue(effects.random_unchanged)
                    if dependencies:
                        preloaded = import_effects(
                            [name], watched, Path(elsewhere), preload=dependencies
                        )
                        self.assertEqual(
                            (preloaded.returncode, preloaded.stderr, preloaded.random_unchanged),
                            (0, "", True),
                        )
                    self.assertEqual(list(Path(elsewhere).iterdir()), [])

    def test_data_read_at_import_is_caught(self) -> None:
        """A module that reads a data file as it is imported fails the import check.

        The read is caught whatever the module imports first: nothing, NumPy, or scipy.stats
        with its own metadata reads, which stay allowed. The module is compiled beforehand,
        as an installed one is, so that importing it writes no bytecode cache.
        """
        with tempfile.TemporaryDirectory() as folder, tempfile.TemporaryDirectory() as elsewhere:
            data = Path(folder) / "returns.csv"
            data.write_text("0.01\n")
            for dependencies in ((), NUMPY, SCIPY_STATS):
                module = f"reader_{len(dependencies)}"
                source = Path(folder) / f"{module}.py"
                source.write_text(
                    "".join(f"import {d}\n" for d in dependencies)
                    + f"from pathlib import Path\nDATA = Path({str(data)!r}).read_text()\n"
                )
                py_compile.compile(str(source), doraise=True)
                with self.subTest(dependencies=dependencies):
                    effects = import_effects([module], HEAVY, Path(elsewhere), path=[Path(folder)])
                    self.assertEqual((effects.returncode, effects.stderr), (0, ""))
                    allowed = (
                        dependency_reads(dependencies, Path(elsewhere))
                        if dependencies
                        else frozenset[str]()
                    )
                    self.assertNotIn(str(data), allowed)
                    self.assertEqual(effects.reads_beyond(allowed), [str(data)])
            self.assertEqual(list(Path(elsewhere).iterdir()), [])


class ExactCountryRisk(unittest.TestCase):
    """The country-risk example's exact run stays in rational arithmetic."""

    def test_exact_example_is_rational_throughout(self) -> None:
        """Every exact result is a Fraction, equal to its rational closed form."""
        exact = country_risk_premium.example(Fraction)
        self.assertTrue(all(type(value) is Fraction for value in exact.values()), exact)
        self.assertEqual(exact["crp relative sd"], Fraction(10, 3))
        self.assertEqual(exact["ke weighted"], Fraction(331, 25))
        self.assertEqual(exact["ke local inflation"], Fraction(87672, 5125))  # 17.1067317...
        self.assertTrue(all(type(v) is float for v in country_risk_premium.example(float).values()))

    def test_premium_formulas_keep_their_input_type(self) -> None:
        """The premium formulas return Fraction for Fraction inputs and float for floats."""
        third = Fraction(1, 3)
        self.assertIs(type(country_risk_premium.relative_sd_crp(third, third, third)), Fraction)
        self.assertIs(type(country_risk_premium.melded_crp(third, third, third)), Fraction)
        self.assertIs(type(country_risk_premium.default_spread_crp(third)), Fraction)
        self.assertIs(type(country_risk_premium.melded_crp(2.25, 24, 17)), float)


class CashFlowLinkage(unittest.TestCase):
    """The cash-flow example derives closing cash from the balances, in integers."""

    def test_closing_cash_follows_the_balances(self) -> None:
        """A receivable one higher lowers derived cash by one; the balance sheet still balances."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            base = cash_flow_linkage.check_indirect_from_operating_profit(
                report, cash_flow_linkage.check_roll_forwards(report)
            )
            raised = replace(cash_flow_linkage.CLOSING, receivables=151)
            with mock.patch.object(cash_flow_linkage, "CLOSING", raised):
                movements = cash_flow_linkage.check_roll_forwards(report)
                moved = cash_flow_linkage.check_indirect_from_operating_profit(report, movements)
                cash_flow_linkage.check_balance_sheets(report, moved.close_cash)
        self.assertEqual((base.close_cash, moved.close_cash), (97, 96))
        self.assertEqual(report.failures, ["operating cash flow", "closing cash"])

    def test_statement_amounts_are_integers(self) -> None:
        """The roll-forwards and the derived sections stay in integer arithmetic."""
        with contextlib.redirect_stdout(io.StringIO()):
            report = CheckReport()
            movements = cash_flow_linkage.check_roll_forwards(report)
            flows = cash_flow_linkage.check_indirect_from_operating_profit(report, movements)
        amounts = [*vars(movements).values(), *vars(flows).values()]
        self.assertTrue(all(type(amount) is int for amount in amounts), amounts)


class RootFinders(unittest.TestCase):
    """The two bisection routines keep their different contracts."""

    def test_time_value_bisect_rejects_bad_brackets(self) -> None:
        """Bad brackets raise ValueError with their own message, before any iteration."""
        bisect = time_value_returns.bisect
        with self.assertRaisesRegex(ValueError, r"^bracket needs lo < hi$"):
            bisect(lambda x: x, 1.0, 1.0)
        with self.assertRaisesRegex(ValueError, r"^ends of the bracket have the same sign$"):
            bisect(lambda x: x, 1.0, 2.0)

    def test_time_value_bisect_returns_exact_roots_and_midpoints(self) -> None:
        """Exact roots at an end or a midpoint return as they are; otherwise n halvings."""
        bisect = time_value_returns.bisect
        self.assertEqual(bisect(lambda x: x - 0.5, 0.0, 1.0), 0.5)
        self.assertEqual(bisect(lambda x: x, 0.0, 1.0), 0.0)
        self.assertEqual(bisect(lambda x: x - 0.3, 0.0, 1.0, n=0), 0.5)
        self.assertEqual(bisect(lambda x: x - 0.3, 0.0, 1.0, n=1), 0.25)

    def test_implied_volatility_does_not_validate_its_bracket(self) -> None:
        """A price beyond the bracket returns about the nearer end instead of raising."""
        case = bsm_svi.CASE
        high = bsm_svi.bs(case.S, case.K, case.r, case.q, 9.0, case.T)
        iv = bsm_svi.implied(high, case.S, case.K, case.r, case.q, case.T)
        self.assertAlmostEqual(iv, 5.0, places=9)


D = dt.date
OPEN = D(9999, 12, 31)


def corrected_history() -> bitemporal.SplitHistory:
    """Return the example's history: a 2-for-1 split recorded on 3 March, corrected on 20 March."""
    history = bitemporal.SplitHistory(
        [bitemporal.SplitRow(D(2000, 1, 1), OPEN, D(2000, 1, 1), OPEN, 1.0)]
    )
    history.record(D(2026, 3, 3), D(2026, 3, 2), 2.0)
    history.record(D(2026, 3, 20), D(2026, 3, 2), 1.5)
    return history


class BitemporalHistory(unittest.TestCase):
    """A split history is append-only, inclusive at its boundaries and owned by one instance."""

    def test_correction_closes_and_appends_rows(self) -> None:
        """Both records leave every earlier row, closed or replaced, in lookup order."""
        row = bitemporal.SplitRow
        self.assertEqual(
            corrected_history().rows,
            (
                row(D(2000, 1, 1), D(2026, 3, 2), D(2000, 1, 1), OPEN, 1.0),  # seed, closed
                row(D(2026, 3, 3), OPEN, D(2000, 1, 1), D(2026, 3, 1), 1.0),  # pre-split remainder
                row(D(2026, 3, 3), D(2026, 3, 19), D(2026, 3, 2), OPEN, 2.0),  # first entry, closed
                row(D(2026, 3, 20), OPEN, D(2026, 3, 2), OPEN, 1.5),  # correction
            ),
        )

    def test_boundaries_are_inclusive(self) -> None:
        """Record and actual ranges include both ends, the sentinel date included."""
        factor = corrected_history().factor_at
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 2)), 1.0)
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 3)), 2.0)
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 19)), 2.0)
        self.assertEqual(factor(D(2026, 3, 5), D(2026, 3, 20)), 1.5)
        self.assertEqual(factor(D(2026, 3, 1), D(2026, 10, 17)), 1.0)
        self.assertEqual(factor(D(2026, 3, 2), D(2026, 10, 17)), 1.5)
        self.assertEqual(factor(OPEN, OPEN), 1.5)

    def test_no_matching_row_gives_no_split(self) -> None:
        """Dates outside every row, or an empty history, give the factor 1.0."""
        self.assertEqual(bitemporal.SplitHistory().factor_at(D(2026, 3, 5), D(2026, 10, 17)), 1.0)
        self.assertEqual(corrected_history().factor_at(D(1999, 12, 31), D(2026, 10, 17)), 1.0)
        self.assertEqual(corrected_history().factor_at(D(2026, 3, 5), D(1999, 12, 31)), 1.0)

    def test_instances_do_not_share_history(self) -> None:
        """Recording into one history changes neither another nor the rows it started from."""
        seed = [bitemporal.SplitRow(D(2000, 1, 1), OPEN, D(2000, 1, 1), OPEN, 1.0)]
        first, second = bitemporal.SplitHistory(seed), bitemporal.SplitHistory(seed)
        first.record(D(2026, 3, 3), D(2026, 3, 2), 2.0)
        self.assertEqual(len(first.rows), 3)
        self.assertEqual(second.rows, tuple(seed))
        self.assertEqual(len(seed), 1)
        self.assertEqual(bitemporal.SplitHistory().rows, ())


class FilingTimestamps(unittest.TestCase):
    """Availability is recorded or unknown; the deemed filing date and lower bound stay apart."""

    def test_unknown_availability_stays_none(self) -> None:
        """Without recorded times availability is None, whatever else the record holds."""
        record = filing_timestamps.FilingRecord(
            "10-K", dt.datetime(2026, 11, 19, 18, 0), period=D(2026, 9, 30)
        )
        self.assertIsNone(filing_timestamps.available_at(record))
        self.assertEqual(filing_timestamps.not_before(record), dt.datetime(2026, 11, 20, 6, 0))

    def test_dissemination_takes_precedence(self) -> None:
        """A recorded dissemination wins even over an earlier first observation."""
        both = filing_timestamps.FilingRecord(
            "10-K",
            dt.datetime(2026, 11, 19, 9, 0),
            disseminated=dt.datetime(2026, 11, 19, 9, 30),
            first_observed=dt.datetime(2026, 11, 19, 9, 10),
        )
        seen = replace(both, disseminated=None)
        self.assertEqual(filing_timestamps.available_at(both), dt.datetime(2026, 11, 19, 9, 30))
        self.assertEqual(filing_timestamps.available_at(seen), dt.datetime(2026, 11, 19, 9, 10))

    def test_cutoffs_are_inclusive(self) -> None:
        """A start at 17:30 (22:00 for late forms) is filed that day; a second later is not."""
        filed = filing_timestamps.filing_date
        self.assertEqual(filed("10-K", dt.datetime(2026, 11, 19, 17, 30)), D(2026, 11, 19))
        self.assertEqual(filed("10-K", dt.datetime(2026, 11, 19, 17, 30, 1)), D(2026, 11, 20))
        self.assertEqual(filed("4/A", dt.datetime(2026, 11, 19, 22, 0)), D(2026, 11, 19))
        self.assertEqual(filed("4/A", dt.datetime(2026, 11, 19, 22, 0, 1)), D(2026, 11, 20))
        bound = filing_timestamps.not_before
        at_cutoff = filing_timestamps.FilingRecord("10-K", dt.datetime(2026, 11, 19, 17, 30))
        self.assertEqual(bound(at_cutoff), at_cutoff.accepted)
        late = replace(at_cutoff, accepted=dt.datetime(2026, 11, 19, 17, 30, 1))
        self.assertEqual(bound(late), dt.datetime(2026, 11, 20, 6, 0))

    def test_amendments_follow_their_base_form(self) -> None:
        """An /A form takes its base form's cutoff and dissemination treatment."""
        bound = filing_timestamps.not_before
        f4a = filing_timestamps.FilingRecord("4/A", dt.datetime(2026, 11, 19, 19, 0))
        tenka = filing_timestamps.FilingRecord("10-K/A", dt.datetime(2026, 11, 19, 19, 0))
        self.assertEqual(bound(f4a), f4a.accepted)
        self.assertEqual(bound(tenka), dt.datetime(2026, 11, 20, 6, 0))

    def test_non_business_days(self) -> None:
        """A weekend start is filed the next business day; the fixed holidays are skipped."""
        filed = filing_timestamps.filing_date
        self.assertEqual(filed("10-K", dt.datetime(2026, 11, 21, 9, 0)), D(2026, 11, 23))
        self.assertEqual(filing_timestamps.next_business_day(D(2026, 12, 24)), D(2026, 12, 28))


class FilingDeadlines(unittest.TestCase):
    """The computed federal-holiday calendar of the deadline example."""

    def test_observed_fixed_date_holidays(self) -> None:
        """A Saturday holiday is observed on Friday, a Sunday one on Monday."""
        self.assertIn(D(2026, 7, 3), filing_deadlines.holidays(2026))
        self.assertNotIn(D(2026, 7, 4), filing_deadlines.holidays(2026))
        self.assertIn(D(2027, 7, 5), filing_deadlines.holidays(2027))
        self.assertIn(D(2027, 12, 24), filing_deadlines.holidays(2027))
        self.assertEqual(len(filing_deadlines.holidays(2026)), 11)

    def test_last_weekday_including_december(self) -> None:
        """The last Monday of May and of December (the year-end branch)."""
        self.assertEqual(filing_deadlines.last_weekday(2026, 5, 0), D(2026, 5, 25))
        self.assertEqual(filing_deadlines.last_weekday(2026, 12, 0), D(2026, 12, 28))

    def test_business_day_steps(self) -> None:
        """A business day rolls to itself; add_bd skips a holiday and counts from the next day."""
        self.assertEqual(filing_deadlines.roll(D(2026, 11, 16)), D(2026, 11, 16))
        self.assertEqual(filing_deadlines.add_bd(D(2026, 11, 10), 1), D(2026, 11, 12))
        self.assertEqual(filing_deadlines.add_bd(D(2026, 11, 10), 0), D(2026, 11, 10))


class FundingReporting(unittest.TestCase):
    """perpetual_funding's report: its own line format, tolerance and silent mismatches."""

    def test_lines_and_relative_or_absolute_tolerance(self) -> None:
        """Lines show got and want to 12 digits; tol is absolute below 1 and relative above."""
        report = FundingReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.check("zero", 1e-12, 0.0)
            report.check("zero, beyond", 1.1e-12, 0.0)
            report.check("large", 1000 + 0.9e-9, 1000.0)
            report.check("large, beyond", 1000 + 2e-9, 1000.0)
            report.check("loose", 1.5, 1.0, tol=0.5)
        self.assertEqual(
            out.getvalue(),
            "ok   zero: got 1e-12, want 0\n"
            "FAIL zero, beyond: got 1.1e-12, want 0\n"
            "ok   large: got 1000, want 1000\n"
            "FAIL large, beyond: got 1000, want 1000\n"
            "ok   loose: got 1.5, want 1\n",
        )
        self.assertEqual(report.failures, ["zero, beyond", "large, beyond"])

    def test_mismatches_are_silent_and_belong_to_one_report(self) -> None:
        """A mismatch prints nothing; the failure list is a copy, and a new report is empty."""
        report = FundingReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.mismatch("grid cap=0.5 p=0.03")
        self.assertEqual(out.getvalue(), "")
        report.failures.append("tampered")
        self.assertEqual(report.failures, ["grid cap=0.5 p=0.03"])
        self.assertEqual(FundingReport().failures, [])

    def test_grid_mismatches_accumulate_without_lines(self) -> None:
        """A wrong piecewise rule fails the grid silently: one status line, every point counted."""
        piecewise = perpetual_funding.piecewise

        def shrink_too_far(premium: float, cap: float) -> float:
            # Above the band, shrink by 0.03 instead of the damper's 0.025.
            if premium > perpetual_funding.DAMPER:
                return min(cap, max(-cap, premium - 0.03))
            return piecewise(premium, cap)

        with mock.patch.object(perpetual_funding, "piecewise", shrink_too_far):
            status, out = captured(perpetual_funding.main)
        self.assertEqual(status, 1)
        self.assertIn("\n   grid mismatch\n2. Worked examples", out)
        self.assertEqual(len(OK_FAIL_LINE.findall(out)), 17)
        self.assertNotIn("FAIL", out)
        self.assertTrue(
            out.endswith(
                "\n1300 check(s) failed: ['grid cap=0.5 p=0.03', 'grid cap=0.5 p=0.035', "
                "'grid cap=0.5 p=0.04', 'grid cap=0.5 p=0.045', 'grid cap=0.5 p=0.05']\n"
            )
        )


class PerpetualFunding(unittest.TestCase):
    """The printed closed form and the piecewise prose rule, in percent per 8 hours."""

    def test_routes_agree_at_band_edges_and_caps(self) -> None:
        """Both routes give zero on the damper band edges and the cap beyond it."""
        for route in (perpetual_funding.closed_form, perpetual_funding.piecewise):
            with self.subTest(route.__name__):
                self.assertEqual(route(0.025, 0.5), 0.0)
                self.assertEqual(route(-0.025, 0.5), 0.0)
                self.assertAlmostEqual(route(0.1, 0.5), 0.075, places=15)
                self.assertAlmostEqual(route(-0.1, 0.5), -0.075, places=15)
                self.assertEqual(route(3.0, 0.5), 0.5)
                self.assertEqual(route(-3.0, 0.5), -0.5)

    def test_premium_rate_is_in_percent(self) -> None:
        """A mark 0.075% over the index gives 0.075, not 0.00075."""
        self.assertAlmostEqual(perpetual_funding.premium_rate(100_075, 100_000), 0.075, places=12)


class MarginSpiral(unittest.TestCase):
    """The loop series is summed independently of the closed form it is checked against."""

    def test_series_and_closed_form_are_independent(self) -> None:
        """Both give 1/(k - l) = 2 at k = 1, l = 0.5; a wrong closed form fails the check."""
        self.assertEqual(margin_spiral.price_response(1.0, 0.5), 2.0)
        self.assertAlmostEqual(margin_spiral.series_response(1.0, 0.5), 2.0, places=12)
        self.assertEqual(margin_spiral.loop_strengths(), (1.0, 0.2, 0.3))

        def wrong(k: float, ell: float) -> float:
            return 1 / (k - ell) + 1e-9

        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            with mock.patch.object(margin_spiral, "price_response", wrong):
                margin_spiral.check_series(report)
        self.assertEqual(report.failures, ["series = closed form (2.000000 vs 2.000000)"])

    def test_negative_loss_loop_is_not_super_additive(self) -> None:
        """With x0 < 0 the loss loop dampens, and the joint extra falls below the sum."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            with mock.patch.object(margin_spiral, "X0", -0.3):
                margin_spiral.check_amplification(report)
        self.assertEqual(
            report.failures,
            [
                "loss spiral amplifies: 0.7692 > 1.0000",
                "joint extra -0.0909 > sum of separate extras 0.0192",
            ],
        )


class CmeAllocation(unittest.TestCase):
    """Pro Rata flooring and minimum, Leveling order, Split rounding and FIFO."""

    def test_pro_rata_floors_then_applies_the_minimum(self) -> None:
        """Shares are floored before the minimum; a share equal to PR Min is allocated."""
        self.assertEqual(cme_allocation.pro_rata([1, 1, 1], 2), [0, 0, 0])
        self.assertEqual(cme_allocation.pro_rata([2, 1, 1], 8), [4, 2, 2])
        self.assertEqual(cme_allocation.apply_minimum([1, 2, 3], 2), [0, 2, 3])

    def test_leveling_by_quantity_then_time(self) -> None:
        """Only unallocated orders qualify, larger first, then earlier; one lot each."""
        self.assertEqual(cme_allocation.leveling_order([5, 5, 9, 7], [0, 0, 0, 2]), [2, 0, 1])
        self.assertEqual(cme_allocation.leveling([5, 5, 9, 7], [0, 0, 0, 2], 2), [1, 0, 1, 0])
        self.assertEqual(cme_allocation.leveling([5, 5, 9, 7], [0, 0, 0, 2], 9), [1, 1, 1, 0])

    def test_split_rounds_fifo_up_and_fifo_fills_in_time_order(self) -> None:
        """The FIFO part of a Split is rounded up; FIFO stops when the lots run out."""
        self.assertEqual(cme_allocation.split_fifo(49, 20), 10)
        self.assertEqual(cme_allocation.split_fifo(49, 1), 1)
        quantities = [5, 9, 57]
        self.assertEqual(cme_allocation.fifo(quantities, 10), [0, 4, 57])
        self.assertEqual(cme_allocation.fifo(quantities, 100), [0, 0, 0])
        self.assertEqual(quantities, [5, 9, 57])

    def test_expected_allocations_are_not_derived_from_the_rules(self) -> None:
        """A higher PR Min changes the allocations, so the page's printed values fail."""
        with mock.patch.object(cme_allocation, "PR_MIN", 8):
            status, out = captured(cme_allocation.main)
        self.assertEqual(status, 1)
        self.assertIn("  BAD Pro Rata allocated (PR Min 2): [0, 0, 0, 0, 0, 37]", out)
        self.assertIn("  BAD lots left for Leveling: 13 (want 3)", out)


class AbsoluteToleranceLines(unittest.TestCase):
    """Each script keeps its own number format; all three use an absolute tolerance."""

    def test_commodity_latency_prints_four_decimals(self) -> None:
        """Four decimals for got, want and tol as given; |got - want| = tol passes."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            commodity_latency.near(report, "edge", 1.5, 1.0, 0.5)
            commodity_latency.near(report, "beyond", 1.5, 1, 0.25)
        self.assertEqual(
            out.getvalue(),
            "  ok  edge: 1.5000 (want 1.0, tol 0.5)\n  BAD beyond: 1.5000 (want 1, tol 0.25)\n",
        )
        self.assertEqual(report.failures, ["beyond"])

    def test_contract_statistics_prints_six_decimals(self) -> None:
        """The got value has six decimals, and the default tolerance is 1e-9."""
        report = CheckReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            contract_statistics.near(report, "sum", 100, 100)
            contract_statistics.near(report, "off", 100.0 + 1e-6, 100.0)
        self.assertEqual(
            out.getvalue(),
            "  ok  sum: 100.000000 (want 100, tol 1e-09)\n"
            "  BAD off: 100.000001 (want 100.0, tol 1e-09)\n",
        )

    def test_synthetic_short_tolerance_is_not_relative(self) -> None:
        """1e-6 is absolute even for large values, unlike perpetual_funding's relative one."""
        report = ShortReport()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            report.check("close", 1000.0000005, 1000.0)
            report.check("far", 1000.000002, 1000.0)
        self.assertEqual(
            out.getvalue(),
            "ok   close: got 1000.000001, want 1000.000000\n"
            "FAIL far: got 1000.000002, want 1000.000000\n",
        )
        self.assertEqual(report.failures, ["far"])
        self.assertEqual(ShortReport().failures, [])


class SyntheticShort(unittest.TestCase):
    """Quadrature, closed forms and daily cash accounts stay independent routes."""

    def test_simple_daily_interest_fails_the_rebate_checks(self) -> None:
        """Accounts credited at simple daily rates miss the closed forms; nothing else fails."""

        def simple(start: float, rate: float, T: float, days: int = 365) -> float:
            bal = start
            for _ in range(days):
                bal *= 1 + rate * T / days
            return bal

        with mock.patch.object(synthetic_short, "account", simple):
            status, out = captured(synthetic_short.main)
        self.assertEqual(status, 1)
        failed = [line for line in out.splitlines() if line.startswith("FAIL")]
        self.assertEqual(len(failed), 21)
        self.assertTrue(all("r_b=" in line or "package, S_T=" in line for line in failed))
        self.assertTrue(out.endswith("\n21 check(s) failed\n"))

    def test_quadrature_does_not_use_the_closed_form(self) -> None:
        """A shifted closed form fails both quadrature comparisons."""
        bs = synthetic_short.bs

        def shifted(
            S: float, K: float, r: float, q: float, s: float, T: float
        ) -> tuple[float, float]:
            call, put = bs(S, K, r, q, s, T)
            return call + 1e-3, put + 1e-3

        report = ShortReport()
        with contextlib.redirect_stdout(io.StringIO()):
            with mock.patch.object(synthetic_short, "bs", shifted):
                synthetic_short.check_parity(report)
        self.assertEqual(
            report.failures,
            ["   call, quadrature vs closed form", "   put, quadrature vs closed form"],
        )


class IsmCalendar(unittest.TestCase):
    """The ISM exceptions are stated, not derived: a changed release date is reported."""

    def test_changed_release_date_is_printed_and_fails(self) -> None:
        """A February Services date moved by one day joins the printed mismatches."""
        moved = {**contract_statistics.ISM_2026, 2: (2, 5)}
        with mock.patch.object(contract_statistics, "ISM_2026", moved):
            status, out = captured(contract_statistics.main)
        self.assertEqual(status, 1)
        self.assertIn(
            "  federal-holiday rule vs ISM (month, rule, ISM): "
            "[(1, (2, 6), (5, 7)), (2, (2, 4), (2, 5)), (4, (1, 3), (1, 6))]\n",
            out,
        )
        self.assertTrue(
            out.endswith(
                "\nFAILED: ['months where the plain rule differs', "
                '"all twelve months with ISM\'s 2 January and Good Friday skipped"]\n'
            )
        )

    def test_business_days_skip_weekends_and_listed_days(self) -> None:
        """Thursday 1 January 2026 is skipped as a holiday, so the first business day is the 2nd."""
        holidays = contract_statistics.federal_holidays(2026)
        self.assertEqual(contract_statistics.business_day(2026, 1, 1, holidays), 2)
        self.assertEqual(contract_statistics.business_day(2026, 1, 1, set()), 1)
        self.assertEqual(contract_statistics.business_day(2026, 2, 1, holidays), 2)


if __name__ == "__main__":
    unittest.main()
