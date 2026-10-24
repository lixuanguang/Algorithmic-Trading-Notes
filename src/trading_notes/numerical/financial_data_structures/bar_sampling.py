"""The tick rule, imbalance and runs bars, and the symmetric CUSUM filter (AFML chap. 2)."""

from typing import Final, Literal

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.records import Record

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]

BURN_IN: Final = 100


def tick_rule(p: Floats, b0: int) -> Ints:
    """b_t = sign(dp_t), carried forward when dp_t = 0; b0 is the previous bar's terminal value.

    Returns one sign per price change, so fewer than two prices give an empty integer array.
    """
    b, prev = [], b0
    for dp in np.diff(p):
        prev = prev if dp == 0 else int(np.sign(dp))
        b.append(prev)
    return np.array(b, dtype=np.int64)


def _side_mean(v: Floats, side: NDArray[np.bool_]) -> float:
    """Return the mean volume of one side's ticks, NaN (without a warning) if it has none."""
    return float(v[side].mean()) if side.any() else np.nan


class ImbalanceBars(Record):
    """Tick or volume imbalance bars, or runs bars, with expectations from earlier bars only.

    Attributes:
        e_t0: The initial expected bar length E0[T].
        alpha: The weight of the bar just closed in each exponentially weighted update.
        kind: Whether the imbalance counts ticks or signed volume.
        runs: Runs bars (the larger one-sided total) instead of imbalance bars.
    """

    e_t0: float
    alpha: float = 0.1
    kind: Literal["tick", "volume"] = "tick"
    runs: bool = False

    def bar_ends(self, b: Ints, v: Floats) -> Ints:
        """Return the index of each bar's last tick, after a 100-tick burn-in.

        Each bar's threshold uses expectations fixed at its start. No bar closes within the
        burn-in, so a flow of at most 100 ticks, like one where no threshold is reached,
        gives an empty integer array.

        Args:
            b: The tick signs, +1 or -1.
            v: The volume of each tick, as long as b.

        Raises:
            ValueError: If b and v differ in length, or volume runs bars are asked for and
                the burn-in has no buy or no sell from which to set its expected volume.
        """
        if len(b) != len(v):
            raise ValueError(f"{len(b)} signs but {len(v)} volumes")
        if len(b) <= BURN_IN:
            return np.empty(0, dtype=np.int64)
        alpha, kind, runs = self.alpha, self.kind, self.runs
        ends: list[int] = []
        warm_b, warm_v = b[:BURN_IN], v[:BURN_IN]  # warm-up expectations from a burn-in window
        eT, ep = self.e_t0, (warm_b == 1).mean()
        ebv = (warm_b * warm_v).mean()
        evb, evs = _side_mean(warm_v, warm_b == 1), _side_mean(warm_v, warm_b == -1)
        if runs and kind == "volume" and np.isnan(evb + evs):
            raise ValueError("the burn-in needs buys and sells for volume runs bars")
        t = BURN_IN
        start = t
        theta: np.int64 | np.float64
        thresh: float
        while t < len(b):
            seg_b, seg_v = b[start : t + 1], v[start : t + 1]
            if not runs:
                if kind == "tick":
                    theta = abs(seg_b.sum())
                else:
                    theta = abs((seg_b * seg_v).sum())
                thresh = eT * abs(2 * ep - 1) if kind == "tick" else eT * abs(ebv)
            else:
                if kind == "tick":
                    theta = max((seg_b == 1).sum(), (seg_b == -1).sum())
                    thresh = eT * max(ep, 1 - ep)
                else:
                    theta = max(seg_v[seg_b == 1].sum(), seg_v[seg_b == -1].sum())
                    thresh = eT * max(ep * evb, (1 - ep) * evs)
            if theta >= thresh:
                T = t - start + 1
                ends.append(t)
                # update the averages with the bar just closed; the next threshold uses closed bars
                eT = (1 - alpha) * eT + alpha * T
                ep = (1 - alpha) * ep + alpha * (seg_b == 1).mean()
                ebv = (1 - alpha) * ebv + alpha * (seg_b * seg_v).mean()
                if (seg_b == 1).any():
                    evb = (1 - alpha) * evb + alpha * seg_v[seg_b == 1].mean()
                if (seg_b == -1).any():
                    evs = (1 - alpha) * evs + alpha * seg_v[seg_b == -1].mean()
                start = t + 1
            t += 1
        return np.array(ends, dtype=np.int64)


class CusumFilter(Record):
    """The symmetric CUSUM filter with reset of Snippet 2.4, with E_{t-1}[y_t] = y_{t-1}.

    Attributes:
        threshold: h; an event fires when a cumulative sum moves strictly beyond it.
    """

    threshold: float

    def events(self, x: Floats) -> list[int]:
        """Return the indices at which the filter fires; only the triggered side resets."""
        ev, sp, sn = [], 0.0, 0.0
        for i in range(1, len(x)):
            dx = x[i] - x[i - 1]
            sp, sn = max(0.0, sp + dx), min(0.0, sn + dx)
            if sn < -self.threshold:
                sn = 0.0
                ev.append(i)
            elif sp > self.threshold:
                sp = 0.0
                ev.append(i)
        return ev
