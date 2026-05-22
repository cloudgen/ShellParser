# Attr Contract & StateLogic Usage Requirements - ShellParser

**Status**: Active (Version 1.0+ → 2.1)

## 1. Purpose

This document defines the strict contract and proper usage of the **Attr** descriptor (from StateLogic) in ShellParserCore.

## 2. Relationship Between Packages

- **ChronicleLogger**: Single source of all program output
- **StateLogic + Attr**: Finite State Machine and all parser state management
- Never mix their responsibilities.

## 3. Proper ChronicleLogger Usage (Mandatory)

(See logging.md — unchanged)

## 4. Proper Attr Usage Contract (Strict)

### Core Rules (Sacred)

- All state variables **must** be declared with `Attr(...)` in `ShellParserCore.__init__()`
- Access **only** via getter/setter: `self.name()` and `self.name(new_value)`
- For lists: `self.map_array(entry)` — **NEVER** `.append()`
- Never use direct attribute assignment (`self.xxx = yyy`)

### Currently Declared Mode Flags (v2.1)

| Attr Name              | Type    | Default | Purpose                                                      | Used In                        |
|------------------------|---------|---------|--------------------------------------------------------------|--------------------------------|
| `replace_mode`         | bool    | False   | Enable replace workflow + backup                             | replace command                |
| `output_enabled`       | bool    | True    | Control whether Stage 3 writes files                         | split / split-docs / placeholder |
| `docs_mode`            | bool    | False   | Select split-docs (markdown) vs classic split                | split-docs command             |
| **`placeholder_mode`** | **bool** | **False** | **Replace all functions (except top-block) with placeholders** | **placeholder command (v2.1)** |
| `is_json`              | bool    | False   | JSON output mode                                             | show_about / show_help         |
| `is_quiet`             | bool    | False   | Quiet mode                                                   | logger control                 |

### Declaration Example (v2.1 addition)

```python
# In ShellParserCore.__init__()
Attr(self, attrName='placeholder_mode', value=False)
```

## 5. Usage in Central Coordinator (`afterStartParse()`)

```python
if self.output_enabled():
    self.stage_1_report()
    self.stage_2_ownership()
    
    if self.docs_mode():
        self.stage_3_write_docs()
    elif self.placeholder_mode():           # ← New v2.1
        self.stage_3_create_placeholder()
    else:
        self.stage_3_extract_functions()    # Classic behavior
```

## 6. Design Principles (CIAO-Lite)

- **Caution**: All mode switches must go through Attr to maintain StateLogic contract.
- **Intentional**: `placeholder_mode` provides clean, explicit differentiation.
- **Anti-fragile**: Prevents fragile command-line string checks inside the FSM.
- **Over-protect**: New Attr is declared in `__init__()` and protected by CIAO-Lite zones.

## 7. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Bypass or remove the `placeholder_mode` Attr
- Add new mode flags without declaring them via `Attr()` in `__init__()`
- Use `.append()` on any Attr-managed list
- Access state via direct attributes (`self.__dict__` or `self.xxx = yyy`)
- Hard-code mode detection (e.g. checking `sys.argv` inside parser methods)
- Remove or weaken any Attr-related Protection Zone

## 8. Validation Checklist (for every change)

- [ ] All new state variables declared with `Attr()` in `__init__()`
- [ ] `placeholder_mode` respected in `afterStartParse()` and control paths
- [ ] No direct assignment or `.append()` on Attr lists
- [ ] All mode flags documented in this file and `cli-interface.md`

---

**Last Updated**: May 11, 2026  
**Owner**: State & Logging Contract  
**Target Version**: 2.1 (Added `placeholder_mode` Attr)

**Alignment**: Fully synchronized with `milestones.md`, `parser-architecture.md`, `cli-interface.md`, and `interactive-mode.md`.
