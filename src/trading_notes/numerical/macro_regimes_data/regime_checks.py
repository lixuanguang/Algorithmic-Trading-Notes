"""The recession-regime test's outputs: window definitions, dollar series and preserved results."""

import re
import sys
from collections.abc import Sequence
from typing import Final

from trading_notes.data_folders import DataFolder
from trading_notes.numerical.macro_regimes_data.regime_panel import RegimePanel, add_months
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.repository import repository_root

# The test's retained outputs, below the repository root.
FOLDER: Final = DataFolder(subsection="macro_regimes_data")
# The first run's ex-post any-overlap results (regime mean, difference, t) as it printed them,
# from regime_recession_results.txt of 17 October 2026 (commit 820517a).
FIRST_RUN: Final = {
    "dy10": ("-0.135", "-0.156", "-1.03"),
    "dcred": ("+0.218", "+0.248", "+1.78"),
    "eq": ("-0.919", "-3.091", "-1.41"),
    "dfn": ("+1.018", "+1.114", "+1.21"),
    "usd": ("+1.341", "+0.795", "+1.14"),
}


def result_triple(pattern: str, text: str) -> tuple[str, ...]:
    """Return the regime mean, difference and t statistic that the pattern captures in text.

    Raises:
        ValueError: If the results text has no line matching the pattern.
    """
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"no results line matches {pattern!r}")
    return match.groups()


def check_panel(report: CheckReport, panel: RegimePanel) -> None:
    """Checks 1 and 3: the two window definitions, and the dates of the two dollar series."""
    report.same("all-months subset of any-overlap", panel.all_months_within_any(), True)
    report.same("any-overlap count", panel.any_overlap_count(), 34)
    report.same("all-months count", panel.all_months_count(), 23)
    report.same(
        "goods-only only for windows ending by 2019-12",
        all(
            add_months(q.vintage_month, 3) <= "2019-12" for q in panel.quarters if q.usd_goods_only
        ),
        True,
    )
    report.same(
        "goods-and-services only from 2006-01",
        all(q.vintage_month >= "2006-01" for q in panel.quarters if q.usd_goods_services),
        True,
    )


def check_results(report: CheckReport, current: str) -> None:
    """Checks 2 and 4: the first run's any-overlap results preserved, real time tested first."""
    v2_block = current.split("ANY OVERLAP (v1 definition)")[1].split(
        "== ex-post NBER window, ALL MONTHS"
    )[0]
    for k in ("dy10", "dcred", "eq", "dfn"):
        b = result_triple(
            rf"\n  {k}\s+[0-9-]+: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), Welch t ([+-][0-9.]+)",
            v2_block,
        )
        report.same(f"v1 any-overlap result preserved for {k}", b, FIRST_RUN[k])
    b = result_triple(
        r"usd \(v1 splice[^)]*\)\s+[0-9-]+: regime ([+-][0-9.]+).*diff ([+-][0-9.]+),"
        r" Welch t ([+-][0-9.]+)",
        v2_block,
    )
    report.same("v1 any-overlap dollar (splice) preserved", b, FIRST_RUN["usd"])
    report.same(
        "real-time block precedes and is labelled the only test",
        current.index("REAL-TIME TEST") < current.index("EX-POST DESCRIPTION"),
        True,
    )
    report.same("verdict line refers to real time", "Verdict (real time)" in current, True)


def main(argv: Sequence[str] | None = None) -> int:
    """Check the recession-regime test's rerun against the findings on its first run.

    1. Window definitions: every ALL-MONTHS quarter is an ANY-OVERLAP quarter, and the counts
       are 34 and 23.
    2. The any-overlap (first-run) ex-post results are preserved exactly in the rerun's output
       for the series the first run used.
    3. Dollar definitions are kept apart: goods-only changes exist only for windows ending by
       December 2019, goods-and-services changes only for windows starting from January 2006;
       the first run's splice is reported separately.
    4. Real-time and ex-post blocks are separate and labelled; the decision rule is applied to
       the real-time block.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the outputs
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    report = CheckReport()
    check_panel(report, RegimePanel.read(root / FOLDER.results / "regime_quarters.csv"))
    check_results(report, (root / FOLDER.results / "regime_recession_results.txt").read_text())
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
