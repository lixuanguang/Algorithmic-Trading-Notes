"""derivatives and empirical validation (2026-10-17): settlement conventions behind mod:multi-curve-fra-swap-valuation.

End settlement (a swaplet): receive N tau (L - K) at T2. With F_j defined as the T2-forward-measure expectation of the
  index fixing L (the market FRA/swaplet rate read from index j's projection curve) and OIS discounting of a
  collateralised trade, its value is N tau (F_j - K) P_OIS(T2) exactly; that is what the entry's formula prices.
Start settlement (the conventional FRA): receive N tau (L - K) / (1 + tau L) at T1, the end amount discounted at the
  fixing itself (Hull, 11th Global ed., sec. 4.9, p. 111, footnote 4: the payment "would be made at time two years and
  equal to the present value of $125,000 discounted for three months at 3.5%"). Its value is
  N P_OIS(T1) E^{T1}[tau (L - K) / (1 + tau L)]. Substituting L = F_j gives N tau (F_j - K) P_OIS(T1) / (1 + tau F_j);
  that is exact when L is deterministic, and in the single-curve case, where 1/(1 + tau L) = P(T1, T2) and the payoff
  is replicated by bonds whatever L does. With a separate projection curve and stochastic L it omits a convexity term:
  the payoff is concave in L, and the T1-measure mean of L need not equal F_j.
Checks:
  1. The entry's invented two-curve example: start -20,777.37 against end -20,792.96 (the audit's figures).
  2. Single curve: start and end values coincide, and equal N (P(T1) - (1 + tau K) P(T2)).
  3. Separate curves: they differ, by N tau (F_j - K) [P_OIS(T1)/(1 + tau F_j) - P_OIS(T2)].
  4. Stochastic L with deterministic OIS rates (so all forward measures coincide and E[L] = F_j): the expected
     start-settled payoff lies below the deterministic substitution (Jensen), by an amount that grows with the
     volatility of L (expectation by quadrature over the normal density). Illustration only; lognormal L and the
     volatilities are invented.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.fra_settlement (standard library).
"""

import math
import sys
from collections.abc import Callable
from typing import Final

from trading_notes.numerical.report import CheckReport

type Discount = Callable[[float], float]

# The FRA: fixing at T1, payment period to T2 (years), fixed rate K, notional N.
T1: Final = 1.0
T2: Final = 1.25
K: Final = 0.034
N: Final = 100e6
tau: Final = T2 - T1


def flat_curve(rate: float) -> Discount:
    """Return the discount factor function exp(-rate t) of a flat continuously compounded rate."""
    return lambda t: math.exp(-rate * t)


def values(Pois: Discount, Pref: Discount) -> tuple[float, float, float]:
    """Return the forward F_j and the start- and end-settled values with L = F_j substituted.

    Args:
        Pois: OIS discount factors.
        Pref: Discount factors of the index's projection curve.
    """
    F = (Pref(T1) / Pref(T2) - 1) / tau
    end = N * tau * (F - K) * Pois(T2)
    start = N * tau * (F - K) * Pois(T1) / (1 + tau * F)
    return F, start, end


def check_entry_example(report: CheckReport, Pois: Discount, Pref: Discount) -> float:
    """Check 1: the entry's invented two-curve example; returns its forward F_j."""
    print("== 1. the entry's invented curves (OIS 3.0%, term reference 3.3%, continuous)")
    F, start, end = values(Pois, Pref)
    print(f"     F_j = {F * 100:.4f}%; start-settled {start:,.2f}; end-settled {end:,.2f}")
    report.ok("start-settled -20,777.37", round(start, 2) == -20777.37)
    report.ok("end-settled -20,792.96", round(end, 2) == -20792.96)
    return F


def check_single_curve(report: CheckReport) -> None:
    """Check 2: with one curve the conventions coincide and equal the bond replication."""
    print("== 2. single curve: projection and discounting on the same curve")
    for r in (0.01, 0.03, 0.08):
        P = flat_curve(r)
        _, s1, e1 = values(P, P)
        rep = N * (P(T1) - (1 + tau * K) * P(T2))
        report.ok(
            f"coincide at {r:.0%}",
            abs(s1 - e1) < 1e-6 and abs(s1 - rep) < 1e-6,
            f"start {s1:,.4f}, end {e1:,.4f}, bonds {rep:,.4f}",
        )


def check_separate_curves(report: CheckReport, Pois: Discount) -> None:
    """Check 3: with a projection basis the conventions differ by the stated gap."""
    print("== 3. separate curves: the conventions diverge")
    for spread in (0.001, 0.003, 0.010):
        Pr = flat_curve(0.030 + spread)
        F3, s3, e3 = values(Pois, Pr)
        gap = N * tau * (F3 - K) * (Pois(T1) / (1 + tau * F3) - Pois(T2))
        report.ok(
            f"differ with a {spread * 1e4:.0f} bp basis",
            abs(s3 - e3) > 0.01 and abs((s3 - e3) - gap) < 1e-6,
            f"start - end = {s3 - e3:,.2f}",
        )


def check_convexity(report: CheckReport, Pois: Discount, F: float) -> None:
    """Check 4: a stochastic fixing L lowers the start-settled value below the substitution.

    Args:
        report: The run's report.
        Pois: OIS discount factors, deterministic.
        F: The forward F_j, the mean of the lognormal fixing L.
    """
    print(
        "== 4. stochastic L, deterministic OIS: deterministic substitution overstates the start-settled value"
    )
    Fm = F
    det = N * Pois(T1) * tau * (Fm - K) / (1 + tau * Fm)
    prev = 0.0
    for vol in (0.2, 0.5, 1.0):
        m, lo, hi = 8001, -10.0, 10.0  # trapezoid rule over the standard normal density
        h = (hi - lo) / (m - 1)
        acc = 0.0
        for i in range(m):
            z = lo + i * h
            L = Fm * math.exp(vol * math.sqrt(T1) * z - 0.5 * vol * vol * T1)  # E[L] = F_j
            w = (
                (0.5 if i in (0, m - 1) else 1.0)
                * h
                * math.exp(-0.5 * z * z)
                / math.sqrt(2 * math.pi)
            )
            acc += w * tau * (L - K) / (1 + tau * L)
        ex = N * Pois(T1) * acc
        report.ok(
            f"lognormal vol {vol:.0%}: exact expectation below substitution",
            ex < det and det - ex > prev,
            f"{ex:,.2f} vs substitution {det:,.2f} (gap {det - ex:,.2f})",
        )
        prev = det - ex


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    Pois = flat_curve(0.030)
    F = check_entry_example(report, Pois, flat_curve(0.033))
    check_single_curve(report)
    check_separate_curves(report, Pois)
    check_convexity(report, Pois, F)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
