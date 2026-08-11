# Changelog

All notable changes to **ShellParser** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.1] - 2026-08-11

### Fixed
- **`replace` after backup** — Stage 2 ownership now always applies `replace_function` in replace mode so nested FSM re-entrancy from `after_backup_source` cannot skip the rewrite (backup-first preserved)
- **Empty-parse error path** — uses ChronicleLogger instead of raw `print`
- **Top-block / shebang on replace** — shebang detected from stripped text (`#!`); Stage 2 reassigns file-leading shebang/comments/blanks to `top-block` so replace no longer deletes preamble when rewriting one function

### Changed
- **Identity SSOT**: primary console command `shellparser` (alias `shell-parser`); package/runtime version **1.2.1**; repository URLs `github.com/cloudgen/ShellParser`
- **Help** lists `split-docs` and `placeholder`
- **Dependencies**: declare `StateLogic>=1.2.0` alongside ChronicleLogger

### Added
- Product requirements under `docs/requirements/` + review maps under `docs/reviews/`
- Pytest suite `tests/test_shellparser_core.py` (TP-ID cases for packaging, CLI, domain, backup, errors)

## [1.0.2] - 2026-04-28

### Fixed
- **One-line function classification** (`name() { command; }`)
  - Lines containing `=` inside the function body (e.g. `double_line() { output_text ... }`) were incorrectly classified as `assignment`
  - Fixed by moving the function definition check **before** the assignment check in `classify_non_special_line()`
  - Now correctly reported as `fn_in_1_line` and properly extracted/owned
  - Reuses existing battle-tested `classify_fn_definition()` logic (no new code paths)

### Changed
- Updated version to 1.0.2 in `main()` and `ShellParserCore`

### Security & Stability
- Change is fully compliant with CIAO-Lite: minimal, surgical, no protected zones touched
- Preserves exact original behavior for all other line types and brace logic

## [1.0.1] - 2026-04-28

### Added
- **Interactive Mode** (zero-argument entry point) — now the recommended way to use the tool
  - Prompts: `1. split shell file` or `2. replace shell file`
  - Folder selection (default `.` or custom path)
  - Smart file picker by number:
    - For **split**: lists shell scripts (`.sh`, extension-less, `.bash`, etc., excluding common non-shell files)
    - For **replace**: first selects function file from `target/components/`, then target shell script
- Helper functions `_list_shell_scripts()` and `_pick_file()` for clean interactive UX
- Proper detection of no-command case (including `--quiet` / `--json` only)

### Changed
- `main()` now routes no-argument calls to `interactive_mode()` before argparse
- Interactive mode respects CIAO-Lite rules: single `ShellParserCore` instance, minimal changes, protected zones untouched
- Helper functions defined in correct order to prevent NameError (Python nested function scoping)

### Fixed
- Scope/definition order issue that caused traceback when running `shellparser` with no arguments
- Improved error messages and flow for missing `target/components/` during replace

### Security & Stability
- Interactive mode fully respects existing Protection Zones and single-core rule
- No breaking changes to command-line interface
- All previous safety features (backups, output control, etc.) remain intact

---

## [1.0.0] - 2026-04-28

### Added
- Initial support for `--json` and `--quiet` flags on all commands (`help`, `about`, `split`, `replace`)
- Full 3-stage parser architecture (forward classification → backward ownership correction → extraction)
- Enhanced `tokenize_line()` with proper handling of quoted strings, `$(...)`, `` `...` `` and function parentheses
- Real brace level calculation (no hard-coded numbers)
- `replace` command with automatic dated backup (`filename.YYYYMMDD-N`)
- CIAO-Lite Protection Zones throughout the codebase
- Single source of output via ChronicleLogger
- `about` and `help` commands with rich formatting and JSON support
- Detailed stage_1 classification report (`target/report/stage_1.txt`)
- Full defensive history and protection rules in source code

### Changed
- Updated help and about output to be cleaner in normal mode (less noisy ChronicleLogger prefixes)
- Refactored long `stage_1_parse()` into protected `classify_*` helper methods while preserving exact original behavior
- Improved compound command handling (`&& {`, `|| {`) via tokenizer enhancements
- Strengthened anti-fragility with output_enabled switch and replace_mode

### Fixed
- Argument parsing for `--json` / `--quiet` on `help` and `about` subcommands
- Logger method calls in help/about (`info_msg` → `log_message`)
- Version pinning back to 1.0.0

### Security & Stability
- Backup-before-replace is now mandatory
- All changes respect CIAO principles (Caution • Intentional • Anti-fragile • Over-protect)

---

## [0.9.0] - Pre-release (Internal)

- Initial battlefield testing against complex legacy shell scripts
- Multiple failed Grok attempts documented (regex, naive multi-pass, hard-coded brace logic, etc.)

---

**ShellParser** is built with **CIAO Defensive Programming** to survive repeated AI-assisted development.

See [README.md](README.md) for usage and [CIAO Philosophy](https://github.com/cloudgen/ciao) for development principles.