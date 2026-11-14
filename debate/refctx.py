#!/usr/bin/env python3
"""Print context for each flagged ref site: root line(s) + JSON text(s)."""
import json
import re

V = '/home/ruby.tian/minishield'
REF = re.compile(r'lesson[s]? \d+')

sites = [
    (1, '1.3.1', ['lesson 5', 'lesson 15', 'lesson 6', 'lesson 9', 'lesson 16']),
    (1, '1.3.3', ['lesson 3', 'lesson 1', 'lesson 5', 'lesson 2']),
    (1, '1.4.1', ['lesson 6']),
    (1, '1.4.4', ['lesson 9', 'lesson 19']),
    (1, '1.5.1', ['lesson 11']),
    (1, '1.5.3', ['lesson 16', 'lesson 18']),
    (1, '1.5.4', ['lesson 19']),
    (1, '1.7.3', ['lesson 0', 'lessons 11']),
    (1, 'BG', ['lesson 0', 'lesson 16', 'lesson 11', 'lesson 13', 'lesson 1', 'lesson 2', 'lesson 17', 'lesson 12', 'lesson 14']),
    (2, '2.2.2', ['lesson 1']),
    (2, '2.7.5', ['lesson 24']),
    (2, '2.13.1', ['lesson 3']),
    (2, '2.13.2', ['lesson 15']),
    (2, '2.13.3', ['lesson 1', 'lesson 13']),
]

V1_MAP = {'1.3.1': 4, '1.3.3': 6, '1.4.1': 8, '1.4.4': 11, '1.5.1': 15,
          '1.5.3': 17, '1.5.4': 23, '1.7.3': 26, 'BG': 0}
V2_MAP = {'2.2.2': 29, '2.7.5': 55, '2.13.1': 44, '2.13.2': 71, '2.13.3': 72}

for vol, sec, tokens in sites:
    print(f'===== v{vol} {sec} =====')
    if vol == 1:
        lines = open(f'{V}/volume1').read().splitlines()
        if sec == 'BG':
            rng = range(0, next(i for i, l in enumerate(lines) if l.startswith('1.2.1 ')))
        else:
            start = next(i for i, l in enumerate(lines) if l.startswith(sec + ' '))
            nxt = [i for i, l in enumerate(lines) if re.match(r'^\d\.\d+\.\d+ ', l) and i > start]
            rng = range(start, min(nxt) if nxt else len(lines))
        toks = [re.compile(r'\b' + re.escape(t) + r'\b') for t in tokens]
        for i in rng:
            if any(p.search(lines[i]) for p in toks):
                print(f'  ROOT L{i + 1}: {lines[i].strip()[:130]}')
    else:
        lines = open(f'{V}/volume2').read().splitlines()
        start = next(i for i, l in enumerate(lines) if l.startswith(sec + ' '))
        nxt = [i for i, l in enumerate(lines) if re.match(r'^\d\.\d+\.\d+ ', l) and i > start]
        toks = [re.compile(r'\b' + re.escape(t) + r'\b') for t in tokens]
        for i in range(start, min(nxt) if nxt else len(lines)):
            if any(p.search(lines[i]) for p in toks):
                print(f'  ROOT L{i + 1}: {lines[i].strip()[:130]}')
    d = json.load(open(f'{V}/docs/assets/volume{vol}.json'))
    lid = (V1_MAP if vol == 1 else V2_MAP)[sec]
    l = next(x for x in d['lessons'] if x['id'] == lid)
    toks = [re.compile(r'\b' + re.escape(t) + r'\b') for t in tokens]
    hits = []
    def walk(blocks):
        for b in blocks:
            t = b.get('text', '')
            if isinstance(t, str) and any(p.search(t) for p in toks):
                hits.append((b['type'], t))
            if 'items' in b:
                joined = ' '.join(x for x in b['items'] if isinstance(x, str))
                if any(p.search(joined) for p in toks):
                    hits.append(('list', joined))
            if 'blocks' in b:
                walk(b['blocks'])
    walk(l['blocks'])
    for typ, t in hits:
        for p in toks:
            m = p.search(t)
            if m:
                i = m.start()
                print(f'  JSON[{typ}]: ...{t[max(0, i - 80):i + 90]}...')
                break
    print()
