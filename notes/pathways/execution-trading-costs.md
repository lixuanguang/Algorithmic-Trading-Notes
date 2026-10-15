---
key: execution-trading-costs
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Execution, trading costs and market structure (section overview)

Overview outcome, from the guide: plan the execution of an equity order, a futures roll and a bond trade, estimate expected cost and its uncertainty from a stated impact model, and split realised implementation shortfall into spread, impact, timing and fees under the rules in force. The overview's readings are `wide-perold-shortfall`, `alpha-almgren`, `catalogue-0504`, `ex-goyal-jegadeesh-wu-2026`, `wide-bsv-fi-survey` and `exp-fx-algos`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 10 (`notes/migration.md`), because the guide runs one study loop per section overview and the optimal-execution blocks of the legacy notes belong to this overview rather than to a specialist pathway: its outcome asks for a schedule and an expected cost with its uncertainty from a stated impact model, and `alpha-almgren` is one of its readings. The entries come from migration and source checking against Lehalle and Laruelle (`alpha-laruelle`, on no route), the Almgren–Chriss author preprint of December 2000 (`alpha-almgren`, selected passages) and Harris (`alpha-harris`). That is not study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 10, 2026-10-15:

- `mod:almgren-chriss-execution`: mean–variance optimal execution; the Almgren–Chriss closed form and Lehalle and Laruelle's discrete version with power-law temporary impact; expectation-only, variance-only and mean–variance schedules.
- `def:block-trade`: block trades and the four problems of arranging them (Harris).

Both: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`. The impact concepts they use (price impact and its empirical estimation) are owned by `price-impact-execution` and are cross-referenced from the entries, not listed here.

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The rest of `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/` is shared between this overview and its specialist pathways; decide each block's owner when its file is migrated.

## What changed in my view or practice

## Questions carried forward

- Lehalle and Laruelle's appendix mixes two timing conventions (price step (A.16) against the terminal conditions (A.27)); the entry uses the Almgren–Chriss convention. Is the book's Figure A.11 computed under either?
- The journal version of Almgren and Chriss (2001) has not been compared with the December 2000 preprint.
