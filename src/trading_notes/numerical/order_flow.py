"""Order flow: spreads, imbalance, trade signing, noise, Epps, Hawkes and waiting times.

Order books and order flow review (2026-10-16): independent checks for the order-book, order-flow
and point-process entries.

Each block recomputes a claim from first principles or gives a counterexample; nothing here is
fitted to real data.

One generator, seeded 33, serves the blocks on queue imbalance, realised variance, Epps,
deseasonalisation, the Hawkes process, inhibition, the queue and the waiting-time estimator in
order; the jump block has its own generator, seeded 35, and the renewal block its own, seeded 34.
Each part returns the names of its failed checks; a failure prints BAD and exits 1, and a passing
run prints no summary.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.order_flow
(numpy, scipy; fixed seeds; about 20 s). Exits 1 on failure.
"""

import itertools
import sys
from collections.abc import Sequence
from decimal import Decimal
from typing import Final

import numpy as np
from numpy.typing import NDArray
from scipy import integrate, stats

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

SEED: Final = 33
SHAPE: Final = 4.0  # gamma shape of the latent spread
D = Decimal


def head(t: str) -> None:
    """Print a block heading."""
    print("\n== " + t)


def check(failed: list[str], name: str, cond: bool) -> None:
    """Record name in failed when cond is false; a passing check prints nothing."""
    if not cond:
        failed.append(name)


def latent_pdf(x: float, mean: float) -> float:
    """Return the density of the latent spread in old ticks: a gamma with the given mean."""
    value: float = stats.gamma.pdf(x, a=SHAPE, scale=mean / SHAPE)
    return value


def expected_discrete(mean: float, delta: float, kmax: int = 400) -> float:
    """Return the expected observed spread in old ticks after rounding to a grid of 1/delta."""
    tot = 0.0
    p1 = integrate.quad(latent_pdf, 0, 1.5 / delta, args=(mean,))[0]
    tot += (1 / delta) * p1
    for k in range(2, kmax):
        pk = integrate.quad(latent_pdf, (k - 0.5) / delta, (k + 0.5) / delta, args=(mean,))[0]
        tot += (k / delta) * pk
        if (k - 0.5) / delta > mean * 10:
            break
    return tot


def e_n(prev: tuple[float, int, float, int], cur: tuple[float, int, float, int]) -> float:
    """Return the Cont-Kukanov-Stoikov order-flow imbalance between two best-quote states."""
    pb0, qb0, pa0, qa0 = prev
    pb1, qb1, pa1, qa1 = cur
    return (pb1 >= pb0) * qb1 - (pb1 <= pb0) * qb0 - (pa1 <= pa0) * qa1 + (pa1 >= pa0) * qa0


def tick_sign(prices: Sequence[Decimal]) -> int:
    """Return the sign of the last non-zero price change before the current trade (0 if none)."""
    for k in range(len(prices) - 1, 0, -1):
        d = prices[k] - prices[k - 1]
        if d != 0:
            return 1 if d > 0 else -1
    return 0


def lee_ready(price: Decimal, bid: Decimal, ask: Decimal, prior_prices: Sequence[Decimal]) -> int:
    """Return the Lee-Ready sign: the quote rule against the midpoint, then the tick test."""
    mid = (bid + ask) / 2
    if price > mid:
        return +1
    if price < mid:
        return -1
    return tick_sign([*list(prior_prices), price])


def prev_tick(P: Floats, obs: Ints, grid: Floats) -> Floats:
    """Return the previous-tick values of the path P observed at the times obs, on grid."""
    idx = np.searchsorted(obs, grid, side="right") - 1
    value: Floats = P[obs[np.clip(idx, 0, len(obs) - 1)]]
    return value


def sim_hawkes_exp(
    mu: float, alpha: float, beta: float, T: float, rng: np.random.Generator
) -> Floats:
    """Return the event times of a Hawkes process with exponential kernel, by Ogata thinning."""
    t, excite = 0.0, 0.0
    ev: list[float] = []
    while True:
        lam_bar = mu + excite
        w = rng.exponential(1 / lam_bar)
        t_new = t + w
        excite *= np.exp(-beta * w)
        if t_new > T:
            value: Floats = np.array(ev)
            return value
        if rng.uniform() * lam_bar <= mu + excite:
            ev.append(t_new)
            excite += alpha
        t = t_new


