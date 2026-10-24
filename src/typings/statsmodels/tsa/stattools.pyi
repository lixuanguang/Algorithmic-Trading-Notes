from typing import Literal, overload

import numpy as np
from numpy.typing import NDArray

# With result_object=False and autolag=None: (statistic, p-value, lags used, observations,
# critical values by level); with an information criterion choosing the lag, its best value too.
@overload
def adfuller(
    x: NDArray[np.float64],
    maxlag: int | None = None,
    regression: Literal["c", "ct", "ctt", "n"] = "c",
    *,
    autolag: None,
    result_object: Literal[False],
) -> tuple[float, float, int, int, dict[str, np.float64]]: ...
@overload
def adfuller(
    x: NDArray[np.float64],
    maxlag: int | None = None,
    regression: Literal["c", "ct", "ctt", "n"] = "c",
    autolag: Literal["AIC"] = "AIC",
    *,
    result_object: Literal[False],
) -> tuple[float, float, int, int, dict[str, np.float64], np.float64]: ...

# (statistic, p-value, lags used, critical values by level)
def kpss(
    x: NDArray[np.float64],
    regression: Literal["c", "ct"] = "c",
    nlags: Literal["auto"] | int = "auto",
    *,
    result_object: Literal[False],
) -> tuple[np.float64, np.float64, int, dict[str, float]]: ...
def acf(x: NDArray[np.float64], nlags: int | None = None) -> NDArray[np.float64]: ...

# (t statistic, p-value, critical values at 1, 5 and 10 percent)
def coint(
    y0: NDArray[np.float64], y1: NDArray[np.float64]
) -> tuple[float, float, NDArray[np.float64]]: ...
