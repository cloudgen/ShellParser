**file**: docs/requirements/requirement-python-cli-interface.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-PYTHON-CLI-INTERFACE  
**Area**: python  
**Project**: ShellParser  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official Python CLI surface for ShellParser: entry routing, global flags, empty-argv behavior (Type N interactive), and the relationship between argparse subcommands and interactive mode. Domain verb semantics live in the domain requirement; this file owns the **interface contract**.

## 2. Core Rules (Mandatory)

### 2.1 Empty argv (Type N)

1. Unless the product also specializes online install empty-argv Type O (this product does **not**), bare invocation without a subcommand **MUST** show help **or** interactive prompts as designed — **Type N**.  
2. **MUST NOT** default empty argv to channel install-ensure.  
3. For ShellParser, empty argv **MUST** enter **interactive mode** (recommended daily workflow).

### 2.2 Global flags

4. **MUST** support `--quiet` to suppress non-essential human output.  
5. **MUST** support `--json` for machine-readable success/status output.  
6. When `--json` is set, **MUST** imply quiet behavior so human chatter does not pollute JSON (output peer owns emission rules).  
7. Flags **MUST** be honored both as top-level options and as subcommand options where the dispatcher implements them.

### 2.3 Subcommand interface

8. **MUST** expose domain subcommands registered by the domain requirement (`split`, `replace`, `split-docs`, `placeholder`, `about`, `help`).  
9. **MUST** parse required operands for mutating/read domain verbs (`source_file`, and `func_name` for replace).  
10. **MUST** keep a single main entry function that initializes the logger and one orchestrator core per run.

### 2.4 Interactive mode

11. Interactive mode **MUST** present a menu covering domain verbs (split, replace, split-docs, placeholder, about/help, exit).  
12. Interactive pickers **MUST** list candidate shell scripts / components without bypassing the same core code paths used by CLI verbs.  
13. Interactive mode **MUST** route all user-facing messages through the output SSOT (no free-form parallel UI stack).

### 2.5 Non-interactive honesty

14. In non-interactive environments, argparse path **MUST** remain usable without hanging on prompts when a full subcommand + operands is supplied.  
15. **MUST NOT** require TTY for `split` / `replace` / `split-docs` / `placeholder` when paths are provided.

### 2.6 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Package entry** | `ShellParser.cli:main` |
| **Console script (primary)** | `shellparser` |
| **Console script (alias)** | `shell-parser` (same entry; compatibility) |
| **Help/README documented name** | `shellparser` (aligned) |
| **Empty argv** | Type N → `interactive_mode(logger)` when `len(sys.argv)<=1` or only `--quiet`/`--json` |
| **Orchestrator** | `ShellParserCore` |
| **Logger** | `ChronicleLogger(logname='ShellParser')` then `logName()` / `baseDir()` for path resolution |
| **Subcommands** | split, replace, split-docs, placeholder, about, help |
| **Global flags** | `--quiet`, `--json` |
| **Install mode** | local-only Python package (`pip install`); **not** online Type O CLI |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 16 – Interactive awareness**: Empty argv is intentionally interactive; full argv stays scriptable.  
- **CIAO Principle 15 – Helpful surfaces**: help/about and menu stay discoverable.  
- **CIAO Principle 5 – SSOT**: One entry + one core per invocation.  
- **CIAO Principle 21**: Portable core rules; concrete names in notes.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Prefer interactive selection when operands missing.  
- **Intentional**: Type N empty argv is declared, not assumed.  
- **Anti-fragile**: CLI path works without TTY when fully specified.  
- **Over-protect**: Do not add a second procedural CLI outside the orchestrator without redesign.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Change empty-argv from interactive Type N to silent no-op or Type O install without explicit law change.  
- Remove `--quiet` / `--json` support.  
- Add business logic outside `main` + `ShellParserCore` as a parallel CLI.  
- Document a console command name that does not match the installed entry without recording the drift as a Gap.  
- Move domain verb semantics solely into this file (domain peer owns four pillars).

## 6. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-01** | `tests/test_shellparser_core.py` | have |
| **TP-CLI-02** | `tests/test_shellparser_core.py` | have |
| **TP-SHELLPARSER-05** | (planned) | todo |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Partial** — flags/help **have**; empty-argv interactive **todo**.

## 7. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-domain-shellparser.md` | Domain verbs |
| `docs/requirements/requirement-python-output-requirements.md` | quiet/json emission |
| `docs/requirements/requirement-python-packaging.md` | console script name |
| `src/ShellParser/cli.py` | Implementation |
| `pyproject.toml` | Entry point declaration |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