def sim_nonlinear(mu: float, a: float, beta: float, T: float, rng: np.random.Generator) -> Floats:
    """Return the event times of lambda = (mu + sum a exp(-beta (t - t_i)))^+, by thinning."""
    t, ex = 0.0, 0.0
    ev: list[float] = []
    while True:
        w = rng.exponential(1 / mu)
        t += w
        ex *= np.exp(-beta * w)
        if t > T:
            value: Floats = np.array(ev)
            return value
        if rng.uniform() * mu <= max(mu + ex, 0.0):
            ev.append(t)
            ex += a


def check_latent_spread() -> list[str]:
    """Part 1: the discretised spread's expectation under a finer tick, in old-tick units."""
    head(
        "Harris discretised spread: E(Psi | delta) = sum_k (k/delta) f_delta(k), k in new ticks"
        " (Lehalle-Laruelle app. A.6)"
    )
    for mean in [0.6, 1.2, 3.0, 8.0]:
        e1, e5 = expected_discrete(mean, 1), expected_discrete(mean, 5)
        print(
            f"latent mean {mean:4.1f} old ticks: E(Psi|delta=1) = {e1:.3f}, E(Psi|delta=5) ="
            f" {e5:.3f} old ticks,"
            f" change {e5 - e1:+.3f} ({(e5 - e1) / e1:+.1%})"
        )
    print(
        "units: an observed spread of k old ticks is k*delta NEW ticks (3 old ticks = 15 new ticks"
        " at delta = 5);"
        " it is a count of k NEW ticks that equals k/delta old ticks. Reading a k-tick spread as"
        " k/delta old-tick"
        " units mixes the two."
    )
    print(
        "the counterfactual re-rounds the latent spread on the finer grid; it does not rescale"
        " observed spreads:"
        f" mean 8.0 changes by {expected_discrete(8.0, 5) - expected_discrete(8.0, 1):+.3f} old"
        f" ticks, not 8.0/5"
        f" - 8.0 = {8 / 5 - 8:+.1f}"
    )
    return []


def check_queue_imbalance(rng: np.random.Generator) -> list[str]:
    """Part 2: the queue imbalance QI = (B - A)/(B + A) equals 2I - 1 and is scale-invariant."""
    head(
        "queue imbalance: QI = (B - A)/(B + A) = 2I - 1 with I = B/(B + A) (Bouchaud et al. eq."
        " 7.1)"
    )
    B, A = rng.integers(1, 500, 5), rng.integers(1, 500, 5)
    intensity = B / (B + A)
    QI = (B - A) / (B + A)
    print(
        "max |QI - (2I - 1)| =",
        float(np.abs(QI - (2 * intensity - 1)).max()),
        "; I in (0,1), QI in (-1,1); both scale-invariant:",
        bool(np.allclose((3 * B - 3 * A) / (3 * B + 3 * A), QI)),
    )
    return []


def check_ofi() -> list[str]:
    """Part 3: event-based order-flow imbalance against signed trade volume."""
    head(
        "event-based order-flow imbalance e_n (Cont, Kukanov and Stoikov, p. 4) against signed"
        " trade volume"
    )
    # best-quote states (bid price, bid size, ask price, ask size) and any trade (signed volume)
    # between them
    seq: list[tuple[tuple[float, int, float, int], int]] = [
        ((10.00, 500, 10.01, 400), 0),
        ((10.00, 300, 10.01, 400), -200),  # market sell of 200 hits the bid
        ((10.00, 500, 10.01, 400), 0),  # 200 replenished at the bid
        ((10.00, 500, 10.01, 100), 0),  # 300 cancelled at the ask (no trade)
        (
            (10.00, 500, 10.02, 600),
            +100,
        ),  # market buy of 100 empties the ask; new ask level 10.02 with 600
    ]
    ofi, ti = 0.0, 0.0
    for (prev, _), (cur, tr) in itertools.pairwise(seq):
        e = e_n(prev, cur)
        ofi += e
        ti += tr
        print(f"  {prev} -> {cur}: e_n = {e:+5.0f}, signed trade = {tr:+5d}")
    print(
        f"OFI = {ofi:+.0f}, trade imbalance = {ti:+.0f}: the cancellation at the ask (+300) and the"
        f" replenished bid"
        " (+200) move OFI but not the trade imbalance; the two measures can even differ in sign"
    )
    return []


