"""Brownian motion, Ito's lemma and risk-neutral pricing, checked on model-generated data.

Library gap-filling Batch L1, package P1 (2026-10-21): the worked examples of
def:brownian-motion-quadratic-variation, res:ito-lemma-geometric-brownian-motion and
res:risk-neutral-pricing-feynman-kac.

Every check uses model-generated data with a known answer: S0 = 100, mu = 8 percent, sigma = 20
percent, T = 1 unless stated. Seeds (20261021 and offsets) and tolerances (four standard errors,
or three for the Girsanov price) were fixed before any run and are not tuned. The checks show
that the formulas are implemented correctly under the model; they are not evidence about
markets.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.stochastic_calculus
(numpy, scipy). Exits 1 on failure.
"""

import math
import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import stats

from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

SEED: Final = 20261021  # Brownian motion; SEED + 1 to SEED + 3 for the later sections
S0: Final = 100.0
MU: Final = 0.08
SG: Final = 0.20
T: Final = 1.0
M: Final = 200_000  # exact draws for the GBM and Girsanov checks
K: Final = 105.0  # the call's strike
R: Final = 0.03


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def check_brownian_motion(report: CheckReport, rng: np.random.Generator) -> None:
    """Quadratic and first variation of one path, refined, and the Ito and midpoint sums."""
    print("== Brownian motion and quadratic variation")
    n = 10_000
    dW = rng.standard_normal(n) * math.sqrt(T / n)
    W = np.concatenate(([0.0], np.cumsum(dW)))
    qv = float(np.sum(dW**2))
    qv_sd = math.sqrt(2 / n) * T
    report.ok(
        "quadratic variation of W on [0, 1], 10,000 steps, within 4 s.d. (sqrt(2/n) = 0.0141) of 1",
        abs(qv - T) <= 4 * qv_sd,
        f"{qv:.5f}",
    )
    # Halving the step quarters the variance of the sum of squared increments: refine the same
    # path by Brownian-bridge midpoints, so the coarse and fine sums use one path.
    mid = 0.5 * (W[:-1] + W[1:]) + rng.standard_normal(n) * math.sqrt(T / n / 4)
    fine = np.empty(2 * n + 1)
    fine[0::2], fine[1::2] = W, mid
    qv_fine = float(np.sum(np.diff(fine) ** 2))
    report.ok(
        "on the refined path (20,000 steps) quadratic variation is within 4 s.d. (0.0100) of 1",
        abs(qv_fine - T) <= 4 * math.sqrt(2 / (2 * n)),
        f"{qv_fine:.5f}",
    )
    abs_var = float(np.sum(np.abs(dW)))
    report.ok(
        "first variation sum |dW| grows like sqrt(2n/pi) (79.8 at n = 10,000): paths have"
        " unbounded length",
        abs(abs_var - math.sqrt(2 * n / math.pi) * T**0.5) <= 4 * math.sqrt(1 - 2 / math.pi),
        f"{abs_var:.2f}",
    )
    ito_int = float(np.sum(W[:-1] * dW))
    report.ok(
        "left-point sum of W dW equals (W_T^2 - [W]_T)/2 exactly, and so is near (W_T^2 - T)/2",
        bool(
            close(ito_int, 0.5 * (W[-1] ** 2 - qv), 1e-9)
            and abs(ito_int - 0.5 * (W[-1] ** 2 - T)) <= 4 * 0.5 * qv_sd
        ),
        f"{ito_int:.5f} against {0.5 * (W[-1] ** 2 - T):.5f}",
    )
    report.ok(
        "the midpoint (Stratonovich-type) sum gives W_T^2 / 2 with no -T/2 term",
        close(float(np.sum(0.5 * (W[:-1] + W[1:]) * dW)), 0.5 * W[-1] ** 2, 1e-9),
    )


