---
key: nyfed-sofr-averages-index
pathways: [rates-credit-mortgages]
version: Federal Reserve Bank of New York, "Additional Information about the Treasury Repo Reference Rates", HTML retrieved 2026-10-18 (SHA-256 1ab21c57fcbf917bc5183a52818e1d255ebd11ace2d1bcc632dd9bc0d31c82d4); formulas are images on the page and were read from the surrounding definitions and worked tables
sections: "Calculation Methodology for the SOFR Averages and Index"; "Details on Publication and Revisions for the Treasury Repo Reference Rates"
read:
status: draft
---

Prepared on 2026-10-18 by the correction pass on PR #24 from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:floating-money-market-yields`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- The SOFR Averages and Index "employ daily compounding on each business day"; on other days "simple interest applies, at a rate of interest equal to the SOFR value for the preceding business day"; actual days over a 360-day year. n_i is the calendar days for which SOFR_i applies (3 for most Fridays).
- Index set to 1.00000000 on 2 April 2018; the published table reaches 1.00034365 on 9 April 2018 with the Friday rate 1.75% applied for three days (reproduced in `bond-valuation-checks.py`). Custom-period averages come from index ratios; index rounding can differ from published averages at the fifth decimal.
- Rates are not published on, or for, days for which SIFMA recommends a full closure of U.S. government securities trading.

## Limits

Methodology for the New York Fed's averages and index; a note's own terms (lookback, observation shift, payment delay, rounding) govern its coupon.
