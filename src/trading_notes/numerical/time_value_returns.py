"""Batch 2 foundations (2026-10-18): worked examples of the return and present-value entries.

The worked examples of def:return-measures (holding-period, price and total returns; arithmetic and geometric
means), def:required-return-components, meth:instrument-present-value and res:cash-flow-additivity.

Each closed-form result is checked against an independent route: explicit cash-flow summation, a ledger of the
replicating trades, root finding by bisection, or the alternative formula. Annual compounding and end-of-year cash
flows throughout unless stated. Corrections of 2026-10-18: dated forward-lending cash flows, uncertain inflation, yield quotation.
Unit review of 2026-10-23: single amounts and quote conversion, dated streams and annuities, loan amortisation,
the internal rate of return and its pitfalls, and a forward on a dividend-paying share.
Correction pass of 2026-10-23: bisect() rejects invalid brackets and returns endpoint roots; a double-root IRR;
the annuity due at zero and negative rates; perpetuity timing; zero-rate loan limits; a negative IRR.
Inputs are invented; they illustrate the mechanics, not any security. Rates are decimals per period.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.time_value_returns (standard library).
"""

import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Final

from trading_notes.numerical.report import CheckReport


@dataclass(frozen=True)
class GrowingDividend:
    """The share valued by constant growth and then priced back to its implied return and growth.

    Attributes:
        d0: Dividend just paid.
        g: Constant growth rate of the dividend.
        r: Required return.
    """

    d0: float
    g: float
    r: float


# The 5% 3-year annual-coupon bond per 100 face, valued and then priced back to its yield.
COUPON_FLOWS: Final = (5, 5, 105)
SHARE: Final = GrowingDividend(d0=2.00, g=0.04, r=0.09)
# A conventional project at t = 0, 1, 2, 3: its IRR, the bisection contract and reinvestment.
CONVENTIONAL: Final = (-1000, 300, 400, 500)


def close(a: float, b: float, tol: float = 5e-5) -> bool:
    """Return whether a and b differ by at most tol."""
    return abs(a - b) <= tol


def bisect(f: Callable[[float], float], lo: float, hi: float, n: int = 200) -> float:
    """Root of f in [lo, hi]; the ends must have opposite signs unless one is a root.

    An end, or a midpoint, where f is exactly zero is returned as it is; otherwise the
    midpoint of the bracket left after n halvings.

    Raises:
        ValueError: If lo >= hi, or if f has the same nonzero sign at both ends.
    """
    if not lo < hi:
        raise ValueError("bracket needs lo < hi")
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if (flo > 0) == (fhi > 0):
        raise ValueError("ends of the bracket have the same sign")
    for _ in range(n):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if fmid == 0:
            return mid
        if (fmid > 0) == (flo > 0):
            lo, flo = mid, fmid
        else:
            hi = mid
    return (lo + hi) / 2


def rejects(f: Callable[[float], float], lo: float, hi: float) -> bool:
    """Return whether bisect refuses the bracket [lo, hi] with ValueError."""
    try:
        bisect(f, lo, hi)
    except ValueError:
        return True
    return False


def check_holding_period_returns(report: CheckReport) -> None:
    """Split a share's one-period total return into price and income returns, and net a fee."""
    print("== holding-period, price and total return of a share")
    p0, p1, div = 50.00, 54.00, 1.20
    price_ret = p1 / p0 - 1
    income_ret = div / p0
    total_ret = (p1 + div) / p0 - 1
    report.ok("price return 8.0%", close(price_ret, 0.08))
    report.ok("income return 2.4%", close(income_ret, 0.024))
    report.ok(
        "total = price + income return (one period, income at the end)",
        close(total_ret, price_ret + income_ret) and close(total_ret, 0.104),
    )

    gross_end, fee = 1000 * 1.08, 0.01 * 1000
    report.ok("net of a 1% fee on opening assets: 7.0%", close((gross_end - fee) / 1000 - 1, 0.07))


def check_return_indices(report: CheckReport) -> None:
    """Compare a total-return index with a holding that reinvests its dividend."""
    print("== price index against total-return index, dividend reinvested at the ex-date close")
    # Two periods of one share: prices 100 -> 102 (ex-dividend 2 paid in period 1) -> 105.
    prices, divs = [100.0, 102.0, 105.0], [0.0, 2.0, 0.0]
    pr_index, tr_index = [100.0], [100.0]
    for t in (1, 2):
        pr_index.append(pr_index[-1] * prices[t] / prices[t - 1])
        tr_index.append(tr_index[-1] * (prices[t] + divs[t]) / prices[t - 1])
    # Independent route: hold one share, reinvest the dividend in shares at 102.
    shares = 1 + divs[1] / prices[1]
    ledger_value = shares * prices[2]
    report.ok("price index 105.00", close(pr_index[-1], 105.0))
    report.ok(
        "total-return index equals the reinvested holding",
        close(tr_index[-1], ledger_value),
        f"{tr_index[-1]:.4f}",
    )
    report.ok("total return 7.0588%", close(tr_index[-1] / 100 - 1, 0.070588))


