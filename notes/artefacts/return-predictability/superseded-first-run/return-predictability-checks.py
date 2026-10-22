"""Return predictability: present-value identity, nested forecast tests and restricted forecasts (2026-10-22).

Worked numbers of res:campbell-shiller-identity, meth:nested-forecast-tests and meth:restricted-forecast-value,
under return-predictability-protocol.md (definitions, timing and tolerances written before the first run).

Data: goyal-annual-1871-2025.csv and goyal-monthly-1871-2025.csv, extracted by goyal_extract.py from the workbook
on Amit Goyal's page labelled "Original data (up to 2005) used in the paper", served on 2026-10-22 with data to
December 2025 (a 2026 vintage, not the file behind the 2008 tables). Synthetic data from fixed seeds (20261022,
20261023) where the true model must be known.

Independent routes: recursive OLS by running sums against numpy.linalg.lstsq refitted at each origin; the
Clark-West statistic as the mean of f against 2 mean(e_N (e_N - e_A)) and against MSE_N - (MSE_A - adj); ENC
against the Clark-West numerator; the exact return identity against the log-linear one with its error kept;
forecasts recomputed after the future is overwritten (timing).

After the first run (recorded in the protocol): a harness correction in C4, a cap-share diagnostic, the post-run
supplement C5 (not part of any verdict) and regression checks on the observed values; no tolerance changed.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python return-predictability-checks.py   (numpy, pandas; about 1 s). Exits 1 on failure.
Recorded output: return-predictability-results.txt.
"""

# standard library imports
import sys
from pathlib import Path

# third party library imports
import numpy as np
import pandas as pd

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, pandas {pd.__version__}")
HERE = Path(__file__).resolve().parent
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{(': ' + detail) if detail else ''}")
    if not cond:
        fails.append(name)


