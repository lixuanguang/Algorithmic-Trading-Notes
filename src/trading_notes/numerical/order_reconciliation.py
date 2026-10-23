"""Offline, synthetic illustration behind mech:order-state-reconciliation.

Source verification (2026-10-17); corrected the same day. Not a test against any venue, broker or
FIX engine, and not production logic: messages are records whose fields are named after FIX tags,
the parent intents are invented, and no network or file is touched.

Correction. The first version released every order that was terminal and reconciled "for
resubmission", so a fully filled order (B1) became a resubmission candidate. Being reconciled
says only that our record of an order agrees with the recipient's; whether anything may be sent
again depends on two further facts, kept separate here:
  * reconciled state per order: fills applied once by ExecID(17), compared with the
    ExecType(150)=I status reply (OrdStatus(39), CumQty(14), LeavesQty(151)); a reply whose
    CumQty exceeds the fills applied is a break (a missing execution), and Pending Cancel
    (OrdStatus 6) is unresolved;
  * remaining authorised quantity per parent intent: the intent's quantity less what is filled
    and less what could still fill (LeavesQty of live orders, and the full open quantity of
    unresolved orders and of orders with a break);
  * a valid intent: the parent instruction is still wanted (not cancelled by the strategy or a
    risk control).
A replacement order may be proposed only for an intent that is valid, has every child order
reconciled and resolved, and has remaining authorised quantity; its size is that remaining
quantity.
Cases: a fully filled order; a partially filled order then cancelled (with a valid and with a
withdrawn intent); an order in Pending Cancel; a duplicate execution report (PossDupFlag(43)=Y)
and an unseen PossDup; a missing execution found from a status reply.

Second correction (empirical extensions (2026-10-17)). OrdStatus(39)=3, Done for Day, was in
TERMINAL. FIX Latest (Orchestra, FIXTradingCommunity/orchestrations commit cd24169) describes it
as "Order not, or partially, filled; no further executions forthcoming for the trading day":
complete for today, not ended. Expired (C) is the state of an order "canceled in broker's system
due to TimeInForce(59) instructions"; a GoodTillCancel order "remains in effect until it is
either executed or canceled"; and LeavesQty(151) "could be 0" under Done for Day. FIX 4.4
Appendix D (read through OnixS's FIX dictionary mirror, not the FIX Trading Community's own copy)
shows both cases: a day order ends Done for Day with LeavesQty 0 (A.1.b, "Assuming day order"),
while a GTC order reports Done for Day with LeavesQty 8000 and is restated next morning with
ExecType D and ExecRestatementReason "GTC renewal/restatement" (H.1.a). So:
  * lifetime-terminal states are Filled (2), Canceled (4), Rejected (8) and Expired (C) only;
  * Done for Day ends the order's lifetime only for TimeInForce Day (0, or absent) and only where
    the venue's own rules say a day order receives no later Expired or Canceled; otherwise the
    order is dormant;
  * a dormant good-till order (GTC 1, GTD 6, or TimeInForce unknown) can fill next session for
    OrderQty - CumQty, whatever LeavesQty it reported, until a cancellation or expiry is
    confirmed.
The earlier cases (filled, partial-then-cancelled, Pending Cancel, duplicates, missing fill) are
unchanged.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.order_reconciliation
(standard library). Exits non-zero on failure.
"""

# standard library imports
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

# project library imports
from trading_notes.numerical.report import CheckReport

TERMINAL: Final = frozenset(
    {"2", "4", "8", "C"}
)  # lifetime ends: Filled, Canceled, Rejected, Expired
DONE_FOR_DAY: Final = "3"  # complete for today only
UNRESOLVED: Final = frozenset({"6", "E", "A"})  # Pending Cancel, Pending Replace, Pending New
DAY: Final = "0"  # TimeInForce(59) Day
# TERMINAL before the second correction, with Done for Day (3) in it.
OLD_TERMINAL: Final = frozenset({"2", "3", "4", "8", "C"})


@dataclass(frozen=True)
class Intent:
    """A parent instruction from the strategy.

    Attributes:
        qty: Quantity authorised.
        valid: Whether it is still wanted (not cancelled by the strategy or a risk control).
    """

    qty: int
    valid: bool


@dataclass(frozen=True)
class Order:
    """A child order as in our order log.

    Attributes:
        intent: Key of the parent intent it works.
        qty: Child order quantity, OrderQty(38).
        tif: TimeInForce(59) as logged, or None where our log does not record it. An absent
            TimeInForce means Day under FIX, but unknown in our log is not absent, so None is
            never read as Day.
    """

    intent: str
    qty: int
    tif: str | None = None


