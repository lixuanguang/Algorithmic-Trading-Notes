---
key: cfd-butz-oomen-2019
pathways: [fx-dealer-market-making]
version: M. Butz and R. Oomen, "Internalisation by electronic FX spot dealers", Quantitative Finance 19(1), 35-56, 2019 (DOI 10.1080/14697688.2018.1504167). Copy used: authors' accepted version on LSE Research Online (eprint 90485, available October 2018; manuscript dated November 2017), downloaded 2026-10-15 with a generic header; text layer, printed page = PDF page - 2. The published version was not checked
sections: abstract; pp. 1-2, 5-7 (Examples 1-2, eqs. (5)-(9), page images, slice-20 follow-up), 8 (Proposition 1, page image), 11 (calibration, page image) (checked for migration slice 20)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 20 from source checks, not from study: the headings that need your own reading are left empty. The authors were in Deutsche Bank's electronic FX spot division (disclosed on the abstract page).

## Question and claim

## Mechanism

## Method

## Data and timing

- Top-down calibration from the BIS 2016 triennial survey (p. 8).

## Key results

- Internalise against externalise (p. 1); internalisation horizon by Little's law proportional to risk limit over flow rate; skewing costs, including information leakage or signalling (p. 2).
- Eq. (8)-(9), p. 7: $L=\sum\varphi_n|n|$, $\lambda$ the arrival rate of risk-increasing trades; $L/\lambda$ is the conditional horizon of a risk-increasing trade, and $W=\tfrac12L/\lambda$ the all-trade average (risk-reducing trades wait zero). $\lambda_0$ is the baseline intensity of buys and of sells in the skew examples (Examples 1-2, eqs. (5)-(7), pp. 5-6), not $\lambda$.
- Proposition 1: all-trade $W=(R/\lambda_0)c_R/4$ (binary skew), $W\approx(R/\lambda_0)c_R/\sqrt{2\pi}$ (exponential) (p. 8).
- EUR/USD: $R=\$12.75$mn, $\lambda_0=\$3.66$mn/min, all-trade $W\approx1.39$ minutes as the authors report (p. 11, recomputed); conditional horizon of a risk-increasing trade $L/\lambda\approx2.78$ minutes (interpretation; exact stationary sum 2.774, $W=1.387$). Single-digit minutes in liquid G10, tens of minutes in many Asian and EM currencies (p. 11).

## Limits

## Implementation

## Notation map

## Connections

## Entries

`mod:fx-internalisation-horizon`; also cited in `def:fx-market-structure`.
