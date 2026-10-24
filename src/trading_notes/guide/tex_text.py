"""TeX argument parsing, escaping and the small TeX-to-HTML rendering the catalogue needs."""

import html
import re
import unicodedata
from collections.abc import Sequence
from typing import Final

# The catalogue commands whose arguments the guide reads, with their argument counts.
CATALOGUE_COMMANDS: Final = {"CatalogueEntry": 7, "ExtendedNote": 2, "EntryRecency": 7}
TEX_SPECIALS: Final = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}
ACCENTS: Final = {
    "'": "\u0301",
    "`": "\u0300",
    '"': "\u0308",
    "^": "\u0302",
    "~": "\u0303",
    "c": "\u0327",
    "u": "\u0306",
    "H": "\u030b",
    "v": "\u030c",
    "=": "\u0304",
}
SPECIAL_WORDS: Final = {
    "textquotesingle": "'",
    "textquotedblleft": "\u201c",
    "textquotedblright": "\u201d",
    "textquoteleft": "\u2018",
    "textquoteright": "\u2019",
    "textendash": "\u2013",
    "textemdash": "\u2014",
    "ss": "ß",
    "O": "Ø",
    "o": "ø",
    "i": "\u0131",
    "ae": "æ",
    "AA": "Å",
    "LaTeX": "LaTeX",
    "par": "<br>",
    "newline": "<br>",
    "quad": " ",
    "enspace": " ",
    "textasciitilde": "~",
    "textasciicircum": "^",
}
FONT_TAGS: Final = {
    "emph": "em",
    "textit": "em",
    "textbf": "strong",
    "texttt": "code",
    "textsuperscript": "sup",
}
SPAN_COMMANDS: Final = (
    "emph",
    "textit",
    "textbf",
    "texttt",
    "mbox",
    "zh",
    "textrm",
    "textnormal",
    "textsuperscript",
)


class TexError(ValueError):
    """The TeX source is malformed for the guide's reading of it."""


def argument(s: str, i: int) -> tuple[str, int]:
    """Return the braced argument starting at or after s[i] and the index after it.

    Raises:
        TexError: If no brace opens there, or the braces do not balance.
    """
    while s[i].isspace():
        i += 1
    if s[i] != "{":
        raise TexError(s[i : i + 100])
    depth = 1
    j = i + 1
    while j < len(s):
        if s[j] == "\\":
            j += 2
            continue
        if s[j] == "{":
            depth += 1
        if s[j] == "}":
            depth -= 1
        if depth == 0:
            return s[i + 1 : j], j + 1
        j += 1
    raise TexError("Unbalanced argument at " + str(i))


def commands(source: str, name: str, count: int) -> list[list[str]]:
    """Return the arguments of every line-initial use of a command with count arguments."""
    result = []
    for m in re.finditer(r"^\\" + name + r"\{", source, re.M):
        args = []
        i = m.end() - 1
        for _ in range(count):
            a, i = argument(source, i)
            args.append(a)
        result.append(args)
    return result


def check_one_line_commands(source: str) -> None:
    """Check that each catalogue command fills one line, so a line diff finds every change.

    Raises:
        TexError: If a command spans lines or shares its line.
    """
    for m in re.finditer(r"^\\(CatalogueEntry|ExtendedNote|EntryRecency)\{", source, re.M):
        i = m.end() - 1
        for _ in range(CATALOGUE_COMMANDS[m[1]]):
            _, i = argument(source, i)
        if "\n" in source[m.start() : i] or source[i : i + 1] not in ("\n", ""):
            raise TexError(
                "Keep each catalogue command on one line: " + source[m.start() : m.start() + 80]
            )


def unlinked(s: str) -> str:
    """Keep TeX typography; strip nested destinations from a linked guide title."""
    out = ""
    i = 0
    while i < len(s):
        m = re.match(r"\\(href|hyperlink|hypertarget)\{", s[i:])
        if m:
            _, j = argument(s, i + m.end() - 1)
            b, k = argument(s, j)
            out += "" if m[1] == "hypertarget" else unlinked(b)
            i = k
        elif s.startswith("\\sourcecite{", i):
            _, i = argument(s, i + len("\\sourcecite"))
        else:
            out += s[i]
            i += 1
    return out


def tex_escape(s: str) -> str:
    """Return text with TeX's special characters escaped."""
    return "".join(TEX_SPECIALS.get(c, c) for c in s)


def and_list(items: Sequence[str]) -> str:
    """Return items joined with commas and a final "and"."""
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def web_url(s: str) -> str:
    """Return a TeX-escaped URL as a plain one."""
    return s.replace(r"\_", "_").replace(r"\%", "%").replace(r"\&", "&").replace(r"\#", "#")


def to_html(s: str) -> str:
    """Render the small TeX prose subset used by the catalogue, without TeX input."""
    out: list[str] = []
    i = 0
    while i < len(s):
        if s[i] == "\\":
            m = re.match(r"\\([A-Za-z]+|.)\s*", s[i:])
            if not m:
                i += 1
                continue
            cmd = m[1]
            j = i + m.end()
            if cmd in ["&", "%", "$", "#", "_", "{", "}"]:
                out.append(html.escape(cmd))
                i = j
                continue
            if cmd in ACCENTS and j < len(s):
                if s[j] == "{":
                    a, k = argument(s, j)
                else:
                    a, k = s[j], j + 1
                out.append(html.escape(unicodedata.normalize("NFC", a + ACCENTS[cmd])))
                i = k
                continue
            if cmd in ["href", "hyperlink", "hypertarget"]:
                a, j = argument(s, j)
                b, j = argument(s, j)
                if cmd != "hypertarget":
                    url = web_url(a) if cmd == "href" else "#" + a
                    out.append(
                        '<a href="' + html.escape(url, quote=True) + '">' + to_html(b) + "</a>"
                    )
                i = j
                continue
            if cmd == "hyperref" and j < len(s) and s[j] == "[":
                k = s.index("]", j)
                target = s[j + 1 : k]
                a, j = argument(s, k + 1)
                out.append(
                    '<a href="#' + html.escape(target, quote=True) + '">' + to_html(a) + "</a>"
                )
                i = j
                continue
            if cmd in ["ref", "sourcecite"]:
                a, j = argument(s, j)
                dest = a if cmd == "ref" else "source-" + a
                text = a if cmd == "sourcecite" else "catalogue section"
                out.append(
                    '<a href="#' + html.escape(dest, quote=True) + '">' + html.escape(text) + "</a>"
                )
                i = j
                continue
            if cmd == "url":
                a, j = argument(s, j)
                url = html.escape(web_url(a), quote=True)
                out.append('<a href="' + url + '">' + url + "</a>")
                i = j
                continue
            if cmd in SPAN_COMMANDS:
                a, j = argument(s, j)
                tag = FONT_TAGS.get(cmd, "span")
                out.append("<" + tag + ">" + to_html(a) + "</" + tag + ">")
                i = j
                continue
            if cmd in ["label", "Needspace"]:
                if j < len(s) and s[j] == "{":
                    _, j = argument(s, j)
                i = j
                continue
            if cmd in SPECIAL_WORDS:
                out.append(SPECIAL_WORDS[cmd])
                i = j
                continue
            # Remaining mathematical/formatting commands are shown as readable text.
            out.append(html.escape(cmd))
            i = j
            continue
        if s[i] not in "{}$":
            out.append(html.escape(s[i]))
        i += 1
    return (
        "".join(out)
        .replace("---", "\u2014")
        .replace("--", "\u2013")
        .replace("``", "\u201c")
        .replace("''", "\u201d")
    )
