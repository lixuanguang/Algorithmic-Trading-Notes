"""Order routing and fragmentation: auctions, pro-rata fills, posting, venue shares, SOR learning.

Order matching and fragmentation review (2026-10-16): independent checks for the order-instruction,
matching, dark-trading and fragmentation entries.

Each block recomputes a source's example or a derived claim from first principles, or gives a
counterexample.

One generator, seeded 34, serves the Gini, Kolmogorov-Smirnov and learner blocks in order (the
learner block through its own helpers); the posting block has its own generator, seeded 341, and the
venue-share block its own, seeded 342, and the learner's draws come from the generator seeded 343.
Each part returns the names of its failed checks; a failure prints BAD and exits 1, and a passing
run prints no summary.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.order_routing_fragmentation
(numpy, scipy; fixed seeds; a few seconds). Exits 1 on failure.
"""

# standard library imports
import sys
from fractions import Fraction as Fr
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray
from scipy import stats

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

SEED: Final = 34
K: Final = 3  # venues in the learner
NU: Final = 0.8  # log-normal spread of the learner's venue draws
INF: Final = 10**6


def head(t: str) -> None:
    """Print a block heading."""
    print("\n== " + t)


def check(failed: list[str], name: str, cond: bool) -> None:
    """Record name in failed when cond is false; a passing check prints nothing."""
    if not cond:
        failed.append(name)


def pro_rata(Q: int, resting: list[int]) -> tuple[int, list[Fr], list[int], int, int]:
    """Return the executable quantity, exact and floored shares, rounding remainder and residual.

    Executable quantity is capped by eligible resting liquidity; shares are proportional to size;
    floors leave a rounding remainder for a venue rule; any excess of Q over the liquidity is the
    incoming order's residual.
    """
    E = min(Q, sum(resting))
    exact = [Fr(E * q, sum(resting)) for q in resting]
    floors = [int(x) for x in exact]
    rounding = E - sum(floors)
    residual = Q - E
    assert all(f <= q for f, q in zip(floors, resting)), "no order fills beyond its size"
    assert sum(floors) + rounding + residual == Q, "quantity conserved"
    assert sum(floors) + rounding <= sum(resting), "capacity respected"
    return E, exact, floors, rounding, residual


def outcomes(
    ask0: float, bid0: float, filled: bool, chase_price: float | None, mark: float
) -> tuple[float, float, float]:
    """Return the crossing and posting outcomes of buying one unit by the horizon.

    Crossing pays ask0 now. Posting pays bid0 if filled, otherwise buys at the horizon at
    chase_price. Both end long one unit, marked at the same terminal price.
    """
    cross = mark - ask0
    if filled:
        post = mark - bid0
    elif chase_price is None:
        raise ValueError("a missed order needs a chase price")
    else:
        post = mark - chase_price
    return cross, post, post - cross


def ex_fixing(M: float, m: float, p: float) -> float:
    """Return the ex-fixing share (M - m p)/(1 - p) of a venue with share M and fixing share m."""
    assert 0 <= p < 1 and 0 <= m <= 1 and m * p <= M <= m * p + (1 - p), "shares must be feasible"
    return (M - m * p) / (1 - p)


def gini(x: Floats) -> float:
    """Return the Gini coefficient from the Lorenz curve, G = 1 - 2 int L."""
    x = np.sort(np.asarray(x, float))
    L = np.concatenate([[0], np.cumsum(x) / x.sum()])
    u = np.linspace(0, 1, len(L))
    value: float = 1 - 2 * np.trapezoid(L, u)
    return value


def gini_mean_diff(x: Floats) -> float:
    """Return the Gini coefficient as half the relative mean difference."""
    x = np.asarray(x, float)
    value: float = np.abs(x[:, None] - x[None, :]).sum() / (2 * len(x) ** 2 * x.mean())
    return value


def var_diff(w: Floats, sig2: Floats, k: int, cov: Floats | None = None) -> float:
    """Return Var(p_hat_k - sum_j w_j p_hat_j) for independent or covariance-given shares."""
    a = -np.asarray(w, float)
    a[k] += 1.0  # p_hat_k - sum_j w_j p_hat_j
    C = np.diag(sig2) if cov is None else np.asarray(cov)
    return float(a @ C @ a)


