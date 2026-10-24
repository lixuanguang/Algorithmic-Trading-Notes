"""Worked examples of delta hedging with transaction costs (Wilmott, PWOQF 2nd ed., chap. 48)."""

import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.option_hedging.leland_hedging import LelandExperiment, Simulation
from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.numerical.report import CheckReport, print_versions

type Floats = NDArray[np.float64]

SEED: Final = 20261023
# Wilmott sec. 48.12 setting; q = 0
S0: Final = 100.0
KS: Final = 100.0  # the call's strike
SIG: Final = 0.2
R: Final = 0.05
T: Final = 1.0
N_PATHS: Final = 100_000
N_FINE: Final = 208  # steps of the finest grid
BLOCK: Final = 10_000  # paths drawn at a time
GRIDS: Final = (13, 52, 208)
# (position sign, Leland number K): short and long, at K = 0.1 and 0.4
CASES: Final = tuple((s, K) for s in (-1, +1) for K in (0.1, 0.4))
NAME: Final = {-1: "short", +1: "long"}
EXPERIMENT: Final = LelandExperiment(
    spot=S0,
    strike=KS,
    sigma=SIG,
    rate=R,
    maturity=T,
    n_paths=N_PATHS,
    n_fine=N_FINE,
    block=BLOCK,
    grids=GRIDS,
    cases=CASES,
)


def check_leland_volatilities(report: CheckReport) -> None:
    """Check Leland's volatilities, their limits and domain, and Wilmott's spread."""
    sig = SIG
    print("== part 1: Leland volatilities, limits, domain, Wilmott's spread approximation")
    worst = 0.0
    for kappa in (0.0005, 0.002, 0.01):
        for dt in (1 / 252, 1 / 52, 1 / 13):
            for sign in (+1, -1):
                if EXPERIMENT.leland_variance(kappa, dt, sign) <= 0:
                    continue
                printed = sig * (1 + sign * math.sqrt(8 / (math.pi * dt)) * kappa / sig) ** 0.5
                worst = max(
                    worst, abs(math.sqrt(EXPERIMENT.leland_variance(kappa, dt, sign)) / printed - 1)
                )
    report.ok(
        "(48.5)-(48.6) equal the printed sigma (1 -/+ sqrt(8/(pi dt)) kappa/sigma)^(1/2)",
        worst <= 1e-14,
        f"{worst:.1e}",
    )
    dt52 = 1 / 52
    signs_ok = all(
        math.sqrt(EXPERIMENT.leland_variance(k, dt52, -1))
        < sig
        < math.sqrt(EXPERIMENT.leland_variance(k, dt52, +1))
        for k in (1e-5, 0.002, 0.01)
    )
    report.ok(
        "signs: sigma_check < sigma < sigma_hat for kappa > 0 (long valued lower, short higher)",
        signs_ok,
    )
    report.ok(
        "zero-cost limit: kappa = 0 gives sigma_check = sigma_hat = sigma and a zero premium"
        " adjustment",
        EXPERIMENT.leland_variance(0.0, dt52, 1)
        == EXPERIMENT.leland_variance(0.0, dt52, -1)
        == sig**2
        and BlackScholes(
            spot=S0,
            strike=KS,
            maturity=T,
            rate=R,
            vol=math.sqrt(EXPERIMENT.leland_variance(0.0, dt52, 1)),
        ).call()
        - BlackScholes(spot=S0, strike=KS, maturity=T, rate=R, vol=sig).call()
        == 0.0,
    )
    Kstar = math.sqrt(math.pi / 8)
    kap_star = Kstar * sig * math.sqrt(dt52)
    report.ok(
        "domain of the long formula: sigma_check^2 = 0 at K* = sqrt(pi/8), negative above",
        abs(EXPERIMENT.leland_variance(kap_star, dt52, -1)) <= 1e-15 * sig**2
        and EXPERIMENT.leland_variance(1.01 * kap_star, dt52, -1) < 0,
        f"K* = {Kstar:.4f}; at dt = 1/52 kappa* = sigma sqrt(pi dt/8) = {kap_star:.5f}; the bound"
        " printed on p. 789,"
        f" sigma/sqrt(8 pi dt), would be {sig / math.sqrt(8 * math.pi * dt52):.4f}",
    )
    d1 = (math.log(S0 / KS) + (R + sig**2 / 2) * T) / (sig * math.sqrt(T))
    rel = {}
    for K in (0.01, 0.001):
        kap = K * sig * math.sqrt(dt52)
        L = (
            BlackScholes(
                spot=S0,
                strike=KS,
                maturity=T,
                rate=R,
                vol=math.sqrt(EXPERIMENT.leland_variance(kap, dt52, 1)),
            ).call()
            - BlackScholes(spot=S0, strike=KS, maturity=T, rate=R, vol=sig).call()
        )
        approx = 2 * kap * S0 * stats.norm.pdf(d1) * math.sqrt(T) / math.sqrt(2 * math.pi * dt52)
        rel[K] = abs(approx / L - 1)
    report.ok(
        "Wilmott's spread 2 kappa S N'(d1) sqrt(tau)/sqrt(2 pi dt) is first order: relative error"
        " falls 5-20 times from K = 0.01 to 0.001",
        5 <= rel[0.01] / rel[0.001] <= 20,
        f"{rel[0.01]:.2e} and {rel[0.001]:.2e}",
    )


