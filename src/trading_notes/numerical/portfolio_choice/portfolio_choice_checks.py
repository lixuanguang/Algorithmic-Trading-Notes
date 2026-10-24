"""Worked examples of asset-class history, risk aversion, the efficient frontier and the CAL."""

import math
import re
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, optimize, stats

from trading_notes.numerical.portfolio_choice.frontier import (
    MeanVarianceFrontier,
    mean_variance_utility,
)
from trading_notes.numerical.portfolio_choice.history import AssetClassHistory
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

DATA: Final = Path("notes/artefacts/portfolio-risk-return/us-asset-class-returns-1928-2025.csv")
FIGURE: Final = Path("compendium/portfolio-construction-risk/figures/mean-sd-frontier.tikz")
A: Final = 3.0  # risk aversion of parts 2 and 4
RF: Final = 0.03
# Invented inputs of parts 3 and 4: funds E, B and P.
MU: Final = (0.08, 0.035, 0.06)
SD: Final = (0.18, 0.06, 0.12)
CORR: Final = ((1.0, 0.1, 0.6), (0.1, 1.0, 0.3), (0.6, 0.3, 1.0))


def utility(m: float, s: float, a: float = A) -> float:
    """Return mean-variance utility with risk aversion a, by default part 2's A = 3."""
    return mean_variance_utility(m, s, a)


def funds() -> MeanVarianceFrontier:
    """Return the frontier of the three invented funds, as new arrays."""
    sd = np.array(SD)
    return MeanVarianceFrontier(mu=np.array(MU), cov=np.outer(sd, sd) * np.array(CORR))


def slsqp(
    objective: Callable[[Floats], float],
    constraints: list[Callable[[Floats], float]],
    long_only: bool = False,
    maxiter: int = 1000,
) -> optimize.OptimizeResult[np.float64]:
    """Minimise an objective of three weights by SLSQP from equal weights, as a reference route."""
    return optimize.minimize(
        objective,
        np.ones(3) / 3,
        bounds=[(0, None)] * 3 if long_only else None,
        constraints=[{"type": "eq", "fun": c} for c in constraints],
        method="SLSQP",
        options={"ftol": 1e-15, "maxiter": maxiter},
    )


def numerical_frontier(
    f: MeanVarianceFrontier, m: float, long_only: bool = False
) -> optimize.OptimizeResult[np.float64]:
    """Return SLSQP's minimum-variance portfolio at mean m, independent of the closed form."""
    return slsqp(
        lambda w: float(w @ f.cov @ w),
        [lambda w: float(w.sum() - 1), lambda w: float(w @ f.mu - m)],
        long_only,
    )


