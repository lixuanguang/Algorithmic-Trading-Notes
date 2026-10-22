# Editorial backlog

Open work on the catalogue and guide, grouped by what would close it. A listed lead is not a recommendation, and a failed search is not proof that a resource doesn't exist. Verification standards are in [bibliographic_audit.md](bibliographic_audit.md); deliberate exclusions are in [removal_plan.md](removal_plan.md).

## 1. Verification of existing entries

- **326 entries with no entry-level check.** Carried over from the original catalogue (`verification_provenance: not-established` in [catalogue_recency.json](catalogue_recency.json)). Verify identity and version, and replace the annotation if it doesn't match the source.
- **57 title-only annotations.** No abstract could be retrieved, so the annotation covers only title, authors and venue. Read the paper and rewrite.
- **Classic papers annotated from their standard results** (for example Kaldor, Working, Margrabe, Garman–Kohlhagen, Krugman 1979). Each says it wasn't checked against the text.
- **39 entries that are not machine-verified.** Their publishers refused automated access. Check them by hand.
- **About 1,870 version records cite evidence files in `archive/`,** which has been removed. Re-verify those entries or drop the dead citations.
- **Study-guide migration additions to check against their text (22 October 2026).** Annotated from the title and standard result: Ross (1976), Johansen (1991), Yaari (1965), Constantinides (1983), Modigliani–Miller (1958), Myers (1984), Graham–Harvey (2001) and Gilson–John–Lang (1990); Sharpe (1964) and Miller–Modigliani (1961) from their opening sections. End pages are not established for seven Econometrica, *Journal of Business* and *Review of Economic Studies* papers whose Crossref records give only the first page. Read the two EU regulations on EUR-Lex, which refused automated access, in their latest consolidated versions (identified from metadata as 8 March 2026 for 2023/1803 and 5 June 2026 for the Market Abuse Regulation; the records link the original acts), and the IFRS 18 and Conceptual Framework texts, of which only the IASB pages were read. Replace IRS Publication 550 and Revenue Procedure 2025-32 each year, and recheck the UK inheritance-tax thresholds when they change.
- **Correction-pass sources to extend (22 October 2026).** Confirm on MSCI's methodology page whether editions later than March 2026 (*Global Investable Market Indexes Methodology*) and June 2026 (*Index Calculation Methodology*) exist; add S\&P Dow Jones Indices' *Index Mathematics Methodology* if its site allows retrieval, as a second provider's divisor and total-return conventions; read O'Kane chapters 12, 13, 16 and 18 and Duffie–Singleton section 5.2 and chapters 10–11, which were identified from chapter records and the author's table of contents only.
- **Not added for lack of a readable publisher page:** Luenberger, *Investment Science*, 2nd ed. (Oxford University Press page returned no content), and Mankiw, *Macroeconomics*, 11th ed. (library records only). Berk–DeMarzo and OpenStax texts cover the same ground in the guide.

## 2. Versions to recheck

Recheck working papers and preprints quarterly for a journal version. The ones flagged so far:

- Commodities and macro: Känzig (2023); Bhardwaj–Gorton–Rouwenhorst (2015).
- International markets: French–Poterba; Bian et al.; Ma–Rogers–Zhou; Koijen–Yogo; Fang–Hardy–Lewis; Bertaut–Bruno–Shin.
- Other: Hou–Wang–Chen–Härdle (crypto option pricing); Chen–Kelly–Xiu, "Expected Returns and Large Language Models"; the deferred Hansen–Timmermann sample-split paper; Goldsmith-Pinkham–Lyu (2025) on financial event studies.
- All 2025–2026 SSRN, NBER and arXiv entries.

## 3. Candidates left out for lack of a source

Add them if an abstract or an accessible primary page turns up. Other entries currently cover each topic.

