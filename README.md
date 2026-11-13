# MiniShield

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-yellow.svg)](LICENSE)

An LLVM pass-plugin study project that is also a **framework for code-hardening
techniques** — control-flow flattening is its first named pass, and the same plugin
hosts others (opaque predicates, function splitting, forward CFI, name obfuscation).
The study covers IR inspection, CFG analysis, eligibility, and control-flow
rewriting. The learner implementation is in progress; the books include future
exercises and complete reference examples.

**[Read the Volume 1 book](https://zilutian.github.io/minishield/)** — step-by-step
lessons, diagrams, code, explanations, and checkpoints. The editable teaching
source is [volume1](volume1); the roadmap is [PLAN.md](PLAN.md).

**Volume 1 roadmap.** Volume 1 ends with one decision — which functions a
control-flow-flattening pass may touch. You build a read-only stats pass and a
CFG analysis first, because you can't safely flatten what you haven't inspected.
The flattening rewrite itself is Volume 2.
[Volume 2: transformations](https://zilutian.github.io/minishield/#day2) adds
PHI and cross-block value demotion, then dispatcher construction, then the
testing, measurement, and demo chapters that prove it. Its teaching notes are
in [volume2](volume2).
[Volume 3: hardening techniques](https://zilutian.github.io/minishield/#day3)
is a crash course on the techniques flattening leaves out — control-flow
integrity, stack canaries, OLLVM-style obfuscation, position independence, and
the fuzzing that proves each one still behaves; its teaching source is
[volume3](volume3). Both books are complete drafts, with implementation exercises
and measurements still to be done.

## Beyond flattening: a framework for hardening

Flattening is the first entry in a larger design. The plugin is built from
technique-agnostic seams — a named-pass registry, a per-technique eligibility
guard, a shared CFG analysis, and a differential/stats harness — so other
code-hardening techniques (opaque predicates, function splitting, instruction
substitution, forward CFI, name obfuscation) each become one more named pass
plugged into the same skeleton. Volume 1 closes on this as a capstone lesson:
[Zoom out: a framework for hardening](https://zilutian.github.io/minishield/#lesson-78).

## Set up the environment

Requires Conda/Miniforge on Linux x86-64. Create the named environment once:

```bash
conda env create -f environment.yml
conda activate minishield
export LIBRARY_PATH="$CONDA_PREFIX/lib"
```

[environment.yml](environment.yml) specifies LLVM/Clang 23.1.5, CMake, Ninja,
GoogleTest, and C++ development headers. In each new shell, activate the
environment and export `LIBRARY_PATH` again. Volume 1’s environment chapter explains how the
original environment was created, what each package does, and how to verify it.

## Configure and build

From the project root:

```bash
cmake -G Ninja -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER="$CONDA_PREFIX/bin/clang++-23" \
  -DLLVM_DIR="$CONDA_PREFIX/lib/cmake/llvm"
cmake --build build
```

Output: `build/libMiniShield.so`. Missing `build.ninja` means configuration
has not completed; `ninja: no work to do` means the build is up to date.

## Run and verify

```bash
# Inspect instructions and CFG information.
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-stats),verify' \
  -disable-output tests/ir/phi.ll

# Run the current flattening checkpoint and verify its output.
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -S tests/ir/phi.ll -o build/phi-output.ll
```

Fixtures live in [tests/ir](tests/ir). `verify` checks IR structure; it does not
prove equivalent program behavior. The book explains expected counts,
rejection cases, and unchanged-IR checks for rejected or read-only passes.

## Read the book locally

```bash
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. No Node installation or frontend build is needed.
The book supports chapter search, reading progress, focus mode, copyable code,
and interactive concept diagrams. Source files are in [docs](docs).

## License

This repository uses a split license; see [LICENSE](LICENSE) for the full text.

- **Code** — the pass-plugin source (`include/`, `lib/`), build files, tests,
  and scripts are licensed under the [MIT License](LICENSE).
- **Book and teaching content** — the teaching sources ([volume1](volume1),
  [volume2](volume2), [volume3](volume3)), the rendered book site ([docs](docs)), and the
  roadmap ([PLAN.md](PLAN.md)) are licensed under
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). You may
  share and adapt them for non-commercial purposes with attribution, but
  commercial use requires prior written permission.
- **Fonts** — `docs/assets/fonts/` remains under the SIL Open Font License,
  as stated in the accompanying `*-OFL.txt` files.
