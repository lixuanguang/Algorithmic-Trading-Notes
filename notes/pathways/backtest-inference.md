---
key: backtest-inference
section: research-engineering-validation
status: not started (draft entries only, not from study)
---

# Backtest inference, multiple testing and Sharpe-ratio statistics

Pathway outcome, from the guide: report a strategy result with the number of trials, multiplicity-adjusted significance and Sharpe-ratio uncertainty under dependence. Its checkpoint generates 200 variants of a simple signal, records every trial, and reports the best Sharpe ratio with Lo standard errors, a deflated Sharpe ratio, a Romano–Wolf stepdown test and BH-adjusted p-values, documenting the leakage checks run. Its sixteen readings run from p-hacking incentives (`wide-harvey-scientific-outlook`) and a backtesting protocol (`wide-arnott-harvey-markowitz`), through Reality Check, stepdown and false-discovery control, the factor-zoo thresholds, Sharpe-ratio standard errors and the stationary bootstrap, to the deflated Sharpe ratio and leakage and look-ahead audits.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. The entries come from source checking against `s7-narang` (third edition, Wiley 2024, chapter "Research"), which is not a reading of this pathway. None of the pathway's readings has been read, and the checkpoint was not attempted. The entries therefore describe one practitioner's diagnostics and say where the pathway's statistics are missing; they do not supply those statistics.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in backtest evaluation / source review / optimal execution / high-frequency strategies reviews:

- `meth:hypothesis-driven-strategy-research`: Narang's scientific method (observation, theory, deduced consequences, attempted falsification, capital risked only on confidence) and his four sources of ideas.
- `meth:backtest-evaluation-diagnostics`: cumulative profit curve, average return, variability and lumpiness, drawdowns and recovery, $R^2$ and quantile buckets, win rates, Sharpe, information, Sterling, Calmar and Omega ratios as Narang defines them, fit with other strategies, and time decay; the smooth-P&L and lower-volatility heuristics, the $R^2$ of 0.05, the bucket text–figure mismatch and time decay as crowding qualified.
- `pit:parameter-overfitting`: isolated optima, nearby-parameter checks, plateaus, parsimony, the out-of-sample $R^2$ ratio and burnt out-of-sample data, and the third edition's balance against underfitting; parameter stability is not a correction for the number of trials.
- `pit:backtest-cost-short-assumptions`: over- and underestimated trading costs, and hard-to-borrow names a backtest could not have shorted; Narang's "naked short sale \dots illegal" not adopted, and borrow fees and recall added from the lending entries as interpretation.

Corrected 2026-10-15 (backtest evaluation review follow-up): `meth:backtest-evaluation-diagnostics` now gives the S&P example's no-trade state (zero signal on 65% of days, threshold not stated) and writes Calmar and zero-threshold Omega with absolute-value denominators, kept apart from Narang's shorthand.

Corrected 2026-10-15 (model risk and contagion review follow-up): the same entry now distinguishes the recomputed Calmar ratio, $12.1/39.7\approx0.3048$ (0.30 to two places), from Narang's reported 0.31 (pp. 173-174), drops "as reported" after 0.30, and no longer calls all the example figures consistent; the difference is left unexplained.

All four: verification partly checked 2026-10-15, stability draft; human review outstanding.

- `meth:sharpe-ratio-standard-error`: Lo's IID and GMM standard errors and the time-aggregation factor eta(q). Partly checked 2026-10-17, draft.
- `meth:deflated-sharpe-ratio`: Bailey and López de Prado's expected maximum Sharpe ratio and deflated Sharpe ratio, with their example reproduced. Partly checked 2026-10-17, draft.

method validation (2026-10-17):

- `meth:multiple-testing-control`: familywise error, Bonferroni and Holm, the Reality Check and Romano and Wolf's StepM, with conditions and an own Monte Carlo. Partly checked 2026-10-17, draft.

