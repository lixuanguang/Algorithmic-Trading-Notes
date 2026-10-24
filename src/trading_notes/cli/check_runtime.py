"""Check that the interpreter is the pinned CPython build, with the GIL, on a supported machine."""

import argparse
import platform
import sys
import sysconfig
from collections.abc import Sequence
from pathlib import Path
from typing import Final, Self

from trading_notes.records import Record

DESCRIPTION = "Check the interpreter against .python-version and the supported platform."
# CI runs on GitHub's ubuntu-latest runners.
SUPPORTED_MACHINE: Final = "x86_64"


class Runtime(Record):
    """The properties of an interpreter that the supported runtime fixes.

    Attributes:
        implementation: The Python implementation, such as "CPython".
        version: The full version, such as "3.14.7".
        gil_enabled: Whether the GIL is enabled in the running process.
        free_threaded_build: Whether the build was configured with Py_GIL_DISABLED.
        machine: The hardware name, such as "x86_64" or "arm64".
    """

    implementation: str
    version: str
    gil_enabled: bool
    free_threaded_build: bool
    machine: str

    @classmethod
    def current(cls) -> Self:
        """Return the running interpreter's properties."""
        return cls(
            implementation=platform.python_implementation(),
            version=platform.python_version(),
            gil_enabled=sys._is_gil_enabled(),
            free_threaded_build=bool(sysconfig.get_config_var("Py_GIL_DISABLED")),
            machine=platform.machine(),
        )

    def problems(self, pinned: str, machine: str) -> list[str]:
        """Return how the runtime differs from CPython `pinned` with the GIL on `machine`."""
        found = []
        if self.implementation != "CPython":
            found.append(f"implementation {self.implementation}, not CPython")
        if self.version != pinned:
            found.append(f"version {self.version}, not the pinned {pinned}")
        if not self.gil_enabled or self.free_threaded_build:
            found.append("a free-threaded build or a disabled GIL")
        if self.machine != machine:
            found.append(f"machine {self.machine}, not {machine}")
        return found


def main(argv: Sequence[str] | None = None) -> int:
    """Print the interpreter and platform; return 1 when the runtime is not the supported one.

    Run from the repository root, or pass --root:
    uv run --frozen --no-editable python -m trading_notes.cli.check_runtime [--root DIR]
        [--machine NAME]
    The pinned version is read from ROOT/.python-version.
    """
    ap = argparse.ArgumentParser(description=DESCRIPTION)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument(
        "--machine",
        default=SUPPORTED_MACHINE,
        help=f"the required hardware name (default: {SUPPORTED_MACHINE})",
    )
    args = ap.parse_args(argv)
    root: Path = args.root
    machine: str = args.machine
    print(sys.version, platform.platform(), platform.machine())
    pinned = (root / ".python-version").read_text().strip()
    found = Runtime.current().problems(pinned, machine)
    for problem in found:
        print(f"{ap.prog}: unsupported runtime: {problem}", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
