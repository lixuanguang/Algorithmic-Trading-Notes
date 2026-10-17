# Compendium migration record

The working record for moving the notes written before the study method into the guide's typed entries. The plan, with its type mapping and order, is in [compendium/README.md](../compendium/README.md). This file holds the conventions, the current status, an index of the slices and the map of legacy files to pathways; each slice's full record (sources, findings, checks, dispositions, counts, build) is in [migration-slices.md](migration-slices.md). Check the map and progress with `python3 tools/migration_status.py` (add `--check` to fail on any problem).

## Four kinds of progress, kept apart

| Kind | What it means | Where it is recorded | Set by |
|---|---|---|---|
| Migration progress | A legacy block has a disposition: rewritten as an entry, merged into one, stubbed in a backlog, or deleted | Each slice's dispositions in [migration-slices.md](migration-slices.md); counts in this file's status and index, and `tools/migration_status.py` | The migration |
| Source verification | An entry's claims have been compared with the passages at their locators | Each entry's *Status: Verification*, and the *Checks and their limits* of each slice in [migration-slices.md](migration-slices.md) | Whoever reads the passage |
| Learner mastery | A pathway's checkpoint passed from your own notes, readings closed | `notes/log.md`, *Mastered* | You only |
| Pathway consolidation | Everything the pathway relies on is in checked entries and its backlog is empty | `notes/log.md`, *Consolidated* | You, after review |

Migrating a block and compiling the result advances only the first. An entry written during migration starts as a draft whose verification says exactly what was compared; no migration step sets a mastery or consolidation date.

## Conventions

- **Legacy staging.** Old chapters lived in `compendium/legacy/<section-key>/` and compiled, through `compendium/legacy/part.tex`, as the final part *Notes awaiting migration*, a temporary convention of this repository, not part of the guide's layout. Slice 37 (16 October 2026) emptied the last legacy chapter and removed `part.tex` and its line in `compendium.tex`; only `compendium/legacy/execution-trading-costs/figures/` (21 unused figures) remains, and the original texts are in `notes/artefacts/`. The convention below is kept as the record of how the migration worked. Their chapter labels carry a `legacy:` prefix so that they never collide with the canonical chapter label (`\label{<section-key>}`) when that chapter appears. Their block, figure and remark labels are unchanged.
- **Canonical homes.** Migrated entries go in `compendium/<section-key>/`, in the section where the guide first needs the concept. Other pathways link to that entry rather than restating it.
- **Map.** `% migrate-to: key, key` on the first line of each legacy file with blocks names the pathways its blocks are *candidate* material for. These lists are provisional: drawn from the plan's folder table and narrowed by file name, not from reading every block. A file listing several pathways is shared material; none of those pathways owns its blocks until one is assigned.
- **Assignment.** `% assign: <pathway-key>` on the line before a block assigns that block to one pathway. Only assigned blocks, or blocks in a file with a single candidate, count towards one pathway; the status script lists shared, unassigned blocks separately.
- **Removal.** A block is deleted from a legacy file only when its content is represented in an entry, a backlog stub or an artefact, and the pathways that list the file can find it: the deletion site keeps a `% migrated:` comment naming the destination labels.
- **Derivations.** When an entry keeps only the idea of a proof, the full working goes to `notes/artefacts/<pathway-key>/`, and the entry's *Further reading* names the file.

- **Records.** Each slice appends one section to [migration-slices.md](migration-slices.md) and one row to the index below. A correction to a finished slice is appended as a follow-up; earlier records are left as written.

## Status after slice 37 (16 October 2026), updated 17 October 2026

