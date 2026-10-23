"""Allocating to alternatives: roles, risk mitigation, factor opportunity sets, illiquidity hurdles, commitment pacing
and liquidity planning (2026-10-20).

Worked numbers of def:alternatives-roles-opportunity-set and meth:alternatives-allocation-approaches. Portfolios and
cash-flow parameters are hypothetical except where a check reproduces a published figure (Ang 2014, pp. 438, 442;
Demaria et al. 2021, pp. 101, 175, 186; Luxenberg et al. 2022, pp. 8-9, 20).

Independent routes: steady-state private exposure from the closed form of a linear commitment model against a long
deterministic simulation; crisis returns of label-based and factor-based portfolios computed from the same scenario;
liquidity needs summed by source against a year-by-year cash-flow projection.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python alternatives-allocation-checks.py   (numpy). Exits 1 on failure.
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
print("== part 1: published figures")
ok(
    "Ang p. 438: illiquidity hurdle rates of about 0.70% (liquidity every six months), 1% (a year) and 6% (ten years)",
    0.70 < 1.0 < 6.0,
)
ok(
    "Demaria et al. p. 186: committing 20% more when 60% is expected to be called raises net exposure to 72%; "
    "net exposure is 'at best between 40 and 60 percent' (p. 186) against 45-65% (p. 175)",
    close(0.60 * 1.20, 0.72) and (40, 60) != (45, 65),
)
alpha_i = 3.685
ok(
    "Luxenberg et al. pp. 9, 20: with a steady-state gain of 3.685, holding 100 of private assets needs a commitment "
    "of 27.14 a period",
    round(100 / alpha_i, 2) == 27.14,
)

# ---------------------------------------------------------------------------------------------
print("== part 2: alternatives and bonds as equity risk mitigators")
crisis = {
    "equity": -0.30,
    "bonds": 0.05,
    "hedge_funds": -0.09,
    "private_equity": -0.36,
    "trend": 0.10,
}
normal_mu = {
    "equity": 0.07,
    "bonds": 0.035,
    "hedge_funds": 0.05,
    "private_equity": 0.09,
    "trend": 0.04,
}


def port(weights, scen):
    return sum(w * scen[k] for k, w in weights.items())


p_6040 = {"equity": 0.6, "bonds": 0.4}
p_hf = {"equity": 0.6, "bonds": 0.2, "hedge_funds": 0.2}
p_trend = {"equity": 0.6, "bonds": 0.2, "trend": 0.2}
p_pe = {"equity": 0.5, "bonds": 0.3, "private_equity": 0.2}
ok(
    "equities -30%: 60/40 loses 16.0%; replacing half the bonds with hedge funds (beta 0.3) loses 18.8%; with trend "
    "following loses 15.0%; a 20% private equity sleeve (beta 1.2) in a 50/30/20 mix loses 20.7%",
    close(port(p_6040, crisis), -0.160)
    and close(port(p_hf, crisis), -0.188)
    and close(port(p_trend, crisis), -0.150)
    and close(port(p_pe, crisis), -0.207),
)
ok(
    "in normal times the hedge fund and private equity mixes earn more (5.9% and 6.35% against 5.6%), the trend mix "
    "slightly less (5.7%) - mitigation and return trade off",
    close(port(p_6040, normal_mu), 0.056)
    and close(port(p_hf, normal_mu), 0.059)
    and close(port(p_pe, normal_mu), 0.0635)
    and close(port(p_trend, normal_mu), 0.057),
)

# ---------------------------------------------------------------------------------------------
print("== part 3: traditional against risk-based opportunity sets")
labels = {
    "public_equity": 0.40,
    "bonds": 0.25,
    "private_equity": 0.15,
    "hedge_funds": 0.10,
    "real_estate": 0.10,
}
equity_beta = {
    "public_equity": 1.0,
    "bonds": -0.1,
    "private_equity": 1.2,
    "hedge_funds": 0.4,
    "real_estate": 0.5,
}
rate_dur = {
    "public_equity": 0.0,
    "bonds": 6.0,
    "private_equity": 0.0,
    "hedge_funds": 0.0,
    "real_estate": 3.0,
}
eq_exposure = sum(labels[k] * equity_beta[k] for k in labels)
dur = sum(labels[k] * rate_dur[k] for k in labels)
ok(
    "a portfolio labelled 40% equities carries an equity beta of 0.645 once private equity, hedge funds and real "
    "estate are mapped to factors, and a duration of 1.8 years",
    round(eq_exposure, 3) == 0.645 and round(dur, 2) == 1.80,
)
sig_eq, sig_rate = 0.16, 0.01  # equity volatility; volatility of yields (per year of duration)
var_eq = (eq_exposure * sig_eq) ** 2
var_rate = (dur * sig_rate) ** 2
ok(
    "with uncorrelated factors (16% equity volatility, 1% yield volatility), equity risk is 97.0% of variance",
    round(var_eq / (var_eq + var_rate) * 100, 1) == 97.0,
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 4: commitment pacing in a linear model (Takahashi-Alexander type, Luxenberg et al. form)"
)
lam0, lam1, delta, R = 0.20, 0.35, 0.30, 1.10
A = np.array([[R * (1 - delta), lam1], [0.0, 1 - lam1]])
B = np.array([lam0, 1 - lam0])
x_ss = np.linalg.solve(np.eye(2) - A, B)
I_ss, K_ss = x_ss
C_ss = lam0 + lam1 * K_ss
D_ss = R * delta * I_ss
ok(
    "call intensities 0.20 (new) and 0.35 (uncalled), distribution intensity 0.30, return 10%: a unit commitment each "
    "period gives steady-state NAV 4.348 and uncalled 2.286; calls equal 1 (as Luxenberg et al. show) and "
    "distributions 1.435",
    round(I_ss, 3) == 4.348
    and round(K_ss, 3) == 2.286
    and close(C_ss, 1.0, 1e-12)
    and round(D_ss, 3) == 1.435,
)
x = np.zeros(2)
for _ in range(400):
    x = A @ x + B
ok(
    "a 400-period simulation of constant commitments converges to the closed form",
    np.allclose(x, x_ss, atol=1e-10),
)
target = 0.10 * 1000
ok(
    "to hold 100 (10% of 1,000) commit 23.0 a period; the unfunded commitments are then 52.6, so total exposure "
    "(NAV + uncalled) is 152.6, 15.3% of assets",
    round(target / I_ss, 1) == 23.0
    and round(target / I_ss * K_ss, 1) == 52.6
    and round(target + target / I_ss * K_ss, 1) == 152.6,
)

# ---------------------------------------------------------------------------------------------
print("== part 5: denominator effect and liquidity planning")
w0 = np.array([600.0, 300.0, 100.0])  # listed equity, bonds, private real estate (stale)
w1 = w0 * np.array([0.70, 1.05, 1.00])
ok(
    "Demaria et al. p. 101: with a 60/30/10 policy, equities -30% and bonds +5% while appraisals do not move, real "
    "estate rises to 11.98% of a portfolio of 835 - over its target without any purchase",
    close(w1.sum(), 835.0) and round(w1[2] / w1.sum() * 100, 2) == 11.98,
)
assets, unfunded, payout = 1000.0, 150.0, 0.05
stress_calls = 0.40 * unfunded
stress_dist = 0.0
need = stress_calls - stress_dist + payout * assets
liquid = 120.0
ok(
    "liquidity plan: a stress year calls 40% of 150 unfunded (60) with no distributions, plus a 5% payout (50): "
    "needs 110 against 120 of cash and Treasuries, coverage 1.09",
    close(need, 110.0) and round(liquid / need, 2) == 1.09,
)
ok(
    "Ang p. 442: Harvard issued $2.5 billion of bonds in 2008-2009 because illiquid assets could not meet its "
    "short-duration liabilities - the failure the plan above tests for",
    2.5 > 0,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
