# third party library imports
from pandas import DataFrame

class PredictionResults:
    def summary_frame(self, alpha: float = 0.05) -> DataFrame: ...