def check_ledgers(report: CheckReport, sim: Simulation) -> None:
    """Check the ledger identity on every path, and the mean discounted wealth."""
    for s in (-1, +1):
        led = sim.ledger[s]
        report.ok(
            f"{NAME[s]}, K = 0.1, N = 52: ledger identity on every path (signs, financing and"
            " discounting)",
            led.id_err <= 1e-9,
            f"largest relative error {led.id_err:.1e}",
        )
        x = np.concatenate(led.test)
        m, se = x.mean(), x.std(ddof=1) / math.sqrt(N_PATHS)
        report.ok(
            f"{NAME[s]}: mean discounted wealth within 4 s.e. of -s(P - V) - C_N (exact in"
            " expectation)",
            bool(abs(m) <= 4 * se),
            f"difference {m:+.4f} (s.e. {se:.4f}), z = {m / se:+.2f}",
        )


def check_residuals(report: CheckReport, sim: Simulation, V: float) -> None:
    """Check the residual e_N = C_N - L on each grid, which must shrink as N grows."""
    sig = SIG
    print("    residual e_N = C_N - L (s.e. of C_N), relative to L")
    for s, K in CASES:
        dt_ref = {n: T / n for n in GRIDS}
        res = {}
        for n in GRIDS:
            kappa = K * sig * math.sqrt(dt_ref[n])
            vol = math.sqrt(EXPERIMENT.leland_variance(kappa, dt_ref[n], -s))
            L = -s * (BlackScholes(spot=S0, strike=KS, maturity=T, rate=R, vol=vol).call() - V)
            sm, sq = sim.cost_acc[(s, K, n)]
            C = sm / N_PATHS
            se = math.sqrt((sq / N_PATHS - C**2) / (N_PATHS - 1))
            res[n] = C - L
            print(
                f"    {NAME[s]:5s} K = {K}: N = {n:3d}, kappa = {kappa:.5f}, vol = {vol:.4f}, L ="
                f" {L:.4f}, C_N = {C:.4f}"
                f" (s.e. {se:.4f}), e_N = {C - L:+.4f} ({(C - L) / L:+.2%})"
            )
        a = [abs(res[n]) for n in GRIDS]
        report.ok(
            f"{NAME[s]} K = {K}: |e_13| > |e_52| > |e_208| and |e_208| <= |e_13| / 2",
            a[0] > a[1] > a[2] and a[2] <= 0.5 * a[0],
            f"{a[0]:.4f}, {a[1]:.4f}, {a[2]:.4f}",
        )


def report_pnl(sim: Simulation, V: float) -> None:
    """Part 2, reported: P&L at the Leland price, and the fixed-kappa hedge on each grid."""
    for s in (-1, +1):
        led = sim.ledger[s]
        w = np.concatenate(led.pnl)
        print(
            f"    {NAME[s]} at the Leland price, K = 0.1, N = 52: mean discounted P&L"
            f" {w.mean():+.4f} (s.e."
            f" {w.std(ddof=1) / math.sqrt(N_PATHS):.4f}), s.d. {w.std(ddof=1):.3f}, 5th percentile"
            f" {np.percentile(w, 5):+.3f};"
            f" opening cost {np.concatenate(led.opening).mean():.4f}; settlement trade"
            f" {np.concatenate(led.settle).mean():.4f} against a"
            f" cash-settled close {np.concatenate(led.cash_close).mean():.4f}"
        )
    for n in GRIDS:
        c, p = np.concatenate(sim.fixed[n].cost), np.concatenate(sim.fixed[n].pnl)
        print(
            f"    fixed kappa = 0.2%, BSM delta, short call, N = {n:3d}: mean PV cost"
            f" {c.mean():.4f},"
            f" P&L s.d. {p.std(ddof=1):.3f},"
            f" premium for a loss only 5 percent of the time {V - np.percentile(p, 5):.3f}"
        )


