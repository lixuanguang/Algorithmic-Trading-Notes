"""Forced failures and cheap stand-ins for in-process runs of the numerical examples."""

import contextlib
import io
from collections.abc import Callable, Mapping, Sequence
from types import ModuleType
from typing import Protocol, runtime_checkable
from unittest import mock

from trading_notes.numerical.report import CheckReport


@runtime_checkable
class ValueReport(Protocol):
    """A report whose checks compare a value with the one wanted."""

    def check(self, name: str, got: float, want: float) -> None:
        """Print one check line and record a failure."""


@runtime_checkable
class FailureListChecks(Protocol):
    """A module whose checks print a line and append failures to a list."""

    def check(self, failures: list[str], name: str, cond: bool, detail: str) -> None:
        """Print one check line and record a failure."""


@runtime_checkable
class Example(Protocol):
    """A numerical example module."""

    def main(self, argv: Sequence[str] | None = ...) -> int:
        """Run the example and return its exit status."""


# A forced failure gets the example module and the arguments of the call it follows; it
# records one failed check, or returns one failed condition to add to the call's list.
type Forced = Callable[[ModuleType, tuple[object, ...]], list[str] | None]


def forced_failure(_: ModuleType, args: tuple[object, ...]) -> None:
    """Record one failed check on the CheckReport passed to the call."""
    report = args[0]
    assert isinstance(report, CheckReport)
    report.ok("forced failure", False)


def forced_value_failure(_: ModuleType, args: tuple[object, ...]) -> None:
    """Record one failed check on the value-comparing report passed to the call."""
    report = args[0]
    assert isinstance(report, ValueReport)
    report.check("forced failure", 1.0, 0.0)


def forced_list_failure(module: ModuleType, args: tuple[object, ...]) -> None:
    """Record one failed check, with the module's own `check`, on the list passed to the call."""
    failures = args[0]
    assert isinstance(module, FailureListChecks) and isinstance(failures, list)
    module.check(failures, "forced failure", False, "forced")


def forced_condition_failure(_: ModuleType, __: tuple[object, ...]) -> list[str]:
    """Return one failed condition, to add to those the call returns."""
    return ["forced failure"]


def skipped(*_: object) -> None:
    """Stand in for an expensive check function that returns nothing, running no checks."""


def no_conditions(*_: object) -> list[str]:
    """Stand in for an expensive function that returns its failed conditions: none."""
    return []


def unused_value(*_: object) -> float:
    """Stand in for an expensive check whose value only feeds checks that are stood in for too."""
    return 0.0


class Function(Protocol):
    """A module function, called with any arguments."""

    def __call__(self, *args: object, **kwargs: object) -> object:
        """Call the function."""


def with_forced_failure(module: ModuleType, original: Function, forced: Forced) -> Function:
    """Return original, followed by one forced failure recorded on its arguments."""

    def wrapped(*args: object, **kwargs: object) -> object:
        result = original(*args, **kwargs)
        extra = forced(module, args)
        return [*result, *extra] if isinstance(result, list) and extra is not None else result

    return wrapped


def run_main(
    module: ModuleType,
    args: Sequence[str] = (),
    stand_ins: Mapping[str, object] | None = None,
    failure: tuple[str, Forced] | None = None,
) -> tuple[int, str]:
    """Call the example's `main()` in this process; return its status and its output.

    Args:
        module: The example module.
        args: Command-line arguments for `main`; none means `main()` is called without any.
        stand_ins: Module attributes replaced for the run, such as expensive check functions.
        failure: The function after which one failure is forced, and how it is recorded.
    """
    assert isinstance(module, Example)
    out = io.StringIO()
    with contextlib.ExitStack() as stack:
        for name, value in (stand_ins or {}).items():
            stack.enter_context(mock.patch.object(module, name, value))
        if failure is not None:
            name, forced = failure
            original: Function = getattr(module, name)
            stack.enter_context(
                mock.patch.object(module, name, with_forced_failure(module, original, forced))
            )
        stack.enter_context(contextlib.redirect_stdout(out))
        status = module.main(list(args)) if args else module.main()
    return status, out.getvalue()
