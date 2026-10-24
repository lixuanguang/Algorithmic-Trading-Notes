"""Credit risk, CDS, sovereign debt and securitisation: worked numbers by independent routes."""

import sys
from typing import Final

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq, fsolve
from scipy.stats import norm

from trading_notes.numerical.credit_risk_analysis.credit_instruments import (
    CreditDefaultSwap,
    MortgagePool,
    RiskyBond,
    absolute_priority_recovery,
    sequential_payoff_months,
    tranche_loss,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

RECOVERY: Final = 0.40
SPREAD_RATE: Final = 0.05


ARDEN: Final = RiskyBond(hazard=0.015, recovery=0.40, rate=0.03, coupon=5.0, years=3)
CDS: Final = CreditDefaultSwap(rate=SPREAD_RATE, recovery=RECOVERY, maturity=5.0, frequency=1)
POOL: Final = MortgagePool(balance=660e6, wac=0.06, pass_through_rate=0.055, wam=358, age=2)


def check_components(report: CheckReport) -> None:
    """Part 1: components of credit risk: default probability, loss given default and exposure.

    Args:
        report: The run's report.
    """
    print(
        "== part 1: components of credit risk - default probability, loss given default, exposure"
    )
    lam = 0.015
    Q = [1 - np.exp(-lam * t) for t in range(1, 6)]
    report.ok(
        "Hull Example 17.2: hazard 1.5% gives cumulative default 0.0149, 0.0296, 0.0440, 0.0582,"
        " 0.0723; unconditional year-4 default 0.0142, conditional 0.0149",
        [round(q, 4) for q in Q] == [0.0149, 0.0296, 0.044, 0.0582, 0.0723]
        and round(Q[3] - Q[2], 4) == 0.0142
        and round((Q[3] - Q[2]) / (1 - Q[2]), 4) == 0.0149,
    )
    cum = {  # Hull Table 17.1, cumulative default rates (%), years 1-5, 7, 10, 15
        "A": [0.05, 0.13, 0.22, 0.33, 0.46],
        "BBB": [0.16, 0.43, 0.75, 1.14, 1.54],
        "CCC/C": [28.30, 38.33, 43.42, 46.36, 48.58],
    }
    unc = {k: np.diff([0.0, *v]) for k, v in cum.items()}
    report.ok(
        "Table 17.1: BBB year-2 unconditional default 0.27%; CCC/C year-3 conditional 8.25% (5.09 /"
        " 61.67)",
        round(unc["BBB"][1], 2) == 0.27 and round(unc["CCC/C"][2] / (100 - 38.33), 4) == 0.0825,
    )
    report.ok(
        "the term structure of default is rising for A (0.05, 0.08, 0.09, 0.11) and falling for"
        " CCC/C (28.30, 10.03, 5.09, 2.94)",
        [round(x, 2) for x in unc["A"][:4]] == [0.05, 0.08, 0.09, 0.11]
        and [round(x, 2) for x in unc["CCC/C"][:4]] == [28.30, 10.03, 5.09, 2.94],
    )
    # A loan: drawn 6, undrawn 4 with half expected to be drawn by default; PD 2%, LGD 60%.
    ead = 6.0 + 0.5 * 4.0
    el = 0.02 * 0.60 * ead
    report.ok(
        "loan: exposure at default 8.0 (6 drawn + half of 4 undrawn), expected loss 0.02 x 0.60 x"
        " 8.0 = 0.096",
        close(ead, 8.0) and close(el, 0.096),
    )
    spread7 = {
        "AAA": 35.74,
        "AA": 43.67,
        "A": 68.68,
        "BBB": 127.53,
        "BB": 280.28,
        "B": 481.04,
        "CCC/C": 1103.70,
    }
    cum7 = {"AAA": 0.51, "AA": 0.49, "A": 0.76, "BBB": 2.27, "BB": 8.89, "B": 20.99, "CCC/C": 50.75}
    table175 = {
        "AAA": (0.073, 0.596),
        "AA": (0.070, 0.728),
        "A": (0.109, 1.145),
        "BBB": (0.328, 2.126),
        "BB": (1.330, 4.671),
        "B": (3.366, 8.017),
        "CCC/C": (10.118, 18.395),
    }
    rows_ok = all(
        round(-np.log(1 - cum7[k] / 100) / 7 * 100, 3) == table175[k][0]
        and round(spread7[k] / 1e4 / 0.6 * 100, 3) == table175[k][1]
        for k in table175
    )
    report.ok(
        "Table 17.5 rebuilt from Table 17.4: physical seven-year hazards (A 0.109%, BBB 0.328%) are"
        " a"
        " tenth of risk-neutral ones (A 1.145%, BBB 2.126%) at 40% recovery",
        bool(rows_ok),
    )
    report.ok(
        "Hull Table 17.2 recovery as % of face: first lien 54.6 > second lien 44.3 > senior"
        " unsecured"
        " 38.0 > junior subordinated 22.3 (subordinated 32.1 above senior subordinated 31.0)",
        54.6 > 44.3 > 38.0 > 22.3 and 32.1 > 31.0,
    )


def check_corporate(report: CheckReport) -> None:
    """Part 2: corporate credit analysis: Altman Z, leverage and coverage, recovery by priority.

    Args:
        report: The run's report.
    """
    print(
        "== part 2: corporate credit analysis - Altman Z, leverage and coverage, recovery by"
        " priority"
    )
    wc, ta, ebit, sales, mve, tl, re_ = 170e3, 670e3, 60e3, 2200e3, 380e3, 240e3, 300e3
    x = [wc / ta, re_ / ta, ebit / ta, mve / tl, sales / ta]
    z = 1.2 * x[0] + 1.4 * x[1] + 3.3 * x[2] + 0.6 * x[3] + 0.999 * x[4]
    report.ok(
        "Hull Example 17.1: X = 0.254, 0.448, 0.0896, 1.583, 3.284 and Z = 5.46 (above 3.0:"
        " unlikely"
        " to default)",
        [round(v, 3) for v in x[:2]] == [0.254, 0.448]
        and round(x[2], 4) == 0.0896
        and [round(v, 3) for v in x[3:]] == [1.583, 3.284]
        and round(z, 2) == 5.46,
    )
    # Kestrel Logistics (EUR millions)
    k = dict(ebitda=120.0, capex=40.0, interest=42.0, taxes=10.0, cash=20.0)
    debt = {
        "revolver (1st lien)": 150.0,
        "term loan (1st lien)": 250.0,
        "senior notes": 200.0,
        "sub notes": 100.0,
    }
    total_debt = sum(debt.values())
    report.ok(
        "Kestrel: debt 700 is 5.83x EBITDA (5.67x net), EBITDA/interest 2.86x, (EBITDA -"
        " capex)/interest"
        " 1.90x, FFO/debt 9.7%",
        round(total_debt / k["ebitda"], 2) == 5.83
        and round((total_debt - k["cash"]) / k["ebitda"], 2) == 5.67
        and round(k["ebitda"] / k["interest"], 2) == 2.86
        and round((k["ebitda"] - k["capex"]) / k["interest"], 2) == 1.90
        and round((k["ebitda"] - k["interest"] - k["taxes"]) / total_debt, 3) == 0.097,
    )
    classes = [("first lien", 400.0), ("senior notes", 200.0), ("sub notes", 100.0)]
    low = absolute_priority_recovery(5.0 * 80.0 - 20.0, classes)
    high = absolute_priority_recovery(6.0 * 80.0 - 20.0, classes)
    report.ok(
        "recovery by absolute priority: at 5x distressed EBITDA of 80 less 20 of administrative"
        " claims,"
        " first lien 95%, unsecured 0%; at 6x, first lien 100%, senior notes 30%, sub notes 0%",
        [round(v, 2) for v in low.values()] == [0.95, 0.0, 0.0]
        and [round(v, 2) for v in high.values()] == [1.0, 0.30, 0.0],
    )


def check_risky_bond(report: CheckReport) -> None:
    """Part 3: valuing a risky bond: expected loss, CVA and the credit spread.

    Args:
        report: The run's report.
    """
    print("== part 3: valuing a risky bond - expected loss, CVA and the credit spread")
    r = 0.05
    t_cf = np.arange(0.5, 5.01, 0.5)
    cf = np.full(len(t_cf), 3.0)
    cf[-1] += 100.0
    v_rf = (cf * np.exp(-r * t_cf)).sum()
    v_risky = (cf * np.exp(-0.07 * t_cf)).sum()
    t_def = np.arange(0.5, 4.51, 1.0)
    fwd_value = np.array(
        [(cf[t_cf >= td] * np.exp(-r * (t_cf[t_cf >= td] - td))).sum() for td in t_def]
    )
    pv_loss_perQ = ((fwd_value - 40.0) * np.exp(-r * t_def)).sum()
    Q_h = (v_rf - v_risky) / pv_loss_perQ
    report.ok(
        "Hull Table 17.3: risky bond 95.34, risk-free 104.09, expected loss 8.75; forward value at"
        " 3.5"
        " years 104.34; total 288.48Q, so Q = 3.03% a year",
        round(v_risky, 2) == 95.34
        and round(v_rf, 2) == 104.09
        and round(fwd_value[3], 2) == 104.34
        and round(pv_loss_perQ, 2) == 288.48
        and round(Q_h, 4) == 0.0303,
    )
    surv = np.array([1 - Q_h * (t_def <= t).sum() for t in t_cf])
    price_direct = (cf * surv * np.exp(-r * t_cf)).sum() + (Q_h * 40.0 * np.exp(-r * t_def)).sum()
    report.ok(
        "independent route: survival-weighted cash flows plus discounted recoveries give the same"
        " 95.34",
        close(price_direct, v_risky, 1e-9),
    )
    arden = ARDEN.value()
    vnd, expo, pod, lgd = (
        arden.default_free_value,
        arden.exposure,
        arden.default_probability,
        arden.loss_given_default,
    )
    cva = arden.credit_value_adjustment
    price_a = vnd - cva
    ytm = brentq(
        lambda y: (np.array([5, 5, 105.0]) * (1 + y) ** -np.arange(1, 4)).sum() - price_a, 0.0, 0.2
    )
    report.ok(
        "Arden bond (3 years, 5% annual, risk-free 3%, hazard 1.5%, recovery 40%): value without"
        " default 105.66; exposures 108.83, 106.94, 105.00; default probabilities 1.50%, 1.48%,"
        " 1.46%;"
        " CVA 2.80, fair value 102.86, yield 3.97%, credit spread 97 bp",
        round(float(vnd), 2) == 105.66
        and [round(v, 2) for v in expo] == [108.83, 106.94, 105.0]
        and [round(p, 4) for p in pod] == [0.015, 0.0148, 0.0146]
        and round(cva, 2) == 2.80
        and round(float(price_a), 2) == 102.86
        and round(ytm, 4) == 0.0397
        and round((ytm - 0.03) * 1e4) == 97,
    )
    s_flat = 1 - np.array([0.985, 0.985**2, 0.985**3])
    pv_direct = (np.array([5, 5, 105.0]) * (1 - s_flat) * 1.03 ** -np.arange(1, 4)).sum() + (
        pod * 40.0 * 1.03 ** -np.arange(1, 4)
    ).sum()
    report.ok(
        "Arden by survival-weighted cash flows: the same 102.86",
        close(float(pv_direct), float(price_a), 1e-9),
    )
    df_a = 1.03 ** -np.arange(1, 4)
    report.ok(
        "Arden table: LGD 68.83, 66.94, 65.00; PD 1.500%, 1.478%, 1.455%; discount factors 0.9709,"
        " 0.9426, 0.9151; expected-loss PVs 1.00, 0.93, 0.87",
        [round(v, 2) for v in lgd] == [68.83, 66.94, 65.0]
        and [round(v * 100, 3) for v in pod] == [1.5, 1.478, 1.455]
        and [round(v, 4) for v in df_a] == [0.9709, 0.9426, 0.9151]
        and [round(v, 2) for v in lgd * pod * df_a] == [1.0, 0.93, 0.87],
    )
    cva_r30 = ARDEN.model_copy(update={"recovery": 0.30}).value().credit_value_adjustment
    cva_h3 = ARDEN.model_copy(update={"hazard": 0.03}).value().credit_value_adjustment
    report.ok(
        "sensitivity: recovery 30% raises CVA to 3.22; hazard 3% raises it to 5.52",
        round(cva_r30, 2) == 3.22 and round(cva_h3, 2) == 5.52,
    )
    cva_phys = ARDEN.model_copy(update={"hazard": 0.0016}).value().credit_value_adjustment
    report.ok(
        "using a physical default rate (0.16%, Table 17.1 BBB year 1) instead gives CVA of only"
        " 0.30:"
        " valuation needs the risk-neutral rate",
        round(cva_phys, 2) == 0.30,
    )


def check_migration(report: CheckReport) -> None:
    """Part 4: rating migration: Hull Tables 19.1-19.2 and the expected return of a BBB bond.

    Args:
        report: The run's report.
    """
    print(
        "== part 4: rating migration - Hull Tables 19.1-19.2 and the expected return of a BBB bond"
    )
    M = (
        np.array(
            [
                [89.85, 9.35, 0.55, 0.05, 0.11, 0.03, 0.05, 0.00],
                [0.50, 90.76, 8.08, 0.49, 0.05, 0.06, 0.02, 0.02],
                [0.03, 1.67, 92.61, 5.23, 0.27, 0.12, 0.02, 0.05],
                [0.00, 0.10, 3.45, 91.93, 3.78, 0.46, 0.11, 0.17],
                [0.01, 0.03, 0.12, 5.03, 86.00, 7.51, 0.61, 0.70],
                [0.00, 0.02, 0.08, 0.17, 5.18, 85.09, 5.66, 3.81],
                [0.00, 0.00, 0.12, 0.20, 0.65, 14.72, 50.90, 33.42],
                [0, 0, 0, 0, 0, 0, 0, 100.0],
            ]
        )
        / 100
    )
    report.ok(
        "Table 19.1 rows sum to 100% within rounding",
        bool(np.allclose(M.sum(axis=1), 1.0, atol=0.0003)),
        f"{np.round(M.sum(axis=1) * 100, 2)}",
    )
    M5 = np.linalg.matrix_power(M, 5)
    t192_bbb = [0.02, 0.80, 12.77, 68.51, 12.35, 3.53, 0.50, 1.53]
    report.ok(
        "Table 19.2 BBB row reproduced as the fifth power of Table 19.1: stays BBB 68.51%, defaults"
        " 1.53%",
        bool(np.allclose(M5[3] * 100, t192_bbb, atol=0.02)),
        f"{np.round(M5[3] * 100, 2)}",
    )
    spreads = np.array([60, 80, 110, 160, 300, 500, 1000]) / 1e4  # assumed spreads by rating
    dur = 7.0
    moves = M[3, :7] * (-dur * (spreads - spreads[3]))
    exp_ret = spreads[3] + moves.sum() + M[3, 7] * (-(1 - 0.40))
    report.ok(
        "BBB bond, modified duration 7, assumed spreads 60-1,000 bp: carry 1.60%, migration -0.42%,"
        " default -0.10%: expected excess return 1.08%, against 1.60% if the rating never moved",
        round(moves.sum(), 4) == -0.0042
        and round(M[3, 7] * -0.6, 4) == -0.001
        and round(exp_ret, 4) == 0.0108,
        f"migration {moves.sum():.5f}",
    )
    report.ok(
        "the downgrade to BB alone costs 0.37%",
        round(M[3, 4] * dur * (spreads[4] - spreads[3]), 4) == 0.0037,
    )


def check_structural(report: CheckReport) -> float:
    """Part 5: structural against reduced-form models: Merton's model and its spread.

    Args:
        report: The run's report.

    Returns:
        The Merton credit spread of Example 17.4, which part 8 compares a CDS against.
    """
    print("== part 5: structural against reduced-form models")
    E0, sE, rr, T, Dd = 3.0, 0.80, 0.05, 1.0, 10.0

    def merton_eq(p: Floats) -> list[float]:
        V, sV = p
        d1 = (np.log(V / Dd) + (rr + sV**2 / 2) * T) / (sV * np.sqrt(T))
        d2 = d1 - sV * np.sqrt(T)
        return [
            V * norm.cdf(d1) - Dd * np.exp(-rr * T) * norm.cdf(d2) - E0,
            norm.cdf(d1) * sV * V - sE * E0,
        ]

    V0, sV = fsolve(merton_eq, [13.0, 0.2])
    d1 = (np.log(V0 / Dd) + (rr + sV**2 / 2) * T) / (sV * np.sqrt(T))
    d2 = d1 - sV * np.sqrt(T)
    debt_val = V0 - E0
    report.ok(
        "Hull Example 17.4: V0 12.40, asset volatility 0.2123, d2 1.1408, default probability"
        " 12.7%,"
        " debt 9.40 against 9.51 promised: expected loss about 1.2%",
        round(V0, 2) == 12.40
        and round(sV, 4) == 0.2123
        and round(d2, 3) == 1.141
        and round(norm.cdf(-d2), 3) == 0.127
        and round(debt_val, 2) == 9.40
        and round((Dd * np.exp(-rr) - debt_val) / (Dd * np.exp(-rr)), 3) == 0.012,
    )
    L = Dd * np.exp(-rr * T) / V0
    spread_closed = -np.log(norm.cdf(d2) + norm.cdf(-d1) / L) / T
    spread_direct = -np.log(debt_val / Dd) / T - rr
    report.ok(
        "Merton credit spread 1.24% from the debt value equals Hull's closed form (Problem 17.17)",
        close(spread_closed, spread_direct, 1e-6) and round(spread_direct, 4) == 0.0124,
    )
    lam_rf = spread_direct / (1 - 0.40)
    rec_frac = V0 * np.exp(rr * T) * norm.cdf(-d1) / norm.cdf(-d2) / Dd
    report.ok(
        "the reduced-form hazard that matches the same spread at 40% recovery is 2.06% a year, far"
        " below Merton's 12.7% one-year risk-neutral default probability, because Merton's recovery"
        " is"
        " endogenous: the debt holders take assets expected to be worth about 90% of the face value"
        " when V < D",
        round(lam_rf, 4) == 0.0206 and round(rec_frac, 2) == 0.90,
    )
    # Distance to default and asset drift
    report.ok(
        "distance to default is d2 = 1.14 standard deviations",
        round(d2, 2) == 1.14,
    )
    return float(spread_direct)


def check_term_structure(report: CheckReport) -> None:
    """Part 6: the term structure of credit spreads and average and forward hazards.

    Args:
        report: The run's report.
    """
    print("== part 6: the term structure of credit spreads")
    s3, s5, s10, R60 = 0.0050, 0.0060, 0.0100, 0.60
    h3, h5, h10 = s3 / (1 - R60), s5 / (1 - R60), s10 / (1 - R60)
    report.ok(
        "Hull Example 17.3: average hazards 1.25%, 1.5%, 2.5%; forward hazards 1.875% (years 3-5)"
        " and"
        " 3.5% (years 5-10)",
        [round(h, 4) for h in (h3, h5, h10)] == [0.0125, 0.015, 0.025]
        and round((5 * h5 - 3 * h3) / 2, 5) == 0.01875
        and round((10 * h10 - 5 * h5) / 5, 4) == 0.035,
    )
    par_spread: dict[str, list[float]] = {}
    for name, hz in {
        "flat 2%": lambda t: 0.02,
        "rising 1%->3%": lambda t: 0.01 + 0.004 * t,
        "falling 6%->2%": lambda t: 0.06 - 0.008 * t,
    }.items():
        par_spread[name] = []
        for T in (1, 3, 5):
            prem_acc, prot = CDS.model_copy(update={"maturity": T}).legs(hz)
            par_spread[name].append(10000 * (prot / prem_acc))
    report.ok(
        "a rising hazard (an investment-grade name) gives an upward credit curve, a falling one (a"
        " distressed name) an inverted curve; a flat hazard a flat curve at 123 bp, near lambda (1"
        " - R)"
        " = 120 bp",
        par_spread["rising 1%->3%"][0] < par_spread["rising 1%->3%"][2]
        and par_spread["falling 6%->2%"][0] > par_spread["falling 6%->2%"][2]
        and all(round(s) == 123 for s in par_spread["flat 2%"]),
        "; ".join(f"{k}: " + ", ".join(f"{v:.0f}" for v in vals) for k, vals in par_spread.items()),
    )


def check_cds(report: CheckReport) -> None:
    """Part 7: pricing a CDS: Hull Appendix K, OFOD pp. 593-596 and the index trade.

    Args:
        report: The run's report.
    """
    print("== part 7: pricing a CDS - Hull Appendix K and OFOD pp. 593-596")
    dur_k, prot_k = CDS.legs(lambda t: 0.02)
    S_k = np.exp(-0.02 * np.arange(1, 6))
    report.ok(
        "Appendix K: survival 0.9802, 0.9608, 0.9418, 0.9231, 0.9048 (Table K.1 misprints year 4 as"
        " 0.9321; Table K.2 has 0.9231); payments 4.0728s + accrual 0.0422s = 4.1150s; payoff"
        " 0.0506;"
        " spread 123 bp",
        [round(v, 4) for v in S_k] == [0.9802, 0.9608, 0.9418, 0.9231, 0.9048]
        and round((S_k * np.exp(-0.05 * np.arange(1, 6))).sum(), 4) == 4.0728
        and round(dur_k, 4) == 4.1150
        and round(prot_k, 4) == 0.0506
        and round(prot_k / dur_k * 1e4) == 123,
    )
    report.ok(
        "the rule of thumb lambda (1 - R) = 0.02 x 0.6 = 120 bp is close to the exact 123 bp",
        close(0.02 * 0.6, 0.012) and abs(prot_k / dur_k - 0.012) < 0.0005,
    )
    report.ok(
        "marking to market a CDS struck at 150 bp: 4.1150 x 0.015 - 0.0506 = 0.0111 to the seller,"
        " -0.0111 to the buyer",
        round(dur_k * 0.015 - prot_k, 4) == 0.0111,
    )
    binary = (
        (np.concatenate([[1.0], S_k[:-1]]) - S_k) * np.exp(-0.05 * (np.arange(1, 6) - 0.5))
    ).sum()
    report.ok(
        "binary CDS paying 1: PV of payoff 0.0844, spread 205 bp",
        round(binary, 4) == 0.0844 and round(binary / dur_k * 1e4) == 205,
    )

    def implied_gap(h: float) -> float:
        prem_acc, prot = CDS.legs(lambda t: h)
        return prot / prem_acc - 0.01

    lam_imp = brentq(implied_gap, 1e-5, 0.2)
    report.ok(
        "a 100 bp spread implies a hazard of 1.63% (OFOD p. 594)",
        round(lam_imp, 4) == 0.0163,
    )
    # Recovery insensitivity: imply the hazard from 123 bp at R = 30% and revalue the 150 bp
    # contract.

    def implied_gap30(h: float) -> float:
        prem_acc, prot = CDS.model_copy(update={"recovery": 0.30}).legs(lambda t: h)
        return prot / prem_acc - prot_k / dur_k

    lam30 = brentq(implied_gap30, 1e-5, 0.2)
    d30, p30 = CDS.model_copy(update={"recovery": 0.30}).legs(lambda t: lam30)
    report.ok(
        "with the hazard implied consistently, assuming 30% recovery instead of 40% changes the 150"
        " bp"
        " contract's value from 0.0111 to 0.0112 (hazard 1.71% against 2%): the vanilla CDS value"
        " is"
        " insensitive to recovery",
        round(lam30, 4) == 0.0171 and round(d30 * 0.015 - p30, 4) == 0.0112,
    )

    def index_gap(h: float) -> float:
        prem_acc, prot = CDS.model_copy(update={"rate": 0.04, "frequency": 4}).legs(lambda t: h)
        return prot / prem_acc - 0.00345

    lam_ix = brentq(index_gap, 1e-6, 0.1)
    d_ix, _ = CDS.model_copy(update={"rate": 0.04, "frequency": 4}).legs(lambda t: lam_ix)
    price_ix = 100 - 100 * d_ix * (0.00345 - 0.00406)
    report.ok(
        "OFOD Example 25.1: index quote 0.345% against coupon 0.406%, quarterly, 4% rates, 40%"
        " recovery: hazard 0.572% (Hull 0.5717%), duration 4.447, price 100.27; the seller pays"
        " 0.27 per"
        " 100 up front",
        abs(lam_ix - 0.005717) < 0.00001
        and round(d_ix, 3) == 4.447
        and round(price_ix, 2) == 100.27,
        f"hazard {lam_ix:.6f}",
    )


def check_cds_strategies(report: CheckReport, spread_direct: float) -> None:
    """Part 8: CDS strategies: hedging, the basis, index trades and a Credit01-neutral curve trade.

    Args:
        report: The run's report.
        spread_direct: The Merton credit spread of Example 17.4, from part 5.
    """
    print(
        "== part 8: CDS strategies - hedging, the basis, index trades and a Credit01-neutral curve"
        " trade"
    )
    report.ok(
        "Hull: a 7% five-year bond hedged with 200 bp of protection earns about 5%, the risk-free"
        " rate",
        close(0.07 - 0.02, 0.05),
    )
    bond_spread, cds_spread = 0.0240, 0.0200
    report.ok(
        "negative basis of -40 bp (CDS 200 against a bond spread of 240): buying the bond and"
        " protection locks in about 40 bp a year before funding, if the bond can be financed at the"
        " risk-free rate",
        round((cds_spread - bond_spread) * 1e4) == -40,
    )
    report.ok(
        "CDX index (RMFI p. 377): 125 names x 800,000 at 166 bp cost 1,660,000 a year; after a"
        " default"
        " the payment falls by 13,280",
        round(0.0166 * 800_000 * 125) == 1_660_000 and round(1_660_000 / 125) == 13_280,
    )
    # Larkspur: flat hazard 2%, R 40%, r 5%, annual payments.
    d5, _ = CDS.model_copy(update={"maturity": 5.0}).legs(lambda t: 0.02)
    d10, _ = CDS.model_copy(update={"maturity": 10.0}).legs(lambda t: 0.02)
    n10 = 10.0
    n5 = n10 * d10 / d5
    report.ok(
        "Credit01-neutral steepener on Larkspur: buy 10m of 10-year protection (risky duration"
        " 7.01)"
        " and sell 17.05m of 5-year (4.11)",
        round(d10, 2) == 7.01 and round(d5, 2) == 4.11 and round(n5, 2) == 17.05,
    )

    def mtm_change(d_s5: float, d_s10: float) -> float:
        # P&L for the protection buyer ~ notional x risky duration x spread change (first order)
        return n10 * d10 * d_s10 - n5 * d5 * d_s5

    report.ok(
        "first order: a parallel 50 bp widening nets zero; 10-year +50 bp with 5-year unchanged"
        " gains"
        " 0.351m; 5-year +50 bp with 10-year unchanged loses 0.351m",
        close(mtm_change(0.005, 0.005), 0.0, 1e-9)
        and round(mtm_change(0.0, 0.005), 3) == 0.351
        and round(mtm_change(0.005, 0.0), 3) == -0.351,
    )
    jtd = (n10 - n5) * (1 - 0.40)
    report.ok(
        "jump to default: the trade is net short 7.05m of protection, so an immediate default loses"
        " 4.23m at 40% recovery - the cost of being Credit01-neutral",
        round(jtd, 2) == -4.23,
    )
    report.ok(
        "the bearish variant (Berd, Mashal and Wang p. 13): equal notionals of 10m net long 29.0k"
        " of"
        " risky duration per unit spread, gaining 0.145m on a parallel 50 bp widening, with no"
        " jump-to-default exposure",
        round(n10 * (d10 - d5), 1) == 29.0
        and round(n10 * (d10 - d5) * 0.005, 3) == 0.145
        and close((n10 - n10) * 0.6, 0.0),
    )
    cds_mkt = 0.0200
    report.ok(
        "capital-structure view: the equity-implied (Merton) spread for Hull's Example 17.4 firm is"
        " 124"
        " bp; a market CDS at 200 bp is 76 bp rich relative to the equity",
        round((cds_mkt - spread_direct) * 1e4) == 76,
    )


def check_sovereign(report: CheckReport) -> None:
    """Part 9: sovereign debt dynamics: Fabozzi's Handbook eqs. 17-1 to 17-3 for Veloria.

    Args:
        report: The run's report.
    """
    print("== part 9: sovereign debt dynamics - Fabozzi Handbook eqs. 17-1 to 17-3 (Veloria)")
    D0, pb, g, pi, i_eff, alpha, e, i_f = 0.70, -0.01, 0.02, 0.04, 0.065, 0.40, 0.10, 0.05
    dD_formula = (
        -pb + (i_eff - pi * (1 + g) - g + alpha * e * (1 + i_f)) / (1 + g + pi + g * pi) * D0
    )
    # Nominal route: domestic debt grows at i_d, foreign at (1 + i_f)(1 + e); i_eff =
    # (1 - alpha) i_d + alpha i_f.
    i_d = (i_eff - alpha * i_f) / (1 - alpha)
    gdp0 = 100.0
    gdp1 = gdp0 * (1 + g) * (1 + pi)
    debt1 = D0 * gdp0 * ((1 - alpha) * (1 + i_d) + alpha * (1 + i_f) * (1 + e)) - pb * gdp1
    report.ok(
        "debt ratio 70%, primary deficit 1%, real growth 2%, inflation 4%, effective rate 6.5% (40%"
        " in"
        " foreign currency at 5%), 10% depreciation: the ratio rises 4.05 points by eq. 17-1 and by"
        " a"
        " nominal roll-forward",
        close(debt1 / gdp1 - D0, dD_formula, 1e-12) and round(dD_formula, 4) == 0.0405,
    )
    pb_star = (i_eff - pi * (1 + g) - g + alpha * e * (1 + i_f)) / (1 + g + pi + g * pi) * D0
    pb_star_nofx = (i_eff - pi * (1 + g) - g) / (1 + g + pi + g * pi) * D0
    report.ok(
        "debt-stabilising primary balance (eq. 17-2): a surplus of 3.05% of GDP with the"
        " depreciation,"
        " 0.28% without it - the currency, not the budget, drives this year",
        round(pb_star, 4) == 0.0305 and round(pb_star_nofx, 4) == 0.0028,
    )
    gfn = 0.01 + 0.065 * 0.70 + 0.08
    report.ok(
        "gross financing needs (eq. 17-3): primary deficit 1% + interest 4.55% + amortisation 8% ="
        " 13.55% of GDP",
        round(gfn, 4) == 0.1355,
    )


def check_securitisation(report: CheckReport) -> None:
    """Part 10: securitisation: pass-through, sequential pay, PAC, credit cards and tranches.

    Args:
        report: The run's report.
    """
    print(
        "== part 10: securitisation - Fabozzi and Kothari (2008) Tables 3.1-3.3 and the sizing on"
        " p. 96"
    )
    p165 = POOL.cash_flows(1.65)
    row1 = [round(v) for v in p165[0, 1:]]
    report.ok(
        "Table 3.1, month 1 at 165% PSA: SMM 0.00083, payment 3,964,947, net interest 3,025,000,"
        " scheduled principal 664,947, prepayment 546,435, total principal 1,211,383; month-2"
        " balance"
        " 658,788,617",
        round(p165[0, 2], 5) == 0.00083
        and row1[2:] == [3964947, 3025000, 664947, 546435, 1211383]
        and round(p165[1, 1]) == 658_788_617,
    )
    al = {
        psa: (POOL.cash_flows(psa)[:, 0] * POOL.cash_flows(psa)[:, 7]).sum() / 12 / 660e6
        for psa in (1.0, 1.65, 5.0)
    }
    report.ok(
        "average life 8.54 years at 165% PSA (the book prints 8.6), 11.2 at 100% PSA ('a little"
        " more"
        " than 11') and 3.7 at 500% PSA",
        round(al[1.65], 2) == 8.54 and round(al[1.0], 1) == 11.2 and round(al[5.0], 1) == 3.7,
    )
    po = sequential_payoff_months(p165, [320.925e6, 59.4e6, 159.225e6, 120.45e6])
    report.ok(
        "Structure 1 (sequential A 320.925m, B 59.4m, C 159.225m, D 120.45m): A is retired in month"
        " 78"
        " and B in month 97, as Table 3.2 shows (the text says 98)",
        po[:2] == [78, 97],
        f"payoff months {po}",
    )
    p100, p250 = POOL.cash_flows(1.0), POOL.cash_flows(2.5)
    pac = np.minimum(p100[:, 7], p250[:, 7])
    report.ok(
        "Table 3.3: month 1 principal 995,525 at 100% PSA and 1,494,837 at 250%; month 101"
        " 2,577,230 and"
        " 2,709,199; the PAC schedule (the lower of the two) sums to 470,224,580, leaving"
        " 189,775,420 of"
        " support bonds",
        [round(p100[0, 7]), round(p250[0, 7]), round(p100[100, 7]), round(p250[100, 7])]
        == [995525, 1494837, 2577230, 2709199]
        and abs(pac.sum() - 470_224_580) < 1.0
        and abs(660e6 - pac.sum() - 189_775_420) < 1.0,
    )
    mult = {"AAA": 5, "AA": 4, "A": 3, "BBB": 2, "BB": 1.75}
    support = {kk: 0.0168 * v for kk, v in mult.items()}
    sizes = [1 - support["AAA"]] + [
        support[a] - support[b] for a, b in zip(list(mult)[:-1], list(mult)[1:])
    ]
    report.ok(
        "sizing (p. 96): base-case loss 1.68% times multiples 5, 4, 3, 2, 1.75 gives support 8.40%,"
        " 6.72%, 5.04%, 3.36%, 2.94%; classes of 91.60% AAA, 1.68% each AA to BBB, 0.42% BB and"
        " 2.94%"
        " unrated",
        [round(v * 100, 2) for v in support.values()] == [8.40, 6.72, 5.04, 3.36, 2.94]
        and [round(v * 100, 2) for v in sizes] == [91.60, 1.68, 1.68, 1.68, 0.42]
        and close(sum(sizes) + support["BB"], 1.0, 1e-12),
    )
    card = dict(portfolio_yield=0.18, charge_offs=0.05, servicing=0.02, coupon=0.05)
    xs_card = card["portfolio_yield"] - card["charge_offs"] - (card["servicing"] + card["coupon"])
    report.ok(
        "credit card ABS (pp. 159-161): portfolio yield 18% less charge-offs 5% less the base rate"
        " (servicing 2% + coupon 5%) leaves excess spread of 6%; charge-offs would have to reach"
        " 11% for"
        " the three-month average to hit the zero trigger and start early amortisation",
        close(xs_card, 0.06, 1e-12)
        and close(card["portfolio_yield"] - card["servicing"] - card["coupon"], 0.11, 1e-12),
    )
    report.ok(
        "excess spread (p. 87): asset yield 9.5% less servicing 1.5% less bond coupon 5% = 3%",
        close(0.095 - 0.015 - 0.05, 0.03, 1e-12),
    )
    rows81 = []
    for L in (0.10, 0.13, 0.17, 0.20):
        m = tranche_loss(L, 0.05, 0.20)
        rows81.append(
            [
                round(100 * v, 1)
                for v in (
                    m,
                    tranche_loss(m, 0, 0.10),
                    tranche_loss(m, 0.10, 0.35),
                    tranche_loss(m, 0.35, 1.0),
                )
            ]
        )
    report.ok(
        "Hull OFOD Table 8.1: ABS 80/15/5 and ABS CDO 65/25/10; at 10, 13, 17, 20% asset losses the"
        " ABS"
        " mezzanine loses 33.3, 53.3, 80, 100% and the CDO senior 0, 28.2, 69.2, 100%; the CDO"
        " senior is"
        " hit beyond 10.25%",
        rows81
        == [
            [33.3, 100.0, 93.3, 0.0],
            [53.3, 100.0, 100.0, 28.2],
            [80.0, 100.0, 100.0, 69.2],
            [100.0, 100.0, 100.0, 100.0],
        ]
        and close(tranche_loss(tranche_loss(0.1025, 0.05, 0.20), 0.35, 1.0), 0.0)
        and close(0.80 + 0.65 * 0.15, 0.8975),
    )


def main() -> int:
    """Print the versions, then run the ten parts with one report.

    Worked numbers of the entries for the credit-risk, CDS, sovereign and securitisation objectives.
    Reproduces Hull, Risk Management and Financial Institutions, 6th ed. (2023): Example 17.1
    (Altman Z), Example 17.2 (hazard rates), Tables 17.1 and 17.4-17.5, Example 17.3 (hazard term
    structure), Table 17.3 (risky bond, Q = 3.03%), Example 17.4 (Merton), Tables 19.1-19.2 (rating
    transitions) and Appendix K (CDS valuation); Hull, Options, Futures, and Other Derivatives, 11th
    Global ed. (2021), pp. 593-596 (implied hazard, binary CDS, index trades, Example 25.1); Fabozzi
    (ed.), Handbook of Fixed Income Securities, 9th ed. (2021), eqs. 17-1 to 17-3; Fabozzi and
    Kothari, Introduction to Securitization (2008), Tables 3.1-3.3, Structure 1, Structure 2 and the
    sizing of credit enhancement on p. 96; Hull (2021) Table 8.1 (ABS CDO). Kestrel Logistics, the
    Arden bond, the Larkspur CDS curve and Veloria are hypothetical.

    Independent routes: survival probabilities from hazard rates against cumulative default tables;
    the risky bond price as the default-free value less expected loss against survival-weighted cash
    flows plus recovery; the Merton equations solved numerically against Hull's closed-form spread
    (Problem 17.17); CDS spreads from the premium and protection legs against the rule of thumb s =
    lambda (1 - R); the sovereign debt ratio from Fabozzi's formula against a nominal debt and GDP
    roll-forward; the pass-through and PAC from a month-by-month amortisation against the printed
    tables.

    Count convention: one check is one executed ok() call (a call inside a loop counts once per
    iteration).

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    report = CheckReport()
    check_components(report)
    check_corporate(report)
    check_risky_bond(report)
    check_migration(report)
    spread_direct = check_structural(report)
    check_term_structure(report)
    check_cds(report)
    check_cds_strategies(report, spread_direct)
    check_sovereign(report)
    check_securitisation(report)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
