# Structure

How the catalogue is organised, how the learning guide draws on it, and the rules that keep links stable when entries move. Figures are as of 22 October 2026.

## Catalogue

3,956 entries in 23 chapters and 4 parts. Chapters and sections carry `catalogue-chapter-*` and `catalogue-section-*` labels.

| Part | Chapter | Sections | Entries |
| --- | --- | ---: | ---: |
| Foundations and research methods | 1. Mathematics, probability and statistics | 10 | 144 |
| | 2. Asset pricing, econometrics and forecasting | 6 | 178 |
| | 3. Machine learning and alternative data | 7 | 187 |
| | 4. Causal inference and experimental design | 2 | 53 |
| | 5. Research validation and reproducibility | 4 | 84 |
| Portfolio, pricing and trading methods | 6. Portfolio construction, risk and ALM | 8 | 201 |
| | 7. Derivatives valuation, volatility and hedging | 7 | 225 |
| | 8. Microstructure, market making and execution | 8 | 235 |
| | 9. Funding, collateral and securities lending | 4 | 96 |
| Markets and instruments | 10. Equities | 7 | 173 |
| | 11. Rates, inflation and cash instruments | 7 | 185 |
| | 12. Credit and securitisation | 11 | 197 |
| | 13. FX, macro and regional markets | 17 | 393 |
| | 14. Commodities and energy | 29 | 575 |
| | 15. Private capital | 5 | 114 |
| | 16. Property, infrastructure and natural-resource rights | 5 | 74 |
| | 17. Insurance-linked investments | 2 | 37 |
| | 18. Digital assets | 10 | 414 |
| | 19. Event contracts and prediction markets | 3 | 125 |
| Data, systems and research resources | 20. Data specifications, identifiers and sources | 3 | 41 |
| | 21. Software and research infrastructure | 4 | 92 |
| | 22. Governance and institutional controls | 3 | 58 |
| | 23. Course and research-outlet directories | 9 | 75 |

## Learning guide

The guide is organised by learning order, not by catalogue chapter: 8 parts, 49 overview sections and 222 specialist pathways, defined in [learning_routes.json](learning_routes.json). The main catalogue sources of each part's required readings are:

| Guide part | Sections | Pathways | Main catalogue chapters |
| --- | ---: | ---: | --- |
| I. Financial mathematics, statistics and numerical methods | 7 | 11 | 1–2, with numerical pricing from 7 and time-value material from 6 and 10 |
| II. Empirical finance, machine learning and research governance | 5 | 21 | 2–5, with ethics and model governance from 22 |
| III. Public markets and pricing | 13 | 67 | 13, 7, 11, 12, 10, with portfolio material from 6 |
| IV. Portfolio financing and execution | 4 | 22 | 8, 6, 9 |
| V. Energy and commodities | 7 | 37 | 14 |
| VI. Private capital, real assets and insurance | 4 | 19 | 15, 16, 17, 6, with some 14 |
| VII. Digital assets | 6 | 33 | 18, with venue and execution material from 8 |
| VIII. Event contracts and prediction markets | 3 | 12 | 19 |

Readings cross chapter boundaries freely; a pathway's prerequisites, not its catalogue chapter, decide where it sits. The 22 October 2026 migration from 7 parts and 38 sections, including the divided `common-toolkit` and `empirical-causal-research` overviews, is recorded in [study_guide_migration_plan.md](study_guide_migration_plan.md).

## Stable identifiers

- **Entry identifiers never change.** Each `\CatalogueEntry` identifier is a PDF named destination, the HTML anchor and the key in `learning_routes.json`. Move an entry by moving its whole block; keep the identifier.
- **Merged entries keep their old identifiers** as `\hypertarget` aliases inside the surviving entry (63 at present), so earlier links still resolve.
- **Legacy section labels** (153 `sec:*` labels from the pre-restructure catalogue) remain as navigation aliases in the sections that now hold their material. Keep them when reorganising sections.
- **Find where an entry lives** by searching the catalogue source for its identifier; `refresh_views.py` fails if a guide reading or branch points at an identifier or label that no longer exists.
