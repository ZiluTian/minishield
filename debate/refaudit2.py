#!/usr/bin/env python3
"""Compare every 'lesson[s] N' token: root file vs JSON, per volume, per lesson."""
import json
import re
from collections import Counter

V = '/home/ruby.tian/minishield'
REF = re.compile(r'lesson[s]? \d+')

# root section -> start/end line (0-based), matched to JSON lessons by title.
def root_sections(path):
    lines = open(path).read().splitlines()
    secs = []
    pat = re.compile(r'^\d\.\d+\.\d+ ')
    idx = [i for i, l in enumerate(lines) if pat.match(l)]
    for k, i in enumerate(idx):
        end = idx[k + 1] if k + 1 < len(idx) else len(lines)
        title = lines[i].split(None, 2)[-1] if len(lines[i].split(None, 2)) > 2 else lines[i]
        secs.append((i, end, lines[i]))
    return lines, secs

def json_texts(path):
    d = json.load(open(path))
    out = {}
    for l in d['lessons']:
        texts = [l.get('title', ''), l.get('summary', ''), l.get('takeaway', '')]
        def walk(blocks):
            for b in blocks:
                if 'text' in b and isinstance(b['text'], str):
                    texts.append(b['text'])
                if 'title' in b and isinstance(b['title'], str):
                    texts.append(b['title'])
                if 'items' in b:
                    texts.extend(x for x in b['items'] if isinstance(x, str))
                if 'rows' in b:
                    for r in b['rows']:
                        if isinstance(r, str):
                            texts.append(r)
                        elif isinstance(r, list):
                            texts.extend(str(c) for c in r)
                        elif isinstance(r, dict):
                            texts.extend(str(c) for c in r.values())
                if 'blocks' in b:
                    walk(b['blocks'])
        walk(l['blocks'])
        out[l['id']] = ' '.join(texts)
    return out

# v1: map root section -> json id via the verified mapping
V1_MAP = {
    '1.2.1': 1, '1.2.2': 2, '1.2.3': 3,
    '1.3.1': 4, '1.3.2': 5, '1.3.3': 6, '1.3.4': 7,
    '1.4.1': 8, '1.4.2': 9, '1.4.3': 10, '1.4.4': 11, '1.4.5': 12,
    '1.4.6': 13, '1.4.7': 14, '1.5.1': 15, '1.5.2': 16, '1.5.3': 17,
    '1.5.4': 23, '1.5.5': 78,
    '1.6.1': 75, '1.6.2': 76, '1.6.3': 77, '1.6.4': 73, '1.6.5': 74,
    '1.7.1': 18, '1.7.2': 19, '1.7.3': 26,
}
V2_MAP = {
    '2.1.1': 27, '2.2.1': 28, '2.2.2': 29, '2.2.3': 30,
    '2.3.1': 31, '2.3.2': 32, '2.3.3': 33, '2.3.4': 34, '2.3.5': 35, '2.3.6': 36,
    '2.4.1': 37, '2.4.2': 38,
    '2.5.1': 39, '2.5.2': 40, '2.5.3': 41, '2.5.4': 42, '2.5.5': 43,
    '2.6.1': 45, '2.6.2': 46, '2.6.3': 47, '2.6.4': 48, '2.6.5': 49, '2.6.6': 50,
    '2.7.1': 51, '2.7.2': 52, '2.7.3': 53, '2.7.4': 54, '2.7.5': 55,
    '2.8.1': 56, '2.8.2': 57,
    '2.9.1': 58, '2.9.2': 59, '2.9.3': 60, '2.9.4': 61,
    '2.10.1': 62, '2.10.2': 63, '2.10.3': 64,
    '2.11.1': 65, '2.11.2': 66,
    '2.12.1': 67, '2.12.2': 68, '2.12.3': 69,
    '2.13.1': 44, '2.13.2': 71, '2.13.3': 72, '2.13.4': 70,
}
V3_MAP = {
    '3.1.1': 79, '3.2.1': 80, '3.2.2': 81, '3.3.1': 82,
    '3.4.1': 83, '3.4.2': 84, '3.4.3': 85, '3.4.4': 86,
    '3.5.1': 87, '3.6.1': 88, '3.7.1': 89,
}
for vol, mapping in [(1, V1_MAP), (2, V2_MAP), (3, V3_MAP)]:
    lines, secs = root_sections(f'{V}/volume{vol}')
    jtext = json_texts(f'{V}/docs/assets/volume{vol}.json')
    for i, end, head in secs:
        num = head.split()[0]
        lid = mapping[num]
        rrefs = Counter(REF.findall('\n'.join(lines[i:end])))
        jrefs = Counter(REF.findall(jtext[lid]))
        diff_r = rrefs - jrefs
        diff_j = jrefs - rrefs
        if diff_r or diff_j:
            print(f'v{vol} {num} (id {lid}):')
            if diff_r:
                print(f'   root-only: {dict(diff_r)}')
            if diff_j:
                print(f'   json-only: {dict(diff_j)}')
    # Background (before first section) vs lesson 0 — v1 only
    if vol != 1:
        continue
    bg = '\n'.join(lines[:secs[0][0]])
    rrefs = Counter(REF.findall(bg))
    jrefs = Counter(REF.findall(jtext[0]))
    if rrefs - jrefs or jrefs - rrefs:
        print(f'v{vol} Background (id 0):')
        if rrefs - jrefs:
            print(f'   root-only: {dict(rrefs - jrefs)}')
        if jrefs - rrefs:
            print(f'   json-only: {dict(jrefs - rrefs)}')
print('done')
