# standard library imports
from typing import Literal

# third party library imports
import numpy as np
from numpy.typing import NDArray

# With autolag=None and result_object=False: (statistic, p-value, lags used, observations,
# critical values by level).
def adfuller(
    x: NDArray[np.float64],
    maxlag: int | None = None,
    regression: Literal["c", "ct", "ctt", "n"] = "c",
    autolag: None = None,
    *,
    result_object: Literal[False],
) -> tuple[float, float, int, int, dict[str, np.float64]]: ...
