# Model reference

Detailed mathematical specifications and derivations behind compendium entries. The compendium states each result with its assumptions, applications, pitfalls and an idea of the proof; this reference gives the full working. Executable implementations and their numerical checks stay in `src/trading_notes/`.

| Location | Purpose |
| --- | --- |
| `model-reference.tex` | The single entrypoint; it inputs the compendium's `preamble.tex` and `house.tex` rather than a copy of them |
| `model-reference.pdf` | The compiled reference, committed like `compendium/compendium.pdf` |
| `front/notation.tex` | Model-local symbols, units and conventions |
| `front/model-index.tex` | Model, compendium entry, derivation, implementation and numerical check |
| `<section-key>/<topic>/<model>.tex` | One file per model, below the compendium section and topic it serves |

The chapters mirror the compendium: one chapter per compendium section, one section per specialist pathway, one subsection per model. A model gets its own folder only when it needs supporting files or several substantial parts.

## Labels and links

Compendium labels such as `mod:kyle-single-auction` stay in the compendium. Each derivation has its own stable label with the `drv:` prefix, such as `drv:kyle-single-auction`. Both documents load hyperref with `destlabel`, so every PDF destination is named after its label, and the two PDFs link to each other by label, without page numbers:

- `\qfentrylink{mod:...}` in the model reference opens the entry in `../compendium/compendium.pdf`;
- `\qfderivation{drv:...}` in a compendium entry's proof sketch opens the derivation in `../model-derivations/model-reference.pdf`.

The links are relative, so they work while both PDFs sit in their folders of one checkout. Citations use the compendium's `\citep`, which links catalogue keys into the guide's reading list; a source outside the catalogue is registered with `\qfsource` in the reference's back matter.

## Add a derivation

1. Write `<section-key>/<topic>/<model>.tex`, starting with `\subsection{...}\label{drv:<name>}`, and input it from `model-reference.tex` under its chapter and pathway section.
2. State the purpose, assumptions (variables, units, timing, information sets and constraints), the derivation with its intermediate steps, the results with interpretation and limiting cases, and the limitations; cite with locators.
3. Add a row to `front/model-index.tex`, and link the compendium entry's proof sketch with `\qfderivation{drv:<name>}`.
4. Build both documents and check that the links resolve.

## Build

From the repository root:

```sh
make model-reference   # latexmk -lualatex in model-derivations/
make pdf               # the compendium, built independently
```

Or, from this folder, `latexmk -lualatex model-reference.tex`. LuaLaTeX is needed: the shared preamble runs `../compendium/typography.lua` through `\qfcompendiumdir`. Auxiliary files are ignored by Git; only `model-reference.pdf` is kept.
