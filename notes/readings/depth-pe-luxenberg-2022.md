---
key: depth-pe-luxenberg-2022
pathways: [portfolio-construction-risk]
version: Eric Luxenberg, Stephen Boyd, Misha van Beek, Wen Cao and Mykel Kochenderfer, Strategic Asset Allocation with Illiquid Alternatives; read as arXiv 2207.07767 (27 pages), PDF retrieved 2026-10-20 (SHA-256 e8757cd44d11ba2159dfef16fb4e7440daee648d6948e0c434b136d2a0327dca); cited by PDF page. The catalogue's ICAIF 2022 version (8 pages) was not read; the Takahashi and Alexander (2002) paper was not read and is cited through this paper's description
sections: sec. 2 p. 3 (literature: Takahashi and Alexander's deterministic linear model; Giommetti and Sorensen); sec. 3 pp. 6-9 (stochastic linear model of commitments, calls, distributions and illiquid wealth; impulse and step responses; steady-state gains); sec. 7.1 p. 20 (steady-state commitment policy)
read:
status: draft
---

Prepared on 2026-10-20 by the alternatives batch (2026-10-20) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:alternatives-allocation-approaches`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Takahashi-Alexander: calls a time-varying fraction of uncalled commitments, distributions a fraction of NAV, constant returns (p. 3).
- K_(t+1) = K_t + n_t - C_t; I_(t+1) = I_t R_t + C_t - D_t; C_t = lambda0 n_t + lambda1 K_t; D_t = I_t R_t delta_t (p. 6).
- Steady-state gains alpha_K 2.491, alpha_C 1.000, alpha_I 3.685, alpha_D 1.804; alpha_C = 1 in general (pp. 8-9).
- Steady-state policy commits I_target / alpha_I each period (p. 20).

## Limits

Calibration from the authors' data is not reproduced; the model is time-invariant unlike Takahashi and Alexander's.
