"""Institutional portfolios: pension risk, IPS and portfolio evaluation, a sovereign fund risk case, endowment liquidity
and ESG constraints (2026-10-20).

Worked numbers of the entries in compendium/portfolio-construction-risk/institutional-portfolios.tex. Every
institution is hypothetical (Harlow Industrial's DB plan, the Elmsworth University endowment, the Calder Foundation,
Bank Ardent and the Vardø Fund, a commodity sovereign fund), except the published benchmark parameters of Norway's
Government Pension Fund Global quoted in the entries (NBIM web pages, 2026).

Independent routes: surplus volatility from the covariance matrix against a Monte Carlo of asset and liability
returns; hedge ratios from dollar durations; deficit amortisation against an annuity schedule; spending rules
simulated year by year against closed forms; the equity duration gap against a full repricing of assets and
liabilities; the GPFG rebalancing trigger by rule; stress-test liquidity coverage summed source by source; the
denominator effect by recomputing weights; exclusion tracking error against a simulated active return.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python institutional-checks.py   (numpy). Exits 1 on failure.
"""

# standard library imports
import math
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


def annuity(r, n):
    return (1 - (1 + r) ** -n) / r


rng = np.random.default_rng(20261020)

# ---------------------------------------------------------------------------------------------
print(
    "== part 1: Harlow Industrial's defined benefit plan - funded status, surplus risk and the sponsor"
)
A, L = 8.0, 9.0  # USD bn assets and liabilities (PBO)
D_L, D_B, D_LONG = 12.0, 6.0, 15.0
VOL_EQ, VOL_RATE = 0.16, 0.01  # equity volatility; annual volatility of the discount rate (100 bp)


def surplus_vol(w_eq, d_bond):
    """Assets: w_eq equity, rest bonds of duration d_bond; liability duration D_L; one rate factor + equity."""
    rho_eq_rate = -0.2  # equity returns and rate changes; rates up -> both bonds and equities lower
    w_b = 1 - w_eq
    # dollar exposures to (equity return, rate change)
    a_eq = A * w_eq
    a_rate = -A * w_b * d_bond
    l_rate = -L * D_L
    cov = np.array(
        [
            [VOL_EQ**2, rho_eq_rate * VOL_EQ * VOL_RATE],
            [rho_eq_rate * VOL_EQ * VOL_RATE, VOL_RATE**2],
        ]
    )
    x = np.array([a_eq, a_rate - l_rate])  # surplus = assets - liabilities
    return math.sqrt(x @ cov @ x)


s_now = surplus_vol(0.55, D_B)
s_ldi = surplus_vol(0.30, D_LONG)
ok(
    "funded ratio 8/9 = 88.9%; hedge ratio (asset dollar duration over liability dollar duration) 20% with 55/45 "
    "and 6-year bonds, 78% with 30/70 and 15-year bonds",
    round(A / L * 100, 1) == 88.9
    and round(0.45 * A * D_B / (L * D_L) * 100) == 20
    and round(0.70 * A * D_LONG / (L * D_L) * 100) == 78,
)
ok(
    "surplus volatility: 1.00bn a year (12.5% of assets) as invested, against 0.41bn with the liability-driven mix",
    round(s_now, 2) == 1.00 and round(s_ldi, 2) == 0.41,
    f"{s_now:.3f}, {s_ldi:.3f}",
)
z = rng.multivariate_normal(
    [0, 0],
    [[VOL_EQ**2, -0.2 * VOL_EQ * VOL_RATE], [-0.2 * VOL_EQ * VOL_RATE, VOL_RATE**2]],
    size=400_000,
)
sim = A * 0.55 * z[:, 0] - A * 0.45 * D_B * z[:, 1] + L * D_L * z[:, 1]
ok(
    "a Monte Carlo of equity and rate shocks reproduces the surplus volatility within 1%",
    abs(sim.std() / s_now - 1) < 0.01,
)
MCAP = 6.0
sar = 1.645 * s_now
ok(
    "the 95% one-year surplus at risk (1.64bn) is 27% of the sponsor's 6bn market capitalisation: plan risk is "
    "material to shareholders",
    round(sar, 2) == 1.64 and round(sar / MCAP * 100) == 27,
)
deficit = L - A
pay = deficit / annuity(0.05, 7)
ok(
    "closing the 1.0bn deficit over seven years at 5% needs 0.173bn a year, 14% of the sponsor's 1.2bn EBITDA",
    round(pay, 3) == 0.173 and round(pay / 1.2 * 100) == 14,
)

