# All Things on Quantitative Trading

A structured notes repository for quantitative trading. The notes compile into one LaTeX reference, `compendium/compendium.pdf`, organised by the sections and pathways of the institutional quantitative finance learning guide, which this repository pins as a submodule in `guide/`.

The goal is to keep the notes practical, source-aware, and concise: books are integrated into the relevant sections rather than summarized chapter by chapter. The guide's *How to study with this guide* sets out the method: reading notes, pathway notes, and typed compendium entries that cite readings by catalogue key.

## Layout

```
guide/                                  the learning guide and catalogue, pinned as a git submodule
notes/readings/<catalogue-key>.md       one note per reading
notes/pathways/<pathway-key>.md         one note per pathway, with its entry backlog
notes/artefacts/<pathway-key>/          checkpoint code, derivations and data vintages
notes/log.md                            coverage log, reading progress and open questions
notes/migration.md                      migration record: conventions, status, slice index and map of legacy files to pathways
notes/migration-slices.md               each slice's full record: sources, checks, dispositions, counts and build
notes/tooling/                          calculator, reading AI papers, Python and VS Code; compiles on its own
notes/legacy-references.bib             the old BibTeX file; nothing reads it now
compendium/compendium.tex               master file: one chapter per guide section, in the guide's order
compendium/preamble.tex                 your own packages, macros and the older environments
compendium/house.tex                    entry environments, \citep and \qfsource, copied from the guide
compendium/front/                       notation list and overrides, preface, and sources outside the catalogue
compendium/<section-key>/section.tex    a chapter's heading and pathway keys, then its topic files of entries
compendium/<section-key>/figures/       that chapter's figures
compendium/legacy/<section-key>/        notes awaiting migration, compiled as the final part (temporary)
tools/migration_status.py               migration progress and entry metadata checks, with its tests
```

A chapter appears in the PDF once `compendium/<section-key>/section.tex` exists; `compendium.tex` already lists every section key of the guide. The legacy folders were a temporary convention of this repository, not part of the guide's layout: `compendium/legacy/part.tex` compiled them after the main chapters, and each folder was deleted once its blocks were migrated. The migration finished on 16 October 2026 (slice 37): no legacy chapter remains, `part.tex` is gone, and only `compendium/legacy/execution-trading-costs/figures/` (21 unused figures) is left; the original texts are in `notes/artefacts/`.

## Building

```
git clone --recurse-submodules https://github.com/lixuanguang/Algorithmic-Trading-Notes.git
cd Algorithmic-Trading-Notes/compendium
latexmk -pdf compendium.tex
```

In an existing clone, run `git submodule update --init` once to fetch `guide/`. Citations of catalogue keys link to the catalogue PDF in `guide/`.

## Writing

- **Entries.** Write each new entry as `\begin{qf<type>}[Title]\label{<prefix>:<name>}` … `\end{qf<type>}`, with fields started by `\qffield{Statement}` and so on, using the eleven types and label prefixes in the guide.
- **Citations.** Cite as `\citep[locator]{catalogue-key}`, one key per citation. Give a source outside the catalogue a `\qfsource{key}{reference}` line in `compendium/front/sources.tex` and cite its key the same way.
- **Figures.** Keep figures in `compendium/<section-key>/figures/` and reference them from `compendium/`, as in `\includegraphics{execution-market-making/figures/name}`.
- **Older notes.** The chapters written before the study method are in `compendium/legacy/` and compile as the final part, *Notes awaiting migration*. Their blocks use the environments in `preamble.tex` (`definition`, `taxonomy`, `principle`, `mechanism`, `caveat` and others), and are retyped into the guide's entry types, labelled and cited at the claim when each pathway is consolidated. The `mechanism` environment means an economic mechanism, while the guide's Mechanism type covers contract terms and settlement, so retype each block by its content rather than its environment name. The plan is in [compendium/README.md](compendium/README.md) and the record of what has moved, with the map of legacy files to pathways, in [notes/migration.md](notes/migration.md). Check progress and entry metadata with `python3 tools/migration_status.py --check`.

## Moving to a newer edition of the guide

```
cd guide && git fetch && git checkout <commit> && cd ..
git add guide && git commit -m "Move to guide <commit>"
```

Before committing, run the comparison in the guide's *Maintaining the compendium* to list the catalogue keys and pathway keys to revisit.

## Reading progress

Progress through the books read before the study method is in `notes/log.md`, with each book's catalogue key and the chapters that hold its material.

`reading materials/` is a local folder of PDFs and is ignored by git.
