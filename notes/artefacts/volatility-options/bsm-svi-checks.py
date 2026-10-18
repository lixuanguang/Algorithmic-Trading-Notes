"""empirical extensions (2026-10-17): own checks behind mod:black-scholes-merton and def:implied-volatility-surface.

Sources compared (see the entries for locators): Black and Scholes (1973), eq. (7) (the differential equation) and
eq. (13) (the formula); Merton (1973), Theorems 1-2 (lower bound and no early exercise of a call on a stock without
payouts); Hull, 11th Global ed., Example 15.6 (c = 4.76, p = 0.81) and Table 19.6 (Greeks with a yield q); Gatheral and
Jacquier, arXiv:1204.0646, Lemma 2.1 (calendar condition), eq. (2.1) and Lemma 2.2 (butterfly condition g >= 0),
eq. (3.1) (raw SVI) and Example 3.1 (Vogt's parameters, which give a negative density).
Finding: in the proof of Lemma 2.2 (p. 5, page image) the source writes p(k) = d2C/dK2 at K = F e^k and then
p(k) = g(k)/sqrt(2 pi w(k)) exp(-d_-(k)^2/2); the second is the density per unit log-moneyness, K times the first
(checked below). The sign condition g >= 0 is unaffected because K > 0.
Checks are independent of the entries' algebra: formulas against quadrature, finite differences and the PDE.
Run: uv run python bsm-svi-checks.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import math
import sys

fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
n = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def bs(S, K, r, q, sig, T, call=True):
    d1 = (math.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    if call:
        return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2)
    return K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1)


print("== Black-Scholes-Merton price")
c, p = bs(42, 40, 0.1, 0, 0.2, 0.5), bs(42, 40, 0.1, 0, 0.2, 0.5, call=False)
ok(
    "Hull Example 15.6: c = 4.76, p = 0.81",
    round(c, 2) == 4.76 and round(p, 2) == 0.81,
    f"{c:.4f}, {p:.4f}",
)
ok("put-call parity c - p = S - K exp(-rT)", abs(c - p - (42 - 40 * math.exp(-0.05))) < 1e-12)
# risk-neutral expectation by quadrature over the lognormal terminal price
S, K, r, q, sig, T = 100.0, 105.0, 0.05, 0.02, 0.25, 0.75
m = math.log(S) + (r - q - sig * sig / 2) * T
s = sig * math.sqrt(T)
h = 1e-3
tot = 0.0
for i in range(-8000, 8000):
    z = (i + 0.5) * h
    tot += max(math.exp(m + s * z) - K, 0) * n(z) * h
ok(
    "formula equals discounted risk-neutral expectation",
    abs(math.exp(-r * T) * tot - bs(S, K, r, q, sig, T)) < 1e-6,
    f"{math.exp(-r * T) * tot:.6f} vs {bs(S, K, r, q, sig, T):.6f}",
)

print("== the differential equation (Black and Scholes eq. (7), with a yield q as in Hull)")
f = lambda x, t: bs(x, K, r, q, sig, T - t)
x0, t0, e = 100.0, 0.1, 1e-3
w1 = (f(x0 + e, t0) - f(x0 - e, t0)) / (2 * e)
w11 = (f(x0 + e, t0) - 2 * f(x0, t0) + f(x0 - e, t0)) / e**2
w2 = (f(x0, t0 + 1e-5) - f(x0, t0 - 1e-5)) / 2e-5
res = w2 + (r - q) * x0 * w1 + 0.5 * sig**2 * x0**2 * w11 - r * f(x0, t0)
ok("PDE residual near zero", abs(res) < 1e-5, f"{res:.2e}")

print("== Greeks (Hull Table 19.6) against finite differences")
d1 = (math.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * math.sqrt(T))
d2 = d1 - sig * math.sqrt(T)
g = {
    "delta": math.exp(-q * T) * N(d1),
    "gamma": n(d1) * math.exp(-q * T) / (S * sig * math.sqrt(T)),
    "vega": S * math.sqrt(T) * n(d1) * math.exp(-q * T),
    "theta": -S * n(d1) * sig * math.exp(-q * T) / (2 * math.sqrt(T))
    + q * S * N(d1) * math.exp(-q * T)
    - r * K * math.exp(-r * T) * N(d2),
    "rho": K * T * math.exp(-r * T) * N(d2),
}
fd = {
    "delta": (bs(S + e, K, r, q, sig, T) - bs(S - e, K, r, q, sig, T)) / (2 * e),
    "gamma": (bs(S + e, K, r, q, sig, T) - 2 * bs(S, K, r, q, sig, T) + bs(S - e, K, r, q, sig, T))
    / e**2,
    "vega": (bs(S, K, r, q, sig + 1e-5, T) - bs(S, K, r, q, sig - 1e-5, T)) / 2e-5,
    "theta": -(bs(S, K, r, q, sig, T + 1e-5) - bs(S, K, r, q, sig, T - 1e-5)) / 2e-5,
    "rho": (bs(S, K, r + 1e-6, q, sig, T) - bs(S, K, r - 1e-6, q, sig, T)) / 2e-6,
}
for k in g:
    ok(f"call {k}", abs(g[k] - fd[k]) < 1e-4 * max(1, abs(g[k])), f"{g[k]:.6f} vs {fd[k]:.6f}")
lhs = g["theta"] + (r - q) * S * g["delta"] + 0.5 * sig**2 * S**2 * g["gamma"]
ok(
    "theta + (r-q) S delta + sig^2 S^2 gamma / 2 = r c",
    abs(lhs - r * bs(S, K, r, q, sig, T)) < 1e-10,
    f"{lhs:.8f}",
)

print("== Merton (1973) Theorems 1-2, no payouts")
for sg in (0.05, 0.2, 0.6):
    cc = bs(42, 40, 0.1, 0, sg, 0.5)
    ok(
        f"sigma {sg}: c >= max(0, S - K P(tau)) > S - K",
        cc >= 42 - 40 * math.exp(-0.05) - 1e-12 and cc > 2,
        f"{cc:.4f}",
    )
# with a large yield q the European call can fall below intrinsic value: early exercise can then be worth something
cq = bs(150, 100, 0.02, 0.10, 0.2, 2.0)
ok(
    "with yield q = 10%, deep ITM European call below S - K (Theorem 1 needs no payouts)",
    cq < 50,
    f"{cq:.4f}",
)

print("== implied volatility")


def implied(price, S, K, r, q, T, lo=1e-4, hi=5.0):
    for _ in range(200):
        mid = (lo + hi) / 2
        if bs(S, K, r, q, mid, T) > price:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


iv = implied(bs(S, K, r, q, 0.3127, T), S, K, r, q, T)
ok("bisection recovers sigma = 0.3127", abs(iv - 0.3127) < 1e-9, f"{iv:.10f}")

print("== SVI slices (Gatheral and Jacquier)")


def svi(k, a, b, rho, mm, s):
    return a + b * (rho * (k - mm) + math.sqrt((k - mm) ** 2 + s * s))


def gfun(k, w, eps=1e-4):
    W = w(k)
    W1 = (w(k + eps) - w(k - eps)) / (2 * eps)
    W2 = (w(k + eps) - 2 * W + w(k - eps)) / eps**2
    return (1 - k * W1 / (2 * W)) ** 2 - W1**2 / 4 * (1 / W + 0.25) + W2 / 2


def density_numeric(k, w, eps=1e-3):
    """Second strike derivative of the undiscounted Black-Scholes call with forward 1, in log-strike k."""

    def call(K):
        kk = math.log(K)
        W = w(kk)
        dp = -kk / math.sqrt(W) + math.sqrt(W) / 2
        return N(dp) - K * N(dp - math.sqrt(W))

    K0 = math.exp(k)
    return (call(K0 * (1 + eps)) - 2 * call(K0) + call(K0 * (1 - eps))) / (K0 * eps) ** 2


good = lambda k: svi(k, 0.04, 0.4, -0.4, 0.0, 0.2)  # an illustrative slice (own parameters, t = 1)
vogt = lambda k: svi(
    k, -0.0410, 0.1331, 0.3060, 0.3586, 0.4153
)  # Example 3.1: (a, b, m, rho, sigma) = (-0.0410, 0.1331, 0.3586, 0.3060, 0.4153)
for name, w in (("illustrative slice", good), ("Vogt slice", vogt)):
    worst = min(gfun(k / 100, w) for k in range(-150, 151))
    # density from g (Lemma 2.2 proof) against a numerical second derivative, at k = 0.1
    k = 0.1
    W = w(k)
    dm = -k / math.sqrt(W) - math.sqrt(W) / 2
    p_g = gfun(k, w) / math.sqrt(2 * math.pi * W) * math.exp(-dm * dm / 2)
    dens_K = density_numeric(k, w)  # d2C/dK2: the risk-neutral density per unit strike (forward 1)
    ok(
        f"{name}: g-based expression equals K * d2C/dK2 (density per unit log-moneyness) at k = 0.1",
        abs(p_g - math.exp(k) * dens_K) < 1e-4,
        f"{p_g:.6f} vs {math.exp(k) * dens_K:.6f}",
    )
    ok(
        f"{name}: it differs from d2C/dK2 itself by the factor K = e^k (the source writes both as p(k))",
        abs(p_g / dens_K - math.exp(k)) < 1e-3,
        f"ratio {p_g / dens_K:.5f}, e^k {math.exp(k):.5f}",
    )
    print(f"     {name}: min g over k in [-1.5, 1.5] = {worst:+.4f}")
    if name == "Vogt slice":
        ok("Vogt slice has g < 0 somewhere (butterfly arbitrage)", worst < 0)
    else:
        ok("illustrative slice has g >= 0 on the grid", worst >= 0)
ok(
    "raw SVI non-negativity condition a + b sigma sqrt(1 - rho^2) >= 0 holds for Vogt",
    -0.0410 + 0.1331 * 0.4153 * math.sqrt(1 - 0.306**2) >= 0,
)
w1 = lambda k: svi(k, 0.02, 0.3, -0.3, 0.0, 0.2)
w2 = lambda k: svi(k, 0.03, 0.3, -0.3, 0.0, 0.2)
ok(
    "calendar condition: the volatility slice that lies above another everywhere (w2 >= w1)",
    all(w2(k / 10) >= w1(k / 10) for k in range(-30, 31)),
)
if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
