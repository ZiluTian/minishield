# MiniShield

An LLVM-based code-hardening engine: a loadable pass plugin that flattens a
function's control-flow graph into a dispatcher-based state machine to make
reverse engineering harder, while provably preserving program behavior.

Built against a single LLVM release (conda-forge LLVM 23.1.5) using the New
Pass Manager. Project roadmap and day-by-day tasks: see [PLAN.md](PLAN.md).

---

## Configure and build

From the project root, activate the environment and configure the build:

```bash
conda activate minishield
export LIBRARY_PATH="$CONDA_PREFIX/lib"

cmake -G Ninja -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER="$CONDA_PREFIX/bin/clang++-23" \
  -DLLVM_DIR="$CONDA_PREFIX/lib/cmake/llvm"
```

This is CMake's **configure/generate step**: it reads `CMakeLists.txt`, finds
LLVM, and generates the instructions Ninja will execute.

| Option | Meaning |
|---|---|
| `-G Ninja` | Select Ninja as the build system |
| `-S .` | Read `CMakeLists.txt` from the current directory |
| `-B build` | Write generated files, including `build.ninja`, into `build/` |
| `-DCMAKE_BUILD_TYPE=Release` | Select a release build |
| `-DCMAKE_CXX_COMPILER=…` | Use the environment's Clang C++ compiler |
| `-DLLVM_DIR=…` | Locate the environment's LLVM CMake configuration |

After CMake reports **"Generating done"**, compile and link the plugin:

```bash
cmake --build build
```

The output is `build/libMiniShield.so`. For later source edits, run the build
command again. In a new shell, activate the environment and export
`LIBRARY_PATH` again before building.

If building reports `ninja: error: loading 'build.ninja': No such file or
directory`, the configure/generate step has not completed successfully.
Run the configuration command above and resolve any errors it reports before
retrying the build. A `build/CMakeCache.txt` file alone does not mean CMake
finished generating the build instructions.

### Verify the plugin

`ninja: no work to do` means the build is already up to date. The repository
includes a small LLVM IR input at
[`tests/ir/minishield-input.ll`](tests/ir/minishield-input.ll).
With the `minishield` environment activated, run from the project root:

```bash
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -S tests/ir/minishield-input.ll \
  -o build/minishield-output.ll
```

The current diagnostic stub should print:

```text
[MiniShield] function: add_one, blocks: 1
```

This confirms that the plugin loads, recognizes the pass name, and executes
`run()`. The `verify` pass checks LLVM IR's structural rules after the pass;
it does not prove equivalent program behavior. `-S` writes text IR, and `-o`
selects the output file.

Inspect the result with:

```bash
cat build/minishield-output.ll
```

The current pass only prints statistics, so the output should contain the
same function instructions. This checks the plugin plumbing; it does not
test a flattening transformation yet.

### Inspect function statistics (task 1.2)

**Status:** the statistics pass is the next implementation task. The current
plugin only registers `minishield-flatten`; the fixtures below are ready for
you to use while writing the pass and its test scripts.

Implement it in these steps:

1. Declare a function pass in `include/minishield/StatsPass.h` and implement
   `run()` in `lib/StatsPass.cpp`. Use `RequiredPassInfoMixin<StatsPass>` so
   inspection also runs on functions marked `optnone`.
2. Visit each `BasicBlock` in the function, then each `Instruction` in the
   block. The function pass manager already handles visiting functions.
3. Use `isa<T>(I)` to classify instructions. LLVM 23 provides `CondBrInst`,
   `UncondBrInst`, `SwitchInst`, `PHINode`, `ReturnInst`, `CallInst`,
   `InvokeInst`, and `IndirectBrInst`. Include `llvm/IR/Instructions.h` and
   `llvm/Support/Casting.h`.
4. Print one report per function definition to `llvm::errs()`. Skip
   declarations. Do not change IR; return `PreservedAnalyses::all()`.
5. Add `lib/StatsPass.cpp` to the existing CMake target and register
   `minishield-stats` in `Plugin.cpp` using the function pipeline callback.

After implementing and rebuilding, run:

```bash
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-stats),verify' \
  -disable-output tests/ir/phi.ll
```

Suggested output format (the counts are the expected result):

```text
[MiniShield stats] function=merge blocks=4 branches=3 cond_br=1 uncond_br=2 switches=0 phis=1 returns=1 calls=0 invokes=0 indirectbr=0 loops=deferred
```

`branches` counts `br` instructions, split into conditional and unconditional
forms. `switch` and `indirectbr` are counted separately. `calls` counts `call`
instructions, including recursive and indirect calls, while `invokes` counts
`invoke` instructions separately. These are static instruction counts, not
runtime execution counts. Loop counting is deferred to CFG analysis in task
1.3; print `loops=deferred` until then.

The fixtures in `tests/ir/` have these hand-counted expectations. Total
`branches` is conditional plus unconditional `br`; it excludes `switch` and
`indirectbr`.

