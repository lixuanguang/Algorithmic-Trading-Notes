"""Delta hedging at the wrong volatility, and the vanna and volga formulas.

Library gap-filling Batch L1, package P4 (2026-10-21): the worked example of
res:delta-hedging-volatility-mismatch, and the vanna and volga formulas added to
meth:greeks-delta-gamma-hedging.

Model: dS = mu S dt + sigma S dW with mu = 10 percent and actual volatility sigma = 30 percent;
a European call (S0 = K = 100, T = 1, r = 5 percent, q = 0) bought at the BSM price with implied
volatility 20 percent and marked at that volatility; short delta shares; cash at r; no costs.
20,000 paths, rebalanced 252 or 2,520 times on common Brownian paths (the coarse grid uses
every tenth fine date). Profit is measured as present value at time 0. Acceptance ranges were
fixed before any run; seed 20261051. Synthetic data only: not evidence about markets.

Correction, 2026-10-21 (L1 audit finding L1-F2): the entry had dropped the condition Gamma >= 0
from the claim that sigma > implied volatility makes the implied-volatility hedge profitable. A
final deterministic section now shows the condition matters: a unit cash-or-nothing call
(S0 = 120, K = 100, r = 5 percent, q = 0, T = 1) is worth less at 30 than at 20 percent
volatility, and its gamma changes sign (where d1 = 0, S about 93). The vanilla simulation above
is unchanged.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.volatility_mismatch_hedging
(numpy, scipy). Exits 1 on failure. About 10 seconds.
"""

# standard library imports
import math
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

SEED: Final = 20261051
S0: Final = 100.0
K: Final = 100.0
T: Final = 1.0
R: Final = 0.05
Q: Final = 0.0
MU: Final = 0.10  # actual drift
SIG_A: Final = 0.30  # actual volatility
SIG_I: Final = 0.20  # implied volatility
N_PATHS: Final = 20_000
N_FINE: Final = 2520  # fine rebalancing dates; the coarse grid uses every tenth
COARSE_EVERY: Final = 10


def d12[X: (float, Floats)](S: X, tau: float, vol: float) -> tuple[X, X]:
    """Return BSM's d1 and d2 for the call, at a price or an array of prices."""
    d1: X = (np.log(S / K) + (R - Q + vol**2 / 2) * tau) / (vol * np.sqrt(tau))
    return d1, d1 - vol * np.sqrt(tau)


def price[X: (float, Floats)](S: X, tau: float, vol: float) -> X:
    """Return the BSM call value."""
    d1, d2 = d12(S, tau, vol)
    value: X = S * np.exp(-Q * tau) * stats.norm.cdf(d1) - K * np.exp(-R * tau) * stats.norm.cdf(d2)
    return value


def delta[X: (float, Floats)](S: X, tau: float, vol: float) -> X:
    """Return the BSM call delta."""
    value: X = np.exp(-Q * tau) * stats.norm.cdf(d12(S, tau, vol)[0])
    return value


def gamma[X: (float, Floats)](S: X, tau: float, vol: float) -> X:
    """Return the BSM gamma."""
    value: X = np.exp(-Q * tau) * stats.norm.pdf(d12(S, tau, vol)[0]) / (S * vol * np.sqrt(tau))
    return value


@dataclass
class Hedge:
    """One delta hedge's running position, rebalanced every `every` fine steps.

    Attributes:
        every: Fine steps between rebalancing dates.
        vol: The volatility the deltas are computed at.
        delta: Shares held short, one per path.
        cash: The cash account, one per path.
    """

    every: int
    vol: float
    delta: Floats
    cash: Floats


@dataclass(frozen=True)
class Simulation:
    """The hedges' discounted P&L and the implied-delta hedge's pathwise integrals.

    Attributes:
        pnl: Present value of each path's P&L, by (grid, "a" or "i" for the hedging volatility).
        integral: The left-point Riemann sum of the pathwise integral, by grid.
    """

    pnl: dict[tuple[str, str], Floats]
    integral: dict[str, Floats]


