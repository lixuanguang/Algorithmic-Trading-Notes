"""TikZ DAGs of the guide: the whole-guide chart by part and a focused chart per section."""

import itertools
from collections.abc import Sequence
from typing import Final

from trading_notes.guide.routes import ROMAN, Overview, Part, RouteIndex, require
from trading_notes.guide.tex_text import and_list, tex_escape

type Position = tuple[float, float]

COLUMNS: Final = 4
STEP: Final = 4.15


def section_dag_label(identifier: str) -> str:
    """Return the TeX label of an overview's section DAG."""
    return (
        "digital-map" if identifier == "digital-assets-prediction-markets" else "map-" + identifier
    )


def chart_node(
    index: RouteIndex,
    identifier: str,
    x: str,
    y: str | int,
    width: str = "2.85cm",
    style: str = "pathnode",
    show_count: bool = False,
) -> str:
    """Return a clickable node for a route, its box sized to its wrapped title in TeX."""
    r = index.routes[identifier]
    label = r.label
    title = r"\textbf{\ref*{" + label + r"}.} " + tex_escape(r.chart_title)
    if show_count and isinstance(r, Overview):
        title += r"\\[2pt]{\small " + str(len(r.specialist_order)) + " pathways}"
    # Measure the actual wrapped label in TeX; the whole interior stays clickable.
    # Long refreshed titles grow their boxes instead of overflowing a fixed parbox.
    content = r"\MeasurePathNode{" + width + "}{" + title + "}"
    content += (
        r"\hyperref["
        + label
        + r"]{\parbox[c][\pathnodeheight][c]{"
        + width
        + r"}{\centering "
        + title
        + "}}"
    )
    return (
        r"\node["
        + style
        + "] ("
        + identifier
        + ") at ("
        + str(x)
        + ","
        + str(y)
        + ") {"
        + content
        + "};\n"
    )


def overview_chart(index: RouteIndex) -> str:
    """Return the whole-guide DAG: one row per part, or per group in a part's chart_rows.

    A dashed spine from the first foundation section, the shared prerequisite of every
    subject part, feeds each later row. Solid arrows give the recommended study order
    within a row; they are not hard gates. Rows hold at most four sections. Each page
    holds only a heading and the chart, so that the chart is never split from its heading.
    When the parts do not fit one page, whole parts continue on a second page, where the
    spine resumes from the top edge.

    Raises:
        RouteError: If a part's chart_rows do not list its sections in order, or a row is
            wider than four sections.
    """
    parts = index.parts
    width = "3.30cm"
    spine, label_x, page_depth = -2.40, -1.80, -23.0
    layout: list[tuple[int, Part, list[list[str]], float]] = []
    for i, part in enumerate(parts):
        groups = part.chart_rows or [
            part.routes[k : k + COLUMNS] for k in range(0, len(part.routes), COLUMNS)
        ]
        require(
            [m for g in groups for m in g] == part.routes,
            "chart_rows must list the part sections in order",
            part.id,
        )
        require(
            max(len(g) for g in groups) <= COLUMNS,
            "Whole-guide DAG row is wider than four sections",
            part.id,
        )
        layout.append((i, part, groups, 1.10 + 1.80 * (len(groups) - 1) + 1.25))
    pages: list[list[tuple[int, Part, list[list[str]], float]]] = [[]]
    used = 0.0
    for item in layout:
        if pages[-1] and used + item[3] > -page_depth:
            pages.append([])
            used = 0.0
        pages[-1].append(item)
        used += item[3]
    source = parts[0].routes[0]
    result = []
    for n, page in enumerate(pages):
        if n == 0:
            result.append(
                "\\clearpage\n"
                "\\section*{Learning pathway DAG}\\phantomsection\\label{learning-map}\n"
                "\\markboth{Learning pathway DAG}{}\n"
                "\\addcontentsline{toc}{section}{Learning pathway DAG}\n"
            )
        else:
            result.append(
                "\\clearpage\n"
                "\\section*{Learning pathway DAG (continued)}\\phantomsection"
                "\\label{learning-map-" + str(n + 1) + "}\n"
                "The dashed connector from "
                + index.link(source)
                + " continues from the \\hyperref[learning-map]{previous page}.\n"
            )
        result.append("\\begin{center}\n\\begin{tikzpicture}[x=1cm,y=1cm]\n")
        y = 0.0
        rows: list[tuple[float, list[str]]] = []
        for i, part, groups, _ in page:
            label = (
                r"\hyperref[part-"
                + part.id
                + "]{PART "
                + ROMAN[i]
                + ": "
                + tex_escape(part.title).upper()
                + "}"
            )
            result.append(
                r"\node[maplabel,anchor=west] at ("
                + f"{label_x:.2f},{y:.2f}"
                + ") {"
                + label
                + "};\n"
            )
            y -= 1.10
            for j, group in enumerate(groups):
                if j:
                    y -= 1.80
                for k, identifier in enumerate(group):
                    result.append(
                        chart_node(
                            index,
                            identifier,
                            f"{k * STEP:.2f}",
                            f"{y:.2f}",
                            width=width,
                            show_count=True,
                        )
                    )
                for a, b in itertools.pairwise(group):
                    result.append(r"\draw[patharrow] (" + a + ".east) -- (" + b + ".west);\n")
                rows.append((y, group))
            y -= 1.25
        start = f"{spine:.2f},0.30"
        if n == 0:
            result.append(
                r"\draw[entryline] ("
                + source
                + ".west) -- ("
                + f"{spine:.2f},{rows[0][0]:.2f}"
                + ") -- ("
                + f"{spine:.2f},{rows[-1][0]:.2f}"
                + ");\n"
            )
        else:
            result.append(
                r"\draw[entryline] (" + start + ") -- (" + f"{spine:.2f},{rows[-1][0]:.2f}" + ");\n"
            )
        for row_y, group in rows:
            if source not in group:
                result.append(
                    r"\draw[entryarrow] ("
                    + f"{spine:.2f},{row_y:.2f}"
                    + ") -- ("
                    + group[0]
                    + ".west);\n"
                )
        result.append("\\end{tikzpicture}\n\\end{center}\n")
    return "".join(result)


