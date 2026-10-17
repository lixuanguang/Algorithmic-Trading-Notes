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
Run: python3 batch40-reconciliation-check.py   (standard library). Exits non-zero on failure.
"""
import sys

fails = []


def truth(name, cond):
    print(f"  {'ok ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


TERMINAL = {'2', '3', '4', '8', 'C'}  # Filled, Done for Day, Canceled, Rejected, Expired
UNRESOLVED = {'6', 'E', 'A'}          # Pending Cancel, Pending Replace, Pending New

intents = {  # parent instructions from the strategy: quantity authorised and whether still wanted
    'P-full': {'qty': 200, 'valid': True},
    'P-part': {'qty': 300, 'valid': True},
    'P-withdrawn': {'qty': 150, 'valid': False},
    'P-pending': {'qty': 100, 'valid': True},
    'P-missing': {'qty': 300, 'valid': True},
}
orders = {  # ClOrdID -> parent intent and child quantity, as in our order log
    'F1': {'intent': 'P-full', 'qty': 200},
    'X1': {'intent': 'P-part', 'qty': 300},
    'W1': {'intent': 'P-withdrawn', 'qty': 150},
    'C1': {'intent': 'P-pending', 'qty': 100},
    'M1': {'intent': 'P-missing', 'qty': 300},
}
stream = [  # execution reports received around a disconnect
    {'ClOrdID': 'F1', 'ExecID': 'f1', 'LastQty': 120},
    {'ClOrdID': 'F1', 'ExecID': 'f1', 'LastQty': 120, 'PossDupFlag': 'Y'},  # resent copy of f1
    {'ClOrdID': 'F1', 'ExecID': 'f2', 'LastQty': 80, 'PossDupFlag': 'Y'},   # unseen: may never have arrived
    {'ClOrdID': 'X1', 'ExecID': 'x1', 'LastQty': 120},
    {'ClOrdID': 'W1', 'ExecID': 'w1', 'LastQty': 50},
    {'ClOrdID': 'M1', 'ExecID': 'm1', 'LastQty': 100},
]
status = {  # ExecType=I replies after OrderMassStatusRequest(35=AF)
    'F1': {'OrdStatus': '2', 'CumQty': 200, 'LeavesQty': 0},
    'X1': {'OrdStatus': '4', 'CumQty': 120, 'LeavesQty': 0},
    'W1': {'OrdStatus': '4', 'CumQty': 50, 'LeavesQty': 0},
    'C1': {'OrdStatus': '6', 'CumQty': 0, 'LeavesQty': 100},
    'M1': {'OrdStatus': '1', 'CumQty': 250, 'LeavesQty': 50},
}

# step 1: apply each execution once, keyed by ExecID
seen, filled = set(), {k: 0 for k in orders}
for m in stream:
    if m['ExecID'] in seen:
        continue
    seen.add(m['ExecID'])
    filled[m['ClOrdID']] += m['LastQty']

# steps 2-4: reconciled state per order
state = {}
for k, r in status.items():
    brk = r['CumQty'] - filled[k]
    state[k] = {
        'reconciled': brk == 0,
        'break': brk,
        'resolved': r['OrdStatus'] not in UNRESOLVED,
        'terminal': r['OrdStatus'] in TERMINAL,
        # what could still execute: live leaves, or everything open if the state is unresolved or broken
        'could_fill': r['LeavesQty'] if (brk == 0 and r['OrdStatus'] not in UNRESOLVED) else orders[k]['qty'] - min(filled[k], r['CumQty']),
        'cum': max(filled[k], r['CumQty']),  # conservative exposure: the larger of the two views
    }

# step 5: proposals per intent, from remaining authorised quantity and validity, never from order state alone
proposals = {}
for p, it in intents.items():
    kids = [k for k in orders if orders[k]['intent'] == p]
    settled = all(state[k]['reconciled'] and state[k]['resolved'] for k in kids)
    remaining = it['qty'] - sum(state[k]['cum'] + state[k]['could_fill'] for k in kids)
    if it['valid'] and settled and all(state[k]['terminal'] for k in kids) and remaining > 0:
        proposals[p] = remaining

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
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed (offline synthetic illustration)')
