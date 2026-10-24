"""Conditional predictive ability: statistic validation, simulations and a rolling illustration."""

import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
import scipy
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.return_predictability.conditional_ability import (
    InstrumentedLosses,
    LossDifferences,
    RollingForecasts,
    SingularInstrumentsError,
    ar1,
    moving_average,
)
from trading_notes.numerical.return_predictability.labelled_table import LabelledTable
from trading_notes.numerical.return_predictability.scoring_rules import NormalForecast
from trading_notes.records import Record

type Floats = NDArray[np.float64]

DATA: Final = Path("notes/artefacts/return-predictability/goyal-annual-predictors-1871-2025.csv")
ALPHA: Final = 0.05
CRIT1, CRIT2 = float(stats.chi2.ppf(1 - ALPHA, 1)), float(stats.chi2.ppf(1 - ALPHA, 2))
Z975: Final = float(stats.norm.ppf(1 - ALPHA / 2))
M_N, BURN, PHI = 12, 200, 0.9
M_U, C_U, R_U = 4, 0.5, 10_000
T_X, R_X = 2000, 10_000
FIRST_OUTCOME, FIRST_FORECAST, LAST, M_E = 1927, 1947, 2025, 20


def mc(p: float, reps: int) -> float:
    """Return the Monte Carlo standard error of a rejection rate."""
    return float(np.sqrt(p * (1 - p) / reps))


def gw(Z: Floats) -> Floats:
    """Return the GW statistic of instrumented loss differences."""
    return InstrumentedLosses(Z=Z).statistic()


class ReproductionGates:
    """First-run reproduction gates, reported against their original criterion, not counted."""

    def __init__(self) -> None:
        """Start with no gates."""
        self._gates: list[tuple[str, bool, str]] = []

    @property
    def gates(self) -> list[tuple[str, bool, str]]:
        """Return each gate's name, whether it was met, and its detail, as a new list."""
        return list(self._gates)

    def record(self, name: str, met: bool, detail: str) -> None:
        """Print and keep one gate."""
        self._gates.append((name, met, detail))
        print(
            f"    reproduction gate (first-run criterion) {'MET' if met else 'NOT MET'}: {name}:"
            f" {detail}"
        )


def check_validation(report: CheckReport) -> Fraction:
    """V: the statistic on a hand example, random data, edge cases and its variances.

    Returns:
        The hand example's exact statistic.
    """
    print("\nV. Validation of the statistic")
    # V1. hand example
    a = [2, -1, 0, 3, 1, -2]
    dL = [3, -2, 1, 4, -1, 2]
    n6 = len(a)
    z1 = [Fraction(d) for d in dL]
    z2 = [Fraction(ai * d) for ai, d in zip(a, dL, strict=True)]
    zb = [sum(z1, Fraction(0)) / n6, sum(z2, Fraction(0)) / n6]
    o11 = sum((v * v for v in z1), Fraction(0)) / n6
    o12 = sum((u * v for u, v in zip(z1, z2, strict=True)), Fraction(0)) / n6
    o22 = sum((v * v for v in z2), Fraction(0)) / n6
    det = o11 * o22 - o12 * o12
    inv = [[o22 / det, -o12 / det], [-o12 / det, o11 / det]]
    T_exact = n6 * sum((zb[i] * inv[i][j] * zb[j] for i in range(2) for j in range(2)), Fraction(0))
    Zh = np.column_stack([np.ones(n6), np.array(a, float)]) * np.array(dL, float)[:, None]
    hand = InstrumentedLosses(Z=Zh)
    T_solve, T_nr2 = float(hand.statistic()), hand.n_r2()
    report.ok(
        "V1 hand example: exact = solve = n R^2",
        abs(T_solve - float(T_exact)) < 1e-12 and abs(T_nr2 - float(T_exact)) < 1e-12,
        f"T = {T_exact} = {float(T_exact):.6f}, p = {stats.chi2.sf(float(T_exact), 2):.4f}",
    )
    # V2. random data
    rng = np.random.default_rng(20261109)
    Zr = rng.standard_normal((500, 3)) + np.array([0.1, 0.0, -0.05])
    random_z = InstrumentedLosses(Z=Zr)
    report.ok(
        "V2 random n = 500, q = 3: solve = n R^2",
        bool(abs(random_z.statistic() - random_z.n_r2()) < 1e-10),
        f"T = {float(random_z.statistic()):.6f}",
    )
    # V3. q = 1 equals the square of ZT eq. (4)
    x1 = Zr[:, 0]
    report.ok(
        "V3 h = 1: T = (sum dL)^2 / sum dL^2 = GW_T^2",
        bool(
            abs(gw(x1[:, None]) - LossDifferences.of(x1).signed_gw() ** 2) < 1e-12
            and abs(gw(x1[:, None]) - x1.sum() ** 2 / (x1**2).sum()) < 1e-12
        ),
    )
    # V4. chi-square tails
    xs = [1.0, 4.0, 5.991, 10.0]
    report.ok(
        "V4 chi2(2) upper tail = exp(-x/2)",
        all(abs(stats.chi2.sf(x, 2) - np.exp(-x / 2)) < 1e-14 for x in xs),
    )
    report.ok(
        "V4 5% critical values q = 1, 2", [round(CRIT1, 3), round(CRIT2, 3)] == [3.841, 5.991]
    )
    # V5. singular instruments
    base = np.column_stack([np.ones(n6), np.array(a, float)])
    dup = np.column_stack([base, base[:, 1]]) * np.array(dL, float)[:, None]
    for label, Zs in (
        ("duplicated column", dup),
        (
            "h = (1, 2)",
            np.column_stack([np.ones(n6), 2 * np.ones(n6)]) * np.array(dL, float)[:, None],
        ),
    ):
        msg = ""
        try:
            gw(Zs)
            raised = False
        except SingularInstrumentsError as err:
            raised, msg = True, str(err)
        report.ok(f"V5 {label}: singular instruments raise", raised, msg if raised else "")
    zbar_d = dup.mean(axis=0)
    T_pinv = n6 * zbar_d @ np.linalg.pinv(dup.T @ dup / n6) @ zbar_d
    report.ok(
        "V5 Moore-Penrose statistic with the duplicate = reduced statistic (df = rank 2, not 3)",
        bool(abs(T_pinv - T_solve) < 1e-10),
        f"{T_pinv:.6f} vs {T_solve:.6f}",
    )
    # V6. multi-step covariance
    loop = Zh.T @ Zh / n6
    for t in range(1, n6):
        loop = loop + (np.outer(Zh[t], Zh[t - 1]) + np.outer(Zh[t - 1], Zh[t])) / n6
    report.ok(
        "V6 Omega-tilde (tau = 2) = hand loop; tau = 1 gives Omega-hat",
        np.allclose(hand.omega_tilde(2), loop, atol=1e-12, rtol=0)
        and np.allclose(hand.omega_tilde(1), Zh.T @ Zh / n6, atol=1e-12, rtol=0),
    )
    # V7. long-run variance and subsample t
    x12 = LossDifferences.of(
        np.array([0.5, -1.2, 2.0, 0.3, -0.7, 1.1, -0.4, 0.9, -1.5, 0.2, 0.8, -0.6])
    )
    e12 = x12.dl - x12.dl.mean()
    report.ok(
        "V7 uniform LRV (L = 2) = Omega-tilde (tau = 3) on demeaned data",
        bool(
            abs(x12.lrv(2, "uniform") - InstrumentedLosses(Z=e12[:, None]).omega_tilde(3)[0, 0])
            < 1e-12
        ),
    )
    nw = e12 @ e12 / 12 + sum(2 * (1 - j / 4) * (e12[j:] @ e12[:-j]) / 12 for j in range(1, 4))
    report.ok("V7 Newey-West (L = 3) = hand loop", bool(abs(x12.lrv(3, "bartlett") - nw) < 1e-12))
    bm = [x12.dl[0:3].mean(), x12.dl[3:6].mean(), x12.dl[6:9].mean(), x12.dl[9:12].mean()]
    by_hand = 2 * np.mean(bm) / np.std(bm, ddof=1)
    report.ok(
        "V7 subsample t (K = 4) = hand calculation",
        bool(abs(x12.subsample_t(4) - by_hand) < 1e-12),
        f"{by_hand:.6f}",
    )
    return T_exact


