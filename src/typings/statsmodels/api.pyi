# third party library imports
import numpy as np
from numpy.typing import NDArray
from statsmodels.regression.linear_model import OLS as OLS

def add_constant(data: NDArray[np.float64]) -> NDArray[np.float64]: ...
