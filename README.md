# All Things on Quantitative Trading

A source-based reference on quantitative trading and the financial analysis behind it. Its eight Parts and their chapters follow the `\qfpart` declarations in `compendium/compendium.tex`, which match the Parts and sections of the institutional learning guide pinned in `guide/`; within each chapter, the numbered sections are the guide's specialist pathways that have entries. The guide also supplies the reading catalogue. The compiled document is [compendium/compendium.pdf](compendium/compendium.pdf).

## Layout

| Location | Purpose |
|---|---|
| `compendium/` | LaTeX reference: one Part per `\qfpart` declaration in the master, one chapter per populated section and one section per specialist pathway with entries |
| `compendium/preamble.tex` | Packages, typography, list spacing and mathematical macros |
| `compendium/house.tex` | Entry environments, citation commands and source references |
| `compendium/front/` | Notation and sources outside the guide catalogue |
| `notes/readings/` | Reading notes by catalogue key |
| `notes/pathways/` | Topic notes, entry links and research questions |
| `notes/artefacts/` | Derivations, numerical checks, protocols and research outputs |
| `notes/entry-evidence.json` | Source-review provenance keyed by entry label |
| `notes/source-review-index.md` | Index of source-review records |
| `notes/source-review-records.md` | Detailed source findings, corrections and verification history |
| `notes/coverage/` | Subject topics and learning objectives, their coverage and prerequisites, and the crosswalk from external topic outlines |
| `notes/log.md` | Reading progress and unresolved questions |
| `notes/tooling/` | Standalone calculator, Python, editor and research-tool notes |
| `tools/check_compendium.py` | Entry, citation, label and pathway-link checks; Part, section and specialist-pathway agreement with the guide; single inclusion of every topic file |
| `tools/check_coverage.py` | Objective and crosswalk structure, coverage report and optional outline hash check |

## Build and check

