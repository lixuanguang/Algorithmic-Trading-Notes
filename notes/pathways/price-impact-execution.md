---
key: price-impact-execution
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Price impact, optimal execution and implementation shortfall

Pathway outcome, from the guide: estimate a price-impact model from executions, derive an optimal schedule and measure implementation shortfall with confidence intervals.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. This note was opened on 15 October 2026 by migration liquidity and impact review (`notes/source-review-index.md`), when three entries on price impact were migrated from the legacy liquidity-and-market-impact file into the new canonical chapter `compendium/execution-trading-costs/`. The entries were checked against Webster's handbook (`wide-webster-price-impact`, a required reading of this pathway) and against Bouchaud, Bonart, Donier and Gould (`catalogue-0528`, on no route). That is migration and source checking, not study of the readings. Gatheral (`catalogue-0501`) was not consulted and is cited only through Webster. In market-impact models review three required readings were read in open versions for source checking: `alpha-almgren` (author preprint of December 2000), `wide-bouchaud-propagator` (arXiv cond-mat/0307332v2) and `wide-bacry-life-cycle` (arXiv preprint of December 2014); their journal versions and pagination were not checked. In impact estimation review `wide-almgren-direct-impact` was read in the authors' preprint of 10 May 2005; `wide-toth-square-root` remains unread.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration liquidity and impact / source review / optimal execution / high-frequency strategies reviews:

- `def:price-impact`: unperturbed, observed and trade prices; reaction, observed and prediction impact; transient and permanent impact; the "temporary impact" ambiguity.
- `mod:propagator`: the propagator model of transient impact; response function and sign autocorrelation.
- `res:no-price-manipulation`: price manipulation as a round trip with negative expected cost; Webster's Obizhaeva–Wang example and the condition 2β+γ′>0; the closed-trajectory cost in the latent-liquidity model.

Written in migration market-impact models / source review / optimal execution / high-frequency strategies reviews, from the legacy market-impact-models file:

- `ev:square-root-impact`: the square-root law of metaorder impact, its range and conditions (`catalogue-0528`; confirmed in `wide-bacry-life-cycle`).
- `meth:post-execution-impact-profile`: Bacry et al.'s debiasing for later metaorders and index decomposition of post-execution prices.

Changed in market-impact models review: `def:price-impact` (model families from the Almgren–Chriss original; the three meanings of "temporary impact"; mechanical and informational views of permanent impact) and `mod:propagator` (the 2004 original read; kernel shapes and the fine balance; order splitting as the source of sign memory; legacy departures corrected).

Written in migration impact estimation / source review / optimal execution / high-frequency strategies reviews, from the legacy price-impact-estimation file:

- `ev:intraday-impact-profile`: the impact path during and after execution, and its dependence on participation and duration (`alpha-laruelle`; `wide-bacry-life-cycle`).
- `meth:almgren-impact-estimation`: Almgren et al.'s direct estimation of permanent and temporary impact from Citigroup orders (`wide-almgren-direct-impact`, preprint).
- `meth:order-flow-impact-regression`: the Glosten–Harris order-flow regression (`alpha-harris`, `s6-hasbrouck`).
- `ev:index-reconstitution-impact`: Russell reconstitution price pressure and reversal (`alpha-harris`, after Madhavan, not consulted).

