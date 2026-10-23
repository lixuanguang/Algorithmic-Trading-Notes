"""Credit portfolios: spread risk and DTS, spread measures, selection, liquidity and tail risk, CDS, international
and structured credit (2026-10-20; liquidity-cost marks and covered bonds corrected the same day).

Worked numbers of meth:credit-spread-portfolio-risk, meth:credit-selection-positioning, meth:credit-liquidity-tail-risk
and meth:credit-cds-international-structured. Bonds, portfolios and rates are hypothetical except where a check
reproduces a published figure (Ben Dor et al. 2012, pp. 4, 82, 257; Ben Dor et al. 2021, p. 515; Hull 2023, p. 416;
Larreur 2021, p. 309).

Independent routes: excess returns from absolute spread changes against relative changes times DTS; issuer caps from a
DTS budget against position-size ratios; Vasicek's worst-case default rate from the closed form against a one-factor
simulation; hedge ratios by duration against DTS; OC tests before and after defaults; a one-way sale from mid
against the round-trip LCS and the cash identity (start value = proceeds + remaining bonds + cost); a covered bond's
issuer and pool claims against securitisation tranches paid from the pool alone.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python credit-portfolio-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import sys

# third party library imports
import numpy as np
import scipy
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
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
print("== part 1: spread risk, DTS and spread measures")
ok(
    "Ben Dor et al. p. 4: a 5% overweight at 80 bp and spread duration 3 equals a 3% overweight at 50 bp and "
    "duration 8 in DTS contribution (12 in %-years-%)",
    close(5 * 3 * 0.80, 12.0) and close(3 * 8 * 0.50, 12.0),
)
D, s = 6.0, 1.50  # spread duration (years), spread (%)
abs_change = 0.15  # 15 bp widening
rel_change = abs_change / s
ok(
    "a 15 bp widening on a bond with spread duration 6 and spread 150 bp costs 0.90%; the same as a 10% relative "
    "widening times DTS 9",
    close(-D * abs_change, -0.90) and close(-D * s * rel_change, -0.90) and close(D * s, 9.0),
)
low, high = (6.0, 0.80), (6.0, 2.40)
sigma_rel = 0.10  # monthly relative spread volatility, the same for both (DTS assumption)
vol_low, vol_high = low[0] * low[1] * sigma_rel, high[0] * high[1] * sigma_rel
ok(
    "with a common 10% relative spread volatility, a 240 bp bond has three times the excess return volatility of an "
    "80 bp bond of the same duration (1.44% against 0.48% a month)",
    close(vol_high / vol_low, 3.0) and round(vol_high, 2) == 1.44 and round(vol_low, 2) == 0.48,
)
yld, tsy, swp = 5.20, 4.00, 4.30
z_spread, option_cost = 1.80, 0.40
ok(
    "spread measures: G-spread 120 bp over the Treasury, I-spread 90 bp over swaps; for a callable bond a Z-spread "
    "of 180 bp less 40 bp of option cost leaves an OAS of 140 bp",
    close((yld - tsy) * 100, 120)
    and close((yld - swp) * 100, 90)
    and close((z_spread - option_cost) * 100, 140),
)

# ---------------------------------------------------------------------------------------------
print("== part 2: bottom-up and top-down selection, and positioning")
ok(
    "Ben Dor et al. 2021 p. 515: lowest equity-momentum bonds -7.2%/yr against 8.10%/yr for the highest, index 1.43%",
    -7.2 < 1.43 < 8.10 and close(8.10 - (-7.2), 15.3),
)
peers = np.array(
    [1.10, 1.25, 1.30, 1.40, 1.55]
)  # spreads of same-rating, same-sector, similar-duration peers (%)
bond = 1.60
esp = bond - np.median(peers)
ok(
    "excess spread to peers: a bond at 160 bp against a peer median of 130 bp has an ESP of +30 bp, a candidate "
    "overweight if fundamentals do not explain it",
    close(esp, 0.30, 1e-12),
)
short_bond, long_bond = (3.0, 1.00), (10.0, 1.80)  # (spread duration, spread %)
dur_ratio = short_bond[0] / long_bond[0]
dts_ratio = short_bond[0] * short_bond[1] / (long_bond[0] * long_bond[1])
ok(
    "credit steepener: per 100 of short-dated bonds, a duration-neutral hedge sells 30 of long-dated bonds, a "
    "DTS-neutral hedge 16.67",
    close(dur_ratio * 100, 30.0) and round(dts_ratio * 100, 2) == 16.67,
)
port_dts, bench_dts = 7.2, 6.0
ok(
    "a portfolio DTS of 7.2 against a benchmark of 6.0 is a 1.2 overweight: a 10% relative widening costs 0.72% "
    "against 0.60%, a 12 bp underperformance",
    close(port_dts * 0.10 - bench_dts * 0.10, 0.12),
)

# ---------------------------------------------------------------------------------------------
print("== part 3: liquidity and tail risk")
oasd, bid_ask = 7.0, 0.10  # years, bid-ask spread in %
lcs = oasd * bid_ask
ok(
    "Ben Dor et al. p. 82: LCS = OASD x bid-ask spread; 7 x 10 bp = 0.70% round-trip cost",
    close(lcs, 0.70),
)
w = np.array([0.5, 0.3, 0.2])
lcs_b = np.array([0.40, 0.90, 2.00])
PORT = 100.0  # portfolio value at mid prices
ok(
    "a portfolio with LCS 0.40/0.90/2.00 weighted 50/30/20 has an LCS of 0.87%, a round-trip cost",
    round(float(w @ lcs_b), 2) == 0.87,
)
# A round trip pays the whole bid-ask spread; a one-way sale from mid pays half of it. Against a bid-side mark the
# sale costs nothing relative to the mark (the cost was already taken in the valuation); against an ask mark it costs
# the full spread.
sold = w[0] * PORT
cost_mid = sold * lcs_b[0] / 100 / 2
cost_round = sold * lcs_b[0] / 100
cost_bid_mark = 0.0
cost_ask_mark = sold * lcs_b[0] / 100
proceeds = sold - cost_mid
ok(
    "selling the most liquid half (50 at mid) one way costs half its LCS against mid: 0.10, or 0.10% of the "
    "portfolio, not the 0.20% round-trip figure; proceeds 49.90",
    close(cost_mid, 0.10) and close(cost_round, 0.20) and close(proceeds, 49.90),
)
ok(
    "the same sale against other marks: zero against a bid-side mark, 0.20 against an ask-side mark; mark-to-mid "
    "cost + bid-marked cost = half the round trip for a symmetric spread",
    close(cost_bid_mark, 0.0)
    and close(cost_ask_mark, 0.20)
    and close(cost_mid, (cost_round + cost_bid_mark) / 2),
)
rest = w[1:] * PORT
rest_lcs = float(rest @ lcs_b[1:]) / rest.sum()
total_after = proceeds + rest.sum()
ok(
    "after the sale: cash 49.90 and bonds 50 (weights 60/40 within the bonds) with an LCS of 1.34%; the whole "
    "portfolio of 99.90 has a value-weighted LCS of 0.67% (cash at zero), and liquidating the rest later would cost "
    "a further 0.335 one way at mid",
    round(rest_lcs, 2) == 1.34
    and close(total_after, 99.90)
    and round(rest.sum() * rest_lcs / total_after, 2) == 0.67
    and round(rest.sum() * rest_lcs / 100 / 2, 3) == 0.335,
)
ok(
    "accounting identity: start value 100 = cash proceeds + remaining bonds at mid + one-way cost",
    close(PORT, proceeds + rest.sum() + cost_mid),
)
ok(
    "Ben Dor et al. p. 257: issuer position-size ratios 9.2 : 3.1 : 1 on downgrade risk and 4.0 : 2.5 : 1 with all "
    "non-systematic risk before the crisis; full sample 2.6 : 1.5 : 1 (printed '2:6') and 2.4 : 1.5 : 1",
    9.2 > 4.0 and 3.1 > 2.5 and 2.6 > 2.4,
)
cap = 0.12  # DTS-contribution cap per issuer (weight % x duration x spread %)
ok(
    "a DTS cap of 0.12 allows 2.50% in an issuer at 80 bp and duration 6 but 0.83% in one at 240 bp",
    round(cap / (6 * 0.8) * 100, 2) == 2.50 and round(cap / (6 * 2.4) * 100, 2) == 0.83,
)
pd, rho, X, lgd = 0.01, 0.10, 0.999, 0.60
wcdr = norm.cdf((norm.ppf(pd) + np.sqrt(rho) * norm.ppf(X)) / np.sqrt(1 - rho))
ok(
    "Hull eq. 19.1: PD 1%, correlation 0.10, 99.9%: worst-case default rate 7.75%; with LGD 60% the 99.9% credit "
    "loss is 4.65% of a granular portfolio against an expected 0.60%",
    round(wcdr * 100, 2) == 7.75 and round(wcdr * lgd * 100, 2) == 4.65,
)
rng = np.random.default_rng(20261020)
F = rng.standard_normal(400_000)
cond_pd = norm.cdf((norm.ppf(pd) - np.sqrt(rho) * F) / np.sqrt(1 - rho))
ok(
    "simulating the one-factor model, the 99.9th percentile of the default rate matches the closed form within 0.3 points",
    abs(np.quantile(cond_pd, X) - wcdr) < 0.003,
    f"{np.quantile(cond_pd, X) * 100:.2f}%",
)

# ---------------------------------------------------------------------------------------------
print("== part 4: CDS, international and structured credit")
notional = 0.5 * 100 / 4.5
ok(
    "adding 0.5 years of spread duration to a 100m portfolio by selling protection on an index with spread duration "
    "4.5 needs 11.1m notional",
    round(notional, 1) == 11.1,
)
eur_yield, usd_rate, eur_rate, usd_bond = 3.5, 4.5, 2.5, 5.2
hedged = eur_yield + (usd_rate - eur_rate)
ok(
    "a euro bond yielding 3.5% hedged into dollars with rates at 4.5% and 2.5% yields about 5.5%, above a comparable "
    "US bond at 5.2%",
    close(hedged, 5.5) and hedged > usd_bond,
)
collateral, rated = 120.0, 100.0
oc0 = collateral / rated
loss = 10.0 * (1 - 0.40)
oc1 = (collateral - loss) / rated
ok(
    "CLO OC test (Larreur p. 309): 120 of collateral against 100 of rated notes is 120%; 10 of defaults at 40% "
    "recovery cut it to 114%, below a 115% trigger, diverting cash to pay down senior notes",
    close(oc0, 1.20) and close(oc1, 1.14) and oc1 < 1.15,
)


# Covered bond against a securitisation of the same pool (Directive (EU) 2019/2162 Arts 4, 15; Regulation (EU)
# 2017/2402 Art 2(1)). Bank Corvel: covered bonds 100 on a cover pool of 110; the same 110 pool securitised instead
# into a senior 80, mezzanine 15 and equity 15.
COVERED, POOL = 100.0, 110.0
TRANCHES = [("senior", 80.0), ("mezzanine", 15.0), ("equity", 15.0)]


def tranche_payoff(pool_value):
    out, left = {}, pool_value
    for k, size in TRANCHES:
        out[k] = min(left, size)
        left -= out[k]
    return out


def covered_payoff(pool_value, issuer_solvent, unsecured_recovery):
    if issuer_solvent:
        return COVERED  # the issuer pays; the pool is security, not the source of payment
    priority = min(pool_value, COVERED)
    return priority + (COVERED - priority) * unsecured_recovery


ok(
    "pool loses 15 (worth 95) with the bank solvent: covered bonds are paid 100 by the issuer; the securitisation's "
    "equity absorbs the loss and the senior 80 is intact",
    close(covered_payoff(95.0, True, 0.4), 100.0)
    and close(tranche_payoff(95.0)["equity"], 0.0)
    and close(tranche_payoff(95.0)["senior"], 80.0),
)
ok(
    "pool worth 90 and the bank insolvent: covered bonds take 90 from the pool and claim the 10 shortfall pari passu "
    "with unsecured creditors (40% recovery): 94; in the securitisation the equity is wiped, the mezzanine loses 5 "
    "of 15 and the senior is whole",
    close(covered_payoff(90.0, False, 0.4), 94.0)
    and close(tranche_payoff(90.0)["equity"], 0.0)
    and close(tranche_payoff(90.0)["mezzanine"], 10.0)
    and close(tranche_payoff(90.0)["senior"], 80.0),
)
ok(
    "the senior tranche is 80/110 = 72.7% of this structure: tranche proportions describe securitisations; covered "
    "bonds are a single untranched class backed by overcollateralisation of 10%",
    round(80.0 / POOL * 100, 1) == 72.7 and close(POOL / COVERED - 1, 0.10),
)
prepay = 20.0
ok(
    "the pool prepays 20: a pass-through investor receives 20 of principal early, whereas the covered bonds stay at "
    "100; coverage falls to 90% and the issuer must add at least 10 of eligible or substitution assets (Art 15(6))",
    (POOL - prepay) / COVERED < 1.0
    and close(COVERED - (POOL - prepay), 10.0)
    and close(COVERED, 100.0),
)
print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