# ---------------------------------------------------------------------------------------------
print("== part 2: spending rules, a foundation's payout and bank and insurer balance sheets")
MV0, SPEND_RATE, INFL = 2_000.0, 0.05, 0.025  # Elmsworth endowment, USD m
returns = [0.08, 0.08, -0.25, 0.10, 0.08]
mv_s, mv_p = MV0, MV0
sp_s = sp_p = SPEND_RATE * MV0
spend_s, spend_p = [], []
for rr in returns:
    sp_p = SPEND_RATE * mv_p
    sp_s = 0.7 * sp_s * (1 + INFL) + 0.3 * SPEND_RATE * mv_s
    spend_p.append(sp_p)
    spend_s.append(sp_s)
    mv_p = (mv_p - sp_p) * (1 + rr)
    mv_s = (mv_s - sp_s) * (1 + rr)
ok(
    "after two 8% years, a -25% year: pure 5%-of-value spending falls from 105.3m to 75.0m the next year (-29%); a "
    "70/30 smoothed rule (70% last year's spending grown with inflation, 30% of 5% of value) falls from 106.0m to "
    "98.5m (-7%)",
    round(spend_p[3], 1) == 75.0
    and round(spend_p[2], 1) == 105.3
    and round(spend_s[2], 1) == 106.0
    and round(spend_s[3], 1) == 98.5,
    f"{[round(x, 1) for x in spend_p]} vs {[round(x, 1) for x in spend_s]}",
)
mv_track = MV0
sp_track = SPEND_RATE * MV0
rates = []
for rr in returns:
    sp_track = 0.7 * sp_track * (1 + INFL) + 0.3 * SPEND_RATE * mv_track
    rates.append(sp_track / mv_track)
    mv_track = (mv_track - sp_track) * (1 + rr)
ok(
    "UPMIFA: spending above 7% of value creates a rebuttable presumption of imprudence; the smoothed rule's rate "
    "peaks at 6.6% of the post-crash value (98.5m on 1,497m), below it",
    round(max(rates) * 100, 1) == 6.6 and max(rates) < 0.07,
)
req_found = (1 + 0.05) * (1 + INFL) * (1 + 0.005) - 1
real_erosion = (1.065 / ((1 + 0.05 + 0.005) * (1 + INFL))) ** 20
ok(
    "the Calder Foundation must pay out 5% (s. 4942(e)); with 2.5% inflation and 0.5% costs it needs about 8.2% "
    "nominal to keep real value; at 6.5% expected its real value falls to 74% in 20 years",
    round(req_found * 100, 1) == 8.2 and round(real_erosion * 100) == 74,
)
A_B, L_B, DA, DL_B, y = 100.0, 90.0, 4.0, 1.5, 0.04
dgap = DA - (L_B / A_B) * DL_B
d_equity = -dgap * A_B * 0.01 / (1 + y)
reprice_a = A_B * (1 - DA * 0.01 / (1 + y))
reprice_l = L_B * (1 - DL_B * 0.01 / (1 + y))
ok(
    "Bank Ardent: assets 100 (duration 4), liabilities 90 (duration 1.5): duration gap 2.65; a 1-point rise in "
    "rates cuts equity by 2.55, a quarter of its 10 of equity; repricing assets and liabilities agrees",
    close(dgap, 2.65)
    and round(d_equity, 2) == -2.55
    and close(reprice_a - reprice_l - 10.0, d_equity, 1e-12),
)
A_I, L_I, DA_I, DL_I = 120.0, 100.0, 7.0, 10.0
ok(
    "an insurer with assets 120 (duration 7) and liabilities 100 (duration 10) gains surplus when rates rise: dollar "
    "duration 840 against 1,000; matching needs asset duration 8.33",
    close(A_I * DA_I, 840.0) and close(L_I * DL_I, 1000.0) and round(L_I * DL_I / A_I, 2) == 8.33,
)