## Source verification after macro markets and pricing review

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `meth:sharpe-ratio-standard-error` and `meth:deflated-sharpe-ratio` resolved as new entries in `research-engineering-validation/backtest-evaluation.tex`: Lo (FAJ 2002, read in a copy hosted by a Berkeley student organisation, provenance not established; eqs. (9), (15), (17)-(22) and Table 2 checked as page images and recomputed) and Bailey and López de Prado (author version of 31 July 2014; SR0 = 0.1132 and DSR = 0.9004, 0.9505 at N = 46 and 0.9505 under normal returns at N = 88, all reproduced in `notes/artefacts/backtest-inference/sharpe-checks.py`). The 2026 López de Prado and Porcu paper was not obtained. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Audit repair: `meth:sharpe-ratio-standard-error` now states that 1 + SR^2/2 needs normal third and fourth moments (general IID form 1 - skew SR + (kurt - 1)/4 SR^2, finite fourth moment), records Lo's finite-variance wording at eq. (5) as an overstatement, scopes the sqrt(q) rule to additive returns with a consistent benchmark (zero autocovariances suffice), and adds counterexamples (`sharpe-conditions-checks.py`). Queue: `meth:multiple-testing-control` resolved as a new entry from Romano and Wolf's working paper (White and Benjamini-Hochberg described only as Romano and Wolf report them; own Monte Carlo); `meth:dependent-resampling-drawdowns` narrowed (own synthetic check, `drawdown-resampling-checks.py`; Politis and Romano not obtained); `ev:out-of-sample-r2-scale` narrowed (Welch and Goyal's Table 1 read; Campbell and Thompson refused, HTTP 429); `meth:backtest-protocol` blocked (Research Affiliates gate page, SSRN 403). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `meth:multiple-testing-control` narrowed (Benjamini and Hochberg (1995) and White (2000) read and merged into `meth:multiple-testing-control`; Romano and Wolf unread); `meth:dependent-resampling-drawdowns` narrowed (White's restatement of Politis and Romano merged; the original and its validity for drawdowns unread); `ev:out-of-sample-r2-scale` resolved (Campbell and Thompson (NBER WP 11468) read: the $R^2/S^2$ scale and their Table 1 merged into `meth:backtest-evaluation-diagnostics`); `ev:signal-decay-crowding` narrowed (two crowding studies read at abstract level measure crowding from holdings or fire-sale dislocations, not from delayed-signal decay; noted in `meth:backtest-evaluation-diagnostics`); `data:historical-borrow-availability` narrowed (Nasdaq's daily Regulation SHO threshold files (public from January 2005) merged into `data:derived-market-statistics`; no public point-in-time borrow-fee source found). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `meth:multiple-testing-control`, `meth:dependent-resampling-drawdowns`, `ev:factor-zoo-hurdle` and `meth:sharpe-ratio-standard-error` questions: Hansen's SPA working paper and Harvey, Liu and Zhu's hurdle merged into `meth:multiple-testing-control`; Patton, Politis and White's block-length correction into `meth:backtest-evaluation-diagnostics`; Ledoit and Wolf's Sharpe-difference test into `meth:sharpe-ratio-standard-error`. Correction: the reconciled backlog line written earlier in this batch called Romano and Wolf's working paper unread; it had been read in method validation (2026-10-17), and the line now names only the published versions. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here and not changed: `meth:relative-performance-evaluation` (`performance-manager-evaluation`; smoothed returns from stale valuations); `meth:transaction-cost-analysis`, `def:transaction-costs` (`execution-trading-costs`); `mech:securities-lending-short-sale`, `def:securities-lending-fee-rebate` (`money-markets-repo-lending`). Checked and not linked: `meth:automated-trading-operational-controls` (`model-governance-controls`), which concerns production controls, not research.

## Entry backlog

- meth:multiple-testing-control: the published versions of the two stepwise tests, Romano and Wolf (Econometrica 2005) and Hansen's SPA test (JBES 2005); both working papers (UPF 712, October 2003; Brown 01-06, November 2001) are in the entry, with Benjamini and Hochberg, White and Harvey, Liu and Zhu.
- meth:backtest-protocol: a protocol fixed before experiments, against Narang's practitioner screening (`wide-arnott-harvey-markowitz`: Research Affiliates served a gate page and SSRN HTTP 403 on 2026-10-17; a third-party copy of unverified provenance was not used).
- meth:dependent-resampling-drawdowns: Politis and Romano's stationary bootstrap paper itself (`wide-politis-romano-stationary`; only White's restatement and Patton, Politis and White's 2009 block-length correction are read), and whether block resampling is valid for path statistics such as maximum drawdown (only an own AR(1) check so far).
- ev:signal-decay-crowding: a study that measures crowding by the decay of a delayed signal, as Narang suggests without evidence. The two crowding studies read at abstract level (`w3-kyle-crowded-markets`, `w4-chincarini-crowded-anomalies`) measure crowding from holdings or fire-sale dislocations instead.
- data:historical-borrow-availability: a point-in-time source of borrow fees and hard-to-borrow status for short-side backtests. Nasdaq's daily Regulation SHO threshold lists (public from January 2005) cover only fails-to-deliver thresholds and are in `data:derived-market-statistics`; belongs to `point-in-time-data`.

## What changed in my view or practice

## Questions carried forward

- Which edition of `s7-narang` do the research-chapter entries follow? They match the 2024 third edition in wording and order, but the catalogue does not establish its edition.
- Narang's information ratio uses a zero benchmark and his Sterling ratio a downside deviation; check standard definitions before any formula entry uses these names.
