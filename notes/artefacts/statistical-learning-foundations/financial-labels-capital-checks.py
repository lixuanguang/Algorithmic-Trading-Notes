"""financial data and labels review follow-up checks (2026-10-16): ETF-trick timing and capital, label spans and the returns they use.

Independent of the entries' formulas where possible: holdings and spans are recomputed by brute force.
Run: python3 financial-labels-capital-checks.py   (numpy only)
"""
import numpy as np


def head(t):
    print('\n== ' + t)


# ------------------------------------------------------------------ ETF trick: sizing at the next open
head('ETF trick: holdings h = w K / (o_{t+1} phi sum|w|) need the next open, unknown at decision time t')
K, w, phi = 1.0, np.array([0.6, -0.4]), np.array([1.0, 1.0])
o_next = np.array([[100.0, 50.0], [101.5, 49.2]])           # two possible opening prints
for o in o_next:
    h = w * K / (o * phi * np.abs(w).sum())
    print('open', o, '-> holdings', h.round(6), ' gross exposure at that open', round(float((np.abs(h) * o * phi).sum()), 6))
print('same causal weights, different opens -> different quantities: the quantity is not fixed at t')
# a notional-sized order filled at the single opening price reproduces the convention exactly
notional = w * K / np.abs(w).sum()                          # currency amounts per leg, fixed at t
o = o_next[1]
print('notional per leg fixed at t', notional, '-> quantity at the opening print', (notional / (o * phi)).round(6),
      '(equals the convention when every leg fills in full at o_{t+1})')
# an order sized at t on the last close leaves a residual exposure when the open gaps
p_close = np.array([100.0, 50.0])
h_close = w * K / (p_close * phi * np.abs(w).sum())
print('quantities sized on p_t, valued at o_{t+1}: gross', round(float((np.abs(h_close) * o * phi).sum()), 6), 'not 1')

head('ETF trick: gross exposure = |K| only with positive o*phi; K <= 0 inverts or zeroes the holdings')
for Kt in [1.0, 0.3, 0.0, -0.2]:
    h = w * Kt / (o * phi * np.abs(w).sum())
    print(f'K={Kt:5}: holdings {h.round(6)}  gross {float((np.abs(h) * o * phi).sum()):.4f}  sign of long leg {np.sign(h[0]):+.0f}')
o_neg = np.array([-5.0, 50.0])                               # a negative price (e.g. a rolled or spread series)
h = w * 1.0 / (o_neg * phi * np.abs(w).sum())
print('negative open on leg 1 (w_1 = +0.6): holding', h.round(6), '-> a short position although w_1 > 0;',
      'sum |h| o phi =', round(float((np.abs(h) * o_neg * phi).sum()), 4), 'is no longer the gross exposure')


# ------------------------------------------------------------------ label spans and the returns they use
head('label spans: returns r_{t-1,t} indexed by ending time t; label on (t0, t1] uses t0 < t <= t1')
labels = [(0, 3), (2, 4), (4, 6)]                            # AFML sec. 4.5.3: y1=f(r_{0,3}), y2=f(r_{2,4}), y3=f(r_{4,6})
T = 6


def ind_matrix(spans, rows, rule):
    m = np.zeros((len(rows), len(spans)))
    for j, (a, b) in enumerate(spans):
        for i, t in enumerate(rows):
            m[i, j] = rule(a, b, t)
    return m


def avg_u(m):
    c = m.sum(1)
    u = np.divide(m, c[:, None], out=np.zeros_like(m), where=c[:, None] > 0)
    return c, u.sum(0) / m.sum(0)


# brute force: which one-bar returns does each label's return compound?
for j, (a, b) in enumerate(labels):
    used = [t for t in range(1, T + 1) if a < t <= b]
    print(f'label {j + 1} on r_({a},{b}) compounds r_(t-1,t) for t in {used}')
ending = ind_matrix(labels, range(1, T + 1), lambda a, b, t: float(a < t <= b))
c, u = avg_u(ending)
print('ending-time rule, rows t=1..6:\n', ending.astype(int), '\nconcurrency', c, 'average uniqueness', u.round(4))
start = ind_matrix([(a, b - 1) for a, b in labels], range(0, T), lambda a, b, s: float(a <= s <= b))
print('consistent reindexing by start time s (r_{s,s+1}, t0 <= s < t1; AFML Snippet 4.6 codes t1 = {0:2, 2:3, 4:5}): identical matrix:',
      bool((start == ending).all()))
incl = ind_matrix(labels, range(0, T + 1), lambda a, b, t: float(a <= t <= b))
c2, u2 = avg_u(incl)
print('inclusive [t0, t1] on ending-time rows t=0..6 (getIndMatrix applied to the events themselves):\n', incl.astype(int),
      '\nconcurrency', c2, 'average uniqueness', u2.round(4))
print('labels 2 and 3 are adjacent (one ends at 4, the other starts at 4) yet share row t=4, the return r_{3,4} that label 3 never uses')

# attribution weights on a toy log-price path: the inclusive rule adds a return from before the label starts
logp = np.log(np.array([100, 101, 103, 102, 104, 103, 106.0]))
r = np.diff(logp)                                          # r[t-1] = r_{t-1,t}, t = 1..6
w_end = [abs(sum(r[t - 1] / c[t - 1] for t in range(a + 1, b + 1))) for a, b in labels]
w_inc = [abs(sum((r[t - 1] if t >= 1 else 0.0) / c2[t] for t in range(a, b + 1))) for a, b in labels]
print('attribution |sum r/c|: ending-time rule', np.round(w_end, 5), ' inclusive rule', np.round(w_inc, 5))
