# Compendium conventions

The compendium is a reference organised by subject. `compendium.tex` includes each existing `<section-key>/section.tex` in guide order; each chapter wrapper contains its heading, label and topic inputs.

## Content

Use the guide's eleven entry types and their label prefixes. Every entry needs a descriptive title, a unique label, a Statement field and citations with locators. Conditions, Notation, Practice, Pitfalls, See also and Further reading should contain information useful to a reader of the subject.

Explain the concept directly. Aim for one idea and roughly 80–140 words per paragraph; split long fields at topic changes and sentence boundaries. Preserve assumptions, units, date ranges, source limitations and distinctions between illustrative calculations and empirical evidence. Explain an incorrect formula or interpretation only when the correction teaches a material distinction. Omit editing narratives, migration history, study progress, retrieval diaries and lists of keywords: do not record what was or was not read, checked or compared, how a source was obtained, which script reproduced a number, or which version of an entry came first. A version note belongs in an entry only when it changes the locators (for example, page numbers that refer to a working paper).

Source-review provenance is stored by entry label in `notes/entry-evidence.json`, with detailed research records in `notes/source-review-records.md`. These records do not imply that a claim is independently verified. Keep important historical or jurisdictional limits in the entry's Conditions even when also recorded outside the PDF.

Use subject names for files and operations for functions. Update references when renaming an artefact. Preserve numerical inputs, results and historical evidence identities; a filename change is not a new research run.

## Typography

The document uses `extbook` at 8 pt, with Source Sans Pro text, Source Code Pro identifiers and matching sans-serif mathematics (`newtxsf`). Chapter, section, subsection and subsubsection headings use 14, 11, 9 and 8 pt respectively. The title page follows the class's scaled type sizes. Lists have no extra vertical space between items or paragraphs within items. The LuaTeX line breaker in `typography.lua` keeps at least five words on the last line of every multi-line paragraph and list item: it first breaks the paragraph with its last five words tied, and falls back to the normal break if that would overfill a line or stretch one beyond the normal tolerance. Where the fallback still leaves a short last line, reword the paragraph; never use manual line breaks or ragged-right setting to move words. Single-line items and table cells keep their natural layout; widow/orphan penalties keep isolated lines off page boundaries. The rules are in `preamble.tex`; avoid local spacing overrides unless a particular table or diagram needs one.

## Validation

From the repository root:

```sh
python3 tools/check_compendium.py --check
python3 -m unittest discover -s tools
```

Build from this directory:

```sh
latexmk -lualatex -interaction=nonstopmode -halt-on-error compendium.tex
```

The checker validates entry structure, known citation keys and locators, duplicate labels and links from pathway notes. It does not establish the truth of a claim. After layout changes, inspect rendered pages containing chapter headings, lists, tables, equations and figures, and check the LaTeX log for overfull boxes and unresolved references.
