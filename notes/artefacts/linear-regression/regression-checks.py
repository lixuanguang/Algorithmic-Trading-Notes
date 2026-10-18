"""Batch 2 regression foundations (2026-10-18): the worked example of meth:simple-regression-estimation,
meth:regression-diagnostics-anova and meth:regression-prediction-functional-form.

Declared sampling model: ten invented corporate bonds with fixed leverage x = 20, 25, ..., 65 (debt over assets,
percent) and credit spread y (basis points) generated as y = 40 + 5 x + e, e independent N(0, 30^2), first draw
of seed 20261018 + 11, rounded to whole basis points. The seed was fixed before the run and not changed.

Each result is computed by the closed-form formulas in the entries and by an independent route (statsmodels OLS,
its ANOVA table and prediction intervals, numpy least squares, or a seeded simulation under the declared model
compared within four standard errors). Retransformation checks use the lognormal mean and Duan's smearing
estimate. All data are invented for illustration.

Correction pass (2026-10-18): adds the matching-null check (F = t^2 for beta1 = 0 only; the t for beta1 = 5
squares to the F of that restriction), the fractional and percentage log-log change, the geometric-mean identity
and a mean-zero skewed log error that separates geometric mean, median and mean. No seed or data were changed.
Second correction (2026-10-18): the x_i = 2^-i design, full rank in every sample yet Sxx -> 1/3, so the slope
variance tends to 3 sigma^2 and least squares is not consistent without an asymptotically nondegenerate design.

Run: uv run python regression-checks.py   (numpy, scipy, statsmodels). Exits 1 on failure.
"""

# standard library imports
import math
import sys
from fractions import Fraction

# third party library imports
import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import integrate, stats
from statsmodels.stats.anova import anova_lm

print(
    f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}, "
    f"statsmodels {statsmodels.__version__}"
)
fails = []
SEED = 20261018


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


print("== data from the declared model")
x = np.arange(20, 70, 5).astype(float)
y = np.round(40 + 5 * x + np.random.default_rng(SEED + 11).normal(0, 30, x.size))
ok(
    "spreads as printed in the entry",
    np.array_equal(y, [102, 216, 229, 240, 222, 197, 265, 326, 388, 349]),
)
n = len(x)

print("== least squares estimates (hand route)")
xb, yb = x.mean(), y.mean()
Sxx = ((x - xb) ** 2).sum()
Sxy = ((x - xb) * (y - yb)).sum()
b1 = Sxy / Sxx
b0 = yb - b1 * xb
fit = b0 + b1 * x
e = y - fit
ok(
    "x mean 42.5, y mean 253.4, Sxx 2,062.5, Sxy 9,905",
    close(xb, 42.5) and close(yb, 253.4) and close(Sxx, 2062.5) and close(Sxy, 9905),
)
ok(
    "slope 4.8024 bp per pp, intercept 49.297 bp",
    close(b1, 4.802424, 1e-6) and close(b0, 49.29697, 1e-5),
)
ok(
    "residuals sum to zero and are orthogonal to x; line passes through the means",
    close(e.sum(), 0, 1e-9) and close((x * e).sum(), 0, 1e-8) and close(b0 + b1 * xb, yb, 1e-9),
)
ok(
    "residuals -43.35 ... -12.45 as printed",
    np.allclose(
        np.round(e, 2), [-43.35, 46.64, 35.63, 22.62, -19.39, -68.41, -24.42, 12.57, 50.56, -12.45]
    ),
)
grid = np.linspace(b1 - 1, b1 + 1, 2001)
sse_grid = [((y - (yb - g * xb) - g * x) ** 2).sum() for g in grid]
ok(
    "least squares criterion is minimised at the formula slope",
    close(grid[int(np.argmin(sse_grid))], b1, 1e-3),
)

print("== independent routes: numpy least squares and statsmodels")
X = sm.add_constant(x)
coef, *_ = np.linalg.lstsq(X, y, rcond=None)
m = sm.OLS(y, X).fit()
ok("numpy lstsq agrees", np.allclose(coef, [b0, b1], atol=1e-9))
ok("statsmodels OLS agrees", np.allclose(m.params, [b0, b1], atol=1e-9))

