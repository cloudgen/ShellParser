# Versioning Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the official versioning strategy for ShellParser, including independent component versioning, semantic versioning rules, and how versions are maintained across the codebase and documentation.

## 2. Versioning Scheme

ShellParser uses **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):

- **MAJOR**: Incompatible API or architecture changes (e.g., breaking changes to parser output format)
- **MINOR**: New features or significant enhancements (e.g., `split-docs` command in v2.0)
- **PATCH**: Backward-compatible bug fixes and small improvements

### Independent Component Versioning (CIAO Style)

Every major class/module maintains its own version:

```python
class ShellParserCore(StateLogic):
    CLASSNAME = "ShellParserCore"
    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 2

    @staticmethod
    def class_version():
        return f"{ShellParserCore.CLASSNAME} v{ShellParserCore.MAJOR_VERSION}.{ShellParserCore.MINOR_VERSION}.{ShellParserCore.PATCH_VERSION}"
```

## 3. Version Locations (Single Source of Truth)

| Location                        | Purpose                                      | Must Update On Change |
|---------------------------------|----------------------------------------------|-----------------------|
| `pyproject.toml`                | PyPI / pip package version                   | Yes                   |
| `ShellParserCore.class_version()` | Runtime version reporting                    | Yes                   |
| `main()` in `cli.py`            | Startup banner and debug output              | Yes                   |
| `CHANGELOG.md`                  | Human readable history                       | Yes                   |
| `README.md`                     | Badge and documentation                      | Yes                   |
| Requirements `.md` files        | Target Version field                         | Yes                   |

## 4. Release Process

1. Update `CHANGELOG.md` (new section at top)
2. Bump version in `pyproject.toml`
3. Update `ShellParserCore` version constants
4. Update version in `main()`
5. Update any affected requirements documents
6. Run full test cycle (`split` + `replace` + `split-docs`)
7. Tag release in git (`v1.1.0`)

## 5. Design Principles (CIAO-Lite)

- **Caution**: Version must be visible at runtime (`about` command) and in logs.
- **Intentional**: Independent component versioning allows different modules to evolve at different speeds.
- **Anti-fragile**: Clear changelog + semantic rules prevent accidental breaking changes.
- **Over-protect**: All version numbers are explicitly documented and protected.

## 6. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Hard-code version numbers in multiple places without updating all locations.
- Remove or weaken independent component versioning (`class_version()` method).
- Change version format without updating `CHANGELOG.md` and all references.
- Bump version without a corresponding changelog entry.
- Remove version information from `about` or `help` commands.
- Use date-based versioning instead of Semantic Versioning.

## 7. Milestone Alignment

- **v1.0+**: Current stable versioning
- **v1.1**: Complete requirements suite + parameters/output docs
- **v2.0**: `split-docs` command + markdown output
- **v3.0**: Semantic extraction
- **v4.0**: SQLite database with version tracking

---

**Last Updated**: May 2026  
**Owner**: Versioning System  
**Target Version**: 1.1 (Versioning Rules Stable)