def check_history(report: CheckReport, history: AssetClassHistory) -> None:
    """Check the US asset-class history against the workbook's summary rows."""
    print("== part 1: US asset-class history, 1928-2025 (Damodaran, January 2026 update)")
    years, series = history.years, history.series
    report.ok(
        "98 years, 1928 to 2025, no gaps",
        bool(len(years) == 98 and (np.diff(years) == 1).all() and years[-1] == 2025),
    )
    # The workbook's 'Arithmetic Average' and 'Geometric Average' rows, 1928-2025, to four decimals.
    reported = {
        "sp500": (0.1185, 0.1002),
        "tbill_3m": (0.0341, 0.0337),
        "tbond_10y": (0.0482, 0.0453),
        "baa_corp": (0.0690, 0.0663),
        "real_estate": (0.0438, 0.0420),
        "gold": (0.0736, 0.0561),
    }
    stats_tab = {}
    for name, (arith_rep, geo_rep) in reported.items():
        r = series[name]
        arith = r.mean()
        geo = np.prod(1 + r) ** (1 / len(r)) - 1
        sd = r.std(ddof=1)
        real_geo = np.prod((1 + r) / (1 + series["cpi_inflation"])) ** (1 / len(r)) - 1
        worst = (r.min(), int(years[r.argmin()]))
        stats_tab[name] = (arith, geo, sd, real_geo, worst)
        report.ok(
            f"{name}: arithmetic {arith:.4f}, geometric {geo:.4f} match the workbook's"
            f" {arith_rep}, {geo_rep}",
            bool(abs(arith - arith_rep) < 5e-5 and abs(geo - geo_rep) < 5e-5),
            f"s.d. {sd:.4f}, real geometric {real_geo:.4f}, worst {worst[0]:.4f} in {worst[1]}",
        )
    infl = series["cpi_inflation"]
    report.ok(
        "CPI inflation 1928-2025: geometric mean 3.04 percent",
        close(float(np.prod(1 + infl)) ** (1 / 98) - 1, 0.030357, 5e-6),
        f"{np.prod(1 + infl) ** (1 / 98) - 1:.6f}",
    )
    report.ok(
        "geometric below arithmetic for every series, by roughly half the variance",
        all(v[1] < v[0] and abs((v[0] - v[1]) - v[2] ** 2 / 2) < 0.012 for v in stats_tab.values()),
        ", ".join(
            f"{k} gap {v[0] - v[1]:.4f} vs s^2/2 {v[2] ** 2 / 2:.4f}" for k, v in stats_tab.items()
        ),
    )
    excess = series["sp500"] - series["tbond_10y"]
    report.ok(
        "stocks minus T.bonds, 1928-2025: arithmetic mean 7.03 percent, standard error 2.10"
        " percent",
        close(excess.mean(), 0.070323, 5e-6)
        and close(excess.std(ddof=1) / math.sqrt(98), 0.021028, 5e-6),
        f"mean {excess.mean():.6f}, s.e. {excess.std(ddof=1) / math.sqrt(98):.6f}",
    )
    last10 = years >= 2016
    report.ok(
        "2016-2025 arithmetic means differ from the full sample (stocks 15.75, T.bonds 1.22, gold"
        " 16.53)",
        close(series["sp500"][last10].mean(), 0.1575, 5e-5)
        and close(series["tbond_10y"][last10].mean(), 0.0122, 5e-5)
        and close(series["gold"][last10].mean(), 0.1653, 5e-5),
    )
    stock_neg = int((series["sp500"] < 0).sum())
    report.ok("stocks fell in 26 of the 98 years", stock_neg == 26, f"{stock_neg}")
    real_neg = int(((1 + series["tbill_3m"]) / (1 + infl) < 1).sum())
    report.ok(
        "the T.bill never had a negative annual return; real T.bill return negative in 40 years",
        bool((series["tbill_3m"] >= 0).all()) and real_neg == 40,
        f"{real_neg}",
    )


def check_risk_aversion(report: CheckReport) -> None:
    """Check mean-variance utility, CARA-normal certainty equivalents and log utility."""
    print("== part 2: risk aversion and mean-variance utility")
    report.ok(
        "A = 3: E 0.07, s.d. 0.15 gives U = 0.03625 (decimals); in percent units U = 7 - 0.005 x 3"
        " x 225 = 3.625",
        close(utility(0.07, 0.15), 0.03625) and close(7 - 0.5 * A * 15**2 / 100, 3.625),
    )
    report.ok(
        "the same risky portfolio is worth less than a 4 percent riskless rate to A = 3 and more to"
        " A = 1",
        utility(0.07, 0.15) < 0.04 and utility(0.07, 0.15, 1.0) > 0.04,
        f"A = 1: {utility(0.07, 0.15, 1.0):.5f}",
    )
    report.ok(
        "A = 0 (risk neutral) ranks by expected return only", close(utility(0.07, 0.15, 0.0), 0.07)
    )
    # CARA utility u(W) = -exp(-a W) with normal W: the certainty equivalent is exactly
    # mu_W - a s_W^2 / 2.
    W0, a_abs = 100.0, 0.03  # wealth in dollars and absolute risk aversion per dollar; a W0 = 3
    muW, sW = W0 * 1.07, W0 * 0.15
    EU = integrate.quad(
        lambda w: -math.exp(-a_abs * w) * stats.norm.pdf(w, muW, sW), muW - 12 * sW, muW + 12 * sW
    )[0]
    CE = -math.log(-EU) / a_abs
    report.ok(
        "CARA-normal: certainty equivalent by integration = mu - a s^2 / 2 = 103.625 (a W0 = 3,"
        " i.e. A = 3)",
        close(CE, muW - 0.5 * a_abs * sW**2, 1e-6)
        and close(CE / W0 - 1, utility(0.07, 0.15), 1e-8),
        f"CE {CE:.6f}",
    )
    # Log utility (relative risk aversion 1) and a two-point return: the Arrow-Pratt
    # approximation s^2 R / 2 of the risk premium is close for small risks and poor for large ones.
    for h in (0.05, 0.40):
        ce_log = math.exp(0.5 * math.log(1 + h) + 0.5 * math.log(1 - h)) - 1  # mean return 0
        prem = 0.0 - ce_log
        approx = 0.5 * h * h
        print(f"    two-point +/-{h:.2f}: exact premium {prem:.6f}, approximation {approx:.6f}")
    ce5 = math.sqrt(1 - 0.05**2) - 1
    ce40 = math.sqrt(1 - 0.40**2) - 1
    report.ok(
        "log utility, +/-5 percent: premium 0.1251 percent vs 0.1250; +/-40 percent: 8.35 vs 8.00"
        " percent",
        close(-ce5, 0.0012508, 1e-7) and close(-ce40, 0.083485, 1e-6),
    )
    report.ok(
        "concave utility rejects a fair bet: E[ln(1 + r)] < ln(1 + E r) for r = +/-0.2",
        0.5 * math.log(1.2) + 0.5 * math.log(0.8) < 0.0,
    )


def check_frontier(report: CheckReport, f: MeanVarianceFrontier) -> None:
    """Check the feasible set, the minimum-variance frontier and the efficient frontier."""
    print(
        "== part 3: feasible set, minimum-variance frontier and efficient frontier (invented"
        " inputs)"
    )
    mu, S = f.mu, f.cov
    one = np.ones(3)
    report.ok(
        "covariance matrix positive definite (eigenvalues > 0)",
        bool(np.linalg.eigvalsh(S).min() > 0),
        f"{np.linalg.eigvalsh(S)}",
    )
    a_, b_, c_, d_ = f.constants
    report.ok(
        "D = AC - B^2 > 0 because mu is not proportional to the vector of ones",
        d_ > 0,
        f"A {a_:.4f} B {b_:.4f} C {c_:.4f} D {d_:.4f}",
    )
    wg = f.global_minimum_variance()
    mg, sg = f.mean(wg), f.sd(wg)
    print(f"    GMV weights {wg.round(4)}, mean {mg:.6f}, s.d. {sg:.6f}")
    res = slsqp(lambda w: float(w @ S @ w), [lambda w: float(w.sum() - 1)], maxiter=500)
    report.ok(
        "GMV: Sigma^-1 1 / (1' Sigma^-1 1) = numerical minimum; weights 0.0536, 0.8933, 0.0531;"
        " mean 3.874, s.d. 5.821",
        bool(
            np.allclose(res.x, wg, atol=1e-6)
            and np.allclose(wg, [0.053563, 0.893327, 0.053109], atol=1e-6)
        )
        and close(mg, b_ / a_)
        and close(sg**2, 1 / a_)
        and close(mg, 0.038738, 1e-6)
        and close(sg, 0.058211, 1e-6),
    )
    table = {}
    agree = True
    for m in (0.05, 0.06, 0.07, 0.075, 0.08, 0.09):
        w = f.weights(m)
        r = numerical_frontier(f, m)
        table[m] = (w, math.sqrt(f.variance(m)))
        agree &= bool(np.allclose(r.x, w, atol=1e-6)) and close(
            float(w @ S @ w), f.variance(m), 1e-12
        )
        print(
            f"    target {m:.3f}: unconstrained weights {w.round(4)},"
            f" s.d. {math.sqrt(f.variance(m)):.4f}"
        )
    report.ok(
        "closed-form target-return weights = SLSQP at 5, 6, 7, 7.5, 8 and 9 percent; variance"
        " formula = w'Sw",
        agree,
    )
    report.ok(
        "unconstrained frontier: 6 percent needs weights 0.3718, 0.2974, 0.3308 and s.d. 10.11"
        " percent",
        bool(np.allclose(table[0.06][0], [0.371783, 0.297426, 0.330791], atol=1e-6))
        and close(table[0.06][1], 0.101114, 1e-6),
    )
    # The unconstrained bond weight w_B(m) is linear in m; find where it reaches zero.
    m_star = optimize.brentq(lambda m: float(f.weights(m)[1]), 0.06, 0.08)
    report.ok(
        "unconstrained bond weight falls to zero at a 7.06 percent target and is negative above it"
        " (-0.2631 at 8)",
        close(m_star, 0.070612, 1e-6)
        and f.weights(0.08)[1] < 0
        and close(f.weights(0.08)[1], -0.263108, 1e-6),
        f"{m_star:.6f}",
    )
    w75 = numerical_frontier(f, 0.075, long_only=True).x
    # Long-only at 7.5 percent: B = 0 binds. On the active set {E, P} the solution is the
    # two-asset frontier point, and the KKT multiplier on w_B >= 0 is non-negative.
    wEP = np.array([(0.075 - 0.06) / (0.08 - 0.06), 0.0, 1 - (0.075 - 0.06) / (0.08 - 0.06)])
    grad = 2 * S @ wEP
    M = np.array([[1.0, mu[0]], [1.0, mu[2]]])
    nu = np.linalg.solve(M, grad[[0, 2]])  # grad_i = nu0 + nu1 mu_i for the free assets
    kkt_B = grad[1] - (nu[0] + nu[1] * mu[1])
    report.ok(
        "long-only 7.5 percent: boundary solution 0.75 E, 0 B, 0.25 P (s.d. 15.49 percent); KKT"
        " multiplier on w_B > 0",
        bool(np.allclose(w75, wEP, atol=1e-5))
        and kkt_B > 0
        and close(math.sqrt(wEP @ S @ wEP), 0.154871, 1e-6),
        f"multiplier {kkt_B:.6f}, unconstrained s.d. {table[0.075][1]:.4f}",
    )
    # Where the unconstrained optimum already satisfies w >= 0, the long-only optimum is the same
    # portfolio; the 7.5 percent target is where the constraint changes the answer.
    interior = all(
        bool((f.weights(m) > 1e-3).all())
        and bool(np.allclose(numerical_frontier(f, m, long_only=True).x, f.weights(m), atol=1e-5))
        for m in (0.05, 0.06)
    )
    report.ok(
        "5 and 6 percent: unconstrained weights strictly positive, so the long-only optimum is"
        " identical; 7.5 percent differs (w_B = 0, s.d. 15.49 against 15.25)",
        interior
        and f.weights(0.075)[1] < 0
        and math.sqrt(wEP @ S @ wEP) > math.sqrt(f.variance(0.075)) + 1e-3,
    )
    lo8 = numerical_frontier(f, 0.08, long_only=True)
    report.ok(
        "long-only 8 percent: only E is feasible (s.d. 18)",
        bool(np.allclose(lo8.x, [1, 0, 0], atol=1e-6)),
    )
    lo9 = numerical_frontier(f, 0.09, long_only=True)
    report.ok(
        "long-only 9 percent is infeasible: above the largest expected return; the optimiser"
        " reports failure",
        (not lo9.success)
        or abs(f.mean(np.asarray(lo9.x, dtype=np.float64)) - 0.09) > 1e-6
        or bool((lo9.x < -1e-9).any()),
        f"success={lo9.success}, message={lo9.message}",
    )
    # A point on the lower branch is dominated by the frontier point with the same s.d. above the
    # GMV, its mirror image about the GMV mean.
    m_low = 0.03
    s_low = math.sqrt(f.variance(m_low))
    m_up = 2 * mg - m_low
    report.ok(
        "3 percent lies on the inefficient branch: the 4.75 percent frontier portfolio has the same"
        " s.d. (6.74)",
        close(f.variance(m_up), f.variance(m_low), 1e-12)
        and close(m_up, 0.047476, 1e-6)
        and close(s_low, 0.067402, 1e-6),
        f"{m_up:.6f}, {s_low:.6f}",
    )
    m_at_6 = mg + math.sqrt((0.06**2 - 1 / a_) * d_ / a_)
    report.ok(
        "bond fund alone: frontier s.d. at 3.5 percent is 5.99986 < 6.00; efficient mean at s.d. 6"
        " is 4.2478 percent",
        math.sqrt(f.variance(0.035)) < 0.06
        and close(math.sqrt(f.variance(0.035)), 0.05999857, 1e-8)
        and close(m_at_6, 0.042478, 1e-6)
        and close(f.variance(m_at_6), 0.06**2, 1e-12),
    )
    # Singular covariance: two perfectly correlated assets; the inverse does not exist.
    S_sing = np.outer([0.2, 0.1], [0.2, 0.1])
    report.ok(
        "a 2x2 covariance with correlation +1 is singular (rank 1)",
        bool(np.linalg.matrix_rank(S_sing) == 1),
    )
    Si, flat = f.inverse, np.full(3, 0.05)
    report.ok(
        "equal expected returns make D = 0: the frontier is a single point in mean",
        close((one @ Si @ one) * (flat @ Si @ flat) - (one @ Si @ flat) ** 2, 0.0, 1e-9),
    )
    # No long-only portfolio on a grid over the simplex lies left of the frontier.
    grid = [
        np.array([x, y, 1 - x - y])
        for x in np.linspace(0, 1, 201)
        for y in np.linspace(0, 1, 201)
        if x + y <= 1 + 1e-12
    ]
    pts = np.array([(w @ mu, math.sqrt(max(w @ S @ w, 0.0))) for w in grid])
    report.ok(
        "grid of 20,301 long-only portfolios: none lies left of the unconstrained frontier",
        all(s >= math.sqrt(f.variance(m)) - 1e-12 for m, s in pts),
    )


def check_capital_allocation(
    report: CheckReport, f: MeanVarianceFrontier
) -> tuple[float, tuple[float, float]]:
    """Check the tangency portfolio, the CAL and optimal allocations with borrowing costs.

    Returns:
        The tangency's Sharpe ratio and the A = 4 optimum (mean, s.d.), for the figure check.
    """
    print("== part 4: risk-free asset, capital allocation line and optimal allocation")
    mu, rf = f.mu, RF
    a_, b_, _, d_ = f.constants
    wg = f.global_minimum_variance()
    mg = f.mean(wg)
    wt = f.tangency(rf)
    mt, st = f.mean(wt), f.sd(wt)
    sharpe = (mt - rf) / st
    report.ok("tangency exists on the upper branch: GMV mean 3.874 > rf 3.0", mg > rf)
    res_t = slsqp(lambda w: -f.sharpe(w, rf), [lambda w: float(w.sum() - 1)])
    report.ok(
        "tangency Sigma^-1 (mu - rf 1) normalised = maximum-Sharpe SLSQP: 0.4374, 0.1745, 0.3881;"
        " mean 6.438, s.d. 11.547",
        bool(
            np.allclose(res_t.x, wt, atol=1e-5)
            and np.allclose(wt, [0.437403, 0.174545, 0.388052], atol=1e-6)
        )
        and close(mt, 0.064384, 1e-6)
        and close(st, 0.115473, 1e-6),
        f"Sharpe {sharpe:.6f}",
    )
    report.ok(
        "Sharpe ratio of the tangency (slope of the CAL) 0.2978", close(sharpe, 0.297771, 1e-6)
    )
    report.ok(
        "the tangency is also on the minimum-variance frontier (variance formula at its mean)",
        close(st**2, f.variance(mt), 1e-12),
    )
    report.ok(
        "CALs through the GMV, the 7 percent frontier portfolio and a 60/20/20 mix are flatter",
        all(
            f.sharpe(w_any, rf) <= sharpe + 1e-12
            for w_any in (wg, f.weights(0.07), np.array([0.6, 0.2, 0.2]))
        ),
    )
    ystar = {Aa: (mt - rf) / (Aa * st * st) for Aa in (2.0, 4.0, 8.0)}
    print("    y* =", {k: round(v, 4) for k, v in ystar.items()})
    report.ok(
        "optimal risky share y* = (E r_T - rf)/(A s_T^2): 1.2894 (borrow), 0.6447, 0.3223",
        close(ystar[2.0], 1.289357, 1e-6)
        and close(ystar[4.0], 0.644679, 1e-6)
        and close(ystar[8.0], 0.322339, 1e-6),
    )
    yy = np.linspace(-0.5, 3, 35001)
    report.ok(
        "y* equals the grid maximiser of U(y) for A = 2, 4, 8",
        all(
            abs(yy[np.argmax(rf + yy * (mt - rf) - 0.5 * Aa * (yy * st) ** 2)] - y) < 1e-4
            for Aa, y in ystar.items()
        ),
    )
    pos4 = (rf + ystar[4.0] * (mt - rf), ystar[4.0] * st)
    report.ok(
        "A = 4: 64.5 percent in T, 35.5 percent lent; mean 5.217, s.d. 7.444; U = 0.04108",
        close(pos4[0], 0.052167, 1e-6)
        and close(pos4[1], 0.074443, 1e-6)
        and close(utility(pos4[0], pos4[1], 4.0), 0.041083, 1e-6),
        f"{pos4}",
    )
    pos2 = (rf + ystar[2.0] * (mt - rf), ystar[2.0] * st)
    report.ok(
        "A = 2: 128.9 percent in T financed by borrowing 28.9 percent at 3; mean 7.433, s.d."
        " 14.889",
        close(pos2[0], 0.074334, 1e-6) and close(pos2[1], 0.148886, 1e-6),
    )
    # A borrowing rate above the GMV mean has no upper-branch tangency:
    # 1' Sigma^-1 (mu - r 1) = B - r A < 0.
    z5 = float((f.inverse @ (mu - 0.05)).sum())
    w5 = f.tangency(0.05)
    report.ok(
        "r = 5 percent > GMV mean 3.874: the normalised formula gives a lower-branch point (mean"
        " 1.88 percent)",
        z5 < 0
        and close(z5, b_ - 0.05 * a_)
        and f.mean(w5) < mg
        and close(f.mean(w5), 0.018839, 1e-6),
        f"sum {z5:.4f}",
    )
    # Borrowing at 3.5 percent (lending stays at 3): the borrowing line is tangent at a riskier
    # frontier portfolio, which in this unconstrained example shorts B.
    rb = 0.035
    wb = f.tangency(rb)
    mb, sb = f.mean(wb), f.sd(wb)
    y_b = (mb - rb) / (2.0 * sb * sb)
    print(
        f"    borrowing tangency {wb.round(4)}, mean {mb:.6f}, s.d. {sb:.6f}, y at rb for A=2:"
        f" {y_b:.4f}"
    )
    report.ok(
        "borrowing at 3.5 percent: tangency 0.9508, -0.7869, 0.8361 (mean 9.87, s.d. 24.03); for"
        " A = 2, y = 0.55 < 1",
        bool(np.allclose(wb, [0.950820, -0.786885, 0.836066], atol=1e-6))
        and close(mb, 0.098689, 1e-6)
        and close(sb, 0.240277, 1e-6)
        and close(y_b, 0.551577, 1e-6),
    )

    # With lending at 3 and borrowing at 3.5 percent the A = 2 investor wants y > 1 on the
    # lending line and y < 1 on the borrowing line, so holds a frontier portfolio between the
    # two tangencies, maximising mu_p - (A/2) s_p^2 along the frontier.
    def u_front(m: float) -> float:
        return m - 1.0 * f.variance(m)

    m_opt = optimize.minimize_scalar(
        lambda m: -u_front(m), bounds=(mt, mb), method="bounded", options={"xatol": 1e-12}
    ).x
    report.ok(
        "A = 2 with 3.5 percent borrowing: frontier portfolio with mean 7.18 and s.d. 14.11,"
        " between the tangencies",
        bool(mt < m_opt < mb)
        and close(m_opt, b_ / a_ + d_ / (2.0 * a_), 1e-6)
        and close(m_opt, 0.071805, 1e-6)
        and close(math.sqrt(f.variance(m_opt)), 0.141146, 1e-6),
        f"{m_opt:.6f}, weights {f.weights(m_opt).round(4)}",
    )
    report.ok(
        "its utility 0.05188 beats lending-line and borrowing-line choices restricted to y <= 1 and"
        " y >= 1",
        u_front(m_opt)
        >= max(utility(rf + y * (mt - rf), y * st, 2.0) for y in np.linspace(0, 1, 1001)) - 1e-12
        and u_front(m_opt)
        >= max(utility(rb + y * (mb - rb), y * sb, 2.0) for y in np.linspace(1, 3, 2001)) - 1e-12
        and close(u_front(m_opt), 0.051884, 1e-6),
        f"{u_front(m_opt):.6f}",
    )
    return sharpe, pos4


def figure_coordinates(txt: str, tag: str) -> Floats:
    """Return the (s.d., mean) coordinates, in percent, of the plot under `% <tag>`.

    Raises:
        ValueError: If the figure has no such plot.
    """
    match = re.search(rf"% {tag}\n.*?coordinates \{{(.*?)\}}", txt, re.S)
    if match is None:
        raise ValueError(f"no plot tagged {tag!r} in the figure")
    points = re.findall(r"\(([^)]*)\)", match.group(1))
    return np.array([[float(v) for v in p.split(",")] for p in points])


def check_figure(
    report: CheckReport,
    f: MeanVarianceFrontier,
    figure: str,
    sharpe: float,
    pos4: tuple[float, float],
) -> None:
    """Check the mean-standard deviation diagram's coordinates against the computed frontier."""
    print("== figure: mean-standard deviation diagram coordinates")
    upper = figure_coordinates(figure, "efficient")
    lower = figure_coordinates(figure, "inefficient")
    lo_front = figure_coordinates(figure, "long-only")
    report.ok(
        "figure: efficient and inefficient branches are (100 s, 100 m) of the closed-form frontier"
        " to 0.01",
        all(
            abs(100 * math.sqrt(f.variance(m / 100)) - s) < 0.006
            for s, m in np.vstack([upper, lower])
        ),
    )
    report.ok(
        "figure: long-only frontier points match SLSQP with w >= 0 to 0.01",
        all(
            abs(100 * math.sqrt(numerical_frontier(f, m / 100, long_only=True).fun) - s) < 0.006
            for s, m in lo_front
        ),
    )
    report.ok(
        "figure: T, GMV, E, B, P, the A = 4 optimum (7.44, 5.22) and the CAL end (24, 10.147) as"
        " computed",
        all(
            s in figure
            for s in (
                "(11.55,6.44)",
                "(5.82,3.87)",
                "(18,8)",
                "(6,3.5)",
                "(12,6)",
                "(7.44,5.22)",
                "(24,10.147)",
            )
        )
        and close(3 + sharpe * 24, 10.147, 1e-3)
        and close(100 * pos4[1], 7.44, 0.005)
        and close(100 * pos4[0], 5.22, 0.005),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Read the history and the figure from the repository root, then run the parts.

    Part 1 recomputes the means that Damodaran's workbook reports (January 2026 update) from the
    transcribed CSV and adds standard deviations, worst years and real geometric means: dated
    historical statistics of one country's realised returns, not expected returns. Parts 2-4 use
    invented inputs: one-year horizon, US dollars, total returns in decimals; funds E (equity), B
    (bond) and P (property) and a risk-free rate of 3 percent. Every closed form is checked against
    an independent route (SLSQP, numerical integration, grids or the KKT conditions), and the figure
    coordinates of mean-sd-frontier.tikz are recomputed. No random draws.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data and
            the figure (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, scipy)
    history = AssetClassHistory.read(root / DATA)
    figure = (root / FIGURE).read_text(encoding="utf-8")
    report = CheckReport()
    check_history(report, history)
    check_risk_aversion(report)
    f = funds()
    check_frontier(report, f)
    sharpe, pos4 = check_capital_allocation(report, f)
    check_figure(report, f, figure, sharpe, pos4)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
