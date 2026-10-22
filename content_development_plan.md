# Content development plan: return predictability and forecast evaluation

Status: deferred proposal, 22 October 2026; not started. No proposed new entry,
objective, note or artefact has been implemented. Owner: repository maintainer.

The next task is to align the compendium's subsections with the learning guide's
specialist pathways. This content batch is retained for later consideration;
committing this proposal does not authorize its implementation. After subsection
alignment, reassess the proposed file paths, heading placement, existing material
and batch scope, including the size question in section 8.3, before starting it.

This plan follows the completed content migration (commit `53e2b1c`; records in
[content_migration_plan.md](content_migration_plan.md) and
[content_migration_ledger.md](content_migration_ledger.md), kept as historical
evidence and not edited by this batch). Guide pin:
`6c7734ed49f1c242908b86a57c4f5d1f0e349ec0`.

## 1. Choice of batch

### 1.1 Candidates

Three small batches were ranked on five criteria: position in the guide's learning
order, readiness of prerequisites, source availability, how much existing material
can be extended rather than rewritten, and whether the claims can be checked
numerically from public data.

| Rank | Pathway (section) | Ledger state | Order and prerequisites | Sources | Numerical validation | Verdict |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `return-predictability` (`asset-pricing`, Part II) | Partial | Fourth of five in the asset-pricing specialist order. Guide prerequisites `time-series-volatility` (Note) and `empirical-asset-pricing` (Related, `asset-pricing/asset-pricing-models`) both have material | Welch–Goyal 2008 and Campbell–Thompson (NBER WP) are local and already checked in part; open working papers exist for Clark–West and Campbell–Shiller | Public annual and monthly predictor data on Goyal's site; synthetic Monte Carlo for test size | **Recommended** |
| 2 | `standard-errors-inference` (`asset-pricing`) | Partial | Second in the specialist order; a prerequisite of `event-studies` | None of its 16 required readings is on disk; open copies would have to be found for each | The checkpoint needs a licensed firm-month panel (CRSP) and a published IV replication; only simulation is possible without them | Next, once sources are obtained |
| 3 | `trend-following` (`multi-asset-systematic-macro`, Part III) | Partial | Later Part; prerequisites present | Moskowitz–Ooi–Pedersen and Hurst–Ooi–Pedersen are local and already cited | The checkpoint needs 40 continuous futures series, which are not public | Defer; the core evidence already sits in `def:alpha-model-taxonomy` |

### 1.2 Recommendation and rationale

Choose `return-predictability`. It has the best ratio of verifiable new content to
effort.

- *Clear unmet need.* Existing entries already *apply* the Clark–West test
  (`def:contango-backwardation-stocks`, `meth:fx-valuation-signals`) and *quote*
  Welch–Goyal and Campbell–Thompson results (`meth:backtest-evaluation-diagnostics`).
  None explains why nested forecast comparisons need special tests, or where
  valuation-ratio predictability comes from. The compendium uses a method it does
  not teach.
- *Sources in hand.* The two central empirical papers are local, and
  their key locators were checked for this plan (section 4). The two theory and
  test papers have open working-paper versions.
- *Checkable.* Each proposed claim can be checked by a short script: synthetic data
  for the test's size, public data for the published magnitudes.
- *Learning order.* `standard-errors-inference` comes earlier in the guide's
  specialist order, but it is not a prerequisite route of `return-predictability`.
  Without sources it would be an acquisition batch rather than a content batch.
  Stambaugh's predictive-regression bias belongs to that pathway and is deferred to
  it (section 8).

## 2. Learning outcome and scope boundary

**Outcome**, adapted from the guide's pathway outcome: judge an aggregate equity
return predictor by (a) the present-value logic that links valuation ratios to
expected returns and dividend growth, (b) out-of-sample tests that are valid for
nested models, and (c) the economic value of a restricted forecast to a
mean–variance investor.

**In scope**

- The aggregate U.S. equity premium, annual and monthly, with a single predictor
  or a small fixed set of them.
- Recursive (expanding-window) out-of-sample forecasts against the historical mean.
- Statistics: out-of-sample $R^2$, ΔRMSE, MSE-F, ENC and the Clark–West adjusted
  MSPE test, and why the standard Diebold–Mariano comparison is not valid for
  nested models.
- The Campbell–Shiller log-linear present-value identity and what it implies for
  the joint predictability of returns and dividend growth.
- Sign restrictions on coefficients and forecasts, and the certainty-equivalent gain
  with bounded weights.

