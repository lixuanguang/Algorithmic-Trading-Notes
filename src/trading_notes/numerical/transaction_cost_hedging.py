"""The worked examples of meth:transaction-cost-hedging.

Library gap-filling Batch L5, package L5-b (2026-10-21).

Inputs, conventions and acceptance were frozen before the first run. Wilmott, PWOQF 2nd ed.,
chap. 48: trading nu shares at S costs kappa |nu| S; rebalancing every dt = T/N; Leland's
volatilities (48.5)-(48.6), sigma_hat^2, sigma_check^2 = sigma^2 +/- 2 kappa sigma
sqrt(2/(pi dt)); K = kappa/(sigma sqrt(dt)) (48.7).

Conventions: position sign s = +1 long, -1 short one call; stock holding h_k = -s Delta_k with
the BSM delta at the position's Leland volatility (sigma_check long, sigma_hat short); trades
nu_k = h_k - h_{k-1} at S(t_k); cash grows at r and pays trades and costs; physical settlement,
so at T the holding moves to the payoff delta -s 1{S_T > K} (the N-th, costed trade). The
opening trade and the cash-settled close are reported separately. Risk-neutral simulation
(mu = r), q = 0, so the discounted stock is a martingale.

Comparable quantity (Interpretation): BSM(sigma_hat) - BSM(sigma) = E^Q int e^{-rt} kappa sigma
sqrt(2/(pi dt)) S^2 Gamma_hat dt exactly, the expected present value of Wilmott's leading-order
cost (48.2) under the sigma_hat delta. The simulated estimand C_N is the expected present value
of the actual costs of trades 1..N under the same rule; e_N = C_N - L is the approximation
residual, and E[e^{-rT} W_T] = -e_N for the writer at the Leland price.

Part 1 deterministic; part 2 simulation, default_rng(20261023), 100,000 paths of 208 log-exact
steps drawn in ten blocks of 10,000, nested grids N = 13, 52, 208, Leland numbers K = 0.1 and
0.4; part 3 the call-spread hedge-cost demonstration on the same paths (N = 52, kappa = 0.2
percent, BSM deltas at sigma). Synthetic model data only.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.transaction_cost_hedging
(numpy, scipy). Exits 1 on failure. About 20 seconds.
"""

# standard library imports
import math
import sys
from dataclasses import dataclass, field
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

# project library imports
from trading_notes.numerical.report import CheckReport

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


def bs_call(S: float, K: float, tau: float, vol: float) -> float:
    """Return the BSM call (q = 0)."""
    d1 = (math.log(S / K) + (R + vol**2 / 2) * tau) / (vol * math.sqrt(tau))
    return S * stats.norm.cdf(d1) - K * math.exp(-R * tau) * stats.norm.cdf(
        d1 - vol * math.sqrt(tau)
    )


def bs_delta(S: Floats, K: float, tau: Floats, vol: float) -> Floats:
    """Return the BSM call delta at each price, tau broadcast along the time axis."""
    return stats.norm.cdf((np.log(S / K) + (R + vol**2 / 2) * tau) / (vol * np.sqrt(tau)))


def leland_var(kappa: float, dt: float, sign: int) -> float:
    """sigma_hat^2 (sign = +1, short) or sigma_check^2 (sign = -1, long), eqs. (48.5)-(48.6)."""
    return SIG**2 + sign * 2 * kappa * SIG * math.sqrt(2 / (math.pi * dt))


