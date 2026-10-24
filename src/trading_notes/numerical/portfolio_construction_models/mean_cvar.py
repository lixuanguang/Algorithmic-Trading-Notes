"""Minimum-CVaR portfolios by Rockafellar and Uryasev's linear programme on return scenarios."""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import optimize, sparse, special

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def empirical_cvar(losses: Floats, alpha: float) -> float:
    """Return the average of the worst n(1 - alpha) losses, the last one fractionally weighted.

    A whole or fractional part within 1e-12 of an integer is treated as that integer.
    """
    srt = np.sort(losses)[::-1]
    m = len(losses) * (1 - alpha)
    whole = math.floor(m + 1e-12)
    frac = m - whole
    cvar: float = (srt[:whole].sum() + (frac * srt[whole] if frac > 1e-12 else 0.0)) / m
    return cvar


class CVaRSolution(Record):
    """An optimum of the mean-CVaR programme.

    Attributes:
        weights: Portfolio weights, one per asset.
        cvar: The minimised CVaR of the portfolio loss.
        zeta: The optimal auxiliary variable, a VaR of the loss.
    """

    weights: Floats
    cvar: float
    zeta: float


class MeanCVaRProblem(Record):
    """Minimise the CVaR of the loss L = -R'w, long only, fully invested, at a target mean.

    Attributes:
        mu: Expected returns, one per asset; the constraint is mu'w = target.
        target: The target expected return.
        alpha: The CVaR confidence level.
    """

    mu: Floats
    target: float
    alpha: float

    def solve(self, R: Floats) -> CVaRSolution:
        """Solve the programme on equally weighted scenarios R, n x d, with HiGHS.

        The variables are (w_1..w_d, zeta, u_1..u_n), minimising
        zeta + sum_k u_k / (n (1 - alpha)) subject to u_k >= -R_k'w - zeta and u >= 0.

        Raises:
            AssertionError: If the solver does not report an optimum.
        """
        n, d = R.shape
        c = np.concatenate([np.zeros(d), [1.0], np.full(n, 1 / (n * (1 - self.alpha)))])
        # u_k >= -R_k'w - zeta  <=>  -R_k'w - zeta - u_k <= 0
        A_ub = sparse.hstack(
            [
                sparse.csr_matrix(-R),
                sparse.csr_matrix(-np.ones((n, 1))),
                -sparse.identity(n, format="csr"),
            ],
            format="csr",
        )
        A_eq = np.zeros((2, d + 1 + n))
        A_eq[0, :d] = 1.0
        A_eq[1, :d] = self.mu
        bounds = [(0, None)] * d + [(None, None)] + [(0, None)] * n
        res = optimize.linprog(
            c,
            A_ub=A_ub,
            b_ub=np.zeros(n),
            A_eq=A_eq,
            b_eq=[1.0, self.target],
            bounds=bounds,
            # interior point with crossover: same vertex, about three times faster here
            method="highs-ipm",
        )
        assert res.status == 0, res.message
        assert res.x is not None and res.fun is not None
        return CVaRSolution(weights=res.x[:d], cvar=res.fun, zeta=np.float64(res.x[d]))


def normal_scenarios(n: int, seed: int, mu: Floats, Sigma: Floats) -> Floats:
    """Return n jointly normal scenarios drawn with the given seed, with mean exactly mu."""
    R = np.random.default_rng(seed).multivariate_normal(mu, Sigma, size=n)
    shifted: Floats = R - R.mean(axis=0) + mu
    return shifted


def normal_var_multiple(b: float) -> float:
    """Return the normal VaR at confidence b in standard deviations (Rockafellar-Uryasev eq. 18)."""
    return math.sqrt(2) * special.erfinv(2 * b - 1)


def normal_cvar_multiple(b: float) -> float:
    """Return the normal CVaR at confidence b in standard deviations (eq. 19)."""
    return 1 / (math.sqrt(2 * math.pi) * math.exp(special.erfinv(2 * b - 1) ** 2) * (1 - b))
