from typing import Literal

import numpy as np
from numpy.typing import NDArray

# Critical values at 1, 5 and 10 percent of the Dickey-Fuller distribution for N variables.
def mackinnoncrit(
    N: int = 1, regression: Literal["c", "n", "ct", "ctt"] = "c", nobs: float = ...
) -> NDArray[np.float64]: ...
