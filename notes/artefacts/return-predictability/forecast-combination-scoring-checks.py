"""Forecast combination and proper scoring: annual combination example and scoring-rule checks (2026-10-22).

Worked numbers of meth:forecast-combination and meth:proper-scoring-rules, under
forecast-combination-scoring-protocol.md (predictors, sample, transformations, seeds and tolerances written before
the first run).

Data: goyal-annual-predictors-1871-2025.csv, extracted by goyal_extract_predictors.py from the workbook on Amit
Goyal's page labelled "Original data (up to 2005) used in the paper", served on 2026-10-22 with data to December
2025 (a 2026 vintage). Synthetic data from seeds 20261105-20261108.

Independent routes: recursive OLS by running sums against numpy.linalg.lstsq refitted at each origin; the
combination's MSE from its errors, from the matrix of error products and from the ambiguity decomposition; forecasts
recomputed after the future is overwritten (chronological indexing); the normal CRPS in closed form against
quadrature of the threshold integral (Gneiting and Raftery eq. (20)) and against Monte Carlo of the kernel form
(eq. (21)); the interval score (43) against the sum of two quantile scores (41); the published Table 2 by simulation
in its design.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run --frozen --no-editable python forecast-combination-scoring-checks.py   (numpy, pandas, scipy; about 10 s). Exits 1 on failure.
Recorded output: forecast-combination-scoring-results.txt.
"""

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import integrate, stats

print(
    f"Python {sys.version.split()[0]}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}"
)
HERE = Path(__file__).resolve().parent
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{(': ' + detail) if detail else ''}")
    if not cond:
        fails.append(name)


# ================================================================ part F: forecast combination
print("\nF. Forecast combination, annual log equity premium, four predictors")

PREDICTORS = ["dp", "ep", "tms", "dfy"]
FIRST_OUTCOME, FIRST_FORECAST, LAST = 1927, 1947, 2025
SHOW_YEARS = [1947, 1970, 1990, 2010, 2025]


def load():
    return pd.read_csv(HERE / "goyal-annual-predictors-1871-2025.csv", comment="#").set_index(
        "yyyy"
    )


def build(raw):
    """Outcome y_t and predictors dated t - 1 for outcomes FIRST_OUTCOME..LAST (protocol, part F)."""
    pred = pd.DataFrame(
        {
            "dp": np.log(raw["D12"]) - np.log(raw["Index"]),
            "ep": np.log(raw["E12"]) - np.log(raw["Index"]),
            "tms": raw["lty"] - raw["tbl"],
            "dfy": raw["BAA"] - raw["AAA"],
        }
    )
    y = np.log1p(raw["CRSP_SPvw"]) - np.log1p(raw["Rfree"])
    years = np.arange(FIRST_OUTCOME, LAST + 1)
    X = pred.loc[years - 1].to_numpy()
    return years, y.loc[years].to_numpy(), X


def recursive(x, y, first):
    """Forecasts of y[i], i >= first, from OLS of y[s] on (1, x[s]) for s < i, by running sums; and the mean."""
    n = np.arange(1, len(y) + 1, dtype=float)
    sx, sy, sxx, sxy = (np.cumsum(v) for v in (x, y, x * x, x * y))
    sl = slice(first - 1, len(y) - 1)
    nn = n[sl]
    b = (nn * sxy[sl] - sx[sl] * sy[sl]) / (nn * sxx[sl] - sx[sl] ** 2)
    a = (sy[sl] - b * sx[sl]) / nn
    return a + b * x[first:], sy[sl] / nn


def lstsq_forecasts(x, y, first):
    out = []
    for i in range(first, len(y)):
        Z = np.column_stack([np.ones(i), x[:i]])
        coef = np.linalg.lstsq(Z, y[:i], rcond=None)[0]
        out.append(coef[0] + coef[1] * x[i])
    return np.array(out)


def all_forecasts(raw):
    years, y, X = build(raw)
    first = FIRST_FORECAST - FIRST_OUTCOME
    F = np.column_stack([recursive(X[:, j], y, first)[0] for j in range(X.shape[1])])
    bench = recursive(X[:, 0], y, first)[1]
    return years[first:], y[first:], F, bench, X, y, first


def stats_vs_mean(y, f, bench):
    eN, eA = y - bench, y - f
    mseN, mseA = np.mean(eN**2), np.mean(eA**2)
    fcw = eN**2 - (eA**2 - (bench - f) ** 2)
    t = fcw.mean() / (fcw.std(ddof=1) / np.sqrt(len(fcw)))
    return mseA, 100 * (1 - mseA / mseN), 100 * (np.sqrt(mseN) - np.sqrt(mseA)), t


