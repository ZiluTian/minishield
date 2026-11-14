# Round 1 — review from a senior C++ reader with zero LLVM

## 1. Reader profile

- 8 years of professional C++ (systems, embedded, build tooling); one university PL course (parsing, basic IR ideas, no LLVM API).
- Never used LLVM: no `opt`, no IRBuilder, no `dyn_cast`/`PHINode`, no pass-manager or analysis-manager experience. Reading a `.ll` file past "hello world" output is new to me.
- The book's C++ is at most a mild strain for me: pointers, references, namespaces, CMake modules, GoogleTest, reading installed headers — all fine.
- Security-hardening knowledge is **not** my gap: I know canaries, CFI, ASLR, OLLVM at working level. Volume 3 is fine to skim.
- My gap is precisely the LLVM side: printed-IR literacy, the C++ API surface, and the manager/plumbing architecture.

## 2. Reading route

- **Volume 1 in full** (3,875 lines; 1.2.1–1.7.3 plus the unnumbered Background chapter).
- **Volume 2 in full** (11,483 lines; 2.1.1–2.13.4). I skimmed only the repeated "Reading this LLVM program from zero" / "Every instruction used in this pair" blocks — and only after the 3rd–4th occurrence. That behavior is itself a finding (G5).
- **Volume 3 at lesson-heading + checkpoint level** (1,942 lines): 3.1.1 landscape; 3.2.1/3.2.2 CFI; 3.3.1 canaries; 3.4.1–3.4.4 OLLVM; 3.5.1 PIE; 3.6.1 fuzzing; 3.7.1 glossary.
- Reading text is the root `volumeN` files; `docs/assets/volumeN.json` is context only (it explains the day-based ordering behind the sequential "lesson N" cross-refs).

## 3. Gap log

Each entry: location → quote → what was assumed/missing → how I recovered.

**G1 — Three numbering systems coexist.** Headings are x.y.z; cross-refs are sequential "lesson N"; tasks are "task 1.x". v1 L134 "lesson 16", L888 "lesson 5 traces that registration", L902 "CFGAnalyzer declaration comes in lesson 15"; v2 L539 "lesson 1", L699 "lesson 01", L1646 "lesson 9", L2907 "lesson 12", L6959/L8112 "lesson 24" (= 2.7.2), L11094 "lesson 8", L11409 "lesson 13's pointer-key fix". The v2 sequence resolves by counting from 2.2.1 (lesson 24 = 2.7.2, confirmed at L6959), but nothing documents that; v1 and glossary refs (v1 L3657 "EH pad … see lesson 20") stay opaque. *Recovered by reconstructing the mapping from `docs/assets/volume2.json`'s day order — thirty minutes of detective work for a signposting problem.*

**G2 — A third system inside a heading:** v1 L1291 "1.4.1 Start task 1.2 by declaring StatsPass". Now I must also track task-number ↔ lesson.

**G3 — Stale session artifact in 1.4.5** (v1 L1685–1689): "Status: the statistics pass is the next implementation task. The current plugin only registers `minishield-flatten`" — but I had *already* implemented StatsPass in 1.4.1–1.4.4; the five-step brief then re-instructs what I just did. Related: 1.4.4 L1544–1556 prescribes switch-on-opcodes; 1.4.5 L1698 prescribes `isa<T>`; no statement of which to use when replaying. *Recovered by re-reading 1.4.1–1.4.4 to work out which half was current.*

**G4 — Session-record voice throughout.** v1 L1516 "The learner preferred switch/case", L1950 "was reported by the learner", L2384 "The learner should write it", plus "Observed error/bug/omission:" markers; v2 has dozens of "Study-session walkthrough — …" headings (L1940, L2190, L2414, L3117, L3373, L3598, L3981–L4656 …), "Observed error:" L2903/L3409, "the first draft" L2816/L3335, L3774 "compiled separately from the learner's source". This violates the book's own SKILL.md and makes the text read as one student's session log rather than a book for me. *Read through; the content is good, the frame is not.*

