# Requirements index

**Workspace state:** **Software-development** (project class #2 — specialized product: ShellParser).  
**Updated:** 2026-08-11

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| RQ-CLASS-SOFTWARE-DEV | Software-development class law + residual stack | class | Active | `requirement-class-software-dev.md` | 2026-08-11 |
| RQ-DOMAIN-SHELLPARSER | ShellParser domain: split / replace / split-docs / placeholder / interactive | domain | Active | `requirement-domain-shellparser.md` | 2026-08-11 |
| RQ-PYTHON-CLI-INTERFACE | Python CLI surface, empty-argv Type N, flags | python | Active | `requirement-python-cli-interface.md` | 2026-08-11 |
| RQ-PYTHON-OUTPUT-REQUIREMENTS | ChronicleLogger output SSOT, quiet/json | python | Active | `requirement-python-output-requirements.md` | 2026-08-11 |
| RQ-PYTHON-PACKAGING | pyproject.toml packaging and console entry | python | Active | `requirement-python-packaging.md` | 2026-08-11 |
| RQ-PYTHON-ERROR-HANDLING | Python CLI error routing and safe failure | python | Active | `requirement-python-error-handling.md` | 2026-08-11 |
| RQ-BACKUP-STRATEGY | Dated backup before replace/placeholder mutate | ops | Active | `requirement-backup-strategy.md` | 2026-08-11 |

**Rules for agents:**

1. This registry is the **authoritative inventory** of product law for ShellParser.  
2. **Do not invent** `requirement-*.md` paths; append a row when creating a file in the same change.  
3. Class file **MUST** stay Active while class is software-development.  
4. Domain surface (split / replace / split-docs / placeholder / interactive) is owned by **RQ-DOMAIN-SHELLPARSER**.  
5. This surface lists **requirement rows only** — no harness path inventories.  
6. Keep Status in sync with each file header.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status consistent.
