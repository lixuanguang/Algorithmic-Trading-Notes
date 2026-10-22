# Subject coverage

This folder records which financial capabilities the compendium teaches, how they are sequenced, and how external topic outlines map onto them. Topics and objectives are named for financial subjects and operations. Outline providers, editions, levels and reading numbers appear only as source metadata.

| File | Holds |
| --- | --- |
| [objectives.json](objectives.json) | Canonical topics (owning chapter, scope, prerequisite topics) and learning objectives (operations, depth, entries, candidate entries, coverage, missing requirement, next action, evidence) |
| [outline-manifest.json](outline-manifest.json) | The eight supplied outline files: neutral id, full SHA-256, local path, page and item counts, provider, edition and level as metadata, original filename as provenance |
| [outline-crosswalk.json](outline-crosswalk.json) | 203 outline modules and 1,030 items, each paraphrased with its command verbs and page locators and mapped to one or more objectives |
| [learning-roadmap.md](learning-roadmap.md) | Prerequisite order of the topics, from foundations to client decisions, and the two worked source-to-entry journeys |
| [source-changes.md](source-changes.md) | Comparisons between outline editions and their effect on objectives |

Run `make check-coverage` (`uv run python tools/check_coverage.py --check`) for the current counts by chapter and by outline component; `make verify-outlines` also hashes the local outline copies. The report, not this page, is the place to read coverage figures.

## Legend

- **Coverage** of an objective: `missing` (no entry reviewed against it), `partial` (an entry covers some operations; `missing` says which part remains), `covered` (a reviewed entry performs every operation at the stated depth, with substantive sources, review evidence and, for a calculation, a worked example). Mapped entries must be typed entries; their entry-evidence records and the objective's evidence must name the same entries, and each listed source must be cited by one of them. Sources read only to check an entry go under `review_sources`.
- **Next action**: `review` (inspect the candidate entries first), `extend` (add the missing part to a mapped entry), `write` (find and read sources, then write), `obtain-source` (a named source is needed before anything can be written), `reuse` (an entry is believed sufficient but the mapping is not yet confirmed). Covered objectives have none.
- **Depth**: `foundation` (definition, units, mechanics, a calculation or interpretation), `analysis` (application, competing methods, diagnostics, sensitivity), `decision` (constraints, alternatives and a justified recommendation). These describe the capability, not an examination level.
- An **outline item** is covered only when its mapping has a review date (`reviewed`), every objective it maps to is covered and its `residual_gap` is empty; an unreviewed mapping to covered objectives reports `partial`. Each active outline's item and module occurrences, shared-core copies included, must equal the manifest's counts. Item coverage and objective coverage are reported separately; several items can map to one objective.

Candidate entries are existing labels found by subject search during the inventory. They have not been read against the objective; until they are, the objective stays `missing`.

## Limits

- The supplied files are topic outlines, not readings. They define scope; they are never cited as the source of an explanation, derivation or rule.
- Outline items are paraphrased in our own words with their command verbs; the outline text itself is not reproduced. Module headings are kept as printed, as locators.
- The PDFs are kept under the git-ignored `reading_materials/outlines/`, so a fresh clone cannot run `--verify-outlines` until the files are supplied again.
- Editorial coverage is not study. Mastery and consolidation dates are recorded only in `notes/log.md`, from the reader's own work.

## Likely source needs by subject (candidates, not reviewed)

Inventory of 18 October 2026. These are categories to search when each batch starts, not documents found or read.

| Subject | Existing reviewed material | Likely sources to look for |
| --- | --- | --- |
| Quantitative foundations | Harris (skill-luck tests), GARCH, covariance entries | Open statistics and econometrics texts; original papers for tests and bootstrap |
| Economics | Gliner and central-bank material in the macro and rates chapters | Central-bank and IMF/WTO/World Bank publications; open economics texts |
| Financial statements | IAS 7 and IFRS 18 (EU-adopted text), ASU 2016-15 for Topic 230, an open accounting text | Further IAS/IFRS standards in EU-adopted form; FASB Accounting Standards Updates (free PDFs; the Codification itself needs a login); issuer filings for cases |
| Corporate finance | None | Open corporate-finance texts; original Modigliani-Miller and payout papers; governance codes |
| Equity valuation | Index-valuation screen only | Damodaran's public notes and datasets; Ohlson and residual-income papers (in the guide catalogue) |
| Fixed income and derivatives | Rates, duration, CDS and option-pricing entries | Treasury and central-bank conventions; ISDA documentation; original model papers |
| Alternatives | Commodity and crypto entries | ILPA and fund documents; NCREIF and REIT index rules; academic private-equity performance papers (some in the catalogue) |
| Portfolio and performance | GIPS 2020, Harris, mean-variance and Black-Litterman entries | Original allocation, attribution and fundamental-law papers; pension and insurer regulations |
| Professional ethics | None | The current code and standards and their handbook from the issuing body; the asset manager code; regulators' conduct rules for contrast |
| Private wealth | None | Jurisdiction-specific tax and estate law, dated; academic life-cycle and human-capital papers |
