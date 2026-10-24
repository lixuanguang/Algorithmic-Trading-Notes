"""Rate trees and bonds with embedded options: calibration, callable and putable bonds, duration."""

import itertools
import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq

from trading_notes.numerical.embedded_option_bonds.binomial_tree import LognormalTree
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

SEED: Final = 20261019
PAR: Final = (0.035, 0.042, 0.047, 0.052)
CF: Final = (6.5, 6.5, 6.5, 106.5)  # the 6.5% four-year bond's cash flows


def value_shifted(
    par_shift: float, oas_: float, kind: str = "call", key: int | None = None
) -> float:
    """Value of the 6.5% bond on the tree calibrated to the par curve shifted by par_shift.

    The shift is applied to every par rate, or only to the key-rate `key` when given.
    """
    p = [x + (par_shift if key is None or k == key else 0.0) for k, x in enumerate(PAR)]
    tree = LognormalTree.calibrate(p)
    call_px = 100.0 if kind == "call" else None
    put_px = 100.0 if kind == "put" else None
    return tree.value([6.5] * 4, spread=oas_, call=call_px, put=put_px)


def check_calibration(report: CheckReport) -> LognormalTree:
    """Part 1: calibrating the lattice to the par curve (Handbook chap. 36, pp. 836-840).

    Args:
        report: The run's report.

    Returns:
        The calibrated lattice.
    """
    print("== part 1: calibrating the lattice to the par curve (Handbook chap. 36, pp. 836-840)")
    tree = LognormalTree.calibrate(PAR)
    r1 = [tree.rate(1, i) for i in range(2)]
    r2 = [tree.rate(2, i) for i in range(3)]
    r3 = [tree.rate(3, i) for i in range(4)]
    report.ok(
        "year-1 rates 4.4448 / 5.4289; year-2 rates 4.6958 / 5.7354 / 7.0053 percent",
        all(
            abs(a - b) < 5e-7
            for a, b in zip(
                r1 + r2, [0.044448, 0.054289, 0.046958, 0.057354, 0.070053], strict=True
            )
        ),
        " ".join(f"{x:.6f}" for x in r1 + r2),
    )
    report.ok(
        "year-3 rates 5.0483 / 6.1660 / 7.5312 / 9.1986 percent (Exhibit 36-9 prints 9.1987 for the"
        " top node)",
        all(
            abs(a - b) < 5e-7
            for a, b in zip(r3, [0.050483, 0.061660, 0.075312, 0.091986], strict=True)
        ),
        " ".join(f"{x:.6f}" for x in r3),
    )
    report.ok(
        "every on-the-run par bond reprices at 100 on the calibrated tree",
        all(
            abs(LognormalTree(lows=tree.lows[: k + 1]).value([100 * PAR[k]] * (k + 1)) - 100) < 1e-9
            for k in range(4)
        ),
    )
    report.ok(
        "first trial r1 = 4.75% gives 99.691 (too low), so the calibrated rate must be lower (p."
        " 837)",
        bool(abs(LognormalTree(lows=(0.035, 0.0475)).value([4.2, 4.2]) - 99.691) < 5e-4),
    )
    return tree


