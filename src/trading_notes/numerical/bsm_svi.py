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
Rates, yields and volatilities are annual decimals and times are in years.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.bsm_svi (standard library).
"""

# standard library imports
import math
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

# project library imports
from trading_notes.numerical.report import CheckReport

# A total-variance slice w(k) of log-moneyness k.
Slice = Callable[[float], float]


@dataclass(frozen=True)
class OptionCase:
    """A European call shared by the quadrature, PDE, Greeks and implied-volatility checks.

    Attributes:
        S: Spot price.
        K: Strike.
        r: Continuously compounded risk-free rate.
        q: Continuous dividend yield.
        sig: Volatility.
        T: Time to expiry in years.
    """

    S: float
    K: float
    r: float
    q: float
    sig: float
    T: float


CASE: Final = OptionCase(S=100.0, K=105.0, r=0.05, q=0.02, sig=0.25, T=0.75)
# Spot step of the central differences in the PDE and Greek checks.
FD_STEP: Final = 1e-3


def N(x: float) -> float:
    """Return the standard normal distribution function."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def n(x: float) -> float:
    """Return the standard normal density."""
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def bs(S: float, K: float, r: float, q: float, sig: float, T: float, call: bool = True) -> float:
    """Return the Black-Scholes-Merton price of a European call or put with a continuous yield q."""
    d1 = (math.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    if call:
        return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2)
    return K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1)


def check_price(report: CheckReport) -> None:
    """Check Hull's example, put-call parity, and the formula against quadrature."""
    print("== Black-Scholes-Merton price")
    c, p = bs(42, 40, 0.1, 0, 0.2, 0.5), bs(42, 40, 0.1, 0, 0.2, 0.5, call=False)
    report.ok(
        "Hull Example 15.6: c = 4.76, p = 0.81",
        round(c, 2) == 4.76 and round(p, 2) == 0.81,
        f"{c:.4f}, {p:.4f}",
    )
    report.ok(
        "put-call parity c - p = S - K exp(-rT)", abs(c - p - (42 - 40 * math.exp(-0.05))) < 1e-12
    )
    # risk-neutral expectation by quadrature over the lognormal terminal price
    S, K, r, q, sig, T = CASE.S, CASE.K, CASE.r, CASE.q, CASE.sig, CASE.T
    m = math.log(S) + (r - q - sig * sig / 2) * T
    s = sig * math.sqrt(T)
    h = 1e-3
    tot = 0.0
    for i in range(-8000, 8000):
        z = (i + 0.5) * h
        tot += max(math.exp(m + s * z) - K, 0) * n(z) * h
    report.ok(
        "formula equals discounted risk-neutral expectation",
        abs(math.exp(-r * T) * tot - bs(S, K, r, q, sig, T)) < 1e-6,
        f"{math.exp(-r * T) * tot:.6f} vs {bs(S, K, r, q, sig, T):.6f}",
    )


def check_pde(report: CheckReport) -> None:
    """Check the price against the Black-Scholes equation by finite differences."""
    print("== the differential equation (Black and Scholes eq. (7), with a yield q as in Hull)")
    K, r, q, sig, T = CASE.K, CASE.r, CASE.q, CASE.sig, CASE.T

    def f(x: float, t: float) -> float:
        return bs(x, K, r, q, sig, T - t)

    x0, t0, e = 100.0, 0.1, FD_STEP
    w1 = (f(x0 + e, t0) - f(x0 - e, t0)) / (2 * e)
    w11 = (f(x0 + e, t0) - 2 * f(x0, t0) + f(x0 - e, t0)) / e**2
    w2 = (f(x0, t0 + 1e-5) - f(x0, t0 - 1e-5)) / 2e-5
    res = w2 + (r - q) * x0 * w1 + 0.5 * sig**2 * x0**2 * w11 - r * f(x0, t0)
    report.ok("PDE residual near zero", abs(res) < 1e-5, f"{res:.2e}")


