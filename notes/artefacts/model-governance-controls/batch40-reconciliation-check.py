"""Batch of 17 October 2026: offline illustration of mech:order-state-reconciliation on synthetic FIX-like messages.

Not a test against any venue. Messages are dicts with FIX tag names. Steps, as arranged in the entry:
(1) apply execution reports once, keyed by ExecID(17); a resent copy (PossDupFlag(43)=Y) of an ExecID already applied is
    ignored, and an unseen PossDup message is applied (it may never have arrived);
(2) take the ExecType(150)=I status replies (to OrderStatusRequest 35=H / OrderMassStatusRequest 35=AF) as the
    recipient's view of OrdStatus(39), CumQty(14), LeavesQty(151);
(3) compare with the internal log; a status reply whose CumQty exceeds the fills applied reveals a missing execution;
(4) Pending Cancel (OrdStatus 6) is unresolved: the order is not treated as cancelled;
(5) only orders reconciled as terminal and matching are released for resubmission.
Run: python3 batch40-reconciliation-check.py   (standard library). Exits non-zero on failure.
"""
import sys

fails = []


def truth(name, cond):
    print(f"  {'ok ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


internal = {  # ClOrdID -> what our order log believes
    'A1': {'side': 1, 'qty': 300, 'status': 'sent'},
    'B1': {'side': 1, 'qty': 200, 'status': 'cancel_sent'},
    'C1': {'side': 2, 'qty': 100, 'status': 'sent'},
}
stream = [  # execution reports received around a disconnect
    {'ClOrdID': 'A1', 'ExecID': 'e1', 'ExecType': 'F', 'LastQty': 100, 'OrdStatus': '1'},
    {'ClOrdID': 'A1', 'ExecID': 'e1', 'ExecType': 'F', 'LastQty': 100, 'OrdStatus': '1', 'PossDupFlag': 'Y'},
    {'ClOrdID': 'B1', 'ExecID': 'e2', 'ExecType': '6', 'LastQty': 0, 'OrdStatus': '6'},   # Pending Cancel
    {'ClOrdID': 'B1', 'ExecID': 'e3', 'ExecType': 'F', 'LastQty': 200, 'OrdStatus': '2', 'PossDupFlag': 'Y'},
]
status_replies = [  # ExecType=I after OrderMassStatusRequest
    {'ClOrdID': 'A1', 'ExecType': 'I', 'OrdStatus': '1', 'CumQty': 200, 'LeavesQty': 100},
    {'ClOrdID': 'B1', 'ExecType': 'I', 'OrdStatus': '2', 'CumQty': 200, 'LeavesQty': 0},
    {'ClOrdID': 'C1', 'ExecType': 'I', 'OrdStatus': '6', 'CumQty': 0, 'LeavesQty': 100},
]

seen, filled = set(), {k: 0 for k in internal}
for m in stream:                                   # step (1)
    if m['ExecID'] in seen:
        continue
    seen.add(m['ExecID'])
    filled[m['ClOrdID']] += m['LastQty']
truth('PossDup copy of e1 ignored (A1 filled 100, not 200)', filled['A1'] == 100)
truth('unseen PossDup e3 applied (B1 filled 200)', filled['B1'] == 200)

breaks, release = {}, []
for r in status_replies:                           # steps (2)-(5)
    k = r['ClOrdID']
    if r['CumQty'] != filled[k]:
        breaks[k] = r['CumQty'] - filled[k]
    terminal = r['OrdStatus'] in ('2', '4', '8', 'C')
    if r['OrdStatus'] == '6':
        continue                                   # Pending Cancel: unresolved
    if terminal and k not in breaks:
        release.append(k)
truth('missing execution on A1 detected (status CumQty 200 vs 100 applied)', breaks == {'A1': 100})
truth('B1, believed cancelled internally, is reconciled as filled', 'B1' in release and filled['B1'] == 200)
truth('C1 in Pending Cancel is not released', 'C1' not in release)
truth('A1 with a break is not released', 'A1' not in release)
position = sum((1 if internal[k]['side'] == 1 else -1) * (filled[k] + breaks.get(k, 0)) for k in internal)
truth(f'position after reconciliation = +400 (A1 200 + B1 200 bought): {position}', position == 400)
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
