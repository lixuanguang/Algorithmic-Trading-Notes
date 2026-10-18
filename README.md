# All Things on Quantitative Trading

A source-based reference on quantitative trading and the financial analysis behind it. Its chapters follow the ordered section list in `compendium/compendium.tex`; the institutional learning guide pinned in `guide/` supplies the reading catalogue and specialist pathways. The compiled document is [compendium/compendium.pdf](compendium/compendium.pdf).

## Layout

| Location | Purpose |
|---|---|
| `compendium/` | LaTeX reference, one chapter per populated section of the master's `\qfsections` list |
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
| `tools/check_compendium.py` | Entry, citation, label and pathway-link checks |
| `tools/check_coverage.py` | Objective and crosswalk structure, coverage report and optional outline hash check |

## Build and check

Prerequisites: [uv](https://docs.astral.sh/uv/) 0.12.7, which installs the pinned Python 3.14.7 from `.python-version`, and a LuaLaTeX installation with `latexmk` for the PDF.

```sh
git clone --recurse-submodules https://github.com/lixuanguang/Algorithmic-Trading-Notes.git
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

Dependencies are pinned exactly in `pyproject.toml` and resolved in `uv.lock`; after changing them, run `uv lock` and commit both files. Scripts that read spreadsheet data need the `empirical` group: `uv run --group empirical python <script>`. CI runs `make source-check` when a pull request into `main` is labelled `ready-to-merge`; the outline check and the PDF build need git-ignored local copies, so they run locally. The workflow checks out the private guide with a read-only `GUIDE_READ_TOKEN` repository secret. GitHub passes no secrets other than `GITHUB_TOKEN` to workflows triggered from a forked repository, so CI can validate only pull requests from branches of this repository; supporting forks would be a separate decision, and the workflow must not switch to a privileged trigger that runs untrusted pull-request code. `make examples` runs in the default environment; scripts that read spreadsheets, directly or through another script (for example `jet_fuel_hedge_test.py` through `backwardation_test.series`), need `--group empirical`.

For an existing clone, initialise the guide with `git submodule update --init`. Catalogue citations link to its PDF in `guide/`.

## Write an entry

Use `\begin{qf<type>}[Title]\label{<prefix>:<name>}` and the matching end command. Start fields with `\qffield{Statement}`, `\qffield{Conditions}`, and the other relevant content fields. Cite claims with `\citep[locator]{catalogue-key}`. Register sources outside the catalogue using `\qfsource[url]{key}{reference}` in `compendium/front/sources.tex`.

Keep explanations, assumptions, evidence dates and substantive caveats in the entry. Keep verification diaries, study progress and edit history in `notes/`; do not print Status blocks or keyword dumps. See [the compendium conventions](compendium/README.md).

Name files and functions for their subject or operation. Store figures beside their chapter and use paths relative to `compendium/`. `notes/artefacts/` holds derivations, numerical checks, protocols and research outputs; it is not compiled into the reference.

## Chapters and coverage

The ordered `\qfsections` list in `compendium/compendium.tex` declares every compendium section and its place in the reading order. A chapter folder and its overview note `notes/pathways/<key>.md` must use one of those keys; a specialist pathway note may instead use a pathway key of the pinned guide. A section prints once `<key>/section.tex` exists and inputs its topic files; a declared section without content prints nothing. To add a subject, add its key to the list and write its wrapper, first topic file and overview note together.

`notes/coverage/` maps subject objectives to entries and sources, and external topic outlines to objectives; see [its README](notes/coverage/README.md). `make verify-outlines` also hashes the local outline copies in the ignored `reading_materials/outlines/`. Coverage is editorial; it does not record study.

## Update the guide

```sh
cd guide
git fetch
git checkout <commit>
cd ..
git add guide
git commit -m "Update learning guide"
```

Compare catalogue and pathway keys using the guide's maintenance instructions before committing. Local reading PDFs and downloaded research inputs are ignored by Git.
