"""Numerical checks for migration slice 36 (market making, information and volatility, and the
feature- and data-engineering files; the legacy execution-market-making chapter closed), 2026-10-16.

Run with numpy and scipy:  /opt/homebrew/bin/python3.10 slice36-checks.py
Each section prints its result and asserts what the entries state.

1. Harris's inside spread (Table 13-1, p. 281) (def:dealer-quotes-order-flow).
2. Cyclic currency arbitrage: Harris's box (p. 357) recomputed, and the no-arbitrage band with
   bid and ask quotes (def:arbitrage).
3. Make/take fees and the speed race: Lehalle and Laruelle's eq. (A.4), after Foucault, Kadan and
   Kandel, re-derived and checked against a finite-population equilibrium (mod:make-take-fee-speed-race).
4. The toy flash-crash model (Lehalle and Laruelle, app. A.5): the hot-potato rate, the overflow,
   and the time term of eq. (A.14) (mod:depth-overflow-flash-crash).
5. The May 2010 report's arithmetic (ev:may-2010-flash-crash).
6. Queue-position values in Moallemi and Yuan's Table 3 (res:queue-position-value).
7. Proportion intervals: the normal (Wald) interval against Wilson's, and the rule of thumb
   (meth:venue-market-share).
8. Harris's t-test power and data requirements (Tables 22-2 and 22-3), sampling frequency, the
   best of many managers, regression to the mean and a short-volatility return stream
   (meth:skill-luck-significance-tests).
9. Regression fit, R^2 definitions, and the averaging effect: index spreads and volatilities, and
   the regression of averages against the average of regressions (meth:spread-volatility-regression,
   meth:intraday-deseasonalisation).
10. A spread's factor exposure with a hedge ratio (res:arbitrage-risks).
"""
import numpy as np
from scipy import optimize, stats

rng = np.random.default_rng(36)


def section(title):
    print("\n== " + title)


# 1. Inside spread ------------------------------------------------------------------------
section("1. Harris's inside spread (Table 13-1)")
quotes = {"Charles": (99.9, 100.4), "Cheryl": (100.0, 100.5), "Goldie": (100.1, 100.6),
          "Larry": (100.2, 100.7), "Teri": (100.3, 100.8)}
best_bid = max(b for b, a in quotes.values())
best_ask = min(a for b, a in quotes.values())
spreads = [round(a - b, 10) for b, a in quotes.values()]
print(f"  each dealer's spread {set(spreads)}; inside {best_bid} / {best_ask}, inside spread {best_ask - best_bid:.1f}")
assert abs(best_ask - best_bid - 0.1) < 1e-9 and best_ask - best_bid <= min(spreads)


# 2. Cyclic currency arbitrage -----------------------------------------------------------
section("2. cyclic (triangular) currency arbitrage")
usdjpy, eurusd = 110.0, 1.10                  # yen per dollar; dollars per euro
implied = usdjpy * eurusd                     # yen per euro
print(f"  Harris's box: 110 yen per dollar and 1.10 dollars per euro imply {implied:.0f} yen per euro, not the printed 100")
assert abs(implied - 121.0) < 1e-9
# the box's cycle with its own numbers: buy $1.10m for 100m yen, buy 1m euro for $1.10m, buy 99.9m yen for 1m euro
yen = 100.0
usd = 1.10                                    # bought for the 100m yen
eur = usd / 1.10                              # bought for the dollars
yen_end = eur * 99.9                          # yen bought for the euros
print(f"  the box's cycle as printed: start 100m yen, end {yen_end:.1f}m yen: a loss of {100 - yen_end:.1f}m; "
      f"it buys euros at the implied rate and sells them where they are cheap")
assert abs(yen_end - 99.9) < 1e-9
# a consistent example: direct euro quote 120.9 yen below the implied 121
start = 120.9
eur = 1.0                                     # bought for 120.9m yen in the direct market
usd = eur * eurusd
yen_end = usd * usdjpy
print(f"  consistent example: buy 1m euro for {start}m yen, sell for ${usd:.2f}m, sell for {yen_end:.1f}m yen: "
      f"profit {yen_end - start:.1f}m yen = ${1e6*(yen_end - start)/usdjpy:,.0f}")