def project_simplex(v: Floats) -> Floats:
    """Return the Euclidean projection of v onto the probability simplex."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    value: Floats = np.maximum(v - (css[rho] - 1) / (rho + 1), 0)
    return value


def draw_D(rng: np.random.Generator, mu: Floats, size: int) -> Floats:
    """Return venue depths D with mean mu, log-normal around it (sd proportional to the mean)."""
    value: Floats = mu * np.exp(rng.normal(-(NU**2) / 2, NU, (size, K)))
    return value


def calibrate(
    rng: np.random.Generator, p_target: Floats, iters: int = 60, size: int = 40_000
) -> tuple[Floats, Floats]:
    """Return the venue means giving target shares E[D_k / sum D], and the shares achieved."""
    mu = p_target.copy()
    Z = rng.normal(-(NU**2) / 2, NU, (size, K))
    D: Floats = mu * np.exp(Z)
    for _ in range(iters):
        D = mu * np.exp(Z)
        share = (D / D.sum(1, keepdims=True)).mean(0)
        mu = mu * p_target / share
        mu = mu / mu.sum()
    achieved: Floats = (D / D.sum(1, keepdims=True)).mean(0)
    return mu, achieved


def learn(
    rng: np.random.Generator,
    r: Floats,
    mu: Floats,
    n_draws: int,
    gamma0: float = 0.02,
    tau: int = 300,
) -> tuple[Floats, Floats]:
    """Return the last and the average keys of projected stochastic gradient ascent.

    The objective is E[sum min(r_k V, D_k)] with decreasing steps; the average key is over the
    second half.
    """
    D = draw_D(rng, mu, n_draws)
    V = np.exp(rng.normal(-0.02, 0.2, n_draws)) * mu.sum()  # independent of D, E[V] ~ sum E[D]
    acc = np.zeros(K)
    for i, (d, v) in enumerate(zip(D, V)):
        g = v * (r * v < d) / mu.sum()  # stochastic gradient, scaled by order size
        r = project_simplex(r + gamma0 / (1 + i / tau) * (g - g.mean()))
        if i >= n_draws // 2:
            acc += r
    return r, acc / (n_draws - n_draws // 2)


def optimum(
    rng: np.random.Generator, mu: Floats, n: int = 100_000
) -> tuple[Floats, Floats, float, float]:
    """Return the exact KKT solution on a sample: keys, marginal values, capture and the multiplier.

    Each r_k solves h_k(r_k) = E[V 1{r_k V < D_k}] = lam (h_k decreasing in r_k), r_k = 0 if h_k(0)
    <= lam, and lam is set by bisection so that the keys sum to one.
    """
    D = draw_D(rng, mu, n)
    V = np.exp(rng.normal(-0.02, 0.2, n)) * mu.sum()
    ratio = D / V[:, None]  # r_k V < D_k  <=>  r_k < D_k / V

    def key(k: int, lam: float) -> float:
        """Return the key of venue k at multiplier lam: first breakpoint where h_k drops to lam."""
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
        tot = sum(key(k, lam) for k in range(K))
        lo, hi = (lam, hi) if tot > 1 else (lo, lam)
    r = np.array([key(k, lam) for k in range(K)])
    r = r / r.sum()
    g = (V[:, None] * (r * V[:, None] < D)).mean(0)
    capture: float = np.minimum(r * V[:, None], D).sum(1).mean()
    return r, g, capture, lam


def check_single_price_auction() -> list[str]:
    """Part 1: the single-price auction on Harris's Table 6-1 orders: price, volume and surplus."""
    failed: list[str] = []
    head(
        "single-price auction on Harris's Table 6-1 orders (chap. 6, pp. 118-125): clearing price,"
        " volume, surplus"
    )
    buys: list[tuple[str, int, Fr | None]] = [
        ("Bea", 3, Fr("20.0")),
        ("Ben", 2, Fr("20.0")),
        ("Bif", 4, None),
        ("Bob", 2, Fr("20.1")),
        ("Bud", 7, Fr("19.8")),
    ]
    sells: list[tuple[str, int, Fr]] = [
        ("Sam", 2, Fr("20.1")),
        ("Sol", 1, Fr("19.8")),
        ("Stu", 5, Fr("20.2")),
        ("Sue", 6, Fr("20.0")),
    ]
    prices = sorted({p for *_, p in buys + sells if p is not None})

    def demand(p: Fr) -> int:
        """Return the buy quantity at price p: market orders and limits at or above p."""
        return sum(q for _, q, lim in buys if lim is None or lim >= p)

    def supply(p: Fr) -> int:
        """Return the sell quantity at price p: limits at or below p."""
        return sum(q for _, q, lim in sells if lim <= p)

    rows = [
        (p, demand(p), supply(p), min(demand(p), supply(p)), demand(p) - supply(p)) for p in prices
    ]
    for p, d, s_, m, e in rows:
        print(
            f"  p={float(p):5.1f}: demand {d:2d} supply {s_:2d} matched {m:2d} excess demand {e:+d}"
        )
    mx = max(r[3] for r in rows)
    cands = [r for r in rows if r[3] == mx]
    surplus_min = min(abs(r[4]) for r in cands)
    cands = [r for r in cands if abs(r[4]) == surplus_min]
    print(
        "rule 1 (maximum volume) and rule 2 (minimum surplus) leave",
        [float(r[0]) for r in cands],
        "with volume",
        mx,
    )
    check(
        failed,
        "clearing price 20.0 with volume 7",
        bool([float(r[0]) for r in cands] == [20.0] and mx == 7),
    )
    # surplus: valuations = limit prices, market buyer valued at 20.3 (Harris's assumption)
    val = {n: (lim if lim is not None else Fr("20.3")) for n, _, lim in buys + sells}
    uniform_trades = [("Sol", "Bif", 1), ("Sue", "Bif", 3), ("Sue", "Bob", 2), ("Sue", "Bea", 1)]
    s_uniform = sum((val[b] - val[s]) * q for s, b, q in uniform_trades)
    cont_trades = [
        ("Sol", "Bea", Fr("20.0"), 1),
        ("Sam", "Bif", Fr("20.1"), 2),
        ("Stu", "Bif", Fr("20.2"), 2),
        ("Sue", "Bob", Fr("20.1"), 2),
        ("Sue", "Bea", Fr("20.0"), 2),
        ("Sue", "Ben", Fr("20.0"), 2),
    ]
    s_cont = sum((val[b] - val[s]) * q for s, b, _, q in cont_trades)
    print(
        f"total surplus: single price {float(s_uniform):.1f} on 7 units; continuous"
        f" {float(s_cont):.1f} on 11"
        " units (Harris Tables 6-7 and 6-9: 1.6 and 1.0); the surplus of a trade does not depend on"
        " its price"
    )
    check(
        failed,
        "surplus 1.6 at a single price and 1.0 continuous",
        bool(s_uniform == Fr("1.6") and s_cont == Fr("1.0")),
    )
    bif_cont = (Fr("20.1") * 2 + Fr("20.2") * 2) / 4
    print(
        f"Bif's average price: discriminatory {float(bif_cont):.2f} against 20.2 if his order alone"
        f" set a uniform"
        " price (Harris p. 128); Sue's average 20.033 against 20.0"
    )
    return failed


