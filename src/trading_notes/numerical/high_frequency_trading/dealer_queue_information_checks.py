"""Dealer quotes, arbitrage, speed races, queue values, inference and spread regressions."""

import sys
from typing import Final, Literal

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.high_frequency_trading.speed_race import SpeedRace, cycle_returns
from trading_notes.numerical.report import require, section
from trading_notes.numerical.statistical_inference.sample_inference import (
    ProportionEstimate,
    SkillTest,
)

type Floats = NDArray[np.float64]

SEED: Final = 36
N_TRIALS: Final = 20_000
# Harris's example: skill 2% a year with 7% market-adjusted standard deviation.
HARRIS: Final = SkillTest(skill=2.0, sd=7.0)


def check_inside_spread() -> list[str]:
    """Part 1: Harris's inside spread from five dealers' quotes."""
    failed: list[str] = []
    section("1. Harris's inside spread (Table 13-1)")
    quotes = {
        "Charles": (99.9, 100.4),
        "Cheryl": (100.0, 100.5),
        "Goldie": (100.1, 100.6),
        "Larry": (100.2, 100.7),
        "Teri": (100.3, 100.8),
    }
    best_bid = max(b for b, a in quotes.values())
    best_ask = min(a for b, a in quotes.values())
    spreads = [round(a - b, 10) for b, a in quotes.values()]
    print(
        f"  each dealer's spread {set(spreads)}; inside {best_bid} / {best_ask}, inside spread"
        f" {best_ask - best_bid:.1f}"
    )
    require(
        failed,
        "inside spread 0.1 and no wider than any dealer's spread",
        bool(abs(best_ask - best_bid - 0.1) < 1e-9 and best_ask - best_bid <= min(spreads)),
    )
    return failed


def check_cyclic_arbitrage(rng: np.random.Generator) -> list[str]:
    """Part 2: Harris's currency box, and cycles against bid-ask quotes by simulation."""
    failed: list[str] = []
    section("2. cyclic (triangular) currency arbitrage")
    usdjpy, eurusd = 110.0, 1.10  # yen per dollar; dollars per euro
    implied = usdjpy * eurusd  # yen per euro
    print(
        f"  Harris's box: 110 yen per dollar and 1.10 dollars per euro imply {implied:.0f} yen per"
        " euro, not the printed 100"
    )
    require(failed, "Harris box implies 121 yen per euro", bool(abs(implied - 121.0) < 1e-9))
    # the box's cycle with its own numbers: buy $1.10m for 100m yen, buy 1m euro for $1.10m, buy
    # 99.9m yen for 1m euro
    usd = 1.10  # bought for the 100m yen
    eur = usd / 1.10  # bought for the dollars
    yen_end = eur * 99.9  # yen bought for the euros
    print(
        f"  the box's cycle as printed: start 100m yen, end {yen_end:.1f}m yen: a loss of"
        f" {100 - yen_end:.1f}m; it buys euros at the implied rate and sells them where they are"
        f" cheap"
    )
    require(failed, "the box's cycle ends at 99.9m yen", bool(abs(yen_end - 99.9) < 1e-9))
    # a consistent example: direct euro quote 120.9 yen below the implied 121
    start = 120.9
    eur = 1.0  # bought for 120.9m yen in the direct market
    usd = eur * eurusd
    yen_end = usd * usdjpy
    print(
        f"  consistent example: buy 1m euro for {start}m yen, sell for ${usd:.2f}m, sell for"
        f" {yen_end:.1f}m yen: profit {yen_end - start:.1f}m yen ="
        f" ${1e6 * (yen_end - start) / usdjpy:,.0f}"
    )
    require(
        failed, "consistent example: profit of 0.1m yen", bool(abs(yen_end - start - 0.1) < 1e-9)
    )
    # with bid and ask: converting X into Y at the quoted "Y per X" gets the bid; Y into X costs the
    # ask
    viol_agree = 0
    for _ in range(N_TRIALS):
        m_eu, m_uj = rng.uniform(1.0, 1.2), rng.uniform(100, 150)
        h_eu, h_uj = rng.uniform(0, 2e-4) * m_eu, rng.uniform(0, 2e-4) * m_uj
        m_ej = m_eu * m_uj * (1 + rng.normal(0, 3e-4))
        h_ej = rng.uniform(0, 2e-4) * m_ej
        q = {
            "EURUSD": (m_eu - h_eu, m_eu + h_eu),
            "USDJPY": (m_uj - h_uj, m_uj + h_uj),
            "EURJPY": (m_ej - h_ej, m_ej + h_ej),
        }
        a, b = cycle_returns(q)
        band_lo = q["EURUSD"][0] * q["USDJPY"][0]  # synthetic bid
        band_hi = q["EURUSD"][1] * q["USDJPY"][1]  # synthetic ask
        arbitrage = (a > 1) or (b > 1)
        outside = (band_lo > q["EURJPY"][1]) or (q["EURJPY"][0] > band_hi)
        viol_agree += arbitrage == outside
    print(
        f"  {N_TRIALS:,} random quote sets: a cycle earns money exactly when the direct quotes do"
        f" not"
        f" overlap the synthetic band [bid x bid, ask x ask]: agreement {viol_agree}/{N_TRIALS}"
    )
    require(
        failed, "a cycle earns money exactly when the quotes leave the band", viol_agree == N_TRIALS
    )
    # Midpoints need not satisfy the frictionless equality while no cycle pays.
    q = {"EURUSD": (1.0999, 1.1001), "USDJPY": (109.99, 110.01), "EURJPY": (120.99, 121.03)}
    a_, b_ = cycle_returns(q)
    syn_mid = (q["EURUSD"][0] + q["EURUSD"][1]) / 2 * (q["USDJPY"][0] + q["USDJPY"][1]) / 2
    dir_mid = sum(q["EURJPY"]) / 2
    print(
        f"  quotes EUR/USD 1.0999/1.1001, USD/JPY 109.99/110.01, EUR/JPY 120.99/121.03: synthetic"
        f" midpoint {syn_mid:.2f}, direct {dir_mid:.2f}; cycle returns per euro {a_:.5f} (via USD)"
        f" and"
        f" {b_:.5f} (via JPY): no arbitrage"
    )
    require(
        failed,
        "midpoints 121.00 and 121.01, and no cycle pays",
        bool(abs(syn_mid - 121.00) < 1e-9 and abs(dir_mid - 121.01) < 1e-9 and a_ < 1 and b_ < 1),
    )
    return failed


