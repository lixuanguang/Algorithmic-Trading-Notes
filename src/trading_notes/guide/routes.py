"""The guide's route file: parts, overview sections, specialist pathways and their checks."""

import datetime as dt
import re
from pathlib import Path
from typing import Final, Literal, Self

from pydantic import ConfigDict, Field

from trading_notes.guide.tex_text import tex_escape
from trading_notes.records import Record

ROMAN: Final = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
KEY: Final = re.compile(r"[a-z0-9-]+")
# The guide's original numbering: each overview key keeps its label, on a live overview or a
# retired bridge. Taken from learning_routes.json at commit 343d145; the scheme is closed.
LEGACY_LABELS: Final = {
    "common-toolkit": "route-1",
    "systematic-equities": "route-2",
    "multi-asset-systematic-macro": "route-3",
    "rates-credit-mortgages": "route-4",
    "volatility-options": "route-5",
    "execution-market-making": "route-6",
    "ml-alternative-data": "route-7",
    "portfolio-risk-financing": "route-8",
    "energy-commodities": "route-9",
    "digital-assets-prediction-markets": "route-10",
    "research-engineering-validation": "route-11",
    "private-capital-allocator": "route-12",
    "real-asset-investor": "route-13",
    "insurance-climate-risk": "route-14",
    "global-regional-markets": "route-15",
    "empirical-causal-research": "route-16",
    "corporate-credit-capital": "route-17",
    "securitised-structured-credit": "route-18",
    "portfolio-construction-risk": "route-19",
    "power-gas-environmental": "route-20",
    "onchain-protocols": "route-21",
    "event-contracts-prediction-markets": "route-22",
    "execution-trading-costs": "route-23",
    "government-bond-markets": "route-24",
    "volatility-trading-premia": "route-25",
    "currency-markets": "route-26",
    "international-equity-markets": "route-27",
    "commodity-investing-premia": "route-28",
    "physical-commodity-markets": "route-29",
    "commodity-spot-markets": "route-30",
    "oil-shocks-macro": "route-31",
    "environmental-markets": "route-32",
    "crypto-spot-markets": "route-33",
    "tokenised-fractional-assets": "route-34",
    "crypto-market-making": "route-35",
    "crypto-trading-strategies": "route-36",
    "event-contract-venues": "route-37",
    "event-contract-trading": "route-38",
}
# A hard-coded section or part number in prose, with an ordinary or TeX (~) space.
BARE_REFERENCE: Final = (
    r"\(\d+\.\d+\)|\b(?:Section|Part)[\s~]+(?:\d+|[IVX]+)\b"
    r"|\b(?:from|after|of|and|in)[\s~]+\d+\.\d+\b(?!\s?%)"
)
PROSE_REFERENCE: Final = re.compile(r"\[\[(part:)?([a-z0-9-]+)\]\]")


class RouteError(ValueError):
    """The route file breaks one of the guide's placement, reference or labelling rules."""


def require(condition: bool, *message: object) -> None:
    """Raise RouteError with the message unless the condition holds."""
    if not condition:
        raise RouteError(message[0] if len(message) == 1 else message)


class FileRecord(Record):
    """A record read from the route file; an unknown field is an error."""

    model_config = ConfigDict(extra="forbid")


class Reading(FileRecord):
    """A required reading.

    Attributes:
        anchor: Its catalogue key.
        reason: Why it is read.
        selection: The passages to read, in the source's own numbering, if not the whole.
        stage: Its stage label, for specialist pathways.
    """

    anchor: str
    reason: str
    selection: str | None = None
    stage: str | None = None


class Branch(FileRecord):
    """An optional branch.

    Attributes:
        target: A catalogue key or a catalogue label.
        reason: Its link text.
    """

    target: str
    reason: str


class SectionGoal(FileRecord):
    """A goal of an overview section and the pathways that teach it.

    Attributes:
        goal: The goal.
        pathways: The specialist pathway keys.
    """

    goal: str
    pathways: list[str]


class Route(FileRecord):
    """What overview sections and specialist pathways share.

    Attributes:
        id: The route key.
        name: Its title.
        chart_name: A shorter title for the DAGs, if any.
        outcome: What the route delivers.
        prerequisites: Its prerequisites, in prose.
        prerequisite_routes: The route keys to review first.
        required_readings: The readings, in order.
        checkpoint: Its checkpoint.
        optional_branches: Further catalogue entries.
    """

    id: str
    name: str
    chart_name: str | None = None
    outcome: str
    prerequisites: str
    prerequisite_routes: list[str] = Field(default_factory=list)
    required_readings: list[Reading]
    checkpoint: str
    optional_branches: list[Branch]

    @property
    def label(self) -> str:
        """Return its TeX label: route-<key> for an overview, specialist-<key> for a pathway."""
        return ("route-" if isinstance(self, Overview) else "specialist-") + self.id

    @property
    def chart_title(self) -> str:
        """Return the title the DAGs use."""
        return self.chart_name or self.name

    def texts(self) -> list[str]:
        """Return its prose fields, in which references are checked."""
        return [self.outcome, self.prerequisites, self.checkpoint]


