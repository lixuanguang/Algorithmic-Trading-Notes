---
key: alpha-almgren
pathways: [execution-trading-costs, price-impact-execution]
version: Robert Almgren and Neil Chriss, "Optimal Execution of Portfolio Transactions", Journal of Risk 3(2), 2001 (DOI 10.21314/JOR.2001.041). Copy used: the authors' preprint dated December 2000, 42 pages, downloaded 2026-10-15 from a Wayback Machine snapshot (11 August 2017) of www.cims.nyu.edu/~almgren/papers/optliq.pdf, because the catalogue's author link returned "Access forbidden". Page numbers below are the preprint's; the journal pagination was not checked
sections: secs. 1.1-1.5 (pp. 7-11), secs. 2-2.3 (pp. 12-15); page images of pp. 9, 11 and 14 (checked for migration slices 8 and 10)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 8 from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Price follows an arithmetic random walk with permanent impact $g(v)$ of the trading rate (eq. (1), p. 8); each sale executes at $\tilde S_k=S_{k-1}-h(n_k/\tau)$, and $h$ does not enter the next market price (eq. (2), p. 9, page image).
- Temporary impact as a short-lived imbalance, liquidity returning after each period (p. 8).
- Linear forms $g(v)=\gamma v$, $h=\epsilon\,\mathrm{sgn}(n_k)+(\eta/\tau)n_k$, with units (eqs. (6)–(7), pp. 10–11, page image); expected cost $E(x)=\tfrac12\gamma X^2+\epsilon\sum|n_k|+(\tilde\eta/\tau)\sum n_k^2$, $\tilde\eta=\eta-\tfrac12\gamma\tau$ (eq. (8), p. 11).
- Trading trajectory $x_0=X$, $x_N=0$, $n_k=x_{k-1}-x_k$; static and dynamic strategies (sec. 1.1, p. 7); $V=\sigma^2\sum\tau x_k^2$ (eq. (5), p. 10).
- Minimum-impact (uniform) and minimum-variance (sell all in the first step, zero variance because of the discretisation) extremes (eqs. (9)–(13), pp. 11–12).
- Efficient frontier: minimise $E(x)+\lambda V(x)$, strictly convex for $\lambda\ge0$ if trades keep one sign (pp. 12–14); solution $x_j=\sinh(\kappa(T-t_j))/\sinh(\kappa T)\,X$ with $\tfrac{2}{\tau^2}(\cosh\kappa\tau-1)=\lambda\sigma^2/\tilde\eta$ (eqs. (16)–(17), p. 14, page image); monotone, never buying in a sell program unless there is drift or serial correlation (p. 14); half-life $\theta=1/\kappa$ (sec. 2.3, p. 15).

## Limits

## Implementation

## Notation map

- The paper's $\eta$ (temporary impact coefficient) and $\epsilon$ (fixed cost) are local to `def:price-impact`; the compendium's $\eta$ elsewhere is not this one.

## Connections

- Webster (`wide-webster-price-impact`, n. 3, p. 53) reads its "temporary market impact" as the instantaneous transaction cost; the preprint agrees.

## Entries

`def:price-impact` (model families; meanings of "temporary impact"); `mod:almgren-chriss-execution` (slice 10).

## Open questions

- Check the journal version's pagination and any changes from the December 2000 preprint.

## Retrieval cards
