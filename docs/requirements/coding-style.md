# Coding Style Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the official coding style and CIAO-Lite conventions for all ShellParser source code.

## 2. Core Philosophy

ShellParser strictly follows **CIAO-Lite**:
- **C** - Caution
- **I** - Intentional
- **A** - Anti-fragile
- **O** - Over-protect

All code must prioritize long-term maintainability and safety when worked on by AI assistants (Grok, Claude, etc.).

## 3. File Header (Mandatory for Every .py File)

```python
# =============================================================================
# CIAO DEFENSIVE CODING STYLE - ShellParser
# =============================================================================
#
# !!! ALL OUTPUT MUST GO THROUGH CHRONICLELOGGER !!!
# !!! STATE MUST USE ATTR + STATELogic CONTRACT !!!
#
# Last aligned with CIAO principles: May 2026
# =============================================================================
```

## 4. General Rules

- Use Python 3.8+
- Follow PEP 8 with CIAO-Lite exceptions for verbosity and protection blocks
- All output → ChronicleLogger only (no `print()`, no `sys.stdout`)
- All parser state → Attr descriptors (never direct assignment or `.append()`)
- Maximum line length: 100 characters (for readability with long comments)

## 5. Function Documentation Style

Every public or important function must have:

```python
def function_name(self):
    """Short one-line description.

    CIAO-Lite Protection Zone
    =================================================================================
    DO NOT refactor, simplify, or remove without explicit user instruction.

    Purpose:
        ...

    Current Logic:
        ...

    Defensive Notes:
        ...
    =================================================================================
    """
```

## 6. Proper Package Usage

### ChronicleLogger (Output Only)
- Instantiate once in `main()`
- Always call `logger.logName()` and `logger.baseDir()`
- `logger.quiet(True)` when `--json` is used
- Use `logger.log_message()` and `logger.prn()`

### Attr + StateLogic (State Only)
- Declare with `Attr(self, attrName='name', value=...)`
- Access via `self.name()` (getter) / `self.name(new_value)` (setter)
- For lists: `self.map_array(entry)` — **never** `.append()`

## 7. Protection Zones

Use liberally:

```python
# =============================================================================
# CIAO-Lite Protection Zone
# DO NOT simplify, merge stages, remove comments, or refactor without approval
# =============================================================================
```

## 8. Design Principles (CIAO-Lite)

- **Caution**: Heavy comments, explicit contracts, no silent failures
- **Intentional**: Every major decision explained in code and requirements
- **Anti-fragile**: Survives repeated AI editing sessions
- **Over-protect**: Verbose headers and sacred rules are intentional

## 9. Forbidden Practices

- Direct `print()` anywhere
- `.append()` on Attr lists
- Hard-coded brace numbers
- Merging the 3-stage parser
- Bypassing ChronicleLogger or Attr contract
- Removing Protection Zones

## 10. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- "Clean up" or shorten verbose CIAO headers
- Remove or weaken any Protection Zone
- Ignore the Attr contract or ChronicleLogger rules
- Refactor core parser architecture without explicit approval

---

**Last Updated**: May 2026  
**Owner**: Coding Standards  
**Target Version**: 1.0+ (Style Frozen)