assert abs(yen_end - start - 0.1) < 1e-9
# with bid and ask: converting X into Y at the quoted "Y per X" gets the bid; Y into X costs the ask
def cycle_profits(q):
    """q[pair] = (bid, ask) for EURUSD ($ per euro), USDJPY (yen per $), EURJPY (yen per euro).
    Returns the gross return of the two directions of the cycle starting with one euro."""
    (eu_b, eu_a), (uj_b, uj_a), (ej_b, ej_a) = q["EURUSD"], q["USDJPY"], q["EURJPY"]
    via_usd = eu_b * uj_b / ej_a              # euro -> $ -> yen -> euro
    via_jpy = ej_b / uj_a / eu_a              # euro -> yen -> $ -> euro
    return via_usd, via_jpy
viol_agree, n_trials = 0, 20_000
for _ in range(n_trials):
    m_eu, m_uj = rng.uniform(1.0, 1.2), rng.uniform(100, 150)
    h_eu, h_uj = rng.uniform(0, 2e-4) * m_eu, rng.uniform(0, 2e-4) * m_uj
    m_ej = m_eu * m_uj * (1 + rng.normal(0, 3e-4))
    h_ej = rng.uniform(0, 2e-4) * m_ej
    q = {"EURUSD": (m_eu - h_eu, m_eu + h_eu), "USDJPY": (m_uj - h_uj, m_uj + h_uj), "EURJPY": (m_ej - h_ej, m_ej + h_ej)}
    a, b = cycle_profits(q)
    band_lo = q["EURUSD"][0] * q["USDJPY"][0]             # synthetic bid
    band_hi = q["EURUSD"][1] * q["USDJPY"][1]             # synthetic ask
    arbitrage = (a > 1) or (b > 1)
    outside = (band_lo > q["EURJPY"][1]) or (q["EURJPY"][0] > band_hi)
    viol_agree += (arbitrage == outside)
print(f"  {n_trials:,} random quote sets: a cycle earns money exactly when the direct quotes do not overlap the synthetic "
      f"band [bid x bid, ask x ask]: agreement {viol_agree}/{n_trials}")
assert viol_agree == n_trials


# 3. Make/take fees and the speed race -----------------------------------------------------
section("3. make/take fees and the speed race (Lehalle and Laruelle, eq. (A.4))")
def equilibrium(M, N, piM, piT, beta, gamma):
    """Symmetric Nash equilibrium of the speed game: each market maker m maximises
    (mu_m / mubar) piM R - beta mu_m^2 / 2, each investor n (tau_n / taubar) piT R - gamma tau_n^2 / 2,
    with mubar and taubar the sums of intensities and R = mubar taubar / (mubar + taubar)."""
    def foc(x):
        mu, tau = np.exp(x)
        mb, tb = M * mu, N * tau
        s = mb + tb
        f1 = piM * tb * (s - mu) / s**2 - beta * mu
        f2 = piT * mb * (s - tau) / s**2 - gamma * tau
        return [f1 / (beta * mu), f2 / (gamma * tau)]
    sol = optimize.root(foc, x0=[0.0, 0.0], tol=1e-12)
    mu, tau = np.exp(sol.x)
    assert sol.success
    mb, tb = M * mu, N * tau
    return mu, tau, mb * tb / (mb + tb)
def best_split(M, N, G, beta, gamma):
    f = lambda x: -equilibrium(M, N, x, G - x, beta, gamma)[2]
    r = optimize.minimize_scalar(f, bounds=(1e-6 * G, G * (1 - 1e-6)), method="bounded", options={"xatol": 1e-10})
    return r.x
G, beta, gamma = 1.0, 1.0, 2.0
for M, N in [(5, 5), (50, 50), (500, 1000), (5000, 5000)]:
    z = (M * gamma / (N * beta)) ** (1 / 3)
    formula = G / (1 + z)
    x = best_split(M, N, G, beta, gamma)
    print(f"  M={M}, N={N}: trade-rate-maximising maker margin pi_M = {x:.5f} against G/(1+(M gamma/(N beta))^(1/3)) = {formula:.5f}")
