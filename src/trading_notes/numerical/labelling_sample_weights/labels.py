"""Triple-barrier labels, label concurrency, uniqueness and the sequential bootstrap."""

from collections.abc import Callable, Sequence
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]


class TripleBarrier(Record):
    """Profit-taking and stop-loss barriers on a close path, with a vertical barrier at its end.

    Attributes:
        profit_take: The return at which the upper barrier is touched, or None.
        stop_loss: The loss at which the lower barrier is touched, or None.
        side: +1 for a long position, -1 for a short one.
        label_vertical: How a path that touches neither barrier is labelled: by the sign of
            its final return, or 0.
    """

    profit_take: float | None
    stop_loss: float | None
    side: int = 1
    label_vertical: Literal["sign", "zero"] = "sign"

    def label(self, path: Floats) -> tuple[int, int]:
        """Return (label, index of the first touch) for one close path."""
        r = (path / path[0] - 1) * self.side
        for k in range(1, len(path)):
            if self.profit_take is not None and r[k] >= self.profit_take:
                return 1, k
            if self.stop_loss is not None and r[k] <= -self.stop_loss:
                return -1, k
        last = r[-1]
        return (int(np.sign(last)) if self.label_vertical == "sign" else 0), len(path) - 1


class LabelIndicators(Record):
    """The indicator matrix 1{t, i}: one row per time, one column per label.

    Attributes:
        matrix: 1 where label i uses the return of row t, else 0.
    """

    matrix: Floats

    @classmethod
    def closed_spans(cls, spans: Sequence[tuple[int, int]], rows: int) -> LabelIndicators:
        """Return the indicators of labels using rows a..b inclusive, for each span (a, b)."""
        ind = np.zeros((rows, len(spans)))
        for j, (a, b) in enumerate(spans):
            ind[a : b + 1, j] = 1
        return cls(matrix=ind)

    @classmethod
    def by_rule(
        cls,
        spans: Sequence[tuple[int, int]],
        rows: Sequence[int],
        rule: Callable[[int, int, int], float],
    ) -> LabelIndicators:
        """Return the indicators rule(a, b, t), one row per time in rows and one column per span.

        Args:
            spans: Each label's (a, b).
            rows: The times indexing the rows, in order.
            rule: rule(a, b, t), the indicator that the label on (a, b) uses the return at t.
        """
        m = np.zeros((len(rows), len(spans)))
        for j, (a, b) in enumerate(spans):
            for i, t in enumerate(rows):
                m[i, j] = rule(a, b, t)
        return cls(matrix=m)

    def concurrency(self) -> Floats:
        """Return c_t, the number of labels using each row."""
        c: Floats = self.matrix.sum(1)
        return c

    def average_uniqueness(self) -> Floats:
        """Return each label's average uniqueness; a row no label uses counts 0, not 0/0."""
        m = self.matrix
        c = self.concurrency()
        u = np.divide(m, c[:, None], out=np.zeros_like(m), where=c[:, None] > 0)
        avg: Floats = u.sum(0) / m.sum(0)
        return avg

    def sample_uniqueness(self, drawn: Sequence[int]) -> np.float64:
        """Return the mean average uniqueness of the labels drawn, repeats included."""
        return np.float64(LabelIndicators(matrix=self.matrix[:, drawn]).average_uniqueness().mean())

    def sequential_probabilities(self, drawn: Sequence[int]) -> tuple[Floats, Floats]:
        """Return each label's average uniqueness given those drawn, and the draw probabilities."""
        ind = self.matrix
        base = ind[:, drawn].sum(1) if drawn else np.zeros(ind.shape[0])
        means = []
        for j in range(ind.shape[1]):
            uj = ind[:, j] / (1 + base)
            means.append(uj[ind[:, j] > 0].mean())
        ub = np.array(means)
        return ub, ub / ub.sum()

    def sequential_bootstrap(self, n: int, rng: np.random.Generator) -> list[int]:
        """Draw n labels by the sequential bootstrap, one generator choice per draw."""
        drawn: list[int] = []
        for _ in range(n):
            _, pr = self.sequential_probabilities(drawn)
            drawn.append(rng.choice(self.matrix.shape[1], p=pr))
        return drawn


class TimeDecay(Record):
    """Piecewise-linear decay d(x) = max(0, a + b x) of weights in cumulative uniqueness x.

    Attributes:
        last: c, the factor of the oldest observation as x tends to 0; negative c zeroes the
            oldest share -c of cumulative uniqueness.
    """

    last: float

    def coefficients(self, total: float) -> tuple[float, float]:
        """Return (a, b) with d(total) = 1, for total cumulative uniqueness S."""
        c = self.last
        b = (1 - c) / total if c >= 0 else 1 / ((c + 1) * total)
        return 1 - b * total, b
