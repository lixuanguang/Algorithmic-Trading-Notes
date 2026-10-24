"""Exchange-rate mechanics and determination: the worked numbers of nine FX entries.

Exchange-rate mechanics and determination (2026-10-19): the worked numbers of
def:fx-market-real-exchange-rates, meth:cross-forward-rates,
meth:fx-bid-offer-triangular-arbitrage, meth:currency-forward-mark-to-market,
def:exchange-rate-regimes-capital-flows, res:international-parity-conditions,
meth:exchange-rate-forecasting-fair-value, meth:carry-trade-uip and def:flows-policy-exchange-rates.

Notation: EIDM writes A/B for the price of one unit of B (the base currency) in units of A (the
price currency), so USD/EUR 1.30 is 1.30 dollars per euro; the market code for the same quote is
EURUSD.

Reproduced from Economics for Investment Decision Makers (CFA Institute Investment Series,
2013), chaps. 9-10: the euro's 4.00% rise and the dollar's 3.85% fall (p. 487); MXN bid/offer
inversion (Example 9-4, pp. 487-488); a real exchange rate change of about 13% (p. 469); cross
rates 1.3472 and 81.74 with a 0.26 arbitrage (pp. 488-489); GBP/EUR 0.8808 (Example 9-5, p.
492); forward points 26.5 and 5.5 (pp. 492-494); the forward 1.6775 and the 77 bp arbitrage at
1.6900 (p. 495); the Marshall-Lerner sum 0.09 (Exhibit 9-9, p. 514); implied cross bid/offers
104.61/104.65 and 0.8724/0.8726 (pp. 533-535) and Example 10-1 (pp. 536-537); the dealer's
misaligned quote (p. 533); the forward mark-to-market AUD 237,154 (pp. 542-543) and Example
10-3 (USD 79,938, pp. 544-545). Original: covered interest parity with money-market day counts;
the parity conditions tied together; real-interest-differential fair value; forward and
random-walk forecasts on a simulated series with a carry premium; carry-trade P&L and crash
skew; the current-account identity; reserves and crisis warning indicators.

Count convention: one check is one executed ok() call (a call inside a loop counts once per
iteration). One generator, seeded 20261019, serves parts 7 and 8 in order.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.fx_mechanics
(numpy, scipy). Exits 1 on failure.
"""

import sys
from typing import Final

import numpy as np
import scipy
from scipy.stats import skew

from trading_notes.numerical.report import CheckReport

SEED: Final = 20261019


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def check_quotes(report: CheckReport) -> None:
    """Part 1: quotes, percentage changes and the real exchange rate."""
    print("== part 1: quotes, percentage changes and the real exchange rate")
    report.ok(
        "USD/EUR from 1.2500 to 1.3000: the euro rises 4.00%, the dollar falls 3.85% (not 4%)",
        close(1.30 / 1.25 - 1, 0.04, 1e-12) and abs(1.25 / 1.30 - 1 + 0.03846) < 1e-5,
    )
    bid, offer = 12.4020, 12.4060
    report.ok(
        "MXN/USD 12.4020/12.4060 inverts to USD/MXN 0.08061/0.08063: the new bid is 1/old offer",
        round(1 / offer, 5) == 0.08061 and round(1 / bid, 5) == 0.08063,
    )
    real = 1.10 * 1.05 / 1.02 - 1
    report.ok(
        "real GBP/EUR rate: nominal +10%, euro-area prices +5%, U.K. prices +2% gives +13.24%"
        " exactly (about 13% to first"
        " order): Eurozone goods cost the U.K. buyer 13% more in real terms",
        abs(real - 0.13235) < 1e-5 and abs(real - (0.10 + 0.05 - 0.02)) < 0.003,
        f"{real:.4%}",
    )


