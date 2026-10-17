# Source-review records

The full record of each entry editing, from the baseline to the the topic review, in order: scope, sources and their availability, source findings, checks and their limits, dispositions of every legacy block, counts, build and items for review. Dates, results and source identities describe the original reviews; topic names and paths use the current naming conventions. Corrections appear beside the findings they qualify. The conventions, current status, topic index and file map are in [source-review-index.md](source-review-index.md). Open questions arising from the topic review are also logged in [log.md](log.md).

## Baseline: 14 October 2026, before source organisation (commit `9634e2b`)

- **Blocks:** 879 in the old environments, of which 12 were in the tooling appendix and 867 in the finance chapters: `taxonomy` 178, `remark` 146, `caveat` 113, `definition` 98, `mechanism` 81, `principle` 80, `model` 58, `method` 31, `proposition` 25, `process` 18, `marketrule` 18, `practitionernote` 14, `empiricalfinding` 11, `casestudy` 3, `notation` 2, `corollary` 2, `lemma` 1.
- **Labels:** five figure labels and one remark label (`rmk:propfracdifffeat`); no entry labels.
- **Figures:** the 21 PNG files in `execution-trading-costs/figures/` were referenced by no file.
- **Build** (`latexmk -g -pdf compendium.tex`, TeX Live, pdfTeX): exit 0; 143 pages; no LaTeX warnings, no undefined references or citations; 0 overfull and 30 underfull boxes; 7 pdfTeX warnings for duplicate destinations (`page.i` and six `figure.*` anchors).

## source organisation: done 14 October 2026

1. Moved the seven chapters unchanged (`git mv`) to `compendium/legacy/<section-key>/`, rewrote their `\input` and figure paths, renamed their chapter labels to `legacy:<section-key>` and the one cross-chapter reference, and compiled them as *Notes awaiting migration*. The 21 unused execution figures moved with `legacy/execution-trading-costs/figures/`.
2. Moved the tooling appendix (calculator, reading AI papers, Python, VS Code), with its figures and its three sources (`downey-2015`, `ramalho-2015`, `speight-2021`), to `notes/tooling/`, which compiles on its own (`latexmk -pdf tooling.tex`). The VS Code and Python files stay commented out of it, as they were; they also compile when enabled.
3. Replaced the placeholder preface (*Lorem Ipsum* overview and roadmap) with a short description of the layout, keeping its acknowledgement of Narang, Velu and López de Prado.
4. Moved `hyperref` to the end of `compendium/preamble.tex`: loaded before `float` and `algorithm`, it gave every captioned figure a duplicate anchor. `house.tex` and the guide submodule are unchanged.
5. Added this file, the `% migrate-to:` lines in 71 legacy files, and `tools/check_compendium.py` with its tests (`python3 -m unittest discover -s tools`).
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

As at the pilot; rechecked in dealer-information models review below, which unblocked Grossman–Miller through its NBER working paper and the `crypto-cartea` p. 33 misprint through the authors' errata. spread and inventory models review migrated *Inventory-Skew Quoting* from textbook accounts (Hasbrouck's version of Stoll (1978); O'Hara's report of Ho–Stoll); the Ho–Stoll paper itself is still needed, for the backlog stub `res:ho-stoll-dealer-pricing`.

| Needed | Why | Passage required |
|---|---|---|
| Ho and Stoll (1981), *Journal of Financial Economics* 9(1) (`ho-stoll-1981`); the route reads it through `catalogue-0527`, which names no paper | `market-making-lob` requires a Ho–Stoll inventory entry; the legacy *Inventory-Skew Quoting* block cannot be sourced without it | The section deriving the dealer's optimal bid and ask as functions of inventory, with the equation numbers |
| Grossman and Miller (1988), *Journal of Finance* 43(3) (`grossman-miller-1988`) | Two legacy implications are not in `crypto-cartea` | The participation-cost (entry) stage and the discussion of market structure for large orders |
| Kyle (1985), *Econometrica* 53(6) (`s6-kyle`) | To check the single-auction results at the original, and the misprint in `crypto-cartea` p. 33 | The single-auction equilibrium theorem and its proof |

### Build after the pilot

`latexmk -g -pdf compendium.tex`: exit 0; 139 pages (the tooling appendix left; six entries came in); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes; one pdfTeX duplicate-destination warning, `page.i`, inherited from `\maketitle` before the roman-numbered front matter. Rendered and inspected: the contents, notation and preface; the new chapter (pp. 1–5; pp. 2 and 4 at full size, with both figures); the part title page (p. 6); and the pruned legacy market-making section (p. 116).

## dealer-information models review: Glosten–Milgrom and the dealer material, 15 October 2026

Migration of the `market-making-lob` candidate blocks named as the the topic review, run from the pilot's pushed state (`ce64308`, pushed straight to `main`, no pull request). It is migration and source checking, not study: the pathway is neither mastered nor consolidated, and its Methods readings are untouched.

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

Four legacy files emptied and were deleted, with their `\input` lines and map rows: `03_.../05_information_based_models.tex`, `05_.../02_avellaneda_stoikov_framework.tex`, `05_.../03_adverse_selection_and_toxic_flow.tex` and `05_.../07_risk_management_for_market_makers.tex`. Their `% migrated:` comments are recorded above. Every removed block and table is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Glosten–Milgrom and dealer quoting (dealer-information models review)*.

### Counts

`check_compendium.py`: 858 → 840 legacy blocks (18 migrated: 3 + 1 + 5 + 4 + 3 + 2). Assigned 2 → 19 (+11 `execution-market-making`, +7 `hft-market-design`, −1 for *Quote-Control Segmentation*, migrated); one candidate only 144 → 135 (the 9 blocks of the two deleted single-candidate files); shared 712 → 686 (−3 migrated from `03_.../05`, −5 migrated and −18 assigned from `05_.../01`, `04`, `05`). Entries 6 → 12. No block is counted twice: an assigned block counts only towards its pathway.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 142 pages (139 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy part; the one pre-existing `page.i` duplicate-destination warning. A first build had one new overfull box (an artefact path in *Further reading*) and one new underfull box (in the Glosten–Milgrom entry's *Pitfalls*); both were reworded away. Rendered and inspected: the notation overrides (p. iv), the new sections (pp. 5–10) and the pruned legacy market-making section (p. 119). The artefact `derivations.tex` compiles on its own: 10 pages, no warnings, the same 3 underfull boxes as before. The tooling appendix was not affected and was not rebuilt.

### For review

- All six new entries: wording, the interpretations they flag, and the locators. In particular, check whether citing Harris rather than Glosten and Milgrom for the $2\alpha e$ result is the attribution you want.
- Whether the working-paper keys (`glosten-milgrom-1983`, `grossman-miller-1988-nber`) should stay as separate sources or be replaced by the journal versions once those are read.
- The cross-asset arbitrage file (`05_.../06`): its candidate list (`market-making-lob`, `hft-market-design`) looks wrong; `execution-market-making` (Harris, chap. "Arbitrageurs") or the asset-class pathways seem closer. The list was left unchanged.
- The 9 + 2 blocks assigned to `execution-market-making` and the 7 assigned to `hft-market-design`: the assignments are provisional and can be changed with their `% assign:` lines.

## spread and inventory models review: spread decomposition and inventory models, 15 October 2026

Migration of the two files named as the selected topic, run from dealer-information models review's pushed state (`07a0504`, on `main`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Scope

All 21 blocks of `03_.../03_bid_ask_spread_decomposition.tex` (17) and `03_.../04_inventory_models.tex` (4), shared between `execution-market-making` and `market-making-lob`, one of them (*Inventory-Skew Quoting*) assigned to `market-making-lob`. Every block was merged into an existing entry or into one of six new ones; both files emptied and were deleted.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF outside the repository, as in dealer-information models review (2002 Oxford printing; printed page = PDF page − 13) | As in dealer-information models review |
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

`meth:dealer-quote-adjustment` gained cross-references only. Both legacy files were deleted with their `\input` lines and map rows; their full text, with the `% migrated:` destinations above, is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Spread decomposition and inventory models (spread and inventory models review)*. A script confirmed every line of both files is there, in order.

### Counts

`check_compendium.py`: 840 → 819 legacy blocks (21 migrated: 17 + 4). Assigned 19 → 18 (*Inventory-Skew Quoting*, migrated); one candidate only 135 → 135; shared 686 → 666 (the other 20). Entries 12 → 18 (definitions 1 → 3, models 5 → 6, results 5 → 8, methods 1). `market-making-lob`: 0 assigned, 166 shared, 18 entries, 5 stubs. No block is counted twice. One notation override row added (`front/notation.tex`: $A$, $C$, $Q_t$, $q_t$).

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 145 pages (142 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one pre-existing `page.i` duplicate-destination warning. Rendered and inspected: notation overrides (p. iv), the revised and new entries (PDF pp. 14–22, chapter pp. 8–16) and the pruned legacy section (PDF p. 112). The artefact compiles on its own: 12 pages (10 before), no warnings, the same 3 underfull boxes. The tooling appendix was not affected and was not rebuilt.

### For review

- The six new entries and the three revised ones; in particular the corrected reading of the equivalence proposition, the Roll bias directions, and whether `mod:inventory-based-quotes` should be split into a Stoll entry and a Ho–Stoll entry once the paper is read.
- The five measurement entries (`def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `res:spread-determinants`, `def:outside-spread`) serve the section overview route `execution-market-making`, whose required readings include `s6-hasbrouck`; they are listed in the `market-making-lob` note because that route has no pathway note yet.
- The new notation override row, and the per-side versus full-spread conventions it records.

## volatility and liquidity review: volatility and liquidity, 15 October 2026

Migration of the file named as the selected topic, run from spread and inventory models review's pushed state (`79aa634`, on `main`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Scope

The 22 blocks of `03_.../08_volatility_and_liquidity_interaction.tex`, shared between `execution-market-making` and `market-making-lob`. Fourteen were migrated. The other eight (liquidity spiral, Flash Crash case and toy model, hot-potato amplification, flash-crash controls, systemic-risk link, shock propagation, trade count as HFT proxy) were assigned to `hft-market-design`, whose required readings include the Flash Crash paper (`w5-kirilenko-flash-crash`) and whose optional branch includes `w5-menkveld-yueshen-flash`; they stay in legacy. To allow the assignment, `hft-market-design` was added to the file's `% migrate-to:` line and its map row. The file is therefore not deleted.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF, as in dealer-information models / spread and inventory models reviews | As before |
| `s6-hasbrouck` | Local PDF, as in spread and inventory models review | As before |
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

`res:roll-spread-estimator` gained a cross-reference only. The 14 migrated blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Volatility, liquidity and crashes (volatility and liquidity review)*; a script confirmed they are there, contiguous and in order, and that the 8 blocks left in the legacy file are unchanged.

### Counts

`check_compendium.py`: 819 → 805 legacy blocks (14 migrated). Assigned 18 → 26 (+8 `hft-market-design`, now 15); one candidate only 135 → 135; shared 666 → 644 (−14 migrated, −8 assigned). Entries 18 → 22 (definitions 3 → 4, methods 1 → 3, mechanisms 0 → 1). `market-making-lob`: 0 assigned, 144 shared, 22 entries listed, 5 stubs. No block is counted twice. No notation override was added: $A_0$ and the $p^O,p^H,p^L,p^C$ superscripts are explained in the entries' Notation fields.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 148 pages (145 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had three new underfull boxes in the new entries; they were reworded away. Rendered and inspected: the new section (PDF pp. 22–26) and the pruned legacy section (PDF p. 121). The artefact compiles on its own: 13 pages (12 before), no warnings, the same 3 underfull boxes. The tooling appendix was not affected and was not rebuilt.

### For review

- The four new entries and the two revised ones; in particular the decision to make the regressions a method entry rather than part of `res:spread-determinants`, and the own-derivation notes (the predictor's unbiasedness, the variance split's covariance term).
- The assignment of the eight flash-crash and systemic blocks to `hft-market-design`. *Systemic Risk Link* and *Shock Propagation Channels* concern fragmentation and could instead go to `market-structure-execution-quality`; *Liquidity Spiral* is general enough for `execution-market-making`.
- The (A.14) exponent in Lehalle and Laruelle's toy model, before that block is migrated.
- As in spread and inventory models review, the new entries serve the overview route `execution-market-making` and are listed in the `market-making-lob` note only because that route has no note.

## information and price discovery review: information, market efficiency and price discovery, 15 October 2026

Migration of the two files named as the selected topic, run from volatility and liquidity review's pushed state (`326ad36`, on `main`, matching `origin/main`; guide submodule at `343d145`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied. The volatility and liquidity review overlap list was judged from titles; each candidate overlap below was settled by comparing definitions and claims.

### Scope

The 21 blocks of `03_.../01_information_and_market_efficiency.tex` (9) and `03_.../02_price_discovery.tex` (12), both shared between `execution-market-making` and `market-making-lob`. Eighteen were migrated, into six new entries and one revised entry. Three were assigned elsewhere and stay in legacy. The first file is empty and was deleted, with its `\input` line in `03_.../00_overview.tex`.

### Routing decisions

- **Overview route note.** The guide runs one study loop per section overview, and an overview route's key doubles as its section key (guide, *Keys, layers and registers* and *The study loop*). So `notes/pathways/execution-market-making.md` was created for the existing route `execution-market-making`. The nine spread and inventory models review and volatility and liquidity review entries listed provisionally in `market-making-lob.md` (`def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `res:spread-determinants`, `def:outside-spread`, `def:volatility-components`, `meth:garman-klass-volatility`, `meth:spread-volatility-regression`, `mech:bubble-crash-dynamics`) moved there with the six new ones. The dealer entries stay with `market-making-lob`, whose second reading is on dealer inventory. Entry labels, files and the derivations artefact path are unchanged.
- **Taxonomy used.** `market-structure-execution-quality`: "how fragmentation, dark trading, fees, tick size, odd lots, retail routing and trading hours affect execution quality", with O'Hara and Ye on fragmentation. `hft-market-design`: "how speed, latency races and fast arbitrage affect liquidity, price discovery and the costs borne by slower traders", with the Flash Crash readings.
- ***Fragmentation and Price Formation*** and ***Outage Price Discovery*** → `market-structure-execution-quality`. Their mechanism is fragmentation itself: a common reference, stale primary quotes, pegged orders and the consolidated tape. Lehalle and Laruelle frame the outage this way (Introduction, pp. 5–7; chap. 2, sec. 2.5.2, pp. 183–186).
- ***Fast Liquidity and Price Discovery*** → `hft-market-design`. Its mechanism is fast market makers, speed investment and queue priority. Its fee-schedule point is secondary relevance to `market-structure-execution-quality`, for a cross-reference when migrated. Lehalle and Laruelle's source for it is app. A.2 (pp. 250–251), their summary of Foucault, Kadan and Kandel (2009), not read here.
- **volatility and liquidity review systemic assignments, reassessed.** *Systemic Risk Link* → `market-structure-execution-quality`. Its claim is that fragmentation is not systemic risk by itself, but becomes dangerous through same-direction reactions, desynchronised venues and propagation to hedges. The subject is fragmentation's effect on market quality, not speed. *Shock Propagation Channels* stays with `hft-market-design`. Its channels are the Flash Crash mechanisms of linked electronic markets: high-frequency market makers hedging across futures and equities, routers pausing, pegged orders losing their reference, kill switches (Lehalle and Laruelle, sec. 2.5.2, p. 183). That pathway's readings cover them (`w5-kirilenko-flash-crash`, optional `w5-menkveld-yueshen-flash`). The reassignment migrates nothing; the block is unchanged.
- **Insider-information blocks.** No pathway in the pinned taxonomy covers insider-trading law for securities. The prediction-market and crypto pathways that mention insiders concern those markets, and `model-governance-controls` covers model risk and algorithm controls. Harris, a reading of the overview route, gives the economic definition and the U.S. summary, so the three blocks were migrated into one entry under that route, with its legal content dated 2002.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF, as in dealer-information models / volatility and liquidity reviews (printed page = PDF page − 13) | As before |
| `s6-hasbrouck` | Local PDF, as in spread and inventory models / volatility and liquidity reviews (printed page = PDF page − 11) | As before |
| `alpha-laruelle` | Local PDF, as in volatility and liquidity review (printed page = PDF page − 27, Introduction included) | As before |

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
- **Not reopened.** The volatility and liquidity review question on the toy model's eq. (A.14) does not bear on these blocks and stays open. Sec. 2.5.3 (pp. 187–189) was not read; nothing here depends on it.

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
| `08_...`: *Systemic Risk Link* (volatility and liquidity review) | Reassigned from `hft-market-design` to `market-structure-execution-quality`, left in legacy |

Cross-references only: `def:volatility-components` and `meth:garman-klass-volatility`. The 18 migrated blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Information, market efficiency and price discovery (information and price discovery review)*. A script confirmed four things: each block appears there exactly once and in order; the artefact's earlier content is unchanged; the three blocks left in `02_...` are unchanged; and the eight blocks of `08_...` are unchanged (only the assignment line before *Systemic Risk Link* and the file's `% migrate-to:` line changed). `market-structure-execution-quality` was added to the `% migrate-to:` lines of `02_...` and `08_...`, and `hft-market-design` to that of `02_...`, with their map rows.

### Counts

`check_compendium.py`: 805 → 787 legacy blocks (18 migrated). Assigned 26 → 29: `market-structure-execution-quality` 0 → 3 (two from `02_...`, *Systemic Risk Link* from `08_...`); `hft-market-design` 15 → 15 (one added, one moved out). One candidate only 135 → 135. Shared 644 → 623 (−18 migrated, −3 assigned). Entries 22 → 28 (definitions 4 → 9, results 8 → 9). Entries listed by pathway note: `execution-market-making` 0 → 15, `market-making-lob` 22 → 13 (nine moved, none deleted). No block is counted twice. No notation override was added: $V_t$, $P_t$, $\epsilon_t$, $f_i$, $e_i$ and the return superscripts are defined in the entries.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 152 pages (148 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. Rendered and inspected: the new section (PDF pp. 11–16), the revised outside spread (pp. 26–27), the new returns entry (pp. 29–30) and the pruned legacy section (p. 122). The chapter opener (p. 7) was also inspected. The artefact compiles on its own: 15 pages (13 before), no warnings, the same 3 underfull boxes; its new section (p. 14) was inspected. The tooling appendix was not affected and was not rebuilt.

### For review

- The six new entries and the revised outside spread, in particular:
  - the decision to keep Harris's fundamental value apart from Hasbrouck's efficient price;
  - the own-derivation notes: the variance of the average, correlated errors, squared and absolute errors, the no-trade band, and the return identity;
  - the insider entry's scope: economic definition plus dated U.S. summary, with no current law.
- The routing above: the three assignments of `02_...` and the reassignment of *Systemic Risk Link*.
- The new overview note and the nine entries moved into it.
- `03_.../06_strategic_trading_models.tex` repeats the topic review material (informed-trader styles, trading speed, insider-trading profitability and deterrence): consolidate it into these entries next.

## strategic trading review: strategic trading models, 15 October 2026

Migration of the file named as the selected topic, run from information and price discovery review's pushed state (`80810ee`, on `main`, matching `origin/main`; guide submodule at `343d145`). Migration and source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Scope

The 30 blocks of `03_.../06_strategic_trading_models.tex`, shared between `execution-market-making` and `market-making-lob`. All 30 were migrated: 21 into seven new entries, 9 merged into new or existing entries. The file was deleted, with its `\input` line in `03_.../00_overview.tex` and its map row.

### Routing

Every block's source is Harris (`alpha-harris`), a reading of the overview route, and none concerns market making specifically, so all went to `execution-market-making`; nothing was put under `market-making-lob` by default. The pinned taxonomy has no general pathway for arbitrageurs, order anticipators or bluffers. The candidates are asset-specific or about funding (`statistical-arbitrage`, `commodity-spatial-arbitrage`, `fx-cip-dollar-funding`, `funding-crowding`, `futures-delivery-manipulation`, `crypto-exchange-market-quality`, `prediction-integrity`); the entries cross-reference them by key. *Specialist Order-Flow Strategy Segmentation* (Harris chap. 24) was merged into the order-anticipation entry rather than assigned to `market-structure-execution-quality`. Harris presents the specialists' quote matching and stop-order tactics as the order-anticipation strategies of chap. 11 (pp. 502–503), and the entry dates the specialist material to 2002. Settled routing decisions are unchanged.

### Sources and availability, 2026-10-15

`alpha-harris`, the local PDF used in dealer-information models / information and price discovery reviews (printed page = PDF page − 13); text layer for all passages; page images of p. 225 (the aggregation box) and p. 270 (the bluffing example). No other source was needed.

### Overlaps resolved, from content

- **Informed-trader styles** were not in `res:informed-trading-aggregation`, which is about how prices aggregate estimates. So a new definition, `def:informed-trader-types` (Harris sec. 10.5, Table 10-3). *Value Traders vs News Traders* merged into it: it adds who loses to whom, beyond the profit sources already in `def:outside-spread`.
- **Trading speed** (aggressive, stealth) and **orthogonal information** were already in the Practice of `res:informed-trading-aggregation` from information and price discovery review. They were merged there with what the blocks added: the reasons for each speed, and the precision–orthogonality trade-off of p. 237. The legacy "inactive" speed is stale information, not a speed.
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
- **Harris's comparison, rechecked against the page image of p. 225.** information and price discovery review's statement ("holds for squared errors, not absolute") was true only realisation by realisation, so it was restated by loss measure:
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

`def:outside-spread` gained cross-references only. The 30 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Strategic trading models (strategic trading review)*. A script confirmed three things: each block appears there exactly once and in order; the artefact's earlier content is unchanged; and `02_...` and `08_...` are byte-identical to their state before the topic review.

### Counts

`check_compendium.py`: 787 → 757 legacy blocks (30 migrated). Assigned 29 → 29; one candidate only 135 → 135; shared 623 → 593. Entries 28 → 35 (definitions 9 → 14, results 9 → 11). Entries listed in pathway notes: `execution-market-making` 15 → 22, `market-making-lob` 13 → 13. No notation override was added.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 155 pages (152 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. Rendered and inspected: PDF pp. 12–22 (the revised aggregation entry, the new entries and section) and p. 128 (the pruned legacy section). The artefact compiles on its own: 18 pages (15 before), no warnings, the same 3 underfull boxes.

### For review

- The seven new entries and four revised ones. In particular:
  - the restated error comparison and the counterexample in `res:informed-trading-aggregation`;
  - the fixed-point form of the winner's-curse bid;
  - the merge of the specialist strategies into order anticipation rather than an assignment to `market-structure-execution-quality`.
- `03_.../07_liquidity_and_market_impact.tex` repeats the topic review bluffing material (*Round-Trip Manipulation Profit Test*, *Impact Symmetry Disciplines Bluffing*).

## liquidity and impact review: liquidity and market impact, 15 October 2026

Migration of the file named as the selected topic, run from strategic trading review's pushed state (`3780514`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts were confirmed before starting: 757 legacy blocks, 29 assigned, 593 shared, 35 entries; 22 entries listed for `execution-market-making` and 13 for `market-making-lob`. Migration and source checking, not study.

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
| `alpha-harris` | As in dealer-information models / strategic trading reviews | pp. 271–273 reread |

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
| `alpha-harris` | chap. 12, pp. 270–273 | Text layer and the strategic trading review page image of p. 270 |

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

The 6 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Liquidity and market impact (liquidity and impact review)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and `02_...` and `08_...` are byte-identical to before.

### Counts

`check_compendium.py`: 757 → 751 legacy blocks (6 migrated). Assigned 29 → 29; one candidate only 135 → 135; shared 593 → 587. Entries 35 → 38 (definitions 14 → 15, models 6 → 7, results 11 → 12). Entries listed: `price-impact-execution` 0 → 3 (new note), `execution-market-making` 22 → 22, `market-making-lob` 13 → 13. No notation override was added: Webster's $S$, $P$, $I$ and the impact superscripts are defined in the entries.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 159 pages (155 before; the new chapter adds pages); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had one new overfull box in the Status line of `def:price-impact`; it was reworded away. Rendered and inspected: PDF p. 22 (the revised bluffing entry), pp. 39–42 (the new chapter and entries) and p. 132 (the pruned legacy section). The artefact compiles on its own: 19 pages (18 before), no warnings, the same 3 underfull boxes.

### For review

- The three new entries and the revised bluffing entry. In particular:
  - the new canonical chapter and the routing to `price-impact-execution`;
  - the separation of strategic bluffing from mechanical manipulation;
  - the "temporary impact" terminology note.
- Whether `catalogue-0528`, on no route, should be the main empirical source for these entries until the pathway's own readings are studied.

## market-impact models review: market impact models, 15 October 2026

Migration of the file named as the selected topic, run from liquidity and impact review's pushed state (`c7ed121`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged).

**Baseline counts.** The reported counts were confirmed (751 legacy blocks, 29 assigned, 587 shared, 38 entries; 13 listed for `market-making-lob`, 3 for `price-impact-execution`) except one. The status script listed 23 entries for `execution-market-making`, not 22, because liquidity and impact review had named `res:no-price-manipulation` under that note's Entries heading. The sentence was reworded, and the count is 22 again.

Migration and source checking, not study.

### Scope

The 10 blocks of `04_.../05_market_impact_models.tex`, whose only candidate pathway is `price-impact-execution`. All 10 were migrated. The file, its `\input` line in `04_.../00_overview.tex` and its map row were deleted. `04_.../04_price_impact_estimation.tex` was not touched.

### Routing

liquidity and impact review's routing is carried forward: the entries live in the canonical chapter `compendium/execution-trading-costs/` under `price-impact-execution`. No block concerns market making or bluffing, so `def:bluffing-manipulation` and `res:no-price-manipulation` were compared but not changed.

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
| `catalogue-0528` | As in liquidity and impact review | As before |
| `wide-webster-price-impact` | As in liquidity and impact review | As before |

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
- **Kept distinct.** Permanent impact (a limit) against impact at a finite post-execution horizon (Bacry et al.'s 20 days). Observed against reaction and prediction impact. The simple common kernel against the extensions (volume weight, event types). No no-manipulation claim was made or changed in the topic review.

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

The 10 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Market impact models (market-impact models review)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and the other files of `04_...` are byte-identical (only the `\input` line was removed from `00_overview.tex`).

### Counts

`check_compendium.py`: 751 → 741 legacy blocks (10 migrated). Assigned 29 → 29; one candidate only 135 → 125 (these blocks counted to `price-impact-execution` alone); shared 587 → 587. Entries 38 → 40 (evidence 0 → 1, methods 3 → 4). Entries listed: `price-impact-execution` 3 → 5; `execution-market-making` 23 → 22 (the liquidity and impact review listing artefact removed); `market-making-lob` 13 → 13. No notation override was added; $\mathcal I_d$ (index), $P_d$ (close) and the Almgren–Chriss coefficients are defined in their entries.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 160 pages (159 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had one new underfull box in the Status line of `mod:propagator`; it was reworded away. Rendered and inspected: PDF pp. 40–45 (the revised and new entries) and pp. 136–137 (the pruned legacy section, which now passes from *Price Impact Estimation* to *Trade Duration*). The artefact compiles on its own: 20 pages (19 before), no warnings, the same 3 underfull boxes.

### For review

- The two new entries and the revised `def:price-impact` and `mod:propagator`.
- Reliance on preprint versions of the three required readings.
- The three meanings of "temporary impact".
- The interpretation notes on Bacry et al.'s in-sample beta.

## impact estimation review: price impact estimation, 15 October 2026

Migration of the file named as the selected topic, run from market-impact models review's pushed state (`2214a1b`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 741 legacy blocks (125 single-candidate, 587 shared, 29 assigned), 40 entries, and pathway listings of 5, 22 and 13. Migration and source checking, not study.

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
| `alpha-laruelle` | As in volatility and liquidity / information and price discovery reviews | As before |
| `alpha-harris` | As in dealer-information models / strategic trading reviews | As before |
| `s6-hasbrouck` | The 2007 book PDF, `Empirical Market Microstructure_ ... (2007, Oxford University Press, USA) - libgen.li.pdf`. Another local file named "Joel Hasbrouck - Empirical market microstructure ... (2007).pdf" renders as his 2004 lecture-notes draft and was not used | Page image of p. 91 matches the 2007 book |
| `wide-almgren-direct-impact` | Authors' preprint of 10 May 2005, 26 pp., from a Wayback snapshot (2017-08-08) of `cims.nyu.edu/~almgren/papers/costestim.pdf` | Title, authors and date; the published Risk version was not compared |
| `wide-bacry-life-cycle` | arXiv preprint of 9 December 2014, as in market-impact models review | As before; Lehalle and Laruelle (2018) restate its procedure, citing the 2015 paper |

Not consulted: Glosten and Harris (1988), Madhavan (2002), Moro et al. (2009), Huberman and Stanzl (2004), Tóth et al. (2011). Claims from them are attributed to the source that reports them. market-impact models review's checks of Almgren and Chriss covered only selected passages of a preprint and were not reused as a check of Almgren et al. (2005).

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

The 8 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Price impact estimation (impact estimation review)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and the other files of `04_...` are byte-identical (only the `\input` line was removed from `00_overview.tex`).

### Counts

`check_compendium.py`: 741 → 733 legacy blocks (8 migrated). Single-candidate 125 → 117; shared 587 → 587; assigned 29 → 29. Entries 40 → 44 (evidence 1 → 3, methods 4 → 6). Entries listed: `price-impact-execution` 5 → 9; `execution-market-making` 22 → 22 (one of its entries gained a cross-reference, recorded in its note without a new listing); `market-making-lob` 13 → 13. No notation override was added: the house trade sign $q_t$ is kept, and Almgren et al.'s $I$, $J$ and coefficients are declared local in their entry.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 163 pages (160 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning; no new boxes. Rendered and inspected: PDF p. 40 (the revised `def:price-impact`), pp. 44–48 (the revised and new entries) and pp. 140–141 (the pruned legacy section, which no longer contains *Price Impact Estimation* or *Market Impact Models*). The artefact compiles on its own: 21 pages (20 before), no warnings, the same 3 underfull boxes.

### For review

- The four new entries and the three revised ones.
- The decision to give Almgren et al.'s design its own method entry.
- The $\lambda_0$ correction to the Glosten–Harris form.
- The duration reconciliation.
- The reliance on preprints (Almgren et al. 2005, Bacry et al. 2014) and on Harris's report of Madhavan.

## optimal execution review: optimal execution problem, 15 October 2026

Migration of the file named as the selected topic, run from impact estimation review's pushed state (`3d597b1`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 733 legacy blocks (117 single-candidate, 587 shared, 29 assigned), 44 entries, and listings of 9, 22 and 13. `price-impact-execution`'s 36 were candidate associations of shared blocks, not owned blocks, and are reported that way below. Migration and source checking, not study.

### Scope

The 9 blocks of `execution-trading-costs/01_.../01_optimal_execution_problem.tex`, shared in the map between `price-impact-execution` and the section overview `execution-trading-costs`. All 9 were migrated. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership

The overview's outcome asks for a schedule and an expected cost with its uncertainty "from a stated impact model". Its readings include `alpha-almgren` ("Set a benchmark for the trade-off between impact risk and execution speed"). The guide therefore first needs the scheduling model at the overview; `price-impact-execution` builds on it to estimate impact models and derive schedules. Block trading is part of planning an order's execution (venue, mechanism, schedule) and has no specialist pathway in the pinned taxonomy. Both new entries are therefore owned by the overview. A note was opened for it, `notes/pathways/execution-trading-costs.md`, on the same basis as the `execution-market-making` note in information and price discovery review. The impact concepts the entries use stay with `price-impact-execution` and are cross-referenced. Owned listings and cross-references are kept apart: a first draft of the note named two `price-impact-execution` entries under its Entries heading, which the checker counted as owned, and it was reworded.

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
- **Almgren and Chriss** were checked in the authors' preprint of December 2000, the copy obtained in market-impact models review. The passages used in market-impact models review (pp. 8–11) were reused; additional passages were read for the topic review (sec. 1.1, p. 7; eqs. (4)–(5), p. 10; secs. 2–2.3, pp. 11–15, with a page image of p. 14). The 2001 journal version was not compared.
- **Harris** chap. 15, pp. 322–327, for the block blocks.
- The Cartea–Jaimungal framework in A.7.3 was read but not used, since no block draws on it.

### Mathematical checks (own, Interpretation in the entry)

**Units and conventions.** The concession $\kappa\sigma_n(v_n/V_n)^\gamma$ is currency per share, with $\sigma_n$ in currency per slice (p. 275). The execution-slice cost is $v_n$ times it, and the order's expected impact cost is $\kappa\sum\sigma_nv_n^{\gamma+1}/V_n^\gamma$, a total, not a rate. It is a temporary cost on that execution slice's own fills, not a transient displacement. There is no permanent-impact term and no spread or fee term, unlike Almgren–Chriss's $g$ and $\epsilon$.

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

The 9 blocks are kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Optimal execution problem (optimal execution review)*. A script confirmed three things: each block appears there once and in order; the artefact's earlier content is unchanged; and the other files of `execution-trading-costs/01_...` are byte-identical (only the `\input` line was removed from `00_overview.tex`).

### Counts

`check_compendium.py`: 733 → 724 legacy blocks (9 migrated). Shared 587 → 578; single-candidate 117 → 117; assigned 29 → 29. Each of the 9 blocks was a candidate of both pathways, so the per-pathway candidate counts fell by 9 each: `execution-trading-costs` 57 → 48, `price-impact-execution` 36 → 27. This is one block counted under two candidates, not 18 blocks. Entries 44 → 46 (definitions 15 → 16, models 7 → 8). Entries listed: `execution-trading-costs` 0 → 2 (new note); `price-impact-execution` 9 → 9; `execution-market-making` 22 → 22; `market-making-lob` 13 → 13. No notation override was added: the entry declares its $\kappa$, $\gamma$ and $\lambda$ locally, against the Almgren–Chriss symbols.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 164 pages (163 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning; no new boxes. Rendered and inspected: PDF pp. 39–41 (the chapter opener and the new section) and p. 151 (the pruned legacy chapter, which now starts at *Execution Benchmarks*). The artefact compiles on its own: 21 pages (as before, the new section fitting the last page), no warnings, the same 3 underfull boxes.

### For review

- The two new entries.
- Ownership by the overview rather than `price-impact-execution`.
- The timing-convention resolution and the corrected comparative static and convexity claims.
- Reliance on the Almgren–Chriss preprint.

## execution benchmarks review: execution benchmarks, 15 October 2026

Migration of the file named as the selected topic, run from optimal execution review's pushed state (`bbaafa5`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 724 legacy blocks (117 single-candidate, 578 shared, 29 assigned), 46 entries, listings of 2, 9, 22 and 13, and candidate associations of 48 (`execution-trading-costs`) and 27 (`price-impact-execution`). Migration and source checking, not study.

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

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Execution benchmarks (execution benchmarks review)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears there once, and that the three blocks and the table (with its `\stepcounter`, column settings and caption) each appear once and in order. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`. The table's disposition is recorded separately above, since the checker counts only the three blocks.

### Counts

`check_compendium.py`: 724 → 721 legacy blocks (3 migrated). Shared 578 → 575; single-candidate 117 → 117; assigned 29 → 29. Each block was a candidate of `execution-trading-costs` and `market-structure-execution-quality`, so each pathway's candidate associations fell by 3: 48 → 45 and 321 → 318 (3 blocks, not 6). `price-impact-execution` stays at 27. Entries 46 → 49 (definitions 16 → 18, methods 6 → 7). Entries listed: `execution-trading-costs` 2 → 5; `price-impact-execution` 9; `execution-market-making` 22; `market-making-lob` 13.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 167 pages (164 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. A first build had three overfull boxes in the new section (a long key at a line end, the table's paragraph indent, a long path), fixed before commit. Rendered and inspected: PDF pp. 39–43 (the chapter opener, the new section and its table) and p. 154 (the pruned legacy chapter, which now starts at *Execution Algorithms*). The artefact compiles on its own: 22 pages (21 before), no warnings, the same 3 underfull boxes; its new last page shows the original table.

### For review

- The three new entries, and ownership by the overview rather than `market-structure-execution-quality`.
- Reliance on Kissell and Harris for implementation shortfall while Perold is unread.
- The corrections to Kissell's eq. (3.10) and p. 100, and the double-counting and model-against-measurement notes.

## execution algorithms review: execution algorithms, 15 October 2026

Migration of the file named as the selected topic, run from execution benchmarks review's pushed state (`5d113ac`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 721 legacy blocks (117 single-candidate, 575 shared, 29 assigned), 49 entries, listings of 5, 9, 22 and 13, and candidate associations of 45 (`execution-trading-costs`), 27 (`price-impact-execution`) and 318 (`market-structure-execution-quality`). Migration and source checking, not study.

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

- **Lehalle and Laruelle**, 2018 World Scientific printing (text layer; printed page = PDF page − 27): sec. 3.1.1, pp. 196–197 (historical data, dark-pool probes, models with daily parameters and real-time variables); sec. 3.1.2, pp. 197–198 (components); sec. 3.1.3, pp. 198–201 (pre-trade, monitoring, performance and what-if); sec. 3.4.1, pp. 230–233 (Table 3.2, customisation, trading envelopes). Page images of pp. 198, 201, 230 (Table 3.2), 231 and 233. execution benchmarks review's inspection of Table 3.1 was not relied on for this material.
- **Harris**, 2002 Oxford printing: chap. 18, pp. 380–389 (order submission, reactive and proactive traders, defensive strategies); chap. 23, pp. 486–491 (index funds, program trades, the firm bid/offer market); chap. 28, sec. 28.2.2, pp. 560–561 with both boxes (portfolio insurance).
- **Kissell**, `s7-kissellscience`, the copy whose copyright page says 2014 (the catalogue's date is 2013; the guide is unchanged): chap. 1, pp. 16–19 (algorithm types, basket algorithms, risk-aversion parameter), and chap. 3, p. 108 (participation-weighted price).
- **Perold (1988)** remains unread; nothing in the topic review cites it.

### Algorithm checks (own, Interpretation in the entries)

- **Benchmark against policy.** VWAP and TWAP keep their two meanings (price statistic and policy) in `def:execution-benchmark`; `def:trading-envelope` describes the policies. Kissell's VWAP and TWAP policies are static day schedules; POV reacts to realised volume and need not complete, with a broker minimum rate as the completion fix; arrival-price and IS algorithms are cost–risk optimisations, IS adding adaptation; definitions and risk-aversion scales vary by broker.
- **Parent schedule against child placement.** The envelope bounds the parent order's cumulative quantity; child size, price and venue belong to the tactics (pp. 197–198).
- **Information.** Parameters are estimated about daily; $V$ in $\kappa\sigma(v/V)^\gamma$ is realised market volume, so a schedule fixed at the start can use only a forecast of it.
- **Participation denominator.** Neither source states whether a rate $\rho$ counts the order's own fills. With them, the order is $\rho/(1-\rho)$ of others' volume (25 percent at 20 percent); without, $\rho/(1+\rho)$ of the total (16.7 percent). Kissell's participation-weighted price counts own fills in its window. Checked numerically; logged as an open question.
- **Feedback.** The legacy proposition shows only the sign. If induced moves persist and retrigger the rule, the total move is $dS/(1-\lambda q')$ for dimensionless $\lambda q'<1$ (1.67 at 0.4, checked by iteration); purely temporary impact gives no amplification.
- **Portfolio-insurance sizing.** Harris's box multiplies the fall by delta; the rebalancing trade depends on the change in the hedge ratio. A Black–Scholes illustration (zero rate, 20 percent volatility, one year) gives sales of about 1.0, 1.6 and 1.8 percent of insured value per 1 percent fall for floors at 80, 90 and 100 percent.
- The spread-against-impact accounting gap from execution benchmarks review stays open; no cost already in execution prices was added.

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

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Execution algorithms (execution algorithms review)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears once, and that the 17 blocks and the table (with its settings and caption) each appear once and in order. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`. The table's disposition is recorded separately above.

### Counts

`check_compendium.py`: 721 → 704 legacy blocks (17 migrated). Shared 575 → 558; single-candidate 117; assigned 29. Each block was a candidate of `execution-trading-costs` and `price-impact-execution`, so each fell by 17: 45 → 28 and 27 → 10 (17 blocks, not 34). `market-structure-execution-quality` stays at 318. Entries 49 → 54 (definitions 18 → 21, methods 7 → 8, mechanisms 1 → 2). Entries listed: `execution-trading-costs` 5 → 10; `price-impact-execution` 9; `execution-market-making` 22; `market-making-lob` 13. A first draft of the overview note named `mech:bubble-crash-dynamics` under its Entries heading, which the checker counted as owned (11); reworded.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 170 pages (167 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` duplicate-destination warning. Rendered and inspected: PDF pp. 43 (the rebuilt Table 3.2), 45–49 (the new section) and 159 (the pruned legacy chapter, which now starts at *Transaction Cost Analysis (TCA)*). The artefact compiles on its own: 24 pages (22 before), no warnings, the same 3 underfull boxes; its last page shows the original table.

### For review

- The five new entries, the Table 3.2 extension, and ownership by the overview rather than `price-impact-execution`.
- The participation-denominator question and the portfolio-insurance sizing correction.
- The source slips in Lehalle and Laruelle (A.6 reference, Figure 3.14 caption).

## transaction-cost analysis review: transaction cost analysis, 15 October 2026

Migration of the file named as the selected topic, run from execution algorithms review's pushed state (`3d93967`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 704 legacy blocks (117 single-candidate, 558 shared, 29 assigned), 54 entries, listings of 10, 9, 22 and 13, and candidate associations of 28 (`execution-trading-costs`), 10 (`price-impact-execution`) and 318 (`market-structure-execution-quality`). Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../04_transaction_cost_analysis.tex`: 25 counted blocks, including the closing sentences inside them. The file had no table, figure or text outside the blocks (checked by script). The map listed `market-structure-execution-quality` and `execution-trading-costs`. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership

Each block was read and routed on its content, not the filename or earlier topic reviews:

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

- **Harris**, 2002 Oxford printing (text layer; printed page = PDF − 13): chap. 7, pp. 151–167 (principal–agent problem, best execution, dual trading, preferencing, soft dollars, dishonest brokers); chap. 15, pp. 328–331 (block dealers, trade reporting, motive audit, Table 15-2); chap. 21, pp. 420–423, 432 and 435–441 (components, signed cost, marginal rule, prediction), reusing execution benchmarks review's pp. 424–437; chap. 22, pp. 442–450 and 469–470 (performance evaluation, smoothing); chap. 25, pp. 514–519 (best execution practice, Rules 11Ac1-5 and 11Ac1-6). The marginal-aggressiveness passage (pp. 437–438) was read in the topic review, not taken from the earlier lead.
- **Kissell**, `s7-kissellscience`, the inspected copy whose copyright page says 2014 (the catalogue's 2013 date is unchanged): chap. 3, pp. 87–96 (best execution, ten components, TCA phases, cost against performance) and pp. 110–113 (index-adjusted cost and z-scores; page image of p. 112).
- **Lehalle and Laruelle**, 2018 printing: sec. 3.1.3, pp. 200–203 (performance indicators, pre-, live- and post-trade compatibility, TCA); app. A, sec. A.7.2, pp. 278–279, with the page image of p. 279 for (A.26), the passage the average-price decomposition cites.
- **Perold** remains unread; the topic review relies on it only through Kissell's and Harris's attributions, as before.

### Accounting checks (own, Interpretation in the entries)

- **Legacy shortfall formula.** $\mathrm{IS}=dq(\bar p-p_0)+d(Q-q)(p_T-p_0)+$ explicit costs equals Perold's form with $S=dQ$; execution benchmarks review's example gives 3,960 for the buy and the sell.
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

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Transaction cost analysis (transaction-cost analysis review)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears once, that all 25 blocks appear once and in order, and that no text lies outside them. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`.

### Counts

`check_compendium.py`: 704 → 679 legacy blocks (25 migrated). Shared 558 → 533; single-candidate 117; assigned 29. Each block was a candidate of `execution-trading-costs` and `market-structure-execution-quality`, so each fell by 25: 28 → 3 and 318 → 293 (25 blocks, not 50); `price-impact-execution` stays at 10. Entries 54 → 60 (definitions 21 → 24, methods 8 → 11). Entries listed: `execution-trading-costs` 10 → 13; `market-structure-execution-quality` 0 → 2 (new note); `performance-manager-evaluation` 0 → 1 (new note); `price-impact-execution` 9; `execution-market-making` 22; `market-making-lob` 13.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 174 pages (170 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` warning. A first build had one overfull box (a See-also line with an unbreakable key) and one underfull line in the chapter opener, both from the topic review and fixed. Rendered and inspected: PDF p. 7 (the new Chapter 1), pp. 47 and 52–55 (the block-trade extension, the new sections) and p. 166 (the pruned legacy chapter, which now starts at *Smart Order Routing*). The artefact compiles on its own: 27 pages (24 before), no warnings, the same 3 underfull boxes.

### For review

- Routing four blocks to `performance-manager-evaluation`, outside the map candidates, and opening its chapter.
- The three best-execution and broker blocks given to `market-structure-execution-quality`.
- The accounting split and its limits, the (A.26) correction, the Kissell side correction.

## smart order routing review: smart order routing, 15 October 2026

Migration of the file named as the selected topic, run from transaction-cost analysis review's pushed state (`b699ed2`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 679 legacy blocks (117 single-candidate, 533 shared, 29 assigned), 60 entries, listings of 13, 2, 1, 9, 22 and 13, and candidate associations of 3, 293 and 10. The file's map row names one pathway, so its 15 blocks were among the 117 single-candidate (`market-structure-execution-quality` exclusive: 21), not the shared count. Migration and source checking, not study.

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
- Harris's preferencing passages (chap. 7, pp. 161–162) were reused from transaction-cost analysis review. `ex-sec-rule605-2024`, `ex-sec-withdrawal-2025`, `ex-sec-tick-access-2024` and Perold remain unread.

### Regulatory claims: historical against verified

- **Verified as of 15 October 2026:** Rule 611 obliges a *trading center* to keep and enforce written policies reasonably designed to prevent trade-throughs of protected quotations in NMS stocks, and to surveil them, with nine exceptions (system failures, non-regular-way trades, single-priced opening, reopening and closing transactions, crossed protected quotations, intermarket sweep orders, orders not priced off the quote, quotes inferior within the prior second, stopped customer orders). It is quote protection by venues, not a broker's best-execution duty or a reporting obligation, and it does not require venues to reroute; an intermarket sweep order lets the router take protected quotes itself.
- **Historical (2018, not verified as current):** Lehalle and Laruelle's statements that U.S. clearing and settlement fees must be equal across venues, and that European executing brokers choose their consolidation and must disclose a best-execution policy.
- **Historical (2002):** Harris's Rules 11Ac1-5 and 11Ac1-6, unchanged from transaction-cost analysis review.

### Routing and fee-accounting checks (own, Interpretation in the entries)

- **Three-broker example.** Sweeping Table 3.3's cheapest levels: B1 (Euronext and Chi-X, split) 101.15 and B3 (all three, split) 100.75, as printed. The best single venue for 500 shares is Chi-X at 102.05 (Euronext 102.10, Turquoise 102.20), against the printed 102.50: a likely misprint. B1's bracketed quantities add to 600 and list depth, not fills.
- **Fee threshold.** Exactly $\delta<\phi/(1+f-\phi)$ for a buy (acquisition cost) and $\delta<\phi/(1-f+\phi)$ for a sell (proceeds), both about $\phi$; illustrative $P=100$, $f=3$ bp, $\phi=1$ bp give thresholds 0.99980 and 1.00020 bp, and $\delta=0.99$ and 1.01 bp flip the choice on both sides. With per-share fees the condition is $P\delta<c-c'$. Fees are proportional and paid by the taker; rebates are negative fees; both quotes are assumed contemporaneous, executable for the whole size and taken; the spread is in the prices and not added again. A favourable fee-adjusted quote does not establish a fill or best execution.
- **Passive split.** The book prints eq. (3.4) as $(D-\sum Q_n)/\sum r_n$; its footnote and Table 3.5 need $D+\sum Q_n$ (62.5 s, against −12.5 s). Table 3.5 recomputed (35/42.5/22.5 percent; 175/212.5/112.5 shares). A venue with $f_n<0$ must be dropped and $\tau^\star$ recomputed: setting it to zero leaves fractions not summing to one (checked on an illustrative case). Equal finishing times minimise the completion time of the whole order, not an average. The model treats queues and rates as fixed.
- **Latency.** Displayed depth is not assumed to remain while a sequence of child orders is routed; the book's mirrored-liquidity example is kept as a scenario, not a measured effect.
- **Routing conflict.** The legacy proposition is a condition under which client- and broker-optimal routing differ; it is not evidence of conflicted routing.
- The accounting split of transaction-cost analysis review and its limit (midpoint drift is not automatically own impact) are unchanged.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | sec. 3.4.2, pp. 233–244 | Text layer; page images of pp. 235, 236, 240, 241; Laruelle et al. (2011, 2013) not consulted |
| 17 CFR 242.611 | full section, eCFR point-in-time 13 Oct. 2026 | Effective and compliance dates of the 2024 amendment not checked |
| MiFID II | none | Not retrieved; European regime dated 2018 |

The three new entries and the two extended ones are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *Smart order routing (smart order routing review)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged, that the file body appears once, that the 15 blocks and the table (with its caption) each appear once and in order, and that no text lies outside them. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed.

### Counts

`check_compendium.py`: 679 → 664 legacy blocks (15 migrated). Single-candidate 117 → 102; shared 533 → 533 (unchanged, as these blocks were never shared); assigned 29. `market-structure-execution-quality`: exclusive 21 → 6, shared candidates 293 (unchanged), listed entries 2 → 5. Entries 60 → 63 (definitions 24 → 25, methods 11 → 12, results 12 → 13). Other listings unchanged: `execution-trading-costs` 13, `performance-manager-evaluation` 1, `price-impact-execution` 9, `execution-market-making` 22, `market-making-lob` 13.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 175 pages (174 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before; the one `page.i` warning. A first build had one overfull line (a long path), fixed. Rendered and inspected: PDF pp. 55 (best execution with Rule 611), 56–58 (the new section and the rebuilt table) and 168 (the pruned legacy chapter, which now starts at *High-Frequency Trading Strategies*). The artefact compiles on its own: 28 pages (27 before), no warnings, the same 3 underfull boxes.

### For review

- The three new entries; the merges into `def:best-execution` and `def:broker-agency-conflicts`.
- The Rule 611 statement and its scope; the European regime left as of 2018.
- The eq. (3.4) and B2 misprints, the fee thresholds and the split's non-negativity correction.

## high-frequency strategies review: high-frequency trading strategies, 15 October 2026

Migration of the file named as the selected topic, run from smart order routing review's pushed state (`4fb411c`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 664 legacy blocks (102 single-candidate, 533 shared, 29 assigned), 63 entries, listings of 13, 5, 1, 9, 22 and 13, and `market-structure-execution-quality` with 6 exclusive blocks and 293 shared candidate associations. Migration and source checking, not study.

### Scope

The whole of `execution-trading-costs/01_.../06_high_frequency_trading_strategies.tex`: 3 counted blocks, including the closing sentence inside the taxonomy. The file had no table, figure, caption or text outside the blocks other than its `% migrate-to:` line and subsection heading (checked by script). The map listed `execution-trading-costs` and `market-structure-execution-quality`. The file, its `\input` line in `01_.../00_overview.tex` and its map row were deleted.

### Ownership and the routing exception

All three blocks belong to `hft-market-design`, which is not among the file's map candidates. The blocks classify HFT strategies, claim that speed edges decay as speed diffuses, and say how HFT should be judged by other traders' costs. That pathway's outcome is to "evaluate how speed, latency races and fast arbitrage affect liquidity, price discovery and the costs borne by slower traders", and two of its required readings are the theory and evidence the blocks need (`wide-budish-cramton-shim`, `wide-menkveld-hft-review`). The overview's outcome (planning and costing an order) and `market-structure-execution-quality`'s (rules, fees and execution quality) touch the material only through routing and fees, which already have entries there and are cross-referenced. The pathway sits in the section `execution-market-making`, so the entries are in `compendium/execution-market-making/high-frequency-trading.tex`, and a pathway note was opened. The routing outside the map is a judgement **for review**, as with transaction-cost analysis review's routing to `performance-manager-evaluation`. The fifteen blocks already assigned to `hft-market-design` were not touched.

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

The whole file below its `% migrate-to:` line is kept verbatim in `notes/artefacts/market-making-lob/derivations.tex`, section *High-frequency trading strategies (high-frequency strategies review)*, with only the subsection unnumbered. A script confirmed that the artefact's earlier content is unchanged (its first 128,718 characters, everything before `\end{document}`, are identical), that the file body appears once, that the three blocks appear once each and in order, and that nothing but the `% migrate-to:` line and the subsection heading lay outside them. The other files of `execution-trading-costs/01_...` are byte-identical; only the `\input` line was removed from `00_overview.tex`.

### Counts

`check_compendium.py`: 664 → 661 legacy blocks (3 migrated). Shared 533 → 530; single-candidate 102; assigned 29. Each block was a candidate of `execution-trading-costs` and `market-structure-execution-quality`, so each fell by 3: 3 → 0 and 293 → 290 (3 blocks, not 6); `market-structure-execution-quality` keeps 6 exclusive and 3 assigned. Entries 63 → 66 (definitions 25 → 26, results 13 → 15). Entries listed: `hft-market-design` 0 → 3 (new note, whose cross-references are under *Related entries owned elsewhere*, not the Entries heading); unchanged: `execution-trading-costs` 13, `market-structure-execution-quality` 5, `performance-manager-evaluation` 1, `price-impact-execution` 9, `execution-market-making` 22, `market-making-lob` 13. `hft-market-design` keeps 15 assigned and 7 shared blocks.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 178 pages (175 before); no LaTeX warnings, no undefined references or citations; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 40–44 (the new section 2.10) and 172 (the pruned legacy chapter, which now starts at *Reinforcement Learning and ML in Execution*). The artefact compiles on its own: 28 pages (unchanged count), no warnings, the same 3 underfull boxes. Tests: 14 passed.

### For review

- Routing all three blocks to `hft-market-design`, outside the map candidates, and opening its note and topic file.
- The three new entries; the reading of the SEC's types as an organising device, not a classification.
- The correction to the "edge decays" principle and the 0.37 bp correction to Lehalle and Laruelle.

## execution control review: reinforcement learning and ML in execution, 15 October 2026

Migration of the file named as the selected topic, run from high-frequency strategies review's pushed state (`60753ff`, on `main`, matching `origin/main`; guide submodule at `343d145`; `house.tex` unchanged). The reported counts matched the checker: 661 legacy blocks (530 shared, 102 single-candidate, 29 assigned), 66 entries, 0 problems. Migration and source checking, not study.

### high-frequency strategies review correction

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

`check_compendium.py`: 661 → 657 legacy blocks (4 migrated) = 530 shared + 98 single-candidate (102 − 4) + 29 assigned. `reinforcement-learning-trading`: exclusive 4 → 0, listed entries 0 → 1, backlog stubs 0 → 1. Entries 66 → 67 (models 8 → 9). Other listings unchanged: `execution-trading-costs` 13, `market-structure-execution-quality` 5, `performance-manager-evaluation` 1, `price-impact-execution` 9, `execution-market-making` 22, `market-making-lob` 13, `hft-market-design` 3.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 181 pages (178 before); no LaTeX warnings, no undefined references; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had one overfull line in the entry's See-also (an unbreakable key), reworded. Rendered and inspected: PDF pp. 7–9 (the new Chapter 1), 10 (Chapter 2, renumbered), 45 (the corrected Budish–Cramton–Shim paragraph) and 175 (the pruned legacy chapter, which now starts at *Production Considerations*). The new artefact compiles with no warnings or bad boxes. Tests: 14 passed.

### For review

- Ownership by `reinforcement-learning-trading` and the new chapter `ml-alternative-data/`.
- The appendix corrections and the qualified parameter intuition; whether to check the model against Cartea and Jaimungal's originals.
- The backlog stub for hybrid execution.

## execution control review follow-up: mathematical corrections to `mod:cartea-jaimungal-execution`, 15 October 2026

A bounded correction to execution control review (`6d04e52`), run from that pushed state (657 legacy blocks = 530 shared + 98 single-candidate + 29 assigned, 67 entries, checker clean, guide `343d145`). The execution control review record above is left as written; where it differs, this section supersedes it. No block, owner, label or backlog stub changed; no source was re-read; the legacy blocks in the artefact are untouched.

### Corrections

1. **One terminal payoff.** execution control review kept the printed objective $Q_T(S_T-AQ_T)$ in the Statement while its terminal condition and ansatz used $Q_T(S_T-\psi/2-AQ_T)$. The Statement now defines $H_t(\nu)$ with the corrected payoff, marked as Interpretation; the value, terminal condition, decomposition $h:=H^*-x-q(S-\psi/2)$, reduced equation and policy $\nu^*$ all use it. The printed objective is quoted under Pitfalls with its own decomposition $g:=H-x-qS$, giving $\nu^{\mathrm{pr}}=-(bq+\partial_qg+\psi/2)/(2\kappa)=\nu^*-(\psi/(4\kappa))e^{-\int_t^T\xi/\kappa}$. execution control review's sentence "$\nu^*=-(bq+\partial_qh+\psi/2)/(2\kappa)$" reused $h$ across the two decompositions and is replaced.
2. **Finite value.** The unconstrained model can have infinite value: with $T=Q_0=1$, $\mu=\sigma=\psi=0$, $b=0.1$, $\kappa=A=0.01$, $\phi=0.001$ and $\nu=-M$, the reward's $M^2$ coefficient is $b/2-\kappa-A-\phi/3=0.0297>0$. From the pathwise identity (reward $=Q_0S_0-\psi Q_0/2-bQ_0^2/2+b\int Q\mu+\sigma\int Q\,dW-\kappa\int\nu^2-\phi\int Q^2-(A-b/2)Q_T^2$), the entry now states the sufficient regime $\kappa>0$, $\phi>0$, $A>b/2$, progressively measurable policies with $\mathbb E\int\nu^2<\infty$ and a flow with $\mathbb E\int\mu^2<\infty$; under it $|\zeta|<1$ and $\xi$ is finite and positive. It is sufficient, not necessary, and no verification theorem is claimed. The formal unconstrained benchmark is kept apart from one-directional execution ($\nu\ge0$, $Q\ge0$); clipping $\nu^*$ is not the constrained solution; a finite $A$ is a penalty, not compulsory completion.
3. **Variance.** For a deterministic schedule the random reward is $b\int Q\mu\,dt+\sigma\int Q\,dW$, so $\sigma^2\int Q^2$ is only the Brownian contribution; the variance adds $b^2\operatorname{Var}\int Q\mu$ and $2b\sigma\operatorname{Cov}$. It equals the whole variance when $b=0$ or the flow path is deterministic. Example $Q_t=1-t$, $\mu_t=B_t$, $T=1$, $\sigma=0$: $b^2/20$. execution control review's "for a deterministic schedule the price-risk part of the shortfall has variance $\sigma^2\int Q^2$, so $\phi=\lambda\sigma^2$ reproduces a mean--variance penalty" is qualified accordingly.
4. **Units.** $b$ is in currency per share$^2$ (execution control review said currency per share). The rest were rechecked: $\kappa$ currency·time/share$^2$, $\phi$ currency/(share$^2$·time), $A$, $h_2$, $\xi$ and $\sqrt{\kappa\phi}$ currency/share$^2$ (so $A-b/2\pm\sqrt{\kappa\phi}$ is homogeneous), $h_1$ currency/share, $\gamma$ per unit time, $\sigma$ currency/share/$\sqrt{\text{time}}$.

### Independent checks (`notes/artefacts/reinforcement-learning-trading/cartea_jaimungal_checks.py`, `check_wealth_identity_and_feedback`)

- **Wealth identity.** Euler simulation of the dynamics against the identity for a random policy and flow ($\sigma=0$): 9.908237 against 9.908208 (discretisation error).
- **Terminal-payoff consistency.** A direct discretised optimisation over the inventory path ($\mu=\sigma=0$, a tridiagonal concave problem) against the feedback policies: inventory at $T/2$ and $T$ 0.5903 and 0.1954 for the corrected payoff, 0.6148 and 0.2451 for the printed payoff ($\kappa=0.01$, $\phi=0.001$, $A=0.05$, $b=0.02$, $\psi=0.01$), agreeing to four decimals in each case.
- **Finite-value restriction.** Simulated reward$/M^2$ for $\nu=-M$: 0.1375, 0.0315, 0.0298 at $M=10,100,1000$, converging to 0.02967; with $A=0.06>b/2$ it is $-0.02033$, matching $b/2-\kappa-A-\phi/3$.
- **Variance counterexample.** $\operatorname{Var}\int_0^1(1-t)B_t\,dt$: quadrature 0.05000, Monte Carlo (20,000 paths) 0.0506, exact $1/20$.
- The execution control review checks in the same script still reproduce their earlier output.

### Validation

`check_compendium.py --check`: 0 problems; 657 legacy blocks (530 + 98 + 29) and 67 entries, unchanged. Tests: 14 passed. `latexmk -g -pdf compendium.tex`: exit 0; 182 pages (181 before; the entry grew by a page); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had one overfull line (the wealth identity in one display), split into two lines. Rendered and inspected: PDF pp. 7–10 (the corrected entry). The standalone artefact `derivations.tex` did not change and was not rebuilt.

### Remaining limits

No verification theorem for the quadratic ansatz; the constrained one-directional problem is not solved; Cartea and Jaimungal's originals and `crypto-cartea` are still unconsulted; `wide-hambly-xu-yang` still read only in arXiv v4.

## trading infrastructure review: production considerations, 15 October 2026

Migration of the file named as the selected topic, run from the execution control review follow-up's pushed state (`8aa672a`, on `main`, matching `origin/main`; guide `343d145`; `house.tex` unchanged). The reported counts matched the checker: 657 legacy blocks (530 shared, 98 single-candidate, 29 assigned), 67 entries, 0 problems. Migration and source checking, not study.

### execution control review clarification

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

`check_compendium.py`: 657 → 646 legacy blocks = 530 shared + 87 single-candidate + 29 assigned. `model-governance-controls`: exclusive 16 → 5 (the five in `sysinv/modelrisk.tex`), listed entries 0 → 1, backlog stubs 0 → 2. Entries 67 → 70 (definitions 26 → 28, methods 12 → 13). Listings: `execution-trading-costs` 13 → 14, `execution-market-making` 22 → 23; unchanged `market-structure-execution-quality` 5, `performance-manager-evaluation` 1, `price-impact-execution` 9, `market-making-lob` 13, `hft-market-design` 3, `reinforcement-learning-trading` 1.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 186 pages (182 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had three overfull lines (the new artefact path in Further reading) and one underfull line (a See-also), all from the topic review and fixed. The new chapter `research-engineering-validation` is Chapter 1; later chapters are renumbered by one, labels unchanged. Rendered and inspected: PDF pp. 7–9 (the new chapter), 51 (the floor-against-automated entry), 60–61 (the architecture entry and decision support) and 182 (the legacy execution chapter, which now starts at *Asset-Class-Specific Microstructure*). Tests: 14 passed.

### For review

- Routing blocks 1–7 to the execution overview, 11 to `execution-market-making`, and deleting block 3.
- The order-state synthesis and the reliance on one U.S. rule; the RTS 6 and FIX stubs.

## trading infrastructure review follow-up: clarifications, 15 October 2026

Three clarifications to trading infrastructure review (`1c3fabc`), made at the start of equity market structure review; the trading infrastructure review record above is left as written.

- `def:automated-trading-architecture`: Lehalle and Laruelle's "known in real time" is now quoted as theirs and qualified. The market volume $V$ is available only as observed; volume still to come requires a forecast. It cross-references the decision-time item already in `def:trading-envelope`.
- `cfr-240-15c3-5` in `front/sources.tex`: the SEC adopting release, 34-63241, is dated 3 November 2010 (checked on p. 130 of the release PDF from sec.gov); the Federal Register published it on 15 November 2010, where the eCFR cites the rule text at 75 FR 69825.
- `def:floor-automated-trading-systems`: the six bullets are now presented as the entry's grouping of Harris's seven sections (27.1–27.7), with Table 27-1 listing eleven issues. High absolute start-up costs (p. 549) and the table's relatively lower software costs (p. 552) are recorded as compatible, not as a contradiction; the Harris reading note and the `execution-market-making` pathway note were reworded to match.

## equity market structure review: equity market microstructure, 15 October 2026

Migration of the file named as the selected topic, run from trading infrastructure review's pushed state (`1c3fabc`, on `main`, matching `origin/main`; guide `343d145`; `house.tex` unchanged). The reported counts matched the checker: 646 legacy blocks (530 shared, 87 single-candidate, 29 assigned), 70 entries, 0 problems. Migration and source checking, not study.

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

- **Harris**, 2002 Oxford printing (text through macOS PDFKit, as in trading infrastructure review; printed page = PDF − 13): sec. 15.6.1, pp. 333–334; chap. 23, p. 484, sec. 23.4, p. 489, sec. 23.5 with Table 23-1, pp. 491–492.
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

`check_compendium.py`: 646 → 640 legacy blocks = 530 shared + 81 single-candidate + 29 assigned. `market-structure-execution-quality`: exclusive 6 → 0; assigned 3 and shared 290 unchanged; listed entries 5; backlog stubs 0 → 1. Entries 70 → 71 (mechanisms 2 → 3). Listings: `etf-index-closing-execution` 0 → 1 (new note); `execution-trading-costs` 14 (two entries extended, none added); others unchanged.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 187 pages (186 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 59 (`def:block-trade`), 64 (`def:portfolio-trading`), 81–82 (the new ETF section) and 184 (the legacy asset-class section, which now starts at *Futures Market Microstructure*); pp. 52 and 61 hold the trading infrastructure review follow-up wording. Tests: 14 passed.

### For review

- Routing all six blocks away from the map candidate; deleting blocks 1 and 2.
- The ETF entry's reliance on working-paper versions.

## equity market structure review follow-up: ETF and Harris precision, 15 October 2026

A bounded correction to equity market structure review (`580463e`), run from that pushed state (640 legacy blocks = 530 shared + 81 single-candidate + 29 assigned, 71 entries, checker clean, guide `343d145`). The equity market structure review record above is left as written; where it differs, this section supersedes it.

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

## futures market structure review: futures market microstructure, 15 October 2026

Migration of the file named as the selected topic, run after the follow-up above. Migration and source checking, not study, and not the pathway's checkpoint: no roll cost was measured.

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

`check_compendium.py`: 640 → 633 legacy blocks = 530 shared + 74 single-candidate + 29 assigned. `futures-execution`: exclusive 7 → 0, shared 18 unchanged, listed entries 0 → 4 (new note), backlog stubs 0 → 1. Entries 71 → 75 (conventions 0 → 2, evidence 3 → 4, mechanisms 3 → 4). Other listings unchanged. A first checker run, before the pathway note existed, reported the four new entries as listed in no note; fixed by the note.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 191 pages (187 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. A first build had one overfull See-also line in the new evidence entry, reworded. Rendered and inspected: PDF pp. 41 (`res:spread-determinants`), 82–86 (the ETF follow-up and the new futures section) and 188 (the legacy asset-class section, which now starts at *FX Market Microstructure*). Tests: 14 passed.

### For review

- The four new entries; routing the large-tick block to `execution-market-making`.
- The reliance on CME documentation retrieved on one date, and on a 2000 working-paper draft for the price-discovery evidence.

## futures market structure review follow-up: corrections, 15 October 2026

A bounded correction to futures market structure review (`fb56198`), run from that pushed state (633 legacy blocks = 530 shared + 74 single-candidate + 29 assigned, 75 entries, checker clean, guide `343d145`, clean tree matching `origin/main`). The futures market structure review record above is left as written; where it differs, this section supersedes it. No block, owner, label, artefact or backlog stub changed; the FX file (FX market structure review) was not started.

1. **Large-tick equation.** Lehalle and Laruelle's eq. (2.1), checked on the page image of p. 145, is $\psi_i=a+(b_1\sigma_i+b_2\eta\,\mathrm{tick})/\sqrt{N_i}$: both terms are over $\sqrt{N_i}$. futures market structure review had put only the volatility term over it in `res:spread-determinants`. The entry now matches `meth:spread-volatility-regression`, which already had it right; the reading note `alpha-laruelle` was corrected too. No other occurrence in the compendium or notes. The empirical scope and the futures-specific backlog stub are unchanged.
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

`check_compendium.py --check`: 0 problems; 633 legacy blocks and 75 entries, unchanged. Tests: 14 passed. `latexmk -g -pdf compendium.tex`: exit 0; 193 pages (191 before, from the longer waterfall and settlement text); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: printed pp. 35 (`res:spread-determinants`), 75 (the ETF opening), 78 (settlement) and 79--80 (EFRP and margin), PDF pp. 41, 81, 84 and 85--86.

### Remaining limits

- The current CME settlement page is still unretrieved, so the procedure is as filed in 2020.
- Default-management auction details (subordination and seniorization amounts) are in confidential guidelines.
- Customer-side FCM rules and intraday cycle times are unchecked.

## futures market structure review second follow-up: account classes and the second-month settlement, 15 October 2026

Two wording clarifications, run from `bd4ba54` (633 legacy blocks = 530 shared + 74 single-candidate + 29 assigned, 75 entries, checker clean, guide `343d145`). Earlier records are left as written.

1. `mech:futures-margin-settlement`: "customer losses only from the collateral of the customer account class concerned" stated the restriction in the wrong direction. CME Rules 802.A.5 and 802.G (including 802.G.1 and 802.G.6), read in the chapter-8 text retrieved on 15 October 2026, give the following, and the entry now says so:
   - default management runs separately by account class;
   - a customer-class loss is met first from that class's customer collateral, which in a defaulted customer futures class includes the collateral of customers who did not cause the default (802.G.1);
   - the member's own assets are applied across classes with priority to customers (802.A.5.i, iii);
   - remaining proprietary collateral may cover customer-class losses, pro rata among defaulted customer classes (802.G.6);
   - segregated customer collateral may not be used for proprietary obligations or for another customer class.
2. `conv:cme-globex-trading`: the second month is derived by applying the lead–second spread price to the lead-month settlement. Tier 2 says so explicitly in Exhibit B (PDF p. 6, rendered blackline): the last spread trade, or the nearer of the spread's bid or ask if the trade lies outside them. The entry marks the same reading of Tier 1 as Interpretation. The ES-only VWAP, the rounding and the 2020 dating are unchanged.

## FX market structure review: FX market microstructure, 15 October 2026

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

`check_compendium.py`: 633 → 629 legacy blocks = 530 shared + 70 single-candidate + 29 assigned. `fx-dealer-market-making`: exclusive 4 → 0, listed entries 0 → 3 (new note), backlog stubs 0 → 1. Entries 75 → 78 (definitions 28 → 29, mechanisms 4 → 5, models 9 → 10). Other listings unchanged.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 195 pages (193 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 53–55 (the new FX section), 87 and 89 (the futures market structure review clarifications) and 192 (the legacy asset-class section, which now starts at *Options Market Microstructure*). Tests: 14 passed.

### For review

- The three new FX entries.
- Leaving fixing windows to `fx-funding-settlement` without an entry.
- The reliance on a voluntary code, one provider's disclosure and open manuscript versions.

## FX market structure review follow-up: corrections, 15 October 2026

Targeted corrections to two FX market structure review entries; the FX market structure review record above is left as written.

- `mod:fx-internalisation-horizon`: Butz and Oomen's eq. (8) defines the expected queue length $L$ and the arrival rate $\lambda$ of risk-increasing trades; $L/\lambda$ is the conditional horizon of a risk-increasing trade, and, since risk-reducing trades wait zero, the all-trade average is $W=L/(2\lambda)$ (eq. (9), p. 7). $\lambda_0$ is the baseline intensity of buys and of sells in the skew examples (Examples 1–2, eqs. (5)–(7), pp. 5–6, page images), not $\lambda$. The EUR/USD figure of 1.39 minutes is now labelled the all-trade average the authors report; the conditional horizon, about 2.78 minutes, is labelled as own recomputation (exact stationary sum: $L/\lambda=2.774$, $W=1.387$). Notation and Status updated; `notes/readings/cfd-butz-oomen-2019.md` and the pathway note updated.
- `mech:fx-last-look`: all three of the Code's cover-and-deal conditions are stated (explicit understanding of filling without market risk by first entering offsetting transactions; the volume traded in the window passed on in its entirety; the understanding documented and disclosed, p. 23, page image). The Code's "expected or typical period of time for making the decision" is called the decision time, the duration of the last-look window, and is kept apart from the time spent on checks and from any additional hold. The Deutsche Bank 10-millisecond bound is kept to its scope: the spot price check, with no additional hold; the validity check's duration is not bounded in the sheet, and non-spot products may differ. `notes/readings/exp-fx-code.md` and the pathway note updated.

Checks: as for options market structure review below (same build and test run).

## options market structure review: options market microstructure, 15 October 2026

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

`check_compendium.py`: 629 → 625 legacy blocks = 530 shared + 66 single-candidate + 29 assigned. `options-execution`: exclusive 4 → 0, listed entries 0 → 3 (new note), backlog stubs 0 → 2. Entries 78 → 81 (results 15 → 16, methods 13 → 14, mechanisms 5 → 6). Six reading notes added. Other listings unchanged.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 199 pages (195 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before (one overfull Status line in the new file was fixed by rephrasing); the one `page.i` warning. Rendered and inspected: PDF pp. 54 (the corrected internalisation model), 56–58 (the new options section) and 196 (the legacy asset-class section, which now starts at *Fixed Income Microstructure*). Tests: 14 passed.

### For review

- The three new options entries, and the reliance on five abstracts.
- The two backlog stubs, which need dated OCC and exchange rule documents.
- Not adopting "buy-side typically consume liquidity".

## options market structure review follow-up: corrections, 15 October 2026

Targeted corrections to two options market structure review entries after rechecking Bryzgalova, Pavlova and Sikorskaya pp. 2, 11–12 and 14–17 and the page images of Table I (pp. 15–16); the options market structure review record above is left as written.

- `meth:option-spread-measurement`: "lowest quoted spreads" removed. At-the-money quoted spreads (8.7 percent SLIM, 8.4 percent non-SLIM) are far below those of slightly out-of-the-money trades (28.7, 21.3) but not the lowest bin: slightly in-the-money trades (0.1 to 1) have 8.6 and 5.9. Moneyness, written in Table I as (MidpointPrice − Strike)/Strike for calls, is read as using the underlying's midpoint, distinct from the option-premium midpoint used for spreads; this is labelled interpretation, since the caption does not name the underlying. SLIM is defined as the single-leg non-ISO price-improvement-auction proxy and non-SLIM as the whole remaining pool; "say nothing about spread or multi-leg costs" is replaced by the precise limit that the results do not isolate the execution costs of multi-leg strategies. The Pitfalls on "ATM deepest" now rest on trade share only.
- `res:option-market-maker-spreads` and `mech:options-retail-wholesaler-routing`: exchange-only execution is bounded to the U.S. listed-options market the authors study (their OPRA data). FINRA Regulatory Notice 22-14 (22 June 2022; `finra-rn-22-14`, added to `front/sources.tex`) is cited for its background distinction between listed (standardised) and OTC (conventional) options, OTC trades not generally being centrally cleared or reported to FINRA, the SEC, an exchange or the CAT; the notice's proposal is stated as a request for comment, not an effective rule, and its later status was not checked.
- `mech:options-retail-wholesaler-routing`: the $0.30 net rebate is tied to the responder-execution case of p. 11, footnote 15 (another market maker paying $0.50 to break up a paired order).
- The reading note for `ex-bryzgalova-pavlova-sikorskaya-2023` and the pathway note were updated; the abstract-only limits on the other five readings are unchanged. The options market structure review artefact is unchanged.

## fixed-income market structure review: fixed-income microstructure, 15 October 2026

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

`check_compendium.py`: 625 → 619 legacy blocks = 530 shared + 60 single-candidate + 29 assigned. `otc-fixed-income-trading`: exclusive 6 → 0, listed entries 0 → 3 (new note), backlog stubs 0 → 3. Entries 81 → 84 (definitions 29 → 30, evidence 4 → 5, rules 0 → 1). Four reading notes added; five sources and the options market structure review follow-up's FINRA notice added to `front/sources.tex`. `options-execution` unchanged at 3 entries and 2 stubs.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 203 pages (199 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 57–58 (the corrected options entries), 95, 97–98 (the new fixed-income section) and 200 (the legacy asset-class section, which now starts at *Securities Lending and Synthetic Shorts*). Tests: 14 passed.

### For review

- The three new fixed-income entries, and the reliance on one survey plus three abstracts.
- The rule entry's reading of SR-FINRA-2024-004 and SR-FINRA-2025-008 from their filing summaries.
- The three backlog stubs (credit derivatives and swaps, EU Level 1 text, U.K.).

## fixed-income market structure review follow-up: corrections, 15 October 2026

Targeted corrections to `compendium/execution-trading-costs/fixed-income-trading.tex`; the fixed-income market structure review record above is left as written.

- `def:fixed-income-market-structure`: the 19 percent figure is now an estimate in an industry report published in July 2016, as the survey cites it (p. 2); the observation period behind it is not given, and the publication date is no longer presented as one.
- `ev:bond-transparency-trading-costs`: Edwards, Harris and Piwowar's conclusion keeps the abstract's wording, that the results "suggest that public traders benefit significantly from price transparency".
- `rule:us-eu-bond-transparency`: SR-FINRA-2026-009 rechecked against the SEC approval order (Release No. 34-105991, 24 July 2026, 91 FR 47909–47911; `sec-34-105991`, added to `front/sources.tex`). The presently effective exclusion suppresses from dissemination qualifying same-day, same-price, same-security transactions between a member and its non-member affiliate; the amendment extends it to member affiliates and renames the indicator the Affiliate—Principal Transaction indicator, with an implementation date of at least 12 months after approval (listed as 2 August 2027) and voluntary earlier use. The rulebook's displayed Rule 6750(d)(1), "Affiliate—principal transaction indicator", is named as the future wording.
- `ev:bond-transparency-trading-costs`: "markup disclosure for riskless principal trades" replaced, after rechecking FINRA Rule 2232 (`finra-rule-2232`) and Regulatory Notice 17-08 (`finra-rn-17-08`, both added): since 14 May 2018, Rule 2232(c) requires the mark-up or mark-down on the confirmation when the member trades as principal in a corporate or agency debt security with a non-institutional customer and makes same-trading-day offsetting trades of at least that size, looking through non-arm's-length affiliate trades; (d) exempts functionally separate trading desks and same-day fixed-price-offering sales. FINRA's notice reports a parallel MSRB rule with the same effective date; MSRB's own text was not read, so the municipal statement is attributed to FINRA.
- Layout: the follow-up added about fifteen lines to the evidence entry, so its continuation page (PDF p. 99 before, p. 104 after securities lending and synthetic shorts review) now carries the end of Pitfalls, See also, Further reading, Index and Status (18 text lines) and is no longer near-empty; removing it would require cutting evidence or status text, so it was kept. `house.tex` is unchanged.
- The reading notes for `wide-bsv-fi-survey` and `wide-edwards-harris-piwowar` and the pathway note were updated. Earlier artefacts and the options corrections are unchanged.

## securities lending and synthetic shorts review: securities lending and synthetic shorts, 15 October 2026

Migration of the six-block securities-lending file, run after the follow-up above. Migration and source checking, not study; no checkpoint was attempted.

### Scope

The whole of `execution-trading-costs/02_.../06_securities_lending_and_synthetic_shorts.tex`: 6 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its `\input` in `02_.../00_overview.tex` and its map row were deleted; the wrapper keeps its last topic (crypto).

### Ownership and dispositions

The map names `synthetic-equity-cfd-trs`, whose outcome is pricing CFDs and equity total return swaps from financing, dividend, borrow and margin terms and identifying their counterparty, disclosure and tax exposures. Its prerequisite `money-markets-repo-lending` has the outcome of distinguishing repo from securities lending and pricing collateral financing, with the ICMA FAQ, Duffie–Gârleanu–Pedersen and the ISLA handbook as readings. **Routing exception:** blocks 1–4 and 6 describe the lending market itself (custody, the loan, availability, rebates, the votes of lent shares) and belong to `money-markets-repo-lending`; block 5, a synthetic position replacing borrow, stays with `synthetic-equity-cfd-trs`. Derivative-based empty voting and beneficial-ownership disclosure, which do belong to `synthetic-equity-cfd-trs`, are stubbed there. Both pathways sit in the section `portfolio-risk-financing`, which had no chapter; the topic review opened `compendium/portfolio-risk-financing/` (`section.tex`, `securities-lending.tex`, `synthetic-shorts.tex`). The artefact sits under the map candidate, `notes/artefacts/synthetic-equity-cfd-trs/`, keeping the file whole, as in trading infrastructure / equity market structure reviews.

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

`check_compendium.py`: 619 → 613 legacy blocks = 530 shared + 54 single-candidate + 29 assigned. `synthetic-equity-cfd-trs`: exclusive 6 → 0, listed entries 0 → 1, backlog stubs 0 → 2. `money-markets-repo-lending`: entries 0 → 3, stubs 0 → 2. Entries 84 → 88 (definitions 30 → 32, mechanisms 6 → 7, results 16 → 17). Two pathway notes and four reading notes added, `alpha-harris` updated; five sources added in this follow-up and slice (`finra-rule-2232`, `finra-rn-17-08`, `sec-34-105991`, `cfr-242-203`, `cfr-242-204`).

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 207 pages (203 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF pp. 16–20 (the new chapter, its continuation and closing pages), 97–99 and 104 (the fixed-income market structure review follow-up and the fixed-income continuation page) and 205 (the legacy asset-class section, now only *Crypto Market Microstructure*). Tests: 14 passed.

### For review

- The routing of five blocks to `money-markets-repo-lending` against the map, and the new `portfolio-risk-financing` chapter.
- The synthetic-short entry's reliance on an own derivation in place of Hull.
- The four backlog stubs.

## securities lending and synthetic shorts review follow-up: corrections, 15 October 2026

Targeted corrections to two securities lending and synthetic shorts review entries; the securities lending and synthetic shorts review record above is left as written, including its numerical-check paragraph, which this record supersedes for the short-sale comparison.

- `res:synthetic-short-put-call`, bond replication. Harris's sidebar on p. 157, rechecked by page image (PDF p. 170 of the local copy, rendered through PDFKit), says a long put and a short call ``plus a long position in a bond with the same maturity'' are equivalent to a short position in the underlying. With a long bond paying $K$ the terminal payoff is $2K-S_T$. The entry now states the correct replication: long put, short call and a short zero-coupon bond repaying $K$ pay $-S_T$; for a stock with no dividends the initial values agree ($P-C-Ke^{-rT}=-S_0$), so the package is equivalent to short stock; equivalently, long put and short call equal short stock plus a long bond (a short sale with proceeds invested). With dividends, the package less the bond is a terminal claim $-S_T$ worth $-S_0e^{-qT}$, while short stock is worth $-S_0$ and owes the interim dividends. Harris's wording is quoted as printed and the discrepancy recorded. The European payoff identity and dividend-adjusted parity are unchanged.
- `res:synthetic-short-put-call`, short-sale comparison. The securities lending and synthetic shorts review bullet compared the package with a fixed short of $e^{-qT}$ shares and gave it terminal wealth $S_0e^{-qT}e^{r_bT}-S_T$; with the borrower paying dividends that is not the strategy's terminal wealth. The narrow repair uses $q=0$: one share sold short, the whole proceeds held as cash collateral credited at a constant rebate $r_b$ (lending fee implicit in $r_b$, no other fee, no extra margin, no recall), ends with $S_0e^{r_bT}-S_T$; the package, European options priced at frictionless parity and its premium financed or invested at $r$, ends with $S_0e^{rT}-S_T$. The existing $q=2\%$ Black–Scholes parity example is kept and labelled separately.
- `mech:securities-lending-short-sale`: ``so someone must lend them'' replaced by the standard stock-loan route for delivery at settlement, with two cases where no loan is needed: delivery from securities held in street name for other clients (Harris, p. 155) and Regulation SHO's exception for sales of securities the seller is deemed to own (17 CFR 242.203(b)(2)(ii)).
- **Numerical checks**, added as `notes/artefacts/synthetic-equity-cfd-trs/synthetic_short_checks.py` (standard library; `derivations.tex` unchanged). (1) Payoffs leg by leg at $S_T=60, 95, 100, 140$: put minus call $=K-S_T$; with a short bond $=-S_T$; with a long bond $=2K-S_T$ (130, 95, 90, 50). (2) Parity example $S_0=100$, $K=95$, $r=5\%$, $q=2\%$, $\sigma=25\%$, $T=1$: options repriced by midpoint integration over the risk-neutral density, $C=13.684728$, $P=6.031656$, matching the closed forms to $10^{-4}$, and $P-C=-7.653072=Ke^{-rT}-S_0e^{-qT}=e^{-rT}(K-F)$ with $F=103.0455$. (3) Rebate comparison, $q=0$, same $S_0$, $K$, $r$, $\sigma$, $T$: $C=15.0471$, $P=5.4138$, $P-C=-9.6332$; day-by-day accounts give the package $S_0e^{rT}-S_T$ (5.127110 at $S_T=100$) and the short sale $S_0e^{r_bT}-S_T$ (5.127110, 3.045453, $-0.995017$ for $r_b=5\%, 3\%, -1\%$), gaps $S_0(e^{rT}-e^{r_bT})=0$, 2.081656, 6.122126 at every $S_T$. All checks passed.
- The pathway note for `synthetic-equity-cfd-trs`, the `alpha-harris` reading note and the log were updated. Ownership, stubs and counts are unchanged (613 legacy blocks; 88 entries).

## securities lending and synthetic shorts review second follow-up: lending opening, 15 October 2026

`mech:securities-lending-short-sale` now opens with the standard stock-loan route only: a short seller sells securities it does not own and borrows them to meet delivery at settlement. The examples added in the first follow-up, delivery from other clients' street-name holdings (Harris, p. 155) and Regulation SHO's deemed-to-own locate exception (§ 242.203(b)(2)(ii)), were removed as explanations of why a loan is unnecessary: delivering another customer's street-name securities does not show that no lending occurs, and a locate exemption is a separate regulatory question. The Regulation SHO conditions stay in the entry's Conditions. The synthetic-short mathematics and `synthetic_short_checks.py` are unchanged and still pass. The first follow-up record above is left as written.

## crypto market structure review: crypto market microstructure, 15 October 2026

Migration of the four-block crypto file, the last topic of the legacy execution-trading-costs chapter, run after the clarification above. Migration and source checking, not study; no checkpoint was attempted.

### Scope

The whole of `execution-trading-costs/02_.../07_crypto_market_microstructure.tex`: 4 counted blocks with the sentences inside them; outside them only the `% migrate-to:` line and the subsection heading (checked by script). The file, its map row and both wrappers that input it were deleted: `02_.../00_overview.tex` (a section heading and this one `\input`) and `execution-trading-costs/section.tex` (the legacy chapter heading with label `legacy:execution-trading-costs`, a comment and one `\input`); both are kept verbatim as display text (`verbatim`) in the artefact, so their inputs do not execute. The line `\InputIfFileExists{legacy/execution-trading-costs/section}{}{}` was removed from `compendium/legacy/part.tex`. The 21 unused PNGs in `compendium/legacy/execution-trading-costs/figures/` were left unchanged; `tools/check_compendium.py` now requires a `part.tex` input only for legacy folders that still contain `.tex` files, so the figures-only folder passes (the 14 tests pass unchanged).

References to `legacy:execution-trading-costs` were updated: the comment and the closing sentence of `compendium/execution-trading-costs/section.tex` (all its older notes are now migrated; the impact material remains in the legacy execution-market-making chapter), and the overview paragraph of `compendium/legacy/execution-market-making/section.tex` (algorithmic execution and asset-class microstructure have been migrated). No other `.tex` reference remained; earlier records in this file keep the label as history.

### Ownership and dispositions

The map names `crypto-mm-microstructure`, whose outcome is estimating the fee, impact, latency and adverse-selection terms of quoting one crypto order book from the venue's own data. None of the four blocks is about that. `crypto-perpetuals` has the outcome of reconciling spot, perpetual and dated-futures basis with financing, transfer, margin and liquidation paths across fragmented venues, and its readings include Makarov–Schoar, the perpetual-pricing papers and Deribit's rulebook and funding specification. **Routing exception:** all four blocks go to `crypto-perpetuals`. Items outside its outcome were not given entries: options (`crypto-options-numeraire`), AMM pools (`amm-lending`) and stablecoin, network and bridge risk (`stablecoin-pegs-runs` and the section overview) are stubbed in the `crypto-perpetuals` note with their destination named. `crypto-price-discovery` was considered for block 1 (cross-exchange gaps) but its readings were not used and its outcome centres on information shares and reference rates. The pathway sits in the section `digital-assets-prediction-markets`, which had no chapter; the topic review opened `compendium/digital-assets-prediction-markets/` (`section.tex`, `crypto-venues-perpetuals.tex`). The artefact sits under the map candidate, `notes/artefacts/crypto-mm-microstructure/`, keeping the file whole, as in trading infrastructure / equity market structure / securities lending and synthetic shorts reviews.

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

`check_compendium.py`: 613 → 609 legacy blocks = 530 shared + 50 single-candidate + 29 assigned. `crypto-mm-microstructure`: exclusive 4 → 0, no entries. `crypto-perpetuals`: entries 0 → 3, backlog stubs 0 → 5 (new note). Entries 88 → 91 (definitions 32 → 34, mechanisms 7 → 8). Four reading notes added; no new `front/sources.tex` keys (all sources are catalogue keys).

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 210 pages (207 before); no LaTeX warnings; 0 overfull and 26 underfull boxes, all in the legacy volatility-options (25) and portfolio (1) files, as before; the one `page.i` warning. Rendered and inspected: PDF p. 65 (the execution-trading-costs opener), pp. 105–108 (the new chapter and its last page), p. 109 (the part page for notes awaiting migration) and p. 167 (the legacy execution-market-making opener, now the last legacy chapter). Tests: 14 passed; `synthetic_short_checks.py` and `funding_checks.py` pass.

### For review

- Routing all four blocks to `crypto-perpetuals` against the map, and the new `digital-assets-prediction-markets` chapter.
- The checker change for figures-only legacy folders.
- The five backlog stubs, three of which name other pathways.

## crypto market structure review follow-up: socialised-loss trigger, 15 October 2026

A narrow correction to one item of `def:crypto-trading-risk-layers`; the crypto market structure review record above is left as written.

- **Source rechecked.** Deribit FZE Exchange Rulebook version 2.0, applicable 13 August 2026 (help-centre article updated and edited 15 September 2026, unchanged since crypto market structure review), retrieved again on 15 October 2026 through the help-centre JSON API: Rules 10.6–10.11 with their guidance notes, and Rules 9.16–9.17 for comparison.
- **Finding.** crypto market structure review wrote that socialised loss applies "if the fund is depleted". Rule 10.8 has two branches: the insurance fund is depleted in all currencies, **or** it is depleted in the bankrupt account's currency and Deribit decides not to convert other currencies. In either case Deribit "may, in its absolute discretion" trigger the mechanism. Converting another currency of the fund under Rule 10.7 is also at its absolute discretion. Socialised loss can therefore be triggered while other currencies remain in the fund, and is not automatic when the fund is exhausted.
- **Changed.** The *socialised loss* item now states both branches and both discretions (Rule 10.8), with the deductions, halts, cancellations and mark-price closes cited to Rules 10.9–10.11 rather than 10.8–10.11. It also records "the same day's session" and "in any currency" as Rule 10.9(a) words them. The *insurance fund* item now says that conversion is discretionary and applies when the fund in the account's currency is depleted. The entry's status records the recheck; verification stays *partly checked*, stability *draft*, currency *Deribit as of October 2026*.
- **Notes.** The `gapclose-deribit-rules` reading note records the two-branch trigger. It also notes that Rule 9.17 applies the same trigger to a short spot under cross-collateral margin, read but not used in an entry. The `crypto-perpetuals` pathway note records the correction. No other entry, stub, ownership or count changed; `funding_checks.py` is unaffected and was not rerun.

## backtest evaluation review: research and backtest evaluation, 15 October 2026

Migration of the four-block research file of Narang's systematic-investing chapter, run after the crypto market structure review follow-up above. Migration and source checking, not study; no checkpoint was attempted, and no reading of the owning pathway was read.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/research.tex`: 4 counted blocks (one `definition`, three `remark`s) with their 21 items. Outside them was only the `% migrate-to:` line and the subsection heading (checked by script). The file and its map row were deleted. In `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment naming the destinations. The legacy chapter's other files, `sysinv/modelrisk.tex` included, are unchanged, as are earlier artefacts, the 21 PNGs, `house.tex` and the guide pin (`343d145`).

### Ownership and dispositions

The map names only `research-engineering-validation`, a **section overview**. Its outcome is reconstructing a research decision and its trade from versioned identities, data events, experiments and control records; its readings are GLEIF, CRSP CIZ, CDM, FIX, bitemporal data, DDIA, MLflow and BCBS 239. None of the four blocks is about that. The specialist pathways were compared:
- `backtest-inference`: reporting a strategy result with the number of trials, multiplicity-adjusted significance and Sharpe-ratio uncertainty. Its readings include p-hacking incentives, a backtesting protocol, Sharpe-ratio statistics and leakage and look-ahead audits.
- `point-in-time-data`: research panels whose every field was available at decision time.
- `model-governance-controls`: model inventory, validation and pre-trade controls.
- `reproducible-research-code`: rebuildable research packages.

**Routing exception:** all four blocks go to `backtest-inference`. They concern forming hypotheses and judging backtests, which that pathway owns, although its statistics are not in the blocks. Historical borrow availability is stubbed with `point-in-time-data` named as its home. Nothing was routed to `model-governance-controls` or `reproducible-research-code`. The pathway had no note; the topic review opened `notes/pathways/backtest-inference.md` and the topic file `compendium/research-engineering-validation/backtest-evaluation.tex`. The artefact sits under the map candidate, `notes/artefacts/research-engineering-validation/`, keeping the file whole, as in trading infrastructure / equity market structure / securities lending and synthetic shorts / crypto market structure reviews.

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

`check_compendium.py --check`, 0 problems: 609 → 605 legacy blocks = 530 shared + 46 single-candidate + 29 assigned. `research-engineering-validation`: exclusive 4 → 0. `backtest-inference`: entries 0 → 4, backlog stubs 0 → 8 (new note). Entries 91 → 95 (methods 14 → 16, pitfalls 0 → 2, the first Pitfall entries). One reading note added (`s7-narang`); no new `front/sources.tex` keys.

### Other files

- Chapter opener `compendium/research-engineering-validation/section.tex`: pathway comment, opening paragraph and `\input` updated; its legacy-candidate comment now names only `sysinv/modelrisk.tex`.
- `notes/log.md`: coverage row for `backtest-inference`; the `s7-narang` progress cell now records the edition question; two open questions appended.
- `compendium/README.md` (order paragraph) and `README.md` (layout line for `source-review-records.md`).
- Numerical scripts: unchanged and not rerun, since no content they check changed.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 213 pages (210 before); no LaTeX warnings; the one `page.i` duplicate-destination warning; 0 overfull and 26 underfull boxes, all in the legacy volatility-options and portfolio files, as before. The first build had four new overfull boxes from the artefact path in each entry's *Further reading*; they were removed by splitting the path. Rendered and inspected: PDF pp. 7–11 (the chapter opener and the four new entries, plus the start of the operational-controls section), pp. 111–112 (`def:crypto-trading-risk-layers` after the crypto market structure review follow-up) and p. 169 (the legacy portfolio chapter where the research subsection was). Tests: 14 passed.

### For review

- Routing all four blocks to `backtest-inference` against the map, and opening that pathway's note with eight stubs, two of which name other pathways.
- Citing the third edition while the catalogue leaves the edition open.
- The qualifications to Narang's heuristics: smooth P&L, lower volatility, the R² of 0.05, time decay as crowding, and parameter stability as evidence against overfitting.

## backtest evaluation review follow-up: corrections, 15 October 2026

Narrow corrections after an audit of backtest evaluation review; the backtest evaluation review record above is left as written, and this record supersedes it where they differ. The artefact `notes/artefacts/research-engineering-validation/derivations.tex` is unchanged.

- **S&P example, `meth:backtest-evaluation-diagnostics`.** backtest evaluation review described the strategy as "long when the index's earnings yield exceeds the 10-year Treasury yield and short otherwise", which leaves out its no-trade state. Narang (third edition) p. 168 reads a higher stock yield as a signal to be long and a lower one as a signal to be short, as "an adjustment to" the equity risk premium. P. 173 says the strategy signals "only when the model perceives that the opportunity is sufficiently attractive to warrant trading at all" and is at zero 65% of the time. The entry now gives both, and says that the adjustment and the threshold are not stated; no threshold was supplied.
- **Ratio signs, same entry.** Narang defines Calmar as average return divided by the worst drawdown and Omega as the sum of positive returns divided by the sum of negative returns, both of which have negative denominators taken literally. He reports both as positive (0.31 and 1.26, pp. 173–174). The entry now quotes his wording and sets out, as interpretation, the explicit conventions Calmar $=\bar R/\lvert\mathrm{MDD}\rvert$ and $\Omega(0)=\sum\max(R_t,0)/\lvert\sum\min(R_t,0)\rvert$. Hand-check, in the session with no script kept: $12.1/\lvert-39.7\rvert=0.305$ against $-0.305$ taken literally; returns $+2,+1,-1.5,-0.5$ give $\Omega(0)=3/2=1.5$ against $-1.5$. His Sterling and Omega values were not recomputed, since the strategy's returns are not available.
- **Item count.** The backtest evaluation review *Preservation* paragraph says "all 21 items are present". The 21 counted the substring `\item`, which also matches the three `\setlength{\itemsep}{0pt}` lines. The original has 18 `\item` commands: 3 in *Scientific Method*, 4 in *Sources of Alpha Idea Generation*, 11 in *Model Quality Assessment* and none in *Other Considerations in Model Testing*. Recounted against `9148410:…/sysinv/research.tex` with a pattern that excludes `\itemsep`; all 18 and the three `\itemsep` lines appear in the artefact. No text was lost.
- **Guidance after the record split.** `compendium/README.md` now points dispositions and checks to `source-review-records.md` (its opening paragraph and entry disposition instructions). In `source-review-index.md` the progress table's "checks table below" now points to the topic review *Checks and their limits*, and the backtest evaluation review index row now gives its commit `c45e2b5`. Historical slice narratives that mention `source-review-index.md` were not changed.
- **Notes.** The `s7-narang` reading note and the `backtest-inference` pathway note record the corrections. Entries, stubs, ownership and counts are unchanged (605 legacy blocks; 95 entries).

## model risk and contagion review: risk assessment (model risk, regime change, shocks, contagion, monitoring), 15 October 2026

Migration of the five-block risk-assessment file of Narang's systematic-investing notes, run after the backtest evaluation review follow-up above. Migration and source checking, not study; no checkpoint was attempted, and no reading of either owning pathway was read.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/modelrisk.tex`: 5 counted blocks (four `definition`s and one `method`) with their 7 `\item` commands (3 in *Model Risks*, 4 in *Risk Monitoring Methods*; the two `\setlength{\itemsep}{0pt}` lines are not items). Outside the blocks was only the `% migrate-to:` line and the subsection heading (checked by script). The file and its map row were deleted. In `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The other `sysinv/` files, other legacy files, earlier artefacts (including `notes/artefacts/model-governance-controls/derivations.tex` from trading infrastructure review), the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map names `model-governance-controls`, whose outcome is designing a model inventory, validation and change process and the pre-trade and kill-switch controls a strategy needs before production, with monitoring in its checkpoint. Model risk, regime change, exogenous shocks and their monitoring are what such a process must cover, so blocks 1, 2, 3 and 5 stay with it.

`funding-crowding` (section `portfolio-risk-financing`) has the outcome of tracing "how margin, leverage, funding runs and crowded positions turn small shocks into forced liquidations". Its readings include the 2007 quant meltdown (`exp-khandani-lo-quant-meltdown`) and crowded exits (`wide-pedersen-exit`). The contagion block is about common positions, cross-collateralisation, volatility targeting and forced exits, so **routing exception:** block 4 goes to `funding-crowding`. Other candidates were rejected:
- `risk-tail-systemic` (fire-sale stress tests) and `risk-parity-vol-targeting` (volatility targeting as an allocation method): the block describes the mechanism of forced exits, not a stress model or an allocation rule.
- `macro-regimes-stock-bond` (regime identification) for block 2: the block is a model-risk statement, not regime estimation.

The new entries opened the topic files `compendium/research-engineering-validation/strategy-risk.tex` and `compendium/portfolio-risk-financing/crowding-contagion.tex`, and the pathway note `notes/pathways/funding-crowding.md`. The artefact sits under the map candidate as a new file, `notes/artefacts/model-governance-controls/risk-assessment.tex`, so that trading infrastructure review's `derivations.tex` there is unchanged.

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

No claim was deleted outright. **Kept distinct:** the backtest evaluation review stub `ev:signal-decay-crowding` in `backtest-inference` (does delayed-signal decay identify crowding?) is unchanged and is named in the contagion entry as a separate question.

**Existing entries checked.**
- `meth:automated-trading-operational-controls`: covers operational controls, the destination for implementation failure; cross-referenced, unchanged.
- `meth:execution-decision-support`: execution-algorithm indicators; cross-referenced from the monitoring entry, unchanged.
- `meth:backtest-evaluation-diagnostics`: the source of expected hit rates and exposures; cross-referenced.
- `pit:parameter-overfitting`: contrasted with regime change; cross-referenced.
- `res:arbitrage-risks`: Harris's model risk and staying power; already pointed to `funding-crowding`; cross-referenced, unchanged.
- Also linked: `ev:square-root-impact`, `mech:futures-margin-settlement`, `def:securities-lending-fee-rebate`.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024, the same local copy as backtest evaluation review (text layer through PDFKit; printed page = PDF page − 20). Chap. 10, "Risks Inherent to Quant Strategies", secs. 10.1–10.6, pp. 191–211, was verified to exist in this edition from the contents (pp. 191–211) and the running heads. Exhibit 10.6 (p. 206) was read by page image; Exhibits 10.1–10.5 were read from the text layer only.
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

`check_compendium.py --check`, 0 problems: 605 → 600 legacy blocks = 530 shared + 41 single-candidate + 29 assigned. `model-governance-controls`: exclusive 5 → 0, entries 1 → 3, stubs 2 → 4. `funding-crowding`: entries 0 → 1, stubs 0 → 4 (new note). Entries 95 → 98 (definitions 34 → 36, methods 16 → 17). The `s7-narang` reading note was extended; no new `front/sources.tex` keys.

### Other files

- Chapter openers of `research-engineering-validation` (`model-governance-controls` now three entries; no legacy file now mapped to the section) and `portfolio-risk-financing` (`funding-crowding` added first, as in the guide's order).
- `notes/log.md`: coverage rows for `model-governance-controls` and `funding-crowding`, the `s7-narang` progress cell, and one open question appended.
- `notes/source-review-index.md`: status, index, the topic review and map.
- `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 216 pages (213 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, none in the changed chapters, as before. Rendered and inspected:
- PDF pp. 8–9: the backtest evaluation review corrections, including the displayed Calmar and Omega formulas;
- pp. 13–15: the end of the operational-controls entry and the two new `model-governance-controls` entries;
- pp. 22–23: the `portfolio-risk-financing` opener and the contagion entry;
- p. 172: the legacy portfolio chapter, which now ends after the execution file.

Tests: 14 passed. The numerical scripts were not rerun; none covers changed content.

### For review

- Routing the contagion block to `funding-crowding` against the map, and the new pathway note with four stubs.
- Presenting Narang's 2007 drivers as his explanation, and the Pulte Homes arithmetic against his text.
- The qualification of discretionary overrides, and implementation failure treated as operational rather than model risk.

## model risk and contagion review follow-up: overrides, impact inference and the Calmar ratio, 15 October 2026

Narrow corrections to backtest evaluation / model risk and contagion reviews after an audit, run before transaction-cost models review; the records above are left as written, and this record supersedes them where they differ. No legacy block, entry label, stub, artefact or count changed (600 legacy blocks; 98 entries). The passages were reread in the same local third edition of `s7-narang` (text layer; printed page = PDF page − 20).

- **Overrides, `def:quant-strategy-risk-sources`** (`compendium/research-engineering-validation/strategy-risk.tex`). model risk and contagion review wrote that "an override is itself an unvalidated change to the model". The entry now separates an ad hoc intervention, improvised outside the validated design and in effect an untested model change, from an approved contingency response (a pre-specified de-risking rule, limit or kill switch whose triggers, authority and effects were tested and approved), which is part of the validated design. Narang's p. 208 account and the one-firm anecdote are unchanged. Operational failure is now said to be made less likely and less costly by testing, change control and operational controls, which mitigate it rather than guarantee its prevention. The five causes are presented as overlapping questions (a regime change can expose a misspecification; others' forced selling can look like a regime change; one loss can have several causes), not exclusive categories. The `model-governance-controls` pathway note records the change.
- **Pulte Homes and impact, `def:common-investor-contagion`** (`compendium/portfolio-risk-financing/crowding-contagion.tex`). model risk and contagion review set Narang's "quadratic nature of market impact" (p. 206) against the square-root law as if the table contradicted it. That inference is withdrawn: average daily volume and returns over crisis sub-periods give no metaorder sizes or schedules, mix many traders' flow, and do not reveal the price without the liquidation, so they identify no metaorder impact exponent, quadratic or square-root. The checked arithmetic (31.75% fall, about a third recovered, 3.7–5.4 times the earlier pace) and the separation of Narang's account from causal evidence are kept; his unsourced "as much as 15 percent in market impact" is now noted. The `funding-crowding` note and the `s7-narang` reading note record the change; the dated open question in `log.md` is left as written, with a new dated line withdrawing its impact clause.
- **Calmar ratio, `meth:backtest-evaluation-diagnostics`** (`compendium/research-engineering-validation/backtest-evaluation.tex`). $12.1/39.7=0.30479$, which rounds to 0.30, while Narang reports 0.31 on pp. 173 and 174. The entry no longer says "as reported" after 0.30, and its *Practice* now says that most example figures agree within rounding, with the Calmar ratio the unexplained exception. No explanation was supplied. The backtest evaluation review *Findings* line "all consistent within rounding" is superseded for this ratio. Recomputed in the session: $12.1/39.7=0.3048$, $12.1/21.2=0.5708$, $19/35=0.5429$.
- **Index.** The model risk and contagion review row in `notes/source-review-index.md` now gives its commit `e0451c9`.

## transaction-cost models review: transaction cost models (components and cost functions), 15 October 2026

Migration of the transaction-cost-models file of Narang's systematic-investing notes, run after the model risk and contagion review follow-up above. Migration and source checking, not study; no checkpoint was attempted, and no reading of either owning pathway was read.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/txncostmod.tex`: an introductory paragraph outside the environments, and 2 counted blocks (one `remark`, one `definition`) with 7 `\item` commands (3 in *Transaction Cost Components*, 4 in *Types of Transaction Cost Models*; the two `\setlength{\itemsep}{0pt}` lines are not items). Outside the blocks were only the `% migrate-to:` line, the subsection heading and the introduction (checked by script). The file and its map row were deleted. In `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The other `sysinv/` files, other legacy files, earlier artefacts, the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map names only `portfolio-construction-risk`, a **section overview**, whose outcome is a portfolio "whose forecasts, risk model, constraints, costs and tail measures are explicit and testable", and whose first goal, constrained portfolios "with factor risk models, shrinkage and costs", names `portfolio-construction`. The candidates compared:
- `portfolio-construction`: construct a constrained portfolio from noisy forecasts "with a factor risk model, shrinkage and costs"; readings include convex Markowitz with costs and multi-period trading (`wide-boyd-markowitz-seventy`, `exp-boyd-multiperiod-trading`) and, as an optional branch, no-trade regions (`w2-davis-norman`). A cost function supplied to the portfolio optimiser, and the reason it exists, is this pathway's material.
- `execution-trading-costs` (overview): plan executions, estimate expected cost from a stated impact model and split realised shortfall into spread, impact, timing and fees. It already owns `def:transaction-costs`, `meth:transaction-cost-analysis` and `def:execution-benchmark`; the cost-components block restates those terms in Narang's words.
- `price-impact-execution`: estimate an impact model from executions. It owns `ev:square-root-impact`, `meth:almgren-impact-estimation` and `def:price-impact`, the evidence on the shape of impact costs. The legacy blocks make no estimation; their shape claims are checked against these entries, not moved into them.

**Routing exception:** the introduction and *Types of Transaction Cost Models* go to `portfolio-construction` as one new entry, `mod:portfolio-transaction-cost-function`, in the new topic file `compendium/portfolio-construction-risk/transaction-cost-models.tex`; *Transaction Cost Components* is merged into `def:transaction-costs` (owned by `execution-trading-costs`). Nothing was routed to `price-impact-execution`, whose entries are cross-referenced and unchanged. The pathway had no note; the topic review opened `notes/pathways/portfolio-construction.md`. The artefact sits under the map candidate as `notes/artefacts/portfolio-construction-risk/transaction-cost-models.tex`, keeping the file whole.

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

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024 (copyright page: ISBN 9781119931911 Adobe PDF), the same local copy as backtest evaluation / model risk and contagion reviews, read through PDFKit's text layer (printed page = PDF page − 20, checked again on this chapter). Chap. 5, "Transaction Cost Models", secs. 5.1–5.3 and notes, pp. 85–97, located from the contents (Transaction Cost Models 85; 5.1 p. 86; 5.2 p. 91; 5.3 p. 96; Notes p. 97) and the running heads. Exhibits 5.1–5.4 (pp. 93–95) and note 2 with Exhibit 5.5 (p. 97) were read from page images; p. 98 is blank (page image).
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

`check_compendium.py --check`, 0 problems: 600 → 598 legacy blocks = 530 shared + 39 single-candidate + 29 assigned. `portfolio-construction-risk`: exclusive 10 → 8. `portfolio-construction`: entries 0 → 1, stubs 0 → 2 (new note); exclusive 7, unchanged. `execution-trading-costs`: entries 14, unchanged (the merge changes an existing entry); stubs 0 → 1. Entries 98 → 99 (models 10 → 11). The note for `execution-trading-costs` names the new entry's pathway without its label, so that the entry is counted only under its owner. No new `front/sources.tex` keys (`exp-pfmi` is a catalogue key).

### Other files

- Chapter openers: `portfolio-construction-risk` (`portfolio-construction` added first, in the guide's order; the new topic file input before the performance file) and `execution-trading-costs` (the merge noted in its comment and opening paragraph).
- `notes/readings/s7-narang.md`: pathways, sections and key results for chap. 5; entries.
- `notes/log.md`: coverage row for `portfolio-construction`; the `s7-narang` progress cell; one open question appended.
- `notes/source-review-index.md`: status, index, the topic review and map; `compendium/README.md`: order paragraph.

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

## transaction-cost models review follow-up: units, cost-function conditions and the sell example, 15 October 2026

Narrow corrections to transaction-cost models review after an audit, run before portfolio construction review; the transaction-cost models review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub, artefact or count changed (598 legacy blocks; 99 entries).

- **Units, `mod:portfolio-transaction-cost-function`** (`compendium/portfolio-construction-risk/transaction-cost-models.tex`). transaction-cost models review let $q$ be shares, "contracts, or currency" while giving coefficients per share. The notation is now for one equity: $q$ and $V$ in shares, $P$ in currency per share, coefficients in currency, currency per share or currency per share squared, and $\eta$ dimensionless. The per-share cost $c(q)=C(q)/\lvert q\rvert$ is defined only for $q\neq0$. Contracts or notional are said to need their own units (such as a multiplier), not the same conversions. "Per-unit" became "per-share" where it meant that.
- **Parameter conditions.** All coefficients are nonnegative and every form has $C(0)=0$, $C\ge0$ and depends only on $\lvert q\rvert$. The displayed $\max_i(b_i\lvert q\rvert-d_i)$ with increasing slopes alone did not guarantee this: slopes 0.01, 0.03 with intercepts $-5$, 200 give $C(0)=5$, and with 5, 200 give $C(0)=-5$. The entry now uses the convex hinge form $b_0\lvert q\rvert+\sum_ih_i(\lvert q\rvert-\kappa_i)_+$ with $0<\kappa_1<\dots$, and states the equivalent maximum of lines with slopes $s_j=b_0+\sum_{i\le j}h_i$ and intercepts $d_j=\sum_{i\le j}h_i\kappa_i$. The 3/2-power form $\eta P\lvert q\rvert(\lvert q\rvert/V)^{1/2}$ is written out, and the assumptions are stated: symmetric between buys and sales, nonnegative (no rebates or favourable drift), expected rather than realised, one instrument and period, independent of duration and other trades.
- **Checks**, exact fractions in the session (no script kept): for $b_0=0.01$, $h=(0.02,0.05)$, $\kappa=(10{,}000,50{,}000)$, $C=0$ at 0 and 50, 100, 700, 1,300, 2,100 at $\lvert q\rvert=$ 5,000, 10,000, 30,000, 50,000, 60,000, equal for $\pm q$; left and right values at each breakpoint differ by under $10^{-7}$; equal to the maximum of lines (0.01, 0), (0.03, 200), (0.08, 2,700) at every point tested. The illustration with $\eta=0.01$, $P=50$, $V=10^6$ still gives \$500 and 10 bp at $\pm$10,000 shares and \$1,414.21 and 14.142 bp at 20,000.
- **Sell example, `def:transaction-costs`** (`compendium/execution-trading-costs/transaction-cost-analysis.tex`). transaction-cost models review said Narang's sale filled at \$100.20 "though the order did not raise the price". That assertion is removed: the example shows a negative arrival-to-fill cost against a benchmark, which does not identify the order's causal effect.
- **Notes and index.** The `portfolio-construction` and `execution-trading-costs` pathway notes record the changes; the transaction-cost models review row in `notes/source-review-index.md` now gives its commit `0224ac7`.

## portfolio construction review: portfolio construction models (rules, mean–variance optimisation, signal portfolios), 15 October 2026

Migration of the portfolio-construction-models file of Narang's systematic-investing notes, run after the transaction-cost models review follow-up above. Migration and source checking, not study; no checkpoint was attempted. One of the owning pathway's readings, Boyd et al., was read in part for method mechanics; that is source checking, not study of it.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/portconstmod.tex`: an introductory paragraph outside the environments, and 3 counted blocks (one `definition`, one `remark`, one `method`) with 13 `\item` commands (4 in *Rule-Based Models*, 3 in *Optimisers Models Parameters*, 6 in *Optimisation Techniques*), plus the remark's two paragraphs of prose before its list; the three `\setlength{\itemsep}{0pt}` lines are not items. Outside the blocks were only the `% migrate-to:` line, the subsection heading and the introduction (checked by script). The file and its map row were deleted; in `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The other `sysinv/` files (`alphamod.tex`, `riskmod.tex`, `executionmod.tex`, the overview's method block), other legacy files, earlier artefacts (including transaction-cost models review's `transaction-cost-models.tex`), the deferred assignments, the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map's only candidate is `portfolio-construction`, whose outcome is to "construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk", with readings on mean–variance selection, estimation error, shrinkage, factor risk models, risk-based portfolios, Black–Litterman and convex optimisation with costs. Every block is portfolio construction in that sense, so all stay with it; no routing exception. Equal risk contribution and GARCH volatility forecasts are stubbed here with their home pathways named (`risk-parity-vol-targeting`, `time-series-volatility`), as backtest evaluation review did for borrow data.

The new entries are in the new topic file `compendium/portfolio-construction-risk/portfolio-construction-models.tex`, input before transaction-cost models review's cost entry. The artefact is a new file, `notes/artefacts/portfolio-construction-risk/portfolio-construction-models.tex`, beside transaction-cost models review's, which is unchanged.

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

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024 (copyright page: Third Edition, ISBN 9781119931911 Adobe PDF), the same local copy as backtest evaluation / transaction-cost models reviews, text layer through PDFKit. Chap. 6, "Portfolio Construction Models", secs. 6.1–6.5 and notes, pp. 99–125 (PDF pages 119–145; contents: chapter p. 99, notes p. 125; running heads checked). Read by page image: Exhibit 6.1 (p. 102), 6.2 (p. 107), 6.4 (p. 111), 6.5 (p. 112), 6.6 (p. 116), 6.7 (p. 122) and the worked example on p. 118. Exhibit 6.3 (p. 109) was read from the text layer only.
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

`check_compendium.py --check`, 0 problems: 598 → 595 legacy blocks = 530 shared + 36 single-candidate + 29 assigned. `portfolio-construction`: exclusive 7 → 4, entries 1 → 4, stubs 2 → 7. Other pathways unchanged (`execution-trading-costs` 14/1, `model-governance-controls` 3/4, `funding-crowding` 1/4, `backtest-inference` 4/8, `crypto-perpetuals` 3/5). Entries 99 → 102 (methods 17 → 19, models 11 → 12). Reading notes: `s7-narang` extended, `wide-boyd-markowitz-seventy` opened. No new `front/sources.tex` keys.

### Other files

- Chapter opener `compendium/portfolio-construction-risk/section.tex`: comment, paragraph and inputs.
- `notes/pathways/portfolio-construction.md`: status, entries, related entries, backlog, legacy material, one question.
- `notes/log.md`: the `portfolio-construction` coverage row, the `s7-narang` progress cell, one open question.
- `notes/source-review-index.md`: status, index, the topic review and map; `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 222 pages (219 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, all after the start of the legacy part in the log, as before. The first builds had one overfull and one underfull box from a pathway key and the artefact file name in *Further reading*, and an underfull opening line of the mean–variance Statement; the wording was changed and the file name put on its own line. Rendered and inspected: PDF pp. 21–24 (opener and the three new entries), p. 25 (the corrected cost-function notation), p. 93 (the corrected sell example) and p. 177 (the legacy portfolio chapter, where *Risk Models* now runs into *Execution Model*). Tests: 14 passed.

### For review

- The reading of Exhibit 6.1 as inverse-variance and the ERC distinction.
- The correction of the unconstrained single-asset claim, and the treatment of Black–Litterman and resampling on Narang's and Boyd et al.'s accounts alone.
- Keeping Grinold and Kahn's approach as a separate entry on Narang's account only.
- The not-adopted data-mining and decision-tree details, which may come from an earlier edition.

## portfolio construction review follow-up: closed-form conditions, permutations, learning and rounding, 15 October 2026

Narrow corrections to portfolio construction review after an audit, run before risk models review; the portfolio construction review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub, artefact or count changed (595 legacy blocks; 102 entries).

- **Closed form, `mod:mean-variance-portfolio-optimisation`.** The entry now states that $w^\star=\tfrac1{2\gamma}\Sigma^{-1}(\mu+\nu^\star\mathbf 1)$ assumes a positive-definite $\Sigma$ and $\gamma>0$, and gives $\nu^\star=(2\gamma-\mathbf 1^\top\Sigma^{-1}\mu)/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$, the budget constraint's dual variable (Boyd et al., p. 4), which shifts all expected returns equally so that the weights sum to one. The volatility-target form is feasible only when $\sigma_{\mathrm{tar}}^2\ge1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$, quoting Boyd et al.'s "can be infeasible when $\sigma^{\mathrm{tar}}$ is too small" (p. 4). A singular $\Sigma$ is said to need separate treatment, with no pseudoinverse by default.
- **Single asset, same entry.** portfolio construction review said a single-asset answer arises "when risk is ignored". The entry now separates the bounded case (budget and no shorting: the highest-return asset) from the unbounded one (shorting allowed, returns not all equal) and box limits.
- **Resampling, same entry.** portfolio construction review said Narang's remark "shows that reordering cannot change the sample means and covariances an optimiser uses". His remark concerns one series. The entry now says that reordering one series keeps its mean and variance, a common permutation of multivariate rows keeps covariances, and independent permutations change them; Michaud's procedure and performance claims remain unchecked.
- **Machine learning, same entry.** "Supervised learning fits a forecast; it does not choose weights" is replaced by a distinction between forecasting, learning allocation weights (possible; its literature not read) and optimisation, keeping the narrower conclusion that the legacy item lacks source support.
- **ERC rounding and positive variance, `meth:rule-based-position-sizing`.** The displayed weights 29.9, 29.9 and 40.2 percent did not match the stored calculation ($b=0.401492$ rounds to 40.1); they now read about 29.93, 29.93 and 40.15 percent with their closed form. Normalised risk contributions are stated to require $w^\top\Sigma w>0$.
- **Transaction-cost entry.** `mod:portfolio-transaction-cost-function`'s *Further reading* and *Status* no longer say that no pathway reading was read; they name the parts of Boyd et al. read in portfolio construction review.
- **Checks**, in the session with numpy (no script kept): for a three-asset positive-definite $\Sigma$ (eigenvalues 0.0219, 0.0374, 0.0932), $\gamma=1$ and $\gamma=5$ give $\nu^\star=-0.0555$ and $0.0562$, weights summing to 1 and first-order residuals below $10^{-16}$; minimum variance 0.01396; with $\gamma=0$ the direction $(1,0,-1)$ raises return by 0.03 per unit with unchanged budget, so the problem is unbounded; two perfectly correlated assets give eigenvalues 0 and 0.08. Permutation: $x=y=(1,2,3,4)$, covariance 1.25; reversing $y$ alone gives $-1.25$ with means 2.5 and variances 1.25 unchanged; a common permutation keeps 1.25. ERC: 29.9254, 29.9254, 40.1492 percent; equal weights give 39.13, 39.13, 21.74 percent at variance 0.02044.
- **Notes and index.** The `portfolio-construction` note records the changes; `log.md` keeps its portfolio construction review line and gains a dated line narrowing it; the portfolio construction review index row gives `4e7666d`.

## risk models review: risk models (factor exposures, limits and penalties), 15 October 2026

Migration of the risk-models file of Narang's systematic-investing notes, run after the portfolio construction review follow-up above. Migration and source checking, not study; no checkpoint was attempted. Two further sections of Boyd et al., a reading of the owning pathway, were read for method mechanics.

### Scope

The whole of `compendium/legacy/portfolio-construction-risk/sysinv/riskmod.tex`: an introductory paragraph outside the environments, and 4 counted `method` blocks with 9 `\item` commands (4 in *Factor-Based Models*, 3 in *Statistical Models*, none in *Limiting Size of Risk*, which is prose only, and 2 in *Limiting the Types of Risk*), with the prose around them; the three `\setlength{\itemsep}{0pt}` lines are not items. Outside the blocks were only the `% migrate-to:` line, the subsection heading and the introduction (checked by script). The file and its map row were deleted; in `sysinv/sysinvoverview.tex` only its `\input` line was replaced, by a `% migrated:` comment. The remaining `sysinv/` files (`alphamod.tex`, `executionmod.tex`, `sysinvoverview.tex` with its method block), their inputs and the chapter wrappers, other legacy files, earlier artefacts (transaction-cost models / portfolio construction reviews included), the deferred assignments, the 21 PNGs, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

The map's only candidate is `portfolio-construction` ("construct a constrained portfolio from noisy forecasts with a factor risk model, shrinkage and costs, and attribute its realised risk"). The factor-model, size-limit and exposure-type material is that pathway's. The *Statistical Models* block lists historical simulation, Monte Carlo simulation and parametric methods for "risk metrics" and "key risk measures"; it is about estimating portfolio risk measures, not about the covariance an optimiser uses. `risk-tail-systemic` has the outcome "forecast and backtest VaR and ES, design a tail hedge, and run a stress test", with a checkpoint built on filtered historical simulation and EVT. **Routing exception:** that block goes to `risk-tail-systemic`, as a backlog item only (`meth:var-es-estimation-methods`), because its text is generic, absent from Narang's chapter, and supports no entry; the topic review opened `notes/pathways/risk-tail-systemic.md`. Nothing went to `time-series-volatility`: the block does not discuss GARCH, and `mod:garch-volatility-forecast` is unchanged.

One new entry, `mod:factor-risk-model`, in the new topic file `compendium/portfolio-construction-risk/risk-models.tex`; the size-limit block merged into `mod:mean-variance-portfolio-optimisation`. The artefact is a new file, `notes/artefacts/portfolio-construction-risk/risk-models.tex`, beside those of transaction-cost models / portfolio construction reviews.

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
- `meth:rule-based-position-sizing`, `meth:signal-portfolio-allocation`, `mod:portfolio-transaction-cost-function`: no overlap beyond cross-references; unchanged in the topic review (the first two were corrected in the follow-up above).
- Stub `meth:portfolio-covariance-estimation`: narrowed to estimation (shrinkage, fitting a factor model, out-of-sample tests), since the factor model's structure is now in the new entry.
- Stub `mod:garch-volatility-forecast` (home `time-series-volatility`): unchanged; the statistical block does not discuss GARCH.
- Cross-referenced, unchanged: `def:quant-strategy-risk-sources` (`model-governance-controls`), `def:common-investor-contagion` (`funding-crowding`), `pit:parameter-overfitting` (`backtest-inference`).

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024, the same local copy as backtest evaluation / portfolio construction reviews, text layer through PDFKit. Chap. 4, "Risk Models", secs. 4.1–4.4 and notes, pp. 71–84 (PDF pages 91–104; contents: chap. 4 p. 71, notes p. 84; running heads checked). Its only exhibit, 4.1 (p. 83), the black-box schematic, was read by page image; the chapter has no data exhibits.
- **Boyd et al.** (`wide-boyd-markowitz-seventy`), authors' version of 5 January 2024, the same copy as portfolio construction review: sec. 3.3, factor model (pp. 20–21), and sec. 4.2, softening constraints (pp. 25–27). The reading note records them.
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

`check_compendium.py --check`, 0 problems: 595 → 591 legacy blocks = 530 shared + 32 single-candidate + 29 assigned. `portfolio-construction`: exclusive 4 → 0, entries 4 → 5, stubs 7 (one narrowed). `risk-tail-systemic`: entries 0, stubs 0 → 1 (new note). `portfolio-construction-risk` (overview): exclusive 8, unchanged. Other pathways unchanged (`execution-trading-costs` 14/1, `model-governance-controls` 3/4, `funding-crowding` 1/4, `backtest-inference` 4/8, `crypto-perpetuals` 3/5). Entries 102 → 103 (models 12 → 13). No new `front/sources.tex` keys.

`portfolio-construction` now has no legacy file listing it alone. That is migration progress only: its backlog is open, no reading has been studied, and the remaining `sysinv/` files, mapped to the overview, may still bear on it.

### Other files

- Chapter opener `compendium/portfolio-construction-risk/section.tex`: comment, paragraph and inputs.
- `notes/pathways/portfolio-construction.md` (entries, related entries, backlog, legacy material); `notes/pathways/risk-tail-systemic.md` (new).
- `notes/readings/s7-narang.md` and `notes/readings/wide-boyd-markowitz-seventy.md`.
- `notes/log.md`: coverage rows for `portfolio-construction` and `risk-tail-systemic`, the `s7-narang` progress cell, one open question.
- `notes/source-review-index.md`: status, index, the topic review and map; `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 223 pages (222 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 26 underfull boxes, all after the start of the legacy part in the log, as before. No new bad boxes at any stage. Rendered and inspected: PDF pp. 22–24 (the portfolio construction review corrections and the merged size-limit and covariance passages), pp. 25–26 (the factor-risk-model entry), p. 177 (the legacy portfolio chapter, where the overview's method block now runs into *Alpha Models Overview*), and the artefact's page. Tests: 14 passed.

### For review

- Routing the statistical-methods block to `risk-tail-systemic` as a backlog item only, and opening that note without entries.
- Reading the legacy factor list as roles that depend on the strategy, and "unintended is not uncompensated".
- Merging the size-limit material into the mean–variance entry, including the softening reading of penalties and the non-adoption of Narang's VaR and dispersion statements.

## risk models review follow-up: residual diversification, the CVX–XOM hedge and compensation, 15 October 2026

Narrow corrections to risk models review after an audit, run before systematic-investing architecture review; the risk models review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub, artefact or count changed (591 legacy blocks; 103 entries). Narang's p. 76 was reread in the same third-edition copy.

- **Residual diversification, `mod:factor-risk-model`.** risk models review said that "diversification of residual risk depends on the diagonal-$D$ assumption holding". A diagonal $D$ with bounded variances and equal weights is sufficient, not necessary. The entry now keeps the constant-equicorrelation example (correlation 0.2, variance 0.09: $0.018+0.072/n$, a floor of 0.018) and adds a counterexample: correlation 0.2 within disjoint pairs only gives $0.108/n$, which still vanishes. In these examples correlation confined to small groups still diversifies, while correlation shared by every pair leaves a floor, like an omitted factor. Checked with numpy for $n=10$, 100, 1,000 (0.0108, 0.00108, 0.000108; and 0.0252, 0.01872, 0.018072).
- **CVX–XOM, same entry.** "Removed by shorting XOM" is replaced by Narang's "substantially eliminated" (p. 76), with the interpretation that equal dollar positions hedge the market exactly only with equal betas; exact neutrality needs beta-weighted sizes under a stated risk model.
- **Compensation, same entry.** "Narang's rule assumes that exposures the alpha model does not forecast earn nothing" is replaced by his wording, "no expectation of being compensated sufficiently" (p. 76): expected reward not enough for the risk, not zero.
- **Notes and index.** The `portfolio-construction` and `s7-narang` notes record the changes; `log.md` keeps its risk models review line and gains a dated correction; the risk models review index row gives `cd7b13c`.

## systematic-investing architecture review: Narang's systematic-investing cluster (overview and diagram, alpha models, execution), 15 October 2026

A multi-file batch: the last three files of Narang's systematic-investing notes, migrated together after the risk models review follow-up above, with the legacy chapter removed. Migration and source checking, not study; no checkpoint was attempted and no reading of any owning pathway was studied.

### Scope

Under `compendium/legacy/portfolio-construction-risk/` (all mapped to the section overview `portfolio-construction-risk`), counted by script against the committed originals:

| File | Counted blocks | `\item` commands (excluding `\itemsep`) | Outside the blocks |
|---|---|---|---|
| `sysinv/alphamod.tex` | 3: *Theory Driven Models* (definition, 5), *Strategy Parameters* (method, 6), *Blending of Models* (method, 3) | 14 | introduction (318 characters) and the data-driven paragraph (308) |
| `sysinv/executionmod.tex` | 4: *Order Execution Algorithm Parameters* (remark, 5), *High Frequency Trading*, *HFT Shark Strategy* (definitions), *HFT Trading Infrastructure* (remark) | 5 | introduction (926 characters) |
| `sysinv/sysinvoverview.tex` | 1: *Chains of Production for Alpha Signals* (method, 6 + 5 nested) | 11 in the block, 3 in the module list outside it | introduction, the figure, the module list, the bridge prose, two `\input` lines and the backtest evaluation / risk models reviews `% migrated:` comments |
| **Total** | **8** | **33** (substring counts would give 39) | |

Also accounted for: `figures/strategystructure.tikz` (moved to `compendium/portfolio-construction-risk/figures/`, with a return arrow added) and the chapter wrapper `section.tex` (removed). The line `\InputIfFileExists{legacy/portfolio-construction-risk/section}{}{}` was removed from `compendium/legacy/part.tex`, the three map rows from `notes/source-review-index.md`, and the empty folder. The other legacy chapters, earlier artefacts, the deferred assignments, the 21 PNGs of the legacy execution chapter, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

Each block was routed by concept against the guide's outcomes; the map candidate, the overview whose outcome is a portfolio "whose forecasts, risk model, constraints, costs and tail measures are explicit and testable", kept the material about the structure of a strategy and its forecasts. **Routing exceptions:** signal combination to `equity-long-short-construction` (outcome: "scale forecasts, combine signals … compare mixing with integrating"), opening the canonical chapter `systematic-equities/` and the pathway's note; the production chain to `model-governance-controls` (inventory, validation, change and approval before production); execution material into existing `execution-trading-costs` entries; HFT material into `hft-market-design`'s `def:hft-strategies`. Rejected: `trend-following`, `statistical-arbitrage` and `equity-factor-premia` for the alpha taxonomy (the block makes no evidence claims those pathways test; evidence stubbed with them named as homes); `backtest-inference` for strategy parameters (cross-referenced); `market-structure-execution-quality` for routing and spoofing (stub only); `research-engineering-validation` overview for the production chain (its outcome is reconstructing decisions from records, not promotion stages).

| File and block | Owner | Destination | Checked source | Disposition |
|---|---|---|---|---|
| overview: introduction, figure, module list, bridge prose | `portfolio-construction-risk` | `def:quant-strategy-components` (new), Figure (redrawn) | Narang chap. 2, pp. 16–19; Exhibit 2.1 by page image | Rewritten; return arrow restored |
| overview: *Chains of Production* (11 items) | `model-governance-controls` | `meth:strategy-production-lifecycle` (new); stub `meth:strategy-promotion-criteria` | López de Prado (`alpha-afml`) chap. 1, pp. 5–9 | Rewritten as one author's prescription |
| alpha: introduction, *Theory Driven Models* (5), data-driven paragraph | `portfolio-construction-risk` | `def:alpha-model-taxonomy` (new); stubs `ev:trend-following-evidence`, `meth:residual-reversion-strategy`, `ev:value-carry-premia` | Narang chap. 3, secs. 3.1–3.3, pp. 23–52; Exhibit 3.2 by page image | Rewritten; three classes added; claims qualified |
| alpha: *Strategy Parameters* (6) | `portfolio-construction-risk` | `meth:alpha-strategy-specification` (new) | sec. 3.4, pp. 52–63 | Rewritten; conditioning variables added |
| alpha: *Blending of Models* items i–ii | `equity-long-short-construction` | `meth:alpha-signal-combination` (new); stubs `meth:forecast-scaling-ic`, `meth:signal-mixing-vs-integration` | sec. 3.5, pp. 64–68; Exhibits 3.9–3.10 by page image | Rewritten; "independence" corrected |
| alpha: *Blending of Models* item iii | `model-governance-controls` | merged into `meth:strategy-production-lifecycle` | López de Prado pp. 5–6 | Merged; source corrected (not Narang) |
| execution: introduction | `execution-trading-costs` | merged into `def:order-exposure-decisions`, `def:portfolio-trading`, `def:automated-trading-architecture` | Narang chap. 7, pp. 127–129 | Merged |
| execution: *Order Execution Algorithm Parameters* (5) | `execution-trading-costs` | merged into `def:order-exposure-decisions`; stub `rule:spoofing-securities-markets` in `market-structure-execution-quality` | chap. 7, pp. 129–138; chap. 14, p. 270; Appendix pp. 314–315; 7 U.S.C. §6c(a)(5) | Merged; item v kept as an unresolved pitfall |
| execution: *High Frequency Trading* | `hft-market-design` | merged into `def:hft-strategies` | chap. 15, pp. 291–293; chap. 7, pp. 129–134 | Merged; ML claim not adopted |
| execution: *HFT Shark Strategy* | `hft-market-design` | merged into `def:hft-strategies` (Pitfalls) | Appendix, pp. 312–314; FINRA Rule 5270; SEC 2010 release as already cited | Kept as historical description, qualified |
| execution: *HFT Trading Infrastructure* | `execution-trading-costs` | merged into `def:automated-trading-architecture` | chap. 7, pp. 138–141 | Merged; FIX reversal corrected |

**Subclaims.**

| Where | Legacy claim | Disposition |
|---|---|---|
| overview intro | Schematic of a live production strategy, without research tools | Rewritten (p. 17); data and research added from Exhibit 2.3 (p. 19) |
| overview figure | Three modules → portfolio construction → execution | Redrawn with Exhibit 2.1's return arrow (portfolio construction and execution "interact"); original kept verbatim and rendered in the artefact |
| overview list i–iii | Alpha predicts; risk limits unrewarded exposure, "i.e. directional exposure limit on an asset class"; t-cost model decides if costs are "desirable" | Rewritten (pp. 17–18); the risk example generalised by the legacy, qualified; the t-cost model estimates costs, the portfolio model decides |
| overview bridge | Portfolio construction balances profit and risk; trades are the differences; execution uses urgency and liquidity | Rewritten (p. 18); costs added to the balance; Exhibit 2.2 checked |
| chain i–v | Data curation, feature analysis, strategists, backtesters, deployment | Rewritten from AFML pp. 7–8; "good back-tested" read as backtester; probability of overfitting from the number of trials added |
| chain vi.1–5 | Embargo, paper trading, graduation, re-allocation ("follows a concave function"), decommission | Rewritten (pp. 8–9); "in general" and the decommission condition restored; no quantitative criteria in the source (stub) |
| alpha intro | Theory-driven tests theories; price data → trend and reversion; fundamental → value, growth, quality; models combined | Rewritten (pp. 25–29): eight classes, not five; technical sentiment, supply/demand and tactical/events added |
| theory i | Trend: consensus-building; moving-average crossover "has less than one point of return for every point of downside risk" | Consensus and greater-fools rationales kept (pp. 29–30); the return-to-downside sentence restored to its subject, "the typical successful trend follower" (p. 32), unsourced; evidence stubbed |
| theory ii | Mean reversion; stat arb; trends and reversions coexist | Rewritten (pp. 33–35); coexistence by horizon (Exhibit 3.5); March 2020 pitfall noted; evidence stubbed |
| theory iii | Value as inverted ratios; "buying undervalued … selling overvalued … is a carry trade"; QLS | Rewritten (pp. 38–41); carry restored to a yield spread (p. 40, example checked); value and carry kept apart as interpretation; stub |
| theory iv–v | Growth; quality | Rewritten (pp. 42–46) |
| data-driven paragraph | Harder, data mining, less practised, more used at high frequency | Rewritten (pp. 47–52); his "in general … do not work" kept as judgement |
| params i | Signal strength → bigger bet | Kept as his "in general, though certainly not always" (p. 53), with his large-signal caution; calibration, risk, correlation, costs and constraints added as interpretation |
| params ii | Short-term strategies vary more | Rewritten (pp. 53–55) as his generalisation |
| params iii | Pairs, clusters, statistical or heuristic grouping; relative alpha smoother in normal times | Rewritten (pp. 55–57); the smoothness claim kept as a conditional generalisation without data |
| params iv | Universe; "biotech stocks are excluded" | Rewritten (pp. 57–59); "some quants exclude" restored |
| params v | Model specification; ML for parameters; refitting raises overfitting | Rewritten (pp. 59–60); his "without overfitting" claim not adopted |
| params vi | Run frequency trade-offs | Rewritten (pp. 61–62) |
| (omitted) | Conditioning variables | Added (pp. 60–61) |
| blending stem | Linear, nonlinear, ML; or separate portfolios | Rewritten (pp. 64, 68) |
| blending i | Linear "require independence of factors" | Corrected: additivity, not statistical independence (p. 65; interpretation); regression weights; example checked |
| blending ii | Nonlinear: conditional; rotational weights favour recent performance | Rewritten (pp. 66–67); rotation qualified as a bet on factor trends, no evidence |
| blending iii | ML research effort; macroscopic against microscopic alpha | Source corrected to López de Prado (pp. 5–6); merged into the lifecycle entry as opinion |
| exec intro | Electronic or human; DMA; build/broker/vendor; portfolio bidding | Merged (pp. 127–128) |
| exec i | Aggressive/passive; rebates; momentum aggressive, reversion passive; signal strength; middle ground | Merged (pp. 130–133); side-dependence of "aggressive" made explicit; venue-specific fees and inverted venues noted; inside-spread orders need spread > tick |
| exec ii | Splitting large orders | Merged (pp. 136–137) |
| exec iii | Hidden orders lose priority; iceberging | Merged (pp. 131, 134–135); "most exchanges", venue rules |
| exec iv | Smart order routing | Cross-referenced to `def:smart-order-routing` (Narang pp. 137–138; his dated venue names and his Reg NMS description not adopted) |
| exec v | Orders "with no intention of execution", cancelled; small sell orders to "improve market perception" | Not in the third edition. Kept as a description of conduct, not a technique: for futures and swaps on registered entities, 7 U.S.C. §6c(a)(5)(C) makes "spoofing" unlawful; the securities and non-U.S. positions are unresolved (stub). Narang's defence of routine cancellation cited |
| HFT block | Microstructure alphas; ML discerns others' execution patterns, "somewhat stable" | Microstructure alpha mapped to fast alpha (pp. 291–293); the ML claim not in the third edition, not adopted |
| shark | Detect icebergs with small orders, front-run, "relatively riskless profit" | Not in the third edition; kept as a historical description of pinging for order anticipation; "front-run" qualified against Narang's fiduciary definition and FINRA Rule 5270; not riskless |
| infrastructure | Broker as agent; colocation; sponsored access; "software that implements FIX … free and open source"; own FIX engines | Merged (pp. 138–140); protocol and engine reversed back to Narang's wording; sponsored access referred to Rule 15c3-5; FIX licence unchecked |

No claim was deleted outright; every not-adopted claim stays in the artefacts and is named in an entry.

**Existing entries checked.** Changed: `def:order-exposure-decisions`, `def:portfolio-trading`, `def:automated-trading-architecture` (`execution-trading-costs`), `def:hft-strategies` (`hft-market-design`). Cross-referenced and unchanged: `def:smart-order-routing`, `def:order-anticipation`, `meth:automated-trading-operational-controls`, `meth:hypothesis-driven-strategy-research`, `meth:backtest-evaluation-diagnostics`, `pit:parameter-overfitting`, `meth:signal-portfolio-allocation`, `meth:rule-based-position-sizing`, `mod:mean-variance-portfolio-optimisation`, `mod:factor-risk-model`, `mod:portfolio-transaction-cost-function`, `def:quant-strategy-risk-sources`, `meth:quant-strategy-monitoring`.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), third edition, Wiley 2024, the local copy of backtest evaluation / risk models reviews (text layer; printed page = PDF page − 20). Read: chap. 2, secs. 2.1–2.2, pp. 16–19, Exhibit 2.1 by page image; chap. 3, "Alpha Models: How Quants Make Money", whole, pp. 23–69 (contents: 23; notes 69), Exhibits 3.2, 3.9 and 3.10 by page image; chap. 7, "Execution", whole, pp. 127–141 (contents: 127; notes 141); chap. 14, sec. 14.1.3, p. 270; chap. 15, sec. 15.4, pp. 291–293; Appendix, secs. A.2–A.2.2, pp. 311–315. "Shark" does not occur anywhere in the copy (text search).
- **López de Prado** (`alpha-afml`), *Advances in Financial Machine Learning*, Wiley 2018 (ISBN 9781119482086), local copy, text layer (printed page = PDF page − 27): chap. 1, secs. 1.2.2 and 1.3.1, pp. 5–9. A reading note was opened.
- **7 U.S.C. §6c** (`usc-7-6c`), 2024 edition, GPO via govinfo, retrieved 2026-10-15: paragraph (a)(5). The House Office of the Law Revision Counsel site returned "page not found".
- **FINRA Rule 5270** (`finra-rule-5270`), as displayed on finra.org on 2026-10-15.
- **Not read:** every reading of the overview, `equity-long-short-construction`, `trend-following`, `statistical-arbitrage`, `equity-factor-premia` and `market-structure-execution-quality` named in stubs; the FIX specification (`s6-fix`) and its licence; SEC and FINRA spoofing rules; EU MAR; earlier editions of Narang, from which the legacy's cancel-and-replace, ML-HFT and shark passages may come.

### Numerical checks

Recomputed in the session; no script kept and none existing covers this content: Exhibit 2.2 trades (+5, +5, −15, −15 percent); linear blend $0.7\times20+0.3\times(-10)=11$; carry $4.25-2=2.25$; variants $2\times4\times2\times4=64$; the conditional blend gives no signal or $+20$ percent. risk models review follow-up: equicorrelated and disjoint-pair residual variances (above).

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | as listed | Third edition; one practitioner's account; anecdotes and performance figures unsourced; several legacy passages from an unknown (probably earlier) edition |
| `alpha-afml` | pp. 5–9 | One author's prescription; no criteria or evidence for the stages |
| `usc-7-6c`, `finra-rule-5270` | (a)(5); (a) | Futures/swaps and FINRA members only; securities-market spoofing and other jurisdictions unchecked |
| Specialist readings | none | Stubs |

The five new entries and the merged passages are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Preservation

New artefacts in `notes/artefacts/portfolio-construction-risk/` (earlier ones unchanged):
- `alpha-models.tex` and `execution-model.tex`: each file below its `% migrate-to:` line, rendered, with only the subsection unnumbered;
- `systematic-investing-overview.tex`: displays, without executing, the removed `part.tex` line and exact copies of the chapter wrapper (`legacy-section-original.tex`), the overview (`sysinvoverview-original.tex`) and the diagram (`strategystructure-original.tikz`), and renders the diagram from its copy.

A script compared them with `git show HEAD:…`:
- the three copies are byte-identical to the committed originals;
- each body appears exactly once; the prose outside the blocks (318 and 308; 926 characters; the overview's in its copy) once each;
- all 8 blocks appear verbatim once each, in order;
- `\item` commands, matched as `\item` not followed by a letter: 5, 6, 3 (alpha, 14); 5, 0, 0, 0 (execution, 5); 11 in the block and 3 outside (overview, 14): 33 in both originals and artefacts; substring counts would give 17, 6 and 16;
- the `\begin`/`\end` sequences are identical (12, 10 and 10 commands).

All three artefacts compile alone without warnings or bad boxes (2, 2 and 3 pages); the diagram's rendering was inspected by page image.

### Counts

`check_compendium.py --check`, 0 problems: 591 → 583 legacy blocks = 530 shared + 24 single-candidate + 29 assigned. `portfolio-construction-risk` (overview): exclusive 8 → 0, entries 0 → 3, stubs 0 → 3 (new note). `equity-long-short-construction`: entries 0 → 1, stubs 0 → 2 (new note). `model-governance-controls`: entries 3 → 4, stubs 4 → 5. `market-structure-execution-quality`: stubs 1 → 2. `execution-trading-costs` (14/1) and `hft-market-design` (3 entries) unchanged in count, their entries extended. Entries 103 → 108 (definitions 36 → 38, methods 19 → 22). Two `front/sources.tex` keys added (`finra-rule-5270`, `usc-7-6c`); reading notes `s7-narang` extended and `alpha-afml` opened.

### Other files

- Chapter openers: `portfolio-construction-risk` (overview added, legacy reference removed, new topic file input first), `systematic-equities` (new), `research-engineering-validation`, `execution-trading-costs`, `execution-market-making`.
- Pathway notes: new `portfolio-construction-risk.md` and `equity-long-short-construction.md`; `model-governance-controls`, `execution-trading-costs`, `hft-market-design`, `market-structure-execution-quality`, `portfolio-construction`.
- `notes/log.md`: coverage rows, the `s7-narang` progress cell, two open questions; `notes/source-review-index.md`: status, index, next batch, map; `compendium/README.md`: order paragraph.

### Build

`latexmk -g -pdf compendium.tex`: exit 0; 225 pages (223 before); no LaTeX warnings; the one `page.i` warning; 0 overfull and 25 underfull boxes, all after the start of the legacy part in the log. The underfull count fell from 26 because one was in the removed legacy portfolio chapter. During the topic review two overfull boxes (an artefact file name in *Further reading*, and section headings with long paths in the overview artefact) and a stray "Figure 1: \*" from `\caption*` without the caption package were fixed. Rendered and inspected: PDF p. 10 (production lifecycle), p. 16 (systematic-equities opener and signal combination), pp. 18–20 (overview opener, redrawn figure, alpha taxonomy and specification), p. 25 (the risk models review follow-up), p. 70 (`def:hft-strategies`), p. 93 (`def:order-exposure-decisions`), and the three artefacts, including the original diagram's rendering. Tests: 14 passed.

### Independent review

Before committing, a separate review compared every changed claim, quotation, locator and calculation with the source text layers and the legal texts. It confirmed the arithmetic, all 23 cross-referenced labels and both legal quotations, and found four overstatements and seven judgement calls, all fixed in this batch:
- "most trend followers win on fewer than 40 percent" → his "often less than 40 percent" (pp. 60–61);
- "no evidence for the classes" → two papers for value/yield (Fama–French, Ball) and his reading of volume research (pp. 37–40);
- macroscopic alpha "converging to zero" → the *chances* of an individual finding it (AFML p. 6);
- "larger quants use order-book signals" (legacy, not Narang) → his micro price and footprint passages (pp. 130, 133–134);
- FINRA 5270: "inferring a hidden order is not that information" marked as interpretation, with the undefined term and the rule's note on Rules 2010 and 5320;
- Narang's front-running argument limited to "most" HFTs, with his contractual-market-maker exception (p. 312);
- the CEA clause's scope given in its own words, "futures and swaps" marked as gloss;
- order types, not fees and priority, are what he says change often (pp. 134–135);
- "inert and useless" applies to data only (p. 19);
- the non-contiguous machine-learning quotation split and the rebuttal marked as interpretation;
- "worth sizing on only if calibrated" softened; "largely" restored; the CVX view and the carry context restated.

### For review

- The routing of signal combination and the production chain away from the map's overview, and the new `systematic-equities` chapter.
- Keeping the cancel-and-replace and shark passages as historical descriptions with limited legal support, rather than as techniques or stubs only.
- The redrawn diagram's return arrow, and the alpha taxonomy's correction from five classes to eight.

## systematic-investing architecture review follow-up: hidden-order leakage, lifecycle timing and currency fields, 15 October 2026

Narrow corrections to systematic-investing architecture review, run before derivatives and hedging review; the systematic-investing architecture review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub, artefact or count changed (583 legacy blocks; 108 entries).

- **Hidden orders, `def:order-exposure-decisions`.** "Hidden orders reveal nothing" overstated Narang, who says a hidden order "provides no information to the market" (p. 134), meaning no displayed interest. The entry now separates undisplayed pre-trade interest from information inferred through executions and probing, citing the SEC's 2010 release on immediate-or-cancel "pinging" to find undisplayed liquidity (p. 47, n. 69) and linking `def:order-anticipation`; hiding lowers, not removes, leakage.
- **Lifecycle timing, `meth:strategy-production-lifecycle`.** "Embargo and paper trading are forms of validation before production" contradicted López de Prado, whose portfolio-oversight stages follow deployment (AFML pp. 8–9). They are now validation before live-capital trading (graduation).
- **Currency fields.** `def:hft-strategies` no longer says no current rule was checked: FINRA Rule 5270 (as displayed 15 October 2026) is recorded as the one current rule checked, with historical figures dated as given. `def:order-exposure-decisions` dates the U.S. Code passage to its 2024 edition and Narang's venue details to 2024, with no current venue rule checked. `def:automated-trading-architecture` adds Narang's 2024 account, with his latency figures undated.
- **Notes and index.** The `execution-trading-costs`, `model-governance-controls` and `hft-market-design` notes record the changes; the systematic-investing architecture review index row gives `2642451`.

## derivatives and hedging review: derivatives, hedging, rates and time value (Hull notes and the time-value file), 16 October 2026

A three-file batch closing two legacy chapters, run after the systematic-investing architecture review follow-up above. Migration and source checking, not study; no checkpoint was attempted. Hull's book is the first reading of the `volatility-options` overview and the GIPS standards a reading of `performance-manager-evaluation`; both were read only where the blocks needed them.

### Scope

Counted by script against the committed originals (`e`, the starting commit `2642451`):

| File | Blocks | `\item` (excl. `\itemsep`) | Other content |
|---|---|---|---|
| `volatility-options/basic.tex` | 8: *derivative*, *spot/forward contract*, *call/put option*, *American/European option*, *credit spread*, *Forward Rates*, *FRA*, *Duration* (all `definition`) | 0 in blocks, 3 outside (OTC reforms) | introduction and prose on exchanges, OTC, futures, convergence (figure `convgspotfuture.png`), clearing house, OTC markets, rate types, compounding, zero/bond/par yields, forward and instantaneous forward rates, FRA value, duration, modified duration, convexity, term-structure theories; 13 display equations |
| `volatility-options/fwdfut.tex` | 5: *Basic Principles of Futures Hedging* (with a table), *basis*, *basis risk*, *Cross Hedging*, *Hedge Ratio* (all `definition`) | 2 in blocks, 27 outside | pricing assumptions, arbitrage lists, income, yield, forward value, index arbitrage, interest rate parity, commodities, convenience yield, cost of carry, imperfect hedges, hedge-ratio derivation (figure `hedgeratio.png`), contract numbers, daily settlement, tailing, index futures, beta change, stack and roll, day counts, T-bill and T-bond quotes; 20 display equations |
| `rates-credit-mortgages/01_tvm.tex` | 2: *Time Value of Money Formulas*, *Return Metrics* (`definition`, each a table) | 0 | none |
| **Total** | **15** | **32** (2 inside, 30 outside; substring counts give 43) | 33 display equations, 3 tables, 2 figures |

Also accounted for: the chapter wrappers `legacy/volatility-options/section.tex` (citing Hull and inputting both files) and `legacy/rates-credit-mortgages/section.tex`, their two lines in `legacy/part.tex`, the three map rows and the two PNGs. All were removed from the compendium after preservation; the two legacy folders are gone. Other legacy chapters, earlier artefacts, deferred assignments, `house.tex` and the guide pin (`343d145`) are unchanged.

### Ownership and dispositions

Routed block by block on guide outcomes. **Routing exceptions** against the map (`basic.tex` → `volatility-options`; `fwdfut.tex` → `rates-credit-mortgages`, `commodity-hedging`; `01_tvm.tex` → `rates-credit-mortgages`, `performance-manager-evaluation`):
- the rates material of `basic.tex` (credit spread, forward rates, FRA, duration, and the prose on rate types, compounding, yields, clearing) goes to `rates-credit-mortgages` ("connect a rate quote or bond position to its curve … collateral and hedge-contract assumptions");
- its exchange-clearing prose is merged into `mech:futures-margin-settlement` (`futures-execution`) as a generic account beside the CME rules;
- the pricing half of `fwdfut.tex` (cost of carry) goes to the `volatility-options` overview, whose first reading is Hull, rather than to its map candidates; its day-count and quotation prose goes to `rates-credit-mortgages`.
Rejected: `curve-term-structure` for forward rates and term-structure theories (no curve building or term-premium estimation in the blocks; evidence stubbed with it as home), `rate-derivatives` for the FRA (no model calibration), `energy-commodities` and `commodity-storage-curves` for convenience yield (stubbed), `money-markets-repo-lending` for repo rates (a definition only, cross-referenced).

| # | Legacy block | Owner | Destination | Hull 11th Global ed. / other source | Disposition |
|---|---|---|---|---|---|
| B1 | *derivative* | `volatility-options` | `def:derivative-contracts` (new) | chap. 1, p. 23 | Rewritten |
| B2 | *spot/forward contract* | `volatility-options` | `def:derivative-contracts` | sec. 1.3, pp. 28–30 | Rewritten, payoffs kept |
| B3 | *call/put option* | `volatility-options` | `def:derivative-contracts` | sec. 1.5, p. 31 | **Corrected**: the legacy reversed the rights |
| B4 | *American/European option* | `volatility-options` | `def:derivative-contracts` | p. 31 | Rewritten |
| B5 | *credit spread* | `rates-credit-mortgages` | `def:interest-rate-measures` (new) | sec. 4.1, p. 98 | Rewritten ("interest rate" → over a risk-free rate) |
| B6 | *Forward Rates* | `rates-credit-mortgages` | `mod:forward-rates-fra` (new) | sec. 4.8, pp. 109–110 | Rewritten |
| B7 | *FRA* | `rates-credit-mortgages` | `mod:forward-rates-fra` | sec. 4.9, pp. 110–112 | Rewritten; value **corrected** to a present value |
| B8 | *Duration* | `rates-credit-mortgages` | `mod:duration-convexity` (new) | secs. 4.10–4.11, pp. 112–117 | Rewritten; approximations marked |
| B9 | *Basic Principles of Futures Hedging* (table) | `commodity-hedging` | `def:futures-hedge-basis` (new) | sec. 3.1, pp. 70–72 | Rewritten; the long-hedge column noted as not Hull's |
| B10 | *basis* | `commodity-hedging` | `def:futures-hedge-basis` | sec. 3.3, p. 76 | Rewritten; sign convention stated |
| B11 | *basis risk* | `commodity-hedging` | `def:futures-hedge-basis` | p. 77 | Rewritten; long-hedge case and cross-hedge components added |
| B12 | *Cross Hedging* | `commodity-hedging` | `def:futures-hedge-basis` | sec. 3.4, p. 79 | Rewritten |
| B13 | *Hedge Ratio* | `commodity-hedging` | `mod:minimum-variance-hedge-ratio` (new) | sec. 3.4, pp. 79–83 | Rewritten; derivation added |
| B14 | *Time Value of Money Formulas* | `rates-credit-mortgages` | `def:interest-rate-measures` | none (derived here) | Rewritten; "Expected Annual Rate" corrected to effective |
| B15 | *Return Metrics* | `performance-manager-evaluation` | `def:return-measures` (new) | GIPS 2020 | Rewritten; TWR root and real-return "risk" factor corrected |

**Subclaims outside and inside the blocks.**

| Where | Legacy claim | Disposition |
|---|---|---|
| basic intro | Derivatives market much larger than stocks by underlying assets; hedging, speculation, arbitrage; risk transfer | Kept as Hull's (p. 23); qualified: notional (\$558.5 tn OTC) is not value (\$11.6 tn), pp. 27–28 |
| basic | Exchanges trade standardised contracts; clearing house "takes care of credit risk" by margin | Rewritten (p. 25); qualified: margin reduces, does not remove, credit risk (`mech:otc-clearing-collateral`) |
| basic, items i–iii | OTC reforms: SEFs, CCP clearing, reporting | Kept as Hull's account with his qualifiers restored ("whenever possible", "most parts of the world", p. 26); primary rules unchecked → stub `rule:otc-derivatives-reforms` |
| basic | Forward payoffs $S_T-K$, $K-S_T$ | Rewritten (p. 29); option payoff and profit with premium added (p. 32, examples recomputed) |
| basic | Futures on exchange; most closed out | Rewritten (pp. 30, 47–48) |
| basic | Delivery notice, grade, size, place, months, last trading; price limits "trading ceases" | Rewritten (pp. 48–50); limits contract-specific, exchanges can change them, controversial |
| basic + figure | Convergence by arbitrage | Rewritten (pp. 50–51) with the deliverability condition as interpretation; figure redrawn in TikZ, original PNG (a reproduction of Hull's Figure 2.1) preserved |
| basic | Margin accounts, daily settlement, variation, maintenance, margin call, withdrawal, brokers pay interest; minimum levels by clearing house | Merged into `mech:futures-margin-settlement` as Hull's generic account (pp. 51–54): "most brokers"; maintenance about 75%; not any clearing house's rules |
| basic | Clearing house members: net basis, maintenance = initial, guaranty fund | Merged (pp. 53–54), with Hull's "about 99%" sizing |
| basic | OTC CCPs, novation-like substitution, CCP takes credit risk; bilateral ISDA/CSA; 2016 margin rules | `mech:otc-clearing-collateral` (pp. 54–57; PFMI para. 1.13); scope of the 2016 rules from Hull's footnote; CCPs mitigate, not eliminate |
| basic | Treasury rates risk-free "as there is no chance" of default | Qualified: "usually assumed" (p. 99), default in own currency only; not the derivatives discount rate (p. 101) |
| basic | Fed funds; EFFR as weighted average of brokered rates; Fed may intervene | **Corrected** with the New York Fed: volume-weighted median of FR 2420 transactions since 1 March 2016 (`exp-sofr-data`); Hull's p. 99 description superseded |
| basic | Repo rates; overnight and term repo | Rewritten (p. 99); SOFR methodology added (`exp-sofr-data`) |
| basic | Compounding $A(1+R/m)^{mn}$, $Ae^R$, "equivalent annual interest rate" | Rewritten (pp. 102–104) with conversions |
| basic | Spot rate, bond price, bond yield, par yield | Rewritten (pp. 104–106); examples recomputed |
| basic | $R_F$ formulas; instantaneous forward | Rewritten (pp. 109–110); finite-difference check |
| basic | FRA value $\tau(R_K-R_F)L$ | **Corrected**: present value; settlement timing; single-curve caveat; SOFR backward-looking |
| basic | Duration definition and relations; modified duration; convexity Taylor | Rewritten with approximation signs; ±200 bp checks |
| basic | Parallel-shift assumption for portfolios | Kept (p. 115), with yield change against curve shift |
| basic | Expectations, segmentation, liquidity-preference theories; "forward rates are greater" | Kept as Hull's conjectures (pp. 117–119); "are" qualified; evidence stubbed (`ev:term-premia`, home `curve-term-structure`) |
| fwdfut, items i–iv | Four assumptions | Rewritten (p. 126): needed for some participants only |
| fwdfut, numbered lists (no-short-sale arbitrage, yield strategy, commodity arbitrage) | Arbitrage strategies | Rewritten (pp. 127–142); the commodity reverse arbitrage limited to investment assets; consumption assets give only an upper bound |
| fwdfut | Income $I$, yield $q$, forward value $f$ "close to zero" | Rewritten (pp. 130–133); $K$ set so $f=0$ at inception |
| fwdfut | Index arbitrage | Rewritten (pp. 135–137), with October 1987 failure |
| fwdfut | Currency parity with $S_0$ as "local in foreign" | **Corrected** to Hull's quote direction (p. 138) |
| fwdfut | Commodities, storage $U$, $u$, convenience yield, cost of carry items i–iv | Rewritten (pp. 141–144) |
| fwdfut, items in B9 | Short and long hedges | Rewritten (pp. 71–72) |
| fwdfut, 1–3 | Causes of imperfect hedges | Kept (pp. 75–76) |
| fwdfut | Hedge-ratio derivation, $h^*$, figure | Rewritten with the entry's own variance derivation; figure redrawn from Hull's Table 3.2 data; original PNG (a reproduction of Hull's Figure 3.3) preserved |
| fwdfut | Hedge effectiveness $=R^2=\rho^2$ | Kept (p. 81), qualified as in-sample |
| fwdfut | $N^*$, daily-settlement versions | Rewritten (pp. 81–83); price-change and return regressions kept apart |
| fwdfut | Tailing $N^*/(1+0.01r)$ | Qualified: one year at simple rate only (Hull's 1.05 example, p. 83) |
| fwdfut | Index futures, CAPM beta, changing beta | Rewritten (pp. 85–88); Hull's table assumptions noted |
| fwdfut | Reasons for index hedging | Kept as motivations (pp. 87–88), not evidence |
| fwdfut | Stack and roll | Rewritten (pp. 89–90), with Metallgesellschaft's liquidity mismatch |
| fwdfut, items i–iii | U.S. day counts | `conv:us-rate-quotation` (pp. 152–153) |
| fwdfut | T-bill quote, T-bond 32nds, clean/dirty | `conv:us-rate-quotation` (p. 154); examples recomputed |
| tvm table | EAR, continuous FV, PV, ordinary annuity, annuity due, perpetuity | Derived here (no source); "Expected" → effective; timing, $r\to0$ and perpetuity limits stated |
| tvm table | IRR, MWR | `def:return-measures` (GIPS p. 78); existence and multiple roots added |
| tvm table | TWR $\sqrt[1/n]{\cdot}$ "geometric mean" | **Corrected**: malformed root; cumulative, geometric mean and annualised kept apart; split at external cash flows (GIPS 2.A.24) |
| tvm table | Annualised, log return | Kept, derived |
| tvm table | Gross, net, pre-tax, after-tax | Gross and net from GIPS glossary (pp. 76, 78); tax measures not checked |
| tvm table | Real return with $(1+r_{\mathrm{Risk}})$ factor | **Corrected**: $(1+r_{\mathrm{nom}})/(1+\pi)-1$; the risk factor has no basis |
| tvm table | Leveraged return | Kept, derived with its funding assumptions |

No claim was deleted outright; every not-adopted claim stays in the artefacts.

**Existing entries checked.** `mech:futures-margin-settlement` (merged into, generic account kept apart from CME rules); `def:arbitrage` and `res:synthetic-short-put-call` (cross-referenced; parity and carrying costs not repeated); `meth:relative-performance-evaluation` (IRR and holding-period return already there; cross-referenced); `def:fixed-income-market-structure`, `mech:securities-lending-short-sale`, `def:securities-lending-fee-rebate`, `def:common-investor-contagion`, `mod:factor-risk-model` (cross-referenced). No duplication was found.

### Sources, 2026-10-15/16

- **Hull** (`s7-hulloptions`), *Options, Futures, and Other Derivatives*, 11th Global edition, Pearson 2022, ISBN 9781292410654 (copyright page checked; matches the catalogue's selected edition), local PDF, 881 pages, text layer through PDFKit, printed page = PDF page − 1 (PDF 24 is p. 23, chapter 1's opening). Read: chap. 1 pp. 23–33; chap. 2 pp. 46–57 and 62–65; chap. 3 pp. 70–90; chap. 4 pp. 98–119; chap. 5 pp. 124–145; chap. 6 pp. 152–155. Figures 2.1 (p. 51) and 3.3 (p. 81) viewed as page images: the two legacy PNGs reproduce them. Author errata not checked.
- **New York Fed**, *Additional Information about Reference Rates* (`exp-sofr-data`) and the EFFR and SOFR pages, retrieved 2026-10-15: EFFR and OBFR methodology (volume-weighted median, FR 2420, change of 1 March 2016) and SOFR's scope.
- **GIPS standards for firms, 2020 edition** (`wide-gips-2020`), official PDF (146 pages) downloaded 2026-10-15, printed page = PDF page − 18: provisions 1.A.35 (pp. 5–6), 2.A.23–2.A.30 (pp. 11–13) and the glossary entries for external cash flow (p. 75), gross-of-fees (p. 76), money-weighted and net-of-fees returns (p. 78) and time-weighted return (p. 83).
- **CPSS–IOSCO PFMI** (`exp-pfmi`), para. 1.13, p. 9, as read in transaction-cost models review.
- **Not read:** the readings of the four owning pathways beyond those above; the Dodd–Frank, swap-reporting and uncleared-margin rule texts; Hull chaps. 6.2–6.5 and 7 onward; any source for the legacy time-value file, whose origin is not recorded.

### Numerical checks

Independent of the formulas being checked, in a scratch script (numpy/scipy, not kept in the repository):
- **Hedge objective**: the sample variance of $\Delta S-h\Delta F$ on Hull's Table 3.2 data minimised numerically gives $h^*=0.7777$, equal to the OLS slope and to $\rho\sigma_S/\sigma_F$; variance retained 13.81% (removed 86.19% $=\rho^2$); at $h=1$, 20.86%; $N^*=37.03$; one-day $N^*=32.23$; tailing factor $1/1.05=0.9524$ against $1/(1+0.05\times0.5)$ for six months.
- **Discounted cash flows**: Hull's forward prices (40.50, 886.60, 51.14, 25.77), forward value 2.17, parity 0.7206, storage 484.63, index 1,313.07; bond 98.39, yield 6.76%, par yield 6.873%; forward 3→4 6.2%; instantaneous forward by finite difference of $-\ln P$ equal to $R+TR'$.
- **FRA**: Example 4.3 gives \$369,247 (Hull prints \$369,200); sign from the receive-fixed side.
- **Duration**: $B=94.213$, $D=2.653$, $C=7.570$; exact against approximate at $\Delta y=+0.001$, $\pm0.02$; semiannual $D^*=2.499$, exact 93.978.
- **Annuity limits**: brute-force sums equal the closed forms; factor → 10 as $r\to0$; perpetuity partial sums converge to $A/r$.
- **Returns**: TWR −1.00% against MWR −3.71% in a contribution example; cumulative 3.95%, geometric mean 1.30%; annualised 7.42%; IRR roots 10% and 40%; a no-root case (maximum NPV −0.75); real 4.854% against $n-\pi=5\%$; leveraged 13%.
- **Quotes**: 2.6957, 2.7111, T-bill quote 4.00, \$120,156.25, accrued 1.64; gold margin balance \$7,980 on day 7.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-hulloptions` | as listed | Textbook account as of 2021; U.S.-centred conventions and examples; the legacy notes' edition is unknown |
| `exp-sofr-data` | methodology page | As published 15 October 2026 |
| `wide-gips-2020` | definitions and provisions listed | Presentation standard, not a full methodology; after-tax returns not covered |
| Reform rules, term-premium and hedging evidence | none | Stubs |

The ten new entries and the merged passage are *partly checked*, *draft*; **human review is outstanding**.

### Preservation

New artefacts (earlier ones unchanged): `notes/artefacts/volatility-options/hull-basics.tex`, `hull-forwards-futures.tex`, `legacy-wrappers.tex` (display-only wrappers and `part.tex` lines, with both figures rendered) and `legacy-section-original.tex`; `notes/artefacts/rates-credit-mortgages/time-value.tex` and `legacy-section-original.tex`. The PNGs were moved, byte-identical (SHA-256 prefixes `9d6e55b4…`, `ba04bf8f…`), to `notes/artefacts/volatility-options/legacy/volatility-options/figures/`, the same relative path the originals use, so the verbatim bodies compile unedited. A script compared everything with `git show HEAD:…`:
- each body below its migrate-to line appears exactly once; both wrapper copies are byte-identical;
- all 15 blocks appear verbatim once each, in order; every prose segment outside the blocks appears;
- `\item` commands, matched as `\item` not followed by a letter: 3, 29 and 0 (32; 2 inside blocks, 30 outside), equal in originals and artefacts; substring counts give 4, 39 and 0;
- `\begin`/`\end` sequences identical (46, 76 and 8 commands), covering all 33 display equations, 3 tables and 2 figures.

All four artefacts compile alone without warnings or overfull boxes (4, 5, 1 and 2 pages); the two Hull files carry 15 and 10 underfull boxes from their own `\\` line breaks, which are the legacy boxes removed from the compendium. Their tables, equations and figures were inspected by page image, including the malformed TWR root, preserved as committed.

### Counts

`check_compendium.py --check`, 0 problems: 583 → 568 legacy blocks = 523 shared + 16 single-candidate + 29 assigned. Entries 108 → 118 (definitions 38 → 42, models 13 → 16, results 17 → 18, conventions 2 → 3, mechanisms 8 → 9). New pathway notes: `volatility-options` (2 entries, 2 stubs), `rates-credit-mortgages` (5, 3), `commodity-hedging` (2, 3); `performance-manager-evaluation` 1 → 2 entries, 0 → 1 stub; `futures-execution` 4/1 unchanged in count, its entry extended. New reading note `s7-hulloptions`. No new `front/sources.tex` keys (all sources are catalogue keys).

### Other files

- New chapters `volatility-options/`, `rates-credit-mortgages/` and `energy-commodities/`, with their openers and two TikZ figures; `portfolio-construction-risk` and `execution-trading-costs` openers updated.
- Pathway notes as above; `notes/log.md` coverage rows, a Hull reading row and two open questions; `notes/source-review-index.md` status, index, next batch and map; `compendium/README.md` order paragraph.

### Build

`latexmk -g -pdf compendium.tex` exits 0: 228 pages (225 before); no LaTeX warnings; 0 overfull and 0 underfull boxes (25 underfull before, all in the removed legacy chapters); the inherited `page.i` duplicate-destination warning. `check_compendium.py --check` 0 problems; `python3 -m pytest -q tools` 14 passed. Pages inspected as images: the rates chapter (forward rates, FRA, duration), the options entry, the return measures and the hedge-variance figure, after the review fixes as well.

### Independent review

An independent subagent re-read the cited Hull pages (chaps. 1–6), the GIPS, PFMI and New York Fed passages and Narang p. 134, recomputed every number in the entries and checked every cross-reference label. All quotes, locators and numbers not listed below were confirmed. Fixed:
- **Definite errors.** The hedge-ratio minimum was stated as $dV/dh=0$; now $d\operatorname{Var}V(h)/dh=0$. A locator "pp. 82" → p. 82. The gold margin example cited only Table 2.1 (p. 52); the loss and the call are in the text on pp. 51 and 53. The legacy "value is close to zero" at a forward's inception is Hull's own sentence (p. 133), not an omission; the entry now says the legacy dropped Hull's next step, $K$ set so $f=0$. The receive-fixed FRA cash flow $\tau(R_K-R_M)L$ is now marked as derived from Hull's definitions (pp. 111–112), and the Pitfalls record that Hull's p. 111 example reverses the payment direction (Party A, receiving 3% fixed with LIBOR at 3.5%, pays \$125,000); his p. 112 value formula is correct; errata not checked.
- **Qualifications.** Yield change against a parallel zero-curve shift: approximately equal, exactly only for a flat curve (0.9996 on Hull's Table 4.2 bond, recomputed). EFFR: the methodology changed with the rate for 1 March 2016 and is now a volume-weighted median. The annuity limits are the future-value factor's. LTCM (Business Snapshot 2.2): collateral on both legs and high leverage forced close-outs, not "unable to meet calls". Term-structure theories: Hull calls two conjectures and finds liquidity preference "most appealing". GIPS 2.A.23–2.A.24: sub-period returns at large cash flows apply if daily returns are not calculated, with exceptions for private-market investment portfolios. SOFR's 360-day year cited to Hull p. 100. "DV01" dropped from an index that never defined it.
- **systematic-investing architecture review wording.** In `def:order-exposure-decisions`, words after Narang's quotation had read as his; "in Narang's words" now sits with the quotation and the gloss (size and price not displayed before it trades) is the entry's.
Not changed: Hull's "tranasaction" typo (p. 23) is silently corrected in the quotation.

### For review

- Splitting the Hull notes across four pathways against the map, and the cost-of-carry entry under the options overview.
- Using the New York Fed's methodology to correct Hull's EFFR description, and treating Hull's reform list as his account.
- The time-value identities written as derived, unsourced material.

## derivatives and hedging review follow-up: cross-hedge components, yield-shift condition, return horizons and GIPS annualisation, 16 October 2026

Narrow corrections to derivatives and hedging review (`9fbd551`), run before financial data and labels review; the derivatives and hedging review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub or count changed (568 legacy blocks; 118 entries).

- **Cross hedging, `def:futures-hedge-basis`.** The entry gave $F_1+(S_2^*-F_2)+(S_2-S_2^*)$ without naming its parts and cited pp. 77 and 79. Hull calls the two last terms "the two components of the basis": $S_2^*-F_2$ the basis that would exist if the hedged asset were the futures' underlying, $S_2-S_2^*$ "the basis arising from the difference between the two assets" (p. 77). Both that expression and $S_2+F_1-F_2=F_1+b_2$ are one-to-one hedges: Hull's examples use a hedge ratio of 1.0, "natural" for the same asset and "not always optimal" in a cross hedge (p. 79). Added, as derived: with hedge ratio $h$ (futures units per unit of exposure, taken in the offsetting direction) the effective price is $S_2+h(F_1-F_2)$, equal to $F_1+b_2$ at $h=1$; $h$ carries any unit conversion between the two assets. The locator of "Cross hedging uses a futures contract on a different asset", which had been p. 78 (Hull's *Choice of Contract*), is now p. 77 and sec. 3.4, p. 79; and the units remark now notes that Hull's jet-fuel and heating-oil example needs no conversion (both in gallons).
- **Returns, `def:return-measures`.** The example compared a cumulative TWR ($-1.0$ percent over two periods) with a per-sub-period IRR ($-3.71$ percent). Recomputed independently: the IRR solving $-100-100(1+x)^{-1}+189(1+x)^{-2}=0$ is $-3.7126$ percent per equal sub-period, $-7.2874$ percent compounded over both; the TWR's geometric mean is $-0.5013$ percent per sub-period. The entry now labels units and compares like with like.
- **GIPS annualisation, same entry.** "Money-weighted returns must be annualised since-inception returns" stated 2.A.29 without the presentation rules. Read in the GIPS 2020 PDF (printed page = PDF page − 18): 2.A.12, "Returns for periods of less than one year must not be annualized" (p. 9); 2.A.29.a, "Calculate annualized since-inception money-weighted returns" (p. 12); 5.A.1.a–b, the annualised since-inception MWR through the most recent annual period end and, "when the composite has a track record that is less than a full year, the non-annualized composite since-inception money-weighted return through the initial annual period end" (p. 33). The entry now separates the mathematical annualisation $(1+R)^{365/d}-1$ from what a firm may present, and marks its 200-day example as one GIPS would not allow a firm to present. The advertising provisions were not read.
- **Yield against zero-curve shift, `mod:duration-convexity`.** derivatives and hedging review's review fix said the two coincide "exactly only when the zero curve is flat". Flatness is sufficient, not necessary. Derived and checked: the yield moves by exactly $\Delta$ for every parallel shift $\Delta$ if and only if the zero rates at all the bond's payment dates equal its yield; a zero-coupon bond ($y=R(T)$) moves one for one on any curve, and a two-payment bond on a curve level at its payment dates does too. Counterexamples: Hull's Table 4.2 bond moves 0.9996$\Delta$; a 10-year 5 percent annual-coupon bond on a curve rising 40 bp a year from 1.4 percent moves 0.986$\Delta$, with yield duration 8.13 against zero-curve duration 8.01 years. The script is kept as `notes/artefacts/rates-credit-mortgages/yield-shift-check.py` (numpy, scipy).
- **Notes and index.** `commodity-hedging`, `rates-credit-mortgages` and `performance-manager-evaluation` notes, the `s7-hulloptions` reading note and `log.md` record the changes; the derivatives and hedging review index row gives `9fbd551`.

## financial data and labels review: the AFML data cluster (taxonomy, data structures, labels, sample weights, fractional differentiation), 16 October 2026

A five-file batch of 36 blocks closing the legacy `ml-alternative-data` chapter, run after the derivatives and hedging review follow-up above. Migration and source checking, not study; no checkpoint was attempted. López de Prado (`alpha-afml`) is a required reading of `statistical-learning-foundations` and was read only in chaps. 2–5; Velu, Hardy and Nehren (`s3-velu`) is no pathway's reading. Two internal review groups were used: A, taxonomy and data structures (17 blocks); B, labels, sample weights and fractional differentiation (19 blocks).

### Scope

Counted by script against the committed originals (starting commit `9fbd551`):

| File | Blocks | `\item` (excl. `\itemsep`) | Other content |
|---|---|---|---|
| `ml-alternative-data/data/taxonomy.tex` | 9: four `remark` (Fundamental, Market, Analytics, Alternative Data Characteristics), five `definition` (Reference Data, Market Data Feed, Binned Data, Granular Intraday Microstructure Activity, Fundamental Data and Other Data) | 83, all inside blocks | opening sentence; a four-column table (AFML Table 2.1) |
| `ml-alternative-data/data/datastruct.tex` | 8: two `remark` (Standard Bars, Information-Driven Bars), one `definition` (ETF Trick), five `method` (ETF Trick, PCA allocation, Single Futures Roll, Sampling for Reduction, CUSUM filter) | 21, all inside | figure `standardbars.png`; one prose paragraph before *Sampling for Reduction*; 25 display environments |
| `ml-alternative-data/data/datalabel.tex` | 6: three `method` (Fixed-Time Horizon, Triple-Barrier, Meta-Labelling), three `remark` (two sets of limitations, configurations) | 24, all inside | figure `metalabel.tikz`; 1 display |
| `ml-alternative-data/data/datasampleweights.tex` | 9: two `remark` (Overlapping Outcomes, IID and Oversampling), seven `method` (Estimating Uniqueness, Average Uniqueness, Bootstrap Redundancy, Sequential Bootstrap, Return Attribution, Time Decay, Class Weighting) | 19, all inside | opening sentence; 2 displays |
| `ml-alternative-data/data/fracdifffeat.tex` | 4: `definition` (BackShift Operator), `remark` (Properties), two `method` (Expanding, Fixed-Width Window) | 3, all inside | opening prose; figure with two PNGs; 7 displays |
| **Total** | **36** | **150** (all inside blocks; substring counts give 188) | 35 display environments, 1 table, 3 figures with 4 assets |

Also accounted for: `data/dataoverview.tex` (the wrapper inputting the five files, no blocks), the chapter's `section.tex`, its line in `legacy/part.tex`, the five map rows and the four figure assets. All were removed from the compendium after preservation; the legacy folder is gone. The other legacy chapters, earlier artefacts, deferred assignments, `house.tex` and the guide pin (`343d145`) are unchanged.

### Provenance

- `datastruct.tex`, `datalabel.tex` (except as below), `datasampleweights.tex` and `fracdifffeat.tex`: López de Prado chaps. 2–5, close paraphrase with the source's own slips copied (below).
- `taxonomy.tex`: its table and four remarks follow López de Prado sec. 2.2 (pp. 23–25); its five definitions follow Velu, Hardy and Nehren chap. 1, sec. 1.4 (pp. 26–44), not named in the file. The "Binned Data" definition holds Velu's *Daily Statistics* (pp. 39–40); his *Binned Data* is p. 42.
- `datalabel.tex` meta-labelling: the steps (high-recall primary model, threshold possibly from ROC curves, concatenated features and predictions, positive "only where both are true") follow the Hudson & Thames blog "Meta Labeling (A Toy Example)" (`ht-meta-labeling-toy`, read 2026-10-16); `metalabel.tikz` follows its architecture. The five feature groups beyond the concatenation and the three "Limitations of Meta-Labelling" were found in neither source nor by web search; they are not adopted.
- Figures: `standardbars.png` reproduces AFML Figure 2.1 (p. 28); `fracdiffexpandwindow.png` and `fracdifffixedwidthwind.png` reproduce AFML Figures 5.3(b) (p. 81) and 5.4 (p. 83); none was credited. They are kept only in the artefact, with attribution there; no entry uses them.

### Ownership and dispositions

Routed block by block on guide outcomes. `statistical-learning-foundations` ("fit and tune ... estimate out-of-sample error with a validation scheme suited to dependent, non-stationary data"; `alpha-afml` is its reading for "finance-specific labelling") owns the bars, sampling, labels, weights and fractional differencing. `financial-ml-evaluation` ("time-valid inputs") owns the time-validity consequences, as one pitfall. `alternative-data-sources` ("assess an alternative dataset by its coverage, timing and incremental information") owns the four data types. **Routing exceptions** against the map (all five files: `statistical-learning-foundations`, `financial-ml-evaluation`, `alternative-data-sources`): the reference-data, market-data-feed, binned-data and intraday blocks go to `point-in-time-data` ("a research panel whose every field is available at decision time, with documented vintages, corrections and survivorship controls"), as `data` entries in a new topic file of `research-engineering-validation/`; the PCA allocation block goes to `portfolio-construction` (a risk allocation across principal components), appended to its portfolio-construction-models file. Rejected: the section overview `ml-alternative-data` for the taxonomy (its outcome is a filing-text test); `market-structure-execution-quality` and `lob-deep-learning` for the market-data levels (noted for review in the pathway note).

| # | Legacy block | Owner | Destination | Source | Disposition |
|---|---|---|---|---|---|
| T1 | *Fundamental Data Characteristics* | `alternative-data-sources` | `def:financial-data-types` (new) | AFML sec. 2.2.1, pp. 23–24 | Rewritten; Bloomberg-specific lag restored, backfill and reinstatement defined |
| T2 | *Market Data Characteristics* | `alternative-data-sources` | `def:financial-data-types` | sec. 2.2.2, pp. 24–25 | Rewritten; "over 10TB" and its "appealing" context restored, marked unsourced |
| T3 | *Analytics Data Characteristics* | `alternative-data-sources` | `def:financial-data-types` | sec. 2.2.3, p. 25 | Rewritten; crowding point added |
| T4 | *Alternative Data Characteristics* | `alternative-data-sources` | `def:financial-data-types` | sec. 2.2.4, p. 25 (Kolanovic–Krishnamachari split) | Rewritten; "annoys your data infrastructure team" marked opinion, in context |
| T5 | *Reference Data* | `point-in-time-data` | `data:trading-reference-data` (new) | Velu sec. 1.4.1, pp. 26–35 | Rewritten; dividend conflation **corrected**; rule histories restored |
| T6 | *Market Data Feed* | `point-in-time-data` | `data:market-data-levels` (new) | Velu sec. 1.4.2, pp. 35–39, Table 1.10 | Rewritten; "divide by 1000" **corrected** to 10000; consolidation and latency restored |
| T7 | *Binned Data* | `point-in-time-data` | `data:derived-market-statistics` (new) | Velu sec. 1.4.3, pp. 39–40 (Daily Statistics) | Rewritten; mislabelled heading **corrected** |
| T8 | *Granular Intraday Microstructure Activity* | `point-in-time-data` | `data:derived-market-statistics` | pp. 41–42 | Rewritten; reference-data caveat and binned-data limits added |
| T9 | *Fundamental Data and Other Data* | `alternative-data-sources` | `def:financial-data-types` | Velu sec. 1.4.4, pp. 42–44 | Rewritten; hedges ("might", "thought to be", "generally") restored; claims stubbed as evidence |
| D1 | *Standard Bars* | `statistical-learning-foundations` | `meth:activity-sampled-bars` (new) | AFML sec. 2.3.1, pp. 26–28 | Rewritten; dollar-bar robustness narrowed; distributional evidence qualified (Ané–Geman abstract read) |
| D2 | *Information-Driven Bars* | `statistical-learning-foundations` | `meth:information-driven-bars` (new) | sec. 2.3.2, pp. 29–32 | Rewritten; runs statistics and imbalance thresholds **corrected**; $b_0$ and causal EWMAs stated |
| D3 | *Multi-Product Series: ETF Trick* (definition) | `statistical-learning-foundations` | `meth:etf-trick` (new) | secs. 2.4–2.4.1, pp. 32–33 | Merged into the method entry |
| D4 | *ETF Trick* (method) | `statistical-learning-foundations` | `meth:etf-trick` | p. 34 | Rewritten; $o_{i,t+1}$ **corrected**; timing, positivity and cost limits added |
| D5 | *ETF Trick: Computation of Allocation Vector with PCA* | `portfolio-construction` | `mod:pca-risk-distribution-weights` (new) | sec. 2.4.2, pp. 35–36 | Rewritten; two formula slips **corrected**; eigenvalue and sign conditions added |
| D6 | *ETF Trick: Single Futures Roll* | `statistical-learning-foundations` | `meth:etf-trick` | sec. 2.4.3, pp. 36–37 | Rewritten; denominator **corrected** to the previous raw price; roll gaps added |
| D7 | *Sampling for Reduction* | `statistical-learning-foundations` | `meth:event-based-sampling` (new) | sec. 2.5.1, p. 38 | Rewritten |
| D8 | *Event-Based Sampling: CUSUM Filter* | `statistical-learning-foundations` | `meth:event-based-sampling` | sec. 2.5.2.1, pp. 38–40, Snippet 2.4 | Rewritten; zero condition and run condition **corrected**; sampling, reset and strict-inequality rules added |
| L1 | *Labelling with Fixed-Time Horizon Method* | `statistical-learning-foundations` | `meth:triple-barrier-labelling` (new) | sec. 3.2, p. 43 | Rewritten |
| L2 | *Limitations of Fixed-Time Horizon Method* | `statistical-learning-foundations` | `meth:triple-barrier-labelling` | p. 44, Snippet 3.1 | Rewritten; third limitation (path) added |
| L3 | *Labelling with Triple-Barrier Method* | `statistical-learning-foundations` | `meth:triple-barrier-labelling` | sec. 3.4, p. 45 | Rewritten; vertical-barrier preference, side and size, intrabar ties added |
| L4 | *Triple-Barrier Method Configurations* | `statistical-learning-foundations` | `meth:triple-barrier-labelling` | p. 46 | Rewritten; "physical", "loose", "immediate" corrected |
| L5 | *Meta-Labelling* | `statistical-learning-foundations` | `meth:meta-labelling` (new) | secs. 3.6–3.8, pp. 50–55 | Rewritten from AFML; the legacy steps attributed to Hudson & Thames; claims stated as claims; out-of-sample primary predictions added |
| L6 | *Limitations of Meta-Labelling* | `statistical-learning-foundations` | `meth:meta-labelling` (Pitfalls) | no source found | Not adopted; first item contradicts AFML p. 53; kept in the artefact |
| W1 | *Overlapping Outcomes* | `statistical-learning-foundations` | `def:label-concurrency-uniqueness` (new) | sec. 4.2, pp. 59–60 | Rewritten |
| W2 | *Estimating Uniqueness of Label* | `statistical-learning-foundations` | `def:label-concurrency-uniqueness` | sec. 4.3, p. 60 | Rewritten; $r_{t-1,t}$ **corrected** |
| W3 | *Average Uniqueness of Label* | `statistical-learning-foundations` | `def:label-concurrency-uniqueness` | sec. 4.4, pp. 61–62 | Rewritten; training-set condition restored |
| W4 | *IID and Oversampling* | `statistical-learning-foundations` | `meth:sequential-bootstrap` (new) | sec. 4.5, p. 62 | Rewritten; AFML's $e^{-K/I}$ **corrected** to $e^{-I/K}$, "overlapping" to non-overlapping |
| W5 | *Sampling with Bootstrap, Redundancy* | `statistical-learning-foundations` | `meth:sequential-bootstrap` | pp. 62–63 | Rewritten |
| W6 | *Sequential Bootstrap* | `statistical-learning-foundations` | `meth:sequential-bootstrap` | secs. 4.5.1–4.5.4, pp. 63–68 | Rewritten; normaliser **corrected**; Monte Carlo evidence qualified |
| W7 | *Weighting Observations by Uniqueness and Absolute Return* | `statistical-learning-foundations` | `meth:sample-weights-attribution-decay` (new) | sec. 4.6, pp. 68–69 | Rewritten; factor $I$ and the weighting direction **corrected** |
| W8 | *Time Decay Weighting* | `statistical-learning-foundations` | `meth:sample-weights-attribution-decay` | sec. 4.7, pp. 70–71 | Rewritten; AFML's $d[1]$ and $cT$ slips **corrected** |
| W9 | *Class Weighting* | `statistical-learning-foundations` | `meth:sample-weights-attribution-decay` | sec. 4.8, pp. 71–72 | Rewritten |
| F1 | *BackShift Operator* | `statistical-learning-foundations` | `mod:fractional-differencing-weights` (new) | sec. 5.4, p. 77 | Rewritten |
| F2 | *Properties of Fractionally Differentiated Features* | `statistical-learning-foundations` | `mod:fractional-differencing-weights` | secs. 5.4.1–5.4.3, pp. 77–80 | Rewritten; weight formula **corrected**; "makes stationary" corrected to AFML's "necessary"; decay rate added |
| F3 | *Expanding Window* | `statistical-learning-foundations` | `meth:fixed-width-fractional-differencing` (new) | sec. 5.5.1, pp. 80–82 | Rewritten with one consistent index (AFML's is not) |
| F4 | *Fixed-Width Window* | `statistical-learning-foundations` | `meth:fixed-width-fractional-differencing` | sec. 5.5.2, pp. 82–83; secs. 5.6–5.7, pp. 84–88 | Rewritten; FFD range **corrected**; "it is stationary" qualified; minimum-$d$ procedure added |

The time-validity consequences of W3, W7, W8, L3, L5, D8 and F4 are also stated once in `pit:label-weight-leakage` (`financial-ml-evaluation`, new).

**Subclaims outside the blocks and inside them, beyond the rows above.**

| Where | Legacy claim | Disposition |
|---|---|---|
| taxonomy opening and table | "brief overview"; the four-column table | Table rewritten as AFML Table 2.1 in `def:financial-data-types`; the "increasing diversity" ordering restored |
| D1 | Time bars oversample quiet periods; poor statistical properties | Kept as AFML's with "often" and his citation |
| D1 | "returns closer to IID Normal" (Ané–Geman) | Qualified: abstract claims normality under a trade-count clock, ranks trades above volume; "IID" is AFML's gloss; replication stubbed |
| D1 | Volume bars "better statistical properties" | Kept as AFML's report of Clark (1973), with the conflict noted |
| D2 | TIBs are "buckets of trades containing equal amounts of information" | Kept as AFML's interpretation, untested |
| D2 | VIB/DIB address corporate actions | Kept (p. 31) |
| D4 | Series "strictly positive" | Qualified with AFML's own "at worst, infinitesimal"; a short-leg counterexample computed |
| D4 | $c_t$ not embedded in $K_t$ "as shorting will generate fictitious proceeds" | Rewritten ("profits" when the spread is shorted, p. 34) |
| prose before D7 | ML algorithms scale badly; learn better from relevant examples | Kept (p. 38) |
| D8 | "IID observations from a locally stationary process" | Kept as AFML's words; the snippet's level-series convention stated |
| L5 | Meta-labelling achieves higher F1 | Kept as AFML's unsupported claim; F1 not guaranteed (derived) |
| datasampleweights opening | ML literature assumes IID; fails in finance | Kept as AFML's (p. 59) in `def:label-concurrency-uniqueness` |
| W3 | "no information leakage" | Qualified with AFML's training-set condition; `pit:label-weight-leakage` |
| W6 | "much close to IID, verified by increase" | Qualified: Monte Carlo evidence on synthetic spans |
| W7 | "Lower returns should be assigned higher weights" | **Corrected**: applies only to a neutral class, which AFML advises dropping |
| W8 | "$c<0$ ... oldest portion $cT$" | **Corrected**: a share $-c$ of cumulative uniqueness |
| fracdiff opening | Integer differencing removes memory; stationarity needed for inference | Kept as AFML's (pp. 75–76), with "stationarity does not ensure predictive power" added |
| fracdiff opening | Fractional processes "enhance forecasting power compared to ARIMA" | Kept as AFML's account of Hosking (1981), unchecked |
| F3 | Negative drift on an expanding window "still substantial" | Kept (pp. 80–82) |
| F4 | FFD output "is stationary" | Qualified: ADF outcome on one sample; I(1-d) theory; truncation residue computed |

No claim was deleted outright; every not-adopted claim stays in the artefacts.

**Existing entries checked.** `meth:strategy-production-lifecycle` (its "embargo" is a lifecycle stage, distinct from cross-validation embargo; cross-referenced); `pit:parameter-overfitting`, `meth:backtest-evaluation-diagnostics` (cross-referenced, not repeated); `def:order-exposure-decisions` (hidden and reserve orders; cross-referenced from the market-data entry); `meth:garman-klass-volatility`, `def:spread-measures`, `def:securities-lending-fee-rebate`, `mech:securities-lending-short-sale`, `ev:index-reconstitution-impact`, `conv:cme-globex-trading`, `def:futures-hedge-basis`, `mech:etf-creation-redemption`, `def:informed-trader-types`, `mod:factor-risk-model`, `mod:mean-variance-portfolio-optimisation` (cross-referenced). No duplication was found; no existing entry was changed.

### Sources, 2026-10-16

- **López de Prado** (`alpha-afml`), *Advances in Financial Machine Learning*, Wiley 2018, local PDF with a text layer, printed page = PDF page − 27 throughout chaps. 2–5 (checked at pp. 23, 24, 28, 35, 39, 43, 59, 62, 75, 83). Read: chap. 2 pp. 23–42, chap. 3 pp. 43–55, chap. 4 pp. 59–73, chap. 5 pp. 75–89, with snippets and exercises. Page images: pp. 62 (overlap approximation), and, by the two reviews, pp. 28–40 (equations, Figure 2.1, Snippet 2.4), 45–46, 52–53, 60–71, 77–83 (equations, Figures 5.3–5.4). Errata not checked.
- **Velu, Hardy and Nehren** (`s3-velu`), *Algorithmic Trading and Quantitative Strategies*, CRC Press, ISBN 9781498737166, local PDF (copyright page "© 2020"; the catalogue records a 2021 copyright), printed page = PDF page − 17. Read: chap. 1, sec. 1.4, pp. 26–44; Table 1.10 (p. 37) by page image.
- **Ané and Geman (2000)** (`ane-geman-2000`): abstract only, on RePEc, read 2026-10-16; the paper was not accessible (publisher 403).
- **Hudson & Thames**, "Meta Labeling (A Toy Example)" (`ht-meta-labeling-toy`, new source key): read 2026-10-16 for provenance only.
- **Read by the group-A review only**: Murphy and Izzeldin, working-paper comment on Ané and Geman (2006); used only in the backlog stub. **Read by the group-B review only**: web searches for the meta-labelling limitations (no source found).
- **Not read**: AFML chaps. 1 (beyond systematic-investing architecture review), 6–22, including chap. 7 (purging and embargo); Mandelbrot–Taylor, Clark, Easley–López de Prado–O'Hara, Hosking, Kolanovic–Krishnamachari and the other works AFML cites; the readings of the four owning pathways; any U.S. rule text behind Velu's footnotes.

### Numerical checks

Independent of the formulas being checked, kept as `notes/artefacts/statistical-learning-foundations/afml-checks.py` (numpy, statsmodels; fixed seed):
- **Bars**: tick rule with $b_0$; imbalance and runs bars with thresholds from prior bars on a toy flow (all four types close more often in a one-sided burst; on a balanced flow the tick-imbalance threshold collapses to 5,424 bars from 5,900 ticks).
- **ETF trick**: two-leg toy, a consistency check only ($\Delta K$ recomputed from the same prices, 0.007425 against 0.007426, rounding; gross exposure at execution equals $K$); a short leg can drive $K$ to $-0.2$.
- **PCA**: target risk distribution and $\sigma$ delivered exactly; flipping the sign of a component given risk keeps $R$.
- **CUSUM**: events with reset; no events when hovering; strict against non-strict threshold.
- **Triple barrier**: toy paths, vertical barrier by sign or zero, the intrabar ambiguity.
- **Uniqueness and bootstrap**: AFML's toy concurrency $(1,1,2,1,1,1)$ and uniqueness $(0.833,0.75,1)$; probabilities $(5,3,6)/14$ and $(5,3,3)/11$; Monte Carlo medians 0.600 and 0.700, the sequential sample less unique in 22 percent of runs; $(1-1/I)^I\to e^{-1}$; for $I=1000$, $K=100$, $(1-1/K)^I=4.3\times10^{-5}$ against AFML's $e^{-K/I}=0.905$, and 0.100 distinct effective outcomes per in-bag row.
- **Weights**: attribution weights sum to $I$; decay constants for $c=1,0.5,0,-0.5$ meet their boundary conditions; the oldest observation's factor exceeds $c$.
- **Fractional differencing**: recurrence equals the binomial form for $d=0,0.4,1,1.5,2$; signs; ratio $\to1$ and power-law decay $|\omega_k|k^{1+d}\to1/|\Gamma(-d)|$; FFD window 11, 55, 1,458 weights at $\tau=10^{-2},10^{-3},10^{-5}$ with residual sums 0.264, 0.136, 0.036; expanding-window weight loss; a random walk's FFD($d$), $\tau=10^{-4}$, rejecting a unit root by one-lag ADF already at $d=0.2$ ($-5.3$) and at $d=0.4$ ($-10.2$), although I($1-d$), not stationary, in theory.

The group-B review's own script (`checkB.py`, scratch, not kept) reproduced the toy, bootstrap, decay and fractional-differencing results independently, with the sequential bootstrap less unique in 23 percent of its 3,000 runs.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-afml` | chaps. 2–5 as listed | A 2018 practitioner text; its evidence is one futures market (E-mini) or synthetic; several formulas wrong (marked); chap. 7 unread |
| `s3-velu` | chap. 1, sec. 1.4 | Practitioner descriptions as of about 2018–2020; exchange rules and calendars not checked against current sources |
| `ane-geman-2000` | abstract | Paper unread |
| `ht-meta-labeling-toy` | the page | Provenance only; undated, no author |
| Evidence on bars, meta-labelling, alternative-data decay; purging and embargo | none | Stubs |

The seventeen new entries are *partly checked*, *draft*; **human review is outstanding**.

### Preservation

New artefacts under `notes/artefacts/statistical-learning-foundations/` (earlier ones unchanged): `data-taxonomy.tex`, `financial-data-structures.tex`, `labelling.tex`, `sample-weights.tex`, `fractional-differentiation.tex` (each a whole legacy file below its migrate-to line, with only the subsection heading starred), `legacy-wrappers.tex` (display-only `part.tex` line and both wrappers, with all four figures rendered and attributed), `legacy-section-original.tex` and `dataoverview-original.tex` (exact copies), and `afml-checks.py`. The four figure assets were moved, byte-identical (SHA-256 prefixes `fb0a58ca` standardbars, `36f8a864` metalabel, `2faacde0` and `6221383e` the fractional-differencing PNGs), to `notes/artefacts/statistical-learning-foundations/legacy/ml-alternative-data/figures/`, the relative path the originals use, so the bodies compile unedited. A script compared everything with `git show HEAD:…`:
- each body appears exactly once; both wrapper copies are byte-identical;
- all 36 blocks appear verbatim once each, in order; every non-empty segment outside the blocks appears;
- `\item` commands, matched as `\item` not followed by a letter: 83, 21, 24, 19 and 3 (150, all inside blocks), equal in originals and artefacts; substring counts give 98, 27, 32, 27 and 4;
- `\begin`/`\end` sequences identical (52, 86, 34, 38 and 28 commands), covering all 35 display environments (25, 1, 2 and 7; taxonomy none), the table and the three figure environments.

All six artefacts compile alone without warnings, overfull or underfull boxes (5, 5, 2, 2, 2 and 2 pages); their equations, the table and the figures were inspected by page image, including the legacy's preserved errors.

### Counts

`check_compendium.py --check`, 0 problems: 568 → 532 legacy blocks = 487 shared + 16 single-candidate + 29 assigned. Entries 118 → 135 (definitions 42 → 44, data 0 → 3, methods 22 → 31, models 16 → 18, pitfalls 2 → 3). New pathway notes: `statistical-learning-foundations` (11 entries, 4 stubs), `financial-ml-evaluation` (1, 1), `alternative-data-sources` (1, 3), `point-in-time-data` (3, 3); `portfolio-construction` 5 → 6 entries, 7 stubs unchanged. New reading note `s3-velu`; `alpha-afml` extended. One new `front/sources.tex` key, `ht-meta-labeling-toy`.

### Other files

- New topic files `ml-alternative-data/financial-data-structures.tex`, `labelling-sample-weights.tex`, `fractional-differentiation.tex`, `financial-data-types.tex` and `research-engineering-validation/point-in-time-data.tex`; `mod:pca-risk-distribution-weights` appended to `portfolio-construction-risk/portfolio-construction-models.tex`. Openers of `ml-alternative-data` (stale reference to the legacy chapter removed), `research-engineering-validation` and `portfolio-construction-risk` updated.
- Pathway and reading notes as above; `notes/log.md` coverage rows, reading rows (`s3-velu` updated, `alpha-afml` added) and an open question; `notes/source-review-index.md` status, index, next batch and map; `compendium/README.md` order paragraph.

### Build

`latexmk -g -pdf compendium.tex` exits 0: 227 pages (228 before: the legacy ML chapter removed, the new entries added); no LaTeX warnings; 0 overfull and 0 underfull boxes (four overfull and two underfull boxes in the first build fixed: the bars table, the ETF-trick display, two long paths, one paragraph and the new source line); the inherited `page.i` duplicate-destination warning. `check_compendium.py --check` 0 problems; `python3 -m pytest -q tools` 14 passed; `afml-checks.py` runs in about 3 s. Pages inspected as images: the point-in-time data entries, all four new ML topic files (bars table, ETF-trick and bootstrap displays, fractional-differencing pages), the PCA entry and, for the follow-up, the cross-hedge and duration pages; the artefacts' figures and tables.

### Independent review

Two source reviews ran before writing (group A: taxonomy and data structures against AFML chap. 2, Velu sec. 1.4 and the Ané–Geman abstract and critique; group B: labels, weights and fractional differentiation against AFML chaps. 3–5, with their own numerical script), and their findings are the provenance and corrections above. An independent review of the integrated changes then re-read every quote by script against the AFML and Velu text layers, rechecked locators, recomputed the derivatives and hedging review follow-up (Hull pp. 77–79, the return example, GIPS 2.A.12, 2.A.29, 5.A.1, the yield-shift condition) and the mathematics, ran `afml-checks.py`, and compared the records, counts and artefacts. Fixed:
- **Definite errors.** The fractional-differencing ADF illustration quoted a statistic ($-7.6$) from an earlier run of the script: adding the balanced-flow test had shifted the random-number stream; the entry now gives the script's $-5.3$ at $d=0.2$ and $-10.2$ at $d=0.4$, with $\tau=10^{-4}$. The cross-hedging locator p. 78 (Hull's *Choice of Contract*) became p. 77 and sec. 3.4, p. 79, also noted in the follow-up record. The PCA entry's "$2^N$ allocations" became $2^k$ for the $k$ components given risk, with distinct eigenvalues (non-unique with repeated ones); the script and the portfolio-construction note follow. The compendium was rebuilt after the last edit, and this record appended (it had been drafted outside the repository at review time).
- **Judgement calls adopted.** The share of Monte Carlo runs in which the sequential bootstrap is less unique is now computed by the kept script (22 percent; the review's 3,000 runs gave 23); the overlap example distinguishes the exact $4.3\times10^{-5}$ from $e^{-I/K}=4.5\times10^{-5}$; the attribution weights name log returns; the Monte Carlo spans are 1–4 bars (Snippet 4.7, `maxH=5`); the ETF-trick toy is called a consistency check; GIPS 2.A.12 is described as a calculation provision with no stated reason, the reason being interpretation; Hull's jet-fuel example needs no unit conversion; "routed against the map" became "outside the map's candidates"; the CUSUM input remark is labelled interpretation; an unread chap.-10 phrase was dropped from the meta-labelling entry.
- **Verified unchanged.** All other quotes, locators and numbers; the derivatives and hedging review follow-up; the provenance claims; counts, labels and pathway order; preservation.

### For review

- Routing the reference- and market-data blocks to `point-in-time-data` and the PCA weights to `portfolio-construction`, both against the map.
- Correcting López de Prado's own formulas (overlap approximation, time-decay boundary, index ranges) on the basis of derivation and computation, without errata.
- Qualifying the stationarity of fractionally differenced series with fractional-integration theory, which is interpretation, not a reading.
- Keeping the three reproduced AFML figures only in the artefact, with attribution.

## financial data and labels review follow-up: hedge-ratio sign, ETF-trick timing and capital, label spans, and the Hawkes lead, 16 October 2026

Narrow corrections to financial data and labels review (`8be60d1`) and to a derivatives and hedging review entry, run before order books and order flow review; the earlier records are left as written, and this record supersedes them where they differ. No legacy block, entry label, stub or count changed (532 legacy blocks; 135 entries). Decisive examples are reproduced by `notes/artefacts/volatility-options/negative-hedge-ratio-check.py` and `notes/artefacts/statistical-learning-foundations/financial-labels-capital-checks.py` (numpy only); the earlier scripts are unchanged.

- **Negative hedge ratios, `def:futures-hedge-basis` and `mod:minimum-variance-hedge-ratio`.** The first said a negative $h$ "would add to the exposure". With the stated convention ($V(h)=\Delta S-h\Delta F$; $h>0$ a short futures position against a long exposure), $h^*=\operatorname{Cov}(\Delta S,\Delta F)/\operatorname{Var}\Delta F$ has the sign of $\rho$, and a negative $h^*$, a long futures position against a long exposure, still reduces variance to $\sigma_S^2(1-\rho^2)$. Example: $\sigma_S=\sigma_F=1$, $\rho=-0.6$: $h^*=-0.6$ leaves 0.64 against 1 unhedged, while $h=+0.6$ gives 2.08; a 200,000-draw simulation gives an OLS slope of $-0.6003$ and the same grid minimiser. Both entries now state the sign convention and the case.
- **ETF trick timing, `meth:etf-trick`.** The entry called sizing at $o_{i,t+1}$ "execution at the next open, not look-ahead, provided $\omega_t$ uses information up to $t$". López de Prado's holdings divide by the next open, unknown at $t$, so the series is an accounting convention; causal weights are necessary but not sufficient for it to be executable. The entry now names what would reproduce it: an order whose quantity is set by its own fill price, such as a notional order per leg filled in full in a single-price opening auction at $o_{i,t+1}$ with $\varphi_{i,t}$ known, to be checked per venue and instrument; a quantity sized on $p_{i,t}$ leaves a gross exposure of 1.0026 against $K=1$ on a two-leg toy with 1.5 and 1.6 percent opening gaps.
- **Gross exposure and capital, same entry.** "Gross exposure equals $K_t$" is $|K_t|$ when every $o_{i,t+1}\varphi_{i,t}>0$, and $K_t$ only with $K_t\ge0$; with a negative price a holding's sign no longer follows its weight. At $K_t=0$ the holdings vanish and at $K_t<0$ they reverse ($K=-0.2$ turns the long leg short, gross 0.2); the method has no rule for exhausted capital, so a backtest must stop the series or state its own financing or loss rule. No production system is described.
- **Label spans, `def:label-concurrency-uniqueness`, `meth:sample-weights-attribution-decay`, `meth:triple-barrier-labelling`.** For returns $r_{t-1,t}$ indexed by ending time, a label from $t_{i,0}$ to $t_{i,1}$ uses $t_{i,0}<t\le t_{i,1}$; the entries now define $1_{t,i}$ that way and start the attribution sum at $t_{i,0}+1$. The earlier remark that "either convention can be used if it is used consistently", and that the toy "has the same off-by-one", was wrong. López de Prado's toy matrix (p. 65, rows $t=1,\dots,6$) is the ending-time rule, and Snippet 4.6's spans $\{0{:}2,2{:}3,4{:}5\}$ are a consistent start-time reindexing; his Snippets 4.1, 4.3 and 4.10 mark $t_{i,0}$ to $t_{i,1}$ inclusive on event timestamps, which adds the return ending at $t_{i,0}$. On the toy's events that inclusive rule gives concurrency $(1,1,2,2,2,1,1)$ and uniqueness $(0.75,0.5,0.833)$ against $(1,1,2,1,1,1)$ and $(0.833,0.75,1)$, and labels 2 and 3, adjacent at $t=4$, share $r_{3,4}$, which label 3 does not use; attribution sums on a toy path change from $(0.0247,0.0145,0.0190)$ to $(0.0149,0.0146,0.0288)$. The bootstrap probabilities and Monte Carlo of `meth:sequential-bootstrap` are unaffected (the toy matrix is unchanged; the Monte Carlo replicates AFML's own code convention, as financial data and labels review recorded). Read again: AFML pp. 60–61, 64–66 and 69 (text layer).
- **Hawkes lead, `notes/source-review-index.md`.** The proposed the topic review named `wide-bacry-life-cycle` (an impact paper) as the Hawkes lead and said a reading note existed for it in that role. Replaced by `wide-bacry-hawkes`, Bacry, Mastromatteo and Muzy, "Hawkes Processes in Finance", a required reading of `market-making-lob`, with no reading note and no full-text check at the time of the correction (order books and order flow review then read parts of its preprint; see below).
- **Notes and index.** `statistical-learning-foundations` and `commodity-hedging` notes, the `alpha-afml` reading note and `log.md` record the changes; the financial data and labels review index row gives `8be60d1`.

## order books and order flow review: orders, the limit order book, queues, order flow and point processes (eight files, one batch), 16 October 2026

A single integrated batch of 73 blocks from `compendium/legacy/execution-market-making/`, run after the financial data and labels review follow-up above, organised for checking in three groups that were not separate stopping points: A, orders and books (`02_orders_matching_and_limit_order_books/02_order_lifecycle.tex`, 5; `03_limit_order_book_mechanics.tex`, 24; `05_queue_dynamics_and_latency.tex`, 7); B, signing, imbalance and stylised facts (`04_order_flow_and_empirical_microstructure/01_...`, 5; `02_...`, 5; `03_...`, 11); C, event time and point processes (`06_...`, 5; `07_...`, 11). Migration and source checking, not study; no checkpoint was attempted.

### Scope

Counted by script against the committed originals (starting commit `8be60d1`): 73 blocks (5, 24, 7, 5, 5, 11, 5, 11), 61 `\item` commands (11, 18, 4, 3, 5, 4, 5, 11), all inside blocks; one proof (inside the limit-order proposition); no figures, tables or assets. Outside the blocks the files hold only their `% migrate-to:` line and `\subsection` heading. Also accounted for: the two folder wrappers (`02_.../00_overview.tex`, `04_.../00_overview.tex`), from which the eight `\input` lines were removed, and the eight map rows. The other files of both folders, the macro chapter, the assigned HFT and information and price discovery review remnants, Ho–Stoll and the other deferred items are unchanged.

### Provenance

No file named a source. Block by block, the material follows:
- **Lehalle and Laruelle** (`alpha-laruelle`, 2nd ed. 2018): chap. 3, sec. 3.3 (pp. 216–227) for the CLOB and RFQ contrast, messages and channels, the three event types, conditioning, the Poisson baseline and its estimation, queue-reactive Models I–III, the A/R ratio, mean reversion and reset, and imbalance; chap. 1, sec. 1.3 (pp. 74–90) for tick size, binding probability and leeway, quoted depth, order-to-trade ratio, cumulative depth, queue jumping; app. A, sec. A.6 (pp. 266–273) for the Harris model and its counterfactual, nearly symbol for symbol; secs. A.11–A.13 (pp. 298–319) for decomposition, moving averages, deseasonalisation, the volume model, point processes, Hawkes processes, signature plot and Epps effect, also nearly symbol for symbol.
- **Harris** (`alpha-harris`): limit-price placement, limit orders as options, their two risks and absent traders (chap. 4, pp. 73–78); price clustering (p. 91); open and closed books (p. 109); the block statistic and block-price rule (sec. 15.5, pp. 332–333); Lee–Ready and its limits (p. 423).
- **Hasbrouck** (`s6-hasbrouck`): signing and signed volume (sec. 9.7, pp. 89–90); event against wall-clock time (p. 90); duration analysis (sec. 15.2.3, pp. 163–164).
- **Bouchaud et al.** (`catalogue-0528`): queue imbalance $I$ (chap. 7), Hawkes conditions and inhibition (chap. 9), stylised facts (chaps. 2, 4, 10), priority rules (chap. 3) and the "order-flow imbalance" of signed market orders (p. 222).
- Not found in any source read: the five-state lifecycle as worded, the "latency race boundary", queue imbalance's "less likely to reverse", the horizon caveat on imbalance, clustering's three reasons, the consolidated-tape caveat, refresh-time sampling, "false persistence", and the claim that marked Hawkes models can inhibit. Each is either rewritten as interpretation, corrected, or not adopted, as below.

### Ownership and dispositions

Routed by guide outcomes; every owner is one of its file's map candidates, so there is **no routing exception**. The section overview `execution-market-making` (outcome: evaluate a quoting policy on an order-book replay by fill probability, adverse selection and inventory risk, with queue-position assumptions; its checkpoint replays acknowledgements, cancellations, fills and missed fills) owns the lifecycle, the book and limit orders as options. `market-making-lob` ("model queue dynamics and fill probabilities"; readings include Huang–Lehalle–Rosenbaum, Lehalle–Mounjid and `wide-bacry-hawkes`) owns queues, queue imbalance, queue-reactive intensities and Hawkes processes. `market-structure-execution-quality` (its outcome names tick size) owns the tick-size blocks. `lob-deep-learning` (checkpoint: "a linear OFI baseline"; readings on OFI) owns order-flow imbalance. `market-simulation` ("validate it against stylised facts") owns stylised facts, realised variance, deseasonalisation, clocks and point processes. `price-impact-execution` (estimate impact from executions; signs are inputs to impact regressions and propagators) owns trade signing. Rejected: `lob-deep-learning` for trade signing (its readings start from book data, not signed trades); `market-simulation` for Hawkes processes (the reading that defines them is `market-making-lob`'s); `execution-market-making` for tick size (its outcome does not name market design).

| File | # | Legacy block | Owner | Destination | Disposition |
|---|---|---|---|---|---|
| 02/02 | 1 | *Order State Segmentation* | `execution-market-making` | `mech:order-lifecycle` (new) | Rewritten against FIX 4.4 OrdStatus; the five states kept as a simplification |
| | 2 | *Limit-Order Lifecycle* | | same | Rewritten; "loses priority when price worsens" **corrected** to CME FIFO's rule (any price change, size increase, account change) and made venue-specific |
| | 3 | *Message-Channel Segmentation* | | same | Rewritten (LL p. 218: private channel faster) |
| | 4 | *Absent Trader Representation* | | same | Rewritten (Harris pp. 77–78; stop-order example) |
| | 5 | *Lifecycle Tags Change Priority* | | same | Partly adopted (time in force, iceberg priority, IOC); minimum quantity and cancel-on-disconnect stubbed |
| 02/03 | 1 | *Best Quotes and Spread* | `execution-market-making` | `def:limit-order-book` (new) | Merged; spread measures cross-referenced to `def:spread-measures`, not repeated |
| | 2 | *Liquidity Supply and Demand* | | same | Merged (TQP p. 43) |
| | 3 | *Limit Price Placement* | | same | Rewritten as Harris's Table 4-1; "far: low immediacy cost" **corrected** |
| | 4 | *Standing Limit Orders Are Trading Options* | | `res:limit-order-options` (new) | Rewritten (Harris pp. 75–76; TQP p. 46); payoff and proof idea kept as derived, conditions added |
| | 5 | *Limit-Order Regret* | | same | Rewritten as Harris's two risks (p. 77) |
| | 6 | *Equilibrium Spread as Order-Choice Indifference* | | `res:spread-determinants` (existing) | Already stated there (Harris pp. 304–310); cross-referenced, not repeated |
| | 7 | *Limit Orders Give Timing Options* | | `res:limit-order-options` | Merged; monitoring speed marked as beyond the pages read |
| | 8 | *Tick Size* | `market-structure-execution-quality` | `def:tick-size` (new) | Rewritten (LL p. 74; TQP pp. 48–49) |
| | 9 | *Price Clustering* | | same | Rewritten as Harris p. 91; the legacy reasons not adopted |
| | 10 | *Binding Tick Constraint* | | same | Rewritten (LL p. 77); "further reductions mostly change queue behaviour" not adopted |
| | 11 | *Harris Tick Discretisation Model* | | `mod:harris-discretised-spread` (new) | Rewritten with $\Phi$ stated |
| | 12 | *Continuous Spread Expectation* | | same | Rewritten; likelihood and fit added |
| | 13 | *Tick-Size Counterfactual* | | same | Units **corrected**: an observed $k$-tick spread is $k\delta$ new ticks; the model re-rounds the latent spread, $E=\sum_k(k/\delta)f_\delta(k)$ in old ticks (page images pp. 272–273) |
| | 14 | *Harris Model Inputs* | | same | Merged |
| | 15 | *Tick Size and Queue Discipline* | | `def:tick-size` | Rewritten (TQP p. 49; LL pp. 88–89) |
| | 16 | *Quoted Depth Under Small Ticks* | | `ev:tick-size-market-quality` (new) | Rewritten with sample (FTSE 100, April 2012) |
| | 17 | *Order-to-Trade Ratio* | | same | Rewritten (+50 percent, LL p. 84) |
| | 18 | *Cumulative Depth* | | same | Rewritten; conditioning on takers and fragmentation added |
| | 19 | *CLOB as Price-Formation Device* | `execution-market-making` | `def:limit-order-book` | Merged |
| | 20 | *Order-Book Visibility* | | same | Open/closed book from Harris p. 109; top-of-book and depth-book levels pointed to `data:market-data-levels` |
| | 21 | *LOB Event Types* | | same | Merged (LL p. 219; TQP p. 51) |
| | 22 | *Tick-Size Quality Proxies* | `market-structure-execution-quality` | `def:tick-size` | Merged (LL pp. 77, 84) |
| | 23 | *Value of a Quote* | | `ev:tick-size-market-quality` | Value of quote adopted (LL p. 84); consolidated-tape clause not adopted |
| | 24 | *RFQ Can Mimic a Book* | `execution-market-making` | `def:limit-order-book` | Rewritten (LL p. 216); conditional depth as interpretation |
| 02/05 | 1 | *Condition on the Queue* | `market-making-lob` | `mod:queue-reactive-intensities` (new) | Rewritten (LL pp. 219–220) |
| | 2 | *Queue Imbalance* | | `def:queue-imbalance` (new) | Merged with 04/02 #3; the reversal claim not adopted |
| | 3 | *Arrival-Departure Ratio* | | `mod:queue-reactive-intensities` | Rewritten (LL p. 224) with the promotion argument and a drift check |
| | 4 | *Adverse Queue Selection* | `execution-market-making` | `res:limit-order-options` | Merged (Harris p. 77; TQP p. 46) |
| | 5 | *Queue-Reactive Estimation* | `market-making-lob` | `mod:queue-reactive-intensities` | Rewritten (LL pp. 221–223); the starting-time dependence (n. 12) added and computed |
| | 6 | *Mechanical Mean Reversion* | | same | Rewritten (LL pp. 225–226) |
| | 7 | *Latency Race Boundary* | | same (Pitfalls) | Kept as interpretation, with LL p. 89 and TQP p. 59 |
| 04/01 | 1 | *Trade-Sign Classification Segmentation* | `price-impact-execution` | `meth:trade-sign-classification` (new) | Rewritten (Hasbrouck p. 89; Harris pp. 332, 423) |
| | 2 | *Lee-Ready Classification* | | same | Rewritten; the paper itself not read |
| | 3 | *Signed Volume* | | same | Rewritten; transforms (p. 89); "false persistence" not adopted |
| | 4 | *Passive-Aggressive Ambiguity* | | same | Rewritten from Harris's sidebar (p. 423) |
| | 5 | *Block Initiator Asymmetry* | | same | Kept as Harris's report ("approximately 80 percent", no sample); primary evidence stubbed |
| 04/02 | 1 | *Order Flow Imbalance* | `lob-deep-learning` | `def:order-flow-imbalance` (new) | **Corrected**: defined as Cont–Kukanov–Stoikov's event-based $e_n$, not signed trades |
| | 2 | *Signed-Trade Imbalance* | | same | Renamed trade imbalance (CKS $\mathrm{TI}_k$); naming collision with TQP p. 222 recorded |
| | 3 | *Queue Imbalance* | `market-making-lob` | `def:queue-imbalance` | Merged duplicate; $QI=2I-1$ |
| | 4 | *Imbalance Feature Segmentation* | `lob-deep-learning` | `def:order-flow-imbalance` | Kept as a menu, not results; multi-level OFI stubbed |
| | 5 | *Imbalance Is Horizon-Dependent* | | same (Pitfalls) | Not found; not adopted as a claim; CKS fits are contemporaneous; stubbed |
| 04/03 | 1 | *High-Frequency Stylized Facts* | `market-simulation` | `ev:high-frequency-stylised-facts` (new) | Rewritten with each fact's sample (TQP) |
| | 2 | *Signature Plot* | | `meth:realised-variance-signature-plot` (new) | Rewritten (LL pp. 316–317; TQP pp. 25–28) |
| | 3 | *Microstructure Noise in Volatility* | | same | Rewritten; divergence conditioned on the noise model |
| | 4 | *Epps Effect* | | same | Rewritten with Epps's words as LL quote them and their sample |
| | 5 | *Realised Covariance* | | same | Rewritten; refresh-time not adopted (stub); previous-tick shown to cause Epps |
| | 6 | *Time-Series Decomposition* | | `meth:intraday-deseasonalisation` (new) | Rewritten (LL p. 299) |
| | 7 | *Centred Moving Average* | | same | Rewritten; $A_t$ typo and window rule **corrected**; look-ahead added |
| | 8 | *Additive Deseasonalisation* | | same | Rewritten (LL pp. 300–301) |
| | 9 | *Multiplicative Deseasonalisation* | | same | Rewritten (LL pp. 301–302) |
| | 10 | *Volume Seasonality Factorisation* | | same | Rewritten with LL's $E[H]=1$, $\sum F=1$ and example |
| | 11 | *Seasonality Before Signal* | | same (Pitfalls) | Kept; estimation from earlier data added |
| 04/06 | 1 | *Trade Duration* | `market-simulation` | `def:market-clocks-durations` (new) | Rewritten (LL p. 306; Hasbrouck pp. 163–164) |
| | 2 | *Market Time Segmentation* | | same | Rewritten (Hasbrouck p. 90; TQP p. 173); volume time pointed to `meth:activity-sampled-bars` |
| | 3 | *Duration Notation* | | same | Merged |
| | 4 | *Event Time for Microstructure Laws* | | same | Rewritten as Hasbrouck's rule |
| | 5 | *Activity Time Can Hide Stress* | | same (Practice) | Kept as interpretation |
| 04/07 | 1 | *Point-Process View* | `market-simulation` | `def:order-event-point-processes` (new) | Rewritten (LL p. 305) |
| | 2 | *Counting Process and Duration* | | same | Rewritten (LL p. 306) |
| | 3 | *Conditional Intensity* | | same | Rewritten; predictability stated |
| | 4 | *Order-Book Event Segmentation* | | same (Notation) | Merged (LL p. 221) |
| | 5 | *Homogeneous Poisson Baseline* | `market-making-lob` | `mod:queue-reactive-intensities` | Rewritten as LL's finding for one stock |
| | 6 | *Integrated Intensity* | `market-simulation` | `def:order-event-point-processes` | Rewritten; LL's printed condition $\int\lambda=1$ **corrected** to divergence (page image p. 308); time rescaling computed |
| | 7 | *Linear Hawkes Process* | `market-making-lob` | `mod:hawkes-order-flow` (new) | Rewritten with conditions (non-negative causal kernel, $g<1$ or spectral radius $<1$) |
| | 8 | *Exponential Hawkes Kernel* | | same | Kept ($\alpha/\beta$, $\lambda_0/(1-\alpha/\beta)$, LL pp. 309–311); parameterisations compared |
| | 9 | *Conditioning Improves Queue Dynamics* | | `mod:queue-reactive-intensities` | Merged (LL pp. 223–224) |
| | 10 | *Conditioning Segmentation* | | same | Merged; its event-time item to `def:market-clocks-durations` |
| | 11 | *Marked Flow Segmentation* | | `mod:hawkes-order-flow` | **Corrected**: inhibition needs a non-linear link (TQP p. 181; BMM p. 8); agent classes from LL pp. 315–316 |

**Existing entries checked.** `def:spread-measures` (best quotes, spread, midpoint), `res:spread-determinants` (order-driven equilibrium, timing option, large-tick bounce and depth), `meth:information-driven-bars` (tick rule) and `meth:activity-sampled-bars` (volume and dollar clocks), `data:market-data-levels` (book levels), `conv:cme-globex-trading` (matching and priority), `def:order-exposure-decisions` (hidden orders), `mod:propagator` (sign persistence), `def:volatility-components`, `meth:garman-klass-volatility`, `res:roll-spread-estimator` and `def:intraday-overnight-returns` (volatility), `mod:kyle-single-auction` and `meth:order-flow-impact-regression` (net flow), `pit:label-weight-leakage`: cross-referenced from the new entries; no duplication found and none changed.

### Sources, 2026-10-16

- **Lehalle and Laruelle** (`alpha-laruelle`), local PDF with a text layer, printed page = PDF page − 27: chap. 1, pp. 74–90; chap. 3, pp. 216–227; app. A, pp. 266–273, 298–319; page images of pp. 272–273 (counterfactual), 306 and 308 (intensity, time change).
- **Bouchaud, Bonart, Donier and Gould** (`catalogue-0528`), local PDF, printed = PDF − 19: chaps. 2 (pp. 23–31), 3 (pp. 43–56), 4 (pp. 58–61), 7 (pp. 118–120), 9 (pp. 163–185), 10 (pp. 187–189), 11 (pp. 222–223).
- **Harris** (`alpha-harris`), 2002 printing through macOS PDFKit, printed = PDF − 13: pp. 73–78, 91, 109, 332–333, 423.
- **Hasbrouck** (`s6-hasbrouck`), 2007 book (not the 2004 draft), printed = PDF − 11: pp. 89–90, 163–164, 180.
- **Cont, Kukanov and Stoikov** (`catalogue-0503`): arXiv 1011.6402v3, pp. 1, 4, 8, 16, downloaded 2026-10-16; journal version not checked. New reading note.
- **Bacry, Mastromatteo and Muzy** (`wide-bacry-hawkes`): arXiv 1502.04592v2, secs. 1–2.2.4 (pp. 1–8), 5.1 (p. 27), 6.1 (pp. 29–30), downloaded 2026-10-16; journal version not checked. New reading note.
- **FIX 4.4 OrdStatus** through the OnixS dictionary (`onixs-fix44-ordstatus`, new source key), read 2026-10-16; the FIX Trading Community's specification not consulted.
- **CME Globex FIFO rule**: as cited from `ex-cme-matching` in futures market structure review, not reread.
- **Not read**: Huang–Lehalle–Rosenbaum, Cont–Stoikov–Talreja, Lehalle–Mounjid, Moallemi–Yuan, Kolm–Turiel–Westray, Cont–Cucuringu–Zhang, Vyetrenko et al., Lee–Ready, Epps, Harris (1994), Brémaud–Massoulié, Daley–Vere-Jones, and the tick-size studies Lehalle and Laruelle summarise; Johnson (`alpha-johnson`) has no text layer in the local copy and was not used.

### Numerical checks

`notes/artefacts/market-simulation/order-flow-checks.py` (numpy, scipy; fixed seed; about 2 s), independent of the entries' formulas:
- **Harris counterfactual**: gamma latent spread (shape 4), $\delta=5$: latent means 0.6, 1.2, 3 and 8 old ticks give expected spreads 1.010→0.601, 1.302→1.200, 3.005→3.000, 8.000→8.000 old ticks; the legacy $k/\delta$ rescaling would predict −6.4 for the last.
- **Imbalance**: $QI=2I-1$ to $10^{-16}$; scale invariance. **OFI against trade imbalance**: a five-state toy gives $\mathrm{OFI}=+400$, $\mathrm{TI}=-100$.
- **Lee–Ready**: four toy trades, including a sell at the bid after an uptick.
- **Realised variance with i.i.d. noise**: tracks $\int\sigma^2+2n\sigma_\eta^2$ from 13 to 23,400 returns. **Epps from asynchrony**: true correlation 0.6, previous-tick sampling, 40 paths: 0.120 at step 5, 0.394 at 30, 0.547 at 120, 0.629 at 600.
- **Deseasonalisation**: multiplicative coefficients recovered within 0.0052; a later shock moves the centred average at the six earlier times.
- **Hawkes**: exponential kernel, branching ratio 0.6: rate 2.471 against 2.500, clustering ratio 6.38 against the long-window 6.25; compensator-rescaled durations mean 1.005, KS $p=0.35$ (raw durations $p\approx10^{-268}$). **Inhibition**: linear intensity $-0.30$ after one event; positive-part link: rate 0.369, clustering ratio 0.62. **A/R ratio**: drifts $+0.091$ and $-0.111$ per event at 1.2 and 0.8. **Waiting-time estimator**: 0.594 from uniform starts against 0.405 from events on a Hawkes sample.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | as listed | Practitioner text, 2018; queue-reactive results reported second-hand; one large-tick stock |
| `catalogue-0528` | as listed | NASDAQ 2015 samples; book's own summaries of the literature |
| `alpha-harris` | as listed | 2002; the 80 percent block statistic has no stated sample |
| `s6-hasbrouck` | as listed | Methods; Lee–Ready not read |
| `catalogue-0503` | arXiv v3 | Preprint; April 2010 U.S. data; contemporaneous fits |
| `wide-bacry-hawkes` | arXiv v2, parts | Review; empirical results second-hand |
| `onixs-fix44-ordstatus` | one page | Vendor rendering of a 2003-era standard |

The sixteen new entries are *partly checked*, *draft*; **human review is outstanding**.

### Preservation

New artefacts, one standalone file per legacy file (whole file below its `% migrate-to:` line, only the subsection heading starred), each with a header naming its destinations: `notes/artefacts/execution-market-making/order-lifecycle.tex`, `limit-order-book-mechanics.tex`, `02-overview-original.tex` (exact copy of the folder wrapper before the topic review); `notes/artefacts/market-making-lob/queue-dynamics-latency.tex`, `statistical-models-order-flow.tex`; `notes/artefacts/price-impact-execution/trade-classification.tex`; `notes/artefacts/lob-deep-learning/order-flow-imbalance.tex`; `notes/artefacts/market-simulation/stylized-facts.tex`, `trade-duration-event-time.tex`, `04-overview-original.tex`, and `order-flow-checks.py`. The earlier `market-making-lob/derivations.tex` is unchanged. A script compared everything with `git show 8be60d1:…`: each body appears exactly once; all 73 blocks appear verbatim and in order; `\item` counts (matched as `\item` not followed by a letter) 11, 18, 4, 3, 5, 4, 5, 11 equal in originals and artefacts; `\begin`/`\end` sequences identical (16, 58, 16, 12, 12, 24, 12, 28 commands, the proof included); both wrapper copies byte-identical. All eight artefacts compile alone with no warnings, overfull or underfull boxes (1, 3, 1, 2, 1, 1, 2, 1 pages); the limit-order-book and stylised-facts pages were inspected by image.

### Counts

`check_compendium.py --check`, 0 problems: 532 → 459 legacy blocks = 414 shared + 16 single-candidate + 29 assigned; `execution-market-making` legacy 412 → 339. Entries 135 → 151 (definitions 44 → 50, evidence 5 → 7, mechanisms 9 → 10, methods 31 → 34, models 18 → 21, results 18 → 19). Pathway notes: new `lob-deep-learning` (1 entry, 2 stubs) and `market-simulation` (5, 3); `execution-market-making` 23 → 26 entries, 0 → 1 stub; `market-making-lob` 13 → 16 listed, 5 → 8 stubs; `market-structure-execution-quality` 5 → 8, 2 → 4; `price-impact-execution` 9 → 10, 0 → 2. New reading notes `catalogue-0503` and `wide-bacry-hawkes`; `alpha-laruelle`, `catalogue-0528`, `alpha-harris` and `s6-hasbrouck` extended. One new `front/sources.tex` key, `onixs-fix44-ordstatus`.

### Other files

- New topic files `execution-market-making/order-books.tex` and `order-flow-statistics.tex` (input first in the chapter), `execution-trading-costs/tick-size.tex` and `trade-signing.tex`; both chapter openers updated.
- `notes/log.md` coverage rows (two new) and three open questions; `notes/source-review-index.md` status, index, next batch and map (eight rows removed); `compendium/README.md` order paragraph.

### Build

`latexmk -g -pdf compendium.tex` exits 0: 234 pages (227 before); no LaTeX warnings; 0 overfull and 0 underfull boxes; the inherited `page.i` duplicate-destination warning. `python3 -B -m unittest discover -s tools -p 'test_*.py'`: 14 tests pass. Pages inspected as images: the queue-imbalance, queue-reactive and OFI pages, the Harris model page, the label-concurrency page, and, before the final rebuild, all pages carrying the new entries and the corrected ETF-trick and hedge entries.

### Independent review

An integrated review of the whole batch, by the same session, after writing: every quotation in the new and changed entries was searched by script in the normalised text layers of the seven sources (all order books and order flow review source quotations found; unmatched strings are legacy wording quoted as such, page titles, or financial data and labels review quotes containing mathematics); locators were rechecked against the printed-page offsets; the mathematics was rederived (the $e_n$ cases, $QI=2I-1$, $E[\hat V_R]$ with noise, the Hawkes mean, branching and stability conditions, the counterfactual's units, the ETF gross-exposure identity). Fixed: a figure locator (Epps, pp. 318–319), the Harris chapter for open books (chap. 5), the CKS robustness passage (p. 8, not a claim of stability), the tick-regime pitfall (Lehalle and Laruelle's quotation groups do group by liquidity), an index clash in the ETF identity, and simulation figures re-taken after the Epps check was replicated over 40 paths (which shifted the random stream). This was not an independent second reader: **human review is outstanding.**

### For review

- Merging the two queue-imbalance definitions under `market-making-lob` and the OFI definition under `lob-deep-learning`, with Bouchaud et al.'s naming collision recorded rather than resolved.
- Correcting a printed condition in Lehalle and Laruelle (time change) and the legacy counterfactual's units by derivation and computation, without errata.
- Treating the FIX 4.4 states (through a vendor page) as the reference for order states.
- Keeping Harris's 80 percent block statistic as his unsourced report.

## order books and order flow review follow-up: trade-signing arithmetic, order types, session boundaries, FIX states, realised variance and waiting times, 16 October 2026

Corrections to order books and order flow review (`d40d4c2`), run before order matching and fragmentation review; the order books and order flow review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label or count changed (459 legacy blocks; 151 entries). Each correction is reproduced in `notes/artefacts/market-simulation/order-flow-checks.py` (run with numpy and scipy); the other results of that script are unchanged.

1. **Trade signing, `meth:trade-sign-classification`.** The order books and order flow review check computed the midpoint in binary floating point, so $(10.00+10.01)/2=10.004999\dots$ and the half-tick midpoint trade at 10.005 after a downtick returned $+1$ (a buy); the order books and order flow review record's "four toy trades" therefore included one wrong result, although the entry's wording happened to state the right rule. The check now holds prices as `Decimal` values built from strings, signs zero ticks by the last non-zero change, and asserts ten cases: half-tick and whole-tick midpoints after up- and downticks, zero upticks and zero downticks, a midpoint with no prior change (unclassified), trades just above and below a half-tick midpoint, and trades at the bid and ask against the previous tick. All ten pass; the entry's *Checked* sentence states them.
2. **Order type against aggressiveness, `def:limit-order-book`.** The entry said an order that matches on arrival *is* a market order. That is Bouchaud et al.'s event convention (p. 45), now named as such; Harris's market order is an instruction to trade at the best price (p. 71), and a marketable limit order can execute at once while limiting its price (p. 73). A crossing limit order executes the matching part and rests the rest at its limit (Bouchaud et al., p. 45) unless an immediate-or-cancel instruction removes it (p. 55).
3. **Session boundaries, `mech:order-lifecycle`.** "An order book is empty at the start of the day" was stated as universal. Lehalle and Laruelle say "most often empty" (p. 217); the entry now attributes it and adds Harris's day and good-till-cancel orders (pp. 82–84, Table 4-3) and FIX 4.4's TimeInForce (an absent value means "Day (or session)"; good till cancel and good till date exist), so orders carried across sessions rest in the reopened book. A dated CME rule could not be read (CME's site refuses scripted access; not circumvented) and is a backlog stub (`conv:session-carry-over`).
4. **FIX 4.4 states, same entry.** "Replaced" was listed among OrdStatus values from a vendor page that itself marked it as replaced in FIX 4.3. Checked against the FIX Trading Community's FIX 4.4 Orchestra repository (FIX.4.4_EP311) as rendered by Orchimate, to which FIXimate links: OrdStatus (39) has new, partially filled, filled, done for day, cancelled, pending cancel, stopped, rejected, suspended, pending new, calculated, expired, accepted for bidding and pending replace, and no value 5; ExecType (150) "describes the specific ExecutionRpt ... while OrdStatus (39) will always identify the current order status", with 5 = Replace and F = Trade. The entry and a new source key `fix44-orchestra` say so; the OnixS key is kept in the sources with a note that it was superseded.
5. **Realised variance, `meth:realised-variance-signature-plot`.** The limits to integrated variance and covariance are now attributed to Lehalle and Laruelle's "Itô semi-martingale framework" and restricted to continuous Itô processes; with jumps the limits are the quadratic variation and covariation, including co-jumps. Counterexample (computed): a unit-jump Poisson path with five jumps on [0, 1] has zero diffusion variance and realised variance 9 on a 10-step grid, 5 from 10^4 steps; three common jumps of +1 and −0.5 give realised covariance −1.5. The finite-grid expectation $\sigma^2T+2n\sigma_\eta^2$ is stated as exact for the simulated driftless Brownian model with i.i.d. centred noise independent of it, not for general semimartingales.
6. **Waiting times, `mod:queue-reactive-intensities` and the script.** "Equal in expectation only for a Poisson process" was wrong. For a stationary renewal process with finite second moment the mean wait from an arbitrary time is $E[X^2]/(2E[X])$, equal to $E[X]$ exactly when the coefficient of variation is 1. Counterexample: gaps 0.5 with probability 0.8 and 3 with probability 0.2 have $E[X]=1$, $E[X^2]=2$, CV 1, and a simulated mean wait of 1.0006 against a mean gap of 0.9997. The valid point is kept: the Hawkes sample's gaps (CV 1.37) give a mean wait from uniform starts of 0.594 against a mean gap of 0.405, near $E[X^2]/(2E[X])=0.579$.

Source statements and derived corrections are kept apart in the entries: items 2–4 restate sources more exactly, items 1, 5 and 6 are derivations and computations.

## order matching and fragmentation review: the rest of the orders-and-matching folder (order types, matching, hidden liquidity and dark trading, routing and fragmentation), 16 October 2026

A single batch of 108 blocks from `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/`, run after the order books and order flow review follow-up, with review checkpoints of 34 blocks (`01_order_types_and_instructions.tex`, 16; `04_matching_algorithms.tex`, 18), 23 (`06_hidden_liquidity_and_dark_trading.tex`) and 51 (`07_cross_venue_routing_and_fragmentation.tex`). It closes the folder. Migration and source checking, not study.

### Scope

Counted by script against the starting commit `d40d4c2`: 108 blocks (16, 18, 23, 51), 117 `\item` commands (33, 16, 26, 42), four proofs (one in the fill-threshold proposition, two in the matching file's lemma and proposition, one in the consolidation proposition), no figures, tables or assets. Outside the blocks each file holds only its `% migrate-to:` line and its `\subsection` heading. Also accounted for: the folder wrapper `00_overview.tex` (four `\input` lines after order books and order flow review) and the chapter file's `\newpage`/`\input` lines for the folder, both removed, and four map rows.

### Provenance

- **Harris** (`alpha-harris`): order instructions (chap. 4, pp. 68–86), precedence, matching and trade pricing, crossing networks, price ownership and derivative-price risks (chap. 6, pp. 115–136), order choice (chap. 14, p. 304), sunshine trading (sec. 15.3, pp. 327–328), exposure (chap. 18, pp. 382–384), internal crossing (sec. 25.4, pp. 520–521), consolidation and fragmentation (chap. 26, pp. 526–534).
- **Lehalle and Laruelle** (`alpha-laruelle`): market share and its metrics (chap. 1, sec. 1.1.1, pp. 33–39), SOR (sec. 1.2, pp. 62–73), dark pools (sec. 1.4, pp. 102–115), auctions, matching curves and volume curves (chap. 2, sec. 2.1, pp. 117–140), spreads, resilience and coverage (secs. 2.3–2.4, pp. 153–163), Spain and the 2010 outage (sec. 2.5, pp. 170–185), FEI (app. A.1), the SOR toy model (A.3), market-share estimation (A.8), Gini and KS (A.9); sec. 3.4.2 was already the source of the existing routing entries.
- **Bouchaud et al.** (`catalogue-0528`): order categories and order types (pp. 45, 55), the auction price (p. 56).
- **FIX 4.4** code sets (`fix44-orchestra`): OrdType, TimeInForce, ExecInst.
- Not found in any source read: the legacy venue-selection list and routing-cost formula, frequent batch auctions' "muted" time priority (Budish et al.'s batch-auction sections not read), pegging references, the Gini for participants and time segments, leave-one-out estimators, and "subsidised share" beyond Turquoise's 2009 episode; each is marked interpretation, narrowed or stubbed.

### Ownership and dispositions

Routed by guide outcomes and map candidates. The overview `execution-market-making` (replay with acknowledgements, cancellations and fills; queue-position assumptions) owns order instructions and matching (files 01 and 04; candidates: execution-market-making, market-making-lob, market-structure-execution-quality, and for 04 futures-execution). `market-structure-execution-quality` ("fragmentation, dark trading, fees") owns dark trading and fragmentation (files 06 and 07). **Routing exception:** nine blocks of file 06 merged into `def:order-exposure-decisions` and `def:block-trade`, owned by the overview `execution-trading-costs`, which is not a candidate of the file, because those entries already hold the concepts (Harris chaps. 15 and 18); parallel entries were not written. `futures-execution`'s `conv:cme-globex-trading` gained a cross-reference only. Rejected: `market-making-lob` for matching (its outcome is queue dynamics and fill probabilities, which use the rules but do not define them).

| File | Blocks | Destination | Disposition |
|---|---|---|---|
| 02/01 | *Order*; *Order-Instruction Segmentation*; *Core Order-Type Segmentation*; *Market Order Cost Segmentation*; *Conditional Activation*; *Stops Are Not Limits*; *Tick-Sensitive Orders*; *Time-in-Force*; *Quantity and Handling*; *Special Instruction*; *Instruction Semantics Are Venue-Specific* (11) | `def:order-instructions` (new) | Rewritten from Harris chap. 4 and FIX 4.4; IOC/FOK naming conflict recorded; pegs attributed to FIX, not Harris; T+3 marked historical; venue semantics stubbed |
| 02/01 | *Marketable Limit Order* | `def:limit-order-book`, `def:order-instructions` | Merged; remainder rule (Harris p. 126) |
| 02/01 | *Order Choice Trades Certainty for Leakage*; *Market vs Limit Order Choice*; *Limit-Order Fill Threshold* (with proof); *Spread-Only Rules Fail* (4) | `res:limit-order-options` | Merged; Harris p. 304 and Table 14-1; threshold derived and computed; spread-only rule reframed by information |
| 02/04 | all 18 (principle, procedure, continuous and call matching, frequent batch auctions, pricing rules and incidence, auction rules, surplus, schedules, lemma and proposition with proofs, randomised uncrossing, priority, public order precedence, pro-rata, matching curve, indicative volume) | `mech:order-matching-pricing` (new) | Rewritten from Harris chap. 6 and Lehalle–Laruelle chap. 2; pro-rata remainders computed; frequent batch auctions stubbed (`hft-market-design`); public order precedence and random ends dated |
| 02/06 | *Dark Pool*; *Reference Price Trading*; *Crossing Network Rules*; *Price Ownership*; *Dark Liquidity Pools*; *Integrated vs Midpoint Books*; *Dark Pools and Price Discovery*; *Derivative Pricing Risks*; *Dark Activity Drivers*; *Why Investors Use Dark Pools*; *Dark Liquidity Is Conditional*; *Toxic Liquidity and Gaming*; *Bilateral vs Multilateral*; *Internal Crossing Agency* (14) | `def:dark-pools-crossing` (new) | Rewritten; "volatile periods" **qualified** (true of LL's dark turnover, not of dark share, against Buti et al. as reported); Zhu and Buti not read |
| 02/06 | *Reserve and Iceberg Display*; *Discovering Hidden Size*; *Order Exposure Decision*; *Exposure Benefit-Cost*; *Parasitic and Defensive Suppliers*; *Exposure Defence* (6) | `def:order-exposure-decisions` | Merged (routing exception); Harris pp. 84–85, 117, 382–384 |
| 02/06 | *Block Exposure-Control*; *Sunshine Trading Credibility*; *Block Hanging Over the Market* (3) | `def:block-trade` | Merged (routing exception); sunshine trading added; Table 15-1 already present |
| 02/07 | *Routing After Fragmentation*; *Smart Order Routing*; *Temporal Then Spatial*; *SOR Feedback Loop*; *Venue Selection*; *Consolidation Loop*; *Consolidation Bound* (with proof); *Aggregated Liquidity*; *Average Trade Size*; *Duplicate Liquidity*; *Transparency Is Not Certainty*; *Fragmented Routing Objective* (12) | `def:smart-order-routing` | Merged; LL sec. 1.2.1 and Harris sec. 26.4; bound derived; venue list and cost formula marked as the notes' synthesis |
| 02/07 | *Maker-Taker*; *Smart Routers vs Fee Savers*; *Rebate Effects* (3) | `res:fee-adjusted-venue-choice` | Merged |
| 02/07 | *Toy SOR Model*; *SOR Share Feedback*; *SOR Fragmentation Drivers*; *Primary-Market Variance Feedback* (4) | `mod:sor-market-share-dynamics` (new) | Rewritten; three printed slips and the first-order condition **corrected**; the "finding" reclassified as a model result |
| 02/07 | *Market Share as Routing Prior*; *Venue-Share Estimator*; *Index-Level Venue Share*; *Estimator Comparison*; *Metric Choice*; *Market Share Segmentation*; *Market Share Is Conditional*; *Intraday Non-Stationarity*; *Volume-Curve Segmentation*; *Event-Driven Volume Clustering*; *Reference Rules Create Volume* (11) | `meth:venue-market-share` (new) | Rewritten; ex-fixing formula **corrected**; Bernoulli assumption tested |
| 02/07 | *FEI*; *Fragmentation Measurement Segmentation*; *FEI Venue Count*; *Fragmentation of What*; *Coverage*; *Gini Liquidity Imbalance*; *Lorenz-Curve Gini*; *Gini Measurement Segmentation*; *KS Test*; *Venue-Share Distribution Comparison* (10) | `meth:fragmentation-concentration-metrics` (new) | Rewritten; LL's "H0 accepted ... same distribution" **corrected** to failure to reject; Gini inconsistency flagged |
| 02/07 | *Intraday Venue-Share Shape*; *Liquidity and Capitalisation*; *Why Large Caps Fragment First*; *Subsidised Share*; *Post-Trade Barriers*; *Spain*; *Spread-Share Feedback*; *Venue Quality*; *HFT Perimeter*; *Primary Outage*; *Fragmentation Needs Shared References* (11) | `ev:european-fragmentation-evidence` (new) | Rewritten with samples and periods; Spain treated as a confounded comparison |

### Sources, 2026-10-16

- `alpha-harris`, 2002 printing via macOS PDFKit (printed = PDF − 13): pp. 68–86, 115–136, 304, 327–328, 382–384, 520–521, 526–534.
- `alpha-laruelle`, 2018 printing (printed = PDF − 27): pp. 5, 33–39, 62–73, 102–115, 117–140, 153–185, 247–260, 284–292; page images of pp. 35, 255, 257, 288 and 291.
- `catalogue-0528` (printed = PDF − 19): pp. 45, 55–56.
- `fix44-orchestra` (new key): FIX 4.4 OrdStatus, ExecType, TimeInForce, OrdType and ExecInst code sets via Orchimate, retrieved 2026-10-16.
- Not read: Zhu (`wide-zhu-dark-pools`, catalogue metadata only), Moallemi and Yuan (`wide-moallemi-yuan-queue`), Buti, Rindi and Werner, Budish et al.'s batch-auction sections, O'Hara and Ye, Foucault and Menkveld, the current EU and U.S. rules, and CME's documentation (scripted access refused).

### Numerical checks

`notes/artefacts/market-structure-execution-quality/order-routing-fragmentation-checks.py` (numpy, scipy; fixed seeds; run with `/opt/homebrew/bin/python3.10`): Harris's Table 6-1 call clears 7 at 20.0 by maximum volume, surplus 1.6 against 1.0 continuously (exact fractions), Bif's average 20.15; pro-rata 18 against 10 and 20 gives 6 and 12, POSIT 1,000 and 2,000, 10 against three 3s leaves one lot after floors and 7 against 1, 1 and 100 floors the small orders to nothing; the posting threshold's sign in three cases; the ex-fixing share 0.50 against the printed 0.60; FEI 0.854 and 0.676 with an empty venue; Lorenz and mean-difference Gini agree (0.565); KS fails to reject different normals in 89 percent of 30-sample trials; the binomial standard error 0.010 against 0.047 with venue choices repeated in runs of 20; the SOR model with the described update takes (0.95, 0.03, 0.02) to (0.52, 0.27, 0.21), and at a grid optimum the size-weighted first-order terms are near equal; a cross-venue gap beyond costs.

### Checks and their limits

| Source | Passages | Limits |
|---|---|---|
| `alpha-harris` | as listed | 2002 U.S. institutions; Harris's own views on IOC/FOK naming |
| `alpha-laruelle` | as listed | European data 2006–2013; several printed slips; claims reported without sources (variance and share; HFT shares) |
| `catalogue-0528` | pp. 45, 55–56 | Definitions only |
| `fix44-orchestra` | five code sets | A third-party rendering of the Community's repository; message vocabulary, not venue behaviour |

The seven new entries and nine changed entries are *partly checked*, *draft*; **human review is outstanding**.

### Preservation

New artefacts: `notes/artefacts/execution-market-making/order-types-instructions.tex`, `matching-algorithms.tex`, `orders-matching-overview.tex` (the folder wrapper as it stood after order books and order flow review) and `microstructure-orders-chapter.tex` (the chapter file before the topic review); `notes/artefacts/market-structure-execution-quality/hidden-liquidity-dark-trading.tex`, `cross-venue-routing-fragmentation.tex` and `order-routing-fragmentation-checks.py`. The order books and order flow review snapshot `02-overview-original.tex` is unchanged. Compared by script with `git show d40d4c2:…`: each body appears once; all 108 blocks appear verbatim and in order (16, 18, 23 and 51 top-level blocks); `\item` counts 33, 16, 26 and 42 equal; `\begin`/`\end` sequences identical (48, 48, 58 and 124 commands, the four proofs included); wrapper and chapter copies byte-identical. The four artefacts compile alone without warnings, overfull or underfull boxes (2, 2, 3 and 5 pages); the routing artefact's equations were inspected by page image.

### Counts

`check_compendium.py --check`, 0 problems: 459 → 351 legacy blocks = 306 shared + 16 single-candidate + 29 assigned; `execution-market-making` legacy 339 → 231; multi-asset macro 120 unchanged. Entries 151 → 158 (definitions 50 → 52, evidence 7 → 8, mechanisms 10 → 11, methods 34 → 36, models 21 → 22). Pathway notes: `execution-market-making` 26 → 28 entries, 1 → 3 stubs; `market-structure-execution-quality` 8 → 13 entries, 4 → 7 stubs; `hft-market-design` +1 stub; `execution-trading-costs` and `futures-execution` changed entries recorded. Reading notes `alpha-harris`, `alpha-laruelle` and `catalogue-0528` extended. One new source key, `fix44-orchestra`.

### Other files

New topic file `execution-trading-costs/dark-trading-fragmentation.tex`; two entries added to `execution-market-making/order-books.tex`; extensions in `smart-order-routing.tex`, `execution-algorithms.tex`, `execution-scheduling.tex` and `futures-execution.tex`; both chapter openers; `notes/log.md`, `notes/source-review-index.md` and `compendium/README.md`.

### Build

`latexmk -g -pdf compendium.tex` exits 0: 233 pages (234 before: the legacy folder removed, entries added); no LaTeX warnings; 0 overfull and 0 underfull boxes after two long artefact paths and one opener line were reworded; the inherited `page.i` warning. Tests: 14 pass. Pages inspected as images: the chapter opener and lifecycle, order instructions, matching, venue market share, fragmentation metrics and the SOR model.

### Independent review

An integrated review by the same session after writing, with the three checkpoints, rechecked every quotation in the new and changed entries by script against the text layers and the FIX pages, the locators against printed-page offsets, and the mathematics (auction schedules, surplus, pro-rata, ex-fixing share, FEI, Gini, KS, the SOR first-order condition and update sign). Fixed before commit: the variance-feedback pitfall, which first claimed the legacy direction contradicted Lehalle and Laruelle (it does not for a noisier alternative venue; the error was calling a model result empirical), and the dark-trading pitfall, which first rejected "volatile periods" outright (it holds for dark turnover). **Human review is outstanding.**

### For review

- Merging nine dark-trading-file blocks into entries owned by `execution-trading-costs` (routing exception).
- Correcting Lehalle and Laruelle's ex-fixing formula, the A.3 update sign and the A.6 condition, and their KS conclusion, by derivation and computation without errata.
- Using a third-party rendering of the FIX Orchestra repository for FIX 4.4 values.
- Leaving pro-rata remainder rules, session carry-over and current EU dark-trading caps as stubs because the primary venue documents were not readable here.

## order matching and fragmentation review follow-up: pro-rata capacity, posting against crossing, the ex-fixing domain, fixed-weight venue-share variance and the SOR objective, 16 October 2026

Corrections to order matching and fragmentation review (`4d9d5da`), run before market design and liquidity review; the order matching and fragmentation review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label, stub or count changed (351 legacy blocks; 158 entries). Each correction is reproduced, with assertions, in the rewritten `notes/artefacts/market-structure-execution-quality/order-routing-fragmentation-checks.py` (numpy and scipy, fixed seeds; exit 0 with `/opt/homebrew/bin/python3.10`); its other results (Harris's call, POSIT, FEI, Gini, KS, the cross-venue bound) are unchanged.

1. **Pro-rata allocation, `mech:order-matching-pricing`.** The order matching and fragmentation review example "10 against three resting orders of 3 leaves one lot after floors" confused two quantities. The executable quantity is first capped by the eligible resting liquidity: 10 against 3, 3 and 3 executes 9 and leaves 1 of the *incoming* order unexecuted, which rests or cancels by its own instructions; nothing is rounded. A rounding remainder arises only when proportional shares of the executable quantity are fractional: 10 against 4, 4 and 4 gives $10/3$ each, floors of 3 and one lot for the venue's further rule. A `pro_rata()` function computes capacity, exact shares, floors, rounding remainder and incoming residual, and asserts $\text{executed}\le\min(Q,\sum q_i)$, each allocation $\le q_i$, and $\text{floors}+\text{remainder}+\text{residual}=Q$ for undersubscribed (10 vs [4,4,4]), equal (12 vs [4,4,4]) and oversubscribed (10 vs [3,3,3]) cases, plus Harris's 18 vs [10,20] and 7 vs [1,1,100].
2. **Posting against crossing, `res:limit-order-options`.** The legacy-derived threshold $p(S-A)-(1-p)M$ charged the post-fill fall $A$ to posting alone. Re-derived from explicit cash flows for the same target quantity and a common terminal mark $c_T$: crossing pays $a_0$; posting pays $b_0$ on a fill, otherwise the chase price; the gain of posting is $pS-(1-p)M$ with $S=a_0-b_0$ and $M=E[\text{chase}-a_0\mid\text{miss}]$, because a fall after a fill hits both positions equally. Examples: fill at 99 against buying at 100, marked at 97, gains +1; a miss chased at 101.5 loses 1.5. Pathwise check on 200,000 random-walk paths: $P(\text{fill})=0.432$, mean gain $-0.0457$, equal to $pS-(1-p)M$; the old formula gives $-0.3127$ ($A=+0.618$). Adverse selection now enters through $p$ and $M$; the entry states when a separate $A$ would be justified (different terminal quantities).
3. **Ex-fixing share, `meth:venue-market-share`.** "Agrees only when $m(n)=0$" was too strong. The derived $(\mathfrak M-mp)/(1-p)$ equals the printed $(1-mp)\mathfrak M/(1-p)$ exactly when $m\,p\,(1-\mathfrak M)=0$: no auction volume at the venue, no auctions, or a monopolist ($\mathfrak M=m=1$, share 1 under both). Domain stated: $0\le p<1$, $0\le m\le1$, $mp\le\mathfrak M\le mp+1-p$; undefined at $p=1$. Asserted for (0.6, 1, 0.2) → 0.5 against 0.6, (0.7, 1, 0.25) → 0.6 against 0.7, and the agreeing cases $m=0$, $p=0$ and the monopolist.
4. **Venue-share variance, same entry.** The order matching and fragmentation review entry restated Lehalle and Laruelle's $\operatorname{Var}(\hat p_k-\hat p)=(1-2w_k)p_k(1-p_k)/n_k+p(1-p)/n$ (sec. A.8.3, p. 288) without testing it. For the fixed-weight index $\hat p=\sum_jw_j\hat p_j$ with independent estimates, $\operatorname{Var}(\hat p_k-\hat p)=(1-w_k)^2\sigma_k^2+\sum_{j\ne k}w_j^2\sigma_j^2$; with dependence, $a^\top\Sigma a$ for $a=e_k-w$. The printed form replaces $\sum_jw_j^2\sigma_j^2$ by a pooled binomial variance, which has no basis for an arbitrarily weighted index: $w=(0.9,0.1)$, $p=(0.5,0.5)$, $n=(100,100)$ gives 0.00005 (simulated 0.000050) against $-0.00075$ printed with $n=200$. Sample sizes are now defined (trades per stock); count shares ($\sigma^2=p(1-p)/n$ under independent identical trials) are distinguished from value shares ($p(1-p)/n_{\text{eff}}$, $n_{\text{eff}}=(\sum v)^2/\sum v^2$; 92 of 2,000 lognormal trades, sd 0.0478 by simulation and formula). The textbook formula is recorded as an unsupported simplification.
5. **SOR objective and simulation, `mod:sor-market-share-dynamics`.** The first-order condition is now stated with its marginal value $h_k(r_k)=E[V\mathbf 1\{r_kV<D_k\}]$: equal to $\lambda$ for every venue with $r_k>0$ (interior), $h_k(0)\le\lambda$ for a venue at zero (boundary). Two-scenario counterexample ($V=1$, $D=(0.4,0.6)$; $V=10$, $D=(6,4)$, equally likely): $(0.5,0.5)$ equalises the unweighted indicators and captures 4.95; $(0.6,0.4)$ captures 5.4, the grid optimum. The order matching and fragmentation review simulation set $E[D_k]=p_k$ instead of the book's $E[D_k/\sum D]=p_k$ (eq. A.10), made $V$ depend on $D$ and used unweighted indicators; its claim to reproduce the 50/25/25 path is **withdrawn**. Replaced by an explicitly illustrative variant: $D_k=\mu_kX_k$, $X_k$ i.i.d. lognormal with $\nu=0.8$ (chosen here), $V$ independent with $E[V]=\sum\mu_k$, means calibrated each period to $E[D_k/\sum D]=p_k$ (calibrated $(0.9709, 0.0175, 0.0115)$ for $(0.95,0.03,0.02)$), $a=0.3$, projected stochastic gradient ascent with the size-weighted indicators. An exact KKT solver gives keys $(0.99888, 0.00056, 0.00056)$ with equal marginal values 0.3412 (interior); the learner's averaged keys are within 0.001. By scale invariance the optimal key is $\mu_k/\sum\mu$ (checked: means (0.6, 0.25, 0.15) give those keys), so the largest venue's key exceeds its share and the variant concentrates, to $(0.998, 0.001, 0.001)$ after 60 periods. It does not reproduce the book's path, which depends on an unreported $\nu$ and the printed update.

Source statements and derived corrections are kept apart: items 1, 2 and 5 are derivations and computations; items 3 and 4 correct the order matching and fragmentation review restatement of Lehalle and Laruelle and the book's own formula by derivation, without errata. Notes changed: `execution-market-making` and `market-structure-execution-quality` pathway notes, the `alpha-laruelle` reading note. The order matching and fragmentation review index row in `notes/source-review-index.md` keeps `4d9d5da`.

## market design and liquidity review: the foundations folder (roles of markets, participants and motives, venues, auction and dealer structures, market quality, regulation and structural evolution; six files, folder closed), 16 October 2026

### Scope

All six files of `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/` as one batch of 171 blocks (11 + 34 + 22 + 21 + 32 + 51), with the folder wrapper `00_overview.tex`. Every file listed `execution-market-making` and `market-structure-execution-quality`; none was assigned. Starting commit `4d9d5da`; the order matching and fragmentation review follow-up (above) ran first.

### Provenance

The first five files paraphrase Harris (chaps. 1, 3, 5, 7, 8, 9, 15, 19, 22, 24, 26–28) and Hasbrouck (chaps. 1–2) closely, with Lehalle and Laruelle's introduction and chap. 2 for the four liquidity variables, flow reactivity and the "Nyquist–Shannon latency bound". The regulatory file mixes Harris (chaps. 3, 9, 18, 26, 28, 29), Lehalle and Laruelle (introduction, chap. 1, sec. 2.5) and undated statements of U.S. and EU rules; every dated rule statement was rebuilt from primary texts. Legacy additions with no source found are named in each entry's Pitfalls (for example "funding" among spread components, "payoff convexity" for gamblers, the trading-edge list, "liquidity risk", "price continuity", "measurement risk", the tick-policy principle). Four legacy propositions were wrong or incomplete as stated (below).

### Ownership and dispositions

Ownership follows the two outcomes: conceptual material on markets, traders, venues and liquidity to the overview `execution-market-making` (seven new entries in a new topic file `execution-market-making/market-organisation.tex`); regulation, venue competition, dated U.S. and EU rules and circuit breakers to `market-structure-execution-quality`, whose outcome names U.S. and EU rule changes (five new entries in a new topic file `execution-trading-costs/market-regulation.tex`). Overlap was merged into twenty existing entries. **Routing exceptions** (entries owned outside the two candidates, which already held the material): `def:block-trade` and `def:order-exposure-decisions` (`execution-trading-costs`), `def:price-impact` (`price-impact-execution`), `def:hft-strategies` and `res:hft-spread-investor-cost` (`hft-market-design`). Labels are preserved; `res:insider-trading-deterrence` was retitled to include the policy debate.

| File | Blocks | Destination | Outcome |
|---|---|---|---|
| 01 | *Core Market Functions*; *Immediacy Has a Price*; *Trading Benefit Segmentation*; *Price Discovery*; *Risk Transfer*; *Capital Allocation*; *Informative Prices and Allocation*; *Mechanism Relevance*; *Microstructure Trade-Off* (9) | `def:market-functions` (new) | Rewritten from Harris chaps. 1, 3, 9 and Hasbrouck chap. 1 |
| 01 | *Zero-Sum Trading Accounting* (proposition with proof) | `res:zero-sum-skill-luck` (new) | Rewritten; the common-valuation condition stated |
| 01 | *Liquidity Provision* | `def:market-intermediaries` (new) | Merged as Harris's short list (p. 394) |
| 02 | *Trading Game View*; *Long and Short Positions*; *Motive Segmentation*; *Multiple Trader Identities*; *Patience Defines the Liquidity Side*; *Buy-Side Motives*; *Instrument Choice Follows the Problem*; *Hedge-Vehicle Fit*; *Profit-Motivated Trader Segmentation*; *Speculation Requires Comparative Advantage*; *Trading Edge Segmentation*; *Noise and Liquidity Traders*; *Futile Trader Segmentation* (13) | `def:trader-motives` (new) | Rewritten from Harris chap. 8; "payoff convexity", the edge list and the noise-trader definition flagged as legacy |
| 02 | *Skill and Luck Look Similar Ex Post*; *Past Profit Alone Does Not Identify Skill*; *Profit-Motivated Flow Needs Non-Profit Motives*; *Turnover Drag for Active Management* (4, three with proofs) | `res:zero-sum-skill-luck` | Rewritten; the skill–luck proposition **restated with conditional mean independence of luck**, the corollaries' conditions stated; simulated |
| 02 | *Liquidity Supplier Segmentation*; *Dealers and Market Makers*; *Sell-Side Intermediaries*; *Broker Service Segmentation* (4) | `def:market-intermediaries` (new) | Rewritten from Harris chaps. 3, 7, 8, 19 |
| 02 | *Information-Motivated Traders*; *Informed Trader Liquidity Role Segmentation* (2) | `def:informed-trader-types` | Merged (pp. 194–196, 402–403) |
| 02 | *Arbitrageur Economic Function* | `def:arbitrage` | Merged (pp. 6, 404–405) |
| 02 | *Block-Trading Role Segmentation*; *Block Dealers vs Block Brokers*; *Block Trader Skill Segmentation* (3) | `def:block-trade` | Merged (routing exception; pp. 328–330) |
| 02 | *Broker Agency Conflict* | `def:broker-agency-conflicts` | Merged |
| 02 | *Institutional Investors and HFTs*; *HFT Identification Markers*; *HFT as Fragmentation Link*; *Blurring of Roles* (4) | `def:hft-strategies` | Merged (routing exception; Lehalle and Laruelle, pp. 5–6, 22) |
| 02 | *Tighter Spread, Different Cost*; *Investor Size Asymmetry* (2) | `res:hft-spread-investor-cost` | Merged (routing exception) as restatements; size asymmetry flagged as legacy |
| 03 | *Venue as Rule System*; *Market-Structure Segmentation*; *Access Form Segmentation*; *Market-Centre Segmentation*; *Exchanges*; *Exchanges as Search Engines*; *OTC Markets*; *ECNs and ATSs*; *RFQ vs CLOB*; *Designated Market Maker Segmentation*; *Market Information Systems*; *Post-Trade Infrastructure*; *Brokered Credit Compression* (proposition with proof); *Architecture Choice*; *Straight-Through Processing* (15) | `def:market-structures-venues` (new) | Rewritten from Harris chaps. 3, 5, 7, 24, 26; the credit count's conventions and assumptions stated and checked |
| 03 | *Brokered Transaction Segmentation* | `def:market-intermediaries` | Merged (Table 7-1) |
| 03 | *Dark Pools, Internalizers, and Crossing Networks* | `def:dark-pools-crossing` | Merged |
| 03 | *Order-Flow Arrangement Segmentation* | `def:broker-agency-conflicts` | Merged; internal crossing and the EU payment-for-order-flow ban added |
| 03 | *Trading Systems and Technology*; *Automated Reporting Advantage* (2) | `def:floor-automated-trading-systems` | Merged (pp. 35, 97, 524–525) |
| 03 | *Stale Quotes and Vanishing Liquidity* | `def:smart-order-routing` | Merged into the latency paragraph |
| 03 | *Liquidity Bridges* | `def:hft-strategies` | Merged (routing exception) |
| 04 | *Execution-System Segmentation*; *Trading Session Segmentation*; *Continuous Auctions*; *Call Auctions*; *Fixing Auctions*; *Auction Session Segmentation*; *Dealer Markets*; *Brokered Markets*; *Hybrid Markets*; *Specialist Role Segmentation*; *Gold Fixing as Sequential Auction*; *Why Large Orders Like Calls*; *Auction Transparency Trade-Off* (13) | `def:trading-sessions-execution-systems` (new) | Rewritten from Harris chaps. 5, 24, 28 and Hasbrouck chap. 2; the gold fixing **dated** (1919–2015 from LBMA, the IBA auction as of October 2026) |
| 04 | *Open-Outcry Oral Auctions*; *Public Exposure Rule*; *Order-Driven Rule Stack*; *Priority and Access Rules* (4) | `mech:order-matching-pricing` | Merged (pp. 112–114) |
| 04 | *Floor vs Automated Auction Segmentation*; *Fast-Market Capacity Condition* (proposition with proof); *Floor Information Exchange* (3) | `def:floor-automated-trading-systems` | Merged; the capacity proposition **restated** as a necessary, not sufficient, queue-stability condition and simulated |
| 04 | *Reference Price Monopoly* | `meth:venue-market-share` | Merged (Hasbrouck p. 18) |
| 05 | *Market Quality*; *Liquidity*; *Liquidity as Bilateral Search*; *Search Stopping Rule* (proposition with proof); *Liquidity Search Strategy Segmentation*; *Four Liquidity Variables*; *Liquidity Risk*; *Tightness, Depth, and Resiliency*; *Price Continuity*; *Search-Output Liquidity Dimensions*; *Depth-Width Duality* (proposition with proof); *Displayed, Undisclosed, and Latent Liquidity*; *Book Size*; *Book Size Is a Lower Bound*; *Resiliency as Synchronisation*; *Value-Trader Resiliency*; *Liquidity State Drivers*; *Quality Trade-Offs*; *Intraday Liquidity Seasonality*; *Flow Reactivity* (20) | `def:liquidity-dimensions` (new) | Rewritten from Harris chap. 19, Hasbrouck chap. 1, Lehalle and Laruelle secs. 2.2–2.3; duality **given its attainment condition**; the search rule stated as one-step; "book size is a lower bound" **corrected** |
| 05 | *Public Benefits of Liquid Markets*; *Visible Activity vs Economic Importance* (2) | `def:market-functions` | Merged (pp. 45, 214–216) |
| 05 | *Transparency Paradox*; *Transparency Segmentation*; *Volume Is Not Directly Comparable* (3) | `def:market-structures-venues` | Merged (pp. 48, 101; Lehalle and Laruelle pp. 19–20) |
| 05 | *Latency and Book State*; *Nyquist-Shannon Latency Bound* (2) | `def:smart-order-routing` | Merged; the bound **not adopted as a theorem**: restated as a staleness condition with a computed probability |
| 05 | *Market Impact and Decay* | `def:price-impact` | Merged (routing exception) as a restatement |
| 05 | *Informational Efficiency* | `def:market-efficiency` | Merged (pp. 215–216) |
| 05 | *Bid-Ask Bounce*; *Spread and Depth Substitute Imperfectly* (2) | `res:spread-determinants` | Merged; already present, interpretations recorded |
| 05 | *Spread-Volatility Link* | `meth:spread-volatility-regression` | Merged |
| 06 | *Regulation as Market Design*; *Market-Design Question Segmentation*; *Welfare Evaluation*; *Policy Objective Segmentation*; *Regulatory Institutions*; *Regulatory Political-Economy Risks*; *Unintended Consequences*; *Regulatory-Service Segmentation* (8) | `def:market-regulation-design` (new) | Rewritten from Harris chaps. 3, 9, 26, 28 |
| 06 | *Fragmentation*; *Order-Flow Externality* (proposition with proof); *Levels of Fragmentation*; *Structural Evolution of Fragmentation*; *Post-MiFID Phases*; *Early MiFID Failures*; *Liquidity Segmentation*; *Market-Segmentation Motives*; *Technology Fragmentation*; *Cross-Market Precedence Failure*; *Consolidated Tape as Resilience*; *Competition to Merger*; *Electronification Beyond Equities* (13) | `mech:venue-competition-fragmentation` (new) | Rewritten from Harris chap. 26, Hasbrouck chap. 1, Lehalle and Laruelle; their inconsistent dates recorded; electronification also in `def:market-structures-venues` |
| 06 | *Decimalization*; *Reg NMS*; *Post-Flash-Crash Controls*; *Stub Quotes* (4) | `rule:us-equity-market-structure` (new) | Rebuilt from Federal Register, eCFR and SEC texts with adoption, effective, stay and compliance dates |
| 06 | *MiFID and MiFID II*; *Transparency and Dark Trading*; *MiFID II Dark Caps*; *MiFID Venue Statuses* (4) | `rule:eu-trading-venue-transparency` (new) | Rebuilt from EU texts (Publications Office) and ESMA statements; the double-to-single volume cap transition dated |
| 06 | *Circuit Breakers and Structural Controls*; *Circuit Breaker Scope*; *Extreme-Volatility Control Segmentation*; *Circuit Breaker Design*; *Halt Value Depends on Volatility Source* (proposition with proof); *Gravitational Effect*; *Propagation Problem*; *Price Limits and Margin Waterfall*; *Trading-Restriction Incidence* (9) | `mech:circuit-breakers-trading-halts` (new) | Rewritten from Harris chap. 28, Lehalle and Laruelle sec. 2.5.3, MiFID II Art. 48(5); the halt proposition identified as definitional |
| 06 | *Insider-Trading Restrictions*; *Insider-Trading Control Segmentation* (2) | `def:inside-information` | Merged; Rule 10b5-1 (2022 amendments), Form 4 and Regulation FD checked as of October 2026; Harris's superseded statements marked |
| 06 | *Insider-Trading Enforcement Logic*; *Insider-Trading Debate Segmentation*; *Insider-Trading Policy Trade-Off* (proposition with proof) (3) | `res:insider-trading-deterrence` | Merged (sec. 29.3); the trade-off identified as an accounting identity |
| 06 | *Exposure-Protection Rule Segmentation* | `def:order-exposure-decisions` | Merged (routing exception; p. 389) |
| 06 | *Best Execution After Fragmentation* | `def:best-execution` | Merged (Lehalle and Laruelle pp. 17–19, 43) |
| 06 | *Broker Crossing Networks* | `def:dark-pools-crossing` | Merged (pp. 18, 55–56) |
| 06 | *Tick Size Reforms*; *Tick Size as Market Share Tool*; *Sub-Penny and Tick-Size Wars*; *Who Gains From Tick Changes*; *Tick Policy Design* (5) | `def:tick-size` | Merged (Harris pp. 114, 531, 537–538; Lehalle and Laruelle p. 15); the sub-penny rule in `rule:us-equity-market-structure` |

Block total: 171 (11 + 34 + 22 + 21 + 32 + 51); none deleted without a destination; no stub replaces a block, but six backlog stubs record what the sources could not settle (below).

**Corrections to the legacy propositions.** (i) *Past profit and skill*: the proof needed $E[L_{t+1}\mid\mathcal F_t,\Pi_t]=E[L_{t+1}\mid\mathcal F_t]$; unconditional zero-mean luck does not suffice (AR(1) luck with mean zero gives a slope of 0.5), and when skill is unknown past profit is informative (slope $\tau^2/(\tau^2+\sigma^2)$). (ii) *Brokered credit*: correct as an unordered count under stated assumptions; Harris's sidebar counts ordered relationships ($2n+B(B-1)$ = 2,009,900; ratio 497,537, his "500,000"). (iii) *Depth–width duality*: needs the maximum to be attained (counterexample with a jump). (iv) *Capacity*: $N\lambda<\mu$ is necessary, not sufficient (queueing delays and bursts). The *Nyquist–Shannon latency bound* is Lehalle and Laruelle's heuristic (p. 23, page image), not a sampling-theorem result; the *halt-value* and *insider-trading trade-off* propositions are definitional; the *order-flow externality* is a rearrangement whose content is in its specification.

### Sources, 2026-10-16

- `alpha-harris` (printed = PDF − 13): pp. 3–10, 32–66, 89–115, 139–144, 176–219, 328–330, 389, 394–409, 442–454, 470–471, 494–496, 524–541, 547, 572–582, 584–598.
- `s6-hasbrouck` (printed = PDF − 11): pp. 3–6, 17–19.
- `alpha-laruelle` (printed = PDF − 27): pp. 4–9, 15–24 (page image of p. 23), 39–62, 143–149, 156–158, 177–191.
- U.S. primary texts (Federal Register PDFs via govinfo.gov; eCFR versioner API for 14 October 2026; SEC PDF via WebFetch because sec.gov returns HTTP 403 to plain scripted requests): Releases 34-42914, 34-44568, 34-51808 (first ten pages), 34-63255, 34-63241 (dates), 34-67090, 34-67091, 34-67457, 34-79318 (date), 34-85623 (date, purpose), 33-11138/34-96492 (summary, dates), 34-105656 (whole); a MEMX filing of October 2020; 17 CFR 242.612, 242.610, 242.611, 240.15c3-5, 240.10b5-1, 240.16a-3, 243.100. New source keys: `cfr-240-10b5-1`, `cfr-240-16a-3`, `cfr-242-612`, `cfr-243-100`, `sec-34-105656`, `sec-34-42914`, `sec-34-44568`, `sec-34-51808`, `sec-34-63255`, `sec-34-67090`, `sec-34-67091`, `sec-34-67457`, `sec-34-79318`, `sec-34-85623`, `sec-34-96492`, `sec-fr-2020-23011`.
- EU primary texts via the Publications Office's CELLAR service (EUR-Lex's HTML and PDF endpoints returned HTTP 202 with an empty body, a bot check that was not circumvented): Directives 2006/31/EC, 2014/65/EU (Arts. 4, 48, 49, 93), (EU) 2016/1034; Regulations (EU) No 600/2014 (Arts. 5, 55), 2016/1033, 2024/791 (recitals, Arts. 1(4) and 2, new Art. 39a). Directive 2004/39/EC itself was not retrievable in that format; its date is from 2006/31/EC. New keys: `eu-dir-2006-31`, `eu-dir-2014-65`, `eu-dir-2016-1034`, `eu-reg-2016-1033`, `eu-reg-600-2014`; Regulation 2024/791 cited through the catalogue key `ex-eu-mifir-review-2024`.
- ESMA: public statements of 27 March 2024 (`esma-transition-statement-2024`, new) and 10 October 2025 (`esma-mifir-review-statement-2025`); the double-volume-cap page (`esma-dvc-page`, new).
- LBMA centenary page and IBA auction page (`lbma-gold-centenary`, `iba-precious-metals-auctions`, new).
- Not read: the Regulation NMS compliance phases (sec. VII of the release), the 2010 single-stock circuit-breaker orders, current market-wide circuit-breaker rules after the 2020 filing, the CAT plan's later amendments and litigation, MiFID II Art. 27 and RTS 1/11, the U.K. regime, Directive 2004/39/EC's own text, Lee–Ready and other primary studies, and the empirical circuit-breaker literature.

### Numerical checks

`notes/artefacts/execution-market-making/liquidity-market-design-checks.py` (numpy, fixed seed; exit 0 with `/opt/homebrew/bin/python3.10`; about 3 s): skill and luck (slopes 0.200 against 0.200; −0.006; 0.501 for persistent luck; incremental 0.0005); zero-sum and the two corollaries (gross sum $-7\times10^{-13}$; value-weighted active return $10^{-18}$; not zero when actives do not hold the market); credit counts (Harris's 999,999,000,000 and 2,009,900, ratio 497,537; the unordered 499,999,500,000 and 1,004,950; enumeration $n=12$, $B=3$ gives 15); depth–width duality and its counterexample; Harris's camera arithmetic and a reservation-value search (0.80; net 0.8005 against 0.784 and 0.792); book-size replenishment (1,900 against 20); the latency staleness probabilities ($e^{-1}=0.368$, $e^{-2}=0.135$; 250 and 125 Hz recomputed); queueing (M/M/1 means 2, 10, 100 ms; bursts 12.5 against 3.9 ms mean, 74 against 21 ms 99th percentile; growth at utilisation 1.05); Harris's volume-counting example; the order-flow externality inequality.

### Checks and their limits

| Source | Passages | Limits |
|---|---|---|
| `alpha-harris` | as listed | 2002 U.S. institutions; several statements superseded (insider reporting, prearranged plans, DJIA halts, T+3) and marked |
| `s6-hasbrouck` | pp. 3–6, 17–19 | Definitions and auction design only |
| `alpha-laruelle` | as listed | Inconsistent dates (Turquoise, NASDAQ OMX Europe, Euronext outage, stub quotes) recorded, not resolved |
| U.S. primary texts | as listed | Federal Register first pages and dates for some releases; current MWCB and CAT status unchecked |
| EU primary texts | as listed | Original texts, not consolidated versions; RTS not read |
| ESMA, LBMA, IBA pages | as listed | Living pages, as retrieved 2026-10-16 |

The twelve new entries and twenty changed entries are *partly checked*, *draft*; **human review is outstanding**.

### Preservation

New artefacts: `notes/artefacts/execution-market-making/roles-of-financial-markets.tex`, `market-participants-trading-motives.tex`, `trading-venues-market-architecture.tex`, `auction-dealer-market-structures.tex`, `market-quality-efficiency.tex`, `market-foundations-overview.tex` (the folder wrapper) and `microstructure-foundations-chapter.tex` (the chapter file before the topic review); `notes/artefacts/market-structure-execution-quality/regulatory-structural-evolution.tex`. Compared by script with `git show 4d9d5da:…`: each file body appears once; all 171 blocks appear verbatim, once and in order (11, 34, 22, 21, 32, 51); `\item` counts 8, 65, 41, 32, 32, 99 equal; `\begin`/`\end` sequences identical (28, 98, 62, 56, 80, 144 commands, proofs included); wrapper and chapter copies byte-identical. The six artefacts compile alone with no warnings and no overfull or underfull boxes (1, 4, 3, 2, 3 and 6 pages).

### Counts

`check_compendium.py --check`, 0 problems: 351 → 180 legacy blocks = 135 shared + 16 single-candidate + 29 assigned (306 → 135 shared; 16 and 29 unchanged); `execution-market-making` legacy 231 → 60; multi-asset macro 120 unchanged. Entries 158 → 170 (definitions 52 → 59, mechanisms 11 → 13, results 19 → 20, rules 1 → 3). Pathway notes: `execution-market-making` 28 → 35 entries; `market-structure-execution-quality` 13 → 18 entries, 7 → 10 stubs (the tick-regime stub narrowed to the EU regime; the EU dark-cap stub, now answered by `rule:eu-trading-venue-transparency`, replaced by four: EU waiver thresholds, current U.S. market-wide circuit breakers, CAT status and circuit-breaker evidence); `execution-trading-costs`, `price-impact-execution` and `hft-market-design` record the routing-exception changes. Reading notes `alpha-harris`, `alpha-laruelle` and `s6-hasbrouck` extended. Twenty-five new source keys.

### Other files

Two new topic files (`execution-market-making/market-organisation.tex`, `execution-trading-costs/market-regulation.tex`) and their inputs; both chapter openers; the legacy chapter file (the foundations input removed, its overview sentence updated); `compendium/front/sources.tex`; `notes/log.md` (two open questions); `notes/source-review-index.md` (status, index, the topic review, six map rows removed); `compendium/README.md`.

### Build

`latexmk -g -pdf compendium.tex` exits 0: 236 pages (233 before); no LaTeX warnings; 0 overfull and 0 underfull boxes after one *Further reading* line was reworded; the inherited `page.i` warning. Tests: 14 pass. Pages inspected as images: the new section openers and the regulation entries.

### Independent review

An integrated review by the same session after writing. Every quotation in the new and changed text (215) was checked by script against the text layers, the downloaded primary texts and the legacy files at `4d9d5da`; about 140 phrases were located to their printed pages to check locators. Fixed before commit: a sentence that attributed to Harris the legacy remark that smoothing prices against informed flow "only transfers losses to liquidity suppliers" (now marked as the legacy notes' interpretation); the broker-services pitfall, which first said the legacy list added clearing and settlement (Harris's first item); a misquoted legacy phrase ("weaken" for "weakens"); the LULD band sentence (bands of 5 and 10 percent apply above $3.00 after the May 2012 amendment); and an underfull *Further reading* line. **Human review is outstanding.**

### For review

- The ownership split between the overview (conceptual) and `market-structure-execution-quality` (rules, competition, circuit breakers), and the five routing exceptions.
- The restated skill–luck proposition and the reading of Harris's credit count as ordered.
- Treating Lehalle and Laruelle's "Nyquist–Shannon latency bound" as a heuristic, not a theorem.
- Using the EU Publications Office's CELLAR service and WebFetch for SEC PDFs where EUR-Lex and sec.gov refuse plain scripted requests; no bot check was solved or bypassed.
- The compliance status of the U.S. 2024 tick and fee amendments (exempted to November 2027) and the EU single volume cap, which change often.

## market design and liquidity review follow-up: liquidity units, the current systematic-internaliser definition and U.S. currency, queue stability and bursts, and preservation counts, 16 October 2026

Corrections to market design and liquidity review (`063de31`), run before dealer models and information review; the market design and liquidity review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label or entry count changed (180 legacy blocks; 170 entries); one backlog stub was added and one narrowed (item 2). Numerical corrections are reproduced, with assertions, in the rewritten sections 4 and 8 of `notes/artefacts/execution-market-making/liquidity-market-design-checks.py` (numpy; fixed seeds; exit 0 with `/opt/homebrew/bin/python3.10`); its other sections give byte-identical output (compared by script with the output before the change).

1. **Liquidity dimensions, `def:liquidity-dimensions`.** Harris states width as "the cost per unit of liquidity" and depth as "measured in units available at a given price of liquidity" (pp. 398--399, rechecked). The market design and liquidity review entry wrote $D(c)=\max\{q:C(q)\le c\}$ with $C$ an all-in (total) cost and $c$ a "cost budget", and its script inverted a cumulative cost: that answers a cash-budget question, not Harris's. Counterexample: midpoint 99, 100 shares offered at 100: per-unit cost 1, depth at per-unit cost 1 is 100 shares; inverting total cost at a budget of 1 gives one share. The entry now defines a size domain (positive lot multiples or $[q_{\min},\bar q]$; per-unit cost undefined at zero), the per-unit cost $w(q)$ in currency per share, depth $D(\bar w)$ in shares and total cost $C(q)=q\,w(q)$ with a budget $K$ as a separate object; distinguishes average from marginal per-unit cost (depth at 1.5 is 200 against 100 shares with 100 more at 101); notes that a fixed fee per order makes $w$ fall with size, so the equivalence can fail (feasible set {100} at 1.5 with a fee of 50, while $w(50)=2$); and states attainment correctly: on an interval the maximum exists if and only if the feasible set is nonempty, bounded and contains its supremum; a compact domain with $w$ lower semicontinuous suffices, lower semicontinuity is not necessary (an upward jump at 2 with the maximum 1 attained) and does not give a finite maximum without boundedness. Source statement (the per-unit units and the duality) and interpretation (the formalisation) are kept apart.
2. **Systematic internaliser and U.S. currency, `rule:eu-trading-venue-transparency` and `rule:us-equity-market-structure`.** The 2014 definition ("organised, frequent systematic and substantial basis", pre-set quantitative limits for both, opt-in already available) is now dated as historical. The current definition is quoted from Directive (EU) 2024/790, Art. 1 point (3)(b): "on an organised, frequent and systematic basis, deals on own account in equity instruments \dots\ or which opts in"; recital (7) gives the reasons (excessive burden of the quantitative criteria; qualitative assessment for equity instruments only; non-equity pre-trade transparency removed for systematic internalisers by Regulation (EU) 2024/791; opt-in possible for non-equity instruments), and Commission Delegated Regulation (EU) 2026/392, recital (1), reads it the same way. Dates: the directive of 28 February 2024, published 8 March 2024, in force on the twentieth day, transposition due 29 September 2025 (Arts. 2--3), national measures not checked; the delegated regulation of 20 February 2026, published 1 June 2026, in force on the twentieth day (Art. 2). U.S.: Release 34-104612 (15 January 2026) exempts the plan participants from Rule 600(b)(69)(ii), aggregate odd-lot depth at or between the NBBO, until the first business day of May 2028, and not from Rule 600(b)(69)(iii), the best odd-lot order; Release 34-94441 (16 March 2022) approved NYSE's market-wide circuit breakers on a permanent basis, with Amendment No. 1's testing and reporting duties (other venues' 2022 filings not read); the 2024 tick and fee amendments took effect on 9 December 2024 (Federal Register record) and are effective rule text whose compliance Release 34-105656, read in full in its Federal Register version, exempts to the first business day of November 2027. Six source keys added or updated: `eu-dir-2024-790`, `eu-reg-del-2026-392`, `fr-2024-21867`, `sec-34-104612`, `sec-34-94441`, `sec-34-105656` (updated).
3. **Queue stability and bursts, `def:floor-automated-trading-systems`.** For the M/M/1 queue the legacy condition $\mu>N\lambda$ is necessary and sufficient for stability; market design and liquidity review called it "necessary, not sufficient", conflating stability with delay. The entry now separates stability from waiting time ($\rho/(\mu-N\lambda)$), time in system ($1/(\mu-N\lambda)$) and deadline misses ($e^{-(\mu-N\lambda)d}$), and replaces "peak, not average, rates decide" with conditions on burst duration, backlog, buffering and deadlines. The market design and liquidity review burst simulation drew each gap from the rate at the previous arrival, inexact across rate boundaries; reproduced, its realised rate was 799.8 per second against the stated 798, and it did not separate waits from time in system. Section 8 now samples arrivals by thinning (exact for the piecewise-constant rate), sets the low rate so the average is exactly 0.8 of capacity (0.7222 of capacity outside bursts; realised 800.2 per second), checks the constant-rate case against the M/M/1 formulas (mean wait 3.94 against 4.00 ms, mean time in system 4.94 against 5.00 ms, 99th percentiles 20.6 and 21.7 against 21.9 and 23.0 ms, $P(T>10\text{ ms})$ 0.131 against 0.135, all asserted), and reports the bursts (mean wait 12.53 ms, time in system 13.53 ms, 99th percentile 72.9 ms, share over 10 ms 0.343; backlog at the end of a burst near the fluid 50 messages), shorter bursts at the same peak and average (99th percentiles 25.8 and 22.5 ms for 20 and 5 ms bursts), a finite buffer of 20 (4.8 percent rejected with bursts, 0.29 percent at a constant rate against 0.23 percent in the M/M/1/20 formula) and overload at 1.05 (waits of 2.5 and 4.6 s after 50 and 100 s). Every affected number in the entry was refreshed.
4. **Preservation metadata.** The market design and liquidity review record counted `\itemsep` as `\item`: its "8, 65, 41, 32, 32, 99" are the naive counts. Counting `\item` not followed by a letter, by script against `4d9d5da`, the six files have 6, 53, 33, 26, 26 and 81 items, 225 in all (52 `\itemsep` excluded). Rechecked by script against the artefacts: each file body occurs once; all 171 top-level blocks occur verbatim, once and in order (11, 34, 22, 21, 32, 51); item counts and `\begin`/`\end` sequences (28, 98, 62, 56, 80, 144 commands; 11 proofs) match; the folder-wrapper and chapter snapshots are byte-identical. The market design and liquidity review preservation result is otherwise confirmed.

Source statements and derived corrections are kept apart: items 1 (units) and 2 restate sources more exactly; items 1 (attainment), 3 and 4 are derivations, computations and counts. Notes changed: the `execution-market-making` and `market-structure-execution-quality` pathway notes (two backlog stubs updated or added: `rule:us-market-wide-circuit-breakers-current` narrowed, `rule:eu-si-national-transposition` new). The market design and liquidity review index row in `notes/source-review-index.md` keeps its commit.

## dealer models and information review: the rest of the legacy microstructure chapter (market making; information and volatility; feature and data engineering; eight files, chapter closed), 16 October 2026

A single batch of 60 blocks from `compendium/legacy/execution-market-making/`, run after the market design and liquidity review follow-up (above), with three review groups: market making (25 blocks), information and volatility (11) and feature and data engineering (24). It closes the legacy chapter. Migration and source checking, not study.

### Scope

Counted by script against the starting commit `063de31`: 60 top-level blocks in eight files (`05_.../01_economics_of_market_making.tex` 9, `05_.../04_optimal_quoting_and_inventory_control.tex` 2, `05_.../05_latency_and_queue_competition.tex` 7, `05_.../06_cross_asset_and_cross_venue_market_making.tex` 7, `03_.../02_price_discovery.tex` 3, `03_.../08_volatility_and_liquidity_interaction.tex` 8, `04_.../08_feature_engineering_for_microstructure_alpha.tex` 6, `04_.../09_microstructure_data_engineering.tex` 18); 85 `\item` commands (26, 0, 5, 11, 0, 10, 15, 18; `\itemsep` excluded); 158 `\begin`/`\end` commands; one proof (*Power Is a Signal-to-Noise Problem*); no figures, tables or other assets. Before the risk models review blocks were assigned (11 to `execution-market-making`, 15 to `hft-market-design`, 3 to `market-structure-execution-quality`), 6 were single-candidate (`lob-deep-learning`) and 25 shared. Also accounted for: the three folder wrappers (`03_`, `04_`, `05_.../00_overview.tex`), the chapter file `section.tex`, its line in `compendium/legacy/part.tex`, the earlier `% migrated:` comments kept in four files, and eight map rows.

### Provenance

- **Market making.** The economics and optimal-quoting files paraphrase Harris chap. 13 (dealers, pp. 278--283), chap. 16 (p. 344) and chap. 24 (specialists, pp. 495--511, the tick-size box on p. 500); the participation-option inequality is the legacy notes' formalisation of p. 499. **The latency file's unidentified source is now identified**: Lehalle and Laruelle's app. A.2 (pp. 250--254, page images of pp. 252--253), a summary of Foucault, Kadan and Kandel (2009 working paper; not read); its "latency as queue option" is unsourced, and checked against Moallemi and Yuan (`wide-moallemi-yuan-queue`, previously unread; the June 2017 revision read in part). The cross-asset file paraphrases Harris chap. 17 (pp. 349--378).
- **Information and volatility.** Lehalle and Laruelle sec. 2.5 (pp. 169--186) and app. A.5 (pp. 261--266, page images), with the 2010 CFTC--SEC staff report (executive summary) for the event and Hasbrouck chap. 10 for price discovery across venues.
- **Feature and data engineering.** The feature file has no source; its blocks are relative-value arbitrage material in Harris's terms (chap. 17), a comparative-advantage principle (Harris p. 196) and label design (López de Prado chap. 3). The data-engineering file follows Lehalle and Laruelle's apps. A.8, A.10 and A.14 (proportions, regression, the averaging effect), Harris chap. 22 (tests of skill and luck, unattributed in the legacy notes) and, for feeds and identifiers, matches Velu, Hardy and Nehren chaps. 1 and 11; drop copies, clearing feeds and the identifier attribute list are the legacy notes'. No block of either file states a multilevel or cross-asset OFI result.

### Ownership and dispositions

Routed by the guide's outcomes. The 29 assigned blocks stayed with their pathways. **Routing exceptions** (all recorded here and in the pathway notes): the cross-asset file (candidates `market-making-lob`, `hft-market-design`) to `execution-market-making`'s `def:arbitrage` and `res:arbitrage-risks`, because its blocks are Harris's arbitrage material, neither inventory hedging across venues nor latency races, and the entries already held it (FX triangles and derivative conversion included; `fx-dealer-market-making` cross-references the cyclic band); the feature file (single candidate `lob-deep-learning`) to `res:arbitrage-risks`, `def:trader-motives` (both `execution-market-making`) and `meth:triple-barrier-labelling` (`statistical-learning-foundations`), with one block a `lob-deep-learning` stub; the data-engineering file (candidates `lob-deep-learning`, `market-simulation`) to `point-in-time-data` (identifiers, feeds, timestamps and availability: the pathway's outcome is a decision-time panel), `market-structure-execution-quality` (`meth:venue-market-share`), `execution-market-making` (`meth:spread-volatility-regression`) and a new `performance-manager-evaluation` entry (Harris's tests of skill against luck, that pathway's outcome); only *Averaging Effect* went to a candidate (`market-simulation`). Seven new entries; fourteen existing entries changed (`mech:bubble-crash-dynamics` only in its See also, which pointed to the removed chapter).

| File | Blocks | Destination | Disposition |
|---|---|---|---|
| 05/01 | *Dealer*; *Dealer Problem Segmentation*; *Dealer Quote Segmentation*; *Order-Flow Acquisition Segmentation*; *Preferencing and Payment for Order Flow*; *Trading with Dealers* (6) | `def:dealer-quotes-order-flow` (new) | Rewritten from Harris chap. 13; compensation list and "wide quote is information" marked as the notes' interpretation; 2002 U.S. figures dated |
| 05/01 | *Designated Market Maker Obligation Segmentation*; *Specialist Privilege Segmentation* (2) | `def:specialist-obligations-privileges` (new) | Rewritten from Harris chap. 24 (as of 2002); current DMM rules stubbed |
| 05/01 | *Dealer Spread vs Outside Spread* | `def:outside-spread` | Merged as a restatement (pp. 344--345) |
| 05/04 | *Specialist Participation Option* (model); *Tick Size and Participation* (2) | `def:specialist-obligations-privileges` | Merged; the inequality marked as interpretation of p. 499; the tick-size box (p. 500) |
| 05/05 | *Latency as Queue Option* | `res:queue-position-value` (new) | Rewritten from Moallemi and Yuan; "thin queues" **contradicted** (value is large in long, large-tick queues) |
| 05/05 | *HFMM and Investor Race Model*; *Race Intensity*; *Latency-Cost Segmentation*; *Efficient Maker Fee*; *Fee Rebates Are Comparative*; *Queue Competition Diagnostic* (6) | `mod:make-take-fee-speed-race` (new) | Rewritten; source identified (LL app. A.2); "averages" **corrected** to sums; eq. (A.4) re-derived as the trade-maximising split and checked; printed slips recorded; cost list and diagnostic marked as interpretation |
| 05/06 | *Arbitrageurs as Cross-Sectional Dealers*; *Cross-Asset Arbitrage Segmentation*; *Triangular FX No-Arbitrage*; *Derivative Conversion* (4) | `def:arbitrage` | Merged (routing exception); the equality restated as a bid--ask band, derived and checked; Harris's currency box found inconsistent and recomputed |
| 05/06 | *Legging and Synchronisation Risk*; *Balanced Arbitrage Execution*; *Arbitrage Capital Constraint* (3) | `res:arbitrage-risks` | Merged (routing exception; pp. 366--367); the capital generalisation marked |
| 03/02 | *Fragmentation and Price Formation* | `mech:venue-competition-fragmentation` | Merged; Hasbrouck's information shares; general claim marked as synthesis |
| 03/02 | *Fast Liquidity and Price Discovery* | `mod:make-take-fee-speed-race` | Merged; LL's question about fee schedules and the PFP; the claim marked as interpretation (the model has no price discovery) |
| 03/02 | *Outage Price Discovery* | `ev:european-fragmentation-evidence` | Merged; the Euronext outage of 13 October 2010 (pp. 183--186); caption date recorded |
| 03/08 | *Liquidity Spiral*; *Depth-Driven Flash Crash Toy Model*; *Hot-Potato Amplification*; *Flash-Crash Control Segmentation* (4) | `mod:depth-overflow-flash-crash` (new) | Rewritten; **the time term resolved by derivation** (rounds, the overflow bound, (A.14) needs the overflow); the legacy $\rho$ wording corrected; control list marked as synthesis |
| 03/08 | *Flash Crash Mechanism*; *Shock Propagation Channels* (2) | `ev:may-2010-flash-crash` (new) | Rewritten from the staff report and LL; the reference-price channel placed with the Euronext outage |
| 03/08 | *Systemic Risk Link* | `mech:venue-competition-fragmentation` | Merged (LL pp. 169, 177); conditions marked as plausible mechanisms |
| 03/08 | *Trade Count as HFT Proxy* | `def:hft-strategies` | Merged (LL pp. 20--21, 170--171; the report's volume warning) |
| 04/08 | *Relative-Value Feature Segmentation*; *Factor-Residual Arbitrage View* (2) | `res:arbitrage-risks` | Merged (routing exception); the factor decomposition **corrected** for a hedge ratio $h$ |
| 04/08 | *Alpha Needs Comparative Advantage* | `def:trader-motives` | Merged (routing exception; p. 196) |
| 04/08 | *Microstructure Alpha Evaluation Segmentation* | stub `meth:lob-signal-transaction-usefulness` (`lob-deep-learning`) | Stubbed; no source read |
| 04/08 | *Arbitrage Labels Need Path Information*; *Arbitrage Event Label Segmentation* (2) | `meth:triple-barrier-labelling` | Merged (routing exception; AFML p. 44); legacy categories marked |
| 04/09 | *Market-Data Depth Segmentation*; *Trading-Message Segmentation* (2) | `data:market-data-levels` | Merged (routing exception); timestamps, sequencing, availability and corrections added from Hasbrouck p. 105; Velu chap. 11; drop copies and clearing feeds marked as the notes' |
| 04/09 | *Ticker Is Not an Instrument Key* | `data:trading-reference-data` | Merged (routing exception) |
| 04/09 | *Microstructure Proportion*; *Bernoulli Proportion Estimator*; *Normal Approximation Boundary*; *Sampling Unit Segmentation* (4) | `meth:venue-market-share` | Merged (routing exception; LL A.8); the rule of thumb stated with the true $p$; Wald and Wilson coverage computed |
| 04/09 | *Simple Linear Regression Baseline*; *Regression Fit Quality*; *Regression Is an Empirical Approximation*; *Average of Regressions vs Regression of Averages* (4) | `meth:spread-volatility-regression` | Merged (routing exception; LL A.10, A.14.2); the two $R^2$ forms distinguished; the spread identity limited to price units; LL's $\bar a_1$ slip recorded |
| 04/09 | *Mean Excess-Return Test*; *Power Is a Signal-to-Noise Problem* (proposition with proof); *More Ticks Are Not More History*; *Performance-Inference Bias Segmentation*; *Regression to the Mean*; *Distributional Shape Matters* (6) | `meth:skill-luck-significance-tests` (new, `performance-manager-evaluation`) | Rewritten from Harris chap. 22 (routing exception); the proposition restated with its error rates; Harris's tables recomputed; look-ahead and fillability pointed to their entries |
| 04/09 | *Averaging Effect* | `meth:intraday-deseasonalisation` | Merged (LL A.14.1) |

Block total: 60 (25 + 11 + 24); none deleted without a destination; one block became a backlog stub.

**Corrections to legacy claims.** (i) *Latency as queue option*: "thin" queues reversed. (ii) *Race intensity*: $\bar\mu,\bar\tau$ are sums. (iii) *Triangular FX*: an equality after costs is a band. (iv) *Factor-residual view*: exposure $\beta_i-h\beta_j$, not $\beta_i-\beta_j$. (v) *Normal approximation boundary*: the rule uses the true $p$. (vi) *Average of regressions*: the spread identity holds for price-unit spreads only. (vii) *Power*: $n=((z_{1-\alpha}+z_{1-\beta})\sigma/\mu)^2$, the expected-$t$ statement large-sample only. Source slips recorded, not silently fixed: Harris's currency box (p. 357); Lehalle and Laruelle's A.2 indices and cost scaling, its "$\Gamma-\bar c$ obviously larger than $s\Delta$", A.5's round-indexed $t$ and (A.14), A.14.2's $\bar a_1$, and the outage captions' date.

### Sources, 2026-10-16

- `alpha-harris` (printed = PDF − 13): pp. 278--283, 344--345, 354--357 (page image of p. 357), 366--367, 452--474, 495--511.
- `alpha-laruelle` (printed = PDF − 27): pp. 20--21, 169--186 (figure captions pp. 185--186), 250--254 (page images of pp. 252--253), 261--266 (page images), 284--286, 292--298, 318--321.
- `s6-hasbrouck` (printed = PDF − 11): pp. 99--105.
- `s3-velu` (printed = PDF − 17): pp. 383--386.
- `wide-moallemi-yuan-queue`: the authors' working paper, June 2017 revision (the catalogue records 2016), pp. 1--6 and 18--25.
- `alpha-afml`: p. 44 (already read in financial data and labels review).
- New source key `sec-cftc-may6-2010`: the staff report of 30 September 2010 from the CFTC's site (sec.gov returned HTTP 403 to a plain request; the CFTC copy was used, nothing circumvented), cover and pp. 1--7.
- Not read: Foucault, Kadan and Kandel; Kirilenko et al. and Menkveld--Yueshen; the staff report's detailed sections; Gliner and Drobny (not needed here); current designated-market-maker rules; multilevel and cross-asset OFI papers (`wide-cont-cross-impact-ofi`, `wide-kolm-deep-ofi`); Agresti and Caffo; the pathway readings of `performance-manager-evaluation`, `point-in-time-data` and `lob-deep-learning`.

### Numerical checks

`notes/artefacts/execution-market-making/dealer-queue-information-checks.py` (numpy, scipy; fixed seed; exit 0 with `/opt/homebrew/bin/python3.10`; about 1.5 s), each with assertions: Harris's inside spread (0.10 from five 0.50 spreads); Harris's currency box (121, not 100, yen per euro; the printed cycle loses 0.1 million yen; a consistent cycle gains 0.1 million, about \$909) and the cyclic band (20,000 random quote sets, exact agreement between "a cycle earns money" and "the direct quote leaves the synthetic band"); eq. (A.4) against exact finite-population equilibria (0.4463, 0.4429, 0.4425 against 0.4425) and the rebate signs; a counterexample to "$\Gamma-\bar c$ obviously larger than $s\Delta$"; the hot-potato sums (rounds; overflow gap up to 3.75 $r_0$ at $\rho=0.6$) and the time term by simulation (2.459 against 2.455 linear; 1.210 against 1.205 quadratic); the staff report's arithmetic (an index near 1,090; about 55,000 contracts in 14 seconds); Moallemi and Yuan's Table 3 gaps; Wald and Wilson coverage; Harris's power and data tables (0.157, 0.229; 22.3, 132.6, 33.1, 33.1 and 5.6 years), sampling frequency (mean $t$ 0.91 monthly, 0.90 daily), AR(1) standard errors (1.36), the best of many managers (0.37 and 3.6 percent against Harris's 0.5 and 5), regression to the mean (0.20) and a short-volatility stream; the two $R^2$ forms, price-unit and basis-point spread aggregation, subadditive index volatility, index against average slopes (3.108 against 2.507), LL's $\bar a_1$ slip, mean against path; and a hedged spread's factor exposure and variance.

### Checks and their limits

| Source | Passages | Limits |
|---|---|---|
| `alpha-harris` | as listed | U.S. institutions as of 2002; the currency box inconsistent; the Buffett box's method unstated |
| `alpha-laruelle` | as listed | Its A.2 summarises an unread paper; A.5 is illustrative and unestimated; several printed slips |
| `s6-hasbrouck` | pp. 99--105 | Method and data advice, no venue evidence |
| `s3-velu` | pp. 383--386 | One firm's order path; no drop-copy or clearing-feed detail |
| `wide-moallemi-yuan-queue` | pp. 1--6, 18--25 | Working paper; sec. 3 not checked; U.S. large-tick names, August 2013 |
| `sec-cftc-may6-2010` | cover, pp. 1--7 | Executive summary only; staff findings, no Commission view |

The seven new entries and fourteen changed entries are *partly checked*, *draft*; **human review is outstanding**.

### Preservation

New artefacts: `notes/artefacts/execution-market-making/economics-of-market-making.tex`, `optimal-quoting-inventory-control.tex`, `cross-asset-cross-venue-market-making.tex`, the wrappers `03-`, `04-` and `market-making-overview.tex`, the chapter file `microstructure-dealers-chapter.tex` and `dealer-queue-information-checks.py`; `notes/artefacts/hft-market-design/latency-queue-competition.tex` and `volatility-liquidity-flash-crash.tex` (a new folder); `notes/artefacts/market-structure-execution-quality/price-discovery-fragmentation-outage.tex`; `notes/artefacts/lob-deep-learning/feature-engineering-microstructure-alpha.tex` and `microstructure-data-engineering.tex`. Compared by script with `git show 063de31:…`: each file body (below its `% migrate-to:` line, the subsection starred, earlier `% migrated:` comments included) occurs exactly once; all 60 top-level blocks occur verbatim, once and in order (9, 2, 7, 7, 3, 8, 6, 18); `\item` counts (26, 0, 5, 11, 0, 10, 15, 18; 85) and `\begin`/`\end` sequences (30, 4, 16, 18, 6, 20, 18, 46; 158, the one proof included) match; the three wrappers and the chapter file are byte-identical. No asset was referenced. The eight artefacts compile alone without warnings or overfull or underfull boxes (2, 1, 1, 1, 1, 1, 1 and 2 pages). Only then were the eight files, the three wrappers and the chapter file deleted and the chapter's line removed from `compendium/legacy/part.tex`; the two sources cited only by the chapter's introduction (`demsetz-1968`, `madhavan-2000`) stay in the register, as the snapshot cites them.

### Counts

`check_compendium.py --check`, 0 problems: 180 → 120 legacy blocks = 110 shared + 10 single-candidate + 0 assigned (shared 135 → 110, single-candidate 16 → 10, assigned 29 → 0); `execution-market-making` legacy 60 → 0; multi-asset macro 120 unchanged. Entries 170 → 177 (definitions 59 → 61, evidence 8 → 9, methods 36 → 37, models 22 → 24, results 20 → 21). Pathway notes: `execution-market-making` 35 → 37 entries, 3 → 4 stubs; `hft-market-design` 3 → 7 entries, 1 → 3 stubs; `performance-manager-evaluation` 2 → 3 entries; `lob-deep-learning` 2 → 3 stubs; `point-in-time-data` 3 → 4 stubs; `market-structure-execution-quality` 10 → 11 stubs (one from the follow-up); changes recorded in `market-making-lob`, `market-simulation`, `statistical-learning-foundations` and `fx-dealer-market-making`. Reading notes `alpha-harris`, `alpha-laruelle`, `s6-hasbrouck` and `s3-velu` extended; `wide-moallemi-yuan-queue` opened. One new source key in the topic review (`sec-cftc-may6-2010`), six in the follow-up.

### Other files

Entries in `execution-market-making/market-organisation.tex`, `high-frequency-trading.tex`, `market-making-models.tex`, `order-flow-statistics.tex`; `execution-trading-costs/market-regulation.tex`, `dark-trading-fragmentation.tex`; `research-engineering-validation/point-in-time-data.tex`; `ml-alternative-data/labelling-sample-weights.tex`; `portfolio-construction-risk/performance-evaluation.tex`; five chapter openers (three `\ref`s to the removed legacy chapter replaced); `compendium/front/sources.tex`; `compendium/legacy/part.tex`; `compendium/README.md`; `notes/log.md` (coverage rows for market design and liquidity / dealer models and information reviews, three open questions answered, five added); `notes/source-review-index.md` (status, index, the topic review, eight map rows removed).

### Build

`latexmk -g -pdf compendium.tex` exits 0: 240 pages (236 before); no LaTeX warnings; 0 overfull and 0 underfull boxes after four long artefact paths were shortened; the inherited `page.i` warning. Tests: 14 pass. Pages inspected as images: the liquidity-dimensions conditions, the dealer and specialist entries, the queue-value, fee-race, toy-model and Flash Crash entries, the skill-and-luck entry, the arbitrage entries, the U.S. and EU rules, the market-data entry and the regression entry. The committed PDF was rebuilt from the final sources.

### Independent review

An integrated review by the same session after writing, against the diff. Every quotation on added lines (181 distinct) was checked by script against the text layers of the sources and the legacy files at `063de31`; the misses were pre-existing quotations on modified lines, metadata strings checked by eye, or math stripped by the script, except two of the topic review, fixed: Harris's "by decreasing the cost of stepping in front of booked orders" (the draft had "decreases") and the legacy "follows volume mechanically". Locators were checked against the printed-page offsets. Also fixed: a generalisation that the index slope "is steeper" (now what the simulation and a derivation show), the claim that Harris "does not discuss" ETFs or ADRs (limited to his arbitrage chapter), the opt-in described as new in the follow-up's first draft (it was already in the 2014 text), a Delegated Regulation citation narrowed to its recital, a pathway-note layout that counted other pathways' entries, and three `\ref`s to the removed chapter. **Human review is outstanding.**

### For review

- The routing exceptions: the cross-asset file to `execution-market-making`'s arbitrage entries; the feature file away from `lob-deep-learning`; the data-engineering file to `point-in-time-data`, `performance-manager-evaluation`, `market-structure-execution-quality` and `execution-market-making`.
- Reading eq. (A.4) as the trade-maximising fee split, and the resolution of (A.14)'s time term, both by derivation without the original paper or errata.
- Correcting Harris's currency box, and the Buffett-box probabilities not reproduced exactly.
- Using Moallemi and Yuan's 2017 revision where the catalogue records 2016, and the staff report's executive summary only.

## dealer models and information review follow-up: the triangular no-arbitrage band, 16 October 2026

Correction to dealer models and information review (`ca6986e`), run before macro markets and pricing review; the dealer models and information review record above is left as written. No legacy block, entry label or entry count changed (120 legacy blocks; 177 entries).

1. **Triangular FX arbitrage, `def:arbitrage`.** dealer models and information review kept an exact triangular equality of cross rates alongside the bid--ask band. The equality holds only in the frictionless case (single prices, no costs); with quotes, the synthetic and direct midpoints can differ while both executable cycles lose. The entry now restricts the equality to that case. Check: EUR/USD 1.0999/1.1001, USD/JPY 109.99/110.01 and EUR/JPY 120.99/121.03 give a synthetic bid and ask of 120.978 and 121.022 and a synthetic midpoint of 121.00 against a direct midpoint of 121.01; the direct bid (120.99) is below the synthetic ask and the direct ask (121.03) above the synthetic bid, so the quotes overlap the synthetic band, and the two cycles return 0.99957 (via USD) and 0.99974 (via JPY) per euro, both below one. Reproduced, with assertions, in section 2 of `notes/artefacts/execution-market-making/dealer-queue-information-checks.py` (exit 0 with `/opt/homebrew/bin/python3.10`; the script's other sections and its random draws unchanged).

Notes changed: the `execution-market-making` and `fx-dealer-market-making` pathway notes; the entry's *Status*. The dealer models and information review index row in `notes/source-review-index.md` now carries its commit, `ca6986e`.

## market design and liquidity review follow-up (second): dimensionally consistent liquidity cost, 16 October 2026

A second correction to market design and liquidity review (`063de31`), after the first follow-up above; earlier records are left as written. No legacy block, entry label or entry count changed.

1. **Liquidity dimensions, `def:liquidity-dimensions`.** The entry's per-unit width $w(q)$ and total cost $C(q)$ were not stated in consistent units. It now says: with $w$ in currency per share, $C(q)=q\,w(q)$; with $w_{bp}$ in basis points of the midpoint $m$, $w=m\,w_{bp}/10{,}000$ and $C(q)=q\,m\,w_{bp}/10{,}000$. Check: 100 shares at a midpoint of 100 and a cost of 10 bp give a cash cost of 10 (0.10 per share). Reproduced, with assertions, in section 4 of `notes/artefacts/execution-market-making/liquidity-market-design-checks.py` (exit 0; other sections unchanged).

Notes changed: the `execution-market-making` pathway note; the entry's *Notation*, *Statement* and *Status*.

## macro markets and pricing review: the legacy macro chapter (global macro, regimes and data; transmission across FX, equities, rates, credit and commodities; practitioner frameworks; three files, chapter closed, legacy part removed), 16 October 2026

One integrated batch of all 120 remaining legacy blocks, from `compendium/legacy/multi-asset-systematic-macro/`, run after the two follow-ups above. It empties the last legacy chapter. Migration and source checking, not study.

### Scope

Counted by script against the starting commit `ca6986e` (guide pin `343d145909ba5384202b50604bf5ebe7e5b6ed86`, unchanged): 120 blocks, `01_regimes.tex` 35 (34 remarks, 1 definition), `02_transmission_maps.tex` 75 remarks (plus one top-level `enumerate`, the three roles of FX, outside any block), `03_practitioner_insights.tex` 10 remarks; 522 `\item` commands (145, 319, 58; `\itemsep` excluded); 492 `\begin`/`\end` commands (148, 304, 40); no proofs. Also in scope: the chapter wrapper `section.tex` (one introductory sentence citing `s7-gliner`), the transmission file's opening sentence and its four subsection introductions (FX, equities, fixed income, commodities), and the practitioner file's introduction.

### Provenance

- **Gliner, *Global Macro Trading* (`s7-gliner`).** Now available: a local PDF of the Wiley 2014 ebook (copyright page: Greg Gliner, Wiley, 2014; ISBN 978-1-118-36242-6 hardback, 978-1-118-42038-6 ePDF), 462 PDF pages, in the ignored `reading materials/`. The ebook has no printed page numbers; locators are chapter, section and PDF page, mapped from the PDF's outline and checked against the text, with no offset assumed. The regimes file follows chaps. 1, 3, 11 and 12; the transmission file chaps. 2, 4 and 7--10, often closely; chaps. 5 and 6 were not used.
- **Drobny, *Inside the House of Money* (`s7-drobny`).** The local copy is the Wiley 2006 printing (copyright 2006; ISBN-13 978-0-471-79447-9 cloth), not the catalogue's revised 2013 edition; printed page = PDF page $-$ 15. Every practitioner claim was compared with the interview it named; several belong to other interviewees (below).
- **Legacy additions without a source**: the "structural reasons" for macro, the three policy regimes, QE channels, the regime map's ordering claims, several indicator rules of thumb, LTCM/2015/2020 stress scenarios, BoJ/PBOC/APP/TLTRO/2015 SNB details, Greece 2012 and Argentina 2020, El Niño, Buxl and Schatz bands, and others, each marked in its entry.

### Ownership and dispositions

Routed by content and the guide's outcomes. The map's candidates were `multi-asset-systematic-macro` and `macro-regimes-stock-bond` (01), `macro-nowcasting-signals`, `macro-announcements-policy`, `monetary-policy-curve` and `fx-determination-forecasting` (02), and `multi-asset-systematic-macro` (03). **Routing exceptions** (recorded in each pathway note): from 01, central banks to `monetary-policy-curve`, the impossible trinity to `em-currencies-intervention`, data releases to `macro-nowcasting-signals` and `macro-announcements-policy`; from 02, the strategy and sizing blocks to the overview `multi-asset-systematic-macro`, regime responses to `macro-regimes-stock-bond`, and the asset-class blocks to `currency-markets`, `em-currencies-intervention`, `fx-premia`, `fx-dealer-market-making` (merge), `cross-asset-style-premia`, `international-equity-markets`, `vix-correlation-dividends`, `rates-credit-mortgages` (overview and merges), `money-markets-repo-lending`, `rate-derivatives`, `curve-term-structure`, `rates-inflation`, `futures-execution`, `sovereign-municipal`, `corporate-credit-cds`, `commodity-storage-curves`, `commodity-index-products`, `crude-oil-products`, `gas-hub-pricing`, `metals-storage-delivery` and `agricultural-futures-delivery`, because the map named only four keys for a file spanning every asset class. Nine chapters were opened: `multi-asset-systematic-macro`, `government-bond-markets`, `corporate-credit-capital`, `currency-markets`, `international-equity-markets`, `volatility-trading-premia`, `physical-commodity-markets`, `commodity-investing-premia` and `power-gas-environmental`; new topic files went into `rates-credit-mortgages/`, `portfolio-risk-financing/` and `energy-commodities/`, and one entry into `execution-trading-costs/futures-execution.tex`.

| File | Blocks | Destination | Disposition |
|---|---|---|---|
| 01 | *Global Macro* (definition); *Existence of Global Macro as a Strategy*; *Types of Global Macro Strategies*; *Trade Types in Macro*; *Liquidity Advantage* (5) | `def:global-macro-strategy` (new) | Rewritten from Gliner chap. 1; the "structural reasons" and "structural inefficiency" kept as unsourced hypotheses; liquidity consequences qualified |
| 01 | *Return Profile Across Cycles*; *Behaviour in Economic Crisis*; *Global Macro Correlation Properties* (3) | `ev:global-macro-crisis-performance` (new) | Gliner's index figures with their limits; crisis mechanisms marked as generalisation |
| 01 | *Monetary Policy Regimes*; *Objectives of Central Banks*; *Conventional Central Bank Tools*; *Central Bank Balance Sheet*; *Types of Money Supply*; *Zero Lower Bound and the Liquidity Trap*; *Quantitative Easing (QE)*; *Hawks and Doves*; *Fed Crisis-Era Programmes* (9) | `def:central-bank-policy-framework` (new, `monetary-policy-curve`) | Routing exception; QE figures **qualified** as announcement-day sums (Bauer via Gliner); "base only via OMO" corrected; regimes and channels marked as synthesis |
| 01 | *Taylor's Rule* | `mod:taylor-rule` (new) | Checked against Taylor (1993); $r^*$ "2--3\%" corrected to Taylor's 2\%; Gliner's printed slip recorded |
| 01 | *The Impossible Trinity* | `def:currency-regimes-intervention` (new, `em-currencies-intervention`) | Routing exception; Gliner p. 363 (Mundell, Frankel) |
| 01 | *Central Bank Communication*; *Major Central Banks*; *ECB-Specific Tools* (3) | `rule:major-central-banks-current` (new) | Dated from primary pages; ECB "25 members", "HICP $<2\%$" and "6 meetings" **corrected**; BoE minutes timing qualified; TARGET2 described correctly; BoJ, PBOC, APP, OMT-use claims stubbed |
| 01 | *Data Releases and Market Impact*; *Building Queries for Data Events* (2) | `meth:macro-event-queries` (new, `macro-announcements-policy`) | Routing exception; the six-event hit rate given its binomial probability |
| 01 | *Growth Indicators*; *Inflation*; *Employment Data*; *External Accounts*; *Government/Fiscal Indicators*; *Consumption Indicators*; *Housing Indicators*; *Business and Industry Indicators*; *Demographics*; *Demographic Implications by Country* (10) | `def:macroeconomic-indicators` (new, `macro-nowcasting-signals`) | Routing exception; "central banks target core" and Gliner's "core PCE" **corrected** (FOMC statement); the demographic column mix-up resolved; BDI, capacity and payroll-scope claims qualified or stubbed |
| 01 | *Key Data Release Calendar (US)* | `data:us-macro-release-calendar` (new) | ECB "6 per year" **corrected**; agency calendars as the record |
| 02 | *Macro Strategy Product Groups*; *Macro View Thesis* (2) | `def:global-macro-strategy` | Merged (routing exception) as Practice; the framing marked as the legacy's |
| 02 | *Relationship Between Assets*; *Sector Rotation Across Economic Cycles*; *Fixed Income in Different Macro Regimes*; *Commodities in Different Macro Regimes* (4) | `def:macro-regime-asset-map` (new, `macro-regimes-stock-bond`) | Routing exception; kept as hypotheses with Gliner's chap. 4 and 8 passages |
| 02 | *Asset Correlation Dynamics*; *Position Sizing Framework*; *Risk/Reward Discipline*; *Gap Risk*; *Risk Utilisation*; *Stress Testing*; *Performance Metrics* (7) | `meth:macro-position-sizing-risk` (new) | Routing exception; Turtle $N$ as standard deviation **corrected**; Gliner's correlation slip; legacy stress additions marked |
| 02 | *FX Market Structure* | `def:fx-market-structure` | Merged (routing exception); "5.5 days" corrected; BIS 2025 turnover |
| 02 | *Role of the US Dollar*; *Special Drawing Rights (SDRs)* (2), with the top-level list of FX roles and the FX introduction | `def:us-dollar-dxy-sdr` (new, `currency-markets`) | Routing exception; IMF factsheet for the current basket |
| 02 | *Currency Regimes*; *Central Bank Intervention* (2) | `def:currency-regimes-intervention` | Routing exception; legacy arguments marked as hypotheses |
| 02 | *Valuation Techniques* | `meth:fx-valuation-signals` (new, `fx-determination-forecasting`) | Gliner's factors; Balassa--Samuelson and Meese--Rogoff descriptions **corrected** |
| 02 | *Carry Trade Mechanics*; *Carry Trade Risk Factors* (2) | `mod:fx-carry-trade` (new, `fx-premia`) | Routing exception; skew and crash claims stubbed |
| 02 | *Top-Down Macro Approach to Equities*; *Equity Valuation Techniques for Macro* (2), with the equities introduction | `meth:equity-index-valuation` (new, `cross-asset-style-premia`) | Routing exception; Tobin's $q$ slip recorded |
| 02 | *Major Equity Indices by Region*; *Index Construction Methods*; *Equity Derivatives Overview* (3) | `def:equity-indices-derivatives` (new, `international-equity-markets`) | Routing exception |
| 02 | *The Volatility Index (VIX)*; *Variance Swaps*; *Dividend Swaps* (3) | `def:vix-variance-dividend-swaps` (new, `vix-correlation-dividends`) | Routing exception; "priced with realized volatility" **corrected**; daily move as a standard deviation |
| 02 | *Leading Indicators for Equities*; *AUD Volatility as Risk Barometer* (2) | `meth:equity-macro-leading-indicators` (new, `macro-nowcasting-signals`) | BDI "cannot be speculated" **contradicted** (unsupported; freight forwards) |
| 02 | *Fixed Income Universe*; *Fixed Income ETFs* (2), with the fixed-income introduction | `def:fixed-income-universe` (new, `rates-credit-mortgages`) | Routing exception; Gliner's Table 9.5 |
| 02 | *Money Markets and Funding*; *Key Reference Rates*; *LIBOR-OIS Spread* (3) | `def:money-market-reference-rates` (new, `money-markets-repo-lending`) | Routing exception; LIBOR and EONIA ends dated from primary pages |
| 02 | *Overnight Index Swaps (OIS)*; *Eurodollar Futures* (2) | `meth:policy-path-ois-futures` (new) | OIS probability conditions derived; Eurodollar futures historical, conversion dated from the CBOT filing (date discrepancy stubbed) |
| 02 | *Interest Rate Swaps* | `def:interest-rate-swaps` (new, `rate-derivatives`) | Routing exception |
| 02 | *Forward Rate Agreements (FRAs)* | `mod:forward-rates-fra` | Merged (routing exception); Gliner's fixing-date slip recorded |
| 02 | *US Treasury Futures*; *German Bund Futures* (2) | `conv:government-bond-futures` (new, `futures-execution`) | Routing exception; "backwardation due to term premium" **corrected** to carry; ticks recomputed |
| 02 | *Yield Curve Trades*; *Carry and Rolldown*; *Curve Inversion as Recession Indicator* (3) | `meth:curve-trades-carry-rolldown` (new, `curve-term-structure`) | Routing exception; carry sign shown conditional; "every recession since 1970" **corrected** to Estrella--Trubin's record; Gliner's rolldown misdefinition recorded |
| 02 | *Treasury Inflation-Protected Securities (TIPS)*; *Breakeven Inflation* (2) | `def:tips-breakevens` (new, `rates-inflation`) | Routing exception; schedule from TreasuryDirect; "trades at 105" and breakeven-as-expectations **corrected** |
| 02 | *Sovereign Credit Risk*; *Historical Sovereign Defaults* (2) | `def:sovereign-credit-defaults` (new, `sovereign-municipal`) | Routing exception; recovery test depends on $n$; Greece 2012 and Argentina 2020 stubbed |
| 02 | *Credit Default Swaps (CDS)*; *CDS Credit Events* (2) | `mech:cds-contract-credit-events` (new, `corporate-credit-cds`) | Routing exception; settlement equivalence; Gliner's upside **corrected**; post-2009 contract stubbed |
| 02 | *Duration and DV01*; *Convexity* (2) | `mod:duration-convexity` | Merged (routing exception); the convexity formula's missing price **corrected** |
| 02 | *Contango and Backwardation*; *Ending Stocks and Supply/Demand Balance* (2), with the commodities introduction | `def:contango-backwardation-stocks` (new, `commodity-storage-curves`) | Routing exception; the balance identity extended for trade |
| 02 | *Commodity Indices*; *Commodity Risk and Return Profile* (2) | `def:commodity-indices-risk-return` (new, `commodity-index-products`) | Routing exception; DBC's energy weight moved back from the GSCI |
| 02 | *Crude Oil Fundamentals*; *Major Oil Benchmarks*; *OPEC and Oil Supply*; *Oil Chokepoints and Infrastructure*; *Crack Spread* (5) | `def:crude-oil-markets` (new, `crude-oil-products`) | Routing exception; kerosene and Aramco slips recorded; Brent delivery stubbed |
| 02 | *Natural Gas* | `def:natural-gas-market` (new, `gas-hub-pricing`) | Routing exception; the flaring explanation **corrected** |
| 02 | *Gold*; *Silver*; *Platinum*; *Copper*; *Aluminium* (5) | `def:metals-markets` (new, `metals-storage-delivery`) | Routing exception; the platinum density and copper consumption slips recorded |
| 02 | *Agricultural Commodities Overview*; *Corn*; *Wheat*; *Soybeans*; *Cotton*; *Coffee*; *Weather Risk in Agriculture* (7) | `def:agricultural-markets` (new, `agricultural-futures-delivery`) | Routing exception; legacy additions (El Niño, coffee contract) marked |
| 03 | all ten blocks, with the file introduction | `meth:macro-practitioner-frameworks` (new) | Checked interview by interview; misattributions **corrected** (below) |
| wrapper | `section.tex` introductory sentence | `def:global-macro-strategy` and the chapter opener of `multi-asset-systematic-macro/` | Restated as Gliner's capital-preservation aim |

Block total: 120 (35 + 75 + 10); none deleted without a destination; no block became a stub alone. 34 new entries; merges into `mod:duration-convexity`, `mod:forward-rates-fra` and `def:fx-market-structure`.

**Corrections to legacy claims and source slips**, each in its entry: the Fed's goal is headline PCE (Gliner's and the legacy's "core"); ECB 27 members and decisions every six weeks (not 25, 23 or "6 per year"); variance-swap strikes are set ex ante (Gliner's "priced with realized volatility"); Treasury futures sit below the bond because of positive carry (not term premium); a TIPS price is not the adjusted principal; breakevens contain risk and liquidity premia; Turtle $N$ is an average range; perfect correlation is not equal moves; Taylor's $r^*$ is 2\%; QE figures are announcement-day sums; OIS probabilities need a meeting-dated swap; the steepener's carry sign depends on the curve and repo; inversion's record is Estrella--Trubin's six recessions to 2005 on monthly averages; Moody's recovery test depends on $n$; CDS payout is par minus recovery; the convexity formula is proportional; the demographic peaks mix two columns; platinum's density ratio is 1.11; Balassa--Samuelson, Tobin's $q$, TARGET2, rolldown, FRA fixing date, kerosene, Saudi Aramco, Chile's copper share and V2X misstated by Gliner. **Drobny attributions corrected**: the "75 percent of price movement", long-gamma leverage, forced-seller and "inevitable" points are the anonymous currency specialist's (not Siva-Jothy's); 4:1, cooling-off and three or four trades a year are Andres Drobny's (not Wadhwani's); time-horizon arbitrage is Porter's; front-page contrarianism is Rogers's and Porter's (not Anderson's); Porter's "90 percent explained by the direction of interest rates" restored; the anonymous manager's blocs are Europe, Asia and Latin America. Bessent's 50/30/20 (p. 280), Dimitrijević's internal stops and one-month cool-off (pp. 295--296), Yra Harris's 80 percent, probes, clearing the books and three or four positions (pp. 210, 214--215) and the five-month horizon (p. 334) were all found.

### Sources, 2026-10-16

- `s7-gliner` (PDF pages, no printed numbers): chap. 1 pp. 29--40; chap. 2 pp. 50--69; chap. 3 pp. 79--86; chap. 4 pp. 91--102; chap. 7 pp. 179--209; chap. 8 pp. 214--240; chap. 9 pp. 245--280; chap. 10 pp. 291--348; chap. 11 pp. 355--398; chap. 12 pp. 401--428.
- `s7-drobny` (2006 printing; printed = PDF $-$ 15): pp. 50, 54, 60--63, 78--79, 85, 109, 125, 130--131, 135, 139, 147--148, 152, 163, 177, 204--210, 214--215, 217, 230, 249--262, 280, 283, 293--296, 327--336.
- New source keys (`compendium/front/sources.tex`), retrieved 2026-10-16: `fomc-page`, `fomc-longer-run-goals`, `ecb-governing-council`, `ecb-strategy`, `ecb-estr`, `emmi-eonia`, `boe-mpc-page`, `boe-mps-minutes`, `boj-policy-board`, `snb-strategy`, `arrc-sofr-transition`, `cbot-23-214` (CBOT filing with the CFTC, 1 June 2023), `treasurydirect-tips`, `bls-ces-page`, `imf-sdr-factsheet`, `bis-triennial-2025`, `estrella-trubin-2006` (read in full) and `taylor-1993` (p. 202, page image). Catalogue keys reused: `exp-sofr-data` (EFFR and SOFR); several unread catalogue readings named only in *Further reading* or as "catalogue entry only, not read".
- Not retrievable or not read: CME's Eurodollar conversion notices and contract pages (403 or time-outs); ICE's dollar-index methodology (404); the FCA's announcement page (403); the ISDA Determinations Committee's 2012 Greece decision; the BLS handbook page on CES concepts; the BIS 2025 currency shares; Bauer (2012), Moody's (2007), Goldman Sachs (2007) and the other secondary sources Gliner reproduces; Gliner's chaps. 5--6; the 2013 edition of Drobny; every pathway's required readings.

### Numerical checks

`notes/artefacts/multi-asset-systematic-macro/macro-pricing-risk-checks.py` (numpy, scipy; fixed seed; exit 0 with `/opt/homebrew/bin/python3.10`), 17 sections with assertions: Turtle $N$ against a standard deviation; risk/reward arithmetic; correlation against beta; the six-event hit rate; the Taylor rule and Gliner's slip; OIS probabilities and dilution; Eurodollar and Treasury futures ticks; futures below spot with positive carry; steepener carry signs; duration, DV01 and convexity; TIPS index ratio, floor and breakevens; CDS settlement and Moody's recovery test; variance swaps and daily moves; commodity notionals, the 3:2:1 crack spread and platinum density; Gliner's Table 12.2 columns; ending stocks with trade; carry-to-risk rankings.

### Checks and their limits

| Source | Passages | Limits |
|---|---|---|
| `s7-gliner` | as listed | A 2013--2014 practitioner text; market figures, contract terms and memberships dated; many slips recorded; its own sources not read |
| `s7-drobny` | as listed | 2006 printing, not the catalogue's 2013 edition; opinions of selected survivors |
| Central-bank, benchmark, Treasury, BLS, IMF and BIS pages | as retrieved | Living pages: current as of 16 October 2026 only; history of changes mostly unchecked |
| `cbot-23-214` | secs. 1--2 | An exchange's account in a rule filing; the conversion date conflicts with the weekday |
| `estrella-trubin-2006`, `taylor-1993` | as listed | Record to 2005; Taylor read from a page image |

The 34 new entries and the merged entries are *partly checked*, *draft*; **human review is outstanding**. Quotations: every `` `` '' `` quotation on added lines (363 distinct) was compared by script with the text layers of Gliner, Drobny, the retrieved pages and the legacy files at `ca6986e`; 330 matched, and the 33 misses were inspected by eye: legacy wording containing LaTeX math, quotations broken by a page marker or hyphenation in the text layer, Gliner's misprints quoted with "[sic]", and pre-existing quotations on modified lines. Paraphrases that had been put in quotation marks were rewritten or quoted exactly before the count.

### Preservation

New artefacts in `notes/artefacts/multi-asset-systematic-macro/`: `regimes.tex`, `transmission-maps.tex` and `practitioner-insights.tex` (each file body below its migrate-to line, verbatim, with only the subsection headings unnumbered), `global-macro-original-chapter.tex` (the chapter wrapper, byte-identical) and `macro-pricing-risk-checks.py`. Checked by script against `ca6986e`: each body occurs once; all 121 top-level blocks (35, 76 including the FX-roles list, 10) occur verbatim, once and in order; `\item` counts 145, 319 and 58 (522) and `\begin`/`\end` sequences 148, 304 and 40 (492) match; no proofs. The three artefacts compile standalone (8, 15 and 2 pages; no warnings).

### Counts

`check_compendium.py --check`, 0 problems: 120 → 0 legacy blocks (shared 110 → 0, single-candidate 10 → 0); entries 177 → 211 (conventions 3 → 4, data 3 → 4, definitions 61 → 80, evidence 9 → 10, mechanisms 13 → 14, methods 37 → 45, models 24 → 26, rules 3 → 4). Pathway notes: 23 new (`multi-asset-systematic-macro`, `macro-regimes-stock-bond`, `macro-nowcasting-signals`, `macro-announcements-policy`, `cross-asset-style-premia`, `monetary-policy-curve`, `curve-term-structure`, `rates-inflation`, `rate-derivatives`, `sovereign-municipal`, `corporate-credit-cds`, `currency-markets`, `em-currencies-intervention`, `fx-determination-forecasting`, `fx-premia`, `international-equity-markets`, `vix-correlation-dividends`, `commodity-storage-curves`, `commodity-index-products`, `crude-oil-products`, `metals-storage-delivery`, `agricultural-futures-delivery`, `gas-hub-pricing`), with 32 backlog stubs; `rates-credit-mortgages`, `futures-execution` and `money-markets-repo-lending` gained entries or merges and 4 stubs; `fx-dealer-market-making` and `execution-market-making` record the merge and follow-ups.

### Other files

`compendium/compendium.tex` (the legacy-part line removed); `compendium/legacy/part.tex` and `compendium/legacy/multi-asset-systematic-macro/` removed (`compendium/legacy/execution-trading-costs/figures/` kept); `compendium/front/preface.tex` (the link to the removed part replaced); `compendium/front/sources.tex`; chapter openers of `rates-credit-mortgages`, `portfolio-risk-financing`, `energy-commodities`, `execution-trading-costs` and `execution-market-making`; `README.md` and `compendium/README.md`; reading notes `notes/readings/s7-gliner.md` and `s7-drobny.md` (new); `notes/log.md` (coverage rows, the reading table, open questions); `notes/source-review-index.md` (status, index, *After the migration* replacing the planning text that deferred the transmission blocks for want of Gliner, the emptied map). The old block environments stay in `compendium/preamble.tex`, because the artefacts compile with them.

### Build

`latexmk -g -pdf compendium.tex` exits 0: 251 pages (240 before, with the legacy part); no LaTeX warnings; 0 overfull and 0 underfull boxes after six long monospace keys and paths were moved away from line ends (the baseline build at `ca6986e` also had none); the inherited `page.i` warning. Tests: 14 pass. The committed PDF was rebuilt from the final sources.

### For review

- The routing of the transmission file across twenty pathways, and of the central-bank and data blocks away from the regimes file's candidates.
- Every correction of Gliner listed above, and the reattributions in Drobny (the 2013 edition not inspected).
- Current-status statements dated 16 October 2026 (FOMC, ECB, BoE, BoJ, SNB, LIBOR, EONIA, TIPS schedule, payroll date), against their pages.
- The backlog stubs that stand in for unread primary sources: the Eurodollar conversion date, BoE minutes history, BLS payroll scope, ISDA's 2012 Greece decision, the BIS dollar share, ICE's index methodology and current exchange contract terms.

## macro markets and pricing review follow-up: audit corrections, a source-verification pass over the 37 macro entries and merges, and the 36 macro markets and pricing review backlog items, 16 October 2026

Corrections and source checks after macro markets and pricing review (`f73498d`); the macro markets and pricing review record above is left as written, and this record supersedes it where they differ. No legacy block, entry label or entry count changed (0 legacy blocks; 211 entries). This is source verification, not human review or study: every entry stays *draft*, and verification statuses were extended only for the passages actually read.

### Audit findings resolved

1. **Convexity, `mod:duration-convexity`.** Positive convexity improves price relative to the linear approximation; it does not make an unhedged bond gain both ways: the 10-year 4 percent par bond loses 7.722 percent at $+100$~bp and gains 8.530 percent at $-100$~bp (duration alone: $\mp8.111$). The long-volatility analogy is restricted to a duration-hedged position (long the 10-year, short 4.30 times the face of a 2-year: $+0.274$ and $+0.302$ per 100 for $\pm100$~bp, $+0.018$ for $+25$~bp), with its conditions (parallel moves, rebalancing, carry and financing cost). Negative convexity is qualified for callables and MBS (near the money; model-dependent effective convexity). Derivation, not a source check.
2. **Inversion, `meth:curve-trades-carry-rolldown`.** Estrella and Trubin reread (pp.~4--6, table p.~6): on their 1968--2005 sample the monthly-average 10-year minus three-month spread was both necessary and sufficient (every recession preceded by three to twelve negative months within twelve months; no false signals), which reverses the macro markets and pricing review sentence calling it sufficient but not necessary; the entry now separates sample, signal and horizon from a forecasting claim. Extended with Treasury par yields (CMT proxy) and the NBER chronology: inversions before the December 2007 and February 2020 peaks, and November 2022--November 2024 plus five months of 2025 with no peak dated after February 2020 as of 16 October 2026.
3. **VIX, `def:vix-variance-dividend-swaps`.** Cboe's methodology (v6.0, 26 February 2026): $\text{VIX}=100\sigma$ with $\sigma^2$ an annualised 30-day variance computed from option prices, minutes-based annualisation (43,200 and 525,600); VIX~20 means variance 0.04 (0.0033 over 30 days); first value date January 1990, current method from 2003; VIX derivatives settle to a Special Opening Quotation. Gliner's implied-volatility description and the legacy's futures remark corrected.
4. **Gold and silver, `def:metals-markets`.** Gliner p.~320 names China, the United States, Australia and South Africa (``more than 40 percent'') and states that China overtook South Africa; the entry had dropped two countries and called the overtaking unstated. USGS gives 38.9 and 37.8 percent for 2011 and 2012. Table~10.9 (p.~322) is internally inconsistent: Mexico 162.2 plus China 117.0 over the stated 787.0 total is 35.5 percent, the printed shares imply a denominator near 594 and sum to 132.5 percent, and Gliner's 47 and 83 percent follow the printed shares; USGS gives 33.5 percent for 2012. Recorded, not repaired; the World Silver Survey was not read.
5. **Drobny, `meth:macro-practitioner-frameworks` and the reading note.** Andres Drobny (pp.~131--132): re-entry on a single trade with a very tight stop and the incurred loss counted (4:1 becoming 4:3 after two stops), ``On a specific trade, no'' cooling-off; a month away only after a portfolio-wide stop-out and big losses. Siva-Jothy (p.~85): ``50 to 60 percent options'' with no stated denominator (not ``of risk''); three or four opportunities a year and overtrading are his; Andres Drobny only accepts the interviewer's framing (p.~125).
6. **Chapter 8 and 12 locators, `def:macro-regime-asset-map` and `def:macroeconomic-indicators`.** Figure~8.3 (p.~217) compared phase by phase with the legacy sector table (partly matching; the legacy late-cycle list contradicts the figure's defensive slowing-growth phase). The U.S.-consumer figure is Gliner's (p.~416); the macro markets and pricing review statement that it was not in the passages read was wrong. Table~12.2 is on pp.~424 (heading) and~425 (data), not pp.~422--423.
7. **Commercial paper, `def:money-market-reference-rates`.** Section 3(a)(3) quoted (``not exceeding nine months'', with the current-transaction condition); SEC interpretations 219.01--219.02; the Richmond Fed's account of the other historical conditions (not ordinarily purchased by the general public, prime quality and Federal Reserve discountability under Release 33-4412, discounting dropped in 1980). Gliner's ``less than 270 days'' kept as attributed.
8. **GSCI history, `def:commodity-indices-risk-return`.** ``Pre-2000 back-filled'' corrected: the index dates from 1991 (Dunsby and Nelson; S\&P pages refused access, and the supplied 11 April 1991 date could not be confirmed, search listings showing April 1991), so 1970--1990 of Gliner's Table~10.1 is back-calculated; spot, excess-return and total-return variants distinguished, without assuming which the 2007 study used.
9. **FX carry and CDS.** `mod:fx-carry-trade` states the quote convention ($S$ domestic per foreign), simple rates, the exact covered-parity and funded-P\&L formulas and their first-order forms (example: $+0.2550$ against $+0.2500$ percent). `mech:cds-contract-credit-events` presents the physical/cash equivalence as an illustration under a common recovery valuation, with a counterexample (62 against 60), and dates the 2009 Big Bang changes and the 2012 Greek determination.

### Verification pass over the 37 entries (34 entries and 3 merges)

Every quotation in the macro markets and pricing review entries was mapped by script to the Gliner PDF page or Drobny printed page where it occurs (`loccheck` against the text layers); locators matched except those corrected above, and two labels (``Short-end TIPS trade like food and energy'' and ``TIPS are typically issued on a quarterly basis'', pp.~247--248, are Gliner's, not only the legacy's) were fixed. Spot rereads: Gliner pp.~52, 55, 57 (sizing, risk/reward, gap risk), 36--38 (Barclays Prime Services), 222--227, 246--248, 302, 314, 317, 320--325, 356, 373 (Table~11.4 against Bauer's Table~1, which matches exactly), 416, 424--425.

| Entry | Follow-up result |
|---|---|
| `def:global-macro-strategy`, `ev:global-macro-crisis-performance` | Locators and quotations re-matched; no change |
| `meth:macro-position-sizing-risk` | pp.~52--57 reread; no change |
| `meth:macro-practitioner-frameworks` | Corrected (item 5) |
| `def:macro-regime-asset-map` | Corrected (item 6) |
| `def:macroeconomic-indicators` | Corrected (item 6); CES scope from BLS (nonprofits in scope; other legacy exclusions right); release timing |
| `meth:equity-macro-leading-indicators`, `meth:macro-event-queries`, `meth:equity-index-valuation` | Re-matched; no change |
| `data:us-macro-release-calendar` | BEA, Census and G.17 calendars read; cadence confirmed; CPI and ISM unchecked |
| `def:central-bank-policy-framework` | Bauer's letter read; event-study caveats quoted |
| `mod:taylor-rule` | No change |
| `rule:major-central-banks-current` | BoE minutes history, FOMC practice, BoJ 2024 exit, SNB 2015, ECB APP and OMT status dated; TARGET2/T2S |
| `meth:policy-path-ois-futures` | Eurodollar conversion narrowed (CME notice not readable; 14 April 2023 better supported than the filing's 23 April) |
| `meth:curve-trades-carry-rolldown` | Corrected (item 2) |
| `def:tips-breakevens` | Gliner's 2014 calendar compared with today's; attribution of two sentences fixed |
| `def:interest-rate-swaps` | BIS: interest rate derivatives the largest OTC component ($579 trillion, end-June 2024) |
| `def:fixed-income-universe` | SIFMA 2025 totals; the legacy ranking shown to be ill-posed |
| `def:money-market-reference-rates` | Corrected (item 7); Treasury bill schedule |
| `def:sovereign-credit-defaults` | ISDA Greece determination and auction dated |
| `mech:cds-contract-credit-events` | Corrected (item 9) |
| `conv:government-bond-futures` | Eurex terms read (legacy Schatz and Buxl bands are current); CME unread |
| `def:us-dollar-dxy-sdr` | ICE formula and history; BIS 2025 shares (dollar 89.2 percent) |
| `def:currency-regimes-intervention`, `meth:fx-valuation-signals` | Re-matched; no change |
| `mod:fx-carry-trade` | Corrected (item 9); BNP abstract |
| `def:equity-indices-derivatives` | Re-matched; no change |
| `def:vix-variance-dividend-swaps` | Corrected (item 3) |
| `def:contango-backwardation-stocks` | Re-matched; no change |
| `def:commodity-indices-risk-return` | Corrected (item 8) |
| `def:crude-oil-markets` | ICE Brent terms (EFP delivery, cash-settlement option) |
| `def:metals-markets` | Corrected (item 4); USGS 2025 production shares |
| `def:agricultural-markets` | ICE coffee and cotton terms |
| `def:natural-gas-market` | Re-matched; no change |
| Merges: `mod:duration-convexity` (item 1), `mod:forward-rates-fra` (re-matched, no change), `def:fx-market-structure` (re-matched, no change) | |

### The 36 backlog items

Resolved (9): `data:bls-ces-scope`, `rule:boe-minutes-publication-history`, `data:fomc-communication-current`, `ev:isda-greece-2012-determination`, `data:bis-2025-currency-shares`, `conv:dxy-methodology`, `conv:cboe-vix-methodology`, `data:fixed-income-market-size`, `data:treasury-bill-offering-schedule`. Narrowed to a named document, dataset or empirical test (27): `data:eurodollar-sofr-conversion-date` (CME advisories 23-082 and 23-121), `ev:qe-announcement-effects` (Gagnon et al.), `rule:central-bank-policy-history` (OMT activation, TLTRO, PBOC), `ev:curve-inversion-after-2005` (H.15 series), `rule:tips-auction-schedule-history` (refunding announcements), `data:irs-notional-share` (BIS swaps line), `ev:sovereign-restructurings-after-2006`, `conv:cds-standard-contract` (fixed coupons, 2014 Definitions), `data:de-facto-regime-classification`, `ev:carry-crash-skewness` (paper bodies), `data:equity-index-lists-current`, `conv:commodity-index-methodologies`, `conv:brent-wti-contract-terms` (NYMEX WTI), `data:opec-membership-current`, `data:metals-market-shares-current` (consumption shares, COMEX/LME), `conv:cbot-ice-ag-contract-terms` (CBOT grains), `conv:henry-hub-contract-terms`, `conv:treasury-bund-futures-current-specs` (CME), `data:us-release-schedules-2026` (BLS CPI, ISM), `data:demographic-projections-current`, `data:post-libor-funding-stress-measures`, and six empirical items that no reading can close (`ev:global-macro-returns-after-2013`, `ev:practitioner-rules-tested`, `ev:regime-asset-responses-tested`, `ev:equity-index-value-signal`, `ev:fx-valuation-factors-oos`, `ev:backwardation-scarcity-or-premium`). Each stub's text in its pathway note names what is missing; each affected note records the follow-up under *Source verification after macro markets and pricing review*.

### Sources, 2026-10-16

Read directly: Estrella and Trubin (New York Fed PDF); Cboe's VIX methodology (catalogue key `gap-cboe-vix6`); Bauer (FRBSF Economic Letter 2012-16, with Table~1 as an image); the Warsh review and the Bank of England's 2015 documentation page; the FOMC calendars; the Bank of Japan statement of 19 March 2024; the SNB release of 15 January 2015 (title and date); the ECB's APP page and TPI release; NBER's chronology and dating pages; Treasury's daily par-yield files 2006--2026 (monthly averages in `ust-10y3m-monthly.csv`); TreasuryDirect's bills and TIPS pages; the BIS 2025 FX results; ICE's Dollar Index FAQ, Brent, coffee and cotton specifications; Eurex's fixed-income factsheet and contract specifications of 10 September 2025; ISDA's Big Bang page and Greece releases; USGS Mineral Commodity Summaries 2013 (gold, silver) and 2025 (gold, silver, copper); the Richmond Fed's commercial-paper chapter; Dunsby and Nelson (2010); BEA's schedule, the Census calendar, the Fed's G.17 dates; SIFMA's Fact Book highlights; the NBER abstract of Brunnermeier, Nagel and Pedersen. Read through a web-fetching tool's extracts (direct requests refused): the BLS CES concepts page and FAQ, the SEC's Securities Act interpretations, 15 U.S.C. 77c, the BIS OTC release for end-June 2024. Seen only in search listings: CME Clearing Advisory 23-082's title and summary, S\&P's GSCI launch information, the Greek auction final price. Refused or unusable: CME (terms-of-use block, not circumvented), S\&P Dow Jones Indices and Bloomberg methodologies (403), OPEC (challenge), EIA (script-only pages), ISM, BLS schedule pages, the IJCB PDF. Gliner and Drobny reread at the pages listed above. 32 source keys added (`sifma-factbook-2026` among them) and `bis-triennial-2025` updated in `compendium/front/sources.tex`.

### Checks

`notes/artefacts/multi-asset-systematic-macro/convexity-curve-signals-checks.py` (exit 0 with `/opt/homebrew/bin/python3.10`; reads `ust-10y3m-monthly.csv` in the same folder), seven sections: convexity unhedged and duration-hedged; inversion runs against NBER peaks; VIX units; gold and silver shares and Table~10.9's denominators; exact and first-order FX carry; CDS settlement with different recovery valuations; Andres Drobny's 4:1 after two stops. The market design and liquidity / dealer models and information / macro markets and pricing reviews scripts were rerun unchanged (exit 0). Quotations added in this follow-up were compared by script with the source text layers; the misses are source titles, passages read only through fetching-tool extracts (BLS, SEC, statute, BIS), Gliner and legacy text broken by page markers, LaTeX or ``[sic]'', and the search-listing title of CME's notice, all inspected.

### Other files

README.md and compendium/README.md (stale descriptions of the removed legacy part corrected); the Gliner and Drobny reading notes; 26 pathway notes; `notes/log.md`; `notes/source-review-index.md`. Preservation artefacts unchanged.

### For review

- The corrections listed above, especially the reversal on necessity and sufficiency, the reading of Table~10.9 and the restricted long-volatility analogy.
- Facts taken from fetching-tool extracts or search listings (BLS, SEC, BIS OTC, CME notice title, GSCI launch).
- The post-2005 inversion check, which uses Treasury's 3-month CMT rather than Estrella and Trubin's bill series.

## macro markets and pricing review second follow-up: five audit corrections (inversion signals, FX accrual bases, CDS coverage, convexity carry, the GSCI launch), primary sources for the 21 source-based macro markets and pricing review stubs, and four dealer models and information review source gaps, 16 October 2026

Corrections and source checks after the first macro markets and pricing review follow-up (`b11076f`); earlier records are left as written, and this record supersedes them where they differ. No legacy block, entry label or entry count changed (0 legacy blocks; 211 entries). This is source verification, not human review or study: every entry stays *draft*, mastery and consolidation dates are untouched, and verification statuses were extended only for the passages read. The quotation-matching pass over all 37 macro markets and pricing review entries was not repeated; new quotations were checked by script against the text of the sources read (below).

### Audit findings resolved

1. **Inversion, `meth:curve-trades-carry-rolldown`.** The pitfalls now separate three statements: the historical observation (Estrella and Trubin's 1968--2005 table: every recession preceded by negative monthly averages, no false episodes), the paper's probit, which predicts recession status twelve months ahead ($P(\text{recession})=0.273$ at a zero spread, not a sufficient condition), and an onset rule defined here. Recessions start the month after an NBER peak; an inverted expansion month is a *hit* if a recession begins in months $t+1$ to $t+12$, a *miss* if a complete window has none, and *provisional* while the window is incomplete or has no NBER determination; an *episode* is a run of consecutive inverted months. On the paper's own series (H.15 three-month bill converted to a bond-equivalent yield as in its n.~4, against the 10-year CMT), rebuilt from the Board's H.15 data package by `h15_monthly.py` (16,181 business days 1962-01-02 to 2026-10-14; unique, increasing dates; no missing months; October 2026 flagged incomplete), the paper's table is reproduced (minimum $-0.07$ in 1990 against the printed $-0.08$; June 1989 $-0.16$). 1968--2005: 54 inverted expansion months, 6 month-rule misses (1968-12, 1978-11, 1978-12, 1979-01, 1989-06, 1989-07), all 9 episodes hits; so ``every monthly inversion was a sufficient twelve-month onset signal'' was wrong and is removed, and the June 1989 footnote says why. 2006--2026: 43 months, 11 hits, 5 misses (2006-08 to 2006-12), 27 provisional; episodes 2006-08 to 2007-05, 2019-05 to 2019-09 and 2020-02 hits, 2022-11 to 2024-11 and 2025-03 to 2025-04 provisional. Treasury's CMT proxy (rebuilt by `ust_monthly.py` from a 5,202-day extract; `complete` column added, spreads unchanged) gives 46 months (11, 5, 30) and one more provisional episode (2025-06 to 2025-08), and is kept distinct from the paper's series. Section~2 of the first follow-up script now tests these rules; NBER peak months are kept separate from first contraction months throughout.
2. **FX carry, `mod:fx-carry-trade`.** Separate accrual fractions $\tau_d,\tau_f$ for the two rates' day-count bases, carried through covered parity, the funded P\&L $\Pi=(S_T/S_0)(1+i_f\tau_f)-(1+i_d\tau_d)$, carry $i_f\tau_f-i_d\tau_d$, hedging at $F$ and the first-order forms; the continuously compounded log excess return $x$ is defined separately, with $e^x-1=\Pi/(1+i_d\tau_d)$. Example, 90 days, 5 percent ACT/360 against 2 percent ACT/365: $\tau_f=0.246575$, $F/S_0=1.0075314$, carry $-0.75685$ percent (not $-0.75$), $\Pi=+0.24808$ percent for a 1 percent rise in $S$ against $+0.24315$ to first order, $x=0.24472$ percent (second follow-up script, section~1).
3. **CDS, `mech:cds-contract-credit-events`.** The Determinations Committee discussion is qualified by contract coverage from the Big Bang protocol page and its FAQ: Protocol Covered Transactions, DC provisions from 8 April 2009 and backstop dates from 20 June 2009, excluded LCDS and ABS CDS, Covered Non-Auction Transactions; triggering by a DC request or by a bilateral Credit Event Notice with Notice of Publicly Available Information within 60 days, tolling and dismissal; no physical settlement before an auction unless agreed bilaterally; no 2009 auctions for Restructuring; the 100/500 Standard North American contract. Bilateral notices are no longer described as pre-2009 only. The 2014 Definitions (a purchased document) were not read.
4. **Convexity, `mod:duration-convexity`.** The $\pm100$~bp shock example is kept; negative carry is qualified: on the flat 4 percent curve with financing and rebate at 4 percent, carry is $4-4k+4(k-1)=0$ for any hedge ratio ($k=4.30$); carry depends on curve shape, repo against rebate, financing and rebalancing, and ``positive convexity alone does not determine carry'' (second follow-up script, section~2).
5. **GSCI, `def:commodity-indices-risk-return`.** S\&P's education note (``The S\&P GSCI was launched April 11, 1991. \dots\ All data prior to such date is back-tested hypothetical data'', PDF p.~6) and methodology (base date 31 December 1969, launch 11 April 1991, p.~18; ER and TR definitions, p.~13; back-test disclosure, p.~39) give the exact boundary: back-tested to 10 April 1991, live from 11 April; 1991 is not labelled wholly live. The Goldman Sachs table's return variant stays unresolved. The Bloomberg Commodity Index methodology (February 2026) was added for weights, caps, the 2026 targets, the roll and the 14 July 1998 launch.

### The 21 source-based macro markets and pricing review stubs

Resolved (7): `data:eurodollar-sofr-conversion-date` (CME Clearing Advisory 23-082: trade date 17 April 2023 after the close of 14 April; the CBOT filing's ``April 23'' is the date of a CME press release cited in CME Submission 24-271), `conv:commodity-index-methodologies` (S\&P GSCI and BCOM methodologies), `rule:tips-auction-schedule-history` (refunding statements of 31 October 2018 and 5 May 2004, the former with its 2018 and 2019 TIPS calendar), `data:irs-notional-share` (BIS bulk data: swaps 81.4 percent of \$669.5 trillion at end-December 2025), `data:de-facto-regime-classification` (Ilzetzki--Reinhart--Rogoff, to December 2025), `data:demographic-projections-current` (UN WPP 2024), `ev:qe-announcement-effects` (NY Fed Staff Report 441). Narrowed (10): `rule:central-bank-policy-history` (TLTRO and the 2014 PBOC band read; OMT activation, the current CNY band and fixing reform, reserve requirements and the Bank of England's first forecast remain), `ev:curve-inversion-after-2005` (H.15 rebuild done; only the outcome-dependent revisit remains), `data:equity-index-lists-current` (JASDAQ and MOEX read), `data:opec-membership-current` (opec.org refused; secondary reports of a 2026 change not used), `data:metals-market-shares-current` (gold and silver demand shares read), `data:us-release-schedules-2026` (BLS CPI read; ISM behind a login), `ev:sovereign-restructurings-after-2006` (IMF reports read; the ``ninth default'' count remains), `conv:cds-standard-contract` (FAQ read; 2014 Definitions remain), `ev:carry-crash-skewness` (BNP body read; Menkhoff et al.\ remain), `data:post-libor-funding-stress-measures` (OFR's replacement variables and index read; research usage and a dated CP--SOFR OIS series remain). Unchanged, access barrier (4): `conv:treasury-bund-futures-current-specs`, `conv:brent-wti-contract-terms`, `conv:henry-hub-contract-terms` and `conv:cbot-ice-ag-contract-terms` (CME returned HTTP 403 to the shell and the fetching tool; CFTC-hosted copies of NYMEX Chapter 200 were from 2011--2012 and not current). The six empirical stubs (`ev:global-macro-returns-after-2013`, `ev:practitioner-rules-tested`, `ev:regime-asset-responses-tested`, `ev:equity-index-value-signal`, `ev:fx-valuation-factors-oos`, `ev:backwardation-scarcity-or-premium`) stay open. Entries changed for these: `meth:policy-path-ois-futures`, `def:central-bank-policy-framework`, `rule:major-central-banks-current`, `def:tips-breakevens`, `def:interest-rate-swaps`, `def:currency-regimes-intervention`, `def:macroeconomic-indicators`, `data:us-macro-release-calendar`, `def:sovereign-credit-defaults`, `mod:fx-carry-trade`, `def:equity-indices-derivatives`, `def:metals-markets`, `def:money-market-reference-rates`, `def:commodity-indices-risk-return`.

### dealer models and information review source gaps worked because of the access barriers

Recorded in *dealer models and information review follow-up (second)* below.

### Sources, 2026-10-16

Supplied by the user (folder `reading_materials/`, not committed; SHA-256 in parentheses): Bloomberg Commodity Index methodology, February 2026, direct download (c63d3919\dots 7469); CME Clearing Advisory 23-082, browser print to PDF, not byte-identical (3eaafc64\dots 86ff); S\&P GSCI Methodology, August 2026, browser print (92f688ee\dots 08b0); \emph{Why S\&P GSCI?}, November 2024, browser print (00dd63d2\dots e994); Estrella and Trubin (already read). Read directly: the Board's H.15 data package; Treasury's daily par-yield files; NBER's chronology; the ARRC minutes of 9 March 2023; CME Submission 24-271 (CFTC filing); the CFTC chairman's LIBOR keynote; Treasury refunding statements SM-538 and JS-1490; NY Fed Staff Report 441; the ECB's TLTRO page; the PBOC's 2014 announcement (State Council English copy); IMF Country Reports 12/57, 17/44 and 22/92; Brunnermeier, Nagel and Pedersen (NBER w14473, November 2008 PDF); the BIS OTC derivatives bulk file (sha256 49e5b5c5\dots e923); the Ilzetzki--Reinhart--Rogoff workbook (sha256 ab62b84f\dots 6fe4); the UN WPP 2024 age-group file (sha256 a04d7d14\dots 87cd); the OFR's FSI fact sheet and daily data (sha256 6db3785e\dots 67e4); the Federal Reserve's May 2026 \emph{Financial Stability Report}, sec.~4; the JPX market-structure page and 4 April 2022 release; Moscow Exchange's index page; the World Gold Council's full-year 2025 release and jewellery section; the Silver Institute's \emph{World Silver Survey 2026} release; ISDA's Big Bang protocol page with its FAQ. Through the fetching tool only: the BLS CPI schedule (curl refused). Refused or unavailable: CME's rulebook (HTTP 403), opec.org (402 and 403), the ISM calendar (login), the IMF AREAER overview and database (403, login), the Census Bureau's International Database API (key required), EUR-Lex and curia (OMT), the IJCB version of Gagnon et al., Menkhoff et al., the 2014 ISDA Definitions, S\&P's and Goldman Sachs's 2007 note. No reference PDF is committed.

### Checks

`notes/artefacts/multi-asset-systematic-macro/carry-market-statistics-checks.py` (exit 0 with `/opt/homebrew/bin/python3.10`), six sections: FX carry with unequal bases; zero carry of the hedged convexity position; BIS swap shares from `bis-otc-ird-instruments.csv`; UN WPP peak years from `wpp2024-working-prime-age.csv`; the two OFI conventions on one bid move; Foucault, Kadan and Kandel's Proposition~4 against Lehalle and Laruelle's (A.4). `convexity-curve-signals-checks.py` section~2 rewritten for the signal rules (exit 0); `ust_monthly.py` and `h15_monthly.py` rebuild their monthly files byte for byte. The market design and liquidity / dealer models and information / macro markets and pricing reviews scripts rerun unchanged (exit 0). `tools/check_compendium.py --check`: 0 problems; `python3 -B -m unittest discover -s tools`: 14 tests OK. Quotations on added lines (145 distinct) were compared by script with the text of the sources read, including raw copies of the Treasury, PBOC, ECB, Moscow Exchange, World Gold Council, Silver Institute and CFTC pages: 121 matched; the 24 others are legacy wording quoted as such, wording from the audit request, source titles and file names, the OFR table entry split across lines, the workbook's cover date (read in the file), the first follow-up's BIS phrase (fetching tool only) and the Argentina quote (confirmed separately; the script's dollar-sign parsing failed).

### Other files

`notes/log.md`; the Gliner reading note; 21 pathway notes (a paragraph under *Source verification after macro markets and pricing review*, created in `hft-market-design`, `point-in-time-data` and `lob-deep-learning`); `notes/source-review-index.md`; `compendium/front/sources.tex` (29 keys added; `isda-big-bang-2009` amended); `.gitignore` (`reading_materials/`).

### For review

- The inversion rules (month against episode, onset window $t+1$ to $t+12$, provisional outcomes) and the six 1968--2005 month misses.
- The fee-mapping between Foucault, Kadan and Kandel and Lehalle and Laruelle, and the Cont--Cucuringu--Zhang order-flow convention.
- Facts read only through the fetching tool (BLS CPI dates) or from browser-printed copies (CME, S\&P).
- The decision-time handling of TAQ correction records stated in `data:market-data-levels`.

## dealer models and information review follow-up (second): four source gaps worked in the second macro markets and pricing review follow-up, 16 October 2026

Worked because CME, OPEC and other sources for the macro markets and pricing review stubs refused access. Resolved: `mod:fkk-make-take-original` (Foucault, Kadan and Kandel's September 2009 working paper, pp.~20 and 23--25 read as page images: the platform maximises $(c_m+c_t)\mathcal R$ for a fixed total fee, and Proposition~4 is Lehalle and Laruelle's (A.4) under $s\Delta=\Delta/2$, $\Gamma=L$, $r=\gamma/\beta$; ``efficient'' therefore means trade-maximising for a given total fee, and the paper's welfare, $\mathcal R L-MC_m-NC_t$, is a different objective; entry `mod:make-take-fee-speed-race`) and `def:multi-level-ofi` (Cont, Cucuringu and Zhang, arXiv v4: definitions, sample, windows, in- and out-of-sample results, and the negative one-minute forecasting $R^2$; their per-level flow uses the new size when a price moves away, checked on the page image; entry `def:order-flow-imbalance`). Narrowed: `ev:flash-crash-studies` (Kirilenko, Kyle, Samadi and Tuzun read in the accepted manuscript: account classification, HFT volume shares and unchanged HFT inventory behaviour; Menkveld and Yueshen not obtained; entry `ev:may-2010-flash-crash`) and `data:trade-correction-records` (NYSE Daily TAQ specification v4.0: correction indicator codes 00--12 and late-report sale conditions; Holden and Jacobsen not read; entry `data:market-data-levels`). Sources: `fkk-2009`, `wide-cont-cross-impact-ofi` (arXiv), `w5-kirilenko-flash-crash` (Cambridge repository), `nyse-daily-taq-spec`. Checks: second follow-up script, sections~5 and~6.

## Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections, 16 October 2026

Corrections and source checks after the second macro markets and pricing review follow-up (`14c92bc`); earlier records are left as written, and this record supersedes them where they differ, in particular the second follow-up's statement that the CBOT filing's ``April 23'' is the date of a CME press release (*macro markets and pricing review second follow-up*, *The 21 source-based macro markets and pricing review stubs*), which was wrong. No legacy block, entry label or entry count changed (0 legacy blocks; 211 entries). This is source verification, not human review or study: every entry stays *draft*, mastery and consolidation dates are untouched, the guide pin (343d145) is unchanged, and verification statuses were extended only for the passages read.

### Audit corrections

1. **OFI universe selection, `def:order-flow-imbalance`.** Cont, Cucuringu and Zhang (arXiv v4, n.~3, p.~5) selected their 100 stocks by market capitalisation ``as of the most recent market close at the time of our analysis, i.e.\ 2019-12-31'', for a 2017--2019 sample. The entry now states the look-ahead in the choice of universe, separates it from the rolling train/test design (30-minute fits, rolling one-minute forecasts, pp.~11 and 22), and does not call the calculations invalid.
2. **Conversion chronology, `meth:policy-path-ois-futures`.** CME's press release is dated 24 April 2023 (read in Mondo Visione's dated reprint; CME's page and its investor-relations copy returned HTTP 403). The entry separates the processing weekend (close of Friday 14 April, transformation Sunday 16 April), the trade date (Monday 17 April 2023) and the announcement (24 April 2023), and says the filings' ``April 23'' matches none of them, without explaining it. The pathway note and `notes/log.md` carry explicit corrections.
3. **Stale status, same entry.** The Pitfalls paragraph no longer says the advisory was unread or the date partly unresolved. Other entries changed in `14c92bc` were rechecked for ``not read'', ``unverified'' and ``pending'': `def:commodity-indices-risk-return` (``index methodologies not read'' now dated to that stage) and `mod:make-take-fee-speed-race` (``the original paper not read'' replaced by its history) were corrected; qualifications that still apply (the Goldman 2007 note, the Small Bang terms, the 2014 ISDA Definitions, Menkhoff et al.\ at that time, AREAER, H.6, SONIA's reform, Release 33-4412, Hull chap.~6, the World Silver Survey itself) were kept.
4. **Demographic attribution, `def:macroeconomic-indicators`.** The second follow-up's ``a decade of revised migration and fertility assumptions both contribute'' is withdrawn: Gliner's Table~12.2 is ``Source: U.S. Census Bureau'' (p.~424) with no vintage, the comparison is with another publisher's 2024 revision, and no controlled comparison was made. Peaks before about 2012 were historical estimates in both sources (so differences there are not projection assumptions); later ones are projections; no cause is attributed.
5. **Inversion, `meth:curve-trades-carry-rolldown`.** Counts unchanged. The entry now says the episode rule is scored from the last inverted month and ex-post NBER dates and is not a prospective forecasting result, and that the month rule also uses ex-post dating.

### The 35-item queue

Each line gives the outcome, the claim checked and the evidence locator, then what is missing.

*Macro (14)*
- `rule:central-bank-policy-history`, narrowed: OMT not implemented ``more than two years after'' its announcement (Court of Justice, C-62/14, para.~84, CELLAR; Press Release 70/15); the PBC's 11 August 2015 central-parity change (NAFMII Weekly Update, 14 August 2015, p.~1); the Bank of England's first Inflation Report February 1993 and fan chart February 1996 (Quarterly Bulletin, February 1998, pp.~30--31). Missing: the PBOC's current band and RRR history; other central banks' dates for ``first major''.
- `ev:curve-inversion-after-2005`, deferred: no new NBER peak dated as of 16 October 2026; outcomes depend on future dating.
- `data:equity-index-lists-current`, narrowed: Nikkei 225 price-weighted, 225 Prime Market stocks (Nikkei profile page); TOPIX free-float capitalisation-weighted, base 4 January 1968 (JPX page). Missing: the other indices (IDX and JSE pages HTTP 403, Wilshire 404).
- `data:opec-membership-current`, narrowed to a recorded conflict: OPEC's home page navigation (retrieved 2026-10-16) lists twelve members including the UAE; member and press pages HTTP 403. Missing: OPEC's own statement on the UAE.
- `data:metals-market-shares-current`, narrowed: platinum 2025 demand 8,671 koz, automotive 35.0, jewellery 25.5, industrial 26.1, investment 13.3 percent; South Africa 71.2 percent of refined mine supply (WPIC Platinum Quarterly Q2 2026, Table~1; check script section~7). Missing: copper and aluminium (ICSG timed out), LME (HTTP 403) and COMEX terms.
- `data:us-release-schedules-2026`, blocked: ISM calendar and report pages redirect to a member login.
- `ev:sovereign-restructurings-after-2006`, blocked: no named dataset with a dated Argentine default count obtained (Reinhart's data page has no static links; the BoC--BoE database measures amounts from 1960).
- `conv:cds-standard-contract`, blocked: the 2014 ISDA Definitions are sold by ISDA.
- `ev:carry-crash-skewness`, resolved: Menkhoff, Sarno, Schmeling and Schrimpf, accepted version (City repository): 48 currencies, November 1983--August 2009, net of bid--ask (sec.~II, pp.~8--9); H/L 7.23 percent, skewness $-1.03$, Sharpe 0.74; developed 5.72, $-0.92$, 0.56 (Table~I, p.~45); volatility, not skewness, prices the cross-section (sec.~V.C, pp.~28--29). The journal version not compared.
- `data:post-libor-funding-stress-measures`, deferred: a CP minus SOFR OIS series needs SOFR OIS rates not found in public data.
- `conv:treasury-bund-futures-current-specs`, narrowed: the 10-year note basket from CBOT Submissions 22-468 (6\textonehalf\ to 7\textthreequarters\ years from September 2023) and 25-099 (6 years 6 months to under 8 years; reopenings from March 2026), both from cftc.gov. Missing: TU, FV, US, UB and tick sizes (CME rulebook HTTP 403).
- `conv:brent-wti-contract-terms`, narrowed: CL grade and Cushing delivery from NYMEX Submission 23-057 (cftc.gov). Missing: contract size and trading terms, post-2023 amendments.
- `conv:henry-hub-contract-terms`, narrowed: Rule 220104 delivery from NYMEX Submission 16-080 (cftc.gov). Missing: size, trading terms, later amendments; EIA LNG data.
- `conv:cbot-ice-ag-contract-terms`, resolved for CBOT: corn, soybean and wheat terms from the chapter text reprinted in CBOT Submission 24-443 (filed 16 December 2024, effective 2 January 2025). Amendments after January 2025 not checked.

*dealer models and information review follow-ups (2)*
- `ev:flash-crash-studies`, narrowed: the staff report's sec.~I, printed pp.~12--17 (depth, the no-bust range, aggressive and passive fills, the fundamental imbalance, cross-market interviews). Missing: Menkveld and Yueshen (INFORMS subscription; SSRN HTTP 403; SMU bot check) and the equities sections.
- `data:trade-correction-records`, blocked: Holden and Jacobsen (journal subscription, SSRN HTTP 403, SMU record without file, Indiana page 401/404); Daily TAQ v4.0 field~8 rechecked, silent on the 10 and 11 records' time.

*order books and order flow / dealer models and information reviews (19)*
- `conv:order-instruction-venue-rules`, narrowed: CME wiki pages (Order Qualifiers v3, Cancel on Disconnect v7, Matching Algorithm Steps v5) through the public REST interface; MIAX PEARL Rule 2616(a)(5) from SR-PEARL-2021-35 (86~FR 43279). Missing: Nasdaq Rule 4703 (HTTP 403), other venues.
- `conv:dmm-obligations-current`, narrowed: NYSE Rules 104 and 107B in NYSE's rulebook compilation (last modified 9 May 2019); later filings listed (84~FR 30262, 84~FR 51205; 2023 proposal withdrawn, 89~FR 56456). Missing: the current consolidated text; other venues.
- `res:trade-sign-accuracy`, narrowed: Jurkatis, BoE SWP 896, pp.~1--5 and 12--14, with LR, EMO and CLNV computed (check script section~5). Missing: Lee and Ready (1991), Ellis et al.\ (2000) (subscriptions).
- `res:queue-reactive-models-hlr`, resolved: arXiv v2, pp.~4--20; invariant law and estimator checked (section~4). The journal version not compared.
- `ev:imbalance-placement-latency`, narrowed: Lehalle and Mounjid arXiv v4, pp.~3--9 and 18--19. Missing: a numerical out-of-sample effect size and a calibrated latency price.
- `ev:ofi-forecast-horizons`, narrowed: LOBCAST arXiv v2, pp.~1--10. Missing: Kolm, Turiel and Westray (Wiley and SSRN HTTP 403).
- `meth:lob-signal-transaction-usefulness`, narrowed: Briola et al.\ arXiv v4, pp.~7--8 and 22--25 ($p_T$ is assumption-free, not after costs). Missing: a source for the checklist and a costed test of our own signal, which no reading can supply.
- `meth:refresh-time-covariance`, narrowed: Barndorff-Nielsen, Hansen, Lunde and Shephard, CREATES RP 2008-63, Definition~1, Assumptions~1--2, sec.~5.3; simulated (section~1). Missing: Hayashi and Yoshida (2005) (Project Euclid bot check).
- `res:time-rescaling-theorem`, narrowed: Brown et al.\ (2002), pp.~329 and 331 (finite window, KS bands). Missing: the half-line statement in a point-process text.
- `ev:simulator-realism-metrics`, resolved: Vyetrenko et al.\ arXiv v1, pp.~4--8; Noble, Rosenbaum and Souilmi arXiv v1, pp.~2, 8--13.
- `res:frequent-batch-auctions`, resolved: QJE secs.~VII--VIII, pp.~1594--1611; 2013 NBER version n.~33; $\delta/\tau$ and $\epsilon/(2\tau)$ simulated (section~2).
- `rule:tick-size-regimes-current`, resolved: Delegated Regulation (EU) 2017/588 and amendments 2019/443, 2023/960; MiFIR Art.~17a (2019/2033 Arts.~63 and 67; replaced by 2024/791 Art.~1(16)); Directive 2024/790 Art.~1(8); table checks (section~6).
- `ev:tick-size-primary-studies`, blocked: the five studies are behind journal subscriptions; the Goldstein--Kavajecz working-paper link returned 404 and the Internet Archive rate-limited the lookup.
- `conv:eu-pre-trade-waiver-thresholds`, resolved: MiFIR Art.~4 (original and 2024/791 Art.~1(3)); RTS~1 Arts.~5--8 and Annex~II with 2019/442, 2023/944 and 2025/1246; amendment list from a CELLAR metadata query.
- `rule:us-market-wide-circuit-breakers-current`, resolved for the rules named: 87~FR 23296, 23291; 91~FR 59278, 64439; LULD 89~FR 77203, 91~FR 51515, 65016. Other exchanges' 2022 filings and the 21st, 22nd, 25th, 26th and 28th LULD amendments only listed.
- `rule:eu-si-national-transposition`, narrowed: CELLAR national-measures metadata (66 measures, 24 Member States; none from France, Spain or Romania); Ireland S.I. 436/2025 regs~1 and 4(c); Malta L.N. 218/2025 (page image). Missing: other Member States' texts, Malta's route, ESMA guidance (SI data page behind a login).
- `rule:cat-current-status`, resolved as of October 2026: 91~FR 13410, 2164, 16284, 20945 and 90~FR 44910. The court's opinion and the technical specifications not read.
- `ev:circuit-breaker-effects`, narrowed: Hautsch and Horvath, CFS WP 571, pp.~1--17 and 40--41. Missing: price-limit and market-wide-halt studies; the journal version.
- `ev:dark-pool-price-discovery`, narrowed: Zhu (RFS 2014), pp.~747--770; Buti, Rindi and Werner, June 2010 working paper (Internet Archive capture), pp.~2--16. Missing: the published Buti--Rindi--Werner version and its price-efficiency results.

Totals: 9 resolved, 19 narrowed, 5 blocked, 2 deferred. The six macro empirical-test stubs stay open: no specified experiment was run.

### Sources, 2026-10-16

Saved in the ignored `reading_materials/` with source URL, retrieval date, version, acquisition method and SHA-256 in `sources_2026-10-16.json` (67 files listed; none committed). Read: arXiv papers (Cont--Cucuringu--Zhang v4, Huang--Lehalle--Rosenbaum v2, Lehalle--Mounjid v4, LOBCAST v2, Briola et al.\ v4, Vyetrenko et al.\ v1, Noble--Rosenbaum--Souilmi v1); author or institutional copies (Zhu; Budish--Cramton--Shim, QJE via UMD and the 2013 NBER version; Brown et al.; Barndorff-Nielsen et al.; Jurkatis; Hautsch--Horvath; Menkhoff et al.); the Buti--Rindi--Werner 2010 working paper from the Internet Archive; EU texts through CELLAR (2014/600, 2017/587, 2017/588, 2019/442, 2019/443, 2019/2033, 2023/944, 2023/960, 2024/791, 2025/1246, the Gauweiler judgment) and the national-measures SPARQL endpoint; the Irish Statute Book; legislation.mt (page image); curia's Press Release 70/15; Federal Register documents through its API (MWCB, LULD, CAT, NYSE and MIAX filings); CFTC-hosted CBOT and NYMEX certifications (22-468, 25-099, 24-443, 23-057, 16-080); CME's client wiki through its REST interface; NYSE's rulebook compilation; WPIC; the Bank of England's Quarterly Bulletin; NAFMII's weekly update; Nikkei, JPX and OPEC pages; the staff report's sec.~I (local copy). Through the fetching tool only: ESMA's 10 April 2025 news item. Refused or unavailable: cmegroup.com (press release, rulebook), investor.cmegroup.com, SSRN, Wiley (Kolm et al.), INFORMS and SMU (Menkveld--Yueshen), Holden and Jacobsen, Project Euclid (Hayashi--Yoshida), JSTOR/JFQA (Lee--Ready, Ellis et al.), the tick-size studies, Nasdaq's rulebook, LME, ICSG (timeout), IDX and JSE, opec.org member pages, the ISM, ESMA's SI data page. Paywalls, logins and bot checks were not bypassed.

### Checks

New `notes/artefacts/execution-market-making/market-estimators-rules-checks.py` (numpy; exit 0 with `/opt/homebrew/bin/python3.10`), seven sections: refresh time and Hayashi--Yoshida against previous-tick sampling (refresh-time realised covariance 0.39 against 0.60, 0.60 with one lead and lag, Hayashi--Yoshida 0.59, previous tick at 1/5000 0.02); batch-auction $\delta/\tau$ and $\epsilon/(2\tau)$; convergence-rate arithmetic; Model~I invariant law and estimator; LR, EMO and CLNV on trades inside the spread and interpolated times; the RTS~11 and RTS~1 tables; platinum shares. The hand example in section~1 was corrected while writing (refresh times 2, 4, 7, 9). Existing scripts unchanged and passing: market design and liquidity review, dealer models and information review, macro markets and pricing review, the two macro markets and pricing review follow-ups. No yield data or aggregation code changed; `h15_monthly.py` and `ust_monthly.py` rebuild their CSVs byte-identically. Quotations on new lines: 197 distinct, 171 matched by script; two non-verbatim quotes found by the script were corrected; the 26 unmatched are titles, LaTeX-escaped strings, legacy wording and the checkpoint's own phrase.

### Other files

Pathway notes (22) with a paragraph under *Source verification after macro markets and pricing review* and updated stubs; reading notes created for seven catalogue readings and updated for `wide-budish-cramton-shim`; `notes/source-review-index.md`; `notes/log.md`; `compendium/front/sources.tex` (45 keys added).

### For review

- The universe-selection and validation-design cautions stated for Cont--Cucuringu--Zhang and Briola et al.
- The refresh-time simulation result and its reading against Barndorff-Nielsen et al.'s kernel.
- The OPEC membership conflict, the NYSE rule compilation's date, and the CFTC-filed contract texts used in place of CME's rulebook.
- The EU transposition statement, which covers Ireland and Malta only.

## Second source follow-up of the order books and order flow / macro markets and pricing reviews queue, 16 October 2026

Works the 24 items left unresolved and not deferred by the previous record (*Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*, commit `9cc18eb`): its 19 narrowed and 5 blocked items, from local copies obtained for this pass (author and institutional copies, official chapter PDFs downloaded through a browser, and browser exports of web rulebooks and calendars). It also rechecks one resolved item (`conv:cbot-ice-ag-contract-terms`) against the current chapters. The two deferred items (`ev:curve-inversion-after-2005`, `data:post-libor-funding-stress-measures`) and the six macro empirical-test stubs stay open. No legacy block, entry label or entry count changed (0 legacy blocks; 211 entries). This is source verification, not study or human review: every entry stays *draft*, mastery and consolidation dates are untouched, the guide pin (343d145) is unchanged, and verification statuses were extended only for the passages read.

### Statements superseded

Earlier records are left as written; where they differ, this record supersedes them:

- that Holden and Jacobsen, Lee and Ready, Hayashi and Yoshida, Kolm, Turiel and Westray, and Menkveld and Yueshen were unread or unobtainable, and that the tick-size studies were all blocked (the Goldstein--Kavajecz working paper is now read, and Harris (1994) in part);
- that the ISM calendar, Nasdaq Rule 4703, NYSE's current Rule 104, CME's TU, FV, US and UB chapters and the CL and NG contract sizes were not read;
- that the UAE's departure from OPEC was reported only by secondary sources: the UAE's own announcement and EIA's analysis are now read, with the conflict documented below;
- that ``ninth default'' was not checked: it is now attributed to the CRS;
- that the copper and aluminium shares and the COMEX and LME terms were not checked;
- that ESMA's final report on SI notifications was not read;
- that the later amendments to Rule~104 were those of June and September 2019: the current amendment history lists six more, in January 2020, June 2021 and four in 2022, the last on 22 November 2022.

### Corrections of fact

- **Gliner's 2-year Treasury tick is out of date** (`conv:government-bond-futures`). CBOT Chapter~21 now sets one-eighth of a 32nd (\$7.8125) on \$200,000 face, against Gliner's quarter (\$15.625). His FV, TY, US and UB ticks match the current chapters. The chapters are undated, so when the change happened was not established.
- **Attribution of the aluminium shares.** The IAI/MPP strategy credits its p.~15 figures to a 2020 World Economic Forum and Accenture report and the same figures on p.~26 to the IAI Material Flow Model (accessed January 2022). The preparation manifest attributed them to the Material Flow Model only.
- **Working-paper date.** The Kolm, Turiel and Westray SSRN copy is dated 6 August 2021 on its title page, not 5 August as the preparation manifest and prompt gave.
- **The ISM rule has exceptions.** The first- and third-business-day rule, counted against federal holidays, misses January (an ISM holiday on 2 January) and April's Services date (6 April, which skips Good Friday). The entry now states both.

### The 24 items

Each line gives the outcome, then the claim checked, the source version and the locator, then what is missing.

*Resolved (9)*
- `data:us-release-schedules-2026`: ISM 2026 calendar, browser export of the page (p.~1). Every listed date is reproduced by the rule except the two exceptions above (`contract-specifications-statistics-checks.py`, section~5). Missing: nothing for the entry's claim; other years must be read from each year's calendar.
- `ev:sovereign-restructurings-after-2006`: three attributed counts, not merged.
  - CRS IF10991 v6 (15 June 2020), pp.~1--2: nine external defaults since 1816; May 2020 is the ninth.
  - Reinhart, NBER w15815 (March 2010), Figure~3a table, printed p.~16, checked as an image: seven external and five domestic episodes to 2009.
  - Fitch, *Sovereign 2020 Transition and Default Study* (27 May 2021), pp.~2--3: rating defaults in 2001, 2014, 2019 (twice) and 2020.
  - Missing: none for the entry; the counts remain method-dependent.
- `conv:treasury-bund-futures-current-specs`: CBOT Chapters 18--21 and~40, official chapter PDFs (undated; footnotes ``Revised March 2008; January 2009''), Rules xx101.A--xx102.C. Covers face value, deliverable bands and ticks, and the TU discrepancy (section~1). Missing: the date of the TU tick change.
- `conv:brent-wti-contract-terms`: NYMEX Chapter~200, official PDF (undated), Rules 200101 and 200102.B--F. Covers 1,000 barrels with a 2 percent tolerance, \$0.01, last trading day and ASTM D-6377. Missing: the amendment history.
- `ev:flash-crash-studies`, for the entry's claims:
  - Menkveld and Yueshen, SSRN version dated 15 November 2017 (earlier titled ``Anatomy of the Flash Crash''), printed pp.~2--7 and~15, and the undated online appendix, sec.~A. The *Management Science* version was not compared, and the 2014 thesis chapter was not used.
  - The staff report's secs.~II.2.e and II.3.a, printed pp.~58 and 64--65, from the local text copy.
  - Missing: the rest of secs.~II--III.
- `conv:order-instruction-venue-rules`, for the venues named: Nasdaq Equity~4, browser export of 16 October 2026, Rules 4703(e) (export pp.~19--20), 4756(a)(3) (p.~29) and 4757(a)(1) (p.~30). Missing: other venues, which are outside the entry's scope.
- `conv:dmm-obligations-current`, for NYSE: current Rules 104 and 107B, browser exports, amendment histories to 22 November 2022 and 25 January 2023. Covers the ETP 25 percent requirement and unchanged percentages. Missing: what each later amendment changed.
- `ev:ofi-forecast-horizons`: Kolm, Turiel and Westray, SSRN version of 6 August 2021, PDF pp.~5--31, with Fig.~8 read as an image. Missing: the *Mathematical Finance* version, not compared.
- `meth:refresh-time-covariance`: Hayashi and Yoshida, *Bernoulli* 11(2), author copy, pp.~367--375. Condition~C and Definition~3.1 (p.~368) were checked by page image, as were Theorem~3.1 and Remarks~3.3--3.4. Missing: none for the entry.

*Narrowed further (8)*
- `data:equity-index-lists-current`: FTSE/JSE ground rules v9.3 (September 2026), secs.~1.7.1 and 4.5.1, pp.~4 and~13; FT Wilshire 5000 methodology WI-METH-001 (January 2026), sec.~1.1, p.~4. Missing: the Jakarta Composite (IDX HTTP 403) and the rest of Gliner's table.
- `data:opec-membership-current`: four kinds of evidence, kept apart (`def:crude-oil-markets`).
  - The announced exit: WAM, 28 April 2026, effective 1 May 2026.
  - EIA's classification: its analysis of 23 June 2026 and its live glossary, which lists eleven members (section~4 recomputes 31 percent).
  - OPEC's own pages: navigation still listing twelve, and a 3 May 2026 release silent on membership.
  - The statutory rule: Statute (2021 edition), Art.~8A, PDF p.~12, under which a withdrawal takes effect at the start of the next calendar year.
  - Missing: OPEC's statement on the date and legal effect.
- `data:metals-market-shares-current`.
  - Copper: ICSG *World Copper Factbook 2025*, pp.~5 and~48 (end-use chart as an image; 2024, preliminary); ICA 2023 dataset, World sheet rows 48--51 (2022, copper content of semis).
  - Aluminium: IAI/MPP (April 2023), PDF pp.~15 and~26, sector shares of about 2020.
  - Contracts: COMEX Chapters 107 and 111--113; LME Rulebook as of 13 October 2026, Part~6, pp.~6-1 and 6-11 (section~3).
  - Missing: aluminium shares by country, and the LME's minimum price fluctuations (Rule~11.3.7 leaves them to the Exchange).
- `conv:henry-hub-contract-terms`: NYMEX Chapter~220, official PDF (undated), Rules 220101--220104. Missing: EIA LNG data and the amendment history.
- `data:trade-correction-records`, from blocked: Holden and Jacobsen, JF 69(4), published version (author copy). Read: sec.~III, p.~1758, n.~16, n.~12, p.~1754, eq.~(16) and n.~29, pp.~1766--1767. Missing: the Internet Appendix with the full screens, and the time in the TAQ 10/11 records.
- `res:trade-sign-accuracy`: Lee and Ready, JF 46(2), University at Buffalo course scan without a text layer. OCR was used only to search; pp.~734 and 736--739 were checked as page images. Table~I gives agreement rates, not accuracy. Missing: Ellis, Michaely and O'Hara (2000) and the other accuracy studies.
- `ev:tick-size-primary-studies`, from blocked.
  - Goldstein and Kavajecz, Rodney L.~White Center working paper of 16 September 1998 (not the 2000 JFE version), PDF pp.~2, 5 and 9--15.
  - Harris, RFS 7(1), partial course scan, pp.~149 and~155 as images. PDF p.~27 renders only in part, and pp.~28--30 show only the watermark.
  - Missing: Bacidore et al., Jones and Lipson, Ahn et al., Harris (1996), and Harris's projection tables.
- `rule:eu-si-national-transposition`: ESMA final report ESMA74-2134169708-7780 (10 April 2025), paras~8 and 21--23 and Next Steps. These are draft ITS, not law. Missing: other Member States, Malta's route, and whether the Commission adopted the ITS.

*Still blocked (1)*
- `conv:cds-standard-contract`: ISDA's release of 21 February 2014 (2 pp.) was read. It is not the 2014 Definitions, which are sold by ISDA. Missing: the operative wording.

*Unchanged, no new source in this pass (6)*
- `rule:central-bank-policy-history`, `ev:imbalance-placement-latency`, `meth:lob-signal-transaction-usefulness`, `res:time-rescaling-theorem`, `ev:circuit-breaker-effects` and `ev:dark-pool-price-discovery`. The gaps recorded by the previous record stand.

*Rechecked (resolved item)*
- `conv:cbot-ice-ag-contract-terms`: CBOT Chapters 10, 11 and~14, official PDFs (undated), agree with the 24-443 reprint. Location differentials are split at December 2027 and March 2028 for corn, and November 2027 and January 2028 for soybeans.

Queue totals after this pass, over the 35 items of the previous record: 18 resolved, 14 narrowed, 1 blocked, 2 deferred. The six macro empirical-test stubs stay open: no specified experiment was run.

### Sources

Listed with source URL, retrieval date, version, acquisition method and SHA-256 in `reading_materials/sources_audit_9cc18eb_2026-10-16.json` (47 files; ignored; none committed). Thirty source keys were added to `compendium/front/sources.tex`. Catalogue readings are cited by their catalogue keys with the version read in the locator (`wide-holden-jacobsen`, `wide-kolm-deep-ofi`, `w5-menkveld-yueshen-flash`).

Acquisition:
- **Direct downloads:** author and institutional copies, the CRS, NBER, Fitch, ICA, IAI, ESMA, OPEC Statute, ISDA, FTSE Russell and Wilshire files.
- **Official PDFs downloaded through a browser** after direct requests were refused: CME Group chapter files, the LME Rulebook, the ICSG Factbook and the two SSRN papers. No challenge was solved and no login was used.
- **Browser exports of rendered pages:** Nasdaq Equity~4, NYSE Rules 104 and 107B, the ISM calendar and the WAM announcement. These are not publisher PDFs.

Scan limits:
- The Lee--Ready and Harris files are course scans; OCR served only as a search aid.
- Harris's scan is incomplete.

### Checks

New `notes/artefacts/execution-market-making/contract-specifications-statistics-checks.py` (standard library; exit 0 with `/opt/homebrew/bin/python3.10`) has five sections:
1. Treasury tick values.
2. Commodity tick values.
3. Copper groupings and aluminium share sums.
4. EIA's OPEC shares.
5. The ISM business-day rule, with federal holidays and Easter computed and tested on known dates.

The Easter function was wrong in the first draft (it gave 29 March for 2026) and was replaced before use. In `market-estimators-rules-checks.py`, two docstring lines that called the Hayashi--Yoshida paper unread were updated, and the code is unchanged. The other scripts are unchanged and passing.

### Other files

- Eighteen pathway notes have a paragraph under *Source verification after macro markets and pricing review*, with backlog stubs updated or removed.
- New reading notes: `wide-holden-jacobsen`, `wide-kolm-deep-ofi`, `w5-menkveld-yueshen-flash`.
- Also updated: `notes/source-review-index.md`, `notes/log.md` and `compendium/front/sources.tex`.

### For review

- The OPEC membership conflict and the Statute's next-calendar-year rule.
- The TU tick discrepancy and the undated CME chapters.
- The ISM Good Friday inference.
- The three Argentine counts.
- The reading of Kolm et al.'s Fig.~8 values from the plot.
- The page images used for Lee--Ready, Harris, Hayashi--Yoshida, Reinhart and ICSG.

## source verification (2026-10-17): four audit corrections, the 15 active leftovers of the order books and order flow / macro markets and pricing reviews queue, 19 older backlog items and the six macro empirical stubs

Starting state checked: `main` at `9e403e3`, equal to `origin/main`, clean; guide pin `343d145` (unchanged); 211 entries, all draft; no legacy block. This record covers 40 distinct items in three groups, kept apart in the counts below, plus the two deferred items. It is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them.

### Audit corrections

1. **Kolm, Turiel and Westray, Table~3** (`def:order-flow-imbalance`; `notes/readings/wide-kolm-deep-ofi.md`). The statement that the CNN-LSTM with book inputs did better ``for 23 to 45 of the 115 stocks'' is withdrawn. In the SSRN version of 6 August 2021 a Table~3 entry is the number of stocks with a significantly positive $t$-statistic (1 percent) minus the number with a significantly negative one (sec.~4.1.2, PDF p.~19; caption, PDF p.~21; checked as page images); the CNN-LSTM row runs from 70 to 93. These are net counts, and 115 minus them is not a count of losing stocks. The source is ambiguous: the caption and text also read an entry $X$ as OF outperforming ``for $X$ stocks'', the caption tests a ``loss difference'' where the text tests a difference in $R^2_{OS}$, and the text's ``about 40 stocks'' (PDF p.~20) cannot be derived from the net counts. No exact count is stated.
2. **Kolm et al., the decline after two average price changes.** Now cited to Fig.~8 (PDF p.~28, horizons to ten); Fig.~2 (PDF p.~18) stops at two. The text on Fig.~8 says $R^2_{OS}$ ``plateaus at around two average price changes'' (sec.~4.3, PDF p.~27); the plot falls from about 1.5 to roughly 0.64 percent; both are recorded.
3. **Ultra Bond spreads** (`conv:government-bond-futures`). CBOT Rule 40102.C: outright one 32nd (\$31.25); intermonth spreads ``one quarter of one thirty-second of one point (equal to \$7.8125 per contract)''. Check added to `contract-specifications-statistics-checks.py`, section~1.
4. **`lob-deep-learning` status.** The pathway note's ``none of the pathway's required readings has been read'' is superseded: specified sections of Briola et al., LOBCAST, Kolm et al.\ and Cont, Cucuringu and Zhang were source-checked on 16 October 2026; full study, LOBCAST's supplement (SUP sec.~7, its trading simulation), Briola et al.'s Appendices~A--C and a costed checkpoint remain incomplete. Its backlog item no longer says the readings are ``unread''.

### Statements superseded

- That López de Prado's chap.~7, Lo (2002), the deflated Sharpe ratio paper, Grinold and Kahn's chap.~10, Boyd et al.'s multi-period paper, Brunnermeier and Pedersen, RTS~6, the Knight Capital order, FIX's message definitions, the PFMI glossary annex, Grossman and Miller's NBER paper (eqs.~(16)--(19)), Holden and Jacobsen's Internet Appendix and a half-line statement of the time-change theorem were unread or unobtainable: each is now read for the passages named below.
- That no EU algorithmic-trading obligation could be stated (`meth:automated-trading-operational-controls`): RTS~6 is now read through CELLAR.
- The second source follow-up's description of Buti, Rindi and Werner's published version as the source of the dark-pool stub: the published paper is ``Diving into Dark Pools'', \emph{Financial Management} 51(4), 961--994 (2022) by its bibliographic record; their 2017 JFE paper is a different, theoretical paper.

### The 40 items

Each line gives the outcome, the evidence (version and locator) and what remains.

*Group A: the 15 active leftovers of the 35-item queue*
- `data:equity-index-lists-current`, narrowed further: NSE Indices' methodology, September 2026, PDF p.~19 (Nifty~50 float-adjusted cap-weighted); Borsa Istanbul's ground rules, April 2020, secs.~2.2--2.3, 2.20, 3.1. Remaining: IDX (403 again), S\&P DJI (403, also via the fetching tool), stoxx.com (TLS certificate not verifiable; not forced), Euronext (403), Hang Seng (404 at the address tried) and the rest of Gliner's Table~8.1.
- `data:opec-membership-current`, reviewed, unchanged: OPEC's home navigation still lists the UAE (2026-10-17); releases of 4, 6 and 12 October 2026 silent; press-release index 403; no Secretariat statement found. Prerequisite: OPEC's statement, or 1 January 2027 under Statute Art.~8A.
- `data:metals-market-shares-current`, narrowed further: USGS \emph{Mineral Commodity Summaries} 2026, aluminum, p.~2 (2025 smelter output 74.0 Mt, China 45.0, about 61 percent). Remaining: consumption by country; LME minimum price fluctuations.
- `conv:henry-hub-contract-terms`, narrowed further: EIA's annual LNG export series (release of 30 September 2026); NYMEX Submissions 17-048 (administrative amendments to Chapter~220, effective trade date 13 March 2017) and 18-465 (Rule~589). Remaining: filings after 2018 (search not exhaustive).
- `data:trade-correction-records`, narrowed further: Holden and Jacobsen's Internet Appendix (author-hosted), MTAQ program, PDF p.~19 (\texttt{where corr eq 0 and price gt 0}). Remaining: their DTAQ code (linked file 404) and the time carried by TAQ 10/11 records.
- `res:trade-sign-accuracy`, reviewed, unchanged (subscription): no open copy of Ellis, Michaely and O'Hara (Cambridge paywall; HKU record without file).
- `ev:tick-size-primary-studies`, reviewed, unchanged (subscription): Jones and Lipson's Columbia working paper is listed by RePEc only with a publisher link; the others not found.
- `rule:eu-si-national-transposition`, narrowed further (slightly): CELLAR title searches (2026-10-17) found no implementing act on SI notifications under MiFIR Art.~15(5) (the ITS's legal basis, ESMA report Annex~II, PDF p.~43); Delegated Regulation 2026/482 noted by title. Non-adoption not established; other Member States remain.
- `rule:central-bank-policy-history`, reviewed, unchanged: a BIS-hosted 2018 RBNZ speech dates the RBNZ Act (February 1990), not its first inflation forecast; PBOC band and RRR pages not found.
- `ev:imbalance-placement-latency`, resolved as to the evidence asked (merged into `def:queue-imbalance`): Gould and Bonart, arXiv v1, secs.~4--5.2 and Tables~4--5 (out-of-sample AUC 0.752--0.805 large tick, 0.581--0.642 small tick; random 80/20 split of 2014 Nasdaq data); Moallemi and Sağlam, revision of 5 February 2013, eq.~(1), Corollary~1, p.~23 calibration reproduced. A costed placement rule stays with `lob-deep-learning`.
- `meth:lob-signal-transaction-usefulness`, narrowed further: Briola et al., sec.~7, pp.~22--23 (four backtest assumptions) and Table~7, pp.~16--17; costed-test protocol written into `def:order-flow-imbalance`, not run (LOBSTER samples now behind a request and terms). Remaining: capacity and crowding sources; the test itself on licensed data.
- `res:time-rescaling-theorem`, resolved with a caveat (merged into `def:order-event-point-processes`): Laub, Taimre and Pollett, arXiv v1, Theorem~5, p.~18, restating Daley and Vere-Jones's Proposition~7.4.IV; Daley and Vere-Jones not read.
- `ev:circuit-breaker-effects`, narrowed further: Kasahara and Yamada, JPX Working Paper~52 (10 April 2026), abstract and sec.~3 (TSE pauses reduce volatility and spreads; IV within one regime), against Hautsch and Horvath. Remaining: price-limit and market-wide-halt studies; the published Hautsch and Horvath.
- `ev:dark-pool-price-discovery`, reviewed, unchanged (paywall): see *Statements superseded*.
- `conv:cds-standard-contract`, still blocked: ISDA's 2014 Definitions Protocol (21 August 2014, PDF pp.~1 and~13) dates the switch (Implementation Date the later of 22 September 2014 and a cut-off date; effectiveness condition met 17 September 2014); the Definitions' operative wording is sold by ISDA.

*Group B: 19 older backlog items*
- `conv:pro-rata-allocation-rules`, resolved for CME Globex (merged into `mech:order-matching-pricing`): Matching Algorithm Steps, version~5 (2 June 2026), retained REST export; CME's examples recomputed.
- `conv:session-carry-over`, resolved for CME Globex (merged into `mech:order-lifecycle`): Order Qualifiers, version~3; GTC timestamp retention and no TOP over a weekend from the Steps page.
- `rule:spoofing-securities-markets`, advanced (narrowed): new entry; MAR Art.~12 and Annex~I and Delegated Regulation 2016/522, Annex~II, sec.~1, point~5(e), through CELLAR; 15 U.S.C.~78i(a). Remaining: FINRA's rules (404, then 429), Rule 10b-5, enforcement.
- `rule:block-print-trade-through-current`, narrowed: Rule 611(b), eCFR text for 15 October 2026, merged into `def:block-trade` (no block-size exception). Remaining: FINRA reporting rules and exchange cross rules.
- `rule:mifid-rts6-algorithmic-controls`, resolved (new entry): Delegated Regulation 2017/589, Arts.~5--17 and~29; CELLAR SPARQL (no amending act; German-only corrigendum of 28 July 2017).
- `ev:quant-implementation-failures`, resolved (new entry): SEC Releases 34-70694 and 33-9181 (Internet Archive captures of 29 October 2013 and 20 February 2011; sec.gov returned 403), against Narang pp.~195--196.
- `mech:order-state-reconciliation`, resolved (new entry): FIX Orchestra files (FIX Latest EP312; FIXT EP247; commit \texttt{cd24169}); RTS~6 Art.~17(3); Knight order paras.~16 and~21; offline illustration only.
- `res:avellaneda-stoikov-infinite-horizon`, resolved (merged into `mod:avellaneda-stoikov`): sec.~2.3, p.~219, page image; the printed ask breaks the problem's symmetry at $q=0$ and is recorded as an apparent misprint (own derivation and quadrature).
- `res:avellaneda-stoikov-exact-quotes`, resolved (merged): sec.~3.1, eqs.~(15)--(19), pp.~220--221.
- `res:grossman-miller-free-entry`, resolved (merged into `mod:grossman-miller`): NBER WP 2641, eqs.~(16)--(19), printed pp.~18--19 (page image). Eq.~(19) fixes $t=e^{2ac}-1$; $M$ falls with $c$ and rises with each variance, but its response to $a$ is not monotone (own algebra), so the paper's ``the smaller $a$'' holds only for $2ac>1.594$.
- `res:grossman-miller-market-structure`, resolved (merged): printed pp.~9--10 (page image).
- `meth:convex-cost-portfolio-optimisation`, resolved (merged into `mod:portfolio-transaction-cost-function`): Boyd et al.\ 2017, secs.~2.3, 4.7, 5.3.
- `def:clearing-settlement`, resolved (merged into `def:transaction-costs`): PFMI Annex~H, pp.~174--178; the CPMI web glossary renders by script and was not compared.
- `meth:purged-embargoed-cross-validation`, resolved (new entry): AFML chap.~7 and secs.~6.3.3--6.4; Bergmeir et al.\ working paper; Cerqueira et al.\ arXiv v1. The printed ``$\Phi_i\cap\Phi_j=\emptyset$'' (p.~106) is an apparent misprint; Snippet~7.3 keeps boundary-touching labels.
- `meth:sharpe-ratio-standard-error`, resolved (new entry): Lo (2002), pp.~36--41.
- `meth:deflated-sharpe-ratio`, resolved (new entry): Bailey and López de Prado, author version of 31 July 2014, pp.~7--11; the 2026 López de Prado--Porcu paper not obtained.
- `meth:forecast-scaling-ic`, resolved (new entry): Grinold and Kahn, 2nd ed., chap.~10, pp.~261--271; `eq-grinold-1994` not obtained (publisher login).
- `data:holdings-insider-filing-lags`, resolved (new entry): eCFR texts for 15 October 2026, 15 U.S.C.~78p (2023 edition), 88~FR 76896; Velu et al.'s footnotes predate the 2024 deadlines.
- `mod:margin-liquidity-spiral`, resolved (new entry): Brunnermeier and Pedersen, RFS Advance Access version, pp.~1--5, 8--9, 18--19.

*Group C: the six macro empirical stubs.* For each the hypothesis, data, sample, timing, benchmark, costs and pass rule were written into the script's docstring before results were computed.
- `ev:backwardation-scarcity-or-premium`, empirically tested (bounded): EIA futures (contracts 1, 2, 4; series end 5 April 2024) and inventories; WTI August 1987--March 2024 ($n=439$), Henry Hub 2015--March 2024 ($n=111$). Scarcity supported (backwardation on inventory deviation: WTI $\beta=-0.112$, NW $t=-5.9$; gas $-0.124$, $t=-4.4$). Premium not supported (return on backwardation: WTI $t=0.1$, OOS $R^2=-2.2$ percent, Clark--West $t=-0.4$; gas $t=-0.6$, OOS too short). Exploratory, added after the first run: WTI backwardated months $+2.2$ against $-0.3$ percent ($t=3.4$); gas the reverse. `notes/artefacts/commodity-storage-curves/`.
- `ev:fx-valuation-factors-oos`, empirically tested for relative PPP only: nine currencies against USD, forecasts 1985 to 2021--2026; full-sample slopes negative 9/9 at 12 months, but pooled OOS $R^2$ against a random walk $-2.0$ (1 month) and $-15.3$ percent (12 months); value portfolio $+0.09$ percent a year spot (1985--2025), $-0.17$ with interest differentials (2002--2025). Not supported. `notes/artefacts/fx-determination-forecasting/`.
- `ev:regime-asset-responses-tested`, empirically tested for the recession row only: real-time Sahm-type rule on RTDSM unemployment vintages 1965Q4--2025Q4 (241 vintages; 53 signals; 2026 vintages skipped for the missing October 2025 rate); no sign supported at $\abs{t}>2$; equities and defensives against the map; ex-post NBER windows match the map's signs without significance. `notes/artefacts/macro-regimes-stock-bond/`.
- `ev:global-macro-returns-after-2013`, open, protocol recorded: macro hedge-fund index data behind registration (BarclayHedge, Eurekahedge, HFR; 2026-10-17).
- `ev:practitioner-rules-tested`, open, protocol recorded: needs trade-level data.
- `ev:equity-index-value-signal`, open, protocol recorded: needs point-in-time country valuation data (MSCI licensed).

*Deferred, tracked separately.* `ev:curve-inversion-after-2005`: NBER's table (last updated 14 March 2023) still ends at the February 2020 peak; deferral retained. `data:post-libor-funding-stress-measures`: no public dated SOFR OIS series; deferral retained.

### Counts

- Original 35-item queue: before this batch 18 resolved, 14 narrowed, 1 blocked, 2 deferred. Of the 15 active leftovers: 2 resolved, 7 narrowed further, 5 reviewed and unchanged, 1 still blocked. Queue now 20 resolved, 12 narrowed, 1 blocked, 2 deferred.
- Older backlog (19 items, separate): 17 resolved, 2 narrowed.
- Macro empirical stubs (6, separate): 3 empirically tested within stated bounds (one row, one factor, two contracts; the untested remainder stays in each backlog), 3 open with executable protocols and named missing data.
- All 40: 19 resolved, 9 narrowed or advanced, 5 reviewed without change, 1 blocked, 3 empirically tested, 3 protocol only.
- Entries 211 $\to$ 221 (new: `meth:purged-embargoed-cross-validation`, `meth:sharpe-ratio-standard-error`, `meth:deflated-sharpe-ratio`, `meth:forecast-scaling-ic`, `data:holdings-insider-filing-lags`, `mod:margin-liquidity-spiral`, `rule:mifid-rts6-algorithmic-controls`, `mech:order-state-reconciliation`, `ev:quant-implementation-failures`, `rule:spoofing-securities-markets`); legacy blocks 0; all draft.

### Sources

Listed with URL, retrieval date, version, acquisition route and SHA-256 in `reading_materials/sources_source-verification_2026-10-17.json` (96 files; ignored; none committed). Routes: direct downloads of author, institutional and official copies; the eCFR versioner API; GovInfo; CELLAR content negotiation and SPARQL; the FIX Trading Community's GitHub repository at a pinned commit; Internet Archive captures for the two SEC orders; public data from EIA, FRED, the Philadelphia Fed and Ken French's library. Local library copies outside the repository: AFML (Wiley 2018), Grinold and Kahn (2nd ed.), Narang (3rd ed.), Velu et al. Nineteen keys were added to `compendium/front/sources.tex`. Refused or unavailable, not bypassed: sec.gov (403), finra.org (404 then 429), S\&P DJI (403), stoxx.com (TLS certificate unverifiable), Euronext (403), IDX (403), LME notices, ISDA's 2014 Definitions (sold), journal paywalls (JFQA, JFE, \emph{Financial Management}, JPM), LOBSTER samples (request and terms), macro hedge-fund indices (registration). The Lo (2002) copy is hosted by a Berkeley student organisation; its provenance is not established, though it carries the journal pagination.

### Checks

New, all exit 0 with `/opt/homebrew/bin/python3.10`: `market-making-lob/model-checks.py` (Avellaneda--Stoikov infinite horizon by quadrature, eqs.~(18)--(19), Grossman--Miller free entry); `statistical-learning-foundations/cv-checks.py`; `backtest-inference/sharpe-checks.py`; `equity-long-short-construction/forecast-checks.py`; `point-in-time-data/filing-checks.py`; `funding-crowding/spiral-checks.py` (an illustration); `model-governance-controls/reconciliation-check.py` (an offline illustration); `execution-market-making/cme-allocation-checks.py`; `execution-market-making/commodity-production-latency-checks.py`. Extended: `contract-specifications-statistics-checks.py` (Ultra Bond spread tick). The seven existing scripts (market design and liquidity review, dealer models and information review, macro markets and pricing review, the two macro markets and pricing review follow-ups and the two source follow-ups) rerun and pass. Empirical scripts (`backwardation_test.py`, `fx_ppp_oos_test.py`, `regime_recession_test.py`) reproduce their printed results and rebuild their derived panels byte for byte (SHA-256 6953ecd1\dots, da1bb9d4\dots, 82ce2b97\dots). `h15_monthly.py` and `ust_monthly.py` were not rerun: neither their code nor their inputs changed. The first drafts of three checks were corrected before use: a vacuous variance check and a first-order test that did not shrink $\gamma^2\sigma^2/\omega$ (model checks), and a mislabelled message in the CV check. `tools/check_compendium.py --check`: 0 problems; `python3 -B -m unittest discover -s tools`: 14 tests OK.

### Other files

Pathway notes (28) with a paragraph under *Source verification after macro markets and pricing review* (created where absent) and backlogs updated; reading notes created for eleven catalogue readings (`wide-lo-sharpe`, `alpha-dsr`, `alpha-grinold`, `exp-boyd-multiperiod-trading`, `exp-pfmi`, `exp-brunnermeier-pedersen-liquidity`, `wide-mifid-rts6`, `wide-knight-capital`, `s6-fix`, `rf-bergmeir-hyndman-koo-2018`, `rf-cerqueira-torgo-mozetic-2020`) and updated for `alpha-afml`, `s6-stoikov`, `wide-holden-jacobsen`, `w2-briola-lob-guide`, `s3-velu` and `wide-kolm-deep-ofi`; `notes/log.md`; `notes/source-review-index.md`; `compendium/README.md`; `compendium/front/sources.tex`.

### For review

- The Avellaneda--Stoikov ask and the AFML p.~106 condition, both read as misprints from the surrounding text and own algebra.
- The non-monotone response of Grossman and Miller's market-maker count to risk aversion (own algebra against the paper's ``of course'').
- The Kolm et al.\ Table~3 ambiguity, recorded rather than resolved.
- The three empirical tests' design choices (expiry mapping of EIA's continuous contracts, monthly-average FX rates and revised CPI, the Sahm-type rule on quarterly vintages) and the exploratory WTI sign effect.
- Sources read in non-publisher hosts: Lo (student-organisation host), the SEC orders (Internet Archive), Brunnermeier and Pedersen (Advance Access PDF).

## method validation (2026-10-17): eight audit repairs (three empirical tests rerun) and a source-review coverage

Starting state checked: `main` at `820517a`, equal to `origin/main`, clean; guide pin `343d145` (unchanged); 221 entries, all draft; no legacy block. This is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them. No protocol here is preregistered: protocols written in docstrings and committed together with results are labelled as such, and v2 corrections were chosen after v1's results had been seen.

### Stage 1: audit repairs

1. **Energy test** (`notes/artefacts/commodity-storage-curves/`; `def:contango-backwardation-stocks`). v1 (script, results, panel) moved unchanged to `v1-2026-10-17/`; v2 replaces it.
   - *Contract identity and complete holding periods.* v1 paired 28 March 2024 with the incomplete month ending 5 April 2024, when contract 1 (May WTI) was not 28 March's contract 2 (June). v2 uses only complete months (data continuing into the next month) and requires the delivery month of C2 at $t$ to equal that of C1 at $t+1$ under NYMEX Rules 200102.F and 220102.F, on the trading calendar of EIA's own series. A roll check (score of $C_1(d+1)$ against $C_2(d)$) supports the WTI rule in every five-year block from 1985 and the Henry Hub rule from about 1997. Before then the gas data roll two or three days earlier, so gas identity is required under expiries 3, 5 and 6 business days before the delivery month. The 2020--2024 WTI block's score at offset $-1$ (19.5) reflects April 2020's negative prices on nine roll days.
   - *Samples.* The premium regression, its out-of-sample test and the timing rules now use all identity-valid months (WTI 1985-01 to 2024-02, 470; gas 1994-01 to 2024-02, 362). The scarcity and joint regressions use the inventory sample (WTI 1987-08 to 2024-02, 438; gas 2015-01 to 2024-02, 110). The gas out-of-sample test, impossible in v1, now runs from January 2004 (242 forecasts).
   - *Inventory availability.* v1's fixed five-day lag let a Wednesday month-end use a gas report released on the Thursday. v2 dates reports from EIA's published schedules (local copies retrieved 2026-10-17: WPSR Wednesday 10:30 ET, WNGSR Thursday 10:30 ET; holiday releases up to Thursday noon or Friday 10:30, and Monday 29 December 2025, 5 p.m., for the week ending 19 December 2025). Convention: usable at settlement $t$ if $t\ge F+6$ days (crude) or $F+7$ (gas), or $F+11$ when 25 December or 1 January falls in $F+1..F+7$. Schedules before 2025 were not obtained. Sensitivity: $F+14$ throughout, with unchanged conclusions (WTI $t=-5.8$, gas $-4.0$).
   - *Statistical against executable.* The regressions and the settlement-to-settlement timing rule are labelled closing-price associations. An executable variant forms the signal at settlement $t$ and trades the next trading day's settlement in the same contract, exiting on the first trading day after $t+1$, with two ticks round trip. Settlement fills are an assumption. For Henry Hub, NYMEX's TAS order type covered the spot and second through seventh months by May 2019 (Submission 19-158); earlier availability was not established.
   - *Message.* v1's ``months with $|r|\ge50\%$ dropped'' was wrong: they were counted, not dropped. v2 says retained.
   - *Results, v2* (v1 in brackets). Pre-specified verdicts unchanged.
     - Scarcity: WTI $\beta=-0.111$, $t=-5.9$ ($-0.112$, $-5.9$); gas $-0.114$, $-4.3$ ($-0.124$, $-4.4$).
     - Premium slope: WTI $+0.02$, $t=0.1$ ($+0.05$, $0.1$); gas $-0.05$, $-0.3$ ($-0.19$, $-0.6$).
     - Out-of-sample $R^2$: WTI $-1.8\%$, Clark--West $t=-0.4$ ($-2.2\%$, $-0.4$); gas $-0.8\%$, $-1.4$ (not computable in v1).
     - Exploratory, not pre-specified: WTI backwardated against contango months $+1.95$ against $-0.22\%$, difference $t=2.95$ ($+2.17$ against $-0.33$, $t=3.4$); gas $-1.32$ against $-0.90$, $t=-0.2$ ($-4.96$ against $-0.38$, $t=-1.9$).
     - Executable timing rule, net of two ticks: WTI $+0.92\%$ a month, Newey--West $t=2.34$; gas $+0.58\%$, $t=0.9$.
   - Focused checks: `energy-checks.py`, testing CLJ24, CLK24 and NGJ24 expiries on a synthetic calendar, v1's bad pairing, the terminal month, report availability, samples, wording, execution and v1's preserved hash.
2. **FX test** (`notes/artefacts/fx-determination-forecasting/`; `meth:fx-valuation-signals`). v1 kept in `v1-2026-10-17/`.
   - *Eligibility.* Predictor eligibility now uses only price levels known at $t$. Outcomes use spot rates alone, so future CPI is no longer needed: JPY's 12-month forecasts gain the last 12 months.
   - *Stale-data rule.* Monthly CPI must be exactly two months old. Quarterly CPI is accepted 4 to 6 months after its quarter ends. v1 carried 2025Q1 AUD and NZD CPI to September 2026; v2 stops them at September 2025.
   - *Reporting.* Ages and effective endpoints are reported: JPY ends August 2021, monthly-CPI currencies May--June 2025, AUD and NZD September 2025. Expanding-training cutoffs are unchanged and checked against an independent OLS fit.
   - *Results* (v1 in brackets): pooled 12-month OOS $R^2$ $-14.9\%$, Clark--West $t=-0.3$ ($-15.3\%$, $-0.4$); 1-month $-2.0\%$ ($-2.0\%$). Portfolio unchanged in substance: spot $+0.09\%$ a year, with interest differentials $-0.17\%$. It is now labelled a statistical return on monthly averages with interbank-rate carry, not an executable result. Neither pass rule is met.
   - Focused checks: `fx-checks.py`.
3. **Regime test** (`notes/artefacts/macro-regimes-stock-bond/`; `def:macro-regime-asset-map`). v1 kept in `v1-2026-10-17/`.
   - *Window definition.* v1's NBER window is stated as \emph{any overlap} and preserved exactly (checked). \emph{All months inside} is added as a sensitivity, not chosen for significance.
   - *Dollar.* TWEXBMTH (goods only, to December 2019) and DTWEXBGS (goods and services, new weights and composition, from January 2006; FEDS Note of 15 January 2019 and H.10 of 19 February 2019, read) are tested separately. Goods-only is primary; v1's splice is reported with its January 2020 definition break.
   - *Inference.* Real-time and ex-post blocks are printed separately. Newey--West (4 quarterly lags) $t$ and episode counts are added as an inference sensitivity chosen before computing.
   - *Real-time results.* No sign passes. The goods-only dollar is $+1.11$, Welch $t=1.98$, Newey--West $1.87$, 6 episodes; goods-and-services $-0.39$, $t=-0.3$.
   - *Ex post.* Any-overlap results equal v1's, with Baa spread Welch $t=1.78$ but Newey--West $2.46$. On all-months windows the yield ($-0.41$, $t=-2.2$) and spread ($+0.45$, $t=+2.9$) signs pass Welch $|t|>2$. The earlier claim that no ex-post sign reaches $|t|=2$ is therefore restricted to any-overlap windows with Welch $t$.
   - Focused checks: `regime-checks.py`.
4. **Sharpe inference** (`meth:sharpe-ratio-standard-error`). Lo's eq. (5), p. 38 (page image), asserts $2\sigma^4$ under ``finite mean $\mu$ and variance $\sigma^2$''. The entry now states:
   - a finite fourth moment and $\sigma>0$ are required;
   - the general IID variance is $V=1-\gamma_3SR+(\gamma_4-1)SR^2/4$, and $1+SR^2/2$ is its normal-moment case;
   - Lo's own eqs. (25)--(26), p. 42, set normal moments explicitly.

   The wording at eq. (5) is recorded as an overstatement in the source, not edited. Lo's aggregation is scoped to additive (summed) returns with a consistently aggregated benchmark (eq. (16) and note 7). Zero autocovariances suffice, so IID is not necessary. Compounded simple returns differ (0.515 against $\sqrt{12}\times0.155=0.538$ in a lognormal example). Independent checks in `sharpe-conditions-checks.py`: a skewed two-point distribution (Monte Carlo 1.70 against general 1.68, normal-moment 1.02), Student-$t_3$ ($T\operatorname{Var}$ rising from 2.5 to 10.0 with $T$), and an uncorrelated but dependent process obeying $\sqrt{12}$.
5. **Forecast scaling** (`meth:forecast-scaling-ic`). Grinold and Kahn's appendix proves a best linear projection (Proposition 1, pp. 287--288); the conditional expectation follows only under joint normality (Proposition 2, p. 289); n. 1, p. 263, calls the notation ``somewhat loosely'' used. The entry now:
   - states that equality needs an affine conditional mean, for example joint normal or elliptical returns;
   - distinguishes uncorrelated from mean-independent errors;
   - gives the counterexample $r=g^2-1+\varepsilon$, with zero IC but a conditional mean explaining two thirds of the variance (`projection-checks.py`).
6. **Cross-validation** (`meth:purged-embargoed-cross-validation`). The performance plateau as $k$ grows (AFML pp. 106--107) is now the source's heuristic, with examples of leakage that does not grow with $k$; the overlap and endpoint corrections stand; provenance and time-valid evaluation are stated as necessary.
7. **Order reconciliation** (`mech:order-state-reconciliation`, `reconciliation-check.py`, corrected in place). The first version released every terminal reconciled order for resubmission, including a filled one. Now reconciled state, remaining authorised quantity and a valid intent are separate. The cases are:
   - a filled order: nothing proposed;
   - a partially filled cancelled order: 180 of 300 proposed with a valid intent, nothing with a withdrawn intent;
   - an order in Pending Cancel: unresolved, nothing proposed;
   - duplicate reports: applied once;
   - a missing execution: a break of 150, nothing proposed until it is resolved.

   The illustration remains offline and synthetic.
8. **Filing timestamps** (`data:holdings-insider-filing-lags`). There was no literal ``three-minute'' text; the entry's single ``acceptance time'' convention was the defect.
   - *Four timestamps.* The entry now separates EDGAR acceptance, the official filing date (17 CFR 232.13(a)(2) and (a)(4): 5:30 p.m., or 10 p.m. for Forms 3--5, 144 and Schedules 13D, 13G and 14N; 232.12(c) hours; 232.13(b) adjustment), public dissemination and the user's first-observed time.
   - *No fixed delay.* None of the texts read guarantees a fixed delay. The convention is first-observed time, else the start of the next business day after acceptance.
   - *Later information.* Amendments, and 13F information withheld under 15 U.S.C. 78m(f)(4) and Rule 24b-2 and released later, keep their own timestamps.
   - Checks: `filing-timestamp-checks.py`, which shows that a deadline-day 13F transmitted at 17:31 is filed the next day.

*Misprint review.* The candidates were re-examined, not silently changed:
- Avellaneda--Stoikov ask: a 2025 preprint prints the same ask without derivation, inconsistent with its own Lemma 2 and Definition 3; still an apparent misprint, quoted unchanged.
- AFML's $\Phi_i\cap\Phi_j=\emptyset$ (p. 106): unchanged, apparent misprint.
- Lehalle and Laruelle's ``$=1$'': unchanged.
- Lo's eq. (5): new, recorded as an overstatement.
- Grossman and Miller: the non-monotone response stays an own-algebra finding against the paper's wording.

### The source-review coverage

Outcome per identifier (evidence, then what remains). Repairs overlapping the queue (items 16--18) are counted once.

*A. Carry-forward source gaps (15)*
1. `data:equity-index-lists-current`, narrowed further: Hang Seng Index methodology v2.3, July 2023 (free-float cap-weighted, 100 constituents, 8 percent cap). Remaining: IDX, S\&P DJI (403 on a second URL), STOXX (no response), Euronext (403), and others.
2. `data:opec-membership-current`, unchanged: no new evidence since the same-day check; prerequisite unchanged.
3. `data:metals-market-shares-current`, unchanged and blocked: LME contract specifications 403 on a second route; consumption by country not found.
4. `conv:henry-hub-contract-terms`, narrowed further: NYMEX Submissions 19-158 (TAS months, 20 May 2019) and 19-198 (settlement procedures, 4 September 2019). Later filings not found.
5. `data:trade-correction-records`, narrowed further: NYSE Daily TAQ Client Specification v4.0, sec. 3, codes 00--12. The 01 records carry the original time and the corrected data; the 12 records carry the correction time and the original data. The time on 10 and 11 records is not stated.
6. `res:trade-sign-accuracy`, narrowed: Ellis, Michaely and O'Hara's abstract from Cambridge Core (76.4, 77.66, 81.05 percent). The body is paywalled.
7. `ev:tick-size-primary-studies`, unchanged: paywalls. One search found only the RePEc record of Goldstein and Kavajecz's working paper.
8. `rule:eu-si-national-transposition`, unchanged: no new route.
9. `rule:central-bank-policy-history`, narrowed: PBOC English pages, with a managed-float statement without a band and RRR cuts of 27 September 2024 and 15 May 2025 (0.5 point each). Whether the 2014 band has changed, and the RBNZ dates (403), remain.
10. `meth:lob-signal-transaction-usefulness`, unchanged: licensed message data.
11. `ev:circuit-breaker-effects`, narrowed: SEC Release 34-93365 on the four March 2020 Level 1 halts and the SRO working group's conclusions. The study itself (nyse.com 404) and price-limit studies remain.
12. `ev:dark-pool-price-discovery`, narrowed: Comerton-Forde and Putniņš, accepted manuscript (ASX 2008--2011; harmful above about 10 percent dark volume; blocks benign). Buti, Rindi and Werner (2022) remains unobtained.
13. `conv:cds-standard-contract`, still blocked: the ISDA 2014 Definitions are sold.
14. `rule:spoofing-securities-markets`, narrowed further: Rule 10b-5 (eCFR), FINRA Rules 2020 and 5210.03 (Types 1 and 2, from 3 April 2017). Enforcement actions remain (sec.gov 403).
15. `rule:block-print-trade-through-current`, narrowed further: FINRA Rule 6380B(a), 10 seconds, late designation and modifiers, version of 30 March to 5 December 2026. Exchange cross rules remain.

*B. Macro empirical scopes (6)*
16. `ev:backwardation-scarcity-or-premium`: repaired and retested (Stage 1, item 1). Untested remainder: other commodities and hedging-pressure readings.
17. `ev:fx-valuation-factors-oos`: repaired and retested (Stage 1, item 2). Gliner's other factors untested.
18. `ev:regime-asset-responses-tested`: repaired and retested (Stage 1, item 3). Other rows of the map untested.
19. `ev:global-macro-returns-after-2013`: newly tested within stated bounds. The protocol was recorded in the earlier batch before any data were seen. Data choices were fixed before computing: estimated months excluded, French Mkt-RF as benchmark, sample ending July 2026.
   - Data: BarclayHedge's public page (Barclay Global Macro Index, net), January 2022 to July 2026 (55 months).
   - All months: mean 0.68 percent a month, annualised Sharpe 0.76.
   - Down months (24): $-0.39$ percent ($t=-1.5$), correlation $+0.29$ (CI $-0.13$ to $0.62$), beta $+0.13$.
   - Ten worst benchmark months: index $-0.79$ against benchmark $-6.49$.
   - Crisis protection is not supported. The window from 2014 needs the history behind registration. Script: `notes/artefacts/multi-asset-systematic-macro/global_macro_down_months_test.py`.
20. `ev:practitioner-rules-tested`: open with its protocol; missing input is trade-level data of a discretionary macro book.
21. `ev:equity-index-value-signal`: open with its protocol; missing input is point-in-time country B/P and E/P with publication dates (MSCI licensed). A U.S.-only valuation test would answer a different question and was not run.

*C. Existing backlog items (29)*
22. `res:nonlinear-hawkes-stability`, narrowed: Theorems 4--5 as restated by Zhu (arXiv:1304.7531v3, pp. 33--34), merged into `mod:hawkes-order-flow`. The original was refused by bot protection.
23. `meth:multiple-testing-control`, narrowed with a new entry: Romano and Wolf's working paper, with an own Monte Carlo (error rates 0.014--0.046; power 0.57--0.74). White and Benjamini--Hochberg were not read.
24. `meth:backtest-protocol`, blocked: Research Affiliates served a gate page and SSRN returned 403. A third-party copy of unverified provenance was not used.
25. `meth:dependent-resampling-drawdowns`, narrowed: own AR(1) check (shuffle 0.53 and blocks 0.85, against 0.99). Politis and Romano not obtained.
26. `ev:out-of-sample-r2-scale`, narrowed: Welch and Goyal's Table 1 (page image). Campbell and Thompson refused (429).
27. `meth:bitemporal-reference-tables`, resolved as a new entry (Fowler 2021; own check).
28. `ev:delisting-survivorship-rewriting`, narrowed: Shumway's abstract. Full text 403; Elton, Gruber and Blake and Ljungqvist et al. not obtained.
29. `meth:alternative-dataset-assessment`, unchanged and blocked: CAIA 404, SSRN 403, the J.P. Morgan report not public.
30. `meth:time-valid-ml-experiment-record`, narrowed with a new entry: Kelly et al., NBER WP 35247. Levy and Jansen's third edition not read.
31. `meth:signal-mixing-vs-integration`, resolved (merged): Fitzgibbons et al., AQR reprint.
32. `ev:august-2007-quant-unwind`, resolved (merged): Khandani and Lo, NBER WP 14465.
33. `mod:volatility-targeting-deleveraging`, narrowed: Moreira and Muir and Pedersen merged. The 1.5--2 times estimate is unverified.
34. `meth:overlap-crowding-measure`, narrowed: Pedersen gives no measure; Chincarini et al. paywalled.
35. `rule:us-short-sale-margin-and-price-test`, resolved (merged): 12 CFR 220.12(c), FINRA 4210(c), 17 CFR 242.201.
36. `ev:securities-lending-fees-evidence`, resolved (merged): Sikorskaya, author version of 27 April 2026, Table 1.
37. `mech:options-clearing-exercise-assignment`, narrowed: SEC Release 34-56845 (2007). OCC rulebook 403.
38. `def:option-complex-orders`, narrowed: Cboe Rule 5.33 from SEC Release 34-92729. Cboe rulebook 403; no evidence on multi-leg costs.
39. `ev:credit-derivative-swap-trading-structure`, narrowed: 17 CFR 50.4, 37.9 and 37.10. MAT lists and trading shares remain.
40. `rule:eu-mifir-bond-transparency-level1`, resolved (merged): Regulation 2024/791 and Delegated Regulation 2025/1246 (OJ, 3 November 2025).
41. `rule:uk-bond-transparency`, blocked: FCA 403; legislation.gov.uk returned an empty 202.
42. `meth:gips-composite-presentation`, resolved as a new entry (GIPS 2020).
43. `res:no-trade-region`, narrowed: Guasoni and Muhle-Karbe's survey. Davis and Norman not obtained.
44. `mod:black-litterman`, resolved as a new entry: the 1991 Goldman Sachs paper, with the appendix formula by page image. The 1992 FAJ version was not compared.
45. `meth:portfolio-covariance-estimation`, narrowed with a new entry: Ledoit and Wolf's review WP; factor-model estimation unread.
46. `meth:var-es-estimation-methods`, resolved as a new entry: Christoffersen 2nd ed. and own simulation. QRM and Kupiec not read.
47. `mod:theory-of-storage`, blocked: Working and Brennan paywalled; no open copy found.
48. `meth:time-varying-hedge-ratio`, blocked: Baillie and Myers and Lien and Tse paywalled.
49. `ev:why-firms-hedge`, narrowed: Froot, Scharfstein and Stein's NBER WP read by OCR. Tufano and Jin and Jorion not obtained.
50. `ev:trend-following-evidence`, resolved (merged): Moskowitz, Ooi and Pedersen's abstract and Hurst, Ooi and Pedersen's Exhibit 1 (page image).

*Deferred, tracked separately and not in the tally.* `ev:curve-inversion-after-2005`: no new NBER dating is known; the trigger was not rechecked online. `data:post-libor-funding-stress-measures`: no public dated SOFR OIS series was found or sought anew. Both deferrals are retained.

### Counts

- All 50: 10 resolved (4 as new entries); 23 narrowed (3 of them with new entries); 4 unchanged; 7 blocked; 3 repaired and retested; 1 newly tested within bounds; 2 open with protocols.
- New entries: 7. Entries 221 $\to$ 228: `meth:multiple-testing-control`, `meth:bitemporal-reference-tables`, `meth:time-valid-ml-experiment-record`, `meth:gips-composite-presentation`, `mod:black-litterman`, `meth:portfolio-covariance-estimation`, `meth:var-es-estimation-methods`. Legacy blocks 0; all entries draft.

### Sources

Listed with URL, retrieval date, version and SHA-256 in `reading_materials/sources_method-validation_2026-10-17.json` (58 files; ignored; none committed), with local library copies (Grinold and Kahn, AFML, Christoffersen) and reused batch-40 files noted. Routes: eCFR versioner API; GovInfo and Federal Register public-inspection PDFs (SEC releases); CELLAR (local copies of the EU texts); finra.org (the version marked as selected on each page); CFTC filings; official pages of the PBOC, Hang Seng Indexes, NYSE, EIA and the Federal Reserve; author, NBER, arXiv and university repositories; a BarclayHedge public page. Two copies sit on course pages (Black and Litterman 1991 at Duke, Hurst et al. at Yale), and one paper (Froot, Scharfstein and Stein) was read by OCR. Refused or unavailable, not bypassed:
- regulators and standard setters: sec.gov, the FCA (403), legislation.gov.uk (empty 202), ISDA (sold);
- market operators: theocc.com, cboe.com, S\&P DJI, Euronext and the LME (403), and stoxx.com (no response);
- research hosts: SSRN (403), Project Euclid (bot protection), Harvard DASH (429), CAIA (404), the nyse.com MWCB study (404), the BYU full text (403);
- publishers and data: journal paywalls; hedge-fund index histories behind registration.

### Checks

New, all exit 0 with `/opt/homebrew/bin/python3.10`:
- `commodity-storage-curves/energy-checks.py`, `fx-determination-forecasting/fx-checks.py`, `macro-regimes-stock-bond/regime-checks.py`;
- `backtest-inference/sharpe-conditions-checks.py`, `multiple-testing-checks.py` and `drawdown-resampling-checks.py`;
- `equity-long-short-construction/projection-checks.py`;
- `point-in-time-data/filing-timestamp-checks.py` and `bitemporal-check.py`;
- `portfolio-construction/black-litterman-check.py` and `shrinkage-check.py`;
- `risk-tail-systemic/var-backtest-check.py`.

`model-governance-controls/reconciliation-check.py` was corrected. All existing numerical checks rerun and pass; `afml-checks.py` needs statsmodels, installed for the run in a scratch library.

Empirical scripts:
- *Byte-for-byte reproduction.* `backwardation_test.py` (3.7 s), `fx_ppp_oos_test.py` (1.4 s), `regime_recession_test.py` (0.9 s) and `global_macro_down_months_test.py` (0.6 s) reproduce their printed results and derived panels byte for byte on rerun. SHA-256 prefixes: backwardation panel 2eab519e, FX panel 2379a3a3, regime panel 294292e2, global macro panel dbbd9544.
- *v1 preserved.* The v1 scripts, run from a copy, still reproduce their v1 outputs (6953ecd1, da1bb9d4, 82ce2b97).
- *Not rerun.* `h15_monthly.py` and `ust_monthly.py`: code and inputs unchanged.
- *Validity separate from reproducibility.* Timing, eligibility, contract identity and units were checked by the focused checks, not inferred from reproducibility.

`tools/check_compendium.py --check`: 0 problems. `python3 -B -m unittest discover -s tools`: 14 tests OK.

### Build

Clean `latexmk -pdf compendium.tex` after `latexmk -C`: exit 0, 307 pages. Seven overfull or underfull boxes introduced by new text were fixed by rewording; after the last edit, 0 overfull and 0 underfull boxes and no LaTeX warnings remain, apart from the inherited `page.i` duplicate-destination warning. Pages with the repaired energy and regime passages and the new entries were inspected as images.

### Other files

- Pathway notes (31) received a dated paragraph and updated backlogs. Resolved items were removed, narrowed and blocked stubs rewritten, and new entries listed.
- Reading notes: created for 17 catalogue readings and updated for `wide-lo-sharpe`, `alpha-grinold`, `alpha-afml` and `s6-stoikov`.
- Also updated: `notes/log.md` (entries and open questions; no dates of mastery or consolidation), `notes/source-review-index.md`, `compendium/front/sources.tex` (25 keys added) and v1 READMEs.

### For review

- The energy test's expiry inference for Henry Hub before 1997, the inventory availability convention, and the executable variant's settlement-fill assumption.
- The FX stale-data limits (2 months; 4--6 months).
- The regime sensitivities: the all-months window and Newey--West with 4 lags.
- The global macro test's data choices, and that only 2022--2026 was available.
- Lo's eq. (5) reading; the Avellaneda--Stoikov ask after the 2025 preprint.
- Sources read from course pages, author hosts and OCR.

## empirical extensions (2026-10-17): six audit repairs and a source-review coverage

Starting state checked: `main` at `12e634a`, equal to `origin/main`; guide pin `343d145` (unchanged); 228 entries, all draft; no legacy block. This is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them. Protocols for the empirical extensions were written before the results were computed and are committed with them, so none is a preregistration.

### Stage 1: audit repairs

1. **Filing availability** (`data:holdings-insider-filing-lags`; `filing-timestamp-checks.py`, corrected in place). method validation (2026-10-17)'s fallback, the start of the next business day, was not conservative: EDGAR's *Determine the Status of My Filing* page (dated 4 June 2024, reviewed 31 October 2024; Internet Archive capture of 5 October 2026, sec.gov refusing automated retrieval) gives after-cutoff submissions a 6:00 a.m. filing date on the next business day and dissemination only "the next business day", with no time. Availability is now the recorded dissemination time, else the first-observed time, else unknown (the record does not enter the panel). A separate lower bound (acceptance, or 6:00 a.m. on the next business day after holidays for after-cutoff forms outside the same-day list) only detects look-ahead. The check adds a holiday case, a Form 4 before 10 p.m., a Schedule 13D/A and a first observation earlier than the bound, flagged as a data error.
2. **FIX Done for Day** (`mech:order-state-reconciliation`; `reconciliation-check.py`, corrected in place). OrdStatus 3 was treated as terminal. FIX 4.4's state matrices (OnixS reprint of Appendix D, scenarios A.1.b and H.1.a) show a GTC order continuing after Done for Day and being restated the next day (ExecRestatementReason 1, GT renewal). Terminal states are now Filled, Canceled, Rejected and Expired; Done for Day ends the lifetime only for a Day order where the venue's rule says so (a named configuration flag). New cases: a GTC order with Done for Day and zero leaves (not released), and a Day order.
3. **Expected shortfall** (`meth:var-es-estimation-methods`, Notation; new `es-discrete-check.py`). ES is now defined as the quantile integral $\mathrm{ES}_p=\frac1p\int_0^p\mathrm{VaR}_u\,du$ (Acerbi and Tasche, 2001), which differs from the tail conditional expectation when the distribution has an atom at the quantile. Example: a loss of 100 with probability 0.005 at $p=1\%$ gives VaR $=0$ and ES $=50$.
4. **Sharpe asymptotics** (`meth:sharpe-ratio-standard-error`; new `sharpe-zero-check.py`). A finite fourth moment is sufficient, not necessary: at $SR=0$ the Slutsky argument needs only finite variance. Student-$t_3$ returns at $SR=0$ give a scaled variance of 0.990 (Monte Carlo) and a tail rejection rate of 0.0483 at 5 percent; a non-normal three-point law with skewness 0 and kurtosis 3 gives $T\operatorname{Var}=1.113$ against the normal-moment $1+SR^2/2=1.125$, so normal moments, not normality, are what the simple formula needs. "Only then" was qualified accordingly.
5. **GIPS benchmark exception** (`meth:gips-composite-presentation`). Provision 4.A.1(e) lets a composite present no benchmark when no appropriate one exists, with the reason disclosed under 4.C.31 (PDF pp. 39 and 47, printed pp. 21 and 29); the parallel provisions for pooled funds and asset owners (5.C.30, 6.A.1(e), 6.C.26, 7.C.26, 8.D.4, 8.F.4, 8.H.1) are listed.
6. **Global macro from 2014** (`ev:global-macro-returns-after-2013`; target 27). The BarclayHedge workbook was obtained through the site's public Excel download form (an HTTP POST; SHA-256 `ead890c4…`, matching the audit). The registered window, January 2014 to July 2026 (151 months), gives 53 down months for the benchmark, a mean index return in them of $-0.5217$ percent ($t=-2.9952$, the audit's values), correlation $+0.42$ (CI 0.17 to 0.62). Crisis protection is not supported, more firmly than in 2022--2026, which is kept. The statements that the window needed registration are corrected. Revision check: 0 of the 55 overlapping months differ from the earlier page; the index's weighting and backfill rules are not public. Script `global_macro_down_months_2014_test.py`; v1 (`global_macro_down_months_test.py`) unchanged and reproduced.

### Statements superseded

- The next-business-day availability fallback (method validation (2026-10-17), item 8) is superseded by Stage 1, item 1.
- "Done for Day is terminal" in method validation (2026-10-17)'s reconciliation check is superseded by Stage 1, item 2.
- method validation (2026-10-17)'s ES notation (tail expectation without the atom correction) is superseded by Stage 1, item 3.
- "Only then" for the fourth-moment condition (method validation (2026-10-17), item 4) is qualified by Stage 1, item 4.
- "The window from 2014 needs the history behind registration" (method validation (2026-10-17), item 19) is superseded: the workbook is public through a form.
- In `def:crypto-venue-instrument-structure`, "fewer venues and strikes … not checked" is replaced by the one-venue snapshot (target 34). In the Hawkes entry, "the same stability condition holds" is qualified to $\int|h|<1$ (target 10). In `def:block-trade`, "exchange cross rules … remain open" is replaced by NYSE Rule 127 (target 9).

### The source-review coverage

Outcome per identifier. Wording is short; the entries and pathway notes carry the locators.

*A. Index, contract and record data (4)*
1. `data:equity-index-lists-current`, narrowed: DJIA, Russell 2000, FTSE 100, EURO STOXX 50 and DAX rules read and merged into `def:equity-indices-derivatives`.
2. `conv:henry-hub-contract-terms`, narrowed: a scan of 281 NYMEX filings on the CFTC's listing (September 2019 to October 2026) found one Henry Hub futures filing, Submission 20-166 (spot-month limit), and no Chapter 220 text amendment.
3. `data:trade-correction-records`, narrowed: three earlier Daily TAQ specifications define the correction records alike and give no time for them; Holden and Jacobsen's code archive returns 404.
31. `data:historical-borrow-availability`, narrowed: Nasdaq's daily Regulation SHO threshold files (public from January 2005) merged into `data:derived-market-statistics`; no public point-in-time borrow-fee source found.

*B. Market structure, regulation and execution (12)*
4. `res:trade-sign-accuracy`, unchanged: open versions of Ellis, Michaely and O'Hara and of the later accuracy studies were searched for and not found.
6. `ev:circuit-breaker-effects`, narrowed: Chen, Gao, He, Jiang and Xiong on Shenzhen daily price limits (NBER WP 24014, abstract and sec. 1) merged into `mech:circuit-breakers-trading-halts`.
7. `ev:dark-pool-price-discovery`, narrowed: the published version's abstract (Financial Management 2022) adds 2020: dark pools improve spreads in 2009 but worsen market quality for large caps in 2020; full text not obtained.
8. `rule:spoofing-securities-markets`, narrowed: FINRA Regulatory Notice 17-22 read: Rule 5210.03 has no express intent element and supports an expedited cease-and-desist order; enforcement actions unread.
9. `rule:block-print-trade-through-current`, narrowed: NYSE Rules 76 and 127 (compilation of May 2019) read: a block cross outside the quote trades with the NYSE best bid or offer and better-priced book orders first, then has priority at its price; merged into `def:block-trade`.
18. `mech:options-clearing-exercise-assignment`, narrowed: current OCC Rules 803-805 and 1803 (last modified 19 August 2025, archived copy) read and merged into the options-dealing entry: the rule text names neither random nor pro rata assignment.
19. `def:option-complex-orders`, narrowed: Cboe filing SR-CBOE-2026-081, Exhibit 5 (current Rule 5.33(g) legging text) merged.
20. `ev:credit-derivative-swap-trading-structure`, narrowed: the CFTC's made-available-to-trade filings and TW SEF's 2023 submission merged.
37. `ev:futures-tick-size-evidence`, narrowed: Dayri and Rosenbaum: ten futures in 2009 all large-tick (one-tick spreads for 72.7 to 99.6 percent of trades); merged into `res:spread-determinants`; the equity comparison and depth unchecked.
38. `ev:fx-last-look-fill-reject-evidence`, narrowed: Oomen's accepted manuscript is theory; no measured fill or reject rates found.
39. `ev:market-share-variance-claim`, narrowed: the only formal counterpart in Lehalle and Laruelle is an appendix assumption; no study cited.
47. `ev:block-initiator-asymmetry`, narrowed: Harris gives the rule without a citation; Saar (theory) and Alzahrani et al. (Saudi data) merged.

*C. Backtest inference and machine learning (9)*
11. `meth:multiple-testing-control`, narrowed: Benjamini and Hochberg (1995) and White (2000) read and merged into `meth:multiple-testing-control`; Romano and Wolf unread.
12. `meth:dependent-resampling-drawdowns`, narrowed: White's restatement of Politis and Romano merged; the original and its validity for drawdowns unread.
13. `ev:out-of-sample-r2-scale`, resolved: Campbell and Thompson (NBER WP 11468) read: the $R^2/S^2$ scale and their Table 1 merged into `meth:backtest-evaluation-diagnostics`.
14. `ev:delisting-survivorship-rewriting`, narrowed: Shumway and Warther's abstract (a $-55$ percent substitute delisting return; no Nasdaq size effect after correction) merged into `data:trading-reference-data`; Shumway's full text still refused.
15. `meth:time-valid-ml-experiment-record`, narrowed: He, Lv, Manela and Wu's abstract merged; Levy's full text refused again (Wiley 403).
30. `ev:signal-decay-crowding`, narrowed: two crowding studies read at abstract level measure crowding from holdings or fire-sale dislocations, not from delayed-signal decay; noted in `meth:backtest-evaluation-diagnostics`.
52. `ev:transaction-clock-normality`, narrowed: Murphy and Izzeldin's working paper merged.
53. `ev:meta-labelling-performance`, unchanged: no open out-of-sample evaluation found (arXiv, Crossref and web searched); Joubert's journal articles are paywalled.
54. `meth:fractional-integration-tests`, resolved: MacKinnon and Nielsen's working paper merged into the fractional-differentiation entry.

*D. Microstructure models (2)*
10. `res:nonlinear-hawkes-stability`, resolved: Brémaud and Massoulié (1996) read from an archived copy: a signed kernel is allowed and the condition is on the $L^1$ norm of $|h|$; merged into `mod:hawkes-order-flow`.
51. `meth:hybrid-control-learning-execution`, narrowed: Kolm and Ritter's preprint (archived copy) has no hybrid design; the claim stays unsupported.

*E. Portfolio construction and risk (9)*
16. `mod:volatility-targeting-deleveraging`, narrowed: the ECB's May 2020 box on volatility-targeting strategies merged into `def:common-investor-contagion`.
17. `meth:overlap-crowding-measure`, narrowed: Chincarini, Lazo-Paz and Moneta's abstract (open access, but the publisher refused automated retrieval) merged into `def:common-investor-contagion`; their holdings measure unread.
21. `res:no-trade-region`, blocked: Davis and Norman (1990) has no open copy (arXiv and OpenAlex searched).
22. `meth:portfolio-covariance-estimation`, narrowed: Boyd et al. sec. 3.4 and their backtest's normalised EWMA (half-life 125 days) merged into `meth:portfolio-covariance-estimation`; factor-model estimation and DCC unread.
42. `meth:residual-reversion-strategy`, narrowed: Avellaneda and Lee and Gatev et al. merged into the alpha taxonomy.
43. `ev:value-carry-premia`, resolved: Koijen et al., Asness, Moskowitz and Pedersen and the QMJ paper merged into `def:alpha-model-taxonomy`.
44. `meth:resampled-efficiency`, narrowed: new entry `meth:resampled-efficiency` from the Michauds' authors' version (2007): what is drawn and averaged; out-of-sample evidence only the proponents' simulation.
45. `meth:equal-risk-contribution`, resolved: new entry `meth:equal-risk-contribution` from Maillard, Roncalli and Teïletche.
46. `mod:garch-volatility-forecast`, resolved: new entry `mod:garch-volatility-forecast` from Christoffersen and Hansen and Lunde.

*F. Commodities, rates, credit and governance (8)*
23. `ev:why-firms-hedge`, narrowed: Tufano (1996) and Jin and Jorion (2006) read at abstract level and merged into the hedging entry: neither supports the value channel.
40. `meth:strategy-promotion-criteria`, resolved: new entry `meth:strategy-promotion-criteria` from PRA SS1/23 and SR 26-2.
41. `meth:discretionary-override-governance`, resolved: new entry `meth:discretionary-override-governance` from PRA SS1/23 and SR 26-2.
48. `rule:otc-derivatives-reforms`, narrowed: U.S. rules resolved (17 CFR 23.150-161, 43.3, 45.3) and merged into `mech:otc-clearing-collateral`; BCBS-IOSCO, prudential regulators and EMIR unread.
49. `mod:multi-curve-fra-swap-valuation`, resolved: new entry `mod:multi-curve-fra-swap-valuation` from Hull, with own checks.
50. `ev:term-premia`, resolved: Adrian, Crump and Moench and the New York Fed's file summarised and merged into `mod:forward-rates-fra`.
56. `ev:option-implied-borrow-cost`, resolved: Ofek, Richardson and Whitelaw (NBER WP 9423) merged into `res:synthetic-short-put-call`.
55. `ev:empty-voting-equity-derivatives`, resolved: new entry `ev:empty-voting-equity-derivatives` from Hu and Black and the SEC's 2023 release.

*G. Crypto (5)*
32. `ev:crypto-funding-crowding`, narrowed: BIS WP 1087's dated-futures evidence and its restatements merged; a direct funding-rate study unread.
33. `ev:crypto-dated-futures-carry`, resolved: new entry `ev:crypto-dated-futures-carry` from BIS WP 1087 (archived copy).
34. `def:crypto-options-venue-structure`, narrowed: a one-day Deribit API snapshot (inverse against USDC-settled listings, open-interest concentration) merged into `def:crypto-venue-instrument-structure`; other venues unread.
35. `def:amm-pool-mechanics`, narrowed: new entry `def:amm-pool-mechanics` from the Uniswap v2 and v3 papers; gas costs not covered.
36. `ev:stablecoin-network-settlement-risk`, narrowed: the Federal Reserve's FEDS Note on USDC and SVB merged into `def:crypto-trading-risk-layers`.

*H. Options and volatility (2)*
57. `mod:black-scholes-merton`, resolved: new entry `mod:black-scholes-merton`.
58. `def:implied-volatility-surface`, resolved: new entry `def:implied-volatility-surface`.

*I. Central banks and data definitions (3)*
5. `rule:central-bank-policy-history`, unchanged: only a route was found (RBNZ's pre-1997 statements reposted on a former official's blog); the PBOC band and the full reserve-requirement history were not obtained.
28. `ev:alternative-data-edge-decay`, narrowed: Dessaint, Foucault and Frésard and Farboodi and Veldkamp read at abstract level and merged.
29. `ev:holdings-insider-ratings-signals`, narrowed: Cohen, Malloy and Pomorski (abstract and sec. I) merged.

*J. Empirical extensions (protocol recorded before computing) (4)*
24. `ev:backwardation-scarcity-or-premium`, tested within stated bounds: heating oil added under a protocol recorded before the data: scarcity supported, premium not.
25. `ev:fx-valuation-factors-oos`, tested within stated bounds: the carry factor added under a protocol recorded before the results: forecasts not supported out of sample, a carry portfolio narrowly supported.
26. `ev:regime-asset-responses-tested`, tested within stated bounds: the inflation-shock row tested on real-time CPI vintages under a protocol with two recorded deviations: no response supported.
27. `ev:global-macro-returns-after-2013`, tested within stated bounds: the BarclayHedge window January 2014 to July 2026 run as registered: 53 down months, mean $-0.52$ percent, $t=-3.00$; the registration statements corrected.

*K. Deferral-trigger reviews (2)*
59. `ev:curve-inversion-after-2005`, deferral trigger reviewed, retained: trigger review: no NBER peak after February 2020; 24 of the 27 months lie beyond the longest past announcement lag, 3 months and both episodes within it; retained.
60. `data:post-libor-funding-stress-measures`, deferral trigger reviewed, retained: trigger review: still no free official dated SOFR OIS series; retained.
### Counts

- All 60: 15 resolved (9 as new entries); 35 narrowed (2 of them with new entries: `def:amm-pool-mechanics`, `meth:resampled-efficiency`); 3 unchanged; 1 blocked; 4 tested within stated bounds (three extensions and the global-macro window); 2 deferral-trigger reviews, both retained.
- New entries: 11. Entries 228 $\to$ 239: `mod:black-scholes-merton`, `def:implied-volatility-surface`, `meth:equal-risk-contribution`, `mod:garch-volatility-forecast`, `meth:resampled-efficiency`, `mod:multi-curve-fra-swap-valuation`, `meth:strategy-promotion-criteria`, `meth:discretionary-override-governance`, `ev:crypto-dated-futures-carry`, `def:amm-pool-mechanics`, `ev:empty-voting-equity-derivatives`. Legacy blocks 0; all entries draft.

### Conclusions that changed

- Filing availability: no fixed fallback is conservative; a missing dissemination time means unknown.
- Global macro: crisis protection is not supported over January 2014 to July 2026 ($t=-3.0$), more firmly than over 2022--2026.
- Dark pools: the 2009 association with narrower spreads does not hold for large caps in 2020 (published abstract).
- Nonlinear Hawkes stability with inhibition needs $\alpha\int|h|<1$; "slope at most one, same condition" holds only with the absolute value.
- Spoofing: FINRA's Rule 5210.03 has no intent element, unlike the MAR and Rule 10b-5 framing the entry used.
- Heating oil: backwardation tracks low distillate stocks (scarcity supported) but does not forecast returns (premium not supported), as for WTI and gas.
- FX: the short-rate differential does not forecast 12-month changes out of sample; a carry portfolio earned +2.07 percent a year net (Newey--West $t=2.04$), a statistical return on averaged prices.
- Inflation-shock row: no hypothesised response (10-year yield, slope, oil) is supported on real-time CPI vintages.
- Why firms hedge: the two industry studies read at abstract level do not support the value channel.

### Sources

Listed with URL, retrieval date, acquisition route, content type, size and SHA-256 in `reading_materials/sources_empirical-extensions_2026-10-17.json` (106 files kept, 3 not kept with reasons, 23 failed or refused requests; ignored; none committed), with derived text layers and the local library copies (Hull 11th Global edition, Christoffersen proof, Harris 2002, Lehalle and Laruelle 2nd edition) noted. 36 source keys were added to `compendium/front/sources.tex` (298 in all); `ecfr-17cfr-cftc-swaps`, `nber-business-cycles` and `nyse-rules-2019` were extended in place. Internet Archive captures were used where a publisher refused automated retrieval and an archived copy existed: SEC (filing status), BIS (WP 1087), the OCC rulebook, Project Euclid (Brémaud and Massoulié, open access), S\&P DJI, STOXX, Deutsche Börse and NYU (Kolm and Ritter). Abstract-only routes: RePEc (Tufano; Jin and Jorion; Shumway and Warther; Buti, Rindi and Werner 2022) and OpenAlex (Chincarini et al.; Kyle, Obizhaeva and Wang). Refused or unavailable, not bypassed: sec.gov and theocc.com (403), FRED (HTTP/2 errors and timeouts; H.15 and EIA used, a recorded protocol deviation), BYU (Shumway, 403, no archived copy), ScienceDirect (403 on an open-access article), Wiley (Levy, 403), the Philadelphia Fed's quarterly-vintage file (does not exist; monthly vintages used), Nasdaq and FTSE MIB methodologies (403, 404), journal paywalls (Davis and Norman; Joubert; Tufano and Jin and Jorion full texts).

### Checks

New, all exit 0: `backtest-inference/sharpe-zero-check.py`; `risk-tail-systemic/es-discrete-check.py` and `garch-ewma-check.py`; `volatility-options/bsm-svi-checks.py`; `portfolio-construction/erc-check.py`; `rates-credit-mortgages/multicurve-check.py`; `crypto-perpetuals/amm-checks.py`; `multi-asset-systematic-macro/inversion-horizons.py` (output unchanged on rerun). Corrected in place and passing: `filing-timestamp-checks.py`, `reconciliation-check.py`. All 37 earlier no-argument checks rerun and pass.

Empirical scripts, rerun and compared byte for byte with their saved outputs: `heating_oil_test.py` (results and panel), `fx_carry_test.py`, `inflation_regime_test.py`, `global_macro_down_months_2014_test.py`, `acm-term-premium-summary.py`, `deribit-options-snapshot.py`. The v2 scripts (`backwardation_test.py`, `fx_ppp_oos_test.py`, `regime_recession_test.py`) and the global-macro v1 script reproduce their committed outputs, which are unchanged. `tools/check_compendium.py --check`: 0 problems. `python3 -B -m unittest discover -s tools`: 14 tests OK.

### Build

Clean `latexmk -pdf compendium.tex` after `latexmk -C`: exit 0, 328 pages. Three overfull and two underfull boxes from new text were fixed by rewording (the Greeks set as a list); after the last edit, 0 overfull and 0 underfull boxes and no LaTeX warnings remain, apart from the inherited `page.i` duplicate-destination warning. Pages with the new option-pricing, resampled-efficiency, Hawkes and crypto passages were inspected as images.

### Other files

- Pathway notes (31): a dated paragraph each, new entries listed, resolved stubs removed and the others annotated.
- Reading notes updated: `wide-boyd-markowitz-seventy`, `cfd-hu-black-2007`, `s7-hulloptions`, `alpha-laruelle`, `alpha-harris`, `wide-christoffersen-elements`.
- Also updated: `notes/log.md` (no dates of mastery or consolidation), `notes/source-review-index.md` and `compendium/README.md`.

### For review

- The filing-availability convention (dissemination or first observation, else unknown) and its lower bound.
- The venue-rule flag for Done for Day on Day orders.
- The heating-oil expiry assumption (rule text not obtained; supported by the roll check in 6 of 7 blocks) and the two inflation-row protocol deviations.
- The Gatheral--Jacquier density factor recorded as a source discrepancy (p. 5).
- Abstract-only evidence (targets 7, 14, 17, 23, 30) and archived copies used in place of refused publisher pages.
- The NYSE rulebook read is a 2019 compilation.

## derivatives and empirical validation (2026-10-17): seven audit repairs, backlog reconciliation and a source-review coverage

Starting state checked: `main` at `012aa19`, equal to `origin/main`; working tree clean; guide pin `343d145` (unchanged); 239 entries, all draft; no legacy block. This is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them. Protocols for new empirical tests were written to files before their results were computed and are committed with the results, so none is a preregistration.

### Stage 1: audit repairs

1. **Quarterly CPI vintages** (`ev:regime-asset-responses-tested`; new `inflation_quarterly_test.py`). empirical extensions (2026-10-17)'s protocol deviation was wrong: it had requested `pcpiqvmd.xlsx`, a name formed from the monthly file's root, and concluded that no quarterly file exists. The quarterly file is `cpiQvMd.xlsx` (vintages CPIyyQq), linked from the Philadelphia Fed's CPI page (dated 2 October 2026). The collection documentation says quarterly vintages hold what was available on the 15th of the quarter's middle month and exclude later releases, while monthly vintages are taken just after the BLS report, which can fall either side of the 15th. The correction was appended to `inflation-row-protocol.md` before the quarterly results were computed; the protocol is otherwise unchanged. Results: 128 usable vintages (1994Q3--2026Q2), 34 signal quarters in 13 episodes; 10-year yield $+0.07$ (Welch $t=0.83$), slope $-0.17$ ($t=-1.56$), WTI $-2.2$ percent ($t=-0.60$): no response supported. Diagnostic: on 111 common vintage months with responses (112 classifiable), the latest CPI month differs in 55, always later in the monthly vintage, and 11 signal labels change. These match the audit's counts, recomputed independently. The monthly run (`inflation_regime_test.py` and outputs) is unchanged and relabelled a timing sensitivity; it still reproduces byte for byte.
2. **FX forecast inference** (`ev:fx-valuation-factors-oos`; `fx_ppp_oos_test.py` and `fx_carry_test.py` corrected in place, pre-correction versions kept in `rowlag-2026-10-17/`). The carry test stacked 7--9 currencies per month and used $h-1$ row lags; the PPP test stacked currencies one after another and ignored their contemporaneous dependence. Both now use `panel_nw_t`: Clark--West scores keep their forecast-origin month, are summed across currencies within it (each currency-month still weighted $1/N$, so pooled $R^2$ and forecasts are unchanged), and Newey--West runs over $h-1$ calendar months, with $h$ months as a sensitivity. Carry: $h=12$ Clark--West $t=-1.97$ (sensitivity $-1.94$; was $-4.44$, the audit's $-1.973$), $h=1$ $-0.41$ (was $-0.85$). PPP: $h=12$ $-0.18$ (was $-0.31$), $h=1$ $-1.30$ (was $-2.14$). All verdicts unchanged. The carry portfolio (one return a month, $+2.07$ percent a year, $t=2.04$) was unaffected and is described as a statistical return on monthly-average prices, distinct from an executable return. New focused check `fx-panel-inference-check.py` fails if currency rows are treated as months (identical currencies must give the single-series $t$; row order must not matter).
3. **Heating-oil return definition** (`ev:backwardation-scarcity-or-premium`; `heating_oil_test.py` corrected in place, the simple-return run kept in `simple-return-2026-10-17/` with the unchanged `backwardation_test.py` it imports). The protocol's log held-contract return now replaces the builder's simple return for heating oil only: premium slope 0.3276, $t=1.55$ (was 0.3582, 1.67); OOS $R^2=-0.95$ percent, Clark--West $t=0.31$ (was $-0.92$, 0.37); premium not supported; scarcity unaffected. EIA's own definitions (Futures Prices (NYMEX), ``Contract~1'') document the delivery-month mapping. Month-ends are the last date on which EIA reports both contracts: 79 of 361 precede the last date in the month on which EIA reports either contract (12 by more than five days, at most 21), now reported and written to the panel; the roll check on that calendar is consistent with the mapping and does not prove the expiry date. An exploratory regression on the 243 pairs whose dates are both the month's last observed date (chosen after the results) gives slope 0.07, $t=0.20$. The WTI and gas protocols were not changed.
4. **FRA settlement convention** (`mod:multi-curve-fra-swap-valuation`; new `fra-settlement-check.py`). $N\tau(F_j-K)P_{\mathrm{OIS}}(T_2)$ is now labelled the end-settled swaplet value, exact when $F_j$ is the $T_2$-forward expectation of the fixing. The conventional FRA pays $N\tau(L-K)/(1+\tau L)$ at $T_1$ (Hull, sec.~4.9, p.~111, n.~4); with deterministic $L=F_j$ its value is $N\tau(F_j-K)P_{\mathrm{OIS}}(T_1)/(1+\tau F_j)$. Invented curves: $-\$20{,}777.37$ start-settled against $-\$20{,}792.96$ end-settled. The check shows the two coincide on one curve (bond replication) and diverge on two, and that with a stochastic $L$ the substitution omits a concavity term (by quadrature, $-\$21{,}044.50$ at 20 percent volatility); the stochastic conditions are stated rather than a general pricing theorem.
5. **ERC conditions** (`meth:equal-risk-contribution`; new `erc-sharpe-check.py`). The source's first-order condition holds for any common Sharpe ratio $s$; ERC maximises the Sharpe ratio over long-only, fully invested weights only if $s>0$ (with constant correlation $\rho\in(-1/(n-1),1)$); for $s<0$ it minimises it. Counterexample: two uncorrelated unit-volatility assets with excess return $-1$: ERC $-\sqrt2$, either asset $-1$. The source's wording and the corrected condition are distinguished.
6. **Crypto liquidation units** (`ev:crypto-dated-futures-carry`). BIS WP 1087, revision of October 2025, PDF pp.~7, 25 and~44 (Table~7 as a page image): coefficient 2.22 (s.e.\ 0.79) on the standardised one-month basis for next-month sell liquidations scaled by open interest, intercept 10.84 (OKEx, 1,619 observations), i.e.\ about 2.2 percentage points of open interest per standard deviation of carry. ``22 percent of open interest'' is withdrawn; the prose's two wordings and its ``10\%'' are reported, not resolved; the measure includes voluntary and forced closures.
7. **Market-manipulation intent** (`rule:spoofing-securities-markets`). MAR's Article 12(1)(a) is effect-based with a legitimate-reasons defence, (b) turns on deception or contrivance, and (c)--(d) on ``knew, or ought to have known''; ESMA/2015/224 (feedback on Q1, para.~12; sec.~2.2.2, para.~8) says conduct without intent can fall within MAR; Directive 2014/57/EU makes the criminal offence require intent (Art.~5(1); recital~23); Rule 10b-5 requires scienter (\emph{Aaron}, \emph{Hochfelder}); Section~9(a)(2) has a purpose element; FINRA Rule 5210.03 has no express intent element and is described as one regime among others, not the exception. FINRA's findings are kept.

### Backlog reconciliation

All 57 active backlog lines that carried stacked status prefixes were rewritten to state only the remaining gap (the dated paragraphs above each backlog keep the history). In particular: `ev:global-macro-returns-after-2013` is complete within its stated scope, and the registration blocker is gone; `ev:curve-inversion-after-2005` now says all 27 inverted months have complete twelve-month horizons and only retrospective NBER dating remains, with a revisit trigger of an NBER peak announcement or April 2027 (when the last month passes the longest past announcement lag); claims that read material was unread were removed, including two stale entry passages (`mod:mean-variance-portfolio-optimisation` on Michaud and shrinkage, and the further reading of `mod:harris-discretised-spread` on Dayri and Rosenbaum). Correction within this batch: the first reconciled line for `meth:multiple-testing-control` repeated a stale claim that Romano and Wolf's working paper was unread; it had been read in method validation (2026-10-17), and the line now names only the published versions. After Stage 2, 19 lines were updated again to reflect new outcomes.

### Statements superseded

- empirical extensions (2026-10-17)'s protocol deviation ``The Philadelphia Fed does not publish a quarterly-vintage CPI file'' and the record's ``the Philadelphia Fed's quarterly-vintage file (does not exist; monthly vintages used)'' (empirical extensions (2026-10-17), *Sources*) are superseded by Stage 1, item 1.
- empirical extensions (2026-10-17)'s carry Clark--West $t=-4.44$ and $-0.85$, and method validation (2026-10-17)'s PPP $t=-0.31$ and $-2.14$, are superseded by Stage 1, item 2.
- empirical extensions (2026-10-17)'s heating-oil premium figures (slope $+0.36$, $t=1.67$; OOS $-0.92$ percent, Clark--West 0.37) are superseded by Stage 1, item 3, as is ``the expiry assumption (rule text not obtained; supported by the roll check)'' in its *For review*, which now rests on EIA's definition, with the roll check described as consistent only.
- ``A 10 percent rise in standardised carry predicts short liquidations of 22 percent of open interest'' (empirical extensions (2026-10-17), target 33) is withdrawn (Stage 1, item 6).
- ``Spoofing: FINRA's Rule 5210.03 has no intent element, unlike the MAR and Rule 10b-5 framing the entry used'' (empirical extensions (2026-10-17), *Conclusions that changed*) and the entry's ``Under MAR and Rule 10b-5, legality turns on intent'' are superseded by Stage 1, item 7.
- ``The registered window'' and ``run as registered'' (empirical extensions (2026-10-17), Stage 1 item 6 and target 27, and the pathway note's dated paragraph) should read ``the protocol's window'' and ``run under the protocol recorded in method validation (2026-10-17)''; no preregistration occurred. The pathway note carries an explicit correction.

### The 70-target work list

Constructed after the reconciliation from the remaining backlog gaps and the pinned guide's required readings and checkpoints, and fixed in a working file before any of it was processed. Two changes were made while processing and are recorded here: target 1 was re-aimed (its original question, Romano and Wolf's working paper, had already been read) to the entry's stated remaining gap, Hansen's SPA test; and new questions whose answers were merged into an existing entry received their own question identifiers (for example `res:cfmm-reported-price`), with the entry named under *Recorded in*. 24 targets follow up existing gaps and 46 are new bounded questions; 48 targets carry identifiers outside empirical extensions (2026-10-17)'s 60. No Stage 1 correction is counted among the 70.

*A. Backtest inference and multiple testing*
1. `meth:multiple-testing-control` (backtest-inference; follow-up). **Question.** How does Hansen's test of superior predictive ability differ from White's Reality Check, which the entry names as unread? (Re-aimed: the Romano-Wolf working paper the backlog line named had been read in method validation (2026-10-17).) **Source or input.** Hansen, Brown University Working Paper 01-06 (November 2001), Internet Archive capture of the author's page; JBES 2005 not obtained. **Would resolve it.** The test's null treatment and threshold rule at locators. **Outcome: narrowed.** Hansen's test (Brown WP 01-06, November 2001, archived copy) read: the Reality Check's least-favourable null makes it biased and sensitive to poor models; the SPA test drops models whose mean is below a vanishing threshold. Merged into meth:multiple-testing-control. The original target (Romano and Wolf's working paper) had already been read in method validation (2026-10-17), so the question was re-aimed at the entry's stated remaining gap; the Econometrica and JBES versions remain unread. **Recorded in:** `meth:multiple-testing-control`.
2. `meth:dependent-resampling-drawdowns` (backtest-inference; follow-up). **Question.** How does the stationary bootstrap draw blocks, and how is its mean block length chosen? **Source or input.** Politis and Romano (1994) not obtained; route: Patton, Politis and White's 2009 correction to Politis and White (2004), author copy. **Would resolve it.** The resampling scheme and the corrected block-length rule as stated by the authors of the method. **Outcome: narrowed.** Patton, Politis and White's 2009 correction read: D_SB = 2g^2(0), circular against stationary ARE (2/3)^(2/3) = 0.763, corrected simulations. Merged into meth:backtest-evaluation-diagnostics. Politis and Romano (1994) still not obtained; validity for drawdowns not addressed. **Recorded in:** `meth:backtest-evaluation-diagnostics`.
3. `ev:factor-zoo-hurdle` (backtest-inference; new). **Question.** What t-ratio threshold do Harvey, Liu and Zhu propose for new factors, and on what count of tested factors? **Source or input.** Harvey, Liu and Zhu, NBER WP 20592 (alpha-harvey). **Would resolve it.** The threshold, the multiple-testing methods behind it and the factor count, at locators. **Outcome: resolved.** HLZ (NBER WP 20592) read: 316 factors; t > 3.0 hurdle; Holm 3.64 (316) or 3.29 (113); 3.9 FWER 5% and 3.0 FDR 1% across correlation specifications. Merged into meth:multiple-testing-control. **Recorded in:** `meth:multiple-testing-control`.
4. `meth:sharpe-ratio-standard-error` (backtest-inference; new). **Question.** How do Ledoit and Wolf test the difference of two Sharpe ratios, and why is the Jobson-Korkie/Memmel test unreliable? **Source or input.** Ledoit and Wolf, IEW Working Paper 320 (wide-ledoit-wolf-sharpe). **Would resolve it.** The test statistic, its HAC and bootstrap inference, and the stated failure conditions. **Outcome: resolved.** Ledoit and Wolf (IEW WP 320) read: Jobson-Korkie/Memmel invalid with heavy tails or time-series dependence; HAC standard error and studentized circular block bootstrap interval. Merged into meth:sharpe-ratio-standard-error. **Recorded in:** `meth:sharpe-ratio-standard-error`.
5. `pit:ml-leakage-taxonomy` (backtest-inference; new). **Question.** Which types of leakage do Kapoor and Narayanan distinguish, and which apply to a financial backtest? **Source or input.** Kapoor and Narayanan, arXiv 2207.07048 (wide-kapoor-narayanan-leakage). **Would resolve it.** Their taxonomy at locators, mapped to the entry's checks. **Outcome: resolved.** Kapoor and Narayanan (arXiv 2207.07048) read: 3 classes, 8 leakage types; mapped to meth:time-valid-ml-experiment-record, which lacks L1.4 and L3.3 checks. **Recorded in:** `meth:time-valid-ml-experiment-record`.

*B. Covariance, factor and volatility estimation*
6. `meth:portfolio-covariance-estimation` (portfolio-construction; follow-up). **Question.** How is a DCC correlation model specified and estimated? **Source or input.** Engle and Sheppard, NBER WP 8554 (the DCC estimator's two-step form; Engle 2002 JBES not obtained). **Would resolve it.** The model equations and the two-step likelihood at locators. **Outcome: narrowed.** Engle and Sheppard (NBER WP 8554) read for DCC's equations, positivity conditions and two-step estimation; merged into meth:portfolio-covariance-estimation. Engle's 2002 JBES paper not obtained; factor-model estimation (Connor et al.) still unread. **Recorded in:** `meth:portfolio-covariance-estimation`.
7. `meth:constant-correlation-shrinkage` (high-dimensional-estimation; new). **Question.** What shrinkage target and optimal intensity do Ledoit and Wolf use in 'Honey, I Shrunk the Sample Covariance Matrix'? **Source or input.** Ledoit and Wolf, 2003 manuscript (s6-honey). **Would resolve it.** The target, the intensity formula and its estimator, with an own numerical check. **Outcome: resolved.** Honey (2003 manuscript) read: constant-correlation target, kappa = (pi - rho)/gamma, delta* = max(0, min(kappa/T, 1)); own check; merged into meth:portfolio-covariance-estimation (filling the 'feasible intensity not transcribed' pitfall). **Recorded in:** `meth:portfolio-covariance-estimation`.
8. `ev:correlation-matrix-noise` (high-dimensional-estimation; new). **Question.** How much of an empirical correlation matrix lies within the random-matrix (Marchenko-Pastur) band in Laloux et al.? **Source or input.** Laloux, Cizeau, Bouchaud and Potters, arXiv cond-mat/9810255 (wide-laloux-noise-dressing). **Would resolve it.** The band formula, sample (N, T) and the share of eigenvalues outside it, with an own simulation. **Outcome: resolved.** Laloux et al. (arXiv) read: MP band, N=406, T=1309, lambda_1 = 25 lambda_max, 94/6 split; a source slip found (sigma^2 = 1 - lambda_1/N, not lambda_max). New entry ev:correlation-matrix-noise with own simulation. **Recorded in:** `ev:correlation-matrix-noise` (new entry).
9. `meth:poet-covariance` (high-dimensional-estimation; new). **Question.** What is the POET estimator and what does it assume? **Source or input.** Fan, Liao and Mincheva, arXiv 1201.0175 (wide-fan-liao-mincheva-poet). **Would resolve it.** The estimator's definition and the pervasive-factor and sparsity conditions. **Outcome: resolved.** POET (arXiv 1201.0175) read: estimator, adaptive threshold, pervasiveness; merged into meth:portfolio-covariance-estimation. **Recorded in:** `meth:portfolio-covariance-estimation`.
10. `meth:shrinkage-estimator-choice` (portfolio-construction; new). **Question.** Which estimator do Ledoit and Wolf's 2022 review recommend for portfolio selection, and when does nonlinear shrinkage beat linear? **Source or input.** Ledoit and Wolf, J. Financial Econometrics 20(1), 2022, author-hosted copy (wide-ledoit-wolf-review). **Would resolve it.** The recommendation and its stated conditions at locators. **Outcome: resolved.** 2022 journal version read: N, T > 50 rule of thumb for nonlinear shrinkage; DCC-NL for Markowitz; RiskMetrics 2006 not recommended; passages compared agree with the working paper read earlier. **Recorded in:** `meth:portfolio-covariance-estimation`.
11. `meth:volatility-forecast-loss` (time-series-volatility; new). **Question.** Which loss functions rank volatility forecasts consistently when the proxy is noisy? **Source or input.** Patton, UTS QFRC Research Paper 175 (April 2006) (wide-patton-robust-loss). **Would resolve it.** The robust family, the MSE and QLIKE members, and an own check that a non-robust loss misranks. **Outcome: resolved.** Patton (QFRC RP 175) read: robust-loss characterisation, MSE and QLIKE uniqueness, family; own simulation shows MAE misranks. New entry meth:volatility-forecast-loss. **Recorded in:** `meth:volatility-forecast-loss` (new entry).
12. `mod:har-rv` (time-series-volatility; new). **Question.** What is Corsi's HAR-RV specification? **Source or input.** Corsi, J. Financial Econometrics 7(2), 2009, hosted copy (wide-corsi-har). **Would resolve it.** The regression with its daily, weekly and monthly components and their horizons. **Outcome: resolved.** Corsi (JFEC 2009) read: HAR-RV with 5- and 22-day averages as a restricted AR(22); own mapping check; merged into mod:garch-volatility-forecast. **Recorded in:** `mod:garch-volatility-forecast`.
13. `mod:gjr-asymmetric-garch` (time-series-volatility; new). **Question.** How does the GJR model add an asymmetric response, and which sign do the authors estimate? **Source or input.** Glosten, Jagannathan and Runkle, Minneapolis Fed Working Paper 505 (1992) (wide-gjr-garch). **Would resolve it.** The variance equation and the estimated asymmetry at locators. **Outcome: resolved.** GJR working paper 505 read from page images: Model 2 with an indicator on POSITIVE shocks (sign convention opposite the textbook form); negative shocks raise volatility; merged into mod:garch-volatility-forecast. **Recorded in:** `mod:garch-volatility-forecast`.
14. `ev:high-frequency-stylised-facts` (high-dimensional-estimation; new). **Question.** Which of Cont's stylised facts of returns survive in recent equity data? **Source or input.** Cont (2001) not obtained; route: Ratliff-Crain et al., arXiv 2311.07738v2, which retests them (wide-cont-stylized-facts). **Would resolve it.** The list of facts as restated and the replication's verdict on each. **Outcome: narrowed.** Cont (2001) not obtained; Ratliff-Crain et al. (arXiv v2) retest: 8 of 11 facts supported intraday for Dow 30 stocks, 2018-19; facts 3, 9, 11 unsupported. Merged into ev:high-frequency-stylised-facts. **Recorded in:** `ev:high-frequency-stylised-facts`.

*C. Portfolio construction, risk parity and volatility management*
15. `mod:mean-variance-portfolio-optimisation` (portfolio-construction; new). **Question.** Why does Markowitz (1952) reject the rule of maximising expected return, and what is his E-V rule? **Source or input.** Markowitz, Journal of Finance 7(1), 1952, hosted copy (s6-markowitz). **Would resolve it.** The two rules and the diversification argument at locators. **Outcome: resolved.** Markowitz (1952) p. 77 read as page image: expected-return rule rejected because it never implies diversification; E-V rule. Merged into mod:mean-variance-portfolio-optimisation. **Recorded in:** `mod:mean-variance-portfolio-optimisation`.
16. `mod:mean-variance-portfolio-optimisation` (portfolio-construction; new). **Question.** How long must the estimation window be for sample mean-variance to beat 1/N, according to DeMiguel, Garlappi and Uppal? **Source or input.** DeMiguel, Garlappi and Uppal (s7-demiguel); NBER conference draft and LBS repository. **Would resolve it.** The analytical window estimate (assets, months) at locators, or the access outcome. **Outcome: resolved.** DeMiguel, Garlappi and Uppal (RFS 2009, authors' copy via an archived LBS page) read: 14 models, 7 datasets, critical window about 3000 months (25 assets) and 6000 (50). Merged into mod:mean-variance-portfolio-optimisation. **Recorded in:** `mod:mean-variance-portfolio-optimisation`.
17. `mod:portfolio-transaction-cost-function` (portfolio-construction; new). **Question.** What does multi-period optimisation add over single-period optimisation in Boyd et al., and what does their backtest show? **Source or input.** Boyd et al., Multi-Period Trading via Convex Optimization, author PDF (exp-boyd-multiperiod-trading). **Would resolve it.** The MPO formulation and the reported comparison at locators. **Outcome: resolved.** Boyd et al. secs. 5.2 and 7.4 read: MPO motivation; H = 2 example's advantage mostly from the extra forecast, built from realised returns plus noise. Merged into mod:portfolio-transaction-cost-function. **Recorded in:** `mod:portfolio-transaction-cost-function`.
18. `ev:risk-parity-risk-share` (risk-parity-vol-targeting; new). **Question.** What share of a 60/40 portfolio's risk comes from equities in Qian's risk-parity paper, and what does he claim for risk parity? **Source or input.** Qian, PanAgora, September 2005 (s16-r24). **Would resolve it.** The risk share, the weights and the claims at locators, with an own check. **Outcome: resolved.** Qian (2005) read: 93% stock risk in 60/40, 23/77 parity, Sharpe 0.87 vs 0.67; own check 92.7% and 23.4/76.6. Merged into meth:equal-risk-contribution. **Recorded in:** `meth:equal-risk-contribution`.
19. `meth:equal-risk-contribution` (risk-parity-vol-targeting; follow-up). **Question.** What do Maillard, Roncalli and Teiletche's empirical sections report for ERC against 1/N and minimum variance? **Source or input.** Authors' version of May 2009, sec. 4 (local copy from empirical extensions (2026-10-17)). **Would resolve it.** Their tables' Sharpe, volatility and drawdown figures at locators. **Outcome: resolved.** MRT sec. 4 read: three backtests ending 2008 (Sharpe 1/n, MV, ERC: 0.62/0.77/0.65; 0.27/0.74/0.49; 0.27/0.49/0.67). Merged; the entry's 'sec. 4 not read' pitfall replaced. **Recorded in:** `meth:equal-risk-contribution`.
20. `mod:volatility-targeting-deleveraging` (funding-crowding; follow-up). **Question.** How do Moreira and Muir build a volatility-managed portfolio, and how much leverage does it take? **Source or input.** Moreira and Muir, NBER WP 22208, full text (s16-r25; the abstract alone was read before). **Would resolve it.** The scaling rule c/sigma^2, the alpha and the reported leverage statistics at locators. **Outcome: narrowed.** Moreira and Muir full text read: scaling rule, alpha 4.86%, weight percentiles 1.6/2.6/6.4. New entry ev:volatility-managed-portfolios. The backlog's measured volatility-targeted capital and Narang's 1.5-2x estimate remain unsourced. **Recorded in:** `ev:volatility-managed-portfolios` (new entry).

*D. Statistical arbitrage and trend*
21. `def:alpha-model-taxonomy` (statistical-arbitrage; new). **Question.** How much of contrarian profit do Lo and MacKinlay attribute to cross-autocorrelation (lead-lag) rather than overreaction? **Source or input.** Lo and MacKinlay, NBER WP 2977 (wide-lo-mackinlay-contrarian). **Would resolve it.** The decomposition formula and the reported shares at locators. **Outcome: resolved.** Lo and MacKinlay (NBER WP 2977) read: decomposition into cross- and own-autocovariance terms; half of lag-1 profit from cross-autocovariances (67% central quintile); under 50% attributable to overreaction. Merged into def:alpha-model-taxonomy (residual reversion). **Recorded in:** `def:alpha-model-taxonomy`.
22. `meth:s-score-residual-trading` (statistical-arbitrage; new). **Question.** What entry and exit thresholds does Avellaneda and Lee's s-score use, and how did the strategy fare in 2007-2008? **Source or input.** Avellaneda and Lee, version of 16 June 2009 (alpha-residual). **Would resolve it.** The s-score definition, thresholds and reported performance at locators. **Outcome: resolved.** Avellaneda and Lee eqs. (15)-(16) read: s-score, entry 1.25, exits -0.50/0.75; cutoffs chosen on 2000-2004 inside the 1997-2007 backtest (in-sample threshold choice). Merged into def:alpha-model-taxonomy. **Recorded in:** `def:alpha-model-taxonomy`.
23. `meth:residual-reversion-strategy` (statistical-arbitrage; follow-up). **Question.** How large were the contrarian strategy's losses in August 2007 and how fast did they reverse? **Source or input.** Khandani and Lo, NBER WP 14465, full text (exp-khandani-lo-quant-meltdown). **Would resolve it.** Daily returns of 6-10 August 2007 and the explanation, at locators. **Outcome: narrowed.** Khandani and Lo sec. 5 read: the m-minute mean-reversion strategy dips 7-13 August 2007 and resumes; magnitudes only in figures, no daily percentages. Merged into def:common-investor-contagion. **Recorded in:** `def:common-investor-contagion`.
24. `def:alpha-model-taxonomy` (trend-following; new). **Question.** How do Moskowitz, Ooi and Pedersen size each time-series momentum position? **Source or input.** Moskowitz, Ooi and Pedersen, author-hosted journal copy (s6-tsmom; only the abstract was read). **Would resolve it.** The ex-ante volatility estimator and the 40 percent scaling at locators. **Outcome: resolved.** Moskowitz, Ooi and Pedersen secs. 2.4 and 4.1 read: EWMA variance with 60-day centre of mass, 261 scaling, t-1 estimate, 40% position volatility. Merged into def:alpha-model-taxonomy. **Recorded in:** `def:alpha-model-taxonomy`.

*E. Options and volatility models*
25. `mod:heston-stochastic-volatility` (option-pricing-models; new). **Question.** Does Heston's closed-form price reproduce an independent valuation? **Source or input.** Heston (1993), hosted copy (s6-heston). **Would resolve it.** The characteristic-function formula at locators and an own check against Monte Carlo and the Black-Scholes limit. **Outcome: resolved.** Heston eqs. (10)-(18) read from a page image; own check vs Black-Scholes limit and Monte Carlo. New entry mod:heston-stochastic-volatility. **Recorded in:** `mod:heston-stochastic-volatility` (new entry).
26. `mod:heston-stochastic-volatility` (option-pricing-models; new). **Question.** How does Carr and Madan's FFT method price calls, and what does its damping parameter require? **Source or input.** Carr and Madan (1999), author copy (s6-carrmadan). **Would resolve it.** The damped transform, the condition on alpha and an own FFT check against Black-Scholes. **Outcome: resolved.** Carr and Madan eqs. (5)-(7) read: damping, E[S^(alpha+1)] finite, alpha one quarter of the bound; own FFT reproduces BS and Heston. In mod:heston-stochastic-volatility. **Recorded in:** `mod:heston-stochastic-volatility` (new entry).
27. `mod:merton-jump-diffusion` (option-pricing-models; new). **Question.** What is Merton's jump-diffusion option price and why can jump risk not be hedged with the stock? **Source or input.** Merton, Sloan WP 787-75 (MIT DSpace) or the hosted JFE version (wide-merton-jumps). **Would resolve it.** The series formula and the hedging argument at locators, with an own check. **Outcome: resolved.** Merton Sloan WP 787-75 (Internet Archive capture; MIT returned 429) read from page images: no riskless hedge, eq. (16) and lognormal case (19), dF/dlambda > 0; own check. New entry mod:merton-jump-diffusion. **Recorded in:** `mod:merton-jump-diffusion` (new entry).
28. `meth:leland-cost-adjusted-volatility` (option-hedging-smile; new). **Question.** What hedging volatility does Leland propose for proportional costs? **Source or input.** Leland, Journal of Finance 1985 (vo-leland-1985). **Would resolve it.** The adjusted variance formula at a locator, or the access outcome. **Outcome: blocked.** Leland (1985): no open copy found (search found only secondary accounts, some disputing his main theorem); JF paywalled. Not attempted through any unauthorised copy. **Recorded in:** `none`.
29. `mod:sabr-smile` (rate-derivatives; new). **Question.** What is the SABR implied-volatility approximation and how is it used in a multi-curve setting? **Source or input.** Bianchetti and Carlicchi, arXiv 1103.2567 (gap-rates-multicurve-sabr), restating Hagan et al. (2002). **Would resolve it.** The formula at locators and an own check of its ATM limit and normal-SABR comparison. **Outcome: resolved.** SABR expansion from Bianchetti and Carlicchi Table 5 (page image); own check vs Monte Carlo within 0.2 vol points at one parameter set. New entry mod:sabr-smile; Hagan et al. themselves unread. **Recorded in:** `mod:sabr-smile` (new entry).
30. `def:implied-volatility-surface` (option-pricing-models; follow-up). **Question.** Does the earlier arXiv version of Gatheral and Jacquier carry the same density expression in Lemma 2.2? **Source or input.** arXiv 1204.0646 v1 or v2 against the v of 27 November 2024 already read. **Would resolve it.** The lemma's text in each version, as page images. **Outcome: narrowed.** arXiv v1 and v2 read: the same density expressions appear in Lemma 4.1 (PDF p. 8), so the slip predates the 2024 revision; journal version still not compared. Merged into def:implied-volatility-surface. **Recorded in:** `def:implied-volatility-surface`.

*F. Rates, reference rates, money markets and post-trade rules*
31. `conv:fra-rate-multicurve-measure` (rate-derivatives; new). **Question.** Which FRA settlement convention and pricing formula do Bianchetti and Carlicchi use in the multi-curve setting? **Source or input.** Bianchetti and Carlicchi, arXiv 1103.2567 (gap-rates-multicurve-sabr). **Would resolve it.** Their FRA formula and convexity remarks compared with the entry's end- and start-settled forms. **Outcome: resolved.** Bianchetti and Carlicchi Table 2 (page image): FRA valued N P_d(T_k) omega (F~ - K) tau with F~ the T_k-forward expectation under the discount curve, i.e. the end-settled form; merged into mod:multi-curve-fra-swap-valuation. **Recorded in:** `mod:multi-curve-fra-swap-valuation`.
32. `data:gsw-treasury-curve` (curve-term-structure; new). **Question.** What is the Gurkaynak-Sack-Wright curve and does a published parameter row reproduce the published zero yield? **Source or input.** GSW, FEDS 2006-28, and the Federal Reserve's feds200628 file (wide-gsw-yield-curve). **Would resolve it.** The Svensson formula at locators and an own recomputation of one date's yields. **Outcome: tested within stated bounds.** GSW eq. (22) read from a page image; own recomputation of SVENY10 from published parameters on 13,759 days matches to 0.00005 pp. New entry data:gsw-treasury-curve. **Recorded in:** `data:gsw-treasury-curve` (new entry).
33. `ev:term-premia` (curve-term-structure; follow-up). **Question.** How does the Kim-Wright 10-year term premium compare with ACM's on common dates? **Source or input.** Kim and Wright, FEDS 2005-33, the Board's KW file, and the ACM file retained in empirical extensions (2026-10-17) (rt-kim-wright-2005). **Would resolve it.** The model definition at locators and the two series on stated dates. **Outcome: resolved.** Kim-Wright FEDS 2005-33 read (abstract, sec. 2); own month-end comparison with ACM 1990-2026: correlation 0.86, KW 0.24 pp lower on average, range -2.22 to +1.18. Merged into mod:forward-rates-fra. **Recorded in:** `mod:forward-rates-fra`.
34. `def:money-market-reference-rates` (rate-derivatives; new). **Question.** Why did overnight risk-free rates replace IBORs, and how do they differ, per Schrimpf and Sushko? **Source or input.** BIS Quarterly Review, March 2019 (rt-schrimpf-sushko-rfr-2019). **Would resolve it.** Their comparison of secured and unsecured RFRs at locators. **Outcome: resolved.** Schrimpf and Sushko (BIS QR March 2019) read: unsecured interbank collapse, OIS term structure, backward vs forward-looking term rates. Merged into def:money-market-reference-rates. **Recorded in:** `def:money-market-reference-rates`.
35. `def:money-market-reference-rates` (money-markets-repo-lending; new). **Question.** How is SOFR calculated and published, and when is it revised? **Source or input.** New York Fed, Additional Information about Reference Rates (exp-sofr-data). **Would resolve it.** The calculation (volume-weighted median, trimming), publication time and revision threshold. **Outcome: resolved.** New York Fed methodology read: SOFR = BGCR + DVP with 20% lowest-rate DVP trim; volume-weighted median; 8:00 a.m. ET; same-day revision at 2:30 p.m. only if > 1 bp. Merged into def:money-market-reference-rates. **Recorded in:** `def:money-market-reference-rates`.
36. `def:money-market-reference-rates` (money-markets-repo-lending; new). **Question.** What maturities dominate commercial paper, against Gliner's 'most between 90 and 270 days'? **Source or input.** Aquilina, Schrimpf and Todorov, BIS Quarterly Review, September 2023 (gap-money-cp-cd-primer). **Would resolve it.** The maturity statements at locators. **Outcome: resolved.** BIS CP/CD primer read: US average CP maturity around 30 days, Europe about four months; 270 days is the legal limit. Contradicts Gliner's 'most 90-270 days'; merged into def:money-market-reference-rates. (A first request fetched a different BIS article; the correct page was then retrieved.) **Recorded in:** `def:money-market-reference-rates`.
37. `def:money-market-reference-rates` (money-markets-repo-lending; new). **Question.** What liquidity risk premium do Copeland and Engbretson measure in repo, and how? **Source or input.** New York Fed Staff Report 1189 (latest-copeland-repo-premium-2026). **Would resolve it.** The measure, sample and estimate at locators. **Outcome: narrowed.** Copeland and Engbretson (SR 1189) abstract read: 100 bp IORB rise -> 0.9 bp liquidity premium (10% of dealer spread), equivalent to a 429 bn reserve fall, nonlinear. Merged into def:money-market-reference-rates. Only the abstract (or abstract and introduction) was read, so methods and robustness are unchecked. **Recorded in:** `def:money-market-reference-rates`.
38. `ev:money-fund-runs` (money-markets-repo-lending; new). **Question.** Did institutional and retail prime funds run differently in March 2020, per Cipriani and La Spada? **Source or input.** New York Fed Staff Report 956, revised (gap-money-prime-fund-runs). **Would resolve it.** The outflow figures by investor type at locators. **Outcome: resolved.** Cipriani and La Spada (SR 956 rev. 2024) read: 22% prime-fund redemptions (32% institutional, 11% retail); fundamentals vs herding; cheap safe-haven switching worsens runs. New entry ev:money-fund-runs. **Recorded in:** `ev:money-fund-runs` (new entry).
39. `rule:otc-derivatives-reforms` (rates-credit-mortgages; follow-up). **Question.** What are the BCBS-IOSCO uncleared-margin thresholds and phase-in dates? **Source or input.** BCBS-IOSCO framework (bis.org refused; Internet Archive capture). **Would resolve it.** The thresholds (AANA, initial-margin threshold) and phase dates at locators, or the access outcome. **Outcome: narrowed.** BCBS-IOSCO April 2020 framework read via Internet Archive: VM zero threshold, IM threshold up to EUR 50m, MTA 500k, phase-in 3.0tn (2016) to 8bn (permanent from 1 Sep 2022). Merged into mech:otc-clearing-collateral. U.S. prudential rule and EMIR still unread. **Recorded in:** `mech:otc-clearing-collateral`.
40. `rule:uk-bond-transparency` (otc-fixed-income-trading; follow-up). **Question.** What does the FCA's PS24/14 set for U.K. bond post-trade deferrals? **Source or input.** FCA PS24/14 (fca.org.uk refused; Internet Archive capture). **Would resolve it.** The categories and deferral periods at locators, or the access outcome. **Outcome: narrowed.** FCA PS24/14 read via Internet Archive: four bond size groups (real-time, T+1 end of day, 2 weeks, 3 months), most rules from 1 December 2025. Merged into rule:us-eu-bond-transparency; Table 8 thresholds and MAR 11 text not transcribed. **Recorded in:** `rule:us-eu-bond-transparency`.

*G. Commodities, FX and indices*
41. `ev:backwardation-scarcity-or-premium` (commodity-storage-curves; follow-up). **Question.** Does commercial hedging pressure in the CFTC's Commitments of Traders predict WTI held-contract returns? **Source or input.** CFTC legacy futures-only COT files with the retained WTI panel; protocol recorded before computing. **Would resolve it.** Coefficient and t on a pre-set rule, or the access outcome. **Outcome: tested within stated bounds.** Protocol recorded before download; CFTC legacy COT 1986-2024 (code 067651): HP does not predict WTI held-contract returns (beta -0.008, t -0.17; OOS R2 -1.1%, CW -0.28; n 458). Hedging pressure not supported. Merged into ev:backwardation-scarcity-or-premium. **Recorded in:** `def:contango-backwardation-stocks`.
42. `meth:time-varying-hedge-ratio` (commodity-hedging; follow-up). **Question.** Out of sample, do rolling-window hedge ratios cut the variance of a jet-fuel exposure hedged with heating-oil or WTI futures more than a static ratio? **Source or input.** EIA daily Gulf Coast jet fuel spot and the retained NYMEX contract-1 series; protocol recorded before computing. **Would resolve it.** Out-of-sample variance reductions on a pre-set design. **Outcome: tested within stated bounds.** Protocol recorded before computing; jet fuel vs HO and WTI contract 1 weekly, roll weeks dropped: OOS variance reduction static 49.3% vs rolling-104 53.8% (HO), 25.3% vs 28.1% (WTI); rolling helps. Merged into mod:minimum-variance-hedge-ratio; GARCH not run. **Recorded in:** `mod:minimum-variance-hedge-ratio`.
43. `ev:cip-deviations` (fx-cip-dollar-funding; new). **Question.** How large and persistent are covered-interest-parity deviations after 2008, per Du, Tepper and Verdelhan? **Source or input.** NBER WP 23170. **Would resolve it.** The basis definition and reported magnitudes at locators. **Outcome: resolved.** Du, Tepper and Verdelhan (NBER WP 23170) read: basis definition, G10 average absolute 24 bp (3m) and 27 bp (5y) 2010-2016, quarter-end effect. New entry ev:cip-deviations. **Recorded in:** `ev:cip-deviations` (new entry).
44. `data:equity-index-lists-current` (international-equity-markets; follow-up). **Question.** How is the IBEX 35 weighted and capped today? **Source or input.** BME's technical rules for the IBEX 35 (a route not tried before). **Would resolve it.** The weighting, free-float and cap rules at locators, or the access outcome. **Outcome: narrowed.** BME notice 18/2024 (Internet Archive; site served HTML) read: free-float bands, 20% single-stock cap, 40% in sector sub-indices. Merged into def:equity-indices-derivatives; the Technical Regulations themselves not read. **Recorded in:** `def:equity-indices-derivatives`.

*H. Macro regimes*
45. `ev:regime-asset-responses-tested` (macro-regimes-stock-bond; follow-up). **Question.** In real time, does the deflation/disinflation row (yields down, duration rallies) hold on quarterly CPI vintages? **Source or input.** Philadelphia Fed cpiQvMd.xlsx with the retained GS10 and H.15 series; protocol recorded before computing. **Would resolve it.** Signal-quarter differences with Welch and Newey-West t on a pre-set rule. **Outcome: tested within stated bounds.** Protocol recorded before this row's results; quarterly CPI vintages: 28 signal quarters in 12 episodes; dy10 +0.04 (Welch t 0.51), wrong sign; not supported. Merged into def:macro-regime-asset-map. **Recorded in:** `def:macro-regime-asset-map`.

*I. Market structure and regulation*
46. `rule:spoofing-securities-markets` (market-structure-execution-quality; follow-up). **Question.** Has FINRA applied Rule 5210.03 in a disciplinary action, and on what facts? **Source or input.** FINRA disciplinary actions (finra.org), a route not tried before. **Would resolve it.** A dated action citing Rule 5210, Supplementary Material .03, or the search outcome. **Outcome: unchanged.** No FINRA disciplinary action citing Rule 5210.03 was found: the search returned exchange rule filings on expedited suspension for layering and a press report of a BGC AWC under Rules 3110 and 2010 (not verified at FINRA; finra.org's action database not queried automatically). The enforcement gap stands. **Recorded in:** `none`.
47. `ev:circuit-breaker-effects` (market-structure-execution-quality; follow-up). **Question.** What did the MWCB working group's study conclude about the March 2020 halts? **Source or input.** The study via an Internet Archive capture of its nyse.com link. **Would resolve it.** Its conclusions at locators, or the access outcome. **Outcome: resolved.** MWCB Working Group report (31 March 2021) read via an Internet Archive capture of the nyse.com link: mechanism worked as intended, halts calmed volatility without harm, 7/13/20 and 15 minutes appropriate, four recommendations; descriptive evidence only. Merged into mech:circuit-breakers-trading-halts. **Recorded in:** `mech:circuit-breakers-trading-halts`.
48. `ev:dark-pool-price-discovery` (market-structure-execution-quality; follow-up). **Question.** What are Buti, Rindi and Werner's price-efficiency results in the published 'Diving into Dark Pools'? **Source or input.** Author or institutional copies (a route not tried before). **Would resolve it.** The results at locators, or the access outcome. **Outcome: blocked.** No open copy of the published Buti, Rindi and Werner (2022) found (Bocconi, Dauphine and OSU profiles give citations only; Wiley paywall); the 2010 Dice working paper was read earlier. Not obtained. **Recorded in:** `none`.

*J. Crypto: perpetuals, options, AMMs, lending, stablecoins and leverage*
49. `ev:crypto-funding-crowding` (crypto-perpetuals; follow-up). **Question.** What do perpetual funding rates measure in He, Manela, Ross and von Wachter, and how large are the deviations from the no-arbitrage price? **Source or input.** arXiv 2212.06888, draft of September 2026 (roadmap-perpetual-fundamentals; only the abstract read before). **Would resolve it.** The no-arbitrage price, the funding definition and reported magnitudes at locators. **Outcome: narrowed.** He, Manela, Ross and von Wachter (arXiv v7) read in full introduction: deviations 52-90%/yr, comove, shrink 22 pp/yr; driven by end-user leverage demand against limited arbitrage capital (portfolio margining compressed them). Merged into mech:perpetual-funding. Funding as positioning concentration (crowding) still untested. **Recorded in:** `mech:perpetual-funding`.
50. `ev:crypto-dated-futures-carry` (crypto-perpetuals; follow-up). **Question.** Do BIS WP 1087's ETF difference-in-differences coefficients match the text's 3 and 5 percentage points? **Source or input.** BIS WP 1087, Table 5, page image (local copy). **Would resolve it.** The coefficients and their units. **Outcome: resolved.** BIS 1087 Table 5 (page image): ETF DiD Post -0.03, TreatxPost -0.05; micro futures +0.11; basis in annual decimals, matching the text's 3 and 5 pp. Merged into ev:crypto-dated-futures-carry. **Recorded in:** `ev:crypto-dated-futures-carry`.
51. `def:crypto-options-venue-structure` (crypto-perpetuals; follow-up). **Question.** How does a second venue's option listing compare with Deribit's (settlement currency, open-interest concentration)? **Source or input.** OKX public API, instruments and open interest, one day. **Would resolve it.** A dated snapshot summary. **Outcome: tested within stated bounds.** OKX public API snapshot (17 Oct 2026): 1,466 BTC options, 99.2% of 2.55 bn USD OI inverse, top 3 expiries 64.7%; same pattern as Deribit. Merged into def:crypto-venue-instrument-structure; script and output retained. **Recorded in:** `def:crypto-venue-instrument-structure`.
52. `def:amm-pool-mechanics` (amm-lending; follow-up). **Question.** How do trading fees and block times change arbitrage profits (LVR) in Milionis, Moallemi and Roughgarden? **Source or input.** arXiv 2305.14604v2 (roadmap-amm-fees). **Would resolve it.** The probability-of-trade result and its formula at locators. **Outcome: resolved.** Milionis, Moallemi and Roughgarden (arXiv v2) read: P_trade formula, ARB ~ LVR x P_trade, FEE ~ LVR x (1-P_trade), lower gas fees reduce LP losses. Merged into def:amm-pool-mechanics; measured gas costs still unread. **Recorded in:** `def:amm-pool-mechanics`.
53. `res:cfmm-reported-price` (amm-lending; new). **Question.** What no-arbitrage band ties a CFMM's reported price to the market price, per Angeris and Chitra? **Source or input.** arXiv 2003.10001 (s6-cfmm). **Would resolve it.** The bound with fee gamma at locators and an own check. **Outcome: resolved.** Angeris and Chitra (arXiv v4) read: reported price as supporting hyperplane, arbitrage incentive, fees make CFMMs path-deficient (1/gamma more input). Merged into def:amm-pool-mechanics. **Recorded in:** `def:amm-pool-mechanics`.
54. `ev:uniswap-reference-tracking` (amm-lending; new). **Question.** Do Angeris et al. find Uniswap prices tracking reference markets, and under what conditions? **Source or input.** arXiv 1911.03380 (s11-r12). **Would resolve it.** The conditions and the empirical comparison at locators. **Outcome: narrowed.** Angeris et al. (arXiv v7) abstract read: constant-product markets must closely track the reference price under common conditions; simulation stability. Merged into def:amm-pool-mechanics. Only the abstract (or abstract and introduction) was read, so methods and robustness are unchecked. **Recorded in:** `def:amm-pool-mechanics`.
55. `meth:cfmm-convex-multi-asset-trade` (amm-lending; new). **Question.** How can a multi-asset CFMM trade be posed as a convex problem? **Source or input.** Angeris et al., arXiv 2107.12484 (roadmap-cfmm-convex). **Would resolve it.** The trading-function conditions and the convex formulation at locators. **Outcome: narrowed.** Angeris et al. (arXiv v1) abstract read: multi-asset CFMM trades as convex problems. Merged into def:amm-pool-mechanics. Only the abstract (or abstract and introduction) was read, so methods and robustness are unchecked. **Recorded in:** `def:amm-pool-mechanics`.
56. `mech:uniswap-v4-hooks` (amm-lending; new). **Question.** What do Uniswap v4 hooks and dynamic fees change in pool mechanics? **Source or input.** Uniswap v4 Core whitepaper (exp-uniswap4). **Would resolve it.** The hook points and fee rules at locators. **Outcome: resolved.** Uniswap v4 whitepaper (August 2024) read: hooks, dynamic fees, singleton, flash accounting. Merged into def:amm-pool-mechanics. **Recorded in:** `def:amm-pool-mechanics`.
57. `mech:auction-managed-amm` (amm-lending; new). **Question.** What does the am-AMM's auction manage, and what does it claim for fees and arbitrage? **Source or input.** Adams, Moallemi, Reynolds and Robinson, arXiv 2403.03367v4 (exp-amamm). **Would resolve it.** The mechanism and claims at locators. **Outcome: narrowed.** am-AMM (arXiv v4) abstract read: auction for pool manager, fee setting, higher equilibrium liquidity under assumptions. Merged into def:amm-pool-mechanics. Only the abstract (or abstract and introduction) was read, so methods and robustness are unchecked. **Recorded in:** `def:amm-pool-mechanics`.
58. `mech:defi-lending-liquidation` (defi-lending-liquidations; new). **Question.** How do DeFi lending protocols liquidate (fixed spread against auction), and how much was liquidated in Qin et al.'s sample? **Source or input.** Qin et al., arXiv 2106.06389 (roadmap-defi-liquidations). **Would resolve it.** The mechanisms, totals and periods at locators. **Outcome: resolved.** Qin et al. (arXiv v2) read: fixed spread vs auction, 807.46m USD, 28,138 events, bad debt, 43% ETH fall -> 1.07bn liquidatable. New entry mech:defi-lending-liquidation. **Recorded in:** `mech:defi-lending-liquidation` (new entry).
59. `mech:defi-lending-liquidation` (defi-lending-liquidations; new). **Question.** How sensitive is liquidatable debt to collateral price drops in Perez et al.? **Source or input.** Perez, Werner, Xu and Livshits, arXiv 2009.13235 (oc-perez-knife-edge-2021). **Would resolve it.** The reported sensitivity at locators. **Outcome: narrowed.** Perez et al. (arXiv v6) abstract read: 3% price moves -> over 10m USD liquidatable; >70% liquidated immediately. In mech:defi-lending-liquidation. Only the abstract (or abstract and introduction) was read, so methods and robustness are unchecked. **Recorded in:** `mech:defi-lending-liquidation` (new entry).
60. `mech:defi-lending-liquidation` (defi-lending-liquidations; new). **Question.** How does Aave V3 define the health factor and how much debt may one liquidation repay? **Source or input.** Aave V3 Technical Paper (January 2022) (al-aave). **Would resolve it.** The definitions and close-factor rule at locators. **Outcome: resolved.** Aave V3 technical paper read: full liquidation below HF 0.95 (V2 half), L2 grace period, e-mode example. In mech:defi-lending-liquidation. **Recorded in:** `mech:defi-lending-liquidation` (new entry).
61. `ev:stablecoin-runs` (stablecoin-pegs-runs; new). **Question.** Do stablecoin runs resemble money-fund runs, with flights to safer coins and a threshold near USD 0.99? **Source or input.** Anadu et al., New York Fed Staff Report 1073 (cd-anadu-2023). **Would resolve it.** The reported flows and thresholds at locators. **Outcome: resolved.** Anadu et al. (SR 1073) read: flight to safety, break-the-buck at 1 USD (+34 bp daily outflow below), within-chain flows. New entry ev:stablecoin-runs; the guide's '0.99' wording and the paper's '95-cent' slip noted. **Recorded in:** `ev:stablecoin-runs` (new entry).
62. `rule:stablecoin-standards` (stablecoin-pegs-runs; new). **Question.** What do the FSB's 2023 recommendations require for redemption and reserve assets? **Source or input.** FSB final report, 17 July 2023 (cd-fsb-stablecoin-2023). **Would resolve it.** The recommendation texts at locators. **Outcome: resolved.** FSB final report (17 July 2023) Recommendation 9 read: legal claim, timely redemption at par, stabilisation; algorithmic stablecoins do not meet it. New entry rule:stablecoin-standards. **Recorded in:** `rule:stablecoin-standards` (new entry).
63. `ev:stablecoin-network-settlement-risk` (stablecoin-pegs-runs; follow-up). **Question.** What does CPMI-IOSCO require of a stablecoin arrangement on settlement finality and money settlement? **Source or input.** CPMI-IOSCO, July 2022 (d206), Internet Archive capture (cd-cpmi-iosco-stablecoin-pfmi-2022). **Would resolve it.** The guidance on Principles 8 and 9 at locators. **Outcome: narrowed.** CPMI-IOSCO July 2022 (Internet Archive capture; bis.org served HTML) read: Principle 8 finality, probabilistic settlement and forks, Principle 9 little or no credit/liquidity risk. Merged into def:crypto-trading-risk-layers; measured congestion and bridge delays still unread. **Recorded in:** `def:crypto-trading-risk-layers`.
64. `ev:stablecoin-runs` (stablecoin-pegs-runs; new). **Question.** How large is the effect of stablecoin flows on Treasury bill yields, per Ahmed and Aldasoro? **Source or input.** BIS WP 1270 (rt-ahmed-aldasoro-stablecoins). **Would resolve it.** The estimate (bp per flow unit) at locators, or the access outcome. **Outcome: narrowed.** BIS WP 1270 May 2025 version (Internet Archive capture) read: 2-sd inflow lowers 3m bill yields 2-2.5 bp in 10 days; outflows 2-3x larger. In ev:stablecoin-runs; the March 2026 revision not compared. Only the abstract (or abstract and introduction) was read, so methods and robustness are unchecked. **Recorded in:** `ev:stablecoin-runs` (new entry).
65. `mech:crypto-auto-deleveraging` (crypto-leverage-liquidations; new). **Question.** What is auto-deleveraging, and what does Chitra report for the October 2025 cascade? **Source or input.** Chitra, arXiv 2512.01112 v3 (cd-chitra-adl-2025). **Would resolve it.** The mechanism, the trilemma and the reported figures at locators. **Outcome: resolved.** Chitra (arXiv v3) read: ADL trilemma; Hyperliquid 10 Oct 2025, 2.1bn in 12 minutes, excess haircut 45.0-51.7m USD. New entry mech:crypto-auto-deleveraging. **Recorded in:** `mech:crypto-auto-deleveraging` (new entry).
66. `mod:liquidity-spirals` (crypto-leverage-liquidations; new). **Question.** When are margins destabilising in Brunnermeier and Pedersen, and what makes a loss spiral? **Source or input.** NBER WP 12939 (exp-brunnermeier-pedersen-liquidity). **Would resolve it.** The propositions and conditions at locators. **Outcome: resolved.** Brunnermeier and Pedersen (NBER WP 12939) read: destabilising margins, Propositions 1-3, margin and loss spirals. New entry mod:liquidity-spirals. **Recorded in:** `mod:liquidity-spirals` (new entry).

*K. Data, transaction costs, volatility management and breaks*
67. `ev:holdings-insider-ratings-signals` (alternative-data-sources; follow-up). **Question.** How much do opportunistic insider trades earn against routine ones? **Source or input.** Cohen, Malloy and Pomorski, NBER WP 16454 (the Harvard DASH copy refused). **Would resolve it.** The return spreads and sample at locators. **Outcome: narrowed.** NBER WP 16454 read (Harvard DASH refused with a CAPTCHA): routine-trader definition, opportunistic long-short 82 bp VW (t 2.15) and 180 bp EW (t 6.07), routine -20 bp (t -0.57); merged into the insider passage. 13F holdings and rating-downgrade evidence still unsourced. **Recorded in:** `def:financial-data-types`.
68. `res:no-trade-region` (portfolio-construction; follow-up). **Question.** What do Shreve and Soner prove about the no-trade wedge, as a route to Davis and Norman's result? **Source or input.** Shreve and Soner, Ann. Appl. Probab. 4(3), 1994, Internet Archive capture of the open Project Euclid PDF. **Would resolve it.** The theorem's conditions and the wedge's form at locators. **Outcome: narrowed.** Shreve and Soner (1994; archived open-access scan) sec. 1 read as page images: wealth-independent no-trade interval under only a finite value function; Davis and Norman's assumptions called restrictive; leverage reduced by costs; 2/3-power liquidity premium. Merged into mod:portfolio-transaction-cost-function. Davis and Norman's own paper still not obtained. **Recorded in:** `mod:portfolio-transaction-cost-function`.
69. `ev:volatility-managed-portfolios` (risk-parity-vol-targeting; new). **Question.** Do volatility-managed portfolios beat their unmanaged versions out of sample, per Cederburg et al.? **Source or input.** Cederburg, O'Doherty, Wang and Yan, JFE 138, 2020, co-author-hosted copy (wide-cederburg-volmanaged). **Would resolve it.** The number of strategies, the real-time comparison and the stated cause at locators. **Outcome: resolved.** Cederburg et al. (JFE 2020, co-author copy) read: 103 strategies, 77 positive spanning alphas, real-time CER lower in 72 of 103, structural instability. In ev:volatility-managed-portfolios. **Recorded in:** `ev:volatility-managed-portfolios` (new entry).
70. `meth:structural-break-tests` (time-series-volatility; new). **Question.** How do Bai and Perron estimate break dates and test for several breaks (trimming, maximum breaks, sequential and sup-F tests)? **Source or input.** Bai and Perron (2003) not obtained; route: their 1995 MIT working paper (Internet Archive), the basis of the 1998 Econometrica paper. **Would resolve it.** The procedures and their stated conditions at locators. **Outcome: narrowed.** Bai and Perron's 1995 MIT WP 95-17 (Internet Archive scan, OCR) read: rate-T break fractions, trimmed sup-F test, sequential l vs l+1 procedure, BIC vs AIC. New entry meth:structural-break-tests. The 2003 JAE paper the catalogue cites was not obtained. **Recorded in:** `meth:structural-break-tests` (new entry).

### Counts

- **Stage 1:** seven audit repairs, all made; three empirical outputs regenerated (inflation row on quarterly vintages, FX inference for two scripts, heating-oil premium), with the earlier runs kept and reproducible; no verdict of an empirical test changed.
- **The 70 targets:** 41 resolved, 21 narrowed, 5 tested within stated bounds, 2 blocked, 1 unchanged, none deferred. Follow-ups (24): 5 resolved, 13 narrowed, 4 tested, 1 blocked, 1 unchanged. New questions (46): 36 resolved, 8 narrowed, 1 tested, 1 blocked. Six targets answered from abstracts only (37, 54, 55, 57, 59, 64) are counted as narrowed, not resolved.
- **New entries: 15** (239 $\to$ 254), all draft: `ev:correlation-matrix-noise`, `meth:volatility-forecast-loss`, `meth:structural-break-tests`, `ev:volatility-managed-portfolios`, `mod:heston-stochastic-volatility`, `mod:merton-jump-diffusion`, `mod:sabr-smile`, `data:gsw-treasury-curve`, `ev:money-fund-runs`, `ev:cip-deviations`, `mech:defi-lending-liquidation`, `ev:stablecoin-runs`, `rule:stablecoin-standards`, `mech:crypto-auto-deleveraging`, `mod:liquidity-spirals`. Eight pathway notes were opened for their owning pathways (`high-dimensional-estimation`, `time-series-volatility`, `risk-parity-vol-targeting`, `option-pricing-models`, `fx-cip-dollar-funding`, `defi-lending-liquidations`, `stablecoin-pegs-runs`, `crypto-leverage-liquidations`); entries of the guide sections `common-toolkit` and `onchain-protocols`, which have no chapter folder, sit in the nearest existing chapter, as each note says. Legacy blocks 0.

### Conclusions that changed

- Inflation-shock row: the headline now rests on the quarterly vintages the protocol named; no response is supported either way.
- FX forecasts: the evidence against the carry and PPP forecasts is weaker than reported (carry $h=12$ Clark--West $t=-1.97$, not $-4.44$); both still lose to the random walk out of sample.
- Heating oil: the premium slope is smaller with log returns (0.33, $t=1.55$); still not supported.
- FRA valuation: start- and end-settled values differ on two curves; the deterministic substitution is a convention-specific approximation.
- ERC: maximum Sharpe ratio only with a positive common Sharpe ratio.
- Crypto carry and liquidations: a standard deviation of carry goes with about 2.2 percentage points of open interest more sell liquidations, not 22 percent of open interest.
- Manipulation intent: MAR's administrative regime does not generally require intent; criminal liability and Rule 10b-5 do.
- New empirical results (targets 41, 42, 45): WTI hedging pressure does not predict returns; rolling hedge ratios beat a static ratio modestly out of sample for jet fuel; the deflation row is not supported in real time.
- Sources: U.S.\ commercial paper averages about 30 days (BIS), against Gliner's ``most between 90 and 270 days''; Laloux et al.'s $\sigma^2=1-\lambda_{\max}/N$ must mean $\lambda_1$; GJR's working paper puts the indicator on positive shocks; Anadu et al.\ estimate a USD~1 break-the-buck threshold, not the guide note's USD~0.99; Avellaneda and Lee chose their s-score cutoffs inside their backtest period; Boyd et al.'s multi-period gain comes mostly from an extra, unrealistic forecast.

### Sources

Listed with URL, retrieval date, acquisition route, size and SHA-256 in `reading_materials/sources_derivatives-validation_2026-10-17.json` (93 files kept; 11 wrong or failed responses kept only as evidence; 21 failed or refused requests; reused earlier files and the local Hull copy listed; ignored, none committed). 19 source keys were added to `compendium/front/sources.tex` (317 in all). Internet Archive captures were used where a publisher refused automated retrieval or served a web page in place of a PDF: BIS (CPMI--IOSCO d206, WP 1270, BCBS--IOSCO d499), the FCA (PS24/14), Project Euclid (Shreve and Soner), MIT DSpace (Merton's working paper, HTTP 429), BME (IBEX notice), nyse.com (the MWCB report, 404 directly), Hansen's former Brown page, an LBS faculty page (DeMiguel, Garlappi and Uppal) and the Internet Archive's own scan of Bai and Perron's 1995 working paper. CELLAR content negotiation needed the XHTML representation for Directive 2014/57/EU. Refused or unavailable, not bypassed: the Library of Congress's U.S. Reports PDFs (403; Cornell LII used), Harvard DASH (CAPTCHA; NBER copy used), SSRN (Hull and White, 403), Oxford ORA (Patton, 403; the UTS working paper used), a former NYU Stern page for Merton (404), Leland (no open copy), Buti, Rindi and Werner's published paper (no open copy), and a Nasdaq filing (TLS certificate mismatch). A first BIS request returned a different article; the CP primer was then read from its own page.

### Checks

New, all exit 0: `fx-determination-forecasting/fx-panel-inference-check.py`, `rates-credit-mortgages/fra-settlement-check.py`, `portfolio-construction/erc-sharpe-check.py`, `high-dimensional-estimation/covariance-volatility-checks.py`, `option-pricing-models/option-model-checks.py`, `risk-parity-vol-targeting/risk-parity-checks.py`. All 50 check scripts in `notes/artefacts/` (outside the preserved-run folders) were rerun and pass. `tools/check_compendium.py --check`: 0 problems. `python3 -B -m unittest discover -s tools`: 14 tests OK.

Empirical scripts rerun from retained inputs and compared byte for byte with their saved outputs, all identical: `inflation_quarterly_test.py`, `inflation_regime_test.py` (sensitivity), `deflation_row_test.py`, `fx_ppp_oos_test.py`, `fx_carry_test.py`, `heating_oil_test.py`, `backwardation_test.py`, `hedging_pressure_test.py`, `jet_fuel_hedge_test.py`, `gsw-kw-acm.py`, `okx-options-snapshot.py`, `regime_recession_test.py`, both global-macro scripts, `acm-term-premium-summary.py` and `deribit-options-snapshot.py`; committed panels other than the heating-oil panel (regenerated with the log return and the date gap) are unchanged. The preserved pre-correction FX scripts and the simple-return heating-oil script reproduce their committed outputs when run from copies of their folders.

### Build

Clean `latexmk -pdf compendium.tex` after `latexmk -C`: exit 0, 346 pages (328 after empirical extensions (2026-10-17)). The first clean build had two overfull and five underfull boxes from new text; they were removed by rewording (long file names moved to sentence ends, two catalogue keys set as a list). After the last edit: 0 overfull and 0 underfull boxes, no LaTeX warnings, and the inherited `page.i` duplicate-destination warning only. Pages with the FRA conventions, the inflation and deflation rows, the FX inference, ERC, Heston, the Marchenko--Pastur entry, the spoofing pitfalls and the DeFi entries were inspected as images.

### Other files

- Pathway notes: 34 existing notes received a dated fourth-batch paragraph (backlog reconciliation alone for some), three list new entries, and `multi-asset-systematic-macro` carries the explicit ``run as registered'' correction; eight new notes.
- Also updated: `notes/log.md` (no dates of mastery or consolidation), `notes/source-review-index.md`, `compendium/README.md`, the Hull reading note, `compendium/front/sources.tex`, and the protocol files of the inflation and heating-oil tests (corrections appended).

### For review

- The quarterly-vintage rerun and its diagnostic, and whether the monthly run should stay as a sensitivity.
- The calendar-month panel standard error for pooled Clark--West tests (`panel_nw_t`), including the $h-1$ against $h$ lag choice for 12-month changes of monthly averages.
- The heating-oil month-end calendar (last common observation) and EIA's contract definition used in place of the NYMEX rule.
- The FRA settlement wording and the stochastic-valuation conditions; the ERC condition and counterexample.
- The withdrawn liquidation figure and the unresolved prose of BIS WP 1087.
- The manipulation-intent rewrite (EU administrative, EU criminal, U.S. securities, FINRA).
- Target identifiers given to merged new questions, and the six abstract-only targets counted as narrowed.
- Archived copies used in place of refused publisher pages; working papers read in place of published versions (Hansen, Romano and Wolf, Patton, GJR, DeMiguel et al.\ excepted, Merton, Brunnermeier and Pedersen, Bai and Perron).
- The guide's reading note for `cd-anadu-2023` (USD~0.99) against the paper (USD~1); the pin is unchanged.
