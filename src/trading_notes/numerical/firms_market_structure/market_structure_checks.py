"""Firms and market structure: cost and output decisions, oligopoly outcomes and concentration."""

import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import minimize_scalar

from trading_notes.numerical.firms_market_structure.firm_costs import (
    CubicCostFirm,
    LinearCournot,
    long_run_average_cost,
)
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close

F: Final = 108.0  # fixed cost
A_D: Final = 100.0  # demand intercept, p = A_D - Y
C: Final = 10.0  # oligopoly marginal cost
FIRM: Final = CubicCostFirm(fixed_cost=F)
MARKET: Final = LinearCournot(intercept=A_D, marginal_cost=C)


def cournot_iterated(n: int, iters: int = 2000) -> tuple[NDArray[np.float64], float]:
    """Return outputs and price after `iters` rounds of sequential best responses from 1 each."""
    q = np.full(n, 1.0)
    for _ in range(iters):
        for i in range(n):
            q[i] = max((A_D - C - (q.sum() - q[i])) / 2, 0.0)
    return q, A_D - q.sum()


def check_shutdown(report: CheckReport) -> None:
    """Check breakeven and shutdown prices, and profit at four prices."""
    print("== part 1: breakeven and shutdown (fixed cost 108, c_v = y^3 - 12 y^2 + 60 y)")
    min_avc = minimize_scalar(
        FIRM.average_variable_cost, bounds=(0.1, 20), method="bounded", options={"xatol": 1e-12}
    )
    min_atc = minimize_scalar(
        FIRM.average_total_cost, bounds=(0.1, 20), method="bounded", options={"xatol": 1e-12}
    )
    report.ok(
        "shutdown price 24 at y = 6 (MC = AVC there); breakeven price 40.42 at y = 7.08 (MC = ATC"
        " there)",
        close(min_avc.x, 6.0, 1e-5)
        and close(FIRM.marginal_cost(6.0), FIRM.average_variable_cost(6.0))
        and round(min_atc.fun, 2) == 40.42
        and round(min_atc.x, 2) == 7.08
        and close(FIRM.marginal_cost(min_atc.x), FIRM.average_total_cost(min_atc.x), 1e-5),
        f"min ATC {min_atc.fun:.4f} at {min_atc.x:.4f}",
    )
    rows = {}
    for p in (60, 40, 30, 20):
        y = FIRM.best_output(p)
        y_mc = (24 + np.sqrt(576 - 12 * (60 - p))) / 6  # where MC = p even if not chosen
        rows[p] = (
            y,
            p * y - FIRM.variable_cost(y) - F if y else -F,
            p * y_mc - FIRM.variable_cost(y_mc) - F,
        )
    report.ok(
        "outputs 8.00, 7.06, 6.45 and 0; profits 148.00, -2.97, -70.61 and -108.00 (closing); at 20"
        " producing on MC "
        "would lose 131.29",
        [round(rows[p][0], 2) for p in (60, 40, 30, 20)] == [8.0, 7.06, 6.45, 0.0]
        and [round(rows[p][1], 2) for p in (60, 40, 30, 20)] == [148.0, -2.97, -70.61, -108.0]
        and round(rows[20][2], 2) == -131.29,
    )
    report.ok(
        "between the shutdown and breakeven prices the loss is smaller than the fixed cost:"
        " operating covers part of F",
        all(-F < rows[p][1] < 0 for p in (40, 30)),
    )


def check_scale(report: CheckReport) -> None:
    """Check minimum efficient scale, natural monopoly and the tangency solution."""
    print(
        "== part 2: scale - minimum efficient scale, natural monopoly and the"
        " monopolistic-competition tangency"
    )
    mes = np.sqrt(2000 / 0.004)
    report.ok(
        "LRAC 2,000/y + 20 + 0.004y: minimum efficient scale 707, cost 25.66; demand of 4,000 holds"
        " 5.7 efficient "
        "plants, demand of 600 not one",
        round(mes) == 707
        and round(long_run_average_cost(mes), 2) == 25.66
        and round(4000 / mes, 1) == 5.7
        and 600 < mes,
    )
    y_t = np.sqrt(2000 / 0.024)  # tangency: LRAC'(y) = -0.02
    a_t = long_run_average_cost(y_t) + 0.02 * y_t
    report.ok(
        "tangency of p = 33.86 - 0.02y with LRAC at y = 289, p = 28.08: zero profit, 41% of"
        " efficient scale, cost "
        "2.43 above the minimum",
        round(y_t) == 289
        and round(long_run_average_cost(y_t), 2) == 28.08
        and round(a_t, 2) == 33.86
        and close(a_t - 0.02 * y_t, long_run_average_cost(y_t))
        and round(y_t / mes, 2) == 0.41
        and round(long_run_average_cost(y_t) - long_run_average_cost(mes), 2) == 2.43,
    )


def check_oligopoly(report: CheckReport) -> None:
    """Check Cournot by formula and by iteration, Stackelberg, and a cartel deviation."""
    print("== part 3: oligopoly outcomes for p = 100 - Y, MC = 10")
    for n in (1, 2, 5):
        qc, pc = MARKET.equilibrium(n)
        qi, pi = cournot_iterated(n)
        report.ok(
            f"Cournot with {n} firm(s): each {qc:.2f}, price {pc:.2f}; best-response iteration"
            " agrees",
            np.allclose(qi, qc, atol=1e-9) and close(pi, pc, 1e-9),
        )
    q_lead = (A_D - C) / 2
    q_follow = (A_D - C - q_lead) / 2
    p_stack = A_D - q_lead - q_follow
    report.ok(
        "Stackelberg: leader 45, follower 22.5, price 32.50; markups 0.82 (monopoly), 0.69, 0.75"
        " (duopoly), 0.60 "
        "(five firms), 0 (Bertrand)",
        q_lead == 45.0
        and q_follow == 22.5
        and p_stack == 32.5
        and [round((p - C) / p, 2) for p in (55.0, p_stack, 40.0, 25.0, 10.0)]
        == [0.82, 0.69, 0.75, 0.60, 0.0],
    )
    dev_q = (A_D - C - 22.5) / 2
    p_dev = A_D - dev_q - 22.5
    report.ok(
        "cartel at 22.5 each earns 1,012.5 each; a member that expands to its best response 33.75"
        " earns 1,139.06 and "
        "leaves the other 759.38",
        close((55 - C) * 22.5, 1012.5)
        and close(dev_q, 33.75)
        and round((p_dev - C) * dev_q, 2) == 1139.06
        and round((p_dev - C) * 22.5, 2) == 759.38,
    )


def check_concentration(report: CheckReport) -> None:
    """Check CR4, HHI, a merger's change in HHI and the Cournot markup."""
    print("== part 4: concentration measures")
    shares = np.array([30, 25, 15, 10, 5, 5, 5, 5], dtype=float)
    cr4 = shares[:4].sum()
    hhi = float(np.sum(shares**2))
    merged = np.concatenate([[30, 25, 25], shares[4:]])
    report.ok(
        "CR4 80; HHI 1,950; merging the 15 and 10 firms adds 2ab = 300 to 2,250, above 1,800 with"
        " a change above 100",
        cr4 == 80
        and hhi == 1950
        and float(np.sum(merged**2)) - hhi == 2 * 15 * 10
        and float(np.sum(merged**2)) == 2250,
    )
    eps = 1.5
    s = shares / 100
    report.ok(
        "Cournot: share-weighted markup sum s_i (s_i / |e|) = HHI / |e| = 0.195 / 1.5 = 13%",
        close(float(np.sum(s * s / eps)), hhi / 1e4 / eps) and round(hhi / 1e4 / eps, 2) == 0.13,
    )
    report.ok(
        "same CR4 of 80, different HHI: five firms of 20% give 2,000; 77% plus 23 firms of 1% give"
        " 5,952",
        5 * 20**2 == 2000 and 77**2 + 23 * 1 == 5952 and 77 + 3 == 80,
    )


def main() -> int:
    """Print the versions, then run the four parts with one report and print the count.

    All firms and markets are hypothetical; the rules come from Varian (2014), OpenStax Principles
    of Microeconomics 3e and the 2023 US Merger Guidelines. Shutdown and breakeven prices from the
    first-order conditions are checked against numerical minimisation, profit at each price against
    the closed-form loss of closing, the symmetric Cournot formula against iterated best responses,
    and the merger change in HHI as 2ab against recomputation from the merged shares.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    check_shutdown(report)
    check_scale(report)
    check_oligopoly(report)
    check_concentration(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