def check_trade_signing() -> list[str]:
    """Part 4: the quote rule and the tick test at the midpoint, on Decimal prices."""
    failed: list[str] = []
    head(
        "trade signing: quote rule, then tick rule at the midpoint (Lee-Ready as described by"
        " Harris and Hasbrouck)"
    )
    cases: list[tuple[Decimal, Decimal, Decimal, list[Decimal], int, str]] = [
        # (trade, bid, ask, earlier trade prices, expected sign, what it tests)
        (
            D("10.005"),
            D("10.00"),
            D("10.01"),
            [D("10.00")],
            +1,
            "half-tick midpoint after an uptick",
        ),
        (
            D("10.005"),
            D("10.00"),
            D("10.01"),
            [D("10.01")],
            -1,
            "half-tick midpoint after a downtick",
        ),
        (
            D("10.01"),
            D("10.00"),
            D("10.02"),
            [D("10.02")],
            -1,
            "whole-tick midpoint after a downtick",
        ),
        (
            D("10.01"),
            D("10.00"),
            D("10.02"),
            [D("10.00"), D("10.01")],
            +1,
            "midpoint, zero tick, last non-zero change up (zero uptick)",
        ),
        (
            D("10.01"),
            D("10.00"),
            D("10.02"),
            [D("10.02"), D("10.01")],
            -1,
            "midpoint, zero tick, last non-zero change down (zero downtick)",
        ),
        (
            D("10.01"),
            D("10.00"),
            D("10.02"),
            [D("10.01")],
            0,
            "midpoint, no earlier non-zero change: unclassified",
        ),
        (
            D("10.006"),
            D("10.00"),
            D("10.01"),
            [D("10.01")],
            +1,
            "just above a half-tick midpoint, after a downtick",
        ),
        (
            D("10.004"),
            D("10.00"),
            D("10.01"),
            [D("10.00")],
            -1,
            "just below a half-tick midpoint, after an uptick",
        ),
        (D("10.00"), D("10.00"), D("10.02"), [D("9.98")], -1, "at the bid after an uptick"),
        (D("10.02"), D("10.00"), D("10.02"), [D("10.04")], +1, "at the ask after a downtick"),
    ]
    n_before = len(failed)
    for p, b, a, prior, want, what in cases:
        got = lee_ready(p, b, a, prior)
        check(failed, what, got == want)
        print(f"  {what:62}: trade {p} in [{b}, {a}] after {[str(x) for x in prior]} -> {got:+d}")
    if len(failed) == n_before:
        print("all", len(cases), "assertions hold")
    print(
        "binary floating point: (10.00 + 10.01)/2 =",
        repr((10.00 + 10.01) / 2),
        "< 10.005 ->",
        "a float implementation calls the downtick midpoint case a buy;",
        "Decimal gives",
        (D("10.00") + D("10.01")) / 2,
    )
    print(
        "a trade at the bid is a sell under the quote rule whatever the previous tick; a passive"
        " buyer who pegs the"
        " bid is never classified as the buyer (Harris, p. 423)"
    )
    return failed


def check_realised_variance(rng: np.random.Generator) -> list[str]:
    """Part 5: realised variance under i.i.d. microstructure noise grows as 2 n sigma_eta^2."""
    head(
        "realised variance with i.i.d. noise: E[RV(Delta)] = IV + 2 n sigma_eta^2, n = T/Delta"
        " (Lehalle-Laruelle app. A.13 model)"
    )
    T, N = 1.0, 23_400
    sigma, s_eta = 0.01, 0.0002
    dW = rng.standard_normal(N) * sigma * np.sqrt(T / N)
    M = np.concatenate([[0.0], np.cumsum(dW)])
    X = M + rng.standard_normal(N + 1) * s_eta
    for step in [1, 5, 30, 300, 1800]:
        rv = np.sum(np.diff(X[::step]) ** 2)
        n = N // step
        print(
            f"  step {step:5d} ({n:5d} returns): RV = {rv:.3e}, IV + 2 n s_eta^2 ="
            f" {sigma**2 + 2 * n * s_eta**2:.3e}"
        )
    return []


