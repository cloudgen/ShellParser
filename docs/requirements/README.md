# Requirements

Authoritative specialized product law for **ShellParser** (software-development class).

## Purpose

- **Plan** designs work from these docs and keeps them current.  
- **Implement** delivers code that traces to registered requirement keys / optional `RQ-*` IDs.  
- **Review** verifies delivery against requirements and CIAO defensive checklists.

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry SSOT (IDs, status, paths) — keep in sync with files |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Class gate

| Class | Required |
|-------|----------|
| software-development | Active `requirement-class-software-dev.md` |

## Rules

1. Never invent requirement paths not on disk.  
2. Class file only via class-requirement process; non-class REQs only after class is Active.  
3. Domain features live under `requirement-domain-*` (Area **domain**).  
4. Never dump harness inventories into this folder’s versioned surfaces.  
5. Product source cites live `requirement-*.md` / `RQ-*`, not templates or skills.
