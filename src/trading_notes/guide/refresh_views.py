"""Generate the learning guide's TeX source, HTML notes and recency export from its sources."""

import argparse
import datetime as dt
import functools
import html
import json
import re
import sys
import textwrap
from collections.abc import Sequence
from importlib import resources
from pathlib import Path
from typing import Final

from trading_notes.guide.catalogue import CATALOGUE, AuxDestinations, Catalogue, CatalogueError
from trading_notes.guide.charts import overview_chart, section_chart, section_dag_label
from trading_notes.guide.routes import (
    ROMAN,
    LearningRoutes,
    Overview,
    Part,
    RouteError,
    RouteIndex,
    Specialist,
)
from trading_notes.guide.tex_text import TexError, and_list, tex_escape, to_html, unlinked, web_url

GUIDE: Final = "institutional_quantitative_finance_learning_guide"
NOTES: Final = "catalogue_extended_notes.html"
RECENCY: Final = "catalogue_recency.json"
ROUTES: Final = "learning_routes.json"
PART_WORDS: Final = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
]
RECENCY_FIELDS: Final = [
    "Publication / issue date",
    "Selected version / revision",
    "Last verification",
    "Evidence inspected",
    "Version relationship / superseding source",
    "Review policy",
]
RECENCY_KEYS: Final = [
    "publication",
    "version",
    "last_verified",
    "evidence",
    "supersession",
    "review_policy",
]


def display(date: dt.date) -> str:
    """Return a date as the guide prints it, such as 22 October 2026."""
    return f"{date.day} {date.strftime('%B %Y')}"


@functools.cache
def template(name: str, final_newline: bool = True) -> str:
    """Return a verbatim TeX or HTML template of the guide, read from the package.

    The files end with a newline; final_newline=False drops it, for text that has none.
    """
    text = (resources.files("trading_notes.guide") / "templates" / name).read_text()
    return text if final_newline else text.removesuffix("\n")


