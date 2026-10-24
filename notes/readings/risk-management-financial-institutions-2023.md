---
key: risk-management-financial-institutions-2023
pathways: [portfolio-construction-risk, portfolio-risk-financing, corporate-credit-cds, securitised-structured-credit, risk-tail-systemic]
version: John C. Hull, Risk Management and Financial Institutions, 6th ed., John Wiley & Sons, 2023 (ISBN 978-1-119-93248-2). Copy used: local PDF supplied by the owner in `reading materials/` on 2026-10-19 (SHA-256 18d308d777cc9f4fc8d7f53a8ca519716a304a148509e996445ef2b397109a45), text layer; printed page = PDF page - 28. An earlier 4th ed. (2015) copy was consulted first and set aside for this edition
sections: chap. 11, pp. 233-249 (VaR and ES, confidence-level changes, marginal, incremental and component measures, Euler allocation, aggregation, the VaR-limit gaming example on p. 237); chap. 13, sec. 13.1, pp. 279-281 (model-building VaR for Microsoft and AT&T); chap. 15, p. 319 (Greeks and limits); chap. 16, pp. 347-352 (stress testing, stressing individual variables, management scenarios, reverse stress testing); chap. 21, sec. 21.2, pp. 458-460 (liquidity funding risk and its sources); chap. 25, sec. 25.12, pp. 557-558 (Solvency II); chap. 27, p. 586 (FRTB 97.5% ES); chap. 28, pp. 609-613 (economic capital allocation, RAROC); credit, time-series and valuation batch (2026-10-20): chap. 2 pp. 28-34 (DLC bank, capital, deposit insurance), chap. 3 pp. 57-66 (insurers, ratios, regulation), chap. 17 pp. 367-391 (default probabilities, recovery, CDS, spreads, Merton), chap. 18 pp. 393-401 (CVA), chap. 19 pp. 413-415 (transition matrices), App. K pp. 689-691 (CDS valuation); PR #32 audit (2026-10-20): chap. 3 pp. 52, 56-57, 62-63 (guaranteed annuity options, longevity and mortality risk, adverse selection, life insurer balance sheet); alternatives batch (2026-10-20): chap. 19 pp. 413, 416-417 (credit VaR definition, Vasicek WCDR eq. 19.1, Gordy extension eq. 19.2); library gap-filling Batch L2 (2026-10-21), same copy: P7, chap. 18, pp. 393-411 (credit exposure, CVA eqs. (18.1)-(18.3), collateral and cure periods eq. (18.4) and Example 18.1, peak exposure, downgrade triggers, incremental CVA, CVA risk eq. (18.5), wrong-way risk and the alpha multiplier, DVA, simple examples eqs. (18.6)-(18.11) and Example 18.3, MVA, FVA and KVA); pp. 395-396 reread for the rate-tree extension of meth:risky-bond-cva; P8, chap. 9, secs. 9.5-9.6.3, pp. 202-213 (copulas, Tables 9.3-9.5, the algebraic form, Student t copula, tail dependence, multivariate and factor copulas, Vasicek's model eqs. (9.9)-(9.15), Example 9.2, estimating PD and rho, alternatives); P9, chap. 8, sec. 8.4, pp. 170-172 (the power law, Example 8.4, Table 8.2) and chap. 12, secs. 12.3-12.6.1, pp. 266-276 (volatility scaling, bootstrap, EVT key result eq. (12.5), ML eqs. (12.6)-(12.7), tail eq. (12.8), power-law equivalence, left tail, VaR and ES eqs. (12.9)-(12.10), the worked application, Table 12.10, choice of u)
read:
status: draft
---

Prepared on 2026-10-19 by the derivatives, portfolio and execution batch (2026-10-19) from source checks, not from study: the headings that need your own reading are left empty. Used for `def:short-term-funding-repo`, `meth:portfolio-var-methods-decomposition`, `meth:sensitivity-scenario-risk-measures` and `meth:market-risk-limits-capital`. Search: none; the owner supplied the 6th edition during the batch.

Also used by the credit, time-series and valuation batch (2026-10-20) for `def:financial-institution-features`, `meth:bank-camels-analysis`, `meth:insurer-analysis`, `def:credit-risk-components`, `meth:corporate-credit-analysis`, `meth:risky-bond-cva`, `meth:rating-migration-returns`, `mod:structural-reduced-form-credit`, `meth:credit-spread-term-structure`, `def:cds-contract-features`, `meth:cds-pricing`, `meth:cds-strategies`.

Also used by the PR #32 audit correction pass (2026-10-20) for `meth:life-insurer-analysis`.

Also used by the alternatives batch (2026-10-20) for `meth:credit-liquidity-tail-risk`.


Also used by library gap-filling Batch L2 (2026-10-21) for `def:counterparty-exposure-measures`, `meth:credit-valuation-adjustment`, `def:wrong-way-risk` and the rate-tree extension of `meth:risky-bond-cva`.


Also used for `mod:gaussian-copula-default-correlation` (`securitised-structured-credit`).


Also used for `meth:extreme-value-tail-estimation` (`risk-tail-systemic`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Model-building VaR: one-day 99% VaR 512,300 and ten-day 1,620,100 for 10m Microsoft and 5m AT&T (rho 0.3); ten-day ES 1,856,100; diversification benefit 219,000 (pp. 279-281).
- Component VaRs sum to total VaR by Euler's theorem; component approximates incremental VaR for small subportfolios (pp. 246-248).
- RAROC = (revenues - costs - expected losses)/economic capital; 0.80/4 = 20%, 22% with interest on capital (pp. 612-613).
- Six sources of funding liquidity; wholesale deposits ``can disappear quickly'' (pp. 459-460).

- Reproduced by trading_notes.numerical.credit_risk_analysis.credit_cds_securitisation_checks: Examples 17.1-17.4, Tables 17.1-17.5 (Q = 3.03%), 19.1-19.2, Appendix K (123 bp, MTM 0.0111); Table K.1 misprints year-4 survival 0.9321 (Table K.2: 0.9231).
- DLC: 12% pre-tax ROE on 5% equity; a 3.2% rise in loan losses makes a 1%-equity bank insolvent (pp. 28-30); combined and operating ratios, Table 3.2 (pp. 59-60).
- Longevity hurts annuities and helps life cover; mortality risk the reverse; the two partly offset, net exposure assessed by actuaries (pp. 56-57). Life insurers invest mostly in corporate bonds matched to liability maturity; reserves are conservative estimates (p. 63). Guaranteed annuity rates as unpriced options (p. 52); adverse selection in life and annuity books (p. 62).
- Credit VaR: the credit loss not exceeded with a given confidence; default-only or including migration and spreads (p. 413); WCDR(T, X) = N((N^-1(PD) + sqrt(rho) N^-1(X)) / sqrt(1 - rho)) (p. 416).

## Limits

Regulatory descriptions are Hull's as of 2023; national implementation of FRTB and Solvency II changes and must be checked. Errata not checked.
