"""Splitting an order across venues of random depth: calibration, a learner and the optimum."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


def project_simplex(v: Floats) -> Floats:
    """Return the Euclidean projection of v onto the probability simplex."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    value: Floats = np.maximum(v - (css[rho] - 1) / (rho + 1), 0)
    return value


class VenueDepths(Record):
    """Depths D_k = mu_k X_k with log-normal X_k of mean 1, independent of the order size V.

    The router's keys r (on the simplex) send r_k V to venue k and capture
    E[sum_k min(r_k V, D_k)]; the order size is log-normal around sum mu.

    Attributes:
        venues: How many venues.
        spread: nu, the log-normal spread of the depths.
    """

    venues: int
    spread: float

    def draw(self, rng: np.random.Generator, mu: Floats, size: int) -> Floats:
        """Return size draws of the venue depths with means mu (sd proportional to the mean)."""
        nu = self.spread
        value: Floats = mu * np.exp(rng.normal(-(nu**2) / 2, nu, (size, self.venues)))
        return value

    def calibrate(
        self, rng: np.random.Generator, p_target: Floats, iters: int = 60, size: int = 40_000
    ) -> tuple[Floats, Floats]:
        """Return the venue means giving target shares E[D_k / sum D], and the shares achieved."""
        nu = self.spread
        mu = p_target.copy()
        Z = rng.normal(-(nu**2) / 2, nu, (size, self.venues))
        D: Floats = mu * np.exp(Z)
        for _ in range(iters):
            D = mu * np.exp(Z)
            share = (D / D.sum(1, keepdims=True)).mean(0)
            mu = mu * p_target / share
            mu = mu / mu.sum()
        achieved: Floats = (D / D.sum(1, keepdims=True)).mean(0)
        return mu, achieved

    def learn(
        self,
        rng: np.random.Generator,
        r: Floats,
        mu: Floats,
        n_draws: int,
        gamma0: float = 0.02,
        tau: int = 300,
    ) -> tuple[Floats, Floats]:
        """Return the last and the average keys of projected stochastic gradient ascent.

        The objective is the expected capture, with decreasing steps gamma0 / (1 + i / tau);
        the average key is over the second half of the draws.
        """
        D = self.draw(rng, mu, n_draws)
        V = np.exp(rng.normal(-0.02, 0.2, n_draws)) * mu.sum()  # independent of D, E[V] ~ sum E[D]
        acc = np.zeros(self.venues)
        for i, (d, v) in enumerate(zip(D, V, strict=True)):
            g = v * (r * v < d) / mu.sum()  # stochastic gradient, scaled by order size
            r = project_simplex(r + gamma0 / (1 + i / tau) * (g - g.mean()))
            if i >= n_draws // 2:
                acc += r
        return r, acc / (n_draws - n_draws // 2)

    def optimum(
        self, rng: np.random.Generator, mu: Floats, n: int = 100_000
    ) -> tuple[Floats, Floats, float, float]:
        """Return the exact KKT solution on a sample: keys, marginal values, capture, multiplier.

        Each r_k solves h_k(r_k) = E[V 1{r_k V < D_k}] = lam (h_k decreasing in r_k), r_k = 0
        if h_k(0) <= lam, and lam is set by bisection so that the keys sum to one.
        """
        D = self.draw(rng, mu, n)
        V = np.exp(rng.normal(-0.02, 0.2, n)) * mu.sum()
        ratio = D / V[:, None]  # r_k V < D_k  <=>  r_k < D_k / V

        def key(k: int, lam: float) -> float:
            """Return the key of venue k at multiplier lam: first breakpoint with h_k at lam."""
            order = np.argsort(ratio[:, k])
            rk = ratio[order, k]
            vk = V[order]
            tail = np.cumsum(vk[::-1])[::-1] / n  # h_k just below each breakpoint
            idx = np.searchsorted(-tail, -lam, side="right")  # first breakpoint where h_k <= lam
            return 0.0 if idx == 0 else rk[min(int(idx), n) - 1]

        lo, hi = 0.0, V.mean()
        lam = 0.0
        for _ in range(80):
            lam = (lo + hi) / 2
            tot = sum(key(k, lam) for k in range(self.venues))
            lo, hi = (lam, hi) if tot > 1 else (lo, lam)
        r = np.array([key(k, lam) for k in range(self.venues)])
        r = r / r.sum()
        g = (V[:, None] * (r * V[:, None] < D)).mean(0)
        capture: float = np.minimum(r * V[:, None], D).sum(1).mean()
        return r, g, capture, lam