**Out of scope for this batch** (deferred, section 8): cross-sectional predictability
and anomalies; predictive-regression bias and long-horizon inference; Giacomini–White
conditional tests; density forecasts and proper scoring rules; option-implied
premium bounds; forecast combination, unless an open copy of Rapach–Strauss–Zhou is
obtained (section 4); bond, currency and commodity predictability, which already
have their own entries; machine-learning predictors.

**Constraints**: no rewriting of existing entries to relocate or reclassify them; no
empty chapters or placeholder headings; no mastery or study claims. Coverage moves to
`covered` only under the coverage README's standard: a reviewed entry,
substantive sources with checked locators, review evidence and a worked example.

## 3. Existing material

### 3.1 Reuse (link, do not repeat)

| Label | File | Use in this batch |
| --- | --- | --- |
| `meth:forecast-accuracy-evaluation` | `regression-time-series/time-series-models.tex` | Chronological splits, benchmarks and RMSE; the new test entry starts where its *Conditions* field stops ("needs a formal comparison") |
| `meth:time-series-model-selection` | `regression-time-series/time-series-models.tex` | Out-of-sample confirmation in model choice |
| `meth:autoregressive-forecasting` | `regression-time-series/time-series-models.tex` | Persistent AR(1) predictors, as with the dividend–price ratio |
| `meth:backtest-evaluation-diagnostics` | `research-engineering-validation/backtest-evaluation.tex` | Already holds the Welch–Goyal Table 1 magnitudes (p. 1470) and Campbell–Thompson's restriction counts and $R^2/S^2$ rule. These stay where they are; the new entries link to them |
| `meth:correlation-independence-tests` | `probability-statistics/statistical-inference.tex` | Overlapping observations; the reason annual, non-overlapping forecasts are used first |
| `meth:hypothesis-testing` | `probability-statistics/statistical-inference.tex` | Size and power, needed for the Clark–West Monte Carlo |
| `mod:return-generating-models`, `mod:capm-sml` | `asset-pricing/asset-pricing-models.tex` | The expected-return concepts that a predictor is meant to track |
| `def:risk-aversion-utility`, `meth:capital-allocation-line` | `portfolio-construction-risk/portfolio-choice.tex` | Mean–variance utility and the optimal risky weight used in the economic-value calculation |

### 3.2 Entries that apply the methods (navigation only)

`def:contango-backwardation-stocks` (`energy-commodities/commodity-curves.tex`) and
`meth:fx-valuation-signals` (`currency-markets/macro-fx.tex`) report Clark–West
statistics from their own scripts. In this batch each gains, at most, a `\hyperref`
to the new test entry where the statistic is named. Their content is not changed.
The Clark–West function in
`notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py` is a reference
implementation to compare against, not a dependency.

## 4. Sources

Locators below were checked on 22 October 2026 against the copies named; anything
else is marked unchecked.