def check_gbm(report: CheckReport, rng: np.random.Generator) -> None:
    """The exact GBM's mean, median and log return, and E[S_T^2] by Ito's lemma."""
    print("== Ito's lemma and geometric Brownian motion")
    z = rng.standard_normal(M)
    ST = S0 * np.exp((MU - SG**2 / 2) * T + SG * math.sqrt(T) * z)
    mean_exact = S0 * math.exp(MU * T)
    median_exact = S0 * math.exp((MU - SG**2 / 2) * T)
    report.ok("exact mean S0 e^(mu T) = 108.33", close(mean_exact, 108.328707, 1e-5))
    report.ok(
        "exact median S0 e^((mu - sigma^2/2) T) = 106.18", close(median_exact, 106.183655, 1e-5)
    )
    m_se = ST.std(ddof=1) / math.sqrt(M)
    report.ok(
        "200,000 exact draws: sample mean within 4 s.e. of 108.33",
        bool(abs(ST.mean() - mean_exact) <= 4 * m_se),
        f"{ST.mean():.4f} (s.e. {m_se:.4f})",
    )
    dens = stats.lognorm.pdf(median_exact, SG * math.sqrt(T), scale=median_exact)
    med_se = 1 / (2 * dens * math.sqrt(M))
    report.ok(
        "sample median within 4 s.e. (1/(2 f(m) sqrt(M))) of 106.18",
        bool(abs(np.median(ST) - median_exact) <= 4 * med_se),
        f"{np.median(ST):.4f} (s.e. {med_se:.4f})",
    )
    report.ok(
        "mean log return is mu - sigma^2/2 = 6 percent, not mu",
        bool(abs(np.mean(np.log(ST / S0)) - 0.06) <= 4 * SG / math.sqrt(M)),
    )
    # Ito on S^2: d(S^2) = (2 mu + sigma^2) S^2 dt + 2 sigma S^2 dW, so
    # E[S_T^2] = S0^2 e^((2 mu + sigma^2) T).
    s2_exact = S0**2 * math.exp((2 * MU + SG**2) * T)
    s2 = ST**2
    s2_se = s2.std(ddof=1) / math.sqrt(M)
    report.ok(
        "E[S_T^2] = S0^2 e^((2 mu + sigma^2) T) = 12,214.03", close(s2_exact, 12214.027582, 1e-5)
    )
    report.ok(
        "simulated E[S_T^2] within 4 s.e.",
        bool(abs(s2.mean() - s2_exact) <= 4 * s2_se),
        f"{s2.mean():.2f} (s.e. {s2_se:.2f})",
    )
    report.ok(
        "the ordinary chain rule (no sigma^2 term) would give 11,735.11, rejected by the"
        " simulation",
        bool(abs(s2.mean() - S0**2 * math.exp(2 * MU * T)) > 10 * s2_se),
    )


def euler(dw: Floats) -> Floats:
    """Return S_T by Euler steps of dS = mu S dt + sigma S dW, one column of dw per step."""
    s = np.full(dw.shape[0], S0)
    h = T / dw.shape[1]
    for k in range(dw.shape[1]):
        s = s * (1 + MU * h + SG * dw[:, k])
    return s


