"""Money-market instruments on act/360: repos, discount paper and repo margin."""

from trading_notes.records import Record


class Repo(Record):
    """A repurchase agreement: cash lent against collateral, repaid with simple interest.

    Attributes:
        cash: The amount lent.
        rate: The repo rate, annual, act/360 simple.
        days: The term in days.
    """

    cash: float
    rate: float
    days: int

    def interest(self) -> float:
        """Return cash x rate x days / 360."""
        return self.cash * self.rate * self.days / 360

    def repurchase_price(self) -> float:
        """Return the cash repaid at the end: the loan plus interest."""
        return self.cash + self.interest()


class DiscountPaper(Record):
    """Paper quoted on a discount basis, such as commercial paper: price = face (1 - d t).

    Attributes:
        discount_rate: d, annual, act/360.
        days: The term in days.
    """

    discount_rate: float
    days: int

    @property
    def year_fraction(self) -> float:
        """Return days / 360."""
        return self.days / 360

    def face_for(self, proceeds: float) -> float:
        """Return the face value that raises the given proceeds."""
        return proceeds / (1 - self.discount_rate * self.year_fraction)

    def money_market_yield(self) -> float:
        """Return interest over proceeds, annualised on act/360: d / (1 - d t)."""
        return self.discount_rate / (1 - self.discount_rate * self.year_fraction)


class RepoMargin(Record):
    """A repo whose loan is kept at a fixed fraction of the collateral's market value.

    Attributes:
        loan: The cash lent.
        loan_to_value: Loan over required collateral value: 0.98 for a 2% haircut on value.
    """

    loan: float
    loan_to_value: float

    def required_collateral(self) -> float:
        """Return the collateral value that the loan needs."""
        return self.loan / self.loan_to_value

    def deficit(self, collateral: float) -> float:
        """Return the securities to post to restore the margin at the collateral's value."""
        return self.required_collateral() - collateral

    def cash_repayment(self, collateral: float) -> float:
        """Return the cash to repay so that the loan is again loan_to_value of the collateral."""
        return self.loan - self.loan_to_value * collateral
