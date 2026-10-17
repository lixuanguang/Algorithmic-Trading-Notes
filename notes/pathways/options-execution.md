---
key: options-execution
section: execution-market-making
status: not started (draft entries from the migration only)
---

# Options market making and execution costs

Pathway outcome, from the guide: explain option spreads and execution costs through market-maker hedging, inventory and volatility risk, and measure how retail order flow is routed and what it pays. Its checkpoint measures quoted and effective spreads by moneyness and maturity for one liquid equity or index option series, estimates how much compensates hedging and volatility risk, and simulates executing a delta-hedged order at the quote, at mid and with timing based on the underlying's price, reporting cost net of hedge slippage. Its nine readings run from the multiply listed U.S. options market (`ex-battalio-hatch-jennings-2004`) through market-maker hedging, inventory and informed trading (`ex-jameson-wilhelm-1992`, `ex-huh-lin-mello-2015`, `wide-muravyev-order-flow`), execution costs and illiquidity premia (`wide-muravyev-pearson`, `wide-christoffersen-option-illiquidity`), inventory-aware quoting (`ex-eraker-osterrieder-2023`, `exp-baldacci-options-market-making`) to retail routing (`ex-bryzgalova-pavlova-sikorskaya-2023`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 21 (`notes/migration.md`), which migrated the legacy options-market-microstructure file mapped to this pathway alone. The entries come from migration and source checking: `ex-bryzgalova-pavlova-sikorskaya-2023` in its published open-access version, read in part; the other five readings drawn on through their publishers' abstracts only. That is not study of the readings, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 21, 2026-10-15:

- `res:option-market-maker-spreads`: discrete-hedging and volatility-uncertainty components of quoted spreads (Jameson–Wilhelm), inventory against information components of option price impact (Muravyev), hedging against informed trading and the choice of hedge instrument (Huh–Lin–Mello model), with hedging, volatility, inventory and information risk kept apart and the implied volatility surface distinguished from uniform liquidity.
- `meth:option-spread-measurement`: quoted against effective spreads in percent of premium, timing-adjusted spreads against a fair-value benchmark (Muravyev–Pearson), premium against volatility units, and the U.S. listed-options 2019–2021 split by moneyness (moneyness on the underlying's midpoint, read as interpretation; ATM spreads far below slightly OTM but not the lowest bin), expiry and trade size (Bryzgalova–Pavlova–Sikorskaya Table I, SLIM single-leg auction proxy against the remaining pool); outright against multi-leg (multi-leg strategy costs not isolated), option against hedge liquidity. Corrected in the slice-21 follow-up.
- `mech:options-retail-wholesaler-routing`: PFOF, wholesalers' affiliated market makers and paired orders in exchange price-improvement auctions, the responder-fee asymmetry (the $0.30 net rebate in the responder-execution case), concentration in three wholesalers, and what SLIM trades paid (2019–2021); exchange-only execution bounded to listed options, with OTC options per FINRA Regulatory Notice 22-14's background.

All three: verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/options-execution/derivations.tex`.

## Source verification after slice 37

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Queue: `mech:options-clearing-exercise-assignment` narrowed (OCC rulebook HTTP 403; SEC Release 34-56845 of 2007 describes random and pro rata assignment, merged into `res:option-market-maker-spreads`; no source links clearing to fragmentation); `def:option-complex-orders` narrowed (Cboe rulebook 403; Rule 5.33's COB, COA, SBBO and legging from SEC Release 34-92729, merged into `meth:option-spread-measurement`; no evidence on multi-leg costs). The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `mech:options-clearing-exercise-assignment` narrowed (current OCC Rules 803-805 and 1803 (last modified 19 August 2025, archived copy) read and merged into the options-dealing entry: the rule text names neither random nor pro rata assignment); `def:option-complex-orders` narrowed (Cboe filing SR-CBOE-2026-081, Exhibit 5 (current Rule 5.33(g) legging text) merged). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment`, `mod:inventory-based-quotes`, `def:spread-measures`, `res:spread-determinants`, `res:adverse-selection-spread-component` (`market-making-lob` and `execution-market-making`); `def:best-execution`, `def:broker-agency-conflicts` (`market-structure-execution-quality`); `conv:futures-block-efrp` (`futures-execution`), `def:portfolio-trading` (`execution-trading-costs`) and `mech:etf-creation-redemption` (`etf-index-closing-execution`). None of them is option evidence.

## Entry backlog

- mech:options-clearing-exercise-assignment: (narrowed in the third batch of 2026-10-17) (narrowed 2026-10-17: OCC assignment procedures as of 2007 from an SEC release) current OCC rules (theocc.com HTTP 403) and any source linking common clearing, exercise, assignment and margin to multiple listing and fragmentation.
- def:option-complex-orders: (narrowed in the third batch of 2026-10-17) (narrowed 2026-10-17: Cboe Rule 5.33 mechanisms from an SEC notice of 2021) the current rule text (Cboe HTTP 403) and evidence on multi-leg spreads against outrights.

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 21 no legacy file lists this pathway.

## What changed in my view or practice

## Questions carried forward

- Read Jameson and Wilhelm, Huh, Lin and Mello, Muravyev, Muravyev and Pearson, and Battalio, Hatch and Jennings in full: only abstracts were read on 2026-10-15; no open full text was found except a working-paper copy of Huh, Lin and Mello on the EFMA site, which returned an error.
- Does "uncertainty reduces quoted size" hold in any sample? Not checked.
- Read Christoffersen et al., Eraker–Osterrieder and Baldacci–Bergault–Guéant, not drawn on in slice 21.
