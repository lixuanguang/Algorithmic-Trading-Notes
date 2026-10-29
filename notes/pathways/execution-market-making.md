---
key: execution-market-making
section: execution-market-making
status: not started (draft entries only, not from study)
---

# Market microstructure and market making (section overview)

Overview outcome, from the guide: evaluate a quoting policy on an order-book replay by fill probability, adverse selection and inventory risk, and state how the result depends on queue-position and self-impact assumptions. The overview's readings are `alpha-harris`, `s6-hasbrouck`, `s6-stoikov`, `exp-cont-kukanov-order-placement`, `exp-huang-lehalle-rosenbaum-queue-reactive` and `exp-noble-rosenbaum-souilmi-reality-gap`; read them for orientation before the section's pathways. Its checkpoint is not marked as a section capstone.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 15 October 2026 by information and price discovery review (`notes/source-review-index.md`), because the guide runs one study loop per section overview and this route had no note. It lists the entries that serve the overview route rather than a specialist pathway. Until then they were listed provisionally in `market-making-lob.md`. They come from source checking against Harris (`alpha-harris`) and Hasbrouck (`s6-hasbrouck`), two of this route's readings, and against Lehalle and Laruelle (`alpha-laruelle`), which is on no route. None of it is study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Moved here from `market-making-lob.md` on 2026-10-15; written in spread and inventory models / volatility and liquidity reviews:

- `def:spread-measures`: quoted, inside, relative, effective and realised spreads (Harris, Hasbrouck).
- `res:roll-spread-estimator`: Roll's serial-covariance estimator and its biases (Harris, Hasbrouck); full derivation `drv:roll-spread-estimator` in the model reference, `model-derivations/execution-market-making/market-making-models/roll-spread-estimator.tex`.
- `res:spread-component-identification`: transitory and permanent components; the generalized Roll model; inventory versus information (Harris, Hasbrouck).
- `res:spread-determinants`: Harris's primary and secondary spread determinants and the order-driven equilibrium spread.
- `def:outside-spread`: value traders' outside spread (Harris); changed in information and price discovery review (profit sources, the no-trade band, not trading as a decision).
- `def:volatility-components`: fundamental and transitory volatility; the random-walk decomposition (Harris, Hasbrouck).
- `meth:garman-klass-volatility`: range-based intraday volatility as Lehalle and Laruelle use it (the 1980 paper not consulted).
- `meth:spread-volatility-regression`: spread on volatility in levels and logs, with the retransformation correction (Lehalle and Laruelle).
- `mech:bubble-crash-dynamics`: how bubbles build and crashes unwind; the price accelerator; crash attribution (Harris).

Written in information and price discovery / source review / optimal execution / high-frequency strategies reviews:

