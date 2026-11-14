#!/usr/bin/env python3
"""E20: insert the CFI mechanism note into volume3 3.2.1 (root + JSON lesson 80).

Root: inserted between the end of the 'Where LTO can see the target, the check
changes shape' section and the '### Proof at runtime' heading.
JSON: inserted after block 10 ('The parsed address is compared ...'), before the
'Proof at runtime' heading block.
Recomputes lesson 80 words; byte-identical JSON recipe. Re-runnable (skips if present).
"""
import json

V = '/home/ruby.tian/minishield'
HEADING = 'What `type.test` is actually testing'

PARAS = [
    'The guard\'s second operand is the expected type as **call-site metadata**: in the minimal module it is the mangled type-info name `_ZTSFiiE` attached directly to the `type.test` call, and LTO\'s capture of the same check carries the pair `!{i64 0, !"_ZTSFiiE"}` \u2014 an offset and a name \u2014 recorded once per CFI-compiled function in the module\'s CFI metadata (the module flag `!{i32 4, !"CFI Canonical Jump Tables", i32 1}` marks the module as using this scheme; vcall\'s capture lists one such entry per class and per virtual method, `!{i64 16, !"_ZTS4Base"}`, `!{i64 16, !"_ZTSM4BaseFiiE.virtual"}`).',
    'This is why the check is an **LTO feature**. Without LTO, each translation unit only sees its own functions and the check has to fall back to a runtime-library lookup of the target\'s descriptor; with LTO the link step can merge the per-function descriptors into one table and the check becomes a direct resolution of the pointer against that table \u2014 no table, no check, hence the flag\'s hard requirement on `-flto`. The `.cfi` copy of `op_right` exists for the same reason: the rebuilt body carries its descriptor, while the original symbol stays behind as a one-instruction trampoline for callers that are not CFI-compiled.',
    '"Target set" therefore has a concrete meaning: it is *all functions whose descriptor matches this type* \u2014 a type as a coarse stand-in for an address set. That reconciles the landscape lesson\'s "target-set checks" with this lesson\'s "not an address check": the guard does not compare the pointer against a list of allowed addresses; it asks whether the pointed-to function\'s type descriptor agrees with the call site\'s.',
    'Reading the names: the Itanium mangling here is short on purpose. `_ZTS` marks a **type-info name** (the `__class_type_info` name field, not a function address); `Fii` is a function taking `i32` and returning `i32`; in vcall\'s `4Base`, the leading `4` is the length of the identifier `Base`.',
]

ROOT_NOTE = '''### What `type.test` is actually testing

The guard's second operand is the expected type as **call-site metadata**: in
the minimal module it is the mangled type-info name `_ZTSFiiE` attached
directly to the `type.test` call, and LTO's capture of the same check carries
the pair `!{i64 0, !"_ZTSFiiE"}` \u2014 an offset and a name \u2014 recorded once per
CFI-compiled function in the module's CFI metadata (the module flag
`!{i32 4, !"CFI Canonical Jump Tables", i32 1}` marks the module as using
this scheme; vcall's capture lists one such entry per class and per virtual
method, `!{i64 16, !"_ZTS4Base"}`, `!{i64 16, !"_ZTSM4BaseFiiE.virtual"}`).

This is why the check is an **LTO feature**. Without LTO, each translation
unit only sees its own functions and the check has to fall back to a
runtime-library lookup of the target's descriptor; with LTO the link step can
merge the per-function descriptors into one table and the check becomes a
direct resolution of the pointer against that table \u2014 no table, no check,
hence the flag's hard requirement on `-flto`. The `.cfi` copy of `op_right`
exists for the same reason: the rebuilt body carries its descriptor, while
the original symbol stays behind as a one-instruction trampoline for callers
that are not CFI-compiled.

"Target set" therefore has a concrete meaning: it is *all functions whose
descriptor matches this type* \u2014 a type as a coarse stand-in for an address
set. That reconciles the landscape lesson's "target-set checks" with this
lesson's "not an address check": the guard does not compare the pointer
against a list of allowed addresses; it asks whether the pointed-to
function's type descriptor agrees with the call site's.

Reading the names: the Itanium mangling here is short on purpose. `_ZTS`
marks a **type-info name** (the `__class_type_info` name field, not a
function address); `Fii` is a function taking `i32` and returning `i32`; in
vcall's `4Base`, the leading `4` is the length of the identifier `Base`.
'''

# consistency: root note paragraphs (unwrapped) must equal PARAS
root_paras = []
for chunk in ROOT_NOTE.strip().split('\n\n'):
    if chunk.startswith('###'):
        continue
    root_paras.append(' '.join(chunk.strip().split('\n')))
assert root_paras == PARAS, 'root/JSON text mismatch'

# ---- root ----
path = f'{V}/volume3'
root = open(path).read()
if '### What `type.test` is actually testing' in root:
    print('root: ALREADY PRESENT; skipping')
else:
    anchor = 'in whatever form is cheapest there.\n\n### Proof at runtime'
    assert root.count(anchor) == 1, f'anchor count={root.count(anchor)}'
    root = root.replace(anchor, 'in whatever form is cheapest there.\n\n' + ROOT_NOTE + '### Proof at runtime')
    open(path, 'w').write(root)
    print('root: inserted')

# ---- json ----
jpath = f'{V}/docs/assets/volume3.json'
raw = open(jpath).read()
d = json.loads(raw)


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


l80 = [x for x in d['lessons'] if x['id'] == 80][0]
if any(b.get('text', '') == HEADING for b in l80['blocks']):
    print('json: ALREADY PRESENT; skipping')
else:
    idx = next(i for i, b in enumerate(l80['blocks'])
               if b['type'] == 'heading' and b['text'] == 'Proof at runtime')
    assert l80['blocks'][idx - 1]['text'].startswith('The parsed address is compared'), 'unexpected predecessor'
    new_blocks = [{'type': 'heading', 'text': HEADING}]
    new_blocks += [{'type': 'paragraph', 'text': p} for p in PARAS]
    old_words = l80['words']
    l80['blocks'] = l80['blocks'][:idx] + new_blocks + l80['blocks'][idx:]
    l80['words'] = sum(count_block(b) for b in l80['blocks'])
    rt = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
    open(jpath, 'w').write(rt)
    d2 = json.loads(open(jpath).read())
    ok = json.dumps(d2, indent=2, ensure_ascii=False) + '\n' == open(jpath).read()
    print(f'json: lesson 80 words {old_words} -> {l80["words"]}; round-trip={ok}')
print('done')
