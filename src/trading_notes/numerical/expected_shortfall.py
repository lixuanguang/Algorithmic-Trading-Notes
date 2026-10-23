"""Expected shortfall for discrete and historical-simulation distributions.

Empirical extensions (2026-10-17), audit repair, behind meth:var-es-estimation-methods.

Definition used (Acerbi and Tasche, "On the coherence of Expected Shortfall",
arXiv:cond-mat/0104295v3, Definition 2.6 p. 5, Proposition 3.2 p. 6 and eq. (3.3) p. 7, written
there for a profit X and a tail level alpha in (0,1)), restated here for a loss L = -X,
confidence level c and exceedance (tail) probability alpha = 1 - c:
    VaR_c(L) = inf{l : P(L <= l) >= c}                         (lower quantile of the loss)
    ES_c(L)  = (1/alpha) * integral_c^1 VaR_u(L) du
             = (1/alpha) * ( E[L 1{L > VaR_c}] + VaR_c * (P(L <= VaR_c) - c) )
                                                                (fractional tail mass)
The second line is the loss-side form of Definition 2.6's tail mean; it puts weight on the atom
at VaR so that the tail always carries probability exactly alpha. E[L | L > VaR] and
E[L | L >= VaR] (the two tail conditional expectations) differ from ES when L has an atom at
VaR.
Checked: the audit's example; equality of the integral and fractional-mass forms; historical
simulation with an integer and a fractional number of tail observations; and agreement with a
continuous distribution, where all three coincide.
Run: uv run --frozen --no-editable python -m trading_notes.numerical.expected_shortfall
(standard library). Exits non-zero on failure.
"""

# standard library imports
import math
import random
import sys
from collections.abc import Sequence
from typing import Final

# project library imports
from trading_notes.numerical.report import CheckReport

type Atoms = Sequence[tuple[float, float]]
"""A discrete loss distribution as (loss, probability) pairs."""

# The audit example: loss 100 with probability 0.005, otherwise 0.
AUDIT_ATOMS: Final = ((0.0, 0.995), (100.0, 0.005))
SEED: Final = 7
DRAWS: Final = 400000


def close(report: CheckReport, name: str, got: float, want: float, tol: float = 1e-9) -> None:
    """Check |got - want| <= tol and print both values to six significant digits."""
    report.ok(name, abs(got - want) <= tol, f"{got:.6g} (want {want:.6g})")


def var_discrete(atoms: Atoms, c: float) -> float:
    """Return the lower c-quantile of the loss.

    The cumulative probability is compared with c less 1e-15, so that rounding in the running
    sum cannot skip the atom at which it reaches c.
    """
    cum = 0.0
    for x, p in sorted(atoms):
        cum += p
        if cum >= c - 1e-15:
            return x
    return max(x for x, _ in atoms)


def es_fractional(atoms: Atoms, c: float) -> float:
    """Return ES_c by the fractional-tail-mass form."""
    a = 1 - c
    v = var_discrete(atoms, c)
    above = sum(x * p for x, p in atoms if x > v)
    at_or_below = sum(p for x, p in atoms if x <= v)
    return (above + v * (at_or_below - c)) / a


def es_integral(atoms: Atoms, c: float, n: int = 200000) -> float:
    """Return ES_c as the quantile integral over (c, 1), by the midpoint rule with n points."""
    a = 1 - c
    h = a / n
    return sum(var_discrete(atoms, c + (i + 0.5) * h) for i in range(n)) * h / a


def tce(atoms: Atoms, c: float, strict: bool = True) -> float:
    """Return the tail conditional expectation E[L | L > VaR_c], or E[L | L >= VaR_c]."""
    v = var_discrete(atoms, c)
    sel = [(x, p) for x, p in atoms if (x > v if strict else x >= v)]
    return sum(x * p for x, p in sel) / sum(p for _, p in sel)


def es_hs(sample: Sequence[float], c: float) -> float:
    """Return the historical-simulation ES_c.

    The average of the worst n*alpha losses, the last one fractionally weighted. A whole or
    fractional part within 1e-12 of an integer is treated as that integer, so that n*alpha
    computed in floating point keeps its intended count: 1000 * 0.01 == 10.0, but alpha is
    computed as 1 - c, and 1000 * (1 - 0.99) == 10.000000000000009.
    """
    xs = sorted(sample, reverse=True)
    k = len(xs) * (1 - c)
    whole = math.floor(k + 1e-12)
    frac = k - whole
    tail = sum(xs[:whole]) + (frac * xs[whole] if frac > 1e-12 else 0.0)
    return tail / k


