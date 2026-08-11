# ShellParser - AI-Augmented Shell Script Component Manager

[![Version](https://img.shields.io/badge/Version-1.2.1-blue?style=flat-square)](https://github.com/cloudgen/ShellParser)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE.md)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--protect)-purple.svg)](https://github.com/cloudgen/ciao)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)]()

**Repository:** [github.com/cloudgen/ShellParser](https://github.com/cloudgen/ShellParser)

**Now with v2.0 `split-docs` — LLM-friendly markdown output!**

---

## Overview

ShellParser is a **battlefield-hardened** tool that turns massive monolithic shell scripts into small, AI-editable components — with full bidirectional safety.

### Identity (SSOT)

| Field | Value |
|-------|--------|
| Product name | ShellParser |
| Version | **1.2.1** (`pyproject.toml`, package `__version__`, runtime core) |
| Primary CLI command | **`shellparser`** |
| Compatibility alias | `shell-parser` (same entry point) |
| Package import | `ShellParser` |
| Install | local Python package (`pip install` / editable) |

### v2.0 Feature — `split-docs`

- Generates clean, LLM-optimized markdown files in `target/docs/`
- Perfect for AI training, documentation, and context injection
- Reuses the same proven 3-stage parser (zero breaking changes)

---

## Key Features

- **Interactive Mode** (recommended daily workflow; empty argv)
- Classic `split` → `target/components/*.sh`
- **`split-docs`** → `target/docs/*.md` (LLM-ready)
- Safe `replace` with automatic dated backups
- `placeholder` mass rewrite (backup first; keeps top-block)
- 3-stage parser with real brace calculation + enhanced tokenizer
- Full CIAO-Lite Protection Zones
- ChronicleLogger as Single Source of Truth for output
- `--quiet` / `--json` support

---

## Usage

### Interactive Mode (Recommended)

```bash
shellparser
```

Menu:

```text
1. split shell file          → target/components/*.sh
2. replace shell file        → safe function replacement + backup
3. split-docs                → target/docs/*.md (LLM training ready)
4. placeholder               → placeholder rewrite (keep top-block)
5. about / help              → version & usage info
0. exit
```

### Command Line

```bash
# Classic split
shellparser split myscript.sh

# LLM-friendly markdown
shellparser split-docs myscript.sh

# Safe replace
shellparser replace myscript.sh my_function

# Mass placeholder (with backup)
shellparser placeholder myscript.sh

# Info
shellparser about
shellparser help
```

All commands support `--quiet` and `--json`.

---

## Output Structure (Target Project)

```text
{project-root}/
├── myscript.sh
├── target/
│   ├── components/          # .sh files (classic split)
│   └── docs/                # .md files (split-docs)
├── myscript.sh.20260510-1   # Automatic backup (replace / placeholder)
└── ...
```

**Example `target/docs/my_function.md`:**

```markdown
# Function: my_function

## Metadata
- Extracted: 2026-05-10 17:41:00
- Source File: /path/to/myscript.sh
- Line Range: 45-78
- Line Count: 34

## Description
<!-- Optional summary -->

```sh
my_function() {
    # Full original content with comments and whitespace preserved
    ...
}
```
```

---

## AI Collaboration Workflow

1. `split` or `split-docs` → break script into small files  
2. Edit individual `.sh` or `.md` files with an AI assistant  
3. `replace` → safely merge changes back with backup  

---

## Installation

```bash
pip install ShellParser
```

Or from source:

```bash
pip install -e ".[test]"
```

---

## Tests

```bash
pytest
# or
./build.sh test
```

Product law: `docs/requirements/`. Verification map: `docs/reviews/test-plan.md`.

---

## Requirements & Philosophy

- Built with strict **CIAO-Lite** principles  
- All product output through **ChronicleLogger** (JSON mode may emit one JSON object on stdout intentionally)  
- 3-stage parser is sacred (forward → backward ownership → extract)  
- Protection Zones prevent regression from AI-assisted edits  

See `docs/requirements/` for enforceable product law.

---

**Version 1.2.1** — identity SSOT alignment (console name, version, repository).

**Made for AI-augmented shell script maintenance.**
