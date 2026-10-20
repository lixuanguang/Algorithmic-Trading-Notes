"""Hedge funds: exposures, fee layers, strategy arithmetic and the effect of an allocation (2026-10-20).

Worked numbers of def:hedge-fund-features, meth:hedge-fund-strategy-classification and meth:hedge-fund-factor-exposures.
Funds, returns and positions are hypothetical except where a check reproduces a published figure (Ang 2014,
pp. 565 and 585; Jaeger 2008, pp. 4 and 15; Getmansky, Lo and Makarov 2004).

Independent routes: smoothing effects from the Getmansky-Lo-Makarov closed forms against a long simulation; factor
loadings from OLS on simulated returns against the loadings used to generate them, with and without lagged factors;
the marginal effect of an allocation from the Sharpe-ratio rule against the portfolio computed directly.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python hedge-fund-checks.py   (numpy). Exits 1 on failure.
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
    "Ang p. 565: Malkiel and Saha's backfilled 14.7% against 7.3% non-backfilled is a 7.4-point gap; Ang prints 7.3%",
    close(round(14.7 - 7.3, 1), 7.4),
)
ok(
    "Ang p. 585: equivalent flat fees 6.4% (2/20), 5.8% with a high-water mark, 5.3% adding a 4% hurdle - "
    "each feature lowers the fee",
    6.4 > 5.8 > 5.3,
)
ok(
    "Jaeger p. 15: a fund of funds charging 1% and 10% above a hurdle on top of 2/20 underlying funds; "
    "Jaeger p. 4: leverage at Libor + 60-80 bp against cash at Libor - 20 bp loses 80-100 bp on the spread",
    close(0.60 + 0.20, 0.80) and close(0.80 + 0.20, 1.00),
)

# ---------------------------------------------------------------------------------------------
print("== part 2: fee layers in a fund of funds")
gross = np.array([0.20, -0.10])  # two underlying funds, equal weights, gross of fees
mgmt, carry = 0.02, 0.20
net_each = np.where(gross - mgmt > 0, (gross - mgmt) * (1 - carry), gross - mgmt)
portfolio_gross = gross.mean()
netted = (portfolio_gross - mgmt) * (1 - carry)
ok(
    "two funds at +20% and -10% gross: the portfolio's gross is 5%; paying 2/20 fund by fund nets 1.20%, "
    "against 2.40% if incentive fees were netted - a 1.20-point 'diversification cost'",
    close(portfolio_gross, 0.05)
    and close(net_each.mean(), 0.012)
    and close(netted, 0.024)
    and close(netted - net_each.mean(), 0.012),
)
fof = net_each.mean() - 0.01
fof = fof * (1 - 0.10) if fof > 0 else fof
ok(
    "adding the fund of funds' own 1% fee (and 10% of any positive remainder) leaves 0.18%",
    round(fof * 100, 2) == 0.18,
)

# ---------------------------------------------------------------------------------------------
print("== part 3: strategy arithmetic")
offer, price, fallback = 50.0, 48.0, 40.0
p_close = (price - fallback) / (offer - fallback)
spread = offer / price - 1
ok(
    "cash merger: target at 48 against a 50 offer and a 40 fallback implies an 80% chance of completion; "
    "the 4.17% spread over four months annualises to 13.03%",
    close(p_close, 0.80)
    and round(spread * 100, 2) == 4.17
    and round(((1 + spread) ** 3 - 1) * 100, 2) == 13.03,
)
ok("a deal break back to 40 costs 16.67% from 48", round((fallback / price - 1) * 100, 2) == -16.67)
ratio, acq = 0.5, 98.0
ok(
    "stock merger at 0.5 acquirer shares: long one target at 48, short 0.5 acquirer at 98 locks a spread of 1.00",
    close(ratio * acq - price, 1.0),
)
long_, short_, beta_l, beta_s = 1.30, 0.70, 1.1, 0.9
ok(
    "long/short equity: 130% long and 70% short is 200% gross and 60% net; with betas 1.1 and 0.9 the "
    "beta-adjusted net is 80%",
    close(long_ + short_, 2.0)
    and close(long_ - short_, 0.6)
    and close(long_ * beta_l - short_ * beta_s, 0.80),
)
cb_price, delta, stock = 105.0, 0.6, 40.0
conv_ratio = 2.0  # shares per bond
hedge_shares = delta * conv_ratio
ok(
    "convertible arbitrage: a bond convertible into 2 shares with delta 0.6 is hedged by shorting 1.2 shares (48 of "
    "stock against 105 of bond); a 1% stock move changes the hedged position by about zero to first order",
    close(hedge_shares, 1.2)
    and close(hedge_shares * stock, 48.0)
    and close(delta * conv_ratio * 0.4 - hedge_shares * 0.4, 0.0),
)

# ---------------------------------------------------------------------------------------------
print("== part 4: return smoothing (Getmansky, Lo and Makarov)")
theta = np.array([0.5, 0.3, 0.2])
ratio_vol = float(np.sqrt(np.sum(theta**2)))
rho1 = float(theta[0] * theta[1] + theta[1] * theta[2]) / float(np.sum(theta**2))
ok(
    "weights 0.5/0.3/0.2: reported volatility is 61.6% of true, the Sharpe ratio is inflated 1.62 times and "
    "first-order autocorrelation is 0.553",
    round(ratio_vol, 3) == 0.616 and round(1 / ratio_vol, 2) == 1.62 and round(rho1, 3) == 0.553,
)
rng = np.random.default_rng(20261020)
T = 200_000
true = rng.normal(0.006, 0.03, T)
rep = theta[0] * true[2:] + theta[1] * true[1:-1] + theta[2] * true[:-2]
sim_ratio = rep.std() / true.std()
sim_rho = np.corrcoef(rep[1:], rep[:-1])[0, 1]
ok(
    "simulation (200,000 months) matches: volatility ratio and autocorrelation within 0.01 of the closed forms",
    abs(sim_ratio - ratio_vol) < 0.01 and abs(sim_rho - rho1) < 0.01,
    f"{sim_ratio:.3f}, {sim_rho:.3f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 5: factor model of hedge fund exposures")
T = 240  # 20 years of months
mkt = rng.normal(0.006, 0.045, T + 1)
shortvol = 0.5 * mkt + rng.normal(
    0.004, 0.02, T + 1
)  # a short-volatility factor, partly correlated with equities
alpha, b_mkt, b_vol = 0.001, 0.30, 0.60
true_r = alpha + b_mkt * mkt + b_vol * shortvol + rng.normal(0, 0.01, T + 1)
smooth = 0.6 * true_r[1:] + 0.4 * true_r[:-1]  # reported returns with one lag of smoothing
X1 = np.column_stack([np.ones(T), mkt[1:]])
c1 = np.linalg.lstsq(X1, smooth, rcond=None)[0]
X3 = np.column_stack([np.ones(T), mkt[1:], mkt[:-1], shortvol[1:], shortvol[:-1]])
c3 = np.linalg.lstsq(X3, smooth, rcond=None)[0]
beta_eq_total = c3[1] + c3[2]
beta_vol_total = c3[3] + c3[4]
ok(
    "an equity-only regression on smoothed returns loads only part of the equity and volatility exposure "
    "(contemporaneous beta well below the true 0.60 combined) and reports a larger alpha",
    c1[1] < 0.45 and c1[0] > c3[0],
    f"beta {c1[1]:.2f}, alpha {c1[0] * 1200:.2f}% a year against {c3[0] * 1200:.2f}%",
)
ok(
    "with the volatility factor and one lag of each factor (Dimson sums), the loadings recover 0.30 and 0.60 "
    "within 0.08",
    abs(beta_eq_total - b_mkt) < 0.08 and abs(beta_vol_total - b_vol) < 0.08,
    f"{beta_eq_total:.2f}, {beta_vol_total:.2f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 6: adding a hedge fund strategy to a 60/40 portfolio")
rf = 0.03
mu_p, sd_p = 0.065, 0.10  # 60/40 portfolio
mu_h, sd_h_rep, rho_rep = 0.07, 0.06, 0.40  # reported hedge fund statistics
sr_p = (mu_p - rf) / sd_p


def combined(w, sd_h, rho, mu_hf=mu_h):
    mu = (1 - w) * mu_p + w * mu_hf
    var = (1 - w) ** 2 * sd_p**2 + w**2 * sd_h**2 + 2 * w * (1 - w) * rho * sd_p * sd_h
    return (mu - rf) / np.sqrt(var)


hurdle_rep = sr_p * rho_rep
sr_h_rep = (mu_h - rf) / sd_h_rep
ok(
    "on reported numbers (7%, 6% volatility, correlation 0.40) the fund's Sharpe 0.67 beats the hurdle "
    "0.35 x 0.40 = 0.14, and a 10% allocation lifts the portfolio Sharpe ratio from 0.350 to 0.384",
    round(sr_h_rep, 2) == 0.67
    and round(hurdle_rep, 2) == 0.14
    and round(sr_p, 3) == 0.350
    and round(combined(0.10, sd_h_rep, rho_rep), 3) == 0.384,
)
sd_h_true, rho_true = sd_h_rep / ratio_vol, 0.70
sr_h_true = (mu_h - rf) / sd_h_true
ok(
    "de-smoothed (volatility / 0.616 = 9.7%) and with the full-cycle correlation 0.70, the fund's Sharpe is 0.41 "
    "against a hurdle of 0.245; the 10% allocation raises the portfolio Sharpe only to 0.366",
    round(sd_h_true * 100, 1) == 9.7
    and round(sr_h_true, 2) == 0.41
    and round(sr_p * rho_true, 3) == 0.245
    and round(combined(0.10, sd_h_true, rho_true), 3) == 0.366,
)
mu_net = mu_h - 0.015
ok(
    "if 1.5 points of the 7% are fees an investor could avoid with liquid factor exposure, the net fund at 5.5% "
    "still clears the rule (0.257 > 0.245) but adds less than 0.001 to the portfolio Sharpe ratio",
    round((mu_net - rf) / sd_h_true, 3) == 0.257
    and 0 < combined(0.10, sd_h_true, rho_true, mu_net) - sr_p < 0.001,
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
