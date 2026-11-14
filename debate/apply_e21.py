#!/usr/bin/env python3
"""E21 applier: book-wide session-voice cleanup.

Root: volume1/volume2/volume3
  - 49 'Study-session walkthrough' headings -> 'Common mistake:' (12) / 'Gotcha:' (37)
  - Observed marker rewrites (v1: 10 + 1 environment; v2: 5)
  - 'the learner' rewrites (v1: 4, v2: 4, v3: 2 header lines)
  - 'first draft' x2 (v2)
  - 3 volume headers
JSON: docs/assets/volume1.json (lessons 0-17, 74) + volume2.json (touched set)
  - same logical replacements; lesson 74 JSON-only heading relabel
  - words recomputed for every touched lesson (73/76/77 never touched)
Re-runnable: idempotence guards skip already-applied items.
"""
import json
import re

V = '/home/ruby.tian/minishield'

# ---------------------------------------------------------------- root text

def repl_inline(text, old, new, label, count=1):
    n = text.count(old)
    if n == 0:
        assert text.count(new) >= 1, f'{label}: neither old nor new present'
        print(f'  {label}: already applied')
        return text
    assert n == count, f'{label}: expected {count} of {old[:60]!r}, found {n}'
    return text.replace(old, new)


def repl_line(lines, anchor, new_line, label):
    idx = [i for i, l in enumerate(lines) if anchor in l]
    if not idx:
        assert any(new_line in l for l in lines), f'{label}: not found and not applied'
        print(f'  {label}: already applied')
        return
    assert len(idx) == 1, f'{label}: anchor {anchor!r} found {len(idx)}x'
    lines[idx[0]] = new_line
    print(f'  {label}: line {idx[0] + 1}')


def repl_block(lines, anchor, new_lines, label):
    """Replace the paragraph (consecutive non-empty lines) containing anchor."""
    idx = [i for i, l in enumerate(lines) if anchor in l]
    if not idx:
        assert any(l.startswith(new_lines[0]) for l in lines), f'{label}: not found and not applied'
        print(f'  {label}: already applied')
        return
    assert len(idx) == 1, f'{label}: anchor {anchor!r} found {len(idx)}x'
    i = idx[0]
    j = i
    while j + 1 < len(lines) and lines[j + 1].strip():
        j += 1
    lines[i:j + 1] = new_lines
    print(f'  {label}: lines {i + 1}-{j + 1}')


# ---- heading relabels (topic -> new prefix)
V1_CM = [  # 'Common mistake:' (7)
    'give headers, linked symbols, and output paths different jobs',
    'build.ninja comes from configuration, not from the build command',
    'a header declaration, implementation, and plugin entry point are not interchangeable',
    'a balanced pipeline is checked before the pass runs',
    'diagnose runtime registration separately from compile-time visibility',
    'switch classification still needs the installed opcode names',
    'a readable test runner is still a program with syntax',
]
V1_GT = [  # 'Gotcha:' (11)
    'separate the program being compiled from the pass doing the work',
    'activation selects tools; the manifest describes their installation',
    'required changes skipping behavior, not scheduling',
    'turn a user-facing pipeline string into a pass object',
    'finish a small interface before solving its behavior',
    'the function manager already chose the function',
    'write an expectation before trusting a report',
    'prove that reading did not secretly edit the program',
    'one branch instruction can represent two graph edges',
    'return graph facts instead of making later passes parse text',
    'fill one record completely, then append it',
]
V2_CM = [  # 'Common mistake:' (5)
    'collect a worklist before calling a mutating helper',
    'the push_back mismatch is about the static pointer type',
    'a filter does not append, and an empty first stage is not the end',
    'object, address, and key/value pair are separate C++ ideas',
    'the C++ handle is not the IR label',
]
V2_GT = [  # 'Gotcha:' (26)
    'make one representation change at a time',
    'demotion replaces a choice, not merely a line of text',
    'a PHI-free graph can still carry values between blocks',
    'void describes a result, not whether an operation matters',
    'an allocation produces an address, not its stored integer',
    'the argument type tells you whether to pass the pointer or the object',
    'demote the collected result, then track the actual edit',
    'trace one number through an ordinary spill',
    'trace a choice through PHI demotion',
    'give a next-block decision an integer encoding',
    'construct valid machinery before making it live',
    'initialize the state before the first dispatcher read',
    'operation, result, and storage are different',
    'why an allocation must dominate its uses',
    'build the result-type guard',
    'an intrinsic is a special operation expressed as a call',
    'musttail is a requirement, not a hint',
    'inspect inline-assembly calls through CallBase',
    'a convergent call has participation constraints',
    'an operand bundle is part of call semantics',
    'returns_twice can resume one continuation again',
    'naked changes the function\u2019s low-level entry/exit contract',
    'declare the builder interface first',
    'define the first implementation body',
    'turn the entry branch into a runtime state choice',
    'keep the original default while lowering cases',
]


