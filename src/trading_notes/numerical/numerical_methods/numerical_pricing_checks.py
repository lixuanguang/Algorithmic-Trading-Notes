"""Checks of finite-difference option pricing and least-squares Monte Carlo against BSM."""

import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray

from trading_notes.numerical.numerical_methods.least_squares_monte_carlo import (
    LongstaffSchwartz,
    quadratic_basis,
)
from trading_notes.numerical.numerical_methods.put_pricing import FiniteDifferenceGrid, PutOption
from trading_notes.numerical.report import CheckReport, print_versions

type Floats = NDArray[np.float64]

PUT: Final = PutOption(
    strike=100.0, rate=0.05, dividend_yield=0.0, vol=0.20, maturity=1.0, spot=100.0
)
GRID: Final = FiniteDifferenceGrid(option=PUT, s_max=3 * PUT.strike)
SEED_FIT: Final = 20261021  # paths that fit the exercise policy
SEED_VALUE: Final = 20261022  # fresh paths that value it
N_EX: Final = 50  # Bermudan exercise dates


def scaled_basis(s: Floats) -> Floats:
    """Return the regressors 1, S/K, (S/K)^2 of the Bermudan example."""
    return quadratic_basis(s / PUT.strike)


def check_european(report: CheckReport) -> float:
    """The European put: Crank-Nicolson's order, and the explicit scheme's stability bound."""
    sg, r = PUT.vol, PUT.rate
    print("== European put by finite differences")
    ref = PUT.black_scholes()
    report.ok("BSM put 5.5735", abs(ref - 5.573526) < 1e-6, f"{ref:.6f}")
    cn = {M: GRID.crank_nicolson(M, M // 2).at(PUT.spot) for M in (150, 300)}
    e150, e300 = abs(cn[150] - ref), abs(cn[300] - ref)
    report.ok(
        "Crank-Nicolson (150, 75) and (300, 150): error ratio in [3, 5] (second order)",
        3 <= e150 / e300 <= 5,
        f"errors {e150:.2e}, {e300:.2e}, ratio {e150 / e300:.2f}",
    )
    ex = {}
    for M in (150, 300):
        bound = 1 / (sg**2 * M**2 + r)
        N = math.ceil(PUT.maturity / bound)
        values, (A, B, C) = GRID.explicit(M, N)
        ex[M] = values.at(PUT.spot)
        report.ok(
            f"explicit at I = {M}, N = {N} (dt just inside 1/(sigma^2 I^2 + r)): all coefficients"
            " >= 0",
            bool(min(A.min(), B.min(), C.min()) >= 0 and PUT.maturity / N <= bound),
        )
    _, _, _, up = GRID.coefficients(150)
    report.ok("sigma^2 < r here, so node i = 1 alone is upwinded", list(np.where(up)[0] + 1) == [1])
    x150, x300 = abs(ex[150] - ref), abs(ex[300] - ref)
    report.ok(
        "explicit error ratio in [3, 5] with dt proportional to dS^2",
        3 <= x150 / x300 <= 5,
        f"errors {x150:.2e}, {x300:.2e}, ratio {x150 / x300:.2f}",
    )
    unstable, (A, B, C) = GRID.explicit(150, 200)
    Vbad = unstable.values
    report.ok(
        "explicit at I = 150, N = 200 (dt = 4.5 times the bound): B < 0 and |V| > 1e6",
        bool(B.min() < 0 and np.abs(Vbad).max() > 1e6),
        f"max |V| {np.abs(Vbad).max():.2e}",
    )
    return ref


def check_american(report: CheckReport, ref: float) -> float:
    """The American put: CRR reference, Crank-Nicolson with PSOR, and projected explicit."""
    print("== American put")
    t8000, t8001 = PUT.crr_value(8000), PUT.crr_value(8001)
    amer = 0.5 * (t8000 + t8001)
    report.ok(
        "reference 6.0904: mean of CRR trees with 8,000 and 8,001 steps",
        abs(amer - 6.0904) < 5e-5,
        f"{t8000:.5f}, {t8001:.5f}, mean {amer:.5f}",
    )
    am = {M: GRID.crank_nicolson(M, M // 2, american=True).at(PUT.spot) for M in (150, 300)}
    a150, a300 = abs(am[150] - amer), abs(am[300] - amer)
    report.ok(
        "Crank-Nicolson with projected SOR (omega 1.5, tol 1e-9) at I = 300 within 4e-3 of the"
        " reference",
        a300 <= 4e-3,
        f"{am[150]:.4f} at I = 150, {am[300]:.4f} at I = 300",
    )
    report.ok(
        "error ratio from I = 150 to I = 300 in [3, 5]", 3 <= a150 / a300 <= 5, f"{a150 / a300:.2f}"
    )
    projected = GRID.explicit(150, 901, american=True)[0].at(PUT.spot)
    report.ok(
        "explicit with projection (I = 150, N = 901) is also close (within 0.02)",
        abs(projected - amer) < 0.02,
        f"{projected:.4f}",
    )
    report.ok(
        "early-exercise premium over the European put is about 0.52", 0.50 < amer - ref < 0.54
    )
    return amer


def check_hull_paths(report: CheckReport) -> None:
    """Least-squares Monte Carlo on Hull's eight paths (Table 27.4)."""
    print("== Least-squares Monte Carlo: Hull's eight paths (Table 27.4)")
    paths = np.array(
        [
            [1.09, 1.08, 1.34],
            [1.16, 1.26, 1.54],
            [1.22, 1.07, 1.03],
            [0.93, 0.97, 0.92],
            [1.11, 1.56, 1.52],
            [0.76, 0.77, 0.90],
            [0.92, 0.84, 1.01],
            [0.88, 1.22, 1.34],
        ]
    )
    hull_disc, hull_beta = LongstaffSchwartz(
        strike=1.10, rate=0.06, dt=1.0, basis=quadratic_basis
    ).fit(paths)
    report.ok(
        "value 0.1144 (Hull p. 663)",
        bool(abs(hull_disc.mean() - 0.1144) < 5e-5),
        f"{hull_disc.mean():.5f}",
    )
    # Hull prints c = -1.813 at year 2; the least-squares value is -1.81358, so the printed figure
    # is truncated rather than rounded. The comparison therefore allows one unit in the third
    # decimal.
    report.ok(
        "regressions -1.070 + 2.983 S - 1.813 S^2 at year 2, 2.038 - 3.335 S + 1.356 S^2 at year 1"
        " (to 1e-3)",
        np.allclose(hull_beta[1], [-1.070, 2.983, -1.813], atol=1e-3)
        and np.allclose(hull_beta[0], [2.038, -3.335, 1.356], atol=1e-3),
        f"year 2 c = {hull_beta[1][2]:.5f}",
    )


def check_bermudan(report: CheckReport, ref: float, amer: float) -> None:
    """The Bermudan put by trees, Crank-Nicolson and LSM fitted and valued on separate paths."""
    print("== Least-squares Monte Carlo: Bermudan put with 50 exercise dates")
    tree5000, tree5050 = PUT.crr_value(5000, False, 100), PUT.crr_value(5050, False, 101)
    berm = 0.5 * (tree5000 + tree5050)
    report.ok(
        "tree reference: CRR 5,000 and 5,050 steps, exercise only at t_j = j/50",
        abs(tree5000 - tree5050) < 2e-3,
        f"{tree5000:.5f}, {tree5050:.5f}, mean {berm:.5f}",
    )
    cn_berm = GRID.crank_nicolson(600, 1000, exercise_steps=set(range(20, 1001, 20))).at(PUT.spot)
    report.ok(
        "Crank-Nicolson (600, 1,000) with projection only at the 50 dates within 5e-3 of the trees",
        abs(cn_berm - berm) <= 5e-3,
        f"{cn_berm:.5f}",
    )
    report.ok("Bermudan lies between the European and American values", ref < berm < amer)
    lsm = LongstaffSchwartz(
        strike=PUT.strike, rate=PUT.rate, dt=PUT.maturity / N_EX, basis=scaled_basis
    )
    fit_paths = PUT.price_paths(np.random.default_rng(SEED_FIT), 100_000, N_EX)
    in_sample, policy = lsm.fit(fit_paths)
    val_paths = PUT.price_paths(np.random.default_rng(SEED_VALUE), 100_000, N_EX)
    out_sample = lsm.value(val_paths, policy)
    est, se = out_sample.mean(), out_sample.std(ddof=1) / math.sqrt(len(out_sample))
    report.ok(
        "policy fitted on 100,000 paths (seed 20261021), valued on 100,000 fresh paths (seed"
        " 20261022): "
        "reference - 0.05 <= estimate <= reference + 3 s.e.",
        bool(berm - 0.05 <= est <= berm + 3 * se),
        f"{est:.4f} (s.e. {se:.4f}) against {berm:.4f}",
    )
    print(
        f"  in-sample estimate on the fitting paths {in_sample.mean():.4f} (reported, not tested)"
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    The worked examples of meth:finite-difference-option-pricing and
    meth:least-squares-monte-carlo. Inputs: K = 100, r = 5 percent, q = 0, sigma = 20 percent,
    T = 1, value read at S = 100, a grid node; S_max = 3K. Acceptance ranges, seeds (20261021,
    20261022) and path counts were fixed before any run and are not tuned. Synthetic model
    data only: the checks show that the schemes are implemented correctly under
    Black-Scholes-Merton; they are not evidence about markets. About 30 seconds.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    ref = check_european(report)
    amer = check_american(report, ref)
    check_hull_paths(report)
    check_bermudan(report, ref, amer)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
