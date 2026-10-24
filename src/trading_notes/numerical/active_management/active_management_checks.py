"""Worked examples of active return, the information ratio, the fundamental law and active risk."""

import math
import sys

import numpy as np
import scipy
from scipy.optimize import minimize_scalar

from trading_notes.numerical.active_management.fundamental_law import FundamentalLaw
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close


def check_ex_post(report: CheckReport) -> None:
    """Check ex post active return, tracking error, information ratio and Sharpe ratios."""
    print("== part 1: ex post active return, tracking error, information ratio and Sharpe ratios")
    B = np.array([2.0, -1.5, 2.7, 1.1, -2.4, 1.2, 3.5, -0.9, 1.3, -2.9, 2.4, 0.9])
    P = np.array([2.9, -2.1, 3.1, 0.9, -1.3, 0.4, 4.0, -0.6, 0.4, -2.2, 2.6, 1.1])
    rf = np.full(12, 0.30)
    a = P - B
    abar, sa = a.mean(), a.std(ddof=1)
    report.ok(
        "mean monthly active return 0.15%, sample sd 0.6516%",
        bool(abs(abar - 0.15) < 1e-12 and abs(sa - 0.651572) < 1e-6),
    )
    te_ann = sa * math.sqrt(12)
    ir_ann = 12 * abar / te_ann
    report.ok(
        "annualised active return 1.80%, tracking error 2.257%, ex post IR 0.797",
        bool(abs(te_ann - 2.257110) < 1e-6 and abs(ir_ann - 0.79748) < 1e-5),
    )
    R_P = np.prod(1 + P / 100) - 1
    R_B = np.prod(1 + B / 100) - 1
    report.ok(
        "compound returns 9.34% and 7.40%: geometric excess 1.80%, arithmetic difference 1.94%",
        bool(
            abs(R_P - 0.093426) < 1e-6
            and abs(R_B - 0.074044) < 1e-6
            and abs((1 + R_P) / (1 + R_B) - 1 - 0.018046) < 1e-6
        ),
    )
    t_stat = abar / (sa / math.sqrt(12))
    report.ok(
        "t-statistic of the mean active return = annual IR x sqrt(years) = 0.797 x 1, far from"
        " significant",
        bool(close(t_stat, ir_ann * math.sqrt(1)) and t_stat < 1.645),
    )
    ex_P, ex_B = P - rf, B - rf
    sr_P = 12 * ex_P.mean() / (ex_P.std(ddof=1) * math.sqrt(12))
    sr_B = 12 * ex_B.mean() / (ex_B.std(ddof=1) * math.sqrt(12))
    report.ok(
        "annualised Sharpe ratios 0.779 (portfolio) and 0.530 (benchmark)",
        bool(abs(sr_P - 0.77904) < 1e-5 and abs(sr_B - 0.53003) < 1e-5),
    )
    report.ok(
        "the IR and the Sharpe ratio answer different questions: here IR 0.797 > SR 0.779",
        bool(ir_ann > sr_P),
    )


def check_ex_ante(report: CheckReport) -> None:
    """Check Table 5.3, optimal active risk and the Sharpe ratio of benchmark plus active."""
    print(
        "== part 2: ex ante IR, optimal active risk and the Sharpe ratio of benchmark plus active"
    )
    table = {(ir, lam): ir / (2 * lam) for ir in (1.0, 0.75, 0.5) for lam in (0.05, 0.10, 0.15)}
    printed = {
        (1.0, 0.05): 10.00,
        (1.0, 0.10): 5.00,
        (1.0, 0.15): 3.33,
        (0.75, 0.05): 7.50,
        (0.75, 0.10): 3.75,
        (0.75, 0.15): 2.50,
        (0.5, 0.05): 5.00,
        (0.5, 0.10): 2.50,
        (0.5, 0.15): 1.67,
    }
    report.ok(
        "Grinold-Kahn Table 5.3 (omega* = IR / 2 lambda) reproduced to the printed 2 dp",
        all(abs(round(table[k], 2) - v) < 1e-9 for k, v in printed.items()),
    )
    report.ok(
        "value added IR^2/(4 lambda) = 1.40625% at IR 0.75, lambda 0.1 (their 1.40% curve)",
        close(0.75**2 / 0.4, 1.40625),
    )
    mu_B, s_B, IR = 6.0, 15.0, 0.5  # Sharpe (1994): excess return 6%, sd 15%, SR 0.40
    srb = mu_B / s_B

    def sr_total(om: float) -> float:
        return (mu_B + IR * om) / math.sqrt(s_B**2 + om**2)

    opt = minimize_scalar(
        lambda om: -sr_total(om), bounds=(0, 60), method="bounded", options={"xatol": 1e-10}
    )
    report.ok(
        "optimal active risk = (IR/SR_B) sigma_B = 18.75% when active and benchmark returns are"
        " uncorrelated",
        bool(abs(opt.x - IR / srb * s_B) < 1e-5),
    )
    report.ok(
        "then SR_P = sqrt(SR_B^2 + IR^2) = 0.6403",
        abs(sr_total(opt.x) - math.sqrt(srb**2 + IR**2)) < 1e-12
        and abs(math.sqrt(srb**2 + IR**2) - 0.64031) < 1e-5,
    )
    report.ok(
        "a 4% tracking-error limit gives SR 0.5153; doubling active risk past the optimum (37.5%)"
        " lowers SR to 0.6128",
        abs(sr_total(4.0) - 0.51533) < 1e-5 and abs(sr_total(37.5) - 0.61279) < 1e-5,
    )