def check_states(report: CheckReport) -> tuple[float, float]:
    """H: same average accuracy, different conditional accuracy; return the two rejection rates."""
    print("\nH. Same average accuracy, different conditional accuracy (states)")
    EL = {}
    for s, mu in ((1, 1), (0, -1)):
        # E[(y - f)^2 | S] = 1 + (mu - f)^2 with var(eps) = 1
        EL[("A", s)] = 1 + Fraction(mu - 1) ** 2
        EL[("B", s)] = 1 + Fraction(mu + 1) ** 2
    cond = {s: EL[("A", s)] - EL[("B", s)] for s in (1, 0)}
    report.ok(
        "H exact: E[L_A|S] = 1, 5; E[L_B|S] = 5, 1; E[dL|S] = -4, +4; E dL = 0",
        [EL[("A", 1)], EL[("A", 0)], EL[("B", 1)], EL[("B", 0)]] == [1, 5, 5, 1]
        and cond == {1: -4, 0: 4}
        and (cond[1] + cond[0]) / 2 == 0,
    )
    R_H, n_H = 10_000, 120
    rng = np.random.default_rng(20261110)
    S = rng.integers(0, 2, size=(R_H, n_H)).astype(float)
    yH = np.where(S == 1, 1.0, -1.0) + rng.standard_normal((R_H, n_H))
    dLH = (yH - 1.0) ** 2 - (yH + 1.0) ** 2
    report.ok("H dL = -4 y exactly", np.allclose(dLH, -4 * yH, atol=1e-12, rtol=0))
    m1 = np.array([dLH[r][S[r] == 1].mean() for r in range(R_H)])
    m0 = np.array([dLH[r][S[r] == 0].mean() for r in range(R_H)])
    for lab, mm, target in (("S = 1", m1, -4), ("S = 0", m0, 4)):
        se = mm.std(ddof=1) / np.sqrt(R_H)
        report.ok(
            f"H pooled E[dL | {lab}] within 3 se of {target:+d}",
            bool(abs(mm.mean() - target) < 3 * se),
            f"{mm.mean():+.4f} (se {se:.4f})",
        )
    rej_unc = float(np.mean(gw(dLH[..., None]) > CRIT1))
    rej_cond = float(np.mean(gw(np.stack([dLH, S * dLH], axis=-1)) > CRIT2))
    print(
        f"  rejection at 5%, n = {n_H}, R = {R_H}: unconditional {rej_unc:.4f} (mc se"
        f" {mc(rej_unc, R_H):.4f}); conditional h = (1, S) {rej_cond:.4f} (mc se"
        f" {mc(rej_cond, R_H):.4f})"
    )
    report.ok(
        "H unconditional rejection in [0.035, 0.070]", 0.035 <= rej_unc <= 0.070, f"{rej_unc:.4f}"
    )
    report.ok("H conditional rejection >= 0.99", rej_cond >= 0.99, f"{rej_cond:.4f}")
    return rej_unc, rej_cond