def normal_draws(n: int = DRAWS) -> list[float]:
    """Return n standard normal draws from a generator of this run, seeded with SEED.

    The draws are random.Random(SEED).gauss(0, 1) in order, the sequence the module-level
    generator gives after random.seed(SEED); the shared generator is not used.
    """
    rng = random.Random(SEED)
    return [rng.gauss(0, 1) for _ in range(n)]


def check_audit_example(report: CheckReport) -> None:
    """The audit's two-atom example: VaR, ES by both forms and the two conditional means."""
    print(
        "== the audit example: loss 100 with probability 0.005, otherwise 0; "
        "confidence 99%, exceedance 1%"
    )
    atoms = AUDIT_ATOMS
    close(report, "VaR_99%", var_discrete(atoms, 0.99), 0.0)
    close(report, "ES_99% (fractional tail mass)", es_fractional(atoms, 0.99), 50.0)
    close(
        report,
        "ES_99% (quantile integral, midpoint rule)",
        es_integral(atoms, 0.99),
        50.0,
        1e-6,
    )
    close(
        report,
        "E[L | L > VaR] (strict tail conditional expectation)",
        tce(atoms, 0.99, strict=True),
        100.0,
    )
    close(
        report,
        "E[L | L >= VaR] (weak tail conditional expectation)",
        tce(atoms, 0.99, strict=False),
        0.5,
    )
    close(
        report,
        "confidence 99.5%: VaR (P(L<=0) = 0.995 already)",
        var_discrete(atoms, 0.995),
        0.0,
    )
    close(report, "confidence 99.6%: VaR", var_discrete(atoms, 0.996), 100.0)
    close(report, "confidence 99.6%: ES", es_fractional(atoms, 0.996), 100.0)


def check_historical_simulation(report: CheckReport) -> None:
    """Historical simulation with an integer and a fractional number of tail observations."""
    print("== historical simulation")
    hs = [100.0] * 5 + [0.0] * 995  # the same law as an empirical sample of 1000
    close(report, "HS, 1000 obs, 10 tail obs: ES_99%", es_hs(hs, 0.99), 50.0)
    close(
        report,
        "HS, 1000 obs: worst-10 mean equals the fractional formula",
        es_hs(hs, 0.99),
        es_fractional([(0.0, 0.995), (100.0, 0.005)], 0.99),
    )
    hs250 = [40.0, 30.0, 20.0, 10.0] + [0.0] * 246  # 2.5 tail observations at 99%
    close(report, "HS, 250 obs, 2.5 tail obs: (40 + 30 + 0.5*20)/2.5", es_hs(hs250, 0.99), 32.0)
    close(
        report,
        "HS, 250 obs: same as the fractional formula on the empirical law",
        es_hs(hs250, 0.99),
        es_fractional(
            [(40.0, 1 / 250), (30.0, 1 / 250), (20.0, 1 / 250), (10.0, 1 / 250), (0.0, 246 / 250)],
            0.99,
        ),
        1e-9,
    )
    naive = sum(sorted(hs250, reverse=True)[:2]) / 2
    print(
        f"     (dropping the fraction: worst-2 mean {naive:.1f}; "
        f"rounding up: worst-3 mean {sum([40, 30, 20]) / 3:.1f})"
    )


def check_continuous_law(report: CheckReport) -> None:
    """A standard normal law, where ES and both conditional means coincide."""
    print("== a continuous law: all three agree")
    z99 = 2.3263478740408408
    phi = math.exp(-(z99**2) / 2) / math.sqrt(2 * math.pi)
    close(report, "standard normal ES_99% = phi(z)/0.01", phi / 0.01, 2.665214220345808, 1e-9)
    draws = normal_draws()
    close(report, "HS ES_99% on 400000 normal draws within 0.02", es_hs(draws, 0.99), 2.6652, 0.02)


def main() -> int:
    """Run the checks with a fresh report and return the exit status (0 or 1)."""
    report = CheckReport()
    check_audit_example(report)
    check_historical_simulation(report)
    check_continuous_law(report)
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
