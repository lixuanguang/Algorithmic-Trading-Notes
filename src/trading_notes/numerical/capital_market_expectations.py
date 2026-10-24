"""Capital market expectations: the worked numbers of six CME entries.

Capital market expectations (2026-10-19): the worked numbers of meth:cme-framework-forecasting,
meth:growth-shocks-long-run-expectations, meth:cycle-policy-curve-expectations,
meth:asset-class-return-forecasts, meth:fx-volatility-forecasts and
ex:global-portfolio-macro-rebalancing.

Reproduced from Portfolio Management in Practice, Volume 1 (CFA Institute Investment Series,
2020), chaps. 3-4: the regime example (Example 7, p. 65: expansions of 39 months, contractions
of 20, +2%/-2% a month, long-run 8% a year); long-run equity returns and growth (Example 5, pp.
55-56: baseline 6.75%, P/E effect 51.3% cumulative, -1.71% a year over 30 years);
yield-to-maturity forecasts with rising yields (Example 1, pp. 97-98: -1.09%, 2.71%, 3.44%);
Grinold-Kroner (Example 4, pp. 109-110: 9.5%, long run 7.25%; P/E from 16 to 20 at 4.56%,
2.26%, 0.75% a year over 5, 10, 30 years); Singer-Terhaar for German equities and bonds (p.
114: 3.57/1.05, 5.95/1.75, 3.93/1.16, 6.93%/4.16%); smoothing (eq. 16, p. 135: lambda 0.8 gives
9 times the variance); and the ARCH update (eq. 17, p. 137: 2.0833% and 1.9849%). Original:
sampling error of a historical mean; the three types of growth shock; a Markov regime forecast
computed exactly; the real-estate return equation; a shrinkage covariance estimate against the
sample estimate on simulated data; an exchange-rate forecast combining PPP, UIP and
current-account views; and a global reweighting whose quantified views raise the expected
return per unit of risk.

Count convention: one check is one executed ok() call (a call inside a loop counts once per
iteration). One generator, seeded 20261019, serves parts 1 and 5 in order.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.capital_market_expectations
(numpy, scipy). Exits 1 on failure.
"""

import math
import sys
from itertools import pairwise, product
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray

from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

SEED: Final = 20261019


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def horizon_return(P: Floats, mu: Floats, months: int, start: int = 1) -> float:
    """Return the expected cumulative log return over `months`, starting in state `start`.

    Args:
        P: The monthly transition matrix, expansion then contraction.
        mu: Each state's monthly log return.
        months: The horizon.
        start: The starting state; 1 is contraction.
    """
    state = np.eye(2)[start]
    total = 0.0
    for _ in range(months):
        total += state @ mu
        state = state @ P
    return total


