"""Counterparty credit risk: exposures, CVA, wrong-way risk, collateral and rate-tree CVA."""

import itertools
import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, optimize, stats

from trading_notes.numerical.arbitrage_free_valuation.short_rate_models import (
    GSW_CURVE,
    HullWhite,
)
from trading_notes.numerical.counterparty_xva.swap_exposure import AnnualSwap, par_rate
from trading_notes.numerical.counterparty_xva.tree_cva import DefaultRisk, ShortRateTree
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

N: Final = stats.norm.cdf
N_PDF: Final = stats.norm.pdf
CURVE: Final = GSW_CURVE
HW: Final = HullWhite(curve=CURVE, a=0.1, sigma=0.01)  # illustrative, not calibrated
NOTIONAL: Final = 100.0
DELTA: Final = 10 / 252  # the margin period of risk, in years
PAY_DATES: Final = (1.0, 2.0, 3.0, 4.0, 5.0)
N_PATHS: Final = 40_000
PAR: Final = (0.035, 0.042, 0.047, 0.052)


def P0(t: float) -> float:
    """Return the discount factor P(0, t) of the GSW curve."""
    return CURVE.discount(t)


def lag_windows() -> dict[int, float]:
    """The margin periods of the lag diagnostic, in years, keyed by days."""
    return {5: 5 / 252, 10: 10 / 252, 20: 20 / 252}


def expo_dates() -> list[float]:
    """The exposure dates: nine daily dates, then mid-months for five years."""
    return [k / 252 for k in range(1, 10)] + [(m + 0.5) / 12 for m in range(60)]


def crossing_dates(lag: float, dates: list[float]) -> list[float]:
    """The exposure dates whose window (t - lag, t] contains a payment date."""
    return [t for t in dates if any(t - lag < p <= t for p in PAY_DATES) and t >= lag]


def diagnostic_dates() -> list[float]:
    """The exposure dates whose windows, for every lag, contain no payment date."""
    dates = expo_dates()
    lags = lag_windows()
    crossing = {lag: crossing_dates(d, dates) for lag, d in lags.items()}
    return [t for t in dates if t >= lags[20] and not any(t in crossing[g] for g in lags)]


