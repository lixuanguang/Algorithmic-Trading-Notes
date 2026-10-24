"""Worked examples of option replication, covered positions, spreads, collars and selection."""

import math
import sys
from collections.abc import Callable
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

S0: Final = 100.0
K: Final = 100.0
T: Final = 0.5
R: Final = 0.04
SIG: Final = 0.20


def call_payoff(st: Floats | float, k: float) -> Floats:
    """Return the payoff of a long call struck at k at expiry, at the terminal prices st."""
    return np.maximum(st - k, 0.0)


def put_payoff(st: Floats | float, k: float) -> Floats:
    """Return the payoff of a long put struck at k at expiry, at the terminal prices st."""
    return np.maximum(k - st, 0.0)


def fd_delta(f: Callable[[float], float], s: float, h: float = 1e-4) -> float:
    """Return the central finite-difference derivative of f at s."""
    return (f(s + h) - f(s - h)) / (2 * h)


def share_plus_forwards(s: float, n_fwd: float, q_: float = 0.02) -> float:
    """Return one share (dividends to be received) plus n_fwd short fixed-strike forwards."""
    return s - n_fwd * (s * math.exp(-q_ * T) - K * math.exp(-R * T))


def skew_vol(k: float, atm: float = 0.20, slope: float = -0.30) -> float:
    """Equity-style skew: implied volatility falls 3 points per 10% of moneyness."""
    return atm + slope * math.log(k / S0)


