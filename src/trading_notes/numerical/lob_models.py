"""Checks behind the market-making model statements.

Source verification (2026-10-17) (40-item source and backlog pass).

1. Avellaneda and Stoikov (2008), sec. 2.3, p. 219: the infinite-horizon value of a frozen
   inventory q, v(x,s,q) = E int_0^inf -exp(-omega t) exp(-gamma (x + q S_t)) dt with
   S_t = s + sigma W_t, equals -exp(-gamma (x + q s)) / D(q),
   D(q) = omega - gamma^2 sigma^2 q^2 / 2, finite iff omega > gamma^2 sigma^2 q^2 / 2.
   The indifference prices defined as in eqs. (4)-(5) are r_b = s + ln(D(q+1)/D(q))/gamma and
   r_a = s + ln(D(q)/D(q-1))/gamma (own derivation). The printed bid formula equals r_b
   exactly; the printed ask,
   s + ln(1 + (1-2q) gamma^2 sigma^2 / (2 omega - gamma^2 q^2 sigma^2))/gamma, does not equal
   r_a: it agrees only to first order in gamma^2 sigma^2 / omega and is not symmetric about s
   at q = 0, while the problem is. The value integral is also evaluated by quadrature as a check
   on the closed form. With omega = gamma^2 sigma^2 (q_max+1)^2 / 2, D(q) > 0 for |q| <= q_max
   and D(q_max+1) = 0, so the bid at q_max is -infinity (own reading of "bounded").
2. Avellaneda and Stoikov, sec. 3.1, eqs. (18)-(19), p. 221: with exponential intensities
   lambda = A exp(-k delta), lambda / lambda' = -1/k, so each implicit equation reduces to
   delta = (s - r_b) + ln(1 + gamma/k)/gamma (bid), the spread term of eq. (29) at the
   reservation prices; checked by solving (18) with a root finder.
3. Grossman and Miller, NBER WP 2641 (July 1988), eqs. (16)-(19), printed pp. 18-19: the
   free-entry condition with CARA utility and a normal imbalance i gives
   e^{ac} E exp(-(t/2) z^2) = 1, t = a^2 Var(P2) Var(i)/(1+M)^2, z^2 = i^2/Var(i). With E i = 0,
   (19) gives t = e^{2ac} - 1, so
   1 + M = a sqrt(Var(P2) Var(i)) / sqrt(e^{2ac} - 1).
   t is set by ac alone; M falls with c and rises with each variance; its response to a is not
   monotone (own derivation): d ln(1+M)/d a > 0 when 2ac < u*, u* e^{u*} = 2 (e^{u*} - 1),
   u* ~ 1.5936.
   The chi-squared moment generating function behind (18) is checked by simulation; the
   exponent carries (E i)^2 / Var(i) where the printed (18) shows (E i)^2 (immaterial when
   E i = 0).
Run: uv run --frozen --no-editable python -m trading_notes.numerical.lob_models
(numpy and scipy). Exits non-zero on failure.
"""

import math
import sys
from typing import Final

import numpy as np
from scipy import integrate, optimize

from trading_notes.numerical.report import CheckReport

SEED: Final = 20261017
GAMMA: Final = 0.1
SIGMA: Final = 2.0
S: Final = 100.0  # mid price
QMAX: Final = 5
A2: Final = GAMMA**2 * SIGMA**2  # gamma^2 sigma^2
OMEGA: Final = 0.5 * A2 * (QMAX + 1) ** 2


def near(report: CheckReport, name: str, got: float, want: float, tol: float = 1e-9) -> None:
    """Check |got - want| <= tol, printing got and want to eight significant digits."""
    report.ok(name, abs(got - want) <= tol, f"{got:.8g} (want {want:.8g}, tol {tol:g})")


def D(q: float) -> float:
    """Return the value's denominator, omega - gamma^2 sigma^2 q^2 / 2."""
    return OMEGA - 0.5 * A2 * q**2


