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

Written in migration slice 6, 2026-10-15, from the strategic-trading-models file (Harris chaps. 10–12, 16, 17, 24 and 29):

- `def:informed-trader-types`: value, news, information-oriented technical traders and arbitrageurs; when value and news traders profit.
- `def:winners-curse`: the winner's curse and the break-even bid as a fixed point.
- `res:insider-trading-deterrence`: insider-trading profitability, detection and deterrence (U.S., as described in 2002).
- `def:arbitrage`: hedge portfolio, basis, fair value, arbitrage spread and bounds; pure and speculative arbitrage; price and quantity characterisations.
- `res:arbitrage-risks`: implementation, basis, model and carrying-cost risk; staying power; the causes of arbitrage opportunities.
- `def:order-anticipation`: front running, quote matching, sentiment-oriented technical trading, squeezes, stop gunning, and the 2002 specialist privileges.
- `def:bluffing-manipulation`: rumourmongers and price manipulators; the asymmetric-impact condition; the proof problem.

Changed in slice 6:
- `res:informed-trading-aggregation`: trading speed and orthogonality merged, inverse-variance weighting, and the error comparison restated by loss measure, with the counterexample to "better than any individual".
- `def:market-efficiency`: the legacy paradox wording.
- `def:inside-information`: skilled speculation against inside information.
- `def:outside-spread`: cross-references only.

Changed in slice 7: `def:bluffing-manipulation` (the legacy impact-symmetry principle merged into its Practice, with a pointer to the absence-of-manipulation entry listed under `price-impact-execution`), and cross-references from `def:price-formation-process` and `res:spread-component-identification` to the new price-impact entries, which live under `price-impact-execution`. Changed in slice 9: `res:spread-component-identification` (a cross-reference to the Glosten–Harris regression listed under `price-impact-execution`).

All twenty-two: verification partly checked 2026-10-15, stability draft. Human review is outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`, where the migration has kept every removed block since the pilot.

Written in migration slice 17, 2026-10-15, from a legacy execution file whose map named only `model-governance-controls` (a routing exception):

- `def:floor-automated-trading-systems`: Harris's comparison of floor and automated trading systems (chap. 27, Table 27-1), as of 2002; the six headings are the entry's grouping of Harris's seven sections (slice-17 follow-up).

Partly checked 2026-10-15, draft; its artefact is `notes/artefacts/model-governance-controls/derivations.tex`.

Changed in migration slice 19, 2026-10-15: `res:spread-determinants` took the legacy large-tick futures principle, adding Lehalle and Laruelle's large-tick bounce term (eq. (2.1)) and the book-size compensation at a one-tick spread (p. 148); the futures-specific claim is a backlog item of `futures-execution`.

Written in migration slice 33, 2026-10-16, from the legacy order-lifecycle and limit-order-book-mechanics files:

- `mech:order-lifecycle`: order states (FIX 4.4), insert, modify, cancel and execute, private and public channels, and venue-specific loss of priority (CME's FIFO rule), from Lehalle and Laruelle, Bouchaud et al. and Harris.
- `def:limit-order-book`: the book, best quotes, Harris's limit-price placement, open and closed books, the three event types, price changes and RFQ screens.
- `res:limit-order-options`: Harris's standing limit orders as trading options, the two risks and adverse selection of fills (the queue file's adverse-selection caveat merged).

All three: partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/execution-market-making/order-lifecycle.tex`, `limit-order-book-mechanics.tex` and `02-overview-original.tex`. The tick-size blocks of the same file went to `market-structure-execution-quality`; the legacy equilibrium-spread principle was already in `res:spread-determinants` and the best-quote definitions in `def:spread-measures`, both cross-referenced rather than repeated.

Written in migration slice 34, 2026-10-16, from the legacy order-types and matching-algorithms files:

- `def:order-instructions`: Harris's standard order instructions (types, validity, quantity, display, handling, special), the FIX 4.4 fields that carry them, and their interactions (immediate-or-cancel against fill-or-kill, remainders, size restrictions, stops through gaps).
- `mech:order-matching-pricing`: Harris's matching procedure, precedence rules and uniform, discriminatory and derivative pricing; pro-rata allocation with worked remainders; Lehalle and Laruelle's four call-auction rules, random ends and matching curves; Harris's surplus result with its conditions.