def check_cross_forward(report: CheckReport) -> None:
    """Part 2: cross rates, forward points and covered interest parity."""
    print("== part 2: cross rates, forward points and covered interest parity")
    cad_eur = 1.0460 * 1.2880
    jpy_cad = 85.50 / 1.0460
    report.ok(
        "CAD/EUR = CAD/USD x USD/EUR = 1.3472; JPY/CAD = JPY/USD / CAD/USD = 81.74; a dealer"
        " quoting"
        " 82.00 offers a 0.26"
        " JPY per CAD triangular arbitrage",
        round(cad_eur, 4) == 1.3472
        and round(jpy_cad, 2) == 81.74
        and abs(82.00 - round(jpy_cad, 2) - 0.26) < 1e-9,
    )
    report.ok(
        "Example 9-5: GBP/EUR = USD/EUR / USD/GBP = 1.3960/1.5850 = 0.8808, expected 1.3863/1.5794"
        " ="
        " 0.8777: sterling"
        " expected to strengthen against the euro",
        round(1.3960 / 1.5850, 4) == 0.8808 and round(1.3863 / 1.5794, 4) == 0.8777,
    )
    spot = 1.2875
    pts = {"1w": -0.3, "1m": -1.1, "3m": -5.5, "6m": -13.3, "12m": -26.5}
    fwd = {k: spot + v / 10_000 for k, v in pts.items()}
    report.ok(
        "forward points (scaled to the fourth decimal): 12-month 1.2875 - 26.5/10,000 = 1.28485;"
        " 3-month 1.28695, a"
        " discount of 0.043%; points grow with maturity",
        close(fwd["12m"], 1.28485, 1e-12)
        and close(fwd["3m"], 1.28695, 1e-12)
        and abs(fwd["3m"] / spot - 1 + 0.00043) < 5e-6
        and all(
            abs(a) < abs(b)
            for a, b in zip(list(pts.values())[:-1], list(pts.values())[1:], strict=True)
        ),
    )
    s_fd, i_d, i_f = 1.6535, 0.035, 0.05
    f_fd = s_fd * (1 + i_f) / (1 + i_d)
    hedged_ret = s_fd * (1 + i_f) / 1.69 - 1
    report.ok(
        "EIDM (f/d convention): 1.6535 x 1.05/1.035 = 1.6775; a misquoted 1.6900 makes the hedged"
        " foreign deposit earn"
        " 2.73% against 3.50% at home: borrow foreign, sell spot, buy forward, deposit at home for"
        " 77 bp",
        round(f_fd, 4) == 1.6775
        and round(hedged_ret, 4) == 0.0273
        and abs((i_d - hedged_ret) - 0.0077) < 5e-5,
    )
    # money-market day counts: 90 days, USD SOFR-like act/360 at 4.30%, GBP act/365 at 3.90%,
    # spot USD/GBP 1.2700
    s0, days, r_usd, r_gbp = 1.2700, 90, 0.043, 0.039
    f0 = s0 * (1 + r_usd * days / 360) / (1 + r_gbp * days / 365)
    report.ok(
        "CIP with day counts (USD act/360 4.30%, GBP act/365 3.90%, 90 days, spot 1.2700 USD per"
        " GBP): forward 1.27143,"
        " +14.3 points; the higher-yielding dollar is at a forward discount",
        abs(f0 - 1.271426) < 1e-6 and round((f0 - s0) * 10_000, 1) == 14.3,
        f"{f0:.6f}",
    )
    report.ok(
        "the hedged GBP deposit earns exactly the USD rate: 1/1.27 x (1 + 0.039 x 90/365) x F = 1 +"
        " 0.043 x 90/360",
        close((1 / s0) * (1 + r_gbp * days / 365) * f0, 1 + r_usd * days / 360, 1e-12),
    )