Prerequisites: [uv](https://docs.astral.sh/uv/) 0.12.7, which installs the pinned Python 3.14.7 from `.python-version`, and a LuaLaTeX installation with `latexmk` for the PDF.

```sh
git clone https://github.com/lixuanguang/Algorithmic-Trading-Notes.git
cd Algorithmic-Trading-Notes
make sync           # install the locked environment from uv.lock
uv run pre-commit install
make source-check   # lock, lint, format, compendium and coverage checks, tests, numerical examples
make check          # source-check, the outline hash check and the PDF build
```

| Target | Runs |
| --- | --- |
| `make lint`, `make format-check`, `make format` | ruff on `tools/` and `notes/artefacts/` |
| `make check-compendium`, `make check-coverage` | the two structural checkers with `--check` |
| `make test` | pytest on `tools/` |
| `make examples` | every `notes/artefacts/*/*check*.py` script, from its own folder, with warnings as errors |
| `make verify-outlines` | the coverage check plus hashes of the local outline copies |
| `make pdf` | `latexmk -lualatex` in `compendium/` |
| `make pre-commit` | every pre-commit hook on all files |

Dependencies are pinned exactly in `pyproject.toml` and resolved in `uv.lock`; after changing them, run `uv lock` and commit both files. Scripts that read spreadsheet data need the `empirical` group: `uv run --group empirical python <script>`. Remote CI runs `make source-check` only after a pull request into `main` is merged, on the merged commit; commits, pushes, opening or updating a pull request, labels and closing a pull request without merging run nothing, so run `make check` and the pre-commit hooks locally before merging. The outline check and the PDF build need git-ignored local copies, so they run locally only. The guide is committed in this repository, so the workflow needs no secrets; it must not switch to a privileged trigger that runs untrusted pull-request code. `make examples` runs in the default environment; scripts that read spreadsheets, directly or through another script (for example `jet_fuel_hedge_test.py` through `backwardation_test.series`), need `--group empirical`.

Catalogue citations link to the reading-list PDF in `guide/`.

## Write an entry

Use `\begin{qf<type>}[Title]\label{<prefix>:<name>}` and the matching end command. Start fields with `\qffield{Statement}`, `\qffield{Conditions}`, and the other relevant content fields. Cite claims with `\citep[locator]{catalogue-key}`. Register sources outside the catalogue using `\qfsource[url]{key}{reference}` in `compendium/front/sources.tex`.

Keep explanations, assumptions, evidence dates and substantive caveats in the entry. Keep verification diaries, study progress and edit history in `notes/`; do not print Status blocks or keyword dumps. See [the compendium conventions](compendium/README.md).

Name files and functions for their subject or operation. Store figures beside their chapter and use paths relative to `compendium/`. `notes/artefacts/` holds derivations, numerical checks, protocols and research outputs; it is not compiled into the reference.

## Chapters and coverage

The `\qfpart{part-key}{Title}{section-key, ...}` declarations in `compendium/compendium.tex` are the single declaration of the compendium's Parts, their sections and the reading order. `make check-compendium` compares them directly with `learning_parts` in `guide/learning_routes.json`: Part keys, titles and order, and each Part's sections and their order, must be the guide's. A chapter folder and its overview note `notes/pathways/<key>.md` must use a declared key; a specialist pathway note may instead use a pathway key of the pinned guide. A section prints once `<key>/section.tex` exists and inputs its topic files, and a Part prints its heading only when one of its sections does; a declared section without content prints nothing. A populated section needs its overview note. To add a subject, write its wrapper, first topic file and overview note together; the key is already declared by the guide.

Within a chapter, each section is one of the guide's specialist pathways for that section, opened in the wrapper by `\qfpathway{pathway-key}{Name}` with the guide's name and in the guide's `specialist_order`. A pathway prints only when it has entries of its own; one without them is omitted, and material it shares with a printed pathway is cross-referenced rather than repeated. Topic files below a pathway start with `\subsection`, except that the only topic file of a pathway has no heading of its own; `\subsubsection` divides a topic. Every topic file, and so every entry, is input exactly once, under the pathway whose outcome covers it; a chapter may open with brief prose in its wrapper, but holds no unnumbered collection of entries. Entries keep their labels when they move; chapter and entry numbers may change. The mapping of entries to pathways and its exceptions are recorded in [subsection_alignment_plan.md](subsection_alignment_plan.md); entries added later are mapped in their batch records, for `return-predictability` in [content_development_plan.md](content_development_plan.md).

The guide's `retired_overviews` keep the keys of divided overviews, `common-toolkit` and `empirical-causal-research`. They are not compendium sections; their notes in `notes/pathways/` are bridges that name each successor section and keep the earlier history.

`notes/coverage/` maps subject objectives to entries and sources, and external topic outlines to objectives; see [its README](notes/coverage/README.md). `make verify-outlines` also hashes the local outline copies in the ignored `reading_materials/outlines/`. Coverage is editorial; it does not record study.

## Update the guide

`guide/` is a plain copy of the tracked files of the `institutional_reading_list` repository, taken at commit `8302467bc5acfedba55c7e79b311cfb2154f433c` (local branch `codex/compendium-pathway-coverage`, 22 October 2026: 227 pathways, five added and eleven broadened so that every compendium subject has a numbered pathway); it is no longer a submodule. The previous copies were `6c7734ed49f1c242908b86a57c4f5d1f0e349ec0` (the eight-Part edition of 22 October 2026, 222 pathways) and `343d145909ba5384202b50604bf5ebe7e5b6ed86`, the edition that notes and review records dated before 22 October 2026 refer to. To update it, export the committed files of a newer commit (`git -C <reading-list> archive <commit>`, not its working tree), replace the contents of `guide/` with them, check that `git write-tree --prefix=guide/` after staging equals the commit's tree, record the commit here and in the commit message, and run `make check`. Compare catalogue and pathway keys using the guide's maintenance instructions before committing; do not edit the copied files here. Local reading PDFs and downloaded research inputs are ignored by Git.
