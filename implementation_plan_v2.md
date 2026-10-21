# Compendium gap-filling from the owner's finance library: implementation plan v2

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
| CAIA depth, lookbacks, Kolmogorov equations, second-order Greeks beyond a sentence, MC Greeks, others | B1-B10 | Backlog |
| C0 depth gaps not placed in L2 | B12-B17 | Backlog |

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

## 8. Backlog (needs evidence before it is scheduled)

| ID | Item | What is needed first |
| --- | --- | --- |
| B1 | Kolmogorov forward and backward equations, transition densities | Decide whether it adds teaching beyond P1; Wilmott chap. 10 |
| B2 | Lookback options | Hull sec. 26.11, Wilmott chap. 26; low priority |
| B3 | Monte Carlo Greeks (pathwise, likelihood ratio) | Hull sec. 21.7 and Glasserman (not held); could be one entry |
| B4 | Second-order Greeks beyond the P4 sentence (vanna/volga hedging, the vanna-volga method) | A source for market practice |
| B5 | Discrete-hedging error distribution and transaction costs (Wilmott chaps. 47-48) | Overlap check with P4 and `mod:black-scholes-merton` |
| B6 | CAIA depth: CTA industry structure and vehicles (chaps. 29, 32), payoff-distribution and bottom-up replication (chap. 33), convertible arbitrage risks (chap. 34) | Owner decision on a CAIA citation exception, or non-curriculum sources (Kat and Palaro; Hasanhodzic and Lo) located and read. No own empirical CTA performance. A trend illustration is synthetic; an empirical futures backtest needs a defined continuous-contract roll rule, collateral return, a signal lag of $t-1$ information, and costs |
| B7 | (Done in Batch L3, 2026-10-21.) Regulatory currency P10: FRTB status by jurisdiction (BCBS, EU CRR3, UK PRA, US); SA-CCR and the revised CVA framework (CRE52, MAR50); ISSB IFRS S1/S2 adoption, TCFD's transfer to the ISSB, SEC climate-rule status; LCR/NSFR dates in `financial-institution-analysis.tex` | The issuers' current texts read with retrieval dates; corrections to existing entries plus at most one `rule:` entry for counterparty capital |
| B8 | LIBOR-era CQF and Gregory material | Historical only; used solely as dated context in P6-P7 |
| B9 | Empirical EVT illustration | A daily return series with a documented source, dates and licence |
| B10 | "Monte Carlo Methods.pdf" | Identify author and edition (OCR or bibliographic match) only if B3 needs it |
| B11 | C0 findings | Done: Section 8.1; the items not placed in L2 are B12-B17 |
| B12 | Variance swap valued during its life: time-weighted realised and implied variance, discounted (C0 candidate 6) | Extends `meth:volatility-derivative-applications`; read `wide-demeterfi-varswaps` (catalogue, DOI; not held) |
| B13 | Cross-currency basis swap: cash flows, which leg carries the basis, synthetic funding (candidate 6) | Extends `meth:swap-valuation-replication` or `res:international-parity-conditions`; read `cur-borio-mccauley-mcguire-sushko-2016` (BIS, open) |
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

## 12. Risks and limits

- Wilmott 2006, Gregory 2015, the CQF 2016 packs and CAIA 2012 predate the LIBOR transition,
  the post-2017 Basel reforms and the ISSB. Their concepts are durable; their market and
  regulatory statements are used only as dated history.
- Several catalogue texts are not held locally; entries do not cite what was not read.
- The planning-run numbers in Section 6 come from small exploratory calculations outside the
  repository. The package scripts recompute them; the acceptance ranges, not the planning
  values, are binding.
- Editorial coverage is not study. Human review of all new entries is still outstanding.
- C0 is a bounded sample, not a census. Hand comparison of section heads covered 76 of 175
  modules, and the unexamined candidates are listed in Section 8.1. A gap that C0 did not find
  may still exist.
