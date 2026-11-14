# E21 prep: session-voice inventory (read-only scan, 2026-11-14)

Targets per the E21 spec: throughout `volume1` and `volume2`, plus the three
volume headers. The content inside is good and must stay; only the frame changes.

## 1. "Study-session walkthrough" headings — 49 total (18 in v1, 31 in v2, 0 in v3)

These are the blocks that become first-class "Common mistake / gotcha:" sections
(relabel + de-narrate the body). The em-dash subtitle after the marker is the
gotcha's topic and should be kept.

volume1 (18):
- L221 separate the program being compiled from the pass doing the work
- L328 activation selects tools; the manifest describes their installation
- L744 give headers, linked symbols, and output paths different jobs
- L847 build.ninja comes from configuration, not from the build command
- L929 a header declaration, implementation, and plugin entry point are not interchangeable
- L1013 required changes skipping behavior, not scheduling
- L1159 turn a user-facing pipeline string into a pass object
- L1217 a balanced pipeline is checked before the pass runs
- L1315 finish a small interface before solving its behavior
- L1367 the function manager already chose the function
- L1479 diagnose runtime registration separately from compile-time visibility
- L1558 switch classification still needs the installed opcode names
- L1773 write an expectation before trusting a report
- L1911 a readable test runner is still a program with syntax
- L1960 prove that reading did not secretly edit the program
- L2078 one branch instruction can represent two graph edges
- L2292 return graph facts instead of making later passes parse text
- L2485 fill one record completely, then append it

volume2 (31):
- L105 make one representation change at a time
- L342 collect a worklist before calling a mutating helper
- L517 the push_back mismatch is about the static pointer type
- L730 demotion replaces a choice, not merely a line of text
- L1003 a PHI-free graph can still carry values between blocks
- L1222 void describes a result, not whether an operation matters
- L1386 an allocation produces an address, not its stored integer
- L1572 a filter does not append, and an empty first stage is not the end
- L1748 the argument type tells you whether to pass the pointer or the object
- L1942 demote the collected result, then track the actual edit
- L2192 trace one number through an ordinary spill
- L2416 trace a choice through PHI demotion
- L2660 give a next-block decision an integer encoding
- L2869 object, address, and key/value pair are separate C++ ideas
- L3119 construct valid machinery before making it live
- L3375 the C++ handle is not the IR label
- L3600 initialize the state before the first dispatcher read
- L3985 operation, result, and storage are different
- L4006 why an allocation must dominate its uses
- L4035 build the result-type guard
- L4070 an intrinsic is a special operation expressed as a call
- L4098 musttail is a requirement, not a hint
- L4123 inspect inline-assembly calls through CallBase
- L4168 a convergent call has participation constraints
- L4214 an operand bundle is part of call semantics
- L4262 returns_twice can resume one continuation again
- L4312 naked changes the function's low-level entry/exit contract
- L4563 declare the builder interface first
- L4660 define the first implementation body
- L4890 turn the entry branch into a runtime state choice
- L5225 keep the original default while lowering cases

## 2. "the learner" mentions (case-insensitive) — v1: 4, v2: 4, v3: 10

volume1:
- L6 (header): "The learner writes the C++ and test scripts. … records the mistakes encountered along the way."
- L1516: "The learner preferred switch/case. Use switch (I.getOpcode()) with these"
- L1950: "An empty diff is expected and was reported by the learner."
- L2384: "The next small step is lib/CFGAnalyzer.cpp. The learner should write it."

volume2:
- L8 (header): "The learner writes the implementation and scripts."
- L11 (header): "they do not change the learner's source files."
- L3776: "… compiled separately from the learner's source, passed verify on the 10 existing fixtures …"
- L6967: "… not a claim that the learner implementation has reached it."

volume3 (out of the E21 target scope v1+v2, but logged): 10 mentions, mostly
"the learner's own build flags" / "the learner's flattening pass" style —
these read as "your build" and are lower priority; header L8 is in scope.

## 3. "Observed error/bug/omission/correction" markers — v1: 10, v2: 5

volume1:
- L809 "Observed error: Ninja could not find build.ninja…"
- L813 "Observed result: 'ninja: no work to do' means…"
- L923 "Observed mistakes: the header was initially named FlatteningPass.cpp…"
- L1214 "Observed error: function(minishield-flatten)] had an extra closing bracket."
- L1470 "Observed error: 'unknown function pass minishield-stats'…"
- L1474 "Observed error: 'no member named StatsPass in namespace minishield'…"
- L1532 "Observed correction: an earlier teaching example used Instruction::Br…"
- L1536 "Observed bug: a missing break after a branch case would also increment…"
- L1540 "Observed omission: switches was counted but initially absent…"
- L1899 "Observed error: Bash reported 'unexpected end of file'…"

volume2:
- L552 "Observed error: phis.push_back(&I) fails because the vector needs PHINode*…"
- L796 "Observed error: Do not delete PHIs while using an ordinary loop…"
- L1560 "Observed error: The reviewed draft created escapingValues …"
- L2905 "Observed error: const auto *BB would be a pointer to const BasicBlock…"
- L3411 "Observed error: The build failed before producing a new plugin…"

Rewrite rule: "Observed X:" → "Common mistake:" (or "Common pitfall:" where the
text warns rather than recounts), with the wrong code/behavior still labeled
as the mistake and the correct one explained.

## 4. "first draft" mentions — v2: 2

- L2654: "The next lesson revisits the pointer and pair-construction errors found in the first draft."
- L3337: "Task: Review the BasicBlock creation statements and the empty invalid block found in the first draft."

Rewrite rule: → labeled before/after without the session frame, e.g. "the
earlier version of this code" / "the first attempt".

## 5. Volume header session voice (all three volumes)

- volume1 L2: "Recorded from the study sessions on 2026-11-11 and 2026-11-12"
- volume1 L6: "The learner writes the C++ and test scripts. Each lesson gives a small task,
  explains the concept, shows a check, and records the mistakes encountered along the way."
- volume2 L2: "Study notes and future exercises · expanded 2026-11-13"
- volume2 L8–12: "The learner writes the implementation and scripts. … they do not change
  the learner's source files. …"
- volume3 L2: "Study notes and future exercises · expanded 2026-11-13"
- volume3 L8–12: same L8 framing as volume2.

Note: the headers are also E18's territory (the front-matter "How to read this
volume" page replaces/absorbs them) — if E18 lands first, E21 only has to clean
the leftover session voice, not restructure.

## 6. Scope summary

| Element | Count | Where |
| --- | --- | --- |
| Study-session walkthrough headings | 49 | v1 ×18, v2 ×31 |
| "the learner" (in-scope v1/v2) | 8 | v1 ×4, v2 ×4 |
| "Observed " markers | 15 | v1 ×10, v2 ×5 |
| "first draft" | 2 | v2 |
| header session voice | 3 volumes | v1 L2/L6, v2 L2/L8, v3 L2/L8 |

Every one of these maps to a lesson in the JSON (`sessionWalkthrough: true`
blocks in v1/v2 JSON — 90 paragraph blocks + 18 with a `language` field, plus
the `answers`-carrying walkthroughs), so the JSON side of E21 is a mechanical
mirror of the same relabel/rewrite on those blocks.
