---
key: broadie-glasserman-1996
pathways: [volatility-options]
version: Mark Broadie and Paul Glasserman, "Estimating Security Price Derivatives Using Simulation", Management Science 42(2), February 1996, 269-285, DOI 10.1287/mnsc.42.2.269. Copy: Columbia Business School PDF (business.columbia.edu/sites/default/files-efs/pubfiles/1848/estimating.pdf), a 17-page scan of the published article without a text layer, read as page images; SHA-256 247d7319c1034d5872df47b5ce895d6bb5870da5082987438814c8a1d70e1304; git-ignored copy in reading_materials/library-gap-l4-20261021/; retrieved 2026-10-21. Not in the catalogue; registered in sources.tex. Locators are journal pages (PDF page = journal page - 268)
sections: pp. 269-275 (sec. 1; sec. 2.1 pathwise eqs. (4)-(9) with n. 1; sec. 2.2 likelihood ratio eqs. (10)-(16); sec. 2.3 discussion of scope; sec. 3 second derivatives, eq. (18) and nn. 2-3, likelihood-ratio gamma; sec. 4 resimulation and the Example 1 discussion, p. 275); pp. 280-281 (control variate eq. (23); sec. 5 conclusions; App. A conditions (A1)-(A4), Proposition 1 and the remark on second derivatives; App. B optimal increment, eqs. (25)-(26)). Not read: pp. 276-279 (Tables 1-3; Asian and stochastic-volatility examples) and Apps. C-D
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L4 from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Pathwise: dS_T/dsigma = S_T(-sigma T + sqrt(T) Z), dS_T/dS0 = S_T/S0; call estimators e^{-rT} 1{S_T >= K} dS_T/dtheta, unbiased (eqs. (5)-(9), pp. 270-271). Unbiased under (A1)-(A4): a.s. differentiable path, payoff differentiable a.s., payoff Lipschitz, path a.s. Lipschitz with integrable modulus (Proposition 1, pp. 280-281). Rule of thumb: continuous payoff, method usually applicable (p. 272).
- Likelihood ratio: weight the discounted payoff by d ln g(S_T)/dtheta (eqs. (14)-(16), p. 272); the same estimator for any payoff with that density (pp. 272-273). Does not apply to the strike, "except possibly through a change of variables"; "The pathwise method, however, easily covers this case" (p. 272), said of the call.
- Gamma: the pathwise delta (17) differentiated inside the expectation concentrates at S_T = K and gives eq. (18), e^{-rT}(K/S0)^2 g(K), the closed-form gamma (p. 273; n. 2 gives the Dirac-delta form). Pathwise second derivatives need problem-dependent smoothing (p. 281).
- Resimulation: forward difference (P(theta_1) - P(theta_0))/h, biased; n + 1 simulations for n derivatives (p. 274); optimal h* = (2 nu^2 (1 - rho)/b^2)^{1/4} (eq. (26), p. 281).
- European example: likelihood-ratio standard errors "typically 1.5 to 4 times greater" than pathwise and resimulation (p. 275); conclusions say "significantly larger" in their examples (p. 280).

## Limits

Scanned copy, read as images; tables not read. The paper's delta symbol is the dividend yield (q in the compendium). The Z-form scores are rewritten from eqs. (15)-(16) in the compendium and checked numerically, not printed.

## Implementation

## Notation map

## Connections

## Entries

`meth:monte-carlo-greeks`

## Open questions
