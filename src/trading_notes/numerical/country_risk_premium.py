"""Country-risk example of meth:cost-of-debt-equity-estimation.

Library gap-filling Batch L6, package L6-a (2026-10-21). Inputs and acceptance were fixed before the first run.
Part 1 reproduces Damodaran, Applied Corporate Finance, 4th ed. (2014): Table 4.5 (p. 100), Illustration 4.2 and
Table 4.9 (pp. 106-107), and the Vale R$ cost of equity (pp. 134-135), to their printed rounding. Part 2 computes the
original example in floating point and again in exact rational arithmetic and compares both with hand values. Part 3
checks the zero-country-premium limit. All rates are annual and in percent. Deterministic; synthetic inputs except the
reproduced figures.

First run (recorded in the L6 review record): two failures, both in the harness: India's bond volatility taken from
the p. 100 formula line instead of Table 4.5, and a mistyped hand literal (17.10705 for 1.1324 x 1.06 / 1.025 - 1 =
17.10673 percent). Both corrected; no tolerance changed.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.country_risk_premium
"""

# standard library imports
import sys
from fractions import Fraction

# project library imports
from trading_notes.numerical.report import CheckReport

# The premium formulas and the example take float or Fraction inputs and keep that type, so the exact run never
# passes through floating point.


def default_spread_crp[T: (float, Fraction)](spread: T) -> T:
    """Return the country premium as the sovereign default spread."""
    return spread


def relative_sd_crp[T: (float, Fraction)](mature_erp: T, sd_country: T, sd_mature: T) -> T:
    """Return the country premium from relative equity volatility: ERP sd_country / sd_mature - ERP."""
    return mature_erp * sd_country / sd_mature - mature_erp


def melded_crp[T: (float, Fraction)](spread: T, sd_equity: T, sd_bond: T) -> T:
    """Return the melded country premium: default spread scaled by equity over bond volatility."""
    return spread * sd_equity / sd_bond


def example[T: (float, Fraction)](kind: type[T]) -> dict[str, T]:
    """Compute the original example's premiums and costs of equity in the arithmetic of kind.

    Args:
        kind: float, or Fraction for exact rational arithmetic.

    Returns:
        Each named result, in percent, of type kind.
    """
    rf, erp, spread = kind(4), kind(5), kind(3)
    sd_c, sd_m, sd_b = kind(30), kind(18), kind(20)
    beta, w_country = kind(12) / 10, kind(6) / 10
    local_bond, local_spread, inf_l, inf_u = kind(11), kind(5) / 2, kind(6), kind(5) / 2
    crp = {
        "default spread": default_spread_crp(spread),
        "relative sd": relative_sd_crp(erp, sd_c, sd_m),
        "melded": melded_crp(spread, sd_c, sd_b),
    }
    out = {f"crp {k}": v for k, v in crp.items()}
    out |= {f"total {k}": erp + v for k, v in crp.items()}
    out["ke scaled"] = rf + beta * (erp + crp["melded"])
    out["ke additive"] = rf + beta * erp + crp["melded"]
    out["weighted erp"] = w_country * (erp + crp["melded"]) + (1 - w_country) * erp
    out["ke weighted"] = rf + beta * out["weighted erp"]
    out["local rf"] = local_bond - local_spread
    out["ke local inflation"] = (
        (1 + out["ke weighted"] / 100) * (1 + inf_l / 100) / (1 + inf_u / 100) - 1
    ) * 100
    out["ke local kept premium"] = out["local rf"] + beta * out["weighted erp"]
    out["ke double counted"] = local_bond + beta * out["weighted erp"]
    return out


def zero_limit() -> tuple[float, float, float, float]:
    """Return the default-spread and melded premiums, cost of equity and relative-sd premium at spread 0."""
    spread = 0.0
    crp_ds, crp_m = default_spread_crp(spread), melded_crp(spread, 30, 20)
    return crp_ds, crp_m, 4.0 + 1.2 * (5.0 + crp_m), relative_sd_crp(5.0, 30, 18)


