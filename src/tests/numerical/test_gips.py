"""Tests of the invented composite policy's month boundaries at whole-month dates."""

import unittest

from trading_notes.numerical.performance_standards.composite import MembershipRule

MONTHS = range(1, 13)


def months_in(rule: MembershipRule) -> list[int]:
    """Return the months in which the portfolio is a member."""
    return [m for m in MONTHS if rule.member(m)]


class Boundaries(unittest.TestCase):
    """Entry at the first full month after funding; exit after the last full month."""

    def test_entry(self) -> None:
        """Funded at a month's end (3.0) or within it (3.4), the portfolio enters in month 4."""
        self.assertEqual(months_in(MembershipRule(start=3.0))[0], 4)
        self.assertEqual(months_in(MembershipRule(start=3.4))[0], 4)
        self.assertEqual(months_in(MembershipRule(start=0)), list(MONTHS))

    def test_exit(self) -> None:
        """Terminated at 11.0 or 11.99, the last full month counted is 10."""
        self.assertEqual(months_in(MembershipRule(start=0, end=11.0))[-1], 10)
        self.assertEqual(months_in(MembershipRule(start=0, end=11.99))[-1], 10)

    def test_flow_and_mandate(self) -> None:
        """A large flow removes its month and the next; a mandate change takes effect next month."""
        self.assertEqual(months_in(MembershipRule(start=0, sig_flow_month=12)), list(range(1, 12)))
        self.assertEqual(months_in(MembershipRule(start=0, mandate_change=6.0)), list(range(1, 7)))
        self.assertEqual(months_in(MembershipRule(start=0, nondiscretionary=True)), [])


if __name__ == "__main__":
    unittest.main()
