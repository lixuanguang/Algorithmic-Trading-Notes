# Compendium migration: slice records

The full record of each migration step, from the baseline to the latest slice, in order: scope, sources and their availability, source findings, checks and their limits, dispositions of every legacy block, counts, build and items for review. Records are left as written; corrections are appended as follow-ups. The conventions, current status, slice index and file map are in [migration.md](migration.md). Open questions arising from a slice are also logged in [log.md](log.md).

## Baseline: 14 October 2026, before Phase 0 (commit `9634e2b`)

- **Blocks:** 879 in the old environments, of which 12 were in the tooling appendix and 867 in the finance chapters: `taxonomy` 178, `remark` 146, `caveat` 113, `definition` 98, `mechanism` 81, `principle` 80, `model` 58, `method` 31, `proposition` 25, `process` 18, `marketrule` 18, `practitionernote` 14, `empiricalfinding` 11, `casestudy` 3, `notation` 2, `corollary` 2, `lemma` 1.
- **Labels:** five figure labels and one remark label (`rmk:propfracdifffeat`); no entry labels.
- **Figures:** the 21 PNG files in `execution-trading-costs/figures/` were referenced by no file.
- **Build** (`latexmk -g -pdf compendium.tex`, TeX Live, pdfTeX): exit 0; 143 pages; no LaTeX warnings, no undefined references or citations; 0 overfull and 30 underfull boxes; 7 pdfTeX warnings for duplicate destinations (`page.i` and six `figure.*` anchors).

## Phase 0: done 14 October 2026

1. Moved the seven chapters unchanged (`git mv`) to `compendium/legacy/<section-key>/`, rewrote their `\input` and figure paths, renamed their chapter labels to `legacy:<section-key>` and the one cross-chapter reference, and compiled them as *Notes awaiting migration*. The 21 unused execution figures moved with `legacy/execution-trading-costs/figures/`.
2. Moved the tooling appendix (calculator, reading AI papers, Python, VS Code), with its figures and its three sources (`downey-2015`, `ramalho-2015`, `speight-2021`), to `notes/tooling/`, which compiles on its own (`latexmk -pdf tooling.tex`). The VS Code and Python files stay commented out of it, as they were; they also compile when enabled.
3. Replaced the placeholder preface (*Lorem Ipsum* overview and roadmap) with a short description of the layout, keeping its acknowledgement of Narang, Velu and López de Prado.
4. Moved `hyperref` to the end of `compendium/preamble.tex`: loaded before `float` and `algorithm`, it gave every captioned figure a duplicate anchor. `house.tex` and the guide submodule are unchanged.
5. Added this file, the `% migrate-to:` lines in 71 legacy files, and `tools/migration_status.py` with its tests (`python3 -m unittest discover -s tools`).
6. Declared the pilot's notation overrides in `compendium/front/notation.tex`.

## Pilot: `market-making-lob` format pilot, 14 October 2026

A test of the entry format on the formal models named in the plan, not a migration of the pathway. Grossman–Miller and Kyle are supplemental to `market-making-lob`; its required readings (Glosten–Milgrom, Ho–Stoll, Guéant–Lehalle–Fernandez-Tapia, the queue and order-flow papers) are not covered, and the pathway is neither mastered nor consolidated.

### Source findings

- The legacy Grossman–Miller block, with its fee extension and liquidity measures, and the *Market Making using Limit Orders* block follow Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (`crypto-cartea`), chapter "A Primer on the Microstructure of Financial Markets", pp. 20–30, in notation and order. They cited `grossman-miller-1988` and `ho-stoll-1981`, neither of which was consulted.
- The limit-order block is **not** the Ho–Stoll model. The book sets it up as a static simplification in place of Ho and Stoll (1981), which it calls the usual first reference (p. 28). Its citation of `ho-stoll-1981` was therefore wrong for its formulas; the entry cites `crypto-cartea` and lists `ho-stoll-1981` only as further reading. `catalogue-0527`, the route's Ho–Stoll reading, is a topic lead that names no paper and was not substituted for one.
- The legacy Kyle equilibrium ($\beta=\sigma_u/\sigma_v$, $\lambda=\sigma_v/(2\sigma_u)$, profit $\sigma_v\sigma_u/2$, posterior variance $\sigma_v^2/2$) agrees with O'Hara, *Market Microstructure Theory* (`catalogue-0496`), chapter "Strategic Trader Models I: Informed Traders", pp. 91–98, eqs. (4.3)–(4.5), (4.17), (4.20). `crypto-cartea` p. 33 prints $\lambda=2\sigma_u/\sigma$, the reciprocal, which contradicts its own step $\beta=(2\lambda)^{-1}$; the entry records the conflict in its *Pitfalls*. The legacy block cited `s6-kyle`, which was not consulted.
- The legacy Avellaneda–Stoikov formulas agree with the author-hosted journal PDF of `s6-stoikov` (eqs. (8), (12), (29)–(30)), with one omission now stated: the spread formula is an approximation from an expansion in inventory with a linearised order-arrival term (sec. 3.2), not the exact solution.

### Checks and their limits

| Source | Copy used | Passages compared | Limits |
|---|---|---|---|
| `crypto-cartea` | Local scan, 2015 Cambridge printing, no text layer | pp. 20–33: every formula and statement the entries cite, read from page images, with OCR for the running text | Some signs on p. 26 are faint in the scan; the printed results agree with the clearing condition on the same page |
| `catalogue-0496` | Local scan, 1998 Wiley printing of the 1995 book | pp. 91–98, eqs. (4.1), (4.3)–(4.5), (4.16)–(4.17), (4.20), from page images and OCR | A later printing than the catalogue's 1995 record; page numbers may differ in other printings |
| `s6-stoikov` | Author-hosted journal PDF, the copy named in the catalogue's version record | pp. 217–222, eqs. (1)–(30), Table 1, text layer | The HJB and expansion steps were read, not re-derived |
| `grossman-miller-1988`, `ho-stoll-1981`, `s6-kyle` | Not available locally | None | Cited only as further reading, marked not yet read |

Every pilot entry is therefore *partly checked*, *draft* and, except Avellaneda–Stoikov, *timeless*. **Human review is outstanding** for all six entries: their wording, the interpretations they flag, and the locators, before any is marked *checked*.

### Dispositions of the pilot blocks

| Legacy block (file, before migration) | Disposition |
|---|---|
| *Grossman-Miller Model* (`05_.../01_economics_of_market_making.tex`), main equilibrium | Rewritten as `mod:grossman-miller`; figure kept as `fig:grossman_miller_trading` |
| same block, *Trading Costs* part | Rewritten as `res:grossman-miller-trading-fees` |
| same block, *Measuring Liquidity* part | Rewritten as `res:grossman-miller-liquidity-measures` |
| same block, *Implications* items on free entry ("until spread capture just covers $c$") and market design (migration to search, block crossing or delayed execution) | Not supported by `crypto-cartea`; kept verbatim in the artefact and stubbed in the pathway backlog as needing `grossman-miller-1988` |
| *Kyle Model* (same file) | Rewritten as `mod:kyle-single-auction` |
| *Kyle Linear Price Impact* and *Kyle Linear Equilibrium* (`03_.../05_information_based_models.tex`), a second version of the same model in other notation | Merged into `mod:kyle-single-auction` (same equilibrium; its notation, $p_\infty$, $n_\omega$, $\tilde P$, is kept in the artefact) |
| *Market Making using Limit Orders* (same file as Grossman–Miller) | Rewritten as `mod:static-limit-order-depth`; figure kept as `fig:limit_order_market_making` |
| *Avellaneda-Stoikov Setup*, *Reservation Price*, *Symmetric Optimal Spread* (`05_.../02_avellaneda_stoikov_framework.tex`) | Merged into `mod:avellaneda-stoikov` |
| *Framework, Not Production Model* caveat (same file) | Merged into the *Pitfalls* of `mod:avellaneda-stoikov`, marked as interpretation |
| *Quote-Control Segmentation* taxonomy (same file) | Left in legacy, assigned to `market-making-lob`: a list without a claim to check, to be placed in a quoting entry at consolidation |
| *Inventory-Skew Quoting* model (`03_.../04_inventory_models.tex`) | Left in legacy, assigned to `market-making-lob`: Ho–Stoll-related, unsourced, needs the Ho–Stoll paper |
| *Adverse Selection Through Flow* principle (`03_.../05_information_based_models.tex`) | Left in legacy, shared: interpretation of the Kyle and Glosten–Milgrom mechanisms, to be placed when Glosten–Milgrom is migrated |

All removed blocks are kept verbatim, with only figure paths changed, in `notes/artefacts/market-making-lob/derivations.tex`, which compiles on its own. Each deletion site in the legacy files carries a `% migrated:` comment naming its destination.

### Source blockers

As at the pilot; rechecked in slice 2 below, which unblocked Grossman–Miller through its NBER working paper and the `crypto-cartea` p. 33 misprint through the authors' errata. Slice 3 migrated *Inventory-Skew Quoting* from textbook accounts (Hasbrouck's version of Stoll (1978); O'Hara's report of Ho–Stoll); the Ho–Stoll paper itself is still needed, for the backlog stub `res:ho-stoll-dealer-pricing`.

| Needed | Why | Passage required |
|---|---|---|
| Ho and Stoll (1981), *Journal of Financial Economics* 9(1) (`ho-stoll-1981`); the route reads it through `catalogue-0527`, which names no paper | `market-making-lob` requires a Ho–Stoll inventory entry; the legacy *Inventory-Skew Quoting* block cannot be sourced without it | The section deriving the dealer's optimal bid and ask as functions of inventory, with the equation numbers |
| Grossman and Miller (1988), *Journal of Finance* 43(3) (`grossman-miller-1988`) | Two legacy implications are not in `crypto-cartea` | The participation-cost (entry) stage and the discussion of market structure for large orders |
| Kyle (1985), *Econometrica* 53(6) (`s6-kyle`) | To check the single-auction results at the original, and the misprint in `crypto-cartea` p. 33 | The single-auction equilibrium theorem and its proof |

### Build after the pilot

`latexmk -g -pdf compendium.tex`: exit 0; 139 pages (the tooling appendix left; six entries came in); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes; one pdfTeX duplicate-destination warning, `page.i`, inherited from `\maketitle` before the roman-numbered front matter. Rendered and inspected: the contents, notation and preface; the new chapter (pp. 1–5; pp. 2 and 4 at full size, with both figures); the part title page (p. 6); and the pruned legacy market-making section (p. 116).

## Slice 2: Glosten–Milgrom and the dealer material, 15 October 2026

Migration of the `market-making-lob` candidate blocks named as the next slice, run from the pilot's pushed state (`ce64308`, pushed straight to `main`, no pull request). It is migration and source checking, not study: the pathway is neither mastered nor consolidated, and its Methods readings are untouched.

### Scope

The 43 blocks left in `05_market_making_and_liquidity_provision/` (40) and `03_.../05_information_based_models.tex` (3), and the assigned *Inventory-Skew Quoting* block in `03_.../04_inventory_models.tex`. Each was either migrated or assigned to the one candidate pathway it belongs to; the seven cross-asset blocks fit neither listed candidate and are left shared (see *For review*).

### Source availability, rechecked 2026-10-15

| Source | Result | Used |
|---|---|---|
| `s6-glosten`, *JFE* 14(1), 1985 | Closed (Unpaywall: no open copy; ScienceDirect refused scripted access). Third-party reposts exist, of unclear authorisation; not used | No |
| Glosten and Milgrom, Northwestern CMS-EMS Discussion Paper 570, August 1983 (`glosten-milgrom-1983`) | The Kellogg-hosted scan has moved; retrieved from the Internet Archive's 2025-12-12 snapshot of that URL. 31 pages, scanned, no text layer | Yes, as its own key; its numbering may differ from the journal version |
| `ho-stoll-1981`, *JFE* 9(1), 1981 | Closed (Unpaywall; ScienceDirect refused); the 1979 Wharton working paper 27-79 is listed without a download. Still blocked. O'Hara's textbook account (`catalogue-0496`, ch. 2) was not substituted | No |
| `s6-kyle`, *Econometrica* 53(6), 1985 | Closed (Unpaywall; Econometric Society page requires login); only third-party reposts of a JSTOR copy, of unclear authorisation; not used | No |
| `grossman-miller-1988`, *JF* 43(3), 1988 | Journal version closed; NBER Working Paper 2641, July 1988 (`grossman-miller-1988-nber`) is open, with a text layer | Yes, for the two blocked passages |
| `crypto-cartea` errata | Authors' page; equations read from their LaTeX source in the page (`crypto-cartea-errata`) | Yes |
| `alpha-harris` | Local copy outside the repository (the 2002 Oxford printing, with a text layer; printed page = PDF page − 13) | Yes |

### Source findings

- **The legacy Glosten–Milgrom proposition is Harris's example, not the paper.** Its $a=V+PE$, $b=V-PE$, $a-b=2PE$, with the information and accounting views agreeing, is Harris, *Trading and Exchanges*, chap. "Bid/Ask Spreads", sec. 14.10, pp. 320–321, "a simple example based on the Glosten–Milgrom model". It is now `res:adverse-selection-spread-component`, citing `alpha-harris`. Harris misprints the dealer's profit against an informed buyer as $A-(V-E)$ (p. 321, checked on the page image); his result needs $A-(V+E)$.
- **The paper's model** (`mod:glosten-milgrom`) was checked in the 1983 discussion paper: zero-profit quotes $A_t=\mathbb{E}[V\mid S_t,Z_t>A_t]$ (p. 6), Proposition 1 ($A_t\ge\mathbb{E}_t[V]\ge B_t$, p. 8), Proposition 2 (martingale prices, p. 10), Proposition 3 (root-mean-square spread bound, p. 11), Proposition 5 (comparative statics, pp. 15–16), market shutdown (pp. 9, 12, 17) and the volume result (pp. 18–19). The closed-form two-value half-spreads are `crypto-cartea`'s simplification (pp. 34–36), kept as a separate result.
- **Two `crypto-cartea` misprints are confirmed by the authors' errata.** P. 33: Kyle's $\lambda$ should be $\sigma/(2\sigma_u)$, which settles the pilot's conflict at textbook level, in agreement with `catalogue-0496` (Kyle's paper still unread). P. 37: the bid half-spread prints $F(\Delta_a)$ for $F(\Delta_b)$.
- **Grossman–Miller (NBER 2641).** Free entry: market makers enter until $\mathbb{E}U(W_0-c+(\bar P_2-P_1)x_1^m)=\mathbb{E}U(W_0)$ (eq. (16), p. 18). With $\mathbb{E}i=0$ this gives $1/\sqrt{1+t}=e^{-ac}$ with $t=a^2\operatorname{Var}_1(\bar P_2)\operatorname{Var}(i)/(1+M)^2$ (eq. (19), pp. 18–19). The number of market makers is set by $ac$ and rises as $c$ or $a$ falls, or as either variance rises (p. 19). The legacy wording "until spread capture just covers $c$" is loose: entry balances the expected utility of the risky position, not spread capture. Large orders: a specialist can switch to "search mode" when an order exceeds what the specialist and the limit-order book can absorb, and upstairs block desks served mainly as a search market (p. 9). Both are now backlog stubs, not entries.
- **Harris supports the remaining dealer blocks** almost line for line (chap. "Dealers", pp. 283–294; chap. "Bid/Ask Spreads", pp. 297–302, 312–313). One legacy claim was not found: that poorly informed dealers *underreact* to informed flow. Harris says only that they more often mistake uninformed clients for informed ones (p. 293). It was dropped from the entry and kept in the artefact.

### Checks and their limits

| Source | Copy used | Passages compared | Limits |
|---|---|---|---|
| `glosten-milgrom-1983` | Internet Archive snapshot of the Kellogg-hosted scan | pp. 1–25: setup, Propositions 1–5 and their proofs' structure, shutdown, volume and the conclusion's limitations; page images for every formula, OCR for running text | Working paper, not the 1985 journal version the catalogue names; proofs read, not re-derived |
| `crypto-cartea` | Local scan (as in the pilot) | pp. 34–37, Figure 2.3, n. 5, from page images (p. 37 at 300 dpi) | — |
| `crypto-cartea-errata` | Authors' web page, retrieved 2026-10-15 | Entries for pp. 33, 36 and 37 | Undated page |
| `alpha-harris` | Local PDF with text layer | chap. "Dealers", pp. 283–295; chap. "Bid/Ask Spreads", pp. 297–302, 312–313, 320–321; p. 321 also as a page image | Text layer, not page images, except p. 321 |
| `grossman-miller-1988-nber` | NBER PDF | pp. 4–5, 9, 18–19, 23–24; eqs. (16)–(19) from page images | Working paper, not the journal version |

The six new entries are all *partly checked 2026-10-15*, *draft* and *timeless*; **human review is outstanding** for them, as for the six pilot entries.

### Dispositions

| Legacy block (file, before migration) | Disposition |
|---|---|
| *Glosten-Milgrom Adverse-Selection Spread Component* proposition, *Information and Accounting Views Agree* (`03_.../05_information_based_models.tex`) | Rewritten as `res:adverse-selection-spread-component`, cited to `alpha-harris` rather than to Glosten and Milgrom |
| *Adverse Selection Through Flow* (same file) | Merged into the *Practice* of `mod:glosten-milgrom` |
| *Adverse Selection Risk*, *Information Creates Inventory Imbalance* (`05_.../03_adverse_selection_and_toxic_flow.tex`) | Merged into `def:dealer-inventory-risk` |
| *Adverse Selection Spread Component* principle (same file) | Merged into the *Practice* of `res:adverse-selection-spread-component` |
| Two tables, *Informed-Trader Identification*, *Refusing Flow* (same file) | Merged into `meth:dealer-quote-adjustment` (steps 2 and 3, *Conditions*, *Practice*; "reduces market-wide immediacy" kept as interpretation) |
| *Inventory Imbalance*, its tactics table, *Inventory Control Is Price Discovery* (`05_.../04_optimal_quoting_and_inventory_control.tex`) | Merged into `def:dealer-inventory-risk` and `meth:dealer-quote-adjustment` |
| *Dealer Inventory Risk Segmentation*, *Dealer Valuation Priority* (`05_.../07_risk_management_for_market_makers.tex`) | Merged into `def:dealer-inventory-risk` |
| *Poorly Informed Dealers*, *Dealers and Value Traders* (same file) | Merged into the *Practice* of `meth:dealer-quote-adjustment`; "underreact to informed flow" not supported and dropped |
| *Quote-Control Segmentation* (`05_.../02_avellaneda_stoikov_framework.tex`) | Merged into the *Statement* of `meth:dealer-quote-adjustment` (level, skew, spread, size) |
| *Two-Sided Flow* (`05_.../01_economics_of_market_making.tex`) | Merged into `meth:dealer-quote-adjustment` (the "risk warehousing" phrase as interpretation) |
| *Free Entry Bounds Dealer Spreads*, *Dealer Spread Cost Segmentation* (same file) | Merged into the *Conditions* of `res:adverse-selection-spread-component` |
| The other 9 blocks of `05_.../01_...` (dealer definition, dealer-problem, DMM, specialist-privilege, quote, outside-spread and order-flow lists, preferencing caveat, trading-with-dealers note) | Assigned to `execution-market-making`: institutional material for the section overview, left in legacy |
| *Specialist Participation Option*, *Tick Size and Participation* (`05_.../04_...`) | Assigned to `execution-market-making`, left in legacy |
| All 7 blocks of `05_.../05_latency_and_queue_competition.tex` | Assigned to `hft-market-design`, left in legacy |
| All 7 blocks of `05_.../06_cross_asset_and_cross_venue_market_making.tex` | Left shared and unassigned: arbitrage as cross-instrument dealing (Harris, chap. "Arbitrageurs"), which fits neither `market-making-lob` nor `hft-market-design` |
| *Inventory-Skew Quoting* (`03_.../04_inventory_models.tex`) | Unchanged, assigned to `market-making-lob`: still blocked on `ho-stoll-1981` |

New entries from the textbook and working-paper passages: `mod:glosten-milgrom`, `res:glosten-milgrom-half-spreads` and `res:glosten-milgrom-market-collapse` (the two backlog stubs written up). `mod:kyle-single-auction` gained the errata correction in its *Pitfalls* and *Status*.

Four legacy files emptied and were deleted, with their `\input` lines and map rows: `03_.../05_information_based_models.tex`, `05_.../02_avellaneda_stoikov_framework.tex`, `05_.../03_adverse_selection_and_toxic_flow.tex` and `05_.../07_risk_management_for_market_makers.tex`. Their `% migrated:` comments are recorded above. Every removed block and table is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Glosten–Milgrom and dealer quoting (slice 2)*.

### Counts

`migration_status.py`: 858 → 840 legacy blocks (18 migrated: 3 + 1 + 5 + 4 + 3 + 2). Assigned 2 → 19 (+11 `execution-market-making`, +7 `hft-market-design`, −1 for *Quote-Control Segmentation*, migrated); one candidate only 144 → 135 (the 9 blocks of the two deleted single-candidate files); shared 712 → 686 (−3 migrated from `03_.../05`, −5 migrated and −18 assigned from `05_.../01`, `04`, `05`). Entries 6 → 12. No block is counted twice: an assigned block counts only towards its pathway.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 142 pages (139 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy part; the one pre-existing `page.i` duplicate-destination warning. A first build had one new overfull box (an artefact path in *Further reading*) and one new underfull box (in the Glosten–Milgrom entry's *Pitfalls*); both were reworded away. Rendered and inspected: the notation overrides (p. iv), the new sections (pp. 5–10) and the pruned legacy market-making section (p. 119). The artefact `derivations.tex` compiles on its own: 10 pages, no warnings, the same 3 underfull boxes as before. The tooling appendix was not affected and was not rebuilt.

### For review

- All six new entries: wording, the interpretations they flag, and the locators. In particular, check whether citing Harris rather than Glosten and Milgrom for the $2\alpha e$ result is the attribution you want.
- Whether the working-paper keys (`glosten-milgrom-1983`, `grossman-miller-1988-nber`) should stay as separate sources or be replaced by the journal versions once those are read.
- The cross-asset arbitrage file (`05_.../06`): its candidate list (`market-making-lob`, `hft-market-design`) looks wrong; `execution-market-making` (Harris, chap. "Arbitrageurs") or the asset-class pathways seem closer. The list was left unchanged.
- The 9 + 2 blocks assigned to `execution-market-making` and the 7 assigned to `hft-market-design`: the assignments are provisional and can be changed with their `% assign:` lines.

## Slice 3: spread decomposition and inventory models, 15 October 2026

Migration of the two files named as the next bounded slice, run from slice 2's pushed state (`07a0504`, on `main`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Scope

All 21 blocks of `03_.../03_bid_ask_spread_decomposition.tex` (17) and `03_.../04_inventory_models.tex` (4), shared between `execution-market-making` and `market-making-lob`, one of them (*Inventory-Skew Quoting*) assigned to `market-making-lob`. Every block was merged into an existing entry or into one of six new ones; both files emptied and were deleted.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF outside the repository, as in slice 2 (2002 Oxford printing; printed page = PDF page − 13) | As in slice 2 |
| `s6-hasbrouck` | Local PDF outside the repository: *Empirical Market Microstructure: The Institutions, Economics, and Econometrics of Securities Trading*, Oxford University Press, 2007, ISBN 978-0-19-530164-9, matching the catalogue; text layer; printed page = PDF page − 11. A second local file with Hasbrouck's name is his 2004 lecture-notes draft (PDF title "Microstructure Notes 02 Intro.nb"), not the book: not used | Title page and copyright page read |
| `catalogue-0496` (O'Hara) | Local scan, 1998 Wiley printing, no text layer; printed page = PDF page − 9 | As in the pilot |
| `ho-stoll-1981` | Still no accessible copy: a web search found only citations and the RePEc listing of the 1979 working paper, no full text; no library access is available to this session | Not used |

### Source findings

- **The three overlaps.** *Spread Component Segmentation*, *Simple Dealer Quote Decomposition* and *Adverse-Selection Component Equivalence* were merged into `res:adverse-selection-spread-component`, now titled *Spread components: the adverse-selection component, its two views, and the total spread* (label kept).
  - The quote decomposition $a=V^B+C/2$, $b=V^S-C/2$, $a-b=A+C$ is Harris's Figure 14-1 (p. 301, checked on the page image). It now opens the entry's Statement, with Figure 14-2's revision after a buy (pp. 301–302).
  - The three-way component list (order processing, inventory, adverse selection) is not Harris's: he uses two components, the inventory-risk premium sitting inside the transaction-cost component (pp. 298–299). Hasbrouck notes that spreads impound noninformational costs and inventory effects as well (sec. 5.5, p. 53). Kept as a qualified Condition.
  - The equivalence proposition's claim that $A$ is "twice the dealer's mark-to-market loss … against a correctly signed informed trade" is wrong except when every trader is informed. In Harris's example the loss on an informed trade is the pricing error $e$; $A/2=\alpha e$ is the expected revision given a trade on that side (pp. 300–302, 320). Recorded as a Pitfall, with the corrected reading labelled as own derivation. Its assumption $V_0=(V^B+V^S)/2$ is Harris's symmetry condition (p. 301).
- **Roll's estimator.** The legacy derivation matches Harris's box line for line (p. 415, page image) and Hasbrouck's half-spread version (sec. 3.4, pp. 29–30). The legacy caveat had one direction wrong: trade signs correlated with information make the autocovariance *more* negative and bias the estimate up (Hasbrouck, Exercise 4.3, pp. 38–39), while autocorrelated signs bias it down (Exercise 4.2). Harris says violations typically bias it down (p. 434). Price discreteness and hidden liquidity, also listed, are not in the passages checked.
- **Effective and realised spreads.** Harris defines both as doubled signed differences from the time-of-trade and a later midpoint (pp. 424–425), and uses "realised spread" also for a dealer's round-trip outcome (p. 280); Hasbrouck's effective and realised *costs* are per side, for a buy (p. 148). The entry keeps the conventions apart and states the factor of two.
- **Inventory models.** *Inventory-Skew Quoting* ($r=m-\kappa(q-q^\star)$, constant spread) is exactly Hasbrouck's version of Stoll (1978) with the ask derived by the same indifference argument: $\kappa=s=\gamma\sigma_X^2$ (sec. 11.2, pp. 110–111; the ask is own derivation). O'Hara reports that Ho–Stoll also gives a spread independent of inventory, with both quotes shifted (sec. 2.3, pp. 35–36, page images). Hasbrouck's account of Amihud–Mendelson, where the spread widens away from the preferred position (pp. 108–109), shows the constant spread is not general. Written as `mod:inventory-based-quotes`, citing the textbooks and stating that neither original paper was consulted.
- **Inventory versus information.** The legacy caveat is supported by Hasbrouck sec. 11.4 (p. 115): the same short-run quote response, separated by permanence; NYSE specialist inventories add little to quote dynamics.
- **Spread determinants and outside spreads.** Harris chap. 14, secs. 14.4–14.6 (pp. 304–317, Table 14-2 p. 311) and chap. 16 (pp. 340–346) support the lists almost item by item. One legacy phrase, "availability of close risk substitutes", is not Harris's; his factor is risk replication for hedgers (p. 316).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. "Dealers" p. 280; chap. "Bid/Ask Spreads" pp. 297–318 (Figure 14-1 p. 301 also as page image); chap. "Value Traders" pp. 340–346; chap. "Volatility" pp. 413–417 (Roll box p. 415 also as page image); chap. "Liquidity and Transaction Cost Measurement" pp. 423–427, 434 | Text layer except the two page images; Table 14-2 read from the text layer |
| `s6-hasbrouck` | secs. 3.4 (pp. 29–30), 4.4–4.5 (pp. 38–39), 5.4.2 (p. 49), 5.5 (p. 53), 8.1–8.3 (pp. 67–69), chap. 11 (pp. 106–117), 14.2.2 (p. 148), 14.3.3 (pp. 150–151) | Text layer only; its equations extracted cleanly apart from lost $\Delta$ signs, restored from context |
| `catalogue-0496` | sec. 2.3, pp. 29–36 | Page images; a textbook account of Ho–Stoll, not the paper |

The six new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding** for them and for the three revised entries.

### Dispositions

| Legacy block (`03_.../03_bid_ask_spread_decomposition.tex` unless stated) | Disposition |
|---|---|
| *Spread Notation*, *Spread Measurement Segmentation* (outside-spread item excepted), *Quoted vs Realised Spread*, *Effective Spread Decomposition* | Rewritten as `def:spread-measures` |
| *Outside Spread*, *Outside Spread Determinant Segmentation*, and the outside-spread item above | Rewritten as `def:outside-spread` |
| *Spread Component Segmentation* | Merged into the Conditions of `res:adverse-selection-spread-component` (qualified: Harris's split is two-way) |
| *Simple Dealer Quote Decomposition* | Merged into the Statement of `res:adverse-selection-spread-component` |
| *Adverse-Selection Component Equivalence* | Merged into `res:adverse-selection-spread-component`: symmetry condition in Conditions; the "twice the loss" claim corrected in Pitfalls |
| *Uninformed Trading Loss Channels* | Merged into the Practice of `res:adverse-selection-spread-component` |
| *Component Identification* | Rewritten as `res:spread-component-identification` |
| *Roll Serial-Covariance Spread Estimator*, *Roll Estimator Limits* | Rewritten as `res:roll-spread-estimator`; the informed-trading direction corrected |
| *Primary Spread Determinants*, *Order-Driven Spread Determinant Segmentation*, *Secondary Spread Proxy Segmentation*, *Liquidity and Capital Structure* | Rewritten as `res:spread-determinants` |
| *Inventory Spread Component*, *Inventory Cost Segmentation* (`04_inventory_models.tex`) | Merged into `def:dealer-inventory-risk` (Practice; Conditions, with unsupported items named) |
| *Inventory-Skew Quoting* (`04_...`, assigned to `market-making-lob`) | Rewritten as `mod:inventory-based-quotes` from textbook accounts; Ho–Stoll paper check left as backlog stub `res:ho-stoll-dealer-pricing` |
| *Inventory vs Information Identification* (`04_...`) | Merged into the Practice of `res:spread-component-identification` and the Pitfalls of `mod:inventory-based-quotes` |

`meth:dealer-quote-adjustment` gained cross-references only. Both legacy files were deleted with their `\input` lines and map rows; their full text, with the `% migrated:` destinations above, is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Spread decomposition and inventory models (slice 3)*. A script confirmed every line of both files is there, in order.

### Counts

`migration_status.py`: 840 → 819 legacy blocks (21 migrated: 17 + 4). Assigned 19 → 18 (*Inventory-Skew Quoting*, migrated); one candidate only 135 → 135; shared 686 → 666 (the other 20). Entries 12 → 18 (definitions 1 → 3, models 5 → 6, results 5 → 8, methods 1). `market-making-lob`: 0 assigned, 166 shared, 18 entries, 5 stubs. No block is counted twice. One notation override row added (`front/notation.tex`: $A$, $C$, $Q_t$, $q_t$).

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 145 pages (142 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one pre-existing `page.i` duplicate-destination warning. Rendered and inspected: notation overrides (p. iv), the revised and new entries (PDF pp. 14–22, chapter pp. 8–16) and the pruned legacy section (PDF p. 112). The artefact compiles on its own: 12 pages (10 before), no warnings, the same 3 underfull boxes. The tooling appendix was not affected and was not rebuilt.

### For review

- The six new entries and the three revised ones; in particular the corrected reading of the equivalence proposition, the Roll bias directions, and whether `mod:inventory-based-quotes` should be split into a Stoll entry and a Ho–Stoll entry once the paper is read.
- The five measurement entries (`def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `res:spread-determinants`, `def:outside-spread`) serve the section overview route `execution-market-making`, whose required readings include `s6-hasbrouck`; they are listed in the `market-making-lob` note because that route has no pathway note yet.
- The new notation override row, and the per-side versus full-spread conventions it records.

## Slice 4: volatility and liquidity, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 3's pushed state (`79aa634`, on `main`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Scope

The 22 blocks of `03_.../08_volatility_and_liquidity_interaction.tex`, shared between `execution-market-making` and `market-making-lob`. Fourteen were migrated. The other eight (liquidity spiral, Flash Crash case and toy model, hot-potato amplification, flash-crash controls, systemic-risk link, shock propagation, trade count as HFT proxy) were assigned to `hft-market-design`, whose required readings include the Flash Crash paper (`w5-kirilenko-flash-crash`) and whose optional branch includes `w5-menkveld-yueshen-flash`; they stay in legacy. To allow the assignment, `hft-market-design` was added to the file's `% migrate-to:` line and its map row. The file is therefore not deleted.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF, as in slices 2–3 | As before |
| `s6-hasbrouck` | Local PDF, as in slice 3 | As before |
| `alpha-laruelle` | Local PDF outside the repository: Lehalle and Laruelle (eds.), *Market Microstructure in Practice*, 2nd ed., World Scientific, 2018, ISBN 9789813231122, matching the catalogue record (DOI 10.1142/10739); text layer; printed page = PDF page − 27 | Copyright page read |
| `garman-klass-1980` | Not consulted; added to `front/sources.tex` from its Crossref record (DOI 10.1086/296072) as further reading | Crossref metadata only |

### Source findings

- **The three spread–volatility blocks are Lehalle and Laruelle, not Harris.** The level and log-log regressions, the back-transformation $\psi=A_0\sigma^{a_1}e^\epsilon$ and the predictor $\hat A_0\sigma^{\hat a_1}e^{\hat\sigma_\epsilon^2/2}$ are their appendix A.10 (pp. 292–298, Rio Tinto, 15-minute intervals); the fits are weak ($R^2$ 0.24 in levels, 0.16 in logs, 0.11 for the back-transformed predictor). The identification caveat's controls are supported for tick size (p. 148: at a one-tick spread, size at the best quotes adjusts instead), time of day (pp. 145–148) and trade intensity (pp. 144–145, $\psi_i=a+b\sigma_i/\sqrt{N_i}$); venue and depth as regression controls are not in the passages checked. Their "unbiased predictor" is exact only with known parameters (own note).
- **Overlap with `res:spread-determinants`.** The regressions became a method entry, `meth:spread-volatility-regression`, since they estimate a determinant rather than state one; the determinants entry gained Lehalle and Laruelle's empirical relation and a cross-reference. The principle *Volatility Is a Liquidity Price* was merged into it: wider spreads and, in crashes, withdrawal are supported (Harris pp. 561, 563); smaller displayed size and faster cancellations as responses to volatility are not, and are named in its Pitfalls.
- **Garman–Klass.** Lehalle and Laruelle print $\sqrt{\tfrac12(\text{high}-\text{low})^2-(2\log2-1)(\text{close}-\text{open})^2}$ divided by the average price (p. 172, page image; the text layer drops the $\tfrac12$); the legacy block used log ratios. The two agree to first order. The 1980 paper was not consulted.
- **Overlap with `res:roll-spread-estimator`.** *Volatility Component Decomposition* ($P_t=M_t+u_t$) is Hasbrouck's random-walk decomposition (sec. 8.6, pp. 72–74): only the random-walk variance is identified, the pricing-error variance has only a lower bound. *Transitory Volatility and Reversal* and *Volatility Source Segmentation* are Harris chap. 20 (pp. 410–416). These went into a new definition, `def:volatility-components`, with Roll's model as its special case; the Roll entry gained a cross-reference only. Negative serial covariance is a strong indicator (Harris p. 414) but neither necessary nor sufficient: perishable spot prices (box p. 413) and lagged adjustment (Hasbrouck Exercise 8.2, p. 74). The legacy sources *episodic* and *continuing* volatility: Harris's episodic volatility (p. 410) describes episodes, not a source; continuing volatility was not found.
- **Bubbles and crashes** follow Harris chap. 28 almost item by item (pp. 555–563, 570–571): the five-phase dynamics, the price accelerator box (p. 556, after Treynor's unpublished manuscript, not consulted) and the "market failures or corrections" box (p. 559). *Regulating Volatility* is Harris pp. 410 and 575–577 (circuit breakers' net effect on transitory volatility indeterminate).
- **Flash-crash blocks (assigned, not migrated).** All eight follow Lehalle and Laruelle chap. 2, sec. 2.5 (pp. 169–183) and app. A.5 (pp. 261–266, page images). Two findings for when they are migrated: (1) the legacy *Hot-Potato Amplification* calls $\rho$ the fraction of traders following volume; in the book $\rho$ is the proportion of traders playing the hot-potato game, while the large seller follows volume (p. 264); (2) the book's solution (A.14), $I_t^-=I_0\exp\bigl(\tfrac{t^2}{1-\rho}\tfrac{r_0}{2}-\tfrac12\sigma_I^2t+\sigma_IW_t^-\bigr)$, does not follow from its own approximation $R_t\simeq tr_0/(1-\rho)$, which gives an exponent linear in $t$ (own derivation, to be rechecked). Sec. 2.5.3 (pp. 187–189), on circuit breakers, was not read.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. 20 "Volatility", pp. 410–417; chap. 28 "Bubbles, Crashes, and Circuit Breakers", pp. 555–563, 570–578 | Text layer only |
| `s6-hasbrouck` | secs. 8.3 (p. 69), 8.4–8.7 (pp. 69–75) | Text layer; $\Delta$ signs restored from context |
| `alpha-laruelle` | chap. 2, secs. 2.2 (pp. 143–148), 2.3.1 (pp. 150–151), 2.5–2.5.2 (pp. 169–184); app. A.5 (pp. 261–266), A.10 (pp. 292–298) | Text layer; page images for p. 172 and pp. 262–266 |

The four new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding** for them and for the two revised ones.

### Dispositions

| Legacy block (`03_.../08_volatility_and_liquidity_interaction.tex`) | Disposition |
|---|---|
| *Volatility Is a Liquidity Price* | Merged into `res:spread-determinants` (Practice; unsupported responses named in Pitfalls) |
| *Volatility Source Segmentation*, *Fundamental Volatility Driver Segmentation*, *Transitory Volatility and Reversal*, *Volatility Component Decomposition* | Rewritten as `def:volatility-components` |
| *Regulating Volatility* | Merged into the Practice of `def:volatility-components` |
| *Bubbles and Crashes*, *Bubble-Crash Dynamics Segmentation*, *Price Accelerator* | Rewritten as `mech:bubble-crash-dynamics` |
| *Crash Attribution* | Merged into the Pitfalls of `mech:bubble-crash-dynamics` |
| *Garman-Klass Intraday Volatility* | Rewritten as `meth:garman-klass-volatility` |
| *Spread-Volatility Regression*, *Log-Log Spread-Volatility Model* | Rewritten as `meth:spread-volatility-regression` |
| *Spread-Volatility Identification* | Merged into the Pitfalls of `meth:spread-volatility-regression` |
| *Liquidity Spiral*, *Flash Crash Mechanism*, *Depth-Driven Flash Crash Toy Model*, *Hot-Potato Amplification*, *Flash-Crash Control Segmentation*, *Systemic Risk Link*, *Shock Propagation Channels*, *Trade Count as HFT Proxy* | Assigned to `hft-market-design`, left in legacy |

`res:roll-spread-estimator` gained a cross-reference only. The 14 migrated blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Volatility, liquidity and crashes (slice 4)*; a script confirmed they are there, contiguous and in order, and that the 8 blocks left in the legacy file are unchanged.

### Counts

`migration_status.py`: 819 → 805 legacy blocks (14 migrated). Assigned 18 → 26 (+8 `hft-market-design`, now 15); one candidate only 135 → 135; shared 666 → 644 (−14 migrated, −8 assigned). Entries 18 → 22 (definitions 3 → 4, methods 1 → 3, mechanisms 0 → 1). `market-making-lob`: 0 assigned, 144 shared, 22 entries listed, 5 stubs. No block is counted twice. No notation override was added: $A_0$ and the $p^O,p^H,p^L,p^C$ superscripts are explained in the entries' Notation fields.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 148 pages (145 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had three new underfull boxes in the new entries; they were reworded away. Rendered and inspected: the new section (PDF pp. 22–26) and the pruned legacy section (PDF p. 121). The artefact compiles on its own: 13 pages (12 before), no warnings, the same 3 underfull boxes. The tooling appendix was not affected and was not rebuilt.

### For review

- The four new entries and the two revised ones; in particular the decision to make the regressions a method entry rather than part of `res:spread-determinants`, and the own-derivation notes (the predictor's unbiasedness, the variance split's covariance term).
- The assignment of the eight flash-crash and systemic blocks to `hft-market-design`. *Systemic Risk Link* and *Shock Propagation Channels* concern fragmentation and could instead go to `market-structure-execution-quality`; *Liquidity Spiral* is general enough for `execution-market-making`.
- The (A.14) exponent in Lehalle and Laruelle's toy model, before that block is migrated.
- As in slice 3, the new entries serve the overview route `execution-market-making` and are listed in the `market-making-lob` note only because that route has no note.

## Slice 5: information, market efficiency and price discovery, 15 October 2026

Migration of the two files named as the next bounded slice, run from slice 4's pushed state (`326ad36`, on `main`, matching `origin/main`; guide submodule at `343d145`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied. The slice-4 overlap list was judged from titles; each candidate overlap below was settled by comparing definitions and claims.

### Scope

The 21 blocks of `03_.../01_information_and_market_efficiency.tex` (9) and `03_.../02_price_discovery.tex` (12), both shared between `execution-market-making` and `market-making-lob`. Eighteen were migrated, into six new entries and one revised entry. Three were assigned elsewhere and stay in legacy. The first file is empty and was deleted, with its `\input` line in `03_.../00_overview.tex`.

### Routing decisions

- **Overview route note.** The guide runs one study loop per section overview, and an overview route's key doubles as its section key (guide, *Keys, layers and registers* and *The study loop*). So `notes/pathways/execution-market-making.md` was created for the existing route `execution-market-making`. The nine slice-3 and slice-4 entries listed provisionally in `market-making-lob.md` (`def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `res:spread-determinants`, `def:outside-spread`, `def:volatility-components`, `meth:garman-klass-volatility`, `meth:spread-volatility-regression`, `mech:bubble-crash-dynamics`) moved there with the six new ones. The dealer entries stay with `market-making-lob`, whose second reading is on dealer inventory. Entry labels, files and the derivations artefact path are unchanged.
- **Taxonomy used.** `market-structure-execution-quality`: "how fragmentation, dark trading, fees, tick size, odd lots, retail routing and trading hours affect execution quality", with O'Hara and Ye on fragmentation. `hft-market-design`: "how speed, latency races and fast arbitrage affect liquidity, price discovery and the costs borne by slower traders", with the Flash Crash readings.
- ***Fragmentation and Price Formation*** and ***Outage Price Discovery*** → `market-structure-execution-quality`. Their mechanism is fragmentation itself: a common reference, stale primary quotes, pegged orders and the consolidated tape. Lehalle and Laruelle frame the outage this way (Introduction, pp. 5–7; chap. 2, sec. 2.5.2, pp. 183–186).
- ***Fast Liquidity and Price Discovery*** → `hft-market-design`. Its mechanism is fast market makers, speed investment and queue priority. Its fee-schedule point is secondary relevance to `market-structure-execution-quality`, for a cross-reference when migrated. Lehalle and Laruelle's source for it is app. A.2 (pp. 250–251), their summary of Foucault, Kadan and Kandel (2009), not read here.
- **Slice-4 systemic assignments, reassessed.** *Systemic Risk Link* → `market-structure-execution-quality`. Its claim is that fragmentation is not systemic risk by itself, but becomes dangerous through same-direction reactions, desynchronised venues and propagation to hedges. The subject is fragmentation's effect on market quality, not speed. *Shock Propagation Channels* stays with `hft-market-design`. Its channels are the Flash Crash mechanisms of linked electronic markets: high-frequency market makers hedging across futures and equities, routers pausing, pegged orders losing their reference, kill switches (Lehalle and Laruelle, sec. 2.5.2, p. 183). That pathway's readings cover them (`w5-kirilenko-flash-crash`, optional `w5-menkveld-yueshen-flash`). The reassignment migrates nothing; the block is unchanged.
- **Insider-information blocks.** No pathway in the pinned taxonomy covers insider-trading law for securities. The prediction-market and crypto pathways that mention insiders concern those markets, and `model-governance-controls` covers model risk and algorithm controls. Harris, a reading of the overview route, gives the economic definition and the U.S. summary, so the three blocks were migrated into one entry under that route, with its legal content dated 2002.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF, as in slices 2–4 (printed page = PDF page − 13) | As before |
| `s6-hasbrouck` | Local PDF, as in slices 3–4 (printed page = PDF page − 11) | As before |
| `alpha-laruelle` | Local PDF, as in slice 4 (printed page = PDF page − 27, Introduction included) | As before |

### Source findings

- **Fundamental value is not the efficient price.** Harris's fundamental value is the value everyone would agree on if all knew everything known about the instrument (chap. 10, pp. 222–223). Hasbrouck's fundamental value or efficient price conditions on all *public* information (sec. 3.2, p. 26). So Harris's noise $P_t-V_t$ is not the pricing error $s_t$ of `def:volatility-components`, and *Fundamental Value and Price Noise* became its own entry, `def:fundamental-value`, with the contrast in its Pitfalls. The legacy "all payoff-relevant information" reads as the perfect-foresight value, which Harris distinguishes from it.
- **Forecast aggregation** is Harris's algebraic box (p. 225). There the average price follows from linear demands with a common slope and zero net supply. The legacy proof's $\sigma^2/N$ needs a common variance that Harris does not assume (own step). Harris's claim that the market error is below the average individual error "if the individual forecast errors are not identical" holds for squared errors, not absolute ones (own check). The correlated-error caveat is own working, $\operatorname{Var}(e_M)=\sigma^2[
ho+(1-
ho)/N]$, consistent with Harris on correlated estimates (p. 237).
- **Market efficiency** is Harris sec. 10.6.6 (p. 240). His weak form uses past prices; volumes are in the semistrong set, not the weak-form set as the legacy notes had it. His cost-sensitive definition is unnamed; the legacy notes called it "economic". The information–liquidity trade-off is sec. 10.6.7 (p. 241). Publishing information is Harris's counterexample (sec. 10.6.8), added to the entry.
- **Insider information** is Harris chap. 29 (pp. 584–592), with the SEC's 2002 summary quoted in a box on p. 585. "Temporary insider", a personal-benefit tipping test, auditors, consultants and exchange staff are not in the passages. For *Signal Tradability Requires Permission*, confidentiality duties, employer pre-approval (p. 588) and liquidity (p. 236) are supported; restricted lists, signal compliance approval and data provenance are not. The legal details (reporting deadlines, prearranged plans, penalties) are dated 2002 and were left out of the entry.
- **Value traders.** *Value-Trader Profit Source Segmentation* listed three sources; Harris has two (chap. 16, pp. 338–339). New information profits news traders, and value traders gain there only by correcting news traders' errors (chap. 10, Table 10-1, p. 230; p. 239). Dealer inventory pressure is the indirect channel of uninformed demand (pp. 339–340). The no-trade band proposition is own working: a symmetric special case of the outside spread with one all-in half-cost. It was merged into `def:outside-spread` as an Interpretation, with the reason it understates Harris's widening factors. *No-Trade Is an Information Position* is Harris's box on p. 343.
- **Price formation process** is Lehalle and Laruelle's term. Its two phases, immediate impact and decay or resilience, are on pp. 27–29 (Figure 8, not inspected). The temporary-or-permanent impact depending on consensus is on pp. 3 and 28, and the design tension over information on pp. 19–20.
- **Returns by time scale.** *Volatility Scale Segmentation*, *Intraday and Overnight Returns*, *Correlation Interpretation* and *Microstructure to Macro Prices* follow Lehalle and Laruelle sec. 2.5 (p. 169) and sec. 2.5.1 (eqs. (2.2)–(2.3), pp. 174–177). They do not overlap `def:volatility-components` (fundamental against transitory) or `meth:garman-klass-volatility` (an estimator within intervals): they split time scales. So they became `def:intraday-overnight-returns`, with cross-references. The source finds correlation spikes mainly overnight; the legacy "different mechanisms at different horizons" was corrected. News revaluation overnight and benchmark paths are not in the passages. The authors' HFT explanation of the 2010 rise is flagged as a conjecture.
- **Outage (assigned, not migrated).** Lehalle and Laruelle date the Euronext halt to 13 October 2010 in the text but caption Figures 2.31–2.32 "October 10, 2010", a Sunday. The captions are probably wrong (own check of the calendar).
- **Not reopened.** The slice-4 question on the toy model's eq. (A.14) does not bear on these blocks and stays open. Sec. 2.5.3 (pp. 187–189) was not read; nothing here depends on it.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. 10 "Informed Traders and Market Efficiency", pp. 222–244; chap. 16 "Value Traders", pp. 338–346; chap. 29 "Insider Trading", pp. 584–598 | Text layer only; the SEC web page quoted on p. 585 not consulted |
| `s6-hasbrouck` | sec. 3.2, pp. 24–27 | Text layer |
| `alpha-laruelle` | Introduction, pp. 3–7, 19–20, 27–29; chap. 2, secs. 2.5–2.5.2, pp. 169–177 and 183–186; app. A.2, pp. 250–251 (routing only) | Text layer; no page images (equations (2.2)–(2.3) read cleanly); Figure 8 not inspected |

The six new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the revised `def:outside-spread`. No original paper was consulted: Grossman and Stiglitz (1980), Bouchaud et al. (2002) and Foucault, Kadan and Kandel (2009) are named only as the textbooks' sources.

### Dispositions

| Legacy block | Disposition |
|---|---|
| `01_...`: *Fundamental Value and Price Noise*, *Information Segmentation* | Rewritten as `def:fundamental-value` |
| `01_...`: *Material Nonpublic Information*, *Inside-Information Holder Segmentation* | Rewritten as `def:inside-information` |
| `01_...`: *Signal Tradability Requires Permission* | Merged into the Practice and Pitfalls of `def:inside-information` (unsupported parts named) |
| `01_...`: *Market Efficiency Segmentation* | Rewritten as `def:market-efficiency` |
| `01_...`: *Information-Liquidity Trade-Off* | Merged into the Practice of `def:market-efficiency` |
| `01_...`: *Forecast Aggregation Reduces Idiosyncratic Error* | Rewritten as `res:informed-trading-aggregation` |
| `01_...`: *Correlated Information Error* | Merged into the Pitfalls of `res:informed-trading-aggregation` |
| `02_...`: *Informed Trading Price Discovery* | Merged into the Statement of `res:informed-trading-aggregation` |
| `02_...`: *Price Formation Process (PFP)* | Rewritten as `def:price-formation-process` |
| `02_...`: *Value-Trader Profit Source Segmentation* | Merged into `def:outside-spread` (Conditions; correction in Pitfalls) |
| `02_...`: *Value Traders Supply Liquidity Outside the No-Trade Band* | Merged into the Statement of `def:outside-spread` (Interpretation) |
| `02_...`: *No-Trade Is an Information Position* | Merged into the Practice of `def:outside-spread` |
| `02_...`: *Volatility Scale Segmentation*, *Intraday and Overnight Returns* | Rewritten as `def:intraday-overnight-returns` |
| `02_...`: *Correlation Interpretation*, *Microstructure to Macro Prices* | Merged into the Practice and Pitfalls of `def:intraday-overnight-returns` |
| `02_...`: *Fragmentation and Price Formation*, *Outage Price Discovery* | Assigned to `market-structure-execution-quality`, left in legacy |
| `02_...`: *Fast Liquidity and Price Discovery* | Assigned to `hft-market-design`, left in legacy |
| `08_...`: *Systemic Risk Link* (slice 4) | Reassigned from `hft-market-design` to `market-structure-execution-quality`, left in legacy |

Cross-references only: `def:volatility-components` and `meth:garman-klass-volatility`. The 18 migrated blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Information, market efficiency and price discovery (slice 5)*. A script confirmed four things: each block appears there exactly once and in order; the artefact's earlier content is unchanged; the three blocks left in `02_...` are unchanged; and the eight blocks of `08_...` are unchanged (only the assignment line before *Systemic Risk Link* and the file's `% migrate-to:` line changed). `market-structure-execution-quality` was added to the `% migrate-to:` lines of `02_...` and `08_...`, and `hft-market-design` to that of `02_...`, with their map rows.

### Counts

`migration_status.py`: 805 → 787 legacy blocks (18 migrated). Assigned 26 → 29: `market-structure-execution-quality` 0 → 3 (two from `02_...`, *Systemic Risk Link* from `08_...`); `hft-market-design` 15 → 15 (one added, one moved out). One candidate only 135 → 135. Shared 644 → 623 (−18 migrated, −3 assigned). Entries 22 → 28 (definitions 4 → 9, results 8 → 9). Entries listed by pathway note: `execution-market-making` 0 → 15, `market-making-lob` 22 → 13 (nine moved, none deleted). No block is counted twice. No notation override was added: $V_t$, $P_t$, $\epsilon_t$, $f_i$, $e_i$ and the return superscripts are defined in the entries.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 152 pages (148 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. Rendered and inspected: the new section (PDF pp. 11–16), the revised outside spread (pp. 26–27), the new returns entry (pp. 29–30) and the pruned legacy section (p. 122). The chapter opener (p. 7) was also inspected. The artefact compiles on its own: 15 pages (13 before), no warnings, the same 3 underfull boxes; its new section (p. 14) was inspected. The tooling appendix was not affected and was not rebuilt.

### For review

- The six new entries and the revised outside spread, in particular:
  - the decision to keep Harris's fundamental value apart from Hasbrouck's efficient price;
  - the own-derivation notes: the variance of the average, correlated errors, squared and absolute errors, the no-trade band, and the return identity;
  - the insider entry's scope: economic definition plus dated U.S. summary, with no current law.
- The routing above: the three assignments of `02_...` and the reassignment of *Systemic Risk Link*.
- The new overview note and the nine entries moved into it.
- `03_.../06_strategic_trading_models.tex` repeats this slice's material (informed-trader styles, trading speed, insider-trading profitability and deterrence): consolidate it into these entries next.

## Slice 6: strategic trading models, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 5's pushed state (`80810ee`, on `main`, matching `origin/main`; guide submodule at `343d145`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Scope

The 30 blocks of `03_.../06_strategic_trading_models.tex`, shared between `execution-market-making` and `market-making-lob`. All 30 were migrated: 21 into seven new entries, 9 merged into new or existing entries. The file was deleted, with its `\input` line in `03_.../00_overview.tex` and its map row.

### Routing

Every block's source is Harris (`alpha-harris`), a reading of the overview route, and none concerns market making specifically, so all went to `execution-market-making`; nothing was put under `market-making-lob` by default. The pinned taxonomy has no general pathway for arbitrageurs, order anticipators or bluffers. The candidates are asset-specific or about funding (`statistical-arbitrage`, `commodity-spatial-arbitrage`, `fx-cip-dollar-funding`, `funding-crowding`, `futures-delivery-manipulation`, `crypto-exchange-market-quality`, `prediction-integrity`); the entries cross-reference them by key. *Specialist Order-Flow Strategy Segmentation* (Harris chap. 24) was merged into the order-anticipation entry rather than assigned to `market-structure-execution-quality`. Harris presents the specialists' quote matching and stop-order tactics as the order-anticipation strategies of chap. 11 (pp. 502–503), and the entry dates the specialist material to 2002. Settled routing decisions are unchanged.

### Sources and availability, 2026-10-15

`alpha-harris`, the local PDF used in slices 2–5 (printed page = PDF page − 13); text layer for all passages; page images of p. 225 (the aggregation box) and p. 270 (the bluffing example). No other source was needed.

### Overlaps resolved, from content

- **Informed-trader styles** were not in `res:informed-trading-aggregation`, which is about how prices aggregate estimates. So a new definition, `def:informed-trader-types` (Harris sec. 10.5, Table 10-3). *Value Traders vs News Traders* merged into it: it adds who loses to whom, beyond the profit sources already in `def:outside-spread`.
- **Trading speed** (aggressive, stealth) and **orthogonal information** were already in the Practice of `res:informed-trading-aggregation` from slice 5. They were merged there with what the blocks added: the reasons for each speed, and the precision–orthogonality trade-off of p. 237. The legacy "inactive" speed is stale information, not a speed.
- **The informed trading paradox** is Harris's market paradox, already in `def:market-efficiency`. Only the legacy wording difference was recorded.
- **Skilled speculation versus inside information** merged into `def:inside-information` (Harris's box, p. 590); its alternative-data and channel-check examples are flagged as unsupported.
- **Insider profitability, deterrence and market footprint** are a different concept from the definition, namely when insider trading pays and when it is caught. So a new result, `res:insider-trading-deterrence`, cross-referenced from the definition and tied to 2002 U.S. law.
- **The winner's curse** was a bullet in `def:outside-spread`; it is a general concept (auctions, value trading), so a new `def:winners-curse`, linked both ways.
- **Arbitrage** (six blocks) → `def:arbitrage`; **arbitrage risks** and the common-against-specific factor test → `res:arbitrage-risks`. No existing entry covered them. The no-trade band is the analogue of the value traders' band in `def:outside-spread`, linked, not merged.
- **Bluffing** (four blocks) → `def:bluffing-manipulation`; **order anticipation** (six blocks, specialists included) → `def:order-anticipation`. They are distinct mechanisms, false signals against information about others' orders. Harris treats stop gunning as manipulation inside the order-anticipation chapter, so it sits in the order-anticipation entry, cross-referenced.

### Source findings and corrections

- **Styles and speed** (chap. 10, pp. 226–235): the legacy technical-trader item covered all "predictable errors by other traders". Harris restricts information-oriented technical traders to informed traders' errors; trading on uninformed traders' predictable impact is order anticipation (p. 231).
- **Arbitrage** (chap. 17, pp. 347–379):
  - *Types:* Harris has two arbitrage types, pure and speculative. "Risk arbitrage" is a synonym for speculative arbitrage, usually meaning merger arbitrage, and statistical arbitrage is one kind of speculative arbitrage (pp. 350, 360). The legacy list had four parallel types.
  - *Cross-rate arbitrage* is a cyclic conversion arbitrage (p. 356), not a fourth pure mechanism.
  - *Risks:* Harris names four risks; the legacy "staying power" and "specific-factor" risks are consequences and sources of basis and carrying-cost risk.
  - *Terms:* basis, fair value, arbitrage spread and arbitrage bounds are Harris's own (p. 349); the legacy notation $A_t=B_t-B_t^\star$ matches.
- **Order anticipation** (chap. 11, pp. 245–258; chap. 24, pp. 498–508): quote matching is front running of passive traders, not a parallel category, and gunning the market is a manipulation of stop orders (sec. 11.4). Front running informed traders raises informativeness in the short run but lowers it in the long run (pp. 250–251), which the legacy block omitted.
- **Bluffing** (chap. 12, pp. 259–275): Harris has two bluffer types; wash trading is a price manipulator's technique, not a third type. The asymmetric-impact condition and Harris's worked example were added from pp. 270–273, and the example was rechecked.
- **Winner's curse** (chap. 16, pp. 341–343): supported. The legacy "information overlap" severity factor is not in the passages.
- **Insider trading** (chap. 29, pp. 588–595): the deterrence rule (expected benefit against probability times penalty, p. 590) is Harris's. The legacy $G\le K+R+qF$ adds $K$ and $R$ as own working. Penalty figures are 2002 U.S. law, labelled as dated.

### Mathematical checks (own, recorded as Interpretation in the entries)

- **Aggregation, reused and changed.** The estimator is $P=\sum_ia_if_i/\sum_ia_i$ from linear demands and zero net supply. It is unbiased when each $f_i$ is conditionally unbiased. With independent errors its variance is $\sum_ia_i^2\sigma_i^2/(\sum_ia_i)^2$, minimised by inverse-variance weights at $(\sum_i\sigma_i^{-2})^{-1}$. The equicorrelated variance $\sigma^2[\rho+(1-\rho)/N]$ was rederived from $\tfrac1{N^2}[N\sigma^2+N(N-1)\rho\sigma^2]$. It requires $\rho\ge-1/(N-1)$, and the limit $\rho\sigma^2$ assumes $\rho\ge0$.
- **Harris's comparison, rechecked against the page image of p. 225.** Slice 5's statement ("holds for squared errors, not absolute") was true only realisation by realisation, so it was restated by loss measure:
  - *Signed errors* average exactly.
  - *Squared errors* are strictly smaller unless all errors are equal, by the identity $\tfrac1N\sum e_i^2-e_M^2=\tfrac1N\sum(e_i-e_M)^2$.
  - *Absolute errors*, by the triangle inequality, are equal whenever the errors share a sign (counterexample $e=(1,2)$).
  - *In expectation*, with independent, zero-mean, nondegenerate errors, both are strict.
  - *"Better than any individual trader"* holds in expected squared error only with equal accuracies. The counterexample: variances 0.01 and 1 give 0.2525 for the equal-weighted average.
- **Winner's curse.** The legacy break-even bid $b^\star=\widehat V-\omega_N-c$ needs $\omega$ conditioned on one's own estimate and on winning *at that bid*. It is then a fixed point, $b=\widehat V-\omega(b)-c$, and it is the highest acceptable bid, not the optimal one.
- **Deterrence.** If the penalty is only disgorgement ($F=G$), the condition becomes $(1-q)G\le K+R$. $R$ is a cost only under risk aversion.
- **Arbitrage band.** $|A_t|>K_t+R_t$ assumes full convergence; with partial or slow convergence the gain is the expected narrowing net of extra carry.
- **Bluffing example.** Recomputed: \$1.5 million profit with asymmetric impact, a \$3 million loss with symmetric impact, and a \$0.4 million loss in 100-contract trades, all as printed (pp. 270–271).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. 10, pp. 222–244 (box p. 225 by page image); chap. 11, pp. 245–258; chap. 12, pp. 259–275 (p. 270 by page image); chap. 16, pp. 338–346; chap. 17, pp. 347–379; chap. 24, pp. 494–508; chap. 29, pp. 584–598 | Text layer except the two page images; the SEC web page and the cases Harris cites were not consulted |

The seven new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the four revised entries.

### Dispositions

| Legacy block (`03_.../06_strategic_trading_models.tex`) | Disposition |
|---|---|
| *Informed Trader Style Segmentation* | Rewritten as `def:informed-trader-types` |
| *Value Traders vs News Traders* | Merged into the Conditions of `def:informed-trader-types` |
| *Informed Trading Speed Segmentation*, *Orthogonal Information Advantage* | Merged into the Practice of `res:informed-trading-aggregation` |
| *Informed Trading Paradox* | Merged into `def:market-efficiency` (Conditions already held it; wording noted in Pitfalls) |
| *Skilled Speculation vs Inside Information* | Merged into `def:inside-information` (Statement; unsupported examples in Pitfalls) |
| *Insider-Trading Profitability Segmentation*, *Deterrence Condition for Illegal Information Trading* | Rewritten as `res:insider-trading-deterrence` |
| *Insider-Trading Market Footprint* | Merged into the Practice and Pitfalls of `res:insider-trading-deterrence` |
| *Arbitrage Opportunity*, *Basis and Arbitrage Spread*, *No-Trade Band for Basis Arbitrage* | Rewritten as `def:arbitrage` (the band as Interpretation) |
| *Arbitrage Characterisation Segmentation*, *Arbitrage Type Segmentation*, *Pure Arbitrage Mechanism Segmentation* | Merged into the Conditions of `def:arbitrage` (types corrected) |
| *Arbitrage Risk Segmentation* | Rewritten as `res:arbitrage-risks` |
| *Common vs Specific Factor Test* | Merged into the Conditions and Practice of `res:arbitrage-risks` |
| *Winner's Curse*, *Winner's-Curse Bid Adjustment* | Rewritten as `def:winners-curse` (the bid as a fixed point) |
| *Winner's-Curse Severity Segmentation* | Merged into the Conditions of `def:winners-curse` |
| *Bluffing and Manipulation Segmentation*, *Bluffers vs Informed Speculators* | Rewritten as `def:bluffing-manipulation` |
| *Value Traders Discipline Bluffs*, *Manipulation Evidence Problem* | Merged into the Conditions and Pitfalls of `def:bluffing-manipulation` |
| *Order-Anticipation Segmentation*, *Front-Running Effect*, *Sentiment-Oriented Technical Trading* | Rewritten as `def:order-anticipation` |
| *Quote Matching and Tick Protection*, *Squeezes and Stop Gunning*, *Specialist Order-Flow Strategy Segmentation* | Merged into the Conditions and Practice of `def:order-anticipation` |

`def:outside-spread` gained cross-references only. The 30 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Strategic trading models (slice 6)*. A script confirmed three things: each block appears there exactly once and in order; the artefact's earlier content is unchanged; and `02_...` and `08_...` are byte-identical to their state before the slice.

### Counts

`migration_status.py`: 787 → 757 legacy blocks (30 migrated). Assigned 29 → 29; one candidate only 135 → 135; shared 623 → 593. Entries 28 → 35 (definitions 9 → 14, results 9 → 11). Entries listed in pathway notes: `execution-market-making` 15 → 22, `market-making-lob` 13 → 13. No notation override was added.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 155 pages (152 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. Rendered and inspected: PDF pp. 12–22 (the revised aggregation entry, the new entries and section) and p. 128 (the pruned legacy section). The artefact compiles on its own: 18 pages (15 before), no warnings, the same 3 underfull boxes.

### For review

- The seven new entries and four revised ones. In particular:
  - the restated error comparison and the counterexample in `res:informed-trading-aggregation`;
  - the fixed-point form of the winner's-curse bid;
  - the merge of the specialist strategies into order anticipation rather than an assignment to `market-structure-execution-quality`.
- `03_.../07_liquidity_and_market_impact.tex` repeats this slice's bluffing material (*Round-Trip Manipulation Profit Test*, *Impact Symmetry Disciplines Bluffing*).

## Slice 7: liquidity and market impact, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 6's pushed state (`3780514`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts were confirmed before starting: 757 legacy blocks, 29 assigned, 593 shared, 35 entries; 22 entries listed for `execution-market-making` and 13 for `market-making-lob`. Migration and source checking, not study.

### Scope

The 6 blocks of `03_.../07_liquidity_and_market_impact.tex`, whose candidate pathways were `execution-market-making` and `market-structure-execution-quality`. All 6 were migrated, and the file, its `\input` line and its map row were deleted. No other legacy file was touched.

### Routing

- **Impact concepts → `price-impact-execution`.** Its outcome is to estimate an impact model, derive a schedule and measure shortfall. Its required readings include the propagator paper (`wide-bouchaud-propagator`), Gatheral's no-dynamic-arbitrage paper (`catalogue-0501`) and Webster's handbook (`wide-webster-price-impact`). The concepts of price impact, propagators and absence of manipulation are where that pathway first needs them. So the three entries opened the canonical chapter `compendium/execution-trading-costs/` (`section.tex`, `impact-models.tex`), which the compendium includes automatically once `section.tex` exists.
- **Neither candidate pathway owns this material.** `execution-market-making` lists none of these readings, and its checkpoint needs self-impact only as an assumption to vary. `market-structure-execution-quality` concerns rules, fees and execution quality, not impact models. `market-making-lob` does not apply.
- **Cross-references.** The overview entries that touch impact (`def:price-formation-process`, `res:spread-component-identification`, `def:bluffing-manipulation`) now cross-reference the new entries. The impact-symmetry block, Harris's bluffing rule, stayed in the overview's bluffing entry, its existing home.

### Overlaps resolved, from content

- **Temporary and permanent impact** (with *Market Impact Lens Segmentation* and *Permanent Impact Identification*) → new `def:price-impact`. Three existing entries touch the same words but not the same concept:
  - `def:price-formation-process` describes Lehalle and Laruelle's two phases of the price formation process;
  - `res:spread-component-identification` splits the *spread* into transitory and permanent components per trade (Hasbrouck);
  - `mod:grossman-miller` covers the concession for immediacy.

  None defines the impact of one's own trading, the reaction/prediction split or the decay over time. They are linked, not merged.
- **Propagator** → new `mod:propagator`. The generalized Roll model is recorded as its constant-propagator special case (Interpretation).
- **Round-trip manipulation test** → new `res:no-price-manipulation`. This is distinct from `def:bluffing-manipulation`. Bluffing fools other traders through their inferences (Harris), whereas price manipulation in an impact model is a round trip with negative expected cost through one's own impact, with nobody fooled (Gatheral's definition, via Webster).
- **Impact symmetry disciplines bluffing** restates the rule already in the Practice of `def:bluffing-manipulation` (Harris pp. 271–273). It was merged there, with its two additions qualified: "risk" is not in Harris, and its no-profit conclusion holds only in Harris's immediate, permanent-impact example.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `wide-webster-price-impact` | Local PDF outside the repository: Webster, *Handbook of Price Impact Modeling*, CRC, first edition 2023; printed page = PDF page − 17 | Copyright page: DOI 10.1201/9781003316923, matching the catalogue |
| `catalogue-0528` | Local PDF outside the repository: Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices*, Cambridge 2018; printed page = PDF page − 19 | Copyright page: ISBN 9781107156050, DOI 10.1017/9781316659335; the catalogue record does not establish an edition |
| `alpha-harris` | As in slices 2–6 | pp. 271–273 reread |

### Source findings

- **The blocks are not Harris's, except impact symmetry.**
  - *Lens taxonomy:* a simplification of Webster's four communities (chap. 1, sec. 1.1.5, pp. 9–15).
  - *Temporary/permanent and identification blocks:* follow Bouchaud et al. chaps. 11–12 (pp. 208–212, 240).
  - *Propagator:* their chap. 13 (pp. 249–253).
  - *Round-trip test:* the accounting behind Gatheral's definition of manipulation (Webster n. 3, p. 7).
  - *Impact symmetry:* Harris chap. 12 (pp. 271–273).
- **"Temporary impact" is ambiguous.** Almgren and Chriss use it for the instantaneous transaction cost (Webster n. 3, p. 53), not for a displacement that decays. The legacy definition mixed the two.
- **Permanent impact.** Correlated metaorders can mimic permanent impact, and permanent impact mixes reaction with prediction (Bouchaud et al. p. 240). The legacy controls for market and sector moves are not in the passages; the book suggests conditioning on the rest of the market's order-sign imbalance (p. 212).
- **The legacy "different decay profiles"** per trade belong to the generalised models of chap. 14, which was not read; the simple propagator has one kernel.
- **Conditioning in eq. (11.2).** As printed, observed impact conditions on execution only; the identity (11.4) needs $\mathcal F_t$ throughout, which the authors say is implicit (p. 210).

### Mathematical checks (own, Interpretation in the entries)

- **Round trip.**
  - *Identity:* with average execution prices that include impact, zero initial and terminal inventory, and explicit costs $F$, profit is $Q(\bar P_S-\bar P_B)-F$.
  - *Undefined $c$:* the legacy $c$ was not defined per side or per round trip; per side, $F=2Qc$.
  - *No double counting:* spread already in $\bar P$ must not be counted again in $c$.
  - *Realised against expected:* a realised profit is not manipulation, which concerns *expected* profit under a model with no information.
- **Webster's Example 2.7.1** (page image p. 94), rederived. Buying $\Delta$ at $t$ costs $(S_t+\tfrac12\lambda_t\Delta)\Delta$. Selling at $t'$ yields $(S_{t'}+e^{-\int\beta}\lambda_t\Delta-\tfrac12\lambda_{t'}\Delta)\Delta$. The profit is $(S_{t'}-S_t)\Delta+\tfrac12\lambda_t\Delta^2(2e^{-\int\beta}-1-e^{\int\gamma'})=(S_{t'}-S_t)\Delta-\tfrac12\lambda_t(2\beta+\gamma')h\Delta^2+o(h)$, as printed. With constant liquidity ($\gamma'=0$, $\beta>0$) the impact term is a cost. So a model that treats buys and sells alike can still admit manipulation through time-varying liquidity, and impact symmetry is not a general no-manipulation proof.
- **Volume bound.** $v'/v<4\beta$ gives a doubling time above $\ln2/(4\beta)$, a quarter of the half-life $\ln2/\beta$, as Webster states.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `wide-webster-price-impact` | chap. 1, pp. 3–15; chap. 2, pp. 53–54 and 93–97 | Text layer; page image of p. 94; Figure 2.5 and exercise 4 not inspected |
| `catalogue-0528` | chap. 11, pp. 208–212; chap. 12, pp. 240–241; chap. 13, pp. 249–253; chap. 19, pp. 361–362 | Text layer; page images of pp. 211, 252 and 362; chap. 14 and eq. (19.7) not read |
| `alpha-harris` | chap. 12, pp. 270–273 | Text layer and the slice-6 page image of p. 270 |

No original paper was consulted: Gatheral (2010), Fruth, Schöneborn and Urusov (2013), Bouchaud, Gefen, Potters and Wyart (2004) and Almgren and Chriss (2001) appear only through the two books.

### Dispositions

| Legacy block (`03_.../07_liquidity_and_market_impact.tex`) | Disposition |
|---|---|
| *Market Impact Lens Segmentation* | Merged into the Practice and Pitfalls of `def:price-impact` (corrected to Webster's four communities) |
| *Temporary and Permanent Impact* | Rewritten as `def:price-impact` (with the temporary-impact ambiguity) |
| *Propagator Intuition* | Rewritten as `mod:propagator` |
| *Round-Trip Manipulation Profit Test* | Rewritten as `res:no-price-manipulation` (the identity as Interpretation; Webster's example and Bouchaud et al.'s closed-trajectory result as the substance) |
| *Impact Symmetry Disciplines Bluffing* | Merged into the Practice of `def:bluffing-manipulation`, qualified, with a pointer to `res:no-price-manipulation` |
| *Permanent Impact Identification* | Merged into the Pitfalls of `def:price-impact` |

The 6 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Liquidity and market impact (slice 7)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and `02_...` and `08_...` are byte-identical to before.

### Counts

`migration_status.py`: 757 → 751 legacy blocks (6 migrated). Assigned 29 → 29; one candidate only 135 → 135; shared 593 → 587. Entries 35 → 38 (definitions 14 → 15, models 6 → 7, results 11 → 12). Entries listed: `price-impact-execution` 0 → 3 (new note), `execution-market-making` 22 → 22, `market-making-lob` 13 → 13. No notation override was added: Webster's $S$, $P$, $I$ and the impact superscripts are defined in the entries.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 159 pages (155 before; the new chapter adds pages); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had one new overfull box in the Status line of `def:price-impact`; it was reworded away. Rendered and inspected: PDF p. 22 (the revised bluffing entry), pp. 39–42 (the new chapter and entries) and p. 132 (the pruned legacy section). The artefact compiles on its own: 19 pages (18 before), no warnings, the same 3 underfull boxes.

### For review

- The three new entries and the revised bluffing entry. In particular:
  - the new canonical chapter and the routing to `price-impact-execution`;
  - the separation of strategic bluffing from mechanical manipulation;
  - the "temporary impact" terminology note.
- Whether `catalogue-0528`, on no route, should be the main empirical source for these entries until the pathway's own readings are studied.

## Slice 8: market impact models, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 7's pushed state (`c7ed121`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged).

**Baseline counts.** The reported counts were confirmed (751 legacy blocks, 29 assigned, 587 shared, 38 entries; 13 listed for `market-making-lob`, 3 for `price-impact-execution`) except one. The status script listed 23 entries for `execution-market-making`, not 22, because slice 7 had named `res:no-price-manipulation` under that note's Entries heading. The sentence was reworded, and the count is 22 again.

Migration and source checking, not study.

### Scope

The 10 blocks of `04_.../05_market_impact_models.tex`, whose only candidate pathway is `price-impact-execution`. All 10 were migrated. The file, its `\input` line in `04_.../00_overview.tex` and its map row were deleted. `04_.../04_price_impact_estimation.tex` was not touched.

### Routing

Slice 7's routing is carried forward: the entries live in the canonical chapter `compendium/execution-trading-costs/` under `price-impact-execution`. No block concerns market making or bluffing, so `def:bluffing-manipulation` and `res:no-price-manipulation` were compared but not changed.

### Overlaps resolved, from content

- *Model Family Segmentation*, *Permanent Impact or Price Anticipation* and *Permanent-Impact View Segmentation* → merged into `def:price-impact`, which already held the reaction/prediction split. The model families were added with the Almgren–Chriss definitions from the original. Bacry et al.'s mechanical and informational views were added with the book's split of permanent impact into prediction and reaction.
- *Propagator Midprice Dynamics*, *Trade-Sign Memory and Kernel Decay*, *Price Response Curve* and *Propagator Kernel Segmentation* → merged into `mod:propagator`, which already held the model, the sign-memory argument and the response function. Added: the 2004 original, kernel estimation, power-law decay and the fine balance, and the cause of sign memory.
- The **square-root law**, one item in the model-family list, is a distinct empirical regularity with its own required reading, so it became a new evidence entry, `ev:square-root-impact`.
- *Debiasing Long-Horizon Impact*, *CAPM-Like Post-Execution Decomposition* and *Autocorrelated Flow Bias* describe one procedure, Bacry et al.'s sec. 7.2, so they became a new method, `meth:post-execution-impact-profile`. It is cross-referenced from `def:price-impact`, which keeps the general warning that correlated metaorders mimic permanent impact.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-almgren` | Authors' preprint dated December 2000, from a Wayback snapshot (2017-08-11) of `cims.nyu.edu/~almgren/papers/optliq.pdf`; the catalogue's author link returned "Access forbidden" | Title, authors, date; journal pagination not checked |
| `wide-bouchaud-propagator` | arXiv cond-mat/0307332v2, 25 August 2003 | Title and authors match the catalogue; journal pagination not checked |
| `wide-bacry-life-cycle` | arXiv 1412.0217, printed 9 December 2014 | Title and authors match; journal version not checked |
| `catalogue-0528` | As in slice 7 | As before |
| `wide-webster-price-impact` | As in slice 7 | As before |

The downloads were kept in a scratch folder outside the repository and read only as PDF text and page images. Gatheral (2010), Fruth, Schöneborn and Urusov (2013), Tóth et al. (2011), Waelbroeck and Gomes (2013), Brokmann et al. (2014) and Bouchaud (2009) were not consulted; claims from them are attributed to the source that reports them.

### Source findings and corrections

- **"Temporary impact" has three meanings.** The original Almgren–Chriss $h(v)$ lowers only the execution price of one's own sale and does not enter the next market price (eq. (2), p. 9). Webster's reading of it as the instantaneous transaction cost is therefore confirmed from the original. Bacry et al. use "temporary market impact" for the impact at the end of execution (p. 3), a third meaning, recorded in `def:price-impact`.
- **Propagator block.** It departed from its sources in four ways:
  - it called $m_k$ the mid-price *after* trade $k$ while summing over $k'<k$, which in the sources is the price *before* the trade;
  - it used a single noise $\eta_k$ instead of the cumulative sum, which would make the price stationary apart from trading (Interpretation);
  - it dropped the original's $\ln V$ volume weight (eq. (12), p. 14 of the arXiv version), which the book's simple model also omits;
  - it said the response is estimated with the kernel, whereas response and sign correlation are measured and the kernel is estimated from them.
- **Sign memory.** The legacy block attributed it to splitting *and* similar agents trading together. Bouchaud et al. (book) find order splitting the primary cause and herding not relevant on the relevant time scale (p. 198).
- **Kernel taxonomy.** Non-parametric and power-law kernels are supported (pp. 254–257); exponential follows from the Obizhaeva–Wang model (Interpretation, from Webster). Agent-specific kernels are not in the passages checked.
- **Square-root law.** The legacy line omitted the volatility scale, the condition $Q\ll V_T$ and the exponent range 0.4–0.7 (book, eq. (12.6), p. 234).
- **Debiasing.** Bacry et al. could not classify trades as informed or liquidity-driven (broker data). That design is Waelbroeck and Gomes's, reported by them, and they remove only reference-index moves, not sector or factor moves. In their reading, the systematic component is aggregated information, not just a market move to exclude.

### Mathematical checks (own, Interpretation in the entries)

- **Units and signs:** Almgren–Chriss's linear forms $g=\gamma v$, $h=\epsilon\,\mathrm{sgn}(n)+(\eta/\tau)n$, with the units printed (eqs. (6)–(7)).
- **Book eq. (12.6):** dimensionally consistent, both sides in percent of price, as the authors state.
- **Bacry et al.'s eq. (21):** cumulates to $W_d-W_{D-1}$ plus the systematic part from $D-1$. Their beta is estimated over $D-20$ to $D+20$, so it is in-sample and can absorb the event. Removing the systematic part also removes any impact of the aggregate flow on the index. The debiasing inherits the error of the square-root model for later flow.
- **Kept distinct.** Permanent impact (a limit) against impact at a finite post-execution horizon (Bacry et al.'s 20 days). Observed against reaction and prediction impact. The simple common kernel against the extensions (volume weight, event types). No no-manipulation claim was made or changed in this slice.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-almgren` | secs. 1.2–1.5 and 2, pp. 7–13 (preprint) | Text layer; page images of pp. 9 and 11 |
| `wide-bouchaud-propagator` | secs. 3.1–3.2, pp. 14–17 (arXiv v2) | Text layer; page image of p. 14 |
| `wide-bacry-life-cycle` | abstract; sec. 2.2, pp. 3–4; secs. 7–8, pp. 19–22 (arXiv) | Text layer; page image of p. 21 |
| `catalogue-0528` | chap. 10, p. 198; chap. 12, pp. 233–236 and 241; chap. 13, pp. 254–257 | Text layer; page image of p. 234; chap. 14 seen only in the contents |

The two new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the two revised ones.

### Dispositions

| Legacy block (`04_.../05_market_impact_models.tex`) | Disposition |
|---|---|
| *Model Family Segmentation* | Merged into the Practice of `def:price-impact` (Almgren–Chriss from the original; linear; propagator and square-root linked); the square-root item rewritten as `ev:square-root-impact` |
| *Permanent Impact or Price Anticipation* | Merged into the Pitfalls of `def:price-impact` |
| *Permanent-Impact View Segmentation* | Merged into the Conditions of `def:price-impact` (Bacry et al.'s views) |
| *Propagator Midprice Dynamics* | Merged into `mod:propagator` (the 2004 original; departures corrected in Pitfalls) |
| *Trade-Sign Memory and Kernel Decay* | Merged into the Conditions of `mod:propagator` (splitting, not herding; the fine balance) |
| *Price Response Curve* | Merged into `mod:propagator` (definition already there; estimation direction corrected) |
| *Propagator Kernel Segmentation* | Merged into the Practice of `mod:propagator` (agent-specific kernels flagged unsupported) |
| *Debiasing Long-Horizon Impact*, *CAPM-Like Post-Execution Decomposition* | Rewritten as `meth:post-execution-impact-profile` |
| *Autocorrelated Flow Bias* | Merged into the Conditions of `meth:post-execution-impact-profile` |

The 10 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Market impact models (slice 8)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and the other files of `04_...` are byte-identical (only the `\input` line was removed from `00_overview.tex`).

### Counts

`migration_status.py`: 751 → 741 legacy blocks (10 migrated). Assigned 29 → 29; one candidate only 135 → 125 (these blocks counted to `price-impact-execution` alone); shared 587 → 587. Entries 38 → 40 (evidence 0 → 1, methods 3 → 4). Entries listed: `price-impact-execution` 3 → 5; `execution-market-making` 23 → 22 (the slice-7 listing artefact removed); `market-making-lob` 13 → 13. No notation override was added; $\mathcal I_d$ (index), $P_d$ (close) and the Almgren–Chriss coefficients are defined in their entries.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 160 pages (159 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had one new underfull box in the Status line of `mod:propagator`; it was reworded away. Rendered and inspected: PDF pp. 40–45 (the revised and new entries) and pp. 136–137 (the pruned legacy section, which now passes from *Price Impact Estimation* to *Trade Duration*). The artefact compiles on its own: 20 pages (19 before), no warnings, the same 3 underfull boxes.

### For review

- The two new entries and the revised `def:price-impact` and `mod:propagator`.
- Reliance on preprint versions of the three required readings.
- The three meanings of "temporary impact".
- The interpretation notes on Bacry et al.'s in-sample beta.

## Slice 9: price impact estimation, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 8's pushed state (`2214a1b`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 741 legacy blocks (125 single-candidate, 587 shared, 29 assigned), 40 entries, and pathway listings of 5, 22 and 13. Migration and source checking, not study.

### Scope

The 8 blocks of `04_.../04_price_impact_estimation.tex`, whose only candidate pathway is `price-impact-execution`. All 8 were migrated. The file, its `\input` line in `04_.../00_overview.tex` and its map row were deleted. No other legacy file was touched.

### Routing and overlaps, from content

Routing is carried forward: the entries live in `compendium/execution-trading-costs/` under `price-impact-execution`.

**Merged into existing entries:**
- *Execution-Time Impact* → `def:price-impact`. It is a measurement of the impact path, from the arrival price, signed and in spreads or volatility; the path itself is in the new evidence entry.
- *Timing Is Not Noise* → `def:price-impact`. It is the reaction/prediction split already there, with Lehalle and Laruelle's timing examples.

**New entries, because their designs or targets differ from the existing ones:**
- *Impact Has a Hump Shape*, *Impact Driver Segmentation* and *Participation-Duration Shape* → `ev:intraday-impact-profile`. Its target is the intraday path and its dependence on participation and duration, not the size scaling of `ev:square-root-impact`, so it is cross-referenced rather than merged.
- `meth:almgren-impact-estimation`. Almgren et al.'s design differs in target ("permanent" measured half an hour after the last fill, realised cost, temporary $J-I/2$), clock (volume time) and normalisation. It is kept distinct from Lehalle and Laruelle's fit and from Bacry et al.'s 20-day profile. No legacy block was solely its rewrite: it supports the participation, driver and execution-time blocks.
- *Order-Flow Impact Regression* and *Order-Flow Regression Identification* → `meth:order-flow-impact-regression`. This is a regression procedure on signed trades. It extends the generalized Roll model in `res:spread-component-identification`, which gained a cross-reference; it was not merged there because the target (per-trade permanent and transitory effects as functions of size) and the estimation question differ.
- *Index Reconstitution Impact* → `ev:index-reconstitution-impact`. The pathway `etf-index-closing-execution` is named as a reader.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-laruelle` | As in slices 4–5 | As before |
| `alpha-harris` | As in slices 2–6 | As before |
| `s6-hasbrouck` | The 2007 book PDF, `Empirical Market Microstructure_ ... (2007, Oxford University Press, USA) - libgen.li.pdf`. Another local file named "Joel Hasbrouck - Empirical market microstructure ... (2007).pdf" renders as his 2004 lecture-notes draft and was not used | Page image of p. 91 matches the 2007 book |
| `wide-almgren-direct-impact` | Authors' preprint of 10 May 2005, 26 pp., from a Wayback snapshot (2017-08-08) of `cims.nyu.edu/~almgren/papers/costestim.pdf` | Title, authors and date; the published Risk version was not compared |
| `wide-bacry-life-cycle` | arXiv preprint of 9 December 2014, as in slice 8 | As before; Lehalle and Laruelle (2018) restate its procedure, citing the 2015 paper |

Not consulted: Glosten and Harris (1988), Madhavan (2002), Moro et al. (2009), Huberman and Stanzl (2004), Tóth et al. (2011). Claims from them are attributed to the source that reports them. Slice 8's checks of Almgren and Chriss covered only selected passages of a preprint and were not reused as a check of Almgren et al. (2005).

### What each estimator measures

| Design | Target and horizon | Unit and benchmark | Normalisation | Sample and uncertainty |
|---|---|---|---|---|
| Lehalle and Laruelle (`ev:intraday-impact-profile`) | Price path during and after execution; dependence on participation and duration | Order; signed move from the arrival price | Bid–ask spreads; participation = share of market volume during execution; duration in 5-minute intervals | Crédit Agricole Cheuvreux, CAC 40, 2010; bucket averages; 95% band on the path; no exponent uncertainty reported |
| Bacry et al. (same entry, and `meth:post-execution-impact-profile`) | Signed move at the end of execution; daily profile to 20 days | Metaorder; relative mid-price move from the start | Daily participation $R$ or trading rate $r$; duration $T$ | One European broker, 2010; L1, L2 and log-log fits, no standard errors in Table 2 |
| Almgren et al. (`meth:almgren-impact-estimation`) | $I$ to half an hour after the last fill; realised $J$; temporary $J-I/2$ | Order; pre-trade midpoint | Volume time; size relative to volume during execution; volatility; inverse turnover | Citigroup, S&P 500, 2001–2003, 29,509 orders after filters; one-standard-deviation errors; $R^2$ below 1% |
| Glosten–Harris (`meth:order-flow-impact-regression`) | Per-trade permanent and transitory effects | Trade (event time) or interval (clock time); trade prices or midpoints | Trade size | Assumes size and sign exogenous; the original not read |
| Russell reconstitution (`ev:index-reconstitution-impact`) | Monthly return difference, additions against deletions | Stock; June and July returns | None | 1996–2001 averages, via Harris |

### Source findings and corrections

- **Participation and duration.** *Participation-Duration Shape* is Lehalle and Laruelle's eq. (3.1) (p. 208, page image), with only $\gamma\approx0.5$ reported. Bacry et al.'s Table 2 shows that the sign of the duration effect depends on what is held fixed: negative at fixed daily participation, positive at fixed trading rate. That reconciles the two. Interpretation: $R=rT$ gives $T^{a+b}$, $a+b\approx0.2$–0.36. Almgren et al. reject the square root at 95% for temporary impact (exponent $0.600\pm0.038$); that was added to `ev:square-root-impact`.
- **Drivers.** Tick size, depth, side, auctions and venue access are not in the passages. The sources disagree on the spread (Almgren et al.: no consistent dependence; Bacry et al.: a log-log exponent of 0.28).
- **The regression block** is Harris's box (p. 435, page image), the Glosten–Harris model with only size-proportional permanent impact. Hasbrouck's statement of the model has also a size-independent permanent term, $\lambda_0$ (eq. (9.26), p. 91, page image); the legacy form sets $\lambda_0=0$. Harris's sentence that regression "ensures" an error uncorrelated with the regressors confuses residual orthogonality with exogeneity (Interpretation).
- **The identification caveat's controls.** Partly supported:
  - *Index return:* Hasbrouck p. 87.
  - *Volume time:* Almgren et al.
  - *Volatility and spread:* Bacry et al.

  Controls alone do not make coefficients causal (Interpretation).
- **Index reconstitution.** Harris's box (p. 487, page image) reports the 15% and 5% figures from Madhavan (2002), not consulted. The legacy residual explanations (ownership, attention, information) are not Harris's; his are liquidity value, momentum, or later reversal.
- **"Permanent" is horizon-dependent.** Almgren et al.: half an hour after the last fill. Lehalle and Laruelle: one day. Bacry et al.: a 20-day profile. Each entry states its horizon.
- **Bacry et al.'s in-sample beta.** Lehalle and Laruelle's restatement keeps the same window and least-squares beta. The question stays open; a same-author restatement is not independent evidence.

### Mathematical checks (own, Interpretation in the entries)

- Differencing Hasbrouck's eq. (9.26) gives $\Delta p_t=\lambda_0q_t+\lambda_1q_tV_t+c_0\Delta q_t+c_1\Delta(q_tV_t)+u_t$; Harris's form follows with $\lambda_0=0$.
- Almgren et al.'s Table 3 recomputed from the fitted coefficients: IBM $I=19.9$ bp, $J=32.2$, $24.6$, $18.4$ bp; DRI $I=21.7$ bp, $J=42.9$, $32.0$, $23.1$ bp. These match the printed 20, 32, 25, 18 and 22, 43, 32, 23 bp to rounding.
- The duration reconciliation above, from Bacry et al.'s Table 2.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | chap. 3, secs. 3.2–3.2.2, pp. 203–215 | Text layer; page image of p. 208 |
| `alpha-harris` | chap. 21, box p. 435; chap. 23, box p. 487 | Page images of both |
| `s6-hasbrouck` | secs. 9.6–9.8.1, pp. 87–92 | Text layer; page image of p. 91 |
| `wide-almgren-direct-impact` | preprint pp. 1–22 | Text layer; page images of pp. 19 and 21 |
| `wide-bacry-life-cycle` | arXiv sec. 3, pp. 5–8 | Text layer; page image of p. 8 |

The four new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the three revised ones.

### Dispositions

| Legacy block (`04_.../04_price_impact_estimation.tex`) | Disposition |
|---|---|
| *Execution-Time Impact* | Merged into the Practice of `def:price-impact` |
| *Impact Has a Hump Shape* | Rewritten as `ev:intraday-impact-profile` (Statement) |
| *Impact Driver Segmentation* | Merged into the Practice and Pitfalls of `ev:intraday-impact-profile` (unsupported drivers named) |
| *Participation-Duration Shape* | Rewritten as `ev:intraday-impact-profile` (eq. (3.1); Bacry et al.'s comparison; Almgren et al. in `meth:almgren-impact-estimation`) |
| *Order-Flow Impact Regression* | Rewritten as `meth:order-flow-impact-regression` |
| *Index Reconstitution Impact* | Rewritten as `ev:index-reconstitution-impact` |
| *Order-Flow Regression Identification* | Merged into the Pitfalls of `meth:order-flow-impact-regression` |
| *Timing Is Not Noise* | Merged into the Pitfalls of `def:price-impact` |

Also changed:
- `ev:square-root-impact`: Almgren et al.'s 3/5 exponent and Bacry et al.'s duration factor.
- `meth:post-execution-impact-profile`: Lehalle and Laruelle's restatement.
- `res:spread-component-identification`: a cross-reference.

The 8 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Price impact estimation (slice 9)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and the other files of `04_...` are byte-identical (only the `\input` line was removed from `00_overview.tex`).

### Counts

`migration_status.py`: 741 → 733 legacy blocks (8 migrated). Single-candidate 125 → 117; shared 587 → 587; assigned 29 → 29. Entries 40 → 44 (evidence 1 → 3, methods 4 → 6). Entries listed: `price-impact-execution` 5 → 9; `execution-market-making` 22 → 22 (one of its entries gained a cross-reference, recorded in its note without a new listing); `market-making-lob` 13 → 13. No notation override was added: the house trade sign $q_t$ is kept, and Almgren et al.'s $I$, $J$ and coefficients are declared local in their entry.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 163 pages (160 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning; no new boxes. Rendered and inspected: PDF p. 40 (the revised `def:price-impact`), pp. 44–48 (the revised and new entries) and pp. 140–141 (the pruned legacy section, which no longer contains *Price Impact Estimation* or *Market Impact Models*). The artefact compiles on its own: 21 pages (20 before), no warnings, the same 3 underfull boxes.

### For review

- The four new entries and the three revised ones.
- The decision to give Almgren et al.'s design its own method entry.
- The $\lambda_0$ correction to the Glosten–Harris form.
- The duration reconciliation.
- The reliance on preprints (Almgren et al. 2005, Bacry et al. 2014) and on Harris's report of Madhavan.

## Slice 10: optimal execution problem, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 9's pushed state (`3d597b1`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 733 legacy blocks (117 single-candidate, 587 shared, 29 assigned), 44 entries, and listings of 9, 22 and 13. `price-impact-execution`'s 36 were candidate associations of shared blocks, not owned blocks, and are reported that way below. Migration and source checking, not study.

### Scope

The 9 blocks of `execution-trading-costs/01_.../01_optimal_execution_problem.tex`, shared in the map between `price-impact-execution` and the section overview `execution-trading-costs`. All 9 were migrated. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership

The overview's outcome asks for a schedule and an expected cost with its uncertainty "from a stated impact model". Its readings include `alpha-almgren` ("Set a benchmark for the trade-off between impact risk and execution speed"). The guide therefore first needs the scheduling model at the overview; `price-impact-execution` builds on it to estimate impact models and derive schedules. Block trading is part of planning an order's execution (venue, mechanism, schedule) and has no specialist pathway in the pinned taxonomy. Both new entries are therefore owned by the overview. A note was opened for it, `notes/pathways/execution-trading-costs.md`, on the same basis as the `execution-market-making` note in slice 5. The impact concepts the entries use stay with `price-impact-execution` and are cross-referenced. Owned listings and cross-references are kept apart: a first draft of the note named two `price-impact-execution` entries under its Entries heading, which the checker counted as owned, and it was reworded.

| Legacy block | Owner | Destination | Disposition |
|---|---|---|---|
| *Impact-Risk Trade-Off* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Statement) | Merged |
| *Discrete Execution Schedule* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Notation; timing in Pitfalls) | Merged |
| *Temporary Impact Cost* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Notation and Conditions; temporary-impact concept in `def:price-impact`) | Merged |
| *Expectation-Minimising Schedule* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Conditions) | Merged (a result, not a definition) |
| *Risk-Only Schedule* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Conditions) | Merged |
| *Mean-Variance Execution Objective* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Statement and Conditions; comparative static corrected) | Rewritten |
| *Execution Schedule Segmentation* | `execution-trading-costs` | `mod:almgren-chriss-execution` (Practice; convexity corrected) | Merged |
| *Block Order* | `execution-trading-costs` | `def:block-trade` | Rewritten |
| *Block Execution Problem Segmentation* | `execution-trading-costs` | `def:block-trade` | Merged |

### Sources and model identity, 2026-10-15

- **The notation of the blocks** ($v^\star$, $\kappa\sigma_n(v_n/V_n)^\gamma$, $v_n^{\exp}$) is Lehalle and Laruelle's app. A, sec. A.7 (pp. 273–281). They call it a "simplified and commented version of the original Almgren–Chriss paper". It is distinct from Almgren–Chriss's linear model and from Almgren et al. (2005), whose empirical procedure is `meth:almgren-impact-estimation`.
- **Almgren and Chriss** were checked in the authors' preprint of December 2000, the copy obtained in slice 8. The passages used in slice 8 (pp. 8–11) were reused; additional passages were read for this slice (sec. 1.1, p. 7; eqs. (4)–(5), p. 10; secs. 2–2.3, pp. 11–15, with a page image of p. 14). The 2001 journal version was not compared.
- **Harris** chap. 15, pp. 322–327, for the block blocks.
- The Cartea–Jaimungal framework in A.7.3 was read but not used, since no block draws on it.

### Mathematical checks (own, Interpretation in the entry)

**Units and conventions.** The concession $\kappa\sigma_n(v_n/V_n)^\gamma$ is currency per share, with $\sigma_n$ in currency per slice (p. 275). The slice cost is $v_n$ times it, and the order's expected impact cost is $\kappa\sum\sigma_nv_n^{\gamma+1}/V_n^\gamma$, a total, not a rate. It is a temporary cost on the slice's own fills, not a transient displacement. There is no permanent-impact term and no spread or fee term, unlike Almgren–Chriss's $g$ and $\epsilon$.

**Expectation-only schedule.** (A.22) rederived: marginal impact costs are equalised across slices. A numerical check (random $V_n$, $\sigma_n$, $\gamma=0.6$) found no feasible perturbation that lowers expected cost. The source's Lagrange condition omits $\kappa$, which is harmless because $\kappa$ is absorbed into the multiplier.

**Timing.** Lehalle and Laruelle's (A.16) prices slice $n$ after shock $n$, and (A.24) sums over the quantity remaining from slice $n$ on. Their terminal conditions $x_0=v^\star$, $x_N=0$ belong to the other convention. The legacy blocks use the Almgren–Chriss convention (slice $n$ at $S_n$, then $S_{n+1}=S_n+\sigma_n\xi_{n+1}$), under which their risk term $\lambda\sum x_n^2\sigma_n^2$ with $x_0=v^\star$, $x_N=0$ is consistent.

**Recurrence and closed form.** (A.28) rederived from the first-order conditions. For $\gamma=1$ and constant parameters, the legacy-convention solution equals the Almgren–Chriss $\sinh$ trajectory with $\cosh k=1+\lambda\sigma V/(2\kappa)$, numerically to $10^{-12}$. The mapping is $\kappa\sigma_n/V_n\leftrightarrow\eta/\tau$ and $\sigma_n^2\leftrightarrow\sigma^2\tau$, without the $\tilde\eta$ correction. Proposition 5 is mislabelled "variance minimization" in the source.

**Comparative statics.** The minimiser depends only on $\lambda/\kappa$. The legacy "higher impact sensitivity back-loads" is corrected: larger $\kappa$ moves the schedule towards the expectation-only one. In the varying-parameter cases checked it never went beyond it; that is numerical evidence, not a proof.

**Shape.** The mean–variance path is convex for constant parameters (the $\sinh$ form). With time-varying $V_n$ and $\sigma_n$ all 200 random cases checked were non-convex, so the legacy "convex remaining-quantity path" holds only under constant parameters.

**Variance-only schedule.** Zero variance in Almgren–Chriss is an artefact of the discretisation, as they say (p. 12).

**Parameters against estimates.** The model's $\kappa,\gamma$ are inputs estimated daily or weekly (p. 274). Almgren et al.'s exponent 0.6 measures a related quantity at a 30-minute post-trade horizon; the two are linked only by a cross-reference.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | app. A, sec. A.7, pp. 273–284 | Text layer; Figure A.11 seen only in the text layer |
| `alpha-almgren` | author preprint (Dec. 2000), pp. 7–15 | Text layer; page images of pp. 9, 11 and 14; the journal version not compared |
| `alpha-harris` | chap. 15, pp. 322–327 | Text layer |

The two new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The 9 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Optimal execution problem (slice 10)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and the other files of `execution-trading-costs/01_...` are byte-identical (only the `\input` line was removed from `00_overview.tex`).

### Counts

`migration_status.py`: 733 → 724 legacy blocks (9 migrated). Shared 587 → 578; single-candidate 117 → 117; assigned 29 → 29. Each of the 9 blocks was a candidate of both pathways, so the per-pathway candidate counts fell by 9 each: `execution-trading-costs` 57 → 48, `price-impact-execution` 36 → 27. This is one block counted under two candidates, not 18 blocks. Entries 44 → 46 (definitions 15 → 16, models 7 → 8). Entries listed: `execution-trading-costs` 0 → 2 (new note); `price-impact-execution` 9 → 9; `execution-market-making` 22 → 22; `market-making-lob` 13 → 13. No notation override was added: the entry declares its $\kappa$, $\gamma$ and $\lambda$ locally, against the Almgren–Chriss symbols.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 164 pages (163 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning; no new boxes. Rendered and inspected: PDF pp. 39–41 (the chapter opener and the new section) and p. 151 (the pruned legacy chapter, which now starts at *Execution Benchmarks*). The artefact compiles on its own: 21 pages (as before, the new section fitting the last page), no warnings, the same 3 underfull boxes.

### For review

- The two new entries.
- Ownership by the overview rather than `price-impact-execution`.
- The timing-convention resolution and the corrected comparative static and convexity claims.
- Reliance on the Almgren–Chriss preprint.

## Slice 11: execution benchmarks, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 10's pushed state (`bbaafa5`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 724 legacy blocks (117 single-candidate, 578 shared, 29 assigned), 46 entries, listings of 2, 9, 22 and 13, and candidate associations of 48 (`execution-trading-costs`) and 27 (`price-impact-execution`). Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../02_execution_benchmarks.tex`: its 3 counted blocks (*Benchmark Matches Trading Need*, *Regional Benchmark Preference*, *Benchmark Is Not an Objective Alone*) and the uncounted table *Typical uses of benchmarks for trading algorithms*, with its settings and caption. There was no prose outside these. The file was shared in the map between the overview `execution-trading-costs` and `market-structure-execution-quality`. It contains no implementation-shortfall formula; the benchmarks it names are PoV, VWAP/TWAP, implementation shortfall and liquidity seekers. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership

The content is the choice of an algorithm's benchmark for an order, by size, market context and the risk to hedge. That is planning an order's execution, which is the overview's outcome ("plan the execution ... and split realised implementation shortfall"), and its checkpoint measures shortfall against arrival price; its first reading is Perold's implementation-shortfall paper and `exp-fx-algos` is on "venue and benchmark choices". `market-structure-execution-quality` covers fragmentation, dark trading, fees, tick size, odd lots, retail routing, trading hours and the rule changes; the file touches fragmentation and HFT only as Lehalle and Laruelle's reasons for a regional preference, so it has no block of its own there and is cross-referenced by name (it has no entries yet). Perold's place was one input; the decision rests on the blocks' content.

Existing entries were searched first. `mod:almgren-chriss-execution` holds the schedule and its expected shortfall, not benchmark definitions; `def:price-impact` and `meth:almgren-impact-estimation` hold impact concepts and one firm's estimation; `def:spread-measures` (owned by `execution-market-making`) already holds the effective and realised spreads, Harris's contemporaneous and post-trade midpoint benchmarks. Nothing defined a benchmark price, an algorithm target or implementation shortfall, so three entries were created, all owned by the overview: the benchmark definitions, kept apart from the source-specific choice method and from Harris's and Kissell's measurement conventions, and implementation shortfall, which the table's IS row and the overview's checkpoint both need. The others are cross-referenced, not listed.

| Legacy item | Owner | Destination | Disposition |
|---|---|---|---|
| *Benchmark Matches Trading Need* (principle) | `execution-trading-costs` | `meth:algorithm-benchmark-choice` (Statement, Practice) | Merged |
| *Regional Benchmark Preference* (taxonomy) | `execution-trading-costs` | `meth:algorithm-benchmark-choice` (Statement; rationales corrected in Pitfalls) | Rewritten |
| Table *Typical uses of benchmarks for trading algorithms* (not a counted block) | `execution-trading-costs` | Rows: `meth:algorithm-benchmark-choice`, rebuilt as a sourced summary of Lehalle and Laruelle's Table 3.1 with links to the definitions; the benchmarks it names: `def:execution-benchmark` and `def:implementation-shortfall` | Rebuilt; original kept verbatim in the artefact |
| *Benchmark Is Not an Objective Alone* (caveat) | `execution-trading-costs` | `meth:algorithm-benchmark-choice` (Pitfalls, Interpretation) | Rewritten |

### Sources, 2026-10-15

- **Lehalle and Laruelle**, sec. 3.4.1, pp. 227–231, Table 3.1 on p. 229 by page image: the source of all three blocks and the table (2018 World Scientific printing; text layer, printed page = PDF page − 27). Table 3.2 (p. 230) and sec. 3.1 (pp. 193–201) read for context.
- **Perold (1988)**, `wide-perold-shortfall`, identified from the pinned catalogue record (*Journal of Portfolio Management* 14(3), 4–9, DOI 10.3905/jpm.1988.409150). No copy was available: the DOI resolves to the publisher's site, which refused the request (HTTP 429), and the search found only a ProQuest preview page and secondary accounts. It was not read, and nothing in the entries rests on it directly.
- **Kissell**, `s7-kissellscience`, local copy identified from its title page, copyright page (Academic Press, copyright 2014) and ISBN 978-0-12-401689-7; the catalogue cites it as 2013. Chap. 1, pp. 16–18 (algorithm types); chap. 3, pp. 97–108 (cost conventions, Perold and Wagner formulations, arrival cost, benchmark, VWAP and participation-weighted price performance), page images of pp. 100, 103 and 105. Printed page = PDF page − 19. Its attribution of the formulas to Perold and Wagner is secondary.
- **Harris**, chap. "Liquidity and Transaction Cost Measurement", pp. 424–437, Table 21-1 (p. 433) by page image: price-benchmark estimators, implementation shortfall with the filled and missed parts, the properties of each benchmark, missed-trade costs and the Plexus box. His attribution to Perold and Treynor is secondary.

### What each benchmark fixes (from the sources; details in `def:execution-benchmark`)

| Benchmark | Reference price and time | Weighting and eligible trades | Own fills | Unfilled quantity | Known |
|---|---|---|---|---|---|
| Decision price (Perold IS) | Midpoint when the manager decides (Harris p. 426); often the previous close (p. 437) | One price | Not in the benchmark | Opportunity cost at a later price | Before the order |
| Arrival price | Midpoint when the order enters the market; last trade or official close after hours (Kissell p. 102) | One price | Not in the benchmark | Opportunity cost from $P_0$ (Wagner) | At the start of trading |
| VWAP (full day, interval, to end of day) | The day, the order's horizon, or from the start to the close | Trade-size weights (Harris p. 425); vendors choose eligible trades and may drop delayed or negotiated ones (Kissell p. 107) | Included: biases towards zero for large orders | Not measured | Afterwards |
| Participation-weighted price at $\rho$ | First (shares traded)$/\rho$ market shares from arrival (Kissell p. 108) | Volume weights | Included | Window shrinks with fills (Interpretation) | Afterwards |
| Open, close, later closes | Single daily prices (Harris p. 425; Kissell p. 106) | — | Close moved by own impact (Harris p. 429) | Not measured | Open before, close after |
| TWAP | Algorithm only (Kissell p. 17); no benchmark price defined in the passages checked | — | — | — | — |
| PoV, liquidity seeker | Algorithm targets; no reference price (Kissell p. 17; Lehalle and Laruelle p. 230) | — | — | PoV completion not guaranteed (Kissell p. 17) | — |

Units and signs: basis points of the benchmark with a side factor (Kissell eqs. (3.11)–(3.14)), or currency for implementation shortfall; cost and gain sign conventions both occur (pp. 97, 108). Gross and net: the benchmark formulas exclude fees; implementation shortfall adds them.

### Accounting checks (own, Interpretation in the entries)

- **Reconciliation.** For a buy of 10,000 shares (decision midpoint 50.00, arrival 50.10, fills 3,000 at 50.20 and 3,000 at 50.30, rest cancelled, $P_n=50.60$, fees 60), paper minus real portfolio gives 3,960; Perold's components 1,500 + 2,400 + 60 and Wagner's 1,000 + 900 + 2,000 + 60 both reconcile exactly (rational arithmetic). The mirror-image sell with signed quantities gives the same figures. Kissell's three worked examples reproduce (\$2,600; \$3,080 as 2,000/1,000/80 and as 1,250/1,000/750/80), as do Harris's split-order example (\$400 against the decision midpoint, zero against VWAP, −\$200 against the close) and DINE missed-trade figures (\$12,600 and \$714,600).
- **Corrections to the source.** Kissell's intermediate actual return for a partial fill adds fees instead of subtracting them (p. 100); his final formula is right. His eq. (3.10) divides by the signed $(\sum s_j)P_0$ and so reverses the sign for sells (−30.06 against +30.06 bp in the example), unlike (3.11); (3.16) has no side factor. He describes TWAP as "a constant participation rate" while meaning a constant rate in time.
- **Double counting.** With a midpoint decision or arrival price the half-spread is already inside the execution component; adding an effective-spread term counts it twice, and fees enter once as the explicit term. No source checked splits the trading-related part into spread and impact, as the overview's checkpoint asks.
- **Model against measurement.** Almgren–Chriss's shortfall $XS_0-\sum n_k\tilde S_k$ equals Kissell's trading-related part for a complete sale from the pre-trade price (checked on the sell example: 900 both ways); its mean and variance are model forecasts, it has no opportunity term, and its temporary impact already carries half-spread and fees. Performance against an algorithm's own target (VWAP) is not its cost.

### Corrections to the legacy text

- Asia's rationale: the source speaks of differences between local markets, not "fragmented market conventions".
- Europe's rationale: the source names avoiding detection by HFT as well as routing efficiency.
- The table's risk column condensed Lehalle and Laruelle's "do not miss ..." wording and dropped "especially if I have the information" for PoV.
- The caveat is Interpretation, consistent with the risk–reward reading on p. 228 but not in the source.
- The table's "benchmarks" are algorithm classes; PoV and liquidity seekers are not benchmark prices.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | sec. 3.4.1, pp. 227–231 | Text layer; Table 3.1 by page image |
| `s7-kissellscience` | chap. 1, pp. 16–18; chap. 3, pp. 97–108 | Text layer; page images of pp. 100, 103, 105; not on a route |
| `alpha-harris` | chap. 21, pp. 424–437 | Text layer; Table 21-1 by page image |
| `wide-perold-shortfall` | none | Not available; unread |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Execution benchmarks (slice 11)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears there once, and that the three blocks and the table (with its `\stepcounter`, column settings and caption) each appear once and in order. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`. The table's disposition is recorded separately above, since the checker counts only the three blocks.

### Counts

`migration_status.py`: 724 → 721 legacy blocks (3 migrated). Shared 578 → 575; single-candidate 117 → 117; assigned 29 → 29. Each block was a candidate of `execution-trading-costs` and `market-structure-execution-quality`, so each pathway's candidate associations fell by 3: 48 → 45 and 321 → 318 (3 blocks, not 6). `price-impact-execution` stays at 27. Entries 46 → 49 (definitions 16 → 18, methods 6 → 7). Entries listed: `execution-trading-costs` 2 → 5; `price-impact-execution` 9; `execution-market-making` 22; `market-making-lob` 13.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 167 pages (164 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had three overfull boxes in the new section (a long key at a line end, the table's paragraph indent, a long path), fixed before commit. Rendered and inspected: PDF pp. 39–43 (the chapter opener, the new section and its table) and p. 154 (the pruned legacy chapter, which now starts at *Execution Algorithms*). The artefact compiles on its own: 22 pages (21 before), no warnings, the same 3 underfull boxes; its new last page shows the original table.

### For review

- The three new entries, and ownership by the overview rather than `market-structure-execution-quality`.
- Reliance on Kissell and Harris for implementation shortfall while Perold is unread.
- The corrections to Kissell's eq. (3.10) and p. 100, and the double-counting and model-against-measurement notes.

## Slice 12: execution algorithms, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 11's pushed state (`5d113ac`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 721 legacy blocks (117 single-candidate, 575 shared, 29 assigned), 49 entries, listings of 5, 9, 22 and 13, and candidate associations of 45 (`execution-trading-costs`), 27 (`price-impact-execution`) and 318 (`market-structure-execution-quality`). Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../03_execution_algorithms.tex`: 17 counted blocks (the proposition's proof is inside its block), the uncounted table *Typical features of trading algorithms* with its settings and caption, and the closing sentences inside the taxonomies. There was no prose outside the blocks and the table. The file was shared in the map between the overview `execution-trading-costs` and `price-impact-execution`. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted. `04_transaction_cost_analysis.tex` was not touched.

### Ownership

The blocks describe how an order is worked: an algorithm's parameters, risk-control layer and tactics; customising it; pre-trade and monitoring tools; order exposure and routing; portfolio and index trading; and a hedging rule's own execution demand. That is the overview's outcome, planning the execution of an order by venue, mechanism and schedule. `price-impact-execution`'s outcome is estimating impact models, deriving schedules and measuring shortfall with confidence intervals; its models are inputs to the risk-control layer, so it is cross-referenced, not given blocks. The positive-feedback blocks could have gone to the 1987-crash entry `mech:bubble-crash-dynamics`, but that belongs to `execution-market-making`, not a candidate here, and covers the crash, not the hedging rule's mechanics; the new entry cross-references it.

Existing entries were compared first. `def:execution-benchmark` already separates VWAP and TWAP as prices and as policies, and is not repeated; `meth:algorithm-benchmark-choice` already cited Table 3.2, so the table was added to it rather than to a new entry; `mod:almgren-chriss-execution` holds the two algorithm layers from app. A.7 and a model for the trading curve; `def:block-trade` holds order exposure as a block problem, and `ev:index-reconstitution-impact` the reconstitution timing. Algorithm variants (VWAP, TWAP, POV, IS, liquidity seeker) are described inside `def:trading-envelope`, not as separate entries.

| Legacy block | Owner | Destination | Disposition |
|---|---|---|---|
| *Algo as Layered Decision System* | `execution-trading-costs` | `def:trading-envelope` (Statement) | Merged |
| *Algorithm Layer Segmentation* | `execution-trading-costs` | `def:trading-envelope` (Statement) | Merged |
| *Benchmark Customisation* | `execution-trading-costs` | `def:trading-envelope` (Practice; examples corrected) | Rewritten |
| *Hard Mixtures Are Fragile* | `execution-trading-costs` | `def:trading-envelope` (Practice) | Merged |
| *Trading Envelope* | `execution-trading-costs` | `def:trading-envelope` (Statement; "posts passively" corrected) | Rewritten |
| *Envelope Construction Segmentation* | `execution-trading-costs` | `def:trading-envelope` (Statement, Conditions; "minimum-impact curve" unsourced) | Merged |
| *Customisation Workflow* | `execution-trading-costs` | `def:trading-envelope` (Practice) | Merged |
| *Execution Decision Loop* | `execution-trading-costs` | `def:trading-envelope` (Conditions, Pitfalls) | Merged |
| *Pre-Trade Segmentation* | `execution-trading-costs` | `meth:execution-decision-support` | Merged; portfolio coupling relocated |
| *Order-Submission Control Segmentation* | `execution-trading-costs` | `def:order-exposure-decisions` | Rewritten; unsourced levers flagged |
| *Reactive vs Proactive Execution* | `execution-trading-costs` | `def:order-exposure-decisions` | Rewritten; conflation with aggressiveness corrected |
| *Portfolio Trading Segmentation* | `execution-trading-costs` | `def:portfolio-trading` | Rewritten; basket/package distinction corrected |
| *Portfolio Insurance as Dynamic Execution* | `execution-trading-costs` | `mech:positive-feedback-hedging` | Merged |
| *Dynamic Hedging Feedback* (proposition and proof) | `execution-trading-costs` | `mech:positive-feedback-hedging` (Interpretation) | Merged; size and stability added |
| *Basket Characterisation Inputs* | `execution-trading-costs` | `def:portfolio-trading` (Conditions; reason for tight quotes corrected) | Rewritten |
| *Index Rebalance Controls* | `execution-trading-costs` | `def:portfolio-trading` (Practice) | Rewritten |
| *What-If Controls* | `execution-trading-costs` | `meth:execution-decision-support` | Merged; examples corrected |
| Table *Typical features of trading algorithms* (not a counted block) | `execution-trading-costs` | `meth:algorithm-benchmark-choice`, rebuilt from Lehalle and Laruelle's Table 3.2 with links | Rebuilt; original kept verbatim in the artefact |

### Sources, 2026-10-15

- **Lehalle and Laruelle**, 2018 World Scientific printing (text layer; printed page = PDF page − 27): sec. 3.1.1, pp. 196–197 (historical data, dark-pool probes, models with daily parameters and real-time variables); sec. 3.1.2, pp. 197–198 (components); sec. 3.1.3, pp. 198–201 (pre-trade, monitoring, performance and what-if); sec. 3.4.1, pp. 230–233 (Table 3.2, customisation, trading envelopes). Page images of pp. 198, 201, 230 (Table 3.2), 231 and 233. Slice 11's inspection of Table 3.1 was not relied on for this material.
- **Harris**, 2002 Oxford printing: chap. 18, pp. 380–389 (order submission, reactive and proactive traders, defensive strategies); chap. 23, pp. 486–491 (index funds, program trades, the firm bid/offer market); chap. 28, sec. 28.2.2, pp. 560–561 with both boxes (portfolio insurance).
- **Kissell**, `s7-kissellscience`, the copy whose copyright page says 2014 (the catalogue's date is 2013; the guide is unchanged): chap. 1, pp. 16–19 (algorithm types, basket algorithms, risk-aversion parameter), and chap. 3, p. 108 (participation-weighted price).
- **Perold (1988)** remains unread; nothing in this slice cites it.

### Algorithm checks (own, Interpretation in the entries)

- **Benchmark against policy.** VWAP and TWAP keep their two meanings (price statistic and policy) in `def:execution-benchmark`; `def:trading-envelope` describes the policies. Kissell's VWAP and TWAP policies are static day schedules; POV reacts to realised volume and need not complete, with a broker minimum rate as the completion fix; arrival-price and IS algorithms are cost–risk optimisations, IS adding adaptation; definitions and risk-aversion scales vary by broker.
- **Parent schedule against child placement.** The envelope bounds the parent order's cumulative quantity; child size, price and venue belong to the tactics (pp. 197–198).
- **Information.** Parameters are estimated about daily; $V$ in $\kappa\sigma(v/V)^\gamma$ is realised market volume, so a schedule fixed at the start can use only a forecast of it.
- **Participation denominator.** Neither source states whether a rate $\rho$ counts the order's own fills. With them, the order is $\rho/(1-\rho)$ of others' volume (25 percent at 20 percent); without, $\rho/(1+\rho)$ of the total (16.7 percent). Kissell's participation-weighted price counts own fills in its window. Checked numerically; logged as an open question.
- **Feedback.** The legacy proposition shows only the sign. If induced moves persist and retrigger the rule, the total move is $dS/(1-\lambda q')$ for dimensionless $\lambda q'<1$ (1.67 at 0.4, checked by iteration); purely temporary impact gives no amplification.
- **Portfolio-insurance sizing.** Harris's box multiplies the fall by delta; the rebalancing trade depends on the change in the hedge ratio. A Black–Scholes illustration (zero rate, 20 percent volatility, one year) gives sales of about 1.0, 1.6 and 1.8 percent of insured value per 1 percent fall for floors at 80, 90 and 100 percent.
- The spread-against-impact accounting gap from slice 11 stays open; no cost already in execution prices was added.

### Source findings and legacy corrections

- Lehalle and Laruelle's p. 197 sends the trading curve to app. A.6, which is the Harris tick model; the scheduling appendix is A.7. Figure 3.14's caption lacks its second algorithm name; the text says IS (p. 232).
- Envelope: a too-fast algorithm stops posting (not "posts passively"). Customisation examples: the would level makes an algorithm IS-like and the SOR liquidity-seeker-like; "PoV capped by urgency" and the "minimum-impact curve" are not in the source. Dark probes are supported (p. 196).
- What-if examples in the source are finishing now and switching IS to PoV; "portfolio coupling" is outside the pre-trade list.
- Harris separates the reactive–proactive continuum (search cost) from the aggressive–passive one (eagerness); the legacy principle conflated them. "Discretion range", "protection price", "pegging" and "minimum fill" are not in the passages.
- Harris treats package, basket and portfolio trading as one market; he explains tight package quotes by lower adverse selection, not diversification; his index-fund substitutes are non-index stocks, not futures or ETFs. "Portfolio transition" is only named (Kissell p. 16).
- Table 3.2: the legacy rows dropped PoV's "can be very aggressive", the VWAP/TWAP condition on unexpected volume in the order's direction and the liquidity seeker's relative-price orientation, and called VWAP/TWAP a "volume-curve schedule".

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | secs. 3.1.1–3.1.3, pp. 196–201; sec. 3.4.1, pp. 230–233 | Text layer; page images of pp. 198, 201, 230, 231, 233; envelope references (Bouchard et al., Lehalle, Guéant et al.) not consulted |
| `alpha-harris` | chap. 18, pp. 380–389; chap. 23, pp. 486–491; chap. 28, pp. 560–561 | Text layer; market facts as of 2002 |
| `s7-kissellscience` | chap. 1, pp. 16–19; chap. 3, p. 108 | Text layer; not on a route |

The five new entries and the extended `meth:algorithm-benchmark-choice` are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Execution algorithms (slice 12)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears once, and that the 17 blocks and the table (with its settings and caption) each appear once and in order. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`. The table's disposition is recorded separately above.

### Counts

`migration_status.py`: 721 → 704 legacy blocks (17 migrated). Shared 575 → 558; single-candidate 117; assigned 29. Each block was a candidate of `execution-trading-costs` and `price-impact-execution`, so each fell by 17: 45 → 28 and 27 → 10 (17 blocks, not 34). `market-structure-execution-quality` stays at 318. Entries 49 → 54 (definitions 18 → 21, methods 7 → 8, mechanisms 1 → 2). Entries listed: `execution-trading-costs` 5 → 10; `price-impact-execution` 9; `execution-market-making` 22; `market-making-lob` 13. A first draft of the overview note named `mech:bubble-crash-dynamics` under its Entries heading, which the checker counted as owned (11); reworded.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 170 pages (167 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. Rendered and inspected: PDF pp. 43 (the rebuilt Table 3.2), 45–49 (the new section) and 159 (the pruned legacy chapter, which now starts at *Transaction Cost Analysis (TCA)*). The artefact compiles on its own: 24 pages (22 before), no warnings, the same 3 underfull boxes; its last page shows the original table.

### For review

- The five new entries, the Table 3.2 extension, and ownership by the overview rather than `price-impact-execution`.
- The participation-denominator question and the portfolio-insurance sizing correction.
- The source slips in Lehalle and Laruelle (A.6 reference, Figure 3.14 caption).

## Slice 13: transaction cost analysis, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 12's pushed state (`3d93967`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 704 legacy blocks (117 single-candidate, 558 shared, 29 assigned), 54 entries, listings of 10, 9, 22 and 13, and candidate associations of 28 (`execution-trading-costs`), 10 (`price-impact-execution`) and 318 (`market-structure-execution-quality`). Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../04_transaction_cost_analysis.tex`: 25 counted blocks, including the closing sentences inside them. The file had no table, figure or text outside the blocks (checked by script). The map listed `market-structure-execution-quality` and `execution-trading-costs`. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership

Each block was read and routed on its content, not the filename or earlier slices:

- **`execution-trading-costs`** (overview): measuring, predicting and splitting execution costs and shortfall, which is the last clause of its outcome ("split realised implementation shortfall into spread, impact, timing and fees") and its checkpoint; and the block-trading blocks, whose canonical entry it already owns.
- **`market-structure-execution-quality`**: best execution, retail execution quality and broker conflicts. Its outcome names retail routing and execution quality, its checkpoint measures retail execution quality by venue type, and its readings include the Rule 605 amendments and the 2025 withdrawal of the best-execution proposal. A pathway note was opened.
- **`performance-manager-evaluation`**: four blocks evaluate investment managers, not executions (total and money-weighted returns, Jensen-style alpha, the selection and timing decomposition, smoothed returns). Neither map candidate has that outcome; this pathway's is "attribute returns, adjust for factor exposure, smoothing and survivorship". Routing outside the map candidates is a judgement **for review**. A pathway note and the canonical chapter `compendium/portfolio-construction-risk/` were opened; because that section comes first in the guide's order, later chapters are renumbered by one (labels unchanged).

| # | Legacy block | Owner | Destination | Disposition |
|---|---|---|---|---|
| 1 | *TCA* | `execution-trading-costs` | `meth:transaction-cost-analysis` | Merged |
| 2 | *Transaction Cost Component Segmentation* | `execution-trading-costs` | `def:transaction-costs` | Rewritten; glosses corrected |
| 3 | *Signed Benchmark Cost* | `execution-trading-costs` | `def:execution-benchmark` | Merged (duplication) |
| 4 | *Implementation Shortfall with Missed Quantity* | `execution-trading-costs` | `def:implementation-shortfall` (Notation) | Merged (duplication) |
| 5 | *Marginal Aggressiveness Rule* | `execution-trading-costs` | `meth:aggressiveness-tradeoff` | Rewritten |
| 6 | *Benchmark Price Segmentation* | `execution-trading-costs` | `def:execution-benchmark` | Merged (duplication) |
| 7 | *VWAP Benchmark* | `execution-trading-costs` | `def:execution-benchmark` | Merged (duplication) |
| 8 | *Performance Measurement Segmentation* | `performance-manager-evaluation` | `meth:relative-performance-evaluation` | Rewritten |
| 9 | *Risk-Adjusted Excess Return* | `performance-manager-evaluation` | `meth:relative-performance-evaluation`; TCA analogy in `meth:transaction-cost-analysis` | Rewritten; alpha definitions distinguished |
| 10 | *Benchmark Failure Modes* | `execution-trading-costs` | `meth:transaction-cost-analysis` (Pitfalls) | Merged; a synthesis, flagged |
| 11 | *Pre-, Live-, and Post-Trade Consistency* | `execution-trading-costs` | `meth:execution-decision-support` | Merged |
| 12 | *Performance Attribution Segmentation* | `execution-trading-costs` | `meth:execution-decision-support` | Merged; (A.26) relationship corrected |
| 13 | *Selection and Timing Decomposition* | `performance-manager-evaluation` | `meth:relative-performance-evaluation` | Merged (Harris's identity) |
| 14 | *TCA Uses Wider Samples Than Post-Trade Review* | `execution-trading-costs` | `meth:transaction-cost-analysis` | Merged; selection limit added |
| 15 | *TCA Estimator Quality Segmentation* | `execution-trading-costs` | `def:execution-benchmark` | Merged (duplication of Harris sec. 21.4) |
| 16 | *TCA Context Segmentation* | `execution-trading-costs` | `meth:transaction-cost-analysis` | Merged |
| 17 | *Pre-Trade Cost Prediction Variables* | `execution-trading-costs` | `meth:transaction-cost-analysis` (Conditions) | Merged; unsourced variables flagged |
| 18 | *Broker and Algo Selection* | `execution-trading-costs` | `meth:transaction-cost-analysis` | Merged; selection caveat |
| 19 | *Best Execution as Auditability* | `market-structure-execution-quality` | `def:best-execution` | Rewritten |
| 20 | *Retail Execution Quality Segmentation* | `market-structure-execution-quality` | `def:best-execution` | Merged |
| 21 | *Broker-Conflict Segmentation* | `market-structure-execution-quality` | `def:broker-agency-conflicts` | Rewritten |
| 22 | *Gaming the Measure* | `execution-trading-costs` | `def:execution-benchmark` | Merged; venue-selection gloss flagged |
| 23 | *Smooth Returns Are Not Safer Returns* | `performance-manager-evaluation` | `meth:relative-performance-evaluation` (Conditions) | Merged |
| 24 | *Block Motive Audit* | `execution-trading-costs` | `def:block-trade` | Merged |
| 25 | *Block Trade Reporting Trade-Off* | `execution-trading-costs` | `def:block-trade` | Merged; argument corrected |

Existing entries compared and kept: `def:spread-measures` and `res:spread-component-identification` (owned by `execution-market-making`) hold the effective and realised spreads; they are cross-referenced, and no spread measure was duplicated. `def:price-impact` and the estimation methods stay with `price-impact-execution`.

### Sources, 2026-10-15

- **Harris**, 2002 Oxford printing (text layer; printed page = PDF − 13): chap. 7, pp. 151–167 (principal–agent problem, best execution, dual trading, preferencing, soft dollars, dishonest brokers); chap. 15, pp. 328–331 (block dealers, trade reporting, motive audit, Table 15-2); chap. 21, pp. 420–423, 432 and 435–441 (components, signed cost, marginal rule, prediction), reusing slice 11's pp. 424–437; chap. 22, pp. 442–450 and 469–470 (performance evaluation, smoothing); chap. 25, pp. 514–519 (best execution practice, Rules 11Ac1-5 and 11Ac1-6). The marginal-aggressiveness passage (pp. 437–438) was read in this slice, not taken from the earlier lead.
- **Kissell**, `s7-kissellscience`, the inspected copy whose copyright page says 2014 (the catalogue's 2013 date is unchanged): chap. 3, pp. 87–96 (best execution, ten components, TCA phases, cost against performance) and pp. 110–113 (index-adjusted cost and z-scores; page image of p. 112).
- **Lehalle and Laruelle**, 2018 printing: sec. 3.1.3, pp. 200–203 (performance indicators, pre-, live- and post-trade compatibility, TCA); app. A, sec. A.7.2, pp. 278–279, with the page image of p. 279 for (A.26), the passage the average-price decomposition cites.
- **Perold** remains unread; the slice relies on it only through Kissell's and Harris's attributions, as before.

### Accounting checks (own, Interpretation in the entries)

- **Legacy shortfall formula.** $\mathrm{IS}=dq(\bar p-p_0)+d(Q-q)(p_T-p_0)+$ explicit costs equals Perold's form with $S=dQ$; slice 11's example gives 3,960 for the buy and the sell.
- **Spread and drift split.** With pre-fill midpoints $m_j$: delay $S(P_0-P_d)$ + half-spread paid $\sum s_j(p_j-m_j)$ + midpoint drift $\sum s_j(m_j-P_0)$ + opportunity $(S-\sum s_j)(P_n-P_0)$ + fees. Buy and sell examples with partial fills reconcile exactly: 1,000 + 300 + 600 + 2,000 + 60 = 3,960. It is an accounting identity; the drift is not causal impact.
- **Lehalle and Laruelle's decomposition.** (A.26) is $\mathbb E(W)+\lambda\operatorname{Var}(W)$, an ex-ante objective whose third term is a variance penalty. Its realised counterpart $W=v^\star S_0+\sum x_n\sigma_n\xi_n+\kappa\sum\sigma_nv_n^{\gamma+1}/V_n^\gamma$ holds exactly inside the model (checked by simulation, book's timing); on data the impact term is a model value and the move a residual. The refined decomposition (planned price, unexpected moves, trading efficiency) has no formula, so its additivity cannot be checked.
- **Kissell's index adjustment.** Eq. (3.22) leaves the index term unsigned; for a sale 50 bp below arrival while the index fell 50 bp with $\hat\beta=1$, it gives 100 bp of adjusted cost instead of 0. The side factor is needed.
- **Performance identity.** Harris's $r^p=(r^p-\beta r^m)+(\beta r^m-r^m)+r^m$ checked. His realised alpha differs from Jensen's by $(1-\beta)r^f$ (−0.9 points at $\beta=1.3$, $r^f=3\%$).
- **Examples.** Harris's cotton example (\$137,500) recomputed.
- **Marginal rule.** Harris states it as advice: objective, choice variable and smoothness assumptions are Interpretation; there is no proof of optimality in the source.
- **Evaluation populations.** TCA averages by order or by value depend on which orders each broker received; routing tables from unadjusted averages confound selection with skill.

### The spread-versus-impact gap

Partly addressed, not closed. The split above gives spread (half-spread paid against pre-fill midpoints), timing before arrival (delay), opportunity and fees with explicit references, and reconciles to the total without double-counting spreads already in fill prices. The rest, midpoint drift, mixes own impact with market and other traders' moves. Kissell says impact is an unobservable counterfactual (pp. 91–92), and a market-adjusted residual is impact only under the model used. The checkpoint's impact component is therefore still open, as is the effect of the tick, fee and reporting rules in force.

### Source findings and legacy corrections

- Harris: adverse selection is a cause of the spread, not a separate implicit cost; delay is Kissell's investment-related cost. Borrow charges, the venue variables in cost prediction, "benchmark change" and "past behaviour" in the motive audit, and venue selection as gaming are not in the passages.
- Best execution: the legacy "best auditable outcome given objective, limit, urgency, venues and information risk" merges Harris's auditability standard with Kissell's process definition. Rules 11Ac1-5 and 11Ac1-6 are as of 2002 (now Rules 605 and 606, amended 2024; the pathway's readings on them are unread).
- Broker conflicts: Harris treats commission recapture as a sponsor's tool, not a broker incentive; payment for order flow resembles but is generally not a kickback.
- Block reporting: Harris argues that timely reporting hurts facilitating dealers; the legacy claim that delayed reporting helps informed initiators exploit stale prices is not his.
- Performance: the legacy "money-weighted IRR, useful when the investor controls flows" and "trade-weighted" measures are not Harris's; his IRR is approximately time- and value-weighted.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chaps. 7, 15, 21, 22, 25 as above | Text layer; rules and figures as of 2002 |
| `s7-kissellscience` | chap. 3, pp. 87–96, 110–113 | Text layer; page image of p. 112; not on a route |
| `alpha-laruelle` | pp. 200–203; app. A.7.2, pp. 278–279 | Text layer; page image of p. 279 |
| `wide-perold-shortfall`, `ex-sec-rule605-2024`, `ex-sec-withdrawal-2025`, `wide-getmansky-lo-makarov` | none | Not read |

The six new entries and the four extended entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Transaction cost analysis (slice 13)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears once, that all 25 blocks appear once and in order, and that no text lies outside them. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`.

### Counts

`migration_status.py`: 704 → 679 legacy blocks (25 migrated). Shared 558 → 533; single-candidate 117; assigned 29. Each block was a candidate of `execution-trading-costs` and `market-structure-execution-quality`, so each fell by 25: 28 → 3 and 318 → 293 (25 blocks, not 50); `price-impact-execution` stays at 10. Entries 54 → 60 (definitions 21 → 24, methods 8 → 11). Entries listed: `execution-trading-costs` 10 → 13; `market-structure-execution-quality` 0 → 2 (new note); `performance-manager-evaluation` 0 → 1 (new note); `price-impact-execution` 9; `execution-market-making` 22; `market-making-lob` 13.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 174 pages (170 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` warning. A first build had one overfull box (a See-also line with an unbreakable key) and one underfull line in the chapter opener, both from this slice and fixed. Rendered and inspected: PDF p. 7 (the new Chapter 1), pp. 47 and 52–55 (the block-trade extension, the new sections) and p. 166 (the pruned legacy chapter, which now starts at *Smart Order Routing*). The artefact compiles on its own: 27 pages (24 before), no warnings, the same 3 underfull boxes.

### For review

- Routing four blocks to `performance-manager-evaluation`, outside the map candidates, and opening its chapter.
- The three best-execution and broker blocks given to `market-structure-execution-quality`.
- The accounting split and its limits, the (A.26) correction, the Kissell side correction.

## Slice 14: smart order routing, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 13's pushed state (`b699ed2`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 679 legacy blocks (117 single-candidate, 533 shared, 29 assigned), 60 entries, listings of 13, 2, 1, 9, 22 and 13, and candidate associations of 3, 293 and 10. The file's map row names one pathway, so its 15 blocks were among the 117 single-candidate (`market-structure-execution-quality` exclusive: 21), not the shared count. Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../05_smart_order_routing.tex`: 15 counted blocks (the proposition's proof is inside its block), the uncounted table *Passive routing criteria can rank the same venues differently* with its settings and caption, and the sentences inside the blocks. There was no text outside the blocks and the table. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership

The map's single candidate fits: the pathway's outcome is how fragmentation, dark trading and fees affect execution quality, and the blocks are about routing child orders across fragmented venues, the effect of fees on venue choice, and best-execution regimes and broker conflicts. All 15 are owned by `market-structure-execution-quality`; no exception was needed. Routing stays distinct from scheduling (`mod:almgren-chriss-execution`) and from the algorithm's layers (`def:trading-envelope`, which names routers as tactics), both owned by `execution-trading-costs` and cross-referenced; exposure choices stay in `def:order-exposure-decisions`. Two blocks duplicate this pathway's existing entries and were merged.

| # | Legacy block | Destination | Disposition |
|---|---|---|---|
| 1 | *Execution-Side SOR* | `def:smart-order-routing` | Merged |
| 2 | *Marketable Price Across Venues* | `def:smart-order-routing` | Merged |
| 3 | *Routing Logic Segmentation* | `def:smart-order-routing` | Merged; a synthesis, flagged |
| 4 | *Child-Order Routing Loop* | `def:smart-order-routing` | Merged; a synthesis, flagged |
| 5 | *Best Execution Differs by Regime* | `def:best-execution` | Merged; Rule 611 verified, European regime dated 2018 |
| 6 | *Displayed Best Price Is Not Enough* | `def:smart-order-routing` | Merged |
| 7 | *Active Sweep Segmentation* | `def:smart-order-routing` | Merged; "local best price" corrected |
| 8 | *Fee-Adjusted Price Priority* | `res:fee-adjusted-venue-choice` | Rewritten; sell side and per-share fees added |
| 9 | *Order Preferencing* | `def:broker-agency-conflicts` | Merged (duplication) |
| 10 | *Payment-for-Order-Flow Routing Conflict* (proposition and proof) | `def:broker-agency-conflicts` | Merged as Interpretation |
| 11 | *Latency Makes Liquidity Probabilistic* | `def:smart-order-routing` | Merged |
| 12 | *Liquidity Seeking Objective* | `def:smart-order-routing` | Merged |
| 13 | *Passive Posting Segmentation* | `meth:passive-order-split` | Merged |
| 14 | *Minimum Resting-Time Split* | `meth:passive-order-split` | Rewritten; non-negativity corrected |
| 15 | *Liquidity-Seeker Build* | `def:smart-order-routing` | Merged |
| — | Table *Passive routing criteria…* (not counted) | `meth:passive-order-split` | Rebuilt from Lehalle and Laruelle's Table 3.6 with venue names; original kept verbatim |

### Sources, 2026-10-15

- **Lehalle and Laruelle**, 2018 World Scientific printing (text layer; printed page = PDF − 27): sec. 3.4.2, pp. 233–244, with page images of pp. 235 (Table 3.3), 236 (the broker outcomes and the fee inequality), 240 (Table 3.4, eq. (3.3)) and 241 (Table 3.5, eq. (3.4) and footnote 16). Pp. 237–239 and 242 read in the text layer.
- **17 CFR 242.611**, the order protection rule: text retrieved on 15 October 2026 through the eCFR versioner API, point-in-time 13 October 2026; versions listed since 2016, latest 14 June 2024; citations 70 FR 37620 (2005), 83 FR 58429 (2018), 86 FR 18811 (2021), 89 FR 26616 (2024). The effective and compliance dates of the 2024 amendment were not checked. This verifies Rule 611 only, not Rules 605, 606 or 610, FINRA's best-execution rule, or any European rule.
- **MiFID II**: the consolidated text could not be retrieved (EUR-Lex returned an empty response), so the European regime is stated only as Lehalle and Laruelle describe it in 2018.
- Harris's preferencing passages (chap. 7, pp. 161–162) were reused from slice 13. `ex-sec-rule605-2024`, `ex-sec-withdrawal-2025`, `ex-sec-tick-access-2024` and Perold remain unread.

### Regulatory claims: historical against verified

- **Verified as of 15 October 2026:** Rule 611 obliges a *trading center* to keep and enforce written policies reasonably designed to prevent trade-throughs of protected quotations in NMS stocks, and to surveil them, with nine exceptions (system failures, non-regular-way trades, single-priced opening, reopening and closing transactions, crossed protected quotations, intermarket sweep orders, orders not priced off the quote, quotes inferior within the prior second, stopped customer orders). It is quote protection by venues, not a broker's best-execution duty or a reporting obligation, and it does not require venues to reroute; an intermarket sweep order lets the router take protected quotes itself.
- **Historical (2018, not verified as current):** Lehalle and Laruelle's statements that U.S. clearing and settlement fees must be equal across venues, and that European executing brokers choose their consolidation and must disclose a best-execution policy.
- **Historical (2002):** Harris's Rules 11Ac1-5 and 11Ac1-6, unchanged from slice 13.

### Routing and fee-accounting checks (own, Interpretation in the entries)

- **Three-broker example.** Sweeping Table 3.3's cheapest levels: B1 (Euronext and Chi-X, split) 101.15 and B3 (all three, split) 100.75, as printed. The best single venue for 500 shares is Chi-X at 102.05 (Euronext 102.10, Turquoise 102.20), against the printed 102.50: a likely misprint. B1's bracketed quantities add to 600 and list depth, not fills.
- **Fee threshold.** Exactly $\delta<\phi/(1+f-\phi)$ for a buy (acquisition cost) and $\delta<\phi/(1-f+\phi)$ for a sell (proceeds), both about $\phi$; illustrative $P=100$, $f=3$ bp, $\phi=1$ bp give thresholds 0.99980 and 1.00020 bp, and $\delta=0.99$ and 1.01 bp flip the choice on both sides. With per-share fees the condition is $P\delta<c-c'$. Fees are proportional and paid by the taker; rebates are negative fees; both quotes are assumed contemporaneous, executable for the whole size and taken; the spread is in the prices and not added again. A favourable fee-adjusted quote does not establish a fill or best execution.
- **Passive split.** The book prints eq. (3.4) as $(D-\sum Q_n)/\sum r_n$; its footnote and Table 3.5 need $D+\sum Q_n$ (62.5 s, against −12.5 s). Table 3.5 recomputed (35/42.5/22.5 percent; 175/212.5/112.5 shares). A venue with $f_n<0$ must be dropped and $\tau^\star$ recomputed: setting it to zero leaves fractions not summing to one (checked on an illustrative case). Equal finishing times minimise the completion time of the whole order, not an average. The model treats queues and rates as fixed.
- **Latency.** Displayed depth is not assumed to remain while a sequence of child orders is routed; the book's mirrored-liquidity example is kept as a scenario, not a measured effect.
- **Routing conflict.** The legacy proposition is a condition under which client- and broker-optimal routing differ; it is not evidence of conflicted routing.
- The accounting split of slice 13 and its limit (midpoint drift is not automatically own impact) are unchanged.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | sec. 3.4.2, pp. 233–244 | Text layer; page images of pp. 235, 236, 240, 241; Laruelle et al. (2011, 2013) not consulted |
| 17 CFR 242.611 | full section, eCFR point-in-time 13 Oct. 2026 | Effective and compliance dates of the 2024 amendment not checked |
| MiFID II | none | Not retrieved; European regime dated 2018 |

The three new entries and the two extended ones are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Smart order routing (slice 14)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears once, that the 15 blocks and the table (with its caption) each appear once and in order, and that no text lies outside them. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed.

### Counts

`migration_status.py`: 679 → 664 legacy blocks (15 migrated). Single-candidate 117 → 102; shared 533 → 533 (unchanged, as these blocks were never shared); assigned 29. `market-structure-execution-quality`: exclusive 21 → 6, shared candidates 293 (unchanged), listed entries 2 → 5. Entries 60 → 63 (definitions 24 → 25, methods 11 → 12, results 12 → 13). Other listings unchanged: `execution-trading-costs` 13, `performance-manager-evaluation` 1, `price-impact-execution` 9, `execution-market-making` 22, `market-making-lob` 13.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 175 pages (174 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` warning. A first build had one overfull line (a long path), fixed. Rendered and inspected: PDF pp. 55 (best execution with Rule 611), 56–58 (the new section and the rebuilt table) and 168 (the pruned legacy chapter, which now starts at *High-Frequency Trading Strategies*). The artefact compiles on its own: 28 pages (27 before), no warnings, the same 3 underfull boxes.

### For review

- The three new entries; the merges into `def:best-execution` and `def:broker-agency-conflicts`.
- The Rule 611 statement and its scope; the European regime left as of 2018.
- The eq. (3.4) and B2 misprints, the fee thresholds and the split's non-negativity correction.

## Slice 15: high-frequency trading strategies, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 14's pushed state (`4fb411c`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 664 legacy blocks (102 single-candidate, 533 shared, 29 assigned), 63 entries, listings of 13, 5, 1, 9, 22 and 13, and `market-structure-execution-quality` with 6 exclusive blocks and 293 shared candidate associations. Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../06_high_frequency_trading_strategies.tex`: 3 counted blocks, including the closing sentence inside the taxonomy. The file had no table, figure, caption or text outside the blocks other than its `% migrate-to:` line and subsection heading (checked by script). The map listed `execution-trading-costs` and `market-structure-execution-quality`. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership and the routing exception

All three blocks belong to `hft-market-design`, which is not among the file's map candidates. The blocks classify HFT strategies, claim that speed edges decay as speed diffuses, and say how HFT should be judged by other traders' costs. That pathway's outcome is to "evaluate how speed, latency races and fast arbitrage affect liquidity, price discovery and the costs borne by slower traders", and two of its required readings are the theory and evidence the blocks need (`wide-budish-cramton-shim`, `wide-menkveld-hft-review`). The overview's outcome (planning and costing an order) and `market-structure-execution-quality`'s (rules, fees and execution quality) touch the material only through routing and fees, which already have entries there and are cross-referenced. The pathway sits in the section `execution-market-making`, so the entries are in `compendium/execution-market-making/high-frequency-trading.tex`, and a pathway note was opened. The routing outside the map is a judgement **for review**, as with slice 13's routing to `performance-manager-evaluation`. The fifteen blocks already assigned to `hft-market-design` were not touched.

| # | Legacy block | Owner | Destination | Disposition |
|---|---|---|---|---|
| 1 | *HFT Strategy Segmentation* (taxonomy, with its closing sentence) | `hft-market-design` | `def:hft-strategies` | Rewritten against the SEC's four types; statistical and latency arbitrage remapped, liquidity detection reclassified as a tool, momentum ignition added |
| 2 | *HFT Edge Decays With Diffusion* (principle) | `hft-market-design` | `res:latency-arbitrage-arms-race` (Pitfalls) | Rewritten; premise corrected (the prize is not competed away, rents are dissipated into speed); "lower costs" supported (n. 27); inventory control, better models and privileged order flow unsupported, kept in the artefact only |
| 3 | *Message Profit Is Not Market Quality* (caveat) | `hft-market-design` | `res:hft-spread-investor-cost` (Practice, Pitfalls) | Merged; the evaluation criteria kept as the legacy note's own, its effects stated as possibilities and open questions, not findings |

### Overlaps resolved, from content

- `def:order-anticipation` (Harris, owned by `execution-market-making`) keeps order anticipation, front running and quote matching; the new definition only places order anticipation among the SEC's HFT strategy types and adds the release's distinction between pinging for liquidity and pinging to trade ahead. A See-also link was added to `def:order-anticipation`.
- The market-making entries (`mod:avellaneda-stoikov`, `meth:dealer-quote-adjustment`, `mod:glosten-milgrom`) and `def:arbitrage` are cross-referenced for the economics of passive market making and arbitrage; nothing was restated.
- `def:smart-order-routing` keeps latency, mirrored liquidity and liquidity seeking by routers; it gained a See-also link. `res:fee-adjusted-venue-choice` and `meth:passive-order-split` are not referenced and are unchanged. `def:order-exposure-decisions`, `def:trading-envelope`, `def:best-execution` and `def:broker-agency-conflicts` were compared and are unaffected: the blocks make no routing, exposure, best-execution or broker claims.
- `res:latency-arbitrage-arms-race` is distinct from the legacy fee-and-race model in `05_.../05_latency_and_queue_competition.tex` (assigned here, unmigrated, source not identified), which models maker–taker fees and speed investment differently.

### Sources, 2026-10-15

- **SEC, Concept Release on Equity Market Structure**, Release 34-61358, dated 14 January 2010 (`sec-concept-release-2010`, added to `front/sources.tex`): official PDF from sec.gov, 74 pages, text layer; sec. IV.B, pp. 45–58, with nn. 67–75. A request for comment, not a rule, and dated: no current U.S. or EU rule on HFT was needed or checked.
- **Budish, Cramton and Shim** (`wide-budish-cramton-shim`), the published *QJE* 130(4) version, open access, hosted by the University of Maryland economics department: text layer of pp. 1547–1556 and 1576–1592; page images of pp. 1589–1590 (eqs. (5)–(7)). Secs. II–V (data and empirical analysis) and VII–VIII (batch auctions) not read; the ES–SPY evidence is taken from the introduction's summary.
- **Lehalle and Laruelle**, 2018 World Scientific printing (text layer; printed page = PDF − 27): sec. 2.3.3–2.4.3, pp. 158–169, with page images of pp. 164, 165, 166 and 168.
- Harris's order-anticipation passages (chap. 11) were not re-read; `def:order-anticipation` is unchanged except for its See-also line. The SEC quotes Harris's 2003 printing (pp. 245, 251).
- Not available or not read: `wide-menkveld-hft-review` (Annual Reviews, subscriber only; no author copy found), `wide-hendershott-jones-menkveld`, `wide-brogaard-hft-discovery`, `exp-aquilina-budish-oneill-races`, `wide-baron-hft-competition` and the pathway's other readings. Perold remains unread; nothing here cites him.

### Mechanism, evidence and interpretation kept apart

- **Speed against strategy.** Speed, co-location and data feeds are tools; passive market making, arbitrage, stale-quote trading, order anticipation and momentum ignition are different economic mechanisms with different effects (`def:hft-strategies`, Conditions, Interpretation). The SEC's types organise a 2010 request for comment and are not used as a universal classification; no strategy label is treated as illegal.
- **Theory.** The sniping equilibrium and the dissipation of rents are results of a deliberately extreme model (perfectly correlated public signal, costless liquidation, no inventory or information costs, continuous prices).
- **Evidence.** The ES–SPY durations, profits and prize are the authors' measurements for one pair, 2005–2011, read in their summary.
- **Author's interpretation.** Lehalle and Laruelle's cost model attributes the 2007–2011 Euronext Paris spread change to HFT with an assumed 40 percent share; their coverage account is a reading of descriptive statistics.

### Mathematical checks (own, Interpretation in the entries)

- **BCS eq. (7).** Adding (5) and $N-1$ times (6) gives $\lambda_{\mathrm{invest}}s^*/2=N^*c_{\mathrm{speed}}$; subtracting gives eq. (3). Numerically, with $J$ uniform on $[0,1]$, $\lambda_{\mathrm{jump}}=2$, $\lambda_{\mathrm{invest}}=10$ and $c_{\mathrm{speed}}=0.05$: $s^*=0.1678$, prize = investor cost = 0.8392, $N^*=16.78$, and both the liquidity provider's and a sniper's profit before speed costs equal $c_{\mathrm{speed}}$. A simulated race with $N=4$ gives the sniped share 0.750, matching $(N-1)/N$. Units: rates per unit time, $s$ and $J$ in price units.
- **Lehalle and Laruelle.** From $\psi_B=5.41$, $\psi_N=4.73$ bp and $q=0.4$: $\psi_{\mathrm{HFT}}=3.71$ bp; $\mathbb E[C]$ is 2.705, 3.2615, 3.6325 and 4.56 bp at $r=0$, 0.3, 0.5 and 1, matching Figure 2.24's endpoints and markers. The rise from $r=0.3$ to 0.5 is 0.371 bp, not the text's "approximately 0.5bp". $C$ is measured from the trader's own resting quote (Figure 2.21), not against the midpoint.
- **Timing and information.** In BCS all fast firms see the jump at the same time and the outcome is decided by serial processing; investors see $y$ later. The cost model is a single-order, ex ante expectation with $r$ fixed.

### Source findings and legacy corrections

- The legacy taxonomy's five categories are its own: the SEC's arbitrage and directional types split "statistical arbitrage"; "latency arbitrage" is the release's structural stale-price example and its cross-venue arbitrage question; "liquidity detection" is a tool (pinging) used both in ordinary search and in order anticipation; momentum ignition was missing.
- "Edge decays with diffusion" is contradicted by BCS: arbitrage durations fell from 97 to 7 ms while profit per opportunity stayed about constant, and in the model the prize does not depend on speed or its cost. What decays is a firm's relative lead and, at the margin, its profit net of speed costs.
- Lehalle and Laruelle overstate their own cost rise (0.5 against 0.37 bp) and report HFT shares of trades as hearsay; the SEC's 50 percent-plus volume share comes from press reports.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `sec-concept-release-2010` | sec. IV.B, pp. 45–58 | Text layer; a 2010 request for comment; no later SEC action checked |
| `wide-budish-cramton-shim` | pp. 1547–1556, 1576–1592 | Text layer; page images of pp. 1589–1590; secs. II–V and VII–VIII not read |
| `alpha-laruelle` | pp. 158–169 | Text layer; page images of pp. 164–166 and 168 |
| `wide-menkveld-hft-review` and the pathway's other readings | none | Not available or not read |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *High-frequency trading strategies (slice 15)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged (its first 128,718 characters, everything before `\end{document}`, are identical), that the file body appears once, that the three blocks appear once each and in order, and that nothing but the `% migrate-to:` line and the subsection heading lay outside them. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`.

### Counts

`migration_status.py`: 664 → 661 legacy blocks (3 migrated). Shared 533 → 530; single-candidate 102; assigned 29. Each block was a candidate of `execution-trading-costs` and `market-structure-execution-quality`, so each fell by 3: 3 → 0 and 293 → 290 (3 blocks, not 6); `market-structure-execution-quality` keeps 6 exclusive and 3 assigned. Entries 63 → 66 (definitions 25 → 26, results 13 → 15). Entries listed: `hft-market-design` 0 → 3 (new note, whose cross-references are under *Related entries owned elsewhere*, not the Entries heading); unchanged: `execution-trading-costs` 13, `market-structure-execution-quality` 5, `performance-manager-evaluation` 1, `price-impact-execution` 9, `execution-market-making` 22, `market-making-lob` 13. `hft-market-design` keeps 15 assigned and 7 shared blocks.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 178 pages (175 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 40–44 (the new section 2.10) and 172 (the pruned legacy chapter, which now starts at *Reinforcement Learning and ML in Execution*). The artefact compiles on its own: 28 pages (unchanged count), no warnings, the same 3 underfull boxes. Tests: 14 passed.

### For review

- Routing all three blocks to `hft-market-design`, outside the map candidates, and opening its note and topic file.
- The three new entries; the reading of the SEC's types as an organising device, not a classification.
- The correction to the "edge decays" principle and the 0.37 bp correction to Lehalle and Laruelle.

## Slice 16: reinforcement learning and ML in execution, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 15's pushed state (`60753ff`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 661 legacy blocks (530 shared, 102 single-candidate, 29 assigned), 66 entries, 0 problems. Migration and source checking, not study.

### Slice-15 correction

`res:latency-arbitrage-arms-race` said that one firm quotes $y\pm s/2$. Proposition 1(i) (printed p. 1583, rechecked) says that exactly one unit is offered at each of $y-s/2$ and $y+s/2$, and that the two quotes may belong to one trading firm or to two distinct firms; the authors assign the liquidity-provider role to one firm for simplicity, with economically equivalent equilibria in which it rotates or is random (pp. 1579–1580), and the sniping probability is Proposition 1(iii). The entry, its status line and the reading note `wide-budish-cramton-shim` were reworded; eqs. (3) and (7) are unchanged.

### Scope

The whole of `execution-trading-costs/01_.../07_reinforcement_learning_and_ml_in_execution.tex`: 4 counted blocks. Nothing lay outside them but the `% migrate-to:` line and the subsection heading (checked by script). The map listed `reinforcement-learning-trading` alone. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted; `08_production_considerations.tex` was not touched.

### Ownership

`reinforcement-learning-trading` owns all four blocks. Its outcome is to formulate an execution problem as an MDP, train a policy against a validated simulator and compare it with the control-theoretic benchmark, and its checkpoint compares an RL execution policy with Almgren–Chriss. The blocks set out such a benchmark (a stochastic-control execution model with order flow) and contrast control with learning. The pathway is in the section `ml-alternative-data`, which comes before the execution sections in the guide's order, so the entry opened the canonical chapter `compendium/ml-alternative-data/` (Chapter 1; later chapters are renumbered by one, labels unchanged) and a pathway note. `price-impact-execution` and `stochastic-calculus-control` could also claim a continuous-time execution model; neither is a map candidate, and the entry cross-references `mod:almgren-chriss-execution` (owned by `execution-trading-costs`) without restating it. Ownership is **for review**.

| # | Legacy block | Owner | Destination | Disposition |
|---|---|---|---|---|
| 1 | *Stochastic-Control Execution View* (model) | `reinforcement-learning-trading` | `mod:cartea-jaimungal-execution` (Statement, Notation) | Merged; "value function" corrected to a fixed policy's reward |
| 2 | *Cartea-Jaimungal State Dynamics* (model) | `reinforcement-learning-trading` | `mod:cartea-jaimungal-execution` (Statement, Notation, Conditions) | Merged; units, signs and constraints added; attribution qualified (Lehalle and Laruelle's account) |
| 3 | *Value Function Intuition* (principle) | `reinforcement-learning-trading` | `mod:cartea-jaimungal-execution` (Practice) | Merged; qualified by own numerical paths ($A$ governs completion, $\kappa$ also leaves residual) |
| 4 | *Control vs Learning* (taxonomy) | `reinforcement-learning-trading` | `mod:cartea-jaimungal-execution` (Practice, Pitfalls); backlog stub `meth:hybrid-control-learning-execution` | Control and RL items merged from Hambly, Xu and Yang, with simulator and historical data separated; the hybrid item unsupported, kept in the artefact and stubbed |

One entry, as planned: objective, dynamics, HJB and the supported intuition together, without the full closed form or an RL implementation.

### Sources, 2026-10-15

- **Lehalle and Laruelle**, 2018 World Scientific printing (local copy; printed page = PDF − 27): app. A, sec. A.7.3, pp. 281–284, text layer and page images of all four pages; p. 280 for context (Figure A.11).
- **Hambly, Xu and Yang** (`wide-hambly-xu-yang`), arXiv 2112.04553v4 (28 February 2023), downloaded with a generic request header: sec. 1, p. 2; sec. 2, pp. 3–4; sec. 2.2, p. 7; sec. 4.2, pp. 32–35 (page images of pp. 32–33); sec. 5, p. 49. The journal version (*Mathematical Finance* 33(3), 2023) was not checked.
- **Not consulted:** Cartea and Jaimungal's papers and `crypto-cartea` (no passage of it was needed for the claims kept); the execution studies the survey reports (Hendricks and Wilcox; Ning, Lin and Jaimungal, `w2-ning-ddqn-execution`); `wide-kolm-ritter-rl` and the pathway's other readings.

### Mathematical checks (own, Interpretation in the entry; script `notes/artefacts/reinforcement-learning-trading/cartea_jaimungal_checks.py`)

- **min against sup.** Proposition 6 writes $H^*:=\min_\nu H(\nu)$ for a value it calls maximising and solves with a $\sup$; the value is $\sup_\nu H_t(\nu)$, distinct from $H_t(\nu)$, the reward of a fixed policy.
- **Half-spread.** The terminal condition $x+q(S-\psi/2)-Aq^2$ charges the half-spread on residual inventory; the printed objective's $Q_T(S_T-AQ_T)$ does not. The ansatz and $h$-equations follow the terminal condition, so the consistent objective has $Q_T(S_T-\psi/2-AQ_T)$; the half-spread is then paid on every share and leaves the control unchanged (for one-directional selling). With the printed objective the first-order condition would gain $-\psi/(4\kappa)$, an incentive to delay.
- **Inventory term.** $dQ=-\nu\,dt$ gives $-\nu\partial_qH$ in the generator; the book prints $-\partial_qH$. Substituting $H=x+q(S-\psi/2)+h$ with $-\nu\partial_qH$ reproduces the book's p. 283 equation exactly (difference ~1e-16 at random points).
- **Notation.** "bid–ask spread $\phi$" (p. 282) for $\psi$; $k$ for $\kappa$; $b_t$ against $b$; terminal conditions for $h_0,h_1$ printed at $t$.
- **Closed forms.** The printed $h_2=-\xi-b/2$ with the printed $\xi$ and $\zeta$ gives $h_2(T)=A-b$ (0.498 at $A=0.5$, $b=0.002$), not $-A$; the solution of the Riccati equation is $\xi=\sqrt{\kappa\phi}(1+\zeta e^{-2\gamma(T-t)})/(1-\zeta e^{-2\gamma(T-t)})$, $\zeta=(A-b/2-\sqrt{\kappa\phi})/(A-b/2+\sqrt{\kappa\phi})$, matching direct integration ($h_2(0)=-0.011141$). The boxed $h_1$ "when $b=0$" lacks the factor $b$; $h_1=b\int_t^Te^{-\int\xi/\kappa}\mathbb E[\mu_s]ds$ matches the ODE (0.000303).
- **Assumptions stated.** Observed $S,\mu,Q,X$; Markov flow unaffected by the trader; constant coefficients; unconstrained $\nu$ (no sign or inventory constraint); finite $A$ is a penalty, not mandatory completion; $\phi\int Q^2$ equals a mean–variance penalty $\lambda\sigma^2\int Q^2$ only for deterministic schedules. Units and impact signs are in the entry.
- **Benchmark limit.** With $\mu\equiv0$ and $A\to\infty$, $Q_t=Q_0\sinh(\gamma(T-t))/\sinh(\gamma T)$, $\gamma=\sqrt{\phi/\kappa}$, the continuous Almgren–Chriss schedule (matched to four decimals).
- **Parameter intuition.** Base $\kappa=0.01$, $\phi=0.001$, $A=0.5$, $T=Q_0=1$: inventory at $T/2$ 0.503 and residual 1.9 percent; tenfold $\phi$ 0.451 and 1.7 percent; tenfold $A$ 0.495 and 0.2 percent; tenfold $\kappa$ 0.582 and 16.6 percent.

### Source findings and legacy corrections

- The legacy blocks copy the appendix, including its objective without the half-spread at $T$; they call $H_t(\nu)$ a value function and attribute the dynamics to Cartea and Jaimungal directly.
- "Larger $\phi$ or $A$ pushes faster liquidation; stronger $\kappa$ smoother trading" holds under the model for $\phi$ (front-loading) and $\kappa$, but $A$ mainly governs completion near $T$, and a larger $\kappa$ with finite $A$ also leaves more unsold.
- Hambly, Xu and Yang support the control and RL items (model needed against learning from interaction; model-based against model-free) but not "learn … from simulated or historical interaction" as one thing: they flag data scarcity and non-stationarity and call for simulators (p. 49), and replaying history does not show the response to one's own orders. The hybrid item (control for constraints, ML for forecasts, fills and regimes) is not in the passages; the survey reports only a combination of Almgren–Chriss with Q-learning (p. 34).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | app. A.7.3, pp. 281–284 | Text layer and page images; Cartea and Jaimungal's originals not consulted |
| `wide-hambly-xu-yang` | pp. 2–4, 7, 32–35, 49 | arXiv v4, not the journal version; the studies it reports not checked |
| `crypto-cartea`, Cartea–Jaimungal papers, `wide-kolm-ritter-rl`, other readings | none | Not consulted or not read |

The new entry is *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/reinforcement-learning-trading/derivations.tex` (compiles on its own, 1 page), with only the subsection unnumbered; a script confirmed the body appears once and the four blocks once each, in order, with nothing else outside them. The existing artefact `notes/artefacts/market-making-lob/derivations.tex` is unchanged (`git diff` empty). `08_production_considerations.tex` is byte-identical; only the `\input` line was removed from `00_overview.tex`.

### Counts

`migration_status.py`: 661 → 657 legacy blocks (4 migrated) = 530 shared + 98 single-candidate (102 − 4) + 29 assigned. `reinforcement-learning-trading`: exclusive 4 → 0, listed entries 0 → 1, backlog stubs 0 → 1. Entries 66 → 67 (models 8 → 9). Other listings unchanged: `execution-trading-costs` 13, `market-structure-execution-quality` 5, `performance-manager-evaluation` 1, `price-impact-execution` 9, `execution-market-making` 22, `market-making-lob` 13, `hft-market-design` 3.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 181 pages (178 before); no LaTeX warnings, no undefined references; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had one overfull line in the entry's See-also (an unbreakable key), reworded. Rendered and inspected: PDF pp. 7–9 (the new Chapter 1), 10 (Chapter 2, renumbered), 45 (the corrected Budish–Cramton–Shim paragraph) and 175 (the pruned legacy chapter, which now starts at *Production Considerations*). The new artefact compiles with no warnings or bad boxes. Tests: 14 passed.

### For review

- Ownership by `reinforcement-learning-trading` and the new chapter `ml-alternative-data/`.
- The appendix corrections and the qualified parameter intuition; whether to check the model against Cartea and Jaimungal's originals.
- The backlog stub for hybrid execution.

## Slice 16 follow-up: mathematical corrections to `mod:cartea-jaimungal-execution`, 15 October 2026

A bounded correction to slice 16 (`6d04e52`), run from that pushed state (657 legacy blocks = 530 shared + 98 single-candidate + 29 assigned, 67 entries, checker clean, guide `343d145`). The slice-16 record above is left as written; where it differs, this section supersedes it. No block, owner, label or backlog stub changed; no source was re-read; the legacy blocks in the artefact are untouched.

### Corrections

1. **One terminal payoff.** Slice 16 kept the printed objective $Q_T(S_T-AQ_T)$ in the Statement while its terminal condition and ansatz used $Q_T(S_T-\psi/2-AQ_T)$. The Statement now defines $H_t(\nu)$ with the corrected payoff, marked as Interpretation; the value, terminal condition, decomposition $h:=H^*-x-q(S-\psi/2)$, reduced equation and policy $\nu^*$ all use it. The printed objective is quoted under Pitfalls with its own decomposition $g:=H-x-qS$, giving $\nu^{\mathrm{pr}}=-(bq+\partial_qg+\psi/2)/(2\kappa)=\nu^*-(\psi/(4\kappa))e^{-\int_t^T\xi/\kappa}$. Slice 16's sentence "$\nu^*=-(bq+\partial_qh+\psi/2)/(2\kappa)$" reused $h$ across the two decompositions and is replaced.
2. **Finite value.** The unconstrained model can have infinite value: with $T=Q_0=1$, $\mu=\sigma=\psi=0$, $b=0.1$, $\kappa=A=0.01$, $\phi=0.001$ and $\nu=-M$, the reward's $M^2$ coefficient is $b/2-\kappa-A-\phi/3=0.0297>0$. From the pathwise identity (reward $=Q_0S_0-\psi Q_0/2-bQ_0^2/2+b\int Q\mu+\sigma\int Q\,dW-\kappa\int\nu^2-\phi\int Q^2-(A-b/2)Q_T^2$), the entry now states the sufficient regime $\kappa>0$, $\phi>0$, $A>b/2$, progressively measurable policies with $\mathbb E\int\nu^2<\infty$ and a flow with $\mathbb E\int\mu^2<\infty$; under it $|\zeta|<1$ and $\xi$ is finite and positive. It is sufficient, not necessary, and no verification theorem is claimed. The formal unconstrained benchmark is kept apart from one-directional execution ($\nu\ge0$, $Q\ge0$); clipping $\nu^*$ is not the constrained solution; a finite $A$ is a penalty, not compulsory completion.
3. **Variance.** For a deterministic schedule the random reward is $b\int Q\mu\,dt+\sigma\int Q\,dW$, so $\sigma^2\int Q^2$ is only the Brownian contribution; the variance adds $b^2\operatorname{Var}\int Q\mu$ and $2b\sigma\operatorname{Cov}$. It equals the whole variance when $b=0$ or the flow path is deterministic. Example $Q_t=1-t$, $\mu_t=B_t$, $T=1$, $\sigma=0$: $b^2/20$. Slice 16's "for a deterministic schedule the price-risk part of the shortfall has variance $\sigma^2\int Q^2$, so $\phi=\lambda\sigma^2$ reproduces a mean--variance penalty" is qualified accordingly.
4. **Units.** $b$ is in currency per share$^2$ (slice 16 said currency per share). The rest were rechecked: $\kappa$ currency·time/share$^2$, $\phi$ currency/(share$^2$·time), $A$, $h_2$, $\xi$ and $\sqrt{\kappa\phi}$ currency/share$^2$ (so $A-b/2\pm\sqrt{\kappa\phi}$ is homogeneous), $h_1$ currency/share, $\gamma$ per unit time, $\sigma$ currency/share/$\sqrt{\text{time}}$.

### Independent checks (`notes/artefacts/reinforcement-learning-trading/cartea_jaimungal_checks.py`, `followup_checks`)

- **Wealth identity.** Euler simulation of the dynamics against the identity for a random policy and flow ($\sigma=0$): 9.908237 against 9.908208 (discretisation error).
- **Terminal-payoff consistency.** A direct discretised optimisation over the inventory path ($\mu=\sigma=0$, a tridiagonal concave problem) against the feedback policies: inventory at $T/2$ and $T$ 0.5903 and 0.1954 for the corrected payoff, 0.6148 and 0.2451 for the printed payoff ($\kappa=0.01$, $\phi=0.001$, $A=0.05$, $b=0.02$, $\psi=0.01$), agreeing to four decimals in each case.
- **Finite-value restriction.** Simulated reward$/M^2$ for $\nu=-M$: 0.1375, 0.0315, 0.0298 at $M=10,100,1000$, converging to 0.02967; with $A=0.06>b/2$ it is $-0.02033$, matching $b/2-\kappa-A-\phi/3$.
- **Variance counterexample.** $\operatorname{Var}\int_0^1(1-t)B_t\,dt$: quadrature 0.05000, Monte Carlo (20,000 paths) 0.0506, exact $1/20$.
- The slice-16 checks in the same script still reproduce their earlier output.

### Validation

`migration_status.py --check`: 0 problems; 657 legacy blocks (530 + 98 + 29) and 67 entries, unchanged. Tests: 14 passed. `latexmk -g -pdf compendium.tex`: exit 0; 182 pages (181 before; the entry grew by a page); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had one overfull line (the wealth identity in one display), split into two lines. Rendered and inspected: PDF pp. 7–10 (the corrected entry). The standalone artefact `derivations.tex` did not change and was not rebuilt.

### Remaining limits

No verification theorem for the quadratic ansatz; the constrained one-directional problem is not solved; Cartea and Jaimungal's originals and `crypto-cartea` are still unconsulted; `wide-hambly-xu-yang` still read only in arXiv v4.

## Slice 17: production considerations, 15 October 2026

Migration of the file named as the next bounded slice, run from the slice-16 follow-up's pushed state (`8aa672a`, on `main`, matching `origin/main`; guide `343d145`; `house.tex` unchanged). The reported counts matched the checker: 657 legacy blocks (530 shared, 98 single-candidate, 29 assigned), 67 entries, 0 problems. Migration and source checking, not study.

### Slice-16 clarification

The wealth identity in `mod:cartea-jaimungal-execution` now states that the cash account starts at $X_0=0$, with $X_0$ to be added to the right-hand side otherwise. The follow-up's corrections, checks and limits are unchanged; the check script already starts cash at 0.

### Scope

The whole of `execution-trading-costs/01_.../08_production_considerations.tex`: 11 counted blocks; outside them only the `% migrate-to:` line and the subsection heading (checked by script). It was the last topic of `01_execution_and_algorithmic_trading/`, whose wrapper `00_overview.tex` then held only a section heading and this file's `\input`. Both files, the wrapper's `\input` (with its `\newpage`) in `legacy/execution-trading-costs/section.tex` and the map row were deleted. The asset-class folder `02_...` and its input are unchanged.

### Ownership, block by block

The map's single candidate, `model-governance-controls`, was a provisional tag. Its outcome concerns model inventory, validation and change, pre-trade and kill-switch controls, monitoring and incidents, and it receives the three blocks about reliability, network failure and audit trails. The rest go elsewhere:
- the architecture, input, analytics, venue-connection, model-component and indicator blocks follow Lehalle and Laruelle's sec. 3.1, whose sections 3.1.2–3.1.3 already have entries owned by the overview `execution-trading-costs` (`def:trading-envelope`, `meth:execution-decision-support`);
- the floor-against-automated cost comparison is Harris's market-structure chapter, routed to the overview `execution-market-making` (a routing exception);
- the brokerage organisation list was deleted.

The `research-engineering-validation` overview, whose outcome is reconstructing decisions and trades from records, was considered for the order-state and audit material. It has no note, and its FIX reading was not consulted, so it was left as a backlog direction rather than given an entry.

| # | Legacy block | Owner | Destination | Disposition | Rationale |
|---|---|---|---|---|---|
| 1 | *Trading Architecture* (principle) | `execution-trading-costs` | `def:automated-trading-architecture` (new) | Rewritten | Lehalle and Laruelle Fig. 3.1, pp. 193–194, 198; "the hard part … decision chain" flagged as synthesis |
| 2 | *Trading Tool Input Segmentation* | `execution-trading-costs` | `def:automated-trading-architecture` | Merged | sec. 3.1.1, pp. 194–197; calendar items beyond expiries, expected news and half-days unsupported |
| 3 | *Broker-Dealer Operations Segmentation* | none | artefact only | Deleted | Harris sec. 7.2 (pp. 147–148) classifies a brokerage as front office, back office (incl. compliance, credit, systems) and proprietary operations (cash and risk management); the legacy five-way list is its own and serves no pathway outcome |
| 4 | *Analytics Close to the Feed* | `execution-trading-costs` | `def:automated-trading-architecture` | Merged | p. 195; book imbalance and queue size not in the source |
| 5 | *Connections Are Two-Way* | `execution-trading-costs` | `def:automated-trading-architecture` | Merged | pp. 195–196; public book updates belong to the market-data feed, not the connection |
| 6 | *Model Component Segmentation* | `execution-trading-costs` | `def:automated-trading-architecture` | Merged | pp. 196–197, with deactivation of inadequate models; cross-referenced to the governance entry |
| 7 | *Indicator Publication* (process) | `execution-trading-costs` | `meth:execution-decision-support` | Merged | pp. 200–202; the book prints "stateless agents", the legacy "stateful" |
| 8 | *Audit Trail* (process) | `model-governance-controls` | `meth:automated-trading-operational-controls` (new) | Rewritten | Harris pp. 544–545; allocation, linkage to public state and the listed tests unsupported; current audit-trail rules not checked |
| 9 | *Automated Trading Reliability Segmentation* | `model-governance-controls` | `meth:automated-trading-operational-controls` | Merged | Harris pp. 549–551; Rule 15c3-5(c)(2)(iii)–(iv); drop copies, replayable feeds, tamper-resistant logs, bounded delays and the market-quality claim unsupported |
| 10 | *Network Failure Creates Position Risk* (caveat) | `model-governance-controls` | `meth:automated-trading-operational-controls` | Rewritten | Harris box p. 550; Rule 15c3-5(c)(1)(ii) (duplicative orders); unknown order state, fill state, reconciliation, retry, cancellation and recovery separated as Interpretation |
| 11 | *Automated System Cost Structure* (mechanism) | `execution-market-making` | `def:floor-automated-trading-systems` (new) | Rewritten | Harris chap. 27, pp. 543–554 and Table 27-1; routing exception |

### Overlaps resolved

`def:trading-envelope` (components and envelope, sec. 3.1.2) and `meth:execution-decision-support` (outputs, sec. 3.1.3) are not restated: the new architecture entry covers the inputs (sec. 3.1.1) and Figure 3.1 and cross-references both. `meth:transaction-cost-analysis` and `def:smart-order-routing` (dark probes, latency) are cross-referenced. No order-lifecycle entry exists; the venue messages are in the architecture entry and their use after a failure in the controls entry, with a backlog stub for FIX-level evidence.

### Sources, 2026-10-15

- **Lehalle and Laruelle**, 2018 World Scientific printing (local; printed page = PDF − 27): secs. 3.1–3.1.2, pp. 193–198, and sec. 3.1.3, pp. 199–203, text layer; page images of p. 194 (Figure 3.1) and p. 202.
- **Harris**, 2002 Oxford printing (local copy, AES-encrypted with an empty user password: Ghostscript could not open it, so the text was extracted and pages rendered through macOS PDFKit; printed page = PDF − 13): chap. 7, sec. 7.2, pp. 147–148, and box p. 159; chap. 27, pp. 543–554, page images of pp. 550 and 552.
- **17 CFR 240.15c3-5** (`cfr-240-15c3-5`, added to `front/sources.tex`): eCFR versioner API, point-in-time text for 13 October 2026, full section; one version listed (31 December 2016, the start of the versioner's history), adopted 75 FR 69825 (2010). U.S. law for broker-dealers with market access. The adopting release (`wide-sec-15c3-5`) was not read.
- **Not available or not read:** MiFID II RTS 6 (`wide-mifid-rts6`): EUR-Lex returned a bot challenge for both HTML and PDF, so no EU obligation is stated; the FIX specification (`s6-fix`); the Knight Capital order; U.K. statements; FIA guidance; Regulation SCI; audit-trail rules. Requests used a generic header.

### Claims kept apart

- **Legal requirement:** only Rule 15c3-5's provisions as quoted, U.S., broker-dealers with market access, current as of 13 October 2026.
- **Historical description:** Harris's practice and market facts as of 2002; Lehalle and Laruelle's architecture as of 2018.
- **Own synthesis (Interpretation):** the separation of unknown order state, fill state, reconciliation, retry, cancellation and recovery; the replay use of recorded messages.
- No supervisory guidance or voluntary framework was relied on.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | pp. 193–203 | Text layer; page images of pp. 194 and 202 |
| `alpha-harris` | pp. 147–148, 159, 543–554 | Text through PDFKit; page images of pp. 550 and 552 |
| `cfr-240-15c3-5` | full section, eCFR 13 Oct. 2026 | Adopting release not read |
| `wide-mifid-rts6`, `s6-fix`, `wide-knight-capital`, other pathway readings | none | Not retrieved or not read |

The three new entries and the extended `meth:execution-decision-support` are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The wrapper `00_overview.tex` (in a verbatim environment, since it `\input`s the deleted file) and the whole of `08_production_considerations.tex` below its `% migrate-to:` line (only the subsection unnumbered) are kept in the new artefact `notes/artefacts/model-governance-controls/derivations.tex`, which compiles on its own (2 pages, no warnings or bad boxes). A script confirmed both appear once, the 11 blocks once each and in order, and nothing else outside them. The artefacts of `market-making-lob` and `reinforcement-learning-trading` are unchanged (`git diff` empty).

### Counts

`migration_status.py`: 657 → 646 legacy blocks = 530 shared + 87 single-candidate + 29 assigned. `model-governance-controls`: exclusive 16 → 5 (the five in `sysinv/modelrisk.tex`), listed entries 0 → 1, backlog stubs 0 → 2. Entries 67 → 70 (definitions 26 → 28, methods 12 → 13). Listings: `execution-trading-costs` 13 → 14, `execution-market-making` 22 → 23; unchanged `market-structure-execution-quality` 5, `performance-manager-evaluation` 1, `price-impact-execution` 9, `market-making-lob` 13, `hft-market-design` 3, `reinforcement-learning-trading` 1.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 186 pages (182 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had three overfull lines (the new artefact path in Further reading) and one underfull line (a See-also), all from this slice and fixed. The new chapter `research-engineering-validation` is Chapter 1; later chapters are renumbered by one, labels unchanged. Rendered and inspected: PDF pp. 7–9 (the new chapter), 51 (the floor-against-automated entry), 60–61 (the architecture entry and decision support) and 182 (the legacy execution chapter, which now starts at *Asset-Class-Specific Microstructure*). Tests: 14 passed.

### For review

- Routing blocks 1–7 to the execution overview, 11 to `execution-market-making`, and deleting block 3.
- The order-state synthesis and the reliance on one U.S. rule; the RTS 6 and FIX stubs.

## Slice 17 follow-up: clarifications, 15 October 2026

Three clarifications to slice 17 (`1c3fabc`), made at the start of slice 18; the slice-17 record above is left as written.

- `def:automated-trading-architecture`: Lehalle and Laruelle's "known in real time" is now quoted as theirs and qualified. The market volume $V$ is available only as observed; volume still to come requires a forecast. It cross-references the decision-time item already in `def:trading-envelope`.
- `cfr-240-15c3-5` in `front/sources.tex`: the SEC adopting release, 34-63241, is dated 3 November 2010 (checked on p. 130 of the release PDF from sec.gov); the Federal Register published it on 15 November 2010, where the eCFR cites the rule text at 75 FR 69825.
- `def:floor-automated-trading-systems`: the six bullets are now presented as the entry's grouping of Harris's seven sections (27.1–27.7), with Table 27-1 listing eleven issues. High absolute start-up costs (p. 549) and the table's relatively lower software costs (p. 552) are recorded as compatible, not as a contradiction; the Harris reading note and the `execution-market-making` pathway note were reworded to match.

## Slice 18: equity market microstructure, 15 October 2026

Migration of the file named as the next bounded slice, run from slice 17's pushed state (`1c3fabc`, on `main`, matching `origin/main`; guide `343d145`; `house.tex` unchanged). The reported counts matched the checker: 646 legacy blocks (530 shared, 87 single-candidate, 29 assigned), 70 entries, 0 problems. Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/02_.../01_equity_market_microstructure.tex`: 6 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper and its other six topics are unchanged.

### Ownership, block by block

The map's single candidate, `market-structure-execution-quality`, received no block. Its outcome is current fragmentation, fee, tick, odd-lot and retail-routing rules and their effect on execution quality. The checked support for these blocks was Harris's 2002 descriptions and ETF readings, and current venue rules were not checked; the pathway receives a backlog stub instead.

| # | Legacy block | Owner | Destination | Disposition | Rationale |
|---|---|---|---|---|---|
| 1 | *Equities as Microstructure Laboratory* (principle) | none | artefact only | Deleted | No checked source supports "cleanest empirical laboratory" or the transfer list; the asset-class pathways carry the differences with their own readings |
| 2 | *Asset-Class Transfer* (caveat) | none | artefact only | Deleted | Orientation statement without a checked source; the same pathways cover it |
| 3 | *Equity Block Prints and Size Priority* (marketrule) | `execution-trading-costs` | `def:block-trade` (Practice, Pitfalls); stub `rule:block-print-trade-through-current` in `market-structure-execution-quality` | Merged as historical; current rules stubbed | Harris sec. 15.6.1, pp. 333–334 (2002): print requirement, size precedence above 25,000 shares, price priority; reporting, execution priority and trade-through protection separated; "trade-reporting facility" and current exceptions unverified |
| 4 | *Index Markets Trade Common Risk* (principle) | `execution-trading-costs` | `def:portfolio-trading` (Conditions, Pitfalls) | Merged | Harris pp. 484, 489: three reasons (few informed traders, activity, one transaction); "easier to net" and "easier to hedge" are not his |
| 5 | *Index Product Segmentation* (taxonomy) | `etf-index-closing-execution` | `mech:etf-creation-redemption` (Practice, Pitfalls) | Merged | Harris sec. 23.5, pp. 491–492; futures "basis" and the closing choice sentence unsupported |
| 6 | *ETF Basket Arbitrage* (mechanism) | `etf-index-closing-execution` | `mech:etf-creation-redemption` (new) | Rewritten | Lettau and Madhavan pp. 4–8, 18; Pan and Zeng pp. 1–3; borrow, cash substitution and taxes as weakening factors unsupported |

Routing exceptions: blocks 3 and 4 go to the overview `execution-trading-costs`, owner of `def:block-trade` and `def:portfolio-trading`; blocks 5 and 6 go to `etf-index-closing-execution`, whose outcome names ETF creations. `ev:index-reconstitution-impact` (owned by `price-impact-execution`) is cross-referenced, not extended.

### Sources, 2026-10-15

- **Harris**, 2002 Oxford printing (text through macOS PDFKit, as in slice 17; printed page = PDF − 13): sec. 15.6.1, pp. 333–334; chap. 23, p. 484, sec. 23.4, p. 489, sec. 23.5 with Table 23-1, pp. 491–492.
- **Lettau and Madhavan** (`ex-lettau-madhavan-2018`): NBER Working Paper 24250, January 2018, pp. 1, 4–8, 18, text layer. The published JEP version was not retrieved (the AEA site returned a bot check). The paper discloses Madhavan's BlackRock role.
- **Pan and Zeng** (`wide-pan-zeng-etf`): ESRB Working Paper 59, December 2017, abstract and pp. 1–3, text layer (printed page = PDF − 2). SSRN, the catalogue's record, returned a bot page.
- **Not consulted:** current exchange or FINRA block and trade-reporting rules, Rule 611 trade-through exceptions, SEC Rule 6c-11 on ETFs, Hasbrouck (the only local Hasbrouck file found was his 2004 lecture notes, which the reading note already excludes). All requests used generic headers.

### Distinctions kept

- **Block trades.** Reporting or printing venue, execution priority against the book, and trade-through protection across venues are kept apart in `def:block-trade`; only Harris's 2002 exchange rule is stated.
- **ETFs.** Creation and redemption between APs and the fund is kept apart from secondary trading of ETF shares, in-kind from cash, and the arbitrage incentive from guaranteed convergence; stale NAV and AP discretion are the stated limits. Pan and Zeng's evidence is labelled corporate-bond-only.
- **Index costs.** Harris's three reasons replace the legacy four.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | pp. 333–334, 484, 489, 491–492 | Text through PDFKit; facts as of 2001–2002 |
| `ex-lettau-madhavan-2018` | WP pp. 1, 4–8, 18 | Working-paper version, not the JEP article |
| `wide-pan-zeng-etf` | ESRB pp. 1–3 and abstract | Model and data read only in the introduction |
| current venue and ETF rules | none | Not checked; stubbed or stated as unchecked |

The new entry and the two extended entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/etf-index-closing-execution/derivations.tex` (1 page, no warnings or bad boxes), with only the subsection unnumbered; a script confirmed the body appears once and the six blocks once each, in order, with nothing else outside them. Existing artefacts are unchanged (`git diff` empty for the three earlier ones).

### Counts

`migration_status.py`: 646 → 640 legacy blocks = 530 shared + 81 single-candidate + 29 assigned. `market-structure-execution-quality`: exclusive 6 → 0; assigned 3 and shared 290 unchanged; listed entries 5; backlog stubs 0 → 1. Entries 70 → 71 (mechanisms 2 → 3). Listings: `etf-index-closing-execution` 0 → 1 (new note); `execution-trading-costs` 14 (two entries extended, none added); others unchanged.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 187 pages (186 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 59 (`def:block-trade`), 64 (`def:portfolio-trading`), 81–82 (the new ETF section) and 184 (the legacy asset-class section, which now starts at *Futures Market Microstructure*); pp. 52 and 61 hold the slice-17 follow-up wording. Tests: 14 passed.

### For review

- Routing all six blocks away from the map candidate; deleting blocks 1 and 2.
- The ETF entry's reliance on working-paper versions.

## Slice 18 follow-up: ETF and Harris precision, 15 October 2026

A bounded correction to slice 18 (`580463e`), run from that pushed state (640 legacy blocks = 530 shared + 81 single-candidate + 29 assigned, 71 entries, checker clean, guide `343d145`). The slice-18 record above is left as written; where it differs, this section supersedes it.

1. **Pan and Zeng: predictions against findings.** ESRB WP 59 p. 4 was read with pp. 1–3. The entry now separates the model's predictions (an arbitrage effect, and an inventory-management effect that can reverse the direction of creations and redemptions) from the empirical findings:
   - a 1 percent premium raises AP arbitrage by 50 bp, and a one-standard-deviation rise in volatility lowers it by 10 percent, more at discounts;
   - under extreme inventory, creations and redemptions follow inventory more and mispricing less; a difference-in-differences shows less (more) net redemption after large positive (negative) inventory shocks;
   - overall, arbitrage still goes the corrective way, and the authors "do not find evidence of the complete 'failure' of ETF arbitrage".

   The entry says that inventory pressure weakens corrective arbitrage, not that arbitrage fails, and does not claim that opposite-direction episodes never occur.
2. **Fund trading and costs.** Secondary trading and in-kind creations and redemptions do not themselves require the fund to trade the underlying; cash creations and redemptions can, and who bears those costs is not stated in the passages read.
3. **The \$100 million illustration.** The source's arithmetic is preserved (\$84,985,000 for the mutual fund; the ETF's non-selling investors "will hold a fund whose assets are valued at \$85 million"). The entry adds, as Interpretation, that pure secondary trading leaves total assets at \$100 million. Total assets of \$85 million follow from a net \$15 million in-kind redemption, held by the original non-sellers (\$80 million) and new buyers (\$5 million). This distinguishes total fund assets from the holdings of remaining investors.
4. **Harris precision.**
   - `def:portfolio-trading`: index arbitrageurs did about 9 percent of reported program-trade volume, about 2.4 percent of NYSE volume (p. 489).
   - `def:block-trade`: the 2002 print requirement applied to brokers and dealers who were exchange members (p. 333).

Reading notes `wide-pan-zeng-etf` and `ex-lettau-madhavan-2018`, and the pathway notes of `etf-index-closing-execution` and `execution-trading-costs`, were updated.

## Slice 19: futures market microstructure, 15 October 2026

Migration of the file named as the next bounded slice, run after the follow-up above. Migration and source checking, not study, and not the pathway's checkpoint: no roll cost was measured.

### Scope

The whole of `execution-trading-costs/02_.../02_futures_market_microstructure.tex`: 7 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper and its other five topics are unchanged.

### Ownership and dispositions

`futures-execution` (the map's single candidate) owns six blocks. Its outcome is executing futures orders and rolls using the contract's matching algorithm, settlement mechanisms and cross-market price discovery. The large-tick block is general microstructure and went to an existing entry of `execution-market-making` (a routing exception), with a futures-specific backlog stub.

| # | Legacy block | Owner | Destination | Checked locator | Disposition |
|---|---|---|---|---|---|
| 1 | *Centralised Futures Trading* (principle) | `futures-execution` | `conv:cme-globex-trading` (new) | Harris sec. 15.6.2, p. 334; CME Rulebook Rules 526, 538 | Rewritten; the legacy reasons (margining, fungibility) unsupported, the rule-based reason substituted |
| 2 | *No Call Auction Norm* (caveat) | `futures-execution` | `conv:cme-globex-trading` | CME wiki "Indicative Opening Price and Quantity" and "Supported Matching Algorithms" (updated 11 Feb. 2025); CFTC filing 22 Sep. 2020 | Corrected: wrong for the Globex open; ES daily settlement is a 30-second VWAP; "liquid trading hours" unsupported |
| 3 | *Lead-Lag With Cash Markets* (mechanism) | `futures-execution` | `ev:index-futures-price-discovery` (new) | Hasbrouck WP FIN-00-046 abstract, pp. 4–6, 13, 34; Harris p. 489 via `def:portfolio-trading` | Rewritten as evidence; the legacy conditions marked untested |
| 4 | *Large Tick Futures* (principle) | `execution-market-making` | `res:spread-determinants` (merged); stub `ev:futures-tick-size-evidence` in `futures-execution` | Lehalle and Laruelle eq. (2.1), pp. 144–145, and p. 148 | Merged; the futures-specific and equity-comparison claims unchecked |
| 5 | *Futures Architecture Drivers* (taxonomy) | `futures-execution` | `mech:futures-margin-settlement` (Pitfalls) | CME Rules 802, 814, 820; Harris p. 492; Rule 538 | Merged; standardisation and ETF link unchecked |
| 6 | *Variation Margin* (mechanism) | `futures-execution` | `mech:futures-margin-settlement` (new) | CME Rules 814, 820, 802.B | Rewritten; "credit risk controlled continuously" corrected |
| 7 | *Futures Block and EFP Segmentation* (taxonomy) | `futures-execution` | `conv:futures-block-efrp` (new) | CME Rules 526, 538; RA2607-5 pp. 4, 10 (Q14), Q28; RA1911-5 p. 1; Harris p. 334 | Rewritten; "transitory EFP" verified as history and prohibited at CME Group since 4 Aug. 2014 |

`def:block-trade` (equity, Harris 2002) is cross-referenced and kept separate from the futures block rules; `def:portfolio-trading` is cross-referenced from the price-discovery entry.

### Sources, 2026-10-15 (generic request headers)

- **CME Rulebook**, chap. 5 (Rules 526, 538; its 538.K already has the NDF wording effective 7 Aug. 2026) and chap. 8 (Rules 802.B, 814, 820), PDFs from cmegroup.com.
- **CME Group advisory RA2607-5** (24 July 2026, effective 7 Aug. 2026), read as Exhibit B of the CFTC certification of 23 July 2026 (submission 26-369); **RA1911-5** (17 Dec. 2019) for the 2014 history.
- **CME Client Systems Wiki** (the catalogue's `ex-cme-matching`): "Supported Matching Algorithms" and "Indicative Opening Price and Quantity", both updated 11 Feb. 2025, read from the HTML; the parent page through WebFetch.
- **CFTC filing of 22 Sep. 2020** (E-mini S&P 500 daily settlement, trade date 26 Oct. 2020). The current settlement page was not retrievable (a holding response).
- **Hasbrouck** (`ex-hasbrouck-2003`): NYU working paper FIN-00-046, preliminary draft of 16 Nov. 2000, not the published version.
- **Harris**, 2002 printing: pp. 334, 489, 492. **Lehalle and Laruelle**, 2018 printing: pp. 144–145, 148.
- **Not available:** Garbade and Silber (1983, `w5-garbade-silber`); only secondary descriptions were found and none was used.

### Distinctions kept

- **Venue rules against outcomes.** The tick is a constraint, the matching algorithm a rule, and bounce and book size observed outcomes; the opening uncross (rule) is kept apart from the settlement VWAP (a price-determination procedure).
- **Margin.** Contract standardisation, initial margin (performance bond), variation settlement, intraday cycles, FCM–customer arrangements and residual default risk are separated; daily settlement does not eliminate credit risk.
- **Blocks and EFRPs.** Eligibility, the related position, reporting and submission are listed per rule; the history of transitory EFPs (Harris 2002; permitted until 4 Aug. 2014) is kept apart from current rules.
- **Price discovery.** The empirical result (sample March–May 2000) is kept apart from theory (Garbade–Silber, unread) and from the legacy's explanations (untested).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| CME Rulebook chaps. 5, 8 | Rules 526, 538, 802.B, 814, 820 | Product thresholds, reporting times and cycle times in separate notices not read |
| RA2607-5, RA1911-5 | pp. 1, 4, 10, Q14, Q28 | — |
| CME Client Systems Wiki | two pages, updated 11 Feb. 2025 | Product algorithm checked for SOFR futures only |
| CFTC filing 2020 | Exhibit A, E-mini S&P 500 | Current procedure not retrieved |
| `ex-hasbrouck-2003` | WP abstract, pp. 4–6, 13, 34 | Draft, not the JF version; S&P 400 result may differ |
| `w5-garbade-silber` | none | Not available |

The four new entries and the extended `res:spread-determinants` are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/futures-execution/derivations.tex` (1 page, no warnings or bad boxes), with only the subsection unnumbered; a script confirmed the body appears once and the seven blocks once each, in order, with nothing else outside them. Earlier artefacts are unchanged.

### Counts

`migration_status.py`: 640 → 633 legacy blocks = 530 shared + 74 single-candidate + 29 assigned. `futures-execution`: exclusive 7 → 0, shared 18 unchanged, listed entries 0 → 4 (new note), backlog stubs 0 → 1. Entries 71 → 75 (conventions 0 → 2, evidence 3 → 4, mechanisms 3 → 4). Other listings unchanged. A first checker run, before the pathway note existed, reported the four new entries as listed in no note; fixed by the note.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 191 pages (187 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had one overfull See-also line in the new evidence entry, reworded. Rendered and inspected: PDF pp. 41 (`res:spread-determinants`), 82–86 (the ETF follow-up and the new futures section) and 188 (the legacy asset-class section, which now starts at *FX Market Microstructure*). Tests: 14 passed.

### For review

- The four new entries; routing the large-tick block to `execution-market-making`.
- The reliance on CME documentation retrieved on one date, and on a 2000 working-paper draft for the price-discovery evidence.

## Slice 19 follow-up: corrections, 15 October 2026

A bounded correction to slice 19 (`fb56198`), run from that pushed state (633 legacy blocks = 530 shared + 74 single-candidate + 29 assigned, 75 entries, checker clean, guide `343d145`, clean tree matching `origin/main`). The slice-19 record above is left as written; where it differs, this section supersedes it. No block, owner, label, artefact or backlog stub changed; the FX file (slice 20) was not started.

1. **Large-tick equation.** Lehalle and Laruelle's eq. (2.1), checked on the page image of p. 145, is $\psi_i=a+(b_1\sigma_i+b_2\eta\,\mathrm{tick})/\sqrt{N_i}$: both terms are over $\sqrt{N_i}$. Slice 19 had put only the volatility term over it in `res:spread-determinants`. The entry now matches `meth:spread-volatility-regression`, which already had it right; the reading note `alpha-laruelle` was corrected too. No other occurrence in the compendium or notes. The empirical scope and the futures-specific backlog stub are unchanged.
2. **Default waterfall and performance bond.** CME Rules 802.A and 802.B were read in full in the chapter-8 PDF retrieved on 15 October 2026. `mech:futures-margin-settlement` now gives the Base waterfall as:
   - the defaulting member's own resources, applied by account class, with customer collateral ring-fenced from proprietary losses and from other customer classes (802.A.2, 802.A.5);
   - CME's \$100 million;
   - the Base Guaranty Fund, the non-defaulting members' prefunded contributions, applied in the rule's order (subordinated, then pro rata, then seniorized amounts);
   - assessments capped at 275 percent (single default) and 550 percent (all defaults in a cooling-off period) of each member's Base Guaranty Fund requirement.

   Rule 802.B.1 lists "The Base Guaranty Fund" (ii) and "the Guaranty Fund contributions of non-defaulting Base Clearing Members" (iii) as separate items; since the fund consists of members' contributions (802.A.4), the entry counts it once. Rule 820's retention is now quoted as "in whole or in part, as Clearing House staff may deem necessary".
3. **2020 settlement.** The procedure is Exhibit B of the filing (blackline); Exhibit A only lists products. On the rendered blackline the amended Tier 1 uses E-mini Globex trades alone: floor trades in the full-sized contract, the multiplier of five and "combined" are struck. The full procedure is now stated:
   - ES and MES settle to SP's settlement rounded to the nearest tradable tick, and SP's lead month is rounded to 0.10;
   - Tier 2 (bid/ask midpoint) applies if there are no trades, and Tier 3 (carry from the cash index) if no two-sided market is available;
   - the second month follows its three tiers, and staff may override.

   The entry, `front/sources.tex` and the futures pathway note's dating were updated; the procedure stays dated 2020.
4. **Scope points.**
   - `conv:futures-block-efrp` now spells out Rule 538.K, checked on the rulebook page image (p. 29) and on the filing's Exhibit A blackline: EFPs whose related position is a cash transaction and EFRs whose related position is an NDF, in foreign currencies only, never as EOOs. The amendment changed 538.K only, leaving 538.A--J unchanged. It also gives 538.A's carve-out (rulebook p. 28): for these immediately offsetting FX EFPs the third-party pass-through requirement does not apply, and the cash legs need not be passed through when CTAs or account controllers act, though the customer bears the offsetting leg's P&L if the futures leg fails to clear.
   - `mech:etf-creation-redemption`'s opening now quotes Lettau and Madhavan ("does not interact with capital markets directly", p. 4) and qualifies it by the existing distinction: secondary and in-kind transactions do not make the fund trade, while cash creations and redemptions can. The Pan–Zeng, \$100m/\$85m and Harris text are unchanged.

### Sources checked

- Lehalle and Laruelle, 2018 printing, p. 145, page image.
- CME Rulebook chap. 8, Rules 802.A--802.B (full text) and 820.
- CME Rulebook chap. 5, pp. 27--29, page images.
- CFTC filing of 22 September 2020, Exhibits A and B, page images of pp. 5--6.
- CME Group RA2607-5 filing of 23 July 2026, pp. 1--3 with the Exhibit A blackline as a page image.

All are the copies retrieved on 15 October 2026 with generic headers; no new retrieval was needed.

### Validation

`migration_status.py --check`: 0 problems; 633 legacy blocks and 75 entries, unchanged. Tests: 14 passed. `latexmk -g -pdf compendium.tex`: exit 0; 193 pages (191 before, from the longer waterfall and settlement text); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: printed pp. 35 (`res:spread-determinants`), 75 (the ETF opening), 78 (settlement) and 79--80 (EFRP and margin), PDF pp. 41, 81, 84 and 85--86.

### Remaining limits

- The current CME settlement page is still unretrieved, so the procedure is as filed in 2020.
- Default-management auction details (subordination and seniorization amounts) are in confidential guidelines.
- Customer-side FCM rules and intraday cycle times are unchecked.

## Slice 19 second follow-up: account classes and the second-month settlement, 15 October 2026

Two wording clarifications, run from `bd4ba54` (633 legacy blocks = 530 shared + 74 single-candidate + 29 assigned, 75 entries, checker clean, guide `343d145`). Earlier records are left as written.

1. `mech:futures-margin-settlement`: "customer losses only from the collateral of the customer account class concerned" stated the restriction in the wrong direction. CME Rules 802.A.5 and 802.G (including 802.G.1 and 802.G.6), read in the chapter-8 text retrieved on 15 October 2026, give the following, and the entry now says so:
   - default management runs separately by account class;
   - a customer-class loss is met first from that class's customer collateral, which in a defaulted customer futures class includes the collateral of customers who did not cause the default (802.G.1);
   - the member's own assets are applied across classes with priority to customers (802.A.5.i, iii);
   - remaining proprietary collateral may cover customer-class losses, pro rata among defaulted customer classes (802.G.6);
   - segregated customer collateral may not be used for proprietary obligations or for another customer class.
2. `conv:cme-globex-trading`: the second month is derived by applying the lead–second spread price to the lead-month settlement. Tier 2 says so explicitly in Exhibit B (PDF p. 6, rendered blackline): the last spread trade, or the nearer of the spread's bid or ask if the trade lies outside them. The entry marks the same reading of Tier 1 as Interpretation. The ES-only VWAP, the rounding and the 2020 dating are unchanged.

## Slice 20: FX market microstructure, 15 October 2026

Migration of the four-block FX file, run after the follow-up above. Migration and source checking, not study; the pathway's checkpoint was not attempted.

### Scope

The whole of `execution-trading-costs/02_.../03_fx_market_microstructure.tex`: 4 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper and its other four topics are unchanged.

### Ownership and dispositions

`fx-dealer-market-making` (the map's single candidate) owns all four blocks. Its outcome is pricing a spot FX client franchise, choosing between internalising and hedging, and evaluating aggregator and last-look practices against fill and markout evidence. The one item outside that outcome, "fixing windows", is benchmark timing; it was left to `fx-funding-settlement`, whose outcome covers conduct around benchmark fixes, without an entry. That is the only routing exception, and it is not a migration into another entry. The pathway sits in the section `execution-market-making`, so the entries are in `compendium/execution-market-making/fx-dealing.tex`.

| # | Legacy block | Owner | Destination | Checked sources | Disposition |
|---|---|---|---|---|---|
| 1 | *FX Is Dealer-Centric and Fragmented* (principle) | `fx-dealer-market-making` | `def:fx-market-structure` (new) | BIS pp. 22–23; Cartea–Jaimungal–Walton p. 2 | Rewritten; prime-brokered access unchecked |
| 2 | *FX Venue Segmentation* (taxonomy) | `fx-dealer-market-making` | `def:fx-market-structure` (venues, ECNs, RFQ); `mod:fx-internalisation-horizon` (new; internalisation); fixing windows left to `fx-funding-settlement` | BIS pp. 5, 12, 23, 43; Butz–Oomen pp. 1–2, 8, 11 | Split: venues, protocols and internalisation separated; RFQ "for size or less liquid pairs" unsupported as a restriction |
| 3 | *Last Look* (definition) | `fx-dealer-market-making` | `mech:fx-last-look` (new) | FX Global Code Principle 17, pp. 22–23 (page images), p. 1; DB cover sheet sec. C.4; CJW abstract | Rewritten; the stale-quote rationale marked as the model premise |
| 4 | *FX Cost Is Relationship-Dependent* (caveat) | `fx-dealer-market-making` | `mech:fx-last-look` (Practice, Pitfalls) and `mod:fx-internalisation-horizon` (Practice); stub `ev:fx-last-look-fill-reject-evidence` | BIS Box B p. 11, p. 27; Butz–Oomen abstract, p. 2; DB cover sheet | Merged; "can dominate fill quality" dropped as unsupported; prime-broker limits unchecked |

Overlaps: `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment` and `mod:inventory-based-quotes` (generic dealer theory), `def:smart-order-routing` and `def:best-execution` (equity sources) and `res:latency-arbitrage-arms-race` (ES–SPY evidence) are cross-referenced, each labelled as not FX evidence; none was changed.

### Sources, 2026-10-15 (generic request headers)

- **BIS Markets Committee**, *FX execution algorithms and market functioning*, October 2020 (`exp-fx-algos`), official PDF: pp. 5, 11–13, 21–24, 27–28, 43, text layer (printed page = PDF − 6). A study-group survey with interviews.
- **FX Global Code**, updated December 2024 (`exp-fx-code`), official PDF: p. 1 (status) and Principle 17, pp. 22–23, on page images, because the text layer contains hidden placeholder text.
- **Deutsche Bank**, GFXC Liquidity Provider Disclosure Cover Sheet, completed 18 September 2025 (`db-fxgc-lp-cover-2025`, added to `front/sources.tex`), sec. C.4: one provider's self-reported terms.
- **Butz and Oomen** (`cfd-butz-oomen-2019`), accepted version on LSE Research Online (manuscript November 2017): abstract, pp. 1–2, 8 and 11, page images of pp. 8 and 11; the EUR/USD calibration recomputed (12.75/3.66/2.507 ≈ 1.39 minutes). The authors were in Deutsche Bank's e-FX division.
- **Cartea, Jaimungal and Walton** (`dm-cartea-jaimungal-walton-2019`), arXiv 1806.04460v1 (12 June 2018): abstract and p. 2.
- **Not available or not read:**
  - `dm-oomen-last-look-2017` and `dm-oomen-aggregator-2017`: no open copy found; the old LSE eprints listing returned 404, and the new repository's search did not surface them;
  - `wide-king-osler-rime`;
  - the pathway's empirical order-flow readings.

### Distinctions kept

- **Structure.** Venues and access channels, trading protocols (RFQ/RFS, algorithms), internalisation (a dealer's risk-management choice, with its horizon model) and fixing windows (benchmark timing, another pathway's) are separated.
- **Quotes and rejections.** Firm quotes (anonymous order books) are kept apart from conditional ones (disclosed pools with last look). Price-check rejection is kept apart from validity rejection (credit, exposure, permissioning) and from technical failures; prime-broker restrictions are unchecked.
- **Costs.** Quoted spreads are kept apart from realised costs, reject ratios and markouts (named as TCA metrics only). No FX evidence on magnitudes was found, so no benchmark, horizon or selection effect is reported for one.
- **Status of claims.** The Global Code is voluntary guidance (it disclaims legal obligations), the provider sheet is contractual disclosure, Cartea–Jaimungal–Walton is a theoretical prediction, the BIS report is survey evidence, and Butz–Oomen is a model calibrated to survey aggregates.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `exp-fx-algos` | pp. 5, 11–13, 21–24, 27–28, 43 | Survey and interviews, 2020 |
| `exp-fx-code` | p. 1; pp. 22–23 (page images) | Voluntary; December 2024 edition |
| DB cover sheet | sec. C.4 | One provider, self-reported |
| `cfd-butz-oomen-2019` | abstract, pp. 1–2, 8, 11 | Accepted manuscript; model calibrated top-down |
| `dm-cartea-jaimungal-walton-2019` | abstract, p. 2 | arXiv v1; theory |
| Oomen (2017, two papers), King–Osler–Rime | none | Not available or not read |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/fx-dealer-market-making/derivations.tex` (1 page, no warnings or bad boxes), with only the subsection unnumbered; a script confirmed the body appears once and the four blocks once each, in order, with nothing else outside them. Earlier artefacts are unchanged.

### Counts

`migration_status.py`: 633 → 629 legacy blocks = 530 shared + 70 single-candidate + 29 assigned. `fx-dealer-market-making`: exclusive 4 → 0, listed entries 0 → 3 (new note), backlog stubs 0 → 1. Entries 75 → 78 (definitions 28 → 29, mechanisms 4 → 5, models 9 → 10). Other listings unchanged.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 195 pages (193 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 53–55 (the new FX section), 87 and 89 (the slice-19 clarifications) and 192 (the legacy asset-class section, which now starts at *Options Market Microstructure*). Tests: 14 passed.

### For review

- The three new FX entries.
- Leaving fixing windows to `fx-funding-settlement` without an entry.
- The reliance on a voluntary code, one provider's disclosure and open manuscript versions.

## Slice 20 follow-up: corrections, 15 October 2026

Targeted corrections to two slice-20 entries; the slice-20 record above is left as written.

- `mod:fx-internalisation-horizon`: Butz and Oomen's eq. (8) defines the expected queue length $L$ and the arrival rate $\lambda$ of risk-increasing trades; $L/\lambda$ is the conditional horizon of a risk-increasing trade, and, since risk-reducing trades wait zero, the all-trade average is $W=L/(2\lambda)$ (eq. (9), p. 7). $\lambda_0$ is the baseline intensity of buys and of sells in the skew examples (Examples 1–2, eqs. (5)–(7), pp. 5–6, page images), not $\lambda$. The EUR/USD figure of 1.39 minutes is now labelled the all-trade average the authors report; the conditional horizon, about 2.78 minutes, is labelled as own recomputation (exact stationary sum: $L/\lambda=2.774$, $W=1.387$). Notation and Status updated; `notes/readings/cfd-butz-oomen-2019.md` and the pathway note updated.
- `mech:fx-last-look`: all three of the Code's cover-and-deal conditions are stated (explicit understanding of filling without market risk by first entering offsetting transactions; the volume traded in the window passed on in its entirety; the understanding documented and disclosed, p. 23, page image). The Code's "expected or typical period of time for making the decision" is called the decision time, the duration of the last-look window, and is kept apart from the time spent on checks and from any additional hold. The Deutsche Bank 10-millisecond bound is kept to its scope: the spot price check, with no additional hold; the validity check's duration is not bounded in the sheet, and non-spot products may differ. `notes/readings/exp-fx-code.md` and the pathway note updated.

Checks: as for slice 21 below (same build and test run).

## Slice 21: options market microstructure, 15 October 2026

Migration of the four-block options file, run after the follow-up above. Migration and source checking, not study; the pathway's checkpoint was not attempted.

### Scope

The whole of `execution-trading-costs/02_.../04_options_market_microstructure.tex`: 4 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper and its other three topics (fixed income, securities lending, crypto) are unchanged.

### Ownership and dispositions

`options-execution` (the map's single candidate) owns all four blocks. Its outcome is explaining option spreads and execution costs through market-maker hedging, inventory and volatility risk, and measuring how retail order flow is routed and what it pays. The pathway sits in the section `execution-market-making`, so the entries are in the new topic file `compendium/execution-market-making/options-dealing.tex`, input after `fx-dealing.tex`; the chapter opener names it. The blocks were merged into three entries by question (why spreads exist, how costs are measured, how retail flow is routed), not one entry per block.

| # | Legacy block | Owner | Destination | Checked sources | Disposition |
|---|---|---|---|---|---|
| 1 | *Options Are Surface Markets* (principle) | `options-execution` | `res:option-market-maker-spreads` (new) | Jameson–Wilhelm, Huh–Lin–Mello, Muravyev (abstracts) | Rewritten; "liquidity lives on a surface" kept as interpretation only, the implied-volatility surface distinguished from uniform liquidity |
| 2 | *Post-Trade Complexity* (caveat) | `options-execution` | `res:option-market-maker-spreads` (Pitfalls); stub `mech:options-clearing-exercise-assignment` | Battalio–Hatch–Jennings (abstract) | Clearing, exercise, assignment and margin constraining fragmentation unchecked (no OCC or exchange rule read); "dominated by cross-contract risk" dropped as unmeasured |
| 3 | *Market-Maker-Centric Liquidity* (mechanism) | `options-execution` | `res:option-market-maker-spreads` (who supplies quotes); `mech:options-retail-wholesaler-routing` (new) | Bryzgalova–Pavlova–Sikorskaya pp. 2, 11; Muravyev–Pearson (abstract) | Split; "buy-side traders typically consume liquidity" and its explanation not adopted |
| 4 | *Options Liquidity Segmentation* (taxonomy) | `options-execution` | items iii–iv `res:option-market-maker-spreads`; items i, ii, v `meth:option-spread-measurement` (new); stub `def:option-complex-orders` | Bryzgalova–Pavlova–Sikorskaya Table I, pp. 15–16 (page images), pp. 12, 14, 17; Jameson–Wilhelm, Huh–Lin–Mello (abstracts) | Split; ATM "deepest" supported only as trade share and percentage quoted spread, not depth; "reduces size" and complex orders unchecked |

Overlaps: `def:dealer-inventory-risk`, `meth:dealer-quote-adjustment`, `mod:inventory-based-quotes`, `res:adverse-selection-spread-component`, `def:spread-measures` and `res:spread-determinants` (generic and equity dealer material), `def:best-execution` and `def:broker-agency-conflicts` (equity PFOF), and `conv:futures-block-efrp`, `def:portfolio-trading` and `mech:etf-creation-redemption` are cross-referenced, each labelled as not establishing option claims; none was changed.

### Sources, 2026-10-15 (generic request headers)

- **Bryzgalova, Pavlova and Sikorskaya** (`ex-bryzgalova-pavlova-sikorskaya-2023`), the published *Journal of Finance* article, open access (CC BY), early-view pagination, from LBS Research Online eprint 2827: abstract and pp. 2, 4–5, 7, 11–12, 14–17, text layer (printed page = PDF − 1), with page images of Table I (pp. 15–16). U.S. OPRA data, 4 November 2019 to 30 June 2021.
- **Abstracts only**, from the publishers' records as served by RePEc, Crossref and OpenAlex: Jameson and Wilhelm (`ex-jameson-wilhelm-1992`), Huh, Lin and Mello (`ex-huh-lin-mello-2015`), Muravyev (`wide-muravyev-order-flow`), Muravyev and Pearson (`wide-muravyev-pearson`), Battalio, Hatch and Jennings (`ex-battalio-hatch-jennings-2004`). No open full text was found; the EFMA 2013 working-paper copy of Huh, Lin and Mello returned HTTP 503, and a copy of Muravyev and Pearson on a trading-forum host was not used.
- **Not read:** any OCC or exchange rule on clearing, exercise, assignment, margin, complex orders or price-improvement auction fees; `wide-christoffersen-option-illiquidity`, `ex-eraker-osterrieder-2023`, `exp-baldacci-options-market-making`.

### Distinctions kept

- **Surface and liquidity.** A linked set of prices (the implied volatility surface) is kept apart from liquidity, which is measured contract by contract; option liquidity is kept apart from the hedge instrument's.
- **Risks.** Hedging cost, volatility risk, inventory risk and information risk are separated, each with its source and the source's status (empirical abstract, model prediction).
- **Costs.** Quoted against effective spreads, both against timing-adjusted spreads with a fair-value benchmark; percent-of-premium against volatility units; outright against multi-leg (the BPS figures are single-leg only).
- **Market, sample and contract.** Every figure carries its market (U.S.), period (2019–2021), contract set and measure; the abstract-only findings are marked as such, with samples unread.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `ex-bryzgalova-pavlova-sikorskaya-2023` | abstract; pp. 2, 4–5, 7, 11–12, 14–17; Table I page images | U.S., 2019–2021; SLIM proxy single-leg; fees as the authors report |
| `ex-jameson-wilhelm-1992` | abstract | Full text and sample unread |
| `ex-huh-lin-mello-2015` | abstract | Model; empirical tests unread |
| `wide-muravyev-order-flow` | abstract | Full text unread |
| `wide-muravyev-pearson` | abstract | Full text unread |
| `ex-battalio-hatch-jennings-2004` | abstract | Full text unread |
| OCC and exchange rules | none | Not read; stubs |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/options-execution/derivations.tex` (1 page, no warnings or bad boxes), with only the subsection unnumbered; a script confirmed the body appears once and the four blocks once each, in order, with nothing else outside them. Earlier artefacts are unchanged.

### Counts

`migration_status.py`: 629 → 625 legacy blocks = 530 shared + 66 single-candidate + 29 assigned. `options-execution`: exclusive 4 → 0, listed entries 0 → 3 (new note), backlog stubs 0 → 2. Entries 78 → 81 (results 15 → 16, methods 13 → 14, mechanisms 5 → 6). Six reading notes added. Other listings unchanged.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 199 pages (195 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before (one overfull Status line in the new file was fixed by rephrasing); the one `page.i` warning. Rendered and inspected: PDF pp. 54 (the corrected internalisation model), 56–58 (the new options section) and 196 (the legacy asset-class section, which now starts at *Fixed Income Microstructure*). Tests: 14 passed.

### For review

- The three new options entries, and the reliance on five abstracts.
- The two backlog stubs, which need dated OCC and exchange rule documents.
- Not adopting "buy-side typically consume liquidity".

## Slice 21 follow-up: corrections, 15 October 2026

Targeted corrections to two slice-21 entries after rechecking Bryzgalova, Pavlova and Sikorskaya pp. 2, 11–12 and 14–17 and the page images of Table I (pp. 15–16); the slice-21 record above is left as written.

- `meth:option-spread-measurement`: "lowest quoted spreads" removed. At-the-money quoted spreads (8.7 percent SLIM, 8.4 percent non-SLIM) are far below those of slightly out-of-the-money trades (28.7, 21.3) but not the lowest bin: slightly in-the-money trades (0.1 to 1) have 8.6 and 5.9. Moneyness, written in Table I as (MidpointPrice − Strike)/Strike for calls, is read as using the underlying's midpoint, distinct from the option-premium midpoint used for spreads; this is labelled interpretation, since the caption does not name the underlying. SLIM is defined as the single-leg non-ISO price-improvement-auction proxy and non-SLIM as the whole remaining pool; "say nothing about spread or multi-leg costs" is replaced by the precise limit that the results do not isolate the execution costs of multi-leg strategies. The Pitfalls on "ATM deepest" now rest on trade share only.
- `res:option-market-maker-spreads` and `mech:options-retail-wholesaler-routing`: exchange-only execution is bounded to the U.S. listed-options market the authors study (their OPRA data). FINRA Regulatory Notice 22-14 (22 June 2022; `finra-rn-22-14`, added to `front/sources.tex`) is cited for its background distinction between listed (standardised) and OTC (conventional) options, OTC trades not generally being centrally cleared or reported to FINRA, the SEC, an exchange or the CAT; the notice's proposal is stated as a request for comment, not an effective rule, and its later status was not checked.
- `mech:options-retail-wholesaler-routing`: the $0.30 net rebate is tied to the responder-execution case of p. 11, footnote 15 (another market maker paying $0.50 to break up a paired order).
- The reading note for `ex-bryzgalova-pavlova-sikorskaya-2023` and the pathway note were updated; the abstract-only limits on the other five readings are unchanged. The slice-21 artefact is unchanged.

## Slice 22: fixed-income microstructure, 15 October 2026

Migration of the six-block fixed-income file, run after the follow-up above. Migration and source checking, not study; the pathway's checkpoint was not attempted.

### Scope

The whole of `execution-trading-costs/02_.../05_fixed_income_microstructure.tex`: 6 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper keeps its other two topics (securities lending, crypto).

### Ownership and dispositions

`otc-fixed-income-trading` (the map's single candidate) owns all six blocks. Its outcome is measuring what clients pay in bond, swap and FX dealer markets and explaining how RFQ and portfolio trading, transparency rules and dealer capacity change those costs; every block falls inside it. Two exceptions were considered and not taken: the dealer-capacity material could serve `bond-swap-dealer-market-making` (no note yet), and the credit-derivative and swap items could too; both are inside this pathway's outcome, so they stay here, the capacity material cross-referenced to the existing dealer entries and the swap items stubbed. The pathway sits in the section `execution-trading-costs`, so the entries are in the new topic file `compendium/execution-trading-costs/fixed-income-trading.tex`, input after `futures-execution.tex`; the chapter opener names it. Six blocks were merged into three entries by question (how the market is organised, what the rules require, what the evidence shows).

| # | Legacy block | Owner | Destination | Checked sources | Disposition |
|---|---|---|---|---|---|
| 1 | *Fixed-Income Instrument Range* (taxonomy) | `otc-fixed-income-trading` | `def:fixed-income-market-structure` (new); stub `ev:credit-derivative-swap-trading-structure` | BSV pp. 1–5, 7–8, 11, 13–16, 30, 32 | Items i–ii rewritten for U.S. Treasuries and corporate bonds (Treasury electronic share is interdealer); structured products and municipals added from the survey; items iii–iv (CDS indices against bespoke, swaps dealer-mediated) unchecked |
| 2 | *RFQ Dominance* (principle) | `otc-fixed-income-trading` | `def:fixed-income-market-structure` | BSV pp. 2–3, 7–8, 37–38; Hendershott–Madhavan and O'Hara–Zhou (abstracts) | Protocols, venues and risk-bearing separated; "dominance" not supported (19 percent electronic in U.S. IG corporates, 2016); the "because" not adopted |
| 3 | *Dealer Balance Sheet as Venue* (mechanism) | `otc-fixed-income-trading` | `def:fixed-income-market-structure` (Practice) | BSV pp. 4, 32–33 | Treated as a metaphor; reduced capital commitment, prearranged trades, nonbank dealers and the regulatory links as the survey states them |
| 4 | *TRACE and Post-Trade Transparency* (market rule) | `otc-fixed-income-trading` | `rule:us-eu-bond-transparency` (new); `ev:bond-transparency-trading-costs` ("improving") | FINRA Rules 6730, 6750 and filing pages (2026-10-15); BSV Table 2, pp. 8–10, 29–30; ESMA statement (10 Oct 2025) and manual (12 May 2026) | Reporting and dissemination separated; history, current text and the one-minute change and its supersession dated; EU post-trade deferrals from 2 March 2026; the European "aim" and U.K. regime unchecked; stubs `rule:eu-mifir-bond-transparency-level1`, `rule:uk-bond-transparency` |
| 5 | *Pre-Trade Transparency Limits* (caveat) | `otc-fixed-income-trading` | `ev:bond-transparency-trading-costs` (Conditions, Pitfalls) | BSV pp. 29, 37–39 | Kept as dealers' argument, a model prediction (Back–Liu–Teguia, as reported) and an open question; not adopted as a finding |
| 6 | *Data Changes the Market* (practitioner note) | `otc-fixed-income-trading` | `ev:bond-transparency-trading-costs` (Practice); `def:fixed-income-market-structure` (Conditions) | BSV pp. 7–10, 31–32; O'Hara–Zhou (abstract) | Split; data sources and missing 605/606 analogue stated; electronification effects only as O'Hara and Zhou's abstract reports them, not causally; desk governance unchecked |

Overlaps: `def:dealer-inventory-risk` and `meth:dealer-quote-adjustment` (generic inventory theory), `def:spread-measures`, `def:best-execution`, `meth:transaction-cost-analysis`, `def:portfolio-trading` and `mech:etf-creation-redemption` (Pan and Zeng's corporate bond ETF evidence) are cross-referenced; none was changed.

### Sources, 2026-10-15 (generic request headers)

- **Bessembinder, Spatt and Venkataraman** (`wide-bsv-fi-survey`), published JFQA version, as hosted in the SEC's fixed-income advisory committee materials, retrieved through the web-fetch tool after a direct request was refused by SEC's rate page: abstract and pp. 1–5, 7–11, 13–16, 29–33, 37–39, text layer (printed page = PDF page).
- **Abstracts only**, from the publishers' records via OpenAlex, Crossref and RePEc: Edwards, Harris and Piwowar (`wide-edwards-harris-piwowar`), Hendershott and Madhavan (`wide-hendershott-madhavan`), O'Hara and Zhou (`wide-ohara-zhou-electronic`). SSRN returned bot pages; a 2005 working-paper copy of Edwards–Harris–Piwowar returned 403; a Bank of Canada PDF found in the search was a different paper (Edwards, Nimalendran and Piwowar, 2006) and was not used.
- **FINRA** (added to `front/sources.tex`): Rule 6730 (`finra-rule-6730`) and Rule 6750 (`finra-rule-6750`) as displayed on 15 October 2026, with amendment histories; filing pages for SR-FINRA-2024-004 and SR-FINRA-2025-008 (`finra-sr-2024-004`), titles and summaries only, and SR-FINRA-2026-009 (title only). The approval orders were not read.
- **ESMA** (added): public statement No. 2 of 10 October 2025 (`esma-mifir-review-statement-2025`), p. 4; manual on pre- and post-trade transparency of 12 May 2026 (`esma-transparency-manual-2026`), pp. 24–29 and 258–272 (worked examples, Level 3 guidance).
- **Not available or not read:** Regulation (EU) 2024/791 and the amended RTS 2 (EUR-Lex returned an empty page); the Official Journal publication of the amending RTS; U.K. rules; the pathway's other readings, including portfolio trading (`wide-li-ohara-portfolio-trading`) and dealer capacity (`exp-eisfeldt-interdealer-capacity`).

### Distinctions kept

- **Segments.** U.S. Treasuries, structured products (TBA against specified pools), corporate and municipal bonds are described separately; credit derivatives and swaps are not described beyond clearing and one CDS transparency study; no corporate-bond sample is generalised to other segments.
- **Market organisation.** Trading protocols (runs, voice, RFQ, lists), venues (interdealer platforms, RFQ platforms, all-to-all) and dealer risk-bearing (principal, prearranged) are separated; "balance sheet as venue" is a metaphor.
- **Rules.** Reporting to FINRA is kept apart from public dissemination; post-trade from pre-trade; product coverage and exceptions are listed; history (2002–2017, from the survey), current text (rulebook, 15 October 2026), an approved-then-superseded change and a pending amendment are dated separately; the EU and U.K. regimes are kept apart, the latter unchecked; proposals (FIMSAC's 48-hour delay) are not presented as rules.
- **Evidence status.** Empirical associations (the TRACE phase-in studies, through the survey and one abstract), a model prediction (Back–Liu–Teguia) and interpretation are labelled; no causal claim about electronification, and no general claim that transparency helps or harms liquidity.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `wide-bsv-fi-survey` | pp. 1–5, 7–11, 13–16, 29–33, 37–39 | Survey; U.S. data to about 2018; primary studies through its summaries |
| `wide-edwards-harris-piwowar` | abstract | Full text unread |
| `wide-hendershott-madhavan` | abstract | Full text unread |
| `wide-ohara-zhou-electronic` | abstract | Full text unread |
| FINRA Rules 6730, 6750; filing pages | rule text; titles and summaries | As displayed 2026-10-15; approval orders unread; a 2027 amendment may already be displayed |
| ESMA statement, manual | p. 4; pp. 24–29, 258–272 | Level 3 guidance and examples, not the Level 1 or 2 text |
| MiFIR as amended, U.K. rules | none | Not retrievable or not checked; stubs |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/otc-fixed-income-trading/derivations.tex` (1 page, no warnings or bad boxes), with only the subsection unnumbered; a script confirmed the body appears exactly once, the six blocks once each and in order, nothing outside the blocks but the subsection heading, and nothing after the body but `\end{document}`. Earlier artefacts, `house.tex` and the guide pin (`343d145`) are unchanged; earlier log entries and open questions were only appended to.

### Counts

`migration_status.py`: 625 → 619 legacy blocks = 530 shared + 60 single-candidate + 29 assigned. `otc-fixed-income-trading`: exclusive 6 → 0, listed entries 0 → 3 (new note), backlog stubs 0 → 3. Entries 81 → 84 (definitions 29 → 30, evidence 4 → 5, rules 0 → 1). Four reading notes added; five sources and the slice-21 follow-up's FINRA notice added to `front/sources.tex`. `options-execution` unchanged at 3 entries and 2 stubs.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 203 pages (199 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 57–58 (the corrected options entries), 95, 97–98 (the new fixed-income section) and 200 (the legacy asset-class section, which now starts at *Securities Lending and Synthetic Shorts*). Tests: 14 passed.

### For review

- The three new fixed-income entries, and the reliance on one survey plus three abstracts.
- The rule entry's reading of SR-FINRA-2024-004 and SR-FINRA-2025-008 from their filing summaries.
- The three backlog stubs (credit derivatives and swaps, EU Level 1 text, U.K.).

## Slice 22 follow-up: corrections, 15 October 2026

Targeted corrections to `compendium/execution-trading-costs/fixed-income-trading.tex`; the slice-22 record above is left as written.

- `def:fixed-income-market-structure`: the 19 percent figure is now an estimate in an industry report published in July 2016, as the survey cites it (p. 2); the observation period behind it is not given, and the publication date is no longer presented as one.
- `ev:bond-transparency-trading-costs`: Edwards, Harris and Piwowar's conclusion keeps the abstract's wording, that the results "suggest that public traders benefit significantly from price transparency".
- `rule:us-eu-bond-transparency`: SR-FINRA-2026-009 rechecked against the SEC approval order (Release No. 34-105991, 24 July 2026, 91 FR 47909–47911; `sec-34-105991`, added to `front/sources.tex`). The presently effective exclusion suppresses from dissemination qualifying same-day, same-price, same-security transactions between a member and its non-member affiliate; the amendment extends it to member affiliates and renames the indicator the Affiliate—Principal Transaction indicator, with an implementation date of at least 12 months after approval (listed as 2 August 2027) and voluntary earlier use. The rulebook's displayed Rule 6750(d)(1), "Affiliate—principal transaction indicator", is named as the future wording.
- `ev:bond-transparency-trading-costs`: "markup disclosure for riskless principal trades" replaced, after rechecking FINRA Rule 2232 (`finra-rule-2232`) and Regulatory Notice 17-08 (`finra-rn-17-08`, both added): since 14 May 2018, Rule 2232(c) requires the mark-up or mark-down on the confirmation when the member trades as principal in a corporate or agency debt security with a non-institutional customer and makes same-trading-day offsetting trades of at least that size, looking through non-arm's-length affiliate trades; (d) exempts functionally separate trading desks and same-day fixed-price-offering sales. FINRA's notice reports a parallel MSRB rule with the same effective date; MSRB's own text was not read, so the municipal statement is attributed to FINRA.
- Layout: the follow-up added about fifteen lines to the evidence entry, so its continuation page (PDF p. 99 before, p. 104 after slice 23) now carries the end of Pitfalls, See also, Further reading, Index and Status (18 text lines) and is no longer near-empty; removing it would require cutting evidence or status text, so it was kept. `house.tex` is unchanged.
- The reading notes for `wide-bsv-fi-survey` and `wide-edwards-harris-piwowar` and the pathway note were updated. Earlier artefacts and the options corrections are unchanged.

## Slice 23: securities lending and synthetic shorts, 15 October 2026

Migration of the six-block securities-lending file, run after the follow-up above. Migration and source checking, not study; no checkpoint was attempted.

### Scope

The whole of `execution-trading-costs/02_.../06_securities_lending_and_synthetic_shorts.tex`: 6 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper keeps its last topic (crypto).

### Ownership and dispositions

The map names `synthetic-equity-cfd-trs`, whose outcome is pricing CFDs and equity total return swaps from financing, dividend, borrow and margin terms and identifying their counterparty, disclosure and tax exposures. Its prerequisite `money-markets-repo-lending` has the outcome of distinguishing repo from securities lending and pricing collateral financing, with the ICMA FAQ, Duffie–Gârleanu–Pedersen and the ISLA handbook as readings. **Routing exception:** blocks 1–4 and 6 describe the lending market itself (custody, the loan, availability, rebates, the votes of lent shares) and belong to `money-markets-repo-lending`; block 5, a synthetic position replacing borrow, stays with `synthetic-equity-cfd-trs`. Derivative-based empty voting and beneficial-ownership disclosure, which do belong to `synthetic-equity-cfd-trs`, are stubbed there. Both pathways sit in the section `portfolio-risk-financing`, which had no chapter; this slice opened `compendium/portfolio-risk-financing/` (`section.tex`, `securities-lending.tex`, `synthetic-shorts.tex`). The artefact sits under the map candidate, `notes/artefacts/synthetic-equity-cfd-trs/`, keeping the file whole, as in slices 17 and 18.

| # | Legacy block | Owner | Destination | Checked sources | Disposition |
|---|---|---|---|---|---|
| 1 | *Street Name* (definition) | `money-markets-repo-lending` | `def:street-name-beneficial-ownership` (new) | Harris pp. 148, 169–170 | Rewritten; registration, beneficial ownership, custody and permission to lend separated |
| 2 | *Securities Lending* (mechanism) | `money-markets-repo-lending` | `mech:securities-lending-short-sale` (new) | DGP sec. 2, pp. 5–8; ICMA FAQ 13; ISLA pp. 2–3, 24–25; 17 CFR 242.203(b), 242.204(a); Harris pp. 155, 158 | Rewritten; locate, borrow, delivery, recall, replacement borrow, buy-in; Regulation SHO as current U.S. law, ISLA as practice |
| 3 | *Borrow Availability Segmentation* (taxonomy) | `money-markets-repo-lending` | items i–ii `def:securities-lending-fee-rebate` (new); items iii–iv `mech:securities-lending-short-sale` | Harris pp. 156–158; DGP pp. 6–8; Regulation SHO | Split; recall and settlement risk reclassified as operational risks; "failed locate" separated from delivery failure |
| 4 | *Short Interest Rebate* (definition) | `money-markets-repo-lending` | `def:securities-lending-fee-rebate` | ICMA FAQ 13; DGP p. 7; ISLA pp. 7–8; Harris pp. 155–157 | Corrected: cash collateral passes from the borrower (often the broker) to the lender; customer margin separated; negative rebates not exemplified in sources |
| 5 | *Synthetic Short* (principle) | `synthetic-equity-cfd-trs` | `res:synthetic-short-put-call` (new) | Harris p. 157; Hu–Black p. 5, fn. 6; own derivation and numerical check | Payoff, initial value with dividends, short forward against short stock, American exercise and assignment; "can replace scarce borrow" qualified, not adopted |
| 6 | *Voting and Beneficial Ownership* (caveat) | `money-markets-repo-lending` | `def:street-name-beneficial-ownership` (Conditions, Practice, Pitfalls); stub `ev:empty-voting-equity-derivatives` (`synthetic-equity-cfd-trs`) | Harris p. 169; ICMA FAQ 13; DGP p. 8; Hu–Black pp. 1, 5 | Kept as Harris's description of broker voting; record holders vote; no duplicate legal votes; record-date capture through borrowing kept apart from swap-based decoupling |

Overlaps checked: no existing entry covered securities lending, street name or put–call parity. `def:arbitrage`, `res:arbitrage-risks`, `res:option-market-maker-spreads`, `meth:option-spread-measurement`, `mech:futures-margin-settlement` and `def:broker-agency-conflicts` are cross-referenced; none was changed.

### Sources, 2026-10-15 (generic request headers)

- **Harris** (`alpha-harris`), 2002 Oxford printing, local copy, text layer: chap. "Brokers", sec. 7.2.2.2 (p. 148), secs. 7.3.1.4 and 7.3.1.7 with the box "Synthetic Short Positions" (pp. 155–158), the box "Can Investors Vote More Than 100 Percent of the Shares Outstanding?" and sec. 7.5.6.1 (pp. 169–170).
- **Duffie, Gârleanu and Pedersen** (`al-duffie`), NYU Stern working paper FIN-01-023, version of 24 September 2001 (10-page file): abstract and sec. 2, pp. 5–8. The published JFE version was not read.
- **ICMA ERCC Repo FAQ 13** (`al-icma`), living page as retrieved.
- **ISLA Securities Lending Best Practice** (`al-isla`), 29-page compilation dated 31 March 2025, pages as images, read by macOS Vision OCR and page images: pp. 2–3, 7–8, 14–16, 23–26.
- **Regulation SHO** (added: `cfr-242-203`, `cfr-242-204`): 17 CFR 242.203(b) and 242.204(a) on eCFR, version of 13 October 2026.
- **Hu and Black** (`cfd-hu-black-2007`), ECGI Law Working Paper 056/2006, whose first pages carry another paper's cover text in the text layer: abstract, p. 1, sec. 2.2.3 and footnote 6, p. 5 (checked by page image). The published version was not read.
- **Not available or not read:** Hull (`s7-hulloptions`), so put–call parity rests on an own derivation; OCC or exchange documents on listed option exercise style, settlement and multiplier; Regulation T and FINRA margin rules as current; U.S. proxy-processing rules; the 2023 SEC beneficial-ownership rule (`cfd-sec-13d-2023`); other jurisdictions' rules.

### Distinctions kept

- **Ownership.** Holder of record, beneficial owner, custody and permission to lend; economic exposure against the legal vote; record dates; recall to vote; securities-lending vote transfer against derivative-based empty voting and disclosure (stubbed).
- **Contracts.** Broker–customer arrangements (margin agreement, short proceeds, customer margin) against the institutional loan (master agreement, collateral, rebate, recall, claims).
- **Lifecycle.** Locate (a belief or arrangement under Rule 203(b)), completed borrow, delivery, fail and close-out (Rule 204(a)), recall, replacement borrow, buy-in.
- **Availability against operations.** General collateral and specials against locate, delivery, recall and return failures.
- **Economics.** Cash against non-cash collateral; fee against rebate (fee implicit in the rebate); reinvestment return; broker rebate spread; customer margin.
- **Synthetic short.** European payoff identity and initial value; matching strike, maturity, underlying, multiplier and settlement; short forward against short stock with upfront premium, financing and dividends; American early exercise and assignment; no guaranteed access to scarce borrow.
- **Law against practice.** Regulation SHO (U.S., eCFR October 2026) is law; ISLA's handbook is practice that yields to the GMSLA and local codes; Harris and DGP describe 2001–2002 U.S. practice.

### Numerical check

Own script, Black–Scholes prices with $S_0=100$, $K=95$, $r=5\%$, $q=2\%$, $\sigma=25\%$, $T=1$: $C=13.6847$, $P=6.0317$, $P-C=-7.6531=Ke^{-rT}-S_0e^{-qT}=e^{-rT}(K-F)$ with $F=103.0455$; payoff $K-S_T$ at $S_T=60, 95, 100, 140$; terminal wealth of the financed package $F-S_T$, equal to a short sale of $e^{-qT}$ shares with rebate $r_b=r$ ($3.0455$ at $S_T=100$) and not with $r_b=3\%$ ($1.0050$).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | pp. 148, 155–158, 169–170 | U.S., 2002 |
| `al-duffie` | abstract; sec. 2, pp. 5–8 | 2001 working paper |
| `al-icma` | FAQ 13 | Living page; European practice association |
| `al-isla` | pp. 2–3, 7–8, 14–16, 23–26 | OCR of images; sections "Under Review"; practice, not law |
| Regulation SHO | 242.203(b), 242.204(a) | U.S. only; eCFR 13 October 2026 |
| `cfd-hu-black-2007` | abstract, pp. 1, 5 | Working paper; its Regulation T statement unchecked |
| Hull, OCC, margin, proxy rules | none | Not available or not checked; stubs |

The four new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/synthetic-equity-cfd-trs/derivations.tex` (1 page, no warnings or bad boxes), with only the subsection unnumbered; a script confirmed the body appears exactly once, the six blocks (Street Name, Securities Lending, Borrow Availability Segmentation, Short Interest Rebate, Synthetic Short, Voting and Beneficial Ownership) once each and in order, nothing outside the blocks but the subsection heading, and nothing after the body but `\end{document}`. Earlier artefacts, `house.tex` and the guide pin (`343d145`) are unchanged; earlier log entries and open questions were only appended to.

### Counts

`migration_status.py`: 619 → 613 legacy blocks = 530 shared + 54 single-candidate + 29 assigned. `synthetic-equity-cfd-trs`: exclusive 6 → 0, listed entries 0 → 1, backlog stubs 0 → 2. `money-markets-repo-lending`: entries 0 → 3, stubs 0 → 2. Entries 84 → 88 (definitions 30 → 32, mechanisms 6 → 7, results 16 → 17). Two pathway notes and four reading notes added, `alpha-harris` updated; five sources added in this follow-up and slice (`finra-rule-2232`, `finra-rn-17-08`, `sec-34-105991`, `cfr-242-203`, `cfr-242-204`).

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 207 pages (203 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 16–20 (the new chapter, its continuation and closing pages), 97–99 and 104 (the slice-22 follow-up and the fixed-income continuation page) and 205 (the legacy asset-class section, now only *Crypto Market Microstructure*). Tests: 14 passed.

### For review

- The routing of five blocks to `money-markets-repo-lending` against the map, and the new `portfolio-risk-financing` chapter.
- The synthetic-short entry's reliance on an own derivation in place of Hull.
- The four backlog stubs.

## Slice 23 follow-up: corrections, 15 October 2026

Targeted corrections to two slice-23 entries; the slice-23 record above is left as written, including its numerical-check paragraph, which this record supersedes for the short-sale comparison.

- `res:synthetic-short-put-call`, bond replication. Harris's sidebar on p. 157, rechecked by page image (PDF p. 170 of the local copy, rendered through PDFKit), says a long put and a short call ``plus a long position in a bond with the same maturity'' are equivalent to a short position in the underlying. With a long bond paying $K$ the terminal payoff is $2K-S_T$. The entry now states the correct replication: long put, short call and a short zero-coupon bond repaying $K$ pay $-S_T$; for a stock with no dividends the initial values agree ($P-C-Ke^{-rT}=-S_0$), so the package is equivalent to short stock; equivalently, long put and short call equal short stock plus a long bond (a short sale with proceeds invested). With dividends, the package less the bond is a terminal claim $-S_T$ worth $-S_0e^{-qT}$, while short stock is worth $-S_0$ and owes the interim dividends. Harris's wording is quoted as printed and the discrepancy recorded. The European payoff identity and dividend-adjusted parity are unchanged.
- `res:synthetic-short-put-call`, short-sale comparison. The slice-23 bullet compared the package with a fixed short of $e^{-qT}$ shares and gave it terminal wealth $S_0e^{-qT}e^{r_bT}-S_T$; with the borrower paying dividends that is not the strategy's terminal wealth. The narrow repair uses $q=0$: one share sold short, the whole proceeds held as cash collateral credited at a constant rebate $r_b$ (lending fee implicit in $r_b$, no other fee, no extra margin, no recall), ends with $S_0e^{r_bT}-S_T$; the package, European options priced at frictionless parity and its premium financed or invested at $r$, ends with $S_0e^{rT}-S_T$. The existing $q=2\%$ Black–Scholes parity example is kept and labelled separately.
- `mech:securities-lending-short-sale`: ``so someone must lend them'' replaced by the standard stock-loan route for delivery at settlement, with two cases where no loan is needed: delivery from securities held in street name for other clients (Harris, p. 155) and Regulation SHO's exception for sales of securities the seller is deemed to own (17 CFR 242.203(b)(2)(ii)).
- **Numerical checks**, added as `notes/artefacts/synthetic-equity-cfd-trs/synthetic_short_checks.py` (standard library; `derivations.tex` unchanged). (1) Payoffs leg by leg at $S_T=60, 95, 100, 140$: put minus call $=K-S_T$; with a short bond $=-S_T$; with a long bond $=2K-S_T$ (130, 95, 90, 50). (2) Parity example $S_0=100$, $K=95$, $r=5\%$, $q=2\%$, $\sigma=25\%$, $T=1$: options repriced by midpoint integration over the risk-neutral density, $C=13.684728$, $P=6.031656$, matching the closed forms to $10^{-4}$, and $P-C=-7.653072=Ke^{-rT}-S_0e^{-qT}=e^{-rT}(K-F)$ with $F=103.0455$. (3) Rebate comparison, $q=0$, same $S_0$, $K$, $r$, $\sigma$, $T$: $C=15.0471$, $P=5.4138$, $P-C=-9.6332$; day-by-day accounts give the package $S_0e^{rT}-S_T$ (5.127110 at $S_T=100$) and the short sale $S_0e^{r_bT}-S_T$ (5.127110, 3.045453, $-0.995017$ for $r_b=5\%, 3\%, -1\%$), gaps $S_0(e^{rT}-e^{r_bT})=0$, 2.081656, 6.122126 at every $S_T$. All checks passed.
- The pathway note for `synthetic-equity-cfd-trs`, the `alpha-harris` reading note and the log were updated. Ownership, stubs and counts are unchanged (613 legacy blocks; 88 entries).

## Slice 23 second follow-up: lending opening, 15 October 2026

`mech:securities-lending-short-sale` now opens with the standard stock-loan route only: a short seller sells securities it does not own and borrows them to meet delivery at settlement. The examples added in the first follow-up, delivery from other clients' street-name holdings (Harris, p. 155) and Regulation SHO's deemed-to-own locate exception (§ 242.203(b)(2)(ii)), were removed as explanations of why a loan is unnecessary: delivering another customer's street-name securities does not show that no lending occurs, and a locate exemption is a separate regulatory question. The Regulation SHO conditions stay in the entry's Conditions. The synthetic-short mathematics and `synthetic_short_checks.py` are unchanged and still pass. The first follow-up record above is left as written.

## Slice 24: crypto market microstructure, 15 October 2026

Migration of the four-block crypto file, the last topic of the legacy execution-trading-costs chapter, run after the clarification above. Migration and source checking, not study; no checkpoint was attempted.

### Scope

The whole of `execution-trading-costs/02_.../07_crypto_market_microstructure.tex`: 4 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its map row and both wrappers that input it were deleted: `02_.../00_overview.tex` (a section heading and this one `\input`) and `execution-trading-costs/section.tex` (the legacy chapter heading with label `legacy:execution-trading-costs`, a comment and one `\input`); both are kept verbatim as display text (`verbatim`) in the artefact, so their inputs do not execute. The line `\InputIfFileExists{legacy/execution-trading-costs/section}{}{}` was removed from `compendium/legacy/part.tex`. The 21 unused PNGs in `compendium/legacy/execution-trading-costs/figures/` were left unchanged; `tools/migration_status.py` now requires a `part.tex` input only for legacy folders that still contain `.tex` files, so the figures-only folder passes (the 14 tests pass unchanged).

References to `legacy:execution-trading-costs` were updated: the comment and the closing sentence of `compendium/execution-trading-costs/section.tex` (all its older notes are now migrated; the impact material remains in the legacy execution-market-making chapter), and the overview paragraph of `compendium/legacy/execution-market-making/section.tex` (algorithmic execution and asset-class microstructure have been migrated). No other `.tex` reference remained; earlier records in this file keep the label as history.

### Ownership and dispositions

The map names `crypto-mm-microstructure`, whose outcome is estimating the fee, impact, latency and adverse-selection terms of quoting one crypto order book from the venue's own data. None of the four blocks is about that. `crypto-perpetuals` has the outcome of reconciling spot, perpetual and dated-futures basis with financing, transfer, margin and liquidation paths across fragmented venues, and its readings include Makarov–Schoar, the perpetual-pricing papers and Deribit's rulebook and funding specification. **Routing exception:** all four blocks go to `crypto-perpetuals`. Items outside its outcome were not given entries: options (`crypto-options-numeraire`), AMM pools (`amm-lending`) and stablecoin, network and bridge risk (`stablecoin-pegs-runs` and the section overview) are stubbed in the `crypto-perpetuals` note with their destination named. `crypto-price-discovery` was considered for block 1 (cross-exchange gaps) but its readings were not used and its outcome centres on information shares and reference rates. The pathway sits in the section `digital-assets-prediction-markets`, which had no chapter; this slice opened `compendium/digital-assets-prediction-markets/` (`section.tex`, `crypto-venues-perpetuals.tex`). The artefact sits under the map candidate, `notes/artefacts/crypto-mm-microstructure/`, keeping the file whole, as in slices 17, 18 and 23.

| # | Legacy block | Owner | Destination | Checked sources | Disposition |
|---|---|---|---|---|---|
| 1 | *Crypto Liquidity Is Exchange-Fragmented* (principle) | `crypto-perpetuals` | `def:crypto-venue-instrument-structure` (new) | Makarov–Schoar DP 782, abstract, pp. 1–3; Deribit Rulebook v2.0 | Rewritten; executable prices, reference prices, fair value and legal best execution separated; 2017–2018 evidence dated; "fair value is venue-dependent" and the consolidated-tape claim not adopted |
| 2 | *Crypto Instrument Segmentation* (taxonomy) | `crypto-perpetuals` | `def:crypto-venue-instrument-structure`; perpetual item to `mech:perpetual-funding`; stubs `def:crypto-options-venue-structure`, `def:amm-pool-mechanics` | Ackerer–Hugonnier–Jermann arXiv v2, pp. 2–3, 7; Deribit Rulebook Rules 1.2, 11.3, App. A | Spot, dated futures, perpetuals (linear, inverse, quanto) and Deribit's options checked; "kept near spot" qualified; options concentration and pool mechanics unchecked |
| 3 | *Perpetual Funding* (definition) | `crypto-perpetuals` | `mech:perpetual-funding` (new); stub `ev:crypto-funding-crowding` | AHJ pp. 2, 4, 7–8, 12; He et al. v7 abstract; Deribit Funding Specifications; Rule 11.4 | Sign convention confirmed (Deribit); anchoring a model result, not guaranteed; one venue's damper, caps, accrual and settlement; "crowding signal" unsupported |
| 4 | *Crypto Microstructure Risk Segmentation* (taxonomy) | `crypto-perpetuals` | `def:crypto-trading-risk-layers` (new); stub `ev:stablecoin-network-settlement-risk` | Deribit Rulebook Rules 1.1, 2, 10.1–10.11, definitions | Liquidation, insurance fund, socialised loss, ADL and custody for Deribit only; insolvency, outages, withdrawal halts, stablecoin and bridge risk unchecked; fragmentation moved to block 1's entry |

Overlaps checked: no existing entry covered crypto. `def:best-execution`, `def:smart-order-routing`, `def:fx-market-structure`, `res:arbitrage-risks`, `mech:futures-margin-settlement` and `def:securities-lending-fee-rebate` are cross-referenced; none was changed.

### Sources, 2026-10-15 (generic request headers)

- **Makarov and Schoar** (`s6-makarov`), LSE FMG Discussion Paper 782, 15 December 2018, from fmg.ac.uk: abstract and pp. 1–3 with footnotes 1–3, text layer (printed page = PDF − 2). The published JFE version was not read.
- **Ackerer, Hugonnier and Jermann** (`roadmap-perpetual-pricing`), arXiv 2310.11771v2, 3 September 2024: abstract and pp. 2–4, 7–8 (eqs. (4)–(7)) and 12 (Corollary 1), text layer (printed page = PDF page). The Mathematical Finance version was not read.
- **He, Manela, Ross and von Wachter** (`roadmap-perpetual-fundamentals`), arXiv 2212.06888v7, 17 September 2026: abstract and title page only (one author's eToro affiliation disclosed there).
- **Deribit** (`gapclose-deribit-rules`): Exchange Rulebook version 2.0, applicable 13 August 2026 (article updated 15 September 2026), and Funding Specifications (edited 27 July 2026, updated 20 August 2026), retrieved through the help-centre JSON API because the web pages returned a bot check. Rulebook locators are rule numbers (no page numbers); the funding cap table was read from the article's HTML table. Exchange Membership Terms, option and portfolio-margin pages not read.
- **Not available or not read:** the BIS carry paper (`roadmap-carry`; the PDF URL returned an HTML page), Gornall–Rinaldi–Xiao (`s11-r15`; SSRN), the `crypto-mm-microstructure` readings (none supports these blocks), `s11-r29` venue API documentation, and any AMM, stablecoin or bridge source.

### Distinctions kept

- **Evidence, rules and interpretation.** Makarov–Schoar's 2017–2018 findings; Deribit's October 2026 rules for one venue; Ackerer–Hugonnier–Jermann's and He et al.'s model results; interpretation labelled.
- **Prices.** Executable venue prices, reference indices (Deribit Index, Mark Price), fair-value models and legal best-execution obligations.
- **Instruments and contracts.** Spot, dated futures, perpetuals, options and AMM pools (the last unchecked); linear, inverse and quanto contracts.
- **Funding.** Premium against interest terms; sign convention; continuous accrual against the 8-hour quotation; settlement currency and units; damper and caps by currency; equity against cash at the 08:00 UTC settlement.
- **Risk layers.** Liquidation, insurance fund, socialised loss, auto-deleveraging and custody (Deribit), kept apart from venue insolvency and from stablecoin, network and bridge risk (unchecked).

### Numerical check

`notes/artefacts/crypto-mm-microstructure/funding_checks.py` (standard library): Deribit's printed max/min funding formula agrees with an independent piecewise reading of its prose rule at every premium from −10% to +10% in 0.005% steps, for each cap; all of Deribit's worked examples recompute (BTC 0.05% per 8 hours, 0.000001041667 BTC per minute and 0.0005 BTC per 8 hours for 1 BTC; ETH 0.075%, 0.0000015625 and 0.00075 ETH; SOL_USDC 0.075%, 0.15625 and 75 USDC on USDC 100,000; offsetting minutes net to zero; damper examples zero; caps 0.5%, 1.0% and 5.0% binding; ETH uncapped 1.975%); and funding between long and short nets to zero. The page's slips (ETH Example 3 "Index remains at USD 10,000" and "1 BTC long position"; 7.5% inside the ETH formula of Example 5) do not change its stated results. All checks passed.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s6-makarov` | abstract; pp. 1–3 | 2018 discussion paper; 2017–2018 data |
| `roadmap-perpetual-pricing` | abstract; pp. 2–4, 7–8, 12 | Preprint; frictionless model |
| `roadmap-perpetual-fundamentals` | abstract | Body unread |
| `gapclose-deribit-rules` | Rulebook rules and definitions; Funding Specifications | One venue; October 2026; Membership Terms unread |
| `roadmap-carry`, `s11-r15`, AMM, stablecoin, bridge | none | Not retrieved or not in scope; stubs |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/crypto-mm-microstructure/derivations.tex` (1 page; no warnings or bad boxes after setting the wrapper text in `\scriptsize` and a ragged-right path line), with only the subsection unnumbered. A script confirmed, against the committed originals, that the body appears exactly once, the four blocks (Crypto Liquidity Is Exchange-Fragmented, Crypto Instrument Segmentation, Perpetual Funding, Crypto Microstructure Risk Segmentation) once each and in order, nothing outside the blocks but the subsection heading, and each deleted wrapper verbatim exactly once inside a `verbatim` environment. Earlier artefacts, `house.tex`, the guide pin (`343d145`) and the 21 figures are unchanged; earlier log entries and open questions were only appended to.

### Counts

`migration_status.py`: 613 → 609 legacy blocks = 530 shared + 50 single-candidate + 29 assigned. `crypto-mm-microstructure`: exclusive 4 → 0, no entries. `crypto-perpetuals`: entries 0 → 3, backlog stubs 0 → 5 (new note). Entries 88 → 91 (definitions 32 → 34, mechanisms 7 → 8). Four reading notes added; no new `front/sources.tex` keys (all sources are catalogue keys).

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 210 pages (207 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF p. 65 (the execution-trading-costs opener), pp. 105–108 (the new chapter and its last page), p. 109 (the part page for notes awaiting migration) and p. 167 (the legacy execution-market-making opener, now the last legacy chapter). Tests: 14 passed; `synthetic_short_checks.py` and `funding_checks.py` pass.

### For review

- Routing all four blocks to `crypto-perpetuals` against the map, and the new `digital-assets-prediction-markets` chapter.
- The checker change for figures-only legacy folders.
- The five backlog stubs, three of which name other pathways.

## Slice 24 follow-up: socialised-loss trigger, 15 October 2026

A narrow correction to one item of `def:crypto-trading-risk-layers`; the slice-24 record above is left as written.

- **Source rechecked.** Deribit FZE Exchange Rulebook version 2.0, applicable 13 August 2026 (help-centre article updated and edited 15 September 2026, unchanged since slice 24), retrieved again on 15 October 2026 through the help-centre JSON API: Rules 10.6–10.11 with their guidance notes, and Rules 9.16–9.17 for comparison.
- **Finding.** Slice 24 wrote that socialised loss applies "if the fund is depleted". Rule 10.8 has two branches: the insurance fund is depleted in all currencies, **or** it is depleted in the bankrupt account's currency and Deribit decides not to convert other currencies. In either case Deribit "may, in its absolute discretion" trigger the mechanism. Converting another currency of the fund under Rule 10.7 is also at its absolute discretion. Socialised loss can therefore be triggered while other currencies remain in the fund, and is not automatic when the fund is exhausted.
- **Changed.** The *socialised loss* item now states both branches and both discretions (Rule 10.8), with the deductions, halts, cancellations and mark-price closes cited to Rules 10.9–10.11 rather than 10.8–10.11. It also records "the same day's session" and "in any currency" as Rule 10.9(a) words them. The *insurance fund* item now says that conversion is discretionary and applies when the fund in the account's currency is depleted. The entry's status records the recheck; verification stays *partly checked*, stability *draft*, currency *Deribit as of October 2026*.
- **Notes.** The `gapclose-deribit-rules` reading note records the two-branch trigger. It also notes that Rule 9.17 applies the same trigger to a short spot under cross-collateral margin, read but not used in an entry. The `crypto-perpetuals` pathway note records the correction. No other entry, stub, ownership or count changed; `funding_checks.py` is unaffected and was not rerun.

## Slice 25: research and backtest evaluation, 15 October 2026

Migration of the four-block research file of Narang's systematic-investing chapter, run after the slice-24 follow-up above. Migration and source checking, not study; no checkpoint was attempted, and no reading of the owning pathway was read.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/research.tex`: 4 counted blocks (one `definition`, three `remark`s) with their 21 items. Outside them was only the `% migrate-to:` line and the subsection heading (checked by script). The file and its map row were deleted. In `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment naming the destinations. The legacy chapter's other files, `sysinv/modelrisk.tex` included, are unchanged, as are earlier artefacts, the 21 PNGs, `house.tex` and the guide pin (`343d145`).

### Ownership and dispositions

The map names only `research-engineering-validation`, a **section overview**. Its outcome is reconstructing a research decision and its trade from versioned identities, data events, experiments and control records; its readings are GLEIF, CRSP CIZ, CDM, FIX, bitemporal data, DDIA, MLflow and BCBS 239. None of the four blocks is about that. The specialist pathways were compared:
- `backtest-inference`: reporting a strategy result with the number of trials, multiplicity-adjusted significance and Sharpe-ratio uncertainty. Its readings include p-hacking incentives, a backtesting protocol, Sharpe-ratio statistics and leakage and look-ahead audits.
- `point-in-time-data`: research panels whose every field was available at decision time.
- `model-governance-controls`: model inventory, validation and pre-trade controls.
- `reproducible-research-code`: rebuildable research packages.

**Routing exception:** all four blocks go to `backtest-inference`. They concern forming hypotheses and judging backtests, which that pathway owns, although its statistics are not in the blocks. Historical borrow availability is stubbed with `point-in-time-data` named as its home. Nothing was routed to `model-governance-controls` or `reproducible-research-code`. The pathway had no note; this slice opened `notes/pathways/backtest-inference.md` and the topic file `compendium/research-engineering-validation/backtest-evaluation.tex`. The artefact sits under the map candidate, `notes/artefacts/research-engineering-validation/`, keeping the file whole, as in slices 17, 18, 23 and 24.

| # | Legacy block | Owner | Destination | Checked source (`s7-narang`, 3rd ed.) | Disposition |
|---|---|---|---|---|---|
| 1 | *Scientific Method* (definition) | `backtest-inference` | `meth:hypothesis-driven-strategy-research` (new) | sec. 9.1, pp. 161–163 | Rewritten; Narang's deduction of consequences and falsification restored, missing from the legacy three steps; ongoing research added |
| 2 | *Sources of Alpha Idea Generation* (remark) | `backtest-inference` | merged into `meth:hypothesis-driven-strategy-research` | sec. 9.2, pp. 163–165 | Merged; four sources match; Narang's caveat on discretionary patterns added; source of an idea not evidence (interpretation) |
| 3 | *Model Quality Assessment* (remark), items i–ix | `backtest-inference` | `meth:backtest-evaluation-diagnostics` (new); stubs | secs. 9.3.2.1–9.3.2.9, pp. 168–176; Exhibits 9.2–9.3 by page image | Rewritten with qualifications (subclaims below) |
| 3 | same block, items x–xi | `backtest-inference` | `pit:parameter-overfitting` (new); stubs | secs. 9.3.2.10–9.3.4, pp. 176–185; Exhibit 9.5 by page image | Rewritten; underfitting balance added; "flatter curve" corrected |
| 4 | *Other Considerations in Model Testing* (remark) | `backtest-inference` | `pit:backtest-cost-short-assumptions` (new); stub `data:historical-borrow-availability` | sec. 9.3.5, pp. 185–186 | Rewritten; cost asymmetry matches; "naked short … illegal" not adopted; borrow fees and recall linked as interpretation |

**Subclaims of block 3.**

| Item | Legacy claim | Disposition |
|---|---|---|
| i | Profit curve not smooth, long inactivity, sharp moves: "the model may have issues" | Rewritten as Narang's reading of his S&P example (p. 168); qualified in Pitfalls: consistency not always the goal (p. 169); smoothness can come from stale valuations (`meth:relative-performance-evaluation`) or unrealised tail losses (convertible arbitrage, p. 170) |
| ii | Average annual return | Rewritten (p. 168), with the example's 12.1% before costs |
| iii | "The less variable … the better"; lumpiness | Rewritten with Narang's condition "for a given level of returns" restored (p. 169); lumpiness as his firm's statistic; his "67 percent" within one standard deviation noted as roughly normal (68%) |
| iv | Lower drawdown and shorter recovery better | Rewritten (pp. 169–170); sample bias and resampling added; shuffle loses serial dependence (interpretation); stub `meth:dependent-resampling-drawdowns` |
| v | "Exceedingly high R² would be 0.05 out of sample"; decile buckets | Rewritten as Narang's unsourced practitioner judgement ("superb", p. 171), with no horizon, asset or design; stub `ev:out-of-sample-r2-scale`. Buckets: monotonicity (p. 172); the text–figure mismatch of Exhibit 9.3 recorded |
| vi | Winning trades and periods | Rewritten (pp. 172–173) |
| vii | Sharpe, information, Sterling, "Calmer", Omega ratios | Rewritten with Narang's own definitions (pp. 173–174); his zero-benchmark IR and downside-deviation Sterling flagged as differing from other usage (not checked); "Calmer" corrected; stubs `meth:sharpe-ratio-standard-error`, `meth:deflated-sharpe-ratio` |
| viii | Relationship with other strategies | Rewritten (p. 174) |
| ix | Time decay; "crowdedness of strategy" | Rewritten (pp. 174–176); crowding is Narang's inference, not identified by delay (his MSFT move is a public announcement; his S&P signal improves with delay); stub `ev:signal-decay-crowding` |
| x | Small parameter changes; else overfitted | Rewritten (p. 176); stability of nearby parameters is not a correction for the number of trials (interpretation); stub `meth:multiple-testing-control` |
| xi | "Flatter curve with no jumps"; parsimony means less overfitting | Rewritten as Narang's plateau with margins, point B (Exhibit 9.5, pp. 177–179); parsimony with Einstein's caveat; third-edition underfitting balance (pp. 180–183); burning out-of-sample data (pp. 183–185); stub `meth:backtest-protocol` |

**Subclaims of block 4.** Overestimated costs mean holding too long and underestimated costs mean too much turnover and bleed (p. 186): rewritten. Narang's advice to err high, and his 55/45 example, were added and the example recomputed. Short availability and hard-to-borrow lists (p. 186): rewritten. Narang's "naked short sale, which is illegal in the United States" is broader than Regulation SHO as cited in `mech:securities-lending-short-sale` and was not adopted. His remark that historical hard-to-borrow data are hard to obtain was stubbed (`data:historical-borrow-availability`). Borrow fees and recall are not in Narang or the legacy; they are linked to `def:securities-lending-fee-rebate` and `mech:securities-lending-short-sale` as interpretation. No subclaim was deleted outright.

**Existing entries checked.** `meth:automated-trading-operational-controls` covers production controls, not research, so it was not linked. `meth:relative-performance-evaluation` (smoothed returns), `meth:transaction-cost-analysis`, `def:transaction-costs`, `mech:securities-lending-short-sale` and `def:securities-lending-fee-rebate` are cross-referenced from the new entries. None was changed, since no block duplicated their content.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box: A Simple Guide to Systematic Investing*, third edition, Wiley 2024 (ISBN 9781119931911), local PDF outside the repository, read through PDFKit's text layer: chap. "Research", secs. 9.1–9.4, pp. 161–187 (printed page = PDF page − 20). Exhibits 9.2 (p. 171), 9.3 (p. 172) and 9.5 (p. 178) were read from page images. The catalogue's entry carries the first edition's subtitle and leaves the edition unestablished; no route lists the key. Which edition the legacy notes followed is not recorded (open question in `log.md`).
- **Not read:** every reading of `backtest-inference`; `wide-campbell-thompson`, `s7-welch` and the crowding papers named in stubs; standard definitions of the information, Sterling and Omega ratios. Regulation SHO was not rechecked: the comparison uses the text already cited in `mech:securities-lending-short-sale` (eCFR, 13 October 2026).

### Findings

- **Text–figure mismatch, p. 172.** The text gives the two most bearish quintiles average next-day returns of −2.35% and −0.19%. In Exhibit 9.3 these are the signal-bucket labels, and the bars run from about −0.03% to +0.13% (page image). The monotonic ordering holds in the figure.
- **Arithmetic.** Recomputed in the session, with no script kept: IR 12.1/21.2 = 0.571, Calmar 12.1/39.7 = 0.305, drawdown example 1.10 × 0.85 × 1.15 − 1 = +7.5%, 19/35 = 54.3% of non-zero days won, cost example +$0.10 to −$0.90 per 100 shares, and 746% and 870% over 18.6 years giving 12.2% and 13.0% a year (Narang 12.1% and 12.9%). All consistent within rounding and the period's endpoints.
- **The legacy dropped conditions** that change the meaning: "for a given level of returns" (item iii), deduction and falsification (block 1), and the advice on which way to err (block 4).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. "Research", pp. 161–187; Exhibits 9.2, 9.3, 9.5 as images | Third edition; edition of the legacy notes and the catalogue unknown; one practitioner's account; the example strategy is in-sample and untraded |
| `backtest-inference` readings, return-predictability and crowding papers | none | Stubs only |

The four new entries are *partly checked 2026-10-15*, *draft*, current as of 2024; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/research-engineering-validation/derivations.tex`, with only the subsection unnumbered. A script compared it against the committed original (`git show HEAD:…/research.tex`). The body appears exactly once; the four blocks (Scientific Method, Sources of Alpha Idea Generation, Model Quality Assessment, Other Considerations in Model Testing) appear once each, verbatim and in order; all 21 items are present; and nothing lay outside the blocks but the migrate-to line and the subsection heading. The artefact compiles alone: 2 pages, no warnings, no bad boxes.

### Counts

`migration_status.py --check`, 0 problems: 609 → 605 legacy blocks = 530 shared + 46 single-candidate + 29 assigned. `research-engineering-validation`: exclusive 4 → 0. `backtest-inference`: entries 0 → 4, backlog stubs 0 → 8 (new note). Entries 91 → 95 (methods 14 → 16, pitfalls 0 → 2, the first Pitfall entries). One reading note added (`s7-narang`); no new `front/sources.tex` keys.

### Other files

- Chapter opener `compendium/research-engineering-validation/section.tex`: pathway comment, opening paragraph and `\input` updated; its legacy-candidate comment now names only `sysinv/modelrisk.tex`.
- `notes/log.md`: coverage row for `backtest-inference`; the `s7-narang` progress cell now records the edition question; two open questions appended.
- `compendium/README.md` (order paragraph) and `README.md` (layout line for `migration-slices.md`).
- Numerical scripts: unchanged and not rerun, since no content they check changed.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 213 pages (210 before); no LaTeX warnings; the one `page.i` duplicate-destination warning; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before. The first build had four new overfull boxes from the artefact path in each entry's *Further reading*; they were removed by splitting the path. Rendered and inspected: PDF pp. 7–11 (the chapter opener and the four new entries, plus the start of the operational-controls section), pp. 111–112 (`def:crypto-trading-risk-layers` after the slice-24 follow-up) and p. 169 (the legacy portfolio chapter where the research subsection was). Tests: 14 passed.

### For review

- Routing all four blocks to `backtest-inference` against the map, and opening that pathway's note with eight stubs, two of which name other pathways.
- Citing the third edition while the catalogue leaves the edition open.
- The qualifications to Narang's heuristics: smooth P&L, lower volatility, the R² of 0.05, time decay as crowding, and parameter stability as evidence against overfitting.

## Slice 25 follow-up: corrections, 15 October 2026

Narrow corrections after an audit of slice 25; the slice-25 record above is left as written, and this record supersedes it where they differ. The artefact `notes/artefacts/research-engineering-validation/derivations.tex` is unchanged.

- **S&P example, `meth:backtest-evaluation-diagnostics`.** Slice 25 described the strategy as "long when the index's earnings yield exceeds the 10-year Treasury yield and short otherwise", which leaves out its no-trade state. Narang (third edition) p. 168 reads a higher stock yield as a signal to be long and a lower one as a signal to be short, as "an adjustment to" the equity risk premium. P. 173 says the strategy signals "only when the model perceives that the opportunity is sufficiently attractive to warrant trading at all" and is at zero 65% of the time. The entry now gives both, and says that the adjustment and the threshold are not stated; no threshold was supplied.
- **Ratio signs, same entry.** Narang defines Calmar as average return divided by the worst drawdown and Omega as the sum of positive returns divided by the sum of negative returns, both of which have negative denominators taken literally. He reports both as positive (0.31 and 1.26, pp. 173–174). The entry now quotes his wording and sets out, as interpretation, the explicit conventions Calmar $=\bar R/\lvert\mathrm{MDD}\rvert$ and $\Omega(0)=\sum\max(R_t,0)/\lvert\sum\min(R_t,0)\rvert$. Hand-check, in the session with no script kept: $12.1/\lvert-39.7\rvert=0.305$ against $-0.305$ taken literally; returns $+2,+1,-1.5,-0.5$ give $\Omega(0)=3/2=1.5$ against $-1.5$. His Sterling and Omega values were not recomputed, since the strategy's returns are not available.
- **Item count.** The slice-25 *Preservation* paragraph says "all 21 items are present". The 21 counted the substring `\item`, which also matches the three `\setlength{\itemsep}{0pt}` lines. The original has 18 `\item` commands: 3 in *Scientific Method*, 4 in *Sources of Alpha Idea Generation*, 11 in *Model Quality Assessment* and none in *Other Considerations in Model Testing*. Recounted against `9148410:…/sysinv/research.tex` with a pattern that excludes `\itemsep`; all 18 and the three `\itemsep` lines appear in the artefact. No text was lost.
- **Guidance after the record split.** `compendium/README.md` now points dispositions and checks to `migration-slices.md` (its opening paragraph and Phase 1 step 3). In `migration.md` the progress table's "checks table below" now points to each slice's *Checks and their limits*, and the slice-25 index row now gives its commit `c45e2b5`. Historical slice narratives that mention `migration.md` were not changed.
- **Notes.** The `s7-narang` reading note and the `backtest-inference` pathway note record the corrections. Entries, stubs, ownership and counts are unchanged (605 legacy blocks; 95 entries).

## Slice 26: risk assessment (model risk, regime change, shocks, contagion, monitoring), 15 October 2026

Migration of the five-block risk-assessment file of Narang's systematic-investing notes, run after the slice-25 follow-up above. Migration and source checking, not study; no checkpoint was attempted, and no reading of either owning pathway was read.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/modelrisk.tex`: 5 counted blocks (four `definition`s and one `method`) with their 7 `\item` commands (3 in *Model Risks*, 4 in *Risk Monitoring Methods*; the two `\setlength{\itemsep}{0pt}` lines are not items). Outside the blocks was only the `% migrate-to:` line and the subsection heading (checked by script). The file and its map row were deleted. In `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The other `sysinv/` files, other legacy files, earlier artefacts (including `notes/artefacts/model-governance-controls/derivations.tex` from slice 17), the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map names `model-governance-controls`, whose outcome is designing a model inventory, validation and change process and the pre-trade and kill-switch controls a strategy needs before production, with monitoring in its checkpoint. Model risk, regime change, exogenous shocks and their monitoring are what such a process must cover, so blocks 1, 2, 3 and 5 stay with it.

`funding-crowding` (section `portfolio-risk-financing`) has the outcome of tracing "how margin, leverage, funding runs and crowded positions turn small shocks into forced liquidations". Its readings include the 2007 quant meltdown (`exp-khandani-lo-quant-meltdown`) and crowded exits (`wide-pedersen-exit`). The contagion block is about common positions, cross-collateralisation, volatility targeting and forced exits, so **routing exception:** block 4 goes to `funding-crowding`. Other candidates were rejected:
- `risk-tail-systemic` (fire-sale stress tests) and `risk-parity-vol-targeting` (volatility targeting as an allocation method): the block describes the mechanism of forced exits, not a stress model or an allocation rule.
- `macro-regimes-stock-bond` (regime identification) for block 2: the block is a model-risk statement, not regime estimation.

The new entries opened the topic files `compendium/research-engineering-validation/strategy-risk.tex` and `compendium/portfolio-risk-financing/crowding-contagion.tex`, and the pathway note `notes/pathways/funding-crowding.md`. The artefact sits under the map candidate as a new file, `notes/artefacts/model-governance-controls/risk-assessment.tex`, so that slice 17's `derivations.tex` there is unchanged.

| # | Legacy block | Owner | Destination | Checked source (`s7-narang`, 3rd ed., chap. "Risks Inherent to Quant Strategies") | Disposition |
|---|---|---|---|---|---|
| 1 | *Model Risks* (definition) | `model-governance-controls` | `def:quant-strategy-risk-sources` (new) | sec. 10.1, pp. 191–196 | Rewritten |
| 2 | *Regime Change Risk* (definition) | `model-governance-controls` | merged into `def:quant-strategy-risk-sources` | sec. 10.2, pp. 196–200 | Merged |
| 3 | *Exogenous Shock Risk* (definition) | `model-governance-controls` | merged into `def:quant-strategy-risk-sources`; stub `meth:discretionary-override-governance` | sec. 10.3, pp. 200–202 | Merged; overrides qualified |
| 4 | *Contagion Risk* (definition) | `funding-crowding` | `def:common-investor-contagion` (new); stubs `ev:august-2007-quant-unwind`, `mod:margin-liquidity-spiral`, `mod:volatility-targeting-deleveraging`, `meth:overlap-crowding-measure` | sec. 10.4, pp. 202–209; Exhibit 10.6 by page image | Rewritten; 2007 drivers kept as practitioner explanation |
| 5 | *Risk Monitoring Methods* (method) | `model-governance-controls` | `meth:quant-strategy-monitoring` (new) | sec. 10.5, pp. 209–210 | Rewritten; execution indicators left to `meth:execution-decision-support` |

**Substantive claims.**

| Block | Legacy claim | Disposition |
|---|---|---|
| 1 | Model risk defined; every component can have it | Rewritten (p. 192); Narang's list of components and "explode on a busy trading day" added |
| 1 | Inapplicability: wrong problem, or misapplied technique | Rewritten (pp. 192–193), with his VaR example |
| 1 | Misspecification: works most of the time, fails in extreme events | Rewritten (pp. 193–195), with his August 2007 liquidity example |
| 1 | Implementation errors; "models loaded in a wrong sequence" | Rewritten (pp. 195–196). The sequence claim corrected to his example: servers restarted in the wrong order, execution before alpha, selling 80% of the portfolio. Knight and AXA Rosenberg figures reported as his, unchecked; stub `ev:quant-implementation-failures`. Implementation failure separated as operational, linked to `meth:automated-trading-operational-controls` |
| 2 | Relationships in historical data change; model loses effectiveness | Rewritten (pp. 196–200), with his SCHW/MER and value–growth examples; distinguished from overfitting (`pit:parameter-overfitting`) and from funding contagion, which his value–growth example mixes in |
| 3 | Shocks from information outside the market (terrorism, war, bailouts, short-sale rules) | Rewritten (pp. 200–202), with his four 2001–2008 examples; his concession that classification is arguable added |
| 3 | "May require discretionary overrides" | Qualified: an override is an unvalidated model change; his own 2007 account says discretionary unwinding spread losses (p. 208); the one-firm anecdote is not evidence; governance stubbed |
| 4 | Risk from others holding the same strategies; crowding; ATM effect forcing exits "in a panic" | Rewritten (p. 202), with his 1998 LTCM example (pp. 202–203) |
| 4 | 2007 crisis driven by size and popularity, subpar returns, cross-collateralisation, risk targeting | Rewritten as Narang's four drivers (pp. 203–205), presented as his explanation ("likely", "it appears", "in my view"), with no data in the chapter. Not adopted as causal evidence; stubs for Khandani–Lo, margin spirals, volatility-targeting deleveraging and an overlap measure. "Criss" read as crisis |
| 4 | (Narang, not legacy) losses "solely the result of market impact"; Pulte Homes illustration | Reported as his claims, qualified by the arithmetic below and the square-root impact entry |
| 5 | Exposure, P&L (hit rate), execution, systems monitors | Rewritten (pp. 209–210); VaR measure, "how money is made" monitors and early-warning purpose added; execution-algorithm indicators cross-referenced, not duplicated |

No claim was deleted outright. **Kept distinct:** the slice-25 stub `ev:signal-decay-crowding` in `backtest-inference` (does delayed-signal decay identify crowding?) is unchanged and is named in the contagion entry as a separate question.

**Existing entries checked.**
- `meth:automated-trading-operational-controls`: covers operational controls, the destination for implementation failure; cross-referenced, unchanged.
- `meth:execution-decision-support`: execution-algorithm indicators; cross-referenced from the monitoring entry, unchanged.
- `meth:backtest-evaluation-diagnostics`: the source of expected hit rates and exposures; cross-referenced.
- `pit:parameter-overfitting`: contrasted with regime change; cross-referenced.
- `res:arbitrage-risks`: Harris's model risk and staying power; already pointed to `funding-crowding`; cross-referenced, unchanged.
- Also linked: `ev:square-root-impact`, `mech:futures-margin-settlement`, `def:securities-lending-fee-rebate`.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024, the same local copy as slice 25 (text layer through PDFKit; printed page = PDF page − 20). Chap. 10, "Risks Inherent to Quant Strategies", secs. 10.1–10.6, pp. 191–211, was verified to exist in this edition from the contents (pp. 191–211) and the running heads. Exhibit 10.6 (p. 206) was read by page image; Exhibits 10.1–10.5 were read from the text layer only.
- **Not read:** every reading of `model-governance-controls` and `funding-crowding`, including the Knight Capital order and Khandani and Lo; the AXA Rosenberg order (not catalogued); `risk-parity-vol-targeting` readings.

### Findings and arithmetic

- **Pulte Homes, Exhibit 10.6.** −22.0%, −12.5%, +15.6%, −22.6%, with average daily volume 3.5, 7.2, 10.4 and 5.7 million shares. The two declines compound to 1 − 0.78 × 0.875 = 31.75%. The +15.6% rebound brings the price from 0.6825 to 0.789 of its 31 May level, recovering (0.789 − 0.6825)/0.3175 = 33.6% of the lost price (38% in logs), not "about half". Narang counts the decline over 44 days and the rebound over 4: the rate is about 3.7 times the earlier pace by share of lost ground, or 5.4 times by percentage points per day (15.6/4 against 31.75/44), not "about 20 times". Volume rose 106% and then 44%, matching his "100 percent" and "50 percent".
- **His other pace claims check out.** Value–growth: half the loss in 16 days against 160 gives 5 times (his "five times"); 40% in 6 days against 115 gives 7.7 times (his "almost eight").
- **Leverage arithmetic.** 4 × 1.5 = 6 and 4 × 2 = 8 gross, matching his "six or eight".
- All recomputed in the session; no script kept, and no existing numerical script covers this content.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. "Risks Inherent to Quant Strategies", pp. 191–211; Exhibit 10.6 as image | Third edition; one practitioner's account; company and episode figures unsourced in the chapter; 2007 drivers are his inferences |
| Pathway readings (`exp-khandani-lo-quant-meltdown`, `wide-knight-capital`, `s8-governance` and others) | none | Stubs only |

The three new entries are *partly checked 2026-10-15*, *draft*, current as of 2024; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/model-governance-controls/risk-assessment.tex`, with only the subsection unnumbered. A script compared it with `git show HEAD:…/sysinv/modelrisk.tex`, counting commands rather than substrings:
- the body appears exactly once;
- the 5 blocks appear verbatim once each, with titles in order;
- `\item` commands (excluding `\itemsep`) number 3, 0, 0, 0 and 4 per block, 7 in both the original and the artefact, plus 2 `\itemsep` lines;
- the sequence of 14 `\begin`/`\end` commands is identical;
- nothing lay outside the blocks but the migrate-to line and the subsection heading.

The artefact compiles alone: 1 page, no warnings, no bad boxes.

### Counts

`migration_status.py --check`, 0 problems: 605 → 600 legacy blocks = 530 shared + 41 single-candidate + 29 assigned. `model-governance-controls`: exclusive 5 → 0, entries 1 → 3, stubs 2 → 4. `funding-crowding`: entries 0 → 1, stubs 0 → 4 (new note). Entries 95 → 98 (definitions 34 → 36, methods 16 → 17). The `s7-narang` reading note was extended; no new `front/sources.tex` keys.

### Other files

- Chapter openers of `research-engineering-validation` (`model-governance-controls` now three entries; no legacy file now mapped to the section) and `portfolio-risk-financing` (`funding-crowding` added first, as in the guide's order).
- `notes/log.md`: coverage rows for `model-governance-controls` and `funding-crowding`, the `s7-narang` progress cell, and one open question appended.
- `notes/migration.md`: status, index, next slice and map.
- `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 216 pages (213 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, none in the changed chapters, as before. Rendered and inspected:
- PDF pp. 8–9: the slice-25 corrections, including the displayed Calmar and Omega formulas;
- pp. 13–15: the end of the operational-controls entry and the two new `model-governance-controls` entries;
- pp. 22–23: the `portfolio-risk-financing` opener and the contagion entry;
- p. 172: the legacy portfolio chapter, which now ends after the execution file.

Tests: 14 passed. The numerical scripts were not rerun; none covers changed content.

### For review

- Routing the contagion block to `funding-crowding` against the map, and the new pathway note with four stubs.
- Presenting Narang's 2007 drivers as his explanation, and the Pulte Homes arithmetic against his text.
- The qualification of discretionary overrides, and implementation failure treated as operational rather than model risk.

## Slice 26 follow-up: overrides, impact inference and the Calmar ratio, 15 October 2026

Narrow corrections to slices 25 and 26 after an audit, run before slice 27; the records above are left as written, and this record supersedes them where they differ. No legacy block, entry label, stub, artefact or count changed (600 legacy blocks; 98 entries). The passages were reread in the same local third edition of `s7-narang` (text layer; printed page = PDF page − 20).

- **Overrides, `def:quant-strategy-risk-sources`** (`compendium/research-engineering-validation/strategy-risk.tex`). Slice 26 wrote that "an override is itself an unvalidated change to the model". The entry now separates an ad hoc intervention, improvised outside the validated design and in effect an untested model change, from an approved contingency response (a pre-specified de-risking rule, limit or kill switch whose triggers, authority and effects were tested and approved), which is part of the validated design. Narang's p. 208 account and the one-firm anecdote are unchanged. Operational failure is now said to be made less likely and less costly by testing, change control and operational controls, which mitigate it rather than guarantee its prevention. The five causes are presented as overlapping questions (a regime change can expose a misspecification; others' forced selling can look like a regime change; one loss can have several causes), not exclusive categories. The `model-governance-controls` pathway note records the change.
- **Pulte Homes and impact, `def:common-investor-contagion`** (`compendium/portfolio-risk-financing/crowding-contagion.tex`). Slice 26 set Narang's "quadratic nature of market impact" (p. 206) against the square-root law as if the table contradicted it. That inference is withdrawn: average daily volume and returns over crisis sub-periods give no metaorder sizes or schedules, mix many traders' flow, and do not reveal the price without the liquidation, so they identify no metaorder impact exponent, quadratic or square-root. The checked arithmetic (31.75% fall, about a third recovered, 3.7–5.4 times the earlier pace) and the separation of Narang's account from causal evidence are kept; his unsourced "as much as 15 percent in market impact" is now noted. The `funding-crowding` note and the `s7-narang` reading note record the change; the dated open question in `log.md` is left as written, with a new dated line withdrawing its impact clause.
- **Calmar ratio, `meth:backtest-evaluation-diagnostics`** (`compendium/research-engineering-validation/backtest-evaluation.tex`). $12.1/39.7=0.30479$, which rounds to 0.30, while Narang reports 0.31 on pp. 173 and 174. The entry no longer says "as reported" after 0.30, and its *Practice* now says that most example figures agree within rounding, with the Calmar ratio the unexplained exception. No explanation was supplied. The slice-25 *Findings* line "all consistent within rounding" is superseded for this ratio. Recomputed in the session: $12.1/39.7=0.3048$, $12.1/21.2=0.5708$, $19/35=0.5429$.
- **Index.** The slice-26 row in `notes/migration.md` now gives its commit `e0451c9`.

## Slice 27: transaction cost models (components and cost functions), 15 October 2026

Migration of the transaction-cost-models file of Narang's systematic-investing notes, run after the slice-26 follow-up above. Migration and source checking, not study; no checkpoint was attempted, and no reading of either owning pathway was read.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/txncostmod.tex`: an introductory paragraph outside the environments, and 2 counted blocks (one `remark`, one `definition`) with 7 `\item` commands (3 in *Transaction Cost Components*, 4 in *Types of Transaction Cost Models*; the two `\setlength{\itemsep}{0pt}` lines are not items). Outside the blocks were only the `% migrate-to:` line, the subsection heading and the introduction (checked by script). The file and its map row were deleted. In `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The other `sysinv/` files, other legacy files, earlier artefacts, the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map names only `portfolio-construction-risk`, a **section overview**, whose outcome is a portfolio "whose forecasts, risk model, constraints, costs and tail measures are explicit and testable", and whose first goal, constrained portfolios "with factor risk models, shrinkage and costs", names `portfolio-construction`. The candidates compared:
- `portfolio-construction`: construct a constrained portfolio from noisy forecasts "with a factor risk model, shrinkage and costs"; readings include convex Markowitz with costs and multi-period trading (`wide-boyd-markowitz-seventy`, `exp-boyd-multiperiod-trading`) and, as an optional branch, no-trade regions (`w2-davis-norman`). A cost function supplied to the portfolio optimiser, and the reason it exists, is this pathway's material.
- `execution-trading-costs` (overview): plan executions, estimate expected cost from a stated impact model and split realised shortfall into spread, impact, timing and fees. It already owns `def:transaction-costs`, `meth:transaction-cost-analysis` and `def:execution-benchmark`; the cost-components block restates those terms in Narang's words.
- `price-impact-execution`: estimate an impact model from executions. It owns `ev:square-root-impact`, `meth:almgren-impact-estimation` and `def:price-impact`, the evidence on the shape of impact costs. The legacy blocks make no estimation; their shape claims are checked against these entries, not moved into them.

**Routing exception:** the introduction and *Types of Transaction Cost Models* go to `portfolio-construction` as one new entry, `mod:portfolio-transaction-cost-function`, in the new topic file `compendium/portfolio-construction-risk/transaction-cost-models.tex`; *Transaction Cost Components* is merged into `def:transaction-costs` (owned by `execution-trading-costs`). Nothing was routed to `price-impact-execution`, whose entries are cross-referenced and unchanged. The pathway had no note; this slice opened `notes/pathways/portfolio-construction.md`. The artefact sits under the map candidate as `notes/artefacts/portfolio-construction-risk/transaction-cost-models.tex`, keeping the file whole.

| Part | Legacy text | Owner | Destination | Checked source (`s7-narang`, 3rd ed., chap. 5) | Disposition |
|---|---|---|---|---|---|
| Intro | Two reasons to trade; benefit above cost; the model informs, does not minimise | `portfolio-construction` | `mod:portfolio-transaction-cost-function` (new), Statement and Practice | pp. 85–86, 96 | Rewritten; Narang's framing kept as his; joint optimisation and forced trades added as interpretation |
| 1 | *Transaction Cost Components* (remark), items i–iii | `execution-trading-costs` | merged into `def:transaction-costs` (Statement; Pitfalls, "Narang's terms") | sec. 5.1, pp. 86–91; `exp-pfmi` paras 1.12–1.13 | Merged with corrections (subclaims below) |
| 2 | *Types of Transaction Cost Models* (definition), items i–iv | `portfolio-construction` | `mod:portfolio-transaction-cost-function` (new); stubs `meth:convex-cost-portfolio-optimisation`, `res:no-trade-region` | sec. 5.2–5.3 and n. 2, pp. 91–97; Exhibits 5.1–5.4 and n. 2 by page image | Rewritten; rankings not adopted (subclaims below) |

**Subclaims.**

| Where | Legacy claim | Disposition |
|---|---|---|
| Intro | "Trade is made only if it increases the odds or magnitude of return … or decreases … loss" | Rewritten as Narang's "only two reasons to make a trade" (p. 85); interpretation: forced trades (flows, margin, constraints) exist |
| Intro | "This improvement should be higher than cost of trading" | Rewritten as his hurdle (p. 85); interpretation: in an optimiser cost enters jointly with alpha and risk, compared over the same horizon and units, not trade by trade |
| Intro | Not designed to minimise cost, only to inform portfolio construction | Rewritten (pp. 85–86); his two phases of cost reduction added (p. 96) |
| 1.i | Commissions and fees paid to brokerages (access), exchanges (security), regulators (infrastructure) | Corrected: the text lists three payers and three services without pairing them; p. 87 credits exchanges with access to liquidity and with guaranteeing performance; that guarantee is a central counterparty's function (`exp-pfmi` para. 1.13), as interpretation |
| 1.i | Quants use the bank's infrastructure; commissions small per trade | Merged (p. 86) |
| 1.i | Brokers collect clearing and settlement fees | Merged: usually a component of commissions (p. 86) |
| 1.i | Clearing = regulatory reporting and monitoring, tax handling, handling failure, before settlement | Reported as Narang's description, not adopted as a definition. The CPMI glossary was not retrieved; the PFMI paragraphs read describe settlement systems' clearing functions (confirmation of instructions) and CCP netting, not his list. Stubbed (`def:clearing-settlement`, `execution-trading-costs`) |
| 1.i | Settlement = delivery of securities against payment in full | Reported as his; set beside the PFMI's free-of-payment and DvP transfers (para. 1.12) |
| 1.ii | Slippage from decision to the order at the exchange | Merged and mapped to the delay term $S(P_0-P_d)$, signed by side; his CVX example (pp. 87–88) |
| 1.ii | Trend-following suffers most, mean-reverting least | Kept as Narang's conditional claim about the expected drift over the delay relative to trade side; no data in the source |
| 1.ii | Lower latency, smaller slippage | Qualified: shortens the delay; lowers expected cost only with adverse expected drift (his accurate-forecast condition, p. 88) |
| 1.ii | More volatile, bigger slippage | Qualified: widens the dispersion; raises expected cost only with adverse drift (pp. 88, 91). His GOOG figure not used (undated, unsourced) |
| 1.iii | Impact: how much an order moves the market by demanding liquidity | Merged with his operational definition, arrival price to fill (pp. 88–89), mapped to the trading-related part of shortfall, not causal impact (`def:price-impact`) |
| 1.iii | "Unknown until the trade has already been completed" | Corrected: after completion the fills and realised cost are known, but impact is not, since the unaffected price is never observed (Kissell pp. 91–92 as cited in the entry; `def:price-impact`) |
| 1.iii | Slippage–impact interaction when selling into an uptrend | Merged with his example ($100.00, $100.05, $100.20; −$0.05 and −$0.15, checked) and his concession that they may be inseparable (pp. 89–90) |
| 2.i | Flat: same cost regardless of size; reasonable if size nearly constant and liquidity constant | Rewritten (pp. 92–93) with units; interpretation: a per-share commission is linear, only a per-ticket charge is flat |
| 2.ii | Linear: constant rate; "better estimate than flat" | Rewritten (pp. 93–94); the comparison held against his drawn curve only, not adopted generally |
| 2.iii | Piecewise-linear: balance of simplicity and accuracy; "better accuracy than flat or linear" | Rewritten as his "happy medium" (p. 94); accuracy ranking not adopted |
| 2.iv | Quadratic: "most computationally intensive, but also most accurate" | Not adopted as fact. Narang's exhibits are schematic, against an assumed convex curve from zero; his note 2 says quadratic is "not universally accepted" and reports square-root per-share costs for U.S. equities; computational cost depends on the optimiser formulation (interpretation, stubbed) |

No claim was deleted outright.

**Units and conventions** (all in `mod:portfolio-transaction-cost-function`): total cost $C(q)$ in currency against signed size $q$; per-unit cost $C/\lvert q\rvert$ in currency per share or basis points. A quadratic total is a linear per-unit cost; square-root per-unit cost is a 3/2-power total. Narang's note 2, "cost per share scales with an exponent of 1.5, or in other words, as the square root of trade size" (p. 97), conflates the two conventions; recorded, not repeated.

**Existing entries checked.**
- `def:transaction-costs`: the destination of block 1; Statement, Pitfalls (new paragraph "Narang's terms"), Index, Further reading and Status extended; its accounting split, examples and other text unchanged.
- `meth:transaction-cost-analysis`: ex-ante forecasts against realised costs; cross-referenced from the new entry, unchanged.
- `def:execution-benchmark`: its decision and arrival prices fix Narang's slippage interval; not changed, since `def:transaction-costs` already uses them.
- `def:price-impact`: the counterfactual definition of impact; cross-referenced, unchanged.
- `meth:almgren-impact-estimation`: the fitted 3/5 per-unit temporary-impact exponent, a total exponent of about 1.6 at fixed duration; cross-referenced, unchanged.
- `ev:square-root-impact`: the empirical shape and the two-thirds shortfall ratio; cross-referenced, unchanged.
- Also linked: `mod:almgren-chriss-execution` (linear temporary impact, a quadratic total cost for a given schedule) and `pit:backtest-cost-short-assumptions` (misestimated costs, Narang p. 186; repeated by him on p. 86).

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024 (copyright page: ISBN 9781119931911 Adobe PDF), the same local copy as slices 25 and 26, read through PDFKit's text layer (printed page = PDF page − 20, checked again on this chapter). Chap. 5, "Transaction Cost Models", secs. 5.1–5.3 and notes, pp. 85–97, located from the contents (Transaction Cost Models 85; 5.1 p. 86; 5.2 p. 91; 5.3 p. 96; Notes p. 97) and the running heads. Exhibits 5.1–5.4 (pp. 93–95) and note 2 with Exhibit 5.5 (p. 97) were read from page images; p. 98 is blank (page image).
- **CPSS–IOSCO, *Principles for financial market infrastructures*** (`exp-pfmi`, April 2012), downloaded 2026-10-15 from bis.org (the catalogue's `d101a.pdf` link redirects to `bis.org/publications/principles-financial-market-infrastructures.pdf`; server length 1,117,912 bytes). PDFKit read only the first 18 PDF pages, the front matter to para. 1.19; paras. 1.8–1.13 (pp. 7–9) were read. The glossary annex was not reached.
- **Not retrieved:** the CPMI glossary (`bis.org/cpmi/glossary.pdf` returned "page not found"; `bis.org/cpmi/publ/d00b.pdf` returned an HTML page). A web search found secondary pages quoting a CPMI-style clearing definition; they were not used.
- **Not read:** every reading of `portfolio-construction` (including the Boyd papers and Davis–Norman named in stubs) and of `price-impact-execution`; the sources behind Narang's note 2.

### Distinctions kept

- Narang's terminology against current usage: his slippage is the delay cost; his market impact is the arrival-to-fill trading cost, not causal impact.
- Total cost against per-unit cost, with sizes in shares, currency or fraction of volume.
- The author's claims (two reasons to trade; the accuracy and computational ranking; the trend/mean-reversion, latency and volatility statements) against interpretation, each marked.
- The realised cost observed after a trade against the impact, which is never observed.

### Numerical check

Recomputed in the session, with no script kept and no existing script covering this content: slippage–impact example $100.05-100.00=0.05$, $100.20-100.05=0.15$; ECN take fee minus rebate $0.3-0.2=0.1$ cents; the illustration in the new entry: per-share cost $0.5\times0.02\times(q/10^6)^{1/2}$ of a \$50 price gives 10 bp and \$500 at 10,000 shares, 14.14 bp and \$1,414.21 at 20,000, 20 bp and \$4,000 at 40,000; ratios $2^{1/2}=1.414$ per share and $2^{3/2}=2.828$ in total.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. 5, pp. 85–97; Exhibits 5.1–5.4, 5.5 and n. 2 as images | Third edition; one practitioner's account; exhibits schematic with no data; the 20–50 percent cost share, the "generally accepted" quadratic, the GOOG statistic, the 2019 dark-pool share and the square-root evidence in n. 2 are unsourced or cited only to a newspaper, not checked |
| `exp-pfmi` | paras. 1.8–1.13, pp. 7–9 | Only the first 18 PDF pages could be read; no glossary; 2012 text |
| `portfolio-construction` and `price-impact-execution` readings | none | Stubs and cross-references only; the computational remarks are interpretation |

The new entry and the merged paragraph are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/portfolio-construction-risk/transaction-cost-models.tex`, with only the subsection unnumbered; no earlier artefact was touched. A script compared it with `git show HEAD:compendium/legacy/portfolio-construction-risk/sysinv/txncostmod.tex`, counting commands with patterns rather than substrings:
- the body below the subsection heading appears exactly once;
- the introduction (373 characters) appears exactly once, before the blocks;
- the 2 blocks appear verbatim once each, in order (*Transaction Cost Components*, *Types of Transaction Cost Models*);
- `\item` commands (pattern `\item` not followed by a letter, excluding `\itemsep`) number 3 and 4, 7 in both the original and the artefact, plus 2 `\itemsep` lines;
- the sequence of 8 `\begin`/`\end` commands is identical (ignoring the artefact's `document`);
- nothing lay outside the blocks but the migrate-to line, the subsection heading and the introduction.

The artefact compiles alone: 1 page, no warnings, no bad boxes; its page image was inspected.

### Counts

`migration_status.py --check`, 0 problems: 600 → 598 legacy blocks = 530 shared + 39 single-candidate + 29 assigned. `portfolio-construction-risk`: exclusive 10 → 8. `portfolio-construction`: entries 0 → 1, stubs 0 → 2 (new note); exclusive 7, unchanged. `execution-trading-costs`: entries 14, unchanged (the merge changes an existing entry); stubs 0 → 1. Entries 98 → 99 (models 10 → 11). The note for `execution-trading-costs` names the new entry's pathway without its label, so that the entry is counted only under its owner. No new `front/sources.tex` keys (`exp-pfmi` is a catalogue key).

### Other files

- Chapter openers: `portfolio-construction-risk` (`portfolio-construction` added first, in the guide's order; the new topic file input before the performance file) and `execution-trading-costs` (the merge noted in its comment and opening paragraph).
- `notes/readings/s7-narang.md`: pathways, sections and key results for chap. 5; entries.
- `notes/log.md`: coverage row for `portfolio-construction`; the `s7-narang` progress cell; one open question appended.
- `notes/migration.md`: status, index, next slice and map; `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 219 pages (216 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files (located from the log), as before. The first build had two new overfull boxes and one underfull box from catalogue keys in the new entry's *Further reading*; that line was reworded. Inspection of the rendered page then showed $\mathbb 1$ printing as a wrong glyph; the flat form was rewritten in words, which gave one overfull display, split into two lines. Rendered and inspected:
- PDF p. 9: the corrected Calmar passage and *Practice* of `meth:backtest-evaluation-diagnostics`;
- p. 14: `def:quant-strategy-risk-sources` with the corrected *Practice* and overrides;
- pp. 21–23: the `portfolio-construction-risk` opener, the new entry and the unchanged performance entry after it;
- p. 25: `def:common-investor-contagion` with the corrected Pulte passage;
- pp. 88–89: `def:transaction-costs` with Narang's components and the new Pitfalls paragraph;
- pp. 171 and 173: the legacy portfolio chapter, where *Risk Models* now runs straight into *Portfolio Construction Models*.

Tests: 14 passed.

### For review

- Routing the introduction and cost-function block to `portfolio-construction` against the map, and merging the components into an `execution-trading-costs` entry rather than adding a new one.
- The mapping of Narang's slippage and impact onto the delay and trading-related terms, and the correction of "unknown until the trade has been completed".
- The interpretation on computational cost (convex piecewise-linear, quadratic, 3/2-power, integer variables for per-trade fixed costs), which no source read supports and which the `meth:convex-cost-portfolio-optimisation` stub should replace.
- Clearing left undefined pending the CPMI glossary (`def:clearing-settlement`).

## Slice 27 follow-up: units, cost-function conditions and the sell example, 15 October 2026

Narrow corrections to slice 27 after an audit, run before slice 28; the slice-27 record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub, artefact or count changed (598 legacy blocks; 99 entries).

- **Units, `mod:portfolio-transaction-cost-function`** (`compendium/portfolio-construction-risk/transaction-cost-models.tex`). Slice 27 let $q$ be shares, "contracts, or currency" while giving coefficients per share. The notation is now for one equity: $q$ and $V$ in shares, $P$ in currency per share, coefficients in currency, currency per share or currency per share squared, and $\eta$ dimensionless. The per-share cost $c(q)=C(q)/\lvert q\rvert$ is defined only for $q\neq0$. Contracts or notional are said to need their own units (such as a multiplier), not the same conversions. "Per-unit" became "per-share" where it meant that.
- **Parameter conditions.** All coefficients are nonnegative and every form has $C(0)=0$, $C\ge0$ and depends only on $\lvert q\rvert$. The displayed $\max_i(b_i\lvert q\rvert-d_i)$ with increasing slopes alone did not guarantee this: slopes 0.01, 0.03 with intercepts $-5$, 200 give $C(0)=5$, and with 5, 200 give $C(0)=-5$. The entry now uses the convex hinge form $b_0\lvert q\rvert+\sum_ih_i(\lvert q\rvert-\kappa_i)_+$ with $0<\kappa_1<\dots$, and states the equivalent maximum of lines with slopes $s_j=b_0+\sum_{i\le j}h_i$ and intercepts $d_j=\sum_{i\le j}h_i\kappa_i$. The 3/2-power form $\eta P\lvert q\rvert(\lvert q\rvert/V)^{1/2}$ is written out, and the assumptions are stated: symmetric between buys and sales, nonnegative (no rebates or favourable drift), expected rather than realised, one instrument and period, independent of duration and other trades.
- **Checks**, exact fractions in the session (no script kept): for $b_0=0.01$, $h=(0.02,0.05)$, $\kappa=(10{,}000,50{,}000)$, $C=0$ at 0 and 50, 100, 700, 1,300, 2,100 at $\lvert q\rvert=$ 5,000, 10,000, 30,000, 50,000, 60,000, equal for $\pm q$; left and right values at each breakpoint differ by under $10^{-7}$; equal to the maximum of lines (0.01, 0), (0.03, 200), (0.08, 2,700) at every point tested. The illustration with $\eta=0.01$, $P=50$, $V=10^6$ still gives \$500 and 10 bp at $\pm$10,000 shares and \$1,414.21 and 14.142 bp at 20,000.
- **Sell example, `def:transaction-costs`** (`compendium/execution-trading-costs/transaction-cost-analysis.tex`). Slice 27 said Narang's sale filled at \$100.20 "though the order did not raise the price". That assertion is removed: the example shows a negative arrival-to-fill cost against a benchmark, which does not identify the order's causal effect.
- **Notes and index.** The `portfolio-construction` and `execution-trading-costs` pathway notes record the changes; the slice-27 row in `notes/migration.md` now gives its commit `0224ac7`.

## Slice 28: portfolio construction models (rules, mean–variance optimisation, signal portfolios), 15 October 2026

Migration of the portfolio-construction-models file of Narang's systematic-investing notes, run after the slice-27 follow-up above. Migration and source checking, not study; no checkpoint was attempted. One of the owning pathway's readings, Boyd et al., was read in part for method mechanics; that is source checking, not study of it.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/portconstmod.tex`: an introductory paragraph outside the environments, and 3 counted blocks (one `definition`, one `remark`, one `method`) with 13 `\item` commands (4 in *Rule-Based Models*, 3 in *Optimisers Models Parameters*, 6 in *Optimisation Techniques*), plus the remark's two paragraphs of prose before its list; the three `\setlength{\itemsep}{0pt}` lines are not items. Outside the blocks were only the `% migrate-to:` line, the subsection heading and the introduction (checked by script). The file and its map row were deleted; in `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The other `sysinv/` files (`alphamod.tex`, `riskmod.tex`, `executionmod.tex`, the overview's method block), other legacy files, earlier artefacts (including slice 27's `transaction-cost-models.tex`), the deferred assignments, the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map's only candidate is `portfolio-construction`, whose outcome is to "construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk", with readings on mean–variance selection, estimation error, shrinkage, factor risk models, risk-based portfolios, Black–Litterman and convex optimisation with costs. Every block is portfolio construction in that sense, so all stay with it; no routing exception. Equal risk contribution and GARCH volatility forecasts are stubbed here with their home pathways named (`risk-parity-vol-targeting`, `time-series-volatility`), as slice 25 did for borrow data.

The new entries are in the new topic file `compendium/portfolio-construction-risk/portfolio-construction-models.tex`, input before slice 27's cost entry. The artefact is a new file, `notes/artefacts/portfolio-construction-risk/portfolio-construction-models.tex`, beside slice 27's, which is unchanged.

| Part | Legacy text | Destination | Checked source | Disposition |
|---|---|---|---|---|
| Intro | Two families: rule-based heuristics; optimisers with an objective function | `meth:rule-based-position-sizing` (Statement), `mod:mean-variance-portfolio-optimisation` | Narang chap. 6, pp. 99–100 | Rewritten |
| 1 | *Rule-Based Models* (definition), items i–iv | `meth:rule-based-position-sizing` (new); stub `meth:equal-risk-contribution` | secs. 6.1–6.1.4, 6.4, pp. 100–104, 123; Exhibit 6.1 by page image | Rewritten with corrections (subclaims below) |
| 2 | *Optimisers Models Parameters* (remark): prose and items i–iii | `mod:mean-variance-portfolio-optimisation` (new); stubs `meth:portfolio-covariance-estimation`, `mod:garch-volatility-forecast` | sec. 6.2–6.2.1, pp. 104–113; Exhibits 6.2, 6.4, 6.5 by page image; Boyd et al. secs. 1.1, 3.2, 3.4 | Rewritten with corrections |
| 3 | *Optimisation Techniques* (method), items i–vi | `mod:mean-variance-portfolio-optimisation`; `meth:signal-portfolio-allocation` (new); stubs `mod:black-litterman`, `meth:resampled-efficiency` | secs. 6.2.2–6.3, pp. 113–123; Exhibits 6.6, 6.7 and the p. 118 example by page image; Boyd et al. secs. 1.3–1.4, 2.4, 4.3, 5.6 | Rewritten, item vi not adopted |

**Subclaims.**

| Where | Legacy claim | Disposition |
|---|---|---|
| Intro | Rule-based from experience; optimisers use an objective and algorithms | Rewritten (pp. 99–100) |
| 1.i | Equal position: no other information needed; signal strength not used | Rewritten (pp. 100–101), with the implicit homogeneity assumption |
| 1.i | "Assumes sufficient statistical strength … to predict … magnitude"; "few large bets on 'best' forecast, many smaller bets"; adverse selection | **Misplaced in the legacy**: these are Narang's two arguments *against unequal* weighting, which equal weighting avoids (pp. 101–102). Restored to that role; bad-data and winsorisation points added |
| 1.ii | Equal risk: inverse to volatility or another risk measure | Rewritten (p. 102). Exhibit 6.1's 39/61 shown to be inverse-variance (inverse-volatility gives 44.4/55.6); Narang's "risk the allocation contributes to the portfolio" kept apart from inverse volatility: equal risk contribution uses the full covariance matrix and differs for three or more assets (computed). Stub `meth:equal-risk-contribution` |
| 1.ii | Backward-looking risk; changing volatility misleads | Rewritten with his 2008 bank-stock example (p. 103) |
| 1.iii | Alpha-driven: size by signal with position and group limits; forecast-to-size function | Rewritten (pp. 103–104), with his 3% and 20% example |
| 1.iii | Futures trend following "might suffer sharp drawdowns"; reliance on alpha | Rewritten as his "relatively frequently", with his reason (largest position at the reversal) (p. 104) |
| 1.iv | Decision tree: path by alpha and instrument type; percentage limits; size grows dramatically | Only the name and one sentence are in the third edition (p. 100); the details are not, perhaps from an earlier edition (not checked); kept in the artefact, not adopted |
| 2 prose | MVO the pioneer; MPT; inputs mean, variance, correlation | Rewritten with Boyd et al.'s two formulations and closed form (sec. 1.1, pp. 4–5) and Narang (pp. 104–105) |
| 2 prose | Other inputs: currency size, desired risk level "(volatility or expected drawdown)", constraints | Qualified: Narang calls them not required by the optimiser and "mostly arbitrary" (p. 105); expected drawdown is not part of mean–variance, and a return-to-drawdown objective is a different model (p. 124) |
| 2 prose | Objective "usually maximising return … relative to volatility" | Qualified: Sharpe maximisation is a distinct objective from the variance-target and risk-aversion forms (Boyd et al. sec. 3.2, p. 20); tangency portfolio (Exhibit 6.7) |
| 2.i | Expected return from alpha models, including direction | Rewritten (p. 108): sign-only forecasts set equal |
| 2.ii | Stochastic volatility methods common; "GARCH model is most used" | Reported as Narang's unsourced claim (pp. 108–109), with his own EWMA remark; his calling GARCH a stochastic-volatility model and his reading of a negative autoregression as trending not adopted; Boyd et al.'s EWMA, DCC, iterated EWMA listed. Stub `mod:garch-volatility-forecast` |
| 2.iii | Correlations unstable, so "group assets together before computing correlation within the group" | Qualified: Narang's grouping is "in the definition of relative … and/or in the specification of the risk model" (p. 111), shown with two pairs over one sample (Exhibit 6.5), not a method for estimating a covariance matrix. His 1,998,000 pairs corrected to 1,999,000. Stub `meth:portfolio-covariance-estimation` |
| 3.i | Unconstrained: "might provide a single-instrument portfolio" | Corrected: not a property of mean–variance; the closed form generally holds every asset, and Narang's own unconstrained example (85% CVX, 75% NFLX, p. 106, Exhibit 6.2) holds both; the case where a single asset results is stated as interpretation |
| 3.ii | Constraints; may drive the portfolio more than the optimiser | Rewritten with his 1.5% cap example (p. 114); penalties, costs (cross-referenced to `mod:portfolio-transaction-cost-function`), sign flips and the substitution effect (pp. 114–121) |
| 3.iii | Black–Litterman blends expectations, confidence and history; "adjusts historically observed correlation levels" | Narang's description kept as his (p. 117); the correlation claim is in neither Narang nor Boyd et al., where the method shrinks the means toward market-implied returns (secs. 1.3, 3.4); not adopted. Note 5's 1982 against the text's 1992 recorded. Stub `mod:black-litterman` |
| 3.iv | Grinold–Kahn: portfolio of signals; rule-based factor portfolios backtested and optimised; "not more than 20"; inputs | `meth:signal-portfolio-allocation`: Narang's account with his 0.2% example checked; "about 20" kept as his unsourced statement; Grinold and Kahn unread |
| 3.v | Resampled efficiency reduces estimation error by Monte Carlo resampling | Qualified: Narang describes reordering observed returns and says mean and volatility stay the same (pp. 118–119), so the reordering he describes cannot change the optimiser's inputs; his example is strategy robustness. Michaud's actual procedure and its claimed improvement not checked. Stub `meth:resampled-efficiency` |
| 3.vi | Data mining: supervised learning or genetic algorithms because MVO searches many portfolios | Not in the third edition, which says few strictly ML portfolio models are seen (pp. 113–114). Not adopted: supervised learning fits forecasts, and convex problems need no generic search (Boyd et al. secs. 1.4, 4.3) |

No claim was deleted outright; the not-adopted claims stay in the artefact and are named in the entries.

**Existing entries and backlog checked.**
- `mod:portfolio-transaction-cost-function` (this pathway): cost inputs cross-referenced, not repeated; its Pitfalls now cite Boyd et al. secs. 2.4 and 4.3 for the computational remarks, and its Status records this.
- Stub `meth:convex-cost-portfolio-optimisation`: kept; its text now records that Boyd et al. was read in part, while the multi-period paper is unread.
- Stub `res:no-trade-region`: unchanged; not in the legacy file.
- Also cross-referenced, unchanged: `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting` (`backtest-inference`), `def:common-investor-contagion` (`funding-crowding`), `mod:almgren-chriss-execution` (`execution-trading-costs`).

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024 (copyright page: Third Edition, ISBN 9781119931911 Adobe PDF), the same local copy as slices 25–27, text layer through PDFKit. Chap. 6, "Portfolio Construction Models", secs. 6.1–6.5 and notes, pp. 99–125 (PDF pages 119–145; contents: chapter p. 99, notes p. 125; running heads checked). Read by page image: Exhibit 6.1 (p. 102), 6.2 (p. 107), 6.4 (p. 111), 6.5 (p. 112), 6.6 (p. 116), 6.7 (p. 122) and the worked example on p. 118. Exhibit 6.3 (p. 109) was read from the text layer only.
- **Boyd, Johansson, Kahn, Schiele and Schmelzer** (`wide-boyd-markowitz-seventy`), "Markowitz Portfolio Construction at Seventy", the authors' version of 5 January 2024 (53 pages), downloaded 2026-10-15 from the authors' page given in the catalogue; published in *Journal of Portfolio Management* 50(8), 117–160, 2024, whose pagination was not checked. Read: secs. 1.1–1.4 (pp. 3–10), 2.4 (p. 17), 3.2 (pp. 19–20), 3.4 (pp. 21–22), 4.3 (pp. 27–28), 5.6 with Table 2 (pp. 39–40). A reading note was opened.
- **Downloaded but not used:** Markowitz (1952) from the catalogue link, a scan with no text layer; not read.
- **Not read:** Black and Litterman (`alpha-black`), Michaud's book and paper, Grinold and Kahn (`alpha-grinold`), Bollerslev, Maillard–Roncalli–Teïletche, Ledoit–Wolf, Connor–Goldberg–Korajczyk, Johansson et al. (Narang's EWMA source), the multi-period paper.

### Numerical checks

Recomputed in the session with numpy and by hand; no script kept, and no existing script covers this content:
- Exhibit 6.1: inverse-variance weights 39.02/60.98% (the table's 39/61); inverse-volatility 44.44/55.56%; $w_i\sigma_i$ 1.111/1.111 against 0.976/1.220.
- Risk contributions: for two assets inverse-volatility weights give 50/50 at correlations −0.5, 0.1 and 0.8. For three assets at 20% volatility with $\rho_{12}=0.8$ and the third uncorrelated, equal weights give 39.13/39.13/21.74%; the ERC weights $a=1/(2+\sqrt{1.8})=0.2993$, $b=0.4015$ give 1/3 each (closed form and numerical check).
- Pairs: $2000^2=4{,}000{,}000$; $2000\times1999/2=1{,}999{,}000$.
- Grinold–Kahn example: $0.01\times0.6-0.01\times0.4=0.002$.
- Sharpe scale invariance: $\Sigma^{-1}\mu$ and $3\Sigma^{-1}\mu$ give the same ratio, 0.5596, for an illustrative two-asset $\mu$, $\Sigma$.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. 6, pp. 99–125; exhibits listed above as images | Third edition; one practitioner's account; GARCH prevalence, "about 20" factors, the users of each method, and the decision-tree details absent; some text–exhibit inconsistencies (Exhibit 6.1 labels; "high correlation" on p. 115 against about 0.1 on p. 106) |
| `wide-boyd-markowitz-seventy` | the sections listed | Authors' version, not the journal; one paper's view of the alleged deficiencies; timings are for one solver and hardware |
| Black–Litterman, Michaud, Grinold–Kahn, ERC, GARCH and covariance readings | none | Stubs; claims about them are limited to what Narang and Boyd et al. say |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/portfolio-construction-risk/portfolio-construction-models.tex`, with only the subsection unnumbered. A script compared it with `git show HEAD:compendium/legacy/portfolio-construction-risk/sysinv/portconstmod.tex`:
- the body below the subsection heading appears exactly once;
- the introduction (279 characters) appears once, before the blocks, and the remark's prose before its list (604 characters) once;
- the 3 blocks appear verbatim once each, in order;
- `\item` commands, matched as `\item` not followed by a letter, number 4, 3 and 6, 13 in both original and artefact; the substring count would have given 16, because of the 3 `\itemsep` lines;
- the sequence of 12 `\begin`/`\end` commands is identical (ignoring `document`);
- nothing lay outside the blocks but the migrate-to line, the subsection heading and the introduction.

The artefact compiles alone: 2 pages, no warnings, no bad boxes.

### Counts

`migration_status.py --check`, 0 problems: 598 → 595 legacy blocks = 530 shared + 36 single-candidate + 29 assigned. `portfolio-construction`: exclusive 7 → 4, entries 1 → 4, stubs 2 → 7. Other pathways unchanged (`execution-trading-costs` 14/1, `model-governance-controls` 3/4, `funding-crowding` 1/4, `backtest-inference` 4/8, `crypto-perpetuals` 3/5). Entries 99 → 102 (methods 17 → 19, models 11 → 12). Reading notes: `s7-narang` extended, `wide-boyd-markowitz-seventy` opened. No new `front/sources.tex` keys.

### Other files

- Chapter opener `compendium/portfolio-construction-risk/section.tex`: comment, paragraph and inputs.
- `notes/pathways/portfolio-construction.md`: status, entries, related entries, backlog, legacy material, one question.
- `notes/log.md`: the `portfolio-construction` coverage row, the `s7-narang` progress cell, one open question.
- `notes/migration.md`: status, index, next slice and map; `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 222 pages (219 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, all after the start of the legacy part in the log, as before. The first builds had one overfull and one underfull box from a pathway key and the artefact file name in *Further reading*, and an underfull opening line of the mean–variance Statement; the wording was changed and the file name put on its own line. Rendered and inspected: PDF pp. 21–24 (opener and the three new entries), p. 25 (the corrected cost-function notation), p. 93 (the corrected sell example) and p. 177 (the legacy portfolio chapter, where *Risk Models* now runs into *Execution Model*). Tests: 14 passed.

### For review

- The reading of Exhibit 6.1 as inverse-variance and the ERC distinction.
- The correction of the unconstrained single-asset claim, and the treatment of Black–Litterman and resampling on Narang's and Boyd et al.'s accounts alone.
- Keeping Grinold and Kahn's approach as a separate entry on Narang's account only.
- The not-adopted data-mining and decision-tree details, which may come from an earlier edition.

## Slice 28 follow-up: closed-form conditions, permutations, learning and rounding, 15 October 2026

Narrow corrections to slice 28 after an audit, run before slice 29; the slice-28 record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub, artefact or count changed (595 legacy blocks; 102 entries).

- **Closed form, `mod:mean-variance-portfolio-optimisation`.** The entry now states that $w^\star=\tfrac1{2\gamma}\Sigma^{-1}(\mu+\nu^\star\mathbf 1)$ assumes a positive-definite $\Sigma$ and $\gamma>0$, and gives $\nu^\star=(2\gamma-\mathbf 1^\top\Sigma^{-1}\mu)/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$, the budget constraint's dual variable (Boyd et al., p. 4), which shifts all expected returns equally so that the weights sum to one. The volatility-target form is feasible only when $\sigma_{\mathrm{tar}}^2\ge1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$, quoting Boyd et al.'s "can be infeasible when $\sigma^{\mathrm{tar}}$ is too small" (p. 4). A singular $\Sigma$ is said to need separate treatment, with no pseudoinverse by default.
- **Single asset, same entry.** Slice 28 said a single-asset answer arises "when risk is ignored". The entry now separates the bounded case (budget and no shorting: the highest-return asset) from the unbounded one (shorting allowed, returns not all equal) and box limits.
- **Resampling, same entry.** Slice 28 said Narang's remark "shows that reordering cannot change the sample means and covariances an optimiser uses". His remark concerns one series. The entry now says that reordering one series keeps its mean and variance, a common permutation of multivariate rows keeps covariances, and independent permutations change them; Michaud's procedure and performance claims remain unchecked.
- **Machine learning, same entry.** "Supervised learning fits a forecast; it does not choose weights" is replaced by a distinction between forecasting, learning allocation weights (possible; its literature not read) and optimisation, keeping the narrower conclusion that the legacy item lacks source support.
- **ERC rounding and positive variance, `meth:rule-based-position-sizing`.** The displayed weights 29.9, 29.9 and 40.2 percent did not match the stored calculation ($b=0.401492$ rounds to 40.1); they now read about 29.93, 29.93 and 40.15 percent with their closed form. Normalised risk contributions are stated to require $w^\top\Sigma w>0$.
- **Transaction-cost entry.** `mod:portfolio-transaction-cost-function`'s *Further reading* and *Status* no longer say that no pathway reading was read; they name the parts of Boyd et al. read in slice 28.
- **Checks**, in the session with numpy (no script kept): for a three-asset positive-definite $\Sigma$ (eigenvalues 0.0219, 0.0374, 0.0932), $\gamma=1$ and $\gamma=5$ give $\nu^\star=-0.0555$ and $0.0562$, weights summing to 1 and first-order residuals below $10^{-16}$; minimum variance 0.01396; with $\gamma=0$ the direction $(1,0,-1)$ raises return by 0.03 per unit with unchanged budget, so the problem is unbounded; two perfectly correlated assets give eigenvalues 0 and 0.08. Permutation: $x=y=(1,2,3,4)$, covariance 1.25; reversing $y$ alone gives $-1.25$ with means 2.5 and variances 1.25 unchanged; a common permutation keeps 1.25. ERC: 29.9254, 29.9254, 40.1492 percent; equal weights give 39.13, 39.13, 21.74 percent at variance 0.02044.
- **Notes and index.** The `portfolio-construction` note records the changes; `log.md` keeps its slice-28 line and gains a dated line narrowing it; the slice-28 index row gives `4e7666d`.

## Slice 29: risk models (factor exposures, limits and penalties), 15 October 2026

Migration of the risk-models file of Narang's systematic-investing notes, run after the slice-28 follow-up above. Migration and source checking, not study; no checkpoint was attempted. Two further sections of Boyd et al., a reading of the owning pathway, were read for method mechanics.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/riskmod.tex`: an introductory paragraph outside the environments, and 4 counted `method` blocks with 9 `\item` commands (4 in *Factor-Based Models*, 3 in *Statistical Models*, none in *Limiting Size of Risk*, which is prose only, and 2 in *Limiting the Types of Risk*), with the prose around them; the three `\setlength{\itemsep}{0pt}` lines are not items. Outside the blocks were only the `% migrate-to:` line, the subsection heading and the introduction (checked by script). The file and its map row were deleted; in `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The remaining `sysinv/` files (`alphamod.tex`, `executionmod.tex`, `sysinvoverview.tex` with its method block), their inputs and the chapter wrappers, other legacy files, earlier artefacts (slices 27 and 28 included), the deferred assignments, the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map's only candidate is `portfolio-construction` ("construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk"). The factor-model, size-limit and exposure-type material is that pathway's. The *Statistical Models* block lists historical simulation, Monte Carlo simulation and parametric methods for "risk metrics" and "key risk measures"; it is about estimating portfolio risk measures, not about the covariance an optimiser uses. `risk-tail-systemic` has the outcome "forecast and backtest VaR and ES, design a tail hedge, and run a stress test", with a checkpoint built on filtered historical simulation and EVT. **Routing exception:** that block goes to `risk-tail-systemic`, as a backlog item only (`meth:var-es-estimation-methods`), because its text is generic, absent from Narang's chapter, and supports no entry; this slice opened `notes/pathways/risk-tail-systemic.md`. Nothing went to `time-series-volatility`: the block does not discuss GARCH, and `mod:garch-volatility-forecast` is unchanged.

One new entry, `mod:factor-risk-model`, in the new topic file `compendium/portfolio-construction-risk/risk-models.tex`; the size-limit block merged into `mod:mean-variance-portfolio-optimisation`. The artefact is a new file, `notes/artefacts/portfolio-construction-risk/risk-models.tex`, beside those of slices 27 and 28.

| Part | Legacy text | Owner | Destination | Checked source | Disposition |
|---|---|---|---|---|---|
| Intro | Risk model concerns intentional selection and sizing of exposures; alpha exposure accepted for long-run profit | `portfolio-construction` | `mod:factor-risk-model` (Statement, Pitfalls) | Narang chap. 4, pp. 71–73; Exhibit 4.1, p. 83 by page image | Corrected: Narang says this of risk *management*; the risk model is an input to the portfolio decision |
| 1 | *Factor-Based Models* (method), items i–iv | `portfolio-construction` | `mod:factor-risk-model` (new) | Boyd et al. sec. 3.3, pp. 20–21; Narang pp. 71–72, 77–78 | Rewritten with the factor covariance and its assumptions; the factor list qualified |
| 2 | *Statistical Models* (method), items i–iii | `risk-tail-systemic` | stub `meth:var-es-estimation-methods` (new note) | none in Narang's chapter | Stubbed, not written as an entry |
| 3 | *Limiting Size of Risk* (method), prose | `portfolio-construction` | merged into `mod:mean-variance-portfolio-optimisation` (Practice, Pitfalls) | Narang secs. 4.1–4.1.3, pp. 73–76; Boyd et al. sec. 4.2, pp. 25–27 | Merged with corrections |
| 4 | *Limiting the Types of Risk* (method), items i–ii | `portfolio-construction` | `mod:factor-risk-model` (Conditions, Practice, Pitfalls) | Narang secs. 4.2–4.2.3, pp. 76–81 | Rewritten with qualifications |

**Subclaims.**

| Where | Legacy claim | Disposition |
|---|---|---|
| Intro | "Risk model concerns the intentional selection and sizing of exposures to improve the quality and consistency of returns" | Corrected: Narang's sentence is about risk management (p. 71); the risk model measures and flags exposures and feeds portfolio construction (p. 72, Exhibit 4.1) |
| Intro | Alpha exposure accepted for long-run profit | Rewritten as his definition: risks are the exposures not intentionally forecast (pp. 71–72) |
| 1 stem | Returns decomposed into systematic factors and idiosyncratic components | Rewritten with Boyd et al.'s $r=Ff+\epsilon$, $\Sigma=F\Sigma_fF^\top+D$ and its assumptions (uncorrelated $f$ and $\epsilon$, diagonal $D$) |
| 1.i–iv | Market, size, value, momentum as "the most common factors"; size and value as risks; momentum as a tendency | Qualified: the list is not in Narang's chap. 4, which names market, sector and market-cap risk (pp. 77–78) and uses value as an alpha (pp. 71–72); whether a factor is a risk, a signal or a premium depends on the strategy's forecasts. Boyd et al.'s market, industry and style (Fama–French) factors cited |
| 1 close | Lets traders see what drives risk and adjust exposures | Rewritten as Narang's uses: measure, explain P&L, model residuals (pp. 72, 82–83); the adjustment is the portfolio decision |
| 2.i–iii | Historical simulation, Monte Carlo, parametric methods | Stubbed in `risk-tail-systemic`, with the methods treated as overlapping (filtered historical simulation mixes a volatility model with historical residuals; Monte Carlo draws from a parametric or resampled model) |
| 2 close | "Useful for dynamically updating risk assessments" | Stubbed with the qualification that updating is not evidence of better forecasts |
| 3 | Limits vary by how size is limited, how risk is measured, what is limited | Merged (p. 73) |
| 3 | Hard constraints and penalties; penalty lets a position pass the limit only for a larger expected return | Merged with his 3% example (pp. 73–74) and Boyd et al.'s softening, which replaces a hard constraint by a penalty and keeps mandated limits hard (pp. 25–27): a penalty does not permit breaching a separate hard cap |
| 3 | Levels from theory or data | Merged (p. 74), with the overfitting link |
| 3 | Two ways to measure risk: volatility (longitudinal) and correlation/covariance (dispersion) | Corrected: Narang's dispersion is the cross-sectional standard deviation or correlation (pp. 74–75); a covariance risk model contains volatilities and correlations together; his "higher dispersion, less risky" not adopted |
| 3 | Limits on positions, groups, risk types, leverage | Merged (p. 75); his VaR-based leverage critique noted, and his description of VaR as a one-standard-deviation move not adopted (pp. 75–76) |
| 4 stem | Eliminate unintentional exposure, "no expectation of being compensated" | Kept as Narang's rule (p. 76), qualified: unintended is not the same as uncompensated; his CVX/XOM and value-sector examples given |
| 4 stem | Through theoretical or empirical risk models | Rewritten (pp. 76–80), with his preference for building exposure control into alpha models (pp. 80–81) |
| 4.i | Theory-driven: systematic factors from economic theory; "cannot be diversified away"; market, sector, cap; rates | Rewritten (pp. 77–78), with the diversification condition shown numerically (residuals diversify only if uncorrelated) |
| 4.ii | Empirical: PCA finds unnamed systematic risks; used by stat-arb traders | Rewritten (p. 78): PCA factors need not have stable names (sign, order and composition can change; interpretation), may be spurious (his caution); "used by" corrected to his "most commonly found among"; adaptiveness against data needs (p. 79) |

No claim was deleted outright.

**Existing coverage checked.**
- `mod:mean-variance-portfolio-optimisation`: the destination of block 3; its *Practice* gains a size-limits passage and its *Pitfalls* a volatility-and-covariance passage, and its Status is updated.
- `meth:rule-based-position-sizing`, `meth:signal-portfolio-allocation`, `mod:portfolio-transaction-cost-function`: no overlap beyond cross-references; unchanged in this slice (the first two were corrected in the follow-up above).
- Stub `meth:portfolio-covariance-estimation`: narrowed to estimation (shrinkage, fitting a factor model, out-of-sample tests), since the factor model's structure is now in the new entry.
- Stub `mod:garch-volatility-forecast` (home `time-series-volatility`): unchanged; the statistical block does not discuss GARCH.
- Cross-referenced, unchanged: `def:quant-strategy-risk-sources` (`model-governance-controls`), `def:common-investor-contagion` (`funding-crowding`), `pit:parameter-overfitting` (`backtest-inference`).

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024, the same local copy as slices 25–28, text layer through PDFKit. Chap. 4, "Risk Models", secs. 4.1–4.4 and notes, pp. 71–84 (PDF pages 91–104; contents: chap. 4 p. 71, notes p. 84; running heads checked). Its only exhibit, 4.1 (p. 83), the black-box schematic, was read by page image; the chapter has no data exhibits.
- **Boyd et al.** (`wide-boyd-markowitz-seventy`), authors' version of 5 January 2024, the same copy as slice 28: sec. 3.3, factor model (pp. 20–21), and sec. 4.2, softening constraints (pp. 25–27). The reading note records them.
- **Not read:** the readings of `risk-tail-systemic` (VaR, ES, historical simulation, backtests), the factor-premia and covariance-estimation readings (`wide-connor-goldberg-korajczyk`, `wide-ledoit-wolf-review`), and any PCA reading.

### Numerical checks

In the session with numpy; no script kept, and no existing script covers this content:
- One-factor model, unit loadings, factor volatility 15%, residual 30%, equal weights: portfolio variance 0.1125, 0.0315, 0.0234, 0.02259 (volatility 33.5, 17.8, 15.3, 15.0%) for $n=1$, 10, 100, 1,000; factor part fixed at 0.0225.
- Residuals with correlation 0.2 and variance 0.09, 1,000 assets: residual variance 0.01807, above the floor $0.2\times0.09=0.018$.
- Neutrality: loadings $(1,0.5)$, $(1,-0.5)$, $(0.8,1)$, $\Sigma_f=\begin{pmatrix}0.04&0.012\\0.012&0.01\end{pmatrix}$, $w=(0.5,-0.5,0)$: exposures $(0,0.5)$, covariance with the factors $(0.006,0.005)$.
- PCA sign: the eigenvectors of a 2×2 correlation matrix with $\rho=0.6$ are returned with arbitrary sign (eigenvalues 0.4 and 1.6).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. 4, pp. 71–84; Exhibit 4.1 as image | Third edition; one practitioner's account with no data; his VaR description and dispersion inference not adopted; the legacy factor list and statistical block absent |
| `wide-boyd-markowitz-seventy` | secs. 3.3, 4.2 | Authors' version; the factor model stated, not estimated |
| VaR/ES, factor-premia and covariance-estimation readings | none | Stubs; "unintended is not uncompensated" is interpretation |

The new entry and the merged passages are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in the new artefact `notes/artefacts/portfolio-construction-risk/risk-models.tex`, with only the subsection unnumbered. A script compared it with `git show HEAD:compendium/legacy/portfolio-construction-risk/sysinv/riskmod.tex`:
- the body below the subsection heading appears exactly once;
- the introduction (223 characters) appears once, before the blocks;
- the 4 blocks appear verbatim once each, in order (773, 688, 958 and 967 characters, all prose included);
- `\item` commands, matched as `\item` not followed by a letter, number 4, 3, 0 and 2, 9 in both original and artefact; the substring count would give 12, because of the 3 `\itemsep` lines;
- the sequence of 14 `\begin`/`\end` commands is identical (ignoring `document`);
- nothing lay outside the blocks but the migrate-to line, the subsection heading and the introduction.

The artefact compiles alone: 1 page, no warnings, no bad boxes; its page image was inspected.

### Counts

`migration_status.py --check`, 0 problems: 595 → 591 legacy blocks = 530 shared + 32 single-candidate + 29 assigned. `portfolio-construction`: exclusive 4 → 0, entries 4 → 5, stubs 7 (one narrowed). `risk-tail-systemic`: entries 0, stubs 0 → 1 (new note). `portfolio-construction-risk` (overview): exclusive 8, unchanged. Other pathways unchanged (`execution-trading-costs` 14/1, `model-governance-controls` 3/4, `funding-crowding` 1/4, `backtest-inference` 4/8, `crypto-perpetuals` 3/5). Entries 102 → 103 (models 12 → 13). No new `front/sources.tex` keys.

`portfolio-construction` now has no legacy file listing it alone. That is migration progress only: its backlog is open, no reading has been studied, and the remaining `sysinv/` files, mapped to the overview, may still bear on it.

### Other files

- Chapter opener `compendium/portfolio-construction-risk/section.tex`: comment, paragraph and inputs.
- `notes/pathways/portfolio-construction.md` (entries, related entries, backlog, legacy material); `notes/pathways/risk-tail-systemic.md` (new).
- `notes/readings/s7-narang.md` and `notes/readings/wide-boyd-markowitz-seventy.md`.
- `notes/log.md`: coverage rows for `portfolio-construction` and `risk-tail-systemic`, the `s7-narang` progress cell, one open question.
- `notes/migration.md`: status, index, next slice and map; `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 223 pages (222 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, all after the start of the legacy part in the log, as before. No new bad boxes at any stage. Rendered and inspected: PDF pp. 22–24 (the slice-28 corrections and the merged size-limit and covariance passages), pp. 25–26 (the factor-risk-model entry), p. 177 (the legacy portfolio chapter, where the overview's method block now runs into *Alpha Models Overview*), and the artefact's page. Tests: 14 passed.

### For review

- Routing the statistical-methods block to `risk-tail-systemic` as a backlog item only, and opening that note without entries.
- Reading the legacy factor list as roles that depend on the strategy, and "unintended is not uncompensated".
- Merging the size-limit material into the mean–variance entry, including the softening reading of penalties and the non-adoption of Narang's VaR and dispersion statements.
