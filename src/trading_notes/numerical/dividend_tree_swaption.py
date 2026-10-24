"""Known dividends in a binomial tree, and the receiver swaption behind a callable bond.

Library gap-filling Batch L2, decision L2-D5 (2026-10-21): the two optional Hull extensions.

Part 1, meth:multi-period-binomial-valuation: known dollar dividends in a recombining tree
(Hull, Options, Futures, and Other Derivatives, 11th Global ed., sec. 21.3): the tree models
S* = S - PV(dividends) and adds the dividend's present value back at nodes before the
ex-dividend date. Example 21.5 is reproduced (4.44 with 5 steps; 4.208 and 4.214 with 50 and
100). Hull's early-exercise condition for an American call (sec. 15.12, eqs. (15.23)-(15.25)):
exercise just before the last ex-dividend date can be optimal only if
D_n > K(1 - exp(-r(T - t_n))). Original inputs test both sides.

Part 2, meth:black-model-rates-currencies: the receiver swaption (eq. (29.11)), payer-receiver
parity (Problem 29.18) and the callable bond as a straight bond less a receiver swaption
(Business Snapshot 29.2). Example 29.4's inputs are reused. The payoff identity
B_T - L = L A_T (s_K - s_T) is checked on 1,000 random curves at the exercise date (seed
20261121).

Run: uv run --frozen --no-editable python -m trading_notes.numerical.dividend_tree_swaption
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys
from collections.abc import Sequence
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

SEED: Final = 20261121
N = stats.norm.cdf


def dividend_tree(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    steps: int,
    divs: Sequence[tuple[float, float]],
    call: bool,
    american: bool = True,
    exercise_log: list[float] | None = None,
) -> float:
    """Hull sec. 21.3: CRR tree on S* = S - PV(dividends), dividends added back before ex-dates.

    Args:
        S0: The stock price.
        K: The strike.
        r: The continuously compounded rate.
        sigma: The volatility of S*.
        T: The maturity in years.
        steps: The number of tree steps.
        divs: Each dividend as (ex-dividend time, amount); those after T are ignored.
        call: A call if true, else a put.
        american: Whether early exercise is allowed.
        exercise_log: If given, receives the time of each step at which some node exercises.
    """
    dt = T / steps
    pv0 = sum(D * math.exp(-r * t) for t, D in divs if t <= T)
    s_star0 = S0 - pv0
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)

    def stock(i: int) -> Floats:
        t = i * dt
        pv = sum(D * math.exp(-r * (td - t)) for td, D in divs if t < td <= T)
        nodes: Floats = s_star0 * u ** np.arange(i, -1, -1) * d ** np.arange(0, i + 1) + pv
        return nodes

    def payoff(s: Floats) -> Floats:
        return np.maximum(s - K, 0) if call else np.maximum(K - s, 0)

    v = payoff(stock(steps))
    for i in range(steps - 1, -1, -1):
        v = disc * (p * v[:-1] + (1 - p) * v[1:])
        if american:
            ex = payoff(stock(i))
            if exercise_log is not None and np.any(ex > v):
                exercise_log.append(i * dt)
            v = np.maximum(v, ex)
    return float(v[0])


def bsm_call(s: float, k: float, tau: float, r: float, sig: float) -> float:
    """Return the BSM call on a non-dividend stock s, strike k, maturity tau."""
    d1 = (math.log(s / k) + (r + sig**2 / 2) * tau) / (sig * math.sqrt(tau))
    return s * N(d1) - k * math.exp(-r * tau) * N(d1 - sig * math.sqrt(tau))


def check_dividend_tree(report: CheckReport) -> None:
    """Part 1: Example 21.5, and Hull's early-exercise bound on both sides."""
    print("== Part 1: known dollar dividends in a tree (Hull sec. 21.3)")
    vals = {
        n: dividend_tree(
            S0=52.0,
            K=50.0,
            r=0.10,
            sigma=0.40,
            T=5 / 12,
            steps=n,
            divs=[(3.5 / 12, 2.06)],
            call=False,
        )
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
        am = dividend_tree(S0, K, r, sig, T, steps, [(t_ex, D)], call=True, exercise_log=log)
        eu = dividend_tree(S0, K, r, sig, T, steps, [(t_ex, D)], call=True, american=False)
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
            black = max(bsm_call(S0 - pv, K, T, r, sig), bsm_call(S0, K, t_ex, r, sig))
            print(
                f"  (reported) Black's approximation (Hull p. 363): max of European to T and to"
                f" t_n = {black:.4f}; it puts"
                " the 25% volatility on the whole stock price for the t_n leg, while the tree"
                " puts it on S* (Hull p. 360,"
                " n. 13), so the two are different models and the approximation can exceed the"
                " tree's American value"
            )


def check_swaptions(report: CheckReport, rng: np.random.Generator) -> None:
    """Part 2: Example 29.4, payer-receiver parity and the callable bond's payoff identity."""
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

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_dividend_tree(report)
    check_swaptions(report, np.random.default_rng(SEED))
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