Changed in slice 34: `res:limit-order-options` (order choice: Harris's spread argument and Table 14-1, with the legacy posting threshold derived and computed). Changed in the slice-34 follow-up: `res:limit-order-options` (posting against crossing re-derived from cash flows with a common terminal mark, $pS-(1-p)M$, checked pathwise; the slice-34 $p(S-A)-(1-p)M$ withdrawn) and `mech:order-matching-pricing` (pro-rata capped by eligible liquidity; rounding remainder distinguished from the incoming order's residual). Changed in the slice-33 follow-up: `mech:order-lifecycle` (FIX 4.4 OrdStatus and ExecType distinguished; sessions and orders carried across them) and `def:limit-order-book` (order type against aggressiveness). All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/execution-market-making/order-types-instructions.tex`, `matching-algorithms.tex`, and the folder wrapper and chapter file as they stood before slice 34 (`02-overview-before-slice34.tex`, `legacy-section-before-slice34.tex`); checks in `notes/artefacts/market-structure-execution-quality/slice34-checks.py`.

Written in migration slice 35, 2026-10-16, from the first five files of the legacy foundations folder (roles of markets, participants and motives, venues and architecture, auction and dealer structures, market quality; map candidates `execution-market-making` and `market-structure-execution-quality`; the overview owns them as conceptual material):

- `def:market-functions`: what markets do (liquidity, price discovery, risk transfer, capital allocation), private and public benefits, why the mechanism matters, and Harris's wealth shares as dated estimates (Harris chaps. 1, 3, 9; Hasbrouck chap. 1).
- `def:trader-motives`: utilitarian, profit-motivated and futile traders; long and short; patience and the liquidity side; hedging instruments; comparative advantage (Harris chaps. 3, 8, 19).
- `res:zero-sum-skill-luck`: zero-sum accounting and its two corollaries with their conditions; when past profit predicts future profit, with the conditional assumptions on luck the legacy proposition lacked (Harris chaps. 8, 9, 22; simulated).
- `def:market-intermediaries`: dealers, market makers, brokers and broker-dealers; why brokers are cheaper; Harris's five liquidity suppliers (Harris chaps. 3, 7, 8, 19).
- `def:market-structures-venues`: market structure, forums and access, exchanges, OTC and alternative systems, information systems and transparency, clearing and settlement, brokered credit (Harris's ordered count and the legacy unordered one), reported volume, RFQ against CLOB (Harris chaps. 3, 5, 7, 24; Lehalle and Laruelle).
- `def:trading-sessions-execution-systems`: continuous and call sessions; quote-driven, order-driven, brokered and hybrid markets; auctions and fixings; specialists; the London gold price dated from LBMA and IBA (Harris chaps. 5, 24, 28; Hasbrouck chap. 2).
- `def:liquidity-dimensions`: liquidity as bilateral search; immediacy, width, depth, resiliency; the depth--width duality with its attainment condition; the search rule; displayed and latent liquidity; book size (the legacy "lower bound" corrected); flow reactivity (Harris chap. 19; Hasbrouck chap. 1; Lehalle and Laruelle secs. 2.2--2.3).

Changed in slice 35 (merges): `def:informed-trader-types` (liquidity roles), `def:arbitrage` (porters of liquidity), `def:floor-automated-trading-systems` (technology, reporting, and the capacity condition restated as a necessary queue-stability condition), `mech:order-matching-pricing` (open-outcry rule, precedence), `res:spread-determinants` and `meth:spread-volatility-regression` (legacy restatements recorded), `def:market-efficiency` (liquidity and informative prices), `def:inside-information` (insiders' controls; Rule 10b5-1 as amended in 2022, Form 4 and Regulation FD as of October 2026) and `res:insider-trading-deterrence` (Harris's policy debate; retitled). Routing exceptions recorded in `notes/migration-slices.md`: blocks merged into the block-trade, order-exposure and price-impact entries (owned by `execution-trading-costs` and `price-impact-execution`) and into the two high-frequency-trading entries (owned by `hft-market-design`). All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/execution-market-making/roles-of-financial-markets.tex`, `market-participants-trading-motives.tex`, `trading-venues-market-architecture.tex`, `auction-dealer-market-structures.tex`, `market-quality-efficiency.tex`, the folder wrapper and chapter file as they stood before slice 35 (`01-overview-before-slice35.tex`, `legacy-section-before-slice35.tex`) and the checks `slice35-checks.py`.

Corrected in the slice-35 follow-up, 2026-10-16: `def:liquidity-dimensions` (width and depth stated per unit, after Harris pp. 398--399, and kept apart from a cash budget; average against marginal cost; an explicit size domain; attainment conditions, with lower semicontinuity neither necessary nor enough without boundedness) and `def:floor-automated-trading-systems` (for the M/M/1 queue, utilisation below one is necessary and sufficient for stability; delay, deadlines, burst duration, backlog and buffers treated separately; the burst simulation redone with exact arrival sampling and waits separated from time in system). `slice35-checks.py` sections 4 and 8 were rewritten; its other results are unchanged.

Written in migration slice 36, 2026-10-16, from the legacy economics-of-market-making and optimal-quoting files of the market-making folder (eleven blocks assigned here):

- `def:dealer-quotes-order-flow`: Harris's dealers and their four problems; two-sided and one-sided, firm and soft, continuous and on-request quotes; the inside spread (Table 13-1 recomputed); trading with dealers; attracting and buying order flow; preferencing (chap. 13, as of 2002).
- `def:specialist-obligations-privileges`: affirmative, negative, auction and capital obligations; the privileges; the legacy participation-option inequality marked as interpretation of Harris p. 499; tick size and participation (box, p. 500); the regulator's question and who pays (chap. 24, as of 2002).

