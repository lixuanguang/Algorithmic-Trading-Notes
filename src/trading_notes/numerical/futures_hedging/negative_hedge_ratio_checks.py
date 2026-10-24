"""A demonstration that a negative minimum-variance hedge ratio reduces variance."""

import sys
from typing import Final

import numpy as np

from trading_notes.numerical.futures_hedging.hedge_ratio import HedgeMoments

MOMENTS: Final = HedgeMoments(spot_vol=1.0, futures_vol=1.0, correlation=-0.6)
DRAWS: Final = 200_000
SEED: Final = 7


def main() -> int:
    """Print the demonstration and return the exit status, always 0.

    Behind mod:minimum-variance-hedge-ratio, with its position convention V(h) = dS - h dF.
    The analytic variance, the covariance-over-variance estimate and an empirical grid search
    are three separate calculations. A demonstration, not a checker: it prints its values for
    comparison by eye and asserts nothing.
    """
    hstar = MOMENTS.optimal_ratio()
    print(
        "analytic: h* =",
        hstar,
        " Var(h*) =",
        MOMENTS.variance(hstar),
        " Var(0) =",
        MOMENTS.variance(0.0),
        " Var(+0.6) =",
        MOMENTS.variance(0.6),
    )
    sample = MOMENTS.simulate(np.random.default_rng(SEED), DRAWS)
    h_ols = sample.cov_var_ratio()
    h_grid = sample.grid_minimiser()
    print(f"simulated: Cov/Var = {h_ols:.4f}, grid minimiser = {h_grid:.4f}")
    for h in [0.0, h_ols, -h_ols]:
        print(f"  h = {h:+.4f}: Var(dS - h dF) = {sample.variance(h):.4f}")
    print(
        "a long futures position (h < 0) against a long exposure removes",
        f"{1 - sample.variance(h_ols) / sample.variance(0.0):.3f}",
        "of the variance (rho^2 =",
        MOMENTS.correlation**2,
        "); the same size short adds variance",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
