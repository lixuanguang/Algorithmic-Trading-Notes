"""Country-risk example of the cost-of-equity entry: printed figures, an exact run and a limit."""

import sys
from fractions import Fraction

from trading_notes.numerical.capital_structure_cost_of_capital.country_risk import CountryRisk
from trading_notes.numerical.report import CheckReport, print_versions


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
    country = CountryRisk(spread=spread, sd_equity=sd_c, sd_bond=sd_b)
    crp = {
        "default spread": country.default_spread_premium(),
        "relative sd": country.relative_sd_premium(erp, sd_m),
        "melded": country.melded_premium(),
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
    """Return the default-spread and melded premiums, ke and relative-sd premium at spread 0."""
    country = CountryRisk(spread=0.0, sd_equity=30.0, sd_bond=20.0)
    crp_ds, crp_m = country.default_spread_premium(), country.melded_premium()
    return crp_ds, crp_m, 4.0 + 1.2 * (5.0 + crp_m), country.relative_sd_premium(5.0, 18.0)


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
        country = CountryRisk(spread=sp, sd_equity=se, sd_bond=sb)
        rel, mel = country.relative_sd_premium(us, su), country.melded_premium()
        report.ok(
            f"Table 4.5 {c}: relative-sd {p_rel:.2f}, melded {p_mel:.2f}",
            abs(rel - p_rel) <= 0.005 and abs(mel - p_mel) <= 0.005,
            f"{rel:.4f}, {mel:.4f}",
        )
    report.ok(
        "Illustration 4.2: 5.5 plus melded premiums gives 8.50, 9.10, 6.94",
        all(abs(5.5 + v - t) <= 0.005 for v, t in ((3.00, 8.50), (3.60, 9.10), (1.44, 6.94))),
    )
    # Table 4.5 prints India's melded premium as (24%/15%)(2.25%) = 3.60, while the formula line
    # on p. 100 prints 4.20% + 2.25%(24%/17%) = 7.80%; 24/17 gives 7.38, so only the table's 15
    # is consistent with both printed results. The table is checked; the line is only printed.
    india_p100 = CountryRisk(spread=2.25, sd_equity=24.0, sd_bond=17.0).melded_premium()
    print(
        f"    p. 100 formula line with 17: 4.20 + {india_p100:.4f} ="
        f" {4.20 + india_p100:.4f}, printed 7.80"
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
        "local rf": 8.5, "ke local inflation": 17.10673, "ke local kept premium": 17.74,
        "ke double counted": 20.24,
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
        "spread 0: default-spread and melded premiums are 0 and the cost of equity is the mature"
        " CAPM 10.0",
        ds0 == 0 and m0 == 0 and ke0 == 10.0,
    )
    report.ok(
        "the relative-volatility method does not use the spread: still 3.3333",
        abs(rel0 - 10 / 3) <= 1e-12,
        f"{rel0:.4f}",
    )
    report.ok(
        "relative-volatility premium is 0 only when the volatilities are equal",
        CountryRisk(spread=3.0, sd_equity=18.0, sd_bond=20.0).relative_sd_premium(5.0, 18.0) == 0.0,
    )


def main() -> int:
    """Run every check with a fresh report and return the exit status (0 or 1).

    Part 1 reproduces Damodaran, Applied Corporate Finance, 4th ed. (2014): Table 4.5 (p. 100),
    Illustration 4.2 and Table 4.9 (pp. 106-107), and the Vale R$ cost of equity (pp. 134-135), to
    their printed rounding; India's bond volatility is Table 4.5's, not the p. 100 formula line.
    Part 2 computes the original example in floating point and in exact rational arithmetic and
    compares both with hand values. Part 3 checks the zero-country-premium limit. Rates are annual,
    in percent; deterministic; synthetic inputs except the reproduced figures.
    """
    print_versions()
    report = CheckReport()
    check_printed_figures(report)
    check_original_example(report)
    check_zero_limit(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