raw = load()
fy, y_out, F, bench, X, y_all, first = all_forecasts(raw)
comb = F.mean(axis=1)
print(
    f"  outcomes {FIRST_OUTCOME}-{LAST} ({len(y_all)}), first forecast {FIRST_FORECAST} after {first} observations, P = {len(fy)}"
)

# F1. running sums against lstsq
dev = max(
    np.max(np.abs(lstsq_forecasts(X[:, j], y_all, first) - F[:, j])) for j in range(len(PREDICTORS))
)
ok("F1 recursive OLS by running sums equals lstsq refits", dev < 1e-10, f"max |diff| {dev:.1e}")

# F2. chronological indexing: overwrite the future in the raw data
for t in (1970, 2000):
    junk = raw.copy()
    rng = np.random.default_rng(t)
    later = junk.index > t
    for c in junk.columns:
        junk.loc[later, c] = rng.uniform(0.5, 2.0, later.sum()) * junk.loc[later, c].abs().mean()
    fy2, _, F2, b2, *_ = all_forecasts(junk)
    keep = fy <= t + 1
    d = max(np.max(np.abs(F2[keep] - F[keep])), np.max(np.abs(b2[keep] - bench[keep])))
    ok(
        f"F2 chronological indexing: forecasts through {t + 1} unchanged when later rows are overwritten",
        d == 0.0,
        f"max |diff| {d:.1e}",
    )


def report(label, y, F, bench, comb):
    print(f"\n  {label}: P = {len(y)}")
    print(f"  {'forecast':10s} {'MSFE x100':>10s} {'R2_OS %':>9s} {'dRMSE pp':>9s} {'CW t':>7s}")
    mseN = np.mean((y - bench) ** 2)
    print(f"  {'hist mean':10s} {100 * mseN:10.4f}")
    rows = {}
    for name, f in [*zip(PREDICTORS, F.T, strict=True), ("mean comb", comb)]:
        rows[name] = stats_vs_mean(y, f, bench)
        mse, r2, drmse, t = rows[name]
        print(f"  {name:10s} {100 * mse:10.4f} {r2:9.2f} {drmse:9.2f} {t:7.2f}")
    return rows


main = report("Evaluation 1947-2025", y_out, F, bench, comb)
w05 = fy <= 2005
sub = report("Evaluation 1947-2005", y_out[w05], F[w05], bench[w05], comb[w05])

# F3. error algebra
E = y_out[:, None] - F
ec = y_out - comb
N = len(PREDICTORS)
S = E.T @ E / len(y_out)
mse_c = np.mean(ec**2)
spread = np.mean((F - comb[:, None]) ** 2)
ok(
    "F3 combination error = mean of individual errors",
    np.max(np.abs(ec - E.mean(axis=1))) < 1e-12,
)
ok("F3 MSE_c = 1'S1 / N^2 (S = mean error products)", abs(mse_c - S.sum() / N**2) < 1e-12)
ok(
    "F3 ambiguity decomposition MSE_c = mean MSE_i - mean spread",
    abs(mse_c - (np.mean(E**2) - spread)) < 1e-12,
    f"{100 * mse_c:.4f} = {100 * np.mean(E**2):.4f} - {100 * spread:.4f} (x100)",
)

# F6. exact deterministic check with nonzero individual error biases
biased_errors = [
    [Fraction(3), Fraction(2), Fraction(3)],
    [Fraction(0), Fraction(3), Fraction(3)],
    [Fraction(0), Fraction(1), Fraction(3)],
]
T_bias, N_bias = len(biased_errors), len(biased_errors[0])


def fraction_mean(values):
    return sum(values, Fraction(0)) / len(values)


