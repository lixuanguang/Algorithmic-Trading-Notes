import numpy as np
from numpy.typing import NDArray

# A float and a NumPy scalar for one restriction; arrays for several.
class ContrastResults:
    @property
    def fvalue(self) -> float | NDArray[np.float64]: ...
    @property
    def pvalue(self) -> np.float64 | NDArray[np.float64]: ...
