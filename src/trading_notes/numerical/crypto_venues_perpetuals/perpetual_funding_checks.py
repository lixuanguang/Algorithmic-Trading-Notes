"""Deribit's perpetual funding rule against its prose, and its worked payment examples."""

import sys
from collections.abc import Mapping
from typing import Final

from trading_notes.numerical.crypto_venues_perpetuals.funding_rates import (
    FundingRule,
    premium_rate,
)

TOL: Final = 1e-12
RULE: Final = FundingRule(damper=0.025)  # percent
CAPS: Final[Mapping[str, float]] = {"BTC": 0.5, "ETH": 1.0, "USDC/USDT": 5.0}  # percent, symmetric


class FundingReport:
    """One run's results: tolerance checks print a line each, grid mismatches only count.

    Its lines and summary differ from CheckReport's: `ok  ` or `FAIL` with got and want to
    12 significant digits, and a count with the first five failures. Use a new report for
    each run.
    """

    def __init__(self) -> None:
        """Start a run with no failures."""
        self._failures: list[str] = []

    @property
    def failures(self) -> list[str]:
        """Return the names of the failures in the order they occurred, as a new list."""
        return list(self._failures)

    def check(self, name: str, got: float, want: float, tol: float = TOL) -> None:
        """Print `ok   <name>: got <got>, want <want>`, or the FAIL line, and record a failure.

        Args:
            name: What the check asserts.
            got: The computed value.
            want: The expected value.
            tol: Relative tolerance, absolute when |want| < 1:
                |got - want| <= tol * max(1, |want|).
        """
        ok = abs(got - want) <= tol * max(1.0, abs(want))
        print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got:.12g}, want {want:.12g}")
        if not ok:
            self._failures.append(name)

    def mismatch(self, name: str) -> None:
        """Record a failure without printing it; the grid prints one status line instead."""
        self._failures.append(name)


def check_grid(report: FundingReport) -> None:
    """Check 1: the closed form against the piecewise rule on a grid of premium rates."""
    print("1. Closed form against piecewise rule on a grid of premium rates")
    for cap in CAPS.values():
        for i in range(-2000, 2001):
            p = i * 0.005  # -10% to +10% in 0.005% steps
            a, b = RULE.closed_form(p, cap), RULE.piecewise(p, cap)
            if abs(a - b) > 1e-12:
                report.mismatch(f"grid cap={cap} p={p}")
    agree = not any(f.startswith("grid") for f in report.failures)
    print(f"   {'all grid points agree' if agree else 'grid mismatch'}")


def check_worked_examples(report: FundingReport) -> None:
    """Check 2: every worked example of the Funding Specifications page."""
    print(
        "2. Worked examples (payment = rate/100 * position * minutes/480, in the settlement unit)"
    )
    # BTC inverse perpetual: position quoted USD 100,000 = 1 BTC at index 100,000; payment in BTC.
    r = RULE.closed_form(premium_rate(100_075, 100_000), CAPS["BTC"])
    report.check("   BTC example 1 rate (%)", r, 0.05)
    report.check("   BTC 1 minute, 1 BTC (BTC)", r / 100 * 1 * 1 / 480, 0.000001041667, 1e-12)
    report.check("   BTC 8 hours (BTC)", r / 100 * 1 * 480 / 480, 0.0005)
    # ETH inverse perpetual: USD 5,000 = 1 ETH.
    r = RULE.closed_form(premium_rate(5_005, 5_000), CAPS["ETH"])
    report.check("   ETH example 1 rate (%)", r, 0.075)
    report.check("   ETH 1 minute, 1 ETH (ETH)", r / 100 * 1 / 480, 0.0000015625)
    report.check("   ETH 8 hours (ETH)", r / 100 * 1, 0.00075)
    # SOL_USDC linear perpetual: USDC 100,000 = 1,000 SOL; payment in USDC.
    r = RULE.closed_form(premium_rate(100.10, 100.0), CAPS["USDC/USDT"])
    report.check("   SOL_USDC example 1 rate (%)", r, 0.075)
    report.check("   SOL_USDC 1 minute (USDC)", r / 100 * 100_000 / 480, 0.15625)
    report.check("   SOL_USDC 8 hours (USDC)", r / 100 * 100_000, 75.0)
    # Example 3: symmetric premium for one minute each nets to zero.
    up = RULE.closed_form(premium_rate(100_075, 100_000), CAPS["BTC"])
    dn = RULE.closed_form(premium_rate(99_925, 100_000), CAPS["BTC"])
    report.check("   BTC example 3 net over two minutes (BTC)", (up + dn) / 100 / 480, 0.0)
    # Example 4: inside the damper band.
    report.check(
        "   BTC example 4 rate (%)",
        RULE.closed_form(premium_rate(100_020, 100_000), CAPS["BTC"]),
        0.0,
    )
    report.check(
        "   ETH example 4 rate (%)", RULE.closed_form(premium_rate(5_001, 5_000), CAPS["ETH"]), 0.0
    )
    # Example 5: caps bind.
    report.check(
        "   BTC example 5 rate (%)",
        RULE.closed_form(premium_rate(107_500, 100_000), CAPS["BTC"]),
        0.5,
    )
    report.check(
        "   ETH example 5 rate (%)", RULE.closed_form(premium_rate(5_100, 5_000), CAPS["ETH"]), 1.0
    )
    report.check("   ETH example 5 uncapped (%)", premium_rate(5_100, 5_000) - RULE.damper, 1.975)
    report.check(
        "   USDC example 5 rate (%)",
        RULE.closed_form(premium_rate(107.5, 100.0), CAPS["USDC/USDT"]),
        5.0,
    )


def check_sign_convention(report: FundingReport) -> None:
    """Check 3: longs pay a positive rate, and the long and short flows cancel."""
    print(
        "3. Sign convention: positive rate, longs pay; a long's cash flow is"
        " -rate * size * fraction"
    )
    long_flow = -RULE.closed_form(0.075, CAPS["BTC"]) / 100 * 1 / 480
    short_flow = -long_flow
    report.check(
        "   long + short flows sum to zero (no fee on funding)", long_flow + short_flow, 0.0
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status.

    Numerical checks for mech:perpetual-funding. Rates are in percent per 8 hours, as Deribit
    quotes them; the closed form Deribit prints (max/min with a damper and caps) is compared with
    an independent piecewise reading of its prose rule, and every worked example on the Funding
    Specifications page (edited 27 July 2026) is recomputed.

    Returns:
        The exit status, 0 or 1.
    """
    report = FundingReport()
    check_grid(report)
    check_worked_examples(report)
    check_sign_convention(report)
    failures = report.failures
    if failures:
        print(f"{len(failures)} check(s) failed: {failures[:5]}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
