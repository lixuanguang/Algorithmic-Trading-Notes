"""Cash-flow streams, annuity factors, present values, internal rates and a growing dividend."""

from collections.abc import Callable

from trading_notes.records import Record


def bisect(f: Callable[[float], float], lo: float, hi: float, n: int = 200) -> float:
    """Return a root of f in [lo, hi]; the ends must have opposite signs unless one is a root.

    An end, or a midpoint, where f is exactly zero is returned as it is; otherwise the
    midpoint of the bracket left after n halvings.

    Raises:
        ValueError: If lo >= hi, or if f has the same nonzero sign at both ends.
    """
    if not lo < hi:
        raise ValueError("bracket needs lo < hi")
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if (flo > 0) == (fhi > 0):
        raise ValueError("ends of the bracket have the same sign")
    for _ in range(n):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if fmid == 0:
            return mid
        if (fmid > 0) == (flo > 0):
            lo, flo = mid, fmid
        else:
            hi = mid
    return (lo + hi) / 2


def annuity(r: float, n: float) -> float:
    """Return the annuity factor: n payments of one at rate r, at period ends (n if r is zero)."""
    return n if r == 0 else (1 - (1 + r) ** -n) / r


class CashFlowStream(Record):
    """Cash flows at t = 0, 1, 2, ... periods, with annual compounding at a rate per period.

    Attributes:
        flows: The flow at each date, from t = 0.
    """

    flows: tuple[float, ...]

    def npv(self, rate: float) -> float:
        """Return the value at t = 0 of the flows discounted at rate per period."""
        return sum(c / (1 + rate) ** t for t, c in enumerate(self.flows))

    def npv_slope(self, rate: float) -> float:
        """Return d NPV / d rate, the sum of -t c / (1 + rate)^(t + 1)."""
        return sum(-t * c / (1 + rate) ** (t + 1) for t, c in enumerate(self.flows))

    def irr(self, lo: float, hi: float) -> float:
        """Return the internal rate in [lo, hi] by bisection on the NPV.

        Raises:
            ValueError: If the bracket is invalid or does not change sign (see `bisect`).
        """
        return bisect(self.npv, lo, hi)


class GrowingDividend(Record):
    """A share valued by a dividend growing at a constant rate.

    Attributes:
        d0: Dividend just paid.
        g: Constant growth rate of the dividend.
        r: Required return.
    """

    d0: float
    g: float
    r: float

    def value(self) -> float:
        """Return the constant-growth value D1 / (r - g), with D1 = D0 (1 + g)."""
        return self.d0 * (1 + self.g) / (self.r - self.g)
