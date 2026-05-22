# Milestones & Roadmap - ShellParser

**Status**: Active (Target: Version 2.1)

## 1. Purpose

This document tracks all major milestones, completed features, and future roadmap for ShellParser while maintaining full alignment with CIAO-Lite principles.

## 2. Current Version

**Version 1.2.1** (in progress)  
**Milestone v2.1** — Placeholder Skeleton Feature

### Completed in v2.0 (May 2026)
- Classic `split` command (`target/components/*.sh`)
- Safe `replace` command with automatic dated backup
- `split-docs` command (`target/docs/*.md` — LLM-friendly)
- `docs_mode` Attr flag + clean Stage 3 branching
- Enhanced interactive mode with 4 options
- Full `--quiet` / `--json` support across all commands
- Complete requirements documentation suite

### New in v2.1 (Current Milestone)
- **`placeholder` subcommand** — Replace all functions (except `top-block`) with minimal placeholder skeletons
  - Uses new `placeholder_mode` Attr flag
  - Backup-first safety (same as `replace`)
  - Preserves `top-block` and shebang completely
  - Generates clean skeleton for rapid modernization / refactoring
  - Full integration with 3-stage parser and interactive mode

### Interactive Mode Update
Menu now includes:
5. **placeholder** shell file → replace all functions with TODO placeholders (except top-block)

## 3. Future Milestones

### v2.2 (Planned)
- `--both` flag (run `split` + `split-docs` + `placeholder` in one pass)
- Configuration file support (`~/.app/ShellParser/config.conf`)
- Enhanced placeholder templates (customizable via config)

### v3.0 — Semantic Extraction
- Variable / string / heredoc extraction
- Database integration (v4.0 foundation)

### v4.0 — Persistence Layer
- SQLite database for parsed knowledge
- Version history per function
- Semantic search for AI context

## 4. Design Principles (CIAO-Lite)

- **Caution**: Every new feature uses dedicated Attr flag + protected Stage 3 method.
- **Intentional**: `placeholder` follows exact pattern from `parser-architecture.md`.
- **Anti-fragile**: Backup before any modification; `top-block` always preserved.
- **Over-protect**: New Protection Zones will be added in `cli.py`.

## 5. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Add new features without a corresponding `xxx_mode` Attr flag
- Bypass `afterStartParse()` branching for Stage 3 modes
- Modify existing commands (`split`, `replace`, `split-docs`) behavior
- Remove or weaken any CIAO-Lite Protection Zone

---

**Last Updated**: May 11, 2026  
**Owner**: Roadmap & Milestones  
**Target Version**: 2.1 (`placeholder` subcommand + skeleton workflow)

**Alignment**: Fully synchronized with `parser-architecture.md`, `attr-contract.md`, `cli-interface.md`, `interactive-mode.md`, and `parameters.md`.