def check_published(report: CheckReport) -> None:
    """Part 1: published examples of the exposure measures, the CVA and the gold forward.

    Args:
        report: The run's report.
    """
    print("== Part 1: published examples")
    for mu, s, ee_p, pfe_p in ((2.0, 2.0, 2.17, 6.65), (2.0, 4.0, 2.79, 11.31)):
        ee = mu * N(mu / s) + s * N_PDF(mu / s)
        pfe = mu + stats.norm.ppf(0.99) * s
        report.ok(
            f"Gregory p. 116: normal future value (mean {mu:g}, s.d. {s:g}) has EE {ee_p} and 99%"
            " PFE"
            f" {pfe_p}",
            abs(ee - ee_p) < 5e-3 and abs(pfe - pfe_p) < 5e-3,
            f"{ee:.4f}, {pfe:.4f}",
        )
    spread, lgd = 0.03, 0.6

    def ee_g(t: float) -> float:
        return 0.01 * math.sqrt(t)

    def surv(t: float) -> float:
        return math.exp(-spread * t / lgd)

    grid = [0.25 * i for i in range(21)]
    cva_end = lgd * sum(ee_g(b) * (surv(a) - surv(b)) for a, b in itertools.pairwise(grid))
    cva_mid = lgd * sum(
        0.5 * (ee_g(a) + ee_g(b)) * (surv(a) - surv(b)) for a, b in itertools.pairwise(grid)
    )
    cva_exact = lgd * integrate.quad(lambda t: ee_g(t) * spread / lgd * surv(t), 0, 5)[0]
    report.ok(
        "Gregory p. 312: CVA of EE = 1% sqrt(t), 300 bp, LGD 60%, 20 quarterly dates: 0.200%, exact"
        " 0.193%, averaged 0.192%",
        abs(100 * cva_end - 0.200) < 5e-4
        and abs(100 * cva_exact - 0.193) < 5e-4
        and abs(100 * cva_mid - 0.192) < 5e-4,
        f"{100 * cva_end:.4f}%, {100 * cva_exact:.4f}%, {100 * cva_mid:.4f}%",
    )
    F0, K, sg_f, r_f, R_f, T_f = 1600.0, 1500.0, 0.2, 0.05, 0.3, 2.0
    q = (0.02, 0.03)
    v = []
    for t in (0.5, 1.5):
        d1 = (math.log(F0 / K) + sg_f**2 * t / 2) / (sg_f * math.sqrt(t))
        v.append(math.exp(-r_f * T_f) * (F0 * N(d1) - K * N(d1 - sg_f * math.sqrt(t))))
    cva_gold = (1 - R_f) * (q[0] * v[0] + q[1] * v[1])
    report.ok(
        "RMFI Example 18.3: v1 = 132.38, v2 = 186.65, CVA = 5.77 and value 84.71",
        abs(v[0] - 132.38) < 5e-3
        and abs(v[1] - 186.65) < 5e-3
        and abs(cva_gold - 5.77) < 5e-3
        and abs(100 * math.exp(-0.1) - cva_gold - 84.71) < 5e-3,
        f"{v[0]:.2f}, {v[1]:.2f}, {cva_gold:.3f}",
    )
    report.ok(
        "OFOD Example 24.6 prints v1 = 92.67 and v2 = 130.65: the same exposures times (1 - R)",
        abs((1 - R_f) * v[0] - 92.67) < 5e-3 and abs((1 - R_f) * v[1] - 130.65) < 5e-3,
        f"{(1 - R_f) * v[0]:.2f}, {(1 - R_f) * v[1]:.2f}",
    )
    # Units of Gregory's EPE x spread (sec. 14.2.5, p. 313). Eq. (14.4) gives CVA "in the same units
    # as the credit spread", a per-annum charge with undiscounted EPE; an upfront CVA is that spread
    # times the risky annuity. Gregory's annuity (zero rates, his online Appendix 14B, not read) is
    # reproduced by (1 - e^{-hT}) / h.
    haz_g = spread / lgd
    annuity = (1 - math.exp(-haz_g * 5)) / haz_g
    cva_bp = 1e4 * cva_end / annuity
    epe_q = sum(ee_g(b) for b in grid[1:]) / 20
    epe_exact = integrate.quad(ee_g, 0, 5)[0] / 5
    approx_bp = 1e4 * epe_q * spread
    report.ok(
        "Gregory p. 313: risky annuity 4.42, CVA spread 0.200% / 4.42 = 4.52 bp a year, EPE 1.54%"
        " (1.49% exact), EPE x 300 bp = 4.62 bp a year",
        abs(annuity - 4.42) < 5e-3
        and abs(cva_bp - 4.52) < 5e-3
        and abs(100 * epe_q - 1.54) < 5e-3
        and abs(100 * epe_exact - 1.49) < 5e-3
        and abs(approx_bp - 4.62) < 5e-3,
        f"{annuity:.4f}, {cva_bp:.4f} bp, {100 * epe_q:.4f}%, {100 * epe_exact:.4f}%,"
        f" {approx_bp:.4f} bp",
    )
    upfront_from_approx = approx_bp / 1e4 * annuity
    report.ok(
        "EPE x spread is a running spread: times the annuity it is within 5% of the 0.200% upfront"
        " CVA, while read as upfront it is about a quarter of it",
        abs(upfront_from_approx / cva_end - 1) < 0.05 and epe_q * spread / cva_end < 0.3,
        f"{100 * upfront_from_approx:.4f}% upfront against {100 * cva_end:.4f}%; EPE x spread"
        f" {100 * epe_q * spread:.4f}% of notional a year",
    )
    # E(t) is undiscounted here, so a default-time exposure enters CVA multiplied by D(0, t). One
    # date at 1 year, exposure 100, PD 5%, R = 40%, deterministic continuously compounded rate 5%.
    pv_cva = (1 - 0.40) * 0.05 * 100 * math.exp(-0.05 * 1)
    report.ok(
        "PV CVA of a one-year exposure of 100 (PD 5%, R 40%, rate 5% continuous) is 2.8536882735,"
        " not 3",
        abs(pv_cva - 2.8536882735) < 1e-10 and abs(pv_cva - 3) > 0.1,
        f"{pv_cva:.10f}",
    )