def check_conditional_null(report: CheckReport) -> dict[int, dict[str, float]]:
    """N: the conditional null true by construction (two moving-average forecasts, ZT Ex. 2)."""
    print("\nN. Conditional null true by construction (two moving-average forecasts, ZT Example 2)")
    R_N = 10_000
    rng = np.random.default_rng(20261111)
    resN = {}
    momN = []
    for n in (120, 1000):
        rej: dict[str, list[NDArray[np.bool_]]] = {"(1, dL_t)": [], "(1, f1 - f2)": []}
        for _chunk in range(5):
            reps = R_N // 5
            # n + 1 loss differences: the first serves only as the lagged instrument
            L = M_N - 1 + n + 1
            f1 = moving_average(ar1(rng, (reps, L), PHI, BURN), M_N)
            f2 = moving_average(ar1(rng, (reps, L), PHI, BURN), M_N)
            y = (f1 + f2) / 2 + rng.standard_normal(f1.shape)
            dl = (y - f1) ** 2 - (y - f2) ** 2
            cur, lag = dl[:, 1:], dl[:, :-1]
            Zi = np.stack([cur, lag * cur], axis=-1)
            Zii = np.stack([cur, (f1 - f2)[:, 1:] * cur], axis=-1)
            rej["(1, dL_t)"].append(gw(Zi) > CRIT2)
            rej["(1, f1 - f2)"].append(gw(Zii) > CRIT2)
            if n == 1000:
                momN.append(Zi.mean(axis=1))
        resN[n] = {k: float(np.mean(np.concatenate(v))) for k, v in rej.items()}
        for k, p in resN[n].items():
            print(f"  n = {n:4d}, h = {k:13s}: rejection {p:.4f} (mc se {mc(p, R_N):.4f})")
    moments = np.concatenate(momN)
    for i, lab in enumerate(("dL", "dL_t dL")):
        mean, se = moments[:, i].mean(), moments[:, i].std(ddof=1) / np.sqrt(R_N)
        report.ok(
            f"N pooled mean of Z component {lab} within 3 se of 0 (n = 1000)",
            bool(abs(mean) < 3 * se),
            f"{mean:+.5f} (se {se:.5f})",
        )
    report.ok(
        "N rejection with h = (1, dL_t), n = 1000, within 0.015 of 0.05",
        abs(resN[1000]["(1, dL_t)"] - 0.05) <= 0.015,
        f"{resN[1000]['(1, dL_t)']:.4f}",
    )
    return resN


def check_unconditional_null(report: CheckReport) -> tuple[dict[int, dict[str, float]], float]:
    """U: unconditional null true, conditional null false (ZT Example 4, Gaussian, m = 4).

    Returns:
        The rejection rates at each n, and the variance of the signed statistic at n = 1000.
    """
    print("\nU. Unconditional null true, conditional null false (ZT Example 4, Gaussian, m = 4)")
    rng = np.random.default_rng(20261112)
    resU = {}
    momU, varU = np.empty((0, 4)), float("nan")
    for n in (120, 1000):
        out: dict[str, list[NDArray[np.bool_]]] = {
            k: []
            for k in (
                "U-a mds",
                "U-b uniform HAC",
                "U-c Newey-West",
                "U-d subsample K=4",
                "U-e (1, f1)",
                "U-e (1, f1^2)",
            )
        }
        nonpos, signed, mom = 0, [], []
        lag_nw = int(np.floor(0.75 * n ** (1 / 3)))
        for _chunk in range(5):
            reps = R_U // 5
            y = C_U + rng.standard_normal((reps, M_U + n))
            # origins t = m-1 .. m+n-2, forecasts of y[:, m: m+n]
            f1 = moving_average(y[:, :-1], M_U)
            yt = y[:, M_U:]
            dl = (yt - f1) ** 2 - yt**2
            losses = LossDifferences.of(dl)
            out["U-a mds"].append(gw(dl[..., None]) > CRIT1)
            tb, vb = losses.hac_t(M_U, "uniform")
            bad = ~(vb > 0)
            nonpos += int(bad.sum())
            if bad.any():
                tb[bad] = LossDifferences.of(dl[bad]).hac_t(M_U, "bartlett")[0]
            out["U-b uniform HAC"].append(np.abs(tb) > Z975)
            out["U-c Newey-West"].append(np.abs(losses.hac_t(lag_nw, "bartlett")[0]) > Z975)
            out["U-d subsample K=4"].append(
                np.abs(losses.subsample_t(4)) > stats.t.ppf(1 - ALPHA / 2, 3)
            )
            out["U-e (1, f1)"].append(gw(np.stack([dl, f1 * dl], axis=-1)) > CRIT2)
            out["U-e (1, f1^2)"].append(gw(np.stack([dl, f1**2 * dl], axis=-1)) > CRIT2)
            signed.append(losses.signed_gw())
            mom.append(
                np.column_stack(
                    [dl.mean(1), (dl**2).mean(1), (f1 * dl).mean(1), (f1**2 * dl).mean(1)]
                )
            )
        resU[n] = {k: float(np.mean(np.concatenate(v))) for k, v in out.items()}
        print(
            f"  n = {n}: Newey-West lag {lag_nw}; uniform HAC not positive in {nonpos} samples"
            " (Bartlett used)"
        )
        for k, p in resU[n].items():
            print(f"    {k:20s} rejection {p:.4f} (mc se {mc(p, R_U):.4f})")
        all_signed = np.concatenate(signed)
        print(
            f"    variance of signed GW_T {all_signed.var(ddof=1):.4f}; ZT Proposition 6 V_4 ="
            f" 88/130 = {88 / 130:.4f}"
        )
        if n == 1000:
            momU, varU = np.concatenate(mom), float(all_signed.var(ddof=1))
    for i, (lab, target) in enumerate(
        (("dL", 0.0), ("dL^2", 8 / M_U + 2 / M_U**2), ("f1 dL", 0.0), ("f1^2 dL", 2 / M_U**2))
    ):
        mean, se = momU[:, i].mean(), momU[:, i].std(ddof=1) / np.sqrt(R_U)
        report.ok(
            f"U pooled mean of {lab} within 3 se of {target:g} (n = 1000)",
            bool(abs(mean - target) < 3 * se),
            f"{mean:+.5f} (se {se:.5f})",
        )
    for k in ("U-b uniform HAC", "U-d subsample K=4"):
        report.ok(
            f"U {k} rejection, n = 1000, within 0.02 of 0.05",
            abs(resU[1000][k] - 0.05) <= 0.02,
            f"{resU[1000][k]:.4f}",
        )
    return resU, varU


def check_methods(report: CheckReport) -> tuple[float, float, float]:
    """C: equal population models, unequal methods; return mean dL and the two rejection rates."""
    print(
        "\nC. Equal population models, unequal methods (rolling mean vs rolling OLS on an"
        " irrelevant predictor)"
    )
    M_C, MU_C, R_C, n_C = 20, 0.5, 2_000, 1000
    rng = np.random.default_rng(20261113)
    mC_parts, cross_parts, rej_cond, rej_sub = [], [], [], []
    spot_gap = float("nan")
    for chunk in range(4):
        reps = R_C // 4
        N = M_C + n_C + 1  # origins M_C .. M_C + n_C, n_C + 1 loss differences
        x = ar1(rng, (reps, N + 1), PHI, BURN)
        y = MU_C + rng.standard_normal((reps, N + 1))
        # pairs (x_s, y_{s+1}); window for origin t: s = t-20 .. t-1
        xs_, ys_ = x[:, :-1], y[:, 1:]
        sx, sy, sxx, sxy = (M_C * moving_average(v, M_C) for v in (xs_, ys_, xs_ * xs_, xs_ * ys_))
        xbar, ybar = sx / M_C, sy / M_C
        b = (sxy - M_C * xbar * ybar) / (sxx - M_C * xbar**2)
        origin_x = x[:, M_C : M_C + b.shape[1]]
        d = origin_x - xbar
        fM, fD = ybar, ybar + b * d
        target = y[:, M_C + 1 : M_C + 1 + b.shape[1]]
        k = min(fM.shape[1], target.shape[1])
        fM, fD, target, b, d, ybar = (
            fM[:, :k],
            fD[:, :k],
            target[:, :k],
            b[:, :k],
            d[:, :k],
            ybar[:, :k],
        )
        dl = (target - fM) ** 2 - (target - fD) ** 2
        dl = dl[:, : n_C + 1]
        cross = (2 * (MU_C - ybar) * b * d)[:, 1 : n_C + 1]
        cur, lag = dl[:, 1:], dl[:, :-1]
        mC_parts.append(cur.mean(1))
        cross_parts.append(cross.mean(1))
        rej_cond.append(gw(np.stack([cur, lag * cur], axis=-1)) > CRIT2)
        rej_sub.append(
            np.abs(LossDifferences.of(cur).subsample_t(4)) > stats.t.ppf(1 - ALPHA / 2, 3)
        )
        if chunk == 3:
            # spot check the last replication's last forecast against lstsq on its window
            Zw = np.column_stack([np.ones(M_C), xs_[-1, k - 1 : k - 1 + M_C]])
            coef = np.linalg.lstsq(Zw, ys_[-1, k - 1 : k - 1 + M_C], rcond=None)[0]
            spot_gap = float(coef[0] + coef[1] * x[-1, M_C + k - 1] - fD[-1, k - 1])
    mC, crossC = np.concatenate(mC_parts), np.concatenate(cross_parts)
    report.ok("C rolling OLS by window sums = lstsq (one window)", abs(spot_gap) < 1e-10)
    seC = mC.std(ddof=1) / np.sqrt(R_C)
    report.ok(
        "C pooled mean dL = L_M - L_D below zero by > 3 se",
        bool(mC.mean() < -3 * seC),
        f"{mC.mean():+.5f} (se {seC:.5f})",
    )
    seX = crossC.std(ddof=1) / np.sqrt(R_C)
    report.ok(
        "C pooled mean of 2(mu - ybar) b d within 3 se of 0",
        bool(abs(crossC.mean()) < 3 * seX),
        f"{crossC.mean():+.5f} (se {seX:.5f})",
    )
    pc, ps = float(np.mean(np.concatenate(rej_cond))), float(np.mean(np.concatenate(rej_sub)))
    print(
        f"  n = {n_C}, R = {R_C}: conditional h = (1, dL_t) rejects {pc:.4f} (mc se"
        f" {mc(pc, R_C):.4f}); subsample t rejects {ps:.4f} (mc se {mc(ps, R_C):.4f}); mean dL /"
        f" mean dL^2 scale: {mC.mean():+.5f}"
    )
    return float(mC.mean()), pc, ps