def check_greeks(report: CheckReport) -> None:
    """Check the closed-form call Greeks against finite differences and the PDE identity."""
    print("== Greeks (Hull Table 19.6) against finite differences")
    S, K, r, q, sig, T = CASE.S, CASE.K, CASE.r, CASE.q, CASE.sig, CASE.T
    e = FD_STEP
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
        "gamma": (
            bs(S + e, K, r, q, sig, T) - 2 * bs(S, K, r, q, sig, T) + bs(S - e, K, r, q, sig, T)
        )
        / e**2,
        "vega": (bs(S, K, r, q, sig + 1e-5, T) - bs(S, K, r, q, sig - 1e-5, T)) / 2e-5,
        "theta": -(bs(S, K, r, q, sig, T + 1e-5) - bs(S, K, r, q, sig, T - 1e-5)) / 2e-5,
        "rho": (bs(S, K, r + 1e-6, q, sig, T) - bs(S, K, r - 1e-6, q, sig, T)) / 2e-6,
    }
    for k in g:
        report.ok(
            f"call {k}", abs(g[k] - fd[k]) < 1e-4 * max(1, abs(g[k])), f"{g[k]:.6f} vs {fd[k]:.6f}"
        )
    lhs = g["theta"] + (r - q) * S * g["delta"] + 0.5 * sig**2 * S**2 * g["gamma"]
    report.ok(
        "theta + (r-q) S delta + sig^2 S^2 gamma / 2 = r c",
        abs(lhs - r * bs(S, K, r, q, sig, T)) < 1e-10,
        f"{lhs:.8f}",
    )


def check_merton_bounds(report: CheckReport) -> None:
    """Check Merton's lower bound without payouts, and its failure with a large yield."""
    print("== Merton (1973) Theorems 1-2, no payouts")
    for sg in (0.05, 0.2, 0.6):
        cc = bs(42, 40, 0.1, 0, sg, 0.5)
        report.ok(
            f"sigma {sg}: c >= max(0, S - K P(tau)) > S - K",
            cc >= 42 - 40 * math.exp(-0.05) - 1e-12 and cc > 2,
            f"{cc:.4f}",
        )
    # with a large yield q the European call can fall below intrinsic value: early exercise can then be worth something
    cq = bs(150, 100, 0.02, 0.10, 0.2, 2.0)
    report.ok(
        "with yield q = 10%, deep ITM European call below S - K (Theorem 1 needs no payouts)",
        cq < 50,
        f"{cq:.4f}",
    )


def implied(
    price: float,
    S: float,
    K: float,
    r: float,
    q: float,
    T: float,
    lo: float = 1e-4,
    hi: float = 5.0,
) -> float:
    """Return the call's implied volatility by 200 bisection steps on [lo, hi].

    Relies on the call price rising with volatility. The bracket is not validated: a price
    above the price at hi returns about hi, and one below the price at lo about lo.
    """
    for _ in range(200):
        mid = (lo + hi) / 2
        if bs(S, K, r, q, mid, T) > price:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def check_implied_volatility(report: CheckReport) -> None:
    """Recover a known volatility from its own price."""
    print("== implied volatility")
    S, K, r, q, T = CASE.S, CASE.K, CASE.r, CASE.q, CASE.T
    iv = implied(bs(S, K, r, q, 0.3127, T), S, K, r, q, T)
    report.ok("bisection recovers sigma = 0.3127", abs(iv - 0.3127) < 1e-9, f"{iv:.10f}")


def svi(k: float, a: float, b: float, rho: float, mm: float, s: float) -> float:
    """Return raw SVI total variance at log-moneyness k (Gatheral and Jacquier eq. (3.1))."""
    return a + b * (rho * (k - mm) + math.sqrt((k - mm) ** 2 + s * s))