def check_wrong_way(report: CheckReport) -> None:
    """Part 2: wrong-way risk at one exposure date, by quadrature and by Monte Carlo.

    Args:
        report: The run's report.
    """
    print("== Part 2: wrong-way risk at one exposure date (200,000 draws)")
    PD, R, s_v = 0.05, 0.40, 1.0
    c = stats.norm.ppf(PD)

    def cva_quad(rho: float) -> float:
        """(1 - R) E[max(V, 0) 1{Y < c}] by quadrature over v of v phi(v) P(Y < c | V = v)."""

        def f(x: float) -> float:
            return s_v * x * N_PDF(x) * N((c - rho * x) / math.sqrt(1 - rho**2))

        return (1 - R) * integrate.quad(f, 0, np.inf, epsabs=1e-14, epsrel=1e-12)[0]

    rhos = (-0.5, -0.25, 0.0, 0.25, 0.5)
    quad_vals = [cva_quad(rho) for rho in rhos]
    rng = np.random.default_rng(20261071)
    z = rng.standard_normal((2, 200_000))
    for rho, qv in zip(rhos, quad_vals, strict=True):
        V = s_v * z[0]
        Y = rho * z[0] + math.sqrt(1 - rho**2) * z[1]
        loss = (1 - R) * np.maximum(V, 0) * (Y < c)
        m, se = float(loss.mean()), float(loss.std(ddof=1) / math.sqrt(loss.size))
        report.ok(
            f"rho = {rho:+.2f}: quadrature CVA {qv:.5f} within 3 s.e. of Monte Carlo",
            abs(m - qv) <= 3 * se,
            f"{m:.5f} (s.e. {se:.5f})",
        )
    indep = (1 - R) * PD * s_v / math.sqrt(2 * math.pi)
    report.ok(
        "at rho = 0 the value equals the independent (1 - R) PD s / sqrt(2 pi) to 1e-10",
        abs(quad_vals[2] - indep) < 1e-10,
        f"{indep:.8f}",
    )
    report.ok(
        "CVA is strictly decreasing in rho (rho < 0: default with high V, wrong-way)",
        all(a > b for a, b in itertools.pairwise(quad_vals)),
        ", ".join(f"{x:.5f}" for x in quad_vals),
    )


def check_swaps(report: CheckReport) -> tuple[dict[float, Floats], dict[float, Floats]]:
    """Part 3: swap exposures under Hull-White on the GSW curve, from 40,000 simulated paths.

    Args:
        report: The run's report.

    Returns:
        The five-year payer exposures' values and the discounted state, by date, for part 3b.
    """
    print("== Part 3: swap exposure under Hull-White on the GSW curve (40,000 paths)")
    a = HW.a
    payer5 = AnnualSwap(fixed_rate=par_rate(CURVE, 5), years=5, payer=True, notional=NOTIONAL)
    receiver3 = AnnualSwap(fixed_rate=par_rate(CURVE, 3), years=3, payer=False, notional=NOTIONAL)
    K5 = payer5.fixed_rate
    lags = lag_windows()
    crossing = {lag: crossing_dates(d, expo_dates()) for lag, d in lags.items()}
    report.ok(
        "no payment falls in (t - 10/252, t] for any exposure date (so V(t) and V(t - delta) share"
        " a"
        " reset)",
        not crossing[10] and not crossing[5],
    )
    diag_dates = diagnostic_dates()
    print(
        f"  20-day windows cross a payment at {len(crossing[20])} dates"
        f" ({', '.join(f'{12 * t:.1f}m' for t in crossing[20])}); they are left out of the lag"
        f" diagnostic for every lag ({len(diag_dates)} common dates)"
    )
    times = sorted(
        set(expo_dates())
        | {t - d for t in expo_dates() for d in lags.values() if t - d > 0}
        | set(PAY_DATES[:-1])
    )
    n_p = N_PATHS
    rng = np.random.default_rng(20261072)
    x = np.zeros(n_p)
    integ = np.zeros(n_p)
    reset_bond: dict[int, Floats] = {0: np.full(n_p, P0(1.0))}
    V5: dict[float, Floats] = {}
    V3: dict[float, Floats] = {}
    D: dict[float, Floats] = {}
    t_prev = 0.0
    for t in times:
        dt = t - t_prev
        e1 = math.exp(-a * dt)
        L = np.linalg.cholesky(HW.step_covariance(dt))
        eps = L @ rng.standard_normal((2, n_p))
        integ = integ + x * HW.b(dt) + eps[1]
        x = x * e1 + eps[0]
        t_prev = t
        if t in PAY_DATES:
            reset_bond[round(t)] = HW.bond(t, t + 1, x)
            continue
        k = math.floor(t)
        V5[t] = payer5.value(HW, t, x, reset_bond[k])
        V3[t] = receiver3.value(HW, t, x, reset_bond[k])
        D[t] = HW.path_discount(t, integ)
    # Deterministic checks of the discount factor. The opposite sign, P0(t) exp(+var_int / 2 - I),
    # overstates every D(0, t) by exp(var_int(t)), at most 0.29 percent here; the Monte Carlo
    # checks below could not detect it.
    chk = (0.5, 1.96, 4.96)
    int_alpha = [integrate.quad(HW.alpha, 0, t, epsabs=1e-14, epsrel=1e-12)[0] for t in chk]
    err_new = max(
        abs(HW.path_discount(t, 0.0) / math.exp(-ia) - 1)
        for t, ia in zip(chk, int_alpha, strict=True)
    )
    err_old = min(
        abs(P0(t) * math.exp(0.5 * HW.var_int(t)) / math.exp(-ia) - 1)
        for t, ia in zip(chk, int_alpha, strict=True)
    )
    report.ok(
        "D(0, t) at I = 0 equals exp(-int alpha) with int alpha by quadrature, to 1e-10 relative"
        " (the"
        " +var/2 sign fails at every date, by more than 1e-6)",
        err_new < 1e-10 and err_old > 1e-6,
        f"error {err_new:.1e}; opposite sign {err_old:.2e} or more",
    )
    # Exact-sampling covariance of (x, I), propagated through the simulation's own steps without
    # random numbers. The gap is absolute: var_int is about 1e-13 on the first daily dates, where
    # the closed form loses relative precision, and an absolute variance error e moves D(0, t) by e
    # / 2 relative.
    cov = np.zeros((2, 2))
    var_gap = 0.0
    t_prev = 0.0
    for t in times:
        dt = t - t_prev
        e1 = math.exp(-a * dt)
        step = np.array([[e1, 0.0], [HW.b(dt), 1.0]])
        cov = step @ cov @ step.T + HW.step_covariance(dt)
        var_gap = max(var_gap, abs(cov[1, 1] - HW.var_int(t)))
        t_prev = t
    mean_d = max(
        abs(HW.path_discount(t, 0.0) * math.exp(0.5 * HW.var_int(t)) / P0(t) - 1) for t in chk
    )
    report.ok(
        "the simulated I has variance var_int(t) at every date (to 1e-14 absolute), so E[D(0, t)] ="
        " P0(t) exactly by the normal moment generating function (to 1e-12)",
        var_gap < 1e-14 and mean_d < 1e-12,
        f"{var_gap:.1e}, {mean_d:.1e}",
    )
    v0 = payer5.value(HW, 0.0, np.zeros(1), np.array([P0(1.0)]))[0]
    report.ok(
        "the at-market five-year payer swap has V(0) = 0, so EE(0) = 0, to 1e-12",
        abs(v0) < 1e-12,
        f"{v0:.1e}",
    )
    zs = []
    for t in (0.5 / 12, 11.5 / 12, 24.5 / 12, 36.5 / 12, 54.5 / 12):
        # payments after t: floating coupon j is worth P0(j - 1) - P0(j) today whether or not it has
        # been set
        target = NOTIONAL * sum((P0(j - 1) - P0(j)) - K5 * P0(j) for j in range(1, 6) if j > t)
        y = D[t] * V5[t]
        zs.append((float(y.mean()) - target) / float(y.std(ddof=1) / math.sqrt(n_p)))
    report.ok(
        "the discounted ex-coupon swap value has the curve's forward value at five dates (within 4"
        " s.e.)",
        max(abs(z) for z in zs) <= 4,
        "z = " + ", ".join(f"{z:+.2f}" for z in zs),
    )
    mid = [t for t in expo_dates() if t > 0.04]
    EE = np.array([float(np.maximum(V5[t], 0).mean()) for t in mid])
    peak = int(EE.argmax())
    report.ok(
        "EE of the payer swap peaks at an interior date",
        0 < peak < len(mid) - 1,
        f"peak {EE[peak]:.3f} at {mid[peak]:.2f} years; EE at {mid[0]:.2f} and {mid[-1]:.2f} years"
        f" {EE[0]:.3f}, {EE[-1]:.3f}",
    )
    net = {t: V5[t] + V3[t] for t in expo_dates()}
    pathwise = all(
        bool(np.all(np.maximum(net[t], 0) <= np.maximum(V5[t], 0) + np.maximum(V3[t], 0) + 1e-12))
        for t in expo_dates()
    )
    report.ok(
        "netted exposure never exceeds the sum of stand-alone exposures on any path or date",
        pathwise,
    )
    EE_net = np.array([float(np.maximum(net[t], 0).mean()) for t in mid])
    EE_sum = np.array(
        [float(np.maximum(V5[t], 0).mean() + np.maximum(V3[t], 0).mean()) for t in mid]
    )
    report.ok(
        "so netted EE is at most the sum of stand-alone EEs at every date",
        bool(np.all(EE_net <= EE_sum + 1e-12)),
    )
    t_pk = mid[peak]
    pfe = float(np.quantile(np.maximum(V5[t_pk], 0), 0.975))
    rng_b = np.random.default_rng(20261073)
    boot = [
        float(np.quantile(np.maximum(V5[t_pk], 0)[rng_b.integers(0, n_p, n_p)], 0.975))
        for _ in range(200)
    ]
    print(
        f"  97.5% PFE at the EE peak: {pfe:.3f} (bootstrap s.e. {np.std(boot, ddof=1):.3f}, 200"
        f" resamples); netting with the three-year receiver lowers EE at {mid[17]:.2f} years from"
        f" {EE_sum[17]:.3f} to {EE_net[17]:.3f}"
    )
    return V5, D


