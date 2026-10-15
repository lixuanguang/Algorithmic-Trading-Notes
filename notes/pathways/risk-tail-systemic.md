---
key: risk-tail-systemic
section: portfolio-construction-risk
status: not started (one backlog item from the migration only)
---

# Market risk, tail hedging and systemic stress

Pathway outcome, from the guide: forecast and backtest VaR and ES, design a tail hedge, and run a stress test that includes fire-sale and network spillovers. Its checkpoint forecasts 1-day 99% VaR and 97.5% ES for a multi-asset portfolio with filtered historical simulation and an EVT model, backtests them with Kupiec, Christoffersen and an ES scoring function, and runs a scenario stress with a fire-sale overlay. Its fifteen readings run from risk-measure theory and estimation (`wide-christoffersen-elements`, `s7-qrm`, `s7-artzner`, `wide-acerbi-tasche-es`), through backtesting (`wide-kupiec-backtest`, `wide-christoffersen-interval`, `wide-fissler-ziegel`) and regulation (`wide-bcbs-frtb`), to tail hedging and systemic stress (`wide-kelly-jiang-tail`, `wide-bhansali-tail`, `wide-rebonato-stress`, `wide-adrian-brunnermeier-covar`, `wide-brownlees-engle-srisk`, `wide-greenwood-landier-thesmar`, `wide-cont-schaanning`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 29 (`notes/migration-slices.md`), which routed the *Statistical Models* block of the legacy risk-models file (`sysinv/riskmod.tex`, mapped to `portfolio-construction`) here as a backlog item. The block lists historical simulation, Monte Carlo simulation and parametric methods for computing risk measures, which is this pathway's outcome (VaR and ES estimation), not portfolio covariance. It is generic text that Narang's risk-model chapter does not contain, so no entry was written from it. None of the pathway's readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

None yet.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:factor-risk-model` and `mod:mean-variance-portfolio-optimisation` (`portfolio-construction`; the latter records Narang's description of VaR-based leverage, not adopted as a definition of VaR); `def:common-investor-contagion` (`funding-crowding`; VaR-based deleveraging in August 2007).

## Entry backlog

- meth:var-es-estimation-methods: historical simulation, Monte Carlo simulation and parametric (distributional) estimation of VaR and ES, treated as overlapping choices rather than exclusive categories (filtered historical simulation combines a volatility model with historical residuals; Monte Carlo needs a parametric or resampled model to draw from), with their assumptions and backtests. To replace the legacy block's generic list, whose claim that the methods are "useful for dynamically updating risk assessments" needs evidence of better forecasts, not only of updating (`wide-christoffersen-elements`, `s7-qrm`, `wide-kupiec-backtest`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its slice-29 item came from a file mapped to `portfolio-construction`.

## What changed in my view or practice

## Questions carried forward