@dataclass(frozen=True)
class Execution:
    """An execution report as received.

    Attributes:
        cl_ord_id: ClOrdID(11) of the order filled.
        exec_id: ExecID(17), the key fills are applied once by.
        last_qty: LastQty(32), the quantity of this fill.
        poss_dup: PossDupFlag(43)=Y: possibly a resent copy. It decides nothing: a PossDup whose
            ExecID is unseen is applied, since the first copy may never have arrived.
    """

    cl_ord_id: str
    exec_id: str
    last_qty: int
    poss_dup: bool = False


@dataclass(frozen=True)
class StatusReply:
    """The recipient's view of one order.

    Attributes:
        ord_status: OrdStatus(39).
        cum_qty: CumQty(14), the quantity filled so far.
        leaves_qty: LeavesQty(151), the quantity still working as reported.
        exec_type: ExecType(150): I for a status reply after OrderMassStatusRequest(35=AF), D
            for a restatement.
        restatement_reason: ExecRestatementReason(378) of a restatement (1 = GT renewal), or
            None.
    """

    ord_status: str
    cum_qty: int
    leaves_qty: int
    exec_type: str = "I"
    restatement_reason: int | None = None


@dataclass(frozen=True)
class OrderState:
    """The reconciled state of one order (steps 2-4).

    Attributes:
        reconciled: Whether the reply's CumQty equals the fills applied.
        break_qty: Reply CumQty less fills applied; positive for a missing execution.
        resolved: Whether the order is not in a pending state (Pending Cancel, Replace or New).
        terminal: Whether the order's lifetime has ended.
        dormant: Done for Day without the lifetime ending: it can fill in a later session.
        could_fill: Quantity that could still fill.
        cum: Conservative exposure: the larger of the fills applied and the reply's CumQty.
    """

    reconciled: bool
    break_qty: int
    resolved: bool
    terminal: bool
    dormant: bool
    could_fill: int
    cum: int


INTENTS: Final[Mapping[str, Intent]] = MappingProxyType(
    {  # parent instructions from the strategy: quantity authorised and whether still wanted
        "P-full": Intent(200, True),
        "P-part": Intent(300, True),
        "P-withdrawn": Intent(150, False),
        "P-pending": Intent(100, True),
        "P-missing": Intent(300, True),
        "P-gtc": Intent(10000, True),
        "P-day": Intent(500, True),
    }
)
ORDERS: Final[Mapping[str, Order]] = MappingProxyType(
    {  # ClOrdID -> parent intent and child quantity, as in our order log
        "F1": Order("P-full", 200),
        "X1": Order("P-part", 300),
        "W1": Order("P-withdrawn", 150),
        "C1": Order("P-pending", 100),
        "M1": Order("P-missing", 300),
        "G1": Order("P-gtc", 10000, tif="1"),
        "D1": Order("P-day", 500, tif=DAY),
    }
)
# Venue rule read for D1's venue: a Done for Day day order receives nothing later.
VENUE_DAY_DFD_FINAL: Final[Mapping[str, bool]] = MappingProxyType({"D1": True})
STREAM: Final = (  # execution reports received around a disconnect
    Execution("F1", "f1", 120),
    Execution("F1", "f1", 120, poss_dup=True),  # resent copy of f1
    Execution("F1", "f2", 80, poss_dup=True),  # unseen: may never have arrived
    Execution("X1", "x1", 120),
    Execution("W1", "w1", 50),
    Execution("M1", "m1", 100),
    Execution("G1", "g1", 2000),
    Execution("D1", "d1", 300),
)
STATUS: Final[Mapping[str, StatusReply]] = MappingProxyType(
    {  # ExecType=I replies after OrderMassStatusRequest(35=AF)
        "F1": StatusReply("2", 200, 0),
        "X1": StatusReply("4", 120, 0),
        "W1": StatusReply("4", 50, 0),
        "C1": StatusReply("6", 0, 100),
        "M1": StatusReply("1", 250, 50),
        "G1": StatusReply("3", 2000, 0),  # Done for Day, zero leaves reported (allowed by FIX)
        "D1": StatusReply("3", 300, 0),
    }
)


