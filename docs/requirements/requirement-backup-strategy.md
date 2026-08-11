**file**: docs/requirements/requirement-backup-strategy.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-BACKUP-STRATEGY  
**Area**: ops  
**Project**: ShellParser  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the recoverable backup policy for ShellParser operations that mutate user shell scripts (replace and placeholder). Aligns with CIAO Principle 12: recovery proportionate to risk — user scripts are durable content, not temps.

## 2. Core Rules (Mandatory)

### 2.1 Data classification (this product)

| Class | Examples in ShellParser | Rule |
|-------|-------------------------|------|
| **EPHEMERAL** | in-memory parse maps, temp counter loops | No museum copies required |
| **REGENERABLE** | `target/components/*.sh`, `target/docs/*.md` after re-split | Optional dated backup; can regenerate via `split` / `split-docs` |
| **CONFIGURATION / USER SCRIPT** | the user’s `source_file` shell script | **MUST** dated backup **before** in-place replace/placeholder rewrite |
| **CREDENTIAL** | N/A for core domain | Do not invent secret backup rituals in this product |

1. **MUST** treat the operator’s source shell script as durable user content for mutate paths.  
2. **MUST NOT** require dated backups of regenerable `target/` extracts as a precondition for split (split does not mutate source).

### 2.2 When backup is mandatory

3. **MUST** create a dated backup of `source_file` **before** any successful in-place rewrite for:  
   - `replace`  
   - `placeholder`  
4. **MUST NOT** write the mutated script until the backup file has been written successfully.  
5. **MUST** keep the backup beside the source (same directory) unless a future authorized redesign relocates it.

### 2.3 Naming

6. Backup basename pattern **MUST** be:

```text
<source-basename>.YYYYMMDD-N
```

where `YYYYMMDD` is the local date and `N` increments while a same-day name already exists.

7. **MUST NOT** overwrite an existing backup name; always allocate the next free `N`.

### 2.4 Restore posture

8. Operators restore by copying the backup over the source (or equivalent). Product **SHOULD** log the backup path clearly after creation.  
9. Product **MUST NOT** auto-delete backups as part of replace success.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Backup creator** | `ShellParserCore.after_backup_source` |
| **Pattern** | `{basename}.{YYYYMMDD}-{counter}` e.g. `myscript.sh.20260811-1` |
| **FSM** | transition into `start_backup` before parse/replace paths for mutate commands |
| **placeholder** | reuses same backup-first entry (`state('start_backup')` then `backup_source`) |
| **split / split-docs** | no source backup required (non-mutating) |
| **Log component** | `replace` (and related) via ChronicleLogger |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 12 – Right backup & restore**: Mutating user scripts without recovery is forbidden.  
- **CIAO Principle 1 – Caution**: Fail closed if backup cannot be made.  
- **CIAO Principle 10 – Temps**: Temps are not a substitute for durable backups.  
- **CIAO Principle 20 / O**: Keep backup-before-replace protection zones.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Backup first, write second.  
- **Intentional**: Only mutate paths require source backups.  
- **Anti-fragile**: Incrementing `N` avoids clobbering same-day backups.  
- **Over-protect**: Do not “optimize away” backups for convenience.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Remove backup-before-replace/placeholder.  
- Overwrite an existing backup path.  
- Claim replace is safe without a restorable copy.  
- Treat user scripts as EPHEMERAL for backup classification.  
- Auto-delete backups on success without explicit user-ordered retention redesign.

## 6. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-BAK-01** | `tests/test_shellparser_core.py` | have |
| **TP-BAK-02** | `tests/test_shellparser_core.py` | have |
| **TP-SHELLPARSER-03** | `tests/test_shellparser_core.py` | have |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Covered**.

## 7. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-domain-shellparser.md` | Mutating verbs |
| `docs/requirements/requirement-python-error-handling.md` | Fail closed if backup fails |
| `src/ShellParser/cli.py` | `after_backup_source` |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
