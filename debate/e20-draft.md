# E20 draft — CFI mechanism note (PENDING author confirmation, NOT applied)

Target: `volume3` 3.2.1, inserted after L116 (end of the "Where LTO can see the
target, the check changes shape" section), mirrored into
`docs/assets/volume3.json` (3.2.1 lesson). Evidence: `debate/e20-evidence.md`.

## Proposed note text (in the book's voice)

---

### What `type.test` is actually testing

The guard's second operand is the expected type as **call-site metadata**: in
the minimal module it is the mangled type-info name `_ZTSFiiE` attached
directly to the `type.test` call, and LTO's capture of the same check carries
the pair `!{i64 0, !"_ZTSFiiE"}` — an offset and a name — recorded once per
CFI-compiled function in the module's CFI metadata (the module flag
`!{i32 4, !"CFI Canonical Jump Tables", i32 1}` marks the module as using
this scheme; vcall's capture lists one such entry per class and per virtual
method, `!{i64 16, !"_ZTS4Base"}`, `!{i64 16, !"_ZTSM4BaseFiiE.virtual"}`).

This is why the check is an **LTO feature**. Without LTO, each translation
unit only sees its own functions and the check has to fall back to a
runtime-library lookup of the target's descriptor; with LTO the link step can
merge the per-function descriptors into one table and the check becomes a
direct resolution of the pointer against that table — no table, no check,
hence the flag's hard requirement on `-flto`. The `.cfi` copy of `op_right`
exists for the same reason: the rebuilt body carries its descriptor, while
the original symbol stays behind as a one-instruction trampoline for
callers that are not CFI-compiled.

"Target set" therefore has a concrete meaning: it is *all functions whose
descriptor matches this type* — a type as a coarse stand-in for an address
set. That reconciles the landscape lesson's "target-set checks" with this
lesson's "not an address check": the guard does not compare the pointer
against a list of allowed addresses; it asks whether the pointed-to
function's type descriptor agrees with the call site's.

Reading the names: the Itanium mangling here is short on purpose. `_ZTS`
marks a **type-info name** (the `__class_type_info` name field, not a
function address); `Fii` is a function taking `i32` and returning `i32`; in
vcall's `4Base`, the leading `4` is the length of the identifier `Base`.

---

## Verification status

| Claim | Status |
| --- | --- |
| Call-site metadata is the expected type (`!"_ZTSFiiE"` / `!{i64 0, !"_ZTSFiiE"}`) | **Verified** — `.v3ref/cfi/cfi_pipe.s` L53, L132 |
| Per-class/per-method descriptor entries for vcall | **Verified** — `.v3ref/cfi/vcall_pipe.s` L187–195 (`!2`, `!3`, `!5`, `!10`) |
| `CFI Canonical Jump Tables` module flag | **Verified** — `.v3ref/cfi/cfi_pipe.s` L120 |
| Itanium type-info symbols emitted in the CFI module (`_ZTI4Base` as `{ptr, ptr}`, `_ZTS4Base` = `c"4Base\00"`, comdat) | **Verified** — `.v3ref/cfi/vcall_pipe.s` L26/L44/L46 |
| "`op_right` gets a `.cfi` copy; the original stays as a trampoline" | **Stated in the book (L116, glossary L1872) — not re-verified in this pass.** No `.cfi` symbol appears in the two `.s` captures (grep empty), which is consistent with the trimmed listings but not a confirmation |
| "LTO merges the per-function descriptors into one table and `type.test` resolves the pointer against it" | **UNVERIFIED — author to confirm.** The metadata shape is captured, but the exact runtime resolution path (what the `i64` offset indexes in memory, where the descriptor blob lives) is not pinned down from the `.s` files alone. If the mechanism differs, only this sentence and the "no table, no check" framing need adjusting |
| "Without LTO the check falls back to a runtime-library lookup" | **Plausible, not verified.** The book already states the flag refuses to work without `-flto` (L104); this sentence explains *why* in mechanism terms and should be confirmed or softened to "without LTO there is no merged descriptor table to resolve against" |

## Author confirmation checklist

1. Is the `i64` in `!{i64 0, !"_ZTSFiiE"}` an offset into a link-time
   descriptor table, or something else (e.g. an index)? Fix the "offset and
   a name" wording accordingly.
2. Does `type.test` at runtime read a descriptor pointer out of the target
   function (prologue/embedded), or does it consult a table the call site
   knows about? Fix the "resolves the pointer against that table" sentence.
3. Confirm or drop the "runtime-library lookup" fallback sentence (the
   legacy `cfi_icheck` / `__cfi_check_d` path in non-LTO builds).
4. If (1)–(3) check out, apply the note as written to root + JSON and
   recompute the 3.2.1 lesson's `words`.
