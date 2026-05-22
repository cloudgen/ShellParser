# Replace Workflow Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the safe replace workflow used by ShellParser for updating individual functions from the extracted components back into the original monolithic script.

## 2. Scope / Milestones Alignment

- Version 1.0+: Current backup-before-replace mechanism is stable and sacred.
- All replace operations must follow this exact flow.

## 3. Core Replace Workflow (Step by Step)

1. User runs: shellparser replace <source_file> <func_name>
2. Enter backup_source state → create dated backup first (*.YYYYMMDD-N)
3. Load the component file from target/components/<func_name>.sh
4. Rebuild the full script using map_array_for_file
5. Override ONLY the target function with the new content
6. Write the updated script back to the original location
7. Log success via ChronicleLogger

## 4. Safety Rules (Mandatory)

- Backup is ALWAYS created BEFORE any modification
- Backup naming: <original>.YYYYMMDD-N (incremental counter)
- Original file is never touched until backup succeeds
- Only one function is replaced — all other code remains untouched
- Works in both interactive and command-line modes

## 5. Design Principles (CIAO-Lite)

- Caution: Backup-first strategy prevents data loss
- Intentional: Explicit separation of backup and replace logic
- Anti-fragile: Survives failed writes or interrupted operations
- Over-protect: Replace mode disables component overwriting (output_enabled=False)

## 6. Protection Rule (Sacred)

Future AI or developers MUST NOT:
- Remove the backup step
- Write directly to original file without backup
- Modify replace_function() without explicit approval
- Change backup naming convention
- Bypass output_enabled switch in replace mode

## 7. Future Enhancements

- Optional dry-run mode (--dry-run)
- Multi-function replace support
- Diff preview before applying changes

---

**Last Updated**: May 2026  
**Owner**: Replace Engine  
**Target Version**: 1.0+ (Workflow Frozen)
