---
key: market-structure-execution-quality
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Market structure rules, fees and execution quality

Pathway outcome, from the guide: explain how fragmentation, dark trading, fees, tick size, odd lots, retail routing and trading hours affect execution quality, and track the 2024–2026 U.S. and EU rule changes. Its checkpoint measures effective and realised spreads and price improvement on Rule 605-style data by order size and venue type. Its readings include `ex-sec-rule605-2024` and `ex-sec-withdrawal-2025` (best-execution proposals withdrawn in 2025).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 13 (`notes/migration.md`), because the legacy transaction-cost file's best-execution, retail execution-quality and broker-conflict blocks belong to this pathway's outcome (retail routing and execution quality) rather than to the overview. The entries come from migration and source checking against Harris (`alpha-harris`, 2002) and Kissell (`s7-kissellscience`, on no route); their rules and figures are as of 2002 and 2014, and none of this pathway's readings has been read. That is not study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 13, 2026-10-15:

- `def:best-execution`: Harris's three standards of best execution, speed and price as dimensions of execution quality, NBBO and price-improvement practice, Rules 11Ac1-5 and 11Ac1-6 (as of 2002), and Kissell's process definition.
- `def:broker-agency-conflicts`: the broker principal–agent problem; dual trading and internalisation, order preferencing and payment for order flow, soft dollars and directed brokerage, dishonest practices; venue rebates (Kissell).

Both: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`. The spread measures they use are owned by `execution-market-making` and cross-referenced, not listed here.

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. This pathway has three blocks assigned to it and others exclusive to it in `compendium/legacy/`; most of its candidates are shared with the microstructure overview.

## What changed in my view or practice

## Questions carried forward

- The regulatory statements in `def:best-execution` predate Rules 605 and 606 as amended in 2024 and the 2025 withdrawal; update them from `ex-sec-rule605-2024` and `ex-sec-withdrawal-2025`.