def check_printed_figures(report: CheckReport) -> None:
    """Part 1: Damodaran's printed figures, to their printed rounding."""
    print("== part 1: Damodaran's printed figures")
    us = 4.20
    table = {  # spread, equity sd, US sd, bond sd; printed relative-sd and melded country premiums
        "Brazil": (2.00, 21, 15, 14, 1.68, 3.00),
        "India": (2.25, 24, 15, 15, 2.52, 3.60),
        "China": (0.80, 18, 15, 10, 0.84, 1.44),
    }
    for c, (sp, se, su, sb, p_rel, p_mel) in table.items():
        rel, mel = relative_sd_crp(us, se, su), melded_crp(sp, se, sb)
        report.ok(
            f"Table 4.5 {c}: relative-sd {p_rel:.2f}, melded {p_mel:.2f}",
            abs(rel - p_rel) <= 0.005 and abs(mel - p_mel) <= 0.005,
            f"{rel:.4f}, {mel:.4f}",
        )
    report.ok(
        "Illustration 4.2: 5.5 plus melded premiums gives 8.50, 9.10, 6.94",
        all(abs(5.5 + v - t) <= 0.005 for v, t in ((3.00, 8.50), (3.60, 9.10), (1.44, 6.94))),
    )
    # Source slip, found on the first run: Table 4.5 prints India's melded premium as (24%/15%)(2.25%) = 3.60, while the
    # formula line on p. 100 prints 4.20% + 2.25%(24%/17%) = 7.80%; 24/17 gives 7.38, so only the table's 15 is consistent
    # with the printed 3.60 and 7.80. The first run wrongly used 17 as the gated input; the table is gated, the line reported.
    print(
        f"    p. 100 formula line with 17: 4.20 + {melded_crp(2.25, 24, 17):.4f} = {4.20 + melded_crp(2.25, 24, 17):.4f}, printed 7.80"
    )
    disney = (82.01 * 5.50 + 11.64 * 6.72 + 6.02 * 7.27 + 0.33 * 9.44) / 100
    report.ok(
        "Table 4.9 Disney revenue-weighted premium 5.76",
        abs(disney - 5.76) <= 0.005,
        f"{disney:.4f}",
    )
    k_usd = 2.75 + 1.1503 * 7.38
    naive = 10.18 + 1.15 * 7.38
    scaled = ((1 + k_usd / 100) * 1.09 / 1.02 - 1) * 100
    report.ok(
        "Vale in R$: 18.67 keeping the dollar premium, 18.87 by the inflation differential",
        abs(naive - 18.67) <= 0.005 and abs(scaled - 18.87) <= 0.005,
        f"dollar cost {k_usd:.4f}; {naive:.4f} and {scaled:.4f}",
    )


def check_original_example(report: CheckReport) -> None:
    """Part 2: the original example in float and exact rational arithmetic, against hand values."""
    print("== part 2: original example (float and exact rational)")
    fl, ex = example(float), example(Fraction)
    hand = {
        "crp default spread": 3.0, "crp relative sd": 3.33333, "crp melded": 4.5,
        "total default spread": 8.0, "total relative sd": 8.33333, "total melded": 9.5,
        "ke scaled": 15.4, "ke additive": 14.5, "weighted erp": 7.7, "ke weighted": 13.24,
        "local rf": 8.5, "ke local inflation": 17.10673, "ke local kept premium": 17.74, "ke double counted": 20.24,
    }  # fmt: skip
    for k, h in hand.items():
        report.ok(
            f"{k}: float = exact, and = hand {h}",
            abs(fl[k] - float(ex[k])) <= 1e-12 and abs(fl[k] - h) <= 5e-5,
            f"{fl[k]:.6f}",
        )


def check_zero_limit(report: CheckReport) -> None:
    """Part 3: the zero-country-premium limit."""
    print("== part 3: zero-country-premium limit")
    ds0, m0, ke0, rel0 = zero_limit()
    report.ok(
        "spread 0: default-spread and melded premiums are 0 and the cost of equity is the mature CAPM 10.0",
        ds0 == 0 and m0 == 0 and ke0 == 10.0,
    )
    report.ok(
        "the relative-volatility method does not use the spread: still 3.3333",
        abs(rel0 - 10 / 3) <= 1e-12,
        f"{rel0:.4f}",
    )
    report.ok(
        "relative-volatility premium is 0 only when the volatilities are equal",
        relative_sd_crp(5.0, 18, 18) == 0.0,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    print(f"Python {sys.version.split()[0]}")
    report = CheckReport()
    check_printed_figures(report)
    check_original_example(report)
    check_zero_limit(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
