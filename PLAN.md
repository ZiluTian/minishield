# MiniShield — 3-Day Plan

LLVM-based control-flow-flattening pass plugin. Working environment is **ready**
(see "Environment" below). You write the code; this file is the roadmap: tasks,
pitfalls, and a verifiable *exit criteria* for every task.

## Progress (2026-11-11)

| Milestone | Status |
|---|---|
| Environment and CMake | Complete: plugin builds against LLVM 23.1.5 |
| 1.1 Plugin skeleton | Complete: `minishield-flatten` loads and executes; remains a diagnostic stub |
| 1.2 IR statistics | Ready to implement: requirements and fixtures are documented in README |
| 1.3 CFG analysis | Not started; loop counting is deferred here |
| 1.4 Function eligibility | Not started |
| Day 2 flattening | Not started |
| Day 3 tests, benchmarks, demo | Not started; smoke input and IR fixtures exist |

**Current study task:** implement the statistics pass and its check scripts
yourself, using the README instructions and supplied fixtures. Manually
cross-check `phi.ll` against the expected counts before moving to 1.3.

Target layout (create as you go):

```
minishield/
├── CMakeLists.txt
├── include/minishield/
│   ├── CFGAnalyzer.h
│   ├── FunctionEligibility.h
│   ├── StateMachineBuilder.h
│   ├── StatsPass.h
│   └── FlatteningPass.h
├── lib/
│   ├── CFGAnalyzer.cpp
│   ├── FunctionEligibility.cpp
│   ├── StateMachineBuilder.cpp
│   ├── StatsPass.cpp
│   ├── FlatteningPass.cpp
│   └── Plugin.cpp
├── tests/
│   ├── unit/
│   ├── integration/
│   └── ir/
├── benchmarks/
│   └── results/
├── scripts/
└── README.md
```

---

## Environment (done — do not re-do)

- Conda env: `minishield` at `/home/ruby.tian/miniforge3/envs/minishield`
- Contents (single release, conda-forge): **LLVM/Clang 23.1.5** (`clang`, `opt`,
  `llvm-config`, `llc`, `llvm-as`, `llvm-dis`, `lld`, ...), **gtest 1.18.0**
  (CMake-config based: `find_package(GTest)` works), **cmake**, **ninja**.
- Use it: `conda activate minishield`, then `clang` (C) / `clang++-23` (C++;
  there is no plain `clang++` in the env) / `opt` / `llvm-config`.
- CMake must point at LLVM: `-DLLVM_DIR=$CONDA_PREFIX/lib/cmake/llvm`
  (= `.../minishield/lib/cmake/llvm`).
- **C++ standard: C++20** (LLVM 23 requires it — the original spec said
  "C++17 or C++20"; pick 20: `set(CMAKE_CXX_STANDARD 20)`).
- C++ development headers are installed via `libstdcxx-devel_linux-64`
  16.2.0, matching the environment's GCC runtime. A missing `<type_traits>`
  means those development headers need checking, not LLVM's include paths.
- Shared `libLLVM-23.so` is present → build the plugin as a `MODULE` and link
  against the LLVM dylib (see Day 1, Task 1.1).
- `opt` writes the transformed module to **stdout** by default — always pass
  `-S` (text IR) or `-o out.ll`.
- **Deviation from spec (accepted):** conda-forge does not ship `FileCheck`/`not`/
  `count` for LLVM 23. IR-level assertions are written in **C++/GoogleTest**
  using LLVM's own APIs (`verifyModule`, `DT`, block/terminator inspection) —
  stronger than text-matching, and matches the spec's GoogleTest requirement.

---

## Day 1 — Foundations: plugin skeleton, IR stats, CFG analysis, eligibility
(~7–8 h)

### 1.1 Hello-pass plugin (New Pass Manager) — ~2 h
Goal: a loadable pass plugin that `opt` can run, printing per-function stats.