print("== sums of squares, fit and coefficient tests")
SSE = (e**2).sum()
SST = ((y - yb) ** 2).sum()
SSR = ((fit - yb) ** 2).sum()
s = math.sqrt(SSE / (n - 2))
R2 = SSR / SST
ok(
    "SSE 14,356.4 + SSR 47,568.0 = SST 61,924.4",
    close(SSE, 14356.388, 1e-3) and close(SSR, 47568.012, 1e-3) and close(SSE + SSR, SST, 1e-8),
)
ok(
    "standard error of estimate s = sqrt(SSE/(n-2)) = 42.36 bp; R^2 = 0.768 = r^2",
    close(s, 42.36211, 1e-5)
    and close(R2, 0.768163, 1e-6)
    and close(np.corrcoef(x, y)[0, 1] ** 2, R2, 1e-12),
)
se1 = s / math.sqrt(Sxx)
se0 = s * math.sqrt(1 / n + xb**2 / Sxx)
t1, t0 = b1 / se1, b0 / se0
p1 = 2 * stats.t.sf(abs(t1), n - 2)
ok(
    "se(b1) 0.9328, t 5.148, p 0.00088; se(b0) 41.85, t 1.178, p 0.273",
    close(se1, 0.932783, 1e-6)
    and close(t1, 5.148490, 1e-5)
    and close(p1, 0.000876, 1e-6)
    and close(se0, 41.8455, 1e-4)
    and close(t0, 1.178072, 1e-5)
    and close(2 * stats.t.sf(t0, n - 2), 0.272621, 1e-5),
)
ok(
    "statsmodels standard errors, t values and p values agree",
    np.allclose(m.bse, [se0, se1])
    and np.allclose(m.tvalues, [t0, t1])
    and close(m.pvalues[1], p1, 1e-12),
)
tc = stats.t.ppf(0.975, n - 2)
ok(
    "95% interval for the slope 2.65 to 6.95 excludes 0; t multiplier 2.306 on 8 d.f.",
    close(tc, 2.306004, 1e-6)
    and close(b1 - tc * se1, 2.6514, 1e-4)
    and close(b1 + tc * se1, 6.9534, 1e-4)
    and np.allclose(m.conf_int()[1], [b1 - tc * se1, b1 + tc * se1]),
)
t5 = (b1 - 5) / se1
ok(
    "test of beta1 = 5 (the generating value): t -0.212, not rejected",
    close(t5, -0.211814, 1e-5) and abs(t5) < tc,
)

print("== simple-regression ANOVA and F = t^2")
MSR, MSE = SSR / 1, SSE / (n - 2)
F = MSR / MSE
pF = stats.f.sf(F, 1, n - 2)
aov = anova_lm(smf.ols("spread ~ leverage", data=pd.DataFrame({"spread": y, "leverage": x})).fit())
ok(
    "MSR 47,568.0, MSE 1,794.5, F 26.507 on (1, 8) d.f.",
    close(MSR, 47568.012, 1e-3) and close(MSE, 1794.548, 1e-3) and close(F, 26.506953, 1e-5),
)
ok("F equals the squared slope t statistic", close(F, t1**2, 1e-9))
ok("ANOVA p equals the two-sided t p-value", close(pF, p1, 1e-12))
ok(
    "statsmodels ANOVA table agrees (sums of squares, F, p) and so does its model F",
    close(aov["sum_sq"].iloc[0], SSR, 1e-6)
    and close(aov["sum_sq"].iloc[1], SSE, 1e-6)
    and close(aov["F"].iloc[0], F, 1e-9)
    and close(m.fvalue, F, 1e-9),
)
ok(
    "R^2 = SSR/SST = 1 - SSE/SST, and F = R^2 (n-2)/(1-R^2)",
    close(F, R2 * (n - 2) / (1 - R2), 1e-9),
)
# F = t^2 only for the same null: the ANOVA F tests beta1 = 0; the t for beta1 = 5 squares to that null's F.
f5 = m.f_test((np.array([[0.0, 1.0]]), np.array([5.0])))
ok(
    "test of beta1 = 5: t^2 = 0.044865 is the F of that restriction, not the ANOVA F of 26.507",
    close(t5**2, 0.044865, 1e-6)
    and close(float(np.squeeze(f5.fvalue)), t5**2, 1e-9)
    and close(float(f5.pvalue), 2 * stats.t.sf(abs(t5), n - 2), 1e-12)
    and not close(t5**2, F, 1.0),
)

