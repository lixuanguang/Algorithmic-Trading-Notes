---
key: alpha-afml
pathways: [model-governance-controls, statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources, portfolio-construction]
version: Marcos López de Prado, Advances in Financial Machine Learning, John Wiley & Sons, Hoboken, 2018 (ISBN 9781119482086 hardcover, 9781119482116 ePDF), copyright 2018. Copy used: a local PDF outside the repository with a text layer (printed page = PDF page - 27 in chap. 1)
sections: chap. 1, secs. 1.2.2 "The Meta-Strategy Paradigm" (p. 5) and 1.3.1 "Structure by Production Chain" (pp. 6-9), text layer, read for migration slice 30; chaps. 2-5 (pp. 23-89, with exercises and snippets), text layer and page images of the equations, figures and tables used, read for migration slice 32 (printed page = PDF page - 27 throughout chaps. 1-5); nothing else read
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 30 from source checks, not from study: the headings that need your own reading are left empty. Extended on 2026-10-16 by migration slice 32 (chaps. 2-5), also from source checks. The route `statistical-learning-foundations` names this book as a required reading ("purged and embargoed cross-validation and finance-specific labelling"); chap. 7, which that line refers to, is unread. The legacy notes' *Chains of Production for Alpha Signals* block and the machine-learning item of their alpha-models file follow these pages closely. The catalogue lists this book; no route checked here names it as a reading of `model-governance-controls`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- "It takes almost as much effort to produce one true investment strategy as to produce a hundred"; the meta-strategy paradigm, applied by "every successful quantitative firm I am aware of" (p. 5).
- Macroscopic alpha from simple tools "quickly converging to zero"; "the only true alpha left is microscopic" and needs heavy ML tools (p. 6).
- Stations: data curators, feature analysts, strategists ("features may be discovered by a black box, but the strategy is developed in a white box"), backtesters (probability of backtest overfitting from the number of trials; results to management only), deployment team (pp. 7-8).
- Portfolio oversight: embargo, paper trading, graduation, re-allocation ("in general" concave allocation), decommission when the theory "is no longer backed by empirical evidence"; new variations run in parallel (pp. 8-9).

- Chap. 2 (pp. 23-41): four types of financial data (Table 2.1; Bloomberg's fundamental indexing lag "often by 1.5 months"; FIX data "over 10TB" a day, unsourced); time, tick, volume and dollar bars, with the evidence cited (Mandelbrot-Taylor "may", Clark, Ane-Geman) and Figure 2.1 on E-mini; tick rule with $b_0$ from the previous bar; imbalance and runs bars with EWMA thresholds from prior bars; the ETF trick, PCA risk-distribution weights (Snippet 2.1), the single futures roll and the non-negative rolled series (Snippets 2.2-2.3); sampling for reduction; the CUSUM filter, sampled "if and only if $S_t\ge h$, at which point $S_t$ is reset", Snippet 2.4 resetting only the triggered side.
- Chap. 3 (pp. 43-56): fixed-horizon labels and three objections; daily volatility (Snippet 3.1); triple barrier, configurations, side and size; meta-labelling, with unsupported claims that it "will increase your F1-score" and that "the effects of overfitting are limited" (pp. 52-53); quantamental use; dropping rare labels.
- Chap. 4 (pp. 59-73): overlapping outcomes; concurrency and average uniqueness, used "on the training set ... and not on the testing set" (p. 62); bootstrap redundancy; sequential bootstrap, toy example $(5,3,6)/14$, Monte Carlo medians 0.6 and 0.7; return attribution (weights sum to $I$); time decay on cumulative uniqueness; class weights.
- Chap. 5 (pp. 75-89): fractional differencing weights and recurrence; expanding window and FFD; minimum $d$ by ADF, E-mini crossing near $d=0.35$ with correlation 0.995, 87 futures all below $d=0.6$ (Table 5.1).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`meth:strategy-production-lifecycle`. Slice 32: `meth:activity-sampled-bars`, `meth:information-driven-bars`, `meth:etf-trick`, `meth:event-based-sampling`, `meth:triple-barrier-labelling`, `meth:meta-labelling`, `def:label-concurrency-uniqueness`, `meth:sequential-bootstrap`, `meth:sample-weights-attribution-decay`, `mod:fractional-differencing-weights`, `meth:fixed-width-fractional-differencing` (`statistical-learning-foundations`); `pit:label-weight-leakage` (`financial-ml-evaluation`); `def:financial-data-types` (`alternative-data-sources`); `mod:pca-risk-distribution-weights` (`portfolio-construction`).

Slice-32 follow-up, 2026-10-16: rechecked pp. 60--61, 64--66 and 69 (text layer) for the indicator convention: the printed toy matrix (p. 65) marks the returns ending at $t=1,\dots,6$ that each label compounds, Snippet 4.6 codes it in start-time indexing, and Snippets 4.1, 4.3 and 4.10 mark the event's own bar; see `def:label-concurrency-uniqueness`. The ETF-trick timing (p. 34) restated in `meth:etf-trick`.

## Open questions

- The stages carry no quantitative promotion or decommission criteria; which governance readings supply them?
- The book's own slips found in slice 32: $(1-K^{-1})^I\approx e^{-K/I}$ (p. 62; it is $e^{-I/K}$); $d[1]=c$ and "the oldest portion $cT$" in the time decay (pp. 70-71); $\bar u^{(2)}_j$ written with $u_{t,j}$ (p. 64); the weight-loss sum to $T$ and the FFD range $T-l^*+1,\dots,T$ (pp. 80, 82); $E_{i-1}[y_t]$ in the CUSUM run condition (p. 39); "$1-P[b_t=-1]$" for the runs expectation (p. 31). Check the errata or a later printing.
- Meta-labels are refitted "on the same training set" (p. 53) and $d$ is chosen on the full sample (p. 85): what does chap. 7 require?