def check_make_take() -> list[str]:
    """Part 3: maker-taker fees and the speed race, against the finite-population equilibrium."""
    failed: list[str] = []
    section("3. make/take fees and the speed race (Lehalle and Laruelle, eq. (A.4))")
    G, beta, gamma = 1.0, 1.0, 2.0
    for M, N in [(5, 5), (50, 50), (500, 1000), (5000, 5000)]:
        z = (M * gamma / (N * beta)) ** (1 / 3)
        formula = G / (1 + z)
        x = SpeedRace(makers=M, takers=N, beta=beta, gamma=gamma).best_maker_margin(G)
        print(
            f"  M={M}, N={N}: trade-rate-maximising maker margin pi_M = {x:.5f} against"
            f" G/(1+(M gamma/(N beta))^(1/3)) = {formula:.5f}"
        )
    require(
        failed,
        "M = N = 5000: maker margin matches G/(1 + 2^(1/3))",
        bool(
            abs(
                SpeedRace(makers=5000, takers=5000, beta=beta, gamma=gamma).best_maker_margin(G)
                - G / (1 + 2 ** (1 / 3))
            )
            < 2e-3
        ),
    )
    # signs: with s Delta = 1 tick and a total fee cbar, c_M* = s Delta - (Gamma - cbar)/(1 + z)
    sD, Gamma, cbar = 1.0, 3.0, 0.3
    for M, N, b_, g_ in [(2, 50, 1.0, 1.0), (50, 50, 1.0, 1.0), (200, 20, 1.0, 4.0)]:
        z = (M * g_ / (N * b_)) ** (1 / 3)
        cM = sD - (Gamma - cbar) / (1 + z)
        cT = cbar - cM
        print(
            f"  M={M}, N={N}, gamma/beta={g_ / b_:.0f}: c_M* = {cM:+.3f} ("
            f"{'maker rebate' if cM < 0 else 'maker fee'}), c_T* = {cT:+.3f} ("
            f"{'taker rebate' if cT < 0 else 'taker fee'})"
        )
    z_hi = (200 * 4.0 / 20) ** (1 / 3)
    z_lo = (2 / 50) ** (1 / 3)
    require(
        failed,
        "signs of c_M* and c_T* at the two extremes",
        bool(
            sD - (Gamma - cbar) / (1 + z_lo) < 0 and cbar - (sD - (Gamma - cbar) / (1 + z_hi)) < 0
        ),
    )
    print(
        "  LL's 'Gamma - cbar is obviously larger than s Delta' needs pi_T > c_M; the participation"
        " conditions pi_M, pi_T > 0 do not imply it:"
    )
    cM_, cT_ = 0.9, 0.0
    Gam_ = sD + cT_ + 0.05  # pi_T = 0.05 > 0, c_M = 0.9 > pi_T
    print(
        f"    s Delta = 1, c_M = {cM_}, c_T = {cT_}, Gamma = {Gam_}: pi_M = {sD - cM_:.2f} > 0,"
        f" pi_T ="
        f" {Gam_ - sD - cT_:.2f} > 0, Gamma - cbar = {Gam_ - cM_ - cT_:.2f} < s Delta"
    )
    require(
        failed,
        "Gamma - cbar below s Delta with both participation conditions",
        bool(Gam_ - cM_ - cT_ < sD),
    )
    return failed


