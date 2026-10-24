"""NBER recession dates and the outcomes of yield-curve inversion signals before recessions."""

import csv
from pathlib import Path
from typing import Literal

from trading_notes.records import Record

type Outcome = Literal["hit", "miss", "provisional miss", "window open"]


def add_months(m: str, k: int) -> str:
    """Return the month k calendar months after m, both written YYYY-MM."""
    y, mo = map(int, m.split("-"))
    n = 12 * y + (mo - 1) + k
    return f"{n // 12:04d}-{n % 12 + 1:02d}"


def read_monthly(path: Path, column: str, last: str) -> dict[str, float]:
    """Read a monthly series, keeping the complete months.

    Raises:
        ValueError: If the months repeat or skip, or the file does not end with the
            incomplete month `last`.
    """
    with path.open() as fh:
        rows = list(csv.DictReader(fh))
    months = [r["month"] for r in rows]
    if len(months) != len(set(months)) or any(
        add_months(months[k], 1) != months[k + 1] for k in range(len(months) - 1)
    ):
        raise ValueError(f"{path.name}: months are not consecutive")
    if rows[-1]["month"] != last or rows[-1]["complete"] != "no":
        raise ValueError(f"{path.name}: the last row is not the incomplete month {last}")
    return {r["month"]: float(r[column]) for r in rows if r["complete"] == "yes"}


class RecessionCalendar(Record):
    """NBER business-cycle peaks and troughs, as months.

    Attributes:
        peaks: Each peak month, the last month of an expansion.
        troughs: Each trough month, the last month of the following contraction.
    """

    peaks: tuple[str, ...]
    troughs: tuple[str, ...]

    def onsets(self) -> list[str]:
        """Return each recession's first contraction month, the month after its peak."""
        return [add_months(p, 1) for p in self.peaks]

    def in_recession(self, m: str) -> bool:
        """Return whether the month lies in a contraction, from onset to trough."""
        return any(
            add_months(p, 1) <= m <= tr for p, tr in zip(self.peaks, self.troughs, strict=True)
        )

    def signal_outcomes(
        self, series: dict[str, float], lo: str, hi: str
    ) -> tuple[dict[str, Outcome], list[tuple[str, str, Outcome]]]:
        """Return the month-rule and episode-rule outcomes of the negative expansion months.

        A signal is each month from lo to hi with a negative spread outside recessions. The
        month rule asks for an onset in t+1..t+12; the episode rule, for consecutive signal
        months, an onset from the month after the first to twelve months after the last. A
        window that ends after the data is open; a window without an onset that ends after the
        last peak is a provisional miss.
        """
        last = max(series)
        onsets = self.onsets()
        neg = [
            m
            for m in sorted(series)
            if lo <= m <= hi and series[m] < 0 and not self.in_recession(m)
        ]

        def out(start: str, end: str) -> Outcome:
            if [o for o in onsets if add_months(start, 1) <= o <= add_months(end, 12)]:
                return "hit"
            if add_months(end, 12) > last:
                return "window open"
            return "miss" if add_months(end, 12) < self.peaks[-1] else "provisional miss"

        eps: list[list[str]] = []
        cur: list[str] = []
        for m in neg:
            if cur and add_months(cur[-1], 1) == m:
                cur.append(m)
            else:
                if cur:
                    eps.append(cur)
                cur = [m]
        if cur:
            eps.append(cur)
        months = {m: out(m, m) for m in neg}
        episodes = [(e[0], e[-1], out(e[0], e[-1])) for e in eps]
        return months, episodes
