"""Run one numerical example's entrypoint once, as `python -m` or `python <script>` would."""

import contextlib
import random
import runpy
import sys
from collections.abc import Iterator, Sequence
from typing import Final, Self

import numpy as np
from pydantic import BaseModel, ConfigDict

# The run starts with both shared generators seeded with this and each holding a cached
# Gaussian, unlike a fresh process, so an example that draws from them changes the state.
PRIMING_SEED: Final = 20261023


class GlobalState(BaseModel):
    """The process-wide state that a numerical run must leave as it found it.

    Attributes:
        python_random: The shared `random` generator's state, its cached Gaussian included.
        numpy_random: NumPy's legacy generator as (kind, key bytes, position, has cached
            Gaussian, cached Gaussian).
        printoptions: NumPy's print options, as sorted (name, repr of value) pairs.
        errors: NumPy's floating-point error handling, as sorted (kind, action) pairs.
    """

    model_config = ConfigDict(frozen=True)

    python_random: tuple[int, tuple[int, ...], float | None]
    numpy_random: tuple[str, bytes, int, int, float]
    printoptions: tuple[tuple[str, str], ...]
    errors: tuple[tuple[str, str], ...]

    @classmethod
    def now(cls) -> Self:
        """Return the current state, copied so that later changes cannot reach it."""
        legacy = np.random.get_state(legacy=True)
        assert isinstance(legacy, tuple)
        kind, key, position, has_gauss, gauss = legacy
        return cls(
            python_random=random.getstate(),
            numpy_random=(str(kind), key.tobytes(), int(position), int(has_gauss), float(gauss)),
            printoptions=tuple(sorted((k, repr(v)) for k, v in np.get_printoptions().items())),
            errors=tuple(sorted((k, str(v)) for k, v in np.geterr().items())),
        )


@contextlib.contextmanager
def restored_global_state() -> Iterator[None]:
    """Restore the shared random generators and NumPy's settings afterwards, even on failure."""
    python_random, numpy_random = random.getstate(), np.random.get_state(legacy=True)
    try:
        with np.printoptions(**np.get_printoptions()), np.errstate(**np.geterr()):
            yield
    finally:
        random.setstate(python_random)
        np.random.set_state(numpy_random)


def prime_global_random(seed: int) -> None:
    """Seed both shared generators and leave each holding a cached Gaussian draw."""
    random.seed(seed)
    random.gauss(0, 1)
    np.random.seed(seed)
    np.random.standard_normal()


def run_entrypoint(module: str, script: str, args: Sequence[str]) -> int:
    """Execute the module, or its script, as the main program and return its exit status.

    runpy is what `python -m` and `python <script>` use, so the module's own
    `if __name__ == "__main__"` block runs.

    Raises:
        AssertionError: The program finished without `sys.exit`, or exited with a status that
            is not an integer.
    """
    sys.argv = [script or module, *args]
    try:
        if script:
            runpy.run_path(script, run_name="__main__")
        else:
            runpy.run_module(module, run_name="__main__", alter_sys=True)
    except SystemExit as stop:
        if isinstance(stop.code, int):
            return stop.code
        raise AssertionError(f"{script or module} exited with {stop.code!r}") from None
    raise AssertionError(f"{script or module} returned without calling sys.exit")


def main(argv: Sequence[str]) -> int:
    """Run one example once and return its status; report changed shared state on stderr.

    Args:
        argv: The module name, its forwarding script or "", then the arguments to pass it.
    """
    module, script, *args = argv
    prime_global_random(PRIMING_SEED)
    before = GlobalState.now()
    status = run_entrypoint(module, script, args)
    if GlobalState.now() != before:
        print(f"{module} changed the shared random or NumPy state", file=sys.stderr)
    return status