def check_replication(report: CheckReport, ST: Floats) -> None:
    """Check replicating asset returns with options, and the deltas of hedged positions.

    Args:
        report: The run's report.
        ST: The terminal prices of the payoff grid.
    """
    print("== part 1: replicating asset returns with options, and the deltas of hedged positions")
    report.ok(
        "synthetic long forward: long call - short put at K = F costs zero (F = 102.0201, no"
        " dividend)",
        abs(
            BlackScholes(spot=S0, strike=S0 * math.exp(R * T), maturity=T, rate=R, vol=SIG).call()
            - BlackScholes(spot=S0, strike=S0 * math.exp(R * T), maturity=T, rate=R, vol=SIG).put()
        )
        < 1e-10,
    )
    report.ok(
        "terminal payoffs (any dividend policy): call - put + K pays S_T; stock - call pays K -"
        " (K - S_T)+; stock + put pays (S_T - K)+ + K. Dividends are extra cash to the stockholder"
        " only",
        bool(
            np.allclose(call_payoff(ST, K) - put_payoff(ST, K) + K, ST)
            and np.allclose(ST - call_payoff(ST, K), K - put_payoff(ST, K))
            and np.allclose(ST + put_payoff(ST, K), call_payoff(ST, K) + K)
        ),
    )
    for q_ in (0.0, 0.02):
        c_q, p_q = (
            BlackScholes(spot=S0, strike=K, maturity=T, rate=R, vol=SIG, dividend_yield=q_).call(),
            BlackScholes(spot=S0, strike=K, maturity=T, rate=R, vol=SIG, dividend_yield=q_).put(),
        )
        pv_div = S0 * (1 - math.exp(-q_ * T))  # PV of the yield paid over the life
        report.ok(
            f"q = {q_:.0%}: values. Synthetic stock costs S0 e^(-qT) ="
            f" {S0 * math.exp(-q_ * T):.4f};"
            f" stock = synthetic + PV(dividends) {pv_div:.4f}; covered call = short put + bond +"
            " PV(div); protective put = call + bond + PV(div)",
            close(c_q - p_q + K * math.exp(-R * T), S0 * math.exp(-q_ * T), 1e-10)
            and close(S0 - c_q, K * math.exp(-R * T) - p_q + pv_div, 1e-10)
            and close(S0 + p_q, c_q + K * math.exp(-R * T) + pv_div, 1e-10),
        )
    # discrete dividend: 1.00 paid at three months; options priced on the escrowed price S0 - D
    # (Hull sec. 15.12)
    d_amt, t_d = 1.00, 0.25
    D = d_amt * math.exp(-R * t_d)
    c_d, p_d = (
        BlackScholes(spot=S0 - D, strike=K, maturity=T, rate=R, vol=SIG).call(),
        BlackScholes(spot=S0 - D, strike=K, maturity=T, rate=R, vol=SIG).put(),
    )
    st_paths = np.array([70.0, 100.0, 130.0])
    stock_cash = st_paths + d_amt * math.exp(R * (T - t_d))  # dividend reinvested at r to expiry
    synth_cash = call_payoff(st_paths, K) - put_payoff(st_paths, K) + K
    report.ok(
        "discrete dividend 1.00 at 3 months: p + S0 = c + Ke^(-rT) + D with D = 0.9900; at expiry"
        " the stock (dividend reinvested) exceeds the synthetic by 1.0101 in every state, whose"
        " present value is D",
        close(p_d + S0, c_d + K * math.exp(-R * T) + D, 1e-10)
        and bool(np.allclose(stock_cash - synth_cash, d_amt * math.exp(R * (T - t_d))))
        and close(d_amt * math.exp(R * (T - t_d)) * math.exp(-R * T), D, 1e-12),
    )

    for q_ in (0.0, 0.02):
        dc, dp = (
            BlackScholes(
                spot=S0, strike=K, maturity=T, rate=R, vol=SIG, dividend_yield=q_
            ).call_delta(),
            BlackScholes(
                spot=S0, strike=K, maturity=T, rate=R, vol=SIG, dividend_yield=q_
            ).put_delta(),
        )
        fwd_short = fd_delta(lambda s: -(s * math.exp(-q_ * T) - K * math.exp(-R * T)), S0)
        fd_c = fd_delta(
            lambda s: BlackScholes(
                spot=s, strike=K, maturity=T, rate=R, vol=SIG, dividend_yield=q_
            ).call(),
            S0,
        )
        fd_p = fd_delta(
            lambda s: BlackScholes(
                spot=s, strike=K, maturity=T, rate=R, vol=SIG, dividend_yield=q_
            ).put(),
            S0,
        )
        gap = (-1 + dc) - dp
        report.ok(
            f"q = {q_:.0%}: spot deltas by finite difference match BSM; a fixed-strike short"
            " forward"
            f" has delta -e^(-qT) = {fwd_short:.7f}; call - put = e^(-qT); short stock + call - put"
            f" delta = {gap:+.7f} (zero only without dividends)",
            abs(fd_c - dc) < 1e-7
            and abs(fd_p - dp) < 1e-7
            and abs(fwd_short + math.exp(-q_ * T)) < 1e-9
            and abs(dc - dp - math.exp(-q_ * T)) < 1e-12
            and abs(gap - (math.exp(-q_ * T) - 1)) < 1e-12,
            f"call {dc:.4f}, put {dp:.4f}, covered call {1 - dc:.4f}, protective put {1 + dp:.4f}",
        )

    report.ok(
        "at q = 2%, T = 0.5 (finite differences): one share plus one short forward keeps delta"
        " +0.00995, although the forward's payoff slope at expiry is -1; e^(qT) = 1.01005 short"
        " forwards per share are needed for delta zero",
        abs(fd_delta(lambda s: share_plus_forwards(s, 1.0), S0) - (1 - math.exp(-0.01))) < 1e-8
        and abs(fd_delta(lambda s: share_plus_forwards(s, 1.0), S0) - 0.00995) < 5e-6
        and abs(fd_delta(lambda s: share_plus_forwards(s, math.exp(0.01)), S0)) < 1e-8,
    )
    dc, dp = (
        BlackScholes(spot=S0, strike=K, maturity=T, rate=R, vol=SIG).call_delta(),
        BlackScholes(spot=S0, strike=K, maturity=T, rate=R, vol=SIG).put_delta(),
    )
    report.ok(
        "no dividend: call delta 0.5840, covered call 0.4160, protective put 0.5840, short stock +"
        " call -0.4160",
        abs(dc - 0.5840) < 5e-5
        and abs((1 + dp) - 0.5840) < 5e-5
        and abs((-1 + dc) + 0.4160) < 5e-5,
    )