def simulate(rng: np.random.Generator, Vi: float) -> Simulation:
    """Hedge the call bought at Vi on common paths: both grids, both hedging volatilities.

    One normal vector per fine step drives every hedge, so the four share their paths.
    """
    dt = T / N_FINE
    S = np.full(N_PATHS, S0)
    hedges: dict[tuple[str, str], Hedge] = {}
    integral: dict[str, Floats] = {}
    for name, every in (("fine", 1), ("coarse", COARSE_EVERY)):
        for hedge_vol in ("a", "i"):
            vol = SIG_A if hedge_vol == "a" else SIG_I
            d = delta(S, T, vol)
            hedges[(name, hedge_vol)] = Hedge(every, vol, d, -Vi + d * S)
        integral[name] = np.zeros(N_PATHS)
    for k in range(N_FINE):
        t = k * dt
        for name, every in (("fine", 1), ("coarse", COARSE_EVERY)):
            # left-point Riemann sum of the pathwise integral for the implied-delta hedge
            if k % every == 0:
                h = every * dt
                integral[name] += (
                    0.5
                    * (SIG_A**2 - SIG_I**2)
                    * math.exp(-R * t)
                    * S**2
                    * gamma(S, T - t, SIG_I)
                    * h
                )
        S = S * np.exp(
            (MU - SIG_A**2 / 2) * dt + SIG_A * math.sqrt(dt) * rng.standard_normal(N_PATHS)
        )
        t_new = (k + 1) * dt
        for st in hedges.values():
            st.cash = st.cash * math.exp(R * dt)
            if (k + 1) % st.every == 0 and k + 1 < N_FINE:
                new_delta = delta(S, T - t_new, st.vol)
                st.cash += (new_delta - st.delta) * S
                st.delta = new_delta
    payoff = np.maximum(S - K, 0)
    pnl = {key: math.exp(-R * T) * (payoff - st.delta * S + st.cash) for key, st in hedges.items()}
    return Simulation(pnl, integral)


def check_actual_hedge(report: CheckReport, sim: Simulation, Va: float, Vi: float) -> None:
    """The actual-volatility hedge's mean P&L, and its spread against the number of steps."""
    print("== hedging with actual volatility locks in V^a - V^i")
    for name, n in (("coarse", 252), ("fine", 2520)):
        x = sim.pnl[(name, "a")]
        m, se = x.mean(), x.std(ddof=1) / math.sqrt(N_PATHS)
        report.ok(
            f"{n} steps: mean P&L within 3 s.e. of 3.7807",
            bool(abs(m - (Va - Vi)) <= 3 * se),
            f"{m:.4f} (s.e. {se:.4f}, s.d. {x.std(ddof=1):.3f})",
        )
    ratio = sim.pnl[("coarse", "a")].std(ddof=1) / sim.pnl[("fine", "a")].std(ddof=1)
    report.ok(
        "s.d. ratio 252 against 2,520 steps in [2.8, 3.5] (sqrt(10) = 3.16)",
        bool(2.8 <= ratio <= 3.5),
        f"{ratio:.2f}",
    )


def check_implied_hedge(report: CheckReport, sim: Simulation) -> None:
    """The implied-volatility hedge's P&L against each path's integral."""
    print("== hedging with implied volatility: path-dependent total")
    gap = {}
    for name in ("coarse", "fine"):
        gap[name] = math.sqrt(np.mean((sim.pnl[(name, "i")] - sim.integral[name]) ** 2))
    shrink = gap["coarse"] / gap["fine"]
    report.ok(
        "RMS gap between each path's P&L and its pathwise integral shrinks by a factor in"
        " [2.5, 3.8]",
        2.5 <= shrink <= 3.8,
        f"{gap['coarse']:.3f} to {gap['fine']:.3f}, factor {shrink:.2f}",
    )
    sd_i = sim.pnl[("fine", "i")].std(ddof=1)
    report.ok(
        "cross-path s.d. at 2,520 steps stays above 1.5: the total remains random",
        bool(sd_i > 1.5),
        f"{sd_i:.2f}",
    )
    report.ok(
        "with sigma > implied and gamma >= 0 the pathwise integral is positive on every path",
        bool((sim.integral["fine"] > 0).all()),
    )
    mi = sim.pnl[("fine", "i")]
    print(
        f"  mean P&L of the implied-delta hedge {mi.mean():.4f} (s.e."
        f" {mi.std(ddof=1) / math.sqrt(N_PATHS):.4f});"
        " reported, not tested against V^a - V^i"
    )


