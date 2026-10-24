"""Tests of the per-check reports, the numerical checks and the numerical demonstrations.

The numerical assertions themselves are the checks' own; these tests only confirm how a run
is reported, that each run starts fresh and leaves shared state alone, and that a failure
reaches the exit status. A demonstration prints values and asserts nothing, so only its runs,
not a failure contract, are tested here.

Run: make test (uv run --frozen --no-editable pytest)
"""

import ast
import contextlib
import datetime as dt
import io
import os
import pkgutil
import py_compile
import random
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from types import CodeType, ModuleType
from typing import Final
from unittest import mock

import numpy as np
import pytest
from pydantic import Field

import trading_notes.numerical
from trading_notes.numerical import (
    afml,
    amm_pool,
    asset_pricing_factor_models,
    bitemporal,
    capital_market_expectations,
    cartea_jaimungal,
    commodity_returns,
    concentrated_position,
    covariance_shrinkage,
    covariance_volatility,
    currency_management,
    digital_assets,
    economic_growth,
    etf_mechanics,
    filing_deadlines,
    filing_timestamps,
    financial_labels,
    financial_ml_methods,
    forecast_scaling,
    fx_mechanics,
    fx_panel_inference,
    garch_ewma,
    index_construction,
    institutional_portfolios,
    intercorporate_fx_institutions,
    linear_projection,
    macro_policy_trade,
    macro_pricing_risk,
    macro_valuation,
    margin_spiral,
    monte_carlo_greeks,
    negative_hedge_ratio,
    numerical_pricing,
    order_reconciliation,
    order_routing_fragmentation,
    perpetual_funding,
    private_capital,
    private_wealth,
    purged_cv,
    real_assets,
    synthetic_short,
    time_value_returns,
    us_calendar,
)
from trading_notes.numerical.active_management import active_management_checks as active_management
from trading_notes.numerical.alternatives_allocation import (
    alternatives_allocation_checks as alternatives_allocation,
)
from trading_notes.numerical.arbitrage_free_valuation import (
    short_rate_model_checks as short_rate_model,
)
from trading_notes.numerical.backtest_evaluation import backtest_design_checks as backtest_design
from trading_notes.numerical.backtest_evaluation import (
    drawdown_resampling_checks as drawdown_resampling,
)
from trading_notes.numerical.backtest_evaluation import multiple_testing_checks as multiple_testing
from trading_notes.numerical.backtest_evaluation import (
    sharpe_conditions_checks as sharpe_conditions,
)
from trading_notes.numerical.backtest_evaluation import (
    sharpe_statistics_checks as sharpe_statistics,
)
from trading_notes.numerical.backtest_evaluation import sharpe_zero_checks as sharpe_zero
from trading_notes.numerical.bond_pricing_yields import bond_valuation_checks as bond_valuation_risk
from trading_notes.numerical.capital_structure_cost_of_capital import (
    country_risk_premium_checks as country_risk_premium,
)
from trading_notes.numerical.capital_structure_cost_of_capital.country_risk import CountryRisk
from trading_notes.numerical.cash_flow_analysis import cash_flow_linkage_checks as cash_flow_linkage
from trading_notes.numerical.company_case import statement_analysis_checks as statement_analysis
from trading_notes.numerical.corporate_finance import corporate_finance_checks as corporate_finance
from trading_notes.numerical.counterparty_xva import (
    counterparty_capital_checks as counterparty_capital,
)
from trading_notes.numerical.counterparty_xva import counterparty_xva_checks as counterparty_xva
from trading_notes.numerical.credit_portfolio_management import (
    credit_portfolios_checks as credit_portfolios,
)
from trading_notes.numerical.credit_risk_analysis import (
    credit_cds_securitisation_checks as credit_cds_securitisation,
)
from trading_notes.numerical.default_correlation import (
    default_correlation_checks as default_correlation,
)
from trading_notes.numerical.derivative_overlays import (
    derivative_overlays_checks as derivative_overlays,
)
from trading_notes.numerical.derivative_overlays import (
    seasoned_variance_swap_checks as seasoned_variance_swap,
)
from trading_notes.numerical.descriptive_statistics import (
    statistics_probability_checks as statistics_probability,
)
from trading_notes.numerical.embedded_option_bonds import (
    rate_tree_checks as rate_tree_embedded_options,
)
from trading_notes.numerical.equity_portfolio_management import (
    equity_portfolio_management_checks as equity_portfolio_management,
)
from trading_notes.numerical.exotic_options import exotic_options_checks as exotic_options
from trading_notes.numerical.exotic_options import lookback_options_checks as lookback_options
from trading_notes.numerical.extreme_values import extreme_value_checks as extreme_value
from trading_notes.numerical.firms_market_structure import (
    market_structure_checks as market_structure,
)
from trading_notes.numerical.fixed_income_portfolio_management import (
    fixed_income_portfolio_checks as fixed_income_portfolio,
)
from trading_notes.numerical.forward_commitment_valuation import (
    cross_currency_basis_checks as cross_currency_basis,
)
from trading_notes.numerical.forward_commitment_valuation import (
    forward_swap_valuation_checks as forward_swap_valuation,
)
from trading_notes.numerical.futures_execution import (
    contract_statistics_checks as contract_statistics,
)
from trading_notes.numerical.hedge_fund_strategies import hedge_funds_checks as hedge_funds
from trading_notes.numerical.high_frequency_trading import (
    dealer_queue_information_checks as dealer_queue_information,
)
from trading_notes.numerical.interest_rates import yield_shift_checks as yield_shift
from trading_notes.numerical.investment_process_planning import (
    investment_planning_checks as investment_planning,
)
from trading_notes.numerical.manager_selection import manager_selection_checks as manager_selection
from trading_notes.numerical.market_making_models import (
    lob_model_derivations_checks as lob_model_derivations,
)
from trading_notes.numerical.market_making_models import lob_models_checks as lob_models
from trading_notes.numerical.market_organisation import (
    liquidity_market_design_checks as liquidity_market_design,
)
from trading_notes.numerical.market_risk_measurement import (
    market_risk_measurement_checks as market_risk_measurement,
)
from trading_notes.numerical.money_markets import funding_repo_checks as funding_repo
from trading_notes.numerical.multiple_regression import (
    multiple_regression_checks as multiple_regression,
)
from trading_notes.numerical.option_hedging import (
    transaction_cost_hedging_checks as transaction_cost_hedging,
)
from trading_notes.numerical.option_hedging import (
    volatility_mismatch_hedging_checks as volatility_mismatch_hedging,
)
from trading_notes.numerical.option_pricing import bsm_svi_checks as bsm_svi
from trading_notes.numerical.option_pricing import option_models_checks as option_models
from trading_notes.numerical.option_strategies import option_strategies_checks as option_strategies
from trading_notes.numerical.option_valuation import (
    dividend_tree_swaption_checks as dividend_tree_swaption,
)
from trading_notes.numerical.option_valuation import option_valuation_checks as option_valuation
from trading_notes.numerical.order_books import cme_allocation_checks as cme_allocation
from trading_notes.numerical.order_books import commodity_latency_checks as commodity_latency
from trading_notes.numerical.order_books import matching_allocation
from trading_notes.numerical.order_flow_statistics import (
    market_estimators_rules_checks as market_estimators_rules,
)
from trading_notes.numerical.order_flow_statistics import order_flow_checks as order_flow
from trading_notes.numerical.performance_attribution_appraisal import (
    performance_evaluation_checks as performance_evaluation,
)
from trading_notes.numerical.performance_standards import gips_checks as gips
from trading_notes.numerical.perpetual_funding import FundingReport
from trading_notes.numerical.portfolio_choice import portfolio_choice_checks as portfolio_choice
from trading_notes.numerical.portfolio_construction_models import (
    black_litterman_checks as black_litterman,
)
from trading_notes.numerical.portfolio_construction_models import (
    equal_risk_contribution_checks as equal_risk_contribution,
)
from trading_notes.numerical.portfolio_construction_models import erc_sharpe_checks as erc_sharpe
from trading_notes.numerical.portfolio_construction_models import (
    kelly_growth_checks as kelly_growth,
)
from trading_notes.numerical.portfolio_construction_models import mean_cvar_checks as mean_cvar
from trading_notes.numerical.portfolio_construction_models import risk_parity_checks as risk_parity
from trading_notes.numerical.portfolio_moments import portfolio_moments_checks as portfolio_moments
from trading_notes.numerical.rate_swaps_clearing import fra_settlement_checks as fra_settlement
from trading_notes.numerical.rate_swaps_clearing import multicurve_checks as multicurve
from trading_notes.numerical.records import Record
from trading_notes.numerical.regression import linear_regression_checks as linear_regression
from trading_notes.numerical.report import CheckReport, require, section
from trading_notes.numerical.scenario_simulation import (
    scenario_simulation_checks as scenario_simulation,
)
from trading_notes.numerical.securities_lending import margin_purchase_checks as margin_purchase
from trading_notes.numerical.statistical_inference import (
    correlation_independence_checks as correlation_independence,
)
from trading_notes.numerical.statistical_inference import (
    inference_simulation_checks as inference_simulation,
)
from trading_notes.numerical.stochastic_calculus import (
    stochastic_calculus_checks as stochastic_calculus,
)
from trading_notes.numerical.strategic_asset_allocation import (
    strategic_asset_allocation_checks as strategic_asset_allocation,
)
from trading_notes.numerical.synthetic_short import ShortReport
from trading_notes.numerical.systematic_equities import (
    equity_fcf_ri_private_checks as equity_fcf_ri_private,
)
from trading_notes.numerical.systematic_equities import equity_valuation_checks as equity_valuation
from trading_notes.numerical.term_structure_returns import term_structure_checks as term_structure
from trading_notes.numerical.time_series_models import time_series_checks as time_series
from trading_notes.numerical.trade_strategy_governance import (
    trade_execution_checks as trade_execution,
)
from trading_notes.numerical.var_es_estimation import (
    expected_shortfall_checks as expected_shortfall,
)
from trading_notes.numerical.var_es_estimation import var_backtest_checks as var_backtest

