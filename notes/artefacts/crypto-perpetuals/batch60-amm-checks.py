"""Third batch of 17 October 2026: own checks behind def:amm-pool-mechanics.

Sources: Uniswap v2 Core (March 2020): constant product x*y = k, a 30-basis-point fee to liquidity providers (sec. 1),
enforced as (x1 - 0.003 x_in)(y1 - 0.003 y_in) >= x0 y0 (sec. 3.2.1, eq. (10)); Uniswap v3 Core (March 2021): fee
tiers 0.05%, 0.30%, 1% (sec. 1), liquidity L = sqrt(k), and a position on [p_a, p_b] whose real reserves satisfy
(x + L/sqrt(p_b))(y + L sqrt(p_a)) = L^2 (sec. 2, eq. (2.2), read from the page image).
Own derivations checked numerically: the swap output, execution price against the pool price, the value of a
full-range position against holding (impermanent loss 2 sqrt(r)/(1+r) - 1 for a price ratio r, before fees), and the
real reserves of a concentrated position. Run: python3 batch60-amm-checks.py (standard library). Exits non-zero on failure.
"""
import math
import sys

fails = []


def ok(name, cond, detail=''):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


print('== v2 swap with the 0.30% fee')
x, y, dx, fee = 1000.0, 2_000_000.0, 10.0, 0.003  # 1,000 ETH and 2,000,000 USDC; sell 10 ETH
g = 1 - fee
dy = y * g * dx / (x + g * dx)
x1, y1 = x + dx, y - dy
lhs = (x1 - fee * dx) * (y1 - 0)
ok('output satisfies eq. (10) with equality', abs(lhs - x * y) / (x * y) < 1e-12, f'dy = {dy:.4f}')
ok('k rises after the trade (fee retained in the pool)', x1 * y1 > x * y, f'{x1 * y1:.1f} > {x * y:.1f}')
p0, exec_p, p1 = y / x, dy / dx, y1 / x1
print(f'     pool price {p0:.2f}, execution price {exec_p:.2f}, new pool price {p1:.2f}')
ok('execution price lies between pool prices before and after', p1 < exec_p < p0)
ok('fee-free execution shortfall (p0 - exec/g)/p0 = g dx/(x + g dx)', abs((p0 - exec_p / g) / p0 - g * dx / (x + g * dx)) < 1e-12,
   f'{(p0 - exec_p / g) / p0 * 100:.3f}% for a trade of {dx / x * 100:.1f}% of the reserve')

print('== impermanent loss of a full-range position (no fees)')
for r in (0.5, 1.0, 1.5, 2.0, 4.0):
    k = x * y
    p = p0 * r
    xr, yr = math.sqrt(k / p), math.sqrt(k * p)  # arbitraged to the external price p
    v_pool, v_hold = xr * p + yr, x * p + y
    il = v_pool / v_hold - 1
    ok(f'r = {r}: IL = 2 sqrt(r)/(1+r) - 1', abs(il - (2 * math.sqrt(r) / (1 + r) - 1)) < 1e-12, f'{il*100:+.2f}%')

print('== v3 concentrated position')
pa, pb, pc, L = 1600.0, 2500.0, 2000.0, 10_000.0
xr = L * (1 / math.sqrt(pc) - 1 / math.sqrt(pb))
yr = L * (math.sqrt(pc) - math.sqrt(pa))
ok('real reserves satisfy eq. (2.2)', abs((xr + L / math.sqrt(pb)) * (yr + L * math.sqrt(pa)) - L * L) / L ** 2 < 1e-12,
   f'x_real = {xr:.4f}, y_real = {yr:.2f}')
full_x, full_y = L / math.sqrt(pc), L * math.sqrt(pc)  # same L over (0, inf)
eff = (full_x * pc + full_y) / (xr * pc + yr)
print(f'     capital for the same L: full range {full_x * pc + full_y:,.0f} against {xr * pc + yr:,.0f} in [{pa:.0f}, {pb:.0f}], ratio {eff:.2f}')
ok('concentration needs less capital for the same liquidity', eff > 1)
xa = L * (1 / math.sqrt(pa) - 1 / math.sqrt(pb)); yb = L * (math.sqrt(pb) - math.sqrt(pa))
ok('below p_a the position is all X, above p_b all Y', xa > 0 and yb > 0, f'all-X {xa:.4f}, all-Y {yb:.2f}')
if fails:
    print('\nFAILED:', fails)
    sys.exit(1)
print('\nall checks passed')