class Overview(Route):
    """An overview section, opening its specialist pathways.

    Attributes:
        legacy_label: Its label in the original numbered scheme, if any.
        specialist_order: Its pathways, in the order the section DAG draws them.
        section_goals: Its goals, mapping every pathway.
        learning_note: Its place in the learning order.
        checkpoint_after: For a capstone checkpoint, the pathways it follows.
    """

    legacy_label: str | None = None
    specialist_order: list[str]
    section_goals: list[SectionGoal]
    learning_note: str
    checkpoint_after: list[str] = Field(default_factory=list)

    def texts(self) -> list[str]:
        """Return its prose fields, goals included."""
        return [*super().texts(), self.learning_note, *(g.goal for g in self.section_goals)]


class Specialist(Route):
    """A specialist pathway.

    Attributes:
        parent_route: The name of the overview it applies.
    """

    parent_route: str


class Part(FileRecord):
    """A part of the guide.

    Attributes:
        id: The part key.
        title: Its title.
        introduction: Its introduction.
        routes: Its overview sections, in order.
        chart_rows: How the whole-guide DAG groups them, when not by fours.
    """

    id: str
    title: str
    introduction: str
    routes: list[str]
    chart_rows: list[list[str]] | None = None


class RetiredOverview(FileRecord):
    """An overview that was divided, kept so that earlier links still resolve.

    Attributes:
        id: Its key.
        legacy_label: Its original label, if any.
        name: Its name.
        successors: The live overviews that replace it.
        note: An editorial note.
    """

    id: str
    legacy_label: str | None = None
    name: str
    successors: list[str]
    note: str


class LearningRoutes(FileRecord):
    """The route file, learning_routes.json.

    Attributes:
        schema_version: The file's schema version.
        source: The catalogue it selects from.
        learning_parts: The parts, in order.
        routes: The overview sections.
        specialist_routes: The specialist pathways.
        retired_overviews: The divided overviews.
        catalogue_link_target: Whether readings link to the catalogue PDF or the HTML notes.
        as_of: The guide's edition date.
        pathway_updated_on: When the pathways were last revised.
    """

    schema_version: int
    source: str
    learning_parts: list[Part]
    routes: list[Overview]
    specialist_routes: list[Specialist] = Field(default_factory=list)
    retired_overviews: list[RetiredOverview] = Field(default_factory=list)
    catalogue_link_target: Literal["html", "pdf"] = "pdf"
    as_of: dt.date = dt.date(2026, 10, 4)
    pathway_updated_on: dt.date

    @classmethod
    def read(cls, path: Path) -> Self:
        """Read and validate the route file."""
        return cls.model_validate_json(path.read_text())


