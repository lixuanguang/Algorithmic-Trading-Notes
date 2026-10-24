"""A let office building's net operating income by year."""

from trading_notes.records import Record


class LetBuilding(Record):
    """A multi-let building: rents and costs per square foot a year.

    Attributes:
        area: Lettable area in square feet.
        rent: Rent per square foot.
        loss: Collection loss as a share of rent.
        other: Other income a year.
        tax: Property tax per square foot.
        fixed: Fixed operating cost per square foot.
        variable: Variable cost per occupied square foot.
        reserve: Capital reserve per square foot.
    """

    area: float
    rent: float
    loss: float
    other: float
    tax: float
    fixed: float
    variable: float
    reserve: float

    def noi(
        self, year: int, g: float = 0.025, occ_path: tuple[float, ...] = (0.93, 0.94, 0.95)
    ) -> float:
        """Return the NOI in a year, rents and costs growing at g, occupancy on a path.

        The last occupancy of the path holds for every later year.
        """
        occ = occ_path[min(year - 1, len(occ_path) - 1)]
        f = (1 + g) ** (year - 1)
        gross = self.area * self.rent * f * occ * (1 - self.loss) + self.other * f
        opex = (
            self.area * (self.tax + self.fixed + self.reserve) * f
            + self.area * occ * self.variable * f
        )
        return gross - opex
