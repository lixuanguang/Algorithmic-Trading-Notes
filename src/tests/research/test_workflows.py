"""Tests of the research package: its arguments, imports, helpers and workflow outputs."""

# The H.15, Treasury and inversion workflows read only committed extracts, so they run here
# against the committed outputs. The others read the gitignored reading materials; they are
# replayed against the retained evidence when the materials are present and skipped otherwise.
# Every run writes into a temporary repository root holding a copy of src/data.

import contextlib
import datetime as dt
import filecmp
import hashlib
import importlib
import io
import math
import pkgutil
import shutil
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
from trading_notes.data_folders import DATA, LOCAL_RUN, DataFolder
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
from trading_notes.research.workflow import WorkflowArguments

from ..import_probe import HEAVY, dependency_reads, import_effects

ROOT: Final = Path(__file__).resolve().parents[3]
MATERIALS: Final = ROOT / "reading_materials"
MODULES: Final = sorted(
    m.name for m in pkgutil.walk_packages(research.__path__, research.__name__ + ".")
)
SPREADS: Final = monthly_spreads.SpreadArguments.folder


def workspace(root: Path) -> Path:
    """Copy the retained data below src/data, without local runs, into a new root; return it."""
    shutil.copytree(ROOT / DATA, root / DATA, ignore=shutil.ignore_patterns(LOCAL_RUN.parts[0]))
    return root


def retained_hashes(root: Path) -> dict[str, str]:
    """Return the SHA-256 of every file below root/src/data outside local runs, by path."""
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((root / DATA).rglob("*"))
        if p.is_file() and LOCAL_RUN.parts[0] not in p.relative_to(root / DATA).parts
    }


class Sample(WorkflowArguments):
    """A workflow's arguments with one input of its own."""

    folder: ClassVar[DataFolder] = DataFolder(subsection="sample_folder")
    data: Path


