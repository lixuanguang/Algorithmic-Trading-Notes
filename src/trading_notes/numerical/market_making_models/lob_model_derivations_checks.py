"""Closed forms of four market-making models against root-finding, grids and simulation."""

import sys
from typing import Final

import numpy as np
from scipy import optimize

from trading_notes.numerical.market_making_models.microstructure_models import (
    GrossmanMillerFees,
    KyleAuction,
    RollModel,
)

GROSSMAN_MILLER: Final = GrossmanMillerFees(
    mu=10.0, gamma=2.0, variance=0.04, market_makers=5, imbalance=3.0, fee=0.01
)


def check(failures: list[str], name: str, ok: bool, detail: str) -> None:
    """Print `ok   <name>: <detail>` or `FAIL <name>: <detail>`, and record a failure."""
    print(("ok   " if ok else "FAIL ") + name + ": " + detail)
    if not ok:
        failures.append(name)


def check_fee_equilibrium(failures: list[str]) -> None:
    """1. The fee equilibrium's price and LT1 demand by brentq against the closed forms.

    For i > 0 LT1's fee cancels, q1_LT1 = (mu - S1)/(gamma sigma^2), while a market maker pays
    a round trip, q1_MM = (mu - S1 - 2 eta)/(gamma sigma^2); clearing i = n q1_MM + q1_LT1
    (model-derivations.tex, "Per-share fees").
    """
    gm = GROSSMAN_MILLER
    mu, g, s2 = gm.mu, gm.gamma, gm.variance
    P1_closed, q_lt_closed = gm.price(), gm.trader_demand()
    P1_root = optimize.brentq(gm.excess_demand, mu - 10, mu + 10, xtol=1e-14)
    q_lt_root = (mu - P1_root) / (g * s2)
    check(
        failures,
        "GM fee price",
        abs(P1_root - P1_closed) < 1e-9 and abs(P1_root - 9.943333333333333) < 1e-9,
        f"P1 root {P1_root:.9f}, closed {P1_closed:.9f}",
    )
    check(
        failures,
        "GM fee LT demand",
        abs(q_lt_root - q_lt_closed) < 1e-9 and abs(q_lt_root - 0.708333333333333) < 1e-9,
        f"q_LT1 root {q_lt_root:.9f}, closed {q_lt_closed:.9f}",
    )


def check_liquidity(failures: list[str], rng: np.random.Generator) -> None:
    """2. P1 - mu = lambda Q with lambda = -g s2 / n; dP2 = noise - lambda Q."""
    lam = GROSSMAN_MILLER.liquidity()
    check(failures, "GM lambda", abs(lam + 0.016) < 1e-15, f"lambda {lam}")
    N = 400_000
    Q = rng.normal(0.0, 1.0, N)
    e1 = rng.normal(0.0, 0.1, N)
    e2 = rng.normal(0.0, 0.1, N)
    dP1 = e1 + lam * Q
    dP2 = e2 - lam * Q
    cov = np.cov(dP1, dP2)[0, 1]
    check(
        failures,
        "GM autocovariance",
        abs(cov - (-(lam**2))) < 3e-5,
        f"simulated {cov:.6f}, closed {-(lam**2):.6f}",
    )


def check_kyle(failures: list[str], rng: np.random.Generator) -> None:
    """3. Kyle's single auction: lambda, the projection slope, profit and posterior variance."""
    kyle = KyleAuction(sigma_v=2.0, sigma_u=3.0, mean=1.0)
    sv, su, m = kyle.sigma_v, kyle.sigma_u, kyle.mean
    beta, lk = kyle.beta, kyle.price_impact
    N = 1_000_000
    v = m + rng.normal(0.0, sv, N)
    u = rng.normal(0.0, su, N)
    x = beta * (v - m)
    y = x + u
    p = m + lk * y
    profit = np.mean(x * (v - p))
    slope = np.cov(v, y)[0, 1] / np.var(y, ddof=1)
    resid_var = np.var(v - (m + slope * y))
    check(failures, "Kyle lambda", abs(lk - 1 / 3) < 1e-15, f"lambda {lk:.6f}")
    check(failures, "Kyle projection", abs(slope - lk) < 0.005, f"regression slope {slope:.5f}")
    check(
        failures,
        "Kyle profit",
        bool(abs(profit / kyle.expected_profit - 1) < 0.01),
        f"simulated {profit:.4f}, closed {kyle.expected_profit}",
    )
    check(
        failures,
        "Kyle posterior variance",
        abs(resid_var / kyle.posterior_variance - 1) < 0.01,
        f"simulated {resid_var:.4f}, closed {kyle.posterior_variance}",
    )


