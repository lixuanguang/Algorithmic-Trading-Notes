# third party library imports
import numpy as np
from numpy.typing import NDArray

class OLSInfluence:
    @property
    def resid_studentized_internal(self) -> NDArray[np.float64]: ...