def check_covered_positions(report: CheckReport, ST: Floats) -> None:
    """Check covered calls, protective puts and short-position hedges.

    Args:
        report: The run's report.
        ST: The terminal prices of the payoff grid.
    """
    print("== part 2: covered calls, protective puts and short-position hedges")
    report.ok(
        "Natenberg: stock at 100, sell the 95 call at 6.50 -> break-even 93.50, maximum profit 1.50"
        " (the time premium)",
        95 + 6.5 - 100 == 1.5 and 100 - 6.5 == 93.5,
    )
    report.ok(
        "sell the 105 call at 2.00 instead -> break-even 98, maximum profit 7 at or above 105",
        100 - 2 == 98 and 105 + 2 - 100 == 7,
    )
    cc_profit = np.minimum(ST, 105) + 2 - 100
    report.ok(
        "covered-call profit is the short-put shape: capped at 7, loss 98 - S_T below 98",
        bool(cc_profit.max() == 7 and close(cc_profit[ST == 60][0], -38)),
    )
    pp = BlackScholes(spot=S0, strike=95, maturity=T, rate=R, vol=SIG).put()
    pp_fin = pp * math.exp(R * T)
    pp_profit = ST + put_payoff(ST, 95) - 100 - pp
    report.ok(
        "protective put: 95 put costs 2.6786; max loss 100 - 95 + premium = 7.68 (7.73 with the"
        " premium financed); break-even 102.68 (102.73 financed)",
        abs(pp - 2.6786) < 5e-5
        and abs(-pp_profit.min() - 7.68) < 5e-3
        and abs(100 - 95 + pp_fin - 7.73) < 5e-3
        and abs(100 + pp - 102.68) < 5e-3,
        f"{pp:.4f}",
    )
    report.ok(
        "Natenberg's euro hedge: buying the 1.40 call on EUR 1m at 0.02 caps the cost at 1.42m all"
        " in; at 1.25 the firm pays 1.27m",
        1.40e6 + 0.02e6 == 1.42e6 and 1.25e6 + 0.02e6 == 1.27e6,
    )
    # a short seller at 100 hedges with a long 105 call or a short 95 put (both six months)
    c105 = BlackScholes(spot=S0, strike=105, maturity=T, rate=R, vol=SIG).call()
    p95 = pp
    short_call_hedge = (100 - ST) + (call_payoff(ST, 105) - c105)
    short_put_write = (100 - ST) + (p95 - put_payoff(ST, 95))
    report.ok(
        "short stock + long 105 call: loss capped at 5 + 4.3770 = 9.38 however high the stock goes",
        abs(c105 - 4.3770) < 5e-5 and abs(short_call_hedge.min() + 5 + c105) < 1e-9,
        f"{c105:.4f}",
    )
    report.ok(
        "short stock + short 95 put: the 2.68 premium only cushions; the loss is unlimited as the"
        " stock rises and the gain is capped at 7.68 below 95",
        bool(short_put_write[-1] < -50 and abs(short_put_write.max() - (5 + p95)) < 1e-9),
    )


