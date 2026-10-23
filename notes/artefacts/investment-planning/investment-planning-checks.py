"""Investment planning case (2026-10-18; tax and transition corrections the same day): the worked numbers of
meth:investment-policy-statement, meth:asset-class-portfolio-construction, ex:investment-planning-case,
def:behavioural-biases and meth:risk-identification-modification.

A fictional client: age 50, 2,000,000 investable (currency units of an unnamed jurisdiction), of which 150,000 is
needed for a renovation in 18 months and 50,000 is held as an emergency reserve; real after-tax savings of 40,000 a
year (end of year) for 12 years; real after-tax spending of 145,000 a year from the portfolio for 30 years from age
62, withdrawn at the start of each year. Inflation 2.5 percent is hypothetical.

Tax basis (hypothetical, stated so that no tax is counted twice):
- a flat 15 percent tax on every year's nominal return as earned, losses fully offset; withdrawals are not taxed
  again, so savings, spending and the required return are real and after tax;
- capital market assumptions are real and pre-tax; with nominal return (1 + r)(1 + pi) - 1 taxed at t, the
  after-tax real return is exactly (1 - t) r - t pi / (1 + pi), so its mean and sd follow linearly;
- a 20 percent tax applies only to the 300,000 gain already embedded in the inherited stock (400,000). The stock is
  sold in thirds now, in 12 and in 24 months, at today's value, and 20,000 (nominal) is paid from the long-term pool at
  the end of each of years 1-3. The stock's returns from today are taxed like all others at 15 percent.

The transition risk (part 3) uses the five-asset weights with the stock carved out of the equity sleeve. The stock's
expected real return is assumed equal to global equity's 5.5 percent (no view on the stock); a beta-consistent
alternative, 0.5 + 1.3125 x 5.0 = 7.06 percent, is also checked. The capital market assumptions are invented for
teaching, not forecasts. The risk objective (5th-percentile one-year real loss no worse than -13 percent) is measured
on pre-tax returns, the fall in portfolio value before any tax offset; the after-tax alternative is also reported.

Part 4 reproduces Edwards's urn calculation as quoted by Barberis and Thaler (NBER w9222, p. 14): posterior 0.97.

No random draws. Run: uv run --frozen --no-editable python investment-planning-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: return requirement (real, after tax)")
investable = 2_000_000
renovation, reserve = 150_000, 50_000
A0 = investable - renovation - reserve
S, n_save = 40_000, 12
W, n_draw = 145_000, 30
infl, tax, cgt = 0.025, 0.15, 0.20
conc, gain = 400_000, 300_000
gains_tax = [(k, gain * cgt / 3 / (1 + infl) ** k) for k in (1, 2, 3)]  # (year end, real amount)


def fv_at_62(r, savings=S, years=n_save, with_gains_tax=True):
    v = A0 * (1 + r) ** years + savings * ((1 + r) ** years - 1) / r
    if with_gains_tax:
        v -= sum(x * (1 + r) ** (years - k) for k, x in gains_tax)
    return v


def pv_need(r, spend=W, years=n_draw):
    return spend * (1 - (1 + r) ** -years) / r * (1 + r)  # annuity due


r_base = brentq(lambda r: fv_at_62(r, with_gains_tax=False) - pv_need(r), 1e-6, 0.2)
r_req = brentq(lambda r: fv_at_62(r) - pv_need(r), 1e-6, 0.2)
ok(
    "long-term pool 1,800,000 after setting aside 200,000 for the renovation and reserve",
    A0 == 1_800_000,
)
ok(
    "the stock sale realises 60,000 of gains tax: 20,000 nominal at the end of years 1-3 (19,512, 19,036, 18,571 real)",
    close(sum(gain * cgt / 3 for _ in gains_tax), 60_000)
    and np.allclose([x for _, x in gains_tax], [19_512.195, 19_036.288, 18_571.988], atol=1e-3),
)
ok("ignoring the gains tax the requirement would be 2.699%", abs(r_base - 0.0269872) < 1e-6)
ok(
    "paying it from the pool raises the required real after-tax return to 2.808%",
    abs(r_req - 0.0280809) < 1e-6,
)
ok(
    "at 2.808% the pool reaches 2,995,705 at 62, the present value of the spending",
    abs(fv_at_62(r_req) - pv_need(r_req)) < 1e-6 and abs(fv_at_62(r_req) - 2_995_705) < 1,
)
# Independent check: roll the account forward year by year at r_req, paying the gains tax and saving at year ends.
bal = A0
for yr in range(1, n_save + 1):
    bal = bal * (1 + r_req) + S - sum(x for k, x in gains_tax if k == yr)
for _ in range(n_draw):
    bal = (bal - W) * (1 + r_req)
ok("year-by-year roll-forward ends at zero after 30 withdrawals", abs(bal) < 1e-3, f"{bal:.6f}")
nominal = (1 + r_req) * (1 + infl) - 1
pretax = nominal / (1 - tax)
pretax_real = (1 + pretax) / (1 + infl) - 1
ok("nominal after-tax requirement (1.02808)(1.025) - 1 = 5.38%", abs(nominal - 0.053783) < 1e-5)
ok(
    "pre-tax nominal, taxing all nominal returns at 15% every year: 6.33%",
    abs(pretax - 0.063274) < 1e-5,
)
ok(
    "pre-tax real 3.73%, the same as inverting the after-tax map (r + t pi/(1 + pi))/(1 - t)",
    abs(pretax_real - 0.037339) < 1e-5
    and close(pretax_real, (r_req + tax * infl / (1 + infl)) / (1 - tax), 1e-12),
)
ok(
    "the additive shortcut (2.81 + 2.5)/0.85 = 6.24% understates the pre-tax nominal requirement",
    abs((r_req + infl) / (1 - tax) - 0.062448) < 1e-5,
)

# Maginn, Tuttle, McLeavey and Pinto (MIP, 3rd ed., 2007, chap. 1, p. 14): two required-return examples.
ok(
    "MIP p. 14: (2.0m / 1.2m)^(1/18) - 1 = 2.88% after tax",
    abs((2.0 / 1.2) ** (1 / 18) - 1 - 0.0288) < 5e-5,
)
r_wd = brentq(lambda r: 1.2e6 * (1 + r) ** 18 - 25_000 * ((1 + r) ** 18 - 1) / r - 2.0e6, 1e-6, 0.2)
ok(
    "MIP p. 14: with 25,000 withdrawn at each year end, 4.55% after tax; 7.0% pre-tax at a 35% tax rate",
    abs(r_wd - 0.0455) < 5e-5 and abs(r_wd / 0.65 - 0.070) < 5e-4,
)
ok(
    "MIP p. 14: retiree (4% + 2%)/(1 - 0.40) = 10% pre-tax nominal (an additive approximation)",
    close((0.04 + 0.02) / 0.60, 0.10),
)

print("== part 2: candidate strategic allocations against the requirement and the loss limit")
names = ["global equity", "government bonds", "inflation-linked bonds", "cash"]
mu = np.array([5.5, 1.5, 1.2, 0.5])  # percent, real, pre-tax, arithmetic
sd = np.array([16.0, 6.0, 5.0, 1.0])
C = np.array([[1, 0.1, 0.2, 0.0], [0.1, 1, 0.7, 0.1], [0.2, 0.7, 1, 0.1], [0.0, 0.1, 0.1, 1]])
V = np.outer(sd, sd) * C
ok("correlation matrix is positive definite", np.all(np.linalg.eigvalsh(C) > 0))
drag = 100 * tax * infl / (1 + infl)  # percent: tax on the inflation part of the nominal return
ok("tax on inflation costs 0.366 points of real return a year", abs(drag - 0.365854) < 1e-6)
# Independent check of the linear after-tax map on one return.
r_test = 0.07
direct = (1 + (1 - tax) * ((1 + r_test) * (1 + infl) - 1)) / (1 + infl) - 1
ok(
    "after-tax real return = (1 - t) r - t pi/(1 + pi), exactly",
    close(direct, (1 - tax) * r_test - tax * infl / (1 + infl), 1e-15),
)
z5 = norm.ppf(0.05)
mixes = {
    "conservative": np.array([0.30, 0.50, 0.15, 0.05]),
    "balanced": np.array([0.55, 0.30, 0.10, 0.05]),
    "growth": np.array([0.75, 0.15, 0.05, 0.05]),
}
loss_limit = -13.0  # percent: one-year 5th-percentile real loss (pre-tax) must not be worse


def mix_stats(w):
    m, s = w @ mu, math.sqrt(w @ V @ w)
    m_at, s_at = (1 - tax) * m - drag, (1 - tax) * s
    return {
        "mean": m,
        "sd": s,
        "q5": m + z5 * s,
        "mean_at": m_at,
        "sd_at": s_at,
        "geo_at": m_at - s_at * s_at / 200,  # geometric approximation, percent units
        "q5_at": m_at + z5 * s_at,
    }


res = {k: mix_stats(w) for k, w in mixes.items()}
for k, v in res.items():
    print(
        f"    {k:12s} pre-tax mean {v['mean']:.3f} sd {v['sd']:.3f} 5th pct {v['q5']:.3f} | "
        f"after-tax mean {v['mean_at']:.3f} sd {v['sd_at']:.3f} geometric~ {v['geo_at']:.3f} 5th pct {v['q5_at']:.3f}"
    )
req = 100 * r_req
ok(
    "conservative: after-tax geometric 1.70 < 2.81 (fails the return requirement); 5th pct -7.81",
    abs(res["conservative"]["geo_at"] - 1.7035) < 1e-3 and res["conservative"]["geo_at"] < req,
)
ok(
    "balanced: pre-tax mean 3.62, sd 9.34; after tax mean 2.71, sd 7.93, geometric 2.396 < 2.81; 5th pct -11.73",
    abs(res["balanced"]["sd"] - 9.3351) < 1e-3
    and abs(res["balanced"]["mean_at"] - 2.7111) < 1e-3
    and abs(res["balanced"]["geo_at"] - 2.3963) < 1e-3
    and res["balanced"]["geo_at"] < req
    and res["balanced"]["q5"] > loss_limit,
)
ok(
    "growth: after-tax geometric 2.87 meets the requirement, but the 5th percentile -15.61 breaches -13",
    abs(res["growth"]["geo_at"] - 2.8672) < 1e-3
    and res["growth"]["geo_at"] >= req
    and abs(res["growth"]["q5"] + 15.6134) < 1e-3
    and res["growth"]["q5"] < loss_limit,
)
ok(
    "with full loss offset the after-tax 5th percentiles are -7.01, -10.34 and -13.64: the same verdicts",
    np.allclose([res[k]["q5_at"] for k in mixes], [-7.0066, -10.3405, -13.6373], atol=1e-3),
)
ok(
    "so no candidate meets both objectives",
    [k for k, v in res.items() if v["geo_at"] >= req and v["q5"] >= loss_limit] == [],
)


# The best any long-only mix of the four classes can do within the loss limit.
def best_within_limit(limit_key):
    def slack(w):
        v = mix_stats(w)
        return v[limit_key] - loss_limit

    best = None
    for x0 in (mixes["balanced"], np.full(4, 0.25), np.array([0.6, 0.4, 0.0, 0.0])):
        r = minimize(
            lambda w: -mix_stats(w)["geo_at"],
            x0,
            method="SLSQP",
            bounds=[(0, 1)] * 4,
            constraints=[
                {"type": "eq", "fun": lambda w: w.sum() - 1},
                {"type": "ineq", "fun": slack},
            ],
            options={"ftol": 1e-14, "maxiter": 500},
        )
        if best is None or r.fun < best.fun:
            best = r
    return best.x, mix_stats(best.x)


w_pre, v_pre = best_within_limit("q5")
w_post, v_post = best_within_limit("q5_at")
print(
    f"    best within the pre-tax limit {np.round(w_pre, 4)}; within the after-tax limit {np.round(w_post, 4)}"
)
ok(
    "best long-only mix within the pre-tax limit is about 61/39/0/0 and earns 2.61 after tax: still 0.20 short",
    np.allclose(w_pre, [0.6133, 0.3867, 0, 0], atol=2e-3) and abs(v_pre["geo_at"] - 2.6106) < 1e-3,
)
ok(
    "measured after tax with full loss offset, 71/29/0/0 would just reach 2.83 (0.03 above), with no ILB or cash",
    np.allclose(w_post, [0.711, 0.289, 0, 0], atol=2e-3)
    and abs(v_post["geo_at"] - 2.8339) < 1e-3
    and v_post["geo_at"] - req < 0.05,
)
# Funding gap at the balanced mix's after-tax geometric return.
g_bal = res["balanced"]["geo_at"] / 100
spend_ok = fv_at_62(g_bal) / (pv_need(g_bal) / W)
save_ok = brentq(lambda x: fv_at_62(g_bal, savings=x) - pv_need(g_bal), 0, 500_000)
surplus = {
    d: fv_at_62(g_bal, years=n_save + d) - pv_need(g_bal, years=n_draw - d) for d in (0, 1, 2)
}
print(
    f"    at {100 * g_bal:.3f}%: sustainable spending {spend_ok:,.0f}; savings needed {save_ok:,.0f}; "
    f"surplus at retirement by delay {dict((d, round(v)) for d, v in surplus.items())}"
)
ok(
    "at 2.40% the plan is short by 283,249 at 62; it supports spending of about 132,000, not 145,000",
    abs(-surplus[0] - 283_249) < 1 and abs(spend_ok - 131_966) < 1,
)
ok("or savings of about 60,650 a year instead of 40,000", abs(save_ok - 60_652) < 1)
ok(
    "or retiring at 64 (spending to 92): short by 101,562 at 63, 84,479 to spare at 64",
    abs(surplus[1] + 101_562) < 1 and abs(surplus[2] - 84_479) < 1,
)
# Risk contributions (Euler): RC_i = w_i (V w)_i / sigma, summing to sigma.
w = mixes["balanced"]
s = math.sqrt(w @ V @ w)
rc = w * (V @ w) / s
ok("risk contributions sum to portfolio sd", close(rc.sum(), s))
ok("equity is 55% of capital but 91.7% of variance risk", abs(rc[0] / s - 0.9169) < 1e-4)
# Rebalancing ranges: +/- 5 points on equity, +/- 4 on bonds, +/- 2 on others; the drift example.
drift = w * np.array([1.18, 0.99, 1.00, 1.00])
drift = drift / drift.sum()
ok(
    "an 18% equity rally with a 1% bond fall moves equity to 59.2%, inside 50-60%",
    abs(drift[0] - 0.5922) < 1e-4 and 0.50 <= drift[0] <= 0.60,
)

print("== part 3: concentrated holding during the staged sale, hedged and unhedged")
ok("the single stock is 22.2% of the long-term pool", abs(conc / A0 - 0.2222) < 1e-4)
ok(
    "selling it at once would also realise 60,000 of tax (3.3% of the pool): staging at a flat rate defers it",
    close(gain * cgt, 60_000) and abs(gain * cgt / A0 - 0.0333) < 1e-4,
)
sd_stock, rho = 35.0, 0.6
sd5 = np.append(sd, sd_stock)
C5 = np.eye(5)
C5[:4, :4] = C
C5[0, 4] = C5[4, 0] = rho
C5[1, 4] = C5[4, 1] = 0.1
C5[2, 4] = C5[4, 2] = 0.15
V5 = np.outer(sd5, sd5) * C5
ok("five-asset correlation matrix is positive definite", np.all(np.linalg.eigvalsh(C5) > 0))
beta_stock = V5[0, 4] / V5[0, 0]
spec_sd = math.sqrt(V5[4, 4] - beta_stock**2 * V5[0, 0])
ok(
    "stock beta to global equity 1.3125; specific sd 28%, i.e. 6.2 points of sd at a 22.2% weight",
    close(beta_stock, 1.3125) and close(spec_sd, 28.0) and abs(conc / A0 * spec_sd - 6.2222) < 1e-4,
)


def stage(x_stock, hedge, mu_stock):
    """Stock carved out of the 55-point equity sleeve; a short index future on `hedge` of the pool earns minus the
    equity return over cash (basis ignored), i.e. moves `hedge` from equity to cash.
    """
    w5 = np.array([0.55 - x_stock - hedge, 0.30, 0.10, 0.05 + hedge, x_stock])
    m5 = np.append(mu, mu_stock)
    s5 = math.sqrt(w5 @ V5 @ w5)
    return w5 @ m5, s5, w5 @ m5 + z5 * s5


x_full, x_two, x_one = conc / A0, 2 / 3 * conc / A0, 1 / 3 * conc / A0
mu_eq, mu_beta = 5.5, 0.5 + beta_stock * 5.0
m0, s0, q0 = stage(x_full, 0.0, mu_eq)
m1, s1, q1 = stage(x_full, 0.10, mu_eq)
print(
    f"    full holding: unhedged mean {m0:.3f} sd {s0:.4f} 5th {q0:.3f}; hedged mean {m1:.3f} sd {s1:.4f} 5th {q1:.3f}"
)
ok("keeping the stock raises portfolio sd from 9.34% to 12.19%", abs(s0 - 12.1912) < 1e-4)
ok(
    "a 10%-notional short index future with its cash leg lowers it to 10.89% and the mean by 0.50 points",
    abs(s1 - 10.8922) < 1e-4 and close(m0 - m1, 0.50),
)
ok(
    "but the hedged 5th percentile -14.80 still breaches the -13 limit (unhedged -16.43)",
    abs(q1 + 14.796) < 1e-3 and abs(q0 + 16.433) < 1e-3 and q1 < loss_limit,
)
h_need = brentq(lambda h: stage(x_full, h, mu_eq)[2] - loss_limit, 0.0, 0.5)
h_minvar = minimize_scalar(lambda h: stage(x_full, h, mu_eq)[1], bounds=(0, 1), method="bounded").x
ok(
    "with the full holding the limit needs about 22% notional; even the minimum-variance hedge leaves sd 6.75%",
    abs(h_need - 0.2227) < 1e-3 and abs(stage(x_full, h_minvar, mu_eq)[1] - 6.747) < 1e-3,
)
_, _, q_one_h = stage(x_two, 0.10, mu_eq)
_, _, q_two_u = stage(x_one, 0.0, mu_eq)
ok(
    "after the first third is sold, the 10% hedge meets the limit (-12.52); after the second, no hedge is needed (-12.73)",
    abs(q_one_h + 12.524) < 1e-3
    and q_one_h > loss_limit
    and abs(q_two_u + 12.726) < 1e-3
    and q_two_u > loss_limit,
)
qb = [
    stage(x_full, 0.0, mu_beta)[2],
    stage(x_full, 0.10, mu_beta)[2],
    stage(x_two, 0.10, mu_beta)[2],
    stage(x_one, 0.0, mu_beta)[2],
]
ok(
    "with a beta-consistent 7.06% stock mean: -16.09, -14.45, -12.29, -12.61; the same verdicts",
    np.allclose(qb, [-16.086, -14.449, -12.292, -12.610], atol=1e-3)
    and [q < loss_limit for q in qb] == [True, True, False, False],
)
ok(
    "liquidity sleeve covers 18 months: 200,000 = renovation + reserve",
    renovation + reserve == 200_000,
)

print("== part 4: behavioural and governance numbers")
lr = (0.7 / 0.3) ** 8 * (
    0.3 / 0.7
) ** 4  # urn 1: 7 red, 3 blue; urn 2: 3 red, 7 blue; draw 8 red, 4 blue
post = lr / (1 + lr)
ok(
    "Edwards's urn: posterior 0.967 for 8 red and 4 blue (Bayes), against a typical answer of 0.7",
    abs(post - 0.9674) < 1e-4,
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
