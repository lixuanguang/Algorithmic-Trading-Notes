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

Written in migration slice 36, 2026-10-16, from the legacy latency-and-queue-competition, volatility-and-liquidity and price-discovery files (the fifteen blocks assigned here):

- `res:queue-position-value`: Moallemi and Yuan's static and dynamic components of queue value, the large-tick condition, the race after a price change, Table 3's front-against-back gaps (0.03 to 0.22 ticks); the legacy "thin queues" contradicted (`wide-moallemi-yuan-queue`, June 2017 revision, read in part; a reading of `market-making-lob`).
- `mod:make-take-fee-speed-race`: the source of the legacy fee-race blocks identified as Lehalle and Laruelle's app. A.2, summarising Foucault, Kadan and Kandel; eq. (A.4) re-derived as the trade-maximising fee split and checked against finite-population equilibria; printed slips recorded; the legacy "averages" corrected to sums.
- `mod:depth-overflow-flash-crash`: Lehalle and Laruelle's toy model (app. A.5); the time term resolved: the hot-potato $t$ counts rounds, the overflow approximation bounded, and (A.14) follows only if the overflow $R$, not the rate $r$, drives impact (derived and simulated); the remedies and the legacy control list.
- `ev:may-2010-flash-crash`: the CFTC and SEC staff findings of 30 September 2010 (executive summary), compared with Lehalle and Laruelle's account; the legacy case study and propagation channels checked against them.

Changed in slice 36: `def:hft-strategies` (trade counts as an HFT proxy, Lehalle and Laruelle pp. 20--21 and 170--171, against the report's volume warning). The fast-liquidity block of the price-discovery file was merged into `mod:make-take-fee-speed-race`. All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/hft-market-design/latency-queue-competition.tex` and `volatility-liquidity-flash-crash.tex`; checks in `notes/artefacts/execution-market-making/slice36-checks.py`.

## Source verification after slice 37

Second slice-37 follow-up, 2026-10-16, working source gaps of slice 36 (source verification, not study): `ev:flash-crash-studies` narrowed (Kirilenko et al.: classification of over 15,000 E-mini accounts; High Frequency Traders 34.22 percent of volume on 3-5 May and 28.57 on 6 May; their inventory-price relation unchanged during the crash); `mod:fkk-make-take-original` resolved (the September 2009 working paper: the platform maximises (c_m + c_t) R for a fixed total fee; Proposition 4 in the large-market limit is Lehalle and Laruelle's (A.4) with s*Delta for Delta/2 and Gamma for L, so "efficient" is trade-maximising for a given total fee; welfare R L - M C_m - N C_t is a different objective; the 2013 journal version not read). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 second follow-up*.

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `ev:flash-crash-studies` narrowed (the staff report's sec. I, printed pp. 12-17: depth below 1,050 contracts, the six-point no-bust range, 18,000 of the first 35,000 contracts sold aggressively, a 30,000-contract fundamental imbalance, 15 cross-market firms interviewed; Menkveld and Yueshen blocked); `res:frequent-batch-auctions` resolved (Budish, Cramton and Shim, secs. VII-VIII of the published version and n. 33 of the 2013 working paper: priority by whole batches outstanding, pro rata within a batch; speed advantage relevant a fraction delta/tau of the time; random delays do not address sniping). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:order-anticipation`, `def:bluffing-manipulation`, `def:arbitrage`, `def:spread-measures`, `mod:glosten-milgrom` (`execution-market-making` and `market-making-lob`); `def:smart-order-routing` (`market-structure-execution-quality`).

Changed in migration slice 35, 2026-10-16 (a routing exception from the foundations folder, whose candidates are `execution-market-making` and `market-structure-execution-quality`): `def:hft-strategies` (Lehalle and Laruelle's high-frequency liquidity bridges and role blurring, Introduction pp. 5--6 and 22; the legacy identification markers recorded) and `res:hft-spread-investor-cost` (the legacy caveats recorded as restatements). Partly checked 2026-10-16, draft; human review outstanding.

## Entry backlog

- ev:flash-crash-studies: Menkveld and Yueshen (`w5-menkveld-yueshen-flash`: publisher's version behind a subscription, SSRN refused automated access with HTTP 403, Singapore Management University's copy behind a bot check, 2026-10-16) and the staff report's equities sections (II-III); Kirilenko et al. and the report's section I were read

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 migrated every block assigned to this pathway (the latency file, the flash-crash and propagation blocks, the fast-liquidity block) and routed the cross-asset file, which listed this pathway, to `execution-market-making`'s arbitrage entries, because its blocks concern arbitrage rather than latency races. No legacy file now lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Does the ES–SPY constancy of the arms-race prize hold elsewhere? `exp-aquilina-budish-oneill-races` measures races on a UK venue; read it before generalising.
- How do the empirical readings (`wide-hendershott-jones-menkveld`, `wide-brogaard-hft-discovery`) bear on Lehalle and Laruelle's stylised claim that a narrower spread can leave other traders' costs unchanged?
- The SEC's 2010 strategy types and legal remarks are dated; no current U.S. or EU rule on HFT was checked.
