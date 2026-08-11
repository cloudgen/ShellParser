**file**: docs/requirements/requirement-class-software-dev.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-CLASS-SOFTWARE-DEV  
**Area**: class  
**Project**: ShellParser – AI-augmented shell script component manager  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare this workspace as a **software-development** project and hold residual software-stack facts not owned by a more specific Active requirement: primary language, interpreter policy, packaging tool, and residual ownership pointers.

This file is **class law + residual SSOT**, not a second copy of domain features, CLI tables, or packaging detail when peer requirements own those topics.

## 2. Core Rules (Mandatory — portable)

### 2.0 Project class membership

1. **MUST** treat this workspace as **software-development** (shippable software), not genesis-template and not server-maintenance.  
2. **MUST** use basename **`requirement-class-software-dev.md`** as the sole Active class-law file.  
3. **MUST NOT** register an Active `requirement-class-server-maintenance.md` while class is software-development.  
4. **MUST** retain portable harness knowledge separately from specialized product knowledge in peer `requirement-*.md` files.  
5. **MUST NOT** invent hollow product docs solely to look specialized; collect real values or defer explicitly.

### 2.1 Residual collection principle

6. **MUST** treat this file as the default home for software-stack facts **not owned** by another Active requirement.  
7. **MUST NOT** duplicate full normative tables that live in a more specific Active requirement; prefer a one-line pointer.  
8. When a dedicated requirement takes ownership of a residual topic, **MUST** update this file in the same change (own-or-point).  
9. **MUST NOT** leave contradictory stack facts across this file and peer requirements.

### 2.2 Programming language(s)

10. **MUST** declare at least one primary programming language for the ship unit.  
11. **MUST** state whether the product is primarily interpreted, compiled, polyglot, or multi-package.  
12. **MUST NOT** freeze a marketing product name as if it were the language name.

### 2.3 Toolchain and package tools

13. **MUST** declare the target toolchain class (interpreted runtime vs compile step).  
14. **MUST** state version policy: unconstrained | minimum | range | pinned.  
15. **MUST** declare the primary project/package tool and lockfile policy when the ecosystem supports lockfiles.  
16. **MUST NOT** require secrets or private registry passwords in this file.

### 2.4 Dual policy (class file)

17. **MUST NOT** hard-code a single product brand, production hostname, or personal secret as universal core law.  
18. **MUST** put live product name, repo facts, and concrete versions in Implementation Notes (complete when Status is Active/approved).  
19. **MUST NOT** store secrets, PATs, or toy credentials here.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Project display name** | ShellParser |
| **Project class** | software-development |
| **Class requirement basename** | `requirement-class-software-dev.md` |
| **Primary language(s)** | Python 3 (package `ShellParser`); ships/analyzes POSIX shell script text |
| **Language role** | primary: Python; secondary (analyzed only): POSIX shell sources under user control |
| **Toolchain / interpreter** | CPython |
| **Toolchain version policy** | minimum `>=3.8` (from `pyproject.toml` `requires-python`) |
| **Cross-compile in scope?** | no |
| **Primary project/package tool** | setuptools via PEP 517/621 `pyproject.toml` |
| **Lockfile policy** | not used (dependency declared open range on ChronicleLogger) |
| **Test runner (if law)** | not yet specialized as product law |
| **Linter/formatter (if law)** | not yet specialized as product law |
| **Primary runtime / OS family** | POSIX-friendly local CLI (Linux primary; other OS unproven as law) |
| **Architectures supported** | host Python arch; no special arch set |
| **Git surface** | used (this repository) |
| **Ship unit / install** | yes — Python package + console script; see packaging + domain peers |
| **Code version SSOT (runtime)** | `main()` MAJOR/MINOR/PATCH in `src/ShellParser/cli.py` (currently 1.2.1) |
| **Package metadata version** | `pyproject.toml` `version` (currently 1.2.1); keep aligned with runtime |
| **Identity SSOT** | CLI `shellparser` (+ alias `shell-parser`); version `1.2.1`; repo cloudgen/ShellParser — see packaging peer |

**Residual ownership table:**

| Topic | Owner | Notes |
|-------|--------|--------|
| Project class membership | **this file** | Fixed |
| Primary language / toolchain policy | **this file** | Residual |
| Package/build tool | peer `requirement-python-packaging` | Pointer only after this specialization |
| CLI flags / empty argv | peer `requirement-python-cli-interface` | |
| Output SSOT quiet/json | peer `requirement-python-output-requirements` | |
| Error routing | peer `requirement-python-error-handling` | |
| Domain commands / 3-stage parser | peer `requirement-domain-shellparser` | |
| Backup-before-mutate | peer `requirement-backup-strategy` | |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: Class and stack choices are explicit.  
- **CIAO Principle 5 – SSOT**: Residual stack facts have one home until specialized peers own them.  
- **CIAO Principle 1 – Caution**: Version and toolchain policies are declared; agents do not invent compilers.  
- **CIAO Principle 21 / dual policies**: Portable core; filled Implementation Notes; no secret hardcode.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Assume toolchain and package tools are missing until declared and verified.  
- **Intentional**: Residual collection is deliberate.  
- **Anti-fragile**: Version policies survive multi-env installs.  
- **Over-protect**: Protection rule prevents dual stack SSOTs and genesis pollution.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Treat this workspace as genesis-template while this class file is Active.  
- Rename the specialized basename away from `requirement-class-software-dev.md` without an explicit class-model change.  
- Hard-code one product’s secret into core rules as universal law.  
- Duplicate full peer requirement bodies into this residual section.  
- Leave Implementation Notes as hollow unfinished slots when Status claims Active.  
- Claim unconstrained toolchain support without tests or explicit unconstrained policy.  
- Treat this file as server-maintenance allowlist law.

## 6. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Active registered `requirement-class-software-dev.md` matches software-development class |
| AC-2 | Primary language + toolchain policy + package tool declared in Implementation Notes |
| AC-3 | Residual ownership table honest: no silent dual SSOT with peer REQs |
| AC-4 | Core rules free of frozen secret hardcodes |
| AC-5 | No class file conflict with `requirement-class-server-maintenance` |

## 7. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-PKG-01** | `tests/test_shellparser_core.py` | have |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Covered** for residual stack smoke.

## 8. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-domain-shellparser.md` | Domain product ops |
| `docs/requirements/requirement-python-packaging.md` | Packaging SSOT |
| `docs/requirements/requirement-python-cli-interface.md` | CLI surface |
| `src/ShellParser/` | Ship unit package |
| `pyproject.toml` | Package metadata SSOT |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
