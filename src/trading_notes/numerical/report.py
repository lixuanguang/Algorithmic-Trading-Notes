"""Per-check reporting for the numerical evidence scripts."""


class CheckReport:
    """One run's check results: each check is printed as it runs, and failures are kept.

    One check is one `ok` call, so a call inside a loop counts once per iteration. The
    report never ends the process; the caller turns `failures` into an exit status. Use a
    new report for each run.
    """

    def __init__(self) -> None:
        """Start a run with no failures."""
        self._failures: list[str] = []

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
