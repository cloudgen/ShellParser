**file**: docs/requirements/requirement-python-output-requirements.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-PYTHON-OUTPUT-REQUIREMENTS  
**Area**: python  
**Project**: ShellParser  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define mandatory output behavior for the ShellParser Python CLI: a single centralized output module, respect for quiet and JSON modes, and prohibition of ad-hoc prints that break machine-readable contracts.

## 2. Core Rules (Mandatory)

### 2.1 Centralized output module (Sacred)

1. **All** user-facing and machine-readable product messages **MUST** go through the centralized output/logging module.  
2. **Forbidden** in product paths that claim quiet/JSON compliance: raw `print()` for normal success paths, direct `sys.stdout`/`sys.stderr` writes, and ad-hoc `logging` that bypasses the module.  
3. Debug/internal diagnostics **MUST** still route through the same module so quiet/json can suppress them.

### 2.2 Mode matrix

| Mode | Quiet | JSON | Behavior |
|------|-------|------|----------|
| Normal | false | false | Human-readable progress and messages |
| Quiet | true | false | Suppress non-essential output; errors/critical still allowed |
| JSON | true (implied) | true | Machine-readable JSON status; no mixed human chatter on the JSON channel |

4. When JSON mode is true, the implementation **MUST** suppress non-JSON chatter that would corrupt consumers.  
5. JSON mode **MUST** imply quiet (or equivalent) so dual channels do not race.

### 2.3 Path / storage resolution

6. Base directories for logs/target resolution **SHOULD** come from the centralized logger configuration (not hard-coded absolute product homes scattered through the parser).  
7. Relative product outputs (`target/components`, `target/docs`) **MUST** remain project-local paths as domain law defines.

### 2.4 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Output module** | ChronicleLogger (`from ChronicleLogger import ChronicleLogger`) |
| **Primary methods used** | `log_message`, `prn`, quiet controls via `logger.quiet(...)` |
| **JSON flag wiring** | `core.is_json(...)`; `--json` forces `logger.quiet(True)` in `main` |
| **Orchestrator** | `ShellParserCore` holds logger reference; domain methods call `self.logger.*` |
| **Error paths** | Empty parse / missing component use `logger.log_message(..., level="error")` (no raw print) |
| **JSON about/help** | Intentional `print(json.dumps(...))` so JSON is not silenced by quiet (machine channel) |
| **Interactive picker** | Temporary direct print only inside `_pick_file` for picker UX; must not break `--json` non-interactive paths |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – Single source of output**: ChronicleLogger is the SSOT.  
- **CIAO Principle 1 – Caution**: Quiet/JSON must not leak mixed streams.  
- **CIAO Principle 16**: Interactive vs non-interactive both honor modes.  
- **CIAO Principle 20 / O**: Protection against AI reintroducing print-based I/O.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Never assume stdout is free for ad-hoc text under JSON.  
- **Intentional**: Mode matrix is explicit.  
- **Anti-fragile**: Logger configuration can relocate bases without rewriting domain logic.  
- **Over-protect**: Ban parallel output stacks.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Introduce `print()` success paths that bypass ChronicleLogger in domain operations.  
- Invert priority so quiet wins over JSON purity.  
- Hard-code log directory absolute paths inside the parser core.  
- Claim full JSON compliance while human text still appears on the same stream as the JSON object.

## 6. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-02** | `tests/test_shellparser_core.py` | have |
| **TP-OUT-01** | `tests/test_shellparser_core.py` | have |
| **TP-ERR-02** | (planned) | todo |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Covered** for Core quiet/JSON purity paths.

## 7. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-interface.md` | Flag contract |
| `docs/requirements/requirement-domain-shellparser.md` | Domain messages |
| `src/ShellParser/cli.py` | Implementation |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
