"""The command-line paths of every research workflow: the repository root and an output folder."""

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Self

from trading_notes.data_folders import DataFolder
from trading_notes.records import Record


class WorkflowArguments(Record):
    """A workflow's command-line arguments, validated after argparse has read them.

    Subclasses name their subsection's data folder and add their own inputs as fields; an
    argument added to the parser is a field of the same name.

    Attributes:
        root: The repository root, which holds the data folders below src/data.
        output: Where to write every file instead; None writes rebuilt extracts to the local
            run's inputs folder and results to its results folder.
    """

    folder: ClassVar[DataFolder]
    root: Path
    output: Path | None = None

    @property
    def retained_inputs(self) -> Path:
        """Return the subsection's retained inputs folder below the root."""
        return self.root / self.folder.inputs

    @property
    def retained_results(self) -> Path:
        """Return the subsection's retained results folder below the root."""
        return self.root / self.folder.results

    @property
    def output_folder(self) -> Path:
        """Return the folder new results are written to, creating it if needed."""
        return self.writable(self.folder.run_results)

    @property
    def extract_folder(self) -> Path:
        """Return the folder rebuilt extracts are written to, creating it if needed."""
        return self.writable(self.folder.run_inputs)

    def writable(self, run_folder: Path) -> Path:
        """Return --output, or the run folder below the root, after creating it."""
        folder = self.output or self.root / run_folder
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def upstream(self, requested: Path | None, retained: Path) -> Path:
        """Return the file another workflow wrote that this one reads.

        Args:
            requested: A generated file, or a folder holding one under the retained file's
                name, such as a run's results folder; None reads the retained file.
            retained: The retained file, relative to the root.

        Raises:
            FileNotFoundError: If the requested file does not exist; the retained file is
                never read in its place.
        """
        if requested is None:
            return self.root / retained
        path = requested / retained.name if requested.is_dir() else requested
        if not path.is_file():
            raise FileNotFoundError(f"requested input not found: {path}")
        return path

    @classmethod
    def parser(cls, description: str) -> argparse.ArgumentParser:
        """Return a parser with the --root and --output options; add the inputs to it."""
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            "--root",
            type=Path,
            default=Path.cwd(),
            help="repository root, which holds src/data (default: the working directory)",
        )
        parser.add_argument(
            "--output",
            type=Path,
            default=None,
            help=(
                "folder for every file written (default: results to"
                f" ROOT/{cls.folder.run_results}, rebuilt extracts to ROOT/{cls.folder.run_inputs})"
            ),
        )
        return parser

    @classmethod
    def parse(cls, parser: argparse.ArgumentParser, argv: Sequence[str] | None) -> Self:
        """Parse argv (None reads sys.argv) and validate it, with every path made absolute."""
        values = {
            name: value.resolve() if isinstance(value, Path) else value
            for name, value in vars(parser.parse_args(argv)).items()
        }
        return cls.model_validate(values)