def check_option_free(
    report: CheckReport, tree: LognormalTree
) -> tuple[list[float], list[float], float]:
    """Part 2: arbitrage-free value of an option-free bond, by spot rates, the lattice and paths.

    Args:
        report: The run's report.
        tree: The calibrated lattice, from part 1.

    Returns:
        The discount factors, the spot rates and the lattice value of the 6.5% bond.
    """
    print(
        "== part 2: arbitrage-free value of an option-free bond (spot curve, lattice and pathwise)"
    )
    dfs: list[float] = []
    for c in PAR:
        dfs.append((1 - c * sum(dfs)) / (1 + c))
    spots = [d ** (-1 / (k + 1)) - 1 for k, d in enumerate(dfs)]
    report.ok(
        "bootstrapped spot rates 3.5000 / 4.2148 / 4.7352 / 5.2706 percent (annual compounding)",
        all(
            abs(a - b) < 5e-7
            for a, b in zip(spots, [0.035, 0.042148, 0.047352, 0.052706], strict=True)
        ),
        " ".join(f"{s:.6f}" for s in spots),
    )
    pv_spot = sum(c * d for c, d in zip(CF, dfs, strict=True))
    pv_tree = tree.value([6.5] * 4)
    report.ok(
        "6.5% four-year bond: 104.643 by spot rates and by the lattice (identical: the lattice is"
        " arbitrage-free)",
        abs(pv_spot - 104.643) < 5e-4 and close(pv_spot, pv_tree, 1e-9),
        f"{pv_spot:.6f} {pv_tree:.6f}",
    )
    paths = list(itertools.product([0, 1], repeat=3))
    pv_paths = []
    for path in paths:
        rates = [tree.lows[0]] + [tree.rate(t + 1, sum(path[: t + 1])) for t in range(3)]
        disc = np.cumprod([1 / (1 + r) for r in rates])
        pv_paths.append(float(np.dot(CF, disc)))
    report.ok(
        "pathwise valuation: the average of the eight equally likely path values equals the lattice"
        " value",
        len(pv_paths) == 8 and close(float(np.mean(pv_paths)), pv_tree, 1e-9),
        f"range {min(pv_paths):.3f}-{max(pv_paths):.3f}",
    )
    # arbitrage when a market price departs from the arbitrage-free value: strip the bond into zeros
    mkt = 104.20
    zeros_cost = pv_spot
    report.ok(
        "if the bond trades at 104.20, buying it and selling its cash flows as zero-coupon bonds"
        " earns 0.443 now",
        abs(zeros_cost - mkt - 0.443) < 5e-4,
    )
    return dfs, spots, pv_tree


def check_callable(
    report: CheckReport, tree: LognormalTree, straight: float
) -> tuple[float, float, LognormalTree]:
    """Part 3: callable and putable bonds on the lattice, volatility and curve shifts.

    Args:
        report: The run's report.
        tree: The calibrated lattice, from part 1.
        straight: The option-free value of the 6.5% bond, from part 2.

    Returns:
        The callable and putable values, and the lattice at 20% volatility.
    """
    print("== part 3: callable and putable bonds on the lattice (Handbook pp. 840-845)")
    callable_ = tree.value([6.5] * 4, call=100.0)
    putable = tree.value([6.5] * 4, put=100.0)
    report.ok(
        "callable at 100 after year 1: 102.899; call option 1.745 unrounded (Handbook 1.744 from"
        " rounded values, and its text prints 104.634 for 104.643)",
        bool(abs(callable_ - 102.899) < 5e-4 and abs(straight - callable_ - 1.7445) < 1e-4),
        f"{callable_:.6f}",
    )
    report.ok(
        "putable at 100 after year 1: 105.327; put option 0.684",
        bool(abs(putable - 105.327) < 5e-4 and abs(putable - straight - 0.684) < 5e-4),
        f"{putable:.6f}",
    )
    step = [4.25, 4.25, 7.5, 7.5]
    report.ok(
        "single step-up note 4.25%/7.50%: noncallable 102.082, callable at par at years 2 and 3"
        " 100.031",
        bool(
            abs(tree.value(step) - 102.082) < 5e-4
            and abs(tree.value(step, call=100.0, exercise_from=2) - 100.031) < 5e-4
        ),
    )
    # volatility effect: recalibrate at 20% volatility
    tree20 = LognormalTree.calibrate(PAR, 0.20)
    c20 = tree20.value([6.5] * 4, call=100.0)
    p20 = tree20.value([6.5] * 4, put=100.0)
    s20 = tree20.value([6.5] * 4)
    report.ok(
        "at 20% volatility the straight bond is unchanged (104.643), the callable falls and the"
        " putable rises",
        bool(abs(s20 - straight) < 1e-9 and c20 < callable_ and p20 > putable),
        f"callable {c20:.3f}, putable {p20:.3f}",
    )
    # curve level: parallel +100 bp; shape: flat curve at 4.5%
    tree_up = LognormalTree.calibrate([p + 0.01 for p in PAR])
    tree_flat = LognormalTree.calibrate([0.045] * 4)
    call_up = tree_up.value([6.5] * 4, call=100.0)
    str_up = tree_up.value([6.5] * 4)
    call_flat = tree_flat.value([6.5] * 4, call=100.0)
    str_flat = tree_flat.value([6.5] * 4)
    put_up = tree_up.value([6.5] * 4, put=100.0)
    report.ok(
        "rates up 100 bp: the call is worth less (1.744 -> smaller) and the put more",
        bool(
            (str_up - call_up) < (straight - callable_) and (put_up - str_up) > (putable - straight)
        ),
        f"call {str_up - call_up:.3f}, put {put_up - str_up:.3f}",
    )
    report.ok(
        "a flat 4.5% curve, below the upward-sloping curve's later forwards, makes the call worth"
        " more than on the base curve",
        bool((str_flat - call_flat) > (straight - callable_)),
        f"call {str_flat - call_flat:.3f}",
    )
    return callable_, putable, tree20