from ..import_probe import HEAVY, dependency_reads, import_effects
from .single_run import PRIMING_SEED, GlobalState, prime_global_random, restored_global_state
from .stand_ins import (
    Forced,
    forced_condition_failure,
    forced_failure,
    forced_list_failure,
    forced_value_failure,
    no_conditions,
    run_main,
    skipped,
    unused_value,
)

ROOT = Path(__file__).resolve().parents[3]
ARTEFACTS = ROOT / "notes" / "artefacts"
# A reported check line of CheckReport, of the ok/FAIL reports of perpetual_funding,
# synthetic_short and lob_model_derivations, and of the modules that print failed conditions
# only: covariance_shrinkage, drawdown_resampling, multiple_testing, dealer_queue_information,
# liquidity_market_design, order_flow, order_routing_fragmentation and macro_pricing_risk.
CHECK_LINE = re.compile(r"^  (ok |BAD) ", re.M)
OK_FAIL_LINE = re.compile(r"^(ok  |FAIL) ", re.M)
# fx_panel_inference prints PASS or FAIL lines and no summary.
PASS_FAIL_LINE = re.compile(r"^(PASS|FAIL)  ", re.M)
BAD_ONLY_LINE = re.compile(r"^(BAD) ", re.M)
# At most this many example processes run at once: one per CPU.
MAX_PROCESSES: Final = os.cpu_count() or 4


class NumericalCheck(Record):
    """A numerical check module and what its tests expect of it.

    Attributes:
        module: The implementation module, with `main()`, run as `python -m <module>`.
        script: Its forwarding script under notes/artefacts/, or None once the module has moved
            into a package and the script is retired.
        replaced: A function after which the in-process tests record one more, forced, failure.
        summary: The end of its output with that one forced failure: the failure summary,
            or the BAD line itself for a script that prints none.
        checks: The number of check lines a passing run prints; 0 for a module that prints
            only its failures.
        line: Matches each reported check line; group 1 is its status.
        forced: How the failure after `replaced` is recorded, one of `stand_ins.forced_*`.
        passed: The end of a passing run's output; empty for a module that prints no summary.
        imports: The modules it imports for its heavy dependencies (of `HEAVY`), as it
            imports them. Importing it must load exactly their packages, and open no file
            beyond those they open when imported alone.
        args: Command-line arguments of its runs, such as the repository root of a module that
            reads compendium or research files.
        stand_ins: Module attributes replaced in the in-process runs only: expensive check
            functions by `skipped` or `no_conditions`, simulation sizes by small values. The
            full run always uses the real ones.
    """

    module: ModuleType
    script: Path | None
    replaced: str
    summary: str
    checks: int
    line: re.Pattern[str] = CHECK_LINE
    forced: Forced = forced_failure
    passed: str = "all checks passed\n"
    imports: tuple[str, ...] = ()
    args: tuple[str, ...] = ()
    stand_ins: dict[str, object] = Field(default_factory=dict)


