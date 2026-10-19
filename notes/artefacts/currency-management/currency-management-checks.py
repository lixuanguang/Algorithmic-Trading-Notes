"""Currency management (2026-10-19): the worked numbers of meth:currency-portfolio-effects,
meth:currency-hedging-programme, meth:active-currency-strategies and meth:currency-hedge-cost-reduction.

Reproduced from Portfolio Management in Practice, Volume 1 (CFA Institute Investment Series, 2020), chap. 8: the
domestic-currency return (1 + 10%)(1 + 5%) - 1 = 15.5% and the INR portfolio return of 12.4% (eqs. 1-2, pp. 378-380);
the variance approximation (eq. 5, p. 380). Campbell, Serfaty-de Medeiros and Viceira (NBER WP 13088, revised 2009):
risk-minimising currency positions are close to a full hedge for bonds, while currencies that move against equities
are worth holding unhedged in equity portfolios. Original: domestic-currency volatility of hedged and unhedged equity
and bond holdings and their minimum-variance hedge ratios; adjusting a hedge ratio when the asset value changes,
with the settlement of the maturing forward and the FX swap that rolls it; roll yield from forward points; protective
puts, risk reversals, put spreads and seagulls priced with Garman-Kohlhagen; a cross hedge and its residual risk;
a regression-based minimum-variance hedge on simulated data; non-deliverable forward settlement; a carry position
and a volatility trade; and a hedging-cost budget.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python currency-management-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: currency effects on return and risk")
ok(
    "PMiP eq. (1): a 10% foreign-currency return with a 5% rise in the foreign currency gives 15.5% (15% to first"
    " order)",
    close(1.10 * 1.05 - 1, 0.155, 1e-12),
)
r_dc = 0.80 * (50.70 / 43.80) * (85.78 / 84.12) + 0.20 * (12.17 / 14.08) * (67.81 / 65.36) - 1
ok(
    "PMiP eq. (2), Indian investor: 80% in GBP assets (43.80m to 50.70m, INR/GBP 84.12 to 85.78) and 20% in EUR assets"
    " (14.08m to 12.17m, INR/EUR 65.36 to 67.81): domestic-currency return 12.4%",
    round(r_dc, 3) == 0.124,
    f"{r_dc:.4%}",
)


def dc_vol(s_fc, s_fx, rho, h=0.0):
    """Approximate domestic-currency volatility with hedge ratio h (fraction of currency exposure hedged)."""
    e = 1 - h
    return math.sqrt(s_fc**2 + (e * s_fx) ** 2 + 2 * e * s_fc * s_fx * rho)


def mv_hedge(s_fc, s_fx, rho):
    return 1 + rho * s_fc / s_fx


eq = (0.16, 0.10, -0.30)
bd = (0.04, 0.10, -0.05)
ok(
    "PMiP eq. (5): unhedged equities (16% local volatility, 10% currency volatility, correlation -0.3) have 16.1%"
    " domestic volatility, barely above local; unhedged bonds (4%, 10%, -0.05) have 10.6%, dominated by currency",
    abs(dc_vol(*eq) - 0.1611) < 1e-3 and abs(dc_vol(*bd) - 0.1058) < 1e-3,
)
h_eq, h_bd = mv_hedge(*eq), mv_hedge(*bd)
ok(
    "minimum-variance hedge ratios: 52% for the equities (the currency partly hedges the equity risk) and 98% for the"
    " bonds, close to a full hedge, as Campbell et al. find for bond investors",
    abs(h_eq - 0.52) < 1e-12 and abs(h_bd - 0.98) < 1e-12 and dc_vol(*eq, h_eq) < dc_vol(*eq, 1.0),
    f"equity vol at h* {dc_vol(*eq, h_eq):.4f}, fully hedged {dc_vol(*eq, 1.0):.4f}",
)

print("== part 2: hedge ratios with forwards and FX swaps, and roll yield")
notional_old, value_now = 8_000_000, 8_500_000  # EUR exposure hedged by selling EUR forward
f_old, s_now, fwd_pts_1m = 1.1000, 1.0850, 12.0 / 10_000  # USD per EUR
settle = (f_old - s_now) * notional_old
f_new = s_now + fwd_pts_1m
ok(
    "rolling a hedge: the 8m EUR forward sold at 1.1000 settles against spot 1.0850 for a USD 120,000 gain; the FX swap"
    " buys 8m EUR spot and sells 8.5m EUR one month forward at 1.0862, lifting the hedge ratio back to 100% of the"
    " asset now worth 8.5m",
    abs(settle - 120_000) < 1e-6
    and close(f_new, 1.0862, 1e-12)
    and close(8_500_000 / value_now, 1.0),
)
fp_prem = (1.0862 - 1.0850) / 1.0850
ok(
    "roll yield: selling EUR at a forward premium of 12 points earns about 0.11% a month (1.3% a year) as the forward"
    " rolls down to spot, all else equal; buying at a premium would cost the same",
    abs(fp_prem - 0.0011060) < 1e-6 and abs(fp_prem * 12 - 0.01327) < 1e-4,
)
hedge_cost_annual, vol_cut = 0.015, dc_vol(*bd) - dc_vol(*bd, 1.0)
ok(
    "a hedging budget: if the investor's currency trades at a 1.5%-a-year forward premium against it (negative roll),"
    " fully hedging bonds costs 1.5% a year for a 6.6-point cut in volatility; for equities the cut is only 0.1"
    " point, so the cost is harder to justify",
    abs(vol_cut - 0.0658) < 1e-3 and abs(dc_vol(*eq) - dc_vol(*eq, 1.0) - 0.0011) < 1e-3,
)

print("== part 3: options to reduce hedging costs")


def gk(s, k, t, rd, rf, vol, kind):
    d1 = (math.log(s / k) + (rd - rf + 0.5 * vol**2) * t) / (vol * math.sqrt(t))
    d2 = d1 - vol * math.sqrt(t)
    if kind == "c":
        return s * math.exp(-rf * t) * norm.cdf(d1) - k * math.exp(-rd * t) * norm.cdf(d2)
    return k * math.exp(-rd * t) * norm.cdf(-d2) - s * math.exp(-rf * t) * norm.cdf(-d1)


S0, T, RD, RF, VOL = 1.0850, 0.25, 0.043, 0.025, 0.08  # USD-based investor long EUR assets
put_atm = gk(S0, S0, T, RD, RF, VOL, "p")
put_otm = gk(S0, 1.05, T, RD, RF, VOL, "p")
call_k = next(
    k / 10_000 for k in range(10_850, 12_500) if gk(S0, k / 10_000, T, RD, RF, VOL, "c") <= put_otm
)
put_low = gk(S0, 1.01, T, RD, RF, VOL, "p")
ok(
    "protective puts on EUR (8% volatility, 3 months): at the money 1.37% of notional, 3.2% out of the money (1.05)"
    " 0.37%: cheaper, with the first 3% of a fall unprotected",
    abs(put_atm / S0 - 0.0137) < 5e-5 and abs(put_otm / S0 - 0.0037) < 5e-5,
    f"ATM {put_atm / S0:.4%}, OTM {put_otm / S0:.4%}",
)
ok(
    "risk reversal (collar): selling a 1.1323 call pays for the 1.05 put, a zero-premium hedge that gives up upside"
    " above 1.1323",
    abs(call_k - 1.1323) < 0.0002 and gk(S0, call_k, T, RD, RF, VOL, "c") <= put_otm,
    f"call strike {call_k:.4f}",
)
seagull_cost = put_otm - put_low - gk(S0, call_k, T, RD, RF, VOL, "c")
ok(
    "put spread and seagull: selling a 1.01 put cuts the 1.05 put's cost by about a tenth; adding the short call makes"
    " the package net-premium-receiving, but losses below 1.01 return in full",
    put_low < put_otm and abs(put_low / put_otm - 0.115) < 0.01 and seagull_cost < 0,
    f"put spread cost {put_otm - put_low:.5f}, seagull {seagull_cost:.5f}",
)

print(
    "== part 4: multiple currencies, cross hedges, minimum-variance hedges, basis risk, emerging markets"
)
s_nzd, s_aud, rho_cross = 0.11, 0.10, 0.85
h_cross = rho_cross * s_nzd / s_aud
resid = s_nzd * math.sqrt(1 - rho_cross**2)
ok(
    "cross hedge: hedging NZD exposure with AUD forwards (correlation 0.85) uses 0.935 AUD per NZD and leaves 5.8%"
    " residual volatility out of 11%: basis risk remains",
    abs(h_cross - 0.935) < 1e-12 and abs(resid - 0.05795) < 1e-4,
)
rng = np.random.default_rng(20261019)
n = 120
r_fx = rng.normal(0, 0.03, n)
r_fc = rng.normal(0.006, 0.04, n) - 0.4 * r_fx
r_dc = (1 + r_fc) * (1 + r_fx) - 1
beta = np.polyfit(r_fx, r_dc, 1)[0]
grid = np.linspace(0, 1.5, 301)
best = grid[np.argmin([np.var(r_dc - h * r_fx) for h in grid])]
ok(
    "minimum-variance hedge by regression: regressing monthly domestic-currency returns on currency returns gives a"
    " slope near 0.6 (the currency's own effect less the -0.4 asset-currency link); a grid search on the hedged"
    " variance picks the same ratio",
    abs(beta - best) < 0.01 and 0.45 < beta < 0.75,
    f"beta {beta:.3f}, grid {best:.3f}",
)
ndf_rate, fixing, notional_usd = 83.50, 85.00, 10_000_000
settle_usd = notional_usd * (ndf_rate - fixing) / fixing
ok(
    "non-deliverable forward: an investor sold USD 10m against INR at 83.50; at a fixing of 85.00 the contract settles"
    " net in dollars, a payment of USD 176,471 by the investor (no rupees change hands)",
    abs(settle_usd + 176_470.6) < 0.1,
)

print("== part 5: active currency strategies")
carry_pnl = (1 + 0.105) * (1 - 0.04) - (1 + 0.043)
ok(
    "carry: funding in USD at 4.3% and investing in a 10.5% EM currency earns 1.78% even if the currency falls 4%; a"
    " 12% crash turns it into a loss of 7.06%",
    abs(carry_pnl - 0.0178) < 1e-4 and abs((1 + 0.105) * 0.88 - 1.043 + 0.0706) < 1e-4,
)
vega_pnl = 0.5 * (0.12**2 - 0.08**2) * 0.25 * 100
ok(
    "volatility trading: a delta-hedged long option position earns roughly half gamma times the gap between realised"
    " and implied variance; realised 12% against 8% implied over three months is positive (here 0.1 per 100 of"
    " dollar-gamma); realised below implied loses",
    vega_pnl > 0 and 0.5 * (0.06**2 - 0.08**2) * 0.25 * 100 < 0,
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