def check_fundamental_law(report: CheckReport) -> None:
    """Check the fundamental law's examples, the binary example and the transfer coefficient."""
    print("== part 3: fundamental law")
    report.ok(
        "market timer, 4 bets a year, needs IC 0.25 for IR 0.5; a 400-bet stock picker needs 0.025",
        close(FundamentalLaw(ic=0.25, breadth=4).information_ratio, 0.5)
        and close(FundamentalLaw(ic=0.025, breadth=400).information_ratio, 0.5),
    )
    report.ok(
        "2020 sequel: stock picker 0.05 x sqrt(2000) x 0.35 = 0.783; timer 0.1 x 2 x 0.6 = 0.12;"
        " TAA"
        " 0.1 x sqrt(12) x 0.5 = 0.173",
        abs(FundamentalLaw(ic=0.05, breadth=2000, transfer=0.35).information_ratio - 0.7826) < 1e-4
        and close(FundamentalLaw(ic=0.1, breadth=4, transfer=0.6).information_ratio, 0.12)
        and abs(FundamentalLaw(ic=0.1, breadth=12, transfer=0.5).information_ratio - 0.1732) < 1e-4,
    )
    report.ok(
        "additivity: 0.04^2 x 400 + 0.03^2 x 200 = 0.82, IR 0.906 (from 0.80)",
        close(0.04**2 * 400 + 0.03**2 * 200, 0.82) and abs(math.sqrt(0.82) - 0.9055) < 1e-4,
    )
    report.ok(
        "three independent managers 0.75, 0.50, 0.30 combine to 0.95",
        abs(math.sqrt(0.75**2 + 0.5**2 + 0.3**2) - 0.95) < 1e-12,
    )
    # Binary example: residual = sum of 300 +/-1% components; the manager knows one; 200 stocks,
    # two forecasts a year.
    ic = 1 / math.sqrt(300)
    # per half-year, in %^2 (variance remaining after knowing one component)
    act_var = 200 * (1 / 200) ** 2 * 299
    ir_half = 1.0 / math.sqrt(act_var)
    report.ok(
        "IC = 1/sqrt(300) = 0.0577; active sd 1.2227% and IR 0.8179 per half-year",
        abs(ic - 0.05774) < 1e-5
        and abs(math.sqrt(act_var) - 1.2227) < 1e-4
        and abs(ir_half - 0.8179) < 1e-4,
    )
    report.ok(
        "annual IR 1.157 exceeds the law's 1.155 (the law ignores the risk reduction from knowing)",
        abs(ir_half * math.sqrt(2) - 1.1567) < 1e-4
        and abs(FundamentalLaw(ic=ic, breadth=400).information_ratio - 1.1547) < 1e-4,
    )
    report.ok(
        "two sources with IC 0.0816 each and correlation 0.5 combine to IC 0.0942, not 0.1155",
        abs(0.0816 * math.sqrt(2 / 1.5) - 0.0942) < 1e-4
        and abs(0.0816 * math.sqrt(2) - 0.1154) < 1e-3,
    )
    report.ok(
        "expected active return TC x IC x sqrt(BR) x sigma_A = 0.783 x 4% = 3.13%",
        abs(FundamentalLaw(ic=0.05, breadth=2000, transfer=0.35).information_ratio * 4.0 - 3.130)
        < 1e-3,
    )
    # Repackaged information: 12 monthly rebalances of one annual industry view are one bet, not
    # twelve.
    report.ok(
        "one annual view rebalanced monthly: BR = 1, not 12 (IR 0.1 not 0.35 at IC 0.1)",
        close(FundamentalLaw(ic=0.1, breadth=1).information_ratio, 0.1)
        and abs(FundamentalLaw(ic=0.1, breadth=12).information_ratio - 0.3464) < 1e-4,
    )

    # Transfer coefficient: diagonal residual covariance, benchmark-neutral alphas, cash allowed.
    alpha = np.array([1.0, 0.5, -0.5, 1.0, -2.0])  # percent a year
    om = np.array([20.0, 25.0, 30.0, 20.0, 25.0])  # residual sd, percent
    V = np.diag(om**2)
    lam = 0.005
    hQ = alpha / (2 * lam * om**2)  # unconstrained optimum: alpha = 2 lambda V hQ
    hP = np.clip(hQ, -0.05, 0.10)  # policy limits on active positions: -5 to +10 points
    irQ = alpha @ hQ / math.sqrt(hQ @ V @ hQ)
    irP = alpha @ hP / math.sqrt(hP @ V @ hP)
    tc = hP @ V @ hQ / math.sqrt((hP @ V @ hP) * (hQ @ V @ hQ))
    report.ok(
        "unconstrained IR_Q = sqrt(sum (alpha/omega)^2) = 0.1099",
        bool(
            abs(irQ - math.sqrt(((alpha / om) ** 2).sum())) < 1e-12 and abs(irQ - 0.109899) < 1e-6
        ),
    )
    report.ok(
        "limits bind on stocks 1, 3, 4 and 5 (hQ = 25, 8, -5.6, 25, -32 points)",
        np.array_equal(hP != hQ, np.array([True, False, True, True, True])),
    )
    report.ok(
        "IR_P = TC x IR_Q exactly (TC 0.835, IR_P 0.0918)",
        bool(abs(irP - tc * irQ) < 1e-12 and abs(tc - 0.835217) < 1e-6),
    )


