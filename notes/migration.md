# Compendium migration record

The working record for moving the notes written before the study method into the guide's typed entries. The plan, with its type mapping and order, is in [compendium/README.md](../compendium/README.md); this file records what has been done, what was checked and the map of legacy files to pathways. Check the map and progress with `python3 tools/migration_status.py` (add `--check` to fail on any problem).

## Four kinds of progress, kept apart

| Kind | What it means | Where it is recorded | Set by |
|---|---|---|---|
| Migration progress | A legacy block has a disposition: rewritten as an entry, merged into one, stubbed in a backlog, or deleted | This file and `tools/migration_status.py` | The migration |
| Source verification | An entry's claims have been compared with the passages at their locators | Each entry's *Status: Verification*, and the checks table below | Whoever reads the passage |
| Learner mastery | A pathway's checkpoint passed from your own notes, readings closed | `notes/log.md`, *Mastered* | You only |
| Pathway consolidation | Everything the pathway relies on is in checked entries and its backlog is empty | `notes/log.md`, *Consolidated* | You, after review |

Migrating a block and compiling the result advances only the first. An entry written during migration starts as a draft whose verification says exactly what was compared; no migration step sets a mastery or consolidation date.

## Conventions

- **Legacy staging.** Old chapters live in `compendium/legacy/<section-key>/` and compile, through `compendium/legacy/part.tex`, as the final part *Notes awaiting migration*. This is a temporary convention of this repository, not part of the guide's layout. Their chapter labels carry a `legacy:` prefix so that they never collide with the canonical chapter label (`\label{<section-key>}`) when that chapter appears. Their block, figure and remark labels are unchanged.
- **Canonical homes.** Migrated entries go in `compendium/<section-key>/`, in the section where the guide first needs the concept. Other pathways link to that entry rather than restating it.
- **Map.** `% migrate-to: key, key` on the first line of each legacy file with blocks names the pathways its blocks are *candidate* material for. These lists are provisional: drawn from the plan's folder table and narrowed by file name, not from reading every block. A file listing several pathways is shared material; none of those pathways owns its blocks until one is assigned.
- **Assignment.** `% assign: <pathway-key>` on the line before a block assigns that block to one pathway. Only assigned blocks, or blocks in a file with a single candidate, count towards one pathway; the status script lists shared, unassigned blocks separately.
- **Removal.** A block is deleted from a legacy file only when its content is represented in an entry, a backlog stub or an artefact, and the pathways that list the file can find it: the deletion site keeps a `% migrated:` comment naming the destination labels.
- **Derivations.** When an entry keeps only the idea of a proof, the full working goes to `notes/artefacts/<pathway-key>/`, and the entry's *Further reading* names the file.

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

## Next bounded slice

`compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/06_high_frequency_trading_strategies.tex` (3 blocks), shared between `execution-trading-costs` and `market-structure-execution-quality`. Likely overlaps: `def:order-anticipation` and the market-making entries of `execution-market-making` (its strategy taxonomy), `def:smart-order-routing` (latency and liquidity detection), and the `hft-market-design` pathway, which is not among the file's map candidates and already holds the assigned flash-crash blocks. The three slice-5 assignments, the eight flash-crash and systemic blocks, and the deferred items (the toy-model time term, Lehalle and Laruelle sec. 2.5.3, Ho–Stoll) are unchanged.

## File map

One row per legacy file with blocks; `tools/migration_status.py --check` fails if this table and the files' `% migrate-to:` lines disagree.