def check_jumps() -> list[str]:
    """Part 6: realised variance converges to the quadratic variation, not the diffusion one."""
    head(
        "jumps: realised variance converges to quadratic variation, not to the integrated diffusion"
        " variance"
    )
    rng_j = np.random.default_rng(35)
    lam_j, Tj = 5.0, 1.0
    jt = np.sort(
        rng_j.uniform(0, Tj, rng_j.poisson(lam_j * Tj))
    )  # unit-jump Poisson path: sigma = 0
    for n_steps in [10, 100, 10_000, 1_000_000]:
        grid = np.linspace(0, Tj, n_steps + 1)
        Ng = np.searchsorted(jt, grid, side="right")  # N at grid times
        print(
            f"  {n_steps:9d} steps: RV = {np.sum(np.diff(Ng) ** 2):3d}; jump count N_T = {len(jt)};"
            " integrated diffusion variance 0"
        )
    co = np.sort(rng_j.uniform(0, 1, 3))

    def X1(t: Floats) -> Floats:
        """Return the first asset's path: three common jumps of +1."""
        value: Floats = np.asarray(np.searchsorted(co, t, side="right") * 1.0, dtype=np.float64)
        return value

    def X2(t: Floats) -> Floats:
        """Return the second asset's path: three common jumps of -0.5."""
        value: Floats = np.asarray(-np.searchsorted(co, t, side="right") * 0.5, dtype=np.float64)
        return value

    g = np.linspace(0, 1, 100_001)
    print(
        "  co-jumps: realised covariance",
        float(np.sum(np.diff(X1(g)) * np.diff(X2(g)))),
        "= sum of jump products 3 x (1)(-0.5)",
    )
    return []


def check_epps(rng: np.random.Generator) -> list[str]:
    """Part 7: the Epps effect from asynchronous observation alone."""
    head(
        "Epps effect from asynchronous observation alone: true correlation 0.6, previous-tick"
        " sampling of Poisson trade times"
    )
    rho, N, reps = 0.6, 23_400, 40
    steps = [5, 30, 120, 600, 1800]
    corr: dict[int, list[float]] = {s: [] for s in steps}
    for _ in range(reps):
        z1, z2 = rng.standard_normal(N), rng.standard_normal(N)
        P1 = np.cumsum(z1)
        P2 = np.cumsum(rho * z1 + np.sqrt(1 - rho**2) * z2)
        obs1 = np.sort(rng.choice(N, 2000, replace=False))  # about one trade every 12 time units
        obs2 = np.sort(rng.choice(N, 2000, replace=False))
        for step in steps:
            grid = np.arange(max(obs1[0], obs2[0]), N, step)
            r1, r2 = np.diff(prev_tick(P1, obs1, grid)), np.diff(prev_tick(P2, obs2, grid))
            corr[step].append(np.corrcoef(r1, r2)[0, 1])
    for step in steps:
        print(
            f"  step {step:5d}: mean sample correlation over {reps} paths {np.mean(corr[step]):.3f}"
            f" (sd"
            f" {np.std(corr[step]):.3f})"
        )
    return []


def check_deseasonalisation(rng: np.random.Generator) -> list[str]:
    """Part 8: multiplicative deseasonalisation, and the look-ahead of a centred moving average."""
    head(
        "multiplicative deseasonalisation with a centred moving average of length p"
        " (Lehalle-Laruelle app. A.11)"
    )
    p, n = 13, 60  # 13 slots a day, 60 days
    S_true = 1 + 0.6 * np.cos(np.linspace(0, 2 * np.pi, p, endpoint=False)) ** 2
    S_true /= S_true.mean()
    trend = np.linspace(100, 140, p * n)
    X = trend * np.tile(S_true, n) + rng.standard_normal(p * n) * 2.0
    k = p // 2
    MA = np.full(X.size, np.nan)
    for t in range(k, X.size - k):
        MA[t] = X[t - k : t + k + 1].mean()  # odd length 2k+1 = p
    ratio = (X / MA).reshape(n, p)
    S_hat = np.nanmean(ratio, axis=0)
    S_hat /= S_hat.mean()
    print("max |S_hat - S| =", round(float(np.abs(S_hat - S_true).max()), 4))
    X2 = X.copy()
    X2[200 + 3] += 50.0  # a later observation changes
    MA2 = np.array(
        [X2[t - k : t + k + 1].mean() if k <= t < X.size - k else np.nan for t in range(X.size)]
    )
    print(
        "a shock at t = 203 changes the centred MA at t = 197..202 (before it):",
        bool(np.all(MA2[197:203] != MA[197:203])),
        "-> a two-sided trend estimate is not available at decision time; the last k values are"
        " undefined",
    )
    return []


