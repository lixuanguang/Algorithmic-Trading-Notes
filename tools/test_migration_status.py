"""Focused tests for migration_status.py on small synthetic repositories.

Run:  python3 -m unittest discover -s tools
"""
import json
import tempfile
import unittest
from pathlib import Path

import migration_status as ms

ROUTES = {'routes': [{'id': 'sec-a'}, {'id': 'sec-b'}],
          'specialist_routes': [{'id': 'path-x'}, {'id': 'path-y'}, {'id': 'path-z'}]}

GOOD_ENTRY = r"""\begin{qfmodel}[A model]\label{mod:good}
\qffield{Statement} Claim \citep[p.~3]{cat-key}.
\qffield{Further reading} \citep{src-key}.
\qffield{Status} Verification: unchecked. Stability: draft. Currency: timeless.
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
        self.write('compendium/legacy/part.tex', r'\InputIfFileExists{legacy/sec-a/section}{}{}')
        self.write('notes/pathways/.keep', '')

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def map(self, rows):
        body = '\n'.join(f'| `{f}` | {k} |' for f, k in rows)
        self.write('notes/migration.md',
                   f'<!-- map:begin -->\n| Legacy file | Candidates |\n|---|---|\n{body}\n<!-- map:end -->\n')

    def report(self):
        return ms.report(self.root)

    def close(self):
        self.tmp.cleanup()


class SharedMapping(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.repo.write('compendium/legacy/sec-a/shared.tex',
                        '% migrate-to: path-x, path-y\n'
                        '\\begin{definition} one \\end{definition}\n'
                        '% assign: path-x\n'
                        '\\begin{caveat} two \\end{caveat}\n'
                        '\\begin{remark} three \\end{remark}\n')
        self.repo.write('compendium/legacy/sec-a/own.tex',
                        '% migrate-to: path-z\n\\begin{taxonomy} four \\end{taxonomy}\n')
        self.repo.map([('compendium/legacy/sec-a/shared.tex', 'path-x, path-y'),
                       ('compendium/legacy/sec-a/own.tex', 'path-z')])

    def test_each_block_counted_once(self):
        r = self.repo.report()
        self.assertEqual(r['legacy_blocks'], 4)
        self.assertEqual(r['legacy_assigned'] + r['legacy_exclusive_candidates']
                         + r['legacy_shared_unassigned'], 4)
        self.assertEqual(r['problems'], [])

    def test_shared_file_not_owned_by_every_pathway(self):
        p = self.repo.report()['pathways']
        self.assertEqual((p['path-x']['assigned'], p['path-x']['exclusive_candidates'],
                          p['path-x']['shared_candidates']), (1, 0, 2))
        self.assertEqual((p['path-y']['assigned'], p['path-y']['shared_candidates']), (0, 2))
        self.assertEqual(p['path-z']['exclusive_candidates'], 1)

    def test_map_disagreement_reported(self):
        self.repo.map([('compendium/legacy/sec-a/shared.tex', 'path-x'),
                       ('compendium/legacy/sec-a/gone.tex', 'path-z')])
        problems = '\n'.join(self.repo.report()['problems'])
        self.assertIn("migration.md says ['path-x']", problems)
        self.assertIn('own.tex has blocks or a migrate-to line but no row', problems)
        self.assertIn('lists compendium/legacy/sec-a/gone.tex', problems)

    def test_invalid_keys_and_assignments(self):
        self.repo.write('compendium/legacy/sec-a/own.tex',
                        '% migrate-to: path-q\n% assign: path-x\n\\begin{taxonomy} four \\end{taxonomy}\n')
        self.repo.map([('compendium/legacy/sec-a/shared.tex', 'path-x, path-y'),
                       ('compendium/legacy/sec-a/own.tex', 'path-q')])
        problems = '\n'.join(self.repo.report()['problems'])
        self.assertIn('`path-q` is not in guide/learning_routes.json', problems)
        self.assertIn("assigned to `path-x`, not among the file's migrate-to keys", problems)

    def test_unmapped_file_and_uncompiled_folder(self):
        self.repo.write('compendium/legacy/sec-b/x.tex', '\\begin{remark} r \\end{remark}\n')
        problems = '\n'.join(self.repo.report()['problems'])
        self.assertIn("x.tex: 1 blocks but no `% migrate-to:` line", problems)
        self.assertIn('compendium/legacy/sec-b: not input by compendium/legacy/part.tex', problems)

    def test_commented_blocks_ignored(self):
        self.repo.write('compendium/legacy/sec-a/own.tex',
                        '% migrate-to: path-z\n% \\begin{remark} old \\end{remark}\n'
                        '\\begin{taxonomy} four \\end{taxonomy}\n')
        self.assertEqual(self.repo.report()['legacy_blocks'], 4)


class EntryMetadata(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.repo.map([])
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

    def test_each_status_axis_required(self):
        problems = self.gaps(GOOD_ENTRY.replace(' Currency: timeless.', ''))
        self.assertTrue(any('missing status currency' in p for p in problems))
        problems = self.gaps(GOOD_ENTRY.replace(r'\qffield{Status} Verification: unchecked. '
                                                'Stability: draft. Currency: timeless.', ''))
        self.assertTrue(all(any(f'status {a}' in p for p in problems)
                            for a in ('verification', 'stability', 'currency')))

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