def check_means(report: CheckReport) -> None:
    """Compare the arithmetic and geometric means of three returns."""
    print("== arithmetic against geometric mean")
    rets = [0.20, -0.10, 0.05]
    arith = sum(rets) / len(rets)
    growth = math.prod(1 + r for r in rets)
    geo = growth ** (1 / len(rets)) - 1
    report.ok("arithmetic mean 5.0000%", close(arith, 0.05))
    report.ok("geometric mean 4.2808%", close(geo, 0.042808, 2e-6), f"{geo:.6f}")
    report.ok(
        "geometric compounds to the realised wealth",
        close((1 + geo) ** 3, growth) and close(growth, 1.134),
    )
    report.ok("geometric below arithmetic for unequal returns", geo < arith)
    var = sum((r - arith) ** 2 for r in rets) / len(rets)
    report.ok(
        "approximation geo ~ arith - var/2 (population variance) gives 4.25%",
        close(arith - var / 2, 0.0425, 1e-12),
        f"{arith - var / 2:.6f}",
    )
    report.ok("equal returns: the means coincide", close((1.05**3) ** (1 / 3) - 1, 0.05, 1e-12))


def check_required_return_components(report: CheckReport) -> None:
    """Check the Fisher relation, uncertain inflation and additive premia."""
    print("== required-return components (Fisher exact and approximate; additive premia)")
    real, infl = 0.015, 0.025
    nominal = (1 + real) * (1 + infl) - 1
    report.ok("exact Fisher nominal 4.0375%", close(nominal, 0.040375))
    report.ok(
        "additive approximation error = real * inflation",
        close(nominal - (real + infl), real * infl, 1e-12),
    )
    report.ok(
        "real from nominal: (1.08/1.03) - 1 = 4.8544% (the existing entry)",
        close(1.08 / 1.03 - 1, 0.048544),
    )
    report.ok(
        "high inflation: 10% nominal, 20% inflation -> exact real -8.3333%, approximation -10%",
        close(1.10 / 1.20 - 1, -0.083333, 1e-6) and close(0.10 - 0.20, -0.10, 1e-12),
    )
    report.ok(
        "uncertain inflation: deflating by mean inflation gives 0%, mean realised real return 0.8333%",
        close(1.10 / (1 + (0.0 + 0.20) / 2) - 1, 0.0, 1e-12)
        and close(sum(1.10 / (1 + h) - 1 for h in (0.0, 0.20)) / 2, 0.0083333, 1e-6),
    )
    report.ok(
        "realised real return is convex in inflation (Jensen): mean exceeds value at the mean",
        sum(1.10 / (1 + h) - 1 for h in (0.0, 0.20)) / 2 > 1.10 / 1.10 - 1,
    )
    report.ok(
        "continuously compounded rates add exactly",
        close(math.log(1 + nominal), math.log(1 + real) + math.log(1 + infl), 1e-12),
    )
    irp, credit, liquidity, erp = 0.003, 0.012, 0.003, 0.050
    nominal_rf_yield = nominal + irp
    report.ok(
        "nominal risk-free yield with inflation risk premium 4.3375%",
        close(nominal_rf_yield, 0.043375),
    )
    report.ok(
        "corporate bond required yield 5.8375%",
        close(nominal_rf_yield + credit + liquidity, 0.058375),
    )
    report.ok("equity required return 9.3375%", close(nominal_rf_yield + erp, 0.093375))


def check_present_values(report: CheckReport) -> None:
    """Value a zero, the coupon bond, a preferred share and the growing-dividend share."""
    print(
        "== present values: zero, coupon bond (single yield and spot rates), preferred, constant and two-stage growth"
    )
    zero = 1000 / 1.04**3
    report.ok("zero-coupon 888.9964", close(zero, 888.996359, 1e-4), f"{zero:.6f}")
    cf = COUPON_FLOWS
    price_y = sum(c / 1.04**t for t, c in enumerate(cf, 1))
    annuity = 5 * (1 - 1.04**-3) / 0.04 + 100 / 1.04**3
    report.ok(
        "coupon bond at 4% = 102.7751 by summation and annuity formula",
        close(price_y, annuity, 1e-9) and close(price_y, 102.775091, 1e-4),
        f"{price_y:.6f}",
    )
    spots = [0.030, 0.038, 0.041]
    price_s = sum(c / (1 + z) ** t for (t, c), z in zip(enumerate(cf, 1), spots))
    report.ok(
        "coupon bond at spot rates 102.5709", close(price_s, 102.570853, 1e-5), f"{price_s:.6f}"
    )
    ytm_s = bisect(lambda y: sum(c / (1 + y) ** t for t, c in enumerate(cf, 1)) - price_s, 0.0, 0.2)
    report.ok(
        "its yield 4.0723% lies between the spot rates and nearest the 3-year rate",
        close(ytm_s, 0.040723, 2e-6) and spots[0] < ytm_s < spots[2],
        f"{ytm_s:.6f}",
    )
    pref = 6 / 0.075
    pref_sum = sum(6 / 1.075**t for t in range(1, 3001))
    report.ok(
        "preferred perpetuity 80.00 (truncated sum agrees)",
        close(pref, 80.0) and close(pref_sum, 80.0, 1e-6),
    )
    d0, g, r = SHARE.d0, SHARE.g, SHARE.r
    d1 = d0 * (1 + g)
    gordon = d1 / (r - g)
    gordon_sum = sum(d0 * (1 + g) ** t / (1 + r) ** t for t in range(1, 3001))
    report.ok(
        "constant growth 41.60 (truncated sum agrees)",
        close(gordon, 41.60) and close(gordon_sum, 41.60, 1e-4),
    )
    # Two stage: 10% growth for years 1-2, 4% thereafter, r = 9%.
    d_1, d_2 = d0 * 1.10, d0 * 1.10**2
    terminal = d_2 * 1.04 / (0.09 - 0.04)  # value at year 2 of dividends from year 3
    two_stage = d_1 / 1.09 + (d_2 + terminal) / 1.09**2
    two_sum = (
        d_1 / 1.09 + d_2 / 1.09**2 + sum(d_2 * 1.04**k / 1.09 ** (2 + k) for k in range(1, 4000))
    )
    report.ok(
        "two-stage 46.4220 (truncated sum agrees)",
        close(two_stage, 46.422018, 1e-5) and close(two_sum, two_stage, 1e-4),
        f"{two_stage:.6f}",
    )
    report.ok("terminal value 50.3360 at year 2", close(terminal, 50.336, 1e-6))


