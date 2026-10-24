"""The IFRS classification of an investment in another entity, from the facts of the holding."""

from trading_notes.records import Record


class InvestmentFacts(Record):
    """The facts that classify an investment under IFRS 10, IFRS 11, IAS 28 and IFRS 9.

    Control is derived from its three elements (IFRS 10 para. 7), not given as a conclusion;
    designing a vehicle or bearing its losses is not an input to power (paras. B51, B54).

    Attributes:
        stake: The share of the voting rights held.
        influence_evidence: Whether other evidence shows significant influence.
        power: Whether the investor directs the relevant activities, or None when the facts
            about who does are not given.
        variable_returns: Whether it is exposed to variable returns.
        principal: Whether it acts as principal rather than agent.
        joint: Whether control is joint.
        rights: For a joint arrangement, "net assets" (a joint venture) or rights to the assets
            and obligations for the liabilities (a joint operation).
    """

    stake: float
    influence_evidence: bool = False
    power: bool | None = False
    variable_returns: bool = False
    principal: bool = True
    joint: bool = False
    rights: str = "net assets"

    def classify(self) -> str:
        """Classify by IFRS 10 control, IFRS 11 joint control, IAS 28 influence, else IFRS 9."""
        if self.power is None and self.variable_returns:
            return (
                "not determinable: identify who holds substantive rights over the relevant"
                " activities"
            )
        if self.power and self.variable_returns and self.principal:
            return "subsidiary: consolidate (IFRS 10)"
        if self.joint:
            return (
                "joint venture: equity method (IFRS 11.24)"
                if self.rights == "net assets"
                else "joint operation: own share of assets, liabilities, revenue and expenses "
                "(IFRS 11.20)"
            )
        if self.stake >= 0.20 or self.influence_evidence:
            return "associate: equity method (IAS 28.16)"
        if self.variable_returns and self.stake == 0.0:
            return (
                "interest in an unconsolidated structured entity: IFRS 9 measurement, "
                "IFRS 12 disclosure"
            )
        return "financial asset: FVPL, or FVOCI if elected for equity not held for trading (IFRS 9)"
