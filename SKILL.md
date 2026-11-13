---
name: minishield-book-guide
description: Maintain the MiniShield LLVM/C++ study books and teach incremental implementation lessons, preserving beginner explanations, reader-facing walkthroughs, verified IR comparisons, and the learner's ownership of code. Use for book updates, lesson continuation, or agent handover in this repository.
---

# MiniShield book and teaching guide

## Purpose and ownership

This repository is both an LLVM pass-plugin project and a three-day teaching
book. The user writes the implementation and test scripts. The assistant teaches,
reviews that work, maintains the books, and validates reference examples.

- Inspect current files before continuing a lesson; do not infer completion from
  a chat acknowledgment or a finished book chapter.
- Do not write or replace implementation files, CMake configuration, or the user's
  scripts unless explicitly asked. Give scaffolds and let the user fill them in.
  Read-only review, builds, and appropriate verification are part of teaching.
- Documentation updates are expected to track the conversation automatically.
  Newly discussed questions, explanations, errors, and relevant examples belong
  in their matching lessons, not in an unrelated appendix.
- Preserve concurrent edits. Check `git status --short`, stage documentation by
  explicit filename, and leave unrelated dirty files and untracked fixtures alone.
- Keep README short. Put technical explanations in the relevant book chapter.
- The user prefers teaching to continue while requested book work runs in the
  background. Delegate only when current instructions authorize parallel work.
  Coordinate file ownership; one writer should own a given book dataset at a time.
- Never describe queued work as completed or a local commit as published.

## Where content lives

| File | Purpose |
| --- | --- |
| `volume1`, `volume2`, `volume3` | Editable, human-readable teaching sources; these are files without extensions. |
| `docs/assets/volume1.json`, `volume2.json`, `volume3.json` | The volume's web data: object with `day`, `title`, `status`, `groups`, `lessons`. All per-volume display data lives here (see "Volume files"). |
| `docs/assets/book.js` | Volume-agnostic renderer: navigation, quizzes, progress, callouts, widgets. Holds no per-volume data. |
| `docs/assets/book.css`, `docs/index.html` | Reading UI and volume tabs. |
| `PLAN.md` | Roadmap and evidence-based project milestones. |
| `README.md`, `environment.yml` | Concise entry point and reproducible environment. |

The static site is hosted from `main` / `docs` at
https://zilutian.github.io/minishield/ in GitHub repo
https://github.com/ZiluTian/minishield . It does not require a frontend build.
Keep this hosting arrangement unless the user requests a change.

### Stable chapter identity

Do not renumber IDs: URLs and saved reading progress depend on them.

- Volume 1 IDs after the 2026-11-13 tail restructure, IRBuilder chapter, and
  LLVM Crash Course addition: `0..19`, `23`, `26`, `73..77` (27 lessons; `20/21/22/24/25` were absorbed
  into the reference cards and dropped). Background is ID 0; eligibility
  capstone is ID 23; LLVM Crash Course is a separate chapter after ANALYZE,
  with object model/types/control flow lessons ID 75–77 followed by IRBuilder
  lessons ID 73/74; C++/LLVM reference cards are IDs 18/19; glossary is ID 26. All
  display metadata is in `volume1.json`. Lesson numbers are now local to each
  group/chapter; the renderer presents them as `volume.chapter.lesson`.
- Volume 2 logical order (after the 2026-11-13 inlining of the old testing
  volume, `78fcbaa`): `27..43`, then `45..55` (groups 1–7, as before), then the
  inlined testing chapters `56..69` in five new groups — DESIGN (56, 57), UNIT
  TESTS (58–61), INTEGRATION (62–64), MEASURE (65, 66), DELIVER (67–69) — then
  the Reference group `[44, 71, 72, 70]` — 46 lessons in 13 groups. Source
  labels: original sections keep `2.1.1..2.7.5`; the inlined content is
  `2.8.1..2.12.3`; the glossary documents are `2.13.1..2.13.4`. `.number` is
  the local order inside its group; `.day` is 2. Lesson ids and per-group
  numbers were preserved, so old URLs keep working.
- Volume 3 is now "Code hardening beyond flattening" (crash course). It holds
  only lesson `79` ("The code-hardening landscape", group LANDSCAPE) for now;
  new Volume 3 lesson ids start at `80` (id 78 is the Volume 1 capstone
  "Zoom out: a framework for hardening", added by the parallel session in
  `27bc168`). The volume3.json volume has a `home` object; there is deliberately
  no GLOSSARY group in volume3 yet — add one only when the glossary lesson lands
  (the renderer and part-cards need at least one populated group).