| Topic | Candidates |
| --- | --- |
| Research methods | Corrado (1989) rank test |
| Commodities | Telser; Cootner; Bodie–Rosansky; Edwards–Canter; Silber (1981); Easterbrook (1986); Heinkel–Howe–Hughes (1990); Hilliard–Reis (1998); Cortazar–Schwartz (2003); Kolb (1992); Sadorsky (1999); Deaton (1999; indexed abstract belongs to another paper); Joskow (1990); Slade (1982); Wright (2001); Stoll–Whaley (2010, no DOI) |
| Commodity documents | S&P GSCI methodology; CME rulebook; OIES Brent papers; FCA Final Notice on the LME nickel suspension; UNCTAD *Trade and Development Report 2025* chapter |
| Power and carbon | Deng–Johnson–Sogomonian (2001); Uhrig-Homburg–Wagner (2009); revised Oxford offsetting principles (2025); UNFCCC Article 6.4 and ICAO CORSIA pages |
| International markets | Miller on depositary receipts; Arquette–Brown–Burdekin; Lesmond on emerging-market liquidity |
| Execution | OCC options disclosure document |
| Crypto | Li–Mayer (stablecoin shadow banking); Ruan–Streltsov (perpetuals); Chen–Deng–Nie (bitcoin implied volatility); Choi–Lehar–Stauffer (Kimchi premium); Athey et al. (2016); Marshall–Nguyen–Visaltanachoti; unpublished DeFi working papers (Chiu et al., Rivera–Saleh–Vandeweyer, Lehar–Parlour's *Battle of the Bots*, Appel–Grennan, Malinova–Park, Lyandres–Zaidelson) |
| Tokenisation and policy | IMF 2022 crypto–equity spillover note; WEF (2025), McKinsey (2024) and OECD (2020) tokenisation reports; FCA June 2026 cryptoasset policy statements; Grayscale v. SEC opinion; the reported December 2025 DLT Pilot Regime amendment |
| Event contracts | Wang (2026); Štrumbelj (2014); Ottaviani–Sørensen handbook chapter; Berg–Rietz (2003); Chen et al. (2009); MacLean–Thorp–Ziemba (2010); Kalshi's September 2026 margin filing; DFlow's tokenised Kalshi markets |

**Not added on purpose:**

- Crypto strategy families with no academic evidence yet: funding-rate and open-interest positioning, option-skew predictors, the GBTC premium trade, digital-asset treasury companies, token unlocks, copy trading.
- Corbet–Lucey papers, given the retractions of other papers by these authors.

## 4. Unidentified leads from the original sources

Need an exact title, author, date or identifier before they can be catalogued:

- **Courses:** Corcoran's *A Probability Space* series, Bilkent and UIUC graduate probability, Statisticsmatt, Stanford linear models and econometrics, the MIT/Berkeley stochastic-process videos, the IIT Madras probability playlist, *Forecasting Time Series Data*, generic Coursera/edX and MLOps courses.
- **Practitioner reports:**
  - macro and asset management: Nomura macro factors, J.P. Morgan "Flation", Citi GX, Deutsche Bank "Harvesting Risk Premia", 1990s Salomon reports;
  - AQR, Man and Bridgewater titles: *Managing Risk in a Multi-Strategy Portfolio*, *Global Value*, *Growth and Inflation Factor Risks*, *The Unsustainable Narrative*, Man's trend and deep-learning papers;
  - execution: Two Sigma, Citadel, ITG and J.P. Morgan execution studies;
  - structured notes: Goldman Sachs and UBS primers;
  - other: Axioma articles.
- **Papers:**
  - Agarwal–Naik (2000), which could be one of four papers;
  - Harvey–Liu "False Strategies";
  - "Burnside et al. (2011)";
  - Yang–Zhou–Wang (2017);
  - "Mullins, Harvey et al. (2023)";
  - Davis (2001);
  - Romano et al., "Enhanced Indexing";
  - the RavenPack "New News" titles.
- **Crypto:** Khabbaz's *Cryptoasset Derivatives*; the @laineVC volatility-surface toolbox; Amberdata "RiskFactor"; *Cybersecurity Risk and Cryptocurrency Valuation*; "On Liquidity and Incentives in Decentralized Lending"; ConsenSys protocol risk assessment; Paradigm and Cumberland reports; 1000x Group workshop; Parsec; Cryptovisor; HashKey and Huobi reports.
- **Other:** Mishra's *Research Methodology in AI, ML, and Data Science* edition; "QA-Lib" (not TA-Lib); unspecified bank or fund lending experiments and further IOSCO lending reports.

## 5. Bibliographic details still open

- Pan Yiming / Yiming Pan (SSRN 6908098): family and given-name order.
- Boulton–Shohfi–Walz payment-for-order-flow paper: the later four-author draft.
- Fabozzi, *Handbook of Structured Financial Products*: the original imprint and page count (sources give 530, 540 and 568).
- Easley–O'Hara–Yang–Zhang (2026, *Journal of Financial Markets*): online date, volume and issue.
- Grobys et al.: the accepted manuscript is embargoed until August 2027.
- University of Nicosia 2022–23 brochure: no archived copy found.
- Nielsen, *Principles of Effective Research*: identity confirmed, but the page doesn't load reliably.

## 6. Evidence gaps in private and specialist markets

Public sources cover structures but not deal-level terms or returns:

- the final appellate outcome and any bondholder recovery in the Swiss AT1 litigation;
- the full PSA, 424B2 and distribution data for the C39 CMBS deal;
- executed NAV-facility, continuation-fund and sidecar investor agreements, with actual cash flows;
- representative all-cost net returns for litigation, leasing, trade finance, royalties and collectibles;
- current Nigerian hedging, custody and funding terms, and other African markets beyond Kenya, Nigeria and South Africa;
- water rights beyond Chile and Murray–Darling, and asset-level mineral-royalty contracts.