def relabel_headings(text, cm_topics, gt_topics, label):
    for topic in cm_topics:
        old = f'### Study-session walkthrough \u2014 {topic}'
        if old in text:
            text = repl_inline(text, old, f'### Common mistake: {topic}', f'{label} cm:{topic[:40]}')
        else:
            assert f'### Common mistake: {topic}' in text, f'{label}: missing cm {topic[:40]!r}'
    for topic in gt_topics:
        old = f'### Study-session walkthrough \u2014 {topic}'
        if old in text:
            text = repl_inline(text, old, f'### Gotcha: {topic}', f'{label} gt:{topic[:40]}')
        else:
            assert f'### Gotcha: {topic}' in text, f'{label}: missing gt {topic[:40]!r}'
    return text


print('== volume1 (root)')
t = open(f'{V}/volume1').read()
t = repl_inline(t, 'Recorded from the study sessions on 2026-11-11 and 2026-11-12',
                'Expanded 2026-11-12', 'v1 header L2')
t = repl_inline(
    t,
    'The learner writes the C++ and test scripts. Each lesson gives a small task, explains the concept, shows a check, and records the mistakes encountered along the way.',
    'You write the C++ and test scripts. Each lesson gives a small task, explains the concept, shows a check, and flags the mistakes you are likely to make.',
    'v1 header L6')
t = repl_inline(
    t,
    'The learner preferred switch/case. Use switch (I.getOpcode()) with these\nopcode names in this installed LLVM 23 version:',
    'Classify with switch (I.getOpcode()) rather than a long if/else chain:\nthe switch keeps every covered opcode visible in one place. Use these\nopcode names in this installed LLVM 23 version:',
    'v1 switch/case')
t = repl_inline(t, 'An empty diff is expected and was reported by the learner. Both paths use',
                'An empty diff is expected. Both paths use', 'v1 empty diff')
