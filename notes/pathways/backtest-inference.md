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

- `meth:sharpe-ratio-standard-error`: Lo's IID and GMM standard errors and the time-aggregation factor eta(q). Partly checked 2026-10-17, draft.
- `meth:deflated-sharpe-ratio`: Bailey and López de Prado's expected maximum Sharpe ratio and deflated Sharpe ratio, with their example reproduced. Partly checked 2026-10-17, draft.

Second batch of 2026-10-17:

- `meth:multiple-testing-control`: familywise error, Bonferroni and Holm, the Reality Check and Romano and Wolf's StepM, with conditions and an own Monte Carlo. Partly checked 2026-10-17, draft.

## Source verification after slice 37

Batch of 2026-10-17 (source verification and bounded tests, not study or human review): `meth:sharpe-ratio-standard-error` and `meth:deflated-sharpe-ratio` resolved as new entries in `research-engineering-validation/backtest-evaluation.tex`: Lo (FAJ 2002, read in a copy hosted by a Berkeley student organisation, provenance not established; eqs. (9), (15), (17)-(22) and Table 2 checked as page images and recomputed) and Bailey and López de Prado (author version of 31 July 2014; SR0 = 0.1132 and DSR = 0.9004, 0.9505 at N = 46 and 0.9505 under normal returns at N = 88, all reproduced in `notes/artefacts/backtest-inference/batch40-sharpe-checks.py`). The 2026 López de Prado and Porcu paper was not obtained. The record is in `notes/migration-slices.md`, *Batch of 17 October 2026*.

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Audit repair: `meth:sharpe-ratio-standard-error` now states that 1 + SR^2/2 needs normal third and fourth moments (general IID form 1 - skew SR + (kurt - 1)/4 SR^2, finite fourth moment), records Lo's finite-variance wording at eq. (5) as an overstatement, scopes the sqrt(q) rule to additive returns with a consistent benchmark (zero autocovariances suffice), and adds counterexamples (`batch50-sharpe-conditions-checks.py`). Queue: `meth:multiple-testing-control` resolved as a new entry from Romano and Wolf's working paper (White and Benjamini-Hochberg described only as Romano and Wolf report them; own Monte Carlo); `meth:dependent-resampling-drawdowns` narrowed (own synthetic check, `batch50-drawdown-resampling-checks.py`; Politis and Romano not obtained); `ev:out-of-sample-r2-scale` narrowed (Welch and Goyal's Table 1 read; Campbell and Thompson refused, HTTP 429); `meth:backtest-protocol` blocked (Research Affiliates gate page, SSRN 403). The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here and not changed: `meth:relative-performance-evaluation` (`performance-manager-evaluation`; smoothed returns from stale valuations); `meth:transaction-cost-analysis`, `def:transaction-costs` (`execution-trading-costs`); `mech:securities-lending-short-sale`, `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). Checked and not linked: `meth:automated-trading-operational-controls` (`model-governance-controls`), which concerns production controls, not research.

## Entry backlog

- meth:multiple-testing-control: (narrowed; entry written 2026-10-17) White (2000) and Benjamini and Hochberg (1995) themselves, and the 2005 Econometrica version of Romano and Wolf.
- meth:backtest-protocol: a protocol fixed before experiments, against Narang's practitioner screening (`wide-arnott-harvey-markowitz`; blocked 2026-10-17: Research Affiliates served a gate page, SSRN HTTP 403; a third-party copy of unverified provenance not used).
- meth:dependent-resampling-drawdowns: (narrowed 2026-10-17: own AR(1) check shows shuffling understates the drawdown tail, 0.53 against 0.99, blocks 0.85; merged into `meth:backtest-evaluation-diagnostics`) Politis and Romano's paper itself (`wide-politis-romano-stationary`, not obtained).
- ev:out-of-sample-r2-scale: (narrowed 2026-10-17: Welch and Goyal's annual OOS R^2 all negative, e.g. d/p -2.06%, merged into `meth:backtest-evaluation-diagnostics`) Campbell and Thompson's restricted forecasts (`wide-campbell-thompson`; Harvard repository HTTP 429) and monthly horizons; belongs to `return-predictability`.
- ev:signal-decay-crowding: whether faster decay of a delayed signal measures crowding, as Narang suggests without evidence (`w3-kyle-crowded-markets`, `w4-chincarini-crowded-anomalies`, unread).
- data:historical-borrow-availability: point-in-time hard-to-borrow status and borrow fees for short-side backtests, which Narang says are hard to obtain; belongs to `point-in-time-data` (no source identified).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway; its slice-25 material came from a file mapped to the section overview.

## What changed in my view or practice

## Questions carried forward

- Which edition did the legacy notes follow? They match the 2024 third edition in wording and order, but the catalogue does not establish its edition for `s7-narang`.
- Narang's information ratio uses a zero benchmark and his Sterling ratio a downside deviation; check standard definitions before any formula entry uses these names.
