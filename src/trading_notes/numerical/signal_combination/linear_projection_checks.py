"""Best linear projection against conditional expectation for the information coefficient."""

import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.signal_combination.projection import (
    NonlinearSample,
    ZeroIcModel,
    correlation,
    largest_bin_gap,
)

SEED: Final = 17102026
N: Final = 2_000_000  # observations in each simulated sample
MODEL: Final = ZeroIcModel(noise=1.0)
RHO: Final = 0.3  # correlation of the joint-normal pair, and so its projection slope


def check_zero_ic(report: CheckReport, sample: NonlinearSample) -> float:
    """1. The IC is zero, yet E[r | g] explains 2 / (2 + s^2) of the variance.

    Returns:
        The linear projection slope, used by the orthogonality checks.
    """
    ic = correlation(sample.r, sample.g)
    r2_true = MODEL.explained_share()
    r2_sim = float(1 - np.var(sample.r - MODEL.conditional_mean(sample.g)) / np.var(sample.r))
    print("== 1. Zero IC, nonzero information")
    report.ok("IC is zero within simulation error", abs(ic) < 4 / np.sqrt(N), f"IC {ic:+.5f}")
    report.ok(
        "conditional mean explains 2/(2+s^2) of the variance",
        abs(r2_sim - r2_true) < 0.005,
        f"{r2_sim:.4f} against {r2_true:.4f}",
    )
    b = sample.projection_slope()
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


def check_joint_normality(report: CheckReport, rng: np.random.Generator) -> None:
    """3. Under joint normality the binned conditional means lie on the line RHO g."""
    print("\n== 3. Joint normality: projection = conditional mean")
    cov = np.array([[1.0, RHO], [RHO, 1.0]])
    x: NDArray[np.float64] = rng.multivariate_normal([0, 0], cov, size=N)
    worst = largest_bin_gap(x[:, 0], x[:, 1], RHO)
    report.ok(
        "binned conditional means on the line 0.3 g", worst < 0.01, f"largest gap {worst:.4f}"
    )


def main() -> int:
    """Run the three parts on one generator, the joint-normal sample drawn last.

    Behind meth:forecast-scaling-ic:

    1. Zero linear IC with full predictive information: g ~ N(0, 1), r = g^2 - 1 + e with
       e ~ N(0, s^2) independent. Cov(r, g) = E[g^3] = 0, so the IC and the linear refined
       forecast are zero, yet E[r | g] = g^2 - 1 explains a fraction 2 / (2 + s^2) of Var(r).
       Checked in closed form and by simulation.
    2. The linear projection's error is uncorrelated with g (orthogonality) but not
       mean-independent of g: in the same example E[error | g] = g^2 - 1, so a nonlinear
       function of g still predicts the error.
    3. Under joint normality the projection and the conditional mean coincide: binned
       conditional means of r given g lie on the projection line (within simulation error).

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    sample = MODEL.simulate(rng, N)
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
