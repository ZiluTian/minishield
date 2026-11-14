# Round 2 — cross-reaction (reader: senior C++, no LLVM)

I read both round-1 reports in full. My round-1 position: my gap is the LLVM side
(printed-IR literacy, the C++ API surface, the manager/plumbing architecture); security
hardening is home turf. That lens makes the cross-reaction clear: the **no-compiler**
persona's gap is substantially *my* gap, so I endorse most of their B-series; the
**no-hardening** persona's gap (security) is *my* home turf, so I endorse only the parts
of their C-series that touch LLVM or book-trust, and I say so plainly where a proposal
serves only them.

## 1. Endorsements

**B-1 — C→IR mapping ("Where does this IR come from?").** Endorsed, and it helps me more
than I flagged in round 1. I never stopped asking "what C produces this?" when reading the
`phi.ll`/`loop.ll`/`if-else.ll` fixtures (v1 1.4.x) and the demotion listings (v2 2.2.1–2.5);
the book introduces them as "handwritten text IR" with no C beside them. A C→IR pairing at
the first PHI is the same load-bearing anchor I needed. (I dispute its *placement*, see
Pushback 1.)

**B-3 — SSA payoff up front.** Endorsed. SSA was the first IR idea I had to internalize; the
"every assignment is a new value, so merges need a PHI" contrast is exactly what I needed at
2.2.1, delivered ~20 lessons late.

**B-2 — One concrete `verify` failure.** Endorsed. I inferred `verify`'s behavior from prose
("Valid vs. correct", v1 Background) the same way they did; a real error string would let me
predict what it catches.

**B-5 — Front-load the `Module → Function → BasicBlock → Instruction` nesting before 1.4.2.**
Endorsed. My first traversal (1.4.2) iterated `for (const BasicBlock &BB : F)` with no object
model in hand; I read forward to 1.6.1 and back, as they did.

**B-4 — Why `PreservedAnalyses` exists (1.3.1).** Endorsed, and I'd fold it into my A-4
(pass-manager lesson) rather than land it as a separate one-liner — see New proposal A-12.

**B-6 — Label the "Study-session walkthrough" as the recorded-mistake part.** Endorsed as an
*insight*; it refines my A-5. They saw the block's **role** (the third repetition is the
gotcha, which is valuable) where I saw its **offense** (session-voice, SKILL.md violation).
That's a merge, not a pick — see A-10.

**C-1 — Build-state / artifact reconciliation (3.4.4, 3.6.1).** Endorsed in *principle*,
contested in *premise* (see Pushback 2). The trust-breaker is real and cross-profile: any
reader who builds the pass and then replays Volume 3 hits "printed output ≠ my tree" and
cannot separate their error from the book's. I endorse the "name which builder state each
artifact assumes + how to check yours" device book-wide.

**C-6 — Name the mechanism in 3.4.4's -O2 control (DCE + mem2reg vs. proving the state
machine).** Endorsed for cross-profile value: naming the optimizer pass is LLVM knowledge I'd
want too, and it's the kind of "label the mechanism, not the outcome" discipline the book's own
final-artifact standard demands.

