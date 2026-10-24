"""Trading costs and trade execution: worked numbers of five execution entries.

Trading costs and trade execution (2026-10-19): the worked numbers of meth:execution-cost-measures,
def:electronic-trading-environment, meth:trade-strategy-selection,
def:trade-implementation-by-market and meth:trade-execution-evaluation-governance.

Reproduced from Managing Investment Portfolios (2007), chap. 10 (Madhavan, Treynor and Wagner):
the effective spread of $0.02 against a $0.06 quoted spread; the three Alpha Company sells
(effective spreads C$0.06, 0.11, 0.22; averages 0.13 and 0.155); the VWAP cost of EUR 625 plus
25 explicit; and the Impulse Robotics implementation shortfall of 87 bp (commissions 14,
realised 14, delay 35, missed trade 24) with a market-adjusted -13 bp. Original: a stale-quote
loss and the spread it takes to cover it; Almgren-Chriss schedules at three risk aversions
(illustrative parameters); costs of a 50-million trade in five markets under stated assumptions
(illustrative, not quotes); a z-score against a pre-trade estimate; and a broker comparison with
a significance test.

Count convention: one check is one executed ok() call (a call inside a loop counts once per
iteration).

Run: uv run --frozen --no-editable python -m trading_notes.numerical.trade_execution
(numpy, scipy). Exits 1 on failure.
"""

import math
import sys

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.stats import norm

from trading_notes.numerical.report import CheckReport


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


def check_costs(report: CheckReport) -> None:
    """Part 1: effective spread, VWAP cost and implementation shortfall."""
    print(
        "== part 1: explicit and implicit costs: effective spread, VWAP and implementation"
        " shortfall (MIP chap. 10)"
    )
    mid = (20.03 + 19.97) / 2
    report.ok(
        "buy 500 at 20.01 against a 19.97 / 20.03 quote: quoted spread 0.06, effective spread"
        " 2 x (20.01 - 20.00) = 0.02",
        close(20.03 - 19.97, 0.06, 1e-12) and close(2 * (20.01 - mid), 0.02, 1e-9),
    )
    quotes = [(10.12, 10.24, 10.15, 200), (10.11, 10.22, 10.11, 300), (10.05, 10.19, 10.01, 500)]
    eff = [2 * ((b + a) / 2 - p) for b, a, p, _ in quotes]  # sells
    qs = [a - b for b, a, _, _ in quotes]
    report.ok(
        "Alpha Company sells: quoted spreads 0.12, 0.11, 0.14 (average 0.1233); effective 0.06,"
        " 0.11, 0.22",
        bool(
            np.allclose(qs, [0.12, 0.11, 0.14])
            and abs(np.mean(qs) - 0.1233) < 5e-5
            and np.allclose(eff, [0.06, 0.11, 0.22])
        ),
    )
    w_eff = sum(e * n for e, (*_, n) in zip(eff, quotes, strict=True)) / 1000
    report.ok(
        "average effective spread 0.13; share-weighted 0.155: the 500-share order walked the book",
        bool(abs(np.mean(eff) - 0.13) < 5e-12 and abs(w_eff - 0.155) < 5e-12),
    )
    report.ok(
        "VWAP: a 500-share buy at EUR 157.25 against a VWAP of 156.00 costs 625 implicit + 25"
        " explicit = 650",
        close(500 * (157.25 - 156.00), 625, 1e-9) and close(625 + 25, 650, 1e-9),
    )
    paper = 1000 * (10.08 - 10.00)
    real = 700 * 10.08 - (700 * 10.07 + 14)
    IS = paper - real
    comp = {
        "commissions": 14 / 10_000,
        "realised": 700 * (10.07 - 10.05) / 10_000,
        "delay": 700 * (10.05 - 10.00) / 10_000,
        "missed": 300 * (10.08 - 10.00) / 10_000,
    }
    report.ok(
        "Impulse Robotics: paper gain 80, real gain -7, shortfall 87 = 87 bp of the 10,000 paper"
        " trade",
        close(paper, 80, 1e-9) and close(real, -7, 1e-9) and close(IS / 10_000, 0.0087, 1e-12),
    )
    report.ok(
        "components 14 + 14 + 35 + 24 bp sum to 87 bp; market-adjusted for a 1% market rise"
        " (beta 1): -13 bp",
        np.allclose(list(comp.values()), [0.0014, 0.0014, 0.0035, 0.0024])
        and close(sum(comp.values()), 0.0087, 1e-12)
        and close(0.0087 - 1.0 * 0.01, -0.0013, 1e-12),
    )
    report.ok(
        "against a pre-trade estimate of 40 bp with 30 bp standard error the 87 bp outcome is a"
        " z-score of 1.57: worth"
        " review, not proof of poor execution",
        abs((87 - 40) / 30 - 1.567) < 1e-3,
    )


def check_stale_quotes(report: CheckReport) -> None:
    """Part 2: a stale-quote loss and the half-spread that covers adverse selection."""
    print("== part 2: electronic markets: speed, stale quotes and the spread that covers them")
    loss_per_snipe = 500 * 0.02
    report.ok(
        "a dealer's stale 500-share bid at 50.00, picked off when the fair value moves to 49.98,"
        " loses 10.00",
        close(loss_per_snipe, 10.0, 1e-9),
    )
    p_snipe, half_spread = 0.10, 0.005
    report.ok(
        "if 10% of fills are picked off by 0.02 moves, the expected adverse-selection cost is 0.002"
        " a share; a 0.005"
        " half-spread leaves 0.003 net, and the dealer breaks even at a 0.002 half-spread",
        close(p_snipe * 0.02, 0.002, 1e-12) and close(half_spread - p_snipe * 0.02, 0.003, 1e-12),
    )


