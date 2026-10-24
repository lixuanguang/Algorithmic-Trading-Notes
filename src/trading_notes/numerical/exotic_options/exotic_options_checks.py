"""Digital, barrier and Asian option closed forms checked against Monte Carlo."""

import math
import sys
from collections.abc import Callable, Iterator
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.exotic_options.exotic_pricing import ExoticPricer
from trading_notes.numerical.report import CheckReport, print_versions

type Floats = NDArray[np.float64]

N: Final = stats.norm.cdf
M: Final = 100_000
N_DATES: Final = 12  # monthly averaging dates of the Asian checks
S0: Final = 100.0
K: Final = 100.0
r: Final = 0.05
q: Final = 0.02
sg: Final = 0.25
T: Final = 1.0
PRICER: Final = ExoticPricer(rate=r, dividend_yield=q, vol=sg)


def mc(x: Floats) -> tuple[float, float]:
    """Return the mean of x and its standard error."""
    return x.mean(), x.std(ddof=1) / math.sqrt(len(x))


type Price = Callable[[float, float, float, float, float], float]


def vega(f: Price, S: float, k: float, h: float, tau: float, step: float = 1e-4) -> float:
    """Return the central-difference vega of the price f at spot S, with barrier h."""
    return (f(S, k, h, tau, sg + step) - f(S, k, h, tau, sg - step)) / (2 * step)


def check_digital(report: CheckReport, seeds: Iterator[int]) -> float:
    """Check digital options, their identities, the call spread and a Monte Carlo check.

    Args:
        report: The run's report.
        seeds: The run's seed sequence; this part takes its next seed.

    Returns:
        The vanilla call of the inputs, which parts 2 and 3 compare against.
    """
    print("== digital options")
    c = PRICER.call(S0, K, T)
    report.ok(
        "asset digital minus K times the unit cash digital equals the call to 1e-12",
        abs(PRICER.asset_digital(S0, K, T) - K * PRICER.cash_digital(S0, K, T) - c) < 1e-12,
        f"call {c:.6f}, cash digital {PRICER.cash_digital(S0, K, T):.6f}, asset digital"
        f" {PRICER.asset_digital(S0, K, T):.4f}",
    )
    report.ok(
        "cash call plus cash put digital equals the discount factor e^(-rT)",
        abs(
            PRICER.cash_digital(S0, K, T)
            + math.exp(-r * T) * N(-PRICER.option(S0, K, T).d2)
            - math.exp(-r * T)
        )
        < 1e-14,
    )
    err = []
    for eps in (2.0, 1.0, 0.5):
        spread = (PRICER.call(S0, K - eps, T) - PRICER.call(S0, K + eps, T)) / (2 * eps)
        err.append(spread - PRICER.cash_digital(S0, K, T))
    report.ok(
        "centred call spread of half-width 2, 1, 0.5: successive error ratios in [3.5, 4.5]",
        3.5 <= err[0] / err[1] <= 4.5 and 3.5 <= err[1] / err[2] <= 4.5,
        f"errors {err[0]:.2e}, {err[1]:.2e}, {err[2]:.2e}",
    )
    rng = np.random.default_rng(next(seeds))
    ST = S0 * np.exp((r - q - sg**2 / 2) * T + sg * math.sqrt(T) * rng.standard_normal(M))
    est, se = mc(np.asarray(math.exp(-r * T) * (ST > K), dtype=np.float64))
    report.ok(
        "simulated cash digital within 3 s.e. of e^(-rT) N(d2)",
        abs(est - PRICER.cash_digital(S0, K, T)) <= 3 * se,
        f"{est:.4f} (s.e. {se:.4f})",
    )

    deltas = [PRICER.cash_digital_delta(K, K, tau) for tau in (1.0, 1 / 12, 1 / 252)]
    report.ok(
        "pin risk: at the strike the cash digital's delta grows like 1/sqrt(tau) (1 year, 1 month,"
        " 1 day)",
        deltas[0] < deltas[1] < deltas[2] and abs(deltas[2] / deltas[1] - math.sqrt(21)) < 0.1,
        ", ".join(f"{d:.4f}" for d in deltas),
    )

    one_day = [PRICER.cash_digital_delta(S, K, 1 / 252) for S in (99.9, 100.0, 100.1)]
    report.ok(
        "one day before expiry the delta is positive on both sides of the strike: the hedge"
        " changes size, not sign",
        min(one_day) > 0,
        "S = 99.9, 100, 100.1: " + ", ".join(f"{d:.4f}" for d in one_day),
    )
    return c


