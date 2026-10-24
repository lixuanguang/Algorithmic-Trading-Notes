---
key: international-equity-markets
section: international-equity-markets
status: not started (draft entries only, not from study)
---

# International and emerging equity markets

Pathway outcome, from the guide: measure equity-market integration and diversification gains across developed, emerging and frontier markets without relying on raw correlations, in local currency and in dollars, hedged and unhedged, after survivorship, reclassification and stale-price corrections. Its 5 required readings: `gr-karolyi-stulz-2003`, `gr-jorion-goetzmann-1999`, `gr-coeurdacier-rey-2013`, `gr-bekaert-harvey-2003`, `gr-carpenter-whitelaw-2017`. This note is for the section overview.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by macro markets and pricing review (`notes/source-review-index.md`). The entries come from source checking against Gliner (`s7-gliner`, *Global Macro Trading*, Wiley 2014, read from a local PDF and cited by chapter, section and PDF page). That is not study of the readings: none of them has been read for this pathway, and no checkpoint was attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in macro markets and pricing / source review / optimal execution / execution control reviews:

- `def:equity-indices-derivatives`: Gliner's indices by region, weighting methods, ETFs and ADRs, as of 2013.

All: verification partly checked 2026-10-16, stability draft; human review outstanding.


Written in the performance and planning batch (2026-10-18), in `index-construction.tex`, owned by `topic:market-index-construction`:

- `meth:index-value-return-calculation`: capitalisation, price and equal weighting with the divisor and its adjustments (S&P DJI *Index Mathematics Methodology*, September 2026, pp. 4-16; *Equity Indices Policies & Practices*, August 2026, pp. 8, 19 and 24); price, total and net total return (pp. 21-22); one-way turnover (p. 70); a three-stock example with a split, a share issue, a dividend and equal-weight rebalancing.
- `def:equity-fixed-income-index-types`: Bacon's calculation families (3rd ed., chap. 4, pp. 105-113) and S&P DJI's categories (p. 4); Bloomberg's fixed-income design principles, returns and projected universes, return components and market-value weights (January 2026, pp. 9, 42-43, 47 and 57-61); uses as targets, asset-class proxies and product references; a two-bond month.

Both partly checked 2026-10-18, draft; examples in `trading_notes.numerical.index_construction.index_construction_checks`. Coverage records are editorial, not study.

## Source verification after macro markets and pricing review

macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:equity-index-lists-current` narrowed. Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review follow-up*.

Second macro markets and pricing review follow-up, 2026-10-16 (source verification, not study): `data:equity-index-lists-current` narrowed (JPX market-structure page; Moscow Exchange index page). Entries corrected in the same follow-up are listed in `notes/source-review-records.md`, *macro markets and pricing review second follow-up*.

Source follow-up of order books and order flow / dealer models and information reviews and the macro markets and pricing review audit, 2026-10-16 (source verification, not study): `data:equity-index-lists-current` narrowed (Nikkei's Nikkei 225 profile and JPX's TOPIX page). The record is in `notes/source-review-records.md`, *Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*.

Second source follow-up, 2026-10-16 (source verification, not study or human review): `data:equity-index-lists-current` narrowed further (FTSE/JSE ground rules v9.3: Top 40 the 40 most investable All Share companies, headline indices on the SWIX free float from 18 March 2024; FT Wilshire 5000: comprehensive, float-adjusted U.S. market index). The record is in `notes/source-review-records.md`, *Second source follow-up of the order books and order flow / macro markets and pricing reviews queue*.

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `data:equity-index-lists-current` narrowed: NSE's methodology of September 2026 (Nifty 50, float-adjusted capitalisation-weighted) and Borsa Istanbul's ground rules of April 2020 (free-float weighting, capped variants) were read into `def:equity-indices-derivatives`. Failed routes, not repeated blindly: IDX (HTTP 403 again), S&P DJI methodologies (403, also through the fetching tool), stoxx.com (TLS certificate not verifiable; not forced), Euronext (403), and the Hang Seng address tried (404). The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `data:equity-index-lists-current` narrowed further (Hang Seng Index methodology v2.3, July 2023). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `data:equity-index-lists-current` narrowed (DJIA, Russell 2000, FTSE 100, EURO STOXX 50 and DAX rules read and merged into `def:equity-indices-derivatives`). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `data:equity-index-lists-current` question: BME's IBEX committee notice of December 2024 (free-float bands, 20 percent cap) merged into `def:equity-indices-derivatives`. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `meth:equity-index-valuation` (`cross-asset-style-premia`); `def:vix-variance-dividend-swaps` (`vix-correlation-dividends`); `mech:etf-creation-redemption` (`etf-index-closing-execution`).

## Specialist pathways

The guide's pathways for this section, in its order, with the existing material, partial treatment or content gap as recorded by the content migration of 22 October 2026 and its closeout review. A pathway with related material but no note has not been opened. A partial treatment names the existing entries that treat some of the pathway's subtopics, wherever they sit, and the subtopics with nothing written.

Printed as numbered sections of the chapter, under the guide pinned at `8302467` (`subsection_alignment_plan.md`): `intl-equity-integration`. A pathway without entries of its own is not printed; the related material and partial treatments named below are printed under the pathway or section that owns them.

- `intl-equity-integration` (Equity index construction, international integration, diversification and home bias): no pathway note; related existing material in `international-equity-markets/index-construction`, `international-equity-markets/equity-indices`, not reviewed as a complete treatment of the pathway.
- `global-equity-factors` (Global equity factors, country selection and return predictability): no pathway note; partial treatment in existing entries, not reviewed as complete: country and sector selection by valuation (`meth:equity-index-valuation` in `multi-asset-systematic-macro/equity-index-valuation`); integration-weighted equity premia (`meth:asset-class-return-forecasts` in `multi-asset-systematic-macro/capital-market-expectations`); value and momentum across countries and asset classes (`def:alpha-model-taxonomy` in `research-engineering-validation/quant-strategy-structure`). Not written: global factor models; country-level return predictability.
- `em-frontier-equities` (Emerging and frontier equity markets: liberalisation, foreign investors and liquidity): no pathway note; partial treatment in existing entries, not reviewed as complete: emerging-market equity premia under partial integration, and governance risks (`meth:asset-class-return-forecasts` in `multi-asset-systematic-macro/capital-market-expectations`). Not written: liberalisation effects; foreign investors and flows; frontier-market liquidity.
- `cross-listing-global-trading` (Cross-listings, ADRs and asynchronous global trading): no pathway note; partial treatment in existing entries, not reviewed as complete: ADR mechanics and currency exposure (`def:equity-indices-derivatives` in `international-equity-markets/equity-indices`). Not written: cross-listing motives and valuation effects; ADR parity and arbitrage; asynchronous trading across time zones.
- `china-em-equities` (China's stock market: factors, retail trading, intervention and access): content gap; no entry written.

## Entry backlog

- data:equity-index-lists-current: current methodologies for the Jakarta Composite, the S&P 500 and the other S&P DJI indices apart from the DJIA, CAC 40 and AEX, KOSPI, ASX 200, NZX 50, Shanghai Composite, Bovespa, Mexico IPC, Nasdaq Composite and FTSE MIB, and BME's IBEX Technical Regulations themselves; fourteen indices' rules and an IBEX committee notice are in `def:equity-indices-derivatives`.

## What changed in my view or practice

## Questions carried forward
