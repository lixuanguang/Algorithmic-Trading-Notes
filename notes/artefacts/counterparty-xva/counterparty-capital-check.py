"""Library gap-filling Batch L3, package P10 (2026-10-21): the worked example of rule:counterparty-credit-cva-capital.

Deterministic, original inputs. Formulas from the Basel Framework as retrieved on 2026-10-21: SA-CCR (CRE52.1,
52.10, 52.20, 52.23, 52.34, 52.39, 52.48 and 52.57; version effective 1 January 2023) and the reduced basic approach
for CVA risk (MAR50.1 and 50.14-50.16; version effective 1 January 2023). One unmargined netting set holding a
four-year payer interest rate swap on 100 notional, mark-to-market V = 2 to the bank; the counterparty is an
investment-grade industrial (MAR50.16, Table 1: RW = 3 percent). The swap's remaining maturity, 4 years, stands in
for the effective maturity M of CRE32.46-32.54 (illustration only). The default-risk risk weight of 100 percent is
illustrative, not taken from the credit-risk chapters.

Run: uv run python counterparty-capital-check.py   (scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys

# third party library imports
import scipy
from scipy import integrate

print(f"Python {sys.version.split()[0]}, SciPy {scipy.__version__}")
fails = []


def ok(name, cond, detail=""):
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


ALPHA, FLOOR, SF_IR = 1.4, 0.05, 0.005
RHO, DS_BA_CVA = 0.5, 0.65


def supervisory_duration(s, e):
    """CRE52.34: SD = (exp(-0.05 S) - exp(-0.05 E)) / 0.05."""
    return (math.exp(-0.05 * s) - math.exp(-0.05 * e)) / 0.05


def maturity_factor_unmargined(m):
    """CRE52.48: MF = sqrt(min(M, 1) / 1), M floored at 10 business days (10/250 years)."""
    return math.sqrt(min(max(m, 10 / 250), 1.0))


def ir_hedging_set_effective_notional(d1, d2, d3):
    """CRE52.57, step 5 with offsets across the three maturity buckets."""
    return math.sqrt(d1**2 + d2**2 + d3**2 + 1.4 * d1 * d2 + 1.4 * d2 * d3 + 0.6 * d1 * d3)


def multiplier(v_minus_c, addon):
    """CRE52.23: min{1; floor + (1 - floor) exp((V - C) / (2 (1 - floor) AddOn))}."""
    return min(1.0, FLOOR + (1 - FLOOR) * math.exp(v_minus_c / (2 * (1 - FLOOR) * addon)))


def sa_ccr_ead(v, c, addon, alpha=ALPHA):
    """CRE52.1, 52.10 and 52.20: EAD = alpha (RC + PFE) for an unmargined netting set."""
    rc = max(v - c, 0.0)
    pfe = multiplier(v - c, addon) * addon
    return alpha * (rc + pfe), rc, pfe


def supervisory_df(m):
    """MAR50.15: DF = (1 - exp(-0.05 M)) / (0.05 M) for banks not using the IMM."""
    return (1 - math.exp(-0.05 * m)) / (0.05 * m)


def k_reduced(scva):
    """MAR50.14: K = sqrt((rho sum SCVA)^2 + (1 - rho^2) sum SCVA^2)."""
    return math.sqrt((RHO * sum(scva)) ** 2 + (1 - RHO**2) * sum(s * s for s in scva))


print("== Formula identities")
sd = supervisory_duration(0.0, 4.0)
ok(
    "SD equals the integral of exp(-0.05 t) from S to E (a continuously discounted annuity at 5 percent)",
    abs(sd - integrate.quad(lambda t: math.exp(-0.05 * t), 0.0, 4.0)[0]) < 1e-12,
    f"{sd:.6f}",
)
df = supervisory_df(4.0)
ok(
    "DF equals the time average of exp(-0.05 t) over [0, M] (MAR50.15, footnote 3)",
    abs(df - integrate.quad(lambda t: math.exp(-0.05 * t), 0.0, 4.0)[0] / 4.0) < 1e-12,
    f"{df:.6f}",
)
ok(
    "the multiplier is 1 whenever V - C >= 0, tends to the 5 percent floor and never reaches it",
    multiplier(0.0, 1.0) == 1.0
    and multiplier(3.0, 1.0) == 1.0
    and FLOOR < multiplier(-50.0, 1.0) < FLOOR + 1e-10,
    f"{multiplier(-50.0, 1.0):.12f} at V - C = -50 AddOn",
)
ok(
    "with one maturity bucket the hedging-set effective notional is |D|; offsetting trades in buckets 1 and 3 net"
    " only partly",
    abs(ir_hedging_set_effective_notional(0, 362.5, 0) - 362.5) < 1e-12
    and 0 < ir_hedging_set_effective_notional(100, 0, -100) < 200,
    f"{ir_hedging_set_effective_notional(100, 0, -100):.4f} for +100 and -100",
)
s = 0.3
ks = [k_reduced([s] * n) for n in (1, 2, 10)]
ok(
    "K_reduced equals SCVA for one counterparty and S sqrt(rho^2 N^2 + (1 - rho^2) N) for N equal ones, between"
    " sqrt(N) S and N S",
    abs(ks[0] - s) < 1e-15
    and all(
        abs(k - s * math.sqrt(RHO**2 * n**2 + (1 - RHO**2) * n)) < 1e-12
        and math.sqrt(n) * s - 1e-12 <= k <= n * s + 1e-12
        for k, n in zip(ks, (1, 2, 10), strict=True)
    ),
    ", ".join(f"{k / s:.4f} S" for k in ks),
)

print("== Worked example (original inputs)")
# A payer swap is long the rate (delta +1, CRE52.39); its 4-year end date puts it in bucket 2 (one to five years).
d = 100.0 * sd * maturity_factor_unmargined(4.0) * (+1)
en = ir_hedging_set_effective_notional(0.0, d, 0.0)
addon = SF_IR * en
ead, rc, pfe = sa_ccr_ead(2.0, 0.0, addon)
ok(
    "SA-CCR: SD 3.6254, adjusted notional 362.54, add-on 1.8127, RC 2, PFE 1.8127, EAD 5.3378",
    abs(sd - 3.6254) < 5e-5
    and abs(addon - 1.8127) < 5e-5
    and rc == 2.0
    and abs(pfe - 1.8127) < 5e-5
    and abs(ead - 5.3378) < 5e-5,
    f"{sd:.6f}, {d:.4f}, {addon:.6f}, {ead:.6f}",
)
ead_c, rc_c, pfe_c = sa_ccr_ead(2.0, 4.0, addon)
ok(
    "with 4 of cash collateral held: RC 0, multiplier 0.5815, PFE 1.0541, EAD 1.4758",
    rc_c == 0.0
    and abs(multiplier(-2.0, addon) - 0.5815) < 5e-5
    and abs(pfe_c - 1.0541) < 5e-5
    and abs(ead_c - 1.4758) < 5e-5,
    f"{multiplier(-2.0, addon):.6f}, {pfe_c:.6f}, {ead_c:.6f}",
)
rwa_default = 1.00 * ead
ok(
    "default-risk capital at an illustrative 100 percent risk weight: RWA 5.3378, capital at 8 percent 0.4270",
    abs(rwa_default - 5.3378) < 5e-5 and abs(0.08 * rwa_default - 0.4270) < 5e-5,
    f"{0.08 * rwa_default:.6f}",
)
RW_C = 0.03
scva = RW_C * 4.0 * ead * df / ALPHA
cap_cva = DS_BA_CVA * k_reduced([scva])
ok(
    "reduced BA-CVA: DF 0.9063, SCVA 0.4147, capital 0.65 x 0.4147 = 0.2695, RWA 12.5 x capital = 3.3692",
    abs(df - 0.9063) < 5e-5
    and abs(scva - 0.4147) < 5e-5
    and abs(cap_cva - 0.2695) < 5e-5
    and abs(12.5 * cap_cva - 3.3692) < 5e-5,
    f"{df:.6f}, {scva:.6f}, {cap_cva:.6f}, {12.5 * cap_cva:.6f}",
)
two = DS_BA_CVA * k_reduced([scva, scva])
ok(
    "two such counterparties: 1.5811 times one, not 2 (rho = 50 percent)",
    abs(two / cap_cva - math.sqrt(2.5)) < 1e-12,
    f"{two:.6f}",
)
ead_ceu, _, _ = sa_ccr_ead(2.0, 0.0, addon, alpha=1.0)
ok(
    "US rule for a commercial end-user (alpha 1, 12 CFR 217.132(c)(5)(iv)): EAD 3.8127",
    abs(ead_ceu - 3.8127) < 5e-5,
    f"{ead_ceu:.6f}",
)

if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("all checks passed")