**Not endorsed for me (honest):** C-2 (attack primer), C-3 (C++ object model / vtables), C-4
(demo C sources), C-5 (CFI descriptor/`-flto`/mangling), C-7 (security terms), C-8 (CFI table
row), C-9 (libFuzzer `cov`), C-10 (GOT-overwrite walk). These are the no-hardening reader's gap,
which is my home turf; I have no evidence they improve *my* learning and I won't endorse them
politely. (I agree they're important *for that reader*.)

## 2. Pushbacks

**Pushback 1 — B-1's earliest placement (Volume 1 Background, ≈L55) is too early.**
B-1 offers two locations: Background ≈L55 *and/or* 1.4.2. I endorse 1.4.2 / 2.2.1 and push
back on L55. At Background/L55 the reader has met **no** instruction, block, or PHI yet.
Dropping `clang -O0` output of a `for` loop — back-edge PHI, numeric labels (`9:`, `%3`), an
`alloca` for the loop variable — before the object model (B-5's nesting table) and before the
first "Reading this IR" vocabulary would reproduce exactly the failure mode I logged in round 1
(G5): a wall of unfamiliar IR that trains the reader to skip. The C→IR mapping needs the
vocabulary it's mapping *into*. Put it at the first PHI (2.2.1), cross-referenced from 1.4.2,
not in the Background.

**Pushback 2 — C-1's "regenerate against the 2.6.5 end state, what Volume 2 leaves you with"
conflicts with the book's own contract (my A-9).** C-1 pins the 3.4.4/3.6.1 artifacts to "the
2.6.5 end-state, what volume 2 leaves them with." But from 2.6 on every task line reads
"Task: Future exercise … your working implementation has not been updated for you" (v2 2.6.1
L3945). So the 2.6.5 reference is precisely *not* "what Volume 2 leaves you with" — a replaying
reader has **not** implemented it. C-1's premise holds only for a reader who has already built
2.6.5, which the book's own disclaimer says they haven't. The fix is to pin each artifact to an
**explicit builder state / commit**, not to a conceptual "end-state." This also confirms A-9 is
load-bearing: until the 2.5→2.6 contract change is signposted, no artifact in 3.4.4/3.6.1 can
be pinned coherently.

**No conflict found on the C-series security content or B-2/B-3** — I checked them against my
reading notes and they neither hurt my learning nor collide with my A-1…A-9.

## 3. New proposals

**A-10 — Merge A-5 + B-6 into one first-class "Common mistake / gotcha" section. M.**
*Location:* every "Study-session walkthrough" block (v2 L105, L340, L515 … L4656; v1 L1516 et
seq.). *Gap:* my G4 + their G-4 (two personas stuck on the same block from opposite sides).
*Change:* restructure each lesson so the recorded mistake is a labeled, first-class section —
"Common mistake / gotcha: …" — that keeps the technical content (the mistake *is* the useful
part) but drops the session narrative ("the learner preferred…", "the first draft…", "Observed
bug:"). Place it as the lesson's explicit caution, not a buried unlabeled third repetition.
*Why:* B-6 wants to keep-and-label; my A-5 wants to rewrite. Both are right about half; the
merged change serves the strong reader (B-6's "recognize the gotcha") and the standard (A-5's
"no learner-progress log") at once.

**A-11 — Book-wide artifact-provenance note (C-1's principle, de-conflicted from A-9). M.**
*Location:* top of every lesson that prints a "your implementation should produce this"
artifact — v2 2.6.5 (full builder), v3 3.4.4 (persistence listing, L868–958), v3 3.6.1
(negative-control diff, L1720–1733). *Gap:* C-1's trust-breaker (G8/G11) + my A-9. *Change:*
one line per artifact: "This listing assumes builder state X (entry-UncondBr / entry-CondBr).
Check yours: `grep -c 'br label %ms.dispatch' <artifact>`. If your tree predates §2.6.2, your
listing differs — expected." *Why:* C-1's "pin to 2.6.5 end-state" is unsolvable while the
reader's tree is unknown (Pushback 2); a provenance line keyed to *observable* builder state
works for every replay path and makes the A-9 contract concrete.

**A-12 — One consolidated "the shape of what you're manipulating" page (unify A-4 + B-4 + B-5). M.**
*Location:* early Volume 1, before the first traversal (1.4.2) and before first `PreservedAnalyses`
(1.3.1). *Gap:* my G10 + their G-5/G-6 (three readers needed the system model in the same 1.3–1.6
region from different angles). *Change:* a single canonical page: (1) the `Module → Function →
BasicBlock → Instruction` nesting (B-5); (2) who-owns-whom + the PassBuilder /
ModulePassManager / FunctionPassManager / `run(Function&, AnalysisManager&)` graph (A-4);
(3) `PreservedAnalyses` as cache invalidation, the "why" (B-4). *Why:* three separate insertions
in the same pages would collide and fragment the model; one page gives every reader the object
*and* manager model together, and becomes the reference the later "do not blindly transplant"
warnings (v2 2.9.2 L7587) can point at.

## 4. Joint top 3 (all three readers)

1. **A-1 (numbering crosswalk).** Both other personas independently hit the lesson-N / day-number
   opacity — the no-hardening report cites v3 L813 "Lessons 83 through 85" as web day-numbers,
   and the no-compiler report's cross-refs are equally unresolvable. It unblocks every pointer in
   all three volumes for every reader; cheapest fix with the broadest reach.
2. **A-12 (consolidated object + manager model page, = A-4 + B-4 + B-5).** The no-LLVM and
   no-compiler gaps converge on the system model in the same 1.3–1.6 region; the no-hardening
   reader has it as floor. One page serves all three where three insertions would collide.
3. **A-11 (artifact-provenance note, C-1 de-conflicted from A-9).** The trust-breaker for anyone
   who replays code; the no-hardening reader runs every command, and the other two hit it the
   moment they build 2.6 and reach Volume 3. Keying provenance to observable builder state (not a
   conceptual "end-state") is what makes it solvable under the A-9 contract.

*Runner-up: A-10 (the merged session-voice/gotcha change) — book-wide and affects all three
readers, but it's hygiene rather than unblocking.*