- Top-level `CMakeLists.txt`: `find_package(LLVM REQUIRED CONFIG)`, plain
  `add_library(MiniShield MODULE ...)`, link against the imported target
  `LLVM` (= `libLLVM-23.so`, created by `LLVMConfig.cmake`).
  **Verified gotcha:** the conda `llvmdev` package does NOT ship
  `LLVM.cmake`/`AddLLVM.cmake`, so `add_llvm_library` /
  `llvm_map_components_to_llvmlib` / `include(LLVM)` are unavailable —
  plain CMake + the imported target is the correct consumer pattern.
- `lib/Plugin.cpp`: define `::llvm::PassPluginLibraryInfo`
  (name "minishield", plugin version "1.0") with:
  - `PB.registerPipelineParsingCallback(...)` — parse the pass name
    `minishield-flatten` and register `FlatteningPass` on the function PM;
    parse `minishield-stats` and register `StatsPass` (task 1.2). The installed
    LLVM 23 callback takes `(llvm::StringRef Name,
    llvm::FunctionPassManager &FPM,
    llvm::ArrayRef<llvm::PassBuilder::PipelineElement> InnerPipeline)`.
  - Include `llvm/Plugins/PassPlugin.h` and return the header-provided
    `LLVM_PLUGIN_API_VERSION`; no custom version macro is needed.
- `FlatteningPass` is a **stub for now** (prints function/block counts without
  changing IR), so the plugin loads.
- **CMake skeleton** (write it yourself; the non-obvious lines are commented):
  ```cmake
  cmake_minimum_required(VERSION 3.15)
  project(MiniShield CXX)

  set(CMAKE_CXX_STANDARD 20)            # LLVM 23 headers REQUIRE C++20
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  set(CMAKE_EXPORT_COMPILE_COMMANDS ON) # enables clangd

  # This conda build is a dylib build: LLVMConfig.cmake sets
  # LLVM_LINK_LLVM_DYLIB=yes itself and creates the imported target `LLVM`
  # (= libLLVM-23.so). Do NOT try include(LLVM)/add_llvm_library — the
  # installed package does not ship those in-tree-build helpers.
  find_package(LLVM REQUIRED CONFIG)    # CONFIG → use LLVMConfig.cmake
  message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION} at ${LLVM_DIR}")

  # MODULE = dlopen()-able .so for -load-pass-plugin
  add_library(MiniShield MODULE
      lib/Plugin.cpp
      lib/FlatteningPass.cpp            # stub for 1.1; add sources as you create them
  )
  # LLVM's own compile definitions (LLVMConfig.cmake sets them as ONE
  # space-joined string → split into a real list) + include dirs, at
  # TARGET scope (not add_definitions/include_directories, which would
  # pollute every target in the tree).
  separate_arguments(MS_LLVM_DEFS NATIVE_COMMAND ${LLVM_DEFINITIONS})
  target_compile_definitions(MiniShield PRIVATE ${MS_LLVM_DEFS})
  target_include_directories(MiniShield PRIVATE
      ${LLVM_INCLUDE_DIRS}
      ${CMAKE_CURRENT_SOURCE_DIR}/include)

  # Imported target `LLVM` = libLLVM-23.so: every LLVM symbol in the plugin
  # resolves from the same library that opt itself loads.
  target_link_libraries(MiniShield PRIVATE LLVM)

  set_target_properties(MiniShield PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
  ```
  ABI rule: LLVM is built without RTTI → never `dynamic_cast` on LLVM types.
- Build (verified working):
  ```
  conda activate minishield
  export LIBRARY_PATH=$CONDA_PREFIX/lib      # conda's ld can't find -lstdc++ otherwise
  cmake -G Ninja -S . -B build -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_CXX_COMPILER=$CONDA_PREFIX/bin/clang++-23 \
        -DLLVM_DIR=$CONDA_PREFIX/lib/cmake/llvm
  ninja -C build
  ```
  (The env ships `clang++-23`, NOT a plain `clang++` — `$(which clang++)` is
  empty. If you run `cmake ..` inside `build/` instead, keep the same
  `-D` flags and the `LIBRARY_PATH` export.)
  Cosmetic warnings from LLVMConfig.cmake (`Could NOT find ZLIB/LibXml2/
  zstd`) are harmless: optional deps of the LLVM build, already inside the
  shared `libLLVM-23.so`.
