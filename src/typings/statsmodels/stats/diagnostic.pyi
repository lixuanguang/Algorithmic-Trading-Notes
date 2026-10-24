from collections.abc import Sequence
from typing import Literal

import numpy as np
from numpy.typing import NDArray
from pandas import DataFrame

# (LM statistic, its p-value, F statistic, its p-value)
def het_breuschpagan(
    resid: NDArray[np.float64], exog_het: NDArray[np.float64]
) -> tuple[np.float64, np.float64, np.float64, np.float64]: ...
def het_white(
    resid: NDArray[np.float64], exog: NDArray[np.float64]
) -> tuple[np.float64, np.float64, np.float64, np.float64]: ...
def het_arch(
    resid: NDArray[np.float64], nlags: int, *, result_object: Literal[False]
) -> tuple[np.float64, np.float64, float, float]: ...

# A frame with lb_stat and lb_pvalue columns, one row per lag.
def acorr_ljungbox(x: NDArray[np.float64], lags: Sequence[int]) -> DataFrame: ...
