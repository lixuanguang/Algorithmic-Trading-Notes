# Compendium gap-filling from the owner's finance library: implementation plan v2

Status: plan only. Written 2026-10-21 (Asia/Singapore) and revised the same day after a
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
(Section 8) that needs evidence before it can be scheduled.

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
| CFA curricula: 2024 Levels I-III (six volumes each), Level II 2020, 2022 and 2023 vol. 1, Level III 2023 box set; Investment Series books | File list only | None | Gap finding in C0 only (not cited) |
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
| Short rates, xVA, default correlation, EVT | P6-P9 | Proposed Batch L2, frozen after C0 |
| Regulatory and disclosure currency | P10 | Proposed Batch L2 or L3 |
| CAIA depth, lookbacks, Kolmogorov equations, second-order Greeks beyond a sentence, MC Greeks, others | B1-B10 | Backlog |

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

### Proposed Batch L2 (frozen only after C0)

Sources are in hand for each package; the substantive passages are still to be read. Each
package states its data and its claims.

- **P6 Short-rate and forward-rate models** (`rates-credit-mortgages/arbitrage-free-valuation.tex`
  after `mod:term-structure-models-simulation`).
  - Two candidate entries: `mod:affine-short-rate-models` (Vasicek and CIR bond formulas,
    Feller condition, Hull-White $\theta(t)$, negative rates) and
    `mod:hjm-forward-rate-models` (HJM drift condition; the forward market model; Black
    caplets; the backward-looking RFR extension, if `gap-rates-backward-term-rates` is
    read).
  - Sources: Hull OFOD chaps. 31-33 (pp. 719-772; the draft's "32-33" omitted chap. 31) and
    Wilmott chaps. 30-31 and 37.
  - Data: the Federal Reserve Board's GSW Svensson parameters (`feds200628.csv`, kept outside
    Git) on 30 September 2026, giving an analytic instantaneous forward curve. The curve is
    labelled "fitted off-the-run nominal Treasury zero curve (GSW)", never SOFR or OIS.
  - Claims: Hull-White's $\theta(t)$ reproduces that curve by construction (zero prices to
    $10^{-10}$; simulated discount factors within 3 standard errors). The mean-reversion and
    volatility parameters are illustrative and stated as not calibrated: calibrating them
    needs cap or swaption volatilities, which are not held.
  - Further checks: the existing Vasicek 0.846849 is reused; the CIR closed form against
    Monte Carlo; HJM with constant volatility gives the Ho-Lee drift $\sigma^2t$.
- **P7 Counterparty exposure and xVA** (new topic file
  `corporate-credit-capital/counterparty-xva.tex`).
  - Candidates: `def:counterparty-exposure-measures`, `meth:credit-valuation-adjustment`,
    `def:wrong-way-risk`, with DVA/FVA/MVA/KVA in outline inside the CVA entry or a separate
    entry if reading shows a distinct idea. The capital rules go to P10.
  - Formulation stated in the entry: unilateral CVA from the bank's view (own default
    ignored); exposure $E(t)=\max(V(t),0)$ of the netting set's mark-to-market,
    uncollateralised first, then with a margin period of risk; risk-neutral measure with the
    bank-account numéraire. In general
    $\mathrm{CVA}=(1-R)\,E^Q\!\big[D(0,\tau)E(\tau)\mathbf 1_{\{\tau\le T\}}\big]$. With
    exposure independent of default and a constant $R$, this becomes
    $(1-R)\sum_i\mathrm{EE}^*(t_i)\,[\mathrm{PD}(t_{i-1},t_i)]$, where
    $\mathrm{EE}^*(t)=E^Q[D(0,t)E(t)]$, which equals $P(0,t)\,\mathrm{EE}(t)$ under
    deterministic rates. Wrong-way risk breaks the independence, so the joint expectation
    $E^Q[D(0,t_i)E(t_i)\mathbf 1_{\{t_{i-1}<\tau\le t_i\}}]$ is needed.
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
- **P8 Default correlation** (new topic file `securitised-structured-credit/default-correlation.tex`).
  - Candidates: `mod:gaussian-copula-default-correlation` and
    `meth:tranche-loss-base-correlation`; it links to the existing WCDR formula in
    `meth:credit-liquidity-tail-risk` rather than restating it.
  - Sources: Hull OFOD chap. 25, RMFI chap. 9, and the Basel IRB formula (CRE31, current text
    read).
  - Checks (synthetic): large-pool tranche expected loss by quadrature against finite-pool
    simulation; IRB capital at sample PD and correlation.
