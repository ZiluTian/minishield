# Round 2 — cross-reaction (persona: no-compiler / strong systems dev)

## 1. Endorsements

(Only the ones that genuinely serve *my* profile too. I am not politing for the security
proposals — security is my home turf, not my gap.)

- **A-1 (numbering crosswalk)** — I hit the same opaque "lesson N" refs (v1 L134 "lesson
  16"; the glossary's "lesson 24" at 2.13.1 L10069). A crosswalk unblocks every forward
  pointer I use to re-find a concept. Pure signposting; helps me.
- **A-9 (signpost the 2.5→2.6 contract change)** — As a learner, the build-along →
  reference-only flip is the biggest "what am I supposed to implement now?" moment. If I
  miss that 2.6+ ships complete reference implementations, I burn time trying to build-along.
  Strong cross-profile value.
- **A-4 (pass-manager / analysis-manager mini-lesson)** — My round-1 G-5
  (`PreservedAnalyses`) is the same root problem: the object graph (who creates whom, what
  a pipeline is, what `PreservedAnalyses` invalidates) is never drawn. I can infer "cache +
  invalidation" from general systems experience, but the PassBuilder → PassManager →
  AnalysisManager nesting is compiler-specific and I couldn't reconstruct it from the API
  calls. I'd fold my B-4 into this as the better version.
- **A-7 (declare-vs-define row)** — I guessed `declare` = prototype from C++; a one-line
  row in the first syntax table removes that guess. Cheap; helps the IR-weak reader.
- **A-5 (session-voice cleanup)** — The superset of my round-1 B-6. I also found the
  "Study-session walkthrough" / "Observed error:" framing reads like one student's log.
  Crucially, A-5 *preserves* the pedagogical payload (the wrong code, relabeled
  "Common mistake:") while changing the voice — so it keeps the "recorded mistake" value I
  wanted B-6 to surface.
- **A-3 (fix stale 1.4.5)** — A brief that contradicts the reader's current state (I
  already implemented StatsPass in 1.4.1–1.4.4) is a real mid-task stall for any replier.
- **A-6 (fix StateMachineBuilder task at v1 L3361)** — "A task that names a class 800 pages
  away is not a task." True for a no-compiler reader replaying Volume 1: I can't tell
  whether to invent it or wait.
- **A-8 (DenseMap one-liner)** — Minor. I'd infer it's a hash map from C++, but the
  "lookup, not display order" nuance matters for the state-ID mapping. Low-stakes, cheap.
- **C-1 (reconcile 3.4.4/3.6.1 with the actual plugin state)** — The one security proposal
  I endorse, on *reproducibility* grounds, not security knowledge: as a systems dev who
  runs every command, a printed artifact that doesn't reproduce against the current tree is
  a trust-breaker — I can't separate my errors from the book's. That's a version-drift
  problem, which is my home turf; the CFI/canary content inside is not my gap, but
  "does it reproduce?" is.

