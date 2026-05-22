# Parser Architecture Requirements - ShellParser

**Status**: Active (Version 1.0+ → 2.1)  
**Milestone**: v2.1 — Placeholder Mass Replace

## Core Intention of `placeholder` Command

The `placeholder` command is **NOT** a split operation.  
It is a **mass in-place replace** operation.

**Exact Behavior Required**:
- Run: `shellparser placeholder <source_file>`
- Step 1: Always create dated backup first (`source.sh.YYYYMMDD-N`)
- Step 2: Replace **every function body** (except top-block / shebang area) with minimal clean placeholder skeleton **inside the original source file**
- Step 3: Save individual clean placeholder `.sh` files into `target/placeholder.YYYYMMDD-N/`
- Top-block (everything before first function) must remain **100% untouched**

This command exists to quickly "hollow out" a large monolithic script for AI refactoring while keeping editable skeletons.

---

## 1. Purpose

This document defines the official **3-stage parser architecture** and the **standard pattern** for safely extending functionality in ShellParser.

## 2. Standard Way to Introduce New Features (CIAO-Lite Rule)

**All new output modes or major behaviors must be introduced using a dedicated `Attr` flag.**

### Why this pattern?
- Keeps the 3-stage pipeline untouched and sacred.
- Prevents fragile command-string checks or global variables.
- Maintains full backward compatibility.

### Example: Adding `placeholder` (v2.1)

1. **Declare new Attr** in `ShellParserCore.__init__()`:
   ```python
   Attr(self, attrName='placeholder_mode', value=False)
   ```

2. **Set the flag** in `main()` and `interactive_mode()`:
   ```python
   core.placeholder_mode(True)
   ```

3. **Branch in the central coordinator** (`afterStartParse()`):
   ```python
   if self.output_enabled():
       self.stage_1_report()
       self.stage_2_ownership()
       
       if self.docs_mode():
           self.stage_3_write_docs()
       elif self.placeholder_mode():           # ← New v2.1
           self.stage_3_create_placeholder()
       else:
           self.stage_3_extract_functions()
   ```

4. **Document** the new Attr in `attr-contract.md`, `milestones.md`, `cli-interface.md`, and this file.

This exact pattern was used for `docs_mode` (v2.0) and is now applied to `placeholder_mode`.

## 3. Core Architecture (3-Stage Pipeline)

### Stage 1 — Forward Classification
- Line-by-line parsing with enhanced tokenizer.

### Stage 2 — Backward Ownership Correction
- Reverse pass for correct ownership (including `top-block`).

### Stage 3 — Extraction / Replace / Docs / Placeholder (Mode-Driven)

- Controlled exclusively by Attr flags (`docs_mode`, `replace_mode`, `placeholder_mode`, `output_enabled`).
- New `placeholder` mode: replaces all functions **except** `top-block` with skeleton placeholders while preserving original structure.

## 4. Key Design Rules (Non-Negotiable)

- New features **must** use an `Attr` flag declared in `__init__()`.
- Branching must happen in `afterStartParse()` (or dedicated hook).
- Never use `sys.argv`, command name strings, or global variables inside the parser core.
- `placeholder_mode` must preserve `top-block` and shebang 100%.
- All mode flags must be listed in `attr-contract.md`.

- Real Brace Calculation, Enhanced Tokenizer, StateLogic FSM, etc. remain sacred.

## 5. Placeholder Mode Specifics (v2.1)

- Reuses full Stage 1 + Stage 2 for correct ownership detection.
- Only functions with `func_name != "top-block"` and `func_name != ""` are replaced.
- Placeholder template:
  ```sh
  function_name() {
      # Placeholder - to be implemented
      echo "TODO: implement function_name()"
  }
  ```
- Always performs backup before writing (same safety as `replace`).

## 6. Design Principles (CIAO-Lite)

- **Caution**: New features must not risk breaking existing behavior.
- **Intentional**: Explicit `placeholder_mode` Attr makes control flow obvious.
- **Anti-fragile**: Classic `split` / `replace` / `split-docs` remain untouched.
- **Over-protect**: Every new mode follows the proven Attr pattern.

## 7. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Introduce new output modes without a corresponding `xxx_mode` Attr flag
- Bypass `placeholder_mode` (or future mode Attrs) when extending Stage 3
- Merge stages or use fragile detection methods
- Hard-code mode logic inside parser methods
- Remove or weaken any existing CIAO-Lite Protection Zone
- Modify `top-block` preservation logic in placeholder mode

## 8. Future Enhancements

- `--both` mode (classic + docs + placeholder)
- Customizable placeholder templates
- Semantic extraction mode
- Database export mode

---

**Last Updated**: May 11, 2026  
**Owner**: Parser Engine  
**Target Version**: 2.1 (`placeholder` subcommand with `placeholder_mode` Attr)

**Alignment**: Fully synchronized with `milestones.md`, `attr-contract.md`, `cli-interface.md`, `parameters.md`, and `interactive-mode.md`.
