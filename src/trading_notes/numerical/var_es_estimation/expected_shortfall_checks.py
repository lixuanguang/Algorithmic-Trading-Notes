"""Expected shortfall on a two-atom loss, in historical simulation and for a normal law."""

import math
import random
import sys
from typing import Final

from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.var_es_estimation.expected_shortfall import (
    DiscreteLoss,
    historical_expected_shortfall,
)

# Loss 100 with probability 0.005, otherwise 0.
TWO_ATOMS: Final = DiscreteLoss(atoms=((0.0, 0.995), (100.0, 0.005)))
SEED: Final = 7
DRAWS: Final = 400000


def near(report: CheckReport, name: str, got: float, want: float, tol: float = 1e-9) -> None:
    """Check |got - want| <= tol and print both values to six significant digits."""
    report.ok(name, abs(got - want) <= tol, f"{got:.6g} (want {want:.6g})")


def quantile_integral(loss: DiscreteLoss, c: float, n: int = 200000) -> float:
    """Return ES_c as the quantile integral over (c, 1), by the midpoint rule with n points.

    Independent of the fractional-tail-mass form of `DiscreteLoss.expected_shortfall`.
    """
    a = 1 - c
    h = a / n
    return sum(loss.var(c + (i + 0.5) * h) for i in range(n)) * h / a


def normal_draws(n: int = DRAWS) -> list[float]:
    """Return n standard normal draws from random.Random(SEED); the shared generator is not used."""
    rng = random.Random(SEED)
    return [rng.gauss(0, 1) for _ in range(n)]


def check_two_atoms(report: CheckReport) -> None:
    """Check VaR, ES by both forms and the two conditional means of the two-atom loss."""
    print(
        "== a two-atom loss: 100 with probability 0.005, otherwise 0; confidence 99%, exceedance 1%"
    )
    loss = TWO_ATOMS
    near(report, "VaR_99%", loss.var(0.99), 0.0)
    near(report, "ES_99% (fractional tail mass)", loss.expected_shortfall(0.99), 50.0)
    near(
        report,
        "ES_99% (quantile integral, midpoint rule)",
        quantile_integral(loss, 0.99),
        50.0,
        1e-6,
    )
    near(
        report,
        "E[L | L > VaR] (strict tail conditional expectation)",
        loss.tail_conditional_expectation(0.99, strict=True),
        100.0,
    )
    near(
        report,
        "E[L | L >= VaR] (weak tail conditional expectation)",
        loss.tail_conditional_expectation(0.99, strict=False),
        0.5,
    )
    near(report, "confidence 99.5%: VaR (P(L<=0) = 0.995 already)", loss.var(0.995), 0.0)
    near(report, "confidence 99.6%: VaR", loss.var(0.996), 100.0)
    near(report, "confidence 99.6%: ES", loss.expected_shortfall(0.996), 100.0)


def check_historical_simulation(report: CheckReport) -> None:
    """Check historical simulation with an integer and a fractional number of tail observations."""
    print("== historical simulation")
    hs = [100.0] * 5 + [0.0] * 995  # the same law as an empirical sample of 1000
    es_hs = historical_expected_shortfall
    near(report, "HS, 1000 obs, 10 tail obs: ES_99%", es_hs(hs, 0.99), 50.0)
    near(
        report,
        "HS, 1000 obs: worst-10 mean equals the fractional formula",
        es_hs(hs, 0.99),
        DiscreteLoss(atoms=[(0.0, 0.995), (100.0, 0.005)]).expected_shortfall(0.99),
    )
    hs250 = [40.0, 30.0, 20.0, 10.0] + [0.0] * 246  # 2.5 tail observations at 99%
    near(report, "HS, 250 obs, 2.5 tail obs: (40 + 30 + 0.5*20)/2.5", es_hs(hs250, 0.99), 32.0)
    empirical = DiscreteLoss(
        atoms=[(40.0, 1 / 250), (30.0, 1 / 250), (20.0, 1 / 250), (10.0, 1 / 250), (0.0, 246 / 250)]
    )
    near(
        report,
        "HS, 250 obs: same as the fractional formula on the empirical law",
        es_hs(hs250, 0.99),
        empirical.expected_shortfall(0.99),
        1e-9,
    )
    naive = sum(sorted(hs250, reverse=True)[:2]) / 2
    print(
        f"     (dropping the fraction: worst-2 mean {naive:.1f}; "
        f"rounding up: worst-3 mean {sum([40, 30, 20]) / 3:.1f})"
    )


def check_continuous_law(report: CheckReport) -> None:
    """Check a standard normal law, where ES and both conditional means coincide."""
    print("== a continuous law: all three agree")
    z99 = 2.3263478740408408
    phi = math.exp(-(z99**2) / 2) / math.sqrt(2 * math.pi)
    near(report, "standard normal ES_99% = phi(z)/0.01", phi / 0.01, 2.665214220345808, 1e-9)
    draws = normal_draws()
    near(
        report,
        "HS ES_99% on 400000 normal draws within 0.02",
        historical_expected_shortfall(draws, 0.99),
        2.6652,
        0.02,
    )


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    check_two_atoms(report)
    check_historical_simulation(report)
    check_continuous_law(report)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
