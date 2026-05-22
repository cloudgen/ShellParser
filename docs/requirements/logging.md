# Logging Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the mandatory usage of **ChronicleLogger** as the **Single Source of Truth** for all output in ShellParser, in full alignment with the updated [output-requirements.md](output-requirements.md).

## 2. Core Rules (Sacred)

- **Only** ChronicleLogger may produce console or log output.
- **No** `print()`, `print_function`, `sys.stdout.write`, `sys.stderr`, or similar statements anywhere in the project (except inside ChronicleLogger itself).
- All human-readable messages, JSON output, errors, warnings, debug info, and success reports **must** go through the logger.
- When `--json` (or `JSON=1`) is used, **quiet mode is automatically forced** (see output-requirements.md).

## 3. Proper Instantiation & Initialization

```python
from ChronicleLogger import ChronicleLogger

def main():
    logger = ChronicleLogger(logname='ShellParser')
    
    # Mandatory: Read back resolved values
    appname = logger.logName()
    basedir = logger.baseDir()
    
    # Apply command-line / environment settings
    if getattr(args, 'quiet', False):
        logger.quiet(True)
    if getattr(args, 'json', False):
        logger.quiet(True)   # JSON forces quiet - sacred rule (see output-requirements.md)
    
    # Use logger for everything
    logger.log_message("Parser started", component="main")
```

## 4. Recommended Methods (aligned with output-requirements.md)

- `logger.log_message(msg, component="xxx", level="info")` — General logging
- `logger.prn(text)` — Human-readable output (respects quiet mode)
- `logger.error(...)`, `logger.warn(...)` — Errors and warnings (always shown)
- `logger.debug(...)` — Debug messages (only when `DEBUG=1`)

## 5. JSON Mode Behavior (Synchronized with output-requirements.md)

- When `--json` / `JSON=1` → `logger.quiet(True)` is **automatically enforced**.
- Special methods (`show_about()`, `show_help()`) output **pure JSON** via `print(json.dumps(...))` **only** after quiet mode is set.
- No human-readable text may appear in JSON mode.

## 6. Design Principles (CIAO-Lite)

- **Caution**: Centralized output prevents pollution and inconsistent behavior.
- **Intentional**: ChronicleLogger handles quiet/JSON/rotation/storage defensively.
- **Anti-fragile**: Survives different environments (venv, conda, root, etc.).
- **Over-protect**: Strict ban on any direct output statements.

## 7. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Add any `print()` or direct output statements anywhere in the project.
- Create multiple ChronicleLogger instances in one run.
- Remove calls to `logger.logName()` / `logger.baseDir()`.
- Bypass `logger.quiet(True)` in JSON mode.
- Remove or weaken ChronicleLogger integration.
- Bypass rules defined in [output-requirements.md](output-requirements.md).

## 8. Integration with Other Systems

- **Attr / StateLogic**: Logging concerns are **completely separate** from state management.
- **Output Control**: All global options (`--quiet`, `--json`) and environment variables are respected.
- **Milestone Alignment**: Fully supports v2.0 (`split-docs`) and future database/reporting features.

---

**Last Updated**: May 2026  
**Owner**: Logging System  
**Target Version**: 1.1 (Fully synchronized with output-requirements.md)
