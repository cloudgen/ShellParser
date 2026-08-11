**file**: docs/requirements/requirement-domain-shellparser.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-DOMAIN-SHELLPARSER  
**Area**: domain  
**Project**: ShellParser  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define **domain product law** for ShellParser: parsing monolithic shell scripts into components, safe function replacement, LLM-oriented markdown export, mass placeholder rewrite, and the interactive daily workflow. This is the **single Active domain SSOT** for specialized subcommands, features, help items, and about items beyond pure packaging/output plumbing.

## 2. Core Rules (Mandatory)

### 2.1 Domain SSOT

1. **MUST** keep exactly one Active domain requirement for ShellParser domain surface (this file).  
2. **MUST NOT** treat class or generic python packaging REQs as owners of domain verbs.  
3. **MUST** preserve the **3-stage parser** architecture as product law:  
   - Stage 1: forward line classification / tokenization  
   - Stage 2: backward ownership correction  
   - Stage 3: extract write (`target/components`) or docs write (`target/docs`) or placeholder path  
4. **MUST NOT** replace the 3-stage design with a single-pass regex splitter without an explicit authorized redesign.  
5. **MUST** keep CIAO-Lite Protection Zones on the parser stages, replace path, and interactive mode unless the user explicitly orders a redesign of those sections.

### 2.2 Specialized CLI subcommands (pillar 1)

| Verb | Operands | Behavior (MUST) | Mutates source? |
|------|----------|-----------------|-----------------|
| `split` | `source_file` | Parse shell script; write `target/components/<func>.sh` (plus stage report as implemented) | No (read source) |
| `replace` | `source_file` `func_name` | Backup source first; rebuild script replacing only that function from `target/components/<func_name>.sh` | Yes (after backup) |
| `split-docs` | `source_file` | Same parse pipeline; write LLM-friendly `target/docs/<func>.md` | No |
| `placeholder` | `source_file` | Backup once; replace all functions except protected top-block with placeholder skeletons via the same replace mechanism | Yes (after backup) |
| `about` | none | Environment / version / identity info via output SSOT | No |
| `help` | none | Usage surface for domain + flags | No |

6. **MUST** implement the verbs above in the dispatcher (`main` / interactive router).  
7. **MUST** route empty argv (and argv of only global quiet/json flags) to **interactive mode** (Type N) — not online install-ensure.  
8. **MUST NOT** invent `self-install` / channel place-remove as domain verbs for this product (local Python package install only).

### 2.3 Specialized features (pillar 2)

9. **Function extraction** — **MUST** preserve original function body content and whitespace when writing components.  
10. **Ownership map** — Stage 2 map **MUST** be the SSOT for which lines belong to which function before Stage 3 write.  
11. **Replace safety** — **MUST** refuse replace when component file is missing; **MUST** backup before write (see backup peer).  
12. **split-docs markdown shape** — **MUST** keep the fixed markdown skeleton:

```markdown
# Function: <name>

## Metadata
- Extracted: <timestamp>
- Source File: <abs path>
- Line Range: <start>-<end>
- Line Count: <n>

## Description
<!-- optional -->

```sh
<original body>
```
```

13. **placeholder** — **MUST** reuse the battle-tested replace path one function at a time; **MUST NOT** reimplement reassembly with a parallel algorithm.  
14. **Protected names** — **MUST NOT** placeholder-replace `top-block` (and other protected names as implemented, e.g. `main-entry` exclusion rules already in code).  
15. **Single core instance** — CLI path **MUST** use one `ShellParserCore` instantiation per invocation for consistent logger/state.

### 2.4 Specialized project help items (pillar 3)

Help **MUST** document at least:

| Help item | Required content |
|-----------|------------------|
| Usage line | Primary CLI name + `<command> [--quiet] [--json]` |
| `split` | Components output under `target/components/` |
| `replace` | Function replace + backup mention |
| `split-docs` | Markdown under `target/docs/` |
| `placeholder` | Mass placeholder with backup (when command is shipped) |
| `about` / `help` | Info surfaces |
| Flags | `--quiet`, `--json` (json implies quiet) |
| Workflow | split → edit → replace |