assert abs(best_split(5000, 5000, G, beta, gamma) - G / (1 + 2 ** (1 / 3))) < 2e-3
# signs: with s Delta = 1 tick and a total fee cbar, c_M* = s Delta - (Gamma - cbar)/(1 + z)
sD, Gamma, cbar = 1.0, 3.0, 0.3
for M, N, b_, g_ in [(2, 50, 1.0, 1.0), (50, 50, 1.0, 1.0), (200, 20, 1.0, 4.0)]:
    z = (M * g_ / (N * b_)) ** (1 / 3)
    cM = sD - (Gamma - cbar) / (1 + z)
    cT = cbar - cM
    print(f"  M={M}, N={N}, gamma/beta={g_/b_:.0f}: c_M* = {cM:+.3f} ({'maker rebate' if cM < 0 else 'maker fee'}), "
          f"c_T* = {cT:+.3f} ({'taker rebate' if cT < 0 else 'taker fee'})")
z_hi = (200 * 4.0 / 20) ** (1 / 3); z_lo = (2 / 50) ** (1 / 3)
assert sD - (Gamma - cbar) / (1 + z_lo) < 0 and cbar - (sD - (Gamma - cbar) / (1 + z_hi)) < 0
print("  LL's 'Gamma - cbar is obviously larger than s Delta' needs pi_T > c_M; the participation conditions pi_M, pi_T > 0 do not imply it:")
piM_, cM_, cT_ = 0.1, 0.9, 0.0; Gam_ = sD + cT_ + 0.05     # pi_T = 0.05 > 0, c_M = 0.9 > pi_T
print(f"    s Delta = 1, c_M = {cM_}, c_T = {cT_}, Gamma = {Gam_}: pi_M = {sD - cM_:.2f} > 0, pi_T = {Gam_ - sD - cT_:.2f} > 0, "
      f"Gamma - cbar = {Gam_ - cM_ - cT_:.2f} < s Delta")
assert Gam_ - cM_ - cT_ < sD


# 4. The toy flash-crash model ------------------------------------------------------------------
section("4. the toy flash-crash model (app. A.5)")
rho, r0 = 0.6, 1.0
k = np.arange(1, 41)
r_round = (1 - rho**k) / (1 - rho) * r0                      # rate after k rounds of re-trading
geo = np.cumsum(rho ** (k - 1)) * r0
print(f"  hot potato: after k rounds r_k = (1 - rho^k)/(1 - rho) r0 = 1 + rho + ... + rho^(k-1) (times r0); "
      f"k=1: {r_round[0]:.2f}, k=5: {r_round[4]:.3f}, limit r0/(1-rho) = {r0/(1-rho):.2f}")
assert np.allclose(r_round, geo) and abs(r_round[0] - r0) < 1e-12
print("  so t counts rounds (r = r0 after one round), not clock time: at t = 0 the formula gives 0, not r0;")
print(f"  in clock time on [0, 1], as in Figures A.4--A.5, rho^t >= {rho:.1f} and r_t <= r0: no amplification has happened")
R_sum = np.cumsum(r_round)
R_exact = r0 / (1 - rho) * (k - rho * (1 - rho**k) / (1 - rho))
print(f"  overflow after k rounds: sum r = r0/(1-rho) [k - rho(1-rho^k)/(1-rho)]; k=10: {R_sum[9]:.3f} against LL's k r0/(1-rho) = "
      f"{10*r0/(1-rho):.3f}; the gap tends to rho r0/(1-rho)^2 = {rho*r0/(1-rho)**2:.3f}")
assert np.allclose(R_sum, R_exact) and abs((k[-1] * r0 / (1 - rho) - R_sum[-1]) - rho * r0 / (1 - rho) ** 2) < 1e-6
# the time term: (A.14) has t^2 r0 / (2(1 - rho)); integrating (A.12) with the rate r gives a term linear in t
sig, T, n_steps, n_paths = 0.3, 1.0, 2000, 4000
dt = T / n_steps
t_grid = np.linspace(dt, T, n_steps)
dW = rng.normal(0, np.sqrt(dt), (n_paths, n_steps))
def log_I_end(drift):
    # exact log-solution of dI/I = sigma dW + drift dt: log I_T - log I_0 = int drift - sigma^2 T/2 + sigma W_T
    return np.sum(drift * dt) - 0.5 * sig**2 * T + sig * dW.sum(axis=1)
