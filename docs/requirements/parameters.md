# Parameters Requirements - ShellParser

**Status**: Active (Version 1.0+ → 2.1)

## 1. Purpose

This document defines all supported command-line arguments, subcommands, and environment variables in ShellParser.

## 2. Command Line Parameters

### Global Options (available on all commands)

| Parameter     | Description                                      | Default | Example                  |
|---------------|--------------------------------------------------|---------|--------------------------|
| `--quiet`     | Suppress non-essential output                    | false   | `--quiet`                |
| `--json`      | Output in structured JSON format (forces quiet) | false   | `--json`                 |

### Subcommands

| Command                        | Description                                              | Required Arguments                          | Optional |
|--------------------------------|----------------------------------------------------------|---------------------------------------------|----------|
| (no arguments)                 | Interactive mode (recommended)                           | —                                           | —        |
| `split <source_file>`          | Split shell script into `target/components/*.sh`         | `source_file`                               | —        |
| `split-docs <source_file>`     | Split into LLM-friendly markdown (`target/docs/*.md`)    | `source_file`                               | —        |
| `replace <source_file> <func>` | Replace function from components/ (with backup)          | `source_file`, `func_name`                  | —        |
| **`placeholder <source_file>`**| **Replace all functions (except top-block) with placeholders** | `source_file`                        | —        |
| `about`                        | Show version and environment information                 | —                                           | —        |
| `help`                         | Show detailed help                                       | —                                           | —        |

## 3. Environment Variables

| Variable       | Description                                      | Example                     |
|----------------|--------------------------------------------------|-----------------------------|
| `DEBUG=1`      | Enable debug-level logging                       | `DEBUG=1 shellparser ...`   |
| `QUIET=1`      | Force quiet mode                                 | `QUIET=1 shellparser ...`   |
| `JSON=1`       | Force JSON output mode                           | `JSON=1 shellparser ...`    |

## 4. Design Principles (CIAO-Lite)

- **Caution**: All parameters validated early.
- **Intentional**: `placeholder` follows exact Attr pattern.
- **Anti-fragile**: New command does not break existing behavior.
- **Over-protect**: Global options available on every subcommand.

## 5. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Remove or rename the `placeholder` subcommand
- Change placeholder behavior without updating this file
- Remove `--quiet` / `--json` support

---

**Last Updated**: May 11, 2026  
**Owner**: CLI & Parameters System  
**Target Version**: 2.1