| Key | Source and copy | Availability | Verification status |
| --- | --- | --- | --- |
| `s7-welch` (catalogue) | Welch and Goyal, RFS 21(4), 2008; journal copy at `reading_materials/method-validation/src/WelchGoyal_2008_RFS.pdf` | Local | Previously checked: abstract p. 1455; Table 1 p. 1470 (evidence record of `meth:backtest-evaluation-diagnostics`). Checked for this plan, text layer: OOS $R^2$, adjusted $R^2$, ΔRMSE and MSE-F, eq. (6), p. 1461; ENC, eq. (7), and the statement that MSE-F and ENC have nonstandard distributions for nested models, so bootstrapped critical values are used, p. 1462; data sources incl. S&P 500 returns 1926–2005 from CRSP, p. 1457. Equations to be re-read as page images before citing |
| `campbell-thompson-2005-nber` (registered in `front/sources.tex`) | Campbell and Thompson, NBER WP 11468, June 2005; `reading_materials/empirical-extensions/src/Campbell_Thompson_NBER_w11468.pdf` and its text file | Local | Previously checked: Table 1 panels A–D, pp. 6–7; eqs. (8)–(9), pp. 9–10. Checked for this plan, text layer: the two restrictions (coefficient sign; non-negative fitted premium), printed pp. 2–3; $R^2_{OS}$, eq. (1), printed p. 6 (PDF p. 8); weights confined to 0–150 percent with risk aversion three, printed p. 10 (PDF p. 12); utility $E(R_p)-(\gamma/2)\mathrm{Var}(R_p)$ with $\gamma=3$, Table 2 notes (PDF p. 26). The RFS 2008 version (`wide-campbell-thompson`) is not held; cite the working paper |
| `wide-clark-west` (catalogue) | Clark and West, J. Econometrics 138(1), 2007 | Open working papers: NBER Technical WP 326, Aug 2006 ([nber.org/papers/t0326](https://www.nber.org/papers/t0326)); Kansas City Fed RWP 05-05, Nov 2005 | Located by web search on 22 October 2026; not downloaded or read. Register the WP version actually used in `front/sources.tex`; no locators yet |
| `wide-campbell-shiller-1988` (catalogue) | Campbell and Shiller, RFS 1(3), 1988 | Open working paper: NBER WP 2100, Dec 1986 ([nber.org/papers/w2100](https://www.nber.org/papers/w2100)) | Located; not read. The WP may differ from the journal version; record which is used. No locators yet |
| `wide-cochrane-dog` (catalogue) | Cochrane, RFS 21(4), 2008 | Not located in an open copy; an author-hosted version is likely | Unchecked. Optional: used only if obtained, for the joint return/dividend-growth argument |
| `wide-rapach-strauss-zhou` (catalogue) | Rapach, Strauss and Zhou, RFS 23(2), 2010 | No open copy found in one search | Unchecked. Forecast combination is deferred unless a copy is obtained |
| Predictor data | Amit Goyal's data page (sites.google.com/view/agoyal145) | Page reachable on 22 October 2026 (HTTP 200); it links to Google Sheets and Drive files | The predictor file has not been identified or downloaded. The current vintage extends past 2005, and revisions may move published numbers; record the file, date and hash |

## 5. Proposed entries (3 new; no material extensions)

All three go in one new topic file, `compendium/asset-pricing/return-predictability.tex`.
It is input once from `compendium/asset-pricing/section.tex` after
`asset-pricing-models`, under its own `\section{Return predictability and forecast
evaluation}`. This follows the guide's order: theory and factor models before
predictability. Labels are proposals.

1. **`res:campbell-shiller-identity`**. The log-linear present-value identity:
   $r_{t+1}\approx k+\rho\,pd_{t+1}-pd_t+\Delta d_{t+1}$, solved forward so that the
   log price–dividend ratio equals expected discounted future returns and dividend
   growth. Contents: what is exact and what is approximation; how $\rho$ follows from
   the mean ratio; and why a persistent valuation ratio must forecast returns,
   dividend growth or its own future value. Sources: Campbell–Shiller (WP); Cochrane
   only if obtained. Missing today: no entry states the identity.
2. **`meth:nested-forecast-tests`**. Out-of-sample comparison of a predictive
   regression with the historical mean. Contents: recursive design; $R^2_{OS}$ and
   ΔRMSE; why the larger model's MSPE is biased upward under the null (estimation
   noise); MSE-F and ENC with nonstandard distributions; the Clark–West adjustment
   and its approximately normal one-sided test; sensitivity to the start of the
   evaluation sample. Sources: Welch–Goyal; Clark–West (WP). Missing today: the
   statistic is used in two entries but explained nowhere.
3. **`meth:restricted-forecast-value`**. Sign-restricted forecasts and their
   economic value. Contents: the two Campbell–Thompson restrictions; the mean–variance
   weight $w_t=\hat\mu_t/(\gamma\hat\sigma^2_t)$ bounded to [0, 1.5]; average-utility
   (certainty-equivalent) gain against the historical-mean investor. It links to
   `meth:backtest-evaluation-diagnostics` for the published $R^2/S^2$ magnitude rather
   than restating it. Sources: Campbell–Thompson (WP). Missing today: the restriction
   method and the economic-value calculation itself.

Navigation-only edits, not counted as entries: *See also* links from
`meth:forecast-accuracy-evaluation` and `meth:backtest-evaluation-diagnostics` to
entries 2 and 3, and `\hyperref`s to entry 2 where the Clark–West statistic is named
in `def:contango-backwardation-stocks` and `meth:fx-valuation-signals`. These change
no claim.

## 6. Files, navigation and evidence

| Path | Change |
| --- | --- |
| `compendium/asset-pricing/return-predictability.tex` | New topic file with the three entries |
| `compendium/asset-pricing/section.tex` | One `\input` after `asset-pricing-models` |
| `compendium/front/sources.tex` | Register the working-paper versions actually read (Clark–West, Campbell–Shiller) unless the catalogue keys' versions are used |
| `notes/pathways/return-predictability.md` | New specialist pathway note (guide key), listing the three entries and an entry backlog for the deferred readings |
| `notes/pathways/asset-pricing.md` | Its entries list gains the new file; the pathway line points to the new note |
| `notes/entry-evidence.json` | One record per new entry: sources and locators, verification state, stability *draft* |
| `notes/coverage/objectives.json` | New `topic:return-predictability` (section `asset-pricing`; prerequisites `topic:time-series-models`, `topic:asset-pricing-factor-models`) with three objectives (proposed IDs `objective:interpret-present-value-identity`, `objective:test-nested-return-forecasts`, `objective:value-restricted-return-forecasts`). They start `missing` and move to `covered` only after review |
| `notes/coverage/learning-roadmap.md` | The new topic placed after the factor-model topic |
| `notes/readings/` | Reading notes for the Clark–West and Campbell–Shiller copies used; `s7-welch.md` gains this pathway in `pathways` |
| `notes/source-review-records.md` | One dated section recording what was read, checked and left unread |
| `notes/artefacts/return-predictability/` | The check script and its recorded output (section 7) |

The migration ledger is not edited; the pathway's change from Partial to Note is
recorded in this batch's review record.

## 7. Numerical checks

Only these checks, one script
(`notes/artefacts/return-predictability/return-predictability-checks.py`), runnable
under `make examples`. Thresholds are fixed in the script before its first run.

1. **Clark–West size (entry 2).** Monte Carlo of a nested null (true slope zero,
   persistent AR(1) predictor, recursive forecasts). Show that the unadjusted MSPE
   difference favours the historical mean on average, and that the Clark–West
   one-sided test at nominal 10 percent rejects within a stated band, while the naive
   normal comparison is undersized. Synthetic data; no download.
2. **Identity accuracy (entry 1).** On the annual predictor data, compute $\rho$ from
   the mean log dividend–price ratio. Report the standard deviation of the
   approximation residual relative to that of log returns. If the data file cannot be
   obtained, the entry states the identity without an empirical accuracy figure.
3. **Published magnitude (entry 2).** Reproduce Welch–Goyal's annual
   dividend–price-ratio row (forecasts from twenty years into the sample, data through
   2005), with $R^2_{OS}$, MSE-F and the Clark–West statistic. Compare with Table 1 to
   a stated tolerance. A data-vintage mismatch is reported as such, not tuned away.
4. **Economic value (entry 3).** Monthly certainty-equivalent gain for $\gamma=3$ with
   weights in [0, 1.5], historical mean against restricted forecasts, for one
   predictor. Compare the sign and order of magnitude with Campbell–Thompson's Table 2
   only if that table is re-read as a page image first.

## 8. Acceptance criteria and deferred topics

### 8.1 Acceptance

- Three entries exist in `asset-pricing/return-predictability.tex`, each with a
  title, label and Statement, and citations whose locators were checked against the
  copy named in its evidence record. No claim relies on an unread source.
- Entry 2 explains, in its own words, the nested-model MSPE bias and the Clark–West
  adjustment. Check 1 passes against its pre-registered band.
- Entry 1's identity and Entry 3's utility gain each have a worked example reproduced
  by the script. A failed or unobtainable data check is recorded as such in the
  entry's *Conditions* and the review record.
- No existing entry's content changes beyond the navigation links in section 5; all
  697 earlier labels, their types and bodies are unchanged except for those links.
- `make check` and `make pre-commit` pass; the PDF shows the new section after
  *Systematic risk, the CAPM and factor models* with no new overfull boxes or
  unresolved references.
- Coverage is honest: an objective moves to `covered` only with reviewed evidence,
  otherwise it stays `missing` or `partial` with the gap stated. Nothing is recorded
  in `notes/log.md`, and no mastery is claimed.

### 8.2 Deferred

- `standard-errors-inference`, including Stambaugh's predictive-regression bias and
  Hodrick's long-horizon inference: the recommended next batch once its sources are
  obtained.
- Forecast combination (Rapach–Strauss–Zhou), Giacomini–White conditional tests,
  proper scoring rules (Gneiting–Raftery), the SVIX bound (Martin), the updated 2024
  Goyal–Welch–Zafirov study and the real-time kernel check: later
  `return-predictability` increments.
- `event-studies`, after `standard-errors-inference`.
- `trend-following` signal design and managed-futures evidence.

### 8.3 Batch size

The saved preference for content batches is 45 newly covered objectives. This plan
deliberately proposes three objectives, as the review request limited the batch to
3–6 entries. Confirm which limit governs before implementation.