def ac(
    X: float,
    T: float,
    n: int,
    sigma: float,
    eta: float,
    eps: float,
    gamma: float,
    lam: float,
) -> tuple[float, float, NDArray[np.float64]]:
    """Discrete Almgren-Chriss: the optimal schedule's expected cost and variance.

    Returns:
        (E, V, holdings), the holdings at each of the n + 1 times.
    """
    tau = T / n
    eta_t = eta * (1 - gamma * tau / (2 * eta))
    kt = math.sqrt(lam * sigma**2 / eta_t) if lam > 0 else 0.0
    kappa = math.acosh(1 + 0.5 * kt**2 * tau**2) / tau if lam > 0 else 0.0
    t = np.arange(n + 1) * tau
    if lam > 0:
        x = X * np.sinh(kappa * (T - t)) / np.sinh(kappa * T)
    else:
        x = X * (1 - t / T)
    trades = -np.diff(x)
    E = 0.5 * gamma * X**2 + eps * X + (eta_t / tau) * np.sum(trades**2)
    V = sigma**2 * tau * np.sum(x[1:] ** 2)
    return E, V, x


def check_schedules(report: CheckReport) -> None:
    """Part 3: Almgren-Chriss schedules at three risk aversions."""
    print(
        "== part 3: choosing a trading strategy: urgency, benchmark and algorithm (Almgren-Chriss"
        " schedules)"
    )
    X, sigma, eta, eps, gamma = 1e6, 0.95, 2.5e-6, 0.0625, 2.5e-7
    res = {lam: ac(X, 5.0, 25, sigma, eta, eps, gamma, lam) for lam in (0.0, 1e-6, 1e-5)}
    E0, V0, _ = res[0.0]
    E1, V1, x1 = res[1e-6]
    E2, V2, x2 = res[1e-5]
    report.ok(
        "more risk aversion front-loads the schedule: expected cost rises and risk falls"
        " (efficient frontier)",
        bool(E0 < E1 < E2 and V0 > V1 > V2 and x2[5] < x1[5] < X * (1 - 5 / 25)),
        f"E {E0:,.0f} {E1:,.0f} {E2:,.0f}; sd "
        f"{math.sqrt(V0):,.0f} {math.sqrt(V1):,.0f} {math.sqrt(V2):,.0f}",
    )
    report.ok(
        "the linear (TWAP-like) schedule minimises expected cost when lambda = 0", E0 <= min(E1, E2)
    )


def check_markets(report: CheckReport) -> None:
    """Part 4: illustrative one-way costs of 50 million in five markets."""
    print("== part 4: implementation across markets (assumptions for 50 million, not quotes)")
    notional = 50e6
    costs = {
        "large-cap equity (half-spread 1.5 bp + impact 4 bp)": notional * (0.00015 + 0.0004),
        "IG corporate bond via RFQ (half-spread 10 bp)": notional * 0.0010,
        "10-year Treasury futures (half-tick on 476 contracts)": 476 * 15.625 / 2,
        "10-year SOFR swap via SEF (0.25 bp on DV01 of 44,000 per bp)": 0.25 * 44_000,
        "EUR/USD spot (0.3 pip half-spread)": notional * 0.00003 / 2 * 1,
    }
    report.ok(
        "illustrative one-way costs for 50m: equity 27,500; IG bond 50,000; Treasury futures 3,719;"
        " SOFR swap 11,000;"
        " EUR/USD spot 750",
        np.allclose(list(costs.values()), [27_500, 50_000, 3_718.75, 11_000, 750]),
        " ".join(f"{v:,.0f}" for v in costs.values()),
    )


def check_evaluation(report: CheckReport) -> None:
    """Part 5: a broker comparison with a significance test and the sample it needs."""
    print("== part 5: evaluating execution and trading procedures")
    m_a, m_b, s, n_a, n_b = 25.0, 32.0, 40.0, 120, 100
    t_stat = (m_b - m_a) / (s * math.sqrt(1 / n_a + 1 / n_b))
    report.ok(
        "broker B's average shortfall is 7 bp worse than A's (32 vs 25, sd 40, 100 and 120"
        " orders): t = 1.29, p = 0.20 -"
        " not significant; more orders or matched comparisons are needed before re-routing",
        bool(abs(t_stat - 1.292) < 1e-3 and abs(2 * (1 - norm.cdf(t_stat)) - 0.196) < 2e-3),
        f"t {t_stat:.3f}",
    )
    need = (1.96 * s * math.sqrt(2) / 7) ** 2
    report.ok(
        "to detect a 7 bp difference at the 5% level with this dispersion needs about 250 orders"
        " per broker",
        abs(need - 251) < 1,
        f"{need:.0f}",
    )


def main() -> int:
    """Print the versions, then run the five parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_costs(report)
    check_stale_quotes(report)
    check_schedules(report)
    check_markets(report)
    check_evaluation(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
