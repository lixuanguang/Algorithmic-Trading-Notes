"""A throwaway repository laid out like this one, shared by the structural-check tests."""

# The guide declares two Parts: part-one with sections sec-a (pathways path-x, path-y) and sec-b
# (path-z), and part-two with sec-c (path-w); old-ab is a retired overview succeeded by sec-a and
# sec-b. The repository starts with section A's wrapper opening path-x over sec-a/topic, which
# each test writes as it needs.

import json
import tempfile
from pathlib import Path
from typing import Final

from trading_notes.structure.json_fields import JsonObject

type Pathway = tuple[str, str, list[str]]

ROUTES: Final[JsonObject] = {
    "learning_parts": [
        {"id": "part-one", "title": "Part one", "routes": ["sec-a", "sec-b"]},
        {"id": "part-two", "title": "Part two", "routes": ["sec-c"]},
    ],
    "routes": [
        {"id": "sec-a", "name": "Section A", "specialist_order": ["path-x", "path-y"]},
        {"id": "sec-b", "name": "Section B", "specialist_order": ["path-z"]},
        {"id": "sec-c", "name": "Section C", "specialist_order": ["path-w"]},
    ],
    "specialist_routes": [
        {"id": "path-x", "name": "Path X"},
        {"id": "path-y", "name": "Path Y"},
        {"id": "path-z", "name": "Path Z"},
        {"id": "path-w", "name": "Path W"},
    ],
    "retired_overviews": [{"id": "old-ab", "successors": ["sec-a", "sec-b"]}],
}
MASTER: Final = "\\qfpart{part-one}{Part one}{sec-a, sec-b}\n\\qfpart{part-two}{Part two}{sec-c}\n"

GOOD_ENTRY: Final = r"""\begin{qfmodel}[A model]\label{mod:good}
\qffield{Statement} Claim \citep[p.~3]{cat-key}.
\qffield{Further reading} \citep{src-key}.
\end{qfmodel}
"""


def wrapper(title: str, *pathways: Pathway) -> str:
    """Return a chapter wrapper: its title, then (key, name, [inputs]) for each pathway."""
    text = f"\\chapter{{{title}}}\n"
    for key, name, inputs in pathways:
        text += f"\\qfpathway{{{key}}}{{{name}}}\n" + "".join(f"\\input{{{i}}}\n" for i in inputs)
    return text


A_WRAPPER: Final = wrapper("Section A", ("path-x", "Path X", ["sec-a/topic"]))


class SyntheticRepository:
    """A temporary repository with the guide, citation registries, master and section A.

    Attributes:
        root: The repository root, a fresh temporary directory.
    """

    def __init__(self) -> None:
        """Create the repository files."""
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.write_json("guide/learning_routes.json", ROUTES)
        self.write(
            "guide/institutional_quantitative_finance_reading_list.tex",
            r"\CatalogueEntry{cat-key}{A book}" + "\n",
        )
        self.write(
            "compendium/front/sources.tex",
            r"\qfsource{src-key}{A paper}"
            + "\n"
            + r"\qfsource[https://example.org/x]{linked-key}{A page}"
            + "\n",
        )
        self.write("notes/pathways/.keep", "")
        self.write("notes/pathways/sec-a.md", "")
        self.write("compendium/compendium.tex", MASTER)
        self.write("compendium/sec-a/section.tex", A_WRAPPER)

    def write(self, rel: str, text: str) -> None:
        """Write text to a path relative to the repository root, creating folders."""
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_json(self, rel: str, document: object) -> None:
        """Write a JSON document to a path relative to the repository root."""
        self.write(rel, json.dumps(document))

    def close(self) -> None:
        """Remove the repository."""
        self._tmp.cleanup()
