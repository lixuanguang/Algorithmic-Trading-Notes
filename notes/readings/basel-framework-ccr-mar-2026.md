---
key: basel-framework-ccr-mar-2026
pathways: [corporate-credit-cds, portfolio-construction-risk, financial-statement-analysis]
version: Basel Committee on Banking Supervision, The Basel Framework, chapter pages on bis.org (new URL scheme /committees/bcbs/basel-framework/standard/<std>/<ch>/inforce/<date>/published/<date>), retrieved 2026-10-21. bis-cre-51-2023-01-01.html eaa87364...185b08dd; bis-cre-51-2028-11-01.html 09cd5791...96a13443; bis-cre-52-2023-01-01.html fcbd1dd8...07429fe4; bis-mar-33-2023-01-01.html 180ea833...6b9b371d; bis-mar-50-2023-01-01.html 1986a8ea...821385c1; bis-mar-90-2023-01-01.html b49cbc4e...bfa5e7c2; bis-lcr-90-2019-12-15.html e65e948a...5a8cf9bc
sections: CRE51.1-51.15 (2023 version; 2028 version compared), CRE52.1-52.57 and 52.72 (formula images CRE52_20190101_1-8, 21, 23-25 rendered and read), MAR10, MAR11, MAR33.1-33.5 and 33.12 (Table 2), MAR50.1-50.20 (formula images MAR50_20220101_1-3 rendered and read), MAR90.1, LCR20.4-20.5, LCR90.1-90.2, NSF10, NSF20.2-20.3; MAR timeline page
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L3 (P10, regulatory and disclosure currency) from source checks, not from study: the headings that need your own reading are left empty. Copies are in the git-ignored `reading_materials/library-gap-l3-20261021/`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- SA-CCR: EAD = alpha (RC + PFE), alpha = 1.4 (CRE52.1); unmargined RC = max(V - C, 0) (52.10); PFE = multiplier x AddOn (52.20); multiplier floor 5% (52.23); SD = (exp(-0.05 S) - exp(-0.05 E))/0.05 (52.34); delta +1/-1 for linear trades (52.39); MF unmargined sqrt(min(M,1)/1), M floored at 10 business days (52.48-52.49); IR: hedging sets by currency, three maturity buckets, offset formula with 1.4 and 0.6 cross terms, SF 0.5% (52.57, Table 2 in 52.72).
- CRE51.7 and 51.13: CCR exposure feeds the standardised or IRB credit-risk approach; 51.14 IRB maturity adjustment capped at 1 where CVA capital is computed. The CRE51 version effective 1 November 2028 (published 28 October 2025) adds a treatment of guarantees and credit derivatives protecting CCR exposures (51.17-51.18); it does not change the EAD-then-risk-weight sequence.
- MAR50: RWA = 12.5 x requirement (50.1); CVA risk definition (50.4); regulatory CVA excludes own default (50.3); BA-CVA default, SA-CVA with approval (50.7); EUR 100bn materiality option (50.9); reduced BA-CVA with DS = 0.65, rho = 50% (50.14); SCVA, DF = (1 - exp(-0.05 M))/(0.05 M), alpha 1.4 and footnotes 3-4 (50.15); n. 3: DF is the supervisory discount factor averaged over time to the effective maturity, and EAD x M is a proxy for the area under the discounted expected exposure profile (currency x years, not a discounted EE at one date); n. 4: alpha converts EAD back to EEPE; risk weights 0.5%-12% (50.16).
- MAR33.3 (97.5%), 33.4 (10-day base, scaled), 33.5 (stress calibration), 33.12 Table 2 (horizons 10-120 days). MAR chapters effective 1 January 2023; MAR90.1 PLA test from 1 January 2023, Pillar 1 consequences from 1 January 2024. MAR21 was republished in place on 5 July 2024 and 23 March 2026 without a change of effective date.
- LCR90.1: 100% minimum effective 1 January 2019. NSF20.2: NSFR at least 100%.

## Limits

Basel dates are the dates by which members agreed to implement; for chapters already in force at launch the framework shows 15 December 2019, so the original SA-CCR date comes from BCBS 279. Committee standards are not national law.

Audit note (2026-10-21, Batch L3 post-implementation correction pass): the entry's first wording dropped the CRE52.48-52.49 ten-business-day floor from the printed maturity factor and called the BA-CVA product the same object as the discounted EE at a date; both corrected from the passages above.

## Implementation

## Notation map

## Connections

## Entries

`def:financial-institution-features`, `meth:market-risk-limits-capital`, `rule:counterparty-credit-cva-capital`

## Open questions
