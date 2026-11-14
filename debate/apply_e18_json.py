#!/usr/bin/env python3
"""E18 (JSON side): mirror the root header notes into JSON lesson 0 of each volume.

Inserts, at the top of lessons[0].blocks:
  - heading "How lesson references are numbered" + its paragraph (all volumes)
  - heading "Recurring blocks" + its paragraph (v1, v2 only)
Recomputes lessons[0]['words'] with the established counting formula.
Writes with the byte-identical recipe: json.dumps(d, indent=2, ensure_ascii=False) + '\n'.
Re-runnable: skips if the note is already present.
"""
import json
import re

V = '/home/ruby.tian/minishield'
HEADING_TITLE = 'How lesson references are numbered'
RECURRING_TITLE = 'Recurring blocks'
RECURRENCER_VOLS = (1, 2)
SECTION_HEAD = re.compile(r'^\d\.\d\.\d [A-Z]')  # real section heading: "2.1.1 Before ..."


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
            n += len(a.split()) if isinstance(a, str) else count_block(a)
    if 'blocks' in b:
        for c in b['blocks']:
            n += count_block(c)
    if 'title' in b:
        n += len(b['title'].split())
    return n


def extract_notes(root_text, with_recurring):
    """Return [(title, joined-paragraph-text)] for the header notes of a root file."""
    lines = root_text.splitlines()
    i = lines.index(HEADING_TITLE)
    assert set(lines[i + 1]) == {'='}, lines[i + 1]
    j = i + 2
    notes = []
    current_title = HEADING_TITLE
    current_body = []
    while j < len(lines):
        line = lines[j]
        if with_recurring and line == RECURRING_TITLE:
            notes.append((current_title, ' '.join(l for l in current_body if l.strip())))
            current_title = RECURRING_TITLE
            current_body = []
            assert set(lines[j + 1]) == {'='}, lines[j + 1]
            j += 2
            continue
        if line.startswith('Background.') or SECTION_HEAD.match(line):
            break
        current_body.append(line)
        j += 1
    notes.append((current_title, ' '.join(l for l in current_body if l.strip())))
    return notes


for vol in (1, 2, 3):
    root = open(f'{V}/volume{vol}').read()
    with_rec = vol in RECURRENCER_VOLS
    notes = extract_notes(root, with_rec)
    print(f'--- volume{vol}: {len(notes)} note(s)')
    for t, p in notes:
        print(f'    {t!r}: {p[:90]}...')

    jpath = f'{V}/docs/assets/volume{vol}.json'
    raw = open(jpath).read()
    d = json.loads(raw)
    lesson0 = d['lessons'][0]
    existing = [b.get('text', '') for b in lesson0['blocks'] if b['type'] == 'heading']
    if HEADING_TITLE in existing:
        print(f'    ALREADY PRESENT in lesson {lesson0["id"]}; skipping')
        continue
    new_blocks = []
    for t, p in notes:
        new_blocks.append({'type': 'heading', 'text': t})
        new_blocks.append({'type': 'paragraph', 'text': p})
    old_words = lesson0['words']
    lesson0['blocks'] = new_blocks + lesson0['blocks']
    lesson0['words'] = sum(count_block(b) for b in lesson0['blocks'])
    rt = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
    open(jpath, 'w').write(rt)
    again = open(jpath).read()
    d2 = json.loads(again)
    ok = json.dumps(d2, indent=2, ensure_ascii=False) + '\n' == again
    print(f'    lesson {lesson0["id"]} words: {old_words} -> {lesson0["words"]}; round-trip={ok}')
print('done')
