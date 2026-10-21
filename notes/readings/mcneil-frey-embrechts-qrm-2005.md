---
key: mcneil-frey-embrechts-qrm-2005
pathways: [risk-tail-systemic]
version: Alexander J. McNeil, Rüdiger Frey and Paul Embrechts, Quantitative Risk Management: Concepts, Techniques and Tools, Princeton University Press, 2005 (first edition; copyright page, PDF p. 4). The catalogue key s7-qrm is the 2015 revised edition, which is not held; the catalogue records the 2005 edition as a distinct version. Copy used: the owner's library, `Non-Exam/Quant Trading/Quant Stackexchange Books/Quantitative Risk Management/...(2005, Princeton University Press)....pdf` (read-only; SHA-256 a27c34f432fb3f5fb2463124bc063469b45bc45625e56745eadb5e4a28586c7d), 554 PDF pages with a text layer; printed page = PDF page - 16 in chapter 7.
sections: library gap-filling Batch L2 (2026-10-21): contents; chap. 7, secs. 7.1-7.1.2, pp. 264-268 (GEV, Fisher-Tippett-Gnedenko, exponential and Pareto examples, regularly varying tails and the Frechet domain, Theorem 7.8); secs. 7.2.1-7.2.6 and Notes, pp. 275-293 (GPD, excess distribution and mean excess function, Pickands-Balkema-de Haan, ML eq. (7.14), quasi-likelihood for dependent data, mean excess plots, Danish and AT&T examples, tail probabilities and VaR and ES eqs. (7.17)-(7.21), threshold sensitivity, the Hill estimator eq. (7.23) and tail estimator (7.24), the t4 simulation study, conditional EVT); Example 7.29, p. 293 (t tail index)
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L2 from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:extreme-value-tail-estimation` (`risk-tail-systemic`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- VaR_a = u + (beta/xi)[((1 - a)/Fbar(u))^(-xi) - 1]; ES_a = VaR_a/(1 - xi) + (beta - xi u)/(1 - xi) (eqs. (7.18)-(7.19), p. 283); ES/VaR tends to 1/(1 - xi) (7.20).
- Hill: alpha_hat = (k^-1 sum_{j<=k} ln X_{j,n} - ln X_{k,n})^-1 (7.23), p. 287; some versions use X_{(k+1),n}. For t4 with n = 1,000, Hill is best for xi at k about 20-30; the GPD VaR estimator is robust to k (pp. 290-291).
- Conditional EVT: GARCH by QML, GPD on residuals, scale by sigma_{t+1} (pp. 291-292).

## Limits

- 2005 edition; the 2015 revision was not read. Regulatory chapters (Basel II, Solvency 2) are dated and not used.

## Implementation

## Notation map

QRM writes the tail index alpha = 1/xi and order statistics X_{1,n} >= ... >= X_{n,n}; the compendium's H_k uses X_(n-i+1) for the i-th largest.

## Connections

## Entries

`meth:extreme-value-tail-estimation` (`risk-tail-systemic`).

## Open questions
