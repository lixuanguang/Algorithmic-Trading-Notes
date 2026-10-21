---
key: ding-liu-rutkowski-ccbs-2025
pathways: [volatility-options, fx-cip-dollar-funding]
version: Yining Ding, Ruyi Liu and Marek Rutkowski, "Multi-Curve Approach to Cross-Currency Basis Swaps Referencing Backward-Looking Term Rates", arXiv:2410.08477v3 (revision of 30 October 2025), 50 pages; SHA-256 3f4eed4243abb8daf907505da90568d29279b1e81f20b9616c8ed398aca049f2; git-ignored copy in reading_materials/library-gap-l4-20261021/; retrieved 2026-10-21; locators are arXiv pages. The catalogue key w4-ding-rutkowski-ccbs is the SIAM Journal on Financial Mathematics 17(2) 2026 version, titled "Cross-Currency Basis Swaps Referencing Backward-Looking Rates"; not read
sections: pp. 1 and 4 (abstract and introduction: the LIBOR-to-RFR transition; constant-notional and mark-to-market swaps as market variants); pp. 6-7 (sec. 2.2: Definition 2.4, constant-notional cash flows for the long party with principals P^d = Q_{T0} P^f exchanged at T0 and back at Tn, spread kappa on the domestic (AUD) leg; the spread agreed at inception and constant; Definition 2.5 in AUD; FX swap against CCBS); p. 38 (sec. 7: three-year non-MTM AUD/USD swap, receive six-month compounded SOFR, pay six-month AONIA plus a spread, semi-annual)
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L4 from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Constant-notional CCBS: CF_T0 = [P^d, -P^f]; CF_Tj = [-(R^d + kappa) delta_j P^d, R^f delta_j P^f]; CF_Tn adds the principals back (Definition 2.4, p. 6).
- Q is AUD per USD; the domestic (valuation) currency is AUD, the dollar foreign (pp. 6-7).
- The spread is set at inception and stays constant during the life (p. 7).

## Limits

Model sections (3-6) not read and not used. One currency pair's convention; it does not establish which leg carries the spread market-wide. Mark-to-market resets named only.

## Implementation

## Notation map

## Connections

## Entries

`meth:cross-currency-basis-swaps`

## Open questions