def check_expanding_window(gates: ReproductionGates) -> dict[float, float]:
    """X: GW_T with the mds variance against 1.96 under an expanding window (ZT Example 5)."""
    print("\nX. Expanding window (ZT Example 5): GW_T with the mds variance against 1.96")
    rng = np.random.default_rng(20261114)
    resX = {}
    for lam, published in ((0.25, 0.196), (0.5, 0.158)):
        m = int(lam * T_X)
        rej = []
        for _chunk in range(5):
            reps = R_X // 5
            y = rng.standard_normal((reps, T_X))
            tt = np.arange(1, T_X + 1)
            f1 = np.cumsum(y, axis=1) / tt  # forecast made at t (1-based) from y_1..y_t
            f2 = tt**-0.5
            org = slice(m - 1, T_X - 1)  # origins t = m .. T-1 (1-based)
            dl = (y[:, m:] - f1[:, org]) ** 2 - (y[:, m:] - f2[org]) ** 2
            rej.append(np.abs(LossDifferences.of(dl).signed_gw()) > Z975)
        p = float(np.mean(np.concatenate(rej)))
        resX[lam] = p
        print(
            f"  lambda = {lam}: rejection {p:.4f} (mc se {mc(p, R_X):.4f}); ZT Table 2 asymptotic"
            f" {published}"
        )
        # The protocol's gate "rejection exceeds 0.10" is kept with its original criterion and
        # reported as a reproduction outcome; see the protocol and part P below.
        gates.record(f"X lambda = {lam}: rejection exceeds 0.10 (ZT Table 2)", p > 0.10, f"{p:.4f}")
    return resX


