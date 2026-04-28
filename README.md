# ShellParser - AI-Augmented Shell Script Component Manager

[![Version](https://img.shields.io/badge/Version-1.0.1-blue?style=flat-square)](https://github.com/cloudgen/ShellParser)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--protect)-purple.svg)](https://github.com/cloudgen/ciao)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)]()
![GitHub stars](https://img.shields.io/github/stars/cloudgen/ShellParser?style=social)

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

## Why ShellParser is the Best Among Similar Products

Most tools for handling large shell scripts fall into one of these categories — and **none match ShellParser** for AI-assisted modernization:

| Tool / Approach                  | What it does                              | Limitations vs ShellParser |
|----------------------------------|-------------------------------------------|----------------------------|
| Manual `grep`/`sed`/awk          | Basic function extraction                 | Fragile, no ownership correction, no safe reassembly |
| Simple split scripts (custom)    | Manual modularization                     | No parser, no backups, error-prone |
| Mush / shell libraries           | Dependency management                     | Requires rewriting code upfront |
| AI-only prompts (Claude/Grok)    | Direct editing of monoliths               | Hits context limits, risky full-file replaces |
| General code splitters           | Language-agnostic                         | Don't understand shell syntax, braces, or compound commands |

**ShellParser wins because:**

- **True AI-friendly workflow** — Split → Edit small files with any AI → Safe replace with backup.
- **3-Stage Battlefield Parser** — Forward token classification + **backward ownership correction** + extraction.
- **CIAO-Lite Safety** — Automatic dated backups, no silent failures, protected zones.
- **Interactive Mode** — Zero-argument guided prompts (recommended daily use).
- **Robust Tokenizer** — Handles real-world shell edge cases correctly.

If you maintain legacy monolithic shell scripts and want to modernize them safely with AI — **ShellParser is currently the best tool available**.

---

## Dependencies

ShellParser is built on two mature, well-established core libraries:

- **[ChronicleLogger](https://github.com/wilgat/ChronicleLogger)** — Official Recommended by grok. A robust, POSIX-compliant logging utility for Python applications, supporting Python 2.7 and 3.x with optional Cython compilation for enhanced performance. It handles daily log rotation, automatic archiving (tar.gz for logs >7 days), removal (>30 days), privilege-aware paths (/var/log for root, ~/.app for users), and structured output with timestamps, PIDs, levels, and components. No external dependencies beyond the standard library; semantic version 1.3.1. See [pypi package](https://pypi.org/project/ChronicleLogger/)
- **[StateLogic](https://github.com/wilgat/StateLogic)** — A pure, safe, and elegant finite state machine for Python — with colored terminal logging. See [pypi package](https://pypi.org/project/statelogic/)

ChronicleLogger and StateLogic are two mainstream packages with regards to rotational log system and Finite State Machine. Security review by 3-rd party such as [getsafety.com](https://getsafety.com/packages/pypi/chroniclelogger) and [getsafety.com](https://getsafety.com/packages/pypi/statelogic)

---

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

## Usage

### Interactive Mode (Recommended)

Simply run the tool with **no arguments**:

```bash
shellparser
```

It will guide you step by step:
1. Choose `1. split shell file` or `2. replace shell file`
2. Choose folder (default `.`)
3. Select file/function by number

### Command-line Modes

```bash
shellparser split myscript.sh
shellparser replace myscript.sh my_function
```

---

### Full Command Reference

| Command                        | Description                                              | Options                  |
|--------------------------------|----------------------------------------------------------|--------------------------|
| `shellparser`                  | **Interactive mode** (guided prompts) – **Recommended** | —                        |
| `shellparser split <file>`     | Split script into components                             | `--quiet`, `--json`      |
| `shellparser replace <file> <func>` | Replace function from components (with backup)      | `--quiet`, `--json`      |
| `shellparser about`            | Show version & environment                               | `--quiet`, `--json`      |
| `shellparser help`             | Show this help                                           | `--quiet`, `--json`      |

---

## AI Collaboration Workflow

1. **Split** (interactive or command) → break large script into small editable `.sh` files
2. **Edit** → let AI work on individual functions safely
3. **Replace** (interactive or command) → merge changes back with automatic backup

---

## Key Features

- **Interactive Mode** — zero-argument guided workflow
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

- [ChronicleLogger](https://github.com/wilgat/ChronicleLogger)
- [StateLogic](https://github.com/wilgat/StateLogic)
- [CIAO Philosophy](https://github.com/cloudgen/ciao)
- [ShellParser Repository](https://github.com/cloudgen/ShellParser)

---

**Made with ❤️ for power users and AI collaborators maintaining large shell ecosystems.**
