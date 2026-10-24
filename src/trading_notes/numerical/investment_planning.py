"""Investment planning case: the return requirement, allocations, a concentrated stock and biases.

Investment planning case (2026-10-18; tax and transition corrections the same day): the worked
numbers of meth:investment-policy-statement, meth:asset-class-portfolio-construction,
ex:investment-planning-case, def:behavioural-biases and meth:risk-identification-modification.

A fictional client: age 50, 2,000,000 investable (currency units of an unnamed jurisdiction), of
which 150,000 is needed for a renovation in 18 months and 50,000 is held as an emergency reserve;
real after-tax savings of 40,000 a year (end of year) for 12 years; real after-tax spending of
145,000 a year from the portfolio for 30 years from age 62, withdrawn at the start of each year.
Inflation 2.5 percent is hypothetical.

Tax basis (hypothetical, stated so that no tax is counted twice):
- a flat 15 percent tax on every year's nominal return as earned, losses fully offset; withdrawals
  are not taxed again, so savings, spending and the required return are real and after tax;
- capital market assumptions are real and pre-tax; with nominal return (1 + r)(1 + pi) - 1 taxed at
  t, the after-tax real return is exactly (1 - t) r - t pi / (1 + pi), so its mean and sd follow
  linearly;
- a 20 percent tax applies only to the 300,000 gain already embedded in the inherited stock
  (400,000). The stock is sold in thirds now, in 12 and in 24 months, at today's value, and 20,000
  (nominal) is paid from the long-term pool at the end of each of years 1-3. The stock's returns
  from today are taxed like all others at 15 percent.

The transition risk (part 3) uses the five-asset weights with the stock carved out of the equity
sleeve. The stock's expected real return is assumed equal to global equity's 5.5 percent (no view on
the stock); a beta-consistent alternative, 0.5 + 1.3125 x 5.0 = 7.06 percent, is also checked. The
capital market assumptions are invented for teaching, not forecasts. The risk objective
(5th-percentile one-year real loss no worse than -13 percent) is measured on pre-tax returns, the
fall in portfolio value before any tax offset; the after-tax alternative is also reported.

Part 4 reproduces Edwards's urn calculation as quoted by Barberis and Thaler (NBER w9222, p. 14):
posterior 0.97.

No random draws.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.investment_planning
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import OptimizeResult, brentq, minimize, minimize_scalar
from scipy.stats import norm

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

INVESTABLE: Final = 2_000_000
RENOVATION: Final = 150_000
RESERVE: Final = 50_000
A0: Final = INVESTABLE - RENOVATION - RESERVE
S: Final = 40_000  # real savings a year, end of year
N_SAVE: Final = 12
W: Final = 145_000  # real spending a year, start of year
N_DRAW: Final = 30
INFL: Final = 0.025
TAX: Final = 0.15
CGT: Final = 0.20
CONC: Final = 400_000  # the inherited stock at today's value
GAIN: Final = 300_000  # its gain, taxed at CGT on the sale
GAINS_TAX: Final = tuple((k, GAIN * CGT / 3 / (1 + INFL) ** k) for k in (1, 2, 3))  # (year, real)
LOSS_LIMIT: Final = -13.0  # percent: one-year 5th-percentile real loss (pre-tax) must not be worse
DRAG: Final = (
    100 * TAX * INFL / (1 + INFL)
)  # percent: tax on the inflation part of the nominal return
Z5: Final = norm.ppf(0.05)


def fv_at_62(
    r: float, savings: float = S, years: int = N_SAVE, with_gains_tax: bool = True
) -> float:
    """Return the real value at 62 of the long-term pool, net of the gains tax if asked."""
    v = A0 * (1 + r) ** years + savings * ((1 + r) ** years - 1) / r
    if with_gains_tax:
        v -= sum(x * (1 + r) ** (years - k) for k, x in GAINS_TAX)
    return v


def pv_need(r: float, spend: float = W, years: int = N_DRAW) -> float:
    """Return the present value at 62 of the spending, an annuity due."""
    return spend * (1 - (1 + r) ** -years) / r * (1 + r)  # annuity due


def capital_market_assumptions() -> tuple[Floats, Floats, Floats]:
    """Return the real pre-tax means, standard deviations and correlations of the four classes."""
    mu = np.array([5.5, 1.5, 1.2, 0.5])  # percent, real, pre-tax, arithmetic
    sd = np.array([16.0, 6.0, 5.0, 1.0])
    C = np.array([[1, 0.1, 0.2, 0.0], [0.1, 1, 0.7, 0.1], [0.2, 0.7, 1, 0.1], [0.0, 0.1, 0.1, 1]])
    return mu, sd, C


def mix_stats(w: Floats, mu: Floats, V: Floats) -> dict[str, float]:
    """Return the pre- and after-tax statistics of the mix w, in percent."""
    m, s = np.float64(w @ mu), math.sqrt(w @ V @ w)
    m_at, s_at = (1 - TAX) * m - DRAG, (1 - TAX) * s
    return {
        "mean": m,
        "sd": s,
        "q5": m + Z5 * s,
        "mean_at": m_at,
        "sd_at": s_at,
        "geo_at": m_at - s_at * s_at / 200,  # geometric approximation, percent units
        "q5_at": m_at + Z5 * s_at,
    }


def best_within_limit(
    limit_key: str, mixes: dict[str, Floats], mu: Floats, V: Floats
) -> tuple[Floats, dict[str, float]]:
    """Return the long-only mix with the highest after-tax geometric return within the loss limit.

    Args:
        limit_key: The statistic that the loss limit applies to.
        mixes: The candidate mixes, from which the search starts.
        mu: The pre-tax means of the four classes.
        V: The covariance matrix of the four classes, in percent squared.
    """

    def slack(w: Floats) -> float:
        v = mix_stats(w, mu, V)
        return v[limit_key] - LOSS_LIMIT

    def neg_geo(w: Floats) -> float:
        return -mix_stats(w, mu, V)["geo_at"]

    def budget(w: Floats) -> float:
        gap: float = w.sum() - 1
        return gap

    best: OptimizeResult[np.float64] | None = None
    starts: list[Floats] = [mixes["balanced"], np.full(4, 0.25), np.array([0.6, 0.4, 0.0, 0.0])]
    for x0 in starts:
        r = minimize(
            neg_geo,
            x0,
            method="SLSQP",
            bounds=[(0, 1)] * 4,
            constraints=[
                {"type": "eq", "fun": budget},
                {"type": "ineq", "fun": slack},
            ],
            options={"ftol": 1e-14, "maxiter": 500},
        )
        if best is None or r.fun < best.fun:
            best = r
    assert best is not None
    x_best = np.asarray(best.x, dtype=np.float64)
    return x_best, mix_stats(x_best, mu, V)


def check_return_requirement(report: CheckReport) -> float:
    """Part 1: the real after-tax return the plan requires, with the gains tax and the pre-tax map.

    Args:
        report: The run's report.

    Returns:
        The required real after-tax return, as a fraction.
    """
    print("== part 1: return requirement (real, after tax)")
    r_base = brentq(lambda r: fv_at_62(r, with_gains_tax=False) - pv_need(r), 1e-6, 0.2)
    r_req = brentq(lambda r: fv_at_62(r) - pv_need(r), 1e-6, 0.2)
    report.ok(
        "long-term pool 1,800,000 after setting aside 200,000 for the renovation and reserve",
        A0 == 1_800_000,
    )
    report.ok(
        "the stock sale realises 60,000 of gains tax: 20,000 nominal at the end of years 1-3"
        " (19,512, 19,036, 18,571 real)",
        close(sum(GAIN * CGT / 3 for _ in GAINS_TAX), 60_000)
        and np.allclose([x for _, x in GAINS_TAX], [19_512.195, 19_036.288, 18_571.988], atol=1e-3),
    )
    report.ok(
        "ignoring the gains tax the requirement would be 2.699%",
        abs(r_base - 0.0269872) < 1e-6,
    )
    report.ok(
        "paying it from the pool raises the required real after-tax return to 2.808%",
        abs(r_req - 0.0280809) < 1e-6,
    )
    report.ok(
        "at 2.808% the pool reaches 2,995,705 at 62, the present value of the spending",
        abs(fv_at_62(r_req) - pv_need(r_req)) < 1e-6 and abs(fv_at_62(r_req) - 2_995_705) < 1,
    )
    # Independent check: roll the account forward year by year at r_req, paying the gains tax and
    # saving at year ends.
    bal: float = A0
    for yr in range(1, N_SAVE + 1):
        bal = bal * (1 + r_req) + S - sum(x for k, x in GAINS_TAX if k == yr)
    for _ in range(N_DRAW):
        bal = (bal - W) * (1 + r_req)
    report.ok(
        "year-by-year roll-forward ends at zero after 30 withdrawals",
        abs(bal) < 1e-3,
        f"{bal:.6f}",
    )
    nominal = (1 + r_req) * (1 + INFL) - 1
    pretax = nominal / (1 - TAX)
    pretax_real = (1 + pretax) / (1 + INFL) - 1
    report.ok(
        "nominal after-tax requirement (1.02808)(1.025) - 1 = 5.38%",
        abs(nominal - 0.053783) < 1e-5,
    )
    report.ok(
        "pre-tax nominal, taxing all nominal returns at 15% every year: 6.33%",
        abs(pretax - 0.063274) < 1e-5,
    )
    report.ok(
        "pre-tax real 3.73%, the same as inverting the after-tax map (r + t pi/(1 + pi))/(1 - t)",
        abs(pretax_real - 0.037339) < 1e-5
        and close(pretax_real, (r_req + TAX * INFL / (1 + INFL)) / (1 - TAX), 1e-12),
    )
    report.ok(
        "the additive shortcut (2.81 + 2.5)/0.85 = 6.24% understates the pre-tax nominal"
        " requirement",
        abs((r_req + INFL) / (1 - TAX) - 0.062448) < 1e-5,
    )

    # Maginn, Tuttle, McLeavey and Pinto (MIP, 3rd ed., 2007, chap. 1, p. 14): two
    # required-return examples.
    report.ok(
        "MIP p. 14: (2.0m / 1.2m)^(1/18) - 1 = 2.88% after tax",
        abs((2.0 / 1.2) ** (1 / 18) - 1 - 0.0288) < 5e-5,
    )
    r_wd = brentq(
        lambda r: 1.2e6 * (1 + r) ** 18 - 25_000 * ((1 + r) ** 18 - 1) / r - 2.0e6, 1e-6, 0.2
    )
    report.ok(
        "MIP p. 14: with 25,000 withdrawn at each year end, 4.55% after tax; 7.0% pre-tax at a 35%"
        " tax rate",
        abs(r_wd - 0.0455) < 5e-5 and abs(r_wd / 0.65 - 0.070) < 5e-4,
    )
    report.ok(
        "MIP p. 14: retiree (4% + 2%)/(1 - 0.40) = 10% pre-tax nominal (an additive approximation)",
        close((0.04 + 0.02) / 0.60, 0.10),
    )
    return r_req


def check_allocations(report: CheckReport, r_req: float) -> None:
    """Part 2: candidate strategic allocations against the requirement and the loss limit.

    Args:
        report: The run's report.
        r_req: The required real after-tax return, from part 1.
    """
    print("== part 2: candidate strategic allocations against the requirement and the loss limit")
    mu, sd, C = capital_market_assumptions()
    V = np.outer(sd, sd) * C
    report.ok("correlation matrix is positive definite", bool(np.all(np.linalg.eigvalsh(C) > 0)))
    report.ok(
        "tax on inflation costs 0.366 points of real return a year",
        abs(DRAG - 0.365854) < 1e-6,
    )
    # Independent check of the linear after-tax map on one return.
    r_test = 0.07
    direct = (1 + (1 - TAX) * ((1 + r_test) * (1 + INFL) - 1)) / (1 + INFL) - 1
    report.ok(
        "after-tax real return = (1 - t) r - t pi/(1 + pi), exactly",
        close(direct, (1 - TAX) * r_test - TAX * INFL / (1 + INFL), 1e-15),
    )
    mixes = {
        "conservative": np.array([0.30, 0.50, 0.15, 0.05]),
        "balanced": np.array([0.55, 0.30, 0.10, 0.05]),
        "growth": np.array([0.75, 0.15, 0.05, 0.05]),
    }
    res = {k: mix_stats(w, mu, V) for k, w in mixes.items()}
    for k, v in res.items():
        print(
            f"    {k:12s} pre-tax mean {v['mean']:.3f} sd {v['sd']:.3f} 5th pct {v['q5']:.3f} | "
            f"after-tax mean {v['mean_at']:.3f} sd {v['sd_at']:.3f} geometric~ {v['geo_at']:.3f}"
            f" 5th pct {v['q5_at']:.3f}"
        )
    req = 100 * r_req
    report.ok(
        "conservative: after-tax geometric 1.70 < 2.81 (fails the return requirement); 5th pct"
        " -7.81",
        abs(res["conservative"]["geo_at"] - 1.7035) < 1e-3 and res["conservative"]["geo_at"] < req,
    )
    report.ok(
        "balanced: pre-tax mean 3.62, sd 9.34; after tax mean 2.71, sd 7.93, geometric 2.396 <"
        " 2.81;"
        " 5th pct -11.73",
        abs(res["balanced"]["sd"] - 9.3351) < 1e-3
        and abs(res["balanced"]["mean_at"] - 2.7111) < 1e-3
        and abs(res["balanced"]["geo_at"] - 2.3963) < 1e-3
        and res["balanced"]["geo_at"] < req
        and res["balanced"]["q5"] > LOSS_LIMIT,
    )
    report.ok(
        "growth: after-tax geometric 2.87 meets the requirement, but the 5th percentile -15.61"
        " breaches -13",
        abs(res["growth"]["geo_at"] - 2.8672) < 1e-3
        and res["growth"]["geo_at"] >= req
        and abs(res["growth"]["q5"] + 15.6134) < 1e-3
        and res["growth"]["q5"] < LOSS_LIMIT,
    )
    report.ok(
        "with full loss offset the after-tax 5th percentiles are -7.01, -10.34 and -13.64: the same"
        " verdicts",
        np.allclose([res[k]["q5_at"] for k in mixes], [-7.0066, -10.3405, -13.6373], atol=1e-3),
    )
    report.ok(
        "so no candidate meets both objectives",
        [k for k, v in res.items() if v["geo_at"] >= req and v["q5"] >= LOSS_LIMIT] == [],
    )

    # The best any long-only mix of the four classes can do within the loss limit.
    w_pre, v_pre = best_within_limit("q5", mixes, mu, V)
    w_post, v_post = best_within_limit("q5_at", mixes, mu, V)
    print(
        f"    best within the pre-tax limit {np.round(w_pre, 4)}; within the after-tax limit"
        f" {np.round(w_post, 4)}"
    )
    report.ok(
        "best long-only mix within the pre-tax limit is about 61/39/0/0 and earns 2.61 after tax:"
        " still 0.20 short",
        np.allclose(w_pre, [0.6133, 0.3867, 0, 0], atol=2e-3)
        and abs(v_pre["geo_at"] - 2.6106) < 1e-3,
    )
    report.ok(
        "measured after tax with full loss offset, 71/29/0/0 would just reach 2.83 (0.03 above),"
        " with no ILB or cash",
        bool(
            np.allclose(w_post, [0.711, 0.289, 0, 0], atol=2e-3)
            and abs(v_post["geo_at"] - 2.8339) < 1e-3
            and v_post["geo_at"] - req < 0.05
        ),
    )
    # Funding gap at the balanced mix's after-tax geometric return.
    g_bal = res["balanced"]["geo_at"] / 100
    spend_ok = fv_at_62(g_bal) / (pv_need(g_bal) / W)
    save_ok = brentq(lambda x: fv_at_62(g_bal, savings=x) - pv_need(g_bal), 0, 500_000)
    surplus = {
        d: fv_at_62(g_bal, years=N_SAVE + d) - pv_need(g_bal, years=N_DRAW - d) for d in (0, 1, 2)
    }
    print(
        f"    at {100 * g_bal:.3f}%: sustainable spending {spend_ok:,.0f}; savings needed"
        f" {save_ok:,.0f}; "
        f"surplus at retirement by delay {dict((d, round(v)) for d, v in surplus.items())}"
    )
    report.ok(
        "at 2.40% the plan is short by 283,249 at 62; it supports spending of about 132,000, not"
        " 145,000",
        abs(-surplus[0] - 283_249) < 1 and abs(spend_ok - 131_966) < 1,
    )
    report.ok(
        "or savings of about 60,650 a year instead of 40,000",
        abs(save_ok - 60_652) < 1,
    )
    report.ok(
        "or retiring at 64 (spending to 92): short by 101,562 at 63, 84,479 to spare at 64",
        abs(surplus[1] + 101_562) < 1 and abs(surplus[2] - 84_479) < 1,
    )
    # Risk contributions (Euler): RC_i = w_i (V w)_i / sigma, summing to sigma.
    w = mixes["balanced"]
    s = math.sqrt(w @ V @ w)
    rc = w * (V @ w) / s
    report.ok("risk contributions sum to portfolio sd", close(rc.sum(), s))
    report.ok("equity is 55% of capital but 91.7% of variance risk", abs(rc[0] / s - 0.9169) < 1e-4)
    # Rebalancing ranges: +/- 5 points on equity, +/- 4 on bonds, +/- 2 on others; the drift
    # example.
    drift = w * np.array([1.18, 0.99, 1.00, 1.00])
    drift = drift / drift.sum()
    report.ok(
        "an 18% equity rally with a 1% bond fall moves equity to 59.2%, inside 50-60%",
        abs(drift[0] - 0.5922) < 1e-4 and 0.50 <= drift[0] <= 0.60,
    )


def check_concentrated(report: CheckReport) -> None:
    """Part 3: the concentrated holding during the staged sale, hedged and unhedged.

    Args:
        report: The run's report.
    """
    print("== part 3: concentrated holding during the staged sale, hedged and unhedged")
    mu, sd, C = capital_market_assumptions()
    report.ok("the single stock is 22.2% of the long-term pool", abs(CONC / A0 - 0.2222) < 1e-4)
    report.ok(
        "selling it at once would also realise 60,000 of tax (3.3% of the pool): staging at a flat"
        " rate defers it",
        close(GAIN * CGT, 60_000) and abs(GAIN * CGT / A0 - 0.0333) < 1e-4,
    )
    sd_stock, rho = 35.0, 0.6
    sd5 = np.append(sd, sd_stock)
    C5 = np.eye(5)
    C5[:4, :4] = C
    C5[0, 4] = C5[4, 0] = rho
    C5[1, 4] = C5[4, 1] = 0.1
    C5[2, 4] = C5[4, 2] = 0.15
    V5 = np.outer(sd5, sd5) * C5
    report.ok(
        "five-asset correlation matrix is positive definite",
        bool(np.all(np.linalg.eigvalsh(C5) > 0)),
    )
    beta_stock = V5[0, 4] / V5[0, 0]
    spec_sd = math.sqrt(V5[4, 4] - beta_stock**2 * V5[0, 0])
    report.ok(
        "stock beta to global equity 1.3125; specific sd 28%, i.e. 6.2 points of sd at a 22.2%"
        " weight",
        close(beta_stock, 1.3125)
        and close(spec_sd, 28.0)
        and abs(CONC / A0 * spec_sd - 6.2222) < 1e-4,
    )

    def stage(x_stock: float, hedge: float, mu_stock: float) -> tuple[float, float, float]:
        """Return the mean, the sd and the 5th-percentile return of the five-asset mix.

        The stock is carved out of the 55-point equity sleeve; a short index future on `hedge` of
        the pool earns minus the equity return over cash (basis ignored), i.e. moves `hedge` from
        equity to cash.
        """
        w5 = np.array([0.55 - x_stock - hedge, 0.30, 0.10, 0.05 + hedge, x_stock])
        m5 = np.append(mu, mu_stock)
        s5 = math.sqrt(w5 @ V5 @ w5)
        return w5 @ m5, s5, w5 @ m5 + Z5 * s5

    x_full, x_two, x_one = CONC / A0, 2 / 3 * CONC / A0, 1 / 3 * CONC / A0
    mu_eq, mu_beta = 5.5, 0.5 + beta_stock * 5.0
    m0, s0, q0 = stage(x_full, 0.0, mu_eq)
    m1, s1, q1 = stage(x_full, 0.10, mu_eq)
    print(
        f"    full holding: unhedged mean {m0:.3f} sd {s0:.4f} 5th {q0:.3f}; hedged mean {m1:.3f}"
        f" sd {s1:.4f} 5th {q1:.3f}"
    )
    report.ok(
        "keeping the stock raises portfolio sd from 9.34% to 12.19%",
        abs(s0 - 12.1912) < 1e-4,
    )
    report.ok(
        "a 10%-notional short index future with its cash leg lowers it to 10.89% and the mean by"
        " 0.50 points",
        abs(s1 - 10.8922) < 1e-4 and close(m0 - m1, 0.50),
    )
    report.ok(
        "but the hedged 5th percentile -14.80 still breaches the -13 limit (unhedged -16.43)",
        abs(q1 + 14.796) < 1e-3 and abs(q0 + 16.433) < 1e-3 and q1 < LOSS_LIMIT,
    )
    h_need = brentq(lambda h: stage(x_full, h, mu_eq)[2] - LOSS_LIMIT, 0.0, 0.5)
    h_minvar = minimize_scalar(
        lambda h: stage(x_full, h, mu_eq)[1], bounds=(0, 1), method="bounded"
    ).x
    report.ok(
        "with the full holding the limit needs about 22% notional; even the minimum-variance hedge"
        " leaves sd 6.75%",
        abs(h_need - 0.2227) < 1e-3 and abs(stage(x_full, h_minvar, mu_eq)[1] - 6.747) < 1e-3,
    )
    _, _, q_one_h = stage(x_two, 0.10, mu_eq)
    _, _, q_two_u = stage(x_one, 0.0, mu_eq)
    report.ok(
        "after the first third is sold, the 10% hedge meets the limit (-12.52); after the second,"
        " no hedge is needed (-12.73)",
        abs(q_one_h + 12.524) < 1e-3
        and q_one_h > LOSS_LIMIT
        and abs(q_two_u + 12.726) < 1e-3
        and q_two_u > LOSS_LIMIT,
    )
    qb = [
        stage(x_full, 0.0, mu_beta)[2],
        stage(x_full, 0.10, mu_beta)[2],
        stage(x_two, 0.10, mu_beta)[2],
        stage(x_one, 0.0, mu_beta)[2],
    ]
    report.ok(
        "with a beta-consistent 7.06% stock mean: -16.09, -14.45, -12.29, -12.61; the same"
        " verdicts",
        bool(
            np.allclose(qb, [-16.086, -14.449, -12.292, -12.610], atol=1e-3)
            and [q < LOSS_LIMIT for q in qb] == [True, True, False, False]
        ),
    )
    report.ok(
        "liquidity sleeve covers 18 months: 200,000 = renovation + reserve",
        RENOVATION + RESERVE == 200_000,
    )


def check_behaviour(report: CheckReport) -> None:
    """Part 4: the behavioural and governance numbers.

    Args:
        report: The run's report.
    """
    print("== part 4: behavioural and governance numbers")
    lr = (0.7 / 0.3) ** 8 * (
        0.3 / 0.7
    ) ** 4  # urn 1: 7 red, 3 blue; urn 2: 3 red, 7 blue; draw 8 red, 4 blue
    post = lr / (1 + lr)
    report.ok(
        "Edwards's urn: posterior 0.967 for 8 red and 4 blue (Bayes), against a typical answer of"
        " 0.7",
        abs(post - 0.9674) < 1e-4,
    )


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    r_req = check_return_requirement(report)
    check_allocations(report, r_req)
    check_concentrated(report)
    check_behaviour(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
