# Migrating the compendium

The chapters in `legacy/` were written before these notes followed the learning guide's study method (`guide/`, *How to study with this guide*). On 14 October 2026 they were moved, with their text unchanged, into one chapter per guide section, and then into `legacy/<section-key>/`. This file is the plan for turning them into the guide's typed, labelled and cited entries. Phase 0 and a format pilot are done; the record of what has moved, what was checked and the map of legacy files to pathways is in [notes/migration.md](../notes/migration.md).

Migration is not study. Four kinds of progress are kept apart: *migration progress* (each old block has a disposition), *source verification* (an entry's claims compared with the passages at their locators), *mastery* (a checkpoint passed from your own notes) and *consolidation* (a pathway's backlog empty and its entries checked). Migration and a clean build advance only the first; the last two are dated in `notes/log.md` by you alone.

## Where things stood before Phase 0 (14 October 2026)

- **Block types.** There are 879 blocks in 17 environments of our own, against the guide's eleven entry types. The largest groups have no direct equivalent: `taxonomy` (178), `remark` (146), `caveat` (113) and `principle` (80).
- **Organisation.** The chapters follow the books they came from, not the guide's pathways. One microstructure file often feeds three or four pathways.
- **Labels and citations.** Only one block has a label (five figures also do), and sources are cited once per book at the top of a chapter rather than at each claim. No block can yet be linked to, or checked against its source.
- **Leftovers.**
  - 16 topic files have fewer than 250 words.
  - 21 execution-algorithm figures in `execution-trading-costs/figures/` are not used by any file.
  - The appendix (calculator, reading AI papers, Python, VS Code) is not quantitative finance.
  - The preface is placeholder text.

## Approach

Do not retype all 879 blocks in one go. Phase 0 is a one-off mechanical tidy that makes the material easy to work through. Phase 1, the migration itself, happens one pathway at a time, when that pathway is consolidated, with the old blocks as drafts. This is the guide's rule for notes written before the method.

## Phase 0: tidy (done 14 October 2026)

1. **Separate the old notes.** Done: the old chapters are in `legacy/<section-key>/`, compiled by `legacy/part.tex` as a final part, *Notes awaiting migration*. Their chapter labels became `legacy:<section-key>`, so a canonical chapter can take `\label{<section-key>}`; their block and figure labels are unchanged. The main chapters hold only entries in the guide's format. The staging folder is a convention of this repository, not of the guide.
2. **Migration map.** Done: `% migrate-to:` on the first line of each legacy file with blocks names its *candidate* pathways, and `% assign: <key>` before a block assigns it to one. The map is collected in `notes/migration.md`. The candidate lists are provisional, taken from the folder table below and narrowed by file name.
3. **Status script.** Done: `python3 ../tools/migration_status.py` reports the legacy blocks left, by section and by pathway (assigned, the only candidate, or shared and unassigned, so a shared file is never counted as owned by every pathway it lists), the entries written, and entries missing a label, a locator, a known citation key or any of the three status axes. `--check` also fails when the map and the files disagree or a key is not in the pinned routes. It checks presence, not truth: a citation it finds may not support its claim.
4. **Housekeeping.** Done: the tooling appendix is in `notes/tooling/`, which compiles on its own; the 21 unused execution figures stayed with `legacy/execution-trading-costs/figures/`; the placeholder preface text is gone; `hyperref` now loads last in `preamble.tex`, which removed the duplicate figure anchors.

## Phase 1: one pathway at a time

1. Run the status script to list the pathway's old blocks, assigned and shared.
2. At placement in the study loop, treat what the blocks cover as drafts to check against the readings, not material to learn again. Assign each shared block you will handle with `% assign:`.
3. When consolidating the pathway, decide each block's fate, and record it in the dispositions of `notes/migration.md`:
   - rewrite it as an entry, choosing the type by its content rather than its old environment's name;
   - merge it into a field of an existing entry;
   - turn it into a stub in the pathway's entry backlog;
   - or delete it.
4. Give every new entry a label, a `\citep` with a locator found in the reading (never reconstructed from memory), and a status on all three axes: verification, normally *unchecked* until compared with the passage and then saying exactly what was compared; stability, *draft*; and currency. Check existing citations against the source too: the pilot found legacy blocks citing papers whose formulas came from a textbook's simplification.
5. Delete a migrated block only once its content is represented and every pathway listing its file can find it; leave a `% migrated:` comment naming the destination, and keep any full derivation the entry shortens in `notes/artefacts/<pathway-key>/`. Delete each legacy file once it is empty. Compile and run `migration_status.py --check`. Date the pathway in `notes/log.md` only when it is in fact mastered or consolidated.

## How the old environments map to entry types

| Old environment (blocks) | Usually becomes |
|---|---|
| `definition` (98) | Definition; Convention if it states a market's quoting or settlement rule |
| `taxonomy` (178) | The list or table inside its parent concept's Definition; drop lists that make no claim |
| `principle` (80) | Result with its conditions, or Evidence if it is an empirical regularity |
| `mechanism` (81) | Model or Result; the guide's Mechanism type only for contract, order-lifecycle or settlement terms |
| `model` (58), with 28 proofs | Model; each proof shrinks to its idea plus a locator |
| `method` (31), `process` (18) | Method; order or settlement sequences become Mechanism |
| `proposition`, `lemma`, `corollary` (28) | Result |
| `caveat` (113) | Pitfall if it has a check and a remedy; otherwise the Conditions or Pitfalls field of its parent entry |
| `remark` (146), `practitionernote` (14) | The Practice or Conditions field of the entry it comments on, or delete |
| `empiricalfinding` (11), `casestudy` (3) | Evidence, with magnitude, sample and period; Example if it is numerical |
| `marketrule` (18) | Rule for law or regulation, with jurisdiction and date; Convention for venue rules such as matching priority |
| `notation` (2) | The notation register in `front/notation.tex` |

