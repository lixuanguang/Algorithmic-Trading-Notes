---
key: multi-asset-systematic-macro
section: multi-asset-systematic-macro
status: not started (draft entries only, not from study)
---

# Multi-asset and systematic macro

Pathway outcome, from the guide: attribute a cross-asset portfolio's returns to carry, trend, value and rate exposures, using signals built from release vintages and tradable contract rolls, and show how funding haircuts, trading costs and a rapid unwind change the result. Its 8 required readings: `s7-ilmanen`, `wide-dimson-marsh-staunton`, `alpha-carry`, `s6-tsmom`, `s16-r11`, `exp-adrian-crump-moench-term-structure`, `exp-brunnermeier-pedersen-liquidity`, `exp-garleanu-pedersen-dynamic-costs`. This note is for the section overview.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page) and Drobny (`s7-drobny`, *Inside the House of Money*, Wiley 2006 printing, checked interview by interview). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:global-macro-strategy`: global macro as Gliner defines it: discretionary, systematic, high-frequency and CTA approaches; directional, relative-value and thematic trades; the four product groups; multi-asset expression of a view; unsourced "structural reasons" for the strategy kept as hypotheses.
- `ev:global-macro-crisis-performance`: Gliner's index record (Barclays Global Macro Index 2002--2012, DJCS 1995--2013) and conditional correlation with equities, with the limits of hedge-fund index data.
- `meth:macro-position-sizing-risk`: Turtle-style volatility units (N is an average true range, not a standard deviation), 1:3 risk/reward, gap risk, P&L-contingent VaR utilisation, stress tests, performance ratios and correlation against beta.
- `meth:macro-practitioner-frameworks`: Drobny's interviewees with attributions corrected (anonymous currency manager, Andres Drobny, Porter, Rogers) and Porter's "90 percent" quote restored.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `ev:global-macro-returns-after-2013` narrowed; `ev:practitioner-rules-tested` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): Two empirical stubs remain open; executable protocols are now recorded in the backlog, and nothing was computed (a protocol is not evidence). `ev:global-macro-returns-after-2013`: the macro hedge-fund index data are not public (BarclayHedge's index pages redirect to its home page, Eurekahedge requires sign-in, HFR requires registration, checked 2026-10-17). `ev:practitioner-rules-tested`: no trade-level data; a systematic proxy would test the rules on that proxy, not on the practitioners' trades, and was not attempted. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `ev:global-macro-returns-after-2013` empirically tested within bounds on the only public series found (Barclay Global Macro Index, January 2022 to July 2026): down-month mean -0.39 percent (t -1.5), crisis protection not supported by the pre-set rule; `ev:practitioner-rules-tested` unchanged (trade-level data missing). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:global-macro-returns-after-2013` tested (the BarclayHedge window January 2014 to July 2026 run as registered: 53 down months, mean $-0.52$ percent, $t=-3.00$; the registration statements corrected). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog: `ev:global-macro-returns-after-2013` rewritten as complete within its stated scope; the registration blocker removed. Correction to the third-batch paragraph above: "run as registered" should read "run under the protocol recorded in method validation (2026-10-17)"; no preregistration occurred, and the window was not registered with anyone. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:macro-regime-asset-map` (`macro-regimes-stock-bond`); `meth:equity-index-valuation` (`cross-asset-style-premia`); `mod:fx-carry-trade` (`fx-premia`); `meth:curve-trades-carry-rolldown` (`curve-term-structure`); `meth:relative-performance-evaluation` (`performance-manager-evaluation`).

## Entry backlog

- ev:global-macro-returns-after-2013: complete within its stated scope: the protocol's window, January 2014 to July 2026, was run on the public BarclayHedge workbook (53 down months, mean index return in them -0.52 percent, t = -3.00: crisis protection not supported), with the 2022-2026 run kept. What remains is outside that scope: the index's weighting and backfill rules, which BarclayHedge does not publish, and whether other macro indices (HFR, Eurekahedge; sign-in required) agree.
- ev:practitioner-rules-tested: do the Drobny practitioners' rules (1:3 against 4:1 reward-to-risk exits, re-entry counting the incurred loss, a month off after a portfolio-wide stop-out, P&L-contingent VaR limits) improve risk-adjusted results? Protocol: on trade-level data (entries, exits, sizes, P&L, targets, stops), replay each rule on the same entries; compare expectancy, Sharpe with Lo's standard error and drawdowns, with the deflated Sharpe ratio over all variants tried and a block bootstrap after stop-out events. Missing: trade-level data of a discretionary macro book; a systematic proxy on public futures would answer a different question and was not run.

## What changed in my view or practice

## Questions carried forward

- Drobny: page numbers are from the 2006 printing; the 2013 revised edition (EPUB, compared on 2026-10-18 for the quotations used and Bessent's passages) lacks Andres Drobny's interview, so those attributions rest on 2006 alone. Read the rest of the 2013 edition.
- Which of the earlier notes' "structural reasons" for macro (policy jumps, sticky capital, under-arbitraged links) do the section's readings support?