**Deliberately NOT endorsing (security is my home turf, not my gap):** C-2 (attack primer),
C-3 (C++ object-model sidebar), C-5 (CFI descriptor), C-6 (name the -O2 mechanism), C-7
(security terms forward), C-8 (CFI threat row), C-9 (libFuzzer cov), C-10 (GOT-overwrite
walk) — these serve the no-hardening profile specifically. Two notes: C-6 (naming "DCE +
mem2reg") would not help *me* — I don't yet know what those passes are, so naming the
mechanism without teaching it is label-only for a no-compiler reader. And C-3 (vtables) is
the inverse case — it's *my* home turf and their wall (their G5); I can't endorse it as
helping me, though I'm happy to sanity-check the Itanium-ABI details.

## 2. Pushbacks

**A-2 (collapse the ~37 "Reading this LLVM program from zero" blocks into one canonical
guide + per-lesson deltas, full block demoted to a collapsible appendix).**

I support the *diagnosis* (the genuinely new rows — `select`, `store`, `switch`, `phi`,
`unreachable`, `sdiv`/`nsw`, numbered `%0`/`9:` names, the attribute/metadata table — are
buried in ~2,000 lines of repetition; the repetition trains skipping). I push back on the
*mechanism*, from my reading experience:

- The no-llvm persona (G5) skipped the tables by the 3rd–4th occurrence. I did **not**.
  In round 1 my G-4 was about the Task/Checkpoint being restated 3× per lesson — I did
  **not** log the IR-reading tables as skippable filler, because as a no-IR reader each pass
  still carried new information I couldn't infer. That difference is profile-dependent: a
  strong-C++ reader can recover a skipped IR detail from C++ context; a no-compiler reader
  cannot.
- A-2's specific mechanism — "full block demoted to a collapsible appendix" — optimizes for
  the reader who skips (strong C++). For the no-compiler reader it *removes the in-context
  safety net I actually use*: at 2.7.2 (the C→IR discount example, v2 L6162/L9669, with all
  the numeric labels and `sdiv`/`nsw`/`select`) I need the full instruction table *in
  place*, not behind an appendix I expand mid-lesson. Collapsing to one canonical guide +
  appendix optimizes for the profile that can afford to skip, at the expense of the
  profile that can't — and the no-IR reader is the one this book is most for.
- The right fix keeps the full block but surfaces the NEW rows at the top and states the
  block's purpose — my B-7 below — not a collapse.

**Everything else:** I checked A-1, A-3, A-4, A-5, A-6, A-7, A-8, A-9 and the full C-series
for conflicts with my round-1 proposals (B-1…B-6). No other genuine disagreement: my B-6 is
subsumed by A-5; my B-1 (C→IR) and B-3 (SSA) live in Volume 1 and don't touch their Volume
2/3 proposals; my B-2 (verify failure) and B-5 (nesting table) don't conflict with anything
they raised, and B-4 overlaps A-4 (I'd fold B-4 into A-4).

## 3. New proposals

(Only visible once I saw what the other two struggled with. IDs continue from round 1.)

**B-7 — A "repetition key": label what each recurring block is for and which readers it
serves. M.** *Location:* start of each volume (and, briefly, at each lesson's first
recurring block). *Gap:* my round-1 G-4 + the no-llvm persona's G5 + A-2's diagnosis.
*Change:* a short key classifying the book's recurring blocks by intent and audience: (a)
"Task/Checkpoint restated 3× = re-verify your work (intentional); the 3rd occurrence — the
'Study-session walkthrough' — is the recorded-mistake part, read it, skip the
re-statement"; (b) "'Reading this LLVM program from zero' = IR-weak-reader scaffolding —
read the full table once per *new* instruction, then each later occurrence only needs its
**NEW rows**, marked at the top of the block"; (c) "'Walk one concrete execution' = the
worked example, read once." The NEW rows get a `NEW in this lesson:` callout so the reader
finds them without scrolling 2,000 lines. *Why it helps:* it fixes repetition-fatigue for
the IR-strong/strong-C++ reader (skip to the delta) while keeping the in-context safety net
for the IR-weak reader (me) — i.e. it captures A-2's benefit without A-2's appendix-collapse
cost, and it absorbs my round-1 B-6.

**B-8 — A "reader routing" front-matter page: who is each volume for, and what to
read/skip. M.** *Location:* start of each volume (generalizing the no-llvm persona's
ideal-edition "How to read this book" page). *Gap:* all three personas' home-turf
differences; my round-1 reading route; no-llvm G1/G11/G14. *Change:* one page per volume
that (1) gives the x.y.z ↔ lesson-N crosswalk (their A-1), (2) states the
build-along-vs-reference-only contract and where it flips (their A-9), (3) states the
IR-scaffolding policy — which "Reading this" blocks are for IR-weak readers and which you
may skip if you're IR-strong (my + no-llvm repetition finding), and (4) routes by home
turf: "if you know security, skim Volume 3; if you know IR, Volumes 1–2 are below your
floor; the C++ is at the level of a strong C++ dev." *Why it helps:* no single persona
proposed this unified routing; each proposed a piece (A-1, A-9). It only becomes visible
after reading all three reports — the three personas' home turps are three different walls,
and the book currently assumes one reader. It's the cheapest way to make A-1, A-9, and B-7
discoverable.

*Note (elevation, not a new proposal):* no-llvm's G13 (Volume 3 drops the IR scaffolding
entirely) is a real audience-switch, but its *practical* impact on the two IR-weak personas
(me + no-llvm) is low because both of us skip Volume 3 (security isn't either of our
gaps). So I'm not elevating it to a top change; it matters for a hypothetical fourth,
IR-weak-but-security-curious reader.

## 4. Joint top 3

The three changes that would most improve the book for **all three** readers:

1. **A-1 (numbering crosswalk) + A-9 (2.5→2.6 contract signpost)** — signposting every
   persona hit: no-llvm on the numbering (G1/G14) and the contract flip (G11); me on the
   contract flip (I'd misread 2.6+ as build-along); the crosswalk unblocks the cross-refs
   all three use to re-find concepts. Cheap, no content change, universally unblocking.
2. **A-4 (pass-manager / analysis-manager mini-lesson)** — the one *missing content* item
   (not just signposting) that the two IR-weak readers (me + no-llvm) both can't infer from
   the API calls; the IR-strong no-hardening persona already has it (home turf), so it
   doesn't hurt them. The only "teach the concept" fix that serves two of three while
   no-op'ing the third.
3. **C-1 (build-state pinning + artifact regeneration in 3.4.4/3.6.1)** — a stale artifact
   that doesn't reproduce is a trust-breaker for anyone who runs the book's commands, and
   all three personas run commands (no-hardening explicitly; me as a systems dev; no-llvm
   who replays). It's the no-hardening persona's #1 and a systems-dev value for me.
