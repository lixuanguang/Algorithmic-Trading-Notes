# Inflation-shock row of the regime map, real-time classification: protocol

Written 2026-10-17 (third batch of that date) before the CPI vintages, TB3MS or WTISPLC were downloaded and before any
result was computed. It is committed with the results, so it is a protocol recorded in advance within the session,
not a preregistration. The recession-row test (regime_recession_test.py, v2) and its outputs are unchanged.

## Hypothesis (legacy map, def:macro-regime-asset-map, "Inflation shock")

In an inflation shock, nominal yields rise, the curve bear-steepens and commodities (energy) rise. Equities "depend on
real rates" and TIPS and currency rows are not tested (no clear sign; TIPS history too short for most of the sample).

## Regime, real time

Philadelphia Fed Real-Time Data Set, CPI (PCPI), quarterly vintages of monthly data (file pcpiqvmd.xlsx). In vintage
v, with L the last month reported: 12-month inflation pi(L) = 100 ln(P_L / P_{L-12}). Signal = 1 if
pi(L) - pi(L-12) >= 1.0 percentage point (an acceleration of at least one point over a year). The threshold is fixed
now and not varied. Vintage v is dated in the middle month of its quarter, as in the recession test; vintages with a
missing month inside the 25-month window are skipped and listed.

## Responses over the three months after the vintage month m (m+1..m+3)

- dy10   = GS10(m+3) - GS10(m)                      (FRED, monthly average 10-year yield, pp); hypothesis > 0.
- dslope = (GS10 - TB3MS)(m+3) - (GS10 - TB3MS)(m)  (FRED TB3MS, 3-month bill, monthly average); bear steepening
           means dslope > 0 together with dy10 > 0; dslope is tested on its own sign (> 0).
- oil    = 100 ln(WTISPLC(m+3) / WTISPLC(m))        (FRED, WTI spot price, monthly; a spot price, not an investable
           return); hypothesis > 0.

## Test and acceptance

Mean response in signal quarters minus non-signal quarters, Welch t; a sign is supported if it has the hypothesised
sign with |t| > 2. Reported alongside, as in the recession v2 test: a Newey-West t (4 quarterly lags) from the
regression on the regime indicator, and the number of distinct episodes. No ex-post comparison is part of the verdict.

## Deviation recorded before computing (2026-10-17, same session)

The Philadelphia Fed does not publish a quarterly-vintage CPI file (pcpiqvmd.xlsx returned the site's 404 page); it
publishes monthly vintages of monthly CPI (pcpiMvMd.xlsx). The middle-month vintage of each quarter (February, May,
August, November) is used in its place, which matches the RTDSM quarterly-vintage dating of the recession test. Nothing
else changes. The CPI vintages begin late (the first available vintage is reported, not chosen), so the sample is
shorter than the recession test's.

## Second deviation recorded before computing (2026-10-17, same session)

FRED refused or timed out for TB3MS and WTISPLC on every attempt (HTTP/2 errors and 90-180 s timeouts), so the two
series are taken from their primary publishers instead; the definitions do not change:
- TB3MS is the monthly average of the Federal Reserve's H.15 three-month Treasury bill secondary-market rate
  (discount basis). It is computed as the business-day average by month of the committed daily extract
  notes/artefacts/multi-asset-systematic-macro/h15-daily-3m-10y.csv (column tb3m_discount).
- WTISPLC is replaced by EIA's monthly Cushing WTI spot price (series RWTC, monthly, dollars per barrel), the response
  being 100 ln(RWTC(m+3)/RWTC(m)). EIA's series begins in January 1986, before the CPI vintages begin.
GS10 is the FRED file already retained for the recession test (reading_materials/batch40/empirical/fred/GS10.csv).

## Correction recorded in the fourth batch of 17 October 2026, before the quarterly-vintage results were computed

The first deviation above is wrong. The Philadelphia Fed does publish quarterly vintages of monthly CPI: the file is
cpiQvMd.xlsx (column headers CPIyyQq), linked from https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/cpi
(page dated 2 October 2026; retrieved 2026-10-17, SHA-256 57d28f99...). The third batch requested pcpiqvmd.xlsx, a name
formed from the monthly file's root, and that request failed; the failure was not evidence that no quarterly file exists.

The collection documentation (specific notes for CPI and for PCPI; general notes on non-NIPA variables, last updated
22 December 2016, sec. II and IV) says the two files are timed differently: quarterly vintages reflect data available on
the 15th of the middle month of the quarter and include no release published after the 15th, while monthly vintages
reflect data available just after the BLS's monthly CPI report, which may fall a few days before or after the 15th. So
the May monthly vintage may contain April's CPI when the May quarterly vintage does not, and the two can differ around
release day. The middle-month monthly vintage is therefore not the quarterly vintage the protocol named.

The original protocol is now implemented with the actual file, in batch70_inflation_quarterly_test.py:
- regime, signal rule, threshold, response definitions, dating (vintage month = middle month of the quarter), skip rules,
  test and acceptance rule: exactly as in the sections "Regime, real time" to "Test and acceptance" above;
- the second deviation (H.15 bill rate and EIA RWTC in place of FRED TB3MS and WTISPLC) still applies, because the
  response data are unchanged;
- the sample is whatever the quarterly file and the response series jointly allow (the first usable vintage is
  reported, not chosen).
The monthly-vintage run of the third batch (batch60_inflation_regime_test.py and its outputs) is kept unchanged and is
relabelled a sensitivity analysis: "monthly middle-month vintages (PCPI), a timing sensitivity". Its figures are no
longer the headline result. A comparison of the two files on their common vintage months (vintages compared, how often
the latest available CPI month differs, how many signal labels change) is reported alongside, as a diagnostic only; it
does not enter the verdict.
