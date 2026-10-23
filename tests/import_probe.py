"""Observe what importing package modules does, in a separate isolated process."""

# standard library imports
import json
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

# Imported with a stray argument and an audit hook that records every file opened other
# than Python sources; then reports the output and which watched modules were loaded.
PROBE = """
import contextlib, io, json, sys
opened = []
sys.addaudithook(lambda event, args: opened.append(str(args[0])) if event == "open" else None)
out = io.StringIO()
with contextlib.redirect_stdout(out):
    for name in json.loads(sys.argv[1]):
        __import__(name)
loaded = sorted(name for name in json.loads(sys.argv[2]) if name in sys.modules)
data = [path for path in opened if not path.endswith((".py", ".pyc"))]
print(json.dumps({"opened": data, "printed": out.getvalue(), "loaded": loaded}))
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
    """

    opened: list[str]
    printed: str
    loaded: list[str]
    stderr: str
    returncode: int


def import_effects(modules: Sequence[str], watched: Sequence[str], cwd: Path) -> ImportEffects:
    """Import modules in a fresh `python -I` process run from cwd, and report the effects.

    Args:
        modules: Modules to import, in order.
        watched: Modules whose loading should be reported.
        cwd: Working directory of the process; it should be empty and unrelated.
    """
    done = subprocess.run(
        [sys.executable, "-I", "-c", PROBE, json.dumps(list(modules)), json.dumps(list(watched))],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    result: object = json.loads(done.stdout) if done.returncode == 0 else {}
    assert isinstance(result, dict)
    opened, printed, loaded = (
        result.get("opened", []),
        result.get("printed", ""),
        result.get("loaded", []),
    )
    assert isinstance(opened, list) and isinstance(printed, str) and isinstance(loaded, list)
    return ImportEffects(
        [str(p) for p in opened], printed, [str(m) for m in loaded], done.stderr, done.returncode
    )