**G5 — Verbatim-repeated IR-reading blocks.** "Reading this LLVM program from zero" + "Every instruction used in this pair" + "Walk one concrete execution" + the full module pair appear ~7× in v1 (L1249–1290 … L2520–2571) and ~30× in v2 (L133–232 … L9416–9514). By the 3rd–4th occurrence I was skipping them as filler; the genuinely new rows (`select`, `store`, `switch`, `phi`, `unreachable`, `sub`/`mul`/`sdiv`/`nsw`, `ptr`, `align 4`, numbered `%0`/`9:` names, and the new "The other syntax printed around this function" attribute/metadata table variant at L6818/8248/8977/9446) are buried among ~2,000 lines of repetition. Each block sits *after* the checkpoint/model answer, so it reads as a postscript. Early tables also forward-reference the discount kernel ("for the discount kernel it checks whether the amount is negative", v2 L1001) whose fixture first appears at 2.7.2 (L6162).

**G6 — Forward reference without context:** v1 L1269/L1419 "In a demoted listing only the executed path stores its constant" — demotion is a Volume 2 concept; the sentence is uninterpretable in Volume 1. Noted and moved on.

**G7 — v1 L1344** "Skip declarations with `F.isDeclaration()`" — before any IR example of declare-vs-define (only the glossary L3634 and 1.7.2 L3525, both later). *Guessed from C++ that declare = prototype.*

**G8 — v1 L2869 (1.6.1)** names "DenseMap" without definition; v2 gives a one-liner only at re-appearance (2.5.1 L2633; full entry 2.13.2 L11022).

**G9 — v1 L3361 task:** "In `StateMachineBuilder`, build the dispatcher…" — StateMachineBuilder is a Volume 2 class (2.6.2, L4557). Not actionable in replay; I couldn't tell whether to invent it or wait.

**G10 — The pass-manager/analysis-manager hierarchy is never taught.** v1 L886–889 mentions "PassBuilder" in passing; 1.3.3 L1050–1058 uses `FunctionPassManager &FPM` and a `run()` taking `FunctionAnalysisManager &AM` — but the object graph (who creates whom, what a pipeline is, what `PreservedAnalyses` invalidates, module vs function managers) is never drawn. v2 2.9.2 L7587 ("A module pipeline needs the corresponding outer managers and proxy registration; do not blindly transplant") assumes it. As a C++ dev I could read each API call; I could not build the nesting model. *The one place I had to leave the book for external LLVM docs.*

**G11 — The actionable → reference-only contract change is unsigned.** From 2.6 on, every task line reads "Task: Future exercise: …" with "your working implementation has not been updated for you" (2.6.1 L3945; repeats 2.6.2 L4557, 2.6.5 L5440, 2.7.3 L6516, 2.8.1 L7093, 2.9.2 L7574, 2.10.1 L8112, 2.12.2 L9531 …). 2.2–2.5 are build-along; 2.6+ ships full reference implementations (FlatteningPass.cpp L3646–3754, StateMachineBuilder::build L5469–5552). The shift lands without a word at the 2.5/2.6 boundary — exactly where an implementer needs to know the contract changed.

**G12 — v2 L5575:** "not a remembered number like input N+1 from the old roadmap" — "old roadmap" is an artifact I don't have. I recovered the intent (assert N+2 for this design, not a remembered figure) but the referent dangles.

**G13 — Volume 3 drops the IR scaffolding entirely:** zero "Reading this" blocks in 1,942 lines. The 3.4.1 module uses `urem`, `icmp sge`, `tail call`, `llvm.type.test`/`llvm.ubsantrap`, `metadata !"_ZTSFiiE"`, `[16 x i8] c"…"` constants — none taught by the v2 instruction tables. For this persona hardening isn't the gap so skimming was fine; a reader still relying on the tables would stall here. (Low priority for me; logged for completeness.)