def check_oas(
    report: CheckReport,
    tree: LognormalTree,
    tree20: LognormalTree,
    cf_spots: list[float],
    callable_: float,
) -> float:
    """Part 4: the option-adjusted spread and the Z-spread of the callable bond.

    Args:
        report: The run's report.
        tree: The calibrated lattice, from part 1.
        tree20: The lattice at 20% volatility, from part 3.
        cf_spots: The spot rates of part 2.
        callable_: The callable value of part 3, which the OAS reprices.

    Returns:
        The option-adjusted spread, as a fraction.
    """
    print("== part 4: option-adjusted spread (Handbook pp. 849-850)")
    oas = brentq(lambda s: tree.value([6.5] * 4, spread=s, call=100.0) - 102.218, -0.02, 0.05)
    report.ok(
        "OAS that reprices the callable at 102.218 is 35.0 bp",
        abs(oas - 0.0035) < 2e-5,
        f"{oas * 1e4:.2f} bp",
    )
    # at the shifted tree the NHLL node (t=3, one up move) is no longer called
    r_hll = tree.rate(3, 1)
    cont_hll = 106.5 / (1 + r_hll + 0.0035)
    report.ok(
        "with 35 bp added the HLL node is worth 99.985 and is not called (it was 100.315 and"
        " called)",
        abs(cont_hll - 99.985) < 5e-4 and abs(106.5 / (1 + r_hll) - 100.315) < 5e-4,
    )
    z = brentq(
        lambda s: (
            sum(
                c / (1 + sp + s) ** (k + 1)
                for k, (c, sp) in enumerate(zip(CF, cf_spots, strict=True))
            )
            - 102.218
        ),
        -0.05,
        0.05,
    )
    report.ok(
        "Z-spread of the same callable is 67.8 bp; the option cost Z - OAS is 32.8 bp",
        abs(z * 1e4 - 67.80) < 0.01 and abs((z - oas) * 1e4 - 32.80) < 0.02 and z > oas,
        f"Z {z * 1e4:.2f} bp",
    )
    oas20 = brentq(
        lambda s: tree20.value([6.5] * 4, spread=s, call=100.0) - 102.218,
        -0.02,
        0.05,
    )
    report.ok(
        "assuming 20% volatility lowers the callable's OAS (the option is worth more, less spread"
        " is"
        " left)",
        oas20 < oas,
        f"{oas20 * 1e4:.2f} bp",
    )
    return oas