def check_collateral(report: CheckReport, V5: dict[float, Floats], D: dict[float, Floats]) -> None:
    """Part 3b: collateral with a ten-day margin period of risk, and the CVA with and without it.

    Args:
        report: The run's report.
        V5: The five-year payer exposures by date, from part 3.
        D: The discount factors by date, from part 3.
    """
    print("== Part 3b: collateral with a 10-day margin period of risk")
    n_p = N_PATHS
    lags = lag_windows()
    expo = expo_dates()
    early = [t for t in expo if t < DELTA]

    def lagged(t: float, d: float) -> Floats:
        return V5[t - d] if t - d > 0 else np.zeros(n_p)

    report.ok(
        "E_c(t) = E(t) for t < delta on every path (no call has settled yet)",
        len(early) == 9
        and all(
            bool(np.all(np.maximum(V5[t] - lagged(t, DELTA), 0) == np.maximum(V5[t], 0)))
            for t in early
        ),
    )
    late = [t for t in expo if t >= DELTA]
    one_way = all(
        bool(np.all(np.maximum(V5[t] - np.maximum(lagged(t, DELTA), 0), 0) <= np.maximum(V5[t], 0)))
        for t in late
    )
    report.ok("one-way variant C = max(V(t - delta), 0): E_c <= E on every path", one_way)
    two_way = all(
        bool(
            np.all(
                np.maximum(V5[t] - lagged(t, DELTA), 0) <= np.abs(V5[t] - lagged(t, DELTA)) + 1e-12
            )
        )
        for t in late
    )
    report.ok(
        "two-way: E_c <= |V(t) - V(t - delta)| on every path, and E_c = 0 when delta = 0", two_way
    )
    posted = sum(int(np.sum((lagged(t, DELTA) < 0) & (V5[t] > 0))) for t in late)
    worse = [
        t
        for t in late
        if float(np.maximum(V5[t] - lagged(t, DELTA), 0).mean())
        > float(np.maximum(V5[t], 0).mean())
    ]
    print(
        f"  path-dates where the bank had posted and V turned positive (E_c > E there): {posted};"
        f" dates with EE_c > EE: {len(worse)}"
    )
    print("  diagnostic, EE_c against sigma_dV / sqrt(2 pi) (common dates, mean over dates):")
    diag_dates = diagnostic_dates()
    for lag, d in lags.items():
        ratio = []
        for t in diag_dates:
            dv = V5[t] - V5[t - d]
            ratio.append(
                float(np.maximum(dv, 0).mean()) / (float(dv.std(ddof=1)) / math.sqrt(2 * math.pi))
            )
        ee_c = np.mean([float(np.maximum(V5[t] - V5[t - d], 0).mean()) for t in diag_dates])
        print(
            f"    {lag:2d} days: mean EE_c {ee_c:.4f}; EE_c / approximation {np.mean(ratio):.3f}"
            f" (range {min(ratio):.3f}-{max(ratio):.3f})"
        )
    h, R_s = 0.02, 0.40
    cva_u = cva_c = 0.0
    gap = []
    for m in range(60):
        t = (m + 0.5) / 12
        pd_m = math.exp(-h * m / 12) - math.exp(-h * (m + 1) / 12)
        ee_star = float((D[t] * np.maximum(V5[t], 0)).mean())
        cva_u += (1 - R_s) * ee_star * pd_m
        cva_c += (1 - R_s) * float((D[t] * np.maximum(V5[t] - lagged(t, DELTA), 0)).mean()) * pd_m
        gap.append(ee_star - P0(t) * float(np.maximum(V5[t], 0).mean()))
    print(
        f"  CVA (hazard 2%, R = 40%, monthly intervals, per 100 notional): uncollateralised"
        f" {cva_u:.10f}, collateralised {cva_c:.10f}; largest |E[D E] - P(0,t) E[E]|"
        f" {max(abs(g) for g in gap):.10f}"
    )


