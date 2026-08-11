# Reviews (product verification)

Product-local verification maps and review notes for **ShellParser**.  
Not application source; not portable harness molds.

## Files

| Path | Role | When to update |
|------|------|----------------|
| `test-plan.md` | TP-ID catalog: intent, pass criteria, status (`have`/`todo`/`optional`/`n/a`) | Every add/change of suite assert or residual plan |
| `requirement-test-matrix.md` | Requirement → TP families; coverage verdict | When REQs or TP ownership change |
| `README.md` | This index | When new review artifacts are added |

## Rules

1. **Disk-truth:** Status **have** only when the named suite assert is green.  
2. **Domain IDs:** use **`TP-SHELLPARSER-*`** (subject from `requirement-domain-shellparser`). Do not use `TP-DOM-*`.  
3. **Git-surface for REQs:** versioned `docs/requirements/**` may cite TP-IDs + `tests/*` + `docs/reviews/*` only — not harness `docs/templates/**`.  
4. **Run command:** `PYTHONPATH=src python3 -m pytest tests/ -v` (see `test-plan.md` §2).  
5. After suite changes: flip statuses here **and** in each requirement’s Design-time verification table in the same change when possible.

## Related product surfaces

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Product law registry |
| `tests/` | Executable suite |
| `README.md` (repo root) | User install + test pointer |
