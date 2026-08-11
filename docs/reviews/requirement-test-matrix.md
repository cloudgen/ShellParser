# Requirement ↔ test matrix (ShellParser)

**Updated:** 2026-08-11  
**Map:** `docs/reviews/test-plan.md`  
**Suite:** `tests/test_shellparser_core.py`  
**Registry:** `docs/requirements/index.md`

---

## 1. How to read

| Column | Meaning |
|--------|---------|
| Have (Core) | Green TP-IDs |
| Todo | Planned |
| Coverage verdict | **Covered** · **Partial** · **Open** · **n/a** |

---

## 2. Matrix

| Requirement | Area | Have (Core) | Todo | Coverage verdict | Notes |
|-------------|------|-------------|------|------------------|-------|
| **RQ-CLASS-SOFTWARE-DEV** | class | TP-PKG-01 | — | **Covered** | Residual stack smoke |
| **RQ-DOMAIN-SHELLPARSER** | domain | TP-SHELLPARSER-01..04, TP-BAK-01, TP-CLI-01 | TP-SHELLPARSER-05 | **Covered** (Core integrity); interactive still todo | R-1 fixed |
| **RQ-PYTHON-CLI-INTERFACE** | python | TP-CLI-01, TP-CLI-02 | TP-SHELLPARSER-05 | **Partial** | Flags/help have; empty-argv interactive todo |
| **RQ-PYTHON-OUTPUT-REQUIREMENTS** | python | TP-CLI-02, TP-OUT-01 | TP-ERR-02 | **Covered** (Core quiet/JSON) | Pure JSON help have |
| **RQ-PYTHON-PACKAGING** | python | TP-PKG-01, TP-PKG-02 | — | **Covered** | Primary + alias |
| **RQ-PYTHON-ERROR-HANDLING** | python | TP-ERR-01 | TP-ERR-02 | **Partial** | Missing component have |
| **RQ-BACKUP-STRATEGY** | ops | TP-BAK-01, TP-BAK-02, TP-SHELLPARSER-03 | — | **Covered** | Backup-before-mutate + same-day N |

---

## 3. Family index

| Family | IDs (have unless noted) |
|--------|-------------------------|
| **TP-SHELLPARSER** | 01–04 have; **05 todo** |
| **TP-CLI** | 01–02 have |
| **TP-PKG** | 01–02 have |
| **TP-BAK** | 01–02 have |
| **TP-ERR** | 01 have; **02 todo** |
| **TP-OUT** | 01 have |
| **TP-LC / TP-CURL** | **n/a** |

---

## 4. Next proof priorities

1. **TP-SHELLPARSER-05** — Type N interactive (non-hang harness).  
2. **TP-ERR-02** — empty parse map logger path.

---

## 5. Change log

| Date | Change |
|------|--------|
| 2026-08-11 | Initial rows |
| 2026-08-11 | Subject family + partial verdicts |
| 2026-08-11 | **Review+fix:** domain/backup/output/packaging promoted to Covered where applicable |
