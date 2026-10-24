"""Barclay Global Macro Index returns and their behaviour in equity down and up months."""

import calendar
import csv
import hashlib
import html
import math
import re
from pathlib import Path
from typing import Final, Literal, Self

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.newey_west import Month
from trading_notes.records import Record
from trading_notes.research.spreadsheets import xls_rows

type Floats = NDArray[np.float64]
type Factors = dict[Month, tuple[float, float]]

# The workbook header's month abbreviations; English under the default "C" time locale.
MONTH_NAMES: Final = list(calendar.month_abbr)[1:]


def barclay_page(path: Path) -> dict[Month, float]:
    """Return the monthly returns shown on BarclayHedge's index page, as decimals.

    Cells that are not a percentage, such as estimates, are left out.
    """
    t = path.read_text(errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    block = t[t.index("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec YTD") :]
    out = {}
    for m in re.finditer(r"(20\d\d) ((?:\S+ ){13})", block):
        y = int(m.group(1))
        cells = m.group(2).split()[:12]
        for k, c in enumerate(cells):
            if re.fullmatch(r"-?\d+\.\d+%", c):
                out[(y, k + 1)] = float(c[:-1]) / 100
    return out


def french_factors(path: Path) -> Factors:
    """Return Ken French's monthly Mkt-RF and RF, as decimals, from the factors CSV."""
    out = {}
    with path.open() as f:
        for line in f:
            p = [x.strip() for x in line.split(",")]
            if len(p[0]) == 6 and p[0].isdigit():
                out[(int(p[0][:4]), int(p[0][4:]))] = (float(p[1]) / 100, float(p[4]) / 100)
            elif out and (not p[0] or not p[0].isdigit()):
                break
    return out


class SharpeRatio(Record):
    """The monthly Sharpe ratio of excess returns with Lo's IID standard error.

    Attributes:
        value: Mean over standard deviation (ddof 1) of the monthly excess returns.
        se: Lo's normal-moment IID standard error sqrt((1 + SR^2 / 2) / T).
    """

    value: float
    se: float

    @classmethod
    def of(cls, excess: Floats) -> Self:
        """Return the Sharpe ratio of monthly excess returns."""
        sr = float(excess.mean() / excess.std(ddof=1))
        return cls(value=sr, se=math.sqrt((1 + sr**2 / 2) / len(excess)))


class RegimeMoments(Record):
    """The index in one set of benchmark months: mean, correlation and beta, with intervals.

    Attributes:
        n: The number of months.
        mean: The index's mean return.
        t: The mean's IID t statistic.
        correlation: The correlation with the benchmark.
        correlation_ci: Its 95% interval by Fisher z.
        beta: The OLS beta on the benchmark.
        beta_ci: Its 95% interval by t with n - 2 df.
    """

    n: int
    mean: float
    t: float
    correlation: float
    correlation_ci: tuple[float, float]
    beta: float
    beta_ci: tuple[float, float]

    @classmethod
    def of(cls, r: Floats, mk: Floats) -> Self:
        """Return the moments of index returns r against benchmark excess returns mk."""
        n = len(r)
        tmean = r.mean() / (r.std(ddof=1) / math.sqrt(n))
        rho = np.corrcoef(r, mk)[0, 1]
        z = np.arctanh(rho)
        half = 1.96 / math.sqrt(n - 3)
        lr = stats.linregress(mk, r)
        tcrit = stats.t.ppf(0.975, n - 2)
        return cls(
            n=n,
            mean=float(r.mean()),
            t=float(tmean),
            correlation=float(rho),
            correlation_ci=(math.tanh(z - half), math.tanh(z + half)),
            beta=float(lr.slope),
            beta_ci=(float(lr.slope - tcrit * lr.stderr), float(lr.slope + tcrit * lr.stderr)),
        )

    def describe(self, name: str, decimals: int) -> str:
        """Return the report line, the mean in percent and its t to `decimals` decimals."""
        lo, hi = self.correlation_ci
        b_lo, b_hi = self.beta_ci
        return (
            f"{name:5s} months (n {self.n}): mean {self.mean * 100:+.{decimals}f}% (t"
            f" {self.t:+.{decimals}f}), correlation {self.correlation:+.2f} "
            f"[{lo:+.2f}, {hi:+.2f}], beta {self.beta:+.3f} "
            f"[{b_lo:+.3f}, {b_hi:+.3f}]"
        )


class IndexMonths(Record):
    """The index's monthly returns beside the benchmark's, in month order.

    Attributes:
        months: The months.
        index: The index's net returns, as decimals.
        market: French's Mkt-RF, the benchmark; down months are those below zero.
        rf: French's risk-free rate.
    """

    months: list[Month]
    index: Floats
    market: Floats
    rf: Floats

    @classmethod
    def of(cls, months: list[Month], returns: dict[Month, float], factors: Factors) -> Self:
        """Return the given months of the index returns and the factors."""
        return cls(
            months=months,
            index=np.array([returns[m] for m in months]),
            market=np.array([factors[m][0] for m in months]),
            rf=np.array([factors[m][1] for m in months]),
        )

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read a table written by `write`."""
        with path.open() as f:
            rows = list(csv.DictReader(f))
        columns = ("barclay_global_macro", "mkt_rf", "rf")
        r, mk, rf = (np.array([float(row[c]) for row in rows]) for c in columns)
        months = [(int(y), int(m)) for y, m in (row["month"].split("-") for row in rows)]
        return cls(months=months, index=r, market=mk, rf=rf)

    def write(self, path: Path) -> None:
        """Write the month, index return, Mkt-RF and RF of each month, to four decimals."""
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["month", "barclay_global_macro", "mkt_rf", "rf"])
            for m, r, mk, rf in zip(self.months, self.index, self.market, self.rf, strict=True):
                w.writerow([f"{m[0]}-{m[1]:02d}", f"{r:.4f}", f"{mk:.4f}", f"{rf:.4f}"])

    def since(self, first: Month) -> Self:
        """Return the months from `first` on."""
        keep = [i for i, m in enumerate(self.months) if m >= first]
        return type(self)(
            months=[self.months[i] for i in keep],
            index=self.index[keep],
            market=self.market[keep],
            rf=self.rf[keep],
        )

    def returns_by_month(self) -> dict[Month, float]:
        """Return the index returns by month."""
        return {m: float(r) for m, r in zip(self.months, self.index, strict=True)}

    def span(self) -> str:
        """Return the first and last months as "YYYY-MM to YYYY-MM"."""
        (y0, m0), (y1, m1) = self.months[0], self.months[-1]
        return f"{y0}-{m0:02d} to {y1}-{m1:02d}"

    def all_months(self) -> str:
        """Return the mean, volatility and Sharpe ratio of every month."""
        r = self.index
        sr = SharpeRatio.of(r - self.rf)
        return (
            f"mean {r.mean() * 100:+.2f}%/month, vol"
            f" {r.std(ddof=1) * math.sqrt(12) * 100:.2f}%/yr, "
            f"monthly Sharpe (excess) {sr.value:+.3f} (Lo IID s.e. {sr.se:.3f}), "
            f"annualised {sr.value * math.sqrt(12):+.2f}"
        )

    def down(self) -> RegimeMoments:
        """Return the index's moments in benchmark down months."""
        down = self.market < 0
        return RegimeMoments.of(self.index[down], self.market[down])

    def up(self) -> RegimeMoments:
        """Return the index's moments in the other months."""
        up = self.market >= 0
        return RegimeMoments.of(self.index[up], self.market[up])

    def worst(self, kind: Literal["quicksort", "stable"]) -> str:
        """Return the mean benchmark and index returns in the ten lowest benchmark months.

        Args:
            kind: The sort that ranks the benchmark, which decides ties.
        """
        mk, r = self.market, self.index
        worst = np.argsort(mk, kind=kind)[:10]
        return (
            f"ten worst benchmark months: benchmark mean {mk[worst].mean() * 100:+.2f}%, index"
            f" mean {r[worst].mean() * 100:+.2f}% "
            f"({', '.join(f'{self.months[i][0]}-{self.months[i][1]:02d}' for i in sorted(worst))})"
        )

    def verdict(self) -> str:
        """Return the pre-set rule's verdict: protection if the down-month mean has t > 2."""
        down = self.down()
        ok = down.mean > 0 and down.t > 2
        return f"crisis protection {'supported' if ok else 'not supported'} in this window"


class IndexWorkbook(Record):
    """The index workbook from BarclayHedge's public Excel form.

    Attributes:
        returns: The monthly returns, as decimals.
        estimated: The months whose cells are marked as estimates.
        sha256: The workbook's SHA-256.
    """

    returns: dict[Month, float]
    estimated: set[Month]
    sha256: str

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read the first sheet: a year in column A and twelve monthly cells after it.

        Raises:
            ValueError: If the header is not the twelve months, or a non-numeric cell is not a
                '*'-marked estimate.
        """
        rows = xls_rows(path, 0)
        header = rows[1]
        if header[1:13] != MONTH_NAMES:
            raise ValueError(f"{path.name}: unexpected header {header}")
        out: dict[Month, float] = {}
        estimated: set[Month] = set()
        for row in rows[2:]:
            if not isinstance(row[0], float):
                continue
            y = int(row[0])
            for k in range(12):
                c = row[1 + k]
                if isinstance(c, float):
                    out[(y, k + 1)] = c
                elif c.strip():
                    if "*" not in c:
                        raise ValueError(f"{path.name}: unmarked non-numeric cell {(y, k + 1, c)}")
                    estimated.add((y, k + 1))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return cls(returns=out, estimated=estimated, sha256=digest)

    def window(self, factors: Factors, start: Month, end: Month) -> IndexMonths:
        """Return the months from start to end inclusive.

        Raises:
            ValueError: If a month is estimated or missing from the workbook or the factors.
        """
        months = [
            (y, m)
            for y in range(start[0], end[0] + 1)
            for m in range(1, 13)
            if start <= (y, m) <= end
        ]
        if [m for m in months if m in self.estimated]:
            raise ValueError("an estimated month falls inside the window")
        missing = [m for m in months if m not in self.returns or m not in factors]
        if missing:
            raise ValueError(f"months missing from the inputs: {missing}")
        return IndexMonths.of(months, self.returns, factors)

    def revisions(self, earlier: dict[Month, float]) -> list[tuple[Month, float, float]]:
        """Return the months whose earlier value differs from the workbook's at 4 decimals."""
        return [
            (m, earlier[m], round(self.returns[m], 4))
            for m in sorted(earlier)
            if abs(earlier[m] - round(self.returns[m], 4)) > 5e-5
        ]
