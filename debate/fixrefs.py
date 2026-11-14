#!/usr/bin/env python3
"""E18 root-side cross-ref reconciliation (volume1 + volume2).

Every diffed glossary entry is a single ref-token on each side
("lesson N" or "lessons A, B"), so the fix is a word-boundary token
replacement scoped to the entry's line range. Plan by default;
--apply to modify the root files.
"""
import json
import re

ROOT1 = '/home/ruby.tian/minishield/volume1'
ROOT2 = '/home/ruby.tian/minishield/volume2'
J1 = '/home/ruby.tian/minishield/docs/assets/volume1.json'

REF = re.compile(r'lesson[s]? \d+(?:, \d+)*')


def j1_glossary_refs():
    d = json.load(open(J1))
    byid = {l['id']: l for l in d['lessons']}
    tbl = [b for b in byid[26]['blocks'] if b['type'] == 'table'][0]
    return {r[0].strip(): REF.findall(r[1]) for r in tbl['rows'][1:]}


def root1_glossary_entries():
    root = open(ROOT1).read().splitlines()
    gstart = next(i for i, l in enumerate(root) if l.startswith('1.7.3 Glossary'))
    entries = {}
    for i, line in enumerate(root[gstart + 1:], start=gstart + 1):
        m = re.match(r'^\*\*(.+?)\*\*', line)
        if m:
            entries[m.group(1).strip()] = i
    # ranges: from start to next entry start
    starts = sorted(entries.values())
    for term, s in entries.items():
        nxt = next((x for x in starts if x > s), len(root))
        entries[term] = (s, nxt)
    return entries


def main():
    apply = '--apply' in __import__('sys').argv
    jrefs = j1_glossary_refs()
    entries = root1_glossary_entries()

    plan = []
    for term, (s, e) in sorted(entries.items()):
        lines = open(ROOT1).read().splitlines()[s:e]
        rrefs = REF.findall('\n'.join(lines))
        if not rrefs:
            continue
        jrow = jrefs.get(term)
        if jrow is None:
            print(f"NO-JSON-ROW (skip): {term!r}")
            continue
        if len(set(rrefs)) != 1 or len(set(jrow)) != 1:
            print(f"MULTI-TOKEN (manual): {term!r} root={set(rrefs)} json={set(jrow)}")
            continue
        if set(rrefs) == set(jrow):
            continue
        plan.append((term, s, e, rrefs[0], jrow[0]))

    print(f"plan: {len(plan)} glossary token replacements")
    for term, s, e, old, new in plan:
        print(f"  L{s+1}-{e}: {term[:45]!r}: {old!r} -> {new!r}")

    if not apply:
        print("\nplan only; re-run with --apply")
        return

    lines = open(ROOT1).read().splitlines()
    done = 0
    for term, s, e, old, new in plan:
        pat = re.compile(r'(?<![0-9A-Za-z])' + re.escape(old) + r'(?![0-9])')
        hit = False
        for i in range(s, e):
            lines[i], n = pat.subn(new, lines[i])
            if n:
                hit = True
        if not hit:
            print(f"  !! NOT FOUND: {term!r}")
        else:
            done += 1

    text = '\n'.join(lines)
    bg = [
        ("The current policy (lesson 22) rejects", "The current policy (lesson 23) rejects"),
        ("completely unchanged — lesson 24 shows how to", "completely unchanged — lesson 23 shows how to"),
        ("not to transform. By lesson 22 the", "not to transform. By lesson 23 the"),
    ]
    for a, b in bg:
        if a in text:
            text = text.replace(a, b, 1)
            done += 1
        else:
            print(f"  !! BG NOT FOUND: {a[:45]!r}")

    open(ROOT1, 'w').write(text)
    print(f"volume1 applied: {done}")

    r2 = open(ROOT2).read()
    v2 = [
        ("calls, and the C++ API: lesson 29, the Volume 2 LLVM document",
         "calls, and the C++ API: lesson 43, the Volume 2 LLVM document"),
        ("casts, classes, and translation units: lesson 30, the Volume 2 C++ document",
         "casts, classes, and translation units: lesson 44, the Volume 2 C++ document"),
    ]
    for a, b in v2:
        if a in r2:
            r2 = r2.replace(a, b, 1)
            print(f"volume2 applied: lesson {a[-60:][:20]}...")
            done += 1
        else:
            print(f"  !! V2 NOT FOUND: {a[:50]!r}")
    open(ROOT2, 'w').write(r2)


if __name__ == '__main__':
    main()