class Reconciler:
    """Fills applied once by ExecID, and the reconciled state and proposals they imply.

    Each instance owns the ExecIDs it has applied and the fills per order; the intents, orders
    and venue rules it reads are never changed.
    """

    def __init__(self, intents: Mapping[str, Intent], orders: Mapping[str, Order]) -> None:
        """Start with no executions applied.

        Args:
            intents: Parent intents by key.
            orders: Child orders by ClOrdID; each names one of `intents`.
        """
        self._intents = intents
        self._orders = orders
        self._seen: set[str] = set()
        self._filled: dict[str, int] = {k: 0 for k in orders}

    @property
    def filled(self) -> dict[str, int]:
        """Return the fills applied per ClOrdID, as a new dict."""
        return dict(self._filled)

    def has_applied(self, exec_id: str) -> bool:
        """Return whether the execution with this ExecID has been applied."""
        return exec_id in self._seen

    def apply(self, stream: Iterable[Execution]) -> None:
        """Step 1: apply each execution once, keyed by ExecID, whatever its PossDupFlag."""
        for m in stream:
            if m.exec_id in self._seen:
                continue
            self._seen.add(m.exec_id)
            self._filled[m.cl_ord_id] += m.last_qty

    def lifetime_ended(
        self, k: str, r: StatusReply, venue_day_dfd_final: Mapping[str, bool]
    ) -> bool:
        """Return whether order k's lifetime has ended, given its status reply.

        Args:
            k: ClOrdID.
            r: Its status reply.
            venue_day_dfd_final: Per ClOrdID, whether its venue's rules say a Done for Day day
                order receives no later Expired or Canceled; missing means not read.
        """
        if r.ord_status in TERMINAL:
            return True
        if r.ord_status == DONE_FOR_DAY:
            # absent TimeInForce means Day under FIX, but unknown in our log is not absent
            tif = self._orders[k].tif
            return tif == DAY and venue_day_dfd_final.get(k, False)
        return False

    def reconcile(
        self, k: str, r: StatusReply, venue_day_dfd_final: Mapping[str, bool]
    ) -> OrderState:
        """Steps 2-4: compare order k's applied fills with its status reply.

        Args:
            k: ClOrdID.
            r: Its status reply.
            venue_day_dfd_final: Venue rules read, as for `lifetime_ended`.
        """
        brk = r.cum_qty - self._filled[k]
        unresolved = r.ord_status in UNRESOLVED
        ended = self.lifetime_ended(k, r, venue_day_dfd_final)
        dormant = r.ord_status == DONE_FOR_DAY and not ended
        if brk == 0 and not unresolved and not dormant:
            could = 0 if ended else r.leaves_qty
        else:
            # unresolved, broken or dormant: everything not yet filled could still fill,
            # whatever LeavesQty says
            could = self._orders[k].qty - max(self._filled[k], r.cum_qty)
        return OrderState(
            reconciled=brk == 0,
            break_qty=brk,
            resolved=not unresolved,
            terminal=ended,
            dormant=dormant,
            could_fill=could,
            cum=max(self._filled[k], r.cum_qty),  # conservative exposure: the larger view
        )

    def reconcile_all(
        self,
        status: Mapping[str, StatusReply],
        venue_day_dfd_final: Mapping[str, bool] = VENUE_DAY_DFD_FINAL,
    ) -> dict[str, OrderState]:
        """Return the reconciled state of every order with a status reply, by ClOrdID."""
        return {k: self.reconcile(k, r, venue_day_dfd_final) for k, r in status.items()}

    def propose(self, state: Mapping[str, OrderState]) -> dict[str, int]:
        """Step 5: replacement quantities per intent, never from order state alone.

        An intent gets a proposal only when it is valid, every child order is reconciled,
        resolved and lifetime-terminal, and authorised quantity remains after what is filled
        and what could still fill.

        Args:
            state: Reconciled state of every child order, by ClOrdID.

        Returns:
            The remaining authorised quantity of each intent that may be resubmitted.
        """
        out = {}
        for p, it in self._intents.items():
            kids = [k for k in self._orders if self._orders[k].intent == p]
            settled = all(state[k].reconciled and state[k].resolved for k in kids)
            remaining = it.qty - sum(state[k].cum + state[k].could_fill for k in kids)
            if it.valid and settled and all(state[k].terminal for k in kids) and remaining > 0:
                out[p] = remaining
        return out


def check_duplicates(report: CheckReport, rec: Reconciler) -> None:
    """Fills are applied once by ExecID, and an unseen PossDup is applied."""
    print("== duplicates")
    report.ok("resent copy of f1 applied once", rec.filled["F1"] == 200)
    report.ok("unseen PossDup f2 applied (it may never have arrived)", rec.has_applied("f2"))


def check_fully_filled(
    report: CheckReport, state: Mapping[str, OrderState], proposals: Mapping[str, int]
) -> None:
    """A filled order is terminal and reconciled, but frees nothing to resubmit."""
    print("== fully filled order")
    report.ok("F1 is terminal and reconciled", state["F1"].terminal and state["F1"].reconciled)
    report.ok(
        "F1 is NOT a resubmission candidate (no remaining authorised quantity)",
        "P-full" not in proposals,
    )


def check_partial_then_cancelled(
    report: CheckReport, state: Mapping[str, OrderState], proposals: Mapping[str, int]
) -> None:
    """A cancelled partial fill frees the rest for a valid intent only."""
    print("== partially filled, then cancelled")
    report.ok("X1 reconciled at 120 of 300", state["X1"].reconciled and state["X1"].cum == 120)
    report.ok(
        "valid intent P-part: replacement proposed for exactly 180", proposals.get("P-part") == 180
    )
    report.ok(
        "withdrawn intent P-withdrawn: nothing proposed although 100 is unfilled",
        "P-withdrawn" not in proposals,
    )


