"""The data folders of the note subsections below ROOT/src/data, outside the installed package."""

from pathlib import Path
from typing import Final

from trading_notes.records import Record

DATA: Final = Path("src") / "data"
LOCAL_RUN: Final = Path("runs") / "local"


class DataFolder(Record):
    """One subsection's data folder, as paths relative to the repository root.

    The retained files are in inputs/ (source extracts and input datasets), results/
    (calculated tables and reports) and protocols/. A local run writes rebuilt extracts to
    runs/local/inputs/ and new results to runs/local/results/, which Git ignores, so a run
    never overwrites a retained file.

    Attributes:
        subsection: The owning subsection's package name, such as "macro_fx".
    """

    subsection: str

    @property
    def inputs(self) -> Path:
        """Return the retained inputs folder."""
        return DATA / self.subsection / "inputs"

    @property
    def results(self) -> Path:
        """Return the retained results folder."""
        return DATA / self.subsection / "results"

    @property
    def run_inputs(self) -> Path:
        """Return the local run's folder for rebuilt extracts."""
        return DATA / self.subsection / LOCAL_RUN / "inputs"

    @property
    def run_results(self) -> Path:
        """Return the local run's folder for new results."""
        return DATA / self.subsection / LOCAL_RUN / "results"
