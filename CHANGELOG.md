# Changelog

All notable changes to **ShellParser** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
