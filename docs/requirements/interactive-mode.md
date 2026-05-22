# Interactive Mode Requirements - ShellParser

**Status**: Active (Version 1.0+ → 2.1)

## 1. Purpose

This document defines the interactive (zero-argument) mode — the **recommended daily workflow** for ShellParser. It now includes support for the new `placeholder` subcommand (Milestone v2.1).

## 2. Core Behavior

When ShellParser is launched with **no arguments** (or only `--quiet`/`--json`):

- Show welcome message via ChronicleLogger
- Present a numbered menu with all supported operations
- Smart file/folder selection with numbered picker
- Respects all global options (`--quiet`, `--json`) and environment variables
- Uses the **single** `ShellParserCore` instance for all paths

## 3. Menu Options (Updated for v2.1)

```text
=== ShellParser Interactive Mode ===

1. split shell file          → target/components/*.sh
2. replace shell file        → safe function replacement + backup
3. split-docs                → target/docs/*.md (LLM training ready)
4. placeholder               → replace all functions with placeholders (keep top-block)
5. about / help              → version & usage info
```

## 4. Key Features

- **Smart file detection**:
  - For `split` / `split-docs` / `placeholder`: lists shell scripts
  - For `replace`: first pick from `target/components/`, then target script
- For `placeholder`: selects source script and runs with `placeholder_mode=True`
- Automatic creation of `target/` directories when needed
- Full respect for `output_enabled`, `replace_mode`, `placeholder_mode`, and quiet/JSON modes

## 5. Design Principles (CIAO-Lite)

- **Caution**: Helpful validation and error messages at every step.
- **Intentional**: Interactive mode remains the primary entry point.
- **Anti-fragile**: Graceful handling when components or scripts are missing.
- **Over-protect**: Minimal new code, reuses existing `ShellParserCore` and 3-stage parser.

## 6. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Remove interactive mode
- Change menu structure without updating this document
- Bypass `ShellParserCore` in any interactive path
- Use direct `print()` instead of ChronicleLogger
- Remove or weaken support for `placeholder` once added

---

**Last Updated**: May 11, 2026  
**Owner**: User Experience  
**Target Version**: 2.1 (Added `placeholder` option)