| Fixture / function | Blocks | Cond. br | Uncond. br | Switches | PHIs | Returns | Calls | Invokes | Indirectbr |
|---|---|---|---|---|---|---|---|---|---|
| `minishield-input.ll` / `add_one` | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| `if-else.ll` / `choose` | 3 | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| `loop.ll` / `count_to` | 4 | 1 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| `switch.ll` / `select_case` | 4 | 0 | 0 | 1 | 0 | 3 | 0 | 0 | 0 |
| `recursion.ll` / `factorial` | 3 | 1 | 0 | 0 | 0 | 2 | 1 | 0 | 0 |
| `phi.ll` / `merge` | 4 | 1 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| `instruction-kinds.ll` / `with_invoke` | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| `instruction-kinds.ll` / `with_indirectbr` | 3 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 1 |
| `instruction-kinds.ll` / `without_optimization` | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

`instruction-kinds.ll` also contains declarations that should not produce
reports. Its `without_optimization` function has `optnone` and should still
produce a report.

As a manual cross-check, open `phi.ll`: `entry` has one conditional branch;
`left` and `right` each have one unconditional branch; `join` has one PHI
and one return. That gives four blocks and three branch instructions.

You can validate any fixture independently of the plugin:

```bash
opt -passes=verify -disable-output tests/ir/phi.ll
```

Once the stats pass is implemented, confirm that inspection leaves the IR
unchanged by comparing canonical output with and without the pass:

```bash
opt -passes=verify -S tests/ir/phi.ll -o build/phi-before.ll
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-stats),verify' \
  -S tests/ir/phi.ll -o build/phi-after.ll
diff -u build/phi-before.ll build/phi-after.ll
```

An empty diff is expected. Apply the same count and unchanged-IR checks to
all fixtures when you write the test scripts. See task 1.2 in [the plan](PLAN.md)
for the milestone's exit criteria.

## Build-system notes

### Why `find_package(LLVM REQUIRED CONFIG)`?

`find_package(<name>)` can locate a package in two different ways, and the
`CONFIG` keyword selects which:

| | Without `CONFIG` (module mode, default) | With `CONFIG` |
|---|---|---|
| File it hunts for | `FindLLVM.cmake` | `LLVMConfig.cmake` (or `llvm-config.cmake`) |
| Who wrote it | A CMake community contributor, shipped **inside CMake itself** | The **LLVM package author**, shipped *with the package* (e.g. `$CONDA_PREFIX/lib/cmake/llvm/` for the conda-forge `llvmdev` package) |
| How it works | A hand-maintained script that probes paths and compilers | Declares the exact truth about *this build*: imported targets (the `LLVM` dylib target), variables (`LLVM_INCLUDE_DIRS`, `LLVM_DEFINITIONS`, `LLVM_PACKAGE_VERSION`), and helpers (`llvm_map_components_to_llvmlib`) |
| For LLVM specifically | Nothing to find — CMake ships ~162 `Find*.cmake` modules and **no** `FindLLVM.cmake` | Works: the config file is installed with the LLVM package |

So `find_package(LLVM REQUIRED CONFIG)` means: *"the package name is `LLVM`;
don't look for a CMake-contributed finder script — find the configuration file
that the installed LLVM package ships."*

**How the search resolves** (config mode), in priority order:

1. `LLVM_DIR` — a variable named after the package + `_DIR`. This build passes
   `-DLLVM_DIR=$CONDA_PREFIX/lib/cmake/llvm`, which is the top-priority hint
   and removes all ambiguity.
2. `CMAKE_PREFIX_PATH` (if set).
3. System prefixes (`/usr/local`, `/usr`, …), probing subpaths such as
   `<prefix>/lib/cmake/llvm` and `<prefix>/share/cmake/llvm`.

**The three "package" layers** — the same word does three jobs here:

```
conda package   "llvmdev"          → the distribution unit on disk (what was installed)
CMake package   "LLVM"             → the logical contract: "I want to consume LLVM"
config file     "LLVMConfig.cmake" → the file that fulfills the contract (what CONFIG selects)
```

`find_package(LLVM ...)` names the **CMake** package; `CONFIG` selects the
**file** that answers for it; the conda package is just the delivery
mechanism that installed that file.

**Rule of thumb:** if the vendor ships a `FooConfig.cmake`, use
`find_package(Foo CONFIG)`. Find-modules are for ancient libraries that
predate config files. Config files are maintained by the people who *built*
the library, so they're accurate for that exact build (correct C++ standard,
component list, dylib imported targets); community Find-modules are often
years behind, and for LLVM they don't exist at all.

### Do the two search modes affect artifact size or rebuild time?

**No — the search mode is a pure discovery mechanism.** `find_package` is a
*finder*, not a *builder*: it runs once at configure time and only fills in
variables and imported targets (`LLVM_INCLUDE_DIRS`, `LLVM_DEFINITIONS`, the
`LLVM` imported target, …). Whichever mode supplies those, the same
downstream decisions are made by the same `add_llvm_library` /
`target_link_libraries` calls:

```
find_package (module mode) ─┐
                            ├─► same variables / imported targets ─► same flags ─► same link line ─► identical .so
find_package (config mode)  ┘
```