combo_errors = [fraction_mean(row) for row in biased_errors]
biases = [fraction_mean([biased_errors[t][i] for t in range(T_bias)]) for i in range(N_bias)]
bias_bar = fraction_mean(biases)
combo_mse = fraction_mean([e**2 for e in combo_errors])
combo_variance = fraction_mean([(e - bias_bar) ** 2 for e in combo_errors])
second_moment_mse = (
    sum(
        (
            fraction_mean([biased_errors[t][i] * biased_errors[t][j] for t in range(T_bias)])
            for i in range(N_bias)
            for j in range(N_bias)
        ),
        Fraction(0),
    )
    / N_bias**2
)
member_mse = fraction_mean(
    [fraction_mean([biased_errors[t][i] ** 2 for t in range(T_bias)]) for i in range(N_bias)]
)
forecast_spread = fraction_mean(
    [
        fraction_mean([(biased_errors[t][i] - combo_errors[t]) ** 2 for i in range(N_bias)])
        for t in range(T_bias)
    ]
)
ok(
    "F6 biased errors: combination MSE = variance + mean bias squared",
    combo_mse == combo_variance + bias_bar**2,
    f"biases {', '.join(map(str, biases))}; {combo_mse} = {combo_variance} + {bias_bar}^2",
)
ok(
    "F6 biased errors: second-moment and ambiguity identities still hold",
    combo_mse == second_moment_mse == member_mse - forecast_spread,
    f"{combo_mse} = {second_moment_mse} = {member_mse} - {forecast_spread}",
)
corr_e = np.corrcoef(E.T)
D = F - bench[:, None]
corr_d = np.corrcoef(D.T)
print("\n  1947-2025 correlation of forecast errors (dp, ep, tms, dfy):")
for i, r in zip(PREDICTORS, corr_e, strict=True):
    print(f"    {i:4s} " + " ".join(f"{v:6.3f}" for v in r))
print("  1947-2025 correlation of forecast deviations from the historical mean:")
for i, r in zip(PREDICTORS, corr_d, strict=True):
    print(f"    {i:4s} " + " ".join(f"{v:6.3f}" for v in r))
sd_d = D.std(axis=0, ddof=0)
print(
    "  sd of deviations (pp): "
    + ", ".join(f"{p} {100 * s:.2f}" for p, s in zip(PREDICTORS, sd_d, strict=True))
    + f"; combination {100 * D.mean(axis=1).std(ddof=0):.2f}"
)
print(
    f"  sd of outcome (pp): {100 * y_out.std(ddof=0):.2f}; sd of benchmark error {100 * (y_out - bench).std(ddof=0):.2f}"
)

print(
    "\n  Predeclared rows (percent): forecast for year, actual, hist mean, dp, ep, tms, dfy, mean comb"
)
for yr in SHOW_YEARS:
    i = int(np.where(fy == yr)[0][0])
    print(
        f"    {yr}  actual {100 * y_out[i]:7.2f}  mean {100 * bench[i]:6.2f}  "
        + "  ".join(f"{p} {100 * F[i, j]:6.2f}" for j, p in enumerate(PREDICTORS))
        + f"  comb {100 * comb[i]:6.2f}"
    )

# F4. synthetic diversification limit
rng = np.random.default_rng(20261105)
n = 200_000
for rho in (0.0, 0.5, 0.9, 0.99):
    z0 = rng.standard_normal(n)
    Z = rng.standard_normal((n, N))
    e = np.sqrt(rho) * z0[:, None] + np.sqrt(1 - rho) * Z
    got, want = np.mean(e.mean(axis=1) ** 2), rho + (1 - rho) / N
    ok(
        f"F4 rho = {rho}: MSE of average near rho + (1 - rho)/N",
        abs(got - want) < 0.01,
        f"{got:.4f} vs {want:.4f}",
    )

# F5. Bates-Granger weights
sig2 = np.array([1.0, 2.0, 4.0, 0.5])
Sd = np.diag(sig2)
w_mv = np.linalg.solve(Sd, np.ones(4))
w_mv /= w_mv.sum()
w_inv = (1 / sig2) / np.sum(1 / sig2)
ok(
    "F5 diagonal covariance: minimum-variance weights = inverse-MSE weights",
    np.max(np.abs(w_mv - w_inv)) < 1e-12,
)
Ec = np.cov(E.T, ddof=0) + np.outer(E.mean(0), E.mean(0))  # mean error products, as S
w_mv = np.linalg.solve(Ec, np.ones(N))
w_mv /= w_mv.sum()
w_inv = (1 / np.diag(Ec)) / np.sum(1 / np.diag(Ec))
print(
    "  ex post 1947-2025 weights, minimum-MSE (sum to one): "
    + ", ".join(f"{p} {w:.2f}" for p, w in zip(PREDICTORS, w_mv, strict=True))
)
print(
    "  ex post 1947-2025 weights, inverse MSE:             "
    + ", ".join(f"{p} {w:.3f}" for p, w in zip(PREDICTORS, w_inv, strict=True))
)
print(
    f"  ex post minimum-MSE combination MSFE x100: {100 / np.sum(np.linalg.solve(Ec, np.ones(N))):.4f}"
)

