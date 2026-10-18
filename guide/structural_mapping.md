# Structure

How the catalogue is organised, how the learning guide draws on it, and the rules that keep links stable when entries move. Figures are as of 14 October 2026.

## Catalogue

3,893 entries in 23 chapters and 4 parts. Chapters and sections carry `catalogue-chapter-*` and `catalogue-section-*` labels.

| Part | Chapter | Sections | Entries |
| --- | --- | ---: | ---: |
| Foundations and research methods | 1. Mathematics, probability and statistics | 9 | 142 |
| | 2. Asset pricing, econometrics and forecasting | 6 | 170 |
| | 3. Machine learning and alternative data | 7 | 187 |
| | 4. Causal inference and experimental design | 2 | 53 |
| | 5. Research validation and reproducibility | 4 | 84 |
| Portfolio, pricing and trading methods | 6. Portfolio construction, risk and ALM | 7 | 185 |
| | 7. Derivatives valuation, volatility and hedging | 7 | 225 |
| | 8. Microstructure, market making and execution | 8 | 235 |
| | 9. Funding, collateral and securities lending | 4 | 96 |
| Markets and instruments | 10. Equities | 5 | 150 |
| | 11. Rates, inflation and cash instruments | 7 | 185 |
| | 12. Credit and securitisation | 11 | 197 |
| | 13. FX, macro and regional markets | 17 | 390 |
| | 14. Commodities and energy | 29 | 575 |
| | 15. Private capital | 5 | 114 |
| | 16. Property, infrastructure and natural-resource rights | 5 | 74 |
| | 17. Insurance-linked investments | 2 | 37 |
| | 18. Digital assets | 10 | 414 |
| | 19. Event contracts and prediction markets | 3 | 125 |
| Data, systems and research resources | 20. Data specifications, identifiers and sources | 3 | 41 |
| | 21. Software and research infrastructure | 4 | 92 |
| | 22. Governance and institutional controls | 2 | 47 |
| | 23. Course and research-outlet directories | 9 | 75 |

## Learning guide

The guide is organised by learning order, not by catalogue chapter: 7 parts, 38 overview sections and 203 specialist pathways, defined in [learning_routes.json](learning_routes.json). The main catalogue sources of each part's required readings are:

| Guide part | Sections | Pathways | Main catalogue chapters |
| --- | ---: | ---: | --- |
| I. Research foundations | 4 | 24 | 1–5, with model governance from 22 |
| II. Public markets and pricing | 11 | 59 | 13, 7, 11, 12, 10, with portfolio material from 6 |
| III. Portfolio financing and execution | 4 | 22 | 8, 6, 9 |
| IV. Energy and commodities | 7 | 37 | 14 |
| V. Private capital, real assets and insurance | 3 | 16 | 15, 16, 17, with some 14 |
| VI. Digital assets | 6 | 33 | 18, with venue and execution material from 8 |
| VII. Event contracts and prediction markets | 3 | 12 | 19 |

Readings cross chapter boundaries freely; a pathway's prerequisites, not its catalogue chapter, decide where it sits.

## Stable identifiers

- **Entry identifiers never change.** Each `\CatalogueEntry` identifier is a PDF named destination, the HTML anchor and the key in `learning_routes.json`. Move an entry by moving its whole block; keep the identifier.
- **Merged entries keep their old identifiers** as `\hypertarget` aliases inside the surviving entry (63 at present), so earlier links still resolve.
- **Legacy section labels** (153 `sec:*` labels from the pre-restructure catalogue) remain as navigation aliases in the sections that now hold their material. Keep them when reorganising sections.
- **Find where an entry lives** by searching the catalogue source for its identifier; `refresh_views.py` fails if a guide reading or branch points at an identifier or label that no longer exists.
