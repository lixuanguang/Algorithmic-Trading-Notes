"""The worked example of rule:counterparty-credit-cva-capital.

Library gap-filling Batch L3, package P10 (2026-10-21).

Deterministic, original inputs. Formulas from the Basel Framework as retrieved on 2026-10-21:
SA-CCR (CRE52.1, 52.10, 52.20, 52.23, 52.34, 52.39, 52.48-52.49 and 52.57; version effective 1
January 2023) and the reduced basic approach for CVA risk (MAR50.1 and 50.14-50.16; version
effective 1 January 2023). One unmargined netting set holding a four-year payer interest rate
swap on 100 notional, mark-to-market V = 2 to the bank; the counterparty is an investment-grade
industrial (MAR50.16, Table 1: RW = 3 percent). The swap's remaining maturity, 4 years, stands
in for the effective maturity M of CRE32.46-32.54 (illustration only). The default-risk risk
weight of 100 percent is illustrative, not taken from the credit-risk chapters.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.counterparty_capital
(scipy). Exits 1 on failure.
"""

import math
import sys
from collections.abc import Sequence
from typing import Final

import scipy
from scipy import integrate

from trading_notes.numerical.report import CheckReport

ALPHA: Final = 1.4
FLOOR: Final = 0.05
SF_IR: Final = 0.005
RHO: Final = 0.5
DS_BA_CVA: Final = 0.65
RW_C: Final = 0.03  # MAR50.16 risk weight of an investment-grade industrial


def supervisory_duration(s: float, e: float) -> float:
    """CRE52.34: SD = (exp(-0.05 S) - exp(-0.05 E)) / 0.05."""
    return (math.exp(-0.05 * s) - math.exp(-0.05 * e)) / 0.05


def maturity_factor_unmargined(m: float) -> float:
    """CRE52.48: MF = sqrt(min(M, 1) / 1), M floored at 10 business days (10/250 years)."""
    return math.sqrt(min(max(m, 10 / 250), 1.0))


def ir_hedging_set_effective_notional(d1: float, d2: float, d3: float) -> float:
    """CRE52.57, step 5 with offsets across the three maturity buckets."""
    return math.sqrt(d1**2 + d2**2 + d3**2 + 1.4 * d1 * d2 + 1.4 * d2 * d3 + 0.6 * d1 * d3)


def multiplier(v_minus_c: float, addon: float) -> float:
    """CRE52.23: min{1; floor + (1 - floor) exp((V - C) / (2 (1 - floor) AddOn))}."""
    return min(1.0, FLOOR + (1 - FLOOR) * math.exp(v_minus_c / (2 * (1 - FLOOR) * addon)))


def sa_ccr_ead(
    v: float, c: float, addon: float, alpha: float = ALPHA
) -> tuple[float, float, float]:
    """CRE52.1, 52.10 and 52.20: EAD = alpha (RC + PFE) for an unmargined netting set.

    Returns:
        (EAD, RC, PFE).
    """
    rc = max(v - c, 0.0)
    pfe = multiplier(v - c, addon) * addon
    return alpha * (rc + pfe), rc, pfe


def supervisory_df(m: float) -> float:
    """MAR50.15: DF = (1 - exp(-0.05 M)) / (0.05 M) for banks not using the IMM."""
    return (1 - math.exp(-0.05 * m)) / (0.05 * m)


def k_reduced(scva: Sequence[float]) -> float:
    """MAR50.14: K = sqrt((rho sum SCVA)^2 + (1 - rho^2) sum SCVA^2)."""
    return math.sqrt((RHO * sum(scva)) ** 2 + (1 - RHO**2) * sum(s * s for s in scva))


def check_identities(report: CheckReport) -> tuple[float, float]:
    """Check the formula identities; return the 4-year supervisory duration and DF."""
    print("== Formula identities")
    sd = supervisory_duration(0.0, 4.0)
    report.ok(
        "SD equals the integral of exp(-0.05 t) from S to E (a continuously discounted annuity at 5"
        " percent)",
        abs(sd - integrate.quad(lambda t: math.exp(-0.05 * t), 0.0, 4.0)[0]) < 1e-12,
        f"{sd:.6f}",
    )
    df = supervisory_df(4.0)
    report.ok(
        "DF equals the time average of exp(-0.05 t) over [0, M] (MAR50.15, footnote 3)",
        abs(df - integrate.quad(lambda t: math.exp(-0.05 * t), 0.0, 4.0)[0] / 4.0) < 1e-12,
        f"{df:.6f}",
    )
    report.ok(
        "the multiplier is 1 whenever V - C >= 0, tends to the 5 percent floor and never reaches"
        " it",
        multiplier(0.0, 1.0) == 1.0
        and multiplier(3.0, 1.0) == 1.0
        and FLOOR < multiplier(-50.0, 1.0) < FLOOR + 1e-10,
        f"{multiplier(-50.0, 1.0):.12f} at V - C = -50 AddOn",
    )
    report.ok(
        "with one maturity bucket the hedging-set effective notional is |D|; offsetting trades in"
        " buckets 1 and 3 net"
        " only partly",
        abs(ir_hedging_set_effective_notional(0, 362.5, 0) - 362.5) < 1e-12
        and 0 < ir_hedging_set_effective_notional(100, 0, -100) < 200,
        f"{ir_hedging_set_effective_notional(100, 0, -100):.4f} for +100 and -100",
    )
    s = 0.3
    ks = [k_reduced([s] * n) for n in (1, 2, 10)]
    report.ok(
        "K_reduced equals SCVA for one counterparty and S sqrt(rho^2 N^2 + (1 - rho^2) N) for N"
        " equal ones, between"
        " sqrt(N) S and N S",
        abs(ks[0] - s) < 1e-15
        and all(
            abs(k - s * math.sqrt(RHO**2 * n**2 + (1 - RHO**2) * n)) < 1e-12
            and math.sqrt(n) * s - 1e-12 <= k <= n * s + 1e-12
            for k, n in zip(ks, (1, 2, 10), strict=True)
        ),
        ", ".join(f"{k / s:.4f} S" for k in ks),
    )
    # Batch L3 audit correction (2026-10-21): the printed MF had dropped the CRE52.48-52.49
    # floor of 10 business days.
    m_week = 5 / 250
    report.ok(
        "MF floor (CRE52.49, 250-day convention): a 5-business-day trade gets sqrt(10/250) = 0.2,"
        " not sqrt(5/250) = 0.1414;"
        " the floor binds only below 10/250 years",
        abs(maturity_factor_unmargined(m_week) - 0.2) < 1e-15
        and abs(maturity_factor_unmargined(m_week) - math.sqrt(m_week)) > 0.05
        and maturity_factor_unmargined(0.5) == math.sqrt(0.5)
        and maturity_factor_unmargined(4.0) == 1.0,
        f"{maturity_factor_unmargined(m_week):.4f} against {math.sqrt(m_week):.4f} unfloored",
    )
    return sd, df


