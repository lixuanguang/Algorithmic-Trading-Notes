"""Numerical checks for mech:perpetual-funding (slice 24, 2026-10-15).

Run from the repository root:  python3 notes/artefacts/crypto-mm-microstructure/funding_checks.py
Standard library only. Rates are in percent per 8 hours, as Deribit quotes them; the closed form
Deribit prints (max/min with a damper and caps) is compared with an independent piecewise reading
of its prose rule, and every worked example on the Funding Specifications page (edited 27 July 2026)
is recomputed. Exits non-zero if a check fails.
"""
import sys

TOL = 1e-12
failures = []


def check(name, got, want, tol=TOL):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got:.12g}, want {want:.12g}")
    if not ok:
        failures.append(name)


DAMPER = 0.025  # percent
CAPS = {'BTC': 0.5, 'ETH': 1.0, 'USDC/USDT': 5.0}  # percent, symmetric


def closed_form(premium, cap):
    """Deribit's printed formula: Min(MaxCap, Max(MinCap, Max(0.025%, P) + Min(-0.025%, P)))."""
    return min(cap, max(-cap, max(DAMPER, premium) + min(-DAMPER, premium)))


def piecewise(premium, cap):
    """Deribit's prose: zero inside the damper band, otherwise shrink towards zero by 0.025%, then cap."""
    if -DAMPER <= premium <= DAMPER:
        raw = 0.0
    elif premium > DAMPER:
        raw = premium - DAMPER
    else:
        raw = premium + DAMPER
    return min(cap, max(-cap, raw))


def premium_rate(mark, index):
    return (mark - index) / index * 100.0


print("1. Closed form against piecewise rule on a grid of premium rates")
for cap in CAPS.values():
    for i in range(-2000, 2001):
        p = i * 0.005  # -10% to +10% in 0.005% steps
        a, b = closed_form(p, cap), piecewise(p, cap)
        if abs(a - b) > 1e-12:
            failures.append(f'grid cap={cap} p={p}')
print(f"   {'all grid points agree' if not any(f.startswith('grid') for f in failures) else 'grid mismatch'}")

print("2. Worked examples (payment = rate/100 * position * minutes/480, in the settlement unit)")
# BTC inverse perpetual: position quoted USD 100,000 = 1 BTC at index 100,000; payment in BTC.
r = closed_form(premium_rate(100_075, 100_000), CAPS['BTC'])
check("   BTC example 1 rate (%)", r, 0.05)
check("   BTC 1 minute, 1 BTC (BTC)", r / 100 * 1 * 1 / 480, 0.000001041667, 1e-12)
check("   BTC 8 hours (BTC)", r / 100 * 1 * 480 / 480, 0.0005)
# ETH inverse perpetual: USD 5,000 = 1 ETH.
r = closed_form(premium_rate(5_005, 5_000), CAPS['ETH'])
check("   ETH example 1 rate (%)", r, 0.075)
check("   ETH 1 minute, 1 ETH (ETH)", r / 100 * 1 / 480, 0.0000015625)
check("   ETH 8 hours (ETH)", r / 100 * 1, 0.00075)
# SOL_USDC linear perpetual: USDC 100,000 = 1,000 SOL; payment in USDC.
r = closed_form(premium_rate(100.10, 100.0), CAPS['USDC/USDT'])
check("   SOL_USDC example 1 rate (%)", r, 0.075)
check("   SOL_USDC 1 minute (USDC)", r / 100 * 100_000 / 480, 0.15625)
check("   SOL_USDC 8 hours (USDC)", r / 100 * 100_000, 75.0)
# Example 3: symmetric premium for one minute each nets to zero.
up = closed_form(premium_rate(100_075, 100_000), CAPS['BTC'])
dn = closed_form(premium_rate(99_925, 100_000), CAPS['BTC'])
check("   BTC example 3 net over two minutes (BTC)", (up + dn) / 100 / 480, 0.0)
# Example 4: inside the damper band.
check("   BTC example 4 rate (%)", closed_form(premium_rate(100_020, 100_000), CAPS['BTC']), 0.0)
check("   ETH example 4 rate (%)", closed_form(premium_rate(5_001, 5_000), CAPS['ETH']), 0.0)
# Example 5: caps bind.
check("   BTC example 5 rate (%)", closed_form(premium_rate(107_500, 100_000), CAPS['BTC']), 0.5)
check("   ETH example 5 rate (%)", closed_form(premium_rate(5_100, 5_000), CAPS['ETH']), 1.0)
check("   ETH example 5 uncapped (%)", premium_rate(5_100, 5_000) - DAMPER, 1.975)
check("   USDC example 5 rate (%)", closed_form(premium_rate(107.5, 100.0), CAPS['USDC/USDT']), 5.0)

print("3. Sign convention: positive rate, longs pay; a long's cash flow is -rate * size * fraction")
long_flow = -closed_form(0.075, CAPS['BTC']) / 100 * 1 / 480
short_flow = -long_flow
check("   long + short flows sum to zero (no fee on funding)", long_flow + short_flow, 0.0)

if failures:
    print(f"{len(failures)} check(s) failed: {failures[:5]}")
    sys.exit(1)
print("all checks passed")
