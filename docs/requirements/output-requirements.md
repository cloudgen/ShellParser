# Output Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the centralized output and logging system used throughout ShellParser. It establishes **ChronicleLogger** as the **Single Source of Truth** for all console output, logs, errors, and structured data.

## 2. Core Principles

- Only `logger.log_message()`, `logger.prn()`, `logger.error()`, etc. are allowed.  
- Never use `print()`, `sys.stdout`, `sys.stderr`, or direct output anywhere in the project (except inside ChronicleLogger itself).
- Full support for human-readable, quiet, and JSON modes.
- When JSON mode is enabled, **quiet mode is automatically forced** (regardless of command line, environment variables, or future config). This ensures clean JSON output with no human-readable text pollution.

## 3. Available Output Methods (via ChronicleLogger)

- `logger.log_message(msg, component="parser", level="info")` — General messages
- `logger.prn(text)` — Human-readable output (respects quiet mode)
- `logger.error(...)`, `logger.warn(...)` — Errors and warnings (always shown)
- `logger.debug(...)` — Debug messages (only when `DEBUG=1`)

## 4. Output Modes

### 4.1 Normal Mode (default)
- Human readable format with proper prefixes and formatting via ChronicleLogger.

### 4.2 Quiet Mode (`--quiet` or `QUIET=1`)
- Suppresses INFO and DEBUG level messages.
- Still shows WARN, ERROR, and important success messages.

### 4.3 JSON Mode (`--json` or `JSON=1`)
- Structured JSON output (one object per line or single object for `about`/`help`).
- **Important Rule**: JSON mode **automatically forces quiet=true**.
- Example for status:
  ```json
  {"tool": "ShellParser", "command": "split", "status": "success", "functions_extracted": 12, "timestamp": "2026-05-10T17:02:00"}
  ```

## 5. Command Line & Environment Support

- `--quiet` / `QUIET=1`
- `--json` / `JSON=1`
- `DEBUG=1` → enables debug output
- All global options available on every subcommand including `help` and `about`

## 6. Design Rules

- Never use `print`, `fprintf`, or direct stdout anywhere outside ChronicleLogger.
- All output must go through the single `ChronicleLogger` instance created in `main()`.
- Proper handling of JSON mode in `show_about()` and `show_help()`.
- Thread-safe consideration for future parallel parsing (Milestone 3.0+).
- Logger must call `logger.logName()` and `logger.baseDir()` early for correct storage resolution.

## 7. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Add any `print()`, `sys.stdout`, or direct output statements anywhere in the project.
- Bypass ChronicleLogger for any user-facing or log output.
- Remove or weaken the rule that JSON mode forces quiet mode.
- Create multiple ChronicleLogger instances in one run.
- Remove calls to `logger.logName()` / `logger.baseDir()` in `main()`.
- Simplify or remove verbose Protection Zones related to output handling.

## 8. Future Enhancements (Milestone 2.0+)

- Log file output option (daily rotation via ChronicleLogger)
- Structured logging with context (function name, line range, etc.)
- Virtual output for testing
- Configurable log level and component filtering

---

**Last Updated**: May 2026  
**Owner**: Output & Logging System  
**Target Version**: 1.1 (Output System Stable)