def check_semiannual_yields(report: CheckReport) -> None:
    """Value semiannual flows at an effective annual rate and at its bond-equivalent quote."""
    print("== semiannual cash flows: effective against nominal (bond-equivalent) annual yields")
    half_eff = 1.10**0.5 - 1
    pv_eff = 5 / (1 + half_eff) + 105 / (1 + half_eff) ** 2
    y_nom = 2 * half_eff
    pv_nom = 5 / (1 + y_nom / 2) + 105 / (1 + y_nom / 2) ** 2
    report.ok(
        "10% effective annual: half-year rate 4.8809%, value 100.2218584",
        close(half_eff, 0.048809, 1e-6) and close(pv_eff, 100.2218584, 1e-7),
    )
    report.ok(
        "equivalent nominal 9.7618% compounded semiannually gives the same value",
        close(y_nom, 0.097618, 1e-6) and close(pv_nom, pv_eff, 1e-10),
    )
    report.ok(
        "halving the effective rate misprices: 100.00",
        close(5 / 1.05 + 105 / 1.05**2, 100.0, 1e-10),
    )


def check_implied_returns(report: CheckReport) -> None:
    """Price the coupon bond and the growing-dividend share back to their yield and growth."""
    print("== implied returns and growth")
    cf = COUPON_FLOWS
    d0, g = SHARE.d0, SHARE.g
    d1 = d0 * (1 + g)
    ytm = bisect(lambda y: sum(c / (1 + y) ** t for t, c in enumerate(cf, 1)) - 98.00, 0.0, 0.2)
    report.ok(
        "yield of the 5% 3-year bond priced 98.00 is 5.7447%",
        close(ytm, 0.057447, 2e-6),
        f"{ytm:.6f}",
    )
    report.ok(
        "repricing at that yield returns 98.00",
        close(sum(c / (1 + ytm) ** t for t, c in enumerate(cf, 1)), 98.00, 1e-8),
    )
    report.ok("implied required return D1/P0 + g = 9%", close(d1 / 41.60 + g, 0.09))
    g_impl = (0.09 * 52 - d0) / (52 + d0)
    report.ok("implied growth at price 52: 4.9630%", close(g_impl, 0.049630, 2e-6), f"{g_impl:.6f}")
    report.ok(
        "Gordon value at the implied growth returns 52",
        close(d0 * (1 + g_impl) / (0.09 - g_impl), 52.0, 1e-9),
    )
    g_bis = bisect(lambda gg: d0 * (1 + gg) / (0.09 - gg) - 52, 0.0, 0.0899)
    report.ok("bisection agrees with the closed form", close(g_bis, g_impl, 1e-9))


def check_forward_rate(report: CheckReport) -> None:
    """Build the one-year forward rate from the dated flows of the replicating trades."""
    print("== cash-flow additivity: forward rate, forward FX, option by replication and parity")
    z1, z2 = 0.030, 0.038
    f12 = (1 + z2) ** 2 / (1 + z1) - 1
    report.ok("1-year rate one year forward 4.6062%", close(f12, 0.046062, 2e-6), f"{f12:.6f}")
    # Ledger: buy a 2-year zero paying 1,000; finance it by a 1-year borrowing; at year 1 refinance at the forward.
    cost = 1000 / (1 + z2) ** 2
    repay_y1 = cost * (1 + z1)
    report.ok("two-year zero paying 1,000 costs 928.1225", close(cost, 928.122482, 1e-5))
    # Correction of 2026-10-18: check the dated cash flows of the trades themselves; no future rate assumed.
    # Buy the 2-year zero, borrow its cost for 1 year: flows (t0, t1, t2) = (0, -repay, +1000).
    flows_lend = (-cost + cost, -repay_y1, 1000.0)
    report.ok(
        "forward lending: flows 0, -955.9662, +1000",
        close(flows_lend[0], 0, 1e-12)
        and close(flows_lend[1], -955.966157, 1e-5)
        and flows_lend[2] == 1000.0,
    )
    report.ok(
        "rate earned from year 1 to year 2 equals the implied forward",
        close(flows_lend[2] / -flows_lend[1] - 1, f12, 1e-12),
    )
    # Reverse: short the 2-year zero, lend the proceeds for 1 year: (0, +955.9662, -1000), forward borrowing.
    flows_borrow = tuple(-x for x in flows_lend)
    report.ok(
        "forward borrowing: flows 0, +955.9662, -1000",
        close(flows_borrow[1], 955.966157, 1e-5) and flows_borrow[2] == -1000.0,
    )
    # Rolling the year-1 debt into a new loan at an unknown future rate is not a lock-in: at 8% it costs 1,032.4434.
    report.ok(
        "refinancing at a later 8% spot costs 1,032.4434, not 1,000",
        close(repay_y1 * 1.08, 1032.443449, 1e-5),
    )
    f12_c = (2 * math.log(1 + z2) - math.log(1 + z1)) / 1
    report.ok(
        "continuous version (Hull eq. 4.5) agrees after conversion",
        close(math.exp(f12_c) - 1, f12, 1e-12),
    )


