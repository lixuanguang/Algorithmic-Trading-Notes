"""Lookback options: Hull's and Wilmott's closed forms, seasoned simulation and monitoring bias."""

import itertools
import math
import sys
from collections.abc import Callable
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.exotic_options.lookback import LookbackModel
from trading_notes.numerical.records import Record
from trading_notes.numerical.report import CheckReport, print_versions

type Floats = NDArray[np.float64]
# A floating-strike price: (S, recorded extreme, tau) -> value.
type Floating = Callable[[float, float, float], float]

N = stats.norm.cdf
S0: Final = 50.0  # Hull Example 26.2
SIG: Final = 0.4
R: Final = 0.10
Q: Final = 0.0
T: Final = 0.25
X0: Final = math.log(S0)
DISC: Final = math.exp(-R * T)
HULL: Final = LookbackModel(rate=R, dividend=Q, vol=SIG)


class WilmottLookback(Record):
    """Wilmott's lookback closed forms (PWOQF 2nd ed., sec. 26.6), an independent transcription.

    Attributes:
        rate: Risk-free rate r.
        dividend: Dividend yield D, different from r.
        vol: Volatility sigma.
    """

    rate: float
    dividend: float
    vol: float

    def _terms(self, S: float, M: float, tau: float) -> tuple[float, float, float, float, float]:
        r, D, sig = self.rate, self.dividend, self.vol
        st = sig * math.sqrt(tau)
        d1 = (math.log(S / M) + (r - D + sig**2 / 2) * tau) / st
        return (
            d1,
            d1 - st,
            sig**2 / (2 * (r - D)),
            (S / M) ** (-2 * (r - D) / sig**2),
            2 * (r - D) * math.sqrt(tau) / sig,
        )

    def floating_call(self, S: float, M: float, tau: float) -> float:
        """Return the floating-strike call on the minimum M to date."""
        r, D = self.rate, self.dividend
        d1, d2, w, pw, sh = self._terms(S, M, tau)
        return float(
            S * math.exp(-D * tau) * N(d1)
            - M * math.exp(-r * tau) * N(d2)
            + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
        )

    def floating_put(self, S: float, M: float, tau: float) -> float:
        """Return the floating-strike put on the maximum M to date."""
        r, D = self.rate, self.dividend
        d1, d2, w, pw, sh = self._terms(S, M, tau)
        return float(
            M * math.exp(-r * tau) * N(-d2)
            - S * math.exp(-D * tau) * N(-d1)
            + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
        )

    def fixed_call(self, S: float, M: float, E: float, tau: float) -> float:
        """Return the fixed-strike call on the maximum M to date (both strike cases)."""
        r, D = self.rate, self.dividend
        if E > M:
            d1, d2, w, pw, sh = self._terms(S, E, tau)
            return float(
                S * math.exp(-D * tau) * N(d1)
                - E * math.exp(-r * tau) * N(d2)
                + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
            )
        d1, d2, w, pw, sh = self._terms(S, M, tau)
        return float(
            (M - E) * math.exp(-r * tau)
            + S * math.exp(-D * tau) * N(d1)
            - M * math.exp(-r * tau) * N(d2)
            + S * math.exp(-r * tau) * w * (-pw * N(d1 - sh) + math.exp((r - D) * tau) * N(d1))
        )

    def fixed_put(self, S: float, M: float, E: float, tau: float) -> float:
        """Return the fixed-strike put on the minimum M to date (both strike cases)."""
        r, D = self.rate, self.dividend
        if E < M:
            d1, d2, w, pw, sh = self._terms(S, E, tau)
            return float(
                E * math.exp(-r * tau) * N(-d2)
                - S * math.exp(-D * tau) * N(-d1)
                + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
            )
        d1, d2, w, pw, sh = self._terms(S, M, tau)
        return float(
            (E - M) * math.exp(-r * tau)
            - S * math.exp(-D * tau) * N(-d1)
            + M * math.exp(-r * tau) * N(-d2)
            + S * math.exp(-r * tau) * w * (pw * N(-d1 + sh) - math.exp((r - D) * tau) * N(-d1))
        )


