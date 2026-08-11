# ShellParser product test plan

**Updated:** 2026-08-11  
**Product:** ShellParser **1.2.1**  
**Claim under proof:** C-full-product (domain CLI + packaging/output/error/backup)  
**Executable suite:** `tests/test_shellparser_core.py`  
**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Primary law:** `docs/requirements/index.md`

---

## 1. Purpose

Product status surface for design-time and run-time verification:

- Core TP-IDs are **have** only when suite asserts are green.  
- Domain cases use **`TP-SHELLPARSER-*`** (subject from `requirement-domain-shellparser`).  
- Stack families: `TP-CLI`, `TP-PKG`, `TP-BAK`, `TP-ERR`, `TP-OUT`.

---

## 2. How to run

```bash
cd /path/to/ShellParser
PYTHONPATH=src python3 -m pytest tests/ -v
```

**Isolation:** `tmp_path` cwd; no public network; no TTY Core cases.

---

## 3. Status legend

| Status | Meaning |
|--------|---------|
| **have** | Assert green |
| **todo** | Planned |
| **optional** | Not Core gate |
| **n/a** | Out of product claim |

---

## 4. Case catalog

### 4.1 Have (Core — suite green)

| TP-ID | Intent | Method | Pass criteria | Suite symbol | Primary REQ(s) | Status |
|-------|--------|--------|---------------|--------------|----------------|--------|
| **TP-PKG-01** | Version + console + repo identity | import + pyproject | `1.2.1`; `shellparser` entry; cloudgen/ShellParser | `test_TP_PKG_01_version_alignment` | RQ-PYTHON-PACKAGING, RQ-CLASS-SOFTWARE-DEV | **have** |
| **TP-PKG-02** | Compatibility alias | pyproject read | both `shellparser` and `shell-parser` entries | `test_TP_PKG_02_console_alias` | RQ-PYTHON-PACKAGING | **have** |
| **TP-CLI-01** | JSON help identity + verbs | CLI | JSON; usage has shellparser; full verb set | `test_TP_CLI_01_json_help_identity` | RQ-PYTHON-CLI-INTERFACE, RQ-DOMAIN-SHELLPARSER | **have** |
| **TP-CLI-02** | about --quiet | CLI | exit 0 | `test_TP_CLI_02_quiet_about` | RQ-PYTHON-CLI-INTERFACE, RQ-PYTHON-OUTPUT-REQUIREMENTS | **have** |
| **TP-OUT-01** | Pure JSON stdout for help | CLI | stdout strips to `{…}`; `json.loads` | `test_TP_OUT_01_json_help_pure_stdout` | RQ-PYTHON-OUTPUT-REQUIREMENTS | **have** |
| **TP-SHELLPARSER-01** | split → components | API | `target/components/*.sh` + known fn | `test_TP_SHELLPARSER_01_split_writes_components` | RQ-DOMAIN-SHELLPARSER | **have** |
| **TP-SHELLPARSER-02** | split-docs skeleton | API | metadata headers + ````sh` | `test_TP_SHELLPARSER_02_docs_markdown_skeleton` | RQ-DOMAIN-SHELLPARSER | **have** |
| **TP-SHELLPARSER-03** | placeholder backup first | API | `sample.sh.YYYYMMDD-N` matches pre-mutate | `test_TP_SHELLPARSER_03_placeholder_backup` | RQ-DOMAIN-SHELLPARSER, RQ-BACKUP-STRATEGY | **have** |
| **TP-SHELLPARSER-04** | replace preserves top-block | API | shebang not in hello.sh; after replace source starts with `#!/bin/sh`; greet/double_line remain | `test_TP_SHELLPARSER_04_replace_preserves_top_block` | RQ-DOMAIN-SHELLPARSER | **have** |
| **TP-BAK-01** | replace backup + rewrite | API | backup exists; body updated; shebang preserved | `test_TP_BAK_01_replace_backup_then_rewrite` | RQ-BACKUP-STRATEGY, RQ-DOMAIN-SHELLPARSER | **have** |
| **TP-BAK-02** | same-day backup counter | API | `-1` and `-2` both present | `test_TP_BAK_02_same_day_counter` | RQ-BACKUP-STRATEGY | **have** |
| **TP-ERR-01** | missing component abort | API | False; source unchanged | `test_TP_ERR_01_replace_missing_component` | RQ-PYTHON-ERROR-HANDLING | **have** |

### 4.2 Todo / n/a

| TP-ID | Intent | Status |
|-------|--------|--------|
| **TP-SHELLPARSER-05** | Empty-argv interactive Type N (non-hang harness) | **todo** |
| **TP-ERR-02** | Empty parse map → logger only | **todo** |
| **TP-LC-*** / **TP-CURL-*** | Online install lifecycle | **n/a** |

### 4.3 ID migration

| Deprecated | Replacement |
|------------|-------------|
| TP-DOM-SPLIT-01 | TP-SHELLPARSER-01 |
| TP-DOM-DOCS-01 | TP-SHELLPARSER-02 |
| TP-DOM-PLACEHOLDER-01 | TP-SHELLPARSER-03 |
| TP-BAK-REPLACE-01 | TP-BAK-01 |
| TP-ERR-MISS-COMP-01 | TP-ERR-01 |

---

## 5. Coverage summary

| Area | Have | Todo | n/a |
|------|------|------|-----|
| Packaging | TP-PKG-01, TP-PKG-02 | — | — |
| CLI / output | TP-CLI-01, TP-CLI-02, TP-OUT-01 | TP-SHELLPARSER-05 | Type O |
| Domain | TP-SHELLPARSER-01..04 | TP-SHELLPARSER-05 | — |
| Backup | TP-BAK-01, TP-BAK-02, TP-SHELLPARSER-03 | — | — |
| Errors | TP-ERR-01 | TP-ERR-02 | — |

**Gate “basic + domain integrity”:** all §4.1 **have** (includes TP-SHELLPARSER-04).

---

## 6. Review findings (closed / open)

| ID | Severity | Finding | Disposition |
|----|----------|---------|-------------|
| R-1 | Medium | Replace dropped shebang/top-block | **Fixed** 2026-08-11: shebang typed via `stripped.startswith("#!")`; Stage 2 leading preamble → `top-block`; **TP-SHELLPARSER-04 have** |
| R-2 | Low | Interactive Type N untested | Open → **TP-SHELLPARSER-05 todo** |
| R-3 | Info | Portable proof molds not local | Accept until H2 harness sync |
| R-4 | Info | JSON help purity | **TP-OUT-01 have** |

### Fix notes (R-1)

1. **Stage 1:** shebang detection uses stripped text (tokenizer returns `[]` for `#` lines).  
2. **Stage 2:** shebang owned as `top-block`; post-pass reassigns comment/blank lines before first `fn_start`/`fn_in_1_line` to `top-block`.  
3. **Replace:** only the named function group is overridden; top-block group remains.

---

## 7. Change log

| Date | Change |
|------|--------|
| 2026-08-11 | Initial have catalog |
| 2026-08-11 | Subject-family IDs; residual todos |
| 2026-08-11 | **Review+fix:** R-1 closed; TP-SHELLPARSER-04, TP-BAK-02, TP-OUT-01, TP-PKG-02 → have |
