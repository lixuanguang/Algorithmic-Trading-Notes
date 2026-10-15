---
key: reinforcement-learning-trading
section: ml-alternative-data
status: not started (draft entries from the migration only)
---

# Reinforcement learning for trading, hedging and execution

Pathway outcome, from the guide: formulate a trading, hedging or execution problem as an MDP, train a policy against a validated simulator and compare it with the control-theoretic benchmark. Its checkpoint trains an RL execution or hedging policy in a simulator calibrated to real data and compares it with Almgren–Chriss or delta hedging on cost and risk, reporting seeds, hyperparameter trials and out-of-sample degradation when the simulator is perturbed. Its twelve readings run from Sutton and Barto (`catalogue-0814`) and the surveys (`wide-hambly-xu-yang`, `wide-kolm-ritter-rl`) through continuous-time RL (`wide-wang-zariphopoulou-zhou`) to implementations and a validation study (`w2-ning-ddqn-execution`, `w4-brini-kolm-ppo-trading` and others).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 16 (`notes/migration.md`), which migrated the legacy reinforcement-learning-and-ML-in-execution file, mapped to this pathway alone. Its blocks set out a stochastic-control execution model and contrast control with learning; the model is the control-theoretic benchmark the outcome names. The entry comes from migration and source checking against Lehalle and Laruelle (`alpha-laruelle`, 2018 printing, app. A.7.3) and the arXiv version of `wide-hambly-xu-yang`, one of this pathway's required readings, read only in the passages the entry cites. That is not study of the readings: the other eleven are unread.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 16, 2026-10-15:

- `mod:cartea-jaimungal-execution`: the Cartea–Jaimungal objective, dynamics and HJB as presented by Lehalle and Laruelle, with the appendix's inconsistencies corrected (min against sup, the half-spread in the terminal condition, the inventory term, notation, the closed forms for $h_2$ and $h_1$); units, signs, constraints and terminal treatment; the Almgren–Chriss limit; qualified parameter intuition; and the contrast between control, model-based and model-free RL, and simulator against historical data.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/reinforcement-learning-trading/` (the legacy blocks verbatim and the numerical checks).

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:almgren-chriss-execution`, `def:implementation-shortfall` and `def:trading-envelope` (`execution-trading-costs`); `def:price-impact` (`price-impact-execution`).

## Entry backlog

- meth:hybrid-control-learning-execution: the legacy claim that hybrid execution uses control structure for constraints and machine learning for forecasts, fills and regime detection. Not in the passages read; Hambly, Xu and Yang report only a combination of the Almgren–Chriss solution with Q-learning (p. 34). Needs a primary source, for instance the cited study or `wide-kolm-ritter-rl`, before an entry is written.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 16 no legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Check the model against Cartea and Jaimungal's own papers or book (`crypto-cartea`), which the appendix cites but which were not consulted.
- Read `wide-hambly-xu-yang` in its journal version (*Mathematical Finance* 33(3), 2023); the arXiv v4 was used.
- How should learning from logged historical decisions, without interaction, be evaluated against the simulator-based training the checkpoint asks for?
