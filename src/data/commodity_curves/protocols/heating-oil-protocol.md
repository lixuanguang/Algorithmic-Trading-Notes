# Heating oil extension of ev:backwardation-scarcity-or-premium: protocol

Written 2026-10-17 (empirical extensions (2026-10-17) that date) before any heating-oil or distillate data were downloaded or results
computed. It is committed together with the results, so it is a protocol recorded in advance within the session, not a
preregistration. The WTI and Henry Hub v2 test and its outputs are unchanged.

## Question

Does the v2 test's distinction between scarcity and premium hold for a third storable energy commodity, NY Harbor
No. 2 heating oil / ultra-low-sulfur diesel (NYMEX "HO"), with U.S. distillate fuel oil stocks as the inventory measure?
This is the backlog's "other commodities" extension. Hedging-pressure readings are not part of it (no positions data are
used), so that half of the backlog item stays untested.

## Data (EIA, public; to be retained under reading_materials/empirical-extensions/)

- NYMEX heating oil / ULSD futures, contracts 1 and 2, daily ($/gallon): EIA series EER_EPD2F_PE1_Y35NY_DPG and
  EER_EPD2F_PE2_Y35NY_DPG (the series EIA labels for this contract; if EIA's labels or splice across the 2013
  heating-oil-to-ULSD change differ, that is reported, not repaired).
- U.S. distillate fuel oil stocks, weekly (thousand barrels): EIA series WDISTUS1, from the Weekly Petroleum Status
  Report, released with crude stocks (standard Wednesday 10:30 ET).

## Definitions and timing (fixed now, identical to the WTI rules of v2 unless stated)

- Month-end t: last trading day of a calendar month present in EIA's daily series, with data continuing into the next
  month (complete months only).
- Basis B_t = ln(C1_t) - ln(C2_t) (positive = backwardation).
- Excess return r_{t+1} of holding contract 2 from t to the next month-end t1: ln(price at t1 of the contract that was
  C2 at t) - ln(C2_t), using C1 at t1 when the contract identity holds.
- Contract identity: NYMEX heating oil and ULSD futures terminate on the last business day of the month preceding the
  delivery month (rule text not obtained in this batch; to be checked against the data by the same roll check as v2,
  scoring C1(d+1) against C2(d) around month-ends). A month pair is used only if the roll check supports a roll at
  month-end; if it does not, the extension stops and reports why.
- Inventory deviation I_t: ln(stocks) at the latest usable week minus the mean of ln(stocks) in the same ISO week over
  the previous five years; a week ending Friday F is usable at t if t >= F + 6 days (the crude rule, same release),
  or F + 11 days when 25 December or 1 January falls in F+1..F+7.
- Inference: OLS with Newey-West (12 lags), as v2.

## Hypotheses and acceptance criteria (as v2)

- S (scarcity): beta_S < 0 in B_t = a + beta_S I_t + e_t; supported if t < -2.
- P (premium): beta_P > 0 in r_{t+1} = a + beta_P B_t + u_{t+1}; supported if t > 2 AND the expanding out-of-sample
  R^2 (from 120 months) is positive with a Clark-West t above 1.65.
- No other specification is part of the verdict. Any further figure (for example an executable timing rule) is
  labelled exploratory.

## Correction recorded in derivatives and empirical validation (2026-10-17) (after the results were seen)

- The return above is the log return ln(C1(t1)/C2(t)). empirical extensions (2026-10-17)'s script took the simple return
  C1(t1)/C2(t) - 1 from the imported v2 builder, so its premium figures did not implement this protocol. The script now
  uses the log return for heating oil; empirical extensions (2026-10-17)'s run is kept in superseded-simple-return-run/. The WTI and Henry
  Hub protocols are separate and are not changed.
- "Month-end" as implemented is the last date in the month on which EIA reports both contracts. Before about 2007
  contract 2 is sparse, so 79 of the 361 selected dates precede the last date in the month on which EIA reports either
  contract (12 of them by more than five days; the largest gap is 21 days, 9 August 1996). That is the last available
  common observation, not the month's last trading day; the gap is now reported and written to the panel.
- Expiry: EIA's own definitions (Futures Prices (NYMEX), "Contract 1"; page retrieved 2026-10-17) state the rule this
  protocol assumed. The roll check, run on the intersection calendar, is consistent with it in 6 of 7 blocks but does
  not prove the exact expiry date; the NYMEX rule text was still not obtained.
