---
key: s6-glosten
pathways: [market-making-lob]
version: checked in the working-paper version only, Northwestern CMS-EMS Discussion Paper 570, August 1983 (compendium source key glosten-milgrom-1983), a scan retrieved from the Internet Archive's snapshot of the Kellogg-hosted PDF; the catalogue names the 1985 Journal of Financial Economics article, not consulted
sections: working paper secs. I-IV, pp. 1-25 (checked for migration slice 2)
read:
status: draft
---

Prepared on 2026-10-15 by migration slice 2 from source checks, not from study: the headings that need your own reading are left empty. Locators in the entries are to the 1983 working paper and may not match the journal version.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Competitive, risk-neutral specialists earning zero expected profit on each purchase and each sale set $A_t=\mathbb{E}[V\mid S_t,Z_t>A_t]$, $B_t=\mathbb{E}[V\mid S_t,Z_t<B_t]$, with reservation price $Z_t=\rho_t\mathbb{E}[V\mid F_t]$ (p. 6).
- Proposition 1: $A_t\ge\mathbb{E}_t[V]\ge B_t$, strictly if adverse selection is possible (p. 8). Proposition 2: transaction prices are a martingale (p. 10).
- Proposition 3: with buy and sell probabilities bounded below, the root-mean-square spread over $k$ trades is at most $\sqrt{\operatorname{Var}(V)/(\alpha\beta k)}$ (p. 11); average spread of order one over the square root of volume with Poisson arrivals (pp. 18–19).
- Proposition 5: spreads widen with finer insider information, a higher ratio of informed to uninformed arrivals, or less dispersed liquidity parameters (pp. 15–16). The market can shut down, a lemons problem (pp. 9, 17).
- Section III: with discounting, observed returns are approximately a normal return plus what the uninformed expect to lose to insiders (pp. 19–23); not migrated.

## Limits

## Implementation

## Notation map

- $A_t,B_t\to a_t,b_t$; $F_t,S_t,H_t\to\mathcal{F}_t,\mathcal{S}_t,\mathcal{H}_t$; the paper's $\alpha,\beta$ (probability bounds in Proposition 3) $\to\theta_a,\theta_b$, since $\alpha$ is the fraction of informed traders in the related entries.

## Connections

- `crypto-cartea` pp. 34–37 gives a two-value simplification; Harris (`alpha-harris`, pp. 320–321) gives a simpler example, the source of the legacy $2PE$ proposition.

## Entries

`mod:glosten-milgrom`; also cited in `res:glosten-milgrom-half-spreads` and `res:glosten-milgrom-market-collapse`.

## Open questions

- Do the journal version's propositions and pages match the working paper?

## Retrieval cards