def check_flash_crash(rng: np.random.Generator) -> list[str]:
    """Part 4: the hot-potato rate, the overflow, and the time term of the toy flash crash."""
    failed: list[str] = []
    section("4. the toy flash-crash model (app. A.5)")
    rho, r0 = 0.6, 1.0
    k = np.arange(1, 41)
    r_round = (1 - rho**k) / (1 - rho) * r0  # rate after k rounds of re-trading
    geo = np.cumsum(rho ** (k - 1)) * r0
    print(
        f"  hot potato: after k rounds r_k = (1 - rho^k)/(1 - rho) r0 = 1 + rho + ... + rho^(k-1)"
        f" (times"
        f" r0); k=1: {r_round[0]:.2f}, k=5: {r_round[4]:.3f}, limit r0/(1-rho) ="
        f" {r0 / (1 - rho):.2f}"
    )
    require(
        failed,
        "hot potato rates equal the geometric sum and r_1 = r0",
        bool(np.allclose(r_round, geo) and abs(r_round[0] - r0) < 1e-12),
    )
    print(
        "  so t counts rounds (r = r0 after one round), not clock time: at t = 0 the formula gives"
        " 0,"
        " not r0;"
    )
    print(
        f"  in clock time on [0, 1], as in Figures A.4--A.5, rho^t >= {rho:.1f} and r_t <= r0: no"
        " amplification has happened"
    )
    R_sum = np.cumsum(r_round)
    R_exact = r0 / (1 - rho) * (k - rho * (1 - rho**k) / (1 - rho))
    print(
        f"  overflow after k rounds: sum r = r0/(1-rho) [k - rho(1-rho^k)/(1-rho)]; k=10:"
        f" {R_sum[9]:.3f} against LL's k r0/(1-rho) = {10 * r0 / (1 - rho):.3f}; the gap tends to"
        f" rho r0/(1-rho)^2 = {rho * r0 / (1 - rho) ** 2:.3f}"
    )
    require(
        failed,
        "overflow sums match the closed form and its limiting gap",
        bool(
            np.allclose(R_sum, R_exact)
            and abs((k[-1] * r0 / (1 - rho) - R_sum[-1]) - rho * r0 / (1 - rho) ** 2) < 1e-6
        ),
    )
    # the time term: (A.14) has t^2 r0 / (2(1 - rho)); integrating (A.12) with the rate r gives a
    # term linear in t
    sig, T, n_steps, n_paths = 0.3, 1.0, 2000, 4000
    dt = T / n_steps
    t_grid = np.linspace(dt, T, n_steps)
    dW = rng.normal(0, np.sqrt(dt), (n_paths, n_steps))

    def log_I_end(drift: Floats) -> Floats:
        # exact log-solution of dI/I = sigma dW + drift dt: log I_T - log I_0 = int drift - sigma^2
        # T/2 + sigma W_T
        value: Floats = np.sum(drift * dt) - 0.5 * sig**2 * T + sig * dW.sum(axis=1)
        return value

    rbar = r0 / (1 - rho)
    case_rate = log_I_end(np.full(n_steps, rbar)).mean()  # drift = the limiting rate
    case_overflow = log_I_end(rbar * t_grid).mean()  # drift = R_t = t r0/(1 - rho)
    print(
        f"  E[log I_1/I_0] with drift r = r0/(1-rho): {case_rate:.4f} (theory"
        f" {rbar * T - sig**2 * T / 2:.4f},"
        " linear in t)"
    )
    print(
        f"  with drift R_t = t r0/(1-rho): {case_overflow:.4f} (theory, LL's (A.14) exponent:"
        f" {rbar * T**2 / 2 - sig**2 * T / 2:.4f}, quadratic in t)"
    )
    require(
        failed,
        "E[log I] with the limiting rate is linear in t",
        bool(abs(case_rate - (rbar * T - sig**2 * T / 2)) < 0.02),
    )
    require(
        failed,
        "E[log I] with the overflow drift is quadratic in t",
        bool(abs(case_overflow - (rbar * T**2 / 2 - sig**2 * T / 2)) < 0.02),
    )
    print(
        "  (A.14) therefore follows from (A.12) only if the overflow R, not the rate r, drives"
        " impact, as"
        " LL's prose says"
    )
    print(
        "  ('when more volume is traded than expected, R is large, thus the impact I is large', p."
        " 262);"
        " with r the term is"
    )
    print(
        "  linear. Units: r dt is a quantity, dI/I a number, so a scale (1/quantity, or 1/(quantity"
        " x time)"
        " for R dt) is implicit."
    )
    return failed