If a `FindLLVM.cmake` existed and pointed at the *same* installation that
`LLVMConfig.cmake` points at, the result would be byte-identical: same
include dirs, same definitions, same `libLLVM-23.so` on the link line — no
recompilation, no size change. The mode only becomes visible if the two routes
disagree about *which* LLVM they find; then the difference comes from
different installations, not from the mode.

The three axes, kept separate:

| Axis | What it decides | Affects artifact size? | Forces recompilation? |
|---|---|---|---|
| **Search mode** (module vs config) | *how* CMake locates the package's metadata | No | No |
| **Which installation** is found (e.g. conda 23.1.5 vs anything else) | headers, ABI, `LLVM_DEFINITIONS` | No | Yes — different headers/ABI → our sources recompile |
| **Link strategy** (dylib vs static; see below) | whether LLVM code lives *in* our `.so` | **Yes** — tens of KB vs hundreds of MB | No (link-time only) |

So: **mode = discovery, installation = compatibility, link strategy = size.**
`CONFIG` buys nothing in bytes or build time — it buys *correctness and
determinism* (the package author's own truth about their build, and for LLVM
the only route that exists at all).

### Where does the size go? (`MODULE` + dylib linking)

Measured in this environment (conda-forge LLVM 23.1.5):

- `libLLVM.so.23.1` (the shared library): **188 MB** — prebuilt, already loaded by `opt`
- the static component archives (`libLLVMCore.a`, `libLLVMPasses.a`, …): **363 MB total**

The small-plugin outcome comes from the **`MODULE` + dylib-linking**
combination, not from the `find_package` mode:

- **This project:** `MiniShield` is built as a `MODULE` (a `dlopen()`-able
  `.so` containing *only* our ~5 `.cpp` files — tens of KB). With
  `LLVM_LINK_LLVM_DYLIB ON`, every LLVM symbol resolves **at load time** from
  the *same* `libLLVM-23.so` that `opt` uses — one LLVM in the process.
- **Static alternative** (linking the component archives): those symbols are
  copied into our `.so` → it bloats toward hundreds of MB, *and* you get
  duplicate-LLVM-in-one-process corruption (two sets of globals), *and* every
  relink re-copies that pile. Bigger and wrong, not smaller and safer.
- **`SHARED` vs `MODULE`:** on Linux they produce nearly identical `.so`
  files — the difference is contractual, not mechanical. Details in the next
  section.

Recompilation story: editing MiniShield code → recompile 5 files, relink a
small `.so` (seconds). Switching LLVM releases → recompile our files against
the new headers. We never compile LLVM itself (hours/days) — consuming the
prebuilt 188 MB shared library is the point. You can't hot-swap the LLVM `.so`
under a running `opt`, so versions must match: **one release only.**

### What does `add_library` do?

`add_library(<name> [STATIC | SHARED | MODULE] [EXCLUDE_FROM_ALL] <srcs>…)`
creates a **library target**: a named node in CMake's build graph carrying
sources, compile/link rules, and the *usage requirements* attached by the
`target_*` commands (below). The type keyword sets the artifact and its
contract (Linux):

| Type | Artifact | Contract | Other targets may link it? |
|---|---|---|---|
| `STATIC` | `libX.a` (object archive) | code is *copied into* each consumer at its link time | yes — every consumer embeds its own copy (how you get "two LLVMs in one process") |
| `SHARED` | `libX.so` with a soname | *linked against* at build time; consumers record a `DT_NEEDED` entry | yes |
| `MODULE` | `libX.so` | *loaded at runtime* via `dlopen()` — a plugin, not a dependency | **no** — CMake refuses to link a MODULE into another target |

**Why `MODULE` for MiniShield:** the relationship between `opt` and the
plugin is `dlopen()` at runtime — a load-time, not link-time, relationship.
Nothing ever *links against* MiniShield, so `STATIC` is out (an archive is
not a loadable image) and `SHARED`, while mechanically near-identical on
Linux, would declare a "you may link me" relationship that doesn't exist.
`MODULE` declares the plugin contract — which is also why all link scopes
are `PRIVATE`.

Mechanically, for a real target
(`add_library(MiniShield MODULE lib/Plugin.cpp lib/FlatteningPass.cpp)`):

1. one **compile rule per source** → `build/CMakeFiles/MiniShield.dir/…o`,
   compiled with the target's standard, definitions, and include dirs;
2. one **archive/link rule** → the artifact, by default named
   `libMiniShield.so` (default `lib` prefix) at the build root — pinned
   explicitly by `LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}`;
3. the **target node** itself, which `ninja -C build` builds and the
   `target_*` commands attach properties to.

**The same command has a second role — describing things you do *not*
build.** `LLVMConfig.cmake` line 1775 contains:

```cmake
add_library(LLVM SHARED IMPORTED)
```

An *imported* target builds nothing; it is pure metadata describing an
existing binary (`libLLVM-23.so`: location, soname, link interface).
`target_link_libraries(MiniShield PRIVATE LLVM)` links against that
description, resolved to the real `.so` at link time. One command, two
directions:

```
add_library(MiniShield MODULE …)   producer:  "build this artifact from these sources"
add_library(LLVM SHARED IMPORTED)  consumer:  "here is an existing .so, its properties are…"
```

(`add_llvm_library` — unavailable here, see below — was simply LLVM's
in-tree wrapper around `add_library` with extra LLVM build plumbing; plain
`add_library` is the correct consumer-side replacement.)

### What do `target_include_directories`, `target_link_libraries`, and `set_target_properties` do?

These commands configure the `MiniShield` target created by `add_library`.
Compilation and linking happen later, when the build runs.

**`target_include_directories` — where to find headers.**

```cmake
target_include_directories(MiniShield PRIVATE
    ${LLVM_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
```

This adds LLVM's header directories and this project's `include/` directory
to MiniShield's compiler search paths (typically through `-I` options).
It lets source files include LLVM and project headers; it does not link
LLVM's compiled implementation. `PRIVATE` applies these paths to MiniShield
without exposing them as requirements for consumers.

**`target_link_libraries` — which libraries to link.**

```cmake
target_link_libraries(MiniShield PRIVATE LLVM)
```

`LLVM` is an imported target supplied by `find_package(LLVM REQUIRED CONFIG)`.
CMake uses its metadata to locate the existing LLVM shared library and
construct MiniShield's link command. Target dependencies can also contribute
usage requirements, such as include paths and compile definitions.
Here, shared linking records a runtime dependency on LLVM instead of copying
LLVM's implementation into the plugin. `PRIVATE` keeps LLVM out of
MiniShield's public link interface.

**`set_target_properties` — configure named settings on the target.**

```cmake
set_target_properties(MiniShield PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
```

The general form is `set_target_properties(<targets> PROPERTIES <name> <value>…)`.
Here, `LIBRARY_OUTPUT_DIRECTORY` chooses where to write the built module;
`${CMAKE_BINARY_DIR}` is the top-level build directory. Configuring with
`cmake -S . -B build` and building with Ninja therefore produces
`build/libMiniShield.so`. This changes the destination, not the filename or
link dependencies. Multi-configuration generators may append a configuration
subdirectory such as `Debug/`.

### Why target-scoped `target_*` instead of `add_definitions` / `include_directories`?

You'll find the classic LLVM-consumer snippet in older docs and tutorials:

```cmake
separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})
include_directories(${LLVM_INCLUDE_DIRS})
```

It *works*, but both `add_definitions(...)` and `include_directories(...)` are
**directory-global**: they apply to *every* target defined in that directory
(and subdirectories, until overridden) — your pass, and every test or tool you
add later. The modern style is **target-scoped**, i.e. each target declares
its own requirements:

```cmake
separate_arguments(MS_LLVM_DEFS NATIVE_COMMAND ${LLVM_DEFINITIONS})
target_compile_definitions(MiniShield PRIVATE ${MS_LLVM_DEFS})
target_include_directories(MiniShield PRIVATE
    ${LLVM_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
```

Why prefer target scope:

- **No leakage.** Flags and include paths attach to the target that actually
  needs them; future targets (Day-3 test binaries, benchmark harnesses) start
  from a clean slate instead of inheriting LLVM's definitions by accident.
- **Explicit dependency graph.** A target's requirements are readable on the
  target itself, which is exactly what CMake's *usage requirements* model
  (`PRIVATE` / `PUBLIC` / `INTERFACE`) is built around.

The scope keywords, for reference:

| Keyword | Affects this target's own compilation | Affects consumers linking to it |
|---|---|---|
| `PRIVATE` | yes | no |
| `PUBLIC` | yes | yes (and re-exports transitively) |
| `INTERFACE` | no | yes |

`MiniShield` is a `MODULE` (a `dlopen()`-able `.so` that nothing links to), so
everything is `PRIVATE`.

Two more details from that snippet worth keeping:

- `separate_arguments(... NATIVE_COMMAND ...)` does **real work** here:
  `LLVMConfig.cmake` sets `LLVM_DEFINITIONS` as a single *space-joined
  string* (e.g. `"-D_GNU_SOURCE -D__STDC_FORMAT_MACROS ..."`), not a CMake
  list, so it must be split into individual `-D` flags before use. The
  `NATIVE_COMMAND` flag is a Windows relic; on Linux it's a harmless no-op.
- The tutorial's `add_subdirectory(<pass name>)` is a *layout* choice (one
  subdirectory per pass/chapter), not a linking mechanism. This project uses a
  single top-level `CMakeLists.txt` and adds exactly one subdirectory later:
  `tests/`, for the standard CTest/GoogleTest setup.

### What does `separate_arguments` do?

CMake has no array type: a "list" is a string whose elements are separated
by `;`. Two distinct representations therefore exist for "several things":

```cmake
set(X a b c)                    # stored as "a;b;c" — a 3-element list
set(Y "a b c")                  # stored as ONE element containing spaces
```

`LLVMConfig.cmake` defines `LLVM_DEFINITIONS` with the *second* form — one
quoted, space-joined string (line 367):

