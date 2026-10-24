"""Delta hedging at the wrong volatility, the vanna and volga formulas, and the gamma condition."""

import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.option_hedging.volatility_mismatch import (
    CashDigital,
    MismatchExperiment,
    Simulation,
    VanillaCall,
)
from trading_notes.numerical.report import CheckReport, print_versions

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
CALL: Final = VanillaCall(strike=K, maturity=T, rate=R, dividend_yield=Q)
EXPERIMENT: Final = MismatchExperiment(
    call=CALL,
    spot=S0,
    drift=MU,
    actual_vol=SIG_A,
    implied_vol=SIG_I,
    n_paths=N_PATHS,
    n_fine=N_FINE,
    coarse_every=COARSE_EVERY,
)


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
    d1, d2 = CALL.d12(S0, T, SIG_I)
    vega = S0 * math.exp(-Q * T) * stats.norm.pdf(d1) * math.sqrt(T)
    vanna = -math.exp(-Q * T) * stats.norm.pdf(d1) * d2 / SIG_I
    volga = vega * d1 * d2 / SIG_I
    h = 1e-4
    fd_vanna = (CALL.delta(S0, T, SIG_I + h) - CALL.delta(S0, T, SIG_I - h)) / (2 * h)
    fd_volga = (
        CALL.price(S0, T, SIG_I + h) - 2 * CALL.price(S0, T, SIG_I) + CALL.price(S0, T, SIG_I - h)
    ) / h**2
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
DIGITAL: Final = CashDigital(strike=KD, maturity=TD, rate=R)


def check_gamma_condition(report: CheckReport) -> None:
    """The cash digital: worth less at the higher volatility, and gamma of both signs."""
    print("== the gamma condition: a cash-or-nothing call (deterministic counterexample)")
    dig_a, dig_i = DIGITAL.value(SD, SIG_A), DIGITAL.value(SD, SIG_I)
    report.ok(
        "S0 = 120, K = 100: the cash digital is worth less at actual 30 percent than at implied 20"
        " percent",
        dig_a - dig_i < 0 and abs(dig_i - 0.8140556) < 5e-7 and abs(dig_a - 0.6980305) < 5e-7,
        f"V^a - V^i = {dig_a:.4f} - {dig_i:.4f} = {dig_a - dig_i:+.4f}",
    )
    h = 1e-3
    fd_gamma = (DIGITAL.value(SD + h, SIG_I) - 2 * dig_i + DIGITAL.value(SD - h, SIG_I)) / h**2
    g_low, g_high = DIGITAL.gamma(80.0, SIG_I), DIGITAL.gamma(SD, SIG_I)
    report.ok(
        "its implied-volatility gamma is positive at S = 80 and negative at S = 120 (closed form"
        " matches a"
        " finite difference)",
        g_low > 0 > g_high and abs(fd_gamma - g_high) < 1e-7,
        f"{g_low:+.6f} and {g_high:+.6f}",
    )


def main() -> int:
    """Print the versions, then run the value check, the simulation and the closed forms.

    Model: dS = mu S dt + sigma S dW with mu = 10 percent and actual volatility 30 percent; a call
    (S0 = K = 100, T = 1, r = 5 percent, q = 0) bought at the BSM price at implied volatility 20
    percent and marked there; short delta shares; cash at r; no costs. 20,000 paths, rebalanced 252
    or 2,520 times on common paths; profit is present value at time 0; seed 20261051. The final
    section shows that sigma above implied volatility makes the implied-volatility hedge profitable
    only with Gamma >= 0: a unit cash digital (S0 = 120, K = 100) is worth less at 30 than at 20
    percent volatility, and its gamma changes sign. Synthetic data only; about 10 seconds.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    Va, Vi = float(CALL.price(S0, T, SIG_A)), float(CALL.price(S0, T, SIG_I))
    report.ok(
        "V^a - V^i = 3.7807", abs(Va - Vi - 3.7807) < 5e-5, f"{Va:.4f} - {Vi:.4f} = {Va - Vi:.4f}"
    )
    print("== simulation on common paths")
    sim = EXPERIMENT.simulate(np.random.default_rng(SEED), Vi)
    check_actual_hedge(report, sim, Va, Vi)
    check_implied_hedge(report, sim)
    check_vanna_volga(report)
    check_gamma_condition(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
