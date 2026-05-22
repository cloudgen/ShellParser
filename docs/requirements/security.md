# Security Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the security model, threat considerations, and defensive practices for ShellParser — a tool that parses, extracts, and modifies shell scripts.

## 2. Threat Model

### Assets to Protect
- Original shell scripts (never modified without explicit backup)
- Extracted component files (`target/components/*.sh` and `target/docs/*.md`)
- User data and environment (no network access, no execution of parsed scripts)
- Parser state integrity (brace levels, function ownership)

### Potential Risks
- Data loss during `replace` operations
- Parser confusion leading to incorrect function boundaries
- Malicious input scripts attempting to exploit tokenizer/parser
- Privilege escalation or unsafe file writes

### Out of Scope
- Security of the shell scripts themselves (e.g. dangerous commands inside scripts)
- Execution of generated shell code
- Network / remote attacks (ShellParser is strictly local)

## 3. Core Security Principles (CIAO-Lite)

- **Caution**: Always backup before any write operation. Validate all file paths.
- **Intentional**: Explicit Protection Zones prevent dangerous simplifications by AI or humans.
- **Anti-fragile**: Dated incremental backups (`*.YYYYMMDD-N`) allow safe recovery.
- **Over-protect**: Parser never executes shell code — only reads and classifies.

## 4. Key Security Mechanisms

### 4.1 Backup Strategy (Mandatory)
- Every `replace` operation **must** create a backup first: `original.sh.YYYYMMDD-N`
- Original file is never touched until backup succeeds
- Backups preserve exact content and permissions

### 4.2 Input Validation
- File existence and readability checks before parsing
- No execution of user scripts (`subprocess` or `os.system` forbidden)
- Safe path handling (no shell injection)

### 4.3 Output Control
- Single Source of Truth: **ChronicleLogger** only
- JSON mode forces quiet to prevent leakage
- No direct `print()` anywhere in the codebase

### 4.4 Parser Safety
- Real brace calculation (no hard-coded numbers)
- Enhanced tokenizer handles quoted strings, `$(...)`, `` `...` `` safely
- No evaluation of parsed content

## 5. Design Rules

- Never use `eval`, `os.system`, `subprocess` with shell=True
- All file writes go through backup-first pattern
- Parser must survive maliciously crafted shell scripts without crashing or corrupting data
- Dependencies (ChronicleLogger, StateLogic) must be pinned to known-safe versions

## 6. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Remove or weaken the backup-before-replace mechanism
- Add any code that executes parsed shell content
- Bypass ChronicleLogger for output
- Remove or simplify any CIAO-Lite Protection Zones
- Introduce unsafe file operations or path traversal risks
- Hard-code temporary or output paths without using ChronicleLogger storage resolution
- Change backup naming convention without updating this document and replace workflow

## 7. Reporting & Response

- Security issues should be reported privately to the maintainer
- Critical parser bugs affecting data integrity will trigger immediate PATCH release
- All security-related changes must be clearly marked in `CHANGELOG.md`

## 8. Future Enhancements (v2.0+)

- `--dry-run` mode for safe preview of replace operations
- Hash verification of backups
- Optional read-only mode for scanning large script collections
- Audit logging of all replace operations

---

**Last Updated**: May 2026  
**Owner**: Security & Defensive Layer  
**Target Version**: 1.1 (Security Requirements Complete)