def vbar(x: float, q: float) -> float:
    """Return the closed-form infinite-horizon value."""
    return -math.exp(-GAMMA * (x + q * S)) / D(q)


def vbar_quad(x: float, q: float) -> float:
    """Return the value by quadrature.

    The integrand uses E exp(-gamma q sigma W_t) = exp(gamma^2 q^2 sigma^2 t / 2).
    """
    gamma, s, omega, a = GAMMA, S, OMEGA, A2

    def f(t: float) -> float:
        return (
            -math.exp(-omega * t) * math.exp(-gamma * (x + q * s)) * math.exp(0.5 * a * q * q * t)
        )

    return integrate.quad(f, 0, np.inf)[0]


def check_reservation_prices(report: CheckReport) -> None:
    """1. The closed-form value, the indifference prices and the printed bid and ask."""
    print("== 1. Avellaneda-Stoikov infinite-horizon reservation prices")
    gamma, s, qmax, a, omega = GAMMA, S, QMAX, A2, OMEGA
    for q in (0, 2, -3):
        near(
            report,
            f"closed form against quadrature, q={q}",
            vbar(0.0, q),
            vbar_quad(0.0, q),
            1e-9 * abs(vbar(0.0, q)) + 1e-12,
        )

    for q in (-2, 0, 1, 3):
        rb = s + math.log(D(q + 1) / D(q)) / gamma
        ra = s + math.log(D(q) / D(q - 1)) / gamma
        near(
            report,
            f"indifference, bid, q={q}",
            vbar(-rb, q + 1),
            vbar(0.0, q),
            1e-10 * abs(vbar(0.0, q)),
        )
        near(
            report,
            f"indifference, ask, q={q}",
            vbar(ra, q - 1),
            vbar(0.0, q),
            1e-10 * abs(vbar(0.0, q)),
        )
        printed_b = s + math.log(1 + (-1 - 2 * q) * a / (2 * omega - a * q * q)) / gamma
        printed_a = s + math.log(1 + (1 - 2 * q) * a / (2 * omega - a * q * q)) / gamma
        near(report, f"printed bid = derived bid, q={q}", printed_b, rb, 1e-9)
        print(
            f"     q={q}: derived ask {ra:.6f}, printed ask {printed_a:.6f}, difference"
            f" {printed_a - ra:+.6f}"
        )
        report.ok(f"printed ask differs from derived ask, q={q}", abs(printed_a - ra) > 1e-6)
    ra0 = s + math.log(D(0) / D(-1)) / gamma
    rb0 = s + math.log(D(1) / D(0)) / gamma
    near(report, "derived prices symmetric about s at q=0", (ra0 + rb0) / 2, s, 1e-12)
    pa0 = s + math.log(1 + a / (2 * omega)) / gamma
    report.ok("printed ask not symmetric with the bid at q=0", abs((pa0 + rb0) / 2 - s) > 1e-6)
    for om2 in (1e2, 1e4):  # first-order agreement as a / omega -> 0 (q = 2)
        der = math.log((om2 - 0.5 * a * 4) / (om2 - 0.5 * a * 1))
        pri = math.log(1 + (1 - 4) * a / (2 * om2 - a * 4))
        near(
            report,
            f"printed/derived ask offset, a/omega = {a / om2:.0e} (relative)",
            pri / der,
            1.0,
            10 * a / om2,
        )
    report.ok("D(q) > 0 for |q| <= q_max", all(D(q) > 0 for q in range(-qmax, qmax + 1)))
    near(report, "D(q_max+1) = 0 under the natural choice of omega", D(qmax + 1), 0.0, 1e-12)


