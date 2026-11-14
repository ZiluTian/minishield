#!/usr/bin/env python3
"""Audit: every 'lesson N' ref in root volume1 between the first numbered
section (1.2.1) and the glossary (1.7.3) — i.e. in-text, not Background."""
import re

V = '/home/ruby.tian/minishield'
root = open(f'{V}/volume1').read().splitlines()
first = next(i for i, l in enumerate(root) if l.startswith('1.2.1 '))
gstart = next(i for i, l in enumerate(root) if l.startswith('1.7.3 Glossary'))

REF = re.compile(r'lesson[s]? \d+')
for i in range(first, gstart):
    for m in REF.finditer(root[i]):
        print(f'L{i + 1}: {m.group(0)!r}  |  {root[i][:90]}')
