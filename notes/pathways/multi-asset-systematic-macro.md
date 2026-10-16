---
key: multi-asset-systematic-macro
section: multi-asset-systematic-macro
status: not started (draft entries from the migration only)
---

# Multi-asset and systematic macro

Pathway outcome, from the guide: attribute a cross-asset portfolio's returns to carry, trend, value and rate exposures, using signals built from release vintages and tradable contract rolls, and show how funding haircuts, trading costs and a rapid unwind change the result. Its 8 required readings: `s7-ilmanen`, `wide-dimson-marsh-staunton`, `alpha-carry`, `s6-tsmom`, `s16-r11`, `exp-adrian-crump-moench-term-structure`, `exp-brunnermeier-pedersen-liquidity`, `exp-garleanu-pedersen-dynamic-costs`. This note is for the section overview.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 37 (`notes/migration.md`), which routed here the legacy chapter's strategy, record, sizing and practitioner blocks, two of whose files named this overview as a candidate. The entries come from migration and source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page) and Drobny (`s7-drobny`, *Inside the House of Money*, Wiley 2006 printing, checked interview by interview). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 37, 2026-10-16:

- `def:global-macro-strategy`: global macro as Gliner defines it: discretionary, systematic, high-frequency and CTA approaches; directional, relative-value and thematic trades; the four product groups; multi-asset expression of a view; the legacy's unsourced "structural reasons" kept as hypotheses.
- `ev:global-macro-crisis-performance`: Gliner's index record (Barclays Global Macro Index 2002--2012, DJCS 1995--2013) and conditional correlation with equities, with the limits of hedge-fund index data.
- `meth:macro-position-sizing-risk`: Turtle-style volatility units (N is an average true range, not a standard deviation), 1:3 risk/reward, gap risk, P&L-contingent VaR utilisation, stress tests, performance ratios and correlation against beta.
- `meth:macro-practitioner-frameworks`: Drobny's interviewees with attributions corrected (anonymous currency manager, Andres Drobny, Porter, Rogers) and Porter's "90 percent" quote restored.

All: verification partly checked 2026-10-16, stability draft; human review outstanding. The legacy wording is kept in `notes/artefacts/multi-asset-systematic-macro/`.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `ev:global-macro-returns-after-2013` narrowed; `ev:practitioner-rules-tested` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:macro-regime-asset-map` (`macro-regimes-stock-bond`); `meth:equity-index-valuation` (`cross-asset-style-premia`); `mod:fx-carry-trade` (`fx-premia`); `meth:curve-trades-carry-rolldown` (`curve-term-structure`); `meth:relative-performance-evaluation` (`performance-manager-evaluation`).

## Entry backlog

- ev:global-macro-returns-after-2013: monthly returns of a named macro hedge-fund index (Credit Suisse/DJCS, Barclay or HFR) from 2014 to date and their correlation with the S&P 500 in down months, from the index provider's data (not public on the pages tried); a reading cannot replace that data.
- ev:practitioner-rules-tested: an empirical test of the practitioners' rules (1:3 against 4:1 targets, re-entry with the incurred loss counted, a month off after a portfolio-wide stop-out, P&L-contingent VaR limits) on trade-level data; the follow-up only rechecked what each interviewee said (Drobny 2006, pp. 85, 131-132), which is not evidence that the rules work.

## Legacy candidate material

None: the legacy chapters were all migrated by slice 37.

## What changed in my view or practice

## Questions carried forward

- Inspect the 2013 revised edition of Drobny that the catalogue names; page numbers here are from the 2006 printing.
- Which of the legacy's "structural reasons" for macro (policy jumps, sticky capital, under-arbitraged links) do the section's readings support?
