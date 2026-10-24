"""Mean-CVaR optimisation: Rockafellar and Uryasev's benchmark, the LP and normal equivalence."""

import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import optimize, stats

from trading_notes.numerical.portfolio_construction_models.mean_cvar import (
    MeanCVaRProblem,
    empirical_cvar,
    normal_cvar_multiple,
    normal_scenarios,
    normal_var_multiple,
)
from trading_notes.numerical.report import CheckReport, print_versions

type Floats = NDArray[np.float64]

MU: Final = (0.04, 0.06, 0.08)  # expected returns of the synthetic world
TARGET: Final = 0.06  # the target expected return, in the synthetic world
ALPHA: Final = 0.95  # the CVaR confidence level


def cvar_weights(R: Floats) -> Floats:
    """Return the minimum-CVaR weights of the scenarios R at the synthetic world's target and 95%.

    The slow step of part 3 and a pure function of R, so a test may answer a repeat from an
    earlier solve.
    """
    return MeanCVaRProblem(mu=np.array(MU), target=TARGET, alpha=ALPHA).solve(R).weights


def check_benchmark(report: CheckReport) -> None:
    """Check Rockafellar and Uryasev's minimum-variance benchmark (Tables 1-4).

    Args:
        report: The run's report.
    """
    print("== Part 1: Rockafellar and Uryasev's minimum-variance benchmark (Tables 1-4)")
    m_ru = np.array([0.0101110, 0.0043532, 0.0137058])
    V_ru = np.array(
        [
            [0.00324625, 0.00022983, 0.00420395],
            [0.00022983, 0.00049937, 0.00019247],
            [0.00420395, 0.00019247, 0.00764097],
        ]
    )
    # minimum variance with x >= 0, sum x = 1, m'x = 0.011 (the constraint is active): solve the KKT
    # system
    K = np.block(
        [
            [2 * V_ru, np.ones((3, 1)), m_ru[:, None]],
            [np.ones((1, 3)), np.zeros((1, 2))],
            [m_ru[None, :], np.zeros((1, 2))],
        ]
    )
    x_ru = np.linalg.solve(K, np.concatenate([np.zeros(3), [1.0, 0.011]]))[:3]
    var_ru = float(x_ru @ V_ru @ x_ru)
    # The printed weights are a numerical QP solution: they miss the return constraint by about
    # 4e-9 (mean 0.0109999956), which moves two weights by 2e-6, hence the 5e-6 tolerance.
    x_print = np.array([0.452013, 0.115573, 0.432414])
    report.ok(
        "Table 3: exact weights within 5e-6 of the printed 0.452013, 0.115573, 0.432414 (all"
        " positive); variance 0.00378529",
        bool(np.all(np.abs(x_ru - x_print) < 5e-6))
        and abs(var_ru - 0.00378529) < 5e-9
        and bool(np.all(x_ru > 0)),
        ", ".join(f"{v:.7f}" for v in x_ru)
        + f"; {var_ru:.8f}; printed weights' mean return {x_print @ m_ru:.10f} against the target"
        " 0.011",
    )
    tab4 = {0.90: (0.067847, 0.096975), 0.95: (0.090200, 0.115908), 0.99: (0.132128, 0.152977)}
    got = {
        b: (
            -0.011 + normal_var_multiple(b) * math.sqrt(var_ru),
            -0.011 + normal_cvar_multiple(b) * math.sqrt(var_ru),
        )
        for b in tab4
    }
    report.ok(
        "Table 4: VaR and CVaR at 90, 95 and 99% from eqs. (18)-(19)",
        all(abs(got[b][0] - v[0]) < 5e-6 and abs(got[b][1] - v[1]) < 5e-6 for b, v in tab4.items()),
        "; ".join(f"{got[b][0]:.6f}, {got[b][1]:.6f}" for b in tab4),
    )
    report.ok(
        "eq. (19) is the normal ES phi(z)/(1 - beta) of meth:var-es-estimation-methods",
        all(
            abs(normal_cvar_multiple(b) - stats.norm.pdf(stats.norm.ppf(b)) / (1 - b)) < 1e-12
            for b in tab4
        ),
    )