rbar = r0 / (1 - rho)
case_rate = log_I_end(np.full(n_steps, rbar)).mean()           # drift = the limiting rate
case_overflow = log_I_end(rbar * t_grid).mean()                # drift = R_t = t r0/(1 - rho)
print(f"  E[log I_1/I_0] with drift r = r0/(1-rho): {case_rate:.4f} (theory {rbar*T - sig**2*T/2:.4f}, linear in t)")
print(f"  with drift R_t = t r0/(1-rho): {case_overflow:.4f} (theory, LL's (A.14) exponent: {rbar*T**2/2 - sig**2*T/2:.4f}, quadratic in t)")
assert abs(case_rate - (rbar * T - sig**2 * T / 2)) < 0.02
assert abs(case_overflow - (rbar * T**2 / 2 - sig**2 * T / 2)) < 0.02
print("  (A.14) therefore follows from (A.12) only if the overflow R, not the rate r, drives impact, as LL's prose says")
print("  ('when more volume is traded than expected, R is large, thus the impact I is large', p. 262); with r the term is")
print("  linear. Units: r dt is a quantity, dI/I a number, so a scale (1/quantity, or 1/(quantity x time) for R dt) is implicit.")


# 5. The May 2010 report's arithmetic --------------------------------------------------------------
section("5. the May 6, 2010 report (CFTC and SEC staff, September 2010)")
per_contract = 4.1e9 / 75_000
per_contract2 = 1.9e9 / 35_000
print(f"  75,000 E-mini contracts at about $4.1 billion: ${per_contract:,.0f} a contract (50 x index level ~ {per_contract/50:,.0f}); "
      f"35,000 at $1.9 billion: ${per_contract2:,.0f}")
assert abs(per_contract / 50 - 1093) < 5 and abs(per_contract2 / 50 - 1086) < 5
total_14s = 27_000 / 0.49
print(f"  hot potato, 2:45:13--2:45:27: HFTs traded over 27,000 contracts, about 49% of volume (total ~{total_14s:,.0f}), "
      f"while buying about 200 net: turnover {27_000/200:.0f} times the net change")
print(f"  buy-side depth fell to about $58 million, {58e6/6e9:.1%} of the morning's nearly $6 billion ('less than 1%')")
assert 58e6 / 6e9 < 0.01


# 6. Queue-position values (Moallemi and Yuan, Table 3) -------------------------------------------
section("6. queue-position values (Moallemi and Yuan, June 2017 revision, Table 3, model columns, ticks)")
order_value = {"BAC": 0.14, "CSCO": 0.08, "GE": 0.08, "F": 0.13, "INTC": 0.11, "PFE": 0.12, "PBR": -0.03, "EMM": 0.07, "EFA": 0.03}
touch_value = {"BAC": 0.36, "CSCO": 0.24, "GE": 0.19, "F": 0.24, "INTC": 0.28, "PFE": 0.16, "PBR": 0.03, "EMM": 0.21, "EFA": 0.06}
gaps = {s: round(touch_value[s] - order_value[s], 2) for s in order_value}
print("  touch (front) minus back-of-queue value:", ", ".join(f"{s} {g:.2f}" for s, g in gaps.items()))
assert all(g >= 0 for g in gaps.values()) and gaps["BAC"] == 0.22 and gaps["PFE"] == 0.04


# 7. Proportion intervals -------------------------------------------------------------------------
section("7. proportion intervals: Wald against Wilson")
z = stats.norm.ppf(0.975)
def wald(k, n):
    p = k / n; h = z * np.sqrt(p * (1 - p) / n); return p - h, p + h
def wilson(k, n):
    p = k / n; c = (p + z**2 / (2 * n)) / (1 + z**2 / n)
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / (1 + z**2 / n); return c - h, c + h
for n, p in [(30, 0.5), (30, 0.1), (30, 0.02), (200, 0.02), (1000, 0.02)]:
    ks = np.arange(n + 1); pk = stats.binom.pmf(ks, n, p)
    cov_w = sum(pk[k] for k in ks if wald(k, n)[0] <= p <= wald(k, n)[1])
    cov_s = sum(pk[k] for k in ks if wilson(k, n)[0] <= p <= wilson(k, n)[1])
    print(f"  n={n:5d}, p={p:.2f} (np={n*p:5.1f}): exact coverage of the nominal 95% interval: Wald {cov_w:.3f}, Wilson {cov_s:.3f}")