def check_bid_offer(report: CheckReport) -> None:
    """Part 3: bid-offer spreads, cross bid-offers and triangular arbitrage."""
    print("== part 3: bid-offer spreads, cross bid-offers and triangular arbitrage")
    report.ok(
        "implied JPY/EUR from USD/EUR 1.3649/1.3651 and JPY/USD 76.64/76.66: bid 104.61, offer"
        " 104.65 (multiply bids, multiply"
        " offers)",
        round(76.64 * 1.3649, 2) == 104.61 and round(76.66 * 1.3651, 2) == 104.65,
    )
    gbp_usd_bid, gbp_usd_off = 1 / 1.5646, 1 / 1.5644
    report.ok(
        "implied GBP/EUR needs USD/GBP 1.5644/1.5646 inverted to 0.63914/0.63922 (bid from the"
        " offer): 0.8724/0.8726",
        round(gbp_usd_bid, 5) == 0.63914
        and round(gbp_usd_off, 5) == 0.63922
        and round(gbp_usd_bid * 1.3649, 4) == 0.8724
        and round(gbp_usd_off * 1.3651, 4) == 0.8726,
    )
    sek_eur = (6.8739 * 1.4559, 6.8741 * 1.4561)
    jpy_cad_bo = (81.87 / 0.9546, 81.89 / 0.9544)
    report.ok(
        "Example 10-1: SEK/EUR 10.0077/10.0094; JPY/CAD 85.76/85.80 (JPY/USD bid over CAD/USD"
        " offer,"
        " and vice versa)",
        tuple(round(x, 4) for x in sek_eur) == (10.0077, 10.0094)
        and tuple(round(x, 2) for x in jpy_cad_bo) == (85.76, 85.80),
    )
    report.ok(
        "a dealer at 85.73/85.75 sells CAD below the interbank bid: buy CAD from the dealer at"
        " 85.75, sell it interbank at"
        " 85.76, 0.01 JPY per CAD; at 85.74/85.81 there is no arbitrage",
        abs(round(jpy_cad_bo[0], 2) - 85.75 - 0.01) < 1e-9
        and not (85.81 < jpy_cad_bo[0] or 85.74 > jpy_cad_bo[1]),
    )
    report.ok(
        "a dealer's 1.3652/1.3654 against an interbank 1.3649/1.3651: buy EUR interbank at 1.3651,"
        " sell to the dealer at"
        " 1.3652, one pip (USD 100 per EUR 1 million)",
        abs((1.3652 - 1.3651) * 1_000_000 - 100) < 1e-6,
    )


def check_mark_to_market(report: CheckReport) -> None:
    """Part 4: marking a currency forward to market."""
    print("== part 4: marking a currency forward to market")
    alln = 1.6210 + 130 / 10_000
    cf = (alln - 1.6100) * 10_000_000
    mtm = cf / (1 + 0.048 * 90 / 360)
    report.ok(
        "long GBP 10m at 1.6100 AUD/GBP, three months left: sell GBP forward at the bid, 1.6210 +"
        " 0.0130 = 1.6340; AUD"
        " 240,000 at settlement, worth AUD 237,154 today at 4.80% act/360",
        close(alln, 1.6340, 1e-12) and abs(cf - 240_000) < 1e-6 and round(mtm) == 237_154,
    )
    offset = 0.7830 + (-10.0) / 10_000
    gain = (0.7900 - offset) * 10_000_000
    report.ok(
        "Example 10-3: short NZD 10m at 0.7900 USD/NZD; buy NZD back at the offer 0.7830 - 0.0010 ="
        " 0.7820; USD 80,000 at"
        " settlement, USD 79,938 today at 0.31% USD Libor (discount in the currency of the cash"
        " flow)",
        close(offset, 0.7820, 1e-12)
        and abs(gain - 80_000) < 1e-6
        and round(gain / (1 + 0.0031 * 90 / 360)) == 79_938,
    )


