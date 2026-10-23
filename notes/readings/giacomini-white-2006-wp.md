---
key: giacomini-white-2006-wp
pathways: [return-predictability]
version: Raffaella Giacomini and Halbert White, "Tests of conditional predictive ability", authors' version "This version: April 2006" (post-referee; published in Econometrica 74(6), 2006, 1545-1578, catalogue wide-giacomini-white, not obtained). Copy used: GiacominiWhite04.pdf from Giacomini's former UCLA page, Wayback Machine capture of 2006-09-20 (31 pages, SHA-256 2d937c5c...f15a7), retrieved 2026-10-22; printed page = PDF page
sections: sec. 1 (pp. 2-5); sec. 2.1 (pp. 5-7); sec. 3.1-3.4 (pp. 7-13); sec. 4 (p. 13); sec. 5 (pp. 14-17); sec. 6.2-6.4 (pp. 18-21)
read:
status: draft
---

Prepared on 2026-10-22 for the conditional predictive ability entry from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:conditional-predictive-ability`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Object of evaluation: the forecasting method (model, estimation procedure, estimation window), not the model (pp. 2-3). Null (2)/(3) on losses at the estimates, conditional on G_t; DMW null (1) at probability limits (pp. 5, 8).
- G_t trivial gives equal unconditional predictive ability; G_t = F_t asks whether information at t predicts which method will be more accurate at t + tau (pp. 3, 6). Analogy: unconditional is a test of the intercept, conditional a test for serial correlation of the loss-difference regression (p. 3).
- Estimation window bounded, m <= m-bar < infinity; "rules out an expanding window forecasting scheme"; a fixed estimation sample is allowed; any loss including predictive log likelihood (p. 8).
- One-step test: under the null {dL, F_t} is an mds; test function h_t (q x 1); T = n Zbar' Omega^-1 Zbar with Omega = n^-1 sum Z Z' (uncentred); reject above chi2_q (eq. (4), Theorem 1, p. 9).
- Comments (p. 10): 3, expanding windows ruled out; 4, non-vanishing estimation noise avoids the DMW singularity for nested models; 5, HAC allowed but may lower power; 7, T = n R^2 of ones on Z' (and n R^2 of dL on h under conditional homoskedasticity).
- Power and instruments (p. 11): with heterogeneity the test can have no power against alternatives correlated with omitted parts of F_t; too few instruments may "accept" a false null, too many dilute power.
- Multi-step (eq. (6), Theorem 3, pp. 11-12): Omega-tilde with lags 1..tau-1, weights tending to one. Unconditional (eq. (8), Theorem 4, p. 12): DM t with HAC, truncation lag growing (p. 13).
- Decision rule (sec. 4, p. 13): regress dL on h_t, choose by the sign of the fitted value at T.
- Monte Carlo (sec. 5): Table 1 sizes of the unconditional test with equal expected method MSE by construction (Proposition 5); power against AR(1) and state-dependent loss differences simulated directly as loss differences (eq. (13) and sec. 5.2.2, pp. 16-17).

## Limits

The copy is the authors' version, not the journal's; its text calls the tests of Theorems 1-4 "Theorems 5 and 6" in places (pp. 15-17, 19), so the published numbering may differ. The empirical application (sec. 6) and the appendix of additional results (CPAappendix.pdf, also archived) were not used. GW's own power simulations generate loss differences directly; they do not derive the null from a DGP and forecasting methods.