# ================================================================ part S: proper scoring
print(
    "\nS. Proper scoring rules (negatively oriented losses; units: percentage points unless stated)"
)
phi, Phi, Qn = stats.norm.pdf, stats.norm.cdf, stats.norm.ppf


def logs(mu, s, x):
    return -stats.norm.logpdf(x, mu, s)


def crps_normal(mu, s, x):
    z = (x - mu) / s
    return s * (z * (2 * Phi(z) - 1) + 2 * phi(z) - 1 / np.sqrt(np.pi))


def crps_quad(cdf, x):
    left = integrate.quad(lambda u: cdf(u) ** 2, -np.inf, x, epsabs=1e-12, epsrel=1e-12, limit=200)[
        0
    ]
    right = integrate.quad(
        lambda u: (1 - cdf(u)) ** 2, x, np.inf, epsabs=1e-12, epsrel=1e-12, limit=200
    )[0]
    return left + right


def interval_score(lo, hi, x, alpha):
    return (hi - lo) + (2 / alpha) * (lo - x) * (x < lo) + (2 / alpha) * (x - hi) * (x > hi)


def quantile_score(r, x, tau):
    return ((x <= r) - tau) * (r - x)


ALPHA = 0.1
fc = {"A": (5.0, 10.0), "B": (5.0, 20.0)}
rng = np.random.default_rng(20261106)
print("\n  S1 hand example: A = N(5, 10^2), B = N(5, 20^2); 90% central intervals")
print(
    f"  {'':3s} {'x':>5s} {'sq. err':>8s} {'-log f (pct)':>12s} {'-log f (dec)':>12s} {'CRPS':>7s} {'interval':>16s} {'IS':>7s}"
)
for x in (5.0, -15.0, -40.0):
    for k, (mu, s) in fc.items():
        lo, hi = mu + s * Qn(ALPHA / 2), mu + s * Qn(1 - ALPHA / 2)
        ls_pct = logs(mu, s, x)
        ls_dec = logs(mu / 100, s / 100, x / 100)
        cr = crps_normal(mu, s, x)
        IS = interval_score(lo, hi, x, ALPHA)
        print(
            f"  {k:3s} {x:5.0f} {(x - mu) ** 2:8.0f} {ls_pct:12.3f} {ls_dec:12.3f} {cr:7.3f} [{lo:6.2f}, {hi:5.2f}] {IS:7.2f}"
        )
        cq = crps_quad(lambda u, mu=mu, s=s: Phi((u - mu) / s), x)
        ok(
            f"S1 {k}, x = {x:.0f}: closed-form CRPS = quadrature of eq. (20)",
            abs(cr - cq) < 1e-7,
            f"{abs(cr - cq):.1e}",
        )
        X1 = rng.normal(mu, s, 1_000_000)
        X2 = rng.normal(mu, s, 1_000_000)
        h = np.abs(X1 - x) - 0.5 * np.abs(X1 - X2)
        se = h.std(ddof=1) / np.sqrt(h.size)
        ok(
            f"S1 {k}, x = {x:.0f}: kernel form eq. (21) by Monte Carlo within 4 se",
            abs(h.mean() - cr) < 4 * se,
            f"{h.mean():.3f} (se {se:.3f})",
        )
        qsum = (2 / ALPHA) * (
            quantile_score(lo, x, ALPHA / 2) + quantile_score(hi, x, 1 - ALPHA / 2)
        )
        ok(
            f"S1 {k}, x = {x:.0f}: interval score = (2/alpha) x sum of quantile scores",
            abs(qsum - IS) < 1e-12,
        )
        ok(
            f"S1 {k}, x = {x:.0f}: log score in decimals = in percent - log 100",
            abs(ls_dec - (ls_pct - np.log(100))) < 1e-12,
        )

# S2. propriety by quadrature
print("\n  S2 truth Q = N(5, 15^2); forecasts N(5, s^2)")
grid = np.arange(5.0, 30.0 + 1e-9, 0.5)
q = lambda x: stats.norm.pdf(x, 5, 15)
lim = (5 - 15 * 12, 5 + 15 * 12)


def expect(fun):
    return integrate.quad(
        lambda x: fun(x) * q(x), *lim, epsabs=1e-11, epsrel=1e-11, limit=400, points=[5.0]
    )[0]


