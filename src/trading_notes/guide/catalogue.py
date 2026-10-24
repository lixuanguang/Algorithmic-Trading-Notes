"""The reading-list catalogue: its entries, extended notes, version records and PDF destinations."""

import re
from pathlib import Path
from typing import Final, Self

from trading_notes.guide.tex_text import TexError, argument, check_one_line_commands, commands
from trading_notes.records import Record

CATALOGUE: Final = "institutional_quantitative_finance_reading_list"


class CatalogueError(ValueError):
    """The catalogue's entries and records do not correspond one to one."""


class Catalogue(Record):
    r"""The catalogue source and the records the guide and notes are built from.

    Attributes:
        source: The catalogue's TeX source.
        records: Each \CatalogueEntry's seven arguments, the key first and the title second.
        notes: Each \ExtendedNote's key and text.
        recency: Each entry's six version-record fields, by key.
        by_anchor: The entry of each key and of each alias declared in an entry's title.
    """

    source: str
    records: list[list[str]]
    notes: list[list[str]]
    recency: dict[str, list[str]]
    by_anchor: dict[str, list[str]]

    @classmethod
    def read(cls, root: Path) -> Self:
        """Read the catalogue source in a guide folder and check its one-line commands.

        Raises:
            TexError: If a command spans lines.
            CatalogueError: If keys repeat or an entry lacks its one version record.
        """
        source = (root / (CATALOGUE + ".tex")).read_text()
        check_one_line_commands(source)
        records = commands(source, "CatalogueEntry", 7)
        notes = commands(source, "ExtendedNote", 2)
        recency_rows = commands(source, "EntryRecency", 7)
        recency = {r[0]: r[1:] for r in recency_rows}
        by_anchor = {r[0]: r for r in records}
        if len(by_anchor) != len(records):
            raise CatalogueError("Duplicate catalogue identifiers")
        if len(recency) != len(recency_rows):
            raise CatalogueError("Duplicate recency identifiers")
        if set(recency) != set(by_anchor):
            raise CatalogueError("Every catalogue entry needs one recency record")
        for r in records:
            for alias in re.findall(r"\\hypertarget\{([^}]+)\}", r[1]):
                by_anchor[alias] = r
        return cls(
            source=source, records=records, notes=notes, recency=recency, by_anchor=by_anchor
        )

    def declared_labels(self) -> set[str]:
        r"""Return every \label the catalogue declares."""
        return set(re.findall(r"\\label\{([^}]+)\}", self.source))


class AuxDestinations(Record):
    """Named destinations and page numbers from the catalogue's TeX auxiliary file.

    Attributes:
        labels: The named destination of each label.
        pages: The page of each entry key and of each other destination.
    """

    labels: dict[str, str]
    pages: dict[str, int]

    @classmethod
    def read(cls, root: Path) -> Self:
        """Read the .aux file beside the catalogue; empty when the catalogue is not compiled."""
        p = root / (CATALOGUE + ".aux")
        if not p.exists():
            return cls(labels={}, pages={})
        text = p.read_text()
        labels = {
            m[1]: m[2]
            for m in re.finditer(
                r"\\newlabel\{([^}]+)\}\{\{[^}]*\}\{[^}]*\}\{.*?\}\{([^}]+)\}", text
            )
        }
        pages: dict[str, int] = {}
        for line in text.splitlines():
            if not line.startswith("\\newlabel{"):
                continue
            label, j = argument(line, len("\\newlabel"))
            fields, j = argument(line, j)
            try:
                _, j = argument(fields, 0)
                page, j = argument(fields, j)
                _, j = argument(fields, j)
                dest, j = argument(fields, j)
            except TexError, IndexError:
                continue
            if not page.isdigit():
                continue
            if label.startswith("entry-"):
                pages[label[len("entry-") :]] = int(page)
            else:
                pages.setdefault(dest, int(page))
        return cls(labels=labels, pages=pages)
