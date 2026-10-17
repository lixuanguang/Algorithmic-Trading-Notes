---
key: equity-long-short-construction
section: systematic-equities
status: not started (draft entries from the migration only)
---

# Equity long/short construction

Pathway outcome, from the guide: turn several equity signals into one market-, sector- and style-neutral portfolio: scale forecasts, combine signals, align the risk model with the alpha, choose neutralisation and the short side, and net the result of realistic trading costs. Its checkpoint combines at least four signals into daily forecasts scaled by volatility and information coefficient, builds neutral portfolios with a factor risk model, compares mixing with integrating the signals, and reports the transfer coefficient, risk, turnover, borrow costs and net Sharpe ratio. Its sixteen readings run from Grinold's forecast scaling (`s7-grinold`, `eq-grinold-1994`) and Qian's portfolio construction (`alpha-qian`), through risk models (`wide-menchero-barra-use4`, `eq-ceria-saxena-stubbs-2012`), signal combination and mixing against integrating (`eq-fitzgibbons-2017`, `w5-kakushadze-tulchinsky-4000`), to parametric portfolios, factor costs and dynamic trading with costs (`wide-brandt-parametric`, `eq-frazzini-israel-moskowitz-2018`, `exp-garleanu-pedersen-dynamic-costs`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 30 (`notes/migration-slices.md`), which routed the *Blending of Models* block of the legacy alpha-models file (`sysinv/alphamod.tex`, mapped to the section overview `portfolio-construction-risk`) here, because combining signals into one forecast is this pathway's outcome. The block's third item, on the cost of machine-learning research, came from López de Prado and went to `model-governance-controls`. The entry comes from source checking against `s7-narang` (third edition, 2024), not a reading of this pathway; none of the readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 30, 2026-10-15:

- `meth:alpha-signal-combination`: Narang's linear (regression or equal weights), conditional and rotational combinations, machine-learning weights, and not combining at all; his example checked; "linear" read as additive, not as statistically independent factors; rotation and machine-learning claims kept as his unsupported judgements.

Partly checked 2026-10-15, draft; human review outstanding. Its artefact is `notes/artefacts/portfolio-construction-risk/alpha-models.tex`.

- `meth:forecast-scaling-ic`: refined forecast = volatility x IC x score, its regression form and the two-signal combination (Grinold and Kahn, chap. 10). Partly checked 2026-10-17, draft.

## Source verification after slice 37

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `meth:forecast-scaling-ic` resolved as a new entry in `systematic-equities/signal-combination.tex` from Grinold and Kahn's second edition, chap. 10 (pp. 261-271, the rule of thumb on p. 266 as a page image; the binary-model IC, the two-signal weights and combined IC, and Table 10.1 recomputed in `notes/artefacts/equity-long-short-construction/batch40-forecast-checks.py`). Grinold's 1994 paper (`eq-grinold-1994`) is behind the publisher's login and his 1989 paper was not read. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:alpha-model-taxonomy` and `meth:alpha-strategy-specification` (`portfolio-construction-risk`); `meth:signal-portfolio-allocation`, `meth:rule-based-position-sizing` and `mod:mean-variance-portfolio-optimisation` (`portfolio-construction`); `pit:parameter-overfitting` (`backtest-inference`); `meth:strategy-production-lifecycle` (`model-governance-controls`).

## Entry backlog

- meth:signal-mixing-vs-integration: combining signals into one forecast before optimising against optimising on them separately, with the transfer coefficient (`eq-fitzgibbons-2017`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its slice-30 material came from a file mapped to the overview `portfolio-construction-risk`.

## What changed in my view or practice

## Questions carried forward