exp_log, exp_crps, exp_is, exp_lin = [], [], [], []
for s in grid:
    lo, hi = 5 + s * Qn(ALPHA / 2), 5 + s * Qn(1 - ALPHA / 2)
    exp_log.append(expect(lambda x, s=s: logs(5, s, x)))
    exp_crps.append(expect(lambda x, s=s: crps_normal(5, s, x)))
    exp_is.append(
        integrate.quad(
            lambda x, lo=lo, hi=hi: interval_score(lo, hi, x, ALPHA) * q(x),
            *lim,
            points=[lo, hi],
            limit=400,
            epsabs=1e-11,
            epsrel=1e-11,
        )[0]
    )
    exp_lin.append(expect(lambda x, s=s: stats.norm.pdf(x, 5, s)))
for name, v in (("log score", exp_log), ("CRPS", exp_crps), ("interval score", exp_is)):
    v = np.array(v)
    ok(
        f"S2 expected {name} smallest at s = 15",
        grid[np.argmin(v)] == 15.0,
        f"argmin {grid[np.argmin(v)]:.1f}",
    )
ok(
    "S2 expected linear score (improper) largest at the smallest s",
    grid[np.argmax(exp_lin)] == grid[0],
)
for s in (10.0, 15.0, 20.0):
    i = int(np.where(grid == s)[0][0])
    print(
        f"    s = {s:4.1f}: E[-log f] {exp_log[i]:.4f}  E[CRPS] {exp_crps[i]:.4f}  E[IS90] {exp_is[i]:.3f}  E[f(x)] {exp_lin[i]:.5f}"
    )

# S3. Gneiting and Raftery, Table 2
print(
    "\n  S3 bilinear process (44), one-step 95% intervals I, J, K; Gneiting and Raftery Table 2 in brackets"
)


def bilinear(n, burn, seed):
    eps = np.random.default_rng(seed).standard_normal(n + burn).tolist()
    out = np.empty(n + burn)
    x = 0.0
    for t, e in enumerate(eps):
        out[t] = x
        x = 0.5 * x + 0.5 * x * e + e
    return out[burn:]


path = bilinear(100_001, 1_000, 20261107)
long = bilinear(10_000_000, 1_000, 20261108)
jlo, jhi = np.quantile(long, [0.025, 0.975])
print(f"    J's unconditional quantiles from 10^7 draws: [{jlo:.3f}, {jhi:.3f}]")
xt, xn = path[:-1], path[1:]
c = Qn(0.975)
m, sc = xt / 2, np.abs(1 + xt / 2)
gam = np.where(sc <= 7.36, np.sqrt(2 * np.clip(np.log(7.36) - np.log(sc), 0, None)) * sc, 0.0)
ints = {
    "I": (m - c * sc, m + c * sc),
    "J": (np.full_like(xt, jlo), np.full_like(xt, jhi)),
    "K": (m - gam, m + gam),
}
pub = {"I": (95.01, 4.00, 4.77), "J": (95.08, 5.45, 8.04), "K": (94.98, 3.79, 5.32)}
avg_is = {}
for k, (lo, hi) in ints.items():
    cov = 100 * np.mean((xn >= lo) & (xn <= hi))
    wid = np.mean(hi - lo)
    sc_k = interval_score(lo, hi, xn, 0.05)
    avg_is[k] = sc_k.mean()
    se = sc_k.reshape(100, -1).mean(axis=1).std(ddof=1) / 10
    pc, pw, ps = pub[k]
    print(
        f"    {k}: coverage {cov:6.2f}% ({pc}), width {wid:5.2f} ({pw}), interval score {avg_is[k]:5.2f} ({ps}), batch-means se {se:.3f}"
    )
    ok(f"S3 {k} coverage within 0.5 pp", abs(cov - pc) < 0.5)
    ok(f"S3 {k} width within 2%", abs(wid / pw - 1) < 0.02)
    ok(f"S3 {k} interval score within 3%", abs(avg_is[k] / ps - 1) < 0.03)
ok("S3 order by interval score I < K < J", avg_is["I"] < avg_is["K"] < avg_is["J"])

