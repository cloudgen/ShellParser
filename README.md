# ShellParser - AI-Augmented Shell Script Component Manager

[![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)](https://github.com/cloudgen/ShellParser)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--protect)-purple.svg)](https://github.com/cloudgen/ciao)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)]()

**A battlefield-hardened, CIAO-defensive tool that turns massive legacy shell scripts into small, AI-editable components.**

This project follows strict [CIAO defensive programming principles](https://github.com/cloudgen/ciao).

---

## Overview

ShellParser solves one of the biggest pain points when working with large shell scripts (thousands of lines):

- It **splits** a monolithic `.sh` file into clean, single-responsibility components (`target/components/*.sh`)
- It enables **safe surgical editing** by AI (Grok, Claude, etc.) on small focused files
- It **reassembles** changes safely with automatic dated backups via the `replace` command

**Core Innovation:**
- True bidirectional human-AI workflow for shell code
- 3-stage parser (forward classification → backward ownership correction → extraction)
- Real brace calculation + enhanced tokenizer (handles quoted strings, `$(...)`, `` `...` ``)
- Production-grade safety (backups before every replace)

**Powered by ChronicleLogger + StateLogic**

---

## Dependencies

ShellParser is built on two core libraries:

- **[ChronicleLogger](https://github.com/cloudgen/ChronicleLogger)** — Single source of truth for all logging, quiet mode, JSON output, and file logging.
- **[StateLogic](https://github.com/cloudgen/StateLogic)** — Lightweight Finite State Machine (FSM) framework with `Attr` descriptor for safe, explicit state management.

### Installation

```bash
pip install ShellParser
```

Or from source:

```bash
git clone https://github.com/cloudgen/ShellParser.git
pip install ChronicleLogger==1.3.1 StateLogic 
pip install ShellParser
cd ShellParser
pip install -e .
```

---

## Technology Stack Explanation

### StateLogic + Attr

ShellParser uses the **StateLogic** framework as its core engine:

- **StateLogic**: A defensive Finite State Machine that forces all state changes through registered `transition()` calls and supports `before` / `on` / `after` hooks.
- **Attr**: A powerful descriptor pattern that turns normal attributes into safe, callable getters/setters:
  ```python
  Attr(self, attrName='brace_level', value=0)
  Attr(self, attrName='map_array', value=[], sorting=False)
  ```

  Usage:
  ```python
  self.brace_level(5)          # setter
  current = self.brace_level() # getter
  ```

**Why this matters:**
- Prevents accidental state corruption (common failure mode in previous Grok sessions)
- Enforces the contract: `self.map_array(entry)` instead of `.append()`
- Makes the 3-stage parser extremely stable and introspectable

### ChronicleLogger

All output (console, logs, JSON, quiet mode) goes through **ChronicleLogger** — the single source of truth. This ensures consistent behavior across normal, quiet, and JSON modes.

---

## Usage

### 1. Split Mode (Break script into components)

```bash
shellparser split myscript.sh
```

This creates:
- `target/components/*.sh` (one file per function + `top-block.sh`)
- `target/report/stage_1.txt` (detailed classification report)

### 2. Replace Mode (Merge AI-edited component back)

```bash
shellparser replace myscript.sh my_function
```

- Automatic backup: `myscript.sh.20260428-1`
- Only the target function is replaced

### 3. Helper Commands

```bash
shellparser about
shellparser help
shellparser help --json
```

---

### Full Command Reference

| Command                        | Description                                      | Options                  |
|--------------------------------|--------------------------------------------------|--------------------------|
| `shellparser split <file>`     | Split script into components                     | `--quiet`, `--json`      |
| `shellparser replace <file> <func>` | Replace function from components (with backup) | `--quiet`, `--json`      |
| `shellparser about`            | Show version & environment                       | `--quiet`, `--json`      |
| `shellparser help`             | Show this help                                   | `--quiet`, `--json`      |

---

## AI Collaboration Workflow

1. **Split** → break large script into small editable `.sh` files
2. **Edit** → let AI work on individual functions safely
3. **Replace** → merge changes back with automatic backup

---

## Key Features

- **3-Stage Architecture** with backward ownership correction
- Real brace level calculation (no hard-coded numbers)
- Enhanced tokenizer for quoted strings and compound commands
- Full CIAO-Lite Protection Zones
- Single source of output via ChronicleLogger
- Quiet + JSON support
- Automatic dated backups

---

## Development Philosophy

Built with **CIAO Defensive Programming Principles** (Caution • Intentional • Anti-fragile • Over-protect) to survive repeated AI-assisted modifications.

---

## Links

- [ChronicleLogger](https://github.com/cloudgen/ChronicleLogger)
- [StateLogic](https://github.com/cloudgen/StateLogic)
- [CIAO Philosophy](https://github.com/cloudgen/ciao)
- [ShellParser Repository](https://github.com/cloudgen/ShellParser)

---

**Made with ❤️ for power users and AI collaborators maintaining large shell ecosystems.**