def pde_residual(
    price: Floating,
    model: LookbackModel,
    S: float,
    M: float,
    tau: float,
    hS: float = 0.01,
    ht: float = 1e-5,
) -> float:
    """Return the pricing-equation residual of price at (S, M, tau) by central differences."""
    v = price(S, M, tau)
    vS = (price(S + hS, M, tau) - price(S - hS, M, tau)) / (2 * hS)
    vSS = (price(S + hS, M, tau) - 2 * v + price(S - hS, M, tau)) / hS**2
    vtau = (price(S, M, tau + ht) - price(S, M, tau - ht)) / (2 * ht)
    r, q, sig = model.rate, model.dividend, model.vol
    return -vtau + 0.5 * sig**2 * S**2 * vSS + (r - q) * S * vS - r * v


# ---------------------------------------------------------------- part 1
def check_closed_forms(report: CheckReport) -> tuple[float, float]:
    """Check Example 26.2, the two sources, the pricing equation and the boundary condition.

    Returns:
        The new-issue floating call and put of Example 26.2.
    """
    print("== part 1: Example 26.2, two sources, pricing equation, boundary condition, history")
    terms = HULL.floating_put_terms(S0, S0, T)
    put0, b1, b2, b3, Y2 = terms.value, terms.b1, terms.b2, terms.b3, terms.y2
    call0 = HULL.floating_call(S0, S0, T)
    report.ok(
        "Example 26.2 new-issue put rounds to 7.79 (S_max = S_0) and call to 8.04 (S_min = S_0)",
        round(put0, 2) == 7.79 and round(call0, 2) == 8.04,
        f"put {put0:.6f}, call {call0:.6f}",
    )
    report.ok(
        "printed intermediates b1 = -0.025, b2 = -0.225, b3 = 0.025 and Y2 = 0",
        abs(b1 + 0.025) <= 5e-4
        and abs(b2 + 0.225) <= 5e-4
        and abs(b3 - 0.025) <= 5e-4
        and abs(Y2) <= 1e-15,
        f"{b1:.6f}, {b2:.6f}, {b3:.6f}, {Y2:.1e}",
    )

    points = [
        (50.0, 0.25, 0.10, 0.00, 0.40),
        (50.0, 0.25, 0.10, 0.02, 0.40),
        (100.0, 1.00, 0.05, 0.02, 0.25),
    ]
    worst = 0.0
    for S, tau, rr, qq, ss in points:
        hull = LookbackModel(rate=rr, dividend=qq, vol=ss)
        wilmott = WilmottLookback(rate=rr, dividend=qq, vol=ss)
        for smin, smax in ((S, S), (0.9 * S, 1.12 * S)):
            pairs = [
                (
                    hull.floating_call(S, smin, tau),
                    wilmott.floating_call(S, smin, tau),
                ),
                (
                    hull.floating_put(S, smax, tau),
                    wilmott.floating_put(S, smax, tau),
                ),
            ]
            for K in (0.95 * smax, 1.1 * smax):
                pairs.append(
                    (
                        hull.fixed_call(S, smax, K, tau),
                        wilmott.fixed_call(S, smax, K, tau),
                    )
                )
            for K in (0.9 * smin, 1.05 * smin):
                pairs.append(
                    (
                        hull.fixed_put(S, smin, K, tau),
                        wilmott.fixed_put(S, smin, K, tau),
                    )
                )
            worst = max(worst, max(abs(a - b) / abs(b) for a, b in pairs))
    report.ok(
        "Hull and Wilmott agree: floating call and put, fixed call and put in both strike cases"
        " (6 points, q = 0 and 0.02)",
        worst <= 1e-12,
        f"largest relative difference {worst:.1e}",
    )

    # Central differences in S with hS = 0.01 leave a truncation error of order hS^2 (up to about
    # 4e-6 near the running extreme), so the 1e-6 bound applies to the Richardson-extrapolated
    # residual (4 R(0.01) - R(0.02)) / 3, which removes the hS^2 term.
    seasoned = LookbackModel(rate=0.10, dividend=0.02, vol=0.40)
    new_issue = LookbackModel(rate=0.10, dividend=0.00, vol=0.40)
    long_dated = LookbackModel(rate=0.05, dividend=0.02, vol=0.25)
    pts: list[tuple[Floating, LookbackModel, float, float, float]] = [
        (seasoned.floating_call, seasoned, 52.0, 45.0, 0.25),
        (new_issue.floating_call, new_issue, 50.0, 48.0, 0.10),
        (seasoned.floating_put, seasoned, 50.0, 56.0, 0.25),
        (long_dated.floating_put, long_dated, 95.0, 110.0, 1.00),
    ]
    raw = [pde_residual(*p) for p in pts]
    res = [(4 * pde_residual(*p, hS=0.01) - pde_residual(*p, hS=0.02)) / 3 for p in pts]
    print(f"    raw residuals at hS = 0.01: {', '.join(f'{x:.1e}' for x in raw)}")
    report.ok(
        "pricing-equation residual at interior points (S strictly inside the extreme), extrapolated"
        " in hS, <= 1e-6",
        max(abs(x) for x in res) <= 1e-6,
        f"largest {max(abs(x) for x in res):.1e}",
    )

    interior = (HULL.floating_call(50, 45 + 1e-3, T) - HULL.floating_call(50, 45 - 1e-3, T)) / 2e-3
    fd = {h: (call0 - HULL.floating_call(S0, S0 - h, T)) / h for h in (1e-2, 1e-3)}
    report.ok(
        "dV/dS_min = 0 on S = S_min: one-sided difference small against the interior derivative"
        " and linear in h",
        abs(fd[1e-3]) <= 1e-2 * abs(interior) and 5 <= fd[1e-2] / fd[1e-3] <= 20,
        f"interior dc/dS_min {interior:.5f}; at S = S_min {fd[1e-2]:.2e} (h = 0.01), "
        f"{fd[1e-3]:.2e} (h = 0.001)",
    )

    deep_c = HULL.floating_call(S0, 20.0, T) - (S0 * math.exp(-Q * T) - 20.0 * math.exp(-R * T))
    deep_p = HULL.floating_put(S0, 120.0, T) - (120.0 * math.exp(-R * T) - S0 * math.exp(-Q * T))
    report.ok(
        "deep-seasoned limits: S_min = 20 gives S e^{-q tau} - 20 e^{-r tau}, S_max = 120 gives"
        " 120 e^{-r tau} - S e^{-q tau}",
        0 <= deep_c <= 1e-4 and 0 <= deep_p <= 1e-4,
        f"excess {deep_c:.1e} and {deep_p:.1e}; values "
        f"{HULL.floating_call(S0, 20.0, T):.4f} and "
        f"{HULL.floating_put(S0, 120.0, T):.4f} against new issue {call0:.4f} and "
        f"{put0:.4f}",
    )
    cgrid = [HULL.floating_call(S0, m, T) for m in np.arange(20.0, 50.01, 2.5)]
    pgrid = [HULL.floating_put(S0, m, T) for m in np.arange(50.0, 120.01, 5.0)]
    report.ok(
        "c_fl strictly decreasing in S_min (20 to 50) and p_fl strictly increasing in S_max"
        " (50 to 120)",
        all(a > b for a, b in itertools.pairwise(cgrid))
        and all(a < b for a, b in itertools.pairwise(pgrid)),
    )
    return call0, put0