def check_forward_fx(report: CheckReport) -> None:
    """Check covered interest parity by its ledger (continues the cash-flow additivity section)."""
    spot, i_usd, i_eur = 1.1000, 0.040, 0.025  # USD per EUR; one year, annual compounding
    fwd = spot * (1 + i_usd) / (1 + i_eur)
    report.ok("forward 1.116098 USD per EUR", close(fwd, 1.116098, 1e-6), f"{fwd:.6f}")
    # Ledger: borrow USD 1,100, buy EUR 1,000, deposit at 2.5%, sell EUR 1,025 forward; repay USD 1,144.
    report.ok(
        "covered position nets zero at the forward",
        close(1000 * (1 + i_eur) * fwd - 1100 * (1 + i_usd), 0.0, 1e-9),
    )
    report.ok("forward points +160.98 (pips of 0.0001)", close((fwd - spot) * 1e4, 160.98, 0.01))


def check_option_replication(report: CheckReport) -> None:
    """Value a one-period call and put by replication, risk-neutrally and by parity.

    Continues the cash-flow additivity section.
    """
    s0, su, sd, k, rf = 50.0, 60.0, 40.0, 50.0, 0.05  # one period; rf simple for the period
    cu, cd = max(su - k, 0), max(sd - k, 0)
    delta = (cu - cd) / (su - sd)
    bond_pv = (cd - delta * sd) / (1 + rf)
    call = delta * s0 + bond_pv
    report.ok(
        "call replication: 0.5 share and borrowing 19.0476 -> 5.9524",
        close(delta, 0.5) and close(bond_pv, -19.047619, 1e-6) and close(call, 5.952381, 1e-6),
    )
    report.ok(
        "replicating portfolio pays the call in both states",
        close(delta * su + bond_pv * (1 + rf), cu, 1e-12)
        and close(delta * sd + bond_pv * (1 + rf), cd, 1e-12),
    )
    q = ((1 + rf) * s0 - sd) / (su - sd)
    report.ok(
        "risk-neutral expectation gives the same value",
        close((q * cu + (1 - q) * cd) / (1 + rf), call, 1e-12),
    )
    pu, pd = max(k - su, 0), max(k - sd, 0)
    put_rep = (pu - pd) / (su - sd) * s0 + (pd - (pu - pd) / (su - sd) * sd) / (1 + rf)
    put_parity = call + k / (1 + rf) - s0
    report.ok(
        "put by replication equals put by parity 3.5714",
        close(put_rep, put_parity, 1e-12) and close(put_parity, 3.571429, 1e-6),
    )
    report.ok(
        "parity holds state by state: call - put = share - K",
        all(close(max(s - k, 0) - max(k - s, 0), s - k, 1e-12) for s in (su, sd, 47.3)),
    )


# Unit review 2026-10-23: def:time-value-compounding, meth:cash-flow-streams, meth:loan-amortisation,
# meth:internal-rate-of-return and the share forward in res:cash-flow-additivity.


def npv(rate: float, flows: Sequence[float]) -> float:
    """Return the value at t = 0 of flows[t] paid at t = 0, 1, 2, ..., discounted at rate per period."""
    return sum(c / (1 + rate) ** t for t, c in enumerate(flows))


