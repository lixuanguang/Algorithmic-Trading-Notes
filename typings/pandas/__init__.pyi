# standard library imports
from collections.abc import Mapping
from typing import overload

# third party library imports
import numpy as np
from numpy.typing import NDArray

# Float-valued frames only.
class DataFrame:
    def __init__(self, data: Mapping[str, NDArray[np.float64]]) -> None: ...
    @overload
    def __getitem__(self, key: str) -> Series: ...
    @overload
    def __getitem__(self, key: list[str]) -> DataFrame: ...
    @property
    def values(self) -> NDArray[np.float64]: ...

class Series:
    @property
    def iloc(self) -> _ILocIndexer: ...

class _ILocIndexer:
    def __getitem__(self, i: int) -> np.float64: ...
