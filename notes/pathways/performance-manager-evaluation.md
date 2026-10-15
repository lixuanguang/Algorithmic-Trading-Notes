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

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The rest of this pathway's candidates are in `compendium/legacy/rates-credit-mortgages/`.

## What changed in my view or practice

## Questions carried forward

- Was it right to route these four blocks here rather than to a map candidate? The map listed only the execution pathways.
- Harris's realised alpha omits the risk-free rate and uses concurrent betas; the legacy regression form is Jensen's alpha. Which does the pathway's checkpoint (Carhart alphas) need, and how should smoothing be corrected (`wide-getmansky-lo-makarov`, unread)?