<!-- map:begin -->
| Legacy file | Candidate pathways |
|---|---|
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/01_roles_of_financial_markets.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/02_market_participants_and_trading_motives.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/03_trading_venues_and_market_architecture.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/04_auction_and_dealer_market_structures.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/05_market_quality_and_efficiency.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/01_foundations_of_trading_and_market_organization/06_regulatory_and_structural_evolution.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/01_order_types_and_instructions.tex` | execution-market-making, market-making-lob, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/02_order_lifecycle.tex` | execution-market-making, market-making-lob, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/03_limit_order_book_mechanics.tex` | execution-market-making, market-making-lob, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/04_matching_algorithms.tex` | execution-market-making, market-making-lob, futures-execution |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/05_queue_dynamics_and_latency.tex` | execution-market-making, market-making-lob |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/06_hidden_liquidity_and_dark_trading.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/02_orders_matching_and_limit_order_books/07_cross_venue_routing_and_fragmentation.tex` | execution-market-making, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/03_information_price_formation_and_spreads/02_price_discovery.tex` | execution-market-making, market-making-lob, market-structure-execution-quality, hft-market-design |
| `compendium/legacy/execution-market-making/03_information_price_formation_and_spreads/08_volatility_and_liquidity_interaction.tex` | execution-market-making, market-making-lob, hft-market-design, market-structure-execution-quality |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/01_trade_classification_and_signed_flow.tex` | price-impact-execution, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/02_order_flow_imbalance.tex` | market-making-lob, lob-deep-learning, price-impact-execution |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/03_stylized_facts_of_high_frequency_data.tex` | market-simulation, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/06_trade_duration_and_event_time.tex` | market-simulation, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/07_statistical_models_for_order_flow.tex` | market-simulation, market-making-lob |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/08_feature_engineering_for_microstructure_alpha.tex` | lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/09_microstructure_data_engineering.tex` | lob-deep-learning, market-simulation |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/01_economics_of_market_making.tex` | market-making-lob, execution-market-making |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/04_optimal_quoting_and_inventory_control.tex` | market-making-lob, execution-market-making |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/05_latency_and_queue_competition.tex` | market-making-lob, hft-market-design |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/06_cross_asset_and_cross_venue_market_making.tex` | market-making-lob, hft-market-design |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/06_high_frequency_trading_strategies.tex` | execution-trading-costs, market-structure-execution-quality |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/07_reinforcement_learning_and_ml_in_execution.tex` | reinforcement-learning-trading |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/08_production_considerations.tex` | model-governance-controls |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/01_equity_market_microstructure.tex` | market-structure-execution-quality |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/02_futures_market_microstructure.tex` | futures-execution |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/03_fx_market_microstructure.tex` | fx-dealer-market-making |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/04_options_market_microstructure.tex` | options-execution |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/05_fixed_income_microstructure.tex` | otc-fixed-income-trading |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/06_securities_lending_and_synthetic_shorts.tex` | synthetic-equity-cfd-trs |
| `compendium/legacy/execution-trading-costs/02_asset_class_specific_microstructure/07_crypto_market_microstructure.tex` | crypto-mm-microstructure |
| `compendium/legacy/ml-alternative-data/data/datalabel.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/datasampleweights.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/datastruct.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/fracdifffeat.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/ml-alternative-data/data/taxonomy.tex` | statistical-learning-foundations, financial-ml-evaluation, alternative-data-sources |
| `compendium/legacy/multi-asset-systematic-macro/01_regimes.tex` | multi-asset-systematic-macro, macro-regimes-stock-bond |
| `compendium/legacy/multi-asset-systematic-macro/02_transmission_maps.tex` | macro-nowcasting-signals, macro-announcements-policy, monetary-policy-curve, fx-determination-forecasting |
| `compendium/legacy/multi-asset-systematic-macro/03_practitioner_insights.tex` | multi-asset-systematic-macro |
| `compendium/legacy/portfolio-construction-risk/sysinv/alphamod.tex` | portfolio-construction-risk |
| `compendium/legacy/portfolio-construction-risk/sysinv/executionmod.tex` | portfolio-construction-risk |
| `compendium/legacy/portfolio-construction-risk/sysinv/modelrisk.tex` | model-governance-controls |
| `compendium/legacy/portfolio-construction-risk/sysinv/portconstmod.tex` | portfolio-construction |
| `compendium/legacy/portfolio-construction-risk/sysinv/research.tex` | research-engineering-validation |
| `compendium/legacy/portfolio-construction-risk/sysinv/riskmod.tex` | portfolio-construction |
| `compendium/legacy/portfolio-construction-risk/sysinv/sysinvoverview.tex` | portfolio-construction-risk |
| `compendium/legacy/portfolio-construction-risk/sysinv/txncostmod.tex` | portfolio-construction-risk |
| `compendium/legacy/rates-credit-mortgages/01_tvm.tex` | rates-credit-mortgages, performance-manager-evaluation |
| `compendium/legacy/volatility-options/basic.tex` | volatility-options |
| `compendium/legacy/volatility-options/fwdfut.tex` | rates-credit-mortgages, commodity-hedging |
<!-- map:end -->
