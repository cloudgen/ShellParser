# Build and Packaging Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines how ShellParser is built, packaged, and distributed.

## 2. Packaging Standards

- Modern Python packaging using pyproject.toml + setuptools
- Installable via pip: `pip install ShellParser`
- Provides console script: `shell-parser`
- Editable install support: `pip install -e .`

## 3. Build Commands

```bash
# Development
pip install -e .

# Clean build
rm -rf build dist *.egg-info target/

# Install from source
pip install .
```

## 4. Key Files

- pyproject.toml — Build configuration and entry points
- src/ShellParser/__init__.py — Package metadata
- src/ShellParser/cli.py — Main implementation
- setup is fully declarative (no setup.py)

## 5. Target Directory Structure

- target/components/ → Extracted function files
- target/report/ → Stage 1 classification report
- target/ is gitignored

## 6. Design Principles (CIAO-Lite)

- Caution: Clean separation between source and build artifacts
- Intentional: pyproject.toml as Single Source of Truth for packaging
- Anti-fragile: Works in virtualenvs, conda, pyenv, Docker, etc.
- Over-protect: target/ directory is strictly for generated content

## 7. Protection Rule (Sacred)

Future AI or developers MUST NOT:
- Add setup.py if pyproject.toml is sufficient
- Hard-code paths outside of ChronicleLogger resolution
- Remove editable install support
- Change console script name without updating all references
- Pollute source directory with build artifacts

## 8. Future Enhancements

- Wheel and source distribution publishing to PyPI
- GitHub Actions CI/CD pipeline
- Version bumping automation

---

**Last Updated**: May 2026  
**Owner**: Build System  
**Target Version**: 1.0+ (Packaging Stable)
