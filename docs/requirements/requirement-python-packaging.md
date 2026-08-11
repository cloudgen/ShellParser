**file**: docs/requirements/requirement-python-packaging.md  
**Status**: Active (Version 1.0.0)  
**id**: RQ-PYTHON-PACKAGING  
**Area**: python  
**Project**: ShellParser  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define packaging standards for ShellParser as a Python PyPI-style execution project: `pyproject.toml` as package metadata SSOT, console entry points, dependency declaration, and version alignment discipline.

## 2. Core Rules (Mandatory)

### 2.1 Primary manifest

1. **`pyproject.toml` MUST** be the primary packaging manifest (PEP 517/621).  
2. **MUST** declare: name, version, description, authors, requires-python, dependencies, build-system, console scripts.  
3. **`requirements.txt` MUST NOT** be the primary dependency SSOT for published install.

### 2.2 Console entry

4. Console script entry **MUST** point at a minimal `main()` that initializes logger + core and dispatches.  
5. Entry **MUST NOT** embed domain business logic outside the orchestrator class.  
6. Documented command name, console script name, and help usage strings **SHOULD** match; if they drift, **MUST** record an honest Gap until aligned.

### 2.3 Dependencies

7. Runtime dependencies **MUST** be declared in `pyproject.toml`.  
8. Secrets **MUST NOT** appear in packaging files.  
9. Dependency version policy **MUST** be intentional (open range vs pin) and stated in notes.

### 2.4 Version alignment

10. Package version in `pyproject.toml` and runtime version reported by the CLI **SHOULD** match for any tagged release.  
11. When they differ during development, **MUST NOT** claim both as authoritative without stating which is release SSOT.

### 2.5 Layout

12. Importable package **MUST** live under a clear package directory (here: `src/ShellParser/`).  
13. Optional Cython/extension sources under `src/` **MUST NOT** silently replace the Python package entry without packaging notes.

### 2.6 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Distribution name** | ShellParser |
| **Import package** | `ShellParser` |
| **Manifest** | `pyproject.toml` |
| **Build backend** | setuptools (`setuptools.build_meta`) |
| **requires-python** | `>=3.8` |
| **Runtime dependency** | `ChronicleLogger>=1.3.1` |
| **Console script** | `shell-parser = "ShellParser.cli:main"` |
| **License** | MIT (`LICENSE.md`) |
| **Version (package)** | `1.2.1` in `pyproject.toml` |
| **Version (runtime main)** | 1.2.1 (MAJOR/MINOR/PATCH in `cli.py`) |
| **Version (package `__init__`)** | may lag; align to package/runtime on release |
| **Install modes** | `pip install ShellParser` / `pip install -e .` — local package only |
| **Identity SSOT (aligned 2026-08-11)** | Primary console `shellparser`; alias `shell-parser`; repo `https://github.com/cloudgen/ShellParser`; version `1.2.1` |
| **Legacy** | `src/setup.py` present historically; packaging SSOT remains `pyproject.toml` |

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT**: One packaging manifest.  
- **CIAO Principle 1 – Caution**: Explicit Python and dependency bounds.  
- **CIAO Principle 15**: Installable entry point is discoverable.  
- **CIAO Principle 21**: Notes hold product-specific packaging facts.

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Do not dual-own dependencies in free-floating lists.  
- **Intentional**: Entry point and version policy explicit.  
- **Anti-fragile**: PEP 517 tools can rebuild without bespoke steps.  
- **Over-protect**: Prevent silent entry-point renames without docs/law update.

## 5. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Move primary dependency SSOT to an undocumented `requirements.txt`.  
- Change console script name without updating help, README, and this requirement.  
- Embed secrets or tokens in packaging metadata.  
- Claim PyPI identity fields without disk-truth alignment.  
- Delete `pyproject.toml` in favor of setuptools-only legacy without redesign order.

## 6. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-PKG-01** | `tests/test_shellparser_core.py` | have |
| **TP-PKG-02** | `tests/test_shellparser_core.py` | have |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`.

Coverage verdict (map): **Covered**.

## 7. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-class-software-dev.md` | Class residual pointer |
| `docs/requirements/requirement-python-cli-interface.md` | CLI name contract |
| `pyproject.toml` | Packaging SSOT |
| `src/ShellParser/` | Package body |
| `README.md` | Install user surface |

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
