---
key: market-making-lob
section: execution-market-making
status: not started (draft entries from the migration only)
---

# Market making, queues and limit-order-book models

Pathway outcome, from the guide: derive inventory-aware quotes, model queue dynamics and fill probabilities, and evaluate learned order-book signals.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. On 14 October 2026 the compendium migration pilot (`notes/migration.md`) wrote the entries below from the legacy notes, as a test of the entry format. They are supplemental models; of the pathway's required readings they touch only `s6-stoikov`, and the checkpoint has not been attempted. On 15 October 2026 a second migration slice added Glosten–Milgrom, from its 1983 working paper (`glosten-milgrom-1983`) rather than the journal version `s6-glosten`, and Harris's account of dealer inventory and quoting. A third slice, the same day, migrated the spread-decomposition and inventory-model files, checked against Harris and Hasbrouck (`s6-hasbrouck`, a required reading of the section overview route, not of this pathway) and O'Hara's account of Ho–Stoll. A fourth slice, also on 15 October 2026, migrated the volatility, bubble-and-crash and spread–volatility blocks of the volatility-and-liquidity file, checked against Harris, Hasbrouck and Lehalle and Laruelle (`alpha-laruelle`), and assigned that file's flash-crash and systemic blocks to `hft-market-design`. A fifth slice moved the entries that serve the section overview route to its new note, `execution-market-making.md`. That is migration and source checking, not study of the readings.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

- `mod:grossman-miller`: Grossman–Miller immediacy model (supplemental; risk-based price concession).
- `res:grossman-miller-trading-fees`: fee incidence in Grossman–Miller (supplemental).
- `res:grossman-miller-liquidity-measures`: linear impact and negative autocovariance in Grossman–Miller (supplemental).
- `mod:static-limit-order-depth`: static depth choice with exponential fill probability; a stand-in for, not a statement of, Ho–Stoll.
- `mod:avellaneda-stoikov`: inventory-aware quotes (`s6-stoikov`, a required reading).
- `mod:kyle-single-auction`: Kyle single-auction model (supplemental; information-based impact).

- `mod:glosten-milgrom`: Glosten–Milgrom sequential-trade model (the route's first reading, checked in its 1983 working paper).
- `res:glosten-milgrom-half-spreads`: two-value half-spreads (`crypto-cartea` simplification).
- `res:glosten-milgrom-market-collapse`: collapse with price-sensitive liquidity traders (`crypto-cartea`, corrected by its errata).
- `res:adverse-selection-spread-component`: Harris's $2\alpha e$ example (supplemental; formerly attributed to Glosten–Milgrom).
- `def:dealer-inventory-risk`: inventory imbalance; diversifiable and adverse-selection risk (Harris; supplemental).
- `meth:dealer-quote-adjustment`: dealer quote and size tactics for inventory and suspected informed trading (Harris; supplemental).

- `mod:inventory-based-quotes`: Stoll's CARA reservation quotes (Hasbrouck's version) and the Ho–Stoll properties as O'Hara reports them; the original papers not consulted.

Changed in slice 3: `res:adverse-selection-spread-component` (now also the total spread, Figure 14-1, the uninformed-traders lesson, and a correction of the legacy "twice the loss" claim; title changed, label kept), `def:dealer-inventory-risk` (inventory costs and the inventory premium) and `meth:dealer-quote-adjustment` (cross-references only).

The first six: verification partly checked 2026-10-14, stability draft. The next six: partly checked 2026-10-15, draft. The last: partly checked 2026-10-15 (slice 3), draft. `mod:kyle-single-auction` was changed on 2026-10-15: the `crypto-cartea` errata confirm its p. 33 misprint. Human review outstanding for all thirteen.

Moved on 2026-10-15 (slice 5) to the note for the section overview route, `execution-market-making.md`: the five spread-measurement entries of slice 3 and the four volatility entries of slice 4, which serve that route more than this pathway and were listed here only because it had no note.

Written in migration slice 33, 2026-10-16, from the legacy queue-dynamics and statistical-models-for-order-flow files and the queue-imbalance block of the order-flow-imbalance file:

- `def:queue-imbalance`: Bouchaud et al.'s $I$ and the legacy $QI=2I-1$, merged from two duplicate legacy definitions; INTC and CSCO, 2015.
- `mod:queue-reactive-intensities`: the Poisson baseline, Huang--Lehalle--Rosenbaum conditioning as Lehalle and Laruelle report it, the arrival--departure ratio, mean reversion and the reset; the legacy latency boundary as interpretation.
- `mod:hawkes-order-flow`: linear Hawkes processes with their conditions (non-negative causal kernels, norm or spectral radius below 1), parameterisations, inhibition only through a non-linear link, and calibrations with their samples; from Lehalle and Laruelle, Bouchaud et al. and `wide-bacry-hawkes` (a required reading, read in its arXiv version 2 for this slice; not studied).