def check_euler(report: CheckReport, rng: np.random.Generator) -> None:
    """Euler's RMS error to the exact GBM at 50 and 5,000 steps on the same increments."""
    # Euler steps of the SDE converge to the exact solution as the step shrinks. Compare 2,000
    # paths at 50 and 5,000 steps driven by the same Brownian increments.
    paths, steps = 2_000, 5_000
    dWf = rng.standard_normal((paths, steps)) * math.sqrt(T / steps)
    exact = S0 * np.exp((MU - SG**2 / 2) * T + SG * dWf.sum(1))
    coarse = euler(dWf.reshape(paths, 50, steps // 50).sum(2))
    finer = euler(dWf)
    e_c = math.sqrt(np.mean((coarse - exact) ** 2))
    e_f = math.sqrt(np.mean((finer - exact) ** 2))
    report.ok(
        "Euler scheme on the same Brownian paths: RMS error to the exact GBM falls as the step"
        " shrinks",
        e_f < e_c / 5,
        f"{e_c:.4f} at 50 steps, {e_f:.4f} at 5,000",
    )


def check_girsanov(report: CheckReport, rng: np.random.Generator) -> float:
    """The BSM call, and real-world draws reweighted by Z_T; return the BSM price."""
    print("== Risk-neutral pricing, Girsanov and Feynman-Kac")
    d1 = (math.log(S0 / K) + (R + SG**2 / 2) * T) / (SG * math.sqrt(T))
    d2 = d1 - SG * math.sqrt(T)
    bsm = S0 * stats.norm.cdf(d1) - K * math.exp(-R * T) * stats.norm.cdf(d2)
    report.ok("BSM call (K = 105, r = 3 percent, q = 0) = 7.1281", close(bsm, 7.128065, 1e-5))
    theta = (MU - R) / SG
    report.ok("market price of risk theta = (mu - r)/sigma = 0.25", close(theta, 0.25, 1e-12))
    WT = rng.standard_normal(M) * math.sqrt(T)
    ST_p = S0 * np.exp((MU - SG**2 / 2) * T + SG * WT)  # real-world draws
    Z = np.exp(-theta * WT - 0.5 * theta**2 * T)
    report.ok(
        "density Z_T has mean 1 under P (within 4 s.e.)",
        bool(abs(Z.mean() - 1) <= 4 * Z.std(ddof=1) / math.sqrt(M)),
        f"{Z.mean():.5f}",
    )
    g = math.exp(-R * T) * Z * np.maximum(ST_p - K, 0)
    g_se = g.std(ddof=1) / math.sqrt(M)
    report.ok(
        "real-world draws reweighted by Z_T reproduce the BSM call within 3 s.e.",
        bool(abs(g.mean() - bsm) <= 3 * g_se),
        f"{g.mean():.4f} (s.e. {g_se:.4f})",
    )
    report.ok(
        "reweighted drift: E_P[Z_T S_T] = S0 e^(r T), the risk-neutral forward",
        bool(
            abs(np.mean(Z * ST_p) - S0 * math.exp(R * T))
            <= 4 * (Z * ST_p).std(ddof=1) / math.sqrt(M)
        ),
    )
    plain = math.exp(-R * T) * np.maximum(ST_p - K, 0)
    report.ok(
        "discounting the unweighted real-world expectation at r overstates the price",
        bool(plain.mean() - bsm > 10 * plain.std(ddof=1) / math.sqrt(M)),
        f"{plain.mean():.4f} against {bsm:.4f}",
    )
    return bsm


# Feynman-Kac: V(S, t) = e^{-r tau} E[payoff] under dS = m S dt + sigma S dW solves
# V_t + 0.5 sigma^2 S^2 V_SS + m S V_S - r V = 0. With m = mu it is not a price; with m = r it is
# BSM.
def disc_exp(S: float, tau: float, m: float) -> float:
    """Return e^{-r tau} E[(S_T - K)^+] when S drifts at m."""
    a1 = (math.log(S / K) + (m + SG**2 / 2) * tau) / (SG * math.sqrt(tau))
    a2 = a1 - SG * math.sqrt(tau)
    return math.exp(-R * tau) * (
        S * math.exp(m * tau) * stats.norm.cdf(a1) - K * stats.norm.cdf(a2)
    )


def pde_residual(
    m: float, drift: float, S: float = 100.0, tau: float = 0.5, h: float = 1e-2, k: float = 1e-5
) -> float:
    """Return the PDE residual of disc_exp(., ., m) with drift term `drift` S V_S.

    The derivatives are central differences with steps h in S and k in tau.
    """
    v = disc_exp(S, tau, m)
    v_s = (disc_exp(S + h, tau, m) - disc_exp(S - h, tau, m)) / (2 * h)
    v_ss = (disc_exp(S + h, tau, m) - 2 * v + disc_exp(S - h, tau, m)) / h**2
    v_t = -(disc_exp(S, tau + k, m) - disc_exp(S, tau - k, m)) / (2 * k)
    return v_t + 0.5 * SG**2 * S**2 * v_ss + drift * S * v_s - R * v


def check_feynman_kac(report: CheckReport, bsm: float) -> None:
    """Which PDE each discounted expectation solves."""
    report.ok(
        "the discounted real-world expectation solves the PDE with mu S V_S (residual < 1e-5)",
        abs(pde_residual(MU, MU)) < 1e-5,
        f"{pde_residual(MU, MU):.2e}",
    )
    report.ok(
        "it fails the Black-Scholes PDE, whose drift term is r S V_S (residual > 1e-2)",
        abs(pde_residual(MU, R)) > 1e-2,
        f"{pde_residual(MU, R):.4f}",
    )
    report.ok(
        "the risk-neutral expectation (m = r) solves the Black-Scholes PDE and equals BSM at t = 0",
        abs(pde_residual(R, R)) < 1e-5 and close(disc_exp(S0, T, R), bsm, 1e-10),
    )


def main() -> int:
    """Print the versions, then run the sections with one report, each with its own seed.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_brownian_motion(report, np.random.default_rng(SEED))
    check_gbm(report, np.random.default_rng(SEED + 1))
    check_euler(report, np.random.default_rng(SEED + 2))
    bsm = check_girsanov(report, np.random.default_rng(SEED + 3))
    check_feynman_kac(report, bsm)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