def check_framework(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 1: sampling error of a mean, and the variance hidden by smoothing."""
    print("== part 1: framework and forecasting challenges")
    sigma, years = 0.16, 60
    report.ok(
        "a historical mean from 60 years of 16%-volatility returns has a standard error of 2.07"
        " points: a 95% interval of"
        " about +-4 points around the estimate",
        abs(sigma / math.sqrt(years) - 0.02066) < 1e-5,
    )
    lam = 0.8
    report.ok(
        "smoothing (PMiP eq. 16): with R_t = (1 - lambda) r_t + lambda R_{t-1} and lambda = 0.8,"
        " true variance is (1 + 0.8)/"
        "(1 - 0.8) = 9 times observed, so true volatility is 3 times the appraisal-based figure",
        close((1 + lam) / (1 - lam), 9.0, 1e-12),
    )
    true_r = rng.normal(0.0, 0.10, 200_000)
    obs = np.empty_like(true_r)
    obs[0] = true_r[0]
    for t in range(1, len(true_r)):
        obs[t] = (1 - lam) * true_r[t] + lam * obs[t - 1]
    report.ok(
        "simulated: smoothing the true series with lambda 0.8 cuts its measured variance to 1/9"
        " (within 3%)",
        bool(abs(np.var(true_r) / np.var(obs) / 9 - 1) < 0.03),
        f"ratio {np.var(true_r) / np.var(obs):.3f}",
    )


def check_growth_shocks(report: CheckReport) -> None:
    """Part 2: growth trends and exogenous shocks in long-run expectations."""
    print("== part 2: growth trends and exogenous shocks in long-run expectations")
    base = 0.009 + 0.015 + 0.021 + 0.0225
    report.ok(
        "Example 5: labour input 0.9%, productivity 1.5%, inflation 2.1%, dividend yield 2.25% give"
        " a 6.75% baseline;"
        " a P/E adding 0.95% for 54 years leaves 51.3% (1.67 times) above fair value, -1.71% a year"
        " if unwound over 30"
        " years and -10.26% over 5 (to -3.51%)",
        close(base, 0.0675, 1e-12)
        and close(54 * 0.0095, 0.513, 1e-9)
        and abs(math.exp(0.513) - 1.67) < 0.005
        and abs(0.513 / 30 - 0.0171) < 1e-4
        and close(base - 0.513 / 5, -0.0351, 1e-9),
    )
    g, t10 = 0.02, 10
    type1 = 0.95 * (1 + g) ** t10
    type2 = (1 + 0.015) ** t10
    type3 = 0.95 * (1 + 0.015) ** t10
    report.ok(
        "shocks over 10 years from a 2% trend: a 5% level loss (type 1) leaves output at 1.158; a"
        " growth cut to 1.5% (type"
        " 2) at 1.161 and widening; both (type 3) at 1.103 against 1.219 without the shock",
        abs(type1 - 1.1580) < 1e-3 and abs(type2 - 1.1605) < 1e-3 and abs(type3 - 1.1025) < 1e-3,
    )


def check_regimes(report: CheckReport) -> None:
    """Part 3: the Markov regime chain's stationary and horizon returns, and a trade linkage."""
    print("== part 3: the cycle, policy and the yield curve")
    p_ee, p_cc = 1 - 1 / 39, 1 - 1 / 20  # monthly persistence: expected durations 39 and 20 months
    P = np.array([[p_ee, 1 - p_ee], [1 - p_cc, p_cc]])
    mu = np.array([0.02, -0.02])
    stationary = np.linalg.lstsq(
        np.vstack([P.T - np.eye(2), np.ones(2)]), np.array([0.0, 0.0, 1.0]), rcond=None
    )[0]
    report.ok(
        "Example 7: expected spells of 39 and 20 months put the economy in expansion 66.1% of the"
        " time; the unconditional"
        " log return is 0.644% a month, about 8% a year (the text rounds to two-thirds and 0.67%)",
        bool(abs(stationary[0] - 39 / 59) < 1e-12 and abs(stationary @ mu - 0.006441) < 1e-6),
    )
    r3, r12, r60, r120 = (horizon_return(P, mu, m) for m in (3, 12, 60, 120))
    report.ok(
        "starting in contraction, the homogeneous chain gives expected cumulative log returns of"
        " -5.4% over 3 months, -13.6% over 1 year, 0.8% a year over 5 years"
        " and 4.2% a year over 10: the longer the horizon, the closer to the unconditional log"
        " mean; the book's qualitative"
        " -6%, -18%, 4.8% and ~8% are guideline estimates, not exact outputs of this specified"
        " chain",
        bool(
            abs(r3 + 0.0542) < 5e-4
            and abs(r12 + 0.1362) < 5e-4
            and abs(r60 / 5 - 0.0080) < 5e-4
            and abs(r120 / 10 - 0.0423) < 5e-4
            and r3 / 3 < r12 / 12 < r60 / 60 < r120 / 120 < stationary @ mu
        ),
        f"{r3:.4f} {r12:.4f} {r60 / 5:.4f} {r120 / 10:.4f}",
    )
    # Conditional means alone do not identify wealth. Add deterministic state log returns
    # only for the wealth illustration. Exhaustively enumerate short paths independently.
    D = np.diag(np.exp(mu))
    for horizon in (1, 3, 12):
        logs, wealth = 0.0, 0.0
        for tail in product((0, 1), repeat=horizon - 1):
            path = (1, *tail)
            probability = math.prod(P[a, b] for a, b in pairwise(path))
            log_total = sum(mu[j] for j in path)
            logs += probability * log_total
            wealth += probability * math.exp(log_total)
        matrix_wealth = np.eye(2)[1] @ D @ np.linalg.matrix_power(P @ D, horizon - 1) @ np.ones(2)
        report.ok(
            f"{horizon} months: path enumeration reconciles log sums and expected wealth",
            bool(close(logs, horizon_return(P, mu, horizon)) and close(wealth, matrix_wealth)),
        )
        report.ok(
            f"{horizon} months: geometric equivalent is not expected wealth",
            wealth >= math.exp(logs) - 1e-12 and (horizon == 1 or wealth > math.exp(logs) + 1e-7),
        )
    report.ok(
        "stationary annual log return and geometric equivalent",
        bool(
            close(12 * stationary @ mu, 0.07728813559322034)
            and abs(math.expm1(12 * stationary @ mu) - 0.080353) < 1e-6
        ),
    )

    trade_share, elasticity, shock = 0.25, 0.8, -0.04
    report.ok(
        "cross-economy linkage: if exports to a partner are 25% of GDP and respond with elasticity"
        " 0.8 to its 4% fall in"
        " demand, the exporter's GDP falls by 0.8% before second-round effects",
        close(trade_share * elasticity * shock, -0.008, 1e-12),
    )


def check_asset_classes(report: CheckReport) -> None:
    """Part 4: fixed income, equities and real estate."""
    print("== part 4: fixed income, equities and real estate")
    dur, ytm, dy = 4.84, 0.0325, 0.02
    loss = dur * dy
    r2 = ytm + (-loss + 0.010) / 2
    r5 = ytm + (-loss + 0.010 + 0.060) / 5
    r7 = ytm + (-loss + 0.010 + 0.060 + 0.040) / 7
    report.ok(
        "Example 1: modified duration 4.84, YTM 3.25%, yields +200 bp over two years: about -1.09%"
        " a"
        " year over 2 years,"
        " 2.71% over 5 and 3.44% over 7; Macaulay duration is 5.0",
        abs(r2 + 0.0109) < 5e-5
        and abs(r5 - 0.0271) < 5e-5
        and abs(r7 - 0.0344) < 5e-5
        and abs(dur * (1 + ytm) - 5.0) < 0.005,
    )
    report.ok(
        "building blocks: short default-free rate 2.0% + term premium 1.0% + credit premium 1.2% +"
        " liquidity premium 0.3% ="
        " 4.5% for an investment-grade corporate bond fund",
        close(0.020 + 0.010 + 0.012 + 0.003, 0.045, 1e-12),
    )
    gk = 0.0225 + (0.06 - (-0.01)) + 0.0025
    report.ok(
        "Example 4 (Grinold-Kroner): 2.25% yield + (6% earnings growth + 1% net buybacks) + 0.25%"
        " P/E expansion = 9.5%; the"
        " sustainable long-run figure is 7.25% (yield + nominal GDP growth)",
        close(gk, 0.095, 1e-12) and close(0.0225 + 0.05, 0.0725, 1e-12),
    )
    pe_rates = {n: (20 / 16) ** (1 / n) - 1 for n in (5, 10, 30)}
    report.ok(
        "a P/E reverting from 16 to 20 implies 4.56% a year over 5 years, 2.26% over 10 and 0.75%"
        " over 30: horizon-specific"
        " growth rates must not be extrapolated",
        abs(pe_rates[5] - 0.0456) < 5e-5
        and abs(pe_rates[10] - 0.0226) < 5e-5
        and abs(pe_rates[30] - 0.0075) < 5e-5,
    )
    sr_g = 0.30
    rp_g = {"equity": 0.70 * 0.17 * sr_g, "bond": 0.50 * 0.07 * sr_g}
    rp_s = {"equity": 0.17 * 0.35, "bond": 0.07 * 0.25}
    rp = {k: 0.85 * rp_g[k] + 0.15 * rp_s[k] for k in rp_g}
    report.ok(
        "Singer-Terhaar (German assets): integrated premia 3.57% and 1.05%, segmented 5.95% and"
        " 1.75%, at 85% integration"
        " 3.93% and 1.16%; with a 3% risk-free rate, 6.93% and 4.16%",
        round(rp_g["equity"], 4) == 0.0357
        and round(rp_g["bond"], 4) == 0.0105
        and round(rp["equity"], 4) == 0.0393
        and round(rp["bond"], 4) == 0.0116
        and round(0.03 + rp["equity"], 4) == 0.0693
        and round(0.03 + rp["bond"], 4) == 0.0416,
    )
    # Forward-NOI timing: income in year one is 5; the sale capitalizes year-two NOI.
    price0, income1, income2, cap1 = 100.0, 5.0, 5.125, 0.053
    sale1 = income2 / cap1
    ledger_return = (income1 + sale1 - price0) / price0
    cap0 = income1 / price0
    relative_cap_change = cap1 / cap0 - 1
    approx_return = cap0 + income2 / income1 - 1 - relative_cap_change
    report.ok(
        "cap change is 6% relative, and first-order return 1.5%",
        close(relative_cap_change, 0.06) and close(approx_return, 0.015),
    )
    report.ok(
        "cash-income plus terminal-value ledger gives 1.698113%, within 0.2 point of first order",
        close(ledger_return, 0.0169811320754717) and abs(ledger_return - approx_return) < 0.002,
    )
    report.ok(
        "stable-cap-rate control: value 102.5 plus income 5 gives exactly 7.5%",
        close((income1 + income2 / cap0 - price0) / price0, 0.075),
    )
    # Independent finite perturbation checks the first derivative of the cash ledger.
    eps = 1e-5
    near = (income1 + income1 * (1 + eps * 0.025) / (cap0 * (1 + eps * 0.06))) / price0 - 1
    report.ok(
        "small changes converge to first-order cap-rate sensitivity",
        abs((near - cap0) / eps - (0.025 - 0.06)) < 1e-7,
    )


def check_fx_volatility(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 5: the ARCH update, a shrinkage covariance estimate and a combined FX view."""
    print("== part 5: exchange rates and volatility")
    gam, alpha_, beta_ = 0.000002, 0.9, 0.08
    var_prev = 0.0004
    var_t = gam + alpha_ * var_prev + beta_ * 0.03**2
    var_alt = gam + alpha_ * var_prev + beta_ * 0.02**2
    report.ok(
        "ARCH (eq. 17): gamma 0.000002, persistence 0.9, shock weight 0.08; long-run variance"
        " 0.0001"
        " (1% a day); from"
        " 0.0004 a 3% surprise gives 2.0833% and a 2% surprise 1.9849%",
        close(gam / (1 - alpha_ - beta_), 0.0001, 1e-15)
        and abs(math.sqrt(var_t) - 0.020833) < 1e-6
        and abs(math.sqrt(var_alt) - 0.019849) < 1e-6,
    )
    n_assets, n_obs = 10, 60
    true_corr = 0.5
    true_cov = (
        np.full((n_assets, n_assets), true_corr) + (1 - true_corr) * np.eye(n_assets)
    ) * 0.04
    err_sample, err_shrunk = [], []
    for _ in range(300):
        x = rng.multivariate_normal(np.zeros(n_assets), true_cov, n_obs)
        s = np.cov(x, rowvar=False)
        vols = np.sqrt(np.diag(s))
        rbar = (s / np.outer(vols, vols))[~np.eye(n_assets, dtype=bool)].mean()
        target = rbar * np.outer(vols, vols)
        np.fill_diagonal(target, np.diag(s))
        shrunk = 0.5 * s + 0.5 * target
        err_sample.append(np.sum((s - true_cov) ** 2))
        err_shrunk.append(np.sum((shrunk - true_cov) ** 2))
    report.ok(
        "shrinkage: with 10 assets and 60 observations, averaging the sample covariance with a"
        " constant-correlation target"
        " (weight 0.5) cuts the mean squared estimation error versus the true matrix",
        bool(np.mean(err_shrunk) < np.mean(err_sample)),
        f"MSE ratio {np.mean(err_shrunk) / np.mean(err_sample):.3f}",
    )
    ppp_view = (
        0.02 - 0.035
    )  # inflation 2% at home, 3.5% abroad: foreign currency falls 1.5%/yr (d/f)
    uip_view = 0.04 - 0.055  # interest differential implies the same direction
    ca_view = -0.01  # widening foreign deficit: extra 1% pressure
    report.ok(
        "an exchange-rate view combining relative PPP (-1.5% a year for the foreign currency), the"
        " interest differential"
        " (-1.5%) and a current-account adjustment (-1%) gives -2.5% if the first two are treated"
        " as one anchor, not -4%:"
        " the two parity views share the inflation differential",
        close(ppp_view, uip_view, 1e-12)
        and close(0.5 * (ppp_view + uip_view) + ca_view, -0.025, 1e-12),
    )


def check_reweighting(report: CheckReport) -> None:
    """Part 6: a global reweighting on macro views raises return per unit of risk."""
    print("== part 6: reweighting a global portfolio on macro views")
    # equity A (near trough), equity B (near peak), bonds A, bonds B
    er = np.array([0.075, 0.055, 0.035, 0.040])
    vol = np.array([0.18, 0.16, 0.06, 0.05])
    corr = np.array(
        [[1, 0.7, -0.1, 0.0], [0.7, 1, 0.0, -0.1], [-0.1, 0.0, 1, 0.6], [0.0, -0.1, 0.6, 1]]
    )
    cov = np.outer(vol, vol) * corr
    w0 = np.array([0.30, 0.30, 0.20, 0.20])
    w1 = np.array([0.38, 0.24, 0.18, 0.20])  # equities from B to A, a little less bond A

    def sr(w: Floats) -> float:
        return float((w @ er - 0.02) / math.sqrt(w @ cov @ w))

    report.ok(
        "macro views (A near its trough: higher expected equity return; B near its peak) adding 8"
        " points to equity"
        " A, funded by 6 points from equity B and 2 from bond A, raises expected return from 5.40%"
        " to 5.60% and the ratio of excess return to risk",
        bool(
            abs(w0 @ er - 0.0540) < 1e-12
            and abs(w1 @ er - 0.0560) < 1e-12
            and sr(w1) > sr(w0)
            and close(w1.sum(), 1.0)
            and np.allclose(w1 - w0, [0.08, -0.06, -0.02, 0.0])
        ),
        f"Sharpe {sr(w0):.3f} -> {sr(w1):.3f}",
    )


def main() -> int:
    """Print the versions, then run the six parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_framework(report, rng)
    check_growth_shocks(report)
    check_regimes(report)
    check_asset_classes(report)
    check_fx_volatility(report, rng)
    check_reweighting(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