def check_spreads_collars(report: CheckReport, ST: Floats) -> None:
    """Check spreads, straddles, the range forward, calendar spreads, collars and skew.

    Args:
        report: The run's report.
        ST: The terminal prices of the payoff grid.
    """
    print("== part 3: spreads, straddles, collars, calendar spreads, and skew")
    bull = call_payoff(ST, 30) - call_payoff(ST, 35) - 2
    report.ok(
        "Hull Example 12.2 bull spread (buy 30 call at 3, sell 35 call at 1): profit -2, S_T - 32,"
        " +3",
        bool(bull.min() == -2 and bull.max() == 3),
    )
    bear = put_payoff(ST, 35) - put_payoff(ST, 30) - 2
    report.ok(
        "Hull Example 12.3 bear spread (buy 35 put at 3, sell 30 put at 1): profit +3 below 30, -2"
        " above 35",
        bool(bear.max() == 3 and bear.min() == -2),
    )

    def strad(s: float) -> float:
        return max(s - 70, 0) + max(70 - s, 0) - 7

    report.ok(
        "Hull straddle at 70 (call 4, put 3): -6 at 69, -7 at 70, +13 at 90, +8 at 55; break-evens"
        " 63 and 77",
        (strad(69), strad(70), strad(90), strad(55), strad(63), strad(77)) == (-6, -7, 13, 8, 0, 0),
    )
    k1 = 1.30
    k2 = brentq(
        lambda k: (
            BlackScholes(
                spot=1.32, strike=k, maturity=0.25, rate=0.02, vol=0.14, dividend_yield=0.02
            ).call()
            - BlackScholes(
                spot=1.32, strike=k1, maturity=0.25, rate=0.02, vol=0.14, dividend_yield=0.02
            ).put()
        ),
        1.31,
        1.45,
    )
    report.ok(
        "Hull sec. 17.2 zero-cost range forward: a 1.3000 put and a 1.3414 call are both worth"
        " 0.0273",
        abs(k2 - 1.3414) < 5e-5
        and abs(
            BlackScholes(
                spot=1.32, strike=k1, maturity=0.25, rate=0.02, vol=0.14, dividend_yield=0.02
            ).put()
            - 0.0273
        )
        < 5e-5,
    )
    # calendar spread: sell 3-month 100 call, buy 6-month 100 call. Valuation date: the 3-month
    # expiry, with 0.25 years left on the long call and the BSM inputs unchanged. Value = long call
    # - payoff of the expiring short call; profit = value - initial cost (premium paid at
    # inception, not financed); the financed profit subtracts the cost grown at r for the three
    # months.
    c3, c6 = (
        BlackScholes(spot=S0, strike=100, maturity=0.25, rate=R, vol=SIG).call(),
        BlackScholes(spot=S0, strike=100, maturity=0.5, rate=R, vol=SIG).call(),
    )
    cost_cal = c6 - c3
    grid_s = (80, 95, 100, 105, 120)
    cal_value = [
        BlackScholes(spot=s, strike=100, maturity=0.25, rate=R, vol=SIG).call() - max(s - 100, 0)
        for s in grid_s
    ]
    cal_profit = [v - cost_cal for v in cal_value]
    cal_profit_fin = [v - cost_cal * math.exp(R * 0.25) for v in cal_value]
    report.ok(
        "calendar spread (buy 6m, sell 3m 100 calls, cost 2.141842): at the 3-month expiry its"
        " value"
        " is 0.052704, 2.190593, 4.485236, 2.747684 and 1.108320 at 80-120; profits after the cost"
        " are -2.089, +0.049, +2.343, +0.606 and -1.034, peaking at the strike",
        abs(cost_cal - 2.141842) < 5e-7
        and bool(
            np.allclose(cal_value, [0.052704, 2.190593, 4.485236, 2.747684, 1.108320], atol=5e-7)
        )
        and min(cal_value) > 0
        and cal_profit[2] == max(cal_profit)
        and cal_profit[0] < 0 < cal_profit[2],
        "value "
        + " ".join(f"{x:.6f}" for x in cal_value)
        + "; profit "
        + " ".join(f"{x:+.3f}" for x in cal_profit),
    )
    report.ok(
        "value never falls below zero (the long call is worth at least the expiring call's payoff),"
        " so the maximum loss is the 2.141842 cost; financing the cost at 4% for three months"
        " lowers"
        " every profit by 0.021526",
        all(v >= 0 for v in cal_value)
        and bool(
            np.allclose(
                np.subtract(cal_profit, cal_profit_fin),
                cost_cal * (math.exp(R * 0.25) - 1),
                atol=1e-12,
            )
        )
        and abs(cost_cal * (math.exp(R * 0.25) - 1) - 0.021526) < 5e-7,
    )
    report.ok(
        "a long calendar spread is long vega: at inception, a 2-point rise in implied volatility"
        " raises its value",
        BlackScholes(spot=S0, strike=100, maturity=0.5, rate=R, vol=0.22).call()
        - BlackScholes(spot=S0, strike=100, maturity=0.25, rate=R, vol=0.22).call()
        > cost_cal,
    )

    put90_flat = BlackScholes(spot=S0, strike=90, maturity=T, rate=R, vol=0.20).put()
    put90_skew = BlackScholes(spot=S0, strike=90, maturity=T, rate=R, vol=skew_vol(90)).put()
    k_flat = brentq(
        lambda k: BlackScholes(spot=S0, strike=k, maturity=T, rate=R, vol=0.20).call() - put90_flat,
        100,
        150,
    )
    k_skew = brentq(
        lambda k: (
            BlackScholes(spot=S0, strike=k, maturity=T, rate=R, vol=skew_vol(k)).call() - put90_skew
        ),
        100,
        150,
    )
    report.ok(
        "zero-cost collar with a 90 put: flat 20% volatility allows a 116.80 call; with the skew"
        " the"
        " dearer put (23.2%) forces the call strike down to 110.29",
        abs(k_flat - 116.80) < 0.01
        and abs(k_skew - 110.29) < 0.01
        and abs(skew_vol(90) - 0.2316) < 5e-4,
        f"flat {k_flat:.2f}, skew {k_skew:.2f}",
    )

    collar_profit = np.minimum(np.maximum(ST, 90), k_flat) - 100
    report.ok(
        "bear spread break-even 33; zero-cost collar (stock 100, 90 put, 116.80 call): max gain"
        " 16.80, max loss 10, break-even 100",
        abs(bear[np.argmin(np.abs(ST - 33))]) < 1e-9
        and abs(collar_profit.max() - (k_flat - 100)) < 1e-9
        and abs(collar_profit.min() + 10) < 1e-9
        and abs(k_flat - 116.80) < 0.005,
    )


