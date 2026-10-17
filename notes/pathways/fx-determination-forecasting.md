---
key: fx-determination-forecasting
section: currency-markets
status: not started (draft entries from the migration only)
---

# Exchange-rate determination, forecasting and order flow

Pathway outcome, from the guide: test exchange-rate forecasts against a random walk with economic as well as statistical criteria, and explain the forward-premium puzzle, the disconnect from fundamentals and the roles of order flow and financial flows. Its 18 required readings: `s16-r10`, `ma-engel-west-2005`, `ma-rossi-2013`, `ma-molodtsova-papell-2009`, `ma-della-corte-sarno-tsiakas-2009`, `ma-engel-wu-2023`, `s16-r33`, `ma-engel-1996`, `cur-engel-2016`, `ma-taylor-taylor-2004`, `wide-evans-lyons-orderflow`, `w3-burnside-fx-order-flow`, `cur-froot-ramadorai-2005`, `cur-camanho-hau-rey-2022`, `ma-gabaix-maggiori-2015`, `ma-itskhoki-mukhin-2021`, `cur-lilley-maggiori-neiman-schreger-2022`, `w3-jiang-richmond-zhang-dollar`. This note is for a pathway of the section `currency-markets`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the FX valuation block of the legacy chapter; `02_transmission_maps.tex` named this pathway as a candidate. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `meth:fx-valuation-signals`: Gliner's currency factors from equity flows to rate differentials, with his Balassa--Samuelson and Meese--Rogoff descriptions corrected.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:fx-valuation-factors-oos` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `ev:fx-valuation-factors-oos` empirically tested for one factor, relative PPP (own bounded test, protocol fixed before computing; `notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py`, results and panel beside it): for nine currencies against the dollar, 1985 to 2021-2026, the real-exchange-rate deviation has the expected sign in-sample but loses to a random walk out of sample (pooled 12-month OOS R^2 -15.3 percent), and a cheap-minus-dear portfolio earns about zero; written into `meth:fx-valuation-signals`. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:fx-carry-trade` (`fx-premia`); `def:macroeconomic-indicators` (`macro-nowcasting-signals`).

## Entry backlog

- ev:fx-valuation-factors-oos: out-of-sample tests of Gliner's other factors (equity flows, sovereign CDS, risk reversals, trade and TWI, export-partner growth, debt, GDP per capita, carry indicators), which need data not used here; relative PPP was tested on 2026-10-17 (not supported statistically or economically; `meth:fx-valuation-signals`)

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward
