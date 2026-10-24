"""FRED series downloaded as CSV files of date and value, keyed by calendar month."""

import csv
from pathlib import Path

from trading_notes.numerical.newey_west import Month

MISSING = ("", ".")


def observations(path: Path) -> list[tuple[Month, float]]:
    """Return the reported (month, value) pairs of a FRED CSV in file order, skipping blanks."""
    out = []
    with path.open() as f:
        r = csv.reader(f)
        next(r)
        for d, v in r:
            if v not in MISSING:
                y, m, _ = map(int, d.split("-"))
                out.append(((y, m), float(v)))
    return out


def monthly_values(path: Path) -> dict[Month, float]:
    """Return a monthly series by month; a month reported twice keeps its last value."""
    return dict(observations(path))


def monthly_means(path: Path) -> dict[Month, float]:
    """Return the mean of each month's observations, for a daily or weekly series."""
    acc: dict[Month, list[float]] = {}
    for month, v in observations(path):
        acc.setdefault(month, []).append(v)
    return {k: sum(v) / len(v) for k, v in acc.items()}
