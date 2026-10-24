---
key: risk-tail-systemic
section: portfolio-construction-risk
status: not started (one backlog item only, not from study)
---

# Market risk, tail hedging and systemic stress

Pathway outcome, from the guide: forecast and backtest VaR and ES, design a tail hedge, and run a stress test that includes fire-sale and network spillovers. Its checkpoint forecasts 1-day 99% VaR and 97.5% ES for a multi-asset portfolio with filtered historical simulation and an EVT model, backtests them with Kupiec, Christoffersen and an ES scoring function, and runs a scenario stress with a fire-sale overlay. Its fifteen readings run from risk-measure theory and estimation (`wide-christoffersen-elements`, `s7-qrm`, `s7-artzner`, `wide-acerbi-tasche-es`), through backtesting (`wide-kupiec-backtest`, `wide-christoffersen-interval`, `wide-fissler-ziegel`) and regulation (`wide-bcbs-frtb`), to tail hedging and systemic stress (`wide-kelly-jiang-tail`, `wide-bhansali-tail`, `wide-rebonato-stress`, `wide-adrian-brunnermeier-covar`, `wide-brownlees-engle-srisk`, `wide-greenwood-landier-thesmar`, `wide-cont-schaanning`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by risk models review (`notes/source-review-records.md`). Its backlog item, historical simulation, Monte Carlo simulation and parametric methods for computing risk measures, is this pathway's outcome (VaR and ES estimation); Narang's risk-model chapter does not cover it. None of the pathway's readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

None yet.

method validation (2026-10-17):

- `meth:var-es-estimation-methods`: historical, filtered historical, parametric and Monte Carlo VaR and ES as overlapping choices, and the unconditional coverage backtest. Partly checked 2026-10-17, draft.

Written in library gap-filling Batch L2 (2026-10-21), in `portfolio-construction-risk/risk-models.tex`:

- `meth:extreme-value-tail-estimation`: block maxima and the GEV family, peaks over threshold and the GPD, POT VaR and ES, the Hill estimator, threshold bias against sampling error, and the two-step GARCH-GPD method. `meth:var-es-estimation-methods` now links to it from its Pitfalls.

Partly checked 2026-10-21, draft. Checks in `trading_notes.numerical.extreme_values.extreme_value_checks` (synthetic; no empirical EVT claim, backlog B9). Sources: Hull, *RMFI* 6th ed., secs. 8.4 and 12.5-12.6; McNeil, Frey and Embrechts, *QRM*, 1st ed. (2005), chap. 7; Wilmott, sec. 19.8. Human review outstanding. See [record](../source-review-records.md#library-gap-filling-batch-l2-21-october-2026).

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:var-es-estimation-methods` resolved as a new entry in `portfolio-construction-risk/risk-models.tex` (Christoffersen, 2nd ed., chaps. 2, 6, 8 and 13; own GARCH backtest simulation); QRM and Kupiec not read. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:factor-risk-model` and `mod:mean-variance-portfolio-optimisation` (`portfolio-construction`; the latter records Narang's description of VaR-based leverage, not adopted as a definition of VaR); `def:common-investor-contagion` (`funding-crowding`; VaR-based deleveraging in August 2007).

## Entry backlog

## What changed in my view or practice

## Questions carried forward
