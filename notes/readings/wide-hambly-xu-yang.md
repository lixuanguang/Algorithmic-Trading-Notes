---
key: wide-hambly-xu-yang
pathways: [reinforcement-learning-trading]
version: Ben Hambly, Renyuan Xu and Huining Yang, "Recent advances in reinforcement learning in finance", Mathematical Finance 33(3), 437-503, 2023 (DOI 10.1111/mafi.12382). Copy used: arXiv 2112.04553v4, 28 February 2023 (title page dated 1 March 2023), 65 pages, downloaded 2026-10-15; text layer, printed page = PDF page. The journal version was not checked
sections: sec. 1 (p. 2); sec. 2 (pp. 3-4); sec. 2.2 (p. 7); sec. 4.2 (pp. 32-35, page images of pp. 32-33); sec. 5, sample efficiency (p. 49) (checked for execution control review)
read:
status: draft
---

Prepared on 2026-10-15 by execution control review from source checks, not from study: the headings that need your own reading are left empty.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Stochastic control needs a model; simple models are tractable but may oversimplify, realistic ones are often intractable (p. 2).
- RL learns from interaction, without exemplary supervision or a complete model of the environment (p. 3).
- Unknown transitions and rewards turn an MDP into an RL problem; learning them explicitly is model-based, implicitly model-free (sec. 2.2, p. 7).
- Almgren–Chriss in discrete form, its sinh trajectory (eq. (4.1)), and why RL is motivated: reliance on the dynamics and linear impact, and a pre-planned schedule that ignores real-time conditions (pp. 32–33).
- Reported execution studies: Almgren–Chriss combined with Q-learning, double DQN against TWAP with a final one-second step to force liquidation, policy-gradient and PPO studies (pp. 33–35); reports only, not checked.
- Sample efficiency: RL needs more samples than relevant historical data provide; non-stationarity; simulators as a response (p. 49).

## Limits

## Implementation

## Notation map

## Connections

- `alpha-laruelle` app. A.7.3 gives the stochastic-control execution model used as the benchmark.

## Entries

`mod:cartea-jaimungal-execution`.
