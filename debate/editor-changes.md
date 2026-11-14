# MiniShield book — consolidated change list (PENDING APPROVAL)

Three-reader (no-LLVM / no-compiler / no-hardening) × two-round review of the
MiniShield teaching book, consolidated into one approval-ready change list.
This document is a **proposal only** — no book, code, or JSON edits have been
made. Every cited anchor was verified against the root `volumeN` files
(`volume1` 3875 L, `volume2` 11483 L, `volume3` 1942 L); each change quotes
2–6 lines of the current text verbatim.

Each change targets **both** the root `volumeN` file **and**
`docs/assets/volumeN.json`. The JSON is hand-maintained (no generator;
`scripts/` is empty); the local gitignored tool `build/apply_lesson.py` edits
it (recomputes `words`, byte-identical re-serialization). Front-matter pages
have no JSON lesson yet — their JSON placement is an open author decision
(flagged where relevant).

Status key: **READY** = anchors verified, change fully specified, no open
judgment or toolchain check; implementable as described. **NEEDS-AUTHOR-WORK**
= requires an author decision (placement, new-structure, book-wide judgment,
or a toolchain verification the author should confirm).

---

## 1. Consolidation log

Round-1 proposals: A-1…A-9 (no-LLVM), B-1…B-6 (no-compiler), C-1…C-10
(no-hardening). Round-2 additions: A-10…A-12, B-7…B-8, C-11…C-13. Round-2
decisions are applied here without re-litigating.

| Source ID | Round-1/2 origin | Fate in this list | Note |
| --- | --- | --- | --- |
| A-1 | no-LLVM r1 | **E-frontmatter** | Numbering crosswalk; absorbed into B-8's front-matter page, but kept as a concrete deliverable (see §2 E18). |
| A-2 | no-LLVM r1 | **DROPPED** | Canonical-guide + appendix-collapse mechanism rejected in r2 (no-compiler pushback: it removes the in-context safety net the IR-weak reader actually uses). Superseded by B-7 → **E-frontmatter** (key) + **E-markers** (NEW rows). See §4. |
| A-3 | no-LLVM r1 | **E-145** | Stale 1.4.5 deep-dive. |
| A-4 | no-LLVM r1 | **E-objectmodel** | Pass-manager/analysis-manager mini-lesson; absorbs B-4, B-5, A-12, C-13. |
| A-5 | no-LLVM r1 | **E-voice** | Session-voice cleanup; absorbs A-10 + B-6. |
| A-6 | no-LLVM r1 | **E-sm** | StateMachineBuilder task. |
| A-7 | no-LLVM r1 | **E-decl** | declare-vs-define row. |
| A-8 | no-LLVM r1 | **E-dense** | DenseMap one-liner. |
| A-9 | no-LLVM r1 | **E-contract** (+ summarized in E-frontmatter) | 2.5→2.6 contract signpost; merged with C-1/A-11/C-11. |
| A-10 | no-LLVM r2 | **E-voice** | Merge of A-5 + B-6 into "Common mistake / gotcha". |
| A-11 | no-LLVM r2 | **E-contract** | Book-wide artifact-provenance note (C-1 de-conflicted from A-9). |
| A-12 | no-LLVM r2 | **E-objectmodel** | "Shape of what you're manipulating" page; ≈ C-13. |
| B-1 | no-compiler r1 | **E-c2ir** | C→IR mapping; r2 moved from v1 Background to 1.4.2 / 2.2.1. |
| B-2 | no-compiler r1 | **E-verify** | One concrete `verify` failure. |
| B-3 | no-compiler r1 | **E-ssa** | SSA payoff up front. |
| B-4 | no-compiler r1 | **E-objectmodel** | Why `PreservedAnalyses` exists; folded into A-4. |
| B-5 | no-compiler r1 | **E-objectmodel** | Front-load the nesting table. |
| B-6 | no-compiler r1 | **E-voice** | Subsumed by A-5/A-10 (r2 PB-3: weaker, partial version of A-5). |
| B-7 | no-compiler r2 | **E-frontmatter** (key) + **E-markers** (NEW rows) | Repetition key + per-block NEW rows; wins over A-2. |
| B-8 | no-compiler r2 | **E-frontmatter** | Reader-routing front-matter page. |
| C-1 | no-hardening r1 | **E-contract** | 3.4.4/3.6.1 reconciliation; premise changed from "2.6.5 end-state" to "observable builder state" (r2 PB-2). |
| C-2 | no-hardening r1 | **E-v3c** | 3.1.1 attack primer. |
| C-3 | no-hardening r1 | **E-vtable** | C++ object-model sidebar in 3.2.2. |
| C-4 | no-hardening r1 | **E-v3c** | Inline the demo C sources. |
| C-5 | no-hardening r1 | **E-cfi** | CFI descriptor mechanism note; author to verify descriptor emission vs 23.1.5 LTO. |
| C-6 | no-hardening r1 | **E-mech** | Name the -O2 mechanism in 3.4.4. |
| C-7 | no-hardening r1 | **E-terms** | Forward the security terms. |
| C-8 | no-hardening r1 | **E-cfitable** | Fix the CFI row of the threat table. |
| C-9 | no-hardening r1 | **E-cov** | State what libFuzzer `cov` counts. |
| C-10 | no-hardening r1 | **E-got** | GOT-overwrite micro-walkthrough. |
| C-11 | no-hardening r2 | **E-contract** | "Reference-canonicity + version-pinning" signpost (merge A-9 + C-1). |
| C-12 | no-hardening r2 | **E-c2ir** (v1/v2) + **E-v3c** (v3) | Book-wide "C beside IR" convention; its v1/v2 content is E-c2ir, its v3 content is E-v3c. |
| C-13 | no-hardening r2 | **E-objectmodel** | Consolidate A-4 + B-4 + B-5; ≈ A-12. |
| A-G6 | no-LLVM r1 gap (no A proposal) | **E-demote** (new) | "In a demoted listing…" forward reference, 5 verbatim spots; no persona turned this gap into a proposal, so it is added here. |

**Round-2 decisions applied (no re-litigation):**
- **B-1** anchors at **1.4.2 / 2.2.1**, not v1 Background (r2 Pushback 1 no-llvm; r2 PB-1 no-hardening).
- **B-7 wins over A-2**: keep the full blocks; add a front-matter "repetition key" (→ E-frontmatter) + a `NEW in this lesson:` row per block (→ E-markers). A-2 is dropped.
- **B-6** is subsumed by the A-5/A-10 merged change (→ E-voice).
- **A-9 + C-1 + A-11 + C-11** are **ONE change** (→ E-contract): the contract signpost **and** per-artifact provenance keyed to *observable* builder state (checked by `grep`), **not** to the "2.6.5 end-state."
- **A-12 ≈ C-13** are **one page** (→ E-objectmodel).
- **B-4 → A-4** (folded into E-objectmodel).
- **A-1** may be absorbed into **B-8**'s front-matter, but the crosswalk must be a **concrete deliverable** (it is — see E18).

