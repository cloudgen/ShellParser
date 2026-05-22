# Backup Strategy Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the official backup strategy used by ShellParser to ensure **zero data loss** during `replace` operations and any future modifying commands. It is a critical safety layer of the CIAO-Lite philosophy.

## 2. Core Backup Rules (Mandatory)

- **Backup BEFORE any modification** — Never overwrite or edit the original file without a successful backup.
- **Dated incremental naming** — Format: `original.sh.YYYYMMDD-N`
- **N = incremental counter** — Starts at 1 on the same day, increments if multiple backups occur on the same day.
- **Preserve exact content** — Backup must be a byte-for-byte copy of the original at the moment of backup.
- **Backup location** — Same directory as the original file (unless overridden by future config).

### Example Backup Names
```
myscript.sh.20260510-1
myscript.sh.20260510-2
deploy.sh.20260511-1
```

## 3. Backup Workflow (Replace Command)

1. Enter `backup_source` state
2. Generate unique backup filename using current date + counter
3. Read original file content
4. Write full copy to backup file
5. Log success via ChronicleLogger
6. Only then proceed to `replace_function()`

## 4. Design Requirements

- Backup creation must be atomic where possible (write to temp → rename)
- Must work even if target directory is read-only or under version control
- Must respect file permissions and ownership
- Clear logging of backup path created
- Graceful error handling if backup fails (do not proceed with replace)
- Support for future `--dry-run` mode (simulate backup without writing)

## 5. Design Principles (CIAO-Lite)

- **Caution**: Assume the replace could fail or be interrupted — backup must always exist first.
- **Intentional**: Backup naming and location are explicitly documented and easy to locate.
- **Anti-fragile**: Incremental counter prevents overwriting same-day backups; dated format aids manual recovery.
- **Over-protect**: Backup logic is protected and must never be bypassed.

## 6. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Remove or weaken the "backup before replace" rule
- Write directly to the original file without creating a backup first
- Change the backup naming convention (`*.YYYYMMDD-N`) without updating this document and all related code
- Remove backup logging via ChronicleLogger
- Bypass backup in `replace_function()` or any future modifying commands
- Simplify backup logic "for cleanliness" or performance
- Hard-code backup paths instead of using the same directory as source (or future config)

## 7. Restore Guidance

Users can restore by:
```bash
cp myscript.sh.20260510-1 myscript.sh
```

Future versions may include a `restore` subcommand.

## 8. Future Enhancements (v1.1+)

- Configurable backup directory (`~/.app/ShellParser/backups/`)
- Automatic backup pruning (keep last N backups)
- Hash verification (SHA256) of backup vs original
- `--no-backup` flag for advanced users (with strong warning)
- Integration with git (optional `git commit` after replace)

---

**Last Updated**: May 2026  
**Owner**: Backup & Safety System  
**Target Version**: 1.1 (Backup Strategy Fully Documented)
