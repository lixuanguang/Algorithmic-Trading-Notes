"""derivatives and empirical validation (2026-10-17): settlement conventions behind mod:multi-curve-fra-swap-valuation.

End settlement (a swaplet): receive N tau (L - K) at T2. With F_j defined as the T2-forward-measure expectation of the
  index fixing L (the market FRA/swaplet rate read from index j's projection curve) and OIS discounting of a
  collateralised trade, its value is N tau (F_j - K) P_OIS(T2) exactly; that is what the entry's formula prices.
Start settlement (the conventional FRA): receive N tau (L - K) / (1 + tau L) at T1, the end amount discounted at the
  fixing itself (Hull, 11th Global ed., sec. 4.9, p. 111, footnote 4: the payment "would be made at time two years and
  equal to the present value of $125,000 discounted for three months at 3.5%"). Its value is
  N P_OIS(T1) E^{T1}[tau (L - K) / (1 + tau L)]. Substituting L = F_j gives N tau (F_j - K) P_OIS(T1) / (1 + tau F_j);
  that is exact when L is deterministic, and in the single-curve case, where 1/(1 + tau L) = P(T1, T2) and the payoff
  is replicated by bonds whatever L does. With a separate projection curve and stochastic L it omits a convexity term:
  the payoff is concave in L, and the T1-measure mean of L need not equal F_j.
Checks:
  1. The entry's invented two-curve example: start -20,777.37 against end -20,792.96 (the audit's figures).
  2. Single curve: start and end values coincide, and equal N (P(T1) - (1 + tau K) P(T2)).
  3. Separate curves: they differ, by N tau (F_j - K) [P_OIS(T1)/(1 + tau F_j) - P_OIS(T2)].
  4. Stochastic L with deterministic OIS rates (so all forward measures coincide and E[L] = F_j): the expected
     start-settled payoff lies below the deterministic substitution (Jensen), by an amount that grows with the
     volatility of L (expectation by quadrature over the normal density). Illustration only; lognormal L and the
     volatilities are invented.
Run: python3 fra-settlement-check.py  (standard library; exits 1 on failure).
"""
import math
import sys

fails = []


def ok(name, cond, detail=''):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


T1, T2, K, N = 1.0, 1.25, 0.034, 100e6
tau = T2 - T1


def values(Pois, Pref):
    F = (Pref(T1) / Pref(T2) - 1) / tau
    end = N * tau * (F - K) * Pois(T2)
    start = N * tau * (F - K) * Pois(T1) / (1 + tau * F)
    return F, start, end


print('== 1. the entry\'s invented curves (OIS 3.0%, term reference 3.3%, continuous)')
Pois = lambda t: math.exp(-0.030 * t)
Pref = lambda t: math.exp(-0.033 * t)
F, start, end = values(Pois, Pref)
print(f'     F_j = {F*100:.4f}%; start-settled {start:,.2f}; end-settled {end:,.2f}')
ok('start-settled -20,777.37', round(start, 2) == -20777.37)
ok('end-settled -20,792.96', round(end, 2) == -20792.96)

print('== 2. single curve: projection and discounting on the same curve')
for r in (0.01, 0.03, 0.08):
    P = lambda t, r=r: math.exp(-r * t)
    F1, s1, e1 = values(P, P)
    rep = N * (P(T1) - (1 + tau * K) * P(T2))
    ok(f'coincide at {r:.0%}', abs(s1 - e1) < 1e-6 and abs(s1 - rep) < 1e-6, f'start {s1:,.4f}, end {e1:,.4f}, bonds {rep:,.4f}')

print('== 3. separate curves: the conventions diverge')
for spread in (0.001, 0.003, 0.010):
    Pr = lambda t, s=spread: math.exp(-(0.030 + s) * t)
    F3, s3, e3 = values(Pois, Pr)
    gap = N * tau * (F3 - K) * (Pois(T1) / (1 + tau * F3) - Pois(T2))
    ok(f'differ with a {spread*1e4:.0f} bp basis', abs(s3 - e3) > 0.01 and abs((s3 - e3) - gap) < 1e-6,
       f'start - end = {s3 - e3:,.2f}')

print('== 4. stochastic L, deterministic OIS: deterministic substitution overstates the start-settled value')
Fm = F
det = N * Pois(T1) * tau * (Fm - K) / (1 + tau * Fm)
prev = 0.0
for vol in (0.2, 0.5, 1.0):
    m, lo, hi = 8001, -10.0, 10.0  # trapezoid rule over the standard normal density
    h = (hi - lo) / (m - 1)
    acc = 0.0
    for i in range(m):
        z = lo + i * h
        L = Fm * math.exp(vol * math.sqrt(T1) * z - 0.5 * vol * vol * T1)  # E[L] = F_j
        w = (0.5 if i in (0, m - 1) else 1.0) * h * math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
        acc += w * tau * (L - K) / (1 + tau * L)
    ex = N * Pois(T1) * acc
    ok(f'lognormal vol {vol:.0%}: exact expectation below substitution', ex < det and det - ex > prev,
       f'{ex:,.2f} vs substitution {det:,.2f} (gap {det - ex:,.2f})')
    prev = det - ex

if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