# S4. linear pool versus Gaussian around the averaged point forecast
print("\n  S4 forecasts N(0, 10^2) and N(8, 10^2): equal-weight linear pool against N(4, 10^2)")
MU, SD, W = np.array([0.0, 8.0]), np.array([10.0, 10.0]), np.array([0.5, 0.5])
pool_pdf = lambda x: np.sum(W * stats.norm.pdf(x, MU, SD))
pool_cdf = lambda x: np.sum(W * Phi((x - MU) / SD))
mean_pool = integrate.quad(lambda x: x * pool_pdf(x), -200, 210, limit=400, epsabs=1e-12)[0]
var_pool = integrate.quad(
    lambda x: (x - mean_pool) ** 2 * pool_pdf(x), -200, 210, limit=400, epsabs=1e-12
)[0]
ok(
    "S4 pool variance = 100 + 16 = 116 by quadrature",
    abs(var_pool - 116) < 1e-8,
    f"{var_pool:.10f}, mean {mean_pool:.10f}",
)


def abs_mean(m, s):
    return m * (2 * Phi(m / s) - 1) + 2 * s * phi(m / s)


def crps_pool(x):
    t1 = np.sum(W * abs_mean(MU - x, SD))
    t2 = sum(
        W[i] * W[j] * abs_mean(MU[i] - MU[j], np.hypot(SD[i], SD[j]))
        for i in range(2)
        for j in range(2)
    )
    return t1 - 0.5 * t2


for x in (-15.0, 4.0, 20.0):
    cp, cq = crps_pool(x), crps_quad(pool_cdf, x)
    ok(f"S4 pool CRPS at x = {x:.0f}: closed form = quadrature of eq. (20)", abs(cp - cq) < 1e-7)
    print(
        f"    x = {x:5.0f}: pool -log f {-np.log(pool_pdf(x)):.3f}, CRPS {cp:.3f};  N(4,10^2) -log f {logs(4, 10, x):.3f}, CRPS {crps_normal(4, 10, x):.3f}"
    )
lim4 = (-200, 210)
E_pool_log = integrate.quad(
    lambda x: -np.log(pool_pdf(x)) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11
)[0]
E_avg_log = integrate.quad(lambda x: logs(4, 10, x) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11)[
    0
]
E_pool_crps = integrate.quad(lambda x: crps_pool(x) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11)[
    0
]
E_avg_crps = integrate.quad(
    lambda x: crps_normal(4, 10, x) * pool_pdf(x), *lim4, limit=400, epsabs=1e-11
)[0]
print(
    f"    truth = pool: E[-log f] pool {E_pool_log:.4f}, N(4,10^2) {E_avg_log:.4f}; E[CRPS] pool {E_pool_crps:.4f}, N(4,10^2) {E_avg_crps:.4f}"
)
ok("S4 truth = pool: pool has the lower expected log score", E_pool_log < E_avg_log)
ok("S4 truth = pool: pool has the lower expected CRPS", E_pool_crps < E_avg_crps)

# ================================================================ recorded values (added after the first run)
print("\nR. Recorded values of the first run, at their printed rounding (drift check)")
r2_main = [round(main[k][1], 2) for k in [*PREDICTORS, "mean comb"]]
r2_sub = [round(sub[k][1], 2) for k in [*PREDICTORS, "mean comb"]]
ok(
    "R R2_OS 1947-2025 (dp, ep, tms, dfy, comb)",
    r2_main == [-1.83, -2.28, -3.60, -0.83, 2.56],
    f"{[float(v) for v in r2_main]}",
)
ok(
    "R R2_OS 1947-2005 (dp, ep, tms, dfy, comb)",
    r2_sub == [1.34, 4.61, -3.70, -1.00, 5.82],
    f"{[float(v) for v in r2_sub]}",
)
ok(
    "R combination CW t 1947-2025 and 1947-2005",
    [round(main["mean comb"][3], 2), round(sub["mean comb"][3], 2)] == [1.44, 2.13],
)
ok(
    "R ambiguity terms x100",
    [round(100 * mse_c, 4), round(100 * np.mean(E**2), 4), round(100 * spread, 4)]
    == [2.65, 2.7777, 0.1277],
)
ok(
    "R S2 expected scores at s = 15",
    [round(exp_log[20], 4), round(exp_crps[20], 4), round(exp_is[20], 3)]
    == [4.127, 8.4628, 61.881],
)
ok(
    "R S3 average interval scores I, J, K",
    [round(avg_is[k], 2) for k in "IJK"] == [4.76, 8.03, 5.29],
)
ok(
    "R S4 expected scores, truth = pool",
    [round(v, 4) for v in (E_pool_log, E_avg_log, E_pool_crps, E_avg_crps)]
    == [3.7957, 3.8015, 6.0816, 6.0903],
)

# ================================================================ summary
print(f"\n{n_checks} checks, {len(fails)} failed")
if fails:
    print("FAILED: " + "; ".join(fails))
    sys.exit(1)
