# third party library imports
from pandas import DataFrame

# A model built from a formula is an OLS whose results hold pandas objects; it is typed here
# only as far as anova_lm takes its results.
class FormulaOLS:
    def fit(self) -> FormulaResults: ...

class FormulaResults: ...

def ols(formula: str, data: DataFrame) -> FormulaOLS: ...
