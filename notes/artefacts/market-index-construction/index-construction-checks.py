"""Index values and returns (2026-10-18): the worked examples of meth:index-value-return-calculation and
def:equity-fixed-income-index-types.

Three invented stocks A, B and C over three closes (day 0, 1 and 2), a two-bond invented fixed-income index over
one month, and the conventions of S&P DJI's Index Mathematics Methodology (September 2026): level = market value /
divisor; the divisor is changed so that the level is unchanged by a constituent or share change (eqs. (6) and (7));
a stock split changes shares and price but not market value; a price-weighted index adjusts its divisor for a split;
total return adds index dividend points on the ex-date; net total return deducts withholding first; equal weights
are reset with additional weight factors at each rebalancing; one-way turnover is half the sum of absolute weight
changes. Bond returns follow Bloomberg's Fixed Income Index Methodology (8 January 2026): price, coupon and
paydown return on the beginning dirty value, weights fixed at the beginning market value of the returns universe.

Every input is invented. No random draws. Run: uv run python index-construction-checks.py   (numpy). Exits 1 on
failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


# Inputs. Prices in currency units; shares in millions; IWF = investable weight factor.
P0 = np.array([50.0, 20.0, 80.0])
P1 = np.array([55.0, 19.0, 84.0])
shares0 = np.array([100.0, 300.0, 50.0])
iwf = np.array([0.8, 1.0, 0.5])

print("== part 1: price-weighted index with a 2-for-1 split in C after the close of day 1")
D0 = P0.sum() / 100.0  # base level 100
L0 = P0.sum() / D0
L1 = P1.sum() / D0
ok("divisor 1.5 gives a base of 100.00", close(D0, 1.5) and close(L0, 100.0))
ok("day 1 level 105.3333 (+5.3333%)", close(L1, 158 / 1.5) and abs(L1 / L0 - 1 - 0.053333) < 1e-6)
w_pw = P0 / P0.sum()
ok(
    "price weights at day 0 are 33.3, 13.3, 53.3%; C dominates because its price is highest",
    np.allclose(w_pw, [1 / 3, 2 / 15, 8 / 15]),
)
P1_split = P1.copy()
P1_split[2] /= 2  # C's price halves; its share count doubles
D1 = P1_split.sum() / L1  # S&P DJI eq. (6): new divisor keeps the level
ok(
    "post-split divisor 1.101266 keeps the level at 105.3333",
    close(D1, 116 / L1) and close(P1_split.sum() / D1, L1),
)
P2 = np.array([54.0, 20.0, 44.0])
L2 = P2.sum() / D1
ok(
    "day 2 level 107.1494 (+1.7241%)",
    abs(L2 - 107.149425) < 1e-5 and abs(L2 / L1 - 1 - 0.017241) < 1e-6,
)
L2_wrong = P2.sum() / D0
ok(
    "without the divisor change day 2 would print 78.67, a spurious fall of 25.3%",
    abs(L2_wrong - 78.6667) < 1e-4 and abs(L2_wrong / L1 - 1 + 0.25316) < 1e-4,
)
# After the split C's weight halves although nothing economic happened: price-weighted weights depend on price level.
w_after = P1_split / P1_split.sum()
ok(
    "C's price weight falls from 53.2% to 36.2% at the split",
    abs(P1[2] / P1.sum() - 0.5316) < 1e-4 and abs(w_after[2] - 0.3621) < 1e-4,
)

print("== part 2: float-adjusted capitalisation-weighted index")
q0 = shares0 * iwf
MV0 = (P0 * q0).sum()
Dc0 = MV0 / 1000.0
MV1 = (P1 * q0).sum()
Lc1 = MV1 / Dc0
ok(
    "index market value 12,000 (millions) and divisor 12 for a base of 1,000",
    close(MV0, 12000) and close(Dc0, 12),
)
ok("day 1 level 1,016.667 (+1.6667%)", close(Lc1, 12200 / 12))
w0 = P0 * q0 / MV0
r1 = P1 / P0 - 1
ok(
    "the same return as the weighted sum of constituent returns: 1/3 x 10% + 1/2 x (-5%) + 1/6 x 5%",
    close((w0 * r1).sum(), Lc1 / 1000 - 1),
)
# Corporate actions after the close of day 1: C splits 2-for-1 (no market-value change, no divisor change);
# B issues 30 million new shares (IWF 1.0): market value rises by 19 x 30 = 570, so the divisor rises (eq. (7)).
shares1 = shares0 * np.array([1.0, 1.0, 2.0]) + np.array([0.0, 30.0, 0.0])
q1 = shares1 * iwf
P1_adj = P1 * np.array([1.0, 1.0, 0.5])
MV1_split_only = (P1_adj * (shares0 * np.array([1, 1, 2]) * iwf)).sum()
ok(
    "the split alone leaves index market value at 12,200 (no divisor change)",
    close(MV1_split_only, 12200),
)
CMV = 19.0 * 30.0
Dc1_add = Dc0 + CMV / Lc1  # additive form, eq. (7)
Dc1_mult = Dc0 * (P1_adj * q1).sum() / MV1  # multiplicative form, eq. (6)
ok(
    "divisor 12.560656 by eq. (7) = eq. (6)",
    close(Dc1_add, Dc1_mult) and abs(Dc1_add - 12.560656) < 1e-6,
)
ok("level unchanged across the share issue", close((P1_adj * q1).sum() / Dc1_add, Lc1))
P2c = np.array([54.0, 20.0, 44.0])
MV2 = (P2c * q1).sum()
Lc2 = MV2 / Dc1_add
ok(
    "day 2 market value 13,120, level 1,044.531 (+2.7408%)",
    close(MV2, 13120) and abs(Lc2 - 1044.5315) < 1e-4 and abs(Lc2 / Lc1 - 1 - 0.027408) < 1e-6,
)
w1 = P1_adj * q1 / (P1_adj * q1).sum()
r2 = P2c / P1_adj - 1
ok(
    "day 2 return equals the post-action weights times returns",
    close((w1 * r2).sum(), Lc2 / Lc1 - 1),
)

print("== part 3: total return and net total return on day 2 (B goes ex-dividend 0.40)")
div = np.array([0.0, 0.40, 0.0])
idx_div_points = (div * q1).sum() / Dc1_add
ok("index dividend points = 0.40 x 330 / 12.560656 = 10.5090", abs(idx_div_points - 10.5090) < 1e-4)
dtr = (Lc2 + idx_div_points) / Lc1 - 1
ok("daily total return 3.7745% against a price return of 2.7408%", abs(dtr - 0.037745) < 1e-6)
TR1 = 1000.0 * (
    Lc1 / 1000.0
)  # assume TR and price indices start together at 1,000 on day 0, no dividend on day 1
TR2 = TR1 * (1 + dtr)
ok("TR index: 1,016.667 -> 1,055.040", abs(TR2 - 1055.0405) < 1e-3)
ok(
    "equivalent S&P form TR_t = TR_t-1 x (PR_t + dividend points) / PR_t-1",
    close(TR2, TR1 * (Lc2 + idx_div_points) / Lc1),
)
wht = 0.15
ntr = (Lc2 + idx_div_points * (1 - wht)) / Lc1 - 1
ok("net total return with 15% withholding: 3.6194%", abs(ntr - 0.036194) < 1e-6)
ok("ordering price < net total < total", Lc2 / Lc1 - 1 < ntr < dtr)

print("== part 4: equal weighting, drift and rebalancing")
# Equal-weight index of the same three stocks, base 1,000 on day 0, rebalanced after the close of day 1.
w_eq0 = np.ones(3) / 3
Le1 = 1000 * (1 + (w_eq0 * r1).sum())
ok(
    "equal-weight day 1 return 3.3333% (simple average)",
    close(Le1, 1000 * (1 + (0.10 - 0.05 + 0.05) / 3)),
)
w_drift = w_eq0 * (1 + r1) / (1 + (w_eq0 * r1).sum())
ok(
    "weights drift to 35.48, 30.65, 33.87%",
    np.allclose(np.round(w_drift, 4), [0.3548, 0.3065, 0.3387]),
)
turnover = np.abs(w_eq0 - w_drift).sum() / 2
ok(
    "one-way turnover to rebalance = half the sum of |weight changes| = 2.69%",
    abs(turnover - 0.026882) < 1e-6,
)
# S&P DJI: AWF_i = Z / (N x float-adjusted market value_i), so every adjusted market value equals Z/N.
fav = P1_adj * q1
Z = fav.sum()
awf = Z / (3 * fav)
ok(
    "AWFs make the adjusted market values equal and preserve the index market value",
    np.allclose(awf * fav, Z / 3) and close((awf * fav).sum(), Z),
)
Le2 = Le1 * (1 + (w_eq0 * r2).sum())
ok(
    "rebalanced equal-weight day 2 return 2.7356% (simple average), level 1,061.601",
    abs(r2.mean() - 0.027356) < 1e-6 and abs(Le2 - 1061.6013) < 1e-3,
)

print("== part 5: fixed-income index month (Bloomberg conventions)")
# Two bonds in the returns universe at the start of the month; par outstanding in millions; prices per 100 par.
par = np.array([500.0, 300.0])
clean0 = np.array([98.0, 102.5])
ai0 = np.array([1.00, 0.50])
clean1 = np.array([99.0, 101.8])
ai1 = np.array([1.40, 0.90])
coupon_paid = np.array([0.0, 0.0])
dirty0 = clean0 + ai0
price_ret = (clean1 - clean0) / dirty0
coupon_ret = (ai1 - ai0 + coupon_paid) / dirty0
bond_tr = price_ret + coupon_ret
mv0 = par * dirty0 / 100
wb = mv0 / mv0.sum()
idx_tr = (wb * bond_tr).sum()
ok(
    "bond 1: price 1.0101%, coupon 0.4040%, total 1.4141%",
    abs(price_ret[0] - 0.010101) < 1e-6
    and abs(coupon_ret[0] - 0.004040) < 1e-6
    and abs(bond_tr[0] - 0.014141) < 1e-6,
)
ok(
    "bond 2: price -0.6796%, coupon 0.3883%, total -0.2913%",
    abs(price_ret[1] + 0.006796) < 1e-6 and abs(bond_tr[1] + 0.002913) < 1e-6,
)
ok(
    "beginning market-value weights 61.6 / 38.4% (495 and 309 of 804); index total return 0.7587%",
    np.allclose(mv0, [495, 309]) and abs(idx_tr - 0.007587) < 1e-6,
)
# A new bond issued mid-month enters the projected universe but not the returns universe until month end:
# adding it would change the weights only from the next month, so the month's return is unchanged by construction.
dirty_end = clean1 + ai1
ok(
    "total return also equals the change in dirty value (no coupon paid)",
    np.allclose(bond_tr, (dirty_end - dirty0) / dirty0),
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