def check_selection(report: CheckReport) -> None:
    """Check strategy selection for a 10 million single-stock holding.

    Args:
        report: The run's report.
    """
    print(
        "== part 4: strategy selection for a 10 million single-stock holding (100,000 shares at"
        " 100)"
    )
    n, s0 = 100_000, 100.0
    T6 = 0.5
    put85 = BlackScholes(spot=s0, strike=85, maturity=T6, rate=R, vol=skew_vol(85)).put()
    call110 = BlackScholes(spot=s0, strike=110, maturity=T6, rate=R, vol=skew_vol(110)).call()
    k_c = brentq(
        lambda k: (
            BlackScholes(spot=s0, strike=k, maturity=T6, rate=R, vol=skew_vol(k)).call() - put85
        ),
        100,
        160,
    )
    alts = {
        "protective 85 put": (
            n * put85,
            1 + BlackScholes(spot=s0, strike=85, maturity=T6, rate=R, vol=skew_vol(85)).put_delta(),
        ),
        "covered 110 call": (
            -n * call110,
            1
            - BlackScholes(
                spot=s0, strike=110, maturity=T6, rate=R, vol=skew_vol(110)
            ).call_delta(),
        ),
        "zero-cost 85/k collar": (
            0.0,
            1
            + BlackScholes(spot=s0, strike=85, maturity=T6, rate=R, vol=skew_vol(85)).put_delta()
            - BlackScholes(
                spot=s0, strike=k_c, maturity=T6, rate=R, vol=skew_vol(k_c)
            ).call_delta(),
        ),
    }
    report.ok(
        "85 put (24.9% implied) costs 1.24% of the holding (124k); a 110 call (17.1%) raises 2.05%;"
        " the zero-cost collar's call strike is 113.05",
        abs(put85 / s0 - 0.0124) < 5e-4
        and abs(call110 / s0 - 0.0205) < 5e-4
        and abs(k_c - 113.05) < 0.01,
        f"put {put85:.4f}, call110 {call110:.4f}, collar call {k_c:.2f}",
    )
    report.ok(
        "deltas per share: protective put 0.870, covered 110 call 0.713, zero-cost collar 0.667 (a"
        " third less exposure for no premium)",
        all(
            abs(alts[a][1] - v) < 0.001
            for a, v in (
                ("protective 85 put", 0.870),
                ("covered 110 call", 0.713),
                ("zero-cost 85/k collar", 0.667),
            )
        ),
        " ".join(f"{a}: {v[1]:.3f}" for a, v in alts.items()),
    )
    scen = {"-30%": 70.0, "-10%": 90.0, "flat": 100.0, "+10%": 110.0, "+30%": 130.0}
    res: dict[str, tuple[float, float, float, float]] = {}
    for name, st in scen.items():
        stock = st - s0
        res[name] = (
            stock,
            stock + max(85 - st, 0) - put85 * math.exp(R * T6),
            stock - max(st - 110, 0) + call110 * math.exp(R * T6),
            stock + max(85 - st, 0) - max(st - k_c, 0),
        )
    report.ok(
        "in a 30% fall the put and the collar stop the loss near 15 (put -16.27 with financed"
        " premium, collar -15.00); the covered call loses 27.91",
        abs(res["-30%"][1] + 16.27) < 0.01
        and abs(res["-30%"][3] + 15.0) < 1e-9
        and abs(res["-30%"][2] + 27.91) < 0.01,
    )
    report.ok(
        "in a 30% rise the stock alone earns 30; put 28.73, covered call 12.09, collar 13.05",
        abs(res["+30%"][1] - 28.73) < 0.01
        and abs(res["+30%"][2] - 12.09) < 0.01
        and abs(res["+30%"][3] - 13.05) < 0.01,
    )
    d110 = BlackScholes(spot=s0, strike=110, maturity=T6, rate=R, vol=skew_vol(110)).call_delta()
    d100 = BlackScholes(spot=s0, strike=100, maturity=T6, rate=R, vol=0.20).call_delta()
    report.ok(
        "to cut exposure to 60% with 110 calls would take 1.39 calls per share, more calls than"
        " shares (partly naked); at-the-money calls need 0.685 per share, fully covered",
        abs(0.4 / d110 - 1.391) < 0.001 and 0.4 / d110 > 1 and abs(0.4 / d100 - 0.685) < 0.001,
    )
    atm = BlackScholes(spot=s0, strike=100, maturity=T6, rate=R, vol=0.20).call()
    report.ok(
        "to raise exposure to 125% without buying stock, buy 0.25/0.584 = 0.428 at-the-money calls"
        " per share, a premium of 0.284m (2.8% of the holding) against 2.5m of stock",
        abs(0.25 / d100 - 0.428) < 0.001 and abs(0.25 / d100 * n * atm / 1e6 - 0.284) < 0.001,
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Reproduced from Hull, Options, Futures, and Other Derivatives, 11th Global ed. (2022), chap. 12
    and sec. 17.2, and Natenberg, Option Volatility and Pricing, 2nd ed. (2015), chap. 17.
    Conventions: value is what a position is worth on the valuation date; profit is value (or payoff
    at expiry) less the premium paid, with the premium also shown financed to expiry where stated;
    Black-Scholes prices with a continuous dividend yield; per share unless stated. No random draws.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    ST = np.linspace(0, 200, 401)
    report = CheckReport()
    check_replication(report, ST)
    check_covered_positions(report, ST)
    check_spreads_collars(report, ST)
    check_selection(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