t = repl_inline(t, 'The learner should write it.', 'You write it.', 'v1 CFGAnalyzer')
t = relabel_headings(t, V1_CM, V1_GT, 'v1')
lines = t.splitlines(keepends=False)
repl_block(lines, 'Observed error: Ninja could not find build.ninja', [
    'Common mistake: running the build before configuration completes. If the',
    'build directory has CMakeCache.txt but generation has not completed, Ninja',
    'cannot find build.ninja; running the configuration command creates',
    'build.ninja. A cache file alone is insufficient.',
], 'v1 R1 ninja')
repl_block(lines, 'Observed result: "ninja: no work to do"', [
    '"ninja: no work to do" means the target is up to date. It is not a test',
    'result or an indication that the plugin failed.',
], 'v1 R2 no work')
repl_block(lines, 'Environment issue encountered:', [
    'Environment issue: the compiler could not find <type_traits>.',
    'The Conda environment had the runtime but lacked its matching C++ development',
    'headers. Installing libstdcxx-devel_linux-64 16.2.0 supplied those headers.',
    'The LIBRARY_PATH export addresses the separate linker search for libstdc++.',
], 'v1 R3 env')
repl_block(lines, 'Observed mistakes: the header was initially named', [
    'Common mistake: naming the header FlatteningPass.cpp while the includes',
    'request FlatteningPass.h. Rename the declaration file to .h. Plugin.cpp',
    'also needs semicolons after the callback registration expression and the',
    'returned aggregate initializer. Read the compiler location and check the',
    'surrounding statement boundaries when diagnosing these syntax errors.',
], 'v1 R4 naming')
repl_block(lines, 'Observed error: function(minishield-flatten)]', [
    'Common mistake: writing function(minishield-flatten)] with an extra',
    'closing bracket. Pipeline syntax must be valid before LLVM can run any pass.',
], 'v1 R5 bracket')
repl_block(lines, 'Observed error: "unknown function pass', [
    'Common mistake: the "unknown function pass \'minishield-stats\'" error means',
    'the loaded plugin does not register that name. Defining a class alone does',
    'not register it. Also check that the plugin is rebuilt after adding the',
    'registration.',
], 'v1 R6 register')
repl_block(lines, 'Observed error: "no member named', [
    'Common mistake: including FlatteningPass.h twice instead of StatsPass.h, so',
    'the compiler reports "no member named \'StatsPass\' in namespace',
    '\'minishield\'". It needs the declaration in this translation unit; CMake\'s',
    'source list supplies the implementation at link time but does not replace',
    'includes.',
], 'v1 R7 include')
repl_block(lines, 'Observed correction: an earlier teaching example', [
    'Common mistake: reaching for Instruction::Br, which does not exist here.',
    'This version has separate CondBr and UncondBr opcodes. Consult',
    'llvm/IR/Instruction.def to inspect the installed names.',
], 'v1 R8 Br')
repl_block(lines, 'Observed bug: a missing break', [
    'Common mistake: a missing break after a branch case also increments the',
    'switch counter through fallthrough. Compilation success alone does not',
    'detect that counting mistake; the fixture expectations do.',
], 'v1 R9 break')
repl_block(lines, 'Observed omission: switches was counted', [
    'Common mistake: counting a metric but leaving it out of the printed report.',
    'Every requested metric must appear in the output.',
], 'v1 R10 omission')
repl_block(lines, 'Observed error: Bash reported "unexpected end of file"', [
    'Common mistake: writing don instead of done to close a Bash loop. Bash',
    'reports "unexpected end of file" because it reaches the end of the file',
    'while still expecting the loop to close.',
], 'v1 R11 don')
open(f'{V}/volume1', 'w').write('\n'.join(lines) + '\n')

print('== volume2 (root)')
lines = open(f'{V}/volume2').read().splitlines(keepends=False)
repl_line(lines, 'Study notes and future exercises', 'Exercises and reference material \u00b7 expanded 2026-11-13', 'v2 header L2')
repl_line(lines, 'The learner writes the implementation and scripts.',
          'You write the implementation and scripts.', 'v2 header L8')
for i, l in enumerate(lines):
    if 'they do not change the learner' in l:
        assert 'source files.' in l
        lines[i] = re.sub(r"the learner.s source files\.", 'your source files.', l)
        print(f'  v2 header L{i + 1} (learner\'s)')
        break
t = '\n'.join(lines)
t = repl_inline(t, 'not a claim that the learner implementation has reached it.',
                'not a claim that your implementation has reached it.', 'v2 L7042')
