# Error Handling Requirements - ShellParser

**Status**: Active (Version 1.0+)

## 1. Purpose

This document defines the defensive error handling strategy used throughout ShellParser, with special attention to preserving Finite State Machine stability.

## 2. Core Principles

- Never silent failures
- All errors must be reported through ChronicleLogger
- Prefer graceful degradation over abrupt termination
- The StateLogic FSM must continue or reach a clean final state whenever possible
- Hard `sys.exit()` is **strongly discouraged** inside parser/FSM logic

## 3. Error Handling Patterns

### Recommended Pattern (FSM Safe)
```python
try:
    # operation
except Exception as e:
    self.logger.log_message(f"Error in stage {current_stage}: {e}", 
                           component="parser", level="error")
    # Graceful path: set error state, log details, continue to final state
    self.error_occurred(True)
    # Do NOT call sys.exit() here
```

### For CLI Level (main())
- Only at the very top level (outside FSM) is `sys.exit(1)` acceptable for fatal startup errors.
- Parser and StateLogic code must return control cleanly to the caller.

## 4. Error Handling in FSM Context

- Use dedicated error state or flag (`self.error_occurred(True)`)
- Allow the FSM to reach `parse_end` or `split_end` naturally
- Log full context (line number, component, stage, input snippet)
- Return meaningful status instead of crashing the machine

## 5. Validation & Early Checks

- Check file existence before starting FSM
- Validate arguments in `main()` before creating ShellParserCore
- Graceful fallback when target/components/ is missing in replace mode
- Defensive storage path resolution via ChronicleLogger

## 6. Design Principles (CIAO-Lite)

- **Caution**: Assume things can go wrong, but keep FSM alive
- **Intentional**: Errors should not break the state machine flow
- **Anti-fragile**: Parser survives malformed scripts and continues to final state
- **Over-protect**: No hard exits inside parser logic

## 7. Protection Rule (Sacred)

**Future AI or developers MUST NOT**:
- Use `sys.exit()` or `os._exit()` inside ShellParserCore or any FSM method
- Add bare `except:` that swallows exceptions without logging
- Let errors break the FSM transition chain
- Use `print()` for errors instead of ChronicleLogger
- Remove guidance messages like "run split first"

## 8. Future Enhancements

- Structured error objects for JSON mode
- Recovery suggestions in interactive mode
- Centralized error state handler in StateLogic

---

**Last Updated**: May 2026  
**Owner**: Error Handling & Resilience  
**Target Version**: 1.0+ (Error Strategy Frozen)
