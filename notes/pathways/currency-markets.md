---
key: currency-markets
section: currency-markets
status: not started (draft entries only, not from study)
---

# Currency markets: exchange rates, premia and hedging

Pathway outcome, from the guide: from spot, forward and money-market rates, measure forward-implied carry, covered-interest-parity deviations and realised currency excess returns, and show how a carry portfolio behaves in the worst equity months. Its 6 required readings: `ma-engel-2014`, `gap-bis-fx-survey`, `wide-king-osler-rime`, `catalogue-0240`, `gap-cip`, `exp-bis-2026-carry-policy-transmission`. This note is for the section overview.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page), the IMF's SDR factsheet and the BIS's 2025 survey page as retrieved on 16 October 2026. That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:us-dollar-dxy-sdr`: the dollar's share of turnover and reserves (2013), the dollar index weights, the SDR basket as of 2022, and FX's three roles in macro.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

Written in the macro, allocation and currency batch (2026-10-19):

In `fx-mechanics-parity.tex`: `def:fx-market-real-exchange-rates`, `meth:cross-forward-rates`, `meth:fx-bid-offer-triangular-arbitrage`, `meth:currency-forward-mark-to-market`, `def:exchange-rate-regimes-capital-flows`, `res:international-parity-conditions`, `meth:exchange-rate-forecasting-fair-value`, `meth:carry-trade-uip` and `def:flows-policy-exchange-rates` (EIDM chaps. 9-10).

In `currency-management.tex`: `meth:currency-portfolio-effects`, `meth:currency-hedging-programme`, `meth:active-currency-strategies` and `meth:currency-hedge-cost-reduction` (PMiP chap. 8; Campbell, Serfaty-de Medeiros and Viceira).

All partly checked 2026-10-19, draft. Examples in `trading_notes.numerical.fx_mechanics_parity.fx_mechanics_checks` and `trading_notes.numerical.currency_management.currency_management_checks`; human review is outstanding. Coverage records are editorial, not study. `def:fx-market-structure`, `def:currency-regimes-intervention`, `ev:cip-deviations`, `mod:fx-carry-trade` and `mod:minimum-variance-hedge-ratio` are linked, not repeated.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:bis-2025-currency-shares` resolved (BIS 2025: the dollar on one side of 89.2 percent of trades in April 2025 (88.4 in 2022)); `conv:dxy-methodology` resolved (ICE's U.S. Dollar Index FAQ (June 2015): geometric average, constant 50.14348112, weights as Gliner gives them). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:fx-market-structure` (`fx-dealer-market-making`); `mod:fx-carry-trade` (`fx-premia`); `def:currency-regimes-intervention` (`em-currencies-intervention`); `meth:fx-valuation-signals` (`fx-determination-forecasting`).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `fx-determination-forecasting`, `fx-funding-settlement`, `fx-premia`, `fx-cip-dollar-funding`, `currency-hedging`, `em-currencies-intervention`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `fx-determination-forecasting` (Exchange-rate quotes, real exchange rates, determination and forecasting): pathway note [fx-determination-forecasting.md](fx-determination-forecasting.md), 1 entries listed, in `currency-markets/macro-fx`. Broadened by the guide revision of 22 October 2026 (`8302467`) to cover FX quotes and real exchange rates; its entries are in `currency-markets/fx-market`, `currency-markets/fx-mechanics-parity`, `currency-markets/macro-fx`.
- `fx-funding-settlement` (FX forwards, options, fixes and settlement): no pathway note; related existing material in `currency-markets/fx-quotes-forwards`, not reviewed as a complete treatment of the pathway.
- `fx-premia` (Currency premia: carry, momentum, value and the dollar): pathway note [fx-premia.md](fx-premia.md), 1 entries listed, in `currency-markets/currency-carry`.
- `fx-cip-dollar-funding` (Covered interest parity, the cross-currency basis and dollar funding): pathway note [fx-cip-dollar-funding.md](fx-cip-dollar-funding.md), 2 entries listed, in `currency-markets/cross-currency-basis`.
- `fx-volatility-crash-risk` (FX volatility, skew and crash risk): no pathway note; partial treatment in existing entries, not reviewed as complete: carry crash risk and negative skew (`meth:carry-trade-uip` in `currency-markets/currency-carry`, `mod:fx-carry-trade` in `currency-markets/currency-carry`); FX volatility trading with straddles and risk reversals (`meth:active-currency-strategies` in `currency-markets/currency-management`); option structures for currency hedging (`meth:currency-hedge-cost-reduction` in `currency-markets/currency-management`). Not written: FX volatility-surface quoting conventions; FX volatility and skew premia.
- `currency-hedging` (Currency hedging for international portfolios): no pathway note; related existing material in `currency-markets/currency-management`, not reviewed as a complete treatment of the pathway.
- `em-currencies-intervention` (Emerging-market currencies: regimes, intervention and the global financial cycle): pathway note [em-currencies-intervention.md](em-currencies-intervention.md), 1 entries listed, in `currency-markets/currency-intervention`.

## Entry backlog

## What changed in my view or practice

## Questions carried forward

Audit corrections, 19 October 2026: units, timing, pricing probabilities and source conventions corrected; Cedar and Lins decisions add complete alternatives and funding. See [correction record](../source-review-records.md#correction-pass-on-pr-26-19-october-2026). Editorial evidence only; not study, mastery or human review.
