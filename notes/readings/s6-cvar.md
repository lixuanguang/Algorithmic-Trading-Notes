---
key: s6-cvar
pathways: [portfolio-construction]
version: R. Tyrrell Rockafellar and Stanislav Uryasev, "Optimization of Conditional Value-at-Risk", author preprint dated 5 September 1999, 26 pages (https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf, the catalogue's link; SHA-256 34aff2161733085ca8e5a067053a8f144cba52f556e253d69c932f7d22d842f4; copy in the git-ignored reading_materials/library-gap-l2-20261021/), retrieved 2026-10-21. The catalogue records the 2000 Journal of Risk article; locators here are to the preprint.
sections: whole paper read: abstract, secs. 1-3 (definitions (1)-(3), F_beta (4), Theorems 1-2, sampling (9), portfolio application (11)-(17), the LP, problems P1-P3, the normal Proposition with (18)-(19)), the numerical example and Tables 1-6, the appendix proofs in outline
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L2 from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:mean-cvar-optimisation` (`portfolio-construction`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- CVaR = min over alpha of F_beta(x, alpha); VaR the left end of the argmin (Theorem 1, p. 5). Joint minimisation over (x, alpha) is convex for convex losses (Theorem 2, p. 6); scenarios give an LP (p. 8-9).
- Normal losses: VaR = mu + c1 sigma, CVaR = mu + c2 sigma; with an active return constraint the min-CVaR, min-VaR and min-variance portfolios coincide (p. 10). Tables 3-4 (p. 12) reproduced; Table 3's printed weights miss the return constraint by about 4e-9.

## Limits

- Assumes continuous loss distributions (p. 4); the 2002 generalisation was not read. Pseudo-random convergence was slow in their example (p. 11).

## Implementation

## Notation map

## Connections

## Entries

`meth:mean-cvar-optimisation` (`portfolio-construction`).

## Open questions
