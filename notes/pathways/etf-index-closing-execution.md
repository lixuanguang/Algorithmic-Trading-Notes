---
key: etf-index-closing-execution
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# ETFs, index events and closing auctions

Pathway outcome, from the guide: plan trades around ETF creations, index reconstitutions and the closing auction, estimating price pressure, reversal and the cost borne by index funds. Its checkpoint takes one index reconstitution, measures abnormal returns, volume and closing-auction imbalance for added and deleted stocks, and compares executing an index fund's trades in the closing auction with a VWAP schedule over the prior week. Its twelve readings begin with ETF mechanics (`ex-lettau-madhavan-2018`) and theory (`wide-pan-zeng-etf`), then evidence on ETF trading, index inclusion and closing auctions.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 18 (`notes/migration.md`), which routed the ETF-product and creation-redemption blocks of the legacy equity-market-microstructure file here, outside that file's map candidate (`market-structure-execution-quality`), because this pathway's outcome names ETF creations. The entry comes from migration and source checking against the working-paper versions of the pathway's first two readings and Harris (2002), read only in the passages the entry cites. That is not study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 18, 2026-10-15:

- `mech:etf-creation-redemption`: authorised participants, creation units, in-kind and cash baskets, creation and redemption against secondary trading, arbitrage that tends to align price and value without guaranteeing it, stale reference values, APs' discretion, and Pan and Zeng's liquidity-mismatch evidence for corporate bond ETFs; index products as Harris lists them (2001–2002).

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/etf-index-closing-execution/derivations.tex`.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:portfolio-trading` (`execution-trading-costs`); `ev:index-reconstitution-impact` (`price-impact-execution`).

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Check the entry against the published *Journal of Economic Perspectives* version of Lettau and Madhavan (the working paper of January 2018 was used) and against a published version of Pan and Zeng if one exists (the ESRB working paper of December 2017 was used).
- Current SEC rules on ETF baskets and creation (Rule 6c-11) were not checked.