# Full rank in every sample does not give consistency: with x_i = 2^-i, Sxx tends to 1/3, so Var(b1) = sigma^2/Sxx
# tends to 3 sigma^2. Exact rational arithmetic against the closed form and numpy.
sxx_closed = {
    k: Fraction(1, 3) * (1 - Fraction(1, 4**k)) - (1 - Fraction(1, 2**k)) ** 2 / k
    for k in (2, 10, 40, 60, 200)
}
sxx_direct = {}
for k in sxx_closed:
    xs = [Fraction(1, 2**i) for i in range(1, k + 1)]
    xm = sum(xs) / k
    sxx_direct[k] = sum((v - xm) ** 2 for v in xs)
xs60 = 2.0 ** -np.arange(1, 61)
ok(
    "x_i = 2^-i: Sxx > 0 for every n (full rank) but Sxx -> 1/3, so Var(b1)/sigma^2 -> 3, not 0",
    all(sxx_direct[k] == sxx_closed[k] and sxx_closed[k] > 0 for k in sxx_closed)
    and abs(float(sxx_closed[200]) - 1 / 3) < 0.0051
    and close(1 / float(sxx_closed[200]), 3.0, 0.05)
    and close(((xs60 - xs60.mean()) ** 2).sum(), float(sxx_closed[60]), 1e-12)
    and sxx_closed[200] < Fraction(1, 3),
    f"Sxx at n = 10, 40, 200: {float(sxx_closed[10]):.4f}, {float(sxx_closed[40]):.4f}, {float(sxx_closed[200]):.4f}",
)