def check_tree(report: CheckReport) -> None:
    """Part 4: CVA on the Handbook's calibrated rate tree, by nodes and by paths.

    Args:
        report: The run's report.
    """
    print("== Part 4: CVA on the Handbook's calibrated rate tree (original derivation)")
    par = list(PAR)
    tree = ShortRateTree.calibrate(par, 0.10)
    report.ok(
        "calibrated year-1 and year-3 rates match Handbook Exhibits 36-6 to 36-8 (4.4448, 5.4289;"
        " 5.0483, 9.1986 percent)",
        abs(100 * tree.rates[1][0] - 4.4448) < 5e-5
        and abs(100 * tree.rates[1][1] - 5.4289) < 5e-5
        and abs(100 * tree.rates[3][0] - 5.0483) < 5e-5
        and abs(100 * tree.rates[3][3] - 9.1986) < 5e-4,
    )
    cpn, risk = 5.0, DefaultRisk(hazard=(0.015,) * 4, recovery=0.40)
    cva_tree, cva_path = tree.bond_cva(cpn, risk), tree.bond_path_cva(cpn, risk)
    report.ok(
        "node-weighted expected exposure gives the same CVA as the pathwise average to 1e-10",
        abs(cva_tree - cva_path) < 1e-10,
        f"{cva_tree:.6f}",
    )
    spot: list[float] = []  # discount factors bootstrapped from the par curve
    for k in range(4):
        spot.append((1 - par[k] * sum(spot)) / (1 + par[k]))
    fwd_rates = [1 / spot[0] - 1] + [spot[t - 1] / spot[t] - 1 for t in range(1, 4)]
    flat_tree = ShortRateTree(rates=tuple(np.full(t + 1, fwd_rates[t]) for t in range(4)))
    cva_fwd = flat_tree.bond_cva(cpn, risk)
    gaps = {
        sgm: abs(ShortRateTree.calibrate(par, sgm).bond_cva(cpn, risk) - cva_fwd)
        for sgm in (0.2, 0.1, 1e-2, 1e-4)
    }
    report.ok(
        "as sigma -> 0 the tree CVA tends to the forward-rate calculation of meth:risky-bond-cva"
        " (gap"
        " < 1e-6 at sigma = 1e-4)",
        gaps[1e-4] < 1e-6,
        f"forward-rate CVA {cva_fwd:.6f}; gaps "
        + ", ".join(f"{s:g}: {g:.2e}" for s, g in gaps.items()),
    )
    for sgm in (0.0001, 0.10, 0.20):
        print(
            f"  sigma = {sgm:g}: CVA of the 5% four-year bond (hazard 1.5%, R = 40%)"
            f" {ShortRateTree.calibrate(par, sgm).bond_cva(cpn, risk):.6f}"
        )
    # The bond's CVA does not depend on sigma: sum_j AD(t, j) [V(t, j) + C] is the curve value of
    # the flows from t on, so a linear exposure has a curve-determined CVA. A swap's exposure
    # max(V, 0) is not linear, so its CVA should rise with sigma.
    swap_cvas = [
        ShortRateTree.calibrate(par, sgm).swap_cva(par[-1], risk) for sgm in (0.0001, 0.10, 0.20)
    ]
    report.ok(
        "an at-market four-year payer swap on the same tree has a CVA that rises with sigma (1e-4,"
        " 10%, 20%)",
        swap_cvas[0] < swap_cvas[1] < swap_cvas[2],
        ", ".join(f"{x:.4f}" for x in swap_cvas),
    )
    fl = tree.floater_values(0.0)
    report.ok(
        "a default-free floater paying the tree rate flat is worth par at every node to 1e-10",
        all(float(np.max(np.abs(fl[t] - 100))) < 1e-10 for t in range(4)),
    )
    qm, floater_risk = 0.005, DefaultRisk(hazard=(0.010, 0.015, 0.020, 0.025), recovery=0.40)
    nd_value = float(tree.floater_values(qm)[0][0])
    fair = nd_value - tree.floater_cva(qm, floater_risk)

    def dm_gap(d: float) -> float:
        return float(tree.floater_values(qm, d)[0][0]) - fair

    dm = optimize.brentq(dm_gap, -0.05, 0.2, xtol=1e-15, rtol=1e-15)
    report.ok(
        "the discount margin solved on the tree reprices the risky floater's fair value to 1e-8",
        abs(float(tree.floater_values(qm, dm)[0][0]) - fair) < 1e-8,
        f"no-default value {nd_value:.4f}, CVA {nd_value - fair:.4f}, fair value {fair:.4f}, quoted"
        f" margin 50 bp, discount margin {1e4 * dm:.2f} bp",
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Worked examples of def:counterparty-exposure-measures, meth:credit-valuation-adjustment,
    def:wrong-way-risk and the rate-tree extension of meth:risky-bond-cva.

    Part 1 reproduces published examples: Gregory's normal-distribution EE and PFE (The xVA
    Challenge, 3rd ed., sec. 7.2.4, p. 116), his CVA of a square-root exposure (sec. 14.2.4, p. 312)
    and the units of his EPE x spread approximation, and the gold forward of Hull (Options, Futures,
    and Other Derivatives, 11th Global ed., Example 24.6) and Hull (Risk Management and Financial
    Institutions, 6th ed., Example 18.3). Part 2 is the one-date wrong-way-risk example: V ~ N(0,
    1), default when a latent normal Y with Corr(V, Y) = rho falls below Phi^-1(PD) (lower-tail
    default), PD = 5 percent, R = 40 percent, unit discounting. Part 3 simulates swap exposures
    under one-factor Hull-White on the GSW curve of 30 September 2026, the model and curve of the
    short-rate model checks (a = 0.1, sigma = 1 percent; illustrative). The swaps are single-curve
    and synthetic. Part 4 is the rate-tree CVA and risky floater: an original derivation on the
    Handbook's calibrated tree (Fabozzi, Handbook of Fixed Income Securities, 9th ed., chap. 36),
    with original credit inputs.

    Conventions: unilateral CVA from the bank's side; exposure max(V, 0) of the netting set's
    ex-coupon mark-to-market; risk-neutral measure with the bank-account numeraire. Two-way CSA in
    cash, daily variation margin, zero threshold and minimum transfer amount, no initial margin;
    collateral C(t) = V(t - delta) for t >= delta and 0 before, held by the bank when positive; no
    margin moves in the margin period of risk; posted collateral not segregated; collateral earns
    the discount rate and accrual during the MPR is ignored. delta = 10 business days (10/252
    years). Exposure dates are mid-months (plus nine daily dates before delta), so no swap payment
    falls in any window (t - delta, t]; part 3 checks this for every lag it uses. Default is
    independent of rates, with a deterministic hazard.

    Seeds: 20261071 wrong-way Monte Carlo, 20261072 swap paths, 20261073 PFE bootstrap. Each
    generator is made in the part that draws from it; part 3b reads the exposures that part 3
    returns.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_published(report)
    check_wrong_way(report)
    V5, D = check_swaps(report)
    check_collateral(report, V5, D)
    check_tree(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
