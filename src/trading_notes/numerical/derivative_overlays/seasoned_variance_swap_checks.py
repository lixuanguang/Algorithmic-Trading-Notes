"""Seasoned variance-swap value: limits, units, realised leg, expectation and simulation."""

import sys
from typing import Final

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, stats

from trading_notes.numerical.derivative_overlays.variance_swap import SeasonedVarianceSwap
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.records import Record

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
SWAP: Final = SeasonedVarianceSwap(
    n_returns=N, annualisation=A, variance_notional=N_VAR, variance_strike=K_VAR, scale=PTS, rate=R
)


def rel(a: float, b: float) -> float:
    """Return |a - b| / |b|."""
    return abs(a - b) / abs(b)


class RealisedLeg(Record):
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
        return cls(ret=ret, sum_sq=sum_sq, rv=PTS * A / n * sum_sq)


def check_limits(report: CheckReport, leg: RealisedLeg) -> float:
    """Check The worked value, and the limits at inception and expiry; return the worked value."""
    print("== 1. limits and the worked value")
    v = SWAP.value(leg.sum_sq, n, K_REM_QUOTED, TAU)
    print(
        f"  N_var = {N_VAR:,.1f} per point squared; realised RV over {n} returns ="
        f" {leg.rv:.6f} points^2"
    )
    report.ok(
        "worked value 2,500 e^{-0.02} (312.5 + 162 - 400) = 182,562.00",
        abs(v - 182_562.00) < 0.01,
        f"{v:,.4f}",
    )
    v0 = SWAP.value(0.0, 0, K_VAR, N / A)
    report.ok(
        "inception (n = 0, empty realised sum, K_rem = K_var) is zero", abs(v0) <= 1e-6, f"{v0:.2e}"
    )
    # the series twice: 252 returns with realised RV 625
    full = np.sum(np.concatenate([leg.ret, leg.ret]) ** 2)
    # the remaining term has weight zero, so its strike is irrelevant
    v_T = SWAP.value(full, N, 0.0, 0.0)
    report.ok(
        "expiry (n = N, P = 1) equals the payoff N_var (RV - K_var)",
        abs(v_T - N_VAR * (625 - K_VAR)) <= 1e-6,
        f"{v_T:,.4f}",
    )
    return v


def check_units(report: CheckReport, leg: RealisedLeg, v: float) -> None:
    """Check Decimal variance units, and the vega notional as the payoff's slope at K_vol."""
    print("== 2. units and notionals")
    decimal = SWAP.model_copy(
        update={"variance_notional": N_VAR * PTS, "variance_strike": K_VAR / PTS, "scale": 1.0}
    )
    v_dec = decimal.value(leg.sum_sq, n, K_REM_QUOTED / PTS, TAU)
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
    """Check The observation weights from the data, and the contract alternatives reported."""
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


class DiscreteExpectation(Record):
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
    """Check E[r^2] by quadrature, and the exact discrete K_rem against the continuous one."""
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
    v_exact = SWAP.value(leg.sum_sq, n, K_rem_exact, TAU)
    v_cont = SWAP.value(leg.sum_sq, n, PTS * SIG_REM**2, TAU)
    print(
        f"  K_rem exact discrete {K_rem_exact:.6f} against continuous {PTS * SIG_REM**2:.6f}"
        " points^2"
    )
    print(
        f"  value at exact K_rem {v_exact:,.4f}; continuous approximation {v_cont:,.4f}; difference"
        f" {v_exact - v_cont:,.4f} (deterministic)"
    )
    return DiscreteExpectation(m_r=m_r, s_r=float(s_r), v_exact=v_exact, v_cont=v_cont)


def check_simulation(
    report: CheckReport,
    rng: np.random.Generator,
    leg: RealisedLeg,
    expectation: DiscreteExpectation,
) -> None:
    """Check The simulated value of the remaining returns, in four blocks of 50,000 paths."""
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

    Contract: N = 252 daily log returns, zero mean, A = 252, K_vol = 20 vol points, vega notional
    100,000 (N_var = 2,500 per point squared). Example: n = 126 returns at realised volatility 25,
    quoted K_rem = 324, r = 4 percent, q = 1 percent, T - t = 0.5; under risk-neutral GBM with sigma
    = 18 percent the exact discrete K_rem is 10^4 [sigma^2 + (r - q - sigma^2/2)^2 / A], against the
    continuous 324 of option-strip replication. The value formula is a labelled derivation from
    Demeterfi et al.'s definitions and additivity. Simulation: default_rng(20261021), 200,000 paths
    in four blocks; the value must lie within 4 standard errors of the exact discrete value.
    Synthetic inputs only.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
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
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