class Demonstration(Record):
    """A numerical module that prints values to be read and asserts nothing.

    Its `main()` always returns 0, so it has no failure contract to test.

    Attributes:
        module: The implementation module, with `main()`, run as `python -m <module>`.
        script: Its forwarding script under notes/artefacts/, or None once it is retired.
        lines: The number of lines a run prints.
        imports: The modules it imports for its heavy dependencies (of `HEAVY`), as it
            imports them. Importing it must load exactly their packages, and open no file
            beyond those they open when imported alone.
    """

    module: ModuleType
    script: Path | None
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
        module=funding_repo,
        script=None,
        replaced="check_margin_call",
        summary="\n1 check(s) failed: ['forced failure']\n",
        checks=11,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=fra_settlement,
        script=None,
        replaced="check_convexity",
        summary=LIST_SUMMARY,
        checks=11,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=multicurve,
        script=None,
        replaced="check_two_curves",
        summary=LIST_SUMMARY,
        checks=6,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=amm_pool,
        script=ARTEFACTS / "crypto-perpetuals" / "amm-checks.py",
        replaced="check_concentrated_position",
        summary=LIST_SUMMARY,
        checks=12,
    ),
    NumericalCheck(
        module=country_risk_premium,
        script=None,
        replaced="check_zero_limit",
        summary=JOINED_SUMMARY,
        checks=23,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=cash_flow_linkage,
        script=None,
        replaced="check_cash_tax",
        summary=JOINED_SUMMARY,
        checks=34,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=bsm_svi,
        script=None,
        replaced="check_svi",
        summary=JOINED_SUMMARY,
        checks=23,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=time_value_returns,
        script=ARTEFACTS / "time-value-returns" / "time-value-return-checks.py",
        replaced="check_share_forward",
        summary="\nFAILED: forced failure\n",
        checks=114,
    ),
    NumericalCheck(
        module=bitemporal,
        script=ARTEFACTS / "point-in-time-data" / "bitemporal-check.py",
        replaced="check_split_correction",
        summary=NO_SUMMARY,
        checks=4,
    ),
    NumericalCheck(
        module=filing_deadlines,
        script=ARTEFACTS / "point-in-time-data" / "filing-checks.py",
        replaced="check_deadlines",
        summary=LIST_SUMMARY,
        checks=8,
    ),
    NumericalCheck(
        module=filing_timestamps,
        script=ARTEFACTS / "point-in-time-data" / "filing-timestamp-checks.py",
        replaced="check_holiday_cutoff",
        summary=LIST_SUMMARY,
        checks=18,
    ),
    NumericalCheck(
        module=margin_spiral,
        script=ARTEFACTS / "funding-crowding" / "spiral-checks.py",
        replaced="check_amplification",
        summary=LIST_SUMMARY,
        checks=4,
    ),
    NumericalCheck(
        module=cme_allocation,
        script=None,
        replaced="check_fifo",
        summary=LIST_SUMMARY,
        checks=12,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=perpetual_funding,
        script=ARTEFACTS / "crypto-mm-microstructure" / "funding_checks.py",
        replaced="check_sign_convention",
        summary="FAIL forced failure: got 1, want 0\n1 check(s) failed: ['forced failure']\n",
        checks=17,
        line=OK_FAIL_LINE,
        forced=forced_value_failure,
    ),
    NumericalCheck(
        module=commodity_latency,
        script=None,
        replaced="check_latency_calibration",
        summary=LIST_SUMMARY,
        checks=7,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=contract_statistics,
        script=None,
        replaced="check_ism_calendar",
        summary=LIST_SUMMARY,
        checks=38,
    ),
    NumericalCheck(
        module=synthetic_short,
        script=ARTEFACTS / "synthetic-equity-cfd-trs" / "synthetic_short_checks.py",
        replaced="check_rebate",
        summary="FAIL forced failure: got 1.000000, want 0.000000\n1 check(s) failed\n",
        checks=37,
        line=OK_FAIL_LINE,
        forced=forced_value_failure,
    ),
    NumericalCheck(
        module=order_reconciliation,
        script=ARTEFACTS / "model-governance-controls" / "reconciliation-check.py",
        replaced="check_day_order",
        summary=LIST_SUMMARY,
        checks=22,
        passed="\nall checks passed (offline synthetic illustration)\n",
    ),
    NumericalCheck(
        module=black_litterman,
        script=None,
        replaced="check_posterior",
        summary=JOINED_SUMMARY,
        checks=4,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=equal_risk_contribution,
        script=None,
        replaced="check_unequal_correlations",
        summary=JOINED_SUMMARY,
        checks=10,
        imports=("numpy", "pydantic"),
        stand_ins={"check_constant_correlation": skipped, "check_unequal_correlations": skipped},
    ),
    NumericalCheck(
        module=erc_sharpe,
        script=None,
        replaced="check_unequal_correlations",
        summary=JOINED_SUMMARY,
        checks=7,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=expected_shortfall,
        script=None,
        replaced="check_historical_simulation",
        summary=JOINED_SUMMARY,
        checks=14,
        imports=("pydantic",),
    ),
    NumericalCheck(
        module=covariance_shrinkage,
        script=ARTEFACTS / "portfolio-construction" / "shrinkage-check.py",
        replaced="failed_conditions",
        summary="\nBAD forced failure\n",
        checks=0,
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        imports=NUMPY,
    ),
    NumericalCheck(
        module=risk_parity,
        script=None,
        replaced="check_two_asset_erc",
        summary=JOINED_SUMMARY,
        checks=3,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=garch_ewma,
        script=ARTEFACTS / "risk-tail-systemic" / "garch-ewma-check.py",
        replaced="check_ewma_against_garch",
        summary=LIST_SUMMARY,
        checks=3,
        imports=NUMPY,
        stand_ins={"check_ewma_against_garch": skipped},
    ),
    NumericalCheck(
        module=sharpe_zero,
        script=None,
        replaced="check_three_point",
        summary=LIST_SUMMARY,
        checks=4,
        imports=("numpy", "scipy.stats", "pydantic"),
        stand_ins={"check_student_t": skipped, "check_three_point": skipped},
    ),
    NumericalCheck(
        module=drawdown_resampling,
        script=None,
        replaced="failed_conditions",
        summary="\nBAD forced failure\n",
        checks=0,
        imports=("numpy", "pydantic"),
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        stand_ins={
            "EXPERIMENT": drawdown_resampling.EXPERIMENT.model_copy(
                update={"reference_paths": 50, "sample_paths": 2, "replications": 5}
            ),
            "failed_conditions": no_conditions,
        },
    ),
    NumericalCheck(
        module=linear_projection,
        script=ARTEFACTS / "equity-long-short-construction" / "projection-checks.py",
        replaced="check_joint_normality",
        summary=LIST_SUMMARY,
        checks=5,
        imports=NUMPY,
    ),
    NumericalCheck(
        module=var_backtest,
        script=None,
        replaced="check_clustering",
        summary=JOINED_SUMMARY,
        checks=3,
        imports=(*SCIPY_STATS, "pydantic"),
        stand_ins={"DAYS": 500, "check_clustering": skipped},
    ),
    NumericalCheck(
        module=multiple_testing,
        script=None,
        replaced="failed_conditions",
        summary="\nBAD forced failure\n",
        checks=0,
        imports=("numpy", "scipy.stats", "pydantic"),
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
    ),
    NumericalCheck(
        module=sharpe_statistics,
        script=None,
        replaced="check_deflated_sharpe",
        summary=LIST_SUMMARY,
        checks=23,
        imports=("numpy", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=forecast_scaling,
        script=ARTEFACTS / "equity-long-short-construction" / "forecast-checks.py",
        replaced="check_table_10_1",
        summary=LIST_SUMMARY,
        checks=16,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        module=purged_cv,
        script=ARTEFACTS / "statistical-learning-foundations" / "cv-checks.py",
        replaced="check_purged_kfold",
        summary=LIST_SUMMARY,
        checks=7,
        imports=NUMPY,
    ),
    NumericalCheck(
        module=concentrated_position,
        script=ARTEFACTS / "private-wealth" / "concentrated-position-check.py",
        replaced="check_exchange_fund",
        summary=JOINED_SUMMARY,
        checks=8,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        module=lob_model_derivations,
        script=None,
        replaced="check_roll",
        summary="FAIL forced failure: forced\n",
        checks=11,
        imports=("numpy", "scipy.optimize", "pydantic"),
        line=OK_FAIL_LINE,
        forced=forced_list_failure,
        passed="",
    ),
    NumericalCheck(
        module=sharpe_conditions,
        script=None,
        replaced="check_compounding",
        summary=LIST_SUMMARY,
        checks=8,
        imports=("numpy", "scipy.stats", "pydantic"),
        stand_ins={"check_infinite_kurtosis": skipped, "check_general_variance": skipped},
    ),
    NumericalCheck(
        module=dividend_tree_swaption,
        script=None,
        replaced="check_swaptions",
        summary=JOINED_SUMMARY,
        checks=6,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=lob_models,
        script=None,
        replaced="check_free_entry",
        summary=LIST_SUMMARY,
        checks=37,
        imports=("numpy", "scipy.integrate", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=margin_purchase,
        script=None,
        replaced="check_levered_return",
        summary=JOINED_SUMMARY,
        checks=7,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=cross_currency_basis,
        script=None,
        replaced="check_final_exchange",
        summary=JOINED_SUMMARY,
        checks=16,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=seasoned_variance_swap,
        script=None,
        replaced="check_simulation",
        summary=JOINED_SUMMARY,
        checks=8,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=covariance_volatility,
        script=ARTEFACTS / "high-dimensional-estimation" / "covariance-volatility-checks.py",
        replaced="check_har",
        summary=LIST_SUMMARY,
        checks=11,
        imports=NUMPY,
    ),
    NumericalCheck(
        module=etf_mechanics,
        script=ARTEFACTS / "etf-mechanics" / "etf-checks.py",
        replaced="check_cost_of_ownership",
        summary=LIST_SUMMARY,
        checks=13,
        imports=NUMPY,
        passed="\n13 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=trade_execution,
        script=None,
        replaced="check_evaluation",
        summary=COUNTED_SUMMARY,
        checks=14,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=macro_valuation,
        script=ARTEFACTS / "macro-asset-valuation" / "macro-valuation-checks.py",
        replaced="check_multiples_and_property",
        summary=COUNTED_SUMMARY,
        checks=16,
        imports=("numpy", "scipy"),
    ),
    NumericalCheck(
        module=commodity_returns,
        script=ARTEFACTS / "commodity-investment" / "commodity-return-checks.py",
        replaced="check_swaps",
        summary=LIST_SUMMARY,
        checks=15,
        imports=NUMPY,
        passed="\n15 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=correlation_independence,
        script=None,
        replaced="check_size",
        summary=JOINED_SUMMARY,
        checks=13,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        stand_ins={"check_size": skipped, "report_overlap": skipped},
    ),
    NumericalCheck(
        module=counterparty_capital,
        script=None,
        replaced="check_worked_example",
        summary=JOINED_SUMMARY,
        checks=13,
        imports=("numpy", "scipy", "scipy.integrate", "pydantic"),
    ),
    NumericalCheck(
        module=volatility_mismatch_hedging,
        script=None,
        replaced="check_gamma_condition",
        summary=JOINED_SUMMARY,
        checks=10,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        stand_ins={
            "EXPERIMENT": volatility_mismatch_hedging.EXPERIMENT.model_copy(
                update={"n_paths": 4, "n_fine": 20}
            ),
            "check_actual_hedge": skipped,
            "check_implied_hedge": skipped,
        },
    ),
    NumericalCheck(
        module=alternatives_allocation,
        script=None,
        replaced="check_liquidity",
        summary=JOINED_SUMMARY,
        checks=13,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=market_structure,
        script=None,
        replaced="check_concentration",
        summary=JOINED_SUMMARY,
        checks=13,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=hedge_funds,
        script=None,
        replaced="check_allocation",
        summary=JOINED_SUMMARY,
        checks=17,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=gips,
        script=None,
        replaced="check_composite_report",
        summary=JOINED_SUMMARY,
        checks=25,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=stochastic_calculus,
        script=None,
        replaced="check_feynman_kac",
        summary=JOINED_SUMMARY,
        checks=23,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=index_construction,
        script=ARTEFACTS / "market-index-construction" / "index-construction-checks.py",
        replaced="check_bond_index",
        summary=COUNTED_SUMMARY,
        checks=30,
        imports=NUMPY,
    ),
    NumericalCheck(
        module=monte_carlo_greeks,
        script=ARTEFACTS / "numerical-pricing" / "monte-carlo-greeks-check.py",
        replaced="check_fd_variance",
        summary="\nFAILED:forced failure\n",
        checks=17,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        module=currency_management,
        script=ARTEFACTS / "currency-management" / "currency-management-checks.py",
        replaced="check_active_strategies",
        summary=COUNTED_SUMMARY,
        checks=21,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        module=option_models,
        script=None,
        replaced="check_sabr",
        summary=JOINED_SUMMARY,
        checks=20,
        imports=("numpy", "pydantic"),
        stand_ins={"check_heston": skipped, "check_sabr": skipped},
    ),
    NumericalCheck(
        module=economic_growth,
        script=ARTEFACTS / "economic-growth" / "growth-checks.py",
        replaced="check_endogenous_growth",
        summary=COUNTED_SUMMARY,
        checks=22,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        module=derivative_overlays,
        script=None,
        replaced="check_endowment_case",
        summary=JOINED_SUMMARY,
        checks=25,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=active_management,
        script=None,
        replaced="check_risk_decomposition",
        summary=JOINED_SUMMARY,
        checks=30,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=credit_portfolios,
        script=None,
        replaced="check_structured",
        summary=LIST_SUMMARY,
        checks=25,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        passed="\n25 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=fx_mechanics,
        script=ARTEFACTS / "fx-mechanics-determination" / "fx-checks.py",
        replaced="check_flows",
        summary=COUNTED_SUMMARY,
        checks=27,
        imports=("numpy", "scipy", "scipy.stats"),
    ),
    NumericalCheck(
        module=manager_selection,
        script=None,
        replaced="check_shrinkage",
        summary=JOINED_SUMMARY,
        checks=26,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=transaction_cost_hedging,
        script=None,
        replaced="check_nonadditivity",
        summary=JOINED_SUMMARY,
        checks=16,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        stand_ins={
            "EXPERIMENT": transaction_cost_hedging.EXPERIMENT.model_copy(
                update={"n_paths": 8, "block": 8}
            ),
            "check_ledgers": skipped,
            "check_residuals": skipped,
            "report_pnl": skipped,
            "check_nonadditivity": skipped,
        },
    ),
    NumericalCheck(
        module=capital_market_expectations,
        script=ARTEFACTS / "capital-market-expectations" / "cme-checks.py",
        replaced="check_reweighting",
        summary=COUNTED_SUMMARY,
        checks=28,
        imports=("numpy", "scipy"),
    ),
    NumericalCheck(
        module=portfolio_moments,
        script=None,
        replaced="check_conditional_correlation",
        summary=JOINED_SUMMARY,
        checks=29,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=digital_assets,
        script=ARTEFACTS / "digital-assets" / "digital-asset-checks.py",
        replaced="check_custody",
        summary=LIST_SUMMARY,
        checks=21,
        imports=NUMPY,
        passed="\n21 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=numerical_pricing,
        script=ARTEFACTS / "numerical-pricing" / "numerical-pricing-checks.py",
        replaced="check_bermudan",
        summary=JOINED_SUMMARY,
        checks=18,
        imports=("numpy", "scipy", "scipy.stats", "scipy.linalg"),
        stand_ins={"check_american": unused_value, "check_bermudan": skipped},
    ),
    NumericalCheck(
        module=asset_pricing_factor_models,
        script=ARTEFACTS / "asset-pricing-factor-models" / "asset-pricing-checks.py",
        replaced="check_factor_models",
        summary=JOINED_SUMMARY,
        checks=39,
        imports=(*STATSMODELS, "statsmodels.api"),
    ),
    NumericalCheck(
        module=backtest_design,
        script=None,
        replaced="check_survivorship",
        summary=LIST_SUMMARY,
        checks=19,
        imports=("numpy", "pydantic"),
        passed="\n19 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=bond_valuation_risk,
        script=None,
        replaced="check_treasury_formulas",
        summary=COUNTED_SUMMARY,
        checks=94,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=credit_cds_securitisation,
        script=None,
        replaced="check_migration",
        summary="\n53 checks executed\nFAILED: ['forced failure']\n",
        checks=52,
        imports=("numpy", "scipy.optimize", "scipy.stats", "pydantic"),
        passed="\n52 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=counterparty_xva,
        script=None,
        replaced="check_collateral",
        summary=JOINED_SUMMARY,
        checks=32,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=default_correlation,
        script=None,
        replaced="check_base_correlation",
        summary=JOINED_SUMMARY,
        checks=18,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats", "pydantic"),
        stand_ins={"check_base_correlation": skipped, "check_tranches": skipped},
    ),
    NumericalCheck(
        module=short_rate_model,
        script=None,
        replaced="check_forward_market",
        summary=JOINED_SUMMARY,
        checks=22,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "pydantic"),
        args=("--root", str(ROOT)),
        stand_ins={"check_cir_exact": skipped, "check_hull_white_paths": skipped},
    ),
    NumericalCheck(
        module=term_structure,
        script=None,
        replaced="check_curves",
        summary=COUNTED_SUMMARY,
        checks=36,
        imports=("numpy", "pydantic"),
        args=("--root", str(ROOT)),
    ),
    NumericalCheck(
        module=statistics_probability,
        script=None,
        replaced="check_bayesian",
        summary=JOINED_SUMMARY,
        checks=64,
        imports=("numpy", "scipy.integrate", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=equity_portfolio_management,
        script=None,
        replaced="check_capacity_structure",
        summary=JOINED_SUMMARY,
        checks=26,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
        stand_ins={"check_capacity_structure": skipped},
    ),
    NumericalCheck(
        module=dealer_queue_information,
        script=None,
        replaced="check_power_and_inference",
        summary="\nBAD forced failure\n",
        checks=0,
        imports=("numpy", "scipy", "scipy.stats", "scipy.optimize", "pydantic"),
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        stand_ins={"check_power_and_inference": no_conditions},
    ),
    NumericalCheck(
        module=liquidity_market_design,
        script=None,
        replaced="check_capacity",
        summary="\nBAD forced failure\n",
        checks=0,
        imports=("numpy", "pydantic"),
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        stand_ins={"check_capacity": no_conditions, "check_search": no_conditions},
    ),
    NumericalCheck(
        module=market_estimators_rules,
        script=None,
        replaced="check_model_i",
        summary="\nFAILURES: ['forced failure']\n",
        checks=45,
        imports=("numpy", "pydantic"),
        passed="\nFAILURES: none\n",
        stand_ins={"check_model_i": skipped},
    ),
    NumericalCheck(
        module=exotic_options,
        script=None,
        replaced="check_barrier",
        summary=JOINED_SUMMARY,
        checks=21,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        stand_ins={"check_barrier": skipped},
    ),
    NumericalCheck(
        module=lookback_options,
        script=None,
        replaced="check_monitoring",
        summary=JOINED_SUMMARY,
        checks=19,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        stand_ins={"check_monitoring": skipped},
    ),
    NumericalCheck(
        module=extreme_value,
        script=None,
        replaced="check_rmfi",
        summary=JOINED_SUMMARY,
        checks=8,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats", "pydantic"),
        stand_ins={"report_diagnostics": skipped},
    ),
    NumericalCheck(
        module=financial_ml_methods,
        script=ARTEFACTS / "financial-ml-methods" / "ml-methods-checks.py",
        replaced="check_classifier",
        summary=LIST_SUMMARY,
        checks=23,
        imports=("numpy", "scipy", "scipy.cluster.hierarchy", "scipy.optimize", "scipy.stats"),
        passed="\n23 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=intercorporate_fx_institutions,
        script=ARTEFACTS
        / "financial-statement-analysis"
        / "intercorporate-fx-institutions-checks.py",
        replaced="check_classification",
        summary=LIST_SUMMARY,
        checks=54,
        imports=NUMPY,
        passed="\n54 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=statement_analysis,
        script=None,
        replaced="check_leases",
        summary=JOINED_SUMMARY,
        checks=138,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
        passed="\n138 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=fixed_income_portfolio,
        script=None,
        replaced="check_indexes",
        summary=COUNTED_SUMMARY,
        checks=40,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=forward_swap_valuation,
        script=None,
        replaced="check_option_payoffs",
        summary=JOINED_SUMMARY,
        checks=69,
        imports=("numpy", "pydantic"),
    ),
    NumericalCheck(
        module=inference_simulation,
        script=None,
        replaced="check_discretisation",
        summary=JOINED_SUMMARY,
        checks=52,
        imports=("numpy", "scipy", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=institutional_portfolios,
        script=ARTEFACTS / "institutional-portfolios" / "institutional-checks.py",
        replaced="check_endowment",
        summary=LIST_SUMMARY,
        checks=28,
        imports=NUMPY,
        passed="\n28 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=investment_planning,
        script=None,
        replaced="check_behaviour",
        summary=JOINED_SUMMARY,
        checks=41,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=macro_policy_trade,
        script=ARTEFACTS / "macro-policy-trade" / "macro-policy-trade-checks.py",
        replaced="check_trade",
        summary=COUNTED_SUMMARY,
        checks=25,
        imports=("numpy", "scipy", "scipy.optimize"),
    ),
    NumericalCheck(
        module=market_risk_measurement,
        script=None,
        replaced="check_sensitivity_scenarios",
        summary=JOINED_SUMMARY,
        checks=27,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=order_flow,
        script=None,
        replaced="check_trade_signing",
        summary="\nBAD forced failure\n",
        checks=0,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "pydantic"),
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        passed="",
        stand_ins={"check_latent_spread": no_conditions},
    ),
    NumericalCheck(
        module=order_routing_fragmentation,
        script=ARTEFACTS
        / "market-structure-execution-quality"
        / "order-routing-fragmentation-checks.py",
        replaced="check_learner",
        summary="\nBAD forced failure\n",
        checks=0,
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        imports=SCIPY_STATS,
        passed="",
        stand_ins={"check_learner": no_conditions},
    ),
    NumericalCheck(
        module=macro_pricing_risk,
        script=ARTEFACTS / "multi-asset-systematic-macro" / "macro-pricing-risk-checks.py",
        replaced="check_duration",
        summary="\nBAD forced failure\n",
        checks=0,
        line=BAD_ONLY_LINE,
        forced=forced_condition_failure,
        imports=SCIPY_STATS,
    ),
    NumericalCheck(
        module=option_strategies,
        script=None,
        replaced="check_selection",
        summary=JOINED_SUMMARY,
        checks=31,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=option_valuation,
        script=None,
        replaced="check_greeks",
        summary=JOINED_SUMMARY,
        checks=44,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=performance_evaluation,
        script=None,
        replaced="check_skill",
        summary=JOINED_SUMMARY,
        checks=41,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "pydantic"),
    ),
    NumericalCheck(
        module=kelly_growth,
        script=None,
        replaced="check_levered_ruin",
        summary=JOINED_SUMMARY,
        checks=23,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.stats", "pydantic"),
        stand_ins={"check_daily_rebalancing": skipped},
    ),
    NumericalCheck(
        module=mean_cvar,
        script=None,
        replaced="check_mean_variance",
        summary=JOINED_SUMMARY,
        checks=8,
        imports=(
            "numpy",
            "scipy",
            "scipy.optimize",
            "scipy.stats",
            "scipy.sparse",
            "scipy.special",
            "pydantic",
        ),
        stand_ins={
            "check_mean_variance": skipped,
            "report_skewed_case": skipped,
            "check_lp": skipped,
        },
    ),
    NumericalCheck(
        module=private_capital,
        script=ARTEFACTS / "private-capital" / "private-capital-checks.py",
        replaced="check_valuation",
        summary=LIST_SUMMARY,
        checks=38,
        imports=("numpy", "scipy", "scipy.optimize"),
        passed="\n38 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=private_wealth,
        script=ARTEFACTS / "private-wealth" / "private-wealth-checks.py",
        replaced="check_residence",
        summary=LIST_SUMMARY,
        checks=59,
        imports=("numpy", "scipy", "scipy.optimize"),
        passed="\n59 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=rate_tree_embedded_options,
        script=None,
        replaced="check_paths",
        summary=COUNTED_SUMMARY,
        checks=46,
        imports=("numpy", "scipy", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=real_assets,
        script=ARTEFACTS / "real-assets" / "real-asset-checks.py",
        replaced="check_reit",
        summary=LIST_SUMMARY,
        checks=37,
        imports=("numpy", "scipy", "scipy.optimize"),
        passed="\n37 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=strategic_asset_allocation,
        script=None,
        replaced="check_goals_heuristics",
        summary=JOINED_SUMMARY,
        checks=40,
        imports=("numpy", "scipy", "scipy.stats", "scipy.optimize", "pydantic"),
    ),
    NumericalCheck(
        module=fx_panel_inference,
        script=ARTEFACTS / "fx-determination-forecasting" / "fx-panel-inference-check.py",
        replaced="check_empty_months",
        summary="FAIL  forced failure: forced\n",
        checks=11,
        line=PASS_FAIL_LINE,
        forced=forced_list_failure,
        imports=NUMPY,
        passed="",
        stand_ins={"check_independent_currencies": skipped},
    ),
    NumericalCheck(
        module=linear_regression,
        script=None,
        replaced="check_functional_forms",
        summary=JOINED_SUMMARY,
        checks=44,
        imports=(
            *STATSMODELS,
            "statsmodels.api",
            "statsmodels.formula.api",
            "scipy.integrate",
            "scipy.stats",
            "statsmodels.regression.linear_model",
            "statsmodels.stats.anova",
            "pydantic",
        ),
    ),
    NumericalCheck(
        module=scenario_simulation,
        script=None,
        replaced="check_sensitivities",
        summary=LIST_SUMMARY,
        checks=10,
        passed="\n10 checks executed\nall checks passed\n",
        imports=("numpy", "pydantic"),
        args=("--root", str(ROOT)),
    ),
    NumericalCheck(
        module=multiple_regression,
        script=None,
        replaced="check_extensions",
        summary=LIST_SUMMARY,
        checks=24,
        passed="\n24 checks executed\nall checks passed\n",
        imports=(
            *STATSMODELS,
            "statsmodels.api",
            "statsmodels.regression.linear_model",
            "statsmodels.stats.diagnostic",
            "statsmodels.stats.outliers_influence",
            "statsmodels.stats.stattools",
            "pydantic",
        ),
        args=("--root", str(ROOT)),
    ),
    NumericalCheck(
        module=time_series,
        script=None,
        replaced="check_model_selection",
        summary=LIST_SUMMARY,
        checks=36,
        passed="\n36 checks executed\nall checks passed\n",
        imports=(
            *STATSMODELS,
            "statsmodels.api",
            "scipy.stats",
            "statsmodels.regression.linear_model",
            "statsmodels.stats.diagnostic",
            "statsmodels.stats.stattools",
            "statsmodels.tools.sm_exceptions",
            "statsmodels.tsa.adfvalues",
            "statsmodels.tsa.stattools",
            "pydantic",
        ),
        args=("--root", str(ROOT)),
    ),
    # It reads its data file and a compendium figure below the repository root.
    NumericalCheck(
        module=portfolio_choice,
        script=None,
        replaced="check_risk_aversion",
        summary=JOINED_SUMMARY,
        checks=50,
        imports=("numpy", "scipy", "scipy.integrate", "scipy.optimize", "scipy.stats", "pydantic"),
        args=("--root", str(ROOT)),
    ),
    NumericalCheck(
        module=corporate_finance,
        script=None,
        replaced="check_payout_policy",
        summary=JOINED_SUMMARY,
        checks=75,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
        passed="\n75 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=equity_valuation,
        script=None,
        replaced="check_momentum",
        summary=JOINED_SUMMARY,
        checks=72,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
        passed="\n72 checks executed\nall checks passed\n",
    ),
    NumericalCheck(
        module=equity_fcf_ri_private,
        script=None,
        replaced="check_normalised_earnings",
        summary=JOINED_SUMMARY,
        checks=57,
        imports=("numpy", "scipy", "scipy.optimize", "scipy.stats", "pydantic"),
        passed="\n57 checks executed\nall checks passed\n",
    ),
]
DEMONSTRATIONS = [
    Demonstration(
        module=cartea_jaimungal,
        script=ARTEFACTS / "reinforcement-learning-trading" / "cartea_jaimungal_checks.py",
        lines=22,
    ),
    Demonstration(
        module=negative_hedge_ratio,
        script=ARTEFACTS / "volatility-options" / "negative-hedge-ratio-check.py",
        lines=6,
        imports=NUMPY,
    ),
    Demonstration(
        module=yield_shift,
        script=None,
        lines=9,
        imports=("numpy", "scipy.optimize", "pydantic"),
    ),
    Demonstration(
        module=financial_labels,
        script=ARTEFACTS
        / "statistical-learning-foundations"
        / "financial-labels-capital-checks.py",
        lines=39,
        imports=NUMPY,
    ),
    Demonstration(
        module=afml,
        script=ARTEFACTS / "statistical-learning-foundations" / "afml-checks.py",
        lines=84,
        imports=(*STATSMODELS, "statsmodels.tsa.stattools"),
    ),
]
EXAMPLES: list[NumericalCheck | Demonstration] = [*CHECKS, *DEMONSTRATIONS]
# Package modules that are not examples, with the heavy dependencies each imports (of `HEAVY`).
SUPPORT: dict[str, tuple[str, ...]] = {
    "trading_notes": (),
    "trading_notes.numerical": (),
    "trading_notes.numerical.active_management": (),
    "trading_notes.numerical.active_management.fundamental_law": ("pydantic",),
    "trading_notes.numerical.alternatives_allocation": (),
    "trading_notes.numerical.alternatives_allocation.commitment_pacing": ("numpy", "pydantic"),
    "trading_notes.numerical.arbitrage_free_valuation": (),
    "trading_notes.numerical.arbitrage_free_valuation.short_rate_models": ("numpy", "pydantic"),
    "trading_notes.numerical.backtest_evaluation": (),
    "trading_notes.numerical.backtest_evaluation.backtest_book": ("numpy", "pydantic"),
    "trading_notes.numerical.backtest_evaluation.drawdown_bootstrap": ("numpy", "pydantic"),
    "trading_notes.numerical.backtest_evaluation.familywise_tests": ("numpy", "pydantic"),
    "trading_notes.numerical.backtest_evaluation.sharpe_inference": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.bond_pricing_yields": (),
    "trading_notes.numerical.bond_pricing_yields.fixed_rate_bonds": (
        "numpy",
        "scipy.optimize",
        "pydantic",
    ),
    "trading_notes.numerical.bond_pricing_yields.sofr_notes": ("pydantic",),
    "trading_notes.numerical.capital_structure_cost_of_capital": (),
    "trading_notes.numerical.capital_structure_cost_of_capital.cost_of_capital": ("pydantic",),
    "trading_notes.numerical.capital_structure_cost_of_capital.country_risk": ("pydantic",),
    "trading_notes.numerical.cash_flow_analysis": (),
    "trading_notes.numerical.cash_flow_analysis.statement_linkage": ("pydantic",),
    "trading_notes.numerical.company_case": (),
    "trading_notes.numerical.company_case.harbour": ("numpy", "scipy.stats", "pydantic"),
    "trading_notes.numerical.corporate_finance": (),
    "trading_notes.numerical.counterparty_xva": (),
    "trading_notes.numerical.counterparty_xva.regulatory_capital": ("pydantic",),
    "trading_notes.numerical.counterparty_xva.swap_exposure": ("numpy", "pydantic"),
    "trading_notes.numerical.counterparty_xva.tree_cva": ("numpy", "scipy.optimize", "pydantic"),
    "trading_notes.numerical.credit_portfolio_management": (),
    "trading_notes.numerical.credit_portfolio_management.structured_claims": ("pydantic",),
    "trading_notes.numerical.credit_risk_analysis": (),
    "trading_notes.numerical.credit_risk_analysis.credit_instruments": ("numpy", "pydantic"),
    "trading_notes.numerical.default_correlation": (),
    "trading_notes.numerical.default_correlation.factor_model": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.default_correlation.tranche_pricing": (
        "numpy",
        "scipy.integrate",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.derivative_overlays": (),
    "trading_notes.numerical.derivative_overlays.variance_swap": ("numpy", "pydantic"),
    "trading_notes.numerical.descriptive_statistics": (),
    "trading_notes.numerical.descriptive_statistics.return_statistics": ("pydantic",),
    "trading_notes.numerical.embedded_option_bonds": (),
    "trading_notes.numerical.embedded_option_bonds.binomial_tree": (
        "numpy",
        "scipy.optimize",
        "pydantic",
    ),
    "trading_notes.numerical.equity_portfolio_management": (),
    "trading_notes.numerical.equity_portfolio_management.equity_universe": ("numpy", "pydantic"),
    "trading_notes.numerical.exotic_options": (),
    "trading_notes.numerical.exotic_options.exotic_pricing": ("numpy", "scipy.stats", "pydantic"),
    "trading_notes.numerical.exotic_options.lookback": ("numpy", "scipy.stats", "pydantic"),
    "trading_notes.numerical.extreme_values": (),
    "trading_notes.numerical.extreme_values.tail_estimation": (
        "numpy",
        "scipy.optimize",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.firms_market_structure": (),
    "trading_notes.numerical.firms_market_structure.firm_costs": ("numpy", "pydantic"),
    "trading_notes.numerical.fixed_income_portfolio_management": (),
    "trading_notes.numerical.fixed_income_portfolio_management.curve_exposures": (
        "numpy",
        "pydantic",
    ),
    "trading_notes.numerical.forward_commitment_valuation": (),
    "trading_notes.numerical.forward_commitment_valuation.cross_currency": ("pydantic",),
    "trading_notes.numerical.forward_commitment_valuation.swap_valuation": ("numpy", "pydantic"),
    "trading_notes.numerical.futures_execution": (),
    "trading_notes.numerical.hedge_fund_strategies": (),
    "trading_notes.numerical.hedge_fund_strategies.return_smoothing": ("numpy", "pydantic"),
    "trading_notes.numerical.high_frequency_trading": (),
    "trading_notes.numerical.high_frequency_trading.speed_race": (
        "numpy",
        "scipy.optimize",
        "pydantic",
    ),
    "trading_notes.numerical.interest_rates": (),
    "trading_notes.numerical.interest_rates.continuous_cash_flows": (
        "numpy",
        "scipy.optimize",
        "pydantic",
    ),
    "trading_notes.numerical.investment_process_planning": (),
    "trading_notes.numerical.investment_process_planning.retirement_plan": (
        "numpy",
        "scipy.optimize",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.manager_selection": (),
    "trading_notes.numerical.manager_selection.manager_evaluation": (
        "numpy",
        "scipy.optimize",
        "pydantic",
    ),
    "trading_notes.numerical.market_making_models": (),
    "trading_notes.numerical.market_making_models.inventory_models": ("pydantic",),
    "trading_notes.numerical.market_making_models.microstructure_models": ("pydantic",),
    "trading_notes.numerical.market_organisation": (),
    "trading_notes.numerical.market_organisation.liquidity_models": ("numpy", "pydantic"),
    "trading_notes.numerical.market_risk_measurement": (),
    "trading_notes.numerical.market_risk_measurement.market_risk": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.money_markets": (),
    "trading_notes.numerical.money_markets.money_market_instruments": ("pydantic",),
    "trading_notes.numerical.multiple_regression": (),
    "trading_notes.numerical.multiple_regression.least_squares": ("numpy", "pydantic"),
    "trading_notes.numerical.newey_west": ("numpy",),
    "trading_notes.numerical.option_hedging": (),
    "trading_notes.numerical.option_hedging.leland_hedging": (
        "numpy",
        "pydantic",
        "scipy",
        "scipy.stats",
    ),
    "trading_notes.numerical.option_hedging.volatility_mismatch": (
        "numpy",
        "scipy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.option_pricing": (),
    "trading_notes.numerical.option_pricing.black_scholes": ("numpy", "scipy.stats", "pydantic"),
    "trading_notes.numerical.option_pricing.stochastic_models": ("numpy", "pydantic"),
    "trading_notes.numerical.option_pricing.svi": ("pydantic",),
    "trading_notes.numerical.option_strategies": (),
    "trading_notes.numerical.option_valuation": (),
    "trading_notes.numerical.option_valuation.delta_hedging": ("numpy", "scipy.stats", "pydantic"),
    "trading_notes.numerical.option_valuation.dividend_tree": ("numpy", "pydantic"),
    "trading_notes.numerical.order_books": (),
    "trading_notes.numerical.order_books.latency_calibration": ("pydantic",),
    "trading_notes.numerical.order_books.matching_allocation": ("pydantic",),
    "trading_notes.numerical.order_flow_statistics": (),
    "trading_notes.numerical.order_flow_statistics.covariance_estimators": ("numpy", "pydantic"),
    "trading_notes.numerical.order_flow_statistics.point_processes": (
        "numpy",
        "scipy.integrate",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.order_flow_statistics.trade_classification": ("pydantic",),
    "trading_notes.numerical.performance_attribution_appraisal": (),
    "trading_notes.numerical.performance_attribution_appraisal.performance_measures": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.performance_standards": (),
    "trading_notes.numerical.performance_standards.composite": ("pydantic",),
    "trading_notes.numerical.portfolio_choice": (),
    "trading_notes.numerical.portfolio_choice.frontier": ("numpy", "pydantic"),
    "trading_notes.numerical.portfolio_choice.history": ("numpy", "pydantic"),
    "trading_notes.numerical.portfolio_construction_models": (),
    "trading_notes.numerical.portfolio_construction_models.black_litterman": ("numpy", "pydantic"),
    "trading_notes.numerical.portfolio_construction_models.kelly_growth": ("numpy", "pydantic"),
    "trading_notes.numerical.portfolio_construction_models.mean_cvar": (
        "numpy",
        "scipy",
        "scipy.optimize",
        "scipy.sparse",
        "scipy.special",
        "pydantic",
    ),
    "trading_notes.numerical.portfolio_construction_models.risk_contributions": (
        "numpy",
        "pydantic",
    ),
    "trading_notes.numerical.portfolio_moments": (),
    "trading_notes.numerical.portfolio_moments.scenario_moments": ("numpy", "pydantic"),
    "trading_notes.numerical.rate_swaps_clearing": (),
    "trading_notes.numerical.rate_swaps_clearing.fra_valuation": ("pydantic",),
    "trading_notes.numerical.records": ("pydantic",),
    "trading_notes.numerical.regression": (),
    "trading_notes.numerical.regression.simple_regression": ("numpy", "scipy.stats", "pydantic"),
    "trading_notes.numerical.report": (),
    "trading_notes.numerical.repository": (),
    "trading_notes.numerical.scenario_simulation": (),
    "trading_notes.numerical.scenario_simulation.return_simulation": ("numpy", "pydantic"),
    "trading_notes.numerical.securities_lending": (),
    "trading_notes.numerical.securities_lending.margin_accounts": ("pydantic",),
    "trading_notes.numerical.statistical_inference": (),
    "trading_notes.numerical.statistical_inference.correlation_tests": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.statistical_inference.sample_inference": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.stochastic_calculus": (),
    "trading_notes.numerical.stochastic_calculus.geometric_brownian_motion": (
        "numpy",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.strategic_asset_allocation": (),
    "trading_notes.numerical.strategic_asset_allocation.allocation": (
        "numpy",
        "scipy.optimize",
        "scipy.stats",
        "pydantic",
    ),
    "trading_notes.numerical.systematic_equities": (),
    "trading_notes.numerical.term_structure_returns": (),
    "trading_notes.numerical.term_structure_returns.curve_bootstrap": ("numpy", "pydantic"),
    "trading_notes.numerical.time_series_models": (),
    "trading_notes.numerical.time_series_models.forecasting_models": (
        "numpy",
        "pandas",
        "scipy",
        "statsmodels",
        "statsmodels.api",
        "scipy.optimize",
        "pydantic",
    ),
    "trading_notes.numerical.tolerance": (),
    "trading_notes.numerical.trade_strategy_governance": (),
    "trading_notes.numerical.trade_strategy_governance.almgren_chriss": ("numpy", "pydantic"),
    "trading_notes.numerical.us_calendar": (),
    "trading_notes.numerical.var_es_estimation": (),
    "trading_notes.numerical.var_es_estimation.expected_shortfall": ("pydantic",),
    "trading_notes.numerical.var_es_estimation.var_backtest": ("numpy", "pydantic"),
}


def captured(run: Callable[[], int]) -> tuple[int, str]:
    """Return a run's exit status and everything it printed."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        status = run()
    return status, out.getvalue()


def run_concurrently(
    commands: Sequence[tuple[Sequence[str], Path]],
) -> list[subprocess.CompletedProcess[str]]:
    """Run independent commands, each from its working directory; results in command order.

    The processes share nothing, so they run together, at most `MAX_PROCESSES` at once.
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

    def test_summarise_with_no_failures_returns_0(self) -> None:
        """With every check passed, `summarise` prints `all checks passed` and returns 0."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            report.ok("x", True)
        self.assertEqual(captured(report.summarise), (0, "all checks passed\n"))

    def test_summarise_with_failures_returns_1(self) -> None:
        """With failures, `summarise` lists them in order, returns 1 and keeps the record."""
        report = CheckReport()
        with contextlib.redirect_stdout(io.StringIO()):
            report.ok("x", False)
            report.ok("y", True)
            report.ok("z", False)
        status, out = captured(report.summarise)
        self.assertEqual((status, out), (1, "FAILED: x, z\n"))
        self.assertEqual(report.failures, ["x", "z"])
        self.assertEqual(captured(report.summarise), (1, "FAILED: x, z\n"))

    def test_summarise_without_checks_returns_0(self) -> None:
        """A run with no checks has no failures, so it passes."""
        self.assertEqual(captured(CheckReport().summarise), (0, "all checks passed\n"))


class FailureOnlyReporting(unittest.TestCase):
    """The helpers of checks that print only their failures, and the shared section heading."""

    def test_require_records_only_failures_and_prints_nothing(self) -> None:
        """A false condition appends its name in order; a true one leaves the list alone."""
        failed: list[str] = ["earlier"]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            require(failed, "holds", True)
            require(failed, "fails", False)
            require(failed, "fails again", False)
        self.assertEqual((out.getvalue(), failed), ("", ["earlier", "fails", "fails again"]))

    def test_section_prints_a_heading_after_a_blank_line(self) -> None:
        """A heading is `== <title>` preceded by an empty line."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            section("1. Part")
        self.assertEqual(out.getvalue(), "\n== 1. Part\n")


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


# Runs one example as the main program, from wherever the process starts; see single_run.
HARNESS = (
    f"import sys\nsys.path.append({str(ROOT / 'src')!r})\n"
    "from tests.numerical.single_run import main\nsys.exit(main(sys.argv[1:]))\n"
)


def full_run_command(example: NumericalCheck | Demonstration) -> list[str]:
    """Return the isolated command that runs the example's entrypoint once, as a user would."""
    args = example.args if isinstance(example, NumericalCheck) else ()
    return [
        sys.executable,
        "-I",
        "-W",
        "error",
        "-c",
        HARNESS,
        example.module.__name__,
        str(example.script or ""),
        *args,
    ]


def failed_lines(check: NumericalCheck, out: str) -> list[str]:
    """Return the statuses of the failed check lines in a run's output."""
    return [s for s in check.line.findall(out) if s in ("BAD", "FAIL")]


def verify_clean_success(check: NumericalCheck, status: int, out: str) -> None:
    """Assert that a run passed: exit status 0, no failed check line and the success summary."""
    assert status == 0, f"status {status}: {out[-300:]}"
    assert failed_lines(check, out) == [], out[-300:]
    assert out.endswith(check.passed), out[-300:]


def verify_forced_failure(check: NumericalCheck, status: int, out: str) -> None:
    """Assert that the one forced failure was reported, summarised and made the status 1."""
    assert status == 1, f"status {status}: {out[-300:]}"
    assert out.endswith(check.summary), out[-300:]
    assert len(failed_lines(check, out)) == 1, out[-300:]


def verify_runs_in_process(check: NumericalCheck) -> None:
    """Run `main()` three times in one process: clean, with one forced failure, clean again.

    The two clean runs must pass and print the same thing, so a failure, or any state that
    one run leaves behind, cannot reach the next; the forced failure must reach the summary and
    the status. The shared generators start primed and NumPy's settings must be left as found.
    Expensive parts are replaced by the check's `stand_ins`.
    """
    with restored_global_state():
        prime_global_random(PRIMING_SEED)
        before = GlobalState.now()
        first = run_main(check.module, check.args, check.stand_ins)
        failed = run_main(
            check.module, check.args, check.stand_ins, failure=(check.replaced, check.forced)
        )
        again = run_main(check.module, check.args, check.stand_ins)
        assert GlobalState.now() == before, "shared random or NumPy state changed"
    verify_clean_success(check, *first)
    verify_forced_failure(check, *failed)
    assert again == first, "a second clean run printed something else"


def main_guard(module: ModuleType) -> CodeType:
    """Return the compiled `if __name__ == "__main__":` block of a module."""
    path = Path(module.__file__ or "")
    guards: list[ast.stmt] = [
        node
        for node in ast.parse(path.read_text()).body
        if isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
        and [type(op) for op in node.test.ops] == [ast.Eq]
        and isinstance(node.test.comparators[0], ast.Constant)
        and node.test.comparators[0].value == "__main__"
    ]
    assert len(guards) == 1, f"{module.__name__} has {len(guards)} main guards"
    return compile(ast.Module(body=guards, type_ignores=[]), str(path), "exec")


def answering(status: int) -> Callable[[Sequence[str] | None], int]:
    """Return a stand-in for `main` that returns status."""

    def main(argv: Sequence[str] | None = None) -> int:
        return status

    return main


class NumericalChecks(unittest.TestCase):
    """The numerical checks and demonstrations: one run each, their imports and their coverage."""

    def test_each_example_runs_once(self) -> None:
        """One isolated, real run of each example's entrypoint checks a clean pass.

        Each example runs once as the main program, `python -I -W error`, from an unrelated
        folder: the module through runpy as `python -m` runs it, or its forwarding script while
        it has one. A check must exit 0 with every check line ok, its number of check lines and
        its success summary; a demonstration exits 0 with its number of lines. The shared
        generators start seeded and holding cached Gaussians, unlike a fresh process, and must
        be left exactly as found, with NumPy's print options and error handling; nothing may be
        written to the working folder.
        """
        with tempfile.TemporaryDirectory() as elsewhere:
            results = run_concurrently([(full_run_command(e), Path(elsewhere)) for e in EXAMPLES])
            for example, done in zip(EXAMPLES, results, strict=True):
                with self.subTest(example.module.__name__):
                    self.assertEqual(done.stderr, "")
                    if isinstance(example, Demonstration):
                        self.assertEqual(done.returncode, 0)
                        self.assertEqual(done.stdout.count("\n"), example.lines)
                        continue
                    verify_clean_success(example, done.returncode, done.stdout)
                    self.assertEqual(len(example.line.findall(done.stdout)), example.checks)
            self.assertEqual(list(Path(elsewhere).iterdir()), [])

    def test_entrypoints_exit_with_the_status_of_main(self) -> None:
        """Each entrypoint passes main()'s status to sys.exit, so a failure reaches the shell.

        The module's own `if __name__ == "__main__":` block, and the forwarding script while
        there is one, are executed with `main` answered by a stand-in returning 0, then 1.
        """
        for example in EXAMPLES:
            guard = main_guard(example.module)
            for status in (0, 1):
                with self.subTest(example.module.__name__, status=status):
                    namespace = vars(example.module) | {
                        "__name__": "__main__",
                        "main": answering(status),
                    }
                    with self.assertRaises(SystemExit) as stop:
                        exec(guard, namespace)
                    self.assertEqual(stop.exception.code, status)
                    if example.script is None:
                        continue
                    with (
                        mock.patch.object(example.module, "main", answering(status)),
                        self.assertRaises(SystemExit) as stop,
                    ):
                        runpy.run_path(str(example.script), run_name="__main__")
                    self.assertEqual(stop.exception.code, status)

    def test_every_package_module_is_covered(self) -> None:
        """Each module and package below trading_notes.numerical is listed exactly once."""
        found = {
            module.name
            for module in pkgutil.walk_packages(
                trading_notes.numerical.__path__, "trading_notes.numerical."
            )
        }
        checks = {check.module.__name__ for check in CHECKS}
        demonstrations = {demonstration.module.__name__ for demonstration in DEMONSTRATIONS}
        self.assertEqual(checks & demonstrations, set())
        self.assertEqual(len(checks) + len(demonstrations), len(EXAMPLES))
        listed = checks | demonstrations | set(SUPPORT)
        self.assertEqual(found, listed - {"trading_notes", "trading_notes.numerical"})

    def test_every_forwarding_script_is_listed(self) -> None:
        """Each artefact script that forwards to the package is an example's `script`.

        `make examples` skips these scripts because the single run here covers them.
        """
        forwarding = {
            script
            for script in ARTEFACTS.glob("*/*check*.py")
            if re.search(r"^from trading_notes\.numerical", script.read_text(), re.M)
        }
        self.assertEqual(forwarding, {e.script for e in EXAMPLES if e.script is not None})

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
        with (
            tempfile.TemporaryDirectory() as elsewhere,
            ThreadPoolExecutor(max_workers=MAX_PROCESSES) as pool,
        ):
            cwd = Path(elsewhere)
            needed = sorted(set(imports.values()) - {()})
            reads = pool.map(lambda dependencies: dependency_reads(dependencies, cwd), needed)
            allowed = {(): frozenset[str]()} | dict(zip(needed, reads, strict=True))
            # The standard-library and NumPy modules stay held to opening nothing at all, and
            # no dependency's own reads reach the notes, where the research data is kept.
            self.assertEqual(allowed[NUMPY], frozenset())
            notes = ARTEFACTS.parent
            self.assertFalse(
                [p for r in allowed.values() for p in r if Path(p).is_relative_to(notes)]
            )
            names = list(imports)
            alone = list(pool.map(lambda name: import_effects([name], watched, cwd), names))
            with_dependencies = [name for name in names if imports[name]]
            preloaded = dict(
                zip(
                    with_dependencies,
                    pool.map(
                        lambda name: import_effects([name], watched, cwd, preload=imports[name]),
                        with_dependencies,
                    ),
                    strict=True,
                )
            )
            for name, effects in zip(names, alone, strict=True):
                dependencies = imports[name]
                with self.subTest(name):
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
                        again = preloaded[name]
                        self.assertEqual(
                            (again.returncode, again.stderr, again.random_unchanged),
                            (0, "", True),
                        )
            self.assertEqual(list(cwd.iterdir()), [])

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


def synthetic_example(
    status: Callable[[CheckReport], int], shared: CheckReport | None = None
) -> NumericalCheck:
    """Return a one-check example whose main returns status(report) after the check.

    Args:
        status: Turns the run's report into the exit status.
        shared: A report kept across runs, instead of a new one for each run.
    """
    module = ModuleType("synthetic_example")

    def check_value(report: CheckReport) -> None:
        report.ok("value", True)

    def main() -> int:
        report = shared or CheckReport()
        vars(module)["check_value"](report)
        print()
        return status(report)

    vars(module).update(check_value=check_value, main=main)
    return NumericalCheck(
        module=module, script=None, replaced="check_value", summary=JOINED_SUMMARY, checks=1
    )


class VerifiersRejectBrokenExamples(unittest.TestCase):
    """The verifiers used above fail for an example that reports wrongly."""

    def test_correct_example_passes(self) -> None:
        """An example that returns its report's summary passes the in-process verification."""
        verify_runs_in_process(synthetic_example(CheckReport.summarise))

    def test_always_nonzero_main_is_rejected(self) -> None:
        """A main that prints the right summary but always returns 1 fails clean success."""
        always_failing = synthetic_example(lambda report: report.summarise() or 1)
        with self.assertRaises(AssertionError):
            verify_runs_in_process(always_failing)
        with self.assertRaises(AssertionError):
            verify_clean_success(always_failing, 1, "  ok  value\n\nall checks passed\n")

    def test_always_zero_main_is_rejected(self) -> None:
        """A main that ignores its failures fails the forced-failure verification."""
        with self.assertRaises(AssertionError):
            verify_runs_in_process(synthetic_example(lambda report: report.summarise() and 0))

    def test_report_kept_across_runs_is_rejected(self) -> None:
        """A report shared between runs carries the forced failure into the next clean run."""
        with self.assertRaises(AssertionError):
            verify_runs_in_process(synthetic_example(CheckReport.summarise, CheckReport()))


@pytest.mark.parametrize("check", CHECKS, ids=lambda check: check.module.__name__.split(".")[-1])
def test_failure_reaches_status_and_runs_repeat(check: NumericalCheck) -> None:
    """In process: a clean run, one with a forced failure, then an identical clean run."""
    verify_runs_in_process(check)


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
        exact = CountryRisk(spread=third, sd_equity=third, sd_bond=third)
        self.assertIs(type(exact.relative_sd_premium(third, third)), Fraction)
        self.assertIs(type(exact.melded_premium()), Fraction)
        self.assertIs(type(exact.default_spread_premium()), Fraction)
        self.assertEqual(exact.melded_premium(), third)
        inexact = CountryRisk(spread=2.25, sd_equity=24.0, sd_bond=17.0)
        self.assertIs(type(inexact.melded_premium()), float)
        self.assertIs(type(inexact.relative_sd_premium(4.2, 15.0)), float)


class CashFlowLinkage(unittest.TestCase):
    """The cash-flow example derives closing cash from the balances, in integers."""

    def test_closing_cash_follows_the_balances(self) -> None:
        """A receivable one higher lowers derived cash by one; the balance sheet still balances."""
        linkage = cash_flow_linkage.LINKAGE
        raised = linkage.model_copy(
            update={"closing": linkage.closing.model_copy(update={"receivables": 151})}
        )
        base, moved = linkage.cash_flows, raised.cash_flows
        self.assertEqual((base.close_cash, moved.close_cash), (97, 96))
        self.assertEqual((base.cfo - moved.cfo, base.cfi, base.cff), (1, moved.cfi, moved.cff))
        o, c, i = raised.opening, raised.closing, raised.income
        re_close = (
            (o.assets(raised.opening_cash) - o.liabilities() - o.share_capital)
            + i.profit
            - raised.dividends_paid
        )
        self.assertEqual(c.assets(moved.close_cash), c.liabilities() + c.share_capital + re_close)

    def test_statement_amounts_are_integers(self) -> None:
        """The roll-forwards and the derived sections stay in integer arithmetic."""
        linkage = cash_flow_linkage.LINKAGE
        amounts = [
            *linkage.movements.model_dump().values(),
            *linkage.cash_flows.model_dump().values(),
        ]
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
        book = matching_allocation.RestingOrders
        self.assertEqual(book(quantities=(1, 1, 1)).pro_rata_shares(2), [0, 0, 0])
        self.assertEqual(book(quantities=(2, 1, 1)).pro_rata_shares(8), [4, 2, 2])
        self.assertEqual(book(quantities=(1, 2, 3)).pro_rata_shares(6), [1, 2, 3])
        self.assertEqual(book(quantities=(1, 2, 3)).pro_rata(6, 2), [0, 2, 3])

    def test_leveling_by_quantity_then_time(self) -> None:
        """Only unallocated orders qualify, larger first, then earlier; one lot each."""
        book = matching_allocation.RestingOrders(quantities=(5, 5, 9, 7))
        self.assertEqual(book.leveling_order([0, 0, 0, 2]), [2, 0, 1])
        self.assertEqual(book.leveling([0, 0, 0, 2], 2), [1, 0, 1, 0])
        self.assertEqual(book.leveling([0, 0, 0, 2], 9), [1, 1, 1, 0])

    def test_split_rounds_fifo_up_and_fifo_fills_in_time_order(self) -> None:
        """The FIFO part of a Split is rounded up; FIFO stops when the lots run out."""
        self.assertEqual(matching_allocation.split_fifo(49, 20), 10)
        self.assertEqual(matching_allocation.split_fifo(49, 1), 1)
        book = matching_allocation.RestingOrders(quantities=(5, 9, 57))
        self.assertEqual(book.fifo(10), [0, 4, 57])
        self.assertEqual(book.fifo(100), [0, 0, 0])
        self.assertEqual(book.quantities, (5, 9, 57))

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
        holidays = us_calendar.federal_holidays(2026)
        self.assertEqual(us_calendar.business_day(2026, 1, 1, holidays), 2)
        self.assertEqual(us_calendar.business_day(2026, 1, 1, set()), 1)
        self.assertEqual(us_calendar.business_day(2026, 2, 1, holidays), 2)


if __name__ == "__main__":
    unittest.main()
