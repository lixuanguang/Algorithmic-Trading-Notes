"""Order-state reconciliation on records named after FIX tags: fills, replies, resubmission."""

from collections.abc import Iterable, Mapping
from typing import Final

from trading_notes.records import Record

# OrdStatus(39) values whose order lifetime has ended: Filled, Canceled, Rejected, Expired.
TERMINAL: Final = frozenset({"2", "4", "8", "C"})
DONE_FOR_DAY: Final = "3"  # complete for today only
UNRESOLVED: Final = frozenset({"6", "E", "A"})  # Pending Cancel, Pending Replace, Pending New
DAY: Final = "0"  # TimeInForce(59) Day


class Intent(Record):
    """A parent instruction from the strategy.

    Attributes:
        qty: Quantity authorised.
        valid: Whether it is still wanted (not cancelled by the strategy or a risk control).
    """

    qty: int
    valid: bool


class Order(Record):
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


class Execution(Record):
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


class StatusReply(Record):
    """The recipient's view of one order.

    Attributes:
        ord_status: OrdStatus(39).
        cum_qty: CumQty(14), the quantity filled so far.
        leaves_qty: LeavesQty(151), the quantity still working as reported; it may be 0 under
            Done for Day even for an order that can fill later.
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


class OrderState(Record):
    """The reconciled state of one order.

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


class Reconciler:
    """Fills applied once by ExecID, and the reconciled state and proposals they imply.

    Being reconciled says only that our record of an order agrees with the recipient's;
    whether anything may be sent again also depends on the remaining authorised quantity of
    the parent intent and on the intent still being wanted. Each instance owns the ExecIDs it
    has applied and the fills per order; the intents, orders and venue rules it reads are
    never changed.
    """

    def __init__(
        self,
        intents: Mapping[str, Intent],
        orders: Mapping[str, Order],
        venue_day_dfd_final: Mapping[str, bool],
    ) -> None:
        """Start with no executions applied.

        Args:
            intents: Parent intents by key.
            orders: Child orders by ClOrdID; each names one of `intents`.
            venue_day_dfd_final: Per ClOrdID, whether its venue's rules say a Done for Day day
                order receives no later Expired or Canceled; missing means not read.
        """
        self._intents = intents
        self._orders = orders
        self._venue_day_dfd_final = venue_day_dfd_final
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
        """Apply each execution once, keyed by ExecID, whatever its PossDupFlag."""
        for m in stream:
            if m.exec_id in self._seen:
                continue
            self._seen.add(m.exec_id)
            self._filled[m.cl_ord_id] += m.last_qty

    def lifetime_ended(
        self, k: str, r: StatusReply, venue_day_dfd_final: Mapping[str, bool]
    ) -> bool:
        """Return whether order k's lifetime has ended, given its status reply.

        Only Filled, Canceled, Rejected and Expired end a lifetime. Done for Day ends it only
        for a TimeInForce Day order on a venue whose rules say such an order receives nothing
        later; otherwise the order is dormant and, if good till cancel or date, can fill next
        session for OrderQty - CumQty until a cancellation or expiry is confirmed.

        Args:
            k: ClOrdID.
            r: Its status reply.
            venue_day_dfd_final: The venue rules read, as for the constructor.
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
        """Compare order k's applied fills with its status reply.

        Args:
            k: ClOrdID.
            r: Its status reply.
            venue_day_dfd_final: The venue rules read, as for the constructor.
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
        venue_day_dfd_final: Mapping[str, bool] | None = None,
    ) -> dict[str, OrderState]:
        """Return the reconciled state of every order with a status reply, by ClOrdID.

        Args:
            status: Status replies by ClOrdID.
            venue_day_dfd_final: Venue rules to use instead of the constructor's.
        """
        venue = self._venue_day_dfd_final if venue_day_dfd_final is None else venue_day_dfd_final
        return {k: self.reconcile(k, r, venue) for k, r in status.items()}

    def propose(self, state: Mapping[str, OrderState]) -> dict[str, int]:
        """Return replacement quantities per intent, never from order state alone.

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
