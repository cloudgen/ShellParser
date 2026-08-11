**file**: docs/requirements/requirement-python-error-handling.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-PYTHON-ERROR-HANDLING  
**Area**: python  
**Project**: ShellParser  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how ShellParser handles errors safely: clear messages through the output SSOT, non-destructive defaults when components are missing, and clean failure without corrupting user shell sources.

## 2. Core Rules (Mandatory)

### 2.1 Principles

1. **MUST** prefer safe failure over partial silent corruption of the user script.  
2. **MUST** route error and warning messages through the centralized logger/output module.  
3. **MUST NOT** continue a replace/placeholder write after a failed mandatory pre-check (e.g. missing component file) as if success occurred.

### 2.2 Domain error categories

| Error type | Detection | Required action | Output |
|------------|-----------|-----------------|--------|
| Missing component for replace | before write | Abort replace; instruct to run split | ERROR via logger |
| Unreadable source | open/read | Abort command with clear path error | ERROR |
| Empty parse map when replace needs it | after parse | Abort without writing partial script | ERROR via logger (not raw print) |
| Invalid selection in interactive mode | picker | Reprompt or exit cleanly | human guidance via logger |
| JSON mode failure | any | Do not mix traceback chatter with JSON object | pure error handling + mode rules |

4. **MUST** create dated backup **before** successful mutate paths (backup peer); if backup cannot be created, **MUST NOT** proceed to overwrite source.  
5. **MUST NOT** treat user shell scripts as ephemeral temps: they are configuration/user content for backup classification.

### 2.3 Exceptions and stack traces

6. Unhandled exceptions **SHOULD** fail closed; in normal mode, messages **MUST** remain actionable.  
7. Under JSON mode, **MUST NOT** dump multi-line human stack traces onto the same stream as the sole success JSON object without a defined error JSON contract.

### 2.4 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Logger** | ChronicleLogger via `ShellParserCore.logger` |
| **Replace missing component** | logs error + “Run split first…” and returns False |
| **Backup failure posture** | backup writes before mutate; OS errors should abort (fail closed) |
| **Empty parse path** | `logger.log_message("Error: No parsed data available", level="error")` (aligned 2026-08-11) |
| **Network errors** | N/A for core domain (no network required) |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution**: Fail closed on missing inputs.  
- **CIAO Principle 12 – Backup**: Mutate only after recovery path.  
- **CIAO Principle 5 – Output SSOT**: Errors through logger.  
- **CIAO Principle 20 / O**: Keep defensive abort paths.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Missing component ≠ empty successful replace.  
- **Intentional**: Error tables map to domain verbs.  
- **Anti-fragile**: Interactive and CLI share abort semantics.  
- **Over-protect**: No silent overwrite after failed pre-check.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Swallow replace failures as success.  
- Remove backup-before-mutate on replace/placeholder.  
- Reintroduce raw print as the primary error channel.  
- Continue writing the user script after backup creation failed.

## 6. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-ERR-01** | `tests/test_shellparser_core.py` | have |
| **TP-ERR-02** | (planned) | todo |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Partial** — missing component **have**; empty-map logger path **todo**.

## 7. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-domain-shellparser.md` | Domain verbs |
| `docs/requirements/requirement-python-output-requirements.md` | Output channel |
| `docs/requirements/requirement-backup-strategy.md` | Backup law |
| `src/ShellParser/cli.py` | Implementation |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