def check_pro_rata() -> list[str]:
    """Part 2: pro-rata allocation with capacity, rounding and the incoming residual."""
    failed: list[str] = []
    head(
        "pro-rata allocation (corrected 2026-10-16): capacity first, then proportional shares,"
        " rounding remainder,"
        " incoming residual"
    )
    cases: list[tuple[str, int, list[int]]] = [
        ("Harris p. 117", 18, [10, 20]),
        ("undersubscribed, fractional", 10, [4, 4, 4]),
        ("equal", 12, [4, 4, 4]),
        ("oversubscribed", 10, [3, 3, 3]),
        ("small orders", 7, [1, 1, 100]),
    ]
    for name, Q, rest in cases:
        E, exact, floors, rounding, residual = pro_rata(Q, rest)
        print(
            f"  {name:28} Q={Q:2d} vs {rest}: executable {E}, exact {[str(x) for x in exact]},"
            f" floors {floors},"
            f" rounding remainder {rounding} (venue rule), unexecuted incoming residual {residual}"
        )
    check(
        failed,
        "pro-rata: 10 against 3, 3, 3 gives floors 3, 3, 3 with residual 1",
        bool(pro_rata(10, [3, 3, 3])[1:] == ([Fr(3), Fr(3), Fr(3)], [3, 3, 3], 0, 1)),
    )
    check(
        failed,
        "pro-rata: 10 against 4, 4, 4 leaves rounding 1 and residual 0",
        bool(pro_rata(10, [4, 4, 4])[3:] == (1, 0)),
    )
    print(
        "POSIT example (p. 134): sell 3,000 against buys 5,000 and 10,000 ->",
        pro_rata(3000, [5000, 10000])[2],
    )
    return failed


