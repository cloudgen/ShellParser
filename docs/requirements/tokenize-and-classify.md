# Tokenize and Classify Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the enhanced tokenizer and line classification logic used in Stage 1 of the parser.

## 2. Core Requirements

### tokenize_line()
- Must treat quoted strings ("..." and '...') as single atomic tokens
- Must treat command substitutions ($(...) and `...`) as single tokens
- Must correctly detect function definitions (name() { or name() { on same line)
- Must handle compound commands (&&, ||, ;, |)
- Early exit for pure comment lines and blank lines

### Classification Priority (Strict Order)
1. Shebang (first line)
2. Comments
3. Heredoc start / body / end
4. Blank lines
5. Function definitions (fn_start, fn_in_1_line)
6. Control structures (if, while, case, etc.)
7. Logical operators (&&, ||)
8. Assignments
9. Commands / printf / exit
10. Body / brace fallback (default)

## 3. Key Design Rules

- Real brace level calculation on every relevant line
- Preserve original whitespace and raw line content
- Never use simple string.split() for tokenization
- Function name must be correctly captured even for one-line functions

## 4. Design Principles (CIAO-Lite)

- Caution: Robust handling of real-world messy shell syntax
- Intentional: Clear priority order prevents misclassification
- Anti-fragile: Survives complex scripts with nested constructs
- Over-protect: Tokenizer logic is heavily protected

## 5. Protection Rule (Sacred)

Future AI or developers MUST NOT:
- Replace tokenizer with simple regex or split()
- Change classification priority order
- Hard-code token positions or brace numbers
- Remove support for quoted strings or command substitutions
- Simplify classify_* helper functions

## 6. Future Enhancements

- Better support for arrays and here-strings
- Configurable classification rules for custom shells

---

**Last Updated**: May 2026  
**Owner**: Tokenizer Engine  
**Target Version**: 1.0+ (Tokenizer Frozen)