def check_may_2010() -> list[str]:
    """Part 5: the arithmetic of the May 2010 joint report."""
    failed: list[str] = []
    section("5. the May 6, 2010 report (CFTC and SEC staff, September 2010)")
    per_contract = 4.1e9 / 75_000
    per_contract2 = 1.9e9 / 35_000
    print(
        f"  75,000 E-mini contracts at about $4.1 billion: ${per_contract:,.0f} a contract (50 x"
        f" index level"
        f" ~ {per_contract / 50:,.0f}); 35,000 at $1.9 billion: ${per_contract2:,.0f}"
    )
    require(
        failed,
        "E-mini value per contract consistent with the index level",
        bool(abs(per_contract / 50 - 1093) < 5 and abs(per_contract2 / 50 - 1086) < 5),
    )
    total_14s = 27_000 / 0.49
    print(
        f"  hot potato, 2:45:13--2:45:27: HFTs traded over 27,000 contracts, about 49% of volume"
        f" (total"
        f" ~{total_14s:,.0f}), while buying about 200 net: turnover {27_000 / 200:.0f} times the"
        f" net change"
    )
    print(
        f"  buy-side depth fell to about $58 million, {58e6 / 6e9:.1%} of the morning's nearly $6"
        f" billion"
        " ('less than 1%')"
    )
    require(failed, "buy-side depth below 1% of the morning's volume", bool(58e6 / 6e9 < 0.01))
    return failed


def check_queue_position() -> list[str]:
    """Part 6: queue-position values (Moallemi and Yuan, Table 3): touch against back of queue."""
    failed: list[str] = []
    section(
        "6. queue-position values (Moallemi and Yuan, June 2017 revision, Table 3, model columns,"
        " ticks)"
    )
    order_value = {
        "BAC": 0.14,
        "CSCO": 0.08,
        "GE": 0.08,
        "F": 0.13,
        "INTC": 0.11,
        "PFE": 0.12,
        "PBR": -0.03,
        "EMM": 0.07,
        "EFA": 0.03,
    }
    touch_value = {
        "BAC": 0.36,
        "CSCO": 0.24,
        "GE": 0.19,
        "F": 0.24,
        "INTC": 0.28,
        "PFE": 0.16,
        "PBR": 0.03,
        "EMM": 0.21,
        "EFA": 0.06,
    }
    gaps = {s: round(touch_value[s] - order_value[s], 2) for s in order_value}
    print(
        "  touch (front) minus back-of-queue value:",
        ", ".join(f"{s} {g:.2f}" for s, g in gaps.items()),
    )
    require(
        failed,
        "queue value gaps non-negative; BAC 0.22; PFE 0.04",
        bool(all(g >= 0 for g in gaps.values()) and gaps["BAC"] == 0.22 and gaps["PFE"] == 0.04),
    )
    return failed


def coverage(n: int, p: float, kind: Literal["wald", "wilson"]) -> float:
    """Return the exact binomial coverage of p by the Wald or the Wilson 95% interval."""
    ks = np.arange(n + 1)
    pk = stats.binom.pmf(ks, n, p)
    total = 0.0
    for k in ks:
        estimate = ProportionEstimate(successes=int(k), trials=n)
        lo, hi = estimate.wald_interval() if kind == "wald" else estimate.wilson_interval()
        if lo <= p <= hi:
            total += pk[k]
    return total


