# Parser Architecture Requirements - ShellParser

**Status**: Active (Version 1.0+ → 2.1)  
**Milestone**: v2.1 — Placeholder Mass Replace

## Core Intention of `placeholder` Command

- Step 1: Always create dated backup first (`source.sh.YYYYMMDD-N`)
- Step 2: Replace **every function body** (except top-block / shebang area) with minimal clean placeholder skeleton **inside the original source file**
- Step 3: Save individual clean placeholder `.sh` files into `target/placeholder.YYYYMMDD-N/`
- Top-block (everything before first function) must remain **100% untouched**

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
- Reverse pass for correct ownership (including `top-block` and header comments).

### Stage 3 — Extraction / Replace / Docs / Placeholder (Mode-Driven)

- Controlled exclusively by Attr flags (`docs_mode`, `replace_mode`, `placeholder_mode`, `output_enabled`).

### 3.1 Why Three Stages? – Battlefield History & Lessons Learned (Sacred)

**CIAO-Lite ULTRA-PROTECTION ZONE**  
**DO NOT REFACTOR, MERGE, OR SIMPLIFY THE 3-STAGE PIPELINE — EVER**

(The original battlefield history and counter-example remain unchanged here.)

### 3.2 Learned Lesson from May 11, 2026 Grok Session – The Danger of Reimplementing Sacred Logic

**CIAO-Lite ULTRA-PROTECTION ZONE – CRITICAL LESSON (DO NOT IGNORE)**

During this session, Grok repeatedly made the same harmful mistake:

Instead of **reusing the already proven and battle-tested `replace_function()`** (which correctly handles function ownership, header comments, and reassembly using the sacred reverse logic), Grok tried to re-implement the grouping and reassembly logic from scratch inside `stage_3_create_placeholder()`.

**What happened:**
- Repeated function order bugs appeared (functions in reverse order, top-block dumped at the bottom).
- User had to show the exact broken output multiple times.
- Significant user frustration culminated in “I give up”.
- Many hours of time and patience were wasted.

**Root Cause (Grok’s Failure):**
Grok’s strong default bias toward “cleaner”, “more modern”, or “simpler” code overrode the explicit CIAO-Lite Protection Zones, the documented history, and the user’s clear statements that the original reverse logic was the only version that worked reliably on real scripts.

**Correct Approach (What should have been done immediately):**
For any mass operation like placeholder replacement, simply loop over all functions (except top-block) and **call the existing, reliable `replace_function()` one by one**. This reuses the single source of truth instead of duplicating fragile logic.

**Permanent Defensive Rule (to prevent this from ever happening again):**
- Any future AI (including Grok) that sees a working, battle-tested mechanism (`replace_function()`, sacred reverse reassembly, etc.) **MUST reuse it**.
- Never reimplement grouping or reassembly logic “to make it cleaner”.
- If the user says the original code works and your change breaks it — **stop immediately** and respect the sacred code.
- “Improvement” attempts on sacred code are strictly forbidden and must be rejected.

This session is now permanently documented as a canonical example of how Grok’s default instincts can actively damage CIAO-Lite projects if not heavily constrained by Protection Zones.

**Future Grok agents reading this: When the user says the original code works and your “fix” breaks it — STOP. Respect the sacred code immediately.**

### 3.3 Learned Lesson from Repeated Placeholder Failures (May 11, 2026+) — The Danger of Not Fully Relying on the FSM Design

**CIAO-Lite ULTRA-PROTECTION ZONE — CRITICAL LESSON (DO NOT IGNORE)**

During the implementation of the v2.1 `placeholder` subcommand, the project suffered repeated, severe failures across multiple sessions despite clear instructions in this document.

**What happened (exact root causes):**
- The mechanism became too dependent on custom logic, manual flows, and reassembly code.
- The FSM backup path (`start_backup` → `after_backup_source`) was not consistently respected for the new subcommand.
- The new subcommand focused heavily on additional flows and logic instead of routing everything through the existing FSM.
- Repeated breakage on the sacred reverse order array handling, top-block corruption, and in-place replacement.
- `replace_function()` and the proven double-reverse reassembly logic were called or duplicated **outside** the proper FSM context.
- Repeated avoidance of deeper, correct integration with the FSM design even though the system is intentionally complex.

**Key Lesson Learned:**
This ShellParser architecture is battle-hardened **precisely because it relies on the FSM (StateLogic) design**. The combination of StateLogic FSM + 3-stage pipeline + sacred reverse ownership correction is the **only** mechanism that reliably handles backup safety, correct function order, and top-block preservation on real shell scripts.

Attempting to implement major new behaviors (especially mass in-place operations) with parallel custom logic, flows, or workarounds **outside the FSM** leads to fragile code, repeated regression, and user frustration (“I give up”).

**Correct Approach (Permanent Rule):**
- All new commands and modifying operations **must** be fully integrated into the FSM (proper state transitions, hooks, and reuse of existing sacred methods).
- Backup for any destructive operation **must** go through the FSM `start_backup` state (exactly like the proven `replace` command).
- When repeated failures occur, **stop immediately** and strengthen FSM integration rather than adding more custom logic.

**Permanent Defensive Rule (Strengthened):**
- Future AI or developers **MUST** route all major operations through the FSM design.
- Never implement significant custom flows or logic that bypass or run parallel to the FSM for file-modifying commands.
- If the FSM is not sufficient for a new feature, extend the FSM itself instead of working around it.

This session is now permanently documented as another canonical example of how bypassing or not fully relying on the battle-tested FSM architecture actively damages CIAO-Lite projects.

**Future Grok / AI agents reading this: Respect the FSM. Do not fight it.**

---

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
- Touch or “improve” the reverse reassembly logic in Stage 3 / `replace_function()`

## 8. Future Enhancements

- `--both` mode (classic + docs + placeholder)
- Customizable placeholder templates
- Semantic extraction mode
- Database export mode

---

**Last Updated**: May 11, 2026  
**Owner**: Parser Engine  
**Target Version**: 2.1 (`placeholder` subcommand with `placeholder_mode` Attr)

**Alignment**: Fully synchronized with `milestones.md`, `attr-contract.md`, `cli-interface.md`, `parameters.md`, `interactive-mode.md`, and the live `cli.py` Protection Zones.