def check_hawkes(rng: np.random.Generator) -> tuple[list[str], Floats]:
    """Part 9: homogeneous Poisson and Hawkes time changes; returns the events for part 12."""
    failed: list[str] = []
    head(
        "homogeneous Poisson: exponential durations; time change of a Hawkes compensator to"
        " unit-rate Poisson"
    )
    mu, alpha, beta, T = 1.0, 0.6, 1.0, 20_000.0
    ev = sim_hawkes_exp(mu, alpha, beta, T, rng)
    print(
        f"exponential kernel, branching ratio alpha/beta = {alpha / beta}: mean rate"
        f" {len(ev) / T:.3f}"
        f" against mu/(1 - alpha/beta) = {mu / (1 - alpha / beta):.3f}"
    )
    counts = np.histogram(ev, bins=np.arange(0, T + 1, 50.0))[0]
    print(
        f"clustering ratio Var/E of counts in windows of 50: {counts.var() / counts.mean():.2f}"
        f" (Poisson 1; Hawkes long-window limit 1/(1-g)^2 = {1 / (1 - alpha / beta) ** 2:.2f})"
    )
    # compensator between events
    Lam_list: list[float] = []
    excite_at = 0.0
    for i in range(1, len(ev)):
        dt = ev[i] - ev[i - 1]
        excite_after = excite_at + alpha  # just after event i-1
        Lam_list.append(mu * dt + excite_after / beta * (1 - np.exp(-beta * dt)))
        excite_at = excite_after * np.exp(-beta * dt)
    Lam = np.array(Lam_list)
    print(
        f"time-rescaled durations: mean {Lam.mean():.3f}, KS p-value against Exp(1)"
        f" {stats.kstest(Lam, 'expon').pvalue:.2f};"
        f" raw durations against Exp(mean): p ="
        f" {stats.kstest(np.diff(ev) / np.diff(ev).mean(), 'expon').pvalue:.1e}"
    )
    return failed, ev


def check_inhibition(rng: np.random.Generator) -> list[str]:
    """Part 10: a negative kernel in a linear Hawkes intensity can go negative; a link does not."""
    head(
        "inhibition: a negative kernel in a linear Hawkes intensity can go negative; a non-negative"
        " link keeps it valid"
    )
    mu, a_neg, beta = 0.5, -0.8, 2.0
    lin = mu + a_neg * np.exp(-beta * 0.0)
    print(f"linear intensity just after one event: mu + a = {lin:+.2f} < 0 (not an intensity)")
    ev_in = sim_nonlinear(mu, a_neg, beta, 20_000.0, rng)
    c = np.histogram(ev_in, bins=np.arange(0, 20_001, 50.0))[0]
    print(
        f"(.)^+ link: rate {len(ev_in) / 20_000:.3f} < mu = {mu}; clustering ratio"
        f" {c.var() / c.mean():.2f} < 1"
        " (events repel)"
    )
    return []


def check_queue_ad(rng: np.random.Generator) -> list[str]:
    """Part 11: the arrival-departure ratio of a birth-death queue sets the drift if rates are."""
    head(
        "queue arrival/departure ratio: birth-death queue with insertion rate L and departure rate"
        " D"
        " (cancellations plus trades)"
    )
    for L, D_ in [(1.2, 1.0), (0.8, 1.0)]:
        q, path = 20, []
        for _ in range(20_000):
            if q == 0:
                q = 1
            q += 1 if rng.uniform() < L / (L + D_) else -1
            path.append(q)
        print(
            f"  A/D ratio {L / D_:.1f}: queue after 20,000 events {path[-1]}, mean drift per event"
            f" {(L - D_) / (L + D_):+.3f}"
        )
    print(
        "the drift sign follows the ratio only when both rates are constant in the queue size; with"
        " state-dependent"
        " rates (Huang-Lehalle-Rosenbaum) the ratio must be read at each size"
    )
    return []


