"""One year of a timber stand: biological growth, harvest, stumpage price and land value."""

from trading_notes.records import Record


class TimberYear(Record):
    """The stand at the close of a year.

    Attributes:
        v1: Closing volume.
        p1: Closing stumpage price.
        proceeds: Harvest sold at the closing price.
        dist: Proceeds less cash costs, distributed.
        nav0: Opening NAV, timber plus land.
        nav1: Closing NAV.
        total: (NAV1 + distributions - NAV0) / NAV0.
    """

    v1: float
    p1: float
    proceeds: float
    dist: float
    nav0: float
    nav1: float
    total: float


class TimberStand(Record):
    """A stand of timber on its land at the opening of a year.

    Attributes:
        volume: Standing volume in cubic metres.
        price: Stumpage price per cubic metre.
        land: Land value.
    """

    volume: float
    price: float
    land: float

    def year(
        self, growth: float, harvest: float, dprice: float, dland: float, costs: float
    ) -> TimberYear:
        """Return one year of the stand.

        Args:
            growth: Biological growth as a share of the opening volume.
            harvest: Volume harvested and sold at the closing price.
            dprice: Change in the stumpage price.
            dland: Change in the land value.
            costs: Management, tax and harvest costs paid in cash.
        """
        p1 = self.price * (1 + dprice)
        v1 = self.volume * (1 + growth) - harvest
        proceeds = harvest * p1
        dist = proceeds - costs
        nav0, nav1 = self.volume * self.price + self.land, v1 * p1 + self.land * (1 + dland)
        return TimberYear(
            v1=v1,
            p1=p1,
            proceeds=proceeds,
            dist=dist,
            nav0=nav0,
            nav1=nav1,
            total=(nav1 + dist - nav0) / nav0,
        )
