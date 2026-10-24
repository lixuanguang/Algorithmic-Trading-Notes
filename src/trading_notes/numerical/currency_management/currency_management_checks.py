"""Currency management: the worked numbers of four currency entries."""

import math
import sys
from typing import Final

import numpy as np
import scipy

from trading_notes.numerical.currency_management.currency_hedging import (
    CrossHedge,
    CurrencyExposure,
    GarmanKohlhagen,
)
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close

SEED: Final = 20261019
# The equity and bond holdings' local and currency volatility and their correlation.
EQ: Final = CurrencyExposure(local_vol=0.16, fx_vol=0.10, correlation=-0.30)
BD: Final = CurrencyExposure(local_vol=0.04, fx_vol=0.10, correlation=-0.05)


def check_effects(report: CheckReport) -> None:
    """Part 1: currency effects on return and risk, and the minimum-variance hedge ratios."""
    eq, bd = EQ, BD
    print("== part 1: currency effects on return and risk")
    report.ok(
        "PMiP eq. (1): a 10% foreign-currency return with a 5% rise in the foreign currency gives"
        " 15.5% (15% to first"
        " order)",
        close(1.10 * 1.05 - 1, 0.155, 1e-12),
    )
    r_dc = 0.80 * (50.70 / 43.80) * (85.78 / 84.12) + 0.20 * (12.17 / 14.08) * (67.81 / 65.36) - 1
    report.ok(
        "PMiP eq. (2), Indian investor: 80% in GBP assets (43.80m to 50.70m, INR/GBP 84.12 to"
        " 85.78) and 20% in EUR assets"
        " (14.08m to 12.17m, INR/EUR 65.36 to 67.81): domestic-currency return 12.4%",
        round(r_dc, 3) == 0.124,
        f"{r_dc:.4%}",
    )
    report.ok(
        "PMiP eq. (5): unhedged equities (16% local volatility, 10% currency volatility,"
        " correlation -0.3) have 16.1%"
        " domestic volatility, barely above local; unhedged bonds (4%, 10%, -0.05) have 10.6%,"
        " dominated by currency",
        abs(eq.domestic_vol() - 0.1611) < 1e-3 and abs(bd.domestic_vol() - 0.1058) < 1e-3,
    )
    h_eq, h_bd = eq.min_variance_hedge(), bd.min_variance_hedge()
    report.ok(
        "minimum-variance hedge ratios: 52% for the equities (the currency partly hedges the equity"
        " risk) and 98% for the"
        " bonds, close to a full hedge, as Campbell et al. find for bond investors",
        abs(h_eq - 0.52) < 1e-12
        and abs(h_bd - 0.98) < 1e-12
        and eq.domestic_vol(h_eq) < eq.domestic_vol(1.0),
        f"equity vol at h* {eq.domestic_vol(h_eq):.4f}, fully hedged {eq.domestic_vol(1.0):.4f}",
    )


def check_hedge_ratios(report: CheckReport) -> None:
    """Part 2: rolling a hedge with an FX swap, roll yield and a hedging budget."""
    eq, bd = EQ, BD
    print("== part 2: hedge ratios with forwards and FX swaps, and roll yield")
    notional_old, value_now = 8_000_000, 8_500_000  # EUR exposure hedged by selling EUR forward
    f_old, s_now, fwd_pts_1m = 1.1000, 1.0850, 12.0 / 10_000  # USD per EUR
    settle = (f_old - s_now) * notional_old
    f_new = s_now + fwd_pts_1m
    report.ok(
        "rolling a hedge: the 8m EUR forward sold at 1.1000 settles against spot 1.0850 for a USD"
        " 120,000 gain; the FX swap"
        " buys 8m EUR spot and sells 8.5m EUR one month forward at 1.0862, lifting the hedge ratio"
        " back to 100% of the"
        " asset now worth 8.5m",
        abs(settle - 120_000) < 1e-6
        and close(f_new, 1.0862, 1e-12)
        and close(8_500_000 / value_now, 1.0),
    )
    fp_prem = (1.0862 - 1.0850) / 1.0850
    report.ok(
        "roll yield: selling EUR at a forward premium of 12 points earns about 0.11% a month (1.3%"
        " a"
        " year) as the forward"
        " rolls down to spot, all else equal; buying at a premium would cost the same",
        abs(fp_prem - 0.0011060) < 1e-6 and abs(fp_prem * 12 - 0.01327) < 1e-4,
    )
    _hedge_cost_annual, vol_cut = (
        0.015,
        bd.domestic_vol() - bd.domestic_vol(1.0),
    )  # the cost is quoted
    report.ok(
        "a hedging budget: if the investor's currency trades at a 1.5%-a-year forward premium"
        " against it (negative roll),"
        " fully hedging bonds costs 1.5% a year for a 6.6-point cut in volatility; for equities the"
        " cut is only 0.1"
        " point, so the cost is harder to justify",
        abs(vol_cut - 0.0658) < 1e-3
        and abs(eq.domestic_vol() - eq.domestic_vol(1.0) - 0.0011) < 1e-3,
    )


