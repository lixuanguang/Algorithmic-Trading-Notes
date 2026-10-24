"""The seasoned variance swap added to meth:volatility-derivative-applications.

Library gap-filling Batch L4, package L4-b (2026-10-21).

Contract: N = 252 daily log returns r_i = ln(S_i / S_{i-1}), zero mean, annualisation A = 252,
realised variance RV = 10^4 (A/N) sum r_i^2 in variance points; K_vol = 20 vol points,
K_var = K_vol^2 = 400 points squared; vega notional 100,000, so
N_var = 100,000 / (2 K_vol) = 2,500 per point squared; payoff N_var (RV - K_var) at T.
After n returns, V_t = N_var P(t,T) [10^4 (A/N) sum_{i<=n} r_i^2 + ((N-n)/N) K_rem - K_var],
where K_rem is the fair variance strike of the remaining N - n returns of the same contract. A
labelled derivation from Demeterfi et al.'s definitions and additivity, not a formula printed
in the sources.

Example: n = 126, realised volatility 25 over them, quoted K_rem = 324, r = 4 percent
continuously compounded, q = 1 percent, T - t = 0.5. Under risk-neutral GBM with sigma = 18
percent the exact discrete K_rem is 10^4 [sigma^2 + (r - q - sigma^2/2)^2 / A]; option-strip
replication gives the continuous 324, reported separately with its deterministic difference.

Frozen before the first run: default_rng(20261021), 200,000 paths of 126 returns in four blocks
of 50,000; deterministic checks to 1e-6 currency or relative 1e-9; the simulated value within 4
standard errors of the value at the exact discrete K_rem. Synthetic inputs only: not evidence
about markets.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.seasoned_variance_swap
(numpy, scipy). Exits 1 on failure. About two seconds.
"""

# standard library imports
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, stats

# project library imports
from trading_notes.numerical.report import CheckReport

SEED: Final = 20261021
A: Final = 252  # annualisation
N: Final = 252  # returns in the contract
n: Final = 126  # returns observed so far
K_VOL: Final = 20.0
VEGA_NOTIONAL: Final = 100_000.0
K_VAR: Final = K_VOL**2
N_VAR: Final = VEGA_NOTIONAL / (2 * K_VOL)
R: Final = 0.04
Q: Final = 0.01
SIG_REM: Final = 0.18
K_REM_QUOTED: Final = 324.0
PTS: Final = 1e4  # variance points (vol points squared) per unit of decimal variance
TAU: Final = (N - n) / A


def rel(a: float, b: float) -> float:
    """Return |a - b| / |b|."""
    return abs(a - b) / abs(b)


@dataclass(frozen=True)
class RealisedLeg:
    """The returns observed so far.

    Attributes:
        ret: The n returns.
        sum_sq: The sum of their squares.
        rv: Their zero-mean realised variance over n, in points squared.
    """

    ret: NDArray[np.float64]
    sum_sq: float
    rv: float

    @classmethod
    def example(cls) -> RealisedLeg:
        """Return a deterministic series with a non-zero mean, scaled to realised volatility 25.

        The volatility is measured with zero mean.
        """
        raw = np.sin(1.7 * np.arange(1, n + 1)) + 0.15
        c = np.sqrt(0.25**2 * n / (A * np.sum(raw**2)))
        ret = c * raw
        sum_sq = float(np.sum(ret**2))
        return cls(ret, sum_sq, PTS * A / n * sum_sq)


def value(
    sum_sq_realised: float,
    n_obs: int,
    k_rem: float,
    tau: float,
    scale: float = PTS,
    n_var: float = N_VAR,
    k_var: float = K_VAR,
) -> float:
    """Return the seasoned value.

    Args:
        sum_sq_realised: The sum of squared returns observed so far (empty sum = 0).
        n_obs: The number of returns observed so far.
        k_rem: The fair strike of the remaining returns.
        tau: The time to expiry in years.
        scale: Variance units per unit of decimal variance.
        n_var: The variance notional.
        k_var: The variance strike.
    """
    disc = np.exp(-R * tau)
    return float(n_var * disc * (scale * A / N * sum_sq_realised + (N - n_obs) / N * k_rem - k_var))


def check_limits(report: CheckReport, leg: RealisedLeg) -> float:
    """1. The worked value, and the limits at inception and expiry; return the worked value."""
    print("== 1. limits and the worked value")
    v = value(leg.sum_sq, n, K_REM_QUOTED, TAU)
    print(
        f"  N_var = {N_VAR:,.1f} per point squared; realised RV over {n} returns ="
        f" {leg.rv:.6f} points^2"
    )
    report.ok(
        "worked value 2,500 e^{-0.02} (312.5 + 162 - 400) = 182,562.00",
        abs(v - 182_562.00) < 0.01,
        f"{v:,.4f}",
    )
    v0 = value(0.0, 0, K_VAR, N / A)
    report.ok(
        "inception (n = 0, empty realised sum, K_rem = K_var) is zero", abs(v0) <= 1e-6, f"{v0:.2e}"
    )
    # the series twice: 252 returns with realised RV 625
    full = np.sum(np.concatenate([leg.ret, leg.ret]) ** 2)
    v_T = value(
        full, N, 0.0, 0.0
    )  # the remaining term has weight zero, so its strike is irrelevant
    report.ok(
        "expiry (n = N, P = 1) equals the payoff N_var (RV - K_var)",
        abs(v_T - N_VAR * (625 - K_VAR)) <= 1e-6,
        f"{v_T:,.4f}",
    )
    return v


