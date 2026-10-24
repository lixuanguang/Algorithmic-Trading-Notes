"""Recoveries by absolute priority, and Chapter 11 class acceptance and confirmation."""

from trading_notes.numerical.records import Record


class RecoveryWaterfall(Record):
    """Claims paid in order of priority out of an enterprise value.

    Attributes:
        claims: (class, claim amount) from most senior to most junior.
    """

    claims: tuple[tuple[str, float], ...]

    def recoveries(self, ev: float) -> dict[str, float]:
        """Return each class's recovery rate at enterprise value ev, and the residual to equity."""
        rec: dict[str, float] = {}
        left = ev
        for k, c in self.claims:
            pay = min(left, c)
            rec[k] = pay / c
            left -= pay
        rec["equity"] = left
        return rec

    def fulcrum(self, ev: float) -> str:
        """Return the most senior class not paid in full: the class that takes the new equity."""
        for k, _ in self.claims:
            if self.recoveries(ev)[k] < 1.0:
                return k
        return "equity"


class ClassVote(Record):
    """The ballots cast in one class of claims.

    Attributes:
        ballots: (claim amount, accepts) for each holder voting.
    """

    ballots: tuple[tuple[float, bool], ...]

    def accepts(self) -> bool:
        """Return whether the class accepts under 11 U.S.C. 1126(c).

        At least two-thirds in amount and more than half in number of the claims voting accept.
        """
        yes = [a for a, v in self.ballots if v]
        amount = sum(yes) / sum(a for a, _ in self.ballots)
        number = len(yes) / len(self.ballots)
        return amount >= 2 / 3 and number > 0.5


class PlanConfirmation(Record):
    """The facts that decide whether a Chapter 11 plan can be confirmed.

    The remaining 1129(a) tests (feasibility, best interests) are assumed met.

    Attributes:
        impaired_accepting_classes: How many impaired classes accepted.
        dissenting_impaired: Whether an impaired class rejected.
        junior_gets_value: Whether a class junior to the dissenter receives value.
        unfair_discrimination: Whether the plan discriminates unfairly against the dissenter.
    """

    impaired_accepting_classes: int
    dissenting_impaired: bool
    junior_gets_value: bool = False
    unfair_discrimination: bool = False

    def confirmable(self) -> bool:
        """Return whether the plan can be confirmed under 1129(a)(8), (a)(10) and (b).

        A dissenting impaired class can be crammed down only if another impaired class
        accepted and the plan is fair and equitable (for unsecured claims, full value or
        nothing to juniors) and does not discriminate unfairly.
        """
        if not self.dissenting_impaired:
            return self.impaired_accepting_classes >= 1
        return (
            self.impaired_accepting_classes >= 1
            and not self.junior_gets_value
            and not self.unfair_discrimination
        )
