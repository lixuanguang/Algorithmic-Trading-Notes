---
key: time-value-cash-flows
section: financial-mathematics
status: not started (draft entries only, not from study)
---

# Time value of money, discounting and cash-flow valuation

Pathway outcome, from the guide: price a finite or perpetual stream of dated cash flows, convert between compounding and quoting conventions, solve for the internal rate of return and recognise its pitfalls, and price a forward contract by cost of carry with the same no-arbitrage argument. Prerequisites, from the guide: the section overview and algebra with geometric series. Its four required readings: `fm-openstax-principles-finance` (registered in the compendium as `principles-of-finance-2026`), `corp-berk-demarzo`, `catalogue-0233` (Tuckman and Serrat, *Fixed Income Securities*, 4th edition) and `s7-hulloptions`. This note is for a pathway of the section `financial-mathematics`; it is printed as Section 1.1 of the chapter.

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 23 October 2026 by the unit review of this pathway (review record in `notes/source-review-records.md`, *Time value and cash flows unit review, 23 October 2026*). A correction pass the same day (same record, *Correction pass*) corrected the IRR definition and rule, the annuity-due and perpetuity boundaries, the zero-rate loan limits and one printed figure. The entries come from source checking and derivation, not study. Of the required readings, OpenStax 2e was read at secs. 7.1-7.4, 8.1-8.4, 9.1, 16.3 and 16.5 (and earlier at 3.4, 10.2, 11.2), and Hull at chap. 4, sec. 4.4, chap. 5, sec. 5.5, and chap. 6, sec. 6.1 (and earlier at secs. 4.5-4.8, 11.4 and 13.1). `corp-berk-demarzo` and `catalogue-0233` were not available and are unread; nothing in the entries rests on them.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted. The checkpoint asks the reader to build and test a small library: rate conversions, annuity and loan schedules, an IRR solver with a two-IRR example, and a share forward checked against replication. The worked examples in `notes/artefacts/time-value-returns/time-value-return-checks.py` are editorial checks of the entries' figures; they are not that library and do not count as the checkpoint.

## Entries

In compiled order (`financial-mathematics/time-value.tex`, the pathway's only topic file). The order runs from single amounts to streams, loans and the IRR, then to required returns, instrument values and no arbitrage:

- `def:time-value-compounding` (new, 23 October 2026): time value, lump sums and timelines; simple against compound interest; FV and PV; compounding frequency as units; stated against effective rates; simple money-market rates and day counts; conversion by equating growth factors; solving for rate and periods; the rule of 72 and its error.
- `meth:cash-flow-streams` (new): mixed streams; ordinary annuity and annuity due, derived as a geometric series; perpetuity, growing perpetuity and growing annuity, with the r = g and g >= r boundaries; non-annual payments with nominal against effective rates. Corrected 23 October 2026: the annuity due is larger only for r > 0 (equal at 0, smaller for -1 < r < 0); domains of the finite and perpetual formulas; C/r has its first payment at t = 1; future value printed as 5,637.0930.
- `meth:loan-amortisation` (new): level payment, interest and principal split, schedule recursion, balance as the PV of remaining payments, total interest; a four-year hand-checkable schedule and OpenStax's auto loan recomputed. Corrected 23 October 2026: the domain and the zero-rate limits A = L/N and B_k = L(1 - k/N).
- `meth:internal-rate-of-return` (new): definition, bisection and Newton steps, Descartes' bound and uniqueness for conventional streams, two IRRs, no IRR, borrowing-type streams, the reinvestment statement read as one about realised wealth, scale and the crossover rate. Capital-budgeting ranking stays in `meth:capital-project-evaluation`. Corrected 23 October 2026: an IRR is any rate with NPV = 0, crossing not required (double-root example -100, 220, -121 at 10 percent); Descartes' rule with multiplicity and equally spaced periods; bracketing certifies only crossing roots; solutions validated by domain and residual; the hurdle rule restricted to conventional investments, with the reversed comparison kept for borrowing streams; bracketing only where a sign-change bracket exists; a conventional investment's single IRR distinguished from its sign (final wording pass).
- `def:required-return-components` (moved from first to fifth place; text unchanged): Fisher relation, risk premia.
- `meth:instrument-present-value` (coupons, face value and yield to maturity defined at first use; See also updated; figures unchanged).
- `res:cash-flow-additivity` (fourth consequence added: forward on an asset with known income, with a discrete-compounding share example and its replication ledger; other figures unchanged).

## Related entries owned elsewhere

- `def:interest-rate-measures` (rates chapter): reference rates, Hull's conversion formulas, zero and par yields. It also states the level-annuity identities and the EAR, without a source; they now overlap with `meth:cash-flow-streams` and `def:time-value-compounding`. Left unchanged here because it belongs to another unit.
- `def:bond-yield-spread-measures`, `meth:bond-price-from-yield`, `meth:floating-money-market-yields`, `conv:us-rate-quotation`: bond yield periodicity, pricing between coupon dates, money-market quotations and day counts.
- `res:cost-of-carry-forward-price`, `meth:arbitrage-replication-carry`, `meth:forward-price-value-lifecycle`: canonical forward pricing by cost of carry, continuous compounding, and forward value over the life.
- `meth:capital-project-evaluation`, `meth:capital-allocation-principles`: NPV against IRR in capital budgeting, capital rationing and unequal lives.
- `def:return-measures` (next pathway, `return-measurement`): the money-weighted return as an IRR.

## Entry backlog

## Remaining gaps

- `corp-berk-demarzo` (Part 2, interest rates and decision rules) and `catalogue-0233` (discount factors, day counts, yields) are unread required readings. Next action: obtain them and compare against the EAR/APR treatment, the IRR rule's failure cases and Tuckman and Serrat's discount-factor approach.
- The overlap with `def:interest-rate-measures` should be resolved when the rates unit is reviewed: keep the time-value identities in this pathway and cross-reference them from there.
- Not covered in this unit: the modified IRR, irregular-date (XIRR-style) worked examples beyond a sentence, annuities with payment frequency different from compounding frequency beyond the effective-rate conversion, and taxes or fees in loan costs (the APR as a regulatory measure).
- OpenStax equations were read in web renderings, partly garbled, and reconstructed from the printed numbers; the cited sections have no page numbers.
- The root-counting argument is stated for equally spaced periods only; irregular-date streams have no bound on the number of IRRs in the entry.
- Human review of the four new entries, and of the correction pass, is outstanding.

## What changed in my view or practice

## Questions carried forward