- **P9 Extreme value theory** (`portfolio-construction-risk/risk-models.tex` after
  `meth:var-es-estimation-methods`, whose Pitfalls sentence is then updated).
  - Candidate `meth:extreme-value-tail-estimation` (block maxima and peaks over threshold;
    GPD; Hill; threshold choice; VaR and ES; the McNeil-Frey two-step on GARCH residuals).
  - Source: RMFI chap. 12; `s7-qrm`, `w2-mcneil-frey` and `wide-embrechts-extremal` only if
    obtained and read.
  - Data (known truth, synthetic):
    - i.i.d. Student $t$ with 4 degrees of freedom (tail index $\xi=0.25$, VaR and ES in
      closed form), $n=5{,}000$. Acceptance: the GPD and Hill estimates' 95% bootstrap
      intervals cover 0.25, and the 99.5% VaR is within 10% of the truth.
    - The GARCH(1,1)-$t$ generator already used for `meth:var-es-estimation-methods`, for the
      two-step method.
  - The annual Damodaran file (98 observations, 1928-2025) is not suitable and is not used.
    No empirical claim is made unless a daily series with stated source, dates and licence is
    added (backlog B9).

Batch L2 is estimated at about 8-9 objectives. P10 may join it if C0 adds few items.

## 8. Backlog (needs evidence before it is scheduled)

| ID | Item | What is needed first |
| --- | --- | --- |
| B1 | Kolmogorov forward and backward equations, transition densities | Decide whether it adds teaching beyond P1; Wilmott chap. 10 |
| B2 | Lookback options | Hull sec. 26.11, Wilmott chap. 26; low priority |
| B3 | Monte Carlo Greeks (pathwise, likelihood ratio) | Hull sec. 21.7 and Glasserman (not held); could be one entry |
| B4 | Second-order Greeks beyond the P4 sentence (vanna/volga hedging, the vanna-volga method) | A source for market practice |
| B5 | Discrete-hedging error distribution and transaction costs (Wilmott chaps. 47-48) | Overlap check with P4 and `mod:black-scholes-merton` |
| B6 | CAIA depth: CTA industry structure and vehicles (chaps. 29, 32), payoff-distribution and bottom-up replication (chap. 33), convertible arbitrage risks (chap. 34) | Owner decision on a CAIA citation exception, or non-curriculum sources (Kat and Palaro; Hasanhodzic and Lo) located and read. No own empirical CTA performance. A trend illustration is synthetic; an empirical futures backtest needs a defined continuous-contract roll rule, collateral return, a signal lag of $t-1$ information, and costs |
| B7 | Regulatory currency P10: FRTB status by jurisdiction (BCBS, EU CRR3, UK PRA, US); SA-CCR and the revised CVA framework (CRE52, MAR50); ISSB IFRS S1/S2 adoption, TCFD's transfer to the ISSB, SEC climate-rule status; LCR/NSFR dates in `financial-institution-analysis.tex` | The issuers' current texts read with retrieval dates; corrections to existing entries plus at most one `rule:` entry for counterparty capital |
| B8 | LIBOR-era CQF and Gregory material | Historical only; used solely as dated context in P6-P7 |
| B9 | Empirical EVT illustration | A daily return series with a documented source, dates and licence |
| B10 | "Monte Carlo Methods.pdf" | Identify author and edition (OCR or bibliographic match) only if B3 needs it |
| B11 | C0 findings | Added here by C0 |

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

## 11. Sequence

1. Owner decides E1 and E2.
2. Batch L1: P1, P2, P3, P4, P5, each with focused checks and records before the next.
3. Batch L1 integration checks and completion report; commit and PR only when the owner asks.
4. C0 (bounded) adds its findings to Section 8 and proposes the Batch L2 scope.
5. Owner freezes Batch L2. P10 (B7) goes in Batch L2 or L3 according to C0's size.

## 12. Risks and limits

- Wilmott 2006, Gregory 2015, the CQF 2016 packs and CAIA 2012 predate the LIBOR transition,
  the post-2017 Basel reforms and the ISSB. Their concepts are durable; their market and
  regulatory statements are used only as dated history.
- Several catalogue texts are not held locally; entries do not cite what was not read.
- The planning-run numbers in Section 6 come from small exploratory calculations outside the
  repository. The package scripts recompute them; the acceptance ranges, not the planning
  values, are binding.
- Editorial coverage is not study. Human review of all new entries is still outstanding.