def check_single_amounts(report: CheckReport) -> None:
    """Compound and discount single amounts and convert between rate quotations."""
    print("== single amounts, compounding and quote conversion")
    report.ok(
        "1,000 at 5% for 3 years: compound 1,157.625, simple 1,150, interest on interest 7.625",
        close(1000 * 1.05**3, 1157.625, 1e-9)
        and close(1000 * 1.05**3 - 1000 * (1 + 0.05 * 3), 7.625, 1e-9),
    )
    year_by_year = 1000.0
    for _ in range(3):
        year_by_year += year_by_year * 0.05
    report.ok(
        "year-by-year crediting gives the same 1,157.625", close(year_by_year, 1157.625, 1e-9)
    )
    report.ok("PV of 1,000 in 3 years at 5% is 863.8376", close(1000 / 1.05**3, 863.837599, 1e-6))
    report.ok("zero rate: PV equals FV", 1000 / 1.0**3 == 1000)
    report.ok(
        "growth 1,000 -> 1,500 in 6 years is 6.9913%", close(1.5 ** (1 / 6) - 1, 0.069913, 1e-6)
    )
    n_double = math.log(2) / math.log(1.06)
    report.ok(
        "doubling at 6%: 11.8957 years; rule of 72 gives 12",
        close(n_double, 11.895661, 1e-6) and close(1.06**n_double, 2.0, 1e-12),
    )
    report.ok(
        "rule of 72 poorer at 36%: exact 2.2542 years",
        close(math.log(2) / math.log(1.36), 2.254249, 1e-6),
    )
    growth = 1.01**12
    report.ok("nominal 12% monthly: EAR 12.6825%", close(growth - 1, 0.126825, 1e-6))
    r_semi, r_q, r_c = 2 * (1.01**6 - 1), 4 * (1.01**3 - 1), 12 * math.log(1.01)
    report.ok(
        "equivalents 12.3040% semiannual, 12.1204% quarterly, 11.9404% continuous",
        close(r_semi, 0.123040, 1e-6) and close(r_q, 0.121204, 1e-6) and close(r_c, 0.119404, 1e-6),
    )
    report.ok(
        "each equivalent grows 100 to 112.6825 in a year",
        all(
            close(100 * x, 112.682503, 1e-5)
            for x in ((1 + r_semi / 2) ** 2, (1 + r_q / 4) ** 4, math.exp(r_c))
        ),
    )
    report.ok(
        "OpenStax credit card: 1.5% a month is 19.562% effective",
        close(1.015**12 - 1, 0.19562, 1e-5),
    )
    mm = 1 + 0.05 * 90 / 360
    report.ok(
        "90-day 5% simple act/360: growth 1.0125, EAR 5.1671%, continuous 5.0380%",
        close(mm, 1.0125, 1e-12)
        and close(mm ** (365 / 90) - 1, 0.051671, 1e-6)
        and close(math.log(mm) * 365 / 90, 0.050380, 1e-6),
    )
    r_s = (1.05 ** (90 / 365) - 1) * 360 / 90
    report.ok(
        "EAR 5% as a 90-day act/360 simple rate: 4.8412%, and back",
        close(r_s, 0.048412, 1e-6) and close((1 + r_s * 90 / 360) ** (365 / 90), 1.05, 1e-12),
    )


def check_streams(report: CheckReport) -> None:
    """Value dated streams, annuities and perpetuities, including timing and r <= 0 cases."""
    print("== dated streams, annuities and perpetuities")
    report.ok(
        "mixed stream 300, 500, 700 at years 1, 2, 4 and 6%: 1,282.4827",
        close(npv(0.06, [0, 300, 500, 0, 700]), 1282.482652, 1e-5),
    )
    a5 = 1000 * (1 - 1.06**-5) / 0.06
    report.ok(
        "ordinary annuity 4,212.3638 by formula and by summing",
        close(a5, 4212.363786, 1e-5) and close(a5, sum(1000 / 1.06**t for t in range(1, 6)), 1e-9),
    )
    report.ok(
        "annuity due 4,465.1056 (first payment now) by formula and by summing",
        close(a5 * 1.06, 4465.105613, 1e-5)
        and close(a5 * 1.06, sum(1000 / 1.06**t for t in range(5)), 1e-9),
    )
    report.ok(
        "future value 5,637.0930 by formula, by compounding each payment and as (1+r)^N PV",
        close(1000 * (1.06**5 - 1) / 0.06, 5637.09296, 1e-5)
        and close(sum(1000 * 1.06 ** (5 - t) for t in range(1, 6)), 5637.09296, 1e-5)
        and close(a5 * 1.06**5, 5637.09296, 1e-5),
    )
    # Each rate with the expected ordering of the annuity due (d) against the ordinary annuity (o).
    due_against_ordinary: tuple[tuple[float, Callable[[float, float], bool]], ...] = (
        (0.06, lambda d, o: d > o),
        (0.0, lambda d, o: d == o == 5000),
        (
            -0.02,
            lambda d, o: d < o and close(d, 5208.289237, 1e-5) and close(o, 5314.580854, 1e-5),
        ),
    )
    report.ok(
        "annuity due: larger at 6%, equal at 0% (5,000), smaller at -2% (5,208.2892 < 5,314.5809), by summing",
        all(
            cmp(
                sum(1000 / (1 + x) ** t for t in range(5)),
                sum(1000 / (1 + x) ** t for t in range(1, 6)),
            )
            for x, cmp in due_against_ordinary
        ),
    )
    report.ok(
        "C/r is a perpetuity paid from t = 1; paid from t = 0 it is worth C + C/r",
        close(sum(1000 / 1.06**t for t in range(1, 3001)), 1000 / 0.06, 1e-6)
        and close(sum(1000 / 1.06**t for t in range(3001)), 1000 + 1000 / 0.06, 1e-6),
    )
    report.ok(
        "r <= 0: partial sums of a level perpetuity do not converge (N C at r = 0)",
        sum(1000 / 1.0**t for t in range(1, 1001)) == 1000 * 1000
        and sum(1000 / 0.99**t for t in range(1, 201))
        > sum(1000 / 0.99**t for t in range(1, 101)) * 2,
    )
    report.ok(
        "annuity = perpetuity paid from year 1 less perpetuity paid from year 6",
        close(1000 / 0.06 - 1000 / 0.06 / 1.06**5, a5, 1e-9),
    )
    report.ok(
        "zero-rate limit: annuity factor tends to N",
        close((1 - 1.000001**-5) / 0.000001, 5, 1e-4),
    )
    report.ok(
        "growing perpetuity 100 at 8% growing 3%: 2,000; after a payment of 100 just made: 2,060",
        close(100 / 0.05, 2000, 1e-12) and close(100 * 1.03 / 0.05, 2060, 1e-9),
    )
    report.ok(
        "growing perpetuity truncated sum agrees",
        close(sum(100 * 1.03 ** (t - 1) / 1.08**t for t in range(1, 3001)), 2000, 1e-6),
    )
    ga = 100 / 0.05 * (1 - (1.03 / 1.08) ** 10)
    report.ok(
        "growing annuity, 10 payments: 755.0134 by formula and by summing",
        close(ga, 755.013369, 1e-5)
        and close(ga, sum(100 * 1.03 ** (t - 1) / 1.08**t for t in range(1, 11)), 1e-9),
    )
    report.ok(
        "g = r boundary: N C1/(1+r) = 925.9259, and the r != g formula tends to it",
        close(sum(100 * 1.08 ** (t - 1) / 1.08**t for t in range(1, 11)), 925.925926, 1e-5)
        and close(100 / (0.08 - 0.0799999) * (1 - (1.0799999 / 1.08) ** 10), 925.925926, 1e-3),
    )
    report.ok(
        "monthly: 200 a month, 36 months, 0.75%: 6,289.3611",
        close(200 * (1 - 1.0075**-36) / 0.0075, 6289.361050, 1e-5),
    )
    m_eff = 1.06 ** (1 / 12) - 1
    report.ok(
        "6% effective: monthly rate 0.48676%; 12 x 100 worth 1,162.88, not 1,161.89 at 0.5%",
        close(m_eff, 0.0048676, 1e-7)
        and close(100 * (1 - (1 + m_eff) ** -12) / m_eff, 1162.88, 0.005)
        and close(100 * (1 - 1.005**-12) / 0.005, 1161.89, 0.005),
    )
    report.ok(
        "OpenStax 8.2: year-3 PV of 25,000 at 8% is 19,845.81; five payments 99,817.75",
        close(25000 / 1.08**3, 19845.81, 0.005)
        and close(sum(25000 / 1.08**t for t in range(1, 6)), 99817.75, 0.005),
    )