def check_proportions() -> list[str]:
    """Part 7: the Wald and Wilson intervals' exact coverage, and zero successes."""
    failed: list[str] = []
    section("7. proportion intervals: Wald against Wilson")
    for n, p in [(30, 0.5), (30, 0.1), (30, 0.02), (200, 0.02), (1000, 0.02)]:
        cov_w, cov_s = coverage(n, p, "wald"), coverage(n, p, "wilson")
        print(
            f"  n={n:5d}, p={p:.2f} (np={n * p:5.1f}): exact coverage of the nominal 95% interval:"
            f" Wald"
            f" {cov_w:.3f}, Wilson {cov_s:.3f}"
        )
    cov_w = coverage(30, 0.02, "wald")
    require(failed, "Wald coverage below 0.6 at n = 30, p = 0.02", bool(cov_w < 0.6))
    none = ProportionEstimate(successes=0, trials=30)
    lo0, hi0 = none.wald_interval()
    lo_s, hi_s = none.wilson_interval()
    print(
        f"  zero successes in 30: Wald interval [{lo0:.3f}, {hi0:.3f}] (degenerate); Wilson"
        f" [{lo_s:.3f}, {hi_s:.3f}]"
    )
    require(failed, "zero successes give a degenerate Wald interval", bool(lo0 == hi0 == 0.0))
    print(
        "  Lehalle and Laruelle's rule of thumb is n p > 5 and n (1 - p) > 5 with the true p (p."
        " 286),"
        " not the estimate"
    )
    return failed