def check_equity_premium(
    report: CheckReport, raw: LabelledTable
) -> dict[tuple[int, str], tuple[float, float, float, float, float, float, float, int]]:
    """E: the annual log equity premium, rolling 20-year mean against rolling regression on dp."""
    print(
        "\nE. Annual log equity premium: rolling 20-year mean (M) vs rolling 20-year regression on"
        " dp (D)"
    )
    first = FIRST_FORECAST - FIRST_OUTCOME
    years = np.arange(FIRST_OUTCOME, LAST + 1)

    def build(table: LabelledTable) -> tuple[Floats, Floats]:
        dp = np.log(table["D12"]) - np.log(table["Index"])
        y = 100 * (np.log1p(table["CRSP_SPvw"]) - np.log1p(table["Rfree"]))
        return table.at(y, years), table.at(dp, years - 1)

    yE, xE = build(raw)
    fc = RollingForecasts.of(years, yE, xE, M_E, first)
    # E1. closed form against lstsq
    diffs = []
    for i in range(first, len(yE)):
        Zw = np.column_stack([np.ones(M_E), xE[i - M_E : i]])
        cf = np.linalg.lstsq(Zw, yE[i - M_E : i], rcond=None)[0]
        diffs.append(abs(cf[0] + cf[1] * xE[i] - fc.fD[fc.at(int(years[i]))]))
    report.ok(
        "E1 rolling OLS closed form = lstsq per window",
        max(diffs) < 1e-10,
        f"max |diff| {max(diffs):.1e}",
    )
    # E2. chronological indexing
    for cut in (1970, 2000):
        later = raw.labels > cut
        reversed_columns = {}
        for c, col in raw.columns.items():
            col = col.copy()
            col[later] = col[later][::-1] * 1.7
            reversed_columns[c] = col
        fc2 = RollingForecasts.of(
            years, *build(LabelledTable(labels=raw.labels, columns=reversed_columns)), M_E, first
        )
        keep = fc.years <= cut + 1
        dmax = float(
            np.max(
                np.abs(
                    np.column_stack([fc2.fM, fc2.fD, fc2.s2M, fc2.s2D])[keep]
                    - np.column_stack([fc.fM, fc.fD, fc.s2M, fc.s2D])[keep]
                )
            )
        )
        report.ok(
            f"E2 forecasts through {cut + 1} unchanged when later rows are overwritten",
            dmax == 0.0,
            f"max |diff| {dmax:.1e}",
        )
    # E3. the 1947 forecasts equal the recursive ones (same 20 observations), by running sums
    nn = first
    sx, sy, sxx, sxy = (
        xE[:first].sum(),
        yE[:first].sum(),
        (xE[:first] ** 2).sum(),
        (xE[:first] * yE[:first]).sum(),
    )
    b_rec = (nn * sxy - sx * sy) / (nn * sxx - sx**2)
    f_rec = (sy - b_rec * sx) / nn + b_rec * xE[first]
    i47 = fc.at(1947)
    report.ok(
        "E3 1947 forecasts equal the recursive ones of the forecast-combination check",
        bool(abs(f_rec - fc.fD[i47]) < 1e-12 and abs(sy / nn - fc.fM[i47]) < 1e-12),
        f"M {fc.fM[i47]:.2f}, D {fc.fD[i47]:.2f} percent",
    )
    # E4. CRPS closed form against quadrature
    mu0, s0, x0 = float(fc.fD[i47]), float(np.sqrt(fc.s2D[i47])), float(fc.y[i47])
    quad = (
        integrate.quad(lambda u: (stats.norm.cdf(u, mu0, s0) - (u >= x0)) ** 2, -np.inf, x0)[0]
        + integrate.quad(lambda u: (stats.norm.cdf(u, mu0, s0) - 1) ** 2, x0, np.inf)[0]
    )
    report.ok(
        "E4 Gaussian CRPS closed form = quadrature (1947, D)",
        abs(NormalForecast(mean=mu0, sd=s0).crps(x0) - quad) < 1e-7,
        f"{quad:.6f}",
    )
    losses = {
        "seM": (fc.y - fc.fM) ** 2,
        "seD": (fc.y - fc.fD) ** 2,
        "crM": NormalForecast(mean=fc.fM, sd=np.sqrt(fc.s2M)).crps(fc.y),
        "crD": NormalForecast(mean=fc.fD, sd=np.sqrt(fc.s2D)).crps(fc.y),
    }
    print(
        "  forecasts (percent): "
        + "; ".join(
            f"{yr}: y {fc.y[fc.at(yr)]:.2f}, M {fc.fM[fc.at(yr)]:.2f}, D {fc.fD[fc.at(yr)]:.2f}"
            for yr in (1947, 1970, 1990, 2010, 2025)
        )
    )
    resE = {}
    for end in (2025, 2005):
        sub = fc.years <= end
        n = int(sub.sum())
        lag = int(np.floor(0.75 * n ** (1 / 3)))
        r2 = 100 * (1 - losses["seD"][sub].sum() / losses["seM"][sub].sum())
        print(
            f"\n  Evaluation 1947-{end}: n = {n}, Newey-West lag {lag}, R2_OS of D against M"
            f" {r2:.2f}%"
        )
        print("  loss       mean dL   DM t (NW)  p      mds t   p      cond. T  p      (n cond.)")
        for loss, cM, cD in (("squared", "seM", "seD"), ("CRPS", "crM", "crD")):
            dl = losses[cM][sub] - losses[cD][sub]
            series = LossDifferences.of(dl)
            tnw = float(series.hac_t(lag, "bartlett")[0])
            tm = float(series.signed_gw())
            Zc = InstrumentedLosses(Z=np.column_stack([dl[1:], dl[:-1] * dl[1:]]))
            s_ = Zc.singular_values()
            Tc = float(Zc.statistic())
            row = (
                float(dl.mean()),
                tnw,
                float(2 * stats.norm.sf(abs(tnw))),
                tm,
                float(2 * stats.norm.sf(abs(tm))),
                Tc,
                float(stats.chi2.sf(Tc, 2)),
                len(Zc.Z),
            )
            resE[(end, loss)] = row
            print(
                f"  {loss:8s} {row[0]:9.3f} {row[1]:9.2f} {row[2]:6.3f} {row[3]:7.2f}"
                f" {row[4]:6.3f} {row[5]:8.2f} {row[6]:6.3f}   {row[7]}"
            )
            report.ok(
                f"E5 instrument matrix full rank (1947-{end}, {loss})",
                bool(s_[-1] > 1e-10 * max(Zc.Z.shape) * s_[0]),
            )
    return resE


def zt_steps(pairs: int, m: Fraction, kappa2: int = 3) -> Fraction:
    """Return V_m by ZT's proof steps (eqs. (22)-(28)) with a pairing count for E xi^4."""
    c4 = 1 / m**2
    gd = [
        (2 * d * m - d**2 + pairs * (m - d) * (m - d - 1) + (m - d) * kappa2) / m**4
        - c4
        - 4 * (m - d) / m**3
        for d in range(1, int(m))
    ]
    g0_ = (pairs * (m - 1) + kappa2) / m**3 - c4 + 8 / m
    return (g0_ + 2 * sum(gd, Fraction(0))) / g0_