```
"-D_GNU_SOURCE -D_GLIBCXX_USE_CXX11_ABI=1 -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS"
```

so it is a **1-element** "list". Passed as-is to
`target_compile_definitions`, CMake would emit it as a *single*
shell-quoted compiler argument — one giant "macro name" containing spaces and
`=` — which the compiler rejects. What the compiler needs is separate
`-D…` arguments.

`separate_arguments(<out> <mode> <in>)` fixes the representation by splitting
on unquoted whitespace:

```
before:  1 element(s) → '-D_GNU_SOURCE -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS'
after:   3 element(s) → -D_GNU_SOURCE;-D__STDC_FORMAT_MACROS;-D__STDC_LIMIT_MACROS
```

The second argument selects the *quoting rules* used while splitting — it
only matters when the string contains escaped quotes (CMake's internal
command-line representation uses `\"`):

| Mode | Rules applied |
|---|---|
| `NATIVE_COMMAND` (default) | conventions of the machine CMake runs on (Linux → Unix rules) |
| `UNIX_COMMAND` | always Unix rules |
| `WIN32_COMMAND` | always Windows rules (for strings captured from a Windows command line) |

With a quote-free string on Linux, all three behave identically, so
`NATIVE_COMMAND` is just the portable default (and what the canonical LLVM
docs snippet uses).

**When you need it:** only when a variable is a *space-joined string* rather
than a CMake list. Variables you create yourself (`set(X a b c)`) are already
proper lists; `LLVM_DEFINITIONS` is the exception because the package author
wrote it as one quoted string. Rule of thumb: before using a string *as a
list* (foreach, `target_*` call, command arguments), know which of the two
representations you're holding.

### Known environment quirks (conda-forge LLVM 23.1.5)

Verified against this environment; each of these bit the actual build:

- **No `LLVM.cmake` / `AddLLVM.cmake` in the installed package.**
  `include(LLVM)` finds nothing useful and `add_llvm_library` /
  `llvm_map_components_to_llvmlib` are unavailable — they are part of LLVM's
  *in-tree* build infrastructure, not the installed package's CMake API.
  `LLVMConfig.cmap` does the dylib wiring itself (`set(LLVM_LINK_LLVM_DYLIB
  yes)` and `add_library(LLVM SHARED IMPORTED)` → `libLLVM-23.so`), so the
  correct consumer pattern is plain CMake:
  `add_library(MiniShield MODULE ...)` +
  `target_link_libraries(MiniShield PRIVATE LLVM)`.
- **No plain `clang++` in the env** — only `clang` and `clang++-23`. Pin the
  compiler explicitly: `-DCMAKE_CXX_COMPILER=$CONDA_PREFIX/bin/clang++-23`
  (`$(which clang++)` is empty and silently falls back to the system g++).
- **`LIBRARY_PATH` is required for conda's clang at link time.**
  `export LIBRARY_PATH=$CONDA_PREFIX/lib` — the driver's `-L` search paths are
  the gcc-layout dirs and the sysroot, and do *not* include `$PREFIX/lib`
  where the `libstdcxx` package installed `libstdc++.so`; without it the
  link fails with `x86_64-conda-linux-gnu-ld: cannot find -lstdc++`.
- **Cosmetic warnings are expected.** `LLVMConfig.cmake` probes optional
  dependencies and prints `Could NOT find ZLIB / LibXml2 / zstd`. They're
  harmless for a pass plugin: those libraries are already inside the shared
  `libLLVM-23.so`.

## Pass implementation notes

### Start a reusable CFG analysis (task 1.3)

A control-flow graph (CFG) treats basic blocks as nodes and possible control
transfers as edges. A block's **successors** are its possible destinations;
its **predecessors** are blocks that can transfer control to it.

For `tests/ir/phi.ll`, the graph is:

```text
entry -> left right
left  -> join
right -> join
join  ->
```

`join` has no successors because it ends with `ret`. The three branch
instructions create four edges: the conditional branch contributes two.
LLVM's `llvm/IR/CFG.h` provides `llvm::successors(&BB)` and
`llvm::predecessors(&BB)` for traversing those connections.

The statistics pass prints information. A reusable `CFGAnalyzer` analysis
should instead **return information** for other passes to consume.

| Kind | What `run()` returns |
|---|---|
| Transformation or printing pass | `llvm::PreservedAnalyses`, describing which cached analyses remain valid |
| Analysis | Its computed `Result`, which the analysis manager can cache |

**Header exercise:** create `include/minishield/CFGAnalyzer.h` yourself:

1. Add `#pragma once` and include `llvm/IR/PassManager.h`,
   `llvm/IR/BasicBlock.h`, and `<vector>`.
2. Inside `namespace minishield`, declare `CFGAnalyzer` with public
   inheritance from `llvm::AnalysisInfoMixin<CFGAnalyzer>`.
3. Add this public nested structure for one block:

   ```cpp
   struct BlockInfo {
       const llvm::BasicBlock *block;
       std::vector<const llvm::BasicBlock *> successors;
       std::vector<const llvm::BasicBlock *> predecessors;
   };
   ```