def check_exponential_intensities(report: CheckReport) -> None:
    """2. Eq. (18) solved by brentq against the closed-form bid distance."""
    print("\n== 2. Avellaneda-Stoikov eqs. (18)-(19) with exponential intensities")
    gamma = GAMMA
    A, k = 140.0, 1.5

    def lam(d: float) -> float:
        return A * math.exp(-k * d)

    def dlam(d: float) -> float:
        return -k * A * math.exp(-k * d)

    for gap in (0.3, -0.2, 1.1):  # gap = s - r_b

        def g(d: float) -> float:
            return d - math.log(1 - gamma * lam(d) / dlam(d)) / gamma - gap

        d = optimize.brentq(g, -20, 20)
        near(
            report,
            f"bid distance at s - r_b = {gap}",
            d,
            gap + math.log(1 + gamma / k) / gamma,
            1e-10,
        )


def check_free_entry(report: CheckReport, rng: np.random.Generator) -> None:
    """3. Grossman-Miller free entry: eq. (19), the mgf by simulation and the comparative statics.

    The variances are raised by 10 percent and divided back in place, as first run, so the
    later statics use the round-tripped values.
    """
    print("\n== 3. Grossman-Miller free entry, eqs. (16)-(19)")
    varP2, vari, aa, cc = 0.04, 9.0, 2.0, 0.05
    M = aa * math.sqrt(varP2 * vari) / math.sqrt(math.exp(2 * aa * cc) - 1) - 1
    t = aa**2 * varP2 * vari / (1 + M) ** 2
    near(report, "(19): 1/sqrt(1+t) = exp(-ac)", 1 / math.sqrt(1 + t), math.exp(-aa * cc), 1e-12)
    i = rng.normal(0.0, math.sqrt(vari), 2_000_000)
    lhs = float(math.exp(aa * cc) * np.mean(np.exp(-(aa**2 / 2) * varP2 * (i / (1 + M)) ** 2)))
    near(report, "(17a) by simulation with E i = 0", lhs, 1.0, 3e-3)
    mu = 1.5
    z = rng.normal(mu / math.sqrt(vari), 1.0, 2_000_000)
    sim = float(np.mean(np.exp(-(t / 2) * z**2)))
    mgf = math.exp(-(mu**2 / vari) * (t / 2) / (1 + t)) / math.sqrt(1 + t)
    near(report, "non-central chi-squared mgf with (E i)^2/Var(i) in the exponent", sim, mgf, 3e-3)

    def onepM(a_: float, c_: float = cc) -> float:
        # Reads varP2 and vari as they stand when called.
        return a_ * math.sqrt(varP2 * vari) / math.sqrt(math.exp(2 * a_ * c_) - 1)

    report.ok("M falls as c rises", onepM(aa, 0.04) > onepM(aa, 0.05) > onepM(aa, 0.08))
    base = onepM(aa)
    varP2 *= 1.1
    report.ok("M rises with Var(P2)", onepM(aa) > base)
    varP2 /= 1.1
    vari *= 1.1
    report.ok("M rises with Var(i)", onepM(aa) > base)
    vari /= 1.1
    ustar = optimize.brentq(lambda u: u * math.exp(u) - 2 * (math.exp(u) - 1), 0.5, 3)
    near(report, "threshold u* for the response to a", ustar, 1.5936, 1e-4)
    a_lo, a_hi = 0.25 * ustar / (2 * cc), 3 * ustar / (2 * cc)
    report.ok("dM/da > 0 below the threshold (2ac < u*)", onepM(a_lo * 1.01) > onepM(a_lo))
    report.ok("dM/da < 0 above the threshold (2ac > u*)", onepM(a_hi * 1.01) < onepM(a_hi))
    print(
        f"     example: c={cc}, a from {a_lo:.2f} to {a_lo * 1.01:.2f} raises 1+M from"
        f" {onepM(a_lo):.4f} to {onepM(a_lo * 1.01):.4f}"
    )


def main() -> int:
    """Run the three parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    report = CheckReport()
    check_reservation_prices(report)
    check_exponential_intensities(report)
    check_free_entry(report, np.random.default_rng(SEED))
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
