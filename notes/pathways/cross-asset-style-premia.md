---
key: cross-asset-style-premia
section: multi-asset-systematic-macro
status: not started (draft entries from the migration only)
---

# Cross-asset style premia: value, momentum, carry and defensive

Pathway outcome, from the guide: build value, momentum, carry and defensive strategies in equity indices, bonds, currencies and commodities, judge them against a century of out-of-sample evidence, and decide how far to time them. Its 12 required readings: `alpha-value`, `s16-r37`, `ma-asness-liew-stevens-1997`, `wide-ilmanen-century-factors`, `w5-baltussen-global-premiums`, `alpha-bab`, `ma-lettau-maggiori-weber-2014`, `ma-pitkajarvi-suominen-vaittinen-2020`, `s16-r16`, `ma-baltas-2019`, `ma-haddad-kozak-santosh-2020`, `ma-asness-chandra-ilmanen-israel-2017`. This note is for a pathway of the section `multi-asset-systematic-macro`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the legacy chapter's equity valuation and top-down blocks; not a candidate of any legacy file (routing exception). The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `meth:equity-index-valuation`: top-down country and sector selection and Gliner's valuation ratios (P/B thresholds, dividend yield, P/E, FCF yield, market cap to GDP), with his Tobin's q slip.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:equity-index-value-signal` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `ev:equity-index-value-signal` remains open with an executable protocol in the backlog: point-in-time country-level valuation data were not obtained (MSCI's are licensed; Ken French's international files give value portfolios within countries, not country-index book-to-price), so nothing was computed. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:equity-indices-derivatives` (`international-equity-markets`); `mod:fx-carry-trade` (`fx-premia`); `def:global-macro-strategy` (`multi-asset-systematic-macro`).

## Entry backlog

- ev:equity-index-value-signal: does cross-sectional value (book-to-price or earnings yield) across country equity indices predict relative returns out of sample, and do Gliner's fixed P/B thresholds (2.5 'overbought', p. 228) time markets? Protocol: monthly B/P and E/P with publication dates for 15-20 developed markets; rank each month, long the cheapest tercile and short the dearest, from a ten-year warm-up; returns in USD and local currency, net of an assumed futures or ETF cost; Sharpe with Lo's standard error and the deflated Sharpe ratio over variants; the threshold rule against buy-and-hold per market. Missing: point-in-time country valuation data (MSCI licensed; French's international files are within-country portfolios)

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward
