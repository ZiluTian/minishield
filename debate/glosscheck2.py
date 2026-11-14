#!/usr/bin/env python3
"""Wrapping-aware glossary ref comparison (root vs JSON).

Entry text = all lines from the '**Term.**' line to the next entry, joined.
Refs may wrap: '(see lessons\n10, 21).' -> matches r'lesson[s]?\s+\d+(?:,\s*\d+)*'.
"""
import json
import re

ROOT = '/home/ruby.tian/minishield/volume1'
JPATH = '/home/ruby.tian/minishield/docs/assets/volume1.json'

root = open(ROOT).read().splitlines()
gstart = next(i for i, l in enumerate(root) if l.startswith('1.7.3 Glossary'))

entries = {}
cur = None
start = None
for i, line in enumerate(root[gstart + 1:], start=gstart + 1):
    m = re.match(r'^\*\*(.+?)\*\*', line)
    if m:
        cur = m.group(1).strip()
        start = i
        entries[cur] = []
    if cur is not None:
        entries[cur].append(line)

d = json.load(open(JPATH))
byid = {l['id']: l for l in d['lessons']}
tbl = [b for b in byid[26]['blocks'] if b['type'] == 'table'][0]
jrows = {r[0].strip(): r[1] for r in tbl['rows'][1:]}

REF = re.compile(r'lesson[s]?\s+\d+(?:,\s*\d+)*')

bad = 0
for term, lines in entries.items():
    text = ' '.join(l.strip() for l in lines)
    refs = [re.sub(r'\s+', ' ', r) for r in REF.findall(text)]
    if not refs:
        continue
    row = jrows.get(term)
    if row is None:
        print(f'NO-JSON-ROW: {term!r} refs={refs}')
        bad += 1
        continue
    jrefs = [re.sub(r'\s+', ' ', r) for r in REF.findall(row)]
    if refs != jrefs:
        print(f'DIFF {term!r}:\n  root={refs}\n  json={jrefs}')
        bad += 1
print(f'entries with refs checked, diffs: {bad}')
