# First run of 22 October 2026, kept unchanged

These are `return-predictability-checks.py`, its printed output and `return-predictability-protocol.md` as they stood after the first run and its recorded post-run changes (39 checks passing), before the audit of the same day. They were never committed; they are kept here so that the run history survives the corrections.

The audit found two calculation errors in part A and one under-qualified statement in part B:

- **Working-paper linearisation point.** The script computed Campbell and Shiller's `rho = exp(-(r - g))` with `r = mean(log(1 + R))`. NBER WP 2100, printed p. 5, takes the log of one plus the sample average return, `r = log(1 + mean(R))`. The printed values 0.9498 (1872-1986) and 0.9501 (1872-2025) are therefore wrong; the corrected values are 0.9348 and 0.9364.
- **Mixed returns in the identity.** Part A used CRSP returns from 1926 with Goyal's `Index` and `D12`, so the exact identity was checked only for 1872-1925, a restriction the protocol (item A1, "every year") did not record, and the "approximation error" from 1926 included the CRSP-versus-index mismatch. The variance ratios 0.0023 and 0.0025, the correlations 0.9990 and 0.9988, and the decomposition slopes are superseded. With a return built from the same prices and dividends, the pure Taylor remainder gives 0.00021 and 0.00077.
- **Clark-West size.** The size statements did not carry the source's asymptotic regime and exceptions, and the comparison with Table 1 used the simulation error of one side only.

The corrected script and output are in the parent folder; the reasons are in the parent protocol's *Audit corrections* section and in `notes/source-review-records.md`, *Return-predictability content batch (22 October 2026)*. Parts B and C did not change: their numbers in these files are still current.

The script reproduces `return-predictability-results.txt` byte for byte when run from a copy of this folder that also holds `goyal-annual-1871-2025.csv` and `goyal-monthly-1871-2025.csv` from the parent folder (it reads them from its own directory). Do not cite this run's part A figures as current.