ks = np.arange(31); pk = stats.binom.pmf(ks, 30, 0.02)
cov_w = sum(pk[k] for k in ks if wald(k, 30)[0] <= 0.02 <= wald(k, 30)[1])
assert cov_w < 0.6
lo0, hi0 = wald(0, 30)
print(f"  zero successes in 30: Wald interval [{lo0:.3f}, {hi0:.3f}] (degenerate); Wilson [{wilson(0,30)[0]:.3f}, {wilson(0,30)[1]:.3f}]")
assert lo0 == hi0 == 0.0
print("  Lehalle and Laruelle's rule of thumb is n p > 5 and n (1 - p) > 5 with the true p (p. 286); the legacy notes used the estimate")


# 8. Harris's power tables and inference pitfalls -----------------------------------------------------
section("8. t-test power and data requirements (Harris, chap. 22)")
s_adj = np.sqrt(16**2 + 14.5**2 - 2 * 0.9 * 16 * 14.5)
print(f"  market-adjusted sd sqrt(16^2 + 14.5^2 - 2 x 0.9 x 16 x 14.5) = {s_adj:.2f}% a year (Harris: 7.0)")
assert abs(s_adj - 6.97) < 0.01
def power(years, skill=2.0, sd=7.0, conf=0.95):
    return 1 - stats.norm.cdf(stats.norm.ppf(conf) - skill * np.sqrt(years) / sd)
print(f"  power of the one-sided 95% test, skill 2%, sd 7%: 5 years {power(5):.3f}, 10 years {power(10):.3f} (Harris: 15% and 23%)")
assert abs(power(5) - 0.15) < 0.01 and abs(power(10) - 0.23) < 0.01
def years_needed(conf, pw, skill, sd=7.0):
    return ((stats.norm.ppf(conf) + stats.norm.ppf(pw)) * sd / skill) ** 2
table = {(0.75, 0.75, 2): 22, (0.95, 0.95, 2): 132, (0.50, 0.95, 2): 33, (0.95, 0.95, 4): 33, (0.75, 0.75, 4): 6}
for (c, pw, sk), h in table.items():
    y = years_needed(c, pw, sk)
    print(f"  years for confidence {c:.0%}, power {pw:.0%}, skill {sk}%: ((z_c + z_p) sd / skill)^2 = {y:.1f} (Harris, Table 22-3: {h})")
    assert abs(y - h) < 1.0
print("  so detecting an edge mu with noise sigma needs n = ((z_{1-alpha} + z_power) sigma/mu)^2 periods, of order (sigma/mu)^2")
# sampling frequency over a fixed span
mu_a, sd_a, years = 0.02, 0.07, 10
tstats = {}
for label, per_year in [("annual", 1), ("monthly", 12), ("daily", 250)]:
    n = years * per_year
    x = rng.normal(mu_a / per_year, sd_a / np.sqrt(per_year), (20_000, n))
    t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(n))
    tstats[label] = t.mean()
print("  mean t-statistic over 10 years, skill 2%, sd 7%: " + ", ".join(f"{k} {v:.2f}" for k, v in tstats.items())
      + f" (mu sqrt(T)/sigma = {mu_a*np.sqrt(years)/sd_a:.2f}): sampling more often does not add history")
assert abs(tstats["monthly"] - tstats["daily"]) < 0.05
# serially correlated returns: the naive standard error is too small
phi, n = 0.3, 2500
e = rng.normal(0, 1, (4000, n))
x = np.empty_like(e); x[:, 0] = e[:, 0]
for i in range(1, n):
    x[:, i] = phi * x[:, i - 1] + e[:, i]
t0 = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(n))
print(f"  AR(1) returns with phi = {phi}, true mean 0: sd of the naive t {t0.std():.2f} (1 if valid; theory sqrt((1+phi)/(1-phi)) = "
      f"{np.sqrt((1+phi)/(1-phi)):.2f}); effective sample {n*(1-phi)/(1+phi):.0f} of {n}")
