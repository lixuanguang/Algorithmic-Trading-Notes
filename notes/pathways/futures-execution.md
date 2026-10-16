---
key: futures-execution
section: execution-trading-costs
status: not started (draft entries from the migration only)
---

# Futures execution: matching, rolls and settlement

Pathway outcome, from the guide: execute futures orders and rolls using the contract's matching algorithm, settlement mechanisms and cross-market price discovery, and measure roll costs. Its checkpoint identifies one contract's Globex matching algorithm and estimates passive fill probability, then plans a calendar roll (early, in the index roll window, and through trade-at-settlement), measuring spread, impact, calendar-spread slippage and settlement-price risk. Its ten readings begin with futures–cash price discovery (`w5-garbade-silber`, `ex-hasbrouck-2003`) and CME matching (`ex-cme-matching`), then evidence on matching changes, the Flash Crash, Treasury delivery, rolls, index investment and trade-at-settlement.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 15 October 2026 by migration slice 19 (`notes/migration.md`), which migrated the legacy futures-market-microstructure file mapped to this pathway alone. The entries come from migration and source checking against CME Group's rulebook, advisory notices and client documentation as retrieved on 15 October 2026, a dated CFTC filing, Hasbrouck's working paper, and Harris (2002). That is not study of the readings; it is not the checkpoint either, and no roll costs were measured.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 19, 2026-10-15:

- `conv:cme-globex-trading`: the centralised market and its permitted off-exchange exceptions; CME Globex matching algorithms, with SOFR futures' pro-rata allocation as the named example; the pre-open and indicative opening price; the E-mini S&P 500 daily settlement window as of 2020.
- `conv:futures-block-efrp`: CME Rule 526 block trades and Rule 538 EFRPs (eligibility, related position, reporting and submission), and the prohibition of transitory EFRPs since 2014, with Harris's 2002 history kept apart.
- `mech:futures-margin-settlement`: settlement variation each cycle (Rule 814), performance bond (Rule 820) and the default waterfall (Rule 802.B); daily settlement bounds credit risk but does not eliminate it.
- `ev:index-futures-price-discovery`: Hasbrouck's evidence that E-minis led price discovery for the S&P 500 and Nasdaq-100 in March–May 2000 (working-paper draft), with the legacy explanations marked as untested.

Corrected in a follow-up the same day (`notes/migration.md`, *Slice 19 follow-up*): the default waterfall of Rules 802.A–B and the retention wording of Rule 820; the settlement procedure located in Exhibit B of the 2020 filing, with its tiers and rounding; Rule 538.K's exception and 538.A's carve-out.

All four: verification partly checked 2026-10-15, stability draft; human review outstanding. Their artefact is `notes/artefacts/futures-execution/derivations.tex`.

Changed in migration slice 31, 2026-10-15: `mech:futures-margin-settlement` gains Hull's generic margin account (initial, maintenance and variation margin, margin calls, interest, securities as margin, clearing-member net margining and guaranty fund; 11th Global edition, chap. 2, pp. 51-54), marked as illustration, not any clearing house's rules, beside the CME rules already there. Its artefact is `notes/artefacts/volatility-options/hull-basics.tex`.

Changed in migration slice 34, 2026-10-16: `conv:cme-globex-trading` (a note that pro-rata remainders need a further rule, with CME's own allocation steps not read, and a cross-reference to the general matching entry owned by `execution-market-making`).

Written in migration slice 37, 2026-10-16, from the legacy macro chapter:

- `conv:government-bond-futures`: Gliner's 2013--2014 U.S. Treasury contract sizes and ticks (recomputed), physical delivery and cheapest-to-deliver, the German Schatz, Bobl and Bund, and why the futures trade below the bond (carry, not term premium); verification partly checked 2026-10-16, stability draft.

## Source verification after slice 37

Slice-37 follow-up, 2026-10-16 (source verification, not study): `conv:treasury-bund-futures-current-specs` narrowed. Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 follow-up*.

Second slice-37 follow-up, 2026-10-16 (source verification, not study): `conv:treasury-bund-futures-current-specs` unchanged (CME still refused access; recorded as an access barrier). Entries corrected in the same follow-up are listed in `notes/migration-slices.md`, *Slice 37 second follow-up*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `def:block-trade` and `def:portfolio-trading` (`execution-trading-costs`); `res:spread-determinants`, which took the large-tick block (`execution-market-making`).

## Entry backlog

- ev:futures-tick-size-evidence: whether futures "often" have economically large ticks relative to comparable equities, with bounce and larger displayed depth, as the legacy principle claimed; only the general large-tick mechanism (Lehalle and Laruelle, pp. 144–148) was checked.
- conv:treasury-bund-futures-current-specs: CME's TU, FV, TY, US and UB contract terms from its rulebook, which still refused automated access on 2026-10-16 (HTTP 403 to the shell and the fetching tool; the CFTC-hosted filings found were from 2011-2012 or unrelated); Eurex's Schatz, Bobl, Bund and Buxl terms were read on 2026-10-16

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. After slice 19 no legacy file lists this pathway alone; it remains a candidate for 18 shared blocks.

## What changed in my view or practice

## Questions carried forward

- Read Garbade and Silber (1983) for the theory of futures–cash price discovery; it had no open copy.
- Compare the Hasbrouck working-paper draft (2000) with the published Journal of Finance version, whose S&P 400 result the catalogue describes as shared rather than ETF-dominated.
- Check the current CME E-mini S&P 500 settlement procedure page (not retrievable on 2026-10-15) and CME Clearing's intraday settlement-cycle times.
