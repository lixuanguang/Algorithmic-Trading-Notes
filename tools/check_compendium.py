#!/usr/bin/env python3
"""Check compendium entries, citation keys, labels and pathway links.

Run: python3 tools/check_compendium.py [--check] [--json] [--root DIR]

Printed entries require a title, a type-appropriate label, a Statement, and
known citations with locators. Source-review provenance belongs in
notes/entry-evidence.json; it is not a required printed field. Pathway notes
list entry labels under Entries and proposed entries under Entry backlog.

This is a structural check, not a claim or source-verification check.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PREFIX = {'definition': 'def', 'convention': 'conv', 'result': 'res', 'model': 'mod',
          'method': 'meth', 'mechanism': 'mech', 'evidence': 'ev', 'data': 'data',
          'rule': 'rule', 'pitfall': 'pit', 'example': 'ex'}
LABEL_RE = r'(?:%s):[a-z0-9-]+' % '|'.join(sorted(set(PREFIX.values())))

ENTRY = re.compile(r'\\begin\{qf(%s)\}(?:\[(.*?)\])?(.*?)\\end\{qf\1\}' % '|'.join(PREFIX), re.S)
LABEL = re.compile(r'\\label\{([^}]+)\}')
CITEP = re.compile(r'\\citep(\[[^\]]*\])?(\[[^\]]*\])?\{([^}]+)\}')
FIELD = re.compile(r'\\qffield\{([^}]+)\}')


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
        keys |= set(re.findall(r'\\qfsource(?:\[[^]]*\])?\{([^}]+)\}', sources.read_text()))
    return keys


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


def report(root):
    problems = []
    sections, pathways = load_routes(root)
    entries = scan_entries(root, sections, load_citation_keys(root), problems)
    all_labels = duplicate_labels(root, problems)
    listed, stubs = pathway_notes(root, pathways, problems)
    entry_labels = {e['label'] for e in entries if e['label']}
    for key, labels in listed.items():
        for l in sorted(labels - all_labels):
            problems.append(f'notes/pathways/{key}.md lists `{l}`, which no compendium label defines')
    in_notes = set().union(*listed.values()) if listed else set()
    for l in sorted(entry_labels - in_notes):
        problems.append(f'entry `{l}` is listed in no pathway note')
    return {
        'pathways': {k: {'backlog_stubs': stubs.get(k, 0),
                         'entries_listed': sorted(listed.get(k, set()) & entry_labels)}
                     for k in sorted(listed)},
        'entries': len(entries),
        'entries_by_section': dict(Counter(e['section'] for e in entries)),
        'entries_by_type': dict(Counter(e['type'] for e in entries)),
        'entries_with_gaps': [e['label'] or e['file'] for e in entries if e['gaps']],
        'problems': problems,
    }


def print_report(r):
    print(f"Entries: {r['entries']}  "
          + ', '.join(f'{k} {v}' for k, v in sorted(r['entries_by_type'].items())))
    print(f"Pathway notes: {len(r['pathways'])}")
    print(f"Problems: {len(r['problems'])}")
    for problem in r['problems']:
        print('  - ' + problem)
    print('Limits: this checks structure and references, not the truth of claims.')


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
