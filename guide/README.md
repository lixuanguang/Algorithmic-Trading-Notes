# Institutional quantitative-finance reading list

A reference catalogue of 3,956 annotated resources for institutional quantitative research, and a learning guide that turns it into sequenced reading pathways.

| File | What it is |
| --- | --- |
| [Catalogue PDF](institutional_quantitative_finance_reading_list.pdf) | 23 chapters across foundations, methods, markets and research infrastructure. Each entry gives difficulty, resource type, version status and a short annotation. |
| [Learning guide PDF](institutional_quantitative_finance_learning_guide.pdf) | Opens with a study method: a study loop with separate milestones for mastering a pathway and consolidating it into a reference, and layered notes (per reading, per pathway, per concept) with typed entries, house notation with declared overrides and cross-references, with entries written in LaTeX and a tested house file and master file, so that the notes compile into a reference; it also shows how to find what changed between editions. Then 8 parts, 49 sections and 227 pathways. Each section overview lists section goals mapped to its pathways and a narrower overview outcome that its checkpoint tests (some checkpoints are section capstones, taken after named pathways); each pathway has an outcome, prerequisites, ordered readings, a checkpoint and optional branches. Each reading shows its catalogue key and each pathway its key, for naming notes. Clickable DAGs show the study order. |
| [Catalogue notes](catalogue_extended_notes.html) | Searchable extended notes and version records for every entry. |
| [Recency export](catalogue_recency.json) | The version records as structured data. |
| [Editorial records](editorial_backlog.md) | Open leads, plus [bibliographic audit](bibliographic_audit.md), [exclusions](removal_plan.md), [catalogue structure](structural_mapping.md) and the [study-guide migration record](study_guide_migration_plan.md). |

Keep the two PDFs and the HTML file in one folder. Guide links open named destinations in the catalogue PDF (with printed page numbers as a fallback), and catalogue entries link to the HTML notes.

## How the sources fit together

- **[Catalogue source](institutional_quantitative_finance_reading_list.tex)** is the bibliographic authority. Each `\CatalogueEntry` has a stable identifier; keep it when moving an entry. `\ExtendedNote` and `\EntryRecency` records live in the same file and are exported to the HTML and JSON, not printed. Keep each of these commands on one line: a line diff of this file then lists every changed entry, which is how the guide tells note-takers to find changes between editions, and `refresh_views.py` stops if a command spans lines.
- **[learning_routes.json](learning_routes.json)** defines the guide: parts, overview sections, specialist pathways, their readings (by catalogue identifier), prerequisites and checkpoints. Each overview's `section_goals` must map every pathway in its section, and `checkpoint_after` names the pathways a capstone checkpoint needs; the overview's `outcome` is what its checkpoint tests. `specialist_order` must list a section's pathways in the order the section DAG draws them, row by row; the generator stops with the required order if it differs. Prose names other routes as `[[route-id]]` and parts as `[[part:part-id]]`, which print as current numbers, so text survives renumbering; the generator rejects a bare section or part number. `retired_overviews` keeps the keys and legacy labels of overviews that were divided, with their successor sections; their old links land on a short note at the opening of the part that holds the first successor, where `\ref` prints that part's numeral and `\nameref` the retired name. Overviews added since the numbered scheme have no `legacy_label`; each of the labels `route-1` to `route-38` must stay with its original overview key, on a live overview or a bridge.
- **[refresh_views.py](refresh_views.py)** generates the [guide source](institutional_quantitative_finance_learning_guide.tex), the HTML notes and the JSON export, and validates that every reading exists and every prerequisite comes first. It needs only the Python standard library. Do not edit its outputs by hand.

## Keeping entries current

Record publication date, edition or revision, and verification separately; a working-paper upload is not a journal publication. State what was checked (metadata, abstract or full text) and leave unknowns explicit rather than inferring dates. Each entry's review policy suggests a cadence: quarterly for rules, protocols, software and preliminary papers; per vintage for changing data; annually for published research and books. To list the entries changed between two commits, diff the catalogue source by line rather than `catalogue_recency.json`, which does not change when only an annotation does; the guide's "Maintaining the compendium" prints the commands.

## Rebuilding

```sh
latexmk -pdf institutional_quantitative_finance_reading_list.tex   # catalogue first: the guide reads its .aux for page numbers
python3 refresh_views.py
latexmk -pdf institutional_quantitative_finance_learning_guide.tex
```

`catalogue_link_target` in the route file is `pdf`; set it to `html` to link guide readings to the HTML notes when you are not exporting PDFs. The `as_of` field sets the guide's edition date.

After rebuilding, check that both logs have no undefined references, that the guide has no overfull boxes, that every guide link resolves to a named destination in the catalogue PDF, and that the printed page numbers match the catalogue's `.aux`. Look over the rendered DAG pages. These checks confirm the documents are built correctly, not that the sources' claims are right.
