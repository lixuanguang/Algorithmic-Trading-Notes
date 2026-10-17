"""Third batch of 17 October 2026 (audit repair): expected shortfall for discrete and historical-simulation
distributions, behind meth:var-es-estimation-methods.

Definition used (Acerbi and Tasche, "On the coherence of Expected Shortfall", arXiv:cond-mat/0104295v3, Definition
2.6 p. 5, Proposition 3.2 p. 6 and eq. (3.3) p. 7, written there for a profit X and a tail level alpha in (0,1)),
restated here for a loss L = -X, confidence level c and exceedance (tail) probability alpha = 1 - c:
    VaR_c(L) = inf{l : P(L <= l) >= c}                                   (lower quantile of the loss)
    ES_c(L)  = (1/alpha) * integral_c^1 VaR_u(L) du
             = (1/alpha) * ( E[L 1{L > VaR_c}] + VaR_c * (P(L <= VaR_c) - c) )   (fractional tail mass)
The second line is the loss-side form of Definition 2.6's tail mean; it puts weight on the atom at VaR so that the
tail always carries probability exactly alpha. E[L | L > VaR] and E[L | L >= VaR] (the two tail conditional
expectations) differ from ES when L has an atom at VaR.
Checked: the audit's example; equality of the integral and fractional-mass forms; historical simulation with an
integer and a fractional number of tail observations; and agreement with a continuous distribution, where all
three coincide. Run: python3 batch60-es-discrete-check.py  (standard library). Exits non-zero on failure.
"""
import math
import random
import sys

fails = []


def close(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.6g} (want {want:.6g})")
    if not ok:
        fails.append(name)


def var_discrete(atoms, c):
    """atoms: list of (loss, prob). Lower c-quantile of the loss."""
    cum = 0.0
    for x, p in sorted(atoms):
        cum += p
        if cum >= c - 1e-15:
            return x
    return max(x for x, _ in atoms)


def es_fractional(atoms, c):
    a = 1 - c
    v = var_discrete(atoms, c)
    above = sum(x * p for x, p in atoms if x > v)
    at_or_below = sum(p for x, p in atoms if x <= v)
    return (above + v * (at_or_below - c)) / a


def es_integral(atoms, c, n=200000):
    a = 1 - c
    h = a / n
    return sum(var_discrete(atoms, c + (i + 0.5) * h) for i in range(n)) * h / a


def tce(atoms, c, strict=True):
    v = var_discrete(atoms, c)
    sel = [(x, p) for x, p in atoms if (x > v if strict else x >= v)]
    return sum(x * p for x, p in sel) / sum(p for _, p in sel)


def es_hs(sample, c):
    """Historical simulation: average of the worst n*alpha losses, the last one fractionally weighted."""
    xs = sorted(sample, reverse=True)
    k = len(xs) * (1 - c)
    whole = int(math.floor(k + 1e-12))
    frac = k - whole
    tail = sum(xs[:whole]) + (frac * xs[whole] if frac > 1e-12 else 0.0)
    return tail / k


print('== the audit example: loss 100 with probability 0.005, otherwise 0; confidence 99%, exceedance 1%')
atoms = [(0.0, 0.995), (100.0, 0.005)]
close('VaR_99%', var_discrete(atoms, 0.99), 0.0)
close('ES_99% (fractional tail mass)', es_fractional(atoms, 0.99), 50.0)
close('ES_99% (quantile integral, midpoint rule)', es_integral(atoms, 0.99), 50.0, 1e-6)
close('E[L | L > VaR] (strict tail conditional expectation)', tce(atoms, 0.99, True), 100.0)
close('E[L | L >= VaR] (weak tail conditional expectation)', tce(atoms, 0.99, False), 0.5)
close('confidence 99.5%: VaR (P(L<=0) = 0.995 already)', var_discrete(atoms, 0.995), 0.0)
close('confidence 99.6%: VaR', var_discrete(atoms, 0.996), 100.0)
close('confidence 99.6%: ES', es_fractional(atoms, 0.996), 100.0)

print('== historical simulation')
hs = [100.0] * 5 + [0.0] * 995          # the same law as an empirical sample of 1000
close('HS, 1000 obs, 10 tail obs: ES_99%', es_hs(hs, 0.99), 50.0)
close('HS, 1000 obs: worst-10 mean equals the fractional formula', es_hs(hs, 0.99), es_fractional([(0.0, 0.995), (100.0, 0.005)], 0.99))
hs250 = [40.0, 30.0, 20.0, 10.0] + [0.0] * 246   # 2.5 tail observations at 99%
close('HS, 250 obs, 2.5 tail obs: (40 + 30 + 0.5*20)/2.5', es_hs(hs250, 0.99), 32.0)
close('HS, 250 obs: same as the fractional formula on the empirical law',
      es_hs(hs250, 0.99), es_fractional([(40.0, 1 / 250), (30.0, 1 / 250), (20.0, 1 / 250), (10.0, 1 / 250), (0.0, 246 / 250)], 0.99), 1e-9)
naive = sum(sorted(hs250, reverse=True)[:2]) / 2
print(f'     (dropping the fraction: worst-2 mean {naive:.1f}; rounding up: worst-3 mean {sum([40, 30, 20]) / 3:.1f})')

print('== a continuous law: all three agree')
random.seed(7)
z99 = 2.3263478740408408
phi = math.exp(-z99 ** 2 / 2) / math.sqrt(2 * math.pi)
close('standard normal ES_99% = phi(z)/0.01', phi / 0.01, 2.665214220345808, 1e-9)
draws = [random.gauss(0, 1) for _ in range(400000)]
close('HS ES_99% on 400000 normal draws within 0.02', es_hs(draws, 0.99), 2.6652, 0.02)
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
