#!/usr/bin/env python3
"""E19: 'NEW in this lesson:' callouts on the 49 instruction-table blocks.

Cumulative-set scan in reading order (volume1 then volume2), single shared
seen-set. Row-label normalization: 'X on Y' -> Y (flag notes); 'icmp slt' /
'icmp eq' -> icmp. New list sorted alphabetically, backticked.

Root: insert the callout line directly after each
'### Every instruction used in this pair' heading.
JSON: insert a paragraph block after the matching heading block, then
recompute words for every affected lesson (recursive formula).

Plan by default; --apply to modify.
"""
import json
import re
import sys

V = '/home/ruby.tian/minishield'
HEAD = '### Every instruction used in this pair'


def base_of(label):
    # 'nsw` on `mul`' -> mul ; 'icmp slt' -> icmp
    m = re.match(r'^(?:[a-z_]+) on ([a-z_]+)$', label)
    if m:
        return m.group(1)
    m = re.match(r'^icmp (?:slt|sgt|eq|ne|ult|ugt)$', label)
    if m:
        return 'icmp'
    return label


def root_tables(path):
    lines = open(path).read().splitlines()
    idx = [i for i, l in enumerate(lines) if l == HEAD]
    tables = []
    for i in idx:
        rows = []
        for j in range(i + 3, min(i + 45, len(lines))):
            if lines[j].startswith('### '):
                break
            # first cell: `X`: ... or `X` ... or `FLAG` on `BASE`
            m = re.match(r'^\| `(.*?)`(?: on `(.*?)`)?', lines[j])
            if m:
                rows.append(m.group(2) if m.group(2) else m.group(1))
        tables.append((i, rows))
    return lines, tables


def plan(roots):
    seen = set()
    out = []
    for vol, (lines, tables) in roots:
        for i, rows in tables:
            bases = [base_of(r) for r in rows]
            new = sorted({b for b in bases if b not in seen})
            seen.update(rows)
            seen.update(bases)
            out.append((vol, i, rows, new))
    return out


def callout(new):
    if new:
        items = ', '.join(f'`{n}`' for n in new)
        return f'NEW in this lesson: {items}.'
    return ('No new instructions in this pair — every line repeats an earlier '
            'lesson (see the "Recurring blocks" note at the start of this volume).')


def apply_root(vol, lines, plan_rows):
    # original: [heading, '', table...] -> [heading, '', callout, '', table...]
    # insert from bottom up so indices stay valid
    for i, new in reversed(plan_rows):
        assert lines[i] == HEAD and lines[i + 1].strip() == '', (vol, i, lines[i:i + 2])
        lines.insert(i + 2, '')
        lines.insert(i + 2, callout(new))


def apply_json(vol, plan_rows):
    path = f'{V}/docs/assets/volume{vol}.json'
    raw = open(path).read()
    d = json.loads(raw)
    touched = set()
    # count occurrences per lesson in order; match to plan_rows order
    occ = {}  # lesson id -> list of block indices of the heading
    for l in d['lessons']:
        occ[l['id']] = [i for i, b in enumerate(l['blocks'])
                        if b.get('text') == 'Every instruction used in this pair']
    # walk lessons in document order, consuming plan entries in order
    cursor = {vol: 0}
    for l in d['lessons']:
        for bi in occ[l['id']]:
            pvol = vol
            entry = plan_rows[pvol][cursor[pvol]]
            cursor[pvol] += 1
            b = l['blocks'][bi + 1]
            assert b['type'] == 'table', f'expected table after heading in lesson {l["id"]}'
            l['blocks'].insert(bi + 1, {'type': 'paragraph', 'text': callout(entry[2])})
            touched.add(l['id'])
    # recompute words
    def count_block(b):
        n = 0
        if 'text' in b:
            n += len(b['text'].split())
        if 'items' in b:
            for it in b['items']:
                n += len(it.split())
        if 'rows' in b:
            for r in b['rows']:
                if isinstance(r, str):
                    n += len(r.split())
                elif isinstance(r, list):
                    for c in r:
                        n += len(str(c).split())
                elif isinstance(r, dict):
                    for c in r.values():
                        n += len(str(c).split())
        if 'answers' in b:
            for a in b['answers']:
                if isinstance(a, str):
                    n += len(a.split())
                else:
                    n += count_block(a)
        if 'blocks' in b:
            for c in b['blocks']:
                n += count_block(c)
        if 'title' in b:
            n += len(b['title'].split())
        return n

    for l in d['lessons']:
        if l['id'] in touched:
            old = l['words']
            l['words'] = sum(count_block(b) for b in l['blocks'])
            print(f'  v{vol} lesson {l["id"]} ({l["title"][:35]}): words {old} -> {l["words"]}')
    open(path, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def main():
    do_apply = '--apply' in sys.argv
    r1, t1 = root_tables(f'{V}/volume1')
    r2, t2 = root_tables(f'{V}/volume2')
    pl = plan([(1, (r1, t1)), (2, (r2, t2))])

    print(f'tables found: {len(pl)} (v1: {sum(1 for p in pl if p[0]==1)}, v2: {sum(1 for p in pl if p[0]==2)})')
    for vol, i, rows, new in pl:
        tag = 'NEW: ' + ', '.join(new) if new else 'none'
        print(f'  v{vol} L{i+1}: {tag}')
    nnew = sum(1 for p in pl if p[3])
    print(f'NEW blocks: {nnew}')

    if not do_apply:
        print('\nplan only; re-run with --apply')
        return

    # group plan rows per volume in order
    rows1 = [(i, new) for vol, i, rows, new in pl if vol == 1]
    rows2 = [(i, new) for vol, i, rows, new in pl if vol == 2]
    apply_root(1, r1, rows1)
    open(f'{V}/volume1', 'w').write('\n'.join(r1))
    print(f'volume1 root: {len(rows1)} callouts inserted')
    apply_root(2, r2, rows2)
    open(f'{V}/volume2', 'w').write('\n'.join(r2))
    print(f'volume2 root: {len(rows2)} callouts inserted')

    # JSON uses the same plan (callout texts identical to root).
    plan_rows = {1: [(i, rows, new) for vol, i, rows, new in pl if vol == 1],
                 2: [(i, rows, new) for vol, i, rows, new in pl if vol == 2]}
    apply_json(1, plan_rows)
    apply_json(2, plan_rows)
    print('done')


if __name__ == '__main__':
    main()
