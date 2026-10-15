---
key: s7-narang
pathways: [backtest-inference, model-governance-controls, funding-crowding, portfolio-construction, execution-trading-costs]
version: Rishi K. Narang, Inside the Black Box: A Simple Guide to Systematic Investing, third edition, John Wiley & Sons, Hoboken, 2024 (ISBN 9781119931911, Adobe PDF), copyright 2024. Copy used: a local PDF outside the repository with a text layer (printed page = PDF page - 20). The catalogue entry carries the first edition's subtitle and says the edition is not established; no route lists this key as a reading
sections: chap. "Research" (chap. 9), secs. 9.1-9.4, pp. 161-187, text layer, with Exhibits 9.2, 9.3 and 9.5 (pp. 171, 172, 178) by page image (checked for migration slice 25); chap. "Risks Inherent to Quant Strategies" (chap. 10), secs. 10.1-10.6, pp. 191-211, text layer, with Exhibit 10.6 (p. 206) by page image (checked for migration slice 26); chap. "Transaction Cost Models" (chap. 5), secs. 5.1-5.3 and notes, pp. 85-97, text layer, with Exhibits 5.1-5.4 (pp. 93-95) and note 2 (p. 97) by page image; p. 98 is blank (checked for migration slice 27); chap. "Portfolio Construction Models" (chap. 6), secs. 6.1-6.5 and notes, pp. 99-125, text layer (contents: chap. 6 p. 99, notes p. 125; running heads checked), with Exhibits 6.1, 6.2, 6.4-6.7 and the example on p. 118 by page image (checked for migration slice 28)
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
- Correction 2026-10-15 (slice-25 follow-up): the S&P strategy is not always in the market. Its signal reads a higher stock earnings yield than the 10-year Treasury yield as long and a lower one as short (p. 168), but it trades only when the opportunity seems attractive enough, with a zero signal on 65% of days (p. 173); the adjustment and the threshold are not stated. Calmar (0.31) and Omega (1.26) are reported as positive, so the drawdown and the sum of negative returns are used as magnitudes, although his wording divides by negative numbers (pp. 173-174).
- Correction 2026-10-15 (slice-26 follow-up): his printed inputs give Calmar $12.1/39.7\approx0.3048$, which rounds to 0.30, not his reported 0.31 (pp. 173-174); the difference is not explained in the text. In the Pulte Homes passage he calls the episode "an interesting illustration of the quadratic nature of market impact" (p. 206); aggregate crisis-period returns and volume do not identify a metaorder impact exponent, so it is not evidence for or against any exponent.
- "A superb R² in our industry is 0.05 (out of sample)" (p. 171), a practitioner judgement with no sample.
- Text-figure mismatch, p. 172: the text gives the two most bearish quintiles average returns of -2.35% and -0.19%; in Exhibit 9.3 these are the signal-bucket labels, and the bars (next-day returns) run from about -0.03% to +0.13%.
- Overfitting: nearby parameters should give similar results; choose a plateau with margins (Exhibit 9.5, point B); parsimony; overfitting as Type I and underfitting as Type II error, with the balance shifting since the early 2010s (secs. 9.3.2.10-9.3.3, pp. 176-183). Out-of-sample R² ratio "about half or better" considered good; burning data (sec. 9.3.4, pp. 183-185).
- Risks inherent to quant strategies (chap. 10): model risk (inapplicability, misspecification, implementation errors), regime change, exogenous shocks and contagion or common-investor risk (secs. 10.1-10.4, pp. 191-209); exogenous shocks hard to address "other than with discretionary overrides" (p. 202); monitoring by exposure, P&L, execution and systems monitors (sec. 10.5, pp. 209-210).
- August 2007, his account (sec. 10.4.1, pp. 203-209): four drivers (crowding, weak prior returns, cross-collateralisation with illiquid credit strategies, risk targeting); "likely" about $1 trillion gross; leverage up 1.5-2 times as volatility fell; losses "solely the result of market impact"; -5% to -45% at funds. No position or flow data.
- Exhibit 10.6 (Pulte Homes, p. 206): -22.0%, -12.5%, +15.6%, -22.6%; the rebound recovers about a third of the 31.75% decline, not "about half", at roughly four to five times the earlier pace, not "about 20 times" (recomputed).
- Transaction cost models (chap. 5, pp. 85-97): costs "eat away between 20 and 50 percent" of returns for many successful quants (p. 85, unsourced); two reasons to trade, alpha or risk, and the benefit must clear the cost (p. 85); the model informs portfolio construction and does not minimise cost (pp. 85-86, 96). Components: commissions and fees (brokers' clearing and settlement fees usually inside commissions; $0.001 per share example), slippage from decision to arrival at the exchange (CVX sale, $100.00 to $99.90), market impact from arrival to execution (pp. 86-89); the slippage-impact interaction example ($100.00, $100.05, $100.20: -$0.05 and -$0.15) (p. 89); ECN take fee about 0.3 cents, rebate about 0.2 cents (p. 90).
- Four model forms, total cost against size: flat, linear, piecewise-linear, quadratic (sec. 5.2, pp. 91-96); exhibits schematic, unlabelled, with a convex "true" curve from zero; "any of the four ... can be valid in the right set of circumstances" (p. 96). Note 2 (p. 97): square-root cost per share for U.S. equities called better supported, but described as "an exponent of 1.5, or in other words, as the square root", which mixes total and per-share conventions.
- Portfolio construction (chap. 6, pp. 99-125): rule-based (equal position, equal risk, alpha-driven; decision-tree named only, p. 100) against optimisers. Two arguments against unequal weights: forecast power for size, and a few large bets on extreme signals (adverse selection, bad data) (pp. 101-102). Exhibit 6.1 (p. 102): volatilities 2.5% and 2.0%, "volatility-adjusted" weights 39/61, which are inverse-variance (inverse-volatility gives 44.4/55.6). Mean-variance inputs and extra practical inputs, "volatility or expected drawdown" (p. 105). GARCH "most widely used ... (particularly in equity trading)", EWMA about as good (pp. 108-110); S&P-Nikkei rolling correlation +0.01 to +0.66 (pp. 110-111); grouping similar names (p. 111); "1,998,000" correlations for 2,000 names, should be 1,999,000 (p. 113). Few strictly ML portfolio models (pp. 113-114). Unconstrained optimisers "often" give one instrument (p. 114), against his own max-Sharpe example at about 85% CVX and 75% NFLX (p. 106). Black-Litterman (p. 117; note 5 dates it 1982, text 1992); Grinold-Kahn factor portfolios, "not more than about 20", example +0.2% (pp. 117-118); resampling described as reordering returns, which leaves mean and volatility unchanged (pp. 118-119); convex optimisation, 10,000 assets in about one second (pp. 119-120); substitution effect (p. 121); efficient frontier, Exhibit 6.7 adapted from Quantpedia (p. 122).
- Testing assumptions: the 55/45, $0.01 cost example (+$0.10 to -$0.90 per 100 shares); over- and underestimated costs; err towards overestimating; hard-to-borrow lists; historical HTB data hard to obtain (sec. 9.3.5, pp. 185-186).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`meth:hypothesis-driven-strategy-research`, `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting`, `pit:backtest-cost-short-assumptions` (chap. "Research"); `def:quant-strategy-risk-sources`, `meth:quant-strategy-monitoring`, `def:common-investor-contagion` (chap. "Risks Inherent to Quant Strategies"); `mod:portfolio-transaction-cost-function` and the slice-27 merge into `def:transaction-costs` (chap. "Transaction Cost Models"); `meth:rule-based-position-sizing`, `mod:mean-variance-portfolio-optimisation`, `meth:signal-portfolio-allocation` (chap. "Portfolio Construction Models").

## Open questions

- Narang's "naked short sale, which is illegal in the United States" (p. 186) is broader than Regulation SHO's locate and close-out rules; not adopted.