### 2.5 Specialized project about items (pillar 4)

About **MUST** expose product/runtime identity fields useful for support (version components, logger version when debug, target paths as implemented). Domain about may include parser/tooling versions; **MUST** stay consistent with packaging version policy when claiming a release.

### 2.6 Non-goals

16. **MUST NOT** claim full shell language completeness beyond the battle-tested tokenizer/classifier scope.  
17. **MUST NOT** require network install channels for domain operation.  
18. **MUST NOT** delete user sources without backup on replace/placeholder paths.

### 2.7 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Product** | ShellParser |
| **Orchestrator class** | `ShellParserCore` in `src/ShellParser/cli.py` |
| **Entry** | `ShellParser.cli:main` (console script currently `shell-parser` in `pyproject.toml`) |
| **Documented CLI name** | `shellparser` in help/README (known naming drift vs console script — resolve under packaging/CLI peers) |
| **Runtime version block** | MAJOR=1 MINOR=2 PATCH=1 in `main()` |
| **Package export** | `ChronicleLogger`, `ShellParserCore` from `ShellParser` package (`__version__` may lag package metadata — keep aligned) |
| **Dependencies** | `ChronicleLogger>=1.3.1` |
| **Interactive menu** | 1=split, 2=replace, 3=split-docs, 4=placeholder, 5=about/help, 0=exit |
| **Components path** | `target/components/<func>.sh` |
| **Docs path** | `target/docs/<func>.md` |
| **Backup pattern** | `<basename>.YYYYMMDD-N` beside source (see RQ-BACKUP-STRATEGY) |
| **Protection zones** | Parser stages, replace, split-docs Stage 3, placeholder reuse rule, interactive mode, main single-core rule |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: Domain verbs and parser stages are deliberate product law.  
- **CIAO Principle 5 – SSOT**: Ownership map and component paths are single sources for reassembly.  
- **CIAO Principle 12 – Backup**: Mutating replace/placeholder only after recovery path (peer).  
- **CIAO Principle 20 / O – Over-protect**: Protection Zones stop AI regression of the 3-stage parser.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Backup before mutate; fail if component missing.  
- **Intentional**: Interactive menu mirrors dispatcher verbs.  
- **Anti-fragile**: Additive split-docs must not break classic split/replace.  
- **Over-protect**: Sacred stages and replace reuse for placeholder.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Collapse the 3-stage parser into an untested single regex path without explicit redesign order.  
- Rewrite replace/placeholder reassembly without reusing the protected replace mechanism.  
- Drop `split-docs` markdown skeleton compatibility without authorized versioned change.  
- Remove interactive empty-argv workflow without replacing Type N help behavior honestly.  
- Claim domain law complete while omitting any of the four pillars.  
- Move domain verb catalogs into packaging-only requirements as sole SSOT.

## 6. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-SHELLPARSER-01** | `tests/test_shellparser_core.py` | have |
| **TP-SHELLPARSER-02** | `tests/test_shellparser_core.py` | have |
| **TP-SHELLPARSER-03** | `tests/test_shellparser_core.py` | have |
| **TP-SHELLPARSER-04** | `tests/test_shellparser_core.py` | have |
| **TP-BAK-01** | `tests/test_shellparser_core.py` | have |
| **TP-CLI-01** | `tests/test_shellparser_core.py` | have |
| **TP-SHELLPARSER-05** | (planned) | todo |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Covered** for Core domain integrity (top-block on replace); interactive Type N still **todo**.

## 7. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-class-software-dev.md` | Class law |
| `docs/requirements/requirement-python-cli-interface.md` | Flags / Type N |
| `docs/requirements/requirement-python-output-requirements.md` | Output SSOT |
| `docs/requirements/requirement-backup-strategy.md` | Backup before mutate |
| `src/ShellParser/cli.py` | Domain implementation |
| `README.md` | User-facing overview |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
