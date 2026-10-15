---
key: hft-market-design
section: execution-market-making
status: not started (draft entries from the migration only)
---

# High-frequency trading, speed and adverse selection

Pathway outcome, from the guide: evaluate how speed, latency races and fast arbitrage affect liquidity, price discovery and the costs borne by slower traders. Its checkpoint identifies latency races at stale quotes in message data for one stock or futures contract, measures their share of volume and of the effective spread, compares liquidity on days with more and fewer races, and asks whether the evidence points to overinvestment in speed or to faster price discovery. Its readings run from Menkveld's survey (`wide-menkveld-hft-review`) through the evidence on liquidity and price discovery, the theory of fast trading and latency races (`ex-biais-foucault-moinas-2015`, `wide-budish-cramton-shim`), race measurement (`exp-aquilina-budish-oneill-races`), toxic arbitrage, VPIN and its critique, to the Flash Crash.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 15 (`notes/migration.md`), which migrated the legacy high-frequency-trading-strategies file. That file's map named `execution-trading-costs` and `market-structure-execution-quality`; its three blocks were routed here because they classify HFT strategies, describe the speed race and ask how HFT should be judged by other traders' costs, which is this pathway's outcome. The entries come from migration and source checking against the SEC's 2010 concept release, Lehalle and Laruelle (`alpha-laruelle`, 2018 printing) and the published version of `wide-budish-cramton-shim`, one of this pathway's required readings, read only in the sections the entries cite. That is not study of the readings: the other nine are unread, and Menkveld's survey had no open copy.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 15, 2026-10-15:

- `def:hft-strategies`: HFT as proprietary strategies sharing speed tools; the SEC's 2010 types (passive market making, arbitrage, structural, directional, with order anticipation and momentum ignition); pinging as a tool; the legacy taxonomy corrected.
- `res:latency-arbitrage-arms-race`: Budish, Cramton and Shim's sniping equilibrium, eq. (3); rent dissipation with endogenous speed, eq. (7); invariance of the prize to speed; the ES–SPY evidence, 2005–2011; the legacy "edge decays with diffusion" corrected.
- `res:hft-spread-investor-cost`: Lehalle and Laruelle's stylised model in which a narrower effective spread leaves other traders' costs unchanged or higher; calibration recomputed and the text's 0.5 bp corrected to 0.37 bp.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`.

Changed in migration slice 30, 2026-10-15, from the legacy execution-model file of Narang's notes (`sysinv/executionmod.tex`, mapped to the overview `portfolio-construction-risk`):

- `def:hft-strategies`: Narang's fast alpha (chap. 15, pp. 291-293) and footprints (chap. 7); the legacy *High Frequency Trading* block's machine-learning claim and its *HFT Shark Strategy*, neither in the third edition, kept as historical descriptions: "front-run" read against Narang's fiduciary definition (Appendix, pp. 312-314) and FINRA Rule 5270, the profit not riskless.

Partly checked 2026-10-15, draft; the blocks are in `notes/artefacts/portfolio-construction-risk/execution-model.tex`.

Changed in the slice-30 follow-up, 2026-10-15: `def:hft-strategies`' Currency field records FINRA Rule 5270 as the one current rule checked.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:order-anticipation`, `def:bluffing-manipulation`, `def:arbitrage`, `def:spread-measures`, `mod:glosten-milgrom` (`execution-market-making` and `market-making-lob`); `def:smart-order-routing` (`market-structure-execution-quality`).

## Entry backlog

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Fifteen legacy blocks were already assigned to this pathway before slice 15 and are unchanged: the flash-crash and shock-propagation blocks of `03_.../08_volatility_and_liquidity_interaction.tex`, *Fast Liquidity and Price Discovery* in `03_.../02_price_discovery.tex`, and the seven blocks of `05_.../05_latency_and_queue_competition.tex`, a stylised maker–taker fee and speed-investment model whose source has not been identified. The seven cross-asset blocks of `05_.../06_...` list this pathway as a candidate and are unassigned.

## What changed in my view or practice

## Questions carried forward

- Does the ES–SPY constancy of the arms-race prize hold elsewhere? `exp-aquilina-budish-oneill-races` measures races on a UK venue; read it before generalising.
- How do the empirical readings (`wide-hendershott-jones-menkveld`, `wide-brogaard-hft-discovery`) bear on Lehalle and Laruelle's stylised claim that a narrower spread can leave other traders' costs unchanged?
- The SEC's 2010 strategy types and legal remarks are dated; no current U.S. or EU rule on HFT was checked.