4. Add the public result structure:

   ```cpp
   struct Result {
       std::vector<BlockInfo> blocks;
   };
   ```

5. Declare the public analysis method:

   ```cpp
   Result run(
       llvm::Function &F,
       llvm::FunctionAnalysisManager &AM);
   ```

6. Add these private members:

   ```cpp
   friend llvm::AnalysisInfoMixin<CFGAnalyzer>;
   static llvm::AnalysisKey Key;
   ```

`AnalysisKey` gives the analysis a unique identity. The friend declaration
lets LLVM's mixin access that private key. Its definition belongs in the
future `lib/CFGAnalyzer.cpp` implementation.

These pointers refer to blocks owned by the function; the result does not
own or copy them. Consumers must respect analysis invalidation when IR
changes. This first exercise only declares the interface. Implementation,
registration with the function analysis manager, terminator information,
and loop detection follow after the basic graph works.

### References, pointers, and addresses in CFG traversal

In this loop, `BB` is a **reference** to an existing block, not a pointer:

```cpp
for (const llvm::BasicBlock &BB : F) {
    // BB is another name for the block; access members with BB.getName().
}
```

A reference acts as another name for an object. A pointer holds an object's
address. Since `BlockInfo::block` is declared as
`const llvm::BasicBlock *block`, assign it the referenced block's address:

```cpp
info.block = &BB;
```

`&BB` obtains the address of the existing block; it does not copy the block
or create a separate object representing the reference. The `&` symbol has
different meanings in a declaration and an expression:

| Syntax | Meaning |
|---|---|
| `const llvm::BasicBlock &BB` | Declare a reference to a block |
| `&BB` | Obtain the address of the block that `BB` refers to |
| `const llvm::BasicBlock *ptr` | Declare a pointer to a block |
| `*ptr` | Access the object pointed to by `ptr` |
| `BB.getName()` | Access a member through an object or reference |
| `ptr->getName()` | Access a member through a pointer |

The successor loop already declares its variable as a pointer, so append it
directly, without taking its address again:

```cpp
for (const llvm::BasicBlock *successor : llvm::successors(&BB)) {
    info.successors.push_back(successor);
}
```

#### Why different traversal loops use `&` or `*`

The loop variable's type follows what the range supplies. A range-based
`for` loop does not require one particular pointer or reference syntax.

```cpp
for (const llvm::BasicBlock &BB : F) {
    for (const llvm::BasicBlock *successor : llvm::successors(&BB)) {
        // BB refers to a block; successor points to a destination block.
    }
}

for (const auto &info : cfg.blocks) {
    for (const auto *successor : info.successors) {
        // info refers to a stored record; successor is a copied pointer.
    }
}
```

Read the loops one at a time:

| Range | What it supplies | Loop variable | Why |
|---|---|---|---|
| `F` | Basic block objects by reference | `const BasicBlock &BB` | Inspect each existing block without copying it |
| `BB` | Instruction objects by reference | `const Instruction &I` | Inspect each existing instruction without copying it |
| `llvm::successors(&BB)` | Pointers to successor blocks | `const BasicBlock *successor` | Each element already identifies a destination by address |
| `cfg.blocks` | `BlockInfo` records | `const auto &info` | Inspect a stored record without copying its vectors |
| `info.successors` | Stored block pointers | `const auto *successor` | Copy each pointer value, not the pointed-to block |

`llvm::predecessors(&BB)` and `info.predecessors` follow the same pointer
pattern as successors. `const auto &cfg = AM.getResult<CFGAnalyzer>(F)` also
uses a reference to avoid copying the analysis manager's cached result.

In `llvm::successors(&BB)`, `&BB` is an expression that obtains the block's
address because this API accepts a block pointer. It is separate from the
reference declaration `BasicBlock &BB` in the outer loop.

For an ordinary `std::vector<BlockInfo>`, writing `auto info` would copy
each record, including its vectors. Writing `const auto &info` avoids that
copy. For a `std::vector<const BasicBlock *>`, copying an element copies
only a pointer; it does not copy the block. Using `&` everywhere is therefore
unnecessary, and using `*` everywhere would not match the ranges' types.

Pointers and references also determine member access: use `BB.getName()`
and `info.successors`, but `successor->getName()` and
`info.block->getName()`. To pass a pointed-to block to an API that expects a
block reference, dereference the pointer with `*successor`.

#### Why not `for (auto bb : F)`?

`auto` deduces a type; it does not automatically preserve the reference
provided by the iterator. This loop tries to copy each block into a new
local variable:

```cpp
for (auto bb : F) {
    // Tries to copy a BasicBlock; LLVM BasicBlock is noncopyable.
}
```

Use a reference to bind to the existing block instead:

```cpp
for (const auto &bb : F) {
    // Read the existing block without copying it.
}
```

For this traversal, that is equivalent to declaring the loop variable as
`const llvm::BasicBlock &bb`.

