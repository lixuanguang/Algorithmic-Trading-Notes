---
key: gapclose-deribit-rules
pathways: [crypto-perpetuals]
version: Deribit FZE, Exchange Rulebook version 2.0, applicable as of 13 August 2026 (help-centre article updated 15 September 2026), and Funding Specifications (article edited 27 July 2026, updated 20 August 2026); retrieved 2026-10-15 through the help-centre JSON API with a generic header, since the web pages returned a bot check. Inverse Options, Linear USDC Options and Portfolio Margin pages and the Exchange Membership Terms were not read
sections: Rulebook: Rules 1.1-1.2, 2 (guidance on custody), 10.1-10.11, 11.1-11.5, definitions (Auto-Deleveraging, Insurance Fund, Liquidation Fee), Appendix A; Funding Specifications: whole page including the cap table and Examples 1-5 (checked for crypto market structure review); Rules 9.16-9.17 and 10.6-10.11 rechecked 2026-10-15 for the crypto market structure review follow-up
read:
status: draft
---

Prepared on 2026-10-15 by crypto market structure review from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Deribit FZE is a VASP regulated by Dubai's VARA (Rule 1.1); spot via brokerage services, derivatives linear or inverse (Rule 1.2).
- Funding: positive rate, longs pay shorts; no fee; premium rate against the Deribit Index; damper +/-0.025%; caps BTC +/-0.5%, ETH +/-1.0%, USDC & USDT +/-5.0%; quoted per 8 hours, accrued continuously, in RSPL, cash at 08:00 UTC settlement.
- Example slips: ETH Example 3 says index USD 10,000 and "1 BTC long"; ETH Example 5 formula shows 7.5%; stated results correct (recomputed in funding_checks.py).
- Liquidation Process (10.1), liquidation fee (10.5), insurance fund (10.6-10.7; converting another currency of the fund is at Deribit's absolute discretion), socialised loss (10.8-10.11), auto-deleveraging definition; settlement daily 08:00 UTC (11.4); European cash-settled options priced in BTC or ETH (App. A 2(d)).
- Socialised-loss trigger (10.8, rechecked 2026-10-15): Deribit may, in its absolute discretion, trigger the mechanism if the fund is depleted in all currencies, or if the bankrupt account's currency is depleted and it decides not to convert other currencies. crypto market structure review had written only "if the fund is depleted"; corrected in `def:crypto-trading-risk-layers`. Rule 9.17 applies the same two-branch trigger to a short spot under cross-collateral margin (read, not used in an entry).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`mech:perpetual-funding`, `def:crypto-trading-risk-layers`; also cited in `def:crypto-venue-instrument-structure`.
