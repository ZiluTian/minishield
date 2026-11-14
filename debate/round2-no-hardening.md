# Round 2 — cross-reaction (persona: compiler/LLVM dev, no security background)

## 0. Framing — why my endorsements are short

Both other personas list security as home turf. A: "Security-hardening knowledge is **not** my gap… Volume 3 is fine to skim." B: "Working familiarity with security hardening… This is **not** my gap, so Volume 3 reads close to home" — and B logs "No learning-friction entries from this volume." I am the only one who read v3 slowly and hit walls. So their corroboration concentrates in v1/v2 signposting and the LLVM object model, which is *my* home turf, and my v3 security findings stand alone. I endorse only what genuinely crosses into my experience and say where it doesn't.

## 1. Endorsements

- **A-1 (numbering crosswalk)** — hits my G8 directly: line 813's "Lessons 83–85" cites web day-numbers, not volume lesson numbers; I reconstructed the same mapping A flagged (G1, G14). Three personas, one opacity. A crosswalk covering v3 + glossary unblocks my v3 cross-refs too.
- **A-9 (signpost the 2.5→2.6 contract)** — I needed exactly this to even start interpreting G8: "the reference is canonical, your working tree is not updated" is the prerequisite for *asking* why the printed v3 artifact differs from my build. (But see pushback 2 — the contract as stated is incomplete for v3.)

Honest note: A-4 and B-1…B-6 target the compiler/IR gap, which is my home turf; I endorse their *diagnosis* as correct for their profile, but they don't fill a gap of mine. B-1's content is endorsed in C-12, not here.

## 2. Pushbacks

**PB-1 — B-1's placement (v1 Background) is wrong; the content is right.** B-1 wants the C→IR mapping "in Volume 1 Background… ≈ line 55." Two problems from the v3 reader's seat. (a) It addresses the wrong wall for the security-naive reader: in v3 I stalled on the *security* meaning of the IR (what `type.test` checks, why `-flto`) and on the missing C demo sources (my C-2, C-4) — not on C→IR syntax, which I read fluently. A C→IR primer, however good, is not where the v3 reader's wall is. (b) The Background section (v1 lines 13–237) is the book's setup/orientation — it's where 1.5.5 "a framework for hardening" lives, the level-map I cited in round 1 as the setup I needed. Injecting a multi-function compilation tutorial there dilutes the threat/setup framing the whole project hangs on. Move B-1 to where IR is first *used* (1.4.2, first traversal) or first *needed* (2.7.2) — by then the reader has a working plugin and a `.ll` file to point at, so the mapping has a concrete referent. B-1 already offers "and/or 1.4.2"; make 1.4.2 primary and drop the Background placement.

**PB-2 — A-9's "reference is canonical" is incomplete; it doesn't handle reference drift.** A-9 tells the reader "from 2.6 the reference is canonical, your tree is not updated — trust the reference." Right for v2, where the reference *implementation* is complete code to re-derive. But my G8 shows it breaks for v3: the *printed artifacts* (3.4.4's `persist_final.ll`, 3.6.1's negative-control diff) were cut from an older builder state than the working tree — the current `lib/StateMachineBuilder.cpp` has an entry-CondBr case (lines 60–72) the printed listing doesn't reflect. I rebuilt the plugin and replayed the exact 3.4.4 command: the entry *is* rewired (`ms.dispatch` gets `preds = %1`); the printed listing shows the entry branch intact + `; No predecessors!`. A reader who follows A-9's "trust the reference" trusts a stale reference. The contract needs a version-pinning clause: state which builder/plugin state each printed artifact assumes. That's my C-1; A-9 and C-1 are one change (C-11).

**PB-3 — B-6 conflicts with A-5 and is subsumed by it.** B-6 says keep the "Study-session walkthrough" block and relabel the third repetition as "Recorded mistake / gotcha." A-5 says rewrite the session frame out entirely, per SKILL.md, which bans learner-progress logs ("the learner," "Observed bug:", "the first draft"). They conflict: B-6 preserves the frame SKILL.md says to remove. A-5 already does the relabeling B-6 wants — "'Observed bug:' → 'Common mistake:' with the wrong code labeled" — while stripping the session narration. So B-6 is a weaker, partial version of A-5; merge into A-5 and drop B-6. The gotcha *content* (common errors, wrong code) is worth keeping; the session *frame* is not.

