"""Focused tests for check_compendium.py on small synthetic repositories.

Run:  python3 -m unittest discover -s tools
"""
import json
import tempfile
import unittest
from pathlib import Path

import check_compendium as ms

ROUTES = {'routes': [{'id': 'sec-a'}, {'id': 'sec-b'}],
          'specialist_routes': [{'id': 'path-x'}, {'id': 'path-y'}, {'id': 'path-z'}]}

GOOD_ENTRY = r"""\begin{qfmodel}[A model]\label{mod:good}
\qffield{Statement} Claim \citep[p.~3]{cat-key}.
\qffield{Further reading} \citep{src-key}.
\end{qfmodel}
"""


class Repo:
    """A throwaway repository laid out like this one."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write('guide/learning_routes.json', json.dumps(ROUTES))
        self.write('guide/institutional_quantitative_finance_reading_list.tex',
                   r'\CatalogueEntry{cat-key}{A book}' + '\n')
        self.write('compendium/front/sources.tex', r'\qfsource{src-key}{A paper}' + '\n')
        self.write('notes/pathways/.keep', '')

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def report(self):
        return ms.report(self.root)

    def close(self):
        self.tmp.cleanup()


class EntryMetadata(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.repo.write('notes/pathways/path-x.md', '## Entries created or changed\n- `mod:good`\n'
                        '## Entry backlog\n- res:later: a stub \\citep[p.~1]{cat-key}\n')

    def gaps(self, entry):
        self.repo.write('compendium/sec-a/topic.tex', entry)
        return self.repo.report()['problems']

    def test_complete_entry_passes(self):
        r = (self.gaps(GOOD_ENTRY), self.repo.report())
        self.assertEqual(r[0], [])
        self.assertEqual(r[1]['pathways']['path-x']['entries_listed'], ['mod:good'])
        self.assertEqual(r[1]['pathways']['path-x']['backlog_stubs'], 1)

    def test_missing_label_and_wrong_prefix(self):
        self.assertTrue(any('missing label' in p for p in self.gaps(
            GOOD_ENTRY.replace(r'\label{mod:good}', ''))))
        self.assertTrue(any('label prefix (expected mod:)' in p for p in self.gaps(
            GOOD_ENTRY.replace('mod:good', 'res:good'))))

    def test_citation_and_locator(self):
        self.assertTrue(any('missing locator for cat-key' in p for p in self.gaps(
            GOOD_ENTRY.replace(r'\citep[p.~3]{cat-key}', r'\citep{cat-key}'))))
        self.assertTrue(any('missing citation' in p for p in self.gaps(
            GOOD_ENTRY.replace(r'\citep[p.~3]{cat-key}', ''))))
        self.assertTrue(any('unknown citation key nobody' in p for p in self.gaps(
            GOOD_ENTRY.replace('{cat-key}', '{nobody}'))))

    def test_bare_citation_allowed_in_further_reading_only(self):
        self.assertFalse(any('locator for src-key' in p for p in self.gaps(GOOD_ENTRY)))

    def test_editorial_metadata_is_optional(self):
        self.assertEqual(self.gaps(GOOD_ENTRY), [])

    def test_unlisted_entry_and_dangling_listing(self):
        self.repo.write('notes/pathways/path-x.md', '## Entries\n- `res:nowhere`\n')
        problems = '\n'.join(self.gaps(GOOD_ENTRY))
        self.assertIn('entry `mod:good` is listed in no pathway note', problems)
        self.assertIn('lists `res:nowhere`, which no compendium label defines', problems)

    def test_duplicate_labels(self):
        self.repo.write('compendium/sec-b/other.tex', GOOD_ENTRY)
        self.assertTrue(any('label `mod:good` defined 2 times' in p for p in self.gaps(GOOD_ENTRY)))

    def test_folder_must_be_a_section_key(self):
        self.repo.write('compendium/not-a-section/x.tex', GOOD_ENTRY)
        self.assertTrue(any('`not-a-section` is not a guide section key' in p
                            for p in self.repo.report()['problems']))


if __name__ == '__main__':
    unittest.main()
