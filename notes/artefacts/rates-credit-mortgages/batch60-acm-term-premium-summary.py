"""Third batch of 17 October 2026: descriptive summary of the New York Fed's ACM term-premium estimates behind the
term-premium paragraph of mod:forward-rates-fra (backlog item ev:term-premia).

Input: ACMTermPremium.xls as published by the Federal Reserve Bank of New York (retrieved 2026-10-17, monthly sheet
'ACM Monthly', end-of-month estimates, percent). The estimates are model outputs of Adrian, Crump and Moench (2013),
not observed quantities, and are revised when the model is re-estimated; this is a description of one vintage, not a
test. Reported: the 10-year term premium ACMTP10 over the whole sample and by decade, the share of months below zero,
its extremes, and the 10-year yield split ACMY10 = ACMRNY10 + ACMTP10 (checked to rounding).
Run: python3 batch60-acm-term-premium-summary.py <ACMTermPremium.xls>   (xlrd 2.0.1). Exits non-zero on failure.
"""
import sys

import xlrd

sh = xlrd.open_workbook(sys.argv[1]).sheet_by_name('ACM Monthly')
head = sh.row_values(0)
col = {h: i for i, h in enumerate(head)}
rows = [sh.row_values(i) for i in range(1, sh.nrows)]
date = [r[0] for r in rows]
tp = [r[col['ACMTP10']] for r in rows]
y = [r[col['ACMY10']] for r in rows]
rn = [r[col['ACMRNY10']] for r in rows]
gap = max(abs(a - b - c) for a, b, c in zip(y, rn, tp))
print(f'sample {date[0]} to {date[-1]}, {len(rows)} months; max |ACMY10 - ACMRNY10 - ACMTP10| = {gap:.2e}')
assert gap < 1e-6
mean = sum(tp) / len(tp)
neg = sum(1 for v in tp if v < 0)
lo = min(range(len(tp)), key=lambda i: tp[i]); hi = max(range(len(tp)), key=lambda i: tp[i])
print(f'10-year term premium: mean {mean:+.2f} pp; below zero in {neg} of {len(tp)} months ({neg/len(tp)*100:.0f}%); '
      f'min {tp[lo]:+.2f} ({date[lo]}), max {tp[hi]:+.2f} ({date[hi]}); latest {tp[-1]:+.2f} ({date[-1]})')
for start in range(1960, 2030, 10):
    sel = [v for d, v in zip(date, tp) if start <= int(d[-4:]) < start + 10]
    if sel:
        n = sum(1 for v in sel if v < 0)
        print(f'  {start}s: mean {sum(sel)/len(sel):+.2f}, below zero {n}/{len(sel)}')
first_neg = next(d for d, v in zip(date, tp) if v < 0 and int(d[-4:]) > 1990)
print(f'first month below zero after 1990: {first_neg}')