**G14 — Glossary cross-refs use the same opaque "lesson N" system** (2.13.1 L10069 "revisit lesson 1's path-dependent choice", L10121 "DemotePHIToStack in lesson 3 and DemoteRegToStack in lessons 8–9", L10243 "lesson 24 … lesson 26"). The glossary is where I go when lost; if its pointers need the same undocumented mapping, they fail in the one moment they're needed.

## 4. What worked (keep as-is)

- 2.1.1 orientation + stage table; "Check your understanding" MCQs at every v2 lesson end; complete (not fragment) before/after modules in `<details>`, with the right disclaimers (L8856, L9845).
- Full reference implementations: 2.5.5 FlatteningPass.cpp (L3646–3754), 2.6.5 StateMachineBuilder::build (L5469–5552).
- Per-eligibility-guard rationale in 2.6.1–2.6.4 (why each rejection exists, not just that it does).
- 2.7.2 differential-testing design; 2.10.2 L8544 "zero discovered tests can exit successfully"; 2.6.3 "A select is an IR value, not a C++ if"; 2.6.4 L5225 `llvm::Value*` vs `auto*` constant-folding warning.
- The 2.13 three-glossary split (general / LLVM / C++) is the best-organized reference material in the set.

## 5. Improvement proposals

**A-1 — Numbering crosswalk. M.** *Location:* start of each volume + each glossary. *Gap:* G1, G2, G14. *Change:* a small table mapping sequential "lesson N" (the web book's day order) to x.y.z sections per volume, with one line stating the convention ("Volume 2: lesson 0 = §2.2.1"); alternatively rewrite cross-refs to x.y.z anchors. *Why:* pure signposting, no content change, and it unblocks every forward/backward pointer in the book, glossary included.

**A-2 — One canonical IR-reading guide, then per-lesson deltas. L.** *Location:* the 7+30 "Reading this LLVM program from zero" blocks. *Gap:* G5. *Change:* a single canonical section at the first full-module reading (v1 1.4.x): the syntax table, the instruction table, one concrete walk. Every later lesson replaces the verbatim block with a 5–15-line "New in this lesson" delta (only genuinely new rows: `select`/`store`/`switch`/`phi`/`unreachable`/`sub`-`mul`-`sdiv`-`nsw`/`ptr`/`align 4`/numbered names, and the attribute/metadata table once), with the full block demoted to a collapsible appendix. *Why:* the repetition trained me to skip the guide — the opposite of the intent — while burying the new rows that are the actual lesson content.

**A-3 — Relocate/fix the misplaced stats deep dive in 1.4.5. S–M.** *Location:* v1 L1685–1698. *Gap:* G3. *Change:* move the deep dive ahead of the 1.4.1 implementation as the task brief, or rewrite the stale "Status: the statistics pass is the next implementation task" to "you implemented this in 1.4.1–1.4.4; here are the fixtures to verify your counts" — and add one line reconciling switch-on-opcodes (1.4.4) with `isa<T>` (1.4.5): both are correct; the reference uses `isa<T>`. *Why:* a brief that contradicts the reader's current state is worse than no brief.

**A-4 — New mini-lesson: pass managers & analysis managers. M.** *Location:* early Volume 1, before first use of PassBuilder/FPM (v1 L886/L1050). *Gap:* G10. *Change:* one page with a nesting diagram: PassBuilder (pipeline parsing + registration) → ModulePassManager / FunctionPassManager → `pass::run(Function &, FunctionAnalysisManager &)` → `PreservedAnalyses`. What each layer owns; why a module pipeline needs "the corresponding outer managers and proxy registration" (2.9.2 L7587); why the legacy `PassManager` is out of scope. *Why:* the one architectural concept I could not infer from the API calls the book shows; every later "do not blindly transplant" warning assumes it. This is the missing content, not just the missing signpost.

**A-5 — Session-voice cleanup per SKILL.md. M.** *Location:* throughout v1/v2 (v1 L1516/L1950/L2384; v2 "Study-session walkthrough" headings, "Observed error:" L2903/L3409, "the first draft" L2816/L3335, L3774). *Gap:* G4. *Change:* rewrite the narration as direct instruction — "The learner preferred X" → present both options and say which the book takes and why; "Observed bug:" → "Common mistake:" with the wrong code labeled; "the first draft had…" → labeled before/after. *Why:* SKILL.md bans learner-progress logs; the session frame undercuts replayability while the content inside is good and must stay.

**A-6 — Fix the StateMachineBuilder task in 1.6.5. S.** *Location:* v1 L3361. *Gap:* G9. *Change:* replace "In `StateMachineBuilder`" with the free-function version (build the dispatcher block with IRBuilder: load, switch, addCase per pair), or mark "Preview: the class is introduced in Volume 2 §2.6.2; do this step as a free function for now". *Why:* a task that names a class 800 pages away is not a task.

**A-7 — declare-vs-define row in the first syntax table. S.** *Location:* the first IR-reading table in v1, before L1344. *Gap:* G7. *Change:* one row: `declare i32 @f(i32)` announces a bodyless function (no blocks; `isDeclaration()` true); `define … { }` provides a body; passes run only on definitions. *Why:* it's the first use and the book never shows it.

**A-8 — DenseMap one-liner at first use. S.** *Location:* v1 L2869. *Gap:* G8. *Change:* "(LLVM's open-addressing hash map — lookup, not display order; defined in Volume 2 §2.13.2)". *Why:* one line removes a "what is this?" stall in the middle of the state-ID mapping.

**A-9 — Signpost the 2.5 → 2.6 actionable → reference-only shift. S–M.** *Location:* the 2.5/2.6 boundary (before 2.6.1 L3945). *Gap:* G11. *Change:* one paragraph at the boundary: "The contract changes here. 2.2–2.5 were build-along; from 2.6 each lesson ships a complete reference implementation, and 'Task: Future exercise' means 're-implement this from the reference — your working tree has not been updated'. In replay mode: diff against the reference, re-derive each checkpoint, and treat 'Not measured' as a standing instruction." *Why:* for an implementer persona this is the largest structural signposting gap in the book — the contract silently changes mid-volume, and a reader who misses it either keeps expecting build-along tasks or dismisses the references as non-canonical.

## 6. Top 5

1. **A-4** — pass-manager/analysis-manager mini-lesson. The only gap I could not close inside the book; I had to consult external LLVM docs. Everything else is signposting; this is missing content.
2. **A-1** — numbering crosswalk. Cheap (M), unblocks every cross-reference in all three volumes, including the glossary's.
3. **A-2** — canonical IR guide + per-lesson deltas. The book's largest block of repeated text is currently training readers to skip it; the genuinely new rows are buried.
4. **A-9** — signpost the 2.5→2.6 contract change. An implementer who misses it misreads half the book.
5. **A-3** — fix the stale 1.4.5 deep dive (and reconcile the two classification approaches). Small change, high confusion cost, exactly where a replaying reader is mid-task.

*Honorable mention: A-5 (session-voice cleanup) — book-wide hygiene and a violation of the book's own standards, but it doesn't block understanding.*

## 7. Ideal edition

For this reader, the ideal edition is:

- A "How to read this book" page at the start of each volume: the x.y.z ↔ lesson-N crosswalk (A-1), the two reading modes (build-along vs read-and-replay from 2.6, A-9), and a note that the `<details>` reference implementations are canonical and complete.
- One canonical IR-reading section up front, with "New in this lesson" deltas instead of ~37 verbatim repetitions (A-2).
- A one-page pass-manager nesting diagram before the first plugin registration (A-4).
- A book whose voice is the book's, not a study session's: no "the learner", no "Observed bug", no "the first draft" (A-5).
- Every task either actionable at its point in the text, or explicitly marked "Future exercise — do this when you reach §2.6.2" (A-6, A-9).

Everything else I want as-is: the depth is right, the checkpoints are well-posed, the before/after modules are complete, and the 2.13 three-glossary split is genuinely useful.
