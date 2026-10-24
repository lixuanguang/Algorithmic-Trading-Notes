---
key: us-asset-returns-1928-2025
pathways: [portfolio-construction-risk]
version: Aswath Damodaran, "Historical Returns on Stocks, Bonds and Bills" (United States): page histretSP.html dated January 2026 and updated 5 January 2026, and workbook histretSP.xls (last saved 24 August 2026) with annual rows for 1928-2025, retrieved 2026-10-18 (workbook SHA-256 28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69). The transcribed columns are retained in notes/artefacts/portfolio-risk-return/us-asset-class-returns-1928-2025.csv
sections: sheets "Returns by year" (annual returns and summary rows), "Explanations and FAQ" and "Small Cap" (2025 note); credit, time-series and valuation batch (2026-10-20): sheet 'Returns by year', 1928-2025 (used through the transcribed CSV)
read:
status: draft
---

Prepared on 2026-10-18 by the portfolio choice and asset pricing batch from source checks, not from study: the headings that need your own reading are left empty. Used for `def:asset-class-characteristics` and `meth:required-return-on-equity`.

Also used by the credit, time-series and valuation batch (2026-10-20) for `meth:multiple-regression-formulation`, `meth:trend-models`, `def:stationarity-unit-roots`, `meth:autoregressive-forecasting`, `meth:forecast-accuracy-evaluation`, `meth:scenario-simulation-analysis`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Annual returns 1928-2025 for the S&P 500 with dividends, small caps (bottom decile), the 3-month T-bill (average rate in the year), the 10-year T-bond and Baa bonds (returns repriced from constant-maturity yields), residential real estate (Shiller/Case-Shiller, price only), gold (fixed before 1971) and CPI inflation.
- Summary rows reproduced by trading_notes.numerical.portfolio_choice.portfolio_choice_checks: arithmetic 11.85, 3.41, 4.82, 6.90, 4.38 and 7.36 percent and geometric 10.02, 3.37, 4.53, 6.63, 4.20 and 5.61 for stocks, bills, bonds, Baa, real estate and gold.
- FAQ: averages come with error; the bond return keeps a constant 10-year maturity for consistency.
- Used as data, not as a source of claims: Baa excess return regression, US inflation models, and a 60/40 scenario study.

## Limits

Published indices and models of returns, not investable funds, before costs and taxes; one country. The workbook's 1928-2025 geometric average for small caps (0.16 percent against an arithmetic 17.78) looks inconsistent and its 2025 small-cap value runs only to November, so that column is not used. Values may change in later updates.