- `def:fundamental-value`: fundamental value, market value and noise; public, private and stale information (Harris; contrasted with Hasbrouck's efficient price).
- `res:informed-trading-aggregation`: informed trading makes prices informative; the price as an average of forecasts; correlated errors (Harris).
- `def:market-efficiency`: weak, semistrong and strong forms and the cost-sensitive definition; the market paradox; the information–liquidity trade-off (Harris).
- `def:inside-information`: inside information, who may not trade on it, and signal permission (Harris, U.S. law as of 2002).
- `def:price-formation-process`: the price formation process as immediate impact and decay (Lehalle and Laruelle).
- `def:intraday-overnight-returns`: intraday, overnight and close-to-close returns, volatility and correlation by time scale (Lehalle and Laruelle).

information and price discovery review also added cross-references to `def:volatility-components` and `meth:garman-klass-volatility`.

Written in strategic trading / source review / optimal execution / high-frequency strategies reviews (Harris chaps. 10–12, 16, 17, 24 and 29):

- `def:informed-trader-types`: value, news, information-oriented technical traders and arbitrageurs; when value and news traders profit.
- `def:winners-curse`: the winner's curse and the break-even bid as a fixed point.
- `res:insider-trading-deterrence`: insider-trading profitability, detection and deterrence (U.S., as described in 2002).
- `def:arbitrage`: hedge portfolio, basis, fair value, arbitrage spread and bounds; pure and speculative arbitrage; price and quantity characterisations.
- `res:arbitrage-risks`: implementation, basis, model and carrying-cost risk; staying power; the causes of arbitrage opportunities.
- `def:order-anticipation`: front running, quote matching, sentiment-oriented technical trading, squeezes, stop gunning, and the 2002 specialist privileges.
- `def:bluffing-manipulation`: rumourmongers and price manipulators; the asymmetric-impact condition; the proof problem.

Changed in strategic trading review:
- `res:informed-trading-aggregation`: trading speed and orthogonality merged, inverse-variance weighting, and the error comparison restated by loss measure, with the counterexample to "better than any individual".
- `def:inside-information`: skilled speculation against inside information.
- `def:outside-spread`: cross-references only.

Changed in liquidity and impact review: `def:bluffing-manipulation` (impact symmetry added to its Practice, with a pointer to the absence-of-manipulation entry listed under `price-impact-execution`), and cross-references from `def:price-formation-process` and `res:spread-component-identification` to the new price-impact entries, which live under `price-impact-execution`. Changed in impact estimation review: `res:spread-component-identification` (a cross-reference to the Glosten–Harris regression listed under `price-impact-execution`).

All twenty-two: verification partly checked 2026-10-15, stability draft. Human review is outstanding.

Written in trading infrastructure / source review / optimal execution / high-frequency strategies reviews:

- `def:floor-automated-trading-systems`: Harris's comparison of floor and automated trading systems (chap. 27, Table 27-1), as of 2002; the six headings are the entry's grouping of Harris's seven sections (trading infrastructure review follow-up).

Partly checked 2026-10-15, draft.

Changed in futures market structure / source review / optimal execution / high-frequency strategies reviews: `res:spread-determinants` gained Lehalle and Laruelle's large-tick bounce term (eq. (2.1)) and the book-size compensation at a one-tick spread (p. 148); the futures-specific claim is a backlog item of `futures-execution`.

Written in order books and order flow / source review / optimal execution / execution control reviews:

- `mech:order-lifecycle`: order states (FIX 4.4), insert, modify, cancel and execute, private and public channels, and venue-specific loss of priority (CME's FIFO rule), from Lehalle and Laruelle, Bouchaud et al. and Harris.
- `def:limit-order-book`: the book, best quotes, Harris's limit-price placement, open and closed books, the three event types, price changes and RFQ screens.
- `res:limit-order-options`: Harris's standing limit orders as trading options, the two risks and adverse selection of fills (the queue file's adverse-selection caveat merged).

All three: partly checked 2026-10-16, draft; human review outstanding. The equilibrium-spread argument was already in `res:spread-determinants` and the best-quote definitions in `def:spread-measures`, both cross-referenced rather than repeated.

Written in order matching and fragmentation / source review / optimal execution / execution control reviews:

- `def:order-instructions`: Harris's standard order instructions (types, validity, quantity, display, handling, special), the FIX 4.4 fields that carry them, and their interactions (immediate-or-cancel against fill-or-kill, remainders, size restrictions, stops through gaps).
- `mech:order-matching-pricing`: Harris's matching procedure, precedence rules and uniform, discriminatory and derivative pricing; pro-rata allocation with worked remainders; Lehalle and Laruelle's four call-auction rules, random ends and matching curves; Harris's surplus result with its conditions.

Changed in order matching and fragmentation review: `res:limit-order-options` (order choice: Harris's spread argument and Table 14-1, with a posting threshold derived and computed). Changed in the order matching and fragmentation review follow-up: `res:limit-order-options` (posting against crossing re-derived from cash flows with a common terminal mark, $pS-(1-p)M$, checked pathwise; the order matching and fragmentation review $p(S-A)-(1-p)M$ withdrawn) and `mech:order-matching-pricing` (pro-rata capped by eligible liquidity; rounding remainder distinguished from the incoming order's residual). Changed in the order books and order flow review follow-up: `mech:order-lifecycle` (FIX 4.4 OrdStatus and ExecType distinguished; sessions and orders carried across them) and `def:limit-order-book` (order type against aggressiveness). All partly checked 2026-10-16, draft; human review outstanding. Checks: `trading_notes.numerical.dark_trading_fragmentation.order_routing_fragmentation_checks`.

Written in market design and liquidity / source review / optimal execution / execution control reviews:

- `def:market-functions`: what markets do (liquidity, price discovery, risk transfer, capital allocation), private and public benefits, why the mechanism matters, and Harris's wealth shares as dated estimates (Harris chaps. 1, 3, 9; Hasbrouck chap. 1).
- `def:trader-motives`: utilitarian, profit-motivated and futile traders; long and short; patience and the liquidity side; hedging instruments; comparative advantage (Harris chaps. 3, 8, 19).
- `res:zero-sum-skill-luck`: zero-sum accounting and its two corollaries with their conditions; when past profit predicts future profit, with the conditional assumptions on luck stated (Harris chaps. 8, 9, 22; simulated).
- `def:market-intermediaries`: dealers, market makers, brokers and broker-dealers; why brokers are cheaper; Harris's five liquidity suppliers (Harris chaps. 3, 7, 8, 19).
- `def:market-structures-venues`: market structure, forums and access, exchanges, OTC and alternative systems, information systems and transparency, clearing and settlement, brokered credit (Harris's ordered count of pairs and the unordered count), reported volume, RFQ against CLOB (Harris chaps. 3, 5, 7, 24; Lehalle and Laruelle).
- `def:trading-sessions-execution-systems`: continuous and call sessions; quote-driven, order-driven, brokered and hybrid markets; auctions and fixings; specialists; the London gold price dated from LBMA and IBA (Harris chaps. 5, 24, 28; Hasbrouck chap. 2).
- `def:liquidity-dimensions`: liquidity as bilateral search; immediacy, width, depth, resiliency; the depth--width duality with its attainment condition; the search rule; displayed and latent liquidity; book size (a "lower bound" reading corrected); flow reactivity (Harris chap. 19; Hasbrouck chap. 1; Lehalle and Laruelle secs. 2.2--2.3).

Changed in market design and liquidity review (merges): `def:informed-trader-types` (liquidity roles), `def:arbitrage` (porters of liquidity), `def:floor-automated-trading-systems` (technology, reporting, and the capacity condition restated as a necessary queue-stability condition), `mech:order-matching-pricing` (open-outcry rule, precedence), `res:spread-determinants` and `meth:spread-volatility-regression`, `def:market-efficiency` (liquidity and informative prices), `def:inside-information` (insiders' controls; Rule 10b5-1 as amended in 2022, Form 4 and Regulation FD as of October 2026) and `res:insider-trading-deterrence` (Harris's policy debate; retitled). Material was also merged into the block-trade, order-exposure and price-impact entries (owned by `execution-trading-costs` and `price-impact-execution`) and into the two high-frequency-trading entries (owned by `hft-market-design`). All partly checked 2026-10-16, draft; human review outstanding. Checks: `trading_notes.numerical.market_organisation.liquidity_market_design_checks`.

Corrected in the market design and liquidity review follow-up, 2026-10-16: `def:liquidity-dimensions` (width and depth stated per unit, after Harris pp. 398--399, and kept apart from a cash budget; average against marginal cost; an explicit size domain; attainment conditions, with lower semicontinuity neither necessary nor enough without boundedness) and `def:floor-automated-trading-systems` (for the M/M/1 queue, utilisation below one is necessary and sufficient for stability; delay, deadlines, burst duration, backlog and buffers treated separately; the burst simulation redone with exact arrival sampling and waits separated from time in system). `trading_notes.numerical.market_organisation.liquidity_market_design_checks` sections 4 and 8 were rewritten; its other results are unchanged.

Written in dealer models and information / source review / optimal execution / execution control reviews:

- `def:dealer-quotes-order-flow`: Harris's dealers and their four problems; two-sided and one-sided, firm and soft, continuous and on-request quotes; the inside spread (Table 13-1 recomputed); trading with dealers; attracting and buying order flow; preferencing (chap. 13, as of 2002).
- `def:specialist-obligations-privileges`: affirmative, negative, auction and capital obligations; the privileges; the participation-option inequality marked as interpretation of Harris p. 499; tick size and participation (box, p. 500); the regulator's question and who pays (chap. 24, as of 2002).

Changed in dealer models and information review (merges): `def:outside-spread` (the dealer comparison restated), `def:arbitrage` (cross-asset arbitrage mapped onto Harris's types; derivative conversion and dynamic hedges; the cyclic currency band derived and Harris's currency box found inconsistent and recomputed) and `res:arbitrage-risks` (legging and synchronised execution, capital, relative-value features, and the factor decomposition with a hedge ratio); `def:trader-motives` (comparative advantage in signals); `meth:spread-volatility-regression` (fit quality and the averaging effect); and `mech:bubble-crash-dynamics` (See also updated). All partly checked 2026-10-16, draft; human review outstanding. Checks: `trading_notes.numerical.high_frequency_trading.dealer_queue_information_checks`.

Corrected in the dealer models and information review follow-up, 2026-10-16: `def:arbitrage` (exact triangular equality of cross rates restricted to the frictionless case; with bid and ask quotes the synthetic and direct midpoints can differ inside the executable band, checked on EUR/USD 1.0999/1.1001, USD/JPY 109.99/110.01 and EUR/JPY 120.99/121.03, synthetic mid 121.00 against direct 121.01, both cycles unprofitable). Corrected in a second market design and liquidity review follow-up, 2026-10-16: `def:liquidity-dimensions` (the cost function made dimensionally consistent: $C(q)=q\,w(q)$ with $w$ in currency per share, or $C=q\,m\,w_{bp}/10{,}000$ with $w$ in basis points of the midpoint $m$; 100 shares at a midpoint of 100 and 10 bp cost 10). Both checks extend `trading_notes.numerical.high_frequency_trading.dealer_queue_information_checks` and `trading_notes.numerical.market_organisation.liquidity_market_design_checks`.

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467`: `market-organisation-liquidity`, `market-making-lob`, `lob-deep-learning`, `options-execution`, `market-simulation`, `fx-dealer-market-making`, `hft-market-design`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `market-organisation-liquidity` (Market organisation, informed trading and liquidity measurement): added by the guide revision of 22 October 2026 (`8302467`); no pathway note; its entries are in `execution-market-making/market-organisation`, `execution-market-making/trading-systems`, `execution-market-making/informed-trading`, `execution-market-making/arbitrage-anticipation`, `execution-market-making/spread-measurement`, `execution-market-making/volatility-liquidity-crashes`.
- `market-making-lob` (Market making, queues and limit-order-book models): pathway note [market-making-lob.md](market-making-lob.md), 16 entries listed, in `execution-market-making/market-making-models`, `execution-market-making/order-books`, `execution-market-making/order-flow-statistics`.
- `lob-deep-learning` (Deep learning on limit-order-book data): pathway note [lob-deep-learning.md](lob-deep-learning.md), 1 entries listed, in `execution-market-making/order-flow-imbalance`.
- `options-execution` (Options market making and execution costs): pathway note [options-execution.md](options-execution.md), 3 entries listed, in `execution-market-making/options-dealing`.
- `bond-swap-dealer-market-making` (Bond and swap dealing: RFQs, inventory and balance-sheet capacity): no pathway note; partial treatment in existing entries, not reviewed as complete: RFQ protocols, venues and dealer risk-bearing in fixed income (`def:fixed-income-market-structure` in `execution-trading-costs/fixed-income-trading`); OTC derivative execution by RFQ (`def:trade-implementation-by-market` in `execution-trading-costs/trade-strategy-governance`). Not written: RFQ quoting and inventory models for bonds and swaps; balance-sheet capacity constraints.
- `market-simulation` (Market simulation and counterfactual testing): pathway note [market-simulation.md](market-simulation.md), 5 entries listed, in `execution-market-making/order-flow-statistics`.
- `fx-dealer-market-making` (FX dealing: internalisation, last look and hedging): pathway note [fx-dealer-market-making.md](fx-dealer-market-making.md), 3 entries listed, in `execution-market-making/fx-dealing`.
- `hft-market-design` (High-frequency trading, speed and adverse selection): pathway note [hft-market-design.md](hft-market-design.md), 7 entries listed, in `execution-market-making/high-frequency-trading`.

## Entry backlog

Empty after the source verification (2026-10-17); new stubs go here.

## Source verification after macro markets and pricing review

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `conv:order-instruction-venue-rules` narrowed (CME wiki pages Order Qualifiers, Cancel on Disconnect and Matching Algorithm Steps through the public REST interface; MIAX PEARL filing SR-PEARL-2021-35); `conv:dmm-obligations-current` narrowed (NYSE Rule 104: one-round-lot continuous two-sided quote, 15 and 10 percent of the day at the inside by volume class, Designated Percentages 8/28/30 and Defined Limits 9.5/29.5/31.5). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `conv:order-instruction-venue-rules` resolved for the venues named (Nasdaq Equity 4, Rules 4703(e), 4756(a)(3) and 4757(a)(1), browser export of 16 October 2026: two minimum-quantity modes, persistent on the resting order; priority kept only for re-marking and size reduction; CME and MIAX PEARL read earlier); `conv:dmm-obligations-current` resolved for NYSE (current Rules 104 and 107B, browser exports of 16 October 2026: 15/10 percent at the inside for non-ETPs and 25 for ETPs; Designated Percentages and Defined Limits unchanged; last amended 22 November 2022 and 25 January 2023; other venues out of the entry's scope). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `conv:pro-rata-allocation-rules` resolved for CME Globex by merge into `mech:order-matching-pricing` (Client Systems Wiki, "CME Globex Matching Algorithm Steps", version 5 of 2 June 2026, from the retained REST export): algorithms by step, Pro Rata rounded down with a minimum allocation, Leveling (algorithm K), Split with FIFO rounded up, TOP, LMM (options only), the FIFO exception, and display-quantity priority; CME's examples recomputed in `trading_notes.numerical.order_books.cme_allocation_checks`. `conv:session-carry-over` resolved for CME Globex by merge into `mech:order-lifecycle` (Order Qualifiers, version 3; Matching Algorithm Steps, version 5): day orders expire, GTC and GTD carry with their timestamps, no TOP over a weekend. Other venues and CME's market-data recovery were not checked. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

## What changed in my view or practice

## Questions carried forward

- Harris's fundamental value conditions on all information known to anyone; Hasbrouck's efficient price on public information only. Which one does each later entry (Kyle, Glosten–Milgrom, the spread decompositions) use?
- The legal details in `def:inside-information` are U.S. law as of 2002 and were not checked against current law. Which current sources should replace them, and does any pathway own that material?
- Lehalle and Laruelle attribute part of the 2010 rise in extraday correlation to a less noisy intraday price formation process and to high-frequency trading (p. 177). Is there evidence beyond their figures?