All three: partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/market-making-lob/queue-dynamics-latency.tex` and `statistical-models-order-flow.tex`; simulations in `notes/artefacts/market-simulation/order-flow-checks.py`. The point-process definitions of the same file are owned by `market-simulation`.

Changed in the slice-33 follow-up, 2026-10-16: `mod:queue-reactive-intensities` (the claim that uniform-start and event-start waiting times agree "only for a Poisson process" replaced by the renewal result $E[X^2]/(2E[X])$, equal to $E[X]$ when the coefficient of variation is 1, with a non-exponential counterexample).

## Source verification after slice 37

Source follow-up of slices 33-36 and the slice-37 audit, 2026-10-16 (source verification, not study): `res:queue-reactive-models-hlr` resolved (Huang, Lehalle and Rosenbaum, arXiv v2: Theorem 2.1's two sufficient conditions, Model I MLE and invariant law with the shifted arrival/departure ratio, Models IIa-IIb, Cheuvreux data January 2010 to March 2012, Model III's 5 bp against 14 bp mechanical volatility and calibration 0.7 and 0.85; the journal version not compared); `ev:imbalance-placement-latency` narrowed (Lehalle and Mounjid read: sample, imbalance definition, the round-trip caveat and the latency factor). The record is in `notes/migration-slices.md`, *Source follow-up of slices 33-36 and slice-37 audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `ev:imbalance-placement-latency` unchanged (no new source in this batch; the gap recorded on 16 October 2026 stands). The record is in `notes/migration-slices.md`, *Second source follow-up of the slice 33-37 queue*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `res:avellaneda-stoikov-infinite-horizon` and `res:avellaneda-stoikov-exact-quotes` resolved by merge into `mod:avellaneda-stoikov` (author-hosted journal PDF, secs. 2.3 and 3.1, pp. 219-221, page images): the printed infinite-horizon bid matches the indifference definition, but the printed ask does not (it breaks symmetry at q = 0; own derivation and quadrature in `notes/artefacts/market-making-lob/batch40-model-checks.py`), recorded as an apparent misprint; eqs. (18)-(19) reduce to the exponential-intensity spread term. `res:grossman-miller-free-entry` and `res:grossman-miller-market-structure` resolved by merge into `mod:grossman-miller` (NBER WP 2641, eqs. (16)-(19), printed pp. 18-19, and printed pp. 9-10, page images): eq. (19) fixes t = e^{2ac} - 1, not the number of market makers, whose response to risk aversion is not monotone (own algebra, same script); the legacy 'until spread capture covers c' was loose. `ev:imbalance-placement-latency` resolved as to the evidence asked by merge into `def:queue-imbalance`: Gould and Bonart (arXiv v1) give out-of-sample ROC areas of 0.75-0.81 (large tick) and 0.58-0.64 (small tick) on a random 80/20 split of 2014 Nasdaq data, and Moallemi and Saglam (revision of 5 February 2013) price latency, their GS calibration reproduced; neither costs a placement rule, which stays with `lob-deep-learning`. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Misprint review: the Avellaneda-Stoikov infinite-horizon ask stays recorded as an apparent misprint with the printed formula quoted unchanged; a 2025 preprint (Balakaeva and Veretennikov, arXiv:2510.15988) prints the same ask without derivation, while its own value function and indifference definitions give the derived one. Queue: `res:nonlinear-hawkes-stability` narrowed (Brémaud and Massoulié's Theorems 4-5 as restated in Zhu's 2013 thesis, merged into `mod:hawkes-order-flow`; the original refused by Project Euclid's bot protection). The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `res:nonlinear-hawkes-stability` resolved (Brémaud and Massoulié (1996) read from an archived copy: a signed kernel is allowed and the condition is on the $L^1$ norm of $|h|$; merged into `mod:hawkes-order-flow`). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

## Related entries owned elsewhere

Written in slice 36 for `hft-market-design` and cross-referenced here: `res:queue-position-value`, from this pathway's reading `wide-moallemi-yuan-queue` (June 2017 revision; abstract, secs. 1--2, 4.3, 5.2 and 6 read, the value recursion of sec. 3 not checked). The cross-asset file, which listed this pathway, was routed to `execution-market-making`'s arbitrage entries (slice 36).

## Entry backlog

- res:ho-stoll-dealer-pricing: check against the paper the three properties O'Hara reports for the multiperiod model (spread = risk-neutral monopoly spread plus a risk adjustment rising with the horizon; transaction uncertainty does not enter; spread independent of inventory, quotes shifted instead) \citep[sec.~2.3, pp.~35--36]{catalogue-0496}; blocked: `ho-stoll-1981` has no accessible copy, and `catalogue-0527` names no paper

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Slice 36 removed the last legacy microstructure files; no legacy file now lists this pathway. Its blocks went, over slices 2--5, 33 and 36, to this pathway's entries above and to `execution-market-making`, `hft-market-design` and `market-structure-execution-quality`. Ho--Stoll is still unread (backlog).

## What changed in my view or practice

## Questions carried forward

- `crypto-cartea` p. 33 prints Kyle's $\lambda$ as $2\sigma_u/\sigma$: the authors' errata correct it to $\sigma/(2\sigma_u)$, as in `catalogue-0496` eq. (4.5) (checked 2026-10-15). Still to confirm against Kyle (1985), which has no open copy.
- Do the propositions and pages of the 1985 journal version of Glosten–Milgrom (`s6-glosten`) match the 1983 working paper the entries cite?
- Which Ho–Stoll paper does the route intend by `catalogue-0527`: Ho and Stoll (1981), or their 1980 paper on competing dealers that `s6-stoikov` also cites?
- Do O'Hara's three Ho–Stoll properties (pp. 35–36 of the 1998 printing) hold as stated in the paper, and under which approximation (first-order expansion, quadratic utility)?
- Roll's estimator: Harris (p. 434) says violations typically bias it down; Hasbrouck's Exercise 4.3 (pp. 38–39) shows signs correlated with information bias it up. Which dominates in practice is not settled by these passages.