print("== residual diagnostics")
std_res = e / s
ok(
    "largest standardised residual (e/s) is -1.61 at x = 45; none beyond +/-2",
    close(std_res.min(), -1.614793, 1e-5) and np.argmin(std_res) == 5 and np.abs(std_res).max() < 2,
)
ok(
    "internally studentised residuals from statsmodels stay inside +/-2",
    np.abs(m.get_influence().resid_studentized_internal).max() < 2,
)
# High R^2 without a correct linear form: an exact quadratic on the same x has R^2 above 0.9 for a line.
yq = 0.2 * (x - 10) ** 2
mq = sm.OLS(yq, X).fit()
rq = mq.resid
ok(
    "a curved relation fitted by a line: R^2 0.96 yet residuals positive, negative, positive",
    mq.rsquared > 0.95 and rq[0] > 0 and rq[n // 2] < 0 and rq[-1] > 0,
    f"R^2 {mq.rsquared:.3f}",
)

print("== predictions: interval for the mean against interval for a new bond")


def intervals(xh):
    yh = b0 + b1 * xh
    se_fit = s * math.sqrt(1 / n + (xh - xb) ** 2 / Sxx)
    se_pred = s * math.sqrt(1 + 1 / n + (xh - xb) ** 2 / Sxx)
    return yh, se_fit, se_pred


yh, sf, sp = intervals(45)
ok(
    "at 45%: prediction 265.4 bp; s.e. of fit 13.60; s.e. of prediction 44.49",
    close(yh, 265.4061, 1e-4) and close(sf, 13.59753, 1e-4) and close(sp, 44.49092, 1e-4),
)
ok("prediction variance = s^2 + (s.e. of fit)^2", close(sp**2, s**2 + sf**2, 1e-8))
ok(
    "95% interval for the mean 234.1-296.8; for a new bond 162.8-368.0",
    close(yh - tc * sf, 234.0494, 1e-3)
    and close(yh + tc * sf, 296.7627, 1e-3)
    and close(yh - tc * sp, 162.8098, 1e-3)
    and close(yh + tc * sp, 368.0024, 1e-3),
)
frame = m.get_prediction(np.array([[1.0, 45.0]])).summary_frame(alpha=0.05)
ok(
    "statsmodels mean_ci and obs_ci agree",
    np.allclose(frame[["mean_ci_lower", "mean_ci_upper"]].values, [[yh - tc * sf, yh + tc * sf]])
    and np.allclose(frame[["obs_ci_lower", "obs_ci_upper"]].values, [[yh - tc * sp, yh + tc * sp]]),
)
yh90, sf90, sp90 = intervals(90)
ok(
    "extrapolation to 90%: prediction 481.5, s.e. of fit 46.29 (3.4 times that at 45), PI 336.8-626.2",
    close(yh90, 481.5152, 1e-3)
    and close(sf90 / sf, 3.404, 1e-3)
    and close(yh90 - tc * sp90, 336.82, 1e-2)
    and close(yh90 + tc * sp90, 626.21, 1e-2),
)
# Coverage under the declared model, simulated: the mean interval covers E[y|45] = 265; the prediction interval
# covers a new y at 45; the mean interval used for a new y covers far less.
rng = np.random.default_rng(SEED + 12)
R = 20_000
Y = 40 + 5 * x + rng.normal(0, 30, (R, n))
Ynew = 40 + 5 * 45 + rng.normal(0, 30, R)
B1 = ((x - xb) * (Y - Y.mean(1, keepdims=True))).sum(1) / Sxx
B0 = Y.mean(1) - B1 * xb
S = np.sqrt(((Y - B0[:, None] - B1[:, None] * x) ** 2).sum(1) / (n - 2))
YH = B0 + B1 * 45
SF = S * math.sqrt(1 / n + (45 - xb) ** 2 / Sxx)
SP = S * math.sqrt(1 + 1 / n + (45 - xb) ** 2 / Sxx)
cov_mean = np.mean(np.abs(YH - 265) <= tc * SF)
cov_pred = np.mean(np.abs(Ynew - YH) <= tc * SP)
cov_wrong = np.mean(np.abs(Ynew - YH) <= tc * SF)
band = 4 * math.sqrt(0.05 * 0.95 / R)
ok(
    "simulated coverage of the mean interval is 95% within 4 s.e.",
    abs(cov_mean - 0.95) <= band,
    f"{cov_mean:.4f}",
)
ok(
    "simulated coverage of the prediction interval is 95% within 4 s.e.",
    abs(cov_pred - 0.95) <= band,
    f"{cov_pred:.4f}",
)
k_fit = math.sqrt(1 / n + (45 - xb) ** 2 / Sxx)
exact_wrong = 2 * stats.t.cdf(tc * k_fit / math.sqrt(1 + k_fit**2), n - 2) - 1
ok(
    "the mean interval covers a new bond's spread only 49.9% of the time (exact t8 value; simulated within 4 s.e.)",
    close(exact_wrong, 0.499049, 1e-6)
    and abs(cov_wrong - exact_wrong) <= 4 * math.sqrt(exact_wrong * (1 - exact_wrong) / R),
    f"{cov_wrong:.4f}",
)

print("== functional forms and retransformation")
ml = sm.OLS(np.log(y), X).fit()
c0, c1 = ml.params
s2l = ml.mse_resid
ok(
    "log-level: ln(spread) = 4.5967 + 0.020745 leverage; s^2 = 0.04718",
    close(c0, 4.596656, 1e-6) and close(c1, 0.020745, 1e-6) and close(s2l, 0.047178, 1e-6),
)
ok(
    "+1 pp leverage multiplies the geometric-mean spread by e^b1 = 1.0210 (+2.1%)",
    close(math.exp(c1), 1.020962, 1e-6),
)
lh = c0 + c1 * 45
med = math.exp(lh)
mean_ln = math.exp(lh + s2l / 2)
smear = med * np.mean(np.exp(ml.resid))
ok(
    "at 45%: geometric mean 252.2 bp (median if log errors have median 0); normal-theory mean 258.2; smearing 256.8",
    close(med, 252.1899, 1e-3) and close(mean_ln, 258.2096, 1e-3) and close(smear, 256.8127, 1e-3),
)
ok(
    "exp(fitted log) is a geometric mean: at mean leverage it equals the sample geometric mean 239.44 (scipy gmean)",
    close(math.exp(c0 + c1 * xb), stats.gmean(y), 1e-9) and close(stats.gmean(y), 239.444049, 1e-5),
)
# A mean-zero but skewed log error separates the geometric mean, the median and the mean:
# eps = 0.5 (E - 1), E standard exponential; factors relative to exp(x beta).
sk = 0.5
gm_k, med_k = (
    math.exp(stats.expon.expect(lambda u: sk * (u - 1))),
    math.exp(sk * (stats.expon.median() - 1)),
)
mean_k = integrate.quad(lambda u: np.exp(sk * (u - 1) - u), 0, np.inf)[0]
ok(
    "skewed mean-zero log error (var 0.25): geometric mean 1, median 0.8578, mean 1.2131, normal-theory 1.1331",
    close(gm_k, 1.0, 1e-9)
    and close(med_k, math.exp(sk * (math.log(2) - 1)), 1e-12)
    and close(med_k, 0.857764, 1e-6)
    and close(mean_k, math.exp(-sk) / (1 - sk), 1e-9)
    and close(mean_k, 1.213061, 1e-6)
    and close(stats.expon.var() * sk**2, 0.25, 1e-12)
    and close(math.exp(0.25 / 2), 1.133148, 1e-6),
)
ok(
    "there exp(E log Y) overstates the median by 16.6% and understates the mean by 17.6%; normal theory 6.6% low",
    close(gm_k / med_k - 1, 0.165822, 1e-6)
    and close(1 - gm_k / mean_k, 0.175639, 1e-6)
    and close(1 - math.exp(0.25 / 2) / mean_k, 0.065877, 1e-6),
)
ok(
    "smearing estimate is the average of exp(fitted log + each residual) (Duan eq. 3.1)",
    close(smear, np.mean(np.exp(lh + ml.resid)), 1e-9),
)
ok(
    "lognormal identity: median e^mu, mean e^(mu + sigma^2/2) (scipy lognorm)",
    close(stats.lognorm(s=0.3, scale=math.exp(1.2)).median(), math.exp(1.2), 1e-12)
    and close(stats.lognorm(s=0.3, scale=math.exp(1.2)).mean(), math.exp(1.2 + 0.045), 1e-12),
)
mix = 0.995 * math.exp(0.475) + 0.005 * math.exp(5.475)
ok(
    "Duan's mixture: E e^eps = 2.79 against the normal-theory 1.65, a 41% asymptotic bias",
    close(mix, 2.7930, 1e-3)
    and close(math.exp(0.5), 1.6487, 1e-4)
    and close(1 - math.exp(0.5) / mix, 0.4097, 1e-3),
)
mll = sm.OLS(np.log(y), sm.add_constant(np.log(x))).fit()
mlv = sm.OLS(y, sm.add_constant(np.log(x))).fit()
pct_ll = 100 * (1.01 ** mll.params[1] - 1)
ok(
    "log-log elasticity 0.826: +1% leverage gives 100 (1.01^b1 - 1) = 0.825153% (fraction 0.00825153), about b1 %",
    close(mll.params[1], 0.825869, 1e-6)
    and close(1.01 ** mll.params[1] - 1, 0.00825153, 1e-8)
    and close(pct_ll, 0.825153, 1e-6)
    and abs(pct_ll - mll.params[1]) < 0.001,
)
ok(
    "level-log slope 183.9: +1% leverage adds about b1 ln(1.01) = 1.83 bp",
    close(mlv.params[1], 183.89108, 1e-4) and close(mlv.params[1] * math.log(1.01), 1.829777, 1e-5),
)
ok(
    "R^2 0.768 (level), 0.702 (log-level), 0.747 (level-log), 0.737 (log-log): different responses, not comparable",
    close(ml.rsquared, 0.701648, 1e-6)
    and close(mlv.rsquared, 0.746514, 1e-6)
    and close(mll.rsquared, 0.737051, 1e-6),
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
