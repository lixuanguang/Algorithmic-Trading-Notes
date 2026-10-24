"""The recession-regime test's outputs: window definitions, dollar series and preserved results."""

import hashlib
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from trading_notes.numerical.macro_regimes_data.regime_panel import RegimePanel, add_months
from trading_notes.numerical.report import CheckReport
from trading_notes.numerical.repository import repository_root

# The test's outputs, below the repository root, and the first run kept beside them.
FOLDER: Final = Path("notes/artefacts/macro-regimes-stock-bond")
FIRST_RUN: Final = FOLDER / "superseded-first-run"


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


def check_results(report: CheckReport, first: str, current: str) -> None:
    """Checks 2 and 4: the first run's any-overlap results preserved, real time tested first."""
    v1_block = first.split("== ex-post NBER window")[1]
    v2_block = current.split("ANY OVERLAP (v1 definition)")[1].split(
        "== ex-post NBER window, ALL MONTHS"
    )[0]
    for k in ("dy10", "dcred", "eq", "dfn"):
        a = result_triple(
            rf"{k}\s*: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), t ([+-][0-9.]+)", v1_block
        )
        b = result_triple(
            rf"\n  {k}\s+[0-9-]+: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), Welch t ([+-][0-9.]+)",
            v2_block,
        )
        report.same(f"v1 any-overlap result preserved for {k}", b, a)
    a = result_triple(
        r"usd\s*: regime ([+-][0-9.]+).*diff ([+-][0-9.]+), t ([+-][0-9.]+)", v1_block
    )
    b = result_triple(
        r"usd \(v1 splice[^)]*\)\s+[0-9-]+: regime ([+-][0-9.]+).*diff ([+-][0-9.]+),"
        r" Welch t ([+-][0-9.]+)",
        v2_block,
    )
    report.same("v1 any-overlap dollar (splice) preserved", b, a)
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
    5. The first run's derived panel is preserved byte for byte.

    Args:
        argv: Command-line arguments: `--root DIR`, the repository root that holds the outputs
            (default: the working directory).

    Returns:
        The exit status, 0 or 1.
    """
    root = repository_root(__doc__ or "", argv)
    report = CheckReport()
    check_panel(report, RegimePanel.read(root / FOLDER / "regime_quarters.csv"))
    check_results(
        report,
        (root / FIRST_RUN / "regime_recession_results.txt").read_text(),
        (root / FOLDER / "regime_recession_results.txt").read_text(),
    )
    panel_v1 = (root / FIRST_RUN / "regime_quarters.csv").read_bytes()
    report.same(
        "v1 panel preserved (SHA-256 prefix)", hashlib.sha256(panel_v1).hexdigest()[:8], "82ce2b97"
    )
    if report.failures:
        print("\nFAILED:", report.failures)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
