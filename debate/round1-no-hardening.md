# Round 1 review — persona: compiler/LLVM developer, no security background

## 1. Reader profile

I write LLVM New-PM passes: IR, IRBuilder, the analysis managers, SSA, CFGs, and `opt` are home turf, so volumes 1–2 are below my floor. My gap is everything security: threat models, what CFI-ICALL/CFI-VCALL check or why, what a canary protects, what OLLVM is, what "reading" a binary (reverse engineering) means, what ASLR/PIE/RELRO do, what a fuzzer is for beyond crashing, or why an obfuscation is judged on the final artifact. Secondary gap: I read C++ *IR* fluently but know little C++ object model (vtables, type-info), which 3.2.2 silently assumes.

## 2. Reading route

- **Volume 1**: skimmed at heading level; spot-checked 1.5.5 in full — its level map (which techniques are IR passes vs. compiler/linker/OS decisions) is exactly the setup I needed, and 3.1.1 correctly points back to it.
- **Volume 2**: read 2.7.1, 2.7.2, 2.7.4 (partly), 2.10.1 reasonably fully — the differential method, `-disable-O0-optnone`, bounded domains, and the "an unreachable dispatcher proves nothing" warning all land well; 3.6.1 reuses them. Skimmed the rest. Snag feeding G8: 2.6.5's "full builder" (rewrite *every* terminator) is not what the repo's current `lib/StateMachineBuilder.cpp` does.
- **Volume 3**: read in full, slowly. Walls: 3.2.2 (C++ object model), 3.4.4 (printed artifact doesn't match what the repo's code produces), 3.6.1's negative control (recorded diff doesn't reproduce against current `lib/`).

## 3. Gap log

