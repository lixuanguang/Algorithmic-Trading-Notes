---
key: reinforcement-learning-trading
section: ml-alternative-data
status: not started (draft entries only, not from study)
---

# Reinforcement learning for trading, hedging and execution

Pathway outcome, from the guide: formulate a trading, hedging or execution problem as an MDP, train a policy against a validated simulator and compare it with the control-theoretic benchmark. Its checkpoint trains an RL execution or hedging policy in a simulator calibrated to real data and compares it with Almgren–Chriss or delta hedging on cost and risk, reporting seeds, hyperparameter trials and out-of-sample degradation when the simulator is perturbed. Its twelve readings run from Sutton and Barto (`catalogue-0814`) and the surveys (`wide-hambly-xu-yang`, `wide-kolm-ritter-rl`) through continuous-time RL (`wide-wang-zariphopoulou-zhou`) to implementations and a validation study (`w2-ning-ddqn-execution`, `w4-brini-kolm-ppo-trading` and others).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by execution control review (`notes/source-review-index.md`). The entry sets out a stochastic-control execution model and contrasts control with learning; the model is the control-theoretic benchmark the outcome names. The entry comes from source checking against Lehalle and Laruelle (`alpha-laruelle`, 2018 printing, app. A.7.3) and the arXiv version of `wide-hambly-xu-yang`, one of this pathway's required readings, read only in the passages the entry cites. That is not study of the readings: the other eleven are unread.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in execution control / source review / optimal execution / high-frequency strategies reviews:

- `mod:cartea-jaimungal-execution`: the Cartea–Jaimungal objective, dynamics and HJB as presented by Lehalle and Laruelle, with the appendix's inconsistencies corrected (min against sup, the half-spread in the terminal condition, the inventory term, notation, the closed forms for $h_2$ and $h_1$); units, signs, constraints and terminal treatment; the Almgren–Chriss limit; qualified parameter intuition; and the contrast between control, model-based and model-free RL, and simulator against historical data.

Corrected in a follow-up the same day (`notes/source-review-index.md`, *execution control review follow-up*): one consistent terminal payoff $Q_T(S_T-\psi/2-AQ_T)$, with the printed objective and its decomposition $g=H-x-qS$ kept apart under Pitfalls; a sufficient finite-value regime ($\kappa>0$, $\phi>0$, $A>b/2$, square-integrable policies and flow) and a counterexample outside it; the formal unconstrained benchmark kept apart from one-directional execution; $\sigma^2\int Q^2$ restricted to the Brownian contribution to variance; $b$ in currency per share$^2$.

Verification partly checked 2026-10-15, stability draft; human review outstanding. Its artefact is `notes/artefacts/reinforcement-learning-trading/` (the numerical checks).

## Source verification after macro markets and pricing review

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `meth:hybrid-control-learning-execution` narrowed (Kolm and Ritter's preprint (archived copy) has no hybrid design; the claim stays unsupported). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `mod:almgren-chriss-execution`, `def:implementation-shortfall` and `def:trading-envelope` (`execution-trading-costs`); `def:price-impact` (`price-impact-execution`).

## Entry backlog

- meth:hybrid-control-learning-execution: a primary source for execution that uses control structure for constraints and machine learning for forecasts, fills and regime detection. Kolm and Ritter's preprint has no hybrid design, and Hambly, Xu and Yang report only a combination of the Almgren-Chriss solution with Q-learning (p. 34); no entry until a source is found.

## What changed in my view or practice

## Questions carried forward

- Check the model against Cartea and Jaimungal's own papers or book (`crypto-cartea`), which the appendix cites but which were not consulted.
- Read `wide-hambly-xu-yang` in its journal version (*Mathematical Finance* 33(3), 2023); the arXiv v4 was used.
- How should learning from logged historical decisions, without interaction, be evaluated against the simulator-based training the checkpoint asks for?
