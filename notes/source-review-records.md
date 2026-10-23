# Source-review records

The record of each source review, from the format pilot of 14 October 2026 to the latest validation pass, in order: scope, sources and their availability, source findings, checks and their limits. Dates, results and source identities describe the original reviews; topic names and paths use the current naming conventions. Corrections appear beside the findings they qualify. The conventions, current status, topic index and file map are in [source-review-index.md](source-review-index.md). Open questions arising from the reviews are also logged in [log.md](log.md). Bookkeeping for moving the earlier notes into the compendium (block routing, counts, preservation and build logs) was removed from these records on 18 October 2026, together with the earlier notes and their artefact copies, which remain in the repository history at commit `199ed96`; "left as written" in a follow-up means that the earlier record's findings were not revised.

## Pilot: `market-making-lob` format pilot, 14 October 2026

A test of the entry format on the formal models discussed below. Grossman–Miller and Kyle are supplemental to `market-making-lob`; its required readings (Glosten–Milgrom, Ho–Stoll, Guéant–Lehalle–Fernandez-Tapia, the queue and order-flow papers) are not covered, and the pathway is neither mastered nor consolidated.

### Source findings

- Grossman–Miller, with its fee extension and liquidity measures, and *Market Making using Limit Orders* follow Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (`crypto-cartea`), chapter "A Primer on the Microstructure of Financial Markets", pp. 20–30, in notation and order; `grossman-miller-1988` and `ho-stoll-1981` were not consulted.
- The limit-order quoting model is **not** the Ho–Stoll model. The book sets it up as a static simplification in place of Ho and Stoll (1981), which it calls the usual first reference (p. 28). Its citation of `ho-stoll-1981` was therefore wrong for its formulas; the entry cites `crypto-cartea` and lists `ho-stoll-1981` only as further reading. `catalogue-0527`, the route's Ho–Stoll reading, is a topic lead that names no paper and was not substituted for one.
- The Kyle equilibrium ($\beta=\sigma_u/\sigma_v$, $\lambda=\sigma_v/(2\sigma_u)$, profit $\sigma_v\sigma_u/2$, posterior variance $\sigma_v^2/2$) agrees with O'Hara, *Market Microstructure Theory* (`catalogue-0496`), chapter "Strategic Trader Models I: Informed Traders", pp. 91–98, eqs. (4.3)–(4.5), (4.17), (4.20). `crypto-cartea` p. 33 prints $\lambda=2\sigma_u/\sigma$, the reciprocal, which contradicts its own step $\beta=(2\lambda)^{-1}$; the entry records the conflict in its *Pitfalls*. The earlier notes cited `s6-kyle`, which was not consulted.
- The earlier notes' Avellaneda–Stoikov formulas agree with the author-hosted journal PDF of `s6-stoikov` (eqs. (8), (12), (29)–(30)), with one omission now stated: the spread formula is an approximation from an expansion in inventory with a linearised order-arrival term (sec. 3.2), not the exact solution.

### Findings on the earlier notes

| Earlier block (file) | Disposition |
|---|---|
| *Grossman-Miller Model* (`05_.../01_economics_of_market_making.tex`), main equilibrium | Rewritten as `mod:grossman-miller`; figure kept as `fig:grossman_miller_trading` |
| same block, *Implications* items on free entry ("until spread capture just covers $c$") and market design (migration to search, block crossing or delayed execution) | Not supported by `crypto-cartea`; kept verbatim in the artefact and stubbed in the pathway backlog as needing `grossman-miller-1988` |
| *Kyle Linear Price Impact* and *Kyle Linear Equilibrium* (`03_.../05_information_based_models.tex`), a second version of the same model in other notation | Merged into `mod:kyle-single-auction` (same equilibrium; its notation, $p_\infty$, $n_\omega$, $\tilde P$, is kept in the artefact) |
| *Market Making using Limit Orders* (same file as Grossman–Miller) | Rewritten as `mod:static-limit-order-depth`; figure kept as `fig:limit_order_market_making` |
| *Framework, Not Production Model* caveat (same file) | Merged into the *Pitfalls* of `mod:avellaneda-stoikov`, marked as interpretation |
| *Inventory-Skew Quoting* model (`03_.../04_inventory_models.tex`) | Deferred: Ho–Stoll-related, unsourced, needs the Ho–Stoll paper |
| *Adverse Selection Through Flow* principle (`03_.../05_information_based_models.tex`) | Deferred: interpretation of the Kyle and Glosten–Milgrom mechanisms |

**Source blockers.** As at the pilot; rechecked in dealer-information models review below, which unblocked Grossman–Miller through its NBER working paper and the `crypto-cartea` p. 33 misprint through the authors' errata. spread and inventory models review rewrote *Inventory-Skew Quoting* from textbook accounts (Hasbrouck's version of Stoll (1978); O'Hara's report of Ho–Stoll); the Ho–Stoll paper itself is still needed, for the backlog stub `res:ho-stoll-dealer-pricing`.

| Needed | Why | Passage required |
|---|---|---|
| Ho and Stoll (1981), *Journal of Financial Economics* 9(1) (`ho-stoll-1981`); the route reads it through `catalogue-0527`, which names no paper | `market-making-lob` requires a Ho–Stoll inventory entry; the earlier notes' *Inventory-Skew Quoting* block cannot be sourced without it | The section deriving the dealer's optimal bid and ask as functions of inventory, with the equation numbers |
| Grossman and Miller (1988), *Journal of Finance* 43(3) (`grossman-miller-1988`) | Two implications in the earlier notes are not in `crypto-cartea` | The participation-cost (entry) stage and the discussion of market structure for large orders |
| Kyle (1985), *Econometrica* 53(6) (`s6-kyle`) | To check the single-auction results at the original, and the misprint in `crypto-cartea` p. 33 | The single-auction equilibrium theorem and its proof |

### Checks and their limits

| Source | Copy used | Passages compared | Limits |
|---|---|---|---|
| `crypto-cartea` | Local scan, 2015 Cambridge printing, no text layer | pp. 20–33: every formula and statement the entries cite, read from page images, with OCR for the running text | Some signs on p. 26 are faint in the scan; the printed results agree with the clearing condition on the same page |
| `catalogue-0496` | Local scan, 1998 Wiley printing of the 1995 book | pp. 91–98, eqs. (4.1), (4.3)–(4.5), (4.16)–(4.17), (4.20), from page images and OCR | A later printing than the catalogue's 1995 record; page numbers may differ in other printings |
| `s6-stoikov` | Author-hosted journal PDF, the copy named in the catalogue's version record | pp. 217–222, eqs. (1)–(30), Table 1, text layer | The HJB and expansion steps were read, not re-derived |
| `grossman-miller-1988`, `ho-stoll-1981`, `s6-kyle` | Not available locally | None | Cited only as further reading, marked not yet read |

Every pilot entry is therefore *partly checked*, *draft* and, except Avellaneda–Stoikov, *timeless*. **Human review is outstanding** for all six entries: their wording, the interpretations they flag, and the locators, before any is marked *checked*.

## dealer-information models review: Glosten–Milgrom and the dealer material, 15 October 2026

Source checking, not study: the pathway is neither mastered nor consolidated, and its Methods readings are untouched.

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

- **A Glosten–Milgrom example from Harris, not the paper.** Its $a=V+PE$, $b=V-PE$, $a-b=2PE$, with the information and accounting views agreeing, is Harris, *Trading and Exchanges*, chap. "Bid/Ask Spreads", sec. 14.10, pp. 320–321, "a simple example based on the Glosten–Milgrom model". It is now `res:adverse-selection-spread-component`, citing `alpha-harris`. Harris misprints the dealer's profit against an informed buyer as $A-(V-E)$ (p. 321, checked on the page image); his result needs $A-(V+E)$.
- **The paper's model** (`mod:glosten-milgrom`) was checked in the 1983 discussion paper: zero-profit quotes $A_t=\mathbb{E}[V\mid S_t,Z_t>A_t]$ (p. 6), Proposition 1 ($A_t\ge\mathbb{E}_t[V]\ge B_t$, p. 8), Proposition 2 (martingale prices, p. 10), Proposition 3 (root-mean-square spread bound, p. 11), Proposition 5 (comparative statics, pp. 15–16), market shutdown (pp. 9, 12, 17) and the volume result (pp. 18–19). The closed-form two-value half-spreads are `crypto-cartea`'s simplification (pp. 34–36), kept as a separate result.
- **Two `crypto-cartea` misprints are confirmed by the authors' errata.** P. 33: Kyle's $\lambda$ should be $\sigma/(2\sigma_u)$, which settles the pilot's conflict at textbook level, in agreement with `catalogue-0496` (Kyle's paper still unread). P. 37: the bid half-spread prints $F(\Delta_a)$ for $F(\Delta_b)$.
- **Grossman–Miller (NBER 2641).** Free entry: market makers enter until $\mathbb{E}U(W_0-c+(\bar P_2-P_1)x_1^m)=\mathbb{E}U(W_0)$ (eq. (16), p. 18). With $\mathbb{E}i=0$ this gives $1/\sqrt{1+t}=e^{-ac}$ with $t=a^2\operatorname{Var}_1(\bar P_2)\operatorname{Var}(i)/(1+M)^2$ (eq. (19), pp. 18–19). The number of market makers is set by $ac$ and rises as $c$ or $a$ falls, or as either variance rises (p. 19). The earlier wording "until spread capture just covers $c$" is loose: entry balances the expected utility of the risky position, not spread capture. Large orders: a specialist can switch to "search mode" when an order exceeds what the specialist and the limit-order book can absorb, and upstairs block desks served mainly as a search market (p. 9). Both are now backlog stubs, not entries.
- **Harris supports the dealer material** almost line for line (chap. "Dealers", pp. 283–294; chap. "Bid/Ask Spreads", pp. 297–302, 312–313). He does not say that poorly informed dealers *underreact* to informed flow; he says only that they more often mistake uninformed clients for informed ones (p. 293), and the entry states only that.

### Findings on the earlier notes

| Earlier block (file) | Disposition |
|---|---|
| *Glosten-Milgrom Adverse-Selection Spread Component* proposition, *Information and Accounting Views Agree* (`03_.../05_information_based_models.tex`) | Rewritten as `res:adverse-selection-spread-component`, cited to `alpha-harris` rather than to Glosten and Milgrom |
| *Adverse Selection Through Flow* (same file) | Merged into the *Practice* of `mod:glosten-milgrom` |
| *Adverse Selection Spread Component* principle (same file) | Merged into the *Practice* of `res:adverse-selection-spread-component` |
| Two tables, *Informed-Trader Identification*, *Refusing Flow* (same file) | Merged into `meth:dealer-quote-adjustment` (steps 2 and 3, *Conditions*, *Practice*; "reduces market-wide immediacy" kept as interpretation) |
| *Poorly Informed Dealers*, *Dealers and Value Traders* (same file) | Merged into the *Practice* of `meth:dealer-quote-adjustment`; "underreact to informed flow" not supported and dropped |
| *Quote-Control Segmentation* (`05_.../02_avellaneda_stoikov_framework.tex`) | Merged into the *Statement* of `meth:dealer-quote-adjustment` (level, skew, spread, size) |
| *Two-Sided Flow* (`05_.../01_economics_of_market_making.tex`) | Merged into `meth:dealer-quote-adjustment` (the "risk warehousing" phrase as interpretation) |
| *Free Entry Bounds Dealer Spreads*, *Dealer Spread Cost Segmentation* (same file) | Merged into the *Conditions* of `res:adverse-selection-spread-component` |
| All 7 blocks of `05_.../06_cross_asset_and_cross_venue_market_making.tex` | Deferred: arbitrage as cross-instrument dealing (Harris, chap. "Arbitrageurs"), which fits neither `market-making-lob` nor `hft-market-design` |

### Checks and their limits

| Source | Copy used | Passages compared | Limits |
|---|---|---|---|
| `glosten-milgrom-1983` | Internet Archive snapshot of the Kellogg-hosted scan | pp. 1–25: setup, Propositions 1–5 and their proofs' structure, shutdown, volume and the conclusion's limitations; page images for every formula, OCR for running text | Working paper, not the 1985 journal version the catalogue names; proofs read, not re-derived |
| `crypto-cartea` | Local scan (as in the pilot) | pp. 34–37, Figure 2.3, n. 5, from page images (p. 37 at 300 dpi) | — |
| `crypto-cartea-errata` | Authors' web page, retrieved 2026-10-15 | Entries for pp. 33, 36 and 37 | Undated page |
| `alpha-harris` | Local PDF with text layer | chap. "Dealers", pp. 283–295; chap. "Bid/Ask Spreads", pp. 297–302, 312–313, 320–321; p. 321 also as a page image | Text layer, not page images, except p. 321 |
| `grossman-miller-1988-nber` | NBER PDF | pp. 4–5, 9, 18–19, 23–24; eqs. (16)–(19) from page images | Working paper, not the journal version |

The six new entries are all *partly checked 2026-10-15*, *draft* and *timeless*; **human review is outstanding** for them, as for the six pilot entries.

### For review

- All six new entries: wording, the interpretations they flag, and the locators. In particular, check whether citing Harris rather than Glosten and Milgrom for the $2\alpha e$ result is the attribution you want.
- Whether the working-paper keys (`glosten-milgrom-1983`, `grossman-miller-1988-nber`) should stay as separate sources or be replaced by the journal versions once those are read.
- The cross-asset arbitrage file (`05_.../06`): its candidate list (`market-making-lob`, `hft-market-design`) looks wrong; `execution-market-making` (Harris, chap. "Arbitrageurs") or the asset-class pathways seem closer. The list was left unchanged.

## spread and inventory models review: spread decomposition and inventory models, 15 October 2026

Source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

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
- **Roll's estimator.** The derivation matches Harris's box line for line (p. 415, page image) and Hasbrouck's half-spread version (sec. 3.4, pp. 29–30). The earlier caveat had one direction wrong: trade signs correlated with information make the autocovariance *more* negative and bias the estimate up (Hasbrouck, Exercise 4.3, pp. 38–39), while autocorrelated signs bias it down (Exercise 4.2). Harris says violations typically bias it down (p. 434). Price discreteness and hidden liquidity, also listed in the earlier notes, are not in the passages checked.
- **Effective and realised spreads.** Harris defines both as doubled signed differences from the time-of-trade and a later midpoint (pp. 424–425), and uses "realised spread" also for a dealer's round-trip outcome (p. 280); Hasbrouck's effective and realised *costs* are per side, for a buy (p. 148). The entry keeps the conventions apart and states the factor of two.
- **Inventory models.** *Inventory-Skew Quoting* ($r=m-\kappa(q-q^\star)$, constant spread) is exactly Hasbrouck's version of Stoll (1978) with the ask derived by the same indifference argument: $\kappa=s=\gamma\sigma_X^2$ (sec. 11.2, pp. 110–111; the ask is own derivation). O'Hara reports that Ho–Stoll also gives a spread independent of inventory, with both quotes shifted (sec. 2.3, pp. 35–36, page images). Hasbrouck's account of Amihud–Mendelson, where the spread widens away from the preferred position (pp. 108–109), shows the constant spread is not general. Written as `mod:inventory-based-quotes`, citing the textbooks and stating that neither original paper was consulted.
- **Inventory versus information.** The earlier caveat is supported by Hasbrouck sec. 11.4 (p. 115): the same short-run quote response, separated by permanence; NYSE specialist inventories add little to quote dynamics.
- **Spread determinants and outside spreads.** Harris chap. 14, secs. 14.4–14.6 (pp. 304–317, Table 14-2 p. 311) and chap. 16 (pp. 340–346) support the lists almost item by item. His factor is risk replication for hedgers (p. 316), not the availability of close risk substitutes.

### Findings on the earlier notes

| Earlier block (`03_.../03_bid_ask_spread_decomposition.tex` unless stated) | Disposition |
|---|---|
| *Spread Component Segmentation* | Merged into the Conditions of `res:adverse-selection-spread-component` (qualified: Harris's split is two-way) |
| *Adverse-Selection Component Equivalence* | Merged into `res:adverse-selection-spread-component`: symmetry condition in Conditions; the "twice the loss" claim corrected in Pitfalls |
| *Roll Serial-Covariance Spread Estimator*, *Roll Estimator Limits* | Rewritten as `res:roll-spread-estimator`; the informed-trading direction corrected |
| *Inventory Spread Component*, *Inventory Cost Segmentation* (`04_inventory_models.tex`) | Merged into `def:dealer-inventory-risk` (Practice; Conditions, with unsupported items named) |
| *Inventory-Skew Quoting* (`04_...`, assigned to `market-making-lob`) | Rewritten as `mod:inventory-based-quotes` from textbook accounts; Ho–Stoll paper check left as backlog stub `res:ho-stoll-dealer-pricing` |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. "Dealers" p. 280; chap. "Bid/Ask Spreads" pp. 297–318 (Figure 14-1 p. 301 also as page image); chap. "Value Traders" pp. 340–346; chap. "Volatility" pp. 413–417 (Roll box p. 415 also as page image); chap. "Liquidity and Transaction Cost Measurement" pp. 423–427, 434 | Text layer except the two page images; Table 14-2 read from the text layer |
| `s6-hasbrouck` | secs. 3.4 (pp. 29–30), 4.4–4.5 (pp. 38–39), 5.4.2 (p. 49), 5.5 (p. 53), 8.1–8.3 (pp. 67–69), chap. 11 (pp. 106–117), 14.2.2 (p. 148), 14.3.3 (pp. 150–151) | Text layer only; its equations extracted cleanly apart from lost $\Delta$ signs, restored from context |
| `catalogue-0496` | sec. 2.3, pp. 29–36 | Page images; a textbook account of Ho–Stoll, not the paper |

The six new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding** for them and for the three revised entries.

### For review

- The six new entries and the three revised ones; in particular the corrected reading of the equivalence proposition, the Roll bias directions, and whether `mod:inventory-based-quotes` should be split into a Stoll entry and a Ho–Stoll entry once the paper is read.
- The five measurement entries (`def:spread-measures`, `res:roll-spread-estimator`, `res:spread-component-identification`, `res:spread-determinants`, `def:outside-spread`) serve the section overview route `execution-market-making`, whose required readings include `s6-hasbrouck`; they are listed in the `market-making-lob` note because that route has no pathway note yet.
- The new notation override row, and the per-side versus full-spread conventions it records.

## volatility and liquidity review: volatility and liquidity, 15 October 2026

Source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF, as in dealer-information models / spread and inventory models reviews | As before |
| `s6-hasbrouck` | Local PDF, as in spread and inventory models review | As before |
| `alpha-laruelle` | Local PDF outside the repository: Lehalle and Laruelle (eds.), *Market Microstructure in Practice*, 2nd ed., World Scientific, 2018, ISBN 9789813231122, matching the catalogue record (DOI 10.1142/10739); text layer; printed page = PDF page − 27 | Copyright page read |
| `garman-klass-1980` | Not consulted; added to `front/sources.tex` from its Crossref record (DOI 10.1086/296072) as further reading | Crossref metadata only |

### Source findings

- **The spread–volatility regressions are Lehalle and Laruelle's, not Harris's.** The level and log-log regressions, the back-transformation $\psi=A_0\sigma^{a_1}e^\epsilon$ and the predictor $\hat A_0\sigma^{\hat a_1}e^{\hat\sigma_\epsilon^2/2}$ are their appendix A.10 (pp. 292–298, Rio Tinto, 15-minute intervals); the fits are weak ($R^2$ 0.24 in levels, 0.16 in logs, 0.11 for the back-transformed predictor). The identification caveat's controls are supported for tick size (p. 148: at a one-tick spread, size at the best quotes adjusts instead), time of day (pp. 145–148) and trade intensity (pp. 144–145, $\psi_i=a+b\sigma_i/\sqrt{N_i}$); venue and depth as regression controls are not in the passages checked. Their "unbiased predictor" is exact only with known parameters (own note).
- **Overlap with `res:spread-determinants`.** The regressions became a method entry, `meth:spread-volatility-regression`, since they estimate a determinant rather than state one; the determinants entry gained Lehalle and Laruelle's empirical relation and a cross-reference. The principle *Volatility Is a Liquidity Price* was merged into it: wider spreads and, in crashes, withdrawal are supported (Harris pp. 561, 563); smaller displayed size and faster cancellations as responses to volatility are not, and are named in its Pitfalls.
- **Garman–Klass.** Lehalle and Laruelle print $\sqrt{\tfrac12(\text{high}-\text{low})^2-(2\log2-1)(\text{close}-\text{open})^2}$ divided by the average price (p. 172, page image; the text layer drops the $\tfrac12$); the earlier notes used log ratios. The two agree to first order. The 1980 paper was not consulted.
- **Overlap with `res:roll-spread-estimator`.** *Volatility Component Decomposition* ($P_t=M_t+u_t$) is Hasbrouck's random-walk decomposition (sec. 8.6, pp. 72–74): only the random-walk variance is identified, the pricing-error variance has only a lower bound. *Transitory Volatility and Reversal* and *Volatility Source Segmentation* are Harris chap. 20 (pp. 410–416). These went into a new definition, `def:volatility-components`, with Roll's model as its special case; the Roll entry gained a cross-reference only. Negative serial covariance is a strong indicator (Harris p. 414) but neither necessary nor sufficient: perishable spot prices (box p. 413) and lagged adjustment (Hasbrouck Exercise 8.2, p. 74). The earlier notes listed *episodic* and *continuing* volatility as sources: Harris's episodic volatility (p. 410) describes episodes, not a source of volatility; "continuing" volatility as a source was not found.
- **Bubbles and crashes** follow Harris chap. 28 almost item by item (pp. 555–563, 570–571): the five-phase dynamics, the price accelerator box (p. 556, after Treynor's unpublished manuscript, not consulted) and the "market failures or corrections" box (p. 559). *Regulating Volatility* is Harris pp. 410 and 575–577 (circuit breakers' net effect on transitory volatility indeterminate).
- **Flash crash.** The material follows Lehalle and Laruelle chap. 2, sec. 2.5 (pp. 169–183) and app. A.5 (pp. 261–266, page images). Two findings: (1) in the book $\rho$ is the proportion of traders playing the hot-potato game, while the large seller follows volume (p. 264), so $\rho$ is not the fraction of traders following volume; (2) the book's solution (A.14), $I_t^-=I_0\exp\bigl(\tfrac{t^2}{1-\rho}\tfrac{r_0}{2}-\tfrac12\sigma_I^2t+\sigma_IW_t^-\bigr)$, does not follow from its own approximation $R_t\simeq tr_0/(1-\rho)$, which gives an exponent linear in $t$ (own derivation, to be rechecked). Sec. 2.5.3 (pp. 187–189), on circuit breakers, was not read.

### Findings on the earlier notes

| Earlier block (`03_.../08_volatility_and_liquidity_interaction.tex`) | Disposition |
|---|---|
| *Volatility Is a Liquidity Price* | Merged into `res:spread-determinants` (Practice; unsupported responses named in Pitfalls) |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. 20 "Volatility", pp. 410–417; chap. 28 "Bubbles, Crashes, and Circuit Breakers", pp. 555–563, 570–578 | Text layer only |
| `s6-hasbrouck` | secs. 8.3 (p. 69), 8.4–8.7 (pp. 69–75) | Text layer; $\Delta$ signs restored from context |
| `alpha-laruelle` | chap. 2, secs. 2.2 (pp. 143–148), 2.3.1 (pp. 150–151), 2.5–2.5.2 (pp. 169–184); app. A.5 (pp. 261–266), A.10 (pp. 292–298) | Text layer; page images for p. 172 and pp. 262–266 |

The four new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding** for them and for the two revised ones.

### For review

- The four new entries and the two revised ones; in particular the decision to make the regressions a method entry rather than part of `res:spread-determinants`, and the own-derivation notes (the predictor's unbiasedness, the variance split's covariance term).
- The (A.14) exponent in Lehalle and Laruelle's toy model.
- As in spread and inventory models review, the new entries serve the overview route `execution-market-making` and are listed in the `market-making-lob` note only because that route has no note.

## information and price discovery review: information, market efficiency and price discovery, 15 October 2026

Source checking, not study: no pathway is mastered or consolidated, and no reading was studied. The volatility and liquidity review overlap list was judged from titles; each candidate overlap below was settled by comparing definitions and claims.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `alpha-harris` | Local PDF, as in dealer-information models / volatility and liquidity reviews (printed page = PDF page − 13) | As before |
| `s6-hasbrouck` | Local PDF, as in spread and inventory models / volatility and liquidity reviews (printed page = PDF page − 11) | As before |
| `alpha-laruelle` | Local PDF, as in volatility and liquidity review (printed page = PDF page − 27, Introduction included) | As before |

### Source findings

- **Fundamental value is not the efficient price.** Harris's fundamental value is the value everyone would agree on if all knew everything known about the instrument (chap. 10, pp. 222–223). Hasbrouck's fundamental value or efficient price conditions on all *public* information (sec. 3.2, p. 26). So Harris's noise $P_t-V_t$ is not the pricing error $s_t$ of `def:volatility-components`, and *Fundamental Value and Price Noise* became its own entry, `def:fundamental-value`, with the contrast in its Pitfalls. The earlier notes' "all payoff-relevant information" reads as the perfect-foresight value, which Harris distinguishes from it.
- **Forecast aggregation** is Harris's algebraic box (p. 225). There the average price follows from linear demands with a common slope and zero net supply. The earlier proof's $\sigma^2/N$ needs a common variance that Harris does not assume (own step). Harris's claim that the market error is below the average individual error "if the individual forecast errors are not identical" holds for squared errors, not absolute ones (own check). The correlated-error caveat is own working, $\operatorname{Var}(e_M)=\sigma^2[
ho+(1-
ho)/N]$, consistent with Harris on correlated estimates (p. 237).
- **Market efficiency** is Harris sec. 10.6.6 (p. 240). His weak form uses past prices; volumes are in the semistrong set, not the weak-form set as the earlier notes had it. His cost-sensitive definition is unnamed; the earlier notes called it "economic". The information–liquidity trade-off is sec. 10.6.7 (p. 241). Publishing information is Harris's counterexample (sec. 10.6.8), added to the entry.
- **Insider information** is Harris chap. 29 (pp. 584–592), with the SEC's 2002 summary quoted in a box on p. 585. "Temporary insider", a personal-benefit tipping test, auditors, consultants and exchange staff are not in the passages. For *Signal Tradability Requires Permission*, confidentiality duties, employer pre-approval (p. 588) and liquidity (p. 236) are supported; restricted lists, signal compliance approval and data provenance are not. The legal details (reporting deadlines, prearranged plans, penalties) are dated 2002 and were left out of the entry.
- **Value traders.** *Value-Trader Profit Source Segmentation* listed three sources; Harris has two (chap. 16, pp. 338–339). New information profits news traders, and value traders gain there only by correcting news traders' errors (chap. 10, Table 10-1, p. 230; p. 239). Dealer inventory pressure is the indirect channel of uninformed demand (pp. 339–340). The no-trade band proposition is own working: a symmetric special case of the outside spread with one all-in half-cost. It was merged into `def:outside-spread` as an Interpretation, with the reason it understates Harris's widening factors. *No-Trade Is an Information Position* is Harris's box on p. 343.
- **Price formation process** is Lehalle and Laruelle's term. Its two phases, immediate impact and decay or resilience, are on pp. 27–29 (Figure 8, not inspected). The temporary-or-permanent impact depending on consensus is on pp. 3 and 28, and the design tension over information on pp. 19–20.
- **Returns by time scale.** *Volatility Scale Segmentation*, *Intraday and Overnight Returns*, *Correlation Interpretation* and *Microstructure to Macro Prices* follow Lehalle and Laruelle sec. 2.5 (p. 169) and sec. 2.5.1 (eqs. (2.2)–(2.3), pp. 174–177). They do not overlap `def:volatility-components` (fundamental against transitory) or `meth:garman-klass-volatility` (an estimator within intervals): they split time scales. So they became `def:intraday-overnight-returns`, with cross-references. The source finds correlation spikes mainly overnight; the earlier "different mechanisms at different horizons" was corrected. News revaluation overnight and benchmark paths are not in the passages. The authors' HFT explanation of the 2010 rise is flagged as a conjecture.
- **Outage.** Lehalle and Laruelle date the Euronext halt to 13 October 2010 in the text but caption Figures 2.31–2.32 "October 10, 2010", a Sunday. The captions are probably wrong (own check of the calendar).
- **Not reopened.** The volatility and liquidity review question on the toy model's eq. (A.14) does not bear on this material and stays open. Sec. 2.5.3 (pp. 187–189) was not read; nothing here depends on it.

### Findings on the earlier notes

| Earlier block | Disposition |
|---|---|
| `01_...`: *Signal Tradability Requires Permission* | Merged into the Practice and Pitfalls of `def:inside-information` (unsupported parts named) |
| `02_...`: *Value-Trader Profit Source Segmentation* | Merged into `def:outside-spread` (Conditions; correction in Pitfalls) |
| `02_...`: *Value Traders Supply Liquidity Outside the No-Trade Band* | Merged into the Statement of `def:outside-spread` (Interpretation) |

- Lehalle and Laruelle frame the Euronext outage as a fragmentation mechanism (introduction, pp. 5–7; sec. 2.5.2, pp. 183–186); the shock-propagation channels follow sec. 2.5.2, p. 183. The fast-liquidity material is their app. A.2 (pp. 250–251), a summary of Foucault, Kadan and Kandel (2009), not read; its later identification is in the dealer models and information review's *Source identification*.
- The insider-information material rests on Harris's economic definition and U.S. summary; its legal content is dated 2002.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. 10 "Informed Traders and Market Efficiency", pp. 222–244; chap. 16 "Value Traders", pp. 338–346; chap. 29 "Insider Trading", pp. 584–598 | Text layer only; the SEC web page quoted on p. 585 not consulted |
| `s6-hasbrouck` | sec. 3.2, pp. 24–27 | Text layer |
| `alpha-laruelle` | Introduction, pp. 3–7, 19–20, 27–29; chap. 2, secs. 2.5–2.5.2, pp. 169–177 and 183–186; app. A.2, pp. 250–251 (routing only) | Text layer; no page images (equations (2.2)–(2.3) read cleanly); Figure 8 not inspected |

The six new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the revised `def:outside-spread`. No original paper was consulted: Grossman and Stiglitz (1980), Bouchaud et al. (2002) and Foucault, Kadan and Kandel (2009) are named only as the textbooks' sources.

### For review

- The six new entries and the revised outside spread, in particular:
  - the decision to keep Harris's fundamental value apart from Hasbrouck's efficient price;
  - the own-derivation notes: the variance of the average, correlated errors, squared and absolute errors, the no-trade band, and the return identity;
  - the insider entry's scope: economic definition plus dated U.S. summary, with no current law.
- The routing above: the three assignments of `02_...` and the reassignment of *Systemic Risk Link*.
- The new overview note and the nine entries moved into it.
- `03_.../06_strategic_trading_models.tex` repeats the topic review material (informed-trader styles, trading speed, insider-trading profitability and deterrence): consolidate it into these entries next.

## strategic trading review: strategic trading models, 15 October 2026

Source checking, not study: no pathway is mastered or consolidated, and no reading was studied.

### Sources and availability, 2026-10-15

`alpha-harris`, the local PDF used in dealer-information models / information and price discovery reviews (printed page = PDF page − 13); text layer for all passages; page images of p. 225 (the aggregation box) and p. 270 (the bluffing example). No other source was needed.

### Source findings and corrections

- **Styles and speed** (chap. 10, pp. 226–235): Harris restricts information-oriented technical traders to informed traders' errors, not all "predictable errors by other traders"; trading on uninformed traders' predictable impact is order anticipation (p. 231).
- **Arbitrage** (chap. 17, pp. 347–379):
  - *Types:* Harris has two arbitrage types, pure and speculative. "Risk arbitrage" is a synonym for speculative arbitrage, usually meaning merger arbitrage, and statistical arbitrage is one kind of speculative arbitrage (pp. 350, 360). The earlier list had four parallel types.
  - *Cross-rate arbitrage* is a cyclic conversion arbitrage (p. 356), not a fourth pure mechanism.
  - *Risks:* Harris names four risks; the earlier "staying power" and "specific-factor" risks are consequences and sources of basis and carrying-cost risk.
  - *Terms:* basis, fair value, arbitrage spread and arbitrage bounds are Harris's own (p. 349); the earlier notation $A_t=B_t-B_t^\star$ matches.
- **Order anticipation** (chap. 11, pp. 245–258; chap. 24, pp. 498–508): quote matching is front running of passive traders, not a parallel category, and gunning the market is a manipulation of stop orders (sec. 11.4). Front running informed traders raises informativeness in the short run but lowers it in the long run (pp. 250–251), which the earlier notes omitted.
- **Bluffing** (chap. 12, pp. 259–275): Harris has two bluffer types; wash trading is a price manipulator's technique, not a third type. The asymmetric-impact condition and Harris's worked example were added from pp. 270–273, and the example was rechecked.
- **Winner's curse** (chap. 16, pp. 341–343): supported. The earlier "information overlap" severity factor is not in the passages.
- **Insider trading** (chap. 29, pp. 588–595): the deterrence rule (expected benefit against probability times penalty, p. 590) is Harris's. The extended form $G\le K+R+qF$ adds $K$ and $R$ as own working. Penalty figures are 2002 U.S. law, labelled as dated.

### Mathematical checks (own, recorded as Interpretation in the entries)

- **Aggregation, reused and changed.** The estimator is $P=\sum_ia_if_i/\sum_ia_i$ from linear demands and zero net supply. It is unbiased when each $f_i$ is conditionally unbiased. With independent errors its variance is $\sum_ia_i^2\sigma_i^2/(\sum_ia_i)^2$, minimised by inverse-variance weights at $(\sum_i\sigma_i^{-2})^{-1}$. The equicorrelated variance $\sigma^2[\rho+(1-\rho)/N]$ was rederived from $\tfrac1{N^2}[N\sigma^2+N(N-1)\rho\sigma^2]$. It requires $\rho\ge-1/(N-1)$, and the limit $\rho\sigma^2$ assumes $\rho\ge0$.
- **Harris's comparison, rechecked against the page image of p. 225.** information and price discovery review's statement ("holds for squared errors, not absolute") was true only realisation by realisation, so it was restated by loss measure:
  - *Signed errors* average exactly.
  - *Squared errors* are strictly smaller unless all errors are equal, by the identity $\tfrac1N\sum e_i^2-e_M^2=\tfrac1N\sum(e_i-e_M)^2$.
  - *Absolute errors*, by the triangle inequality, are equal whenever the errors share a sign (counterexample $e=(1,2)$).
  - *In expectation*, with independent, zero-mean, nondegenerate errors, both are strict.
  - *"Better than any individual trader"* holds in expected squared error only with equal accuracies. The counterexample: variances 0.01 and 1 give 0.2525 for the equal-weighted average.
- **Winner's curse.** A break-even bid $b^\star=\widehat V-\omega_N-c$ needs $\omega$ conditioned on one's own estimate and on winning *at that bid*. It is then a fixed point, $b=\widehat V-\omega(b)-c$, and it is the highest acceptable bid, not the optimal one.
- **Deterrence.** If the penalty is only disgorgement ($F=G$), the condition becomes $(1-q)G\le K+R$. $R$ is a cost only under risk aversion.
- **Arbitrage band.** $|A_t|>K_t+R_t$ assumes full convergence; with partial or slow convergence the gain is the expected narrowing net of extra carry.
- **Bluffing example.** Recomputed: \$1.5 million profit with asymmetric impact, a \$3 million loss with symmetric impact, and a \$0.4 million loss in 100-contract trades, all as printed (pp. 270–271).

### Findings on the earlier notes

| Earlier block (`03_.../06_strategic_trading_models.tex`) | Disposition |
|---|---|
| *Informed Trading Paradox* | Merged into `def:market-efficiency` (Conditions already held it; wording noted in Pitfalls) |
| *Skilled Speculation vs Inside Information* | Merged into `def:inside-information` (Statement; unsupported examples in Pitfalls) |
| *Arbitrage Opportunity*, *Basis and Arbitrage Spread*, *No-Trade Band for Basis Arbitrage* | Rewritten as `def:arbitrage` (the band as Interpretation) |
| *Arbitrage Characterisation Segmentation*, *Arbitrage Type Segmentation*, *Pure Arbitrage Mechanism Segmentation* | Merged into the Conditions of `def:arbitrage` (types corrected) |
| *Winner's Curse*, *Winner's-Curse Bid Adjustment* | Rewritten as `def:winners-curse` (the bid as a fixed point) |

- Harris presents the specialists' quote matching and stop-order tactics as the order-anticipation strategies of chap. 11 (pp. 502–503); the specialist material is dated 2002.
- Informed-trader styles follow Harris sec. 10.5 and Table 10-3, and the precision–orthogonality trade-off p. 237; the earlier "inactive" speed is stale information, not a speed.
- The informed-trading paradox is Harris's market paradox; only a wording difference was recorded.
- Skilled speculation against inside information is Harris's box (p. 590); the earlier alternative-data and channel-check examples are unsupported.
- Harris treats stop gunning as manipulation inside the order-anticipation chapter.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chap. 10, pp. 222–244 (box p. 225 by page image); chap. 11, pp. 245–258; chap. 12, pp. 259–275 (p. 270 by page image); chap. 16, pp. 338–346; chap. 17, pp. 347–379; chap. 24, pp. 494–508; chap. 29, pp. 584–598 | Text layer except the two page images; the SEC web page and the cases Harris cites were not consulted |

The seven new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the four revised entries.

### For review

- The seven new entries and four revised ones. In particular:
  - the restated error comparison and the counterexample in `res:informed-trading-aggregation`;
  - the fixed-point form of the winner's-curse bid;
  - the merge of the specialist strategies into order anticipation rather than an assignment to `market-structure-execution-quality`.
- `03_.../07_liquidity_and_market_impact.tex` repeats the topic review bluffing material (*Round-Trip Manipulation Profit Test*, *Impact Symmetry Disciplines Bluffing*).

## liquidity and impact review: liquidity and market impact, 15 October 2026

Source checking, not study.

### Sources and availability, 2026-10-15

| Source | Copy used | Identity checked |
|---|---|---|
| `wide-webster-price-impact` | Local PDF outside the repository: Webster, *Handbook of Price Impact Modeling*, CRC, first edition 2023; printed page = PDF page − 17 | Copyright page: DOI 10.1201/9781003316923, matching the catalogue |
| `catalogue-0528` | Local PDF outside the repository: Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices*, Cambridge 2018; printed page = PDF page − 19 | Copyright page: ISBN 9781107156050, DOI 10.1017/9781316659335; the catalogue record does not establish an edition |
| `alpha-harris` | As in dealer-information models / strategic trading reviews | pp. 271–273 reread |

### Source findings

- **The impact material is not Harris's, except impact symmetry.**
  - *Lens taxonomy:* a simplification of Webster's four communities (chap. 1, sec. 1.1.5, pp. 9–15).
  - *Temporary/permanent impact and identification:* follow Bouchaud et al. chaps. 11–12 (pp. 208–212, 240).
  - *Propagator:* their chap. 13 (pp. 249–253).
  - *Round-trip test:* the accounting behind Gatheral's definition of manipulation (Webster n. 3, p. 7).
  - *Impact symmetry:* Harris chap. 12 (pp. 271–273).
- **"Temporary impact" is ambiguous.** Almgren and Chriss use it for the instantaneous transaction cost (Webster n. 3, p. 53), not for a displacement that decays. The earlier definition mixed the two.
- **Permanent impact.** Correlated metaorders can mimic permanent impact, and permanent impact mixes reaction with prediction (Bouchaud et al. p. 240). Controls for market and sector moves are not in the passages; the book suggests conditioning on the rest of the market's order-sign imbalance (p. 212).
- **Decay profiles.** Trade-dependent decay profiles belong to the generalised models of chap. 14, which was not read; the simple propagator has one kernel.
- **Conditioning in eq. (11.2).** As printed, observed impact conditions on execution only; the identity (11.4) needs $\mathcal F_t$ throughout, which the authors say is implicit (p. 210).

### Mathematical checks (own, Interpretation in the entries)

- **Round trip.**
  - *Identity:* with average execution prices that include impact, zero initial and terminal inventory, and explicit costs $F$, profit is $Q(\bar P_S-\bar P_B)-F$.
  - *Undefined $c$:* the earlier notes did not define $c$ per side or per round trip; per side, $F=2Qc$.
  - *No double counting:* spread already in $\bar P$ must not be counted again in $c$.
  - *Realised against expected:* a realised profit is not manipulation, which concerns *expected* profit under a model with no information.
- **Webster's Example 2.7.1** (page image p. 94), rederived. Buying $\Delta$ at $t$ costs $(S_t+\tfrac12\lambda_t\Delta)\Delta$. Selling at $t'$ yields $(S_{t'}+e^{-\int\beta}\lambda_t\Delta-\tfrac12\lambda_{t'}\Delta)\Delta$. The profit is $(S_{t'}-S_t)\Delta+\tfrac12\lambda_t\Delta^2(2e^{-\int\beta}-1-e^{\int\gamma'})=(S_{t'}-S_t)\Delta-\tfrac12\lambda_t(2\beta+\gamma')h\Delta^2+o(h)$, as printed. With constant liquidity ($\gamma'=0$, $\beta>0$) the impact term is a cost. So a model that treats buys and sells alike can still admit manipulation through time-varying liquidity, and impact symmetry is not a general no-manipulation proof.
- **Volume bound.** $v'/v<4\beta$ gives a doubling time above $\ln2/(4\beta)$, a quarter of the half-life $\ln2/\beta$, as Webster states.

### Findings on the earlier notes

| Earlier block (`03_.../07_liquidity_and_market_impact.tex`) | Disposition |
|---|---|
| *Market Impact Lens Segmentation* | Merged into the Practice and Pitfalls of `def:price-impact` (corrected to Webster's four communities) |
| *Temporary and Permanent Impact* | Rewritten as `def:price-impact` (with the temporary-impact ambiguity) |
| *Round-Trip Manipulation Profit Test* | Rewritten as `res:no-price-manipulation` (the identity as Interpretation; Webster's example and Bouchaud et al.'s closed-trajectory result as the substance) |
| *Impact Symmetry Disciplines Bluffing* | Merged into the Practice of `def:bluffing-manipulation`, qualified, with a pointer to `res:no-price-manipulation` |

- The generalised Roll model is recorded as the constant-propagator special case (Interpretation).
- Price manipulation in an impact model is a round trip with negative expected cost through one's own impact, with nobody fooled (Gatheral's definition, via Webster); Harris's bluffing works through other traders' inferences.
- Impact symmetry as a discipline on bluffing is Harris's rule (pp. 271–273); the earlier "risk" is not in Harris, and the no-profit conclusion holds only in his immediate, permanent-impact example.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `wide-webster-price-impact` | chap. 1, pp. 3–15; chap. 2, pp. 53–54 and 93–97 | Text layer; page image of p. 94; Figure 2.5 and exercise 4 not inspected |
| `catalogue-0528` | chap. 11, pp. 208–212; chap. 12, pp. 240–241; chap. 13, pp. 249–253; chap. 19, pp. 361–362 | Text layer; page images of pp. 211, 252 and 362; chap. 14 and eq. (19.7) not read |
| `alpha-harris` | chap. 12, pp. 270–273 | Text layer and the strategic trading review page image of p. 270 |

No original paper was consulted: Gatheral (2010), Fruth, Schöneborn and Urusov (2013), Bouchaud, Gefen, Potters and Wyart (2004) and Almgren and Chriss (2001) appear only through the two books.

### For review

- The three new entries and the revised bluffing entry. In particular:
  - the new canonical chapter and the routing to `price-impact-execution`;
  - the separation of strategic bluffing from mechanical manipulation;
  - the "temporary impact" terminology note.
- Whether `catalogue-0528`, on no route, should be the main empirical source for these entries until the pathway's own readings are studied.

## market-impact models review: market impact models, 15 October 2026

**Baseline counts.** The reported counts were confirmed except one. The status script listed 23 entries for `execution-market-making`, not 22, because liquidity and impact review had named `res:no-price-manipulation` under that note's Entries heading. The sentence was reworded, and the count is 22 again.

Source checking, not study.

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
- **Propagator.** The earlier notes departed from the sources in four ways: they called $m_k$ the mid-price *after* trade $k$ while summing over $k'<k$, which in the sources is the price *before* the trade; they used a single noise $\eta_k$ instead of the cumulative sum, which would make the price stationary apart from trading (Interpretation); they dropped the original's $\ln V$ volume weight (eq. (12), p. 14 of the arXiv version), which the book's simple model also omits; and they said the response is estimated with the kernel, whereas response and sign correlation are measured and the kernel is estimated from them.
- **Sign memory.** Bouchaud et al. (book) find order splitting the primary cause and herding not relevant on the relevant time scale (p. 198). The earlier notes attributed it to splitting *and* similar agents trading together.
- **Square-root law.** The earlier line omitted the volatility scale, the condition $Q\ll V_T$ and the exponent range 0.4–0.7 (book, eq. (12.6), p. 234).
- **Kernel taxonomy.** Non-parametric and power-law kernels are supported (pp. 254–257); exponential follows from the Obizhaeva–Wang model (Interpretation, from Webster). Agent-specific kernels are not in the passages checked.
- **Debiasing.** Bacry et al. could not classify trades as informed or liquidity-driven (broker data). That design is Waelbroeck and Gomes's, reported by them, and they remove only reference-index moves, not sector or factor moves. In their reading, the systematic component is aggregated information, not just a market move to exclude.

### Mathematical checks (own, Interpretation in the entries)

- **Units and signs:** Almgren–Chriss's linear forms $g=\gamma v$, $h=\epsilon\,\mathrm{sgn}(n)+(\eta/\tau)n$, with the units printed (eqs. (6)–(7)).
- **Book eq. (12.6):** dimensionally consistent, both sides in percent of price, as the authors state.
- **Bacry et al.'s eq. (21):** cumulates to $W_d-W_{D-1}$ plus the systematic part from $D-1$. Their beta is estimated over $D-20$ to $D+20$, so it is in-sample and can absorb the event. Removing the systematic part also removes any impact of the aggregate flow on the index. The debiasing inherits the error of the square-root model for later flow.
- **Kept distinct.** Permanent impact (a limit) against impact at a finite post-execution horizon (Bacry et al.'s 20 days). Observed against reaction and prediction impact. The simple common kernel against the extensions (volume weight, event types). No no-manipulation claim was made or changed in the topic review.

### Findings on the earlier notes

| Earlier block (`04_.../05_market_impact_models.tex`) | Disposition |
|---|---|
| *Model Family Segmentation* | Merged into the Practice of `def:price-impact` (Almgren–Chriss from the original; linear; propagator and square-root linked); the square-root item rewritten as `ev:square-root-impact` |
| *Permanent-Impact View Segmentation* | Merged into the Conditions of `def:price-impact` (Bacry et al.'s views) |
| *Propagator Midprice Dynamics* | Merged into `mod:propagator` (the 2004 original; departures corrected in Pitfalls) |
| *Trade-Sign Memory and Kernel Decay* | Merged into the Conditions of `mod:propagator` (splitting, not herding; the fine balance) |
| *Price Response Curve* | Merged into `mod:propagator` (definition already there; estimation direction corrected) |
| *Propagator Kernel Segmentation* | Merged into the Practice of `mod:propagator` (agent-specific kernels flagged unsupported) |

- The three debiasing blocks describe one procedure, Bacry et al.'s sec. 7.2. The model families were checked against the Almgren–Chriss original, and Bacry et al.'s mechanical and informational views against the book's split of permanent impact into prediction and reaction.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-almgren` | secs. 1.2–1.5 and 2, pp. 7–13 (preprint) | Text layer; page images of pp. 9 and 11 |
| `wide-bouchaud-propagator` | secs. 3.1–3.2, pp. 14–17 (arXiv v2) | Text layer; page image of p. 14 |
| `wide-bacry-life-cycle` | abstract; sec. 2.2, pp. 3–4; secs. 7–8, pp. 19–22 (arXiv) | Text layer; page image of p. 21 |
| `catalogue-0528` | chap. 10, p. 198; chap. 12, pp. 233–236 and 241; chap. 13, pp. 254–257 | Text layer; page image of p. 234; chap. 14 seen only in the contents |

The two new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the two revised ones.

### For review

- The two new entries and the revised `def:price-impact` and `mod:propagator`.
- Reliance on preprint versions of the three required readings.
- The three meanings of "temporary impact".
- The interpretation notes on Bacry et al.'s in-sample beta.

## impact estimation review: price impact estimation, 15 October 2026

Source checking, not study.

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
- **The regression** is Harris's box (p. 435, page image), the Glosten–Harris model with only size-proportional permanent impact. Hasbrouck's statement of the model has also a size-independent permanent term, $\lambda_0$ (eq. (9.26), p. 91, page image); the earlier form sets $\lambda_0=0$. Harris's sentence that regression "ensures" an error uncorrelated with the regressors confuses residual orthogonality with exogeneity (Interpretation).
- **The identification caveat's controls.** Partly supported:
  - *Index return:* Hasbrouck p. 87.
  - *Volume time:* Almgren et al.
  - *Volatility and spread:* Bacry et al.

  Controls alone do not make coefficients causal (Interpretation).
- **Index reconstitution.** Harris's box (p. 487, page image) reports the 15% and 5% figures from Madhavan (2002), not consulted. Changed ownership, attention or information are not Harris's explanations of the residual; his are liquidity value, momentum, or later reversal.
- **"Permanent" is horizon-dependent.** Almgren et al.: half an hour after the last fill. Lehalle and Laruelle: one day. Bacry et al.: a 20-day profile. Each entry states its horizon.
- **Bacry et al.'s in-sample beta.** Lehalle and Laruelle's restatement keeps the same window and least-squares beta. The question stays open; a same-author restatement is not independent evidence.

### Mathematical checks (own, Interpretation in the entries)

- Differencing Hasbrouck's eq. (9.26) gives $\Delta p_t=\lambda_0q_t+\lambda_1q_tV_t+c_0\Delta q_t+c_1\Delta(q_tV_t)+u_t$; Harris's form follows with $\lambda_0=0$.
- Almgren et al.'s Table 3 recomputed from the fitted coefficients: IBM $I=19.9$ bp, $J=32.2$, $24.6$, $18.4$ bp; DRI $I=21.7$ bp, $J=42.9$, $32.0$, $23.1$ bp. These match the printed 20, 32, 25, 18 and 22, 43, 32, 23 bp to rounding.
- The duration reconciliation above, from Bacry et al.'s Table 2.

### Findings on the earlier notes

| Earlier block (`04_.../04_price_impact_estimation.tex`) | Disposition |
|---|---|
| *Impact Driver Segmentation* | Merged into the Practice and Pitfalls of `ev:intraday-impact-profile` (unsupported drivers named) |
| *Participation-Duration Shape* | Rewritten as `ev:intraday-impact-profile` (eq. (3.1); Bacry et al.'s comparison; Almgren et al. in `meth:almgren-impact-estimation`) |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | chap. 3, secs. 3.2–3.2.2, pp. 203–215 | Text layer; page image of p. 208 |
| `alpha-harris` | chap. 21, box p. 435; chap. 23, box p. 487 | Page images of both |
| `s6-hasbrouck` | secs. 9.6–9.8.1, pp. 87–92 | Text layer; page image of p. 91 |
| `wide-almgren-direct-impact` | preprint pp. 1–22 | Text layer; page images of pp. 19 and 21 |
| `wide-bacry-life-cycle` | arXiv sec. 3, pp. 5–8 | Text layer; page image of p. 8 |

The four new entries are *partly checked 2026-10-15*, *draft*. **Human review is outstanding** for them and for the three revised ones.

### For review

- The four new entries and the three revised ones.
- The decision to give Almgren et al.'s design its own method entry.
- The $\lambda_0$ correction to the Glosten–Harris form.
- The duration reconciliation.
- The reliance on preprints (Almgren et al. 2005, Bacry et al. 2014) and on Harris's report of Madhavan.

## optimal execution review: optimal execution problem, 15 October 2026

Source checking, not study.

### Sources and model identity, 2026-10-15

- **The notation** ($v^\star$, $\kappa\sigma_n(v_n/V_n)^\gamma$, $v_n^{\exp}$) is Lehalle and Laruelle's app. A, sec. A.7 (pp. 273–281). They call it a "simplified and commented version of the original Almgren–Chriss paper". It is distinct from Almgren–Chriss's linear model and from Almgren et al. (2005), whose empirical procedure is `meth:almgren-impact-estimation`.
- **Almgren and Chriss** were checked in the authors' preprint of December 2000, the copy obtained in market-impact models review. The passages used in market-impact models review (pp. 8–11) were reused; additional passages were read for the topic review (sec. 1.1, p. 7; eqs. (4)–(5), p. 10; secs. 2–2.3, pp. 11–15, with a page image of p. 14). The 2001 journal version was not compared.
- **Harris** chap. 15, pp. 322–327, for block trades.
- The Cartea–Jaimungal framework in A.7.3 was read but not used, since no entry draws on it.

### Mathematical checks (own, Interpretation in the entry)

**Units and conventions.** The concession $\kappa\sigma_n(v_n/V_n)^\gamma$ is currency per share, with $\sigma_n$ in currency per slice (p. 275). The execution-slice cost is $v_n$ times it, and the order's expected impact cost is $\kappa\sum\sigma_nv_n^{\gamma+1}/V_n^\gamma$, a total, not a rate. It is a temporary cost on that execution slice's own fills, not a transient displacement. There is no permanent-impact term and no spread or fee term, unlike Almgren–Chriss's $g$ and $\epsilon$.

**Expectation-only schedule.** (A.22) rederived: marginal impact costs are equalised across slices. A numerical check (random $V_n$, $\sigma_n$, $\gamma=0.6$) found no feasible perturbation that lowers expected cost. The source's Lagrange condition omits $\kappa$, which is harmless because $\kappa$ is absorbed into the multiplier.

**Timing.** Lehalle and Laruelle's (A.16) prices slice $n$ after shock $n$, and (A.24) sums over the quantity remaining from slice $n$ on. Their terminal conditions $x_0=v^\star$, $x_N=0$ belong to the other convention. Under the Almgren–Chriss convention (slice $n$ at $S_n$, then $S_{n+1}=S_n+\sigma_n\xi_{n+1}$), the risk term $\lambda\sum x_n^2\sigma_n^2$ with $x_0=v^\star$, $x_N=0$ is consistent.

**Recurrence and closed form.** (A.28) rederived from the first-order conditions. For $\gamma=1$ and constant parameters, the solution in the Almgren–Chriss convention equals the Almgren–Chriss $\sinh$ trajectory with $\cosh k=1+\lambda\sigma V/(2\kappa)$, numerically to $10^{-12}$. The mapping is $\kappa\sigma_n/V_n\leftrightarrow\eta/\tau$ and $\sigma_n^2\leftrightarrow\sigma^2\tau$, without the $\tilde\eta$ correction. Proposition 5 is mislabelled "variance minimization" in the source.

**Comparative statics.** The minimiser depends only on $\lambda/\kappa$. Larger $\kappa$ moves the schedule towards the expectation-only one; higher impact sensitivity does not back-load it. In the varying-parameter cases checked it never went beyond the expectation-only schedule; that is numerical evidence, not a proof.

**Shape.** The mean–variance path is convex for constant parameters (the $\sinh$ form). With time-varying $V_n$ and $\sigma_n$ all 200 random cases checked were non-convex, so a convex remaining-quantity path holds only under constant parameters.

**Variance-only schedule.** Zero variance in Almgren–Chriss is an artefact of the discretisation, as they say (p. 12).

**Parameters against estimates.** The model's $\kappa,\gamma$ are inputs estimated daily or weekly (p. 274). Almgren et al.'s exponent 0.6 measures a related quantity at a 30-minute post-trade horizon; the two are linked only by a cross-reference.

### Findings on the earlier notes

| Earlier block | Entry | Disposition |
|---|---|---|
| *Discrete Execution Schedule* | `mod:almgren-chriss-execution` (Notation; timing in Pitfalls) | Merged |
| *Temporary Impact Cost* | `mod:almgren-chriss-execution` (Notation and Conditions; temporary-impact concept in `def:price-impact`) | Merged |
| *Expectation-Minimising Schedule* | `mod:almgren-chriss-execution` (Conditions) | Merged (a result, not a definition) |
| *Mean-Variance Execution Objective* | `mod:almgren-chriss-execution` (Statement and Conditions; comparative static corrected) | Rewritten |
| *Execution Schedule Segmentation* | `mod:almgren-chriss-execution` (Practice; convexity corrected) | Merged |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | app. A, sec. A.7, pp. 273–284 | Text layer; Figure A.11 seen only in the text layer |
| `alpha-almgren` | author preprint (Dec. 2000), pp. 7–15 | Text layer; page images of pp. 9, 11 and 14; the journal version not compared |
| `alpha-harris` | chap. 15, pp. 322–327 | Text layer |

The two new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The two new entries.
- Ownership by the overview rather than `price-impact-execution`.
- The timing-convention resolution and the corrected comparative static and convexity claims.
- Reliance on the Almgren–Chriss preprint.

## execution benchmarks review: execution benchmarks, 15 October 2026

Source checking, not study.

### Sources, 2026-10-15

- **Lehalle and Laruelle**, sec. 3.4.1, pp. 227–231, Table 3.1 on p. 229 by page image: the source of the material and the table (2018 World Scientific printing; text layer, printed page = PDF page − 27). Table 3.2 (p. 230) and sec. 3.1 (pp. 193–201) read for context.
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

### Findings on the earlier notes

| Earlier item | Entry | Disposition |
|---|---|---|
| *Regional Benchmark Preference* (taxonomy) | `meth:algorithm-benchmark-choice` (Statement; rationales corrected in Pitfalls) | Rewritten |
| Table *Typical uses of benchmarks for trading algorithms* (not a counted block) | Rows: `meth:algorithm-benchmark-choice`, rebuilt as a sourced summary of Lehalle and Laruelle's Table 3.1 with links to the definitions; the benchmarks it names: `def:execution-benchmark` and `def:implementation-shortfall` | Rebuilt; original kept verbatim in the artefact |
| *Benchmark Is Not an Objective Alone* (caveat) | `meth:algorithm-benchmark-choice` (Pitfalls, Interpretation) | Rewritten |

**Corrections to the earlier text.**

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

### For review

- The three new entries, and ownership by the overview rather than `market-structure-execution-quality`.
- Reliance on Kissell and Harris for implementation shortfall while Perold is unread.
- The corrections to Kissell's eq. (3.10) and p. 100, and the double-counting and model-against-measurement notes.

## execution algorithms review: execution algorithms, 15 October 2026

Source checking, not study.

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
- **Feedback.** The earlier proposition shows only the sign. If induced moves persist and retrigger the rule, the total move is $dS/(1-\lambda q')$ for dimensionless $\lambda q'<1$ (1.67 at 0.4, checked by iteration); purely temporary impact gives no amplification.
- **Portfolio-insurance sizing.** Harris's box multiplies the fall by delta; the rebalancing trade depends on the change in the hedge ratio. A Black–Scholes illustration (zero rate, 20 percent volatility, one year) gives sales of about 1.0, 1.6 and 1.8 percent of insured value per 1 percent fall for floors at 80, 90 and 100 percent.
- The spread-against-impact accounting gap from execution benchmarks review stays open; no cost already in execution prices was added.

### Source findings and corrections to the earlier notes

- Lehalle and Laruelle's p. 197 sends the trading curve to app. A.6, which is the Harris tick model; the scheduling appendix is A.7. Figure 3.14's caption lacks its second algorithm name; the text says IS (p. 232).
- Envelope: a too-fast algorithm stops posting (not "posts passively"). Customisation examples: the would level makes an algorithm IS-like and the SOR liquidity-seeker-like; "PoV capped by urgency" and the "minimum-impact curve" are not in the source. Dark probes are supported (p. 196).
- What-if examples in the source are finishing now and switching IS to PoV; "portfolio coupling" is outside the pre-trade list.
- Harris separates the reactive–proactive continuum (search cost) from the aggressive–passive one (eagerness); the earlier principle conflated them. "Discretion range", "protection price", "pegging" and "minimum fill" are not in the passages.
- Harris treats package, basket and portfolio trading as one market; he explains tight package quotes by lower adverse selection, not diversification; his index-fund substitutes are non-index stocks, not futures or ETFs. "Portfolio transition" is only named (Kissell p. 16).
- Table 3.2: the earlier rows dropped PoV's "can be very aggressive", the VWAP/TWAP condition on unexpected volume in the order's direction and the liquidity seeker's relative-price orientation, and called VWAP/TWAP a "volume-curve schedule".

### Findings on the earlier notes

| Earlier block | Entry | Disposition |
|---|---|---|
| *Benchmark Customisation* | `def:trading-envelope` (Practice; examples corrected) | Rewritten |
| *Trading Envelope* | `def:trading-envelope` (Statement; "posts passively" corrected) | Rewritten |
| *Envelope Construction Segmentation* | `def:trading-envelope` (Statement, Conditions; "minimum-impact curve" unsourced) | Merged |
| *Pre-Trade Segmentation* | `meth:execution-decision-support` | Merged; portfolio coupling relocated |
| *Order-Submission Control Segmentation* | `def:order-exposure-decisions` | Rewritten; unsourced levers flagged |
| *Reactive vs Proactive Execution* | `def:order-exposure-decisions` | Rewritten; conflation with aggressiveness corrected |
| *Portfolio Trading Segmentation* | `def:portfolio-trading` | Rewritten; basket/package distinction corrected |
| *Dynamic Hedging Feedback* (proposition and proof) | `mech:positive-feedback-hedging` (Interpretation) | Merged; size and stability added |
| *Basket Characterisation Inputs* | `def:portfolio-trading` (Conditions; reason for tight quotes corrected) | Rewritten |
| *What-If Controls* | `meth:execution-decision-support` | Merged; examples corrected |
| Table *Typical features of trading algorithms* (not a counted block) | `meth:algorithm-benchmark-choice`, rebuilt from Lehalle and Laruelle's Table 3.2 with links | Rebuilt; original kept verbatim in the artefact |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | secs. 3.1.1–3.1.3, pp. 196–201; sec. 3.4.1, pp. 230–233 | Text layer; page images of pp. 198, 201, 230, 231, 233; envelope references (Bouchard et al., Lehalle, Guéant et al.) not consulted |
| `alpha-harris` | chap. 18, pp. 380–389; chap. 23, pp. 486–491; chap. 28, pp. 560–561 | Text layer; market facts as of 2002 |
| `s7-kissellscience` | chap. 1, pp. 16–19; chap. 3, p. 108 | Text layer; not on a route |

The five new entries and the extended `meth:algorithm-benchmark-choice` are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The five new entries, the Table 3.2 extension, and ownership by the overview rather than `price-impact-execution`.
- The participation-denominator question and the portfolio-insurance sizing correction.
- The source slips in Lehalle and Laruelle (A.6 reference, Figure 3.14 caption).

## transaction-cost analysis review: transaction cost analysis, 15 October 2026

Source checking, not study.

### Sources, 2026-10-15

- **Harris**, 2002 Oxford printing (text layer; printed page = PDF − 13): chap. 7, pp. 151–167 (principal–agent problem, best execution, dual trading, preferencing, soft dollars, dishonest brokers); chap. 15, pp. 328–331 (block dealers, trade reporting, motive audit, Table 15-2); chap. 21, pp. 420–423, 432 and 435–441 (components, signed cost, marginal rule, prediction), reusing execution benchmarks review's pp. 424–437; chap. 22, pp. 442–450 and 469–470 (performance evaluation, smoothing); chap. 25, pp. 514–519 (best execution practice, Rules 11Ac1-5 and 11Ac1-6). The marginal-aggressiveness passage (pp. 437–438) was read in the topic review, not taken from the earlier lead.
- **Kissell**, `s7-kissellscience`, the inspected copy whose copyright page says 2014 (the catalogue's 2013 date is unchanged): chap. 3, pp. 87–96 (best execution, ten components, TCA phases, cost against performance) and pp. 110–113 (index-adjusted cost and z-scores; page image of p. 112).
- **Lehalle and Laruelle**, 2018 printing: sec. 3.1.3, pp. 200–203 (performance indicators, pre-, live- and post-trade compatibility, TCA); app. A, sec. A.7.2, pp. 278–279, with the page image of p. 279 for (A.26), the passage the average-price decomposition cites.
- **Perold** remains unread; the topic review relies on it only through Kissell's and Harris's attributions, as before.

### Accounting checks (own, Interpretation in the entries)

- **Shortfall formula.** $\mathrm{IS}=dq(\bar p-p_0)+d(Q-q)(p_T-p_0)+$ explicit costs equals Perold's form with $S=dQ$; execution benchmarks review's example gives 3,960 for the buy and the sell.
- **Spread and drift split.** With pre-fill midpoints $m_j$: delay $S(P_0-P_d)$ + half-spread paid $\sum s_j(p_j-m_j)$ + midpoint drift $\sum s_j(m_j-P_0)$ + opportunity $(S-\sum s_j)(P_n-P_0)$ + fees. Buy and sell examples with partial fills reconcile exactly: 1,000 + 300 + 600 + 2,000 + 60 = 3,960. It is an accounting identity; the drift is not causal impact.
- **Lehalle and Laruelle's decomposition.** (A.26) is $\mathbb E(W)+\lambda\operatorname{Var}(W)$, an ex-ante objective whose third term is a variance penalty. Its realised counterpart $W=v^\star S_0+\sum x_n\sigma_n\xi_n+\kappa\sum\sigma_nv_n^{\gamma+1}/V_n^\gamma$ holds exactly inside the model (checked by simulation, book's timing); on data the impact term is a model value and the move a residual. The refined decomposition (planned price, unexpected moves, trading efficiency) has no formula, so its additivity cannot be checked.
- **Kissell's index adjustment.** Eq. (3.22) leaves the index term unsigned; for a sale 50 bp below arrival while the index fell 50 bp with $\hat\beta=1$, it gives 100 bp of adjusted cost instead of 0. The side factor is needed.
- **Performance identity.** Harris's $r^p=(r^p-\beta r^m)+(\beta r^m-r^m)+r^m$ checked. His realised alpha differs from Jensen's by $(1-\beta)r^f$ (−0.9 points at $\beta=1.3$, $r^f=3\%$).
- **Examples.** Harris's cotton example (\$137,500) recomputed.
- **Marginal rule.** Harris states it as advice: objective, choice variable and smoothness assumptions are Interpretation; there is no proof of optimality in the source.
- **Evaluation populations.** TCA averages by order or by value depend on which orders each broker received; routing tables from unadjusted averages confound selection with skill.

### The spread-versus-impact gap

Partly addressed, not closed. The split above gives spread (half-spread paid against pre-fill midpoints), timing before arrival (delay), opportunity and fees with explicit references, and reconciles to the total without double-counting spreads already in fill prices. The rest, midpoint drift, mixes own impact with market and other traders' moves. Kissell says impact is an unobservable counterfactual (pp. 91–92), and a market-adjusted residual is impact only under the model used. The checkpoint's impact component is therefore still open, as is the effect of the tick, fee and reporting rules in force.

### Source findings and corrections to the earlier notes

- Harris: adverse selection is a cause of the spread, not a separate implicit cost; delay is Kissell's investment-related cost. Borrow charges, the venue variables in cost prediction, "benchmark change" and "past behaviour" in the motive audit, and venue selection as gaming are not in the passages.
- Best execution: the earlier "best auditable outcome given objective, limit, urgency, venues and information risk" merges Harris's auditability standard with Kissell's process definition. Rules 11Ac1-5 and 11Ac1-6 are as of 2002 (now Rules 605 and 606, amended 2024; the pathway's readings on them are unread).
- Broker conflicts: Harris treats commission recapture as a sponsor's tool, not a broker incentive; payment for order flow resembles but is generally not a kickback.
- Block reporting: Harris argues that timely reporting hurts facilitating dealers; the earlier claim that delayed reporting helps informed initiators exploit stale prices is not his.
- Performance: the earlier "money-weighted IRR, useful when the investor controls flows" and "trade-weighted" measures are not Harris's; his IRR is approximately time- and value-weighted.

### Findings on the earlier notes

| Earlier block | Entry | Disposition |
|---|---|---|
| *Transaction Cost Component Segmentation* | `def:transaction-costs` | Rewritten; glosses corrected |
| *Risk-Adjusted Excess Return* | `meth:relative-performance-evaluation`; TCA analogy in `meth:transaction-cost-analysis` | Rewritten; alpha definitions distinguished |
| *Benchmark Failure Modes* | `meth:transaction-cost-analysis` (Pitfalls) | Merged; a synthesis, flagged |
| *Performance Attribution Segmentation* | `meth:execution-decision-support` | Merged; (A.26) relationship corrected |
| *Selection and Timing Decomposition* | `meth:relative-performance-evaluation` | Merged (Harris's identity) |
| *TCA Uses Wider Samples Than Post-Trade Review* | `meth:transaction-cost-analysis` | Merged; selection limit added |
| *TCA Estimator Quality Segmentation* | `def:execution-benchmark` | Merged (duplication of Harris sec. 21.4) |
| *Pre-Trade Cost Prediction Variables* | `meth:transaction-cost-analysis` (Conditions) | Merged; unsourced variables flagged |
| *Broker and Algo Selection* | `meth:transaction-cost-analysis` | Merged; selection caveat |
| *Gaming the Measure* | `def:execution-benchmark` | Merged; venue-selection gloss flagged |
| *Block Trade Reporting Trade-Off* | `def:block-trade` | Merged; argument corrected |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | chaps. 7, 15, 21, 22, 25 as above | Text layer; rules and figures as of 2002 |
| `s7-kissellscience` | chap. 3, pp. 87–96, 110–113 | Text layer; page image of p. 112; not on a route |
| `alpha-laruelle` | pp. 200–203; app. A.7.2, pp. 278–279 | Text layer; page image of p. 279 |
| `wide-perold-shortfall`, `ex-sec-rule605-2024`, `ex-sec-withdrawal-2025`, `wide-getmansky-lo-makarov` | none | Not read |

The six new entries and the four extended entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The accounting split and its limits, the (A.26) correction, the Kissell side correction.

## smart order routing review: smart order routing, 15 October 2026

Source checking, not study.

### Sources, 2026-10-15

- **Lehalle and Laruelle**, 2018 World Scientific printing (text layer; printed page = PDF − 27): sec. 3.4.2, pp. 233–244, with page images of pp. 235 (Table 3.3), 236 (the broker outcomes and the fee inequality), 240 (Table 3.4, eq. (3.3)) and 241 (Table 3.5, eq. (3.4) and footnote 16). Pp. 237–239 and 242 read in the text layer.
- **17 CFR 242.611**, the order protection rule: text retrieved on 15 October 2026 through the eCFR versioner API, point-in-time 13 October 2026; versions listed since 2016, latest 14 June 2024; citations 70 FR 37620 (2005), 83 FR 58429 (2018), 86 FR 18811 (2021), 89 FR 26616 (2024). The effective and compliance dates of the 2024 amendment were not checked. This verifies Rule 611 only, not Rules 605, 606 or 610, FINRA's best-execution rule, or any European rule.
- **MiFID II**: the consolidated text could not be retrieved (EUR-Lex returned an empty response), so the European regime is stated only as Lehalle and Laruelle describe it in 2018.
- Harris's preferencing passages (chap. 7, pp. 161–162) were reused from transaction-cost analysis review. `ex-sec-rule605-2024`, `ex-sec-withdrawal-2025`, `ex-sec-tick-access-2024` and Perold remain unread.

### Regulatory claims: historical against verified

- **Verified as of 15 October 2026:** Rule 611 obliges a *trading center* to keep and enforce written policies reasonably designed to prevent trade-throughs of protected quotations in NMS stocks, and to surveil them, with nine exceptions (system failures, non-regular-way trades, single-priced opening, reopening and closing transactions, crossed protected quotations, intermarket sweep orders, orders not priced off the quote, quotes inferior within the prior second, stopped customer orders). It is quote protection by venues, not a broker's best-execution duty or a reporting obligation, and it does not require venues to reroute; an intermarket sweep order lets the router take protected quotes itself.
- **Historical (2018, not verified as current):** Lehalle and Laruelle's statements that U.S. clearing and settlement fees must be equal across venues, and that European executing brokers choose their consolidation and must disclose a best-execution policy.
- **Historical (2002):** Harris's Rules 11Ac1-5 and 11Ac1-6, unchanged from transaction-cost analysis review.

### Findings on the earlier notes

| Earlier block | Entry | Disposition |
|---|---|---|
| *Routing Logic Segmentation* | `def:smart-order-routing` | Merged; a synthesis, flagged |
| *Child-Order Routing Loop* | `def:smart-order-routing` | Merged; a synthesis, flagged |
| *Best Execution Differs by Regime* | `def:best-execution` | Merged; Rule 611 verified, European regime dated 2018 |
| *Active Sweep Segmentation* | `def:smart-order-routing` | Merged; "local best price" corrected |
| *Fee-Adjusted Price Priority* | `res:fee-adjusted-venue-choice` | Rewritten; sell side and per-share fees added |
| *Payment-for-Order-Flow Routing Conflict* (proposition and proof) | `def:broker-agency-conflicts` | Merged as Interpretation |
| *Minimum Resting-Time Split* | `meth:passive-order-split` | Rewritten; non-negativity corrected |
| Table *Passive routing criteria…* (not counted) | `meth:passive-order-split` | Rebuilt from Lehalle and Laruelle's Table 3.6 with venue names; original kept verbatim |

**Routing and fee-accounting checks** (own; Interpretation in the entries):

- **Three-broker example.** Sweeping Table 3.3's cheapest levels: B1 (Euronext and Chi-X, split) 101.15 and B3 (all three, split) 100.75, as printed. The best single venue for 500 shares is Chi-X at 102.05 (Euronext 102.10, Turquoise 102.20), against the printed 102.50: a likely misprint. B1's bracketed quantities add to 600 and list depth, not fills.
- **Fee threshold.** Exactly $\delta<\phi/(1+f-\phi)$ for a buy (acquisition cost) and $\delta<\phi/(1-f+\phi)$ for a sell (proceeds), both about $\phi$; illustrative $P=100$, $f=3$ bp, $\phi=1$ bp give thresholds 0.99980 and 1.00020 bp, and $\delta=0.99$ and 1.01 bp flip the choice on both sides. With per-share fees the condition is $P\delta<c-c'$. Fees are proportional and paid by the taker; rebates are negative fees; both quotes are assumed contemporaneous, executable for the whole size and taken; the spread is in the prices and not added again. A favourable fee-adjusted quote does not establish a fill or best execution.
- **Passive split.** The book prints eq. (3.4) as $(D-\sum Q_n)/\sum r_n$; its footnote and Table 3.5 need $D+\sum Q_n$ (62.5 s, against −12.5 s). Table 3.5 recomputed (35/42.5/22.5 percent; 175/212.5/112.5 shares). A venue with $f_n<0$ must be dropped and $\tau^\star$ recomputed: setting it to zero leaves fractions not summing to one (checked on an illustrative case). Equal finishing times minimise the completion time of the whole order, not an average. The model treats queues and rates as fixed.
- **Latency.** Displayed depth is not assumed to remain while a sequence of child orders is routed; the book's mirrored-liquidity example is kept as a scenario, not a measured effect.
- **Routing conflict.** The earlier proposition is a condition under which client- and broker-optimal routing differ; it is not evidence of conflicted routing.
- The accounting split of transaction-cost analysis review and its limit (midpoint drift is not automatically own impact) are unchanged.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | sec. 3.4.2, pp. 233–244 | Text layer; page images of pp. 235, 236, 240, 241; Laruelle et al. (2011, 2013) not consulted |
| 17 CFR 242.611 | full section, eCFR point-in-time 13 Oct. 2026 | Effective and compliance dates of the 2024 amendment not checked |
| MiFID II | none | Not retrieved; European regime dated 2018 |

The three new entries and the two extended ones are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The three new entries; the merges into `def:best-execution` and `def:broker-agency-conflicts`.
- The Rule 611 statement and its scope; the European regime left as of 2018.
- The eq. (3.4) and B2 misprints, the fee thresholds and the split's non-negativity correction.

## high-frequency strategies review: high-frequency trading strategies, 15 October 2026

Source checking, not study.

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

### Source findings and corrections to the earlier notes

- The earlier taxonomy's five categories are its own: the SEC's arbitrage and directional types split "statistical arbitrage"; "latency arbitrage" is the release's structural stale-price example and its cross-venue arbitrage question; "liquidity detection" is a tool (pinging) used both in ordinary search and in order anticipation; momentum ignition was missing.
- "Edge decays with diffusion" is contradicted by BCS: arbitrage durations fell from 97 to 7 ms while profit per opportunity stayed about constant, and in the model the prize does not depend on speed or its cost. What decays is a firm's relative lead and, at the margin, its profit net of speed costs.
- Lehalle and Laruelle overstate their own cost rise (0.5 against 0.37 bp) and report HFT shares of trades as hearsay; the SEC's 50 percent-plus volume share comes from press reports.

### Findings on the earlier notes

| Earlier block | Entry | Disposition |
|---|---|---|
| *HFT Strategy Segmentation* (taxonomy, with its closing sentence) | `def:hft-strategies` | Rewritten against the SEC's four types; statistical and latency arbitrage remapped, liquidity detection reclassified as a tool, momentum ignition added |
| *HFT Edge Decays With Diffusion* (principle) | `res:latency-arbitrage-arms-race` (Pitfalls) | Rewritten; premise corrected (the prize is not competed away, rents are dissipated into speed); "lower costs" supported (n. 27); inventory control, better models and privileged order flow unsupported, kept in the artefact only |
| *Message Profit Is Not Market Quality* (caveat) | `res:hft-spread-investor-cost` (Practice, Pitfalls) | Merged; the evaluation criteria kept as the earlier notes' own, its effects stated as possibilities and open questions, not findings |

- The SEC's 2010 release places order anticipation among its HFT strategy types and distinguishes pinging for liquidity from pinging to trade ahead.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `sec-concept-release-2010` | sec. IV.B, pp. 45–58 | Text layer; a 2010 request for comment; no later SEC action checked |
| `wide-budish-cramton-shim` | pp. 1547–1556, 1576–1592 | Text layer; page images of pp. 1589–1590; secs. II–V and VII–VIII not read |
| `alpha-laruelle` | pp. 158–169 | Text layer; page images of pp. 164–166 and 168 |
| `wide-menkveld-hft-review` and the pathway's other readings | none | Not available or not read |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The three new entries; the reading of the SEC's types as an organising device, not a classification.
- The correction to the "edge decays" principle and the 0.37 bp correction to Lehalle and Laruelle.

## execution control review: reinforcement learning and ML in execution, 15 October 2026

Source checking, not study.

### high-frequency strategies review correction

`res:latency-arbitrage-arms-race` said that one firm quotes $y\pm s/2$. Proposition 1(i) (printed p. 1583, rechecked) says that exactly one unit is offered at each of $y-s/2$ and $y+s/2$, and that the two quotes may belong to one trading firm or to two distinct firms; the authors assign the liquidity-provider role to one firm for simplicity, with economically equivalent equilibria in which it rotates or is random (pp. 1579–1580), and the sniping probability is Proposition 1(iii). The entry, its status line and the reading note `wide-budish-cramton-shim` were reworded; eqs. (3) and (7) are unchanged.

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

### Source findings and corrections to the earlier notes

- The earlier notes copy the appendix, including its objective without the half-spread at $T$; they call $H_t(\nu)$ a value function and attribute the dynamics to Cartea and Jaimungal directly.
- "Larger $\phi$ or $A$ pushes faster liquidation; stronger $\kappa$ smoother trading" holds under the model for $\phi$ (front-loading) and $\kappa$, but $A$ mainly governs completion near $T$, and a larger $\kappa$ with finite $A$ also leaves more unsold.
- Hambly, Xu and Yang support the control and RL items (model needed against learning from interaction; model-based against model-free) but not "learn … from simulated or historical interaction" as one thing: they flag data scarcity and non-stationarity and call for simulators (p. 49), and replaying history does not show the response to one's own orders. The hybrid item (control for constraints, ML for forecasts, fills and regimes) is not in the passages; the survey reports only a combination of Almgren–Chriss with Q-learning (p. 34).

### Findings on the earlier notes

| Earlier block | Entry | Disposition |
|---|---|---|
| *Stochastic-Control Execution View* (model) | `mod:cartea-jaimungal-execution` (Statement, Notation) | Merged; "value function" corrected to a fixed policy's reward |
| *Cartea-Jaimungal State Dynamics* (model) | `mod:cartea-jaimungal-execution` (Statement, Notation, Conditions) | Merged; units, signs and constraints added; attribution qualified (Lehalle and Laruelle's account) |
| *Value Function Intuition* (principle) | `mod:cartea-jaimungal-execution` (Practice) | Merged; qualified by own numerical paths ($A$ governs completion, $\kappa$ also leaves residual) |
| *Control vs Learning* (taxonomy) | `mod:cartea-jaimungal-execution` (Practice, Pitfalls); backlog stub `meth:hybrid-control-learning-execution` | Control and RL items merged from Hambly, Xu and Yang, with simulator and historical data separated; the hybrid item unsupported, kept in the artefact and stubbed |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | app. A.7.3, pp. 281–284 | Text layer and page images; Cartea and Jaimungal's originals not consulted |
| `wide-hambly-xu-yang` | pp. 2–4, 7, 32–35, 49 | arXiv v4, not the journal version; the studies it reports not checked |
| `crypto-cartea`, Cartea–Jaimungal papers, `wide-kolm-ritter-rl`, other readings | none | Not consulted or not read |

The new entry is *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- Ownership by `reinforcement-learning-trading` and the new chapter `ml-alternative-data/`.
- The appendix corrections and the qualified parameter intuition; whether to check the model against Cartea and Jaimungal's originals.
- The backlog stub for hybrid execution.

## execution control review follow-up: mathematical corrections to `mod:cartea-jaimungal-execution`, 15 October 2026

A bounded correction to execution control review (`6d04e52`), run from that pushed state. The execution control review record above is left as written; where it differs, this section supersedes it. No entry, label or backlog stub changed; no source was re-read.

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

`check_compendium.py --check`: 0 problems. Tests: 14 passed. `latexmk -g -pdf compendium.tex`: exit 0; 182 pages (181 before; the entry grew by a page); no LaTeX warnings; 0 overfull and 26 underfull boxes; the one `page.i` warning. A first build had one overfull line (the wealth identity in one display), split into two lines. Rendered and inspected: PDF pp. 7–10 (the corrected entry).

### Remaining limits

No verification theorem for the quadratic ansatz; the constrained one-directional problem is not solved; Cartea and Jaimungal's originals and `crypto-cartea` are still unconsulted; `wide-hambly-xu-yang` still read only in arXiv v4.

## trading infrastructure review: production considerations, 15 October 2026

Source checking, not study.

### execution control review clarification

The wealth identity in `mod:cartea-jaimungal-execution` now states that the cash account starts at $X_0=0$, with $X_0$ to be added to the right-hand side otherwise. The follow-up's corrections, checks and limits are unchanged; the check script already starts cash at 0.

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

### Findings on the earlier notes

| Earlier block | Entry | Disposition | Rationale |
|---|---|---|---|
| *Trading Architecture* (principle) | `def:automated-trading-architecture` (new) | Rewritten | Lehalle and Laruelle Fig. 3.1, pp. 193–194, 198; "the hard part … decision chain" flagged as synthesis |
| *Trading Tool Input Segmentation* | `def:automated-trading-architecture` | Merged | sec. 3.1.1, pp. 194–197; calendar items beyond expiries, expected news and half-days unsupported |
| *Broker-Dealer Operations Segmentation* | artefact only | Deleted | Harris sec. 7.2 (pp. 147–148) classifies a brokerage as front office, back office (incl. compliance, credit, systems) and proprietary operations (cash and risk management); the five-way list of the earlier notes is its own and serves no pathway outcome |
| *Analytics Close to the Feed* | `def:automated-trading-architecture` | Merged | p. 195; book imbalance and queue size not in the source |
| *Connections Are Two-Way* | `def:automated-trading-architecture` | Merged | pp. 195–196; public book updates belong to the market-data feed, not the connection |
| *Model Component Segmentation* | `def:automated-trading-architecture` | Merged | pp. 196–197, with deactivation of inadequate models; cross-referenced to the governance entry |
| *Indicator Publication* (process) | `meth:execution-decision-support` | Merged | pp. 200–202; the book prints "stateless agents", the earlier notes "stateful" |
| *Audit Trail* (process) | `meth:automated-trading-operational-controls` (new) | Rewritten | Harris pp. 544–545; allocation, linkage to public state and the listed tests unsupported; current audit-trail rules not checked |
| *Automated Trading Reliability Segmentation* | `meth:automated-trading-operational-controls` | Merged | Harris pp. 549–551; Rule 15c3-5(c)(2)(iii)–(iv); drop copies, replayable feeds, tamper-resistant logs, bounded delays and the market-quality claim unsupported |
| *Network Failure Creates Position Risk* (caveat) | `meth:automated-trading-operational-controls` | Rewritten | Harris box p. 550; Rule 15c3-5(c)(1)(ii) (duplicative orders); unknown order state, fill state, reconciliation, retry, cancellation and recovery separated as Interpretation |
| *Automated System Cost Structure* (mechanism) | `def:floor-automated-trading-systems` (new) | Rewritten | Harris chap. 27, pp. 543–554 and Table 27-1 |

- The FIX reading of `research-engineering-validation` was not consulted for the order-state and audit material.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-laruelle` | pp. 193–203 | Text layer; page images of pp. 194 and 202 |
| `alpha-harris` | pp. 147–148, 159, 543–554 | Text through PDFKit; page images of pp. 550 and 552 |
| `cfr-240-15c3-5` | full section, eCFR 13 Oct. 2026 | Adopting release not read |
| `wide-mifid-rts6`, `s6-fix`, `wide-knight-capital`, other pathway readings | none | Not retrieved or not read |

The three new entries and the extended `meth:execution-decision-support` are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The order-state synthesis and the reliance on one U.S. rule; the RTS 6 and FIX stubs.

## trading infrastructure review follow-up: clarifications, 15 October 2026

Three clarifications to trading infrastructure review (`1c3fabc`), made at the start of equity market structure review; the trading infrastructure review record above is left as written.

- `def:automated-trading-architecture`: Lehalle and Laruelle's "known in real time" is now quoted as theirs and qualified. The market volume $V$ is available only as observed; volume still to come requires a forecast. It cross-references the decision-time item already in `def:trading-envelope`.
- `cfr-240-15c3-5` in `front/sources.tex`: the SEC adopting release, 34-63241, is dated 3 November 2010 (checked on p. 130 of the release PDF from sec.gov); the Federal Register published it on 15 November 2010, where the eCFR cites the rule text at 75 FR 69825.
- `def:floor-automated-trading-systems`: the six bullets are now presented as the entry's grouping of Harris's seven sections (27.1–27.7), with Table 27-1 listing eleven issues. High absolute start-up costs (p. 549) and the table's relatively lower software costs (p. 552) are recorded as compatible, not as a contradiction; the Harris reading note and the `execution-market-making` pathway note were reworded to match.

## equity market structure review: equity market microstructure, 15 October 2026

Source checking, not study.

### Sources, 2026-10-15

- **Harris**, 2002 Oxford printing (text through macOS PDFKit, as in trading infrastructure review; printed page = PDF − 13): sec. 15.6.1, pp. 333–334; chap. 23, p. 484, sec. 23.4, p. 489, sec. 23.5 with Table 23-1, pp. 491–492.
- **Lettau and Madhavan** (`ex-lettau-madhavan-2018`): NBER Working Paper 24250, January 2018, pp. 1, 4–8, 18, text layer. The published JEP version was not retrieved (the AEA site returned a bot check). The paper discloses Madhavan's BlackRock role.
- **Pan and Zeng** (`wide-pan-zeng-etf`): ESRB Working Paper 59, December 2017, abstract and pp. 1–3, text layer (printed page = PDF − 2). SSRN, the catalogue's record, returned a bot page.
- **Not consulted:** current exchange or FINRA block and trade-reporting rules, Rule 611 trade-through exceptions, SEC Rule 6c-11 on ETFs, Hasbrouck (the only local Hasbrouck file found was his 2004 lecture notes, which the reading note already excludes). All requests used generic headers.

### Distinctions kept

- **Block trades.** Reporting or printing venue, execution priority against the book, and trade-through protection across venues are kept apart in `def:block-trade`; only Harris's 2002 exchange rule is stated.
- **ETFs.** Creation and redemption between APs and the fund is kept apart from secondary trading of ETF shares, in-kind from cash, and the arbitrage incentive from guaranteed convergence; stale NAV and AP discretion are the stated limits. Pan and Zeng's evidence is labelled corporate-bond-only.
- **Index costs.** Harris's three reasons replace the four of the earlier notes.

### Findings on the earlier notes

| Earlier block | Entry | Disposition | Rationale |
|---|---|---|---|
| *Equities as Microstructure Laboratory* (principle) | artefact only | Deleted | No checked source supports "cleanest empirical laboratory" or the transfer list; the asset-class pathways carry the differences with their own readings |
| *Asset-Class Transfer* (caveat) | artefact only | Deleted | Orientation statement without a checked source; the same pathways cover it |
| *Equity Block Prints and Size Priority* (marketrule) | `def:block-trade` (Practice, Pitfalls); stub `rule:block-print-trade-through-current` in `market-structure-execution-quality` | Merged as historical; current rules stubbed | Harris sec. 15.6.1, pp. 333–334 (2002): print requirement, size precedence above 25,000 shares, price priority; reporting, execution priority and trade-through protection separated; "trade-reporting facility" and current exceptions unverified |
| *Index Markets Trade Common Risk* (principle) | `def:portfolio-trading` (Conditions, Pitfalls) | Merged | Harris pp. 484, 489: three reasons (few informed traders, activity, one transaction); "easier to net" and "easier to hedge" are not his |
| *Index Product Segmentation* (taxonomy) | `mech:etf-creation-redemption` (Practice, Pitfalls) | Merged | Harris sec. 23.5, pp. 491–492; futures "basis" and the closing choice sentence unsupported |
| *ETF Basket Arbitrage* (mechanism) | `mech:etf-creation-redemption` (new) | Rewritten | Lettau and Madhavan pp. 4–8, 18; Pan and Zeng pp. 1–3; borrow, cash substitution and taxes as weakening factors unsupported |

- The checked support was Harris's 2002 descriptions and the ETF readings; current venue rules were not checked.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-harris` | pp. 333–334, 484, 489, 491–492 | Text through PDFKit; facts as of 2001–2002 |
| `ex-lettau-madhavan-2018` | WP pp. 1, 4–8, 18 | Working-paper version, not the JEP article |
| `wide-pan-zeng-etf` | ESRB pp. 1–3 and abstract | Model and data read only in the introduction |
| current venue and ETF rules | none | Not checked; stubbed or stated as unchecked |

The new entry and the two extended entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The ETF entry's reliance on working-paper versions.

## equity market structure review follow-up: ETF and Harris precision, 15 October 2026

A bounded correction to equity market structure review (`580463e`), run from that pushed state. The equity market structure review record above is left as written; where it differs, this section supersedes it.

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

Source checking, not study, and not the pathway's checkpoint: no roll cost was measured.

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
- **Price discovery.** The empirical result (sample March–May 2000) is kept apart from theory (Garbade–Silber, unread) and from untested explanations.

### Findings on the earlier notes

| Earlier block | Entry | Checked locator | Disposition |
|---|---|---|---|
| *Centralised Futures Trading* (principle) | `conv:cme-globex-trading` (new) | Harris sec. 15.6.2, p. 334; CME Rulebook Rules 526, 538 | Rewritten; the earlier notes' reasons (margining, fungibility) unsupported, the rule-based reason substituted |
| *No Call Auction Norm* (caveat) | `conv:cme-globex-trading` | CME wiki "Indicative Opening Price and Quantity" and "Supported Matching Algorithms" (updated 11 Feb. 2025); CFTC filing 22 Sep. 2020 | Corrected: wrong for the Globex open; ES daily settlement is a 30-second VWAP; "liquid trading hours" unsupported |
| *Lead-Lag With Cash Markets* (mechanism) | `ev:index-futures-price-discovery` (new) | Hasbrouck WP FIN-00-046 abstract, pp. 4–6, 13, 34; Harris p. 489 via `def:portfolio-trading` | Rewritten as evidence; the earlier notes' conditions marked untested |
| *Large Tick Futures* (principle) | `res:spread-determinants` (merged); stub `ev:futures-tick-size-evidence` in `futures-execution` | Lehalle and Laruelle eq. (2.1), pp. 144–145, and p. 148 | Merged; the futures-specific and equity-comparison claims unchecked |
| *Futures Architecture Drivers* (taxonomy) | `mech:futures-margin-settlement` (Pitfalls) | CME Rules 802, 814, 820; Harris p. 492; Rule 538 | Merged; standardisation and ETF link unchecked |
| *Variation Margin* (mechanism) | `mech:futures-margin-settlement` (new) | CME Rules 814, 820, 802.B | Rewritten; "credit risk controlled continuously" corrected |
| *Futures Block and EFP Segmentation* (taxonomy) | `conv:futures-block-efrp` (new) | CME Rules 526, 538; RA2607-5 pp. 4, 10 (Q14), Q28; RA1911-5 p. 1; Harris p. 334 | Rewritten; "transitory EFP" verified as history and prohibited at CME Group since 4 Aug. 2014 |

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

### For review

- The reliance on CME documentation retrieved on one date, and on a 2000 working-paper draft for the price-discovery evidence.

## futures market structure review follow-up: corrections, 15 October 2026

A bounded correction to futures market structure review (`fb56198`), run from that pushed state. The futures market structure review record above is left as written; where it differs, this section supersedes it. No entry, label or backlog stub changed.

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

`check_compendium.py --check`: 0 problems. Tests: 14 passed. `latexmk -g -pdf compendium.tex`: exit 0; 193 pages (191 before, from the longer waterfall and settlement text); no LaTeX warnings; 0 overfull and 26 underfull boxes; the one `page.i` warning. Rendered and inspected: printed pp. 35 (`res:spread-determinants`), 75 (the ETF opening), 78 (settlement) and 79--80 (EFRP and margin), PDF pp. 41, 81, 84 and 85--86.

### Remaining limits

- The current CME settlement page is still unretrieved, so the procedure is as filed in 2020.
- Default-management auction details (subordination and seniorization amounts) are in confidential guidelines.
- Customer-side FCM rules and intraday cycle times are unchecked.

## futures market structure review second follow-up: account classes and the second-month settlement, 15 October 2026

Two wording clarifications, run from `bd4ba54`. Earlier records are left as written.

1. `mech:futures-margin-settlement`: "customer losses only from the collateral of the customer account class concerned" stated the restriction in the wrong direction. CME Rules 802.A.5 and 802.G (including 802.G.1 and 802.G.6), read in the chapter-8 text retrieved on 15 October 2026, give the following, and the entry now says so:
   - default management runs separately by account class;
   - a customer-class loss is met first from that class's customer collateral, which in a defaulted customer futures class includes the collateral of customers who did not cause the default (802.G.1);
   - the member's own assets are applied across classes with priority to customers (802.A.5.i, iii);
   - remaining proprietary collateral may cover customer-class losses, pro rata among defaulted customer classes (802.G.6);
   - segregated customer collateral may not be used for proprietary obligations or for another customer class.
2. `conv:cme-globex-trading`: the second month is derived by applying the lead–second spread price to the lead-month settlement. Tier 2 says so explicitly in Exhibit B (PDF p. 6, rendered blackline): the last spread trade, or the nearer of the spread's bid or ask if the trade lies outside them. The entry marks the same reading of Tier 1 as Interpretation. The ES-only VWAP, the rounding and the 2020 dating are unchanged.

## FX market structure review: FX market microstructure, 15 October 2026

Source checking, not study; the pathway's checkpoint was not attempted.

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

### Findings on the earlier notes

| Earlier block | Entry | Checked sources | Disposition |
|---|---|---|---|
| *FX Is Dealer-Centric and Fragmented* (principle) | `def:fx-market-structure` (new) | BIS pp. 22–23; Cartea–Jaimungal–Walton p. 2 | Rewritten; prime-brokered access unchecked |
| *FX Venue Segmentation* (taxonomy) | `def:fx-market-structure` (venues, ECNs, RFQ); `mod:fx-internalisation-horizon` (new; internalisation); fixing windows left to `fx-funding-settlement` | BIS pp. 5, 12, 23, 43; Butz–Oomen pp. 1–2, 8, 11 | Split: venues, protocols and internalisation separated; RFQ "for size or less liquid pairs" unsupported as a restriction |
| *Last Look* (definition) | `mech:fx-last-look` (new) | FX Global Code Principle 17, pp. 22–23 (page images), p. 1; DB cover sheet sec. C.4; CJW abstract | Rewritten; the stale-quote rationale marked as the model premise |
| *FX Cost Is Relationship-Dependent* (caveat) | `mech:fx-last-look` (Practice, Pitfalls) and `mod:fx-internalisation-horizon` (Practice); stub `ev:fx-last-look-fill-reject-evidence` | BIS Box B p. 11, p. 27; Butz–Oomen abstract, p. 2; DB cover sheet | Merged; "can dominate fill quality" dropped as unsupported; prime-broker limits unchecked |

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

Source checking, not study; the pathway's checkpoint was not attempted.

### Sources, 2026-10-15 (generic request headers)

- **Bryzgalova, Pavlova and Sikorskaya** (`ex-bryzgalova-pavlova-sikorskaya-2023`), the published *Journal of Finance* article, open access (CC BY), early-view pagination, from LBS Research Online eprint 2827: abstract and pp. 2, 4–5, 7, 11–12, 14–17, text layer (printed page = PDF − 1), with page images of Table I (pp. 15–16). U.S. OPRA data, 4 November 2019 to 30 June 2021.
- **Abstracts only**, from the publishers' records as served by RePEc, Crossref and OpenAlex: Jameson and Wilhelm (`ex-jameson-wilhelm-1992`), Huh, Lin and Mello (`ex-huh-lin-mello-2015`), Muravyev (`wide-muravyev-order-flow`), Muravyev and Pearson (`wide-muravyev-pearson`), Battalio, Hatch and Jennings (`ex-battalio-hatch-jennings-2004`). No open full text was found; the EFMA 2013 working-paper copy of Huh, Lin and Mello returned HTTP 503, and a copy of Muravyev and Pearson on a trading-forum host was not used.
- **Not read:** any OCC or exchange rule on clearing, exercise, assignment, margin, complex orders or price-improvement auction fees; `wide-christoffersen-option-illiquidity`, `ex-eraker-osterrieder-2023`, `exp-baldacci-options-market-making`.

### Distinctions kept

- **Surface and liquidity.** A linked set of prices (the implied volatility surface) is kept apart from liquidity, which is measured contract by contract; option liquidity is kept apart from the hedge instrument's.
- **Risks.** Hedging cost, volatility risk, inventory risk and information risk are separated, each with its source and the source's status (empirical abstract, model prediction).
- **Costs.** Quoted against effective spreads, both against timing-adjusted spreads with a fair-value benchmark; percent-of-premium against volatility units; outright against multi-leg (the BPS figures are single-leg only).
- **Market, sample and contract.** Every figure carries its market (U.S.), period (2019–2021), contract set and measure; the abstract-only findings are marked as such, with samples unread.

### Findings on the earlier notes

| Earlier block | Entry | Checked sources | Disposition |
|---|---|---|---|
| *Options Are Surface Markets* (principle) | `res:option-market-maker-spreads` (new) | Jameson–Wilhelm, Huh–Lin–Mello, Muravyev (abstracts) | Rewritten; "liquidity lives on a surface" kept as interpretation only, the implied-volatility surface distinguished from uniform liquidity |
| *Post-Trade Complexity* (caveat) | `res:option-market-maker-spreads` (Pitfalls); stub `mech:options-clearing-exercise-assignment` | Battalio–Hatch–Jennings (abstract) | Clearing, exercise, assignment and margin constraining fragmentation unchecked (no OCC or exchange rule read); "dominated by cross-contract risk" dropped as unmeasured |
| *Market-Maker-Centric Liquidity* (mechanism) | `res:option-market-maker-spreads` (who supplies quotes); `mech:options-retail-wholesaler-routing` (new) | Bryzgalova–Pavlova–Sikorskaya pp. 2, 11; Muravyev–Pearson (abstract) | Split; "buy-side traders typically consume liquidity" and its explanation not adopted |
| *Options Liquidity Segmentation* (taxonomy) | items iii–iv `res:option-market-maker-spreads`; items i, ii, v `meth:option-spread-measurement` (new); stub `def:option-complex-orders` | Bryzgalova–Pavlova–Sikorskaya Table I, pp. 15–16 (page images), pp. 12, 14, 17; Jameson–Wilhelm, Huh–Lin–Mello (abstracts) | Split; ATM "deepest" supported only as trade share and percentage quoted spread, not depth; "reduces size" and complex orders unchecked |

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

Source checking, not study; the pathway's checkpoint was not attempted.

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

### Findings on the earlier notes

| Earlier block | Entry | Checked sources | Disposition |
|---|---|---|---|
| *Fixed-Income Instrument Range* (taxonomy) | `def:fixed-income-market-structure` (new); stub `ev:credit-derivative-swap-trading-structure` | BSV pp. 1–5, 7–8, 11, 13–16, 30, 32 | Items i–ii rewritten for U.S. Treasuries and corporate bonds (Treasury electronic share is interdealer); structured products and municipals added from the survey; items iii–iv (CDS indices against bespoke, swaps dealer-mediated) unchecked |
| *RFQ Dominance* (principle) | `def:fixed-income-market-structure` | BSV pp. 2–3, 7–8, 37–38; Hendershott–Madhavan and O'Hara–Zhou (abstracts) | Protocols, venues and risk-bearing separated; "dominance" not supported (19 percent electronic in U.S. IG corporates, 2016); the "because" not adopted |
| *Dealer Balance Sheet as Venue* (mechanism) | `def:fixed-income-market-structure` (Practice) | BSV pp. 4, 32–33 | Treated as a metaphor; reduced capital commitment, prearranged trades, nonbank dealers and the regulatory links as the survey states them |
| *TRACE and Post-Trade Transparency* (market rule) | `rule:us-eu-bond-transparency` (new); `ev:bond-transparency-trading-costs` ("improving") | FINRA Rules 6730, 6750 and filing pages (2026-10-15); BSV Table 2, pp. 8–10, 29–30; ESMA statement (10 Oct 2025) and manual (12 May 2026) | Reporting and dissemination separated; history, current text and the one-minute change and its supersession dated; EU post-trade deferrals from 2 March 2026; the European "aim" and U.K. regime unchecked; stubs `rule:eu-mifir-bond-transparency-level1`, `rule:uk-bond-transparency` |
| *Pre-Trade Transparency Limits* (caveat) | `ev:bond-transparency-trading-costs` (Conditions, Pitfalls) | BSV pp. 29, 37–39 | Kept as dealers' argument, a model prediction (Back–Liu–Teguia, as reported) and an open question; not adopted as a finding |
| *Data Changes the Market* (practitioner note) | `ev:bond-transparency-trading-costs` (Practice); `def:fixed-income-market-structure` (Conditions) | BSV pp. 7–10, 31–32; O'Hara–Zhou (abstract) | Split; data sources and missing 605/606 analogue stated; electronification effects only as O'Hara and Zhou's abstract reports them, not causally; desk governance unchecked |

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

Source checking, not study; no checkpoint was attempted.

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

### Findings on the earlier notes

| Earlier block | Entry | Checked sources | Disposition |
|---|---|---|---|
| *Street Name* (definition) | `def:street-name-beneficial-ownership` (new) | Harris pp. 148, 169–170 | Rewritten; registration, beneficial ownership, custody and permission to lend separated |
| *Securities Lending* (mechanism) | `mech:securities-lending-short-sale` (new) | DGP sec. 2, pp. 5–8; ICMA FAQ 13; ISLA pp. 2–3, 24–25; 17 CFR 242.203(b), 242.204(a); Harris pp. 155, 158 | Rewritten; locate, borrow, delivery, recall, replacement borrow, buy-in; Regulation SHO as current U.S. law, ISLA as practice |
| *Borrow Availability Segmentation* (taxonomy) | items i–ii `def:securities-lending-fee-rebate` (new); items iii–iv `mech:securities-lending-short-sale` | Harris pp. 156–158; DGP pp. 6–8; Regulation SHO | Split; recall and settlement risk reclassified as operational risks; "failed locate" separated from delivery failure |
| *Short Interest Rebate* (definition) | `def:securities-lending-fee-rebate` | ICMA FAQ 13; DGP p. 7; ISLA pp. 7–8; Harris pp. 155–157 | Corrected: cash collateral passes from the borrower (often the broker) to the lender; customer margin separated; negative rebates not exemplified in sources |
| *Synthetic Short* (principle) | `res:synthetic-short-put-call` (new) | Harris p. 157; Hu–Black p. 5, fn. 6; own derivation and numerical check | Payoff, initial value with dividends, short forward against short stock, American exercise and assignment; "can replace scarce borrow" qualified, not adopted |
| *Voting and Beneficial Ownership* (caveat) | `def:street-name-beneficial-ownership` (Conditions, Practice, Pitfalls); stub `ev:empty-voting-equity-derivatives` (`synthetic-equity-cfd-trs`) | Harris p. 169; ICMA FAQ 13; DGP p. 8; Hu–Black pp. 1, 5 | Kept as Harris's description of broker voting; record holders vote; no duplicate legal votes; record-date capture through borrowing kept apart from swap-based decoupling |

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

### For review

- The synthetic-short entry's reliance on an own derivation in place of Hull.
- The four backlog stubs.

## securities lending and synthetic shorts review follow-up: corrections, 15 October 2026

Targeted corrections to two securities lending and synthetic shorts review entries; the securities lending and synthetic shorts review record above is left as written, including its numerical-check paragraph, which this record supersedes for the short-sale comparison.

- `res:synthetic-short-put-call`, bond replication. Harris's sidebar on p. 157, rechecked by page image (PDF p. 170 of the local copy, rendered through PDFKit), says a long put and a short call ``plus a long position in a bond with the same maturity'' are equivalent to a short position in the underlying. With a long bond paying $K$ the terminal payoff is $2K-S_T$. The entry now states the correct replication: long put, short call and a short zero-coupon bond repaying $K$ pay $-S_T$; for a stock with no dividends the initial values agree ($P-C-Ke^{-rT}=-S_0$), so the package is equivalent to short stock; equivalently, long put and short call equal short stock plus a long bond (a short sale with proceeds invested). With dividends, the package less the bond is a terminal claim $-S_T$ worth $-S_0e^{-qT}$, while short stock is worth $-S_0$ and owes the interim dividends. Harris's wording is quoted as printed and the discrepancy recorded. The European payoff identity and dividend-adjusted parity are unchanged.
- `res:synthetic-short-put-call`, short-sale comparison. The securities lending and synthetic shorts review bullet compared the package with a fixed short of $e^{-qT}$ shares and gave it terminal wealth $S_0e^{-qT}e^{r_bT}-S_T$; with the borrower paying dividends that is not the strategy's terminal wealth. The narrow repair uses $q=0$: one share sold short, the whole proceeds held as cash collateral credited at a constant rebate $r_b$ (lending fee implicit in $r_b$, no other fee, no extra margin, no recall), ends with $S_0e^{r_bT}-S_T$; the package, European options priced at frictionless parity and its premium financed or invested at $r$, ends with $S_0e^{rT}-S_T$. The existing $q=2\%$ Black–Scholes parity example is kept and labelled separately.
- `mech:securities-lending-short-sale`: ``so someone must lend them'' replaced by the standard stock-loan route for delivery at settlement, with two cases where no loan is needed: delivery from securities held in street name for other clients (Harris, p. 155) and Regulation SHO's exception for sales of securities the seller is deemed to own (17 CFR 242.203(b)(2)(ii)).
- **Numerical checks**, added as `notes/artefacts/synthetic-equity-cfd-trs/synthetic_short_checks.py` (standard library). (1) Payoffs leg by leg at $S_T=60, 95, 100, 140$: put minus call $=K-S_T$; with a short bond $=-S_T$; with a long bond $=2K-S_T$ (130, 95, 90, 50). (2) Parity example $S_0=100$, $K=95$, $r=5\%$, $q=2\%$, $\sigma=25\%$, $T=1$: options repriced by midpoint integration over the risk-neutral density, $C=13.684728$, $P=6.031656$, matching the closed forms to $10^{-4}$, and $P-C=-7.653072=Ke^{-rT}-S_0e^{-qT}=e^{-rT}(K-F)$ with $F=103.0455$. (3) Rebate comparison, $q=0$, same $S_0$, $K$, $r$, $\sigma$, $T$: $C=15.0471$, $P=5.4138$, $P-C=-9.6332$; day-by-day accounts give the package $S_0e^{rT}-S_T$ (5.127110 at $S_T=100$) and the short sale $S_0e^{r_bT}-S_T$ (5.127110, 3.045453, $-0.995017$ for $r_b=5\%, 3\%, -1\%$), gaps $S_0(e^{rT}-e^{r_bT})=0$, 2.081656, 6.122126 at every $S_T$. All checks passed.
- The pathway note for `synthetic-equity-cfd-trs`, the `alpha-harris` reading note and the log were updated. Ownership, stubs and counts are unchanged.

## securities lending and synthetic shorts review second follow-up: lending opening, 15 October 2026

`mech:securities-lending-short-sale` now opens with the standard stock-loan route only: a short seller sells securities it does not own and borrows them to meet delivery at settlement. The examples added in the first follow-up, delivery from other clients' street-name holdings (Harris, p. 155) and Regulation SHO's deemed-to-own locate exception (§ 242.203(b)(2)(ii)), were removed as explanations of why a loan is unnecessary: delivering another customer's street-name securities does not show that no lending occurs, and a locate exemption is a separate regulatory question. The Regulation SHO conditions stay in the entry's Conditions. The synthetic-short mathematics and `synthetic_short_checks.py` are unchanged and still pass. The first follow-up record above is left as written.

## crypto market structure review: crypto market microstructure, 15 October 2026

Source checking, not study; no checkpoint was attempted.

### Sources, 2026-10-15 (generic request headers)

- **Makarov and Schoar** (`s6-makarov`), LSE FMG Discussion Paper 782, 15 December 2018, from fmg.ac.uk: abstract and pp. 1–3 with footnotes 1–3, text layer (printed page = PDF − 2). The published JFE version was not read.
- **Ackerer, Hugonnier and Jermann** (`roadmap-perpetual-pricing`), arXiv 2310.11771v2, 3 September 2024: abstract and pp. 2–4, 7–8 (eqs. (4)–(7)) and 12 (Corollary 1), text layer (printed page = PDF page). The Mathematical Finance version was not read.
- **He, Manela, Ross and von Wachter** (`roadmap-perpetual-fundamentals`), arXiv 2212.06888v7, 17 September 2026: abstract and title page only (one author's eToro affiliation disclosed there).
- **Deribit** (`gapclose-deribit-rules`): Exchange Rulebook version 2.0, applicable 13 August 2026 (article updated 15 September 2026), and Funding Specifications (edited 27 July 2026, updated 20 August 2026), retrieved through the help-centre JSON API because the web pages returned a bot check. Rulebook locators are rule numbers (no page numbers); the funding cap table was read from the article's HTML table. Exchange Membership Terms, option and portfolio-margin pages not read.
- **Not available or not read:** the BIS carry paper (`roadmap-carry`; the PDF URL returned an HTML page), Gornall–Rinaldi–Xiao (`s11-r15`; SSRN), the `crypto-mm-microstructure` readings (none supports these claims), `s11-r29` venue API documentation, and any AMM, stablecoin or bridge source.

### Distinctions kept

- **Evidence, rules and interpretation.** Makarov–Schoar's 2017–2018 findings; Deribit's October 2026 rules for one venue; Ackerer–Hugonnier–Jermann's and He et al.'s model results; interpretation labelled.
- **Prices.** Executable venue prices, reference indices (Deribit Index, Mark Price), fair-value models and legal best-execution obligations.
- **Instruments and contracts.** Spot, dated futures, perpetuals, options and AMM pools (the last unchecked); linear, inverse and quanto contracts.
- **Funding.** Premium against interest terms; sign convention; continuous accrual against the 8-hour quotation; settlement currency and units; damper and caps by currency; equity against cash at the 08:00 UTC settlement.
- **Risk layers.** Liquidation, insurance fund, socialised loss, auto-deleveraging and custody (Deribit), kept apart from venue insolvency and from stablecoin, network and bridge risk (unchecked).

### Numerical check

`notes/artefacts/crypto-mm-microstructure/funding_checks.py` (standard library): Deribit's printed max/min funding formula agrees with an independent piecewise reading of its prose rule at every premium from −10% to +10% in 0.005% steps, for each cap; all of Deribit's worked examples recompute (BTC 0.05% per 8 hours, 0.000001041667 BTC per minute and 0.0005 BTC per 8 hours for 1 BTC; ETH 0.075%, 0.0000015625 and 0.00075 ETH; SOL_USDC 0.075%, 0.15625 and 75 USDC on USDC 100,000; offsetting minutes net to zero; damper examples zero; caps 0.5%, 1.0% and 5.0% binding; ETH uncapped 1.975%); and funding between long and short nets to zero. The page's slips (ETH Example 3 "Index remains at USD 10,000" and "1 BTC long position"; 7.5% inside the ETH formula of Example 5) do not change its stated results. All checks passed.

### Findings on the earlier notes

| Earlier block | Entry | Checked sources | Disposition |
|---|---|---|---|
| *Crypto Liquidity Is Exchange-Fragmented* (principle) | `def:crypto-venue-instrument-structure` (new) | Makarov–Schoar DP 782, abstract, pp. 1–3; Deribit Rulebook v2.0 | Rewritten; executable prices, reference prices, fair value and legal best execution separated; 2017–2018 evidence dated; "fair value is venue-dependent" and the consolidated-tape claim not adopted |
| *Crypto Instrument Segmentation* (taxonomy) | `def:crypto-venue-instrument-structure`; perpetual item to `mech:perpetual-funding`; stubs `def:crypto-options-venue-structure`, `def:amm-pool-mechanics` | Ackerer–Hugonnier–Jermann arXiv v2, pp. 2–3, 7; Deribit Rulebook Rules 1.2, 11.3, App. A | Spot, dated futures, perpetuals (linear, inverse, quanto) and Deribit's options checked; "kept near spot" qualified; options concentration and pool mechanics unchecked |
| *Perpetual Funding* (definition) | `mech:perpetual-funding` (new); stub `ev:crypto-funding-crowding` | AHJ pp. 2, 4, 7–8, 12; He et al. v7 abstract; Deribit Funding Specifications; Rule 11.4 | Sign convention confirmed (Deribit); anchoring a model result, not guaranteed; one venue's damper, caps, accrual and settlement; "crowding signal" unsupported |
| *Crypto Microstructure Risk Segmentation* (taxonomy) | `def:crypto-trading-risk-layers` (new); stub `ev:stablecoin-network-settlement-risk` | Deribit Rulebook Rules 1.1, 2, 10.1–10.11, definitions | Liquidation, insurance fund, socialised loss, ADL and custody for Deribit only; insolvency, outages, withdrawal halts, stablecoin and bridge risk unchecked; fragmentation moved to block 1's entry |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s6-makarov` | abstract; pp. 1–3 | 2018 discussion paper; 2017–2018 data |
| `roadmap-perpetual-pricing` | abstract; pp. 2–4, 7–8, 12 | Preprint; frictionless model |
| `roadmap-perpetual-fundamentals` | abstract | Body unread |
| `gapclose-deribit-rules` | Rulebook rules and definitions; Funding Specifications | One venue; October 2026; Membership Terms unread |
| `roadmap-carry`, `s11-r15`, AMM, stablecoin, bridge | none | Not retrieved or not in scope; stubs |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The five backlog stubs, three of which name other pathways.

## crypto market structure review follow-up: socialised-loss trigger, 15 October 2026

A narrow correction to one item of `def:crypto-trading-risk-layers`; the crypto market structure review record above is left as written.

- **Source rechecked.** Deribit FZE Exchange Rulebook version 2.0, applicable 13 August 2026 (help-centre article updated and edited 15 September 2026, unchanged since crypto market structure review), retrieved again on 15 October 2026 through the help-centre JSON API: Rules 10.6–10.11 with their guidance notes, and Rules 9.16–9.17 for comparison.
- **Finding.** crypto market structure review wrote that socialised loss applies "if the fund is depleted". Rule 10.8 has two branches: the insurance fund is depleted in all currencies, **or** it is depleted in the bankrupt account's currency and Deribit decides not to convert other currencies. In either case Deribit "may, in its absolute discretion" trigger the mechanism. Converting another currency of the fund under Rule 10.7 is also at its absolute discretion. Socialised loss can therefore be triggered while other currencies remain in the fund, and is not automatic when the fund is exhausted.
- **Changed.** The *socialised loss* item now states both branches and both discretions (Rule 10.8), with the deductions, halts, cancellations and mark-price closes cited to Rules 10.9–10.11 rather than 10.8–10.11. It also records "the same day's session" and "in any currency" as Rule 10.9(a) words them. The *insurance fund* item now says that conversion is discretionary and applies when the fund in the account's currency is depleted. The entry's status records the recheck; verification stays *partly checked*, stability *draft*, currency *Deribit as of October 2026*.
- **Notes.** The `gapclose-deribit-rules` reading note records the two-branch trigger. It also notes that Rule 9.17 applies the same trigger to a short spot under cross-collateral margin, read but not used in an entry. The `crypto-perpetuals` pathway note records the correction. No other entry, stub, ownership or count changed; `funding_checks.py` is unaffected and was not rerun.

## backtest evaluation review: research and backtest evaluation, 15 October 2026

Source checking, not study; no checkpoint was attempted, and no reading of the owning pathway was read.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box: A Simple Guide to Systematic Investing*, third edition, Wiley 2024 (ISBN 9781119931911), local PDF outside the repository, read through PDFKit's text layer: chap. "Research", secs. 9.1–9.4, pp. 161–187 (printed page = PDF page − 20). Exhibits 9.2 (p. 171), 9.3 (p. 172) and 9.5 (p. 178) were read from page images. The catalogue's entry carries the first edition's subtitle and leaves the edition unestablished; no route lists the key. Which edition the earlier notes followed is not recorded (open question in `log.md`).
- **Not read:** every reading of `backtest-inference`; `wide-campbell-thompson`, `s7-welch` and the crowding papers named in stubs; standard definitions of the information, Sterling and Omega ratios. Regulation SHO was not rechecked: the comparison uses the text already cited in `mech:securities-lending-short-sale` (eCFR, 13 October 2026).

### Findings

- **Text–figure mismatch, p. 172.** The text gives the two most bearish quintiles average next-day returns of −2.35% and −0.19%. In Exhibit 9.3 these are the signal-bucket labels, and the bars run from about −0.03% to +0.13% (page image). The monotonic ordering holds in the figure.
- **Arithmetic.** Recomputed in the session, with no script kept: IR 12.1/21.2 = 0.571, Calmar 12.1/39.7 = 0.305, drawdown example 1.10 × 0.85 × 1.15 − 1 = +7.5%, 19/35 = 54.3% of non-zero days won, cost example +$0.10 to −$0.90 per 100 shares, and 746% and 870% over 18.6 years giving 12.2% and 13.0% a year (Narang 12.1% and 12.9%). All consistent within rounding and the period's endpoints.
- **Dropped conditions.** The earlier notes dropped conditions that change the meaning: "for a given level of returns" (item iii), deduction and falsification (block 1), and the advice on which way to err (block 4).

### Findings on the earlier notes

| Earlier block | Entry | Checked source (`s7-narang`, 3rd ed.) | Disposition |
|---|---|---|---|
| *Scientific Method* (definition) | `meth:hypothesis-driven-strategy-research` (new) | sec. 9.1, pp. 161–163 | Rewritten; Narang's deduction of consequences and falsification restored, missing from the earlier notes' three steps; ongoing research added |
| *Sources of Alpha Idea Generation* (remark) | merged into `meth:hypothesis-driven-strategy-research` | sec. 9.2, pp. 163–165 | Merged; four sources match; Narang's caveat on discretionary patterns added; source of an idea not evidence (interpretation) |
| *Model Quality Assessment* (remark), items i–ix | `meth:backtest-evaluation-diagnostics` (new); stubs | secs. 9.3.2.1–9.3.2.9, pp. 168–176; Exhibits 9.2–9.3 by page image | Rewritten with qualifications (subclaims below) |
| same block, items x–xi | `pit:parameter-overfitting` (new); stubs | secs. 9.3.2.10–9.3.4, pp. 176–185; Exhibit 9.5 by page image | Rewritten; underfitting balance added; "flatter curve" corrected |
| *Other Considerations in Model Testing* (remark) | `pit:backtest-cost-short-assumptions` (new); stub `data:historical-borrow-availability` | sec. 9.3.5, pp. 185–186 | Rewritten; cost asymmetry matches; "naked short … illegal" not adopted; borrow fees and recall linked as interpretation |

**Subclaims of block 3.**

| Item | Earlier claim | Disposition |
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

**Subclaims of block 4.** Overestimated costs mean holding too long and underestimated costs mean too much turnover and bleed (p. 186): rewritten. Narang's advice to err high, and his 55/45 example, were added and the example recomputed. Short availability and hard-to-borrow lists (p. 186): rewritten. Narang's "naked short sale, which is illegal in the United States" is broader than Regulation SHO as cited in `mech:securities-lending-short-sale` and was not adopted. His remark that historical hard-to-borrow data are hard to obtain was stubbed (`data:historical-borrow-availability`). Borrow fees and recall are not in Narang or the earlier notes; they are linked to `def:securities-lending-fee-rebate` and `mech:securities-lending-short-sale` as interpretation. No subclaim was deleted outright.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. "Research", pp. 161–187; Exhibits 9.2, 9.3, 9.5 as images | Third edition; the edition of the earlier notes and of the catalogue unknown; one practitioner's account; the example strategy is in-sample and untraded |
| `backtest-inference` readings, return-predictability and crowding papers | none | Stubs only |

The four new entries are *partly checked 2026-10-15*, *draft*, current as of 2024; **human review is outstanding**.

### For review

- Citing the third edition while the catalogue leaves the edition open.
- The qualifications to Narang's heuristics: smooth P&L, lower volatility, the R² of 0.05, time decay as crowding, and parameter stability as evidence against overfitting.

## backtest evaluation review follow-up: corrections, 15 October 2026

Narrow corrections after an audit of backtest evaluation review; the backtest evaluation review record above is left as written, and this record supersedes it where they differ.

- **S&P example, `meth:backtest-evaluation-diagnostics`.** backtest evaluation review described the strategy as "long when the index's earnings yield exceeds the 10-year Treasury yield and short otherwise", which leaves out its no-trade state. Narang (third edition) p. 168 reads a higher stock yield as a signal to be long and a lower one as a signal to be short, as "an adjustment to" the equity risk premium. P. 173 says the strategy signals "only when the model perceives that the opportunity is sufficiently attractive to warrant trading at all" and is at zero 65% of the time. The entry now gives both, and says that the adjustment and the threshold are not stated; no threshold was supplied.
- **Ratio signs, same entry.** Narang defines Calmar as average return divided by the worst drawdown and Omega as the sum of positive returns divided by the sum of negative returns, both of which have negative denominators taken literally. He reports both as positive (0.31 and 1.26, pp. 173–174). The entry now quotes his wording and sets out, as interpretation, the explicit conventions Calmar $=\bar R/\lvert\mathrm{MDD}\rvert$ and $\Omega(0)=\sum\max(R_t,0)/\lvert\sum\min(R_t,0)\rvert$. Hand-check, in the session with no script kept: $12.1/\lvert-39.7\rvert=0.305$ against $-0.305$ taken literally; returns $+2,+1,-1.5,-0.5$ give $\Omega(0)=3/2=1.5$ against $-1.5$. His Sterling and Omega values were not recomputed, since the strategy's returns are not available.
- **Item count.** The backtest evaluation review's preservation check (since removed from these records) said "all 21 items are present". The 21 counted the substring `\item`, which also matches the three `\setlength{\itemsep}{0pt}` lines. The original has 18 `\item` commands: 3 in *Scientific Method*, 4 in *Sources of Alpha Idea Generation*, 11 in *Model Quality Assessment* and none in *Other Considerations in Model Testing*. Recounted against `9148410:…/sysinv/research.tex` with a pattern that excludes `\itemsep`; all 18 and the three `\itemsep` lines appear in the artefact. No text was lost.
- **Guidance after the record split.** `compendium/README.md` now points dispositions and checks to `source-review-records.md` (its opening paragraph and entry disposition instructions). In `source-review-index.md` the progress table's "checks table below" now points to the topic review *Checks and their limits*, and the backtest evaluation review index row now gives its commit `c45e2b5`. Historical slice narratives that mention `source-review-index.md` were not changed.
- **Notes.** The `s7-narang` reading note and the `backtest-inference` pathway note record the corrections. Entries, stubs, ownership and counts are unchanged.

## model risk and contagion review: risk assessment (model risk, regime change, shocks, contagion, monitoring), 15 October 2026

Source checking, not study; no checkpoint was attempted, and no reading of either owning pathway was read.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), *Inside the Black Box*, third edition, Wiley 2024, the same local copy as backtest evaluation review (text layer through PDFKit; printed page = PDF page − 20). Chap. 10, "Risks Inherent to Quant Strategies", secs. 10.1–10.6, pp. 191–211, was verified to exist in this edition from the contents (pp. 191–211) and the running heads. Exhibit 10.6 (p. 206) was read by page image; Exhibits 10.1–10.5 were read from the text layer only.
- **Not read:** every reading of `model-governance-controls` and `funding-crowding`, including the Knight Capital order and Khandani and Lo; the AXA Rosenberg order (not catalogued); `risk-parity-vol-targeting` readings.

### Findings and arithmetic

- **Pulte Homes, Exhibit 10.6.** −22.0%, −12.5%, +15.6%, −22.6%, with average daily volume 3.5, 7.2, 10.4 and 5.7 million shares. The two declines compound to 1 − 0.78 × 0.875 = 31.75%. The +15.6% rebound brings the price from 0.6825 to 0.789 of its 31 May level, recovering (0.789 − 0.6825)/0.3175 = 33.6% of the lost price (38% in logs), not "about half". Narang counts the decline over 44 days and the rebound over 4: the rate is about 3.7 times the earlier pace by share of lost ground, or 5.4 times by percentage points per day (15.6/4 against 31.75/44), not "about 20 times". Volume rose 106% and then 44%, matching his "100 percent" and "50 percent".
- **His other pace claims check out.** Value–growth: half the loss in 16 days against 160 gives 5 times (his "five times"); 40% in 6 days against 115 gives 7.7 times (his "almost eight").
- **Leverage arithmetic.** 4 × 1.5 = 6 and 4 × 2 = 8 gross, matching his "six or eight".
- All recomputed in the session; no script kept, and no existing numerical script covers this content.

### Findings on the earlier notes

| Earlier block | Entry | Checked source (`s7-narang`, 3rd ed., chap. "Risks Inherent to Quant Strategies") | Disposition |
|---|---|---|---|
| *Model Risks* (definition) | `def:quant-strategy-risk-sources` (new) | sec. 10.1, pp. 191–196 | Rewritten |
| *Regime Change Risk* (definition) | merged into `def:quant-strategy-risk-sources` | sec. 10.2, pp. 196–200 | Merged |
| *Exogenous Shock Risk* (definition) | merged into `def:quant-strategy-risk-sources`; stub `meth:discretionary-override-governance` | sec. 10.3, pp. 200–202 | Merged; overrides qualified |
| *Contagion Risk* (definition) | `def:common-investor-contagion` (new); stubs `ev:august-2007-quant-unwind`, `mod:margin-liquidity-spiral`, `mod:volatility-targeting-deleveraging`, `meth:overlap-crowding-measure` | sec. 10.4, pp. 202–209; Exhibit 10.6 by page image | Rewritten; 2007 drivers kept as practitioner explanation |
| *Risk Monitoring Methods* (method) | `meth:quant-strategy-monitoring` (new) | sec. 10.5, pp. 209–210 | Rewritten; execution indicators left to `meth:execution-decision-support` |

**Substantive claims.**

| Block | Earlier claim | Disposition |
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
| 4 | (Narang, not the earlier notes) losses "solely the result of market impact"; Pulte Homes illustration | Reported as his claims, qualified by the arithmetic below and the square-root impact entry |
| 5 | Exposure, P&L (hit rate), execution, systems monitors | Rewritten (pp. 209–210); VaR measure, "how money is made" monitors and early-warning purpose added; execution-algorithm indicators cross-referenced, not duplicated |

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. "Risks Inherent to Quant Strategies", pp. 191–211; Exhibit 10.6 as image | Third edition; one practitioner's account; company and episode figures unsourced in the chapter; 2007 drivers are his inferences |
| Pathway readings (`exp-khandani-lo-quant-meltdown`, `wide-knight-capital`, `s8-governance` and others) | none | Stubs only |

The three new entries are *partly checked 2026-10-15*, *draft*, current as of 2024; **human review is outstanding**.

### For review

- Presenting Narang's 2007 drivers as his explanation, and the Pulte Homes arithmetic against his text.
- The qualification of discretionary overrides, and implementation failure treated as operational rather than model risk.

## model risk and contagion review follow-up: overrides, impact inference and the Calmar ratio, 15 October 2026

Narrow corrections to backtest evaluation / model risk and contagion reviews after an audit, run before transaction-cost models review; the records above are left as written, and this record supersedes them where they differ. The passages were reread in the same local third edition of `s7-narang` (text layer; printed page = PDF page − 20).

- **Overrides, `def:quant-strategy-risk-sources`** (`compendium/research-engineering-validation/strategy-risk.tex`). model risk and contagion review wrote that "an override is itself an unvalidated change to the model". The entry now separates an ad hoc intervention, improvised outside the validated design and in effect an untested model change, from an approved contingency response (a pre-specified de-risking rule, limit or kill switch whose triggers, authority and effects were tested and approved), which is part of the validated design. Narang's p. 208 account and the one-firm anecdote are unchanged. Operational failure is now said to be made less likely and less costly by testing, change control and operational controls, which mitigate it rather than guarantee its prevention. The five causes are presented as overlapping questions (a regime change can expose a misspecification; others' forced selling can look like a regime change; one loss can have several causes), not exclusive categories. The `model-governance-controls` pathway note records the change.
- **Pulte Homes and impact, `def:common-investor-contagion`** (`compendium/portfolio-risk-financing/crowding-contagion.tex`). model risk and contagion review set Narang's "quadratic nature of market impact" (p. 206) against the square-root law as if the table contradicted it. That inference is withdrawn: average daily volume and returns over crisis sub-periods give no metaorder sizes or schedules, mix many traders' flow, and do not reveal the price without the liquidation, so they identify no metaorder impact exponent, quadratic or square-root. The checked arithmetic (31.75% fall, about a third recovered, 3.7–5.4 times the earlier pace) and the separation of Narang's account from causal evidence are kept; his unsourced "as much as 15 percent in market impact" is now noted. The `funding-crowding` note and the `s7-narang` reading note record the change; the dated open question in `log.md` is left as written, with a new dated line withdrawing its impact clause.
- **Calmar ratio, `meth:backtest-evaluation-diagnostics`** (`compendium/research-engineering-validation/backtest-evaluation.tex`). $12.1/39.7=0.30479$, which rounds to 0.30, while Narang reports 0.31 on pp. 173 and 174. The entry no longer says "as reported" after 0.30, and its *Practice* now says that most example figures agree within rounding, with the Calmar ratio the unexplained exception. No explanation was supplied. The backtest evaluation review *Findings* line "all consistent within rounding" is superseded for this ratio. Recomputed in the session: $12.1/39.7=0.3048$, $12.1/21.2=0.5708$, $19/35=0.5429$.
- **Index.** The model risk and contagion review row in `notes/source-review-index.md` now gives its commit `e0451c9`.

## transaction-cost models review: transaction cost models (components and cost functions), 15 October 2026

Source checking, not study; no checkpoint was attempted, and no reading of either owning pathway was read.

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

### Findings on the earlier notes

| Part | Earlier text | Entry | Checked source (`s7-narang`, 3rd ed., chap. 5) | Disposition |
|---|---|---|---|---|
| Intro | Two reasons to trade; benefit above cost; the model informs, does not minimise | `mod:portfolio-transaction-cost-function` (new), Statement and Practice | pp. 85–86, 96 | Rewritten; Narang's framing kept as his; joint optimisation and forced trades added as interpretation |
| 1 | *Transaction Cost Components* (remark), items i–iii | merged into `def:transaction-costs` (Statement; Pitfalls, "Narang's terms") | sec. 5.1, pp. 86–91; `exp-pfmi` paras 1.12–1.13 | Merged with corrections (subclaims below) |
| 2 | *Types of Transaction Cost Models* (definition), items i–iv | `mod:portfolio-transaction-cost-function` (new); stubs `meth:convex-cost-portfolio-optimisation`, `res:no-trade-region` | sec. 5.2–5.3 and n. 2, pp. 91–97; Exhibits 5.1–5.4 and n. 2 by page image | Rewritten; rankings not adopted (subclaims below) |

**Subclaims.**

| Where | Earlier claim | Disposition |
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

**Units and conventions** (all in `mod:portfolio-transaction-cost-function`): total cost $C(q)$ in currency against signed size $q$; per-unit cost $C/\lvert q\rvert$ in currency per share or basis points. A quadratic total is a linear per-unit cost; square-root per-unit cost is a 3/2-power total. Narang's note 2, "cost per share scales with an exponent of 1.5, or in other words, as the square root of trade size" (p. 97), conflates the two conventions; recorded, not repeated.

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. 5, pp. 85–97; Exhibits 5.1–5.4, 5.5 and n. 2 as images | Third edition; one practitioner's account; exhibits schematic with no data; the 20–50 percent cost share, the "generally accepted" quadratic, the GOOG statistic, the 2019 dark-pool share and the square-root evidence in n. 2 are unsourced or cited only to a newspaper, not checked |
| `exp-pfmi` | paras. 1.8–1.13, pp. 7–9 | Only the first 18 PDF pages could be read; no glossary; 2012 text |
| `portfolio-construction` and `price-impact-execution` readings | none | Stubs and cross-references only; the computational remarks are interpretation |

The new entry and the merged paragraph are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The mapping of Narang's slippage and impact onto the delay and trading-related terms, and the correction of "unknown until the trade has been completed".
- The interpretation on computational cost (convex piecewise-linear, quadratic, 3/2-power, integer variables for per-trade fixed costs), which no source read supports and which the `meth:convex-cost-portfolio-optimisation` stub should replace.
- Clearing left undefined pending the CPMI glossary (`def:clearing-settlement`).

## transaction-cost models review follow-up: units, cost-function conditions and the sell example, 15 October 2026

Narrow corrections to transaction-cost models review after an audit, run before portfolio construction review; the transaction-cost models review record above is left as written, and this record supersedes it where they differ.

- **Units, `mod:portfolio-transaction-cost-function`** (`compendium/portfolio-construction-risk/transaction-cost-models.tex`). transaction-cost models review let $q$ be shares, "contracts, or currency" while giving coefficients per share. The notation is now for one equity: $q$ and $V$ in shares, $P$ in currency per share, coefficients in currency, currency per share or currency per share squared, and $\eta$ dimensionless. The per-share cost $c(q)=C(q)/\lvert q\rvert$ is defined only for $q\neq0$. Contracts or notional are said to need their own units (such as a multiplier), not the same conversions. "Per-unit" became "per-share" where it meant that.
- **Parameter conditions.** All coefficients are nonnegative and every form has $C(0)=0$, $C\ge0$ and depends only on $\lvert q\rvert$. The displayed $\max_i(b_i\lvert q\rvert-d_i)$ with increasing slopes alone did not guarantee this: slopes 0.01, 0.03 with intercepts $-5$, 200 give $C(0)=5$, and with 5, 200 give $C(0)=-5$. The entry now uses the convex hinge form $b_0\lvert q\rvert+\sum_ih_i(\lvert q\rvert-\kappa_i)_+$ with $0<\kappa_1<\dots$, and states the equivalent maximum of lines with slopes $s_j=b_0+\sum_{i\le j}h_i$ and intercepts $d_j=\sum_{i\le j}h_i\kappa_i$. The 3/2-power form $\eta P\lvert q\rvert(\lvert q\rvert/V)^{1/2}$ is written out, and the assumptions are stated: symmetric between buys and sales, nonnegative (no rebates or favourable drift), expected rather than realised, one instrument and period, independent of duration and other trades.
- **Checks**, exact fractions in the session (no script kept): for $b_0=0.01$, $h=(0.02,0.05)$, $\kappa=(10{,}000,50{,}000)$, $C=0$ at 0 and 50, 100, 700, 1,300, 2,100 at $\lvert q\rvert=$ 5,000, 10,000, 30,000, 50,000, 60,000, equal for $\pm q$; left and right values at each breakpoint differ by under $10^{-7}$; equal to the maximum of lines (0.01, 0), (0.03, 200), (0.08, 2,700) at every point tested. The illustration with $\eta=0.01$, $P=50$, $V=10^6$ still gives \$500 and 10 bp at $\pm$10,000 shares and \$1,414.21 and 14.142 bp at 20,000.
- **Sell example, `def:transaction-costs`** (`compendium/execution-trading-costs/transaction-cost-analysis.tex`). transaction-cost models review said Narang's sale filled at \$100.20 "though the order did not raise the price". That assertion is removed: the example shows a negative arrival-to-fill cost against a benchmark, which does not identify the order's causal effect.
- **Notes and index.** The `portfolio-construction` and `execution-trading-costs` pathway notes record the changes; the transaction-cost models review row in `notes/source-review-index.md` now gives its commit `0224ac7`.

## portfolio construction review: portfolio construction models (rules, mean–variance optimisation, signal portfolios), 15 October 2026

Source checking, not study; no checkpoint was attempted. One of the owning pathway's readings, Boyd et al., was read in part for method mechanics; that is source checking, not study of it.

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

### Findings on the earlier notes

| Part | Earlier text | Entry | Checked source | Disposition |
|---|---|---|---|---|
| Intro | Two families: rule-based heuristics; optimisers with an objective function | `meth:rule-based-position-sizing` (Statement), `mod:mean-variance-portfolio-optimisation` | Narang chap. 6, pp. 99–100 | Rewritten |
| 1 | *Rule-Based Models* (definition), items i–iv | `meth:rule-based-position-sizing` (new); stub `meth:equal-risk-contribution` | secs. 6.1–6.1.4, 6.4, pp. 100–104, 123; Exhibit 6.1 by page image | Rewritten with corrections (subclaims below) |
| 2 | *Optimisers Models Parameters* (remark): prose and items i–iii | `mod:mean-variance-portfolio-optimisation` (new); stubs `meth:portfolio-covariance-estimation`, `mod:garch-volatility-forecast` | sec. 6.2–6.2.1, pp. 104–113; Exhibits 6.2, 6.4, 6.5 by page image; Boyd et al. secs. 1.1, 3.2, 3.4 | Rewritten with corrections |
| 3 | *Optimisation Techniques* (method), items i–vi | `mod:mean-variance-portfolio-optimisation`; `meth:signal-portfolio-allocation` (new); stubs `mod:black-litterman`, `meth:resampled-efficiency` | secs. 6.2.2–6.3, pp. 113–123; Exhibits 6.6, 6.7 and the p. 118 example by page image; Boyd et al. secs. 1.3–1.4, 2.4, 4.3, 5.6 | Rewritten, item vi not adopted |

**Subclaims.**

| Where | Earlier claim | Disposition |
|---|---|---|
| Intro | Rule-based from experience; optimisers use an objective and algorithms | Rewritten (pp. 99–100) |
| 1.i | Equal position: no other information needed; signal strength not used | Rewritten (pp. 100–101), with the implicit homogeneity assumption |
| 1.i | "Assumes sufficient statistical strength … to predict … magnitude"; "few large bets on 'best' forecast, many smaller bets"; adverse selection | **Misplaced in the earlier notes**: these are Narang's two arguments *against unequal* weighting, which equal weighting avoids (pp. 101–102). Restored to that role; bad-data and winsorisation points added |
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

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. 6, pp. 99–125; exhibits listed above as images | Third edition; one practitioner's account; GARCH prevalence, "about 20" factors, the users of each method, and the decision-tree details absent; some text–exhibit inconsistencies (Exhibit 6.1 labels; "high correlation" on p. 115 against about 0.1 on p. 106) |
| `wide-boyd-markowitz-seventy` | the sections listed | Authors' version, not the journal; one paper's view of the alleged deficiencies; timings are for one solver and hardware |
| Black–Litterman, Michaud, Grinold–Kahn, ERC, GARCH and covariance readings | none | Stubs; claims about them are limited to what Narang and Boyd et al. say |

The three new entries are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- The reading of Exhibit 6.1 as inverse-variance and the ERC distinction.
- The correction of the unconstrained single-asset claim, and the treatment of Black–Litterman and resampling on Narang's and Boyd et al.'s accounts alone.
- Keeping Grinold and Kahn's approach as a separate entry on Narang's account only.
- The not-adopted data-mining and decision-tree details, which may come from an earlier edition.

## portfolio construction review follow-up: closed-form conditions, permutations, learning and rounding, 15 October 2026

Narrow corrections to portfolio construction review after an audit, run before risk models review; the portfolio construction review record above is left as written, and this record supersedes it where they differ.

- **Closed form, `mod:mean-variance-portfolio-optimisation`.** The entry now states that $w^\star=\tfrac1{2\gamma}\Sigma^{-1}(\mu+\nu^\star\mathbf 1)$ assumes a positive-definite $\Sigma$ and $\gamma>0$, and gives $\nu^\star=(2\gamma-\mathbf 1^\top\Sigma^{-1}\mu)/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$, the budget constraint's dual variable (Boyd et al., p. 4), which shifts all expected returns equally so that the weights sum to one. The volatility-target form is feasible only when $\sigma_{\mathrm{tar}}^2\ge1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$, quoting Boyd et al.'s "can be infeasible when $\sigma^{\mathrm{tar}}$ is too small" (p. 4). A singular $\Sigma$ is said to need separate treatment, with no pseudoinverse by default.
- **Single asset, same entry.** portfolio construction review said a single-asset answer arises "when risk is ignored". The entry now separates the bounded case (budget and no shorting: the highest-return asset) from the unbounded one (shorting allowed, returns not all equal) and box limits.
- **Resampling, same entry.** portfolio construction review said Narang's remark "shows that reordering cannot change the sample means and covariances an optimiser uses". His remark concerns one series. The entry now says that reordering one series keeps its mean and variance, a common permutation of multivariate rows keeps covariances, and independent permutations change them; Michaud's procedure and performance claims remain unchecked.
- **Machine learning, same entry.** "Supervised learning fits a forecast; it does not choose weights" is replaced by a distinction between forecasting, learning allocation weights (possible; its literature not read) and optimisation, keeping the narrower conclusion that the earlier item lacks source support.
- **ERC rounding and positive variance, `meth:rule-based-position-sizing`.** The displayed weights 29.9, 29.9 and 40.2 percent did not match the stored calculation ($b=0.401492$ rounds to 40.1); they now read about 29.93, 29.93 and 40.15 percent with their closed form. Normalised risk contributions are stated to require $w^\top\Sigma w>0$.
- **Transaction-cost entry.** `mod:portfolio-transaction-cost-function`'s *Further reading* and *Status* no longer say that no pathway reading was read; they name the parts of Boyd et al. read in portfolio construction review.
- **Checks**, in the session with numpy (no script kept): for a three-asset positive-definite $\Sigma$ (eigenvalues 0.0219, 0.0374, 0.0932), $\gamma=1$ and $\gamma=5$ give $\nu^\star=-0.0555$ and $0.0562$, weights summing to 1 and first-order residuals below $10^{-16}$; minimum variance 0.01396; with $\gamma=0$ the direction $(1,0,-1)$ raises return by 0.03 per unit with unchanged budget, so the problem is unbounded; two perfectly correlated assets give eigenvalues 0 and 0.08. Permutation: $x=y=(1,2,3,4)$, covariance 1.25; reversing $y$ alone gives $-1.25$ with means 2.5 and variances 1.25 unchanged; a common permutation keeps 1.25. ERC: 29.9254, 29.9254, 40.1492 percent; equal weights give 39.13, 39.13, 21.74 percent at variance 0.02044.
- **Notes and index.** The `portfolio-construction` note records the changes; `log.md` keeps its portfolio construction review line and gains a dated line narrowing it; the portfolio construction review index row gives `4e7666d`.

## risk models review: risk models (factor exposures, limits and penalties), 15 October 2026

Source checking, not study; no checkpoint was attempted. Two further sections of Boyd et al., a reading of the owning pathway, were read for method mechanics.

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

### Findings on the earlier notes

| Part | Earlier text | Entry | Checked source | Disposition |
|---|---|---|---|---|
| Intro | Risk model concerns intentional selection and sizing of exposures; alpha exposure accepted for long-run profit | `mod:factor-risk-model` (Statement, Pitfalls) | Narang chap. 4, pp. 71–73; Exhibit 4.1, p. 83 by page image | Corrected: Narang says this of risk *management*; the risk model is an input to the portfolio decision |
| 1 | *Factor-Based Models* (method), items i–iv | `mod:factor-risk-model` (new) | Boyd et al. sec. 3.3, pp. 20–21; Narang pp. 71–72, 77–78 | Rewritten with the factor covariance and its assumptions; the factor list qualified |
| 2 | *Statistical Models* (method), items i–iii | stub `meth:var-es-estimation-methods` (new note) | none in Narang's chapter | Stubbed, not written as an entry |
| 3 | *Limiting Size of Risk* (method), prose | merged into `mod:mean-variance-portfolio-optimisation` (Practice, Pitfalls) | Narang secs. 4.1–4.1.3, pp. 73–76; Boyd et al. sec. 4.2, pp. 25–27 | Merged with corrections |
| 4 | *Limiting the Types of Risk* (method), items i–ii | `mod:factor-risk-model` (Conditions, Practice, Pitfalls) | Narang secs. 4.2–4.2.3, pp. 76–81 | Rewritten with qualifications |

**Subclaims.**

| Where | Earlier claim | Disposition |
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

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | chap. 4, pp. 71–84; Exhibit 4.1 as image | Third edition; one practitioner's account with no data; his VaR description and dispersion inference not adopted; the earlier factor list and statistical block absent from his chapter |
| `wide-boyd-markowitz-seventy` | secs. 3.3, 4.2 | Authors' version; the factor model stated, not estimated |
| VaR/ES, factor-premia and covariance-estimation readings | none | Stubs; "unintended is not uncompensated" is interpretation |

The new entry and the merged passages are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### For review

- Merging the size-limit material into the mean–variance entry, including the softening reading of penalties and the non-adoption of Narang's VaR and dispersion statements.

## risk models review follow-up: residual diversification, the CVX–XOM hedge and compensation, 15 October 2026

Narrow corrections to risk models review after an audit, run before systematic-investing architecture review; the risk models review record above is left as written, and this record supersedes it where they differ. Narang's p. 76 was reread in the same third-edition copy.

- **Residual diversification, `mod:factor-risk-model`.** risk models review said that "diversification of residual risk depends on the diagonal-$D$ assumption holding". A diagonal $D$ with bounded variances and equal weights is sufficient, not necessary. The entry now keeps the constant-equicorrelation example (correlation 0.2, variance 0.09: $0.018+0.072/n$, a floor of 0.018) and adds a counterexample: correlation 0.2 within disjoint pairs only gives $0.108/n$, which still vanishes. In these examples correlation confined to small groups still diversifies, while correlation shared by every pair leaves a floor, like an omitted factor. Checked with numpy for $n=10$, 100, 1,000 (0.0108, 0.00108, 0.000108; and 0.0252, 0.01872, 0.018072).
- **CVX–XOM, same entry.** "Removed by shorting XOM" is replaced by Narang's "substantially eliminated" (p. 76), with the interpretation that equal dollar positions hedge the market exactly only with equal betas; exact neutrality needs beta-weighted sizes under a stated risk model.
- **Compensation, same entry.** "Narang's rule assumes that exposures the alpha model does not forecast earn nothing" is replaced by his wording, "no expectation of being compensated sufficiently" (p. 76): expected reward not enough for the risk, not zero.
- **Notes and index.** The `portfolio-construction` and `s7-narang` notes record the changes; `log.md` keeps its risk models review line and gains a dated correction; the risk models review index row gives `cd7b13c`.

## systematic-investing architecture review: Narang's systematic-investing cluster (overview and diagram, alpha models, execution), 15 October 2026

A multi-file batch: the last three files of Narang's systematic-investing notes. Source checking, not study; no checkpoint was attempted and no reading of any owning pathway was studied.

### Sources, 2026-10-15

- **Narang** (`s7-narang`), third edition, Wiley 2024, the local copy of backtest evaluation / risk models reviews (text layer; printed page = PDF page − 20). Read: chap. 2, secs. 2.1–2.2, pp. 16–19, Exhibit 2.1 by page image; chap. 3, "Alpha Models: How Quants Make Money", whole, pp. 23–69 (contents: 23; notes 69), Exhibits 3.2, 3.9 and 3.10 by page image; chap. 7, "Execution", whole, pp. 127–141 (contents: 127; notes 141); chap. 14, sec. 14.1.3, p. 270; chap. 15, sec. 15.4, pp. 291–293; Appendix, secs. A.2–A.2.2, pp. 311–315. "Shark" does not occur anywhere in the copy (text search).
- **López de Prado** (`alpha-afml`), *Advances in Financial Machine Learning*, Wiley 2018 (ISBN 9781119482086), local copy, text layer (printed page = PDF page − 27): chap. 1, secs. 1.2.2 and 1.3.1, pp. 5–9. A reading note was opened.
- **7 U.S.C. §6c** (`usc-7-6c`), 2024 edition, GPO via govinfo, retrieved 2026-10-15: paragraph (a)(5). The House Office of the Law Revision Counsel site returned "page not found".
- **FINRA Rule 5270** (`finra-rule-5270`), as displayed on finra.org on 2026-10-15.
- **Not read:** every reading of the overview, `equity-long-short-construction`, `trend-following`, `statistical-arbitrage`, `equity-factor-premia` and `market-structure-execution-quality` named in stubs; the FIX specification (`s6-fix`) and its licence; SEC and FINRA spoofing rules; EU MAR; earlier editions of Narang, from which the earlier notes' cancel-and-replace, ML-HFT and shark passages may come.

### Numerical checks

Recomputed in the session; no script kept and none existing covers this content: Exhibit 2.2 trades (+5, +5, −15, −15 percent); linear blend $0.7\times20+0.3\times(-10)=11$; carry $4.25-2=2.25$; variants $2\times4\times2\times4=64$; the conditional blend gives no signal or $+20$ percent. risk models review follow-up: equicorrelated and disjoint-pair residual variances (above).

### Findings on the earlier notes

| File and block | Entry | Checked source | Disposition |
|---|---|---|---|
| overview: introduction, figure, module list, bridge prose | `def:quant-strategy-components` (new), Figure (redrawn) | Narang chap. 2, pp. 16–19; Exhibit 2.1 by page image | Rewritten; return arrow restored |
| overview: *Chains of Production* (11 items) | `meth:strategy-production-lifecycle` (new); stub `meth:strategy-promotion-criteria` | López de Prado (`alpha-afml`) chap. 1, pp. 5–9 | Rewritten as one author's prescription |
| alpha: introduction, *Theory Driven Models* (5), data-driven paragraph | `def:alpha-model-taxonomy` (new); stubs `ev:trend-following-evidence`, `meth:residual-reversion-strategy`, `ev:value-carry-premia` | Narang chap. 3, secs. 3.1–3.3, pp. 23–52; Exhibit 3.2 by page image | Rewritten; three classes added; claims qualified |
| alpha: *Strategy Parameters* (6) | `meth:alpha-strategy-specification` (new) | sec. 3.4, pp. 52–63 | Rewritten; conditioning variables added |
| alpha: *Blending of Models* items i–ii | `meth:alpha-signal-combination` (new); stubs `meth:forecast-scaling-ic`, `meth:signal-mixing-vs-integration` | sec. 3.5, pp. 64–68; Exhibits 3.9–3.10 by page image | Rewritten; "independence" corrected |
| alpha: *Blending of Models* item iii | merged into `meth:strategy-production-lifecycle` | López de Prado pp. 5–6 | Merged; source corrected (not Narang) |
| execution: introduction | merged into `def:order-exposure-decisions`, `def:portfolio-trading`, `def:automated-trading-architecture` | Narang chap. 7, pp. 127–129 | Merged |
| execution: *Order Execution Algorithm Parameters* (5) | merged into `def:order-exposure-decisions`; stub `rule:spoofing-securities-markets` in `market-structure-execution-quality` | chap. 7, pp. 129–138; chap. 14, p. 270; Appendix pp. 314–315; 7 U.S.C. §6c(a)(5) | Merged; item v kept as an unresolved pitfall |
| execution: *High Frequency Trading* | merged into `def:hft-strategies` | chap. 15, pp. 291–293; chap. 7, pp. 129–134 | Merged; ML claim not adopted |
| execution: *HFT Shark Strategy* | merged into `def:hft-strategies` (Pitfalls) | Appendix, pp. 312–314; FINRA Rule 5270; SEC 2010 release as already cited | Kept as historical description, qualified |
| execution: *HFT Trading Infrastructure* | merged into `def:automated-trading-architecture` | chap. 7, pp. 138–141 | Merged; FIX reversal corrected |

**Subclaims.**

| Where | Earlier claim | Disposition |
|---|---|---|
| overview intro | Schematic of a live production strategy, without research tools | Rewritten (p. 17); data and research added from Exhibit 2.3 (p. 19) |
| overview figure | Three modules → portfolio construction → execution | Redrawn with Exhibit 2.1's return arrow (portfolio construction and execution "interact"); original kept verbatim and rendered in the artefact |
| overview list i–iii | Alpha predicts; risk limits unrewarded exposure, "i.e. directional exposure limit on an asset class"; t-cost model decides if costs are "desirable" | Rewritten (pp. 17–18); the risk example generalised by the earlier notes, qualified; the t-cost model estimates costs, the portfolio model decides |
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

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-narang` | as listed | Third edition; one practitioner's account; anecdotes and performance figures unsourced; several passages of the earlier notes from an unknown (probably earlier) edition |
| `alpha-afml` | pp. 5–9 | One author's prescription; no criteria or evidence for the stages |
| `usc-7-6c`, `finra-rule-5270` | (a)(5); (a) | Futures/swaps and FINRA members only; securities-market spoofing and other jurisdictions unchecked |
| Specialist readings | none | Stubs |

The five new entries and the merged passages are *partly checked 2026-10-15*, *draft*; **human review is outstanding**.

### Independent review

Before committing, a separate review compared every changed claim, quotation, locator and calculation with the source text layers and the legal texts. It confirmed the arithmetic, all 23 cross-referenced labels and both legal quotations, and found four overstatements and seven judgement calls, all fixed in this batch:
- "most trend followers win on fewer than 40 percent" → his "often less than 40 percent" (pp. 60–61);
- "no evidence for the classes" → two papers for value/yield (Fama–French, Ball) and his reading of volume research (pp. 37–40);
- macroscopic alpha "converging to zero" → the *chances* of an individual finding it (AFML p. 6);
- "larger quants use order-book signals" (the earlier notes, not Narang) → his micro price and footprint passages (pp. 130, 133–134);
- FINRA 5270: "inferring a hidden order is not that information" marked as interpretation, with the undefined term and the rule's note on Rules 2010 and 5320;
- Narang's front-running argument limited to "most" HFTs, with his contractual-market-maker exception (p. 312);
- the CEA clause's scope given in its own words, "futures and swaps" marked as gloss;
- order types, not fees and priority, are what he says change often (pp. 134–135);
- "inert and useless" applies to data only (p. 19);
- the non-contiguous machine-learning quotation split and the rebuttal marked as interpretation;
- "worth sizing on only if calibrated" softened; "largely" restored; the CVX view and the carry context restated.

### For review

- Keeping the cancel-and-replace and shark passages as historical descriptions with limited legal support, rather than as techniques or stubs only.
- The redrawn diagram's return arrow, and the alpha taxonomy's correction from five classes to eight.

## systematic-investing architecture review follow-up: hidden-order leakage, lifecycle timing and currency fields, 15 October 2026

Narrow corrections to systematic-investing architecture review, run before derivatives and hedging review; the systematic-investing architecture review record above is left as written, and this record supersedes it where they differ.

- **Hidden orders, `def:order-exposure-decisions`.** "Hidden orders reveal nothing" overstated Narang, who says a hidden order "provides no information to the market" (p. 134), meaning no displayed interest. The entry now separates undisplayed pre-trade interest from information inferred through executions and probing, citing the SEC's 2010 release on immediate-or-cancel "pinging" to find undisplayed liquidity (p. 47, n. 69) and linking `def:order-anticipation`; hiding lowers, not removes, leakage.
- **Lifecycle timing, `meth:strategy-production-lifecycle`.** "Embargo and paper trading are forms of validation before production" contradicted López de Prado, whose portfolio-oversight stages follow deployment (AFML pp. 8–9). They are now validation before live-capital trading (graduation).
- **Currency fields.** `def:hft-strategies` no longer says no current rule was checked: FINRA Rule 5270 (as displayed 15 October 2026) is recorded as the one current rule checked, with historical figures dated as given. `def:order-exposure-decisions` dates the U.S. Code passage to its 2024 edition and Narang's venue details to 2024, with no current venue rule checked. `def:automated-trading-architecture` adds Narang's 2024 account, with his latency figures undated.
- **Notes and index.** The `execution-trading-costs`, `model-governance-controls` and `hft-market-design` notes record the changes; the systematic-investing architecture review index row gives `2642451`.

## derivatives and hedging review: derivatives, hedging, rates and time value (Hull notes and the time-value file), 16 October 2026

Source checking, not study; no checkpoint was attempted. Hull's book is the first reading of the `volatility-options` overview and the GIPS standards a reading of `performance-manager-evaluation`; both were read only where the entries needed them.

### Sources, 2026-10-15/16

- **Hull** (`s7-hulloptions`), *Options, Futures, and Other Derivatives*, 11th Global edition, Pearson 2022, ISBN 9781292410654 (copyright page checked; matches the catalogue's selected edition), local PDF, 881 pages, text layer through PDFKit, printed page = PDF page − 1 (PDF 24 is p. 23, chapter 1's opening). Read: chap. 1 pp. 23–33; chap. 2 pp. 46–57 and 62–65; chap. 3 pp. 70–90; chap. 4 pp. 98–119; chap. 5 pp. 124–145; chap. 6 pp. 152–155. Author errata not checked. Figures 2.1 (p. 51) and 3.3 (p. 81) viewed as page images: the two PNGs of the earlier notes reproduce them.
- **New York Fed**, *Additional Information about Reference Rates* (`exp-sofr-data`) and the EFFR and SOFR pages, retrieved 2026-10-15: EFFR and OBFR methodology (volume-weighted median, FR 2420, change of 1 March 2016) and SOFR's scope.
- **GIPS standards for firms, 2020 edition** (`wide-gips-2020`), official PDF (146 pages) downloaded 2026-10-15, printed page = PDF page − 18: provisions 1.A.35 (pp. 5–6), 2.A.23–2.A.30 (pp. 11–13) and the glossary entries for external cash flow (p. 75), gross-of-fees (p. 76), money-weighted and net-of-fees returns (p. 78) and time-weighted return (p. 83).
- **CPSS–IOSCO PFMI** (`exp-pfmi`), para. 1.13, p. 9, as read in transaction-cost models review.
- **Not read:** the readings of the four owning pathways beyond those above; the Dodd–Frank, swap-reporting and uncleared-margin rule texts; Hull chaps. 6.2–6.5 and 7 onward; any source for the earlier time-value notes, whose origin is not recorded.

### Numerical checks

Independent of the formulas being checked, in a scratch script (numpy/scipy, not kept in the repository):
- **Hedge objective**: the sample variance of $\Delta S-h\Delta F$ on Hull's Table 3.2 data minimised numerically gives $h^*=0.7777$, equal to the OLS slope and to $\rho\sigma_S/\sigma_F$; variance retained 13.81% (removed 86.19% $=\rho^2$); at $h=1$, 20.86%; $N^*=37.03$; one-day $N^*=32.23$; tailing factor $1/1.05=0.9524$ against $1/(1+0.05\times0.5)$ for six months.
- **Discounted cash flows**: Hull's forward prices (40.50, 886.60, 51.14, 25.77), forward value 2.17, parity 0.7206, storage 484.63, index 1,313.07; bond 98.39, yield 6.76%, par yield 6.873%; forward 3→4 6.2%; instantaneous forward by finite difference of $-\ln P$ equal to $R+TR'$.
- **FRA**: Example 4.3 gives \$369,247 (Hull prints \$369,200); sign from the receive-fixed side.
- **Duration**: $B=94.213$, $D=2.653$, $C=7.570$; exact against approximate at $\Delta y=+0.001$, $\pm0.02$; semiannual $D^*=2.499$, exact 93.978.
- **Annuity limits**: brute-force sums equal the closed forms; factor → 10 as $r\to0$; perpetuity partial sums converge to $A/r$.
- **Returns**: TWR −1.00% against MWR −3.71% in a contribution example; cumulative 3.95%, geometric mean 1.30%; annualised 7.42%; IRR roots 10% and 40%; a no-root case (maximum NPV −0.75); real 4.854% against $n-\pi=5\%$; leveraged 13%.
- **Quotes**: 2.6957, 2.7111, T-bill quote 4.00, \$120,156.25, accrued 1.64; gold margin balance \$7,980 on day 7.

### Findings on the earlier notes

| Earlier block | Entry | Hull 11th Global ed. / other source | Disposition |
|---|---|---|---|
| *derivative* | `def:derivative-contracts` (new) | chap. 1, p. 23 | Rewritten |
| *spot/forward contract* | `def:derivative-contracts` | sec. 1.3, pp. 28–30 | Rewritten, payoffs kept |
| *call/put option* | `def:derivative-contracts` | sec. 1.5, p. 31 | **Corrected**: the earlier notes reversed the rights |
| *American/European option* | `def:derivative-contracts` | p. 31 | Rewritten |
| *credit spread* | `def:interest-rate-measures` (new) | sec. 4.1, p. 98 | Rewritten ("interest rate" → over a risk-free rate) |
| *Forward Rates* | `mod:forward-rates-fra` (new) | sec. 4.8, pp. 109–110 | Rewritten |
| *FRA* | `mod:forward-rates-fra` | sec. 4.9, pp. 110–112 | Rewritten; value **corrected** to a present value |
| *Duration* | `mod:duration-convexity` (new) | secs. 4.10–4.11, pp. 112–117 | Rewritten; approximations marked |
| *Basic Principles of Futures Hedging* (table) | `def:futures-hedge-basis` (new) | sec. 3.1, pp. 70–72 | Rewritten; the long-hedge column noted as not Hull's |
| *basis* | `def:futures-hedge-basis` | sec. 3.3, p. 76 | Rewritten; sign convention stated |
| *basis risk* | `def:futures-hedge-basis` | p. 77 | Rewritten; long-hedge case and cross-hedge components added |
| *Cross Hedging* | `def:futures-hedge-basis` | sec. 3.4, p. 79 | Rewritten |
| *Hedge Ratio* | `mod:minimum-variance-hedge-ratio` (new) | sec. 3.4, pp. 79–83 | Rewritten; derivation added |
| *Time Value of Money Formulas* | `def:interest-rate-measures` | none (derived here) | Rewritten; "Expected Annual Rate" corrected to effective |
| *Return Metrics* | `def:return-measures` (new) | GIPS 2020 | Rewritten; TWR root and real-return "risk" factor corrected |

**Subclaims outside and inside the blocks.**

| Where | Earlier claim | Disposition |
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

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-hulloptions` | as listed | Textbook account as of 2021; U.S.-centred conventions and examples; the edition followed by the earlier notes is unknown |
| `exp-sofr-data` | methodology page | As published 15 October 2026 |
| `wide-gips-2020` | definitions and provisions listed | Presentation standard, not a full methodology; after-tax returns not covered |
| Reform rules, term-premium and hedging evidence | none | Stubs |

The ten new entries and the merged passage are *partly checked*, *draft*; **human review is outstanding**.

### Independent review

An independent subagent re-read the cited Hull pages (chaps. 1–6), the GIPS, PFMI and New York Fed passages and Narang p. 134, recomputed every number in the entries and checked every cross-reference label. All quotes, locators and numbers not listed below were confirmed. Fixed:
- **Definite errors.** The hedge-ratio minimum was stated as $dV/dh=0$; now $d\operatorname{Var}V(h)/dh=0$. A locator "pp. 82" → p. 82. The gold margin example cited only Table 2.1 (p. 52); the loss and the call are in the text on pp. 51 and 53. The earlier "value is close to zero" at a forward's inception is Hull's own sentence (p. 133), not an omission; the entry now says the earlier notes dropped Hull's next step, $K$ set so $f=0$. The receive-fixed FRA cash flow $\tau(R_K-R_M)L$ is now marked as derived from Hull's definitions (pp. 111–112), and the Pitfalls record that Hull's p. 111 example reverses the payment direction (Party A, receiving 3% fixed with LIBOR at 3.5%, pays \$125,000); his p. 112 value formula is correct; errata not checked.
- **Qualifications.** Yield change against a parallel zero-curve shift: approximately equal, exactly only for a flat curve (0.9996 on Hull's Table 4.2 bond, recomputed). EFFR: the methodology changed with the rate for 1 March 2016 and is now a volume-weighted median. The annuity limits are the future-value factor's. LTCM (Business Snapshot 2.2): collateral on both legs and high leverage forced close-outs, not "unable to meet calls". Term-structure theories: Hull calls two conjectures and finds liquidity preference "most appealing". GIPS 2.A.23–2.A.24: sub-period returns at large cash flows apply if daily returns are not calculated, with exceptions for private-market investment portfolios. SOFR's 360-day year cited to Hull p. 100. "DV01" dropped from an index that never defined it.
- **systematic-investing architecture review wording.** In `def:order-exposure-decisions`, words after Narang's quotation had read as his; "in Narang's words" now sits with the quotation and the gloss (size and price not displayed before it trades) is the entry's.
Not changed: Hull's "tranasaction" typo (p. 23) is silently corrected in the quotation.

### For review

- Using the New York Fed's methodology to correct Hull's EFFR description, and treating Hull's reform list as his account.
- The time-value identities written as derived, unsourced material.

## derivatives and hedging review follow-up: cross-hedge components, yield-shift condition, return horizons and GIPS annualisation, 16 October 2026

Narrow corrections to derivatives and hedging review (`9fbd551`), run before financial data and labels review; the derivatives and hedging review record above is left as written, and this record supersedes it where they differ.

- **Cross hedging, `def:futures-hedge-basis`.** The entry gave $F_1+(S_2^*-F_2)+(S_2-S_2^*)$ without naming its parts and cited pp. 77 and 79. Hull calls the two last terms "the two components of the basis": $S_2^*-F_2$ the basis that would exist if the hedged asset were the futures' underlying, $S_2-S_2^*$ "the basis arising from the difference between the two assets" (p. 77). Both that expression and $S_2+F_1-F_2=F_1+b_2$ are one-to-one hedges: Hull's examples use a hedge ratio of 1.0, "natural" for the same asset and "not always optimal" in a cross hedge (p. 79). Added, as derived: with hedge ratio $h$ (futures units per unit of exposure, taken in the offsetting direction) the effective price is $S_2+h(F_1-F_2)$, equal to $F_1+b_2$ at $h=1$; $h$ carries any unit conversion between the two assets. The locator of "Cross hedging uses a futures contract on a different asset", which had been p. 78 (Hull's *Choice of Contract*), is now p. 77 and sec. 3.4, p. 79; and the units remark now notes that Hull's jet-fuel and heating-oil example needs no conversion (both in gallons).
- **Returns, `def:return-measures`.** The example compared a cumulative TWR ($-1.0$ percent over two periods) with a per-sub-period IRR ($-3.71$ percent). Recomputed independently: the IRR solving $-100-100(1+x)^{-1}+189(1+x)^{-2}=0$ is $-3.7126$ percent per equal sub-period, $-7.2874$ percent compounded over both; the TWR's geometric mean is $-0.5013$ percent per sub-period. The entry now labels units and compares like with like.
- **GIPS annualisation, same entry.** "Money-weighted returns must be annualised since-inception returns" stated 2.A.29 without the presentation rules. Read in the GIPS 2020 PDF (printed page = PDF page − 18): 2.A.12, "Returns for periods of less than one year must not be annualized" (p. 9); 2.A.29.a, "Calculate annualized since-inception money-weighted returns" (p. 12); 5.A.1.a–b, the annualised since-inception MWR through the most recent annual period end and, "when the composite has a track record that is less than a full year, the non-annualized composite since-inception money-weighted return through the initial annual period end" (p. 33). The entry now separates the mathematical annualisation $(1+R)^{365/d}-1$ from what a firm may present, and marks its 200-day example as one GIPS would not allow a firm to present. The advertising provisions were not read.
- **Yield against zero-curve shift, `mod:duration-convexity`.** derivatives and hedging review's review fix said the two coincide "exactly only when the zero curve is flat". Flatness is sufficient, not necessary. Derived and checked: the yield moves by exactly $\Delta$ for every parallel shift $\Delta$ if and only if the zero rates at all the bond's payment dates equal its yield; a zero-coupon bond ($y=R(T)$) moves one for one on any curve, and a two-payment bond on a curve level at its payment dates does too. Counterexamples: Hull's Table 4.2 bond moves 0.9996$\Delta$; a 10-year 5 percent annual-coupon bond on a curve rising 40 bp a year from 1.4 percent moves 0.986$\Delta$, with yield duration 8.13 against zero-curve duration 8.01 years. The script is kept as `notes/artefacts/rates-credit-mortgages/yield-shift-check.py` (numpy, scipy).
- **Notes and index.** `commodity-hedging`, `rates-credit-mortgages` and `performance-manager-evaluation` notes, the `s7-hulloptions` reading note and `log.md` record the changes; the derivatives and hedging review index row gives `9fbd551`.

## financial data and labels review: the AFML data cluster (taxonomy, data structures, labels, sample weights, fractional differentiation), 16 October 2026

Source checking, not study; no checkpoint was attempted. López de Prado (`alpha-afml`) is a required reading of `statistical-learning-foundations` and was read only in chaps. 2–5; Velu, Hardy and Nehren (`s3-velu`) is no pathway's reading. Two internal review groups were used: A, taxonomy and data structures; B, labels, sample weights and fractional differentiation.

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

### Findings on the earlier notes

**Source identification.**

- `datastruct.tex`, `datalabel.tex` (except as below), `datasampleweights.tex` and `fracdifffeat.tex`: López de Prado chaps. 2–5, close paraphrase with the source's own slips copied (below).
- `taxonomy.tex`: its table and four remarks follow López de Prado sec. 2.2 (pp. 23–25); its five definitions follow Velu, Hardy and Nehren chap. 1, sec. 1.4 (pp. 26–44), not named in the file. The "Binned Data" definition holds Velu's *Daily Statistics* (pp. 39–40); his *Binned Data* is p. 42.
- `datalabel.tex` meta-labelling: the steps (high-recall primary model, threshold possibly from ROC curves, concatenated features and predictions, positive "only where both are true") follow the Hudson & Thames blog "Meta Labeling (A Toy Example)" (`ht-meta-labeling-toy`, read 2026-10-16); `metalabel.tikz` follows its architecture. The five feature groups beyond the concatenation and the three "Limitations of Meta-Labelling" were found in neither source nor by web search; they are not adopted.
- Figures: `standardbars.png` reproduces AFML Figure 2.1 (p. 28); `fracdiffexpandwindow.png` and `fracdifffixedwidthwind.png` reproduce AFML Figures 5.3(b) (p. 81) and 5.4 (p. 83); none was credited. They are kept only in the artefact, with attribution there; no entry uses them.

| Earlier block | Entry | Source | Disposition |
|---|---|---|---|
| *Fundamental Data Characteristics* | `def:financial-data-types` (new) | AFML sec. 2.2.1, pp. 23–24 | Rewritten; Bloomberg-specific lag restored, backfill and reinstatement defined |
| *Market Data Characteristics* | `def:financial-data-types` | sec. 2.2.2, pp. 24–25 | Rewritten; "over 10TB" and its "appealing" context restored, marked unsourced |
| *Analytics Data Characteristics* | `def:financial-data-types` | sec. 2.2.3, p. 25 | Rewritten; crowding point added |
| *Alternative Data Characteristics* | `def:financial-data-types` | sec. 2.2.4, p. 25 (Kolanovic–Krishnamachari split) | Rewritten; "annoys your data infrastructure team" marked opinion, in context |
| *Reference Data* | `data:trading-reference-data` (new) | Velu sec. 1.4.1, pp. 26–35 | Rewritten; dividend conflation **corrected**; rule histories restored |
| *Market Data Feed* | `data:market-data-levels` (new) | Velu sec. 1.4.2, pp. 35–39, Table 1.10 | Rewritten; "divide by 1000" **corrected** to 10000; consolidation and latency restored |
| *Binned Data* | `data:derived-market-statistics` (new) | Velu sec. 1.4.3, pp. 39–40 (Daily Statistics) | Rewritten; mislabelled heading **corrected** |
| *Granular Intraday Microstructure Activity* | `data:derived-market-statistics` | pp. 41–42 | Rewritten; reference-data caveat and binned-data limits added |
| *Fundamental Data and Other Data* | `def:financial-data-types` | Velu sec. 1.4.4, pp. 42–44 | Rewritten; hedges ("might", "thought to be", "generally") restored; claims stubbed as evidence |
| *Standard Bars* | `meth:activity-sampled-bars` (new) | AFML sec. 2.3.1, pp. 26–28 | Rewritten; dollar-bar robustness narrowed; distributional evidence qualified (Ané–Geman abstract read) |
| *Information-Driven Bars* | `meth:information-driven-bars` (new) | sec. 2.3.2, pp. 29–32 | Rewritten; runs statistics and imbalance thresholds **corrected**; $b_0$ and causal EWMAs stated |
| *Multi-Product Series: ETF Trick* (definition) | `meth:etf-trick` (new) | secs. 2.4–2.4.1, pp. 32–33 | Merged into the method entry |
| *ETF Trick* (method) | `meth:etf-trick` | p. 34 | Rewritten; $o_{i,t+1}$ **corrected**; timing, positivity and cost limits added |
| *ETF Trick: Computation of Allocation Vector with PCA* | `mod:pca-risk-distribution-weights` (new) | sec. 2.4.2, pp. 35–36 | Rewritten; two formula slips **corrected**; eigenvalue and sign conditions added |
| *ETF Trick: Single Futures Roll* | `meth:etf-trick` | sec. 2.4.3, pp. 36–37 | Rewritten; denominator **corrected** to the previous raw price; roll gaps added |
| *Sampling for Reduction* | `meth:event-based-sampling` (new) | sec. 2.5.1, p. 38 | Rewritten |
| *Event-Based Sampling: CUSUM Filter* | `meth:event-based-sampling` | sec. 2.5.2.1, pp. 38–40, Snippet 2.4 | Rewritten; zero condition and run condition **corrected**; sampling, reset and strict-inequality rules added |
| *Labelling with Fixed-Time Horizon Method* | `meth:triple-barrier-labelling` (new) | sec. 3.2, p. 43 | Rewritten |
| *Limitations of Fixed-Time Horizon Method* | `meth:triple-barrier-labelling` | p. 44, Snippet 3.1 | Rewritten; third limitation (path) added |
| *Labelling with Triple-Barrier Method* | `meth:triple-barrier-labelling` | sec. 3.4, p. 45 | Rewritten; vertical-barrier preference, side and size, intrabar ties added |
| *Triple-Barrier Method Configurations* | `meth:triple-barrier-labelling` | p. 46 | Rewritten; "physical", "loose", "immediate" corrected |
| *Meta-Labelling* | `meth:meta-labelling` (new) | secs. 3.6–3.8, pp. 50–55 | Rewritten from AFML; the earlier notes' steps attributed to Hudson & Thames; claims stated as claims; out-of-sample primary predictions added |
| *Limitations of Meta-Labelling* | `meth:meta-labelling` (Pitfalls) | no source found | Not adopted; first item contradicts AFML p. 53; kept in the artefact |
| *Overlapping Outcomes* | `def:label-concurrency-uniqueness` (new) | sec. 4.2, pp. 59–60 | Rewritten |
| *Estimating Uniqueness of Label* | `def:label-concurrency-uniqueness` | sec. 4.3, p. 60 | Rewritten; $r_{t-1,t}$ **corrected** |
| *Average Uniqueness of Label* | `def:label-concurrency-uniqueness` | sec. 4.4, pp. 61–62 | Rewritten; training-set condition restored |
| *IID and Oversampling* | `meth:sequential-bootstrap` (new) | sec. 4.5, p. 62 | Rewritten; AFML's $e^{-K/I}$ **corrected** to $e^{-I/K}$, "overlapping" to non-overlapping |
| *Sampling with Bootstrap, Redundancy* | `meth:sequential-bootstrap` | pp. 62–63 | Rewritten |
| *Sequential Bootstrap* | `meth:sequential-bootstrap` | secs. 4.5.1–4.5.4, pp. 63–68 | Rewritten; normaliser **corrected**; Monte Carlo evidence qualified |
| *Weighting Observations by Uniqueness and Absolute Return* | `meth:sample-weights-attribution-decay` (new) | sec. 4.6, pp. 68–69 | Rewritten; factor $I$ and the weighting direction **corrected** |
| *Time Decay Weighting* | `meth:sample-weights-attribution-decay` | sec. 4.7, pp. 70–71 | Rewritten; AFML's $d[1]$ and $cT$ slips **corrected** |
| *Class Weighting* | `meth:sample-weights-attribution-decay` | sec. 4.8, pp. 71–72 | Rewritten |
| *BackShift Operator* | `mod:fractional-differencing-weights` (new) | sec. 5.4, p. 77 | Rewritten |
| *Properties of Fractionally Differentiated Features* | `mod:fractional-differencing-weights` | secs. 5.4.1–5.4.3, pp. 77–80 | Rewritten; weight formula **corrected**; "makes stationary" corrected to AFML's "necessary"; decay rate added |
| *Expanding Window* | `meth:fixed-width-fractional-differencing` (new) | sec. 5.5.1, pp. 80–82 | Rewritten with one consistent index (AFML's is not) |
| *Fixed-Width Window* | `meth:fixed-width-fractional-differencing` | sec. 5.5.2, pp. 82–83; secs. 5.6–5.7, pp. 84–88 | Rewritten; FFD range **corrected**; "it is stationary" qualified; minimum-$d$ procedure added |

**Subclaims outside the blocks and inside them, beyond the rows above.**

| Where | Earlier claim | Disposition |
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

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `alpha-afml` | chaps. 2–5 as listed | A 2018 practitioner text; its evidence is one futures market (E-mini) or synthetic; several formulas wrong (marked); chap. 7 unread |
| `s3-velu` | chap. 1, sec. 1.4 | Practitioner descriptions as of about 2018–2020; exchange rules and calendars not checked against current sources |
| `ane-geman-2000` | abstract | Paper unread |
| `ht-meta-labeling-toy` | the page | Provenance only; undated, no author |
| Evidence on bars, meta-labelling, alternative-data decay; purging and embargo | none | Stubs |

The seventeen new entries are *partly checked*, *draft*; **human review is outstanding**.

### Independent review

Two source reviews ran before writing (group A: taxonomy and data structures against AFML chap. 2, Velu sec. 1.4 and the Ané–Geman abstract and critique; group B: labels, weights and fractional differentiation against AFML chaps. 3–5, with their own numerical script), and their findings are the provenance and corrections above. An independent review of the integrated changes then re-read every quote by script against the AFML and Velu text layers, rechecked locators, recomputed the derivatives and hedging review follow-up (Hull pp. 77–79, the return example, GIPS 2.A.12, 2.A.29, 5.A.1, the yield-shift condition) and the mathematics, ran `afml-checks.py`, and compared the records, counts and artefacts. Fixed:
- **Definite errors.** The fractional-differencing ADF illustration quoted a statistic ($-7.6$) from an earlier run of the script: adding the balanced-flow test had shifted the random-number stream; the entry now gives the script's $-5.3$ at $d=0.2$ and $-10.2$ at $d=0.4$, with $\tau=10^{-4}$. The cross-hedging locator p. 78 (Hull's *Choice of Contract*) became p. 77 and sec. 3.4, p. 79, also noted in the follow-up record. The PCA entry's "$2^N$ allocations" became $2^k$ for the $k$ components given risk, with distinct eigenvalues (non-unique with repeated ones); the script and the portfolio-construction note follow. The compendium was rebuilt after the last edit, and this record appended (it had been drafted outside the repository at review time).
- **Judgement calls adopted.** The share of Monte Carlo runs in which the sequential bootstrap is less unique is now computed by the kept script (22 percent; the review's 3,000 runs gave 23); the overlap example distinguishes the exact $4.3\times10^{-5}$ from $e^{-I/K}=4.5\times10^{-5}$; the attribution weights name log returns; the Monte Carlo spans are 1–4 bars (Snippet 4.7, `maxH=5`); the ETF-trick toy is called a consistency check; GIPS 2.A.12 is described as a calculation provision with no stated reason, the reason being interpretation; Hull's jet-fuel example needs no unit conversion; "routed against the map" became "outside the map's candidates"; the CUSUM input remark is labelled interpretation; an unread chap.-10 phrase was dropped from the meta-labelling entry.
- **Verified unchanged.** All other quotes, locators and numbers; the derivatives and hedging review follow-up; the provenance claims; counts, labels and pathway order; preservation.

### For review

- Correcting López de Prado's own formulas (overlap approximation, time-decay boundary, index ranges) on the basis of derivation and computation, without errata.
- Qualifying the stationarity of fractionally differenced series with fractional-integration theory, which is interpretation, not a reading.
- Keeping the three reproduced AFML figures only in the artefact, with attribution.

## financial data and labels review follow-up: hedge-ratio sign, ETF-trick timing and capital, label spans, and the Hawkes lead, 16 October 2026

Narrow corrections to financial data and labels review (`8be60d1`) and to a derivatives and hedging review entry, run before order books and order flow review; the earlier records are left as written, and this record supersedes them where they differ. Decisive examples are reproduced by `notes/artefacts/volatility-options/negative-hedge-ratio-check.py` and `notes/artefacts/statistical-learning-foundations/financial-labels-capital-checks.py` (numpy only); the earlier scripts are unchanged.

- **Negative hedge ratios, `def:futures-hedge-basis` and `mod:minimum-variance-hedge-ratio`.** The first said a negative $h$ "would add to the exposure". With the stated convention ($V(h)=\Delta S-h\Delta F$; $h>0$ a short futures position against a long exposure), $h^*=\operatorname{Cov}(\Delta S,\Delta F)/\operatorname{Var}\Delta F$ has the sign of $\rho$, and a negative $h^*$, a long futures position against a long exposure, still reduces variance to $\sigma_S^2(1-\rho^2)$. Example: $\sigma_S=\sigma_F=1$, $\rho=-0.6$: $h^*=-0.6$ leaves 0.64 against 1 unhedged, while $h=+0.6$ gives 2.08; a 200,000-draw simulation gives an OLS slope of $-0.6003$ and the same grid minimiser. Both entries now state the sign convention and the case.
- **ETF trick timing, `meth:etf-trick`.** The entry called sizing at $o_{i,t+1}$ "execution at the next open, not look-ahead, provided $\omega_t$ uses information up to $t$". López de Prado's holdings divide by the next open, unknown at $t$, so the series is an accounting convention; causal weights are necessary but not sufficient for it to be executable. The entry now names what would reproduce it: an order whose quantity is set by its own fill price, such as a notional order per leg filled in full in a single-price opening auction at $o_{i,t+1}$ with $\varphi_{i,t}$ known, to be checked per venue and instrument; a quantity sized on $p_{i,t}$ leaves a gross exposure of 1.0026 against $K=1$ on a two-leg toy with 1.5 and 1.6 percent opening gaps.
- **Gross exposure and capital, same entry.** "Gross exposure equals $K_t$" is $|K_t|$ when every $o_{i,t+1}\varphi_{i,t}>0$, and $K_t$ only with $K_t\ge0$; with a negative price a holding's sign no longer follows its weight. At $K_t=0$ the holdings vanish and at $K_t<0$ they reverse ($K=-0.2$ turns the long leg short, gross 0.2); the method has no rule for exhausted capital, so a backtest must stop the series or state its own financing or loss rule. No production system is described.
- **Label spans, `def:label-concurrency-uniqueness`, `meth:sample-weights-attribution-decay`, `meth:triple-barrier-labelling`.** For returns $r_{t-1,t}$ indexed by ending time, a label from $t_{i,0}$ to $t_{i,1}$ uses $t_{i,0}<t\le t_{i,1}$; the entries now define $1_{t,i}$ that way and start the attribution sum at $t_{i,0}+1$. The earlier remark that "either convention can be used if it is used consistently", and that the toy "has the same off-by-one", was wrong. López de Prado's toy matrix (p. 65, rows $t=1,\dots,6$) is the ending-time rule, and Snippet 4.6's spans $\{0{:}2,2{:}3,4{:}5\}$ are a consistent start-time reindexing; his Snippets 4.1, 4.3 and 4.10 mark $t_{i,0}$ to $t_{i,1}$ inclusive on event timestamps, which adds the return ending at $t_{i,0}$. On the toy's events that inclusive rule gives concurrency $(1,1,2,2,2,1,1)$ and uniqueness $(0.75,0.5,0.833)$ against $(1,1,2,1,1,1)$ and $(0.833,0.75,1)$, and labels 2 and 3, adjacent at $t=4$, share $r_{3,4}$, which label 3 does not use; attribution sums on a toy path change from $(0.0247,0.0145,0.0190)$ to $(0.0149,0.0146,0.0288)$. The bootstrap probabilities and Monte Carlo of `meth:sequential-bootstrap` are unaffected (the toy matrix is unchanged; the Monte Carlo replicates AFML's own code convention, as financial data and labels review recorded). Read again: AFML pp. 60–61, 64–66 and 69 (text layer).
- **Hawkes lead, `notes/source-review-index.md`.** The proposed the topic review named `wide-bacry-life-cycle` (an impact paper) as the Hawkes lead and said a reading note existed for it in that role. Replaced by `wide-bacry-hawkes`, Bacry, Mastromatteo and Muzy, "Hawkes Processes in Finance", a required reading of `market-making-lob`, with no reading note and no full-text check at the time of the correction (order books and order flow review then read parts of its preprint; see below).
- **Notes and index.** `statistical-learning-foundations` and `commodity-hedging` notes, the `alpha-afml` reading note and `log.md` record the changes; the financial data and labels review index row gives `8be60d1`.

## order books and order flow review: orders, the limit order book, queues, order flow and point processes (eight files, one batch), 16 October 2026

Source checking, not study; no checkpoint was attempted.

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
- **Harris counterfactual**: gamma latent spread (shape 4), $\delta=5$: latent means 0.6, 1.2, 3 and 8 old ticks give expected spreads 1.010→0.601, 1.302→1.200, 3.005→3.000, 8.000→8.000 old ticks; the earlier $k/\delta$ rescaling would predict −6.4 for the last.
- **Imbalance**: $QI=2I-1$ to $10^{-16}$; scale invariance. **OFI against trade imbalance**: a five-state toy gives $\mathrm{OFI}=+400$, $\mathrm{TI}=-100$.
- **Lee–Ready**: four toy trades, including a sell at the bid after an uptick.
- **Realised variance with i.i.d. noise**: tracks $\int\sigma^2+2n\sigma_\eta^2$ from 13 to 23,400 returns. **Epps from asynchrony**: true correlation 0.6, previous-tick sampling, 40 paths: 0.120 at step 5, 0.394 at 30, 0.547 at 120, 0.629 at 600.
- **Deseasonalisation**: multiplicative coefficients recovered within 0.0052; a later shock moves the centred average at the six earlier times.
- **Hawkes**: exponential kernel, branching ratio 0.6: rate 2.471 against 2.500, clustering ratio 6.38 against the long-window 6.25; compensator-rescaled durations mean 1.005, KS $p=0.35$ (raw durations $p\approx10^{-268}$). **Inhibition**: linear intensity $-0.30$ after one event; positive-part link: rate 0.369, clustering ratio 0.62. **A/R ratio**: drifts $+0.091$ and $-0.111$ per event at 1.2 and 0.8. **Waiting-time estimator**: 0.594 from uniform starts against 0.405 from events on a Hawkes sample.

### Findings on the earlier notes

**Source identification.** No file named a source. Block by block, the material follows:
- **Lehalle and Laruelle** (`alpha-laruelle`, 2nd ed. 2018): chap. 3, sec. 3.3 (pp. 216–227) for the CLOB and RFQ contrast, messages and channels, the three event types, conditioning, the Poisson baseline and its estimation, queue-reactive Models I–III, the A/R ratio, mean reversion and reset, and imbalance; chap. 1, sec. 1.3 (pp. 74–90) for tick size, binding probability and leeway, quoted depth, order-to-trade ratio, cumulative depth, queue jumping; app. A, sec. A.6 (pp. 266–273) for the Harris model and its counterfactual, nearly symbol for symbol; secs. A.11–A.13 (pp. 298–319) for decomposition, moving averages, deseasonalisation, the volume model, point processes, Hawkes processes, signature plot and Epps effect, also nearly symbol for symbol.
- **Harris** (`alpha-harris`): limit-price placement, limit orders as options, their two risks and absent traders (chap. 4, pp. 73–78); price clustering (p. 91); open and closed books (p. 109); the block statistic and block-price rule (sec. 15.5, pp. 332–333); Lee–Ready and its limits (p. 423).
- **Hasbrouck** (`s6-hasbrouck`): signing and signed volume (sec. 9.7, pp. 89–90); event against wall-clock time (p. 90); duration analysis (sec. 15.2.3, pp. 163–164).
- **Bouchaud et al.** (`catalogue-0528`): queue imbalance $I$ (chap. 7), Hawkes conditions and inhibition (chap. 9), stylised facts (chaps. 2, 4, 10), priority rules (chap. 3) and the "order-flow imbalance" of signed market orders (p. 222).
- Not found in any source read: the five-state lifecycle as worded, the "latency race boundary", queue imbalance's "less likely to reverse", the horizon caveat on imbalance, clustering's three reasons, the consolidated-tape caveat, refresh-time sampling, "false persistence", and the claim that marked Hawkes models can inhibit. Each is either rewritten as interpretation, corrected, or not adopted, as below.

| Earlier block | Entry | Disposition |
|---|---|---|
| *Order State Segmentation* | `mech:order-lifecycle` (new) | Rewritten against FIX 4.4 OrdStatus; the five states kept as a simplification |
| *Limit-Order Lifecycle* | `mech:order-lifecycle` (new) | Rewritten; "loses priority when price worsens" **corrected** to CME FIFO's rule (any price change, size increase, account change) and made venue-specific |
| *Message-Channel Segmentation* | `mech:order-lifecycle` (new) | Rewritten (LL p. 218: private channel faster) |
| *Absent Trader Representation* | `mech:order-lifecycle` (new) | Rewritten (Harris pp. 77–78; stop-order example) |
| *Lifecycle Tags Change Priority* | `mech:order-lifecycle` (new) | Partly adopted (time in force, iceberg priority, IOC); minimum quantity and cancel-on-disconnect stubbed |
| *Best Quotes and Spread* | `def:limit-order-book` (new) | Merged; spread measures cross-referenced to `def:spread-measures`, not repeated |
| *Liquidity Supply and Demand* | `def:limit-order-book` (new) | Merged (TQP p. 43) |
| *Limit Price Placement* | `def:limit-order-book` (new) | Rewritten as Harris's Table 4-1; "far: low immediacy cost" **corrected** |
| *Standing Limit Orders Are Trading Options* | `res:limit-order-options` (new) | Rewritten (Harris pp. 75–76; TQP p. 46); payoff and proof idea kept as derived, conditions added |
| *Limit-Order Regret* | `res:limit-order-options` (new) | Rewritten as Harris's two risks (p. 77) |
| *Equilibrium Spread as Order-Choice Indifference* | `res:spread-determinants` (existing) | Already stated there (Harris pp. 304–310); cross-referenced, not repeated |
| *Limit Orders Give Timing Options* | `res:limit-order-options` | Merged; monitoring speed marked as beyond the pages read |
| *Tick Size* | `def:tick-size` (new) | Rewritten (LL p. 74; TQP pp. 48–49) |
| *Price Clustering* | `def:tick-size` (new) | Rewritten as Harris p. 91; the earlier notes' reasons not adopted |
| *Binding Tick Constraint* | `def:tick-size` (new) | Rewritten (LL p. 77); "further reductions mostly change queue behaviour" not adopted |
| *Harris Tick Discretisation Model* | `mod:harris-discretised-spread` (new) | Rewritten with $\Phi$ stated |
| *Continuous Spread Expectation* | `mod:harris-discretised-spread` (new) | Rewritten; likelihood and fit added |
| *Tick-Size Counterfactual* | `mod:harris-discretised-spread` (new) | Units **corrected**: an observed $k$-tick spread is $k\delta$ new ticks; the model re-rounds the latent spread, $E=\sum_k(k/\delta)f_\delta(k)$ in old ticks (page images pp. 272–273) |
| *Tick Size and Queue Discipline* | `def:tick-size` | Rewritten (TQP p. 49; LL pp. 88–89) |
| *Quoted Depth Under Small Ticks* | `ev:tick-size-market-quality` (new) | Rewritten with sample (FTSE 100, April 2012) |
| *Order-to-Trade Ratio* | `ev:tick-size-market-quality` (new) | Rewritten (+50 percent, LL p. 84) |
| *Cumulative Depth* | `ev:tick-size-market-quality` (new) | Rewritten; conditioning on takers and fragmentation added |
| *Order-Book Visibility* | `def:limit-order-book` | Open/closed book from Harris p. 109; top-of-book and depth-book levels pointed to `data:market-data-levels` |
| *LOB Event Types* | `def:limit-order-book` | Merged (LL p. 219; TQP p. 51) |
| *Tick-Size Quality Proxies* | `def:tick-size` | Merged (LL pp. 77, 84) |
| *Value of a Quote* | `ev:tick-size-market-quality` | Value of quote adopted (LL p. 84); consolidated-tape clause not adopted |
| *RFQ Can Mimic a Book* | `def:limit-order-book` | Rewritten (LL p. 216); conditional depth as interpretation |
| *Condition on the Queue* | `mod:queue-reactive-intensities` (new) | Rewritten (LL pp. 219–220) |
| *Queue Imbalance* | `def:queue-imbalance` (new) | Merged with 04/02 #3; the reversal claim not adopted |
| *Arrival-Departure Ratio* | `mod:queue-reactive-intensities` | Rewritten (LL p. 224) with the promotion argument and a drift check |
| *Adverse Queue Selection* | `res:limit-order-options` | Merged (Harris p. 77; TQP p. 46) |
| *Queue-Reactive Estimation* | `mod:queue-reactive-intensities` | Rewritten (LL pp. 221–223); the starting-time dependence (n. 12) added and computed |
| *Mechanical Mean Reversion* | `mod:queue-reactive-intensities` | Rewritten (LL pp. 225–226) |
| *Latency Race Boundary* | same (Pitfalls) | Kept as interpretation, with LL p. 89 and TQP p. 59 |
| *Trade-Sign Classification Segmentation* | `meth:trade-sign-classification` (new) | Rewritten (Hasbrouck p. 89; Harris pp. 332, 423) |
| *Lee-Ready Classification* | `meth:trade-sign-classification` (new) | Rewritten; the paper itself not read |
| *Signed Volume* | `meth:trade-sign-classification` (new) | Rewritten; transforms (p. 89); "false persistence" not adopted |
| *Passive-Aggressive Ambiguity* | `meth:trade-sign-classification` (new) | Rewritten from Harris's sidebar (p. 423) |
| *Block Initiator Asymmetry* | `meth:trade-sign-classification` (new) | Kept as Harris's report ("approximately 80 percent", no sample); primary evidence stubbed |
| *Order Flow Imbalance* | `def:order-flow-imbalance` (new) | **Corrected**: defined as Cont–Kukanov–Stoikov's event-based $e_n$, not signed trades |
| *Signed-Trade Imbalance* | `def:order-flow-imbalance` (new) | Renamed trade imbalance (CKS $\mathrm{TI}_k$); naming collision with TQP p. 222 recorded |
| *Queue Imbalance* | `def:queue-imbalance` | Merged duplicate; $QI=2I-1$ |
| *Imbalance Feature Segmentation* | `def:order-flow-imbalance` | Kept as a menu, not results; multi-level OFI stubbed |
| *Imbalance Is Horizon-Dependent* | same (Pitfalls) | Not found; not adopted as a claim; CKS fits are contemporaneous; stubbed |
| *High-Frequency Stylized Facts* | `ev:high-frequency-stylised-facts` (new) | Rewritten with each fact's sample (TQP) |
| *Signature Plot* | `meth:realised-variance-signature-plot` (new) | Rewritten (LL pp. 316–317; TQP pp. 25–28) |
| *Microstructure Noise in Volatility* | `meth:realised-variance-signature-plot` (new) | Rewritten; divergence conditioned on the noise model |
| *Epps Effect* | `meth:realised-variance-signature-plot` (new) | Rewritten with Epps's words as LL quote them and their sample |
| *Realised Covariance* | `meth:realised-variance-signature-plot` (new) | Rewritten; refresh-time not adopted (stub); previous-tick shown to cause Epps |
| *Time-Series Decomposition* | `meth:intraday-deseasonalisation` (new) | Rewritten (LL p. 299) |
| *Centred Moving Average* | `meth:intraday-deseasonalisation` (new) | Rewritten; $A_t$ typo and window rule **corrected**; look-ahead added |
| *Additive Deseasonalisation* | `meth:intraday-deseasonalisation` (new) | Rewritten (LL pp. 300–301) |
| *Multiplicative Deseasonalisation* | `meth:intraday-deseasonalisation` (new) | Rewritten (LL pp. 301–302) |
| *Volume Seasonality Factorisation* | `meth:intraday-deseasonalisation` (new) | Rewritten with LL's $E[H]=1$, $\sum F=1$ and example |
| *Seasonality Before Signal* | same (Pitfalls) | Kept; estimation from earlier data added |
| *Trade Duration* | `def:market-clocks-durations` (new) | Rewritten (LL p. 306; Hasbrouck pp. 163–164) |
| *Market Time Segmentation* | `def:market-clocks-durations` (new) | Rewritten (Hasbrouck p. 90; TQP p. 173); volume time pointed to `meth:activity-sampled-bars` |
| *Event Time for Microstructure Laws* | `def:market-clocks-durations` (new) | Rewritten as Hasbrouck's rule |
| *Activity Time Can Hide Stress* | same (Practice) | Kept as interpretation |
| *Point-Process View* | `def:order-event-point-processes` (new) | Rewritten (LL p. 305) |
| *Counting Process and Duration* | `def:order-event-point-processes` (new) | Rewritten (LL p. 306) |
| *Conditional Intensity* | `def:order-event-point-processes` (new) | Rewritten; predictability stated |
| *Order-Book Event Segmentation* | same (Notation) | Merged (LL p. 221) |
| *Homogeneous Poisson Baseline* | `mod:queue-reactive-intensities` | Rewritten as LL's finding for one stock |
| *Integrated Intensity* | `def:order-event-point-processes` | Rewritten; LL's printed condition $\int\lambda=1$ **corrected** to divergence (page image p. 308); time rescaling computed |
| *Linear Hawkes Process* | `mod:hawkes-order-flow` (new) | Rewritten with conditions (non-negative causal kernel, $g<1$ or spectral radius $<1$) |
| *Exponential Hawkes Kernel* | `mod:hawkes-order-flow` (new) | Kept ($\alpha/\beta$, $\lambda_0/(1-\alpha/\beta)$, LL pp. 309–311); parameterisations compared |
| *Conditioning Improves Queue Dynamics* | `mod:queue-reactive-intensities` | Merged (LL pp. 223–224) |
| *Conditioning Segmentation* | `mod:queue-reactive-intensities` | Merged; its event-time item to `def:market-clocks-durations` |
| *Marked Flow Segmentation* | `mod:hawkes-order-flow` | **Corrected**: inhibition needs a non-linear link (TQP p. 181; BMM p. 8); agent classes from LL pp. 315–316 |

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

### Independent review

An integrated review of the whole batch, by the same session, after writing: every quotation in the new and changed entries was searched by script in the normalised text layers of the seven sources (all source quotations of the review found; unmatched strings are wording of the earlier notes quoted as such, page titles, or financial data and labels review quotes containing mathematics); locators were rechecked against the printed-page offsets; the mathematics was rederived (the $e_n$ cases, $QI=2I-1$, $E[\hat V_R]$ with noise, the Hawkes mean, branching and stability conditions, the counterfactual's units, the ETF gross-exposure identity). Fixed: a figure locator (Epps, pp. 318–319), the Harris chapter for open books (chap. 5), the CKS robustness passage (p. 8, not a claim of stability), the tick-regime pitfall (Lehalle and Laruelle's quotation groups do group by liquidity), an index clash in the ETF identity, and simulation figures re-taken after the Epps check was replicated over 40 paths (which shifted the random stream). This was not an independent second reader: **human review is outstanding.**

### For review

- Merging the two queue-imbalance definitions under `market-making-lob` and the OFI definition under `lob-deep-learning`, with Bouchaud et al.'s naming collision recorded rather than resolved.
- Correcting a printed condition in Lehalle and Laruelle (time change) and the earlier counterfactual's units by derivation and computation, without errata.
- Treating the FIX 4.4 states (through a vendor page) as the reference for order states.
- Keeping Harris's 80 percent block statistic as his unsourced report.

## order books and order flow review follow-up: trade-signing arithmetic, order types, session boundaries, FIX states, realised variance and waiting times, 16 October 2026

Corrections to order books and order flow review (`d40d4c2`), run before order matching and fragmentation review; the order books and order flow review record above is left as written, and this record supersedes it where they differ. Each correction is reproduced in `notes/artefacts/market-simulation/order-flow-checks.py` (run with numpy and scipy); the other results of that script are unchanged.

1. **Trade signing, `meth:trade-sign-classification`.** The order books and order flow review check computed the midpoint in binary floating point, so $(10.00+10.01)/2=10.004999\dots$ and the half-tick midpoint trade at 10.005 after a downtick returned $+1$ (a buy); the order books and order flow review record's "four toy trades" therefore included one wrong result, although the entry's wording happened to state the right rule. The check now holds prices as `Decimal` values built from strings, signs zero ticks by the last non-zero change, and asserts ten cases: half-tick and whole-tick midpoints after up- and downticks, zero upticks and zero downticks, a midpoint with no prior change (unclassified), trades just above and below a half-tick midpoint, and trades at the bid and ask against the previous tick. All ten pass; the entry's *Checked* sentence states them.
2. **Order type against aggressiveness, `def:limit-order-book`.** The entry said an order that matches on arrival *is* a market order. That is Bouchaud et al.'s event convention (p. 45), now named as such; Harris's market order is an instruction to trade at the best price (p. 71), and a marketable limit order can execute at once while limiting its price (p. 73). A crossing limit order executes the matching part and rests the rest at its limit (Bouchaud et al., p. 45) unless an immediate-or-cancel instruction removes it (p. 55).
3. **Session boundaries, `mech:order-lifecycle`.** "An order book is empty at the start of the day" was stated as universal. Lehalle and Laruelle say "most often empty" (p. 217); the entry now attributes it and adds Harris's day and good-till-cancel orders (pp. 82–84, Table 4-3) and FIX 4.4's TimeInForce (an absent value means "Day (or session)"; good till cancel and good till date exist), so orders carried across sessions rest in the reopened book. A dated CME rule could not be read (CME's site refuses scripted access; not circumvented) and is a backlog stub (`conv:session-carry-over`).
4. **FIX 4.4 states, same entry.** "Replaced" was listed among OrdStatus values from a vendor page that itself marked it as replaced in FIX 4.3. Checked against the FIX Trading Community's FIX 4.4 Orchestra repository (FIX.4.4_EP311) as rendered by Orchimate, to which FIXimate links: OrdStatus (39) has new, partially filled, filled, done for day, cancelled, pending cancel, stopped, rejected, suspended, pending new, calculated, expired, accepted for bidding and pending replace, and no value 5; ExecType (150) "describes the specific ExecutionRpt ... while OrdStatus (39) will always identify the current order status", with 5 = Replace and F = Trade. The entry and a new source key `fix44-orchestra` say so; the OnixS key is kept in the sources with a note that it was superseded.
5. **Realised variance, `meth:realised-variance-signature-plot`.** The limits to integrated variance and covariance are now attributed to Lehalle and Laruelle's "Itô semi-martingale framework" and restricted to continuous Itô processes; with jumps the limits are the quadratic variation and covariation, including co-jumps. Counterexample (computed): a unit-jump Poisson path with five jumps on [0, 1] has zero diffusion variance and realised variance 9 on a 10-step grid, 5 from 10^4 steps; three common jumps of +1 and −0.5 give realised covariance −1.5. The finite-grid expectation $\sigma^2T+2n\sigma_\eta^2$ is stated as exact for the simulated driftless Brownian model with i.i.d. centred noise independent of it, not for general semimartingales.
6. **Waiting times, `mod:queue-reactive-intensities` and the script.** "Equal in expectation only for a Poisson process" was wrong. For a stationary renewal process with finite second moment the mean wait from an arbitrary time is $E[X^2]/(2E[X])$, equal to $E[X]$ exactly when the coefficient of variation is 1. Counterexample: gaps 0.5 with probability 0.8 and 3 with probability 0.2 have $E[X]=1$, $E[X^2]=2$, CV 1, and a simulated mean wait of 1.0006 against a mean gap of 0.9997. The valid point is kept: the Hawkes sample's gaps (CV 1.37) give a mean wait from uniform starts of 0.594 against a mean gap of 0.405, near $E[X^2]/(2E[X])=0.579$.

Source statements and derived corrections are kept apart in the entries: items 2–4 restate sources more exactly, items 1, 5 and 6 are derivations and computations.

## order matching and fragmentation review: the rest of the orders-and-matching folder (order types, matching, hidden liquidity and dark trading, routing and fragmentation), 16 October 2026

Source checking, not study.

### Sources, 2026-10-16

- `alpha-harris`, 2002 printing via macOS PDFKit (printed = PDF − 13): pp. 68–86, 115–136, 304, 327–328, 382–384, 520–521, 526–534.
- `alpha-laruelle`, 2018 printing (printed = PDF − 27): pp. 5, 33–39, 62–73, 102–115, 117–140, 153–185, 247–260, 284–292; page images of pp. 35, 255, 257, 288 and 291.
- `catalogue-0528` (printed = PDF − 19): pp. 45, 55–56.
- `fix44-orchestra` (new key): FIX 4.4 OrdStatus, ExecType, TimeInForce, OrdType and ExecInst code sets via Orchimate, retrieved 2026-10-16.
- Not read: Zhu (`wide-zhu-dark-pools`, catalogue metadata only), Moallemi and Yuan (`wide-moallemi-yuan-queue`), Buti, Rindi and Werner, Budish et al.'s batch-auction sections, O'Hara and Ye, Foucault and Menkveld, the current EU and U.S. rules, and CME's documentation (scripted access refused).

### Numerical checks

`notes/artefacts/market-structure-execution-quality/order-routing-fragmentation-checks.py` (numpy, scipy; fixed seeds; run with `/opt/homebrew/bin/python3.10`): Harris's Table 6-1 call clears 7 at 20.0 by maximum volume, surplus 1.6 against 1.0 continuously (exact fractions), Bif's average 20.15; pro-rata 18 against 10 and 20 gives 6 and 12, POSIT 1,000 and 2,000, 10 against three 3s leaves one lot after floors and 7 against 1, 1 and 100 floors the small orders to nothing; the posting threshold's sign in three cases; the ex-fixing share 0.50 against the printed 0.60; FEI 0.854 and 0.676 with an empty venue; Lorenz and mean-difference Gini agree (0.565); KS fails to reject different normals in 89 percent of 30-sample trials; the binomial standard error 0.010 against 0.047 with venue choices repeated in runs of 20; the SOR model with the described update takes (0.95, 0.03, 0.02) to (0.52, 0.27, 0.21), and at a grid optimum the size-weighted first-order terms are near equal; a cross-venue gap beyond costs.

### Findings on the earlier notes

**Source identification.**

- **Harris** (`alpha-harris`): order instructions (chap. 4, pp. 68–86), precedence, matching and trade pricing, crossing networks, price ownership and derivative-price risks (chap. 6, pp. 115–136), order choice (chap. 14, p. 304), sunshine trading (sec. 15.3, pp. 327–328), exposure (chap. 18, pp. 382–384), internal crossing (sec. 25.4, pp. 520–521), consolidation and fragmentation (chap. 26, pp. 526–534).
- **Lehalle and Laruelle** (`alpha-laruelle`): market share and its metrics (chap. 1, sec. 1.1.1, pp. 33–39), SOR (sec. 1.2, pp. 62–73), dark pools (sec. 1.4, pp. 102–115), auctions, matching curves and volume curves (chap. 2, sec. 2.1, pp. 117–140), spreads, resilience and coverage (secs. 2.3–2.4, pp. 153–163), Spain and the 2010 outage (sec. 2.5, pp. 170–185), FEI (app. A.1), the SOR toy model (A.3), market-share estimation (A.8), Gini and KS (A.9); sec. 3.4.2 was already the source of the existing routing entries.
- **Bouchaud et al.** (`catalogue-0528`): order categories and order types (pp. 45, 55), the auction price (p. 56).
- **FIX 4.4** code sets (`fix44-orchestra`): OrdType, TimeInForce, ExecInst.
- Not found in any source read: the earlier notes' venue-selection list and routing-cost formula, frequent batch auctions' "muted" time priority (Budish et al.'s batch-auction sections not read), pegging references, the Gini for participants and time segments, leave-one-out estimators, and "subsidised share" beyond Turquoise's 2009 episode; each is marked interpretation, narrowed or stubbed.

| Blocks | Entry | Disposition |
|---|---|---|
| *Order*; *Order-Instruction Segmentation*; *Core Order-Type Segmentation*; *Market Order Cost Segmentation*; *Conditional Activation*; *Stops Are Not Limits*; *Tick-Sensitive Orders*; *Time-in-Force*; *Quantity and Handling*; *Special Instruction*; *Instruction Semantics Are Venue-Specific* (11) | `def:order-instructions` (new) | Rewritten from Harris chap. 4 and FIX 4.4; IOC/FOK naming conflict recorded; pegs attributed to FIX, not Harris; T+3 marked historical; venue semantics stubbed |
| *Marketable Limit Order* | `def:limit-order-book`, `def:order-instructions` | Merged; remainder rule (Harris p. 126) |
| *Order Choice Trades Certainty for Leakage*; *Market vs Limit Order Choice*; *Limit-Order Fill Threshold* (with proof); *Spread-Only Rules Fail* (4) | `res:limit-order-options` | Merged; Harris p. 304 and Table 14-1; threshold derived and computed; spread-only rule reframed by information |
| all 18 (principle, procedure, continuous and call matching, frequent batch auctions, pricing rules and incidence, auction rules, surplus, schedules, lemma and proposition with proofs, randomised uncrossing, priority, public order precedence, pro-rata, matching curve, indicative volume) | `mech:order-matching-pricing` (new) | Rewritten from Harris chap. 6 and Lehalle–Laruelle chap. 2; pro-rata remainders computed; frequent batch auctions stubbed (`hft-market-design`); public order precedence and random ends dated |
| *Dark Pool*; *Reference Price Trading*; *Crossing Network Rules*; *Price Ownership*; *Dark Liquidity Pools*; *Integrated vs Midpoint Books*; *Dark Pools and Price Discovery*; *Derivative Pricing Risks*; *Dark Activity Drivers*; *Why Investors Use Dark Pools*; *Dark Liquidity Is Conditional*; *Toxic Liquidity and Gaming*; *Bilateral vs Multilateral*; *Internal Crossing Agency* (14) | `def:dark-pools-crossing` (new) | Rewritten; "volatile periods" **qualified** (true of LL's dark turnover, not of dark share, against Buti et al. as reported); Zhu and Buti not read |
| *Reserve and Iceberg Display*; *Discovering Hidden Size*; *Order Exposure Decision*; *Exposure Benefit-Cost*; *Parasitic and Defensive Suppliers*; *Exposure Defence* (6) | `def:order-exposure-decisions` | Merged; Harris pp. 84–85, 117, 382–384 |
| *Block Exposure-Control*; *Sunshine Trading Credibility*; *Block Hanging Over the Market* (3) | `def:block-trade` | Merged; sunshine trading added; Table 15-1 already present |
| *Routing After Fragmentation*; *Smart Order Routing*; *Temporal Then Spatial*; *SOR Feedback Loop*; *Venue Selection*; *Consolidation Loop*; *Consolidation Bound* (with proof); *Aggregated Liquidity*; *Average Trade Size*; *Duplicate Liquidity*; *Transparency Is Not Certainty*; *Fragmented Routing Objective* (12) | `def:smart-order-routing` | Merged; LL sec. 1.2.1 and Harris sec. 26.4; bound derived; venue list and cost formula marked as the notes' synthesis |
| *Toy SOR Model*; *SOR Share Feedback*; *SOR Fragmentation Drivers*; *Primary-Market Variance Feedback* (4) | `mod:sor-market-share-dynamics` (new) | Rewritten; three printed slips and the first-order condition **corrected**; the "finding" reclassified as a model result |
| *Market Share as Routing Prior*; *Venue-Share Estimator*; *Index-Level Venue Share*; *Estimator Comparison*; *Metric Choice*; *Market Share Segmentation*; *Market Share Is Conditional*; *Intraday Non-Stationarity*; *Volume-Curve Segmentation*; *Event-Driven Volume Clustering*; *Reference Rules Create Volume* (11) | `meth:venue-market-share` (new) | Rewritten; ex-fixing formula **corrected**; Bernoulli assumption tested |
| *FEI*; *Fragmentation Measurement Segmentation*; *FEI Venue Count*; *Fragmentation of What*; *Coverage*; *Gini Liquidity Imbalance*; *Lorenz-Curve Gini*; *Gini Measurement Segmentation*; *KS Test*; *Venue-Share Distribution Comparison* (10) | `meth:fragmentation-concentration-metrics` (new) | Rewritten; LL's "H0 accepted ... same distribution" **corrected** to failure to reject; Gini inconsistency flagged |
| *Intraday Venue-Share Shape*; *Liquidity and Capitalisation*; *Why Large Caps Fragment First*; *Subsidised Share*; *Post-Trade Barriers*; *Spain*; *Spread-Share Feedback*; *Venue Quality*; *HFT Perimeter*; *Primary Outage*; *Fragmentation Needs Shared References* (11) | `ev:european-fragmentation-evidence` (new) | Rewritten with samples and periods; Spain treated as a confounded comparison |

### Checks and their limits

| Source | Passages | Limits |
|---|---|---|
| `alpha-harris` | as listed | 2002 U.S. institutions; Harris's own views on IOC/FOK naming |
| `alpha-laruelle` | as listed | European data 2006–2013; several printed slips; claims reported without sources (variance and share; HFT shares) |
| `catalogue-0528` | pp. 45, 55–56 | Definitions only |
| `fix44-orchestra` | five code sets | A third-party rendering of the Community's repository; message vocabulary, not venue behaviour |

The seven new entries and nine changed entries are *partly checked*, *draft*; **human review is outstanding**.

### Independent review

An integrated review by the same session after writing, with the three checkpoints, rechecked every quotation in the new and changed entries by script against the text layers and the FIX pages, the locators against printed-page offsets, and the mathematics (auction schedules, surplus, pro-rata, ex-fixing share, FEI, Gini, KS, the SOR first-order condition and update sign). Fixed before commit: the variance-feedback pitfall, which first claimed that the earlier notes' direction of the feedback contradicted Lehalle and Laruelle (it does not for a noisier alternative venue; the error was calling a model result empirical), and the dark-trading pitfall, which first rejected "volatile periods" outright (it holds for dark turnover). **Human review is outstanding.**

### For review

- Correcting Lehalle and Laruelle's ex-fixing formula, the A.3 update sign and the A.6 condition, and their KS conclusion, by derivation and computation without errata.
- Using a third-party rendering of the FIX Orchestra repository for FIX 4.4 values.
- Leaving pro-rata remainder rules, session carry-over and current EU dark-trading caps as stubs because the primary venue documents were not readable here.

## order matching and fragmentation review follow-up: pro-rata capacity, posting against crossing, the ex-fixing domain, fixed-weight venue-share variance and the SOR objective, 16 October 2026

Corrections to order matching and fragmentation review (`4d9d5da`), run before market design and liquidity review; the order matching and fragmentation review record above is left as written, and this record supersedes it where they differ. Each correction is reproduced, with assertions, in the rewritten `notes/artefacts/market-structure-execution-quality/order-routing-fragmentation-checks.py` (numpy and scipy, fixed seeds; exit 0 with `/opt/homebrew/bin/python3.10`); its other results (Harris's call, POSIT, FEI, Gini, KS, the cross-venue bound) are unchanged.

1. **Pro-rata allocation, `mech:order-matching-pricing`.** The order matching and fragmentation review example "10 against three resting orders of 3 leaves one lot after floors" confused two quantities. The executable quantity is first capped by the eligible resting liquidity: 10 against 3, 3 and 3 executes 9 and leaves 1 of the *incoming* order unexecuted, which rests or cancels by its own instructions; nothing is rounded. A rounding remainder arises only when proportional shares of the executable quantity are fractional: 10 against 4, 4 and 4 gives $10/3$ each, floors of 3 and one lot for the venue's further rule. A `pro_rata()` function computes capacity, exact shares, floors, rounding remainder and incoming residual, and asserts $\text{executed}\le\min(Q,\sum q_i)$, each allocation $\le q_i$, and $\text{floors}+\text{remainder}+\text{residual}=Q$ for undersubscribed (10 vs [4,4,4]), equal (12 vs [4,4,4]) and oversubscribed (10 vs [3,3,3]) cases, plus Harris's 18 vs [10,20] and 7 vs [1,1,100].
2. **Posting against crossing, `res:limit-order-options`.** An earlier threshold $p(S-A)-(1-p)M$ charged the post-fill fall $A$ to posting alone. Re-derived from explicit cash flows for the same target quantity and a common terminal mark $c_T$: crossing pays $a_0$; posting pays $b_0$ on a fill, otherwise the chase price; the gain of posting is $pS-(1-p)M$ with $S=a_0-b_0$ and $M=E[\text{chase}-a_0\mid\text{miss}]$, because a fall after a fill hits both positions equally. Examples: fill at 99 against buying at 100, marked at 97, gains +1; a miss chased at 101.5 loses 1.5. Pathwise check on 200,000 random-walk paths: $P(\text{fill})=0.432$, mean gain $-0.0457$, equal to $pS-(1-p)M$; the old formula gives $-0.3127$ ($A=+0.618$). Adverse selection now enters through $p$ and $M$; the entry states when a separate $A$ would be justified (different terminal quantities).
3. **Ex-fixing share, `meth:venue-market-share`.** "Agrees only when $m(n)=0$" was too strong. The derived $(\mathfrak M-mp)/(1-p)$ equals the printed $(1-mp)\mathfrak M/(1-p)$ exactly when $m\,p\,(1-\mathfrak M)=0$: no auction volume at the venue, no auctions, or a monopolist ($\mathfrak M=m=1$, share 1 under both). Domain stated: $0\le p<1$, $0\le m\le1$, $mp\le\mathfrak M\le mp+1-p$; undefined at $p=1$. Asserted for (0.6, 1, 0.2) → 0.5 against 0.6, (0.7, 1, 0.25) → 0.6 against 0.7, and the agreeing cases $m=0$, $p=0$ and the monopolist.
4. **Venue-share variance, same entry.** The order matching and fragmentation review entry restated Lehalle and Laruelle's $\operatorname{Var}(\hat p_k-\hat p)=(1-2w_k)p_k(1-p_k)/n_k+p(1-p)/n$ (sec. A.8.3, p. 288) without testing it. For the fixed-weight index $\hat p=\sum_jw_j\hat p_j$ with independent estimates, $\operatorname{Var}(\hat p_k-\hat p)=(1-w_k)^2\sigma_k^2+\sum_{j\ne k}w_j^2\sigma_j^2$; with dependence, $a^\top\Sigma a$ for $a=e_k-w$. The printed form replaces $\sum_jw_j^2\sigma_j^2$ by a pooled binomial variance, which has no basis for an arbitrarily weighted index: $w=(0.9,0.1)$, $p=(0.5,0.5)$, $n=(100,100)$ gives 0.00005 (simulated 0.000050) against $-0.00075$ printed with $n=200$. Sample sizes are now defined (trades per stock); count shares ($\sigma^2=p(1-p)/n$ under independent identical trials) are distinguished from value shares ($p(1-p)/n_{\text{eff}}$, $n_{\text{eff}}=(\sum v)^2/\sum v^2$; 92 of 2,000 lognormal trades, sd 0.0478 by simulation and formula). The textbook formula is recorded as an unsupported simplification.
5. **SOR objective and simulation, `mod:sor-market-share-dynamics`.** The first-order condition is now stated with its marginal value $h_k(r_k)=E[V\mathbf 1\{r_kV<D_k\}]$: equal to $\lambda$ for every venue with $r_k>0$ (interior), $h_k(0)\le\lambda$ for a venue at zero (boundary). Two-scenario counterexample ($V=1$, $D=(0.4,0.6)$; $V=10$, $D=(6,4)$, equally likely): $(0.5,0.5)$ equalises the unweighted indicators and captures 4.95; $(0.6,0.4)$ captures 5.4, the grid optimum. The order matching and fragmentation review simulation set $E[D_k]=p_k$ instead of the book's $E[D_k/\sum D]=p_k$ (eq. A.10), made $V$ depend on $D$ and used unweighted indicators; its claim to reproduce the 50/25/25 path is **withdrawn**. Replaced by an explicitly illustrative variant: $D_k=\mu_kX_k$, $X_k$ i.i.d. lognormal with $\nu=0.8$ (chosen here), $V$ independent with $E[V]=\sum\mu_k$, means calibrated each period to $E[D_k/\sum D]=p_k$ (calibrated $(0.9709, 0.0175, 0.0115)$ for $(0.95,0.03,0.02)$), $a=0.3$, projected stochastic gradient ascent with the size-weighted indicators. An exact KKT solver gives keys $(0.99888, 0.00056, 0.00056)$ with equal marginal values 0.3412 (interior); the learner's averaged keys are within 0.001. By scale invariance the optimal key is $\mu_k/\sum\mu$ (checked: means (0.6, 0.25, 0.15) give those keys), so the largest venue's key exceeds its share and the variant concentrates, to $(0.998, 0.001, 0.001)$ after 60 periods. It does not reproduce the book's path, which depends on an unreported $\nu$ and the printed update.

Source statements and derived corrections are kept apart: items 1, 2 and 5 are derivations and computations; items 3 and 4 correct the order matching and fragmentation review restatement of Lehalle and Laruelle and the book's own formula by derivation, without errata. Notes changed: `execution-market-making` and `market-structure-execution-quality` pathway notes, the `alpha-laruelle` reading note. The order matching and fragmentation review index row in `notes/source-review-index.md` keeps `4d9d5da`.

## market design and liquidity review: the foundations folder (roles of markets, participants and motives, venues, auction and dealer structures, market quality, regulation and structural evolution; six files, folder closed), 16 October 2026

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

### Findings on the earlier notes

**Source identification.** The first five files paraphrase Harris (chaps. 1, 3, 5, 7, 8, 9, 15, 19, 22, 24, 26–28) and Hasbrouck (chaps. 1–2) closely, with Lehalle and Laruelle's introduction and chap. 2 for the four liquidity variables, flow reactivity and the "Nyquist–Shannon latency bound". The regulatory file mixes Harris (chaps. 3, 9, 18, 26, 28, 29), Lehalle and Laruelle (introduction, chap. 1, sec. 2.5) and undated statements of U.S. and EU rules; every dated rule statement was rebuilt from primary texts. Additions in the earlier notes with no source found are named in each entry's Pitfalls (for example "funding" among spread components, "payoff convexity" for gamblers, the trading-edge list, "liquidity risk", "price continuity", "measurement risk", the tick-policy principle). Four propositions in the earlier notes were wrong or incomplete as stated (below).

| Blocks | Entry | Outcome |
|---|---|---|
| *Core Market Functions*; *Immediacy Has a Price*; *Trading Benefit Segmentation*; *Price Discovery*; *Risk Transfer*; *Capital Allocation*; *Informative Prices and Allocation*; *Mechanism Relevance*; *Microstructure Trade-Off* (9) | `def:market-functions` (new) | Rewritten from Harris chaps. 1, 3, 9 and Hasbrouck chap. 1 |
| *Zero-Sum Trading Accounting* (proposition with proof) | `res:zero-sum-skill-luck` (new) | Rewritten; the common-valuation condition stated |
| *Liquidity Provision* | `def:market-intermediaries` (new) | Merged as Harris's short list (p. 394) |
| *Trading Game View*; *Long and Short Positions*; *Motive Segmentation*; *Multiple Trader Identities*; *Patience Defines the Liquidity Side*; *Buy-Side Motives*; *Instrument Choice Follows the Problem*; *Hedge-Vehicle Fit*; *Profit-Motivated Trader Segmentation*; *Speculation Requires Comparative Advantage*; *Trading Edge Segmentation*; *Noise and Liquidity Traders*; *Futile Trader Segmentation* (13) | `def:trader-motives` (new) | Rewritten from Harris chap. 8; "payoff convexity", the edge list and the noise-trader definition flagged as the earlier notes' own |
| *Skill and Luck Look Similar Ex Post*; *Past Profit Alone Does Not Identify Skill*; *Profit-Motivated Flow Needs Non-Profit Motives*; *Turnover Drag for Active Management* (4, three with proofs) | `res:zero-sum-skill-luck` | Rewritten; the skill–luck proposition **restated with conditional mean independence of luck**, the corollaries' conditions stated; simulated |
| *Liquidity Supplier Segmentation*; *Dealers and Market Makers*; *Sell-Side Intermediaries*; *Broker Service Segmentation* (4) | `def:market-intermediaries` (new) | Rewritten from Harris chaps. 3, 7, 8, 19 |
| *Information-Motivated Traders*; *Informed Trader Liquidity Role Segmentation* (2) | `def:informed-trader-types` | Merged (pp. 194–196, 402–403) |
| *Arbitrageur Economic Function* | `def:arbitrage` | Merged (pp. 6, 404–405) |
| *Block-Trading Role Segmentation*; *Block Dealers vs Block Brokers*; *Block Trader Skill Segmentation* (3) | `def:block-trade` | Merged (pp. 328–330) |
| *Institutional Investors and HFTs*; *HFT Identification Markers*; *HFT as Fragmentation Link*; *Blurring of Roles* (4) | `def:hft-strategies` | Merged (Lehalle and Laruelle, pp. 5–6, 22) |
| *Tighter Spread, Different Cost*; *Investor Size Asymmetry* (2) | `res:hft-spread-investor-cost` | Merged as restatements; size asymmetry flagged as the earlier notes' own |
| *Venue as Rule System*; *Market-Structure Segmentation*; *Access Form Segmentation*; *Market-Centre Segmentation*; *Exchanges*; *Exchanges as Search Engines*; *OTC Markets*; *ECNs and ATSs*; *RFQ vs CLOB*; *Designated Market Maker Segmentation*; *Market Information Systems*; *Post-Trade Infrastructure*; *Brokered Credit Compression* (proposition with proof); *Architecture Choice*; *Straight-Through Processing* (15) | `def:market-structures-venues` (new) | Rewritten from Harris chaps. 3, 5, 7, 24, 26; the credit count's conventions and assumptions stated and checked |
| *Brokered Transaction Segmentation* | `def:market-intermediaries` | Merged (Table 7-1) |
| *Order-Flow Arrangement Segmentation* | `def:broker-agency-conflicts` | Merged; internal crossing and the EU payment-for-order-flow ban added |
| *Trading Systems and Technology*; *Automated Reporting Advantage* (2) | `def:floor-automated-trading-systems` | Merged (pp. 35, 97, 524–525) |
| *Stale Quotes and Vanishing Liquidity* | `def:smart-order-routing` | Merged into the latency paragraph |
| *Liquidity Bridges* | `def:hft-strategies` | Merged |
| *Execution-System Segmentation*; *Trading Session Segmentation*; *Continuous Auctions*; *Call Auctions*; *Fixing Auctions*; *Auction Session Segmentation*; *Dealer Markets*; *Brokered Markets*; *Hybrid Markets*; *Specialist Role Segmentation*; *Gold Fixing as Sequential Auction*; *Why Large Orders Like Calls*; *Auction Transparency Trade-Off* (13) | `def:trading-sessions-execution-systems` (new) | Rewritten from Harris chaps. 5, 24, 28 and Hasbrouck chap. 2; the gold fixing **dated** (1919–2015 from LBMA, the IBA auction as of October 2026) |
| *Open-Outcry Oral Auctions*; *Public Exposure Rule*; *Order-Driven Rule Stack*; *Priority and Access Rules* (4) | `mech:order-matching-pricing` | Merged (pp. 112–114) |
| *Floor vs Automated Auction Segmentation*; *Fast-Market Capacity Condition* (proposition with proof); *Floor Information Exchange* (3) | `def:floor-automated-trading-systems` | Merged; the capacity proposition **restated** as a necessary, not sufficient, queue-stability condition and simulated |
| *Reference Price Monopoly* | `meth:venue-market-share` | Merged (Hasbrouck p. 18) |
| *Market Quality*; *Liquidity*; *Liquidity as Bilateral Search*; *Search Stopping Rule* (proposition with proof); *Liquidity Search Strategy Segmentation*; *Four Liquidity Variables*; *Liquidity Risk*; *Tightness, Depth, and Resiliency*; *Price Continuity*; *Search-Output Liquidity Dimensions*; *Depth-Width Duality* (proposition with proof); *Displayed, Undisclosed, and Latent Liquidity*; *Book Size*; *Book Size Is a Lower Bound*; *Resiliency as Synchronisation*; *Value-Trader Resiliency*; *Liquidity State Drivers*; *Quality Trade-Offs*; *Intraday Liquidity Seasonality*; *Flow Reactivity* (20) | `def:liquidity-dimensions` (new) | Rewritten from Harris chap. 19, Hasbrouck chap. 1, Lehalle and Laruelle secs. 2.2–2.3; duality **given its attainment condition**; the search rule stated as one-step; "book size is a lower bound" **corrected** |
| *Public Benefits of Liquid Markets*; *Visible Activity vs Economic Importance* (2) | `def:market-functions` | Merged (pp. 45, 214–216) |
| *Transparency Paradox*; *Transparency Segmentation*; *Volume Is Not Directly Comparable* (3) | `def:market-structures-venues` | Merged (pp. 48, 101; Lehalle and Laruelle pp. 19–20) |
| *Latency and Book State*; *Nyquist-Shannon Latency Bound* (2) | `def:smart-order-routing` | Merged; the bound **not adopted as a theorem**: restated as a staleness condition with a computed probability |
| *Market Impact and Decay* | `def:price-impact` | Merged as a restatement |
| *Informational Efficiency* | `def:market-efficiency` | Merged (pp. 215–216) |
| *Bid-Ask Bounce*; *Spread and Depth Substitute Imperfectly* (2) | `res:spread-determinants` | Merged; already present, interpretations recorded |
| *Regulation as Market Design*; *Market-Design Question Segmentation*; *Welfare Evaluation*; *Policy Objective Segmentation*; *Regulatory Institutions*; *Regulatory Political-Economy Risks*; *Unintended Consequences*; *Regulatory-Service Segmentation* (8) | `def:market-regulation-design` (new) | Rewritten from Harris chaps. 3, 9, 26, 28 |
| *Fragmentation*; *Order-Flow Externality* (proposition with proof); *Levels of Fragmentation*; *Structural Evolution of Fragmentation*; *Post-MiFID Phases*; *Early MiFID Failures*; *Liquidity Segmentation*; *Market-Segmentation Motives*; *Technology Fragmentation*; *Cross-Market Precedence Failure*; *Consolidated Tape as Resilience*; *Competition to Merger*; *Electronification Beyond Equities* (13) | `mech:venue-competition-fragmentation` (new) | Rewritten from Harris chap. 26, Hasbrouck chap. 1, Lehalle and Laruelle; their inconsistent dates recorded; electronification also in `def:market-structures-venues` |
| *Decimalization*; *Reg NMS*; *Post-Flash-Crash Controls*; *Stub Quotes* (4) | `rule:us-equity-market-structure` (new) | Rebuilt from Federal Register, eCFR and SEC texts with adoption, effective, stay and compliance dates |
| *MiFID and MiFID II*; *Transparency and Dark Trading*; *MiFID II Dark Caps*; *MiFID Venue Statuses* (4) | `rule:eu-trading-venue-transparency` (new) | Rebuilt from EU texts (Publications Office) and ESMA statements; the double-to-single volume cap transition dated |
| *Circuit Breakers and Structural Controls*; *Circuit Breaker Scope*; *Extreme-Volatility Control Segmentation*; *Circuit Breaker Design*; *Halt Value Depends on Volatility Source* (proposition with proof); *Gravitational Effect*; *Propagation Problem*; *Price Limits and Margin Waterfall*; *Trading-Restriction Incidence* (9) | `mech:circuit-breakers-trading-halts` (new) | Rewritten from Harris chap. 28, Lehalle and Laruelle sec. 2.5.3, MiFID II Art. 48(5); the halt proposition identified as definitional |
| *Insider-Trading Restrictions*; *Insider-Trading Control Segmentation* (2) | `def:inside-information` | Merged; Rule 10b5-1 (2022 amendments), Form 4 and Regulation FD checked as of October 2026; Harris's superseded statements marked |
| *Insider-Trading Enforcement Logic*; *Insider-Trading Debate Segmentation*; *Insider-Trading Policy Trade-Off* (proposition with proof) (3) | `res:insider-trading-deterrence` | Merged (sec. 29.3); the trade-off identified as an accounting identity |
| *Exposure-Protection Rule Segmentation* | `def:order-exposure-decisions` | Merged (p. 389) |
| *Best Execution After Fragmentation* | `def:best-execution` | Merged (Lehalle and Laruelle pp. 17–19, 43) |
| *Broker Crossing Networks* | `def:dark-pools-crossing` | Merged (pp. 18, 55–56) |
| *Tick Size Reforms*; *Tick Size as Market Share Tool*; *Sub-Penny and Tick-Size Wars*; *Who Gains From Tick Changes*; *Tick Policy Design* (5) | `def:tick-size` | Merged (Harris pp. 114, 531, 537–538; Lehalle and Laruelle p. 15); the sub-penny rule in `rule:us-equity-market-structure` |

**Corrections to the earlier propositions.** (i) *Past profit and skill*: the proof needed $E[L_{t+1}\mid\mathcal F_t,\Pi_t]=E[L_{t+1}\mid\mathcal F_t]$; unconditional zero-mean luck does not suffice (AR(1) luck with mean zero gives a slope of 0.5), and when skill is unknown past profit is informative (slope $\tau^2/(\tau^2+\sigma^2)$). (ii) *Brokered credit*: correct as an unordered count under stated assumptions; Harris's sidebar counts ordered relationships ($2n+B(B-1)$ = 2,009,900; ratio 497,537, his "500,000"). (iii) *Depth–width duality*: needs the maximum to be attained (counterexample with a jump). (iv) *Capacity*: $N\lambda<\mu$ is necessary, not sufficient (queueing delays and bursts). The *Nyquist–Shannon latency bound* is Lehalle and Laruelle's heuristic (p. 23, page image), not a sampling-theorem result; the *halt-value* and *insider-trading trade-off* propositions are definitional; the *order-flow externality* is a rearrangement whose content is in its specification.

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

### Independent review

An integrated review by the same session after writing. Every quotation in the new and changed text (215) was checked by script against the text layers, the downloaded primary texts and the earlier notes; about 140 phrases were located to their printed pages to check locators. Fixed before commit: a sentence that attributed to Harris the remark that smoothing prices against informed flow "only transfers losses to liquidity suppliers" (now marked as interpretation, not Harris's); the broker-services pitfall, which first treated clearing and settlement as an addition to Harris's list (they are his first item); a misquoted phrase ("weaken" for "weakens"); the LULD band sentence (bands of 5 and 10 percent apply above $3.00 after the May 2012 amendment); and an underfull *Further reading* line. **Human review is outstanding.**

### For review

- The ownership split between the overview (conceptual) and `market-structure-execution-quality` (rules, competition, circuit breakers).
- The restated skill–luck proposition and the reading of Harris's credit count as ordered.
- Treating Lehalle and Laruelle's "Nyquist–Shannon latency bound" as a heuristic, not a theorem.
- Using the EU Publications Office's CELLAR service and WebFetch for SEC PDFs where EUR-Lex and sec.gov refuse plain scripted requests; no bot check was solved or bypassed.
- The compliance status of the U.S. 2024 tick and fee amendments (exempted to November 2027) and the EU single volume cap, which change often.

## market design and liquidity review follow-up: liquidity units, the current systematic-internaliser definition and U.S. currency, and queue stability and bursts, 16 October 2026

Corrections to market design and liquidity review (`063de31`), run before dealer models and information review; the market design and liquidity review record above is left as written, and this record supersedes it where they differ. No entry label or entry count changed (170 entries); one backlog stub was added and one narrowed (*Systematic internaliser and U.S. currency*). Numerical corrections are reproduced, with assertions, in the rewritten sections 4 and 8 of `notes/artefacts/execution-market-making/liquidity-market-design-checks.py` (numpy; fixed seeds; exit 0 with `/opt/homebrew/bin/python3.10`); its other sections give byte-identical output (compared by script with the output before the change).

1. **Liquidity dimensions, `def:liquidity-dimensions`.** Harris states width as "the cost per unit of liquidity" and depth as "measured in units available at a given price of liquidity" (pp. 398--399, rechecked). The market design and liquidity review entry wrote $D(c)=\max\{q:C(q)\le c\}$ with $C$ an all-in (total) cost and $c$ a "cost budget", and its script inverted a cumulative cost: that answers a cash-budget question, not Harris's. Counterexample: midpoint 99, 100 shares offered at 100: per-unit cost 1, depth at per-unit cost 1 is 100 shares; inverting total cost at a budget of 1 gives one share. The entry now defines a size domain (positive lot multiples or $[q_{\min},\bar q]$; per-unit cost undefined at zero), the per-unit cost $w(q)$ in currency per share, depth $D(\bar w)$ in shares and total cost $C(q)=q\,w(q)$ with a budget $K$ as a separate object; distinguishes average from marginal per-unit cost (depth at 1.5 is 200 against 100 shares with 100 more at 101); notes that a fixed fee per order makes $w$ fall with size, so the equivalence can fail (feasible set {100} at 1.5 with a fee of 50, while $w(50)=2$); and states attainment correctly: on an interval the maximum exists if and only if the feasible set is nonempty, bounded and contains its supremum; a compact domain with $w$ lower semicontinuous suffices, lower semicontinuity is not necessary (an upward jump at 2 with the maximum 1 attained) and does not give a finite maximum without boundedness. Source statement (the per-unit units and the duality) and interpretation (the formalisation) are kept apart.
2. **Systematic internaliser and U.S. currency, `rule:eu-trading-venue-transparency` and `rule:us-equity-market-structure`.** The 2014 definition ("organised, frequent systematic and substantial basis", pre-set quantitative limits for both, opt-in already available) is now dated as historical. The current definition is quoted from Directive (EU) 2024/790, Art. 1 point (3)(b): "on an organised, frequent and systematic basis, deals on own account in equity instruments \dots\ or which opts in"; recital (7) gives the reasons (excessive burden of the quantitative criteria; qualitative assessment for equity instruments only; non-equity pre-trade transparency removed for systematic internalisers by Regulation (EU) 2024/791; opt-in possible for non-equity instruments), and Commission Delegated Regulation (EU) 2026/392, recital (1), reads it the same way. Dates: the directive of 28 February 2024, published 8 March 2024, in force on the twentieth day, transposition due 29 September 2025 (Arts. 2--3), national measures not checked; the delegated regulation of 20 February 2026, published 1 June 2026, in force on the twentieth day (Art. 2). U.S.: Release 34-104612 (15 January 2026) exempts the plan participants from Rule 600(b)(69)(ii), aggregate odd-lot depth at or between the NBBO, until the first business day of May 2028, and not from Rule 600(b)(69)(iii), the best odd-lot order; Release 34-94441 (16 March 2022) approved NYSE's market-wide circuit breakers on a permanent basis, with Amendment No. 1's testing and reporting duties (other venues' 2022 filings not read); the 2024 tick and fee amendments took effect on 9 December 2024 (Federal Register record) and are effective rule text whose compliance Release 34-105656, read in full in its Federal Register version, exempts to the first business day of November 2027. Six source keys added or updated: `eu-dir-2024-790`, `eu-reg-del-2026-392`, `fr-2024-21867`, `sec-34-104612`, `sec-34-94441`, `sec-34-105656` (updated).
3. **Queue stability and bursts, `def:floor-automated-trading-systems`.** For the M/M/1 queue the condition $\mu>N\lambda$ is necessary and sufficient for stability; market design and liquidity review called it "necessary, not sufficient", conflating stability with delay. The entry now separates stability from waiting time ($\rho/(\mu-N\lambda)$), time in system ($1/(\mu-N\lambda)$) and deadline misses ($e^{-(\mu-N\lambda)d}$), and replaces "peak, not average, rates decide" with conditions on burst duration, backlog, buffering and deadlines. The market design and liquidity review burst simulation drew each gap from the rate at the previous arrival, inexact across rate boundaries; reproduced, its realised rate was 799.8 per second against the stated 798, and it did not separate waits from time in system. Section 8 now samples arrivals by thinning (exact for the piecewise-constant rate), sets the low rate so the average is exactly 0.8 of capacity (0.7222 of capacity outside bursts; realised 800.2 per second), checks the constant-rate case against the M/M/1 formulas (mean wait 3.94 against 4.00 ms, mean time in system 4.94 against 5.00 ms, 99th percentiles 20.6 and 21.7 against 21.9 and 23.0 ms, $P(T>10\text{ ms})$ 0.131 against 0.135, all asserted), and reports the bursts (mean wait 12.53 ms, time in system 13.53 ms, 99th percentile 72.9 ms, share over 10 ms 0.343; backlog at the end of a burst near the fluid 50 messages), shorter bursts at the same peak and average (99th percentiles 25.8 and 22.5 ms for 20 and 5 ms bursts), a finite buffer of 20 (4.8 percent rejected with bursts, 0.29 percent at a constant rate against 0.23 percent in the M/M/1/20 formula) and overload at 1.05 (waits of 2.5 and 4.6 s after 50 and 100 s). Every affected number in the entry was refreshed.

Source statements and derived corrections are kept apart: items 1 (units) and 2 restate sources more exactly; items 1 (attainment) and 3 are derivations and computations. Notes changed: the `execution-market-making` and `market-structure-execution-quality` pathway notes (two backlog stubs updated or added: `rule:us-market-wide-circuit-breakers-current` narrowed, `rule:eu-si-national-transposition` new). The market design and liquidity review index row in `notes/source-review-index.md` keeps its commit.

## dealer models and information review: market making, information and volatility, and feature and data engineering in the earlier microstructure notes, 16 October 2026

Source checking of the remaining earlier microstructure notes (market making; information and volatility; feature and data engineering), run after the first market design and liquidity review follow-up (above). Not study.

### Source identification

- **Market making.** The economics and optimal-quoting notes paraphrase Harris chap. 13 (dealers, pp. 278--283), chap. 16 (p. 344) and chap. 24 (specialists, pp. 495--511, the tick-size box on p. 500); the participation-option inequality is the earlier notes' formalisation of p. 499. The latency notes' previously unidentified source is Lehalle and Laruelle's app. A.2 (pp. 250--254, page images of pp. 252--253), a summary of Foucault, Kadan and Kandel (2009 working paper; not read); their "latency as queue option" is unsourced, and was checked against Moallemi and Yuan (`wide-moallemi-yuan-queue`, previously unread; the June 2017 revision read in part). The cross-asset notes paraphrase Harris chap. 17 (pp. 349--378).
- **Information and volatility.** Lehalle and Laruelle sec. 2.5 (pp. 169--186) and app. A.5 (pp. 261--266, page images), with the 2010 CFTC--SEC staff report (executive summary) for the event and Hasbrouck chap. 10 for price discovery across venues.
- **Feature and data engineering.** The feature notes have no source; their content is relative-value arbitrage material in Harris's terms (chap. 17), a comparative-advantage principle (Harris p. 196) and label design (López de Prado chap. 3). The data-engineering notes follow Lehalle and Laruelle's apps. A.8, A.10 and A.14 (proportions, regression, the averaging effect), Harris chap. 22 (tests of skill and luck, unattributed in the earlier notes) and, for feeds and identifiers, match Velu, Hardy and Nehren chaps. 1 and 11; drop copies, clearing feeds and the identifier attribute list are the earlier notes' own. Neither file states a multilevel or cross-asset OFI result.

### Source findings

- **Dealers and specialists** (`def:dealer-quotes-order-flow`, `def:specialist-obligations-privileges`, `def:outside-spread`). Rewritten from Harris chaps. 13 and 24 (as of 2002); the compensation list and "wide quote is information" marked as the notes' interpretation; the 2002 U.S. figures dated; current designated-market-maker rules not read. The participation-option inequality is marked as an interpretation of p. 499; the tick-size box is p. 500. The dealer-against-outside-spread comparison restates pp. 344--345.
- **Queue position** (`res:queue-position-value`). Rewritten from Moallemi and Yuan; the earlier claim that queue value matters in "thin" queues is **contradicted**: the value is large in long, large-tick queues.
- **Make--take fees and the speed race** (`mod:make-take-fee-speed-race`). Source identified as LL app. A.2; the race intensities $\bar\mu,\bar\tau$ are sums, not "averages" (**corrected**); eq. (A.4) re-derived as the trade-maximising fee split and checked against exact finite-population equilibria; printed slips recorded; the cost list and the competition diagnostic marked as interpretation. The claim that fast liquidity improves price discovery is marked as interpretation (the model has no price discovery), with LL's question about fee schedules and the PFP.
- **Arbitrage** (`def:arbitrage`, `res:arbitrage-risks`). Harris's arbitrage material (pp. 349--378, 366--367); the triangular FX equality after costs restated as a bid--ask band, derived and checked; Harris's currency box (p. 357) found internally inconsistent and recomputed; the capital-constraint generalisation marked as the notes'. The factor-residual view **corrected** for a hedge ratio $h$: exposure $\beta_i-h\beta_j$, not $\beta_i-\beta_j$.
- **Fragmentation, outages and systemic risk** (`mech:venue-competition-fragmentation`, `ev:european-fragmentation-evidence`). Hasbrouck's information shares; the general fragmentation claim marked as synthesis; the systemic-risk conditions (LL pp. 169, 177) marked as plausible mechanisms. The Euronext outage of 13 October 2010 (pp. 183--186), with the captions' date slip recorded.
- **Flash crashes** (`mod:depth-overflow-flash-crash`, `ev:may-2010-flash-crash`). Rewritten from LL and the staff report; the time term of (A.14) **resolved by derivation** (rounds, the overflow bound; (A.14) needs the overflow); the earlier $\rho$ wording corrected; the control list marked as synthesis; the reference-price channel placed with the Euronext outage.
- **Trade count as an HFT proxy** (`def:hft-strategies`). LL pp. 20--21 and 170--171, with the staff report's warning about volume.
- **Comparative advantage and labels** (`def:trader-motives`, `meth:triple-barrier-labelling`). Harris p. 196; AFML p. 44, with the earlier label categories marked as the notes'. No source was read for microstructure-alpha evaluation; it stays a backlog stub (`meth:lob-signal-transaction-usefulness`).
- **Market data and identifiers** (`data:market-data-levels`, `data:trading-reference-data`). Timestamps, sequencing, availability and corrections added from Hasbrouck p. 105 and Velu chap. 11; drop copies and clearing feeds marked as the notes'.
- **Proportions** (`meth:venue-market-share`). LL A.8; the normal-approximation rule of thumb stated with the true $p$, not its estimate; Wald and Wilson coverage computed.
- **Regression and averaging** (`meth:spread-volatility-regression`, `meth:intraday-deseasonalisation`). LL A.10 and A.14; the two $R^2$ forms distinguished; the spread-aggregation identity limited to price-unit spreads; LL's $\bar a_1$ slip recorded; the averaging effect from A.14.1.
- **Skill and luck** (`meth:skill-luck-significance-tests`). Rewritten from Harris chap. 22; the power proposition restated with its error rates, $n=((z_{1-\alpha}+z_{1-\beta})\sigma/\mu)^2$, the expected-$t$ statement large-sample only; Harris's tables recomputed (the Buffett-box probabilities not reproduced exactly; its method unstated).

Source slips recorded, not silently fixed: Harris's currency box (p. 357); Lehalle and Laruelle's A.2 indices and cost scaling, its "$\Gamma-\bar c$ obviously larger than $s\Delta$" (a counterexample was computed), A.5's round-indexed $t$ and (A.14), A.14.2's $\bar a_1$, and the outage captions' date.

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

### Independent review

An integrated review by the same session after writing, against the diff. Every quotation on added lines (181 distinct) was checked by script against the text layers of the sources and the earlier notes; the misses were pre-existing quotations on modified lines, metadata strings checked by eye, or math stripped by the script, except two, fixed: Harris's "by decreasing the cost of stepping in front of booked orders" (the draft had "decreases") and the earlier notes' "follows volume mechanically". Locators were checked against the printed-page offsets. Also fixed: a generalisation that the index slope "is steeper" (now what the simulation and a derivation show), the claim that Harris "does not discuss" ETFs or ADRs (limited to his arbitrage chapter), the opt-in described as new in the follow-up's first draft (it was already in the 2014 text) and a Delegated Regulation citation narrowed to its recital. **Human review is outstanding.**

### For review

- Placing the cross-asset notes with the arbitrage entries rather than with inventory hedging or latency races, and the data-engineering material with point-in-time data, venue market share, spread regression and skill-and-luck tests.
- Reading eq. (A.4) as the trade-maximising fee split, and the resolution of (A.14)'s time term, both by derivation without the original paper or errata.
- Correcting Harris's currency box, and the Buffett-box probabilities not reproduced exactly.
- Using Moallemi and Yuan's 2017 revision where the catalogue records 2016, and the staff report's executive summary only.

## dealer models and information review follow-up: the triangular no-arbitrage band, 16 October 2026

Correction to dealer models and information review (`ca6986e`), run before macro markets and pricing review; the dealer models and information review record above is left as written.

1. **Triangular FX arbitrage, `def:arbitrage`.** dealer models and information review kept an exact triangular equality of cross rates alongside the bid--ask band. The equality holds only in the frictionless case (single prices, no costs); with quotes, the synthetic and direct midpoints can differ while both executable cycles lose. The entry now restricts the equality to that case. Check: EUR/USD 1.0999/1.1001, USD/JPY 109.99/110.01 and EUR/JPY 120.99/121.03 give a synthetic bid and ask of 120.978 and 121.022 and a synthetic midpoint of 121.00 against a direct midpoint of 121.01; the direct bid (120.99) is below the synthetic ask and the direct ask (121.03) above the synthetic bid, so the quotes overlap the synthetic band, and the two cycles return 0.99957 (via USD) and 0.99974 (via JPY) per euro, both below one. Reproduced, with assertions, in section 2 of `notes/artefacts/execution-market-making/dealer-queue-information-checks.py` (exit 0 with `/opt/homebrew/bin/python3.10`; the script's other sections and its random draws unchanged).

Notes changed: the `execution-market-making` and `fx-dealer-market-making` pathway notes; the entry's *Status*. The dealer models and information review index row in `notes/source-review-index.md` now carries its commit, `ca6986e`.

## market design and liquidity review follow-up (second): dimensionally consistent liquidity cost, 16 October 2026

A second correction to market design and liquidity review (`063de31`), after the first follow-up above; earlier records are left as written.

1. **Liquidity dimensions, `def:liquidity-dimensions`.** The entry's per-unit width $w(q)$ and total cost $C(q)$ were not stated in consistent units. It now says: with $w$ in currency per share, $C(q)=q\,w(q)$; with $w_{bp}$ in basis points of the midpoint $m$, $w=m\,w_{bp}/10{,}000$ and $C(q)=q\,m\,w_{bp}/10{,}000$. Check: 100 shares at a midpoint of 100 and a cost of 10 bp give a cash cost of 10 (0.10 per share). Reproduced, with assertions, in section 4 of `notes/artefacts/execution-market-making/liquidity-market-design-checks.py` (exit 0; other sections unchanged).

Notes changed: the `execution-market-making` pathway note; the entry's *Notation*, *Statement* and *Status*.

## macro markets and pricing review: global macro, regimes and data, cross-asset transmission and practitioner frameworks in the earlier macro notes, 16 October 2026

Source checking of the earlier macro notes (global macro, regimes and data; transmission across FX, equities, rates, credit and commodities; practitioner frameworks), run after the two follow-ups above. Not study.

### Source identification

- **Gliner, *Global Macro Trading* (`s7-gliner`).** A local PDF of the Wiley 2014 ebook (copyright page: Greg Gliner, Wiley, 2014; ISBN 978-1-118-36242-6 hardback, 978-1-118-42038-6 ePDF), 462 PDF pages, in the ignored `reading materials/`. The ebook has no printed page numbers; locators are chapter, section and PDF page, mapped from the PDF's outline and checked against the text, with no offset assumed. The regimes notes follow chaps. 1, 3, 11 and 12; the transmission notes chaps. 2, 4 and 7--10, often closely; chaps. 5 and 6 were not used.
- **Drobny, *Inside the House of Money* (`s7-drobny`).** The local copy is the Wiley 2006 printing (copyright 2006; ISBN-13 978-0-471-79447-9 cloth), not the catalogue's revised 2013 edition; printed page = PDF page $-$ 15. Every practitioner claim was compared with the interview it named; several belong to other interviewees (below).
- **Additions in the earlier notes without a source**: the "structural reasons" for macro (policy jumps, sticky capital, under-arbitraged links), the three policy regimes, QE channels, the regime map's ordering claims, several indicator rules of thumb, LTCM/2015/2020 stress scenarios, BoJ/PBOC/APP/TLTRO/2015 SNB details, Greece 2012 and Argentina 2020, El Niño, Buxl and Schatz bands, and others, each marked in its entry.

### Source findings

- **Global macro** (`def:global-macro-strategy`, `ev:global-macro-crisis-performance`). Rewritten from Gliner chap. 1; the "structural reasons" and "structural inefficiency" kept as unsourced hypotheses; liquidity consequences qualified; Gliner's index figures given with their limits and the crisis mechanisms marked as generalisation; the product-group and view-thesis framing marked as the earlier notes'; the earlier chapter's opening sentence (surviving and profiting from crises) restated as Gliner's capital-preservation aim.
- **Central banks** (`def:central-bank-policy-framework`, `mod:taylor-rule`, `rule:major-central-banks-current`). QE figures **qualified** as announcement-day sums (Bauer via Gliner); "base only via OMO" corrected; regimes and channels marked as synthesis. Taylor's rule checked against Taylor (1993): $r^*$ "2--3\%" corrected to Taylor's 2\%, and Gliner's printed slip recorded. Current facts dated from primary pages: ECB "25 members", "HICP $<2\%$" and "6 meetings" **corrected** (27 members; decisions every six weeks); BoE minutes timing qualified; TARGET2 described correctly; BoJ, PBOC, APP and OMT-use claims left as backlog stubs.
- **Currency regimes** (`def:currency-regimes-intervention`). The impossible trinity from Gliner p. 363 (Mundell, Frankel); the earlier notes' intervention arguments marked as hypotheses.
- **Data and indicators** (`meth:macro-event-queries`, `def:macroeconomic-indicators`, `data:us-macro-release-calendar`). The six-event hit rate given its binomial probability; "central banks target core" and Gliner's "core PCE" **corrected** (the FOMC's goal is headline PCE); the demographic column mix-up resolved; BDI, capacity and payroll-scope claims qualified or stubbed; ECB "6 per year" **corrected**, with agency calendars as the record.
- **Regime and asset map** (`def:macro-regime-asset-map`). Relationships between assets, sector rotation and fixed-income and commodity behaviour across regimes kept as hypotheses with Gliner's chap. 4 and 8 passages.
- **Sizing and risk** (`meth:macro-position-sizing-risk`). Turtle $N$ as a standard deviation **corrected** (it is an average range); perfect correlation is not equal moves (Gliner's slip); the earlier notes' stress additions marked.
- **FX** (`def:fx-market-structure`, `def:us-dollar-dxy-sdr`, `meth:fx-valuation-signals`, `mod:fx-carry-trade`). "5.5 days" corrected and BIS 2025 turnover added; the IMF factsheet for the current SDR basket; Gliner's valuation factors, with the Balassa--Samuelson and Meese--Rogoff descriptions **corrected**; carry skew and crash claims stubbed.
- **Equities and volatility** (`meth:equity-index-valuation`, `def:equity-indices-derivatives`, `def:vix-variance-dividend-swaps`, `meth:equity-macro-leading-indicators`). Tobin's $q$ slip recorded; variance-swap strikes are set ex ante (Gliner's "priced with realized volatility" **corrected**); daily move stated as a standard deviation; the claim that the BDI "cannot be speculated" **contradicted** (unsupported; freight forwards exist).
- **Rates and money markets** (`def:fixed-income-universe`, `def:money-market-reference-rates`, `meth:policy-path-ois-futures`, `def:interest-rate-swaps`, `mod:forward-rates-fra`, `conv:government-bond-futures`, `meth:curve-trades-carry-rolldown`, `def:tips-breakevens`). Gliner's Table 9.5; LIBOR and EONIA ends dated from primary pages; the conditions for OIS-implied probabilities derived (a meeting-dated swap is needed); Eurodollar futures treated as historical, with the conversion dated from the CBOT filing (date discrepancy stubbed); Gliner's FRA fixing-date slip recorded; Treasury futures sit below the bond because of positive carry, not term premium (**corrected**), with ticks recomputed; the steepener's carry sign shown to depend on the curve and repo; "every recession since 1970" **corrected** to Estrella--Trubin's record; Gliner's rolldown misdefinition recorded; the TIPS schedule from TreasuryDirect; "trades at 105" and breakeven-as-expectations **corrected** (a TIPS price is not the adjusted principal; breakevens contain risk and liquidity premia).
- **Credit** (`def:sovereign-credit-defaults`, `mech:cds-contract-credit-events`, `mod:duration-convexity`). Moody's recovery test depends on $n$; Greece 2012 and Argentina 2020 stubbed; CDS payout is par minus recovery, with the equivalence of physical and cash settlement shown, Gliner's upside **corrected** and the post-2009 contract stubbed; the convexity formula's missing price **corrected** (the formula is proportional).
- **Commodities** (`def:contango-backwardation-stocks`, `def:commodity-indices-risk-return`, `def:crude-oil-markets`, `def:natural-gas-market`, `def:metals-markets`, `def:agricultural-markets`). The ending-stocks balance identity extended for trade; DBC's energy weight moved back from the GSCI; kerosene and Saudi Aramco slips recorded and Brent delivery stubbed; the flaring explanation **corrected**; platinum's density ratio is 1.11, and the copper-consumption and Chile copper-share slips recorded; El Niño and the coffee contract marked as the earlier notes' additions.
- **Practitioner frameworks** (`meth:macro-practitioner-frameworks`). Checked interview by interview. **Drobny attributions corrected**: the "75 percent of price movement", long-gamma leverage, forced-seller and "inevitable" points are the anonymous currency specialist's (not Siva-Jothy's); 4:1, cooling-off and three or four trades a year are Andres Drobny's (not Wadhwani's); time-horizon arbitrage is Porter's; front-page contrarianism is Rogers's and Porter's (not Anderson's); Porter's "90 percent explained by the direction of interest rates" restored; the anonymous manager's blocs are Europe, Asia and Latin America. Bessent's 50/30/20 (p. 280), Dimitrijević's internal stops and one-month cool-off (pp. 295--296), Yra Harris's 80 percent, probes, clearing the books and three or four positions (pp. 210, 214--215) and the five-month horizon (p. 334) were all found.

Misstated by Gliner and corrected or recorded in their entries: Balassa--Samuelson, Tobin's $q$, TARGET2, rolldown, the FRA fixing date, kerosene, Saudi Aramco, Chile's copper share and V2X.

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

The 34 new entries and the merged entries are *partly checked*, *draft*; **human review is outstanding**. Quotations: every quotation on added lines (363 distinct) was compared by script with the text layers of Gliner, Drobny, the retrieved pages and the earlier notes; 330 matched, and the 33 misses were inspected by eye: earlier wording containing LaTeX math, quotations broken by a page marker or hyphenation in the text layer, Gliner's misprints quoted with "[sic]", and pre-existing quotations on modified lines. Paraphrases that had been put in quotation marks were rewritten or quoted exactly before the count.

### For review

- Placing the central-bank and data material with the monetary-policy, nowcasting and announcement pathways, and the transmission material with the asset-class pathways.
- Every correction of Gliner listed above, and the reattributions in Drobny (the 2013 edition not inspected).
- Current-status statements dated 16 October 2026 (FOMC, ECB, BoE, BoJ, SNB, LIBOR, EONIA, TIPS schedule, payroll date), against their pages.
- The backlog stubs that stand in for unread primary sources: the Eurodollar conversion date, BoE minutes history, BLS payroll scope, ISDA's 2012 Greece decision, the BIS dollar share, ICE's index methodology and current exchange contract terms.

## macro markets and pricing review follow-up: audit corrections, a source-verification pass over the 37 macro entries and merges, and the 36 macro markets and pricing review backlog items, 16 October 2026

Corrections and source checks after macro markets and pricing review (`f73498d`); the macro markets and pricing review record above is left as written, and this record supersedes it where they differ. This is source verification, not human review or study: every entry stays *draft*, and verification statuses were extended only for the passages actually read.

### Audit findings resolved

1. **Convexity, `mod:duration-convexity`.** Positive convexity improves price relative to the linear approximation; it does not make an unhedged bond gain both ways: the 10-year 4 percent par bond loses 7.722 percent at $+100$~bp and gains 8.530 percent at $-100$~bp (duration alone: $\mp8.111$). The long-volatility analogy is restricted to a duration-hedged position (long the 10-year, short 4.30 times the face of a 2-year: $+0.274$ and $+0.302$ per 100 for $\pm100$~bp, $+0.018$ for $+25$~bp), with its conditions (parallel moves, rebalancing, carry and financing cost). Negative convexity is qualified for callables and MBS (near the money; model-dependent effective convexity). Derivation, not a source check.
2. **Inversion, `meth:curve-trades-carry-rolldown`.** Estrella and Trubin reread (pp.~4--6, table p.~6): on their 1968--2005 sample the monthly-average 10-year minus three-month spread was both necessary and sufficient (every recession preceded by three to twelve negative months within twelve months; no false signals), which reverses the macro markets and pricing review sentence calling it sufficient but not necessary; the entry now separates sample, signal and horizon from a forecasting claim. Extended with Treasury par yields (CMT proxy) and the NBER chronology: inversions before the December 2007 and February 2020 peaks, and November 2022--November 2024 plus five months of 2025 with no peak dated after February 2020 as of 16 October 2026.
3. **VIX, `def:vix-variance-dividend-swaps`.** Cboe's methodology (v6.0, 26 February 2026): $\text{VIX}=100\sigma$ with $\sigma^2$ an annualised 30-day variance computed from option prices, minutes-based annualisation (43,200 and 525,600); VIX~20 means variance 0.04 (0.0033 over 30 days); first value date January 1990, current method from 2003; VIX derivatives settle to a Special Opening Quotation. Gliner's implied-volatility description and a remark on VIX futures corrected.
4. **Gold and silver, `def:metals-markets`.** Gliner p.~320 names China, the United States, Australia and South Africa (``more than 40 percent'') and states that China overtook South Africa; the entry had dropped two countries and called the overtaking unstated. USGS gives 38.9 and 37.8 percent for 2011 and 2012. Table~10.9 (p.~322) is internally inconsistent: Mexico 162.2 plus China 117.0 over the stated 787.0 total is 35.5 percent, the printed shares imply a denominator near 594 and sum to 132.5 percent, and Gliner's 47 and 83 percent follow the printed shares; USGS gives 33.5 percent for 2012. Recorded, not repaired; the World Silver Survey was not read.
5. **Drobny, `meth:macro-practitioner-frameworks` and the reading note.** Andres Drobny (pp.~131--132): re-entry on a single trade with a very tight stop and the incurred loss counted (4:1 becoming 4:3 after two stops), ``On a specific trade, no'' cooling-off; a month away only after a portfolio-wide stop-out and big losses. Siva-Jothy (p.~85): ``50 to 60 percent options'' with no stated denominator (not ``of risk''); three or four opportunities a year and overtrading are his; Andres Drobny only accepts the interviewer's framing (p.~125).
6. **Chapter 8 and 12 locators, `def:macro-regime-asset-map` and `def:macroeconomic-indicators`.** Figure~8.3 (p.~217) compared phase by phase with the sector-rotation table in these notes (partly matching; that table's late-cycle energy-and-materials list contradicts the figure's defensive slowing-growth phase). The U.S.-consumer figure is Gliner's (p.~416); the macro markets and pricing review statement that it was not in the passages read was wrong. Table~12.2 is on pp.~424 (heading) and~425 (data), not pp.~422--423.
7. **Commercial paper, `def:money-market-reference-rates`.** Section 3(a)(3) quoted (``not exceeding nine months'', with the current-transaction condition); SEC interpretations 219.01--219.02; the Richmond Fed's account of the other historical conditions (not ordinarily purchased by the general public, prime quality and Federal Reserve discountability under Release 33-4412, discounting dropped in 1980). Gliner's ``less than 270 days'' kept as attributed.
8. **GSCI history, `def:commodity-indices-risk-return`.** ``Pre-2000 back-filled'' corrected: the index dates from 1991 (Dunsby and Nelson; S\&P pages refused access, and the supplied 11 April 1991 date could not be confirmed, search listings showing April 1991), so 1970--1990 of Gliner's Table~10.1 is back-calculated; spot, excess-return and total-return variants distinguished, without assuming which the 2007 study used.
9. **FX carry and CDS.** `mod:fx-carry-trade` states the quote convention ($S$ domestic per foreign), simple rates, the exact covered-parity and funded-P\&L formulas and their first-order forms (example: $+0.2550$ against $+0.2500$ percent). `mech:cds-contract-credit-events` presents the physical/cash equivalence as an illustration under a common recovery valuation, with a counterexample (62 against 60), and dates the 2009 Big Bang changes and the 2012 Greek determination.

### Verification pass over the 37 entries (34 entries and 3 merges)

Every quotation in the macro markets and pricing review entries was mapped by script to the Gliner PDF page or Drobny printed page where it occurs (`loccheck` against the text layers); locators matched except those corrected above, and two labels (``Short-end TIPS trade like food and energy'' and ``TIPS are typically issued on a quarterly basis'', pp.~247--248, are Gliner's, not only the earlier notes') were fixed. Spot rereads: Gliner pp.~52, 55, 57 (sizing, risk/reward, gap risk), 36--38 (Barclays Prime Services), 222--227, 246--248, 302, 314, 317, 320--325, 356, 373 (Table~11.4 against Bauer's Table~1, which matches exactly), 416, 424--425.

| Entry | Follow-up result |
|---|---|
| `def:global-macro-strategy`, `ev:global-macro-crisis-performance` | Locators and quotations re-matched; no change |
| `meth:macro-position-sizing-risk` | pp.~52--57 reread; no change |
| `meth:macro-practitioner-frameworks` | Corrected (*Drobny*) |
| `def:macro-regime-asset-map` | Corrected (*Chapter 8 and 12 locators*) |
| `def:macroeconomic-indicators` | Corrected (*Chapter 8 and 12 locators*); CES scope from BLS (nonprofits in scope; the other exclusions in the earlier notes right); release timing |
| `meth:equity-macro-leading-indicators`, `meth:macro-event-queries`, `meth:equity-index-valuation` | Re-matched; no change |
| `data:us-macro-release-calendar` | BEA, Census and G.17 calendars read; cadence confirmed; CPI and ISM unchecked |
| `def:central-bank-policy-framework` | Bauer's letter read; event-study caveats quoted |
| `mod:taylor-rule` | No change |
| `rule:major-central-banks-current` | BoE minutes history, FOMC practice, BoJ 2024 exit, SNB 2015, ECB APP and OMT status dated; TARGET2/T2S |
| `meth:policy-path-ois-futures` | Eurodollar conversion narrowed (CME notice not readable; 14 April 2023 better supported than the filing's 23 April) |
| `meth:curve-trades-carry-rolldown` | Corrected (*Inversion*) |
| `def:tips-breakevens` | Gliner's 2014 calendar compared with today's; attribution of two sentences fixed |
| `def:interest-rate-swaps` | BIS: interest rate derivatives the largest OTC component ($579 trillion, end-June 2024) |
| `def:fixed-income-universe` | SIFMA 2025 totals; the earlier notes' product-group ranking shown to be ill-posed |
| `def:money-market-reference-rates` | Corrected (*Commercial paper*); Treasury bill schedule |
| `def:sovereign-credit-defaults` | ISDA Greece determination and auction dated |
| `mech:cds-contract-credit-events` | Corrected (*FX carry and CDS*) |
| `conv:government-bond-futures` | Eurex terms read (the earlier notes' Schatz and Buxl bands current); CME unread |
| `def:us-dollar-dxy-sdr` | ICE formula and history; BIS 2025 shares (dollar 89.2 percent) |
| `def:currency-regimes-intervention`, `meth:fx-valuation-signals` | Re-matched; no change |
| `mod:fx-carry-trade` | Corrected (*FX carry and CDS*); BNP abstract |
| `def:equity-indices-derivatives` | Re-matched; no change |
| `def:vix-variance-dividend-swaps` | Corrected (*VIX*) |
| `def:contango-backwardation-stocks` | Re-matched; no change |
| `def:commodity-indices-risk-return` | Corrected (*GSCI history*) |
| `def:crude-oil-markets` | ICE Brent terms (EFP delivery, cash-settlement option) |
| `def:metals-markets` | Corrected (*Gold and silver*); USGS 2025 production shares |
| `def:agricultural-markets` | ICE coffee and cotton terms |
| `def:natural-gas-market` | Re-matched; no change |
| Merges: `mod:duration-convexity` (*Convexity*), `mod:forward-rates-fra` (re-matched, no change), `def:fx-market-structure` (re-matched, no change) | |

### The 36 backlog items

Resolved (9): `data:bls-ces-scope`, `rule:boe-minutes-publication-history`, `data:fomc-communication-current`, `ev:isda-greece-2012-determination`, `data:bis-2025-currency-shares`, `conv:dxy-methodology`, `conv:cboe-vix-methodology`, `data:fixed-income-market-size`, `data:treasury-bill-offering-schedule`. Narrowed to a named document, dataset or empirical test (27): `data:eurodollar-sofr-conversion-date` (CME advisories 23-082 and 23-121), `ev:qe-announcement-effects` (Gagnon et al.), `rule:central-bank-policy-history` (OMT activation, TLTRO, PBOC), `ev:curve-inversion-after-2005` (H.15 series), `rule:tips-auction-schedule-history` (refunding announcements), `data:irs-notional-share` (BIS swaps line), `ev:sovereign-restructurings-after-2006`, `conv:cds-standard-contract` (fixed coupons, 2014 Definitions), `data:de-facto-regime-classification`, `ev:carry-crash-skewness` (paper bodies), `data:equity-index-lists-current`, `conv:commodity-index-methodologies`, `conv:brent-wti-contract-terms` (NYMEX WTI), `data:opec-membership-current`, `data:metals-market-shares-current` (consumption shares, COMEX/LME), `conv:cbot-ice-ag-contract-terms` (CBOT grains), `conv:henry-hub-contract-terms`, `conv:treasury-bund-futures-current-specs` (CME), `data:us-release-schedules-2026` (BLS CPI, ISM), `data:demographic-projections-current`, `data:post-libor-funding-stress-measures`, and six empirical items that no reading can close (`ev:global-macro-returns-after-2013`, `ev:practitioner-rules-tested`, `ev:regime-asset-responses-tested`, `ev:equity-index-value-signal`, `ev:fx-valuation-factors-oos`, `ev:backwardation-scarcity-or-premium`). Each stub's text in its pathway note names what is missing; each affected note records the follow-up under *Source verification after macro markets and pricing review*.

### Sources, 2026-10-16

Read directly: Estrella and Trubin (New York Fed PDF); Cboe's VIX methodology (catalogue key `gap-cboe-vix6`); Bauer (FRBSF Economic Letter 2012-16, with Table~1 as an image); the Warsh review and the Bank of England's 2015 documentation page; the FOMC calendars; the Bank of Japan statement of 19 March 2024; the SNB release of 15 January 2015 (title and date); the ECB's APP page and TPI release; NBER's chronology and dating pages; Treasury's daily par-yield files 2006--2026 (monthly averages in `ust-10y3m-monthly.csv`); TreasuryDirect's bills and TIPS pages; the BIS 2025 FX results; ICE's Dollar Index FAQ, Brent, coffee and cotton specifications; Eurex's fixed-income factsheet and contract specifications of 10 September 2025; ISDA's Big Bang page and Greece releases; USGS Mineral Commodity Summaries 2013 (gold, silver) and 2025 (gold, silver, copper); the Richmond Fed's commercial-paper chapter; Dunsby and Nelson (2010); BEA's schedule, the Census calendar, the Fed's G.17 dates; SIFMA's Fact Book highlights; the NBER abstract of Brunnermeier, Nagel and Pedersen. Read through a web-fetching tool's extracts (direct requests refused): the BLS CES concepts page and FAQ, the SEC's Securities Act interpretations, 15 U.S.C. 77c, the BIS OTC release for end-June 2024. Seen only in search listings: CME Clearing Advisory 23-082's title and summary, S\&P's GSCI launch information, the Greek auction final price. Refused or unusable: CME (terms-of-use block, not circumvented), S\&P Dow Jones Indices and Bloomberg methodologies (403), OPEC (challenge), EIA (script-only pages), ISM, BLS schedule pages, the IJCB PDF. Gliner and Drobny reread at the pages listed above. 32 source keys added (`sifma-factbook-2026` among them) and `bis-triennial-2025` updated in `compendium/front/sources.tex`.

### Checks

`notes/artefacts/multi-asset-systematic-macro/convexity-curve-signals-checks.py` (exit 0 with `/opt/homebrew/bin/python3.10`; reads `ust-10y3m-monthly.csv` in the same folder), seven sections: convexity unhedged and duration-hedged; inversion runs against NBER peaks; VIX units; gold and silver shares and Table~10.9's denominators; exact and first-order FX carry; CDS settlement with different recovery valuations; Andres Drobny's 4:1 after two stops. The market design and liquidity / dealer models and information / macro markets and pricing reviews scripts were rerun unchanged (exit 0). Quotations added in this follow-up were compared by script with the source text layers; the misses are source titles, passages read only through fetching-tool extracts (BLS, SEC, statute, BIS), text of Gliner and the earlier notes broken by page markers, LaTeX or ``[sic]'', and the search-listing title of CME's notice, all inspected.

### For review

- The corrections listed above, especially the reversal on necessity and sufficiency, the reading of Table~10.9 and the restricted long-volatility analogy.
- Facts taken from fetching-tool extracts or search listings (BLS, SEC, BIS OTC, CME notice title, GSCI launch).
- The post-2005 inversion check, which uses Treasury's 3-month CMT rather than Estrella and Trubin's bill series.

## macro markets and pricing review second follow-up: five audit corrections (inversion signals, FX accrual bases, CDS coverage, convexity carry, the GSCI launch), primary sources for the 21 source-based macro markets and pricing review stubs, and four dealer models and information review source gaps, 16 October 2026

Corrections and source checks after the first macro markets and pricing review follow-up (`b11076f`); earlier records are left as written, and this record supersedes them where they differ. This is source verification, not human review or study: every entry stays *draft*, mastery and consolidation dates are untouched, and verification statuses were extended only for the passages read. The quotation-matching pass over all 37 macro markets and pricing review entries was not repeated; new quotations were checked by script against the text of the sources read (below).

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

`notes/artefacts/multi-asset-systematic-macro/carry-market-statistics-checks.py` (exit 0 with `/opt/homebrew/bin/python3.10`), six sections: FX carry with unequal bases; zero carry of the hedged convexity position; BIS swap shares from `bis-otc-ird-instruments.csv`; UN WPP peak years from `wpp2024-working-prime-age.csv`; the two OFI conventions on one bid move; Foucault, Kadan and Kandel's Proposition~4 against Lehalle and Laruelle's (A.4). `convexity-curve-signals-checks.py` section~2 rewritten for the signal rules (exit 0); `ust_monthly.py` and `h15_monthly.py` rebuild their monthly files byte for byte. The market design and liquidity / dealer models and information / macro markets and pricing reviews scripts rerun unchanged (exit 0). `tools/check_compendium.py --check`: 0 problems; `python3 -B -m unittest discover -s tools`: 14 tests OK. Quotations on added lines (145 distinct) were compared by script with the text of the sources read, including raw copies of the Treasury, PBOC, ECB, Moscow Exchange, World Gold Council, Silver Institute and CFTC pages: 121 matched; the 24 others are earlier wording quoted as such, wording from the audit request, source titles and file names, the OFR table entry split across lines, the workbook's cover date (read in the file), the first follow-up's BIS phrase (fetching tool only) and the Argentina quote (confirmed separately; the script's dollar-sign parsing failed).

### For review

- The inversion rules (month against episode, onset window $t+1$ to $t+12$, provisional outcomes) and the six 1968--2005 month misses.
- The fee-mapping between Foucault, Kadan and Kandel and Lehalle and Laruelle, and the Cont--Cucuringu--Zhang order-flow convention.
- Facts read only through the fetching tool (BLS CPI dates) or from browser-printed copies (CME, S\&P).
- The decision-time handling of TAQ correction records stated in `data:market-data-levels`.

## dealer models and information review follow-up (second): four source gaps worked in the second macro markets and pricing review follow-up, 16 October 2026

Worked because CME, OPEC and other sources for the macro markets and pricing review stubs refused access. Resolved: `mod:fkk-make-take-original` (Foucault, Kadan and Kandel's September 2009 working paper, pp.~20 and 23--25 read as page images: the platform maximises $(c_m+c_t)\mathcal R$ for a fixed total fee, and Proposition~4 is Lehalle and Laruelle's (A.4) under $s\Delta=\Delta/2$, $\Gamma=L$, $r=\gamma/\beta$; ``efficient'' therefore means trade-maximising for a given total fee, and the paper's welfare, $\mathcal R L-MC_m-NC_t$, is a different objective; entry `mod:make-take-fee-speed-race`) and `def:multi-level-ofi` (Cont, Cucuringu and Zhang, arXiv v4: definitions, sample, windows, in- and out-of-sample results, and the negative one-minute forecasting $R^2$; their per-level flow uses the new size when a price moves away, checked on the page image; entry `def:order-flow-imbalance`). Narrowed: `ev:flash-crash-studies` (Kirilenko, Kyle, Samadi and Tuzun read in the accepted manuscript: account classification, HFT volume shares and unchanged HFT inventory behaviour; Menkveld and Yueshen not obtained; entry `ev:may-2010-flash-crash`) and `data:trade-correction-records` (NYSE Daily TAQ specification v4.0: correction indicator codes 00--12 and late-report sale conditions; Holden and Jacobsen not read; entry `data:market-data-levels`). Sources: `fkk-2009`, `wide-cont-cross-impact-ofi` (arXiv), `w5-kirilenko-flash-crash` (Cambridge repository), `nyse-daily-taq-spec`. Checks: second follow-up script, sections~5 and~6.

## Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections, 16 October 2026

Corrections and source checks after the second macro markets and pricing review follow-up (`14c92bc`); earlier records are left as written, and this record supersedes them where they differ, in particular the second follow-up's statement that the CBOT filing's ``April 23'' is the date of a CME press release (*macro markets and pricing review second follow-up*, *The 21 source-based macro markets and pricing review stubs*), which was wrong. This is source verification, not human review or study: every entry stays *draft*, mastery and consolidation dates are untouched, the guide pin (343d145) is unchanged, and verification statuses were extended only for the passages read.

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

New `notes/artefacts/execution-market-making/market-estimators-rules-checks.py` (numpy; exit 0 with `/opt/homebrew/bin/python3.10`), seven sections: refresh time and Hayashi--Yoshida against previous-tick sampling (refresh-time realised covariance 0.39 against 0.60, 0.60 with one lead and lag, Hayashi--Yoshida 0.59, previous tick at 1/5000 0.02); batch-auction $\delta/\tau$ and $\epsilon/(2\tau)$; convergence-rate arithmetic; Model~I invariant law and estimator; LR, EMO and CLNV on trades inside the spread and interpolated times; the RTS~11 and RTS~1 tables; platinum shares. The hand example in section~1 was corrected while writing (refresh times 2, 4, 7, 9). Existing scripts unchanged and passing: market design and liquidity review, dealer models and information review, macro markets and pricing review, the two macro markets and pricing review follow-ups. No yield data or aggregation code changed; `h15_monthly.py` and `ust_monthly.py` rebuild their CSVs byte-identically. Quotations on new lines: 197 distinct, 171 matched by script; two non-verbatim quotes found by the script were corrected; the 26 unmatched are titles, LaTeX-escaped strings, wording of the earlier notes and the checkpoint's own phrase.

### For review

- The universe-selection and validation-design cautions stated for Cont--Cucuringu--Zhang and Briola et al.
- The refresh-time simulation result and its reading against Barndorff-Nielsen et al.'s kernel.
- The OPEC membership conflict, the NYSE rule compilation's date, and the CFTC-filed contract texts used in place of CME's rulebook.
- The EU transposition statement, which covers Ireland and Malta only.

## Second source follow-up of the order books and order flow / macro markets and pricing reviews queue, 16 October 2026

Works the 24 items left unresolved and not deferred by the previous record (*Source follow-up of order books and order flow / dealer models and information reviews and macro markets and pricing review audit corrections*, commit `9cc18eb`): its 19 narrowed and 5 blocked items, from local copies obtained for this pass (author and institutional copies, official chapter PDFs downloaded through a browser, and browser exports of web rulebooks and calendars). It also rechecks one resolved item (`conv:cbot-ice-ag-contract-terms`) against the current chapters. The two deferred items (`ev:curve-inversion-after-2005`, `data:post-libor-funding-stress-measures`) and the six macro empirical-test stubs stay open. This is source verification, not study or human review: every entry stays *draft*, mastery and consolidation dates are untouched, the guide pin (343d145) is unchanged, and verification statuses were extended only for the passages read.

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

### For review

- The OPEC membership conflict and the Statute's next-calendar-year rule.
- The TU tick discrepancy and the undated CME chapters.
- The ISM Good Friday inference.
- The three Argentine counts.
- The reading of Kolm et al.'s Fig.~8 values from the plot.
- The page images used for Lee--Ready, Harris, Hayashi--Yoshida, Reinhart and ICSG.

## source verification (2026-10-17): four audit corrections, the 15 active leftovers of the order books and order flow / macro markets and pricing reviews queue, 19 older backlog items and the six macro empirical stubs

Starting state checked: `main` at `9e403e3`, equal to `origin/main`, clean; guide pin `343d145` (unchanged); 211 entries, all draft. This record covers 40 distinct items in three groups, kept apart in the counts below, plus the two deferred items. It is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them.

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

### Outcomes

- Original 35-item queue: before this batch 18 resolved, 14 narrowed, 1 blocked, 2 deferred. Of the 15 active leftovers: 2 resolved, 7 narrowed further, 5 reviewed and unchanged, 1 still blocked. Queue now 20 resolved, 12 narrowed, 1 blocked, 2 deferred.
- Older backlog (19 items, separate): 17 resolved, 2 narrowed.
- Macro empirical stubs (6, separate): 3 empirically tested within stated bounds (one row, one factor, two contracts; the untested remainder stays in each backlog), 3 open with executable protocols and named missing data.
- All 40: 19 resolved, 9 narrowed or advanced, 5 reviewed without change, 1 blocked, 3 empirically tested, 3 protocol only.
- Entries 211 $\to$ 221 (new: `meth:purged-embargoed-cross-validation`, `meth:sharpe-ratio-standard-error`, `meth:deflated-sharpe-ratio`, `meth:forecast-scaling-ic`, `data:holdings-insider-filing-lags`, `mod:margin-liquidity-spiral`, `rule:mifid-rts6-algorithmic-controls`, `mech:order-state-reconciliation`, `ev:quant-implementation-failures`, `rule:spoofing-securities-markets`); all draft.

### Sources

Listed with URL, retrieval date, version, acquisition route and SHA-256 in `reading_materials/sources_source-verification_2026-10-17.json` (96 files; ignored; none committed). Routes: direct downloads of author, institutional and official copies; the eCFR versioner API; GovInfo; CELLAR content negotiation and SPARQL; the FIX Trading Community's GitHub repository at a pinned commit; Internet Archive captures for the two SEC orders; public data from EIA, FRED, the Philadelphia Fed and Ken French's library. Local library copies outside the repository: AFML (Wiley 2018), Grinold and Kahn (2nd ed.), Narang (3rd ed.), Velu et al. Nineteen keys were added to `compendium/front/sources.tex`. Refused or unavailable, not bypassed: sec.gov (403), finra.org (404 then 429), S\&P DJI (403), stoxx.com (TLS certificate unverifiable), Euronext (403), IDX (403), LME notices, ISDA's 2014 Definitions (sold), journal paywalls (JFQA, JFE, \emph{Financial Management}, JPM), LOBSTER samples (request and terms), macro hedge-fund indices (registration). The Lo (2002) copy is hosted by a Berkeley student organisation; its provenance is not established, though it carries the journal pagination.

### Checks

New, all exit 0 with `/opt/homebrew/bin/python3.10`: `market-making-lob/model-checks.py` (Avellaneda--Stoikov infinite horizon by quadrature, eqs.~(18)--(19), Grossman--Miller free entry); `statistical-learning-foundations/cv-checks.py`; `backtest-inference/sharpe-checks.py`; `equity-long-short-construction/forecast-checks.py`; `point-in-time-data/filing-checks.py`; `funding-crowding/spiral-checks.py` (an illustration); `model-governance-controls/reconciliation-check.py` (an offline illustration); `execution-market-making/cme-allocation-checks.py`; `execution-market-making/commodity-production-latency-checks.py`. Extended: `contract-specifications-statistics-checks.py` (Ultra Bond spread tick). The seven existing scripts (market design and liquidity review, dealer models and information review, macro markets and pricing review, the two macro markets and pricing review follow-ups and the two source follow-ups) rerun and pass. Empirical scripts (`backwardation_test.py`, `fx_ppp_oos_test.py`, `regime_recession_test.py`) reproduce their printed results and rebuild their derived panels byte for byte (SHA-256 6953ecd1\dots, da1bb9d4\dots, 82ce2b97\dots). `h15_monthly.py` and `ust_monthly.py` were not rerun: neither their code nor their inputs changed. The first drafts of three checks were corrected before use: a vacuous variance check and a first-order test that did not shrink $\gamma^2\sigma^2/\omega$ (model checks), and a mislabelled message in the CV check. `tools/check_compendium.py --check`: 0 problems; `python3 -B -m unittest discover -s tools`: 14 tests OK.

### For review

- The Avellaneda--Stoikov ask and the AFML p.~106 condition, both read as misprints from the surrounding text and own algebra.
- The non-monotone response of Grossman and Miller's market-maker count to risk aversion (own algebra against the paper's ``of course'').
- The Kolm et al.\ Table~3 ambiguity, recorded rather than resolved.
- The three empirical tests' design choices (expiry mapping of EIA's continuous contracts, monthly-average FX rates and revised CPI, the Sahm-type rule on quarterly vintages) and the exploratory WTI sign effect.
- Sources read in non-publisher hosts: Lo (student-organisation host), the SEC orders (Internet Archive), Brunnermeier and Pedersen (Advance Access PDF).

## method validation (2026-10-17): eight audit repairs (three empirical tests rerun) and a source-review coverage

Starting state checked: `main` at `820517a`, equal to `origin/main`, clean; guide pin `343d145` (unchanged); 221 entries, all draft. This is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them. No protocol here is preregistered: protocols written in docstrings and committed together with results are labelled as such, and v2 corrections were chosen after v1's results had been seen.

### Audit repairs

1. **Energy test** (`notes/artefacts/commodity-storage-curves/`; `def:contango-backwardation-stocks`). v1 (script, results, panel) moved unchanged to `superseded-first-run/`; v2 replaces it.
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
2. **FX test** (`notes/artefacts/fx-determination-forecasting/`; `meth:fx-valuation-signals`). v1 kept in `superseded-first-run/`.
   - *Eligibility.* Predictor eligibility now uses only price levels known at $t$. Outcomes use spot rates alone, so future CPI is no longer needed: JPY's 12-month forecasts gain the last 12 months.
   - *Stale-data rule.* Monthly CPI must be exactly two months old. Quarterly CPI is accepted 4 to 6 months after its quarter ends. v1 carried 2025Q1 AUD and NZD CPI to September 2026; v2 stops them at September 2025.
   - *Reporting.* Ages and effective endpoints are reported: JPY ends August 2021, monthly-CPI currencies May--June 2025, AUD and NZD September 2025. Expanding-training cutoffs are unchanged and checked against an independent OLS fit.
   - *Results* (v1 in brackets): pooled 12-month OOS $R^2$ $-14.9\%$, Clark--West $t=-0.3$ ($-15.3\%$, $-0.4$); 1-month $-2.0\%$ ($-2.0\%$). Portfolio unchanged in substance: spot $+0.09\%$ a year, with interest differentials $-0.17\%$. It is now labelled a statistical return on monthly averages with interbank-rate carry, not an executable result. Neither pass rule is met.
   - Focused checks: `fx-checks.py`.
3. **Regime test** (`notes/artefacts/macro-regimes-stock-bond/`; `def:macro-regime-asset-map`). v1 kept in `superseded-first-run/`.
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
5. `data:trade-correction-records`, narrowed further (v4.0 PDF retrieved 2026-10-17; the printed entry `nyse-daily-taq-spec` absorbed the duplicate key `nyse-dtaq-spec-v4` on 2026-10-18 without the retrieval date): NYSE Daily TAQ Client Specification v4.0, sec. 3, codes 00--12. The 01 records carry the original time and the corrected data; the 12 records carry the correction time and the original data. The time on 10 and 11 records is not stated.
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
16. `ev:backwardation-scarcity-or-premium`: repaired and retested (the *Energy test* repair). Untested remainder: other commodities and hedging-pressure readings.
17. `ev:fx-valuation-factors-oos`: repaired and retested (the *FX test* repair). Gliner's other factors untested.
18. `ev:regime-asset-responses-tested`: repaired and retested (the *Regime test* repair). Other rows of the map untested.
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

### Outcomes

- All 50: 10 resolved (4 as new entries); 23 narrowed (3 of them with new entries); 4 unchanged; 7 blocked; 3 repaired and retested; 1 newly tested within bounds; 2 open with protocols.
- New entries: 7. Entries 221 $\to$ 228: `meth:multiple-testing-control`, `meth:bitemporal-reference-tables`, `meth:time-valid-ml-experiment-record`, `meth:gips-composite-presentation`, `mod:black-litterman`, `meth:portfolio-covariance-estimation`, `meth:var-es-estimation-methods`. All entries draft.

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

### For review

- The energy test's expiry inference for Henry Hub before 1997, the inventory availability convention, and the executable variant's settlement-fill assumption.
- The FX stale-data limits (2 months; 4--6 months).
- The regime sensitivities: the all-months window and Newey--West with 4 lags.
- The global macro test's data choices, and that only 2022--2026 was available.
- Lo's eq. (5) reading; the Avellaneda--Stoikov ask after the 2025 preprint.
- Sources read from course pages, author hosts and OCR.

## empirical extensions (2026-10-17): six audit repairs and a source-review coverage

Starting state checked: `main` at `12e634a`, equal to `origin/main`; guide pin `343d145` (unchanged); 228 entries, all draft. This is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them. Protocols for the empirical extensions were written before the results were computed and are committed with them, so none is a preregistration.

### Audit repairs

1. **Filing availability** (`data:holdings-insider-filing-lags`; `filing-timestamp-checks.py`, corrected in place). method validation (2026-10-17)'s fallback, the start of the next business day, was not conservative: EDGAR's *Determine the Status of My Filing* page (dated 4 June 2024, reviewed 31 October 2024; Internet Archive capture of 5 October 2026, sec.gov refusing automated retrieval) gives after-cutoff submissions a 6:00 a.m. filing date on the next business day and dissemination only "the next business day", with no time. Availability is now the recorded dissemination time, else the first-observed time, else unknown (the record does not enter the panel). A separate lower bound (acceptance, or 6:00 a.m. on the next business day after holidays for after-cutoff forms outside the same-day list) only detects look-ahead. The check adds a holiday case, a Form 4 before 10 p.m., a Schedule 13D/A and a first observation earlier than the bound, flagged as a data error.
2. **FIX Done for Day** (`mech:order-state-reconciliation`; `reconciliation-check.py`, corrected in place). OrdStatus 3 was treated as terminal. FIX 4.4's state matrices (OnixS reprint of Appendix D, scenarios A.1.b and H.1.a) show a GTC order continuing after Done for Day and being restated the next day (ExecRestatementReason 1, GT renewal). Terminal states are now Filled, Canceled, Rejected and Expired; Done for Day ends the lifetime only for a Day order where the venue's rule says so (a named configuration flag). New cases: a GTC order with Done for Day and zero leaves (not released), and a Day order.
3. **Expected shortfall** (`meth:var-es-estimation-methods`, Notation; new `es-discrete-check.py`). ES is now defined as the quantile integral $\mathrm{ES}_p=\frac1p\int_0^p\mathrm{VaR}_u\,du$ (Acerbi and Tasche, 2001), which differs from the tail conditional expectation when the distribution has an atom at the quantile. Example: a loss of 100 with probability 0.005 at $p=1\%$ gives VaR $=0$ and ES $=50$.
4. **Sharpe asymptotics** (`meth:sharpe-ratio-standard-error`; new `sharpe-zero-check.py`). A finite fourth moment is sufficient, not necessary: at $SR=0$ the Slutsky argument needs only finite variance. Student-$t_3$ returns at $SR=0$ give a scaled variance of 0.990 (Monte Carlo) and a tail rejection rate of 0.0483 at 5 percent; a non-normal three-point law with skewness 0 and kurtosis 3 gives $T\operatorname{Var}=1.113$ against the normal-moment $1+SR^2/2=1.125$, so normal moments, not normality, are what the simple formula needs. "Only then" was qualified accordingly.
5. **GIPS benchmark exception** (`meth:gips-composite-presentation`). Provision 4.A.1(e) lets a composite present no benchmark when no appropriate one exists, with the reason disclosed under 4.C.31 (PDF pp. 39 and 47, printed pp. 21 and 29); the parallel provisions for pooled funds and asset owners (5.C.30, 6.A.1(e), 6.C.26, 7.C.26, 8.D.4, 8.F.4, 8.H.1) are listed.
6. **Global macro from 2014** (`ev:global-macro-returns-after-2013`). The BarclayHedge workbook was obtained through the site's public Excel download form (an HTTP POST; SHA-256 `ead890c4…`, matching the audit). The registered window, January 2014 to July 2026 (151 months), gives 53 down months for the benchmark, a mean index return in them of $-0.5217$ percent ($t=-2.9952$, the audit's values), correlation $+0.42$ (CI 0.17 to 0.62). Crisis protection is not supported, more firmly than in 2022--2026, which is kept. The statements that the window needed registration are corrected. Revision check: 0 of the 55 overlapping months differ from the earlier page; the index's weighting and backfill rules are not public. Script `global_macro_down_months_2014_test.py`; v1 (`global_macro_down_months_test.py`) unchanged and reproduced.

### Statements superseded

- The next-business-day availability fallback (method validation (2026-10-17), *Filing timestamps* repair) is superseded by the *Filing availability* repair.
- "Done for Day is terminal" in method validation (2026-10-17)'s reconciliation check is superseded by the *FIX Done for Day* repair.
- method validation (2026-10-17)'s ES notation (tail expectation without the atom correction) is superseded by the *Expected shortfall* repair.
- "Only then" for the fourth-moment condition (method validation (2026-10-17), *Sharpe inference* repair) is qualified by the *Sharpe asymptotics* repair.
- "The window from 2014 needs the history behind registration" (method validation (2026-10-17), `ev:global-macro-returns-after-2013`) is superseded: the workbook is public through a form.
- In `def:crypto-venue-instrument-structure`, "fewer venues and strikes … not checked" is replaced by the one-venue snapshot (`def:crypto-options-venue-structure`). In the Hawkes entry, "the same stability condition holds" is qualified to $\int|h|<1$ (`res:nonlinear-hawkes-stability`). In `def:block-trade`, "exchange cross rules … remain open" is replaced by NYSE Rule 127 (`rule:block-print-trade-through-current`).

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
### Outcomes

- All 60: 15 resolved (9 as new entries); 35 narrowed (2 of them with new entries: `def:amm-pool-mechanics`, `meth:resampled-efficiency`); 3 unchanged; 1 blocked; 4 tested within stated bounds (three extensions and the global-macro window); 2 deferral-trigger reviews, both retained.
- New entries: 11. Entries 228 $\to$ 239: `mod:black-scholes-merton`, `def:implied-volatility-surface`, `meth:equal-risk-contribution`, `mod:garch-volatility-forecast`, `meth:resampled-efficiency`, `mod:multi-curve-fra-swap-valuation`, `meth:strategy-promotion-criteria`, `meth:discretionary-override-governance`, `ev:crypto-dated-futures-carry`, `def:amm-pool-mechanics`, `ev:empty-voting-equity-derivatives`. All entries draft.

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

### For review

- The filing-availability convention (dissemination or first observation, else unknown) and its lower bound.
- The venue-rule flag for Done for Day on Day orders.
- The heating-oil expiry assumption (rule text not obtained; supported by the roll check in 6 of 7 blocks) and the two inflation-row protocol deviations.
- The Gatheral--Jacquier density factor recorded as a source discrepancy (p. 5).
- Abstract-only evidence (`ev:dark-pool-price-discovery`, `ev:delisting-survivorship-rewriting`, `meth:overlap-crowding-measure`, `ev:why-firms-hedge` and `ev:signal-decay-crowding`) and archived copies used in place of refused publisher pages.
- The NYSE rulebook read is a 2019 compilation.

## derivatives and empirical validation (2026-10-17): seven audit repairs, backlog reconciliation and a source-review coverage

Starting state checked: `main` at `012aa19`, equal to `origin/main`; working tree clean; guide pin `343d145` (unchanged); 239 entries, all draft. This is source verification and bounded empirical testing, not study or human review: every entry stays *draft*, no mastery or consolidation date is set, and verification statuses were extended only for the passages read. Earlier records are left as written; where they differ, this record supersedes them. Protocols for new empirical tests were written to files before their results were computed and are committed with the results, so none is a preregistration.

### Audit repairs

1. **Quarterly CPI vintages** (`ev:regime-asset-responses-tested`; new `inflation_quarterly_test.py`). empirical extensions (2026-10-17)'s protocol deviation was wrong: it had requested `pcpiqvmd.xlsx`, a name formed from the monthly file's root, and concluded that no quarterly file exists. The quarterly file is `cpiQvMd.xlsx` (vintages CPIyyQq), linked from the Philadelphia Fed's CPI page (dated 2 October 2026). The collection documentation says quarterly vintages hold what was available on the 15th of the quarter's middle month and exclude later releases, while monthly vintages are taken just after the BLS report, which can fall either side of the 15th. The correction was appended to `inflation-row-protocol.md` before the quarterly results were computed; the protocol is otherwise unchanged. Results: 128 usable vintages (1994Q3--2026Q2), 34 signal quarters in 13 episodes; 10-year yield $+0.07$ (Welch $t=0.83$), slope $-0.17$ ($t=-1.56$), WTI $-2.2$ percent ($t=-0.60$): no response supported. Diagnostic: on 111 common vintage months with responses (112 classifiable), the latest CPI month differs in 55, always later in the monthly vintage, and 11 signal labels change. These match the audit's counts, recomputed independently. The monthly run (`inflation_regime_test.py` and outputs) is unchanged and relabelled a timing sensitivity; it still reproduces byte for byte.
2. **FX forecast inference** (`ev:fx-valuation-factors-oos`; `fx_ppp_oos_test.py` and `fx_carry_test.py` corrected in place, pre-correction versions kept in `superseded-row-lag-inference/`). The carry test stacked 7--9 currencies per month and used $h-1$ row lags; the PPP test stacked currencies one after another and ignored their contemporaneous dependence. Both now use `panel_nw_t`: Clark--West scores keep their forecast-origin month, are summed across currencies within it (each currency-month still weighted $1/N$, so pooled $R^2$ and forecasts are unchanged), and Newey--West runs over $h-1$ calendar months, with $h$ months as a sensitivity. Carry: $h=12$ Clark--West $t=-1.97$ (sensitivity $-1.94$; was $-4.44$, the audit's $-1.973$), $h=1$ $-0.41$ (was $-0.85$). PPP: $h=12$ $-0.18$ (was $-0.31$), $h=1$ $-1.30$ (was $-2.14$). All verdicts unchanged. The carry portfolio (one return a month, $+2.07$ percent a year, $t=2.04$) was unaffected and is described as a statistical return on monthly-average prices, distinct from an executable return. New focused check `fx-panel-inference-check.py` fails if currency rows are treated as months (identical currencies must give the single-series $t$; row order must not matter).
3. **Heating-oil return definition** (`ev:backwardation-scarcity-or-premium`; `heating_oil_test.py` corrected in place, the simple-return run kept in `superseded-simple-return-run/` with the unchanged `backwardation_test.py` it imports). The protocol's log held-contract return now replaces the builder's simple return for heating oil only: premium slope 0.3276, $t=1.55$ (was 0.3582, 1.67); OOS $R^2=-0.95$ percent, Clark--West $t=0.31$ (was $-0.92$, 0.37); premium not supported; scarcity unaffected. EIA's own definitions (Futures Prices (NYMEX), ``Contract~1'') document the delivery-month mapping. Month-ends are the last date on which EIA reports both contracts: 79 of 361 precede the last date in the month on which EIA reports either contract (12 by more than five days, at most 21), now reported and written to the panel; the roll check on that calendar is consistent with the mapping and does not prove the expiry date. An exploratory regression on the 243 pairs whose dates are both the month's last observed date (chosen after the results) gives slope 0.07, $t=0.20$. The WTI and gas protocols were not changed.
4. **FRA settlement convention** (`mod:multi-curve-fra-swap-valuation`; new `fra-settlement-check.py`). $N\tau(F_j-K)P_{\mathrm{OIS}}(T_2)$ is now labelled the end-settled swaplet value, exact when $F_j$ is the $T_2$-forward expectation of the fixing. The conventional FRA pays $N\tau(L-K)/(1+\tau L)$ at $T_1$ (Hull, sec.~4.9, p.~111, n.~4); with deterministic $L=F_j$ its value is $N\tau(F_j-K)P_{\mathrm{OIS}}(T_1)/(1+\tau F_j)$. Invented curves: $-\$20{,}777.37$ start-settled against $-\$20{,}792.96$ end-settled. The check shows the two coincide on one curve (bond replication) and diverge on two, and that with a stochastic $L$ the substitution omits a concavity term (by quadrature, $-\$21{,}044.50$ at 20 percent volatility); the stochastic conditions are stated rather than a general pricing theorem.
5. **ERC conditions** (`meth:equal-risk-contribution`; new `erc-sharpe-check.py`). The source's first-order condition holds for any common Sharpe ratio $s$; ERC maximises the Sharpe ratio over long-only, fully invested weights only if $s>0$ (with constant correlation $\rho\in(-1/(n-1),1)$); for $s<0$ it minimises it. Counterexample: two uncorrelated unit-volatility assets with excess return $-1$: ERC $-\sqrt2$, either asset $-1$. The source's wording and the corrected condition are distinguished.
6. **Crypto liquidation units** (`ev:crypto-dated-futures-carry`). BIS WP 1087, revision of October 2025, PDF pp.~7, 25 and~44 (Table~7 as a page image): coefficient 2.22 (s.e.\ 0.79) on the standardised one-month basis for next-month sell liquidations scaled by open interest, intercept 10.84 (OKEx, 1,619 observations), i.e.\ about 2.2 percentage points of open interest per standard deviation of carry. ``22 percent of open interest'' is withdrawn; the prose's two wordings and its ``10\%'' are reported, not resolved; the measure includes voluntary and forced closures.
7. **Market-manipulation intent** (`rule:spoofing-securities-markets`). MAR's Article 12(1)(a) is effect-based with a legitimate-reasons defence, (b) turns on deception or contrivance, and (c)--(d) on ``knew, or ought to have known''; ESMA/2015/224 (feedback on Q1, para.~12; sec.~2.2.2, para.~8) says conduct without intent can fall within MAR; Directive 2014/57/EU makes the criminal offence require intent (Art.~5(1); recital~23); Rule 10b-5 requires scienter (\emph{Aaron}, \emph{Hochfelder}); Section~9(a)(2) has a purpose element; FINRA Rule 5210.03 has no express intent element and is described as one regime among others, not the exception. FINRA's findings are kept.

### Backlog reconciliation

All 57 active backlog lines that carried stacked status prefixes were rewritten to state only the remaining gap (the dated paragraphs above each backlog keep the history). In particular: `ev:global-macro-returns-after-2013` is complete within its stated scope, and the registration blocker is gone; `ev:curve-inversion-after-2005` now says all 27 inverted months have complete twelve-month horizons and only retrospective NBER dating remains, with a revisit trigger of an NBER peak announcement or April 2027 (when the last month passes the longest past announcement lag); claims that read material was unread were removed, including two stale entry passages (`mod:mean-variance-portfolio-optimisation` on Michaud and shrinkage, and the further reading of `mod:harris-discretised-spread` on Dayri and Rosenbaum). Correction within this batch: the first reconciled line for `meth:multiple-testing-control` repeated a stale claim that Romano and Wolf's working paper was unread; it had been read in method validation (2026-10-17), and the line now names only the published versions. Later, 19 lines were updated again to reflect new outcomes.

### Statements superseded

- empirical extensions (2026-10-17)'s protocol deviation ``The Philadelphia Fed does not publish a quarterly-vintage CPI file'' and the record's ``the Philadelphia Fed's quarterly-vintage file (does not exist; monthly vintages used)'' (empirical extensions (2026-10-17), *Sources*) are superseded by the *Quarterly CPI vintages* repair.
- empirical extensions (2026-10-17)'s carry Clark--West $t=-4.44$ and $-0.85$, and method validation (2026-10-17)'s PPP $t=-0.31$ and $-2.14$, are superseded by the *FX forecast inference* repair.
- empirical extensions (2026-10-17)'s heating-oil premium figures (slope $+0.36$, $t=1.67$; OOS $-0.92$ percent, Clark--West 0.37) are superseded by the *Heating-oil return definition* repair, as is ``the expiry assumption (rule text not obtained; supported by the roll check)'' in its *For review*, which now rests on EIA's definition, with the roll check described as consistent only.
- ``A 10 percent rise in standardised carry predicts short liquidations of 22 percent of open interest'' (empirical extensions (2026-10-17), the `ev:crypto-dated-futures-carry` question) is withdrawn (the *Crypto liquidation units* repair).
- ``Spoofing: FINRA's Rule 5210.03 has no intent element, unlike the MAR and Rule 10b-5 framing the entry used'' (empirical extensions (2026-10-17), *Conclusions that changed*) and the entry's ``Under MAR and Rule 10b-5, legality turns on intent'' are superseded by the *Market-manipulation intent* repair.
- ``The registered window'' and ``run as registered'' (empirical extensions (2026-10-17), the *Global macro from 2014* repair and the `ev:global-macro-returns-after-2013` question, and the pathway note's dated paragraph) should read ``the protocol's window'' and ``run under the protocol recorded in method validation (2026-10-17)''; no preregistration occurred. The pathway note carries an explicit correction.

### The 70-target work list

Constructed after the reconciliation from the remaining backlog gaps and the pinned guide's required readings and checkpoints, and fixed in a working file before any of it was processed. Two changes were made while processing and are recorded here: the `meth:multiple-testing-control` question was re-aimed (its original question, Romano and Wolf's working paper, had already been read) to the entry's stated remaining gap, Hansen's SPA test; and new questions whose answers were merged into an existing entry received their own question identifiers (for example `res:cfmm-reported-price`), with the entry named under *Recorded in*. 24 targets follow up existing gaps and 46 are new bounded questions; 48 targets carry identifiers outside empirical extensions (2026-10-17)'s 60. No audit repair is counted among the 70.

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

### Outcomes

- **Audit repairs:** seven, all made; three empirical outputs regenerated (inflation row on quarterly vintages, FX inference for two scripts, heating-oil premium), with the earlier runs kept and reproducible; no verdict of an empirical test changed.
- **The 70 targets:** 41 resolved, 21 narrowed, 5 tested within stated bounds, 2 blocked, 1 unchanged, none deferred. Follow-ups (24): 5 resolved, 13 narrowed, 4 tested, 1 blocked, 1 unchanged. New questions (46): 36 resolved, 8 narrowed, 1 tested, 1 blocked. Six targets answered from abstracts only (37, 54, 55, 57, 59, 64) are counted as narrowed, not resolved.
- **New entries: 15** (239 $\to$ 254), all draft: `ev:correlation-matrix-noise`, `meth:volatility-forecast-loss`, `meth:structural-break-tests`, `ev:volatility-managed-portfolios`, `mod:heston-stochastic-volatility`, `mod:merton-jump-diffusion`, `mod:sabr-smile`, `data:gsw-treasury-curve`, `ev:money-fund-runs`, `ev:cip-deviations`, `mech:defi-lending-liquidation`, `ev:stablecoin-runs`, `rule:stablecoin-standards`, `mech:crypto-auto-deleveraging`, `mod:liquidity-spirals`. Eight pathway notes were opened for their owning pathways (`high-dimensional-estimation`, `time-series-volatility`, `risk-parity-vol-targeting`, `option-pricing-models`, `fx-cip-dollar-funding`, `defi-lending-liquidations`, `stablecoin-pegs-runs`, `crypto-leverage-liquidations`); entries of the guide sections `common-toolkit` and `onchain-protocols`, which have no chapter folder, sit in the nearest existing chapter, as each note says.

### Conclusions that changed

- Inflation-shock row: the headline now rests on the quarterly vintages the protocol named; no response is supported either way.
- FX forecasts: the evidence against the carry and PPP forecasts is weaker than reported (carry $h=12$ Clark--West $t=-1.97$, not $-4.44$); both still lose to the random walk out of sample.
- Heating oil: the premium slope is smaller with log returns (0.33, $t=1.55$); still not supported.
- FRA valuation: start- and end-settled values differ on two curves; the deterministic substitution is a convention-specific approximation.
- ERC: maximum Sharpe ratio only with a positive common Sharpe ratio.
- Crypto carry and liquidations: a standard deviation of carry goes with about 2.2 percentage points of open interest more sell liquidations, not 22 percent of open interest.
- Manipulation intent: MAR's administrative regime does not generally require intent; criminal liability and Rule 10b-5 do.
- New empirical results (`ev:backwardation-scarcity-or-premium`, `meth:time-varying-hedge-ratio` and `ev:regime-asset-responses-tested`): WTI hedging pressure does not predict returns; rolling hedge ratios beat a static ratio modestly out of sample for jet fuel; the deflation row is not supported in real time.
- Sources: U.S.\ commercial paper averages about 30 days (BIS), against Gliner's ``most between 90 and 270 days''; Laloux et al.'s $\sigma^2=1-\lambda_{\max}/N$ must mean $\lambda_1$; GJR's working paper puts the indicator on positive shocks; Anadu et al.\ estimate a USD~1 break-the-buck threshold, not the guide note's USD~0.99; Avellaneda and Lee chose their s-score cutoffs inside their backtest period; Boyd et al.'s multi-period gain comes mostly from an extra, unrealistic forecast.

### Sources

Listed with URL, retrieval date, acquisition route, size and SHA-256 in `reading_materials/sources_derivatives-validation_2026-10-17.json` (93 files kept; 11 wrong or failed responses kept only as evidence; 21 failed or refused requests; reused earlier files and the local Hull copy listed; ignored, none committed). 19 source keys were added to `compendium/front/sources.tex` (317 in all). Internet Archive captures were used where a publisher refused automated retrieval or served a web page in place of a PDF: BIS (CPMI--IOSCO d206, WP 1270, BCBS--IOSCO d499), the FCA (PS24/14), Project Euclid (Shreve and Soner), MIT DSpace (Merton's working paper, HTTP 429), BME (IBEX notice), nyse.com (the MWCB report, 404 directly), Hansen's former Brown page, an LBS faculty page (DeMiguel, Garlappi and Uppal) and the Internet Archive's own scan of Bai and Perron's 1995 working paper. CELLAR content negotiation needed the XHTML representation for Directive 2014/57/EU. Refused or unavailable, not bypassed: the Library of Congress's U.S. Reports PDFs (403; Cornell LII used), Harvard DASH (CAPTCHA; NBER copy used), SSRN (Hull and White, 403), Oxford ORA (Patton, 403; the UTS working paper used), a former NYU Stern page for Merton (404), Leland (no open copy), Buti, Rindi and Werner's published paper (no open copy), and a Nasdaq filing (TLS certificate mismatch). A first BIS request returned a different article; the CP primer was then read from its own page.

### Checks

New, all exit 0: `fx-determination-forecasting/fx-panel-inference-check.py`, `rates-credit-mortgages/fra-settlement-check.py`, `portfolio-construction/erc-sharpe-check.py`, `high-dimensional-estimation/covariance-volatility-checks.py`, `option-pricing-models/option-model-checks.py`, `risk-parity-vol-targeting/risk-parity-checks.py`. All 50 check scripts in `notes/artefacts/` (outside the preserved-run folders) were rerun and pass. `tools/check_compendium.py --check`: 0 problems. `python3 -B -m unittest discover -s tools`: 14 tests OK.

Empirical scripts rerun from retained inputs and compared byte for byte with their saved outputs, all identical: `inflation_quarterly_test.py`, `inflation_regime_test.py` (sensitivity), `deflation_row_test.py`, `fx_ppp_oos_test.py`, `fx_carry_test.py`, `heating_oil_test.py`, `backwardation_test.py`, `hedging_pressure_test.py`, `jet_fuel_hedge_test.py`, `gsw-kw-acm.py`, `okx-options-snapshot.py`, `regime_recession_test.py`, both global-macro scripts, `acm-term-premium-summary.py` and `deribit-options-snapshot.py`; committed panels other than the heating-oil panel (regenerated with the log return and the date gap) are unchanged. The preserved pre-correction FX scripts and the simple-return heating-oil script reproduce their committed outputs when run from copies of their folders.

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

## Drobny source check: Bessent's passages and the 2013 revised edition, 18 October 2026

Source checking, not study, for `meth:macro-practitioner-frameworks`; it supersedes the earlier records' statements that the 2013 edition was not inspected, for the passages listed here only. The entry stays *draft*.

### Sources, 2026-10-18

- `s7-drobny`, Wiley 2006 printing: a PDF with a text layer in the checkout's git-ignored directory, `reading materials/Inside the House of Money - Top Hedge Fund Traders on -- by Steven Drobny -- John Wiley & Sons, Inc_ (trade), Hoboken, N_J_, 2006 -- J_ Wiley; J_ -- 9780470038895 -- 18771978aedb018223b91eccc76023e5 -- Anna’s Archive.pdf` (SHA-256 1f2e415bc8042cc4b16bcecd1f3783907ca1998d85d1db787aefcde12cafafeb, 15,629,936 bytes); copyright page "Copyright © 2006", ISBN-13 978-0-471-79447-9 (cloth); printed page = PDF page − 15, checked at pp. 273–286. The file's name carries ISBN 978-0-470-03889-5, which the copyright page does not give.
- The revised edition the catalogue names: an EPUB in the same ignored directory, `reading materials/Inside the House of Money -- Steven Drobny -- 2013 -- John Wiley & Sons -- c20b3ebc6c4460fe8132cb5dce907668 -- Anna’s Archive.epub` (SHA-256 a6a8bab9640c1cfad997b6796143e8a548f8f657609b4ab8a85be869e064a7a6, 4,456,198 bytes; Bessent is `OEBPS/xhtml/Chapter12.html`); metadata publication date 2013-11-16 and identifier ISBN 978-1-118-86572-9; copyright page "Copyright © 2006, 2009, 2014". No printed page numbers; cited by chapter title and the interviewer's question.

### Findings

- **Bessent, bottom-up research** (2006 chap. 13, p. 274; 2013 chap. 12, "The Stock Operator", answer to "So you were running the Soros London office when the pound fell out of the ERM. Can you talk a bit about what happened on that famous trade?"): Soros Fund Management "did a lot of bottom-up research"; "Stan and George believed that if you can find out what's going on at a micro level, you can figure out the big picture". The belief is attributed to Druckenmiller and Soros.
- **Entry discipline** (2006 p. 285; 2013, answer to "When you initiate a trade, do you have profit targets and stop-loss levels?"): "I don't usually have stop-losses. One of the things that I learned from Stan Druckenmiller is how to enter a trade"; he tries to make his entry point "good enough that I rarely stop myself out of a trade". Self-reported practice and a lesson attributed to Druckenmiller, with no results; the entry does not present it as advice to trade without stops and records the conflict with other interviewees' stop rules.
- **Paradigm shifts** (2006 p. 285; 2013, answer to "Do interest rates matter once again for currencies? …"): "Soros used to say, 'Don't try to play the game better, try to figure out when the game has changed'"; "Catching a paradigm shift is where you make a lot of money because everyone is still focusing on what mattered". The advice is Soros's as Bessent reports it; the profit remark is Bessent's opinion.
- These replace the treatment in commit `2606a23`, which listed the three points as not checked against the interview and not adopted.
- **Edition comparison.** The quotation-marked strings in the entry were searched by script in both texts (normalised for ligatures, line-break hyphens and quotation marks), and keyword anchors for the unquoted paraphrases of Wadhwani (positioning; the 24-hour break), Rogers (the Fortune cover; the front page) and the anonymous currency specialist (credit curve, three blocs, negative gamma, long or flat, gestalt, five-month horizon) were located in both; the paraphrases' wording was not compared. Andres Drobny's interview (2006 pp. 109, 125, 130–132; chap. 6 "The Researcher") is not in the 2013 edition, whose chapters from Porter on are numbered one lower. (The first version of this record said that every quotation recurred unchanged; see the closeout correction below.) One question differs: 2006 "What is your favorite trade at the moment?", 2013 "What is your best trade at the moment?".

### Checks and their limits

| Source | Passages compared | Limits |
|---|---|---|
| `s7-drobny`, 2006 printing | pp. 273–286 read; the entry's quotations searched throughout | Text layer; opinions of selected survivors |
| `s7-drobny`, 2013 EPUB | Chapter 12 (Bessent) read around the three passages; the entry's quotations and anchors searched in all chapters | The rest of the text, the new prefaces and the second Leitner interview ("The Family Office Manager, Part Two") not compared; Thiel and Gorton–Standing not used in either edition |

Files changed: `compendium/multi-asset-systematic-macro/global-macro.tex` (Bessent's Statement item, Notation, Conditions; the earlier "not adopted" sentence removed), `notes/readings/s7-drobny.md`, `notes/entry-evidence.json`, the `multi-asset-systematic-macro` pathway note and the reading row in `notes/log.md`. Human review is outstanding.

### Closeout correction, 18 October 2026

- **Quotation handling.** The Practice field quoted three summaries as if verbatim ("75\% of price moves", "3--4 major opportunities annually", "overtrading as damaging as running losers"); the 2006 text reads "75 percent of price movement happens only 10 to 15 percent of the time" (p. 332), "three or four major macro opportunities each year" and "Overtrading is as bad as running losing positions for too long" (p. 85). The three are now unquoted paraphrases. The entry's remaining quotation marks enclose 38 verbatim phrases, one with a marked omission ("money … craves stability", p. 207), six short source terms ("doubly right", "incredibly dangerous", "matrix", "prayer trade", "frozen ice", "inevitable") and one chapter title; all 45 non-title strings occur at their cited 2006 pages. In the 2013 EPUB, 36 occur in the same interviewee's chapter and Andres Drobny's nine do not. Bessent's own statements, the belief he attributes to Druckenmiller and Soros, and the saying he attributes to Soros are kept apart in the entry.
- **Edition claims.** The first version of this record said every quotation recurred unchanged in the 2013 edition; the entry, the reading note, the entry evidence and the edition-comparison item above now state the counts and say that unquoted paraphrases were checked by keyword only.
- **Locations.** Both books are in the checkout's git-ignored `reading materials/` directory, not outside the repository as first recorded; their file names and SHA-256 hashes are given above and in the reading note.

## Coverage inventory and pilot integrations, 18 October 2026

Batches 0 and 1: an inventory of the supplied topic outlines mapped to neutral objectives, and two source-to-entry pilots. Source checking and editorial mapping, not study; no mastery is implied. Both pilot entries stay *draft*.

### Outline inventory

- **Relocation.** The eight outline PDFs in the ignored `reading_materials/curriculum_cfa/` were hashed (SHA-256, all equal to the initial audit values), copied to `reading_materials/outlines/outline-<first 12 hex digits>.pdf`, each copy re-hashed and matched before its original was deleted, and the emptied folder removed. No twelve-digit prefixes collide. Original names are kept only as provenance in `notes/coverage/outline-manifest.json`; no maintained file referred to the old folder.
- **Extraction.** Text from every page with PyPDF2; modules parsed as the heading before each "able to" marker and items as checkbox lines. Split headings (the Standard VII title runs over two lines) and wrapped items were reconciled against the raw extracted page text. Counts: Level I 102 modules / 340 items; Level II 51 / 382; each 2027 Level III file 28 / 183 core plus 8 / 64, 7 / 34 and 7 / 27 pathway items; 2026 files 22 / 171 core plus the same pathway counts. The three core copies are identical within each year. Total in scope: 203 modules / 1,030 items, core counted once with all three occurrences kept.
- **Mapping.** Each item was read and paraphrased in our own words with its command verbs; items were grouped into 424 objectives in 107 topics owned by guide or local chapters. 1,019 items map to one objective and 11 to two. Distinct standards and levels stay distinct items; identical wording across the seven standards maps to the same per-standard objectives at every level. Candidate existing entries were attached to 66 objectives by subject search; none was assessed, so those objectives stay `missing` with next action `review`.
- **Edition comparison.** The 2026-to-2027 Level III differences are the ethics guidance split (six modules, twelve items added per file) and one semicolon in Private Debt; see `notes/coverage/source-changes.md`.

### Sources, 2026-10-18

| Source key | Identity and copy | Read | Use |
| --- | --- | --- | --- |
| `wide-gips-2020` | GIPS for Firms 2020, local PDF `reading_materials/method-validation/src/GIPS_2020_firms.pdf`, SHA-256 9c45d87d…d5532 | Glossary (external cash flow, money- and time-weighted return), provisions 1.A.35-1.A.36, 2.A.12, 2.A.23-2.A.24, 2.A.29, 5.A.1 | `def:return-measures` reuse |
| `alpha-harris` | Harris, *Trading and Exchanges*, Oxford 2003 printing outside the repository, SHA-256 3707e56a…caad6a; the 2002 copy used earlier is AES-encrypted and PyPDF2 lacked the cipher, so Ghostscript text of the 2003 printing was used | chap. 22, sec. 22.2.1, pp. 446-447 | independent source for IRR against holding-period return |
| `eu-2023-1803-ias7` | Regulation (EU) 2023/1803, original OJ XHTML via CELLAR content negotiation (CELEX 32023R1803), SHA-256 7dfd2c91…af3941 | IAS 7 in full | `meth:statement-linked-cash-flows` |
| `eu-2026-338-ifrs18` | Regulation (EU) 2026/338, OJ XHTML via CELLAR (CELEX 32026R0338), SHA-256 231323db…afd8e | Articles 1-3, IFRS 18 para. C1, all amendments to IAS 7 | effective date, operating-profit starting point, interest and dividend classification |
| `principles-financial-accounting-2019` | OpenStax, *Principles of Accounting*, vol. 1 (2019), web pages | secs. 16.3, 16.4, 16.6 | further reading; confirms the indirect-method steps |

Searches (standard web search): "IAS 7 Statement of Cash Flows full text Commission Regulation (EU) 2023/1803 indirect method"; "OpenStax Principles of Accounting Volume 1 statement of cash flows indirect method"; "time-weighted versus dollar-weighted rate of return Dietz pension fund performance measurement". A search summary named Regulation (EU) 2026/338 among the later amendments of IAS 7, which led to the IFRS 18 text. Not used: the EUR-Lex HTML endpoint returned an empty body to a script (CELLAR used instead); a Society of Actuaries 1973 discussion paper on time- and dollar-weighted returns returned the site's "File Not Found" page; Dietz (1966) has no open copy. The EU, GIPS and SOA downloads are kept in the ignored `reading_materials/coverage-pilots/` and `reading_materials/method-validation/`.

### Findings

- **Return pilot (reuse).** `def:return-measures` already calculates both returns on one cash-flow history, compares them on matching horizons, explains why the money-weighted return is lower and states when GIPS permits money-weighted returns (1.A.35: control of external cash flows and a closed-end, fixed-life, fixed-commitment or significantly illiquid vehicle). Harris (pp. 446-447) independently gives the IRR as the rate replicating the capital flows, the holding-period return as one unit invested at the start with distributions reinvested, and their difference when flows are not pro rata. All quoted provisions and pages matched. Every figure in the entry recomputed: money-weighted −3.7126 percent per sub-period and −7.2874 percent over two; time-weighted −1.0 percent cumulative and −0.5013 percent per sub-period; 3.95 and 1.2997 percent; 7.4202 percent annualised; real 4.8544 percent; leveraged 13 percent. Nothing was missing for `objective:compare-time-and-money-weighted-returns`, so the entry text is unchanged and the objective is recorded as covered.
- **Financial-statement pilot (new).** `meth:statement-linked-cash-flows`, in the new local chapter `financial-statement-analysis`. IAS 7 as adopted in 2023 starts the indirect method from profit (para. 18(b)) and lets non-financial entities choose the section for interest and dividends (paras. 33-34). The IFRS 18 amendments, applicable to annual periods beginning on or after 1 January 2027 and adopted for the EU by Regulation 2026/338, start from operating profit or loss and fix dividends paid as financing and, for most entities, interest paid as financing and interest and dividends received as investing (paras. 33A, 34A-34D). The entry states both regimes with dates. Its synthetic example is reconciled three ways (indirect from operating profit, indirect from profit with interest in operating, direct) and the balance sheet balances at 1,005.
- **Outcomes.** Covered: `objective:compare-time-and-money-weighted-returns`, `objective:link-cash-flow-statement`. Partial: `objective:convert-indirect-to-direct-cash-flow` (prepaid and accrued items not converted; next action `extend`) and `objective:compare-cash-flow-reporting-frameworks` (source gap: FASB ASC 230 not obtained or read; next action `obtain-source`). Outline items covered: `outline:7099c7688942:m003:b01` and `:m030:b01`; partial: `:m030:b02`-`:b04`. An objective supported only by non-provider sources (IAS 7, IFRS 18) is now covered, and one with two outline items exists.

### Checks and their limits

| Check | Result |
| --- | --- |
| `notes/artefacts/financial-statement-analysis/cash-flow-linkage-check.py` | All checks pass |
| `python3 tools/check_compendium.py --check` | 0 problems; 255 entries; 64 pathway notes |
| `python3 tools/check_coverage.py --check --verify-outlines` | 0 problems; eight outline hashes match |
| `python3 -m unittest discover -s tools` | 26 tests pass (9 existing, 5 local-section, 12 coverage) |

The mapping of 1,025 unreviewed items is an editorial grouping, not a coverage claim. The paraphrases were written from extracted text; the split ethics headings were checked against the raw page text, and no outline page images were inspected in this pass. Human review of both entries and of the objective grouping is outstanding.

## Cash-flow slice and validator corrections, 18 October 2026

This correction slice covers one section declaration, three coverage-validator corrections and the two partial cash-flow objectives. Source checking and tooling, not study. It supersedes the statements of the record above that the IFRS against US GAAP comparison is unsourced and that the indirect-to-direct conversion lacks prepaid and accrued items.

### Section declaration

`notes/local-sections.json` and its loader, constants, tests and documentation were removed. Both checkers now read the ordered `\qfsections` list in `compendium/compendium.tex` (42 unique keys) as the only section declaration; the guide supplies specialist pathway keys for notes only. Missing, repeated or malformed declarations and keys, collisions with specialist pathway keys, undeclared content folders, wrapper inputs naming no file, and typed entries not reachable from the master through a wrapper's `\input` chain are reported. Declared sections without content need no chapter. All 255 entries are reachable.

### Validator corrections

| Audit finding | Correction | Replayed on the real data |
| --- | --- | --- |
| Unreviewed mappings became covered | An outline item is covered only with a review date, covered objectives and no residual gap; otherwise partial | Clearing the review date of `outline:7099c7688942:m003:b01` now reports it partial |
| Mapped labels and evidence could disagree | Mapped and candidate labels must be typed entries; entry-evidence references must equal the mapped entries, each with a nonempty record naming the entry's file; every listed source must be cited by a mapped entry, with sources read only for review under `review_sources` | Remapping `objective:link-cash-flow-statement` to `def:return-measures` gives four problems |
| Dropped items went unnoticed | Item and module occurrences per active outline, shared-core copies included, must equal the manifest's counts; occurrences must match their module's | Dropping `outline:7099c7688942:m001:b01` and lowering the counters reports 339 against the manifest's 340 |

The new rule moved `alpha-harris` in `objective:compare-time-and-money-weighted-returns` from `sources` to `review_sources`: Harris was read to confirm `def:return-measures`, which does not cite it.

### Sources, 2026-10-18

| Source key | Identity and copy | Read |
| --- | --- | --- |
| `us-cash-flow-classification-amendment-2016` | FASB ASU 2016-15, PDF from storage.fasb.org, SHA-256 6508b9ee…47ed4fd | Effective dates (p. 5); amended ASC 230-10-45-15, -16, -17, -25 (pp. 9-10, 14-15); illustration 230-10-55-10 |
| `cash-flow-statement-roadmap-2026` | Deloitte DART, Roadmap sec. 3.1, web page | Quotations of ASC 230-10-45-28 to 45-30 only |
| `cash-flow-standard-setting-2026` | FASB staff slides AP35 (June 2026) and AP20A (October 2025), PDFs from ifrs.org | In full |
| `eu-2023-1803-ias7`, `eu-2026-338-ifrs18` | As in the record above | IAS 7 paras. 18(b), 19(b), 20, 31-35 and the IFRS 18 amendments reread |
| `principles-financial-accounting-2019` | As above | Sec. 16.6, prepaid insurance and salaries payable |

Not accessible: the FASB Accounting Standards Codification (login) and DART's Codification view (subscription). Not used: exam-preparation and practice summaries found by search.

### Findings

- **Conversion** (`objective:convert-indirect-to-direct-cash-flow`, now covered). Each income-statement line becomes a cash line by removing the change in its related operating balances (IAS 7 paras. 18(b), 19(b); OpenStax sec. 16.6). The example adds prepaid insurance (10 to 16; expense 30, paid 36) and wages payable (12 to 20; expense 150, paid 142). Operating cash flow becomes 197 by both methods, closing cash 97, and the balance sheet balances at 1,023; checked by hand and by `cash-flow-linkage-check.py`.
- **Framework comparison** (`objective:compare-cash-flow-reporting-frameworks`, now covered). US GAAP starts from net income, classifies interest and dividends received, interest paid and taxes as operating and dividends paid as financing, and requires a reconciliation of net income even under the direct method. IFRS before IFRS 18 allows choices for interest and dividends; IFRS 18 (periods from 1 January 2027) starts from operating profit and fixes interest paid as financing and interest and dividends received as investing for most entities. FASB staff papers of 2025 and 2026 report interest classification only as research feedback. On the example, US GAAP gives operating cash flow 177 against 197 under IFRS 18; interest paid is the whole difference.
- **Outline items** `outline:7099c7688942:m030:b02` to `:b04` reviewed; no residual gap remains. Level I: five items covered.

### Checks and their limits

The current Codification text was not read; the US GAAP paragraphs rest on the 2016 Update's reprint and a 2026 secondary quotation, and later amendments other than the pending finance-lease item were not traced. Human review of the entry is outstanding.

## Return measurement and present value: first foundation slice, 18 October 2026

This slice covers the cash-tax correction, the checker docstring warning, and `topic:return-measurement` and `topic:time-value-of-money` only. Source checking and writing, not study.

### Cash-tax correction

The cash-flow entry's line-by-line rule subtracted total deferred-tax balance changes from tax expense. Deferred-tax balances also move through OCI and equity: tax follows the item recognised outside profit or loss (IAS 12 paras. 58, 61A), and a revaluation of property, plant and equipment is such an item (para. 62(a)). The rule now rolls forward the net current tax balance (para. 12): tax paid = current tax recognised in profit or loss, OCI or equity minus the change in current tax payable net of receivable, the current component being disclosed (paras. 79-80, 81(a)-(ab)). The conversion identities state their assumptions (no business combinations, translation, non-cash settlements or OCI/equity movements in the converted balances). Counterexample, checked against an independent ledger of payments: current tax 30 in profit or loss, payable unchanged at 5, a revaluation adding a deferred tax liability of 10 through OCI; tax paid 30, the superseded formula 20. Two more cases (deferred tax wholly in profit or loss; current tax charged in OCI) agree with their ledgers. The distributor example and its figures are unchanged. The US GAAP comparison keeps its 2016-reprint and 2026-quotation vintage and now says so in the entry's Conditions. `tools/check_compendium.py`'s module docstring is raw, removing the `\q` escape warning.

### Sources, 2026-10-18

| Source key | Identity and copy | Read |
| --- | --- | --- |
| `eu-2023-1803-ias12` | IAS 12 in Regulation (EU) 2023/1803, same OJ XHTML as `eu-2023-1803-ias7` | paras. 5, 12, 57-65, 79-81(ab) |
| `principles-of-finance-2026` | Dahlquist and Knight, *Principles of Finance* 2e, OpenStax web edition of 24 June 2026 | secs. 3.4, 7.4, 10.2, 11.2, 15.1 |
| `inflation-compensation-decomposition-2019` | Kim, Walsh and Wei, FEDS Notes, 21 May 2019, HTML, SHA-256 b6ac47d0…f444c | introduction, model and premia discussion, eqs. (1)-(4) |
| `s7-hulloptions` | Hull, 11th Global edition, second local copy outside the repository, SHA-256 36748bb6…45ba8e | sec. 4.8, pp. 109-110; sec. 11.4, pp. 255-256; sec. 13.1, pp. 288-290 |
| `ft-wilshire-5000-2026` | FT Wilshire 5000 methodology, January 2026, local PDF, SHA-256 d1da43d4…f19edff | sec. 1.1, p. 3 (price and total-return indexes) |
| `wide-gips-2020` | as before | glossary definitions reused, not reread |

Searches: OpenStax dividend discount models; OpenStax holding-period and average returns; OpenStax interest rates, real rates and risk premia; the D'Amico, Kim and Wei TIPS decomposition. Not used: S&P Dow Jones Indices' index-mathematics methodology (the script request returned a web page, as in earlier reviews); the 2008 FEDS working paper (downloaded, superseded by the note); exam-preparation summaries.

### Existing entries inspected first

`def:return-measures` and `meth:relative-performance-evaluation` (returns), `def:interest-rate-measures` (compounding, present value, annuities, zero, par and bond yields), `mod:forward-rates-fra` (continuous forward rates and their lock-in), `res:cost-of-carry-forward-price` (forward prices and currency parity, continuous compounding), `def:derivative-contracts` and `res:synthetic-short-put-call` (payoffs and parity with dividends). Gaps found: holding-period, price and total returns; arithmetic against geometric means; equity and preferred present values; implied required return and growth; required-return components; an explicit statement of cash-flow additivity with discrete-compounding applications. `def:return-measures` was extended in place; the other gaps were written as three entries in a new `common-toolkit` chapter (`def:required-return-components`, `meth:instrument-present-value`, `res:cash-flow-additivity`), which link to the existing entries rather than repeating them.

### Findings and checks

- Exact against approximate: the Fisher relation $1+i=(1+R)(1+h)$ is exact, its additive form an approximation with error $Rh$, and the geometric mean $\approx$ arithmetic $-\sigma^2/2$ an approximation (4.25 against 4.2808 percent in the example); additive premia are a convention.
- All examples are original and checked in `notes/artefacts/time-value-returns/time-value-return-checks.py` by an independent route: cash-flow summation for every closed form, bisection for yields and implied growth, ledgers of the replicating trades for the forward rate (928.1225 refinanced to 1,000) and the forward exchange rate (1.116098 USD per EUR), state-by-state replication and risk-neutral expectation for the option (call 5.9524, put 3.5714 by replication and by parity). My own first expected values for five results were wrong and were corrected from the computation and a hand check before the entries were written.
- Objectives now covered: `interpret-return-concepts`, `decompose-required-return`, `calculate-return-types`, `calculate-equity-returns`, `value-instruments-by-present-value`, `solve-implied-return-and-growth`, `apply-cash-flow-additivity`; `compare-time-and-money-weighted-returns` stays covered, its text unchanged. Each of the seven outline items `outline:7099c7688942:m001:b01`, `:m001:b02`, `:m002:b01`, `:m004:b01` to `:b03` and `:m042:b03` was read against its objective and reviewed individually; no other mapping was promoted.

### Limits

The textbook was read as web renderings with partly garbled equations, cited by section. The premia in the required-return example are illustrative; the Federal Reserve decomposition is a model estimate. After-tax returns, pricing between coupon dates, and option pricing beyond one period are outside this slice. Human review is outstanding.

## Time-value corrections and statistics slice, 18 October 2026

This slice covers three corrections to the time-value entries, then `topic:descriptive-statistics` and `topic:probability-distributions` only. Source checking and writing, not study.

### Corrections

| Finding | Correction | Source | Check |
| --- | --- | --- | --- |
| Refinancing at the implied forward treated as assured | `res:cash-flow-additivity` shows the trades' dated cash flows: buy the two-year zero for 928.1225 and borrow it for a year, giving 0, $-955.9662$, $+1{,}000$, a forward loan at 4.6062 percent; the reverse locks in forward borrowing; rolling into a new loan at a later rate is a bet (1,032.4434 at 8 percent) | Hull sec. 4.8, p. 110 and Business Snapshot 4.1, p. 111, reread | the cash flows themselves, no future rate assumed |
| Fisher identity called exact under expected inflation | `def:required-return-components`: identity exact for realised inflation or a specified scenario; ex ante $i-E\pi$ and ex post $i-\pi$; the expected real return under uncertain inflation exceeds deflation by mean inflation (0.8333 against 0 percent for 10 percent nominal and inflation 0 or 20 percent) | Mankiw, *Macroeconomics* 10th ed., chap. 5, sec. 5-3 (user-supplied copy); the Jensen argument is derived | both figures computed |
| Halving an annual yield without naming its quotation | `meth:instrument-present-value`: halving applies to a nominal annual yield compounded semiannually; an effective annual yield uses $(1+y)^{1/2}-1$ | OpenStax sec. 10.2's convention, kept | 100.2218584 at 10 percent effective and at 9.7618 percent nominal; 100.00 if wrongly halved |

Earlier example values are unchanged; the Fisher example is now labelled as assuming known inflation. A 1981 St. Louis Fed *Review* article was sought for the ex ante distinction; its URL redirected to an index page and the download failed, so it was not used.

### Sources, 2026-10-18

| Source key | Identity | Read |
| --- | --- | --- |
| `statistical-methods-handbook` | NIST/SEMATECH e-Handbook, web | 1.3.5.1, 1.3.5.6, 1.3.5.11, 7.2.6.2; 1.3.6.6.1, .2, .4, .9, .18 |
| `coefficient-of-variation-reference-2017` | NIST Dataplot reference page, 24 January 2017 | whole page |
| `probability-statistics-random-processes` | Pishro-Nik, probabilitycourse.com | 1.4.3, 5.1.5, 5.3.1, 8.2.2 |
| `downside-risk-volatility-2026` | Estrada, *Finance Research Open* 2 (2026) 100099, author PDF, SHA-256 052c0108…1bfb1cd | pp. 1-2, eqs. (1)-(3) |
| `macroeconomics-2019` | Mankiw, 10th ed., user-supplied PDF, SHA-256 249ad416…b7276d6f | chap. 5, sec. 5-3 |
| `s7-hulloptions` | as before | sec. 15.1, pp. 339-340 |

Not used: Blitzstein and Hwang's free edition (non-downloadable viewer); exam-preparation summaries of semi-deviation; the Cleveland Fed inflation-expectations page (no ex ante definition).

### Existing entries inspected first

`meth:portfolio-covariance-estimation`, `ev:correlation-matrix-noise`, `meth:var-es-estimation-methods`, `mod:mean-variance-portfolio-optimisation` and `ev:high-frequency-stylised-facts`. They own large-matrix estimation, random-matrix noise, VaR methods, optimisation and empirical tails; none gave the foundational definitions, so seven entries were written in two new files of `common-toolkit` (`descriptive-statistics.tex`, `probability.tex`), linking to those entries without repeating them.

### Findings and checks

- Conventions are stated in the entries: population ($N$) against sample ($N-1$) denominators and the bias of $s$; the $p(N+1)$ percentile rule, with the type-7 rule shown to give different quartiles ($-1.25$/2.375 against $-0.75$/2.125); skewness and kurtosis with $N$ denominators, raw against excess kurtosis, and bias-adjusted versions whose sign can differ ($-0.486$ against $+0.379$); semi-deviation targets (zero, the mean) and three denominators; the CV's ratio-scale condition, with a shifted series giving $-37.6$.
- Probability: a six-cell table reproduces the moments directly and through the laws of total expectation, variance and covariance ($47.0=2.5+44.5$; $-16.25=-1.25-15.0$). Distribution moments match closed forms, scipy and numerical integration; the $t(2)$ second moment grows without bound under truncation. The Bayesian posterior (0.0916, 0.4521, 0.4562) is identical by batch and sequential updating.
- All in `notes/artefacts/descriptive-probability/statistics-probability-checks.py` and `notes/artefacts/time-value-returns/time-value-return-checks.py`.
- Objectives now covered: `calculate-location-dispersion`, `interpret-skewness-kurtosis`, `calculate-covariance-correlation`, `calculate-downside-relative-dispersion`, `calculate-expected-moments`, `apply-financial-distributions`, `apply-bayesian-updating`. Outline items `outline:7099c7688942:m005:b01`-`b04` and `m006:b01`-`b04` reviewed one by one.

### Limits

The outline does not name its "key distributions"; chi-square and $F$ are left to the inference objectives. Web sources were read as renderings and are cited by section; Mankiw by section, its copy having no printed page numbers. Examples are synthetic and make no claim about any asset or strategy. Human review is outstanding.

## Statistics corrections and inference and simulation slice, 18 October 2026

This slice covers five bounded corrections to the statistics entries, then `topic:statistical-inference` and `topic:simulation-methods` only. Source checking and writing, not study.

### Environment

Numerical checks of this slice ran with `/opt/homebrew/bin/python3.10` (Python 3.10.16, NumPy 1.23.5, SciPy 1.10.1), which the scripts now print. The previous statistics run used Anaconda Python 3.11 (NumPy 1.26.4, SciPy 1.13.1); both give the same results. A default `python3` without NumPy or SciPy cannot run these scripts.

### Corrections

| Finding | Correction | Counterexample checked |
| --- | --- | --- |
| Unbiased $s^2$ stated without sampling assumptions | random sample (i.i.d., finite variance), Pishro-Nik sec. 8.2.2 reread; a fixed dataset is described, a sample is used to estimate | $X_1=X_2=Z$: marginal variance 1, expected sample variance 0; independent pair: 1 |
| Kurtosis read as mass in tails and centre | NIST sec. 1.3.5.11's wording (heavy tails or outliers); no central-mass claim | 0.495 at $\pm1$, 0.005 at $\pm10$: variance 1.99, kurtosis 25.50, no mass within half a s.d. (normal 0.383) |
| Sample moments called meaningless when population moments do not exist | finite samples have valid descriptive moments; only their reading as estimates fails; Student-$t$ thresholds for real $\nu$ | $t(1.5)$ sample variance finite, population infinite; $t(0.9)$ no mean, $t(2.5)$ variance 5, $t(3.5)$ infinite kurtosis, $t(4.5)$ finite |
| GBM drift and mean log return | $\ln S_T\sim N(\ln S_0+(\mu-\sigma^2/2)T,\sigma^2T)$; drift 0.07 in the existing example | mean price 107.25 unchanged |
| Independence in the Bayesian example | conditional on the hypothesis | $P(\text{up},\text{up})=0.25125>0.25$ |

The check-script path was removed from the printed section introduction; execution details stay in the evidence. Existing example values are unchanged.

### Sources, 2026-10-18

| Source key | Identity | Read |
| --- | --- | --- |
| `probability-statistics-random-processes` | Pishro-Nik, online | 7.1.2, 8.3.3, 8.4.3, 8.4.4 (8.2.2 reread) |
| `statistical-methods-handbook` | NIST/SEMATECH e-Handbook | 1.3.3.4, 1.3.5.2, 1.3.5.8, 1.3.5.9, 1.3.5.10 (1.3.5.11 reread) |
| `signed-rank-test-reference-2023` | NIST Dataplot, updated 11 December 2023 | whole page |
| `introductory-statistics-2023` | Illowsky and Dean, OpenStax 2e, 13 December 2023 | sec. 1.2 |
| `bootstrap-time-series-2003` | Politis, *Statistical Science* 18(2), author PDF, SHA-256 80c1b133…e9a61f | abstract, secs. 2, 2.3, pp. 219-223 |
| `s7-hulloptions` | as before | sec. 21.6, pp. 489-494; sec. 22.2, pp. 517-521 |

Searches: probabilitycourse.com chapter 8 sections (the guessed URLs 8_3_1 and 8_4_1 returned 404; found by search); NIST signed-rank; Politis 2003. Not used: Kunsch (1989) on Project Euclid (empty page to the fetcher).

### Existing entries inspected first

`meth:skill-luck-significance-tests` (t test, power and data needs), `meth:sharpe-ratio-standard-error`, `meth:multiple-testing-control`, `meth:var-es-estimation-methods` (historical, filtered and Monte Carlo VaR), `meth:sequential-bootstrap`, `meth:resampled-efficiency`. Their applications are linked, not repeated; six foundation entries were written in `common-toolkit/statistical-inference.tex` and `common-toolkit/simulation-methods.tex`.

### Findings and checks

- Inference on twelve invented active returns: exact $t$ interval $-0.17$ to 1.24 against the too-narrow normal interval; chi-square interval for the variance; one-sided $t$ $p=0.062$, sign test 0.194, exact signed-rank 0.076 by enumerating 4,096 patterns; power 0.49 at $n=12$ by the noncentral $t$, matched by simulation; Type I rate 4.9 percent simulated; $F=5.63$ ($p=0.008$). Simulated coverage 95.1 percent for normal samples and 75 percent for AR(1) samples.
- Simulation: equal-weight historical VaR 12,800 and ES 15,700 against an age-weighted VaR of 8,400 on the same 20 scenarios; i.i.d. bootstrap within 1 percent of its ideal value; for AR(1) with coefficient 0.5 and $n=120$ the i.i.d. bootstrap expects 33 percent of the true variance of the mean and moving blocks of 12 expect 79 percent (exact quadratic forms, confirmed by simulation); Monte Carlo call 7.1161 (s.e. 0.0396) against the closed form 7.1281.
- Seeds were fixed in advance and tolerances of four standard errors stated before running. Two of my expected values (the chi-square test $p$-value and the signed-rank normal approximation) were wrong guesses and were corrected from the computation before the entries were written.
- Objectives now covered: `construct-confidence-intervals`, `conduct-hypothesis-tests`, `choose-nonparametric-tests`, `apply-historical-simulation`, `apply-bootstrap-resampling`, `apply-monte-carlo-simulation`. Items `outline:7099c7688942:m007:b01`-`b03` and `m009:b01`-`b03` reviewed one by one; the outline item on sampling also asks for sampling methodologies, so OpenStax sec. 1.2 was read and added before promotion. The scope note on chi-square and $F$ in the distributions mapping is resolved.

### Limits

Examples are synthetic and make no claim about any manager or strategy. Block-size choice is described, not implemented. Web sources were read as renderings and are cited by section. Human review is outstanding.

## Tooling standardisation to Python 3.14 with uv and make, 18 October 2026

No source was read and no entry or coverage status changed. Evidence notes were
updated to name the environment in which the numerical checks now run.

### Environment and checks

- Locked environment: Python 3.14.7, uv 0.12.7, NumPy 2.4.6, SciPy 1.18.1, statsmodels 0.15.0 (`pyproject.toml`, `uv.lock`); `make examples` runs every check script with warnings as errors.
- All 55 check scripts pass. Their printed output matches the earlier Anaconda Python 3.11 run apart from a 1e-18 rounding residue, one printed `-0.` and one version line. `inference-simulation-checks.py` gives the same output under Python 3.10.16 (NumPy 1.23.5, SciPy 1.10.1) and 3.14.7 apart from its version line, rechecked on this date.
- Required code changes: `np.trapz` to `np.trapezoid` (two scripts, output unchanged); `float()` casts where NumPy 2 changed the scalar repr (two scripts); `result_object=False` for `adfuller`. Empirical scripts with git-ignored inputs were compared with HEAD by syntax tree, not rerun.
- `notes/entry-evidence.json` and `notes/coverage/objectives.json` now give the locked environment for the statistics and inference evidence and keep the first-run versions as history.

### Limits

Results from the data-dependent empirical scripts were not reproduced under the new versions. The PDF build and outline hashes are not part of CI.

## Regression slice and inference corrections, 18 October 2026

Source checking and numerical verification for the linear-regression slice; not study and not human review. Three corrections were made first, then three foundation objectives of `topic:linear-regression` were written.

### Sources read

| Source key | Identity | Read |
| --- | --- | --- |
| `s7-hulloptions` | Hull, 11th Global ed., local copy (printed page = PDF page - 1) | sec. 22.2, p. 517 and n. 2, p. 520, p. 521 (reread) |
| `acerbi-tasche-2001` | arXiv cond-mat/0104295v3, local copy | Definitions 2.1-2.6, pp. 3-5; Proposition 3.2, p. 6; eq. (3.3), p. 7 (reread) |
| `applied-statistics-course-notes` | Penn State STAT 500, Lesson 12; Internet Archive capture of 11 August 2026 | sec. 12.1, two-variance test |
| `statistical-methods-handbook` | NIST/SEMATECH e-Handbook, live site | sec. 1.3.5.9 (reread), sec. 1.3.6.6.9 (lognormal median and mean) |
| `regression-methods-course-notes` | Penn State STAT 501; Internet Archive captures, 16 December 2025 to 12 May 2026 | secs. 1.2-1.5, 1.8, 2.1, 2.3, 2.6-2.8, 3.2-3.3, 4.1-4.2, 4.4-4.6, 9.1-9.3 |
| `smearing-retransformation-1983` | Duan, JASA 78(383), local copy supplied by the user, SHA-256 7525fc60…36118885 | abstract, secs. 1-3, pp. 605-606; start of sec. 4 |

Access limits: the live Penn State pages failed TLS verification (incomplete certificate chain) from this environment, so archived captures were read; sections 3.3 and 4.6 had no 2026 capture and were read from captures of 16 December 2025 and 11 January 2026. Figures in the archived pages were not visible. A first search found no open copy of Duan (1983); the user then supplied one. The GitHub documentation on secrets was read through a fetched summary, which quoted that secrets other than `GITHUB_TOKEN` are not passed to workflows triggered from a forked repository.

### Corrections

- `meth:historical-simulation`. The equal-weight example used Hull's rank (second-largest of 20 losses, 12,800), while the age-weighted example used the first cumulative weight exceeding 10 percent (8,400). The second rule is the compendium's lower loss quantile; applied to equal weights it also gives 8,400 (the two worst losses carry exactly 10 percent). The claimed fall of a third came from changing conventions and is withdrawn. ES is now defined by exact tail mass with fractional weight at the VaR loss. On this sample it is 15,700 for equal weights and 14,014 for age weights, so weighting moves ES by about 11 percent and leaves VaR unchanged. The data were not changed. Hull's equal-weight choice and its footnoted alternatives (fifth-highest, sixth-highest or their average) are attributed as a different convention. The evidence check now tests the canonical function against numpy's inverted-CDF quantile and a numerical quantile integral, on uniform weights at an exact CDF boundary, tied losses and a fractional tail (np = 2.5).
- `meth:hypothesis-testing`. The F example compared two series with sample correlation 0.997 under an F distribution that needs independent samples. The second sample is now an independent draw: N(0, 0.5^2), n = 15, seed 20261018 + 7, the first draw taken, rounded to one decimal. That gives F = 4.996 on (11, 14) d.f., p = 0.0062. The entry states both conditions, normal populations and independent samples (STAT 500 sec. 12.1). It also gives a fixed-seed counterexample (seed + 9, 40,000 replications): with equal variances and correlation 0.9, the ordinary test rejects 0.05 percent of the time at nominal 5 percent; at a true s.d. ratio of 1.5 it rejects 6 percent of the time, against 24 percent for independent samples. Paired variance tests are not covered.
- Run commands. `jet_fuel_hedge_test.py` reaches `xlrd` through `backwardation_test.series` and now documents `uv run --group empirical`. The other current scripts were checked for imports of sibling scripts: `hedging_pressure_test.py` and `energy-checks.py` use only `backwardation_test` helpers that do not read spreadsheets; `heating_oil_test.py` and the other spreadsheet readers already named the group. Archived `superseded-*` scripts were left unchanged. All 55 check scripts were rerun in a separate clean default-group environment without `xlrd` and passed. README and the workflow comment now record the fork-secret limitation of CI; no remote CI run or secret configuration was exercised.

### Regression foundations

Inspected first: `mod:minimum-variance-hedge-ratio` (OLS slope, R^2 = rho^2), `meth:spread-volatility-regression` (levels and logs, lognormal correction from Lehalle and Laruelle), Jensen's alpha regression in performance evaluation, `pit:parameter-overfitting` and `meth:purged-embargoed-cross-validation`. These are linked, not repeated.

Example: ten invented bonds with leverage fixed at 20, 25, ..., 65 percent and spreads generated as y = 40 + 5x + e, e ~ N(0, 30^2) (seed 20261018 + 11, first draw, rounded to whole basis points).
- Fit: b1 = 4.802 bp per pp and b0 = 49.30; SSE 14,356.4, SSR 47,568.0, SST 61,924.4; S = 42.36 and R^2 = 0.768.
- Coefficient tests: t(b1) = 5.148, p = 0.00088; 95 percent interval 2.65 to 6.95; the test of beta1 = 5 is not rejected (t = -0.21).
- ANOVA: F = 26.507 = 5.1485^2, with the same p as the t test.
- Prediction at 45 percent leverage: 265.4, with standard error of fit 13.60 and of prediction 44.49. The 95 percent interval for the mean is 234.1-296.8; for a new bond it is 162.8-368.0.
- Coverage in 20,000 samples simulated under the declared model: mean interval 94.8 percent, prediction interval 95.0 percent. The mean interval used for a new bond covers 49.7 percent (49.9 percent exactly from t with 8 d.f.).
- Extrapolation to 90 percent leverage: the standard error of fit rises 3.4-fold.
- Log-level form: slope 0.02075 (median x1.021 per pp). At 45 percent leverage the median is 252.2, the normal-theory mean 258.2 and the smearing estimate 256.8. Duan's mixture bias of 41 percent is reproduced.
- Other forms: log-log elasticity 0.83; level-log slope 183.9.

Each result was checked by closed form against numpy least squares, statsmodels OLS, the statsmodels formula-API ANOVA table and `get_prediction` intervals. One draft expected value was a wrong guess: about 41 percent coverage for the misused mean interval. It was replaced by the computed 49.9 percent before the entry was written.

Outline review: `outline:7099c7688942:m010:b01`-`b03` were reviewed one by one against the outline page (printed p. 3) and the finished entries, and promoted. `m010:b04` (CAPM) and the four Batch 3 analysis objectives of the topic are not promoted. `m009:b01` and `m007:b02` were re-reviewed after the corrections and stay covered.

### Limits

Examples are synthetic and make no claim about credit markets. Residual diagnostics on ten points are weak evidence; no formal normality, heteroscedasticity or serial-correlation test is taught. Multiple regression, misspecification, time-series regression and the CAPM regression are deferred. Course notes are a secondary, teaching source. Human review is outstanding.

### Correction pass, 18 October 2026

A bounded correction of the slice above, after an audit of the finished entries. The earlier record is left as written; where it says F = t^2, "median" for back-transformed log predictions, or ES "beyond" VaR leaving 18,600, read this subsection.

Sources read in this pass:

| Source key | Identity and access | Read |
| --- | --- | --- |
| `linear-regression-lectures` | Marco Taboga, StatLect, live pages, 2026-10-18 | "Normal linear regression model": Setting; Assumptions; Distribution of the OLS estimator; Estimation of the variance of the error terms. "Linear regression - Hypothesis testing": all sections, including the t, F, z and Chi-square tests. "Gauss Markov theorem": Assumptions; OLS is linear and unbiased; The covariance matrix of the OLS estimator |
| `back-transformed-forecast-mean-2014` | Rob J Hyndman, "The forecast mean after back-transformation", Hyndsight, 25 February 2014, live page | the whole post; the opening paragraph supports the symmetry condition for the median |
| `smearing-retransformation-1983` | Duan (1983), local copy, SHA-256 unchanged (7525fc60...36118885) | sec. 2, p. 606, reread |

Access limits: StatLect renders formulas as images. The prose was read from the HTML. The Gauss-Markov assumption formulas, E[eps|X] = 0 and Var[eps|X] = sigma^2 I, were read by cropping the page's equation sprite; the other formula images were not transcribed. A headless browser was unavailable, and WebFetch summaries were cross-checked against the raw HTML text. StatLect does not state that a single-restriction F equals the squared t for the same null value. The entry marks that step as algebra, and the statsmodels check confirms it numerically.

Corrections:
- `meth:simple-regression-estimation`. The claim "can be computed for any data" was replaced. The intercept and slope exist and are unique for finite data with Sxx > 0, which is the one-predictor case of full rank. Fitting assumes nothing about the errors.
- `meth:regression-diagnostics-anova`.
  - MSE, standard errors and tests need n > 2.
  - Conditions now separate four stages: computing; unbiasedness (linear mean, E[eps|X] = 0); conventional variances and BLUE (Var[eps|X] = sigma^2 I); and exact t/F inference (normal errors).
  - Without normality, the tests are large-sample approximations. Least squares remains consistent (Duan p. 606).
  - F = t^2 is restricted to the zero-slope null. ANOVA F = 26.506953 = 5.148490^2. The test of beta1 = 5 has t^2 = 0.044865, which equals the statsmodels f_test F for that restriction (p = 0.83755 for both), not the ANOVA F.
- `meth:regression-prediction-functional-form`.
  - exp(E[log Y | x]) is the conditional geometric mean. It is the median only when the log error has median zero.
  - The normal-theory estimate is consistent for exp(x0 beta + sigma^2/2) whatever the errors. It equals E Y0 under normality but "might not" otherwise (Duan p. 606), so normality is sufficient but not necessary. The arithmetic-mean corrections (normal theory, smearing) and their stated assumptions are unchanged.
  - The log-log rule is now 100 (1.01^b1 - 1) ≈ b1 percent. For b1 = 0.825869 this gives 0.825153 percent, or a fraction of 0.00825153.
  - The log-level and 45 percent figures (1.021 factor; 252.2) are now labelled geometric means. A new original counterexample uses eps = 0.5(E - 1) with E standard exponential, which has mean 0 and variance 0.25. Relative to exp(x beta), the factors are: geometric mean 1, median 0.8578, mean 1.2131 and normal-theory 1.1331.
- `meth:historical-simulation`. The pitfall was stale. At the canonical VaR of 8,400, the mean of strictly greater losses is 15,700. It equals ES only because those two losses carry exactly the 10 percent tail. Only Hull's 12,800 threshold leaves 18,600 alone. Both values were already asserted in `inference-simulation-checks.py`, which is unchanged; data, convention and results are unchanged.

Numerical evidence: `regression-checks.py` gained four targeted checks:
- matching versus different slope nulls;
- the geometric-mean identity (exp of the fitted log at mean leverage equals the sample geometric mean, 239.444, by scipy gmean);
- the skewed log error, by closed form against scipy expon and quadrature;
- fraction versus percentage for the log-log change.

No seed, data or general framework was added.

Outline re-review: `outline:7099c7688942:m010:b01`-`b03` were re-read against the outline page (PDF and printed p. 3) and the corrected entries. All three remain covered, and b02's "describe and compare the assumptions" is now met more fully. `b04` (CAPM) and the four Batch 3 objectives of `topic:linear-regression` were not promoted.

### Second correction pass, 18 October 2026

Bounded audit findings on the corrected regression entries; earlier text above is left as written.

- `meth:regression-diagnostics-anova`: the claim that least squares "remains consistent ... whether or not the errors are normal" omitted Duan's condition. Reread sec. 2, pp. 605-606: errors i.i.d. with mean 0 and variance sigma^2, and coefficients and predictions "unbiased and also consistent if the design matrix is asymptotically nondegenerate". The entry now quotes the condition and adds a counterexample, derived here: x_i = 2^-i is full rank in every sample but Sxx tends to 1/3, so Var(b1) = sigma^2/Sxx tends to 3 sigma^2. The check uses exact rational arithmetic against the closed form (1 - 4^-n)/3 - (1 - 2^-n)^2/n and numpy at n = 60; Sxx is 0.2335, 0.3083 and 0.3283 at n = 10, 40 and 200.
- `meth:regression-prediction-functional-form`: the normal-theory consistency statement now refers to the same design and moment conditions. The smearing estimate's weak consistency is stated with Duan's Theorem 1 (sec. 4, p. 607, read in full for the first time): h continuously differentiable, an intercept, X'X/n tending to a positive-definite matrix, and a moment condition that for logs is E exp(2 eps) < infinity. Duan calls condition (iii) "much stronger than we need".
- Topic ownership: `objective:estimate-capm-regression` belongs to `topic:asset-pricing-factor-models` (as `objectives.json` already records), not `topic:linear-regression`.
- `notes/readings/linear-regression-lectures.md`: the Gamma(N-K, sigma^2) statement follows StatLect's degrees-of-freedom and mean parameterisation ("Gamma distribution" lecture, Caveat and Definition, live page read 2026-10-18). The note now names that convention and gives the shape/scale equivalent; the statement itself was not wrong.

## Portfolio moments and diversification slice, 18 October 2026

Source checking and numerical verification for `objective:calculate-portfolio-moments` and `objective:explain-diversification` (`topic:portfolio-risk-return`); not study and not human review.

### Existing entries reviewed first

- `def:return-dependence`: covariance, correlation, denominators and limits for two return series.
- `def:conditional-moments`: probability-weighted moments.
- `def:return-sample-statistics`: N and N-1.
- `mod:mean-variance-portfolio-optimisation`: uses mu and Sigma; Narang's rolling correlations.
- `meth:portfolio-covariance-estimation`: large-N estimation.
- `def:return-measures`: one-period total return.

None states the portfolio return from value weights, portfolio moments or the correlation sensitivity, so two foundation entries were written and link to these entries rather than repeat them.

### Searches and sources

Searches (2026-10-18): "portfolio variance two assets correlation minus one zero variance weights lecture notes"; "Longin Solnik Extreme Correlation of International Equity Markets pdf". The catalogue (`s6-markowitz`, `w2-longin-solnik`) supplied the two primary sources.

| Source key | Identity and access | Read |
| --- | --- | --- |
| `s6-markowitz` | Markowitz, "Portfolio Selection", JF 7(1), 1952; the catalogue's scanned PDF (no text layer), SHA-256 0af6b760...0e473, read as rendered page images | pp. 77-81 |
| `w2-longin-solnik` | Longin and Solnik, working paper of April 2000 ("Forthcoming in The Journal of Finance"; JF 56(2), 2001); Internet Archive capture of 9 August 2017 of the HEC copy, SHA-256 b4a8c39a...0fa18 | abstract, pp. 1-2; p. 3 skimmed |
| `probability-statistics-random-processes` | probabilitycourse.com sec. 5.3.1, fetched rendering | Lemma 5.3 item 7; eq. (5.21) |
| `linear-regression-lectures` (correction) | StatLect "Gamma distribution", live page | Caveat; Definition |
| `smearing-retransformation-1983` (correction) | Duan (1983), local copy | secs. 2 and 4, pp. 605-607 |

Access limits:
- The Markowitz formulas were read from page images, and two printing slips on p. 81 are recorded in the reading note.
- The Longin-Solnik CEPR copy returned a Cloudflare challenge, and hec.fr no longer serves the file, so the archived working paper was used. Journal pagination is unchecked.
- probabilitycourse.com refused a direct download (HTTP 406), so its section was read through a fetched rendering.
- OpenStax *Principles of Finance* 2e sec. 15.2 was fetched during the search but is not cited. Its page says the book may not be "ingested into large language models or generative AI offerings" without OpenStax's written permission. The same notice may apply to the earlier use of sec. 15.1 (`principles-of-finance-2026`); that is left for the owner to decide.
- No source read gives the beginning-of-period value-weight identity, the long-only weighted-average bound, the zero-variance weights, the threshold rho < sigma2/sigma1 or the equal-weight floor in so many words. The entries mark them as derivations and the script checks each.

### Entries and examples

New file `compendium/portfolio-construction-risk/portfolio-moments.tex`, input from the chapter wrapper before the construction models, with two entries:
- `meth:portfolio-return-moments`.
- `mech:diversification-correlation`.

Example 1 is a three-state, one-year model in US dollars with 600,000 in E and 400,000 in B:
- E[R_P] is 5.86. Var(R_P) is 87.57 + 2.8224 - 30.96 = 59.43, a standard deviation of 7.71.
- Q (30/70) has E 4.63 and Var 3.4461. Cov(P, Q) is 13.894 and corr(P, Q) is 0.971, although the assets' correlation is -0.985.

Example 2 is six hand-typed monthly returns:
- Variances over N-1 are 7.048 and 0.2907, and the covariance is -1.336; over N, 5.873, 0.2422 and -1.113. The correlation is -0.933 with either denominator.
- The rebalanced 60/40 series has mean 0.727 and variance 1.9425 = w'Sw. Under buy and hold the weights drift to 0.606/0.394.

Diversification, with weights 0.6/0.4 and volatilities of 20 and 10 percent:
- The portfolio s.d. is 16.0, 13.74, 12.65 and 8.0 at rho = +1, 0.3, 0 and -1.
- Variance is zero at w = 1/3 when rho = -1. At rho = 0 the mix is not below the safer asset's 10 percent, while a 20 percent equity weight gives 8.94.
- An equal-weight portfolio with s.d. 20 and rho 0.3 has a floor of 10.95.
- Longin and Solnik's 0.21 and 0.62 are reproduced analytically (0.2131 and 0.6184).

The first draft of the check script had several expected values typed before computing, such as a scenario variance of 213.25. They failed and were replaced by the computed values before the entries were written. The data were not changed after that run.

### Coverage

`outline:7099c7688942:m008:b01`, `m087:b04`, `m087:b05` and `m087:b06` were each read on the outline pages (PDF p. 2, and PDF p. 27 = printed p. 1) against the finished entries, and promoted. Both objectives are `covered`; this is editorial coverage, not mastery.

Not promoted:
- `m008:b02`-`b03` and `m087:b01`-`b03`, `b07`: efficient frontier, optimal portfolio, risk aversion and asset classes.
- CAPM, beta and systematic risk.
- The advanced regression objectives.

Totals are 29 of 424 objectives and 33 Level I outline items covered.

### Limits

The examples are synthetic: both happen to show strongly negative stock-bond correlations, which is not a claim about markets. Model moments are taken as given; how expected returns are estimated is not taught. Tail dependence beyond Longin and Solnik's summary, time-varying correlation models and the pricing of systematic risk are deferred. Human review is outstanding.

## Portfolio choice and asset pricing batch, 18 October 2026

Source checking, implementation and numerical verification for the four remaining objectives of `topic:portfolio-risk-return` and the eight of `topic:asset-pricing-factor-models`. This is not study and not human review.

### Audit corrections first

- `mech:diversification-correlation`: the equal-correlation limit is now qualified by sign. A fixed positive correlation leaves a positive floor; zero correlation gives sigma^2/N, which tends to zero; a fixed negative correlation cannot be kept as N grows. For N > 1 an equicorrelation matrix is valid only for -1/(N-1) <= rho <= 1 (eigenvalues 1 + (N-1) rho and 1 - rho). Markowitz's p. 79 sentence is kept and attributed. `portfolio-moments-checks.py` gained six boundary checks.
- `notes/readings/s6-markowitz.md`: the matching-hash scan at `reading_materials/derivatives-validation/src/Markowitz1952.pdf` has a JSTOR cover as one-based PDF page 1. Printed p. 81 is PDF p. 6, so PDF page = printed page - 75; the earlier "- 76" was wrong.

### Existing entries reviewed first

- `meth:portfolio-return-moments` and `mech:diversification-correlation`: reused for moments and diversification.
- `mod:mean-variance-portfolio-optimisation`: has Boyd et al.'s closed form for the risk-aversion objective and the infeasibility of a small target, but no frontier, GMV, CAL or CML. It stays a candidate; the new entries link to it and state gamma = A/2.
- `mod:factor-risk-model`: covers the factor covariance decomposition and economic against statistical factors (Narang; Boyd et al.). It is reused for `objective:compare-factor-model-types`; the three-way comparison, outputs and pricing are new.
- `meth:relative-performance-evaluation`: Harris's realised alpha and Jensen's alpha, and appraisal smoothing. Cross-referenced, not repeated.
- `meth:simple-regression-estimation`, `meth:regression-diagnostics-anova`: the OLS mechanics and assumptions are reused by the CAPM regression rather than repeated.

### Searches and sources

Searches (2026-10-18): "Fama French 2004 Capital Asset Pricing Model Theory and Evidence pdf"; "Huberman Wang Arbitrage Pricing Theory staff report 216"; "Connor Korajczyk factor models of asset returns"; "Sharpe 1964 Capital Asset Prices pdf"; "Ross 1976 arbitrage theory of capital asset pricing pdf"; "Connor 1995 three types of factor models pdf"; "Pratt 1964 risk aversion in the small and in the large pdf"; "Damodaran historical returns 1928-2025"; "UBS Global Investment Returns Yearbook 2025 summary"; "investor.gov beginners guide asset allocation".

| Source key | Identity and access | Read |
| --- | --- | --- |
| `s6-markowitz` | JF 7(1), 1952; matching-hash scan, page images | pp. 82-91 (added to pp. 77-81) |
| `capm-theory-evidence-2004` | Fama and French, JEP 18(3), 2004, DOI checked; published pages from a Tuck course-site copy (AEA refused download) | whole article |
| `capital-asset-prices-1964` | Sharpe, JF 19(3), 1964, DOI checked; JSTOR scan filed with the Kentucky PSC, page images, PDF = printed - 423 | pp. 430, 432-435, 437-440 |
| `arbitrage-theory-1976` | Ross, JET 13(3), 1976, DOI checked; journal scan on an HEC faculty page | pp. 341-348, 352-355 |
| `arbitrage-pricing-review-2005` | Huberman and Wang, FRBNY Staff Report 216 | abstract, secs. 1-9 |
| `factor-model-types-1995` | Connor, FAJ May-June 1995; author deposit at Maynooth (CC BY-NC-SA) | pp. 42-46 |
| `risk-choice-review-2013` | Gollier, Hammitt and Treich, IDEI WP 804 | pp. 1-5, 13-14 |
| `us-asset-returns-1928-2025` | Damodaran histretSP.xls, January 2026 update | "Returns by year", "Explanations and FAQ", "Small Cap" |
| `implied-equity-premium-2026` | Damodaran home page, implied ERP on 1 October 2026 | that section; histimpl.html 2020-2025 |
| `asset-allocation-investor-guide` | SEC investor guide, investor.gov PDF | pp. 1-3 |
| `ust-par-yield-curve` (existing key) | Treasury daily par yields, 2026 file retrieved again | 30 September 2026 row |

Hashes, versions and page offsets are in the reading notes. Access limits:
- Pratt (1964) is paywalled (JSTOR, Econometric Society), so the Arrow-Pratt result is cited from the Gollier-Hammitt-Treich review.
- The UBS yearbook (Dimson, Marsh and Staunton) returned HTTP 403, so the historical table is US-only, with the survivorship caveat stated as interpretation.
- Connor and Korajczyk's 2010 chapter was found only as a listing; Connor (1995) was used.
- The AEA, ScienceDirect, Springer, SEC HTML and UBS pages refused automated download. Authorised or author-hosted copies were used, and DOIs were confirmed with Crossref.
- Damodaran's small-cap column was excluded: its geometric mean is inconsistent with its arithmetic mean, and its 2025 value is partial.
- Tobin (1958), Lintner (1965), Merton (1972) and Chen, Roll and Ross (1986) were not read; their results are cited only as reported by the sources above.

### Entries and examples

New topic files, input after `portfolio-moments`:
- `portfolio-choice.tex`: `def:asset-class-characteristics`, `def:risk-aversion-utility`, `meth:efficient-frontier` and `meth:capital-allocation-line`, with figure `figures/mean-sd-frontier.tikz`.
- `asset-pricing-models.tex`: `mech:systematic-risk-pricing`, `mod:return-generating-models`, `mod:capm-sml`, `meth:capm-regression`, `meth:required-return-on-equity`, `mod:multifactor-apt` and `def:factor-model-types`, with figure `figures/security-market-line.tikz`.

`portfolio-choice-checks.py` (49 checks) covers the following:
- The 1928-2025 table: the workbook's six arithmetic and geometric means are reproduced to 0.005 points.
- Utility: in decimal and percent units; CARA-normal certainty equivalent by integration.
- The three-fund frontier: closed forms against SLSQP; long-only boundary solution with its KKT multiplier; infeasible 9 percent target; dominated portfolios; simplex grid.
- The tangency against maximum-Sharpe SLSQP, and y* for A = 2, 4, 8 against grids.
- Borrowing at 3.5 percent. At 5 percent, above the GMV mean of 3.87, the tangency formula gives a lower-branch point; the first draft used 5 percent and was changed for that reason.
- The figure coordinates.

`asset-pricing-checks.py` covers the following:
- The twelve-month regression by closed form, numpy lstsq and statsmodels OLS: beta 1.2548, alpha 0.1108 percent a month (t 0.26), R^2 0.813.
- Raw against excess returns (a - alpha = -0.0949, of which -0.0932 is (1 - beta) mean r_f).
- SML and CML numbers and the SML figure.
- The cost of equity: 10.12 percent; 9.09 to 11.81 across published premia; 8.78 to 12.34 across the beta interval.
- The APT arbitrage: replica weights (1.0, 0.2, -0.2), an 8,000 sure profit, and 25/sqrt(n) residual risk in the single-stock version.
- Factor attribution: x'Fx = 16.48, factor share 80.5 percent.

Several expected values in both scripts were typed before the first run and failed: a stock count of 27 (actual 26), real T-bill losses of 37 (actual 40), factor variance 20.04 (actual 16.48), replica weights and the stock's mean return. They were replaced by computed values before the entries were written; no data were changed after that.

### Layout correction

The PDF review found entry titles stranded at the foot of a page, apart from their Statement: printed pp. 75 (new) and three earlier pages (PDF pp. 107, 139, 149). The `\label` after `\begin{qf<type>}` writes a whatsit after the title's `\nopagebreak`, which makes the following glue a legal break. `house.tex` now repeats `\nopagebreak` at the first field of an entry, and a scan of all 209 pages finds no stranded title.

### Coverage

The 23 outline items mapped to the 12 objectives were each read on their outline pages and against the finished entries, and all 23 were promoted:
- Level I: `m008:b02`-`b03` (PDF p. 2), `m010:b04` (p. 3), `m050:b01`-`b02` (p. 17), `m087:b01`-`b03` and `b07` (p. 27), `m088:b01`-`b08` (pp. 27-28).
- Level II: `m040:b01`-`b06` (p. 26). `m040:b07` (active risk and the information ratio) maps to another objective and was not reviewed.

All 12 objectives are `covered`; this is editorial coverage, not mastery. Totals: 41 of 424 objectives covered; 50 Level I and 6 Level II items covered; 974 of 1,030 items unreviewed.

### Limits

- The examples are synthetic except the dated US table and the 1 October 2026 inputs, and the beta of 1.15 is assumed.
- The historical table is one country's and excludes small caps.
- The implied premium is one practitioner's model, and his method paper was not read.
- Pratt, Tobin, Lintner, Merton (1972) and Chen-Roll-Ross were not read directly.
- No empirical CAPM or factor test is run.
- Human review is outstanding.

## Correction pass on PR #22, 18 October 2026

A fixes-only pass on `907e84b`. This is not study and not human review.

- `meth:efficient-frontier`: removed the claim that constrained solutions necessarily have zero weights. The entry now states that an unconstrained optimum meeting the limits stays optimal, that binding limits give boundary solutions, and that no single unrestricted formula covers active-set changes. Markowitz p. 87, n. 10 is reused. The added assertion confirms that the 5 and 6 percent long-only optima equal the strictly positive unconstrained weights, and that 7.5 percent does not.
- `meth:required-return-on-equity`: a historical premium with the current 10-year yield is described as a legitimate CAPM estimate with its own assumption and estimation error:
  - 13.38 percent arithmetic and 11.60 geometric; two-standard-error band 8.54 to 18.21.
  - The mechanical mismatch is now described separately: an implied premium paired with a rate other than its own.
  - Damodaran's corporate finance project notes (cfprojectsumm.htm, SHA-256 6c0e6d5a...0c76, undated; sec. V.a "Riskfree Rates" and V.b "Risk Premiums") were read on 2026-10-18 and are registered as `corporate-finance-project-notes`. No numbers are taken from them because the page is out of date.
  - Fama and French's 2.4-point standard error is now attributed to the premium over bills.
- `def:asset-class-characteristics`: one sentence now names both implied and historical premia.
- CI moved to merged pull requests into `main`, checking out `merge_commit_sha`. This was validated locally by `check-yaml` and an event simulation; a live merge event is unverified.
- The earlier "CI pending" statement is reconciled: run 39119458178 passed on `907e84b` only.
- Coverage unchanged: 41 of 424 objectives.

## Performance and planning batch, 18 October 2026

Thirty objectives in nine topics: market index construction (2), the investment management process (3), investment policy planning (4), behavioural finance (2), the risk management framework (2), active management (3), performance evaluation (7), manager selection (3) and performance presentation standards (4). Branch `codex/performance-management-20261018`, stacked on PR #22 at `e82bb90`. Source checks and numerical verification; not study and not human review.

### Source discovery

Searches on 2026-10-18 used subject terms (index divisor and corporate actions; fixed-income index rebalancing and return universes; transfer coefficient and fundamental law; behavioural finance survey; GIPS portability and verification; Rule 205-3 qualified client 2026; ESG integration definitions; investment company fact book 2026). The owner's local library was searched first and supplied the books. Sources read, with sections and identities in their reading notes:

- S&P DJI, *Index Mathematics Methodology* (September 2026), pp. 4-16, 21-22 and 70, and *Equity Indices Policies & Practices* (August 2026), pp. 5-8, 19 and 24. spglobal.com returned HTTP 403 to automated requests, so both were read from Internet Archive captures of the official URLs (1 October and 29 September 2026).
- Bloomberg, *Fixed Income Index Methodology* (8 January 2026), pp. 9-10, 42-43, 47-48 and 57-61.
- Bacon, *Practical Portfolio Performance Measurement and Attribution* (3rd ed., 2023), chaps. 3-6 and 8 at the pages listed in `notes/readings/wide-bacon-attribution.md`.
- Maginn, Tuttle, McLeavey and Pinto (eds.), *Managing Investment Portfolios* (3rd ed., 2007), chaps. 1-3, 5, 7, 9 and 12, used as authored chapters (chap. 9 by Chance, Grant and Marsland; chap. 12 by Bailey, Richards and Tierney), not as an outline.
- Grinold and Kahn, *Active Portfolio Management* (2nd ed.), chaps. 3-6 at the pages listed (equations are images, so formulas were confirmed from text, tables and worked numbers), and *Advances in Active Portfolio Management* (2020), Insight 5, pp. 23-29.
- Ang, *Asset Management* (2014), chaps. 1, 3, 15, 16 and 17 at the pages listed.
- Barberis and Thaler, NBER w9222 (September 2002), secs. 1-3, 5-7, read through a local OCR because the body pages lack a text layer; locators are working-paper pages.
- Statman, *Behavioral Finance: The Second Generation* (2019), chaps. 1, 3 and 4 (section openings); Kahneman, *Thinking, Fast and Slow*, chaps. 7 and 24; Damodaran, *Strategic Risk Taking* (2008), pp. 303-304 and 331-339.
- Sharpe, "The Sharpe Ratio" (1994) and "Asset Allocation: Management Style and Performance Measurement" (1992), author-hosted reprints.
- GIPS for Firms 2020 (Preface, Introduction, secs. 1-3 in full, 4.A and 4.C.1-4.C.40, Glossary p. 75); GIPS Handbook for Firms (November 2020), Provisions 1.A.32, 3.A.2, 3.A.7-3.A.8, 3.A.12 and 4.A.1(i)-(j); GIPS for Verifiers 2020, pp. 1-7 and 11-12.
- ICI, *2026 Investment Company Fact Book* (chap. 2 and Quick Facts Guide, year-end 2025); GSIA, *Global Sustainable Investment Review 2022*, p. 7.
- US law, current at 18 October 2026: 15 U.S.C. 80b-5 and 17 CFR 275.205-3 (Legal Information Institute; eCFR blocked automated access); the SEC order of 1 May 2026 (FR 2026-08480, effective 29 June 2026) and the March notice; the SEC proposal of 6 October 2026 (FR 2026-20474, comments due 7 December 2026, not law).

Access limits and substitutions:
- Clarke, de Silva and Thorley (2002) is paywalled; the transfer coefficient is cited through Grinold and Kahn (2020), who credit it.
- Brinson, Hood and Beebower (1986), Brinson and Fachler (1985), Treynor (1965), Jensen (1968), Modigliani and Modigliani (1997), Sortino and van der Meer (1991), Treynor and Black (1973), Fong, Pearson and Vasicek (1983) and Grinold (1989) were not read directly; their methods are cited through Bacon, Bailey et al. and Grinold and Kahn.
- The PRI's ESG-integration page is script-rendered and could not be read live or from the archive; the harmonised CFA Institute/GSIA/PRI definitions reproduced by GSIA were used.
- investor.gov returned HTTP 403; fund structures rest on Ang and ICI.
- No curriculum text was used as a substantive source; the outlines defined scope only.

### Entries

Thirty new entries in six topic files and one extension:
- `international-equity-markets/index-construction.tex`: `meth:index-value-return-calculation`, `def:equity-fixed-income-index-types`.
- `portfolio-construction-risk/investment-process-planning.tex`: `def:portfolio-management-process`, `def:investor-types-needs`, `def:asset-management-industry`, `meth:investment-policy-statement`, `meth:asset-class-portfolio-construction`, `ex:investment-planning-case`.
- `behavioural-finance.tex`: `def:behavioural-biases`, `mech:biases-market-anomalies`.
- `risk-governance.tex`: `def:risk-management-framework`, `meth:risk-identification-modification`.
- `active-management.tex`: `meth:active-return-information-ratio`, `res:fundamental-law-active-management`, `meth:active-risk-decomposition`.
- `performance-attribution-appraisal.tex`: `def:performance-evaluation-components`, `meth:risk-adjusted-performance-measures`, `meth:return-attribution`, `meth:macro-attribution-owner-manager`, `meth:benchmark-selection-quality`, `meth:downside-appraisal-measures`, `meth:manager-skill-evaluation`.
- `manager-selection.tex`: `meth:manager-due-diligence`, `meth:manager-philosophy-process-behaviour`, `meth:vehicle-contract-fee-analysis`, `ex:manager-selection-case`.
- `performance-standards.tex`: `def:gips-scope-verification`, `meth:gips-return-calculations`, `meth:gips-composite-membership`, `ex:gips-composite-report`.
- `meth:gips-composite-presentation` (in `performance-evaluation.tex`) gained presentation and updating duties and portability.

The existing entries named in the brief were reviewed first. `def:equity-indices-derivatives`, `def:return-measures`, `meth:relative-performance-evaluation`, `meth:forecast-scaling-ic` and the factor-risk, CAPM and downside entries are linked, not repeated. `meth:skill-luck-significance-tests` is mapped, with the new skill entry, to `objective:evaluate-manager-skill`. The GIPS presentation entry is mapped, with the new report example, to `objective:prepare-compliant-presentations`.

### Numerical evidence

Six scripts, found by `make examples`, 164 checks, no random draws:
- `market-index-construction/index-construction-checks.py` (30): divisors for a split and a share issue in both additive and multiplicative forms, TR and NTR, equal-weight drift and turnover, a two-bond month.
- `investment-planning/investment-planning-checks.py` (25): Maginn's required returns reproduced; the case's 2.70 percent requirement solved and rolled forward to zero; three candidate allocations; Euler risk contributions; the concentrated stock; a futures overlay modelled as moving equity to cash; Edwards's posterior.
- `active-management-analysis/active-management-checks.py` (30): ex post IR and Sharpe; Grinold-Kahn Table 5.3; optimal active risk by numerical maximisation; fundamental-law examples and the binary example; IR_P = TC x IR_Q to machine precision; two decompositions of active variance.
- `performance-evaluation/performance-evaluation-checks.py` (35): risk-adjusted measures; Bacon Table 5.6; downside, capture and drawdown with edge cases; Brinson and Carino; fixed-income attribution summing exactly; macro attribution; benchmark statistics; Exhibits 12-19 and 12-20.
- `manager-selection/manager-selection-checks.py` (19): fee schedules, expected fees by numerical integration, Ang's NAV path, filter error rates, SLSQP style analysis, IR shrinkage.
- `performance-presentation-standards/gips-checks.py` (25): true TWR against Modified Dietz, three composite methods, dispersion with n and n - 1, the 36-month factor, a membership calendar, model-fee net returns, a synthetic report.

Findings from the checks:
- Bailey, Richards and Tierney's Exhibit 12-19 equals Phi(IR sqrt(T)) in 33 of 36 cells when its "0.67" column is read as 2/3; it prints 84.03 (IR 1.00, one year), 63.81 and 81.70 (IR 0.20, three and 20 years) where the model gives 84.13, 63.55 and 81.45. Exhibit 12-20 is within 0.05 points of a binomial with p = 0.2442.
- Several expected values were typed before the first runs and failed (index and bond returns, case drift and concentrated-stock volatility, the toy IR series, transfer-coefficient and active-risk figures, fee expectations, composite returns, a membership off-by-one in the script's own rule). They were recomputed, checked by hand, and replaced before the entries were finalised. One check was wrong in substance: a futures overlay was first modelled without the cash leg, and now moves 10 points from equity to cash, reducing the mean by 0.50 rather than 0.55.

### Coverage

The 72 outline items mapped to the 30 objectives were each read on their outline pages (Level I PDF pp. 1, 15, 19 and 28; Level II p. 26; Level III core pp. 9-10) against the finished entries. Six bullets exposed gaps that were closed before promotion: risk interaction and method choice (m092:b06-b07) and tolerance's effect (b04); risk-attribution choice (m013:b07); misspecification's effects (b12); drawdown duration (b14); contract types and the three fee forms (m014:b08-b09); a facts-based discretion determination (m015:b06); and the verification process (m015:b11). All 72 items are promoted with item-specific rationales.

All 30 objectives are `covered` (editorial coverage, not mastery). Totals: 71 of 424 objectives; 78 Level I, 13 Level II and 37 Level III core items covered; 902 of 1,030 items unreviewed.

### Limits

- All examples are synthetic or invented except the dated ICI figures and the legal thresholds. They establish mechanics, not performance or skill; the planning case, the foundation case and the GIPS report are fictional and claim nothing about any person or firm.
- Index rules are S&P DJI's and Bloomberg's at their stated dates; other providers differ. US legal points are dated to 18 October 2026; the October 2026 proposal could change them.
- The Barberis and Thaler locators are working-paper pages from OCR; the anomaly figures are quoted from the survey, not recomputed.
- Human review is outstanding.

## Correction pass on PR #23, 18 October 2026

A fixes-only pass on `0b094ea`, after an external audit. This is not study and not human review. No objective was added and no coverage status or outline mapping changed.

Sources re-read for this pass:
- Sharpe (1992), "Style Analysis", from the hashed local copy (SHA-256 3f82fa85...6286, identical to the batch's) and the live author page: weights minimise the variance of the difference, and the objective "is not to minimize either the average value of this difference or the sum of the squared differences".
- Bacon (3rd ed., 2023), pp. 203-204, from the owner's local PDF: eqs. (5.80)-(5.81) divide by all n; the p. 204 note says a normal distribution with standard deviation 1 has a semi-standard deviation "about 0.6", with no target stated.
- MIP chap. 12, p. 769, from the owner's local PDF: alpha and Treynor "will always give the same assessment", argued from a positive-alpha account plotting above the ex post SML.

Corrections:
- `meth:manager-due-diligence` (style analysis). The script minimised `((fund - X w)^2).var()`, the variance of the squared differences, not Sharpe's objective. Corrected to `(fund - X w).var()`. Weights 1.3745, 56.6014, 0, 27.1260 and 14.8981 percent (previously 1.1787, 55.4429, 0, 28.4609, 14.9175); residual variance 0.05586964 against 0.05604418 for the previous weights; R^2 0.98568 (unchanged at three decimals). New checks: an independently written centred quadratic form gives the same weights and minimum; the KKT conditions hold; adding 2 points to every fund return leaves the weights unchanged; the mean-square objective moves under the same shift and has higher tracking variance. Recovering the construction weights is kept only as a consistency check.
- `ex:investment-planning-case`, `meth:asset-class-portfolio-construction`. Tax basis stated: capital market assumptions are real and pre-tax; a flat 15 percent tax falls on nominal returns as earned, with full loss offset; the after-tax real return is exactly (1 - t) r - t pi/(1 + pi). The 20 percent gains tax falls only on the embedded 300,000 gain, 20,000 nominal at the end of years 1-3, paid from the pool; later stock returns are in the 15 percent regime, so no return is taxed twice. Requirement 2.699 percent without and 2.808 percent with the gains tax (roll-forward to zero). After-tax geometric returns 1.70, 2.40 and 2.87 percent; pre-tax 5th percentiles -7.81, -11.73 and -15.61 (after-tax -7.01, -10.34, -13.64). The previous verdict, balanced "meets both", compared pre-tax forecasts with an after-tax requirement; no candidate meets both. The best long-only mix within the pre-tax limit is about 61/39/0/0 at 2.61 percent; with an after-tax limit, 71/29/0/0 would reach 2.83, 0.03 above, and this is disclosed. Funding gap 283,249 at 62; spending of about 132,000, savings of about 60,650 or retirement at 64 would close it. The IPS return objective is now 2.40 percent with the client's resolution recorded.
- `ex:investment-planning-case`, `meth:risk-identification-modification` (transition hedge). The script applied the 10 percent hedge to the four-asset diversified mix (9.34 to 7.79 percent) while the prose described hedging with the stock still held. Recomputed on the five-asset weights and covariance: 12.1912 to 10.8922 percent, mean down 0.50 points. With the stock's expected real return assumed equal to equity's 5.5 percent, the 5th percentile goes from -16.43 to -14.80, still beyond -13; about 22 percent notional would be needed, and the minimum-variance hedge leaves 6.75 percent. Selling the first third with the hedge gives -12.52, and after the second sale -12.73 unhedged. A beta-consistent 7.06 percent changes no verdict. Specific risk (28 of the stock's 35 points) is unhedgeable by an index future. The 7.79 figure is no longer used.
- `ex:manager-selection-case`. Removed the claim that the prior cannot change the direction of the comparison: posterior IRs are X 0.27746 and Y 0.23386 at a prior sd of 0.30, and X 0.42923 and Y 0.47143 at 0.50, crossing at 0.419. The decision to hire X now rests explicitly on process, attribution and operational evidence.
- `meth:downside-appraisal-measures`. Removed the unconditional 0.6-sigma claim. For a normal distribution, eq. (5.80) gives sigma/sqrt(2) at the mean, 0.2745 sigma one sd below and 1.3873 sigma one sd above (closed form and numerical integration). Bacon's 0.6 is attributed and matched to sqrt(1 - 2/pi), the conditional sd below the mean; this agrees with `def:downside-relative-dispersion`. The Sortino example is unchanged (its arithmetic is unaffected).
- `meth:risk-adjusted-performance-measures`. alpha = beta (T_P - T_M), so agreement requires beta > 0; Treynor is undefined at beta 0 and reverses for negative beta (rf 3, market 8, return 0, beta -1: alpha +2, Treynor 3 against 5). Positive, zero and negative beta checks added; a pitfall added. Positive alpha stays separate from skill.

Checks: `investment-planning-checks.py` 41 (was 25), `manager-selection-checks.py` 26 (was 19), `performance-evaluation-checks.py` 41 (was 35); the batch total is 193. Coverage reassessed for the nine objectives mapped to these entries; each still meets its operations and depth with the corrected teaching, so counts are unchanged: 71 of 424 objectives; 78 Level I, 13 Level II and 37 shared-core items covered; 902 of 1,030 unreviewed.

## Fixed-income and derivatives batch, 18 October 2026

Thirty objectives in six topics: bond features, issuance and markets (5), bond pricing and yields (4), the term structure (6), interest-rate risk (4), derivative instruments and markets (4) and forward, futures and swap valuation (7). Branch `codex/fixed-income-derivatives-20261018`, from `main` at `a1cf781` after PRs #22 and #23 were merged. Source checks and numerical verification; not study and not human review.

### Source discovery

Retrieval on 2026-10-18 targeted these subjects (Treasury price formula with a simple-interest first period; Rule 15c6-1 T+1 compliance date; Trust Indenture Act exemption threshold; Rule 144A qualified institutional buyer; prospectus exemptions consolidated text; IFRS 13 matrix pricing; IBRD funding programme currency; commercial paper tier spread; empirical duration; key-rate duration; principal components of yield changes). The owner's local library was searched first and supplied the books. Sources read, with sections and identities in their reading notes:

- Fabozzi (ed.), *The Handbook of Fixed Income Securities* (9th ed., 2021), catalogue key `s7-fabozzifixed`, chapters 1, 3-5, 7-11, 13-14, 16, 22, 31-33, 35, 37, 40, 44 and 64 at the pages listed in `notes/readings/s7-fabozzifixed.md`. Authored chapters (Ilmanen; Phoa; Bhattacharya, Fabozzi and Berliner) are cited through the Handbook.
- Hull, *Options, Futures, and Other Derivatives* (11th Global ed., 2022), chaps. 1, 4-7, 10-11, 13, 22, 25 and 34 at the pages listed in `notes/readings/s7-hulloptions.md`.
- U.S. law and rules as published by the Legal Information Institute (eCFR and sec.gov were not used because sec.gov requires an identifying user agent): 15 U.S.C. 77c (sec. 3(a)(2)-(3)) and 77ddd; 26 U.S.C. 103; 31 U.S.C. 3124; 17 CFR 230.144A, 230.415, 240.15c6-1 and 260.4a-1; 31 CFR part 356 Appendix B, whose worked examples were reproduced.
- FINRA Regulatory Notice 23-15 (5 September 2023) for the T+1 compliance date of 28 May 2024.
- Regulation (EU) 2017/1129, consolidated text of 4 December 2024, and Commission Regulation (EU) 2023/1803 (IFRS 13), both from the EU Publications Office (CELLAR) because EUR-Lex returned a bot check.
- World Bank Treasury, IBRD/IDA Factsheet (FY2026 currency composition).
- The Federal Reserve's GSW file `feds200628.csv` (to 9 October 2026), already in the repository's validation data, reduced to month-end zero yields by `gsw-month-end-extract.py`.
- CBOT Rule 18101.B (conversion factor at 6 percent), already registered.

Access limits and substitutions:
- FRED downloads failed from this environment; the commercial-paper tier spread is described from the Handbook (chap. 13) and not recomputed.
- Litterman and Scheinkman (1991) was not read directly; factor results are cited through Phoa (Handbook chap. 33) and Hull sec. 22.9, and recomputed from GSW data.
- Hull's Technical Note 24 (forward against futures prices) was not fetched; sec. 5.8 is cited and the result is checked with an original tree.
- Handbook figures date from 2019-2020; its Trust Indenture Act threshold (\$5 million) is superseded by the \$50 million of 17 CFR 260.4a-1 (2015); its chap. 64 description of SEFs as clearing counterparties is corrected against Hull.
- No curriculum text was used as a substantive source; the outlines defined scope only.

### Entries

Thirty new entries in six section files:
- `rates-credit-mortgages/bond-instruments-markets.tex`: `def:bond-features-indenture`, `def:bond-cash-flow-contingencies`, `rule:bond-issuance-legal-tax`, `def:bond-market-segments-trading`, `meth:corporate-funding-ig-hy`, `def:government-agency-supranational-funding`.
- `bond-pricing-yields.tex`: `meth:bond-price-from-yield`, `meth:matrix-pricing`, `def:bond-yield-spread-measures`, `meth:floating-money-market-yields`.
- `term-structure-returns.tex`: `meth:spot-par-forward-curves`, `meth:forward-rates-expected-returns`, `def:swap-curve-short-term-spreads`, `res:term-structure-theories`, `meth:yield-curve-factor-exposures`.
- `interest-rate-risk.tex`: `meth:bond-return-decomposition`, `meth:yield-duration-pvbp`, `meth:convexity-portfolio-duration`, `meth:curve-based-empirical-duration`.
- `volatility-options/derivative-markets-uses.tex`: `def:derivative-markets-otc-exchange`, `def:derivative-types-commitments-contingent`, `meth:option-payoff-profit`, `def:derivative-uses-risks`.
- `forward-commitment-valuation.tex`: `meth:arbitrage-replication-carry`, `meth:forward-price-value-lifecycle`, `res:forward-futures-price-difference`, `def:swaps-as-forward-strips`, `meth:equity-forward-futures-valuation`, `meth:rate-bond-forward-valuation`, `meth:swap-valuation-replication`.

The existing entries named in the brief were reviewed first: `def:fixed-income-market-structure`, `def:fixed-income-universe`, `def:interest-rate-measures`, `conv:us-rate-quotation`, `mod:forward-rates-fra`, `meth:curve-trades-carry-rolldown`, `def:interest-rate-swaps`, `mod:multi-curve-fra-swap-valuation`, `mod:duration-convexity`, `def:derivative-contracts`, `def:futures-hedge-basis`, `res:cost-of-carry-forward-price` and `mech:futures-margin-settlement`. They are linked, not repeated. Single-curve examples are labelled as such, and FRA and swap valuation with separate projection and discounting curves stays in `mod:multi-curve-fra-swap-valuation`. `def:derivative-contracts` and `res:cost-of-carry-forward-price` are mapped alongside the new entries to `objective:describe-derivative-markets` and `objective:price-by-arbitrage-and-carry`.

### Numerical evidence

Three scripts, found by `make examples`, 163 checks; one seeded synthetic series (seed 20261018) for empirical duration:
- `bond-valuation-risk/bond-valuation-checks.py` (77): 31 CFR 356 Appendix B examples (simple-stub price 99.730918; bill rates; FRN index 0.095022819 percent); Handbook Exhibit 4-4 and Illustration 4; an original bond between coupon dates (full 102.1316, clean 101.2149; simple stub 102.1249); compounding conversions; yields to call and worst; G-, I- and Z-spreads on one curve; matrix pricing; discount margins; money-market yields; duration, PVBP and convexity with repricing; a three-bond portfolio with parallel and steepening shocks; horizon returns; effective, key-rate and callable-bond measures; Handbook Exhibit 5-15; empirical duration.
- `term-structure-dynamics/term-structure-checks.py` (36): bootstrapping and repricing; inverted ordering; Ilmanen's example; rolling yield and break-even; convexity bias; swap-curve forwards and spread; Hull Table 22.9 (full 8 x 8 loadings), a two-factor hedge; principal components and volatility of GSW month-end changes (85.3, 10.7 and 2.5 percent of variance; 24.5, 28.7 and 25.5 basis points at 1, 5 and 30 years).
- `forward-swap-valuation/forward-swap-checks.py` (50): option payoffs; carry arbitrage; Hull Examples 5.1-5.4 and others; forward value over the life; dividends and index futures; a tailed futures replication with deterministic rates; a two-period tree with correlated rates; FRA; Hull Examples 6.1-6.3 and conversion factors; a bond forward; swaps by bonds and by FRAs; Hull Examples 7.2-7.3; a EUR/USD swap; equity swaps.

Findings from the checks:
- Hull's Example 6.3 subtracts \$197,000 where its own gain is \$197,500, and in the negative-rate case computes \$102,250 for \$102,500; both totals are \$502,500.
- Hull's Examples 7.2-7.3 print 0.9629 million; his own forward present values and bond values give 0.9628.
- Hull's PCA standard deviation of 25.45 matches neither the printed loadings (25.40) nor unrounded ones (25.50).
- The Handbook's convexity measure 112.38 comes from four-decimal prices; exact prices give 112.27.
- Key-rate durations explain a steepener to within its convexity (-1.7477 against -1.7302); a callable bond's effective duration depends on the shock size near the exercise boundary (6.008 at 5 basis points, 4.956 at 25).
- Many expected values typed before the first runs failed; they were recomputed by independent probes, checked by hand and replaced before the entries were finalised. A Treasury bill investment rate matches only to 5e-6 because Treasury rounds intermediate results.

### Coverage

The 65 outline items mapped to the 30 objectives (47 Level I on PDF pp. 19-24, 18 Level II on pp. 17 and 21) were each read against the finished entries. Four bullets exposed gaps that were closed before promotion: issuer and investor uses (m072:b02), interest-rate forwards' uses (m074:b02), swap price against value (m076:b02) and arbitrage for commitments against contingent claims (m077:b02). All 65 are promoted with item-specific rationales.

All 30 objectives are `covered` (editorial coverage, not mastery). Totals: 101 of 424 objectives; 125 Level I, 31 Level II and 37 Level III core items covered; 837 of 1,030 unreviewed.

### Limits

- Examples are invented or synthetic apart from the reproduced textbook and Treasury examples and the GSW data. Market sizes, spreads and funding figures are dated to their sources.
- Legal points are U.S. and EU as of 18 October 2026, from secondary publications (LII) and consolidated texts; later EU amendments were not reviewed.
- Single-curve valuation is used for teaching; collateral, funding and credit adjustments are not covered.
- Human review is outstanding.

## Correction pass on PR #24, 18 October 2026

A fixes-only pass on `88bd29e`, after an external audit with six findings. This is not study and not human review. No objective was added; the seven objectives and ten outline items whose teaching changed were reassessed and stay covered.

Sources read or re-read for this pass:
- Hull (11th Global ed.), second local copy (SHA-256 36748bb6...ba8e): sec. 6.3, pp. 162-163 (Example 6.3: SOFR plus 200 basis points on \$100 million for three months from 16 December 2021, 0.25 accrual, quote 99.990); sec. 34.4, pp. 777-778 (the next equity cash flow "is L(E - E0)/E0").
- Hull, Technical Note 19, "Valuation of an Equity Swap" (`hull-tn19`). The author's site returned HTTP 404 for the note and the index on 2026-10-18; the Internet Archive capture of 28 August 2025 was read (SHA-256 fbd0c0b8...4356). It values the swap to the equity receiver at L E/E0 - L(1 + R0 tau0)/(1 + R tau), whose equity part is L E/E0 - L/(1 + R tau).
- 31 CFR 356.12(b)(1) and 356.22 from eCFR (point-in-time XML for 15 October 2026); 87 FR 40438 (7 July 2022, effective 8 August 2022) and 91 FR 65456 (15 October 2026), both PDFs from TreasuryDirect's auction-regulations page (hashes in the reading notes); the Handbook, chap. 7, pp. 173-174.
- The New York Fed's methodology page for the SOFR Averages and Index (HTML SHA-256 1ab21c57...82d4).

Corrections:
- `meth:equity-forward-futures-valuation` (discrete-dividend replication). Borrowing only S0 - I left the share purchase unfunded by I = 2.940743. The replication now borrows the full 100, applies each 1.50 dividend to the loan when received, and owes 101.020320 at maturity, the forward price. The script's check, which compared (S0 - I)e^{rT} with itself, is replaced by a dated ledger built event by event: net cash zero at 0, 0.25 and 0.75; terminal debt 101.020320; a 0.979680 arbitrage profit against a quote of 102. The forward price and the 7.4949 value at six months are unchanged.
- `meth:swap-valuation-replication` (equity swap). Under a total-return index, one curve and payment at the reset, the next equity payment is worth N(E_t/E_0 - P(t,T_next)): 7.980133 million in the example, against 6.000 million from N(E_t/E_0 - 1). It is separated from the later payments (11.084044 million), the whole equity leg (19.064 million, unchanged) and the net values. An equity-for-SOFR version with realised overnight growth A_t = 1.019 values the next floating payment at N(A_t - P) = 3.880133 million and the swap at N(E_t/E_0 - A_t) = 4.100 million. New checks cover the payment-date and reset limits, three curves at reset and a Vasicek simulation with correlated equity (40,000 paths, seed 20261018). The simulation gives 0.079516 (se 0.000750) against the formula's 0.079800 and rejects 0.060000; the floating payment agrees within four standard errors. Hull's p. 778 expression is documented as a discrepancy, not quoted as the correction.
- `def:government-agency-supranational-funding`. Noncompetitive bids and awards are limited to \$10 million, except bids made solely to reinvest maturing securities held directly with Treasury (secs. 356.12(b)(1) and 356.22(a)), effective 8 August 2022. The Handbook's \$5 million is the earlier rule. The October 2026 amendment changes how noncompetitive customer bids are submitted, not the limit. The 35 percent rule is now stated as the competitive award cap net of the reportable long position (sec. 356.22(b)).
- `meth:floating-money-market-yields` (SOFR FRN). Simple interest on 91.25-day quarters is replaced by a dated schedule. The note is issued on 21 October 2026, with quarterly modified-following dates to 22 October 2029 (12 periods, 1,097 days). Coupons compound SOFR on business days with calendar-day weights, as in the New York Fed's methodology, with no lookback, Federal Reserve holidays as an illustrative calendar and a 75 bp margin at act/360. Each period is discounted at its projected growth plus the margin, so the note is at par when the discount margin equals the quoted margin. The discount margin at 99.40 is 96.38 bp (previously 96.4). Independent checks: the New York Fed's index example (1.00034365); daily-index ratios against the business-day product; the weights summing to the calendar days; the first coupon, 1.244827 per 100; the price round trip; and the identity P = 100 + 100(qm - dm) x margin annuity (2.8062).
- `meth:rate-bond-forward-valuation` (Hull Example 6.3). The SOFR plus 200 bp borrowing and Hull's 0.25 accrual are now stated. Loan interest and futures P&L are derived from rates, spread, notional and accrual; $25 per basis point comes from 1 million x 0.0001 x 0.25. Quote 99.990 locks the SOFR component at 0.01 percent and the all-in rate at 2.01 percent. Both scenarios (0.80 and -0.40 percent) give \$502,500, as does a sweep from 97.0 to 101.5. A 92-day act/360 loan would need 102.2 contracts. The futures' reference quarter (15 December 2021 to 16 March 2022, 91 days) differs from the loan's 90 days.
- `meth:curve-based-empirical-duration`. The unconditional claim that option-free curve and yield measures coincide is removed. They are equal on a flat curve in a common compounding, or for a single cash flow. Counterexample (continuous compounding for both): a 20-year 10 percent annual bond on z(t) = 0.01 + 0.003t prices at 152.050048 with a yield of 5.454571 percent. Durations are 10.218587 for the parallel zero-curve shift and 11.213091 for the yield shift; convexities are 146.458 and 172.057. Repricing at +100 bp gives -9.525 and -10.400 percent, and the zero shift raises the yield by 91.0 bp. Finite differences match the analytic weighted times. The flat-curve control and a 20-year zero give equal measures. A first probe gave the yield convexity as 172.052 because of round-off at a step of 1e-5; the analytic value 172.0566 was adopted.

Checks: `forward-swap-checks.py` 64 (was 50), `bond-valuation-checks.py` 89 (was 77), `term-structure-checks.py` 36 (unchanged); the batch total is 189. Coverage was reassessed for the seven objectives mapped to the corrected entries (`describe-government-funding`, `calculate-floating-money-market-yields`, `apply-curve-based-risk-measures`, `value-forward-contracts`, `value-equity-forwards-futures`, `value-rate-and-bond-forwards`, `value-swaps-by-replication`) and for the ten outline items they map to. Each still meets its operations and depth, so counts are unchanged: 101 of 424 objectives; 125 Level I, 31 Level II and 37 shared-core items covered; 837 of 1,030 unreviewed.

Limits: Hull's Technical Note 19 was read from an archived copy; his errata were not checked. The FRN calendar is approximate, and real notes' lookback and payment-delay terms are not modelled. Human review is outstanding.

## Second correction pass on PR #24, 19 October 2026

A fixes-only pass on `642e29c`, after an audit that confirmed the six corrections of the first pass and found three further issues. This is not study and not human review. No objective was added.

Sources read for this pass (search date 2026-10-19):
- IRS Publication 550 (2025) and Publication 1212 (revised December 2025), HTML editions supplied by the audit and downloaded in full (hashes in the reading notes `irs-pub-550-2025` and `irs-pub-1212-2025`). Read: Pub. 550, chap. 1, Tax-Exempt Interest and Market Discount Bonds; chap. 4, Discounted tax-exempt obligations and Tax-exempt state and local government bonds. Pub. 1212, Information for Owners of OID Debt Instruments, the constant-yield sections and Tax-Exempt Bonds and Coupons.
- 31 CFR 356.30(a) from the eCFR versioner (point-in-time text for 15 October 2026; last amended 8 August 2022): a weekend payment date is paid the next business day without additional interest.
- Hull (11th Global ed.), second local copy (SHA-256 36748bb6...ba8e), sec. 6.1, pp. 152-153: actual/actual (in period) for Treasury bonds; act/360 for money-market instruments.
- The Handbook (9th ed.), chap. 9, pp. 221-223, reread. P. 221 says "only the coupon interest is exempt from federal income taxes" and computes a discount bond's yield after an assumed capital gains tax. P. 223 states the de minimis cut-off consistently with the IRS, but defines the market discount segment as the purchase price minus the revised issue price, the reverse sign.

Corrections:
- `meth:rate-bond-forward-valuation`. The original bond forward's inputs (accrued interest 0.90 now and 0.375 at delivery, a coupon in 0.35 years, delivery in 0.50 years) did not fit a regular semiannual calendar. The example now has one schedule: a 5 percent note paying on 15 May and 15 November; spot trade on Friday 16 October 2026 for T+1 settlement on Monday 19 October; delivery on Monday 19 April 2027; term repo at 4.20 percent, simple act/360. 15 November 2026 is a Sunday, so the coupon is paid on 16 November (28 days) while accrual restarts on the 15th. Results: accrued interest 2.133152 (157/184) and 2.140884 (155/181); full spot 103.333152; coupon PV 2.491860; forward full 102.982489; quoted forward 100.841605; later value 0.395798 for a 0.40 rise with 91 days left. Independent checks: coupon dates generated back from maturity; accrual equal to the full coupon at the scheduled date and zero after it; a two-repo ledger (B0 - I to delivery, I to the coupon date) with zero net cash at settlement and on the coupon date and a debt equal to the forward full price at delivery; the exact carry identity, quoted forward - spot quote = financing 2.194107 - coupon income 2.507732 - interest on the paid coupon 0.044770 = -0.358395. Sensitivities: discounting the coupon from the Sunday moves the forward by -0.000296; reinvesting it at the 154-day term rate instead of the curve forward moves it by -0.000146.
- `rule:bond-issuance-legal-tax`. The claim that the exemption covers coupon interest only is replaced. A holder's share of OID on a qualifying tax-exempt bond is tax-exempt interest, accrued by constant yield and added to basis (issued after 3 September 1982 and acquired after 1 March 1984). Market discount is not exempt: for a purchase after 30 April 1993 it is ordinary income on disposal or redemption unless included currently, and zero below 0.25 percent times the full years to maturity. Other gains and losses are capital, against the adjusted basis. The earlier text said a discount "below the de minimis cut-off" produced ordinary income; that direction was reversed and is corrected. Example: a 20-year 3 percent bond issued at 900 (3.7128 percent semiannual yield). The adjusted issue price after five years is 918.58 by both accrual routes. A holder at issue who sells at 850 has a capital loss of 68.58. A buyer at 850 has market discount of 68.58, above the 37.50 de minimis amount, and exempt OID of 81.42; the 68.58 redemption gain is ordinary. A purchase at 900 has a discount of 18.58, below 37.50, so the gain is capital. A sale at 950 gives a capital gain of 31.42. Scope: U.S. federal income tax for individuals; it is not tax advice.

Check counts: at `642e29c` the scripts executed 90 (bond), 64 (forward and swap) and 36 (term structure), 190 in all, one more than the 89 and 189 reported in the first correction pass. The convention, stated in both scripts, is one executed `ok()` call per check. After this pass: `bond-valuation-checks.py` 94, `forward-swap-checks.py` 69, `term-structure-checks.py` 36, total 199.

Coverage: three objectives were reassessed against the corrected text and remain covered: `explain-bond-legal-tax-factors`, `value-rate-and-bond-forwards` and `value-forward-contracts`. The two outline items whose passages changed, `outline:7099c7688942:m052:b02` and `outline:0242f4b7ba07:m031:b04`, carry re-review notes. Counts are unchanged: 101 of 424 objectives; 125 Level I, 31 Level II and 37 shared-core items covered.

Limits: the holiday calendar is not modelled beyond the weekend rule. The repo curve is flat and simple, so the replication's coupon leg uses the curve forward rather than a quoted forward repo. The tax example omits state taxes, AMT, premium, stripped and short-term obligations and elections.

## Derivatives, portfolio and execution batch, 19 October 2026

Forty-five objectives in ten topics: short-term funding (1), arbitrage-free bond valuation (3), bonds with embedded options (5), option valuation (6), option strategies (4), derivative overlay strategies (4), market risk measurement (3), fixed-income portfolio management (7), equity portfolio management (7) and trade execution (5). Branch `codex/derivatives-portfolio-execution-20261019`, from `codex/fixed-income-derivatives-20261018` at `f320d35` (draft PR #24, unmerged). Source checks and numerical verification; not study and not human review.

### Source discovery

Retrieval on 2026-10-19 targeted these subjects: binomial rate-tree calibration, OAS and effective duration, capped and floored floaters, convertible valuation with default, put-call-forward parity, Black's model for caplets and swaptions, delta-hedging error, variance swaps, VaR methods and decomposition, RAROC, cash-flow matching and immunisation, Active Share, the transfer coefficient of long-short portfolios, statistical arbitrage, engagement and stewardship, effective spread and implementation shortfall, best-execution rules. The owner's local library was searched first. Sources read, with sections, copies and hashes in their reading notes:

- The Handbook of Fixed Income Securities (9th ed., 2021; `s7-fabozzifixed`): chaps. 13, 32, 36-38, 43-44, 51, 57, 60 and 62 at the pages listed in its reading note.
- Fabozzi, *Fixed Income Analysis* (2nd ed., 2007; `fixed-income-analysis-2007`), chaps. 7 and 9 (floaters, convertible minimum value). A CFA Institute Investment Series text, used like Managing Investment Portfolios; no examination curriculum volume was used.
- Hull, *Options, Futures, and Other Derivatives* (11th Global ed.; `s7-hulloptions`): chaps. 11-13, 15, 17-20, 26-27, 29 and 31.
- Hull, *Risk Management and Financial Institutions* (6th ed., 2023; `risk-management-financial-institutions-2023`): chaps. 11, 13, 15-16, 21 and 28. The owner added this edition to `reading materials/` during the batch; a 4th-edition copy read first was set aside and every locator was re-read in the 6th edition.
- Natenberg, *Option Volatility and Pricing* (2nd ed.; `s7-natenberg`): chaps. 11, 17 and 24.
- Maginn, Tuttle, Pinto and McLeavey (eds.), *Managing Investment Portfolios* (3rd ed., 2007; `managing-investment-portfolios-2007`): chaps. 6 (fixed income), 7 (equity), 9 (risk management), 10 (execution) and 11.
- Ang, *Asset Management* (`s7-ang`), chap. 14; Grinold and Kahn (`alpha-grinold`), chaps. 14 and 16, second local copy (SHA-256 5c2e3efa...).
- Cremers and Petajisto (2009), Yale working paper; Brav, Jiang, Partnoy and Thomas (2008), published version; Gatev, Goetzmann and Rouwenhorst (NBER WP 7032, 1999); Avellaneda and Lee, version of 15 June 2009 (cited by DOI because the online copy is the July 2008 draft).
- The UK Stewardship Code 2026 (FRC, effective 1 January 2026); the 2020 Code was downloaded and found superseded.
- FINRA Rule 5310 with Supplementary Material (rule page, last amended 2014); Directive 2014/65/EU (MiFID II), article 27, original Official Journal text from CELLAR; 17 CFR 240.15c3-5 and the SEC's 2010 concept release (already registered); IRS Publication 550 (2025), chap. 3.

Access limits and substitutions:
- MiFID II article 27 was read as enacted in 2014; later amendments to paragraphs 27(3) and (6) (reporting) were not reviewed.
- Clarke, de Silva and Thorley on the transfer coefficient remains paywalled; the long-short transfer coefficients are computed directly by constrained optimisation.
- No curriculum text was used as a substantive source; the outlines defined scope only.

### Entries

Forty-five new entries, one added to an existing file and the rest in nine new section files:
- `portfolio-risk-financing/money-markets.tex`: `def:short-term-funding-repo`.
- `rates-credit-mortgages/arbitrage-free-valuation.tex`: `meth:arbitrage-free-bond-valuation`, `meth:binomial-rate-tree-calibration`, `mod:term-structure-models-simulation`.
- `rates-credit-mortgages/embedded-option-bonds.tex`: `meth:callable-putable-bond-valuation`, `meth:option-adjusted-spread`, `meth:embedded-option-effective-duration`, `meth:capped-floored-floater-valuation`, `meth:convertible-bond-valuation`.
- `rates-credit-mortgages/fixed-income-portfolio-management.tex`: `def:fixed-income-mandates-return-model`, `meth:bond-leverage-taxation`, `meth:liability-matching-ladders`, `meth:immunisation-liabilities`, `meth:bond-index-exposure-benchmarks`, `meth:yield-curve-positioning`, `meth:curve-strategy-evaluation`.
- `volatility-options/option-valuation.tex`: `def:option-value-drivers`, `res:put-call-forward-parity`, `meth:one-period-binomial-valuation`, `meth:multi-period-binomial-valuation`, `meth:black-model-rates-currencies`, `meth:greeks-delta-gamma-hedging`.
- `volatility-options/option-strategies.tex`: `meth:option-replication-deltas`, `meth:covered-call-protective-put`, `meth:option-spreads-volatility-strategies`, `ex:option-strategy-selection-case`.
- `portfolio-construction-risk/derivative-overlays.tex`: `meth:forward-commitment-risk-overlays`, `meth:volatility-derivative-applications`, `meth:derivative-overlay-allocation`, `ex:endowment-derivative-overlay-case`.
- `portfolio-construction-risk/market-risk-measurement.tex`: `meth:portfolio-var-methods-decomposition`, `meth:sensitivity-scenario-risk-measures`, `meth:market-risk-limits-capital`.
- `systematic-equities/equity-portfolio-management.tex`: `def:equity-portfolio-roles-mandate`, `def:cap-weighted-factor-indexing`, `meth:index-equity-portfolio-construction`, `def:active-equity-strategies`, `meth:active-equity-strategy-creation`, `meth:active-equity-portfolio-construction`, `meth:equity-portfolio-capacity-structure`.
- `execution-trading-costs/trade-strategy-governance.tex`: `meth:execution-cost-measures`, `def:electronic-trading-environment`, `meth:trade-strategy-selection`, `def:trade-implementation-by-market`, `meth:trade-execution-evaluation-governance`.

Existing entries reviewed first and linked, not repeated, and mapped alongside the new entries where they carry part of an objective: `mod:black-scholes-merton`, `def:implied-volatility-surface`, `meth:option-payoff-profit`, `meth:curve-based-empirical-duration`, `def:vix-variance-dividend-swaps`, `meth:var-es-estimation-methods`, `def:transaction-costs`, `def:implementation-shortfall`, `def:spread-measures`, `def:execution-benchmark` and `mech:venue-competition-fragmentation`. `mod:almgren-chriss-execution` is linked from `meth:trade-strategy-selection`.

### Numerical evidence

Nine scripts, found by `make examples`, 250 checks (one executed `ok()` call per check); seeded simulations use seed 20261019:
- `short-term-funding/funding-repo-checks.py` (11): Handbook repo interest and haircut; an original 90-day funding comparison; a margin call.
- `rate-tree-embedded-options/rate-tree-checks.py` (43): calibration to the Handbook par curve; spot-curve, lattice and pathwise values; callable and putable bonds; OAS; effective, one-sided and key-rate durations and convexity; capped, floored and collared floaters; Monte Carlo, Vasicek and Ho-Lee; Hull's convertible tree (107.44).
- `option-valuation/option-valuation-checks.py` (44): value drivers by bumping; parity arbitrages; one- and two-period trees; Black, Garman-Kohlhagen, caplets and swaptions (Hull Examples 15.6, 17.2, 18.6-18.7, 29.3-29.4); Greeks against finite differences; delta-hedging simulation; gamma-theta identity; implied volatility.
- `option-strategies/option-strategy-checks.py` (27), `derivative-overlays/overlay-checks.py` (25), `market-risk-measurement/market-risk-checks.py` (26), `fixed-income-portfolio/fixed-income-portfolio-checks.py` (37, including an LP cash-flow match), `equity-portfolio-management/equity-portfolio-checks.py` (23, including SLSQP long-only and 130/30 transfer coefficients; about 55 s) and `trade-execution/trade-execution-checks.py` (14).

Findings from the checks:
- Handbook chap. 36: the call is worth 1.745 unrounded (printed 1.744), and the difference is written as 104.634 - 102.899, a transposition of 104.643; Exhibit 36-9's top year-3 rate prints 9.1987 against 9.1986.
- Hull Figures 13.7-13.8: 4.1923 and 9.4636 use p rounded to four places; unrounded values are 4.1927 and 9.4639 (American put 5.0896).
- Hull Table 19.4: at half and a quarter of a week the simulated hedging error falls by about the square root of two per halving (0.136, 0.098); Hull's 0.16 and 0.13 fall more slowly, and the cause is not stated.
- MIP chap. 6: the dollar durations 37,315 and 27,526 are averages of three positions, not the portfolio sum (111,945); the rebalancing ratio is unaffected. Cash of 1,077,796 against the book's 1,079,012 comes from rounding.
- MIP chap. 6, pp. 394-396: the forward from the interest differential approximation is 0.7880; exact parity gives 0.7885.
- Component and incremental VaR differ for a large position; they agree to first order for a small one, which is checked.
- Many expected values typed before the first runs failed; they were recomputed by independent routes, checked by hand and replaced before the entries were finalised. Circular or trivial checks (bare constants, restated inputs) were removed.

### Coverage

The 149 outline items mapped to the 45 objectives (8 Level I on PDF pp. 20 and 24; 52 Level II on pp. 18, 21-22 and 26-27; 41 shared Level III core on pp. 5-7 and 11-12; 48 Portfolio Management pathway on pp. 16-18) map to no objective outside the batch. Each was read on its page against the finished entries. Gaps found on that reading were closed before promotion: embedded-option types (m028:b01), ladder risk-return and limitations (m007:b09), implementation alternatives for immunisation (m032:b02), currency swaps and equity forwards in overlays (m017:b02-b03), a strategy summary table (m016:b06), engagement benefits and the manager's role (m006:b04) and the contrast of electronic trader types (m011:b06). All 149 are promoted with item-specific rationales.

All 45 objectives are `covered` (editorial coverage, not mastery). Totals: 146 of 424 objectives (from 101); 133 Level I, 83 Level II, 78 shared-core and 48 Portfolio Management items covered (342 of 1,030, from 193); 688 unreviewed.

### Limits

- Examples are invented or synthetic apart from the reproduced textbook examples. Funding rates, overlay prices, market costs and broker statistics are illustrative, not quotes.
- Rate trees are single-curve and lognormal at one volatility; credit, collateral and funding adjustments are not modelled. Convertibles follow Hull's default-intensity tree without call notice periods or dilution.
- Legal points are U.S., EU and U.K. as of 19 October 2026; MiFID II amendments to article 27 were not reviewed; tax points are U.S. federal and not tax advice.
- Human review is outstanding.

## Correction pass on PR #25, 19 October 2026

A fixes-only pass on `edbf4bf`, after an audit with seven findings. This is not study and not human review. No objective was added.

Sources read for this pass:
- Tesla, Inc., prospectus supplement of 2 May 2019 for the 2.00% Convertible Senior Notes due 2024 (Rule 424(b)(5), Registration No. 333-231168), read through the fetching tool because the shell download returned HTTP 403 (`tesla-2024-notes-prospectus-2019`): The Offering and the named Description of Notes sections.
- Fabozzi, *Fixed Income Analysis* (2007), chap. 7, p. 207, reread: a ladder is "approximately equal dollar amounts (market values) in each maturity sector", and Exhibit 7's 1997 Treasury ladder has roughly equal key-rate durations from year 2 on.
- Hull (11th Global ed.), chap. 15, sec. 15.12, p. 360: European options on stocks with known dividends use the stock price less the present value of the dividends.

Corrections:
- `meth:equity-portfolio-capacity-structure`. The reference portfolio rescaled D^-1 alpha/(2 lambda) by benchmark weights, which gives zero net active weight but does not maximise alpha - lambda a'Da under that constraint. The reference is now the constrained optimum a_Q = D^-1(alpha - eta 1)/(2 lambda) with eta = 1'D^-1 alpha / 1'D^-1 1. Checks: sum zero; alpha - 2 lambda D a_Q constant and equal to eta; equal to the bordered KKT solution; higher utility than the old reference; 50 random feasible perturbations all lower the objective. Transfer coefficients: long-only 0.609280 and 130/30 0.781364 (previously 0.616167 and 0.786273 against the old reference). The ratio, 1.282, still supports "about 28 percent more". The check that the reference correlates perfectly with itself was dropped.
- `meth:portfolio-var-methods-decomposition` (with the stress comparison in `meth:sensitivity-scenario-risk-measures` and the stop-loss in `meth:market-risk-limits-capital`). The parametric total subtracted the sample mean while Monte Carlo and the Euler components used zero mean: components summed to 1,729,124.91 against a reported 1,737,596.65, the gap being the mean, -8,471.74. The convention is now zero expected P&L throughout, with the historical P&L centred on its sample mean (the uncentred historical VaR is exactly 8,472 higher). Revised figures: parametric VaR 1,729,125 and ES 1.981m; historical VaR 2.084m and ES 3.225m; the backtest, with each window centred, has 8 violations in 750 days. Marginal VaRs from central bumps of the same function match the analytic values for both assets. The 2008-style scenario is compared with VaR on the same 100m equity-and-bond book (20.38m against 1.73m). The 48.4m loss covers the whole book with the short puts, and the reverse stress test covers equities and puts only. The stop-loss is 1.16 times the 100m book's VaR.
- `meth:liability-matching-ladders`. The inference that equal amounts per maturity give about equal key-rate durations and little slope exposure is removed. On annual zero rates the equal-face ladder's key-rate durations rise from 0.1304 to 0.6363 and sum to 4.686245, matching the analytic t C_t (1+z_t)^-(t+1)/V. A -50/+50 bp twist changes its value by -0.493% (-0.510% to first order). Equal market value per rung gives 0.13 to 0.63 and -0.48%. Equal dollar duration per rung gives 0.25 to 0.35 and +0.10%, but a duration of 3.14 with 32% of value in the one-year rung. Fabozzi's flat profile is attributed to his portfolio and key-rate grid.
- `meth:option-replication-deltas`. Dividends are carried through the identities: the synthetic stock costs S0 - D (S0 e^-qT with a yield), the covered call equals a short put plus a bond plus D, and the protective put a call plus a bond plus D. A discrete 1.00 dividend gives D = 0.9900 and a terminal difference of 1.0101 in every state. Spot deltas with q = 2%, T = 0.5: a fixed-strike short forward has delta -e^-qT = -0.9900498, distinct from its payoff slope of -1; one share plus one short forward keeps +0.00995; -1 + delta_call = delta_put - (1 - e^-qT). Value, cash-flow and delta identities are checked for q = 0 and q = 2%, the deltas by finite differences.
- `meth:embedded-option-effective-duration`. Convexity was divided by 2 V0 dr^2 while the compendium uses V0 dr^2 with a half in the price formula. Figures are now in the compendium convention: callable -77.149899 (Handbook half-scaled -38.574949, printed -39.1), putable 11.13, straight 16.36. Both conventions and their price formulas are stated. With the stated convention the approximation returns V+ and V- exactly at the measuring shift, and for the straight bond at +-50 bp it is within 0.02 bp of full revaluation; the half-scaled figure misses by about 1 bp.
- `meth:convertible-bond-valuation`. "No call, except on a fundamental change" is replaced by the prospectus terms: Tesla may not redeem before maturity and there is no sinking fund; holders may require repurchase at par plus accrued interest after a fundamental change; a make-whole fundamental change raises the conversion rate for converting holders up to 4.1152 shares per 1,000; conversion before 15 February 2024 depends on price, trading-price and corporate-event triggers; settlement in cash, shares or a combination at Tesla's election, with combination settlement and a 1,000 specified amount as the default. Hull's hypothetical convertible stays separate.
- `meth:option-spreads-volatility-strategies`. The figures -2.089, +0.049, +2.343, +0.606 and -1.034 were profits after the 2.141842 cost, not values. Values at the three-month expiry are 0.052704, 2.190593, 4.485236, 2.747684 and 1.108320. The premium is paid at inception and not financed; financing lowers each profit by 0.021526.

Checks after this pass: `rate-tree-checks.py` 46 (was 43), `option-strategy-checks.py` 31 (27), `market-risk-checks.py` 27 (26), `fixed-income-portfolio-checks.py` 40 (37), `equity-portfolio-checks.py` 26 (23); the others are unchanged (funding 11, option valuation 44, overlays 25, trade execution 14). The nine scripts total 264, counted as executed `ok()` calls.

Coverage: the seven objectives mapped to the corrected entries (`evaluate-equity-portfolio-structure`, `estimate-value-at-risk`, `match-liabilities-with-bonds`, `replicate-with-options`, `measure-embedded-option-risk`, `value-convertible-bonds`, `analyse-spread-and-volatility-strategies`) and the two whose text changed with them (`apply-sensitivity-scenario-measures`, `set-market-risk-limits`) were reassessed against their operations and depth and remain covered. The fifteen outline items whose passages changed carry re-review notes. Counts are unchanged: 146 of 424 objectives; 342 of 1,030 outline items.

Limits: the prospectus was read through a fetching tool, without a local copy or hash, and its make-whole table was not transcribed. The VaR convention ignores the drift, which matters little at one day but would not over longer horizons. Human review is outstanding.

## Macro, allocation and currency batch, 19 October 2026

Forty-five objectives in eleven topics: business cycles (2), fiscal policy (1), monetary policy (2), geopolitics and trade (3), exchange-rate mechanics (4), exchange-rate determination (5), economic growth (4), macro asset valuation (3), capital market expectations (6), strategic asset allocation (11) and currency management (4). Branch `codex/macro-allocation-currency-20261019`, from `codex/derivatives-portfolio-execution-20261019` at `bea4f8e` (draft PR #25 after its correction pass). Source checks and numerical verification; not study and not human review.

### Source discovery

Retrieval on 2026-10-19 targeted these subjects: business-cycle phases and dating, credit and financial cycles, leading indicators, fiscal multipliers and debt dynamics, monetary transmission and the neutral rate, geopolitical risk measurement and fragmentation, tariff welfare, FX quotes, cross and forward rates, triangular arbitrage, forward valuation, parity conditions and fair value, carry, balance of payments and crises, growth accounting and convergence, the consumption-based real rate, breakevens and credit spreads over the cycle, capital market expectations, strategic asset allocation and currency hedging. The owner's local library was searched first. Sources read, with sections, copies and hashes in their reading notes:

- Piros and Pinto (eds.), *Economics for Investment Decision Makers* (CFA Institute Investment Series, 2013; `economics-investment-decision-makers-2013`), chaps. 6-11.
- *Portfolio Management in Practice, Volume 1* (CFA Institute Investment Series, 2020; `portfolio-management-in-practice-v1-2020`), chaps. 3-8.
- Mankiw, *Macroeconomics* (10th ed.; `macroeconomics-2019`), chap. 9, secs. 9-2 to 9-4.
- Cochrane, *Asset Pricing* (rev. ed., 2005; `s6-cochrane`), sec. 1.4.
- Ang, *Asset Management* (2014; `s7-ang`), chaps. 4, 6, 7 and 9.
- Jordà, Schularick and Taylor, NBER WP 17621 (rev. 2012); Caldara and Iacoviello, *AER* 2022; Aiyar, Ilyina et al., IMF SDN/2023/001; Campbell, Serfaty-de Medeiros and Viceira, NBER WP 13088 (rev. 2009); Menkhoff, Sarno, Schmeling and Schrimpf (accepted version, already held locally) for carry and FX volatility.
- Already registered and reused: the NBER dating page, Estrella and Trubin (2006) on the yield curve, the BIS Triennial Survey 2025.

Access limits and substitutions:
- BIS Working Paper 380 (Drehmann, Borio and Tsatsaronis) returned a bot-check page to scripted downloads; only its abstract was read and it is not cited. Jordà, Schularick and Taylor supply the credit-cycle evidence instead.
- The IMF site refused the SDN download; a copy without annexes hosted by Florida State University was read. The Harvard copy of the published Campbell et al. article returned HTTP 403; the NBER working paper was read.
- Two Investment Series books are substantive sources here, as Managing Investment Portfolios was in earlier batches; non-CFA sources (Mankiw, Cochrane, Ang, the papers and the IMF note) supply theory and evidence. The outlines defined scope only.

### Entries

Forty-five new entries in eight new section files:
- `multi-asset-systematic-macro/business-cycles-policy.tex`: `def:business-credit-cycles`, `meth:business-cycle-indicators`, `def:fiscal-policy-tools-stance`, `def:geopolitics-institutions-tools`, `meth:geopolitical-risk-assessment`, `meth:trade-benefits-restrictions-blocs`.
- `rates-credit-mortgages/monetary-fiscal-policy.tex`: `def:monetary-policy-transmission-regimes`, `meth:monetary-fiscal-policy-mix`.
- `currency-markets/fx-mechanics-parity.tex`: `def:fx-market-real-exchange-rates`, `meth:cross-forward-rates`, `meth:fx-bid-offer-triangular-arbitrage`, `meth:currency-forward-mark-to-market`, `def:exchange-rate-regimes-capital-flows`, `res:international-parity-conditions`, `meth:exchange-rate-forecasting-fair-value`, `meth:carry-trade-uip`, `def:flows-policy-exchange-rates`.
- `multi-asset-systematic-macro/economic-growth.tex`: `def:growth-determinants-factors`, `meth:potential-gdp-growth-accounting`, `mod:growth-theories-convergence`, `def:growth-policies-technology-trade`.
- `multi-asset-systematic-macro/macro-asset-valuation.tex`: `res:economy-discount-rates-cash-flows`, `meth:cycle-rates-breakevens-spreads`, `meth:cycle-equities-property`.
- `multi-asset-systematic-macro/capital-market-expectations.tex`: `meth:cme-framework-forecasting`, `meth:growth-shocks-long-run-expectations`, `meth:cycle-policy-curve-expectations`, `meth:asset-class-return-forecasts`, `meth:fx-volatility-forecasts`, `ex:global-portfolio-macro-rebalancing`.
- `multi-asset-systematic-macro/strategic-asset-allocation.tex`: `def:investment-governance-allocation`, `meth:economic-balance-sheet-allocation`, `def:allocation-approaches-risk`, `meth:asset-class-factor-specification`, `meth:asset-only-allocation-mvo`, `meth:allocation-implementation-rebalancing`, `meth:allocation-robustness-liquidity-risk-budget`, `meth:liability-relative-allocation`, `meth:goals-based-allocation-heuristics`, `meth:allocation-constraints-taxes-revision`, `meth:tactical-shifts-behavioural-biases`.
- `currency-markets/currency-management.tex`: `meth:currency-portfolio-effects`, `meth:currency-hedging-programme`, `meth:active-currency-strategies`, `meth:currency-hedge-cost-reduction`.

Existing entries reviewed first and linked, not repeated; those carrying part of an objective are mapped alongside the new entries: `def:macroeconomic-indicators`, `def:central-bank-policy-framework`, `mod:taylor-rule`, `def:fx-market-structure`, `def:currency-regimes-intervention`, `ev:cip-deviations`, `mod:fx-carry-trade`, `mod:mean-variance-portfolio-optimisation`, `mod:black-litterman` and `mod:minimum-variance-hedge-ratio`. `def:macro-regime-asset-map` and `meth:asset-class-portfolio-construction` are cross-referenced.

### Numerical evidence

Seven scripts, found by `make examples`, 140 checks (one executed `ok()` call per check); seeded simulations use seed 20261019: `macro-policy-trade-checks.py` (23), `fx-checks.py` (27), `growth-checks.py` (19), `macro-valuation-checks.py` (13), `cme-checks.py` (18), `saa-checks.py` (25), `currency-management-checks.py` (15). Two governance and geopolitics entries are descriptive and have no numerical check.

Findings from the checks:
- EIDM Exhibit 11-3: the components sum to the 10.82% return only if the EPS/GDP entry is -0.12 (the text layer shows 0.12; the text's combined 0.20 confirms the sign).
- EIDM Exhibit 9-9: the printed working "0.65 - 4" is a slip for 0.65 - 1; the result 0.09 is right.
- PMiP Example 7: the guideline horizon forecasts (-6%, -18%, 4.8% and about 8%) converge faster than an exact Markov chain with the stated 39- and 20-month spells, which gives -5.4%, -13.6%, 0.8% and 4.2% a year.
- PMiP Exhibit 5 maps policy mixes to the level of rates, not the slope; an earlier draft of the CME entry had it wrong and was corrected before promotion.
- PMiP pp. 274-275: the Smiths' required capital of 6,671 and 2,679 thousand implies unrounded rates near 4.13% and 6.81%; the table's 4.1% and 6.8% give 6,691 and 2,683.
- The Solow model's own convergence speed (5.5% a year at alpha = 1/3, 3.5% at 2/3) exceeds the roughly 2% Mankiw reports among similar economies.
- Many expected values typed before the first runs failed (option premia, surplus volatilities, simulated success rates, large-country tariff welfare); they were recomputed and replaced before the entries were finalised. Two checks that only restated inputs were rewritten to test outcomes.

### Coverage

The 118 outline items mapped to the 45 objectives (25 Level I on PDF pp. 5-7, 36 Level II on pp. 5-6 and 25, 57 shared Level III core on pp. 1-3 and 12) map to no objective outside the batch. Each was read on its page against the finished entries; all are promoted with item-specific rationales.

All 45 objectives are `covered` (editorial coverage, not mastery). Totals: 191 of 424 objectives (from 146); 158 Level I, 119 Level II, 135 shared-core and 48 Portfolio Management items covered (460 of 1,030, from 342); 570 unreviewed.

### Limits

- Macro data quoted from the sources are dated (EIDM to 2010-2012; Ang and Piazzesi's sample; PMiP's 2018-2019 figures); original examples are invented or simulated.
- Policy and geopolitical descriptions are frameworks, not forecasts; scenario probabilities are subjective.
- Several papers were read only at abstract or introduction level (Jordà et al., Campbell et al., MSSS, the IMF note beyond its summary and sec. II); their detailed results are not relied on.
- Human review is outstanding.

## Correction pass on PR #26, 19 October 2026

Verified clean `bcc3551` and live draft/open PR stack before changes. This record
supersedes the earlier source-error interpretation of PMiP Example7 and the
misidentification of Cochrane's matching-hash 2000 manuscript as the2005 edition.
No new objective is counted for these corrections.

- `meth:asset-class-return-forecasts`: Cap-rate change is relative (6%), first order 1.5%; forward-NOI cash ledger gives 1.6981%, stable cap control 7.5%. PMiP pp.118-119/PDF146-147 reread, including reinvestment caveat.
- `meth:currency-hedge-cost-reduction`: USD-valued exposure ratio 0.935 converted at USD/NZD 0.60 and USD/AUD 0.66 to 0.85 AUD per NZD; USD P&L and currency-unit scaling checked; forward delta assumptions explicit. PMiP pp.424-426 reread.
- `meth:geopolitical-risk-assessment`: Physical scenarios separated from state prices and pricing probabilities; cash-funded premium, tail-loss/premium constraints and negative-expected-P&L insurance counterexample. Cochrane actual copy is 12 June 2000 manuscript, secs.1.2 and 3.1-3.2, pp.16-17 and54-56.
- `mod:growth-theories-convergence`: Raw K/L grows on the balanced path; K/(L A^(1/(1-alpha))) converges. Aggregate-capital ledger and zero-technology control. EIDM pp.665-669 reread (Exhibit11-13 explicitly a snapshot).
- `meth:cycle-equities-property`: E0, E1 and D1 explicit; trailing 21/26.25/15 and forward 20/25/14.2857 reconciled to independent dividend PV sums.
- `meth:asset-only-allocation-mvo`: Cedar client case covers objectives, capacity/willingness, liquidity/tax/horizon/concentration constraints, market proxy and competing mixes; feasible 30/15/45/10 recommendation justified by declared mean-variance utility and stress limits. USD ledger and adverse forecast implication. PMiP pp.220-223 reread.
- `meth:goals-based-allocation-heuristics`: Lins USD1m available wealth; dated education and home goals, success requirements, explicit module weights, capital budgets, aggregate assets and cash surplus reconciled. Same-client60/40 comparison and USD900k infeasibility resolution. Exact lognormal single-payment example distinguished from book approximation. PMiP pp.268-275,279-282 reread.
- `meth:cycle-policy-curve-expectations`: PMiP p.65/PDF93 explicitly specifies continuously compounded monthly returns. Restored expected cumulative/annualised log labels, homogeneous transition timing, geometric equivalents and separate expected wealth with added deterministic-state assumption; enumeration confirms results. Guideline estimates are qualitative, not proven source errors.
- `def:fiscal-policy-tools-stance`: Monetary accommodation distinguished from offset; EIDM pp.386-387,393-394 reread. Debt scenario uses nominal rate3%, nominal growth5%, zero primary balance.
- `meth:active-currency-strategies`: Rising risk aversion means reducing carry and adding long-volatility hedges within premium budget.
- `ex:global-portfolio-macro-rebalancing`: Weights30/30/20/20 to38/24/18/20: equity A +8, equity B -6, bond A -2. Budget checked.

All 11 affected objectives and 35 mapped outline items were reassessed against
all operations and depth. Actual outline pages reread: Level I p.6; Level II
pp.6,25; shared core pp.1-3,12. The two missing decision applications are now
present; baseline coverage remains191/424 objectives and460/1,030 items.

Six changed scripts execute151 checks: CME28, growth22, currency21, macro
valuation16, policy/trade25, allocation39. A check is one executed ok() call,
including each loop iteration. These are numerical checks, separate from unit
tests, scripts, entries, objectives and outline items. Focused checks passed.
The first allocation calculation exposed an incorrect candidate utility claim;
the final recommendation selects the actual higher-utility feasible candidate.

Sources: exact reread locators are in the reading notes. Optional macro papers
and annexes have not been supplied or newly reviewed. Earlier abstract-only
limitations remain; no new empirical claim relies on those papers. Human review
and learner mastery remain outstanding. Full validation and rendering follow.

Validation completed: `make check` passed lock/lint/format, both structural
validators,36 tests plus3 subtests,84 numerical scripts and all8 outline hashes.
Its PDF step initially failed because the sandbox denied the default font cache;
with TEXMFVAR/TEXMFCACHE set to a writable temporary directory, a forced LuaLaTeX
rebuild passed (287 pages, no overfull boxes or undefined references). Existing
underfull/page-destination warnings are not treated as new errors. `make pre-commit`
passed all hooks. PDF pages96-110 and118-119 were rendered and inspected, covering
all corrections and both complete client cases; no clipping or overlap observed.

## Macro source-correction pass, 20 October 2026

Starting state verified before edits: `main` at `0b78e4d`, clean. PRs #24, #25 and #26
are closed, and their corrected stack, through `893622d`, was merged into `main` by PR #28
on 20 October 2026. The accounting expansion `644f5d0` was reverted by `4196920` before
that merge, so it is absent from `main`. PR #26's branch therefore cannot receive this pass;
it runs on `codex/macro-source-corrections-20261020` from `main`.

**Re-audit of the eight PR #26 findings.** Each correction in the record above was
recomputed by an independent scratch script, not by the repository scripts:
- cap rate: forward-NOI cash ledger 1.6981 percent and stable-cap control 7.5 percent;
- cross hedge: 850,000 AUD and USD P&L -15,120;
- Solow: raw K/L grows at 2.2584 percent, while K/(L A^(1/(1-alpha))) reaches the closed-form 3.7534;
- P/E: trailing 21, 26.25 and 15 against forward 20, 25 and 14.2857, with Gordon prices 210, 262.5 and 150;
- Markov: cumulative log returns -5.415, -13.625, 4.0 and 42.335 percent, confirmed by 200,000 simulated paths (-13.59 percent at 12 months);
- Cedar: all four mixes' mean, volatility, stress and utility;
- Lins: all budgets, the 60/40 comparison, the reduced home goal and a simulated 80.1 percent home success;
- the debt ratio 58.857 and the rebalancing weights.

The pricing-probability and fiscal-multiplier wording, as now on `main`, was reread.
All match. One residual error was found: the Cedar text's normal-model fifth
percentile "about -8.2%" is -8.13% (5.075 - 1.645 x 8.031). It was not computed by any
check.

- `meth:asset-only-allocation-mvo`: now "about -8.1%". `saa-checks.py` part 10 adds one check: the closed form, and the empirical quantile of 400,000 simulated multivariate-normal asset returns (-8.1353%). That script now executes 40 checks, up from 39. No allocation decision changes.
- `def:business-credit-cycles`: BIS Working Paper 380 (Drehmann, Borio and Tsatsaronis, June 2012) was supplied by the owner. Its abstract was read in the earlier batch, but it was not cited. Now read:
  - introduction, printed pp. 1-3;
  - sec. 3.3 with Table 8, pp. 16-17;
  - sec. 4 with Graph 3 and Table 9, pp. 18-20.

  One paragraph cites it for:
  - the medium-term financial cycle (credit, credit/GDP, house prices; seven countries, 1960-2011);
  - average duration of about 16 years (nearly 20 after 1998, 11 before);
  - domestic crises at or near its peaks;
  - average recession depths of -3.4 against -2.2 percent by financial-cycle phase.

  The authors' "indicative" caveat is kept. New key `financial-cycle-medium-term-2012`, with a reading note. The Jordà-Schularick-Taylor note's retrieval remark was updated.
- `imf-sdn-2023-001`: the owner supplied the IMF-published PDF (15 January 2023) and its Online Annexes. The Executive Summary is identical, after whitespace normalisation, to the earlier copy without annexes, so the entry's p. 4 locator is unchanged. The reading note's "p. 9" for export bans and national-security restrictions was a locator error: both copies print that passage on p. 10. Box Figure 1.1 (p. 15) and its comparability caveat were added to the note. The annexes were inspected at heading level only and are not relied on. The source description in `sources.tex` now names the official copy.

Coverage is unchanged: 191/424 objectives and 460/1,030 outline items. The affected
objectives (`describe-business-credit-cycles`, `recommend-asset-allocation`) were
reassessed and remain covered at their stated depth. No new objective is counted.

## Accounting and statement-analysis batch, 20 October 2026

**Starting state.** Branch `codex/accounting-statement-analysis-20261020` from
`codex/macro-source-corrections-20261020` at `6157abb` (draft PR #29 to `main`). The
earlier attempt at this batch (`644f5d0`) was reverted by `4196920` before PR #28 merged.
It was not reused: its main secondary source was the answer section of a workbook. All
45 objectives were `missing`. Their 72 outline items map to no objective outside the batch,
and every declared prerequisite topic is covered or in the batch.

**Scope (45, exactly the Section 23 list).**
- financial-reporting-framework: 3
- income-statement-analysis: 5
- balance-sheet-analysis: 3
- cash-flow-analysis: 2 (interpret, free cash flow; the three covered objectives are excluded)
- inventory-accounting: 3
- long-lived-asset-accounting: 2
- leases-employee-compensation: 6
- income-tax-accounting: 3
- financial-reporting-quality: 7
- ratio-analysis: 4
- financial-statement-modelling: 4
- integrated-statement-analysis: 3

**Outline pages read.** Level I topic outline PDF pp. 11-14 (modules on introduction,
income statements, balance sheets, cash flows II, inventories, long-term assets, liabilities
and equity, income taxes, reporting quality, analysis techniques, modelling). Level II
PDF pp. 7-9 (employee compensation, evaluating quality of financial reports, integration of
techniques). Each of the 72 items has an item-specific rationale in `outline-crosswalk.json`.

**Sources read** (versions, sections and key results in the reading notes):
- Primary IFRS: the original EU text of Regulation 2023/1803 for IAS 1, 2, 7, 8, 12, 16, 19, 23, 33, 36 and 38 and IFRS 2, 3, 5, 7, 9, 15 and 16, by paragraph.
- Later EU amending regulations: 2023/2822 (IAS 1 classification and covenants, applied from 2024), 2023/2468 (IAS 12 Pillar Two) and 2024/1317 (supplier finance, from 2024).
- IFRS 18 in Regulation 2026/338: categories, subtotals, expense disclosure, management-defined performance measures, B50-B55 and transition C1-C8.
- FASB: 18 Accounting Standards Updates (summaries and effective dates) and 8 pre-Codification Statements (paragraphs cited). The current Codification was not consulted.
- SEC: Regulation G, Regulation S-K Items 10(e), 105, 303 and 308 (LII display of 17 CFR, retrieved 2026-10-20), and Release 33-8879 (73 FR 986) on IFRS filings by foreign private issuers.
- EU: Regulation 537/2014, Art. 10 (audit report).
- Books: Subramanyam and Wild, *Financial Statement Analysis*, 10th ed. (2009), read on the pages cited; Damodaran, *Investment Valuation*, 3rd ed. (2012), pp. 2-3, 282-284, 307-313, 364, 380-381, 571-576.
- Articles: Porter (2008), HBR reprint pp. 2-10; Sloan (1996), pp. 289-300 incl. Tables 1-3; Kahneman (2011), chap. 23; Barberis and Thaler (pp. 12-15, already recorded).
- The 2024 CFA Program curriculum volumes in the owner's library were deliberately not used, consistent with earlier batches (Section 3.4 prefers non-curriculum sources).

**Access limits and unread sources.**
- PCAOB AS 3101 was refused (HTTP 403 and a bot check), so the EU audit regulation is cited instead.
- SEC.gov rate-limits scripted requests without a declared contact address; the owner's email was not sent, and the LII copies of the CFR were used.
- Beneish (1999) is paywalled and was not read; no manipulation-model variables or weights are given.
- Richardson, Tuna and Wysocki (2010), Penman, and Nissim and Penman (2001) were not read. The last is named only as the textbook's source for an 84 percent average.
- The textbook's research summaries (inventory signals, LIFO reserve and value, cash-flow usefulness) are attributed to the textbook.

**Disagreements and supersessions recorded.** The 2009 textbook predates several standards. In each case the entries cite the current standard and note the change:
- the SEC's 2008 acceptance of IFRS without reconciliation (the textbook says reconciliation is required);
- ASU 2015-11 lower of cost and NRV (the textbook describes lower of cost or market);
- ASU 2015-01, which removed extraordinary items;
- Topic 842 leases (the textbook capitalises operating leases analytically);
- IFRS 15 and Topic 606;
- ASU 2017-04 goodwill;
- ASU 2017-07 pension presentation.

Issued against effective is stated for IFRS 18 (2027), ASU 2024-03 (annual periods after 15 December 2026), ASU 2025-06 (after 15 December 2027) and ASU 2023-09 (public business entities from 2025).

**Numerical evidence.** `notes/artefacts/financial-statement-analysis/statement-analysis-checks.py`,
21 parts, 111 checks (one check is one executed `ok()` call). These are checks, not tests or
objectives. The independent routes are:
- a double-entry ledger whose direct-method cash flow is summed from tagged postings and compared with an indirect derivation from statements;
- equity roll-forwards;
- brute-force subset search for the most dilutive EPS;
- unit-layer inventory simulation;
- annuity schedules against closed forms;
- Black-Scholes-Merton against Monte Carlo;
- a forecast whose balance sheet must balance with cash from the cash-flow statement;
- an explicit FCFF bridge;
- simulation for interval coverage and persistence;
- currency-unit invariance.

The checks exposed errors during development, all corrected before the text was finalised:
- a reversed cumulative probability in the variable-consideration constraint;
- sign errors in accumulated depreciation and the remeasurement reserve, which the forecast balance-sheet identity caught;
- inventory omitting absorbed depreciation;
- acquisition revenue double-counted and its amortisation not added back, caught by a 2-per-year imbalance;
- an expected sign for the accrual measure under supplier finance (the measured accruals fall, which became the teaching point);
- an expected leverage ranking in the comparability case;
- three text figures (the FCFF bridge, the cash-flow adequacy ratio, and the covenant-breach current ratio 0.94).

Tautological checks were removed before counting.

**Coverage.** All 45 objectives were reassessed operation by operation at their stated depth
and moved to `covered`, mapped to 46 entries (45 objective entries plus the shared case
`ex:harbour-tools-statements`). The decision objective
(`objective:apply-integrated-analysis-framework`) has constraints, three alternatives, base and
downside scenarios and a justified recommendation with monitoring. Editorial coverage moves
from 191/424 to 236/424 objectives, and outline items from 460/1,030 to 532/1,030 (Level I
207, Level II 142, Portfolio Management 48, shared core 135). This is editorial coverage, not
learner mastery or independent human review.

**Limits.** Harbour, Kestrel and Ridgeline are hypothetical; simulations are synthetic and
illustrate methods, not evidence. Pass-through rates and credit-policy thresholds are
scenario inputs. The Codification paragraphs that replaced the cited FASB Statements are an
open question in the pathway note.

## Accounting correction pass, 20 October 2026

**Starting state.** Verified before edits: PR #29 (draft, `codex/macro-source-corrections-20261020`,
head `6157abb`, base `main`) and PR #30 (draft, `codex/accounting-statement-analysis-20261020`,
head `4a9edbc`, stacked on #29) open; `main` at `0b78e4d` is an ancestor of `6157abb`, which is
an ancestor of `4a9edbc`; the checkout was clean at `4a9edbc`; coverage 236/424 objectives and
532/1,030 items. The reverted attempt `644f5d0` was not used. These corrections are commits on
PR #30's branch. They count toward no new objective; the record of the batch above is kept as
history, and the statements below supersede it where they differ.

**Findings reproduced first.** Each audit claim was recomputed before changes:
- FCFF 48.54 omits the 2025 right-of-use addition of 30 (18.54 with it), and the 2026-2028
  additions of 25 have present value 64.4274 at 8 percent;
- `forecast()` added share-based expense back to CFO and part 17 used that CFO in valuation with no
  deduction; the three add-backs (9.45, 9.9225, 10.418625) have present value 25.5276;
- opening development / 5 leaves 0.8^5 = 32.768 percent of an isolated balance after five years;
  the acquired 20, pooled with development and also charged `acquisition["amort"]`, was charged
  2, 5.6 and 4.48 in 2026-2028; acquired PP&E was added at the end of 2026 and never had its own
  depreciation, while the acquired business earned a full 2026 of EBITDA although the decision
  was dated 1 March 2026;
- `tv_value(nopat_2028 (1 + g), ...) / (1 + g)` is NOPAT_2028/WACC by construction, so the check
  could not fail and its label TV/NOPAT_2028 described a quantity it did not compute.

**Sources read for the corrections.**
- Damodaran, *Leases, Debt and Value* (April 2009, NYU Stern), PDF pp. 25-32: lease additions as
  capital expenditure; FCFE unchanged; lease debt in the bridge. Written for US operating leases;
  the reinvestment logic is applied to IFRS 16 right-of-use additions.
- Damodaran, *A Primer on Free Cash Flows* (slides, October 2022), slide 14 (text slides 3, 9, 16,
  21, 24 also read; chart slides not relied on).
- Damodaran, *Investment Valuation*, 3rd ed., pp. 445-449: options valued as claims at the
  estimated value per share with iteration; future grants as an expense.
- IAS 7 paras. 43-44 (non-cash transactions), IAS 38 para. 97 and IAS 16 para. 55 (charge from
  availability for use), IFRS 9 paras. 4.1.4, 5.7.5-5.7.6, B5.7.1 and the Appendix A definition
  of held for trading, all in the EU 2023/1803 Official Journal text already held locally.
- SEC Division of Corporation Finance C&DIs on non-GAAP measures (last updated 13 December 2022),
  Questions 102.03 (17 May 2016) and 100.01 (13 December 2022), read on the SEC website; a
  scripted download returned an access page, so no local copy is kept and no contact address was
  sent.

**Corrections.**
1. *Leases in valuation* (`meth:free-cash-flow-coverage`, `meth:forecast-horizon-steady-state`).
   Statement presentation and valuation are separated. The non-cash lease inception stays out of
   the statutory cash-flow statement. Valuation FCFF deducts right-of-use additions (2025: 48.54 to
   18.54), lease liabilities are claims, and FCFE is unchanged (28.04; forecast years checked).
   A lease-versus-buy-with-debt check shows the superseded convention created 25/1.08 = 23.15 of
   artificial value for one vintage; the corrected convention creates none.
2. *Share-based pay* (`meth:share-based-compensation-modelling`, FCFF and horizon entries).
   Statutory CFO keeps the add-back. Valuation deducts the expense for future grants (non-deductible,
   so no tax effect), keeps it in terminal NOPAT (EBIT - t(EBIT + SBC)), deducts the 5m vested
   options as BSM claims at the iterated value per share (9.28; 8.49 a share; treasury stock 8.56),
   and does not deduct unvested awards whose cost is in the forecast.
3. *Asset schedules* (`ex:harbour-pro-forma-model`, `ex:integrated-credit-decision`). The opening
   development balance of 60 is amortised straight-line over 2026-2030; each year's development is
   available for use on 1 January of the next year and amortised over five years; acquired
   intangibles (ten years) and acquired PP&E (five years) have their own schedules from completion
   on 1 April 2026 (nine months in 2026), are excluded from the development pool and the organic
   depreciation base, and are deductible as an asset purchase. Capital expenditure is 8.5 percent
   of total revenue, as the entry always stated. Base 2026 is unchanged; 2027-2028 profit falls to
   75.47 and 80.36 because development amortisation rises to 16.58 and 21.42. Covenant EBITDA is
   pro forma for the acquisition. Re-running all six original lender scenarios: A and C fail as
   before; B now fails the downside on liquidity alone (1.84 undrawn against 10). A fourth
   alternative, D (lock-up tested on pro forma leverage at completion, 1.85x, so no 2026 dividend),
   passes both scenarios with 19.02 undrawn and is now recommended; a 170 facility, a 1 July
   completion and a capital-expenditure cut are shown as sensitivities.
4. *IFRS 9 equity election* (`meth:financial-instruments-liabilities`): timing, instrument-by-
   instrument basis, both exclusions, and an eligible stake against an ineligible trading holding.
5. *SEC non-GAAP restructuring* (`meth:earnings-management-presentation`): the two-year condition
   restricts the description; adjustment remains possible unless misleading, and excluding normal,
   recurring cash operating expenses may mislead.
6. *Terminal-value check* (`meth:forecast-horizon-steady-state`): NOPAT_2029 fixed gives
   TV = NOPAT_2029/WACC (1,202.48) for g = 0, 2, 4 percent; NOPAT_2028 fixed gives 1,173.16,
   1,196.62 and 1,220.08, each 1,173.16 net of the 2028 reinvestment the growth requires.
   Enterprise value is now 1,218.45 (superseding 1,376.78); equity 855.59.

**Numerical evidence.** `statement-analysis-checks.py` now executes 138 checks (from 111): new
checks detect each audit error (the 32.768 percent residual, the 2/5.6/4.48 pooling, the omitted
lease and share-based PVs, the artificial lease value, both terminal quantities) and verify the
replacements by independent routes (vintage sums against the balance; CFO against NOPAT routes for
valuation FCFF; FCFE as dividends plus change in cash under both lease presentations; an option
fixed point with bounds). The former "only B passes" check was replaced by the recomputed verdict.

**Coverage.** The eight affected objectives (FCFF and coverage, share-based and pension modelling,
pro forma model, forecast horizon, integrated decision, financial instruments, earnings management)
were reassessed at their stated depth and remain covered; their 11 outline items were reread on
their pages (Level I PDF pp. 11-14, Level II PDF pp. 7-9) and their rationales record the
revalidation. Coverage unchanged: 236/424 objectives and 532/1,030 items.

**Limits.** The after-tax pension deficit follows the credit-analysis convention; under Harbour's
simplified tax rule the pre-tax deficit would lower equity by 12.04, as the entry states. WACC,
RONIC, option inputs and credit-policy thresholds are illustrative inputs.

## Corporate-finance and equity-valuation batch, 20 October 2026

**Starting state.** Branch `codex/corporate-equity-valuation-20261020` from the corrected
PR #30 head `1f51fcf` (`codex/accounting-statement-analysis-20261020`). All 45 objectives
were `missing`, with no entries or candidates; their 123 outline items map to no objective
outside the batch. Coverage before: 236/424 objectives, 532/1,030 outline items.

**Scope (45).**
- corporate-ownership-governance: 5
- business-models: 1
- working-capital-liquidity: 2
- capital-investment-decisions: 2
- capital-structure-cost-of-capital: 4
- payout-policy: 4
- equity-securities-markets: 4
- equity-valuation-foundations: 6
- industry-company-analysis: 2
- dividend-discount-models: 6
- market-multiples-valuation: 7
- corporate-restructuring: 2

Implemented in prerequisite order: governance, business models, working capital, capital
investment, capital structure, payout, equity securities, valuation foundations, industry,
dividend models, multiples, and restructuring last, after multiples.

**Outline pages read.** Level I topic outline (`7099c7688942`) PDF pp. 9-10 and 15-17;
Level II (`0242f4b7ba07`) PDF pp. 11-15. Each of the 123 items has an item-specific
rationale in `outline-crosswalk.json`.

**Sources read** (versions, sections and key results in the reading notes):
- Books: Damodaran, *Applied Corporate Finance*, 4th ed. (2014), chaps. 1-2, 4-11 and pp. 556-557; *Investment Valuation*, 3rd ed. (2012), pp. 1-25, 75, 124-132, 285-289, 323-348, 453-517, 542-545, 596-597, 702-728; *Narrative and Numbers* (2017), pp. 83-85; Subramanyam and Wild (2009), pp. 535-544; OpenStax *Principles of Finance*, 2nd ed., secs. 2.1 and 19.1-19.5.
- Articles: Modigliani and Miller (1958), pp. 268-273; Osterwalder, Pigneur and Tucci (2005 manuscript); Rochet and Tirole (2005 manuscript); Berg, Kölbel and Rigobon (2022); Lang and Stulz (1993 working paper); Cooper and Lambertides (2023); Porter (2008), pp. 12-15 added to the pages already read.
- Governance and law: G20/OECD Principles (2023); OECD *Owners of the World's Listed Companies* (2019); EU Shareholder Rights Directive II (2017/828); Delaware General Corporation Law secs. 151, 170, 212, 214, 216; 15 U.S.C. 78l(g); IRS business-structure pages.
- Standards and rules: simplified ESRS (Delegated Regulation 2026/1563), ESRS 1; IAS 1 para. 25 and IFRS 13 paras. 2, 9 and 57 (EU 2023/1803); SEC Rules 10b-18 and 13e-4(f); FINRA Rule 11140 as amended in 2024; US Merger Guidelines (2023); GICS methodology (2023); FTSE Russell free-float rules v3.6 (October 2026); CIPD PESTLE factsheet (2026).
- Curriculum volumes and answer workbooks were not used; the outlines were used only to map items.

**Access limits and unread sources.**
- The ISSB's IFRS S1 and S2 require registration and were not read; ESG materiality follows ESRS.
- The OECD site refused the ownership report; a reproduction in Columbia Business School course materials was read and is identified as such.
- Berg et al.'s PDF download was refused; the open-access Oxford Academic HTML was read, cited by section.
- Rev. Rul. 59-60 (US fair market value) and Nasdaq Rule 5550 (minimum bid price) were not read; fair market value is described as Interpretation, and reverse splits without listing-rule detail.
- Primary studies summarised in the books (Gompers-Ishii-Metrick, Lintner, Jensen-Ruback, Myers-Majluf, Smith 1986, KPMG and McKinsey acquisition studies) were not read; they are attributed to Damodaran.
- SEC.gov pages were not fetched by script; LII renderings of the CFR were used, and the owner's email was not sent anywhere.

**Conventions protected by the examples.**
- Project cash flows are incremental and after tax; sunk costs excluded, opportunity costs and cannibalisation included; financing not deducted when discounting at the WACC (`meth:capital-project-evaluation`).
- NPV ranks mutually exclusive projects; IRR conflicts and multiple IRRs are shown.
- WACC uses market-value weights (`meth:wacc-calculation`).
- Leverage effects follow MM with and without taxes and a trade-off curve; costs of debt and equity rise with leverage.
- Dividends, stock dividends, splits and buybacks are reconciled to value per share, EPS and BVPS.
- Trailing and leading P/E and PVGO are reconciled; multistage terminal values are dated at the start of stable growth, with two dating errors computed.
- Comparables use matched numerators (EV with leases and pensions against post-IFRS 16 EBITDA; US GAAP lease and IAS 38 development adjustments).
- Restructuring separates value created from value transferred; EPS accretion is not a value test.
- Recommendations (Harbour valuation, payout, bolt-on) state alternatives and sensitivity.

**Harbour assumptions added.** Share price EUR 11.00 at 31 December 2025; risk-free rate
3.0 percent; equity premium 5.5 percent; peer unlevered beta 0.93; pre-tax cost of debt
5.2 percent (a 4 percent 2030 bond at 94.83, BBB); an illustrative rating-to-spread
schedule calibrated so Harbour's coverage maps to BBB; cycle ROEs for 2021-2023; a
hypothetical peer table. Computed WACC 8.02 percent supports the 8 percent input of the
earlier valuation.

**Numerical evidence.**
- `notes/artefacts/corporate-finance/corporate-finance-checks.py`: 16 parts, 65 checks. Independent routes: NPV from a cash-flow vector against a line-by-line build; IRR by root search; profitability-index ranking against brute-force search of every combination; equivalent annual cost against replication; MM equity returns from income against the Proposition II formula; trade-off optimum by grid against the first-order condition; Lintner recursion against its closed form; a discrete rating fixed point for the cost-of-capital curve.
- `notes/artefacts/systematic-equities/equity-valuation-checks.py`: 18 parts, 62 checks. Independent routes: Gordon and two-stage values against explicit sums of thousands of years; the H-model against an exact linear decline; implied returns by root search against closed forms; DDM, FCFE and residual income equal under clean surplus, closed form and year by year; harmonic mean against the average earnings yield; regression by least squares; Harbour values reproduced from the statement-analysis script before sensitivities.
- Both scripts execute the Harbour script with output suppressed, so balances and the 8.49 value come from one source.

**Errors caught during development** (all corrected before the text was final):
- several expected figures set before computing (NPV, IRR, ROIC path, the NPV crossover, the expansion option, book-weight WACC, Lintner dispersion, multistage values, harmonic mean, terminal-multiple growth, SUE, HHI); the text uses the computed values;
- a first spread schedule mapped Harbour to AAA at its own debt level, inconsistent with its 5.2 percent cost of debt; it was recalibrated, and the curve now uses a rating fixed point;
- the claim that no return on new capital could justify the price was false (a terminal RONIC of 124 percent does); the text states the reverse-engineered values instead;
- the valuation FCFE of 19.04 was first described as deducting right-of-use additions; it deducts share-based pay (the lease presentation leaves FCFE unchanged);
- a homemade-leverage label and a cumulative-dividend reconciliation label were wrong;
- a quotation of Damodaran's definition of intrinsic value was reconstructed from memory and has been replaced with the printed text (IV p. 12);
- the Paccar example and the capital-allocation process were first attributed beyond what the sources say; the text now follows Porter pp. 12-13 and marks the process as Interpretation;
- unescaped `%` in two source URLs broke the PDF build.

**Coverage.** All 45 objectives were reassessed operation by operation at their stated depth
and moved to `covered`, mapped to 44 entries (`meth:gordon-growth-model` and
`meth:multistage-ddm` together carry the Level I growth-model objective; the basic
constant-growth formula is already in `meth:instrument-present-value`). Objectives move
from 236/424 to 281/424, and outline items from 532/1,030 to 655/1,030 (Level I 256,
Level II 216, Portfolio Management 48, shared core 135). This is editorial coverage, not
learner mastery or independent human review.

**Limits.** Harbour, Kestrel, Ridgeway, Norland, Calder, Ashby, Company R and the peers are
hypothetical. Rating spreads, factor loadings, carbon prices and peer data are scenario
inputs. Damodaran's market data and tax descriptions are as of 2012-2014.

## Corporate-equity audit correction pass, 20 October 2026

**Starting state.** Verified before edits: PR #29 (draft, head `6157abb`, base `main`), PR #30
(draft, head `1f51fcf`, base `codex/macro-source-corrections-20261020`) and PR #31 (draft, head
`a6b6c64`, base `codex/accounting-statement-analysis-20261020`) open and unchanged; the checkout
was clean on `codex/corporate-equity-valuation-20261020` at `a6b6c64`; coverage 281/424 objectives
and 655/1,030 items. These corrections are ordinary commits on PR #31's branch. They count toward
no new objective. The batch record above is kept as history; where it differs, this record
supersedes it.

**Findings reproduced first.** Each audit claim was recomputed from the canonical Harbour inputs
before the text was changed: the five million vested options are worth 17.94 at the market price on
the equity-bridge inputs, so market EV omitting them (1,461.83) is not on the DCF bridge's claim
set; dividing the whole EV/EBITDA residual by the shares gave 11.59 and 9.88; the justified P/E
route multiplied ROE x B0, already E1, by 1.025, so it exceeded the P/B route by exactly 2.5
percent; the Harbour FCFE sentence omitted the 6 of issue proceeds; FCFE for Ridgeway already
contained borrowing; the bolt-on's 8.33 percent was pre-tax; the 102.19 assumed redemption; the
cumulative-voting notation used the holder's shares where the total belongs, and the displayed
1/6 product was not an integer.

**Corrections.**
1. *Options in enterprise value* (`def:price-value-indicators`, `meth:enterprise-value-multiples`,
   `meth:comparables-evaluation`, `meth:valuation-price-judgement`). Market EV 1,479.77 includes
   options at 17.94; the intrinsic bridge with the same claims rebuilds the DCF EV of 1,218.45
   (options 9.28 at 8.49). EV/EBITDA 7.59 (from 7.50); the lease-omission mismatch 7.07 (from 6.98);
   development-adjusted 8.55 (from 8.45). Peer-multiple values solve
   p = (residual - 5 C(p)) / 100.75: 11.39 (options 19.45) and 9.75 (options 13.40), superseding
   11.59 and 9.88.
   *WACC claim definitions* (`meth:wacc-calculation`, `meth:cost-of-debt-equity-estimation`,
   `meth:capital-structure-benchmarking`, `ex:restructuring-valuation-effects`). The entry defined
   equity options as equity but omitted them from the weights. With them: equity 1,126.19, D/E
   31.52 percent, beta 1.1499, ke 9.32 percent (from 9.34), WACC 8.02 percent (unchanged at two
   decimals); book weights 7.40 percent; pension as debt 8.017 percent. The cost-of-capital curve at
   firm value 1,481.19 gives 10.90 percent at 40 percent debt and 12.73 percent at 50 percent (from
   10.15 and 11.60); covenant leverage 1.33, 2.09 and 2.47 at 20, 30 and 35 percent; the bolt-on's
   pro forma D/E 36.85 percent, beta 1.1870, ke 9.53 percent, re-rated WACC 8.17 percent (from 8.18).
2. *ROE timing* (`meth:justified-multiples`, `meth:normalised-earnings`, `meth:sustainable-growth`,
   `meth:alternative-multiples`). Convention chosen: ROE_t = E_t / B_{t-1} wherever ROE drives a
   valuation or growth formula. Harbour's 2024-2025 ROE on opening equity is 12.01 and 9.15 percent
   (11.52 and 8.84 on average equity, which the ratio analysis keeps); the cycle average is 10.79
   percent (from 10.63). With ke 9.32 percent: payout 76.8 percent, leading P/E 11.26, P/B 1.22,
   D1 0.533; P/E x E1 = P/B x B0 = D1/(ke - g) = 7.81, and a 4,000-year dividend sum agrees. The
   superseded double growth gives 8.00 on these inputs (7.83 against 7.64 on the old ones); the
   average-equity variant gives 7.66 on every route. Normalised EPS 0.6935 is dated 2026; the
   like-dated 2025 figure is 0.6505 against underlying 0.6862. Sustainable growth 3.86 percent (from
   3.73), equal to retained profit over opening equity. P/S 0.58; implied ROE 14.18 percent.
   The audit's expected 7.64 assumed the average-equity cycle ROE; it is not adopted because that
   ROE is not E1/B0.
3. *FCFE and dividend funding* (`meth:dividend-sustainability`). Harbour: FCFE 28.04 = dividends 32
   - issue proceeds 6 + cash increase 2.04; the 3.96 by which dividends exceeded FCFE was met by the
   share issue. Ridgeway now states free cash flow before borrowing (60, 52, 34), actual net
   borrowing (30, 18, 21), FCFE (90, 70, 55), opening debt 1,050 and cash 200: the 121 gap is met
   from cash (200 to 79); net debt rises 190 = 69 + 121 = 336 - 146; target-policy borrowing at
   2.25x EBITDA (0, -45, -45) gives policy FCFE 56, cover 0.17. Share-based pay remains a separate
   valuation charge (19.04).
4. *LP, LLP and LLC* (`def:organisational-forms-issuers`). Rewritten from 6 Del. C. secs. 15-306(a),
   (c), (e), 15-1001, 17-303(a), 17-403(b) and 18-303, read in the official online code; the
   inference that a partner remains liable for its own wrongs is marked as Interpretation.
5. *Acquisition return* (`ex:restructuring-valuation-effects`). After tax 5.0 x 0.75 / 60 = 6.25
   percent, 1.77 points below the 8.02 percent WACC. EPS accretion, the one-year accounting return
   and DCF value are listed as different measures. The recommendation is unchanged because it rests
   on the standalone DCF (52 against 60), which the after-tax return confirms.
6. *Callable preferred* (`meth:preferred-stock-valuation`). 102.19 is a deterministic value
   conditional on redemption at year five with the yield held at 4.5 percent; at a year-five yield
   of 5 percent or more redemption at 100 gains the issuer nothing; 8.92 is the cost on that path,
   not an option value.
7. *Cumulative voting* (`def:equity-rights-voting`). N is the total number of shares voting;
   floor(N k/(D+1)) + 1 shares guarantee k seats when all shares vote, plurality elects and ties are
   lost; 1,666,667 retained.

**Numerical evidence.** `corporate-finance-checks.py` now executes 75 checks (from 65) and
`equity-valuation-checks.py` 72 (from 62). New checks would detect each original error: the
superseded EV equals the corrected EV less the option value; the old peer value exceeds the
iterated one; the old P/E route exceeds P/B by exactly g; dividends + cash change - FCFE = 6; net
debt growth equals borrowing + cash drawn, so counting the 121 as borrowing would double count;
EBIT/price is 8.33 percent and after tax 6.25 percent; the voting threshold is minimal by an exact
integer test for k = 1 to 5 and one share fewer fails; redemption is tested against several
year-five yields. Independent routes: the option fixed point against the DCF bridge, the dividend
sum against the closed forms, the cash identity for Ridgeway.

**Coverage.** The 17 objectives whose entries changed were reassessed at their stated depth and
remain covered; their 43 outline items keep their mappings, with rationales noting the recheck.
Coverage unchanged: 281/424 objectives and 655/1,030 items.

**Limits.** Option inputs, the 2021-2023 ROEs and the peer data remain illustrative. Delaware
case law and other states' partnership statutes were not read.

## Credit, time-series and valuation batch, 20 October 2026

**Starting state.** Branch `codex/credit-timeseries-valuation-20261020` from the corrected
PR #31 head `59df95b` (`codex/corporate-equity-valuation-20261020`). All 45 objectives were
`missing`; three had candidate entries (`mech:cds-contract-credit-events`,
`def:sovereign-credit-defaults`, `mod:garch-volatility-forecast`). Their 119 outline items map
to no objective outside the batch. Coverage before: 281/424 objectives, 655/1,030 outline items.

**Scope (45).**
- equity-research-reporting: 2; free-cash-flow-valuation: 4; residual-income-valuation: 3; private-company-valuation: 3
- intercorporate-investments: 2; foreign-currency-reporting: 3; financial-institution-analysis: 3
- credit-risk-analysis: 2; credit-models: 4; credit-default-swaps: 3; sovereign-credit-analysis: 1; securitisation: 3
- linear-regression: 4; time-series-models: 7; backtesting-simulation: 1

Implemented in prerequisite order: forecast models and research reports, free cash flow,
residual income, private companies; intercorporate investments, foreign currency, financial
institutions; credit risk and corporate credit, credit models, CDS, sovereign credit,
securitisation; multiple regression, then time series; scenario analysis last.

**Outline pages read.** Level I (`7099c7688942`) PDF pp. 16-17, 21-22; Level II
(`0242f4b7ba07`) PDF pp. 1-2, 8, 14-16, 18-19, 27. Each of the 119 items was reviewed against
its page and given an item-specific rationale in `outline-crosswalk.json`. The review found
gaps that were then written into the entries rather than recorded as residual gaps: the types
of heteroskedasticity and the direction of serial-correlation bias, the regression process and
problem types, a seasonal-lag forecast value, numerical ARCH variance forecasts, implied
residual-income growth from P/B, value recognition across models, three-stage FCFE and
multiple-based terminal values, special purpose and variable interest entities, IAS 21
disclosures, card and auto ABS, residential loan features, spread drivers by macro, market and
issuer factors, issue ratings by seniority, and CDS against equity and loans.

**Sources read** (versions, sections and key results in the reading notes):
- Books: Damodaran, *Investment Valuation*, 3rd ed. (2012), pp. 157, 167-168, 282-284, 351-363, 372-376, 380-383, 667-698, 870-877, 894-919; Subramanyam and Wild (2009), pp. 41-43, 262-275, 301-311, 492-502, 547-558, 566-568; Hull, *Risk Management and Financial Institutions*, 6th ed. (2023), pp. 28-34, 57-66, 367-401, 413-415, 689-691; Hull, *Options, Futures, and Other Derivatives*, 11th Global ed. (2021), pp. 201-206, 587-598; Fabozzi (ed.), *Handbook of Fixed Income Securities*, 9th ed. (2021), pp. 204-207, 362, 370-374, 1021-1024; Fabozzi and Kothari, *Introduction to Securitization* (2008), pp. 3-24, 31-46, 85-97, 153-166, 217-218, 284-286; Tsay, *Analysis of Financial Time Series*, 3rd ed. (2010), pp. 30-31, 37-47, 53-56, 71-78, 114-117, 428-431.
- Online texts and papers: Hyndman and Athanasopoulos, FPP3 secs. 5.2, 5.8, 5.10, 7.4, 7.5, 9.1; Penn State STAT 501 lessons 5-8 and 10-14 (Internet Archive copies); Fuster, Lucca and Vickery, NY Fed Staff Report 1001 (2022), pp. 1-10; Berd, Mashal and Wang (2004, arXiv 0912.4618), p. 13.
- Standards, law and supervision: IAS 21, IAS 28, IAS 29, IFRS 10, IFRS 11, IFRS 12 and paragraphs of IAS 12, IFRS 3 and IFRS 9 (EU 2023/1803); FAS 52 (paras. 5-16, 39) and the summaries of FAS 141R, FAS 160, FAS 167 and ASU 2016-01; Basel Framework RBC20, RBC30, LEV20, LCR20, NSF20 (generated 20/10/2026); UFIRS, 62 FR 752-757 (1997); Regulation (EU) 2017/2402 Arts. 2, 6; Directive (EU) 2019/2162 Arts. 3, 4, 15, 16; Delegated Regulation (EU) 2016/958 Arts. 2-5; FINRA Rule 2241(c); FHFA AB 2021-02.
- Data: Damodaran's US annual returns 1928-2025 (already in the repository) for the regression, time-series and scenario examples.
- Curriculum volumes and answer workbooks were not used; the outlines were used only to map and review items.

**Access limits and unread sources.**
- The IMF sovereign risk and debt sustainability framework guidance and MSRB pages refused access (403 and access denied); APB Opinion 18 returned an access-denied file, so the US 20 percent equity-method presumption rests on Subramanyam and Wild.
- Ohlson (1995) is paywalled; the persistence factor is stated as a derivation. Diebold's and Hamilton's PDFs were image-only. S&P and Moody's rating methodologies (including notching) were not read; issue ratings by seniority are marked Interpretation.
- Newey and West (1987) and Engle and Granger (1987) were not read; HAC errors and the two-step test are used through statsmodels and marked Interpretation. The 2014 ISDA Definitions remain unread (sold by ISDA).
- The STAT 501 copies were fetched through the Internet Archive; their capture timestamps were not retained in the saved files. Only the summaries of FAS 160 and FAS 167 were read.
- CMBS balloon risk lacks a primary source read here and is marked Interpretation.

**Discrepancies found in sources** (recorded in the entries and reading notes):
- Hull (2023) Table K.1 prints the year-4 survival probability as 0.9321; Table K.2 and $e^{-0.08}$ give 0.9231.
- Fabozzi and Kothari: the average life at 165% PSA rebuilds to 8.54 years against a printed 8.6; Table 3.2 retires class B in month 97 while the text says 98, and prints balances for classes C and D (96.5m, 73m) that differ from Structure 1 as stated (159.225m, 120.45m); the p. 94 mortality table lists A (0.28%) below AA (0.50%). The PAC total of 470,224,580 reproduces to the dollar.
- Hull (2021) Example 25.1: the implied hazard rebuilds to 0.5721% against a printed 0.5717%, with the same duration (4.447) and price (100.27); the difference is within payment and default timing conventions.

**Conventions protected by the examples.**
- Risk-neutral default probabilities for valuation, physical ones for scenarios; recovery as a share of par; CVA with exposure including the coupon due at default.
- CDS hazards implied and values computed with the same recovery; Credit01 neutrality distinguished from jump-to-default neutrality.
- Translation: current rate preserves local ratios; temporal exposure is the net monetary position; hyperinflation restated before translation under IFRS.
- Time series: every forecast comparison is chronological (train to 1989, test 1990-2025, expanding window); stationarity is tested before regressions on levels; Engle-Granger residuals use their own critical values.
- Simulation: the bootstrap resamples whole years to keep the stock-bond pairing; sensitivities use common random numbers.

**Numerical evidence** (locked uv environment, Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1, statsmodels 0.15.0; all run with `python -W error` by `make examples`):
- `notes/artefacts/systematic-equities/equity-fcf-ri-private-checks.py`: 12 parts, 48 checks; rebuilds the Harbour value from its forecast; FCFF by four routes; FCFF and FCFE values equal at constant leverage and against a 3,000-year sum; RI against DDM with the dirty-surplus identity; EVA against DCF.
- `notes/artefacts/financial-statement-analysis/intercorporate-fx-institutions-checks.py`: 9 parts, 44 checks; equity method by two routes; consolidated balance sheet against one-line parent equity; translation adjustment as a plug against its decomposition, including Subramanyam and Wild's BritCo; Hull's DLC and Table 3.2.
- `notes/artefacts/corporate-credit-capital/credit-cds-securitisation-checks.py`: 10 parts, 52 checks; Hull Examples 17.1-17.4, Tables 17.1-17.5, 19.1-19.2 and Appendix K; OFOD Example 25.1 and Table 8.1; the sovereign debt formula against a nominal roll-forward; Fabozzi and Kothari's pool, sequential and PAC tranches rebuilt month by month.
- `notes/artefacts/linear-regression/multiple-regression-checks.py`: 4 parts, 21 checks; normal equations against statsmodels; nested F by SSE; the omitted-variable identity; logit by Newton-Raphson against statsmodels.
- `notes/artefacts/time-series-models/time-series-checks.py`: 7 parts, 32 checks; hand-run Dickey-Fuller and LM statistics against statsmodels; forecasts by recursion against closed form; Chow test from subsample SSE.
- `notes/artefacts/backtest-inference/scenario-simulation-checks.py`: 3 parts, 10 checks; scenario returns against data rows; Monte Carlo moments against analytic values.

**Errors caught during development** (all corrected before the text was final):
- many expected figures were set before computing (ARCH estimates, cointegration critical value, AR(4) out-of-sample RMSE, Merton spread, CDS strategy notionals, sovereign debt change, scenario percentiles, regression residual years and others); the text uses the computed values;
- the Quay balance sheet first used book assets of 540 instead of 530, which broke the consolidated balance sheet; the residual-income identity was first written with the wrong sign for the equity credits; the temporal-method direct route was first mis-specified and was rewritten with fully specified dollar flows;
- the consolidation ratio check claimed full consolidation had the highest leverage; proportionate consolidation does, and the text says so;
- the Silber regression needed exponentiation and division by 100;
- a claim that restoring Tamar Bank's coverage would cost "a full year" of profit was wrong (0.68 against 0.40); an unsourced historical example of capital-structure arbitrage losses was removed; a paraphrase of Hull on speculative-grade spreads was tightened to what p. 384 says;
- a cross-reference to a nonexistent ROIC entry and a \citealp macro the house style does not define were replaced.

**Coverage.** All 45 objectives were reassessed operation by operation at their stated depth
and moved to `covered`, mapped to 45 new entries plus the three candidates above. Objectives
move from 281/424 to 326/424, and outline items from 655/1,030 to 774/1,030 (Level I 279,
Level II 312, Portfolio Management 48, shared core 135). This is editorial coverage, not
learner mastery or independent human review.

**Limits.** Penrose, Quay, Larch Brands, Tamar Bank, Wren Insurance, Kestrel Logistics, the
Arden bond, Larkspur, Veloria, Avon Fittings, Brent Utilities and Fenton Engineering are
hypothetical, as are the rating-spread schedule, the scenario probabilities and the CDS market
quotes used in the strategies. Regulatory texts are as read in October 2026; national
implementations of Basel and of the covered bond directive were not read.

## Valuation and inference audit correction pass, 20 October 2026

**Starting state.** `main` at `191edb2` (PR #32 merged); branch `codex/alternatives-audit-20261020`
from it. The untracked copies whose names end in " 2" were left in place and excluded from every
commit; because the checker reads them as duplicate labels, the final validation ran in a separate
worktree. Coverage at the start: 326/424 objectives and 774/1,030 items. These corrections count
toward no new objective.

**Findings reproduced first**, each by an independent identity or counterexample before the text
changed:
1. *FCFF and interest classification* (`meth:fcff-fcfe-derivation`). Built from receipts and
   payments, Avon's CFO with interest paid in financing and taxes in operating is 120 - 19.50 - 8 =
   92.50. CFO less capital investment is 47.50, 3.00 (= 12 x 0.25) above the 44.50 that the EBIT,
   net-income and EBITDA routes give; CFO - Int x t - FCInv restores it. If the tax saving were also
   classified in financing, CFO would be 89.50. The superseded check described the CFO difference as
   9; it is 12. IAS 7 before IFRS 18 allowed either classification (para. 33); IAS 7 para. 34A as
   amended by IFRS 18 requires financing for entities without a specified main business activity;
   taxes stay in operating (para. 35) in both versions.
2. *FCFE, payout and endogenous borrowing* (`meth:fcf-forecasting`, `meth:cash-flow-proxies`).
   `forecast(payout=0.50)` raises the 2026 dividend to 36.62 and the revolver draw from 30.81 to
   38.28; actual FCFE goes from 31.82 to 39.08, still equal to dividends plus the unchanged 2.46 cash
   increase. FCFE before the revolver moves only from 1.01 to 0.80, and valuation FCFF from 31.93 to
   31.88 (0.8 x t x the extra interest: the model settles a fifth of current tax in-year). The claim
   that FCFE is unchanged was wrong under the revolver policy and right only with borrowing fixed in
   advance (Avon: dividends 30 + buyback 10 + cash 5.50 = 45.50). Damodaran p. 355 says dividends
   above FCFE are financed from cash or new stock; the entry had attributed "or borrow" to him.
3. *Residual income and outstanding options* (`meth:residual-income-valuation`,
   `meth:residual-income-comparison`, `meth:justified-multiples`). The RI aggregate 809.2412 values
   all equity claims, including the five million vested options; the DDM aggregate 834.1610 also
   includes future grantees (PV of credits 24.9198). The option fixed point
   p = (809.2412 - 5C(p))/100.75 gives 7.9557 (options 7.70), confirmed by a root-finder; 834.16 -
   24.92 - 7.70 = 801.54 = 7.9557 x 100.75. Simple division gave 8.0322 and 8.2795. The dirty-surplus
   identity is unchanged; future grants enter only through the RI charge, so deducting the vested
   options does not double count. On all equity claims (1,126.19, P/B 1.74) the implied RI growth is
   7.34 percent and the implied ROE 14.37 percent; the shares alone give 7.27 and 14.18 percent. The
   justified P/B aggregate 786.43 becomes 7.74 a common share (7.81 by division); the multiples
   entry now says so.
4. *Diversification versus marketability* (`meth:private-company-valuation`). Damodaran's Table 24.2
   (p. 689) applies both a total-beta cost of equity and an illiquidity discount to a private sale,
   and Illustrations 24.10-24.11 (pp. 687-690) pair a 15.27 percent total-beta cost of capital with
   a 12.94-28.75 percent illiquidity discount. The blanket double-counting pitfall was therefore
   wrong. Double counting arises when an illiquidity premium is already in the rate (the p. 674 box
   warns of this for build-ups) or in the comparables. Fenton's basis is now stated: a control,
   marketable value to a diversified buyer; an undiversified buyer's 30 percent stake is 3.73 with
   the marketability discount, 4.81 without.
5. *Structured-entity control* (`def:intercorporate-investment-classification`). IFRS 10 paras. 7,
   10, B8-B9, B22, B51 (design ``alone is not sufficient''), B53-B54 and B58-B60, and FAS 167 paras.
   14A-14F and Example 1 (bondholders bear losses without power; the special servicer is the primary
   beneficiary). The Penrose table now has three vehicle cases: power and returns (subsidiary),
   returns without power (unconsolidated structured entity, IFRS 12 disclosure), and design plus
   losses only (not determinable). The check script derives control from power, returns and the
   principal test; the hardcoded `control=True` input is gone.
6. *Regression inference* (`meth:regression-misspecification`). Var(b|X) = (X'X)^-1 X'Omega X
   (X'X)^-1. With ten observations, an intercept and AR(1) errors, the ratio of true slope variance
   to the expected usual estimate is 2.75 and 0.41 for a trend at rho = +0.5 and -0.5, and 0.43 and
   2.96 for an alternating regressor; a seeded 20,000-draw simulation gives 0.42 for the alternating
   case. Rescaling the stock regressor to percentage points divides its slope and standard error by
   100 and leaves t, R2 and fitted values unchanged, so units are not a specification error.
   Unbiasedness is now conditioned on strict exogeneity; the lagged-dependent-variable case is
   described as inconsistency.
7. *Forecast validation matched to the decision* (`meth:time-series-model-selection`). Target:
   cumulative inflation over the five years after each origin. On the 31 common origins 1990-2020,
   with estimation on data to each origin only: RMSE AR(1) 5.94, mean 6.12, AR(4) 7.27, random walk
   7.56, trend 19.36 percentage points; mean errors -3.21, -4.10, -4.63, +0.60, -10.44. AR(1) errors
   autocorrelate at 0.76 at lag 1 (about six independent windows). Diebold-Mariano with Newey-West (4
   lags): AR(4) against AR(1) t = 2.61; AR(1) against the mean -0.40 and against the random walk
   -1.45. The 1990-2025 data are described as selection validation, not a holdout. The wartime
   claim is qualified: from 1953 BIC prefers AR(1) and AIC barely separates the models, and the
   lag-4 coefficient falls from 0.43 to 0.17, which fits but does not demonstrate the explanation.
8. *Insurer coverage* (`meth:insurer-analysis`, new `meth:life-insurer-analysis`). The outline item
   (Level II p. 8) asks for key ratios and other factors for an insurance company, which includes
   life insurers; the existing entry explicitly did not develop them. Sources read: IFRS 17 paras.
   32, 37-38, 43-44, 47-50, 83-85 (EU 2023/1803); Solvency II Directive Arts. 75-78, 101, 105 and
   Annex IV and Delegated Regulation 2015/35 Arts. 37-39, 136-140, 142 (original OJ texts, CELEX
   32009L0138, SHA-256 8b71252cb8de50200e6b2257e753777779c23eb6cdd8c6978563cfd6f182e96e; CELEX
   32015R0035, SHA-256 210316eaa3ef18510c137bbcab8d3fbe824be408e1cb147c4bacc0ec1f7b8471); Hull (2023)
   pp. 52, 56-57, 62-63; CNP Assurances' 2017 MCEV report pp. 6, 12, 21-22. The new entry covers
   new-business value and the CSM, technical provisions and the SCR, matching, mortality, longevity
   and lapse, with limits; a two-insurer comparison and a new-business case are reproduced in
   `intercorporate-fx-institutions-checks.py` part 10. The item stays covered with both entries
   mapped.

**Access and source limits.** EUR-Lex HTML returned empty responses; the Publications Office
CELLAR XHTML was used. The CFO Forum MCEV Principles could not be retrieved (the download did not
return the PDF); an issuer's MCEV report prepared under them is cited instead, as company-defined
measures. The Solvency II texts are the original ones; the 2025 review and later delegated
amendments are not reflected. US risk-based capital was not read.

**Numerical evidence.** `equity-fcf-ri-private-checks.py` 57 checks (from 48);
`intercorporate-fx-institutions-checks.py` 54 (from 44); `multiple-regression-checks.py` 24 (from
21); `time-series-checks.py` 36 (from 32). Each new check would fail on the superseded statement:
CFO - FCInv = 47.50 differs from 44.50; FCFE moves by 7.26 with the payout; simple division exceeds
the option-adjusted value by C(p) x 5 / 100.75; the stake without the marketability discount is
4.81, not 3.73; the design-and-losses case is not determinable; positive autocorrelation gives a
ratio below one for the alternating regressor; the five-year RMSEs and overlap are recomputed from
data to each origin.

**Coverage.** The 11 objectives whose entries changed were reassessed at their stated depth and
remain covered; their 32 outline items keep their mappings, with rationales noting the recheck, and
`objective:analyse-insurer` now maps both insurer entries. Coverage unchanged: 326/424 objectives and
774/1,030 items.

## Alternatives batch, 20 October 2026

**Starting state.** Branch `codex/alternatives-audit-20261020` from `main` at `191edb2`, after the
audit commit `0d62a5d` (*Valuation and inference audit correction pass*), which counts toward no
objective. All 45 objectives were `missing`; three had candidate entries
(`def:contango-backwardation-stocks`, `def:commodity-indices-risk-return`,
`mech:etf-creation-redemption`). Their 113 outline items map to no objective outside the batch;
two items are shared by two batch objectives (`7099c7688942:m084:b03`, `2f25110282bf:m034:b04`)
and carry one rationale each. Coverage before: 326/424 objectives, 774/1,030 outline items.
Untracked copies named "... 2" in the working tree were neither deleted nor committed; the full
checks ran in a separate worktree.

**Scope (45).**
- firms-market-structure: 3 (cost and output, market structures, identification)
- private-capital-allocator: 17 (structures, fees and returns 3; private equity and debt 9; programmes 5)
- real-asset-investor: 10 (real estate 6; infrastructure 3; land, timber and farmland 1)
- commodity-investing-premia: 4; portfolio-construction-risk: hedge funds 3, allocation to alternatives 2
- execution-trading-costs: ETFs 2; corporate-credit-capital: credit portfolio strategies 4

Implemented in prerequisite order: market structure; alternative structures, fees and returns;
private equity and debt; private-market programmes; real estate, infrastructure and land;
commodities; hedge funds; ETFs; credit portfolios; allocation to alternatives last, because it
draws on all of the above.

**Outline pages read.** Level I (`7099c7688942`) PDF pp. 5, 25-26; Level II (`0242f4b7ba07`)
PDF pp. 23-24, 26; Level III core and Portfolio Management (`2e1d62d8f585`) PDF pp. 6, 18;
Level III core and Private Markets (`2f25110282bf`) PDF pp. 16-18. Each of the 113 items was
read against its page and given an item-specific rationale in `outline-crosswalk.json`. Gaps
found in review were written into the entries rather than left as residual gaps: specialist and
multi-manager hedge fund families, vehicles beyond limited partnerships (managed accounts,
registered funds), ETF spread components and the Rule 6c-11 disclosures, international credit
and analytical tools, commitment pacing, the denominator effect and programme monitoring.

**Sources read** (versions, sections and key results in the reading notes):
- Books (owner's library PDFs outside the repository, cited by printed page): Varian (2014); Demaria et al., *Asset Allocation and Private Markets* (2021); Ippolito, *Private Capital Investing* (2020); Tsolacos and Andrew (2021); Lynn et al. (2009); Larreur, *Structured Finance* (2021); Geman, *Commodities and Commodity Derivatives* (2005); Jaeger, *Alternative Beta Strategies and Hedge Fund Replication* (2008); Abner, *The ETF Handbook*, 2nd ed. (2016); Ben Dor et al., *Quantitative Credit Portfolio Management* (2012) and *Systematic Investing in Credit* (2021); and further chapters of Ang (2014) chaps. 11, 13, 14, 17; Damodaran, *Investment Valuation* (2012) chap. 26; Hull, *Options, Futures, and Other Derivatives* (2022) pp. 195, 781; Hull, *Risk Management and Financial Institutions* (2023) chap. 19.
- Papers (working-paper versions, retrieved 2026-10-20): Gorton and Rouwenhorst (NBER WP 10595, revised March 2006); Erb and Harvey (NBER WP 11222, March 2005); Getmansky, Lo and Makarov (NBER WP 9571); Kaplan and Schoar (WP 9807); Kaplan and Strömberg (WP 14207); Harris, Jenkinson and Kaplan (WP 17874); Gompers, Kaplan and Mukharlyamov (WP 21133); Metrick and Yasuda (WP 16652); Luxenberg et al. (arXiv 2207.07767).
- Law, standards and data: SEC Rule 6c-11 (eCFR, last amended 85 FR 83291); 11 U.S.C. 1126 and 1129; the 2023 Merger Guidelines (already held); Nareit FFO White Paper (2018 restatement); NCREIF NPI snapshot 2Q 2026 and a Timberland Index commentary (1Q 2023); USDA ERS Farmland Value page (2026 update); OpenStax *Principles of Microeconomics* 3e secs. 7.5, 8.2, 10.1, 10.2, 11.1.
- Curriculum volumes and answer workbooks were not used; the outlines were used only to map and review items.

**Access limits and unread sources.**
- The published *Financial Analysts Journal* versions of Gorton and Rouwenhorst and of Erb and Harvey (catalogue entries `s16-r34`, `wide-erb-harvey-commodity`), the *Journal of Finance* and *JFE* versions of the private equity papers, and the ICAIF version of Luxenberg et al. were not read; the working papers are cited and the entries say so.
- Takahashi and Alexander (2002) is paywalled; its model is described through Luxenberg et al. (p. 3). Petajisto (2017) and Ben-David, Franzoni and Moussawi on ETFs were not read.
- Lhabitant's *Hedge Funds: Quantitative Insights* copy has no text layer and was set aside. The USDA NASS land values PDF and a farmland dissertation could not be retrieved; the ERS summary was used. The NCREIF NPI full methodology and TPI methodology were not obtained.
- Specialist hedge fund niches (insurance-linked, sector specialists), basis swaps, securities-lending offsets, international credit currency considerations and analytical-tool inputs lack a primary source read here and are marked Interpretation.

**Discrepancies found in sources** (recorded in the entries and reading notes):
- Erb and Harvey (2005) p. 13: oil's roll return printed 13.1% but $40.95/$36.65 - 1 = 11.73%; the far contract is dated June and then July 2005; p. 25 gives the same diversification return as 3.4% and "about 3.5%" (half of 12.8 - 5.3 is 3.75).
- Ang (2014): backfill bias printed 7.3% where 14.7 - 7.3 = 7.4 (p. 565); the 2000s negative roll return attributed to "highly backwardated" oil, contradicting the book's rule that backwardation gives positive roll (pp. 369-370); Table 11.7's 1970s row adds to 21.7 against 21.6 printed.
- Gorton and Rouwenhorst: abstract sample ends March 2004, figures run to December 2004.
- Demaria et al. (2021): net exposure "at best between 40 and 60 percent" (p. 186) against 45-65% (p. 175); n. 103 repeats n. 96; growth pooled IRR above the printed top quartile; the IRR footnote formula and the farmland passage across pp. 143-144 (details in the reading note).
- Ippolito (2020) p. 175: dilution divides by (1 + D) while D is described as the later investors' share.
- Damodaran (2012) Illustration 26.4: intercept printed -2,535.50 and -2,535.70.
- Abner (2016) p. 48: the redemption fee per share printed as 200,000/$2,000 for 2,000/200,000.
- Ben Dor et al. (2012) p. 257: position-size ratio printed "2:6 : 1.5 : 1.0" for 2.6.

**Conventions protected by the examples.**
- Fees, carry and clawback computed on dated LP cash flows; PME and IRR on the same flows; smoothing reversed before risk statistics are used.
- Commodity futures returns compound contract by contract; the roll is measured from the curve, not as a cash flow; the diversification return belongs to a rebalanced portfolio, not one commodity.
- Hedge fund exposures summed across lags; allocation tested on de-smoothed volatility and full-cycle correlation, net of avoidable fees.
- ETF premium measured at NAV time; the Rule 6c-11 median uses 10-second NBBO snapshots.
- Credit exposure in DTS; issuer limits on DTS contribution; Vasicek's percentile checked against simulation.
- Private exposure measured as NAV plus uncalled commitments; commitments sized from the steady-state gain, not set equal to the target NAV.

**Numerical evidence** (locked uv environment, Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1, statsmodels 0.15.0; all run with `python -W error` by `make examples`):
- `notes/artefacts/firms-market-structure/market-structure-checks.py`: 4 parts, 13 checks; shutdown and breakeven prices; Cournot closed form against iteration; CR4, HHI and merger change.
- `notes/artefacts/private-capital/private-capital-checks.py`: 8 parts, 29 checks; hedge fund fees with a high-water mark; fund waterfall, carry and clawback; J-curve, PME, gross and net IRR; venture method; LBO returns; credit ratios; smoothing; allocation.
- `notes/artefacts/real-assets/real-asset-checks.py`: 6 parts, 24 checks; direct capitalisation against DCF; NCREIF chain-linking; REIT NAV, FFO, AFFO and DDM; levered underwriting; DSCR-sculpted project debt; farmland and raw land.
- `notes/artefacts/commodity-investment/commodity-return-checks.py`: 4 parts, 15 checks; Ang's Table 11.7 and eq. 11.3; Erb and Harvey's roll and diversification figures; a quarterly roll simulated in backwardation and contango; rebalancing and roll schedules; swap values.
- `notes/artefacts/hedge-funds/hedge-fund-checks.py`: 6 parts, 17 checks; fund-of-funds fee layers; merger, long/short and convertible arithmetic; smoothing closed forms against simulation; factor regression with lags against generating loadings; the Sharpe-ratio allocation test.
- `notes/artefacts/etf-mechanics/etf-checks.py`: 5 parts, 13 checks; Abner's fee and cash arithmetic; the market maker's quote; Rule 6c-11 premium, seven-day and median-spread tests; leveraged paths; costs of ownership.
- `notes/artefacts/credit-portfolios/credit-portfolio-checks.py`: 4 parts, 17 checks; DTS by two routes; spread measures; ESP and DTS-neutral hedges; LCS; issuer caps; Vasicek against simulation; CDS overlay, hedged yield and CLO OC test.
- `notes/artefacts/alternatives-allocation/alternatives-allocation-checks.py`: 5 parts, 13 checks; crisis scenarios; factor-mapped exposure; steady-state pacing against simulation; denominator effect; liquidity coverage.

**Errors caught during development** (all corrected before the text was final):
- many expected figures were set before computing and differed (contango excess return, hedged-fund Sharpe ratios, Vasicek percentile, ETF quote, merger annualisation, factor-mapped beta, real-asset and private-capital figures); the text uses the computed values;
- a first spread-median test had a tie at the median and was redesigned; a cash merger's annualised spread was misstated by 0.01 point;
- undefined macros (`\citealp`, `\euro`) and a cross-reference to a nonexistent non-GAAP label were replaced; a Gorton and Rouwenhorst point stated in prose was given a citation so the evidence key is cited by its entry; an overfull Vasicek formula was moved to a display;
- a claim that ETF prices "fell far below fair value" in the 2015 flash crash was narrowed to what Abner reports (widened quotes, hard pricing, stop orders in 2010).

**Coverage.** All 45 objectives were reassessed operation by operation at their stated depth
and moved to `covered`, mapped to 45 new entries plus `mech:etf-creation-redemption` (one
sentence updated to point to the new Rule 6c-11 material). Objectives move from 326/424 to
371/424, and outline items from 774/1,030 to 887/1,030 (Level I 302, Level II 349, Portfolio
Management 59, Private Markets 34, shared core 143). This is editorial coverage, not learner
mastery or independent human review.

**Limits.** Brook Relative Value, Ashby Fund I, Novaro, Corran Industrial, Halden, Marlow House,
Kestrel REIT, Ferris Park, Ashdown Hospital and the commodity, hedge fund, ETF, credit and
allocation portfolios are hypothetical. Practitioner books (Demaria, Ippolito, Larreur, Jaeger,
Abner, Ben Dor) describe market practice of their dates; the Ben Dor results are back-tests by a
sell-side research group. Human review is outstanding.

## Alternatives audit correction pass, 20 October 2026

**Starting state.** Branch `codex/alternatives-audit-20261020` at `505a13f`, draft PR #33 to `main`
open, working tree clean; no files named "... 2" were present. Coverage at the start: 371/424
objectives and 887/1,030 items. These corrections count toward no new objective.

**Findings reproduced first**, each by an identity, boundary case or primary text before the entry
changed:
1. *Timberland accounting* (`meth:land-timber-farmland`). Adding 5.04 percent of growth and price,
   a 3 percent harvest yield and 2 percent land appreciation counts the harvested wood twice (it is
   inside the 5.04 percent) and weights land as if it were the whole stand. A stand of 100 m3 at 30
   on land of 1,000 (NAV 4,000), growing 4 percent, harvesting 3 m3 at 30.30 and paying costs of 15,
   closes at NAV 4,080.30 with distributions of 75.90: 3.905 percent. The opening-weight
   decomposition (0.75 x 5.04 + 0.25 x 2 - 0.375) reproduces it. With no growth and unchanged prices
   the harvest returns only the costs (-0.375 percent). The NCREIF split into income and appreciation
   on one denominator (p. 28) is the index analogue; the accounting itself is derivation.
2. *Infrastructure construction financing* (`meth:infrastructure-underwriting`,
   `meth:infrastructure-allocation`). The old script subtracted the debt sized at completion (165.83)
   from the cost of 200 and spread the 34.17 of equity over two years, so lenders implicitly funded
   construction interest-free; its "LLCR at financial close" was an operating-start figure. Dated
   convention adopted: close at t = 0, payments of 100 at t = 1 and 2, pro-rata draws of 80.89 with
   the first draw's 4.04 of interest capitalised, opening operating balance 165.83 at t = 2, sculpted
   repayment to zero over 22 years. Sources 165.83 + 38.21 = uses 200 + 4.04; equity IRR 9.63
   percent. The alternative (draws of 82.92, interest of 4.15 paid by equity) gives 9.65 percent,
   matching the audit's orientation figures; at a zero construction rate both collapse to 10.70.
   Larreur pp. 157-158 (staged drawdowns) and p. 171 (equity first, pro rata or back-ended) support
   the conventions; the interest treatment is derivation. The allocation entry now says 9.6 percent
   on 81 percent gearing of total cost.
3. *Distressed debt* (`meth:special-situations-distressed`). Primary text read for 11 U.S.C. 364,
   506(a), 1124, 1126(c)-(e) and 1129(a)(7)-(10), (b)(1)-(2) (LII pages saved in
   `reading_materials/completion-20261020/`). The entry had conflated a blocking position in the
   class vote with preventing confirmation, and described absolute priority as "no junior class
   receives anything while it is impaired". Cramdown needs an accepting impaired non-insider class
   (a)(10) and fair and equitable treatment, which differs for secured classes ((b)(2)(A)) and
   unsecured ones ((b)(2)(B)). DIP priority over existing liens requires a sec. 364(d) finding
   (credit unavailable otherwise, adequate protection) or consent; the example's assumptions are now
   stated. Threshold corrected from 260 to 250 (40 + 10 + 200); at 255 the bonds receive 5. Boundary
   cases: a holder of two-thirds by amount still fails the number test against ten small holders;
   reinstated senior debt is unimpaired (1124(2)) and cannot supply the accepting class.
4. *Private-fund PME* (`meth:private-fund-multiples-pme`). The formula omitted residual NAV. With it,
   Ashby's year-4 PME is 1.10 (0.56 without); a contribution of 100 with NAV 110 after a 10 percent
   index rise gives exactly 1. Kaplan and Schoar's main sample is of largely liquidated funds (p. 6);
   Harris, Jenkinson and Kaplan state the residual-value treatment (p. 10) and distinguish the
   Long-Nickels excess return (p. 11). The deflated-flow IRR (5.67 percent) is a money-weighted
   excess; with a constant 5 percent index it equals (1 + IRR)/1.05 - 1 = 6.39, not 6.71.
5. *Covered bonds* (`meth:credit-cds-international-structured`, `meth:abs-structures-credit-enhancement`).
   The credit entry listed covered bonds with ABS as pool exposures with subordination, a 50-70
   percent senior tranche and floating coupons. Directive 2019/2162 Arts. 4, 5 and 15(4) and recital
   17 make covered bonds bank obligations with dual recourse, no acceleration and a cover pool kept
   at coverage; Regulation 2017/2402 Art. 2(1) defines securitisation by tranching and pool-dependent
   payments. Larreur's 68.5 percent senior share and Libor coupons belong to his corporate-loan
   securitisation (Table 10.1, p. 260); prepayment pass-through belongs to mortgage pass-throughs
   (Fuster et al. pp. 7, 10). Bank Corvel cases check issuer-solvent, issuer-insolvent and
   prepayment outcomes against a tranched securitisation of the same pool.
6. *Replacement cost* (`meth:real-estate-valuation-indexes`). The entry called the cost approach a
   floor. IVS 105 (2016 exposure draft, paras 70.1-70.3, 80.2-80.5, 90.1-90.7) sets out substitution,
   modern-equivalent replacement cost and physical, functional and economic obsolescence; Damodaran
   pp. 537-538 (Tobin's Q) gives value below replacement cost when assets earn less than their
   required return. Harbour Point: depreciated for physical wear only, 58; income 40, comparables 42,
   reconciled 41; functional 5.33 and economic 11.67 obsolescence close the gap. The text says cost
   is neither a floor nor an unconditional ceiling.
7. *Credit liquidity costs* (`meth:credit-liquidity-tail-risk`). LCS is a round-trip cost (Ben Dor
   et al. pp. 81-82, 88). Applying the full 0.40 percent to a one-way sale of half the portfolio gave
   0.20 percent; against mid marks it is 0.10 (proceeds 49.90; 100 = 49.90 + 50 + 0.10), against bid
   marks 0 and against ask marks 0.20. Remaining bonds 60/40 with LCS 1.34 percent. Index removals at
   the bid (p. 274) and quote indications (p. 90) are noted.

**Numerical evidence.** `real-asset-checks.py` 37 checks (was 24), `private-capital-checks.py` 38
(was 29), `credit-portfolio-checks.py` 25 (was 17), all passing in the locked uv environment
(Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1). New checks test identities (sources = uses, NAV
reconciliation, distribution totals, cash identity), boundary cases (zero growth, zero construction
rate, benchmark-matching PME, junior DIP lien, voting by number) and statutory conditions, not only
restated constants.

**Coverage.** Ten objectives and 27 outline items rechecked, with their rationales and evidence
updated; mapping and coverage unchanged (371/424, 887/1,030).

**Limits.** Case law on cramdown, unfair discrimination, new value and priming was not read; IVS 105
is cited from its exposure draft; national covered-bond transpositions and the CRR minimum
overcollateralisation were not read; construction delay and reserve accounts remain outside the
Ashdown model.

## Completion batch, 20 October 2026

**Starting state.** Branch `codex/alternatives-audit-20261020` at `2d9f2f3` (*Alternatives audit
correction pass*, which counts toward no objective), draft PR #33 open. Coverage before: 371/424
objectives and 887/1,030 outline items. All 53 remaining objectives were `missing`; five had
candidate entries (`def:inside-information`, `rule:spoofing-securities-markets`,
`meth:purged-embargoed-cross-validation`, `meth:backtest-evaluation-diagnostics` with
`pit:parameter-overfitting`, `def:amm-pool-mechanics`, `def:crypto-venue-instrument-structure`),
none of which performs the objectives' operations, so new entries were written and the candidates
kept as cross-references. The 143 remaining outline items map only to these 53 objectives; one item
(`0242f4b7ba07:m007:b07`) maps to two and carries one rationale. No "... 2" copies were present.
This batch supersedes the standing 45-objective preference at the user's request: all remaining
objectives and items.

**Scope (53).**
- professional-ethics (new chapter): 22 (ethics and trust 2; code, programme and enforcement 2; Standards I-VII applied and prevention 14; evaluating conduct 1; Asset Manager Code 2; manager selection 1)
- private-wealth-management (new chapter): 15 (clients and industry 5; planning 5; preservation 2; transfer and complex clients 3)
- portfolio-construction-risk: institutional investors 6
- ml-alternative-data: 7 (learning methods 3; data-science workflow 4)
- research-engineering-validation: backtest design 1
- digital-assets-prediction-markets: distributed ledgers and digital-asset investing 2

Implemented in prerequisite order: ethics (framework, code, Standards, cases, firm code, manager
selection); private wealth (capital and taxes before the IPS, planning before preservation and
transfer); institutional investors (characteristics before DB risk, IPS evaluation, the SWF case,
endowment liquidity and ESG); machine learning (methods before workflow, text and evaluation);
backtest design; ledger mechanics before digital-asset investing.

**Outline pages read.** Level I (`7099c7688942`) PDF pp. 3, 26, 29-31; Level II (`0242f4b7ba07`)
PDF pp. 2-3, 27, 29-30; Level III core (`2e1d62d8f585`) PDF pp. 6-7, 13-15, 18; Private Wealth
(`5bc9c1013387`) PDF pp. 16-18. Each of the 143 items was read on its page and given an
item-specific rationale naming the entry and what it does for that item. Gaps found in review were
written into entries rather than left as residual gaps: bank and insurer balance sheets in the
institutional IPS entry, liquidity strategies in the goals-based plan, the joint family decision
framework, enterprise risk management against GAPP 22, preventive procedures for each Asset
Manager Code provision, and the custody and vehicle layer for digital assets.

**Sources read** (versions, sections and key results in the reading notes):
- Ethics (issuer's official texts, not curriculum readings): *Standards of Practice Handbook*, 12th ed. (2024); *Rules of Procedure for Conduct Related to the Profession* (2022); the *Ethical Decision-Making Framework* card (2014, member-society copy); *Asset Manager Code*, 2nd ed.; SEC Release IA-5248 (2019) on advisers' standard of conduct; Gennaioli, Shleifer and Vishny, *Money Doctors* (NBER WP 18174).
- Private wealth: Survey of Consumer Finances 2022 (Federal Reserve Bulletin, October 2023); Ibbotson et al., *Lifetime Financial Advice* (2007); IRS Rev. Proc. 2025-32 and Notice 2025-67; 26 USC 401(a)(9), 664, 877, 877A, 1014, 1015, 1091, 1202, 1411, 2001, 4942, 7701(b); 17 CFR 240.10b5-1 and 240.15l-1; ESMA suitability guidelines (2022); MiFID II art. 24; GOV.UK and HMRC pages for income tax, CGT, ISAs, pensions, inheritance tax, the statutory residence test (RDR3), IHTM47020 and the 2024 non-dom reform; IRAS residency rules; the UK-US double taxation convention (2001/2002); and *Portfolio Management in Practice*, vol. 1, chap. 6 (read in an earlier batch).
- Institutional: Ang (2014) chaps. 1, 3, 13; the Santiago Principles (2008); NBIM's GPFG pages (2026); Lerner, Schoar and Wang (NBER WP 14341); the GSIA review (2022).
- Machine learning and backtesting: James et al., *ISLR*, 2nd ed. (owner's copy); Gentzkow, Kelly and Taddy (NBER WP 23276); FSB, *AI and Machine Learning in Financial Services* (2017); López de Prado, *AFML*, chaps. 2, 11-12.
- Digital assets: Nakamoto (2008); BIS Annual Economic Report 2018, chap. V; Narayanan et al. (draft of 9 February 2016); ethereum.org proof-of-stake and Merge pages (2026); Liu and Tsyvinski (NBER WP 24877); SEC Release 34-99306 (89 FR 3008, January 2024).
- Curriculum volumes and answer workbooks were not used; the outlines were used only to map and review items. Handbook examples were read but not reproduced: every case in the ethics entries is original.

**Access limits and unread sources.**
- sec.gov, the IRS treaty page, regjeringen.no, SSA life tables and the ISLR/ESL sites refused automated download; the Federal Register (govinfo) copies of the SEC releases, the GOV.UK treaty text, NBIM's own pages and the owner's ISLR copy were used instead. The private-wealth mortality example uses an illustrative Gompertz law, labelled as such, not an official life table.
- EUR-Lex returned blank pages; MiFID II was read from the Publications Office (CELLAR) copy. The BIS chapter PDF link returned HTML; the HTML version is cited by section heading.
- The published *Bitcoin and Cryptocurrency Technologies* (2016), the RFS version of Liu and Tsyvinski, the *Journal of Finance* version of *Money Doctors* and the *JEP* version of Lerner et al. were not read; the drafts and working papers are cited and the entries say so.
- State and local taxes, case law, Treasury regulations, HMRC manuals beyond IHTM47020, the SEC's 10b5-1 and Reg BI adopting releases, and later spot-ETP orders (in-kind creation, ether) were not read.

**Discrepancies and approximations found in sources.**
- Nakamoto (2008) sec. 11 treats the attacker's progress as Poisson; the exact negative-binomial count gives 0.178 percent after 5 blocks at q = 0.1 against the printed 0.091 percent, so the paper's waiting times are lower bounds (`digital-asset-checks.py` part 3, with a simulation).
- The FSB report (2017) and the BIS chapter (2018) describe their dates; Ethereum moved to proof-of-stake in September 2022, after both and after the Narayanan draft.

**Conventions protected by the examples.**
- Taxes and thresholds are dated (US tax year 2026, UK 2026-27) and every client is hypothetical.
- Machine-learning examples are synthetic, labelled as such, with training, validation and an untouched test set; every fitted transform, vocabulary and idf weight is estimated on training data only.
- Backtest examples use a simulated universe with no predictability, so any performance is an artefact of design.
- Ledger mechanics (hashing, consensus, finality) are kept separate from investment exposure, vehicle, custody and liquidity.

**Numerical evidence** (locked uv environment, Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1; all run with `python -W error` by `make examples`):
- `notes/artefacts/private-wealth/private-wealth-checks.py`: 13 parts, 43 checks; human capital and economic net worth; after-tax and real returns; required return; fee models; goals and funded ratio; illustrative mortality, disability and longevity; asset location and harvesting; reporting; retirement accounts; residence tests; founders and executives; gifts against bequests (counting exemption use) and philanthropy.
- `notes/artefacts/institutional-portfolios/institutional-checks.py`: 5 parts, 21 checks; DB funded status and surplus risk; spending rules, a foundation's payout, bank and insurer gaps; the GPFG fiscal rule and a hypothetical sovereign fund; endowment liquidity stress, the denominator effect and pacing; ESG constraint costs.
- `notes/artefacts/financial-ml-methods/ml-methods-checks.py`: 6 parts, 23 checks; overfitting; lasso KKT and ridge closed form; trees, forest, KNN and SVM; PCA, k-means and hierarchical clustering; leakage; text features; classifier metrics and ROC.
- `notes/artefacts/backtest-inference/backtest-design-checks.py`: 5 parts, 10 checks; survivorship, look-ahead, turnover and costs, drawdown by two routes, best-of-24 against walk-forward, expanding against rolling windows.
- `notes/artefacts/digital-assets/digital-asset-checks.py`: 7 parts, 21 checks; SHA-256 chain and Merkle branch; proof-of-work cost; Nakamoto's table, the exact count and a simulation; issuance schedule; proof-of-stake timing; Liu and Tsyvinski consistency; hypothetical allocation and multisignature custody.

**Errors caught during development** (all corrected before the text was final):
- expected values set before computing differed from the computed ones (survivorship and look-ahead figures, risk share of a 5 percent crypto weight, simulated attacker probability, ML test errors); the text uses the computed values, and placeholder checks were replaced by computations (10b5-1 dates, wash-sale window, denominator effect);
- the gift-against-bequest comparison first ignored the use of the lifetime exclusion; four source keys carried the provider token and were renamed (`standards-practice-handbook-2024`, `conduct-rules-of-procedure-2022`, `ethical-decision-framework-2014`, `asset-manager-code-2010`);
- cross-references to labels that do not exist (thirteen across the batch) were corrected; missing locators were added;
- reading-note statements not supported by the saved texts were corrected before commit: the conduct panel and standard of proof, UK dividend rates, a "pandering" claim, the Lerner et al. findings, NBIM's risk limit, the Santiago principle numbers and Singapore's three-year concession.

**Coverage.** All 53 objectives were reassessed operation by operation at their stated depth and
moved to `covered`, each mapped to one new entry. Objectives move from 371/424 to 424/424, and
outline items from 887/1,030 to 1,030/1,030 (Level I 340, Level II 382, Portfolio Management 64,
Private Markets 34, Private Wealth 27, shared core 183). This is editorial coverage, not learner
mastery or independent human review.

**Limits.** The Okafors, Harlow Industrial, the Vardø Fund, Elmsworth, the ethics firms and
people, the default classifier and the crypto allocation are hypothetical. Tax and regulatory
figures are dated and jurisdiction-specific and will change. Ethics entries interpret the Standards
for original cases; the issuer's own guidance governs. Human review is outstanding.

## Final audit correction pass, 20 October 2026

**Starting state.** Branch `codex/alternatives-audit-20261020` at `316c07e`, draft PR #33 to `main` open, working
tree clean. Coverage at the start: 424/424 objectives and 1,030/1,030 items. No new objectives; denominators and
requirements unchanged. Every number below was reproduced by an identity, a boundary case or the primary text before
the entry changed; old values are kept for comparison.

**Findings and corrections.**
1. *Backtest costs* (`meth:backtest-design-evaluation`; `backtest-design-checks.py`). The old rule measured turnover as
   a quarter of the change in successive target weights and deducted twice that times 20 bp: for absolute trades of 2.0
   it charged 0.002 instead of 0.004, and unchanged targets after unequal returns cost nothing. Conventions now stated
   (NAV = cash + signed positions; long-short target +1/-1, gross 2; short proceeds in cash; cash, rebates and borrow
   at zero; targets on post-trade NAV, so f = c sum|w*(V - f) - h|; establishment charged; delisted positions sold).
   Hand-reconciled ledgers: establishment from 100 (fee 0.2/1.002 = 0.19960, cash 0); 55/45 rebalanced to 50/50
   (sell 5.01, buy 4.99, traded 10, fee 0.02); the long-short swap (traded 2.0, fee 0.004, cash 0.996); long-short
   drift (fee 0.2c/(1+c)). The full simulation checks cash + positions = NAV after every trade, zero-cost equality
   with the gross target book, and (1 - f/V)(1 + w*.r) month by month. Momentum: traded 1.09 of NAV a month against
   0.96 from target changes; cost drag 2.62 percent a year (1.17 before); net -2.51 percent a year, Sharpe -0.40
   (was -1.05 and -0.17); hit rate 0.43 (0.47).
2. *Maximum drawdown*. The running peak and its brute-force check both started after the first return. Now both include
   the initial wealth of 1; [-0.10, +0.05] gives 10 percent, [-0.05] 5 percent, a rising path 0, and the old peak gives 0
   on the first two, so the cases detect the error. Net maximum drawdown 50 percent (39 before); gross 32 percent.
   The other two drawdown implementations (`drawdown-resampling-checks.py`, `performance-evaluation-checks.py`)
   already included the start.
3. *Asset location* (`meth:tax-in-planning`; `private-wealth-checks.py` part 7). Taxable stocks compounded
   (1 + d(1 - t))(1 + g) while IRA stocks compounded 1 + d + g. One convention now: price +5 percent and a 2 percent
   dividend on opening value, dividend at year-end, after-tax dividend reinvested and added to basis. Year 1: value
   532,620, basis 507,620, gain 25,000; IRA 535,000. Bonds in the IRA: 2,454,619 (2,474,630 before); reverse
   2,316,409. With zero taxes both placements give 3,140,699, whereas the old conventions would have shown 36,488.
4. *The Okafor case* (`meth:individual-wealth-capital`, `meth:private-client-ips`, `meth:goals-based-financial-plan`,
   `meth:lifetime-exposures`, `meth:private-client-allocation-review`). The 60,000 reserve now sits outside the
   540,000 policy portfolio and on neither side of the funded ratio: required real return 2.30 percent (1.96
   percent counted the reserve twice), confirmed by projecting forward to the 1.76m need. Human capital to retirement at
   62: 3.00m at 40 (3.29m to 65). One saving figure (50,000), education at 8 and 10 years in every calculation (parts
   1 and 5 had used 10 for both), the 35 percent joint band (Rev. Proc. 2025-32 sec. 4.01, Table 1, p. 10) instead of
   "top bracket". Funded ratio 1.16 at 3.5 percent and 0.91 at 1.5 percent (1.22 and 0.95); saving of 58.1k restores
   1.0. Allocation, on stated illustrative real assumptions: 70/30, 60/40 and 40/60 give compound 3.22, 3.03 and 2.57
   percent, one-in-twenty one-year returns of -15.1, -13.4 and -10.2 percent, and surpluses of 0.28, 0.22 and 0.08m.
   The recommendation changes from 70/25/5 to 60/40, which willingness governs; 40/60 is the lower-risk alternative
   if paired with higher saving. Life cover 1.95m (2.17m). The review uses the Okafors' own 540,000 and saving:
   TWR 11.72, MWR 11.78 percent, funded ratio 1.16 to 1.20.
5. *Pension funding law* (`def:institutional-investor-characteristics`, `meth:db-pension-risk`). Read: IRS Notice
   2021-48, IRB 2021-33, p. 305, secs. I-IV (https://www.irs.gov/irb/2021-33_irb); 26 U.S.C. 430(a), (c)(1)-(2),
   (c)(5), (c)(8), (d)(1), (g)(3), (h)(2)(C)(iv) on LII. For single-employer plans, plan years beginning after 31
   December 2021 (earlier by election), earlier shortfall bases are reduced to zero and new bases amortised over 15
   plan years; the minimum is target normal cost plus installments when assets fall short of the funding target of
   accrued benefits; the segment-rate corridor is 95-105 percent through 2030. Ang's seven years (2014) is now
   attributed to the Pension Protection Act. Harlow: statutory shortfall 0.40bn on a stylised funding target of
   8.4bn, accounting deficit 1.0bn, economic deficit about 1.81bn; a single new base over 15 years costs 38.5m; the
   96.34m (15-year) and 172.82m (7-year) annuities on the accounting deficit are labelled policy illustrations. The
   conclusion now separates a moderate cash burden from high economic risk.
6. *Endowment spending law* (`def:institutional-investor-characteristics`, `meth:institutional-ips-portfolios`,
   `meth:endowment-liquidity-allocation`). Read: New York NPC sec. 553(a), (b), (d), (e) and the Article 5-A table
   (NY Senate site, revision of 14 July 2017). The presumption is rebuttable, applies to post-enactment gift
   instruments, uses quarterly values averaged over at least five years, and gives no presumption of prudence below 7
   percent. Elmsworth is now a New York corporation with donor-restricted, post-enactment gifts setting no rate; with
   five prior years assumed flat at 2,000m, spending peaks at 5.28 percent of the statutory average (6.6 percent of the
   post-crash value). The uniform-act text was not obtained, so the entry says only that states differ. Liquidity:
   185.6m remain after net outflows of 212.4m (173 before, which ignored the 12.6m of distributions counted in the
   coverage ratio).
7. *Family accounts and IPOs* (`rule:standard-duties-to-clients`, `meth:preventing-client-duty-violations`,
   `rule:standard-conflicts-of-interest`, `meth:preventing-conflict-violations`). Read: Standards of Practice Handbook,
   12th ed., III(A) Example 7, p. 74; III(B) guidance, p. 77; VI(B) guidance, p. 165, Examples 2-3, p. 167; the issuer's
   III(B) (updated April 2024) and VI(B) (updated January 2024) web pages. The blanket exclusion of family accounts is
   replaced by a classification of personal and beneficially owned accounts (excluded from oversubscribed issues) and
   family client accounts (allocated pro rata, flagged and reviewed); contrasting original cases added.
8. *UK inheritance tax* (`meth:wealth-transfer-strategies`; part 13). Read: HMRC, "Inheritance Tax: residence nil rate
   band" (published 8 November 2016, updated 5 September 2019); IHTM46023 (updated 7 April 2026); the thresholds table
   (updated 6 April 2026) and the gifts page. The band now tapers by 1 for every 2 above 2m on the estate excluding
   lifetime gifts (175k at 2.0m, 125k at 2.1m, 0 at 2.35m), capped at the home's value. The gift example now has the
   donor dying 4.5 years after the gift (24 percent, 42,000). The examples form one chronology: the gift consumes the
   nil-rate band, so the 2.4m estate pays 960,000 (830,000 before, which reused the band); total 1,002,000 against
   1,030,000 without the gift, the difference being the taper relief of 28,000.

**Coverage revalidation.** Sixteen objectives and their 43 outline items, all at their recorded depth (15 decision,
1 analysis). Each item was reread against the corrected entry; 35 rationales gained a specific revalidation note and
8 a note that the correction does not touch them. All remain covered: 424/424 objectives and 1,030/1,030 items.
New sources: `irs-notice-2021-48`, `ny-npc-553`, `govuk-rnrb-guidance-2019`, `hmrc-ihtm46023-2026`, with reading
notes; IRC sec. 430 added to `us-internal-revenue-code-26`.

**Validation** (locked uv environment, Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1; LuaLaTeX from TeX Live 2023).
Focused: `backtest-design-checks.py` 19 checks (10 before), `private-wealth-checks.py` 53 (43), `institutional-checks.py`
22 (21), each with `python -W error`. Final: `make check` (lock, ruff lint and format, check-compendium 0 problems,
check-coverage 0 problems, pytest 36 passed, 106 check scripts, `--verify-outlines` 0 problems, PDF of 424 pages
with no overfull boxes or undefined references) and `make pre-commit` (12 hooks passed). Pages 18-19, 265-267,
276-282 and 36-38 were rendered and inspected.

**Limitations.** The Okafor capital market assumptions, willingness threshold, Harlow funding target and Treasury
spread, and Elmsworth's pre-example values are stated assumptions, not data. The New York article's effective date was
not taken from a primary page. Editorial coverage only; human review and study are outstanding.

## PR #33 correction pass, 21 October 2026

**Starting state.** Branch `codex/alternatives-audit-20261020` at `394d15c`, draft PR #33 to `main` open, working
tree clean. Coverage at the start: 424/424 objectives and 1,030/1,030 items. Corrections only: no objective created,
no denominator or requirement changed. Each finding was reproduced before the entry changed; old values are kept for
comparison.

**Findings and corrections.**
1. *Okafor tax assumptions* (`meth:private-client-ips`; `private-wealth-checks.py` part 3). Reproduced: the IPS read a
   15 percent rate on qualified dividends and gains from the 35 percent ordinary band, but Rev. Proc. 2025-32 sec. 4.03
   (p. 13) puts the 2026 joint 15 percent ceiling at 613,700, inside that band (512,450 to 768,700, sec. 4.01 Table 1).
   Read: IRC sec. 1(h)(1)(A)-(D), (h)(11), (j)(5) (LII, saved 2026-10-21); sec. 1411(a)(1), (b)(1); Rev. Proc. sec.
   4.14 (standard deduction 32,200). Stated 2026 return: wages 650,000 less 49,000 of 401(k) deferrals, interest
   2,400, qualified dividends 6,000, net long-term gains 60,000; AGI 669,400; taxable income 637,200; ordinary taxable
   income 571,200. Stacked: 42,500 at 15 percent and 23,500 at 20 percent; income tax 148,533.50 (the old inference
   gives 1,175 less); NIIT 3.8 percent of 68,400 = 2,599.20 (MAGI exceeds 250,000 by 419,400). Marginal rates by finite
   difference: 23.8 percent on gains (not 18.8), 40 percent on wages, 43.8 percent on interest. Checks: published
   cumulative bracket amounts (116,896 at 512,450; 206,583.50 at 768,700); the statutory formula against layer
   stacking; boundaries at 613,700 (all 15 percent at the ceiling, 20 percent on the next dollar), ordinary income at
   613,700 (all 20 percent), the zero-rate amount (38,900 at 0 percent on 60,000 of ordinary income), ordinary income of
   547,700 (all 66,000 at 15 percent); NIIT below the threshold and on the MAGI excess when it is the smaller amount.
2. *Harlow pension contributions* (`meth:db-pension-risk`, `def:institutional-investor-characteristics`;
   `institutional-checks.py` part 1). Reproduced: the entry treated the whole 0.40bn shortfall as a new base (38.5m)
   and then said the minimum adds installments on 2022-2025 bases, amortising the open bases twice. Read: IRC sec.
   430(a), (c)(1)-(3), (c)(5)-(6), (c)(8), (g)(2), (j)(1)-(3) (LII, saved 2026-10-21); Notice 2021-48 sec. III.B.1 (p. 5,
   PDF saved 2026-10-21), which lists the present value of remaining installments "for purposes of determining any
   shortfall amortization base established in the current plan year under § 430(c)(3)". Stated assumptions: valuation
   date 1 January 2026; one 5 percent effective rate for the segment rates; open bases 0.20, 0.08, 0.03 and 0.05bn set in
   2022-2025, a shortfall in every year; no waiver, prefunding or carryover balances; target normal cost 110m. Result:
   old installments 33.03m a year worth 303.2m; 2026 base 96.8m (installment 8.88m); shortfall charge 41.91m; minimum
   required contribution 151.91m at the valuation date (12.7 percent of EBITDA; deficit repair 3.5 percent), 165.12m if
   paid in one sum on 15 September 2027, before any surcharge on missed quarterly installments (an ordinary-interest
   illustration; see the close-out below). The double-counting
   construction gives 69.73m (27.82m too high). The 38.5m was also an end-of-year annuity; valued at the valuation date
   a single base costs 36.70m. Checks: the present value of all installments still due equals the shortfall; each
   base's balance reaches zero after 15 installments; no open bases (base = shortfall); assets above target (TNC less
   the excess, 60m); a negative base when the shortfall (0.25bn) is below the open installments' value (-53.2m, charge
   28.15m, floored at zero in aggregate by 430(c)(1)). Conclusion: deficit-repair cash is moderate under the stated
   assumptions; the true minimum cannot be determined without Harlow's valuation; accounting (1.0bn) and economic
   (1.81bn) deficits kept separate.
3. *Family client IPO allocations* (`rule:standard-duties-to-clients`, `meth:preventing-client-duty-violations`,
   `rule:standard-conflicts-of-interest`, `meth:preventing-conflict-violations`). Reproduced: the Linton family-client
   class required no employee beneficial interest and the personal class covered only accounts not managed under the
   client process, so a managed family account with an employee interest fitted neither. Read: Handbook III(B), p. 77;
   VI(B) guidance, p. 165; compliance practices, p. 166; Example 3, pp. 167-168 ("If Toffler has beneficial ownership in
   the account, however, ... she may have to preclear the trades and report the transactions"). The policy now asks two
   separate questions: allocation class by how the account is managed, conflict controls (register, holdings report,
   duplicate statements, preclearance of block participation that cannot change the pro-rata share) by beneficial
   interest. New original case: a taxable account the manager holds jointly with her mother, managed in the strategy on
   standard terms, receives the same 1,200 of a 60 percent fill after preclearance and with reporting; cutting it,
   skipping the controls or topping it up are violations. The Brook Lane code and the III(B) and VI(B) statements are
   aligned; Example 3's page reference corrected to pp. 167-168.
4. *Endowment spending comparison* (`meth:institutional-ips-portfolios`; `institutional-checks.py` part 2).
   Reproduced: pure 5 percent spending was divided by five-year averages of quarterly values generated by the smoothed
   rule. Each rule now carries its own quarterly history: pure peak 5.242401 percent (5.24, published 5.25, which the
   cross-policy construction gives as 5.245031); smoothed 5.28 and 5.07 unchanged. A check rebuilds the pure rule's 40
   quarter-end values from its own spending and confirms the cross-policy construction differs.

**Coverage revalidation.** Eight objectives and their 24 outline items, all at decision depth. Each item was reread
against the corrected entry; 21 rationales gained a specific revalidation note and 3 a note that the corrections do
not touch them. All remain covered: 424/424 objectives and 1,030/1,030 items. No new source keys; IRC sec. 1(h) and
(j)(5) added to `us-internal-revenue-code-26`, sec. 4.14 to `irs-rev-proc-2025-32`, sec. III.B.1 to
`irs-notice-2021-48`. Editorial coverage only; it does not establish learner mastery, and human review is outstanding.

**Close-out, 21 October 2026 (documentation only).** Branch at `f3d8791`, tree clean, draft PR #33 open. The
independent re-audit found the four corrections above resolved and all checks passing; it flagged that the 165.12m
September 2027 figure was qualified in the script and this record but not in the PR
description or, explicitly enough, the compendium. Read: 26 CFR 1.430(j)-1(b)(4)(i)-(ii) and (c)(1), (c)(5)-(6) (eCFR
current text, saved 2026-10-21). Paragraph (b)(4)(i) adjusts a payment made after the valuation date at the plan's
effective rate; (b)(4)(ii) treats any part of a payment that settles a late required installment in two steps, first
discounting it to the installment's due date at the effective rate plus 5 percentage points; (c) requires quarterly
installments of 25 percent of the lesser of 90 percent of the current minimum and 100 percent of the prior year's after
a shortfall year, due on the 15th of the 4th, 7th and 10th plan months and 15 days after the year. The 165.12m is
therefore labelled an ordinary-interest equivalent of the 151.91m valuation-date minimum, not a payable amount; an
actual single September 2027 payment would have to be larger by an amount that depends on Harlow's 2025 minimum, which
is not modelled. New source `cfr-26-1-430j-1` with a reading note; no figure, objective, denominator or requirement
changed: 424/424 objectives and 1,030/1,030 items, editorial coverage only.

## Library gap-filling, Batch L1, 21 October 2026

**Starting state.** Branch `codex/library-gap-batch-l1`, created from `codex/alternatives-audit-20261020` at `2b89791`
(draft PR #33 to `main` still open with that head, checked 2026-10-21). Coverage before: 424/424 objectives and
1,030/1,030 outline items, all covered. Scope: packages P1-P5, after the owner approved decisions E1 (ten new neutral
objectives, a denominator change) and E2 (a ten-objective batch, below the standing 45-objective preference). Before
implementation the proposed numerical contracts were corrected for the external audit's findings R1-R4: P7's wrong-way-risk sign (P7 was not implemented in this batch), a predetermined numerical criterion for P5's daily rebalancing, explicit P2-P3 example
conventions, and the count of existing entries touched (two substantive extensions, two cross-reference edits).

**P1, stochastic calculus** (new topic file `compendium/common-toolkit/stochastic-calculus.tex`; new
`topic:stochastic-calculus`).
- Read: Hull, *OFOD* 11th Global ed., chap. 14 (pp. 316-337, all sections and the appendix), chap. 15 (pp. 339-342 and
  348-352), chap. 28 (pp. 670-677); Wilmott, *PWOQF* 2nd ed., chap. 4 (pp. 71-88) and chap. 10, secs. 10.11-10.12
  (pp. 179-181). Wilmott chaps. 3-6 were initial source candidates; the passages that teach the material are chap. 4 and sec. 10.11,
  which are the ones cited. Neither book names Feynman-Kac or writes the Radon-Nikodym density: Hull states
  Girsanov's theorem as a change of the market price of risk that leaves volatilities unchanged (p. 674), and Wilmott
  reaches the risk-neutral expectation through the backward Kolmogorov equation (pp. 179-180). The density
  $Z_T=\exp(-\theta W_T-\tfrac12\theta^2T)$ is therefore given in the entry as a direct calculation and checked
  numerically; Shreve (`crypto-shreve`, not held) is Further reading only.
- Notation: Hull's $z$ and Wilmott's $X$ are written $W$; Hull's market price of risk $\lambda$ is kept in the
  Statement and $\theta$ used for the Girsanov kernel.
- Checks (`notes/artefacts/stochastic-calculus/stochastic-calculus-checks.py`, 22 checks, synthetic, seeds 20261021 to
  +3 fixed before running): quadratic variation 1.0052 (10,000 steps; s.d. 0.0141) and 0.9996 on the bridge-refined
  path; first variation 79.69 against 79.79; the left-point and midpoint integral identities. GBM with 200,000 exact
  draws: mean 108.363 (s.e. 0.049) against 108.329, median 106.207 (s.e. 0.060) against 106.184; $E[S_T^2]$ 12,220.5
  (s.e. 11.4) against Itô's 12,214.0, with the chain-rule 11,735.1 rejected; Euler RMS error 0.441 at 50 steps and
  0.043 at 5,000 on common paths (discretisation, not sampling, error). Girsanov: reweighted real-world draws give
  7.0979 (s.e. 0.0209) against the BSM call 7.1281, inside the predetermined 3 standard errors; unweighted
  discounting gives 9.9148. The discounted real-world expectation satisfies the PDE with $\mu$ (residual
  $-2.4\times10^{-7}$) and fails the Black-Scholes equation (residual $-2.58$).
- Existing entry touched: `mod:black-scholes-merton` (See also links only; no claim or check changed).
- Objectives: `objective:explain-brownian-motion-quadratic-variation`, `objective:apply-ito-lemma-gbm`,
  `objective:value-derivative-risk-neutral-expectation`, all covered.

**P2, numerical pricing** (new topic file `compendium/volatility-options/numerical-methods.tex`; extension of
`meth:monte-carlo-simulation`).
- Read: Hull, chap. 21, secs. 21.6-21.8 (pp. 489-509) and chap. 27, sec. 27.8 (pp. 660-665); Wilmott, chap. 77, secs.
  77.11-77.12 and 77.17 (pp. 1212-1215, 1224-1226), chap. 78, secs. 78.1-78.3, 78.7 and 78.9 (pp. 1227-1230,
  1242-1246) and chap. 80, secs. 80.1-80.6 (pp. 1263-1269). Not read: Longstaff and Schwartz (2001), Andersen and
  Broadie, Glasserman (`s6-glasserman`, not held; Further reading).
- Discrepancies and conventions. Hull's explicit coefficients discount by $1/(1+r\Delta t)$, Wilmott's subtract
  $r\delta t$ from the centre coefficient; the entry teaches Wilmott's form and the stated monotonicity condition,
  which adds the discount term to Wilmott's diffusion-only bound $\delta t\le1/(\sigma^2I^2)$. Hull's implicit American
  example projects after each linear solve (p. 502), which Wilmott calls "not good enough" for an implicit scheme
  (p. 1246); the entry says so. Neither source names the Rannacher start; it is an implementation choice in the
  examples, supported by Wilmott's remark that CN is not the best scheme for discontinuous initial data (p. 1243).
  Hull's control variate uses a coefficient of 1 (eq. (21.20)); neither source gives the estimated optimal
  coefficient, so it is stated as an Interpretation and checked. Hull prints the year-2 $S^2$ coefficient as $-1.813$;
  least squares on his Table 27.4 data gives $-1.81358$ (truncated, not rounded); the published value 0.1144 is
  reproduced (0.11443).
- Checks (`notes/artefacts/numerical-pricing/numerical-pricing-checks.py`, synthetic): European put (BSM 5.573526):
  Crank-Nicolson errors $1.00\times10^{-2}$ and $2.50\times10^{-3}$ at (150, 75) and (300, 150), ratio 4.01; explicit
  at $N=901$ and 3,601 (just inside $1/(\sigma^2I^2+r)$, all coefficients non-negative; node $i=1$ upwinded because
  $\sigma^2<r$) errors $8.86\times10^{-3}$ and $2.21\times10^{-3}$, ratio 4.01; explicit at $N=200$ (4.5 times the
  bound) reaches $2.9\times10^{92}$. American put: CRR 6.09028 (8,000 steps) and 6.09056 (8,001), reference 6.09042;
  CN with projected SOR 6.0780 ($I=150$) and 6.0870 ($I=300$, error $3.4\times10^{-3}\le4\times10^{-3}$), ratio 3.63;
  the explicit scheme with projection gives 6.0806. Bermudan put (50 dates): CRR 6.07853 (5,000 steps) and 6.07851
  (5,050), reference 6.07852; CN (600, 1,000) with projection only on the dates 6.07796 (within $5\times10^{-3}$); LSM
  out of sample 6.0386 (s.e. 0.0227), 0.040 below the reference, inside the predetermined $[-0.05,+3\text{ s.e.}]$
  band; in sample 6.1248 (reported, not tested). Every predetermined acceptance range passed on the first complete
  run; one check of my own on Hull's printed coefficients first used a tolerance of $5\times10^{-4}$ and failed
  because of the truncated print; it now allows $10^{-3}$ and the reason is stated in the script.
- Monte Carlo extension (`inference-simulation-checks.py`, same 100,000 draws as the existing call): estimated
  coefficient 0.5421, correlation 0.8746, variance reduction factor 4.25 (criterion above 2), estimate 7.1289 (s.e.
  0.0192) against 7.1281 (criterion 3 s.e.). A recorded coefficient of 0.5258 written before the run was wrong and
  was replaced by the computed value; the predetermined criteria were not changed. Euler bias on 400,000 common paths
  (seed 20261018 + 11): $-0.1254$, $-0.0536$, $-0.0250$ at 2, 4 and 8 steps (s.e. 0.0024 or less), ratios 2.34 and
  2.14 against the predetermined $[1.5,2.5]$.
- Objectives: `objective:price-options-finite-differences`, `objective:value-early-exercise-least-squares-monte-carlo`,
  covered. The control-variate extension deepens the covered `objective:apply-monte-carlo-simulation` and is not
  counted.

**P3, digital, barrier and Asian options** (new topic file `compendium/volatility-options/exotic-options.tex`).
- Read: Hull, chap. 26, secs. 26.9-26.10 and 26.13 (pp. 620-623, 626-627) and chap. 27, secs. 27.5-27.6 (pp.
  653-658); Wilmott, chap. 2 (pp. 43-44), chap. 7 (pp. 119-121), chap. 23 (pp. 385-386, 400-405) and chap. 25, secs.
  25.9-25.11 (pp. 440-442, page image of p. 440 viewed). Wilmott chaps. 22-23 and 25 were initial source candidates; the binary
  material is in chaps. 2 and 7, which are the passages cited. Not read: Broadie, Glasserman and Kou (1997), Kemna
  and Vorst (1990); both are cited through Hull or Wilmott, and BGK is Further reading.
- Discrepancy: Wilmott's summary of Kemna-Vorst (p. 440) replaces the dividend yield by $D+\sigma^2/6$; his own formula
  (p. 442) and the limit of the discrete geometric distribution give $\tfrac12(r+D+\sigma^2/6)$. The script shows the
  p. 440 version gives 6.5181 against 5.9802. The initial description of Hull's continuous-averaging form (sec. 26.13)
  was inaccurate: Hull gives moment matching for the arithmetic average and a footnote that the geometric average is
  lognormal, not the $\sigma/\sqrt3$ formula; the entry cites Wilmott for that formula.
- Checks (`notes/artefacts/exotic-options/exotic-option-checks.py`, synthetic, $S_0=K=100$, $r=5\%$, $q=2\%$,
  $\sigma=25\%$, $T=1$, 100,000 paths per Monte Carlo check, seeds 20261031-20261035 in check order). Digitals: call
  11.123762 = 58.4955 - 100 x 0.473717 to $10^{-12}$; call-spread errors $1.03\times10^{-4}$, $2.58\times10^{-5}$,
  $6.45\times10^{-6}$ (ratios about 4.0, criterion [3.5, 4.5]); simulated digital 0.4719 (s.e. 0.0015); delta at the
  strike 0.0152, 0.0550, 0.2533 at 1 year, 1 month, 1 day. Barrier $H=90$: $c_{do}=8.1388$, $c_{di}=2.9850$; in-out
  parity path by path to $10^{-12}$; Brownian-bridge Monte Carlo 8.1953 (s.e. 0.0529); daily monitoring 8.4890 (s.e.
  0.0538) against the shifted-barrier 8.5190 (barrier 89.178), inside 3 s.e. + 0.5 percent. Asian, 12 monthly dates
  excluding $S_0$: discrete geometric 6.3903 against 6.3888 (s.e. 0.0309); arithmetic 6.6797 (s.e. 0.0321)
  uncontrolled and 6.6813 (s.e. 0.00107) controlled, variance-reduction factor 900 (criterion above 10), difference
  inside 3 uncontrolled s.e.; continuous geometric 5.9802.
- Errors caught during development, all in checks of my own beyond the predetermined criteria (those criteria passed on
  the first run): a vega check failed because `call` captured $\sigma$ as a default argument, so the vanilla term
  had no vega (coding error, fixed); the corrected down-and-out vega with $H<K$ is positive near the barrier (0.81 at
  $S=91$ against 14.80 at 130), so my expectation of a negative sign was wrong; the check now tests that it shrinks
  below a tenth, and tests Hull's own example of negative vega, an up-and-out call ($K=100$, $H=120$, $S=115$: value
  0.1999, vega $-2.22$; the value was cross-checked once by a Brownian-bridge simulation outside the script, 0.2025,
  s.e. 0.0030). A convergence check with a 2e-3 tolerance at 1,000 dates failed because convergence to continuous
  averaging is first order (gap 0.00491 at 1,000 dates); it was replaced by a refinement check (gap 0.00982 at 500,
  ratio 2.0, criterion [1.9, 2.1]).
- Objectives: `objective:value-digital-options-pin-risk`, `objective:value-barrier-options-monitoring`,
  `objective:value-asian-options`, covered.

**P4, hedging with the wrong volatility** (new `res:delta-hedging-volatility-mismatch` in
`compendium/volatility-options/option-valuation.tex`; vanna and volga added to `meth:greeks-delta-gamma-hedging`; a See
also link in `meth:active-currency-strategies`).
- Read: Wilmott, chap. 12 (pp. 197-205), chap. 47 (pp. 763-770) and chap. 7 (pp. 127-128 with n. 3); Hull, chap. 19,
  sec. 19.4 (pp. 421-427, reread). Not read: Carr (2005), Henrard (2001), Ahmad and Wilmott (2005); eq. (12.2) is
  cited through Wilmott. Neither source uses the names vanna and volga; Wilmott records "vomma" and "kabanga" for
  the same derivatives, and the entry cites that and gives the formulas, checked by finite differences (vanna
  $-0.2814$, volga 9.8501 for the example's call at 20 percent).
- Checks (`notes/artefacts/option-valuation/volatility-mismatch-hedging-check.py`, 20,000 common paths, seed
  20261051): $V^a-V^i=14.2313-10.4506=3.7807$. Actual-volatility delta: mean 3.7770 (s.e. 0.0044, s.d. 0.627) at
  252 rebalancings and 3.7805 (s.e. 0.0014, s.d. 0.200) at 2,520, both inside 3 s.e.; s.d. ratio 3.14 (criterion
  [2.8, 3.5]). Implied-volatility delta: RMS gap to the pathwise integral 0.797 and 0.256, factor 3.12 (criterion
  [2.5, 3.8]); cross-path s.d. 1.75 at 2,520 steps (criterion above 1.5); mean 3.7462 (s.e. 0.0124), reported only.
  All criteria passed on the first run.
- Objective: `objective:quantify-hedging-volatility-mismatch`, covered. The vanna-volga sentence deepens the covered
  `objective:manage-option-greeks` and is not counted.

**P5, growth-optimal (Kelly) sizing** (new `res:kelly-growth-optimal-fraction` in
`compendium/portfolio-construction-risk/portfolio-construction-models.tex`).
- Read: Wilmott, chap. 17, sec. 17.5 (pp. 306-309) and chap. 66, sec. 66.4 (pp. 1057-1058, the growth-optimal
  portfolio, added during source review, which supplies the continuous-time fraction with a riskless asset and
  the log-utility link). Not read: Kelly (1956), Thorp (2008), Busseti, Ryu and Boyd (2016); no copy is in the
  library, so all three are Further reading only. The discrete-bet fraction $p-q/b$, the exact continuous identities
  and the estimation-error formula are derivations stated as Interpretation and checked.
- Discrepancy: Wilmott's "halves your volatility ... only decreases your expected growth rate by 25%" (p. 309) rests
  on his small-edge quadratic approximation (17.1); the entry states the exact continuous identity (excess growth over
  $r$) and shows it does not hold for discrete bets.
- Checks (`notes/artefacts/portfolio-construction/kelly-check.py`, synthetic, $\mu=8\%$, $r=2\%$, $\sigma=20\%$):
  $f^*=1.5$; excess growth 0.045 and 0.03375 (ratio 0.75), variance-rate ratio 0.25, $g(2f^*)=r$. Exact 10-year
  sampling (200,000 draws, seed 20261041): 0.05379 (s.e. 0.00011), 0.06508 (0.00021), 0.02016 (0.00042) against
  0.05375, 0.065, 0.02, standard deviations within 1 percent of $f\sigma/\sqrt T$. Daily rebalancing (20,000 x 2,520,
  seed 20261042) against 80-point Gauss-Hermite expectations 0.053750, 0.064999, 0.019900: simulated 0.05418 (s.e.
  0.00033), 0.06585 (0.00067), 0.02159 (0.00134), all inside 3 s.e.; biases $+2.8\times10^{-7}$, $-8.9\times10^{-7}$,
  $-1.00\times10^{-4}$ a year (criterion below $5\times10^{-4}$), refinement ratios 0.500, 0.500, 0.499 (criterion
  [0.4, 0.6]). Discrete bets: 0.7470 and 0.7727, both different from 0.75. Estimation error (10 years of data, seed
  20261043, a criterion fixed before running): expected excess growth $-0.00500$ at full and $+0.02125$ at half
  Kelly, simulated $-0.00515$ and $+0.02120$. All criteria passed on the first run.
- Objective: `objective:derive-kelly-growth-optimal-fraction`, covered.

**Batch completion.**
- Scope delivered: ten new entries (`def:brownian-motion-quadratic-variation`, `res:ito-lemma-geometric-brownian-motion`,
  `res:risk-neutral-pricing-feynman-kac`, `meth:finite-difference-option-pricing`, `meth:least-squares-monte-carlo`,
  `meth:digital-option-valuation`, `meth:barrier-option-valuation`, `meth:asian-option-valuation`,
  `res:delta-hedging-volatility-mismatch`, `res:kelly-growth-optimal-fraction`); three new topic files
  (`common-toolkit/stochastic-calculus.tex`, `volatility-options/numerical-methods.tex`,
  `volatility-options/exotic-options.tex`); two substantive extensions (`meth:monte-carlo-simulation`,
  `meth:greeks-delta-gamma-hedging`) and two cross-reference edits (`mod:black-scholes-merton`,
  `meth:active-currency-strategies`). Entries 671 to 681.
- Coverage: one new topic (`topic:stochastic-calculus`) and ten new neutral objectives, all covered (decision E1). The
  denominator changes from 424 to 434: 434/434 objectives covered. Outline items unchanged at 1,030/1,030; the new
  objectives have no outline items. Newly covered objectives: 10, a shortfall of 35 against the standing 45-objective
  preference (decision E2): the library-gap programme has about 20 verified objectives in total (Batch L1, the
  proposed Batch L2 and P10), L2 is frozen only after the C0 discovery task, and padding is not allowed. No backlog
  item was created.
- Sources actually read: Hull, *OFOD* 11th Global ed. (chaps. 14, 15, 19, 21, 26, 27, 28) and Wilmott, *PWOQF* 2nd ed.
  (chaps. 2, 4, 7, 10, 12, 17, 23, 25, 47, 66, 77, 78, 80). No curriculum, workbook, CQF or CAIA text was used or cited.
- Numerical scripts: five new (`stochastic-calculus-checks.py`, `numerical-pricing-checks.py`,
  `exotic-option-checks.py`, `volatility-mismatch-hedging-check.py`, `kelly-check.py`) and one extended
  (`inference-simulation-checks.py`); `make examples` now runs 111 scripts. Every predetermined acceptance range
  (as corrected for R2 and R3 before running) passed without changing a seed or
  tolerance. Failures during development were in checks of my own beyond those criteria, recorded under P2 and P3.
- Repository checks (2026-10-21): `make source-check` passed (lock, lint, format, compendium checker 0 problems,
  coverage 0 problems, 36 tests, 111 scripts); `make pdf` built 430 pages with no overfull boxes and no undefined
  references or citations. One underfull box (badness 2277) in the first paragraph of
  `common-toolkit/statistical-inference.tex` is pre-existing: a build of `2b89791` in a temporary worktree shows the
  same box with the same badness. The first PDF build failed on a bracket inside an entry's optional title
  (`$[W]_T=T$`); the title was reworded. Rendered pages of the three new topic files and the edited entries were
  inspected.
- Limits: all examples are synthetic and test the methods under their models, not markets. Hull and Wilmott are cited
  for papers that were not read (Longstaff-Schwartz, Andersen-Broadie, Broadie-Glasserman-Kou, Kemna-Vorst, Carr,
  Henrard). Editorial coverage only; human review of the ten entries is outstanding. Nothing was committed.

**Post-implementation audit corrections, 21 October 2026.** An audit of the uncommitted Batch L1 (findings L1-F1 to
L1-F5) reran the six affected scripts and both checkers, all passing, and found mathematical assumptions the checks did
not cover. The counterexamples were reproduced before any edit, and the file hashes matched the audited state. The owner
authorised the necessary changes to the affected examples and acceptance criteria for P3-P5, as recorded below. No seed was changed and no tolerance loosened; the results
recorded above are kept as the history of the first implementation.
- L1-F1, `res:kelly-growth-optimal-fraction`. The daily-rebalancing check ran at $f=0.75$, 1.5 and 3 and called the
  80-node quadrature value exact. For $f>1$ the one-day gross factor $(1-f)e^{r\Delta t}+fR$ is nonpositive when
  $Z\le-87.21$ ($f=1.5$) or $Z\le-32.20$ ($f=3$), probabilities of about $10^{-1654}$ and $10^{-227}$: not zero, so
  $E[\ln W]$ is undefined, and the quadrature nodes and the 20,000 paths simply missed the tail. The earlier biases
  $-8.9\times10^{-7}$ and $-1.00\times10^{-4}$ at $f=1.5$ and 3 are therefore withdrawn. The script now shows the
  negative gross factor for both levered fractions, checks that $f=1$ (no trade) gives $\mu-\tfrac12\sigma^2=g(1)$ to
  $10^{-12}$, and tests daily rebalancing at $f=0.25$, 0.5 and 0.75 with the same seed 20261042 and criteria:
  quadrature 0.033751, 0.045001, 0.053750 a year; simulated 0.03389 (s.e. 0.00011), 0.04529 (0.00022), 0.05418
  (0.00033); biases $+8.74\times10^{-7}$, $+6.94\times10^{-7}$, $+2.79\times10^{-7}$; refinement ratios 0.500. New
  convergence criterion: 40-, 80- and 160-node rules and adaptive `scipy.integrate.quad` agree within $10^{-10}$ and
  within 1/1,000 of the bias (largest difference $3.0\times10^{-14}$). The continuous leveraged identities and exact
  sampling are unchanged. The entry's Conditions, Practice and Pitfalls explain why continuous rebalancing keeps wealth
  positive and discrete leveraged rebalancing needs a ruin or margin model.
- L1-F2, `res:delta-hedging-volatility-mismatch`. The Conditions had dropped $\Gamma^i\ge0$ from the claim that
  $\sigma>\tilde\sigma$ gives the implied-volatility hedge a positive total. Restored in Statement, Conditions and
  Pitfalls; a deterministic check and Practice item add a unit cash-or-nothing call ($S_0=120$, $K=100$, $r=5\%$,
  $q=0$, $T=1$): 0.8141 at 20 percent and 0.6980 at 30 percent, $V^a-V^i=-0.1160$; gamma $+0.00071$ at $S=80$ and
  $-0.00047$ at $S=120$, matched by a finite difference. The vanilla simulation and its results are unchanged.
- L1-F3, `meth:asian-option-valuation`. Hull's text layer, p. 626, reads "tend to be less expensive than regular
  options" (rechecked); the entry had written "are cheaper". It now quotes Hull, says that averaging moves the forward
  as well as the dispersion, and keeps the AM-GM ordering. A deterministic negative-carry check ($S_0=100$, $K=60$,
  $r=2\%$, $q=8\%$, $\sigma=20\%$, 12 dates excluding $S_0$): vanilla 33.5611, geometric Asian 35.7601, arithmetic at
  least $e^{-rT}(E[S_{\text{ave}}]-K)=36.0876$. The positive-carry Practice item now says "with these inputs".
- L1-F4, `def:brownian-motion-quadratic-variation`. Pitfalls wording: variance is proportional to elapsed time and
  standard deviation to its square root. No check changed.
- L1-F5, `meth:digital-option-valuation`. The example said the hedge "reverses" across the strike; the one-day delta
  is 0.2530, 0.2533 and 0.2525 at 99.9, 100 and 100.1, positive throughout. The text now says the hedge changes size,
  not sign, while gamma changes sign near the strike; a deterministic check was added. It draws no random numbers, so
  the seed sequence of the Monte Carlo checks is unchanged.
- Objectives unchanged: the same ten, all covered; 434/434 objectives and 1,030/1,030 items. Coverage example strings,
  entry-evidence reviews and the pathway summaries for these entries were updated to match.

## Library gap-filling, Batch L2, 21 October 2026

**Starting state.** Branch `codex/library-gap-batch-l2`, created from `c688d54` on `codex/library-gap-batch-l1`
(L1 commit `5e0578e`, then the C0 and corrected L2 proposal `c688d54`); the working tree was clean and no newer work
was found. The 27 files of `5e0578e` were confirmed by count; the earlier audit's per-file manifest is not in the repository
or the session scratchpad, so the per-file byte matches were not re-established here. Coverage before: 434/434 objectives and 1,030/1,030 outline
items. Scope fixed by the owner on 2026-10-21 (decisions L2-D0 to L2-D6:
local only; P6-P9 and P11a-c; the rate-tree CVA as an explicitly labelled original derivation; P10 deferred to L3; both
optional Hull extensions; about 11 objectives). Before any L2 script was written, two criteria were corrected with the
owner's authorisation before implementation: P8's requirement that every tranche's
finite-versus-large-pool gap shrink from 250 to 1,000 names (counterexample reproduced: in pool-loss units
$6.2278\times10^{-6}$, $1.0587\times10^{-5}$, $5.0830\times10^{-6}$ for a 0.2-2 percent tranche) became a reported
result; P9's mean fitted GPD shape over 500 samples became a diagnostic (reproduced: 0.237276, error 0.012724 against
3 s.e. 0.010503). Delegation to other models named by the implementation skill was not available in this session; the
work was done directly.

**P6, short-rate and forward-rate models** (`compendium/rates-credit-mortgages/arbitrage-free-valuation.tex`: new
`mod:affine-short-rate-models` and `mod:hjm-forward-rate-models`; `mod:term-structure-models-simulation` extended).
- Read: Hull, *OFOD* 11th Global ed. (git-ignored copy, SHA-256 `8bc6e2f0…b482`), chap. 29, secs. 29.2-29.3 (pp.
  697-702), chap. 31 (pp. 719-731), chap. 32, secs. 32.1-32.5 (pp. 732-741) and p. 747, chap. 33, secs. 33.1-33.2
  (pp. 755-764); Wilmott, *PWOQF* 2nd ed., chap. 30, secs. 30.6-30.8 (pp. 515-520), chap. 31 (pp. 525-531), chap. 37,
  secs. 37.1-37.13 (pp. 609-619); the Handbook (Fabozzi, 9th ed., SHA-256 `ece05686…b19f`), chap. 37, pp. 855-864.
  Initial source candidates were Hull chaps. 31-33 and Wilmott chaps. 30-31 and 37; Hull sec. 29.2 was added for backward-looking
  rates. Not read: `gap-rates-backward-term-rates` (not held; Further reading).
- Discrepancies. The source review asked whether Handbook chap. 37 (pp. 859-862) describes calibrating Monte Carlo paths by a
  drift adjustment. It does not: it says that in an HJM model the curve is an input, so simulated paths reproduce zero
  prices "on average" (p. 863), and prefers a calibrated LIBOR market model for MBS. The extension of
  `mod:term-structure-models-simulation` therefore rests on Wilmott's yield-curve fitting (chap. 31, a time-dependent
  drift chosen to match market discount factors) and Hull's Black-Karasinski and shifted forms; the Handbook is cited
  only for the "on average" statement. Wilmott's CIR positivity condition ($\eta>\alpha/2$ in his notation) is Hull's
  $2ab\ge\sigma^2$; Hull adds that otherwise the rate "occasionally touches zero" (p. 724). The decomposition
  $r=x+\alpha$ with $\alpha=F+\tfrac{\sigma^2}{2a^2}(1-e^{-at})^2$ and the variance of $\int x$ are standard
  derivations, not printed in either source; they are stated as Interpretation and checked (the mean rate from Hull's
  $\theta$ by quadrature equals the closed form to $10^{-10}$).
- Data: GSW Svensson parameters for 2026-09-30 from `feds200628.csv` (`fed-gsw-data`; file SHA-256
  `72864350…335c`, git-ignored). The six parameters are written in the script, which rereads the row and compares
  the published SVENY01-SVENY30 (largest gap $4.75\times10^{-5}$ percentage points, inside the 4-decimal rounding)
  when the file is present.
- Checks (`notes/artefacts/short-rate-models/short-rate-model-checks.py`; seeds 20261061 Hull-White, 20261062 CIR exact,
  20261063 CIR Euler against exact, 20261064 caplet, written in the script before its first run). The first attempt
  stopped before any statistical check: under `-W error` an unclosed file and a SciPy `IntegrationWarning` from
  quadrature tolerances at $10^{-14}$ relative were raised (coding errors; the file is now closed and quadrature
  tolerances are $10^{-12}$ relative). The complete run then passed every predetermined criterion:
  - Vasicek 0.846849 reused; CIR five-year zero 0.835234, which solves the bond PDE (residual $2\times10^{-10}$).
    Exact non-central chi-square paths (200,000): 0.835325 at $h=1/8$ and 0.835319 (s.e. 0.000104) at $h=1/16$, where
    halving changed the price by $5.6\times10^{-6}<0.1$ s.e.; $z=+0.82$ (criterion 3 s.e.). Exact minimum
    $2.3\times10^{-4}$. With $\sigma=25$ percent (Feller fails), untruncated monthly Euler went negative on 7,052 of
    10,000 paths; exact sampling's minimum was $1.2\times10^{-10}$.
  - Hull-White ($a=0.1$, $\sigma=1$ percent, illustrative): zero prices with Hull's $\theta$ integrated numerically in
    Wilmott's eq. (31.2) equal the GSW discount factors to $2\times10^{-16}$ (criterion $10^{-10}$). Exact joint
    sampling of $(x,\int x)$ on 100,000 paths: largest $|z|$ 1.16 (at 8 years) over the 30 maturities (criterion 4
    s.e.). Trapezoid diagnostic: the 30-year discount factor moved by $1.5\times10^{-6}$ from monthly to half-monthly
    (0.1 s.e. is $2.4\times10^{-5}$), so the trapezoid result is usable but was not needed. 0.85 percent of paths have
    a negative short rate at 30 years.
  - HJM: the numerically integrated drift with constant volatility equals $\partial F/\partial t+\sigma^2t$ at 1, 5
    and 12 years, and with $\sigma e^{-a(T-t)}$ reproduces Hull's $\theta$, both to $10^{-10}$.
  - Forward market model: an at-the-money caplet on the year-5 to year-6 annual forward, $\Lambda=20$ percent, 100,000
    paths under the rolling spot measure with monthly sub-steps: 70.023 bp (s.e. 0.388) against Black's 70.195 bp,
    $z=-0.44$; the rolled numeraire reprices the six-year zero ($z=+0.22$).
- Objectives: `objective:apply-affine-short-rate-models` and `objective:explain-hjm-drift-forward-market-model`
  (`topic:arbitrage-free-bond-valuation`, planned batch 8), covered. The extension adds no objective.

**P7, counterparty exposure and xVA** (new topic file `compendium/corporate-credit-capital/counterparty-xva.tex`:
`def:counterparty-exposure-measures`, `meth:credit-valuation-adjustment`, `def:wrong-way-risk`; `meth:risky-bond-cva`
extended under decision L2-D3).
- Read: Hull, *RMFI* 6th ed., chap. 18 (pp. 393-411); Hull, *OFOD*, chap. 9 (pp. 216-226) and sec. 24.7 (pp. 571-577;
  chap. 9 points to chap. 24 for the calculation); Gregory, *The xVA Challenge*, 3rd ed. (Wiley
  2015, ISBN 978-1-119-10941-9, owner's library, SHA-256 `b2b005d1…f394f`, printed = PDF $-27$; new source
  `gregory-xva-challenge-2015` and reading note), secs. 7.1.6-7.4.4, 11.2-11.3.7, 14.2.3-14.3.1, 14.6.3-14.6.5, 15.2.1
  and 17.1-17.4.2. Not read: Gregory chap. 16 (MVA, KVA; those terms rest on Hull and RMFI), chaps. 10 (exposure
  simulation, contents only) and the capital chapter 8 (pre-reform; P10 is deferred to L3). For L2-D3, the tree
  (Handbook chap. 36, pp. 831-838) and RMFI's CVA formula (pp. 395-396) were reread before the extension was written.
  Smith (2017) is not held and was not read.
- Discrepancies. OFOD's Example 24.6 defines $v_i$ to include $1-R$ (92.67, 130.65) and RMFI's Example 18.3 does not
  (132.38, 186.65); both give CVA 5.77 (reproduced). Gregory signs CVA negative. Gregory and Hull describe the regulators'
  alpha multiplier; it is not used here, pending the Batch L3 currency review.
- Checks (`notes/artefacts/counterparty-xva/counterparty-xva-checks.py`; seeds 20261071 wrong-way Monte Carlo,
  20261072 swap paths, 20261073 PFE bootstrap, written before the first run). The first complete run passed every
  predetermined criterion:
  - Reproduced: Gregory's normal EE and PFE (2.1666 and 6.6527; 2.7912 and 11.3054) and his square-root CVA (0.1999%,
    0.1929% exact, 0.1922% averaged); the gold forward in both books.
  - Wrong-way example (200,000 draws): quadrature 0.03253, 0.02097, 0.01197, 0.00550, 0.00159 at $\rho=-0.5$ to 0.5,
    each within 3 s.e. (Monte Carlo 0.03206 s.e. 0.00039, 0.02055 0.00030, 0.01185 0.00021, 0.00536 0.00013, 0.00161
    0.00006); independent value $0.01196827$ to $10^{-10}$; strictly decreasing.
  - Swaps under Hull-White on the GSW curve (40,000 paths; same model and curve as P6): $V(0)=2.8\times10^{-15}$; the
    discounted ex-coupon value matches the curve's forward value at five dates ($|z|\le1.51$); EE peaks at 1.82 at
    1.96 years (interior); netting dominance holds on every path and date; 97.5% PFE at the peak 7.93 (bootstrap s.e.
    0.053).
  - Collateral (two-way cash, zero threshold and MTA, no IM, $C(t)=V(t-\delta)$, $\delta=10/252$): $E_c=E$ on the nine
    daily dates before $\delta$; the one-way variant never exceeds $E$; $E_c\le|V(t)-V(t-\delta)|$ on every path.
    Payment crossings: exposure dates are mid-month, and the script asserts that no payment falls in $(t-\delta,t]$ for
    the 5- and 10-day lags. Four 20-day windows (12.5, 24.5, 36.5 and 48.5 months) cross an annual payment, so those
    dates are left out of the lag diagnostic for all three lags (55 common dates). Diagnostic: mean collateralised EE
    0.0870, 0.1232 and 0.1746 at 5, 10 and 20 days, 6.1, 7.2 and 8.1 percent above $\sigma_{\Delta V}/\sqrt{2\pi}$ on
    average. On 52,866 path-dates the bank had posted and $V$ turned positive; mean $\mathrm{EE}_c$ never exceeded EE.
    CVA (hazard 2%, $R=40\%$): 0.0601 uncollateralised and 0.0066 collateralised per 100 notional;
    $E[D(0,t)E(t)]-P(0,t)\mathrm{EE}(t)$ up to 0.0445.
  - Rate tree (original derivation): calibrated rates match Exhibits 36-6 to 36-8; node-weighted and pathwise CVA of
    an original 5% four-year bond (hazard 1.5%, $R=40\%$ of par) both 3.296402, to $10^{-10}$; a default-free floater is
    at par at every node; the discount margin of a 50 bp risky floater (hazards 1-2.5%) is 112.07 bp and reprices the
    fair value 97.8397 to $10^{-8}$.
- A criterion met trivially. The predetermined criterion "as $\sigma\to0$ the tree CVA tends to the forward-rate calculation" holds to
  $10^{-15}$ at every volatility (0.2, 0.1, 0.01, $10^{-4}$), because for a bond whose exposure is linear in the tree
  values the state-price sum of value plus coupon is the curve value of the remaining flows. The criterion therefore
  confirms the implementation but does not test convergence. A check of my own was added after the first run to show
  where volatility matters: an at-market four-year payer swap on the same tree has CVA 0.0426, 0.0518 and 0.0680 at
  $\sigma=10^{-4}$, 10 and 20 percent (criterion: strictly increasing). The entry states the identity and the swap
  result; it does not attribute a volatility effect for bonds to any source.
- Objectives: `objective:measure-counterparty-exposure`, `objective:calculate-derivative-cva` and
  `objective:assess-wrong-way-risk` (`topic:credit-models`, planned batch 8), covered. The reading showed wrong-way
  risk as a separate idea (its own chapter in Gregory, a section in RMFI, conditional exposure and its own models), so
  three new objectives were used. The tree extension adds no objective.

**P8, default correlation** (new topic file `compendium/securitised-structured-credit/default-correlation.tex`:
`mod:gaussian-copula-default-correlation`, `meth:tranche-loss-base-correlation`; a See also link added to
`meth:credit-liquidity-tail-risk`, whose WCDR formula is linked, not restated).
- Read: Hull, *OFOD*, secs. 24.8-24.9 (pp. 577-582) and 25.8-25.11 (pp. 599-611); Hull, *RMFI*, secs. 9.5-9.6.3 (pp.
  202-213); Basel Framework CRE31 (all paragraphs, with the CRE31.5-31.6 formula images rendered and read) and CRE99.1-99.3
  with Table 1, versions effective 1 January 2023 (last updated 27 March 2020, status current), retrieved from bis.org on
  2026-10-21 (new source `basel-framework-cre-2026` and reading note; HTML copies in the git-ignored
  `reading_materials/library-gap-l2-20261021/`). The first request for `chapter/CRE/31.htm` returned the CRE index
  page; the chapter was fetched with explicit in-force and publication dates. Not read: Li (2000), Vasicek (1987),
  `wide-nelsen-copulas` (Further reading).
- Checks (`notes/artefacts/default-correlation/default-correlation-checks.py`; seed 20261081, inputs PD 2%, rho 0.3,
  LGD 60% and the CDX tranches fixed before the first run). The first attempt stopped before any statistical check:
  NumPy's Gauss-Hermite rule raised a divide-by-zero warning when the node count was doubled past about 150, and the
  near-step conditional binomial integrand had not converged at 128 nodes (coding/method issue). The integration was
  changed, within the predetermined "adaptive quadrature or nodes doubled" rule, to composite Gauss-Legendre on [-10, 10] with
  panels doubled until the change is below $10^{-10}$ (at most 640 nodes); an adaptive-quadrature cross-check of the
  3-7% tranche agrees to 12 decimals. No seed, input or tolerance changed. The complete run passed every criterion:
  - Reproduced: Hull's basket (86.7380%, 0.00344%); Example 25.2 ($A=4.2845$, $B=0.0187$, $C=0.1497$, 347.8 bp
    against 4.2846, 0.0187, 0.1496 and 348 bp, within the 5e-4 and nearest-basis-point tolerances); RMFI Table 9.5 cells
    (0.0062, 0.4168, 0.9699, 0.3644, 0.0799 against 0.006, 0.417, 0.970, 0.364, 0.080); Example 9.2 (0.12824); CRE99
    Table 1 corporate risk weights at ten PDs from the CRE31.5 formula, largest gap 0.0048 points (82.06% at 1%).
  - The IRB conditional default rate equals the WCDR to $10^{-12}$ (0.140273 at PD 1%, $R=0.1928$; 0.190259 at 2%).
  - Large-pool tranche losses sum to 0.012000000000000. Exact finite pools converge and also sum to PD x LGD. The
    1,000-name simulation (50,000 scenarios) is within 3 s.e. of the exact value for every tranche ($z$ from $-1.71$ to
    $+1.82$).
  - Reported, not tested (L2 freeze correction): exact minus large pool at 250, 500 and 1,000 names is $-1.58$,
    $-0.78$, $-0.39\times10^{-4}$ (0-3%), $+0.98$, $+0.48$, $+0.24\times10^{-4}$ (3-7%), and similarly halving for the
    other tranches. For these tranches the gaps did shrink monotonically; the freeze counterexample (a 0.2-2% tranche)
    shows that this is not guaranteed.
  - Base correlation on a synthetic equal mixture of $\rho=0.1$ and 0.6 (checks of my own, fixed before running):
    base correlations reprice every 0-$d$ loss to $9\times10^{-18}$ and their differences reproduce every tranche;
    reported: base correlations 0.3347 to 0.5284; two compound correlations for 3-7%; a 4-8% tranche at 0.001202 by
    interpolated base correlation and 0.001423 by linearly interpolated 0-$x$ loss against 0.001242; 0.25%-wide
    tranches from interpolated base correlations break the decreasing-rate condition three times (largest
    $1.8\times10^{-5}$). Linear interpolation of the loss curve was worse than base correlation here; the entry
    reports Hull's recommendation (interpolate the loss curve with the concavity imposed) without claiming the crude
    linear version is better.
- Objectives: `objective:model-default-correlation-gaussian-copula` and `objective:value-tranches-base-correlation`
  (`topic:securitisation`, planned batch 8), covered.

**P9, extreme value theory** (new `meth:extreme-value-tail-estimation` in
`compendium/portfolio-construction-risk/risk-models.tex`; the Pitfalls sentence of `meth:var-es-estimation-methods`
now links to it).
- Read: Hull, *RMFI*, sec. 8.4 (pp. 170-172) and secs. 12.3-12.6.1 (pp. 266-276); McNeil, Frey and Embrechts,
  *Quantitative Risk Management*, 1st ed. (Princeton 2005; owner's library, SHA-256 `a27c34f4…6c7d`, printed = PDF
  $-16$; new source `mcneil-frey-embrechts-qrm-2005` and reading note), secs. 7.1-7.1.2 and 7.2.1-7.2.6 with Example
  7.29; Wilmott, sec. 19.8 (pp. 339-341).
- Source gap corrected. The initial inventory listed `s7-qrm`, `w2-mcneil-frey` and `wide-embrechts-extremal` as not held. A
  library search during the package found the 2005 first edition of QRM (the catalogue key is the 2015 revised
  edition, which is not held), so it is registered under its own key and cited. RMFI does not give the Hill estimator;
  QRM's eq. (7.23) supplies it. Hill (1975), `w2-hill-estimator`, could not be obtained (Project Euclid answered the
  scripted request with a bot-protection page); McNeil and Frey (2000), Embrechts et al. (1997) and the 2015 QRM
  were not read. All four are Further reading.
- Definition. The estimator fixed before the first run uses $H_k$ with the $(k+1)$-th largest observation as threshold; QRM's standard form uses the
  $k$-th and notes that some versions use the $(k+1)$-th. The latter form was kept; it makes the Rényi benchmark exact.
- Checks (`notes/artefacts/extreme-value/extreme-value-checks.py`; seeds as listed in the script, fixed before the first
  run). First complete run: every predetermined criterion passed. Pareto: mean $H_k$ 0.25046 (s.e. 0.00035), s.d. 0.015699
  against 0.015811 (within 5%). $t_4$ functional 0.3488984 by quadrature; $n=10^6$ Hill 0.34961 (s.e. 0.00140, within
  3 s.e.). Exact GPD ($k=250$): ML $\xi=0.21563$, $\beta=0.91990$, score $-6.8\times10^{-14}$ and 0; log-likelihood
  $-283.0351887074$ against SciPy's $-283.0351887885$. POT formulas for a Pareto tail exact to $8.9\times10^{-16}$.
- A check of my own failed on the first run and was diagnosed. Reproducing RMFI's example with the printed
  $\beta=110.46$, $\xi=0.354$ gave 99.9% and 99.97% VaR of 1,094.31 and 1,756.66 against the printed 1,094.6 and
  1,757.4 (ES 1,777.29 against 1,778.1). RMFI's own exponent reads $-1/0.3545$ (p. 274): the book computed with the
  unrounded Solver estimate. The cause is print rounding, not the formula. The check was restated after diagnosis: it
  infers $\xi$ from the printed 99.9% VaR (0.35413, which rounds to 0.354) and requires that single value to reproduce
  the other six printed figures to their printed precision. It passes.
- Diagnostics, reported only (L2 freeze correction for the first): ML shape over 500 exact-GPD samples of 250 (seed
  20261094) 0.236875 (s.e. 0.003799), $-0.0131$ from 0.25; the freeze reproduction with planning seed 20261021 gave
  0.237276. Population GPD fit to $t_4$ excesses at the 95th percentile $\xi=0.1917$, $\beta=0.8640$. On one
  $n=5{,}000$ $t_4$ sample: Hill 0.3391, GPD 0.2002; 99%/99.5% VaR 3.5793/4.3992 (true 3.7469/4.6041), ES
  4.9580/5.9832 (true 5.2206/6.3248). Hill bootstrap intervals (200 samples, 1,000 resamples) covered 0.348898 in 190
  and 0.25 in 0 of 200; GPD shape interval [0.0231, 0.3339]. Threshold sensitivity at 90, 95, 97.5 and 99%: Hill 0.3968,
  0.3391, 0.3078, 0.2814 against functionals 0.4161, 0.3489, 0.3129, 0.2866; GPD 0.1695, 0.2002, 0.2296, 0.2166 against
  0.1626, 0.1917, 0.2104, 0.2258. Two-step on GARCH(1,1)-$t_6$ (the generator of `var-backtest-check.py`, own seed):
  99% conditional VaR 0.01368 (true 0.01372), ES 0.01687 (true 0.01761); 99.5% VaR 0.01588 (0.01619), ES 0.01910
  (0.02042); residual GPD shape 0.0092 (the $t_6$ asymptotic value is 1/6). Runtime about 25 s.
- No empirical EVT claim (backlog B9). The two-step method is taught inside the same entry; the reading did not show
  it to be a separate idea, so one objective: `objective:estimate-tail-risk-extreme-value`
  (`topic:market-risk-measurement`, planned batch 8), covered.

**P11a, correlation and independence tests** (new `meth:correlation-independence-tests` in
`compendium/common-toolkit/statistical-inference.tex`).
- Read: OpenStax, *Introductory Statistics* 2e, secs. 11.3 and 12.4 (fetched renderings, 2026-10-21; the fetch tool
  returns a summary with short quotations, not the full text, which limits the record to the formulas, conditions
  and example numbers it reported); NIST Dataplot, "Rank Correlation Independence Test" (new source
  `nist-dataplot-rank-correlation`). The initial source candidate was `statistical-methods-handbook` (the NIST e-Handbook) for rank
  correlation; a search found no Spearman section in it, and the Dataplot reference page was used instead. Not read:
  Conover (1999).
- Checks (`notes/artefacts/inference-simulation/correlation-independence-checks.py`; seeds 20261101 size study,
  20261102 formula data, 20261103 overlap diagnostic, fixed before the first run). All criteria passed on the first
  run: OpenStax $p=0.02615$ (prints 0.026) and six critical values; Example 11.6 $\chi^2=12.9909$, df 4, $p=0.01132$;
  SciPy agreement to $10^{-12}$ (Pearson $p$-value, Spearman with and without ties, chi-square without continuity
  correction); transforms (strictly increasing invariance, sign change for one decreasing transform, invariance for
  two, ties included); the shortcut differs with ties (0.930070 against 0.928832) and agrees without. Size, 20,000
  replications of $n=30$: Pearson 4.84%, Spearman ($t$ approximation, the predetermined test) 4.95%, both within
  $5\pm0.5$; NIST's normal approximation 4.78% (reported). Diagnostic of my own: an AR(1) signal ($\phi=0.95$) and
  independent returns, $T=500$, 2,000 replications: rejection 6.5% with one-day and 62.9% with overlapping 20-day
  returns.
- Objective: `objective:test-correlation-independence` (`topic:statistical-inference`, planned batch 8), covered. No
  outline item maps to it (the 2026/2027 outlines dropped this module).

**P11b, mean-CVaR optimisation** (new `meth:mean-cvar-optimisation` in
`compendium/portfolio-construction-risk/portfolio-construction-models.tex`).
- Read: Rockafellar and Uryasev, "Optimization of Conditional Value-at-Risk" (`s6-cvar`), the author preprint dated 5
  September 1999 (26 pp.) at the catalogue's link, retrieved 2026-10-21 (SHA-256 `34aff216…42f4`; new reading note).
  The catalogue lists the 2000 *Journal of Risk* article; locators are to the preprint. Not read: Rockafellar and
  Uryasev (2002) for general distributions.
- Checks (`notes/artefacts/portfolio-construction/mean-cvar-check.py`; problem and seeds fixed before the first run;
  seeds 0-9 had been used in a planning reproduction and are not unseen data). The first run used HiGHS dual simplex
  with tight tolerances and was stopped after several minutes without output (100,000-scenario LPs); timing one LP
  showed interior point with crossover at 10 s against 32 s for dual simplex, with the same solution, so the solver
  was switched (no criterion changed). In the complete run every predetermined criterion passed: LP objective equals the
  fractional-tail-mass CVaR (0.1678292649 at $n=10{,}000$; 0.1961604624 at $n=250$, 97.5%, tail mass 6.25); the 1%
  grid on the feasible line ($w_1=w_3$) has best 0.167834 against the LP's 0.167829 (allowance 0.006414); normal
  equivalence against the population portfolio (0.321429, 0.357143, 0.321429): largest gap 0.0078 at 100,000
  scenarios (criterion 0.025), mean 0.0135 at 10,000 and 0.0035 at 100,000. Reported: a negatively skewed third asset
  (skewness $-3.63$) moves weights from (0.3388, 0.3224, 0.3388) to (0.2740, 0.4520, 0.2740), CVaR 0.13699 to 0.12496.
- A check of my own failed and was diagnosed: reproducing Table 3 with a $5\times10^{-7}$ tolerance gave 0.4520113,
  0.1155732, 0.4324155 against the printed 0.452013, 0.115573, 0.432414. The printed weights' mean return is
  0.0109999956, so they are a numerical QP solution that misses the constraint by about $4\times10^{-9}$; the exact
  KKT solution is the optimum. The tolerance was widened to $5\times10^{-6}$ with the constraint error reported. Table
  4's VaR and CVaR reproduce to $5\times10^{-6}$. Runtime about two minutes.
- Objective: `objective:construct-minimum-cvar-portfolio` (`topic:portfolio-risk-return`, planned batch 8), covered.

**P11c, buying on margin** (new `meth:margin-purchase-leverage` in
`compendium/portfolio-risk-financing/securities-lending.tex`).
- Read (current texts, retrieved 2026-10-21): 12 CFR 220.4 and 220.12 from the eCFR versioner (title 12 up to date as
  of 19 October 2026, last amended 2 October 2026; the first unauthenticated request returned an error asking for
  compression, repeated with it); FINRA Rule 4210(b)-(d) on finra.org, version from 4 June 2026 (unchanged since the
  17 October reading). New reading notes for `ecfr-12cfr220` and `finra-rules-2026`; the two `sources.tex` entries
  now record the reread. The leverage, levered-return and call-price formulas are derivations (Interpretation) with
  the assumptions corrected after the L2 audit. The 4210(g) portfolio-margin text was not read, and a draft clause
  about portfolio margining was removed from the entry for that reason.
- Checks (`notes/artefacts/short-term-funding/margin-purchase-check.py`; deterministic, original inputs). All passed on
  the first run: static call prices 26.6666666667 (long, 25%) and 46.1538461538 (short, 30%) equal the roots to
  $10^{-12}$; the 30% leg binds (13.85 a share against the \$5 floor). Long ledger (6.5% act/360, \$0.40 dividend
  credited 15 April): loan 20,235.0219, call price 26.980029 (+0.313363 against static). Short ledger (2% rebate, 0.5%
  borrow fee, dividend owed, \$15 commission): credit 59,878.3333, call price 46.060256 ($-0.093590$). The levered
  return identity holds to $10^{-12}$ (16.00% asset, 28.6507% equity; at \$34, $-14.00$% and $-31.30$%).
- Objective: `objective:calculate-margin-leverage-call-price` (`topic:equity-securities-markets`, planned batch 8),
  covered.

**Decision L2-D5, two optional Hull extensions** (no objective).
- Read: Hull, *OFOD*, sec. 21.3 (pp. 480-483, known dividends in trees, Example 21.5), sec. 15.12 (pp. 360-363,
  early exercise of American calls and Black's approximation), secs. 11.5-11.6 and 11.8 (pp. 258-263), and sec. 29.3
  (pp. 699-705, already read for P6). C0 had located sec. 21.3 without reading it; the passages were read before
  writing.
- `meth:multi-period-binomial-valuation`: known dollar dividends via the $S^*$ tree and Hull's early-exercise
  conditions. `meth:black-model-rates-currencies`: the receiver swaption, payer-receiver parity and the callable bond
  as a straight bond less a receiver swaption (the last as an Interpretation of Business Snapshot 29.2).
- Checks (`notes/artefacts/option-valuation/dividend-tree-swaption-checks.py`; seed 20261121). Example 21.5:
  4.4404, 4.2084, 4.2143 at 5, 50 and 100 steps (printed 4.44, 4.208, 4.214). Original call (bound 0.1124): with
  $D=0.05$ no node exercises and American equals European (4.100852); with $D=1.50$ the American is 3.8544 against
  3.3125 and all exercise falls at 0.4545, the last step before the ex-date. Example 29.4 payer 2.1908; receiver
  2.2028; parity to $10^{-12}$; the call-at-par and receiver payoffs agree on 1,000 random curves (largest gap
  $2\times10^{-14}$). Diagnostic: Black's approximation first printed 3.3119 because the $t_n$ leg wrongly deducted the
  dividend (my coding error, corrected before use); correctly computed it is 3.9144, above the tree's 3.8544, because
  it puts the volatility on the whole stock price rather than on $S^*$ (Hull, p. 360, n. 13). It is reported, not
  tested.

**Batch completion.**
- Scope delivered as frozen: P6, P7, P8, P9 and P11a-c complete; the rate-tree CVA and risky floater (L2-D3) and the
  two optional Hull extensions (L2-D5) done; P10 deferred to Batch L3 (L2-D4). No package is partial. Eleven new entries, as estimated
  (`mod:affine-short-rate-models`, `mod:hjm-forward-rate-models`, `def:counterparty-exposure-measures`,
  `meth:credit-valuation-adjustment`, `def:wrong-way-risk`, `mod:gaussian-copula-default-correlation`,
  `meth:tranche-loss-base-correlation`, `meth:extreme-value-tail-estimation`, `meth:correlation-independence-tests`,
  `meth:mean-cvar-optimisation`, `meth:margin-purchase-leverage`) in two new topic files (`corporate-credit-capital/counterparty-xva.tex`,
  `securitised-structured-credit/default-correlation.tex`) and four existing ones. Extended: `mod:term-structure-models-simulation`,
  `meth:risky-bond-cva`, `meth:multi-period-binomial-valuation`, `meth:black-model-rates-currencies`; link-only edits to
  `meth:var-es-estimation-methods` and `meth:credit-liquidity-tail-risk`.
- Coverage: eleven new objectives (P6 2, P7 3, P8 2, P9 1, P11 3), all covered, planned batch 8, no new topic; the
  denominator moves from 434 to 445, all covered. Outline items unchanged at 1,030/1,030 (no outline item maps to the
  new objectives). Newly covered objectives: 11, a shortfall of 34 against the standing 45-objective preference
  (decision L2-D6). The library-gap programme's verified new ideas are nearly exhausted; most remaining gaps are depth
  within covered objectives, which earn no count, and padding is not allowed.
- New sources registered: `gregory-xva-challenge-2015`, `basel-framework-cre-2026`, `mcneil-frey-embrechts-qrm-2005`,
  `nist-dataplot-rank-correlation`; reread and re-dated: `ecfr-12cfr220`, `finra-rules-2026`, `introductory-statistics-2023`.
  Downloaded public texts (BIS CRE31 and CRE99 pages and formula images, the Rockafellar-Uryasev preprint, eCFR XML,
  FINRA HTML) are kept in the git-ignored `reading_materials/library-gap-l2-20261021/`. The owner's library was read only.
- Sources actually read: Hull, *OFOD* 11th Global ed. (chaps. 9, 11, 15, 21, 24, 25, 29, 31-33); Hull, *RMFI* 6th ed.
  (chaps. 8, 9, 12, 18); Wilmott, *PWOQF* 2nd ed. (chaps. 19, 30, 31, 37); the Handbook (chaps. 36-37); Gregory, *The
  xVA Challenge* 3rd ed.; McNeil, Frey and Embrechts, *QRM* 1st ed. (chap. 7); Rockafellar and Uryasev (1999 preprint);
  OpenStax *Introductory Statistics* 2e (secs. 11.3, 12.4); NIST Dataplot; Basel Framework CRE31 and CRE99; 12 CFR 220;
  FINRA Rule 4210. No curriculum, workbook, CQF or CAIA text was used or cited.
- Source gaps remaining: Smith (2017) (tree-based CVA; not held, not read; the extension is an original derivation);
  Hill (1975) (Project Euclid refused scripted access); McNeil and Frey (2000), Embrechts et al. (1997), the 2015 QRM,
  `gap-rates-backward-term-rates`, `wide-nelsen-copulas`, Conover (1999), Gregory chap. 16. All are Further reading
  or are cited only through the books that were read.
- Numerical scripts: eight new (`short-rate-model-checks.py`, `counterparty-xva-checks.py`,
  `default-correlation-checks.py`, `extreme-value-checks.py`, `correlation-independence-checks.py`,
  `mean-cvar-check.py`, `margin-purchase-check.py`, `dividend-tree-swaption-checks.py`); `make examples` now runs 119.
  Every predetermined criterion, as frozen with the two freeze corrections, passed without a change of seed,
  input or tolerance. First-run failures were coding or method issues (P6 warnings, P8 Gauss-Hermite) or in checks of
  my own (P9 RMFI rounding, P11b Table 3, the D5 Black-approximation diagnostic), each recorded above with its cause;
  the P7 sigma-limit criterion holds trivially, as recorded.
- Repository checks (2026-10-21): `make source-check` passed (lock, lint, format, compendium checker 0 problems,
  coverage 0 problems, 36 tests, 119 scripts; about five minutes, of which P11b is about two). `make pdf` built 437
  pages with no overfull boxes and no undefined references or citations; the one underfull box (badness 2277, first
  paragraph of `common-toolkit/statistical-inference.tex`) is the pre-existing one recorded in L1. Rendered pages of the
  new and edited entries (printed pp. 8, 70-73, 87-88, 91-93, 98-100, 181-182, 249-250, 255-256, 283-284) were
  inspected; two short-tailed lines (a Notation formula on p. 71 and a tail-probability formula on p. 255) were moved
  into displays and the PDF rebuilt with the same results.
- Limits: all examples are synthetic or reproduce published examples, except P6's curve (GSW, a Treasury fitted
  curve, not SOFR or OIS); no empirical claim about markets. Volatility parameters in P6-P7 are illustrative. US
  margin rules and the Basel IRB formula are as retrieved on 2026-10-21. Editorial coverage only; human review of all
  eleven entries and four extensions is outstanding. Nothing pushed; no PR.

**Post-implementation audit corrections, Batch L2, 21 October 2026.** An audit of the committed Batch L2 (`cd55096`)
reran the eight new L2 scripts with warnings as errors, the 36 tests, lint, formatting and both checkers (all passing;
445/445 objectives, 1,030/1,030 items) and found four defects that those checks did not test (L2-F1 to L2-F4: three in
P7 discounting and units, one in P11c rule scope). Starting state: branch `codex/library-gap-batch-l2` at `cd55096`,
working tree clean, no newer work. The owner authorised a bounded correction pass: no seed, input or tolerance of an
existing check was changed, the objective count and batch scope are unchanged, and the results recorded above are kept
as the history of the first implementation.
- L2-F1, the Hull-White discount factor in `counterparty-xva-checks.py` (audited line 257). The script used
  $D(0,t)=P(0,t)\exp(+\tfrac12\mathrm{Var}(I_t)-I_t)$ with $I_t=\int_0^tx\,du$. Derivation: with $r=x+\alpha$ and
  $E[x]=0$, the mean short-rate integral is $\int_0^t\alpha\,du=-\ln P(0,t)+\tfrac12\mathrm{Var}(I_t)$ (the P6
  decomposition), so $D(0,t)=\exp(-\int\alpha-I_t)=P(0,t)\exp(-\tfrac12\mathrm{Var}(I_t)-I_t)$; equivalently, since
  $I_t\sim N(0,\mathrm{Var}(I_t))$, $E[e^{-I_t}]=e^{\mathrm{Var}/2}$ and only the minus sign gives $E[D(0,t)]=P(0,t)$.
  The old sign overstated every discount factor by $e^{\mathrm{Var}(I_t)}$, up to 0.29 percent at 4.96 years. P6's own
  script integrates $\alpha$ separately and uses $\exp(-\int\alpha+\tfrac12\mathrm{Var})$ for bond prices, which is
  correct, so P6 is unaffected. The fix is one helper, `disc`, used for every simulated date. Two deterministic checks
  were added: $D(0,t)$ at $I=0$ equals $\exp(-\int\alpha)$ with $\int\alpha$ by quadrature at 0.5, 1.96 and 4.96 years
  ($1.1\times10^{-16}$ relative, criterion $10^{-10}$; the old sign misses by $4.0\times10^{-6}$ to $2.9\times10^{-3}$);
  and the covariance of $(x,I)$ propagated through the simulation's own exact steps, without random numbers, has
  $\mathrm{Var}(I_t)$ equal to the closed form at every date ($3.8\times10^{-16}$ absolute, criterion $10^{-14}$, absolute
  because the closed form loses relative precision near $10^{-13}$ on the first daily dates) and $E[D(0,t)]=P(0,t)$ by
  the normal moment generating function ($1.1\times10^{-16}$). Two of my first thresholds for these new checks were
  mis-set (a relative variance tolerance on the first daily dates, and a $10^{-4}$ discrimination margin that the 0.5-year
  date does not reach, although its $4.0\times10^{-6}$ is $4\times10^4$ times the tolerance); they were reset before the
  checks were accepted, as stated in the script. Mutation check: a scratch copy with the old sign restored fails both
  new checks and still passes every original check. Corrected results (same seed 20261072, 40,000 paths): CVA per 100
  notional 0.0600863777 uncollateralised and 0.0066079387 collateralised; largest $|E[D(0,t)E(t)]-P(0,t)\mathrm{EE}(t)|$
  0.0461283797 (the audit's isolated probe gave the same three values). Originally 0.0601229105, 0.0066095777 and
  0.0444617598 (printed as 0.0601, 0.0066 and 0.0445). The forward-value $z$ values move from $-0.36$, $-1.24$, $-1.51$,
  $-1.24$, $-0.35$ to $-0.36$, $-1.24$, $-1.52$, $-1.25$, $-0.39$. The entry's displayed 0.0601 and 0.0066 are unchanged
  at four decimals; its gap becomes 0.046 (still about 2.5 percent of the 1.82 peak). EE, PFE, netting and collateral
  results do not use $D$ and are unchanged.
- L2-F2, `def:wrong-way-risk`. The Statement wrote $\mathrm{CVA}=(1-R)\sum_iE[E(t_i)\mid\tau=t_i]\,q_i$ with the
  compendium's undiscounted $E(t)$, silently inheriting Gregory's discounted EE. Gregory reread (owner's library copy,
  SHA-256 `b2b005d1…f394f`, extracted 2026-10-21): eq. (17.1), p. 380, is $-\mathrm{LGD}\sum_i\mathrm{EE}(t_i\mid
  t_i=\tau_C)\,\mathrm{PD}(t_{i-1},t_i)$; his EE "is the discounted expected exposure" (sec. 14.2.3, p. 311) and is
  discounted inside the simulation (sec. 14.2.6, p. 313). The entry now conditions $D(0,t_i)E(t_i)$ on
  $t_{i-1}<\tau\le t_i$, the event whose probability is $q_i$, states it as the date-grid approximation of
  $(1-R)E^Q[D(0,\tau)E(\tau)\mathbf 1_{\{\tau\le T\}}]$, and maps Gregory's convention. Added example and check: a
  one-year exposure of 100, PD 5 percent, $R=40$ percent and a deterministic continuously compounded rate of 5 percent
  give PV CVA 2.8536882735, not 3.
- L2-F3, `meth:credit-valuation-adjustment`. The Conditions called $\mathrm{CVA}\approx\mathrm{EPE}\times\text{spread}$
  a rough form of CVA without units. Gregory, sec. 14.2.5, p. 313: eq. (14.4) gives CVA "in the same units as the credit
  spread", a per-annum charge with an undiscounted, constant EPE (nn. 5-7); the upfront example is converted by dividing
  by the risky annuity (4.42, zero rates, n. 4): $-0.200\%/4.42=-4.52$ bp a year, against the approximation's
  $-1.54\%\times300=-4.62$ bp. The annuity formula is in Gregory's online Appendix 14B, which is not in the book and was
  not read; $(1-e^{-hT})/h$ with $h=s/\mathrm{LGD}=5\%$, $T=5$ reproduces 4.4240 (a quarterly end-point sum gives
  4.3964, which does not). The entry now distinguishes the running spread from upfront CVA and shows the conversion
  $\mathrm{CVA}_{\text{upfront}}\approx\mathrm{EPE}\times s\times A$ (Interpretation); Practice and Pitfalls were
  extended. Added checks: annuity 4.4240, 4.5183 bp, EPE 1.5416 percent (1.4907 exact), 4.6249 bp, all within 0.005 of
  the printed figures; the approximation times the annuity is 0.2046 percent upfront, within 5 percent of 0.1999, while
  read as upfront (0.0462 percent) it is about a quarter of the CVA.
- L2-F4, `meth:margin-purchase-leverage`. The Statement gave 150 percent "for a short sale of a non-exempted security".
  The retained eCFR XML of 220.12 (SHA-256 `35633db6…5b21`, title 12 up to date as of 19 October 2026) was rechecked:
  (c) applies to a nonexempted security "except for a non-equity security"; (c)(1) is 150 percent; (c)(2) is 100 percent
  when a security exchangeable or convertible within 90 calendar days is held (a long call only if listed, American-style
  and struck no higher than the short-sale price); (d) is 100 percent plus good-faith margin for an exempted or non-equity
  security. The entry now states 150 percent for the unhedged non-exempted equity short of its examples and gives both
  exceptions with a cross-reference to `mech:securities-lending-short-sale`, whose wording (pre-L2) already cites (c)
  for nonexempted equity securities. The script's docstring was qualified the same way. No number changed.
- Why the earlier checks passed. L2-F1: no check tested $D$ deterministically. The only check using it was the Monte
  Carlo forward-value test at 4 standard errors, and a bias of at most 0.29 percent of a near-zero forward value moved $z$
  by at most 0.04. The CVA figures and the discounting gap were printed, not tested. L2-F2 and L2-F3 were text: the
  wrong-way example uses unit discounting, where $D=1$ hides the convention, and the script reproduced Gregory's p. 312
  upfront figures but not his p. 313 units. L2-F4 was rule scope, which the margin script's arithmetic cannot test.
- Records updated: the two entries, the two scripts, the Gregory and `ecfr-12cfr220` reading notes, the four
  entry-evidence reviews, three coverage example or locator strings and two pathway summaries.
- Checks run (2026-10-21): `counterparty-xva-checks.py` and `margin-purchase-check.py` with `-W error`, all passing
  (the xVA output was identical before and after `ruff format`); `make lint`, `make format-check` (it reformatted one
  new line of my code first), `make check-compendium`, `make check-coverage` (0 problems; 445/445, 1,030/1,030),
  `make test` (36 passed); `make pdf` (437 pages, no overfull boxes or undefined references; the one underfull box is
  the pre-existing one; the first build stopped on two literal `\n` sequences my edit had left in the TeX, fixed before
  the recorded build), with printed pp. 92-93 and 283 rendered and inspected; pre-commit on the committed files. Reused without rerun: the other six L2 scripts
  and the 111 earlier ones, whose files are unchanged since `cd55096` and which import or read nothing that changed
  (no script refers to the two changed ones). Their results at `cd55096` (`make source-check`, 119 scripts) stand.
- Objectives unchanged: eleven new, 445/445 objectives and 1,030/1,030 outline items, editorial coverage only; the
  shortfall against 45 is still 34. Human review of the L2 entries is still outstanding. Nothing pushed; no PR.

## Library gap-filling, Batch L3, 21 October 2026

**Starting state.** Branch `codex/library-gap-batch-l2` at `a519e0c` (the L2 correction commit after `cd55096`), working
tree clean, no newer work; coverage 445/445 objectives and 1,030/1,030 outline items. Branch `codex/library-gap-batch-l3`
created from `a519e0c`. Local only. The L3 scope (P10, backlog B7) was fixed on 2026-10-21 and executed. Delegation to the models named by
the implementation skill was not available; the work was done directly.

**Method.** Each claim rests on the issuer's own text, downloaded to the git-ignored
`reading_materials/library-gap-l3-20261021/` (hashes in its `SHA256SUMS`) and read as extracted text; formula images
(CRE52, MAR50) were rendered and read. BIS chapter pages moved to a new URL scheme with in-force and publication dates;
EUR-Lex returned a bot challenge, so EU acts came from the Publications Office (CELLAR) and were found by SPARQL title
queries; the eCFR API needed a compression header; Federal Register documents came from its API and XML. Web search was
used only to find documents. In one early request the HTTP user-agent string contained the owner's e-mail address (a
connectivity probe to eight issuer sites); later requests used a generic string.

**Claims checked** (retrieval date 2026-10-21 for all; "Basel" dates are the dates by which BCBS members agreed to
implement).

| # | Claim | Issuer, locator | Jurisdiction; institutions | Published; effective/application | Status | Entry; result |
|---|---|---|---|---|---|---|
| 1 | FRTB internal models: ES at 97.5%, stress-calibrated, 10-day base scaled to liquidity horizons 10-120 days | BCBS, MAR33.3-33.5, 33.12 | Basel; internationally active banks | MAR33 version published 5 Jun 2020; effective 1 Jan 2023 | Final (Basel standard) | `meth:market-risk-limits-capital`: sentence corrected; it had implied a completed, uniform move |
| 2 | Basel market-risk standard effective 1 Jan 2023, deferred from 1 Jan 2022 | BCBS, d457 introduction (2022); GHOS press release 27 Mar 2020; MAR90.1 | Basel | Jan 2019; deferral 27 Mar 2020 | Final; deferred | same entry; Conditions added |
| 3 | EU FRTB applies from 1 Jan 2027; pre-CRR3 rules until then | Commission DR (EU) 2025/1496 Art. 1 (CRR Art. 520a), replacing DR 2024/2795 (1 Jan 2026) | EU; CRR institutions | OJ 19.9.2025; applies 1 Jan 2026 | Final; delayed twice | same entry; added |
| 4 | EU temporary FRTB relief to 31 Dec 2029, incl. 0.9 multipliers | DR (EU) 2026/1221 Art. 1 (CRR Arts 495i-495v, 495s) | EU; CRR institutions | OJ 11.9.2026; applies 1 Jan 2027 | Final; transitional | same entry; added |
| 5 | UK Basel 3.1 from 1 Jan 2027; FRTB-IMA from 1 Jan 2028, existing IMA permissions retained in 2027 | PRA PS1/26 paras 1.5, 1.23-1.24, 3.4 | UK; PRA-authorised banks, building societies, designated investment firms | 20 Jan 2026; 1 Jan 2027 / 1 Jan 2028 | Final; delayed (from 2025/2026) | same entry; added |
| 6 | US market-risk rule is 99%, 10-day VaR plus stressed VaR | 12 CFR 217.204(b)(2), 217.205(b)(1) (eCFR to 19 Oct 2026) | US; Board-regulated institutions subject to market risk rule | in force | Effective | same entry; added |
| 7 | US revised framework only proposed; 2023 proposal rescinded | OCC/Board/FDIC NPR 91 FR 14952, 14955 | US; Category I-II and significant-trading banks | 27 Mar 2026; comments to 18 Jun 2026; no final rule found to 21 Oct 2026 | Proposed | same entry and `rule:counterparty-credit-cva-capital`; added |
| 8 | SA-CCR: EAD = 1.4 (RC + PFE); RC, multiplier (5% floor), SD, MF, delta, IR buckets, SF 0.5% | BCBS CRE52.1-52.57, 52.72 | Basel; banks without IMM approval | CRE52 version effective 1 Jan 2023 | Final | new `rule:counterparty-credit-cva-capital` |
| 9 | SA-CCR Basel effective date 1 Jan 2017 | BCBS 279 sec. D, p. 3 | Basel | Mar 2014 | Final | new rule; added |
| 10 | CCR EAD feeds the credit-risk SA or IRB as the exposure | BCBS CRE51.7, 51.13 (2028 version compared: adds CCR-hedge treatment only) | Basel | 2023 version | Final | new rule |
| 11 | CVA-risk capital: separate, RWA = 12.5 x K; BA-CVA reduced K formula, DS 0.65, rho 50%, SCVA, DF, RW 0.5-12%; SA-CVA needs approval; EUR 100bn option | BCBS MAR50.1-50.16 (July 2020 revision BCBS d507 read for the DS and calibration change) | Basel | MAR50 published 8 Jul 2020; effective 1 Jan 2023 | Final | new rule |
| 12 | EU SA-CCR from 28 Jun 2021 | Reg. (EU) 2019/876 Art. 3(2) | EU | OJ 7.6.2019; 28 Jun 2021 | Effective | new rule; added |
| 13 | EU revised CVA approaches from 1 Jan 2025, exemptions kept | Reg. (EU) 2024/1623 Art. 1(198)-(199), Art. 2; Reg. 575/2013 Art. 382(4) | EU; CRR institutions | OJ 19.6.2024; 1 Jan 2025 | Effective | new rule; added |
| 14 | UK SA-CCR (and NSFR) from 1 Jan 2022 | PRA PS17/21 pp. 4, 8 | UK; PRA-authorised firms | Jul 2021; 1 Jan 2022 | Effective | new rule and `def:financial-institution-features`; added |
| 15 | UK Basel 3.1 CVA (AA-CVA, BA-CVA, SA-CVA) removes exemptions, with transition | PRA PS17/23 paras 1.8, 1.13; PS1/26 para. 1.23 | UK | 12 Dec 2023 (near-final); 1 Jan 2027 | Final, not yet effective | new rule; added |
| 16 | US SA-CCR effective 1 Apr 2020, mandatory 1 Jan 2022 for advanced approaches; alpha 1 for commercial end-users | 85 FR 4362, 4365; 12 CFR 217.132(c)(5)(iv) | US | 24 Jan 2020 | Effective | new rule; added |
| 17 | US CVA capital: simple or advanced CVA approach (advanced approaches); BA-/SA-CVA only proposed | 12 CFR 217.132(e); 91 FR 14952 | US | in force / proposal | Effective / proposed | new rule; added |
| 18 | LCR >= 100% outside stress (LCR20.4-20.5); NSFR >= 100% (NSF20.2) | BCBS LCR20, NSF20 | Basel | versions effective 15 Dec 2019 | Final | `def:financial-institution-features`; confirmed, no correction |
| 19 | LCR 100% minimum from 1 Jan 2019; NSFR minimum standard from 1 Jan 2018 | BCBS LCR90.1; BCBS 295 para. 8 | Basel | 2013 / Oct 2014 | Final | same entry; dates added |
| 20 | EU LCR from 1 Oct 2015 at 60%, 100% from 1 Jan 2018; NSFR from 28 Jun 2021 | DR (EU) 2015/61 Arts 38-39; Reg. 2019/876 Art. 3(2) | EU | 2014 / 2019 | Effective | same entry; added |
| 21 | US LCR effective 1 Jan 2015 (80%, 90%, 100% from 2017); NSFR 1 Jul 2021 for $100bn+ organisations | 79 FR 61440, 61444; 86 FR 9120 | US | 10 Oct 2014; 11 Feb 2021 | Effective | same entry; added |
| 22 | IFRS S1/S2 issued June 2023, effective for periods from 1 Jan 2024; climate-first relief; GHG amendments Dec 2025 effective 1 Jan 2027 | IFRS S1 E1, E5; S2 C1, C1B | Global standard; applies only where adopted | Jun 2023; Dec 2025 | Issued (not law) | `meth:esg-exposure-evaluation`; added |
| 23 | ISSB materiality is investor-focused (financial) | IFRS S1 paras 3, 18 | as above | | Issued | same entry; existing claim confirmed and qualified |
| 24 | TCFD monitoring passes to ISSB from 2024; TCFD disbanded after 2023 report | FSB press release 21/2023 (13 Jul 2023); TCFD 2023 Status Report p. 3 | Global | Jul and Oct 2023 | Completed | same entry; added |
| 25 | EU uses ESRS; mandatory scope after Omnibus I: > EUR 450m turnover and > 1,000 employees; transposition by 19 Mar 2027 | Dir. (EU) 2026/470 Art. 2(1), Art. 5(1) | EU; large undertakings | OJ 26.2.2026 | Final directive, awaiting transposition | same entry; added |
| 26 | UK endorsed UK SRS S1/S2 for voluntary use | DBT government response paras 1.4-1.5, 1.15 | UK | 25 Feb 2026 | Final (voluntary) | same entry; added |
| 27 | SEC climate rules adopted Mar 2024; stayed Apr 2024; defence ended 27 Mar 2025; Eighth Circuit abeyance 12 Sep 2025; rescission proposed Jun 2026 | 89 FR 21668; 89 FR 25804 (Release 33-11280); 91 FR 33296, 33299-33300; SEC letter to the Eighth Circuit, 7 May 2026 | US; SEC registrants | adopted 6 Mar 2024; never effective | Stayed; rescission proposed | same entry; added |

**Not verified** (stated precisely; nothing in the teaching text depends on them).
- FCA PS26/19 (listed issuers' sustainability disclosures referring to UK SRS): the FCA site returned a bot challenge to
  every request, so its content, dates and comply-or-explain basis are unread; the entry says only that mandatory use
  depends on separate rules such as the FCA's Listing Rules, which the government response states.
- Eighth Circuit orders after 18 May 2026 (including any ruling on Iowa's motion of 8 May 2026 to lift abeyance) and the
  SEC's planned later status report: not in the public RECAP docket; PACER was not used. The entry states the posture as
  of the SEC's June 2026 proposal and records that no final rescission appears in the Federal Register up to 21 October
  2026.
- The PRA Rulebook instrument (PS1/26 Appendix 1) and the OCC and FDIC parallel capital parts were not read; dates and
  US text come from the policy statement and the Board's part 217.
- Directive (EU) 2025/794 and Commission Recommendation 2025/1710 were found but are not used.

**Entries.** New `rule:counterparty-credit-cva-capital` (in `corporate-credit-capital/counterparty-xva.tex`; the topic
file's introduction no longer says capital is not covered, and See also links were added to the CVA and wrong-way-risk
entries). Corrected or extended: `meth:market-risk-limits-capital` (Banks item, Conditions, Pitfalls),
`def:financial-institution-features` (Liquidity item, Conditions), `meth:esg-exposure-evaluation` (Conditions). No
other backlog item was touched; no L1 or L2 calculation was reopened.

**Check** (`notes/artefacts/counterparty-xva/counterparty-capital-check.py`, deterministic, original inputs). It tests
identities independent of the hand formulas (SD and DF against numerical integrals of $e^{-0.05t}$ to $10^{-12}$; the
multiplier's value of 1 for $V-C\ge0$ and approach to the 5 percent floor; the single-bucket effective notional;
$K_{\text{reduced}}=S\sqrt{\rho^2N^2+(1-\rho^2)N}$ for $N$ equal counterparties) and the worked example: SD 3.6254, add-on
1.8127, EAD 5.3378; with 4 of cash collateral multiplier 0.5815, EAD 1.4758; default RWA 5.3378 and capital 0.4270 at an
illustrative 100 percent risk weight; DF 0.9063, SCVA 0.4147, BA-CVA requirement 0.2695, RWA 3.3692; two counterparties
$\sqrt{2.5}$ times one; US commercial end-user EAD 3.8127. First run: one failure in my own expected value (I had
pre-computed the collateralised multiplier as 0.5816; the formula gives 0.581531), corrected to 0.5815, 1.0541 and
1.4758; no formula or input changed. The script was reformatted by moving two comments.

**Objectives.** One new: `objective:explain-counterparty-credit-capital` (`topic:credit-models`, planned batch 8,
covered). FRTB, liquidity and sustainability were currency corrections to covered objectives
(`objective:set-market-risk-limits`, `objective:explain-financial-institution-features`, `objective:evaluate-esg-exposures`),
whose evidence now lists the new sources. Coverage 446/446 objectives and 1,030/1,030 outline items (no outline item
maps to the new objective). Shortfall against the standing 45: 44.

**Registry and notes.** 25 new `sources.tex` keys and reading notes (Basel, BCBS, EU, PRA, DBT, US agencies, eCFR,
SEC, IFRS Foundation, FSB, TCFD); entry evidence for the new entry and the four touched ones (plus a note on the
wrong-way-risk record); coverage evidence; two pathway notes.

**Checks run (2026-10-21).** `counterparty-capital-check.py` with warnings as errors (all pass); `make lint`,
`make format-check`, `make check-compendium` and `make check-coverage` (0 problems; 446/446, 1,030/1,030) and `make test`
(36 passed). `make pdf`: 441 pages, no overfull boxes, undefined references or citations; the one underfull box
(badness 2277) is the pre-existing one. The first build stopped on an `itemize` I had left unclosed in the ESG
Conditions; the next showed a new underfull line from an inline SCVA formula, moved into a display. Printed pp. 91,
93, 128, 139 and 259 (the changed entries) were rendered and inspected. Pre-commit on the committed files, new ones
included. Reused without rerun: every other numerical script (no script except the new one changed since `a519e0c`,
whose affected scripts and both checkers passed in the L2 correction pass and were confirmed by the later audit; the
full `make source-check` of `cd55096` covers the rest); `verify-outlines` (the outline crosswalk is unchanged).

**Limits.** Status statements are as of 21 October 2026 and will date. Editorial coverage only; human review of the
new entry and the three corrected ones is outstanding. Nothing pushed; no PR.

**Post-implementation audit corrections, Batch L3, 21 October 2026.** An audit of the committed Batch L3 (`440272b`)
found five statements that the passing checks did not test (L3-F1 to L3-F5) and asked for one bounded attempt to close
the two disclosed source gaps. Starting state: branch `codex/library-gap-batch-l3` at `440272b` (parent `a519e0c`),
working tree clean, no newer work; 446/446 objectives and 1,030/1,030 outline items. Branch
`codex/library-gap-l3-audit-fixes` was created from `440272b`. Local only. The owner authorised a fixes-only pass: no
objective added, no backlog batch started, no existing number or tolerance changed. The claims table and "Not verified"
list above are kept as the history of the first implementation. New copies are in the git-ignored
`reading_materials/library-gap-l3-audit-20261021/` (hashes in its `SHA256SUMS`); the Batch L3 copies were reused where
they already held the passage. Delegation to the models named by the implementation skill was again unavailable.
- L3-F1, `rule:counterparty-credit-cva-capital`, printed maturity factor. The text gave $\sqrt{\min(M,1)}$ without
  the floor. CRE52.48 floors the remaining maturity at ten business days; CRE52.49 gives 10/250 years under a 250-day
  convention. The script already applied the floor, so the four-year example (MF 1) is unchanged. The entry now states
  the floor with a short-maturity counterexample: five business days give 0.2, not $\sqrt{0.02}=0.1414$. A new check
  in `counterparty-capital-check.py` asserts it; an unfloored formula fails it.
- L3-F2, same entry, Notation. The text called $M\,\mathrm{EAD}\,\mathrm{DF}/\alpha$ "the same object as
  $\mathrm{EE}^*$". MAR50.15 n.~3 calls $\mathrm{EAD}\times M$ a proxy for the area under the discounted EE profile;
  n.~4 says $\alpha$ converts EAD back to EEPE. The product is in currency times years; $\mathrm{EE}^*(t)$ is in
  currency at one date. The entry now distinguishes them, keeps the supervisory-proxy qualification (flat EEPE, a fixed
  5 percent rate) and gives the example's area, 13.8225 currency-years against an EEPE of 3.8127. A new check
  confirms it equals $\int_0^4\mathrm{EEPE}\,e^{-0.05t}dt$, and that SCVA is RW times it.
- L3-F3, `meth:esg-exposure-evaluation`, EU. The text cited Directive 2026/470 Art.~2(1), which amends the
  legal-form extension in Art.~1(3) of Directive 2013/34/EU, as the reporting scope. It also said, unqualified, that
  "mandatory reporting is limited" to the new thresholds. Corrected from the directive: Art.~2(4) (Art.~19a(1),
  individual undertakings) and Art.~2(5) (Art.~29a(1), consolidated groups). Art.~2(13) (Art.~40a(1)) gives the
  third-country route: EU turnover above EUR~450m in each of the last two years, through a subsidiary or branch above
  EUR~200m. Art.~3(1) (CSRD Art.~5(2)) keeps the first wave for FY 2024--2026 and allows a Member State exemption
  below the new thresholds for FY 2025--2026. Art.~5(1) sets transposition by 19 March 2027. The FY 2027 start of the
  new scope is Directive 2025/794 Art.~1 (retrieved in L3, now registered). The FY 2028 third-country start is CSRD
  Art.~5(2), second subparagraph, which neither amending directive changes. National transposition was not checked.
- L3-F4, `def:financial-institution-features`, US NSFR. The text said the NSFR applies to banking organisations with
  \$100bn or more of assets, a paraphrase of the 2021 rule's summary. 12 CFR 249.1(b)(1) covers GSIB holding companies
  and their depository institutions, Category II and III, and Category IV only with \$50bn or more of average weighted
  short-term wholesale funding, plus covered nonbank companies and Board determinations. 252.5(e) defines Category IV.
  249.105(b) scales required stable funding at 100, 85 or 70 percent. Board text only (eCFR to 19 October 2026); the
  OCC and FDIC parts were not read.
- L3-F5, `meth:market-risk-limits-capital`, EU 0.9 multiplier. The text applied it to "the standardised
  requirements". CRR Art.~495s(1)--(2), inserted by Regulation 2026/1221, apply it to the sensitivities-based method
  result (Art.~325h(4)) and to the simplified standardised approach. The alternative standardised approach's
  default-risk and residual-risk components (Art.~325c(2)) are not scaled. The optional Art.~495v multiplier is not
  described.
- Source gap, FCA PS26/19. fca.org.uk and the FCA Handbook again returned a Cloudflare challenge to direct requests,
  and no installed browser was available. The FCA's PDF was read from the Internet Archive capture of 7 October 2026
  (87 pages; SHA-256 `0a3e0282…048f833f`): paras 1.1--1.11, 3.6--3.25 and Appendix~1, FCA 2026/56 (made
  24 September 2026, in force 1 January 2027). The rules are comply-or-explain for UKLR 6, 14, 15, 16 and 22 issuers,
  for accounting periods from 1 January 2027 (first reports in 2028), with one-year Scope~3 and two-year S1 reliefs.
  They are now stated separately from the voluntary UK SRS endorsement. Law-firm summaries found by search were not
  used.
- Source gap, Eighth Circuit. The order of 21 May 2026 was read from the court's PDF as posted by the Sabin Center's
  Climate Litigation Database: the motion to lift abeyance was denied and an SEC status report was due by 31 August
  2026. The SEC's letter of 1 June 2026 confirms it (Doc. 5642807). The RECAP docket now held later entries. The order
  of 5 October 2026 (Entry ID 5690930, read from RECAP's copy of the court PDF) accepted the 31 August report and set
  the next for 31 December 2026; RECAP showed it as the last known filing. The 31 August report itself was not read,
  and entries after 5 October 2026 are not verified, so the entry dates this claim to 5 October 2026. The Federal
  Register API, queried 21 October 2026, shows no final rescission, only the June proposal.
- HTTP headers. Every request in this pass used a generic user-agent string without personal identifiers. The
  incident recorded under *Method* above (one early Batch L3 probe whose user-agent contained the owner's e-mail
  address) stands as recorded.

Registry and notes: five new `sources.tex` keys and reading notes (`ca8-iowa-v-sec-2026`, `ecfr-12cfr249-2026`,
`eu-2022-2464-csrd`, `eu-2025-794-stop-the-clock`, `fca-ps26-19-2026`). Corrected notes: the 2026/470, US NSFR,
CRR-relief, UK SRS, SEC-rescission and Basel notes, with the superseded readings kept. Entry evidence for the four
entries; coverage evidence for their four objectives. Objectives 446/446 and items 1,030/1,030 unchanged; no objective
added.

Checks run (2026-10-21). `counterparty-capital-check.py` with warnings as errors: all pass, including the two new
checks; the four-year example values are unchanged. `make lint`, `make format-check` (150 files), `make check-compendium`
(0 problems), `make check-coverage` (0 problems; 446/446, 1,030/1,030) and `make test` (36 passed) all pass.
`make pdf` builds 442 pages (was 441) with no overfull boxes or undefined references; the one underfull box (badness
2277) is the pre-existing one. Printed pp.~93, 128, 139 and 259 (the four changed entries) were rendered and
inspected. Pre-commit runs on every changed and new file. Reused without rerun: every other numerical script. No other
script changed since `440272b`, and those scripts passed in the L2 correction pass, whose results the L3 record reused.
No mathematical L1 or L2 statement was touched. `verify-outlines` was not rerun; the outline crosswalk is unchanged.

Limits: status statements are as of 21 October 2026, except the Eighth Circuit posture (5 October 2026). The FCA text
is an archived copy of the FCA's PDF, not a direct download. Editorial coverage only; human review outstanding. Nothing
pushed; no PR.

**L3 wording correction, 21 October 2026.** Branch `codex/library-gap-l4-proposal`, created from `517213d` (parent
`440272b`; clean tree; 446/446 objectives, 1,030/1,030 items). `meth:esg-exposure-evaluation`, EU timing: the item named
only large public-interest entities above 500 employees as the FY 2024-2026 first wave. CSRD Art.~5(2), first
subparagraph, point (a) also covers (ii) public-interest entities that are parents of a large group above 500 employees
on a consolidated basis (retained OJ text in `reading_materials/library-gap-l3-audit-20261021/eu-32022L2464.html`,
SHA-256 `6ad8df8d…d6c29837`). Directive 2025/794 Art.~1 amends only points (b) and (c), and Directive 2026/470
Art.~3(1)(a)(i) replaces only the introductory dates of point (a) (retained copies from Batch L3), so both cases stand
for FY 2024-2026. The item now names both, citing CSRD Art.~5(2)(a)(i)--(ii), and cites Directive 2026/470 Art.~3(1)
for the exemption sentence. Updated with it: the CSRD and 2026/470 reading notes (earlier wording kept), the entry
evidence, and the objective's CSRD locator and example note. No number or objective changed.

Checks run (2026-10-21). `make check-compendium` (0 problems), `make check-coverage` (0 problems; 446/446, 1,030/1,030),
`make pdf` (442 pages, no overfull boxes or undefined references; the one underfull box is the pre-existing one);
printed p.~139 rendered and inspected. Pre-commit on the changed files. Reused without rerun: every numerical script and
the 36 tests, because no script, input or Python file changed since `517213d`, where they passed; the edit is text and
evidence only. `verify-outlines` not rerun; the crosswalk is unchanged. Nothing pushed; no PR.

## Library gap-filling, Batch L4, 21 October 2026

**Starting state.** Branch `codex/library-gap-l4-proposal` at `95c547a` (parent `517213d`), working tree clean, no
newer work; coverage 446/446 objectives and 1,030/1,030 outline items; L4 proposed, not implemented. Branch
`codex/library-gap-batch-l4` created from `95c547a`. Local only. Owner decisions: L4-D1 all three packages; L4-D2 the
seasoned variance-swap value as a labelled derivation with its contract and approximation assumptions stated; L4-D3 no
separate objective for cross-currency basis swaps. Delegation to the models named by the implementation skill was not
available; the work was done directly.

**Freeze corrections, recorded before implementation**. L4-C1: the proposal's dollar-leg basis $b=\frac FS(1+r_f\tau)-(1+r_{\$}\tau)$ is a period amount and
matched the annual quote only at $\tau=1$; frozen as $[\ldots]/\tau$ with the equivalence
$F/S=[1+(r_{\$}+b)\tau]/[1+r_f\tau]$, checked at $\tau=1$ and 0.25. L4-C2: the gamma sentence implied that differentiating
each path gives the closed form; per path the derivative of the pathwise delta is zero almost surely, and eq. (18) is the
derivative of the expectation with the boundary at $S_T=K$; the pathwise strike statement was restricted to Lipschitz
payoffs (the digital fails both naive methods); larger likelihood-ratio variance is reported as a finding for the cited
examples and this call. L4-C3: the seasoned-swap contract (return measure, schedule, $A$, $K_{\text{vol}}$,
$K_{\text{var}}$, $N_{\text{var}}$ units, empty segments) was defined, and the simulation benchmark changed from the
continuous strike to the exact discrete expectation $\sigma^2+(r-q-\sigma^2/2)^2/A$, with the continuous approximation and
its deterministic difference reported separately. Seeds, path counts and tolerances were fixed before the
first run.

**Sources read** (copies in the git-ignored `reading_materials/library-gap-l4-20261021/`, hashes in its `SHA256SUMS`;
retrieved 2026-10-21).

| Source | Passages | Used for | Limits |
|---|---|---|---|
| Broadie and Glasserman (1996), *Management Science* 42(2) (`broadie-glasserman-1996`, new key); Columbia scan, SHA-256 `247d7319…e1304` | pp. 269-275, 280-281, read as page images; eqs. (4)-(18) and n. 2, p. 272 scope (strike, "except possibly through a change of variables"), p. 274 resimulation, p. 275 the 1.5-4 times ratio, App. A (A1)-(A4) and Proposition 1, App. B eq. (26), p. 281 second derivatives | `meth:monte-carlo-greeks` | Tables (pp. 276-279) and Apps. C-D not read; no digital example in the paper (the digital case is Interpretation, checked) |
| Hull, OFOD 11th Global ed. (`s7-hulloptions`), git-ignored copy SHA-256 `8bc6e2f0…b482` | sec. 21.6, pp. 494-495; sec. 7.10, pp. 192-193; sec. 26.16, pp. 629-631 reread | resimulation; direction of principal exchanges and the decomposition; inception-only variance-swap value | Hull values variance swaps only at inception |
| Demeterfi et al., Goldman Sachs note, March 1999 (`demeterfi-varswaps-gs-1999`, new key, naming the catalogued *J. Derivatives* version `wide-demeterfi-varswaps`), SHA-256 `ad289770…f762223e` | pp. 1-2 (contract terms), 13 (variance vega and remaining variance), 15 (EQ 13-16), 19 (EQ 26), 29-30 (EQ 35-37, additivity) | seasoned-swap extension of `meth:volatility-derivative-applications` | No mid-life formula printed: the value is a labelled derivation; journal version not read |
| Ding, Liu and Rutkowski, arXiv:2410.08477v3 (`ding-liu-rutkowski-ccbs-2025`, new key, naming the catalogued SIAM version `w4-ding-rutkowski-ccbs`), SHA-256 `3f4eed42…f049f2` | pp. 1, 4, 6-7 (Definitions 2.4-2.5, constant spread), 38 (AUD/USD example) | `meth:cross-currency-basis-swaps` cash flows | One pair's convention; model sections not read; MTM resets named only |
| Borio, McCauley, McGuire and Sushko (2016), BIS Quarterly Review (`cur-borio-mccauley-mcguire-sushko-2016`), SHA-256 `32dce4f0…a2928` | pp. 45-48, Graph 1 and Box A (p. 48) | the two sign conventions | LIBOR era; pp. 49-58 not read |

**Delivered.** New `meth:monte-carlo-greeks` (`volatility-options/numerical-methods.tex`; the section title now names
simulated Greeks) and `meth:cross-currency-basis-swaps` (`volatility-options/forward-commitment-valuation.tex`); the
seasoned-swap extension of `meth:volatility-derivative-applications` (Statement, two Practice items, Conditions,
Pitfall); See also links from `meth:monte-carlo-simulation`, `meth:digital-option-valuation`,
`meth:swap-valuation-replication`, `ev:cip-deviations` and `meth:cross-forward-rates`. Adjacent prose: a stray comma
before a citation in `meth:swap-valuation-replication`, and "Its last order found, of 5 October 2026" in
`meth:esg-exposure-evaluation` reworded to "Its order of 5 October 2026, the latest available on 21 October 2026" (the
dated posture is unchanged). One new objective, `objective:estimate-greeks-by-simulation` (`topic:option-valuation`,
planned batch 9); `meth:cross-currency-basis-swaps` mapped as depth to `objective:value-swaps-by-replication` and
`objective:apply-international-parity`; seasoned-swap evidence added to `objective:use-volatility-derivatives`. Reading
notes for the four L4 sources (Borio et al. had none) and the Hull locators; entry evidence; pathway notes
`volatility-options`, `fx-cip-dollar-funding` and `portfolio-construction-risk`.

**Numerical results** (locked uv environment, Python 3.14.7, NumPy 2.4.6, SciPy 1.18.1; first runs, no reseeding).
- `notes/artefacts/numerical-pricing/monte-carlo-greeks-check.py`, seed 20261021, 100,000 shared normals. Deterministic:
  path derivatives and scores against central differences, worst relative error $1.3\times10^{-9}$; eq. (18) boundary term
  equals the BSM gamma 0.0199467491; $S_T/S_0$ unchanged by an $S_0$ bump ($2.8\times10^{-16}$). Call: pathwise delta
  0.50101 (s.e. 0.00188, $z=-0.75$), LR delta 0.49582 (0.00403, $-1.64$), pathwise vega 39.505 (0.233, $-1.67$), LR vega
  38.920 (0.763, $-1.28$), pathwise $\partial C/\partial K$ $-0.40989$ (0.00152, $+0.47$) against 0.50241, 39.894 and
  $-0.41060$. Digital: pathwise delta and strike derivative zero on every path (closest path $10^{-4}$ from $K$); LR delta
  0.018861 (0.000090, $z=-1.51$) against 0.018997. Reported: LR/pathwise standard-error ratios 2.15 (delta) and 3.28
  (vega); digital resimulation 0.019030 (0.000426) at $h=1$ and 0.020379 (0.004447) at $h=0.01$.
- `notes/artefacts/derivative-overlays/seasoned-variance-swap-check.py`. Deterministic: worked value 182,562.0029; inception
  0; expiry 562,500; decimal units equal; payoff derivative at $K_{\text{vol}}$ equals the vega notional 100,000;
  observation weights from a return series; $E[r^2]$ by quadrature to $10^{-9}$. Exact discrete remaining strike 324.007557
  (value 182,571.26) against the continuous 324 (182,562.00), difference 9.26, deterministic. Simulation, seed 20261021,
  200,000 paths: 182,634.39 (s.e. 111.83), $z=+0.56$ against the exact discrete value. Reported: mean-subtracted realised
  variance 597.23 (over $n$) and 602.00 (over $n-1$) against 625; calendar-day weights 181,551.59.
- `notes/artefacts/forward-swap-valuation/cross-currency-basis-check.py`, deterministic: cash flows by party (A: $-100$m EUR
  and $+110$m USD at $T_0$, $+2.3$m and $-4.4$m each year, principals back at $T_3$); covered parity at $\kappa=0$
  (1.116098; 1.104099 at $\tau=0.25$); forward with the basis 1.118280 (1.104648); $b=20.3324$ basis points at $\tau=1$ and
  20.0845 at $\tau=0.25$, period amount 5.0211; synthetic dollar rate 4.2033 and 4.2008 percent; inverted quote 0.894231;
  final exchange $+4.0$m at 1.14, matching the fixed-for-fixed example's 4.0m.

One harness correction during the run, recorded: the seasoned-swap script's first run compared the worked value with a
mistyped literal (182,562.4, tolerance 0.5); the value is $2{,}500e^{-0.02}\times74.5=182{,}562.0029$ by hand, so the
literal was corrected and the tolerance tightened to 0.01. No seed, path count or other tolerance changed.

**Checks run (2026-10-21).** The three scripts with warnings as errors (pass, after `ruff format`, which changed layout
only; outputs identical). `make lint`, `make format-check` (153 files), `make check-compendium` (0 problems, 695 entries),
`make check-coverage` (0 problems; 447/447 objectives, 1,030/1,030 items) and `make test` (36 passed) pass. `make pdf`
builds 443 pages (was 442) with no overfull boxes or undefined references; the one underfull box (badness 2277) is the
pre-existing one. Printed pp.~138--139, 181--182, 191 and 261--262 rendered and inspected. Pre-commit on every changed
and new file. Reused without rerun: every other numerical script, including `overlay-checks.py`,
`forward-swap-checks.py`, `numerical-pricing-checks.py`, `exotic-option-checks.py`, the inference-simulation and FX
scripts, because their files and inputs are unchanged and the L4 edits to their entries are text and cross-references;
their last recorded passes (Batch L2 correction pass, reused by L3) still apply. `verify-outlines` not rerun; the crosswalk is unchanged.

Limits: editorial coverage only; human review outstanding. Shortfall 44 against the 45-objective preference, without
padding. The seasoned-swap value and the B13 annualised mapping are Interpretation, checked for internal consistency, not
printed in the sources read. Excluded: mark-to-market cross-currency swaps, multi-period cross-currency valuation and
curves, second-order Monte Carlo Greeks beyond the gamma sentence, empirical basis levels after 2016. Nothing pushed; no
PR.

## C1 pass: L4 corrections and gap inventory, 21 October 2026

**Starting state.** Branch `codex/library-gap-batch-l4` at `e6c22e6` (parent `95c547a`), working tree clean, no newer
work; 447/447 objectives, 1,030/1,030 items. Branch `codex/library-gap-c1-inventory` created from it. Local only.
Delegation to the models named by the implementation skill was not available; the work was done directly.

**L4 corrections** (no objective, input, seed or earlier tolerance changed).
- `meth:monte-carlo-greeks` (L4-F1): Broadie-Glasserman's $h^*$ (App. B, eq. (26), p. 281; the page was reread and states
  that $\rho$ is assumed independent of $h$) is no longer presented as a universal optimum; the call/digital
  shared-path variance distinction and the restriction of unbiasedness to the direct estimators under their conditions
  were added. Fixed before the run: one new section in `monte-carlo-greeks-check.py` on the same seed and draws, with
  relative tolerances of 1% for the two limits and a factor-2 band for the ratio check. Results: call finite-difference
  variance 0.348653, 0.351635, 0.351932 and 0.351952 at $h=1$, 0.1, 0.01, 0.001 against 0.351959 for the pathwise delta;
  digital variance exact from the lognormal distribution, 0.018065, 0.18399, 1.8432 and 18.435, so $h\times$variance runs
  0.018065 to 0.018435 against the limit $e^{-2rT}g(K)K/S_0=0.018435$. All 17 checks pass; parts 1-3 unchanged.
- `meth:volatility-derivative-applications` (L4-F2): "volatility points squared" for the $10^4$ conversion; "zero mean"
  defined as not subtracting the sample mean. Text only; `seasoned-variance-swap-check.py` not rerun.
- `meth:esg-exposure-evaluation` (L4-F3): the 5 October 2026 order qualified as the latest found in the public RECAP
  docket as of 21 October 2026, PACER not used, later filings unverified (as in `notes/readings/ca8-iowa-v-sec-2026.md`).

**C1 inventory**. Discovery material: the 18 volumes of the 2024 curriculum, read-only, text extracted
with pypdf 5.1.0 in an isolated environment to the session scratchpad (none enters the repository and none is cited).
Reconciliation: 175 numbered modules, of which two are statistical-table appendices; 173 substantive; C0's 76 compared
plus 97 remaining. The 97 were title-matched to the crosswalk (78 same-titled), screened by head words (74 of 2,231 heads
flagged) and compared by hand with entry titles and text. Support checked in held or registered sources: Hull sec. 26.11,
pp. 623-625 (lookback formulas, Example 26.2); Wilmott contents, the end of chap. 47 and the opening of chap. 48 (PDF pp. 799-809; Leland's
adjusted volatility, sec. 48.3) and the chap. 24 lookback passages (PDF pp. 443-447); Damodaran, *Applied Corporate
Finance*, printed pp. 98-107 (country risk premiums); *Managing Investment Portfolios* (2007) Example 11-3 and Exhibit
11-4, pp. 693-695 (hedging and monetisation of a concentrated position). Catalogue searched for B4 and B14 sources.
Outcome: 2 confirmed distinct candidate objectives (lookbacks; hedging with transaction costs), 4 sourced depth
extensions, 2 possibly distinct but unresolved (vanna-volga; hedge-fund replication), 5 unsourced depth items;
provisional 449 for this corpus, at most 451. Batch L5 proposed (+2), not frozen.
*Corrected 2026-10-21 (pre-L5 audit, C1-F2):* "4 sourced depth
extensions" overstated the evidence. C1-D1 is supported (passages read); C1-D2 partly (*Managing Investment Portfolios*
read; Hull's collar pages held, not read for it; IRC secs. 1259 and 721 not read); C1-D3 is unsupported (Natenberg held,
its passages not located or read); C1-D4 cited Wilmott secs. 10.11-10.12, which are the backward equation, and became
supported only when sec. 10.4 (forward equation (10.2), printed p. 172) was read in the pre-L5 pass.

**Checks run (2026-10-21).** `monte-carlo-greeks-check.py` with warnings as errors (after `ruff format`); `make lint`,
`make format-check`, `make check-compendium` (0 problems), `make check-coverage` (0 problems; 447/447, 1,030/1,030),
`make test` (36 passed); `make pdf` and inspection of the changed pages; pre-commit on every changed and new file.
Reused without rerun: every other numerical script (no code, input or asserted result changed), including
`seasoned-variance-swap-check.py` and `cross-currency-basis-check.py` from L4. `verify-outlines` not rerun; the
crosswalk is unchanged. Limits: the inventory is a bounded comparison of the inspected corpus, not a census of the
finance library; editorial coverage only; human review outstanding. Nothing pushed; no PR.

## Library gap-filling, Batch L5, 21 October 2026

**Starting state.** The prompt expected `codex/library-gap-c1-inventory` at `d71e127` with a clean tree. Found: that
branch unchanged at `d71e127`, and `main` checked out at `c26a09e`, the merge of PR #33 whose second parent is `d71e127`
and whose tree is identical to it (empty diff); clean tree; 447/447 objectives, 1,030/1,030 items. Branch
`codex/library-gap-batch-l5` was created from `main` so the newer merge is kept. Local only; no push, PR, merge, rebase
or amendment. Delegation was not used; the work was done directly.

**Audit corrections before L5**.
- C1-F1, `meth:monte-carlo-greeks`: "fixed-step resimulation is biased whatever the conditions" replaced by: generally
  biased, since its expectation is the finite difference of the price; more paths reduce only the sampling error; affine
  price functions (a forward's value in $S_0$) are exact. Text only; estimator formulas and numbers unchanged;
  `monte-carlo-greeks-check.py` not rerun.
- C1-F2, Section 8.2 and the C1 record: depth extensions reclassified by evidence (supported C1-D1; partly C1-D2;
  unsupported C1-D3, Natenberg held but passages not located; C1-D4 supported after Wilmott chap. 10, secs. 10.2-10.6,
  printed pp. 169-175 were read for this pass, forward equation (10.2) on p. 172). C1-D1 and C1-D2 were not reread.

**Freeze.** Owner decisions L5-D1 (L5-a and L5-b, +2; L5-c excluded), L5-D2 (Leland through Wilmott chap. 48, Leland
named as originator, the 1985 paper not read and listed under Further reading only), L5-D3 (C1-D1 and C1-D2 deferred;
other backlog items stay deferred). The specification, inputs, seeds, path counts, grids and tolerances were recorded before either script ran; one sign slip in the L5-b
gate (b) expression was corrected before the first run.

**Sources read** (held = in the owner's library or the git-ignored folders; read = the passages below were read).
- Hull, OFOD 11th Global ed., `reading materials/` copy (SHA-256 `8bc6e2f0…b482`, printed = PDF page): sec. 26.11,
  pp. 623-625, read in the text layer. Broadie, Glasserman and Kou (1998), Goldman, Sosin and Gatto (1979) and Wong-Kwok
  (2003) are cited by Hull only; none is held or read.
- Wilmott, PWOQF 2nd ed. (library copy, SHA-256 `e0ff5f09…d549`, printed = PDF $-21$): chap. 24, secs. 24.4-24.5,
  pp. 422-425; chap. 26, pp. 445-452; chap. 48, pp. 783-811 including the appendix, with pp. 785, 788 and 789 also viewed
  as rendered page images; chap. 10, pp. 169-175. Text extracted with pypdf 5.1.0 and pages rendered with PyMuPDF 1.26.3,
  both in isolated throwaway environments outside the project (no dependency added) into the session scratchpad; no
  source text entered the repository.
- Leland (1985, `vo-leland-1985`), Whalley and Wilmott (1997, `vo-whalley-wilmott-1997`), Heynen and Kat (1995),
  Jefferies (1999): catalogued or named, not held or read.

**Discrepancies.** Wilmott p. 789 prints the long-position breakdown as $\kappa>\sigma/\sqrt{8\pi\delta t}$, which is
dimensionally inconsistent with (48.5); (48.5) gives $\kappa<\sigma\sqrt{\pi\delta t/8}$, i.e. $K<\sqrt{\pi/8}\approx0.6267$
(at $\sigma=0.2$, $\delta t=1/52$: 0.01738 against the printed 0.2877). The entry teaches the derived form and notes the
print. The sec. 48.4 heading dates Hoggard-Whalley-Wilmott 1992 and its further reading 1994; the entry gives no year.
No source read prints a lookback discrete-monitoring correction, so none is taught; the barrier shift is not applied.

**Entries.** `meth:lookback-option-valuation` (new, `volatility-options/exotic-options.tex`, after the barrier entry;
section heading and introduction now name lookbacks; the barrier entry gained a See also link) and
`meth:transaction-cost-hedging` (new, `volatility-options/option-valuation.tex`, after
`res:delta-hedging-volatility-mismatch`, which gained a link). Labelled Interpretation: the seasoned use of Hull's
formulas, the exact Brownian-bridge extreme, $\kappa$ as half the proportional spread, and the Itô identity
$\hat V-V=E^Q\!\int e^{-rt}\kappa\sigma\sqrt{2/(\pi\delta t)}S^2\hat\Gamma\,dt$. New objectives
`objective:value-lookback-options` and `objective:hedge-options-with-transaction-costs` (`topic:option-valuation`,
planned batch 10).

**Checks (fixed before the first run).**
- `notes/artefacts/exotic-options/lookback-option-check.py`. First run: 19 of 20 gates passed; the pricing-equation
  residual failed, ``BAD pricing-equation residual at interior points (S strictly inside the extreme) <= 1e-6: largest
  3.6e-06''. Diagnosis (harness, not formula): at $S=50$, $S_{\min}=48$, $\tau=0.1$ the residual is $-3.5\times10^{-4}$,
  $-3.2\times10^{-5}$, $-3.6\times10^{-6}$ and $-3.3\times10^{-7}$ at $h_S=0.1$, 0.03, 0.01 and 0.003, falling as $h_S^2$;
  the frozen tolerance assumed a truncation error below $10^{-9}$, which is false near the running extreme. Correction:
  the frozen $10^{-6}$ is applied to the Richardson-extrapolated residual $(4R(0.01)-R(0.02))/3$ (largest
  $4.5\times10^{-8}$), with the raw residuals printed. All other output is identical between the two runs. Results:
  Example 26.2 put 7.790219 and call 8.037120 (7.79 and 8.04 to the cent); printed $b_1,b_2,b_3,Y_2$ reproduced; Hull and
  Wilmott agree to $7.9\times10^{-15}$ relative (floating, fixed in both strike cases, $q=0$ and 0.02); boundary condition:
  one-sided difference $-4.01\times10^{-4}$ ($h=0.01$) and $-4.01\times10^{-5}$ ($h=0.001$) against the interior
  derivative $-0.39945$; deep-seasoned excesses $3.1\times10^{-6}$ (call, $S_{\min}=20$, value 30.4938) and
  $6.9\times10^{-5}$ (put, $S_{\max}=120$, 67.0373); monotone in the recorded extreme. Seasoned simulation (seed
  20261022, 400,000 paths): call $S_{\min}=45$ 9.0303 (s.e. 0.0123) against 9.0448, $z=-1.18$; put $S_{\max}=56$ 9.0739
  (0.0093) against 9.0729, $z=+0.10$; fixed call $K=52$ 8.3488 (0.0102) against 8.3568, $z=-0.79$; $K=60$ 2.6175 (0.0082)
  against 2.6249, $z=-0.91$; the seasoned-new difference is 82 (call) and 138 (put) standard errors. Monitoring (seed
  20261021, 100,000 paths, 1,008 steps): continuous call 8.0249 (0.0223), $z=-0.55$, put 7.8187 (0.0165), $z=+1.73$;
  paired gaps, call 1.6340, 0.9977, 0.5930, 0.3024, 0.1523 and put 2.1810, 1.3452, 0.8076, 0.4140, 0.2094 for $m=7$, 21,
  63, 252, 1,008 (paired s.e. 0.00025 to 0.00437); $g_{1008}/g_{63}$ 0.257 (call) and 0.259 (put); $g_m\sqrt m$ 4.32 to 4.83
  (call), 5.77 to 6.65 (put); pathwise ordering holds on every path.
- `notes/artefacts/option-valuation/transaction-cost-hedging-check.py`, all gates passed on the first run. (48.5)-(48.6)
  equal the printed forms to $2.2\times10^{-16}$; signs, zero-cost limit and the domain ($K^*=0.6267$) hold; Wilmott's
  spread approximation has relative error $3.77\times10^{-3}$ at $K=0.01$ and $3.78\times10^{-4}$ at $K=0.001$. Ledger
  identity to $3.4\times10^{-13}$; mean discounted wealth minus its exact expectation $-0.0038$ (s.e. 0.0029, short) and
  $+0.0040$ (0.0030, long). Residuals $e_N$ (seed 20261023, 100,000 paths, $N=13$, 52, 208): short $K=0.1$ ($L=0.5777$)
  $+0.0400$, $+0.0125$, $+0.0039$; short $K=0.4$ ($L=2.1123$) $+0.2012$, $+0.0640$, $+0.0199$; long $K=0.1$ ($L=0.6233$)
  $+0.0315$, $+0.0098$, $+0.0031$; long $K=0.4$ ($L=2.9354$) $+0.0543$, $+0.0180$, $+0.0064$; standard errors of $C_N$
  0.0007 to 0.0048. The residual is positive throughout (the simulated cost exceeds the Leland premium) and falls about
  3.2 times per fourfold refinement, consistent with an $O(\sqrt{\delta t})$ leading error; this rate is observed, not
  gated. Reported: opening cost 0.1756 (short) and 0.1781 (long); settlement trade 0.0170 and 0.0157 against a
  cash-settled close of 0.1759 and 0.1760; P&L s.d. 0.925 and 0.878. Fixed $\kappa=0.2$ percent, BSM delta: costs 0.2289,
  0.4399, 0.8686, P&L s.d. 1.773, 0.933, 0.584, premium for a 5 percent loss probability 13.695, 12.527, 12.420. Call
  spread: separate 0.8544, netted 0.2474, saving 0.6070 (s.e. 0.00070), never more on any step; long-short same call
  exactly 0 netted. Leg-by-leg Leland 4.4906, BSM spread 5.3251, BSM less separate cost 4.4707, less netted cost 5.0777
  (approximate values under a fixed delta rule, not solutions of (48.4)).

**Validation.** The two new scripts with warnings as errors (pass; `ruff format` and a lint-only switch to `itertools.pairwise`
changed layout only, outputs identical to the recorded runs). `make lint`, `make format-check` (155 files),
`make check-compendium` (0 problems, 697 entries), `make check-coverage` (0 problems; 449/449 objectives, 1,030/1,030
items), `make verify-outlines` (0 problems) and `make test` (36 passed). `make pdf` builds 445 pages (was 443) with no
overfull boxes or undefined references; the one underfull box (badness 2277) is the pre-existing one. Printed pp.
185-186 and 192-194 (PDF 191-192 and 198-200) rendered and inspected. Pre-commit on every changed and new file.
Reused without rerun: every other numerical script, including `monte-carlo-greeks-check.py` (C1-F1 changed text only),
`exotic-option-checks.py` and `volatility-mismatch-hedging-check.py` (their entries gained links only), because no
code, input or asserted result changed; their last recorded passes (L4 and the C1 pass) still apply.

**Limits.** Editorial coverage only; human review outstanding. The lookback monitoring result is for one parameter set
and no rate is claimed beyond it. The Leland comparison is under the risk-neutral measure with $q=0$, physical
settlement and the opening trade excluded; real-world drift, discrete dividends, fixed costs and band strategies are not
simulated. The Hoggard-Whalley-Wilmott equation is stated, not solved; the call-spread figures are a hedge-cost
demonstration. Wilmott's empirical comparisons (Jefferies) are reported as printed and are dated. Deferred: C1-D1
(country risk premium), C1-D2 (concentrated positions), L5-c (option-strategy practice; Natenberg passages still to be
located), C1-D4 as an entry (now sourced), and the unresolved C1-U1 to C1-U3 items. Shortfall 43 against the
45-objective preference, without padding. Nothing pushed; no PR.

## Library gap-filling, Batch L6, 21 October 2026

**Starting state.** `codex/library-gap-batch-l5` at `af47d03` (parent `c26a09e`, the PR #33 merge), clean, 449/449
objectives and 1,030/1,030 items, as expected. Branch `codex/library-gap-batch-l6` created from it. Local only.

**L5 clarifications**. `meth:transaction-cost-hedging`: Wilmott's p. 788
approximation stated as each side's adjustment from the frictionless value, with the short-minus-long difference about
twice it to first order. Frozen L5-a specification: a dated cross-reference after check 4 to the amended Richardson gate
and the L5 record; the pre-run criterion and its first-run failure are kept. Editorial; no rerun.

**Scope.** Owner decision: C1-D1 and C1-D2, depth only (+0 objectives); C1-D3, C1-D4 and C1-U1 to C1-U3 deferred.
Specification (inputs, contracts, hand values, tolerances) recorded before either script ran.

**Sources read.**
- Damodaran, *Applied Corporate Finance*, 4th ed. (library PDF, SHA-256 matches the reading note; printed = PDF $-16$):
  pp. 89-93, 98-107, 133-135.
- *Portfolio Management in Practice*, Vol. 1 (registered key; same copy as its reading note; printed = PDF $-28$):
  chap. 16, sec. 6, pp. 904-913.
- *Managing Investment Portfolios* (2007) (SHA-256 matches; printed = PDF $-29$): pp. 693-695, p. 687, p. 47.
- Hull, OFOD 11th Global ed. (same copy as L5): sec. 12.2, pp. 270-271; sec. 17.2, pp. 387-389; p. 615 and n. 1.
- US primary texts retrieved 2026-10-21 into the session scratchpad (not saved in Git): 26 U.S.C. 1259 (whole),
  721(a)-(b), 351(e)(1), 704(c)(1)(B), 737(a)-(b), 664(b)-(d), and 26 C.F.R. 1.351-1(a)(1), (c)(1)-(6), from LII (Cornell);
  Rev. Rul. 2003-7 from the 2003-5 Internal Revenue Bulletin PDF on irs.gov. Text extracted locally (pypdf 5.1.0 in a
  throwaway environment; HTML stripped with a standard-library script) and read directly; no summarising tool was used.
- Not read, and nothing taught from them: sec. 170, any regulations under sec. 1259(c)(1)(E), Treas. Reg. 1.721-1, later
  rulings or cases on prepaid forwards, state law. Charitable remainder trusts are included because PMiP p. 912 gives a
  substantive mechanism and sec. 664 was read; the MIP definition alone (p. 47) would not have sufficed.

**Discrepancies.** Damodaran: India's spread 2.00 in the prose of p. 98 against 2.25 in its equation and Table 4.5;
the p. 100 India line prints $4.20+2.25(24/17)=7.80$, but 24/17 gives 7.38, and only Table 4.5's 24/15 is consistent with
7.80; Table 4.5 is headed March 2009 with November 2013 inputs. PMiP: exchange-fund qualified assets "usually REITs",
not reconcilable with 26 U.S.C. 351(e)(1)(B)(iv) and Reg. 1.351-1(c)(1)(ii), which count REIT interests among the
investment assets; not taught. PMiP and MIP describe charitable trusts and exchange funds as avoiding or not triggering
tax; secs. 664(b), 704(c)(1)(B), 737 and the carried-over basis make both deferral, and the entry says so. MIP's
"private exchange ... tax free" is not verified and not taught as a tax result.

**Entry changes.** `meth:cost-of-debt-equity-estimation` (country-risk block in Statement, example in Practice,
conventions and dates in Conditions, four new pitfalls); `meth:complex-client-situations` (concentrated-position
block, US federal tax mechanics dated 21 October 2026, example, Conditions and Pitfalls, See also);
`meth:covered-call-protective-put` (zero-cost collar condition and convergence to a forward, link). Sources: the IRC key
extended; new keys `irs-rev-rul-2003-7` and `us-treas-reg-1-351-1` with reading notes. Objective evidence updated for
`estimate-cost-of-debt-and-equity`, `advise-complex-client-situations` and `analyse-covered-and-protective-positions`;
no objective added.

**Checks** (deterministic; acceptance fixed before the first run).
- `notes/artefacts/corporate-finance/country-risk-premium-check.py`. First run: 2 of 23 failed, both harness errors.
  (1) ``BAD Table 4.5 India: relative-sd 2.52, melded 3.60: 2.5200, 3.1765'': the script took India's bond volatility
  (17) from the p. 100 formula line, while the specification gates Table 4.5, whose ratio is 24/15; the input was
  corrected and the p. 100 line is reported as a source slip. (2) ``BAD ke local inflation: ... hand 17.10705: 17.106732'':
  the hand literal was mistyped ($1.1324\times1.06/1.025-1=17.10673$ percent; the predetermined rounded 17.107 was right).
  No tolerance changed. Final: Table 4.5, Illustration 4.2, Disney 5.7616 and Vale 18.6670 and 18.8733 reproduced to
  printed rounding; the example agrees in float and exact rational arithmetic to $10^{-12}$ and with the hand values;
  zero limit exact.
- `notes/artefacts/private-wealth/concentrated-position-check.py`. First run: 1 failure, ``BAD sale: tax 900,000,
  4,100,000 reinvested, 4,267,328.43 ...: 4,371,405.25''. The frozen hand values were wrong (gain 4,000,000, so tax
  800,000 and 4,200,000 grows to 4,371,405.25); the script was right. Literals corrected, tolerance unchanged, and the
  correction recorded here. Final: parity and zero-cost strike $K_2=62.0380$ to $10^{-10}$; advance
  4,529,075.55 (90.58 percent) by two routes to $10^{-10}$; payoff identity exact and decomposition to $10^{-9}$ on the
  grid; delivered shares 100,000 to 80,000; PMiP Exhibit 15 reproduced to the dollar; break-even fee 1.8081 percent a year.

**Validation.** The two new scripts with warnings as errors (pass; `ruff format` changed layout only, outputs identical to the
recorded passing runs). `make lint`, `make format-check` (157 files), `make check-compendium` (0 problems),
`make check-coverage` (0 problems; 449/449 objectives, 1,030/1,030 items) and `make test` (36 passed). `make pdf`
builds 446 pages (was 445) with no overfull boxes or undefined references; the one underfull box is the pre-existing
one. Printed pp. 144-145, 186-187 and 300-301 (PDF 150-151, 192-193 and 306-307) rendered and inspected; the script
name was then removed from the new practice item, as the conventions require. Pre-commit on every changed and new file.
Reused without rerun: `corporate-finance-checks.py`, `private-wealth-checks.py`, `option-strategy-checks.py` and the L5
scripts, whose code, inputs and asserted results are unchanged (the L6 edits to their entries add text; the L5 edit is
wording); `verify-outlines` not rerun, the crosswalk is unchanged.

**Limits.** Editorial coverage only; human review outstanding. Both examples are synthetic; the option values are
Black--Scholes with no dealer margin, and real collars and prepaid forwards are bespoke. Tax notes are US federal income
tax only, dated 21 October 2026, rules not advice, and exclude the items listed as not read. Damodaran's market figures
are from 2013-2014, MIP's from 2007. Deferred: C1-D3, C1-D4, C1-U1 to C1-U3. Objectives unchanged at 449/449, items at
1,030/1,030. Nothing pushed; no PR.

## Return-predictability content batch (22 October 2026)

**Starting state.** `main` at `2ebe829` (merge of the subsection alignment, PR #36), clean; guide pin `8302467`;
697 entries, 111 printed pathways, 461 PDF pages, 449/449 objectives. Branch `codex/return-predictability-content`.
Scope set by the request: the three entries of the deferred `content_development_plan.md`, no general coverage campaign.
The plan was reconciled first (pin, `\qfpathway` placement after `empirical-asset-pricing`, owning pathways of the
reused entries, batch size); its section 0 records the decisions. Local only; nothing committed or pushed.

**Sources read** (equations and tables as page images; downloads logged with URL, time, status, size and SHA-256 in the
git-ignored `reading_materials/return-predictability/dl_log.tsv`):
- Campbell and Shiller, NBER WP 2100 (December 1986), from nber.org, a 40-page scan whose text layer is unusable for
  equations: pp. 1, 4-5 (eqs. (1)-(5), the linearisation point), Table 1a, p. 21. Registered as
  `campbell-shiller-1986-nber`. The RFS 1988 version was not obtained.
- Clark and West, NBER Technical WP 326 (August 2006), from nber.org: abstract, secs. 1-4 (pp. 1-10), sec. 6.1
  (pp. 13-15), sec. 7 (pp. 19-20), Table 1 (PDF p. 36) and the empirical table (PDF p. 40). Registered as
  `clark-west-2006-nber`. The Journal of Econometrics version was not obtained.
- Cochrane, RFS 21(4) 2008, the published article from the author's site: pp. 1533-1541 and 1544.
- Welch and Goyal, RFS 21(4) 2008, the existing local journal copy: pp. 1456-1457, 1461-1462, 1464, Table 1 (p. 1470,
  rendered at 220 dpi and rotated).
- Campbell and Thompson, NBER WP 11468, the existing local copy: pp. 2-3, 6, 9-10 and Table 2 (PDF p. 26, 220 dpi).
- Goyal's data page (sites.google.com/view/agoyal145) and two workbooks; the one used is labelled "Original data (up
  to 2005) used in the paper" but runs to December 2025 (SHA-256 `8d210b77...be872`).
- Not obtained or read, and nothing taught from them: `wide-campbell-shiller-1988`, `wide-clark-west`,
  `wide-campbell-thompson` (journal versions), `wide-rapach-strauss-zhou`, `wide-goyal-welch-zafirov`,
  `wide-giacomini-white`, `wide-gneiting-raftery`, `wide-martin-svix`, `w3-cakici-pockets-replication`.

**Discrepancies and source limits.**
- Welch and Goyal's adjusted out-of-sample R^2, as printed with eq. (6), is `R^2 - (1 - R^2)(T - k)/(T - 1)`; for R^2
  near zero it gives about -100 percent, which Table 1 does not show. Read as a misprint; ΔRMSE is the gated comparison.
- Clark and West's empirical table is printed "Table 4" and called Table 7 in the text (p. 20).
- Campbell and Thompson define the "wrong" sign against "the theoretically expected sign estimated over the full
  sample" (p. 6), which uses future data if taken literally; the entry and the script fix the sign from theory.
- The 1986 working paper's timing ($\delta_t=d_{t-1}-p_t$) and $\rho=\exp(-(r-g))$ differ from the 1988 form; both are
  stated, and the 1988 form is cited to Cochrane, whose copy is the published article.
- No 2005 data vintage was available: differences from the 2008 and 2005 tables cannot be separated from revisions.

**Entries.** New: `res:campbell-shiller-identity`, `meth:nested-forecast-tests`, `meth:restricted-forecast-value` in
`compendium/asset-pricing/return-predictability.tex`, under `\qfpathway{return-predictability}{Return predictability and
forecast evaluation}` (section 8.3). Navigation only, checked to be identical to `HEAD` once the inserted links are
removed: `def:contango-backwardation-stocks`, `meth:fx-valuation-signals` (a link on the first "Clark--West"),
`meth:forecast-accuracy-evaluation`, `meth:backtest-evaluation-diagnostics` (See also). The other 693 entries are
byte-identical; no label, type or file changed. Their evidence records are unchanged, since no claim moved.

**Coverage.** New `topic:return-predictability` (section `asset-pricing`; prerequisites `topic:time-series-models` and
`topic:asset-pricing-factor-models`) with `objective:interpret-present-value-identity`,
`objective:test-nested-return-forecasts` and `objective:value-restricted-return-forecasts`, covered at analysis depth
with these sources, reading notes, entry evidence and worked examples, and
`objective:score-and-combine-return-forecasts`, missing (next action obtain-source), so that the topic records the part
of the pathway outcome that is not written. The pathway checkpoint was not attempted. Objectives 453: 452 covered, 1
missing; outline items unchanged at 1,030/1,030. Nothing in `notes/log.md`; no study or mastery claimed.

**Checks.** `notes/artefacts/return-predictability/`: `return-predictability-protocol.md` (definitions, timing and
tolerances written before the first run, after the published tables had been read; not a preregistration);
`goyal_extract.py` (empirical group; verifies the workbook hash, writes the two CSVs); `return-predictability-checks.py`
(numpy and pandas, default environment, about 1 s) and `return-predictability-results.txt`.
- First run: every gated check in parts A, B and C1-C3 passed; the run then stopped in C4 on a NumPy RuntimeWarning
  (under `-W error`), because the running variance was computed for a one-observation column that the slice discarded.
  Harness corrected; no reported number depended on it.
- C4 then showed a design flaw in the protocol, not in the code: with DGP 1's mean (1.55 percent a month against a
  variance of 18) the weight sits at the 1.5 cap in 98-100 percent of months, so the synthetic check cannot show a
  forecast's value. Kept and reported; a diagnostic line and a post-run supplement C5 (mean 0.5 percent a month, seed
  20261024, outside any verdict) were added, and a units slip in C5's known-parameter reference (an extra division by
  100) was corrected before values were recorded. The observed values were then added as regression checks. No
  tolerance changed. Final: 39 checks pass.
- Results against published figures (first run; part A superseded by the audit below): identity error-variance ratio
  0.0023 (1872-1986) and 0.0025 (1872-2025), against Campbell and Shiller's 0.0008 for a deflated series; Clark-West
  size 0.069 and 0.059 against 0.085 and 0.070 (inside the 0.02 tolerance, below by more than the simulation error of
  about 0.004; cause not identified), unadjusted 0.023 and 0.010 against 0.028 and 0.012; Welch-Goyal d/p ΔRMSE -0.13 against -0.11 and -0.09, in-sample adjusted R^2 0.32
  against 0.49; Campbell-Thompson d/p utility 0.492 against 0.501 percent a month, changes -0.018 and -0.024 against
  -0.016 and -0.024. Seeds 20261022, 20261023 and 20261024; Python 3.14.7, NumPy 2.4.6, pandas 3.0.5.

**Validation.** See the end of this record.

**Limits.** Editorial coverage only; human review outstanding. One predictor, one market; working-paper locators for
three of the five papers; a 2026 data vintage compared with tables built from 2005 data. Deferred: forecast
combination, conditional tests, proper scoring, option-implied bounds, the checkpoint replication, predictive-regression
bias (`standard-errors-inference`), and the cause of the lower Clark-West size at P = 120 (see the audit below).

**Validation (22 October 2026).** `make check` (exit 0): lock check; ruff lint and format (160 files); `check_compendium.py
--check` (700 entries, 112 pathways printed, 96 pathway notes, 0 problems); `check_coverage.py --check` and
`--verify-outlines` (0 problems; 453 objectives, 452 covered, 1 missing; 1,030 items covered); `make test` (59 passed);
`make examples` (128 scripts, warnings as errors); `make pdf`: 464 pages (was 461), no overfull boxes (one in the
first build, from an inline weight formula, removed by displaying it), no undefined references, the one pre-existing
underfull box. Contents list: 8.3 *Return predictability and forecast evaluation*, p. 35; PDF bookmark under chapter 8
at PDF p. 41. Printed pp. 35-38 (PDF 41-44) rendered and read: headings, equations, the five tables and links; one
sentence corrected afterwards (the restrictions do not improve the utility change). `make pre-commit` (exit 0, no file
changed). Entry preservation: the 697 earlier entries keep labels, types and files; 693 are byte-identical and four
differ only by the inserted links. `guide/` unchanged.

**Audit corrections (22 October 2026, before commit).** An audit of the uncommitted batch reported three findings;
each was checked independently against the local source PDFs as page images before anything was changed. The working
tree was snapshotted first; nothing was reset, committed or pushed. The first run (script, output and protocol as they
stood) is preserved unchanged in `notes/artefacts/return-predictability/superseded-first-run/` with a README, and it
still reproduces its output byte for byte. The protocol keeps its original text with two bracketed notes and a new
*Audit corrections* section; no seed, specification or tolerance changed.
- *Campbell-Shiller linearisation point.* Confirmed: NBER WP 2100, printed p. 5, linearises around `Δd = g` and
  `δ = log(exp(r - g) - 1)` with `r` "the log of one plus the sample average real return", i.e. `log(1 + mean R)`; the
  script used the mean log return. Timing checked: `R_t = (P_{t+1} - P_t + D_t)/P_t` with `δ_t = d_{t-1} - p_t` is the
  Goyal return `(Index_t + D12_t)/Index_{t-1}` with the end-of-year dividend yield. Real data in the paper (Table 1a,
  PPI and CPI deflated); the extracted file has no deflator, so the batch's rows are now labelled a nominal
  illustration, not a reproduction. Working-paper `ρ`: 0.9498 and 0.9501 before, 0.9348 and 0.9364 after (1872-1986,
  1872-2025).
- *Identity and approximation.* Confirmed: part A used CRSP returns from 1926 with `Index` and `D12`, and A1 was
  restricted to 1872-1925 without a protocol record. Part A now builds the return from `Index` and `D12` in every year:
  exact identity 1.9e-15 over 1872-2025; CRSP-versus-constructed log mismatch reported separately (1926-2025: mean
  +0.00002, standard deviation 0.0103, largest 0.0675 in 1931). The approximation error is checked to equal the
  Taylor remainder of `log(1 + e^x)` (1e-12), to be non-negative by convexity and at most `(pd - pd-bar)^2/8`, at both
  points. Variance ratios: mean-pd point 0.00021 and 0.00077 (were 0.0023 and 0.0025, which the CRSP mismatch
  dominated: 0.00229 and 0.00248 with it); working-paper point 0.00089 and 0.00728. The audit's 0.00021 and 0.00077
  were treated as a diagnostic and matched without tuning. Forward iteration exact as before; A4, 1927-2004: `b_r`
  0.066 (was 0.064), `b_ε` -0.0029 (was -0.0052), long-run shares 0.49 and 0.49 (were 0.47 and 0.49); 1872-2025: 0.21
  and 0.76 (were 0.20 and 0.76). Parts B and C keep their CRSP-based return definitions; their output is unchanged.
- *Clark-West inference.* Confirmed: the entry's size statement lacked the source's regime and qualifications. Restored
  from pp. 8-12: `R, P -> ∞` with `P/R` to a finite nonzero constant; one-step, conditionally homoskedastic forecasts;
  numerically computed quantiles for dim(Z) <= 20 and P/R from 0.1 to 20, all 400 recursive entries within (4.2), 4 of
  400 rolling entries with a 0.90 quantile of 1.29; no formal proof and not asserted as literally true; (4.3) with 1 and
  14 exceptions; the dim(Z) = 1 extension. The 48-design result is now presented as simulation evidence (pp. 2,
  15-17), not a guarantee. Locators corrected: eq. (4.1) is on p. 8 (was p. 7), eq. (4.2) on p. 9 (was p. 8).
- *Monte Carlo gap.* With both simulations' errors, the protocol run is 3.0 (P = 120) and 2.3 (P = 240) standard errors
  below Table 1. A bounded investigation (B3b, seed 20261104, 20,000 replications, reported only) used the source's
  design: one R + 720 path shared by every P, stationary initial draw, no observed lag for `y_1`, recursive and rolling
  schemes, the ordinary t statistic. It reproduces the rolling means quoted on p. 16 (-0.247, 0.005, 0.252 against
  -0.24, 0.01, 0.25) and gives recursive sizes 0.0722, 0.0657, 0.0551 against 0.085, 0.070, 0.054 and rolling 0.0722,
  0.0730, 0.0856 against 0.085, 0.078, 0.091. Exploratory runs on common random numbers showed that indexing and the
  variance divisor move the sizes by at most 0.0004. The gap is confined to P = 120 (about 0.013, three standard errors,
  both schemes) and is retained as an unresolved reproduction result.
- *Checks added.* A0 (the working-paper point on three declared returns; the steady state where both points agree), A1
  over every year, the A2 remainder identity and bounds, the two-sided size gap, B3b, and drift checks for the corrected
  values. Mutation tests on a scratch copy: restoring the mean log return fails A0 and the recorded values; restoring
  CRSP returns in part A fails A1, every A2 remainder check and the recorded values. 47 checks pass (39 before).
- *Records updated.* The entries `res:campbell-shiller-identity` and `meth:nested-forecast-tests`, their evidence
  records and coverage evidence, the two reading notes, the pathway backlog, `content_development_plan.md` (status,
  sources, files, section 7 and 7.1, deferred) and this record. `meth:restricted-forecast-value` needed no change. No
  entry, pathway or objective was added, the forecast-combination work was not started, and the guide, the historical
  migration and alignment records, the other 697 entries and every mastery state are unchanged.

**Validation after the audit (22 October 2026).** `make check` (exit 0): lock check; ruff lint and format (160 files;
`superseded-*` folders are excluded by configuration); `check_compendium.py --check` (700 entries, 0 problems);
`check_coverage.py --check` and `--verify-outlines` (0 problems; 453 objectives, 452 covered, 1 missing); `make test`
(59 passed); `make examples` (128 scripts, warnings as errors); `make pdf`: 464 pages, no overfull boxes, no undefined
references, the one pre-existing underfull box. Printed pp. 35-38 (PDF 41-44) rendered and read: the new
four-row identity table, the size discussion and the links display correctly. `make pre-commit` (exit 0, no file
changed). Entry preservation: against `HEAD`, 697 entries keep labels, types and files, 693 byte-identical and four
differing only by the batch's navigation links; against the pre-audit working tree, only the two corrected entries
differ. `guide/`, `content_migration_plan.md`, `content_migration_ledger.md`, `subsection_alignment_plan.md` and
`notes/log.md` are unchanged against `HEAD`.

## Forecast-combination and proper-scoring batch (22 October 2026)

**Starting state.** `main` at `2561b34` (merge of PR #37), clean; guide pin `8302467`; 700 entries, 112 printed
pathways, 464 PDF pages; objectives 453 (452 covered, 1 missing). Branch `codex/forecast-combination-scoring`. GitHub
Actions run 39790431215 (the post-merge source validation of `2561b34`) was `in_progress` when the batch started, with
its only job, *Source validation*, already successful; it completed with conclusion `success` during the batch and
was not cancelled, rerun or changed. Scope set by the request: at most two entries under `return-predictability`
(combining point forecasts; proper scoring of distributions and intervals). Local only; nothing committed or pushed.

**Sources read** (equations and tables as page images; downloads logged with URL, time, status, size and SHA-256 in the
git-ignored `reading_materials/forecast-combination-scoring/download-log.tsv`):
- Gneiting and Raftery, JASA 102(477), 2007, the author-hosted copy of the journal's typeset article
  (`sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf`, SHA-256 `d31a0c5f...7ba2`, 20 pages;
  PDF page = printed page - 358): pp. 359-360 (orientation, eq. (1)), 365 (eq. (19)), 366 (locality, linear score),
  367 (eqs. (20)-(23), the Gaussian CRPS), 370 (eqs. (40)-(43)), 371 (eqs. (44)-(47), Table 2) and 374 (sensitivity of
  the log score). Catalogue key `wide-gneiting-raftery`.
- Rapach, Strauss and Zhou, "Out-of-Sample Equity Premium Prediction: Consistently Beating the Historical Average",
  working paper of 6 February 2008 (first draft 23 July 2007). Zhou's copy (`apps.olin.wustl.edu/faculty/zhou/RSZ.pdf`)
  returns 404; the Wayback Machine capture of 2016-06-16 (same digest as that of 2014-12-22) was used, SHA-256
  `c8dab2ae...f909`, 38 pages, printed page = PDF page - 1. Read: secs. 1-2 (pp. 1-12), 3.1-3.2 (pp. 12-19), 3.6 and 4,
  the notes to Tables 1-4 and Table 1 (PDF pp. 29-30). Registered as `rapach-strauss-zhou-2008-wp`.
- Not obtained: the RFS 2010 article (`wide-rapach-strauss-zhou`, doi 10.1093/rfs/hhp063). doi.org, academic.oup.com
  and SSRN 1257858 returned HTTP 403 on 2026-10-22; archived `rfs.oxfordjournals.org` full-text pages are sign-in
  pages; Zhou's archived *Notes_Data_Code_RSZ2010.pdf* (SHA-256 `b5f6fa64...77d7`) points to data and code only.
  Nothing is attributed to the published version. `wide-timmermann-combinations` and `wide-giacomini-white` were not
  sought.
- Data: the workbook already hashed by the earlier batch (`8d210b77...be872`, 2026 vintage despite its label); new
  columns `E12, tbl, AAA, BAA, lty` extracted by `goyal_extract_predictors.py`. The earlier CSVs are unchanged.

**Discrepancies and source limits.**
- The working paper prints the historical average as `r-bar_{t+1} = sum_{j=1}^t r_j` without the 1/t (p. 4); read as
  a typesetting slip, not used.
- Its Table 1 labels the discounted method "DMSFE"; the text says DMSPE (p. 5).
- It sets the restricted forecasts' expected signs from full-sample estimates (n. 9, p. 8) and notes that the
  Clark-West test has not been analysed for combination forecasts (n. 11, p. 9); both are stated in the entry.
- The working paper contains no forecast-error covariance argument for why combination works. That argument, the
  ambiguity decomposition and the equicorrelated floor are labelled Interpretation and checked numerically.
- Gneiting and Raftery do not state the burn-in, seed or J's unconditional quantiles behind Table 2; they are set or
  estimated in the protocol. They do not discuss linear pools; the pool example is labelled Interpretation.

**Entries.** New: `meth:forecast-combination` (Method 8.11) and `meth:proper-scoring-rules` (Method 8.12) at the end
of `compendium/asset-pricing/return-predictability.tex`, the pathway's only topic file (section 8.3). Navigation only:
See also of `meth:nested-forecast-tests` gains `meth:forecast-combination`; See also of
`meth:forecast-accuracy-evaluation` gains `meth:proper-scoring-rules`. Registered source:
`rapach-strauss-zhou-2008-wp` in `compendium/front/sources.tex`.

**Coverage.** `objective:score-and-combine-return-forecasts` moves from missing to partial: both new entries mapped,
with sources, locators, reading notes, entry evidence and worked examples. Next action stays obtain-source, because
conditional predictive ability (`wide-giacomini-white`) and tests of equal average scores are unwritten. Its title is
unchanged. The scope of `topic:return-predictability` now names what is written. Objectives 453: 452 covered, 1
partial; outline items unchanged at 1,030/1,030 (no item maps to this objective). The pathway checkpoint was not
attempted. Nothing in `notes/log.md`; no study or mastery claimed.

**Checks.** `notes/artefacts/return-predictability/`: `forecast-combination-scoring-protocol.md` (predictors, sample,
rows, transformations, seeds and tolerances written before the script existed, after the published tables had been
read; not a preregistration); `goyal_extract_predictors.py` (empirical group); `goyal-annual-predictors-1871-2025.csv`;
`forecast-combination-scoring-checks.py` (numpy, pandas, scipy, default environment, about 4 s) and
`forecast-combination-scoring-results.txt`.
- First run: all 55 gated checks passed; seven drift checks of observed values were then added (part R), bringing that
  run to 62 checks. The post-first-run audit added two exact deterministic checks; the current total is 64. Seeds
  20261105-20261108; Python 3.14.7, NumPy 2.4.6, pandas 3.0.5, SciPy 1.18.1.
- Part F (annual log premium; dp, ep, tms, dfy dated t - 1; recursive from 1927; first forecast 1947): R2_OS
  1947-2025 -1.83, -2.28, -3.60, -0.83, equal-weight combination +2.56 (ΔRMSE +0.21, Clark-West t 1.44, descriptive);
  1947-2005 +1.34, +4.61, -3.70, -1.00, combination +5.82 (t 2.13). Error correlations 0.89-0.98, deviation
  correlations -0.30 to 0.82; MSE_c 2.6500 = 2.7777 - 0.1277 (x100); ex post minimum-MSE weights -0.02, 0.51, 0.40,
  0.12 (MSE 2.6380). The combination was not required to win, and this is not a reproduction of the working paper's
  monthly Table 1 (0.95 percent for the mean combination).
- Part S: normal CRPS closed form against quadrature of eq. (20) (at most 1.4e-14) and Monte Carlo of eq. (21); the
  interval score against the sum of two quantile scores (1e-12); propriety on a grid (each proper loss smallest at the
  true s = 15; linear score largest at the smallest s); Table 2 in the source's design: coverage 94.98, 94.91, 94.94
  (published 95.01, 95.08, 94.98), widths 4.00, 5.46, 3.79 (4.00, 5.45, 3.79), interval scores 4.76, 8.03, 5.29
  (4.77, 8.04, 5.32), batch-means standard errors 0.024, 0.098, 0.065; linear pool against N(4, 10^2) under the pool:
  log loss 3.7957 against 3.8015, CRPS 6.0816 against 6.0903.

**Limits.** Editorial coverage only; human review outstanding. Working-paper locators for the combination entry; one
annual predictor set and one evaluation window (with a sub-window); a 2026 data vintage; Gaussian illustrative
forecasts. Deferred: Giacomini-White conditional tests, tests of equal average scores, the pathway checkpoint, the
SVIX bound, the real-time kernel check, density combination beyond the pool example, and further investigation of the
Clark-West size gap at P = 120.

**Validation (22 October 2026).** `make check` (exit 0): lock check; ruff lint and format (163 files);
`check_compendium.py --check` (702 entries, 112 pathways printed, 96 pathway notes, 0 problems); `check_coverage.py
--check` and `--verify-outlines` (0 problems; 453 objectives, 452 covered, 1 partial; 1,030 items covered); `make test`
(59 passed); `make examples` (129 scripts, warnings as errors); `make pdf`: 466 pages (was 464), no overfull boxes, no
undefined references, the one pre-existing underfull box. Section 8.3 still starts on printed p. 35; the new entries
are on printed pp. 38-40 (PDF 44-46), rendered and read: headings, equations, the five tables and the links display
correctly. `make pre-commit` (exit 0). Entry preservation against `HEAD`: 700 entries keep labels, types and files;
698 are byte-identical and two differ only by the inserted See-also links. The earlier batch's check script still
reproduces its recorded output byte for byte. `guide/`, `content_migration_plan.md`, `content_migration_ledger.md`,
`subsection_alignment_plan.md` and `notes/log.md` are unchanged against `HEAD`.

**Post-first-run audit corrections (22 October 2026).** The equal-variance equicorrelation expression is now scoped to
unbiased errors; individual biases add the squared mean bias. Two exact deterministic checks use member biases 1, 2 and
3 to verify `MSE = variance + mean bias squared` (`116/27 = 8/27 + 2^2`) and both the second-moment and ambiguity
identities (`116/27 = 116/27 = 50/9 - 34/27`). The Bates-Granger wording now makes explicit that inverse-MSE
optimality needs unbiased, uncorrelated errors (a diagonal error second-moment matrix); this is marked Interpretation,
since the working paper says "forecasts are uncorrelated." The annual predictors are calendar-indexed at `t - 1`; no
publication lags or revisions are modeled, especially for E12, so the data do not establish point-in-time availability
or a real-time investable backtest. The normal comparison in the density example is identified as an assumed density
with the average component variance; point forecasts alone determine neither variance nor predictive distribution.
The data, forecast results, scoring results and original first-run protocol history are unchanged. The focused script
was rerun under `-W error`; 64 checks pass. The repository-wide validation above predates these corrections.

**Publication validation (22 October 2026).** After the corrections, `make check` passed: 59 tests, 129 numerical
scripts, structure and coverage checks, outline hashes, and the PDF build. The PDF remains 466 pages; printed
pp. 38–40 were rendered and inspected, with no overfull boxes or unresolved references and only the existing
underfull box. The earlier return-predictability script still reproduces its recorded output exactly. All 700 earlier
labels, types and file locations are preserved; only the two documented navigation links change their bodies.

## Conditional predictive ability entry (22 October 2026)

**Starting state.** `main` at `4c95e3e` (merge of PR #38), clean; 702 entries, 112 printed pathways, 466 PDF pages;
objectives 453 (452 covered, 1 partial). PR #38's CI run 39803945461 (on its head `5444074`) concluded `success`; no
check runs are reported for the merge commit itself. Branch `codex/conditional-predictive-ability`. Scope set by the
request: at most one entry under `return-predictability`. Local only; nothing committed or pushed.

**Sources read** (equations and tables as page images; downloads logged with URL, date, status, size and SHA-256 in the
git-ignored `reading_materials/conditional-predictive-ability/download-log.tsv`):
- Giacomini and White, "Tests of conditional predictive ability", authors' version "This version: April 2006", whose
  acknowledgement thanks the Editor and three referees. `GiacominiWhite04.pdf` from Giacomini's former UCLA page, Wayback
  Machine capture of 2006-09-20, SHA-256 `2d937c5c...f15a7`, 31 pages, printed page = PDF page. Read: secs. 1-5 and
  6.2-6.4, appendix proofs, Table 1; pp. 5-13 as page images. Registered as `giacomini-white-2006-wp`.
- Not obtained: the Econometrica article (`wide-giacomini-white`, 74(6), 2006, 1545-1578). Wiley and a UCL copy returned
  HTTP 403 on 2026-10-22, and no Wayback snapshot of the UCL copy exists. Unpaywall and Semantic Scholar list only the
  2003 Boston College working paper, which was not used. Nothing is attributed to the journal's pages. The catalogue
  record itself says the full text was not inspected; no verification is inherited from it.
- Zhu and Timmermann, arXiv:2006.03238v2 (submitted 19 August 2022), SHA-256 `afed6367...4cea`, 30 pages, printed
  page = PDF page. Read: secs. 1-5 and the proofs of Propositions 1, 2, 5 and Lemma 1; pp. 5-8 and 13-18 as page images.
  Version 1 (5 June 2020, SHA-256 `4f4b6627...846c`) was compared for its abstract and section list only. It claimed
  that the null cannot be valid under a rolling window; version 2 states a necessary and sufficient condition.
  Registered as `zhu-timmermann-2022-arxiv`.
- Data: `goyal-annual-predictors-1871-2025.csv` from the previous batch, unchanged (2026 vintage, workbook SHA-256
  `8d210b77...be872`).

**Discrepancies and source limits.**
- Giacomini and White's copy refers to its unconditional and conditional tests as "Theorems 5 and 6" (pp. 15-17, 19),
  although they are numbered 1-4 in the same copy; locators use the copy's numbering.
- Zhu and Timmermann's Proposition 6 (p. 14) gives V_4 = 0.677 for Gaussian errors. The autocovariances derived here give
  `V_m = (2m + 1)/(3m)` = 0.75, and the simulation gives 0.755 (se 0.011); the two agree only at m = 1.
- Their Table 2 (p. 18; 0.196 and 0.158 at λ = 0.25 and 0.5) is not reproduced. A direct simulation of Example 5 gives
  0.057 and 0.054. The limit derived here gives 0.054 and 0.053. Eq. (14) as printed, with the opposite sign on its
  second term, gives 0.149 and 0.117.
- The proof of their Proposition 5 writes `Z = -2 y_t ε` and `E Y²` where the statement's `E Y⁴` is correct; this was
  noted, not used.
- Giacomini and White's own power simulations (sec. 5.2) generate loss differences directly; the entry's simulations
  instead derive each null from a DGP and two forecasting methods.

**Entries.** New: `meth:conditional-predictive-ability` (Method 8.13) at the end of
`compendium/asset-pricing/return-predictability.tex`. Navigation only: the See also fields of
`meth:nested-forecast-tests` and `meth:proper-scoring-rules` gain a link to it. Registered sources:
`giacomini-white-2006-wp`, `zhu-timmermann-2022-arxiv` in `compendium/front/sources.tex`.

**Coverage.** `objective:score-and-combine-return-forecasts` moves from partial to covered. Its stated operations are
calculate, compare and test, over combining forecasts, scoring density or interval forecasts with proper scoring rules,
and conditional tests. The new entry adds the missing operation: unconditional and conditional tests of equal
predictive ability, computed on squared-error and CRPS loss differences of Gaussian predictive densities. The CRPS
case is also a test of equal average scores. The remaining limits are of source version and scope, not of operation.
They are kept in the pathway backlog: Giacomini-White from the authors' version, Rapach-Strauss-Zhou from the 2008
working paper without the RFS version's real-economy links, and interval-score differences not tested on data.
Objectives 453: 453 covered. Outline items unchanged. The pathway checkpoint was not attempted. Nothing in
`notes/log.md`; no study or mastery claimed.

**Checks.** `notes/artefacts/return-predictability/`: `conditional-predictive-ability-protocol.md` (hypotheses, designs,
windows, instruments, losses, seeds and acceptance criteria written before the script existed, after the sources and
their tables had been read; not a preregistration); `conditional-predictive-ability-checks.py`;
`conditional-predictive-ability-first-run.txt` (the first run, kept unchanged); `conditional-predictive-ability-results.txt`.
- First run: 41 checks, 39 passed. Both part X gates failed (rates above 0.10 expected from ZT Table 2; observed 0.0567
  and 0.0538). The gates were not loosened: the lines now print as a failed reproduction, and the rates are recorded
  values. Post-run supplements P1 (exact V_m) and P2 (limit with both signs, seed 20261115) were added, then drift
  checks (part R). The script then reported "52 checks, 0 failed" without separating the failed gates; the current
  accounting is in *Correction and final-validation pass (23 October 2026)* below. Seeds 20261109-20261115; Python 3.14.7, NumPy 2.4.6, pandas 3.0.5, SciPy 1.18.1.
- V: the Wald statistic agrees across exact rational arithmetic, a linear solve and n R² (hand example T = 3087/2005).
  Rank-deficient instruments (a duplicated column; a second constant beside the intercept) raise an error; the pseudo-inverse statistic equals the reduced one (df = rank).
  Multi-step and HAC covariances match hand loops.
- H (states, n = 120): unconditional rejection 0.0518, conditional with h = (1, S) 1.0000. N (null true by
  construction): 0.0417/0.0443 (n = 120) and 0.0465/0.0508 (n = 1000). U (unconditional true, conditional false, m = 4,
  n = 1000): mds variance 0.0237, uniform HAC 0.0552, Newey-West 0.0444, subsample t 0.0459, h = (1, f1) 0.0442,
  h = (1, f1²) 0.7881; derived moments within 3 se. C (equal population models): mean L_M - L_D = -0.0969 (se 0.0004);
  the conditional test rejects 0.9985.
- E (fixed 20-year window, annual log premium on lagged log dp): R2_OS of the rolling regression against the rolling
  mean is 3.40 percent (1947-2025) and 1.22 (1947-2005). DM t with Newey-West: 0.50 (p 0.62) squared and 0.31 (p 0.75)
  CRPS. Conditional T with h = (1, ΔL_t): 2.73 (p 0.26) and 3.01 (p 0.22); no p-value below 0.2 in either sample. The
  1947 forecasts equal the earlier recursive ones. Predictor years are calendar-indexed: no publication lags or
  revisions, so not point-in-time.

**Limits.** Editorial coverage only; human review outstanding. Authors'-version locators for Giacomini-White.
Asymptotics with n = 78 and 58 are rough. The Gaussian predictive densities are an assumption. Deferred: the pathway
checkpoint, further predictor searches, the SVIX bound, kernel methods, the Clark-West size gap at P = 120, Zhu and
Timmermann's skewed-error Table 1 and J test, and multi-step conditional tests on data.

**Validation (23 October 2026).** `make check` (exit 0): lock check; ruff lint and format (165 files);
`check_compendium.py --check` (703 entries, 112 pathways printed, 96 pathway notes, 0 problems);
`check_coverage.py --check` and `--verify-outlines` (0 problems; 453 objectives, 453 covered); `make test` (59 passed);
`make examples` (130 scripts, warnings as errors); `make pdf`: 467 pages (was 466), no overfull boxes, no undefined
references, the one pre-existing underfull box. The new entry is on printed pp. 40-41 (PDF 46-47) and was rendered and
read: headings, equations, both tables and the links display correctly. The sources page (PDF 457) was also read.
`make pre-commit` (exit 0). Entry preservation against `HEAD`: all 702 earlier entries keep their labels, types and
files; 700 are byte-identical, and two differ only by the inserted See-also links. The two earlier check scripts and
the new one reproduce their recorded outputs byte for byte. `guide/`, `content_migration_plan.md`,
`content_migration_ledger.md`, `subsection_alignment_plan.md`, `notes/log.md` and `superseded-first-run/` are
unchanged against `HEAD`.

### Correction and final-validation pass (23 October 2026)

Same branch, uncommitted, on top of the work above; earlier experiments, the first-run output, `guide/`, the
migration and alignment records and `notes/log.md` are untouched. The *Validation (23 October 2026)* paragraph above
describes the state before this pass and is superseded by the validation below.

**Corrections.**
- *Singular covariance (entry, Conditions).* The entry said Ω̂ is singular if an instrument "is constant over the
  sample". Wrong: Ω̂ = n⁻¹Z′Z is singular exactly when Z = hΔL has rank below q. A single constant h = 1 is valid
  (Ω̂ is then the mean of ΔL²); a second constant, or an indicator that never changes, is redundant only beside an
  intercept. Checked against V1 (h = (1, a), full rank), V3 (h = 1 accepted) and V5 (duplicated column, h = (1, 2):
  both rank deficient); no test was added. The checks bullet above now reads "rank-deficient instruments".
- *Verdict accounting.* The first run (41 checks, 39 passed, both part X gates failed) stands and its output is
  unchanged (SHA-256 `c46e1ba7…9235`). The script used to print those gates as text and then report "52 checks, 0
  failed". `reproduction_gate()` now reports them under their original criterion, not counted as checks, and the
  summary gives two tallies: 53 correctness and regression checks run, 0 failed (39 protocol checks in V–E, 6 post-run
  supplements, 8 recorded values); 2 historical reproduction gates evaluated, 0 met. The protocol has an appended
  *Amendment, 23 October 2026*; its original criteria are unchanged. No seed, threshold, design or observation was
  changed. The recorded output differs from the previous one only in the two gate lines, one new P1 line and the
  summary (checked with `diff`).
- *Source discrepancies,* read as page images from the cached
  `reading_materials/conditional-predictive-ability/src/ZhuTimmermann_arXiv2006.03238v2.pdf` (SHA-256 re-checked).
  (a) Proposition 6, proof pp. 24–27: eq. (23), p. 25, writes the fourth moment of a sum of k errors as
  `k(k − 1) + kκ₂`, missing the factor 3 for the three pairings; the same omission occurs before eq. (28), p. 26.
  The printed steps give 88/130 exactly; with the factor they give `V_m = (2m + 1)/(3m)`, 3/4 at m = 4. A new exact
  check in P1 records both. A general corrected form for skewed errors was derived and compared with a scratch Monte
  Carlo (reading note): exploratory, not repository-verified evidence, and not used in the entry; Table 1 was not
  re-simulated. (b) Proposition 8: the proof's eq. (30),
  p. 28, gives `Σ ΔL → A + 2N` and `Σ ΔL² → 4I`, so the limit is `A/(2√I) + N/√I`, with ΔL ordered as in eq. (29),
  as the script implements. Eq. (14), p. 17, prints a minus sign. Reversing the loss ordering would flip both terms
  together, so it cannot reconcile the two. (c) Table 2 is reproduced by neither sign (0.054/0.053 and 0.149/0.117
  against 0.196/0.158) and stays unexplained. The entry carries one qualified sentence for each point; derivations are
  in `notes/readings/zhu-timmermann-2022-arxiv.md`.
- *Versions.* `giacomini-white-2006-wp` remains the authors' April 2006 version; no locator is attributed to
  Econometrica (entry, reading note, sources page and evidence checked).
- *Coverage.* `objective:score-and-combine-return-forecasts` re-assessed against `notes/coverage/README.md`
  ("a reviewed entry performs every operation at the stated depth, with substantive sources, review evidence and,
  for a calculation, a worked example"). Combine (`meth:forecast-combination`), score with proper rules
  (`meth:proper-scoring-rules`) and test, conditionally and unconditionally (`meth:conditional-predictive-ability`,
  squared-error and CRPS differences on data) are each still supported, at analysis depth. Kept covered. The
  source-version limits stay in the pathway backlog. This is editorial coverage, not learner mastery: nothing in
  `notes/log.md`, checkpoint not attempted.
- *Records updated:* entry; script, recorded output and protocol amendment; `notes/entry-evidence.json`;
  `notes/coverage/objectives.json` (Zhu–Timmermann locators gain the proof pages); this record;
  `notes/pathways/return-predictability.md`; `notes/readings/zhu-timmermann-2022-arxiv.md`;
  `content_development_plan.md` section 11.7.

**Validation (23 October 2026, after the corrections).**
- `cd notes/artefacts/return-predictability && uv run --frozen --project ../../.. python -W error
  conditional-predictive-ability-checks.py`: exit 0; output byte-identical on a second run and saved as the results
  file; "Correctness and regression checks: 53 run, 0 failed"; "Historical reproduction gates … 2 evaluated, 0 met".
- `make check`, exit 0: lock check; ruff lint and format (165 files); `check_compendium.py --check` (703 entries,
  0 problems; 112 pathways printed, 96 pathway notes); `check_coverage.py --check` and `--verify-outlines` (453
  objectives, 453 covered, 0 problems); `make test` (59 passed, 3 subtests); `make examples` (130 scripts, warnings
  as errors); `make pdf`: 468 pages (467 before this pass), no overfull boxes, no undefined references, the one
  pre-existing underfull box.
- `make pre-commit`, exit 0, all hooks passed.
- PDF pages 46–48 (printed 40–42) rendered and read: the corrected singular-covariance paragraph, the Proposition 6
  and eq. (14)/Table 2 sentences, both tables and the links display correctly; the last three lines of the entry
  (end of Pitfalls, See also) now fall on printed p. 42.
- Preservation against `HEAD`: 702 earlier entries keep labels, types and files; 700 byte-identical, two differ only
  by the inserted See-also link. `return-predictability-checks.py` and `forecast-combination-scoring-checks.py`
  reproduce their recorded outputs byte for byte under `-W error`. `git diff HEAD` is empty for `guide/`,
  `content_migration_plan.md`, `content_migration_ledger.md`, `subsection_alignment_plan.md`, `notes/log.md`,
  `superseded-first-run/` and the earlier batches' artefacts.

**Remaining limits.** ZT Table 2 unreproduced and unexplained; Table 1 and the J test not re-simulated; the
Econometrica text of Giacomini–White not obtained; human review outstanding.

### Publication pass (23 October 2026)

Same branch, before the first commit of this batch; the content and verdicts audited above are unchanged.

**Changes.**
- *Pagination (entry).* The last four lines of `meth:conditional-predictive-ability` (end of Pitfalls, See also) had
  fallen alone on printed p. 42. Reworded, meaning kept: the statistic paragraph (Ω̂ "omits autocovariances: under the
  null Z is a martingale difference"; a HAC estimator "is also valid but may lose power"); the states example
  ("Neither method is better unconditionally; conditionally, A is better after a boom"); design C's simulated mean
  moved into the parenthesis with its standard error; "D is OLS" for "method D is OLS"; "The CRPS assumes a Gaussian"
  for "uses the Gaussian … as an assumption"; two Pitfalls phrases shortened. Table C's label "equal population
  models, method null false" now sits on one row. No spacing commands, no font changes. Every locator, number, caveat
  and source conclusion is unchanged.
- *Scratch calculation.* The skewed-error general form of Proposition 6 (reading note; record above) is now labelled
  exploratory and not repository-verified: its symbolic check and Monte Carlo were not saved or rerun here.

**Source conclusions as published.** Giacomini–White: the authors' April 2006 version only; the Econometrica text was
not obtained. Proposition 6: discrepancy traced to the missing fourth-moment pairing factor 3 in its proof. Eq. (14):
sign opposite to the proof's eq. (30). Table 2: unreproduced and unexplained. Table 1 and the J test: not reproduced
or tested here. Coverage of `objective:score-and-combine-return-forecasts` is editorial; no mastery claimed, checkpoint
not attempted.

**Validation (23 October 2026, after these changes).**
- Check script rerun under `-W error`: exit 0, output byte-identical to `conditional-predictive-ability-results.txt`
  (53 checks run, 0 failed; 2 historical reproduction gates, 0 met). First-run output unchanged (SHA-256
  `c46e1ba7…9235`).
- `make check`, exit 0: lock check; ruff lint and format (165 files); `check_compendium.py --check` (703 entries,
  0 problems; 112 pathways printed, 96 pathway notes); `check_coverage.py --check` and `--verify-outlines` (453
  objectives, 453 covered, 0 problems); `make test` (59 passed, 3 subtests); `make examples` (130 scripts);
  `make pdf`: 467 pages (468 before), no overfull boxes, no undefined references, the one pre-existing underfull box.
- `make pre-commit`, exit 0, all hooks passed, no file changed; rerun after staging so that the six new files are
  in the index (`--all-files` covers only indexed files): `end-of-file-fixer` removed one trailing blank line from
  `notes/readings/zhu-timmermann-2022-arxiv.md` (inspected; no text changed); third run, exit 0, all hooks passed.
- PDF pages 46–48 (printed 40–42) rendered and read: the entry ends on printed p. 41 with Pitfalls and See also; the
  joined table row, the reworded sentences and the links display correctly; chapter 9 opens on printed p. 42.

**Remaining limits.** As above: ZT Table 2 unreproduced and unexplained; Table 1 and the J test not reproduced or
tested; the Econometrica text of Giacomini–White not obtained; human review outstanding.

## Time value and cash flows unit review, 23 October 2026

**Starting state.** `main` at `8b66412` (merge of PR #39), the expected starting commit, clean; no intervening changes. Branch `codex/time-value-cash-flows-review`. Scope set by the request: Part I, chapter 1, Section 1.1, pathway `time-value-cash-flows`, audited against the guide's full pathway outcome. Nothing beyond this unit was edited except its evidence records, the OpenStax source registration and the reading notes. Local only; nothing committed or pushed. Source checking and writing, not study.

**Outcome audited.** The guide's outcome: price finite and perpetual streams of dated cash flows, convert between compounding and quoting conventions, solve for the IRR and recognise its pitfalls, and price a forward by cost of carry with the same no-arbitrage argument. The three existing entries covered present values of bonds and equities, the Fisher relation and premia, and cash-flow additivity applied to forward rates, FX forwards and one-step options.

**Findings.**
- *Prerequisite order.* The section opened with `def:required-return-components`, which assumes nominal, real and risk-free rates, breakevens and term premia before discounting itself has been explained. A reader with algebra but no finance background met inflation risk premia before present value.
- *Missing foundations.* No entry in the section defined time value, present and future value, simple against compound interest, or stated against effective rates. The conversion formulas existed only in `def:interest-rate-measures` (rates chapter), which also states the annuity identities and the EAR without a source.
- *Missing outcome parts.* Not covered anywhere in the unit: annuity due and growing annuity, the r = g and g >= r boundaries, mixed streams, loan amortisation, IRR solution methods, the conditions for zero, one or several IRRs, and borrowing-type streams. NPV against IRR is in `meth:capital-project-evaluation`, which owns capital-budgeting ranking.
- *Forward by cost of carry.* Owned by `res:cost-of-carry-forward-price` and `meth:arbitrage-replication-carry`, in continuous compounding. This unit linked to them but did not itself carry the borrow-buy-sell-forward argument for an asset with income.
- *Vocabulary.* `meth:instrument-present-value` used coupon, face value and yield to maturity without defining them.
- *Existing figures.* Every figure in the three existing entries was rerun by `time-value-return-checks.py` and agreed; the OpenStax Fisher example (8.12 percent, sec. 7.4) was re-read and agrees. No numerical error was found in the existing entries.

**Sources read** (copies saved in the git-ignored `reading_materials/time-value-cash-flows/`, SHA-256 prefixes given):

| Source | Identity | Read |
| --- | --- | --- |
| `principles-of-finance-2026` | Dahlquist and Knight, *Principles of Finance* 2e, OpenStax web edition dated 24 June 2026 (page footer copyright 6 July 2026); prerendered HTML fetched 2026-10-23 | 7.1 (51a1c937d333b1b0), 7.2 (cba7e61e9faeaa1d), 7.3 (0621c8d4ec3cae58), 7.4 reread (71af541b401bd5b2), 8.1 (d462849f7748fdff), 8.2 (2d15f9e202d7fbf8), 8.3 (0b18a66edbf59586), 8.4 (f8a8c4d522df4f10), 9.1 (e6e1dd046787cc8f), 16.3 (b98ba80873565459), 16.5 (4d78e9b06f02779b) |
| `s7-hulloptions` | Hull, 11th Global edition, the git-ignored copy in `reading materials/` (SHA-256 8bc6e2f0...b482, printed page = PDF page) | chap. 4, sec. 4.4, pp. 101-104; chap. 5, sec. 5.5, pp. 130-131 and Table 5.3; chap. 6, sec. 6.1, pp. 152-153 |

The OpenStax pages state that the book may not be ingested into language models without OpenStax's permission. The user was told and decided that the pages should be read for citation checking; the entries paraphrase and quote short phrases only. Not obtained, and not relied on: `corp-berk-demarzo` (6th edition) and `catalogue-0233` (Tuckman and Serrat, 4th edition), both required readings of the pathway.

**Source discrepancies found** (recorded here, not in the entries except where they teach a distinction):
- OpenStax 7.4 calls the discount rate "the inverse of the growth rate"; the discount factor, not the rate, is the reciprocal of the growth factor. This is corrected in `def:time-value-compounding` Pitfalls.
- OpenStax 8.1 applies C/(R_s - G) to the current dividend. The entry states that C is the first payment, one period away, and links to the D_1 pitfall.
- OpenStax 8.2, Table 8.2: year 3 is printed as 19,846.81 (exact 19,845.81) and the total as 99,818.76 (exact 99,817.75). The text attributes the gap from the formula's 99,817.81 to rounding; it is mainly the table's 1.00 slip.
- OpenStax 8.3: the text divides by "32.781" where it means 32.871. The exact payment is 973.5020 and total interest with the exact payment 3,046.07; the table's 3,046.08 reflects rounding.
- OpenStax 16.3 prints the embroidery machine's IRR as 14.09 percent, and Table 16.11 as 14.10 percent; the exact rate is 14.0855 percent. OpenStax does not print the facility's two IRRs; they are computed here (9.1797 and 62.2488 percent).
- Added in the correction pass below: OpenStax 16.3 describes the IRR as the rate at which the NPV profile "crosses the horizontal axis"; a root need not be a crossing. OpenStax 8.2 says the annuity due "must always be larger"; for positive payments that holds only when r > 0.

**Entries.** `time-value.tex` was reordered to run from single amounts to no arbitrage; labels are unchanged.
- New: `def:time-value-compounding` (Definition 1.1), `meth:cash-flow-streams` (Method 1.2), `meth:loan-amortisation` (Method 1.3), `meth:internal-rate-of-return` (Method 1.4).
- Moved: `def:required-return-components`, from 1.1 to 1.5, text unchanged.
- Extended: `meth:instrument-present-value` defines coupons, face value and yield to maturity at first use, and its See also is updated; no figure changed. `res:cash-flow-additivity` gains a fourth consequence, the forward on an asset with known income (Hull sec. 5.5 and Table 5.3), with a discrete-compounding share example and its replication ledger; its title, Notation and Conditions are extended and no existing figure changed.
- Canonical homes kept: forward pricing in `res:cost-of-carry-forward-price`, capital-budgeting ranking in `meth:capital-project-evaluation`, reference rates and zero curves in `def:interest-rate-measures`. All are cross-referenced, not repeated. `def:interest-rate-measures` was not edited; its unsourced annuity identities now overlap with `meth:cash-flow-streams` and should be consolidated when the rates unit is reviewed.
- Derived, not sourced, and labelled "Interpretation" in the entries: conversion by equating growth factors over equal calendar time; simple-rate conversions; the geometric-series and difference-of-perpetuities derivations; the growing annuity and its r = g case; prospective and retrospective loan balances; bisection, Newton steps, Descartes' bound and conventional-stream uniqueness; the reading of the reinvestment statement; the discrete share-forward formula.

**Checks.** `notes/artefacts/time-value-returns/time-value-return-checks.py` was extended rather than replaced. New sections:
- single amounts and conversions: year-by-year crediting against the closed form, round trips between quotes, the money-market conversions both ways;
- streams: formula against summation, annuity due, future value three ways, perpetuity truncation, the growing annuity and the r -> g limit against the r = g formula, effective against nominal monthly rates, the OpenStax table slip;
- amortisation: the schedule rows, the balance prospectively and retrospectively at every date, the geometric growth of principal parts, the lender's IRR equal to the loan rate, the OpenStax auto loan;
- IRR: bisection against Newton, both roots of the facility checked by NPV = 0, no-IRR minimum over a grid, borrowing, the OpenStax machines with the crossover found as the IRR of the difference, and reinvestment at the IRR;
- share forward: a two-loan ledger, both arbitrage directions, and agreement with the continuous formula.

Boundary cases tested: r = 0, r -> 0, g = r, g -> r, no IRR, two IRRs, and a borrowing-type stream. All checks pass with warnings as errors.

**Coverage.** Four objectives were added to `topic:time-value-of-money` and marked covered (editorial coverage): `objective:convert-rate-quotations`, `objective:value-annuities-perpetuities`, `objective:amortise-loans`, `objective:solve-irr-and-recognise-pitfalls`. `objective:apply-cash-flow-additivity` now names the share forward, the Hull sec. 5.5 locator and the ledger example. The topic scope was widened to match. No outline mapping was changed or promoted.

**Notes.** New specialist note `notes/pathways/time-value-cash-flows.md`; the overview `financial-mathematics.md` was updated. `principles-of-finance-2026.md` and `s7-hulloptions.md` record the sections read. `compendium/front/sources.tex` registers the OpenStax sections read.

**Limits.** Editorial coverage only; no checkpoint attempted, no study or mastery claimed, and human review outstanding. OpenStax was read in web renderings with partly garbled equations, cited by section without page numbers. Two required readings are unread. Not covered: the modified IRR, worked irregular-date IRRs, payment frequencies that differ from compounding beyond the effective-rate conversion, and loan fees and regulatory APR.

**Validation (23 October 2026).**
- `make check` exits 0: lock check, ruff lint and format (165 files), `check_compendium` (707 entries, 112 printed pathways, 97 pathway notes, 0 problems), `check_coverage` with outline hashes (457 objectives covered, 0 problems), pytest (59 passed), 130 numerical check scripts, and the PDF (470 pages, previously 467; first recorded here as 466, corrected in the correction pass: the publication pass of PR #39 left the PDF at 467 pages).
- `pre-commit run --all-files` passes.
- The LaTeX log has no overfull boxes, warnings or undefined references. It has the one pre-existing underfull box, in `probability-statistics/statistical-inference.tex` (badness 2277), outside this unit; this line first omitted it and was corrected in the correction pass.
- PDF pages 8-12 (printed 2-6) were rendered and read. Chapter 1 opens with Definition 1.1, and the seven entries run to printed p. 6, where Section 1.2 begins. Displayed equations, the amortisation list, the IRR bullets and the cross-references display correctly, with no short last lines.

### Correction pass (23 October 2026)

**Starting state.** The uncommitted unit review above, on `codex/time-value-cash-flows-review` at `8b66412`; all of its changes kept. A bounded correction pass on Section 1.1 only; Section 1.2 was not started. Local only; nothing committed or pushed.

**Corrections.**
- `meth:internal-rate-of-return`. The IRR is defined by NPV = 0. OpenStax's "crosses the horizontal axis" (sec. 16.3) is attributed and qualified, because a root need not be a crossing. A new original example, -100, +220, -121, has NPV = -(11/(1+r) - 10)^2. NPV is never positive, and its sole distinct IRR is 10 percent, a double root of -(11x - 10)^2. No bracket has ends of opposite signs, and at an 8 percent hurdle the IRR exceeds the hurdle while NPV is -0.0343. Descartes' rule now counts positive roots with multiplicity and is stated to assume equally spaced periods. For irregular dates the entry says the argument does not apply as stated. Bracketing is stated to certify crossing roots only and to miss touching roots and pairs of roots. A numerical IRR is accepted only if it lies in r > -1 and has |NPV| <= 1e-9 sum|CF_t|, with a note that a small residual fixes a multiple root less precisely. The rule "accept if the IRR exceeds the cost of capital" is restricted to conventional investment streams, an outlay followed by inflows with a positive undiscounted sum. NPV decides when a stream has several IRRs or a multiple root. Pitfalls were revised to match. The old pitfall that asked for a sign change around a Newton solution was replaced, because a double root has no sign change.
- `meth:cash-flow-streams`. For positive payments the annuity due is larger when r > 0, equal at r = 0, and smaller when -1 < r < 0; OpenStax's "must always be larger" (sec. 8.2) is attributed. The domains are stated:
  - finite streams need r > -1;
  - the level closed forms also need r != 0, with NC at r = 0;
  - the growing annuity needs g > -1 and r != g, with a separate r = g form;
  - C/r needs r > 0, and the growing perpetuity needs -1 < g < r.

  C/r is stated to be the time-0 value of a perpetuity whose first payment is at t = 1, and the difference-of-perpetuities form is reworded to match ("starting now" was misleading). A pitfall covers applying C/r to a perpetuity paid immediately, whose value is C + C/r. The printed future value is corrected from 5,637.0929 to 5,637.0930 (exact 5,637.09296). The script already checked the exact value, so the slip was in the printed rounding only. A zero-rate and a -2 percent example were added: 5,000 for each annuity at 0 percent, and 5,314.5809 against 5,208.2892 at -2 percent.
- `meth:loan-amortisation`. The formulas are stated to need r > -1 and r != 0. The zero-rate limits are A = L/N and B_k = L(1 - k/N). The example adds the zero-rate schedule: four payments of 2,500 and balances 7,500, 5,000, 2,500 and 0.
- This record. In the unit review's validation, the PDF baseline is corrected from 466 to 467 pages, and the pre-existing underfull box is now named (both above). Two source discrepancies are added to the list above.

No label, title or source locator was changed. No other entry was edited, and no figure outside the ones named changed.

**Checks.** In `time-value-return-checks.py`, `bisect()` now raises `ValueError` when lo >= hi or when the two ends have the same sign. It returns an end, or a midpoint, at which the function is exactly zero. A helper `rejects()` tests the refusal. Every existing call has a valid bracket and still passes. Twelve checks were added, for 113 in all (101 before):
- streams: the annuity due against the ordinary annuity at 6, 0 and -2 percent by direct summation; C/r against truncated sums from t = 1 and t = 0; non-convergent partial sums at r <= 0;
- loans: the zero-rate schedule by recursion, and the closed forms at r = 1e-7 against L/N and L(1 - k/N);
- IRR: the double root's NPV against its closed form on a grid; no positive value on the grid; the root 10/11 with zero discriminant; no grid sign change, and bisection refused on [0, 0.2]; Newton's iterate passing the domain and residual test; NPV at 8 percent; bisection refused for reversed, empty and same-sign brackets; endpoint roots returned exactly (-100, +125 at 25 percent, from either side).

No general-purpose solver was built.

**Notes and evidence.** The `entry-evidence.json` records of the three corrected entries gain a dated correction-pass sentence; earlier text is kept. The `example` fields of the three matching objectives in `objectives.json` name the new checks; coverage status, sources and locators are unchanged. `principles-of-finance-2026.md` annotates the two qualified OpenStax statements. The pathway note, the section overview and the review index record the pass. The source-version limitation (OpenStax web edition of 24 June 2026, read in web renderings, without page numbers) and the unread status of `corp-berk-demarzo` and `catalogue-0233` are unchanged. No study, mastery or checkpoint is claimed.

**Validation (23 October 2026).**
- `uv run python -W error time-value-return-checks.py`: 113 checks passed, exit 0.
- `make check` exits 0. It ran the lock check, ruff lint and format (165 files), and `check_compendium` (707 entries, 112 printed pathways, 97 pathway notes, 0 problems). It also ran `check_coverage` with outline hashes (457 of 457 objectives covered, 0 problems), pytest (59 passed, 3 subtests) and 130 numerical check scripts with warnings as errors. The PDF built at 470 pages, the same as after the unit review.
- `pre-commit run --all-files` passes, and so does `pre-commit run --files notes/pathways/time-value-cash-flows.md`, the untracked note, which `--all-files` does not cover.
- The LaTeX log has no overfull boxes, warnings or undefined references. It has the one pre-existing underfull box (badness 2277), in `probability-statistics/statistical-inference.tex`.
- After the final content change, PDF pages 8-12 (printed 2-6) were rendered and read. They show the annuity-due and domain sentences, the zero-rate examples and limits, the IRR Statement, Notation bullets and double-root example, and the revised Pitfalls. The equations display correctly. Section 1.1 still ends on printed p. 6, where Section 1.2 begins.

**Limits.** Editorial correction only; human review of the unit and this pass is outstanding. The root-counting statement covers equally spaced periods only. The residual tolerance is a stated convention, not a derived bound. The source-version and unread-reading limits above are unchanged.

### Final wording and publication (23 October 2026)

Same branch, before the first commit of this batch. The wording of `meth:internal-rate-of-return` was revised; no other entry, figure, label or locator changed.

**Changes.**
- *Borrowing streams.* The reversed comparison is kept: a borrowing-type stream is worthwhile when its IRR is below the cost of capital. The Pitfalls warning against applying "any IRR rule" to a stream that is not a conventional investment contradicted it and is removed. The Pitfalls now name applying the investment rule to a borrowing stream, and applying either rule to a stream with several IRRs or a multiple root. The double-root example now says that the stream is neither a conventional investment nor a conventional borrowing.
- *Bracketing.* Bisection, and the advice that "a safe solver brackets first", are limited to cases where a sign-change bracket exists. Where none exists, candidates from Newton steps or a scan of NPV are accepted only after the domain and residual validation.
- *Positive IRR against the decision rule.* A conventional investment, outflows followed by inflows, has exactly one IRR, with NPV positive below it and negative above. The rule needs only that, and it holds when the IRR is negative. The IRR is positive exactly when the undiscounted sum NPV(0) is positive. Previously the positive sum was folded into the stream the rule applies to. The Statement, Notation and Conditions now state this.
- *Check.* `time-value-return-checks.py` adds one check, for 114 in all: -100, 50, 40 has an undiscounted sum of -10, a single IRR of -6.9926 percent found by bisection on [-0.5, 0], and NPV positive below it and negative above. The `entry-evidence.json` record gains a dated sentence, with earlier text kept.

Unchanged: the source-version limitation (OpenStax web edition of 24 June 2026, read in web renderings, without page numbers), the unread status of `corp-berk-demarzo` and `catalogue-0233`, and the earlier evidence. The coverage remains editorial: the checkpoint has not been attempted, no study or mastery is claimed, and human review is outstanding.

**Validation (23 October 2026, final state).**
- `uv run python -W error time-value-return-checks.py`: 114 checks passed, exit 0.
- All twelve batch files are staged, including the new `notes/pathways/time-value-cash-flows.md`, so `--all-files` covers them. `pre-commit run --all-files` passed, and no hook changed a file.
- `make check` exits 0. It ran the lock check, ruff lint and format (165 files), and `check_compendium` (707 entries, 112 printed pathways, 97 pathway notes, 0 problems). It also ran `check_coverage` with outline hashes (457 of 457 objectives covered, 0 problems), pytest (59 passed, 3 subtests) and 130 numerical check scripts with warnings as errors. The PDF built at 470 pages, with no overfull boxes, warnings or undefined references; the one pre-existing underfull box in `probability-statistics/statistical-inference.tex` remains.
- PDF pages 9-10 (printed 3-4) were rendered and read: the IRR Statement, Notation bullets, Conditions, double-root example and Pitfalls display correctly. Page 12 (printed 6) was checked: Section 1.2 still begins there.
- After this record was written, pre-commit was rerun on it; nothing else changed.

**Publication.** Committed on `codex/time-value-cash-flows-review` as one batch and merged into `main` by pull request. The post-merge CI run checks out the merge commit; its result is reported in the session, not here.
