---
key: statistical-learning-foundations
section: ml-alternative-data
status: not started (draft entries from the migration only)
---

# Statistical learning foundations and time-series validation

Pathway outcome, from the guide: fit and tune regularised, tree-based and neural models, estimate their out-of-sample error with a validation scheme suited to dependent, non-stationary data, and explain what the model uses. Its checkpoint fits ridge, lasso, random forest and gradient boosting on a monthly stock-characteristic panel, compares shuffled, blocked, purged-and-embargoed and rolling-origin error estimates with the error on an untouched final period, and reports SHAP importances and conformal coverage by year. Its sixteen readings run from the textbooks (`s6-isl`, `s6-esl`, `prob-learning`) and methods papers (`catalogue-0736`, `w5-zou-hastie-enet`, `wide-breiman-rf`, `wide-xgboost`, `wide-grinsztajn-tabular`, `wide-prince-udl`) through validation (`rf-arlot-celisse-2010`, `rf-bergmeir-hyndman-koo-2018`, `rf-cerqueira-torgo-mozetic-2020`) to López de Prado (`alpha-afml`, "purged and embargoed cross-validation and finance-specific labelling"), conformal prediction and interpretability (`wide-angelopoulos-bates-conformal`, `catalogue-0730`, `w5-rudin-stop-explaining`).

## Status

Not mastered and not consolidated: no dates in `notes/log.md`. Opened on 16 October 2026 by migration slice 32 (`notes/migration-slices.md`), which migrated the legacy AFML data cluster (`ml-alternative-data/data/`, five files) and closed the legacy chapter. The entries come from source checking against López de Prado's chaps. 2–5, the pathway's thirteenth reading, read only in those chapters; that is not study of it, and chap. 7 (purged and embargoed cross-validation), which the checkpoint needs, is unread. No other reading has been opened and the checkpoint was not attempted.

## Outcome in my own words

## How the readings fit together

## Checkpoint

Not attempted.

## Entries created or changed

Written in migration slice 32, 2026-10-16:

- `meth:activity-sampled-bars`: time, tick, volume and dollar bars; what each corrects (auction prints, fragmentation, price level, issuance); the evidence on their return distributions as cited (Mandelbrot–Taylor, Clark, Ané–Geman, whose ranking of trades over volume conflicts with Clark's), not guaranteed.
- `meth:information-driven-bars`: tick rule with its boundary condition; imbalance and runs bars in a corrected table (the legacy runs statistics collapsed to $T$); causal EWMA thresholds from prior bars; the unstated independence assumption and Jensen gap; collapse of the threshold on a balanced flow.
- `meth:etf-trick`: the \$1-invested series for baskets and spreads, holdings sized at the next open (execution, not look-ahead), costs, tradable volume, the single futures roll with the previous-raw-price return; positivity not guaranteed with short legs.
- `meth:event-based-sampling`: linspace and uniform downsampling; the CUSUM filter with its sampling, reset and strict-inequality conventions, and the mismatch between "IID observations" and the snippet's differencing.
- `meth:triple-barrier-labelling`: fixed horizons and their three limits; volatility-scaled barriers known at the decision time; first touch, configurations, intrabar ties (unspecified in the source), side against size.
- `meth:meta-labelling`: López de Prado's side-and-size method; his F1 and overfitting claims stated as claims; out-of-sample primary predictions required (interpretation); the legacy's steps and figure traced to a Hudson & Thames blog, its limitations to no source.
- `def:label-concurrency-uniqueness`: overlapping outcomes, concurrency, uniqueness and average uniqueness, with the training-set condition on "no leakage".
- `meth:sequential-bootstrap`: bootstrap redundancy, inflated out-of-bag accuracy, the sequential bootstrap and its Monte Carlo evidence; López de Prado's $e^{-K/I}$ approximation corrected to $e^{-I/K}$.
- `meth:sample-weights-attribution-decay`: return-attribution weights summing to $I$ (large returns weigh more), time decay on cumulative uniqueness (the source's $d[1]$ and $cT$ slips corrected), class weights.
- `mod:fractional-differencing-weights`: binomial weights, recurrence, integer cases, signs, and a power-law decay rate in place of the source's product argument.
- `meth:fixed-width-fractional-differencing`: expanding window and weight loss with one consistent index, FFD with its range corrected, the minimum-$d$ ADF procedure and its evidence; ADF rejection is not demonstrated stationarity, and $d$ is to be chosen on training data.

All partly checked 2026-10-16, draft; human review outstanding. Artefacts: `notes/artefacts/statistical-learning-foundations/` (the five legacy files verbatim, the wrappers and the four original figures, and `afml-checks.py`, the numerical checks).

## Related entries owned elsewhere

Cross-referenced, not owned here: `pit:label-weight-leakage` (`financial-ml-evaluation`); `def:financial-data-types` (`alternative-data-sources`); `data:trading-reference-data`, `data:market-data-levels`, `data:derived-market-statistics` (`point-in-time-data`); `mod:pca-risk-distribution-weights` (`portfolio-construction`); `pit:parameter-overfitting` (`backtest-inference`); `meth:strategy-production-lifecycle` (`model-governance-controls`).

## Entry backlog

- meth:purged-embargoed-cross-validation: purging overlapping training labels and embargoing after the test set, and why shuffled k-fold and out-of-bag estimates are inflated, as the checkpoint asks (`alpha-afml` chap. 7, `rf-bergmeir-hyndman-koo-2018`, `rf-cerqueira-torgo-mozetic-2020`, unread).
- ev:transaction-clock-normality: evidence on returns sampled by trades, volume or dollars (Clark 1973, Ané and Geman 2000, whose paper was not read beyond its abstract, and the replication critique of Murphy and Izzeldin, working paper 2006, read only by the slice-32 review).
- ev:meta-labelling-performance: whether meta-labelling improves precision, F1 or after-cost results out of sample (no source identified; López de Prado's claims are unsupported in chap. 3).
- meth:fractional-integration-tests: testing a fractionally differenced series against fractional rather than unit-root alternatives (MacKinnon and Nielsen 2014, listed by López de Prado; unread).

## Legacy candidate material

Run `python3 tools/migration_status.py` for the current counts. No legacy file lists this pathway: slice 32 migrated the five AFML data files and removed the legacy ML chapter. That says nothing about consolidation.

## What changed in my view or practice

## Questions carried forward

- López de Prado's own slips (the overlap approximation, the time-decay $d[1]$ and $cT$, the expanding-window and FFD index ranges, $E_{i-1}[y_t]$): check the author's errata or a later printing.
- Which source did the legacy notes' meta-labelling feature list and limitations follow?
