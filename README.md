# MiniShield

An LLVM pass-plugin study project for control-flow flattening. The current
implementation inspects IR, reports CFGs and natural loops, and checks function
eligibility. The flattening pass is still a diagnostic stub.

**[Read the Day 1 book](https://zilutian.github.io/minishield/)** — step-by-step
lessons, diagrams, code, explanations, and checkpoints. The editable teaching
source is [day1](day1); the roadmap is [PLAN.md](PLAN.md).

## Set up the environment

Requires Conda/Miniforge on Linux x86-64. Create the named environment once:

```bash
conda env create -f environment.yml
conda activate minishield
export LIBRARY_PATH="$CONDA_PREFIX/lib"
```

[environment.yml](environment.yml) specifies LLVM/Clang 23.1.5, CMake, Ninja,
GoogleTest, and C++ development headers. In each new shell, activate the
environment and export `LIBRARY_PATH` again. Book lesson 0 explains how the
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

# Report eligibility; the current pass leaves IR unchanged.
opt -load-pass-plugin="$PWD/build/libMiniShield.so" \
  -passes='function(minishield-flatten),verify' \
  -S tests/ir/phi.ll -o build/phi-output.ll
```

Fixtures live in [tests/ir](tests/ir). `verify` checks IR structure; it does not
prove equivalent program behavior. The book explains expected counts,
rejection cases, and unchanged-IR checks.

## Read the book locally

```bash
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. No Node installation or frontend build is needed.
The book supports chapter search, reading progress, focus mode, copyable code,
and interactive concept diagrams. Source files are in [docs](docs).