# ---------------------------------------------------------------- part 2
def check_seasoned(
    report: CheckReport, rng: np.random.Generator, call0: float, put0: float
) -> None:
    """Check seasoned contracts by exact simulation of the remaining life."""
    print(
        "== part 2: seasoned contracts by exact simulation of the remaining life"
        " (tau = 0.25, S = 50)"
    )
    n2 = 400_000
    z = rng.standard_normal(n2)
    u_min = 1.0 - rng.random(n2)
    u_max = 1.0 - rng.random(n2)
    x1 = X0 + (R - Q - SIG**2 / 2) * T + SIG * math.sqrt(T) * z
    spread = (x1 - X0) ** 2
    m_fut = np.exp(0.5 * (X0 + x1 - np.sqrt(spread - 2 * SIG**2 * T * np.log(u_min))))
    M_fut = np.exp(0.5 * (X0 + x1 + np.sqrt(spread - 2 * SIG**2 * T * np.log(u_max))))
    ST = np.exp(x1)
    cases = [
        (
            "floating call, S_min = 45",
            DISC * (ST - np.minimum(45.0, m_fut)),
            HULL.floating_call(S0, 45.0, T),
        ),
        (
            "floating put, S_max = 56",
            DISC * (np.maximum(56.0, M_fut) - ST),
            HULL.floating_put(S0, 56.0, T),
        ),
        (
            "fixed call K = 52, S_max = 56",
            DISC * np.maximum(np.maximum(56.0, M_fut) - 52.0, 0),
            HULL.fixed_call(S0, 56.0, 52.0, T),
        ),
        (
            "fixed call K = 60, S_max = 56",
            DISC * np.maximum(np.maximum(56.0, M_fut) - 60.0, 0),
            HULL.fixed_call(S0, 56.0, 60.0, T),
        ),
    ]
    se_seasoned = {}
    for name, x, cf in cases:
        m, se = x.mean(), x.std(ddof=1) / math.sqrt(n2)
        se_seasoned[name] = se
        report.ok(
            f"{name}: simulation within 4 s.e. of the closed form",
            abs(m - cf) <= 4 * se,
            f"{m:.4f} (s.e. {se:.4f}) against {cf:.4f}, z = {(m - cf) / se:+.2f}",
        )
    gap_c = HULL.floating_call(S0, 45.0, T) - call0
    gap_p = HULL.floating_put(S0, 56.0, T) - put0
    report.ok(
        "power: seasoned and new-issue closed forms differ by more than 20 s.e."
        " (ignoring history would fail)",
        abs(gap_c) > 20 * se_seasoned["floating call, S_min = 45"]
        and abs(gap_p) > 20 * se_seasoned["floating put, S_max = 56"],
        f"call +{gap_c:.4f} ({gap_c / se_seasoned['floating call, S_min = 45']:.0f} s.e.), "
        f"put +{gap_p:.4f} ({gap_p / se_seasoned['floating put, S_max = 56']:.0f} s.e.)",
    )


