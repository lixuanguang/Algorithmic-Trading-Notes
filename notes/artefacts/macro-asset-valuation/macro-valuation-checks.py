"""The economy and asset values (2026-10-19): the worked numbers of res:economy-discount-rates-cash-flows,
meth:cycle-rates-breakevens-spreads and meth:cycle-equities-property.

Reproduced: Ang, Asset Management (2014), chap. 9, p. 291: the Ang-Piazzesi decomposition of short and long nominal
yields into real rate, expected inflation and risk premium (1.2 + 3.9 + 0.3 = 5.4; 1.3 + 3.9 + 1.1 = 6.3); chap. 7,
Table 7.2, pp. 215-217: mean returns of large stocks 5.6% in recessions against 12.4% in expansions and of government
bonds 12.3% against 5.9%. Cochrane, Asset Pricing (rev. ed., 2005), sec. 1.4.1, eq. (1.7): the real risk-free rate
delta + gamma E[g] - gamma^2/2 var(g). Original: news against expectations in a growing perpetuity; a two-state
consumption economy in which an asset that pays off in bad times earns a negative premium; breakevens with an
inflation risk premium; expected loss and the credit spread over the cycle; Gordon-model multiples and their
sensitivity to real rates, risk premia and growth; operating leverage; and cap-rate valuation of property.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python macro-valuation-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: value as discounted expected cash flows; news against expectations")


def gordon(d1, r, g):
    return d1 / (r - g)


p_base = gordon(4.0, 0.08, 0.04)
p_expected = gordon(4.0 * 1.04, 0.08, 0.04)  # one year later, growth as expected
p_surprise = gordon(4.0 * 1.04, 0.08, 0.045)  # expected growth revised up by 0.5 points
ok(
    "a perpetuity paying 4 growing at 4% discounted at 8% is worth 100; a year later, with growth exactly as expected,"
    " it is worth 104 (a total return of 8%, the discount rate): expected news moves nothing beyond the required return",
    close(p_base, 100.0) and close((p_expected + 4.0) / p_base - 1, 0.08, 1e-12),
)
ok(
    "an upward revision of expected growth to 4.5% lifts the value to 118.86: prices react to revisions, not to the level"
    " of growth that was already expected",
    abs(p_surprise - 118.857) < 1e-3,
)
ok(
    "a 1-point rise in the discount rate (default-free rate or risk premium) cuts the value from 100 to 80; the same"
    " economic news can work through cash flows, rates or premia with different signs",
    close(gordon(4.0, 0.09, 0.04), 80.0),
)

print("== part 2: consumption risk, the real rate and the equity premium")
delta, gam, g_c, s_c = 0.01, 2.0, 0.02, 0.01
r_f = delta + gam * g_c - 0.5 * gam**2 * s_c**2
ok(
    "Cochrane eq. (1.7): delta 1%, gamma 2, expected consumption growth 2%, volatility 1% give a log real rate of"
    " 4.98%; faster expected growth raises it, more volatile growth lowers it (precautionary saving)",
    abs(r_f - 0.0498) < 1e-12
    and delta + gam * 0.03 - 0.5 * gam**2 * s_c**2 > r_f
    and delta + gam * g_c - 0.5 * gam**2 * 0.03**2 < r_f,
)
beta_ = math.exp(-delta)
cons = np.array([1.04, 0.99])  # gross consumption growth in boom and recession
prob = np.array([0.8, 0.2])
m = beta_ * cons ** (-gam)
rf_gross = 1 / (prob @ m)
stock = np.array([1.20, 0.85])  # pays off in booms
bond = np.array([1.02, 1.08])  # pays off in recessions
p_stock, p_bond = prob @ (m * stock), prob @ (m * bond)
er_stock, er_bond = (prob @ stock) / p_stock - rf_gross, (prob @ bond) / p_bond - rf_gross
ok(
    "two-state economy (consumption +4% in boom, -1% in recession, 80/20): an asset paying 1.20/0.85 earns a positive"
    " premium; one paying 1.02/1.08 (a hedge, like government bonds in recessions) earns a negative premium: premia"
    " reward payoffs that are low in bad times",
    er_stock > 0 > er_bond
    and close(er_stock, -rf_gross * (prob @ ((m - prob @ m) * (stock / p_stock))), 1e-12),
    f"stock premium {er_stock:.4%}, bond premium {er_bond:.4%}",
)
large = {"recession": 5.6, "expansion": 12.4}
govt = {"recession": 12.3, "expansion": 5.9}
ok(
    "Ang Table 7.2: large stocks return 5.6% in NBER recessions against 12.4% in expansions; government bonds 12.3%"
    " against 5.9%: bonds hedge recessions",
    large["recession"] < large["expansion"] and govt["recession"] > govt["expansion"],
)

print("== part 3: rates, curve, breakevens and credit spreads over the cycle")
short = 1.2 + 3.9 + 0.3
long_ = 1.3 + 3.9 + 1.1
ok(
    "Ang-Piazzesi decomposition: short 5.4% and long 6.3%; of the 0.9-point slope, 0.8 points are risk premium and"
    " only 0.1 real rate",
    close(short, 5.4, 1e-9)
    and close(long_, 6.3, 1e-9)
    and close((1.1 - 0.3) / (long_ - short), 8 / 9, 1e-9),
)
nominal, real_y, irp, liq = 0.043, 0.019, 0.003, 0.002
bei = nominal - real_y
ok(
    "breakeven: a 4.3% nominal and 1.9% real yield give a 2.4% breakeven; with a 0.3% inflation risk premium and a 0.2%"
    " real-bond liquidity premium (which lowers the breakeven), expected inflation is 2.3%",
    close(bei, 0.024, 1e-12) and close(bei - irp + liq, 0.023, 1e-12),
)
pd_exp, pd_rec, lgd = 0.015, 0.045, 0.60
el_exp, el_rec = pd_exp * lgd, pd_rec * lgd
spread_exp, spread_rec = el_exp + 0.010, el_rec + 0.025
ok(
    "high-yield spread: expected loss 0.9% in expansion (PD 1.5%, LGD 60%) rises to 2.7% in recession; with the risk"
    " premium rising from 1.0 to 2.5 points, the spread widens from 1.9% to 5.2%: both default and its price rise",
    close(el_exp, 0.009, 1e-12)
    and close(el_rec, 0.027, 1e-12)
    and close(spread_rec - spread_exp, 0.033, 1e-12),
)

print("== part 4: earnings, multiples and property over the cycle")
sales0, sales1, fixed, var_ratio = 100.0, 95.0, 30.0, 0.5
ebit0 = sales0 * (1 - var_ratio) - fixed
ebit1 = sales1 * (1 - var_ratio) - fixed
ok(
    "operating leverage: a 5% fall in sales with fixed costs of 30 and variable costs of 50% cuts operating profit by"
    " 12.5% (degree of operating leverage 2.5): cyclical firms' earnings swing more than the economy",
    close(ebit1 / ebit0 - 1, -0.125, 1e-12)
    and close((sales0 * (1 - var_ratio)) / ebit0, 2.5, 1e-12),
)
payout, g_e = 0.5, 0.05


def pe(real, erp, infl=0.02):
    return payout * (1 + g_e) / (real + infl + erp - g_e)


ok(
    "Gordon multiple (payout 50%, nominal growth 5%): with a 1.5% real rate, 2% inflation and a 4% equity premium the"
    " trailing P/E is 21.0; a 0.5-point lower real rate lifts it to 26.25; a 1-point higher premium cuts it to 15.0",
    abs(pe(0.015, 0.04) - 21.0) < 1e-9
    and abs(pe(0.010, 0.04) - 26.25) < 1e-9
    and abs(pe(0.015, 0.05) - 15.0) < 1e-9,
)
E0, E1, D1 = 10.0, 10.5, 5.25
for required, trailing, forward in (
    (0.075, 21.0, 20.0),
    (0.07, 26.25, 25.0),
    (0.085, 15.0, 100 / 7),
):
    # Direct dividend PV sum independently verifies both earnings denominators.
    terms = np.arange(1, 3001)
    price = np.sum(D1 * (1.05 / (1 + required)) ** terms / 1.05)
    ok(
        f"Gordon price {price:.4f}: matching trailing and forward denominators",
        close(price / E0, trailing, 1e-8)
        and close(price / E1, forward, 1e-8)
        and close(D1 / E1, payout),
    )
noi, cap0, cap1 = 5.0, 0.05, 0.055
ok(
    "property: NOI of 5 at a 5.0% cap rate is worth 100; a rise in the cap rate to 5.5% (higher rates or premia, weaker"
    " outlook) cuts the value 9.1% with NOI unchanged; expected return ~ cap rate + NOI growth - change in cap rate",
    close(noi / cap0, 100.0) and abs(noi / cap1 / (noi / cap0) - 1 + 0.0909) < 1e-4,
)
noi_g = 0.02
ok(
    "with NOI growing 2% and the cap rate stable, the expected total return is about 7% (5% income + 2% growth); a"
    " recession that cuts NOI 5% and lifts the cap rate 0.5 points cuts the value 13.6%",
    abs((noi * 0.95 / cap1) / 100 - 1 + 0.13636) < 1e-4 and close(cap0 + noi_g, 0.07, 1e-12),
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
