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

## Next bounded slice

`compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/05_market_impact_models.tex`. Its blocks (seen while routing this slice: linear impact, propagator, *Permanent Impact or Price Anticipation*, *Permanent-Impact View Segmentation*, *Propagator Midprice Dynamics*, *Propagator Kernel Segmentation*) overlap `def:price-impact` and `mod:propagator`. Read and compare them before merging. The map gives it a single candidate, `price-impact-execution`, so its blocks count to that pathway already. `04_.../04_price_impact_estimation.tex` would follow. The three slice-5 assignments, the eight flash-crash and systemic blocks, and the deferred items (the toy-model time term, Lehalle and Laruelle sec. 2.5.3, Ho–Stoll) are unchanged.

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
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/04_price_impact_estimation.tex` | price-impact-execution |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/05_market_impact_models.tex` | price-impact-execution |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/06_trade_duration_and_event_time.tex` | market-simulation, lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/07_statistical_models_for_order_flow.tex` | market-simulation, market-making-lob |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/08_feature_engineering_for_microstructure_alpha.tex` | lob-deep-learning |
| `compendium/legacy/execution-market-making/04_order_flow_and_empirical_microstructure/09_microstructure_data_engineering.tex` | lob-deep-learning, market-simulation |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/01_economics_of_market_making.tex` | market-making-lob, execution-market-making |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/04_optimal_quoting_and_inventory_control.tex` | market-making-lob, execution-market-making |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/05_latency_and_queue_competition.tex` | market-making-lob, hft-market-design |
| `compendium/legacy/execution-market-making/05_market_making_and_liquidity_provision/06_cross_asset_and_cross_venue_market_making.tex` | market-making-lob, hft-market-design |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/01_optimal_execution_problem.tex` | price-impact-execution, execution-trading-costs |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/02_execution_benchmarks.tex` | execution-trading-costs, market-structure-execution-quality |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/03_execution_algorithms.tex` | execution-trading-costs, price-impact-execution |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/04_transaction_cost_analysis.tex` | market-structure-execution-quality, execution-trading-costs |
| `compendium/legacy/execution-trading-costs/01_execution_and_algorithmic_trading/05_smart_order_routing.tex` | market-structure-execution-quality |
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
