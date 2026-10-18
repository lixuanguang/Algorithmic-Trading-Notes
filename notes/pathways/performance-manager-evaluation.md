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

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `meth:gips-composite-presentation` resolved as a new entry in `portfolio-construction-risk/performance-evaluation.tex` (GIPS for Firms 2020, provisions 3.A.1-3.A.11, 4.A.1-4.A.3, 4.C.1-4.C.5, 5.A.1). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

Coverage pilot (2026-10-18) (source checks, not study): `def:return-measures` reviewed against `objective:compare-time-and-money-weighted-returns` in `notes/coverage/objectives.json`; GIPS glossary and provisions reread at their cited pages, Harris chap. 22, pp. 446-447, read as an independent source, and every worked figure recomputed. No text change was needed. The record is in `notes/source-review-records.md`, *Coverage inventory and pilot integrations*.

First foundation slice (2026-10-18) (source checks, not study): `def:return-measures` extended with holding-period, price and total returns (OpenStax *Principles of Finance 2e*, sec. 15.1; FT Wilshire methodology, sec. 1.1, p. 3) and the arithmetic against geometric mean; the TWR and MWR text is unchanged. Examples in `notes/artefacts/time-value-returns/time-value-return-checks.py`.

## Entry backlog

## What changed in my view or practice

## Questions carried forward

- Harris's realised alpha omits the risk-free rate and uses concurrent betas; the regression form is Jensen's alpha. Which does the pathway's checkpoint (Carhart alphas) need, and how should smoothing be corrected (`wide-getmansky-lo-makarov`, unread)?
