#!/usr/bin/env python3
"""E21 scanner: dump all session-voice sites with context (current line numbers)."""
import re

V = '/home/ruby.tian/minishield'

for vol in (1, 2, 3):
    lines = open(f'{V}/volume{vol}').read().splitlines()
    print(f'===== volume{vol} =====')
    print('-- header (lines 1-12)')
    for i in range(12):
        print(f'  L{i+1}: {lines[i]}')
    print('-- study-session walkthrough headings')
    for i, l in enumerate(lines):
        if l.startswith('### Study-session walkthrough'):
            body = ''
            for j in range(i + 2, min(i + 4, len(lines))):
                if lines[j].strip():
                    body = lines[j]
                    break
            print(f'  L{i+1}: {l}')
            print(f'        body: {body[:100]}')
    print('-- Observed markers')
    for i, l in enumerate(lines):
        if re.search(r'Observed [a-z]+', l):
            print(f'  L{i+1}: {l[:150]}')
    print('-- the learner (case-insensitive)')
    for i, l in enumerate(lines):
        if re.search(r'the learner', l, re.I):
            print(f'  L{i+1}: {l[:150]}')
    print('-- first draft')
    for i, l in enumerate(lines):
        if 'first draft' in l:
            print(f'  L{i+1}: {l[:150]}')
    print()
