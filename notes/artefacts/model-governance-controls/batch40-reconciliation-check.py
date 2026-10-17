"""Offline, synthetic illustration of mech:order-state-reconciliation (batch of 17 October 2026; corrected the same day).

Not a test against any venue, broker or FIX engine, and not production logic: messages are dicts named after FIX
tags, the parent intents are invented, and no network or file is touched.

Correction. The first version released every order that was terminal and reconciled "for resubmission", so a
fully filled order (B1) became a resubmission candidate. Being reconciled says only that our record of an order
agrees with the recipient's; whether anything may be sent again depends on two further facts, kept separate here:
  * reconciled state per order: fills applied once by ExecID(17), compared with the ExecType(150)=I status reply
    (OrdStatus(39), CumQty(14), LeavesQty(151)); a reply whose CumQty exceeds the fills applied is a break (a
    missing execution), and Pending Cancel (OrdStatus 6) is unresolved;
  * remaining authorised quantity per parent intent: the intent's quantity less what is filled and less what could
    still fill (LeavesQty of live orders, and the full open quantity of unresolved orders and of orders with a break);
  * a valid intent: the parent instruction is still wanted (not cancelled by the strategy or a risk control).
A replacement order may be proposed only for an intent that is valid, has every child order reconciled and
resolved, and has remaining authorised quantity; its size is that remaining quantity.
Cases: a fully filled order; a partially filled order then cancelled (with a valid and with a withdrawn intent);
an order in Pending Cancel; a duplicate execution report (PossDupFlag(43)=Y) and an unseen PossDup; a missing
execution found from a status reply.
Second correction (third batch of 17 October 2026). OrdStatus(39)=3, Done for Day, was in TERMINAL. FIX Latest
(Orchestra, FIXTradingCommunity/orchestrations commit cd24169) describes it as "Order not, or partially, filled; no
further executions forthcoming for the trading day": complete for today, not ended. Expired (C) is the state of an
order "canceled in broker's system due to TimeInForce(59) instructions"; a GoodTillCancel order "remains in effect
until it is either executed or canceled"; and LeavesQty(151) "could be 0" under Done for Day. FIX 4.4 Appendix D
(read through OnixS's FIX dictionary mirror, not the FIX Trading Community's own copy) shows both cases: a day order
ends Done for Day with LeavesQty 0 (A.1.b, "Assuming day order"), while a GTC order reports Done for Day with LeavesQty
8000 and is restated next morning with ExecType D and ExecRestatementReason "GTC renewal/restatement" (H.1.a). So:
  * lifetime-terminal states are Filled (2), Canceled (4), Rejected (8) and Expired (C) only;
  * Done for Day ends the order's lifetime only for TimeInForce Day (0, or absent) and only where the venue's own
    rules say a day order receives no later Expired or Canceled; otherwise the order is dormant;
  * a dormant good-till order (GTC 1, GTD 6, or TimeInForce unknown) can fill next session for OrderQty - CumQty,
    whatever LeavesQty it reported, until a cancellation or expiry is confirmed.
The earlier cases (filled, partial-then-cancelled, Pending Cancel, duplicates, missing fill) are unchanged.
Run: python3 batch40-reconciliation-check.py   (standard library). Exits non-zero on failure.
"""
import sys

fails = []


