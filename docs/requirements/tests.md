# Tests Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the official testing strategy for ShellParser, emphasizing safety, realism, and long-term maintainability under CIAO-Lite principles.

## 2. Lessons Learned (Critical)

- The parser is tightly coupled with real shell syntax, brace logic, and StateLogic FSM.
- Attempting small isolated unit tests on tokenizer, stage_2 ownership, or replace logic leads to fragile mocks and repeated breakage.
- Previous experiments with heavy mocking caused more friction than value.

**Key Lesson**:  
Do not test pieces in isolation when they require the full parser context. Prefer integration-style or full workflow verification.

## 3. Testing Philosophy (CIAO-Lite)

- **C - Caution**: Tests must not break production parser logic.
- **I - Intentional**: Respect the real 3-stage architecture.
- **A - Anti-fragile**: Tests should survive refactoring of non-protected areas.
- **O - Over-protect**: Never remove defensive checks just to make tests pass.

## 4. Allowed Testing Approaches

1. **Full Workflow Verification** (Recommended)
   - Run `shellparser split <test-script.sh>`
   - Run `shellparser replace <test-script.sh> <some-func>`
   - Manually verify output in target/components/ and backup creation.

2. **Integration Tests**
   - Test complete round-trip: split → edit component → replace → compare result.
   - Use real sample shell scripts with various edge cases (one-line functions, heredocs, compound commands).

3. **Compile / Install Checks**
   - `pip install -e .`
   - `pip install .`
   - Run `shell-parser --help` and `shell-parser about`

4. **Manual Edge Case Testing**
   - Scripts with nested braces, quoted strings, command substitutions, etc.

**Explicitly Forbidden**:
- Heavy unit testing of `tokenize_line()`, stage_2 reverse pass, or Attr-managed state.
- Mocks that weaken real brace calculation or tokenizer rules.

## 5. Protection Rule (Sacred)

Future AI or developers MUST NOT:
- Create isolated unit tests for the 3-stage parser core without explicit approval.
- Add test-only code that pollutes production files (cli.py, etc.).
- Simplify defensive logic to make tests green.
- Ignore the tight coupling reality of shell syntax parsing.

## 6. Test Scripts Location

- `tests/` directory (to be created)
- Include sample shell scripts with known tricky patterns.

---

**Last Updated**: May 2026  
**Owner**: Testing Strategy  
**Target Version**: 1.0+ (Defensive Foundation)
