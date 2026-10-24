"""Historical scenarios, historical against Monte Carlo simulation, and sensitivity analysis."""

import sys
from collections.abc import Sequence
from typing import Final

import numpy as np
from numpy.typing import NDArray

from trading_notes.numerical.portfolio_choice.history import DATA, AssetClassHistory
from trading_notes.numerical.records import Record
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.repository import repository_root
from trading_notes.numerical.scenario_simulation.return_simulation import (
    NormalReturns,
    compounded_wealth,
)
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]

WEIGHTS: Final = np.array([0.6, 0.4])  # S&P 500 with dividends, 10-year Treasuries
PATHS: Final = 20_000
HORIZON: Final = 10  # years


class Portfolio(Record):
    """The annually rebalanced 60/40 portfolio over the annual history.

    Attributes:
        history: The annual asset-class returns.
    """

    history: AssetClassHistory

    @property
    def assets(self) -> Floats:
        """Return the S&P 500 and 10-year Treasury returns, years x 2."""
        return np.column_stack([self.history.series["sp500"], self.history.series["tbond_10y"]])

    @property
    def returns(self) -> Floats:
        """Return the portfolio's annual returns."""
        returns: Floats = self.assets @ WEIGHTS
        return returns

    @property
    def years(self) -> NDArray[np.int_]:
        """Return the calendar years."""
        return self.history.years

    def in_year(self, year: int) -> float:
        """Return the portfolio's return in one calendar year."""
        return float(self.returns[self.years == year][0])

    def series_in_year(self, name: str, year: int) -> float:
        """Return one column of the history in one calendar year."""
        return float(self.history.series[name][self.years == year][0])


def check_historical_scenarios(report: CheckReport, p: Portfolio) -> None:
    """Part 1: replayed years, a two-year scenario and a three-scenario view."""
    print("== part 1: historical scenarios")
    scen = {y: p.in_year(y) for y in (1931, 1974, 2008, 2022)}
    sp08, tb08 = p.series_in_year("sp500", 2008), p.series_in_year("tbond_10y", 2008)
    report.ok(
        "replayed years: 1931 -27.3%, 1974 -14.7%, 2008 -13.9%, 2022 -18.0%; 2008 equals 0.6 x"
        " -36.6% + 0.4 x 20.1%",
        [round(v, 3) for v in scen.values()] == [-0.273, -0.147, -0.139, -0.180]
        and close(scen[2008], 0.6 * sp08 + 0.4 * tb08, 1e-12)
        and round(sp08, 3) == -0.366
        and round(tb08, 3) == 0.201,
    )
    report.ok(
        "in 2008 Treasuries offset a third of the equity loss; in 2022 both fell (stocks -18.0%,"
        " bonds -17.8%)",
        round(p.series_in_year("sp500", 2022), 3) == -0.180
        and round(p.series_in_year("tbond_10y", 2022), 3) == -0.178,
    )
    in_7374 = (p.years >= 1973) & (p.years <= 1974)
    w7374 = np.prod(1 + p.returns[in_7374]) - 1
    infl7374 = np.prod(1 + p.history.series["cpi_inflation"][in_7374]) - 1
    report.ok(
        "1973-74 as a two-year scenario: -20.8% nominal, -35.2% after 22.1% cumulative inflation",
        round(w7374, 3) == -0.208
        and round(infl7374, 3) == 0.221
        and round((1 + w7374) / (1 + infl7374) - 1, 3) == -0.352,
    )
    probs = {"recession": 0.20, "base": 0.60, "boom": 0.20}
    rets = {"recession": -0.12, "base": 0.06, "boom": 0.18}
    report.ok(
        "a three-scenario view (20% recession at -12%, 60% base at +6%, 20% boom at +18%) has an"
        " expected return of 4.8% and a 20% chance of a double-digit loss",
        round(sum(probs[k] * rets[k] for k in probs), 3) == 0.048,
    )


def check_simulations(report: CheckReport, p: Portfolio, model: NormalReturns, z: Floats) -> Floats:
    """Part 2: a whole-year bootstrap against a fitted normal, over ten years.

    Returns:
        The Monte Carlo ten-year wealth, which part 3 perturbs.
    """
    print("== part 2: historical simulation against Monte Carlo for a ten-year horizon")
    port = p.returns
    idx = np.random.default_rng(20261020).integers(0, len(port), size=(PATHS, HORIZON))
    tw_hist = compounded_wealth(port[idx])
    report.ok(
        "bootstrap of whole years (which keeps each year's stock-bond pairing): mean one-year"
        " return equals the sample mean 9.0% within simulation error",
        bool(abs(port[idx].mean() - port.mean()) < 0.001 and round(port.mean(), 3) == 0.090),
    )
    mu, S = model.mean, model.covariance
    sim = model.simulate(z)
    tw_mc = compounded_wealth(sim @ WEIGHTS)
    report.ok(
        "Monte Carlo with a normal fitted to the same means and covariance: one-year mean 9.0%"
        " and volatility 12.1% match w'mu and sqrt(w' Sigma w)",
        bool(
            abs((sim @ WEIGHTS).mean() - WEIGHTS @ mu) < 0.001
            and abs((sim @ WEIGHTS).std() - np.sqrt(WEIGHTS @ S @ WEIGHTS)) < 0.001
            and round(np.sqrt(WEIGHTS @ S @ WEIGHTS), 3) == 0.121
        ),
    )
    p_hist = np.percentile(tw_hist, [5, 50, 95])
    p_mc = np.percentile(tw_mc, [5, 50, 95])
    report.ok(
        "ten-year wealth per 1 invested: historical 5th/50th/95th percentiles 1.21 / 2.26 / 3.92;"
        " Monte Carlo 1.22 / 2.23 / 3.97",
        [round(v, 2) for v in p_hist] == [1.21, 2.26, 3.92]
        and [round(v, 2) for v in p_mc] == [1.22, 2.23, 3.97],
        f"hist {np.round(p_hist, 3)}, mc {np.round(p_mc, 3)}",
    )
    one_hist = np.percentile(port, 5)
    one_mc = np.percentile(sim[:, 0, :] @ WEIGHTS, 5)
    report.ok(
        "one-year 5th percentile: -13.4% in the data against -10.8% under the normal: the fitted"
        " normal thins the left tail",
        bool(round(one_hist, 3) == -0.134 and round(one_mc, 3) == -0.108),
    )
    report.ok(
        "chance of losing money over ten years: 1.8% historical against 1.4% Monte Carlo",
        bool(round((tw_hist < 1).mean(), 3) == 0.018 and round((tw_mc < 1).mean(), 3) == 0.014),
    )
    return tw_mc


