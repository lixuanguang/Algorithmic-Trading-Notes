---
key: w2-longin-solnik
pathways: [portfolio-construction-risk]
version: François Longin and Bruno Solnik, "Extreme Correlation of International Equity Markets", working-paper version of April 2000 marked "Forthcoming in The Journal of Finance" (first version May 1996), 24-page PDF with a text layer, HEC Paris working paper (hec.fr storage file 7e029195c03db20ea752b55b17924cff.pdf) read through the Internet Archive capture of 9 August 2017 (web.archive.org/web/20170809143748/...), SHA-256 b4a8c39a53bf820072cd4f412d08700b86b9cdc65007da51b9d877a0cf40fa18; published as The Journal of Finance 56(2), 2001, pp. 649-676 (catalogue entry; journal version not read)
sections: abstract (cover page); introduction, pp. 1-2; sec. 1.1 opening, p. 3 skimmed
read:
status: draft
---

Prepared on 2026-10-18 by the portfolio moments and diversification slice from source checks, not from study: the headings that need your own reading are left empty. Used for `mech:diversification-correlation`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Abstract: monthly data on the five largest stock markets, 1958-1996; multivariate normality rejected for the negative tail but not the positive tail; correlation is related to the market trend, not volatility per se, and increases in bear markets but not in bull markets.
- p. 1: conditioning a correlation estimate on realised returns misleads. Bivariate normal, zero mean, unit s.d., constant correlation 0.50, split into two halves by the absolute U.S. return (threshold 0.674): conditional correlations 0.21 (small returns) and 0.62 (large returns), although the correlation is constant by assumption. Reproduced analytically in `notes/artefacts/portfolio-risk-return/portfolio-moments-checks.py` (0.2131 and 0.6184).
- p. 2: the asymmetry rejects constant-correlation normal and constant-correlation GARCH models; implications for asset allocation are noted but not explored.

## Limits

Working-paper version; journal pagination and any revision after April 2000 were not checked. The extreme-value method and empirical tables (secs. 1-3) were not read; the entry uses only the abstract's findings and the p. 1 illustration. Direct downloads from CEPR (Cloudflare challenge) and hec.fr failed from this environment.