def spread(desired: Sequence[float], step: float, lo: float, hi: float) -> list[float]:
    """Keep nodes in their given order, at least `step` apart within [lo, hi], near `desired`."""
    xs: list[float] = []
    for d in desired:
        xs.append(max(d, xs[-1] + step) if xs else max(d, lo))
    for i in range(len(xs) - 1, -1, -1):
        xs[i] = min(xs[i], hi if i == len(xs) - 1 else xs[i + 1] - step)
    # Centre a crowded group on its targets without leaving the chart width.
    shift = sum(d - x for d, x in zip(desired, xs, strict=True)) / len(xs)
    shift = max(lo - xs[0], min(shift, hi - xs[-1]))
    return [x + shift for x in xs]


class SectionLayout:
    """Node positions and entry rails of one overview section's DAG.

    Entry pathways (no prerequisite inside the section) sit in subsection order on the first
    row, fed by a dashed rail from the overview; pathways with in-section prerequisites sit
    below them, each parent centred over its children. When more than four pathways are
    entries, or the rows cannot centre a parent over the pathways that depend only on it,
    prerequisite trees are packed in subsection order into balanced rows, each with its own
    rail.

    Raises:
        RouteError: From the constructor, if an in-section prerequisite follows its pathway,
            a prerequisite tree is wider than four columns, or specialist_order does not
            read row by row through the chart.
    """

    width: Final = "3.65cm"
    row: Final = 2.30
    top: Final = -2.75

    def __init__(self, index: RouteIndex, root_id: str) -> None:
        """Lay out the section's pathways."""
        root = index.overviews[root_id]
        self.root_id = root_id
        self.members = list(root.specialist_order)
        mset = set(self.members)
        self.parents = {
            m: [p for p in index.routes[m].prerequisite_routes if p in mset] for m in self.members
        }
        for m in self.members:
            for p in self.parents[m]:
                require(
                    self.members.index(p) < self.members.index(m),
                    "In-section prerequisite must precede",
                    m,
                    p,
                )
        self.depth: dict[str, int] = {}
        for m in self.members:
            self._depth(m)
        self.levels = {
            level: [m for m in self.members if self.depth[m] == level]
            for level in sorted(set(self.depth.values()))
        }
        self.pos: dict[str, Position] = {}
        self.rails: list[tuple[float, list[str]]] = []
        if max(map(len, self.levels.values())) <= COLUMNS:
            self._layered()
        if not self.pos:
            self._wrapped()
        # Subsection numbers must read row by row, left to right, through the drawn chart.
        drawn = sorted(
            self.members, key=lambda m: (-round(self.pos[m][1], 2), round(self.pos[m][0], 2))
        )
        require(
            drawn == self.members,
            "Reorder specialist_order to follow the chart row by row",
            root_id,
            drawn,
        )

    def _depth(self, m: str) -> int:
        """Return a pathway's level: one more than its deepest in-section prerequisite."""
        if m not in self.depth:
            self.depth[m] = 1 + max([self._depth(p) for p in self.parents[m]], default=0)
        return self.depth[m]

    def _layered(self) -> None:
        """Place each deeper pathway under its parents, then centre parents over children."""
        levels, parents, pos, row, top = self.levels, self.parents, self.pos, self.row, self.top
        right = (max(map(len, levels.values())) - 1) * STEP
        for level, nodes in levels.items():
            if level == 1:
                xs = [i * STEP for i in range(len(nodes))]
            else:
                target = {m: sum(pos[p][0] for p in parents[m]) / len(parents[m]) for m in nodes}
                nodes = sorted(nodes, key=target.__getitem__)
                xs = spread([target[m] for m in nodes], STEP, 0, right)
            for m, x in zip(nodes, xs, strict=True):
                pos[m] = (x, top - (level - 1) * row)
        for level in sorted(levels, reverse=True)[1:]:
            nodes = sorted(levels[level], key=lambda m: pos[m][0])
            centres = []
            for m in nodes:
                below = [c for c in levels.get(level + 1, []) if m in parents[c]]
                centres.append(sum(pos[c][0] for c in below) / len(below) if below else pos[m][0])
            for m, x in zip(nodes, spread(centres, STEP, 0, right), strict=True):
                pos[m] = (x, pos[m][1])
        self.rails.append((top + row / 2, levels[1]))
        # A packed entry row can leave a parent off-centre, so a slanted arrow runs under
        # a neighbouring entry; the tree layout gives each parent its own columns instead.
        for m in self.members:
            only = [c for c in self.members if parents[c] == [m]]
            if only and abs(pos[m][0] - sum(pos[c][0] for c in only) / len(only)) > 0.01:
                self.pos.clear()
                self.rails.clear()
                break

    def _wrapped(self) -> None:
        """Hang each pathway under its latest in-section prerequisite, in balanced bands."""
        members, parents, row = self.members, self.parents, self.row
        tree_parent = {m: max(parents[m], key=members.index) for m in members if parents[m]}
        kids = {m: [c for c in members if tree_parent.get(c) == m] for m in members}

        def span(m: str) -> int:
            return max(1, sum(span(c) for c in kids[m]))

        def height(m: str) -> int:
            return 1 + max([height(c) for c in kids[m]], default=0)

        entries = self.levels[1]
        total = sum(span(m) for m in entries)
        target = -(-total // -(-total // COLUMNS))
        bands: list[list[str]] = [[]]
        used = 0
        for m in entries:
            require(
                span(m) <= COLUMNS,
                "Section DAG prerequisite tree is wider than four columns",
                self.root_id,
                m,
            )
            if bands[-1] and used + span(m) > target:
                bands.append([])
                used = 0
            bands[-1].append(m)
            used += span(m)
        y = self.top

        def put(m: str, col: int, level: int) -> None:
            self.pos[m] = ((col + (span(m) - 1) / 2) * STEP, y - level * row)
            for c in kids[m]:
                put(c, col, level + 1)
                col += span(c)

        for band in bands:
            col = 0
            for m in band:
                put(m, col, 0)
                col += span(m)
            self.rails.append((y + row / 2, band))
            y -= max(height(m) for m in band) * row

    def elbow(
        self, p: str, m: str, edges: Sequence[tuple[str, str]]
    ) -> tuple[str, str, str] | None:
        """Return the corners of a long cross-column arrow, or None if something is in the way.

        The arrow runs down the parent's column, then across the gap above the child into
        its parent-side shoulder.
        """
        pos, row = self.pos, self.row
        (px, py), (cx, cy) = pos[p], pos[m]
        if abs(px - cx) < 0.01:
            return None
        gap = cy + row / 2
        ex = cx + (0.6 if px > cx else -0.6)
        for n, (nx, ny) in pos.items():
            if n not in (p, m) and abs(nx - px) < STEP / 2 and gap < ny < py:
                return None
        lo, hi = sorted((px, ex))
        for a, b in edges:
            if (
                (a, b) != (p, m)
                and pos[a][1] > gap > pos[b][1]
                and lo < (pos[a][0] + pos[b][0]) / 2 < hi
            ):
                return None
        return f"{px:.2f},{gap:.2f}", f"{ex:.2f},{gap:.2f}", f"{ex:.2f},0"


def section_chart(index: RouteIndex, root_id: str) -> str:
    """Return the focused DAG of one overview section, with its capstone and foundations.

    Solid arrows are in-section prerequisites; cross-section prerequisites are listed below
    the chart.

    Raises:
        RouteError: If the section cannot be laid out (see SectionLayout).
    """
    root = index.overviews[root_id]
    layout = SectionLayout(index, root_id)
    members, parents, pos, rails = layout.members, layout.parents, layout.pos, layout.rails
    root_x = max(x for x, _ in pos.values()) / 2
    left = -2.35
    out = [
        "\\clearpage\n"
        "\\subsection*{" + tex_escape(root.name) + ": pathway DAG}\\phantomsection"
        "\\label{" + section_dag_label(root_id) + "}\n"
        "\\addcontentsline{toc}{subsection}{" + tex_escape(root.name) + ": pathway DAG}\n"
        "Start with the section overview's readings, for orientation. Solid arrows show"
        " prerequisites within this section. Dashed connectors identify entry points with no"
        " further prerequisite in this section; the linked foundations below still apply."
        " Follow the arrows for dependencies and the subsection numbers for reading order."
        " Every node is clickable.\n"
        "\\begin{center}\\begin{tikzpicture}[x=1cm,y=1cm]\n"
    ]
    out.append(chart_node(index, root_id, f"{root_x:.2f}", 0, width="4.6cm"))
    for m in members:
        out.append(chart_node(index, m, f"{pos[m][0]:.2f}", f"{pos[m][1]:.2f}", width=layout.width))
    first_rail = max(r for r, _ in rails)
    last_rail = min(r for r, _ in rails)
    out.append(
        r"\draw[entryline] (" + root_id + ".south) -- (" + f"{root_x:.2f},{first_rail:.2f}" + ");\n"
    )
    if len(rails) > 1:
        out.append(
            r"\draw[entryline] ("
            + f"{left:.2f},{first_rail:.2f}"
            + ") -- ("
            + f"{left:.2f},{last_rail:.2f}"
            + ");\n"
        )
    for ry, entries in rails:
        xs = [pos[m][0] for m in entries]
        rail_left = left if len(rails) > 1 else min(min(xs), root_x)
        rail_right = max(max(xs), root_x) if ry == first_rail else max(xs)
        out.append(
            r"\draw[entryline] ("
            + f"{rail_left:.2f},{ry:.2f}"
            + ") -- ("
            + f"{rail_right:.2f},{ry:.2f}"
            + ");\n"
        )
        for m in entries:
            out.append(
                r"\draw[entryarrow] (" + f"{pos[m][0]:.2f},{ry:.2f}" + ") -- (" + m + ".north);\n"
            )
    edges = [(p, m) for m in members for p in parents[m]]
    for p, m in edges:
        if abs(pos[p][1] - pos[m][1]) > layout.row + 0.01:
            route = layout.elbow(p, m, edges)
            if route:
                out.append(
                    r"\draw[patharrow] ("
                    + p
                    + ".south) -- ("
                    + route[0]
                    + ") -- ("
                    + route[1]
                    + ") -- ("
                    + m
                    + ".north -| "
                    + route[2]
                    + ");\n"
                )
            else:
                out.append(
                    r"\draw[patharrow] ("
                    + p
                    + ".south) .. controls +(0,-0.9) and +(0,0.9) .. ("
                    + m
                    + ".north);\n"
                )
        else:
            out.append(r"\draw[patharrow] (" + p + ".south) -- (" + m + ".north);\n")
    out.append(r"\end{tikzpicture}\end{center}" + "\n")
    if root.checkpoint_after:
        out.append(
            r"\textbf{Overview checkpoint.} A section capstone: complete it after "
            + and_list([index.number_link(p) for p in root.checkpoint_after])
            + ".\n\n"
        )
    external: dict[str, list[str]] = {}
    mset = set(members)
    for m in members:
        for p in index.routes[m].prerequisite_routes:
            if p not in mset and p != root_id:
                external.setdefault(p, []).append(m)
    if external:
        out.append(r"\textbf{Bring these foundations with you.}\begin{itemize}" + "\n")
        for p, ms in external.items():
            needed = ", ".join(index.link(m, index.routes[m].chart_title) for m in ms)
            out.append(r"\item " + index.link(p) + " --- needed by " + needed + ".\n")
        out.append(r"\end{itemize}")
    out.append(r"\hyperref[learning-map]{Return to the whole-guide DAG.}" + "\n")
    return "".join(out)
