# Split-Docs Requirements - ShellParser

**Status**: Draft → Active (Target: Version 2.0)

## 1. Purpose

This document defines the `split-docs` command — a specialized output mode that generates LLM-friendly markdown files optimized for AI training, documentation, and context injection.

## 2. Command

```bash
shellparser split-docs <source_file>
```

- New dedicated subcommand (does **not** replace the existing `split` command)
- Output directory: `target/docs/`
- One markdown file per function: `<function_name>.md`

## 3. Output Format (Per File)

Each generated file must follow this exact structure:

```markdown
# Function: <function_name>

## Metadata
- Extracted: YYYY-MM-DD HH:MM:SS
- Source File: /path/to/original/script.sh
- Line Range: START-END
- Line Count: N

## Description
<!-- Optional: First comment block summary if available -->

\`\`\`sh
# Full original function with ALL comments, whitespace, and body
function_name() {
    ...
}
\`\`\`
```

**Requirements for Code Block**:
- Must use triple backticks with `sh` language identifier
- Must contain the **complete** original function (including all leading comments, blank lines, and body)
- Must preserve exact original indentation and formatting
- No modifications to the function content

## 4. Behavior Rules

- Existing `split` command (→ `target/components/*.sh`) remains **unchanged**
- `split-docs` is **additive** — runs independently
- Must reuse the same 3-stage parser (Stage 1→2→3)
- Must respect `output_enabled` and other existing flags
- Support `--quiet` and `--json` modes
- Create `target/docs/` directory if it does not exist

## 5. Design Principles (CIAO-Lite)

- **Caution**: Never modify original script or components during docs generation
- **Intentional**: Markdown format optimized specifically for LLM training and human documentation
- **Anti-fragile**: Falls back gracefully if `target/docs/` cannot be written; preserves all original content
- **Over-protect**: `split-docs` must not interfere with classic `split`/`replace` workflow

## 6. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Change the output directory from `target/docs/`
- Alter the markdown template structure (header, metadata, triple-backtick block)
- Mix `split-docs` output into the regular `split` command
- Remove or weaken the requirement to preserve **exact** original function content inside the code block
- Bypass the 3-stage parser when implementing `split-docs`
- Hard-code markdown formatting logic outside a dedicated method (e.g. `stage_3_write_docs()`)
- Remove support for `--quiet` / `--json` in this mode

## 7. Future Enhancements (v2.1+)

- Configurable output template
- Option to include variable/string/heredoc extraction
- `--docs-only` flag for combined workflows
- Integration with v3.0 semantic extraction
- Front-matter YAML for better LLM ingestion

---

**Last Updated**: May 2026  
**Owner**: Documentation & LLM Output System  
**Target Version**: 2.0 (split-docs Command Stable)