class RouteIndex:
    """The routes by key, after the placement, reference and label checks.

    Raises:
        RouteError: From the constructor, if a rule is broken.
    """

    def __init__(self, data: LearningRoutes) -> None:
        """Index the routes and check every rule the guide relies on."""
        self.data = data
        self.parts = data.learning_parts
        self.overviews: dict[str, Overview] = {r.id: r for r in data.routes}
        self.routes: dict[str, Overview | Specialist] = {r.id: r for r in data.routes}
        self.routes.update({s.id: s for s in data.specialist_routes})
        self.placement = {sid: r.id for r in data.routes for sid in r.specialist_order}
        self.part_of = {identifier: p.id for p in self.parts for identifier in p.routes}
        self._check()

    def _check(self) -> None:
        """Keep editorial placement, prerequisite links and stable route identities aligned."""
        data, overviews, routes = self.data, self.overviews, self.routes
        specialists, parts, retired = data.specialist_routes, self.parts, data.retired_overviews
        require(len(routes) == len(data.routes) + len(specialists), "Duplicate pathway identifiers")
        for identifier in routes:
            require(bool(KEY.fullmatch(identifier)), identifier)
        require(len({p.id for p in parts}) == len(parts), "Duplicate part identifiers")
        for p in parts:
            require(
                bool(KEY.fullmatch(p.id)),
                "Part identifiers use only a-z, 0-9 and hyphens, as prose references do",
                p.id,
            )
        ordered = [identifier for part in parts for identifier in part.routes]
        require(
            len(ordered) == len(set(ordered)) and set(ordered) == set(overviews),
            "Overview placement mismatch",
        )
        children = [identifier for r in data.routes for identifier in r.specialist_order]
        require(
            len(children) == len(set(children)) and set(children) == {r.id for r in specialists},
            "Specialist placement mismatch",
        )
        sequence = []
        for identifier in ordered:
            sequence.extend([identifier, *overviews[identifier].specialist_order])
        positions = {identifier: n for n, identifier in enumerate(sequence)}
        for r in routes.values():
            for prerequisite in r.prerequisite_routes:
                require(prerequisite in routes, r.id, prerequisite)
                require(
                    positions[prerequisite] < positions[r.id],
                    "Prerequisite must precede pathway",
                    r.id,
                    prerequisite,
                )
        # Overviews added after the numbered legacy scheme have no legacy label; retired
        # overviews keep theirs, on a bridge, so earlier links still resolve.
        labelled = [(r.id, r.legacy_label) for r in data.routes] + [
            (r.id, r.legacy_label) for r in retired
        ]
        legacy = [label for _, label in labelled if label is not None]
        require(len(legacy) == len(set(legacy)), "Duplicate legacy route labels")
        owners = {key: label for key, label in labelled if label is not None}
        require(
            owners == LEGACY_LABELS,
            "Keep each inherited legacy label on its original overview key",
            sorted(set(owners.items()) ^ set(LEGACY_LABELS.items())),
        )
        for old in retired:
            require(
                bool(KEY.fullmatch(old.id)) and old.id not in routes,
                "A retired overview key must not be a live route",
                old.id,
            )
            require(
                bool(old.successors) and set(old.successors) <= set(overviews),
                "Retired overview successors must be live overviews",
                old.id,
            )
        require(len({r.id for r in retired}) == len(retired), "Duplicate retired overview keys")
        self._check_prose()
        # An overview's outcome is what its checkpoint tests; its section goals map the wider
        # coverage to the pathways that teach it, and a capstone checkpoint names those it needs.
        for r in data.routes:
            members = set(r.specialist_order)
            goals = r.section_goals
            require(
                bool(goals) and all(g.goal and g.pathways for g in goals),
                "Overview needs section goals",
                r.id,
            )
            taught = {p for g in goals for p in g.pathways}
            require(
                taught == members,
                "Section goals must map every pathway in the section and no other",
                r.id,
                sorted(taught ^ members),
            )
            require(
                set(r.checkpoint_after) <= members,
                "A capstone checkpoint follows pathways in its own section",
                r.id,
            )
        route_names = {r.name for r in data.routes}
        for s in specialists:
            require(s.parent_route in route_names, s.parent_route)

    def _check_prose(self) -> None:
        """Check that prose names routes and parts by key, never by number."""
        part_ids = {p.id for p in self.parts}
        texts = [("part " + p.id, p.introduction) for p in self.parts]
        for r in self.routes.values():
            texts += [(r.id, t) for t in r.texts()]
            texts += [(r.id, rd.reason) for rd in r.required_readings]
            texts += [(r.id, b.reason) for b in r.optional_branches]
        # A reading's selection locates passages in its source (its own section numbers), so
        # only references are checked there, not bare numbers.
        selections = [
            (r.id, rd.selection)
            for r in self.routes.values()
            for rd in r.required_readings
            if rd.selection
        ]
        for owner, text in texts + selections:
            for kind, key in re.findall(r"\[\[(part:)?([^\]]*)\]\]", text):
                require(
                    (key in part_ids) if kind else (key in self.routes),
                    "Unresolved prose reference",
                    owner,
                    kind + key,
                )
        for owner, text in texts:
            bare = re.findall(BARE_REFERENCE, text)
            require(
                not bare,
                "Name routes and parts with [[key]] or [[part:key]], not numbers",
                owner,
                bare,
            )

    def label(self, identifier: str) -> str:
        """Return a route's TeX label."""
        return self.routes[identifier].label

    def number_link(self, identifier: str) -> str:
        """Return a link printing a route's current section or subsection number."""
        label = self.label(identifier)
        return r"\hyperref[" + label + r"]{\ref*{" + label + "}}"

    def link(self, identifier: str, text: str | None = None) -> str:
        """Return a link to a route, with its name or the given text."""
        return (
            r"\hyperref["
            + self.label(identifier)
            + "]{"
            + tex_escape(text or self.routes[identifier].name)
            + "}"
        )

    def numeral(self, part_id: str) -> str:
        """Return a part's Roman numeral."""
        return ROMAN[[p.id for p in self.parts].index(part_id)]

    def prose(self, s: str, linked: bool = True) -> str:
        """Escape route-file prose, printing route and part references as current numbers.

        [[route-id]] prints the route's number and [[part:part-id]] the part's numeral; with
        linked False (inside another link) they are not links.

        Raises:
            RouteError: If a reference is malformed.
        """
        numerals = {p.id: ROMAN[i] for i, p in enumerate(self.parts)}
        require("[[" not in PROSE_REFERENCE.sub("", s), "Unparsed prose reference", s)
        out = []
        i = 0
        for m in PROSE_REFERENCE.finditer(s):
            out.append(tex_escape(s[i : m.start()]))
            i = m.end()
            if m[1]:
                part = numerals[m[2]]
                out.append(r"\hyperref[part-" + m[2] + "]{" + part + "}" if linked else part)
            else:
                out.append(self.number_link(m[2]) if linked else r"\ref*{" + self.label(m[2]) + "}")
        return "".join(out) + tex_escape(s[i:])
