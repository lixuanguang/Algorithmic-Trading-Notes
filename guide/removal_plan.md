# Scope and exclusions

What the catalogue includes, what it leaves out on purpose, and which resources have been removed, so that they aren't added back by accident. Unidentified leads are tracked in [editorial_backlog.md](editorial_backlog.md); retracted or unverifiable papers are covered in [bibliographic_audit.md](bibliographic_audit.md).

## What belongs in the catalogue

A subject-organised reference of books, papers, courses, datasets, software, technical documentation and research outlets for institutional quantitative research. An entry earns its place by making a distinct contribution: a method, result, dataset, specification or worked example that other entries don't already supply.

- **One entry per resource.** Give the author or organisation, title, version, type and level, link, and a short note on why it matters, plus limitations where useful.
- **Don't cut by category.** Introductory, practitioner, historical and non-English material stays when it adds something. Prestige, language and difficulty are not filters.
- **Mark specialist material optional** rather than removing it. Examples are low-latency systems engineering (Gregg, C++ concurrency), infrastructure tooling (Kafka, Kubernetes, observability), discretionary market context (Drobny, Schwager, Soros, Dalio) and developer exercises (Ethernaut, the Buffalo smart-contracts course).
- **Several books on one topic are not duplicates.** Merge only true repeats of the same resource.

## What stays out

- **Companion documents.** Interview handbooks and brainteasers, software implementation specifications, study schedules and workload estimates, historical timelines, embedded tutorials and operating procedures, and the history of how the catalogue was assembled. Readings referenced inside such material are catalogued as ordinary entries.
- **Broad news and commentary feeds** with no identified research series, dataset or method.
- **Display-only dashboards** that give neither data access, documentation nor a reproducible method. Keep the provider's data or API documentation instead.
- **Promotional explainers and beginner roundups** whose points a retained reference already covers.
- **Generic developer onboarding and event directories** with no research-specific material.
- **Unidentified placeholders.** A resource without an identifiable title, author or link goes to the backlog, not the catalogue.

## Removed resources

| Category | Removed | Retained instead |
| --- | --- | --- |
| Crypto news and commentary | The Defiant; Bankless newsletter and podcast; Willy Woo's *The Bitcoin Forecast*; Messari's *Unqualified Opinions* newsletter | Uncommon Core (MEV interview), Deribit Insights, and the Coin Metrics, Kaiko, Glassnode, Flashbots, Paradigm, a16z crypto, Gauntlet and Delphi research outlets |
| Developer onboarding | CryptoZombies; the ETHGlobal event directory; Web3 Foundation events (moved to the backlog) | Ethernaut, Damn Vulnerable DeFi, audit-firm methods, and university blockchain courses |
| Dashboards | TradingView and Coin360 | Dune and Nansen API documentation; DeFiSafety's review method; Gauntlet research |
| Beginner roundups | BigBrainMoney trading lifecycle; QuantStart *Beginner's Guide to Quantitative Trading*; Neudata beginner alternative-data guide; two Amberdata overviews (crypto microstructure ML, institutional crypto risk); LuxAlgo time-series overview; Databricks feature-store glossary; CFI and Investopedia bias explainers | Narang, Davey and Fitschen; QuantStart technical examples; Denev–Amen, Guida and the AIMA survey; Amberdata data documentation; Feast documentation |

Each exclusion is a judgement about marginal value to this catalogue. It is not a claim that the provider has no useful material, and a specific research piece from any of these sources can be added on its own merits.