assert abs(t0.std() - np.sqrt((1 + phi) / (1 - phi))) < 0.05
# the best of many unskilled managers (Harris's Buffett box, p. 463)
t_b = 11.8 / (14.3 / np.sqrt(36))
p1 = stats.norm.sf(t_b)
print(f"  Buffett box: t = 11.8/(14.3/6) = {t_b:.2f}; one unskilled manager exceeds it with probability {p1:.2e} (normal), "
      f"{stats.t.sf(t_b, 35):.2e} (t, 35 df; Harris 0.0011%)")
for m_, h in [(10_000, "0.5%"), (100_000, "5%")]:
    print(f"    best of {m_:,} unskilled managers beats 11.8%: {1 - (1 - p1)**m_:.4f} (normal averages; Harris {h})")
# regression to the mean after selection
tau, sig_l = 0.5, 1.0
skill = rng.normal(0, tau, 200_000)
y1 = skill + rng.normal(0, sig_l, skill.size); y2 = skill + rng.normal(0, sig_l, skill.size)
top = y1 > np.quantile(y1, 0.9)
print(f"  top decile on period 1: mean {y1[top].mean():.2f}, then {y2[top].mean():.2f} in period 2; ratio "
      f"{y2[top].mean()/y1[top].mean():.2f} against the shrinkage tau^2/(tau^2+sigma^2) = {tau**2/(tau**2+sig_l**2):.2f}")
assert abs(y2[top].mean() / y1[top].mean() - tau**2 / (tau**2 + sig_l**2)) < 0.02
# a short-volatility return stream: high t in samples without a crash
p_crash, gain, loss, months = 0.02, 0.01, -0.40, 60
mean_m = (1 - p_crash) * gain + p_crash * loss
print(f"  short volatility: +1% a month, -40% with probability 2%: true mean {mean_m:+.2%} a month; "
      f"P(no crash in 60 months) = {(1-p_crash)**months:.2f}, and those samples show zero variance and an unbounded t")
assert mean_m > 0 and abs((1 - p_crash) ** months - 0.30) < 0.01


# 9. Regression fit and the averaging effect ---------------------------------------------------------
section("9. regression fit, R^2 and the averaging effect (Lehalle and Laruelle, apps. A.10 and A.14)")
x = rng.lognormal(3, 0.6, 500); y = 2.5 + 0.05 * x + rng.normal(0, 1.5, 500)
b1 = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2); b0 = y.mean() - b1 * x.mean()
yh = b0 + b1 * x
r2_a = 1 - np.sum((y - yh) ** 2) / np.sum((y - y.mean()) ** 2)
r2_b = np.sum((yh - y.mean()) ** 2) / np.sum((y - y.mean()) ** 2)
print(f"  OLS with an intercept: 1 - RSS/TSS = {r2_a:.4f} = ESS/TSS = {r2_b:.4f} = r^2 = {np.corrcoef(x, y)[0,1]**2:.4f}")
assert abs(r2_a - r2_b) < 1e-12 and abs(r2_a - np.corrcoef(x, y)[0, 1] ** 2) < 1e-12
# LL's multiplicative predictor: the two definitions differ
ly, lx = np.log(np.abs(y) + 0.1), np.log(x)
c1 = np.polyfit(lx, ly, 1); res = ly - np.polyval(c1, lx)
pred = np.exp(np.polyval(c1, lx)) * np.exp(res.var(ddof=2) / 2) - 0.1
r2_ess = np.sum((pred - y.mean()) ** 2) / np.sum((y - y.mean()) ** 2)
r2_rss = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
print(f"  back-transformed log-log predictor: ESS/TSS {r2_ess:.4f} against 1 - RSS/TSS {r2_rss:.4f} (LL's R'^2 uses ESS/TSS)")
assert abs(r2_ess - r2_rss) > 1e-3
# index spread and volatility
N, Tn = 30, 2000
w = rng.dirichlet(np.ones(N)); S = rng.uniform(20, 200, N)
half = rng.uniform(0.005, 0.05, N)              # absolute half-spreads
idx_spread_abs = np.sum(w * 2 * half)
idx_level = np.sum(w * S)
rel_stock = 2 * half / S
print(f"  absolute spreads aggregate: index ask - bid = sum w (ask - bid) = {idx_spread_abs:.5f}; "
      f"relative spreads do not: index {idx_spread_abs/idx_level:.6f} against sum w psi_rel {np.sum(w*rel_stock):.6f}")
