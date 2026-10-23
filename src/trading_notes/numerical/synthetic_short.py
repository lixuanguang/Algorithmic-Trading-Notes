"""Numerical checks for res:synthetic-short-put-call (securities lending and synthetic shorts review follow-up, 2026-10-15).

Run: uv run --frozen --no-editable python -m trading_notes.numerical.synthetic_short
Standard library only. Each check computes the quantity by a route independent of the
closed form it is compared with, and the script exits non-zero if a check fails.
"""

# standard library imports
import sys
from math import erf, exp, log, pi, sqrt
from typing import Final

TOL: Final = 1e-6
K: Final = 95.0
# Section 2's option case; section 3 uses it with q = 0.
S0: Final = 100.0
R: Final = 0.05
Q: Final = 0.02
SIGMA: Final = 0.25
T: Final = 1.0


class ShortReport:
    """One run's results: `ok  ` or `FAIL` lines with got and want to six decimals.

    Its summary counts the failures without naming them. Use a new report for each run.
    """

    def __init__(self) -> None:
        """Start a run with no failures."""
        self._failures: list[str] = []

    @property
    def failures(self) -> list[str]:
        """Return the names of the failed checks in the order they ran, as a new list."""
        return list(self._failures)

    def check(self, name: str, got: float, want: float, tol: float = TOL) -> None:
        """Print `ok   <name>: got <got>, want <want>`, or the FAIL line, and record a failure.

        Args:
            name: What the check asserts.
            got: The computed value.
            want: The expected value.
            tol: Absolute tolerance: the check holds when |got - want| <= tol.
        """
        ok = abs(got - want) <= tol
        print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got:.6f}, want {want:.6f}")
        if not ok:
            self._failures.append(name)


def N(x: float) -> float:
    """Return the standard normal distribution function."""
    return 0.5 * (1 + erf(x / sqrt(2)))


def bs(S: float, K: float, r: float, q: float, s: float, T: float) -> tuple[float, float]:
    """Return the Black-Scholes call and put values with a continuous yield q."""
    d1 = (log(S / K) + (r - q + 0.5 * s * s) * T) / (s * sqrt(T))
    d2 = d1 - s * sqrt(T)
    return (
        S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2),
        K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1),
    )


def by_quadrature(
    S: float,
    K: float,
    r: float,
    q: float,
    s: float,
    T: float,
    n: int = 200000,
    zmax: float = 10.0,
) -> tuple[float, float]:
    """Return the call and put values by midpoint integration over the lognormal density."""
    # Integrate over z ~ N(0,1), S_T = S exp((r - q - s^2/2) T + s sqrt(T) z), midpoint rule.
    h = 2 * zmax / n
    c = p = 0.0
    for i in range(n):
        z = -zmax + (i + 0.5) * h
        w = exp(-0.5 * z * z) / sqrt(2 * pi) * h
        ST = S * exp((r - q - 0.5 * s * s) * T + s * sqrt(T) * z)
        c += w * max(ST - K, 0.0)
        p += w * max(K - ST, 0.0)
    return exp(-r * T) * c, exp(-r * T) * p


def account(start: float, rate: float, T: float, days: int = 365) -> float:
    """Return a balance credited daily at a continuously compounded rate for T years."""
    bal = start
    for _ in range(days):
        bal *= exp(rate * T / days)
    return bal


def check_terminal_flows(report: ShortReport) -> None:
    """Check 1: terminal cash flows, leg by leg, against short stock (-S_T)."""
    print("1. Terminal cash flows (K = 95): put, -call, bond paying K, total")
    for ST in (60.0, 95.0, 100.0, 140.0):
        put = K - ST if ST < K else 0.0  # long put pays only below the strike
        call = ST - K if ST > K else 0.0  # short call owes only above the strike
        package = put - call
        with_long_bond = package + K  # Harris's wording: plus a long bond paying K
        with_short_bond = package - K  # package plus a short bond (borrowing) repaying K
        print(
            f"   S_T={ST:6.1f}: put {put:6.1f}, call {-call:6.1f}, "
            f"put-call {package:6.1f}, +bond {with_long_bond:6.1f}, -bond {with_short_bond:6.1f}"
        )
        report.check(f"   put-call = K - S_T at {ST}", package, K - ST)
        report.check(f"   put-call-bond = -S_T at {ST}", with_short_bond, -ST)
        report.check(f"   put-call+bond = 2K - S_T at {ST}", with_long_bond, 2 * K - ST)


def check_parity(report: ShortReport) -> None:
    """Check 2: European parity by quadrature against Black-Scholes closed forms.

    Numerical integration over the risk-neutral lognormal density is compared with the
    Black-Scholes closed forms and with K e^{-rT} - S0 e^{-qT}.
    """
    print("2. European parity, S0=100, K=95, r=5%, q=2%, sigma=25%, T=1")
    c_bs, p_bs = bs(S0, K, R, Q, SIGMA, T)
    c_q, p_q = by_quadrature(S0, K, R, Q, SIGMA, T)
    F = S0 * exp((R - Q) * T)
    print(f"   Black-Scholes C={c_bs:.4f} P={p_bs:.4f} P-C={p_bs - c_bs:.4f}; F={F:.4f}")
    report.check("   call, quadrature vs closed form", c_q, c_bs, 1e-4)
    report.check("   put, quadrature vs closed form", p_q, p_bs, 1e-4)
    report.check(
        "   P-C (quadrature) = K e^-rT - S0 e^-qT",
        p_q - c_q,
        K * exp(-R * T) - S0 * exp(-Q * T),
        1e-4,
    )
    report.check("   P-C = e^-rT (K - F)", p_bs - c_bs, exp(-R * T) * (K - F))


def check_rebate(report: ShortReport) -> None:
    """Check 3: rebate comparison with no dividends (q = 0), by day-by-day cash accounts.

    Short sale: sell one share at S0, the full proceeds held as collateral and credited daily
    at the rebate r_b (continuously compounded); no fee beyond the rebate shortfall, no extra
    margin, no recall; buy back at S_T.  Package: buy the put and sell the call at their
    q = 0 European values, financing or investing P - C at r daily; receive K - S_T at T.
    """
    print("3. Rebate comparison, q = 0, S0=100, K=95, r=5%, sigma=25%, T=1")
    c0, p0 = bs(S0, K, R, 0.0, SIGMA, T)
    premium = p0 - c0
    print(
        f"   q=0 values C={c0:.4f} P={p0:.4f} P-C={premium:.4f} = K e^-rT - S0 = {K * exp(-R * T) - S0:.4f}"
    )
    for rb in (0.05, 0.03, -0.01):
        for ST in (80.0, 100.0, 120.0):
            short_sale = account(S0, rb, T) - ST
            package = (K - ST) - account(premium, R, T)
            report.check(
                f"   short sale, r_b={rb:+.2f}, S_T={ST}: S0 e^(r_b T) - S_T",
                short_sale,
                S0 * exp(rb * T) - ST,
            )
            report.check(f"   package, S_T={ST}: S0 e^(rT) - S_T", package, S0 * exp(R * T) - ST)
        gap = ((K - 100.0) - account(premium, R, T)) - (account(S0, rb, T) - 100.0)
        report.check(
            f"   r_b={rb:+.2f}: package minus short sale = S0 (e^rT - e^(r_b T))",
            gap,
            S0 * (exp(R * T) - exp(rb * T)),
        )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = ShortReport()
    check_terminal_flows(report)
    check_parity(report)
    check_rebate(report)
    failures = report.failures
    if failures:
        print(f"{len(failures)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