t = repl_inline(t, 'errors found in the first draft.', 'errors from the first attempt.', 'v2 L2699')
t = repl_inline(t, 'block found in the first draft.', 'block from the first attempt.', 'v2 L3388')
t = relabel_headings(t, V2_CM, V2_GT, 'v2')
lines = t.splitlines(keepends=False)
repl_block(lines, 'Observed error: phis.push_back', [
    'Common mistake: phis.push_back(&I) fails because the vector needs PHINode*, but &I is still Instruction*. Saving the result as phi makes the argument type match.',
], 'v2 O12')
repl_block(lines, 'Observed error: Do not delete PHIs', [
    'Common pitfall: do not delete PHIs while using an ordinary loop over the same instruction list. Collecting first avoids using an invalidated iterator.',
], 'v2 O13')
repl_block(lines, 'Observed error: The reviewed draft created', [
    'Common mistake: declaring escapingValues and applying the filters without pushing any instruction. A filter rejects unsuitable values; it does not automatically collect the suitable ones.',
], 'v2 O14')
repl_block(lines, 'Observed error: const auto *BB', [
    'Common mistake: const auto *BB would be a pointer to const BasicBlock and would not implicitly convert to the map\u2019s BasicBlock* key. const auto BB instead makes the copied pointer itself const. These are different declarations.',
], 'v2 O15')
repl_block(lines, 'Observed error: The build failed before producing', [
    'Common mistake: testing an existing .so after a failed build. The build failed before producing a new plugin; an existing .so can still contain an older implementation, so the test does not verify the draft you just wrote.',
], 'v2 O16')
open(f'{V}/volume2', 'w').write('\n'.join(lines) + '\n')

print('== volume3 (root)')
lines = open(f'{V}/volume3').read().splitlines(keepends=False)
repl_line(lines, 'Study notes and future exercises', 'Exercises and reference material \u00b7 expanded 2026-11-13', 'v3 header L2')
repl_line(lines, 'The learner writes the implementation and scripts.',
          'You write the implementation and scripts.', 'v3 header L8')
for i, l in enumerate(lines):
    if 'they do not change the learner' in l:
        lines[i] = re.sub(r"the learner.s source files\.", 'your source files.', l)
        print(f'  v3 header L{i + 1} (learner\'s)')
        break
open(f'{V}/volume3', 'w').write('\n'.join(lines) + '\n')

# ---------------------------------------------------------------- JSON

def heading_pairs(cm_topics, gt_topics):
    subs = [(f'Study-session walkthrough \u2014 {t}', f'Common mistake: {t}') for t in cm_topics]
    subs += [(f'Study-session walkthrough \u2014 {t}', f'Gotcha: {t}') for t in gt_topics]
    return subs

V1_J_HEADINGS = heading_pairs(V1_CM, V1_GT)
V2_J_HEADINGS = heading_pairs(V2_CM, V2_GT)

