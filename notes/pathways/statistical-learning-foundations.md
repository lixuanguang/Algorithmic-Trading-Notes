---
key: statistical-learning-foundations
section: ml-alternative-data
status: not started (draft entries only, not from study)
---

# Statistical learning foundations and time-series validation

Pathway outcome, from the guide: fit and tune regularised, tree-based and neural models, estimate their out-of-sample error with a validation scheme suited to dependent, non-stationary data, and explain what the model uses. Its checkpoint fits ridge, lasso, random forest and gradient boosting on a monthly stock-characteristic panel, compares shuffled, blocked, purged-and-embargoed and rolling-origin error estimates with the error on an untouched final period, and reports SHAP importances and conformal coverage by year. Its sixteen readings run from the textbooks (`s6-isl`, `s6-esl`, `prob-learning`) and methods papers (`catalogue-0736`, `w5-zou-hastie-enet`, `wide-breiman-rf`, `wide-xgboost`, `wide-grinsztajn-tabular`, `wide-prince-udl`) through validation (`rf-arlot-celisse-2010`, `rf-bergmeir-hyndman-koo-2018`, `rf-cerqueira-torgo-mozetic-2020`) to López de Prado (`alpha-afml`, "purged and embargoed cross-validation and finance-specific labelling"), conformal prediction and interpretability (`wide-angelopoulos-bates-conformal`, `catalogue-0730`, `w5-rudin-stop-explaining`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by financial data and labels review (`notes/source-review-records.md`). The entries come from source checking against López de Prado's chaps. 2–5, the pathway's thirteenth reading, read only in those chapters; that is not study of it, and chap. 7 (purged and embargoed cross-validation), which the checkpoint needs, is unread. No other reading has been opened and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in financial data and labels / source review / optimal execution / execution control reviews:

- `meth:activity-sampled-bars`: time, tick, volume and dollar bars; what each corrects (auction prints, fragmentation, price level, issuance); the evidence on their return distributions as cited (Mandelbrot–Taylor, Clark, Ané–Geman, whose ranking of trades over volume conflicts with Clark's), not guaranteed.
- `meth:information-driven-bars`: tick rule with its boundary condition; imbalance and runs bars in a corrected table (a runs statistic that collapsed to $T$ corrected); causal EWMA thresholds from prior bars; the unstated independence assumption and Jensen gap; collapse of the threshold on a balanced flow.
- `meth:etf-trick`: the \$1-invested series for baskets and spreads, holdings sized at the next open (execution, not look-ahead), costs, tradable volume, the single futures roll with the previous-raw-price return; positivity not guaranteed with short legs.
- `meth:event-based-sampling`: linspace and uniform downsampling; the CUSUM filter with its sampling, reset and strict-inequality conventions, and the mismatch between "IID observations" and the snippet's differencing.
- `meth:triple-barrier-labelling`: fixed horizons and their three limits; volatility-scaled barriers known at the decision time; first touch, configurations, intrabar ties (unspecified in the source), side against size.
- `meth:meta-labelling`: López de Prado's side-and-size method; his F1 and overfitting claims stated as claims; out-of-sample primary predictions required (interpretation); the common steps and figure traced to a Hudson & Thames blog, the limitations to no source.
- `def:label-concurrency-uniqueness`: overlapping outcomes, concurrency, uniqueness and average uniqueness, with the training-set condition on "no leakage".
- `meth:sequential-bootstrap`: bootstrap redundancy, inflated out-of-bag accuracy, the sequential bootstrap and its Monte Carlo evidence; López de Prado's $e^{-K/I}$ approximation corrected to $e^{-I/K}$.
- `meth:sample-weights-attribution-decay`: return-attribution weights summing to $I$ (large returns weigh more), time decay on cumulative uniqueness (the source's $d[1]$ and $cT$ slips corrected), class weights.
- `mod:fractional-differencing-weights`: binomial weights, recurrence, integer cases, signs, and a power-law decay rate in place of the source's product argument.
- `meth:fixed-width-fractional-differencing`: expanding window and weight loss with one consistent index, FFD with its range corrected, the minimum-$d$ ADF procedure and its evidence; ADF rejection is not demonstrated stationarity, and $d$ is to be chosen on training data.

All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/statistical-learning-foundations/` (`afml-checks.py`, the numerical checks).

Changed in the financial data and labels review follow-up, 2026-10-16: `meth:etf-trick` (the next-open sizing is an accounting convention, reproducible only by notional orders filled in full at a single opening price; gross exposure $|K_t|$ with positive prices and conversion factors; holdings reverse at $K_t<0$, so a series that exhausts its capital stops describing the strategy); `def:label-concurrency-uniqueness` (indicator $t_{i,0}<t\le t_{i,1}$ for returns indexed by ending time; López de Prado's toy matrix is consistent, his Snippets 4.1, 4.3 and 4.10 include the event's own bar, which is not equivalent); `meth:sample-weights-attribution-decay` (sum from $t_{i,0}+1$); `meth:triple-barrier-labelling` (the returns a label uses). Checks in `notes/artefacts/statistical-learning-foundations/financial-labels-capital-checks.py`.

Changed in dealer models and information / source review / optimal execution / execution control reviews: `meth:triple-barrier-labelling` (two arbitrage-label items compared with the path argument on p. 44). Partly checked, draft.

- `meth:purged-embargoed-cross-validation`: purging and embargo (AFML chap. 7), inflated out-of-bag scores, and when ordinary K-fold or time-ordered holdouts are appropriate. Partly checked 2026-10-17, draft.

## Source verification after macro markets and pricing review

source verification (2026-10-17) (source verification and bounded tests, not study or human review): `meth:purged-embargoed-cross-validation` resolved as a new entry in `ml-alternative-data/labelling-sample-weights.tex`: López de Prado chap. 7 (pp. 103-109, p. 106 as page images, where the printed information-set condition reads '= ∅' but must mean '≠ ∅') and sec. 6.3.3 on inflated out-of-bag accuracy; Bergmeir, Hyndman and Koo (working paper of 23 July 2017) on when ordinary K-fold is valid; Cerqueira, Torgo and Mozetič (arXiv v1, not the 2020 journal version). `notes/artefacts/statistical-learning-foundations/cv-checks.py` shows that Snippet 7.3 keeps labels touching the test block at one bar, which the closed-interval rule would purge. The record is in `notes/source-review-records.md`, *source verification (2026-10-17)*.

method validation (2026-10-17) (audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): Audit repair: `meth:purged-embargoed-cross-validation` now presents López de Prado's performance plateau as a source heuristic, not proof of no leakage, lists leakage that does not grow with k, and keeps the overlap and endpoint corrections; information provenance and a time-valid evaluation remain necessary. The record is in `notes/source-review-records.md`, *method validation (2026-10-17)*.

empirical extensions (2026-10-17) (six audit repairs and a source-review coverage; source verification and bounded tests, not study or human review): `ev:transaction-clock-normality` narrowed (Murphy and Izzeldin's working paper merged); `ev:meta-labelling-performance` unchanged (no open out-of-sample evaluation found (arXiv, Crossref and web searched); Joubert's journal articles are paywalled); `meth:fractional-integration-tests` resolved (MacKinnon and Nielsen's working paper merged into the fractional-differentiation entry). The record is in `notes/source-review-records.md`, *empirical extensions (2026-10-17)*.

derivatives and empirical validation (2026-10-17) (seven audit repairs, backlog reconciliation and a source-review coverage; source verification and bounded tests, not study or human review): backlog reconciliation only: the backlog lines below were rewritten to state the remaining gap alone, removing stacked dated status prefixes and claims that material was unread or not obtained where earlier batches had read it. The record is in `notes/source-review-records.md`, *derivatives and empirical validation (2026-10-17)*.

## Related entries owned elsewhere

Cross-referenced, not owned here: `pit:label-weight-leakage` (`financial-ml-evaluation`); `def:financial-data-types` (`alternative-data-sources`); `data:trading-reference-data`, `data:market-data-levels`, `data:derived-market-statistics` (`point-in-time-data`); `mod:pca-risk-distribution-weights` (`portfolio-construction`); `pit:parameter-overfitting` (`backtest-inference`); `meth:strategy-production-lifecycle` (`model-governance-controls`).

## Entry backlog

- ev:transaction-clock-normality: Clark (1973) and the body of Ané and Geman (2000) (abstract read), for the evidence on returns sampled by trades, volume or dollars; Murphy and Izzeldin's replication critique (working paper) is merged.
- ev:meta-labelling-performance: whether meta-labelling improves precision, F1 or after-cost results out of sample: no open evaluation found (arXiv, Crossref and web searched on 2026-10-17); López de Prado's claims are unsupported in chap. 3.

## What changed in my view or practice

## Questions carried forward

- López de Prado's own slips (the overlap approximation, the time-decay $d[1]$ and $cT$, the expanding-window and FFD index ranges, $E_{i-1}[y_t]$): check the author's errata or a later printing.