def check_loan_amortisation(report: CheckReport) -> None:
    """Amortise level-payment loans row by row and check the balances and limits."""
    print("== loan amortisation")
    pay = 10000 * 0.08 / (1 - 1.08**-4)
    report.ok("payment on 10,000, 4 years, 8%: 3,019.2080", close(pay, 3019.208045, 1e-5))
    bal = 10000.0
    schedule: list[tuple[float, float, float]] = []  # (interest, principal, closing balance)
    for k in range(1, 5):
        interest = 0.08 * bal
        principal = pay - interest
        bal -= principal
        schedule.append((interest, principal, bal))
    report.ok(
        "schedule rows as printed",
        all(
            close(x, y, 5e-5)
            for row, want in zip(
                schedule,
                [
                    (800.0, 2219.2080, 7780.7920),
                    (622.4634, 2396.7447, 5384.0473),
                    (430.7238, 2588.4843, 2795.5630),
                    (223.6450, 2795.5630, 0.0),
                ],
            )
            for x, y in zip(row, want)
        ),
    )
    report.ok(
        "balance = PV of remaining payments = retrospective balance, every year",
        all(
            close(b, pay * (1 - 1.08 ** -(4 - k)) / 0.08, 1e-8)
            and close(b, 10000 * 1.08**k - pay * (1.08**k - 1) / 0.08, 1e-8)
            for k, (_, _, b) in enumerate(schedule, 1)
        ),
    )
    report.ok(
        "principal parts grow by 1.08; total interest 2,076.8322",
        all(close(schedule[k + 1][1], 1.08 * schedule[k][1], 1e-9) for k in range(3))
        and close(sum(row[0] for row in schedule), 2076.832178, 1e-5)
        and close(4 * pay - 10000, 2076.832178, 1e-5),
    )
    bal0 = 10000.0
    rows0: list[float] = []
    for k in range(1, 5):
        interest0 = 0.0 * bal0  # schedule recursion with r = 0
        bal0 -= 2500.0 - interest0
        rows0.append(bal0)
    report.ok(
        "zero rate: payment L/N = 2,500, balances 7,500, 5,000, 2,500, 0 = L(1 - k/N)",
        rows0 == [10000 * (1 - k / 4) for k in range(1, 5)] == [7500.0, 5000.0, 2500.0, 0.0],
    )
    eps = 1e-7
    pay_eps = 10000 * eps / (1 - (1 + eps) ** -4)
    report.ok(
        "the r -> 0 limits of A and B_k are L/N and L(1 - k/N)",
        close(pay_eps, 2500.0, 1e-2)
        and all(
            close(pay_eps * (1 - (1 + eps) ** -(4 - k)) / eps, 10000 * (1 - k / 4), 1e-2)
            for k in range(1, 4)
        ),
    )
    report.ok(
        "lender's IRR equals the loan rate",
        close(bisect(lambda x: npv(x, [-10000] + [pay] * 4), 0.0, 1.0), 0.08, 1e-9),
    )
    af = (1 - 1.005**-36) / 0.005
    car = 32000 / af
    bal = 32000.0
    total_int = 0.0
    for _ in range(36):
        total_int += 0.005 * bal
        bal -= car - 0.005 * bal
    report.ok(
        "OpenStax auto loan: factor 32.8710, payment 973.5020, interest 3,046.07, month 1 split 160.00/813.50",
        close(af, 32.871016, 1e-6)
        and close(car, 973.501998, 1e-6)
        and close(total_int, 3046.07, 0.005)
        and close(bal, 0.0, 1e-6)
        and close(973.50 - 160.00, 813.50, 1e-9),
    )
    report.ok("6% compounded monthly is 6.1678% effective", close(1.005**12 - 1, 0.061678, 1e-6))


