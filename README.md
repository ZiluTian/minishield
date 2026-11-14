# MiniShield

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-yellow.svg)](LICENSE)

MiniShield is a C++20 study project for an LLVM 23.1.5 New Pass Manager plugin,
developed alongside a three-volume web book that teaches the LLVM and C++
concepts behind the implementation.

**[Read the book](https://zilutian.github.io/minishield/)** ·
[Project roadmap](PLAN.md)

The plugin includes `minishield-stats`, CFG analysis, and function eligibility.
`minishield-flatten` is registered as a learner starting stub: it runs the
eligibility guard and reports whether a function qualifies, but does not
rewrite the function's control flow — the Volume 2 lessons guide you to build
that transformation. The author's own progress on the flattener is kept
separate from these learner stubs and is not included in the published tree.
LLVM's `verify` pass checks IR structure; it does not prove behavior is
preserved.

## Framework direction

MiniShield is intended to grow into a plugin that hosts several independent
code-hardening passes. The design separates shared infrastructure—such as pass
registration and reusable CFG analysis—from each technique's own eligibility
rules and transformation. The [Volume 1 framework capstone](https://zilutian.github.io/minishield/#lesson-78)
works through how another technique, opaque predicates, could fit that design.

That is the project's direction, not its current feature list: control-flow
flattening is the only hardening technique with a pass in this repository; the
other techniques covered in Volume 3 are study topics, not available plugin
passes.

## Quick start

Requires Conda/Miniforge on Linux x86-64. The [environment.yml](environment.yml)
file defines the `minishield` environment with LLVM/Clang 23.1.5, CMake, Ninja,
and C++ development headers.

Create the environment once, then activate it in each new shell:

```bash
conda env create -f environment.yml
conda activate minishield
export LIBRARY_PATH="$CONDA_PREFIX/lib"
```

Configure and build from the repository root:

```bash
cmake -G Ninja -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER="$CONDA_PREFIX/bin/clang++-23" \
  -DLLVM_DIR="$CONDA_PREFIX/lib/cmake/llvm"
cmake --build build
```

This produces `build/libMiniShield.so`. For a read-only inspection pass:

```bash
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-stats),verify' \
  -disable-output tests/ir/phi.ll
```

To run the current flattening prototype and save its IR output:

```bash
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -S tests/ir/phi.ll -o build/phi-output.ll
```

The examples in [tests/ir](tests/ir) are fixtures for the passes and lessons.
See the book for expected results and behavior checks.

## Learning path

The web book is split into three volumes:

1. [Volume 1 — foundations](https://zilutian.github.io/minishield/) covers
   setup, plugin basics, IR, statistics, CFG analysis, eligibility, and an LLVM
   Crash Course.
2. [Volume 2 — transformations](https://zilutian.github.io/minishield/#day2)
   develops value preparation, dispatcher construction, rewriting, and checks.
3. [Volume 3 — hardening](https://zilutian.github.io/minishield/#day3)
   studies control-flow integrity, stack canaries, obfuscation, and evaluation.

Editable book sources are [volume1](volume1), [volume2](volume2), and
[volume3](volume3). To serve the book from this checkout, run
`python3 -m http.server 8000 --directory docs` and open
<http://localhost:8000>.

## Book review and revision log

`debate/` records how the book is reviewed and revised. It is a three-reader
experiment in which three simulated learner personas — `no-llvm`,
`no-compiler`, and `no-hardening` — each read the book from their own
background and propose concrete improvements:

- `debate/README.md` — the experiment design: the personas, their gaps, and
  the round structure.
- `debate/round1-<profile>.md` — each persona's independent reading and
  improvement report.
- `debate/round2-<profile>.md` — each persona reacting to the other two's
  round-1 reports (endorsements, pushback, new proposals, and a joint top-3).
- `debate/editor-changes.md` — an editor consolidating all six reports into a
  single, approval-ready change list. This is the revision log: every entry
  cites its origin, the exact anchor in the current text, and its status
  (READY vs. NEEDS-AUTHOR-WORK).
- `debate/eNN-evidence.md` — read-only evidence backing a specific change; for
  example `e20-evidence.md` quotes CFI metadata from the local `.v3ref/` CFI
  demos.

The change list is a proposal until you approve it; only then are edits applied
to the book sources (`volume1`–`volume3`) and the `docs/assets/*.json` web data.

## Repository layout

`include/minishield/` and `lib/` contain the plugin; `tests/ir/` contains LLVM
fixtures; `volume1`–`volume3` are the teaching sources; `docs/` is the static
book site; and `debate/` holds the book's review and revision log (see the
[Book review and revision log](#book-review-and-revision-log) section).

Two top-level documents guide how the project is built and taught:

- **[PLAN.md](PLAN.md)** — the project roadmap: a three-day plan of tasks,
  pitfalls, and a verifiable exit criterion for every step, across the three
  volumes. It is the "what to build, in what order, and how to check each
  result" reference for the implementation.
- **`SKILL.md`** — the teaching-agent guide: the instruction set for an AI
  agent that walks a learner through the book one lesson at a time, covering
  the lesson progression, the teaching standards (the learner owns the code,
  show real IR, verify every claim), and the MiniShield pipeline invariants
  the teaching must respect.

## License

See [LICENSE](LICENSE) for full terms. Code, build files, tests, and scripts use
MIT. The books, book site, and [PLAN.md](PLAN.md) use CC BY-NC 4.0. Fonts in
`docs/assets/fonts/` use the SIL Open Font License, as stated in their license
files.