def check_limit_order_depth(failures: list[str]) -> None:
    """4. The grid argmax of delta exp(-kappa delta) and the second-order condition."""
    k = 4.0
    grid = np.linspace(0.0, 2.0, 200_001)
    arg = grid[np.argmax(grid * np.exp(-k * grid))]
    # (k^2 delta - 2k) e^{-k delta} at delta = 1/k, i.e. -k/e
    soc = (k**2 * (1 / k) - 2 * k) * np.exp(-1.0)
    check(
        failures,
        "limit-order argmax",
        abs(arg - 1 / k) < 1e-5 and soc < 0,
        f"grid argmax {arg:.6f}, SOC {soc:.4f}",
    )


def check_roll(failures: list[str], rng: np.random.Generator) -> None:
    """5. Roll's variance and autocovariances of price changes, by simulation."""
    roll = RollModel(spread=0.2, sigma=0.1)
    S, sig = roll.spread, roll.sigma
    N = 1_000_000
    eps = rng.normal(0.0, sig, N)
    Qs = rng.choice([-1.0, 1.0], N)
    V = np.cumsum(eps)
    P = V + 0.5 * S * Qs
    dP = np.diff(P)
    var = np.var(dP)
    c1 = np.cov(dP[1:], dP[:-1])[0, 1]
    c2 = np.cov(dP[2:], dP[:-2])[0, 1]
    check(
        failures,
        "Roll variance",
        bool(abs(var - roll.price_change_variance()) < 5e-4),
        f"simulated {var:.5f}, closed {roll.price_change_variance()}",
    )
    check(
        failures,
        "Roll autocovariance",
        abs(c1 - roll.first_autocovariance()) < 5e-4 and abs(c2) < 5e-4,
        f"lag 1 {c1:.5f} (closed {roll.first_autocovariance()}), lag 2 {c2:.5f}",
    )


def main() -> int:
    """Run the five parts, each simulation with its own seeded generator.

    The derivations are in notes/artefacts/market-making-lob/model-derivations.tex.

    1. Grossman-Miller with per-share fees: the date-1 price and LT1's date-1 holding solved by
       root-finding (brentq, xtol 1e-14) against the closed forms (mu=10, gamma=2, sigma^2=0.04,
       n=5 market makers, imbalance i=3, fee eta=0.01); tolerance 1e-9.
    2. Grossman-Miller liquidity measures: lambda = -gamma sigma^2 / n = -0.016, and
       Cov(Delta1, Delta2) = -lambda^2 Var(Q) by simulation (seed 1, N=400,000, Q ~ N(0,1), news
       eps1, eps2 ~ N(0, 0.1^2)); tolerance 3e-5.
    3. Kyle single auction (sigma_v=2, sigma_u=3, m=1): beta = sigma_u/sigma_v,
       lambda = sigma_v/(2 sigma_u) = 1/3, expected profit sigma_v sigma_u / 2 = 3 and
       Var(v|y) = sigma_v^2/2 = 2, by simulation (seed 2, N=1,000,000); relative tolerance 1
       percent; the projection slope by regression, tolerance 0.005.
    4. Static limit-order depth: delta* = 1/kappa maximises delta exp(-kappa delta); grid of 200,001
       points on [0, 2] with kappa=4 gives 0.25, tolerance 1e-5; second-order condition negative.
    5. Roll: Var(dP) = sigma^2 + S^2/2 and Cov(dP_t, dP_{t-1}) = -S^2/4 (S=0.2, sigma=0.1,
       Q = +/-1), by simulation (seed 3, N=1,000,000); tolerance 5e-4; lag-2 autocovariance within
       5e-4 of zero.

    Returns:
        The exit status, 0 or 1; nothing is printed beyond the check lines.
    """
    failures: list[str] = []
    check_fee_equilibrium(failures)
    check_liquidity(failures, np.random.default_rng(1))
    check_kyle(failures, np.random.default_rng(2))
    check_limit_order_depth(failures)
    check_roll(failures, np.random.default_rng(3))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
