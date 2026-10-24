import numpy as np
from numpy.typing import NDArray

class Logit:
    def __init__(self, endog: NDArray[np.float64], exog: NDArray[np.float64]) -> None: ...
    def fit(self, disp: int = 1) -> LogitResults: ...

class LogitResults:
    @property
    def params(self) -> NDArray[np.float64]: ...
