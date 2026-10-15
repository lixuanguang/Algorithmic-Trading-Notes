---
key: performance-manager-evaluation
section: portfolio-construction-risk
status: not started (draft entries from the migration only)
---

# Performance attribution and manager evaluation

Pathway outcome, from the guide: attribute returns, adjust for factor exposure, smoothing and survivorship, and estimate how much apparent skill is luck. Its readings include `wide-sharpe-1994`, `wide-brinson-attribution`, `wide-carhart`, `wide-fama-french-luck` and `wide-getmansky-lo-makarov`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 13 (`notes/migration.md`). Four blocks of the legacy execution file on transaction cost analysis (performance measurement, risk-adjusted excess return, selection and timing, smoothed returns) evaluate managers, not executions; neither of that file's map candidates (`execution-trading-costs`, `market-structure-execution-quality`) has that outcome, and this pathway's names factor adjustment and smoothing. The entry comes from source checking against Harris (`alpha-harris`, chap. 22), not from this pathway's readings. That is not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 13, 2026-10-15:

- `meth:relative-performance-evaluation`: total, holding-period and internal rates of return; market-adjusted and risk-adjusted returns; Harris's decomposition into excess return, market timing and market; return smoothing.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`; it sits in `compendium/portfolio-construction-risk/`, the canonical chapter for this pathway's section, opened by this slice.

Written in migration slice 31, 2026-10-15, from the *Return Metrics* block of the unsourced legacy time-value file (`rates-credit-mortgages/01_tvm.tex`):

- `def:return-measures`: GIPS 2020 definitions of time- and money-weighted returns, external cash flows, gross and net of fees; cumulative, geometric-mean and annualised returns; IRR existence and multiple roots; real and leveraged returns. The legacy's malformed TWR root and its unexplained "risk" factor in the real return are corrected; formulas derived and checked numerically.

Partly checked 2026-10-15, draft; human review outstanding. Artefact: `notes/artefacts/rates-credit-mortgages/time-value.tex`.

## Entry backlog

- meth:gips-composite-presentation: composite construction, required statistics and disclosures for a GIPS report, as the checkpoint asks (`wide-gips-2020`, read only for definitions).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 31 migrated `compendium/legacy/rates-credit-mortgages/01_tvm.tex` and removed that legacy chapter; no legacy file now lists this pathway. That says nothing about consolidation.

## What changed in my view or practice

## Questions carried forward

- Was it right to route these four blocks here rather than to a map candidate? The map listed only the execution pathways.
- Harris's realised alpha omits the risk-free rate and uses concurrent betas; the legacy regression form is Jensen's alpha. Which does the pathway's checkpoint (Carhart alphas) need, and how should smoothing be corrected (`wide-getmansky-lo-makarov`, unread)?
