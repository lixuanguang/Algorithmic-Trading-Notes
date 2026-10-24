"""The discrete-time Solow model in per-worker terms, with labour and TFP growth."""

import numpy as np
from numpy.typing import NDArray

from trading_notes.records import Record

type Floats = NDArray[np.float64]


class SolowPath(Record):
    """One annual path of the per-worker Solow model.

    Attributes:
        y: Output per worker.
        k: Capital per worker at the start of each year.
        k_normalized: Capital per effective worker, k / A^(1/(1 - alpha)).
    """

    y: Floats
    k: Floats
    k_normalized: Floats


class SolowModel(Record):
    """Y = A K^alpha L^(1 - alpha), with capital depreciating and L and A growing annually.

    Attributes:
        capital_share: alpha.
        depreciation: delta.
        labour_growth: n.
        tfp_growth: theta.
    """

    capital_share: float
    depreciation: float
    labour_growth: float
    tfp_growth: float

    def path(self, s: float, k0: float, years: int = 400) -> SolowPath:
        """Return the annual path from capital per worker k0 with saving rate s and A0 = 1."""
        a_s, d_, n_, theta = (
            self.capital_share,
            self.depreciation,
            self.labour_growth,
            self.tfp_growth,
        )
        a, k = 1.0, k0
        ys: list[float] = []
        raw_k: list[float] = []
        normalized_k: list[float] = []
        for _ in range(years):
            y = a * k**a_s
            ys.append(y)
            raw_k.append(k)
            normalized_k.append(k / a ** (1 / (1 - a_s)))
            k = (s * y + (1 - d_) * k) / (1 + n_)
            a *= 1 + theta
        return SolowPath(y=np.array(ys), k=np.array(raw_k), k_normalized=np.array(normalized_k))

    def effective_growth(self) -> float:
        """Return balanced-path growth of output per worker, (1 + theta)^(1/(1-alpha)) - 1."""
        return float((1 + self.tfp_growth) ** (1 / (1 - self.capital_share)) - 1)

    def normalized_steady_state(self, s: float) -> float:
        """Return the steady-state capital per effective worker with saving rate s."""
        a_s, d_, n_ = self.capital_share, self.depreciation, self.labour_growth
        return float((s / ((1 + n_) * (1 + self.effective_growth()) - (1 - d_))) ** (1 / (1 - a_s)))

    def convergence_speed(self) -> float:
        """Return lambda = (1 - alpha)(n + theta / (1 - alpha) + delta), near the steady state."""
        a_s = self.capital_share
        return (1 - a_s) * (self.labour_growth + self.tfp_growth / (1 - a_s) + self.depreciation)
