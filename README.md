# All Things on Quantitative Trading

A source-based quantitative trading reference, organised by the institutional learning guide pinned in `guide/`. The compiled document is [compendium/compendium.pdf](compendium/compendium.pdf).

## Layout

| Location | Purpose |
|---|---|
| `compendium/` | LaTeX reference, with one chapter per guide section |
| `compendium/preamble.tex` | Packages, typography, list spacing and mathematical macros |
| `compendium/house.tex` | Entry environments, citation commands and source references |
| `compendium/front/` | Notation and sources outside the guide catalogue |
| `notes/readings/` | Reading notes by catalogue key |
| `notes/pathways/` | Topic notes, entry links and research questions |
| `notes/artefacts/` | Derivations, numerical checks, protocols and research outputs |
| `notes/entry-evidence.json` | Source-review provenance keyed by entry label |
| `notes/source-review-index.md` | Index of source-review records |
| `notes/source-review-records.md` | Detailed source findings, corrections and verification history |
| `notes/log.md` | Reading progress and unresolved questions |
| `notes/tooling/` | Standalone calculator, Python, editor and research-tool notes |
| `tools/check_compendium.py` | Entry, citation, label and pathway-link checks |

## Build and check

```sh
git clone --recurse-submodules https://github.com/lixuanguang/Algorithmic-Trading-Notes.git
cd Algorithmic-Trading-Notes
python3 tools/check_compendium.py --check
python3 -m unittest discover -s tools
cd compendium
latexmk -lualatex compendium.tex
```

For an existing clone, initialise the guide with `git submodule update --init`. Catalogue citations link to its PDF in `guide/`.

## Write an entry

Use `\begin{qf<type>}[Title]\label{<prefix>:<name>}` and the matching end command. Start fields with `\qffield{Statement}`, `\qffield{Conditions}`, and the other relevant content fields. Cite claims with `\citep[locator]{catalogue-key}`. Register sources outside the catalogue using `\qfsource[url]{key}{reference}` in `compendium/front/sources.tex`.

Keep explanations, assumptions, evidence dates and substantive caveats in the entry. Keep verification diaries, study progress and edit history in `notes/`; do not print Status blocks or keyword dumps. See [the compendium conventions](compendium/README.md).

Name files and functions for their subject or operation. Store figures beside their chapter and use paths relative to `compendium/`. `notes/artefacts/` holds derivations, numerical checks, protocols and research outputs; it is not compiled into the reference.

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
