# Configuration Requirements - ShellParser

**Status**: Draft → Active (Target: Milestone 2.0)

## 1. Purpose

This document defines how ShellParser handles all configuration — from command-line arguments and environment variables to persistent config files and future parser/skill-specific settings.

## 2. Configuration Sources (Priority Order)

1. Command-line arguments (`--config`, `--quiet`, `--json`, etc.)
2. Environment variables (`DEBUG=1`, `QUIET=1`, `JSON=1`)
3. User config file (`~/.app/ShellParser/config.conf`)
4. Built-in defaults (only as final fallback)

## 3. Config File Location

- **Default**: `~/.app/ShellParser/config.conf`  
  (Resolved via ChronicleLogger storage rules — supports pyenv, conda, venv, etc.)
- Override with: `--config /path/to/custom.conf`
- Must respect CIAO defensive storage location handling

## 4. Supported Formats

- **Primary**: INI-style (simple, human editable)
- **Secondary**: JSON (for complex settings, Milestone 3.0+)

## 5. Configuration Example (`config.conf`)

```ini
# =============================================================================
# config.conf - ShellParser
# =============================================================================

[core]
project_name = "ShellParser"
default_target_dir = "target"

[output]
quiet = false
json = false
debug = false

[parser]
enable_semantic_extraction = false
backup_enabled = true

[database]
enabled = false
path = "~/.app/ShellParser/shellparser.db"
journal_mode = "WAL"

[docs]
enabled = true
output_dir = "target/docs"
template_version = "1.0"
```

## 6. Command Line Parameters (Summary)

- `--config <path>`          → Load specific config file
- `--quiet` / `--json`       → Output control
- `--help`, `help`           → Show usage
- Future: `--split-docs`, etc.

## 7. Design Principles (CIAO-Lite)

- All hard-coded values must be removed by Milestone 2.0
- Configuration must be **overridable** and **extensible**
- Graceful degradation when config file is missing or invalid
- Single Source of Truth for storage location via ChronicleLogger
- Defensive parsing with clear error messages via centralized logging

## 8. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Hard-code any paths, output directories, or behaviors after Milestone 2.0
- Bypass ChronicleLogger for storage path resolution
- Remove support for `--config` flag
- Change the priority order (CLI > ENV > config.conf)
- Use silent failures when config is invalid or missing
- Hard-code `~/.app/ShellParser/` without using defensive storage handling

## 9. Future Enhancements (Milestone 2.0+)

- Config UI / editor (future)
- Per-project config files
- Hot-reloading support
- Validation with helpful suggestions
- Encryption for sensitive settings

---

**Last Updated**: May 2026  
**Owner**: Configuration System  
**Target Version**: 2.0 (Configuration Fully Configurable)