# substring replacements applied to every string leaf of the volume
V1_JSON_SUBS = [
    ('The learner preferred `switch/case`. Use `switch (I.getOpcode())` with these opcode names in this installed LLVM 23 version:',
     'Classify with `switch (I.getOpcode())` rather than a long if/else chain: the switch keeps every covered opcode visible in one place. Use these opcode names in this installed LLVM 23 version:'),
    ('An empty diff is expected and was reported by the learner.', 'An empty diff is expected.'),
    ('The learner should write it.', 'You write it.'),
    ('Study-session walkthrough \u2014 construct and inspect a dispatcher', 'Construct and inspect a dispatcher'),
    # Observed-marker rewrites (mirror the root, unwrapped)
    ('Observed error: Ninja could not find build.ninja. The build directory had CMakeCache.txt, but generation had not completed. Running the configuration command successfully created build.ninja. A cache file alone is insufficient.',
     'Common mistake: running the build before configuration completes. If the build directory has CMakeCache.txt but generation has not completed, Ninja cannot find build.ninja; running the configuration command creates build.ninja. A cache file alone is insufficient.'),
    ('Observed result: "ninja: no work to do" means the target is up to date. It is not a test result or an indication that the plugin failed.',
     '"ninja: no work to do" means the target is up to date. It is not a test result or an indication that the plugin failed.'),
    ('Environment issue encountered: the compiler could not find <type_traits>.',
     'Environment issue: the compiler could not find <type_traits>.'),
    ('Observed mistakes: the header was initially named FlatteningPass.cpp, while the includes requested FlatteningPass.h. Rename the declaration file to .h. Plugin.cpp also needed semicolons after the callback registration expression and the returned aggregate initializer. Read the compiler location and check the surrounding statement boundaries when diagnosing these syntax errors.',
     'Common mistake: naming the header FlatteningPass.cpp while the includes request FlatteningPass.h. Rename the declaration file to .h. Plugin.cpp also needs semicolons after the callback registration expression and the returned aggregate initializer. Read the compiler location and check the surrounding statement boundaries when diagnosing these syntax errors.'),
    ('Observed error: function(minishield-flatten)] had an extra closing bracket. Pipeline syntax must be valid before LLVM can run any pass.',
     'Common mistake: writing function(minishield-flatten)] with an extra closing bracket. Pipeline syntax must be valid before LLVM can run any pass.'),
    ('Observed error: "unknown function pass \'minishield-stats\'" meant the loaded plugin did not register that name. Defining a class alone does not register it. Also check that the plugin was rebuilt after adding the registration.',
     'Common mistake: the "unknown function pass \'minishield-stats\'" error means the loaded plugin does not register that name. Defining a class alone does not register it. Also check that the plugin is rebuilt after adding the registration.'),
    ('Observed error: "no member named \'StatsPass\' in namespace \'minishield\'" came from including FlatteningPass.h twice instead of including StatsPass.h. The compiler needs the declaration in this translation unit. CMake\'s source list supplies the implementation at link time; it does not replace includes.',
     'Common mistake: including FlatteningPass.h twice instead of StatsPass.h, so the compiler reports "no member named \'StatsPass\' in namespace \'minishield\'". It needs the declaration in this translation unit; CMake\'s source list supplies the implementation at link time but does not replace includes.'),
    ('Observed correction: an earlier teaching example used Instruction::Br, which does not exist here. This version has separate CondBr and UncondBr opcodes. Consult llvm/IR/Instruction.def to inspect the installed names.',
     'Common mistake: reaching for Instruction::Br, which does not exist here. This version has separate CondBr and UncondBr opcodes. Consult llvm/IR/Instruction.def to inspect the installed names.'),
    ('Observed bug: a missing break after a branch case would also increment the switch counter through fallthrough. Compilation success alone would not detect that counting mistake; the fixture expectations would.',
     'Common mistake: a missing break after a branch case also increments the switch counter through fallthrough. Compilation success alone does not detect that counting mistake; the fixture expectations do.'),
    ('Observed omission: switches was counted but initially absent from the printed report. Every requested metric must also appear in the output.',
     'Common mistake: counting a metric but leaving it out of the printed report. Every requested metric must appear in the output.'),
    ('Observed error: Bash reported "unexpected end of file" because the final loop-closing word was written as don instead of done. Bash reached the file\'s end while still expecting the loop to close.',
     'Common mistake: writing don instead of done to close a Bash loop. Bash reports "unexpected end of file" because it reaches the end of the file while still expecting the loop to close.'),
]
V2_JSON_SUBS = [
    ('errors found in the first draft.', 'errors from the first attempt.'),
    ('block found in the first draft.', 'block from the first attempt.'),
    ('not a claim that the learner implementation has reached it.', 'not a claim that your implementation has reached it.'),
    # Observed-marker rewrites (mirror the root)
    ('Observed error: phis.push_back(&I) fails because the vector needs PHINode* but &I remains Instruction*. Saving the result as phi makes the argument type match.',
     'Common mistake: phis.push_back(&I) fails because the vector needs PHINode*, but &I is still Instruction*. Saving the result as phi makes the argument type match.'),
    ('Observed error: Do not delete PHIs while using an ordinary loop over the same instruction list. Collecting first avoids using an invalidated iterator.',
     'Common pitfall: do not delete PHIs while using an ordinary loop over the same instruction list. Collecting first avoids using an invalidated iterator.'),
    ('Observed error: The reviewed draft created escapingValues and applied the filters, but did not push any instruction. A filter rejects unsuitable values; it does not automatically collect the suitable ones.',
     'Common mistake: declaring escapingValues and applying the filters without pushing any instruction. A filter rejects unsuitable values; it does not automatically collect the suitable ones.'),
    ('Observed error: const auto *BB would be a pointer to const BasicBlock and would not implicitly convert to the map\u2019s BasicBlock* key. const auto BB instead makes the copied pointer itself const. These are different declarations.',
     'Common mistake: const auto *BB would be a pointer to const BasicBlock and would not implicitly convert to the map\u2019s BasicBlock* key. const auto BB instead makes the copied pointer itself const. These are different declarations.'),
    ('Observed error: The build failed before producing a new plugin. An existing .so can still contain an older implementation; testing it after a failed build does not verify the draft you just wrote.',
     'Common mistake: testing an existing .so after a failed build. The build failed before producing a new plugin; an existing .so can still contain an older implementation, so the test does not verify the draft you just wrote.'),
]
V2_JSON_REGEX = [(r"the learner.s source,", 'your source,')]  # curly-apostrophe site


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


