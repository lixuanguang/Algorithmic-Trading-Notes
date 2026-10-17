---
key: risk-tail-systemic
section: portfolio-construction-risk
status: not started (one backlog item from the migration only)
---

# Market risk, tail hedging and systemic stress

Pathway outcome, from the guide: forecast and backtest VaR and ES, design a tail hedge, and run a stress test that includes fire-sale and network spillovers. Its checkpoint forecasts 1-day 99% VaR and 97.5% ES for a multi-asset portfolio with filtered historical simulation and an EVT model, backtests them with Kupiec, Christoffersen and an ES scoring function, and runs a scenario stress with a fire-sale overlay. Its fifteen readings run from risk-measure theory and estimation (`wide-christoffersen-elements`, `s7-qrm`, `s7-artzner`, `wide-acerbi-tasche-es`), through backtesting (`wide-kupiec-backtest`, `wide-christoffersen-interval`, `wide-fissler-ziegel`) and regulation (`wide-bcbs-frtb`), to tail hedging and systemic stress (`wide-kelly-jiang-tail`, `wide-bhansali-tail`, `wide-rebonato-stress`, `wide-adrian-brunnermeier-covar`, `wide-brownlees-engle-srisk`, `wide-greenwood-landier-thesmar`, `wide-cont-schaanning`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration risk models review (`notes/source-review-records.md`), which routed the *Statistical Models* block of the legacy risk-models file (`sysinv/riskmod.tex`, mapped to `portfolio-construction`) here as a backlog item. The block lists historical simulation, Monte Carlo simulation and parametric methods for computing risk measures, which is this pathway's outcome (VaR and ES estimation), not portfolio covariance. It is generic text that Narang's risk-model chapter does not contain, so no entry was written from it. None of the pathway's readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

None yet.

method validation (2026-10-17):

- `meth:var-es-estimation-methods`: historical, filtered historical, parametric and Monte Carlo VaR and ES as overlapping choices, and the unconditional coverage backtest. Partly checked 2026-10-17, draft.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:var-es-estimation-methods` resolved as a new entry in `portfolio-construction-risk/risk-models.tex` (Christoffersen, 2nd ed., chaps. 2, 6, 8 and 13; own GARCH backtest simulation); QRM and Kupiec not read. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:factor-risk-model` and `mod:mean-variance-portfolio-optimisation` (`portfolio-construction`; the latter records Narang's description of VaR-based leverage, not adopted as a definition of VaR); `def:common-investor-contagion` (`funding-crowding`; VaR-based deleveraging in August 2007).

## Entry backlog


## Legacy candidate material

Run `python3 tools/check_compendium.py` for the current counts. No legacy file lists this pathway; its risk models review item came from a file mapped to `portfolio-construction`.

## What changed in my view or practice

## Questions carried forward