def check_durations(
    report: CheckReport, tree: LognormalTree, oas: float, straight: float, putable: float
) -> None:
    """Part 5: effective, one-sided and key-rate durations and effective convexity.

    Args:
        report: The run's report.
        tree: The calibrated lattice, from part 1.
        oas: The option-adjusted spread of the callable, from part 4.
        straight: The option-free value of the 6.5% bond, from part 2.
        putable: The putable value, from part 3.
    """
    print(
        "== part 5: effective, one-sided and key-rate durations and effective convexity (Handbook"
        " pp. 850-851)"
    )
    dr = 0.0025
    v0 = tree.value([6.5] * 4, spread=oas, call=100.0)
    vp, vm = value_shifted(dr, oas), value_shifted(-dr, oas)
    d_eff = (vm - vp) / (2 * v0 * dr)
    c_eff = (vm + vp - 2 * v0) / (v0 * dr**2)  # compendium convention: dP/P ~ -D dr + C dr^2 / 2
    report.ok(
        "callable at constant OAS: V+ = 101.621, V- = 102.765, effective duration 2.24",
        bool(abs(vp - 101.621) < 1e-3 and abs(vm - 102.765) < 1e-3 and abs(d_eff - 2.24) < 0.005),
        f"{vp:.4f} {vm:.4f} D {d_eff:.4f}",
    )
    report.ok(
        "callable effective convexity -77.149899 in the compendium convention (V0 dr^2); the"
        " Handbook"
        " divides by 2 V0 dr^2 and prints -39.1 from rounded prices, -38.574949 unrounded",
        bool(
            abs(c_eff + 77.149899) < 1e-6
            and close(c_eff / 2, (vm + vp - 2 * v0) / (2 * v0 * dr**2), 1e-12)
            and abs(c_eff / 2 + 38.574949) < 1e-6
            and abs((102.765 + 101.621 - 2 * 102.218) / (2 * 102.218 * dr**2) + 39.1) < 0.05
        ),
        f"{c_eff:.6f}",
    )
    d_down = (vm - v0) / (v0 * dr)
    d_up = (v0 - vp) / (v0 * dr)
    report.ok(
        "one-sided durations: the callable is less sensitive to falling rates (capped by the call)"
        " than to rising rates",
        bool(d_down < d_up),
        f"down {d_down:.3f}, up {d_up:.3f}",
    )
    oas_s = brentq(lambda s: tree.value([6.5] * 4, spread=s) - straight, -0.01, 0.01)
    sp_ = value_shifted(dr, 0.0, "straight")
    sm_ = value_shifted(-dr, 0.0, "straight")
    d_str = (sm_ - sp_) / (2 * straight * dr)
    c_str = (sm_ + sp_ - 2 * straight) / (straight * dr**2)
    oas_p = brentq(lambda s: tree.value([6.5] * 4, spread=s, put=100.0) - putable, -0.01, 0.01)
    pp_ = value_shifted(dr, oas_p, "put")
    pm_ = value_shifted(-dr, oas_p, "put")
    d_put = (pm_ - pp_) / (2 * putable * dr)
    c_put = (pm_ + pp_ - 2 * putable) / (putable * dr**2)
    report.ok(
        "durations: callable 2.24 < putable < straight; convexity: callable negative, straight and"
        " putable positive",
        bool(abs(oas_s) < 1e-9 and d_eff < d_put < d_str and c_eff < 0 < c_str and c_put > 0),
        f"straight D {d_str:.3f} C {c_str:.2f}; putable D {d_put:.3f} C {c_put:.2f}",
    )
    report.ok(
        "callable: with C = -77.15, -D dr + C dr^2/2 reproduces V+ and V- exactly at the measuring"
        " shift; the half-scaled -38.57 in the same formula misses each by C dr^2 / 4",
        close(-d_eff * dr + 0.5 * c_eff * dr**2, vp / v0 - 1, 1e-12)
        and close(d_eff * dr + 0.5 * c_eff * dr**2, vm / v0 - 1, 1e-12)
        and close(
            (-d_eff * dr + 0.25 * c_eff * dr**2) - (vp / v0 - 1), -0.25 * c_eff * dr**2, 1e-12
        ),
    )
    for sh in (0.005, -0.005):
        full = value_shifted(sh, 0.0, "straight") / straight - 1
        approx = -d_str * sh + 0.5 * c_str * sh**2
        approx_half = -d_str * sh + 0.25 * c_str * sh**2
        report.ok(
            f"straight bond, {sh * 1e4:+.0f} bp (twice the measuring shift, option-free so smooth):"
            f" -D dr + C dr^2/2 with C = {c_str:.2f} is within 0.5 bp of full revaluation and"
            " closer"
            " than with the half-scaled figure",
            abs(approx - full) < 5e-5 and abs(approx - full) < abs(approx_half - full),
            f"full {full:.6%}, approx {approx:.6%}, half-scaled {approx_half:.6%}",
        )
    krd = [
        (value_shifted(-dr, oas, key=k) - value_shifted(dr, oas, key=k)) / (2 * v0 * dr)
        for k in range(4)
    ]
    report.ok(
        "callable key-rate durations (par-rate shifts of 25 bp, recalibrated) are 0.443 / 0.143 /"
        " 0.166 / 1.539 and sum to 2.290, near but not equal to the 2.239 effective duration:"
        " single-rate"
        " shifts change exercise decisions",
        bool(abs(sum(krd) - 2.290) < 1e-3 and 0 < sum(krd) - d_eff < 0.06),
        " ".join(f"{x:.3f}" for x in krd),
    )
    krd_s = [
        (value_shifted(-dr, 0.0, "straight", key=k) - value_shifted(dr, 0.0, "straight", key=k))
        / (2 * straight * dr)
        for k in range(4)
    ]
    report.ok(
        "the straight bond's key-rate durations sum to its effective duration (3.517) within 0.005"
        " and sit at the four-year key rate; the callable's move toward shorter key rates",
        bool(
            abs(sum(krd_s) - d_str) < 0.005
            and krd_s[3] > 0.9 * sum(krd_s)
            and krd[3] / sum(krd) < krd_s[3] / sum(krd_s)
        ),
        " ".join(f"{x:.3f}" for x in krd_s),
    )


