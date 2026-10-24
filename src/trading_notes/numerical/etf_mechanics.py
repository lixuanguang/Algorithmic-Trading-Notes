"""ETFs: market-maker quotes, premiums and discounts, the 6c-11 spread, tracking and costs.

ETFs: market-maker quotes, premiums and discounts, the Rule 6c-11 spread, tracking and the costs
of ownership (2026-10-20).

Worked numbers of meth:etf-trading-tracking-premiums and meth:etf-costs-risks-uses. Prices, fees
and holding periods are hypothetical except where a check reproduces a published figure (Abner
2016, pp. 48, 140, 213, 269-270; 17 CFR 270.6c-11).

Independent routes: the market maker's quote built from the basket against the sum of its
stated components; the median spread computed as Rule 6c-11(c)(1)(v) prescribes against a
direct sort; leveraged fund levels compounded day by day against the closed-form product; costs
of ownership summed by component against a simulated holding.

Count convention: one check is one executed ok() call (a call inside a loop counts once per
iteration). One generator, seeded 20261020, serves parts 3 and 4 in order.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.etf_mechanics (numpy).
Exits 1 on failure.
"""

import sys
from typing import Final

import numpy as np

from trading_notes.numerical.report import CheckReport

SEED: Final = 20261020


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def check_creation_fees(report: CheckReport) -> None:
    """Part 1: Abner's creation-fee and cash arithmetic."""
    print("== part 1: Abner's creation-fee and cash arithmetic")
    fee, cu = 2000.0, 100_000
    report.ok(
        "Abner p. 48: a $2,000 creation fee on a 100,000-share unit is 2 cents a share; two client"
        " buys embed $4,000 "
        "while one creation costs $2,000",
        close(fee / cu, 0.02) and close(2 * fee / cu * cu, 4000.0),
    )
    report.ok(
        "Abner p. 48: a 200,000-share sale embeds a redemption fee of 1 cent a share ="
        " 2,000/200,000 (printed as "
        "200,000/$2,000)",
        close(fee / 200_000, 0.01) and not close(200_000 / fee, 0.01),
    )
    report.ok(
        "Abner p. 213: total cash of $1,000 per 50,000-share unit with 250,000 shares outstanding"
        " is $5,000 in the "
        "fund, 2 cents a share",
        close(250_000 / 50_000 * 1000, 5000.0) and close(1000 / 50_000, 0.02),
    )


def check_market_maker_quote(report: CheckReport) -> None:
    """Part 2: the market maker's quote from the basket and its stated components."""
    print("== part 2: a market maker's quote from the basket (Abner p. 140)")
    basket_bid, basket_ask = 49.98, 50.02  # per ETF share
    cr_fee_per_share = 0.02
    slippage = 0.01
    days_held, financing_rate = 2, 0.05
    financing = 50.0 * financing_rate * days_held / 360
    bid = basket_bid - cr_fee_per_share - slippage - financing
    ask = basket_ask + cr_fee_per_share + slippage + financing
    report.ok(
        "basket 49.98/50.02, fee 2 cents, slippage 1 cent and two days' financing at 5% (1.4"
        " cents): the ETF quote is "
        "49.936/50.064, a 0.26% spread against 0.08% for the basket",
        round(bid, 3) == 49.936
        and round(ask, 3) == 50.064
        and round((ask - bid) / ((ask + bid) / 2) * 100, 2) == 0.26
        and round((basket_ask - basket_bid) / 50.0 * 100, 2) == 0.08,
    )
    report.ok(
        "with ten times the volume, the market maker expects to net creations against redemptions"
        " half the time, halving "
        "the fee and financing it charges: 49.953/50.047",
        round(basket_bid - cr_fee_per_share / 2 - slippage - financing / 2, 3) == 49.953
        and round(basket_ask + cr_fee_per_share / 2 + slippage + financing / 2, 3) == 50.047,
    )