def check_vanna_volga(report: CheckReport) -> None:
    """The closed-form vanna and volga against finite differences."""
    print("== vanna and volga (meth:greeks-delta-gamma-hedging)")
    d1, d2 = d12(S0, T, SIG_I)
    vega = S0 * math.exp(-Q * T) * stats.norm.pdf(d1) * math.sqrt(T)
    vanna = -math.exp(-Q * T) * stats.norm.pdf(d1) * d2 / SIG_I
    volga = vega * d1 * d2 / SIG_I
    h = 1e-4
    fd_vanna = (delta(S0, T, SIG_I + h) - delta(S0, T, SIG_I - h)) / (2 * h)
    fd_volga = (price(S0, T, SIG_I + h) - 2 * price(S0, T, SIG_I) + price(S0, T, SIG_I - h)) / h**2
    report.ok(
        "vanna -e^(-qT) n(d1) d2 / sigma and volga vega d1 d2 / sigma match finite differences",
        abs(fd_vanna - vanna) < 1e-6 and abs(fd_volga - volga) < 1e-3,
        f"vanna {vanna:.4f}, volga {volga:.4f}",
    )


# Unit cash digital, value e^(-r tau) N(d2), gamma -e^(-r tau) n(d2) d1 / (S^2 vol^2 tau). With
# actual volatility above implied, V^a - V^i < 0 here, and Gamma^i < 0 wherever d1 > 0 (S above
# about 93), so neither hedge's profit is positive merely because sigma > implied. Values
# computed in closed form; no simulation.
SD: Final = 120.0  # the digital's spot
KD: Final = 100.0
TD: Final = 1.0


def digital_d12(S: float, vol: float, k: float = KD, tau: float = TD) -> tuple[float, float]:
    """Return d1 and d2 for the cash digital."""
    d1 = (math.log(S / k) + (R + vol**2 / 2) * tau) / (vol * math.sqrt(tau))
    return d1, d1 - vol * math.sqrt(tau)


def digital(S: float, vol: float) -> float:
    """Return the unit cash-or-nothing call's value."""
    return math.exp(-R * TD) * stats.norm.cdf(digital_d12(S, vol)[1])


def digital_gamma(S: float, vol: float) -> float:
    """Return the cash digital's gamma in closed form."""
    d1, d2 = digital_d12(S, vol)
    return -math.exp(-R * TD) * stats.norm.pdf(d2) * d1 / (S**2 * vol**2 * TD)


def check_gamma_condition(report: CheckReport) -> None:
    """The cash digital: worth less at the higher volatility, and gamma of both signs."""
    print("== the gamma condition: a cash-or-nothing call (deterministic counterexample)")
    dig_a, dig_i = digital(SD, SIG_A), digital(SD, SIG_I)
    report.ok(
        "S0 = 120, K = 100: the cash digital is worth less at actual 30 percent than at implied 20"
        " percent",
        dig_a - dig_i < 0 and abs(dig_i - 0.8140556) < 5e-7 and abs(dig_a - 0.6980305) < 5e-7,
        f"V^a - V^i = {dig_a:.4f} - {dig_i:.4f} = {dig_a - dig_i:+.4f}",
    )
    h = 1e-3
    fd_gamma = (digital(SD + h, SIG_I) - 2 * dig_i + digital(SD - h, SIG_I)) / h**2
    g_low, g_high = digital_gamma(80.0, SIG_I), digital_gamma(SD, SIG_I)
    report.ok(
        "its implied-volatility gamma is positive at S = 80 and negative at S = 120 (closed form"
        " matches a"
        " finite difference)",
        g_low > 0 > g_high and abs(fd_gamma - g_high) < 1e-7,
        f"{g_low:+.6f} and {g_high:+.6f}",
    )


def main() -> int:
    """Print the versions, then run the value check, the simulation and the closed forms.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    Va, Vi = float(price(S0, T, SIG_A)), float(price(S0, T, SIG_I))
    report.ok(
        "V^a - V^i = 3.7807", abs(Va - Vi - 3.7807) < 5e-5, f"{Va:.4f} - {Vi:.4f} = {Va - Vi:.4f}"
    )
    print("== simulation on common paths")
    sim = simulate(np.random.default_rng(SEED), Vi)
    check_actual_hedge(report, sim, Va, Vi)
    check_implied_hedge(report, sim)
    check_vanna_volga(report)
    check_gamma_condition(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