def check_floaters(report: CheckReport, tree: LognormalTree) -> None:
    """Part 6: capped and floored floaters (FIA chap. 9, printed pp. 246-247).

    Args:
        report: The run's report.
        tree: The calibrated lattice, from part 1.
    """
    print("== part 6: capped and floored floaters (FIA chap. 9, printed pp. 246-247)")
    flt = tree.value([], coupon_fn=lambda t, r: 100 * r)
    report.ok(
        "a floater paying the one-year rate in arrears is worth exactly 100 on the lattice",
        bool(abs(flt - 100) < 1e-12),
    )
    cap725 = tree.value([], coupon_fn=lambda t, r: 100 * min(r, 0.0725))
    cap775 = tree.value([], coupon_fn=lambda t, r: 100 * min(r, 0.0775))
    report.ok(
        "7.25% cap: 99.724; 7.75% cap: 99.858 (the higher the cap, the closer to par)",
        bool(abs(cap725 - 99.724) < 5e-4 and abs(cap775 - 99.858) < 5e-4),
        f"{cap725:.4f} {cap775:.4f}",
    )

    def cap_value(strike: float) -> float:
        """Return the value of the cap alone: payoffs 100 * max(r - K, 0), paid a period later."""
        return tree.value([0, 0, 0, 0], coupon_fn=lambda t, r: 100 * max(r - strike, 0.0), face=0.0)

    report.ok(
        "capped floater = floater - cap: 100 - 0.276 = 99.724 (cap valued separately)",
        bool(abs(100 - cap_value(0.0725) - cap725) < 1e-9),
    )
    floor45 = tree.value([], coupon_fn=lambda t, r: 100 * max(r, 0.045))
    floor_alone = tree.value(
        [0, 0, 0, 0], coupon_fn=lambda t, r: 100 * max(0.045 - r, 0.0), face=0.0
    )
    report.ok(
        "a 4.5% floor raises the floater to 100.992; floored floater = floater + floor",
        bool(abs(floor45 - 100.992) < 5e-4 and abs(100 + floor_alone - floor45) < 1e-9),
        f"{floor45:.4f}",
    )
    collar = tree.value([], coupon_fn=lambda t, r: 100 * min(max(r, 0.045), 0.0725))
    report.ok(
        "a collared floater (4.5% floor, 7.25% cap) = 100 + floor - cap",
        bool(abs(collar - (100 + floor_alone - cap_value(0.0725))) < 1e-9),
        f"{collar:.4f}",
    )


