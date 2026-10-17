---
key: market-structure-execution-quality
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Market structure rules, fees and execution quality

Pathway outcome, from the guide: explain how fragmentation, dark trading, fees, tick size, odd lots, retail routing and trading hours affect execution quality, and track the 2024–2026 U.S. and EU rule changes. Its checkpoint measures effective and realised spreads and price improvement on Rule 605-style data by order size and venue type. Its readings include `ex-sec-rule605-2024` and `ex-sec-withdrawal-2025` (best-execution proposals withdrawn in 2025).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 13 (`notes/migration.md`) and extended by slice 14, which migrated the smart-order-routing file mapped to this pathway alone (routing across fragmented venues and the effect of fees). Slice 13 opened it because the legacy transaction-cost file's best-execution, retail execution-quality and broker-conflict blocks belong to this pathway's outcome (retail routing and execution quality) rather than to the overview. The entries come from migration and source checking against Harris (`alpha-harris`, 2002) and Kissell (`s7-kissellscience`, on no route); their rules and figures are as of 2002 and 2014, and none of this pathway's readings has been read. That is not study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 13, 2026-10-15:

- `def:best-execution`: Harris's three standards of best execution, speed and price as dimensions of execution quality, NBBO and price-improvement practice, Rules 11Ac1-5 and 11Ac1-6 (as of 2002), and Kissell's process definition.
- `def:broker-agency-conflicts`: the broker principal–agent problem; dual trading and internalisation, order preferencing and payment for order flow, soft dollars and directed brokerage, dishonest practices; venue rebates (Kissell).

Written in migration slice 14, 2026-10-15:

- `def:smart-order-routing`: venue-specific marketability, Lehalle and Laruelle's three-broker example (recomputed; one misprint), latency and mirrored liquidity, liquidity seekers.
- `res:fee-adjusted-venue-choice`: when a worse price with lower fees is cheaper; buy and sell thresholds; per-share fees.
- `meth:passive-order-split`: queue, distance and trading-rate rankings and the minimum-resting-time split (the book's eq. (3.4) sign misprint corrected).
- Merged: the U.S. and European regimes into `def:best-execution`, with 17 CFR 242.611 checked in the eCFR text of 13 October 2026; order preferencing and a routing-conflict condition into `def:broker-agency-conflicts`.

All five: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`. The spread measures they use are owned by `execution-market-making` and cross-referenced, not listed here.

Written in migration slice 33, 2026-10-16, from the tick-size blocks of the legacy limit-order-book-mechanics file (a map candidate; the pathway's outcome names tick size):

- `def:tick-size`: the grid, regimes, relative tick, binding probability and leeway, queue jumping and price clustering.
- `ev:tick-size-market-quality`: Lehalle and Laruelle's FTSE 100 evidence (April 2012) and their account of the decimalisation studies.
- `mod:harris-discretised-spread`: Harris's latent-spread model as Lehalle and Laruelle present it, with the tick-reduction counterfactual in corrected units (computed in `notes/artefacts/market-simulation/order-flow-checks.py`).

All three: partly checked 2026-10-16, draft; human review outstanding; no current tick rule is stated. Artefact: `notes/artefacts/execution-market-making/limit-order-book-mechanics.tex`.

Written in migration slice 34, 2026-10-16, from the legacy hidden-liquidity-and-dark-trading and cross-venue-routing-and-fragmentation files (both map candidates; the outcome names fragmentation and dark trading):

- `def:dark-pools-crossing`: dark pools and crossing networks, derivative pricing and its risks, the European two-book design, motives, evidence as Lehalle and Laruelle report it (the legacy "volatile periods" qualified: true of dark turnover, not of dark share), gaming and internal crossing.
- `meth:venue-market-share`: value and trade-count shares, the ex-fixing share (Lehalle and Laruelle's printed formula corrected), aggregation, estimation error and time-of-day effects.
- `meth:fragmentation-concentration-metrics`: FEI, coverage, Gini and two-sample KS, with "H0 accepted" corrected to failure to reject.
- `mod:sor-market-share-dynamics`: Lehalle and Laruelle's toy model of routers and shares, with three printed slips and the first-order condition corrected, and the legacy variance-feedback "finding" reclassified as a model result.
- `ev:european-fragmentation-evidence`: fragmentation and liquidity, spreads and share, resilience, intraday share, the 2010 Euronext outage, and Spain as a confounded comparison.

Changed in slice 34: `def:smart-order-routing` (temporal then spatial splitting, execution-policy records, aggregation, duplicate liquidity, average trade size, Harris's consolidation mechanisms and a derived cross-venue bound) and `res:fee-adjusted-venue-choice` (maker--taker and fee complexity). All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/market-structure-execution-quality/hidden-liquidity-dark-trading.tex`, `cross-venue-routing-fragmentation.tex`, `slice34-checks.py`. Six exposure blocks and three block-trading blocks of the dark-trading file were merged into the order-exposure and block-trade entries owned by `execution-trading-costs` (a routing exception; listed in that note). Changed in the slice-34 follow-up: `meth:venue-market-share` (ex-fixing domain and the equality condition $mp(1-\mathfrak M)=0$; the fixed-weight variance of a stock's share against its index, with count and value shares distinguished; the textbook's pooled form recorded as unsupported) and `mod:sor-market-share-dynamics` (size-weighted marginal condition with interior and boundary cases; the slice-34 reproduction claim withdrawn and replaced by an illustrative variant that concentrates).

Written in migration slice 35, 2026-10-16, from the legacy regulatory-and-structural-evolution file of the foundations folder (a map candidate; the outcome names U.S. and EU rule changes, fragmentation and dark trading):

- `def:market-regulation-design`: who regulates, design questions, Harris's four-step evaluation and his stated objectives, public and private services, regulatory risk and capture, unintended consequences (Harris chaps. 3, 9, 26, 28).
- `mech:venue-competition-fragmentation`: the order-flow externality (with the legacy inequality restated), why markets segment, cross-market precedence and the race to the bottom, Lehalle and Laruelle's post-MiFID phases and their inconsistent dates, technology fragmentation, consolidated tapes (Harris chap. 26; Hasbrouck chap. 1; Lehalle and Laruelle).
- `rule:us-equity-market-structure`: decimal pricing (2000--2001), Regulation NMS (2005), Rule 612 as amended in 2024 with its stay and the exemptions to November 2027, single-stock and market-wide circuit breakers and LULD (2010--2019), stub quotes, Rule 15c3-5 and the CAT rule, each from Federal Register, eCFR or SEC texts.
- `rule:eu-trading-venue-transparency`: MiFID and MiFID II dates with their postponements, venue types, waivers, the double volume cap (4 and 8 percent, 2018 to 28 September 2025) replaced by the single 7 percent cap (from 29 September 2025; first results 9 October 2025), and the payment-for-order-flow ban, from EU texts retrieved through the Publications Office and ESMA statements.
- `mech:circuit-breakers-trading-halts`: halts, limits, taxes, margins and collars; when a halt helps; gravitational effect, propagation and related instruments; incidence by trader type; MiFID II Art. 48(5) (Harris chap. 28; Lehalle and Laruelle sec. 2.5.3).

Changed in slice 35: `def:tick-size` (ticks and precedence, the race to the bottom, the 2009 European tick war, MiFID II Art. 49), `def:best-execution` (Lehalle and Laruelle's best execution after fragmentation), `def:dark-pools-crossing` (broker crossing networks), `def:smart-order-routing` (latency and book state; the "Nyquist--Shannon latency bound" not adopted as a theorem, restated as a staleness probability), `def:broker-agency-conflicts` (order-flow arrangements, internal crossing, the EU payment-for-order-flow ban) and `meth:venue-market-share` (reference-price auctions). All partly checked 2026-10-16, draft; human review outstanding. Artefact: `notes/artefacts/market-structure-execution-quality/regulatory-structural-evolution.tex`; checks in `notes/artefacts/execution-market-making/slice35-checks.py`.

Corrected in the slice-35 follow-up, 2026-10-16: `rule:eu-trading-venue-transparency` (the systematic-internaliser definition: the 2014 wording dated as historical, the current wording from Directive (EU) 2024/790, its equity scope, the removed substantial-basis criterion and the opt-in retained for non-equity instruments, supported by Delegated Regulation (EU) 2026/392 recital 1; transposition due 29 September 2025, national measures unchecked) and `rule:us-equity-market-structure` (aggregate odd-lot depth exempted to May 2028 by Release 34-104612, the best odd-lot order not exempted; NYSE's market-wide circuit breakers made permanent by Release 34-94441 of March 2022; the 2024 amendments effective since 9 December 2024 with compliance exempted to November 2027). Partly checked, draft.

Changed in migration slice 36, 2026-10-16, from three blocks assigned here and four routed here: `mech:venue-competition-fragmentation` (price formation across venues with Hasbrouck's information shares, chap. 10, pp. 99--105; the systemic-risk caveat against Lehalle and Laruelle pp. 169 and 177), `ev:european-fragmentation-evidence` (the Euronext outage of 13 October 2010, pp. 183--185) and `meth:venue-market-share` (proportions in general, Wald against Wilson coverage computed, sampling units; four blocks of the data-engineering file, a routing exception). Partly checked 2026-10-16, draft. Artefacts: `notes/artefacts/market-structure-execution-quality/price-discovery-fragmentation-outage.tex` and, for the routed blocks, `notes/artefacts/lob-deep-learning/microstructure-data-engineering.tex`.

- `rule:spoofing-securities-markets`: EU market-abuse law on order placement and cancellation (MAR Art. 12, Annex I; 2016/522 Annex II 'layering and spoofing') and U.S. Exchange Act sec. 9(a); FINRA rules and enforcement not read. Partly checked 2026-10-17, draft.

## Entry backlog


- ev:tick-size-primary-studies: Bacidore et al. (2003), Jones and Lipson (2001), Ahn et al. (1996), Harris (1996), the 2000 journal version of Goldstein and Kavajecz, and Harris's (1994) projection tables; journal paywalls, and Jones and Lipson's Columbia working paper 99-3 is listed by RePEc only with a publisher link (rechecked 2026-10-17)

- rule:spoofing-securities-markets: (narrowed in the third batch of 2026-10-17) SEC and FINRA enforcement actions on layering (sec.gov refuses automated retrieval) and FINRA Regulatory Notice 17-22; Rule 10b-5 and FINRA Rules 2020 and 5210.03 were read on 2026-10-17 and are in the entry

- rule:block-print-trade-through-current: (narrowed in the third batch of 2026-10-17) how exchange crosses rank against displayed orders (size precedence, if any); Rule 611(b) and FINRA Rule 6380B's 10-second reporting and modifiers (version of 30 March to 5 December 2026) were read on 2026-10-17 and merged into `def:block-trade`
- rule:eu-si-national-transposition: the transposition of Directive 2024/790 in Member States other than Ireland and Malta, and Malta's route for the definition; no Commission implementing act on SI notifications (MiFIR Art. 15(5)) was found by a CELLAR title search on 2026-10-17, which does not prove non-adoption
- ev:circuit-breaker-effects: (narrowed in the third batch of 2026-10-17) studies of daily price limits, the MWCB working group's study itself (its nyse.com link 404), and a comparison with the published Hautsch and Horvath (JFE 131(2), 2019); their CFS working paper, Kasahara and Yamada (JPX WP 52) and, on 2026-10-17, SEC Release 34-93365's account of the March 2020 halts were read
- ev:dark-pool-price-discovery: (narrowed in the third batch of 2026-10-17) Buti, Rindi and Werner's published 'Diving into Dark Pools' (Financial Management 51(4), 2022; no open copy found) and its price-efficiency results; Zhu (2014), their June 2010 working paper and, on 2026-10-17, Comerton-Forde and Putniņš's accepted manuscript were read
- ev:market-share-variance-claim: (narrowed in the third batch of 2026-10-17) the source of Lehalle and Laruelle's statement that "all studies have shown that variance is proportional with market share" (p. 72)

## Source verification after slice 37

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `rule:tick-size-regimes-current` resolved (Delegated Regulation (EU) 2017/588 with its 2019 and 2023 amendments, read through CELLAR: six ADNT bands, nineteen price ranges, annual recalculation applied from the first Monday of April; MiFIR Art. 17a for systematic internalisers as inserted in 2019 and replaced in 2024; Directive (EU) 2024/790's third-country tick option); `ev:tick-size-primary-studies` blocked (Bacidore et al. 2003, Goldstein and Kavajecz 2000, Ahn et al. 1996 and Harris 1994 and 1996 behind journal subscriptions; the Wharton working-paper link for Goldstein and Kavajecz returned 404 and the Internet Archive rate-limited the lookup, 2026-10-16); `conv:eu-pre-trade-waiver-thresholds` resolved (MiFIR Art. 4 as published and as amended by Regulation (EU) 2024/791; RTS 1 Arts. 5-8 and Annex II with Delegated Regulations 2019/442, 2023/944 and 2025/1246: large-in-scale EUR 15,000-650,000 by ADT, ETFs EUR 3 million since 5 June 2023, reserve orders at least EUR 10,000); `rule:us-market-wide-circuit-breakers-current` resolved for the rules named (Nasdaq Rule 4121 and FINRA Rule 6121.02 made permanent in April 2022; NYSE Rule 7.12 and Nasdaq Rule 4121 amended in September-October 2026 for Level 3 resumption with overnight trading; LULD plan: 23rd amendment disapproved 2024, 27th approved 2026 for overnight bands, 29th in temporary effect; the other exchanges' 2022 filings and the 21st, 22nd, 25th, 26th and 28th amendments only listed); `rule:eu-si-national-transposition` narrowed (Ireland S.I. 436/2025, in operation 29 September 2025, adopts the directive's wording; Malta L.N. 218/2025 transposes only Art. 1(1); ESMA's 10 April 2025 release read through the fetching tool); `rule:cat-current-status` resolved as of October 2026 from Federal Register texts (Eleventh Circuit vacatur of the 2023 funding order on 25 July 2025, as the SEC and CAT LLC describe it; revised funding model approved 16 March 2026; customer-information amendment approved 13 January 2026; cost reductions approved 27 March 2026; concept release of 20 April 2026); the court's opinion and the technical specifications not read; `ev:circuit-breaker-effects` narrowed (Hautsch and Horvath, CFS WP 571: volatility and spreads rise before pauses and stay higher for an hour; depth falls about 25 percent); `ev:dark-pool-price-discovery` narrowed (Zhu: model, Propositions 3-5; Buti, Rindi and Werner 2010: SIFMA data for eleven pools in 2009, associations with market quality, price-efficiency section marked TBA). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `ev:tick-size-primary-studies` narrowed from blocked (Goldstein and Kavajecz, Wharton working paper of 16 September 1998; Harris, RFS 1994, partial scan, pp. 149 and 155); `rule:eu-si-national-transposition` narrowed (ESMA's final report of 10 April 2025 read: draft ITS, qualitative test for equities only, notifications within 20 calendar days and resubmission by all SIs, guidance left to NCAs); `ev:circuit-breaker-effects` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands); `ev:dark-pool-price-discovery` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/migration-slices.md`, *Second source follow-up of the slice 33-37 queue*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `rule:spoofing-securities-markets` advanced: new entry with the EU law (MAR Art. 12(1)(a) and 12(2)(c), Annex I, and Delegated Regulation 2016/522, Annex II, sec. 1, point 5(e), which names 'layering and spoofing', via CELLAR) and the U.S. statute (Exchange Act sec. 9(a)(1)-(2)); FINRA's rules (finra.org 404, then 429), Rule 10b-5 and enforcement remain. `rule:block-print-trade-through-current` narrowed: Rule 611(b)'s nine exceptions (eCFR, 15 October 2026), none for block size, merged into `def:block-trade`; FINRA trade-reporting and exchange cross rules remain. `rule:eu-si-national-transposition` narrowed slightly: a CELLAR title search found no Commission implementing act on SI notifications under MiFIR Art. 15(5) (Delegated Regulation 2026/482 noted, title only); other Member States remain. `ev:circuit-breaker-effects` narrowed: Kasahara and Yamada (JPX Working Paper 52, April 2026) find TSE single-stock pauses reduce volatility and spreads, against Hautsch and Horvath, in `mech:circuit-breakers-trading-halts`; price-limit and market-wide-halt studies remain. Unchanged, routes recorded: `ev:tick-size-primary-studies` (journal paywalls; Jones and Lipson's Columbia working paper not found) and `ev:dark-pool-price-discovery` (the published *Financial Management* 51(4) version, 2022, not openly available). The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Queue: `rule:spoofing-securities-markets` narrowed further (Rule 10b-5, FINRA Rules 2020 and 5210.03); `rule:block-print-trade-through-current` narrowed further (FINRA Rule 6380B reporting); `ev:circuit-breaker-effects` narrowed (SEC Release 34-93365 on the March 2020 market-wide halts); `ev:dark-pool-price-discovery` narrowed (Comerton-Forde and Putniņš, accepted manuscript); `ev:tick-size-primary-studies` and `rule:eu-si-national-transposition` unchanged. The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `ev:circuit-breaker-effects` narrowed (Chen, Gao, He, Jiang and Xiong on Shenzhen daily price limits (NBER WP 24014, abstract and sec. 1) merged into `mech:circuit-breakers-trading-halts`); `ev:dark-pool-price-discovery` narrowed (the published version's abstract (Financial Management 2022) adds 2020: dark pools improve spreads in 2009 but worsen market quality for large caps in 2020; full text not obtained); `rule:spoofing-securities-markets` narrowed (FINRA Regulatory Notice 17-22 read: Rule 5210.03 has no express intent element and supports an expedited cease-and-desist order; enforcement actions unread); `rule:block-print-trade-through-current` narrowed (NYSE Rules 76 and 127 (compilation of May 2019) read: a block cross outside the quote trades with the NYSE best bid or offer and better-priced book orders first, then has priority at its price; merged into `def:block-trade`); `ev:market-share-variance-claim` narrowed (the only formal counterpart in Lehalle and Laruelle is an appendix assumption; no study cited). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 migrated the three blocks assigned here and removed the legacy microstructure chapter; no legacy file now lists this pathway.

## What changed in my view or practice

## Questions carried forward

- The European best-execution regime in `def:best-execution` is as of Lehalle and Laruelle (2018). Slice 35 retrieved the original MiFID II, MiFIR and 2024/791 texts through the EU Publications Office's CELLAR service (EUR-Lex's HTML pages return an empty bot-check response), but did not read MiFID II Art. 27 or its delegated acts, so no current EU best-execution rule is stated.
- Passive splits assume fixed queues and fill rates; how much do cancellations ahead and queue dynamics change them?
- The regulatory statements in `def:best-execution` predate Rules 605 and 606 as amended in 2024 and the 2025 withdrawal; update them from `ex-sec-rule605-2024` and `ex-sec-withdrawal-2025`.