def check_leland_volatilities(report: CheckReport) -> None:
    """Part 1: Leland's volatilities, their limits and domain, and Wilmott's spread."""
    sig = SIG
    print("== part 1: Leland volatilities, limits, domain, Wilmott's spread approximation")
    worst = 0.0
    for kappa in (0.0005, 0.002, 0.01):
        for dt in (1 / 252, 1 / 52, 1 / 13):
            for sign in (+1, -1):
                if leland_var(kappa, dt, sign) <= 0:
                    continue
                printed = sig * (1 + sign * math.sqrt(8 / (math.pi * dt)) * kappa / sig) ** 0.5
                worst = max(worst, abs(math.sqrt(leland_var(kappa, dt, sign)) / printed - 1))
    report.ok(
        "(48.5)-(48.6) equal the printed sigma (1 -/+ sqrt(8/(pi dt)) kappa/sigma)^(1/2)",
        worst <= 1e-14,
        f"{worst:.1e}",
    )
    dt52 = 1 / 52
    signs_ok = all(
        math.sqrt(leland_var(k, dt52, -1)) < sig < math.sqrt(leland_var(k, dt52, +1))
        for k in (1e-5, 0.002, 0.01)
    )
    report.ok(
        "signs: sigma_check < sigma < sigma_hat for kappa > 0 (long valued lower, short higher)",
        signs_ok,
    )
    report.ok(
        "zero-cost limit: kappa = 0 gives sigma_check = sigma_hat = sigma and a zero premium"
        " adjustment",
        leland_var(0.0, dt52, 1) == leland_var(0.0, dt52, -1) == sig**2
        and bs_call(S0, KS, T, math.sqrt(leland_var(0.0, dt52, 1))) - bs_call(S0, KS, T, sig)
        == 0.0,
    )
    Kstar = math.sqrt(math.pi / 8)
    kap_star = Kstar * sig * math.sqrt(dt52)
    report.ok(
        "domain of the long formula: sigma_check^2 = 0 at K* = sqrt(pi/8), negative above",
        abs(leland_var(kap_star, dt52, -1)) <= 1e-15 * sig**2
        and leland_var(1.01 * kap_star, dt52, -1) < 0,
        f"K* = {Kstar:.4f}; at dt = 1/52 kappa* = sigma sqrt(pi dt/8) = {kap_star:.5f}; the bound"
        " printed on p. 789,"
        f" sigma/sqrt(8 pi dt), would be {sig / math.sqrt(8 * math.pi * dt52):.4f}",
    )
    d1 = (math.log(S0 / KS) + (R + sig**2 / 2) * T) / (sig * math.sqrt(T))
    rel = {}
    for K in (0.01, 0.001):
        kap = K * sig * math.sqrt(dt52)
        L = bs_call(S0, KS, T, math.sqrt(leland_var(kap, dt52, 1))) - bs_call(S0, KS, T, sig)
        approx = 2 * kap * S0 * stats.norm.pdf(d1) * math.sqrt(T) / math.sqrt(2 * math.pi * dt52)
        rel[K] = abs(approx / L - 1)
    report.ok(
        "Wilmott's spread 2 kappa S N'(d1) sqrt(tau)/sqrt(2 pi dt) is first order: relative error"
        " falls 5-20 times from K = 0.01 to 0.001",
        5 <= rel[0.01] / rel[0.001] <= 20,
        f"{rel[0.01]:.2e} and {rel[0.001]:.2e}",
    )


@dataclass
class Ledger:
    """One position's per-path results at K = 0.1, N = 52, appended block by block.

    Attributes:
        id_err: The largest relative error of the ledger identity so far.
        test: Discounted gains plus s(discounted payoff - V), whose mean the identity sets to 0.
        pnl: Discounted terminal wealth at the Leland price.
        opening: The opening trade's cost.
        cash_close: The discounted cost of a cash-settled close instead of delivery.
        settle: The discounted cost of the settlement trade.
    """

    id_err: float = 0.0
    test: list[Floats] = field(default_factory=list)
    pnl: list[Floats] = field(default_factory=list)
    opening: list[Floats] = field(default_factory=list)
    cash_close: list[Floats] = field(default_factory=list)
    settle: list[Floats] = field(default_factory=list)


@dataclass
class FixedHedge:
    """The short call hedged at sigma with kappa = 0.2 percent, on one grid, block by block.

    Attributes:
        cost: Each path's present value of costs.
        pnl: Each path's discounted P&L at the BSM premium.
    """

    cost: list[Floats] = field(default_factory=list)
    pnl: list[Floats] = field(default_factory=list)


@dataclass
class SpreadCosts:
    """Part 3's costs of hedging a bull spread's legs separately and netted, block by block.

    Attributes:
        sep: Each path's present value of the separately hedged legs' costs.
        agg: The same with the legs' trades netted.
        step_ok: Whether netting never cost more, at every step of every path so far.
        same_ok: Whether long and short the same call netted to zero cost, at twice one leg apart.
    """

    sep: list[Floats] = field(default_factory=list)
    agg: list[Floats] = field(default_factory=list)
    step_ok: bool = True
    same_ok: bool = True


