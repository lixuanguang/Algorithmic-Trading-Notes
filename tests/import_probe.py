"""Observe what importing package modules does, in a separate isolated process."""

# standard library imports
import json
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

# Imports the preloaded modules (argv[3]) first, so that their own start-up is not observed;
# then, with a stray argument and an audit hook that records every file opened other than
# Python sources, imports the modules (argv[1]). It reports the output, which watched modules
# (argv[2]) were loaded and whether the import left the shared random states as it found
# them: Python's, including its cached Gaussian, and NumPy's legacy one when NumPy was
# preloaded (its state is seeded from entropy when NumPy is first imported, so it can only be
# compared from then on).
PROBE = """
import contextlib, io, json, random, sys
for name in json.loads(sys.argv[3]):
    __import__(name)
numpy = sys.modules.get("numpy")
def random_states():
    if numpy is None:
        return random.getstate(), None
    kind, key, *rest = numpy.random.get_state(legacy=True)
    return random.getstate(), (kind, key.tobytes(), *rest)
before = random_states()
opened = []
sys.addaudithook(lambda event, args: opened.append(str(args[0])) if event == "open" else None)
out = io.StringIO()
with contextlib.redirect_stdout(out):
    for name in json.loads(sys.argv[1]):
        __import__(name)
unchanged = random_states() == before
loaded = sorted(name for name in json.loads(sys.argv[2]) if name in sys.modules)
data = [path for path in opened if not path.endswith((".py", ".pyc"))]
print(json.dumps({"opened": data, "printed": out.getvalue(), "loaded": loaded,
                  "random_unchanged": unchanged}))
"""
HEAVY = ("numpy", "pandas", "scipy", "statsmodels", "openpyxl", "xlrd")


@dataclass(frozen=True)
class ImportEffects:
    """What importing some modules did.

    Attributes:
        opened: Non-Python files opened.
        printed: Text written to stdout.
        loaded: Watched modules that ended up imported.
        stderr: The process's stderr.
        returncode: The process's exit status.
        random_unchanged: Whether the shared random states were left as they were found.
    """

    opened: list[str]
    printed: str
    loaded: list[str]
    stderr: str
    returncode: int
    random_unchanged: bool


def import_effects(
    modules: Sequence[str], watched: Sequence[str], cwd: Path, preload: Sequence[str] = ()
) -> ImportEffects:
    """Import modules in a fresh `python -I` process run from cwd, and report the effects.

    Args:
        modules: Modules to import, in order.
        watched: Modules whose loading should be reported; a preloaded one is always loaded.
        cwd: Working directory of the process; it should be empty and unrelated.
        preload: Modules imported first, unobserved; preload NumPy to compare its random state.
    """
    done = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            PROBE,
            json.dumps(list(modules)),
            json.dumps(list(watched)),
            json.dumps(list(preload)),
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    result: object = json.loads(done.stdout) if done.returncode == 0 else {}
    assert isinstance(result, dict)
    opened, printed, loaded, unchanged = (
        result.get("opened", []),
        result.get("printed", ""),
        result.get("loaded", []),
        result.get("random_unchanged", False),
    )
    assert isinstance(opened, list) and isinstance(printed, str) and isinstance(loaded, list)
    assert isinstance(unchanged, bool)
    return ImportEffects(
        [str(p) for p in opened],
        printed,
        [str(m) for m in loaded],
        done.stderr,
        done.returncode,
        unchanged,
    )