class Arguments(unittest.TestCase):
    """--root and --output are parsed, made absolute and validated with the inputs."""

    def test_defaults_and_absolute_paths(self) -> None:
        """Relative paths resolve; the retained folders are the subsection's below src/data."""
        parser = Sample.parser("sample")
        parser.add_argument("data", type=Path)
        args = Sample.parse(parser, ["--root", "some/root", "input.csv"])
        self.assertTrue(args.root.is_absolute() and args.data.is_absolute())
        self.assertEqual(args.root, Path("some/root").resolve())
        self.assertIsNone(args.output)
        folder = args.root / "src" / "data" / "sample_folder"
        self.assertEqual(args.retained_inputs, folder / "inputs")
        self.assertEqual(args.retained_results, folder / "results")

    def test_runs_write_to_the_local_run(self) -> None:
        """By default results go to runs/local/results and rebuilt extracts to runs/local/inputs."""
        with tempfile.TemporaryDirectory() as tmp:
            args = Sample(root=Path(tmp), data=Path("x"))
            run = Path(tmp) / "src" / "data" / "sample_folder" / "runs" / "local"
            self.assertEqual(args.output_folder, run / "results")
            self.assertEqual(args.extract_folder, run / "inputs")
            self.assertEqual(sorted(p.name for p in run.iterdir()), ["inputs", "results"])
            self.assertFalse(args.retained_inputs.exists() or args.retained_results.exists())

    def test_output_folder_is_created(self) -> None:
        """An explicit output folder takes every file, and is created with its parents."""
        with tempfile.TemporaryDirectory() as tmp:
            parser = Sample.parser("sample")
            parser.add_argument("data", type=Path)
            out = Path(tmp) / "a" / "b"
            args = Sample.parse(parser, ["--output", str(out), "x"])
            self.assertEqual(args.output_folder, out.resolve())
            self.assertEqual(args.extract_folder, out.resolve())
            self.assertTrue(out.is_dir())

    def test_upstream_files(self) -> None:
        """The retained file by default; a requested file or run folder; never a fallback."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = Sample(root=root, data=Path("x"))
            retained = Sample.folder.results / "panel.csv"
            (root / retained).parent.mkdir(parents=True)
            (root / retained).write_text("retained\n")
            self.assertEqual(args.upstream(None, retained), root / retained)
            run = args.output_folder
            for missing in (run, run / "panel.csv", root / "absent" / "panel.csv"):
                with self.subTest(missing=missing):
                    with self.assertRaisesRegex(FileNotFoundError, "requested input not found"):
                        args.upstream(missing, retained)
            (run / "panel.csv").write_text("generated\n")
            self.assertEqual(args.upstream(run, retained), run / "panel.csv")
            self.assertEqual(args.upstream(run / "panel.csv", retained), run / "panel.csv")

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
        """Spreads written to the local run match the retained ones; so do the horizons.

        The runs change no retained file, and the inversion check reads the run's spreads when
        --spreads names its folder.
        """
        retained = ROOT / SPREADS.results
        with tempfile.TemporaryDirectory() as tmp:
            root = workspace(Path(tmp))
            before = retained_hashes(root)
            run = root / SPREADS.run_results
            for main, name in (
                (h15_spread.main, "h15-spread-monthly.csv"),
                (treasury_spread.main, "ust-10y3m-monthly.csv"),
            ):
                with self.subTest(name):
                    printed = self.run_main(main, ["--root", str(root)])
                    self.assertTrue(printed.startswith("months, first day, last day:"))
                    self.assertTrue(filecmp.cmp(run / name, retained / name, shallow=False))
            expected = (retained / "inversion-horizons.txt").read_text()
            for extra in (
                [],
                ["--spreads", str(run)],
                ["--spreads", str(run / h15_spread.MONTHLY)],
            ):
                with self.subTest(extra=extra):
                    printed = self.run_main(inversion_horizons.main, ["--root", str(root), *extra])
                    self.assertEqual(printed, expected)
            self.assertEqual(retained_hashes(root), before)
            self.assertEqual(
                sorted(p.name for p in run.iterdir()), [h15_spread.MONTHLY, treasury_spread.MONTHLY]
            )
            self.assertFalse((root / SPREADS.run_inputs).exists())

    def test_rebuilt_extract_goes_to_the_run_inputs(self) -> None:
        """--extract writes the daily extract to runs/local/inputs and reads it from there."""
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = Path(tmp) / "root", Path(tmp) / "raw"
            raw.mkdir()
            (raw / "y2006.csv").write_text('Date,"3 Mo","2 Yr","10 Yr"\n12/29/2006,5.0,4.8,4.7\n')
            (raw / "y2007.csv").write_text('Date,"3 Mo","2 Yr","10 Yr"\n01/02/2007,5.1,4.8,4.6\n')
            printed = self.run_main(
                treasury_spread.main, ["--root", str(root), "--extract", str(raw)]
            )
            self.assertEqual(
                printed,
                "daily rows: 2\nmonths, first day, last day: (2, '2006-12-29', '2007-01-02')\n",
            )
            daily = root / SPREADS.run_inputs / treasury_spread.DAILY
            self.assertEqual(
                daily.read_bytes(),
                b"date,cmt_3m,cmt_2y,cmt_10y\r\n2006-12-29,5.0,4.8,4.7\r\n2007-01-02,5.1,4.8,4.6\r\n",
            )
            monthly = (root / SPREADS.run_results / treasury_spread.MONTHLY).read_text()
            self.assertEqual(
                monthly.splitlines()[1:],
                ["2006-12,-0.3000,-0.1000,1,yes", "2007-01,-0.5000,-0.2000,1,yes"],
            )
            self.assertEqual([p.name for p in (root / DATA).iterdir()], [SPREADS.subsection])
            self.assertFalse((root / SPREADS.inputs).exists() or (root / SPREADS.results).exists())

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

    def test_missing_requested_input_fails(self) -> None:
        """A requested generated file that does not exist stops the run before any output."""
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp).resolve() / "runs" / h15_spread.MONTHLY
            done = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-m",
                    inversion_horizons.__name__,
                    "--root",
                    str(ROOT),
                    "--spreads",
                    str(missing),
                ],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
            self.assertEqual((done.returncode, done.stdout), (1, ""))
            self.assertIn(f"FileNotFoundError: requested input not found: {missing}", done.stderr)
            self.assertEqual(list(Path(tmp).iterdir()), [])


# Workflows replayed from the reading materials: module, inputs below the materials, and each
# output (below the workflow's local run folder; stdout as "-") with its retained file below
# src/data.
REPLAYS: Final[list[tuple[str, list[str], dict[str, str]]]] = [
    (
        "commodity_curves.backwardation",
        ["source-verification/empirical"],
        {
            "-": "commodity_curves/results/backwardation_results.txt",
            "results/backwardation_monthly.csv": (
                "commodity_curves/results/backwardation_monthly.csv"
            ),
        },
    ),
    (
        "commodity_curves.heating_oil",
        ["empirical-extensions/empirical"],
        {
            "-": "commodity_curves/results/heating_oil_results.txt",
            "results/heating_oil_monthly.csv": "commodity_curves/results/heating_oil_monthly.csv",
        },
    ),
    (
        "commodity_curves.hedging_pressure",
        ["derivatives-validation/empirical/cot"],
        {
            "-": "commodity_curves/results/hedging_pressure_results.txt",
            "results/hedging_pressure_monthly.csv": (
                "commodity_curves/results/hedging_pressure_monthly.csv"
            ),
        },
    ),
    (
        "futures_hedging.jet_fuel_hedge",
        [
            "derivatives-validation/empirical/EIA_jet_EER_EPJK_PF4_RGC_DPGd.xls",
            "empirical-extensions/empirical",
            "source-verification/empirical",
        ],
        {"-": "futures_hedging/results/jet_fuel_hedge_results.txt"},
    ),
    (
        "crypto_venues_perpetuals.deribit_options",
        ["empirical-extensions/deribit"],
        {
            "-": "crypto_venues_perpetuals/results/deribit-options-snapshot.txt",
        },
    ),
    (
        "crypto_venues_perpetuals.okx_options",
        [
            "derivatives-validation/empirical/okx_option_instruments_BTC-USD.json",
            "derivatives-validation/empirical/okx_option_oi_BTC-USD.json",
        ],
        {"-": "crypto_venues_perpetuals/results/okx-options-snapshot.txt"},
    ),
    (
        "gsw_treasury_curve.curve_checks",
        [
            "derivatives-validation/empirical/feds200628.csv",
            "derivatives-validation/empirical/feds200533.csv",
            "empirical-extensions/data/ACMTermPremium.xls",
        ],
        {"-": "gsw_treasury_curve/results/gsw-kw-acm.txt"},
    ),
    (
        "gsw_treasury_curve.acm_term_premium",
        ["empirical-extensions/data/ACMTermPremium.xls"],
        {
            "-": "gsw_treasury_curve/results/acm-term-premium-summary.txt",
        },
    ),
    (
        "macro_fx.ppp_out_of_sample",
        ["source-verification/empirical/fred"],
        {
            "-": "macro_fx/results/fx_ppp_results.txt",
            "results/fx_ppp_monthly.csv": "macro_fx/results/fx_ppp_monthly.csv",
        },
    ),
    (
        "macro_fx.carry_out_of_sample",
        ["source-verification/empirical/fred"],
        {
            "-": "macro_fx/results/fx_carry_results.txt",
            "results/fx_carry_monthly.csv": "macro_fx/results/fx_carry_monthly.csv",
        },
    ),
    (
        "macro_regimes_data.deflation_row",
        ["."],
        {
            "-": "macro_regimes_data/results/deflation_results.txt",
            "results/deflation_quarters.csv": "macro_regimes_data/results/deflation_quarters.csv",
        },
    ),
    (
        "macro_regimes_data.inflation_quarterly",
        ["."],
        {
            "-": "macro_regimes_data/results/inflation_quarterly_results.txt",
            "results/inflation_quarterly_vintage_quarters.csv": (
                "macro_regimes_data/results/inflation_quarterly_vintage_quarters.csv"
            ),
        },
    ),
    (
        "macro_regimes_data.inflation_regime",
        ["."],
        {
            "-": "macro_regimes_data/results/inflation_results.txt",
            "results/inflation_monthly_vintage_quarters.csv": (
                "macro_regimes_data/results/inflation_monthly_vintage_quarters.csv"
            ),
        },
    ),
    # The retained regime_quarters.csv prints one zero as -0.000, which the run prints as 0.000.
    (
        "macro_regimes_data.regime_recession",
        ["source-verification/empirical"],
        {
            "-": "macro_regimes_data/results/regime_recession_results.txt",
        },
    ),
    (
        "global_macro.down_months",
        [
            "method-validation/empirical/BarclayHedge_Global_Macro_Index_2026-10-17.html",
            "source-verification/empirical/french/F-F_Research_Data_Factors.csv",
        ],
        {
            "-": "global_macro/results/global_macro_results.txt",
            "results/global_macro_monthly.csv": "global_macro/results/global_macro_monthly.csv",
        },
    ),
    (
        "global_macro.down_months_2014",
        [
            "empirical-extensions/barclayhedge/Barclay_Global_Macro_Indexhistorical_data.xls",
            "source-verification/empirical/french/F-F_Research_Data_Factors.csv",
        ],
        {
            "-": "global_macro/results/global_macro_results_2014.txt",
            "results/global_macro_monthly_2014.csv": (
                "global_macro/results/global_macro_monthly_2014.csv"
            ),
        },
    ),
    (
        "return_predictability.goyal_extract",
        [
            "return-predictability/goyal/PredictorData2005_original.xlsx",
        ],
        {
            "inputs/goyal-annual-1871-2025.csv": (
                "return_predictability/inputs/goyal-annual-1871-2025.csv"
            ),
            "inputs/goyal-monthly-1871-2025.csv": (
                "return_predictability/inputs/goyal-monthly-1871-2025.csv"
            ),
        },
    ),
    (
        "return_predictability.goyal_extract_predictors",
        [
            "return-predictability/goyal/PredictorData2005_original.xlsx",
        ],
        {
            "inputs/goyal-annual-predictors-1871-2025.csv": (
                "return_predictability/inputs/goyal-annual-predictors-1871-2025.csv"
            ),
        },
    ),
    (
        "term_structure_returns.gsw_month_end",
        ["derivatives-validation/empirical/feds200628.csv"],
        {
            "inputs/gsw-month-end-zero.csv": "term_structure_returns/inputs/gsw-month-end-zero.csv",
        },
    ),
]


# Labels reworded since the evidence was retained, by retained file: the retained text, the
# text a run prints now, and how often it occurs. Every other character must still match.
RELABELLED: Final[dict[str, list[tuple[str, str, int]]]] = {
    "futures_hedging/results/jet_fuel_hedge_results.txt": [
        (" roll weeks dropped", " weeks excluded (roll or unknown contract)", 2),
    ],
    "commodity_curves/results/backwardation_results.txt": [
        (
            "exploratory (added after the v1 run, not pre-specified)",
            "exploratory (not pre-specified)",
            2,
        ),
    ],
    "commodity_curves/results/heating_oil_results.txt": [
        ("superseded simple-return P          ", "simple-return P                     ", 1),
        ("the v2 executable rule", "the executable rule", 1),
    ],
    "commodity_curves/results/heating_oil_monthly.csv": [
        (",r_simple_superseded,", ",r_simple,", 1),
    ],
    "macro_fx/results/fx_carry_results.txt": [
        ("; superseded row-stacked t:", "; row-stacked t:", 2),
    ],
    "macro_fx/results/fx_ppp_results.txt": [
        ("; superseded row-stacked t:", "; row-stacked t:", 2),
    ],
    "macro_regimes_data/results/inflation_quarterly_results.txt": [
        (
            " (empirical extensions (2026-10-17) used 111 monthly vintages)",
            " (the monthly-vintage test uses 111 vintages)",
            1,
        ),
    ],
    "global_macro/results/global_macro_results_2014.txt": [
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
        """Run each workflow on a copy of src/data from an unrelated directory and compare.

        Each run writes its compared outputs to its subsection's local run folder and changes no
        retained file; downstream workflows read the retained files their upstream ones wrote.
        """
        for module, inputs, outputs in REPLAYS:
            with self.subTest(module), tempfile.TemporaryDirectory() as tmp:
                root = workspace(Path(tmp) / "root")
                before = retained_hashes(root)
                done = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-W",
                        "error",
                        "-m",
                        f"{research.__name__}.{module}",
                        "--root",
                        str(root),
                        *(str(MATERIALS / p) for p in inputs),
                    ],
                    cwd=tmp,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual((done.returncode, done.stderr), (0, ""))
                run = root / DATA / module.partition(".")[0] / LOCAL_RUN
                for produced, retained in outputs.items():
                    expected = (ROOT / DATA / retained).read_text()
                    for old, new, count in RELABELLED.get(retained, []):
                        self.assertEqual(expected.count(old), count, (retained, old))
                        self.assertNotIn(new, expected, retained)
                        expected = expected.replace(old, new)
                    actual = done.stdout if produced == "-" else (run / produced).read_text()
                    self.assertEqual(actual, expected, retained)
                written = {p.relative_to(run).as_posix() for p in run.rglob("*") if p.is_file()}
                self.assertLessEqual(set(outputs) - {"-"}, written)
                self.assertEqual(retained_hashes(root), before)

    def test_relabelled_files_are_replayed(self) -> None:
        """Every reworded file is among the replayed outputs."""
        replayed = {retained for _, _, outputs in REPLAYS for retained in outputs.values()}
        self.assertLessEqual(set(RELABELLED), replayed)


if __name__ == "__main__":
    unittest.main()
