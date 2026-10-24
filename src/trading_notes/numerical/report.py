"""Per-check reporting shared by the numerical checks."""

import sys
from typing import Final, Protocol

# Display names of the libraries whose versions a check prints.
DISPLAY_NAMES: Final = {
    "numpy": "NumPy",
    "pandas": "pandas",
    "scipy": "SciPy",
    "statsmodels": "statsmodels",
}


class Versioned(Protocol):
    """A library module with a version, as NumPy, SciPy and statsmodels are."""

    __name__: str
    __version__: str


def print_versions(*libraries: Versioned) -> None:
    """Print the Python version, then each library's display name and version, on one line.

    Args:
        libraries: Library modules, each a key of DISPLAY_NAMES.
    """
    names = [f"{DISPLAY_NAMES[m.__name__]} {m.__version__}" for m in libraries]
    print(", ".join([f"Python {sys.version.split()[0]}", *names]))


class CheckReport:
    """One run's check results: each check is printed as it runs, and failures are kept.

    One check is one `ok` call, so a call inside a loop counts once per iteration. The
    report never ends the process; `summarise` turns the failures into an exit status. Use a
    new report for each run.
    """

    def __init__(self) -> None:
        """Start a run with no checks and no failures."""
        self._failures: list[str] = []
        self._count = 0

    @property
    def count(self) -> int:
        """Return the number of checks run so far, passed or failed."""
        return self._count

    @property
    def failures(self) -> list[str]:
        """Return the names of the failed checks in the order they ran, as a new list."""
        return list(self._failures)

    def ok(self, name: str, cond: bool, detail: str = "") -> None:
        """Print one check line, `  ok <name>` or `  BAD <name>`, and record a failure.

        Args:
            name: What the check asserts.
            cond: Whether it holds.
            detail: Computed value printed after the name as `: <detail>`; omitted when empty.
        """
        print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
        self._count += 1
        if not cond:
            self._failures.append(name)

    def same[T](self, name: str, got: T, want: T) -> None:
        """Check `got == want` and print `  ok  <name>: <got> (want <want>)`, or the BAD line.

        Args:
            name: What the check asserts.
            got: The computed value, printed with `str`.
            want: The expected value, printed with `str`.
        """
        self.ok(name, got == want, f"{got} (want {want})")

    def summarise(self) -> int:
        """Print `FAILED: <names>` or `all checks passed` and return the exit status.

        Returns:
            0 when every check passed, otherwise 1.
        """
        if self._failures:
            print("FAILED: " + ", ".join(self._failures))
            return 1
        print("all checks passed")
        return 0
