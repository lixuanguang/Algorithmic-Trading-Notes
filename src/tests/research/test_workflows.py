"""Tests of the research package: its arguments, imports, helpers and workflow outputs."""

# The H.15, Treasury and inversion workflows read only committed extracts, so they run here
# against the committed outputs. The others read the gitignored reading materials; they are
# replayed against the retained evidence when the materials are present and skipped otherwise.

import contextlib
import datetime as dt
import filecmp
import importlib
import io
import math
import pkgutil
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import ClassVar, Final

import numpy as np
import pydantic

from trading_notes import research
from trading_notes.research import fred, spreadsheets
from trading_notes.research.business_cycles_policy import (
    h15_spread,
    inversion_horizons,
    monthly_spreads,
    treasury_spread,
)
from trading_notes.research.commodity_curves.backwardation import TimingRule
from trading_notes.research.futures_hedging.jet_fuel_hedge import WeeklyChanges
from trading_notes.research.global_macro import index_returns
from trading_notes.research.macro_fx.currencies import RandomWalkComparison, turnover
from trading_notes.research.macro_regimes_data import regime_inputs
from trading_notes.research.regressions import NeweyWestOls
from trading_notes.research.workflow import ARTEFACTS, WorkflowArguments

from ..import_probe import HEAVY, dependency_reads, import_effects

ROOT: Final = Path(__file__).resolve().parents[3]
MATERIALS: Final = ROOT / "reading_materials"
MODULES: Final = sorted(
    m.name for m in pkgutil.walk_packages(research.__path__, research.__name__ + ".")
)


class Sample(WorkflowArguments):
    """A workflow's arguments with one input of its own."""

    folder: ClassVar[str] = "sample-folder"
    data: Path


class Arguments(unittest.TestCase):
    """--root and --output are parsed, made absolute and validated with the inputs."""

    def test_defaults_and_absolute_paths(self) -> None:
        """Relative paths resolve; output defaults to the artefact folder below the root."""
        parser = Sample.parser("sample")
        parser.add_argument("data", type=Path)
        args = Sample.parse(parser, ["--root", "some/root", "input.csv"])
        self.assertTrue(args.root.is_absolute() and args.data.is_absolute())
        self.assertEqual(args.root, Path("some/root").resolve())
        self.assertIsNone(args.output)
        self.assertEqual(args.artefacts, args.root / ARTEFACTS / "sample-folder")

    def test_output_folder_is_created(self) -> None:
        """An explicit output folder is used, and created with its parents."""
        with tempfile.TemporaryDirectory() as tmp:
            parser = Sample.parser("sample")
            parser.add_argument("data", type=Path)
            out = Path(tmp) / "a" / "b"
            args = Sample.parse(parser, ["--output", str(out), "x"])
            self.assertEqual(args.output_folder, out.resolve())
            self.assertTrue(out.is_dir())

    def test_records_are_frozen_and_strict(self) -> None:
        """Arguments cannot be changed after validation, and a missing input is an error."""
        args = Sample(root=Path("/r"), data=Path("/d"))
        with self.assertRaises(pydantic.ValidationError):
            setattr(args, "root", Path("/elsewhere"))
        with self.assertRaises(pydantic.ValidationError):
            Sample.model_validate({"root": Path("/r")})


class Imports(unittest.TestCase):
    """Importing a research module reads no data, prints nothing and leaves random state alone."""

    def test_modules_import_without_side_effects(self) -> None:
        """Each module, in its own process, opens only what its dependencies open on import."""
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            # SciPy's stats module reads NumPy's install record, which `import scipy` does not.
            allowed = dependency_reads((*HEAVY, "scipy.stats"), cwd)
            for name in MODULES:
                with self.subTest(name):
                    effects = import_effects([name], HEAVY, cwd, preload=("numpy",))
                    self.assertEqual(effects.returncode, 0, effects.stderr)
                    self.assertEqual(effects.reads_beyond(allowed), [])
                    self.assertEqual((effects.printed, effects.stderr), ("", ""))
                    self.assertTrue(effects.random_unchanged)
                    self.assertEqual(list(cwd.iterdir()), [])

    def test_every_workflow_has_a_main(self) -> None:
        """A module with a parser has main(argv) and runs it only under __main__."""
        for name in MODULES:
            module = importlib.import_module(name)
            source = Path(module.__file__ or "").read_text()
            if "def main(" in source:
                with self.subTest(name):
                    self.assertIn('if __name__ == "__main__":', source)
                    self.assertIn("sys.exit(main())", source)


