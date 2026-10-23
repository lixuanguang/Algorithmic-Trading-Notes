"""Commodity investment: return components, roll yield, diversification return, swaps and index construction (2026-10-20).

Worked numbers of def:commodity-features, meth:commodity-sectors-participants, meth:commodity-futures-return-components
and meth:commodity-swaps-index-construction. The curves, prices and positions are hypothetical except where a check
reproduces a published figure (Ang 2014, Table 11.7 and eq. 11.3; Erb and Harvey 2005, pp. 13 and 24-26; Gorton and
Rouwenhorst 2006, p. 6; Geman 2005, p. 144; Hull 2022, p. 781).

Independent routes: a fully collateralised futures position simulated contract by contract against the sum of spot,
roll and collateral components; the roll return with a fixed curve against the ratio of prices; the diversification
return measured from a rebalanced path against half the difference between variance and covariance; the swap value
from forward prices against the sum of discounted settlements; index returns under two weightings and two roll
schedules computed from the same paths.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python commodity-return-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------------------------
print("== part 1: published decompositions and roll arithmetic")
ok(
    "Ang Table 11.7 (GSCI, 1970-2011): total 11.3% = spot 6.4% + cash 5.6% + roll -0.7%",
    close(6.4 + 5.6 - 0.7, 11.3, 1e-12),
)
decades = {
    "1970s": (11.1, 6.6, 4.0, 21.6),
    "1980s": (-0.4, 9.1, 2.4, 11.1),
    "1990s": (0.8, 5.0, -0.5, 5.3),
}
decades["2000-2011"] = (13.0, 2.3, -7.5, 7.8)
gaps = {k: round(s + c + r - t, 1) for k, (s, c, r, t) in decades.items()}
ok(
    "Ang Table 11.7 decade rows add up except the 1970s, where 11.1 + 6.6 + 4.0 = 21.7 against 21.6 printed",
    gaps == {"1970s": 0.1, "1980s": 0.0, "1990s": 0.0, "2000-2011": 0.0},
    str(gaps),
)
ok(
    "Ang eq. 11.3: variance shares 100.0 + 0.2 + 6.0 + 2(-3.4) + 2(0.2) + 2(0.1) = 100% - spot carries the risk",
    close(100.0 + 0.2 + 6.0 + 2 * (-3.4) + 2 * 0.2 + 2 * 0.1, 100.0, 1e-9),
)
spot0, fut0, expected = 30.0, 25.0, 27.0
ok(
    "Gorton and Rouwenhorst p. 6: spot 30, future 25, expected 27 - at 27 the spot holder loses 3 and the futures "
    "buyer gains the 2 premium; at 26 the futures buyer gains 1 = premium 2 less surprise 1",
    close(expected - spot0, -3.0)
    and close(expected - fut0, 2.0)
    and close(26.0 - fut0, (expected - fut0) - (expected - 26.0)),
)
ok(
    "Geman p. 144: ending stocks 540m bushels over use of 2.7bn = 20% stocks-to-use",
    close(540 / 2700, 0.20),
)
oil_roll = 40.95 / 36.65 - 1
gold_roll = 398.3 / 404 - 1
ok(
    "Erb and Harvey's May 2004 curves: gold's roll return 398.3/404 - 1 = -1.41% as printed; oil's 40.95/36.65 - 1 "
    "is 11.73%, not the 13.1% printed",
    round(gold_roll * 100, 2) == -1.41
    and round(oil_roll * 100, 2) == 11.73
    and abs(oil_roll - 0.131) > 0.01,
)
avg_var, avg_cov = (21.2 + 4.4) / 2, (9.5 + 1.1) / 2
ok(
    "Erb and Harvey Table 6: average variance 12.8%, average covariance 5.3%; half the difference is 3.75%, against "
    "the 3.4% measured (10.9% - 7.5%) and the 'about 3.5%' stated",
    close(avg_var, 12.8)
    and close(avg_cov, 5.3)
    and close((avg_var - avg_cov) / 2, 3.75)
    and close(10.9 - 7.5, 3.4),
)

# ---------------------------------------------------------------------------------------------
print("== part 2: a fully collateralised position rolled quarterly - spot, roll and collateral")
RF = 0.04  # annual T-bill yield on the collateral


def simulate(spot_path, basis):
    """Hold the 3-month contract priced at S(1 + basis) and roll at expiry into the next; collateral earns RF.

    Returns the total-return index value after the path and its components.
    """
    value = 1.0
    excess = 1.0
    for q in range(len(spot_path) - 1):
        f_buy = spot_path[q] * (1 + basis)
        f_sell = spot_path[q + 1]  # converges to spot at expiry
        r_fut = f_sell / f_buy - 1
        excess *= 1 + r_fut
        value *= 1 + r_fut + RF / 4
    return value, excess


flat = [100.0] * 5
tr_back, er_back = simulate(flat, -0.02)
tr_cont, er_cont = simulate(flat, +0.02)
ok(
    "spot unchanged for a year: in backwardation (futures 2% below spot) each roll earns 2.04% and the excess return "
    "is 8.42%; in contango (2% above) it is -7.62%",
    round((100 / 98 - 1) * 100, 2) == 2.04
    and round((er_back - 1) * 100, 2) == 8.42
    and round((er_cont - 1) * 100, 2) == -7.62,
)
ok(
    "with 1% a quarter on the collateral, the total return is 12.73% in backwardation and -3.79% in contango",
    round((tr_back - 1) * 100, 2) == 12.73 and round((tr_cont - 1) * 100, 2) == -3.79,
)
down = [100.0, 98.75, 97.5, 96.25, 95.0]
tr_d, er_d = simulate(down, -0.02)
ok(
    "spot falling 5% in a backwardated market: the excess return is still +3.00% and the total +7.15% - futures can "
    "earn when spot falls",
    round((er_d - 1) * 100, 2) == 3.00 and round((tr_d - 1) * 100, 2) == 7.15,
)

# ---------------------------------------------------------------------------------------------
print("== part 3: index construction - weighting, rebalancing and roll schedule")
a_ret = np.array([0.50, -1 / 3, 0.50, -1 / 3])  # volatile commodity, zero geometric return
b_ret = np.zeros(4)


def rebalanced(w):
    return float(np.prod(1 + w * a_ret + (1 - w) * b_ret)) - 1


bh = (0.5 * np.prod(1 + a_ret) + 0.5) - 1
ok(
    "two commodities, one swinging +50%/-33.3% (no net change), one flat: buy-and-hold gains 0, an equally weighted "
    "monthly rebalanced index gains 8.51%, a 90/10 weighting 3.02%",
    close(bh, 0.0, 1e-12)
    and round(rebalanced(0.5) * 100, 2) == 8.51
    and round(rebalanced(0.9) * 100, 2) == 3.02,
)
front, deferred = -0.02, -0.0075  # monthly roll cost in a contango steeper at the front
ok(
    "roll schedule: in a contango of 2% a month at the front but 0.75% a month further out, rolling the front contract "
    "costs 21.53% a year against 8.64% for a deferred contract",
    round((1 - (1 + front) ** 12) * 100, 2) == 21.53
    and round((1 - (1 + deferred) ** 12) * 100, 2) == 8.64,
)

# ---------------------------------------------------------------------------------------------
print("== part 4: commodity swaps")
ok(
    "Hull's oil swap: paying 5m a year for 100,000 barrels at the market price locks in $50 a barrel; at a spot of "
    "$60 the consumer receives a net 1m",
    close(5e6 / 1e5, 50.0) and close(1e5 * 60 - 5e6, 1e6),
)
fwd = np.array([52.0, 54.0, 55.0])
df = 1.04 ** -np.arange(1, 4)
value = float(np.sum((fwd - 50.0) * 1e5 * df))
ok(
    "a three-year swap fixed at $50 when forwards are 52, 54 and 55 and rates 4%: worth 1.01m to the fixed payer",
    round(value / 1e6, 2) == 1.01,
)
tr_index, bill, spread = 0.071, 0.04, 0.0025
ok(
    "a total return swap on a commodity index: the investor receives the index total return (7.1%) and pays bills plus "
    "25 bp (4.25%), netting the excess return less the spread: 2.85%",
    close(tr_index - (bill + spread), 0.0285, 1e-12),
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
