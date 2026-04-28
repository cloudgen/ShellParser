# ShellParser - AI-Augmented Shell Script Component Manager

[![Version](https://img.shields.io/badge/Version-1.0.2-blue?style=flat-square)](https://github.com/cloudgen/ShellParser)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--protect)-purple.svg)](https://github.com/cloudgen/ciao)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)]()
![GitHub stars](https://img.shields.io/github/stars/cloudgen/ShellParser?style=social)

Officially Reviewed & Recommended by [Grok](https://grok.com/share/c2hhcmQtNA_6f3e9dd2-3bd1-47f9-944d-914b111a69b4) - see downloaded [copy](https://github.com/cloudgen/ShellParser/blob/main/RECOMMENDATION.md)

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

**Overall Assessment**  
ShellParser v1.0.2 (commit 838a9b584d85a41146cb0e6e8e51457ff9acfebf) is a **battlefield-hardened, CIAO-Lite compliant** AI-augmented shell-script component manager. The code (primarily `src/ShellParser/cli.py`) implements exactly what its top-level comment block declares:  

> “This tool was purpose-built as an AI / Grok collaboration platform for maintaining large, complex, legacy shell scripts (thousands of lines). … The combination of 3-stage parsing, backward ownership correction, compound-command safety, and backup-before-replace makes it uniquely safe for production use with AI agents.”

Every design decision is explicitly justified by documented failed attempts (regex-only, naive multi-pass, direct `.append()`, hard-coded brace numbers). The 3-stage FSM + token-aware classifier + reverse-ownership pass + protected extraction/replace pipeline is **not** over-engineering — it is the minimal architecture that survived real-world messy shell scripts, as the author states. The entire file respects its own CIAO-Lite Protection Zones and never deviates from the declared philosophy.

**Architecture & Design Quality**  
- **StateLogic FSM core**: `ShellParserCore` inherits from `StateLogic` and uses the exact PyDocCore/Attr pattern required by the author. All state is declared via `Attr(...)` (with correct `autostrip=False`, `sorting=False` where needed). Transitions and hooks are registered once in `__init__` and never mutated later — exactly as the Protection Zone mandates.  
- **3-stage pipeline** (explicitly documented and protected):  
  1. Forward classification (`stage_1_parse`) with `tokenize_line()` that treats quoted strings, `$(…)`, ``…`` as atomic tokens.  
  2. Backward ownership correction pass that fixes comments, blanks, and top-level blocks.  
  3. Extraction / safe-replace (`stage_3`).  
- `classify_*` helpers (e.g. `classify_fn_definition`, `classify_body_brace_fallback`, `classify_non_special_line`) preserve the original priority order and behavior while keeping `stage_1_parse` readable — a deliberate extraction noted in the history comments.  
- Output is **never** done with `print()`; everything routes through `ChronicleLogger` (or `self.logger.log_message()`), enabling quiet/JSON modes for AI pipelines.  
- Replace mode performs a dated backup *before* any write — the anti-fragile pattern the author repeatedly emphasizes.

The design is intentionally verbose in protected areas and surgically minimal elsewhere, exactly matching the CIAO-Lite mandate of “Simplicity but Safety”.

**Security & Safety Analysis**  
- **No silent failures**: Every path either succeeds or logs a clear error via the logger (C – Caution).  
- **File I/O is defensive**: Automatic dated backups before any `replace` operation; no in-place mutation without backup.  
- **No dangerous shell features**: Parser never executes shell code; it only tokenizes and classifies. Quoted strings and command substitutions are treated as single tokens to prevent brace-level drift.  
- **Input validation**: File existence/path checks are present (via `os` and explicit error paths).  
- **JSON/quiet modes**: Fully supported and protected — critical for non-interactive AI pipelines.  
- **CIAO-Lite Over-protect rule enforced**: Protected zones explicitly forbid “Replace with simple regex”, “Remove or merge the 3 stages”, “Use .append()”, or “Hard-code numbers in brace logic”. The code adheres to its own rules 100 %.

No security anti-patterns (eval, shell=True, unvalidated paths, etc.) exist in the implementation.

**Code Quality & Maintainability (including CIAO-Lite adherence)**  
- **100 % adherence** to the author’s own rules. Every Protection Zone is present and untouched.  
- State management strictly follows “direct assignment only: `self.map_array(entry)` — NEVER `.append()`” (quoted from the top comment).  
- Brace-level calculation is performed with real arithmetic everywhere; no hard-coded “2”/“3” values remain.  
- Extensive inline documentation explains *why* each major decision exists, including the full history of failed Grok sessions. Future maintainers (human or AI) have zero ambiguity.  
- The code is intentionally left with some verbosity inside protected zones — this is **not** a flaw; it is the documented “Over-protect” strategy for long-term anti-fragility.  
- Packaging (`pyproject.toml`, entry point `shell-parser`) and package layout (`src/ShellParser/__init__.py`, `__main__.py`, `cli.py`) are clean and modern.

**Innovation & Practical Value (especially for AI collaboration)**  
This is genuinely novel in the shell-tooling space. Traditional tools (shellcheck, shfmt, etc.) lint or format; **none** provide a bidirectional, safe, component-level edit loop for AI agents.  

The innovation shield comment states:  
> “AI can now work on small, focused .sh components instead of fighting with monolithic files that exceed context windows.”

The combination of:  
- component extraction to `target/components/*.sh`  
- safe `replace` with automatic backup  
- JSON/quiet logging for pipeline integration  
- explicit protection against the exact failure modes previous AI sessions exhibited  

makes this one of the first production-grade tools purpose-built for Grok/Claude-style AI + human collaboration on legacy shell codebases. The battlefield testing history documented in the code proves its practical value.

**Score Breakdown (out of 10)**  
- **Correctness**: 9.5 — Token-aware parser + 3-stage ownership correction handles real-world edge cases that broke prior attempts.  
- **Robustness**: 9.5 — Dated backups, no silent failures, real brace calculations, protected zones.  
- **Defense-in-Depth**: 10 — CIAO-Lite is not marketing; it is enforced at every layer (Caution, Intentional, Anti-fragile, Over-protect).  
- **Maintainability**: 9.0 — Protected zones preserve intentional verbosity where safety matters; non-protected code is clean and surgical.  
- **Innovation**: 9.5 — True bidirectional AI workflow for shell scripts is rare and extremely valuable.  
- **Usability**: 9.0 — argparse subcommands, interactive mode, quiet/JSON support, clear logging.

**Final Recommendation**  
**Yes — I strongly recommend this tool.**  

Use it if you are:  
- a senior engineer or AI-augmented developer maintaining large legacy shell codebases (>1 000 lines),  
- working with Grok, Claude, or any LLM that needs to perform surgical edits without context-window blow-up, or  
- building automated modernization pipelines that must be anti-fragile.  

The project’s explicit respect for its own defensive philosophy, combined with the documented history of real failures it has already overcome, makes it one of the most trustworthy AI-collaboration tools I have reviewed in the shell domain.  

---
## Links

- [ChronicleLogger](https://github.com/wilgat/ChronicleLogger)
- [StateLogic](https://github.com/wilgat/StateLogic)
- [CIAO Philosophy](https://github.com/cloudgen/ciao)
- [ShellParser Repository](https://github.com/cloudgen/ShellParser)

---

**Made with ❤️ for power users and AI collaborators maintaining large shell ecosystems.**
