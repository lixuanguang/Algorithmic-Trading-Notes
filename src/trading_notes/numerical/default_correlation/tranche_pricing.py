"""Tranche losses of homogeneous credit pools in the one-factor Gaussian copula."""

import itertools
import math
from typing import overload

import numpy as np
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.numerical.default_correlation.factor_model import VasicekFactorModel
from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


@overload
def tranche_payoff(loss: float, attach: float, detach: float) -> float: ...
@overload
def tranche_payoff(loss: Floats, attach: float, detach: float) -> Floats: ...
def tranche_payoff(loss: float | Floats, attach: float, detach: float) -> float | Floats:
    """Return the loss absorbed by the tranche from attach to detach, in units of pool notional.

    A scalar loss gives a float; an array gives an array of its shape.
    """
    absorbed = np.clip(loss, attach, detach) - attach
    if isinstance(loss, np.ndarray):
        return absorbed
    return float(absorbed)


def gauss_hermite(n: int) -> tuple[Floats, Floats]:
    """Return Gauss-Hermite nodes and weights for E[g(M)] with M standard normal."""
    x, w = np.polynomial.hermite_e.hermegauss(n)
    return x, w / math.sqrt(2 * math.pi)


def gauss_legendre(
    panels: int, per: int = 20, lo: float = -10.0, hi: float = 10.0
) -> tuple[Floats, Floats]:
    """Return composite Gauss-Legendre nodes and weights for E[g(M)] on [lo, hi]."""
    x, w = np.polynomial.legendre.leggauss(per)
    edges = np.linspace(lo, hi, panels + 1)
    h = np.diff(edges) / 2
    xs = (edges[:-1, None] + h[:, None] * (x[None, :] + 1)).ravel()
    ws = (h[:, None] * w[None, :]).ravel() * stats.norm.pdf(xs)
    return xs, ws


class HomogeneousPool(Record):
    """A pool of identical names over one period: one PD, one copula correlation, one LGD.

    Attributes:
        pd: Each name's default probability to the horizon.
        rho: The copula correlation.
        lgd: The loss given default, a share of each name's notional.
    """

    pd: float
    rho: float
    lgd: float

    def large_pool_loss(self, attach: float, detach: float) -> float:
        """Return E[min(max(LGD p(M) - a, 0), d - a)] for an infinitely granular pool.

        The factor line is split where the pool loss crosses each tranche boundary.
        """
        model = VasicekFactorModel(pd=self.pd, rho=self.rho)
        cuts = []
        for x in (attach, detach):
            if 0 < x / self.lgd < 1:
                g = stats.norm.ppf
                cuts.append(
                    (g(self.pd) - math.sqrt(1 - self.rho) * g(x / self.lgd)) / math.sqrt(self.rho)
                )
        edges = sorted([-40.0, 40.0, *cuts])

        def integrand(m: float) -> float:
            loss = self.lgd * model.conditional_pd(m)
            return tranche_payoff(loss, attach, detach) * stats.norm.pdf(m)

        return sum(
            integrate.quad(integrand, lo, hi, epsabs=1e-15, epsrel=1e-13, limit=400)[0]
            for lo, hi in itertools.pairwise(edges)
        )

    def finite_pool_loss(self, names: int, attach: float, detach: float, panels: int) -> float:
        """Return the exact expected tranche loss of a pool of `names` names, by quadrature."""
        x, w = gauss_legendre(panels)
        k = np.arange(names + 1)
        pay = tranche_payoff(self.lgd * k / names, attach, detach)
        p_nodes = VasicekFactorModel(pd=self.pd, rho=self.rho).conditional_pd(x)
        pmf = stats.binom.pmf(k[None, :], names, p_nodes[:, None])
        return float(w @ (pmf @ pay))

    def finite_pool_loss_converged(
        self, names: int, attach: float, detach: float
    ) -> tuple[float, int, float]:
        """Return the finite-pool loss, the nodes used and the last change.

        The panels double from 16 until the value changes by less than 1e-10, or reach 1024.
        """
        panels, prev = 16, self.finite_pool_loss(names, attach, detach, 16)
        while True:
            panels *= 2
            cur = self.finite_pool_loss(names, attach, detach, panels)
            if abs(cur - prev) < 1e-10 or panels >= 1024:
                return cur, panels * 20, abs(cur - prev)
            prev = cur


class SyntheticCdoTranche(Record):
    """A synthetic CDO tranche on a homogeneous pool, valued as in Hull (eqs. 25.1-25.12).

    Attributes:
        attach: aL, the attachment point.
        detach: aH, the detachment point.
        names: n, the names in the pool.
        recovery: R.
        rho: The copula correlation.
        hazard: lambda, the constant hazard rate.
        rate: r, the continuously compounded risk-free rate.
        maturity: T, in years.
        frequency: Payments a year.
    """

    attach: float
    detach: float
    names: int
    recovery: float
    rho: float
    hazard: float
    rate: float
    maturity: float
    frequency: int

    def legs(self, nodes: int) -> tuple[float, float, float]:
        """Return Hull's A, B and C for principal 1, integrating the factor on Hermite nodes.

        A is the premium leg per unit spread, B its accrual and C the protection leg; the
        breakeven spread is C / (A + B).
        """
        aL, aH, n, R = self.attach, self.detach, self.names, self.recovery
        rho, lam, r, T, freq = self.rho, self.hazard, self.rate, self.maturity, self.frequency
        N, G = stats.norm.cdf, stats.norm.ppf
        x, w = gauss_hermite(nodes)
        t = np.arange(1, T * freq + 1) / freq
        t0 = np.concatenate(([0.0], t))
        nL, nH = aL * n / (1 - R), aH * n / (1 - R)
        mL, mH = math.floor(nL) + 1, math.floor(nH) + 1  # smallest integer greater than x
        k = np.arange(n + 1)
        principal = np.where(
            k < mL, 1.0, np.where(k >= mH, 0.0, (aH - k * (1 - R) / n) / (aH - aL))
        )
        A = B = C = 0.0
        for f, wk in zip(x, w, strict=True):
            q = 1 - np.exp(-lam * t0)
            qf = N((G(np.maximum(q, 1e-300)) - math.sqrt(rho) * f) / math.sqrt(1 - rho))
            qf[0] = 0.0
            E = np.array([stats.binom.pmf(k, n, p) @ principal for p in qf])
            mid = 0.5 * (t0[:-1] + t0[1:])
            A += wk * np.sum(np.diff(t0) * E[1:] * np.exp(-r * t))
            B += wk * np.sum(0.5 * np.diff(t0) * (E[:-1] - E[1:]) * np.exp(-r * mid))
            C += wk * np.sum((E[:-1] - E[1:]) * np.exp(-r * mid))
        return A, B, C
