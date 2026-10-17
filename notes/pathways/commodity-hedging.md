---
key: commodity-hedging
section: energy-commodities
status: not started (draft entries from the migration only)
---

# Commodity hedging with futures

Pathway outcome, from the guide: size and roll a futures hedge for a physical exposure with minimum-variance, cross-hedge and time-varying hedge ratios; judge the funding and basis risk of stack-and-roll hedges; and weigh the evidence on why producers and consumers hedge and whether it adds value. Its checkpoint estimates static, rolling-window and bivariate-GARCH hedge ratios for an exposure without an exact futures contract and reports out-of-sample variance reduction. Its readings run from Working, Johnson and Ederington on hedging theory, through Anderson-Danthine, Baillie-Myers and Lien-Tse on hedge ratios, to Froot-Scharfstein-Stein, Culp-Miller, Mello-Parsons, Neuberger, Tufano, Haushalter and Jin-Jorion on why firms hedge and Metallgesellschaft.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration derivatives and hedging review (`notes/source-review-records.md`), which routed the hedging blocks of the legacy Hull notes (`volatility-options/fwdfut.tex`, a map candidate of this pathway) here. The entries come from source checking against Hull's 11th Global edition, chap. 3, which is not a reading of this pathway; none of the readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration derivatives and hedging / source review / optimal execution / high-frequency strategies reviews:

- `def:futures-hedge-basis`: short and long hedges, the basis and its sign convention, basis risk and the effective price $F_1+b_2$, cross-hedge basis components, contract choice and stack and roll (Metallgesellschaft's funding mismatch); the legacy long-hedge column noted as not Hull's.
- `mod:minimum-variance-hedge-ratio`: the variance objective and its derivation, $h^*=\rho\sigma_S/\sigma_F$, hedge effectiveness as in-sample $R^2$, number of contracts, price-change against return regressions under daily settlement, tailing (the legacy one-year rule generalised), beta hedges with index futures; Hull's Table 3.2 recomputed and plotted.

Both partly checked 2026-10-15, draft; human review outstanding. Artefact: `notes/artefacts/volatility-options/hull-forwards-futures.tex`, with the original figure.

derivatives and hedging review follow-up, 2026-10-16: `def:futures-hedge-basis` now names the two cross-hedge basis components (the futures-underlying basis $S_2^*-F_2$ and the asset difference $S_2-S_2^*$, Hull p. 77), states that $F_1+b_2$ and the decomposition assume a hedge ratio of 1.0 (p. 79), and adds the derived general expression $S_2+h(F_1-F_2)$ with its units.

Changed in the financial data and labels review follow-up, 2026-10-16: `def:futures-hedge-basis` and `mod:minimum-variance-hedge-ratio` no longer say a negative $h$ adds exposure: with $\operatorname{Cov}(\Delta S,\Delta F)<0$ the minimum-variance $h^*$ is negative (a long futures position against a long exposure) and reduces variance; checked in `notes/artefacts/volatility-options/negative-hedge-ratio-check.py`.

## Source verification after macro markets and pricing review

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Queue: `ev:why-firms-hedge` narrowed (Froot, Scharfstein and Stein's NBER WP 4084 read by OCR, merged into `def:futures-hedge-basis`; Tufano and Jin and Jorion not obtained); `mod:theory-of-storage` and `meth:time-varying-hedge-ratio` blocked (Working, Brennan, Baillie and Myers, Lien and Tse paywalled; one search each found no open copy). The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:why-firms-hedge` narrowed (Tufano (1996) and Jin and Jorion (2006) read at abstract level and merged into the hedging entry: neither supports the value channel). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): the `meth:time-varying-hedge-ratio` question: static against rolling hedge ratios for a jet-fuel exposure, out of sample under a recorded protocol: rolling helps modestly (heating oil 53.8 against 49.3 percent variance reduction), merged into `mod:minimum-variance-hedge-ratio`; GARCH not run. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `mod:duration-convexity` (`rates-credit-mortgages`); `mod:factor-risk-model` (`portfolio-construction`); `def:arbitrage` (`execution-market-making`).

## Entry backlog

- meth:time-varying-hedge-ratio: bivariate-GARCH hedge ratios, the checkpoint's third method, and the readings `ec-baillie-myers-1991` and `ec-lien-tse-2002` (paywalled); static against rolling OLS ratios was tested out of sample for a jet-fuel exposure (rolling helps modestly; in `mod:minimum-variance-hedge-ratio`).
- ev:why-firms-hedge: the full texts of Tufano (1996) and Jin and Jorion (2006), for their samples and estimates; their abstracts were read and neither supports a firm-value channel. Froot, Scharfstein and Stein's theory is in the entry.
- mod:theory-of-storage: inventories, convenience yield and the basis as Working (1948) and Brennan (1958) set them out (home pathway `commodity-storage-curves`; `ec-working-1948`, `ec-brennan-1958`: no open copy found on 2026-10-17).

## Legacy candidate material

Run `python3 tools/check_compendium.py` for the current counts. No legacy file lists this pathway after derivatives and hedging review.

## What changed in my view or practice

## Questions carried forward