- Failure-mode table: `can't open shared object` at load → env not activated
  (`ldd build/libMiniShield.so | grep -i llvm` must show exactly one
  `libLLVM-23.so` from the env); `undefined symbol` at load → static component
  archives instead of the dylib (two LLVMs in one process); "no such pass" →
  pipeline name mismatch between `registerPipelineParsingCallback` and
  `-passes=`; `cannot find -lstdc++` at link → missing `LIBRARY_PATH`;
  `No SOURCES given to target` → the listed `.cpp` files don't exist yet.

**Exit criteria:**
```
conda activate minishield
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -S tests/ir/minishield-input.ll -o build/minishield-output.ll
```
The plugin loads without symbol errors. *If you get "undefined symbol" at load
time: you linked against the wrong (or missing) libLLVM — check
`ldd build/libMiniShield.so | grep LLVM` resolves to the env's `libLLVM-23.so`.*

### 1.2 IR traversal pass → function-level statistics — ~2 h
Goal: the "IR inspection pass" of Phase 1, doubled as your stats tool for
Day 3 benchmarks.

- Traverse `Module → Function → BasicBlock → Instruction`. The function pass
  manager visits functions; `StatsPass::run()` loops over blocks/instructions.
- Per function report: #blocks, #branches (cond/uncond), #switches, #PHIs,
  #returns, #calls, #invoke, #indirectbr, #loops (see 1.3 for detection).
- Print a human-readable report to `errs()`.

**To implement:** `include/minishield/StatsPass.h` + `lib/StatsPass.cpp`,
registered as `minishield-stats`. Use a required pass so inspection also runs
on `optnone` functions. Keep it read-only and return `PreservedAnalyses::all()`.
`calls` counts `call` instructions, including recursive and indirect calls;
`invoke` is counted separately. Branch counts count instructions, not edges;
`switch` and `indirectbr` have separate counters. Loop counts should print
`loops=deferred` until task 1.3, rather than reporting a misleading zero.

After implementing and registering the pass, run with the environment activated:

```bash
cmake --build build
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-stats),verify' \
  -disable-output tests/ir/phi.ll
```

Hand-counted expectations for the five study fixtures (all have zero
`invoke` and `indirectbr` instructions):

| Fixture | Blocks | Conditional br | Unconditional br | Switches | PHIs | Returns | Calls |
|---|---|---|---|---|---|---|---|
| `if-else.ll` | 3 | 1 | 0 | 0 | 0 | 2 | 0 |
| `loop.ll` | 4 | 1 | 2 | 0 | 1 | 1 | 0 |
| `switch.ll` | 4 | 0 | 0 | 1 | 0 | 3 | 0 |
| `recursion.ll` | 3 | 1 | 0 | 0 | 0 | 2 | 1 |
| `phi.ll` | 4 | 1 | 2 | 0 | 1 | 1 | 0 |

When writing the check scripts, also cover the smoke input, `invoke`,
`indirectbr`, skipped declarations, and an `optnone` function using
`instruction-kinds.ll`. Check that the pass preserves the canonical IR
produced by `opt`. See README for the remaining expected counts.

**Study walkthrough:** open `tests/ir/phi.ll`. Its four labels are four basic
blocks. `entry` ends in one conditional branch; `left` and `right` each end
in one unconditional branch. `join` contains one PHI and one return. There
are three branch instructions total, even though the conditional branch has
two successor edges. Trace those instructions through the `isa<>` checks in
`StatsPass.cpp`. In LLVM 23, `CondBrInst` and `UncondBrInst` distinguish the
two branch forms directly; `isa<T>(I)` asks whether instruction `I` is a `T`.

**Exit criteria:** report is correct for 5 hand-written `.ll` files covering
if/else, loop, switch, recursion, and a function with PHIs. Cross-check one of
them against your own reading of the IR (that *is* the point of this task).

