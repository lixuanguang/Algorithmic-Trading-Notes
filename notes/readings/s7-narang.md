---
key: s7-narang
pathways: [backtest-inference]
version: Rishi K. Narang, Inside the Black Box: A Simple Guide to Systematic Investing, third edition, John Wiley & Sons, Hoboken, 2024 (ISBN 9781119931911, Adobe PDF), copyright 2024. Copy used: a local PDF outside the repository with a text layer (printed page = PDF page - 20). The catalogue entry carries the first edition's subtitle and says the edition is not established; no route lists this key as a reading
sections: chap. "Research" (chap. 9), secs. 9.1-9.4, pp. 161-187, text layer, with Exhibits 9.2, 9.3 and 9.5 (pp. 171, 172, 178) by page image (checked for migration slice 25)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 25 from source checks, not from study: the headings that need your own reading are left empty. The legacy notes were read before the study method (`notes/log.md`, "Completed"); which edition they followed is not recorded, but their wording and order match this edition's chapter 9.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Scientific method: observe, theorise, deduce consequences, test by attempted falsification; at best, enough confidence to risk capital; research must continue because markets change (sec. 9.1, pp. 161-163).
- Four sources of ideas: market observation, academic literature (and other sciences), migration of researchers, discretionary traders' lessons (sec. 9.2, pp. 163-165).
- Diagnostics on a daily S&P 500 equity-risk-premium strategy, June 1982 to December 2000: 746% cumulative, 12.1% a year before costs; volatility 21.2%; worst drawdown -39.7%; R² 0.0085; zero signal 65% of days, 19% wins, 16% losses; IR 0.57, Sterling 0.87, Calmar 0.31, Omega 1.26; one-day delay raises the total to 870% (12.9% a year) (sec. 9.3.2, pp. 168-176).
- "A superb R² in our industry is 0.05 (out of sample)" (p. 171), a practitioner judgement with no sample.
- Text-figure mismatch, p. 172: the text gives the two most bearish quintiles average returns of -2.35% and -0.19%; in Exhibit 9.3 these are the signal-bucket labels, and the bars (next-day returns) run from about -0.03% to +0.13%.
- Overfitting: nearby parameters should give similar results; choose a plateau with margins (Exhibit 9.5, point B); parsimony; overfitting as Type I and underfitting as Type II error, with the balance shifting since the early 2010s (secs. 9.3.2.10-9.3.3, pp. 176-183). Out-of-sample R² ratio "about half or better" considered good; burning data (sec. 9.3.4, pp. 183-185).
- Testing assumptions: the 55/45, $0.01 cost example (+$0.10 to -$0.90 per 100 shares); over- and underestimated costs; err towards overestimating; hard-to-borrow lists; historical HTB data hard to obtain (sec. 9.3.5, pp. 185-186).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`meth:hypothesis-driven-strategy-research`, `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting`, `pit:backtest-cost-short-assumptions`.

## Open questions

- Narang's "naked short sale, which is illegal in the United States" (p. 186) is broader than Regulation SHO's locate and close-out rules; not adopted.
