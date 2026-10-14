# Coverage log

One row per pathway or section overview, keyed as in the learning guide (`guide/`). A pathway is *mastered* when its checkpoint is passed from your own notes, and *consolidated* when its entry backlog is empty and its entries are checked. Dates are ISO 8601.

| Pathway key | Mastered | Consolidated | Checkpoint artefact | Entries |
| --- | --- | --- | --- | --- |
| `market-making-lob` | | | | Draft entries from the migration pilot, 2026-10-14, not from study: `mod:grossman-miller`, `res:grossman-miller-trading-fees`, `res:grossman-miller-liquidity-measures`, `mod:static-limit-order-depth`, `mod:avellaneda-stoikov`, `mod:kyle-single-auction` |

## Reading before the study method

Books read before these notes followed the learning guide. Their material is in the legacy chapters listed (`compendium/legacy/<section-key>/`), not yet split into reading notes or retyped as entries, except for the entries migrated so far (`notes/migration.md`).

| Catalogue key | Book | Progress | Compendium chapter |
| --- | --- | --- | --- |
| `s7-gliner` | Greg Gliner, *Global Macro Trading* | Completed | `multi-asset-systematic-macro` |
| `s7-narang` | Rishi K. Narang, *Inside the Black Box* | Completed | `portfolio-construction-risk` |
| `alpha-laruelle` | Charles-Albert Lehalle and Sophie Laruelle, *Market Microstructure in Practice* | Completed | `execution-market-making`, `execution-trading-costs` |
| `alpha-harris` | Larry Harris, *Trading and Exchanges* | Completed | `execution-market-making`, `execution-trading-costs` |
| `crypto-cartea` | Álvaro Cartea, Sebastian Jaimungal and José Penalva, *Algorithmic and High-Frequency Trading* | Chapter 1 in progress | `execution-market-making`, `execution-trading-costs` |
| `alpha-johnson` | Barry Johnson, *Algorithmic Trading and DMA* | Through chapter 8 | `execution-market-making`, `execution-trading-costs` |
| `s3-velu` | Raja Velu, Maxence Hardy and Daniel Nehren, *Algorithmic Trading and Quantitative Strategies* | Preface and prerequisites | preface |
| not catalogued | Jeffrey Bacidore, *Algorithmic Trading: A Practitioner's Guide* | Chapter 1 in progress | `execution-market-making`, `execution-trading-costs` |
| `wide-webster-price-impact` | Kevin T. Webster, *Handbook of Price Impact Modeling* | Chapter 1 in progress | `execution-market-making`, `execution-trading-costs` |
| `s7-gueant` | Olivier Guéant, *The Financial Mathematics of Market Liquidity* | Chapter 1 in progress | `execution-market-making`, `execution-trading-costs` |

## Open questions

- 2026-10-14, `market-making-lob`: `crypto-cartea` p. 33 prints Kyle's $\lambda=2\sigma_u/\sigma$, the reciprocal of `catalogue-0496` eq. (4.5). Check against Kyle (1985) and the book's errata.
- 2026-10-14, `market-making-lob`: the route's Ho–Stoll reading, `catalogue-0527`, names no paper. Obtain Ho and Stoll (1981) and decide whether it, or their 1980 paper on competing dealers, is the one to read.
