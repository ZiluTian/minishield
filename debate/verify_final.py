#!/usr/bin/env python3
"""Final verification: E19 JSON state (v1+v2) + v3 executor work."""
import json

V = '/home/ruby.tian/minishield'


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


def check_json(vol):
    path = f'{V}/docs/assets/volume{vol}.json'
    raw = open(path).read()
    d = json.loads(raw)
    rt = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
    print(f'--- volume{vol}.json')
    print(f'  round-trip byte-identical: {rt == raw}')
    bad = []
    for l in d['lessons']:
        calc = sum(count_block(b) for b in l['blocks'])
        if calc != l['words']:
            bad.append((l['id'], l['title'][:40], l['words'], calc))
    print(f'  words formula: {len(d["lessons"]) - len(bad)}/{len(d["lessons"])} exact')
    for b in bad:
        print(f'    stale: id={b[0]} {b[1]!r} stored={b[2]} calc={b[3]}')
    # count E19 callout paragraphs in JSON
    newc = nonec = 0
    for l in d['lessons']:
        for blk in l['blocks']:
            t = blk.get('text', '')
            if t.startswith('NEW in this lesson'):
                newc += 1
            elif t.startswith('No new instructions in this pair'):
                nonec += 1
    print(f'  E19 callout blocks: {newc} NEW + {nonec} none = {newc + nonec}')
    return d


for vol in (1, 2):
    check_json(vol)

# ---- v3 spot checks (root) ----
print('--- volume3 root spot checks')
v3 = open(f'{V}/volume3').read()
checks = [
    ('E1 table cell', 'type-based guard'),
    ('E1 backward CFI glossary', 'backward CFI'),
    ('E8 cov semantics', 'does not pass quietly'),
    ('E10 DCE mechanism', 'DCE'),
    ('E11 nine terms', 'Nine more terms'),
    ('E13 provenance 3.4.4', 'entry-UncondBr'),
    ('E13 seed02 fix', 'pre-entry-CondBr'),
    ('E15 vtable box', 'Virtual dispatch in 30 seconds'),
    ('E15 vtable[-1] fix', 'vtable[-1]'),
    ('E16 primer', 'One attack, end to end'),
    ('E16 cfi source lead', "cfi_pipe.c"),
    ('E16 vcall source lead', "vcall_pipe.cpp"),
    ('E16 canary source lead', "canary_pipe.c"),
]
for name, needle in checks:
    print(f'  {name}: {"OK" if needle in v3 else "MISSING: " + needle}')

# vtable[-2] should be gone
print(f'  stale vtable[-2] occurrences: {v3.count("vtable[-2]")} (expect 0)')

# inlined sources byte-exact vs .v3ref
import re
for refpath in ['cfi/cfi_pipe.c', 'cfi/vcall_pipe.cpp', 'canary/canary_pipe.c']:
    ref = open(f'{V}/.v3ref/{refpath}').read()
    fname = refpath.split('/')[1]
    ref_body = ref.rstrip('\n')
    # find the code fence containing the distinctive first line of each file
    first = ref_body.splitlines()[0]
    ok = first in v3 and ref_body.splitlines()[1] in v3
    print(f'  inlined {fname}: first line present={first in v3}, line2 present={ok}')

# v3 JSON words detail
d3 = json.load(open(f'{V}/docs/assets/volume3.json'))
byid = {l['id']: l for l in d3['lessons']}
print('--- volume3.json words (expected from executor report)')
expected = {79: 1338, 80: 1250, 81: 1311, 82: 1791, 86: 2087, 87: 1794, 88: 4303, 89: 2978}
for lid, exp in expected.items():
    l = byid[lid]
    calc = sum(count_block(b) for b in l['blocks'])
    status = 'OK' if calc == l['words'] == exp else f'MISMATCH (stored={l["words"]} calc={calc} expected={exp})'
    print(f'  id={lid}: {status}')
