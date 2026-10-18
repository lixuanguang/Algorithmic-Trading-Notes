---
key: performance-manager-evaluation
section: portfolio-construction-risk
status: not started (draft entries only, not from study)
---

# Performance attribution and manager evaluation

Pathway outcome, from the guide: attribute returns, adjust for factor exposure, smoothing and survivorship, and estimate how much apparent skill is luck. Its readings include `wide-sharpe-1994`, `wide-brinson-attribution`, `wide-carhart`, `wide-fama-french-luck` and `wide-getmansky-lo-makarov`.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by transaction-cost analysis review (`notes/source-review-index.md`). Its topics (performance measurement, risk-adjusted excess return, selection and timing, smoothed returns) evaluate managers, not executions, and this pathway's outcome names factor adjustment and smoothing. The entry comes from source checking against Harris (`alpha-harris`, chap. 22), not from this pathway's readings. That is not study.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in transaction-cost analysis / source review / optimal execution / high-frequency strategies reviews:

- `meth:relative-performance-evaluation`: total, holding-period and internal rates of return; market-adjusted and risk-adjusted returns; Harris's decomposition into excess return, market timing and market; return smoothing.

Verification partly checked 2026-10-15, stability draft; human review outstanding.

Written in derivatives and hedging / source review / optimal execution / high-frequency strategies reviews:

- `def:return-measures`: GIPS 2020 definitions of time- and money-weighted returns, external cash flows, gross and net of fees; cumulative, geometric-mean and annualised returns; IRR existence and multiple roots; real and leveraged returns; a malformed TWR root and an unexplained "risk" factor in the real return corrected; formulas derived and checked numerically.

Partly checked 2026-10-15, draft; human review outstanding.

derivatives and hedging review follow-up, 2026-10-16: the TWR/MWR example now compares matching horizons (MWR $-3.71$ percent per sub-period, $-7.29$ percent over two; TWR $-1.0$ percent over two, $-0.50$ percent per sub-period), and the entry separates the annualisation formula from GIPS presentation: 2.A.12 (p. 9) forbids annualising periods under a year, 2.A.29 (p. 12) requires annualised since-inception MWRs, and 5.A.1.a--b (p. 33) presents a non-annualised since-inception MWR for a track record under a full year.

Written in dealer models and information / source review / optimal execution / execution control reviews:

- `meth:skill-luck-significance-tests`: the $t$-test of mean excess return, power and the years of data needed (Tables 22-2 and 22-3 recomputed), sample length against frequency, distributional shape, smoothing and fraud, selection, survivorship and regression to the mean (Harris chap. 22, secs. 22.4--22.6).

Partly checked 2026-10-16, draft; human review outstanding.

method validation (2026-10-17):

- `meth:gips-composite-presentation`: composite construction, required statistics and first disclosures of a GIPS composite report. Partly checked 2026-10-17, draft.


Written in the performance and planning batch (2026-10-18):

In `performance-attribution-appraisal.tex` (topic `performance-evaluation`):

- `def:performance-evaluation-components`: measurement, attribution and appraisal and the sponsor's and manager's purposes (Bailey, Richards and Tierney, MIP chap. 12, pp. 718-720); Bacon's attribution definition and Lord's characteristics (pp. 239-241).
- `meth:risk-adjusted-performance-measures`: Sharpe, Treynor, Jensen and M-squared with their benchmarks and criticisms (chap. 12, pp. 767-771); the appraisal ratio and M-squared form (Bacon pp. 190 and 226-227); a two-fund example where rankings split; alpha and Treynor agree only for positive beta.
- `meth:return-attribution`: returns-, holdings- and transactions-based attribution; BHB and Brinson-Fachler; macro and micro levels; Carino linking; fixed-income effects (Bacon chap. 6, pp. 239-258, 331-338 and 361-363; Fong, Pearson and Vasicek in chap. 12, pp. 764-765); risk attribution; accounting against causal claims.
- `meth:macro-attribution-owner-manager`: the six decision levels (chap. 12, pp. 746-753) and an original fund example.
- `meth:benchmark-selection-quality`: liability- and asset-based benchmarks, validity, seven types, universes, Bailey's quality tests, misspecification and alternative-investment benchmarks (chap. 12, pp. 731-744; Bacon p. 125).
- `meth:downside-appraisal-measures`: downside deviation, Sortino, appraisal ratio, capture, drawdown, recovery and Calmar with their denominators and edge cases (Bacon pp. 126, 190, 194-197, 203-208 and 234-236); the normal benchmark of downside deviation depends on the target (sigma/sqrt 2 at the mean).
- `meth:manager-skill-evaluation`: skill as consistent value added, Exhibits 12-19 and 12-20 reproduced (three cells of 12-19 differ from the normal model), power and a decision procedure.

In `manager-selection.tex` (topic `manager-selection`):

- `meth:manager-due-diligence`: search, questionnaire and the Four Ps (MIP chap. 7, pp. 466-470; Bacon pp. 489-491); Type I and II errors (chap. 12, pp. 778-781); returns- and holdings-based style analysis, minimising the variance of the tracking difference (Sharpe 1992; chap. 7, pp. 436 and 442-444).
- `meth:manager-philosophy-process-behaviour`: philosophy and process questions (chap. 7, pp. 466 and 468); team behaviour and mitigations (Kahneman chaps. 7 and 24; Statman p. 6; Ang p. 503).
- `meth:vehicle-contract-fee-analysis`: fee forms and agreement terms (chap. 7, p. 467; Bacon pp. 59-64); US law: Advisers Act sec. 205, Rule 205-3, the 2026 threshold order and the October 2026 proposal; a three-year fee comparison.
- `ex:manager-selection-case`: a fictional foundation's choice between two managers with IR shrinkage and its sensitivity to the prior, process checks, vehicle and contract.

In `performance-standards.tex` (topic `performance-presentation-standards`), extending `meth:gips-composite-presentation` (now with presentation duties and portability, 1.A.32-1.A.34 and the Handbook, pp. 50-52):

- `def:gips-scope-verification`: objectives, scope, fundamentals, firm definition, discretion, verification and performance examination (GIPS 2020, Introduction and sec. 1; Handbook p. 147).
- `meth:gips-return-calculations`: sec. 2 requirements, composite weighting, dispersion and the 36-month standard deviation (Handbook pp. 196-200).
- `meth:gips-composite-membership`: provisions 3.A.1-3.A.13 with the Handbook's discussion of timing and significant cash flows (pp. 166-167 and 173-174); an invented membership calendar.
- `ex:gips-composite-report`: an educational five-year report with no compliance claim.

All partly checked 2026-10-18, draft. Examples in `notes/artefacts/performance-evaluation/performance-evaluation-checks.py`, `notes/artefacts/manager-selection/manager-selection-checks.py` and `notes/artefacts/performance-presentation-standards/gips-checks.py`; human review is outstanding. Coverage records are editorial, not study.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:gips-composite-presentation` resolved as a new entry in `portfolio-construction-risk/performance-evaluation.tex` (GIPS for Firms 2020, provisions 3.A.1-3.A.11, 4.A.1-4.A.3, 4.C.1-4.C.5, 5.A.1). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

Coverage pilot (2026-10-18) (source checks, not study): `def:return-measures` reviewed against `objective:compare-time-and-money-weighted-returns` in `notes/coverage/objectives.json`; GIPS glossary and provisions reread at their cited pages, Harris chap. 22, pp. 446-447, read as an independent source, and every worked figure recomputed. No text change was needed. The record is in `notes/source-review-records.md`, *Coverage inventory and pilot integrations*.

First foundation slice (2026-10-18) (source checks, not study): `def:return-measures` extended with holding-period, price and total returns (OpenStax *Principles of Finance 2e*, sec. 15.1; FT Wilshire methodology, sec. 1.1, p. 3) and the arithmetic against geometric mean; the TWR and MWR text is unchanged. Examples in `notes/artefacts/time-value-returns/time-value-return-checks.py`.

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- Harris's realised alpha omits the risk-free rate and uses concurrent betas; the regression form is Jensen's alpha. Which does the pathway's checkpoint (Carhart alphas) need, and how should smoothing be corrected (`wide-getmansky-lo-makarov`, unread)?
