# State Machine Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the usage of StateLogic FSM (Finite State Machine) pattern in ShellParserCore.

## 2. Core Implementation

- ShellParserCore inherits from StateLogic
- Uses Attr descriptors for all state variables
- Explicit transition() calls in __init__
- Hooks (before/after/on) for key stages
- Main flow coordinated in afterStartParse()

## 3. Defined States & Transitions

- backup_source → backed_or_no_need
- start_parse → line_read → tokenize → line_parsed → next_line
- last_line → parse_end → split_file (for replace)

## 4. Key Rules

- All parser state managed through Attr (autostrip=False where needed)
- Direct assignment only: self.map_array(entry) — never .append()
- Hooks registered once and never mutated
- Single core instance used across all commands

## 5. Design Principles (CIAO-Lite)

- Caution: Strict FSM prevents scattered state logic
- Intentional: Clear separation of concerns via states and hooks
- Anti-fragile: Easy to debug with STATE=show environment variable
- Over-protect: FSM structure is protected from refactoring

## 6. Protection Rule (Sacred)

Future AI or developers MUST NOT:
- Bypass StateLogic transitions
- Add direct loops outside of defined hooks
- Modify Attr declarations or contract
- Remove or weaken any FSM hook
- Change state names without updating all references

## 7. Future Enhancements

- More granular states for advanced parsing
- Visual state diagram generation (debug mode)

---

**Last Updated**: May 2026  
**Owner**: State Engine  
**Target Version**: 1.0+ (FSM Frozen)
