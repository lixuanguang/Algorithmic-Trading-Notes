# Content development plan: return predictability and forecast evaluation

Status: implemented 22 October 2026 on branch `codex/return-predictability-content` from `2ebe829`, then audited and
corrected the same day (section 7.1), then committed for review and merged through a pull request. Three new entries, one new pathway section, one new topic with four objectives (three covered, one missing),
one numerical artefact folder. Owner: repository maintainer.

The proposal was recorded on 22 October 2026 (commit `87faaa0`) against guide pin
`6c7734ed49f1c242908b86a57c4f5d1f0e349ec0` and deferred until the compendium's sections were aligned with the guide's
specialist pathways. That alignment is complete (`f73859c`, merged in `2ebe829`; record in
[subsection_alignment_plan.md](subsection_alignment_plan.md)). The completed content migration (`53e2b1c`; records in
[content_migration_plan.md](content_migration_plan.md) and [content_migration_ledger.md](content_migration_ledger.md))
and the alignment record are kept as historical evidence and are not edited by this batch.

Guide pin now: `8302467bc5acfedba55c7e79b311cfb2154f433c` (227 pathways). Before this batch: 697 entries, 111 printed
pathways, 461 PDF pages. After it: 700 entries, 112 printed pathways, 464 PDF pages.

## 0. Reconciliation before implementation (22 October 2026)

