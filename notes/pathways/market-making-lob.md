---
key: market-making-lob
section: execution-market-making
status: not started (draft entries from the migration only)
---

# Market making, queues and limit-order-book models

Pathway outcome, from the guide: derive inventory-aware quotes, model queue dynamics and fill probabilities, and evaluate learned order-book signals.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. On 14 October 2026 the compendium migration pilot (`notes/migration.md`) wrote the entries below from the legacy notes, as a test of the entry format. They are supplemental models; of the pathway's required readings they touch only `s6-stoikov`, and the checkpoint has not been attempted. On 15 October 2026 a second migration slice added Glosten–Milgrom, from its 1983 working paper (`glosten-milgrom-1983`) rather than the journal version `s6-glosten`, and Harris's account of dealer inventory and quoting. A third slice, the same day, migrated the spread-decomposition and inventory-model files, checked against Harris and Hasbrouck (`s6-hasbrouck`, a required reading of the section overview route, not of this pathway) and O'Hara's account of Ho–Stoll. A fourth slice, also on 15 October 2026, migrated the volatility, bubble-and-crash and spread–volatility blocks of the volatility-and-liquidity file, checked against Harris, Hasbrouck and Lehalle and Laruelle (`alpha-laruelle`), and assigned that file's flash-crash and systemic blocks to `hft-market-design`. That is migration and source checking, not study of the readings.

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

- `mod:glosten-milgrom`: Glosten–Milgrom sequential-trade model (the route's first reading, checked in its 1983 working paper).
- `res:glosten-milgrom-half-spreads`: two-value half-spreads (`crypto-cartea` simplification).
- `res:glosten-milgrom-market-collapse`: collapse with price-sensitive liquidity traders (`crypto-cartea`, corrected by its errata).
- `res:adverse-selection-spread-component`: Harris's $2\alpha e$ example (supplemental; formerly attributed to Glosten–Milgrom).
- `def:dealer-inventory-risk`: inventory imbalance; diversifiable and adverse-selection risk (Harris; supplemental).
- `meth:dealer-quote-adjustment`: dealer quote and size tactics for inventory and suspected informed trading (Harris; supplemental).

- `mod:inventory-based-quotes`: Stoll's CARA reservation quotes (Hasbrouck's version) and the Ho–Stoll properties as O'Hara reports them; the original papers not consulted.
- `def:spread-measures`: quoted, inside, relative, effective and realised spreads (Harris, Hasbrouck).
- `res:roll-spread-estimator`: Roll's serial-covariance estimator and its biases (Harris, Hasbrouck).
- `res:spread-component-identification`: transitory and permanent components; the generalized Roll model; inventory versus information (Harris, Hasbrouck).
- `res:spread-determinants`: Harris's primary and secondary spread determinants and the order-driven equilibrium spread.
- `def:outside-spread`: value traders' outside spread (Harris).

- `def:volatility-components`: fundamental and transitory volatility; the random-walk decomposition (Harris, Hasbrouck).
- `meth:garman-klass-volatility`: range-based intraday volatility as Lehalle and Laruelle use it (the 1980 paper not consulted).
- `meth:spread-volatility-regression`: spread on volatility in levels and logs, with the retransformation correction (Lehalle and Laruelle).
- `mech:bubble-crash-dynamics`: how bubbles build and crashes unwind; the price accelerator; crash attribution (Harris).

Changed in slice 3: `res:adverse-selection-spread-component` (now also the total spread, Figure 14-1, the uninformed-traders lesson, and a correction of the legacy "twice the loss" claim; title changed, label kept), `def:dealer-inventory-risk` (inventory costs and the inventory premium) and `meth:dealer-quote-adjustment` (cross-references only).

