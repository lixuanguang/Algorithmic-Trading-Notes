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

## Status after slice 37 (16 October 2026)

- **Legacy blocks:** 0 (867 in the finance chapters at the baseline). The migration of the notes written before the study method is complete; that is migration progress only, not source verification, mastery or consolidation.
- **Entries:** 211, all *draft* and *partly checked*. **Human review is outstanding** for every entry; the review items of each slice are under its *For review* in [migration-slices.md](migration-slices.md), and the open questions in [log.md](log.md).
- **Legacy chapters emptied:** all. `execution-trading-costs` (only its 21 unused figures remain, in `compendium/legacy/execution-trading-costs/figures/`); `portfolio-construction-risk` (slice 30); `volatility-options` and `rates-credit-mortgages` (slice 31); `ml-alternative-data` (slice 32); `execution-market-making` (slice 36); `multi-asset-systematic-macro` (slice 37, which also removed `compendium/legacy/part.tex`). The old environments stay in `compendium/preamble.tex` because the preservation artefacts compile with them.
- **Build:** `latexmk -g -pdf compendium.tex` exits 0; no LaTeX warnings; 0 overfull and 0 underfull boxes; one inherited `page.i` duplicate-destination warning. Tests: 14 pass.

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
| 36 | The rest of the legacy microstructure chapter: market making (dealers, specialists, queue value, fees and the speed race, cross-asset arbitrage), information and volatility (price formation across venues, the Flash Crash and its toy model), and the feature- and data-engineering files (eight files, chapter closed) | `ca6986e` | 180 → 120 | 170 → 177 | Triangular-arbitrage band (frictionless equality only) |
| 37 | The legacy macro chapter: global macro, its record, sizing and practitioners; regimes, indicators, releases and event queries; central banks, the Taylor rule, the policy path and LIBOR's end, curve trades, TIPS, swaps and money markets; sovereign credit and CDS; currencies; equity indices, valuation and the VIX; commodity curves, indices, oil, gas, metals and agriculture (three files, chapter closed, legacy part removed) | this slice's commit | 120 → 0 | 177 → 211 | |

## After the migration

The migration slices are finished: no legacy block remains. The planning text that stood here before slice 37 (deferring the 75 transmission blocks until Gliner was obtained) is superseded; Gliner's *Global Macro Trading* was then available as a local PDF and was read for the whole chapter. Earlier slice records keep their own planning as written.

**Next substantive work** is study and verification, not migration, in this order:

1. **Human review of the draft entries**, starting with the newest and least-checked: the 34 macro entries of slice 37 (Gliner-derived figures as of 2013, practitioner opinions, dated central-bank facts), then the *For review* lists of slices 33--36. Review compares each claim with its passage and records the result in the entry's *Status*; it does not set mastery or consolidation dates.
2. **Work the backlogs where the gap is a source to read**, not a judgement: for the macro chapter, the stubs listed in slice 37 (CME's Eurodollar conversion date, BoE minutes timing history, TIPS schedule history, BLS payroll scope, the ISDA 2012 Greece determination, the BIS 2025 dollar share, ICE's dollar-index methodology, current CME, Eurex, ICE and LME contract terms, agency commodity data, NBER dating after 2005).
3. **Study pathways one at a time by the guide's method**, choosing ones whose entries already exist so that the readings can be checked against them, in the guide's order for the learner, prerequisites first. No pathway is mastered; `notes/log.md` is where you record that.
4. **Tooling:** `tools/migration_status.py` still reports entry metadata, pathway-note listings and citation keys; its legacy-block counting now always reports zero and can be simplified later.

## File map

One row per legacy file with blocks; `tools/migration_status.py --check` fails if this table and the files' `% migrate-to:` lines disagree. Empty since slice 37: no legacy file with blocks remains.

<!-- map:begin -->
| Legacy file | Candidate pathways |
|---|---|
<!-- map:end -->
