---
key: campbell-shiller-1986-nber
pathways: [return-predictability]
version: John Y. Campbell and Robert J. Shiller, "The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors", NBER Working Paper 2100, December 1986 (journal version RFS 1(3), 1988, catalogue wide-campbell-shiller-1988, not read). Copy used: scanned PDF from nber.org (40 pages, SHA-256 1786a383...c4f7), read as page images; printed page = PDF page - 2
sections: abstract; linearisation of the model, eqs. (1)-(5), pp. 1, 4-5; Table 1a, p. 21; Table 1b, p. 22
read:
status: draft
---

Prepared on 2026-10-22 by the return-predictability content batch from source checks, not from study: the headings that need your own reading are left empty. Used for `res:campbell-shiller-identity`.

## Question and claim

## Mechanism

## Method

## Data and timing

- Timing differs from the 1988 form used today: the log dividend-price ratio is delta_t = d_{t-1} - p_t, the previous period's dividend over this period's price (p. 4). With R_t = (P_{t+1} - P_t + D_t)/P_t (p. 5), P_t is the start-of-period price, so delta_t is the dividend yield at the end of period t - 1; with end-of-year Index and trailing D12 (Goyal) the same return is (Index_t + D12_t)/Index_{t-1}.
- Data are real: "the sample average real return on stocks" (p. 5); Table 1a uses 1871-1986 PPI-deflated and 1889-1985 CPI-deflated series (p. 21).

## Key results

- Taylor expansion of the perfect-foresight log dividend-price ratio around constant r and g: delta*_t approx sum_j rho^j (r_{t+j} - Delta d_{t+j}) + h, rho = exp(-(r - g)), eq. (5), p. 4; n. 1: r > g and rho < 1 for a finite price.
- The same model follows from linearising the one-period return, log(1 + R_t) = log(exp(Delta d_t + delta_t - delta_{t+1}) + exp(delta_t + Delta d_t)), around Delta d_t = g and delta_t = delta_{t+1} = log(exp(r - g) - 1), giving xi_t = delta_t - rho delta_{t+1} + Delta d_t - (1 - rho) h, solved forward (p. 5). "The point of linearization was taken to be the log of one plus the sample average real return on stocks, less the sample average change in log dividends" (p. 5): r = log(1 + mean R), not the mean log return.
- Table 1a (p. 21): 1871-1986 PPI-deflated, the approximate return against log(1 + R) (column ii): mean error 0.0051, correlation 0.9996, error variance / variance of the exact return 0.0008; 1889-1985 CPI-deflated: 0.0037, 0.9998, 0.0005. Against the simple return R (column i) the variance ratios are 0.0166 and 0.0158.

## Limits

Versions I-III of the discount rate, the VAR tests (Tables 2-6) and the appendix were not read for this batch. The scan's text layer is unreliable for equations; equations were read from page images. Pp. 4-5 and Table 1a were re-read as page images in the audit of 22 October 2026, which corrected the batch's script: it had computed r as the mean log return. The batch's nominal S&P 500 rows illustrate the approximation and do not reproduce Table 1a, since the extracted data hold no deflator.