# ---------------------------------------------------------------- shared tools
def recursive_forecasts(x, y, first):
    """One-step forecasts of y[i], i >= first, from OLS of y[s] on x[s] for s < i, and the historical mean.

    x[i] is the predictor known before y[i] (already lagged). Arrays may carry leading replication axes.
    Returns (regression forecast, mean forecast, slope) for i = first, ..., n - 1.
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    cs = lambda a: np.cumsum(a, axis=-1)
    n = np.arange(1, x.shape[-1] + 1, dtype=float)
    sx, sy, sxx, sxy = cs(x), cs(y), cs(x * x), cs(x * y)
    # sums through s = i - 1 sit at position i - 1
    sl = slice(first - 1, x.shape[-1] - 1)
    nn, sx, sy, sxx, sxy = n[sl], sx[..., sl], sy[..., sl], sxx[..., sl], sxy[..., sl]
    b = (nn * sxy - sx * sy) / (nn * sxx - sx * sx)
    a = (sy - b * sx) / nn
    xi = x[..., first:]
    return a + b * xi, sy / nn, b


def lstsq_forecasts(x, y, first):
    out = []
    for i in range(first, len(y)):
        X = np.column_stack([np.ones(i), x[:i]])
        coef = np.linalg.lstsq(X, y[:i], rcond=None)[0]
        out.append(coef[0] + coef[1] * x[i])
    return np.array(out)


def ols_t(v):
    """t statistic of the mean of v (regression on a constant, ordinary standard error)."""
    v = np.asarray(v, float)
    return v.mean(axis=-1) / (v.std(axis=-1, ddof=1) / np.sqrt(v.shape[-1]))


def oos_stats(y, yhat_a, yhat_n):
    e_a, e_n = y - yhat_a, y - yhat_n
    mse_a, mse_n = np.mean(e_a**2), np.mean(e_n**2)
    p = len(y)
    f = e_n**2 - (e_a**2 - (yhat_n - yhat_a) ** 2)
    return {
        "P": p,
        "R2_OS": 1 - mse_a / mse_n,
        "dRMSE": np.sqrt(mse_n) - np.sqrt(mse_a),
        "MSE_F": p * (mse_n - mse_a) / mse_a,
        "ENC": np.sum(e_n * (e_n - e_a)) / mse_a,
        "CW_t": ols_t(f),
        "CW_mean": f.mean(),
        "adj": np.mean((yhat_n - yhat_a) ** 2),
        "mse_a": mse_a,
        "mse_n": mse_n,
    }


def adj_r2(r2, t, k=2):
    return 1 - (1 - r2) * (t - 1) / (t - k)


def ols_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    xc = x - x.mean()
    return np.sum(xc * (y - y.mean())) / np.sum(xc * xc)


# ---------------------------------------------------------------- data
annual = pd.read_csv(HERE / "goyal-annual-1871-2025.csv", comment="#").set_index("yyyy")
monthly = pd.read_csv(HERE / "goyal-monthly-1871-2025.csv", comment="#").set_index("yyyymm")

for frame, per_year in ((annual, 1), (monthly, 12)):
    shiller = (frame["Index"] + frame["D12"] / per_year) / frame["Index"].shift(1) - 1
    frame["R"] = frame["CRSP_SPvw"].where(frame["CRSP_SPvw"].notna(), shiller)
    frame["r"] = np.log1p(frame["R"])
    frame["dp"] = np.log(frame["D12"]) - np.log(frame["Index"])
    frame["pd"] = -frame["dp"]
    frame["dd"] = np.log(frame["D12"]).diff()
    frame["dp_lag"] = frame["dp"].shift(1)
annual["eqp"] = np.log1p(annual["R"]) - np.log1p(annual["Rfree"])
monthly["xr"] = monthly["R"] - monthly["Rfree"]
print(
    f"annual {annual.index[0]}-{annual.index[-1]}, monthly {monthly.index[0]}-{monthly.index[-1]}; "
    f"CRSP returns from {annual['CRSP_SPvw'].first_valid_index()} (annual), "
    f"{monthly['CRSP_SPvw'].first_valid_index()} (monthly)"
)

# ================================================================= A. present-value identity
print("\n== A. Campbell-Shiller log-linear identity, annual S&P 500 data")


def identity_parts(a):
    rho = 1 / (1 + np.exp(a["dp"].mean()))
    k = np.log1p(np.exp(-a["dp"].mean())) - rho * (-a["dp"].mean())
    approx = k + rho * a["pd"] - a["pd"].shift(1) + a["dd"]
    return rho, k, approx


exact = annual["dd"] - annual["pd"].shift(1) + np.log1p(np.exp(annual["pd"]))
gap = (annual["r"] - exact).loc[1872:1925].abs().max()
ok(
    "A1 exact identity r_t = dd_t - pd_{t-1} + log(1 + e^{pd_t}) for 1872-1925 (Index and D12 returns)",
    gap < 1e-12,
    f"max gap {gap:.1e}",
)
crsp_gap = (annual["r"] - exact).loc[1926:].abs().max()
print(
    f"     1926-2025 use CRSP returns, so the identity in Index and D12 holds only approximately there: max gap {crsp_gap:.4f}"
)

a_results = {}
for lo, hi in ((1872, 1986), (1872, 2025)):
    a = annual.loc[lo - 1 : hi].copy()
    rho, k, approx = identity_parts(a)
    r = a["r"].loc[lo:hi]
    err = r - approx.loc[lo:hi]
    vr = err.var() / r.var()
    corr = np.corrcoef(r, approx.loc[lo:hi])[0, 1]
    rho_wp = np.exp(-(r.mean() - a["dd"].loc[lo:hi].mean()))
    a_results[(lo, hi)] = (rho, vr, corr)
    print(
        f"     {lo}-{hi}: rho = {rho:.4f} from mean dp (working-paper point exp(-(mean r - mean dd)) = {rho_wp:.4f}); "
        f"mean error {err.mean():.4f}, sd(error)/sd(r) = {err.std() / r.std():.4f}, variance ratio {vr:.4f}, corr {corr:.4f}"
    )
    ok(
        f"A2 {lo}-{hi}: error variance below 0.5% of var(r) and correlation above 0.99",
        vr < 0.005 and corr > 0.99,
    )

a = annual.loc[1871:2025].copy()
rho, k, approx = identity_parts(a)
eps = (a["r"] - approx).to_numpy()
pd_, dd, rr = a["pd"].to_numpy(), a["dd"].to_numpy(), a["r"].to_numpy()
for J in (1, 5, 10, 20):
    worst = 0.0
    for t in range(0, len(a) - J):
        js = np.arange(1, J + 1)
        rebuilt = (
            np.sum(rho ** (js - 1) * (k + dd[t + js] - rr[t + js] + eps[t + js]))
            + rho**J * pd_[t + J]
        )
        worst = max(worst, abs(rebuilt - pd_[t]))
    ok(
        f"A3 iterating {J} years forward rebuilds pd_t with errors and terminal term kept",
        worst < 1e-10,
        f"max gap {worst:.1e}; terminal weight rho^J = {rho**J:.3f}",
    )

for lo, hi in ((1927, 2004), (1872, 2025)):
    s = annual.loc[lo - 1 : hi].copy()
    rho_s, k_s, approx_s = identity_parts(s)
    s["eps"] = s["r"] - approx_s
    w = s.loc[lo:hi]
    b_r, b_d = ols_slope(w["dp_lag"], w["r"]), ols_slope(w["dp_lag"], w["dd"])
    phi, b_e = ols_slope(w["dp_lag"], w["dp"]), ols_slope(w["dp_lag"], w["eps"])
    lhs = b_r - b_d + rho_s * phi
    ok(
        f"A4 {lo}-{hi}: b_r - b_d + rho*phi = 1 + b_eps",
        abs(lhs - (1 + b_e)) < 1e-10,
        f"b_r {b_r:.3f}, b_d {b_d:.3f}, phi {phi:.3f}, rho {rho_s:.4f}, b_eps {b_e:.4f}, b_r - b_d + rho*phi = {lhs:.4f}",
    )
    blr = b_r / (1 - rho_s * phi)
    print(
        f"     long-run return coefficient b_r/(1 - rho*phi) = {blr:.2f}, dividend-growth share -b_d/(1 - rho*phi) = {-b_d / (1 - rho_s * phi):.2f}"
    )

# ================================================================= B. nested forecast tests
print("\n== B1. hand example: recursive forecasts and the statistics' algebra")
x8 = np.array([3.0, 3.4, 2.9, 3.8, 3.1, 3.6, 4.0, 3.3])
y8 = np.array([0.4, 1.2, -0.3, 2.0, 0.1, 1.5, 0.9, -0.6])
first8 = 4
fa, fn, _ = recursive_forecasts(x8, y8, first8)
ok(
    "recursive OLS by running sums equals lstsq refitted at each origin",
    np.allclose(fa, lstsq_forecasts(x8, y8, first8), atol=1e-12, rtol=0),
)
ok(
    "historical-mean forecast equals the mean of earlier outcomes",
    np.allclose(fn, [y8[:i].mean() for i in range(first8, 8)], atol=1e-14, rtol=0),
)
st = oos_stats(y8[first8:], fa, fn)
e_a, e_n = y8[first8:] - fa, y8[first8:] - fn
ok(
    "Clark-West: mean f = MSE_N - (MSE_A - adj)",
    abs(st["CW_mean"] - (st["mse_n"] - (st["mse_a"] - st["adj"]))) < 1e-12,
)
ok(
    "Clark-West: mean f = 2 mean(e_N (e_N - e_A)) (eq. (4.1))",
    abs(st["CW_mean"] - 2 * np.mean(e_n * (e_n - e_a))) < 1e-12,
)
ok(
    "ENC = P mean(f) / (2 MSE_A)",
    abs(st["ENC"] - st["P"] * st["CW_mean"] / (2 * st["mse_a"])) < 1e-12,
)
ok("R2_OS and DeltaRMSE have the same sign", np.sign(st["R2_OS"]) == np.sign(st["dRMSE"]))
print("     forecasts A", np.round(fa, 4), "N", np.round(fn, 4))
print(
    f"     P {st['P']}, MSE_N {st['mse_n']:.4f}, MSE_A {st['mse_a']:.4f}, adj {st['adj']:.4f}, R2_OS {st['R2_OS']:.4f}, "
    f"MSE-F {st['MSE_F']:.4f}, ENC {st['ENC']:.4f}, CW mean {st['CW_mean']:.4f}, CW t {st['CW_t']:.4f}"
)

print("\n== B2. timing: overwriting the future leaves earlier forecasts unchanged")
rng_t = np.random.default_rng(7)
xt, yt = rng_t.normal(size=60), rng_t.normal(size=60)
base_a, base_n, _ = recursive_forecasts(xt, yt, 20)
for cut in (25, 40, 55):
    y2, x2 = yt.copy(), xt.copy()
    y2[cut:] = 1e6  # the forecast of y[cut] must not see y[cut] itself
    x2[
        cut + 1 :
    ] = -1e6  # x[i] is known before y[i]; forecasts of y[i], i <= cut, use x[i] and pairs before i
    a2, n2, _ = recursive_forecasts(x2, y2, 20)
    m = cut - 20 + 1
    ok(
        f"forecasts for periods up to {cut} unchanged",
        np.array_equal(a2[:m], base_a[:m]) and np.array_equal(n2[:m], base_n[:m]),
    )

print(
    "\n== B3. Monte Carlo, Clark and West's DGP 1 (eq. (6.1)), recursive, R = 120, 5,000 replications"
)
rng = np.random.default_rng(20261022)
REPS, R0 = 5000, 120


def simulate_dgp1(rng, reps, n, gamma):
    u1, u2 = rng.standard_normal((2, reps, n))
    v = np.sqrt(0.025) * u1
    e = np.sqrt(18.0) * (-0.75 * u1 + np.sqrt(1 - 0.75**2) * u2)
    z = np.empty((reps, n + 1))
    z[:, 0] = 3.0 + np.sqrt(0.025 / (1 - 0.95**2)) * rng.standard_normal(reps)
    for t in range(n):
        z[:, t + 1] = 0.15 + 0.95 * z[:, t] + v[:, t]
    y = 0.5 + gamma * z[:, :-1] + e  # y[t] uses z[t], which precedes it
    return z[:, :-1], y


def mc_rates(x, y, first):
    fa, fn, _ = recursive_forecasts(x, y, first)
    yy = y[:, first:]
    e_a, e_n = yy - fa, yy - fn
    d = e_n**2 - e_a**2
    f = d + (fn - fa) ** 2
    return d.mean(axis=1), ols_t(f), ols_t(d)


published = {120: (0.085, 0.028), 240: (0.070, 0.012)}
mc = {}
for P in (120, 240):
    x, y = simulate_dgp1(rng, REPS, R0 + P, 0.0)
    dmean, t_cw, t_n = mc_rates(x, y, R0)
    mc_t = dmean.mean() / (dmean.std(ddof=1) / np.sqrt(REPS))
    rej_cw, rej_n = np.mean(t_cw > 1.282), np.mean(t_n > 1.282)
    mc[P] = (rej_cw, rej_n)
    print(
        f"     P = {P}: mean MSE_N - MSE_A = {dmean.mean():.3f} (MC t {mc_t:.1f}); Clark-West size {rej_cw:.3f} (published {published[P][0]}); unadjusted {rej_n:.3f} (published {published[P][1]})"
    )
    ok(
        f"P = {P}: the unadjusted MSPE difference favours the historical mean under the null",
        mc_t < -5,
    )
    ok(
        f"P = {P}: Clark-West size in [0.04, 0.11] and within 0.02 of Clark and West",
        0.04 <= rej_cw <= 0.11 and abs(rej_cw - published[P][0]) <= 0.02,
    )
    ok(f"P = {P}: unadjusted test rejects in less than 3% of replications", rej_n < 0.03)
x, y = simulate_dgp1(rng, REPS, R0 + 240, 0.35)
_, t_cw, t_n = mc_rates(x, y, R0)
pow_cw, pow_n = np.mean(t_cw > 1.282), np.mean(t_n > 1.282)
ok(
    "gamma = 0.35, P = 240: Clark-West rejects more often than the unadjusted test",
    pow_cw > pow_n,
    f"{pow_cw:.3f} against {pow_n:.3f}",
)

print("\n== B4. Welch and Goyal's annual dividend-price row (data 1872-2005)")


def annual_oos(lo, hi, first_year):
    w = annual.loc[lo:hi]
    x, y = w["dp_lag"].to_numpy(), w["eqp"].to_numpy()
    first = int(np.where(w.index == first_year)[0][0])
    fa, fn, b = recursive_forecasts(x, y, first)
    return oos_stats(y[first:], fa, fn), b


w = annual.loc[1872:2005]
X = np.column_stack([np.ones(len(w)), w["dp_lag"]])
coef, res = np.linalg.lstsq(X, w["eqp"], rcond=None)[:2]
r2_is = 1 - res[0] / np.sum((w["eqp"] - w["eqp"].mean()) ** 2)
r2_is_adj = 100 * adj_r2(r2_is, len(w))
print(
    f"     in sample: slope {coef[1]:.4f}, R2 {100 * r2_is:.2f}%, adjusted {r2_is_adj:.2f}% (Welch and Goyal 0.49)"
)
ok("in-sample adjusted R2 within 0.25 points of 0.49", abs(r2_is_adj - 0.49) <= 0.25)
wg = {}
for first_year, pub_adj, pub_drmse in ((1892, -2.06, -0.11), (1965, -3.69, -0.09)):
    s, _ = annual_oos(1872, 2005, first_year)
    wg[first_year] = s
    adj = 100 * adj_r2(s["R2_OS"], s["P"])
    print(
        f"     forecasts from {first_year}: P {s['P']}, R2_OS {100 * s['R2_OS']:.2f}%, adjusted {adj:.2f}% (published {pub_adj}), "
        f"DeltaRMSE {100 * s['dRMSE']:.2f} (published {pub_drmse}), MSE-F {s['MSE_F']:.2f}, ENC {s['ENC']:.2f}, Clark-West t {s['CW_t']:.2f}"
    )
    ok(
        f"forecasts from {first_year}: DeltaRMSE within 0.05 points of {pub_drmse}",
        abs(100 * s["dRMSE"] - pub_drmse) <= 0.05,
    )

print("\n== B5. start-date sensitivity (reported only)")
for hi in (2005, 2025):
    for first_year in (1892, 1927, 1947, 1965, 1985):
        s, b = annual_oos(1872, hi, first_year)
        print(
            f"     {first_year}-{hi}: P {s['P']:3d}, R2_OS {100 * s['R2_OS']:6.2f}%, Clark-West t {s['CW_t']:5.2f}, slope range {b.min():.3f} to {b.max():.3f}"
        )

# ================================================================= C. restricted forecasts and economic value
print("\n== C1. hand example: weights, portfolio returns and utility")
GAMMA, W_MAX = 3.0, 1.5
mu = np.array([0.006, -0.002, 0.030])
var = np.array([0.0020, 0.0020, 0.0018])
r_m = np.array([0.020, -0.050, 0.010])
r_f = np.array([0.003, 0.003, 0.003])
wts = np.clip(mu / (GAMMA * var), 0.0, W_MAX)
ok(
    "weights 1.0, 0 (no short sales) and 1.5 (leverage cap)",
    np.allclose(wts, [1.0, 0.0, 1.5], atol=1e-12, rtol=0),
    str(np.round(mu / (GAMMA * var), 4)),
)
rp = r_f + wts * (r_m - r_f)
ok(
    "portfolio returns 0.020, 0.003 and 0.0135",
    np.allclose(rp, [0.020, 0.003, 0.0135], atol=1e-12, rtol=0),
)
u = rp.mean() - GAMMA / 2 * rp.var(ddof=1)
ok(
    "utility = mean - (gamma/2) var",
    abs(u - (0.0365 / 3 - 1.5 * np.sum((rp - 0.0365 / 3) ** 2) / 2)) < 1e-15,
    f"{100 * u:.4f}% a month",
)


def ct_run(hi, first_ym=192701):
    m = monthly.loc[187102:hi]
    x, y = m["dp_lag"].to_numpy(), m["xr"].to_numpy()
    first = int(np.where(m.index == first_ym)[0][0])
    fa, fn, b = recursive_forecasts(x, y, first)
    fr = np.where(b < 0, fn, fa)  # wrong (negative) slope: drop the predictor, keep the mean
    fr = np.maximum(fr, 0.0)
    fn_floor = np.maximum(fn, 0.0)
    var_hist = np.array([y[:i].var(ddof=1) for i in range(first, len(y))])
    yy, rf = y[first:], m["Rfree"].to_numpy()[first:]

    def utility(fc):
        wv = np.clip(fc / (GAMMA * var_hist), 0.0, W_MAX)
        rp = rf + wv * yy
        return rp.mean() - GAMMA / 2 * rp.var(ddof=1), wv

    u_n, w_n = utility(fn)
    u_a, w_a = utility(fa)
    u_r, w_r = utility(fr)
    return {
        "P": len(yy),
        "R2_unres": oos_stats(yy, fa, fn)["R2_OS"],
        "R2_res": oos_stats(yy, fr, fn_floor)["R2_OS"],
        "u_mean": u_n,
        "du_unres": u_a - u_n,
        "du_res": u_r - u_n,
        "share_neg_slope": np.mean(b < 0),
        "share_zero_weight": np.mean(w_r == 0),
        "share_capped": np.mean(w_r == W_MAX),
        "mean_w": (w_n.mean(), w_a.mean(), w_r.mean()),
    }


print(
    "\n== C2. Campbell and Thompson's dividend-price comparison, monthly, forecasts 1927-2003, gamma = 3, weights in [0, 1.5]"
)
ct = ct_run(200312)
print(
    f"     P {ct['P']}; R2_OS unrestricted {100 * ct['R2_unres']:.3f}%, restricted {100 * ct['R2_res']:.3f}% (published, restricted: 0.001%)\n"
    f"     utility of the historical-mean investor {100 * ct['u_mean']:.3f}% a month (published 0.501%); change unrestricted "
    f"{100 * ct['du_unres']:+.3f}% (published -0.016%), restricted {100 * ct['du_res']:+.3f}% (published -0.024%)\n"
    f"     negative slope in {100 * ct['share_neg_slope']:.1f}% of months; restricted weight 0 in {100 * ct['share_zero_weight']:.1f}%, "
    f"at 1.5 in {100 * ct['share_capped']:.1f}%; mean weights (mean, unrestricted, restricted) {np.round(ct['mean_w'], 3)}"
)
ok(
    "historical-mean investor's utility within 0.05 points of 0.501% a month",
    abs(100 * ct["u_mean"] - 0.501) <= 0.05,
)
ok(
    "both utility changes within 0.05 points of zero",
    abs(100 * ct["du_unres"]) <= 0.05 and abs(100 * ct["du_res"]) <= 0.05,
)

print("\n== C3. extended to December 2025 (reported only)")
ct25 = ct_run(202512)
print(
    f"     P {ct25['P']}; R2_OS unrestricted {100 * ct25['R2_unres']:.3f}%, restricted {100 * ct25['R2_res']:.3f}%; "
    f"utility {100 * ct25['u_mean']:.3f}%, change unrestricted {100 * ct25['du_unres']:+.3f}%, restricted {100 * ct25['du_res']:+.3f}%"
)

print(
    "\n== C4. synthetic mechanism: DGP 1 in monthly decimals, gamma* = 0.35, R = 240, P = 480, 1,000 replications"
)
rng_c = np.random.default_rng(20261023)
xs, ys = simulate_dgp1(rng_c, 1000, 240 + 480, 0.35)
ys = ys / 100
fa, fn, b = recursive_forecasts(xs, ys, 240)
fr = np.maximum(np.where(b < 0, fn, fa), 0.0)
# variance of the outcomes observed before each forecast month (positions 239, ..., 718 hold 240, ..., 719 outcomes)
csum, csum2 = np.cumsum(ys, axis=1)[:, 239:-1], np.cumsum(ys**2, axis=1)[:, 239:-1]
nobs = np.arange(240, ys.shape[1])
var_h = (csum2 - csum**2 / nobs) / (nobs - 1)
yy = ys[:, 240:]


def util(fc, yy, var_h):
    wv = np.clip(fc / (GAMMA * var_h), 0.0, W_MAX)
    rp = wv * yy
    return rp.mean(axis=1) - GAMMA / 2 * rp.var(axis=1, ddof=1), np.mean(wv == W_MAX)


(u_a, cap_a), (u_r, _), (u_n, cap_n) = (util(f, yy, var_h) for f in (fa, fr, fn))
g_unres, g_res = u_a - u_n, u_r - u_n
print(
    f"     mean gain over the historical mean, % a month: unrestricted {100 * g_unres.mean():.4f}, restricted {100 * g_res.mean():.4f}; "
    f"share of samples with a gain: {np.mean(g_unres > 0):.3f}, {np.mean(g_res > 0):.3f}\n"
    f"     diagnostic added after the first run: weight at the 1.5 cap in {100 * cap_n:.1f}% of months (historical mean) and "
    f"{100 * cap_a:.1f}% (unrestricted); DGP 1's mean excess return, 0.5 + 0.35 x 3 = 1.55% a month against a variance of 18 "
    f"(percent squared), asks for a weight near 2.9, so the cap binds and the predictor can hardly be used"
)

# Supplement added after the first run (not in the protocol's verdicts): the same design with the intercept
# lowered so that the mean excess return is 0.5% a month, close to the historical monthly premium.
print(
    "\n== C5. post-run supplement: C4 with a mean excess return of 0.5% a month (intercept -0.55), seed 20261024"
)
rng_s = np.random.default_rng(20261024)
xs5, ys5 = simulate_dgp1(rng_s, 1000, 240 + 480, 0.35)
ys5 = (ys5 - 1.05) / 100
fa5, fn5, b5 = recursive_forecasts(xs5, ys5, 240)
fr5 = np.maximum(np.where(b5 < 0, fn5, fa5), 0.0)
c1, c2 = np.cumsum(ys5, axis=1)[:, 239:-1], np.cumsum(ys5**2, axis=1)[:, 239:-1]
var5 = (c2 - c1**2 / nobs) / (nobs - 1)
yy5 = ys5[:, 240:]
(u_a5, cap_a5), (u_r5, _), (u_n5, cap_n5) = (util(f, yy5, var5) for f in (fa5, fr5, fn5))
g5u, g5r = u_a5 - u_n5, u_r5 - u_n5
print(
    f"     mean gain, % a month: unrestricted {100 * g5u.mean():.4f}, restricted {100 * g5r.mean():.4f}; share with a gain "
    f"{np.mean(g5u > 0):.3f}, {np.mean(g5r > 0):.3f}; restricted better than unrestricted in {np.mean(g5r > g5u):.3f} of samples; "
    f"tied in {np.mean(g5r == g5u):.3f}; cap binds in {100 * cap_n5:.1f}% and {100 * cap_a5:.1f}% of months"
)
var_x = 0.35**2 * 0.025 / (1 - 0.95**2)  # variance of the predictable part, percent squared
pop_r2, pop_s2 = var_x / (var_x + 18), 0.5**2 / (var_x + 18)
bench = (
    (1 / (2 * GAMMA)) * pop_r2 / (1 - pop_r2) * (1 + pop_s2)
)  # R2 and S2 are unit-free, so this is a decimal return
print(
    f"     population R2 {pop_r2:.4f}, S2 {pop_s2:.4f}; known-parameter, uncapped utility gain (1/(2gamma))(R2/(1-R2))(1+S2) = "
    f"{100 * bench:.4f}% a month (half the expected-return gain of Campbell and Thompson's eq. (8); a conditional\n"
    "     mean-variance reference: the realised measure above also counts the variation of the timed mean, so it is lower)"
)
xs2, ys2 = xs[:1].copy(), ys[:1].copy()
ys2[0, 400:] = 9.0
fa2, fn2, _ = recursive_forecasts(xs2, ys2, 240)
ok(
    "C4 timing: forecasts before the overwritten months are unchanged",
    np.array_equal(fa2[0, : 400 - 240], fa[0, : 400 - 240])
    and np.array_equal(fn2[0, : 400 - 240], fn[0, : 400 - 240]),
)

print(
    "\n== Recorded values (added after the first run, 2026-10-22, to detect drift; no tolerance was changed)"
)
ok(
    "A: variance ratios 0.0023 (1872-1986) and 0.0025 (1872-2025); rho 0.9547 and 0.9634",
    [round(v[1], 4) for v in a_results.values()] == [0.0023, 0.0025]
    and [round(v[0], 4) for v in a_results.values()] == [0.9547, 0.9634],
)
ok(
    "B3: Clark-West sizes 0.069 and 0.059; unadjusted 0.023 and 0.010; power 0.156 against 0.033",
    [round(v, 3) for v in (*mc[120], *mc[240], pow_cw, pow_n)]
    == [0.069, 0.023, 0.059, 0.010, 0.156, 0.033],
)
ok(
    "B4: R2_OS -1.32% and -1.67%; DeltaRMSE -0.13 and -0.13; Clark-West t 0.26 and 0.46",
    [round(100 * wg[y]["R2_OS"], 2) for y in (1892, 1965)] == [-1.32, -1.67]
    and [round(100 * wg[y]["dRMSE"], 2) for y in (1892, 1965)] == [-0.13, -0.13]
    and [round(wg[y]["CW_t"], 2) for y in (1892, 1965)] == [0.26, 0.46],
)
ok(
    "C2/C3: utility 0.492%, changes -0.018% and -0.024%; to 2025 0.517%, -0.051% and -0.055%",
    [
        round(100 * v, 3)
        for v in (
            ct["u_mean"],
            ct["du_unres"],
            ct["du_res"],
            ct25["u_mean"],
            ct25["du_unres"],
            ct25["du_res"],
        )
    ]
    == [0.492, -0.018, -0.024, 0.517, -0.051, -0.055],
)
ok(
    "C5: mean gains 0.0171% and 0.0214% a month",
    [round(100 * g5u.mean(), 4), round(100 * g5r.mean(), 4)] == [0.0171, 0.0214],
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
