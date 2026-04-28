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

## Installation

```bash
pip install ShellParser
```

Or from source (editable):

```bash
git clone https://github.com/cloudgen/ShellParser.git
cd ShellParser
pip install -e .
```

The command `shellparser` will be available in your PATH.

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
- Everything else remains untouched

### 3. Helper Commands

```bash
shellparser about          # Version & environment info
shellparser help           # This help
shellparser help --json    # JSON output
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

### JSON Mode Examples

```bash
shellparser about --json
shellparser help --json
```

---

## AI Collaboration Workflow

1. **Split** → break large script into small editable `.sh` files
2. **Edit** → let AI (Grok/Claude) work on individual functions safely
3. **Replace** → merge changes back with automatic backup

---

## Key Features

- **3-Stage Architecture** with backward ownership correction (battlefield-tested)
- Real brace level calculation (no hard-coded numbers)
- Enhanced tokenizer (quoted strings, command substitutions, compound commands)
- Full CIAO-Lite Protection Zones
- Single source of output via ChronicleLogger
- Quiet + JSON support for scripting/AI pipelines
- Automatic dated backups before every replace

---

## Development Philosophy

This tool is built with **CIAO Defensive Programming Principles** (Caution • Intentional • Anti-fragile • Over-Engineering) to survive repeated AI-assisted modifications.

**Requires ChronicleLogger**

---

## Links

- [CIAO Philosophy](https://github.com/cloudgen/ciao)
- [CIAO-lite](https://github.com/cloudgen/ciao-lite)
- [ChronicleLogger on PyPI](https://pypi.org/project/ChronicleLogger/)
- [ShellParser Repository](https://github.com/cloudgen/ShellParser)

---

**Made with ❤️ for power users and AI collaborators maintaining large shell ecosystems.**