class Helpers(unittest.TestCase):
    """The shared readers and statistics on small hand-made inputs."""

    def test_fred_series(self) -> None:
        """Blanks and '.' are skipped; a repeated month keeps its last value or is averaged."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "series.csv"
            path.write_text(
                "observation_date,X\n2001-01-01,1.0\n2001-01-15,.\n2001-01-29,3.0\n"
                "2001-02-05,\n2001-03-01,-2.5\n"
            )
            self.assertEqual(
                fred.observations(path), [((2001, 1), 1.0), ((2001, 1), 3.0), ((2001, 3), -2.5)]
            )
            self.assertEqual(fred.monthly_values(path), {(2001, 1): 3.0, (2001, 3): -2.5})
            self.assertEqual(fred.monthly_means(path), {(2001, 1): 2.0, (2001, 3): -2.5})

    def test_excel_dates(self) -> None:
        """Serial 1 is 31 December 1899 in xlrd's convention; fractions are dropped."""
        self.assertEqual(spreadsheets.excel_date(1.0), dt.date(1899, 12, 31))
        self.assertEqual(spreadsheets.excel_date(45000.75), dt.date(2023, 3, 15))
        with self.assertRaises(ValueError):
            spreadsheets.excel_date("Date")

    def test_newey_west_without_lags_is_white(self) -> None:
        """With no lags the covariance is White's; the slope is the OLS slope."""
        rng = np.random.default_rng(3)
        x = rng.standard_normal(200)
        y = 0.5 + 2.0 * x + rng.standard_normal(200)
        fit = NeweyWestOls.fit(y, x, lags=0)
        A = np.column_stack([np.ones(200), x])
        b = np.linalg.solve(A.T @ A, A.T @ y)
        e = y - A @ b
        bread = np.linalg.inv(A.T @ A)
        V = bread @ (A.T * e**2) @ A @ bread
        np.testing.assert_allclose(fit.coefficients, b, rtol=1e-12)
        np.testing.assert_allclose(fit.t_stats, b / np.sqrt(np.diag(V)), rtol=1e-10)

    def test_regime_statistics(self) -> None:
        """Welch's t by hand, the indicator slope as a difference in means, and run counts."""
        a = np.array([1.0, 2.0, 3.0, 4.0])
        b = np.array([0.0, 0.0, 1.0])
        se = math.sqrt(a.var(ddof=1) / 4 + b.var(ddof=1) / 3)
        self.assertAlmostEqual(regime_inputs.welch_t(a, b), (2.5 - 1 / 3) / se, places=14)
        y = np.concatenate([a, b])
        d = np.array([1.0] * 4 + [0.0] * 3)
        self.assertAlmostEqual(regime_inputs.indicator_slope(y, d, 0)[0], 2.5 - 1 / 3, places=12)
        self.assertEqual(regime_inputs.episodes([True, True, False, 1, 0, 1, 1]), 3)
        self.assertEqual(regime_inputs.episodes([]), 0)
        self.assertEqual(regime_inputs.month_label("1999:07"), (1999, 7))
        with self.assertRaises(ValueError):
            regime_inputs.month_label(1999.07)

    def test_month_coverage(self) -> None:
        """Gaps are errors; only the month both last observed and retrieved is incomplete."""

        def rows(*dates: str) -> monthly_spreads.DailyRows:
            return monthly_spreads.DailyRows(rows=[{"date": d, "x": "1"} for d in dates])

        daily = rows("1999-11-30", "1999-12-01", "1999-12-31", "2000-01-03")
        self.assertEqual([len(v) for v in daily.months().values()], [1, 2, 1])
        self.assertEqual(list(daily.months()), ["1999-11", "1999-12", "2000-01"])
        with self.assertRaises(ValueError):
            rows("1999-11-30", "2000-01-03").months()
        with self.assertRaises(ValueError):
            daily.months(lambda r: not r["date"].startswith("1999-12"))
        self.assertFalse(rows("2026-10-15").complete("2026-10"))
        self.assertTrue(rows("2026-10-15").complete("2026-09"))
        self.assertTrue(rows("2026-09-30").complete("2026-09"))
        self.assertAlmostEqual(h15_spread.bond_equivalent(5.0), 100 * 18.25 / (360 - 4.55))

    def test_daily_extracts(self) -> None:
        """The raw H.15 XML and Treasury CSVs give status-A, both-series, sorted daily rows."""
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            xml = folder / "h15.xml"
            xml.write_text(
                '<m:Data xmlns:m="urn:x"><m:Series SERIES_NAME="RIFSGFSM03_N.B">'
                '<m:Obs TIME_PERIOD="1961-12-29" OBS_STATUS="A" OBS_VALUE="2.6"/>'
                '<m:Obs TIME_PERIOD="1962-01-02" OBS_STATUS="A" OBS_VALUE="2.7"/>'
                '<m:Obs TIME_PERIOD="1962-01-03" OBS_STATUS="ND" OBS_VALUE="2.8"/>'
                '<m:Obs TIME_PERIOD="1962-01-04" OBS_STATUS="A" OBS_VALUE="2.9"/>'
                '</m:Series><m:Series SERIES_NAME="RIFLGFCY10_N.B">'
                '<m:Obs TIME_PERIOD="1961-12-29" OBS_STATUS="A" OBS_VALUE="3.9"/>'
                '<m:Obs TIME_PERIOD="1962-01-02" OBS_STATUS="A" OBS_VALUE="4.0"/>'
                '<m:Obs TIME_PERIOD="1962-01-03" OBS_STATUS="A" OBS_VALUE="4.1"/>'
                '</m:Series><m:Series SERIES_NAME="OTHER">'
                '<m:Obs TIME_PERIOD="1962-01-04" OBS_STATUS="A" OBS_VALUE="9"/>'
                "</m:Series></m:Data>"
            )
            daily = folder / "daily.csv"
            self.assertEqual(h15_spread.H15Release.parse(xml).write_daily(daily), 1)
            self.assertEqual(
                daily.read_bytes(), b"date,tb3m_discount,cmt_10y\r\n1962-01-02,2.7,4.0\r\n"
            )
            raw = folder / "raw"
            raw.mkdir()
            (raw / "y2007.csv").write_text('Date,"3 Mo","2 Yr","10 Yr"\n01/02/2007,5.0,4.8,4.7\n')
            (raw / "y2006.csv").write_text('Date,"3 Mo","10 Yr"\n12/29/2006,5.02,4.71\n')
            (raw / "notes.csv").write_text("ignored\n")
            files = treasury_spread.ParYieldFiles.read(raw)
            self.assertEqual(
                files.rows,
                [("2006-12-29", "5.02", "", "4.71"), ("2007-01-02", "5.0", "4.8", "4.7")],
            )

    def test_index_tables(self) -> None:
        """BarclayHedge's page and Ken French's CSV are read as decimals, footers ignored."""
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.html"
            cells = " ".join(["<td>1.50%</td>", "<td>-0.25%</td>", "<td>est</td>"] + ["x"] * 10)
            page.write_text(
                "<html><script>ignored</script><table><tr><th>Jan Feb Mar Apr May Jun Jul Aug"
                f" Sep Oct Nov Dec YTD</th></tr><tr><td>2020</td> {cells} </tr></table></html>"
            )
            self.assertEqual(
                index_returns.barclay_page(page), {(2020, 1): 0.015, (2020, 2): -0.0025}
            )
            french = Path(tmp) / "f.csv"
            french.write_text(
                "header\n,Mkt-RF,SMB,HML,RF\n192607,2.96,-2.56,-2.43,0.22\n"
                "192608,2.64,-1.17,3.82,0.25\n\n Annual Factors\n1927,1,2,3,4\n"
            )
            self.assertEqual(
                index_returns.french_factors(french),
                {(1926, 7): (0.0296, 0.0022), (1926, 8): (0.0264, 0.0025)},
            )
        sr = index_returns.SharpeRatio.of(np.array([0.01, 0.03, 0.02, 0.0]))
        self.assertAlmostEqual(sr.value, 0.015 / float(np.std([0.01, 0.03, 0.02, 0.0], ddof=1)))
        self.assertAlmostEqual(sr.se, math.sqrt((1 + sr.value**2 / 2) / 4))