| Item in the deferred proposal | Current repository | Decision |
| --- | --- | --- |
| Guide pin `6c7734e` | Pin `8302467`; `return-predictability` unchanged in name, outcome, prerequisites and required readings; `asset-pricing` specialist order `asset-pricing-theory`, `standard-errors-inference`, `empirical-asset-pricing`, `return-predictability`, `event-studies` | Use `8302467` |
| New file input "after `asset-pricing-models`" under a bare `\section{Return predictability and forecast evaluation}` | Wrappers open each pathway with `\qfpathway{key}{Name}`; bare peer `\section` headings are refused by the checker; `asset-pricing` prints `asset-pricing-theory` and `empirical-asset-pricing` | `\qfpathway{return-predictability}{Return predictability and forecast evaluation}` after `empirical-asset-pricing` (the guide's order; `standard-errors-inference` has no entries and is not printed); one topic file, so no `\subsection` heading |
| Reused entries' files and sections (section 3) | Same files; owning pathways now `stationarity-cointegration` (time-series models), `backtest-inference`, `equity-events-fundamentals` (Gordon model), `portfolio-construction`, `probability-statistical-inference` | Cross-reference; no content moved |
| Batch size question (8.3) | The request of 22 October 2026 sets the limit at three new entries and excludes a general coverage campaign | Three entries; the saved 45-objective preference does not govern this batch |
| Source statuses (section 4) | Inherited "checked" statuses were not relied on | Every locator re-read for this batch; section 4 records what was read |

## 1. Choice of batch

### 1.1 Candidates

Three small batches were ranked on five criteria: position in the guide's learning
order, readiness of prerequisites, source availability, how much existing material
can be extended rather than rewritten, and whether the claims can be checked
numerically from public data.

| Rank | Pathway (section) | Ledger state | Order and prerequisites | Sources | Numerical validation | Verdict |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `return-predictability` (`asset-pricing`, Part II) | Partial | Fourth of five in the asset-pricing specialist order. Guide prerequisites `time-series-volatility` (Note) and `empirical-asset-pricing` (Related, `asset-pricing/asset-pricing-models`) both have material | Welch–Goyal 2008 and Campbell–Thompson (NBER WP) are local; open working papers exist for Clark–West and Campbell–Shiller | Public annual and monthly predictor data on Goyal's site; synthetic Monte Carlo for test size | **Chosen** |
| 2 | `standard-errors-inference` (`asset-pricing`) | Partial | Second in the specialist order; a prerequisite of `event-studies` | None of its 16 required readings is on disk; open copies would have to be found for each | The checkpoint needs a licensed firm-month panel (CRSP) and a published IV replication; only simulation is possible without them | Next, once sources are obtained |
| 3 | `trend-following` (`multi-asset-systematic-macro`, Part III) | Partial | Later Part; prerequisites present | Moskowitz–Ooi–Pedersen and Hurst–Ooi–Pedersen are local and already cited | The checkpoint needs 40 continuous futures series, which are not public | Defer; the core evidence already sits in `def:alpha-model-taxonomy` |

### 1.2 Rationale

- *Clear unmet need.* Existing entries applied the Clark–West test
  (`def:contango-backwardation-stocks`, `meth:fx-valuation-signals`) and quoted
  Welch–Goyal and Campbell–Thompson results (`meth:backtest-evaluation-diagnostics`), but
  none explained why nested forecast comparisons need special tests, or where
  valuation-ratio predictability comes from.
- *Sources in hand or openly available*, and every claim checkable by a short script.
- *Learning order.* `standard-errors-inference` comes earlier in the guide's specialist
  order but is not a prerequisite route of `return-predictability`; without sources it
  would be an acquisition batch. Stambaugh's predictive-regression bias belongs to it.

## 2. Learning outcome and scope boundary

**Outcome**, adapted from the guide's pathway outcome: judge an aggregate equity
return predictor by (a) the present-value logic that links valuation ratios to
expected returns and dividend growth, (b) out-of-sample tests that are valid for
nested models, and (c) the economic value of a restricted forecast to a
mean–variance investor. The guide's outcome also names proper scoring; that part is
not covered (recorded as `objective:score-and-combine-return-forecasts`, missing).

**In scope**: the aggregate U.S. equity premium, annual and monthly, with one predictor
(the dividend–price ratio); recursive out-of-sample forecasts against the historical
mean; $R^2_{OS}$, ΔRMSE, MSE-F, ENC and the Clark–West test; the Campbell–Shiller
identity and its coefficient restriction; sign restrictions and the certainty-equivalent
gain with bounded weights.

**Out of scope** (section 8.2): cross-sectional predictability; predictive-regression
bias and long-horizon inference; Giacomini–White conditional tests; density forecasts
and proper scoring rules; option-implied premium bounds; forecast combination; other
asset classes; machine-learning predictors.

## 3. Existing material

### 3.1 Reused through cross-references (not repeated)

| Label | File (owning pathway) | Use |
| --- | --- | --- |
| `meth:forecast-accuracy-evaluation` | `regression-time-series/time-series-models.tex` (`stationarity-cointegration`) | Chronological splits and benchmarks; the new test entry starts where its Conditions stop ("needs a formal comparison") |
| `meth:autoregressive-forecasting` | same | Persistence $\phi$ of the dividend yield |
| `meth:backtest-evaluation-diagnostics` | `research-engineering-validation/backtest-evaluation.tex` (`backtest-inference`) | Keeps Welch–Goyal's Table 1 magnitudes and Campbell–Thompson's restriction counts and $R^2/S^2$ rule; linked, not restated |
| `meth:gordon-growth-model` | `systematic-equities/dividend-discount-models.tex` (`equity-events-fundamentals`) | The constant-growth special case of the identity |
| `meth:correlation-independence-tests`, `meth:hypothesis-testing` | `probability-statistics/statistical-inference.tex` (`probability-statistical-inference`) | Overlapping observations; size and power |
| `def:risk-aversion-utility`, `meth:capital-allocation-line` | `portfolio-construction-risk/portfolio-choice.tex` (`portfolio-construction`) | Mean–variance utility and the optimal risky share |

### 3.2 Navigation-only edits to existing entries (no claim changed)

- `def:contango-backwardation-stocks` (`energy-commodities/commodity-curves.tex`): the first
  "Clark--West" in its WTI result links to `meth:nested-forecast-tests`.
- `meth:fx-valuation-signals` (`currency-markets/macro-fx.tex`): the same, at its first
  Clark–West statistic.
- `meth:forecast-accuracy-evaluation`: See also gains `meth:nested-forecast-tests`.
- `meth:backtest-evaluation-diagnostics`: See also gains `meth:nested-forecast-tests` and
  `meth:restricted-forecast-value`.

The Clark–West function in `notes/artefacts/fx-determination-forecasting/fx_ppp_oos_test.py`
was not used; the new script computes the statistic independently.

## 4. Sources (verified for this batch, 22 October 2026)

Every locator cited by the new entries was read in the copy named here, equations and tables as page images. Nothing
was taken over from the proposal's or earlier records' "checked" statuses. Downloads were saved under the git-ignored
`reading_materials/return-predictability/` with a download log (URL, time, HTTP status, size, SHA-256).

| Key used | Version read | Copy | Notes |
| --- | --- | --- | --- |
| `campbell-shiller-1986-nber` (registered) | NBER WP 2100, December 1986 | nber.org PDF, scanned, SHA-256 `1786a383…c4f7`; printed page = PDF page − 2 | The journal version (`wide-campbell-shiller-1988`, RFS 1988) was not obtained. The WP linearises the present-value model around constant $r$ and $g$, with $\rho=\exp(-(r-g))$ and $\delta_t=d_{t-1}-p_t$, which differs in notation from the 1988 form; the entry cites the WP for that and Cochrane for the 1988 form. Its point is $r=\log(1+\bar R)$ of real returns (p. 5), re-read in the audit |
| `clark-west-2006-nber` (registered) | NBER Technical WP 326, August 2006 | nber.org PDF, SHA-256 `69d6c6c9…0362`; printed page = PDF page − 2 | The journal version (`wide-clark-west`, J. Econometrics 2007) was not obtained; the Kansas City Fed RWP 05-05 was not used. Tables sit on unnumbered pages; the empirical table is printed "Table 4" but called Table 7 in the text |
| `wide-cochrane-dog` (catalogue) | Published RFS 21(4) article | Author-hosted copy (johnhcochrane.com), SHA-256 `983fc45e…f848`; PDF page = printed page − 1532 | Obtained in this batch (the proposal had it unlocated) |
| `s7-welch` (catalogue) | Published RFS 21(4) article | Existing local journal copy, SHA-256 `57ad3636…5b7b`; PDF page = printed page − 1454 | Eqs. (6)–(7), pp. 1461–1462, and Table 1, p. 1470, re-read as page images. The adjusted-$R^2$ formula printed with eq. (6) cannot produce Table 1's values and is treated as a misprint |
| `campbell-thompson-2005-nber` (registered) | NBER WP 11468, June 2005 | Existing local copy, SHA-256 `bba16755…c5e4`; printed page = PDF page − 2 | Re-read: pp. 2–3, 6, 9–10 and Table 2 (PDF p. 26). The RFS 2008 version (`wide-campbell-thompson`) was not obtained; locators are the WP's |
| Predictor data | Goyal's page, workbook labelled "Original data (up to 2005) used in the paper", Drive id `1qwpl2R_DNujpU5YUkk8lacP1tTeMb9iJ` | SHA-256 `8d210b77…be872`, retrieved 2026-10-22 | Despite the label it runs to December 2025: a 2026 vintage. No 2005 vintage was available, so differences from the 2008 tables cannot be separated from data revisions. The second workbook (data to 2025 in the newer layout, SHA-256 `be74347c…e480`) was downloaded but not used |
| `wide-rapach-strauss-zhou`, `wide-goyal-welch-zafirov`, `wide-giacomini-white`, `wide-gneiting-raftery`, `wide-martin-svix`, `w3-cakici-pockets-replication` | — | — | Not obtained or read; nothing is taught from them |

## 5. Entries (3 new)

All three are in `compendium/asset-pricing/return-predictability.tex`, input once from
`compendium/asset-pricing/section.tex` after `\qfpathway{return-predictability}{Return predictability and forecast
evaluation}`, which follows `empirical-asset-pricing`. The file is the pathway's only topic file and has no heading of
its own. In the PDF the pathway is section 8.3 (printed pp. 35–38).

1. `res:campbell-shiller-identity` (Result 8.8): exact and log-linear identities, the two choices of $\rho$, the
   forward solution with its terminal term, $b_r=1-\rho\phi+b_d$ and the long-run decomposition; S&P 500 worked example.
2. `meth:nested-forecast-tests` (Method 8.9): recursive design, $R^2_{OS}$ and ΔRMSE, MSE-F and ENC, the nested-model
   MSPE bias, the Clark–West test and what it tests; Monte Carlo size and power, Welch–Goyal's d/p row, start-date
   sensitivity, Clark–West's own example.
3. `meth:restricted-forecast-value` (Method 8.10): the two restrictions, the bounded mean–variance weight, realised
   utility and its fee reading; hand example, Campbell–Thompson's d/p row, a synthetic experiment. The real-time
   problem of choosing the expected sign from the full sample is stated in Conditions.

## 6. Files

| Path | Change |
| --- | --- |
| `compendium/asset-pricing/return-predictability.tex` | New topic file, three entries |
| `compendium/asset-pricing/section.tex` | `\qfpathway` line and one `\input` |
| `compendium/front/sources.tex` | `campbell-shiller-1986-nber`, `clark-west-2006-nber` registered |
| Four existing topic files | Navigation links only (section 3.2) |
| `notes/pathways/return-predictability.md` | New specialist pathway note with entry backlog |
| `notes/pathways/asset-pricing.md` | Entries list and pathway status |
| `notes/entry-evidence.json` | Three records |
| `notes/coverage/objectives.json` | `topic:return-predictability` and four objectives |
| `notes/coverage/learning-roadmap.md` | The topic in group 2 after `topic:time-series-models` |
| `notes/readings/` | New notes for `campbell-shiller-1986-nber`, `clark-west-2006-nber`, `wide-cochrane-dog`, `campbell-thompson-2005-nber`; `s7-welch.md` extended |
| `notes/source-review-records.md`, `notes/source-review-index.md` | Batch record and index line |
| `notes/artefacts/return-predictability/` | Protocol, extraction script, derived CSVs, check script, recorded output; `superseded-first-run/` keeps the pre-audit script, output and protocol |
| `README.md`, `compendium/README.md` | Where the mapping of later entries is recorded |

## 7. Numerical checks

`notes/artefacts/return-predictability/return-predictability-checks.py`, run by `make examples`; definitions, timing and
tolerances in `return-predictability-protocol.md`, written before the first run (not blind to the published tables;
not a preregistration). 47 checks pass after the audit (39 before it); output in `return-predictability-results.txt`.

- **Identity.** With a return built from `Index` and `D12` in every year, the exact identity holds to $2\times10^{-15}$
  for 1872–2025; the CRSP return differs by up to 0.0675 in log (1931) and is reported separately. The approximation
  error is the Taylor remainder, non-negative and below $(pd-\overline{pd})^2/8$. Nominal variance ratios 0.00021
  (1872–1986) and 0.00077 (1872–2025) at the mean-$pd$ point; 0.00089 and 0.00728 at the working-paper point
  ($\rho$ 0.9348 and 0.9364). An illustration, not a reproduction of Campbell–Shiller's 0.0008 for PPI-deflated
  returns. Forward iteration exact; $b_r-b_d+\rho\phi=1+b_\varepsilon$ to $10^{-10}$ ($b_r$ 0.066, $b_\varepsilon$
  $-0.0029$ for 1927–2004).
- **Clark–West size.** DGP 1, recursive, $R=120$, 5,000 replications, seed 20261022: 0.069 and 0.059 for $P=120, 240$
  against the published 0.085 and 0.070. Inside the pre-set tolerance (0.02) but 3.0 and 2.3 standard errors below,
  counting both simulations. Unadjusted test 0.023 and 0.010 (published 0.028 and 0.012). The audit's rerun in the
  source's design (seed 20261104, 20,000 replications) reproduces the quoted rolling means and leaves a gap only at
  $P=120$ (0.072 against 0.085 in both schemes, about three standard errors): unresolved.
- **Welch–Goyal d/p row.** ΔRMSE −0.13 against −0.11 (from 1892) and −0.09 (from 1965); in-sample adjusted $R^2$ 0.32
  against 0.49. Within tolerances; the gaps are consistent with, but not shown to come from, the 2026 data vintage.
- **Campbell–Thompson d/p row.** Utility 0.492 against 0.501 percent a month; changes −0.018 and −0.024 against
  −0.016 and −0.024; restricted $R^2_{OS}$ 0.003 against 0.001 percent.
- **Synthetic economic value.** The pre-set design (C4) used DGP 1's mean, which puts the weight at the 1.5 cap in
  98–100 percent of months; this protocol flaw is recorded, and a post-run supplement (C5, outside any verdict) lowers
  the mean to 0.5 percent a month.

### 7.1 Audit corrections (22 October 2026)

An audit of the uncommitted batch found that the script computed the working paper's $\rho$ from the mean log return
(the paper, p. 5, uses $\log(1+\bar R)$), and that part A mixed CRSP returns from 1926 into the identity, so the
exact identity was checked only for 1872–1925 (a restriction the protocol did not record) and the reported
approximation error included the mismatch between the two return series. Both were corrected and checks were added
that fail on either error. The Clark–West entry regained the source's asymptotic regime, one-step homoskedastic
setting and exceptions, and two locators moved ((4.1) to p. 8, (4.2) to p. 9). The first run is kept in
`notes/artefacts/return-predictability/superseded-first-run/`; the protocol's *Audit corrections* section and the
review record give the details. Parts B and C, their seeds, specifications and tolerances are unchanged, and the
third entry needed no change.

## 8. Acceptance and deferred topics

### 8.1 Acceptance (outcome)

- Three entries with title, label, Statement and located citations, each checked against the copy named in its
  evidence record: met.
- Entry 2 explains the MSPE bias and the adjustment in its own words; check 1 passed its pre-set band: met.
- Worked examples for entries 1 and 3 reproduced by the script; data limits stated in the entries' Conditions: met.
- The 697 earlier labels, types and bodies unchanged apart from the four navigation edits: met (section 9).
- `make check` and `make pre-commit` pass; the new section follows *Empirical asset pricing: factor models and tests*
  as 8.3; no new overfull boxes or unresolved references: met.
- Coverage: three objectives covered at analysis depth with reviewed evidence; the pathway's combination and scoring
  outcome recorded as a missing objective; pathway checkpoint not attempted; nothing in `notes/log.md`; no mastery
  claimed.

### 8.2 Deferred

- `standard-errors-inference`, including Stambaugh's predictive-regression bias and Hodrick's long-horizon inference.
- Within `return-predictability`: forecast combination (Rapach–Strauss–Zhou), Giacomini–White conditional tests,
  proper scoring rules (Gneiting–Raftery), the SVIX bound (Martin), the Goyal–Welch–Zafirov update, the real-time
  kernel check and the checkpoint replication with five predictors.
- The cause of the lower Clark–West size at $P=120$, unresolved after a bounded investigation (section 7).
- `event-studies`; `trend-following`.

## 9. Validation

Recorded in `notes/source-review-records.md`, *Return-predictability content batch (22 October 2026)*.