def check_options(report: CheckReport) -> None:
    """Part 3: protective puts, a risk reversal, a put spread and a seagull."""
    print("== part 3: options to reduce hedging costs")
    S0 = 1.0850  # a USD-based investor long EUR assets
    fx = GarmanKohlhagen(
        spot=S0, maturity=0.25, domestic_rate=0.043, foreign_rate=0.025, volatility=0.08
    )
    put_atm = fx.put(S0)
    put_otm = fx.put(1.05)
    call_k = next(k / 10_000 for k in range(10_850, 12_500) if fx.call(k / 10_000) <= put_otm)
    put_low = fx.put(1.01)
    report.ok(
        "protective puts on EUR (8% volatility, 3 months): at the money 1.37% of notional, 3.2% out"
        " of the money (1.05)"
        " 0.37%: cheaper, with the first 3% of a fall unprotected",
        abs(put_atm / S0 - 0.0137) < 5e-5 and abs(put_otm / S0 - 0.0037) < 5e-5,
        f"ATM {put_atm / S0:.4%}, OTM {put_otm / S0:.4%}",
    )
    report.ok(
        "risk reversal (collar): selling a 1.1323 call pays for the 1.05 put, a zero-premium hedge"
        " that gives up upside"
        " above 1.1323",
        abs(call_k - 1.1323) < 0.0002 and fx.call(call_k) <= put_otm,
        f"call strike {call_k:.4f}",
    )
    seagull_cost = put_otm - put_low - fx.call(call_k)
    report.ok(
        "put spread and seagull: selling a 1.01 put cuts the 1.05 put's cost by about a tenth;"
        " adding the short call makes"
        " the package net-premium-receiving, but losses below 1.01 return in full",
        put_low < put_otm and abs(put_low / put_otm - 0.115) < 0.01 and seagull_cost < 0,
        f"put spread cost {put_otm - put_low:.5f}, seagull {seagull_cost:.5f}",
    )