def apply_json(vol, heading_subs, sub_subs, regex_subs):
    path = f'{V}/docs/assets/volume{vol}.json'
    d = json.load(open(path))
    touched = set()
    applied = 0

    def sub(s, lesson_id):
        nonlocal applied
        for old, new in sub_subs:
            if old in s:
                assert s.count(old) == 1
                s = s.replace(old, new)
                touched.add(lesson_id)
                applied += 1
        for pat, new in regex_subs:
            s2, n = re.subn(pat, new, s)
            if n:
                assert n == 1
                s = s2
                touched.add(lesson_id)
                applied += 1
        return s

    for l in d['lessons']:
        for k in ('title', 'summary', 'takeaway'):
            if k in l and isinstance(l[k], str):
                l[k] = sub(l[k], l['id'])
        blocks = l['blocks']

        def walk(bl):
            for b in bl:
                t = b.get('text')
                if isinstance(t, str):
                    for old, new in heading_subs:
                        if t == old:
                            b['text'] = new
                            touched.add(l['id'])
                            nonlocal applied
                            applied += 1
                            break
                    else:
                        b['text'] = sub(t, l['id'])
                if 'items' in b:
                    b['items'] = [sub(it, l['id']) if isinstance(it, str) else it for it in b['items']]
                if 'blocks' in b:
                    walk(b['blocks'])
        walk(blocks)

    # sanity: nothing left behind
    def all_text():
        for l in d['lessons']:
            yield l['title']
            for k in ('summary', 'takeaway'):
                if isinstance(l.get(k), str):
                    yield l[k]

            def w(bl):
                for b in bl:
                    if isinstance(b.get('text'), str):
                        yield b['text']
                    if 'items' in b:
                        for it in b['items']:
                            if isinstance(it, str):
                                yield it
                    if 'blocks' in b:
                        yield from w(b['blocks'])
            yield from w(l['blocks'])

    left = [t for t in all_text() if 'Study-session walkthrough' in t]
    assert not left, f'v{vol}: leftover walkthrough headings: {left}'
    left2 = [t[:80] for t in all_text() if re.search(r'Observed [a-z]+:', t) or 'Environment issue encountered' in t]
    assert not left2, f'v{vol}: leftover Observed/env markers: {left2}'
    left3 = [t[:80] for t in all_text() if re.search(r'\bthe learner\b', t, re.I)]
    assert not left3, f'v{vol}: leftover "the learner": {left3}'
    if vol == 2:
        left4 = [t[:80] for t in all_text() if 'first draft' in t]
        assert not left4, f'v2: leftover first draft: {left4}'

    for l in d['lessons']:
        if l['id'] in touched:
            old_w = l['words']
            l['words'] = sum(count_block(b) for b in l['blocks'])
            print(f"  v{vol} lesson {l['id']}: words {old_w} -> {l['words']}")
    rt = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
    open(path, 'w').write(rt)
    again = open(path).read()
    d2 = json.loads(again)
    ok = json.dumps(d2, indent=2, ensure_ascii=False) + '\n' == again
    print(f'v{vol}.json: applied={applied} touched={sorted(touched)} round-trip={ok}')
    assert ok

apply_json(1, V1_J_HEADINGS, V1_JSON_SUBS, [])
apply_json(2, V2_J_HEADINGS, V2_JSON_SUBS, V2_JSON_REGEX)
print('done')
