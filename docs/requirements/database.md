# Database Requirements - ShellParser

**Status**: Draft (Target: Milestone 4.0)

## 1. Purpose

This document defines the persistent storage strategy using SQLite3 for ShellParser. It enables long-term knowledge retention of parsed tokens, functions, and metadata for advanced features (semantic search, versioning, AI context building, etc.).

## 2. Database Overview

- **Engine**: SQLite3 (single file, zero-configuration)
- **Default Location**: `~/.app/ShellParser/shellparser.db` (respecting ChronicleLogger storage resolution)
- **Purpose**: Store tokenized knowledge with full traceability

## 3. Core Schema

```sql
-- Main tokens table (line-level granularity)
CREATE TABLE IF NOT EXISTS tokens (
    line_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file      TEXT NOT NULL,
    function_name    TEXT,
    token_type       TEXT NOT NULL,        -- 'function', 'variable', 'string', 'heredoc', 'comment', 'command', etc.
    token_value      TEXT,
    leading_spaces   INTEGER DEFAULT 0,
    version_id       TEXT,                  -- e.g. git commit hash or semantic version
    last_updated     TEXT,                  -- ISO 8601 timestamp
    raw_line         TEXT,
    line_number      INTEGER
);

-- Functions metadata
CREATE TABLE IF NOT EXISTS functions (
    name             TEXT PRIMARY KEY,
    first_line       INTEGER,
    last_line        INTEGER,
    line_count       INTEGER,
    source_file      TEXT,
    last_modified    TEXT,
    version_id       TEXT
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_token_value ON tokens(token_value);
CREATE INDEX IF NOT EXISTS idx_function_name ON tokens(function_name);
CREATE INDEX IF NOT EXISTS idx_source_file ON tokens(source_file);
```

## 4. Configuration (Milestone 2.0+)

```ini
[database]
enabled = true
path = "~/.app/ShellParser/shellparser.db"
journal_mode = "WAL"
auto_vacuum = true
```

## 5. Usage in Milestones

- **v3.0**: Populated during semantic extraction (`split` / `split-docs`)
- **v4.0**: Full read/write support with versioning
- Future: Query interface for AI training data export

## 6. Design Principles (CIAO-Lite)

- **Caution**: Defensive initialization (create tables if missing), parameterized queries only (prevent SQL injection)
- **Intentional**: Clear separation between parser logic and database layer
- **Anti-fragile**: Graceful degradation if database is unavailable or corrupted
- **Over-protect**: Database path must respect ChronicleLogger storage rules (never hard-coded)

## 7. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Hard-code database path after Milestone 2.0 (must use configurable storage)
- Use raw string concatenation for SQL queries (always use parameters)
- Remove or weaken defensive initialization and error handling
- Store sensitive data without encryption consideration
- Bypass database module for direct SQLite access
- Change core table schema without migration strategy and changelog entry

## 8. Future Enhancements (v4.0+)

- Migration system for schema changes
- Export functions (JSON, CSV, fine-tuning datasets)
- Query API for LLM context retrieval
- Version history tracking per function
- Optional encryption for sensitive projects

---

**Last Updated**: May 2026  
**Owner**: Persistence Layer  
**Target Version**: 4.0 (Database Milestone)
