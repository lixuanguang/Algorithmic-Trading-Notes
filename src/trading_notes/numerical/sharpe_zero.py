"""When the finite-fourth-moment condition of meth:sharpe-ratio-standard-error is needed.

Empirical extensions (2026-10-17), audit repair: what the condition is, and is not, needed for.

Derivation (own, not Lo's). With IID returns, mean mu, variance sigma^2 > 0 and
SR = (mu - Rf)/sigma:
  * SR = 0 (mu = Rf). Then sqrt(T) * SR_hat = sqrt(T) (mu_hat - mu) / sigma_hat. The classical
    CLT gives sqrt(T)(mu_hat - mu)/sigma -> N(0,1) with a finite variance alone; the weak law of
    large numbers gives sigma_hat -> sigma (finite variance suffices); Slutsky's lemma gives
    sqrt(T) SR_hat -> N(0,1). No fourth moment is needed, so a finite fourth moment is not
    necessary for every normal limit of the Sharpe-ratio estimator.
  * SR != 0. The joint delta method on (mu_hat, sigma2_hat) uses
    sqrt(T)(sigma2_hat - sigma^2) -> N(0, nu4 - sigma^4), which needs a finite fourth moment.
    That is the sufficient condition used for the general variance
    V = 1 - g3 SR + (g4 - 1) SR^2 / 4.
  * "Normal moments, and only then". V = 1 + SR^2/2 iff SR = 0 or g4 = 3 + 4 g3 / SR. So normal
    third and fourth moments are sufficient, not necessary: a symmetric non-normal law with
    kurtosis 3 gives the same V.
Checks (Monte Carlo):
  1. centred IID Student-t3 (finite variance, infinite fourth moment), SR = 0:
     Var(sqrt(T) SR_hat) near 1 and tail frequencies near the normal ones at T = 10 000;
  2. the three-point law {-sqrt(3), 0, +sqrt(3)} with probabilities {1/6, 2/3, 1/6} (variance 1,
     skewness 0, kurtosis 3, not normal), shifted to SR = 0.5: T Var(SR_hat) near
     1 + 0.5^2/2 = 1.125.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.sharpe_zero
(numpy; about 1 s). Exits non-zero on failure.
"""

# standard library imports
import math
import sys
from collections.abc import Callable
from typing import Final

# third party library imports
import numpy as np
from numpy.typing import NDArray

# project library imports
from trading_notes.numerical.report import CheckReport

type Sampler = Callable[[tuple[int, int]], NDArray[np.float64]]
"""Draws a (samples, T) array of returns, one sample per row."""

SEED: Final = 31
THREE_POINT_VALUES: Final = (-math.sqrt(3), 0.0, math.sqrt(3))
THREE_POINT_PROBABILITIES: Final = (1 / 6, 2 / 3, 1 / 6)


def root_t_sr(
    draw: Sampler, T: int, reps: int, sr_true: float = 0.0, chunk: int = 250
) -> NDArray[np.float64]:
    """Return sqrt(T) (SR_hat - sr_true) for reps samples of length T.

    Samples are drawn chunk rows at a time, reps // chunk times, so any remainder of reps is not
    drawn. SR_hat uses the population standard deviation (ddof 0).

    Args:
        draw: The return sampler.
        T: Observations per sample.
        reps: Number of samples.
        sr_true: The true Sharpe ratio.
        chunk: Samples per draw.

    Returns:
        One value per drawn sample, in draw order.
    """
    out = []
    for _ in range(reps // chunk):
        x = draw((chunk, T))
        s = x.mean(axis=1) / x.std(axis=1, ddof=0)
        out.append(math.sqrt(T) * (s - sr_true))
    return np.concatenate(out)


def student_t3(rng: np.random.Generator) -> Sampler:
    """Return a sampler of centred Student-t returns with 3 degrees of freedom."""

    def draw(size: tuple[int, int]) -> NDArray[np.float64]:
        return rng.standard_t(3, size)

    return draw


def shifted_three_point(rng: np.random.Generator, shift: float) -> Sampler:
    """Return a sampler of the three-point law plus shift; with variance 1, SR is the shift."""
    vals = np.array(THREE_POINT_VALUES)
    probs = np.array(THREE_POINT_PROBABILITIES)

    def draw(size: tuple[int, int]) -> NDArray[np.float64]:
        sample: NDArray[np.float64] = vals[rng.choice(3, size=size, p=probs)] + shift
        return sample

    return draw


def check_student_t(report: CheckReport, rng: np.random.Generator) -> None:
    """1. Centred Student-t3, SR = 0: the normal limit holds without a fourth moment."""
    print("== 1. centred Student-t3, SR = 0")
    T, reps = 10000, 4000
    z = root_t_sr(student_t3(rng), T, reps)
    v = z.var()
    tail = np.mean(np.abs(z) > 1.96)
    report.ok("Var(sqrt(T) SR_hat) within 0.08 of 1", abs(v - 1) < 0.08, f"{v:.3f}")
    report.ok(
        "P(|sqrt(T) SR_hat| > 1.96) within 0.012 of 0.05",
        bool(abs(tail - 0.05) < 0.012),
        f"{tail:.4f}",
    )


def check_three_point(report: CheckReport, rng: np.random.Generator) -> None:
    """2. Skewness 0 and kurtosis 3 without normality still give V = 1 + SR^2/2."""
    print("== 2. a non-normal law with skewness 0 and kurtosis 3 gives 1 + SR^2/2")
    vals = np.array(THREE_POINT_VALUES)
    probs = np.array(THREE_POINT_PROBABILITIES)
    m2 = float((probs * vals**2).sum())
    m4 = float((probs * vals**4).sum())
    report.ok(
        "kurtosis of the three-point law is 3", abs(m4 / m2**2 - 3) < 1e-12, f"{m4 / m2**2:.3f}"
    )
    sr = 0.5
    T2, reps2 = 2000, 8000
    y = root_t_sr(shifted_three_point(rng, sr), T2, reps2, sr_true=sr)
    v2 = y.var()
    report.ok("T Var(SR_hat) within 0.06 of 1.125", abs(v2 - 1.125) < 0.06, f"{v2:.3f}")


def main() -> int:
    """Run both checks on one generator, the second continuing the first's stream.

    Returns:
        The exit status, 0 or 1.
    """
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    check_student_t(report, rng)
    check_three_point(report, rng)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
