---
key: roadmap-perpetual-pricing
pathways: [crypto-perpetuals]
version: D. Ackerer, J. Hugonnier and U. Jermann, "Perpetual Futures Pricing", Mathematical Finance 36(3), 481-499, 2026 (DOI 10.1111/mafi.70018). Copy used: arXiv 2310.11771v2, dated 3 September 2024 (posted 4 September 2024), downloaded 2026-10-15; text layer, printed page = PDF page. The published version was not checked
sections: abstract; pp. 2-4, 7-8 (sec. 3, eqs. (3)-(7)), 12 (Corollary 1) (checked for migration slice 24)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 24 from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Funding computed periodically (e.g. every 8h on most platforms) as premium plus interest term; fixed-maturity convergence limits basis (p. 2).
- Linear: size in base units, margined and settled in quote currency; inverse: base asset is margin and settlement asset, size in quote currency; quanto: third currency (pp. 2-3); reference currency in practice often a crypto or stablecoin such as USDT (p. 7).
- Long's one-period cash flow (f_{t+1}-f_t) - kappa_t (f_t - x_t) - iota_t x_t (eqs. (4)-(6), pp. 7-8).
- Funding specifications exist under which the perpetual price equals spot (p. 4; Corollary 1, p. 12) - a frictionless no-arbitrage result.

## Limits

## Implementation

## Notation map

## Connections

## Entries

`mech:perpetual-funding`; also cited in `def:crypto-venue-instrument-structure`.