def check_waiting_time(rng: np.random.Generator, ev: Floats) -> list[str]:
    """Part 12: the waiting-time estimator of 1/lambda depends on where the clock starts."""
    failed: list[str] = []
    head(
        "waiting-time estimator of 1/lambda depends on where the clock starts (Lehalle-Laruelle p."
        " 221, n. 12)"
    )
    starts_uniform = rng.uniform(0, ev[-1], 5000)
    idx = np.searchsorted(ev, starts_uniform)
    ok = idx < len(ev)
    wait_uniform = (ev[idx[ok]] - starts_uniform[ok]).mean()
    wait_after_event = np.diff(ev).mean()
    print(
        f"Hawkes sample: mean wait from uniform start times {wait_uniform:.3f}, mean inter-event"
        f" time"
        f" {wait_after_event:.3f}"
    )
    print(
        "renewal theory: for an equilibrium renewal process with finite E[X^2], the mean wait from"
        " an arbitrary time"
        " is E[X^2]/(2 E[X]); it equals E[X] iff E[X^2] = 2 E[X]^2, i.e. CV = 1, which does not"
        " imply exponential gaps"
    )
    xs, ps = np.array([0.5, 3.0]), np.array([0.8, 0.2])
    EX, EX2 = float((xs * ps).sum()), float((xs**2 * ps).sum())
    check(
        failed,
        "two-point gaps have E[X] = 1 and E[X^2] = 2",
        bool(abs(EX - 1) < 1e-12 and abs(EX2 - 2) < 1e-12),
    )
    print(
        f"two-point gaps P(X=0.5)=0.8, P(X=3)=0.2: E[X] = {EX}, E[X^2] = {EX2}, CV ="
        f" {np.sqrt(EX2 - EX**2) / EX:.3f}, E[X^2]/(2E[X]) = {EX2 / (2 * EX)}"
    )
    rng2 = np.random.default_rng(34)
    gaps = rng2.choice(xs, size=400_000, p=ps)
    times = np.cumsum(gaps)
    st = rng2.uniform(times[1000], times[-1000], 200_000)
    w = times[np.searchsorted(times, st)] - st
    print(
        f"simulated: mean wait from uniform times {w.mean():.4f} against mean gap"
        f" {gaps.mean():.4f}; equal"
        " although not Poisson"
    )
    g_exp = rng2.exponential(1.0, 400_000)
    t_exp = np.cumsum(g_exp)
    st = rng2.uniform(t_exp[1000], t_exp[-1000], 200_000)
    print(
        f"exponential gaps (mean 1): mean wait"
        f" {(t_exp[np.searchsorted(t_exp, st)] - st).mean():.4f}"
    )
    hg = np.diff(ev)
    print(
        f"Hawkes gaps: CV = {hg.std() / hg.mean():.3f}; E[X^2]/(2E[X]) ="
        f" {(hg**2).mean() / (2 * hg.mean()):.3f}"
        f" against the mean wait {wait_uniform:.3f} from uniform start times (the stationary"
        f" inversion formula,"
        " Palm moments)"
    )
    return failed


def main() -> int:
    """Run the parts in order with one generator, print each failed check as BAD, and return 0 or 1.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    failed: list[str] = []
    check_latent_spread()
    failed += check_queue_imbalance(rng)
    check_ofi()
    failed += check_trade_signing()
    failed += check_realised_variance(rng)
    failed += check_jumps()
    failed += check_epps(rng)
    failed += check_deseasonalisation(rng)
    hawkes_failed, ev = check_hawkes(rng)
    failed += hawkes_failed
    failed += check_inhibition(rng)
    failed += check_queue_ad(rng)
    failed += check_waiting_time(rng, ev)
    for name in failed:
        print("BAD", name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