### 1.3 `CFGAnalyzer` — ~2.5 h
Goal: a reusable CFG representation for one function.

- For each function: block list, successors/predecessors, terminator kind
  per block, loop detection.
- Loop detection (sufficient for this project): a back edge is any branch edge
  `A → B` where `B` dominates `A` (use `DominatorTree` — you'll need to add
  `FAM.registerPass`/`PreservedAnalyses` plumbing; register
  `DominatorTreeAnalysis` via the analysis manager).
- Store results in a class with clean read-only accessors (const-correct).

**Pitfalls:**
- The analysis must be a **New PM `Analysis`** (own pass class returning a
  result struct) or it won't compose.
- Invalidate correctly: your analysis pass must not mutate IR; the flattening
  pass (Day 2) should return `PreservedAnalyses::none()` after restructuring
  unless it explicitly maintains particular analyses. Unchanged functions
  can return `PreservedAnalyses::all()`.

**Exit criteria:** CFG report (text dump: blocks, edges, loops, terminators)
verified by hand on the same 5 fixtures as 1.2.

### 1.4 `FunctionEligibility` — ~1.5 h
Goal: reject-unsafe-inputs-loudly. For each function, decide eligible/rejected
**with a `errs()` diagnostic naming the function and the reason**.

- Accept: functions whose terminators are only `br`, `condbr`, `switch`,
  `ret`, `unreachable`; (calls and all non-terminator instructions are fine).
- Reject (leave function **completely untouched**):
  - EH: `invoke`, `landingpad`, `resume`, functions with personality/`cleanup`
  - `indirectbr`
  - coroutines (`isCoroutine`)
  - blocks whose address is taken (labels used as values) — check with
    `BlockAddress` / `blockaddress` uses
  - (bonus, if easy) `musttail`/`nosync` subtleties can be deferred; document.