class SharedStatistics(unittest.TestCase):
    """The forecast, portfolio and index records the workflows share, on hand values."""

    def test_random_walk_comparison(self) -> None:
        """R^2 against forecasting zero, and the Clark-West differentials a^2 - (e^2 - f^2)."""
        rw = RandomWalkComparison(actual=np.array([1.0, -1.0, 2.0]), forecast=np.array([0.5, 0, 1]))
        self.assertEqual((rw.sse, rw.sse_random_walk), (2.25, 6.0))
        self.assertEqual(rw.r2, 0.625)
        np.testing.assert_array_equal(rw.clark_west, [1.0, 0.0, 4.0])

    def test_turnover(self) -> None:
        """Weights entering, leaving and unchanged; an empty book starts from zero."""
        self.assertEqual(turnover({"A": 0.5, "B": -0.5}, {"A": 0.5, "C": -0.5}), 1.0)
        self.assertEqual(turnover({"A": 0.5, "B": -0.5}, {}), 1.0)

    def test_timing_rule(self) -> None:
        """Long when backwardated, else short: the short's net return also pays the ticks."""
        rule = TimingRule(
            gross=np.array([0.1, -0.2, 0.05]),
            net=np.array([0.09, -0.21, 0.04]),
            backwardated=np.array([True, False, False]),
        )
        np.testing.assert_allclose(rule.returns, [0.09, 0.19, -0.06], rtol=0, atol=1e-15)
        self.assertEqual(
            rule.means_by_state(),
            "mean monthly r: backwardated +10.00% (n 1), contango -7.50% (n 2)",
        )

    def test_index_months(self) -> None:
        """The monthly table round-trips at four decimals; `since` keeps the later months."""
        data = index_returns.IndexMonths.of(
            [(2021, 12), (2022, 1), (2022, 2)],
            {(2021, 12): 0.01234, (2022, 1): -0.02, (2022, 2): 0.0},
            {(2021, 12): (-0.03, 0.0001), (2022, 1): (0.01, 0.0), (2022, 2): (-0.01, 0.0)},
        )
        self.assertEqual(data.span(), "2021-12 to 2022-02")
        recent = data.since((2022, 1))
        self.assertEqual(recent.months, [(2022, 1), (2022, 2)])
        np.testing.assert_array_equal(recent.market, [0.01, -0.01])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "monthly.csv"
            data.write(path)
            self.assertEqual(path.read_text().splitlines()[1], "2021-12,0.0123,-0.0300,0.0001")
            back = index_returns.IndexMonths.read(path)
        self.assertEqual(back.months, data.months)
        self.assertEqual(back.returns_by_month()[(2021, 12)], 0.0123)


