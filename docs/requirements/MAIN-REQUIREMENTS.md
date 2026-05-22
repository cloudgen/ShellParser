# Main Requirements - ShellParser

**Status**: Active (Version 1.2.1+)  
**Milestone**: v2.1 — Placeholder Mass Replace

## 1. Purpose

This is the **central master requirements document** for ShellParser.

## 2. Current Milestone Status

**Version 1.2.1** — Milestone v2.1 (Active)

### Key Feature: `placeholder` Command

**Status**: Active & Protected

## Core Intention of `placeholder` Command

The `placeholder` command is **NOT** a split operation.  
It is a **mass in-place replace** operation.

**Exact Behavior Required**:
- Run: `shellparser placeholder <source_file>`
- Step 1: Always create dated backup first (`source.sh.YYYYMMDD-N`)
- Step 2: Replace **every function body** (except top-block / shebang area) with minimal clean placeholder skeleton **inside the original source file**
- Top-block (everything before first function) must remain **100% untouched**

This command exists to quickly "hollow out" a large monolithic script for AI refactoring while keeping editable skeletons in a dated folder.

## 3. Relevant Requirements Files

(All files live in `docs/requirements/` — must stay aligned)

- `backup-strategy.md`
- `cli-interface.md`
- `parser-architecture.md`
- `attr-contract.md`
- `interactive-mode.md`
- `parameters.md`
- `milestones.md`
- `protection-zones.md`
- `split-docs.md`

## 4. Project-Wide Rules (Enforced Everywhere)

- 3-stage parser remains sacred
- New features must use dedicated `xxx_mode` Attr flags
- All output must go through ChronicleLogger
- Backup before any modification
- Strong requirement alignment and comment blocks to prevent mis-interpretation

## 5. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Turn `placeholder` into a split-style operation
- Add extra noisy comments in generated placeholders
- Change dated folder naming (`target/placeholder.YYYYMMDD-N/`)
- Weaken any CIAO-Lite Protection Zone
- Mis-represent user intention in any requirements document

---

**Last Updated**: May 11, 2026  
**Owner**: Master Requirements  
**Target Version**: 2.1 (Placeholder Mass Replace)
