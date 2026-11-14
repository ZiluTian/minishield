#!/usr/bin/env python3
"""Compare root volume1 glossary lesson refs vs the JSON web-book glossary table."""
import json
import re

ROOT = '/home/ruby.tian/minishield/volume1'
JPATH = '/home/ruby.tian/minishield/docs/assets/volume1.json'

root = open(ROOT).read().splitlines()
gstart = next(i for i, l in enumerate(root) if l.startswith('1.7.3 Glossary'))
gloss = '\n'.join(root[gstart:])

entries = {}
cur = None
for line in gloss.splitlines()[1:]:
    m = re.match(r'^\*\*(.+?)\*\*', line)
    if m:
        cur = m.group(1).strip()
        entries[cur] = []
    if cur is not None:
        entries[cur].extend(re.findall(r'lesson[s]? \d+(?:, \d+)*', line))

d = json.load(open(JPATH))
byid = {l['id']: l for l in d['lessons']}
tbl = [b for b in byid[26]['blocks'] if b['type'] == 'table'][0]
jrows = {r[0].strip(): r[1] for r in tbl['rows'][1:]}

REF = re.compile(r'lesson[s]? \d+(?:, \d+)*')
bad = 0
for term, refs in sorted(entries.items()):
    if not refs:
        continue
    row = jrows.get(term)
    if row is None:
        print(f"NO-JSON-ROW: {term!r} root-refs={sorted(set(refs))}")
        bad += 1
        continue
    jrefs = REF.findall(row)
    if set(refs) != set(jrefs):
        print(f"DIFF {term!r}:\n  root={sorted(set(refs))}\n  json={sorted(set(jrefs))}")
        bad += 1
print(f"entries with refs: {sum(1 for v in entries.values() if v)}, diffs: {bad}")