Changed in slice 36 (merges): `def:outside-spread` (the dealer comparison restated), `def:arbitrage` (cross-asset arbitrage mapped onto Harris's types; derivative conversion and dynamic hedges; the cyclic currency band derived and Harris's currency box found inconsistent and recomputed) and `res:arbitrage-risks` (legging and synchronised execution, capital, relative-value features, and the factor decomposition with a hedge ratio), from the cross-asset file, whose candidates are `market-making-lob` and `hft-market-design`, and the feature-engineering file (routing exceptions); `def:trader-motives` (comparative advantage in signals); `meth:spread-volatility-regression` (fit quality and the averaging effect, from the data-engineering file; routing exception); and `mech:bubble-crash-dynamics`, whose See also pointed to the removed legacy chapter. All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/execution-market-making/economics-of-market-making.tex`, `optimal-quoting-inventory-control.tex`, `cross-asset-cross-venue-market-making.tex`, the three folder wrappers and the chapter file as they stood before slice 36 (`03-`, `04-` and `05-overview-before-slice36.tex`, `legacy-section-before-slice36.tex`) and the checks `slice36-checks.py`.

Corrected in the slice-36 follow-up, 2026-10-16: `def:arbitrage` (exact triangular equality of cross rates restricted to the frictionless case; with bid and ask quotes the synthetic and direct midpoints can differ inside the executable band, checked on EUR/USD 1.0999/1.1001, USD/JPY 109.99/110.01 and EUR/JPY 120.99/121.03, synthetic mid 121.00 against direct 121.01, both cycles unprofitable). Corrected in a second slice-35 follow-up, 2026-10-16: `def:liquidity-dimensions` (the cost function made dimensionally consistent: $C(q)=q\,w(q)$ with $w$ in currency per share, or $C=q\,m\,w_{bp}/10{,}000$ with $w$ in basis points of the midpoint $m$; 100 shares at a midpoint of 100 and 10 bp cost 10). Both checks extend `notes/artefacts/execution-market-making/slice36-checks.py` and `slice35-checks.py`.

## Entry backlog

- conv:order-instruction-venue-rules: Nasdaq's minimum-quantity attribute and modification rules (Equity 4, Rule 4703, refused automated access, HTTP 403) and other named venues; CME Globex's minimum quantity, cancel on disconnect and FIFO modification rules (wiki pages, versions of 2025-2026) and MIAX PEARL Rule 2616(a)(5) (as described in a 2021 filing) were read on 2026-10-16
- conv:pro-rata-allocation-rules: how named venues allocate pro-rata remainders (rounding, minimum allocation, time or size tie-breaks) and whether refreshed iceberg slices keep priority, with rule dates; CME's allocation steps could not be retrieved in slice 34 (the site blocks scripted access)
- conv:session-carry-over: which order durations a named venue carries across sessions (for example CME Globex good-till-cancel and good-till-date orders), and what a replay must load at the open; slice-33 follow-up stated only Harris's 2002 broker practice and FIX's TimeInForce values
- conv:dmm-obligations-current: NYSE Rule 104 as currently amended (read in NYSE's rulebook compilation last modified 9 May 2019, with later Federal Register filings listed: June and September 2019 amendments, a 2023 proposal withdrawn in July 2024) and other venues' market-maker obligations

## Source verification after slice 37

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `conv:order-instruction-venue-rules` narrowed (CME wiki pages Order Qualifiers, Cancel on Disconnect and Matching Algorithm Steps through the public REST interface; MIAX PEARL filing SR-PEARL-2021-35); `conv:dmm-obligations-current` narrowed (NYSE Rule 104: one-round-lot continuous two-sided quote, 15 and 10 percent of the day at the inside by volume class, Designated Percentages 8/28/30 and Defined Limits 9.5/29.5/31.5). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 migrated the last blocks of the legacy microstructure chapter (`compendium/legacy/execution-market-making/`) and removed it, with its wrappers kept verbatim in the artefacts: no legacy file now lists this pathway. Earlier: slice 5 migrated the information-and-market-efficiency file and nine of the twelve price-discovery blocks, slices 6 and 7 the strategic-trading and liquidity-and-impact files, slices 33 and 34 the orders-and-matching folder, and slice 35 the foundations folder. That says nothing about consolidation.

## What changed in my view or practice

## Questions carried forward

- Harris's fundamental value conditions on all information known to anyone; Hasbrouck's efficient price on public information only. Which one does each later entry (Kyle, Glosten–Milgrom, the spread decompositions) use?
- The legal details in `def:inside-information` are U.S. law as of 2002 and were not checked against current law. Which current sources should replace them, and does any pathway own that material?
- Lehalle and Laruelle attribute part of the 2010 rise in extraday correlation to a less noisy intraday price formation process and to high-frequency trading (p. 177). Is there evidence beyond their figures?
