---
key: hull-tn19
pathways: [volatility-options]
version: John Hull, Technical Note No. 19, "Valuation of an Equity Swap", Options, Futures, and Other Derivatives, one page, undated. The author's URL (www-2.rotman.utoronto.ca/~hull/TechnicalNotes/TechnicalNote19.pdf) returned HTTP 404 on 2026-10-18, as did the notes index; the copy read is the Internet Archive's capture of 28 August 2025 (SHA-256 fbd0c0b8bb7051bb988f2a2add19dd41cba1b2a8366cb8e69a13f7e9ecb84356). The archived index of 1 April 2024 lists note 19 as the equity-swap note.
sections: the whole note
read:
status: draft
---

Prepared on 2026-10-18 by the correction pass on PR #24 from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:swap-valuation-replication`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Notation: R0 the floating rate fixed at the last reset for tau0; R the (LIBOR) rate from now to the next payment over tau; E0 and E the index at the last reset and now; L the principal. Borrowing L E/E0 at R and investing it in the index creates, at no cost, the exchange of L E1/E0 for L (E/E0)(1 + R tau). Adding L to both sides of the actual exchange gives L E1/E0 for L(1 + R0 tau0).
- Value to the receiver of the equity return: L E/E0 - L(1 + R0 tau0)/(1 + R tau). Separating the floating payment L R0 tau0/(1 + R tau) leaves L E/E0 - L/(1 + R tau) for the next equity payment, which disagrees with the textbook's L(E - E0)/E0 (11th Global ed., p. 778) by L(1 - 1/(1 + R tau)).

## Limits

LIBOR-era note with a floating rate fixed in advance; the compendium extends it to SOFR compounded in arrears by replication. Archived copy, not the author's live site.
