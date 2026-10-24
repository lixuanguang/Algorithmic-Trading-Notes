"""Observe what importing package modules does, in a separate isolated process."""

# standard library imports
import json
import subprocess
import sys
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from pathlib import Path

# Puts the folders of argv[4] first on the module path and imports the preloaded modules
# (argv[3]), so that their own start-up is not observed; then, with a stray argument and an
# audit hook that records every file opened other than Python sources, imports the modules
# (argv[1]). It reports the output, which watched modules (argv[2]) were loaded and whether the
# import left the shared random states as it found them: Python's, including its cached
# Gaussian, and NumPy's legacy one when NumPy was preloaded (its state is seeded from entropy
# when NumPy is first imported, so it can only be compared from then on).
PROBE = """
import contextlib, io, json, random, sys
sys.path[:0] = json.loads(sys.argv[4])
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

    def reads_beyond(self, allowed: Collection[str]) -> list[str]:
        """Return the files opened that are not in allowed, in the order they were opened."""
        return [path for path in self.opened if path not in allowed]


def import_effects(
    modules: Sequence[str],
    watched: Sequence[str],
    cwd: Path,
    preload: Sequence[str] = (),
    path: Sequence[Path] = (),
) -> ImportEffects:
    """Import modules in a fresh `python -I` process run from cwd, and report the effects.

    Args:
        modules: Modules to import, in order.
        watched: Modules whose loading should be reported; a preloaded one is always loaded.
        cwd: Working directory of the process; it should be empty and unrelated.
        preload: Modules imported first, unobserved; preload NumPy to compare its random state.
        path: Folders searched for modules before the isolated interpreter's own path.
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
            json.dumps([str(folder) for folder in path]),
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


def dependency_reads(dependencies: Sequence[str], cwd: Path) -> frozenset[str]:
    """Return the non-Python files that a cold import of the dependencies alone opens.

    A module may open these when importing its dependencies, and nothing else. They are what
    the dependencies read to initialise themselves: SciPy, for one, reads platform,
    interpreter and installed-package metadata (on macOS the system version file, the
    interpreter's zip path and NumPy's install record). Measuring them by importing the same
    dependencies, cold and in the same kind of process, keeps any read by the module itself,
    such as a research data file, outside the allowance.

    Args:
        dependencies: The modules the module imports for its dependencies, as it imports them.
        cwd: Working directory of the process; it should be empty and unrelated.
    """
    effects = import_effects(dependencies, (), cwd)
    assert (effects.returncode, effects.printed, effects.stderr) == (0, "", ""), effects.stderr
    return frozenset(effects.opened)