## 3. New proposals

**C-11. One "reference-canonicity + version-pinning" signpost (merge A-9 + C-1).**
- *Location*: the 2.5→2.6 boundary (before 2.6.1, L3945) and the top of each v3 replay lesson (3.4.4, 3.6.1).
- *Gap*: A-G11; my G8/G11.
- *Change*: at the boundary, one paragraph: "The contract changes here. 2.2–2.5 were build-along; from 2.6 each lesson ships a complete reference — re-derive it, your tree is not updated." Then, because the reference can *drift*, add at each v3 replay a one-line "this artifact was produced with builder state X (entry UncondBr / entry CondBr / non-entry terminators, yes-no); check yours with `grep -c 'br label %ms.dispatch'`."
- *Effort*: M.
- *Why*: A's contract signpost and my artifact reconciliation are the same question — "which code state produced this artifact?" — answered half. This answers it whole, for v2 (contract) and v3 (drift).

**C-12. Make "C beside IR + one-line mapping" a book-wide convention, applied to v3's security demos (merge B-1 + C-4 + C-2).**
- *Location*: v3's "Proof at runtime" sections (3.2.1, 3.2.2, 3.3.1), using B-1's v1/v2 examples as the pattern.
- *Gap*: B-G-1/G-7; my G4/G6; my C-2.
- *Change*: the book's best anchor — a C function beside its IR with a one-line mapping — exists in v2 (2.7.2's `discount.c`) but is absent from v3's hardening demos. Apply it there: show `cfi_pipe.c` (21L), `vcall_pipe.cpp` (20L), `canary_pipe.c` (38L) beside their hardened IR with the *security* mapping ("this `type.test` guard checks the vtable pointer against Base's set"; "this canary slot is at −8(%rbp), the return address at +8(%rbp)"). The canary source makes the 24+4×8 payload arithmetic self-evident.
- *Effort*: M.
- *Why*: one convention serves all three — B gets the C→IR anchor carried into v3, I get the missing v3 C sources *and* the security meaning of the IR, A gets the fixture continuity they value.

**C-13. Consolidate A-4 + B-4 + B-5 into one front-loaded "LLVM object & manager model" page.**
- *Location*: before the first traversal (1.4.2, L1338).
- *Gap*: A-G10; B-G-5, B-G-6 — two personas stuck at the same structural spot.
- *Change*: one page with a nesting figure (Module → Function → BasicBlock → Instruction, B-5) + the manager graph (who creates whom: PassBuilder → Module/FunctionPassManager → `pass::run(F, AM)` → `PreservedAnalyses`, A-4) + one sentence for the why ("analyses are cached; `PreservedAnalyses` declares what your pass invalidated," B-4). Three scattered S/M fixes become one M artifact.
- *Effort*: M.
- *Why*: A and B both stalled on the object/manager model (A: "the one place I had to leave the book for external LLVM docs"; B guessed the `PreservedAnalyses` reason right). One consolidated page closes it for both. (My profile skips it as home turf — noted honestly.)

## 4. Joint top 3

1. **A-1 — numbering crosswalk.** Pure signposting, helps all three (A's G1/G14, my G8 line 813), unblocks every cross-reference including the glossary, cheap. Clear joint #1.
2. **C-12 — C↔IR convention through v3.** The book's core anchor (C beside IR + one-line mapping) made consistent across all three volumes; helps B (C→IR), me (v3 C sources + security meaning), A (fixture continuity).
3. **C-11 — reference-canonicity + version-pinning.** Resolves "which code state produced this artifact" — a structural trust fix for me (v3 replay) and A (v2 contract).

Honorable mention: **C-13** is the single biggest *content* win for the two compiler-naive profiles — A's #1 and B's #3–4 — even though my profile skips it as home turf; it's still the right thing to add.
