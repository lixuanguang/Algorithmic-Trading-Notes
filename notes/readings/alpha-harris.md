---
key: alpha-harris
pathways: [execution-market-making, market-making-lob]
version: Larry Harris, Trading and Exchanges, Oxford University Press, 2002 printing; local PDF with a text layer, outside the repository (printed page = PDF page - 13)
sections: chapter "Dealers", pp. 280, 283-295; chapter "Bid/Ask Spreads", pp. 297-321; chapter "Value Traders", pp. 340-346; chapter "Volatility", pp. 410-417; chapter "Liquidity and Transaction Cost Measurement", pp. 423-427, 434; chapter "Bubbles, Crashes, and Circuit Breakers", pp. 555-563, 570-578 (checked for migration slices 2 to 4)
read:
status: draft
---

Prepared on 2026-10-15 by migration slices 2 to 4 from source checks, not from study: the headings that need your own reading are left empty. Reading progress before the study method is in `notes/log.md` (completed).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Inventory imbalance, and the two inventory risks: diversifiable (independent of the imbalance) and adverse selection (inversely correlated with it) (pp. 283–286).
- Dealers seek market values that produce two-sided flow, and discover fundamental values as a by-product (pp. 284, 286–287).
- Tactics: Table 13-2 for inventory (p. 285), Table 13-3 after a suspected informed trade (p. 288), Table 13-4 for consequences when trading with informed and uninformed buyers (p. 292).
- Adverse-selection spread component: quotes conditional on the side of the next trade (pp. 289–290); the information and accounting views agree, shown in a simple example based on Glosten–Milgrom, $a-b=2PE$ (pp. 300–302, 320–321). P. 321 misprints the informed-buyer profit as $A-(V-E)$.
- Spread determinants: asymmetric information, volatility, utilitarian trading interest (pp. 311–313); secondary proxies (pp. 314–317); market failure and private financing (p. 317).
- Total spread: ask $=V^B+C/2$, bid $=V^S-C/2$ (Figure 14-1, p. 301); both quotes rise by half the adverse-selection component after a buy (Figure 14-2, pp. 301–302). Two components only; the inventory premium sits in the transaction-cost component (pp. 298–299).
- Uninformed traders lose whichever order type they use (sec. 14.3, pp. 303–304, Table 14-1).
- Order-driven equilibrium spread: indifference between limit and market orders; Table 14-2 (p. 311); management cost plus twice the timing option (p. 307).
- Outside spread of value traders and why it exceeds dealer spreads (chap. 16, pp. 340–345).
- Roll's estimator, $S=2\sqrt{-\mathrm{SCov}}$ (box, p. 415, page image); typically biased down by violations, use only without quotes (p. 434).
- Fundamental volatility from unexpected value changes, transitory volatility from impatient uninformed trading, which reverts; total = sum; negative serial correlation a strong indicator; perishable spot prices an exception; regulators can affect only the transitory part (chap. 20, pp. 410–416).
- Bubbles and crashes: five-phase dynamics, price accelerator (box after Treynor, p. 556), most crashes correct earlier mispricing (box p. 559); the 1987 crash (pp. 559–563); circuit breakers' net effect on transitory volatility indeterminate (secs. 28.3.1–28.3.4, pp. 572–577).
- Effective spread = twice the signed difference from the time-of-trade midpoint; realised spread from a later midpoint (pp. 424–425); quoted − effective = price improvement, effective − realised = losses to informed traders (pp. 425–426). "Realised spread" also means a dealer's round-trip outcome (p. 280).

## Limits

## Implementation

## Notation map

- $P\to\alpha$ (probability the next trader is informed); $E\to e$ (pricing error); $A,B\to a,b$.

## Connections

- `s6-hasbrouck` gives the econometric side of chaps. 14, 20 and 21 (Roll model, generalized Roll model, effective and realised costs).
- `glosten-milgrom-1983` is the model behind the chap. 14 appendix; `crypto-cartea` pp. 34–37 parametrises it by the value distribution instead.

## Entries

`res:adverse-selection-spread-component`, `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment`, `def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `res:spread-determinants`, `def:outside-spread`, `def:volatility-components`, `mech:bubble-crash-dynamics`; also cited in `mod:glosten-milgrom` and `meth:spread-volatility-regression`.

## Open questions

## Retrieval cards
