---
key: catalogue-0496
pathways: [market-making-lob]
version: Maureen O'Hara, Market Microstructure Theory; local scan of the 1998 Wiley printing (catalogue record 1995)
sections: chapter "Inventory Models", sec. 2.3, pp. 29-36 (checked for migration slice 3); chapter "Strategic Trader Models I: Informed Traders", pp. 89-98 (checked for the migration pilot)
read:
status: draft
---

Prepared on 2026-10-14 by the compendium migration pilot from source checks, not from study: the headings that need your own reading are left empty. No route lists the book as a required reading; it is used here for supplemental material of `market-making-lob`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Kyle (1985) single auction: $X(v)=\beta(v-p_0)$, $P(x+\mu)=p_0+\lambda(x+\mu)$, $\beta=(\sigma_\mu^2/\Sigma_0)^{1/2}$, $\lambda=\tfrac12(\sigma_\mu^2/\Sigma_0)^{-1/2}$ (p. 93, eqs. (4.3)–(4.5)).
- Ex ante insider profit $\pi=\tfrac12(\Sigma_0\sigma_\mu^2)^{1/2}$; doubling $\sigma_\mu$ doubles order and profit and leaves the ex ante price unchanged (p. 97, eqs. (4.16)–(4.17)).
- Posterior variance $\Sigma_1=\Sigma_0/2$ whatever the order flow: half the information is revealed (p. 98, eq. (4.20)).
- Ho and Stoll (1981), as reported here: multiperiod, Poisson arrivals with rates linear in the quote adjustments, fixed true price, approximated by a first-order expansion with quadratic utility (pp. 29–35); spread = risk-neutral monopoly spread + risk adjustment rising with the horizon; transaction uncertainty does not enter; spread independent of inventory, both quotes shifted (pp. 35–36). Printed page = PDF page − 9 in this scan.
- No other linear equilibrium; nonlinear ones not excluded (p. 97). A linear price can turn negative for a large sell imbalance (p. 96).

## Limits

## Implementation

## Notation map

- $p_0\to\mu$; $\Sigma_0\to\sigma_v^2$; $\sigma_\mu\to\sigma_u$ (the book writes the noise order as $\mu$); $P\to S$.

## Connections

- `ho-stoll-1981` is the original of sec. 2.3's model (not consulted: no accessible copy).
- `s6-kyle` is the original; `crypto-cartea` pp. 31–33 gives a shorter account with a misprinted $\lambda$.

## Entries

`mod:kyle-single-auction`; `mod:inventory-based-quotes` (the Ho–Stoll account).

## Open questions

- Do page numbers in the 1995 printing named by the catalogue match this 1998 printing?

## Retrieval cards