def check_power_and_inference(rng: np.random.Generator) -> list[str]:
    """Part 8: t-test power, the sampling frequency, serial correlation and selection."""
    failed: list[str] = []
    section("8. t-test power and data requirements (Harris, chap. 22)")
    s_adj = np.sqrt(16**2 + 14.5**2 - 2 * 0.9 * 16 * 14.5)
    print(
        f"  market-adjusted sd sqrt(16^2 + 14.5^2 - 2 x 0.9 x 16 x 14.5) = {s_adj:.2f}% a year"
        f" (Harris:"
        " 7.0)"
    )
    require(failed, "market-adjusted sd 6.97", bool(abs(s_adj - 6.97) < 0.01))
    print(
        f"  power of the one-sided 95% test, skill 2%, sd 7%: 5 years {HARRIS.power(5):.3f}, 10"
        " years"
        f" {HARRIS.power(10):.3f} (Harris: 15% and 23%)"
    )
    require(
        failed,
        "power 15% at 5 years and 23% at 10 years",
        bool(abs(HARRIS.power(5) - 0.15) < 0.01 and abs(HARRIS.power(10) - 0.23) < 0.01),
    )
    table = {
        (0.75, 0.75, 2): 22,
        (0.95, 0.95, 2): 132,
        (0.50, 0.95, 2): 33,
        (0.95, 0.95, 4): 33,
        (0.75, 0.75, 4): 6,
    }
    for (c, pw, sk), h in table.items():
        y = SkillTest(skill=sk, sd=7.0, confidence=c).years_needed(pw)
        print(
            f"  years for confidence {c:.0%}, power {pw:.0%}, skill {sk}%: ((z_c + z_p) sd /"
            f" skill)^2 = {y:.1f}"
            f" (Harris, Table 22-3: {h})"
        )
        require(
            failed,
            f"years for confidence {c:.0%}, power {pw:.0%}, skill {sk}% match Table 22-3",
            bool(abs(y - h) < 1.0),
        )
    print(
        "  so detecting an edge mu with noise sigma needs n = ((z_{1-alpha} + z_power) sigma/mu)^2"
        " periods,"
        " of order (sigma/mu)^2"
    )
    # sampling frequency over a fixed span
    mu_a, sd_a, years = 0.02, 0.07, 10
    tstats: dict[str, float] = {}
    for label, per_year in [("annual", 1), ("monthly", 12), ("daily", 250)]:
        n = years * per_year
        x = rng.normal(mu_a / per_year, sd_a / np.sqrt(per_year), (20_000, n))
        t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(n))
        tstats[label] = t.mean()
    print(
        "  mean t-statistic over 10 years, skill 2%, sd 7%: "
        + ", ".join(f"{k} {v:.2f}" for k, v in tstats.items())
        + f" (mu sqrt(T)/sigma = {mu_a * np.sqrt(years) / sd_a:.2f}): sampling more often does not"
        + " add history"
    )
    require(
        failed,
        "monthly and daily mean t-statistics agree",
        bool(abs(tstats["monthly"] - tstats["daily"]) < 0.05),
    )
    # serially correlated returns: the naive standard error is too small
    phi, n = 0.3, 2500
    e = rng.normal(0, 1, (4000, n))
    x = np.empty_like(e)
    x[:, 0] = e[:, 0]
    for i in range(1, n):
        x[:, i] = phi * x[:, i - 1] + e[:, i]
    t0 = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(n))
    print(
        f"  AR(1) returns with phi = {phi}, true mean 0: sd of the naive t {t0.std():.2f} (1 if"
        f" valid;"
        f" theory sqrt((1+phi)/(1-phi)) = {np.sqrt((1 + phi) / (1 - phi)):.2f}); effective sample"
        f" {n * (1 - phi) / (1 + phi):.0f} of {n}"
    )
    require(
        failed,
        "AR(1) naive t has sd sqrt((1+phi)/(1-phi))",
        bool(abs(t0.std() - np.sqrt((1 + phi) / (1 - phi))) < 0.05),
    )
    # the best of many unskilled managers (Harris's Buffett box, p. 463)
    t_b = 11.8 / (14.3 / np.sqrt(36))
    p1 = stats.norm.sf(t_b)
    print(
        f"  Buffett box: t = 11.8/(14.3/6) = {t_b:.2f}; one unskilled manager exceeds it with"
        f" probability"
        f" {p1:.2e} (normal), {stats.t.sf(t_b, 35):.2e} (t, 35 df; Harris 0.0011%)"
    )
    for m_, harris in [(10_000, "0.5%"), (100_000, "5%")]:
        print(
            f"    best of {m_:,} unskilled managers beats 11.8%: {1 - (1 - p1) ** m_:.4f} (normal"
            f" averages;"
            f" Harris {harris})"
        )
    # regression to the mean after selection
    tau, sig_l = 0.5, 1.0
    skill = rng.normal(0, tau, 200_000)
    y1 = skill + rng.normal(0, sig_l, skill.size)
    y2 = skill + rng.normal(0, sig_l, skill.size)
    top = y1 > np.quantile(y1, 0.9)
    print(
        f"  top decile on period 1: mean {y1[top].mean():.2f}, then {y2[top].mean():.2f} in period"
        f" 2; ratio"
        f" {y2[top].mean() / y1[top].mean():.2f} against the shrinkage tau^2/(tau^2+sigma^2) ="
        f" {tau**2 / (tau**2 + sig_l**2):.2f}"
    )
    require(
        failed,
        "regression to the mean matches the shrinkage tau^2/(tau^2+sigma^2)",
        bool(abs(y2[top].mean() / y1[top].mean() - tau**2 / (tau**2 + sig_l**2)) < 0.02),
    )
    # a short-volatility return stream: high t in samples without a crash
    p_crash, gain, loss, months = 0.02, 0.01, -0.40, 60
    mean_m = (1 - p_crash) * gain + p_crash * loss
    print(
        f"  short volatility: +1% a month, -40% with probability 2%: true mean {mean_m:+.2%} a"
        f" month; "
        f"P(no crash in 60 months) = {(1 - p_crash) ** months:.2f}, and those samples show zero"
        f" variance"
        " and an unbounded t"
    )
    require(
        failed,
        "short volatility: positive mean and a 30% chance of no crash",
        bool(mean_m > 0 and abs((1 - p_crash) ** months - 0.30) < 0.01),
    )
    return failed