def check_nonadditivity(report: CheckReport, sim: Simulation) -> None:
    """Check netting the bull spread's trades never costs more, and saves on average."""
    print(
        "== part 3: nonadditivity, a hedge-cost demonstration on the same paths (not a solved"
        " valuation)"
    )
    sep, agg = np.concatenate(sim.spread.sep), np.concatenate(sim.spread.agg)
    report.ok(
        "bull spread: aggregated trade cost never exceeds the separately hedged legs (every step,"
        " every path)",
        sim.spread.step_ok,
    )
    d = sep - agg
    m, se = d.mean(), d.std(ddof=1) / math.sqrt(N_PATHS)
    report.ok(
        "bull spread: mean saving from netting positive by more than 4 paired s.e.",
        bool(m > 4 * se),
        f"separate {sep.mean():.4f}, aggregated {agg.mean():.4f}, saving {m:.4f} (s.e. {se:.5f})",
    )
    report.ok(
        "long and short the same call: aggregated cost 0 on every path, separate cost exactly twice"
        " one leg",
        sim.spread.same_ok,
    )
    kap, dtx = 0.002, 1 / 52
    vc, vh = (
        math.sqrt(EXPERIMENT.leland_variance(kap, dtx, -1)),
        math.sqrt(EXPERIMENT.leland_variance(kap, dtx, +1)),
    )
    leg_by_leg = (
        BlackScholes(spot=S0, strike=95.0, maturity=T, rate=R, vol=vc).call()
        - BlackScholes(spot=S0, strike=105.0, maturity=T, rate=R, vol=vh).call()
    )
    bs_spread = (
        BlackScholes(spot=S0, strike=95.0, maturity=T, rate=R, vol=SIG).call()
        - BlackScholes(spot=S0, strike=105.0, maturity=T, rate=R, vol=SIG).call()
    )
    print(
        f"    reported, approximate: BSM spread {bs_spread:.4f}; leg-by-leg Leland {leg_by_leg:.4f}"
        f" (long at {vc:.4f},"
        f" short at {vh:.4f}); BSM less simulated costs: separate {bs_spread - sep.mean():.4f},"
        " aggregated"
        f" {bs_spread - agg.mean():.4f}"
    )


def main() -> int:
    """Print the versions, then run the three parts with one report.

    Leland's volatilities sigma_hat^2, sigma_check^2 = sigma^2 +/- 2 kappa sigma sqrt(2/(pi dt)),
    with Leland number K = kappa / (sigma sqrt(dt)). The comparable quantity is BSM(sigma_hat) -
    BSM(sigma), exactly the expected present value of Wilmott's leading-order cost (48.2) under the
    sigma_hat delta; the simulated estimand C_N is the expected present value of the actual costs of
    trades 1..N, and e_N = C_N - L is the approximation residual. Part 1 is deterministic; part 2
    simulates 100,000 paths of 208 log-exact steps (default_rng(20261023), ten blocks), nested grids
    N = 13, 52, 208 and K = 0.1 and 0.4; part 3 is a call-spread hedge-cost demonstration on the
    same paths. The opening trade and a cash-settled close are reported separately. Synthetic model
    data only; about 20 seconds.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    check_leland_volatilities(report)
    print(
        "== part 2: simulated hedging costs against the Leland adjustment (risk-neutral, nested"
        " grids)"
    )
    sim = EXPERIMENT.simulate(np.random.default_rng(SEED))
    V = BlackScholes(spot=S0, strike=KS, maturity=T, rate=R, vol=SIG).call()
    check_ledgers(report, sim)
    check_residuals(report, sim, V)
    report_pnl(sim, V)
    check_nonadditivity(report, sim)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