assert abs(idx_spread_abs / idx_level - np.sum(w * S * rel_stock) / idx_level) < 1e-12
corr = 0.4
cov = corr * np.ones((N, N)) + (1 - corr) * np.eye(N)
vols = rng.uniform(0.01, 0.03, N) * S
dS = rng.multivariate_normal(np.zeros(N), cov * np.outer(vols, vols), 5000)
sig_I = np.std(dS @ w); sig_w = np.sum(w * vols)
print(f"  price-change volatilities, correlation {corr}: index {sig_I:.3f} against sum w sigma_k {sig_w:.3f} (subadditive)")
assert sig_I < sig_w
# regression of index quantities against the average of stock regressions
a0, a1 = 0.02, 2.5
c_common, n_intra = 0.6, 50
regime = rng.lognormal(0, 0.4, Tn)                # common volatility level of each period
level = rng.uniform(0.5, 1.5, N)                  # stock-specific volatility scale
vol = 1e-3 * np.outer(regime, level) * (1 + 0.5 * rng.random((Tn, N)))
F = rng.normal(0, 1, (Tn, n_intra))               # common intraperiod shocks
E = rng.normal(0, 1, (Tn, N, n_intra))            # idiosyncratic intraperiod shocks
ret = vol[:, :, None] * (np.sqrt(c_common) * F[:, None, :] + np.sqrt(1 - c_common) * E)
sig_k = ret.std(axis=2, ddof=1)                   # realised stock volatilities per period
sig_I_t = np.einsum("k,tkj->tj", w, ret).std(axis=1, ddof=1)   # realised index volatility per period
psi_k = a0 + a1 * sig_k + rng.normal(0, 1e-3, (Tn, N))
psi_I = psi_k @ w
coef_stock = np.array([np.polyfit(sig_k[:, j], psi_k[:, j], 1) for j in range(N)])
avg_slope = np.sum(w * coef_stock[:, 0])
idx_slope = np.polyfit(sig_I_t, psi_I, 1)[0]
print(f"  stock slopes average {avg_slope:.3f} (true {a1}); slope of the index spread on the index volatility {idx_slope:.3f}: "
      f"higher, because the index volatility is below the weighted average of the stock volatilities")
assert idx_slope > avg_slope
print("  LL's A.14.2 defines abar_1 as sum w_k a^k_0 (p. 320), a printing slip for sum w_k a^k_1")
# mean against path
days = 500; bins = 100
spikes = rng.integers(10, 90, days)
paths = np.ones((days, bins))
for d_, s_ in enumerate(spikes):
    paths[d_, s_:s_ + 3] += 6
mean_path = paths.mean(axis=0)
print(f"  500 days, each calm with one 3-bin spike at a random time: the average profile peaks at {mean_path.max():.2f}, "
      f"every single day at 7.00; no day looks like the average")
assert mean_path.max() < 1.5


# 10. A spread's factor exposure with a hedge ratio ------------------------------------------------------
section("10. factor exposure of a hedged spread")
bi, bj = np.array([1.2, 0.3]), np.array([0.8, 0.5])
for h in [1.0, bi[0] / bj[0]]:
    print(f"  r_i - h r_j with h = {h:.3f}: factor exposure beta_i - h beta_j = {np.round(bi - h*bj, 3)} "
          f"(the legacy beta_i - beta_j is the case h = 1)")
assert np.allclose((bi - (bi[0] / bj[0]) * bj)[0], 0.0)
f = rng.normal(0, 0.01, (100_000, 2)); ei = rng.normal(0, 0.005, 100_000); ej = rng.normal(0, 0.005, 100_000)
ri = f @ bi + ei; rj = f @ bj + ej
h = 1.5
spread = ri - h * rj
pred_var = (bi - h * bj) @ np.diag([1e-4, 1e-4]) @ (bi - h * bj) + 0.005**2 * (1 + h**2)
print(f"  simulated spread variance {spread.var():.3e} against (beta_i - h beta_j)' Sigma_f (beta_i - h beta_j) + var(e_i) + h^2 var(e_j) = {pred_var:.3e}")
assert abs(spread.var() / pred_var - 1) < 0.02

print("\nall checks passed")