@dataclass(frozen=True)
class Simulation:
    """What the simulation accumulates.

    Attributes:
        cost_acc: The sum and the sum of squares of the costs' present values, by
            (sign, K, N).
        ledger: Per-path results by position sign.
        fixed: Per-path results of the fixed-kappa hedge by grid.
        spread: The call-spread demonstration's costs.
    """

    cost_acc: dict[tuple[int, float, int], list[float]]
    ledger: dict[int, Ledger]
    fixed: dict[int, FixedHedge]
    spread: SpreadCosts


def simulate(rng: np.random.Generator) -> Simulation:
    """Simulate the paths in blocks and hedge every case on every grid, on the same paths.

    Each block draws one normal per fine step and path; the coarser grids take every 4th or
    16th fine date.
    """
    r, sig, n_fine = R, SIG, N_FINE
    cost_acc = {(s, K, n): [0.0, 0.0] for s, K in CASES for n in GRIDS}
    ledger = {s: Ledger() for s in (-1, +1)}
    fixed = {n: FixedHedge() for n in GRIDS}
    spread = SpreadCosts()
    for _ in range(N_PATHS // BLOCK):
        z = rng.standard_normal((BLOCK, n_fine))
        dtf = T / n_fine
        S = np.empty((BLOCK, n_fine + 1))
        S[:, 0] = S0
        S[:, 1:] = S0 * np.exp(np.cumsum((r - sig**2 / 2) * dtf + sig * math.sqrt(dtf) * z, axis=1))
        for n in GRIDS:
            Sk = S[:, :: n_fine // n]
            dt = T / n
            # Float64 dates: the integers convert exactly, as they would in the product.
            t = np.arange(n + 1, dtype=np.float64) * dt
            disc = np.exp(-r * t)
            itm = (Sk[:, -1] > KS).astype(float)
            for s, K in CASES:
                kappa = K * sig * math.sqrt(dt)
                # short (s = -1) uses sigma_hat, long sigma_check
                vol = math.sqrt(leland_var(kappa, dt, -s))
                delta = np.empty_like(Sk)
                delta[:, :-1] = bs_delta(Sk[:, :-1], KS, T - t[:-1], vol)
                delta[:, -1] = itm
                h = -s * delta
                nu = np.diff(h, axis=1)
                cost = kappa * Sk[:, 1:] * np.abs(nu)
                pv_cost = cost @ disc[1:]
                cost_acc[(s, K, n)][0] += pv_cost.sum()
                cost_acc[(s, K, n)][1] += (pv_cost**2).sum()
                if n == 52 and K == 0.1:
                    led = ledger[s]
                    V = bs_call(S0, KS, T, sig)
                    P = bs_call(S0, KS, T, vol)
                    cash = -s * P - h[:, 0] * S0
                    for k in range(1, n + 1):
                        cash = cash * math.exp(r * dt) - nu[:, k - 1] * Sk[:, k] - cost[:, k - 1]
                    lhs = math.exp(-r * T) * (cash + h[:, -1] * Sk[:, -1])
                    gains = (h[:, :-1] * np.diff(Sk * disc, axis=1)).sum(axis=1)
                    rhs = -s * P + gains - pv_cost
                    led.id_err = max(
                        led.id_err, float(np.max(np.abs(lhs - rhs) / (1 + np.abs(lhs))))
                    )
                    payoff = np.maximum(Sk[:, -1] - KS, 0)
                    W = lhs + s * math.exp(-r * T) * payoff  # discounted terminal wealth
                    led.test.append(gains + s * (math.exp(-r * T) * payoff - V))
                    led.pnl.append(W)
                    led.opening.append(kappa * np.abs(h[:, 0]) * S0)
                    led.cash_close.append(math.exp(-r * T) * kappa * np.abs(h[:, -2]) * Sk[:, -1])
                    led.settle.append(math.exp(-r * T) * cost[:, -1])
            # fixed kappa = 0.2 percent, short call hedged with the BSM delta at sigma, premium V
            delta = np.empty_like(Sk)
            delta[:, :-1] = bs_delta(Sk[:, :-1], KS, T - t[:-1], sig)
            delta[:, -1] = itm
            h = delta
            nu = np.diff(h, axis=1)
            pv_cost = (0.002 * Sk[:, 1:] * np.abs(nu)) @ disc[1:]
            gains = (h[:, :-1] * np.diff(Sk * disc, axis=1)).sum(axis=1)
            V = bs_call(S0, KS, T, sig)
            fixed[n].cost.append(pv_cost)
            fixed[n].pnl.append(
                V + gains - pv_cost - math.exp(-r * T) * np.maximum(Sk[:, -1] - KS, 0)
            )
            if n == 52:
                # part 3: bull spread, long K1 = 95, short K2 = 105, BSM deltas at sigma,
                # kappa = 0.2 percent
                legs = []
                for Kl, sl in ((95.0, +1), (105.0, -1)):
                    dl = np.empty_like(Sk)
                    dl[:, :-1] = bs_delta(Sk[:, :-1], Kl, T - t[:-1], sig)
                    dl[:, -1] = (Sk[:, -1] > Kl).astype(float)
                    legs.append(np.diff(-sl * dl, axis=1))
                c_sep = 0.002 * Sk[:, 1:] * (np.abs(legs[0]) + np.abs(legs[1]))
                c_agg = 0.002 * Sk[:, 1:] * np.abs(legs[0] + legs[1])
                spread.step_ok &= bool((c_agg <= c_sep + 1e-12).all())
                spread.sep.append(c_sep @ disc[1:])
                spread.agg.append(c_agg @ disc[1:])
                # long and short the same call: net holding zero
                nu_long = np.diff(-delta, axis=1)
                nu_short = np.diff(delta, axis=1)
                agg_same = (0.002 * Sk[:, 1:] * np.abs(nu_long + nu_short)) @ disc[1:]
                sep_same = (0.002 * Sk[:, 1:] * (np.abs(nu_long) + np.abs(nu_short))) @ disc[1:]
                single = (0.002 * Sk[:, 1:] * np.abs(nu_short)) @ disc[1:]
                spread.same_ok &= bool(
                    (agg_same == 0).all() and (np.abs(sep_same - 2 * single) <= 1e-12).all()
                )
    return Simulation(cost_acc, ledger, fixed, spread)


def check_ledgers(report: CheckReport, sim: Simulation) -> None:
    """Part 2: the ledger identity on every path, and the mean discounted wealth."""
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
    """Part 2: the residual e_N = C_N - L on each grid, which must shrink as N grows."""
    sig = SIG
    print("    residual e_N = C_N - L (s.e. of C_N), relative to L")
    for s, K in CASES:
        dt_ref = {n: T / n for n in GRIDS}
        res = {}
        for n in GRIDS:
            kappa = K * sig * math.sqrt(dt_ref[n])
            vol = math.sqrt(leland_var(kappa, dt_ref[n], -s))
            L = -s * (bs_call(S0, KS, T, vol) - V)
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
    """Part 3: netting the bull spread's trades never costs more, and saves on average."""
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
    vc, vh = math.sqrt(leland_var(kap, dtx, -1)), math.sqrt(leland_var(kap, dtx, +1))
    leg_by_leg = bs_call(S0, 95.0, T, vc) - bs_call(S0, 105.0, T, vh)
    bs_spread = bs_call(S0, 95.0, T, SIG) - bs_call(S0, 105.0, T, SIG)
    print(
        f"    reported, approximate: BSM spread {bs_spread:.4f}; leg-by-leg Leland {leg_by_leg:.4f}"
        f" (long at {vc:.4f},"
        f" short at {vh:.4f}); BSM less simulated costs: separate {bs_spread - sep.mean():.4f},"
        " aggregated"
        f" {bs_spread - agg.mean():.4f}"
    )


def main() -> int:
    """Print the versions, then run the three parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_leland_volatilities(report)
    print(
        "== part 2: simulated hedging costs against the Leland adjustment (risk-neutral, nested"
        " grids)"
    )
    sim = simulate(np.random.default_rng(SEED))
    V = bs_call(S0, KS, T, SIG)
    check_ledgers(report, sim)
    check_residuals(report, sim, V)
    report_pnl(sim, V)
    check_nonadditivity(report, sim)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