def check_worked_example(report: CheckReport, sd: float, df: float) -> None:
    """Check SA-CCR, default-risk capital and reduced BA-CVA on the worked example."""
    print("== Worked example (original inputs)")
    # A payer swap is long the rate (delta +1, CRE52.39); its 4-year end date puts it in bucket
    # 2 (one to five years).
    d = 100.0 * sd * maturity_factor_unmargined(4.0) * (+1)
    en = ir_hedging_set_effective_notional(0.0, d, 0.0)
    addon = SF_IR * en
    ead, rc, pfe = sa_ccr_ead(2.0, 0.0, addon)
    report.ok(
        "SA-CCR: SD 3.6254, adjusted notional 362.54, add-on 1.8127, RC 2, PFE 1.8127, EAD 5.3378",
        abs(sd - 3.6254) < 5e-5
        and abs(addon - 1.8127) < 5e-5
        and rc == 2.0
        and abs(pfe - 1.8127) < 5e-5
        and abs(ead - 5.3378) < 5e-5,
        f"{sd:.6f}, {d:.4f}, {addon:.6f}, {ead:.6f}",
    )
    ead_c, rc_c, pfe_c = sa_ccr_ead(2.0, 4.0, addon)
    report.ok(
        "with 4 of cash collateral held: RC 0, multiplier 0.5815, PFE 1.0541, EAD 1.4758",
        rc_c == 0.0
        and abs(multiplier(-2.0, addon) - 0.5815) < 5e-5
        and abs(pfe_c - 1.0541) < 5e-5
        and abs(ead_c - 1.4758) < 5e-5,
        f"{multiplier(-2.0, addon):.6f}, {pfe_c:.6f}, {ead_c:.6f}",
    )
    rwa_default = 1.00 * ead
    report.ok(
        "default-risk capital at an illustrative 100 percent risk weight: RWA 5.3378, capital at 8"
        " percent 0.4270",
        abs(rwa_default - 5.3378) < 5e-5 and abs(0.08 * rwa_default - 0.4270) < 5e-5,
        f"{0.08 * rwa_default:.6f}",
    )
    scva = RW_C * 4.0 * ead * df / ALPHA
    cap_cva = DS_BA_CVA * k_reduced([scva])
    report.ok(
        "reduced BA-CVA: DF 0.9063, SCVA 0.4147, capital 0.65 x 0.4147 = 0.2695, RWA 12.5 x"
        " capital = 3.3692",
        abs(df - 0.9063) < 5e-5
        and abs(scva - 0.4147) < 5e-5
        and abs(cap_cva - 0.2695) < 5e-5
        and abs(12.5 * cap_cva - 3.3692) < 5e-5,
        f"{df:.6f}, {scva:.6f}, {cap_cva:.6f}, {12.5 * cap_cva:.6f}",
    )
    # Batch L3 audit correction: M EAD DF / alpha is an exposure-time area (currency x years),
    # not a discounted EE at a date.
    eepe = ead / ALPHA
    area = 4.0 * ead * df / ALPHA
    report.ok(
        "BA-CVA proxy: M EAD DF / alpha = 13.8225 equals the integral of EEPE exp(-0.05 t) over"
        " [0, 4] (currency x years);"
        " divided by M it is EEPE x DF = 3.4556, a time average in currency",
        abs(area - integrate.quad(lambda t: eepe * math.exp(-0.05 * t), 0.0, 4.0)[0]) < 1e-12
        and abs(area - 13.8225) < 5e-5
        and abs(area / 4.0 - 3.4556) < 5e-5
        and abs(scva - RW_C * area) < 1e-12,
        f"EEPE {eepe:.6f}, area {area:.6f}, area / M {area / 4.0:.6f}",
    )
    two = DS_BA_CVA * k_reduced([scva, scva])
    report.ok(
        "two such counterparties: 1.5811 times one, not 2 (rho = 50 percent)",
        abs(two / cap_cva - math.sqrt(2.5)) < 1e-12,
        f"{two:.6f}",
    )
    ead_ceu, _, _ = sa_ccr_ead(2.0, 0.0, addon, alpha=1.0)
    report.ok(
        "US rule for a commercial end-user (alpha 1, 12 CFR 217.132(c)(5)(iv)): EAD 3.8127",
        abs(ead_ceu - 3.8127) < 5e-5,
        f"{ead_ceu:.6f}",
    )


def main() -> int:
    """Print the versions, then run the identities and the worked example with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, SciPy {scipy.__version__}")
    report = CheckReport()
    sd, df = check_identities(report)
    check_worked_example(report, sd, df)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
