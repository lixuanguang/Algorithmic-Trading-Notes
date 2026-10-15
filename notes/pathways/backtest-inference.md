---
key: backtest-inference
section: research-engineering-validation
status: not started (draft entries from the migration only)
---

# Backtest inference, multiple testing and Sharpe-ratio statistics

Pathway outcome, from the guide: report a strategy result with the number of trials, multiplicity-adjusted significance and Sharpe-ratio uncertainty under dependence. Its checkpoint generates 200 variants of a simple signal, records every trial, and reports the best Sharpe ratio with Lo standard errors, a deflated Sharpe ratio, a Romano–Wolf stepdown test and BH-adjusted p-values, documenting the leakage checks run. Its sixteen readings run from p-hacking incentives (`wide-harvey-scientific-outlook`) and a backtesting protocol (`wide-arnott-harvey-markowitz`), through Reality Check, stepdown and false-discovery control, the factor-zoo thresholds, Sharpe-ratio standard errors and the stationary bootstrap, to the deflated Sharpe ratio and leakage and look-ahead audits.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 25 (`notes/migration-slices.md`). That slice routed all four blocks of the legacy research file (`sysinv/research.tex`, Narang's systematic-investing notes) here, an exception to the file's map candidate. The candidate was the section overview `research-engineering-validation`, whose outcome is reconstructing a research decision and its trade from versioned identities, data events, experiments and control records. The blocks are about forming hypotheses and judging backtests. The entries come from migration and source checking against `s7-narang` (third edition, Wiley 2024, chapter "Research"), which is not a reading of this pathway. None of the pathway's readings has been read, and the checkpoint was not attempted. The entries therefore describe one practitioner's diagnostics and say where the pathway's statistics are missing; they do not supply those statistics.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 25, 2026-10-15:

- `meth:hypothesis-driven-strategy-research`: Narang's scientific method (observation, theory, deduced consequences, attempted falsification, capital risked only on confidence) and his four sources of ideas; the legacy three-step version and the evidential weight of idea sources qualified.
- `meth:backtest-evaluation-diagnostics`: cumulative profit curve, average return, variability and lumpiness, drawdowns and recovery, $R^2$ and quantile buckets, win rates, Sharpe, information, Sterling, Calmar and Omega ratios as Narang defines them, fit with other strategies, and time decay; the smooth-P&L and lower-volatility heuristics, the $R^2$ of 0.05, the bucket text–figure mismatch and time decay as crowding qualified.
- `pit:parameter-overfitting`: isolated optima, nearby-parameter checks, plateaus, parsimony, the out-of-sample $R^2$ ratio and burnt out-of-sample data, and the third edition's balance against underfitting; parameter stability is not a correction for the number of trials.
- `pit:backtest-cost-short-assumptions`: over- and underestimated trading costs, and hard-to-borrow names a backtest could not have shorted; Narang's "naked short sale \dots illegal" not adopted, and borrow fees and recall added from the lending entries as interpretation.

Corrected 2026-10-15 (slice-25 follow-up): `meth:backtest-evaluation-diagnostics` now gives the S&P example's no-trade state (zero signal on 65% of days, threshold not stated) and writes Calmar and zero-threshold Omega with absolute-value denominators, kept apart from Narang's shorthand.

Corrected 2026-10-15 (slice-26 follow-up): the same entry now distinguishes the recomputed Calmar ratio, $12.1/39.7\approx0.3048$ (0.30 to two places), from Narang's reported 0.31 (pp. 173-174), drops "as reported" after 0.30, and no longer calls all the example figures consistent; the difference is left unexplained.

All four: verification partly checked 2026-10-15, stability draft; human review outstanding. The artefact is `notes/artefacts/research-engineering-validation/derivations.tex` (under the map candidate, keeping the file whole).

## Related entries owned elsewhere

Cross-referenced, not owned here and not changed: `meth:relative-performance-evaluation` (`performance-manager-evaluation`; smoothed returns from stale valuations); `meth:transaction-cost-analysis`, `def:transaction-costs` (`execution-trading-costs`); `mech:securities-lending-short-sale`, `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). Checked and not linked: `meth:automated-trading-operational-controls` (`model-governance-controls`), which concerns production controls, not research.

## Entry backlog

- meth:sharpe-ratio-standard-error: standard errors of an estimated Sharpe ratio under serial correlation, to replace the point estimates in the diagnostics (`wide-lo-sharpe`, unread).
- meth:deflated-sharpe-ratio: deflating the best Sharpe ratio for the number of trials and non-normality; parameter stability does not do this (`alpha-dsr`, `w4-lopezdeprado-porcu-dsr`, unread).
- meth:multiple-testing-control: Reality Check, Romano–Wolf stepdown and Benjamini–Hochberg control across a family of strategies (`catalogue-0731`, `wide-romano-wolf-stepdown`, `wide-benjamini-hochberg`, unread).
- meth:backtest-protocol: a protocol fixed before experiments, against Narang's practitioner screening (`wide-arnott-harvey-markowitz`, unread).
- meth:dependent-resampling-drawdowns: resampling returns with their dependence (stationary bootstrap) for drawdown distributions, against Narang's shuffle (`wide-politis-romano-stationary`, unread).
- ev:out-of-sample-r2-scale: out-of-sample $R^2$ magnitudes by horizon and design, against Narang's unsourced "superb $R^2$ \dots 0.05"; belongs to `return-predictability` (`wide-campbell-thompson`, `s7-welch`, unread).
- ev:signal-decay-crowding: whether faster decay of a delayed signal measures crowding, as Narang suggests without evidence (`w3-kyle-crowded-markets`, `w4-chincarini-crowded-anomalies`, unread).
- data:historical-borrow-availability: point-in-time hard-to-borrow status and borrow fees for short-side backtests, which Narang says are hard to obtain; belongs to `point-in-time-data` (no source identified).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its slice-25 material came from a file mapped to the section overview.

## What changed in my view or practice

## Questions carried forward

- Which edition did the legacy notes follow? They match the 2024 third edition in wording and order, but the catalogue does not establish its edition for `s7-narang`.
- Narang's information ratio uses a zero benchmark and his Sterling ratio a downside deviation; check standard definitions before any formula entry uses these names.
