"""The command-line paths of every research workflow: the repository root and an output folder."""

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, Self

from trading_notes.records import Record

ARTEFACTS = Path("notes") / "artefacts"


class WorkflowArguments(Record):
    """A workflow's command-line arguments, validated after argparse has read them.

    Subclasses name their artefact folder and add their own inputs as fields; an argument
    added to the parser is a field of the same name.

    Attributes:
        root: The repository root, which holds the retained inputs and outputs.
        output: Where to write the outputs; None writes them to the artefact folder.
    """

    folder: ClassVar[str]
    root: Path
    output: Path | None = None

    @property
    def artefacts(self) -> Path:
        """Return the workflow's artefact folder below the root."""
        return self.root / ARTEFACTS / self.folder

    @property
    def output_folder(self) -> Path:
        """Return the folder the outputs are written to, creating it if needed."""
        folder = self.output or self.artefacts
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @classmethod
    def parser(cls, description: str) -> argparse.ArgumentParser:
        """Return a parser with the --root and --output options; add the inputs to it."""
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            "--root",
            type=Path,
            default=Path.cwd(),
            help="repository root (default: the working directory)",
        )
        parser.add_argument(
            "--output",
            type=Path,
            default=None,
            help=f"folder for the outputs (default: ROOT/{ARTEFACTS / cls.folder})",
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
