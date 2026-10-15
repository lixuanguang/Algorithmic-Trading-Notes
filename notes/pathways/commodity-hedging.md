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

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:derivative-contracts`, `res:cost-of-carry-forward-price` (`volatility-options`); `mod:duration-convexity` (`rates-credit-mortgages`); `mod:factor-risk-model` (`portfolio-construction`); `def:arbitrage` (`execution-market-making`).

## Entry backlog

- meth:time-varying-hedge-ratio: rolling-window and bivariate-GARCH hedge ratios and their out-of-sample variance reduction (`ec-baillie-myers-1991`, `ec-lien-tse-2002`, unread).
- ev:why-firms-hedge: theory and evidence on whether hedging adds value (`ec-froot-scharfstein-stein-1993`, `ec-tufano-1996`, `ec-jin-jorion-2006`, unread).
- mod:theory-of-storage: inventories, convenience yield and the basis (home pathway `commodity-storage-curves`; `ec-working-1948`, `ec-brennan-1958`, unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway after slice 31.

## What changed in my view or practice

## Questions carried forward
