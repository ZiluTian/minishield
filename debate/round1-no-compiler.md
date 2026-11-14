# MiniShield — Round 1 report (reader: no compiler background)

## 1. Reader profile

- 7 years of C/C++ and some Rust; Linux systems and application development.
- Reads C easily; reads assembly with effort. Build-tooling, CMake/Ninja, `dlopen`, and
  the C++ LLVM API are home turf — low friction there.
- Working familiarity with security hardening (canaries, ASLR, RELRO, obfuscation, CFI).
  This is **not** my gap, so Volume 3 reads close to home.
- **Never studied a compiler.** No IR, no SSA, no basic block, no CFG, no LLVM IR ever
  seen, no clear idea what a "pass" or `verify` concretely does. To me the compiler is a
  black box that turns C into something I cannot read.
- Net: the compiler/IR content in Volumes 1–2 is exactly the gap to probe; the
  C++/build-tool and security content is background I already have.

## 2. Reading route

- **Volume 1 (3,875 lines): read in full**, including the unnumbered *Background* section
  (lines 13–237). 1.2.x CMake skimmed fast (home turf); 1.3.x plugin, 1.4.x stats pass,
  1.5.x CFG analysis + eligibility, 1.6.x "crash course," and 1.7.x C++/LLVM concepts +
  glossary read closely.
- **Volume 2 (11,483 lines): lesson-by-lesson.** Every conceptual section, every
  checkpoint, and every before/after IR listing read in full; C++ implementation skimmed
  after the first pattern. Covered 2.1.1, 2.2.1–2.2.3 (PHI collect/demote), 2.3.x,
  2.4.x (escaping-value demotion/trace), 2.5.x (state assignment, dispatcher), 2.6.x
  (orchestration), 2.7.2 (C→IR bridge + behavioral diff), 2.8.1 (evidence), 2.10.1
  (reproducible seed), 2.11.x (timing), 2.12.x (reporting), 2.13.x (glossary).
- **Volume 3 (1,942 lines): skimmed at heading + checkpoint level.** Security is not my
  gap; the structure reads well and the checkpoints are crisp. No learning-friction
  entries from this volume.

## 3. Gap log

Format: location | what the book assumed | what was missing | how I recovered.

- **G-1 (largest).** Volume 1 *Background* (lines 42–66) and the fixtures throughout;
  first C→IR mapping only at Volume 2 line 6212 (2.7.2). The book assumes you already
  know what a C function *looks like* in IR. The fixtures (`phi.ll`, `loop.ll`,
  `if-else.ll`) are introduced as "handwritten text IR" (line 65) with no C source
  beside them. Missing: the single most load-bearing anchor — "my C `for` loop becomes
  `header`/`body`/`exit` blocks with a back-edge PHI." Recovered by backfilling from
  2.7.2 (line 6212, `clang -O0 … -emit-llvm tests/cases/discount.c`) and 2.2.1
  (lines 251–258, C if/else → PHI). I would have burned real time searching "how does a
  C for loop look in LLVM IR."

- **G-2.** Volume 1 *Background* lines 61–64. SSA is defined as "define once, use
  later." Missing: the payoff — "C lets you reassign a variable; SSA does not, so two
  paths that each write a variable must merge through a PHI." That only lands in 2.2.1.
  Recovered by waiting for the first demotion lesson.

- **G-3.** `verify` appears throughout (Background line 192; "Valid vs. correct"
  lines 207–219). The book assumes you can predict what `verify` catches. Missing: a
  single concrete `verify` **failure** — every example passes silently. I never see a
  use-before-def or a missing terminator with the real error string. Recovered by
  inference from the "valid vs. correct" prose.

- **G-4.** Every lesson in Volume 2 (and many in Volume 1). The pacing assumes you need
  the Task restated three times. Each lesson repeats the Task/Checkpoint in (a) the
  lesson body, (b) the "Study-session walkthrough" block, and (c) the "Model answer."
  For a strong reader that is 3× the scaffolding, and the third occurrence — which is
  really the lesson's "recorded mistake" — is unlabeled as such. Recovered by
  pattern-matching; I only recognized the "Study-session walkthrough" block as the
  mistake/gotcha part after several lessons.

- **G-5.** 1.3.1 (first `PreservedAnalyses`, lines 893–901). The type is introduced as
  bookkeeping without stating why it exists. Missing: the "why" — analyses are cached
  because recomputing them is expensive, so each pass must declare what it invalidated.
  Recovered by guessing (and it is right: it is cache invalidation).

- **G-6.** 1.6.x "crash course" (1.6.1, line 2789) vs. first traversal 1.4.2 (line
  1338). The ordering assumes you can traverse `Function`/`BasicBlock` before the object
  model is explained. The first traversal (1.4.2) iterates
  `for (const BasicBlock &BB : F) for (const Instruction &I : BB)` and relies on the
  `Module → Function → BasicBlock → Instruction` nesting that is only tabulated in
  1.6.1. A no-compiler reader expects the crash course to come first. Recovered by
  reading forward to 1.6.1, then back.

- **G-7.** 2.7.2 (line 6212). The reader is assumed comfortable switching between
  named-block fixtures and numeric-label IR. The C→IR output uses numeric labels
  (`9:`, `%3`, `%0`) while the fixtures use named blocks (`entry:`, `%value`). The
  switch is jarring; I briefly thought the discount function's IR were a different kind
  of IR. Recovered by the "Reading this LLVM program from zero" table (which does cover
  numeric names) — but only once I got to it.