def check_risk_decomposition(report: CheckReport) -> None:
    """Check active risk split into factor and specific, and into beta and residual."""
    print("== part 4: active risk: factor against specific, beta against residual")
    Bx = np.array(
        [[1.1, 0.8, -0.2], [0.9, -0.3, 0.6], [1.3, 0.5, -0.8], [0.8, -0.6, 0.9], [1.0, 0.2, 0.1]]
    )
    fsd = np.array([16.0, 8.0, 6.0])
    fC = np.array([[1, 0.3, 0.1], [0.3, 1, 0.2], [0.1, 0.2, 1]])
    F = np.outer(fsd, fsd) * fC
    spec = np.array([30.0, 25.0, 35.0, 28.0, 32.0])
    Vfull = Bx @ F @ Bx.T + np.diag(spec**2)
    hB = np.full(5, 0.2)
    hA = np.array([0.08, -0.04, 0.05, -0.06, -0.03])
    report.ok("active weights sum to zero", close(hA.sum(), 0.0))
    x = Bx.T @ hA
    fac_var = x @ F @ x
    spec_var = (hA**2 * spec**2).sum()
    psi2 = hA @ Vfull @ hA
    report.ok("active variance = x'Fx + sum h^2 s^2", close(psi2, fac_var + spec_var))
    print(
        f"    active exposures {np.round(x, 4)}, factor var {fac_var:.4f}, specific var"
        f" {spec_var:.4f}, TE {math.sqrt(psi2):.4f}%"
    )
    report.ok(
        "tracking error 3.959%, only 13.5% of active variance from factors (a stock-specific book)",
        bool(abs(math.sqrt(psi2) - 3.959175) < 1e-6 and abs(fac_var / psi2 - 0.134517) < 1e-6),
    )
    mcar = Vfull @ hA / math.sqrt(psi2)
    report.ok(
        "contributions h_i x MCAR_i sum to the tracking error",
        close((hA * mcar).sum(), math.sqrt(psi2)),
    )
    fcontrib = x * (F @ x) / psi2
    report.ok(
        "factor shares of active variance sum to the factor fraction",
        close(fcontrib.sum(), fac_var / psi2),
    )
    sB2 = hB @ Vfull @ hB
    beta_A = hA @ Vfull @ hB / sB2
    resid_var = psi2 - beta_A**2 * sB2
    report.ok(
        "active beta 0.0448 contributes 0.927%^2 of 15.675%^2; residual variance 14.748%^2",
        bool(
            abs(beta_A - 0.044799) < 1e-6
            and abs(beta_A**2 * sB2 - 0.927490) < 1e-6
            and abs(resid_var - 14.747577) < 1e-6
        ),
    )
    report.ok(
        "psi^2 = beta_A^2 sigma_B^2 + omega^2 with omega^2 >= 0",
        bool(resid_var > 0 and close(beta_A**2 * sB2 + resid_var, psi2)),
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Part 1 is a declared synthetic sample of twelve monthly returns (percent) with a bill rate of
    0.30 percent a month. Part 2 reproduces Grinold and Kahn's Table 5.3 (chap. 5, p. 123); part 3
    their fundamental-law numbers (chap. 6, pp. 148-157; 2020 sequel, pp. 23-29), including the
    transfer-coefficient identity IR_P = IR_Q corr(P, Q) on an invented five-stock problem; part 4
    decomposes an invented active position. No random draws.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    check_ex_post(report)
    check_ex_ante(report)
    check_fundamental_law(report)
    check_risk_decomposition(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
