---
key: wide-webster-price-impact
pathways: [price-impact-execution]
version: Kevin T. Webster, Handbook of Price Impact Modeling, Chapman and Hall/CRC, first edition, 2023 (DOI 10.1201/9781003316923; ISBN 978-1-032-32822-5), matching the catalogue record; local PDF with a text layer, outside the repository (printed page = PDF page - 17)
sections: chap. 1, secs. 1.1.1-1.1.5 (pp. 3-15); chap. 2, Definition 2.2.6 (pp. 53-54), sec. 2.7 (pp. 93-96), Definition 2.8.1 (p. 97); page image of p. 94 (checked for liquidity and impact review)
read:
status: draft
---

Prepared on 2026-10-15 by liquidity and impact review from source checks, not from study: the headings that need your own reading are left empty. `notes/log.md` records chapter 1 as in progress before the study method.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Price impact: trading causes price moves that would otherwise not have happened (p. 5). The causality challenge: one cannot observe both outcomes of a trade (pp. 6–7). Four core modelling principles: intuitive, actionable (rules out price manipulation paradoxes), testable, robust (p. 8). Four communities in the history of impact models (pp. 9–15).
- Unperturbed price $S$, perturbed price $P=S+I$, trade price $\widetilde P=S+I+s$; Almgren–Chriss's "temporary market impact" is the instantaneous transaction cost (Definition 2.2.6 and n. 3, pp. 53–54).
- Gatheral's definition of price manipulation, quoted: a round trip with negative expected cost (n. 3, p. 7).
- Generalized OW model, $dI=-\beta I\,dt+\lambda\,dQ$, $\lambda=e^\gamma$; no-manipulation condition $2\beta+\gamma'>0$; Example 2.7.1, a two-trade round trip that profits when it fails (p. 94, page image; rederived); transaction-triggered manipulation not excluded (pp. 94–95); volume-growth bound $v'/v<4\beta$ under square-root impact (p. 96); summary Definition 2.8.1 (p. 97).

## Limits

## Implementation

## Notation map

- Webster's $P$ (perturbed price) and $S$ (unperturbed price) are local to `def:price-impact` and `res:no-price-manipulation`.

## Connections

- `catalogue-0528` gives the empirical side (response functions, propagators) and the reaction/prediction split that Webster's causality challenge refers to (pp. 6–7 quote its pp. 210–211).
- Gatheral (`catalogue-0501`) and Fruth, Schöneborn and Urusov (2013) are the sources of the no-manipulation results; not consulted.

## Entries

`def:price-impact`, `mod:propagator`, `res:no-price-manipulation`.

## Open questions

- Exercise 4 and Figure 2.5 (p. 95) illustrate the manipulation example; not inspected.

## Retrieval cards
