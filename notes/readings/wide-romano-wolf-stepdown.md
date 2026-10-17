---
key: wide-romano-wolf-stepdown
pathways: [backtest-inference]
version: Joseph P. Romano and Michael Wolf, "Stepwise Multiple Testing as Formalized Data Snooping", Econometrica 73(4), 2005, as catalogued. Copy used: Universitat Pompeu Fabra working paper 712, October 2003 (econ-papers.upf.edu), text layer; page numbers are the working paper's
sections: secs. 1-3 (pp. 1-11), Algorithms 3.1-3.2, Assumption 3.1, Theorem 3.1, Scenarios 3.1-3.2
read:
status: draft
---

Prepared on 2026-10-17 by method validation (2026-10-17) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:multiple-testing-control`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- FWE and strong control defined (sec. 2.2, pp. 6-7); Bonferroni and Holm conservative because they ignore dependence (sec. 2.3, pp. 7-8).
- Reality Check as the first step of StepM; StepM rejects stepwise with max-quantiles over the remaining strategies (Algorithm 3.1, pp. 9-10); bootstrap estimate (Algorithm 3.2); block or stationary bootstrap for time series (Scenario 3.2, p. 11).
- Theorem 3.1: asymptotic FWE control and consistency under Assumption 3.1 (pp. 10-11). Own Monte Carlo: FWE 0.014-0.046 at alpha 5%; power ordering as stated.

## Limits

Working paper, not the 2005 Econometrica version; studentized version (sec. 4) and the empirical application not read.