class JetFuelWeeks(unittest.TestCase):
    """Weekly hedge changes keep only weeks whose contract 1 is known to be one contract."""

    def test_rolls_and_unknown_fronts_are_dropped(self) -> None:
        """Weekdays of 2026 to Friday 23 October: WTI's October contract expires on 22 September.

        The front month is unknown from 15 October, ten days before November's 25 October
        anchor, which lies after the data end.
        """
        start = dt.date(2026, 1, 1)
        days = [start + dt.timedelta(days=k) for k in range(296)]
        prices = {d: float(k) for k, d in enumerate(days) if d.weekday() < 5}
        changes = WeeklyChanges.of(prices, prices, "WTI", 0.5)
        fridays = dict(zip(changes.dates, changes.futures, strict=True))
        self.assertNotIn(dt.date(2026, 9, 25), fridays)  # the September roll
        self.assertEqual(fridays[dt.date(2026, 10, 2)], 3.5)  # seven calendar days, scaled
        self.assertEqual(changes.dates[-1], dt.date(2026, 10, 9))
        self.assertNotIn(dt.date(2026, 10, 16), fridays)  # known to unknown
        self.assertNotIn(dt.date(2026, 10, 23), fridays)  # unknown to unknown
        self.assertEqual(len(changes.dates) + changes.dropped, 42)


