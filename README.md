# MiniShield

An LLVM pass-plugin study project for control-flow flattening. The study covers IR inspection, CFG analysis, eligibility, and control-flow
rewriting. The learner implementation is in progress; the books include future
exercises and complete reference examples.

**[Read the Volume 1 book](https://zilutian.github.io/minishield/)** — step-by-step
lessons, diagrams, code, explanations, and checkpoints. The editable teaching
source is [day1](day1); the roadmap is [PLAN.md](PLAN.md).

**Volume 1 roadmap.** Volume 1 ends with one decision — which functions a
control-flow-flattening pass may touch. You build a read-only stats pass and a
CFG analysis first, because you can't safely flatten what you haven't inspected.
The flattening rewrite itself is Volume 2.
[Volume 2: transformations](https://zilutian.github.io/minishield/#day2) adds
PHI and cross-block value demotion, then dispatcher construction. Its teaching
notes are in [day2](day2).
[Volume 3: tests and measurement](https://zilutian.github.io/minishield/#day3)
covers GoogleTest, CTest, differential checks, benchmarks, and a reproducible
demo; its teaching source is [day3](day3). Both books are complete drafts,
with implementation exercises and measurements still to be done.

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