def check_paths(
    report: CheckReport, tree: LognormalTree, dfs: list[float], spots: list[float], pv_tree: float
) -> None:
    """Part 7: Monte Carlo paths of the lattice, a path-dependent note, Vasicek and Ho-Lee.

    Args:
        report: The run's report.
        tree: The calibrated lattice, from part 1.
        dfs: The discount factors of part 2.
        spots: The spot rates of part 2.
        pv_tree: The lattice value of the 6.5% bond, from part 2.
    """
    print("== part 7: term-structure models and Monte Carlo paths")
    rng = np.random.default_rng(SEED)
    n_paths = 200_000
    ups = rng.integers(0, 2, size=(n_paths, 3)).cumsum(axis=1)
    rates = np.column_stack(
        [np.full(n_paths, tree.lows[0])]
        + [tree.lows[t + 1] * np.exp(2 * tree.sigma * ups[:, t]) for t in range(3)]
    )
    disc = np.cumprod(1 / (1 + rates), axis=1)
    mc = disc @ np.array(CF)
    report.ok(
        "Monte Carlo over 200,000 sampled lattice paths reprices the 6.5% bond within 3 standard"
        " errors",
        abs(mc.mean() - pv_tree) < 3 * mc.std(ddof=1) / math.sqrt(n_paths),
        f"{mc.mean():.4f} se {mc.std(ddof=1) / math.sqrt(n_paths):.4f}",
    )
    # a path-dependent note: pays 6.5% but is redeemed at par at the end of the first year in which
    # the one-year rate has been below 4.75% for two consecutive years (a lookback
    # prepayment-style rule a recombining tree cannot hold)
    pv_pd = np.zeros(n_paths)
    alive = np.ones(n_paths, bool)
    below_prev = np.zeros(n_paths, bool)
    for t in range(4):
        below = rates[:, t] < 0.0475
        redeem = alive & below & below_prev if t >= 1 else np.zeros(n_paths, bool)
        pay = np.where(alive, 6.5, 0.0) + np.where(redeem | (alive & (t == 3)), 100.0, 0.0)
        pv_pd += pay * disc[:, t]
        alive &= ~redeem
        below_prev = below
    exact_pd = 0.0
    for path in itertools.product([0, 1], repeat=3):
        rr = [tree.lows[0]] + [tree.rate(t + 1, sum(path[: t + 1])) for t in range(3)]
        dd = np.cumprod([1 / (1 + r) for r in rr])
        a, bp, v = True, False, 0.0
        for t in range(4):
            b = rr[t] < 0.0475
            red = a and b and bp and t >= 1
            v += ((6.5 if a else 0.0) + (100.0 if (red or (a and t == 3)) else 0.0)) * dd[t]
            a = a and not red
            bp = b
        exact_pd += v / 8
    report.ok(
        "path-dependent note: Monte Carlo agrees with the exact eight-path average within 3"
        " standard"
        " errors",
        bool(
            abs(pv_pd.mean() - exact_pd) < 3 * pv_pd.std(ddof=1) / math.sqrt(n_paths)
            and exact_pd < pv_tree
        ),
        f"exact {exact_pd:.4f}",
    )
    # Vasicek: closed form against simulation, and Hull's Example 31.1
    a_v, b_v, s_v, r0 = 0.1, 0.05, 0.01, 0.04

    def vasicek_p(T: float) -> float:
        B = (1 - math.exp(-a_v * T)) / a_v
        A = math.exp((B - T) * (a_v**2 * b_v - s_v**2 / 2) / a_v**2 - s_v**2 * B**2 / (4 * a_v))
        return A * math.exp(-B * r0)

    report.ok(
        "Hull Example 31.1: Vasicek B(0,4) with a = 0.1 is 3.30",
        abs((1 - math.exp(-0.4)) / 0.1 - 3.297) < 5e-4,
    )
    steps, T_v, n_v = 400, 4.0, 40_000
    dt = T_v / steps
    r = np.full(n_v, r0)
    integral = np.zeros(n_v)
    for _ in range(steps):
        r_next = r + a_v * (b_v - r) * dt + s_v * math.sqrt(dt) * rng.standard_normal(n_v)
        integral += 0.5 * (r + r_next) * dt
        r = r_next
    p_mc = np.exp(-integral)
    report.ok(
        "Vasicek four-year zero price: closed form within 3 standard errors of 40,000 simulated"
        " paths",
        abs(p_mc.mean() - vasicek_p(T_v)) < 3 * p_mc.std(ddof=1) / math.sqrt(n_v),
        f"{vasicek_p(T_v):.6f} vs {p_mc.mean():.6f}",
    )
    report.ok(
        "the equilibrium Vasicek curve does not reproduce an arbitrary observed curve: its"
        " four-year"
        " zero rate differs from the bootstrapped 5.27%",
        abs(-math.log(vasicek_p(4.0)) / 4 - math.log(1 + spots[3])) > 1e-3,
    )
    # Ho-Lee as a lattice: normal rates r(t, i) = a_t + sigma (2i - t) per annual period,
    # probability
    # 1/2. The drift a_t is solved by forward induction on Arrow-Debreu prices so that each
    # zero-coupon bond reprices; an independent backward induction then checks every discount
    # factor. A no-arbitrage model takes today's curve as an input.
    s_hl = 0.01
    a_hl: list[float] = []
    Q = np.array([1.0])
    for t in range(4):
        offs = s_hl * (2 * np.arange(t + 1) - t)

        def ad_gap(a: float) -> float:
            return float(np.sum(Q / (1 + a + offs))) - dfs[t]

        a_t = brentq(ad_gap, -0.5, 0.5)
        a_hl.append(a_t)
        disc_t = Q / (1 + a_t + offs)
        Q = np.zeros(t + 2)
        Q[:-1] += 0.5 * disc_t
        Q[1:] += 0.5 * disc_t

    def ho_lee_zero(T: int) -> float:
        v = np.ones(T + 1)
        for t in range(T - 1, -1, -1):
            offs = s_hl * (2 * np.arange(t + 1) - t)
            v = 0.5 * (v[1:] + v[:-1]) / (1 + a_hl[t] + offs)
        root: np.float64 = v[0]
        return root

    report.ok(
        "Ho-Lee lattice calibrated by forward induction reprices all four zero-coupon bonds by"
        " backward induction",
        all(abs(ho_lee_zero(T) - dfs[T - 1]) < 1e-12 for T in range(1, 5)),
        " ".join(f"{a:.5f}" for a in a_hl),
    )
    fwd_simple = [1 / dfs[0] - 1] + [dfs[k - 1] / dfs[k] - 1 for k in range(1, 4)]
    report.ok(
        "its central rates a_t lie above the one-year forward rates (3.500 / 4.935 / 5.784 / 6.893"
        " percent): the drift includes a convexity adjustment, zero in the first period",
        abs(a_hl[0] - fwd_simple[0]) < 1e-12
        and all(a > f for a, f in zip(a_hl[1:], fwd_simple[1:], strict=True))
        and all(
            abs(f - g) < 5e-5
            for f, g in zip(fwd_simple, [0.035, 0.04935, 0.05784, 0.06893], strict=True)
        ),
        " ".join(f"{f:.5f}" for f in fwd_simple),
    )