def check_barrier(report: CheckReport, seeds: Iterator[int], c: float) -> None:
    """Check down-and-out and down-and-in calls by closed form, parity and Monte Carlo.

    Args:
        report: The run's report.
        seeds: The run's seed sequence; this part takes its next three seeds, in order.
        c: The vanilla call of the inputs, from part 1.
    """
    print("== barrier options (down-and-out and down-and-in calls, H = 90)")
    H = 90.0
    cdo, cdi = PRICER.down_out_call(S0, K, H, T), PRICER.down_in_call(S0, K, H, T)
    report.ok(
        "closed forms: c_do + c_di = c",
        abs(cdo + cdi - c) < 1e-12,
        f"c_do {cdo:.4f}, c_di {cdi:.4f}",
    )
    m = 252
    dt = T / m
    rng = np.random.default_rng(next(seeds))
    logS = np.log(S0) + np.cumsum(
        (r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal((M, m)), axis=1
    )
    paths = np.exp(logS)
    hit = (paths <= H).any(axis=1)
    vanilla = math.exp(-r * T) * np.maximum(paths[:, -1] - K, 0)
    knock_out = np.where(hit, 0.0, vanilla)
    knock_in = np.where(hit, vanilla, 0.0)
    report.ok(
        "in-out parity path by path on common paths (daily monitoring), to 1e-12",
        bool(np.max(np.abs(knock_out + knock_in - vanilla)) < 1e-12),
    )
    # Continuous monitoring: weight each path by the Brownian-bridge probability of not crossing H
    # between dates.
    rng = np.random.default_rng(next(seeds))
    logS = np.log(S0) + np.cumsum(
        (r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal((M, m)), axis=1
    )
    x = np.concatenate([np.full((M, 1), math.log(S0 / H)), logS - math.log(H)], axis=1)
    survive_step = np.where(
        (x[:, :-1] > 0) & (x[:, 1:] > 0), 1 - np.exp(-2 * x[:, :-1] * x[:, 1:] / (sg**2 * dt)), 0.0
    )
    bb = math.exp(-r * T) * np.maximum(np.exp(logS[:, -1]) - K, 0) * survive_step.prod(axis=1)
    est, se = mc(np.asarray(bb, dtype=np.float64))
    report.ok(
        "continuous down-and-out call: Brownian-bridge Monte Carlo within 3 s.e. of the closed"
        " form",
        abs(est - cdo) <= 3 * se,
        f"{est:.4f} (s.e. {se:.4f}) against {cdo:.4f}",
    )
    rng = np.random.default_rng(next(seeds))
    logS = np.log(S0) + np.cumsum(
        (r - q - sg**2 / 2) * dt + sg * math.sqrt(dt) * rng.standard_normal((M, m)), axis=1
    )
    disc_do = (
        math.exp(-r * T)
        * np.maximum(np.exp(logS[:, -1]) - K, 0)
        * ~(logS <= math.log(H)).any(axis=1)
    )
    est_d, se_d = mc(np.asarray(disc_do, dtype=np.float64))
    H_shift = H * math.exp(-0.5826 * sg * math.sqrt(T / m))
    bgk = PRICER.down_out_call(S0, K, H_shift, T)
    report.ok(
        "daily monitoring: Monte Carlo within 3 s.e. + 0.5 percent of the shifted-barrier closed"
        " form",
        abs(est_d - bgk) <= 3 * se_d + 0.005 * bgk,
        f"{est_d:.4f} (s.e. {se_d:.4f}) against {bgk:.4f} (barrier {H_shift:.3f}); continuous"
        f" {cdo:.4f}",
    )
    report.ok(
        "discrete monitoring knocks out less often, so it is worth more than continuous",
        est_d > cdo,
    )

    v_far, v_near = (
        vega(PRICER.down_out_call, 130.0, K, H, T),
        vega(PRICER.down_out_call, 91.0, K, H, T),
    )
    report.ok(
        "down-and-out call (H = 90 < K): vega shrinks towards zero near the barrier (below a tenth"
        " of its value at 130)",
        0 < v_near < 0.1 * v_far,
        f"S = 130: {v_far:.2f}; S = 91: {v_near:.2f}",
    )
    v_uo = vega(PRICER.up_out_call, 115.0, K, 120.0, T)
    report.ok(
        "up-and-out call (K = 100, H = 120) near the barrier (S = 115): negative vega",
        v_uo < 0,
        f"{v_uo:.2f}; value {PRICER.up_out_call(115.0, K, 120.0, T):.4f}",
    )


def check_asian(report: CheckReport, seeds: Iterator[int], c: float) -> None:
    """Check Asian options by the geometric closed form, a control variate and the limit.

    Args:
        report: The run's report.
        seeds: The run's seed sequence; this part takes its next seed.
        c: The vanilla call of the inputs, from part 1.
    """
    print("== Asian options (12 monthly averaging dates, S0 excluded)")
    n = N_DATES
    mu_g = math.log(S0) + (r - q - sg**2 / 2) * T * (n + 1) / (2 * n)
    var_g = sg**2 * T * (n + 1) * (2 * n + 1) / (6 * n**2)
    geo_cf = PRICER.geometric_asian_call(mu_g, var_g, K, T)
    rng = np.random.default_rng(next(seeds))
    dta = T / n
    logS = np.log(S0) + np.cumsum(
        (r - q - sg**2 / 2) * dta + sg * math.sqrt(dta) * rng.standard_normal((M, n)), axis=1
    )
    geo_pay = math.exp(-r * T) * np.maximum(np.exp(logS.mean(axis=1)) - K, 0)
    ari_pay = math.exp(-r * T) * np.maximum(np.exp(logS).mean(axis=1) - K, 0)
    est, se = mc(geo_pay)
    report.ok(
        "geometric average call: discrete closed form against Monte Carlo within 3 s.e.",
        abs(est - geo_cf) <= 3 * se,
        f"{est:.4f} (s.e. {se:.4f}) against {geo_cf:.4f}",
    )
    b = np.cov(ari_pay, geo_pay)[0, 1] / geo_pay.var(ddof=1)
    ctrl = ari_pay - b * (geo_pay - geo_cf)
    a_est, a_se = mc(ari_pay)
    c_est, c_se = mc(ctrl)
    vr = ari_pay.var(ddof=1) / ctrl.var(ddof=1)
    report.ok(
        "arithmetic average call: variance-reduction factor of the geometric control above 10",
        vr > 10,
        f"{vr:.0f}",
    )
    report.ok(
        "controlled and uncontrolled estimates differ by less than 3 uncontrolled s.e.",
        abs(c_est - a_est) < 3 * a_se,
        f"{a_est:.4f} (s.e. {a_se:.4f}) and {c_est:.4f} (s.e. {c_se:.5f}), b = {b:.4f}",
    )
    report.ok(
        "arithmetic >= geometric (AM-GM); with these inputs (positive carry) both lie below the"
        " vanilla call",
        geo_cf < c_est < c,
        f"vanilla {c:.4f}",
    )
    # Continuous averaging as the limit n -> infinity: volatility sigma/sqrt(3), Wilmott's explicit
    # formula.
    mu_c = math.log(S0) + (r - q - sg**2 / 2) * T / 2
    var_c = sg**2 * T / 3
    cont = PRICER.geometric_asian_call(mu_c, var_c, K, T)

    # The discrete mean and variance differ from their limits by O(1/n), so the price converges
    # at first order: doubling the number of dates from 500 to 1,000 halves the gap (ratio in
    # [1.9, 2.1]).
    gaps = [PRICER.discrete_geometric_asian_call(nn, S0, K, T) - cont for nn in (12, 500, 1000)]
    report.ok(
        "discrete formula tends to the continuous one at first order in 1/n",
        1.9 <= gaps[1] / gaps[2] <= 2.1,
        f"gap {gaps[0]:.4f} at 12 dates, {gaps[1]:.5f} at 500, {gaps[2]:.5f} at 1,000",
    )
    q_kv = 0.5 * (r + q + sg**2 / 6)
    d1kv = (math.log(S0 / K) + (r - q_kv + sg**2 / 6) * T) / (sg / math.sqrt(3) * math.sqrt(T))
    kv = S0 * math.exp(-q_kv * T) * N(d1kv) - K * math.exp(-r * T) * N(
        d1kv - sg / math.sqrt(3) * math.sqrt(T)
    )
    report.ok(
        "continuous form equals Black-Scholes with sigma/sqrt(3) and yield (r + q + sigma^2/6)/2",
        abs(kv - cont) < 1e-12,
        f"{cont:.4f}",
    )
    q_w = q + sg**2 / 6
    d1w = (math.log(S0 / K) + (r - q_w + sg**2 / 6) * T) / (sg / math.sqrt(3) * math.sqrt(T))
    wil = S0 * math.exp(-q_w * T) * N(d1w) - K * math.exp(-r * T) * N(
        d1w - sg / math.sqrt(3) * math.sqrt(T)
    )
    report.ok(
        "a yield of q + sigma^2/6 alone (as printed in Wilmott's sec. 25.9.1 summary) does not"
        " reproduce it",
        abs(wil - cont) > 0.1,
        f"{wil:.4f}",
    )


def check_carry_ordering(report: CheckReport) -> None:
    """Check the Asian-against-vanilla ordering depends on carry, by a deterministic example.

    Args:
        report: The run's report.
    """
    print("== Asian against vanilla: the ordering depends on carry (deterministic counterexample)")
    # Averaging lowers dispersion but also moves the forward level: E[A] = S0 mean_i
    # e^((r - q) t_i). With q > r the average's forward is above the terminal forward, and for a
    # deep in-the-money call that effect dominates. Same 12 monthly dates, S0 excluded.
    # E[(A - K)+] >= E[A] - K bounds the arithmetic call below, model-free given E[A].
    n = N_DATES
    S0n, Kn, rn, qn, sgn, Tn = 100.0, 60.0, 0.02, 0.08, 0.20, 1.0
    d1n = (math.log(S0n / Kn) + (rn - qn + sgn**2 / 2) * Tn) / (sgn * math.sqrt(Tn))
    vanilla_n = S0n * math.exp(-qn * Tn) * N(d1n) - Kn * math.exp(-rn * Tn) * N(
        d1n - sgn * math.sqrt(Tn)
    )
    m_n = math.log(S0n) + (rn - qn - sgn**2 / 2) * Tn * (n + 1) / (2 * n)
    v_n = sgn**2 * Tn * (n + 1) * (2 * n + 1) / (6 * n**2)
    d2n = (m_n - math.log(Kn)) / math.sqrt(v_n)
    geo_n = math.exp(-rn * Tn) * (math.exp(m_n + v_n / 2) * N(d2n + math.sqrt(v_n)) - Kn * N(d2n))
    EA = S0n * sum(math.exp((rn - qn) * i * Tn / n) for i in range(1, n + 1)) / n
    ari_lb = math.exp(-rn * Tn) * (EA - Kn)
    report.ok(
        "S0 = 100, K = 60, r = 2, q = 8 percent: geometric Asian call and the arithmetic lower"
        " bound both exceed the vanilla call",
        vanilla_n < geo_n < ari_lb
        and abs(vanilla_n - 33.56113) < 5e-5
        and abs(geo_n - 35.76006) < 5e-5
        and abs(ari_lb - 36.08765) < 5e-5,
        f"vanilla {vanilla_n:.4f}, geometric {geo_n:.4f}, arithmetic >= {ari_lb:.4f}",
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    GBM with S0 = K = 100, r = 5 percent, q = 2 percent, sigma = 25 percent, T = 1. Every Monte
    Carlo check uses 100,000 paths sampled exactly on its dates; one seed sequence, 20261031
    onwards, is passed through parts 1 to 3, each check taking the next seed. Two deterministic
    checks qualify the entries: the cash digital's one-day delta is positive on both sides of the
    strike (its size, not its sign, changes near expiry), and with negative carry (q = 8 percent > r
    = 2 percent, K = 60) the Asian call is worth more than the vanilla, while arithmetic stays above
    geometric averaging throughout. Synthetic model data only.

    The Monte Carlo checks of parts 1 to 3 take their seeds, in order, from one sequence made here.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    seeds = iter(range(20261031, 20261040))
    c = check_digital(report, seeds)
    check_barrier(report, seeds, c)
    check_asian(report, seeds, c)
    check_carry_ordering(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
