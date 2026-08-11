# ShellParser tests

Executable verification for product requirements (TP-ID labeled).

## Run

```bash
# from repo root (deps: ChronicleLogger, StateLogic, pytest)
PYTHONPATH=src python3 -m pytest tests/ -v

# or after editable install
pip install -e ".[test]"
pytest -v
```

## Layout

| Path | Role |
|------|------|
| `test_shellparser_core.py` | Core TP suite |
| `fixtures/sample.sh` | Canonical shell fixture |
| `conftest.py` | Isolated tmp cwd + quiet logger |

## TP families (product)

| Family | Examples | Status map |
|--------|----------|------------|
| TP-SHELLPARSER | 01 split, 02 docs, 03 placeholder, 04 top-block | `docs/reviews/test-plan.md` |
| TP-CLI / TP-OUT | 01 JSON help, 02 quiet about, OUT-01 pure JSON | same |
| TP-PKG | 01 identity/version, 02 alias | same |
| TP-BAK | 01 replace backup+rewrite, 02 same-day counter | same |
| TP-ERR | 01 missing component | same |

**Do not use** deprecated `TP-DOM-*` IDs.

Full pass criteria, todos, and review findings: **`docs/reviews/test-plan.md`**.  
Requirement ownership: **`docs/reviews/requirement-test-matrix.md`**.