# ---------------------------------------------------------------- part 3
def check_monitoring(
    report: CheckReport, rng: np.random.Generator, call0: float, put0: float
) -> None:
    """Check discrete against continuous monitoring on coupled nested grids (new issue)."""
    print("== part 3: discrete against continuous monitoring on coupled nested grids (new issue)")
    n_paths, n_steps, block = 100_000, 1008, 5000
    grids = (7, 21, 63, 252, 1008)
    dt = T / n_steps
    keys: list[tuple[str, str | int]] = [("call", "cont"), ("put", "cont")] + [
        (k, m) for k in ("call", "put") for m in grids
    ]
    acc = {k: [0.0, 0.0] for k in keys}  # sums and sums of squares of discounted payoffs
    gacc = {(k, m): [0.0, 0.0] for k in ("call", "put") for m in grids}  # paired gaps
    ordered = True
    for _ in range(n_paths // block):
        z = rng.standard_normal((block, n_steps))
        um = 1.0 - rng.random((block, n_steps))
        uM = 1.0 - rng.random((block, n_steps))
        x = np.empty((block, n_steps + 1))
        x[:, 0] = X0
        np.cumsum((R - Q - SIG**2 / 2) * dt + SIG * math.sqrt(dt) * z, axis=1, out=x[:, 1:])
        x[:, 1:] += X0
        a, b = x[:, :-1], x[:, 1:]
        d2 = (b - a) ** 2
        mc = np.exp(0.5 * (a + b - np.sqrt(d2 - 2 * SIG**2 * dt * np.log(um))).min(axis=1))
        Mc = np.exp(0.5 * (a + b + np.sqrt(d2 - 2 * SIG**2 * dt * np.log(uM))).max(axis=1))
        ST = np.exp(x[:, -1])
        pay: dict[tuple[str, str | int], Floats] = {
            ("call", "cont"): DISC * (ST - mc),
            ("put", "cont"): DISC * (Mc - ST),
        }
        for m in grids:
            sub = x[:, :: n_steps // m]
            pay[("call", m)] = DISC * (ST - np.exp(sub.min(axis=1)))
            pay[("put", m)] = DISC * (np.exp(sub.max(axis=1)) - ST)
        for k in ("call", "put"):
            chain = [pay[(k, "cont")]] + [pay[(k, m)] for m in reversed(grids)]
            ordered &= all(bool((hi >= lo - 1e-12).all()) for hi, lo in itertools.pairwise(chain))
        for key, v in pay.items():
            acc[key][0] += v.sum()
            acc[key][1] += (v**2).sum()
        for k in ("call", "put"):
            for m in grids:
                g = pay[(k, "cont")] - pay[(k, m)]
                gacc[(k, m)][0] += g.sum()
                gacc[(k, m)][1] += (g**2).sum()

    def mean_se(s: list[float]) -> tuple[float, float]:
        m = s[0] / n_paths
        return m, math.sqrt((s[1] / n_paths - m**2) / (n_paths - 1))

    report.ok(
        "pathwise: continuous >= m = 1,008 >= 252 >= 63 >= 21 >= 7 payoff on every path"
        " (call and put)",
        ordered,
    )
    for k, cf in (("call", call0), ("put", put0)):
        est, se = mean_se(acc[(k, "cont")])
        report.ok(
            f"{k}: continuous (bridge) estimate within 4 s.e. of the closed form",
            abs(est - cf) <= 4 * se,
            f"{est:.4f} (s.e. {se:.4f}) against {cf:.4f}, z = {(est - cf) / se:+.2f}",
        )
        gaps = {}
        for mm in grids:
            gap, gse = mean_se(gacc[(k, mm)])
            gaps[mm] = (gap, gse)
            print(
                f"    m = {mm:5d}: value {mean_se(acc[(k, mm)])[0]:.4f}, "
                f"gap {gap:.4f} (paired s.e. {gse:.5f}), gap*sqrt(m) {gap * math.sqrt(mm):.3f}"
            )
        report.ok(
            f"{k}: every monitoring gap positive by more than 4 paired s.e.",
            all(gap > 4 * s for gap, s in gaps.values()),
        )
        report.ok(
            f"{k}: convergence, gap at m = 1,008 at most half the gap at m = 63",
            gaps[1008][0] <= 0.5 * gaps[63][0],
            f"{gaps[1008][0]:.4f} against {gaps[63][0]:.4f} "
            f"(ratio {gaps[1008][0] / gaps[63][0]:.3f})",
        )


def main() -> int:
    """Print the versions, then run the three parts with one report.

    GBM with constant r, q and sigma, r != q. Hull's floating formulas (OFOD 11th Global ed., sec.
    26.11, pp. 623-624) are checked against Wilmott's sec. 26.6 forms (PWOQF 2nd ed., pp. 450-452),
    an independent transcription. Part 1 is deterministic: Hull's Example 26.2 (put 7.79, call
    8.04), the two sources against each other, the pricing-equation residual, dV/dM = 0 on S = M and
    deep-seasoned limits. Part 2 simulates the terminal price and the continuous extreme of the
    remaining life exactly (default_rng(20261022), 400,000 paths). Part 3 measures monitoring bias
    on nested grids m = 7, ..., 1,008 against exact bridge extremes on the same paths
    (default_rng(20261021), 100,000 paths of 1,008 steps in 20 blocks: normals, then uniforms for
    the minimum, then for the maximum), separating sampling error from the paired monitoring gap.
    Synthetic model data only; about 15 seconds.

    Parts 2 and 3 each draw from their own seeded generator.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    report = CheckReport()
    call0, put0 = check_closed_forms(report)
    check_seasoned(report, np.random.default_rng(20261022), call0, put0)
    check_monitoring(report, np.random.default_rng(20261021), call0, put0)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