def check_supplements(
    report: CheckReport, varU: float, resU: dict[int, dict[str, float]], resX: dict[float, float]
) -> None:
    """P: supplements outside the protocol's verdicts: the exact V_4 and the Example 5 limit."""
    print("\nP. Post-run supplements (not part of the protocol's verdicts)")
    # P1. U design: exact variance ratio of the signed mds statistic for Gaussian errors.
    # dL_{t+1} = (v_t^2 - c^2) - 2 (c + v_t) eps_{t+1}; gamma_0 = 2/m^2 + 8/m and, for
    # 1 <= k <= m - 1, gamma_k = 2 (m - k)^2 / m^4 - 4 (m - k) / m^3, zero beyond. Hence
    # V_m = LRV / E dL^2 = (2m + 1) / (3m).
    m_ = Fraction(M_U)
    g0 = 2 / m_**2 + 8 / m_
    lrv_exact = g0 + 2 * sum(
        (2 * (m_ - k) ** 2 / m_**4 - 4 * (m_ - k) / m_**3 for k in range(1, M_U)), Fraction(0)
    )
    V_exact = lrv_exact / g0
    report.ok(
        "P1 exact V_4 = LRV / E dL^2 = (2m + 1)/(3m) = 3/4",
        V_exact == (2 * m_ + 1) / (3 * m_) == Fraction(3, 4),
        f"LRV {lrv_exact} = {float(lrv_exact):.5f}, E dL^2 {g0}",
    )
    # The same proof steps as printed in ZT (eqs. (22)-(28), pp. 24-26) write
    # E xi^4 = k(k - 1) + k kappa2 for a sum of k errors (eq. (23), p. 25, and before eq. (28),
    # p. 26); the Gaussian pairing count is 3 k(k - 1). Run through the printed steps at
    # kappa1 = 0, kappa2 = 3, the printed count gives Proposition 6's 88/130 and the factor 3
    # gives 3/4.
    report.ok(
        "P1 ZT proof steps (eqs. (22)-(28)) give 88/130 with the printed pairing count, 3/4 with"
        " the Gaussian factor 3",
        zt_steps(1, m_) == Fraction(88, 130) and zt_steps(3, m_) == V_exact,
        f"{zt_steps(1, m_)} and {zt_steps(3, m_)}",
    )
    se_var = varU * np.sqrt(2 / (R_U - 1))
    report.ok(
        "P1 simulated variance of signed GW_T (n = 1000) within 3 se of 3/4",
        bool(abs(varU - 0.75) < 3 * se_var),
        f"{varU:.4f} (se {se_var:.4f}); ZT Proposition 6 as printed: {88 / 130:.4f}",
    )
    p_pred = float(2 * stats.norm.sf(Z975 / np.sqrt(0.75)))
    report.ok(
        "P1 implied rejection of U-a, 2 P(|N(0, 3/4)| > 1.96), within 3 mc se of the simulated rate"
        " (n = 1000)",
        abs(resU[1000]["U-a mds"] - p_pred) < 3 * mc(p_pred, R_U),
        f"{p_pred:.4f} vs {resU[1000]['U-a mds']:.4f}",
    )
    # P2. X design: the limit of GW_T derived for Example 5 is A / (2 sqrt(I)) + N / sqrt(I), with
    # A = int (B^2/u^2 - 1/u) du, I = int (u^-1/2 - B/u)^2 du, N = int (u^-1/2 - B/u) dB over
    # [lambda, 1]; ZT eq. (14) prints the second term with a minus sign; the proof's eq. (30),
    # p. 28, has A + 2N over 2 sqrt(I), the plus sign. Both are simulated on a grid (seed
    # 20261115) and compared. Neither reproduces ZT Table 2.
    G_P, R_P = 2000, 10_000
    rng = np.random.default_rng(20261115)
    u = np.arange(1, G_P + 1) / G_P
    for lam in (0.25, 0.5):
        k0 = int(lam * G_P)
        plus, minus = [], []
        for _chunk in range(5):
            dB = rng.standard_normal((R_P // 5, G_P)) / np.sqrt(G_P)
            B = np.cumsum(dB, axis=1)
            A = ((B[:, k0:] ** 2 / u[k0:] ** 2 - 1 / u[k0:]) / G_P).sum(axis=1)
            g = u[k0 - 1 : -1] ** -0.5 - B[:, k0 - 1 : -1] / u[k0 - 1 : -1]
            I_ = (g**2 / G_P).sum(axis=1)
            N_ = (g * dB[:, k0:]).sum(axis=1)
            plus.append(A / (2 * np.sqrt(I_)) + N_ / np.sqrt(I_))
            minus.append(A / (2 * np.sqrt(I_)) - N_ / np.sqrt(I_))
        pp = float(np.mean(np.abs(np.concatenate(plus)) > Z975))
        pm = float(np.mean(np.abs(np.concatenate(minus)) > Z975))
        tol = 3 * np.sqrt(mc(pp, R_P) ** 2 + mc(resX[lam], R_X) ** 2)
        print(
            f"  lambda = {lam}: limit as derived {pp:.4f}, as printed in eq. (14) {pm:.4f}, T ="
            f" 2000 simulation {resX[lam]:.4f}"
        )
        report.ok(
            f"P2 lambda = {lam}: derived limit agrees with the T = 2000 simulation within 3"
            " combined mc se",
            bool(abs(pp - resX[lam]) < tol),
            f"|diff| {abs(pp - resX[lam]):.4f} < {tol:.4f}",
        )


def printed(row: tuple[float, float, float, float, float, float, float, int]) -> list[str]:
    """Return a row of part E as printed: mean dL (3 dp), DM t, p, mds t, p, conditional T, p."""
    return [
        f"{row[0]:.3f}",
        f"{row[1]:.2f}",
        f"{row[2]:.3f}",
        f"{row[3]:.2f}",
        f"{row[4]:.3f}",
        f"{row[5]:.2f}",
        f"{row[6]:.3f}",
    ]


class Recorded(Record):
    """The values the recorded-value checks compare with the first run.

    Attributes:
        T_exact: Part V's hand statistic.
        states: Part H's unconditional and conditional rejection rates.
        resN: Part N's rejection rates.
        resU: Part U's rejection rates.
        methods: Part C's mean loss difference and its two rejection rates.
        resX: Part X's rejection rates.
        resE: Part E's rows.
    """

    T_exact: Fraction
    states: tuple[float, float]
    resN: dict[int, dict[str, float]]
    resU: dict[int, dict[str, float]]
    methods: tuple[float, float, float]
    resX: dict[float, float]
    resE: dict[tuple[int, str], tuple[float, float, float, float, float, float, float, int]]


def check_recorded(report: CheckReport, rec: Recorded) -> None:
    """R: the first run's values, at their printed rounding."""
    print("\nR. Recorded values")
    report.ok("R V1 hand statistic", rec.T_exact == Fraction(3087, 2005))
    report.ok(
        "R H rejection rates", [round(rec.states[0], 4), round(rec.states[1], 4)] == [0.0518, 1.0]
    )
    report.ok(
        "R N rejection rates n = 120, 1000",
        [round(rec.resN[n][k], 4) for n in (120, 1000) for k in ("(1, dL_t)", "(1, f1 - f2)")]
        == [0.0417, 0.0443, 0.0465, 0.0508],
    )
    report.ok(
        "R U rejection rates n = 1000 (U-a..U-e)",
        [round(v, 4) for v in rec.resU[1000].values()]
        == [0.0237, 0.0552, 0.0444, 0.0459, 0.0442, 0.7881],
    )
    report.ok(
        "R U rejection rates n = 120 (U-a..U-e)",
        [round(v, 4) for v in rec.resU[120].values()]
        == [0.0264, 0.0931, 0.0476, 0.0503, 0.0611, 0.1423],
    )
    report.ok(
        "R C pooled mean dL and rejection rates",
        [round(v, 4) for v in rec.methods] == [-0.0969, 0.9985, 0.9825],
    )
    report.ok(
        "R X rejection rates (failed reproduction of ZT Table 2)",
        [round(rec.resX[0.25], 4), round(rec.resX[0.5], 4)] == [0.0567, 0.0538],
    )
    report.ok(
        "R E rows as printed",
        [
            printed(rec.resE[k])
            for k in ((2025, "squared"), (2025, "CRPS"), (2005, "squared"), (2005, "CRPS"))
        ]
        == [
            ["9.865", "0.50", "0.618", "0.38", "0.703", "2.73", "0.255"],
            ["0.116", "0.31", "0.754", "0.23", "0.816", "3.01", "0.222"],
            ["3.377", "0.14", "0.887", "0.11", "0.910", "2.63", "0.269"],
            ["-0.001", "-0.00", "0.999", "-0.00", "0.999", "2.76", "0.251"],
        ],
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Print the versions, run the parts in order with one report, and print the summary.

    Worked numbers of meth:conditional-predictive-ability, under
    conditional-predictive-ability-protocol.md (designs, instruments, windows, losses, seeds and
    acceptance criteria written before the first run). Sources: Giacomini and White, "Tests of
    conditional predictive ability", authors' version of April 2006 (giacomini-white-2006-wp);
    Zhu and Timmermann, arXiv:2006.03238v2 (zhu-timmermann-2022-arxiv).

    Data: goyal-annual-predictors-1871-2025.csv, extracted by
    trading_notes.research.return_predictability.goyal_extract_predictors from
    the workbook on Amit Goyal's page labelled "Original data (up to 2005) used in the paper",
    served in 2026 with data to 2025 (a 2026 vintage). Synthetic data from seeds
    20261109-20261115.

    Independent routes: the Wald statistic by exact rational arithmetic, by a linear solve and
    as n R^2 of an artificial regression (GW comment 7); chi-square tails against the closed
    form for two degrees of freedom; long-run variances against hand loops; simulated moments
    against moments derived in the protocol; rolling forecasts against lstsq refits and against
    the recursive forecasts for the first window.

    The summary splits the checks into the protocol's correctness checks (parts V-E), the
    supplements (P) and the recorded values (R). The two part X gates of the first run, which
    expected ZT Table 2 to reproduce and failed, are reproduction outcomes: they are reported
    against their original criterion and not counted as checks (protocol, "Amendment, 23
    October 2026"). Recorded output: conditional-predictive-ability-results.txt.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np, pd, scipy)
    raw = LabelledTable.read(root / DATA, "yyyy")
    report = CheckReport()
    gates = ReproductionGates()
    T_exact = check_validation(report)
    states = check_states(report)
    resN = check_conditional_null(report)
    resU, varU = check_unconditional_null(report)
    methods = check_methods(report)
    resX = check_expanding_window(gates)
    resE = check_equity_premium(report, raw)
    n_protocol = report.count
    check_supplements(report, varU, resU, resX)
    n_post = report.count
    check_recorded(
        report,
        Recorded(
            T_exact=T_exact,
            states=states,
            resN=resN,
            resU=resU,
            methods=methods,
            resX=resX,
            resE=resE,
        ),
    )
    print(
        f"\nCorrectness and regression checks: {report.count} run, {len(report.failures)} failed"
        f" (protocol parts V-E {n_protocol}, post-run supplements P {n_post - n_protocol},"
        f" recorded values R {report.count - n_post})"
    )
    repro = gates.gates
    print(
        f"Historical reproduction gates, first-run criteria, not counted above: {len(repro)}"
        f" evaluated, {sum(met for _, met, _ in repro)} met"
    )
    for name, met, detail in repro:
        print(f"  {'met' if met else 'NOT MET'}: {name}: {detail}")
    print(
        "  ZT Table 2 (0.196, 0.158) is not reproduced; the first run counted these gates as 2"
        " failures of 41 checks."
    )
    if report.failures:
        print("FAILED: " + "; ".join(report.failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
