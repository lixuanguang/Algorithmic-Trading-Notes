---
key: latest-pit-language-models
pathways: [financial-ml-evaluation]
version: Bryan T. Kelly, Semyon Malamud, Johannes Schwab and Teng Andrea Xu, "Scaling Point-in-Time Language Models", NBER Working Paper 35247, May 2026, as catalogued; text layer of the NBER PDF
sections: abstract; sec. 3 data (p. 5, Table 1); sec. 5 economic evaluation (p. 9); App. B (p. 22)
read:
status: draft
---

Prepared on 2026-10-17 by method validation (2026-10-17) from source checks, not from study: the headings that need your own reading are left empty. Used for `meth:time-valid-ml-experiment-record`.

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Monthly checkpoints 2013-2024 trained on chronologically filtered FineWeb text indexed by publication timestamp.
- Fine-tuning data filtered for "timeless" examples by gpt-5-nano (App. B).
- Economic test: December t-1 checkpoint embeds year-t news; OOS 2014 to May 2020 on Dow Jones Newswire.

## Limits

Tables and numbers not checked; timestamp accuracy not tested in the passages read.