def check_convertible(report: CheckReport) -> None:
    """Part 8: a convertible bond with default risk on a three-step stock tree (Hull sec. 27.4).

    Args:
        report: The run's report.
    """
    print("== part 8: convertible bonds")
    # Hull sec. 27.4: nine-month zero-coupon convertible into 2 shares, callable at 113, stock 50,
    # vol 30%, hazard 1%, r 5%, recovery 40 on default, three quarterly steps
    dt_c, s0, vol, lam, rr_, conv, callp, rec = 0.25, 50.0, 0.30, 0.01, 0.05, 2.0, 113.0, 40.0
    u = math.exp(vol * math.sqrt(dt_c))
    d = 1 / u
    a_c = math.exp(rr_ * dt_c)
    pu = (a_c - d * math.exp(-lam * dt_c)) / (u - d)
    pd = (u * math.exp(-lam * dt_c) - a_c) / (u - d)
    pdef = 1 - math.exp(-lam * dt_c)
    report.ok(
        "Hull: u 1.1618, d 0.8607, pu 0.5115, pd 0.4860, default 0.0025",
        abs(u - 1.1618) < 5e-5
        and abs(d - 0.8607) < 5e-5
        and abs(pu - 0.5115) < 5e-5
        and abs(pd - 0.4860) < 5e-5
        and abs(pdef - 0.0025) < 5e-5,
    )

    def convertible(n: int = 3, s0: float = s0, callp: float = callp) -> float:
        v = [max(100.0, conv * s0 * u**j * d ** (n - j)) for j in range(n + 1)]
        for t in range(n - 1, -1, -1):
            nv = []
            for j in range(t + 1):
                s = s0 * u**j * d ** (t - j)
                hold = (pu * v[j + 1] + pd * v[j] + pdef * rec) * math.exp(-rr_ * dt_c)
                val = max(hold, conv * s)
                if (
                    val > callp
                ):  # issuer calls; the holder then converts if that is worth more than the call
                    # price
                    val = max(callp, conv * s)
                nv.append(val)
            v = nv
        return v[0]

    cb = convertible()
    report.ok("Hull's convertible is worth 107.44", abs(cb - 107.44) < 5e-3, f"{cb:.4f}")
    straight_c = 100 * math.exp(-rr_ * 0.75) * (math.exp(-lam * 0.75)) + rec * (
        1 - math.exp(-lam * 0.75)
    ) * math.exp(-rr_ * 0.375)
    report.ok(
        "convertible above both its straight value and its conversion value (minimum value = max of"
        " the two)",
        cb > max(straight_c, conv * s0),
    )
    # Handbook chap. 38 traditional measures
    cp_ = 1100 / (23 * 40) - 1
    report.ok(
        "Handbook p. 890: conversion premium 19.57%, points premium 18.00, investment premium"
        " 27.17%",
        abs(cp_ - 0.1957) < 5e-5
        and abs((1100 - 23 * 40) / 10 - 18.0) < 1e-12
        and abs(1100 / 865 - 1 - 0.2717) < 5e-5,
    )
    report.ok(
        "Handbook p. 885: conversion price 243 x 1.275 = 309.825 and ratio 1000/309.825 = 3.2276"
        " (text prints 309.63)",
        abs(243 * 1.275 - 309.825) < 1e-9
        and abs(1000 / 309.825 - 3.2276) < 5e-5
        and abs(1000 / 309.63 - 3.2297) < 5e-5,
    )
    # scenario returns: stock up / down 30% immediately; convertible re-valued on the same tree
    up_, dn_ = convertible(s0=65.0), convertible(s0=35.0)
    ret_cb = (up_ / cb - 1, dn_ / cb - 1)
    report.ok(
        "stock +30%: convertible gains less than the stock; stock -30%: it falls much less,"
        " cushioned by the bond floor",
        0 < ret_cb[0] < 0.30 and -0.30 < ret_cb[1] < 0 and abs(ret_cb[1]) < 0.5 * 0.30,
        f"+{ret_cb[0]:.3%} / {ret_cb[1]:.3%}",
    )
    delta_cb = (convertible(s0=50.5) - convertible(s0=49.5)) / (1.0 * conv)
    report.ok(
        "the convertible's delta per share of conversion lies between 0 and 1",
        0 < delta_cb < 1,
        f"{delta_cb:.3f}",
    )


