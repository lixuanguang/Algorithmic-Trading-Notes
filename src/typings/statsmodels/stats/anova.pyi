from pandas import DataFrame
from statsmodels.formula.api import FormulaResults

def anova_lm(*args: FormulaResults) -> DataFrame: ...