- **G1** | 3.1.1, lines 21–29 | The book assumes I know what each threat *is*, as a concrete attack | No end-to-end attack story anywhere: "Reads or patches the program's logic" is label-only; I had no picture of a "static reader" or of what an overflow does byte-by-byte. **Recovered:** guessed from the chapters; would have searched "how a stack overflow attack works."
- **G2** | 3.1.1, line 24 (+ glossary 1866, 1896) | Table promises "`llvm.cfi_icheck` — forward and backward CFI" | Backward CFI is never taught; the named intrinsic is legacy per the glossary's own words. Also 1.5.5's "Forward CFI … target-set checks" primes *target sets*, while 3.2.1 (line 88) calls the check "not an address check" — unreconciled. **Recovered:** stuck; inferred forward = check before the jump, and a type as a coarse stand-in for a target set.
- **G3** | 3.2.1, lines 61, 86, 104, 116 | I can accept a `type.test` guard as IR | Why *require* `-flto`? Where is the CFI type descriptor emitted and laid out? How does `type.test(ptr, metadata !"_ZTSFiiE")` map a pointer to a mangled name? No token-level decode of `_ZTSFiiE` / `_ZTS4Base`. **Recovered:** stuck; would have searched "clang CFI type descriptor LTO."
- **G4** | 3.2.1/3.2.2/3.3.1 "Proof at runtime" (118–137 et seq.) | The demo programs exist | Their C sources (`cfi_pipe.c`, `vcall_pipe.cpp`, `canary_pipe.c`) are **not in the book** (I checked the web-book JSON too); the prose is too thin to reconstruct them, and outputs (`result -> 42`, `HACKED`) are unpredictable without them. Contrast: 3.4.4 and 3.5.1 *do* inline their C fixtures. **Recovered:** guessed at the programs; expected results stayed on trust.
- **G5** | 3.2.2, lines 157–219 | The C++ object model: vptr in the object's first word, vtable slot 0 = first virtual method, class type-info, "belongs to Base's hierarchy" | None of it is taught; the C++-ABI semantics are the payload. How `type.test` tests a vtable pointer against a class (what table it consults) is never shown, and symbol interposition (model answer b) is one unexplained clause. **Recovered:** stuck; would have searched "C++ vtable Itanium ABI layout, type_info."
- **G6** | 3.3.1, lines 306, 310 | I can derive the heuristics and the payload | "The `--help` text" names no tool; "24 bytes of padding" wasn't derivable until I mapped the asm layout (buffer −32, canary −8, return +8 → 24 bytes to reach it) — the C source that makes it obvious is missing (G4). **Recovered:** partially, from the lesson's own asm.
- **G7** | 3.4.1, lines 355, 361 | I know what a "static reader" is, and what an "opaque predicate" is | Reverse engineering is never concretized — no disassembly, no named tools (objdump/IDA/Ghidra), no statement of what an analyst hunts for; and "opaque predicate" is used before its definition (glossary entry at 3.7.1). **Recovered:** guessed from OLLVM lore + the fixture paragraph (line 365).
- **G8** | 3.4.4, lines 868–958 (and 813) | The printed `persist_final.ll` is what *my* plugin produces | Not for either plausible build: rebuilt from the current working tree (`StateMachineBuilder.cpp` now has an entry-CondBr case, lines 60–72) and replayed the exact 3.4.4 command on `.v3ref/ollvm/persist_o2.ll`: the entry **is** rewired (`select` + `store` + `br`; `ms.dispatch` gets `preds = %1`), but the printed listing shows the entry branch intact and `ms.dispatch: ; No predecessors!`. 2.6.5's "full builder" is a third variant. The lesson's *conclusions* still hold (behavior identical on all three inputs; control: `switch i32` 1 → 0) — the artifact and its interpretation are stale. (Line 813's "Lessons 83–85" cites web day-numbers, not lesson numbers.) **Recovered:** stuck → built, replayed, diffed `.v3ref` to diagnose.
- **G9** | 3.4.4 "The control: re-run -O2", lines 978–988 | I can name the exact mechanism removing the dispatcher | "the dispatcher is gone" without a mechanism (printed artifact: unreachable block → DCE + mem2reg restoring the plain shape; fully-wired build: proving the state machine, 2.7.4's merge route). **Recovered:** inferred; both routes give the same observable.
- **G10** | 3.5.1, line 1095 | I know the GOT-overwrite attack and what `checksec` is | The attack is named, never walked; `checksec` is undefined. **Recovered:** inferred.
- **G11** | 3.6.1, lines 1548–1568, 1720–1733 | I can read the libFuzzer log, and the recorded diff reproduces | What `cov` counts isn't stated; the seed descriptions are stale ("seed02 … scaffolding nothing reaches" is false with current code, whose entry-CondBr rewiring makes the scaffolding live); and replaying the negative-control `diff` against current `lib/` shows `54c54` **plus** `56,69d55` — the mutant was cut from a pre-entry-CondBr build, not the printed one-liner. **Recovered:** verified with diff; diagnosed version drift.
- **G12** | Scattered (3.2.1 line 120; 3.3.1 line 324; glossary 1924) | I know ASLR/PIE, exit-code arithmetic, "calling convention" | ASLR/PIE get one clause each four lessons before their chapter; 132/134 = 128 + signal-number is never stated; "matching calling convention" (line 137) is undefined. **Recovered:** guessed; the glossary helps after the fact.

## 4. Improvement proposals

**C-1. Reconcile 3.4.4/3.6.1 with the actual plugin state (build-state pinning + artifact regeneration).**
- *Location*: 3.4.4 (868–958, "The artifact" + "The entry the pass does — and does not — rewire"); 3.6.1 (seeds 1568; negative-control diff 1720–1733).
- *Gap*: G8, G11.
- *Change*: (1) A "build state" note at the top of 3.4.4: which builder capabilities the printed output assumes (entry UncondBr / entry CondBr / non-entry terminators, yes-no each), and how to check yours (`grep -c 'br label %ms.dispatch'` on your artifact; look for `; No predecessors!`). (2) Regenerate the 3.4.4 artifact and the 3.6.1 negative-control diff against the reader's actual builder state — ideally the 2.6.5 end-state, what volume 2 leaves them with. (3) A bridging sentence in the control section: the persistence claim doesn't need a live dispatcher — the original branch edges are intact, so behavior is preserved by the unrewired graph and the -O2 control measures what the *scaffolding* survives (linking 2.7.1's "no predecessors proves nothing").
- *Effort*: M.
- *Why it helps me*: I run every command in this book; when printed output doesn't match mine I can't tell which discrepancies are mine and which are the book's — the volume's biggest trust-breaker.

**C-2. A concrete-attack primer in 3.1.1.**
- *Location*: new subsection after the threat table (after line 29).
- *Gap*: G1, G7 (part).
- *Change*: ~20 lines: one end-to-end overflow story tied to 3.3.1's demo — attacker input; unchecked `memcpy` past the 16-byte buffer; crosses the canary slot at −8(%rbp); overwrites the saved return address at +8(%rbp); on `ret` the CPU loads it and jumps; with a canary the exit compare aborts first. Plus a 5-line "what reverse engineering looks like" box: tools (`strings`, `objdump`, IDA/Ghidra), what analysts hunt for (string literals, clean CFGs, the license branch), why structure inflation buys time.
- *Effort*: M.
- *Why it helps me*: the volume is organized by threat; without a pictured attack every chapter is "here's a check, here's what it stops" — labels, not responses.

**C-3. A C++ object-model sidebar in 3.2.2.**
- *Location*: before "The check is on the vtable pointer" (before line 159).
- *Gap*: G5.
- *Change*: ~35-line box, "Virtual dispatch in 30 seconds (for readers of IR, not C++)": (1) each object starts with a hidden vptr to its class's vtable; (2) a vtable is a per-class array of function pointers, slot 0 = first virtual method; `b->apply(x)` = load vptr, load slot 0, indirect call; (3) derived classes get their own vtable, same leading slots; (4) each class has a `__class_type_info` the vtable points to (`vtable[-2]`) — "belongs to Base's hierarchy" = the type-info is Base or derives from it; (5) `type.test` consults a compiler-built table mapping type-info to the hierarchy's vtables; the guard checks the vtable pointer against Base's set; (6) `-fvisibility=hidden` stops another library's same-named type-info symbol binding in place of yours (symbol interposition).
- *Effort*: M.
- *Why it helps me*: the lesson's IR is trivial to me but its C++ semantics are the payload; as written I decode a known syntax to carry a fact I don't have.

**C-4. Inline the demo C sources in 3.2.1, 3.2.2, 3.3.1.**
- *Location*: each "Proof at runtime" section.
- *Gap*: G4, G6 (part).
- *Change*: include the full sources as templates before the runtime proof — `cfi_pipe.c` (21 lines), `vcall_pipe.cpp` (20), `canary_pipe.c` (38). The book already inlines its C fixtures in 3.4.4 and 3.5.1; the inconsistency is the problem. The canary source makes the 24+4×8 payload arithmetic self-evident.
- *Effort*: S–M.
- *Why it helps me*: the "why" of each check lives in the C; today I must reconstruct three programs from prose to predict a single output line.

**C-5. CFI mechanism note: descriptor location, why `-flto`, mangling decode.**
- *Location*: 3.2.1, after "Where LTO can see the target, the check changes shape" (after line 116).
- *Gap*: G3, G2 (part).
- *Change*: a short paragraph, sketch: the expected type is call-site metadata (`!17 = !{i64 0, !"_ZTSFiiE"}` on the `type.test` call); LTO emits a type-descriptor table with an entry per CFI-compiled function (why `op_right` gets its `.cfi` copy: the original stays for non-CFI references, the copy carries the descriptor); `type.test` resolves the pointer against that table — no LTO, no table, hence `-flto`. The "target set" is simply *all functions of this type*, a stand-in for an address set. Then a two-line decode: `_ZTS` = type-info name; `Fii` = function `(i32)→i32`; `4Base` = length-prefixed identifier. (Author to verify descriptor emission against the 23.1.5 LTO pipeline; the metadata line is in `.v3ref/cfi/cfi_pipe.s`.)
- *Effort*: M.
- *Why it helps me*: I know intrinsics and LTO; what's missing is the data structure connecting a pointer to a mangled name — without it `type.test` is a black box.

**C-6. Name the mechanism in 3.4.4's -O2 control.**
- *Location*: "The control: re-run -O2" (978–988).
- *Gap*: G9.
- *Change*: 2–3 sentences: in the printed (partially-wired) artifact `ms.dispatch` has no predecessors, so DCE deletes it and mem2reg re-promotes the demoted values; in a fully-wired build the same endpoint is reached by proving the state machine (2.7.4's merge example). Same observable, different mechanism.
- *Effort*: S.
- *Why it helps me*: as an optimizer person I want to name the pass that removes the structure; "it's gone" without a mechanism is the label-only move the book's standard forbids.

**C-7. Bring the security terms forward.**
- *Location*: 3.1.1 "How this volume works" (line 42, currently two terms).
- *Gap*: G12, G2, G10 (signposting class).
- *Change*: a compact "terms you'll meet before they're explained" list: vtable/vptr, ASLR, PIE, GOT/RELRO, mangled type-info name, calling convention, symbol interposition, checksec, reverse engineering, exit-code arithmetic (132 = 128+SIGILL; 134 = 128+SIGABRT). One line each, pointing at the lesson; the 3.7.1 entries exist — promote the key ones, don't duplicate.
- *Effort*: S–M.
- *Why it helps me*: I hit ~a dozen terms before any definition; the end-of-volume glossary serves review, not first reading.

**C-8. Fix the CFI row of the threat table (and the backward-CFI promise).**
- *Location*: 3.1.1, line 24 (+ glossary CFI entry, 1866).
- *Gap*: G2.
- *Change*: replace "`llvm.cfi_icheck` — forward and backward CFI" with "type-based guard (`llvm.type.test` + `llvm.ubsantrap` in 23.1.5)"; the glossary already calls `cfi_icheck` legacy, so the table shouldn't lead with an intrinsic the toolchain doesn't emit. For "backward," either add a 3–5 line glossary paragraph defining it (a check at the target that the caller is permitted — the CET/shadow-stack family 1.5.5 already names) with an explicit "this volume teaches only forward checks," or drop the word from the table.
- *Effort*: S.
- *Why it helps me*: the table is read first; leading with an intrinsic the glossary calls legacy makes me uncertain which layer is authoritative, and an unexplained promise reads as a missing lesson.

**C-9. State what libFuzzer's `cov` counts in 3.6.1.**
- *Location*: "Build and run," before the log (line 1548).
- *Gap*: G11 (part).
- *Change*: two sentences: libFuzzer instruments the harness's own instructions; `cov`/`ft` count edges/function-units reached so far, `NEW` = an input reached a new edge. Most mutations die in the parser, so the new edges live in the parser and gate, not the pass — which is why the pass is judged on behavior by the differential, not on coverage.
- *Effort*: S.
- *Why it helps me*: `cov: 185 → 195` is the evidence that the gate works; I need the measurement model to read the log rather than trust it.

**C-10. A GOT-overwrite micro-walkthrough in 3.5.1.**
- *Location*: RELRO section (line 1095).
- *Gap*: G10.
- *Change*: three lines: the attack — an overflow in some reachable buffer rewrites a `.got.plt` jump slot to an attacker address; the next call to that import (`printf`) jumps there; RELRO's `PT_GNU_RELRO` range goes read-only after relocation, so the write faults. Cross-link: CFI-ICALL polices the *call* through a corrupted pointer; RELRO polices the *table* the pointer came from — complementary layers, same threat shape.
- *Effort*: S.
- *Why it helps me*: I can read the `readelf` output; I need the attack to know what the segment defends.

## 5. Top 5 for my profile

1. **C-1** — build-state/artifact reconciliation: until fixed, every replay I run is suspect and I can't separate my errors from the book's.
2. **C-2** — concrete-attack primer: the volume is organized by threat; a pictured attack converts every chapter from label to response.
3. **C-3** — C++ object-model sidebar: 3.2.2 is the one lesson I literally cannot follow semantically without outside material.
4. **C-5** — CFI descriptor mechanism + why `-flto` + mangling decode: makes the volume's central intrinsic non-black-box.
5. **C-4** — inline the demo C sources: cheap; turns three "trust me" runtime proofs into "read the source" ones.

## 6. My ideal edition

For a reader like me, the ideal volume 3 opens with a threat I can picture — one overflow traced byte-by-byte through the canary and return address, plus five lines on a reverse engineer's screen — so every technique after is a response to something I've seen. Each check lesson gives the *data structure* behind the check (CFI descriptor table, vtable/type-info layout, RELRO segment); I learn mechanisms by locating their state in memory. The C++ I don't know gets a 30-second sidebar before the vtable lesson. Every command reproduces the printed output for the builder state volume 2 taught me, with a note on which state it assumes; every "the optimizer removed it" names the pass and route. The glossary splits: definitions before first use, the full list for review. Untouched: IR-first pedagogy, the differential method, the final-artifact standard, the negative control — the parts I, as a compiler person, found excellent.