class GuideViews:
    """The guide, notes and export built from one catalogue and route file.

    Raises:
        RouteError: From the constructor, if the route file breaks a rule or cites a reading
            or branch the catalogue lacks.
    """

    def __init__(self, catalogue: Catalogue, routes: LearningRoutes, aux: AuxDestinations) -> None:
        """Check the routes against the catalogue and hold everything the views need."""
        self.catalogue = catalogue
        self.data = routes
        self.index = RouteIndex(routes)
        self.aux = aux
        self.html_links = routes.catalogue_link_target == "html"
        declared = catalogue.declared_labels()
        for r in self.index.routes.values():
            if not r.required_readings:
                raise RouteError(r.name)
            if len({rd.anchor for rd in r.required_readings}) != len(r.required_readings):
                raise RouteError(r.name)
            for reading in r.required_readings:
                if reading.anchor not in catalogue.by_anchor:
                    raise RouteError(reading)
            for b in r.optional_branches:
                if b.target not in declared and b.target not in catalogue.by_anchor:
                    raise RouteError(b)
        self.summary = (
            f"{len(routes.routes)} overview routes and {len(routes.specialist_routes)} specialist"
            " pathways"
        )
        parts = self.index.parts
        self.dag_sections = [
            r.id
            for part in parts
            for r in (self.index.overviews[i] for i in part.routes)
            if len(r.specialist_order) >= 2
        ]

    @property
    def catalogue_target(self) -> str:
        """Return the file the guide's reading links open."""
        return NOTES if self.html_links else CATALOGUE + ".pdf"

    def preamble(self) -> str:
        """Return the guide's preamble: the catalogue's, adapted, and the guide's additions."""
        source = self.catalogue.source
        preamble = source[: source.index("\\begin{document}")]
        # Retain the catalogue's 9pt body size for compact guide reading lists.
        preamble = preamble.replace("extreport", "extarticle")
        preamble = preamble.replace(r"\fontsize{7}{8}", r"\fontsize{6.3}{7.2}")
        # Report-only chapter settings and catalogue entry declarations are unnecessary.
        preamble = preamble[: preamble.index("\\titleformat{\\chapter}")]
        preamble = preamble.replace(
            "Institutional Quantitative Finance Reference Catalogue",
            "Institutional Quantitative Finance Learning Guide",
        )
        preamble = preamble.replace(
            "Four-part institutional quantitative research reference catalogue", self.summary
        )
        return preamble + template("guide-preamble.tex")

    def study_method(self) -> str:
        """Return the title page, study method and route introduction, placeholders filled."""
        index, parts = self.index, self.index.parts
        dag_index = (
            "; ".join(
                "\\hyperref["
                + section_dag_label(i)
                + "]{"
                + tex_escape(index.overviews[i].name)
                + "}"
                for i in self.dag_sections
            )
            + "."
        )
        section_keys = ", ".join(k for part in parts for k in part.routes)
        section_key_list = (
            textwrap.fill(
                section_keys,
                width=88,
                initial_indent="\\qfsections{",
                subsequent_indent="  ",
                break_on_hyphens=False,
                break_long_words=False,
            )
            + "}"
        )
        text = template("study-method.tex").replace("SECTION_KEY_LIST", section_key_list)
        wasserman = [
            r.id
            for r in self.data.routes
            if any(rd.anchor == "prob-wasserman" for rd in r.required_readings)
        ]
        if not wasserman:
            raise RouteError("The study method cites Wasserman as an overview reading")
        digital = [
            i for i, p in enumerate(parts) if "digital-assets-prediction-markets" in p.routes
        ]
        text = (
            text.replace("WASSERMAN_ROUTE", index.link(wasserman[0]))
            .replace("DIGITAL_PART", ROMAN[digital[0]])
            .replace("FIRST_SECTION", index.link(parts[0].routes[0]))
        )
        text = (
            text.replace("SECTION_DAG_INDEX", dag_index)
            .replace("ROUTE_SUMMARY", tex_escape(self.summary))
            .replace("EDITION_DATE", display(self.data.as_of))
            .replace("PATHWAY_DATE", display(self.data.pathway_updated_on))
            .replace("PART_COUNT_CAP", PART_WORDS[len(parts)].capitalize())
            .replace("PART_COUNT", PART_WORDS[len(parts)])
        )
        if self.html_links:
            old_intro = text.index("Reading titles link to")
            end_intro = text.index("\n\nResearch or preliminary", old_intro)
            links = template("reading-links.tex", final_newline=False)
            text = text[:old_intro] + links + text[end_intro:]
        return text

    def part(self, part: Part) -> str:
        """Return a part's heading, introduction, retired-overview bridges and section list."""
        index = self.index
        out = [
            "\\clearpage\n\\part{"
            + tex_escape(part.title)
            + "}\\label{part-"
            + part.id
            + "}\n"
            + index.prose(part.introduction)
            + "\n\n"
        ]
        for old in self.data.retired_overviews:
            if old.successors[0] in part.routes:
                # A navigation bridge, not a section: earlier links to the retired overview
                # land here.
                numeral = index.numeral(part.id)
                labels = ["route-" + old.id] + ([old.legacy_label] if old.legacy_label else [])
                bridge_labels = "".join(
                    "\\BridgeLabel{"
                    + label
                    + "}{"
                    + numeral
                    + "}{"
                    + tex_escape(old.name)
                    + " (former section)}"
                    for label in labels
                )
                successors = and_list(
                    [index.link(k) + " (" + index.number_link(k) + ")" for k in old.successors]
                )
                out.append(
                    "\\par\\phantomsection"
                    + bridge_labels
                    + "\\textbf{Former section.} "
                    + tex_escape(old.name)
                    + " (key \\texttt{"
                    + old.id
                    + "}) is now divided into "
                    + successors
                    + ". "
                    + index.prose(old.note)
                    + "\n\n"
                )
        out.append("\\textbf{Sections in learning order}\\begin{enumerate}\n")
        for identifier in part.routes:
            route = index.overviews[identifier]
            out.append(
                "\\item[\\ref*{route-"
                + identifier
                + "}.] "
                + index.link(identifier)
                + " --- "
                + index.prose(route.learning_note)
                + "\n"
            )
        out.append(
            "\\end{enumerate}\n\\hyperref[learning-map]{Return to the learning pathway DAG.}\n"
        )
        return "".join(out)

    def route(self, r: Overview | Specialist) -> str:
        """Return a section or subsection: goals, outcome, readings, checkpoint and navigation."""
        index, by_anchor = self.index, self.catalogue.by_anchor
        pages = {} if self.html_links else self.aux.pages
        is_overview = isinstance(r, Overview)
        heading = "section" if is_overview else "subsection"
        out = [
            ("\\clearpage" if is_overview else "\\Needspace{12\\baselineskip}")
            + "\n\\"
            + heading
            + "{"
            + tex_escape(r.name)
            + "}\\label{"
            + r.label
            + "}\n"
        ]
        if isinstance(r, Overview):
            if r.legacy_label is not None:
                out.append("\\label{" + r.legacy_label + "}\n")
            out.append("\\textbf{Learning sequence.} " + index.prose(r.learning_note) + "\n\n")
            out.append(
                "\\textbf{Section goals.} Across its pathways, this section teaches you to:\n"
                "\\begin{itemize}[leftmargin=1.4em,itemsep=0pt,topsep=1pt]\n"
            )
            for g in r.section_goals:
                pathways = ", ".join(index.number_link(p) for p in g.pathways)
                out.append("\\item " + index.prose(g.goal) + " (" + pathways + ")\n")
            out.append("\\end{itemize}\n")
        else:
            out.append(
                "\\textbf{Specialist pathway.} In " + index.link(index.placement[r.id]) + ".\n\n"
            )
        out.append(
            "\\textbf{"
            + ("Overview outcome" if is_overview else "Outcome")
            + ".} "
            + index.prose(r.outcome)
            + "\n\n\\textbf{Prerequisites.} "
            + index.prose(r.prerequisites)
            + "\n\n"
        )
        if r.prerequisite_routes:
            out.append(
                "\\textbf{Review first.} "
                + "; ".join(index.link(identifier) for identifier in r.prerequisite_routes)
                + ".\n\n"
            )
        out.append("\\textbf{Required readings, in order}\n\\begin{enumerate}\\raggedright\n")
        for rd in r.required_readings:
            rec = by_anchor[rd.anchor]
            a = rec[0]
            page = pages.get(a)
            out.append(
                "\\Needspace{5\\baselineskip}\\item \\href{"
                + self.catalogue_target
                + "\\#"
                + a
                + "}{"
                + unlinked(rec[1])
                + "}"
            )
            if page:
                out.append("\\CataloguePage{" + str(page) + "}")
            out.append("\\NoteKey{" + a + "}")
            if rd.selection:
                out.append("\\par\\emph{Selection:} " + index.prose(rd.selection))
            stage = "\\textbf{" + tex_escape(rd.stage) + ".} " if rd.stage else ""
            out.append("\\par " + stage + index.prose(rd.reason) + "\n")
        capstone = r.checkpoint_after if isinstance(r, Overview) else []
        checkpoint = "Checkpoint" + (
            ", a section capstone: complete it after "
            + and_list([index.number_link(p) for p in capstone])
            if capstone
            else ""
        )
        out.append(
            "\\end{enumerate}\n\\Needspace{5\\baselineskip}\\textbf{"
            + checkpoint
            + ".} "
            + index.prose(r.checkpoint)
            + "\n\n"
        )
        branches = []
        for b in r.optional_branches:
            a = b.target
            dest = a if self.html_links else self.aux.labels.get(a, a)
            if a in by_anchor:
                dest = by_anchor[a][0]
            page = pages.get(dest)
            branch = (
                "\\href{"
                + self.catalogue_target
                + "\\#"
                + dest
                + "}{"
                + index.prose(b.reason, linked=False)
                + "}"
            )
            if page:
                branch += "\\BranchPage{" + str(page) + "}"
            branches.append(branch)
        if branches:
            out.append("\\textbf{Optional branches.} " + " ".join(branches) + "\n")
        if isinstance(r, Overview) and r.specialist_order:
            out.append(
                "\\par\\textbf{Continue in this section.} "
                + "; ".join(index.link(s) for s in r.specialist_order)
                + ".\n"
            )
        elsewhere = [
            s
            for s in self.data.specialist_routes
            if s.parent_route == r.name and index.placement[s.id] != r.id
        ]
        if elsewhere:
            homes = [
                p.id
                for p in index.parts
                if p.id in {index.part_of[index.placement[s.id]] for s in elsewhere}
            ]
            out.append(
                "\\par\\textbf{Applications in "
                + ("Part " if len(homes) == 1 else "Parts ")
                + and_list([index.prose("[[part:" + h + "]]") for h in homes])
                + ".} "
                + "; ".join(
                    index.link(s.id) + " (" + index.number_link(s.id) + ")" for s in elsewhere
                )
                + ".\n"
            )
        out.append("\\par{\\small \\hyperref[learning-map]{Learning pathway DAG}")
        if not is_overview:
            out.append(" \\textbar{} " + index.link(index.placement[r.id], "Section overview"))
        section_id = r.id if is_overview else index.placement[r.id]
        if section_id in self.dag_sections:
            out.append(
                " \\textbar{} \\hyperref[" + section_dag_label(section_id) + "]{Section DAG}"
            )
        out.append("\\NoteKey{" + r.id + "}}\n")
        if is_overview and r.id in self.dag_sections:
            out.append(section_chart(index, r.id))
        return "".join(out)

    def guide(self) -> str:
        """Return the guide's TeX source."""
        index = self.index
        out = [
            "% Generated by refresh_views.py. Edit learning_routes.json and canonical catalogue,"
            " then refresh.\n",
            self.preamble(),
            self.study_method(),
            overview_chart(index),
        ]
        for part in index.parts:
            out.append(self.part(part))
            for identifier in part.routes:
                r = index.overviews[identifier]
                out.append(self.route(r))
                out.extend(self.route(index.routes[sid]) for sid in r.specialist_order)
        out.append("\\end{document}\n")
        return "".join(out)

    def notes(self) -> str:
        """Return the HTML page of extended notes and version records, with its search box."""
        cat = self.catalogue
        source, records, notes, recency, by_anchor = (
            cat.source,
            cat.records,
            cat.notes,
            cat.recency,
            cat.by_anchor,
        )
        note_titles = {r[0]: r[1] for r in records}
        subject_titles: dict[str, str] = {}
        # Subject notes are local to the immediately preceding canonical heading.
        current = ""
        for line in source.splitlines():
            m = re.match(r"\\section\{(.+?)\}", line)
            if m:
                current = m[1]
            m = re.match(r"\\ExtendedNote\{(subject-[^}]+)\}", line)
            if m:
                subject_titles[m[1]] = current
        head = template("notes-head.html", final_newline=False).replace(
            "EDITION_DATE", display(self.data.as_of)
        )
        notes_by_id = {n[0]: n[1] for n in notes}
        # Current HTML destinations must not depend on an older saved PDF or aux. Section
        # labels land at their first following entry; citation aliases land at their owning
        # entry. Numbered sources are exported below.
        aliases: dict[str, list[str]] = {r[0]: [] for r in records}
        pending: list[str] = []
        for line in source[source.index("\\begin{document}") :].splitlines():
            pending.extend(re.findall(r"\\label\{([^}]+)\}", line))
            m = re.match(r"\\CatalogueEntry\{([^}]+)\}", line)
            if m:
                a = m[1]
                aliases[a].extend(pending)
                pending = []
                aliases[a].extend(re.findall(r"\\hypertarget\{([^}]+)\}", by_anchor[a][1]))
        if self.html_links:
            head = (
                head.replace("Companion PDFs:", "Earlier saved PDF snapshots:")
                .replace(
                    "Keep these PDFs and this HTML companion together.",
                    "Use this HTML and the current source preview for the latest additions.",
                )
                .replace(">Reference catalogue</a>", ">Saved catalogue PDF snapshot</a>")
                .replace(">Learning guide</a>", ">Saved guide PDF snapshot</a>")
                .replace(
                    '<label for="search">',
                    '<p class="meta">Current source and editor preview include later gap-closure'
                    " edits. The saved PDFs above have not been re-exported.</p>\n"
                    '<label for="search">',
                )
            )
        document = [head]
        display_notes = [(r[0], notes_by_id.get(r[0], r[5])) for r in records]
        display_notes += [(n[0], n[1]) for n in notes if n[0] not in by_anchor]
        for a, body in display_notes:
            title = note_titles.get(a, subject_titles.get(a, "Subject context"))
            document.extend(
                '<span id="' + html.escape(alias, quote=True) + '"></span>'
                for alias in aliases.get(a, [])
                if alias != a
            )
            document.append(
                '<article id="' + html.escape(a, quote=True) + '"><h2>' + to_html(title) + "</h2>"
            )
            if a in by_anchor:
                rec = by_anchor[a]
                document.append(
                    '<p class="meta">Difficulty: '
                    + to_html(rec[2])
                    + " · Type: "
                    + to_html(rec[3])
                    + "<br>Status/version: "
                    + to_html(rec[4])
                    + "</p>"
                )
                if not self.html_links:
                    document.append(
                        '<a href="'
                        + CATALOGUE
                        + ".pdf#nameddest="
                        + a
                        + '">Canonical catalogue entry</a>'
                    )
            document.append("<p>" + to_html(body) + "</p></article>")
            if a in recency:
                metadata = "<details><summary>Version and verification record</summary><dl>"
                metadata += "".join(
                    "<dt><strong>" + name + "</strong></dt><dd>" + to_html(value) + "</dd>"
                    for name, value in zip(RECENCY_FIELDS, recency[a], strict=False)
                )
                metadata += "</dl></details>"
                document[-1] = document[-1].replace("</article>", metadata + "</article>")
        document.append("<h2>Numbered source-link directory</h2>")
        for source_id, url in re.findall(
            r"^\\item\\hypertarget\{(source-\d+)\}\{\}\s*\\url\{([^}]+)\}", source, re.M
        ):
            escaped = html.escape(web_url(url), quote=True)
            document.append(
                '<p id="'
                + source_id
                + '"><a href="'
                + escaped
                + '">'
                + source_id
                + ": "
                + escaped
                + "</a></p>"
            )
        document.append(template("notes-script.html", final_newline=False))
        return "\n".join(document)

    def recency(self) -> str:
        """Return the JSON export of every entry's version record, with derived provenance."""
        cat = self.catalogue
        exported: dict[str, dict[str, str | list[str] | None]] = {}
        for a, values in cat.recency.items():
            record: dict[str, str | list[str] | None] = {
                k: html.unescape(re.sub(r"<[^>]*>", "", to_html(v)))
                for k, v in zip(RECENCY_KEYS, values, strict=False)
            }
            verified = str(record["last_verified"])
            match = re.match(r"^\d{4}-\d{2}-\d{2}", verified)
            record["verified_on"] = match[0] if match else None
            record["verification_provenance"] = (
                "new-source-inspection"
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", verified)
                else ("inherited-evidence" if match else "not-established")
            )
            notes_by_id = {n[0]: n[1] for n in cat.notes}
            record["source_urls"] = list(
                dict.fromkeys(
                    web_url(u)
                    for u in re.findall(
                        r"\\(?:href|url)\{(https?://[^}]+)\}",
                        " ".join(cat.by_anchor[a]) + notes_by_id.get(a, ""),
                    )
                )
            )
            record["evidence_links"] = list(
                dict.fromkeys(
                    web_url(u) for u in re.findall(r"\\(?:href|url)\{([^}]+)\}", " ".join(values))
                )
            )
            exported[a] = record
        return (
            json.dumps(
                {
                    "schema_version": 1,
                    "source": CATALOGUE + ".tex",
                    "as_of": self.data.as_of.isoformat(),
                    "entries": exported,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )

    def report(self) -> str:
        """Return the summary line printed after a refresh."""
        readings = sum(len(r.required_readings) for r in self.index.routes.values())
        return (
            f"Refreshed {self.summary}, {readings} selected readings, {len(self.catalogue.notes)}"
            f" extended notes and {len(self.catalogue.recency)} recency records."
        )


def main(argv: Sequence[str] | None = None) -> int:
    """Refresh the guide's TeX source, HTML notes and recency export; exit 1 on invalid input.

    Reads the catalogue source, its .aux file (for PDF page fallbacks) and learning_routes.json
    from the guide folder, validates that every reading exists and every prerequisite comes
    first, and writes the three generated files to the output folder. The generator comes from
    the institutional_reading_list repository (refresh_views.py of commit 8302467) and
    needs no TeX run, bibliography engine or network.

    Returns:
        0, or 1 when the catalogue or route file is invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root (default: the working directory)",
    )
    parser.add_argument(
        "--guide", type=Path, default=None, help="guide folder (default: ROOT/guide)"
    )
    parser.add_argument(
        "--output", type=Path, default=None, help="output folder (default: the guide folder)"
    )
    args = parser.parse_args(argv)
    root: Path = (args.guide or args.root / "guide").resolve()
    output: Path = (args.output or root).resolve()
    try:
        views = GuideViews(
            Catalogue.read(root), LearningRoutes.read(root / ROUTES), AuxDestinations.read(root)
        )
        guide, notes, recency = views.guide(), views.notes(), views.recency()
    except (TexError, CatalogueError, RouteError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    output.mkdir(parents=True, exist_ok=True)
    (output / (GUIDE + ".tex")).write_text(guide)
    (output / NOTES).write_text(notes)
    (output / RECENCY).write_text(recency)
    print(views.report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