def check_lp(report: CheckReport, mu: Floats, Sigma: Floats, target: float, alpha: float) -> None:
    """Check the LP against the fractional-tail-mass CVaR, and a grid search.

    Args:
        report: The run's report.
        mu: The expected returns of the three assets.
        Sigma: The covariance matrix of the three assets.
        target: The target expected return.
        alpha: The CVaR confidence level.
    """
    print("== Part 2: the LP against the fractional-tail-mass CVaR, and a grid search")
    R10 = normal_scenarios(10_000, 0, mu, Sigma)
    sol10 = MeanCVaRProblem(mu=mu, target=target, alpha=alpha).solve(R10)
    w10, obj10 = sol10.weights, sol10.cvar
    cv10 = empirical_cvar(-(R10 @ w10), alpha)
    report.ok(
        "n = 10,000 at 95% (tail mass 500): LP objective equals the empirical CVaR of its weights"
        " to"
        " 1e-8",
        abs(obj10 - cv10) < 1e-8,
        f"{obj10:.10f}",
    )
    R250 = normal_scenarios(250, 20261111, mu, Sigma)
    sol250 = MeanCVaRProblem(mu=mu, target=target, alpha=0.975).solve(R250)
    w250, obj250 = sol250.weights, sol250.cvar
    cv250 = empirical_cvar(-(R250 @ w250), 0.975)
    report.ok(
        "n = 250 at 97.5% (tail mass 6.25): LP objective equals the fractional-tail-mass CVaR to"
        " 1e-8",
        abs(obj250 - cv250) < 1e-8,
        f"{obj250:.10f}",
    )
    # on the feasible set w1 = w3 = a, w2 = 1 - 2a (mu = 4, 6, 8 with target 6)
    grid = np.round(np.arange(0, 0.5001, 0.01), 10)
    cvs = np.array([empirical_cvar(-(R10 @ np.array([a, 1 - 2 * a, a])), alpha) for a in grid])
    lip = float(np.max(np.abs(R10[:, 0] - 2 * R10[:, 1] + R10[:, 2])))
    report.ok(
        "1% grid on the feasible line: no grid portfolio beats the LP, and the best is within the"
        " grid-step allowance",
        bool(np.all(cvs >= obj10 - 1e-9)) and cvs.min() - obj10 <= lip * 0.005,
        f"LP {obj10:.6f} at w = ({w10[0]:.4f}, {w10[1]:.4f}, {w10[2]:.4f}); grid best"
        f" {cvs.min():.6f} at a = {grid[cvs.argmin()]:.2f}; allowance {lip * 0.005:.6f}",
    )


def check_mean_variance(report: CheckReport, mu: Floats, Sigma: Floats) -> None:
    """Check normal equivalence with mean-variance at an equal expected return.

    Args:
        report: The run's report.
        mu: The expected returns of the three assets.
        Sigma: The covariance matrix of the three assets.
    """
    print("== Part 3: normal equivalence with mean-variance at an equal expected return")
    a_grid = optimize.minimize_scalar(
        lambda a: np.array([a, 1 - 2 * a, a]) @ Sigma @ np.array([a, 1 - 2 * a, a]),
        bounds=(0, 0.5),
        method="bounded",
        options={"xatol": 1e-12},
    )
    w_mv = np.array([a_grid.x, 1 - 2 * a_grid.x, a_grid.x])
    print(f"  population mean-variance weights: {w_mv[0]:.6f}, {w_mv[1]:.6f}, {w_mv[2]:.6f}")
    diffs: dict[int, list[float]] = {10_000: [], 100_000: []}
    for n in diffs:
        for seed in range(10):
            w = cvar_weights(normal_scenarios(n, seed, mu, Sigma))
            diffs[n].append(float(np.max(np.abs(w - w_mv))))
    print(
        "  largest |w - w_mv| by seed, n = 10,000: " + ", ".join(f"{d:.4f}" for d in diffs[10_000])
    )
    print(
        "  largest |w - w_mv| by seed, n = 100,000: "
        + ", ".join(f"{d:.4f}" for d in diffs[100_000])
    )
    report.ok(
        "at 100,000 scenarios the largest weight difference over seeds 0-9 is at most 0.025",
        max(diffs[100_000]) <= 0.025,
        f"{max(diffs[100_000]):.4f}",
    )
    report.ok(
        "its mean over the seeds is lower at 100,000 than at 10,000 scenarios",
        bool(np.mean(diffs[100_000]) < np.mean(diffs[10_000])),
        f"{np.mean(diffs[10_000]):.4f} against {np.mean(diffs[100_000]):.4f}",
    )


