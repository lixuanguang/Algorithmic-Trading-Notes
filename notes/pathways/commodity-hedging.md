---
key: commodity-hedging
section: energy-commodities
status: not started (draft entries from the migration only)
---

# Commodity hedging with futures

Pathway outcome, from the guide: size and roll a futures hedge for a physical exposure with minimum-variance, cross-hedge and time-varying hedge ratios; judge the funding and basis risk of stack-and-roll hedges; and weigh the evidence on why producers and consumers hedge and whether it adds value. Its checkpoint estimates static, rolling-window and bivariate-GARCH hedge ratios for an exposure without an exact futures contract and reports out-of-sample variance reduction. Its readings run from Working, Johnson and Ederington on hedging theory, through Anderson-Danthine, Baillie-Myers and Lien-Tse on hedge ratios, to Froot-Scharfstein-Stein, Culp-Miller, Mello-Parsons, Neuberger, Tufano, Haushalter and Jin-Jorion on why firms hedge and Metallgesellschaft.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 31 (`notes/migration-slices.md`), which routed the hedging blocks of the legacy Hull notes (`volatility-options/fwdfut.tex`, a map candidate of this pathway) here. The entries come from source checking against Hull's 11th Global edition, chap. 3, which is not a reading of this pathway; none of the readings has been read, and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 31, 2026-10-15:

- `def:futures-hedge-basis`: short and long hedges, the basis and its sign convention, basis risk and the effective price $F_1+b_2$, cross-hedge basis components, contract choice and stack and roll (Metallgesellschaft's funding mismatch); the legacy long-hedge column noted as not Hull's.
- `mod:minimum-variance-hedge-ratio`: the variance objective and its derivation, $h^*=\rho\sigma_S/\sigma_F$, hedge effectiveness as in-sample $R^2$, number of contracts, price-change against return regressions under daily settlement, tailing (the legacy one-year rule generalised), beta hedges with index futures; Hull's Table 3.2 recomputed and plotted.

Both partly checked 2026-10-15, draft; human review outstanding. Artefact: `notes/artefacts/volatility-options/hull-forwards-futures.tex`, with the original figure.

Slice-31 follow-up, 2026-10-16: `def:futures-hedge-basis` now names the two cross-hedge basis components (the futures-underlying basis $S_2^*-F_2$ and the asset difference $S_2-S_2^*$, Hull p. 77), states that $F_1+b_2$ and the decomposition assume a hedge ratio of 1.0 (p. 79), and adds the derived general expression $S_2+h(F_1-F_2)$ with its units.

Changed in the slice-32 follow-up, 2026-10-16: `def:futures-hedge-basis` and `mod:minimum-variance-hedge-ratio` no longer say a negative $h$ adds exposure: with $\operatorname{Cov}(\Delta S,\Delta F)<0$ the minimum-variance $h^*$ is negative (a long futures position against a long exposure) and reduces variance; checked in `notes/artefacts/volatility-options/negative-hedge-ratio-check.py`.

## Source verification after slice 37

Second batch of 2026-10-17 (audit repairs and a 50-item queue; source verification and bounded tests, not study or human review): Queue: `ev:why-firms-hedge` narrowed (Froot, Scharfstein and Stein's NBER WP 4084 read by OCR, merged into `def:futures-hedge-basis`; Tufano and Jin and Jorion not obtained); `mod:theory-of-storage` and `meth:time-varying-hedge-ratio` blocked (Working, Brennan, Baillie and Myers, Lien and Tse paywalled; one search each found no open copy). The record is in `notes/migration-slices.md`, *Second batch of 17 October 2026*.

Third batch of 2026-10-17 (six audit repairs and a 60-item queue; source verification and bounded tests, not study or human review): `ev:why-firms-hedge` narrowed (Tufano (1996) and Jin and Jorion (2006) read at abstract level and merged into the hedging entry: neither supports the value channel). The record is in `notes/migration-slices.md`, *Third batch of 17 October 2026*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `mod:duration-convexity` (`rates-credit-mortgages`); `mod:factor-risk-model` (`portfolio-construction`); `def:arbitrage` (`execution-market-making`).

## Entry backlog

- meth:time-varying-hedge-ratio: rolling-window and bivariate-GARCH hedge ratios and their out-of-sample variance reduction (`ec-baillie-myers-1991`, `ec-lien-tse-2002`; blocked on 2026-10-17, paywalled, no open copy found).
- ev:why-firms-hedge: (narrowed in the third batch of 2026-10-17) (narrowed 2026-10-17: Froot, Scharfstein and Stein's theory merged) the evidence, Tufano (1996) and Jin and Jorion (2006), not obtained.
- mod:theory-of-storage: inventories, convenience yield and the basis (home pathway `commodity-storage-curves`; `ec-working-1948`, `ec-brennan-1958`; blocked on 2026-10-17, no open copy found).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway after slice 31.

## What changed in my view or practice

## Questions carried forward