def check_units(report: CheckReport, leg: RealisedLeg, v: float) -> None:
    """2. Decimal variance units, and the vega notional as the payoff's slope at K_vol."""
    print("== 2. units and notionals")
    v_dec = value(
        leg.sum_sq, n, K_REM_QUOTED / PTS, TAU, scale=1.0, n_var=N_VAR * PTS, k_var=K_VAR / PTS
    )
    report.ok(
        "decimal variance with N_var x 10^4 gives the same value",
        rel(v_dec, v) <= 1e-9,
        f"{v_dec:,.4f}",
    )

    def payoff(s: float) -> float:
        return N_VAR * (s**2 - K_VAR)

    dP = (payoff(K_VOL + 1e-3) - payoff(K_VOL - 1e-3)) / 2e-3
    report.ok(
        "dPayoff/dsigma_R at K_vol = 2 K_vol N_var = vega notional",
        rel(dP, VEGA_NOTIONAL) <= 1e-9,
        f"{dP:,.4f}",
    )


def check_realised_leg(report: CheckReport, leg: RealisedLeg) -> None:
    """3. The observation weights from the data, and the contract alternatives reported."""
    print("== 3. realised leg from the return series")
    sum_sq = leg.sum_sq
    report.ok(
        "observation weights from data",
        rel(PTS * A / N * sum_sq, n / N * 625.0) <= 1e-9,
        f"{PTS * A / N * sum_sq:.6f} = (126/252) x 625",
    )
    dm = leg.ret - leg.ret.mean()
    print(
        f"  contract alternatives (reported): mean-subtracted over n"
        f" {PTS * A / n * np.sum(dm**2):.4f}, "
        f"over n - 1 {PTS * A / (n - 1) * np.sum(dm**2):.4f}, against zero-mean {leg.rv:.4f}"
        " points^2"
    )


@dataclass(frozen=True)
class DiscreteExpectation:
    """The one-day log-return moments under risk-neutral GBM and the values they give.

    Attributes:
        m_r: The mean daily log return.
        s_r: Its standard deviation.
        v_exact: The value at the exact discrete K_rem.
        v_cont: The value at the continuous approximation of K_rem.
    """

    m_r: float
    s_r: float
    v_exact: float
    v_cont: float


def check_discrete_expectation(report: CheckReport, leg: RealisedLeg) -> DiscreteExpectation:
    """4. E[r^2] by quadrature, and the exact discrete K_rem against the continuous one."""
    print("== 4. exact discrete expectation under risk-neutral GBM")
    dt = 1.0 / A
    mu = R - Q - SIG_REM**2 / 2
    m_r, s_r = mu * dt, SIG_REM * np.sqrt(dt)
    quad, _ = integrate.quad(
        lambda x: x * x * stats.norm.pdf(x, m_r, s_r),
        m_r - 12 * s_r,
        m_r + 12 * s_r,
        epsabs=0,
        epsrel=1e-13,
    )
    report.ok(
        "E[r^2] by quadrature = sigma^2 dt + mu^2 dt^2",
        rel(quad, s_r**2 + m_r**2) <= 1e-9,
        f"{quad:.12e}",
    )
    K_rem_exact = PTS * (SIG_REM**2 + mu**2 / A)
    v_exact = value(leg.sum_sq, n, K_rem_exact, TAU)
    v_cont = value(leg.sum_sq, n, PTS * SIG_REM**2, TAU)
    print(
        f"  K_rem exact discrete {K_rem_exact:.6f} against continuous {PTS * SIG_REM**2:.6f}"
        " points^2"
    )
    print(
        f"  value at exact K_rem {v_exact:,.4f}; continuous approximation {v_cont:,.4f}; difference"
        f" {v_exact - v_cont:,.4f} (deterministic)"
    )
    return DiscreteExpectation(m_r, float(s_r), v_exact, v_cont)


def check_simulation(
    report: CheckReport,
    rng: np.random.Generator,
    leg: RealisedLeg,
    expectation: DiscreteExpectation,
) -> None:
    """5. The simulated value of the remaining returns, in four blocks of 50,000 paths."""
    print("== 5. simulation of the remaining 126 returns")
    blocks, per = 4, 50_000
    pv = np.empty(blocks * per)
    for b in range(blocks):
        z = rng.standard_normal((per, N - n))
        rr = expectation.m_r + expectation.s_r * z
        rv_rem = PTS * A / (N - n) * np.sum(rr**2, axis=1)
        pv[b * per : (b + 1) * per] = (
            N_VAR * np.exp(-R * TAU) * (PTS * A / N * leg.sum_sq + (N - n) / N * rv_rem - K_VAR)
        )
    m, se = float(pv.mean()), float(pv.std(ddof=1) / np.sqrt(pv.size))
    zsc = (m - expectation.v_exact) / se
    report.ok(
        "simulated value within 4 s.e. of the exact discrete value",
        abs(zsc) <= 4,
        f"{m:,.2f} (s.e. {se:,.2f}) vs {expectation.v_exact:,.2f}, z {zsc:+.2f}",
    )
    print(
        f"  (against the continuous approximation the z-score would be"
        f" {(m - expectation.v_cont) / se:+.2f}; not a check)"
    )


def main() -> int:
    """Print the versions, then run the six parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    leg = RealisedLeg.example()
    v = check_limits(report, leg)
    check_units(report, leg, v)
    check_realised_leg(report, leg)
    expectation = check_discrete_expectation(report, leg)
    check_simulation(report, np.random.default_rng(SEED), leg, expectation)
    print("== 6. reported, not binding")
    cal = N_VAR * np.exp(-R * TAU) * (182 / 365 * 625.0 + 183 / 365 * K_REM_QUOTED - K_VAR)
    print(
        f"  calendar-day weights 182/365 instead of 126/252: {cal:,.2f} (difference {cal - v:,.2f})"
    )
    print("FAILED: " + ", ".join(report.failures) if report.failures else "all checks passed")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
