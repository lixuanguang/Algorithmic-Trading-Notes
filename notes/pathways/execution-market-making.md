---
key: execution-market-making
section: execution-market-making
status: not started (draft entries from the migration only)
---

# Market microstructure and market making (section overview)

Overview outcome, from the guide: evaluate a quoting policy on an order-book replay by fill probability, adverse selection and inventory risk, and state how the result depends on queue-position and self-impact assumptions. The overview's readings are `alpha-harris`, `s6-hasbrouck`, `s6-stoikov`, `exp-cont-kukanov-order-placement`, `exp-huang-lehalle-rosenbaum-queue-reactive` and `exp-noble-rosenbaum-souilmi-reality-gap`; read them for orientation before the section's pathways. Its checkpoint is not marked as a section capstone.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 15 October 2026 by migration slice 5 (`notes/migration.md`), because the guide runs one study loop per section overview and this route had no note. It lists the migrated entries that serve the overview route rather than a specialist pathway. Until then they were listed provisionally in `market-making-lob.md`. They come from migration and source checking against Harris (`alpha-harris`) and Hasbrouck (`s6-hasbrouck`), two of this route's readings, and against Lehalle and Laruelle (`alpha-laruelle`), which is on no route. None of it is study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Moved here from `market-making-lob.md` on 2026-10-15; written in migration slices 3 and 4:

- `def:spread-measures`: quoted, inside, relative, effective and realised spreads (Harris, Hasbrouck).
- `res:roll-spread-estimator`: Roll's serial-covariance estimator and its biases (Harris, Hasbrouck).
- `res:spread-component-identification`: transitory and permanent components; the generalized Roll model; inventory versus information (Harris, Hasbrouck).
- `res:spread-determinants`: Harris's primary and secondary spread determinants and the order-driven equilibrium spread.
- `def:outside-spread`: value traders' outside spread (Harris); changed in slice 5 (profit sources, the no-trade band, not trading as a decision).
- `def:volatility-components`: fundamental and transitory volatility; the random-walk decomposition (Harris, Hasbrouck).
- `meth:garman-klass-volatility`: range-based intraday volatility as Lehalle and Laruelle use it (the 1980 paper not consulted).
- `meth:spread-volatility-regression`: spread on volatility in levels and logs, with the retransformation correction (Lehalle and Laruelle).
- `mech:bubble-crash-dynamics`: how bubbles build and crashes unwind; the price accelerator; crash attribution (Harris).

Written in migration slice 5, 2026-10-15:

- `def:fundamental-value`: fundamental value, market value and noise; public, private and stale information (Harris; contrasted with Hasbrouck's efficient price).
- `res:informed-trading-aggregation`: informed trading makes prices informative; the price as an average of forecasts; correlated errors (Harris).
- `def:market-efficiency`: weak, semistrong and strong forms and the cost-sensitive definition; the market paradox; the information–liquidity trade-off (Harris).
- `def:inside-information`: inside information, who may not trade on it, and signal permission (Harris, U.S. law as of 2002).
- `def:price-formation-process`: the price formation process as immediate impact and decay (Lehalle and Laruelle).
- `def:intraday-overnight-returns`: intraday, overnight and close-to-close returns, volatility and correlation by time scale (Lehalle and Laruelle).

Slice 5 also added cross-references to `def:volatility-components` and `meth:garman-klass-volatility`.

All fifteen: verification partly checked 2026-10-15, stability draft. Human review is outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`, where the migration has kept every removed block since the pilot.

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The route is a candidate for most files in `compendium/legacy/execution-market-making/01_...` to `03_...`. In slice 5 the information-and-market-efficiency file was migrated and deleted, and nine of the twelve price-discovery blocks were migrated. The other three are assigned elsewhere: fragmentation and outage to `market-structure-execution-quality`, fast liquidity to `hft-market-design`. The next bounded slice is the strategic-trading-models file (`notes/migration.md`).

## What changed in my view or practice

## Questions carried forward

- Harris's fundamental value conditions on all information known to anyone; Hasbrouck's efficient price on public information only. Which one does each later entry (Kyle, Glosten–Milgrom, the spread decompositions) use?
- The legal details in `def:inside-information` are U.S. law as of 2002 and were not checked against current law. Which current sources should replace them, and does any pathway own that material?
- Lehalle and Laruelle attribute part of the 2010 rise in extraday correlation to a less noisy intraday price formation process and to high-frequency trading (p. 177). Is there evidence beyond their figures?