def check_conventional_irr(report: CheckReport) -> float:
    """Find the conventional project's IRR by bisection and by Newton's method.

    Returns:
        The IRR found by bisection, as a decimal rate.
    """
    print("== internal rate of return")
    conv = CONVENTIONAL
    irr = bisect(lambda x: npv(x, conv), 0.0, 1.0)
    report.ok(
        "NPV at 6% 58.8271; IRR 8.8963% by bisection",
        close(npv(0.06, conv), 58.827085, 1e-5) and close(irr, 0.088963, 1e-6),
    )
    x = 0.0
    steps: list[float] = []
    for _ in range(3):
        x -= npv(x, conv) / sum(-t * c / (1 + x) ** (t + 1) for t, c in enumerate(conv))
        steps.append(x)
    report.ok(
        "Newton from 0: 7.6923, 8.8737, 8.8963 percent",
        all(close(s, w, 1e-6) for s, w in zip(steps, (0.076923, 0.088737, 0.088963))),
    )
    return irr


def check_irr_pitfalls(report: CheckReport) -> None:
    """Check streams with two IRRs, no IRR, a borrowing IRR and crossing NPV profiles."""
    fac = [-350, 950, -620]
    disc = 950**2 - 4 * 350 * 620
    roots = sorted(1 / ((950 + s * math.sqrt(disc)) / 1240) - 1 for s in (1, -1))
    report.ok(
        "facility: two IRRs 9.1797% and 62.2488%, NPV zero at both",
        close(roots[0], 0.091797, 1e-6)
        and close(roots[1], 0.622488, 1e-6)
        and all(close(npv(r, fac), 0, 1e-9) for r in roots),
    )
    report.ok(
        "facility NPV -20 at 0%, +13.9053 at 30%, -30 at 100%",
        close(npv(0, fac), -20, 1e-9)
        and close(npv(0.3, fac), 13.905325, 1e-6)
        and close(npv(1.0, fac), -30, 1e-9),
    )
    report.ok(
        "no IRR: +100, -250, +200 has negative discriminant; minimum NPV 21.875 at 60%",
        250**2 - 4 * 100 * 200 < 0
        and close(npv(0.6, [100, -250, 200]), 21.875, 1e-9)
        and min(npv(k / 1000, [100, -250, 200]) for k in range(-900, 20000)) > 21.87,
    )
    report.ok(
        "borrowing +1,000, -1,100: IRR 10%, NPV at 8% -18.52",
        close(bisect(lambda x: npv(x, [1000, -1100]), 0.0, 1.0), 0.10, 1e-9)
        and close(npv(0.08, [1000, -1100]), -18.52, 0.005),
    )
    reg = [-16000, 2000, 4000, 5000, 5000, 5000, 5000]
    heavy = [-25000, 2000, 4000, 8000, 9000, 9000, 9000]
    cross = bisect(lambda x: npv(x, [h - g for h, g in zip(heavy, reg)]), 0.0, 1.0)
    report.ok(
        "OpenStax machines: IRRs 14.0855% and 13.2040%, NPVs at 9% 2,835.62 and 3,970.67, crossover 11.9265%",
        close(bisect(lambda x: npv(x, reg), 0, 1), 0.140855, 1e-6)
        and close(bisect(lambda x: npv(x, heavy), 0, 1), 0.132040, 1e-6)
        and close(npv(0.09, reg), 2835.62, 0.005)
        and close(npv(0.09, heavy), 3970.67, 0.005)
        and close(cross, 0.119265, 1e-6)
        and close(npv(cross, reg), npv(cross, heavy), 1e-6),
    )


def check_double_root_irr(report: CheckReport) -> None:
    """Check a stream whose NPV touches zero at 10% without changing sign."""
    dbl = [-100, 220, -121]
    report.ok(
        "double root: -100, 220, -121 has NPV -(11/(1+r) - 10)^2, never positive; -1 at 0%, -0.6944 at 20%",
        all(
            close(npv(k / 100, dbl), -((11 / (1 + k / 100) - 10) ** 2), 1e-9)
            for k in range(-50, 301)
        )
        and max(npv(k / 1000, dbl) for k in range(-500, 3001)) <= 1e-12
        and close(npv(0, dbl), -1, 1e-12)
        and close(npv(0.2, dbl), -0.694444, 1e-6),
    )
    report.ok(
        "double root: 10% is the sole distinct IRR (root 10/11 of -(11x - 10)^2, counted twice)",
        121 * (10 / 11) ** 2 - 220 * (10 / 11) + 100 < 1e-12 and 220**2 - 4 * 121 * 100 == 0,
    )
    report.ok(
        "double root: no grid bracket has opposite signs, and bisection refuses [0, 0.2]",
        not any(npv(k / 1000, dbl) * npv((k + 1) / 1000, dbl) < 0 for k in range(-500, 3000))
        and rejects(lambda x: npv(x, dbl), 0.0, 0.2),
    )
    x = 0.0
    for _ in range(60):
        d = sum(-t * c / (1 + x) ** (t + 1) for t, c in enumerate(dbl))
        if d == 0:
            break
        x -= npv(x, dbl) / d
    report.ok(
        "double root: Newton's iterate passes the domain and residual test (|NPV| <= 1e-9 sum|CF|)",
        x > -1 and abs(npv(x, dbl)) <= 1e-9 * sum(abs(c) for c in dbl) and close(x, 0.10, 1e-6),
        f"{x:.9f}",
    )
    report.ok(
        "double root: IRR 10% exceeds an 8% hurdle, yet NPV at 8% is -0.0343",
        close(npv(0.08, dbl), -0.034294, 1e-6),
    )