def check_sensitivities(
    report: CheckReport, model: NormalReturns, z: Floats, tw_mc: Floats
) -> None:
    """Part 3: changes in the ten-year distribution with common random numbers."""
    print("== part 3: sensitivity analysis with common random numbers")
    mu, S = model.mean, model.covariance

    def wealth(changed: NormalReturns, weights: Sequence[float] | Floats = WEIGHTS) -> Floats:
        return compounded_wealth(changed.simulate(z) @ np.asarray(weights))

    base5, base50 = np.percentile(tw_mc, 5), np.median(tw_mc)
    lowmu = wealth(NormalReturns(mean=mu - np.array([0.02, 0.0]), covariance=S))
    corr = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])
    S_hi = S.copy()
    S_hi[0, 1] = S_hi[1, 0] = 0.5 * np.sqrt(S[0, 0] * S[1, 1])
    hicorr = wealth(NormalReturns(mean=mu, covariance=S_hi))
    w80 = wealth(model, [0.8, 0.2])
    sens = {
        "equity mean -2 points": (np.percentile(lowmu, 5) - base5, np.median(lowmu) - base50),
        "stock-bond correlation 0.5": (
            np.percentile(hicorr, 5) - base5,
            np.median(hicorr) - base50,
        ),
        "80/20 instead of 60/40": (np.percentile(w80, 5) - base5, np.median(w80) - base50),
    }
    for k_, v in sens.items():
        print(f"  {k_:28s} 5th pct {v[0]:+.3f}  median {v[1]:+.3f}")
    report.ok(
        "historical stock-bond correlation is 0.02; raising it to 0.5 lowers the 5th percentile by"
        " 0.10 and the median by only 0.03; a 2-point lower equity mean lowers the median by 0.24"
        " and the 5th percentile by 0.14; moving to 80/20 raises the median by 0.20 and lowers the"
        " 5th percentile by 0.11",
        bool(
            round(corr, 2) == 0.02
            and round(sens["stock-bond correlation 0.5"][0], 2) == -0.10
            and round(sens["stock-bond correlation 0.5"][1], 2) == -0.03
            and round(sens["equity mean -2 points"][1], 2) == -0.24
            and round(sens["equity mean -2 points"][0], 2) == -0.14
            and round(sens["80/20 instead of 60/40"][1], 2) == 0.20
            and round(sens["80/20 instead of 60/40"][0], 2) == -0.11
        ),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Read the history from the repository root, then run the three parts with one report.

    The worked numbers of meth:scenario-simulation-analysis. The investment problem: a 60/40
    portfolio of the S&P 500 (with dividends) and 10-year Treasuries, rebalanced annually, held
    for ten years. Data: annual US returns 1928-2025 from Damodaran's histretSP workbook,
    January 2026. Seeds are fixed (20261020 for the bootstrap, 20261021 for the normal shocks);
    20,000 paths per simulation.

    Independent routes: scenario returns from the weights against a direct reading of the data
    rows; the Monte Carlo mean and standard deviation of the one-year return against the
    analytic w'mu and sqrt(w' Sigma w); the bootstrap's mean against the sample mean of the
    portfolio series; sensitivities as differences between re-simulated distributions that
    share the same random draws (common random numbers). One check is one executed ok() call (a
    call inside a loop counts once per iteration).

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the data
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    print_versions(np)
    portfolio = Portfolio(history=AssetClassHistory.read(root / DATA))
    report = CheckReport()
    check_historical_scenarios(report, portfolio)
    model = NormalReturns(mean=portfolio.assets.mean(axis=0), covariance=np.cov(portfolio.assets.T))
    z = np.random.default_rng(20261021).standard_normal((PATHS, HORIZON, 2))
    tw_mc = check_simulations(report, portfolio, model, z)
    check_sensitivities(report, model, z, tw_mc)
    print(f"\n{report.count} checks executed")
    if report.failures:
        print("FAILED:", report.failures)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
