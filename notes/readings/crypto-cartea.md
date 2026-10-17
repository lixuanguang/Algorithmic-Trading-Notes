---
key: crypto-cartea
pathways: [market-making-lob]
version: 2015 first edition, Cambridge University Press (local scan)
sections: chapter "A Primer on the Microstructure of Financial Markets", pp. 19-37 (pp. 19-33 checked for the migration pilot, pp. 34-37 for dealer-information models review); authors' errata for pp. 33-37
read:
status: draft
---

Prepared on 2026-10-14 by the compendium migration pilot from source checks, not from study: the headings that need your own reading are left empty. Progress through the book is in `notes/log.md`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Grossman–Miller, simplified to three dates and $n$ CARA market makers: date-1 price $S_1=\mu-\gamma\sigma^2\,i/(n+1)$, each market maker and LT1 hold $i/(n+1)$ until LT2 arrives (pp. 21–24).
- Participation cost $c$ lowers the number of market makers monotonically (p. 25); per-share fee $\eta$ adds $2\frac{n}{n+1}\eta$ to the discount, mostly paid by the initiating trader (pp. 25–26).
- Linear impact $\lambda=-\gamma\sigma^2/n$ on the traded quantity $i\,n/(n+1)$, and $\operatorname{Cov}[\Delta_1,\Delta_2]=-\lambda^2\operatorname{Var}[q^{LT1}]$ (pp. 27–28).
- Static limit-order depth: $\delta^{\pm,\ast}=1/\kappa^\pm$, the mean depth of the book, set up as a static stand-in for Ho and Stoll (1981) (pp. 28–30, eq. (2.3)).
- Kyle setup and semi-strong efficiency (pp. 31–32); the printed equilibrium $\lambda=2\sigma_u/\sigma$ on p. 33 is the reciprocal of the value its own step $\beta=(2\lambda)^{-1}$ implies; the authors' errata correct it to $\sigma/(2\sigma_u)$.
- Glosten–Milgrom, simplified to two values $V_H>V_L$, a fraction $\alpha$ informed and price-insensitive liquidity traders: $\Delta_a=(V_H-\mu)/(1+\frac{1-\alpha}{\alpha}\frac{1/2}{p})$, $\Delta_b=(\mu-V_L)/(1+\frac{1-\alpha}{\alpha}\frac{1/2}{1-p})$ (p. 35); the same with $p_t,\mu_t$ updated by Bayes' rule, and martingale execution prices (p. 36).
- With urgency $c_i\sim F$, half-spreads solve implicit equations and may only have the extreme solutions: market collapse (p. 37). The printed bid formula has $F(\Delta_a)$ for $F(\Delta_b)$ (errata).

## Limits

## Implementation

## Notation map

- $S_t$ trade price (house: $S$, kept); $\sigma^2$ per-period shock variance (house override in the Grossman–Miller entries); $\sigma$ for the Kyle value standard deviation (house: $\sigma_v$); $p^\pm$, $P^\pm$ arrival and fill probabilities (house override).

## Connections

- `catalogue-0496` (O'Hara) for the Kyle equilibrium; `s6-stoikov` for the dynamic quoting problem the static model leads to; `ho-stoll-1981`, `grossman-miller-1988`, `s6-kyle` and `s6-glosten` are the originals the chapter simplifies (Glosten–Milgrom checked in its 1983 working paper, `glosten-milgrom-1983`).

## Entries

`mod:grossman-miller`, `res:grossman-miller-trading-fees`, `res:grossman-miller-liquidity-measures`, `mod:static-limit-order-depth`, `mod:kyle-single-auction` (setup only; its printed $\lambda$ is corrected by the errata), `res:glosten-milgrom-half-spreads`, `res:glosten-milgrom-market-collapse`.

## Open questions

- The p. 33 value of $\lambda$ is corrected in the authors' errata (checked 2026-10-15); whether a later printing corrects the page itself is not known.

## Retrieval cards