- Volume 2 policy lesson is ID 45 (`#lesson-45`, label `2.6.1`); builder
  interface lesson is ID 46 (`#lesson-46`, label `2.6.2`). IDs stay stable;
  labels are derived from volume, group position, and local group position.
- Pagers must follow dataset order, not numeric ID plus/minus one. Preserve
  existing localStorage progress and bookmarks when adjusting the UI.
- Lesson labels use `volume.chapter.local-lesson` (for example, `1.6.1`). The
  chapter number is the group's one-based position in that volume; the local
  lesson number is its one-based position in `group.ids`. Do not show chapter
  indexes on the volume overview or chapter cards; show the hierarchical label
  on lesson links and the lesson page.

### Volume files (modularization, 2026-11-13)

Each day is a self-contained volume so Volume 1 and Volume 2/3 can be edited in
parallel without touching shared code:

- `docs/assets/dayN.json` = `{day, title, status, groups, lessons}`.
  Per-lesson fields include `title`, `summary`, `takeaway`, `source`,
  `originalTitle`, optional `quiz`, `widget`, `pill`, plus `blocks`/`words`.
- `widget` (`"graph"`/`"memory"`) selects the interactive diagram rendered
  above the lesson body; `pill` overrides the eyebrow pill (Volume 1 lesson 1:
  `SETUP`).
- Optional volume `home` object (Volume 1 only today) carries the home-page copy:
  `headline`, `intro`, `coverFoot`, `aside: {label, text}`. `book.js` falls
  back to the hardcoded Volume 2/3 strings when `home` is absent.
- The loader fetches all three volumes uniformly and populates `groups`,
  `metadata` (title/summary/takeaway/source), and `quizzes` from the lesson
  fields; `book.js` contains no day-specific data (commit `cd9b0bd`,
  pixel-verified against the pre-refactor render).
- Local lesson tools target `volume1.json` in the volume shape and count
  checkpoint `answers` in `words`: `build/apply_lesson.py` (per-lesson block
  patch + word recompute; re-serializes byte-identically) and
  `build/build_lessons.py` (re-authors the tail lessons). `build/` is
  gitignored scratch (also the CMake build dir) — never commit from it.

Checkpoint model answers: a checkpoint block may carry an optional `answers`
array (blocks). In the teaching source the marker is a `### Model answer`
heading directly after the `Checkpoint:` line (heading consumed, not stored).
`book.js` renders it inside the callout as a click-to-reveal
`<details class="answer-reveal">` ("Show the model answer"); `book.css`
mirrors the deep-dive +/− marker and forces the reveal open in print
(`f03a20b` content/JS, `28bf368` CSS; the JS branch shipped in `36ed076`).
Word counters must recurse into `answers`.

Every rendered checkpoint now has a model answer (129 total: 99 top-level +
30 nested inside `deep`-dive sections — volume1 27, volume2 74, volume3 28;
`db968c8`, `e84164a`, `cd99b78`). Nested checkpoints live in
`deep.blocks` in the JSON and inside `### Deep dive:` sections in the
source; they follow the identical convention (`### Model answer` after the
`Checkpoint:` paragraph, `answers` as the checkpoint block's last key) and
count toward the enclosing lesson's `words` because `collect()` recurses
into both `deep` blocks and `answers`. `answers` shape is always exactly one
ordered list block: `[{"type":"list","ordered":true,"items":[…]}]`, one
item per question clause in order asked; verification-style checkpoints
state the expected concrete result plus what it proves.

### Glossary structure (all days)

The user decided (2026-11-13) that the Volume 2 GLOSSARY group holds three
documents, not one mixed glossary. Do not add LLVM IR constructs or C++
language terms to the main glossary; they have their own documents.

- ID `44` "Look up a term" — general computer-science and
  compiler concepts plus this project's own vocabulary (state ID,
  dispatcher, setup/entry, support contract, prototype checkpoint,
  prototype scope, demotion as a technique, cross-block/escaping value,
  worklist, SSA, dominance, constant folding, tail call, undefined
  behavior, differential test).
- ID `71` "LLVM concepts" — every LLVM-specific term
  the Volume 2 lessons encounter: printed-IR vocabulary, memory, aggregates,
  control flow, calls and attributes, function/block properties, and the
  C++ API side (see the document's own "Terms in this document" table for
  the current list).
