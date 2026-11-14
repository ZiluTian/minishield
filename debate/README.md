# MiniShield book review — three-reader experiment

Started 2026-11-14. Three simulated learner personas read the MiniShield book
(the root files `volume1`, `volume2`, `volume3` — Foundations / Transformations /
Hardening) and propose concrete improvements for their own background profile.

## Personas

| Profile | Persona | Gap | Main terrain |
|---|---|---|---|
| `no-llvm` | Senior C++ dev, one university compiler course, never used LLVM | LLVM/Clang/IR/pass APIs | Vol 1–2 |
| `no-compiler` | Strong systems dev, never studied how compilers work | IR, SSA, CFG, passes, IR itself | Vol 1–2 |
| `no-hardening` | Compiler/LLVM dev, zero security background | CFI, canaries, OLLVM, threat models | Vol 3 |

Each persona assumes working familiarity with the other two territories.

## Rounds

- **Round 1** — independent reading + improvement reports: `round1-<profile>.md`
- **Round 2** — cross-reaction: each persona reads the other two's round-1
  reports, endorses/pushes back/new proposals/joint top 3: `round2-<profile>.md`
- **Editor** — an editor agent consolidates all six reports into one
  actionable change list with exact locations and proposed text:
  `editor-changes.md`. **No book file is modified; the change list is
  pending user approval.**
- **Application** — only after explicit user approval are changes applied
  to `volume1`/`volume2`/`volume3` (and the `docs/assets/*.json` web data if
  it must stay in sync).
