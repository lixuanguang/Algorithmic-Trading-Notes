"""Best linear projection against conditional expectation, behind meth:forecast-scaling-ic.

Source verification (2026-10-17) (audit repair).

1. Zero linear IC with full predictive information: g ~ N(0, 1), r = g^2 - 1 + e with
   e ~ N(0, s^2) independent. Cov(r, g) = E[g^3] = 0, so the IC and the linear refined forecast
   are zero, yet E[r | g] = g^2 - 1 explains a fraction 2 / (2 + s^2) of Var(r). Checked in
   closed form and by simulation.
2. The linear projection's error is uncorrelated with g (orthogonality) but not mean-independent
   of g: in the same example E[error | g] = g^2 - 1, so a nonlinear function of g still predicts
   the error.
3. Under joint normality the projection and the conditional mean coincide: binned conditional
   means of r given g lie on the projection line (within simulation error).
Run: uv run --frozen --no-editable python -m trading_notes.numerical.linear_projection
(numpy; under 1 s). Exits non-zero on failure.
"""

import itertools
import sys
from dataclasses import dataclass
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.report import CheckReport

SEED: Final = 17102026
N: Final = 2_000_000  # observations in each simulated sample
S: Final = 1.0  # standard deviation of the noise e
RHO: Final = 0.3  # correlation of the joint-normal pair, and so its projection slope


@dataclass(frozen=True)
class NonlinearSample:
    """The zero-IC example: a signal and a return that depends on it only through g^2.

    Attributes:
        g: The signal, N draws of N(0, 1).
        r: The return g^2 - 1 + S e, with e independent N(0, 1) draws.
    """

    g: NDArray[np.float64]
    r: NDArray[np.float64]


def simulate_nonlinear(rng: np.random.Generator) -> NonlinearSample:
    """Draw all N signals, then all N noise terms, and form the returns."""
    g = rng.standard_normal(N)
    # The data-generating model, written out; conditional_mean is the claim checked against it.
    r = g**2 - 1 + S * rng.standard_normal(N)
    return NonlinearSample(g, r)


def conditional_mean(g: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return E[r | g] = g^2 - 1 for the zero-IC example."""
    return g**2 - 1


def explained_share(s: float) -> float:
    """Return the share of Var(r) explained by E[r | g]: Var(g^2) / (Var(g^2) + s^2).

    For g ~ N(0, 1), Var(g^2) = 2, so the share is 2 / (2 + s^2), independent of simulation.
    """
    return 2 / (2 + s**2)


def correlation(x: NDArray[np.float64], y: NDArray[np.float64]) -> float:
    """Return the sample correlation of x and y."""
    return float(np.corrcoef(x, y)[0, 1])


def projection_slope(sample: NonlinearSample) -> float:
    """Return the linear projection slope Cov(r, g) / Var(g).

    The covariance is np.cov's (divisor N - 1) and the variance np.var's (divisor N), as in
    the original check; at N = 2,000,000 the mismatch changes the slope by a factor 1 + 5e-7.
    """
    return float(np.cov(sample.r, sample.g)[0, 1] / np.var(sample.g))


def check_zero_ic(report: CheckReport, sample: NonlinearSample) -> float:
    """1. The IC is zero, yet E[r | g] explains 2 / (2 + s^2) of the variance.

    Returns:
        The linear projection slope, used by the orthogonality checks.
    """
    ic = correlation(sample.r, sample.g)
    r2_true = explained_share(S)
    r2_sim = float(1 - np.var(sample.r - conditional_mean(sample.g)) / np.var(sample.r))
    print("== 1. Zero IC, nonzero information")
    report.ok("IC is zero within simulation error", abs(ic) < 4 / np.sqrt(N), f"IC {ic:+.5f}")
    report.ok(
        "conditional mean explains 2/(2+s^2) of the variance",
        abs(r2_sim - r2_true) < 0.005,
        f"{r2_sim:.4f} against {r2_true:.4f}",
    )
    b = projection_slope(sample)
    print(f"     linear projection slope {b:+.5f}; linear R^2 {ic**2:.6f}")
    return b


def check_orthogonality(report: CheckReport, sample: NonlinearSample, b: float) -> None:
    """2. The projection error is uncorrelated with g but correlated with g^2."""
    g, r = sample.g, sample.r
    u = r - (r.mean() + b * (g - g.mean()))
    print("\n== 2. Orthogonality is not mean independence")
    with_g = correlation(u, g)
    report.ok(
        "projection error uncorrelated with g", abs(with_g) < 4 / np.sqrt(N), f"{with_g:+.5f}"
    )
    with_g2 = correlation(u, g**2)
    report.ok("projection error correlated with g^2", with_g2 > 0.5, f"{with_g2:+.4f}")


def largest_bin_gap(g: NDArray[np.float64], r: NDArray[np.float64]) -> float:
    """Return the largest |mean(r) - RHO mean(g)| over eight bins of g of width 0.5.

    Each bin [lo, hi) includes its lower edge and excludes its upper one; observations below
    -2 or at or above 2 fall in no bin.
    """
    worst = 0.0
    for lo, hi in itertools.pairwise(np.linspace(-2, 2, 9)):
        m = (g >= lo) & (g < hi)
        worst = max(worst, float(abs(r[m].mean() - RHO * g[m].mean())))
    return worst


def check_joint_normality(report: CheckReport, rng: np.random.Generator) -> None:
    """3. Under joint normality the binned conditional means lie on the line RHO g."""
    print("\n== 3. Joint normality: projection = conditional mean")
    cov = np.array([[1.0, RHO], [RHO, 1.0]])
    x: NDArray[np.float64] = rng.multivariate_normal([0, 0], cov, size=N)
    worst = largest_bin_gap(x[:, 0], x[:, 1])
    report.ok(
        "binned conditional means on the line 0.3 g", worst < 0.01, f"largest gap {worst:.4f}"
    )


def main() -> int:
    """Run the three parts on one generator, the joint-normal sample drawn last.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    sample = simulate_nonlinear(rng)
    b = check_zero_ic(report, sample)
    check_orthogonality(report, sample, b)
    check_joint_normality(report, rng)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
