#!/usr/bin/env python3
"""Report the compendium migration: legacy blocks left, entries written, and metadata gaps.

Run from anywhere:  python3 tools/migration_status.py [--check] [--json] [--root DIR]

What it reads (conventions in notes/migration.md):
  compendium/legacy/<section-key>/**.tex
      `% migrate-to: key, key` near the top of a file names the pathways its blocks are
      candidate material for. `% assign: key` on the line before a block assigns that block
      to one pathway. Blocks are the old environments declared in compendium/preamble.tex.
  compendium/<section-key>/**.tex
      entries: \\begin{qf<type>}[Title]\\label{<prefix>:<name>} ... \\end{qf<type>}.
  notes/pathways/<pathway-key>.md
      entry labels listed under a heading starting `Entries`, and `- <label>: ...` stubs
      under `Entry backlog`.
  notes/migration.md
      the file map between `<!-- map:begin -->` and `<!-- map:end -->`, one row per legacy file:
      | `compendium/legacy/...tex` | key, key |
  guide/learning_routes.json, the pinned catalogue and compendium/front/sources.tex
      the valid pathway keys and citation keys.

Limits. This is a pattern matcher, not a LaTeX parser: it sees comments, environment names,
labels, \\citep commands and field names. A citation it finds says nothing about whether the
source supports the claim, whether the locator is right, or whether the sentence it sits in is
the claim it should support. Nothing here measures learning: mastery and consolidation dates
live in notes/log.md and are set by the person studying, never by this script.

Exit status: 0, or 1 with --check when any problem is reported.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LEGACY_ENVS = (
    'theorem corollary lemma proposition qnbank process method definition example remark notation '
    'principle mechanism taxonomy model assumption casestudy empiricalfinding practitionernote '
    'caveat marketrule takeaway').split()
PREFIX = {'definition': 'def', 'convention': 'conv', 'result': 'res', 'model': 'mod',
          'method': 'meth', 'mechanism': 'mech', 'evidence': 'ev', 'data': 'data',
          'rule': 'rule', 'pitfall': 'pit', 'example': 'ex'}
LABEL_RE = r'(?:%s):[a-z0-9-]+' % '|'.join(sorted(set(PREFIX.values())))

BEGIN_LEGACY = re.compile(r'\\begin\{(%s)\}' % '|'.join(LEGACY_ENVS))
MIGRATE_TO = re.compile(r'^%\s*migrate-to:\s*(.*)$')
ASSIGN = re.compile(r'^%\s*assign:\s*([a-z0-9-]+)\s*$')
ENTRY = re.compile(r'\\begin\{qf(%s)\}(?:\[(.*?)\])?(.*?)\\end\{qf\1\}' % '|'.join(PREFIX), re.S)
LABEL = re.compile(r'\\label\{([^}]+)\}')
CITEP = re.compile(r'\\citep(\[[^\]]*\])?(\[[^\]]*\])?\{([^}]+)\}')
FIELD = re.compile(r'\\qffield\{([^}]+)\}')
MAP_ROW = re.compile(r'^\|\s*`?(compendium/legacy/[^`|]+?)`?\s*\|\s*([^|]*?)\s*\|')


def strip_comment(line):
    """Drop a LaTeX comment, keeping escaped percent signs."""
    return re.sub(r'(?<!\\)%.*', '', line)


def keys_from(text):
    return [k.strip() for k in text.split(',') if k.strip()]


def load_routes(root):
    data = json.loads((root / 'guide' / 'learning_routes.json').read_text())
    sections = {r['id'] for r in data['routes']}
    return sections, sections | {r['id'] for r in data['specialist_routes']}


def load_citation_keys(root):
    keys = set(re.findall(r'\\CatalogueEntry\{([^}]+)\}', (
        root / 'guide' / 'institutional_quantitative_finance_reading_list.tex').read_text()))
    sources = root / 'compendium' / 'front' / 'sources.tex'
    if sources.exists():
        keys |= set(re.findall(r'\\qfsource\{([^}]+)\}', sources.read_text()))
    return keys


def scan_legacy(root, pathways, problems):
    """Blocks per legacy file, with each file's candidate pathways and each block's assignment."""
    files = []
    for path in sorted((root / 'compendium' / 'legacy').rglob('*.tex')):
        rel = path.relative_to(root).as_posix()
        lines = path.read_text().splitlines()
        candidates, blocks, previous = None, [], ''
        for n, line in enumerate(lines, 1):
            m = MIGRATE_TO.match(line.strip())
            if m and candidates is None:
                candidates = keys_from(m.group(1))
            code = strip_comment(line)
            for b in BEGIN_LEGACY.finditer(code):
                a = ASSIGN.match(previous.strip())
                blocks.append({'env': b.group(1), 'line': n, 'assign': a.group(1) if a else None})
            if line.strip():
                previous = line
        if blocks and candidates is None:
            problems.append(f'{rel}: {len(blocks)} blocks but no `% migrate-to:` line')
        for k in candidates or []:
            if k not in pathways:
                problems.append(f'{rel}: migrate-to key `{k}` is not in guide/learning_routes.json')
        for b in blocks:
            if b['assign'] and b['assign'] not in pathways:
                problems.append(f"{rel}:{b['line']}: assign key `{b['assign']}` is not a pathway key")
            elif b['assign'] and candidates is not None and b['assign'] not in candidates:
                problems.append(f"{rel}:{b['line']}: assigned to `{b['assign']}`, not among the file's migrate-to keys")
        files.append({'file': rel, 'section': rel.split('/')[2], 'candidates': candidates or [],
                      'blocks': blocks})
    return files


def pathway_counts(files):
    """Each legacy block counted once: assigned to one pathway, exclusive to one, or shared."""
    assigned, exclusive, shared = Counter(), Counter(), Counter()
    unassigned_shared = 0
    for f in files:
        for b in f['blocks']:
            if b['assign']:
                assigned[b['assign']] += 1
            elif len(f['candidates']) == 1:
                exclusive[f['candidates'][0]] += 1
            elif f['candidates']:
                unassigned_shared += 1
                for k in f['candidates']:
                    shared[k] += 1
    return assigned, exclusive, shared, unassigned_shared


def scan_entries(root, sections, cite_keys, problems):
    entries = []
    compendium = root / 'compendium'
    for path in sorted(compendium.rglob('*.tex')):
        parts = path.relative_to(compendium).parts
        if len(parts) < 2 or parts[0] in ('legacy', 'front'):
            continue
        rel = path.relative_to(root).as_posix()
        if parts[0] not in sections:
            problems.append(f'{rel}: folder `{parts[0]}` is not a guide section key')
        text = '\n'.join(strip_comment(l) for l in path.read_text().splitlines())
        for m in ENTRY.finditer(text):
            etype, title, body = m.group(1), m.group(2), m.group(3)
            line = text.count('\n', 0, m.start()) + 1
            labels = LABEL.findall(body)
            head = body.split('\\qffield', 1)[0]
            label = next((l for l in LABEL.findall(head) if not l.startswith(('fig:', 'eq:'))), None)
            gaps = []
            if not title:
                gaps.append('title')
            if not label:
                gaps.append('label')
            elif not label.startswith(PREFIX[etype] + ':'):
                gaps.append(f'label prefix (expected {PREFIX[etype]}:)')
            fields = FIELD.findall(body)
            if 'Statement' not in fields:
                gaps.append('Statement field')
            claims = body.split('\\qffield{Further reading}')[0] if 'Further reading' in fields else body
            cites = CITEP.findall(body)
            if not CITEP.search(claims):
                gaps.append('citation')
            for opt1, opt2, key in CITEP.findall(claims):
                if not opt1:
                    gaps.append(f'locator for {key}')
            for _, _, key in cites:
                if key not in cite_keys:
                    gaps.append(f'unknown citation key {key}')
            status = body.split('\\qffield{Status}', 1)[1] if 'Status' in fields else ''
            for axis in ('Verification', 'Stability', 'Currency'):
                if axis + ':' not in status:
                    gaps.append(f'status {axis.lower()}')
            entries.append({'file': rel, 'line': line, 'section': parts[0], 'type': etype,
                            'label': label, 'labels': labels, 'gaps': sorted(set(gaps))})
            for g in sorted(set(gaps)):
                problems.append(f'{rel}:{line}: entry {label or title!r} missing {g}')
    return entries


def duplicate_labels(root, problems):
    seen = defaultdict(list)
    for path in sorted((root / 'compendium').rglob('*.tex')):
        if path.name == 'house.tex':
            continue
        for n, line in enumerate(path.read_text().splitlines(), 1):
            for l in LABEL.findall(strip_comment(line)):
                seen[l].append(f'{path.relative_to(root).as_posix()}:{n}')
    for label, where in seen.items():
        if len(where) > 1:
            problems.append(f'label `{label}` defined {len(where)} times: {", ".join(where)}')
    return set(seen)


def pathway_notes(root, pathways, problems):
    """Entry labels a pathway note lists under its `Entries` heading, and its backlog stubs."""
    listed, stubs = {}, {}
    for path in sorted((root / 'notes' / 'pathways').glob('*.md')):
        key = path.stem
        if key not in pathways:
            problems.append(f'notes/pathways/{path.name}: `{key}` is not a pathway key')
        heading, labels, n_stubs = '', set(), 0
        for line in path.read_text().splitlines():
            if line.startswith('#'):
                heading = line.lstrip('#').strip().lower()
            elif heading.startswith('entries'):
                labels |= set(re.findall(LABEL_RE, line))
            elif heading == 'entry backlog' and re.match(r'-\s*%s:' % LABEL_RE, line.strip()):
                n_stubs += 1
        listed[key], stubs[key] = labels, n_stubs
    return listed, stubs


def check_map(root, files, problems):
    """The file map in notes/migration.md must match the migrate-to comments exactly."""
    path = root / 'notes' / 'migration.md'
    if not path.exists():
        problems.append('notes/migration.md is missing')
        return
    text = path.read_text()
    if '<!-- map:begin -->' not in text:
        problems.append('notes/migration.md has no <!-- map:begin --> table')
        return
    table = text.split('<!-- map:begin -->', 1)[1].split('<!-- map:end -->', 1)[0]
    in_doc = {}
    for line in table.splitlines():
        m = MAP_ROW.match(line.strip())
        if m:
            in_doc[m.group(1).strip()] = keys_from(m.group(2).replace('`', ''))
    in_files = {f['file']: f['candidates'] for f in files if f['blocks'] or f['candidates']}
    for rel in sorted(in_files.keys() - in_doc.keys()):
        problems.append(f'map: {rel} has blocks or a migrate-to line but no row in notes/migration.md')
    for rel in sorted(in_doc.keys() - in_files.keys()):
        problems.append(f'map: notes/migration.md lists {rel}, which has no blocks or no longer exists')
    for rel in sorted(in_doc.keys() & in_files.keys()):
        if sorted(in_doc[rel]) != sorted(in_files[rel]):
            problems.append(f'map: {rel}: migration.md says {in_doc[rel]}, the file says {in_files[rel]}')


def check_legacy_part(root, sections, problems):
    legacy = root / 'compendium' / 'legacy'
    part = (legacy / 'part.tex').read_text() if (legacy / 'part.tex').exists() else ''
    for d in sorted(p for p in legacy.iterdir() if p.is_dir()):
        if d.name not in sections:
            problems.append(f'compendium/legacy/{d.name}: not a guide section key')
        if f'legacy/{d.name}/section' not in part:
            problems.append(f'compendium/legacy/{d.name}: not input by compendium/legacy/part.tex')


def report(root):
    problems = []
    sections, pathways = load_routes(root)
    files = scan_legacy(root, pathways, problems)
    entries = scan_entries(root, sections, load_citation_keys(root), problems)
    all_labels = duplicate_labels(root, problems)
    listed, stubs = pathway_notes(root, pathways, problems)
    check_map(root, files, problems)
    check_legacy_part(root, sections, problems)
    entry_labels = {e['label'] for e in entries if e['label']}
    for key, labels in listed.items():
        for l in sorted(labels - all_labels):
            problems.append(f'notes/pathways/{key}.md lists `{l}`, which no compendium label defines')
    in_notes = set().union(*listed.values()) if listed else set()
    for l in sorted(entry_labels - in_notes):
        problems.append(f'entry `{l}` is listed in no pathway note')
    assigned, exclusive, shared, unassigned_shared = pathway_counts(files)
    return {
        'legacy_blocks': sum(len(f['blocks']) for f in files),
        'legacy_by_section': dict(Counter(f['section'] for f in files for _ in f['blocks'])),
        'legacy_by_env': dict(Counter(b['env'] for f in files for b in f['blocks'])),
        'legacy_assigned': sum(assigned.values()),
        'legacy_exclusive_candidates': sum(exclusive.values()),
        'legacy_shared_unassigned': unassigned_shared,
        'pathways': {k: {'assigned': assigned[k], 'exclusive_candidates': exclusive[k],
                         'shared_candidates': shared[k], 'backlog_stubs': stubs.get(k, 0),
                         'entries_listed': sorted(listed.get(k, set()) & entry_labels)}
                     for k in sorted(set(assigned) | set(exclusive) | set(shared) | set(listed))},
        'entries': len(entries),
        'entries_by_section': dict(Counter(e['section'] for e in entries)),
        'entries_by_type': dict(Counter(e['type'] for e in entries)),
        'entries_with_gaps': [e['label'] or e['file'] for e in entries if e['gaps']],
        'problems': problems,
    }


def print_report(r):
    print(f"Legacy blocks left: {r['legacy_blocks']}")
    for s, n in sorted(r['legacy_by_section'].items()):
        print(f'  {s:32} {n:4}')
    print(f"  assigned to one pathway: {r['legacy_assigned']}; candidates of one pathway only: "
          f"{r['legacy_exclusive_candidates']}; shared, not yet assigned: {r['legacy_shared_unassigned']}")
    print(f"Entries written: {r['entries']}  "
          + ', '.join(f'{k} {v}' for k, v in sorted(r['entries_by_type'].items())))
    print('\nPer pathway (each legacy block counts once as assigned or exclusive; a shared block is')
    print('listed under every pathway that may claim it and is owned by none until assigned):')
    print(f"  {'pathway':36} {'assigned':>8} {'exclusive':>9} {'shared':>6} {'entries':>7} {'stubs':>5}")
    for k, v in r['pathways'].items():
        print(f"  {k:36} {v['assigned']:8} {v['exclusive_candidates']:9} {v['shared_candidates']:6} "
              f"{len(v['entries_listed']):7} {v['backlog_stubs']:5}")
    print(f"\nProblems: {len(r['problems'])}")
    for p in r['problems']:
        print('  - ' + p)
    print('\nLimits: a citation found is not a claim checked; the locator, the source and the claim it '
          'supports are verified only by reading the passage. Learning progress is not measured here.')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument('--json', action='store_true', help='print the report as JSON')
    ap.add_argument('--check', action='store_true', help='exit 1 when any problem is reported')
    args = ap.parse_args(argv)
    r = report(args.root.resolve())
    if args.json:
        json.dump(r, sys.stdout, indent=1)
        print()
    else:
        print_report(r)
    return 1 if args.check and r['problems'] else 0


if __name__ == '__main__':
    sys.exit(main())
