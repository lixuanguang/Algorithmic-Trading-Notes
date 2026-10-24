"""Known dividends in a binomial tree, and the receiver swaption behind a callable bond."""

import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.option_pricing.black_scholes import BlackScholes
from trading_notes.numerical.option_valuation.dividend_tree import KnownDividendTree
from trading_notes.numerical.report import CheckReport, print_versions

type Floats = NDArray[np.float64]

SEED: Final = 20261121
N = stats.norm.cdf


def check_dividend_tree(report: CheckReport) -> None:
    """Check Example 21.5, and Hull's early-exercise bound on both sides."""
    print("== Part 1: known dollar dividends in a tree (Hull sec. 21.3)")
    vals = {
        n: KnownDividendTree(
            spot=52.0,
            strike=50.0,
            rate=0.10,
            vol=0.40,
            maturity=5 / 12,
            steps=n,
            dividends=[(3.5 / 12, 2.06)],
        ).value(call=False)
        for n in (5, 50, 100)
    }
    report.ok(
        "Example 21.5: American put 4.44 with 5 steps, 4.208 and 4.214 with 50 and 100",
        round(vals[5], 2) == 4.44 and round(vals[50], 3) == 4.208 and round(vals[100], 3) == 4.214,
        ", ".join(f"{v:.4f}" for v in vals.values()),
    )
    S0, K, r, sig, T, t_ex, steps = 50.0, 50.0, 0.05, 0.25, 0.5, 0.455, 1_000
    bound = K * (1 - math.exp(-r * (T - t_ex)))
    print(
        f"  call: ex-dividend at {t_ex} years, maturity {T}; Hull's bound K(1 - exp(-r(T - t_n)))"
        f" = {bound:.4f}"
    )
    for D in (0.05, 1.50):
        log: list[float] = []
        am = KnownDividendTree(
            spot=S0, strike=K, rate=r, vol=sig, maturity=T, steps=steps, dividends=[(t_ex, D)]
        ).value(True, exercise_log=log)
        eu = KnownDividendTree(
            spot=S0, strike=K, rate=r, vol=sig, maturity=T, steps=steps, dividends=[(t_ex, D)]
        ).value(True, american=False)
        if D < bound:
            report.ok(
                f"D = {D:.2f} below the bound: no node exercises and the American call equals"
                " the European on the same tree",
                not log and abs(am - eu) < 1e-12,
                f"{am:.6f}",
            )
        else:
            dt = T / steps
            report.ok(
                f"D = {D:.2f} above the bound: exercise is optimal at some nodes, all on the step"
                " just before the ex-date",
                bool(log) and all(t_ex - dt <= t < t_ex for t in log),
                f"American {am:.4f} against European {eu:.4f}; exercise times"
                f" {sorted(set(round(t, 4) for t in log))}",
            )
            pv = D * math.exp(-r * t_ex)
            # to maturity T the stock is reduced by the dividend's PV; to t_n (exercise just
            # before it) it is not
            black = max(
                BlackScholes(spot=S0 - pv, strike=K, maturity=T, rate=r, vol=sig).call(),
                BlackScholes(spot=S0, strike=K, maturity=t_ex, rate=r, vol=sig).call(),
            )
            print(
                f"  (reported) Black's approximation (Hull p. 363): max of European to T and to"
                f" t_n = {black:.4f}; it puts"
                " the 25% volatility on the whole stock price for the t_n leg, while the tree"
                " puts it on S* (Hull p. 360,"
                " n. 13), so the two are different models and the approximation can exceed the"
                " tree's American value"
            )


def check_swaptions(report: CheckReport, rng: np.random.Generator) -> None:
    """Check Example 29.4, payer-receiver parity and the callable bond's payoff identity."""
    print("== Part 2: receiver swaption, parity and the callable bond (Hull sec. 29.3)")
    L, A, sF, sK, sigma, Tx = 100.0, 2.0035, 0.06194, 0.062, 0.20, 5.0
    d1 = (math.log(sF / sK) + sigma**2 * Tx / 2) / (sigma * math.sqrt(Tx))
    d2 = d1 - sigma * math.sqrt(Tx)
    payer = L * A * (sF * N(d1) - sK * N(d2))
    receiver = L * A * (sK * N(-d2) - sF * N(-d1))
    report.ok(
        "Example 29.4: the payer swaption is worth 2.19 million",
        round(payer, 2) == 2.19,
        f"{payer:.4f}",
    )
    report.ok(
        "payer - receiver = L A (s_F - s_K), the forward payer swap, to 1e-12 (Problem 29.18)",
        abs(payer - receiver - L * A * (sF - sK)) < 1e-12,
        f"receiver {receiver:.4f}",
    )
    worst = 0.0
    for _ in range(1_000):
        z = rng.uniform(-0.01, 0.12)
        slope = rng.uniform(-0.02, 0.02)
        times = np.arange(1, 7) / 2  # semiannual payments for three years after the exercise date
        P = np.exp(-(z + slope * times / 3) * times)
        A_T = 0.5 * P.sum()
        s_T = (1 - P[-1]) / A_T
        bond = L * (sK / 2 * P.sum() + P[-1])  # straight bond paying the swaption's fixed rate
        call_payoff = max(bond - L, 0.0)  # issuer's call at par on the exercise date
        receiver_payoff = L * A_T * max(sK - s_T, 0.0)
        worst = max(worst, abs(call_payoff - receiver_payoff))
    report.ok(
        "on 1,000 random curves the issuer's call at par pays exactly the receiver swaption's"
        " payoff (to 1e-12)",
        worst < 1e-12,
        f"largest gap {worst:.1e}",
    )
    print(
        f"  so a bond callable at par on that date is worth the straight bond less {receiver:.4f}"
        " million per 100 million"
        " under Black's swaption model (inputs of Example 29.4)"
    )


def main() -> int:
    """Print the versions, then run the two parts with one report.

    Part 1 reproduces Hull's Example 21.5 (sec. 21.3: 4.44 with 5 steps; 4.208 and 4.214 with 50 and
    100) and tests both sides of his early-exercise condition for an American call (sec. 15.12):
    exercise just before the last ex-dividend date can be optimal only if D_n > K(1 - exp(-r(T -
    t_n))). Part 2 checks the receiver swaption (eq. 29.11), payer-receiver parity (Problem 29.18)
    and the callable bond as a straight bond less a receiver swaption (Business Snapshot 29.2) with
    Example 29.4's inputs; the payoff identity B_T - L = L A_T (s_K - s_T) is checked on 1,000
    random curves (seed 20261121).

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    check_dividend_tree(report)
    check_swaptions(report, np.random.default_rng(SEED))
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
