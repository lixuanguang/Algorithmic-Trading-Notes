"""Business cycles, fiscal and monetary policy, trade and geopolitical risk (2026-10-19): the worked numbers of
def:business-credit-cycles, meth:business-cycle-indicators, def:fiscal-policy-tools-stance,
def:monetary-policy-transmission-regimes, meth:monetary-fiscal-policy-mix, def:geopolitics-institutions-tools,
meth:geopolitical-risk-assessment and meth:trade-benefits-restrictions-blocs.

Reproduced from Economics for Investment Decision Makers (CFA Institute Investment Series, 2013): the fiscal multiplier
1/[1 - 0.9(1 - 0.2)] = 3.57 (chap. 7, p. 387), the neutral rate 2.5% + 2% = 4.5% (eq. 7-4, p. 368), and the South
African paper tariff (Example 8-5, pp. 426-427: consumer loss 185,000, producer gain 120,000, revenue 40,000,
deadweight loss 25,000). Original: the two-quarter recession rule on a sequence it misses; an excess-credit measure
in the sense of Jorda, Schularick and Taylor (2011); a diffusion index and an inventory-to-sales ratio through a
turn; the multiplier by iterating spending rounds; a balanced-budget expansion; public-debt dynamics and the
debt-stabilising primary balance; a structural deficit; Ricardian equivalence; the quantity identity; a policy stance
against the neutral rate and a Taylor-rule benchmark; a real-rate floor at zero; comparative advantage and the
range of mutually beneficial terms of trade; quota rents; a small-country export subsidy; a large-country tariff;
a GPR-style news share index; and a scenario-weighted geopolitical assessment with a hedge.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python macro-policy-trade-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: business and credit cycles, and the indicators that track them")
q_growth = [
    0.6,
    -0.3,
    0.1,
    -0.4,
    0.5,
]  # quarter-on-quarter real GDP growth, percent (not annualised)
two_q = any(q_growth[i] < 0 and q_growth[i + 1] < 0 for i in range(len(q_growth) - 1))
level = np.cumprod([1 + g / 100 for g in q_growth])
peak_to_trough = level[3] / level[0] - 1
ok(
    "two-quarter rule: growth of -0.3, +0.1, -0.4 percent never gives two negative quarters in a row, yet real GDP"
    " falls 0.60% from its peak; a dating committee looking at many series could still call a recession",
    not two_q and abs(peak_to_trough + 0.006) < 2e-4,
    f"peak-to-trough {peak_to_trough:.4%}",
)
# excess credit: change in bank loans/GDP per year over an expansion, relative to its historical mean
loans_gdp_trough, loans_gdp_peak, years, mean_ppy = 80.0, 98.0, 6, 1.0
ppy = (loans_gdp_peak - loans_gdp_trough) / years
ok(
    "excess credit: loans/GDP from 80% to 98% over a six-year expansion is 3.0 percentage points a year, 2.0 ppy above a"
    " 1.0 ppy historical mean; JST find such credit-intensive booms precede deeper recessions",
    close(ppy, 3.0) and close(ppy - mean_ppy, 2.0),
)
rising, unchanged, falling = 6, 1, 3
diff_index = 100 * (rising + 0.5 * unchanged) / (rising + unchanged + falling)
ok(
    "diffusion index of ten leading components: 6 rising, 1 unchanged, 3 falling gives 65, above the 50 that means no"
    " change in breadth",
    close(diff_index, 65.0),
)
sales = np.array([100.0, 95.0, 90.0, 90.0, 95.0, 100.0])
inventory = np.array(
    [120.0, 120.0, 117.0, 108.0, 105.0, 110.0]
)  # orders cut with a lag, then rebuilt
ratio = inventory / sales
ok(
    "inventory-to-sales ratio: sales turn down in period 1 and up in period 4, but the ratio peaks in period 2 and"
    " troughs in period 4-5: it lags the cycle because inventories adjust after sales",
    int(np.argmax(ratio)) == 2 and int(np.argmin(sales)) in (2, 3) and ratio[-2] < ratio[0],
    " ".join(f"{x:.3f}" for x in ratio),
)

print(
    "== part 2: fiscal policy: multiplier, balanced budget, stance, debt dynamics and Ricardian equivalence"
)
c, t = 0.9, 0.2
mult = 1 / (1 - c * (1 - t))
rounds = sum((c * (1 - t)) ** k for k in range(400))
ok(
    "EIDM: MPC 0.9 and net tax rate 0.2 give a fiscal multiplier of 1/0.28 = 3.57; summing 400 spending rounds gives"
    " the same, so 1bn of extra G raises output by 3.57bn with idle resources",
    abs(mult - 3.5714) < 1e-4 and close(rounds, mult, 1e-9),
    f"{mult:.4f}",
)
# balanced-budget expansion with lump-sum taxes: Y = C0 + c (Y - T) + I + G
c0, inv = 100.0, 100.0


def output(g, tax):
    return (c0 + inv + g - c * tax) / (1 - c)


ok(
    "balanced budget with lump-sum taxes: raising G and T by 100 together raises output by exactly 100 (multiplier 1),"
    " because households cut spending by only c x 100",
    close(output(300.0, 300.0) - output(200.0, 200.0), 100.0, 1e-9),
)


def debt_next(d, r, g, pb):
    return d * (1 + r) / (1 + g) - pb


d0, r_, g_ = 1.72, 0.01, 0.005
pb_star = d0 * (r_ - g_) / (1 + g_)
ok(
    "debt dynamics: debt of 172% of GDP at a 1% nominal rate and 0.5% nominal growth needs a primary surplus of 0.856%"
    " of GDP to stay constant; with a balanced primary budget it rises 0.86 points a year",
    abs(pb_star - 0.008557) < 1e-6
    and close(debt_next(d0, r_, g_, pb_star), d0, 1e-12)
    and abs(debt_next(d0, r_, g_, 0.0) - d0 - 0.008557) < 1e-6,
    f"{pb_star:.4%}",
)
ok(
    "when growth exceeds the interest rate (r = 3%, g = 5%) a 60% debt ratio falls with a zero primary balance",
    debt_next(0.60, 0.03, 0.05, 0.0) < 0.60,
)
deficit, gap, semi_el = -0.06, -0.04, 0.5
cyclical = semi_el * gap
ok(
    "structural deficit: an actual deficit of 6% of GDP with a -4% output gap and budget semi-elasticity 0.5 has a"
    " cyclical part of -2% and a structural deficit of -4%: the stance is looser than neutral but not by 6 points",
    close(cyclical, -0.02) and close(deficit - cyclical, -0.04),
)
cut, r_d = 10.0, 0.04
ok(
    "Ricardian equivalence: a 10bn tax cut financed by a one-year bond repaid with 10.4bn of taxes next year leaves the"
    " present value of household taxes unchanged, so consumption need not change",
    close(-cut + cut * (1 + r_d) / (1 + r_d), 0.0, 1e-12),
)

print(
    "== part 3: monetary policy: quantity identity, neutral rate, Taylor benchmark and the zero bound"
)
m_g, y_g = 0.07, 0.03
infl = (1 + m_g) / (1 + y_g) - 1
ok(
    "MV = PY with constant velocity: 7% money growth and 3% real growth give 3.88% inflation (4% to first order)",
    abs(infl - 0.03883) < 1e-5,
)
neutral = 0.025 + 0.02
ok(
    "EIDM eq. (7-4): neutral rate = trend real growth 2.5% + inflation target 2% = 4.5%; a 5.25% policy rate is"
    " contractionary, a 3.5% rate expansionary",
    close(neutral, 0.045) and 0.0525 > neutral > 0.035,
)
taylor = 0.02 + 0.03 + 0.5 * (0.03 - 0.02) + 0.5 * (-1.0 / 100)
ok(
    "Taylor benchmark with r* = 2%: inflation 3%, target 2%, output gap -1% gives 5.0%; a policy rate of 4.5% is easier"
    " than the rule",
    close(taylor, 0.05),
)
ok(
    "zero bound: with inflation at -1% a zero policy rate is a +1% real rate, while a rule calling for -2% nominal"
    " leaves policy 2 points too tight; hence QE and forward guidance",
    close(0.0 - (-0.01), 0.01) and close(0.0 - (-0.02), 0.02),
)

print("== part 4: international trade: comparative advantage, tariffs, quotas, subsidies")
# output per worker per year: A makes 4 cloth or 2 wine; B makes 1 cloth or 1 wine
oc_a_cloth, oc_b_cloth = 2 / 4, 1 / 1  # wine forgone per unit of cloth
tot = 0.75  # wine per cloth
# A specialises in cloth and trades 1 cloth for 0.75 wine; B specialises in wine and trades 0.75 wine for 1 cloth
a_wine_by_trade, a_wine_by_making = tot, oc_a_cloth  # wine A obtains by giving up one cloth
b_cloth_by_trade, b_cloth_by_making = 1.0, tot / oc_b_cloth  # cloth B obtains for 0.75 wine
ok(
    "comparative advantage: B is absolutely less productive in both goods, but A's opportunity cost of cloth is 0.5"
    " wine against B's 1.0; at 0.75 wine per cloth A gets 0.75 wine per cloth traded (0.5 if it made the wine) and B"
    " gets a cloth for 0.75 wine (0.75 cloth if it made it): both gain, and neither would at terms outside 0.5-1.0",
    oc_a_cloth < oc_b_cloth
    and a_wine_by_trade > a_wine_by_making
    and b_cloth_by_trade > b_cloth_by_making
    and 1.2 > oc_b_cloth  # at 1.2 wine per cloth B pays more than its own cost of cloth
    and 0.4 < oc_a_cloth,  # at 0.4 A gets less wine than it could make itself
)
workers = 100
autarky = {
    "cloth": 0.5 * workers * 4 + 0.5 * workers * 1,
    "wine": 0.5 * workers * 2 + 0.5 * workers * 1,
}
# specialise: A puts 75 workers in cloth, 25 in wine; B all in wine
spec = {"cloth": 75 * 4, "wine": 25 * 2 + 100 * 1}
ok(
    "with 100 workers each split evenly, the world makes 250 cloth and 150 wine; with A 75/25 and B all wine it makes"
    " 300 cloth and 150 wine: more of one good and no less of the other",
    autarky == {"cloth": 250.0, "wine": 150.0} and spec == {"cloth": 300, "wine": 150},
)
pw, tariff = 5.0, 1.0
q_s0, q_d0, q_s1, q_d1 = 110_000, 200_000, 130_000, 170_000
cs_loss = tariff * q_d1 + 0.5 * tariff * (q_d0 - q_d1)
ps_gain = tariff * q_s0 + 0.5 * tariff * (q_s1 - q_s0)
revenue = tariff * (q_d1 - q_s1)
dwl = cs_loss - ps_gain - revenue
ok(
    "EIDM Example 8-5 (paper, world price 5, 20% tariff): consumer loss 185,000, producer gain 120,000, revenue 40,000,"
    " deadweight loss 25,000 (production 10,000 + consumption 15,000)",
    (cs_loss, ps_gain, revenue, dwl) == (185_000.0, 120_000.0, 40_000.0, 25_000.0)
    and close(dwl, 0.5 * tariff * (q_s1 - q_s0) + 0.5 * tariff * (q_d0 - q_d1)),
)
ok(
    "an import quota of 40,000 tons has the same price effect; if foreign exporters keep the 40,000 quota rent the"
    " national loss is 65,000 instead of 25,000",
    close(dwl + revenue, 65_000.0),
)
# small-country export subsidy: domestic price rises to world price + s; linear S = 20P, D = 100 - 10P, world P = 5
s_sub = 1.0
supply = lambda p: 20 * p
demand = lambda p: 100 - 10 * p
p0, p1 = 5.0, 6.0
cs_l = (demand(p0) + demand(p1)) / 2 * s_sub
ps_g = (supply(p0) + supply(p1)) / 2 * s_sub
cost = s_sub * (supply(p1) - demand(p1))
ok(
    "small-country export subsidy of 1 (S = 20P, D = 100 - 10P, world price 5): consumers lose 45, producers gain 110,"
    " the subsidy costs 80, a national loss of 15 (two deadweight triangles of 10 and 5)",
    (cs_l, ps_g, cost) == (45.0, 110.0, 80.0) and close(cs_l - ps_g + cost, 15.0),
)


# large importer: home demand D = 100 - P, home supply S = P, foreign export supply X = P_w - 20 (P_w world price)
def large_tariff(tau):
    pw_ = brentq(lambda p: (100 - (p + tau)) - (p + tau) - (p - 20), 0, 100)
    pd = pw_ + tau
    imports = (100 - pd) - pd
    cs = 0.5 * (100 - pd) ** 2
    ps = 0.5 * pd**2
    return pw_, imports, cs + ps + tau * imports


w0 = large_tariff(0.0)
w5 = large_tariff(5.0)
tot_gain = (w0[0] - w5[0]) * w5[1]
dwl_large = 0.5 * (w5[0] + 5.0 - w0[0]) * (w0[1] - w5[1])
foreign_loss = 0.5 * (w0[0] - 20) ** 2 - 0.5 * (w5[0] - 20) ** 2
ok(
    "large importer (D = 100 - P, S = P, foreign supply X = P_w - 20): a tariff of 5 lowers the world price from 40 to"
    " 36.67, so foreign exporters bear two-thirds of it; home welfare rises 52.78 (terms-of-trade gain 55.56 less"
    " deadweight loss 2.78), but foreign producers lose 61.11, so world welfare falls 8.33",
    abs(w0[0] - 40.0) < 1e-9
    and abs(w5[0] - 36.6667) < 1e-4
    and abs(w5[2] - w0[2] - 52.7778) < 1e-4
    and abs(tot_gain - dwl_large - (w5[2] - w0[2])) < 1e-6
    and abs(foreign_loss - 61.1111) < 1e-4
    and abs((w5[2] - w0[2]) - foreign_loss + 8.3333) < 1e-4,
    f"world price {w5[0]:.4f}, imports {w5[1]:.3f}, home welfare change {w5[2] - w0[2]:.4f}",
)

print("== part 5: geopolitical risk: a news-share index and a scenario assessment")
rng = np.random.default_rng(20261019)
total = rng.integers(9_000, 11_000, size=120)
hits = rng.binomial(total, 0.03)
hits[100:103] = (total[100:103] * 0.09).astype(int)  # a three-month episode
share = hits / total
gpr = (
    100 * share / share[:60].mean()
)  # normalised to 100 over the first five years (the reference period)
ok(
    "GPR-style index: the share of articles with adverse geopolitical terms, scaled so the reference period averages"
    " 100; a tripling of the share for three months reads about 300",
    close(gpr[:60].mean(), 100.0, 1e-9) and 270 < gpr[100:103].mean() < 330,
    f"episode mean {gpr[100:103].mean():.0f}",
)
scen = {"base": (0.70, 0.06), "escalation": (0.20, -0.18), "de-escalation": (0.10, 0.12)}
exp_ret = sum(p * r for p, r in scen.values())
put_cost, put_payoff_esc = 0.012, 0.15
hedged = {
    k: r - put_cost + (put_payoff_esc if k == "escalation" else 0.0) for k, (_, r) in scen.items()
}
exp_hedged = sum(scen[k][0] * v for k, v in hedged.items())
ok(
    "scenario weights 70/20/10 with returns +6%/-18%/+12% give +1.8% expected; a put costing 1.2% that pays 15% in"
    " escalation lifts the worst case from -18% to -4.2% and the expected return to 3.6%, because its payoff is"
    " worth more than its cost under these (subjective) probabilities",
    abs(exp_ret - 0.018) < 1e-12
    and abs(hedged["escalation"] + 0.042) < 1e-12
    and abs(exp_hedged - 0.036) < 1e-12,
)
# An event state price is not a physical probability. At zero interest it
# equals the risk-neutral probability only for this binary fixed-date payoff.
state_price = put_cost / put_payoff_esc
bond_price = math.exp(-0.04)
pricing_probability = state_price / bond_price
ok(
    "premium/payoff identifies a state price; discounting recovers pricing probability",
    close(state_price, 0.08) and close(bond_price * pricing_probability * put_payoff_esc, put_cost),
)
# The stated portfolio objective can favour insurance despite negative expected net payoff.
low_probability = np.array([0.85, 0.05, 0.10])
base_returns = np.array([0.06, -0.18, 0.12])
insured_returns = base_returns - put_cost + np.array([0, 0.15, 0])
ok(
    "5% physical probability: expected hedge P&L is -0.45%, yet the loss and premium limits are met",
    close(low_probability @ (insured_returns - base_returns), -0.0045)
    and insured_returns.min() >= -0.05
    and base_returns.min() < -0.05
    and put_cost <= 0.015,
)
# Exponential utility supplies a second, preference-dependent criterion.
util = lambda r: -np.exp(-30 * r)
ok(
    "risk-averse utility can prefer insurance below the pricing probability",
    low_probability @ util(insured_returns) > low_probability @ util(base_returns),
)


print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