**Exit criteria:** each rejection case has a fixture `.ll`; running the pass
prints the diagnostic, IR is byte-identical (or at least `opt -verify` passes
and the function's blocks/terminators are unchanged), and the *success rate*
(metric you'll report on Day 3) can be computed.

**Day 1 exit:** plugin builds; `minishield-stats` + CFG report + eligibility
diagnostics all work via `opt`.

---

## Day 2 — The core: control-flow flattening
(~9–10 h. This is the heart of the project. Go slow, verify constantly.)

### 2.1 PHI demotion — ~1.5 h
- For each eligible function, call `DemotePHIToStack::runOnFunction(F)`
  (`<Transforms/Utils/Local.h>`) **before** restructuring.
- Understand *why* (be able to explain this in an interview): in SSA, a PHI
  merges values from its predecessors. After flattening, every block is
  reached only from the dispatcher (one predecessor), so PHI incomming edges
  no longer line up with control flow. Demoting to `alloca` + `store` (each
  predecessor stores) + `load` (block head) preserves the merged value
  regardless of entry path.
- Note where the allocas get created (entry block, before the first
  instruction) — plan the state variable around that.

**Exit criteria:** `opt ... -passes=minishield-flatten` on a PHI-heavy fixture
produces no PHI nodes (`grep -c "phi" out.ll` → 0) and passes `verify`.

### 2.2 State assignment + dispatcher (`StateMachineBuilder`) — ~3 h
- Assign each block a unique integer state (use the function's existing block
  order → deterministic, easy to test).
- Create the **dispatcher** as the new entry of the function:
  - state variable: `alloca i32` at the top (before PHI allocas — first
    instruction of entry), initialized to the state of the *original* entry
    block, then `br dispatcher`.
  - dispatcher body: `switch (load state) [default: <unreachable or the last
    state>]` with one arm per state → `br` to that block.
- **Chosen style: in-place flattening** (recommended over block-moving):
  original blocks stay where they are; you only (a) insert the dispatcher,
  (b) rewrite terminators (2.3). Block count goes N → N+1. Block-moving
  (creating fresh blocks and `moveBefore`-ing every instruction) is a common
  alternative — discuss the trade-off in the report, but implement in-place:
  fewer IRBuilder calls, less chance of breaking operand ordering.

**Pitfalls:**
- Insert the dispatcher **before** the original entry block
  (`EntryBlock->insertAfter(...)` / `BasicBlock::create` + insert at function
  front), and make the *original* entry block become "state 0" content — its
  instructions still execute exactly once, when state=0.
- `switch` default arm: unreachable is legal; pick one and be consistent.

**Exit criteria:** on the `calculate_discount` fixture, the transformed IR
shows: entry→dispatcher→switch→{state blocks}, one `alloca i32` state
variable, original blocks intact. Verifier passes.

### 2.3 Terminator rewriting — ~3 h
For each original block `B` (collect all terminators **first** — never mutate
while iterating instructions):

| Original terminator | Replacement |
|---|---|
| `br T` | `store stateOf(T) → state; br dispatcher` |
| `br C, A, B` | `ns = select C, stateOf(A), stateOf(B); store ns → state; br dispatcher` |
| `switch V, def D { ci: Ti }` | `ns = stateOf(D); for each case: ns = select(icmp eq V,ci, stateOf(Ti), ns); store; br dispatcher` |
| `ret`, `unreachable` | **unchanged** (terminal states — dispatcher never routes back) |

Use `IRBuilder` at the end of each block (`builder.SetInsertPoint(term)` then
`eraseFromParent()` the old terminator after building the replacement, or use
`ReplaceOpWith...` patterns consistently).

**Pitfalls (the ones that actually bite):**
- **Use-def chains:** the old terminator may be referenced (e.g. a PHI incoming
  — but you demoted those already; a `br` is rarely used, a `switch`'s
  condition is used by nothing after rewrite). If a terminator *is* used,
  replace rather than erase.
- **Iterator invalidation:** erase from the end backwards or collect-then-rewrite.
- **Operand ordering:** a `select`/`icmp` you insert must come after the
  values it uses (IRBuilder appends at insertion point — set it right).
- **Multiple returns:** fine — each `ret` stays terminal. The dispatcher's
  state space still covers them; they just never loop back.
- Don't touch `call` instructions, debug intrinsics (`!dbg`), or metadata.

**Exit criteria:** every fixture from Day 1 (if/else, nested, loop, switch,
multiple returns, PHI-heavy, recursion) transforms, passes `verify`, and the
rewritten terminators look like the table above in the dumped IR.

### 2.4 First real correctness check — ~1.5 h
- Compile `calculate_discount` C source two ways:
  1. original: `clang -O2 -o orig discount_test.c`
  2. protected: `clang -S -emit-llvm -O2 discount_test.c` → `opt
     -load-pass-plugin=... -passes=minishield-flatten -S` → `clang -O2` on the
     `.ll` → `prot`.
- Run both on a handful of inputs (levels 0..5 × amounts, negatives).
  **Identical outputs or you stop and debug.** (Always compare against the
  original at the *same* `-O` level — the spec's warning.)

**Day 2 exit:** `minishield-flatten` produces valid, behavior-preserving IR for
the full fixture set; CFG is visibly a dispatcher state machine.

---

## Day 3 — Tests, benchmarks, report, demo
(~8–9 h)

### 3.1 Test suite — ~3 h
- `tests/unit` (GoogleTest, link `GTest::gtest` + `GTest::gtest_main`,
  LLVM headers/libs):
  - eligibility: accept/reject on functions parsed from `.ll` text
    (`parseFunction`/`parseModule` from `AsmParser`);
  - CFG analysis: known edges/loops on synthetic functions;
  - flattening invariants on transformed IR: (a) `verifyModule` ok;
    (b) block count == original+1; (c) exactly one dispatcher block with a
    `switch` covering all states; (d) no original `br`/`condbr`/`switch`
    remains a terminator except allowed `ret`/`unreachable`; (e) state
    `alloca i32` exists.
- `tests/ir/`: the fixture `.ll`/`.c` files (the ones from Days 1–2, plus
  negatives: EH, indirectbr, coroutine).
- `tests/integration`: **differential executable test** (the one that
  distinguishes you): for each C fixture, build orig and protected at the same
  `-O2`, run both over N seeded-random inputs (write a tiny harness: the
  fixtures read inputs from argv/stdin, print results; a shell or C++ driver
  compares outputs over, e.g., 1000 random cases). Wire into CTest.

**Exit criteria:** `ninja test` all green; negatives prove rejection
(diagnostic + unchanged IR); a *mutated* test (break one invariant) fails
loudly — sanity-check that your tests actually test.

### 3.2 Benchmarks — ~2.5 h
- 4–6 benchmark programs (start: discount, factorial/fibonacci, string search,
  matrix multiply, insertion sort, a small stateful loop).
- Metrics per program: binary size (`size` or `wc -c`), wall-clock runtime
  (harness: call the hot function ~10⁶×, time both binaries, take median of
  3), #blocks and #branches (your `minishield-stats`), compile time
  (time the C→IR→flatten→binary pipeline vs plain), success rate
  (from 1.4, over a small corpus of extra functions).
- Write `benchmarks/results/report.md` in the spec's table format
  (Original / Protected columns). A one-paragraph *analysis*: flattening
  adds structural complexity; overhead is the dispatcher hop per block;
  **state clearly that flattening is a speed bump, not a guarantee**.

**Exit criteria:** table filled with real numbers (never illustrative ones);
reproducible via one command (document it).

### 3.3 README + technical report + 5-minute demo — ~2.5 h
- `README.md`: what it is, architecture (ASCII diagram matching the spec),
  build (conda env + the CMake line), running the pass, running tests,
  running benchmarks, **limitations** (no EH, no indirectbr, no coroutines,
  labels; debug-info untouched — note the state variable adds one register/
  stack slot; in-place style choice).
- Technical report section (in README or `REPORT.md`): design decisions
  (why in-place, why PHI demotion, eligibility philosophy = *reject loudly,
  never transform incorrectly*), the benchmark table, and the trade-off
  discussion.
- `scripts/demo.sh` — the 5-minute demo, in this order:
  1. show `calculate_discount.c`;
  2. show original IR (`clang -S -emit-llvm -O2 | less`/`cat`);
  3. run MiniShield, show transformed IR (highlight the dispatcher + switch);
  4. run both binaries on the same inputs, diff the outputs (empty diff);
  5. print the benchmark table.
- **Stretch (only if all of the above is done):** the simulated customer bug
  report ("protected app crashes only at -O2") — build a minimal reproducer,
  compare IR at -O0 vs -O2, find the transformation/optimizer interaction, add
  a regression test, document root cause. This mirrors the actual support
  workflow from the job description.

**Day 3 exit:** `ninja test` green, benchmark report real, `demo.sh` runs
start-to-finish unattended, README explains everything a stranger needs.

---

## Standing rules (all 3 days)

1. **One release only** — everything against conda `minishield` LLVM 23.1.5.
2. **Verifier after every change** — `opt ... -passes=minishield-flatten,verify`
   (or `verifyModule` in-process). Broken IR is never "debugged later".
3. **Differential testing is the source of truth** — if orig and protected
   differ on any input in your test domain, the transform is wrong, full stop.
4. **Reject loudly, never transform incorrectly** — any unsupported construct
   gets a named diagnostic and an unchanged function.
5. **Be able to explain every line of the transform** — no black-box code; if
   you can't explain an API call's effect on use-def chains, read its docs
   first.
6. Keep each class small: eligibility decides, CFGAnalyzer describes,
   StateMachineBuilder builds, FlatteningPass orchestrates (eligibility →
   PHI demotion → build → verify).

## Reference (official, in priority order)
- LLVM: *Writing an LLVM Pass* (New PM + plugin section) — primary reference.
- LLVM: *New Pass Manager* / `PassBuilder`, `PreservedAnalyses`.
- `DemotePHIToStack` / `Local.cpp` source — read before 2.1.
- Kaleidoscope tutorial — only if you need a refresher on IRBuilder.
