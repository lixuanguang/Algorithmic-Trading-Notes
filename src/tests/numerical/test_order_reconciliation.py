"""Tests of the order reconciliation example's records and state-owning reconciler.

The example's own checks run in test_checks.py; these vary its synthetic inputs to pin down
the rules the checks rely on: ExecID deduplication, conservative state, intent validity and the
Done for Day distinctions.

Run: make test (uv run --frozen --no-editable pytest)
"""

import unittest
from collections.abc import Mapping
from dataclasses import FrozenInstanceError
from types import MappingProxyType

from trading_notes.numerical import order_reconciliation as rec
from trading_notes.numerical.order_reconciliation import (
    INTENTS,
    ORDERS,
    STATUS,
    STREAM,
    Execution,
    Intent,
    Order,
    OrderState,
    Reconciler,
    StatusReply,
)


def day_one(
    intents: Mapping[str, Intent] = INTENTS, orders: Mapping[str, Order] = ORDERS
) -> Reconciler:
    """Return a new reconciler with the example's execution stream applied."""
    reconciler = Reconciler(intents, orders)
    reconciler.apply(STREAM)
    return reconciler


class Deduplication(unittest.TestCase):
    """Fills are applied once per ExecID; PossDupFlag alone decides nothing."""

    def test_resent_exec_id_is_applied_once(self) -> None:
        """Copies of one ExecID count once, flagged or not."""
        reconciler = Reconciler(INTENTS, ORDERS)
        f1 = Execution("F1", "f1", 120)
        reconciler.apply([f1, Execution("F1", "f1", 120, poss_dup=True), f1])
        self.assertEqual(reconciler.filled["F1"], 120)

    def test_unseen_possdup_is_applied(self) -> None:
        """A PossDup whose ExecID was never seen is a fill that may never have arrived."""
        reconciler = Reconciler(INTENTS, ORDERS)
        self.assertFalse(reconciler.has_applied("f2"))
        reconciler.apply([Execution("F1", "f2", 80, poss_dup=True)])
        self.assertTrue(reconciler.has_applied("f2"))
        self.assertEqual(reconciler.filled["F1"], 80)


class ConservativeState(unittest.TestCase):
    """A disagreement is a break, and exposure takes the larger view."""

    def test_missing_fill_is_a_break(self) -> None:
        """Status CumQty 250 against 100 applied: break 150, exposure 250, the rest could fill."""
        self.assertEqual(
            day_one().reconcile_all(STATUS)["M1"],
            OrderState(
                reconciled=False,
                break_qty=150,
                resolved=True,
                terminal=False,
                dormant=False,
                could_fill=50,
                cum=250,
            ),
        )

    def test_fills_beyond_the_reply_also_break(self) -> None:
        """More applied than the reply reports: exposure takes the fills, nothing is proposed."""
        reconciler = day_one()
        state = reconciler.reconcile_all({**STATUS, "X1": StatusReply("4", 100, 0)})
        self.assertEqual((state["X1"].break_qty, state["X1"].cum), (-20, 120))
        self.assertEqual(state["X1"].could_fill, 180)
        self.assertNotIn("P-part", reconciler.propose(state))


class Proposals(unittest.TestCase):
    """Replacements come from intent validity and remaining authorised quantity."""

    def test_withdrawn_intent_gets_nothing(self) -> None:
        """The same unfilled 100 is proposed only while the intent is valid."""
        withdrawn = day_one()
        self.assertNotIn("P-withdrawn", withdrawn.propose(withdrawn.reconcile_all(STATUS)))
        valid = day_one({**INTENTS, "P-withdrawn": Intent(150, True)})
        self.assertEqual(valid.propose(valid.reconcile_all(STATUS))["P-withdrawn"], 100)

    def test_pending_cancel_blocks_until_confirmed(self) -> None:
        """Pending Cancel leaves the open 100 able to fill; a confirmed Canceled frees it."""
        reconciler = day_one()
        pending = reconciler.reconcile_all(STATUS)
        self.assertFalse(pending["C1"].resolved)
        self.assertEqual(pending["C1"].could_fill, 100)
        self.assertNotIn("P-pending", reconciler.propose(pending))
        cancelled = reconciler.reconcile_all({**STATUS, "C1": StatusReply("4", 0, 0)})
        self.assertEqual(reconciler.propose(cancelled)["P-pending"], 100)