def gfun(k: float, w: Slice, eps: float = 1e-4) -> float:
    """Return the butterfly function g(k) of eq. (2.1), with w' and w'' by central differences."""
    W = w(k)
    W1 = (w(k + eps) - w(k - eps)) / (2 * eps)
    W2 = (w(k + eps) - 2 * W + w(k - eps)) / eps**2
    return (1 - k * W1 / (2 * W)) ** 2 - W1**2 / 4 * (1 / W + 0.25) + W2 / 2


def density_numeric(k: float, w: Slice, eps: float = 1e-3) -> float:
    """Second strike derivative of the undiscounted Black-Scholes call with forward 1, in log-strike k."""

    def call(K: float) -> float:
        kk = math.log(K)
        W = w(kk)
        dp = -kk / math.sqrt(W) + math.sqrt(W) / 2
        return N(dp) - K * N(dp - math.sqrt(W))

    K0 = math.exp(k)
    return (call(K0 * (1 + eps)) - 2 * call(K0) + call(K0 * (1 - eps))) / (K0 * eps) ** 2


def good(k: float) -> float:
    """An illustrative slice (own parameters, t = 1)."""
    return svi(k, 0.04, 0.4, -0.4, 0.0, 0.2)


def vogt(k: float) -> float:
    """Example 3.1: (a, b, m, rho, sigma) = (-0.0410, 0.1331, 0.3586, 0.3060, 0.4153)."""
    return svi(k, -0.0410, 0.1331, 0.3060, 0.3586, 0.4153)


def w1(k: float) -> float:
    """The lower slice of the calendar check."""
    return svi(k, 0.02, 0.3, -0.3, 0.0, 0.2)


def w2(k: float) -> float:
    """The upper slice of the calendar check."""
    return svi(k, 0.03, 0.3, -0.3, 0.0, 0.2)


def check_svi(report: CheckReport) -> None:
    """Check the butterfly and calendar conditions and the density identity on SVI slices."""
    print("== SVI slices (Gatheral and Jacquier)")
    slices: tuple[tuple[str, Slice], ...] = (("illustrative slice", good), ("Vogt slice", vogt))
    for name, w in slices:
        worst = min(gfun(k / 100, w) for k in range(-150, 151))
        # density from g (Lemma 2.2 proof) against a numerical second derivative, at k = 0.1
        k = 0.1
        W = w(k)
        dm = -k / math.sqrt(W) - math.sqrt(W) / 2
        p_g = gfun(k, w) / math.sqrt(2 * math.pi * W) * math.exp(-dm * dm / 2)
        # d2C/dK2: the risk-neutral density per unit strike (forward 1)
        dens_K = density_numeric(k, w)
        report.ok(
            f"{name}: g-based expression equals K * d2C/dK2 (density per unit log-moneyness) at k = 0.1",
            abs(p_g - math.exp(k) * dens_K) < 1e-4,
            f"{p_g:.6f} vs {math.exp(k) * dens_K:.6f}",
        )
        report.ok(
            f"{name}: it differs from d2C/dK2 itself by the factor K = e^k (the source writes both as p(k))",
            abs(p_g / dens_K - math.exp(k)) < 1e-3,
            f"ratio {p_g / dens_K:.5f}, e^k {math.exp(k):.5f}",
        )
        print(f"     {name}: min g over k in [-1.5, 1.5] = {worst:+.4f}")
        if name == "Vogt slice":
            report.ok("Vogt slice has g < 0 somewhere (butterfly arbitrage)", worst < 0)
        else:
            report.ok("illustrative slice has g >= 0 on the grid", worst >= 0)
    report.ok(
        "raw SVI non-negativity condition a + b sigma sqrt(1 - rho^2) >= 0 holds for Vogt",
        -0.0410 + 0.1331 * 0.4153 * math.sqrt(1 - 0.306**2) >= 0,
    )
    report.ok(
        "calendar condition: the volatility slice that lies above another everywhere (w2 >= w1)",
        all(w2(k / 10) >= w1(k / 10) for k in range(-30, 31)),
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    check_price(report)
    check_pde(report)
    check_greeks(report)
    check_merton_bounds(report)
    check_implied_volatility(report)
    check_svi(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
