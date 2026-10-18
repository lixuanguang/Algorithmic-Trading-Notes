# Source-version changes

Comparisons between editions of external sources and their effect on objectives. A new edition adds source records and crosswalk mappings; it creates a new objective only when the required capability changes.

## Level III outlines, 2026 against 2027 (compared 18 October 2026)

Sources: the three 2026 Level III outlines (`outline:063c461ba7ab`, `outline:b6d663443715`, `outline:674aec45b29e`, role `historical-comparison`) against the three 2027 ones (`outline:2e1d62d8f585`, `outline:2f25110282bf`, `outline:5bc9c1013387`, the scope references). Method: text extracted from every page with PyPDF2, modules and checkbox items parsed, headings and item text compared after whitespace normalisation. This compares outlines only; it says nothing about whether the underlying readings changed.

| Component | 2026 | 2027 |
| --- | ---: | ---: |
| Shared core (identical in the three files of each year) | 22 modules / 171 items, PDF pp. 1-14 | 28 modules / 183 items, PDF pp. 1-15 |
| Portfolio Management pathway | 8 / 64 | 8 / 64 |
| Private Markets pathway | 7 / 34 | 7 / 34 |
| Private Wealth pathway | 7 / 27 | 7 / 27 |

Differences found:

1. **Ethics guidance split.** The 2026 core has one module, *Guidance for Standards I–VII* (module 20, PDF p. 13, printed p. 1 of the ethics topic, two items). The 2027 core replaces it with seven modules, one per standard (modules 20-26, PDF pp. 13-14), each with the same two items: interpret the code and standards in situations, and recommend preventive practices. That adds six modules and twelve items to each 2027 Level III file. **Effect on objectives:** none created. The 2027 items map to `objective:apply-standard-<standard>` and `objective:prevent-violations-<standard>` for the seven standards, which the Level I and Level II outlines already require; the 2026 module would map to all fourteen. The seven 2027 modules remain separate source obligations in the crosswalk.
2. **Private Debt, item 3.** *Contrast the use of mezzanine debt and unitranche debt* ends in a semicolon in 2026 (`outline:b6d663443715`, module 26, PDF p. 16) and without one in 2027 (`outline:2f25110282bf`, module 32, PDF p. 17). Punctuation only; no effect.

All other headings and items, in all components, are identical after normalisation.
