# Security Policy

## Overview

**ShellParser** is a specialized AI-augmented tool for safely splitting, editing, and reassembling large, complex legacy shell scripts.

Its core responsibility is **safe bidirectional transformation** between monolithic shell scripts and small, single-responsibility component files (`target/components/*.sh`). Because it performs file parsing, function extraction, and in-place replacement with backups, **reliability, correctness, and anti-fragility** are paramount.

ShellParser follows the **[CIAO defensive programming philosophy](https://github.com/cloudgen/ciao)** (Caution • Intentional • Anti-fragile • Over-protect) to survive repeated editing by humans and AI assistants (Grok, Claude, etc.).

---

## Threat Model

### What ShellParser Protects

- Correct function ownership and brace-level tracking in messy real-world shell scripts
- Original script integrity during `replace` operations
- User’s ability to recover from any editing mistake via automatic dated backups
- Stable parser state across thousands of lines of legacy shell code

### Potential Risks

- **Incorrect function replacement** leading to broken scripts
- Brace level drift or ownership corruption during parsing
- Loss of original script content if backup mechanism fails
- Accidental simplification or removal of defensive code by AI assistants
- Path traversal or unexpected file writes (though the tool is strictly local and runs under normal user privileges)

### Out of Scope

- Security of the shell scripts themselves (e.g., malicious code inside the scripts)
- Execution of the generated shell scripts
- Network-related or system-level attacks
- Secrets embedded inside the shell scripts

---

## Security Design Principles (CIAO)

ShellParser applies **CIAO** principles throughout:

1. **Caution** — Input validation, clear error messages, mandatory backups before any write.
2. **Intentional** — Every major function has explicit purpose documented in Protection Zones.
3. **Anti-fragile** — Automatic dated backups (`filename.YYYYMMDD-N`), replace mode with `output_enabled` switch.
4. **Over-protect** — Extensive CIAO-Lite Protection Zones that explicitly forbid common failure patterns (regex-only parsing, hard-coded numbers, `.append()` misuse, merging stages, etc.).

These protections were added after multiple real Grok sessions caused regressions in earlier versions.

---

## Core Safety Mechanisms

- **Backup-before-replace**: Every `replace` operation creates a numbered backup first (`myscript.sh.20260428-1`)
- **3-Stage Architecture**: Forward parse → backward ownership correction → extraction (prevents incorrect ownership)
- **Real Brace Calculation**: No hard-coded numbers — uses `tokens.count('{')` everywhere
- **Enhanced Tokenizer**: Properly handles quoted strings, `$(...)`, `` `...` `` to avoid brace drift in compound commands
- **Single Source of Output**: All console and log output goes through **ChronicleLogger**
- **Protected Zones**: AI assistants are explicitly forbidden from simplifying or removing defensive code

---

## Reporting a Vulnerability

If you discover a security issue in ShellParser, please report it responsibly.

**Preferred method**:

1. Open a **private** issue on GitHub (if possible) or
2. Contact the maintainer directly via GitHub (@cloudgen) with the subject "**ShellParser Security Report**".

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact (especially risk of script corruption or data loss)
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and aim to address critical issues quickly.

**Do not** publicly disclose the vulnerability until a fix has been released.

---

## Best Practices for Users

- Always run `shellparser replace` in a controlled environment
- Review the automatic backup files after each replace
- Keep regular backups of important shell scripts
- When editing the code with AI, **never remove or simplify** the CIAO-Lite Protection Zones
- Use `--json` mode for automation to avoid mixing log output with machine-readable data

---

## Dependency Security

- The only runtime dependency is **[ChronicleLogger](https://pypi.org/project/ChronicleLogger/)**
- We recommend installing from PyPI and keeping it updated
- For development, use a virtual environment (`pip install -e .`)

---

## AI-Assisted Development Note

This project is deliberately written with verbose headers and strict Protection Zones to survive repeated editing by large language models.

**If you are an AI assistant helping with this codebase:**

- **Do not** remove, shorten, or “clean up” the long defensive comment blocks
- **Never** simplify or refactor code inside CIAO-Lite Protection Zones
- Respect all documented rules (real brace calculation, StateLogic + Attr contract, single source of output, etc.)

These protections exist because previous AI “improvements” repeatedly broke core functionality.

---

## Contact

- Repository: [https://github.com/cloudgen/ShellParser](https://github.com/cloudgen/ShellParser)
- Maintainer: McLeon / cloudgen

---

**Last updated**: April 2026  
**Version**: 1.0.2