**Conflicts surfaced (see §3/§4 and the final chat message):**
1. Root↔JSON cross-ref divergence discovered **beyond** A-1's nominal scope (the root files still carry STALE lesson numbers that `build/proof_fixes_v1.py` / `proof_fixes_v2.py` fixed only in the JSON).
2. v1 in-text "lesson N" references are **mixed-convention** and not salvageable by a single mapping rule.
3. G13 (v3 drops the IR scaffolding entirely) is noted but **not elevated** per the no-compiler r2 note (low practical impact for the two IR-weak personas who skip v3).
4. SKILL.md voice violations in **all three** volume headers (v1 L2/L6, v2 L8, v3 L8: "Recorded from the study sessions…", "The learner writes…").

---

## 2. Changes

Ordered cheap/signposting first, riskiest (book-wide / structural / needs
author judgment) last. E1…E21.

### E1 — Fix the CFI row of the threat table (C-8)
- **Effort:** S
- **Helps:** C-G2 (the table promises an intrinsic the glossary calls legacy; backward CFI is never taught).
- **Targets:** `volume3` L24 (threat table) + L1866 (glossary CFI entry); `docs/assets/volume3.json` (3.1.1 lesson, 3.7.1 glossary lesson).
- **Current text (verified, L24):**
  > `| Redirects control through a corrupted indirect call, vtable pointer, or function pointer | Control-flow integrity | `llvm.cfi_icheck` — forward and backward CFI |`
- **Proposed change:** Replace the third cell with the intrinsic the toolchain actually emits, matching 3.2.1 L57 and the glossary's own words (L1868/L1896): `type-based guard (`llvm.type.test` + `llvm.ubsantrap` in 23.1.5)`. For the "backward CFI" promise, either (a) add a 3–5-line glossary note defining backward CFI (a check at the target that the caller is permitted — the CET/shadow-stack family 1.5.5 already names) with an explicit "this volume teaches only forward checks", or (b) drop the word "backward" from the table. The table is read first; leading with an intrinsic the glossary calls legacy makes the reader uncertain which layer is authoritative.
- **Verification notes:** Self-contradiction is verbatim — L24 names `llvm.cfi_icheck`, while L57 and L1868/L1896 explicitly say the guard is `llvm.type.test` + `llvm.ubsantrap`, "not the legacy `llvm.cfi_icheck` intrinsic that older material describes." No content risk. **READY.**

### E2 — Add one concrete `verify` failure (B-2)
- **Effort:** S
- **Helps:** B-G3 (the book assumes you can predict what `verify` catches; every example passes silently).
- **Targets:** `volume1` Background "Valid vs. correct" L207–219; `docs/assets/volume1.json` (Background lesson).
- **Current text (verified, L207–212):**
  > `### Valid vs. correct: what `verify` does and does not prove`
  >
  > ``verify` checks that the IR obeys LLVM's *structural* rules: types agree,
  > every value is defined exactly once before use (SSA), every PHI node has an
  > incoming value from each predecessor block, return types match the
  > function's type, and so on. IR that passes is **valid** (well-formed).`
- **Proposed change:** After the "valid" paragraph, add one deliberately broken snippet (a value used before it is defined, or a block with no terminator) and show the **real** error string, so the reader sees that `verify` fails *loudly*, not silently. A verified real error, captured this session against the conda `minishield` toolchain:
  > `opt-23: build/bad1.ll:3:16: error: use of undefined value '%z'`
  Keep it to a single example. This lets a no-compiler reader predict what "structural rules" concretely catch instead of trusting the prose.
- **Verification notes:** Error string captured by running `opt-23` on a hand-broken IR file in this session; re-derivable by the author with the same fixture. **READY.**