def check_regression_averaging(rng: np.random.Generator) -> list[str]:
    """Part 9: R^2 definitions, index spreads and volatilities, and the averaging effect."""
    failed: list[str] = []
    section(
        "9. regression fit, R^2 and the averaging effect (Lehalle and Laruelle, apps. A.10 and"
        " A.14)"
    )
    x = rng.lognormal(3, 0.6, 500)
    y = 2.5 + 0.05 * x + rng.normal(0, 1.5, 500)
    b1 = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
    b0 = y.mean() - b1 * x.mean()
    yh = b0 + b1 * x
    r2_a = 1 - np.sum((y - yh) ** 2) / np.sum((y - y.mean()) ** 2)
    r2_b = np.sum((yh - y.mean()) ** 2) / np.sum((y - y.mean()) ** 2)
    print(
        f"  OLS with an intercept: 1 - RSS/TSS = {r2_a:.4f} = ESS/TSS = {r2_b:.4f} = r^2 ="
        f" {np.corrcoef(x, y)[0, 1] ** 2:.4f}"
    )
    require(
        failed,
        "three R^2 definitions agree under OLS with an intercept",
        bool(abs(r2_a - r2_b) < 1e-12 and abs(r2_a - np.corrcoef(x, y)[0, 1] ** 2) < 1e-12),
    )
    # LL's multiplicative predictor: the two definitions differ
    ly, lx = np.log(np.abs(y) + 0.1), np.log(x)
    c1 = np.polyfit(lx, ly, 1)
    res = ly - np.polyval(c1, lx)
    pred = np.exp(np.polyval(c1, lx)) * np.exp(res.var(ddof=2) / 2) - 0.1
    r2_ess = np.sum((pred - y.mean()) ** 2) / np.sum((y - y.mean()) ** 2)
    r2_rss = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    print(
        f"  back-transformed log-log predictor: ESS/TSS {r2_ess:.4f} against 1 - RSS/TSS"
        f" {r2_rss:.4f}"
        " (LL's R'^2 uses ESS/TSS)"
    )
    require(
        failed,
        "the two R^2 definitions differ for the log-log predictor",
        bool(abs(r2_ess - r2_rss) > 1e-3),
    )
    # index spread and volatility
    N, Tn = 30, 2000
    w = rng.dirichlet(np.ones(N))
    S = rng.uniform(20, 200, N)
    half = rng.uniform(0.005, 0.05, N)  # absolute half-spreads
    idx_spread_abs = np.sum(w * 2 * half)
    idx_level = np.sum(w * S)
    rel_stock = 2 * half / S
    print(
        f"  absolute spreads aggregate: index ask - bid = sum w (ask - bid) = {idx_spread_abs:.5f};"
        f" relative"
        f" spreads do not: index {idx_spread_abs / idx_level:.6f} against sum w psi_rel"
        f" {np.sum(w * rel_stock):.6f}"
    )
    require(
        failed,
        "absolute spreads aggregate; relative spreads need the price weights",
        bool(abs(idx_spread_abs / idx_level - np.sum(w * S * rel_stock) / idx_level) < 1e-12),
    )
    corr = 0.4
    cov = corr * np.ones((N, N)) + (1 - corr) * np.eye(N)
    vols = rng.uniform(0.01, 0.03, N) * S
    dS = rng.multivariate_normal(np.zeros(N), cov * np.outer(vols, vols), 5000)
    sig_I = np.std(dS @ w)
    sig_w = np.sum(w * vols)
    print(
        f"  price-change volatilities, correlation {corr}: index {sig_I:.3f} against sum w sigma_k"
        f" {sig_w:.3f} (subadditive)"
    )
    require(failed, "index volatility is subadditive", bool(sig_I < sig_w))
    # regression of index quantities against the average of stock regressions
    a0, a1 = 0.02, 2.5
    c_common, n_intra = 0.6, 50
    regime = rng.lognormal(0, 0.4, Tn)  # common volatility level of each period
    level = rng.uniform(0.5, 1.5, N)  # stock-specific volatility scale
    vol = 1e-3 * np.outer(regime, level) * (1 + 0.5 * rng.random((Tn, N)))
    F = rng.normal(0, 1, (Tn, n_intra))  # common intraperiod shocks
    E = rng.normal(0, 1, (Tn, N, n_intra))  # idiosyncratic intraperiod shocks
    ret = vol[:, :, None] * (np.sqrt(c_common) * F[:, None, :] + np.sqrt(1 - c_common) * E)
    sig_k = ret.std(axis=2, ddof=1)  # realised stock volatilities per period
    sig_I_t = np.einsum("k,tkj->tj", w, ret).std(
        axis=1, ddof=1
    )  # realised index volatility per period
    psi_k = a0 + a1 * sig_k + rng.normal(0, 1e-3, (Tn, N))
    psi_I = psi_k @ w
    coef_stock = np.array([np.polyfit(sig_k[:, j], psi_k[:, j], 1) for j in range(N)])
    avg_slope = np.sum(w * coef_stock[:, 0])
    idx_slope = np.polyfit(sig_I_t, psi_I, 1)[0]
    print(
        f"  stock slopes average {avg_slope:.3f} (true {a1}); slope of the index spread on the"
        f" index"
        f" volatility {idx_slope:.3f}: higher, because the index volatility is below the weighted"
        f" average"
        " of the stock volatilities"
    )
    require(failed, "index slope exceeds the average stock slope", bool(idx_slope > avg_slope))
    print(
        "  LL's A.14.2 defines abar_1 as sum w_k a^k_0 (p. 320), a printing slip for sum w_k a^k_1"
    )
    # mean against path
    days = 500
    bins = 100
    spikes = rng.integers(10, 90, days)
    paths = np.ones((days, bins))
    for d_, s_ in enumerate(spikes):
        paths[d_, s_ : s_ + 3] += 6
    mean_path = paths.mean(axis=0)
    print(
        f"  500 days, each calm with one 3-bin spike at a random time: the average profile peaks at"
        f" {mean_path.max():.2f}, every single day at 7.00; no day looks like the average"
    )
    require(failed, "the average profile stays below 1.5 at its peak", bool(mean_path.max() < 1.5))
    return failed


