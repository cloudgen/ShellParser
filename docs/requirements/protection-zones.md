# Protection Zones Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines all **CIAO-Lite Protection Zones** used throughout ShellParser. These zones are sacred boundaries that protect the battle-tested architecture from accidental or over-eager simplification by AI assistants or future developers.

## 2. Core Philosophy

Protection Zones are the strongest form of **Over-protect** in CIAO-Lite.  
They exist because multiple previous Grok sessions caused regressions by:
- Replacing robust logic with simple regex
- Merging the 3-stage parser
- Using .append() on Attr lists
- Hard-coding brace numbers
- Removing verbose defensive comments

## 3. Official Protection Zone Templates

### File-Level Header (Must appear at top of every .py file)
```python
# =============================================================================
# CIAO DEFENSIVE CODING STYLE - MODULE NAME
# =============================================================================
#
# !!! THIS FILE IS PART OF SHELLPARSER !!!
# !!! ALL OUTPUT MUST GO THROUGH CHRONICLELOGGER !!!
#
# Last aligned with CIAO principles: May 2026
# =============================================================================
```

### Major Function Protection Zone
```python
# =============================================================================
# CIAO-Lite Protection Zone
# DO NOT refactor, simplify, merge stages, or remove without explicit user instruction.
# This section exists for safety and anti-fragility reasons.
# =============================================================================
```

### Sacred Rule Block (Inside Functions)
```python
# Protection Rule (Sacred):
#   Future AI or developers MUST NOT:
#     - Remove or weaken this Protection Zone
#     - Use .append() on Attr lists (use map_array(entry) instead)
#     - Hard-code brace level numbers
#     - Replace 3-stage parser with single-pass logic
#     - Simplify tokenizer (must preserve quoted strings, $(...), `...`)
```

## 4. Critical Protected Areas

| Area                        | Protected Rule                                      | Reason |
|----------------------------|-----------------------------------------------------|--------|
| 3-Stage Pipeline           | Never merge stages                                  | Backward ownership correction is essential |
| tokenize_line()            | Keep enhanced tokenizer (no simple split/regex)    | Prevents brace drift in real shell scripts |
| Attr usage                 | Only direct assignment via map_array()             | StateLogic contract |
| Brace calculation          | Always real count (no hard-coded 0/1/2)            | Stability on complex scripts |
| replace_function()         | Always backup first                                 | Anti-fragile data safety |
| JSON / Quiet mode          | JSON forces quiet=true                              | Clean machine output |
| ChronicleLogger            | Single source of all output                        | Consistency & quiet/JSON support |

## 5. Design Principles (CIAO-Lite)

- **Caution**: Explicitly forbid common failure patterns seen in past sessions.
- **Intentional**: Every zone has documented history and justification.
- **Anti-fragile**: Survives repeated AI-assisted development cycles.
- **Over-protect**: Verbose headers are intentional — never “clean them up”.

## 6. Enforcement Rule

Any change that touches a Protection Zone requires:
1. Explicit user confirmation
2. Updated date in the zone comment
3. Entry in CHANGELOG.md explaining why the exception was granted

Violating a Protection Zone is considered a critical regression.

---

**Last Updated**: May 2026  
**Owner**: CIAO-Lite Compliance  
**Target Version**: 1.0+ (Zones Frozen)
