"""Investment planning case (2026-10-18): the worked numbers of meth:investment-policy-statement,
meth:asset-class-portfolio-construction, ex:investment-planning-case, def:behavioural-biases and
meth:risk-identification-modification.

A fictional client: age 50, 2,000,000 investable (currency units of an unnamed jurisdiction), of which 150,000 is
needed for a renovation in 18 months and 50,000 is held as an emergency reserve; real after-tax savings of 40,000 a
year (end of year) for 12 years; real spending of 145,000 a year from the portfolio for 30 years from age 62,
withdrawn at the start of each year. The required real return solves future value at 62 = present value of the
spending. Inflation 2.5 percent and a flat 15 percent tax on all returns are hypothetical. Capital market
assumptions (real, annual, arithmetic means and standard deviations, correlations) are invented for teaching, not
forecasts. The concentrated holding (400,000 with a 300,000 gain, 20 percent tax on realised gains) is invented.

Part 4 reproduces Edwards's urn calculation as quoted by Barberis and Thaler (NBER w9222, p. 14): posterior 0.97.

No random draws. Run: uv run python investment-planning-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.stats import norm

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


print("== part 1: return requirement")
investable = 2_000_000
renovation, reserve = 150_000, 50_000
A0 = investable - renovation - reserve
S, n_save = 40_000, 12
W, n_draw = 145_000, 30


def fv_at_62(r):
    return A0 * (1 + r) ** n_save + S * ((1 + r) ** n_save - 1) / r


def pv_need_at_62(r):
    return W * (1 - (1 + r) ** -n_draw) / r * (1 + r)  # annuity due


r_req = brentq(lambda r: fv_at_62(r) - pv_need_at_62(r), 1e-6, 0.2)
ok(
    "long-term pool 1,800,000 after setting aside 200,000 for the renovation and reserve",
    A0 == 1_800_000,
)
ok("required real after-tax return 2.70% a year", abs(r_req - 0.026987) < 1e-5)
ok(
    "at 2.70% the pool reaches 3,035,787 at 62, equal to the present value of the spending",
    abs(fv_at_62(r_req) - pv_need_at_62(r_req)) < 1e-6 and abs(fv_at_62(r_req) - 3_035_787) < 1,
)
# Independent check: simulate the account year by year at r_req; it should end at ~0 after the last withdrawal year.
bal = A0
for _ in range(n_save):
    bal = bal * (1 + r_req) + S
for _ in range(n_draw):
    bal = (bal - W) * (1 + r_req)
ok("year-by-year roll-forward ends at zero after 30 withdrawals", abs(bal) < 1e-3, f"{bal:.6f}")
infl, tax = 0.025, 0.15
nominal = (1 + r_req) * (1 + infl) - 1
pretax = nominal / (1 - tax)
ok("nominal after-tax requirement (1.0270)(1.025) - 1 = 5.27%", abs(nominal - 0.052662) < 1e-5)
ok("pre-tax nominal, taxing all returns at 15% every year: 6.20%", abs(pretax - 0.061956) < 1e-5)
ok(
    "the additive shortcut (2.70 + 2.5)/0.85 = 6.12% understates it slightly",
    abs((r_req + infl) / (1 - tax) - 0.061161) < 1e-5,
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
mu = np.array([5.5, 1.5, 1.2, 0.5])  # percent, real, arithmetic
sd = np.array([16.0, 6.0, 5.0, 1.0])
C = np.array([[1, 0.1, 0.2, 0.0], [0.1, 1, 0.7, 0.1], [0.2, 0.7, 1, 0.1], [0.0, 0.1, 0.1, 1]])
V = np.outer(sd, sd) * C
ok("correlation matrix is positive definite", np.all(np.linalg.eigvalsh(C) > 0))
mixes = {
    "conservative": np.array([0.30, 0.50, 0.15, 0.05]),
    "balanced": np.array([0.55, 0.30, 0.10, 0.05]),
    "growth": np.array([0.75, 0.15, 0.05, 0.05]),
}
loss_limit = -13.0  # percent: one-year 5th-percentile real loss must not be worse
res = {}
for k, w in mixes.items():
    m = w @ mu
    s = math.sqrt(w @ V @ w)
    g = m - s * s / 200  # geometric approximation, percent units
    q5 = m + norm.ppf(0.05) * s
    res[k] = (m, s, g, q5)
    print(f"    {k:12s} mean {m:.3f}  sd {s:.3f}  geometric~ {g:.3f}  5th pct {q5:.3f}")
ok(
    "conservative: mean 2.605, sd 6.333, geometric 2.404 < 2.70 (fails the return requirement)",
    abs(res["conservative"][2] - 2.4044) < 1e-3 and res["conservative"][2] < 100 * r_req,
)
ok(
    "balanced: mean 3.620, sd 9.335, geometric 3.184 >= 2.70 and 5th percentile -11.73 > -13",
    abs(res["balanced"][1] - 9.3351) < 1e-3
    and res["balanced"][2] > 100 * r_req
    and res["balanced"][3] > loss_limit,
)
ok(
    "growth: 5th percentile -15.61 breaches the -13 limit although its mean is highest",
    abs(res["growth"][3] + 15.6138) < 1e-3 and res["growth"][3] < loss_limit,
)
ok(
    "so balanced is the only candidate meeting both objectives",
    [k for k, v in res.items() if v[2] >= 100 * r_req and v[3] >= loss_limit] == ["balanced"],
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

print("== part 3: concentrated holding and liquidity")
conc, gain, cgt = 400_000, 300_000, 0.20
ok("the single stock is 22.2% of the long-term pool", abs(conc / A0 - 0.2222) < 1e-4)
ok(
    "selling it at once realises 60,000 of tax (3.3% of the pool)",
    close(gain * cgt, 60_000) and abs(gain * cgt / A0 - 0.0333) < 1e-4,
)
sd_stock, rho = 35.0, 0.6
# Risk with the stock carved out of the equity sleeve (22.2 of the 55 points): stock sd 35%, correlation 0.6 with equity.
w5 = np.array([0.55 - conc / A0, 0.30, 0.10, 0.05, conc / A0])
sd5 = np.append(sd, sd_stock)
C5 = np.eye(5)
C5[:4, :4] = C
C5[0, 4] = C5[4, 0] = rho
C5[1, 4] = C5[4, 1] = 0.1
C5[2, 4] = C5[4, 2] = 0.15
V5 = np.outer(sd5, sd5) * C5
s5 = math.sqrt(w5 @ V5 @ w5)
ok("keeping the stock raises portfolio sd from 9.34% to 12.19%", abs(s5 - 12.191) < 1e-3)
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
# Risk modification by shifting: sell equity index futures on 10% of the portfolio (beta 1 to the equity class).
# A short future earns minus the equity return over cash (cost of carry, basis ignored), so the position is
# equivalent to moving 10 points from equity to cash.
w_overlay = w + np.array([-0.10, 0.0, 0.0, 0.10])
s_ov = math.sqrt(w_overlay @ V @ w_overlay)
print(f"    overlay sd {s_ov:.4f}, mean {w_overlay @ mu:.4f}")
ok("a futures overlay on 10% notional cuts sd from 9.34% to 7.79%", abs(s_ov - 7.7919) < 1e-3)
ok(
    "and the arithmetic mean by 0.50 points: 10% of the 5.0-point equity premium over cash",
    close(w @ mu - w_overlay @ mu, 0.50),
)

print()
if fails:
    print(f"{len(fails)} check(s) failed: {fails}")
    sys.exit(1)
print("all checks passed")