def check_pending_cancel(
    report: CheckReport, state: Mapping[str, OrderState], proposals: Mapping[str, int]
) -> None:
    """An order in Pending Cancel is unresolved and blocks its intent."""
    print("== pending cancellation")
    report.ok("C1 in Pending Cancel is unresolved", not state["C1"].resolved)
    report.ok("P-pending: nothing proposed while C1 could still fill", "P-pending" not in proposals)


def check_missing_execution(
    report: CheckReport, state: Mapping[str, OrderState], proposals: Mapping[str, int]
) -> None:
    """A status CumQty above the fills applied is a break, with conservative exposure."""
    print("== missing execution")
    report.ok(
        "M1 break of 150 detected (status CumQty 250 against 100 applied)",
        state["M1"].break_qty == 150,
    )
    report.ok(
        "P-missing: nothing proposed until the break is resolved", "P-missing" not in proposals
    )
    report.ok("M1 exposure taken at the larger CumQty, 250", state["M1"].cum == 250)


def check_gtc_renewal(
    report: CheckReport,
    rec: Reconciler,
    state: Mapping[str, OrderState],
    proposals: Mapping[str, int],
) -> None:
    """A GTC order Done for Day stays live until a cancellation is confirmed.

    Applies the next day's fill to `rec`, so later checks see it.
    """
    print("== GTC order done for the day (overnight renewal)")
    report.ok(
        "G1 Done for Day is not lifetime-terminal (GTC)",
        not state["G1"].terminal and state["G1"].dormant,
    )
    report.ok(
        "G1 zero LeavesQty is not zero exposure: 8000 could still fill",
        state["G1"].could_fill == 8000,
    )
    report.ok("P-gtc: nothing proposed while G1 can be renewed", "P-gtc" not in proposals)
    old_view = (
        "P-gtc"
        if (
            STATUS["G1"].ord_status in OLD_TERMINAL
            and INTENTS["P-gtc"].qty - 2000 - STATUS["G1"].leaves_qty > 0
        )
        else None
    )
    report.ok(
        "the old TERMINAL set would have proposed 8000 more"
        " (18000 possible against 10000 authorised)",
        old_view == "P-gtc",
    )
    # next morning: Restated (ExecType D, ExecRestatementReason 1 = GT renewal), Partially
    # Filled, leaves 8000; then 1000 fills (a new execution, ExecID g2)
    status2 = {**STATUS, "G1": StatusReply("1", 3000, 7000, exec_type="D", restatement_reason=1)}
    rec.apply([Execution("G1", "g2", 1000)])
    state2 = rec.reconcile_all(status2)
    report.ok(
        "G1 renewed and partly filled next day: cum 3000, 7000 live",
        state2["G1"].cum == 3000 and state2["G1"].could_fill == 7000,
    )
    report.ok("P-gtc: still nothing proposed after renewal", "P-gtc" not in rec.propose(state2))
    # the strategy cancels: only a confirmed Canceled (OrdStatus 4) ends G1 and frees the
    # remaining 7000
    status3 = {**status2, "G1": StatusReply("4", 3000, 0)}
    state3 = rec.reconcile_all(status3)
    report.ok(
        "G1 confirmed Canceled: lifetime ended, 7000 proposable for the valid intent",
        rec.propose(state3).get("P-gtc") == 7000,
    )


def check_day_order(
    report: CheckReport,
    rec: Reconciler,
    state: Mapping[str, OrderState],
    proposals: Mapping[str, int],
) -> None:
    """A day order Done for Day ends only where the venue rule has been read."""
    print("== day order done for the day")
    report.ok(
        "D1 Done for Day with TimeInForce Day and venue rule read: lifetime ended",
        state["D1"].terminal,
    )
    report.ok("P-day: 200 proposed (500 - 300) for the valid intent", proposals.get("P-day") == 200)
    report.ok(
        "without the venue rule, D1 stays dormant and nothing is proposed",
        "P-day" not in rec.propose(rec.reconcile_all(STATUS, {"D1": False})),
    )


def main() -> int:
    """Run the checks with a fresh reconciler and report, and return the exit status (0 or 1)."""
    report = CheckReport()
    rec = Reconciler(INTENTS, ORDERS)
    rec.apply(STREAM)
    state = rec.reconcile_all(STATUS)
    proposals = rec.propose(state)
    check_duplicates(report, rec)
    check_fully_filled(report, state, proposals)
    check_partial_then_cancelled(report, state, proposals)
    check_pending_cancel(report, state, proposals)
    check_missing_execution(report, state, proposals)
    check_gtc_renewal(report, rec, state, proposals)
    check_day_order(report, rec, state, proposals)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed (offline synthetic illustration)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