def check_marshall_lerner(report: CheckReport) -> None:
    """Part 5: regimes, trade and the Marshall-Lerner condition."""
    print("== part 5: regimes, trade and the Marshall-Lerner condition")
    wx, ex, wm, em = 0.4, 0.75, 0.6, 0.65
    ml = wx * ex + wm * (em - 1)
    d_exp = 400e6 * 0.10 * ex
    d_imp = 600e6 * 0.10 * (1 - em)
    report.ok(
        "Exhibit 9-9: a 10% depreciation raises exports (EUR 400m, elasticity 0.75) by 30m and"
        " imports (EUR 600m,"
        " elasticity 0.65) by 21m: the balance improves 9m; ML sum 0.4 x 0.75 + 0.6 x (0.65 - 1) ="
        " 0.09 > 0 (the text"
        " prints 0.65 - 4)",
        abs(ml - 0.09) < 1e-12
        and abs(d_exp - 30e6) < 1e-3
        and abs(d_imp - 21e6) < 1e-3
        and abs(ml * 0.10 * 1e9 - 9e6) < 1e-3,
    )
    report.ok(
        "with balanced trade the condition reduces to eps_x + eps_m > 1: 0.75 + 0.65 = 1.40",
        close(0.5 * ex + 0.5 * (em - 1), 0.5 * (ex + em - 1), 1e-12) and ex + em > 1,
    )


def check_parity(report: CheckReport) -> None:
    """Part 6: international parity conditions."""
    print("== part 6: international parity conditions")
    pi_d, pi_f, r_real = 0.03, 0.01, 0.015
    i_dom = (1 + r_real) * (1 + pi_d) - 1
    i_for = (1 + r_real) * (1 + pi_f) - 1
    ppp_change = (1 + pi_d) / (
        1 + pi_f
    ) - 1  # expected change in d/f (domestic currency per foreign)
    uip_change = (1 + i_dom) / (1 + i_for) - 1
    report.ok(
        "with equal real rates (1.5%) and inflation of 3% at home and 1% abroad, Fisher gives"
        " 4.545%"
        " and 2.515%; relative"
        " PPP and UIP both predict the foreign currency rises 1.980% (d/f), and the forward premium"
        " equals it under CIP:"
        " ex ante PPP + Fisher imply real interest parity and the international Fisher effect",
        abs(i_dom - 0.045450) < 1e-6
        and abs(i_for - 0.025150) < 1e-6
        and close(ppp_change, uip_change, 1e-12),
        f"{uip_change:.4%}",
    )
    report.ok(
        "the parity conditions do not tie down the spot level: they relate expected changes and"
        " forwards to rate and"
        " inflation differentials (a check that two spot levels with the same differentials give"
        " the same % forecasts)",
        close((1.30 * (1 + uip_change)) / 1.30, (0.90 * (1 + uip_change)) / 0.90, 1e-15),
    )