def check_posting() -> list[str]:
    """Part 3: posting against crossing, with explicit cash flows on a random-walk midprice."""
    failed: list[str] = []
    head(
        "posting against crossing (corrected 2026-10-16): equal target quantity, common terminal"
        " mark, pathwise"
        " cash flows"
    )
    c, p_, g = outcomes(100, 99, True, None, 97)
    print(
        f"  fill at 99 vs buy at 100, mark 97: crossing {c:+}, posting {p_:+}, posting gain {g:+}"
        f" (= the spread"
        " saved; the fall to 97 hits both)"
    )
    check(failed, "a fill at 99 saves the 1-tick spread", bool(g == 1))
    c, p_, g = outcomes(100, 99, False, 101.5, 103)
    print(
        f"  miss, chase at 101.5, mark 103: crossing {c:+}, posting {p_:+}, posting gain {g:+} (="
        f" ask0 - chase"
        " price)"
    )
    check(failed, "a miss chased at 101.5 costs 1.5", bool(g == -1.5))
    # pathwise check on a random-walk midprice with a fill rule; the identity gain = p*S - (1-p)*M
    # holds by construction
    rng_p = np.random.default_rng(341)
    n, steps, half = 200_000, 50, 0.5
    mid0 = 100.0
    z = rng_p.standard_normal((n, steps)).cumsum(1) * 0.2
    mins, last = z.min(1), z[:, -1]
    filled = (
        mins <= -2 * half
    )  # the bid at mid0 - half is reached if the mid falls one full spread below it
    chase = mid0 + last + half  # buy at the horizon ask if missed
    mark = mid0 + last
    cross = mark - (mid0 + half)
    post = np.where(filled, mark - (mid0 - half), mark - chase)
    gain = post - cross
    p_fill = filled.mean()
    S = 2 * half
    M = (chase - (mid0 + half))[~filled].mean()
    print(
        f"  random walk: P(fill) {p_fill:.3f}; mean pathwise gain {gain.mean():+.4f}; p*S - (1-p)*M"
        f" ="
        f" {p_fill * S - (1 - p_fill) * M:+.4f}"
    )
    check(
        failed,
        "pathwise gain equals p S - (1 - p) M",
        bool(abs(gain.mean() - (p_fill * S - (1 - p_fill) * M)) < 1e-9),
    )
    A = (mid0 - half - mark)[filled].mean()  # the post-fill fall, the old formula's 'A'
    print(
        f"  the old formula subtracts A = E[fill price - mark | fill] = {A:+.3f} from the posting"
        f" branch only; the"
        f" same fall hits the crossing position, so p(S-A)-(1-p)M ="
        f" {p_fill * (S - A) - (1 - p_fill) * M:+.4f}"
        " misstates the gain"
    )
    return failed