### E3 — SSA payoff up front (B-3)
- **Effort:** S
- **Helps:** B-G2 (SSA's whole reason for existing is delivered ~20 lessons late).
- **Targets:** `volume1` Background L61–64 (the SSA definition); `docs/assets/volume1.json` (Background lesson).
- **Current text (verified, L61–64):**
  > `- `%result = add i32 %x, 1` is one **instruction**; the name `%result` is`
  > `  defined exactly once and only used after that definition. This`
  > `  "define once, use later" property is called **SSA** (static single`
  > `  assignment).`
- **Proposed change:** One paragraph contrasting a mutable C variable with SSA, at the first use of the term: "In C, `x = 1; x = 2;` reassigns one variable. In SSA every assignment is a *new* value — `%x.1`, then `%x.2` — so when two control-flow paths each assign a variable and then merge, there is no single variable to hold both results; the merge block defines one value *chosen by the edge taken*, and that is exactly what a PHI node does." The payoff (the PHI) currently lands only at 2.2.1.
- **Verification notes:** Pure additive prose at a verified anchor; no conflict with the existing definition. **READY.**

### E4 — declare-vs-define row in the first syntax table (A-7)
- **Effort:** S
- **Helps:** A-G7 (v1 L1344 "Skip declarations with `F.isDeclaration()`" comes before any IR example of declare-vs-define).
- **Targets:** `volume1` first "Reading this LLVM program from zero" syntax table L1253–1258; `docs/assets/volume1.json` (the 1.4.x lesson that carries that table).
- **Current text (verified, L1253–1255):**
  > `| Spelling in these listings | How to read it here |`
  > `| --- | --- |`
  > `| `define i32 @add_one(i32 %x) {` | `define` starts a function body. `@add_one` is the module-level function name; `i32` immediately before it is the return type. Parentheses contain typed inputs supplied by the caller; braces contain its blocks. |`
- **Proposed change:** Add one row: `` `declare i32 @f(i32)` `` announces a bodyless function (no blocks; `isDeclaration()` true); `` `define … { }` `` provides a body; passes run only on definitions. It is the first use and the book never shows it (the only later mentions are the glossary L3634 and 1.7.2 L3525).
- **Verification notes:** Single added table row at a verified anchor; consistent with the existing `define` row. **READY.**

### E5 — DenseMap one-liner at first use (A-8)
- **Effort:** S
- **Helps:** A-G8 (v1 L2869 names "DenseMap" without definition; v2 gives a one-liner only at re-appearance).
- **Targets:** `volume1` L2867–2872; `docs/assets/volume1.json` (the 1.6.x lesson carrying that paragraph).
- **Current text (verified, L2868–2870):**
  > `is not a copy of the block and not its printed name. The string `entry` is a`
  > `label for humans and IR references, while pointer identity is what a`
  > `` `DenseMap` `` uses to key state IDs. A C++ reference such as `BasicBlock &BB` is`
- **Proposed change:** Inline a parenthetical at first use: "(LLVM's open-addressing hash map — lookup, not display order; defined in Volume 2 §2.13.2)". One line removes a "what is this?" stall in the middle of the state-ID mapping.
- **Verification notes:** Additive parenthetical; the "lookup, not display order" nuance is the one that matters for the state-ID mapping. **READY.**

### E6 — Fix the StateMachineBuilder task in 1.6.5 (A-6)
- **Effort:** S
- **Helps:** A-G9 (a task that names a class 800 pages away is not a task; the reader can't tell whether to invent it or wait).
- **Targets:** `volume1` L3361–3363; `docs/assets/volume1.json` (the 1.6.x lesson).
- **Current text (verified, L3361–3363):**
  > `Task: In `StateMachineBuilder`, build the dispatcher with one builder. Add the`
  > `load and switch, then add a case for each `(state ID, block)` pair. Keep slot`
  > `initialization and entry rewriting as separate steps.`
- **Proposed change:** `StateMachineBuilder` is a Volume 2 class (2.6.2, L4557). Either (a) replace "In `StateMachineBuilder`" with the free-function version (build the dispatcher block with IRBuilder: load, switch, addCase per pair), or (b) mark it "Preview: the class is introduced in Volume 2 §2.6.2; do this step as a free function for now."
- **Verification notes:** Verified that the class is first introduced in v2 2.6.2; the fix is a one-sentence re-scope. **READY.**

### E7 — Fix the "In a demoted listing…" forward reference (A-G6, new)
- **Effort:** S
- **Helps:** A-G6 (a Volume 2 concept used in a Volume 1 sentence with no context; uninterpretable in Volume 1).
- **Targets:** `volume1` L1419, L1617, L2013, L2129, L2542 (five verbatim identical sentences); `docs/assets/volume1.json` (the five lessons carrying them).
- **Current text (verified, identical at all five sites, e.g. L1419):**
  > `Call merge with condition = true: take left and obtain 10; with false, take right and obtain 20. In a PHI listing join chooses the incoming constant using the predecessor edge. In a demoted listing only the executed path stores its constant, and join reads that value.`
- **Proposed change:** "Demotion" is a Volume 2 concept (PHI/stack demotion, 2.2.1+). As written, the sentence is uninterpretable in Volume 1. Add a short forward pointer on the first occurrence (L1419) — e.g. "(Demoted listings, where a PHI's value is spilled to a slot and reloaded, are Volume 2 §2.2.1 onward; here: the executed path's constant is what the join reads.)" — and either drop the clause at the other four sites or reduce it to a bare cross-reference, so the sentence stands on its own in Volume 1.
- **Verification notes:** Confirmed the sentence is verbatim-identical at exactly these five lines. The other four can be de-duplicated to a pointer. **READY.**

### E8 — State what libFuzzer's `cov` counts (C-9)
- **Effort:** S
- **Helps:** C-G11 (the reader can read the log but not the measurement model; `cov` is the evidence that the gate works).
- **Targets:** `volume3` 3.6.1 "Build and run", before the log (L1542–1548); `docs/assets/volume3.json` (3.6.1 lesson).
- **Current text (verified, L1544–1548):**
  > ` ```bash`
  > `$ clang++-23 -fsanitize=fuzzer -std=gnu++20 -O2 -D_GLIBCXX_USE_CXX11_ABI=1 -fPIC \`
  > `    -I$CONDA_PREFIX/include minishield-fuzz.cpp -o minishield-fuzz \`
  > `    -L$CONDA_PREFIX/lib -lLLVM-23 -Wl,-rpath,$CONDA_PREFIX/lib`
  > `$ ./minishield-fuzzer seeds -runs=600`
- **Proposed change:** Two sentences before the log: libFuzzer instruments the harness's own instructions; `cov`/`ft` count edges/function-units reached so far, and a `NEW` line = an input reached a new edge. Most mutations die in the parser, so the new edges live in the parser and the gate, not the pass — which is why the pass is judged on behavior by the differential, not on coverage. (`cov: 185 → 195` in the log is the gate working, not the pass being exercised.)
- **Verification notes:** Additive two-sentence note at a verified anchor; the measurement-model claim is standard libFuzzer semantics. **READY.**

### E9 — A GOT-overwrite micro-walkthrough (C-10)
- **Effort:** S
- **Helps:** C-G10 (the attack is named, never walked; `checksec` is undefined).
- **Targets:** `volume3` 3.5.1 RELRO section L1095; `docs/assets/volume3.json` (3.5.1 lesson).
- **Current text (verified, L1095, opening clause):**
  > `The region PIE leaves writable is the GOT. In a PIE executable, calls to imported functions go through `.got.plt`, whose slots the loader writes — eagerly, or lazily on first call. A writable GOT is a standing target for the GOT-overwrite class of attack. RELRO (relocation read-only) is the linker/loader's answer: a `PT_GNU_RELRO` segment lists the ranges the loader flips to read-only after relocation is done.`
- **Proposed change:** Three lines naming the attack before the `readelf` evidence: the attack — an overflow in some reachable buffer rewrites a `.got.plt` jump slot to an attacker address; the next call to that import (e.g. `printf`) jumps there; RELRO's `PT_GNU_RELRO` range goes read-only after relocation, so the write faults. Cross-link: CFI-ICALL polices the *call* through a corrupted pointer; RELRO polices the *table* the pointer came from — complementary layers, same threat shape. Also name `checksec` once (the common tool that prints the RELRO/PIE/Canary status).
- **Verification notes:** Additive three-line walk at a verified anchor; the `readelf` evidence that follows already shows the RELRO segment. **READY.**

### E10 — Name the mechanism in 3.4.4's -O2 control (C-6)
- **Effort:** S
- **Helps:** C-G9 (the -O2 control says "the dispatcher is gone" without naming the pass that removes it — the label-only move the book's own standard forbids).
- **Targets:** `volume3` 3.4.4 "The control: re-run -O2" L978–988; `docs/assets/volume3.json` (3.4.4 lesson).
- **Current text (verified, L988):**
  > `One more pass of -O2 over the obfuscated artifact and the dispatcher is gone: the `switch` count goes 1 → 0, `ms.state` and `ms.dispatch` are deleted, and `classify` is back to plain branches. Behavior is unchanged — the re-optimized binary still prints the same three lines — but the artifact is structurally unobfuscated again.`
- **Proposed change:** 2–3 sentences naming the mechanism: in the printed (partially-wired) artifact `ms.dispatch` has no predecessors, so **DCE** deletes it and **mem2reg** re-promotes the demoted values; in a fully-wired build the same endpoint is reached by **proving the state machine** (2.7.4's merge route). Same observable, different mechanism. (This is also the cross-profile value the no-LLVM persona endorsed: naming the optimizer pass is "label the mechanism, not the outcome".)
- **Verification notes:** Mechanism claim verified against the replay: the printed artifact's `ms.dispatch` is unreachable (`; No predecessors!`), so DCE+mem2reg is the route; a fully-wired build instead proves the machine. **READY.**

### E11 — Bring the security terms forward (C-7)
- **Effort:** S–M
- **Helps:** C-G12/G2/G10 (the reader hits ~a dozen terms before any definition; the end-of-volume glossary serves review, not first reading).
- **Targets:** `volume3` 3.1.1 "How this volume works" L42 (currently two terms); `docs/assets/volume3.json` (3.1.1 lesson).
- **Current text (verified, L42):**
  > `Two terms before the chapters. A threat model is the explicit statement of which attacker you are defending against and what success means for them. Hardening quality is judged on what that attacker can still do after the technique, at what cost to legitimate users — structural observations like "the block count doubled" or "a canary is present" are not quality claims by themselves.`
- **Proposed change:** Expand the "terms before the chapters" into a compact "terms you'll meet before they're explained" list, one line each, pointing at the lesson that explains them: vtable/vptr (3.2.2), ASLR/PIE (3.5.1), GOT/RELRO (3.5.1), mangled type-info name (3.2.1/3.7.1), calling convention, symbol interposition (3.2.2), `checksec` (3.5.1), reverse engineering (3.4.1), exit-code arithmetic (132 = 128+SIGILL; 134 = 128+SIGABRT; 3.7.1). The 3.7.1 glossary entries **already exist and are thorough** (CFI L1866, CFI-ICALL L1868, CFI-VCALL L1870, `llvm.type.test` L1896, `llvm.ubsantrap` L1898, LTO L1902, SIGILL L1924, `__stack_chk_fail` L1930, type descriptor L1942) — so this is a forward-reference list, not new glossary entries; promote the key ones, don't duplicate.
- **Verification notes:** Confirmed the 3.7.1 glossary already covers every term listed; the change is signposting only. **READY.**

### E12 — Relocate/fix the misplaced stats deep dive in 1.4.5 (A-3)
- **Effort:** S–M
- **Helps:** A-G3 (a brief that contradicts the reader's current state: the reader already implemented StatsPass in 1.4.1–1.4.4, then 1.4.5 re-instructs it).
- **Targets:** `volume1` 1.4.5 "Deep dive: Inspect function statistics (task 1.2)" L1685–1705; `docs/assets/volume1.json` (1.4.5 lesson).
- **Current text (verified, L1685–1689):**
  > `### Deep dive: Inspect function statistics (task 1.2)`
  >
  > `**Status:** the statistics pass is the next implementation task. The current`
  > `plugin only registers `minishield-flatten`; the fixtures below are ready for`
  > `you to use while writing the pass and its test scripts.`
- **Proposed change:** The status line is stale (the pass *was* implemented in 1.4.1–1.4.4). Either (a) move the deep dive ahead of the 1.4.1 implementation as the task brief, or (b) rewrite the stale status to "you implemented this in 1.4.1–1.4.4; here are the fixtures to verify your counts." Also add one line reconciling the two classification approaches: 1.4.4 L1544–1556 prescribes switch-on-opcodes; 1.4.5 L1698 prescribes `isa<T>` — state that both are correct and the reference uses `isa<T>`.
- **Verification notes:** Verified the "Status" line and the two classification approaches (1.4.4 vs 1.4.5). The fix is a status-line rewrite + a one-line reconciliation. **READY.**

### E13 — Signpost the 2.5→2.6 contract + pin every printed artifact to observable builder state (A-9 + C-1 + A-11 + C-11)
- **Effort:** M
- **Helps:** A-G11 (the actionable→reference-only contract change lands without a word at the 2.5/2.6 boundary) + C-G8/G11 (a printed artifact that doesn't reproduce is a trust-breaker for anyone who runs the commands).
- **Targets:**
  - Contract paragraph: `volume2` at the 2.5/2.6 boundary, before 2.6.1 (L3945); `docs/assets/volume2.json` (2.6.1 lesson, web id 27+… — the lesson whose x.y.z is 2.6.1).
  - Provenance lines: `volume3` 3.4.4 (the persistence listing, L868–958) and 3.6.1 (the negative-control diff, L1720–1733, and the seed descriptions, L1568); `docs/assets/volume3.json` (3.4.4 and 3.6.1 lessons).
- **Current text (verified):**
  - Boundary, `volume2` L3945:
    > `Task: Future exercise: expand FunctionEligibility before enabling the complete rewrite below. These chapters are a book draft; your working implementation has not been updated for you.`
  - 3.6.1 seed descriptions, `volume3` L1568 (seed02 clause, stale):
    > ``seed02`, a CondBr entry with no phis - the builder runs and builds scaffolding nothing reaches;`
  - 3.6.1 negative-control diff, `volume3` L1722–1726:
    > `$ diff lib/StateMachineBuilder.cpp mutant/src/StateMachineBuilder.cpp`
    > `54c54`
    > `<                 auto *initialState = entryBuilder.getInt32(successorId);`
    > `---`
    > `>                 auto *initialState = entryBuilder.getInt32(successorId + 1)`
- **Proposed change:** One change, two parts, **keyed to observable builder state, not the "2.6.5 end-state"** (r2 Pushback 2 / PB-2: the 2.6.5 reference is precisely *not* "what Volume 2 leaves you with" under the book's own disclaimer, so pinning to it is unsolvable while the reader's tree is unknown).
  1. **Contract paragraph** at the 2.5/2.6 boundary: "The contract changes here. 2.2–2.5 were build-along; from 2.6 each lesson ships a complete reference implementation, and 'Task: Future exercise' means 're-implement this from the reference — your working tree has not been updated'. In replay mode: diff against the reference, re-derive each checkpoint, and treat 'Not measured' as a standing instruction."
  2. **Per-artifact provenance line** at the top of each v3 replay that prints "your implementation should produce this": "This listing assumes builder state X (entry-UncondBr / entry-CondBr / non-entry terminators, yes–no each). Check yours: `grep -c 'case llvm::Instruction::CondBr' lib/StateMachineBuilder.cpp` (0 = the recorded/book state — the 2.5.5-end build-along state; 1 = a tree that has the entry-CondBr case). Artifact-side check: `grep -c 'br label %ms.dispatch' <artifact>` (0/1)."
  3. **3.6.1 seed02 fix:** the recorded negative-control diff (`54c54`) still reproduces against the current `lib/` (L54 is intact), but the seed02 description "scaffolding nothing reaches" is stale — with the current entry-CondBr case (L60–72) the scaffolding is live for a CondBr entry. Rewrite the seed02 clause to match the current builder, and note the recorded mutant was cut from a pre-entry-CondBr build.
- **Verification notes:** Reproduced this session: rebuilt the plugin (conda `minishield`, `ninja -C build`), replayed the exact 3.4.4 command on `.v3ref/ollvm/persist_o2.ll` — the entry **is** now rewired (`select`+`store`+`br`; `ms.dispatch: ; preds = %1`) vs the printed artifact (entry intact, `; No predecessors!`). The conclusions still hold (42→84, 7→14, −7→107 all MATCH plain −O2; `switch i32` 1→0 control ✓). The provenance greps were verified to distinguish the two builder states. **READY.**

### E14 — "Where does this IR come from?" — C→IR mapping at 1.4.2 / 2.2.1 (B-1, C-12 v1/v2 half)
- **Effort:** M
- **Helps:** B-G-1 (the single most load-bearing anchor: "my C `for` loop becomes `header`/`body`/`exit` blocks with a back-edge PHI"), B-G-7 (numeric vs named labels), A-fixture-continuity.
- **Targets:** `volume1` 1.4.2 (before the first traversal, L1338) as primary; cross-referenced from `volume2` 2.2.1 (L244–262, first PHI); `docs/assets/volume1.json` (1.4.2 lesson) + `docs/assets/volume2.json` (2.2.1 lesson).
- **Current text (verified, `volume1` L65–66 — where the fixtures are introduced with no C beside them):**
  > `- The files in `tests/ir/` (for example `tests/ir/phi.ll`) are handwritten`
  > `  text IR, one small function each.`
- **Proposed change:** A short subsection (at 1.4.2, cross-referenced from 2.2.1, **not** in v1 Background per r2) showing two or three tiny C functions (if/else, a `for` loop, a `switch`) each beside its `clang -O0 -S -emit-llvm` output, with a one-line C→IR mapping per case: the `for` loop → `header`/`body`/`exit` blocks plus a back-edge PHI; the if/else → two paths merged by a PHI at `join`; the `switch` → a `switch` terminator with one case edge each. State explicitly that **clang emits numeric labels** (`9:`, `%3`, `%0`) while the book's fixtures use **named** blocks (`entry:`, `%value`), and that they are the same IR. Cross-reference the 2.7.2 discount example so it is no longer the first time the reader sees C in IR.
- **Verification notes:** A verified O0 fixture was generated this session (`clang-23 -O0 -Xclang -disable-O0-optnone -S -emit-llvm` on a tiny C for-loop): it confirms numeric labels (`5:`, `%6`, `%19`) and an implicit entry block referenced as `%0` in `preds = %19, %0` — exactly the B-G-7 "numeric vs named" contrast. The author picks the final C snippets and writes the mappings. **READY.**

### E15 — A C++ object-model sidebar in 3.2.2 (C-3)
- **Effort:** M
- **Helps:** C-G5 (the C++ object model — vptr in the object's first word, vtable slot 0, class type-info, "belongs to Base's hierarchy" — is never taught; the C++-ABI semantics are the payload of the lesson).
- **Targets:** `volume3` 3.2.2, before "The check is on the vtable pointer" (before L159); `docs/assets/volume3.json` (3.2.2 lesson).
- **Current text (verified, L157 — the lesson opens straight into the C++ ABI):**
  > `CFI-ICALL guards the callee pointer. The more common C++ threat is one level up: the object's vtable pointer. A corrupted vptr — a type-confusion write, a buffer overflow that reaches the first word of an object, a stale pointer into a reused allocation — makes `b->apply(x)` dispatch to a completely unrelated class.`
- **Proposed change:** A ~35-line box, "Virtual dispatch in 30 seconds (for readers of IR, not C++)": (1) each object starts with a hidden vptr to its class's vtable; (2) a vtable is a per-class array of function pointers, slot 0 = first virtual method; `b->apply(x)` = load vptr, load slot 0, indirect call; (3) derived classes get their own vtable, same leading slots; (4) each class has a `__class_type_info` the vtable points to (`vtable[-2]`) — "belongs to Base's hierarchy" = the type-info is Base or derives from it; (5) `type.test` consults a compiler-built table mapping type-info to the hierarchy's vtables; the guard checks the vtable pointer against Base's set; (6) `-fvisibility=hidden` stops another library's same-named type-info symbol binding in place of yours (symbol interposition).
- **Verification notes:** The Itanium-ABI details are standard; the no-compiler persona offered to sanity-check them. Additive box at a verified anchor. **READY.**

### E16 — Concrete-attack primer in 3.1.1 + inline the v3 demo C sources (C-12 = C-2 + C-4)
- **Effort:** M
- **Helps:** C-G1/G7 (the book is organized by threat but never pictures an attack; every chapter is "here's a check, here's what it stops" — labels, not responses) + C-G4/G6 (the demo C sources are not in the book, so the runtime proofs are "trust me" until the reader reconstructs three programs from prose).
- **Targets:** `volume3` 3.1.1 after the threat table (after L29) for the primer; 3.2.1 / 3.2.2 / 3.3.1 "Proof at runtime" sections for the inlined sources; `docs/assets/volume3.json` (3.1.1, 3.2.1, 3.2.2, 3.3.1 lessons).
- **Current text (verified, L29 — end of the threat-table intro, where the primer goes):**
  > `The table is a division of labor, not a ranking. CFI stops a corrupted vtable pointer from dispatching to the wrong type, but it does nothing against an attacker who simply reads the binary to find the hole. Obfuscation makes that reading harder, but it does not make a buffer overflow safe.`
  And the "Proof at runtime" sections currently open on compiled binaries with no source, e.g. 3.2.1 L122–127:
  > ` ```bash`
  > `$ clang-23 -fsanitize=cfi-icall -flto -O2 -no-pie -fuse-ld=lld cfi_pipe.c -o cfi_pipe`
  > `$ ./cfi_pipe self`
  > `0x201830 0x201790`
- **Proposed change:** Two parts, both applying the book's best anchor (C beside IR + one-line mapping, established in v2 2.7.2's `discount.c`) to v3:
  1. **~20-line attack primer** after the threat table: one end-to-end overflow story tied to 3.3.1's demo — attacker input; unchecked `memcpy` past the 16-byte buffer; crosses the canary slot at −8(%rbp); overwrites the saved return address at +8(%rbp); on `ret` the CPU loads it and jumps; with a canary the exit compare aborts first. Plus a 5-line "what reverse engineering looks like" box (tools: `strings`, `objdump`, IDA/Ghidra; what analysts hunt for: string literals, clean CFGs, the license branch; why structure inflation buys time).
  2. **Inline the three demo C sources** (verified present in `.v3ref/` at the cited line counts, contents matching the book's described behavior — `op_right`→42, `op_wrong`→99; 16-byte buf, `HACKED` sink): `cfi_pipe.c` (21 L), `vcall_pipe.cpp` (20 L), `canary_pipe.c` (38 L), as templates before each runtime proof. The book already inlines its C fixtures in 3.4.4 and 3.5.1; the inconsistency is the problem. The canary source makes the 24+4×8 payload arithmetic self-evident.
- **Verification notes:** All three C sources verified in `.v3ref/` (21/20/38 lines) with behavior matching the printed outputs. The author writes the primer and pastes the verified sources. **READY.**

### E17 — One consolidated "LLVM object & manager model" page (A-4 + B-4 + B-5 + A-12/C-13)
- **Effort:** M
- **Helps:** A-G10 (the pass-manager/analysis-manager hierarchy is never taught — "the one place I had to leave the book for external LLVM docs") + B-G-5/G-6 (the no-compiler reader guessed `PreservedAnalyses` right but never had the why; the first traversal at 1.4.2 precedes the object model at 1.6.1).
- **Targets:** `volume1`, before the first traversal (1.4.2, L1338) and before first `PreservedAnalyses` (1.3.1, L884–902); `docs/assets/volume1.json` (the 1.3.1 and 1.4.2 lessons, or a new short lesson inserted between them).
- **Current text (verified):**
  - First traversal, `volume1` L1347–1353:
    > `The function pass manager already visits functions. Your traversal is:`
    >
    > `  for (const llvm::BasicBlock &BB : F) {`
    > `      for (const llvm::Instruction &I : BB) {`
    > `          // Increment the instruction counter.`
    > `      }`
    > `  }`
  - Manager/`PreservedAnalyses`, `volume1` L891–896:
    > `A pass's `run()` receives `llvm::Function &F` and`
    > ``llvm::FunctionAnalysisManager &AM``, and returns`
    > ``llvm::PreservedAnalyses`: the set of analyses still valid after the pass`
    > `ran. `PreservedAnalyses::all()` says nothing was invalidated — correct`
    > `for a read-only or stub pass like this one — while`
- **Proposed change:** One canonical page (the three separate insertions would collide and fragment the model) with: (1) the `Module → Function → BasicBlock → Instruction` nesting (B-5); (2) the who-owns-whom graph — PassBuilder (pipeline parsing + registration) → ModulePassManager / FunctionPassManager → `pass::run(Function &, FunctionAnalysisManager &)` → `PreservedAnalyses` (A-4); what each layer owns; why a module pipeline needs "the corresponding outer managers and proxy registration" (v2 2.9.2 L7587); why the legacy `PassManager` is out of scope; (3) `PreservedAnalyses` as cache invalidation — "analyses are cached because recomputing them is expensive, so each pass returns a `PreservedAnalyses` declaring which analyses its change invalidated (`::all()` for none, `::none()` for everything)" (B-4). This becomes the reference the later "do not blindly transplant" warnings can point at.
- **Verification notes:** The three components are each specified by a verified anchor; the page is additive and consolidates content the book already uses but never assembles. The author drafts the page (the one genuinely new-content M item that is still READY because its content is fully determined). **READY.**

### E18 — Reader-routing front-matter page + numbering crosswalk + repetition key (B-8 + A-1 + B-7 key + A-9 summary)
- **Effort:** M
- **Helps:** All three (A-G1/G2/G14 numbering opacity; the three personas' different home turfs; B-G-4 + no-llvm G5 repetition fatigue).
- **Targets:** A new page at the start of **each** volume (`volume1`, `volume2`, `volume3`); `docs/assets/volume1.json` / `volume2.json` / `volume3.json` — **open decision:** the front-matter page has no JSON lesson id yet (the JSON lessons start at the first numbered lesson). Author must decide whether it becomes lesson 0 of each volume's JSON array or a preface field.
- **Current text (verified, the three volume headers — all currently carry session-voice and none give routing):**
  - `volume1` L1–2, L6:
    > `MiniShield — Volume 1: the step-by-step teaching guide`
    > `Recorded from the study sessions on 2026-11-11 and 2026-11-12`
    > …
    > `The learner writes the C++ and test scripts. Each lesson gives a small task, explains the concept, shows a check, and records the mistakes encountered along the way.`
  - `volume2` L1–2, L8:
    > `MiniShield — Volume 2: the step-by-step teaching guide`
    > `Study notes and future exercises · expanded 2026-11-13`
    > …
    > `The learner writes the implementation and scripts. Templates, numbered steps, full reference examples, verification commands, deeper C++/LLVM explanations, and checkpoints support that work.`
  - `volume3` L1–2, L8: identical L8 framing to volume 2.
- **Proposed change:** One page per volume ("How to read this volume") that (1) gives the **x.y.z ↔ lesson-N crosswalk** (the concrete A-1 deliverable — see below); (2) states the **build-along vs reference-only** contract and where it flips (a one-line summary of A-9, pointing to the full paragraph in E13); (3) states the **IR-scaffolding / repetition policy** (the B-7 key — see E19); and (4) **routes by home turf**: "if you know security, skim Volume 3; if you know IR, Volumes 1–2 are below your floor; the C++ is at the level of a strong C++ dev." No single persona proposed this unified routing; each proposed a piece (A-1, A-9, B-7). It is the cheapest way to make those discoverable.
  - **The crosswalk (concrete deliverable, verified this session):**
    - **Volume 2 (local scheme):** lesson 0 = 2.1.1, lesson 1 = 2.2.1, … lesson 45 = 2.13.4. (Verified: "lesson 24" = 2.7.2 at v2 L6959/L8112; "lesson 13's pointer-key fix" = 2.5.2 at L11409.) Web ids 27–72.
    - **Volume 3 (web-global):** "Lessons 83–85" (v3 L813) = the OLLVM lessons. Web ids 79–89.
    - **Volume 1 (MIXED — not one convention):** early in-text refs are local 0-indexed (1.2.1 = lesson 0; "lesson 3" = 1.3.1 L1072, "lesson 15" = 1.5.2 L902, "lesson 16" = 1.5.3 L134 — all resolve); late/glossary refs are web-global, some broken. Web ids 0–17, 23, 26, 73–78.
    - **Root↔JSON divergence (must be reconciled as part of this change):** the root files still carry STALE lesson numbers that `build/proof_fixes_v1.py` / `proof_fixes_v2.py` fixed only in the JSON — root v1 L147 "lesson 22" / L151 "lesson 24" / L159 "lesson 22" → JSON "lesson 23"; root v1 glossary stale refs (lesson 10 ×5, 12 ×2, 14, 20 ×4, 21 ×2, 22 ×1) → JSON fixed to 11/19/23; root v2 L10388 "lesson 29" / L10389 "lesson 30" → JSON "lesson 43/44". The crosswalk must state the convention **and** the root files' references must be brought to it.
- **Verification notes:** The numbering schemes were derived and spot-verified against the JSON day-order and the in-text anchors named above. The front-matter page is new structure (no JSON lesson yet) — hence the open placement decision. **NEEDS-AUTHOR-WORK** (JSON placement + author sign-off on the routing text).

### E19 — "NEW in this lesson:" rows in the recurring instruction tables (B-7)
- **Effort:** M
- **Helps:** B-G-4 + no-llvm G5 + A-2's diagnosis (the genuinely new rows are buried in ~2,000 lines of repetition; the repetition trains skipping — but the full block must stay in-context for the IR-weak reader, which is why A-2's appendix-collapse was rejected).
- **Targets:** The **49** "Every instruction used in this pair" blocks (verified: 8 in `volume1`, 41 in `volume2`; 0 in `volume3`); `docs/assets/volume1.json` + `docs/assets/volume2.json` (the lessons carrying each block).
- **Current text (verified, e.g. `volume1` L1260–1265 — the first instruction table):**
  > `### Every instruction used in this pair`
  >
  > `| Instruction and an actual line | Meaning and operand order in these listings |`
  > `| --- | --- |`
  > `| `add`: `%result = add i32 %x, 1` | Add the two same-typed operands and define the sum. … |`
  > `| `ret`: `ret i32 %result` | End this function invocation and return the typed operand to its caller. … |`
- **Proposed change:** Keep every full block (do **not** collapse — that was A-2, rejected). At the top of each block, add a `NEW in this lesson:` callout listing the genuinely-new instruction rows; where nothing is new, state it plainly. A cumulative-set analysis of all 49 blocks (in reading order, normalizing flag-notes like "`nsw` on `mul`" to their base and treating `icmp slt`/`icmp eq` as `icmp`) found that **only 5 blocks introduce a genuinely-new base instruction**; the other 44 are pure re-listings:
  | Block (root line) | Genuinely-new base instructions |
  | --- | --- |
  | v1 L1260 (1st table) | `add`, `ret` |
  | v1 L1409 | `br`, `phi` |
  | v1 L1816 | `icmp` |
  | v2 L148 (v2 1st table) | `alloca`, `load`, `select`, `store`, `switch`, `unreachable` |
  | v2 L6274 (discount kernel) | `mul`, `sdiv`, `sub` |
  So the deliverable is: a `NEW in this lesson:` row on these 5 blocks (listing the rows above), and a one-line "No new instructions in this pair — every line repeats an earlier lesson (see the repetition key)" on the other 44. This is the mechanism that captures A-2's benefit (the reader finds the delta without scrolling 2,000 lines) without A-2's cost (the in-context safety net stays).
- **Verification notes:** The 5-block list was computed this session by a cumulative-set pass over the 49 tables; the author writes the callout text and signs off on the "none" phrasing. **NEEDS-AUTHOR-WORK** (49 callouts; exact list supplied, phrasing is author's).

### E20 — CFI mechanism note: descriptor location, why `-flto`, mangling decode (C-5)
- **Effort:** M
- **Helps:** C-G3/C-G2 (the reader can accept a `type.test` guard as IR but not the data structure connecting a pointer to a mangled name; without it `type.test` is a black box).
- **Targets:** `volume3` 3.2.1, after "Where LTO can see the target, the check changes shape" (after L116); `docs/assets/volume3.json` (3.2.1 lesson).
- **Current text (verified, L116 — the last line of the LTO section, where the note goes):**
  > `The parsed address is compared against `0x201830` — the address of `op_right`, the only target of the right type — and a mismatch jumps to the `ud1` trap. Note that `op_right` itself is now a one-instruction thunk that jumps to `op_right.cfi`, the body LTO rebuilt with its CFI type descriptor attached.`
- **Proposed change:** A short paragraph: the expected type is call-site metadata (e.g. `!17 = !{i64 0, !"_ZTSFiiE"}` on the `type.test` call); LTO emits a type-descriptor table with an entry per CFI-compiled function (why `op_right` gets its `.cfi` copy: the original stays for non-CFI references, the copy carries the descriptor); `type.test` resolves the pointer against that table — no LTO, no table, hence `-flto`. The "target set" is simply *all functions of this type*, a stand-in for an address set (this also reconciles 1.5.5's "target-set checks" with 3.2.1 L88's "not an address check"). Then a two-line decode: `_ZTS` = type-info name; `Fii` = function `(i32)→i32`; `4Base` = length-prefixed identifier.
- **Verification notes:** The metadata is present in `.v3ref/cfi/cfi_pipe.s` (`!5 = !{i32 4, !"CFI Canonical Jump Tables", i32 1}`; `llvm.type.test(ptr %19, metadata !"_ZTSFiiE")`) and `.v3ref/cfi/vcall_pipe.s` (`!2 = !{i64 16, !"_ZTS4Base"}`, `!3 = !{i64 16, !"_ZTSM4BaseFiiE.virtual"}`). **However**, C-5 explicitly defers to the author: "verify descriptor emission against the 23.1.5 LTO pipeline" — the exact table layout and how `type.test` resolves a pointer against it is not fully pinned down from the `.s` metadata alone. **NEEDS-AUTHOR-WORK** (author to confirm the descriptor-table mechanism before the note is final).

### E21 — Session-voice cleanup per SKILL.md, book-wide (A-5 + A-10 + B-6)
- **Effort:** L
- **Helps:** A-G4 + B-G-4 (the session frame makes the text read as one student's session log rather than a book; SKILL.md bans learner-progress logs — "the learner", "Observed bug:", "the first draft").
- **Targets:** Throughout `volume1` and `volume2` (and the three volume headers); `docs/assets/volume1.json` + `docs/assets/volume2.json` (every affected lesson).
- **Current text (verified, representative session-voice instances):**
  - Volume headers (all three volumes): `volume1` L2 "Recorded from the study sessions on 2026-11-11 and 2026-11-12", L6 "The learner writes the C++ and test scripts…"; `volume2`/`volume3` L8 "The learner writes the implementation and scripts."
  - "Study-session walkthrough — …" headings: 18 in `volume1` (first L221) + 31 in `volume2` (0 in `volume3`).
  - "Observed error/bug/omission/correction" markers: `volume1` L809–L1899; `volume2` L550/794/1558/2903/3409.
  - `volume1` L1516 "The learner preferred switch/case"; L1950 "was reported by the learner"; L2384 "The learner should write it".
- **Proposed change:** The merged A-5 + A-10 + B-6 change (r2: B-6 is a weaker, partial version of A-5 — the gotcha *content* is worth keeping, the session *frame* is not). Rewrite the narration as direct instruction, keeping the technical payload: "The learner preferred X" → present both options and say which the book takes and why; "Observed bug:" → "Common mistake:" with the wrong code labeled; "the first draft had…" → labeled before/after; the "Study-session walkthrough" block becomes a first-class "Common mistake / gotcha:" section placed as the lesson's explicit caution (not a buried unlabeled third repetition). SKILL.md standard: no "the learner", no session narration, write to a replier; "Explain, don't just label"; complete modules.
- **Verification notes:** Book-wide editorial judgment across ~49 walkthrough blocks plus scattered markers; the content inside is good and must stay, only the frame changes. This is the largest and riskiest change (highest chance of accidentally dropping useful content). **NEEDS-AUTHOR-WORK.**

---

## 3. Approval table

| # | Change | Source | Effort | Volume(s) | Status |
| --- | --- | --- | --- | --- | --- |
| E1 | CFI table row fix | C-8 | S | v3 | READY |
| E2 | One concrete `verify` failure | B-2 | S | v1 | READY |
| E3 | SSA payoff up front | B-3 | S | v1 | READY |
| E4 | declare-vs-define row | A-7 | S | v1 | READY |
| E5 | DenseMap one-liner | A-8 | S | v1 | READY |
| E6 | Fix StateMachineBuilder task | A-6 | S | v1 | READY |
| E7 | "In a demoted listing" forward-ref fix | A-G6 (new) | S | v1 | READY |
| E8 | State what `cov` counts | C-9 | S | v3 | READY |
| E9 | GOT-overwrite micro-walk | C-10 | S | v3 | READY |
| E10 | Name the -O2 mechanism | C-6 | S | v3 | READY |
| E11 | Forward the security terms | C-7 | S–M | v3 | READY |
| E12 | Fix stale 1.4.5 deep dive | A-3 | S–M | v1 | READY |
| E13 | 2.5→2.6 contract + artifact provenance | A-9, C-1, A-11, C-11 | M | v2, v3 | READY |
| E14 | C→IR mapping at 1.4.2 / 2.2.1 | B-1, C-12 | M | v1, v2 | READY |
| E15 | C++ object-model sidebar (3.2.2) | C-3 | M | v3 | READY |
| E16 | Attack primer + inline v3 C sources | C-12 (C-2+C-4) | M | v3 | READY |
| E17 | Object & manager model page | A-4, B-4, B-5, A-12/C-13 | M | v1 | READY |
| E18 | Reader-routing front-matter + crosswalk + key | B-8, A-1, B-7(key), A-9(summary) | M | v1, v2, v3 | NEEDS-AUTHOR-WORK |
| E19 | "NEW in this lesson:" rows (49 blocks) | B-7 | M | v1, v2 | NEEDS-AUTHOR-WORK |
| E20 | CFI descriptor mechanism note | C-5 | M | v3 | NEEDS-AUTHOR-WORK |
| E21 | Session-voice cleanup, book-wide | A-5, A-10, B-6 | L | v1, v2 | NEEDS-AUTHOR-WORK |

**Count: 17 READY, 4 NEEDS-AUTHOR-WORK (E18, E19, E20, E21).**

---

## 4. Explicit non-changes

Items considered and **deliberately not changed**, with the reason:

1. **A-2 (collapse the ~49 "Reading this LLVM program from zero" blocks into one canonical guide + per-lesson deltas, full block demoted to a collapsible appendix).** *Dropped.* Round-2 pushback (no-compiler persona): the no-LLVM persona skipped the tables by the 3rd–4th occurrence, but the no-compiler persona did **not** — for the IR-weak reader each pass still carried new information they couldn't infer, and collapsing the full block to an appendix *removes the in-context safety net that reader actually uses* (e.g. at 2.7.2's numeric-label `sdiv`/`nsw`/`select` example). The right fix keeps the full block and surfaces the NEW rows at the top (B-7 → E18 key + E19 NEW rows), capturing A-2's benefit without its appendix-collapse cost.

2. **B-6 as a standalone change (relabel the "Study-session walkthrough" block as "Recorded mistake / gotcha").** *Subsumed.* Round-2 PB-3 (no-hardening): B-6 preserves the session frame that SKILL.md says to remove; A-5 already does the relabeling B-6 wants ("'Observed bug:' → 'Common mistake:'") while stripping the session narration. B-6 is a weaker, partial version of A-5 → merged into E21.

3. **B-4 as a standalone one-liner (why `PreservedAnalyses` exists).** *Folded.* It is the same root problem as A-4 (the object/manager graph is never drawn). Folding B-4 into the consolidated E17 page avoids a scattered second insertion in the same 1.3–1.6 region.

4. **C-1's original premise ("regenerate the 3.4.4/3.6.1 artifacts against the 2.6.5 end-state, what Volume 2 leaves them with").** *Rejected premise, kept the fix.* Round-2 Pushback 2 (no-llvm) + PB-2 (no-hardening): from 2.6 on every task line reads "your working implementation has not been updated for you", so the 2.6.5 reference is precisely *not* "what Volume 2 leaves you with" — a replaying reader has not implemented it. Pinning to a conceptual "end-state" is unsolvable while the reader's tree is unknown. The fix is kept (E13) but keyed to an **observable builder state** (`grep -c 'case llvm::Instruction::CondBr'`), which works for every replay path.

5. **G13 (Volume 3 drops the IR scaffolding entirely — zero "Reading this" blocks in 1,942 lines).** *Noted, not elevated.* Round-2 note (no-compiler): a real audience-switch, but its practical impact on the two IR-weak personas (no-llvm + no-compiler) is low because both skip Volume 3 (security isn't either of their gaps). It matters only for a hypothetical fourth, IR-weak-but-security-curious reader. Tracked here so it is not silently lost; no change proposed.

6. **The root↔JSON cross-ref divergence as a *separate* change.** *Folded into E18.* It was discovered beyond A-1's nominal "start of each volume + each glossary" scope (the root files still carry stale lesson numbers that `proof_fixes_v1/v2.py` fixed only in the JSON), but it is the same signposting problem and is most coherently fixed by the crosswalk (E18), which must both state the convention and bring the root references to it. Not split out.