The first six: verification partly checked 2026-10-14, stability draft. The next six: partly checked 2026-10-15, draft. The next six: partly checked 2026-10-15 (slice 3), draft. The last four: partly checked 2026-10-15 (slice 4), draft; slice 4 also changed `res:spread-determinants` (volatility and liquidity supply, Lehalle and Laruelle's empirical relation) and `res:roll-spread-estimator` (a cross-reference). `mod:kyle-single-auction` was changed on 2026-10-15: the `crypto-cartea` errata confirm its p. 33 misprint. Human review outstanding for all twenty-two. The five measurement entries (`def:spread-measures` to `def:outside-spread`) and the four slice 4 entries serve the section overview route `execution-market-making` more than this pathway; they are listed here only because no pathway note exists for that route yet.

## Entry backlog

- res:avellaneda-stoikov-infinite-horizon: an infinite-horizon discounted objective gives stationary reservation prices, defined for $\omega>\tfrac12\gamma^2\sigma^2q^2$, so $\omega$ acts as a bound on the inventory allowed; $\omega=\tfrac12\gamma^2\sigma^2(q_{\max}+1)^2$ keeps the prices bounded \citep[sec.~2.3, p.~219]{s6-stoikov}
- res:avellaneda-stoikov-exact-quotes: the exact optimal distances solve implicit equations in the reservation prices and the intensity and its derivative \citep[sec.~3.1, eqs.~(18)--(19), p.~221]{s6-stoikov}
- res:grossman-miller-free-entry: market makers enter until the expected utility of trading at the date-1 price, net of the participation cost $c$, equals that of staying out; with a zero mean imbalance their number is set by $ac$, falling as $c$ or risk aversion $a$ rises and rising with the variances of the price change and of the imbalance \citep[eqs.~(16)--(19), pp.~18--19]{grossman-miller-1988-nber} (the legacy wording "until spread capture covers $c$" was loose)
- res:grossman-miller-market-structure: an order larger than the specialist and the limit-order book can absorb switches the market to search, as in upstairs block trading, which served mainly as a search market \citep[p.~9]{grossman-miller-1988-nber}
- res:ho-stoll-dealer-pricing: check against the paper the three properties O'Hara reports for the multiperiod model (spread = risk-neutral monopoly spread plus a risk adjustment rising with the horizon; transaction uncertainty does not enter; spread independent of inventory, quotes shifted instead) \citep[sec.~2.3, pp.~35--36]{catalogue-0496}; blocked: `ho-stoll-1981` has no accessible copy, and `catalogue-0527` names no paper

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No block is now assigned to this pathway: *Inventory-Skew Quoting* was migrated in slice 3 to `mod:inventory-based-quotes` from textbook sources, with the Ho–Stoll paper still unread (backlog stub above). The market-making section of the legacy notes has been worked through (`notes/migration.md`, slice 2). Its remaining blocks are assigned to `execution-market-making` or `hft-market-design`, except the cross-asset arbitrage file, which is shared and flagged. The spread-decomposition and inventory files of `03_information_price_formation_and_spreads/` were migrated and deleted in slice 3. In slice 4, 14 of the 22 blocks of its volatility-and-liquidity file were migrated; the other 8 (liquidity spiral, Flash Crash, systemic risk, trade count) are assigned to `hft-market-design`, whose readings include the Flash Crash papers. Shared candidate material remains in `02_orders_matching_and_limit_order_books/`, the other `03_...` files and `04_order_flow_and_empirical_microstructure/`.

## What changed in my view or practice

## Questions carried forward

- `crypto-cartea` p. 33 prints Kyle's $\lambda$ as $2\sigma_u/\sigma$: the authors' errata correct it to $\sigma/(2\sigma_u)$, as in `catalogue-0496` eq. (4.5) (checked 2026-10-15). Still to confirm against Kyle (1985), which has no open copy.
- Do the propositions and pages of the 1985 journal version of Glosten–Milgrom (`s6-glosten`) match the 1983 working paper the entries cite?
- Which Ho–Stoll paper does the route intend by `catalogue-0527`: Ho and Stoll (1981), or their 1980 paper on competing dealers that `s6-stoikov` also cites?
- Do O'Hara's three Ho–Stoll properties (pp. 35–36 of the 1998 printing) hold as stated in the paper, and under which approximation (first-order expansion, quadratic utility)?
- Roll's estimator: Harris (p. 434) says violations typically bias it down; Hasbrouck's Exercise 4.3 (pp. 38–39) shows signs correlated with information bias it up. Which dominates in practice is not settled by these passages.
