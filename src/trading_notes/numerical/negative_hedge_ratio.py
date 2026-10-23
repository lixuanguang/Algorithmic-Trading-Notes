"""A negative minimum-variance hedge ratio reduces variance.

Financial data and labels review follow-up check (2026-10-16), behind
mod:minimum-variance-hedge-ratio. Position convention as there: hedged change
V(h) = dS - h dF, so h > 0 is a short futures position against a long exposure and h < 0 a long
one. The analytical variance, the covariance-over-variance estimate and an empirical grid search
are three separate calculations.

This is a demonstration, not a checker: it prints its values for comparison by eye, asserts
nothing and exits 0.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.negative_hedge_ratio
(numpy).
"""

# standard library imports
import sys
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

SIGMA_S: Final = 1.0  # spot volatility
SIGMA_F: Final = 1.0  # futures volatility
RHO: Final = -0.6  # spot-futures correlation
DRAWS: Final = 200_000
SEED: Final = 7


def analytic_variance(h: float) -> float:
    """Return Var(dS - h dF) = sS^2 - 2 h rho sS sF + h^2 sF^2 from the stated moments."""
    return SIGMA_S**2 - 2 * h * RHO * SIGMA_S * SIGMA_F + h**2 * SIGMA_F**2


def simulated_changes(
    rng: np.random.Generator,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return DRAWS correlated spot and futures changes (dS, dF), each of length DRAWS.

    Two standard normal vectors are drawn in turn, the first driving dF.
    """
    z1, z2 = rng.standard_normal(DRAWS), rng.standard_normal(DRAWS)
    dF = SIGMA_F * z1
    dS = SIGMA_S * (RHO * z1 + np.sqrt(1 - RHO**2) * z2)
    return dS, dF


def cov_var_ratio(dS: NDArray[np.float64], dF: NDArray[np.float64]) -> float:
    """Return Cov(dS, dF) / Var(dF), np.cov's default (ddof 1) over Var with ddof 1."""
    return float(np.cov(dS, dF)[0, 1] / dF.var(ddof=1))


def grid_minimiser(dS: NDArray[np.float64], dF: NDArray[np.float64]) -> float:
    """Return the h of 3001 points in [-1.5, 1.5] with the least sample Var(dS - h dF).

    The variance is np.var's default (ddof 0); no closed form is used.
    """
    grid = np.linspace(-1.5, 1.5, 3001)
    return float(grid[np.argmin([np.var(dS - h * dF) for h in grid])])


def main() -> int:
    """Print the demonstration and return the exit status, always 0."""
    hstar = RHO * SIGMA_S / SIGMA_F
    print(
        "analytic: h* =",
        hstar,
        " Var(h*) =",
        analytic_variance(hstar),
        " Var(0) =",
        analytic_variance(0.0),
        " Var(+0.6) =",
        analytic_variance(0.6),
    )
    dS, dF = simulated_changes(np.random.default_rng(SEED))
    h_ols = cov_var_ratio(dS, dF)
    h_grid = grid_minimiser(dS, dF)
    print(f"simulated: Cov/Var = {h_ols:.4f}, grid minimiser = {h_grid:.4f}")
    for h in [0.0, h_ols, -h_ols]:
        print(f"  h = {h:+.4f}: Var(dS - h dF) = {np.var(dS - h * dF):.4f}")
    print(
        "a long futures position (h < 0) against a long exposure removes",
        f"{1 - np.var(dS - h_ols * dF) / np.var(dS):.3f}",
        "of the variance (rho^2 =",
        RHO**2,
        "); the same size short adds variance",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