| Loop variable | Effect |
|---|---|
| `auto bb` | Tries to create a value by copying the element |
| `auto &bb` | Refers to the existing element; whether it is mutable follows the range's element type |
| `const auto &bb` | Refers to the existing element through a read-only reference |

`FunctionEligibility::check` takes `const llvm::Function &F`, so the blocks
obtained from that function are already const. Even `auto &bb` therefore
deduces a const reference in this context. Writing `const auto &bb` makes
the read-only intent explicit.

This also explains why `auto successor` can be valid when iterating a vector
of block pointers: it copies a pointer value, not a block. Choose the loop
variable based on the range's element type and whether copying is intended.

Taking `&successor` would obtain the address of the local pointer variable,
not the block's address. The stored block pointers refer to blocks owned by
the function and must only be used while those blocks remain valid.

### Exception-handling pads and personality routines

In exception handling, **pad** comes from **landing pad**: a designated
place where control arrives when an exception interrupts normal execution.
An LLVM `invoke` has separate normal and exceptional destinations:

```llvm
%result = invoke i32 @callee()
    to label %normal
    unwind label %exception
```

If the call succeeds, control continues at `%normal`. If it unwinds with an
exception, control transfers to `%exception`. In the landing-pad model, that
destination begins with a `landingpad` instruction, after any PHIs:

```llvm
exception:
  %ex = landingpad { ptr, i32 } cleanup
  resume { ptr, i32 } %ex
```

This fragment belongs inside a function with a suitable personality routine.
`landingpad` receives exception information, `cleanup` marks participation
in cleanup handling, and `resume` continues unwinding. The marker does not
perform cleanup work by itself; actual cleanup operations would be separate
instructions before `resume`.

