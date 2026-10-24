"""Hedge-fund management and incentive fees with a high-water mark and a hurdle."""

from collections.abc import Sequence

from trading_notes.numerical.records import Record


class FeeYear(Record):
    """One year of a fund's fees and NAV per 100 invested.

    Attributes:
        mgmt: The management fee.
        inc: The incentive fee.
        nav: The closing NAV.
        net: The investor's net return.
        gross_value: The opening NAV grown by the gross return, before fees.
    """

    mgmt: float
    inc: float
    nav: float
    net: float
    gross_value: float


class FeeTerms(Record):
    """A fund's fee terms.

    The management fee is charged on opening NAV at year end; the incentive fee on the year-end
    NAV after the management fee above the high-water mark (or opening NAV) grown by the
    hurdle. A soft hurdle, once cleared, charges the fee on the whole gain above the base.

    Attributes:
        management: The management fee rate.
        incentive: The incentive fee rate.
        hurdle: The hurdle rate.
        high_water_mark: Whether gains are measured above the high-water mark.
        soft: Whether the hurdle is soft rather than hard.
    """

    management: float = 0.02
    incentive: float = 0.2
    hurdle: float = 0.04
    high_water_mark: bool = True
    soft: bool = False

    def run(self, gross: Sequence[float], nav: float = 100.0) -> list[FeeYear]:
        """Return the fees and NAV, year by year, for the gross returns."""
        hwm = nav
        rows: list[FeeYear] = []
        for g in gross:
            start = nav
            mgmt = self.management * start
            after = start * (1 + g) - mgmt
            base = max(hwm, start) if self.high_water_mark else start
            if self.soft:
                gain = (after - base) if after >= base * (1 + self.hurdle) else 0.0
            else:
                gain = after - base * (1 + self.hurdle)
            inc = self.incentive * max(gain, 0.0)
            nav = after - inc
            hwm = max(hwm, nav)
            rows.append(
                FeeYear(
                    mgmt=mgmt, inc=inc, nav=nav, net=nav / start - 1, gross_value=start * (1 + g)
                )
            )
        return rows
