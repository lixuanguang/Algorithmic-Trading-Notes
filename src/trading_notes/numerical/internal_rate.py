"""The internal rate of return of dated yearly cash flows, shared by the investment examples."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq


def irr(cf: Sequence[float] | NDArray[np.float64]) -> float:
    """Return the internal rate of return of yearly cash flows, the first at time 0.

    The root is bracketed in (-99%, 1000%); brentq raises ValueError if the NPV does not change
    sign there.
    """
    return brentq(lambda r: sum(c / (1 + r) ** i for i, c in enumerate(cf)), -0.99, 10.0)
