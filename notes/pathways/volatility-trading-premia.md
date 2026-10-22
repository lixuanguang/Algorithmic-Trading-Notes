---
key: volatility-trading-premia
section: volatility-trading-premia
status: not started (draft entries only, not from study)
---

# Volatility trading, option premia and implied information (section overview)

A compendium section in Part III, *Public markets and pricing*, declared in `compendium/compendium.tex`. Overview outcome, from the guide: Measure the variance risk premium and risk-neutral volatility and skewness in index and single-stock options, and test how much of the premium survives crash months, quoted spreads and margin.

Its checkpoint, from the guide: For SPX and five liquid single stocks, compute each month the at-the-money implied volatility, model-free implied variance and risk-neutral skewness, then the next month's realised variance and the delta-hedged return of a short at-the-money straddle. Report the average variance premium, its losses in crash months and how much of it survives quoted spreads and margin.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Populated before this note existed; the content migration of 22 October 2026 added this overview without changing the entries' verification, coverage or mastery state. Entry histories and source-review references are in [portfolio-construction-risk.md](portfolio-construction-risk.md), [vix-correlation-dividends.md](vix-correlation-dividends.md).

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries

By pathway, in compiled order: each printed pathway is a numbered section of the chapter, and a pathway with several topic files prints each as a subsection.

- `vix-correlation-dividends` (VIX, correlation and dividend derivatives; `vix-variance-dividends.tex`): `def:vix-variance-dividend-swaps`.

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `vix-correlation-dividends`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `option-premia-dealers` (Option returns, variance premia and dealer hedging): no pathway note; partial treatment in existing entries, not reviewed as complete: the variance risk premium in variance-swap strikes and selling variance (`def:vix-variance-dividend-swaps` in `volatility-trading-premia/vix-variance-dividends`, `meth:volatility-derivative-applications` in `portfolio-construction-risk/derivative-overlays`); hedged-option profit when implied and realised volatility differ (`res:delta-hedging-volatility-mismatch` in `volatility-options/option-hedging`); dealers' hedging and inventory risk in option spreads (`res:option-market-maker-spreads` in `execution-market-making/options-dealing`). Not written: option-return evidence; dealer gamma positioning and its effect on the underlying.
- `option-implied-information` (Option-implied densities, tail risk and expected returns): no pathway note; partial treatment in existing entries, not reviewed as complete: the butterfly condition as a non-negative implied density (`def:implied-volatility-surface` in `volatility-options/option-pricing`); risk-neutral probabilities from call spreads (`meth:derivative-overlay-allocation` in `portfolio-construction-risk/derivative-overlays`). Not written: density extraction; tail-risk and implied-moment measures; their return predictability.
- `equity-option-returns` (Single-stock option returns: volatility mispricing, characteristics and factors): content gap; no entry written.
- `vix-correlation-dividends` (VIX, correlation and dividend derivatives): pathway note [vix-correlation-dividends.md](vix-correlation-dividends.md), 1 entries listed, in `volatility-trading-premia/vix-variance-dividends`.
- `short-dated-retail-options` (Short-dated options, 0DTE and retail option trading): no pathway note; partial treatment in existing entries, not reviewed as complete: retail option routing, payment for order flow and wholesaler internalisation (`mech:options-retail-wholesaler-routing` in `execution-market-making/options-dealing`). Not written: 0DTE options; retail option returns and behaviour.

## Entry backlog

## What changed in my view or practice

## Questions carried forward
