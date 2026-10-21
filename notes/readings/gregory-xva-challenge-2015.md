---
key: gregory-xva-challenge-2015
pathways: [corporate-credit-cds]
version: Jon Gregory, The xVA Challenge: Counterparty Credit Risk, Funding, Collateral and Capital, 3rd ed., John Wiley & Sons, Chichester, 2015 (ISBN 978-1-119-10941-9; title page PDF p. 4 and copyright page PDF p. 5, "This edition first published 2015"). Copy used: the owner's library, `CQF-1-master/Textbooks/The xVA Challenge Counterparty Credit Risk, Funding, Collateral, and Capital.pdf` (read-only; SHA-256 b2b005d1f7f25c71cc7fbe6cf6d98e8f1664ae212c849fbb7962553721af394f), 497 PDF pages with a text layer; printed page = PDF page - 27 (checked at pp. 205, 247 and 311). The catalogue's `gap-gregory5` is a later edition that is not held.
sections: library gap-filling Batch L2 (2026-10-21): contents (PDF pp. 8-18); chap. 7, secs. 7.1.6-7.3.3 and 7.4.4, pp. 113-122 and 133-135 (exposure metrics EFV, PFE, EE, maximum PFE, EPE, NEE and ENE, EEPE; normal-distribution example; square-root and swap profiles; collateral that increases exposure, Table 7.3); chap. 11, secs. 11.2-11.3.7, pp. 247-260 (MPR setup, amortisation, conditionality, disputes, lookback and continuous discretisation and cash flows during the MPR, numerical examples, 0.4 sigma sqrt(MPR), thresholds, two-way CSAs that raise EE for short CDS protection, haircuts); chap. 14, secs. 14.2.3-14.3.1 and 14.6.3-14.6.5, pp. 311-315 and 327-328 (CVA formula, example, CVA as a spread, exposure and discounting with the T-forward measure, risk-neutrality, semi-analytical forms, BCVA); chap. 15, secs. 15.1.4-15.2.1, pp. 341-342 (FVA intuitive definition, eq. (15.2)); chap. 17, secs. 17.1-17.4.2, pp. 377-385 (wrong-way risk, examples and evidence, general and specific, conditional EE eq. (17.1), the simple model, wrong-way collateral, hazard-rate and structural approaches)
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L2 from source checks, not from study: the headings that need your own reading are left empty. Used for `def:counterparty-exposure-measures`, `meth:credit-valuation-adjustment` and `def:wrong-way-risk` (`corporate-credit-cds`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Metrics follow BCBS (2005): EE is the mean of the positive part and is "sometimes called EPE"; EPE is the time-weighted average of EE (pp. 116-118). Normal future value with mean 2: EE 2.17 and 99% PFE 6.65 at s.d. 2, 2.79 and 11.31 at s.d. 4 (pp. 116-117), reproduced.
- Swap EE approximately proportional to (T - t) sqrt(t), maximum at T/3 (p. 121).
- Collateral can increase exposure (Table 7.3, p. 133); a two-way CSA raises EE for short CDS protection (pp. 258-259); payment spikes inside the MPR (pp. 250-254).
- CVA = -LGD sum EE(t_i) PD(t_{i-1}, t_i), eq. (14.2), p. 311, where EE "is the discounted expected exposure"; the 300 bp square-root example gives -0.200%, exact -0.193%, averaged -0.192% (p. 312), reproduced. Taking discount factors outside needs the T-forward measure (p. 313).
- CVA as a spread (sec. 14.2.5, p. 313): -0.200% / risky annuity 4.42 = -4.52 bp per annum (zero rates, n. 4; the annuity formula is in the online Appendix 14B, not read; (1 - e^{-hT})/h with h = 5% reproduces 4.42). Eq. (14.4), CVA ~ -EPE x spread, is "in the same units as the credit spread", with EPE undiscounted and constant (nn. 5-7): -1.54% x 300 = -4.62 bp per annum, not an upfront value. Reread 2026-10-21 in the L2 correction pass.
- Conditional EE replaces EE under wrong-way risk, eq. (17.1), p. 380: EE(t_i | t_i = tau_C), conditional on t_i being the default time and, like eq. (14.2), discounted (reread in the L2 correction pass); wrong-way risk increases as credit quality improves (pp. 381-382); hazard-rate approaches give weak dependence (p. 384).

## Limits

- 2015 text: the capital chapter (8) and regulatory statements predate the post-2017 Basel reforms and are not used. Chap. 16 (MVA, KVA) was not read. LIBOR-era examples are dated.
- Gregory signs CVA negative (a loss); the compendium reports CVA as a positive charge.

## Implementation

## Notation map

Gregory's MPR is RMFI's and Hull's cure period; his EE is discounted inside the simulation unless stated (pp. 311 and 313), whereas the compendium's E(t) and EE are undiscounted and EE* = E[D(0,t) E(t)] is the discounted form. His EPE in eq. (14.4) is undiscounted.

## Connections

## Entries

`def:counterparty-exposure-measures`, `meth:credit-valuation-adjustment`, `def:wrong-way-risk` (`corporate-credit-cds`).

## Open questions