An **EH pad** is the broader term for exception-handling entry instructions.
LLVM recognizes `landingpad`, `catchpad`, `cleanuppad`, and `catchswitch` as
EH-pad instructions. See [LLVM's exception-handling documentation](https://llvm.org/docs/ExceptionHandling.html).

The two eligibility checks inspect different levels:

| Query | Meaning |
|---|---|
| `F.hasPersonalityFn()` | Does the function specify a personality routine defining its exception-handling behavior? |
| `BB.isEHPad()` | Is the block's first non-PHI instruction an EH-pad instruction? |

For `with_invoke` in `tests/ir/instruction-kinds.ll`, the function has a
personality routine. Its `entry` block contains `invoke` but is not an EH
pad; `normal` contains a return and is not an EH pad; `exception` starts with
`landingpad` and is an EH pad. Containing `invoke` therefore does not itself
make a block an EH pad.

A function can have a personality routine without any EH-pad blocks. For
valid IR, EH-pad instructions require an associated personality routine.
Consequently, if MiniShield rejects every function with a personality
routine before inspecting blocks, the later `isEHPad()` rejection is
redundant for those valid inputs. It states the block-level restriction
explicitly rather than providing an independent necessary rejection.

### Intrinsics and instructions

An **instruction** is one operation in LLVM IR. An **intrinsic** is a special
function whose meaning LLVM already knows, commonly invoked through a `call`
instruction. Compare these instruction fragments:

```llvm
%a = add i32 %x, 1
%b = call i32 @my_function(i32 %a)
%c = call double @llvm.sqrt.f64(double %value)
```

| Result | Instruction opcode | Meaning |
|---|---|---|
| `%a` | `add` | Built-in arithmetic operation |
| `%b` | `call` | Call to an ordinary function |
| `%c` | `call` | Call to an LLVM intrinsic |

`llvm.sqrt.f64` has LLVM-defined semantics. Declare it without providing a
function body:

```llvm
declare double @llvm.sqrt.f64(double)
```

Intrinsic names use the reserved `llvm.` prefix. LLVM lowers intrinsic
operations to appropriate target code; an intrinsic call does not necessarily
remain a function call in machine code. See [LLVM's intrinsic documentation](https://llvm.org/docs/LangRef.html#intrinsic-functions).

In the C++ API, the relevant inheritance relationship is:

```text
Instruction
  └── CallBase
       └── CallInst
            └── IntrinsicInst
```

Every `IntrinsicInst` is an instruction and a call, but most instructions
and many calls are not `IntrinsicInst`s. The intrinsic function declaration
itself is a `Function`; the instruction inside the caller is the operation
that invokes it. LLVM also permits certain intrinsics in `invoke`
instructions; `IntrinsicInst` specifically represents intrinsic `call`
instructions.

For coroutine checking, this expression asks whether `I` is an intrinsic
call instruction:

```cpp
llvm::dyn_cast<llvm::IntrinsicInst>(&I)
```

On success, inspect `getCalledFunction()->getName()` to identify the family.
The `llvm.coro.` prefix identifies coroutine intrinsics, which the initial
eligibility policy rejects conservatively. A failed cast returns `nullptr`.

The statistics pass's `Call` opcode counter also counts intrinsic calls:
they still have opcode `Call`. Being recognized as an intrinsic does not
change the instruction's opcode into a separate intrinsic opcode.

### Exercise function eligibility and rejection (task 1.4)

The eligibility helper returns a decision and reason without modifying the
function. In `FlatteningPass.cpp`, include `minishield/FunctionEligibility.h`
and, after skipping declarations, call:

```cpp
const auto eligibility = FunctionEligibility::check(F);
```

For rejection, print the function name and `eligibility.reason`, then return
`PreservedAnalyses::all()` immediately. For acceptance, print an eligible
diagnostic. The pass remains a diagnostic stub; passing eligibility checks
does not mean flattening has occurred.

Keep the success return `{true, ""}` at the end of the eligibility checker,
after every block and instruction has been checked. Its current policy rejects
declarations, presplit coroutine functions, personality routines, coroutine
intrinsic calls, address-taken blocks, EH pads, and unsupported terminators.
The supported terminators are `CondBr`, `UncondBr`, `Switch`, `Ret`, and
`Unreachable` in the installed LLVM 23 API.

The existing fixtures demonstrate:

| Fixture / function | Expected decision |
|---|---|
| `phi.ll` / `merge` | Eligible |
| `instruction-kinds.ll` / `with_invoke` | Rejected: exception-handling personality |
| `instruction-kinds.ll` / `with_indirectbr` | Rejected: unsupported terminator `indirectbr` |
| `instruction-kinds.ll` / `without_optimization` | Skipped by the optional flattening pass because of `optnone` |

Rejection reports the first failing check. The required statistics pass still
inspects `optnone` functions; the optional flattening pass may not run on them.

**Fixture exercises:** write the following files yourself. These isolate checks
that the existing exception and indirect-branch fixture does not exercise
independently.

Create `tests/ir/coroutine.ll`:

```llvm
declare ptr @llvm.coro.noop()

define ptr @coroutine_handle() {
entry:
  %handle = call ptr @llvm.coro.noop()
  ret ptr %handle
}
```

This tests the conservative coroutine-intrinsic policy, including functions
that manipulate coroutine handles. No personality routine or unsupported
terminator should mask this check.

Create `tests/ir/address_taken.ll`:

```llvm
define ptr @address_taken() {
entry:
  br label %target
target:
  ret ptr blockaddress(@address_taken, %target)
}
```

The branch and return are supported terminators, but `%target` has its address
used as a value. This isolates `hasAddressTaken()`.

After building, run each fixture from the project root with the environment
activated:

```bash
cmake --build build
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -disable-output tests/ir/coroutine.ll

opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -disable-output tests/ir/address_taken.ll
```

Expect a coroutine-intrinsic rejection for `coroutine_handle`, and an
address-taken-block rejection for `address_taken`.

Then check that rejection leaves the IR unchanged:

```bash
opt -passes=verify \
  -S tests/ir/coroutine.ll -o build/before.ll

opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -S tests/ir/coroutine.ll -o build/after.ll

diff -u build/before.ll build/after.ll
```

Expect a rejection diagnostic and an empty diff. Repeat with
`tests/ir/address_taken.ll`, and apply the same unchanged-IR check to the
existing rejection cases. Both paths use LLVM's printer, avoiding differences
between handwritten formatting and canonical IR. A successful `verify` alone
does not prove the function was left unchanged.

The presplit coroutine marker is a separate rejection path to test next.
These exercises do not yet establish complete eligibility coverage or prove
that a future transformation preserves behavior.

### `PassInfoMixin` vs `OptionalPassInfoMixin` vs `RequiredPassInfoMixin`

The New Pass Manager uses mixins to supply pass metadata, such as the pass
name and pipeline printing. In this project's installed LLVM 23.1.5 headers,
the relationship is:

| Mixin | Role | `isRequired()` |
|---|---|---|
| `PassInfoMixin<T>` | Common metadata base; still supports the older spelling with optional behavior | `false` |
| `OptionalPassInfoMixin<T>` | Explicitly declares a pass that may be skipped | `false` |
| `RequiredPassInfoMixin<T>` | Explicitly declares a pass that normal pass-skipping mechanisms must not skip | `true` |

Both explicit mixins inherit from `PassInfoMixin<T>`. The installed header
recommends that actual passes inherit from `OptionalPassInfoMixin` or
`RequiredPassInfoMixin`, rather than directly from the common base.

For example, an optional function pass may be skipped on a function marked
`optnone`; a required pass still runs there. **Required does not automatically
add the pass to a pipeline:** it must still be registered and scheduled.
See LLVM's [required-pass documentation](https://llvm.org/docs/WritingAnLLVMNewPMPass.html#required-passes).

For the initial diagnostic stub, declare the choice explicitly:

```cpp
class FlatteningPass
    : public llvm::OptionalPassInfoMixin<FlatteningPass> {
public:
    llvm::PreservedAnalyses run(
        llvm::Function &F,
        llvm::FunctionAnalysisManager &AM);
};
```

If MiniShield must perform hardening even on `optnone` functions, use
`RequiredPassInfoMixin<FlatteningPass>` instead. This choice controls whether
the pass may be skipped; it does not change which functions the flattening
algorithm can safely handle or which analyses remain valid after `run()`.
