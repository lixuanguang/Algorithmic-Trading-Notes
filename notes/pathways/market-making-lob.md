---
key: market-making-lob
section: execution-market-making
status: not started (format pilot entries only)
---

# Market making, queues and limit-order-book models

Pathway outcome, from the guide: derive inventory-aware quotes, model queue dynamics and fill probabilities, and evaluate learned order-book signals.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. On 14 October 2026 the compendium migration pilot (`notes/migration.md`) wrote the entries below from the legacy notes, as a test of the entry format. They are supplemental models; of the pathway's required readings they touch only `s6-stoikov`, and the checkpoint has not been attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

- `mod:grossman-miller`: Grossman–Miller immediacy model (supplemental; risk-based price concession).
- `res:grossman-miller-trading-fees`: fee incidence in Grossman–Miller (supplemental).
- `res:grossman-miller-liquidity-measures`: linear impact and negative autocovariance in Grossman–Miller (supplemental).
- `mod:static-limit-order-depth`: static depth choice with exponential fill probability; a stand-in for, not a statement of, Ho–Stoll.
- `mod:avellaneda-stoikov`: inventory-aware quotes (`s6-stoikov`, a required reading).
- `mod:kyle-single-auction`: Kyle single-auction model (supplemental; information-based impact).

All six: verification partly checked 2026-10-14, stability draft. Human review outstanding.

## Entry backlog

- res:avellaneda-stoikov-infinite-horizon: an infinite-horizon discounted objective gives stationary reservation prices, defined for $\omega>\tfrac12\gamma^2\sigma^2q^2$, so $\omega$ acts as a bound on the inventory allowed; $\omega=\tfrac12\gamma^2\sigma^2(q_{\max}+1)^2$ keeps the prices bounded \citep[sec.~2.3, p.~219]{s6-stoikov}
- res:avellaneda-stoikov-exact-quotes: the exact optimal distances solve implicit equations in the reservation prices and the intensity and its derivative \citep[sec.~3.1, eqs.~(18)--(19), p.~221]{s6-stoikov}
- res:glosten-milgrom-half-spreads: with a fraction $\alpha$ of informed traders and a two-point value, competitive half-spreads rise with the prevalence and magnitude of toxicity \citep[chap.~``A Primer on the Microstructure of Financial Markets'', pp.~34--36]{crypto-cartea}
- res:glosten-milgrom-market-collapse: with price-sensitive liquidity traders of low urgency, the only zero-profit spreads may be the extreme ones and the market collapses \citep[chap.~``A Primer on the Microstructure of Financial Markets'', p.~37]{crypto-cartea}
- Needs a source before it can be stubbed: Grossman–Miller free entry, with the number of market makers set so that spread capture covers the participation cost, and the migration of large orders to search, block crossing or delayed execution when market-making capacity is scarce (legacy implications; passage needed in `grossman-miller-1988`).
- Needs a source before it can be stubbed: Ho–Stoll dealer quotes as functions of inventory (legacy *Inventory-Skew Quoting*; passage needed in `ho-stoll-1981`, which `catalogue-0527` points to without naming).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. Assigned to this pathway: *Quote-Control Segmentation* and *Inventory-Skew Quoting*. The rest of `legacy/execution-market-making/05_market_making_and_liquidity_provision/` is candidate material for this pathway, partly shared with `hft-market-design` and `execution-market-making`.

## What changed in my view or practice

## Questions carried forward

- `crypto-cartea` p. 33 prints Kyle's $\lambda$ as $2\sigma_u/\sigma$, the reciprocal of `catalogue-0496` eq. (4.5): confirm against Kyle (1985) and the book's errata.
- Which Ho–Stoll paper does the route intend by `catalogue-0527`: Ho and Stoll (1981), or their 1980 paper on competing dealers that `s6-stoikov` also cites?
