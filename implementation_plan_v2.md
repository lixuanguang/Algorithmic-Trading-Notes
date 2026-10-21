# Compendium gap-filling from the owner's finance library: implementation plan v2

**Current status (2026-10-21, after Batch L6).** On `codex/library-gap-batch-l6`, created from `af47d03` (L5). Two L5
clarifications (Section 7) and **Batch L6** (C1-D1 country risk premium, C1-D2 concentrated positions; depth only):
`meth:cost-of-debt-equity-estimation`, `meth:complex-client-situations` and `meth:covered-call-protective-put`
extended, two deterministic check scripts (three first-run failures, all harness or hand-value errors, recorded), new
source keys for Rev. Rul. 2003-7 and Treas. Reg. 1.351-1. **449/449 objectives, 1,030/1,030 items** (unchanged). Record:
`notes/source-review-records.md`, *Library gap-filling, Batch L6, 21 October 2026*. Local commits only.

Status after Batch L5 (kept for the record):
**Status (2026-10-21, after Batch L5).** On `codex/library-gap-batch-l5`, created from `main` at `c26a09e`
(the PR #33 merge; second parent and tree identical to the expected `d71e127`; clean tree; 447/447 objectives,
1,030/1,030 items). Two pre-L5 audit corrections (C1-F1, the Monte Carlo Greeks resimulation-bias sentence; C1-F2, the
C1 depth-extension classification) and **Batch L5 frozen and implemented** (L5-D1 to L5-D3; Section 7, "Pre-L5 audit
corrections" and "Batch L5 freeze and frozen specification"): `meth:lookback-option-valuation`,
`meth:transaction-cost-hedging`, two check scripts and records; **449/449 objectives, 1,030/1,030 items**; shortfall 43
against 45, without padding. One harness correction in the lookback script after its first run (recorded). Record:
`notes/source-review-records.md`, *Library gap-filling, Batch L5, 21 October 2026*. Local commits only; no push, PR,
merge, rebase or amendment. Human review of L1-L5 outstanding.

Status after the C1 pass (kept for the record; its depth-extension count is corrected by C1-F2):
**Status (2026-10-21, after the C1 pass).** On `codex/library-gap-c1-inventory`, created from `e6c22e6`
(clean tree; 447/447 objectives, 1,030/1,030 items): three L4 corrections (L4-F1 to L4-F3, Section 7, "C1 pass: L4
corrections"), the C1 gap inventory (Section 8.2: 97 remaining modules reconciled and compared; 2 confirmed distinct
candidate objectives, 4 depth extensions (corrected by C1-F2: not all source-supported), 2 possibly distinct but unresolved; provisional 449 for this corpus),
and **Batch L5 proposed, not frozen or implemented** (lookback options and hedging with transaction costs, +2;
decisions in Section 10.5). Objectives unchanged at 447/447. One local commit; no push, PR, merge, rebase or amendment.

Status after Batch L4 (kept for the record):
**Status (2026-10-21, after Batch L4).** Batch L4 (B3, B12, B13) was frozen by the owner (L4-D1 all three
packages, L4-D2 the seasoned variance-swap value as a labelled derivation, L4-D3 no separate B13 objective) with three
specification corrections (L4-C1 to L4-C3, Section 7, "Batch L4 freeze corrections and frozen specification") and
implemented on `codex/library-gap-batch-l4`, created from `95c547a`. Delivered: `meth:monte-carlo-greeks`,
`meth:cross-currency-basis-swaps`, the seasoned-swap extension of `meth:volatility-derivative-applications`, three
check scripts (all pass on their first runs with the frozen seeds and tolerances; one mistyped expected literal was
then corrected and its tolerance tightened, see the record), records, and one new objective:
447/447 objectives, 1,030/1,030 items; shortfall 44 against 45, without padding. Record:
`notes/source-review-records.md`, *Library gap-filling, Batch L4, 21 October 2026*. One local commit; no push, PR, merge,
rebase or amendment. Human review of L1-L4 outstanding.

Status after the L4 proposal (kept for the record):
**Status (2026-10-21, L4 proposal).** On `codex/library-gap-l4-proposal`, created from `517213d` (parent
`440272b`; clean tree; 446/446 objectives, 1,030/1,030 items), one L3 wording correction was made: the CSRD first wave
in `meth:esg-exposure-evaluation` now includes public-interest parents of large groups (Section 7, "L3 wording
correction"). **Batch L4 (B3, B12, B13) is proposed and awaiting the owner's freeze (Section 7, "Proposed Batch L4";
decisions in Section 10.4). Nothing in it has been implemented**: no teaching entry, script or coverage claim. Expected
new objectives: 1 (shortfall 44 against 45). Local commit only; no push, PR, merge, rebase or amendment.

Status after Batch L3 (kept for the record):
**Current status (2026-10-21, after Batch L3).** Batch L3 (P10, regulatory and disclosure currency; backlog B7) was
frozen and executed on `codex/library-gap-batch-l3`, branched from `a519e0c`; committed locally, not pushed, no PR.
FRTB, liquidity and sustainability-disclosure statements were verified against the issuers' texts and corrected with
EU, UK and US status; one new entry, `rule:counterparty-credit-cva-capital`, and one new objective (446/446 objectives,
1,030/1,030 items; shortfall 44 against 45). Record: `notes/source-review-records.md`, *Library gap-filling, Batch L3,
21 October 2026*. Unverified: the FCA's PS26/19 and Eighth Circuit orders after May 2026. Human review outstanding.
**Correction pass (2026-10-21).** An audit of `440272b` found five statements the checks did not test (L3-F1 to L3-F5:
the SA-CCR maturity-factor floor, the units of the BA-CVA exposure proxy, Directive 2026/470 scope and timing, US NSFR
applicability, and the scope of the EU 0.9 multiplier). They were corrected in a separate local commit on
`codex/library-gap-l3-audit-fixes`, with two deterministic checks; PS26/19 and the Eighth Circuit orders of 21 May and
5 October 2026 were then read. See "Batch L3 post-implementation audit corrections" in Section 7. Objectives (446/446)
and items (1,030/1,030) unchanged. Not done: push, PR, any backlog batch.

Status after Batch L2 (kept for the record):
Batch L2 was frozen by the owner (decisions L2-D0 to L2-D6, Section
10.3, with the two freeze corrections in Section 7) and implemented on `codex/library-gap-batch-l2`, branched from
`c688d54`; committed locally, not pushed, no PR. All packages (P6-P9, P11a-c, the L2-D3 tree extension and the L2-D5
Hull extensions) are complete; P10 is deferred to Batch L3. Eleven new objectives: 445/445 objectives and 1,030/1,030
outline items, editorial coverage only; shortfall 34 against 45. Every frozen criterion passed. Record:
`notes/source-review-records.md`, *Library gap-filling, Batch L2, 21 October 2026*. Human review outstanding.
**Correction pass (2026-10-21).** An audit of `cd55096` found four defects that the passing checks did not test
(L2-F1 to L2-F4: the Hull-White discount sign in the P7 script, the discounting convention of the wrong-way CVA
equation, the units of EPE times spread, and the scope of Regulation T's 150 percent). They were corrected in a separate
local commit after `cd55096`, with deterministic checks for the first and third; see "Batch L2 post-implementation
audit corrections" in Section 7. Scope, objectives (445/445) and items (1,030/1,030) unchanged. Not done: push, PR, L3.

Status after the L2 proposal audit (kept for the record):  Batch L1 and its five audit
repairs are committed locally as `5e0578e` on `codex/library-gap-batch-l1` (parent `2b89791`;
not pushed, no PR). That commit holds this file at its audited pre-C0 state (SHA-256
`afb74d11…8e14`). The C0 revision and the audit corrections to the Batch L2 proposal are
committed separately after it. The corrections are marked "Corrected (L2 audit)" in Section 7
and listed under "Batch L2 proposal audit corrections". **Batch L2 is awaiting the owner's
freeze (Section 10.3); nothing in it has been implemented.**

Status after discovery task C0 (kept for the record): Batch L1 (Section 6) and its five
audit repairs are implemented but not committed, on branch `codex/library-gap-batch-l1` at
`2b89791`. A later read-only audit found no new actionable L1 defect: the six L1 scripts passed
with warnings as errors; 36 tests, lint, formatting and the structural checks passed. Coverage is
434/434 objectives and 1,030/1,030 outline items. That coverage is editorial; human review of the
L1 entries is outstanding. C0 is complete (Section 8.1). Batch L2 is a proposal (Section 7) and
is not frozen; it needs the owner decisions in Section 10.3. The C0 revision changed only this
file. The status paragraphs below and the baselines in them are kept as the record of earlier
revisions.

Status at first writing: plan only. Written 2026-10-21 (Asia/Singapore) and revised the same day after a
read-only audit of the first draft. No compendium, notes, coverage, artefact or library file has
been changed. `implementation_plan.readme` stays the historical record of Batches 0-6 and
Sections 7-36; adding its pointer section is part of Batch L1, not of this revision.

Second revision, 2026-10-21, before Batch L1 execution: the external audit's findings R1-R4
were applied (P7's wrong-way-risk sign, P5's discrete-rebalancing criterion, explicit P2-P3
example conventions, and the count of existing entries touched). The owner approved E1 and E2.

Correction after execution, 2026-10-21: an audit of the implemented Batch L1 (findings L1-F1 to
L1-F5) found mathematical assumptions that the checks did not cover. The owner authorised the
necessary changes to the affected example specifications and acceptance criteria. They are
marked "Corrected (L1 audit)" in P3-P5 below (P1's fix is a wording change in the entry only), with the reasons, and listed under
"Batch L1 post-implementation audit corrections" after the acceptance conditions. The
original wording is kept there for the record.

Repository baseline, rechecked for this revision: branch `codex/alternatives-audit-20261020` at
`2b89791`; the only working-tree change is this untracked file; draft PR #33 to `main` is open
with the same head (`gh pr view 33`, 2026-10-21). Coverage: 424/424 objectives and 1,030/1,030
outline items, all `covered` (editorial coverage only).

## 1. Purpose and scope

v1 used eight CFA topic outlines (2026 and 2027) to define scope and cited no curriculum
volume or workbook. That scope is fully mapped. v2 asks a different question: **what does the
owner's library teach that the compendium does not explain, explains too thinly, or states in
an out-of-date form?** The aim is general finance reference coverage, not exam preparation.

Library: `/Users/lxg/Documents/CFA & Finance/Exam` (576 files). It is read-only; nothing in it
is moved, renamed, annotated or copied into the repository.

The deliverable is the existing compendium, extended in place and rebuilt: no supplement
folder, no standalone notes, no second book and no new chapter.

Execution is bounded. Section 6 freezes **Batch L1**, the only batch this plan authorises once
the decisions in Section 10.1 are made. Everything else is either a proposed later batch whose
scope is frozen only after the bounded discovery task C0 (Section 7), or a backlog item
(Section 8) that needs evidence before it can be scheduled. C0 has now run. Batch L2 is still
not authorised; the owner freezes it with the decisions in Section 10.3.

## 2. Ground rules carried over

- Entry types and label prefixes follow `tools/check_compendium.py` (`PREFIX`): `def:`, `conv:`,
  `res:` (environment `qfresult`), `mod:`, `meth:`, `mech:`, `ev:`, `data:`, `rule:`, `pit:`,
  `ex:`. Slugs are lower-case letters, digits and hyphens. One idea per entry; Statement
  first, then Conditions, Notation, Practice, Pitfalls, See also and Further reading as
  relevant; about 80-140 words per paragraph; no Status blocks, editing diaries or keyword
  lists in the PDF (`compendium/README.md`).
- `\citep[locator]{key}` only for sources actually read. Catalogue keys come from `guide/`;
  other sources are registered in `compendium/front/sources.tex` in key order with edition,
  ISBN or URL, page offset and reading or retrieval date. A relevant source that was not read
  appears only under Further reading as `\nolinkurl{key}`, as existing entries do.
- Provenance in `notes/entry-evidence.json` and `notes/source-review-records.md`; reading notes
  in `notes/readings/`; pathway notes in `notes/pathways/`; numerical checks in
  `notes/artefacts/<area>/*check*.py`, run by `make examples` (numpy and scipy only; no new
  dependency).
- Explanations are written from the sources, not copied. Worked examples are original and
  labelled illustrative unless they reproduce a published example, which is then cited with its
  table or example number.
- Changing standards and market practice are verified against the issuer's current text, with
  effective dates, jurisdiction and "as of" dates in the entry's Conditions.
- Reuse first: extend an existing entry when the gap is depth within its idea; add an entry
  only for a new idea; add a topic file only when a chapter lacks a home for a group of
  entries.
- **Citation policy (unchanged from v1).** CFA curriculum volumes, CFA workbooks, Schweser,
  Wiley guides, formula sheets, question banks and 300Hours tests are not cited. They may be
  used to find gaps and to cross-check. CQF lecture packs are also cross-checks only. Batch L1
  needs no exception. Any later exception (expected only for the CAIA texts in backlog item
  B6) is proposed with the batch that needs it, not assumed here.
- Batch size: the standing preference of `implementation_plan.readme` Section 17.4 is 45
  newly covered objectives per content-expansion prompt, with no padding, and an honest
  shortfall reported with reasons. This plan does not change that preference; Section 10.1
  states the shortfall that Batch L1 would carry.

## 3. Evidence behind this plan

### 3.1 Compendium entries read

The draft's topic searches counted keyword hits. This revision read the matching entries and
reclassified each topic by what those entries actually teach.

| Topic | Existing teaching (label) | Remaining gap |
| --- | --- | --- |
| Monte Carlo pricing | `meth:monte-carlo-simulation` (`common-toolkit/simulation-methods.tex`): discounted-payoff valuation, standard error, 95% interval, seeds, square-root rule, antithetic reduction named; check in `notes/artefacts/inference-simulation/inference-simulation-checks.py` | **Depth**: control variates with an estimated coefficient; discretisation bias against sampling error; early exercise by regression (Longstaff-Schwartz), which is a **new idea** |
| Delta hedging at implied against realised volatility | `meth:greeks-delta-gamma-hedging` gives the local P&L $\tfrac12\Gamma S^2(\sigma_r^2-\sigma_i^2)\Delta t$; `meth:active-currency-strategies` repeats it with an example | **Depth beyond one entry's scope**: which delta to use; the locked-in total for the actual-volatility hedge against the path-dependent total for the implied-volatility hedge; the assumptions; finite-step risk. A new `res:` entry, linked from both |
| Itô calculus, GBM, risk-neutral pricing | `mod:black-scholes-merton` states lognormal prices, the hedging PDE and a check that the formula equals a discounted risk-neutral expectation; no Itô, Girsanov or Feynman-Kac anywhere (the three "Itô" hits are unrelated notation) | **New ideas**: Brownian motion and quadratic variation; Itô's lemma and the GBM solution; martingale pricing with the Feynman-Kac link |
| Finite-difference PDE methods | Finite differences appear only as Greek and PDE-residual checks (`option-pricing.tex`, `option-strategies.tex`) | **New idea** |
| Digital, barrier and Asian options | No entry; the "Asian"/"lookback" hits are unrelated (Asian manufacturers, lookback rate conventions) | **New ideas** |
| Short-rate models | `mod:term-structure-models-simulation`: equilibrium against no-arbitrage, Vasicek $B(0,4)=3.30$ and checked price 0.846849, Ho-Lee lattice fitted by forward induction, HJM drift condition named, market models named | **Depth/new**: affine closed forms, CIR and the Feller condition, Hull-White $\theta(t)$, HJM drift derivation, RFR forward-market model |
| Counterparty exposure and CVA | `meth:risky-bond-cva` (bond CVA $=\sum(1-R)q_iv_i$ with known exposure) | **New ideas** for derivatives: stochastic exposure profiles, netting and collateral, CVA under stated assumptions, wrong-way risk |
| Default correlation | `meth:credit-liquidity-tail-risk` already gives the Vasicek WCDR formula; no copula or tranche entry | **New**: copula definition, one-factor Gaussian copula, tranche loss, base correlation and its failure |
| Extreme value theory | `meth:var-es-estimation-methods` says in its Pitfalls that EVT is not covered | **New idea** |
| Kelly sizing | None (all "Kelly" hits are papers by Bryan Kelly) | **New idea** |
| Managed futures / trend following | `def:global-macro-strategy` (CTAs, regulatory meaning), `meth:macro-position-sizing-risk` (Turtle units), `meth:hedge-fund-strategy-classification` (managed futures family, crisis role), `def:alpha-model-taxonomy` (Moskowitz-Ooi-Pedersen and Hurst-Ooi-Pedersen evidence, volatility scaling, net returns) | **Narrow depth only**: CTA industry structure, vehicles and terms (CAIA chaps. 29 and 32); backlog |
| Hedge-fund replication | `meth:hedge-fund-factor-exposures` covers factor regressions, lags and alternative beta | **Depth**: payoff-distribution and bottom-up replication (CAIA chap. 33); backlog |
| Convertible arbitrage | `meth:hedge-fund-strategy-classification` has the mechanism and a checked delta-hedge example | **Depth only**: gamma trading, credit and borrow risks, crowding episodes (CAIA chap. 34); backlog |
| FRTB, SA-CCR, CVA capital, ISSB | One FRTB sentence in `meth:market-risk-limits-capital`; ESRS dating in `meth:esg-exposure-evaluation`; no SA-CCR, CVA-capital or ISSB statement | **Currency checks** (Section 8) |

Keyword hits and catalogue presence were not treated as proof of absence or of explanatory
completeness; each row above rests on reading the named entries.

### 3.2 Library and in-repo sources

"Read for this plan" means the pages named were opened and read during this revision.
Everything else is a candidate whose substantive passages are read inside the package that
uses it (Section 5, step 2).

| Source | Verified identity | Read for this plan | Planned use |
| --- | --- | --- | --- |
| Hull, *Options, Futures, and Other Derivatives*, 11th Global ed. (in-repo PDF; key `s7-hulloptions`, reading note exists) | Pearson, copyright 2022 per the reading note; printed page = PDF page | Brief contents; chap. 21 section heads (21.6 MC p. 489, 21.7 variance reduction, 21.8 finite differences); chap. 26 section heads (26.9 barriers incl. the Broadie-Glasserman-Kou shift, 26.10 binary, 26.11 lookback, 26.13 Asian); chap. 27.8 Longstaff-Schwartz example, pp. 660-663 | Primary for Batch L1 (chaps. 14, 19, 21, 26-28); chaps. 9, 24-25, 31-33 for later batches |
| Wilmott, *Paul Wilmott on Quantitative Finance*, 2nd ed., 3 vols (2006; catalogue key `wide-wilmott-pwoqf`, not yet cited) | 1,401-page PDF; printed page = PDF page $-21$ | Contents; chap. 12 "How to delta hedge", pp. 197-201; chap. 17.5 Kelly criterion, pp. 306-309; chap. 77 stability analysis, constraints and explicit code, pp. 1214-1218; chap. 78 implicit and Crank-Nicolson opening, pp. 1227-1229 | Primary for Batch L1 (chaps. 3-6, 12, 17, 22-25, 47, 76-78, 80) |
| Hull, *Risk Management and Financial Institutions*, 6th ed., 2023 (in-repo; registered as `risk-management-financial-institutions-2023`, printed = PDF $-28$) | As registered | Contents (chap. 9 copulas, 12 EVT, 18 xVAs, 26-27 Basel and FRTB) | Later batches. The draft's `s7-hullrisk` is the catalogue's key for this book but has never been used; keep the registered key |
| Gregory, *The xVA Challenge*, 3rd ed. (Wiley 2015, ISBN 978-1-119-10941-9) | Title and copyright pages | Contents (chaps. 4-17; chap. 8 capital is pre-reform) | Later batch; register a neutral key when first cited |
| Hilpisch, *Derivatives Analytics with Python* (Wiley 2015, ISBN 978-1-119-03799-6) | PDF metadata and copyright page | None beyond identity | Optional cross-check for MC/LSM code; not required |
| "Monte Carlo Methods.pdf" (CQF Textbooks folder) | 233-page scan without a text layer (PDF metadata 2004, DjVu origin); author not established | Pages 1-3: no text | **Optional, backlog B10.** No package depends on it; Hull and Wilmott cover Batch L1 |
| CAIA, *CAIA Level II: Advanced Core Topics in Alternative Investments*, **2nd ed.** (Wiley; copyright 2009, 2012; ISBN 978-1-118-36975-3) | Title page (PDF p. 5), copyright page (p. 6); printed page = PDF page $-34$ | Contents; chap. 33 pp. 475-477 (three replication approaches: factor-based, payoff-distribution, bottom-up) | Backlog B6. Chaps. 29-34 are managed futures, replication and convertible arbitrage; chap. 37 is quantitative equity and is not needed |
| CFA curricula: 2024 Levels I-III (six volumes each), Level II 2020, 2022 and 2023 vol. 1, Level III 2023 box set; Investment Series books | File list only (C0 later verified the 18 volumes of 2024 and read the passages in Section 8.1) | None | Gap finding in C0 only (not cited) |
| Kenyon and Stamm, *Discounting, Libor, CVA and Funding* (2012) | File name | None | Historical cross-check only |
| Catalogue keys with no local copy: `crypto-shreve`, `s6-glasserman`, `s6-brigo`, `s7-qrm`, `w2-mcneil-frey`, `wide-embrechts-extremal`, `wide-nelsen-copulas`, `w2-thorp-kelly`, `w2-busseti-kelly`, `gap-rates-backward-term-rates`, `vo-broadie-glasserman-kou-1997`, `gap-gregory5` | Catalogue entries only; none is in the repository or the library | None | Cited only if an authorised copy is obtained and read; otherwise Further reading. Kelly (1956) has two catalogue keys; use `ev-kelly-1956` (with DOI), not `s7-kelly` |

## 4. Gap register

The gaps in Section 3.1 are grouped into packages. Batch L1 (Section 6) takes the
derivatives-foundations group, which has its sources in hand and is a prerequisite for the
rest. Proposed later work (Section 7) and the backlog (Section 8) hold the remainder.

| Group | Packages | Placement |
| --- | --- | --- |
| Continuous-time foundations and numerical pricing | P1-P3 | Batch L1 |
| Hedging with the wrong volatility; growth-optimal sizing | P4-P5 | Batch L1 |
| Short rates, xVA, default correlation, EVT | P6-P9 | Proposed Batch L2 (Section 7), awaiting freeze |
| New ideas found by C0: correlation and independence tests, mean-CVaR optimisation, buying on margin | P11 | Proposed Batch L2, owner decision L2-D2 |
| Regulatory and disclosure currency | P10 | Batch L3 by default (decision L2-D4); done 2026-10-21 |
| CAIA depth, lookbacks, Kolmogorov equations, second-order Greeks beyond a sentence, MC Greeks, others | B1-B10 | Backlog (B3 done in L4) |
| C0 depth gaps not placed in L2 | B12-B17 | Backlog (B12, B13 done in L4) |
| Monte Carlo Greeks; seasoned variance swaps; cross-currency basis swaps | B3, B12, B13 | Batch L4, frozen with corrections and implemented 2026-10-21 (Section 7) |
| Lookback options; hedging with transaction costs | B2, B5 (C1-N1, C1-N2) | Batch L5, frozen and implemented 2026-10-21 (Section 7) |

## 5. Method for every package

1. **Define** the entries to add or extend, their objectives and the evidence needed.
2. **Read the substantive passages** in the sources listed for the package, record locators
   and note conflicting conventions (for example Wilmott's forward time against Hull's time to
   maturity).
3. **Verify currency** for any rule, standard, convention or dated fact against the issuer's
   current text. (Batch L1 has none; its content is model mathematics.)
4. **Write** original explanations with notation, assumptions, a worked example, limitations
   and See also links.
5. **Check numbers** in the package's script against the acceptance criteria below. Report
   Monte Carlo results with seed, path count and standard error.
6. **Record** sources, reading notes, entry evidence, review record, pathway links and coverage
   (Section 9) before the next package starts.

## 6. Batch L1 (frozen): derivatives foundations, numerical pricing, hedging and sizing

**Scope.** Ten new entries, three new topic files and ten new objectives (if decision E1 is
accepted). Four existing entries are touched: two substantive extensions
(`meth:monte-carlo-simulation`, control variates and discretisation bias;
`meth:greeks-delta-gamma-hedging`, vanna and volga) and two cross-reference-only edits
(`mod:black-scholes-merton`, `meth:active-currency-strategies`). Nothing outside this list is added to Batch
L1; any idea that surfaces during reading goes to Section 8.

**Dependencies.** P1 precedes all others (Itô, the pricing PDE and risk-neutral expectation).
P2 precedes P3 (P3's Asian check uses P2's control variate). P4 and P5 need only P1.
Order: P1, P2, P3, P4, P5.

**Synthetic data only.** Every Batch L1 check uses model-generated data with known answers and
fixed seeds. The checks show that each method is implemented correctly under its model; they
are not evidence about markets, and the entries say so.

### P1. Stochastic calculus foundations

- **Place.** New topic file `compendium/common-toolkit/stochastic-calculus.tex`, input in
  `common-toolkit/section.tex` after `probability`.
- **Entries.**
  - `def:brownian-motion-quadratic-variation`: Brownian motion, independent Gaussian
    increments, quadratic variation $[W]_T=T$, and why $(dW)^2=dt$ drives Itô's correction.
  - `res:ito-lemma-geometric-brownian-motion`: Itô's lemma in one dimension; GBM
    $S_T=S_0\exp((\mu-\tfrac12\sigma^2)T+\sigma W_T)$; mean $S_0e^{\mu T}$ against median
    $S_0e^{(\mu-\sigma^2/2)T}$.
  - `res:risk-neutral-pricing-feynman-kac`: price as a discounted expectation under the
    risk-neutral measure; Girsanov's change of drift from $\mu$ to $r-q$ with density
    $Z_T=\exp(-\theta W_T-\tfrac12\theta^2T)$, $\theta=(\mu-r+q)/\sigma$; Feynman-Kac linking the
    expectation to the BSM PDE already in `mod:black-scholes-merton`.
- **Extensions.** `mod:black-scholes-merton`: See also links to the three entries; no change
  to its checks.
- **Sources.** Hull OFOD chap. 14 (pp. 316-337) and chap. 28 (pp. 670-687); Wilmott chaps.
  3-6 (pp. 55-108). CQF Module 1 lectures as a cross-check only.
- **Checks** (`notes/artefacts/stochastic-calculus/stochastic-calculus-checks.py`; $S_0=100$,
  $\mu=8\%$, $\sigma=20\%$, $T=1$):
  - Exact GBM sampling (200,000 draws): sample mean and median within 4 standard errors of
    108.33 and 106.18.
  - Simulated quadratic variation of $W$ on $[0,1]$ with $n=10{,}000$ steps: within 4
    standard deviations ($\sqrt{2/n}$) of 1.
  - Itô on $S^2$: simulated $E[S_T^2]$ against $S_0^2e^{(2\mu+\sigma^2)T}$, within 4 standard
    errors.
  - Girsanov: real-world draws reweighted by $Z_T$ reproduce the BSM call ($K=105$, $r=3\%$,
    $q=0$) within 3 standard errors. This is new; the BSM entry's existing quadrature check
    is not repeated.
- **Objectives** (topic decision in Section 10.2): explain Brownian motion and quadratic
  variation; apply Itô's lemma to derive the GBM solution and its moments; value a derivative
  as a risk-neutral expectation and relate it to the pricing PDE.

### P2. Numerical pricing: finite differences and least-squares Monte Carlo

- **Place.** New topic file `compendium/volatility-options/numerical-methods.tex`, input after
  `option-pricing`.
- **Entries.**
  - `meth:finite-difference-option-pricing`. The specification the entry teaches and the
    script checks:
    - PDE in time to maturity $\tau$: $V_\tau=\tfrac12\sigma^2S^2V_{SS}+(r-q)SV_S-rV$.
    - Grid: uniform $S_i=i\,\Delta S$, $i=0,\dots,I$, $S_{\max}=3K$; $\tau_n=n\,\Delta\tau$;
      central differences in $S$.
    - Explicit scheme $V_i^{n+1}=A_iV_{i-1}^n+B_iV_i^n+C_iV_{i+1}^n$ with
      $A_i=\tfrac12\Delta\tau(\sigma^2i^2-(r-q)i)$, $B_i=1-\Delta\tau(\sigma^2i^2+r)$,
      $C_i=\tfrac12\Delta\tau(\sigma^2i^2+(r-q)i)$.
    - Sufficient stability condition: all three coefficients non-negative. Then
      $A_i+B_i+C_i=1-r\Delta\tau\le1$ and the scheme is monotone and stable in the maximum
      norm. This needs $\Delta\tau\le1/(\sigma^2I^2+r)$, which includes the discount term, and
      $\sigma^2i\ge|r-q|$ for $i\ge1$, which holds for every node when $\sigma^2\ge|r-q|$;
      otherwise the first derivative is upwinded near $S=0$. This matches Wilmott's
      conditions (chap. 77, $c\le0$, $2\nu_1a-\delta t\,c\le1$, $\tfrac12\nu_2|b|\le\nu_1a$,
      pp. 1214-1215). It replaces the draft's diffusion-only bound
      $\Delta t\le\Delta S^2/(\sigma^2S^2)$. It is sufficient, not necessary.
    - Boundaries: European put $V(0,\tau)=Ke^{-r\tau}$; American put $V(0,\tau)=K$;
      $V(S_{\max},\tau)=0$; for calls $V(0,\tau)=0$ and
      $V(S_{\max},\tau)=S_{\max}e^{-q\tau}-Ke^{-r\tau}$.
    - Crank-Nicolson: $\theta=\tfrac12$, started with four implicit half-steps (Rannacher)
      to damp the payoff kink. It is unconditionally stable for constant coefficients but not
      monotone for large $\Delta\tau$.
    - American exercise: explicit scheme by projection, $V\leftarrow\max(V,\text{payoff})$
      after each step; Crank-Nicolson by projected SOR on the linear complementarity problem
      ($\omega=1.5$, stop when the maximum change is below $10^{-9}$).
  - `meth:least-squares-monte-carlo`: regression of discounted continuation values on basis
    functions of the in-the-money paths. Exercise is allowed only on the simulated dates, so
    the method prices a Bermudan option. Using the policy on fresh paths gives a low-biased
    estimate; the upper bound (Andersen-Broadie) is mentioned only.
- **Extension.** `meth:monte-carlo-simulation` (common toolkit): control variates with the
  estimated optimal coefficient and variance-reduction factor; sampling error against
  time-discretisation bias. Its existing antithetic, seed and standard-error text stays.
- **Sources.** Hull OFOD secs. 21.6-21.8 (pp. 489-509) and 27.8 (pp. 660-665); Wilmott chaps.
  77-78 (pp. 1199-1252) and 80 (pp. 1263-1284).
- **Checks** (`notes/artefacts/numerical-pricing/numerical-pricing-checks.py`; $K=100$,
  $r=5\%$, $q=0$, $\sigma=20\%$, $T=1$, value read at $S=100$, a grid node):
  - European put, BSM 5.5735: Crank-Nicolson at $(I,N)=(150,75)$ and $(300,150)$; error ratio
    in $[3,5]$ (second order). Planning run: errors $9.9\times10^{-3}$ and
    $2.5\times10^{-3}$. The explicit scheme at $\Delta\tau$ just inside the bound converges
    at the same rate.
  - Instability: the explicit scheme at $I=150$ with $\Delta\tau$ 4.5 times the bound
    ($N=200$) returns $|V|>10^6$. The entry teaches this failure, so it is checked.
  - American put reference: 6.0904, the mean of CRR trees with 8,000 and 8,001 steps (6.09028
    and 6.09056). A single 2,000-step tree is not used, because its odd-even spread is about
    $1.1\times10^{-3}$. Acceptance: Crank-Nicolson with projected SOR at $I=300$ is within
    $4\times10^{-3}$ of the reference, and the error ratio from $I=150$ to $I=300$ is in
    $[3,5]$. Planning run: 6.0780 and 6.0870.
  - Least-squares MC, published example: Hull's eight-path put (Table 27.4, strike 1.10, 6%
    rate, three exercise dates, quadratic basis) gives 0.1144 to four decimals (p. 663).
  - Least-squares MC, Bermudan put: $S_0=K=100$, $r=5\%$, $q=0$, $\sigma=20\%$, $T=1$;
    exercise allowed only at $t_j=j/50$, $j=1,\dots,50$ (not at $t=0$, where immediate
    exercise would pay $K-S_0=0$). Paths sampled exactly at the 50 dates. Reference:
    the mean of two CRR trees with 5,000 and 5,050 steps (100 and 101 steps per exercise
    interval) that allow exercise only on those dates, cross-checked by Crank-Nicolson with
    projection only at those dates (within $5\times10^{-3}$). Basis $\{1,S/K,(S/K)^2\}$ on
    in-the-money paths; policy fitted on 100,000 paths (seed 20261021) and valued on 100,000
    independent paths (seed 20261022). Acceptance: reference $-0.05\le$ estimate $\le$
    reference $+3$ standard errors.
  - Control variate (in `inference-simulation-checks.py`): the existing call with the
    discounted terminal price as control; variance reduced by a factor above 2, and the
    estimate within 3 standard errors of 7.1281.
- **Objectives:** price European and American options by finite differences, with stability
  and convergence; value early-exercise options by least-squares Monte Carlo and state its
  bias. The control-variate extension adds depth to an already covered objective and is not
  counted.

### P3. Digital, barrier and Asian options

- **Place.** New topic file `compendium/volatility-options/exotic-options.tex`, input after
  `numerical-methods`.
- **Entries** (one teaching purpose each):
  - `meth:digital-option-valuation`: cash-or-nothing $e^{-rT}N(d_2)$ and asset-or-nothing
    $S_0e^{-qT}N(d_1)$; the vanilla call as their difference; call-spread replication; pin
    risk from the unbounded delta at the strike near expiry.
  - `meth:barrier-option-valuation`: in-out parity; the down-and-out call in closed form;
    discrete monitoring by the Broadie-Glasserman-Kou shift $He^{\pm0.5826\sigma\sqrt{T/m}}$
    (cited through Hull sec. 26.9); negative vega and gap risk near the barrier.
  - `meth:asian-option-valuation`: geometric-average closed form; the arithmetic average by
    Monte Carlo with the geometric option as a control variate; averaging lowers effective
    volatility. Corrected (L1 audit, L1-F3): averaging also moves the average's forward, so
    an Asian call is not cheaper than the matching vanilla in general (negative carry can
    reverse the order); the arithmetic-over-geometric (AM-GM) ordering always holds.
- **Sources.** Hull OFOD secs. 26.9-26.10 and 26.13 (pp. 620-627), 27.5-27.6 (pp. 653-658);
  Wilmott chaps. 22-23 and 25 (pp. 367-416, 427-444). `vo-broadie-glasserman-kou-1997` goes
  under Further reading unless obtained and read.
- **Checks** (`notes/artefacts/exotic-options/exotic-option-checks.py`, GBM, fixed seeds):
  - Common inputs: $S_0=100$, $K=100$, $r=5\%$, $q=2\%$, $\sigma=25\%$, $T=1$. Every Monte
    Carlo check uses 100,000 paths sampled exactly on its dates, with seeds 20261031,
    20261032, ... fixed in the script in the order of the checks below.
  - Digitals: the cash-or-nothing call pays 1 unit of cash if $S_T>K$ (value
    $e^{-rT}N(d_2)$); the asset-or-nothing call pays $S_T$ if $S_T>K$ (value
    $S_0e^{-qT}N(d_1)$). Asset digital minus $K$ times the unit cash digital equals the BSM
    call to $10^{-12}$. The centred call spread $[C(K-\varepsilon)-C(K+\varepsilon)]/(2\varepsilon)$
    converges to the unit cash digital; with $\varepsilon=2,1,0.5$ both successive error
    ratios lie in $[3.5,4.5]$ (second order).
  - Barrier: down-and-out and down-and-in calls, strike $K=100$, barrier $H=90$ below $S_0$
    and $K$, no rebate, notional one share. Knock-in plus knock-out equals the vanilla payoff
    path by path on common paths (daily monitoring), to $10^{-12}$.
  - Down-and-out call, continuous monitoring: Hull's closed form (sec. 26.9, $H\le K$)
    against Monte Carlo on 252 equal steps, each weighted by the product of the
    Brownian-bridge survival probabilities $1-\exp[-2\ln(S_i/H)\ln(S_{i+1}/H)/(\sigma^2\Delta t)]$
    (exact for continuous monitoring under GBM), within 3 standard errors.
  - Daily monitoring at $t_i=i/252$, $i=1,\dots,252$ ($S_0$ not monitored): discretely
    monitored Monte Carlo against the continuous closed form with the barrier shifted to
    $He^{-0.5826\sigma\sqrt{T/252}}$, within 3 standard errors plus 0.5% of value. The shift
    is an asymptotic approximation, so it does not match exactly.
  - Asian: average-price calls, $K=100$, averaging dates $t_i=i/12$, $i=1,\dots,12$, $S_0$
    excluded, equal weights. The geometric closed form uses the matching discrete
    convention: $\ln G$ normal with mean $\ln S_0+(r-q-\tfrac12\sigma^2)T\frac{n+1}{2n}$ and
    variance $\sigma^2T\frac{(n+1)(2n+1)}{6n^2}$, $n=12$. (Hull's continuous-averaging form,
    $\sigma/\sqrt3$ and $\tfrac12(r-q-\sigma^2/6)$, is taught as the $n\to\infty$ limit and
    not compared with the discrete simulation.) Geometric: closed form against Monte Carlo
    within 3 standard errors. Arithmetic: estimated-coefficient control variate on the
    geometric payoff; variance-reduction factor above 10; the controlled and uncontrolled
    estimates, on common paths, differ by less than 3 uncontrolled standard errors.
  - Corrected (L1 audit), deterministic additions that use no seed: (L1-F5) the unit cash
    digital's delta one day before expiry is positive at $S=99.9$, 100 and 100.1, so the hedge
    changes size, not sign; (L1-F3) with $S_0=100$, $K=60$, $r=2\%$, $q=8\%$, $\sigma=20\%$,
    $T=1$ and the same 12 dates, the vanilla call (33.5611) is below both the geometric
    closed form (35.7601) and the arithmetic lower bound $e^{-rT}(E[S_{\text{ave}}]-K)$
    (36.0876), each to $5\times10^{-5}$.
- **Objectives:** value digital options and explain their hedging (pin) risk; value barrier
  options under continuous and discrete monitoring; value Asian options by closed form and
  controlled simulation.

### P4. Hedging with the wrong volatility

- **Place.** `compendium/volatility-options/option-valuation.tex`, a new entry after
  `meth:greeks-delta-gamma-hedging`.
- **Entry** `res:delta-hedging-volatility-mismatch`. The model and position are stated in
  Conditions:
  - Real-world $dS=\mu S\,dt+\sigma S\,dW$, with constant and known actual volatility $\sigma$
    and constant implied volatility $\tilde\sigma$.
  - Long one European option bought at $V^i=V(S,t;\tilde\sigma)$ and marked to BSM at
    $\tilde\sigma$ throughout.
  - Short $\Delta$ shares; the cash balance earns and pays $r$; dividend yield $q$; no costs;
    continuous rebalancing.
  - Results, with total profit measured as present value at $t_0$:
    - Hedging with $\Delta^a$ (actual volatility) locks in $V^a-V^i$ by expiry. The
      mark-to-market P&L along the way is random.
    - Hedging with $\Delta^i$ (implied volatility) gives increments
      $\tfrac12(\sigma^2-\tilde\sigma^2)S^2\Gamma^i\,dt$, which have no $dW$ term (zero
      infinitesimal diffusion). The total
      $\tfrac12(\sigma^2-\tilde\sigma^2)\int_{t_0}^Te^{-r(t-t_0)}S_t^2\Gamma^i_t\,dt$ is
      path-dependent. Its sign is fixed when $\Gamma^i\ge0$, but its mean depends on the
      real-world drift. Corrected (L1 audit, L1-F2): the entry must state that a positive
      total needs both $\sigma>\tilde\sigma$ and $\Gamma^i\ge0$ (a convex vanilla payoff);
      for a sign-changing gamma it can be negative, and $V^a-V^i<0$ where vega is negative.
  - With finite rebalancing both strategies carry hedging error; "zero diffusion" describes
    the continuous-time increment, not the variance over a finite step (Wilmott chap. 12,
    pp. 200-201; chap. 47 for discrete hedging).
- **Extensions.**
  - `meth:greeks-delta-gamma-hedging`: one or two sentences defining vanna and volga, and a
    See also to the new entry.
  - `meth:active-currency-strategies`: a See also link only.
- **Sources.** Wilmott chap. 12 (read for this plan) and chap. 47; Hull OFOD chap. 19.
  Ahmad and Wilmott (2005) is registered only if obtained and read; it is not required.
- **Checks** (`notes/artefacts/option-valuation/volatility-mismatch-hedging-check.py`):
  - Inputs: $S_0=K=100$, $T=1$, $r=5\%$, $q=0$, $\mu=10\%$, $\sigma=30\%$, $\tilde\sigma=20\%$;
    20,000 paths; 252 and 2,520 rebalancing steps. Then $V^a-V^i=3.7807$.
  - $\Delta^a$ hedge: mean P&L within 3 standard errors of 3.7807 at both step counts, and
    the ratio of standard deviations (252 against 2,520 steps) in $[2.8,3.5]$, against
    $\sqrt{10}=3.16$. Planning run: 0.626 and 0.199.
  - $\Delta^i$ hedge: the RMS gap between each path's P&L and its pathwise integral shrinks
    by a factor in $[2.5,3.8]$. The cross-path standard deviation stays above 1.5 at 2,520
    steps, so the total remains random. Planning run: gap 0.799 to 0.254, standard deviation
    1.75. The entry does not claim that its mean equals $V^a-V^i$.
  - The script runs in under a minute (vectorised; time steps looped, paths not).
  - Corrected (L1 audit, L1-F2), a deterministic counterexample: a unit cash-or-nothing call
    with $S_0=120$, $K=100$, $r=5\%$, $q=0$, $T=1$ is worth 0.8141 at 20% and 0.6980 at 30%
    volatility (each to $5\times10^{-7}$), and its gamma at 20% is positive at $S=80$ and
    negative at $S=120$ (closed form against a finite difference). The vanilla simulation
    and its criteria are unchanged.
- **Objective:** explain and quantify the P&L of delta hedging when implied and actual
  volatility differ, for each choice of hedge volatility.

### P5. Growth-optimal (Kelly) sizing

- **Place.** `compendium/portfolio-construction-risk/portfolio-construction-models.tex`, after
  `meth:rule-based-position-sizing`.
- **Entry** `res:kelly-growth-optimal-fraction`.
  - Discrete bet: $f^*=p-q/b$, maximising $G(f)=p\ln(1+bf)+q\ln(1-f)$.
  - Continuous model: constant $\mu$, $r$ and $\sigma$; continuous rebalancing; no costs or
    leverage limits. Log wealth grows at $g(f)=r+f(\mu-r)-\tfrac12f^2\sigma^2$ (Itô, from P1),
    so $f^*=(\mu-r)/\sigma^2$.
  - Fractional Kelly, and estimation error in $\mu$, which pushes a full-Kelly bet into
    over-betting; the link to log utility. Risk-constrained Kelly appears under Further
    reading unless `w2-busseti-kelly` is read.
- **Corrected half-Kelly statement** (replaces the draft's "3/4 of optimum with half
  variance"). In the continuous model, half Kelly has half the portfolio volatility and one
  quarter of the log-return variance rate. Its expected log growth **in excess of cash** is
  exactly 3/4 of the maximum excess. At twice Kelly the excess growth is zero. These
  identities do not carry over exactly to discrete bets, or to the variance of terminal
  wealth. Wilmott's "halves your volatility ... decreases your expected growth rate by 25%"
  (chap. 17, p. 309) rests on his small-edge quadratic approximation, eq. (17.1).
- **Sources.** Wilmott chap. 17.5 (pp. 306-309, read for this plan); `ev-kelly-1956` (Bell
  System Technical Journal 35(4), 917-926) and `w2-thorp-kelly`, read in the package if an
  authorised copy is accessible, otherwise Further reading.
- **Checks** (`notes/artefacts/portfolio-construction/kelly-check.py`):
  - Continuous model with $\mu=8\%$, $r=2\%$, $\sigma=20\%$: $f^*=1.5$; excess growth 0.045
    and 0.03375 (ratio 0.75 exactly); variance-rate ratio 0.25.
  - Continuous identity, matching model: for $f\in\{f^*/2,f^*,2f^*\}$, log wealth over
    $T=10$ years sampled exactly as $\ln W_T=g(f)T+f\sigma W_T$ (200,000 draws, seed
    20261041); $\ln W_T/T$ has mean within 3 standard errors of $g(f)$ and standard
    deviation within 1% of $f\sigma/\sqrt T$.
  - Daily rebalancing, tested separately against an independent expectation: the asset's
    daily gross return is $\exp((\mu-\tfrac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z)$, cash
    grows by $e^{r\Delta t}$, $\Delta t=1/252$, and the fraction $f$ is restored each day.
    Corrected (L1 audit, L1-F1): for $f>1$ the one-day gross factor is nonpositive with
    positive probability (at $f=3$, $Z\le-32.2$, about $10^{-227}$), so $E[\ln(\dots)]$ is
    not defined and the levered fractions are not used here; they stay in the continuous
    checks. The daily checks use the unlevered fractions $f\in\{0.25,0.5,0.75\}$ ($0.75=f^*/2$).
    The expected annual log growth $g_{\Delta t}(f)=E[\ln(\dots)]/\Delta t$ is approximated
    by 80-point Gauss-Hermite quadrature. Acceptance: (o) for $f=1.5$ and 3 the script
    shows a negative gross factor below the computed threshold; for $f=1$ the quadrature equals
    $\mu-\tfrac12\sigma^2=g(1)$ to $10^{-12}$ (no trade); (q) quadrature convergence: the 40-,
    80- and 160-node rules and adaptive integration agree within $10^{-10}$ a year and within
    1/1,000 of the bias, at $\Delta t$ and $\Delta t/2$; (i) simulated daily-rebalanced log
    wealth (20,000 paths, 2,520 steps, seed 20261042) has mean $\ln W_T/T$ within 3 standard
    errors of $g_{\Delta t}(f)$; (ii) the discretisation bias $|g_{\Delta t}(f)-g(f)|$ is below
    $5\times10^{-4}$ a year for all three fractions; (iii) refinement: the bias at
    $\Delta t/2$ is between 0.4 and 0.6 of the bias at $\Delta t$ (first order). Seed and
    tolerances (i)-(iii) are as before. Original wording: "for all three fractions"
    meant $f^*/2$, $f^*$ and $2f^*$, the quadrature value was called exact, and the planning
    value was $g_{\Delta t}(3)-g(3)\approx-1.0\times10^{-4}$.
  - Discrete bets: $p=0.6$, $b=1$ gives $f^*=0.2$ and a half-Kelly growth ratio of 0.7470;
    $p=0.3$, $b=4$ gives $f^*=0.125$ and 0.7727. Both are asserted as not equal to 0.75,
    which shows the continuous identity's limits.
- **Objective:** derive the growth-optimal fraction for discrete bets and for a lognormal
  asset, and assess fractional Kelly under estimation error.

### Batch L1 acceptance and stopping conditions

**Per package (focused checks).** The package's script passes on its own
(`uv run --frozen python <script>` from its folder); `make check-compendium` passes; ruff
lint and format pass on the changed scripts; the records of Section 9 are written. After the
records, `make check-coverage` passes.

**Batch completion.**
- All ten entries, the two substantive extensions, the two cross-reference edits and the
  records are in place.
- `make source-check` passes.
- `make pdf` builds. The log has no undefined references or citations and no new overfull
  boxes, and the rendered pages of the three new topic files and the edited entries have been
  inspected (equations, lists and short last lines; `compendium/README.md`).
- `make pre-commit` passes on the tree to be committed.
- The completion report lists the sources actually read, entries changed, objectives covered,
  the shortfall against 45 with reasons, and the backlog items created.

**Stop a package and continue the others** (record the objective as `partial` with
`next_action: obtain-source` or `review` and the exact gap) when:
- a passage the package relies on cannot be read; or
- an acceptance check still fails after one diagnosis shows that the cause is conceptual (a
  source disagreement or a wrong criterion), not a coding error. Record the evidence and ask
  the owner before changing the criterion.

**Stop the batch and report** when:
- a repository check fails for reasons outside the batch;
- a checker or schema change appears necessary;
- an entry could only be supported by a curriculum or CAIA volume (a D1 exception); or
- scope would grow beyond the list above.

There are no blanket failure-injection runs. The only deliberate failure is the
explicit-scheme instability that P2 teaches.

### Batch L1 post-implementation audit corrections (2026-10-21)

An audit of the implemented, uncommitted Batch L1 reran the six affected scripts and both
checkers (all passing) and found five issues that the checks did not test. The owner
authorised mathematically necessary changes to the affected examples and criteria; seeds were
not changed and no tolerance was loosened. All ten objectives are kept; none was added.

| Finding | Problem | Correction |
|---|---|---|
| L1-F1 (P5) | Daily rebalancing at $f=1.5$ and 3 called the quadrature value an exact expectation; for $f>1$ a finite step can make wealth nonpositive, so $E[\ln W]$ is undefined. The quadrature nodes and simulation missed a tail of probability about $10^{-227}$ ($f=3$). | Daily checks moved to unlevered $f=0.25,0.5,0.75$ with the same seed and tolerances; the levered case is shown to be undefined; quadrature called an approximation and checked for convergence; $f=1$ checked analytically. Continuous leveraged results unchanged. |
| L1-F2 (P4) | The entry's Conditions said $\sigma>\tilde\sigma$ suffices for a positive implied-hedge total, dropping $\Gamma^i\ge0$. | Condition restored in Statement, Conditions and Pitfalls; cash-digital counterexample ($V^a-V^i=-0.1160$, gamma changing sign) added to the script and the Practice. Vanilla simulation unchanged. |
| L1-F3 (P3) | The Asian entry said average-price options are cheaper than regular ones (Hull says they "tend to be"). | Quoted Hull's wording; stated that averaging moves the forward as well as the dispersion; AM-GM kept; negative-carry counterexample (vanilla 33.5611 below geometric 35.7601 and the arithmetic bound 36.0876) added. |
| L1-F4 (P1) | Pitfalls called the Brownian scaling "square-root scaling of variance". | Variance is proportional to elapsed time, standard deviation to its square root. |
| L1-F5 (P3) | The digital example said the large stock hedge "reverses" across the strike. | The delta is positive on both sides (0.2530, 0.2533, 0.2525 at 99.9, 100, 100.1, one day out); the hedge changes size and the gamma changes sign. A deterministic check was added. |

## 7. After Batch L1: discovery task C0 and the proposed Batch L2

### C0. Bounded CFA cross-level comparison (exploratory; not part of Batch L1)

**Completed 2026-10-21.** All 15 candidate reviews were used, including the six required
readings. The findings, the extent of each pass and what was left unexamined are in Section 8.1.
The specification below is kept as it was run.

C0 runs after Batch L1 and before Batch L2 is frozen. It is gap finding only: no entry is
written and nothing is cited.

- **Inputs.**
  - The contents of the 2024 Level I-III curricula (18 volumes): reading titles and
    second-level section heads.
  - `notes/coverage/objectives.json` (titles, entries).
  - `notes/coverage/outline-crosswalk.json` (the 2026/2027 modules).
- **Pass 1 (titles).** Readings or sections with no matching objective or entry become
  candidates.
- **Pass 2 (depth inside familiar readings).** Read substantively six quantitative readings
  that map to covered objectives:
  - Level II option valuation;
  - Level II arbitrage-free valuation of bonds;
  - Level II term structure and interest-rate dynamics;
  - Level II credit analysis models;
  - Level III options strategies;
  - Level III swaps, forwards and futures strategies.

  Compare their worked depth with the mapped entries.
- **Bound.** At most 15 candidates read substantively in total. Each outcome is "already
  explained" (with the entry label), "depth gap" or "new idea". Investment Series books are
  checked as candidate citable sources for the gaps found, not as comparison targets.
- **Output.** A short table added to Section 8 of this file, and a Batch L2 scope proposal.
  C0 ends when the cap is reached or both passes are complete.

### Proposed Batch L2 (refined by C0 and corrected after audit, 2026-10-21; awaiting owner freeze)

**What C0 changed** (findings in Section 8.1).
- The six required readings teach nothing at worked depth that the mapped entries do not,
  apart from five depth gaps. One of them bears on an L2 package: CVA on a calibrated rate tree,
  including a risky floater and its discount margin (candidate 4). It would extend
  `meth:risky-bond-cva` and adds no objective.
- The 2024 curricula do not teach the P7-P9 subjects. Wrong-way risk and extreme value theory
  are only named (L1 vol. 6, PDF p. 164; L3 vol. 4, PDF p. 156), and copulas and Kelly sizing
  do not appear. P6-P9 therefore rest on the Section 3.1 evidence, not on C0.
- C0 found three new ideas whose sources are registered or openly available. They are proposed
  as package P11.

**Scope, if decisions L2-D1 to L2-D5 are taken as recommended (Section 10.3).**
- New entries: 11 (P6 2, P7 3, P8 2, P9 1, P11 3).
- New topic files: 2 (`corporate-credit-capital/counterparty-xva.tex` and
  `securitised-structured-credit/default-correlation.tex`). Each is input from its existing
  chapter wrapper.
- Existing entries extended (no objective counted):
  - `mod:term-structure-models-simulation` (P6): calibrating simulated rate paths to today's
    curve by a drift adjustment, and the lognormal no-arbitrage alternative. This is added only
    if a source read in the package supports it.
  - `meth:risky-bond-cva` (P7): tree-based CVA and a risky floater, subject to decision L2-D3.
  - `meth:var-es-estimation-methods` (P9): its Pitfalls sentence on EVT becomes a link.
  - `meth:credit-liquidity-tail-risk` (P8): a See also link only.
- Optional small extensions, with sources in the repository (decision L2-D5):
  - `meth:black-model-rates-currencies`: the receiver swaption, payer-receiver parity, and a
    callable bond as a straight bond less a receiver swaption (Hull OFOD chap. 29, sec. 29.3;
    cited by the entry for the payer swaption, not reread in C0 for these points).
  - `meth:multi-period-binomial-valuation`: known discrete dividends in a tree and the
    dividend-motivated early exercise of an American call (Hull OFOD sec. 21.3, p. 480;
    located, not yet read).
- New objectives: about 11, in a range of 10-12 (P6 2, P7 2-3, P8 2, P9 1-2, P11 3). Topics:
  - P6: `topic:arbitrage-free-bond-valuation`;
  - P7: `topic:credit-models`;
  - P8: `topic:securitisation`;
  - P9: `topic:market-risk-measurement`;
  - P11: `topic:statistical-inference`, `topic:portfolio-risk-return` and
    `topic:equity-securities-markets`.

  All have `planned_batch` 8. E1's rule applies: only new ideas get objectives.

**Dependencies and order.** Run P6 first: its Hull-White simulation supplies P7's swap
exposure profile. P7 follows P6. P8, P9 and P11 depend on no other L2 package. Proposed order:
P6, P7, P8, P9, P11a, P11b, P11c, with each package's checks and records complete before the
next starts (Section 5).

**Data.** All checks are synthetic, with fixed seeds, except P6's curve. That curve comes from
the GSW file, which is git-ignored and present at
`reading_materials/derivatives-validation/empirical/feds200628.csv` (last row 2026-10-09; the
row for 2026-09-30 exists). As in Batch L1, a check shows that a method is implemented
correctly under its model. It is not evidence about markets.

**Material source gaps.**
- Tree-based CVA (candidate 4): the curriculum's source, Smith (2017), is not in the library.
  The Investment Series *Fixed Income Analysis* (2015), chap. 6 (section heads examined, PDF
  pp. 305-345) is the earlier, structural and reduced-form version of the reading, without the
  tree. This is decision L2-D3.
- `gap-rates-backward-term-rates`, `s7-qrm`, `w2-mcneil-frey` and `wide-embrechts-extremal`
  are not held. They go under Further reading unless an authorised copy is obtained and read.
- CRE31 (P8) and the margin rules (P11c) must be read in their current text, with retrieval
  dates. Rockafellar and Uryasev (`s6-cvar`, P11b) is an open author PDF. Each needs network
  access during its package.

Each package below states its data, its claims and predetermined criteria. Values written here
are not planning results. Each package script computes its own, and the criteria, not those
values, are binding.

- **P6 Short-rate and forward-rate models** (`rates-credit-mortgages/arbitrage-free-valuation.tex`
  after `mod:term-structure-models-simulation`).
  - Two candidate entries: `mod:affine-short-rate-models` (Vasicek and CIR bond formulas,
    Feller condition, Hull-White $\theta(t)$, negative rates) and
    `mod:hjm-forward-rate-models` (HJM drift condition; the forward market model; Black
    caplets; the backward-looking RFR extension, if `gap-rates-backward-term-rates` is
    read).
  - Sources: Hull OFOD chaps. 31-33 (pp. 719-772; the draft's "32-33" omitted chap. 31) and
    Wilmott chaps. 30-31 and 37. For the extension: the Handbook chap. 37 (pp. 859-862), which
    `mod:term-structure-models-simulation` already cites, is read to confirm that it describes
    calibrating Monte Carlo paths by a drift adjustment.
  - Data: the Federal Reserve Board's GSW Svensson parameters (`feds200628.csv`, kept outside
    Git) on 30 September 2026, giving an analytic instantaneous forward curve. The curve is
    labelled "fitted off-the-run nominal Treasury zero curve (GSW)", never SOFR or OIS.
  - Claims: Hull-White's $\theta(t)$ reproduces that curve by construction (zero prices to
    $10^{-10}$; simulated discount factors within 4 standard errors, below). The mean-reversion and
    volatility parameters are illustrative and stated as not calibrated: calibrating them
    needs cap or swaption volatilities, which are not held.
  - Further checks: the existing Vasicek 0.846849 is reused; the CIR closed form against
    Monte Carlo; HJM with constant volatility gives the Ho-Lee drift $\sigma^2t$.
  - Criteria fixed by C0 (the package script fixes its seeds before its first run; a failed
    statistical check is diagnosed, not rerun with another seed):
    - Hull-White on the GSW curve: analytic zero-coupon prices equal the GSW discount factors
      at 1 to 30 years to $10^{-10}$. Simulated discount factors (100,000 paths) lie within 4
      standard errors at each of the 30 maturities. With 30 correlated comparisons, 4 rather
      than 3 standard errors keeps the chance of a false failure below about 0.2 percent.
      *Corrected (L2 audit).* Exact Ornstein-Uhlenbeck samples of $r$ do not make
      $\exp(-\int_0^T r\,du)$ exact. Each step therefore samples the pair
      $\big(x_t,\int_s^t x_u\,du\big)$ jointly from its exact bivariate normal transition given
      $x_s$, where $x=r-\alpha(t)$ is the Ornstein-Uhlenbeck part, so the discount factor is
      unbiased. The conditional mean of the integral is $x_sB(s,t)$ with
      $B=(1-e^{-a\Delta})/a$. Its variance is
      $\frac{\sigma^2}{a^2}\big[\Delta-2B+\frac{1-e^{-2a\Delta}}{2a}\big]$, and its covariance
      with $x_t$ is $\frac{\sigma^2}{2a^2}(1-e^{-a\Delta})^2$, where $\Delta=t-s$. The
      deterministic part $\int_s^t\alpha(u)\,du$ comes from the curve in closed form. A
      trapezoid rule on the exact $r$ samples is also run as a bias diagnostic: halving its
      step from monthly must change the 30-year discount factor by less than a tenth of a
      standard error, or the trapezoid result is reported as biased and not used.
    - CIR with $a=0.5$, $b=4\%$, $\sigma=10\%$, $r_0=3\%$ (so $2ab\ge\sigma^2$): the closed-form
      five-year zero price against Monte Carlo with exact non-central chi-square transitions
      (200,000 paths), within 3 standard errors. The integration grid is halved until the price
      changes by less than a tenth of a standard error. With $\sigma=25\%$, an Euler scheme
      without truncation produces negative rates and exact sampling does not.
    - HJM with constant volatility: the implied short-rate drift equals
      $\partial f(0,t)/\partial t+\sigma^2t$ to $10^{-10}$ on the GSW curve.
    - The forward market model: a one-factor lognormal simulation of a caplet agrees with
      Black's formula within 3 standard errors, and the existing Hull Example 29.3 value
      (0.00519 million) is reused, not recomputed.
  - Objectives (2): apply affine short-rate models (Vasicek, CIR, Hull-White), including their
    bond prices and fit to today's curve; explain the HJM drift condition and value caplets in
    the forward market model.
- **P7 Counterparty exposure and xVA** (new topic file
  `corporate-credit-capital/counterparty-xva.tex`).
  - Candidates: `def:counterparty-exposure-measures`, `meth:credit-valuation-adjustment`,
    `def:wrong-way-risk`, with DVA/FVA/MVA/KVA in outline inside the CVA entry or a separate
    entry if reading shows a distinct idea. The capital rules go to P10.
  - Formulation stated in the entry: unilateral CVA from the bank's view (own default
    ignored); exposure $E(t)=\max(V(t),0)$ of the netting set's mark-to-market,
    uncollateralised first, then with a margin period of risk; risk-neutral measure with the
    bank-account numéraire. In general
    $\mathrm{CVA}=(1-R)\,E^Q\!\big[D(0,\tau)E(\tau)\mathbf 1_{\{\tau\le T\}}\big]$. On a date
    grid, with default in $(t_{i-1},t_i]$ treated as occurring at $t_i$, this is
    $(1-R)\sum_iE^Q[D(0,t_i)E(t_i)\mathbf 1_{\{t_{i-1}<\tau\le t_i\}}]$. *Corrected (L2
    audit).* Under stochastic rates, independence of the exposure $E$ from default is not
    enough to factor this. The factorization
    $(1-R)\sum_i\mathrm{EE}^*(t_i)\,\mathrm{PD}(t_{i-1},t_i)$, with
    $\mathrm{EE}^*(t)=E^Q[D(0,t)E(t)]$ and $\mathrm{PD}$ the risk-neutral default
    probabilities, requires $\tau$ to be independent of the discounted exposure $D(0,t_i)E(t_i)$
    at each grid date. A sufficient condition is that $\tau$ is independent of the rates and
    market factors jointly, with $R$ constant (or independent of both). Default correlated
    with rates breaks it even when it is independent of the swap's mark-to-market. Always
    $\mathrm{EE}^*(t)=P(0,t)\,E^{Q_t}[E(t)]$ under the $t$-forward measure; this equals
    $P(0,t)\,\mathrm{EE}(t)$ with $\mathrm{EE}$ taken under $Q$ only when rates are
    deterministic, or when $D(0,t)$ and $E(t)$ are uncorrelated under $Q$. Wrong-way risk
    breaks the independence, so the joint expectation above is needed. The entry states the
    assumption it uses, and the swap example uses an independent, deterministic hazard rate.
  - Decisive small example (synthetic): one exposure date, $V\sim N(0,s^2)$ and default when
    a latent normal $Y$, with $\rho=\mathrm{Corr}(V,Y)$, falls below $\Phi^{-1}(\mathrm{PD})$
    (lower-tail default). CVA by bivariate-normal quadrature against Monte Carlo; it equals
    the independent value at $\rho=0$, falls as $\rho>0$ rises (right-way risk: default comes
    with low $V$) and rises as $\rho<0$ falls (wrong-way risk). With $s=1$, $\mathrm{PD}=5\%$,
    $R=40\%$ and unit discounting, CVA is 0.03253, 0.01197 and 0.00159 at $\rho=-0.5$, 0 and
    0.5. An upper-tail default convention is equally valid if the sign is changed
    consistently. A swap exposure profile simulated under one-factor
    Hull-White shows the humped EE and PFE.
  - Sources: Gregory 3rd ed. chaps. 10-11, 14-17; Hull OFOD chap. 9; RMFI chap. 18.
  - Criteria fixed by C0:
    - The wrong-way example: bivariate-normal quadrature against Monte Carlo (200,000 draws,
      fixed seed), within 3 standard errors at each $\rho$. At $\rho=0$ the value equals the
      independent closed form $(1-R)\,\mathrm{PD}\,s/\sqrt{2\pi}$ to $10^{-10}$. CVA is strictly
      decreasing in $\rho$ on $\{-0.5,-0.25,0,0.25,0.5\}$. The three values above are the
      audited planning values (finding R1); the script recomputes them.
    - The swap profile, on P6's Hull-White paths: an at-market swap has EE(0) equal to 0, and
      EE peaks at an interior date. Uncollateralised, the netted exposure never exceeds the sum
      of the stand-alone exposures on any path, since $\max(a+b,0)\le\max(a,0)+\max(b,0)$, so
      the same holds for EE at every date. PFE (97.5 percent) is reported with a bootstrap
      standard error.
    - *Corrected (L2 audit): collateral mechanics.* Value $V(t)$ is the bank's
      mark-to-market of the netting set, ex-coupon. The CSA is two-way, with daily variation
      margin in cash, zero threshold and zero minimum transfer amount, and no initial margin.
      The collateral balance $C(t)$ is held by the bank when positive and posted by the bank
      when negative. The margin period of risk is $\delta=10$ business days ($10/252$ years).
      The last margin call settled before a default at $t$ was based on $V(t-\delta)$, so
      $C(t)=V(t-\delta)$ for $t\ge\delta$ and $C(t)=0$ for $t<\delta$. No margin moves in
      either direction during the MPR, and posted collateral is not segregated. Collateral
      earns the short rate, the rate used to discount, so it adds no funding term. Interest
      accrued on the balance during the MPR is ignored. Exposure dates sit at mid-months, so
      no swap payment falls in any window $(t-\delta,t]$. Each exposure date $t$ and the
      date $t-\delta$ are simulated on the same path, with an exact step between them.
      Collateralised exposure is $E_c(t)=\max(V(t)-C(t),0)$.
    - Collateral criteria. Per-date dominance $\mathrm{EE}_c(t)\le\mathrm{EE}(t)$ is not
      required under two-way lagged collateral. It fails on paths where the bank has posted,
      $V(t-\delta)<0<V(t)$, and can fail in expectation, for example for an out-of-the-money
      swap. Only properties that the model implies are checked:
      - $E_c(t)=E(t)$ for $t<\delta$ on every path.
      - For a one-way variant in which only the bank receives collateral,
        $C(t)=\max(V(t-\delta),0)$, $E_c(t)\le E(t)$ holds on every path.
      - Under two-way collateral, $E_c(t)\le|V(t)-V(t-\delta)|$ on every path, and with
        $\delta=0$ exposure is zero.
      - $\mathrm{EE}_c$ at 5, 10 and 20 business days is reported against the
        Gaussian-increment approximation $\sigma_{\Delta V}(t)/\sqrt{2\pi}$, where
        $\sigma_{\Delta V}(t)$ is the simulated standard deviation of $V(t)-V(t-\delta)$. It is
        reported as a diagnostic, not a pass condition, because swap increments are not
        exactly normal or mean zero.
      - The uncollateralised and collateralised CVA are both reported.
    - The tree-based CVA extension, if L2-D3 accepts it, uses the Handbook tree already in
      `meth:binomial-rate-tree-calibration` and original inputs, not the curriculum's.
      Node-weighted expected exposure gives the same CVA as the pathwise average to
      $10^{-10}$. As $\sigma\to0$, it tends to the forward-rate calculation of
      `meth:risky-bond-cva`. A default-free floater paying the tree rate flat is worth par at
      every node to $10^{-10}$. The discount margin solved on the tree reprices the fair value
      to $10^{-8}$.
  - Objectives (2-3): measure counterparty exposure (EE, EPE, PFE) with netting and collateral;
    calculate unilateral CVA under independence; assess wrong-way risk (the last two may form
    one objective if the reading shows one idea).
- **P8 Default correlation** (new topic file `securitised-structured-credit/default-correlation.tex`).
  - Candidates: `mod:gaussian-copula-default-correlation` and
    `meth:tranche-loss-base-correlation`; it links to the existing WCDR formula in
    `meth:credit-liquidity-tail-risk` rather than restating it.
  - Sources: Hull OFOD chap. 25, RMFI chap. 9, and the Basel IRB formula (CRE31, current text
    read).
  - Checks (synthetic): large-pool tranche expected loss by quadrature against finite-pool
    simulation; IRB capital at sample PD and correlation.
  - Criteria fixed by C0:
    - The expected losses of tranches that partition the capital structure sum to the pool's
      expected loss, $\mathrm{PD}\times\mathrm{LGD}$, to $10^{-12}$.
    - *Corrected (L2 audit).* No granularity allowance is used. The benchmark is an
      independent, exact finite pool. For a homogeneous pool of $N$ names, the number of
      defaults conditional on the factor $M$ is binomial$(N,p(M))$. The tranche expected loss is
      therefore a one-dimensional integral over $M$ of a finite binomial sum, computed by
      adaptive quadrature or with nodes doubled until it changes by less than $10^{-10}$.
      - Correctness: a finite-pool simulation of 1,000 names (50,000 scenarios, fixed seed)
        agrees with the exact finite-pool value for each tranche within 3 standard errors.
      - Granularity: the deterministic gap between the large-pool and exact finite-pool values
        is reported for $N=250$, 500 and 1,000, for each tranche. *Corrected (L2 freeze).* It is
        a reported result, not a pass condition: the gap need not shrink monotonically in $N$
        for a thin tranche (counterexample in "Batch L2 freeze corrections"). The exact
        finite-pool benchmark, its quadrature convergence and the Monte Carlo comparison stay
        binding.
    - The conditional default rate inside the IRB formula equals the WCDR of
      `meth:credit-liquidity-tail-risk` to $10^{-12}$ at the same PD and correlation. The capital
      figure is recomputed from the CRE31 text as read, at its retrieval date.
  - Objectives (2): model default correlation with a one-factor Gaussian copula; value tranches
    and explain base correlation and where it fails.
- **P9 Extreme value theory** (`portfolio-construction-risk/risk-models.tex` after
  `meth:var-es-estimation-methods`, whose Pitfalls sentence is then updated).
  - Candidate `meth:extreme-value-tail-estimation` (block maxima and peaks over threshold;
    GPD; Hill; threshold choice; VaR and ES; the McNeil-Frey two-step on GARCH residuals).
  - Source: RMFI chap. 12; `s7-qrm`, `w2-mcneil-frey` and `wide-embrechts-extremal` only if
    obtained and read.
  - Data (synthetic):
    - i.i.d. Student $t$ with 4 degrees of freedom, $n=5{,}000$. VaR and ES are in closed
      form. The tail index $\xi=0.25$ holds only asymptotically.
    - The GARCH(1,1)-$t$ generator already used for `meth:var-es-estimation-methods`, for the
      two-step method.
  - Estimators, fixed in advance:
    - Upper tail of the loss, with threshold $u$ at the empirical 95th percentile and
      $k=n/20=250$ exceedances.
    - Hill uses those $k$ largest order statistics:
      $H_k=\frac1k\sum_{i=1}^k\ln X_{(n-i+1)}-\ln X_{(n-k)}$, the threshold being the
      $(k+1)$-th largest observation.
    - The GPD is fitted by maximum likelihood to the $k$ excesses.
    - VaR and ES at 99 and 99.5 percent use the peaks-over-threshold formulas.
  - *Corrected (L2 audit).* The original acceptance rule (bootstrap intervals for Student
    $t_4$ must cover 0.25) mixed numerical correctness with finite-threshold bias. At the 95th
    percentile of $t_4$ ($u\approx2.13185$), the population Hill functional
    $E[\ln(X/u)\mid X>u]$ is about 0.348898. The Kullback-Leibler-best GPD shape for the
    excesses there is about 0.192. Neither is 0.25. The plan now separates two kinds of
    check.
  - Numerical correctness (pass or fail; known-truth benchmarks):
    - Exact Pareto data with $\xi=0.25$. By Rényi's representation, $H_k$ is distributed as
      $\xi\,\mathrm{Gamma}(k,1)/k$. Over 2,000 replications (fixed seed), the mean is within
      3 standard errors of 0.25, and the standard deviation is within 5 percent of
      $\xi/\sqrt k$.
    - Student $t_4$, with $n=10^6$ and the same $k/n=0.05$: $H_k$ lies within 3 standard
      errors of the population functional 0.348898. The standard error is the sample standard
      deviation of the $k$ log-excesses over $\sqrt k$. This checks the finite-threshold
      target, not the asymptotic index.
    - Exact GPD data ($\xi=0.25$, $\beta=1$). At the fitted parameters, the score (gradient
      of the log-likelihood) is below $10^{-6}$ in each component. The log-likelihood is no
      lower than that of `scipy.stats.genpareto.fit` with location 0, less $10^{-8}$. This
      avoids comparing two optimisers' parameters. *Corrected (L2 freeze).* The mean fitted
      shape over 500 replications of $k=250$ is reported under Diagnostics, not tested here.
    - For a Pareto tail, whose excesses are exactly GPD above any threshold, the
      peaks-over-threshold VaR and ES formulas at the true parameters reproduce the closed-form
      quantile and ES to $10^{-10}$.
  - Diagnostics (reported, with no pass threshold):
    - Maximum-likelihood shape bias (*moved here at the L2 freeze*): the mean fitted shape over
      500 exact-GPD replications of $k=250$, its standard error and its difference from 0.25.
    - Finite-threshold bias. On the $n=5{,}000$ sample, $H_k$ and the GPD shape are reported
      against both 0.25 and their population values at the threshold. The 99.5 percent VaR
      and ES are reported against the closed form, and against the values implied by the
      population GPD fit at $u$.
    - Bootstrap coverage. Percentile intervals use 1,000 resamples (fixed seed). The coverage
      of Hill's 95 percent interval over 200 independent samples (fixed seeds) is reported
      for both 0.348898 and 0.25. For the GPD, the single-sample interval is reported.
    - Threshold sensitivity. Hill and the GPD shape are reported at the 90, 95, 97.5 and 99
      percent thresholds, a list fixed in advance, each beside its population functional.
  - The annual Damodaran file (98 observations, 1928-2025) is not suitable and is not used.
    No empirical claim is made unless a daily series with stated source, dates and licence is
    added (backlog B9).
  - Seeds, the threshold list and the cutoff $k$ are written into the script before its first
    run. A failed correctness check is diagnosed, not rerun with another seed or threshold.
  - Objective (1, possibly 2): estimate tail risk by extreme value methods (GPD and Hill;
    VaR and ES), including the two-step filtered method. Split into two objectives only if the
    two-step method proves to be a separate idea.

- **P11 New ideas found by C0** (decision L2-D2). These are three small entries, unrelated to
  each other.
  - **P11a** `meth:correlation-independence-tests` (`common-toolkit/statistical-inference.tex`,
    after `meth:nonparametric-tests`).
    - Content: the $t$-test of zero correlation, $t=r\sqrt{n-2}/\sqrt{1-r^2}$ with $n-2$
      degrees of freedom; Spearman's rank correlation and its test, with ties; the chi-square
      test of independence on a contingency table, with expected counts and $(r-1)(c-1)$
      degrees of freedom. The quant use is the significance of an information coefficient and
      a rank IC, with the caveat about overlapping observations.
    - Sources: `introductory-statistics-2023` (OpenStax, registered). Its sections on the
      significance of the correlation coefficient and the test of independence are to be
      located and read. `statistical-methods-handbook` (NIST, registered) is checked for rank
      correlation. The 2026/2027 outlines dropped this module, so no outline item maps to it.
    - Checks:
      - Size: 20,000 replications of independent normal pairs with $n=30$ (fixed seed). The
        5 percent Pearson and Spearman tests reject in $5\pm0.5$ percent of replications.
      - The $t$-test $p$-value equals `scipy.stats.pearsonr` to $10^{-12}$.
      - Spearman equals Pearson on midranks to $10^{-12}$, and equals `scipy.stats.spearmanr`,
        on data with and without ties. *Corrected (L2 audit).* It is unchanged to $10^{-12}$
        by a strictly increasing transform of either variable. A strictly decreasing
        transform of one variable changes only its sign, and of both leaves it unchanged.
        Strict monotonicity preserves ties, so these hold with ties too. A non-strict
        (weakly) monotone transform can create ties and change the value, and is not tested.
        With ties, the shortcut $1-6\sum d_i^2/(n(n^2-1))$ differs from Pearson on midranks,
        and the entry says so. The tied fixture shows the difference.
      - The chi-square statistic equals `scipy.stats.chi2_contingency` (without continuity
        correction) to $10^{-12}$.
    - Objective (1): test whether a correlation is zero, parametrically and by ranks, and test
      independence in a contingency table.
  - **P11b** `meth:mean-cvar-optimisation`
    (`portfolio-construction-risk/portfolio-construction-models.tex`, after
    `mod:mean-variance-portfolio-optimisation`).
    - Content: minimising CVaR at a target return as a linear programme over scenarios
      (Rockafellar-Uryasev); why the allocation changes when returns are skewed or fat-tailed;
      the scenario count needed.
    - Source: `s6-cvar` (catalogue; open author PDF, to be obtained and read). If it cannot be
      read, the package stops with `obtain-source`.
    - Problem, fixed in advance (*corrected, L2 audit*):
      - CVaR of the portfolio loss $L=-R^\top w$ at confidence $\alpha=95$ percent.
      - Constraints: long-only ($w\ge0$), fully invested ($\mathbf 1^\top w=1$), and the
        expected return equal to the target ($\mu^\top w=\mu^*$, an equality, not $\ge$).
      - The empirical CVaR is the existing fractional-tail-mass definition of
        `meth:var-es-estimation-methods`: the average of the worst $n(1-\alpha)$ scenario
        losses, with a fractional weight on the last when $n(1-\alpha)$ is not an integer.
        For equally weighted scenarios, the minimum over $\zeta$ of the Rockafellar-Uryasev
        function $\zeta+\frac1{n(1-\alpha)}\sum_j(L_j-\zeta)^+$ equals this.
    - Checks (scipy `linprog`, no new dependency):
      - The LP objective equals that empirical CVaR of the optimal weights, computed
        directly, to $10^{-8}$. This holds both at $n=10{,}000$ ($n(1-\alpha)=500$) and in a
        case where the tail mass is not an integer: $n=250$ at 97.5 percent, tail mass 6.25.
      - For three assets, no weight on a 1 percent simplex grid that meets the target has a
        lower CVaR, allowing for the grid step.
      - Normal equivalence at an equal expected return. Three assets have
        $\mu=(4,6,8)$ percent, volatilities $(10,15,20)$ percent, all correlations 0.3 and
        $\mu^*=6$ percent. Scenarios are jointly normal, with the sample mean shifted to
        $\mu$ exactly, so both problems face the same return constraint. The benchmark is
        the population mean-variance solution under the same three constraints, where the
        minimum CVaR and the minimum variance coincide because CVaR is
        $-\mu^\top w+\sigma_w\,\varphi(z_\alpha)/(1-\alpha)$. Over seeds 0-9 (fixed), the
        largest absolute weight difference must be at most 0.025 at 100,000 scenarios. Its
        mean over the seeds must be lower at 100,000 than at 10,000. A planning reproduction
        gave a maximum of 0.048 at 10,000 and 0.009 at 100,000. The tolerance is set from the
        $n^{-1/2}$ rate, not tuned, and is binding.
      - Negative skew (*corrected, L2 audit*): with one asset given a negatively skewed
        return of the same mean and variance, the change in its mean-CVaR weight relative to
        mean-variance is reported and explained (tail contribution to CVaR against
        diversification). It is not a pass condition. Lower CVaR does not imply a lower
        weight in general, and no fixture establishing the direction is fixed in advance.
    - Objective (1): construct a minimum-CVaR portfolio and compare it with mean-variance.
  - **P11c** `meth:margin-purchase-leverage` (`portfolio-risk-financing/securities-lending.tex`,
    after `mech:securities-lending-short-sale`).
    - Content: buying on margin; the leverage ratio $1/m_0$; the levered total return after
      financing, income and commissions; the margin-call price
      $P^*=P_0(1-m_0)/(1-m_m)$ for a long position and $P_0(1+m_0)/(1+m_m)$ for a short one.
    - Sources: `ecfr-12cfr220` (Regulation T, sec. 220.12) and `finra-rules-2026` (Rule 4210),
      both registered; their current texts are reread with retrieval dates (Section 5, step 3).
    - *Corrected (L2 audit): assumptions.* The two static formulas assume the loan (for a
      long position) or the credit balance (for a short one) is unchanged since the
      purchase: no interest, fees, dividends, coupons or other cash flows. The entry states
      this. When those flows occur, the call price is computed from the balance at the date.
      For a long position, $P^*=L_t/\big(N(1-m_m)\big)$, with the loan $L_t$ including
      accrued interest and fees and net of income credited. For a short one,
      $P^*=K_t/\big(N(1+m_m)\big)$, where the credit balance $K_t$ includes the sale proceeds
      and margin deposited, plus any interest rebate, less dividends owed to the lender and
      fees.
    - Checks (deterministic, original inputs):
      - Static case: both margin-call prices equal a numerical root of the equity-to-value
        condition to $10^{-12}$.
      - With financing: an example with financing interest, a commission and a dividend
        recomputes $L_t$ or $K_t$ from a dated cash-flow ledger. The balance formula equals a
        numerical root of the same condition to $10^{-12}$, and differs from the static
        formula by an amount that is reported.
      - The levered-return identity equals the cash-flow computation to $10^{-12}$.
    - Objective (1): calculate the leverage ratio, the levered return and the margin-call price
      for long and short margin positions.

**Acceptance and stopping.** As for Batch L1 (Section 6): per-package focused checks and
records, then `make source-check`, `make pdf` with inspection of the new pages, `make
pre-commit`, and a completion report with the sources actually read and the shortfall against
45. The stop rules are the same. In addition, a package whose essential source cannot be read
in its current or authorised form records its objective as `partial` with `obtain-source`, and
the other packages continue.

**Estimated size against the 45-objective preference.** About 11 newly covered objectives
(10-12), a shortfall of about 34 (33-35). With P10, about 12. The estimate before C0 was 8-9
(P6-P9). The reason is the evidence, not
the method. C0 used all 15 candidate reviews and found three new ideas in the curricula. Most
of the other gaps are depth within covered objectives, which earn no count. Nothing is padded
to approach 45.

**Excluded from Batch L2.**
- C0 depth gaps placed in the backlog (B12-B17).
- P10 (by default Batch L3; decision L2-D4).
- B1-B10 unchanged.
- Calibrating Hull-White to cap or swaption volatilities: no data are held.
- An empirical EVT illustration (B9).
- LIBOR-era CQF and Gregory material, except as dated context (B8).
- Any curriculum or workbook citation: the citation policy of Section 2 is unchanged, and
  Batch L2 needs no exception.

### Batch L2 proposal audit corrections (2026-10-21)

An audit of the C0 proposal found criteria that would not have tested what they claimed. They
are corrected in place above, marked "Corrected (L2 audit)". The original wording is kept
here for the record. The values below were reproduced in the scratchpad before the
correction; the package scripts recompute them. The scope, objective count, the 15-candidate
C0 boundary and its unexamined items (Section 8.1) and the source restrictions are unchanged.

| Package | Original wording | Problem | Correction |
|---|---|---|---|
| P9 | "the GPD and Hill estimates' 95% bootstrap intervals cover 0.25, and the 99.5% VaR is within 10% of the truth"; "the threshold … is the 95th percentile" | Student $t_4$'s $\xi=0.25$ is asymptotic. At the 95th percentile, the population Hill functional is 0.348898 and the KL-best GPD shape is about 0.192, so the test mixed estimator bias with correctness. Hill's cutoff was not stated. | Cutoff $k=n/20$ fixed. Pass or fail only on known-truth benchmarks (exact Pareto and GPD data, the finite-threshold functional at $n=10^6$, exact POT formulas). Bias, bootstrap coverage and threshold sensitivity are reported diagnostics. Seeds and thresholds are fixed before the first run. |
| P7 | "With exposure independent of default and a constant $R$, this becomes $(1-R)\sum_i\mathrm{EE}^*(t_i)\mathrm{PD}$" | Under stochastic rates, the factorization needs $\tau$ independent of the discounted exposure $D(0,t)E(t)$. | Condition stated, with a sufficient joint-independence assumption and the forward-measure form. |
| P7 | "Collateral with a 10-day margin period of risk lowers EE at every date" | False for two-way lagged collateral when the bank has posted. | Direction, timing, accrual and MPR mechanics defined. Only model-implied properties are checked (pathwise bounds, the one-way variant, and $t<\delta$). The Gaussian-increment comparison is a diagnostic. |
| P11b | "agree within a tolerance fixed in advance"; "With one negatively skewed asset, the mean-CVaR weight on it is lower" | No confidence level, constraints or equal-return basis. The direction of the skew effect is not guaranteed. | $\alpha=95\%$, long-only, fully invested, equality return target, mean-matched scenarios, tolerance 0.025 at 100,000 over seeds 0-9. The empirical CVaR is the fractional-tail-mass definition. The skew effect is a reported result. |
| P11a | "unchanged by a monotone transform" | Ambiguous: decreasing transforms flip the sign, and the shortcut formula fails with ties. | Strictly increasing invariance, sign change under strictly decreasing transforms, midranks for ties. |
| P11c | Static margin-call formulas only | They assume an unchanged loan or credit balance. | Assumption stated. Separate ledger-based example with financing, fees and a dividend. |
| P6 | "exact Ornstein-Uhlenbeck steps" for simulated discount factors | Exact rate samples do not give an exact $\int r\,du$. | Joint exact sampling of the rate and its integral; trapezoid bias diagnostic; 4 standard errors for the 30-maturity family. |
| P8 | "within 3 standard errors plus a granularity allowance" | The allowance was not predetermined. | Exact finite-pool benchmark (conditional binomial). Granularity is reported as a deterministic gap that must shrink from 250 to 1,000 names. |

### Batch L2 freeze corrections (2026-10-21)

The owner froze Batch L2 with decisions L2-D0 to L2-D6 (Section 10.3) and authorised two
bounded criterion corrections, made before any L2 script was written. Both counterexamples were
reproduced in the session scratchpad before the edit. No seed, input or other tolerance was
changed, and no threshold was tuned. The corrected text above is marked "Corrected (L2 freeze)".

| Package | Original wording | Problem | Correction |
|---|---|---|---|
| P8 | "the deterministic gap between the large-pool and exact finite-pool values is reported for $N=250$, 500 and 1,000. Its absolute value must decrease in $N$ for each tranche." (and, in the L2 audit table, "Granularity is reported as a deterministic gap that must shrink from 250 to 1,000 names") | Not implied by the model for thin tranches. With $\mathrm{PD}=0.02$, $\rho=0.3$, LGD 0.6 and a 0.2-2 percent tranche, the gaps in pool-loss units are about $6.227824\times10^{-6}$, $1.0586963\times10^{-5}$ and $5.082963\times10^{-6}$ at 250, 500 and 1,000 names: they rise, then fall. | Gaps reported per tranche, not tested. The independent conditional-binomial finite-pool benchmark, its quadrature convergence and the 1,000-name Monte Carlo comparison remain binding. |
| P9 | "Over 500 replications of $k=250$, the mean shape is within 3 standard errors of 0.25, which allows for the $O(1/k)$ bias of maximum likelihood." | Three standard errors of the replication mean do not allow for finite-sample MLE bias, which does not shrink with the number of replications. Reproduction: NumPy `default_rng(20261021)`, 500 successive `genpareto.rvs(c=0.25, scale=1, size=250, random_state=rng)` samples, each fitted with `floc=0`: mean shape 0.237276, error 0.012724 against 3 s.e. 0.010503. | Mean shape moved to Diagnostics. The score and likelihood checks, the exact-Pareto Hill checks and the exact tail-formula checks remain binding. |

The rest of the L2 audit table above is unchanged and kept as written.

### Batch L2 post-implementation audit corrections (2026-10-21)

An audit of the committed Batch L2 (`cd55096`) found that its passing checks (eight scripts with warnings as errors, 36
tests, lint, formatting, both checkers) missed three P7 discounting and units defects and one P11c rule-scope
statement. The owner authorised a bounded correction pass. No seed, input or existing tolerance changed; no frozen
criterion was altered; the eleven objectives are unchanged. Original results are kept in
`notes/source-review-records.md` (*Post-implementation audit corrections, Batch L2*), with the corrected values and the
reasons the earlier checks passed.

| Finding | Problem | Correction |
|---|---|---|
| L2-F1 (P7 script) | $D(0,t)=P(0,t)e^{+\mathrm{Var}(I)/2-I}$ overstated each discount factor by $e^{\mathrm{Var}(I)}$ (up to 0.29%); only a Monte Carlo check at 4 s.e. used it. | Sign corrected from the mean short-rate integral; deterministic checks (quadrature of $\int\alpha$; propagated exact-step variance and $E[D]=P$) reject the old sign. CVA 0.0600863777 and 0.0066079387, gap 0.0461283797 (were 0.0601229105, 0.0066095777, 0.0444617598). |
| L2-F2 (`def:wrong-way-risk`) | $E[E(t_i)\mid\tau=t_i]$ with undiscounted $E$ inherited Gregory's discounted EE (eq. (17.1), p. 380; p. 311). | Conditions $D(0,t_i)E(t_i)$ on $t_{i-1}<\tau\le t_i$; convention mapped; PV CVA example 2.8536882735 against 3 checked. |
| L2-F3 (`meth:credit-valuation-adjustment`) | EPE $\times$ spread presented without units. | Gregory sec. 14.2.5, p. 313: a per-annum spread (4.62 bp) against 0.200% upfront, converted by the risky annuity 4.42 (4.52 bp); checked. |
| L2-F4 (`meth:margin-purchase-leverage`) | 150% stated for any non-exempted short sale. | Stated for the unhedged non-exempted equity short of the examples; 220.12(c)(2) and (d) given, from the retained eCFR text. No number changed. |

### Batch L3 (frozen 2026-10-21): P10, regulatory and disclosure currency (backlog B7)

Frozen by the owner's instruction of 2026-10-21 and executed in the same session, on branch
`codex/library-gap-batch-l3` from `a519e0c`; local only (no push, PR, merge, rebase or amendment).
Before the scope was written, the P8 row of "Batch L2 freeze corrections" was repaired: its
`\rho` and `\times` had been stored as a line break and tab characters, which split the table
row. Numbers and meaning are unchanged; this is formatting only.

**Scope.** Four strands, each verified against current primary texts (BIS/BCBS, EU legislation
and official EU institutions, PRA/Bank of England, US banking regulators and the Federal
Register, IFRS Foundation/ISSB, FSB, SEC and official court documents). Search results and
generated summaries are discovery aids only; every cited claim rests on a substantive passage
read in the issuer's text, saved where possible under the git-ignored
`reading_materials/library-gap-l3-20261021/`.

1. *FRTB.* The Basel standard (MAR, with its effective date) separately from implementation in
   the EU, the UK and the US. Review `meth:market-risk-limits-capital` and correct wording
   that implies uniform implementation.
2. *Counterparty capital.* SA-CCR (CRE52) and the revised CVA-risk framework (MAR50) in the
   current Basel chapters, and their EU, UK and US status. Distinguish exposure measurement,
   default-risk capital and CVA-risk capital. At most one new `rule:` entry, in
   `corporate-credit-capital/counterparty-xva.tex`, if the reading shows a distinct idea; its
   small checked example only if needed to teach the formula (deterministic, original inputs,
   numpy/scipy only).
3. *Sustainability disclosure.* IFRS S1/S2 (issuance and effective dates), the TCFD-to-ISSB
   transition, and the SEC climate rule's status (adoption, stay, litigation). Issuance and
   effective dates are kept apart from jurisdictional adoption. Adoption comparisons are limited
   to the EU, the UK and the US. Entry: `meth:esg-exposure-evaluation` (Conditions).
4. *Liquidity.* The LCR and NSFR statements and dates in
   `financial-statement-analysis/financial-institution-analysis.tex`
   (`def:financial-institution-features`), Basel standards against national implementation.

**Record for each material claim** (in `notes/source-review-records.md`): issuer and exact
locator; jurisdiction and affected institutions; publication, effective or application, and
retrieval dates; status (proposed, final, effective, transitional, delayed, stayed or withdrawn);
the entry affected and the correction made, or confirmation that none is needed. Conflicting
dates are resolved by the controlling text and later official amendments; a press release is not
evidence of implementation and a proposal is not law. An essential source that cannot be read is
recorded as the precise unverified claim, and independent work continues.

**Limits.** Extend existing entries first; no new chapter, regulatory calculator framework or
dependency. Retrieval diaries and verification details stay out of the teaching text (Conditions
give the "as of" dates only). No other backlog item; the L1 and L2 mathematical audits are not
reopened without new evidence. Library read-only; citation policy unchanged.

**Objectives.** Only genuinely new ones count. FRTB, liquidity and sustainability are currency
corrections to covered objectives (`objective:set-market-risk-limits`,
`objective:explain-financial-institution-features`, `objective:evaluate-esg-exposures`) and add
none. Regulatory counterparty capital has no objective; if its entry is written, one objective is
added (`topic:credit-models`, planned batch 8). Expected: 0-1 new, a shortfall of 44-45 against
45, reported without padding.

**Acceptance.** Every material claim recorded as above; affected entries corrected or confirmed;
reading notes, `sources.tex`, entry evidence, coverage, pathways and plan status updated; any new
script passes with warnings as errors; unaffected numerical evidence reused with its reason;
`make lint`, `make format-check`, `make check-compendium`, `make check-coverage` and `make test`
pass; `make pdf` builds with no overfull boxes or undefined references, and the changed pages are
rendered and inspected; pre-commit passes on the committed files, new ones included; one new local
commit.

**Outcome (2026-10-21).** All four strands done; every material claim is tabulated in the review record with issuer,
locator, jurisdiction, dates, status and entry outcome. One new entry and objective (counterparty capital), with a
deterministic checked example; three entries corrected or extended; the other claims confirmed. Two sources could not
be read (FCA PS26/19; Eighth Circuit orders after 18 May 2026) and are recorded as unverified; the teaching text does
not depend on them.

### Batch L3 post-implementation audit corrections (2026-10-21)

An audit of the committed Batch L3 (`440272b`) found five statements that its passing checks (the new script with
warnings as errors, 36 tests, lint, formatting, both checkers, the PDF build) did not test. The owner authorised a
bounded, fixes-only pass on `codex/library-gap-l3-audit-fixes`, branched from `440272b`. No objective was added, no
backlog batch started, and no existing number, input or tolerance changed. The Outcome above is kept as the record of
the first implementation; details are in `notes/source-review-records.md` (*Post-implementation audit corrections,
Batch L3*).

| Finding | Problem | Correction |
|---|---|---|
| L3-F1 (`rule:counterparty-credit-cva-capital`) | Printed unmargined MF $\sqrt{\min(M,1)}$ without the ten-business-day floor (the script had it). | Floor restored from CRE52.48-52.49 (10/250 years). Counterexample checked: five business days give 0.2, not 0.141. Four-year example unchanged. |
| L3-F2 (same entry) | $M\,\mathrm{EAD}\,\mathrm{DF}/\alpha$ called "the same object as $\mathrm{EE}^*$". | Per MAR50.15 nn. 3-4, a supervisory proxy for the area under the discounted EE profile, in currency times years, against $\mathrm{EE}^*(t)$ in currency at a date. Checked: 13.8225 currency-years against EEPE 3.8127. |
| L3-F3 (`meth:esg-exposure-evaluation`) | Directive 2026/470 Art. 2(1) cited for the reporting scope; the new thresholds implied to apply already. | Art. 2(4)-(5) (individual, consolidated), 2(13) (third-country), 3(1) (FY 2024-2026 first wave; optional FY 2025-2026 exemption), 5(1) (transposition by 19 March 2027); FY 2027 start from Directive 2025/794 and FY 2028 third-country start from CSRD Art. 5(2). |
| L3-F4 (`def:financial-institution-features`) | US NSFR said to apply at \$100bn of assets. | 12 CFR 249.1(b)(1): Category IV only with \$50bn or more of weighted short-term wholesale funding; 249.105(b): 100, 85 or 70 percent. |
| L3-F5 (`meth:market-risk-limits-capital`) | EU 0.9 multiplier applied to "the standardised requirements". | CRR Art. 495s(1)-(2): the sensitivities-based method result and the simplified standardised approach only. |

Source gaps closed: FCA PS26/19, read from the Internet Archive capture of the FCA's PDF (7 October 2026). Its final
comply-or-explain Listing Rules apply to accounting periods from 1 January 2027 and are stated separately from the
voluntary UK SRS endorsement. Eighth Circuit: the order of 21 May 2026 (abeyance kept) and the order of 5 October 2026
(next SEC status report by 31 December 2026). The court posture is dated 5 October 2026, the last filing found.

### L3 wording correction (2026-10-21)

Authorised with the L4 proposal and made on `codex/library-gap-l4-proposal` (from `517213d`). The EU timing item of
`meth:esg-exposure-evaluation` described the 2024-2026 first wave only as large public-interest entities with more than
500 employees. CSRD Art. 5(2), first subparagraph, point (a) has two cases: (i) large public-interest entities above 500
employees and (ii) public-interest entities that are parents of a large group above 500 employees on a consolidated
basis (retained OJ text, `reading_materials/library-gap-l3-audit-20261021/eu-32022L2464.html`, SHA-256
`6ad8df8d…d6c29837`). Directive 2025/794 Art. 1 amends only points (b) and (c); Directive 2026/470 Art. 3(1)(a)(i)
replaces only the introductory dates of point (a). Both cases therefore stand for FY 2024-2026. The item now names both
and cites CSRD Art. 5(2)(a)(i)-(ii); the exemption sentence cites Directive 2026/470 Art. 3(1) explicitly. Updated with
it: the two CSRD reading notes, the entry evidence, the objective's CSRD locator and example note, and the review record.
No number, objective or other timing qualification changed; the L3 records above are kept as written.

### Proposed Batch L4 (2026-10-21; awaiting owner freeze): Monte Carlo Greeks, seasoned variance swaps, cross-currency basis swaps

*Kept as the proposal record. Frozen with corrections L4-C1 to L4-C3 on 2026-10-21; see "Batch L4 freeze corrections
and frozen specification" below, which binds where the two differ.*

Investigation only. No entry, script, reading note or coverage record has been written for L4. Sources were read on
21 October 2026; copies are in the git-ignored `reading_materials/library-gap-l4-20261021/` (and Hull in
`reading materials/`). Delegation to the models named by the implementation skill was unavailable; the work was done
directly.

**Sources actually read.**

| Source | Identity, copy and locator convention | Passages read | Limits |
|---|---|---|---|
| Hull, OFOD 11th Global ed. (`s7-hulloptions`) | Git-ignored copy in `reading materials/`, SHA-256 `8bc6e2f0…b482`; printed page = PDF page | Sec. 21.6 "Calculating the Greek letters", pp. 494-495; sec. 26.16, pp. 629-631 (variance and volatility swaps, eqs. (26.6)-(26.9), Examples 26.4-26.5); sec. 7.10, pp. 192-193 (fixed-for-floating and floating-for-floating currency swaps: the initial principal exchange runs opposite to the interest payments and the final one in the same direction; decomposition into a fixed-for-fixed swap and two interest-rate swaps); sec. 34.3, pp. 776-777 (valuation by forward rates realised, each leg on its own curve); sec. 7.13, p. 194 (single-currency basis swaps) | MC Greeks only by bump-and-revalue with common random numbers; variance swaps valued at inception only, discounted at $e^{-rT}$; realised volatility with $252/(n-2)$ and a zero mean ("sometimes $n-1$"); $L_{\text{var}}=L_{\text{vol}}/(2\sigma_K)$; no quoted cross-currency basis, no sign convention for it |
| Broadie and Glasserman (1996), "Estimating Security Price Derivatives Using Simulation", *Management Science* 42(2), 269-285, DOI 10.1287/mnsc.42.2.269 | Not in the catalogue; register a neutral key when first cited. Columbia Business School copy (`business.columbia.edu/sites/default/files-efs/pubfiles/1848/estimating.pdf`), a 17-page ProQuest scan of the published article with no text layer, read as page images; SHA-256 `247d7319…e1304`; locators are journal pages | Pp. 269-275 (sec. 1; sec. 2: pathwise eqs. (4)-(9), likelihood ratio eqs. (10)-(16), sec. 2.3 scope; sec. 3 second derivatives, eq. (18); sec. 4 resimulation, sec. 4.1 Example 1 discussion); pp. 280-281 (control variates eq. (23), sec. 5, App. A conditions (A1)-(A4) and Proposition 1, App. B choice of $h$, eq. (26)) | Pp. 276-279 (Tables 1-3, Asian and stochastic-volatility examples) and Apps. C-D not read; the 1.5-4 times larger LR standard errors are quoted from the text of p. 275, not the table. Discontinuous payoffs are treated only through condition (A3) and the "continuous payoff" rule of thumb (p. 272); no digital example is given |
| Demeterfi, Derman, Kamal and Zou, "More Than You Ever Wanted To Know About Volatility Swaps", Goldman Sachs Quantitative Strategies Research Notes, March 1999 (catalogue key `wide-demeterfi-varswaps` is the *J. Derivatives* 6(4) 1999 version) | Author-hosted copy (`emanuelderman.com/wp-content/uploads/1999/02/gs-volatility_swaps.pdf`), 56 PDF pages with text layer; SHA-256 `ad289770…f762223e`; printed page = PDF page $-4$. Cite the catalogue key with a version note, since GS pages differ from the journal's | Pp. 1-3 (volatility and variance swap payoffs, EQ 1-2, quoting in vol points squared, the contract choices: source and frequency, annualisation factor (260 days as example), zero-mean against mean-subtracted); pp. 12-13 (imperfect strikes; variance vega falls linearly with time, "proportional to the remaining variance $\sigma^2\tau$"); pp. 15 and 18-19 (EQ 13-17: continuous realised variance $V=\frac1T\int_0^T\sigma^2dt$, value $e^{-rT}E[V-K]$, fair strike; EQ 26, the strip formula); pp. 29-30 (EQ 35-39, daily log-payoff accumulation, "variance is additive", jump error) | No seasoned-swap valuation formula is printed; the mid-life value is a labelled derivation from EQ 14-16 and additivity (decision L4-D2). The *J. Derivatives* version was not read |
| Borio, McCauley, McGuire and Sushko (2016), "Covered interest parity lost: understanding the cross-currency basis", *BIS Quarterly Review*, September 2016 (`cur-borio-mccauley-mcguire-sushko-2016`) | BIS PDF (`bis.org/publications/covered-interest-parity-lost-understanding-cross-currency-basis_1.pdf`), SHA-256 `32dce4f0…a2928`; printed page = PDF page $+44$ | Pp. 45-48: introduction, Graph 1 (three-month and three-year bases against the dollar, 2006-2016), the framework section and Box A (CIP with $S$ in dollars per foreign unit; FX swaps quoted in forward points; cross-currency basis swap with Libor legs, principals re-exchanged at the initial spot; the one-period relation with $b$ added to the dollar leg; bid-ask and credit causes) | LIBOR era. Two sign conventions in one paper: Box A adds a positive $b$ to the **dollar** leg, while the text and Graph 1 report the basis as **negative** when dollars are dear through swaps (the foreign-leg convention of `ev:cip-deviations`). Pp. 49-58 (cross-section, yen time series, regressions) not read |
| Ding, Liu and Rutkowski, "Multi-Curve Approach to Cross-Currency Basis Swaps Referencing Backward-Looking Term Rates", arXiv:2410.08477v3 (final revision 30 October 2025; catalogue key `w4-ding-rutkowski-ccbs` is the *SIAM J. Financial Math.* 17(2) 2026 version) | arXiv PDF, 50 pages, SHA-256 `3f4eed42…f049f2`; locators are arXiv pages. Cite with a version note | Pp. 1, 4 (abstract: the LIBOR-to-RFR transition; constant-notional and mark-to-market CCBS named as market variants); pp. 6-7 (Definition 2.4: constant-notional CCBS cash flows, principals exchanged at $T_0$ and re-exchanged at $T_n$ with $P^d=Q_{T_0}P^f$, basis spread $\kappa$ on the domestic (AUD) leg, compounded backward-looking rates); p. 38 (example: 3-year non-MTM CCBS, receive six-month compounded SOFR, pay six-month averaged AONIA plus a spread, semi-annual) | Model sections (3-6) not read and not needed. One currency pair's example; it does not establish a market-wide quoting rule or the MTM-reset mechanics |

**Evidence reused (not reread).** `ev:cip-deviations` already defines the basis on the foreign leg after Du, Tepper and
Verdelhan (eqs. (3)-(4), printed p. 9), so the L4 sign convention agrees with an entry in the compendium.
`meth:swap-valuation-replication` already holds Hull's fixed-for-fixed currency swap (secs. 7.8-7.9, pp. 186-192, checked
in its script). `meth:monte-carlo-simulation` already holds the inputs (S 100, K 105, 20 percent, 3 percent, one year;
closed form 7.1281) and the common-random-numbers point.

**Planning values.** The numbers below come from one exploratory script in the session scratchpad (NumPy
`default_rng(20261021)`), not from repository evidence. They show that each check is feasible with margin; the package
scripts recompute them and the acceptance criteria, not these values, are binding.

#### L4-a (B3). Monte Carlo Greeks: pathwise and likelihood-ratio estimators

*Gap.* `meth:monte-carlo-simulation` estimates values, standard errors, control variates and discretisation bias; no
entry estimates a sensitivity by simulation. `meth:greeks-delta-gamma-hedging` and `mod:black-scholes-merton` give
closed-form Greeks, and `option-pricing.tex` checks them by finite differences of the closed form, not of a simulation.
Nothing explains why a direct estimator is unbiased, when it fails, or why resimulation is biased. **New idea; new
entry** `meth:monte-carlo-greeks` in `volatility-options/numerical-methods.tex`, after `meth:least-squares-monte-carlo`,
with one-line See also links from `meth:monte-carlo-simulation` and `meth:digital-option-valuation`.

*Teaching content.* Resimulation with common random numbers and its bias-variance trade-off in $h$ (Hull pp. 494-495;
Broadie-Glasserman p. 274 and App. B, eq. (26)). Pathwise: differentiate the discounted payoff along the path,
$e^{-rT}\mathbf 1\{S_T>K\}S_T/S_0$ for delta and $e^{-rT}\mathbf 1\{S_T>K\}S_T(-\sigma T+\sqrt T Z)$ for vega (eqs.
(5)-(9)), valid under (A1)-(A4) (Lipschitz payoff; p. 281). Likelihood ratio: weight the payoff by the score of the
density, $Z/(S_0\sigma\sqrt T)$ for $S_0$ and $(Z^2-1)/\sigma-\sqrt T Z$ for $\sigma$ (eqs. (14)-(16), rewritten in $Z$
as an Interpretation); it needs no payoff smoothness but the parameter must enter the density, so strike sensitivity
needs the pathwise method (p. 272); its variance is larger (pp. 275, 280). Gamma: the pathwise second derivative of a
call collapses to the closed form (eq. (18)); not repeated as a check.

*Worked example (original).* The `meth:monte-carlo-simulation` call; 100,000 draws, fixed seed. Pathwise and LR delta and
vega against closed form (planning: pathwise delta 0.50101, s.e. 0.00188, exact 0.50241; LR delta s.e. 0.00403; vega
39.505 and 38.920 with s.e. 0.233 and 0.763 against 39.894). A cash-or-nothing digital paying 1 at $K=105$: every
pathwise delta sample is exactly zero though the true delta is $e^{-rT}n(d_2)/(S_0\sigma\sqrt T)=0.018997$; LR gives
0.018861 (s.e. 0.000090); resimulation with common random numbers gives s.e. 0.000426 at $h=1$ and 0.004447 at $h=0.01$.

*Checks (new `notes/artefacts/numerical-pricing/monte-carlo-greeks-check.py`, numpy and scipy only).*
1. Independent derivatives of the estimator building blocks, deterministic: $dS_T/d\sigma$ and $dS_T/dS_0$ against
   central differences of the path map on fixed $Z$; both scores against central differences of the lognormal
   log-density at several $x$ (planning agreement about $10^{-9}$ relative). This catches sign and factor errors that a
   Monte Carlo tolerance would hide.
2. Each of the four call estimators within 4 standard errors of the closed form (seed and path count fixed and
   reported; no reseeding).
3. Digital: the pathwise estimator is identically zero on every path (exact), which differs from the positive closed
   form; the LR estimate is within 4 standard errors of it.
4. Reported, not binding: LR to pathwise standard-error ratios; resimulation bias and standard error at $h=1$ and
   $h=0.01$ for the digital (the variance grows roughly as $1/h$).

*Objective.* Genuinely new: `objective:estimate-greeks-by-simulation` ("Estimate option sensitivities by pathwise and
likelihood-ratio Monte Carlo estimators and explain when each fails"), `topic:option-valuation`, `planned_batch` 9,
prerequisites `objective:apply-monte-carlo-simulation` and `objective:manage-option-greeks`. **+1.**

#### L4-b (B12). Valuing a variance swap during its life

*Gap.* `def:vix-variance-dividend-swaps` gives the payoff, vega notional and variance units at expiry (Gliner);
`meth:volatility-derivative-applications` gives the inception value by option replication (Hull eq. (26.6), Example
26.4) and says realised-variance definitions are contractual. Neither values a seasoned swap, separates realised from
remaining implied variance, or states the observation weights and annualisation that the split needs. **Depth within a
covered objective: extension** of `meth:volatility-derivative-applications` (a paragraph in Statement, one Practice item,
one Pitfall), not a new entry.

*Teaching content.* With $N$ return observations in the contract, $n$ already observed, annualisation factor $A$ (for
example 252) and zero-mean realised variance $\sigma^2_{0,t}=\frac{A}{n}\sum_{i\le n}r_i^2$, the expiry variance is
the observation-weighted sum $\frac nN\sigma^2_{0,t}+\frac{N-n}{N}\sigma^2_{t,T}$ (Demeterfi pp. 15 and 30: realised
variance is a time integral and additive). The swap's value to the variance receiver at $t$ is
$N_{\text{var}}\,P(t,T)\bigl[\frac nN\sigma^2_{0,t}+\frac{N-n}{N}K_{t,T}-K_{\text{var}}\bigr]$, all in the same
variance units (for example points squared). $K_{\text{var}}=K_{\text{vol}}^2$ is the contract's variance strike and
$K_{t,T}$ today's fair variance strike for the remaining period from the option strip (Demeterfi EQ 15-16 and 26 applied at $t$; Hull eq. (26.7)), expressed on
the contract's annualisation, and $P(t,T)$ discounts from expiry, since the payoff is paid then. This is a labelled
**Interpretation**: a derivation from the cited definitions, not a formula printed in the sources read (decision
L4-D2). Notional conventions: vega notional $=2K_{\text{vol}}\times N_{\text{var}}$ with $K_{\text{vol}}$ in vol points (Hull p. 629; Gliner in
`def:vix-variance-dividend-swaps`); variance in points squared against decimal variance differs by $10^4$.

*Worked example (original).* Vega notional 100,000 at strike 20 (so $N_{\text{var}}=2{,}500$ per point squared); one
year, 252 observations, 126 observed with realised volatility 25; remaining fair strike 18 on the same 252-day basis; 4
percent continuously compounded for the remaining half-year. Value
$2{,}500\,e^{-0.02}(0.5\times625+0.5\times324-400)=182{,}562$ (planning).

*Checks (new script in `notes/artefacts/derivative-overlays/`, beside `overlay-checks.py`).*
1. Limits: at $n=0$ with $K_{0,T}=K$ the value is 0; at $n=N$ it is the undiscounted payoff
   $N_{\text{var}}(\sigma^2_{0,T}-K^2)$ (562,500 here).
2. Units: the same value in points squared and in decimal variance with $N_{\text{var}}\times10^4$ (exact).
3. Weights from data: the realised leg recomputed from an explicit synthetic daily return series with the contract
   formula; mean-subtracted and $n-1$ variants reported as contract alternatives, not substitutes.
4. Independent: under GBM with volatility 18 percent for the remaining 126 daily returns, the discounted mean terminal
   payoff of the full contract (realised part fixed) within 4 standard errors of the formula (planning 182,652, s.e.
   112). The small discrete-sampling drift term is stated, not tuned away.
5. Reported, not binding: the value with calendar-day weights (182/365) instead of observation weights, 181,552, as the
   size of the mismatch that the Pitfall describes.

*Objective.* Covered by `objective:use-volatility-derivatives`; no new objective. Coverage evidence and entry evidence
updated only. **+0.**

#### L4-c (B13). Cross-currency basis swaps: cash flows, the quoted basis leg, sign conventions and synthetic funding

*Gap.* `meth:swap-valuation-replication` values fixed-for-fixed currency swaps (principal exchanges included);
`meth:cross-forward-rates` derives CIP; `ev:cip-deviations` defines the basis and reports its size;
`meth:forward-commitment-risk-overlays` uses a cross-currency swap to hedge a foreign bond. None sets out the
floating-for-floating basis swap: who pays the spread, the principal exchanges at the initial spot, why a negative
foreign-leg basis means expensive synthetic dollars, or how the two published sign conventions map. **New entry** (one
idea, too long for the already four-instrument swap entry): `meth:cross-currency-basis-swaps` in
`volatility-options/forward-commitment-valuation.tex` after `meth:swap-valuation-replication`, linked from it, from
`ev:cip-deviations` and from `meth:cross-forward-rates`.

*Teaching content.* Constant-notional cash flows by party (Ding-Liu-Rutkowski Def. 2.4, pp. 6-7; Hull sec. 7.10, pp.
192-193, for the direction of the principal exchanges and the decomposition): exchange principals at $T_0$ at spot, pay one compounded RFR plus $\kappa$ and receive the other flat each period, re-exchange the same
principals at $T_n$. One-period relation in the foreign-leg convention, $F/S=(1+r_{\$}\tau)/(1+(r_f+\kappa)\tau)$ with
$S$ in dollars per foreign unit, mapped to BIS Box A's dollar-leg $b$ (p. 48) by
$b=\frac FS(1+r_f\tau)-(1+r_{\$}\tau)$; to first order $b\approx-\kappa$. Synthetic dollar funding (borrow the foreign
currency, swap into dollars) costs about $r_{\$}-\kappa$, above direct dollar funding when $\kappa<0$ (BIS pp. 45-46,
Graph 1, as Interpretation of the sign). Conditions: LIBOR-era evidence (BIS 2016; Du-Tepper-Verdelhan 2017) separated
from current RFR legs (SOFR and other compounded overnight rates; DLR); the leg carrying the spread is a term of the
contract, shown as such; mark-to-market notional resets are named, not taught.

*Worked example (original, current-convention legs).* EUR/USD at 1.10 dollars per euro; EUR 100 million against USD 110
million; one year; compounded SOFR 4.0 percent against compounded €STR 2.5 percent; $\kappa=-20$ basis points on the
euro leg. A cash-flow table by date and party for a three-year annual version with stated assumed fixings (cash flows
only, no multi-period valuation). One-period: CIP forward 1.116098, forward with the basis 1.118280; dollar-leg
equivalent $b=+20.33$ basis points; synthetic dollar rate 4.2033 percent against 4.0 direct (planning).

*Checks (new script in `notes/artefacts/derivative-overlays/` or the currency-markets artefact folder; numpy only).*
1. Signs and principals: per-party cash-flow table sums; the initial exchange runs opposite to each party's interest
   payments and the final one in the same direction (Hull p. 192); the receiver of the initial dollars repays them at $T_n$;
   initial and final exchanges use the same rate; with fixings at the assumed rates and $\kappa=0$ the one-period legs
   reproduce CIP exactly.
2. Convention mapping: the forward from the foreign-leg $\kappa$ equals the forward from the BIS dollar-leg $b$ under
   the mapping (exact); a negative $\kappa$ raises the synthetic dollar rate above the direct one.
3. Quote direction: the same deal with the quote inverted (euros per dollar) gives the reciprocal forward (exact), and
   entering the inverted quote unconverted changes the result (reported, as in the existing currency-swap Pitfall).
4. Principal exchange exposure: the value change of the final exchange alone for a spot move, reconciled with the
   fixed-for-fixed currency swap in `meth:swap-valuation-replication`.

*Objective.* Deeper treatment of `objective:value-swaps-by-replication` (currency swaps) and
`objective:apply-international-parity` (CIP); no new objective. **+0.** If the owner prefers the entry to carry its own
objective, it would be `objective:explain-cross-currency-basis-swaps` (+1); recommended against, since its operations
(describe, calculate, interpret) are those of the two covered objectives (decision L4-D3).

#### Scope, size, exclusions and dependencies

**Recommended scope.** L4-a, L4-b and L4-c as above: two new entries (`meth:monte-carlo-greeks`,
`meth:cross-currency-basis-swaps`), one substantive extension (`meth:volatility-derivative-applications`), and
cross-reference-only edits to `meth:monte-carlo-simulation`, `meth:digital-option-valuation`,
`meth:swap-valuation-replication`, `ev:cip-deviations` and `meth:cross-forward-rates`. Three new check scripts. No new
chapter or topic file.

**Expected new objectives: 1** (L4-a), 447/447 after the batch; **shortfall 44 against the standing 45**, reported
without padding. B12 and B13 are depth within covered objectives, and adding objectives for them would inflate the count.

**Deferred or excluded.**
- No candidate is deferred: each essential source was read. B12's seasoned-value formula rests on a derivation, not on a
  printed formula; if the owner rejects L4-D2, defer B12 until `w5-bossu-advanced-equity` or `wide-bennett-trading-vol`
  (catalogued, not held) is obtained and read.
- Excluded: mark-to-market (resetting) cross-currency swaps, multi-period basis-swap valuation and cross-currency
  discount curves (would need a curve framework and a source on the reset mechanics); quanto and diff swaps; volatility
  swaps beyond the existing Hull example; second-order MC Greeks beyond a sentence; Broadie-Glasserman's Asian and
  stochastic-volatility examples (pp. 276-279, not read); any empirical basis series or claim about the size of the
  basis after 2016 (none read); any general market statement about which leg carries the spread beyond the cited
  contracts.

**Dependencies.** None between packages; any order. Each depends only on existing entries named above. No new
dependency; the citation policy is unchanged (no curriculum source is cited). Two catalogue keys are cited in a version
other than the catalogued one (GS note; arXiv v3) and must carry version notes, as `dtv-cip-2017` does. Broadie and
Glasserman (1996) is registered in `compendium/front/sources.tex` with DOI, the Columbia URL and the retrieval date.

**Records at implementation.** Reading notes for the three new sources, Hull locators added to `s7-hulloptions.md`;
`sources.tex` (Broadie-Glasserman); entry evidence for the two new and one extended entry; `objectives.json` (one new
objective; evidence notes on the three covered ones); pathway links in `volatility-options.md` and the currency-markets
note; a review record *Library gap-filling, Batch L4*; this plan's status.

**Acceptance.**
1. Each new or extended entry states its assumptions, units, conventions and dated limits in Conditions, and labels the
   B12 value formula, the $Z$-form scores and the sign interpretation as Interpretation where no source prints them.
2. The three scripts pass with warnings as errors; every binding check listed above passes with the fixed seeds and
   path counts reported; no tolerance or seed is changed after a run to obtain a pass. A failure is diagnosed at the
   smallest boundary (estimator formula, unit or sign) before any rerun.
3. `make lint`, `make format-check`, `make check-compendium`, `make check-coverage` (447/447 objectives, 1,030/1,030
   items) and `make test` pass; `make pdf` builds with no overfull boxes or undefined references, and the changed pages
   are rendered and inspected; pre-commit passes on the committed files.
4. Records above complete; one local commit; nothing pushed.

**Evidence-reuse rules.** Existing numerical scripts are not rerun unless their files or inputs change: the L4 edits to
existing entries are text and cross-references, so `overlay-checks.py`, the forward-commitment and simulation scripts
keep their last results with that reason stated. If an existing entry's number is touched, rerun that entry's script.
`verify-outlines` is not needed (the crosswalk is unchanged). The L1-L3 mathematical and regulatory audits are not
reopened without new evidence.

### Batch L4 freeze corrections and frozen specification (2026-10-21)

Frozen by the owner's instruction of 2026-10-21: L4-D1 all three packages; L4-D2 the seasoned variance-swap value as an
explicitly labelled derivation with its contract and approximation assumptions stated; L4-D3 no separate objective for
B13. Expected outcome: one new objective (447/447), shortfall 44 against 45, no padding. Implemented on
`codex/library-gap-batch-l4`, created from the verified proposal state (`95c547a`, parent `517213d`, clean tree,
446/446 objectives, 1,030/1,030 items); one local commit, no push, PR, merge, rebase or amendment. The proposal above
is kept as written for the record; where it differs from this section, this section binds.

**Why the proposal had to be corrected before implementation.** Three statements in the proposal would have been taught
or checked wrongly:

| ID | Proposal text | Problem | Frozen correction |
|---|---|---|---|
| L4-C1 (B13) | $b=\frac FS(1+r_f\tau)-(1+r_{\$}\tau)$ | With annualised rates and $\tau\ne1$ this is a period amount, not an annualised spread; it agrees with the quoted (annual) basis only at $\tau=1$ | $b=\bigl[\frac FS(1+r_f\tau)-(1+r_{\$}\tau)\bigr]/\tau$, equivalently $\frac FS=\frac{1+(r_{\$}+b)\tau}{1+r_f\tau}$; exactly $b=-\kappa\frac{1+r_{\$}\tau}{1+(r_f+\kappa)\tau}$. The period amount is $b\tau$. Checked at $\tau=1$ and $\tau=0.25$ |
| L4-C2 (B3) | "Gamma: the pathwise second derivative of a call collapses to the closed form (eq. (18))" | Differentiating each path's pathwise delta $e^{-rT}\mathbf 1\{S_T>K\}S_T/S_0$ in $S_0$ gives zero almost surely ($S_T/S_0$ does not depend on $S_0$); eq. (18) comes from differentiating the *expectation*, where the indicator's boundary at $S_T=K$ contributes $e^{-rT}(K/S_0)^2g(K)$ (Broadie-Glasserman p. 273 and n. 2) | One sentence stating this; no second-order package. Deterministic check: the boundary formula equals the BSM gamma, and the path ratio $S_T/S_0$ is unchanged by a bump in $S_0$ |
| L4-C2 (B3) | "strike sensitivity needs the pathwise method" | True for payoffs meeting (A1)-(A4) such as the call ($-e^{-rT}\mathbf 1\{S_T>K\}$); for a digital the naive pathwise strike derivative is zero on every path, and plain LR does not apply because $K$ is not a density parameter | Restricted to Lipschitz payoffs; the digital named as a case where neither naive method applies (a change of variables or smoothing is needed, not taught) |
| L4-C2 (B3) | "its [LR] variance is larger (pp. 275, 280)" | Broadie-Glasserman report 1.5-4 times larger standard errors *in their examples*; it is not a universal ordering | Stated as a result for the cited examples and for this call's measured ratios |
| L4-C3 (B12) | $K_{t,T}$ "from the option strip", limits with an overloaded $K$, simulation compared with the continuous strike | The option strip prices continuously monitored variance; the contract pays daily sampled squared log returns. Under risk-neutral GBM, $E[\frac AN\sum r_i^2]=\sigma^2+(r-q-\sigma^2/2)^2/A$, so a simulation of the discrete contract has a different benchmark, and the difference must not be absorbed into Monte Carlo tolerance. $K$ was used for both $K_{\text{vol}}$ and $K_{\text{var}}$, and empty segments ($n=0$, $n=N$) were implicit | Contract, units and empty segments defined below; the remaining fair strike $K^{\text{rem}}_{t}$ is defined for the same discrete contract; the simulation is compared with the exact discrete expectation, and the continuous approximation and its deterministic difference are reported separately |

**Frozen contract and notation for L4-b.** Daily closes $S_0,\dots,S_N$, returns $r_i=\ln(S_i/S_{i-1})$, zero mean,
annualisation $A$ observations per year ($A=252$, $N=252$). Realised variance in decimal $\frac AN\sum_{i=1}^Nr_i^2$, in
variance points $10^4$ times that. Volatility strike $K_{\text{vol}}$ in vol points; variance strike
$K_{\text{var}}=K_{\text{vol}}^2$ in points squared; variance notional $N_{\text{var}}$ in currency per point squared,
$N_{\text{var}}=\text{vega notional}/(2K_{\text{vol}})$; payoff at $T$: $N_{\text{var}}(\text{RV}-K_{\text{var}})$.
After $n$ of $N$ returns, with $P(t,T)$ the discount factor to the payment date,
$V_t=N_{\text{var}}P(t,T)\bigl[\frac{10^4A}{N}\sum_{i\le n}r_i^2+\frac{N-n}{N}K^{\text{rem}}_t-K_{\text{var}}\bigr]$, where
$K^{\text{rem}}_t=E^Q_t\bigl[\frac{10^4A}{N-n}\sum_{i>n}r_i^2\bigr]$ is the fair variance strike of the remaining $N-n$
returns of the same contract. The realised sum is written without dividing by $n$, so $n=0$ needs no convention (empty
sum); at $n=N$ the remaining term has weight zero and $P=1$. Inception: $n=0$ and $K^{\text{rem}}_0=K_{\text{var}}$ give
zero. Labelled Interpretation (L4-D2). Option-strip replication (Demeterfi EQ 26; Hull eq. (26.8)) gives the expected
continuously monitored variance, an approximation to $K^{\text{rem}}_t$; under risk-neutral GBM with dividend yield $q$
the exact discrete value is $10^4[\sigma^2+(r-q-\sigma^2/2)^2/A]$. Example: vega notional 100,000, $K_{\text{vol}}=20$,
$N_{\text{var}}=2{,}500$; $n=126$ with realised volatility 25 over them; quoted $K^{\text{rem}}=324$; $r=4$ percent
continuously compounded, $q=1$ percent, $T-t=0.5$.

**Frozen run parameters (fixed before the first implementation run).**

| Script | Random inputs | Binding tolerances |
|---|---|---|
| `notes/artefacts/numerical-pricing/monte-carlo-greeks-check.py` | NumPy `default_rng(20261021)`, one vector of 100,000 standard normals shared by every estimator | Deterministic: path derivatives and both scores against central differences, relative error $\le10^{-6}$ (scores at $x=80,105,130$); eq. (18) boundary term against BSM gamma, $\le10^{-12}$; $S_T/S_0$ unchanged by an $S_0$ bump, $\le10^{-12}$. Stochastic: call pathwise and LR delta, pathwise and LR vega and pathwise strike sensitivity each within 4 standard errors of the closed form; digital LR delta within 4 standard errors. Exact: digital pathwise delta and pathwise strike sensitivity zero on every path |
| `notes/artefacts/derivative-overlays/seasoned-variance-swap-check.py` | `default_rng(20261021)`, 200,000 paths of 126 daily returns, generated in four blocks of 50,000 | Deterministic: limits within $10^{-6}$ currency; units, data weights and the vega-notional derivative relative $\le10^{-9}$; $E[r^2]$ by quadrature against $\sigma^2\Delta+\mu^2\Delta^2$, relative $\le10^{-9}$. Stochastic: discounted mean payoff within 4 standard errors of the value at the exact discrete $K^{\text{rem}}$ |
| `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py` | None | All deterministic: relative $\le10^{-12}$ or $10^{-6}$ currency on 100 million |

The B13 script goes beside `forward-swap-checks.py`, which serves the same topic file; the proposal's "derivative-overlays
or currency-markets" was a routine default. Reported, not binding: LR to pathwise standard-error ratios; digital
resimulation bias and standard error at $h=1$ and $h=0.01$; the continuous-approximation value and its difference; the
mean-subtracted, $n-1$ and calendar-weight variants; the inverted quote entered unconverted. Any failure is classified
(formula, unit, sign, harness) at the deterministic checks first; no seed, path count or tolerance is changed to pass.

**Frozen B13 conventions.** EUR/USD quoted as $S$ dollars per euro (1.10); notionals EUR 100 million and USD 110 million
exchanged at $T_0$ and re-exchanged at the same spot at $T_n$; party A pays euros and receives dollars at $T_0$, then
receives compounded €STR plus $\kappa$ on the euro notional and pays compounded SOFR on the dollar notional, and at $T_n$
pays dollars and receives euros (Hull sec. 7.10; Ding-Liu-Rutkowski Def. 2.4 with the spread on the non-dollar leg).
$\kappa=-20$ basis points. Assumed fixings 4.0 percent (SOFR) and 2.5 percent (€STR) per year with accrual exactly
$\tau$ (actual contracts accrue ACT/360 on rates compounded in arrears; stated, not modelled). Three annual periods for
the cash-flow table; one period at $\tau=1$ and $\tau=0.25$ for the parity relation. LIBOR-era evidence (BIS 2016,
Du-Tepper-Verdelhan) stays separate from these RFR examples. Excluded as before: resetting (mark-to-market) notionals
and multi-period cross-currency valuation and discount curves.

**Scope unchanged.** Two new entries (`meth:monte-carlo-greeks`, `meth:cross-currency-basis-swaps`), one substantive
extension (`meth:volatility-derivative-applications`), cross-reference edits, one new objective
(`objective:estimate-greeks-by-simulation`, `planned_batch` 9). Version notes: the Goldman Sachs note and arXiv v3 are
registered as their own `sources.tex` keys, each naming the catalogued version, because their locators differ.

### C1 pass: L4 corrections (2026-10-21)

Authorised with the C1 inventory and made on `codex/library-gap-c1-inventory`, created from `e6c22e6` (parent `95c547a`,
clean tree, 447/447 objectives, 1,030/1,030 items). Fixes only: no objective, input, seed or earlier tolerance changed.

| ID | Entry | Problem | Correction and evidence |
|---|---|---|---|
| L4-F1 | `meth:monte-carlo-greeks` | Appendix B's $h^*$ was presented as the optimum; its assumption that the correlation $\rho$ of the two pricing errors does not depend on $h$ (Broadie-Glasserman p. 281) was omitted; "they are unbiased" did not say which estimators and under what conditions | $h^*$ stated with its assumption and not as a universal optimum; Interpretation: with common random numbers $\rho$ depends on $h$, the call's shared-path difference has finite limiting variance, the digital's grows like $e^{-2rT}g(K)K/(S_0h)$; unbiasedness restricted to the direct estimators under (A1)-(A4) or the interchange condition; fixed-step resimulation keeps finite-difference bias. New part 4 of `monte-carlo-greeks-check.py`, tolerances fixed before its run: call variance 0.348653 ($h=1$) and 0.351952 ($h=0.001$) against pathwise 0.351959 (relative 1%); digital variance exact from the lognormal CDF, $h\times$variance 0.018065 to 0.018435 against the limit 0.018435 (relative 1%). Parts 1-3 and their results unchanged |
| L4-F2 | `meth:volatility-derivative-applications` | "vol points with decimal variance" for the $10^4$ conversion; "zero-mean log returns" could read as zero expected returns | "volatility points squared with decimal variance"; "zero mean" stated as the convention of not subtracting the sample mean, not zero expectation (under a drift the expectation is not zero). Numbers and the 1 percent dividend yield unchanged; `seasoned-variance-swap-check.py` not rerun (no code or asserted result changed) |
| L4-F3 | `meth:esg-exposure-evaluation` | "the latest available on 21 October 2026" overstated what was checked | "the latest found in the public RECAP docket as of 21 October 2026 (PACER was not used; later filings are unverified)", matching `notes/readings/ca8-iowa-v-sec-2026.md`. Regulatory review not reopened |

### Proposed Batch L5 (2026-10-21; awaiting owner freeze): lookback options and hedging with transaction costs

*Kept as the proposal record. Frozen on 2026-10-21 with decisions L5-D1 to L5-D3; see "Batch L5 freeze and frozen
specification" below, which binds where the two differ (in particular it replaces the proposal's "within 4 standard
errors of the Leland price difference" gate and its discrete-monitoring "correction" clause).*

From the C1 inventory (Section 8.2). Proposed only: no entry, script, reading note or coverage record has been written.
Both packages extend the option-hedging and path-dependent material of L1 with sources already held, so they form one
coherent `volatility-options` batch.

**L5-a (C1-N1). Lookback options.** New entry `meth:lookback-option-valuation` in
`volatility-options/exotic-options.tex` after `meth:barrier-option-valuation`. Teaching: floating and fixed-strike
payoffs; Hull's closed forms for floating lookbacks with the running minimum or maximum to date (sec. 26.11, pp.
623-625); the Wilmott state-variable formulation and the jump condition for discrete sampling (chap. 24 lookback
passages; chap. 26 to be read); why discrete monitoring lowers the value. New
`objective:value-lookback-options` (`topic:option-valuation`, like the other exotic-option objectives), planned batch 10; prerequisites `objective:value-barrier-options-monitoring`, `objective:apply-monte-carlo-simulation`.
*Checks* (`notes/artefacts/exotic-options/lookback-option-check.py`): reproduce Example 26.2 (put 7.79, call 8.04)
deterministically; seasoned values with a running extreme reduce to the new-issue values when $S_{\min}=S_0$; a
simulation with fine monitoring within 4 standard errors of the closed form after an explicitly stated discrete-
monitoring correction or, if none is printed in the sources read, with the discrete-continuous gap reported and
shown to shrink as monitoring increases (not absorbed into tolerance).

**L5-b (C1-N2). Hedging with transaction costs.** New entry `meth:transaction-cost-hedging` in
`volatility-options/option-valuation.tex` after `res:delta-hedging-volatility-mismatch`. Teaching: Leland's adjusted
volatility for proportional costs and its opposite signs for long and short positions; the condition on gamma; the
Hoggard-Whalley-Wilmott nonlinear equation and why a portfolio's value is not the sum of its parts; the costs of
fixed-interval against band rebalancing (Wilmott chap. 48, pp. 783-812; Leland 1985 cited through Wilmott unless
obtained). New `objective:hedge-options-with-transaction-costs` (`topic:option-valuation`), planned batch 10; prerequisites
`objective:quantify-hedging-volatility-mismatch`, `objective:manage-option-greeks`. *Checks*
(`notes/artefacts/option-valuation/transaction-cost-hedging-check.py`): the adjusted volatility formula against
Wilmott's printed form and its limits ($k\to0$ gives $\sigma$); a discretely hedged call with proportional costs
simulated on fixed seeds, whose mean hedging cost agrees with the Leland price difference within 4 standard errors
for a small cost parameter, with the approximation error at a larger parameter reported, not tuned; the nonlinearity
shown on a call spread (value of the spread against the difference of the two option values).

**Optional L5-c (C1-D3).** Option-strategy practice items in `meth:option-spreads-volatility-strategies` and
`meth:covered-call-protective-put`, only if `s7-natenberg` supports them when read; 0 objectives.

**Expected objectives: +2** (449/449), shortfall 43 against the standing 45, without padding.

**Acceptance.** Seeds, path counts and tolerances fixed in this plan before the first run; deterministic formula,
unit and limit checks before stochastic ones; failures diagnosed, not reseeded. Each entry states its model
assumptions and labels derivations as Interpretation. Gates as in L4: the two scripts with warnings as errors, lint,
format, both checkers (449/449, 1,030/1,030), tests, PDF without overfull boxes or undefined references with changed
pages inspected, pre-commit on changed files; records (reading notes, entry evidence, objectives, pathway, review
record, this plan). Existing scripts reused unless their files or inputs change.

**Dependencies.** L1's barrier, Asian and volatility-mismatch entries and their scripts; no new dependency.

### Pre-L5 audit corrections (2026-10-21)

Authorised with the L5 freeze and made on `codex/library-gap-batch-l5`, created from `main` at `c26a09e` (the merge of
PR #33, whose second parent is the expected proposal commit `d71e127` and whose tree is identical to it; clean tree,
447/447 objectives, 1,030/1,030 items). The prompt expected `codex/library-gap-c1-inventory` at `d71e127`; that branch is
unchanged and `main` holds the same tree plus the merge, so branching from `main` preserves the newer merge. Fixes only.

| ID | Where | Problem | Correction and evidence |
|---|---|---|---|
| C1-F1 | `meth:monte-carlo-greeks` | "Fixed-step resimulation is biased whatever the conditions" is false as stated: a price that is affine in the parameter (for example a forward's value in $S_0$) has an exact finite difference | Generally biased: its expectation is the finite difference of the price, not the derivative, and more paths reduce only the sampling error, never that bias; affine price functions are the exception. Estimator formulas and numbers unchanged; `monte-carlo-greeks-check.py` not rerun (no code, input or asserted result changes) |
| C1-F2 | Section 8.2, the status paragraph, the C1 review record | C1 counted "4 source-supported" depth extensions (C1-D1 to C1-D4). C1-D3's Natenberg passages were not located or read (the book is held; its reading note covers chaps. 11, 17 and 24 for earlier entries, not the three C1-D3 items). C1-D4 cited Wilmott secs. 10.11-10.12, which concern the backward equation and the risk-neutral expectation; the forward equation is sec. 10.4, printed p. 172, eq. (10.2) | Reclassified by evidence status: C1-D1 supported (Damodaran, *Applied Corporate Finance*, printed pp. 98-107 read in C1); C1-D2 partly supported (*Managing Investment Portfolios* Example 11-3 and Exhibit 11-4 read; Hull's collar pages held but not read for D2; IRC secs. 1259 and 721 not read); C1-D3 unsupported (source held, passages not located); C1-D4 supported after this pass: Wilmott chap. 10, secs. 10.2-10.6, printed pp. 169-175 read on 21 October 2026 (forward equation (10.2), p. 172; lognormal solution (10.3), p. 173; steady state, p. 174; backward equation (10.4), p. 175). C1-D1 and C1-D2 were not reread here. The `d71e127` commit message keeps the old wording; this record supersedes it |

### Batch L5 freeze and frozen specification (2026-10-21)

Owner decisions of 2026-10-21: **L5-D1** L5-a and L5-b only (+2 objectives), L5-c excluded; **L5-D2** Leland's model
cited through Wilmott chap. 48 with Leland named as originator, without implying that Leland (1985) was read;
**L5-D3** C1-D1 and C1-D2 deferred to a later batch, other unresolved backlog items stay deferred. Expected: 449/449
objectives, 1,030/1,030 items; shortfall 43 against 45, without padding. This section binds where it differs from the
proposal above. Specification written before any L5 script was run.

**Sources read for the freeze** (git-ignored copies; locators printed pages). Hull, OFOD 11th Global ed., copy in
`reading materials/` (SHA-256 `8bc6e2f0…b482`, printed page = PDF page): sec. 26.11, pp. 623-625 (floating formulas with
$S_{\min}$/$S_{\max}$ "achieved to date", Example 26.2, the fixed-strike parity relation and n. 8; discrete observation
adjusted by Broadie, Glasserman and Kou (1998), n. 9, named but **not printed**). Wilmott, PWOQF 2nd ed. (SHA-256
`e0ff5f09…d549`, printed = PDF $-21$): chap. 24, secs. 24.4-24.5, pp. 422-425 (updating rule $M_i=\max(S(t_i),M_{i-1})$,
jump condition (24.5), algorithm); chap. 26, pp. 445-452 (payoff types, continuous measurement and $\partial V/\partial M=0$
on $S=M$, discrete measurement "used to decrease the value", similarity reduction (26.1), formulas of sec. 26.6, further
reading naming Heynen and Kat (1995), not printed); chap. 48, pp. 783-811 (secs. 48.1-48.14 and the appendix; formula
pages 785, 788-789 also viewed as images); chap. 10, pp. 169-175 (C1-F2).

**Discrepancies found while reading.** (i) Wilmott p. 789 prints the long-position breakdown as $\kappa>\sigma/\sqrt{8\pi\,\delta t}$;
that is dimensionally inconsistent ($\kappa$ is dimensionless, $\sigma/\sqrt{\delta t}$ has units of 1/time). From (48.5),
$\check\sigma^2>0$ if and only if $\kappa<\sigma\sqrt{\pi\delta t/8}$, i.e. $K=\kappa/(\sigma\sqrt{\delta t})<\sqrt{\pi/8}\approx0.6267$.
The derived form is taught and checked; the printed one is recorded here only. (ii) The sec. 48.4 heading dates
Hoggard-Whalley-Wilmott 1992 and the further reading 1994; the entry names the model without a year. (iii) No source
read prints a lookback-specific discrete-monitoring correction; the barrier shift $e^{\pm0.5826\sigma\sqrt{T/m}}$ is **not**
transplanted.

#### L5-a frozen specification: `meth:lookback-option-valuation`

*Contract and notation.* Floating call pays $S_T-S_{\min}$, floating put $S_{\max}-S_T$; fixed call $\max(S_{\max}-K,0)$,
fixed put $\max(K-S_{\min},0)$. Extremes run over the whole option life including the start price; at a valuation date
with remaining time $\tau$ they are the recorded extreme to date. Continuous monitoring in the formulas; a discretely
monitored contract observes $S_0$ and $m$ equally spaced dates $t_i=iT/m$ with $t_m=T$. Hull's formulas (sec. 26.11) are
used with $T$ read as remaining time $\tau$, which is how Hull states the running extreme "to date"; $r\ne q$ (the $r=q$
case, Hull Problem 26.23, is excluded).

*Deterministic checks* (`notes/artefacts/exotic-options/lookback-option-check.py`, part 1):
1. Example 26.2 ($S_0=50$, $\sigma=0.4$, $r=0.1$, $q=0$, $T=0.25$, new issue): put and call rounded to cents equal 7.79 and
   8.04 exactly; printed $b_1=-0.025$, $b_2=-0.225$, $b_3=0.025$ within $5\times10^{-4}$; $Y_2=0$ within $10^{-15}$.
2. New-issue limits: the call evaluated with $S_{\min}=S_0$ and the put with $S_{\max}=S_0$ (where $Y_1=Y_2=0$).
3. Two sources: Hull's floating call and put against Wilmott's sec. 26.6 forms, and Hull's fixed-strike parity route
   against Wilmott's direct fixed-strike formulas in both cases ($K$ above and below the running extreme), relative
   $\le10^{-12}$ (they are algebraically identical, so only rounding remains) at six points with $q=0$ and $q=0.02$.
4. Pricing equation: central-difference residual of $V_t+\frac12\sigma^2S^2V_{SS}+(r-q)SV_S-rV$ at interior points
   ($S\ne$ extreme), steps $h_S=0.01$, $h_t=10^{-5}$, absolute $\le10^{-6}$ (truncation and rounding both below $10^{-9}$).
   *Pre-run criterion, kept as frozen. Amended 2026-10-21 after the first run failed it (harness, $O(h_S^2)$
   truncation): the same $10^{-6}$ is applied to the Richardson-extrapolated residual $(4R(0.01)-R(0.02))/3$; see
   `notes/source-review-records.md`, *Library gap-filling, Batch L5, 21 October 2026*, "Checks".*
5. Boundary condition $\partial V/\partial M=0$ on $S=M$ (Wilmott p. 447): one-sided difference in $S_{\min}$ at $S=S_{\min}$
   is $\le10^{-2}$ times the derivative at an interior point ($S=50$, $S_{\min}=45$), and shrinks linearly: the ratio of the
   differences at $h=10^{-2}$ and $10^{-3}$ lies in $[5,20]$.
6. History matters (would catch ignoring it): deep-seasoned limits $|c_{fl}(50;S_{\min}=20)-(Se^{-q\tau}-20e^{-r\tau})|\le10^{-4}$
   and $|p_{fl}(50;S_{\max}=120)-(120e^{-r\tau}-Se^{-q\tau})|\le10^{-4}$ (the excess is $e^{-r\tau}E[(20-m_\tau)^+]$ with
   $P(m_\tau<20)$ about $10^{-6}$); strict monotonicity: $c_{fl}$ decreasing in $S_{\min}$ and $p_{fl}$ increasing in
   $S_{\max}$ on a grid. Ignoring history gives 8.04 against about 30.5.

*Seasoned Monte Carlo* (part 2; independent of the formulas): $S=50$, $\tau=0.25$, Example 26.2 parameters; call with
$S_{\min}=45$, put with $S_{\max}=56$, fixed call $K=52$ with $S_{\max}=56$ (already in the money) and $K=60$. Exact
simulation of the continuous extreme: one step $X_\tau=\ln S+(r-q-\sigma^2/2)\tau+\sigma\sqrt\tau Z$, then the bridge
minimum $\frac12[x_0+x_1-\sqrt{(x_1-x_0)^2-2\sigma^2\tau\ln U}]$ (maximum with $+$ and an independent $U'$), the inverse of the
crossing probability $\exp[-2(x_0-b)(x_1-b)/(\sigma^2\tau)]$ already used in `meth:barrier-option-valuation` (labelled
Interpretation). `default_rng(20261022)`, 400,000 paths. Gate: each estimate within 4 standard errors of the closed form;
and the seasoned and new-issue closed forms differ by more than 20 standard errors, so the test has power against ignoring
history.

*Monitoring* (part 3): new issue, Example 26.2 parameters. `default_rng(20261021)`, 100,000 paths of 1,008 equal steps in
20 blocks of 5,000, log-exact stepping. Coupled nested grids $m\in\{7,21,63,252,1008\}$ (63 is about daily) are subsets of
the same path, each including $S_0$ and $S_T$; the continuous extreme on the same paths is the minimum (maximum) over the
1,008 sub-intervals of exact bridge extremes (independent uniforms for minimum and maximum). Separation of errors:
*sampling* uncertainty is the standard error of the continuous estimate against the closed form (gate: within 4 standard
errors for call and put); *monitoring bias* is the paired mean gap $g_m=e^{-rT}E[\text{payoff}_{\text{cont}}-\text{payoff}_m]$
with its paired standard error. Gates: payoffs ordered pathwise (finer grid never pays less; exact, a harness check);
each $g_m$ positive by more than 4 paired standard errors; convergence criterion $g_{1008}\le\frac12g_{63}$ (16 times finer
monitoring must remove at least half the gap; pathwise convergence of the discrete extreme follows from path continuity,
and the criterion assumes no rate). Reported, not gated: $g_m\sqrt m$, the daily ($m=63$) values.

#### L5-b frozen specification: `meth:transaction-cost-hedging`

*Units and conventions* (Wilmott sec. 48.3). Trading $\nu$ shares at $S$ costs $\kappa|\nu|S$, buying or selling; $\kappa$
is a one-way proportional cost (if trades fill at mid $\pm$ half the spread, $\kappa$ is half the proportional bid-offer
spread: Interpretation). Rebalancing at fixed $\delta t=T/N$; $K=\kappa/(\sigma\sqrt{\delta t})$ (48.7). Position sign
$s=+1$ long, $-1$ short one call; stock holding $h_k=-s\Delta_k$; trades $\nu_k=h_k-h_{k-1}$ at $S_{t_k}$. Delta rule: BSM
delta at the position's Leland volatility, $\check\sigma$ for long and $\hat\sigma$ for short, $\hat\sigma^2,\check\sigma^2=\sigma^2\pm
2\kappa\sigma\sqrt{2/(\pi\delta t)}$ (48.5)-(48.6); the BSM delta at $\sigma$ for the spread demonstration. Cash: $c_0=-sP-h_0S_0$,
$c_k=c_{k-1}e^{r\delta t}-\nu_kS_{t_k}-\kappa|\nu_k|S_{t_k}$. Settlement: physical; at $T$ the holding moves to the payoff
delta $-s\mathbf 1\{S_T>K\}$ (the $N$-th trade, costed), the delivered share passes at the strike, so terminal wealth is
$W_T=c_N+h_NS_T+s(S_T-K)^+$. Opening trade ($h_0$ from zero) excluded from the comparison and reported separately; the
cash-settled alternative (liquidating $h_{N-1}$ at $S_T$) reported separately. Simulation under the risk-neutral measure
($\mu=r$), $q=0$, so the discounted stock is a martingale; discounting continuous at $r$.

*Comparable quantity* (original derivation, labelled Interpretation). Itô's formula for $e^{-rt}\hat V(S_t,t)$, where $\hat V$
is BSM at $\hat\sigma$ and $S$ has volatility $\sigma$, gives exactly $\hat V-V=E^Q\!\int_0^Te^{-rt}\kappa\sigma\sqrt{2/(\pi\delta t)}
S_t^2\hat\Gamma_t\,dt$: the Leland premium is the expected present value of Wilmott's leading-order cost (48.2) of hedging
with the $\hat\sigma$ delta. Likewise $V-\check V$ with $\check\Gamma$ for the long position. The simulated estimand is
$C_N=E^Q[\sum_{k=1}^Ne^{-rt_k}\kappa S_{t_k}|\nu_k|]$ under the same rule, and the **approximation residual** is
$e_N=C_N-L$ with $L=\hat V-V$ (short) or $V-\check V$ (long). Under $Q$ the writer at price $\hat V$ (holder at $\check V$) has
$E[e^{-rT}W_T]=-e_N$ exactly, so $e_N$ is the expected loss left by the Leland price.

*Deterministic checks* (`notes/artefacts/option-valuation/transaction-cost-hedging-check.py`, part 1): (48.5)-(48.6)
against the printed $\sigma(1\mp\sqrt{8/(\pi\delta t)}\,\kappa/\sigma)^{1/2}$, relative $\le10^{-14}$; signs
$\check\sigma<\sigma<\hat\sigma$ for $\kappa>0$; zero-cost limit $\check\sigma=\hat\sigma=\sigma$ and $L=0$ at $\kappa=0$
exactly; domain $\check\sigma^2(K^*)=0$ at $K^*=\sqrt{\pi/8}$ within $10^{-15}\sigma^2$ and negative above it; Wilmott's spread
$2\kappa SN'(d_1)\sqrt\tau/\sqrt{2\pi\delta t}$ against $\hat V-V$: the relative error at $K=0.01$ is between 5 and 20 times
that at $K=0.001$ (second-order error). Reported: the printed p. 789 bound against the derived one.

*Simulation* (part 2): call $S_0=K_{\text{strike}}=100$, $\sigma=0.2$, $r=0.05$, $q=0$, $T=1$ (the setting of Wilmott sec.
48.12). `default_rng(20261023)`, 100,000 paths of 208 log-exact steps; nested rebalancing grids $N\in\{13,52,208\}$ on
the same paths; Leland numbers $K\in\{0.1,0.4\}$ (so $\kappa=K\sigma\sqrt{T/N}$; at $N=52$, $\kappa=0.277\%$ and $1.109\%$);
long ($\check\sigma$ rule) and short ($\hat\sigma$ rule). Gates: (a) ledger identity on every path, $e^{-rT}(c_N+h_NS_T)=-sP+
\sum_kh_k(\tilde S_{k+1}-\tilde S_k)-\sum_ke^{-rt_k}\kappa S_{t_k}|\nu_k|$, relative $\le10^{-9}$ (signs and discounting);
(b) $E[e^{-rT}W_T]$ within 4 standard errors of $-s(P-V)-C_N$, with $C_N$ estimated on the same paths (exact in expectation: only sampling
error), for short and long at $K=0.1$, $N=52$; (c) convergence of the residual at fixed $K$: $|e_{13}|>|e_{52}|>|e_{208}|$
and $|e_{208}|\le\frac12|e_{13}|$ (16 times more frequent rebalancing must remove at least half the residual; the expected
leading error is $O(\sqrt{\delta t})$ or smaller, which predicts a quarter, but no rate is gated), for all four
position/$K$ cases. Reported with standard errors, not gated: $e_N/L$, the opening cost $\kappa h_0S_0$, the cash-settlement
close, the P&L standard deviation and 95th percentile, and costs against hedge dispersion at fixed $\kappa=0.2\%$ (BSM delta)
for $N\in\{13,52,208\}$ (Wilmott sec. 48.13's trade-off).

*Nonadditivity* (part 3, hedge-cost demonstration, not a solved valuation): bull spread long $K_1=95$, short $K_2=105$, same
paths, $N=52$, $\kappa=0.2\%$, BSM deltas at $\sigma$. Aggregate trades $\nu^{\text{net}}=\nu^{(1)}+\nu^{(2)}$ against
separately hedged legs. Gates: $\kappa S|\nu^{\text{net}}|\le\kappa S(|\nu^{(1)}|+|\nu^{(2)}|)$ on every step of every path
($10^{-12}$); mean saving positive by more than 4 paired standard errors; long and short the same call: aggregated cost
exactly 0 on every path, separate cost exactly twice one leg's. Reported, labelled approximate: leg-by-leg Leland values
$V(K_1;\check\sigma)-V(K_2;\hat\sigma)$ against $V(K_1;\sigma)-V(K_2;\sigma)-C^{\text{agg}}$; the Hoggard-Whalley-Wilmott
equation (48.4) is stated, not solved (its value needs a nonlinear PDE solver, which no retained claim requires).

*Teaching limits.* Band (delta-tolerance) and utility-based rebalancing are described only as Wilmott presents them
(secs. 48.8-48.9, 48.12-48.13): the bandwidth (48.9) and its equation (48.10), the asymptotic optimal band, Jefferies'
simulated 95th-percentile prices (Leland 14.90 at four days, delta tolerance 15.15, utility 15.03) and real-data wins
(delta tolerance about 70 percent, utility 23, Leland 7), with Wilmott's conclusion that the best strategy is unclear.

**Failure policy.** Deterministic parts first; any failure classified (formula, unit, sign, harness, approximation) and
reported with its first-run output; no seed, path count, grid or tolerance is changed to pass.

### L5 clarifications (2026-10-21, before L6)

Made on `codex/library-gap-batch-l6`, created from `codex/library-gap-batch-l5` at `af47d03` (parent `c26a09e`; clean;
449/449, 1,030/1,030). (1) `meth:transaction-cost-hedging`: "long--short difference per side" replaced by the explicit
statement that Wilmott's $2\kappa SN'(d_1)\sqrt{T-t}/\sqrt{2\pi\delta t}$ is each side's adjustment from the frictionless value,
so the short-minus-long difference is about twice it to first order (formula and numbers unchanged). (2) In the frozen
L5-a specification, a dated cross-reference after check 4 points to the amended Richardson gate and the L5 review record;
the pre-run criterion is kept as written. Editorial only; no rerun.

### Batch L6 (2026-10-21): C1-D1 and C1-D2, depth only (+0 objectives)

Owner scope: C1-D1 (country risk premium) and C1-D2 (concentrated single-stock positions), both depth within existing
objectives; C1-D3, C1-D4 and C1-U1 to C1-U3 stay deferred; no inventory repeat. Specification written after source review
and before any L6 script ran.

**Sources read** (held = library or git-ignored copies; read = these passages).
- Damodaran, *Applied Corporate Finance*, 4th ed. (`applied-corporate-finance-2014`, SHA-256 `ab6e2462…a7f4`, printed =
  PDF $-16$): pp. 89-93 (currency consistency, default-spread-adjusted local risk-free rates, CDS alternative), pp. 98-107
  (mature premium plus country premium; default-spread, relative-volatility and melded methods; Table 4.5; whether a
  country premium should exist; company premium weighted by revenues, with production and reserves caveats; Illustration
  4.2, Table 4.9) and pp. 133-135 (Illustration 4.13: dollar cost of equity, R$ by inflation differential). Slips: India's
  spread is 2.00 percent in the prose of p. 98 but 2.25 in its equation and Table 4.5; Table 4.5 is headed "March 2009"
  while its inputs are dated November 2013; n. 15 notes the equity volatility is in R$ and the bond's in dollars.
- *Managing Investment Portfolios* (2007) (`managing-investment-portfolios-2007`, printed = PDF $-29$): Example 11-3 and
  Exhibit 11-4, pp. 693-695; p. 687 (concentrated positions as a unique circumstance); p. 47 (charitable remainder trust
  defined only). Its tax statements are 2007 textbook summaries and are not used as legal support.
- *Portfolio Management in Practice*, Vol. 1 (2020) (`portfolio-management-in-practice-v1-2020`, registered and already
  cited; same copy as its reading note, SHA-256 `9753edc5…8bef`, printed = PDF $-28$, checked on pp. 903-904): chap. 16, sec. 6, pp. 904-913 (risks;
  approaches; staged diversification and completion portfolios with the Exxon tax-against-tracking-error trade-off;
  monetisation as hedge then borrow; zero-cost collar and Example 12; constructive sale named; exchange funds and Exhibit
  15; charitable remainder trust, Exhibit 16; Example 13).
- Hull, OFOD 11th Global ed. (same copy as L5): sec. 12.2, pp. 270-271 (protective put); sec. 17.2, pp. 387-389 (range
  forwards: zero cost, strikes moved together give a forward); sec. 26.1, p. 615 and n. 1 ("zero-cost collar" as another name).
- US primary texts, retrieved 2026-10-21 (LII, Cornell; IRS): 26 U.S.C. secs. 1259 (whole), 721(a)-(b), 351(e)(1),
  704(c)(1)(B), 737(a)-(b), 664(b)-(d); 26 C.F.R. sec. 1.351-1(c)(1)-(6); Rev. Rul. 2003-7, 2003-5 I.R.B. 363-365.
  Not read: sec. 170 (charitable deduction), any regulations under sec. 1259(c)(1)(E), later case law on prepaid forwards,
  state law. These are named as unread where relevant and nothing is taught from them.

**Discrepancies.** PMiP says an exchange fund's 20 percent of "qualified assets" is "usually real estate investment
trusts"; sec. 351(e)(1)(B)(iv) and Reg. sec. 1.351-1(c)(1)(ii) count REIT interests among the investment assets, so the
entry states only the threshold. PMiP and MIP describe charitable trusts as letting shares be sold "without incurring
capital gains taxes"; sec. 664(c)(1) exempts the trust, but sec. 664(b) carries the trust's undistributed capital gain
out to the income beneficiary in the payments, so the entry teaches deferral and spreading at the beneficiary level.
MIP's "private exchange ... tax free" is not verified and is not taught as a tax result.

**L6-a: entry change.** Extend `meth:cost-of-debt-equity-estimation` (objective `estimate-cost-of-debt-and-equity`):
a *Country risk* block in Statement (mature premium plus country premium; the three methods; beta-scaled against
additive use; revenue weights with production caveats; whether the premium should exist), conventions in Notation-style
text (currency of cash flows and risk-free rate; local rate net of the local-currency default spread; premium measured
against the mature market's government bond; volatilities annualised from the same frequency and, ideally, currency),
an original example in Practice, and Pitfalls (double counting the default spread; treating the default spread as the
equity premium; incorporation country instead of operations; mixing currencies).

*Example inputs (synthetic).* Dollar risk-free 4.0 percent; mature premium 5.0; country dollar-bond default spread 3.0;
annualised volatilities: country equity 30, mature equity 18, country dollar bond 20; beta 1.2; operations 60 percent in
the country, 40 mature; local government bond 11.0 with local-currency default spread 2.5; expected inflation 6.0 local
and 2.5 dollar. Expected (hand): country premiums 3.0, 3.3333 and 4.5 for the default-spread, relative-volatility and
melded methods; total premiums 8.0, 8.3333, 9.5; dollar cost of equity with the melded premium 15.4 (beta-scaled) and
14.5 (additive); revenue-weighted premium 7.7 and cost of equity 13.24; local risk-free 8.5; local cost of equity by
inflation differential 17.107 against 17.74 with the dollar premium kept; double counting with the unadjusted 11.0 gives
20.24. Zero limit: spread 0 gives zero country premium for the spread-based methods (cost of equity 10.0), while the
relative-volatility method still gives 3.3333, since it does not use the spread.

*Acceptance* (`notes/artefacts/corporate-finance/country-risk-premium-check.py`, deterministic, no random inputs):
the example computed in floating point and again in exact rational arithmetic, agreeing to $10^{-12}$, and each matching
the hand values above to $5\times10^{-5}$ percentage point (the hand values are exact or rounded at 4-5 decimals);
reproduction of Damodaran's printed values to their rounding ($\le0.005$ percentage point): Table 4.5 (1.68, 3.00; 2.52,
3.60; 0.84, 1.44), Illustration 4.2 (8.50, 9.10, 6.94), Disney's revenue-weighted 5.76 from Table 4.9, Vale's R$ cost of
equity 18.67 and 18.87 (pp. 134-135, with $k_{\$}=2.75+1.1503\times7.38$); and the zero limit exactly.

**L6-b: entry changes.** Extend `meth:complex-client-situations` (objective `advise-complex-client-situations`) with
a block on concentrated public-stock positions: the risks (company-specific, inefficiency, liquidity, tax); the menu (sell,
staged diversification, completion portfolio, hedging and monetisation, exchange fund, charitable remainder trust,
holding); what each retains and surrenders (exposure, liquidity, financing, counterparty, upside, control, fees); US
federal tax mechanics as of 21 October 2026 from the primary texts above, qualified as rules not advice; and an original
example. Extend `meth:covered-call-protective-put`'s collar item with the zero-cost condition and the convergence to a
forward (Hull), linking to the new block. The PMiP Exxon figures (tax 225,000; tracking error 19.8 percent; 2 percent
index weight) are reproduced in text where used.

*Example contract and inputs (synthetic; specified, not "a typical VPF").* Holding 100,000 shares at 50 (5 million),
basis 10 per share, an assumed flat 20 percent tax on the gain (illustrative, not a statutory rate), one year, $r=4$
percent continuously compounded, $q=0$, volatility 30 percent, BSM values. (i) *Sale*: tax 900,000, 4.1 million
reinvested (riskless here, to isolate exposure). (ii) *Zero-cost collar*: long 45 put, short call at the strike $K_2$
that makes the call worth the put (solved, bisection to $10^{-10}$); no cash; value $\min(\max(S_T,45),K_2)$ per share.
(iii) *Variable prepaid forward*, terms patterned on the structure in Rev. Rul. 2003-7: at maturity deliver all shares
if $S_T<F=50$, shares worth $NF$ if $50\le S_T\le C=62.5$, and $NF/C$ shares (80 percent) above; shares pledged; cash may
replace shares. The advance is the BSM present value of the delivery, $N[S_0-c(F)+(F/C)c(C)]$, with no dealer spread
(stated). (iv) PMiP Exhibit 15 reproduced, and the annual fee at which the exchange fund's after-tax value equals the
sale's (Interpretation, bisection).

*Acceptance* (`notes/artefacts/private-wealth/concentrated-position-check.py`, deterministic): put-call parity and the
zero-cost condition to $10^{-10}$; the advance by two routes ($S_0-c(F)$ and $Fe^{-rT}-p(F)$) equal to $10^{-10}$
relative, showing the prepaid forward as a collar plus a loan; on $S_T\in\{30,40,50,60,70,80\}$, retained plus delivered
value equals $NS_T$ exactly, delivered shares lie in $[0.8N,N]$, and payoffs from the formula equal the option
decomposition to $10^{-9}$; hand values for the sale (tax 900,000; 4,264,000 grown at $e^{0.04}$ gives 4,267,328.43) to
0.01; *[Corrected 2026-10-21 after the first run: these hand values were wrong; the gain is 4,000,000, so
the tax is 800,000 and 4,200,000 grows to 4,371,405.25. Tolerance unchanged; see the L6 review record.]* PMiP Exhibit 15 (775,000; 1,510,256; 1,948,717; 183,814; 462,179; 1,326,442; 1,486,538) to 1 dollar (printed
rounding). Reported: $K_2$, the advance as a fraction of value, the break-even fee, and the terminal table.

*First-run outcomes (2026-10-21, recorded after the runs; criteria unchanged).* Country-risk script: India's bond
volatility was taken from Damodaran's p. 100 formula line (17) instead of Table 4.5 (15), which this specification gates;
the p. 100 line is itself inconsistent with its printed 7.80 (a further source slip). The hand value 17.107 above is
correct; the script's literal had been mistyped. Concentrated-position script: see the bracketed correction above.

**Records.** Reading notes (Damodaran, MIP, PMiP, Hull); `sources.tex`: the IRC key extended with secs. 351, 704, 721,
737, 1259 (retrieved 2026-10-21) and new keys for Reg. sec. 1.351-1 and Rev. Rul. 2003-7; entry evidence for the three
entries; objective evidence for `estimate-cost-of-debt-and-equity`, `advise-complex-client-situations` and
`analyse-covered-and-protective-positions`; pathway notes; a review record. Counts stay 449/449, 1,030/1,030.

## 8. Backlog (needs evidence before it is scheduled)

| ID | Item | What is needed first |
| --- | --- | --- |
| B1 | Kolmogorov forward and backward equations, transition densities | Decide whether it adds teaching beyond P1; Wilmott chap. 10. Forward equation read 2026-10-21 (sec. 10.4, p. 172; C1-F2); deferred |
| B2 | Lookback options | Hull sec. 26.11, Wilmott chap. 26; low priority. C1 (2026-10-21): distinct, C1-N1, proposed for L5. **Done in L5 (2026-10-21)** |
| B3 | Monte Carlo Greeks (pathwise, likelihood ratio) | Hull sec. 21.7 and Glasserman (not held); could be one entry. Proposed for L4 (L4-a, 2026-10-21): Hull sec. 21.6, pp. 494-495 and Broadie and Glasserman (1996) read instead; one new entry and objective. **Done in L4 (2026-10-21)** |
| B4 | Second-order Greeks beyond the P4 sentence (vanna/volga hedging, the vanna-volga method) | A source for market practice |
| B5 | Discrete-hedging error distribution and transaction costs (Wilmott chaps. 47-48) | Overlap check with P4 and `mod:black-scholes-merton`. C1 (2026-10-21): discrete error already in P4; transaction costs distinct, C1-N2, proposed for L5. **Transaction costs done in L5 (2026-10-21)** |
| B6 | CAIA depth: CTA industry structure and vehicles (chaps. 29, 32), payoff-distribution and bottom-up replication (chap. 33), convertible arbitrage risks (chap. 34) | Owner decision on a CAIA citation exception, or non-curriculum sources (Kat and Palaro; Hasanhodzic and Lo) located and read. No own empirical CTA performance. A trend illustration is synthetic; an empirical futures backtest needs a defined continuous-contract roll rule, collateral return, a signal lag of $t-1$ information, and costs |
| B7 | (Done in Batch L3, 2026-10-21.) Regulatory currency P10: FRTB status by jurisdiction (BCBS, EU CRR3, UK PRA, US); SA-CCR and the revised CVA framework (CRE52, MAR50); ISSB IFRS S1/S2 adoption, TCFD's transfer to the ISSB, SEC climate-rule status; LCR/NSFR dates in `financial-institution-analysis.tex` | The issuers' current texts read with retrieval dates; corrections to existing entries plus at most one `rule:` entry for counterparty capital |
| B8 | LIBOR-era CQF and Gregory material | Historical only; used solely as dated context in P6-P7 |
| B9 | Empirical EVT illustration | A daily return series with a documented source, dates and licence |
| B10 | "Monte Carlo Methods.pdf" | Identify author and edition (OCR or bibliographic match) only if B3 needs it. Closed by C1: B3 was done in L4 without it |
| B11 | C0 findings | Done: Section 8.1; the items not placed in L2 are B12-B17 |
| B12 | Variance swap valued during its life: time-weighted realised and implied variance, discounted (C0 candidate 6) | Extends `meth:volatility-derivative-applications`; read `wide-demeterfi-varswaps` (catalogue, DOI; not held). Proposed for L4 (L4-b, 2026-10-21): the authors' GS note read; the seasoned formula is a labelled derivation (L4-D2); no new objective. **Done in L4 (2026-10-21)** |
| B13 | Cross-currency basis swap: cash flows, which leg carries the basis, synthetic funding (candidate 6) | Extends `meth:swap-valuation-replication` or `res:international-parity-conditions`; read `cur-borio-mccauley-mcguire-sushko-2016` (BIS, open). Proposed for L4 (L4-c, 2026-10-21): BIS pp. 45-48, Hull secs. 7.10 and 34.3, and Ding-Liu-Rutkowski (arXiv v3) read; a new entry, no new objective; MTM resets excluded. **Done in L4 (2026-10-21)** |
| B14 | Crisis-conditional hedge fund factor exposures (state-dummy interactions) and screening collinear factors (candidate 11) | Extends `meth:hedge-fund-factor-exposures`; the curriculum's source, Hasanhodzic and Lo (2007), is neither catalogued nor held. A non-curriculum source is needed, or the owner accepts an Interpretation |
| B15 | Option-strategy practice: the move implied over a horizon, $\sigma\sqrt{h/252}$, against a straddle's break-even; put writing to buy at $K-p$; skew (90/110) and term-structure (12M-3M) gauges (candidate 5) | Extends `meth:option-spreads-volatility-strategies` and `meth:covered-call-protective-put`; check `s7-natenberg` first |
| B16 | Life insurance pricing: net and gross premium, level term, policy reserve, net payment and surrender cost indexes (candidate 12) | Extends `meth:human-capital-risks`; no non-curriculum source located (mortality tables and an actuarial text needed) |
| B17 | Economics of regulation: kinds of regulator, regulatory competition and arbitrage, the Coase theorem, cost-benefit analysis (candidate 13) | Extends `def:market-regulation-design` or the economics chapter; locate the relevant chapters of `openstax-microeconomics-3e` (registered) |

### 8.1 C0 findings (2026-10-21)

**Library.** The 18 volumes of the 2024 curriculum, six for each level, are at
`/Users/lxg/Documents/CFA & Finance/Exam/CFA/CFA Level {1,2,3}/2024[ Notes]/`. Their identity
was verified from each title page ("2024 • LEVEL n • VOLUME m"), the ©2023 CFA Institute
copyright page and the ISBNs, which run from 978-1-953337-49-8 (L1 vol. 1) to -66-5 (L3 vol. 6).
Text was extracted to the session scratchpad. The library was not modified, and no curriculum
text entered the repository. Locators below are PDF pages.

**Pass 1 (titles and section heads).**
- Reading titles: complete. There are 175 learning modules, including two appendices.
  Matching them to the 203 crosswalk modules leaves 34 without a close title match. Most of
  those are renamed versions of mapped modules, for example "Rates and Returns".
- Second-level heads (about 1,480; L3 vol. 4 parsed from its contents pages, which mix
  levels):
  - screened against entry text by keyword for all volumes. The screen was noisy: 519 heads
    were flagged, so it was used only to find candidates;
  - compared by hand for 76 modules (491 heads): quantitative methods, fixed income,
    derivatives, L2 portfolio and risk readings, and L3 vols. 2-3 and the derivatives,
    hedge-fund, alternatives and trading readings.

  Keyword hits were not counted as coverage or as gaps.

**Pass 2 and the cap.** 15 substantive reviews, the cap. The six required readings are
candidates 1-6. The pages listed in the second column were read; the rest of each reading was
seen only at heading level.

| # | Reading (2024; PDF pages read) | Existing entries compared | Outcome | Gap, support and placement |
|---|---|---|---|---|
| 1 | L2 vol. 5, Valuation of Contingent Claims (pp. 94-153) | `meth:multi-period-binomial-valuation`, `meth:black-model-rates-currencies`, `meth:greeks-delta-gamma-hedging`, `mod:black-scholes-merton`, `def:implied-volatility-surface` | Already explained, with two small depth gaps | Discrete dividends and dividend-motivated early exercise of an American call (p. 113); receiver swaption, payer-receiver parity, callable bond less receiver swaption (pp. 138-139). Hull OFOD sec. 21.3 and sec. 29.3 (in repository, not read in C0). Optional L2 extensions (L2-D5) |
| 2 | L2 vol. 4, The Arbitrage-Free Valuation Framework (pp. 421-453) | `meth:arbitrage-free-bond-valuation`, `meth:binomial-rate-tree-calibration`, `mod:term-structure-models-simulation` | Already explained, with depth gaps | Calibrating simulated paths by a drift adjustment (p. 446); the lognormal KWF model and the multi-factor Gauss+ model are named (pp. 451-452); CIR is only stated. Goes into P6 |
| 3 | L2 vol. 4, The Term Structure and Interest Rate Dynamics (pp. 370-397; pp. 356-369 at heading and example level) | `meth:forward-rates-expected-returns`, `meth:spot-par-forward-curves`, `def:swap-curve-short-term-spreads`, `res:term-structure-theories`, `meth:yield-curve-factor-exposures` | Already explained (the entries go further) | None for L2; the proportional yield-volatility term structure (p. 391) is minor |
| 4 | L2 vol. 4, Credit Analysis Models (pp. 569-584; pp. 552-568 at heading level) | `meth:risky-bond-cva`, `mod:structural-reduced-form-credit`, `meth:credit-spread-term-structure`, `meth:rating-migration-returns` | Depth gap | CVA from node-weighted exposure on a calibrated tree; the effect of rate volatility on CVA; default probability and recovery that vary by year; risky-floater value and discount margin solved on the tree (pp. 573-584). Source gap: Smith (2017) not held; FIA 2015 chap. 6 lacks it. P7 extension, L2-D3 |
| 5 | L3 vol. 2, Options Strategies (pp. 58-78; the rest at heading level) | `meth:option-replication-deltas`, `meth:covered-call-protective-put`, `meth:option-spreads-volatility-strategies`, `ex:option-strategy-selection-case`, `meth:volatility-derivative-applications` | Already explained; minor depth | Implied move against straddle break-even (p. 59); put writing (pp. 67-68); skew and term-structure gauges (pp. 60-62). B15 |
| 6 | L3 vol. 2, Swaps, Forwards, and Futures Strategies (pp. 100-120; the rest at heading level) | `meth:forward-commitment-risk-overlays`, `meth:derivative-overlay-allocation`, `meth:rate-bond-forward-valuation`, `def:vix-variance-dividend-swaps` | Already explained, with two depth gaps | Variance swap valued during its life (p. 120); cross-currency basis swap mechanics (pp. 105-108). B12, B13 |
| 7 | L1 vol. 1, Parametric and Non-Parametric Tests of Independence (pp. 253-264) | `meth:nonparametric-tests`, `meth:hypothesis-testing`, `def:return-dependence` | New idea (no objective; dropped from the 2026/2027 outlines) | Correlation $t$-test, Spearman test, chi-square test of independence. `introductory-statistics-2023` and `statistical-methods-handbook` registered (located, not read). P11a |
| 8 | L2 vol. 4, Credit Default Swaps (pp. 636-643) | `meth:cds-pricing`, `meth:cds-strategies`, `def:cds-contract-features` | Already explained (the entries go further) | None |
| 9 | L2 vol. 4, Bonds with Embedded Options (pp. 496-512, 520-522) | `meth:option-adjusted-spread`, `meth:embedded-option-effective-duration`, `meth:callable-putable-bond-valuation`, `meth:convertible-bond-valuation`, `meth:capped-floored-floater-valuation` | Already explained | None |
| 10 | L3 vol. 4, Asset Allocation to Alternative Investments (pp. 160-170) | `meth:alternatives-allocation-approaches`, `mod:mean-variance-portfolio-optimisation` | New idea; a depth gap | Mean-CVaR optimisation (pp. 167-169): `s6-cvar` catalogued, open PDF (located, not read), P11b. Long-horizon goal-probability simulation (pp. 160-164) is already near the existing Monte Carlo and planning entries; not placed |
| 11 | L2 vol. 5, Hedge Fund Strategies: the conditional factor model (pp. 376-380, 393-398) | `meth:hedge-fund-factor-exposures` | Depth gap | Crisis-dummy betas and stepwise screening of collinear factors (pp. 377-378). No source held. B14 |
| 12 | L3 vol. 4, Risk Management for Individuals (pp. 399-409) | `meth:human-capital-risks`, `meth:lifetime-exposures` | Depth gap (peripheral) | Net and gross premium, reserves, cost indexes (pp. 405-409). No source. B16 |
| 13 | L2 vol. 1, Economics of Regulation (pp. 556-572) | `def:market-regulation-design` | Depth gap (peripheral) | Classification of regulators, competition and arbitrage, the Coase theorem, cost-benefit analysis. B17 |
| 14 | L1 vol. 3, Market Organization and Structure: leveraged positions (pp. 285-288) | `mech:securities-lending-short-sale` (short-sale margin only) | New idea (small) | Leverage ratio, levered return, margin-call price. `ecfr-12cfr220` and `finra-rules-2026` registered (not reread). P11c |
| 15 | L2 vol. 5, Measuring and Managing Market Risk (pp. 540-548) | `meth:portfolio-var-methods-decomposition`, `meth:var-es-estimation-methods`, `meth:sensitivity-scenario-risk-measures` | Already explained | None; the curricula only name EVT (L1 vol. 6, p. 164; L3 vol. 4, p. 156), so P9 rests on Section 3.1 |

**Investment Series as support.**
- *Fixed Income Analysis* (2015): chapter list and the section heads of chap. 6 were
  examined. It does not support candidate 4.
- *Derivatives* (2017): chapter list only.
- *Quantitative Investment Analysis* (2007): no text layer, so it was not searched.

None was read substantively, and none is needed by a proposed L2 package.

**Left unexamined because the cap was reached:**
- Title-pass candidates: L1 Probability Trees and Conditional Expectations; Market
  Efficiency; Security Market Indexes; Overview of Equity Securities; Equity Valuation:
  Concepts and Basic Tools; Introduction to GIPS; Ethics Application. L2 Financial Statement
  Modeling. L3 Passive Equity Investing; Topics in Private Wealth Management; the two Case
  Studies in Risk Management.
- Hand comparison of section heads in the remaining 97 modules (financial statements,
  corporate issuers, equity valuation, economics, ethics, CME and asset allocation, private
  wealth, institutional).

Each title-pass candidate has a renamed or near counterpart in the crosswalk or in
`objectives.json`, but that was not confirmed by reading.

### 8.2 C1 gap inventory (2026-10-21)

Discovery only: no teaching entry, objective or coverage claim was written, and no curriculum text entered the
repository. Curriculum volumes were used to find gaps, never as support; support was checked in registered or held
non-curriculum sources. This inventory covers the inspected corpus below, not the whole finance library.

**Corpus and reconciliation.** The same 18 volumes as C0 (2024 Level I-III, six each; Level II in the `2024 Notes`
folder), read-only, text extracted to the session scratchpad (9,530 pages). Their contents pages list 175 numbered
learning modules. Two are statistical tables ("Appendices A-E", L1 vol. 1 and L2 vol. 1), so 173 are substantive; the
"Appendix" headings inside L2 vol. 1 (currency module) and L3 vol. 6 (Asset Manager Code) are sections, not modules.
C0 recorded 76 modules compared by hand and 97 remaining, which sums to 173: C0's "175 ... including two appendices" is
consistent once the appendices are excluded. C0 named its 76 by category, not by module. Its categories reproduce
exactly 76 when read as: quantitative methods (L1 11, L2 7), fixed income (L1 19, L2 5), derivatives (L1 10, L2 2), the
four L2 vol. 5 portfolio and risk modules, L3 vols. 2-3 (11), and the alternatives and trading modules of L2 vol. 5 (4),
L3 vol. 4 (2) and L3 vol. 5 (1). The remaining 97 are then: economics (L1 8, L2 3), corporate issuers (L1 7, L2 4),
financial statement analysis (L1 12, L2 7), equity (L1 8, L2 6), portfolio management (L1 6, L2 2), L1 alternatives (7),
ethics and GIPS (L1 5, L2 3, L3 5), L3 vol. 1 (5), private wealth (L3 3) and L3 vol. 5 institutional, performance,
manager selection and the three cases (6). This reconstruction fits C0's count and wording but is not proof of which
modules C0 read; C0's three substantive reviews in the 97 (candidates 12-14) are reused.

**Method.** (1) Each of the 97 titles matched against the 203 crosswalk modules: 78 have a same-titled 2026/27 module
whose items are all mapped to covered objectives; 19 do not (renamed, merged or dropped modules, the cases and the
ethics guidance). A match is a pointer, not a review. (2) The 2,231 non-generic section heads were screened for words
absent from the compendium (74 flagged, mostly case names); the screen only shortlists. (3) By hand, every module's heads
were compared with entry titles and, where a concept looked thin, with entry text; substantive curriculum passages
were opened only to locate a gap. (4) Each candidate was checked against existing objectives (granularity follows the
compendium: one objective per distinct capability, as for digital, barrier and Asian options) and against L1-L4.
(5) Support was checked in held or registered sources; the 13 C0 title-pass candidates were resolved in the same pass.

**Outcome for the 97 modules.** 93 are already explained by existing entries (for example market structures,
cycles, fiscal and monetary policy, geopolitics, the FSA chapter including translation, CAMELS and insurers, payout,
restructuring, equity valuation models, CME, asset allocation including Black-Litterman, surplus optimisation and
risk parity, attribution, manager selection, GIPS and the ethics chapter). The 13 C0 title-pass candidates all have
counterparts: probability trees (`def:conditional-moments`, `meth:bayesian-updating`), market efficiency
(`def:market-efficiency`, `mech:biases-market-anomalies`), indexes (`meth:index-value-return-calculation`), equity
securities, equity valuation tools, GIPS, ethics application, FS modelling, passive equity, the two risk-management
cases (`meth:swf-risk-case`, `meth:lifetime-exposures`, `ex:investment-planning-case`), and Topics in Private Wealth
Management except item D2 below. Depth gaps were found in four modules (D1, D2, and the reused B16-B17).

**Candidates** (IDs C1-N distinct, C1-D depth, C1-U unresolved; curriculum discovery locators are printed pages from the 2024 contents pages; C0's table used PDF pages).

| ID | Concept (neutral) | Related entries / objectives | Missing teaching | Discovery; source status | Objective effect | Dependencies; batch |
|---|---|---|---|---|---|---|
| C1-N1 (B2) | Lookback options: floating and fixed strike, valuation during life with the running extreme, discrete against continuous monitoring | `meth:barrier-option-valuation`, `meth:asian-option-valuation`; `objective:value-barrier-options-monitoring` | No lookback anywhere in the compendium | Backlog B2; Wilmott chap. 26 (from printed p. 445; located in the contents, not read) and the lookback passages of chap. 24 (PDF pp. 443-447, read); Hull sec. 26.11 pp. 623-625, formulas and Example 26.2 (7.79 put, 8.04 call) read | **+1** (`objective:value-lookback-options`), matching the per-exotic objectives | Barrier entry (monitoring shift), MC entries; L5 |
| C1-N2 (B5) | Hedging options with proportional transaction costs: Leland's adjusted volatility, its sign for long and short positions, the Hoggard-Whalley-Wilmott portfolio equation, and rebalancing rules | `res:delta-hedging-volatility-mismatch` (assumes no costs), `meth:greeks-delta-gamma-hedging`; `objective:quantify-hedging-volatility-mismatch` | Costs appear only as an assumption ("no costs"); the earlier `meth:leland-cost-adjusted-volatility` question was blocked for lack of Leland (1985) | Backlog B5; Wilmott chap. 48 pp. 783-812 (sec. 48.3 Leland, pp. 784-785; HWW; strategy comparison) located and opening pages read; `vo-leland-1985` catalogued, not held | **+1** (`objective:hedge-options-with-transaction-costs`) | P4 entry and its script; L5 |
| C1-D1 (done in L6, 2026-10-21) | Country risk premium in the cost of equity: sovereign default spread, relative-volatility scaling, melded approach | `meth:cost-of-debt-equity-estimation`, `meth:capital-structure-benchmarking` ("country risk" listed only); `objective:estimate-cost-of-debt-and-equity` | No method or example | L2 vol. 3, Cost of Capital: Advanced Topics, "International Considerations" (pp. 119 and 139); `applied-corporate-finance-2014` printed pp. 98-107 (PDF 114-123) located, passages read | 0 (depth) | None; a later small depth batch |
| C1-D2 (done in L6, 2026-10-21) | Concentrated single-stock positions: risk and tax trade-off, staged diversification and completion portfolios, zero-premium collars, variable prepaid forwards, exchange funds, charitable remainder trusts | `meth:complex-client-situations`, `meth:wealth-transfer-strategies`, `meth:covered-call-protective-put`; `objective:advise-complex-client-situations` | Concentration is named; hedging and monetisation strategies are not taught | L3 vol. 4, Topics in Private Wealth Management (pp. 310-323); `managing-investment-portfolios-2007` Example 11-3 and Exhibit 11-4, pp. 693-695 read; Hull collars (held); US constructive-sale and exchange-fund rules (IRC secs. 1259, 721) not yet read | 0 (depth) | Option-strategy entries; later depth batch |
| C1-D3 (B15) | Option-strategy practice: horizon move against straddle break-even, put writing to buy below market, skew and term-structure gauges | `meth:option-spreads-volatility-strategies`, `meth:covered-call-protective-put` | Short practical items | C0 candidate 5; `s7-natenberg` held, relevant pages not yet located. *Corrected (C1-F2): unsupported; held, not located or read* | 0 (depth) | Optional with L5; excluded by L5-D1, deferred |
| C1-D4 (B1) | Forward (Fokker-Planck) Kolmogorov equation and transition densities | `res:risk-neutral-pricing-feynman-kac` (backward equation already from Wilmott chap. 10) | The forward equation only | Backlog B1; Wilmott chap. 10 (held; secs. 10.11-10.12 already read). *Corrected (C1-F2): those sections are the backward equation; the forward equation is sec. 10.4, printed p. 172, eq. (10.2), read 2026-10-21 (pp. 169-175); now supported* | 0 (depth); low priority | None; deferred |
| C1-U1 (B4) | Vanna-volga smile construction and pricing | `meth:greeks-delta-gamma-hedging` (vanna, volga), `def:implied-volatility-surface` | The method itself | Backlog B4; `cur-bossens-rayee-skantzos-deelstra-2010` and `cur-castagna-fx-smile` catalogued, neither held nor read | Possibly +1; unresolved until a source is read | Smile entries |
| C1-U2 (B6) | Hedge-fund replication (factor and payoff-distribution), CTA structure, convertible-arbitrage risks | `meth:hedge-fund-factor-exposures`, `meth:hedge-fund-strategy-classification` | Replication methods; CTA vehicles | Backlog B6; CAIA chaps. 29, 32-34 held but need an owner decision on citing CAIA; Kat-Palaro, Hasanhodzic-Lo not held | Possibly +1 (replication); rest depth | Owner decision |
| C1-U3 | Depth without a source: conditional hedge-fund betas (B14), life-insurance pricing (B16), economics of regulation including antitrust (B17; `openstax-microeconomics-3e` registered, chapters not located), incapacity planning (L3 vol. 4, p. 345), an empirical EVT illustration (B9, needs data) | as in Section 8 | as in Section 8 | as listed | 0 each | Source or data first |

Closed without action: B8 (historical context only), B10 (moot after L4 used Broadie-Glasserman), C0's minor items
(proportional yield volatility; KWF and Gauss+ named only).

**Counts (inspected corpus only).**
1. Implemented objectives: **447**.
2. Confirmed distinct candidate objectives: **2** (C1-N1, C1-N2).
3. Depth extensions adding no objective: four (C1-D1 to C1-D4), plus five unsourced depth items in C1-U3. *Corrected
   (C1-F2):* C1 wrote "4 source-supported". By evidence: C1-D1 supported (read); C1-D2 partly supported (one source
   read, tax rules not read); C1-D3 unsupported (source held, passages not located); C1-D4 supported only after the
   pre-L5 reading of Wilmott sec. 10.4.
4. Unresolved candidates: **2** that might add an objective (C1-U1, C1-U2) and the five depth items of C1-U3.
5. Provisional total for this corpus: **449** (447 + 2); at most 451 if C1-U1 and C1-U2 are both confirmed. This does
   not exhaust the finance library; the 45-objective preference was not used as a target.

## 9. Records for each package

- `compendium/front/sources.tex`: no entry for catalogue keys such as `wide-wilmott-pwoqf`,
  `s7-hulloptions` or `ev-kelly-1956`, because `tools/check_compendium.py` (lines 149-156)
  resolves them from the guide catalogue, as it does for the existing `s7-hulloptions`
  citations. Non-catalogue sources (for example Gregory 3rd ed. in Batch L2) are registered
  with neutral key names as in v1 Section 33.
- Wilmott's edition (2nd ed., 2006, three volumes, ISBN 978-0-470-01870-5) and its offset
  (printed page $=$ PDF page $-21$) go in its new reading note.
- `notes/readings/<key>.md`: a new or extended reading note with locators and limits (Wilmott;
  Hull OFOD sections added to `s7-hulloptions.md`).
- `notes/entry-evidence.json`: one record per new or changed entry.
- `notes/source-review-records.md`: a section *Library gap-filling, Batch L1* with sources
  read, discrepancies (for example Wilmott's forward-time FD notation against Hull's) and the
  check results.
- `notes/pathways/`: entries added to `common-toolkit.md`, `volatility-options.md`,
  `option-pricing-models.md` and `portfolio-construction.md`.
- `notes/coverage/objectives.json` (if E1 is accepted): new neutral objectives with entries,
  sources and evidence; the outline crosswalk is unchanged, as these objectives have no
  outline items.
- `implementation_plan.readme`: a short Section 37 pointing to this file, with the batch
  outcome.

## 10. Decisions

### 10.1 Essential (owner input needed before Batch L1 starts)

- **E1. Coverage denominator.** Recommended: add ten new neutral objectives for Batch L1's new
  ideas, so the total becomes 434 and is reported as a denominator change. The alternative is
  to record the new entries in entry evidence only, with no objective count. Under Section
  17.4 only newly covered objectives count, and all 424 existing objectives are covered, so
  without E1 no batch in this plan counts towards the 45.
- **E2. Batch L1 size against the 45 preference.** Batch L1 yields 10 newly covered
  objectives, a shortfall of 35. The whole verified programme (Batch L1, the proposed Batch
  L2 and P10) is about 20, plus whatever C0 finds, so 45 cannot be reached honestly in one
  prompt. Recommended: approve Batch L1 as frozen and report the shortfall under Section
  17.4. Alternative: merge P6-P9 into Batch L1 (about 18-19 objectives). That brings more
  review load and starts the credit and rates work before C0 has run.

### 10.2 Routine choices (defaults; no input needed unless the owner objects)

- **Branch.** Implementation starts on a new branch. If PR #33 is still open, the branch is
  stacked on its head `2b89791`; otherwise it starts from `main` after the merge. This
  conversation changes no branch.
- **Topics.** A new `topic:stochastic-calculus` (section `common-toolkit`) for P1's three
  objectives; P2-P4 under `topic:option-valuation`; P5 under `topic:portfolio-risk-return`;
  `planned_batch` 7 for Batch L1.
- **Labels and paths.** As listed in Section 6. They were checked against the label schema;
  none is in use and none of the three new files exists. Check scripts go in new folders
  `stochastic-calculus/`, `numerical-pricing/` and `exotic-options/`, and in the existing
  `option-valuation/`, `portfolio-construction/` and `inference-simulation/`, all matched by
  the `make examples` pattern.
- **Citation policy.** Unchanged (Section 2). Batch L1 needs no exception.

### 10.3 Decisions needed to freeze Batch L2 (after C0)

**Owner decisions, 2026-10-21 (Batch L2 frozen).** L2-D0: everything stays local (no push, PR
or merge); L2 is implemented on `codex/library-gap-batch-l2`, created from `c688d54`. L2-D1:
P6-P9 approved with the two freeze corrections (Section 7, "Batch L2 freeze corrections").
L2-D2: P11a-c included. L2-D3: option (a), the rate-tree CVA and risky floater as an
explicitly labelled original derivation that combines the cited tree and CVA foundations, read
first; Smith (2017) is not held and is not implied to have been read. L2-D4: P10 deferred to
Batch L3. L2-D5: both optional Hull extensions included, after their passages are read.
L2-D6: about 11 new objectives accepted; the actual shortfall against 45 is reported without
padding. The options below are kept as they were put to the owner.

- **L2-D0. Batch L1 first.** Resolved for the commit: L1 and its audit repairs were committed
  locally as `5e0578e` with the owner's authorisation. Still open: whether to push it and
  open or update its PR, and whether L2 continues on this branch or branches from
  `5e0578e`.
- **L2-D1. P6-P9 as specified in Section 7, with the criteria C0 added as corrected after
  the audit.** Recommended: freeze them. The alternative is to drop P8 or P9 for a smaller
  batch; each removes 1-2 objectives.
- **L2-D2. P11 (three new ideas found by C0) in Batch L2.** Recommended: include it. Each idea
  is genuinely absent from the compendium, has a registered or open source and adds one
  objective. They are outside L2's rates-and-credit theme, so the alternative is a separate
  small batch.
- **L2-D3. Tree-based CVA and the risky floater, with no direct source held.** Options:
  - (a) write it as an Interpretation that combines the cited tree
    (`meth:binomial-rate-tree-calibration`) with the cited CVA formula (RMFI pp. 395-396),
    using original inputs. Recommended; it adds no objective;
  - (b) obtain and read Smith (2017) first;
  - (c) move it to the backlog.
- **L2-D4. P10 (regulatory currency, B7).** Recommended: Batch L3. It needs a different kind
  of evidence (current issuer texts in four jurisdictions) and is mainly corrections to
  existing entries, adding about one objective. The alternative is to add it to L2 (about 12
  objectives).
- **L2-D5. Optional Hull extensions** (receiver swaption and parity; discrete dividends in
  trees). Recommended: include them. Both sources are in the repository, and they add no
  objective.
- **L2-D6. Size.** Batch L2 would cover about 11 new objectives, a shortfall of about 34 against
  the standing 45. Recommended: approve and report the shortfall, as under E2. Reaching 45
  would need the backlog items that lack sources, or padding.
- **Routine defaults** (no input needed unless the owner objects):
  - `planned_batch` 8.
  - Check scripts in new folders `short-rate-models/`, `counterparty-xva/`,
    `default-correlation/` and `extreme-value/`, and in the existing `inference-simulation/`
    (P11a), `portfolio-construction/` (P11b) and `short-term-funding/` (P11c). All are matched
    by the `make examples` pattern.
  - Network reads of CRE31, `s6-cvar`, Regulation T and FINRA Rule 4210 during their packages.
    They are reads of public pages, recorded with retrieval dates; nothing is published.

### 10.4 Decisions needed to freeze Batch L4

*Decided 2026-10-21: L4-D1 all three packages; L4-D2 option (a), with the contract and approximation assumptions
stated; L4-D3 no new objective. The options below are kept for the record.*

Only these change what is built. Everything else in the L4 proposal is a routine default.

- **L4-D1. Scope.** Recommended: freeze L4-a, L4-b and L4-c as proposed (two new entries, one extension, one new
  objective, shortfall 44). Alternative: L4-a only, keeping B12-B13 in the backlog.
- **L4-D2. B12's seasoned-swap formula without a printed source.** Recommended: (a) write it as a labelled
  Interpretation derived from Demeterfi et al.'s definitions (EQ 14-16, additivity) and Hull eq. (26.7), checked by the
  limits, units and an independent simulation. Alternatives: (b) obtain and read `w5-bossu-advanced-equity` or
  `wide-bennett-trading-vol` first (neither held; no purchase is authorised); (c) defer B12.
- **L4-D3. B13's objective.** Recommended: no new objective (depth within `objective:value-swaps-by-replication` and
  `objective:apply-international-parity`). Alternative: add `objective:explain-cross-currency-basis-swaps` (+1, shortfall
  43).

Routine defaults (no input needed unless the owner objects): implement on a new local branch from this proposal's
commit; `planned_batch` 9; scripts in `numerical-pricing/` and `derivative-overlays/`; Broadie and Glasserman (1996)
registered under a neutral key; no push or PR.

### 10.5 Decisions needed to freeze Batch L5

*Decided 2026-10-21: L5-D1 L5-a and L5-b only (+2), L5-c excluded; L5-D2 Leland through Wilmott chap. 48, Leland named
as originator, the paper not implied to have been read; L5-D3 C1-D1 and C1-D2 deferred, other backlog items deferred.
The options below are kept for the record.*

- **L5-D1. Scope.** Recommended: L5-a and L5-b (+2). Alternatives: add L5-c (Natenberg depth, +0), or one package only.
- **L5-D2. Leland (1985) through Wilmott.** Recommended: cite the model through Wilmott chap. 48, which derives it, and
  name Leland as the originator; alternative: obtain `vo-leland-1985` first (not held; no purchase authorised).
- **L5-D3. Depth items C1-D1 and C1-D2** (country risk premium; concentrated positions). Recommended: a separate small
  depth batch after L5, since they belong to other chapters; alternative: add them to L5 (+0 objectives).

Routine defaults: new local branch from the commit that records this proposal; `planned_batch` 10; no push or PR.

## 11. Sequence

1. Owner decides E1 and E2. Done.
2. Batch L1: P1, P2, P3, P4, P5, each with focused checks and records before the next. Done,
   with the five audit corrections; committed locally as `5e0578e`.
3. Batch L1 integration checks and completion report; commit and PR only when the owner asks.
   Checks, report and local commit done; push and PR not done (L2-D0).
4. C0 (bounded) adds its findings to Section 8 and proposes the Batch L2 scope. Done
   (Sections 7 and 8.1), with its acceptance criteria corrected after audit.
5. Owner freezes Batch L2 (Section 10.3). P10 (B7) goes in Batch L2 or L3 (L2-D4). Done: frozen 2026-10-21; P10 to L3.
6. Batch L2: P6, P7, P8, P9, P11a-c, each with focused checks and records before the next. Done 2026-10-21 (frozen with
   decisions L2-D0 to L2-D6); committed locally on `codex/library-gap-batch-l2`. Next: Batch L3 (P10), human review.
7. Batch L3: P10 (B7), frozen and executed 2026-10-21 on `codex/library-gap-batch-l3`; committed locally. Audit corrections L3-F1 to L3-F5 committed separately on `codex/library-gap-l3-audit-fixes`. Next: human review; no further batch is scheduled.
8. L3 wording correction (CSRD first wave) and the Batch L4 proposal, 2026-10-21, on `codex/library-gap-l4-proposal`;
   committed locally as `95c547a`.
9. Batch L4 frozen with corrections L4-C1 to L4-C3 and implemented, 2026-10-21, on `codex/library-gap-batch-l4`;
   one local commit.
10. C1 pass, 2026-10-21, on `codex/library-gap-c1-inventory`: three L4 corrections (Section 7), the C1 gap inventory
    (Section 8.2) and the Batch L5 proposal (Section 7; decisions in Section 10.5); one local commit. Next: owner
    freeze of L5; human review of L1-L4 outstanding.
11. Pre-L5 audit corrections C1-F1 and C1-F2, then Batch L5 frozen (L5-D1 to L5-D3) and implemented, 2026-10-21, on
    `codex/library-gap-batch-l5` from `main` (`c26a09e`); local commits. 449/449 objectives. Next: human review of
    L1-L5; deferred: C1-D1, C1-D2, C1-D3, C1-D4 as an entry, C1-U1 to C1-U3.
12. L5 clarifications and Batch L6 (C1-D1, C1-D2; +0 objectives), 2026-10-21, on `codex/library-gap-batch-l6` from
    `af47d03`; local commits. Next: human review of L1-L6; deferred: C1-D3, C1-D4 as an entry, C1-U1 to C1-U3.

## 12. Risks and limits

- Wilmott 2006, Gregory 2015, the CQF 2016 packs and CAIA 2012 predate the LIBOR transition,
  the post-2017 Basel reforms and the ISSB. Their concepts are durable; their market and
  regulatory statements are used only as dated history.
- Several catalogue texts are not held locally; entries do not cite what was not read.
- The planning-run numbers in Section 6 come from small exploratory calculations outside the
  repository. The package scripts recompute them; the acceptance ranges, not the planning
  values, are binding.
- Editorial coverage is not study. Human review of all new entries is still outstanding.
- The L4 proposal rests on the passages listed in its source table only; unread parts (Broadie-Glasserman pp. 276-279,
  BIS pp. 49-58, the *J. Derivatives* and *SIAM* versions) are not cited. Planning values are exploratory, not evidence.
- L4's seasoned variance-swap value and the annualised basis mapping are Interpretation, checked for consistency and
  against an independent simulation or exact identities, not quoted from a source. The cross-currency example uses
  assumed fixings with exact accrual; real ACT/360 compounding in arrears, collateral and curves are not modelled.
- The C1 inventory compared section heads by hand and opened curriculum passages only to locate gaps; a heading that
  looks explained may still hide depth. C0's 76 modules were not recompared (their membership is reconstructed from
  C0's categories). The inventory covers the 18 volumes and the backlog, not the whole finance library.
- L5's Leland comparison rests on Wilmott's presentation; Leland (1985) was not read. The lookback monitoring gaps are
  for one parameter set; no discrete-monitoring correction for lookbacks was read, so none is taught. The
  Hoggard-Whalley-Wilmott equation is stated, not solved.
- C0 is a bounded sample, not a census. Hand comparison of section heads covered 76 of 175
  modules, and the unexamined candidates are listed in Section 8.1. A gap that C0 did not find
  may still exist.
