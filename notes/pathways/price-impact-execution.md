---
key: price-impact-execution
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Price impact, optimal execution and implementation shortfall

Pathway outcome, from the guide: estimate a price-impact model from executions, derive an optimal schedule and measure implementation shortfall with confidence intervals.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 15 October 2026 by migration slice 7 (`notes/migration.md`), when three entries on price impact were migrated from the legacy liquidity-and-market-impact file into the new canonical chapter `compendium/execution-trading-costs/`. The entries were checked against Webster's handbook (`wide-webster-price-impact`, a required reading of this pathway) and against Bouchaud, Bonart, Donier and Gould (`catalogue-0528`, on no route). That is migration and source checking, not study of the readings. Gatheral (`catalogue-0501`) was not consulted and is cited only through Webster. In slice 8 three required readings were read in open versions for source checking: `alpha-almgren` (author preprint of December 2000), `wide-bouchaud-propagator` (arXiv cond-mat/0307332v2) and `wide-bacry-life-cycle` (arXiv preprint of December 2014); their journal versions and pagination were not checked. In slice 9 `wide-almgren-direct-impact` was read in the authors' preprint of 10 May 2005; `wide-toth-square-root` remains unread.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 7, 2026-10-15:

- `def:price-impact`: unperturbed, observed and trade prices; reaction, observed and prediction impact; transient and permanent impact; the "temporary impact" ambiguity.
- `mod:propagator`: the propagator model of transient impact; response function and sign autocorrelation.
- `res:no-price-manipulation`: price manipulation as a round trip with negative expected cost; Webster's Obizhaeva–Wang example and the condition 2β+γ′>0; the closed-trajectory cost in the latent-liquidity model.

Written in migration slice 8, 2026-10-15, from the legacy market-impact-models file:

- `ev:square-root-impact`: the square-root law of metaorder impact, its range and conditions (`catalogue-0528`; confirmed in `wide-bacry-life-cycle`).
- `meth:post-execution-impact-profile`: Bacry et al.'s debiasing for later metaorders and index decomposition of post-execution prices.

Changed in slice 8: `def:price-impact` (model families from the Almgren–Chriss original; the three meanings of "temporary impact"; mechanical and informational views of permanent impact) and `mod:propagator` (the 2004 original read; kernel shapes and the fine balance; order splitting as the source of sign memory; legacy departures corrected).

Written in migration slice 9, 2026-10-15, from the legacy price-impact-estimation file:

- `ev:intraday-impact-profile`: the impact path during and after execution, and its dependence on participation and duration (`alpha-laruelle`; `wide-bacry-life-cycle`).
- `meth:almgren-impact-estimation`: Almgren et al.'s direct estimation of permanent and temporary impact from Citigroup orders (`wide-almgren-direct-impact`, preprint).
- `meth:order-flow-impact-regression`: the Glosten–Harris order-flow regression (`alpha-harris`, `s6-hasbrouck`).
- `ev:index-reconstitution-impact`: Russell reconstitution price pressure and reversal (`alpha-harris`, after Madhavan, not consulted).

Changed in slice 9: `def:price-impact` (execution-time measurement; timing), `ev:square-root-impact` (Almgren et al.'s 3/5 exponent; Bacry et al.'s duration factor), `meth:post-execution-impact-profile` (Lehalle and Laruelle's restatement of the procedure).

All nine: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`, where the migration has kept every removed block.

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The blocks exclusive to this pathway are in `compendium/legacy/execution-trading-costs/`. The legacy market-impact-models file was migrated and deleted in slice 8, and the price-impact-estimation file in slice 9. In slice 10 the optimal-execution-problem file, shared with the section overview, was migrated to entries owned by `execution-trading-costs` (see that note), cross-referencing this pathway's impact entries. No legacy block is now a candidate of this pathway alone; its 27 remaining candidates (after slice 10) are shared, the nearest in `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/`.

## What changed in my view or practice

## Questions carried forward

- Gatheral's (2010) conditions on decay kernels and Fruth, Schöneborn and Urusov's (2013) condition are cited through Webster only. Check both against the papers.
- Is permanent impact identifiable at all beyond the horizon where price variance swamps the signal (`catalogue-0528`, p. 240)? Which design does `wide-bacry-life-cycle` use?