def check_ex_fixing() -> list[str]:
    """Part 4: the ex-fixing share against the printed formula, equal iff m p (1 - M) = 0."""
    failed: list[str] = []
    head(
        "ex-fixing market share: (M - m p)/(1 - p) against the printed (1 - m p) M/(1 - p); equal"
        " iff m p (1 - M) = 0"
    )
    for M_, m_, p_ in [
        (0.60, 1.0, 0.20),
        (0.30, 0.0, 0.20),
        (0.70, 1.0, 0.25),
        (1.0, 1.0, 0.2),
        (0.4, 0.5, 0.0),
    ]:
        exact = ex_fixing(M_, m_, p_)
        printed = (1 - m_ * p_) * M_ / (1 - p_)
        agree = abs(exact - printed) < 1e-12
        check(
            failed,
            f"ex-fixing share agrees with the printed formula iff m p (1 - M) = 0 at M={M_},"
            f" m={m_}, p={p_}",
            bool(agree == (abs(m_ * p_ * (1 - M_)) < 1e-12)),
        )
        print(
            f"  M={M_}, m={m_}, p={p_}: ex-fixing {exact:.4f}; printed {printed:.4f}; agree {agree}"
            f" (m p (1-M) ="
            f" {m_ * p_ * (1 - M_):.3f})"
        )
    print(
        "  a monopolist (M = m = 1) has share 1 ex-fixing under both; p = 1 (all volume in"
        " auctions) leaves it"
        " undefined"
    )
    return failed


def check_entropy_and_gini(rng: np.random.Generator) -> list[str]:
    """Part 5: the normalised entropy FEI and the Gini of turnover, from the Lorenz curve."""
    head("FEI = entropy / log N (app. A.1) and an empty venue added")
    q = np.array([0.6, 0.25, 0.15])
    H = -(q * np.log(q)).sum()
    F3 = H / np.log(3)
    F4 = H / np.log(4)
    print(
        f"q={q}: F(N=3) = {F3:.4f}; with an empty fourth venue F = {F4:.4f} = log3/log4 x F(N=3) ="
        f" {np.log(3) / np.log(4) * F3:.4f}"
    )
    print(
        "uniform -> F =",
        round(float(-(np.full(4, 0.25) * np.log(np.full(4, 0.25))).sum() / np.log(4)), 6),
        "; one venue -> 0",
    )
    head("Gini from the Lorenz curve, G = 1 - 2 int L (app. A.9.1)")
    x = rng.lognormal(0, 1.2, 101)
    print(
        f"  lognormal turnover of 101 stocks: Lorenz Gini {gini(x):.4f}; half relative mean"
        f" difference"
        f" {gini_mean_diff(x):.4f}"
    )
    print(
        "  equal turnover ->",
        round(gini(np.ones(50)), 6),
        "; LL Table A.3: B = 0.18 -> G = 1 - 2B =",
        1 - 2 * 0.18,
    )
    srt = np.sort(x)[::-1]
    cov80 = (np.searchsorted(np.cumsum(srt) / srt.sum(), 0.8) + 1) / len(srt)
    print(
        f"  coverage (share of stocks needed for 80 percent of turnover): {cov80:.2f}; 0.80 for"
        f" equal turnover"
    )
    return []


def check_two_sample_ks(rng: np.random.Generator) -> list[str]:
    """Part 6: a two-sample Kolmogorov-Smirnov test does not show equality of distributions."""
    head("two-sample KS: failure to reject is not equality of distributions")
    fails = 0
    for _ in range(1000):
        a = rng.normal(0, 1, 30)
        b = rng.normal(0.3, 1.2, 30)  # different distributions
        fails += int(stats.ks_2samp(a, b).pvalue > 0.05)
    print(
        f"  N(0,1) against N(0.3,1.2^2), 30 observations each: not rejected at 5 percent in"
        f" {fails / 10:.1f} percent"
        " of 1,000 trials"
    )
    n, m = 120, 120
    print(
        f"  LL Table A.4 statistics for SBF 120 (n=m=120 assumed here): critical D at 5 percent ~"
        f" {1.358 * np.sqrt((n + m) / (n * m)):.3f}; observed 0.1207 (2010) and 0.0833 (2012) fail"
        f" to reject,"
        " nothing more"
    )
    return []


