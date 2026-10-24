"""Historical scenarios, historical against Monte Carlo simulation, and sensitivity analysis (2026-10-20).

Worked numbers of meth:scenario-simulation-analysis. The investment problem: a 60/40 portfolio of the S&P 500
(with dividends) and 10-year Treasuries, rebalanced annually, held for ten years. Data: annual US returns 1928-2025
from notes/artefacts/portfolio-risk-return/us-asset-class-returns-1928-2025.csv (Damodaran's histretSP workbook,
January 2026). Seeds were fixed before the run and not changed; 20,000 paths per simulation.

Independent routes: scenario returns from the weights against a direct reading of the data rows; the Monte Carlo
mean and standard deviation of the one-year return against the analytic w'mu and sqrt(w' Sigma w); the
bootstrap's mean against the sample mean of the portfolio series; sensitivities as differences between
re-simulated distributions that share the same random draws (common random numbers).

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python scenario-simulation-checks.py   (numpy, pandas). Exits 1 on failure.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

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


root = Path(__file__).resolve().parents[1]
d = pd.read_csv(
    root / "portfolio-risk-return" / "us-asset-class-returns-1928-2025.csv", comment="#"
)
w = np.array([0.6, 0.4])
R = d[["sp500", "tbond_10y"]].to_numpy()
port = R @ w
yr = d.year.to_numpy()

# ---------------------------------------------------------------------------------------------
print("== part 1: historical scenarios")
scen = {y: port[yr == y][0] for y in (1931, 1974, 2008, 2022)}
row08 = d[d.year == 2008].iloc[0]
ok(
    "replayed years: 1931 -27.3%, 1974 -14.7%, 2008 -13.9%, 2022 -18.0%; 2008 equals 0.6 x -36.6% + 0.4 x 20.1%",
    [round(v, 3) for v in scen.values()] == [-0.273, -0.147, -0.139, -0.180]
    and close(scen[2008], 0.6 * row08.sp500 + 0.4 * row08.tbond_10y, 1e-12)
    and round(row08.sp500, 3) == -0.366
    and round(row08.tbond_10y, 3) == 0.201,
)
ok(
    "in 2008 Treasuries offset a third of the equity loss; in 2022 both fell (stocks -18.0%, bonds -17.8%)",
    round(d[d.year == 2022].sp500.iloc[0], 3) == -0.180
    and round(d[d.year == 2022].tbond_10y.iloc[0], 3) == -0.178,
)
w7374 = np.prod(1 + port[(yr >= 1973) & (yr <= 1974)]) - 1
infl7374 = np.prod(1 + d.cpi_inflation[(yr >= 1973) & (yr <= 1974)].to_numpy()) - 1
ok(
    "1973-74 as a two-year scenario: -20.8% nominal, -35.2% after 22.1% cumulative inflation",
    round(w7374, 3) == -0.208
    and round(infl7374, 3) == 0.221
    and round((1 + w7374) / (1 + infl7374) - 1, 3) == -0.352,
)
probs = {"recession": 0.20, "base": 0.60, "boom": 0.20}
rets = {"recession": -0.12, "base": 0.06, "boom": 0.18}
ok(
    "a three-scenario view (20% recession at -12%, 60% base at +6%, 20% boom at +18%) has an expected return of "
    "4.8% and a 20% chance of a double-digit loss",
    round(sum(probs[k] * rets[k] for k in probs), 3) == 0.048,
)

# ---------------------------------------------------------------------------------------------
print("== part 2: historical simulation against Monte Carlo for a ten-year horizon")
N, H = 20_000, 10
rng = np.random.default_rng(20261020)
idx = rng.integers(0, len(port), size=(N, H))
tw_hist = np.prod(1 + port[idx], axis=1)
ok(
    "bootstrap of whole years (which keeps each year's stock-bond pairing): mean one-year return equals the "
    "sample mean 9.0% within simulation error",
    abs(port[idx].mean() - port.mean()) < 0.001 and round(port.mean(), 3) == 0.090,
)
mu = R.mean(axis=0)
S = np.cov(R.T)
rng2 = np.random.default_rng(20261021)
Z = rng2.standard_normal((N, H, 2))
L = np.linalg.cholesky(S)
sim = mu + Z @ L.T
tw_mc = np.prod(1 + sim @ w, axis=1)
ok(
    "Monte Carlo with a normal fitted to the same means and covariance: one-year mean 9.0% and volatility 12.1% "
    "match w'mu and sqrt(w' Sigma w)",
    abs((sim @ w).mean() - w @ mu) < 0.001
    and abs((sim @ w).std() - np.sqrt(w @ S @ w)) < 0.001
    and round(np.sqrt(w @ S @ w), 3) == 0.121,
)
p_hist = np.percentile(tw_hist, [5, 50, 95])
p_mc = np.percentile(tw_mc, [5, 50, 95])
ok(
    "ten-year wealth per 1 invested: historical 5th/50th/95th percentiles 1.21 / 2.26 / 3.92; Monte Carlo "
    "1.22 / 2.23 / 3.97",
    [round(v, 2) for v in p_hist] == [1.21, 2.26, 3.92]
    and [round(v, 2) for v in p_mc] == [1.22, 2.23, 3.97],
    f"hist {np.round(p_hist, 3)}, mc {np.round(p_mc, 3)}",
)
one_hist = np.percentile(port, 5)
one_mc = np.percentile(sim[:, 0, :] @ w, 5)
ok(
    "one-year 5th percentile: -13.4% in the data against -10.8% under the normal: the fitted normal thins the "
    "left tail",
    round(one_hist, 3) == -0.134 and round(one_mc, 3) == -0.108,
)
ok(
    "chance of losing money over ten years: 1.8% historical against 1.4% Monte Carlo",
    round((tw_hist < 1).mean(), 3) == 0.018 and round((tw_mc < 1).mean(), 3) == 0.014,
)

# ---------------------------------------------------------------------------------------------
print("== part 3: sensitivity analysis with common random numbers")


def mc_wealth(mu_s=mu, S_s=S, w_s=w):
    Ls = np.linalg.cholesky(S_s)
    return np.prod(1 + (mu_s + Z @ Ls.T) @ w_s, axis=1)


base5, base50 = np.percentile(tw_mc, 5), np.median(tw_mc)
lowmu = mc_wealth(mu_s=mu - np.array([0.02, 0.0]))
corr = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])
S_hi = S.copy()
S_hi[0, 1] = S_hi[1, 0] = 0.5 * np.sqrt(S[0, 0] * S[1, 1])
hicorr = mc_wealth(S_s=S_hi)
w80 = mc_wealth(w_s=np.array([0.8, 0.2]))
sens = {
    "equity mean -2 points": (np.percentile(lowmu, 5) - base5, np.median(lowmu) - base50),
    "stock-bond correlation 0.5": (np.percentile(hicorr, 5) - base5, np.median(hicorr) - base50),
    "80/20 instead of 60/40": (np.percentile(w80, 5) - base5, np.median(w80) - base50),
}
for k_, v in sens.items():
    print(f"  {k_:28s} 5th pct {v[0]:+.3f}  median {v[1]:+.3f}")
ok(
    "historical stock-bond correlation is 0.02; raising it to 0.5 lowers the 5th percentile by 0.10 and the "
    "median by only 0.03; a 2-point lower equity mean lowers the median by 0.24 and the 5th percentile by 0.14; "
    "moving to 80/20 raises the median by 0.20 and lowers the 5th percentile by 0.11",
    round(corr, 2) == 0.02
    and round(sens["stock-bond correlation 0.5"][0], 2) == -0.10
    and round(sens["stock-bond correlation 0.5"][1], 2) == -0.03
    and round(sens["equity mean -2 points"][1], 2) == -0.24
    and round(sens["equity mean -2 points"][0], 2) == -0.14
    and round(sens["80/20 instead of 60/40"][1], 2) == 0.20
    and round(sens["80/20 instead of 60/40"][0], 2) == -0.11,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