## 4. Improvement proposals

(Only changes that help *this* profile. No depth removed; depth is a feature.)

- **B-1 — "Where does this IR come from?" (Effort: M).**
  Location: Volume 1 *Background*, right after "What is LLVM IR?" (≈ line 55), and/or
  1.4.2 before the first traversal. Addresses: G-1, G-7.
  Change: add a short subsection showing two or three tiny C functions (if/else, a
  `for` loop, a `switch`) each beside its `clang -O0 -S -emit-llvm` output, with a
  one-line C→IR mapping per case: the `for` loop → `header`/`body`/`exit` blocks plus a
  back-edge PHI; the if/else → two paths merged by a PHI at `join`; the `switch` → a
  `switch` terminator with one case edge each. Note explicitly that clang emits numeric
  labels (`9:`, `%3`) while the book's fixtures use named blocks, and that they are the
  same IR. Cross-reference the 2.7.2 discount example so it is no longer the first time
  the reader sees C in IR.
  Why it helps: this is my biggest gap. A no-compiler reader cannot read the fixtures
  until they have seen their own C re-expressed as blocks and PHIs.

- **B-3 — SSA payoff up front (Effort: S).**
  Location: Volume 1 *Background* lines 61–64 (the SSA definition). Addresses: G-2.
  Change: one paragraph contrasting a mutable C variable with SSA. Sketch: "In C,
  `x = 1; x = 2;` reassigns one variable. In SSA every assignment is a *new* value —
  `%x.1`, then `%x.2` — so when two control-flow paths each assign a variable and then
  merge, there is no single variable to hold both results; the merge block defines one
  value *chosen by the edge taken*, and that is exactly what a PHI node does."
  Why it helps: SSA's whole reason for existing is currently delivered 20+ lessons late.

- **B-2 — One concrete `verify` failure (Effort: S).**
  Location: Volume 1 *Background* "Valid vs. correct" (lines 207–219). Addresses: G-3.
  Change: add one deliberately broken IR snippet — a value used before it is defined, or
  a block with no terminator — and show the real `opt`/`verify` error string, i.e. that
  `verify` fails *loudly*, not silently. Keep it to a single example.
  Why it helps: it lets me predict what "structural rules" concretely catch instead of
  trusting the prose description of them.

- **B-5 — Front-load the nesting table; label the crash course (Effort: M).**
  Location: Volume 1, before the first traversal (1.4.2, line 1338) and at the open of
  1.6.x (1.6.1, line 2789). Addresses: G-6.
  Change: (a) a four-line `Module → Function → BasicBlock → Instruction` nesting
  reminder immediately before the first traversal in 1.4.2; (b) a one-liner at the open
  of 1.6.x stating that the crash course *consolidates* what the reader has already
  used and is not a prerequisite they were missing.
  Why it helps: a no-compiler reader needs the object map before the first traversal, and
  needs to know the crash course is consolidation, not a missing foundation.

- **B-4 — Why `PreservedAnalyses` exists (Effort: S).**
  Location: 1.3.1 (first mention, lines 893–901). Addresses: G-5.
  Change: one sentence: "Analyses are cached because recomputing them is expensive, so
  each pass returns a `PreservedAnalyses` declaring which analyses its change invalidated
  (`::all()` for none, `::none()` for everything)."
  Why it helps: it turns an opaque bookkeeping return type into a motivated decision.

- **B-6 — Label the "Study-session walkthrough" block (Effort: S, lower priority).**
  Location: all such blocks in Volumes 1–2. Addresses: G-4.
  Change: relabel (or annotate) the third Task/Checkpoint occurrence — the "Study-session
  walkthrough" block — as "Recorded mistake / gotcha:" so a strong reader recognizes the
  third repetition as the lesson's mistake-logging part rather than redundant
  scaffolding.
  Why it helps: reduces perceived redundancy for a strong reader without removing the
  depth a weaker reader still needs.

## 5. Top 5 (ranked)

1. **B-1** — "Where does this IR come from?" (C→IR mapping, numeric vs named labels).
2. **B-3** — SSA payoff up front.
3. **B-2** — One concrete `verify` failure.
4. **B-5** — Front-load the nesting table; label the crash course.
5. **B-4** — Why `PreservedAnalyses` exists.

(B-6 is a worthwhile bonus.)

## 6. My ideal edition

It opens with a two-page "your C, in LLVM's words" that compiles three tiny C functions
(if/else, a `for` loop, a `switch`) and walks their `-O0` IR — numeric labels and all —
side by side with the source. It states SSA as "every assignment is a new value, so
merges need PHIs" the first time the term appears, not twenty lessons later. It shows one
real `verify` failure with the actual error string, so "structural rules" stop being
abstract. It hands the `Module → Function → BasicBlock → Instruction` nesting table
before the first traversal and flags the crash course as consolidation rather than a
missing prerequisite. After that scaffolding it does exactly what the current book
already does well: a small task per lesson, complete before/after IR, a "Reading this
LLVM program from zero" table, a concrete execution trace, a "Check your understanding"
multiple-choice self-check, and a hand-counted fixture expectation — with the C++ kept at
the native level a strong systems developer already brings.