class CommittedInputs(unittest.TestCase):
    """The workflows that read committed extracts reproduce the committed outputs."""

    def run_main(self, main: Callable[[Sequence[str] | None], int], argv: list[str]) -> str:
        """Run a workflow's main in process and return what it printed."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(argv), 0)
        return out.getvalue()

    def test_spreads_and_inversions(self) -> None:
        """Monthly spreads match the committed CSVs; the horizons match the committed text."""
        folder = ROOT / ARTEFACTS / "multi-asset-systematic-macro"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            for main, name in (
                (h15_spread.main, "h15-spread-monthly.csv"),
                (treasury_spread.main, "ust-10y3m-monthly.csv"),
            ):
                with self.subTest(name):
                    printed = self.run_main(main, ["--root", str(ROOT), "--output", str(out)])
                    self.assertTrue(printed.startswith("months, first day, last day:"))
                    self.assertTrue(filecmp.cmp(out / name, folder / name, shallow=False))
            printed = self.run_main(inversion_horizons.main, ["--root", str(ROOT)])
            self.assertEqual(printed, (folder / "inversion-horizons.txt").read_text())

    def test_command_line_exit_status(self) -> None:
        """Run as a module, a workflow exits 0 on success and 2 on a usage error."""
        with tempfile.TemporaryDirectory() as tmp:
            ok = subprocess.run(
                [sys.executable, "-I", "-m", inversion_horizons.__name__, "--root", str(ROOT)],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
            self.assertEqual((ok.returncode, ok.stderr), (0, ""))
            bad = subprocess.run(
                [sys.executable, "-I", "-m", inversion_horizons.__name__, "--unknown"],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
            self.assertEqual(bad.returncode, 2)
            self.assertIn("unrecognized arguments", bad.stderr)


# Workflows replayed from the reading materials: module, inputs below the materials, and the
# outputs compared with the retained evidence (stdout as "-").
EVIDENCE: Final = "notes/artefacts"
REPLAYS: Final[list[tuple[str, list[str], dict[str, str]]]] = [
    (
        "commodity_curves.backwardation",
        ["source-verification/empirical"],
        {
            "-": "commodity-storage-curves/backwardation_results.txt",
            "backwardation_monthly.csv": "commodity-storage-curves/backwardation_monthly.csv",
        },
    ),
    (
        "commodity_curves.heating_oil",
        ["empirical-extensions/empirical"],
        {
            "-": "commodity-storage-curves/heating_oil_results.txt",
            "heating_oil_monthly.csv": "commodity-storage-curves/heating_oil_monthly.csv",
        },
    ),
    (
        "commodity_curves.hedging_pressure",
        ["derivatives-validation/empirical/cot"],
        {
            "-": "commodity-storage-curves/hedging_pressure_results.txt",
            "hedging_pressure_monthly.csv": "commodity-storage-curves/hedging_pressure_monthly.csv",
        },
    ),
    (
        "futures_hedging.jet_fuel_hedge",
        [
            "derivatives-validation/empirical/EIA_jet_EER_EPJK_PF4_RGC_DPGd.xls",
            "empirical-extensions/empirical",
            "source-verification/empirical",
        ],
        {"-": "commodity-hedging/jet_fuel_hedge_results.txt"},
    ),
    (
        "crypto_venues_perpetuals.deribit_options",
        ["empirical-extensions/deribit"],
        {
            "-": "crypto-perpetuals/deribit-options-snapshot.txt",
        },
    ),
    (
        "crypto_venues_perpetuals.okx_options",
        [
            "derivatives-validation/empirical/okx_option_instruments_BTC-USD.json",
            "derivatives-validation/empirical/okx_option_oi_BTC-USD.json",
        ],
        {"-": "crypto-perpetuals/okx-options-snapshot.txt"},
    ),
    (
        "gsw_treasury_curve.curve_checks",
        [
            "derivatives-validation/empirical/feds200628.csv",
            "derivatives-validation/empirical/feds200533.csv",
            "empirical-extensions/data/ACMTermPremium.xls",
        ],
        {"-": "curve-term-structure/gsw-kw-acm.txt"},
    ),
    (
        "gsw_treasury_curve.acm_term_premium",
        ["empirical-extensions/data/ACMTermPremium.xls"],
        {
            "-": "rates-credit-mortgages/acm-term-premium-summary.txt",
        },
    ),
    (
        "macro_fx.ppp_out_of_sample",
        ["source-verification/empirical/fred"],
        {
            "-": "fx-determination-forecasting/fx_ppp_results.txt",
            "fx_ppp_monthly.csv": "fx-determination-forecasting/fx_ppp_monthly.csv",
        },
    ),
    (
        "macro_fx.carry_out_of_sample",
        ["source-verification/empirical/fred"],
        {
            "-": "fx-determination-forecasting/fx_carry_results.txt",
            "fx_carry_monthly.csv": "fx-determination-forecasting/fx_carry_monthly.csv",
        },
    ),
    (
        "macro_regimes_data.deflation_row",
        ["."],
        {
            "-": "macro-regimes-stock-bond/deflation_results.txt",
            "deflation_quarters.csv": "macro-regimes-stock-bond/deflation_quarters.csv",
        },
    ),
    (
        "macro_regimes_data.inflation_quarterly",
        ["."],
        {
            "-": "macro-regimes-stock-bond/inflation_quarterly_results.txt",
            "inflation_quarterly_vintage_quarters.csv": (
                "macro-regimes-stock-bond/inflation_quarterly_vintage_quarters.csv"
            ),
        },
    ),
    (
        "macro_regimes_data.inflation_regime",
        ["."],
        {
            "-": "macro-regimes-stock-bond/inflation_results.txt",
            "inflation_monthly_vintage_quarters.csv": (
                "macro-regimes-stock-bond/inflation_monthly_vintage_quarters.csv"
            ),
        },
    ),
    # The retained regime_quarters.csv prints one zero as -0.000, which the run prints as 0.000.
    (
        "macro_regimes_data.regime_recession",
        ["source-verification/empirical"],
        {
            "-": "macro-regimes-stock-bond/regime_recession_results.txt",
        },
    ),
    (
        "global_macro.down_months",
        [
            "method-validation/empirical/BarclayHedge_Global_Macro_Index_2026-10-17.html",
            "source-verification/empirical/french/F-F_Research_Data_Factors.csv",
        ],
        {
            "-": "multi-asset-systematic-macro/global_macro_results.txt",
            "global_macro_monthly.csv": "multi-asset-systematic-macro/global_macro_monthly.csv",
        },
    ),
    (
        "global_macro.down_months_2014",
        [
            "empirical-extensions/barclayhedge/Barclay_Global_Macro_Indexhistorical_data.xls",
            "source-verification/empirical/french/F-F_Research_Data_Factors.csv",
        ],
        {
            "-": "multi-asset-systematic-macro/global_macro_results_2014.txt",
            "global_macro_monthly_2014.csv": (
                "multi-asset-systematic-macro/global_macro_monthly_2014.csv"
            ),
        },
    ),
    (
        "return_predictability.goyal_extract",
        [
            "return-predictability/goyal/PredictorData2005_original.xlsx",
        ],
        {
            "goyal-annual-1871-2025.csv": "return-predictability/goyal-annual-1871-2025.csv",
            "goyal-monthly-1871-2025.csv": "return-predictability/goyal-monthly-1871-2025.csv",
        },
    ),
    (
        "return_predictability.goyal_extract_predictors",
        [
            "return-predictability/goyal/PredictorData2005_original.xlsx",
        ],
        {
            "goyal-annual-predictors-1871-2025.csv": (
                "return-predictability/goyal-annual-predictors-1871-2025.csv"
            ),
        },
    ),
    (
        "term_structure_returns.gsw_month_end",
        [],
        {
            "gsw-month-end-zero.csv": "term-structure-dynamics/gsw-month-end-zero.csv",
        },
    ),
]


# Labels reworded since the evidence was retained, by retained file: the retained text, the
# text a run prints now, and how often it occurs. Every other character must still match.
RELABELLED: Final[dict[str, list[tuple[str, str, int]]]] = {
    "commodity-hedging/jet_fuel_hedge_results.txt": [
        (" roll weeks dropped", " weeks excluded (roll or unknown contract)", 2),
    ],
    "commodity-storage-curves/backwardation_results.txt": [
        (
            "exploratory (added after the v1 run, not pre-specified)",
            "exploratory (not pre-specified)",
            2,
        ),
    ],
    "commodity-storage-curves/heating_oil_results.txt": [
        ("superseded simple-return P          ", "simple-return P                     ", 1),
        ("the v2 executable rule", "the executable rule", 1),
    ],
    "commodity-storage-curves/heating_oil_monthly.csv": [
        (",r_simple_superseded,", ",r_simple,", 1),
    ],
    "fx-determination-forecasting/fx_carry_results.txt": [
        ("; superseded row-stacked t:", "; row-stacked t:", 2),
    ],
    "fx-determination-forecasting/fx_ppp_results.txt": [
        ("; superseded row-stacked t:", "; row-stacked t:", 2),
    ],
    "macro-regimes-stock-bond/inflation_quarterly_results.txt": [
        (
            " (empirical extensions (2026-10-17) used 111 monthly vintages)",
            " (the monthly-vintage test uses 111 vintages)",
            1,
        ),
    ],
    "multi-asset-systematic-macro/global_macro_results_2014.txt": [
        ("(matches the audited snapshot)", "(matches the recorded snapshot)", 1),
        (
            "revision check against method validation (2026-10-17)'s page values",
            "revision check against the index page's values of 2026-10-17",
            1,
        ),
    ],
}


@unittest.skipUnless(MATERIALS.is_dir(), "the gitignored reading_materials folder is absent")
class RetainedEvidence(unittest.TestCase):
    """Each workflow, run on the reading materials, reproduces its retained outputs exactly."""

    def test_replays(self) -> None:
        """Run each workflow into a temporary folder from an unrelated directory and compare."""
        for module, inputs, outputs in REPLAYS:
            with self.subTest(module), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "out"
                done = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-W",
                        "error",
                        "-m",
                        f"{research.__name__}.{module}",
                        "--root",
                        str(ROOT),
                        "--output",
                        str(out),
                        *(str(MATERIALS / p) for p in inputs),
                    ],
                    cwd=tmp,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual((done.returncode, done.stderr), (0, ""))
                for produced, retained in outputs.items():
                    expected = (ROOT / EVIDENCE / retained).read_text()
                    for old, new, count in RELABELLED.get(retained, []):
                        self.assertEqual(expected.count(old), count, (retained, old))
                        self.assertNotIn(new, expected, retained)
                        expected = expected.replace(old, new)
                    actual = done.stdout if produced == "-" else (out / produced).read_text()
                    self.assertEqual(actual, expected, retained)

    def test_relabelled_files_are_replayed(self) -> None:
        """Every reworded file is among the replayed outputs."""
        replayed = {retained for _, _, outputs in REPLAYS for retained in outputs.values()}
        self.assertLessEqual(set(RELABELLED), replayed)


if __name__ == "__main__":
    unittest.main()
