"""The repository-root option of numerical checks that read compendium or research files."""

import argparse
from collections.abc import Sequence
from pathlib import Path


def repository_root(description: str, argv: Sequence[str] | None = None) -> Path:
    """Parse `--root DIR` and return the resolved repository root.

    Args:
        description: The command's description for `--help`.
        argv: The arguments after the program name; None reads them from sys.argv.

    Returns:
        The given root, or the working directory when none is given.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    root: Path = parser.parse_args(argv).root
    return root.resolve()