- **Legacy blocks:** 0 (867 in the finance chapters at the baseline). The migration of the notes written before the study method is complete; that is migration progress only, not source verification, mastery or consolidation.
- **Entries:** 254 after the fourth batch of 17 October 2026, all *draft* and *partly checked*. The fourth batch repaired seven audit findings (the inflation row on quarterly CPI vintages, calendar-month inference for pooled Clark--West tests, log returns for heating oil, FRA settlement conventions, the ERC Sharpe condition, the BIS liquidation scale, manipulation intent), rewrote the active backlog lines to their remaining gaps, and worked 70 targets (41 resolved, 21 narrowed, 5 tested within stated bounds, 2 blocked, 1 unchanged), adding 15 entries and eight pathway notes; the record is in `notes/migration-slices.md`, *Fourth batch of 17 October 2026*. It is source verification, not human review.

  The paragraph as written after the third batch of 17 October 2026: 239 entries after the third batch of 17 October 2026 (228 after the second, 221 after the first, 211 at slice 37), all *draft* and *partly checked*. The third batch repaired six audit findings and worked a 60-item queue; the record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.
  - *Audit repairs.* Filing availability (dissemination or first observation, else unknown), FIX Done for Day, the expected-shortfall definition, the Sharpe-ratio moment condition, the GIPS no-benchmark exception, and the global-macro window from January 2014 run on the public workbook.
  - *Queue.* 15 resolved, 35 narrowed, 3 unchanged, 1 blocked, 4 tested within stated bounds (heating oil, FX carry, the inflation-shock row, global macro from 2014), 2 deferral triggers reviewed and retained; 11 new entries.

  The paragraph as written after the second batch of 17 October 2026: 228 entries after the second batch of 17 October 2026 (221 after the first, 211 at slice 37), all *draft* and *partly checked*. The second batch repaired eight audit findings and worked a 50-item queue; the record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.
  - *Audit repairs.* The three bounded empirical tests were rerun as v2 with v1 kept: contract identity, inventory release timing and executable timing for energy; CPI staleness and outcome eligibility for FX; window definitions, dollar series and inference for regimes. The Sharpe-ratio standard-error conditions, projection against conditional expectation, the cross-validation plateau heuristic, order reconciliation and filing timestamps were corrected.
  - *Queue.* 10 resolved, 23 narrowed, 4 unchanged, 7 blocked, 3 repaired and retested, 1 newly tested within bounds (global macro, 2022--2026), 2 left with protocols.

  The paragraph as written after the first batch of 17 October 2026: 221 entries after the batch of 17 October 2026 (211 at slice 37), all *draft* and *partly checked*. The batch of 17 October 2026 corrected four audit findings (Kolm et al.'s Table~3 net counts and Fig.~8, the Ultra Bond's spread tick, the `lob-deep-learning` status) and worked 40 items in three groups: the 15 active leftovers of the 35-item queue (2 resolved, 7 narrowed further, 5 unchanged, 1 still blocked; the queue now stands at 20 resolved, 12 narrowed, 1 blocked, 2 deferred), 19 older backlog items (17 resolved, 10 of them as new entries, and 2 narrowed), and the six macro empirical stubs (3 tested within stated bounds, 3 open with executable protocols); the two deferred items were rechecked and stay deferred (`notes/migration-slices.md`, *Batch of 17 October 2026*). Earlier in this paragraph, as written on 16 October 2026: The slice-37 follow-up (16 October 2026) corrected nine audit findings, rechecked the 34 macro entries and three merges against their passages, and resolved 9 and narrowed 27 of the 36 slice-37 backlog items; the second follow-up (same day) corrected five more audit findings (inversion signal rules on a rebuilt H.15 series, FX accrual bases, CDS coverage, convexity carry, the GSCI launch date), resolved 7 and narrowed 10 of the 21 source-based stubs (4 blocked by CME's access refusal; the six empirical stubs stay open) and worked four slice-36 source gaps (2 resolved, 2 narrowed). A third pass, the source follow-up of slices 33--36 (same day), corrected five audit findings (the OFI universe-selection date, the Eurodollar conversion chronology and its stale pitfall, the demographic attribution, the retrospective inversion episode rule) and worked a 35-item queue: 9 resolved, 19 narrowed, 5 blocked, 2 deferred. A second source follow-up (same day) worked the 24 unresolved, non-deferred items from newly obtained local copies: 9 resolved, 8 narrowed further, 1 still blocked, 6 unchanged, leaving the queue at 18 resolved, 14 narrowed, 1 blocked, 2 deferred, and corrected Gliner's 2-year Treasury tick. All four are source verification, not human review. **Human review is outstanding** for every entry; the review items of each slice are under its *For review* in [migration-slices.md](migration-slices.md), and the open questions in [log.md](log.md).
- **Legacy chapters emptied:** all. `execution-trading-costs` (only its 21 unused figures remain, in `compendium/legacy/execution-trading-costs/figures/`); `portfolio-construction-risk` (slice 30); `volatility-options` and `rates-credit-mortgages` (slice 31); `ml-alternative-data` (slice 32); `execution-market-making` (slice 36); `multi-asset-systematic-macro` (slice 37, which also removed `compendium/legacy/part.tex`). The old environments stay in `compendium/preamble.tex` because the preservation artefacts compile with them.
- **Build:** after the fourth batch of 17 October 2026, a clean `latexmk -pdf compendium.tex` (after `latexmk -C`) exits 0 with 346 pages; no LaTeX warnings; 0 overfull and 0 underfull boxes; one inherited `page.i` duplicate-destination warning. Tests: 14 pass. (After the third batch, as then written: a clean `latexmk -pdf compendium.tex` (after `latexmk -C`) exits 0 with 328 pages; no LaTeX warnings; 0 overfull and 0 underfull boxes; one inherited `page.i` duplicate-destination warning. Tests: 14 pass. (After the second batch: 307 pages; after the first: 294.))

## Slices

Blocks are the legacy blocks counted by `migration_status.py` before and after the slice; entries likewise. Follow-ups are the corrections recorded after the slice, each under its own heading in [migration-slices.md](migration-slices.md).

| Slice | Topic | Commit | Blocks | Entries | Follow-ups |
|---|---|---|---|---|---|
| Phase 0 | Legacy staging, tooling, map and checker | `3a02a41` | 879 → 867 (tooling appendix moved out) | 0 | |
| Pilot | `market-making-lob` format pilot | `3a02a41` | 867 → 858 | 0 → 6 | |
| 2 | Glosten–Milgrom and the dealer material | `07a0504` | 858 → 840 | 6 → 12 | |
| 3 | Spread decomposition and inventory models | `79aa634` | 840 → 819 | 12 → 18 | |
| 4 | Volatility and liquidity | `326ad36` | 819 → 805 | 18 → 22 | |
| 5 | Information, market efficiency and price discovery | `80810ee` | 805 → 787 | 22 → 28 | |
| 6 | Strategic trading models | `3780514` | 787 → 757 | 28 → 35 | |
| 7 | Liquidity and market impact | `c7ed121` | 757 → 751 | 35 → 38 | |
| 8 | Market impact models | `2214a1b` | 751 → 741 | 38 → 40 | |
| 9 | Price impact estimation | `3d597b1` | 741 → 733 | 40 → 44 | |
| 10 | Optimal execution problem | `bbaafa5` | 733 → 724 | 44 → 46 | |
| 11 | Execution benchmarks | `5d113ac` | 724 → 721 | 46 → 49 | |
| 12 | Execution algorithms | `3d93967` | 721 → 704 | 49 → 54 | |
| 13 | Transaction cost analysis | `b699ed2` | 704 → 679 | 54 → 60 | |
| 14 | Smart order routing | `4fb411c` | 679 → 664 | 60 → 63 | |
| 15 | High-frequency trading strategies | `60753ff` | 664 → 661 | 63 → 66 | |
| 16 | Reinforcement learning and ML in execution | `6d04e52` | 661 → 657 | 66 → 67 | Corrections to `mod:cartea-jaimungal-execution` (`8aa672a`) |
| 17 | Production considerations | `1c3fabc` | 657 → 646 | 67 → 70 | Clarifications |
| 18 | Equity market microstructure | `580463e` | 646 → 640 | 70 → 71 | ETF and Harris precision |
| 19 | Futures market microstructure | `fb56198` | 640 → 633 | 71 → 75 | Corrections (`bd4ba54`); account classes and second-month settlement |
| 20 | FX market microstructure | `9a9a62e` | 633 → 629 | 75 → 78 | Corrections |
| 21 | Options market microstructure | `c035b4f` | 629 → 625 | 78 → 81 | Corrections |
| 22 | Fixed-income microstructure | `18eef7f` | 625 → 619 | 81 → 84 | Corrections |
| 23 | Securities lending and synthetic shorts | `b56a121` | 619 → 613 | 84 → 88 | Corrections (`74c643e`); lending opening |
| 24 | Crypto market microstructure | `9148410` | 613 → 609 | 88 → 91 | Socialised-loss trigger |
| 25 | Research and backtest evaluation | `c45e2b5` | 609 → 605 | 91 → 95 | Corrections |
| 26 | Risk assessment: model risk, regime change, shocks, contagion, monitoring | `e0451c9` | 605 → 600 | 95 → 98 | Overrides, impact inference, Calmar |
| 27 | Transaction cost models: components and cost functions | `0224ac7` | 600 → 598 | 98 → 99 | Units, cost-function conditions, sell example |
| 28 | Portfolio construction models: rules, mean–variance optimisation, signal portfolios | `4e7666d` | 598 → 595 | 99 → 102 | Closed-form conditions, permutations, ML tasks, ERC rounding |
| 29 | Risk models: factor exposures, limits and penalties | `cd7b13c` | 595 → 591 | 102 → 103 | Residual diversification, CVX–XOM hedge, compensation wording |
| 30 | Narang's systematic-investing cluster: overview and diagram, alpha models, execution (three files, chapter closed) | `2642451` | 591 → 583 | 103 → 108 | Hidden-order leakage, lifecycle timing, currency fields |
| 31 | Hull's derivatives basics, forwards, futures and hedging, and the time-value file (three files, two chapters closed) | `9fbd551` | 583 → 568 | 108 → 118 | Cross-hedge components, yield-shift condition, return horizons and GIPS annualisation |
| 32 | AFML data cluster: taxonomy, bars and multi-product series, labels, sample weights, fractional differentiation (five files, chapter closed) | `8be60d1` | 568 → 532 | 118 → 135 | Hedge-ratio sign, ETF-trick timing and capital, label spans, Hawkes lead |
| 33 | Orders, the limit order book and queues; trade signing and order-flow imbalance; stylised facts, event time and point processes (eight files, one batch) | `d40d4c2` | 532 → 459 | 135 → 151 | Trade-signing arithmetic, order type against aggressiveness, sessions, FIX states, realised-variance limits, waiting times |
| 34 | The rest of the orders-and-matching folder: order instructions, matching and trade pricing, dark trading, routing and fragmentation (four files, folder closed) | `4d9d5da` | 459 → 351 | 151 → 158 | Pro-rata capacity, posting against crossing, ex-fixing domain, venue-share variance, SOR objective |
| 35 | The foundations folder: market functions, motives, skill and luck, intermediaries, venues, sessions, liquidity; regulation, venue competition, U.S. and EU rules, circuit breakers (six files, folder closed) | `063de31` | 351 → 180 | 158 → 170 | Liquidity units, systematic internaliser and U.S. currency, queue stability, preservation counts |
| 36 | The rest of the legacy microstructure chapter: market making (dealers, specialists, queue value, fees and the speed race, cross-asset arbitrage), information and volatility (price formation across venues, the Flash Crash and its toy model), and the feature- and data-engineering files (eight files, chapter closed) | `ca6986e` | 180 → 120 | 170 → 177 | Triangular-arbitrage band (frictionless equality only); second slice-37 follow-up: FKK original and multi-level OFI resolved, Flash Crash studies and TAQ corrections narrowed |
| 37 | The legacy macro chapter: global macro, its record, sizing and practitioners; regimes, indicators, releases and event queries; central banks, the Taylor rule, the policy path and LIBOR's end, curve trades, TIPS, swaps and money markets; sovereign credit and CDS; currencies; equity indices, valuation and the VIX; commodity curves, indices, oil, gas, metals and agriculture (three files, chapter closed, legacy part removed) | `f73498d` | 120 → 0 | 177 → 211 | Audit corrections (convexity, inversion necessity and sufficiency, VIX units, gold and silver shares, Drobny stops, Gliner locators, commercial paper, GSCI history, FX carry and CDS conventions); source-verification pass over the 37 macro entries and merges; 36 backlog items resolved (9) or narrowed (27); second follow-up: inversion month and episode rules on H.15, FX accrual bases, CDS coverage, convexity carry, GSCI launch 11 April 1991; 21 source stubs resolved (7), narrowed (10) or blocked (4) |
| Batch 2026-10-17 | Four audit corrections; 15 queue leftovers, 19 older backlog items and six macro empirical stubs (three bounded tests) | `820517a` | 0 → 0 | 211 → 221 | Second batch: three tests rerun as v2, five conceptual repairs |
| Second batch 2026-10-17 | Eight audit repairs (three empirical tests rerun, v1 kept) and a 50-item queue | `12e634a` | 0 → 0 | 221 → 228 | Third batch: six audit repairs |
| Third batch 2026-10-17 | Six audit repairs and a 60-item queue (four bounded tests) | `012aa19` | 0 → 0 | 228 → 239 | Fourth batch: seven audit repairs |
| Fourth batch 2026-10-17 | Seven audit repairs, backlog reconciliation and a 70-target batch (five new bounded tests or checks on data) | this batch | 0 → 0 | 239 → 254 | |

## After the migration

The migration slices are finished: no legacy block remains. The planning text that stood here before slice 37 (deferring the 75 transmission blocks until Gliner was obtained) is superseded; Gliner's *Global Macro Trading* was then available as a local PDF and was read for the whole chapter. Earlier slice records keep their own planning as written.

**Next substantive work** is study and verification, not migration, in this order:

1. **Human review of the draft entries**, starting with the newest and least-checked: the 34 macro entries of slice 37 (Gliner-derived figures as of 2013, practitioner opinions, dated central-bank facts), then the *For review* lists of slices 33--36. Review compares each claim with its passage and records the result in the entry's *Status*; it does not set mastery or consolidation dates.
2. **Work the backlogs where the gap is a source to read**, not a judgement. For the macro chapter this was done in two slice-37 follow-ups: 9 items resolved and 27 narrowed, then 7 more resolved and 10 narrowed further (CME's notice, the S&P and Bloomberg methodologies, the H.15 series, UN projections, a de facto classification, the BIS swaps line and others were read). The source follow-up of 16 October 2026 then worked 35 macro and microstructure stubs (9 resolved, 19 narrowed, 5 blocked, 2 deferred), reaching CME contract terms through CBOT and NYMEX certifications filed with the CFTC, EU texts through CELLAR and U.S. rules through the Federal Register. A second source follow-up the same day read local copies of most of those sources: CME, LME and Nasdaq rule texts; NYSE's current Rules 104 and 107B; the ISM calendar; OPEC's Statute with the UAE and EIA statements; Holden and Jacobsen; Lee and Ready; Hayashi and Yoshida; Kolm et al.; Menkveld and Yueshen; and two of the tick-size studies. It resolved 9 more items and narrowed 8. What remains needs:
   - statements not yet published or found: OPEC's on the UAE, and any record of the Commission's adoption of ESMA's SI standards;
   - purchased or paywalled documents: the 2014 ISDA Definitions, Ellis, Michaely and O'Hara, and the other tick-size studies;
   - appendices not obtained: Holden and Jacobsen's Internet Appendix;
   - future outcomes: NBER dating;
   - licensed data: SOFR OIS rates;
   - empirical tests no reading can replace: the six macro empirical stubs and any costing of our own order-book signals.

   Each stub says which. The batch of 17 October 2026 then resolved 19 of 40 items, narrowed 9 and tested three empirical stubs within stated bounds; what remains is mostly behind paywalls or registration (the 2014 ISDA Definitions, the tick-size and trade-classification studies, FINRA's rulebook, hedge-fund indices, licensed message and valuation data), awaiting a statement (OPEC) or future dating (NBER), or is the untested remainder of the empirical stubs. The second batch of 17 October 2026 then worked a 50-item queue: 10 resolved, 23 narrowed, 7 blocked and 4 unchanged, with one new bounded test. What remains is mostly refused retrieval (sec.gov, the FCA, OCC, Cboe, LME, S\&P DJI, SSRN), sold or paywalled documents (ISDA 2014, Working, Brennan, Baillie and Myers, the tick-size studies), licensed data (country valuations, message data, macro index histories before 2022), trade-level data for the practitioner rules, and the untested remainder of the empirical stubs. Correction (fourth batch of 17 October 2026): the macro hedge-fund index history listed above among material behind registration was public through BarclayHedge's ordinary download form, as the third batch found; the fourth batch also reached the FCA's PS24/14 and BIS documents through Internet Archive captures, and rewrote every backlog line to its remaining gap.
3. **Study pathways one at a time by the guide's method**, choosing ones whose entries already exist so that the readings can be checked against them, in the guide's order for the learner, prerequisites first. No pathway is mastered; `notes/log.md` is where you record that.
4. **Tooling:** `tools/migration_status.py` still reports entry metadata, pathway-note listings and citation keys; its legacy-block counting now always reports zero and can be simplified later.

## File map

One row per legacy file with blocks; `tools/migration_status.py --check` fails if this table and the files' `% migrate-to:` lines disagree. Empty since slice 37: no legacy file with blocks remains.

<!-- map:begin -->
| Legacy file | Candidate pathways |
|---|---|
<!-- map:end -->
