---
key: basel-framework-cre-2026
pathways: [securitised-structured-credit]
version: Basel Committee on Banking Supervision, The Basel Framework, standard CRE, chapters CRE31 ("IRB approach: risk weight functions") and CRE99 ("Application guidance"), the versions effective 1 January 2023, last updated 27 March 2020, status "Current", next CRE version listed as effective 1 January 2028 for other chapters. Pages retrieved 2026-10-21 from https://www.bis.org/basel_framework/chapter/CRE/31.htm and /99.htm (inforce 2023-01-01, published 2020-03-27); HTML SHA-256 85e2c7dbc0779da331aec4b94aa70297ad3b8eb48e159ee3bbc398eee3bf4651 (CRE31) and ed44f0d11eceb50e28deb8811b3f483d476fa12e5b59e50bf51b03eecddfc6e8 (CRE99); the CRE31.5-31.6 formulas are images (CRE31_20220101_1-5.svg), rendered and read. Copies kept in the git-ignored reading_materials/library-gap-l2-20261021/.
sections: CRE31.1-31.16 (introduction; PD and LGD as decimals, N and G; defaulted exposures; the corporate, sovereign and bank risk-weight function with correlation, maturity adjustment, capital requirement and RWA; the 1.25 correlation multiplier for financial institutions; SME firm-size adjustment; specialised lending and HVCRE; retail functions in outline); CRE99.1-99.3 with Table 1 (illustrative IRB risk weights)
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L2 from source checks, not from study: the headings that need your own reading are left empty. Used for `mod:gaussian-copula-default-correlation` (`securitised-structured-credit`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Corporate, sovereign and bank exposures not in default: R = 0.12 w + 0.24 (1 - w), w = (1 - e^{-50 PD})/(1 - e^{-50}); b = (0.11852 - 0.05478 ln PD)^2; K = [LGD N(G(PD)/sqrt(1 - R) + sqrt(R/(1 - R)) G(0.999)) - PD LGD] (1 + (M - 2.5) b)/(1 - 1.5 b); RWA = 12.5 K EAD (CRE31.5).
- Table 1, corporate, LGD 40%, M 2.5, turnover 50: 17.47% at PD 0.05% to 102.09% at 2%; reproduced to 0.005 points.

## Limits

- Committee standards, not national law; implementation and dates differ by jurisdiction. Only CRE31 and CRE99 were read; PD floors and LGD parameters (CRE32) were not.

## Implementation

## Notation map

Basel's R is the copula correlation rho; G is the inverse standard normal.

## Connections

## Entries

`mod:gaussian-copula-default-correlation` (`securitised-structured-credit`).

## Open questions