def main() -> int:
    """Print the versions, then run the eight parts with one report.

    The worked numbers of meth:arbitrage-free-bond-valuation, meth:binomial-rate-tree-calibration,
    mod:term-structure-models-simulation, meth:callable-putable-bond-valuation,
    meth:option-adjusted-spread, meth:embedded-option-effective-duration,
    meth:capped-floored-floater-valuation and meth:convertible-bond-valuation.

    Reproduced:
    - Fabozzi (ed.), Handbook of Fixed Income Securities, 9th ed. (2021), chap. 36 (Fabozzi,
      Kalotay and Dorigan): a lognormal binomial tree with 10% volatility calibrated to par yields
      3.5, 4.2, 4.7 and 5.2 percent; the 6.5% four-year option-free bond (104.643), callable
      (102.899) and putable (105.327) at par after year 1, step-up notes (102.082, 100.031), OAS of
      35 bp at a price of 102.218, and V+ = 101.621 / V- = 102.765 for a 25 bp curve shift.
    - Fabozzi, Fixed Income Analysis, 2nd ed. (2007), chap. 9, on the same tree: capped floater
      99.724 (7.25% cap) and 99.858 (7.75% cap).
    - Hull, Options, Futures, and Other Derivatives, 11th Global ed. (2022), sec. 27.4: a
      nine-month zero-coupon convertible on a stock tree with default (107.44); sec. 31.2, Example
      31.1 (Vasicek B(0,4) = 3.30).
    - Handbook chap. 38 (Bhattacharya), p. 890: conversion premium 19.57%, points premium 18.00,
      investment premium 27.17%.

    Original checks: spot-curve repricing against the lattice, pathwise valuation over all eight
    paths, volatility and curve-shape effects, one-sided and key-rate durations, a floored floater,
    a Monte Carlo path sample of the lattice and a path-dependent note it can value, Vasicek closed
    form against simulation, a Ho-Lee drift that fits the curve, and convertible scenario returns
    against a straight bond and the stock.

    Convexity is (V+ + V- - 2V0)/(V0 dr^2), the compendium convention, with dP/P ~ -D dr + C dr^2/2;
    the Handbook's half-scaled figure is reported beside it. Conventions: annual periods, cash
    flows at period ends, risk-neutral probability 1/2 on each branch, prices per 100.

    Count convention: one check is one executed ok() call (a call inside a loop counts once per
    iteration). One generator, seeded 20261019, serves part 7 alone: its path sample is drawn first
    and the Vasicek simulation continues from it.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    tree = check_calibration(report)
    dfs, spots, straight = check_option_free(report, tree)
    callable_, putable, tree20 = check_callable(report, tree, straight)
    oas = check_oas(report, tree, tree20, spots, callable_)
    check_durations(report, tree, oas, straight, putable)
    check_floaters(report, tree)
    check_paths(report, tree, dfs, spots, straight)
    check_convertible(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
