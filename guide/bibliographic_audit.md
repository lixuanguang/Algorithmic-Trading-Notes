# Bibliographic verification

How the catalogue's citations are checked, what the version records establish, and what they don't. Each entry's own record (in [catalogue_extended_notes.html](catalogue_extended_notes.html) and [catalogue_recency.json](catalogue_recency.json)) holds the evidence for that entry; this file sets out the standard and the overall position. Open identification questions are in [editorial_backlog.md](editorial_backlog.md); deliberate exclusions are in [removal_plan.md](removal_plan.md).

## Current status

| | Entries |
| --- | ---: |
| Catalogue entries | 3,956 |
| Checked against a source in October 2026 (`new-source-inspection`) | 3,057 |
| Carrying evidence from an earlier check (`inherited-evidence`) | 573 |
| No entry-level check yet (`not-established`) | 326 |
| Linked by DOI | 2,712 |
| Full text not inspected | 2,730 |

The 326 unchecked entries were carried over from the original catalogue with their citations and annotations unchanged. Their records say so and link here; they are the first candidates for verification.

## Standard for new and re-verified entries

- **Identity.** Resolve every DOI against Crossref, or DataCite for arXiv and LIPIcs, and match title and authors before use; first-guess DOIs are often wrong. Items without a DOI cite a primary page (publisher, regulator, exchange, author) that was read.
- **Corrections.** Check Crossref's `updated-by` field for retractions, errata and corrections, and record what it shows.
- **Annotations.** Base each annotation on a retrieved abstract or primary page, in this order: Crossref, OpenAlex, Semantic Scholar, DataCite, RePEc/IDEAS. If none has it, use an author's or repository copy and say which. A secondary index is used only when nothing else exists, and it is labelled.
- **Versions.** Keep publication, online and issue dates, revisions and working-paper postings distinct. Don't infer dates, editions or chapter numbers; state unknowns.
- **Scope.** Each record states what was inspected (metadata, abstract, selected pages or full text). Metadata access does not establish full-text equivalence, legal currency or empirical reproducibility.

The 62 entries added on 22 October 2026 for the study-guide migration (financial mathematics, unit-root and cointegration classics, asset-pricing classics, professional ethics, financial reporting, corporate finance and private wealth) follow this standard; each version record says what was read. Where no abstract was retrievable from Crossref, OpenAlex, Semantic Scholar or RePEc, the annotation says it rests on the title and standard result. EUR-Lex refused automated access, so the two EU regulations were identified from the Publications Office's Cellar metadata; the Modigliani–Miller (1958) metadata come from OpenAlex, a secondary index, because the article has no DOI and its JSTOR record did not load. A correction pass the same day removed one of the 62 (`pw-campbell-viceira-2002`, a duplicate of `s16-r09`, whose record now carries the new Crossref check), added the MSCI index-construction and index-calculation methodologies (selected sections read), and corrected the EU records: each links the original act, and the amending acts and latest consolidated version are identified from Publications Office metadata only. The DOI and full-text counts above are entries whose citation links a doi.org address and version records that say full text was not inspected.

## Findings on record

- **Retractions.** The Bai–Bali–Wen corporate-bond factor article (*JFE*) was retracted in December 2023; the entries that use its corrected factors record the notice. Two Corbet–Lucey crypto papers with 2025–26 retraction notices were excluded.
- **Errata.** Three entries record errata (rough Bergomi, Hasso et al. 2019, Hubáček et al. 2019).
- **Withdrawals and supersessions.** Recorded where they matter: the CFTC's 2024 voluntary-carbon-credit guidance (withdrawn September 2025), SR 11-7 (superseded by SR 26-2 in April 2026), the 2014 ISDA Credit Derivatives Definitions, the December 2024 FX Global Code, and journal versions that supersede working papers.
- **Corrected citations.** Earlier audits replaced DOIs that pointed to unrelated papers, repaired invalid DOIs and fixed author names. The corrected citations are in the catalogue; their earlier forms are not kept.
- **Weak sources.** Three annotations rest on Web of Science abstracts reproduced by a secondary index, and about 40 entries could not be machine-verified because their publishers refuse automated access. Their records say so.

## Known pitfalls

- Crossref's first hit for an older paper is often its SSRN or NBER copy; search for the journal record separately.
- Crossref sometimes holds only a first page (JSTOR), only the first author, initials only, or misspelt names.
- OpenAlex can return another paper's abstract, a citation string or a chapter's opening paragraph. Read the abstract against the title before using it.
- Some repositories misattribute too, for example RePEc misspelling an author's name.

## Not established

There has been no catalogue-wide retraction or correction sweep beyond the entries checked since October 2026. Nor has there been any full-text review, empirical replication, code or dataset execution, test of subscription access, or legal-currency review of rules. About 1,870 inherited version records cite evidence files under `archive/`, which has been removed, so those citations no longer resolve. A failed search is not evidence that a resource or a later version doesn't exist.
