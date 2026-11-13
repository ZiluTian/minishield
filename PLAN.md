# MiniShield — 3-Day Plan

LLVM-based control-flow-flattening pass plugin. Working environment is **ready**
(see "Environment" below). You write the code; this file is the roadmap: tasks,
pitfalls, and a verifiable *exit criteria* for every task.

## Progress (2026-11-12)

| Milestone | Status |
|---|---|
| Environment and CMake | Plugin builds against LLVM 23.1.5 |
| Volume 1 foundations | Statistics, CFG/loop analysis, and eligibility implemented during study |
| Volume 2 flattening | Learner implementation in progress; complete book draft available |
| Volume 3 hardening crash course | Complete book draft; learner exercises and measurements pending |

**Current priority:** finish the books before resuming hands-on lessons.
[Volume 2](https://zilutian.github.io/minishield/#day2) documents preparation,
dispatcher construction, complete branch rewriting, correctness checks, and the
testing, measurement, and delivery chapters that close the project.
[Volume 3](https://zilutian.github.io/minishield/#day3) is a crash course on the
hardening techniques flattening leaves out — CFI, stack canaries, OLLVM-style
obfuscation, and position independence. Reading a chapter does not complete its
implementation or establish its expected results.

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
  against the LLVM dylib (see Volume 1, Task 1.1).
- `opt` writes the transformed module to **stdout** by default — always pass
  `-S` (text IR) or `-o out.ll`.
- **Deviation from spec (accepted):** conda-forge does not ship `FileCheck`/`not`/
  `count` for LLVM 23. IR-level assertions are written in **C++/GoogleTest**
  using LLVM's own APIs (`verifyModule`, `DT`, block/terminator inspection) —
  stronger than text-matching, and matches the spec's GoogleTest requirement.

---

## Volume 1 — Foundations: plugin skeleton, IR stats, CFG analysis, eligibility
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
Goal: the "IR inspection pass" of Phase 1, doubled as your stats tool for the
Volume 2 measurement chapters.

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
  pass (Volume 2) should return `PreservedAnalyses::none()` after restructuring
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
  - The complete Volume 2 prototype rejects special call semantics such as
    `musttail`, `returns_twice`, convergence, and operand bundles before mutation.
    See its stricter support contract; the Volume 1 inspection guard is narrower.

**Exit criteria:** each rejection case has a fixture `.ll`; running the pass
prints the diagnostic, IR is byte-identical (or at least `opt -verify` passes
and the function's blocks/terminators are unchanged), and the *success rate*
(metric you'll report in the Volume 2 measurement chapters) can be computed.

**Volume 1 exit:** plugin builds; `minishield-stats` + CFG report + eligibility
diagnostics all work via `opt`.

---

## Volume 2 — The core: control-flow flattening
(~9–10 h. This is the heart of the project. Go slow, verify constantly.)

### 2.1 PHI demotion — ~1.5 h
- After strict preflight, collect `PHINode*` values, then call the free
  function `llvm::DemotePHIToStack(phi)` for each (`llvm/Transforms/Utils/Local.h`).
  The helper erases the PHI; do not dereference that pointer afterward.
- Collect non-void, non-alloca instruction results used outside their blocks,
  then call `llvm::DemoteRegToStack(*I)` before changing the CFG.
- Understand *why* (be able to explain this in an interview): in SSA, a PHI
  merges values from its predecessors. After flattening, every block is
  reached only from the dispatcher (one predecessor), so PHI incoming edges
  no longer line up with control flow. Demoting to `alloca` + `store` (each
  predecessor stores) + `load` (block head) preserves the merged value
  regardless of entry path.
- Note where the allocas get created (entry block, before the first
  instruction) — plan the state variable around that.

**Exit criteria:** `opt ... -passes=minishield-flatten` on a PHI-heavy fixture
produces no PHI nodes (`grep -c "phi" out.ll` → 0) and passes `verify`.

### 2.2 State assignment + dispatcher (`StateMachineBuilder`) — ~3 h
- Preserve the original entry as one-time setup. Reject non-static allocas
  and other unsupported constructs before any preparation or mutation.
- Assign deterministic state IDs to the prepared non-entry blocks only.
- Allocate `i32` state storage in entry; its original terminator chooses and
  stores the initial successor state before branching to dispatch.
- Append a dispatcher loading that slot and switching to each non-entry block.
  Append a distinct invalid-state block ending in `unreachable`.
- This in-place builder adds **two** blocks: N → N+2, where N is measured
  **after preparation** (demotion may split edges). Snapshot original
  terminators before adding either block.
- Rewrite original transitions as in 2.3, including the entry transition.
  Keep returns and unreachable terminal. Never rewrite the new dispatcher.
- `unreachable` is an invariant, not error recovery; every actual dispatch
  must follow a valid state store. Preserve entry storage dominance.

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
- Collect original terminators before rewriting; erase each only after reading
  its operands and constructing the replacement. Do not use an erased pointer.
- Insert comparisons/selects after their operands and before the old terminator.
- Preserve return/unreachable instructions. In a C++ opcode switch inside a
  loop, use `continue` for terminal cases to skip a shared store/branch tail.
- New transition instructions inherit the old terminator’s debug location.
  Do not blindly copy metadata whose control-flow meaning changed. The strict
  prototype rejects explicit intrinsic calls; full debug/profile preservation
  is outside its support promise.

**Exit criteria:** every fixture from Volume 1 (if/else, nested, loop, switch,
multiple returns, PHI-heavy, recursion) transforms, passes `verify`, and the
rewritten terminators look like the table above in the dumped IR.

### 2.4 First real correctness check — ~1.5 h
- Compile the kernel alone once to common IR with
  `clang -O0 -Xclang -disable-O0-optnone -S -emit-llvm`.
- Transform that IR, then compile original and protected variants with the
  same `-O2` backend and the same untransformed driver. See Volume 2 lesson 24
  for full source and commands.
- Compare successful exit, stdout, and stderr over the documented defined
  domain. Include every branch/switch outcome and record the failing input.
- Inspect final optimized code: later optimization may simplify dispatch.
  A behavior match does not prove that obfuscation structure survived.

**Volume 2 exit:** `minishield-flatten` produces valid, behavior-preserving IR for
the full fixture set; CFG is visibly a dispatcher state machine.

The test suite, benchmark, and demo plans that used to close the project now live in
Volume 2 as the testing chapters (DESIGN → DELIVER): the GoogleTest unit tests,
the CTest integration wiring, the differential runner, the measurement design,
and the reproducible demo.

---

## Volume 3 — Code hardening beyond flattening
(crash course)

MiniShield has implemented one hardening technique — control-flow flattening,
a member of the obfuscation family. Volume 1's capstone lesson established
that the plugin's seams are technique-agnostic and host other techniques as
named passes. This volume is a crash course on the techniques flattening
leaves out, taught through concrete LLVM 23.1.5 examples:

- Threat model: what each family answers (reverse engineering vs
  control-flow hijack vs control-data corruption vs predictable memory
  layout) and what "hardening quality" means — what survives, at what
  cost, in the final artifact.
- Control-flow integrity: `llvm.cfi_icheck`, forward and backward CFI —
  read the IR clang generates, verify the check at runtime.
- Stack canaries: `llvm.stackprotector`, canary placement, what it
  catches and what it misses.
- OLLVM family — the learner implements each as a new MiniShield pass and
  proves it with the Volume 2 differential method:
  - bogus control flow: dead branches under a secret condition;
  - string encryption: plaintext out of the binary, decrypt at use;
  - subroutine splitting: jump-table split of a function.
- Position independence, ASLR, RELRO: the hardening that lives in the
  linker/loader, not the IR.
- Persistence: what -O2 keeps and what it removes — the obfuscation
  failure mode Volume 2's exit evidence already showed.
- Final lesson: fuzz one of the learner's own passes (behavior must stay
  identical).

**Volume 3 exit:** the three OLLVM passes build into the plugin and pass
differential tests on the shared fixtures; the CFI, canary, and PIE
lessons are verified against the toolchain's real output; one technique's
overhead is measured with the Volume 2 method; the fuzzer reports no
behavioral regression.

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
   PHI and escaping-value demotion → build → verify).

## Reference (official, in priority order)
- LLVM: *Writing an LLVM Pass* (New PM + plugin section) — primary reference.
- LLVM: *New Pass Manager* / `PassBuilder`, `PreservedAnalyses`.
- `DemotePHIToStack` / `Local.cpp` source — read before 2.1.
- Kaleidoscope tutorial — only if you need a refresher on IRBuilder.