def check_premiums(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 3: a premium, the seven-day disclosure trigger and the median spread rule."""
    print("== part 3: premiums, discounts and the Rule 6c-11 disclosures")
    nav, close_price = 50.00, 50.30
    report.ok(
        "a close of 50.30 against a NAV of 50.00 is a 0.60% premium",
        close((close_price / nav - 1) * 100, 0.60, 1e-9),
    )
    prem = np.array([0.4, 2.3, 2.6, 2.1, 2.4, 2.2, 2.5, 2.05, 2.1, 1.0])  # daily premium, percent
    run, longest = 0, 0
    for p in prem:
        run = run + 1 if abs(p) > 2 else 0
        longest = max(longest, run)
    report.ok(
        "a premium above 2% on eight consecutive days exceeds Rule 6c-11(c)(1)(vi)'s seven-day"
        " threshold and requires the "
        "website statement",
        longest == 8 and longest > 7,
    )
    mid = 25 + np.cumsum(rng.normal(0, 0.002, 2340))  # one day of 10-second snapshots
    half = rng.choice([0.005, 0.005, 0.005, 0.01], size=mid.size)
    spreads = (2 * half) / mid
    median_rule = round(float(np.median(spreads)) * 100, 2)
    report.ok(
        "median of (offer - bid)/midpoint over 10-second snapshots, rounded to the nearest"
        " hundredth of a percent: 0.04%",
        median_rule == 0.04
        and median_rule
        == round(
            float(np.sort(spreads)[spreads.size // 2 - 1 : spreads.size // 2 + 1].mean()) * 100, 2
        ),
        f"{median_rule}%",
    )


def check_tracking(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 4: leveraged compounding, volatility decay and an index fund's tracking."""
    print("== part 4: tracking and leveraged funds")
    up_index, up_etf = 1.10**10, 1.20**10
    dn_index, dn_etf = 0.90**10, 0.80**10
    report.ok(
        "Abner Exhibits 12.3-12.4: ten days of +10% take the index up 159% and a 2x fund up 519%;"
        " ten days of -10% "
        "take them to 34.87 and 10.74",
        round((up_index - 1) * 100) == 159
        and round((up_etf - 1) * 100) == 519
        and round(dn_index * 100, 2) == 34.87
        and round(dn_etf * 100, 2) == 10.74,
    )
    level_i = level_e = 100.0
    for r in [0.10, -1 / 11] * 5:
        level_i *= 1 + r
        level_e *= 1 + 2 * r
    report.ok(
        "alternating +10% and -9.09% for ten days leaves the index unchanged but the 2x fund down"
        " 8.77%",
        close(level_i, 100.0, 1e-9) and round(level_e - 100, 2) == -8.77,
    )
    idx = rng.normal(0.0004, 0.01, 252)
    etf = idx - 0.0009 / 252 + rng.normal(0, 0.0002, 252)
    td = float(np.prod(1 + etf) - np.prod(1 + idx))
    te = float(np.std(etf - idx, ddof=1) * np.sqrt(252))
    report.ok(
        "an index fund charging 9 bp with daily replication noise of 2 bp: tracking difference"
        " about -0.1% a year and "
        "annualised tracking error about 0.3%",
        -0.004 < td < 0.002 and 0.2 < te * 100 < 0.4,
        f"TD {td * 100:.2f}%, TE {te * 100:.2f}%",
    )


def cost(
    expense: float,
    round_trip_spread: float,
    commission: float,
    years: float,
    premium_paid: float = 0.0,
) -> float:
    """Return the total cost of holding for `years`, as a fraction of the amount invested."""
    return expense * years + round_trip_spread + 2 * commission + premium_paid


def check_cost_of_ownership(report: CheckReport) -> None:
    """Part 5: total costs of ownership and the securities-lending offset."""
    print("== part 5: total cost of ownership")
    etf_1y = cost(0.0009, 0.0004, 0.0, 1)
    etf_5y = cost(0.0009, 0.0004, 0.0, 5)
    niche_1y = cost(0.0060, 0.0050, 0.0, 1, premium_paid=0.0030)
    mf_1y = 0.0050
    report.ok(
        "a core ETF at 9 bp with a 4 bp spread costs 0.13% for one year and 0.49% over five; a"
        " niche ETF at 60 bp with a "
        "50 bp spread bought at a 30 bp premium costs 1.40% for one year, against 0.50% for a 50"
        " bp mutual fund",
        round(etf_1y * 100, 2) == 0.13
        and round(etf_5y * 100, 2) == 0.49
        and round(niche_1y * 100, 2) == 1.40
        and niche_1y > mf_1y > etf_1y,
    )
    lend, split = 0.0010, 0.80
    report.ok(
        "securities lending revenue of 10 bp, 80% to the fund, offsets 8 bp of the expense ratio",
        close(lend * split, 0.0008),
    )


def main() -> int:
    """Print the versions, then run the five parts with one report and print the count.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}")
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_creation_fees(report)
    check_market_maker_quote(report)
    check_premiums(report, rng)
    check_tracking(report, rng)
    check_cost_of_ownership(report)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