## Where the old notes go

| Old notes (folder, blocks) | Main target pathways |
|---|---|
| Microstructure foundations, orders and books, price formation (`execution-market-making/01`–`03`, 420; 418 after the pilot) | Market microstructure overview, `market-making-lob`, `market-structure-execution-quality`, `futures-execution` |
| Order flow and empirical microstructure (`execution-market-making/04`, 79) | `price-impact-execution`, `lob-deep-learning`, `market-making-lob`, `market-simulation` |
| Market making (`execution-market-making/05`, 47; 40 after the pilot) | `market-making-lob`, `hft-market-design` |
| Execution and algorithmic trading (`execution-trading-costs/01`, 87) | Execution overview, `price-impact-execution`, `market-structure-execution-quality`, `reinforcement-learning-trading`, `model-governance-controls` |
| Asset-class microstructure (`execution-trading-costs/02`, 37) | `futures-execution`, `options-execution`, `fx-dealer-market-making`, `otc-fixed-income-trading`, `synthetic-equity-cfd-trs`, `crypto-mm-microstructure` |
| AFML data chapters (`ml-alternative-data/data`, 36) | `statistical-learning-foundations`, `financial-ml-evaluation`, `alternative-data-sources` |
| Narang's systematic investing (`portfolio-construction-risk/sysinv`, 26) | Portfolio construction overview, `portfolio-construction`, `research-engineering-validation`, `model-governance-controls` |
| Gliner and Drobny (`multi-asset-systematic-macro`, 120) | Multi-asset overview, `macro-regimes-stock-bond`, `macro-nowcasting-signals`, `macro-announcements-policy`, `monetary-policy-curve`, `fx-determination-forecasting` |
| Hull basics (`volatility-options`, 13), time value of money (`rates-credit-mortgages`, 2) | Options overview. Forward pricing and hedge ratios go where the guide first needs them (rates, `commodity-hedging`); time- and money-weighted returns go to `performance-manager-evaluation` |
| Appendix (`appendix`, 12) | None: tooling notes, not compendium entries; moved to `notes/tooling/` |

## Order

1. **Pilot `market-making-lob`.** Done 14 October 2026 as a format pilot: six draft entries in `execution-market-making/market-making-models.tex` (Grossman–Miller with fees and liquidity measures, the static limit-order model, Avellaneda–Stoikov, Kyle), partly checked, with human review outstanding. Ho–Stoll is blocked: the legacy block cited it but follows a textbook's static stand-in, and the route's `catalogue-0527` names no paper. The pathway itself is not migrated: Grossman–Miller and Kyle are supplemental to it. Slices 2 to 20 (15 October 2026) migrated Glosten–Milgrom, the dealer material, the spread-decomposition and inventory files, most of the volatility-and-liquidity file (its flash-crash blocks are assigned to `hft-market-design`, one systemic block to `market-structure-execution-quality`) the information and price-discovery files, the strategic-trading-models file (slice 6), and the liquidity-and-market-impact file (slice 7), whose impact entries opened the canonical chapter `execution-trading-costs/` under `price-impact-execution`, the market-impact-models file (slice 8), the price-impact-estimation file (slice 9), the optimal-execution-problem file (slice 10), whose entries belong to the section overview `execution-trading-costs`, which now has a note, the execution-benchmarks file (slice 11) and the execution-algorithms file (slice 12), both also the overview's, and the transaction-cost-analysis file (slice 13), split between the overview, `market-structure-execution-quality` and `performance-manager-evaluation`, whose entry opened the canonical chapter `portfolio-construction-risk/`, the smart-order-routing file (slice 14), owned by `market-structure-execution-quality`, and the high-frequency-trading-strategies file (slice 15), routed outside its map candidates to `hft-market-design`, whose entries opened a topic file in `execution-market-making/`, and the reinforcement-learning-and-ML-in-execution file (slice 16), owned by `reinforcement-learning-trading`, whose entry opened the canonical chapter `ml-alternative-data/`, and the production-considerations file (slice 17), split between the overview `execution-trading-costs`, `model-governance-controls`, whose entry opened the canonical chapter `research-engineering-validation/`, and `execution-market-making`; it was the last topic of `01_execution_and_algorithmic_trading/`, whose folder is gone. Slice 18 migrated the equity-market-microstructure file, routed to the overview `execution-trading-costs` and to `etf-index-closing-execution`, with two blocks deleted. Slice 19 migrated the futures-market-microstructure file to `futures-execution`, with its large-tick block merged into an `execution-market-making` entry. Slice 20 migrated the FX-market-microstructure file to `fx-dealer-market-making`. Slice 5 also opened the note for the section overview `execution-market-making`, which now lists the entries that serve it. Ho–Stoll is still unread. The next bounded slice is recorded in `notes/migration.md`.
2. **Market microstructure overview**, which holds the largest set of blocks (Harris and Hasbrouck), then the rest of that section's pathways.
3. **Execution, trading costs and market structure**: its overview, `price-impact-execution` and `market-structure-execution-quality`, then the asset-class pathways.
4. **AFML, Narang, Gliner, Hull and time value of money**, whenever those pathways are studied.

## Done when

The legacy part is empty and every entry has a label, a citation at each claim and a status. The old environments can then be deleted from `preamble.tex`, with `legacy/part.tex` and its line in `compendium.tex`.
