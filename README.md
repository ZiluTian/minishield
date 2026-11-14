# MiniShield

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-yellow.svg)](LICENSE)

MiniShield is a C++20 study project for an LLVM 23.1.5 New Pass Manager plugin,
developed alongside a three-volume web book that teaches the LLVM and C++
concepts behind the implementation.

**[Read the book](https://zilutian.github.io/minishield/)** ·
[Project roadmap](PLAN.md)

The plugin includes `minishield-stats`, CFG analysis, and function eligibility.
`minishield-flatten` is registered, but its transformation is still under
development; it does not yet rewrite the function control flow.
LLVM's `verify` pass checks IR structure; it does not prove behavior is
preserved.

## Framework direction

MiniShield is intended to grow into a plugin that hosts several independent
code-hardening passes. The design separates shared infrastructure—such as pass
registration and reusable CFG analysis—from each technique's own eligibility
rules and transformation. The [Volume 1 framework capstone](https://zilutian.github.io/minishield/#lesson-78)
works through how another technique, opaque predicates, could fit that design.

That is the project's direction, not its current feature list: control-flow
flattening is the only hardening pass being developed here. Other techniques
covered in Volume 3 are study topics, not available plugin passes.

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

## Repository layout

`include/minishield/` and `lib/` contain the plugin; `tests/ir/` contains LLVM
fixtures; `volume1`–`volume3` are the teaching sources; `docs/` is the static
book site.

## License

See [LICENSE](LICENSE) for full terms. Code, build files, tests, and scripts use
MIT. The books, book site, and [PLAN.md](PLAN.md) use CC BY-NC 4.0. Fonts in
`docs/assets/fonts/` use the SIL Open Font License, as stated in their license
files.
