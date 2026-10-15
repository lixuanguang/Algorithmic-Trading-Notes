---
key: price-impact-execution
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Price impact, optimal execution and implementation shortfall

Pathway outcome, from the guide: estimate a price-impact model from executions, derive an optimal schedule and measure implementation shortfall with confidence intervals.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 15 October 2026 by migration slice 7 (`notes/migration.md`), when three entries on price impact were migrated from the legacy liquidity-and-market-impact file into the new canonical chapter `compendium/execution-trading-costs/`. The entries were checked against Webster's handbook (`wide-webster-price-impact`, a required reading of this pathway) and against Bouchaud, Bonart, Donier and Gould (`catalogue-0528`, on no route). That is migration and source checking, not study of the readings. Gatheral (`catalogue-0501`) and the propagator paper (`wide-bouchaud-propagator`), both required readings, were not consulted; the entries cite them only through these books.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 7, 2026-10-15:

- `def:price-impact`: unperturbed, observed and trade prices; reaction, observed and prediction impact; transient and permanent impact; the "temporary impact" ambiguity.
- `mod:propagator`: the propagator model of transient impact; response function and sign autocorrelation.
- `res:no-price-manipulation`: price manipulation as a round trip with negative expected cost; Webster's Obizhaeva–Wang example and the condition 2β+γ′>0; the closed-trajectory cost in the latent-liquidity model.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`, where the migration has kept every removed block.

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. The blocks exclusive to this pathway are in `compendium/legacy/execution-trading-costs/`. The legacy file `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/05_market_impact_models.tex` repeats propagator and permanent-impact material that belongs with the entries above (see `notes/migration.md`, next bounded slice).

## What changed in my view or practice

## Questions carried forward

- Gatheral's (2010) conditions on decay kernels and Fruth, Schöneborn and Urusov's (2013) condition are cited through Webster only. Check both against the papers.
- Is permanent impact identifiable at all beyond the horizon where price variance swamps the signal (`catalogue-0528`, p. 240)? Which design does `wide-bacry-life-cycle` use?