def check_venue_shares() -> list[str]:
    """Part 7: venue-share estimators and their variances, count and value."""
    failed: list[str] = []
    head(
        "venue-share estimators (corrected 2026-10-16): count and value shares, and the"
        " fixed-weight index estimator"
    )
    rng_v = np.random.default_rng(342)
    p_true, n_tr = 0.3, 2000
    iid = rng_v.binomial(1, p_true, (4000, n_tr)).mean(1)
    print(
        f"  count share, independent trades: sd {iid.std():.4f} against sqrt(p(1-p)/n)"
        f" {np.sqrt(p_true * (1 - p_true) / n_tr):.4f}"
    )
    vals = rng_v.lognormal(0, 1.5, n_tr)  # fixed trade values
    X = rng_v.binomial(1, p_true, (4000, n_tr))
    vshare = (X * vals).sum(1) / vals.sum()
    n_eff = vals.sum() ** 2 / (vals**2).sum()
    print(
        f"  value share, fixed trade values, independent venues: sd {vshare.std():.4f} against"
        f" sqrt(p(1-p)/n_eff)"
        f" {np.sqrt(p_true * (1 - p_true) / n_eff):.4f} with n_eff = {n_eff:.0f} of {n_tr} trades"
    )
    runs = np.array([rng_v.binomial(1, p_true, n_tr // 20).repeat(20).mean() for _ in range(4000)])
    print(
        f"  count share with venue choices repeated in runs of 20: sd {runs.std():.4f}; binomial"
        f" {np.sqrt(p_true * (1 - p_true) / n_tr):.4f}"
    )
    w, p_, n_ = np.array([0.9, 0.1]), np.array([0.5, 0.5]), np.array([100, 100])
    s2 = p_ * (1 - p_) / n_
    correct = var_diff(w, s2, 0)
    book = (1 - 2 * w[0]) * s2[0] + 0.5 * 0.5 / n_.sum()
    print(
        f"  w=(0.9,0.1), p=(0.5,0.5), n=(100,100): Var(p_1 - p_hat) = (1-w1)^2 s1 + w2^2 s2 ="
        f" {correct:.5f};"
        f" the printed formula with pooled n = 200 gives {book:+.5f}"
    )
    check(
        failed,
        "variance of the share difference, and the printed formula's error",
        bool(abs(correct - 0.00005) < 1e-12 and abs(book + 0.00075) < 1e-12),
    )
    sims = rng_v.binomial(n_, p_, (400_000, 2)) / n_
    diff = sims[:, 0] - sims @ w
    print(f"  simulated variance {diff.var():.6f}")
    return failed


def check_sor_objective() -> list[str]:
    """Part 8: the SOR objective, its marginal values, and the grid optimum."""
    failed: list[str] = []
    head(
        "SOR objective (corrected 2026-10-16): E[sum_k min(r_k V, D_k)]; marginal value E[V"
        " 1{r_k V < D_k}]"
    )
    scen = [(1.0, np.array([0.4, 0.6])), (10.0, np.array([6.0, 4.0]))]  # equally likely

    def capture_of(r: Floats) -> float:
        """Return the expected capture of key r over the two equally likely scenarios."""
        value: float = np.mean([np.minimum(r * V, D).sum() for V, D in scen])
        return value

    def ind(r: Floats, weighted: bool) -> Floats:
        """Return E[1(rV < D)], or E[V 1(rV < D)] when weighted, per venue."""
        value: Floats = np.mean([(V if weighted else 1.0) * (r * V < D) for V, D in scen], axis=0)
        return value

    for r in [np.array([0.5, 0.5]), np.array([0.6, 0.4])]:
        print(
            f"  r={r}: expected capture {capture_of(r):.2f}; E[1(rV<D)] {ind(r, False)}; E[V"
            f" 1(rV<D)] {ind(r, True)}"
        )
    check(
        failed,
        "expected capture 4.95 at equal keys and 5.4 at 0.6 and 0.4",
        bool(
            abs(capture_of(np.array([0.5, 0.5])) - 4.95) < 1e-12
            and abs(capture_of(np.array([0.6, 0.4])) - 5.4) < 1e-12
        ),
    )
    grid = np.linspace(0, 1, 1001)
    caps = [capture_of(np.array([x, 1 - x])) for x in grid]
    print(
        f"  grid optimum r1 = {grid[int(np.argmax(caps))]:.3f} with capture {max(caps):.3f}: equal"
        f" unweighted"
        " indicators do not identify the optimum; the size-weighted condition does (interior: equal"
        " for all r_k > 0;"
        " boundary r_k = 0: no larger)"
    )
    return failed


def check_learner(rng: np.random.Generator) -> list[str]:
    """Part 9: a learner consistent with the objective, its exact optimum and the venue shares."""
    failed: list[str] = []
    head(
        "a learner consistent with that objective, with D independent of V and E[D_k / sum D] = p_k"
        " (Lehalle-Laruelle eq. A.10)"
    )
    mu, achieved = calibrate(rng, np.array([0.95, 0.03, 0.02]))
    print(
        f"  calibrated means {mu.round(4)} give E[D_k/sum D] = {achieved.round(4)} (target 0.95,"
        f" 0.03, 0.02)"
    )
    p_share, r, a_sor = np.array([0.95, 0.03, 0.02]), np.full(K, 1 / K), 0.3
    r_avg: Floats = np.full(K, 1 / K)
    for _ in range(60):
        mu, _ = calibrate(rng, p_share, iters=25, size=8_000)
        r, r_avg = learn(rng, r, mu, 3000)
        p_share = (1 - a_sor) * p_share + a_sor * r_avg
    r_opt, g_opt, _, lam = optimum(rng, mu)
    print(
        f"  illustrative coupled run, 60 periods (a = 0.3, nu = {NU}): shares {p_share.round(3)},"
        f" averaged keys"
        f" {r_avg.round(3)}"
    )
    print(
        f"  exact KKT optimum at the final liquidity: keys {r_opt.round(5)}, E[V 1(rV<D)]"
        f" {g_opt.round(4)}, lambda"
        f" {lam:.4f} (all keys positive and the marginal values equal: an interior solution)"
    )
    check(
        failed,
        "the exact optimum has positive keys with equal marginal values",
        bool(np.all(r_opt > 0) and np.ptp(g_opt) < 0.01 * lam + 1e-3),
    )
    print(
        f"  the learner averaged keys {r_avg.round(4)} against the exact optimum {r_opt.round(4)}"
    )
    check(
        failed,
        "the learner's averaged keys are within 0.01 of the optimum",
        bool(np.abs(r_avg - r_opt).max() < 0.01),
    )
    r_mid, g_mid, _, lam_mid = optimum(rng, np.array([0.6, 0.25, 0.15]))
    print(
        f"  same solver with liquidity means (0.6, 0.25, 0.15): keys {r_mid.round(3)}, E[V 1(rV<D)]"
        f" {g_mid.round(4)}"
    )
    check(
        failed,
        "the marginal values of the positive keys are equal at the other liquidity",
        bool(np.ptp(g_mid[r_mid > 0]) < 0.01 * lam_mid + 1e-3),
    )
    print(
        "  with D_k = mu_k X_k, X_k i.i.d. and V independent, the optimal keys are mu_k / sum mu"
        " (scale invariance),"
        " and the constraint E[D_k/sum D] = p_k makes mu_1/sum mu > p_1 for the largest venue, so p"
        " drifts towards"
        " it: this variant concentrates and does not reproduce Lehalle-Laruelle's 50/25/25 path"
        " (their nu is unreported"
        " and their update as printed differs)"
    )
    return failed


def check_cross_venue_bound() -> list[str]:
    """Part 10: a cross-venue buy and sale earn b2 - a1 - k per unit; arbitrage only if positive."""
    head("cross-venue bound: a buy at ask a1 and a sale at bid b2 earn b2 - a1 - k per unit")
    for a1, b2, k in [(100.00, 100.05, 0.02), (100.00, 100.01, 0.02)]:
        print(
            f"  a1={a1}, b2={b2}, all-in cost k={k}: profit per unit {b2 - a1 - k:+.2f} ->"
            f" {'arbitrage' if b2 - a1 > k else 'none'}"
        )
    return []


def main() -> int:
    """Run the parts in order with their generators, print each failed check as BAD.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    failed: list[str] = []
    failed += check_single_price_auction()
    failed += check_pro_rata()
    failed += check_posting()
    failed += check_ex_fixing()
    failed += check_entropy_and_gini(rng)
    failed += check_two_sample_ks(rng)
    failed += check_venue_shares()
    failed += check_sor_objective()
    failed += check_learner(np.random.default_rng(343))
    failed += check_cross_venue_bound()
    for name in failed:
        print("BAD", name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