class DoneForDay(unittest.TestCase):
    """Done for Day ends a lifetime only for a known day order on a venue whose rule is read."""

    def test_gtc_order_is_dormant_with_its_open_quantity(self) -> None:
        """Zero LeavesQty under Done for Day still leaves OrderQty - CumQty able to fill."""
        g1 = day_one().reconcile_all(STATUS)["G1"]
        self.assertEqual((g1.terminal, g1.dormant, g1.could_fill), (False, True, 8000))

    def test_unknown_or_good_till_time_in_force_is_not_day(self) -> None:
        """Unknown TimeInForce, or GTD, keeps D1 dormant even with the venue rule read."""
        for tif in (None, "6"):
            with self.subTest(tif=tif):
                reconciler = day_one(orders={**ORDERS, "D1": Order("P-day", 500, tif=tif)})
                state = reconciler.reconcile_all(STATUS)
                self.assertEqual((state["D1"].terminal, state["D1"].dormant), (False, True))
                self.assertEqual(state["D1"].could_fill, 200)
                self.assertNotIn("P-day", reconciler.propose(state))

    def test_day_order_needs_the_venue_rule(self) -> None:
        """A Day order is lifetime-terminal under Done for Day only where the rule says so."""
        reconciler = day_one()
        self.assertTrue(reconciler.reconcile_all(STATUS)["D1"].terminal)
        unread = reconciler.reconcile_all(STATUS, {})["D1"]
        self.assertEqual((unread.terminal, unread.dormant), (False, True))

    def test_renewal_then_confirmed_cancellation_or_expiry(self) -> None:
        """A renewed GTC order stays live; Canceled or Expired ends it and frees the rest."""
        reconciler = day_one()
        reconciler.apply([Execution("G1", "g2", 1000)])
        renewed = reconciler.reconcile_all(
            {**STATUS, "G1": StatusReply("1", 3000, 7000, exec_type="D", restatement_reason=1)}
        )
        self.assertEqual((renewed["G1"].cum, renewed["G1"].could_fill), (3000, 7000))
        self.assertNotIn("P-gtc", reconciler.propose(renewed))
        for ended in ("4", "C"):
            with self.subTest(ord_status=ended):
                state = reconciler.reconcile_all({**STATUS, "G1": StatusReply(ended, 3000, 0)})
                self.assertEqual(reconciler.propose(state)["P-gtc"], 7000)


class StateOwnership(unittest.TestCase):
    """Each reconciler owns its fills; the example's inputs cannot be changed."""

    def test_reconcilers_do_not_share_fills(self) -> None:
        """Applying to one reconciler changes neither another nor a returned copy."""
        first, second = day_one(), day_one()
        filled = first.filled
        first.apply([Execution("G1", "g2", 1000)])
        self.assertEqual(
            (first.filled["G1"], second.filled["G1"], filled["G1"]), (3000, 2000, 2000)
        )
        self.assertFalse(second.has_applied("g2"))

    def test_example_inputs_are_read_only(self) -> None:
        """The inputs are read-only views of frozen records, so no run changes the next one's."""
        for mapping in (rec.INTENTS, rec.ORDERS, rec.STATUS, rec.VENUE_DAY_DFD_FINAL):
            self.assertIsInstance(mapping, MappingProxyType)
        self.assertIsInstance(rec.STREAM, tuple)
        with self.assertRaises(FrozenInstanceError):
            setattr(rec.INTENTS["P-gtc"], "qty", 1)  # a write the type checker would reject


if __name__ == "__main__":
    unittest.main()
