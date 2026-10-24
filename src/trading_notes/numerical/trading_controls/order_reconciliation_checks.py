"""Checks of order-state reconciliation around a disconnect, on synthetic FIX messages."""

import sys
from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.trading_controls.order_state import (
    DAY,
    Execution,
    Intent,
    Order,
    OrderState,
    Reconciler,
    StatusReply,
)

# The naive terminal set with Done for Day (3) in it: the counterexample of the GTC check.
NAIVE_TERMINAL: Final = frozenset({"2", "3", "4", "8", "C"})
INTENTS: Final[Mapping[str, Intent]] = MappingProxyType(
    {  # parent instructions from the strategy: quantity authorised and whether still wanted
        "P-full": Intent(qty=200, valid=True),
        "P-part": Intent(qty=300, valid=True),
        "P-withdrawn": Intent(qty=150, valid=False),
        "P-pending": Intent(qty=100, valid=True),
        "P-missing": Intent(qty=300, valid=True),
        "P-gtc": Intent(qty=10000, valid=True),
        "P-day": Intent(qty=500, valid=True),
    }
)
ORDERS: Final[Mapping[str, Order]] = MappingProxyType(
    {  # ClOrdID -> parent intent and child quantity, as in our order log
        "F1": Order(intent="P-full", qty=200),
        "X1": Order(intent="P-part", qty=300),
        "W1": Order(intent="P-withdrawn", qty=150),
        "C1": Order(intent="P-pending", qty=100),
        "M1": Order(intent="P-missing", qty=300),
        "G1": Order(intent="P-gtc", qty=10000, tif="1"),
        "D1": Order(intent="P-day", qty=500, tif=DAY),
    }
)
# Venue rule read for D1's venue: a Done for Day day order receives nothing later.
VENUE_DAY_DFD_FINAL: Final[Mapping[str, bool]] = MappingProxyType({"D1": True})
STREAM: Final = (  # execution reports received around a disconnect
    Execution(cl_ord_id="F1", exec_id="f1", last_qty=120),
    Execution(cl_ord_id="F1", exec_id="f1", last_qty=120, poss_dup=True),  # resent copy of f1
    Execution(
        cl_ord_id="F1", exec_id="f2", last_qty=80, poss_dup=True
    ),  # unseen: may never have arrived
    Execution(cl_ord_id="X1", exec_id="x1", last_qty=120),
    Execution(cl_ord_id="W1", exec_id="w1", last_qty=50),
    Execution(cl_ord_id="M1", exec_id="m1", last_qty=100),
    Execution(cl_ord_id="G1", exec_id="g1", last_qty=2000),
    Execution(cl_ord_id="D1", exec_id="d1", last_qty=300),
)
STATUS: Final[Mapping[str, StatusReply]] = MappingProxyType(
    {  # ExecType=I replies after OrderMassStatusRequest(35=AF)
        "F1": StatusReply(ord_status="2", cum_qty=200, leaves_qty=0),
        "X1": StatusReply(ord_status="4", cum_qty=120, leaves_qty=0),
        "W1": StatusReply(ord_status="4", cum_qty=50, leaves_qty=0),
        "C1": StatusReply(ord_status="6", cum_qty=0, leaves_qty=100),
        "M1": StatusReply(ord_status="1", cum_qty=250, leaves_qty=50),
        "G1": StatusReply(
            ord_status="3", cum_qty=2000, leaves_qty=0
        ),  # Done for Day, zero leaves reported (allowed by FIX)
        "D1": StatusReply(ord_status="3", cum_qty=300, leaves_qty=0),
    }
)


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
            STATUS["G1"].ord_status in NAIVE_TERMINAL
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
    status2 = {
        **STATUS,
        "G1": StatusReply(
            ord_status="1", cum_qty=3000, leaves_qty=7000, exec_type="D", restatement_reason=1
        ),
    }
    rec.apply([Execution(cl_ord_id="G1", exec_id="g2", last_qty=1000)])
    state2 = rec.reconcile_all(status2)
    report.ok(
        "G1 renewed and partly filled next day: cum 3000, 7000 live",
        state2["G1"].cum == 3000 and state2["G1"].could_fill == 7000,
    )
    report.ok("P-gtc: still nothing proposed after renewal", "P-gtc" not in rec.propose(state2))
    # the strategy cancels: only a confirmed Canceled (OrdStatus 4) ends G1 and frees the
    # remaining 7000
    status3 = {**status2, "G1": StatusReply(ord_status="4", cum_qty=3000, leaves_qty=0)}
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
    """Run the checks with a fresh reconciler and report, and return the exit status (0 or 1).

    Offline, synthetic illustration of mech:order-state-reconciliation: not a test against any
    venue, broker or FIX engine. The parent intents are invented and no network or file is
    touched. Cases: a fully filled order; a partially filled order then cancelled, with a valid
    and with a withdrawn intent; an order in Pending Cancel; a duplicate execution report
    (PossDupFlag(43)=Y) and an unseen PossDup; a missing execution found from a status reply;
    a GTC order Done for Day and renewed next morning (FIX 4.4 Appendix D, H.1.a); and a day
    order Done for Day (A.1.b). FIX field meanings follow FIX Latest (Orchestra).
    """
    report = CheckReport()
    rec = Reconciler(INTENTS, ORDERS, VENUE_DAY_DFD_FINAL)
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