# ---------------------------------------------------------------------------------------------
print("== part 3: sovereign funds - the GPFG rules and the Vardø Fund's risks")
ok(
    "GPFG (NBIM, 30 June 2026): strategic 70/30; actual benchmark equity 72.93% is 2.93 points above, beyond the "
    "2-point trigger, so the benchmark is rebalanced at month-end; a 1.25% tracking-error limit means the "
    "difference should exceed 1.25 points in about one year in three",
    abs(72.93 - 70.0) > 2.0 and round(2 * (1 - 0.8413), 2) == 0.32,
)
fund, oil_rev = 100.0, 8.0  # Vardø Fund USD bn; annual oil inflow
w = {"public_eq": 0.60, "bonds": 0.20, "direct_ra": 0.12, "domestic": 0.08}
shock = {"public_eq": -0.30, "bonds": 0.03, "direct_ra": -0.10, "domestic": -0.40}
loss = sum(fund * w[k] * shock[k] for k in w)
budget_draw = 6.0
ok(
    "a joint oil and equity crash: the portfolio falls 21.8bn (-22%); oil inflows of 8bn stop and the budget draws "
    "6bn; liquid bonds (20.6bn after the shock) cover more than three years of withdrawals",
    round(loss, 1) == -21.8
    and round(fund * w["bonds"] * 1.03, 1) == 20.6
    and fund * w["bonds"] * 1.03 / budget_draw > 3,
)
ok(
    "the domestic strategic stakes (8%) lose 40% in the crash: 3.2bn, 15% of the fund's loss from 8% of its assets: "
    "concentration that also ties the fund to the same economy as its oil revenue",
    round(fund * w["domestic"] * 0.40, 1) == 3.2 and round(3.2 / 21.8 * 100) == 15,
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 4: Elmsworth endowment - liquidity stress, the denominator effect and commitment pacing"
)
nav = {"cash": 100.0, "bonds": 200.0, "public_eq": 600.0, "hedge": 400.0, "private": 700.0}
unfunded = 500.0
s_ret = {"cash": 0.0, "bonds": 0.04, "public_eq": -0.35, "hedge": -0.10, "private": -0.10}
after = {k: v * (1 + s_ret[k]) for k, v in nav.items()}
total_after = sum(after.values())
calls = 0.25 * unfunded
dists = 0.02 * after["private"]
spend = 0.05 * sum(nav.values())
needs = calls + spend
liquid = after["cash"] + after["bonds"] + 0.25 * after["hedge"]
ok(
    "stress: public equity -35%, hedge funds -10%, private NAV only -10% because appraisals lag; total falls from "
    "2,000 to 1,688",
    round(total_after) == 1688,
)
ok(
    "one-year needs: capital calls 125 (25% of 500 unfunded) + spending 100 = 225, less distributions of 13 (2% of "
    "NAV); liquid sources: cash 100 + bonds 208 + a quarter of hedge funds 90 = 398: coverage 1.87 times net needs",
    close(needs, 225.0)
    and round(dists, 1) == 12.6
    and round(liquid) == 398
    and round(liquid / (needs - dists), 2) == 1.87,
)
w_priv_before = nav["private"] / sum(nav.values())
w_priv_after = after["private"] / total_after
ok(
    "denominator effect: private assets rise from 35.0% to 37.3% of the portfolio while their NAV falls, because "
    "appraisals lag the 35% fall in public equity; counting the 500 unfunded commitments the exposure is 67%; a 35% "
    "cap would block new commitments",
    round(w_priv_before * 100, 1) == 35.0
    and round(w_priv_after * 100, 1) == 37.3
    and round((after["private"] + unfunded) / total_after * 100) == 67,
)
ok(
    "liquidity policy: keep liquid sources of at least two years of spending plus a stressed year of calls "
    "(2 x 100 + 125 = 325); Elmsworth's 398 passes, but after drawing 225 it has 173 and must rebuild before new "
    "commitments",
    close(2 * spend + calls, 325.0) and liquid >= 325 and round(liquid - needs) == 173,
)
prem_needed = 0.02
ok(
    "illiquidity premium: to justify 10 years of lock-up an investor demanding 2% a year more than public equity "
    "needs a private multiple 1.22 times the public one (1.02^10)",
    round((1 + prem_needed) ** 10, 2) == 1.22,
)

# ---------------------------------------------------------------------------------------------
print("== part 5: ESG constraints in a long-term portfolio")
w_ex, sigma_rel = 0.015, 0.25
te_formula = w_ex * sigma_rel
r_sector = rng.normal(0, sigma_rel, 200_000)
te_sim = (w_ex * r_sector).std()
ok(
    "excluding a sector with 1.5% benchmark weight whose return differs from the rest of the market with 25% "
    "volatility adds about 0.375% of tracking error; a simulation agrees",
    round(te_formula * 100, 3) == 0.375 and abs(te_sim / te_formula - 1) < 0.01,
)
ok(
    "four sectors excluded together (1.5% + 1.2% + 2.0% + 0.8% = 5.5%) with independent 25% relative volatility give "
    "tracking error of 0.72%, within a 1.25% budget",
    round(math.sqrt(sum((x * 0.25) ** 2 for x in (0.015, 0.012, 0.020, 0.008))) * 100, 2) == 0.72,
)
w_h = np.array([0.40, 0.35, 0.25])
ci = np.array([20.0, 150.0, 600.0])  # tonnes CO2e per USD m revenue
ok(
    "weighted average carbon intensity of three holdings (40/35/25%, intensities 20/150/600): 210.5 t per USD m of "
    "revenue; moving 10 points from the most to the least intensive cuts it to 152.5",
    close(float(w_h @ ci), 210.5) and close(float(np.array([0.50, 0.35, 0.15]) @ ci), 152.5),
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