def check_forecasting(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 7: fair value, and forward against random-walk forecasts on a simulated series."""
    print("== part 7: fair value and forecasting")
    q_bar, rd, rf, phi_d, phi_f = 1.00, 0.020, 0.005, 0.010, 0.002
    q = q_bar + ((rd - rf) - (phi_d - phi_f))
    report.ok(
        "real-interest-differential model (eq. 10-12, f/d): long-run real rate 1.00 plus a"
        " real-rate gap of 1.5 points"
        " less a risk-premium gap of 0.8 points gives 1.007: the domestic currency sits 0.7% above"
        " fair value",
        abs(q - 1.007) < 1e-12,
    )
    ppp_fair = 1.10 * (110.0 / 100.0) / (105.0 / 100.0)
    report.ok(
        "PPP fair value: base-year rate 1.10 d/f, domestic CPI 110, foreign CPI 105 gives 1.1524; a"
        " spot of 1.20 leaves the"
        " foreign currency 4.1% above PPP",
        abs(ppp_fair - 1.152381) < 1e-6 and abs(1.20 / ppp_fair - 1 - 0.0413) < 1e-4,
    )
    n = 600
    diff = 0.03 / 12  # foreign rate 3 points above domestic, monthly
    s = np.empty(n + 1)
    s[0] = np.log(1.0)
    shocks = rng.normal(0.0, 0.025, n)
    for t in range(n):  # log d/f: UIP fails; the high-yield currency does not depreciate on average
        s[t + 1] = s[t] + shocks[t]
    fwd_fc = s[:-1] - diff  # forward (log) under CIP: foreign at a discount
    rw_fc = s[:-1]
    rmse_fwd = np.sqrt(np.mean((s[1:] - fwd_fc) ** 2))
    rmse_rw = np.sqrt(np.mean((s[1:] - rw_fc) ** 2))
    report.ok(
        "on a simulated monthly series where UIP fails (no depreciation of the high-yield"
        " currency), the random walk"
        " beats the forward as a forecast, but only slightly: the 0.25% monthly forward discount is"
        " small against 2.5%"
        " monthly volatility",
        bool(rmse_rw < rmse_fwd < rmse_rw * 1.01),
        f"RMSE forward {rmse_fwd:.5f}, random walk {rmse_rw:.5f}",
    )


def check_carry(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 8: carry-trade P&L, and the skew of a return stream with rare crashes."""
    print("== part 8: the carry trade")
    i_fund, i_target, dep = 0.001, 0.045, 0.03
    pnl = (1 + i_target) * (1 - dep) - (1 + i_fund)
    report.ok(
        "borrow JPY at 0.1%, invest AUD at 4.5% for a year; the AUD falls 3%: profit 1.265% of the"
        " funding (carry 4.4"
        " points less 3 points of depreciation and a 0.135 cross term); UIP would have predicted a"
        " 4.21% fall",
        abs(pnl - 0.01265) < 1e-12 and abs((1 + i_fund) / (1 + i_target) - 1 + 0.04211) < 1e-5,
    )
    months = 1200
    crash = rng.random(months) < 0.02
    monthly = np.where(crash, rng.normal(-0.08, 0.03, months), rng.normal(0.006, 0.015, months))
    report.ok(
        "a carry return stream that earns 0.6% a month but crashes 8% in 2% of months has a"
        " positive mean and strong"
        " negative skew: small steady gains, rare large losses",
        bool(monthly.mean() > 0 and skew(monthly) < -1.5),
        f"mean {monthly.mean():.4%}, skew {skew(monthly):.2f}",
    )


def check_flows(report: CheckReport) -> None:
    """Part 9: payment flows, policy and crisis warnings."""
    print("== part 9: payment flows, policy and crisis warnings")
    s_priv, inv, fiscal = 0.18, 0.22, -0.03
    ca = (s_priv - inv) + fiscal
    report.ok(
        "current account = (private saving - investment) + government balance: 18% - 22% - 3% = -7%"
        " of GDP, financed by a"
        " capital inflow of the same size",
        abs(ca + 0.07) < 1e-12,
    )
    reserves = np.array([100.0, 98, 95, 90, 82, 70])
    real_fx = np.array([100.0, 104, 109, 114, 118, 123])
    signals = {
        "reserves down > 25% in 5 months": reserves[-1] / reserves[0] - 1 < -0.25,
        "real appreciation > 20% (overvaluation)": real_fx[-1] / real_fx[0] - 1 > 0.20,
    }
    report.ok(
        "early-warning signals in EIDM's list: reserves falling 30% and a 23% real appreciation"
        " both"
        " flash; EIDM warns that"
        " interest differentials and ratings often fail to widen before crises",
        all(signals.values()),
    )


def main() -> int:
    """Print the versions, then run the nine parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_quotes(report)
    check_cross_forward(report)
    check_bid_offer(report)
    check_mark_to_market(report)
    check_marshall_lerner(report)
    check_parity(report)
    rng = np.random.default_rng(SEED)
    check_forecasting(report, rng)
    check_carry(report, rng)
    check_flows(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