Changed in impact estimation review: `def:price-impact` (execution-time measurement; timing), `ev:square-root-impact` (Almgren et al.'s 3/5 exponent; Bacry et al.'s duration factor), `meth:post-execution-impact-profile` (Lehalle and Laruelle's restatement of the procedure).

All nine: verification partly checked 2026-10-15, stability draft; human review outstanding. Their derivations artefact is `notes/artefacts/market-making-lob/derivations.tex`, where the migration has kept every removed block.

Written in migration order books and order flow / source review / optimal execution / execution control reviews, from the legacy trade-classification file (a map candidate):

- `meth:trade-sign-classification`: quote rule, tick rule and Lee--Ready as Harris and Hasbrouck describe them, the block-price rule, signed volume, and the limits of an inferred sign; Harris's 80 percent seller-initiated blocks kept as his unsourced report.

Partly checked 2026-10-16, draft; human review outstanding. Artefact: `notes/artefacts/price-impact-execution/trade-classification.tex`.

Changed in the order books and order flow review follow-up, 2026-10-16: `meth:trade-sign-classification` (the check now uses exact decimal prices and ten assertions; the order books and order flow review float version misclassified a half-tick midpoint trade after a downtick).

Changed in migration market design and liquidity / source review / optimal execution / execution control reviews (a routing exception from the foundations folder, whose candidates are `execution-market-making` and `market-structure-execution-quality`): `def:price-impact` took the legacy temporary-and-permanent impact mechanism as a restatement, with Harris's resiliency (pp. 400 and 403). Partly checked 2026-10-16, draft; human review outstanding.

## Entry backlog

- ev:block-initiator-asymmetry: the primary evidence behind Harris's 'approximately 80 percent' of large U.S. block trades being seller-initiated (p. 332), given without a citation, with sample, period and classification method; Saar (theory) and Alzahrani et al. (Saudi data) are merged.
- res:trade-sign-accuracy: the body of Ellis, Michaely and O'Hara (2000) (abstract only; paywalled, no open version found on 2026-10-17) and the other accuracy studies Jurkatis reviews; Lee and Ready (1991) report agreement rates and quote timing, not accuracy against known directions.

## Source verification after macro markets and pricing review

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `res:trade-sign-accuracy` narrowed (Jurkatis: about 98 percent of volume correct with nanosecond stamps, about 90 percent for Lee-Ready, EMO and CLNV at one-second stamps against 95 for his algorithm; interpolation lowers accuracy). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `res:trade-sign-accuracy` narrowed (Lee and Ready: Table I agreement of the tick test with quote classification 92.1 and 90.2 percent at the ask and bid, quotes recorded ahead of trades, the 5-second rule and n. 10 on other periods). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `res:trade-sign-accuracy` reviewed, unchanged: no lawful open copy of Ellis, Michaely and O'Hara (2000) was found (Cambridge's JFQA page is paywalled; the HKU repository record has no file), nor of the other accuracy studies. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `res:trade-sign-accuracy` narrowed (Ellis, Michaely and O'Hara's abstract from the publisher page: 76.4, 77.66 and 81.05 percent correct; merged into `meth:trade-sign-classification`). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `res:trade-sign-accuracy` unchanged (open versions of Ellis, Michaely and O'Hara and of the later accuracy studies were searched for and not found); `ev:block-initiator-asymmetry` narrowed (Harris gives the rule without a citation; Saar (theory) and Alzahrani et al. (Saudi data) merged). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Legacy candidate material

Run `python3 tools/check_compendium.py` for the current counts. The blocks exclusive to this pathway are in `compendium/legacy/execution-trading-costs/`. The legacy market-impact-models file was migrated and deleted in market-impact models review, and the price-impact-estimation file in impact estimation review. In optimal execution review the optimal-execution-problem file, shared with the section overview, was migrated to entries owned by `execution-trading-costs` (see that note), cross-referencing this pathway's impact entries. In execution algorithms review the execution-algorithms file, also shared with the overview, went to entries owned by `execution-trading-costs`; its envelope entry cross-references this pathway's impact models. No legacy block is now a candidate of this pathway alone; its 10 remaining candidates (after execution algorithms review) are shared, the nearest in `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/`.

## What changed in my view or practice

## Questions carried forward

- Gatheral's (2010) conditions on decay kernels and Fruth, Schöneborn and Urusov's (2013) condition are cited through Webster only. Check both against the papers.
- Is permanent impact identifiable at all beyond the horizon where price variance swamps the signal (`catalogue-0528`, p. 240)? Which design does `wide-bacry-life-cycle` use?