def check_negative_irr(report: CheckReport) -> None:
    """Check a conventional stream whose flows sum to less than zero."""
    neg = [-100, 50, 40]
    irr_neg = bisect(lambda x: npv(x, neg), -0.5, 0.0)
    report.ok(
        "conventional stream with negative sum: one IRR, negative (-6.9926%); NPV positive below, negative above",
        close(irr_neg, -0.069926, 1e-6)
        and npv(irr_neg - 0.05, neg) > 0
        and npv(irr_neg + 0.05, neg) < 0
        and close(npv(0, neg), -10, 1e-12),
        f"{irr_neg:.6f}",
    )


def check_bisect_contract(report: CheckReport) -> None:
    """Check that bisect rejects invalid brackets and returns endpoint roots exactly."""
    conv = CONVENTIONAL
    report.ok(
        "bisect rejects lo >= hi and same-sign ends",
        rejects(lambda x: npv(x, conv), 0.5, 0.1)
        and rejects(lambda x: npv(x, conv), 0.1, 0.1)
        and rejects(lambda x: npv(x, conv), 0.0, 0.05),
    )
    report.ok(
        "bisect returns an endpoint root exactly: -100, 125 at 25%",
        bisect(lambda x: npv(x, [-100, 125]), 0.25, 1.0) == 0.25
        and bisect(lambda x: npv(x, [-100, 125]), 0.0, 0.25) == 0.25,
    )


def check_irr_reinvestment(report: CheckReport, irr: float) -> None:
    """Check that the conventional project's inflows reinvested at irr grow the outlay at irr."""
    conv = CONVENTIONAL
    report.ok(
        "reinvesting the interim inflows at the IRR grows the outlay at the IRR",
        close(
            sum(c * (1 + irr) ** (3 - t) for t, c in enumerate(conv) if t),
            1000 * (1 + irr) ** 3,
            1e-6,
        ),
    )


def check_share_forward(report: CheckReport) -> None:
    """Price a forward on a share paying one dividend, by formula and by its two-loan ledger."""
    print("== forward on a dividend-paying share (discrete compounding)")
    s_0, dvd, rate = 50.0, 1.00, 0.04
    pv_div = dvd / (1 + rate) ** 0.5
    fwd_share = (s_0 - pv_div) * (1 + rate)
    report.ok(
        "PV of dividend 0.9806, forward 50.9802, equal to S(1+r) - D(1+r)^0.5",
        close(pv_div, 0.980581, 1e-6)
        and close(fwd_share, 50.980196, 1e-6)
        and close(fwd_share, s_0 * 1.04 - dvd * 1.04**0.5, 1e-12),
    )
    # Ledger: two loans, 0.9806 for six months and 49.0194 for a year, buy the share, sell forward.
    short_loan, long_loan = pv_div, s_0 - pv_div
    report.ok(
        "the dividend repays the six-month loan exactly", close(short_loan * 1.04**0.5, dvd, 1e-12)
    )
    report.ok(
        "forward proceeds repay the one-year loan exactly",
        close(long_loan * 1.04, fwd_share, 1e-12),
    )
    report.ok(
        "arbitrage at 51.50 earns 0.5198; reverse at 50.50 earns 0.4802",
        close(51.50 - long_loan * 1.04, 0.519804, 1e-6)
        and close(long_loan * 1.04 - 50.50, 0.480196, 1e-6),
    )
    r_cont = math.log(1.04)
    report.ok(
        "Hull's (S - I)e^{rT} with the continuous equivalent gives the same forward",
        close((s_0 - dvd * math.exp(-r_cont * 0.5)) * math.exp(r_cont), fwd_share, 1e-12),
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1)."""
    report = CheckReport()
    check_holding_period_returns(report)
    check_return_indices(report)
    check_means(report)
    check_required_return_components(report)
    check_present_values(report)
    check_semiannual_yields(report)
    check_implied_returns(report)
    check_forward_rate(report)
    check_forward_fx(report)
    check_option_replication(report)
    check_single_amounts(report)
    check_streams(report)
    check_loan_amortisation(report)
    irr = check_conventional_irr(report)
    check_irr_pitfalls(report)
    check_double_root_irr(report)
    check_negative_irr(report)
    check_bisect_contract(report)
    check_irr_reinvestment(report, irr)
    check_share_forward(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