def truth(name, cond):
    print(f"  {'ok ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


TERMINAL = {'2', '4', '8', 'C'}      # lifetime ends: Filled, Canceled, Rejected, Expired
DONE_FOR_DAY = '3'                    # complete for today only
UNRESOLVED = {'6', 'E', 'A'}          # Pending Cancel, Pending Replace, Pending New

intents = {  # parent instructions from the strategy: quantity authorised and whether still wanted
    'P-full': {'qty': 200, 'valid': True},
    'P-part': {'qty': 300, 'valid': True},
    'P-withdrawn': {'qty': 150, 'valid': False},
    'P-pending': {'qty': 100, 'valid': True},
    'P-missing': {'qty': 300, 'valid': True},
    'P-gtc': {'qty': 10000, 'valid': True},
    'P-day': {'qty': 500, 'valid': True},
}
orders = {  # ClOrdID -> parent intent and child quantity, as in our order log
    'F1': {'intent': 'P-full', 'qty': 200},
    'X1': {'intent': 'P-part', 'qty': 300},
    'W1': {'intent': 'P-withdrawn', 'qty': 150},
    'C1': {'intent': 'P-pending', 'qty': 100},
    'M1': {'intent': 'P-missing', 'qty': 300},
    'G1': {'intent': 'P-gtc', 'qty': 10000, 'tif': '1'},
    'D1': {'intent': 'P-day', 'qty': 500, 'tif': '0'},
}
VENUE_DAY_DFD_FINAL = {'D1': True}  # venue rule read for D1's venue: a Done for Day day order receives nothing later
stream = [  # execution reports received around a disconnect
    {'ClOrdID': 'F1', 'ExecID': 'f1', 'LastQty': 120},
    {'ClOrdID': 'F1', 'ExecID': 'f1', 'LastQty': 120, 'PossDupFlag': 'Y'},  # resent copy of f1
    {'ClOrdID': 'F1', 'ExecID': 'f2', 'LastQty': 80, 'PossDupFlag': 'Y'},   # unseen: may never have arrived
    {'ClOrdID': 'X1', 'ExecID': 'x1', 'LastQty': 120},
    {'ClOrdID': 'W1', 'ExecID': 'w1', 'LastQty': 50},
    {'ClOrdID': 'M1', 'ExecID': 'm1', 'LastQty': 100},
    {'ClOrdID': 'G1', 'ExecID': 'g1', 'LastQty': 2000},
    {'ClOrdID': 'D1', 'ExecID': 'd1', 'LastQty': 300},
]
status = {  # ExecType=I replies after OrderMassStatusRequest(35=AF)
    'F1': {'OrdStatus': '2', 'CumQty': 200, 'LeavesQty': 0},
    'X1': {'OrdStatus': '4', 'CumQty': 120, 'LeavesQty': 0},
    'W1': {'OrdStatus': '4', 'CumQty': 50, 'LeavesQty': 0},
    'C1': {'OrdStatus': '6', 'CumQty': 0, 'LeavesQty': 100},
    'M1': {'OrdStatus': '1', 'CumQty': 250, 'LeavesQty': 50},
    'G1': {'OrdStatus': '3', 'CumQty': 2000, 'LeavesQty': 0},   # Done for Day, zero leaves reported (allowed by FIX)
    'D1': {'OrdStatus': '3', 'CumQty': 300, 'LeavesQty': 0},
}

# step 1: apply each execution once, keyed by ExecID
seen, filled = set(), {k: 0 for k in orders}
for m in stream:
    if m['ExecID'] in seen:
        continue
    seen.add(m['ExecID'])
    filled[m['ClOrdID']] += m['LastQty']

# steps 2-4: reconciled state per order
def lifetime_ended(k, r):
    if r['OrdStatus'] in TERMINAL:
        return True
    if r['OrdStatus'] == DONE_FOR_DAY:
        tif = orders[k].get('tif')          # absent TimeInForce means Day under FIX, but unknown in our log is not absent
        return tif == '0' and VENUE_DAY_DFD_FINAL.get(k, False)
    return False


def reconcile(k, r):
    brk = r['CumQty'] - filled[k]
    unresolved = r['OrdStatus'] in UNRESOLVED
    dormant = r['OrdStatus'] == DONE_FOR_DAY and not lifetime_ended(k, r)
    if brk == 0 and not unresolved and not dormant:
        could = 0 if lifetime_ended(k, r) else r['LeavesQty']
    else:  # unresolved, broken or dormant: everything not yet filled could still fill, whatever LeavesQty says
        could = orders[k]['qty'] - max(filled[k], r['CumQty'])
    return {
        'reconciled': brk == 0,
        'break': brk,
        'resolved': not unresolved,
        'terminal': lifetime_ended(k, r),
        'dormant': dormant,
        'could_fill': could,
        'cum': max(filled[k], r['CumQty']),  # conservative exposure: the larger of the two views
    }


state = {k: reconcile(k, r) for k, r in status.items()}

# step 5: proposals per intent, from remaining authorised quantity and validity, never from order state alone
def propose(state):
    out = {}
    for p, it in intents.items():
        kids = [k for k in orders if orders[k]['intent'] == p]
        settled = all(state[k]['reconciled'] and state[k]['resolved'] for k in kids)
        remaining = it['qty'] - sum(state[k]['cum'] + state[k]['could_fill'] for k in kids)
        if it['valid'] and settled and all(state[k]['terminal'] for k in kids) and remaining > 0:
            out[p] = remaining
    return out


proposals = propose(state)

print('== duplicates')
truth('resent copy of f1 applied once', filled['F1'] == 200)
truth('unseen PossDup f2 applied (it may never have arrived)', 'f2' in seen)
print('== fully filled order')
truth('F1 is terminal and reconciled', state['F1']['terminal'] and state['F1']['reconciled'])
truth('F1 is NOT a resubmission candidate (no remaining authorised quantity)', 'P-full' not in proposals)
print('== partially filled, then cancelled')
truth('X1 reconciled at 120 of 300', state['X1']['reconciled'] and state['X1']['cum'] == 120)
truth('valid intent P-part: replacement proposed for exactly 180', proposals.get('P-part') == 180)
truth('withdrawn intent P-withdrawn: nothing proposed although 100 is unfilled', 'P-withdrawn' not in proposals)
print('== pending cancellation')
truth('C1 in Pending Cancel is unresolved', not state['C1']['resolved'])
truth('P-pending: nothing proposed while C1 could still fill', 'P-pending' not in proposals)
print('== missing execution')
truth('M1 break of 150 detected (status CumQty 250 against 100 applied)', state['M1']['break'] == 150)
truth('P-missing: nothing proposed until the break is resolved', 'P-missing' not in proposals)
truth('M1 exposure taken at the larger CumQty, 250', state['M1']['cum'] == 250)
print('== GTC order done for the day (overnight renewal)')
truth('G1 Done for Day is not lifetime-terminal (GTC)', not state['G1']['terminal'] and state['G1']['dormant'])
truth('G1 zero LeavesQty is not zero exposure: 8000 could still fill', state['G1']['could_fill'] == 8000)
truth('P-gtc: nothing proposed while G1 can be renewed', 'P-gtc' not in proposals)
old_terminal = {'2', '3', '4', '8', 'C'}
old_view = 'P-gtc' if (status['G1']['OrdStatus'] in old_terminal and intents['P-gtc']['qty'] - 2000 - status['G1']['LeavesQty'] > 0) else None
truth('the old TERMINAL set would have proposed 8000 more (18000 possible against 10000 authorised)', old_view == 'P-gtc')
# next morning: Restated (ExecType D, ExecRestatementReason 1 = GT renewal), Partially Filled, leaves 8000; then 1000 fills
status2 = dict(status, G1={'OrdStatus': '1', 'CumQty': 3000, 'LeavesQty': 7000, 'ExecType': 'D', 'ExecRestatementReason': 1})
filled['G1'] += 1000
state2 = {k: reconcile(k, r) for k, r in status2.items()}
truth('G1 renewed and partly filled next day: cum 3000, 7000 live', state2['G1']['cum'] == 3000 and state2['G1']['could_fill'] == 7000)
truth('P-gtc: still nothing proposed after renewal', 'P-gtc' not in propose(state2))
# the strategy cancels: only a confirmed Canceled (OrdStatus 4) ends G1 and frees the remaining 7000
status3 = dict(status2, G1={'OrdStatus': '4', 'CumQty': 3000, 'LeavesQty': 0})
state3 = {k: reconcile(k, r) for k, r in status3.items()}
truth('G1 confirmed Canceled: lifetime ended, 7000 proposable for the valid intent', propose(state3).get('P-gtc') == 7000)
print('== day order done for the day')
truth('D1 Done for Day with TimeInForce Day and venue rule read: lifetime ended', state['D1']['terminal'])
truth('P-day: 200 proposed (500 - 300) for the valid intent', proposals.get('P-day') == 200)
VENUE_DAY_DFD_FINAL['D1'] = False
truth('without the venue rule, D1 stays dormant and nothing is proposed', 'P-day' not in propose({k: reconcile(k, r) for k, r in status.items()}))
VENUE_DAY_DFD_FINAL['D1'] = True
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed (offline synthetic illustration)')