def check_cross_hedges(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 4: a cross hedge and its ledger, a regression hedge and an NDF settlement."""
    print(
        "== part 4: multiple currencies, cross hedges, minimum-variance hedges, basis risk,"
        " emerging markets"
    )
    cross = CrossHedge(exposure_vol=0.11, proxy_vol=0.10, correlation=0.85)
    h_cross = cross.ratio()
    resid = cross.residual_vol()
    report.ok(
        "cross hedge: hedging NZD exposure with AUD forwards (correlation 0.85) uses a USD-valued"
        " exposure ratio of 0.935 and leaves 5.8%"
        " residual volatility out of 11%: basis risk remains",
        abs(h_cross - 0.935) < 1e-12 and abs(resid - 0.05795) < 1e-4,
    )
    n_nzd, usd_nzd, usd_aud = 1_000_000.0, 0.60, 0.66
    n_aud = h_cross * n_nzd * usd_nzd / usd_aud
    report.ok(
        "currency units: sell 850,000 AUD against one million NZD", close(n_aud, 850_000, 1e-7)
    )
    # Reprice two currency balances, rather than reusing the return-hedge formula.
    spot_nzd1, spot_aud1 = 0.54, 0.6072
    pnl_asset = n_nzd * (spot_nzd1 - usd_nzd)
    pnl_forward = n_aud * (usd_aud - spot_aud1)  # F0=S0, zero rates and costs
    pnl = pnl_asset + pnl_forward
    report.ok(
        "USD ledger: -60,000 + 44,880 = -15,120",
        close(pnl, -15_120, 1e-7) and close(pnl / (n_nzd * usd_nzd), -0.0252),
    )
    for scale_nzd, scale_aud in ((1, 100), (100, 1), (100, 100)):
        nn = n_nzd * scale_nzd
        sn, sa = usd_nzd / scale_nzd, usd_aud / scale_aud
        na = h_cross * nn * sn / sa
        ledger = nn * (spot_nzd1 / scale_nzd - sn) + na * (sa - spot_aud1 / scale_aud)
        report.ok(
            f"unit invariance with NZD scale {scale_nzd}, AUD scale {scale_aud}",
            close(ledger, pnl, 1e-7) and close(na / scale_aud, n_aud, 1e-7),
        )
    rf_aud, tau = 0.04, 0.5
    forward_notional = n_aud * math.exp(rf_aud * tau)
    # Central difference of the forward present value: N(F Dd - S Df).
    delta = (
        (-forward_notional * (usd_aud + 1e-5) * math.exp(-rf_aud * tau))
        - (-forward_notional * (usd_aud - 1e-5) * math.exp(-rf_aud * tau))
    ) / 2e-5
    report.ok(
        "nonzero-rate forward delta matches the desired AUD spot exposure",
        abs(delta + n_aud) < 1e-4,
    )
    n = 120
    r_fx = rng.normal(0, 0.03, n)
    r_fc = rng.normal(0.006, 0.04, n) - 0.4 * r_fx
    r_dc = (1 + r_fc) * (1 + r_fx) - 1
    beta = np.polyfit(r_fx, r_dc, 1)[0]
    grid = np.linspace(0, 1.5, 301)
    best = grid[np.argmin([np.var(r_dc - h * r_fx) for h in grid])]
    report.ok(
        "minimum-variance hedge by regression: regressing monthly domestic-currency returns on"
        " currency returns gives a"
        " slope near 0.6 (the currency's own effect less the -0.4 asset-currency link); a grid"
        " search on the hedged"
        " variance picks the same ratio",
        bool(abs(beta - best) < 0.01 and 0.45 < beta < 0.75),
        f"beta {beta:.3f}, grid {best:.3f}",
    )
    ndf_rate, fixing, notional_usd = 83.50, 85.00, 10_000_000
    settle_usd = notional_usd * (ndf_rate - fixing) / fixing
    report.ok(
        "non-deliverable forward: an investor sold USD 10m against INR at 83.50; at a fixing of"
        " 85.00 the contract settles"
        " net in dollars, a payment of USD 176,471 by the investor (no rupees change hands)",
        abs(settle_usd + 176_470.6) < 0.1,
    )


def check_active_strategies(report: CheckReport) -> None:
    """Part 5: a carry position and a volatility trade."""
    print("== part 5: active currency strategies")
    carry_pnl = (1 + 0.105) * (1 - 0.04) - (1 + 0.043)
    report.ok(
        "carry: funding in USD at 4.3% and investing in a 10.5% EM currency earns 1.78% even if the"
        " currency falls 4%; a"
        " 12% crash turns it into a loss of 7.06%",
        abs(carry_pnl - 0.0178) < 1e-4 and abs((1 + 0.105) * 0.88 - 1.043 + 0.0706) < 1e-4,
    )
    vega_pnl = 0.5 * (0.12**2 - 0.08**2) * 0.25 * 100
    report.ok(
        "volatility trading: a delta-hedged long option position earns roughly half gamma times the"
        " gap between realised"
        " and implied variance; realised 12% against 8% implied over three months is positive (here"
        " 0.1 per 100 of"
        " dollar-gamma); realised below implied loses",
        vega_pnl > 0 and 0.5 * (0.06**2 - 0.08**2) * 0.25 * 100 < 0,
    )


def main() -> int:
    """Print the versions, then run the five parts with one report.

    The worked numbers of meth:currency-portfolio-effects,
    meth:currency-hedging-programme, meth:active-currency-strategies and
    meth:currency-hedge-cost-reduction.

    Reproduced from Portfolio Management in Practice, Volume 1 (CFA Institute Investment Series,
    2020), chap. 8: the domestic-currency return (1 + 10%)(1 + 5%) - 1 = 15.5% and the INR portfolio
    return of 12.4% (eqs. 1-2, pp. 378-380); the variance approximation (eq. 5, p. 380). Campbell,
    Serfaty-de Medeiros and Viceira (NBER WP 13088, revised 2009): risk-minimising currency
    positions are close to a full hedge for bonds, while currencies that move against equities are
    worth holding unhedged in equity portfolios. Original: domestic-currency volatility of hedged
    and unhedged equity and bond holdings and their minimum-variance hedge ratios; adjusting a hedge
    ratio when the asset value changes, with the settlement of the maturing forward and the FX swap
    that rolls it; roll yield from forward points; protective puts, risk reversals, put spreads and
    seagulls priced with Garman-Kohlhagen; a cross hedge and its residual risk; a regression-based
    minimum-variance hedge on simulated data; non-deliverable forward settlement; a carry position
    and a volatility trade; and a hedging-cost budget.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_effects(report)
    check_hedge_ratios(report)
    check_options(report)
    check_cross_hedges(report, np.random.default_rng(SEED))
    check_active_strategies(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