def check_hedged_spread(rng: np.random.Generator) -> list[str]:
    """Part 10: a spread's factor exposure with a hedge ratio, and its variance."""
    failed: list[str] = []
    section("10. factor exposure of a hedged spread")
    bi, bj = np.array([1.2, 0.3]), np.array([0.8, 0.5])
    for h in [1.0, bi[0] / bj[0]]:
        print(
            f"  r_i - h r_j with h = {h:.3f}: factor exposure beta_i - h beta_j ="
            f" {np.round(bi - h * bj, 3)} "
            "(beta_i - beta_j is the case h = 1)"
        )
    require(
        failed,
        "the hedge ratio removes the first factor exposure",
        bool(np.allclose((bi - (bi[0] / bj[0]) * bj)[0], 0.0)),
    )
    f = rng.normal(0, 0.01, (100_000, 2))
    ei = rng.normal(0, 0.005, 100_000)
    ej = rng.normal(0, 0.005, 100_000)
    ri = f @ bi + ei
    rj = f @ bj + ej
    h = 1.5
    spread = ri - h * rj
    pred_var = (bi - h * bj) @ np.diag([1e-4, 1e-4]) @ (bi - h * bj) + 0.005**2 * (1 + h**2)
    print(
        f"  simulated spread variance {spread.var():.3e} against (beta_i - h beta_j)' Sigma_f"
        f" (beta_i - h"
        f" beta_j) + var(e_i) + h^2 var(e_j) = {pred_var:.3e}"
    )
    require(
        failed,
        "simulated spread variance matches the factor formula",
        bool(abs(spread.var() / pred_var - 1) < 0.02),
    )
    return failed


def main() -> int:
    """Run the ten parts with one generator, print each failed check as BAD, and return 0 or 1.

    Each section prints its result and asserts what the entries state.

    1. Harris's inside spread (Table 13-1, p. 281) (def:dealer-quotes-order-flow).
    2. Cyclic currency arbitrage: Harris's box (p. 357) recomputed, and the no-arbitrage band with
       bid and ask quotes (def:arbitrage).
    3. Make/take fees and the speed race: Lehalle and Laruelle's eq. (A.4), after Foucault, Kadan
       and Kandel, re-derived and checked against a finite-population equilibrium
       (mod:make-take-fee-speed-race).
    4. The toy flash-crash model (Lehalle and Laruelle, app. A.5): the hot-potato rate, the
       overflow, and the time term of eq. (A.14) (mod:depth-overflow-flash-crash).
    5. The May 2010 report's arithmetic (ev:may-2010-flash-crash).
    6. Queue-position values in Moallemi and Yuan's Table 3 (res:queue-position-value).
    7. Proportion intervals: the normal (Wald) interval against Wilson's, and the rule of thumb
       (meth:venue-market-share).
    8. Harris's t-test power and data requirements (Tables 22-2 and 22-3), sampling frequency, the
       best of many managers, regression to the mean and a short-volatility return stream
       (meth:skill-luck-significance-tests).
    9. Regression fit, R^2 definitions, and the averaging effect: index spreads and volatilities,
       and the regression of averages against the average of regressions
       (meth:spread-volatility-regression, meth:intraday-deseasonalisation).
    10. A spread's factor exposure with a hedge ratio (res:arbitrage-risks).

    One generator, seeded 36, serves parts 2, 4, 8, 9 and 10 in order; the other parts draw nothing.
    Each part returns the names of its failed checks; a failure prints BAD and exits 1.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    failed = [
        *check_inside_spread(),
        *check_cyclic_arbitrage(rng),
        *check_make_take(),
        *check_flash_crash(rng),
        *check_may_2010(),
        *check_queue_position(),
        *check_proportions(),
        *check_power_and_inference(rng),
        *check_regression_averaging(rng),
        *check_hedged_spread(rng),
    ]
    for name in failed:
        print("BAD", name)
    if failed:
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
