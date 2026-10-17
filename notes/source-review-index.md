# Source-review index

The reference content is in `compendium/`. Detailed source findings, numerical checks, corrections, input identities and limitations are in [source-review-records.md](source-review-records.md). Entry-level review provenance is keyed by the stable LaTeX label in [entry-evidence.json](entry-evidence.json).

Research protocols and outputs are stored under `artefacts/<topic>/`; reading notes and pathway notes link to the relevant entries. Historical records retain dates and evidence identities. Descriptive filenames and topic names replace numbered editing identifiers. Renaming a record does not renew its verification.

Use `python3 tools/check_compendium.py --check` from the repository root to check entry structure and references. It does not verify source claims or measure learning progress.
