# Jet-fuel cross hedge with heating-oil or WTI futures: protocol (meth:time-varying-hedge-ratio)

Written 2026-10-17 (derivatives and empirical validation (2026-10-17) that date) before any result was computed. The EIA jet-fuel file was downloaded
earlier in the same session but not opened; the heating-oil and WTI series are the ones already used in the
backwardation tests. Committed with the results, so this is a protocol recorded in advance, not a preregistration.

## Question

The commodity-hedging checkpoint asks for static, rolling-window and bivariate-GARCH hedge ratios for an exposure without
an exact contract, compared out of sample. This test does static against rolling OLS (GARCH is not part of it): for a
U.S. Gulf Coast kerosene-type jet fuel spot exposure, does re-estimating the minimum-variance hedge ratio on a rolling
window reduce hedged variance more than a ratio estimated once?

## Data

- Exposure: EIA daily spot price, U.S. Gulf Coast kerosene-type jet fuel (EER_EPJK_PF4_RGC_DPG, $/gallon).
- Hedges: NYMEX heating oil / ULSD contract 1 (EER_EPD2F_PE1_Y35NY_DPG, $/gallon) and WTI contract 1 (RCLC1, $/barrel,
  divided by 42 to $/gallon), as already retained.

## Definitions (fixed now)

- Weekly observations: the last date of each ISO week on which the exposure and the hedge both have a price.
- Changes: dollar changes per gallon from one weekly observation to the next. A week is dropped if the hedge's contract 1
  changes delivery month between the two dates (heating oil: expiry on the last business day of the month before
  delivery, EIA's definition; WTI: NYMEX Rule 200102.F, as coded in backwardation_test.expiry), so no hedge change spans
  a roll.
- Hedge ratio h = cov(dS, dF)/var(dF) by OLS of dS on dF with a constant.
- Static: h estimated once on the first 260 usable weeks and held. Rolling: h re-estimated each week on the previous 104
  usable weeks (sensitivity: 52), using only past weeks.
- Evaluation, out of sample: all usable weeks after the first 260; hedged change = dS - h dF with h known before the week;
  variance reduction VR = 1 - Var(hedged)/Var(dS).
- Verdict: "rolling helps" for a hedge instrument if VR(rolling 104) > VR(static). Reported alongside, not the verdict: the
  52-week rolling result, a full-sample (in-sample) ratio, and VR by sub-period halves.