- ID `72` "C++ concepts" — language concepts the
  lessons rely on (pointers/references, types/conversion,
  classes/translation units, ownership/lifetime).
- ID `70` "Testing and measurement concepts" (formerly "Terms used in
  Volume 3", reworded when the testing volume was inlined into Volume 2) —
  now the fourth member of the Volume 2 Reference group (label `2.13.4`);
  compact two-table format (`Term | Meaning` rows), not full entries.
- Volume 1 ID `26` is the master glossary (71-term table,
  "Glossary. Terms used in the README and Volume 1").

Glossary conventions (applied 2026-11-13 in `e84164a`/`cd99b78`):

- **Titles**: the Volume 2 GLOSSARY group is named `Reference`, matching
  Volume 1. Its pages use the same titles as the Volume 1 reference pages:
  `Look up a term`, `LLVM concepts`, and `C++ concepts` (user request,
  2026-11-13); their Volume 2 summaries still explain their specific scope.
   ID 70 is `Testing and measurement concepts`, the fourth page of the same
   Reference group (label `2.13.4`).
  Volume 1 ID 26 keeps `Glossary. Terms used in the README and Volume 1` as
  `originalTitle` (display title `Look up a term`). JSON `title` and
  `originalTitle` both carry the current display title; hierarchical source
  headings stay in sync.
- **Overview TOC**: each Volume 2 document opens with a "Terms in this
  document" heading + `Group | Terms` table, inserted after the document's
  `task` block (source: after the `Task: ` line). Volume 1/Volume 3 documents are
  themselves compact tables and get none.
- **Group dividers**: each `Group` from that table is a `### <group>`
  heading followed by a ONE-SENTENCE scope line before the first term
  heading (`d61971d`). book.js renders every `heading` block as the same
  `<h2>`, so a divider without a lead sentence renders as a dangling empty
  entry; all 13 dividers across ids 44/71/72 now carry one (11 added
  2026-11-13, "Aggregates" and "Ownership and lifetime" already had theirs).
- **Volume 1 cross-references**: a term already defined in the Volume 1 glossary
  is not repeated. Its entry becomes a pointer + local note: one
  `See the [Volume 1 glossary](#lesson-26) entry "<day-1 term>": <one-sentence
  essence>` line, keep the Volume-2-specific "Lesson N …" usage note and the
  external See link, drop the duplicated code block. Affected entries:
  id44 SSA/Dominance; id71 define-vs-declare, PHI, Terminator,
  unreachable, Intrinsic, EH pad, Personality function,
  Address-taken basic block, Coroutine intrinsic, Presplit coroutine,
  isa/cast/dyn_cast, PreservedAnalyses; id72 Pointer-vs-reference,
  #pragma once; id70 Translation unit, Usage requirement,
  CTest/GoogleTest (table cells). `#lesson-26` links work from any day:
  `book.js` `navigate()` matches `^#lesson-(\d+)$` over the flat cross-day
  lesson list. The id72 "Declaration vs definition" entry is NOT a
  duplicate (C++ header/.cpp side; the Volume 1 entry is the IR
  declare/define pair).
- **IRBuilder entry** (id71) is expanded beyond one construct: the
  `Create*` mechanics + `Value *` chaining, the two insertion-point forms
  (`IRBuilder<>(BB)` end-of-block vs
  `IRBuilder<>(&*entry->getFirstInsertionPt())` before-an-instruction),
  constant-folding and the `IRBuilder<Derived>` template gotchas, with a
  compressed lesson-14 dispatcher-step code example.

Each (non-cross-referenced) term entry is thorough, not a one-line table
row. Per term, in order:

- `heading`: the term.
- `paragraph`: what it is, plus the motivation — the problem it solves or
  the invariant it protects.
- `code`: a small, complete example (`llvm` or `cpp`); no ellipses.
- `paragraph` (optional): how the term appears in the Volume 2 lessons, and
  the gotcha.
- `paragraph`: the official-documentation link.

Volume 2 writes doc links as inline Markdown links in prose (`See [LLVM
casting](url).`), not as `reference` blocks: book.js renders a reference
block with the fixed label "Read the LLVM reference ↗", which is wrong for
cppreference or Wikipedia targets.

Verify every cited URL before adding it. The conventions below were checked
against the llvm-project main branch and the live sites on 2026-11-13:

- LangRef (`https://llvm.org/docs/LangRef.html`): anchors follow section
  titles — `#phi-instruction`, `#call-instruction` (musttail is documented
  inside the call section, there is no standalone musttail anchor),
  `#alloca-instruction`, `#load-instruction`, `#store-instruction`,
  `#select-instruction`, `#switch-instruction`, `#br-instruction`,
  `#ret-instruction`, `#unreachable-instruction` (not
  `#unreachable-statement`), `#aggregate-types`, `#constant-expressions`,
  `#inline-assembler-expressions`, `#function-attributes`,
  `#operand-bundles`, `#personality-function`, `#invoke-instruction`,
  `#callbr-instruction`, `#icmp-instruction`, `#functions`. The intrinsic
  reference now lives inside LangRef at `#intrinsic-functions`;
  `llvm.org/docs/Intrinsics.html` is gone. LangRef source is
  `llvm/docs/LangRef.md` in llvm-project (migrated from RST); derive unknown
  anchors from the section titles there.
- Other LLVM docs: `ConvergentOperations.html`, `Coroutines.html`,
  `ExceptionHandling.html`, `OpaquePointers.html`,
  `NewPassManager.html` (not `NewPM.html`), and
  `ProgrammersManual.html#the-isa-cast-and-dyn-cast-templates`.
- LLVM doxygen: `llvm.org/doxygen/classllvm_1_1{DenseMap, IRBuilder,
  Instruction, PHINode, BasicBlock, AllocaInst, IntrinsicInst, CallBase,
  Attribute, LLVMContext}.html`. `structllvm_1_1PreservedAnalyses.html` and
  `group__Transforms__Utils__Local.html` are 404; use
  `NewPassManager.html` for PreservedAnalyses and link the llvm-project
  `llvm/lib/Transforms/Utils/Local.cpp` source for
  DemotePHIToStack/DemoteRegToStack.
- cppreference: `/w/cpp/language/{reference, static, this, namespace,
  lifetime, auto, default_arguments, declarations, implicit_conversion,
  operator_other, expressions}.html` and
  `/w/cpp/container/vector/erase.html`. Short-circuit evaluation is on
  `operator_other.html`; range-based for is on `expressions.html`. Do not
  guess slugs: `shortcircuit_eval`, `range-based_for`,
  `standard_conversions`, `user_conversions`, `pragma`, `cv-qualifiers`,
  `conversions`, `const`, and `references` under `/w/cpp/language/` are all
  404.
- Wikipedia: `Static_single_assignment_form`, `Dominator_tree` (not
  `Dominator_(programming)`), `Constant_folding`, `Undefined_behavior`,
  `Tail_call`, `Register_allocation`, `Differential_testing`,
  `Dataflow_analysis` (for worklist),
  `Casting_(computer_programming)` (not `Casting_(programming)`),
  `Type_conversion`.

The old glossary quiz asks about `getInt32Ty`/`getInt32`, so it belongs in
the LLVM document; the pruned glossary needs a new general-concept quiz, and
the C++ document needs its own.

### Block format and synchronization

Common blocks are `paragraph` / `heading` with `text`, `code` with `language`
and `text`, `list` with `ordered` and `items`, `table` with `rows`, and
`task`, `checkpoint`, `debug`, `reference`. A `deep` block has `title` and
nested `blocks`; optional `lens: cpp` or `llvm` produces a badge.

Current additions may be tagged `conceptualIntro`, `irComparison`,
`irReadingGuide`, `sessionWalkthrough`, or `eligibilityWalkthrough`. Preserve
unknown fields and flags. Do not assume every historical addition uses one flag.

Update both the JSON and its matching canonical teaching source. Volume 1 contains
careful user revisions: edit the matching sections without regenerating the
whole file from an old parser or snapshot. For Volume 2/3, preserve every block when
serializing, including nested explanations, tables, and quizzes. Recompute
`words` including nested content. Quiz objects use `q`, `choices`, zero-based
`answer`, and `why`.

Use an existing committed generator if one becomes available. Temporary scripts
under `/tmp` from earlier sessions are not durable project dependencies. Do not
add executable scripts just to update prose unless requested or necessary.

## How to teach the next step

1. Read the relevant header/implementation, fixture, and book chapter. Locate the
   first unfinished step. Check actual code rather than repeating an already
   completed exercise or skipping one that is still absent.
2. Explain the concrete problem first: what invariant or behavior would break,
   why this step is relevant to flattening, and how it fits the pipeline.
3. Introduce needed compiler concepts in place. Assume little LLVM knowledge;
   C++ knowledge should also be taught whenever an unfamiliar construct matters.
4. Give a small writing task with an explicit insertion point, file, scaffold,
   relevant API names, and intended result. Avoid dumping the entire future
   implementation into a live lesson. The book may include the full reference.
5. Explain C++ parameter/return types, pointer/reference behavior, lifetime,
   ownership, and control flow as needed. The user prefers opcode `switch`
   classification to long `if/else` chains; use ordinary predicates naturally.
6. Provide a focused fixture and exact verification command. Explain expected
   output and what that observation establishes. Review the result before
   advancing. No requirement to run the same suite repeatedly without a change.
7. Update the matching book walkthrough with reusable teaching, including useful
   errors and their reasoning. Do not narrate the user's implementation history.

### Reusable lesson shape

Adapt length to the idea, but retain this teaching progression:

- **Problem and significance:** why the abstraction exists and why we need it.
- **Mental model:** a small source-language example, graph, or value trace.
- **Template to start with:** make the file, insertion point, and missing pieces
  explicit. Label fragments so nobody mistakes them for standalone programs.
- **Numbered steps:** teach one conceptual/API decision at a time.
- **Full reference:** a complete, coherent implementation or clearly bounded
  insertion, after the scaffold. State dependencies and preconditions.
- **Before/after LLVM program:** show the actual checkpoint's program delta.
- **Verify and explain:** commands, expected results, limitations, and a question
  that tests understanding rather than recall of a method name.

Keep advanced/confusing C++ and LLVM explanations substantial. Put prerequisite
concepts in the main flow; expandable deep dives can hold optional detail.
A glossary definition is not a substitute for explaining relevance in context.

### Study-session walkthrough voice

Write directly to another reader replaying the lesson. Retain the explanation,
code snippets, useful error examples, writing task, and expected check.

Use: “An empty PHI worklist does not mean there are no cross-block values. Let
this phase do zero edits, then continue to the next phase.”

Avoid: “The learner then implemented the guard,” “we observed the learner pass
this test,” personal progress logs, invented dialogue, or current user's
completion/pending status in instructional prose. Keep operational handover
status separate from the book. An expected result is an exercise instruction,
not a claim that the reader has executed it.

## Before/after LLVM examples

Every relevant lesson needs a complete pair for its exact stage. When the
checkpoint leaves the target module byte-identical (inspection, collection,
mapping, or rejection), show that single module once instead of duplicating
it as an After listing (user rule, 2026-11-13):

- Compare the two ```llvm modules byte-for-byte; never trust the prose alone.
- Keep the `### Before — X` heading + module; delete the `### After — X`
  heading + fence (source) and the `After — X` heading + code blocks
  (JSON, inside the `deep` block).
- Reword the details tail from the plural house sentence ("Both listings are
  complete LLVM modules … These listings were generated …") to the singular:
  "This listing is a complete LLVM module defining the example function, not
  a fragment with omitted blocks. It has no main driver unless one is
  explicitly included; opt can parse and verify it, while execution requires
  a caller. Names, alignments, and printer annotations may differ in your
  own output. This listing was generated and verified with the isolated LLVM
  23.1.5 teaching references, not copied from an assumed completed learner
  implementation."
- Reword any section prose that referenced the pair ("both listings",
  "the after listing", "in either listing", "This compares A with B") to
  singular. House sub-headings (`### Every instruction used in this pair`,
  the section heading "### LLVM program before and after this checkpoint",
  and the deep title "Read the complete before-and-after LLVM modules") stay
  unchanged in every section.
- Recompute the affected lessons' `words` (canonical `collect()`/`words()`),
  re-serialize the JSON byte-identically (`indent=2, ensure_ascii=False` +
  trailing newline), and commit source + JSON together, one commit per day.
- Applied 2026-11-13 in `c0b8a7e`/`2d9cefe`/`52513f6`: 21 sections
  (volume1 8, volume2 10, volume3 3) + six dangling-reference rewordings
  (volume1 3, volume2 3).

- Distinguish PHI-only demotion, full value preparation, disconnected dispatch,
  first entry hop, conditional/switch transitions, complete rewriting, and later
  optimization. Do not label the whole pipeline's output as one small edit.
- Generate examples from a separate reference stage, not from an unfinished
  user implementation. Keep generation artifacts outside tracked sources.
- Embed full modules in the book, with a visible explanation and expandable
  before/after listings when long. No ellipses or missing declarations in a
  program presented as standalone. Label partial fragments explicitly.
- Explain every instruction appearing in each pair, plus the local syntax:
  `define`/`declare`, return and argument types, `%` values versus block labels,
  `@` symbols, integer constants, `ptr`, operands, comments, and attributes.
- Explain execution order: branches choose destinations, PHIs select by incoming
  edge, select chooses available values rather than conditionally executing its
  operands, and ret ends the invocation. Trace a concrete input through both
  forms. A load/store uses an address; an alloca result is a pointer even when
  it reserves an i32 element. `align` describes an alignment requirement.
- Include opcode-specific semantics such as icmp predicates, switch defaults,
  PHI value/predecessor pairs, calls, aggregates, and special call contracts
  wherever they occur. Local explanations must be usable without LLVM fluency.
- `unreachable` asserts an execution cannot occur; reaching it is undefined
  behavior. It is not recovery, a return, or input validation.
- Explain why changes preserve intended meaning, rather than just listing added
  instructions. Unchanged output on a rejection must mean no partial edits.

## MiniShield invariants to preserve

The prototype uses this order:

`strict eligibility → PHI demotion → escaping-result demotion → state builder`

- Collect before mutating. `DemotePHIToStack(phi)` erases the PHI; do not use
  that pointer afterward. `DemoteRegToStack(*I)` keeps the defining calculation
  while changing value transport. These are LLVM free functions.
- No PHIs does not imply no cross-block dependencies. Skip void results and
  allocation instructions in the ordinary value worklist.
- Preserve original entry for one-time setup. State IDs identify prepared
  non-entry blocks. Snapshot original terminators before adding routing blocks.
- The builder adds dispatch and invalid: N becomes N+2, measured after value
  preparation. Demotion may alter the graph before that measurement.
- Write the correct destination state before every reachable dispatch load.
  Rewriting only entry is a partial checkpoint. Returns remain terminal.
- Rejection happens before edits. The guard conservatively restricts allocation
  placement, result types, intrinsics, special calls, EH/coroutines, block
  addresses, terminators, and naked functions. Rejection is prototype scope,
  not a claim that those LLVM constructs are intrinsically invalid.
- A changed CFG normally returns `PreservedAnalyses::none()` here. `all()` is
  a cache-validity promise, not an undo operation.

## Validation and publication

### Content/reference validation

- Inspect installed LLVM 23 headers for API details; use primary LLVM/C++ sources
  for semantic questions. Do not copy signatures from older tutorials blindly.
- Parse/verify every new complete LLVM module with the matching environment's
  `opt -passes=verify -disable-output`. Check each displayed checkpoint too.
- For behavior claims, compare original/transformed observations on a defined
  input domain. Bound signed arithmetic, record exact inputs, and distinguish
  finite evidence from proof. Two identical failures are not a passing test.
- Use focused positive and negative cases. Compare rejected input/output after
  canonical printing. An earlier unrelated rejection must not mask the guard
  being tested. Fixtures with external placeholder callees are guard tests,
  not runnable standalone demos.
- When only prose changes, do not rebuild the user's implementation needlessly.
  Temporary reference builds can validate book code without writing user files.
- Check canonical/JSON synchronization, retained blocks, stable IDs/group order,
  valid quiz answers, and `git diff --check` on documentation paths.
- For structural UI changes or large inserted sections, check desktop/mobile
  rendering, code copying, navigation, search, quizzes, and saved progress.
  A text-only edit generally needs proportionate checks.

### Toolchain and local preview

The established environment is `minishield`, LLVM/Clang 23.1.5 on Linux x86-64.
Check `environment.yml` and current tool versions rather than assuming paths.
This workspace's environment is currently
`/home/ruby.tian/miniforge3/envs/minishield`; C++ driver is `clang++-23`.
`LIBRARY_PATH="$CONDA_PREFIX/lib"` may be required for linking; it does not
solve runtime loader lookup. Reference GoogleTest executables need an appropriate
build RPATH when the loader cannot find the environment's shared libraries.

Serve the static book with `python3 -m http.server 8000 --directory docs`.
Choose another free port if occupied; do not stop someone else's server.

### Publishing

Publishing is a separate step from committing. Follow the current user's
requested scope and existing session authorization; the skill itself grants no
new external-action permissions. When publication is authorized:

1. Stage only intended docs. Do not commit the local `test_all.sh`, generated
   before/after `.ll` files, build products, or user source as part of a book edit.
2. Confirm repository identity. This project uses `ZiluTian` /
   `zilu.tian@uzh.ch`, not `ruby.tian@ovt.com`. Use local repo configuration;
   do not change global identity or infer credentials from an email address.
3. Push the intended commit to the authorized remote/branch. Use supported auth
   or an authorized session credential; never put access tokens in this skill,
   source files, git config, command arguments, logs, or handover notes.
4. Check the GitHub Pages action for that commit and fetch the public JSON to
   confirm the actual new section is live. Do not report “published” before this.
5. Give the direct chapter URL and the heading where additions can be found.
   If publication is pending or blocked, say so precisely. Do not repeatedly
   promise background updates while leaving completed local commits unpushed.

## Handover checkpoint — inspect again before acting

Recorded 2026-11-13 (after the Volume 2/3 restructure); this is a starting
pointer, not authoritative live state.

- `main` = `78fcbaa` (pushed, live-verified below). Phase A commit: "Inline the
  testing chapters into Volume 2; start the hardening crash course" — 7 files
  (volume2, volume3, docs/assets/volume2.json, volume3.json, docs/index.html, README.md,
  PLAN.md). The push also carried the parallel session's `27bc168` (Volume 1
  capstone lesson 78) — the remote was at `27bc168` at push time
  (`27bc168..78fcbaa`).
- Parallel session commits since this skill's last update (all pushed):
  `02131a6` IRBuilder chapter + hierarchical `V.G.L` source labels; `664e193`
  Volume 2 glossary titles aligned (`Look up a term`/`LLVM concepts`/
  `C++ concepts`, group back to `Reference`); `7596698` Volume 1 LLVM Crash
  Course (ids 75/76/77, 73/74 re-grouped, CRASH COURSE group); `6f51ace` /
  `59cb468` / `2cfd913` crash-course `diagram` blocks + widgets in
  book.js/book.css; `f177249` split license (MIT for code, CC BY-NC 4.0 for
  book content — new `LICENSE` file, README badges + License section,
  index.html footer notice, environment.yml header, license headers in all
  lib/include sources); `ace83f5` ownership-tree SVG in the object-model
  figure; `27bc168` Volume 1 capstone lesson (id 78, "Zoom out: a framework
  for hardening", group "Follow the control flow" after the eligibility
  capstone, 17 blocks / 1050 words with a quiz) + README "Beyond flattening:
  a framework for hardening" section linking `#lesson-78`.
- Phase A result: old Volume 3 (testing/evidence, ids 56–70) is now Volume 2
  groups 8–13 — DESIGN (56, 57), UNIT TESTS (58–61), INTEGRATION (62–64),
  MEASURE (65, 66), DELIVER (67–69), and 70 joins the Reference group as
  `Testing and measurement concepts` (label `2.13.4`). volume2 has 46 lessons /
  13 groups / 46 source sections (2.1.1–2.13.4). Ids and per-group numbers
  preserved (URLs stable). volume3.json now has a `home` object (headline
  "One technique.<br><em>A whole toolkit.</em>"), one group LANDSCAPE with
  lesson 79 ("The code-hardening landscape", 818 words, 11 blocks incl.
  checkpoint + 3-item model answer). index.html tab reads "Volume 3
  Hardening". No GLOSSARY group in volume3 yet — add one only when the glossary
  lesson lands.
- Phase B (per-part commits, ids from 82 after CFI): CFI ×2 DONE in `3e2738f` (lesson 80 "The indirect call check" 1163w, lesson 81 "The vtable check" 803w, group CFI labels 3.2.1/3.2.2). Remaining: stack canaries ×1 (`llvm.stackprotector` from
  `-fstack-protector-strong`), OLLVM family ×3–4 (learner implements bogus
  control flow, string encryption, subroutine splitting as new MiniShield
  passes per the capstone recipe; differential-verified; plus a "what the
  final -O2 keeps" persistence lesson), PIE ×1 (read-the-IR/tooling),
  fuzzing capstone ×1 (libFuzzer over a learner pass, behavior identity),
  glossary last. Every LLVM module: parse/verify with LLVM 23.1.5 (conda env
  `minishield`: `source /home/ruby.tian/miniforge3/etc/profile.d/conda.sh &&
  conda activate minishield`; transform check
  `opt -load-pass-plugin="$PWD/build/libMiniShield.so" -passes='function(minishield-flatten),verify' -S <fixture>`).
  Reference examples come from a separate reference stage; artifacts stay
  outside tracked sources. House conventions: lesson fields
  `id/number/day/group/title/originalTitle/summary/takeaway/source/blocks/words`,
  canonical `json.dumps(indent=2, ensure_ascii=False)+'\n'`, every rendered
  checkpoint carries exactly one ordered-list `answers` block, source
  headings `V.G.L Title` + `=` separator line synced with `originalTitle`.
- Pitfall hit in Phase A: a markdown-table builder used `out[1] = separator`
  (overwrite) instead of `out.insert(1, separator)` — silently dropped the
  first data row of the generated source table while the JSON stayed
  complete. When generating source from JSON, diff the row counts.
- Concurrent-work incident: at the start of Phase A the worktree carried an
  uncommitted license set + book.js diagram rebuild (later committed by the
  parallel session as `f177249`/`ace83f5`). It was about to be staged over by
  this session's commit; resolved by the user ("keep it separate") — in the
  end the parallel session committed it first, making the separation moot.
  Lesson: re-check `git log`/`git status` immediately before staging; when
  WIP of another session overlaps files you must edit, save their hunks as a
  patch, `git checkout --` those files, commit, then `git apply` the patch.
- CFI evidence + toolchain facts (verified 2026-11-13, LLVM 23.1.5): in LLVM 23 the CFI check is `llvm.type.test` + `llvm.ubsantrap`, NOT the legacy `llvm.cfi_icheck` intrinsic. ICALL: type.test on the callee pointer vs the function-type descriptor (`_ZTSFiiE` = int(int)); VCALL: type.test on the vtable pointer vs the base-class descriptor (`_ZTS4Base`). Commands: ICALL `clang-23 -fsanitize=cfi-icall -flto -O2 -no-pie -fuse-ld=lld <file>`; VCALL `clang++-23 -fsanitize=cfi-vcall -fvisibility=hidden -flto -O2 -no-pie -fuse-ld=lld` (error without hidden visibility). LTO link with system ld fails (LLVMgold.so missing) -> always -fuse-ld=lld. Verify: `opt-23 -passes=verify -disable-output <m.ll>`. All artifacts + the trimmed verified teaching modules live in `.v3ref/cfi/` (untracked). Runtime demos (verified): ICALL GOOD -> "result -> 42" exit 0 / BAD (wrong-type) -> SIGILL exit 132 / no-CFI BAD -> silent "result -> 99" exit 0; VCALL GOOD (Derived) -> 42 exit 0 / BAD (non-derived Evil) -> SIGILL. Final asm: LTO folds the check to `cmpq $<known-addr>; jne trap; callq *%rax` and turns the target into an `op_right.cfi` thunk. Pitfalls taught: CFI needs -flto and every linked object CFI-instrumented (non-LTO target -> even legal calls abort); -no-pie needed for the self-printed-address trick (ASLR); scanf format must be %lli for unsigned long long (%i/%llu leave the high half garbage -> every run traps); type.test is a type check, not an address check (same-type wrong target passes); ubsantrap lowers to ud1 -> SIGILL exit 132, no message.
- Teaching state: learner at label `2.6.3` ("Choose states for conditional
  branches", the old flat "section 19") — entry-hop for CondBr. Expected:
  `tests/ir/phi.ll` stores `select i1 %condition, i32 0, i32 1`;
  `loop.ll`/`select_case.ll` byte-identical (no cond branch). Prompt
  delivered; implementation pending. `lib/StateMachineBuilder.cpp` currently
  has UncondBr only.
- User source and fixtures remain dirty/untracked (`CMakeLists.txt`,
  `lib/FlatteningPass.cpp`, `lib/FunctionEligibility.cpp`, `lib/
  StateMachineBuilder.cpp`, `include/minishield/StateMachineBuilder.h`,
  `tests/ir/aggregate-result.ll`, `convergent.ll`, `inline_assembly.ll`,
  `intrinsics.ll`, `musttail.ll`, `nonentry-alloca.ll`,
  `operand_bundle.ll`, `returns_twice.ll`). Never reset or commit them. Push doc work via the SSH one-shot
  (`git push git@github.com:ZiluTian/minishield.git main`) because the HTTPS
  remote has no stored credentials; the parallel session also commits/pushes
  doc work, so always re-check `git log` before pushing.
- `SKILL.md` (this file) is untracked local notes; keep it current, never
  commit it. Its indentation is normalized to 2-space list continuations; the
  edit tool has failed to match lines that look identical (use a
  whitespace-tolerant regex for replacements).
- Check `git log`, `git status`, remote state, and Pages deployment before
  describing the latest book as published.