def report_skewed_case(mu: Floats, vol: Floats, corr: Floats, target: float, alpha: float) -> None:
    """Report, without checking, asset 3 with a negatively skewed return and equal moments.

    Args:
        mu: The expected returns of the three assets.
        vol: The volatilities of the three assets.
        corr: The correlation matrix of the three assets.
        target: The target expected return.
        alpha: The CVaR confidence level.
    """
    print(
        "== Part 4 (reported): asset 3 given a negatively skewed return with the same mean and"
        " variance"
    )
    rng = np.random.default_rng(20261112)
    n = 100_000
    G = rng.multivariate_normal(np.zeros(3), corr, size=n)
    s = 0.8
    raw = -np.exp(s * G[:, 2])  # negatively skewed, increasing in -G
    z3 = (raw - raw.mean()) / raw.std()
    Rs = np.column_stack([mu[0] + vol[0] * G[:, 0], mu[1] + vol[1] * G[:, 1], mu[2] + vol[2] * z3])
    Rs = Rs - Rs.mean(axis=0) + mu
    skew = float(stats.skew(Rs[:, 2]))
    Sig_s = np.cov(Rs.T)
    a_s = optimize.minimize_scalar(
        lambda a: np.array([a, 1 - 2 * a, a]) @ Sig_s @ np.array([a, 1 - 2 * a, a]),
        bounds=(0, 0.5),
        method="bounded",
        options={"xatol": 1e-12},
    ).x
    sol_s = MeanCVaRProblem(mu=mu, target=target, alpha=alpha).solve(Rs)
    w_cv, obj_s = sol_s.weights, sol_s.cvar
    cv_mv = empirical_cvar(-(Rs @ np.array([a_s, 1 - 2 * a_s, a_s])), alpha)
    print(
        f"  skewness of asset 3: {skew:.2f}; sample mean-variance weights ({a_s:.4f},"
        f" {1 - 2 * a_s:.4f}, {a_s:.4f}), CVaR {cv_mv:.5f}; mean-CVaR weights ({w_cv[0]:.4f},"
        f" {w_cv[1]:.4f}, {w_cv[2]:.4f}), CVaR {obj_s:.5f}"
    )
    print(
        "  with the return constraint w1 = w3, a change in asset 3's weight moves asset 1 by the"
        " same"
        " amount and asset 2 by twice as much the other way; the direction is a result, not a rule"
    )


def main() -> int:
    """Run the four parts with one report.

    Synthetic three-asset world: mu = (4, 6, 8) percent, volatilities (10, 15, 20) percent, all
    correlations 0.3, target 6 percent, CVaR at 95 percent. Scenarios are jointly normal with the
    sample mean shifted to mu exactly; each set has its own seed (0-9 for the normal equivalence,
    20261111 for n = 250, 20261112 for the skewed case). Part 3's LPs on 100,000 scenarios take
    nearly all of the run's two minutes.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    mu = np.array(MU)
    vol = np.array([0.10, 0.15, 0.20])
    corr = np.full((3, 3), 0.3) + 0.7 * np.eye(3)
    Sigma = np.outer(vol, vol) * corr
    report = CheckReport()
    check_benchmark(report)
    check_lp(report, mu, Sigma, TARGET, ALPHA)
    check_mean_variance(report, mu, Sigma)
    report_skewed_case(mu, vol, corr, TARGET, ALPHA)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
