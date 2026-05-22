#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# ShellParser.py — v1 AI-Augmented Shell Script Component Manager
# Exact PyDocCore / StateLogic pattern with CIAO-Lite Protection
# =============================================================================
#
# PURPOSE & AI INTEGRATION INTENT (INNOVATION SHIELD)
# =================================================================================
# This tool was purpose-built as an AI / Grok collaboration platform for
# maintaining large, complex, legacy shell scripts (thousands of lines).
#
# Core Innovation:
#   • Split massive shell scripts into clean, single-responsibility component files
#   • Enable safe, surgical editing of individual functions by AI
#   • Reassemble via safe "replace" with automatic dated backup
#   • Quiet/JSON-friendly logging foundation (via ChronicleLogger) for reliable
#     AI-driven pipelines
#
# Why this is innovative and among the first of its kind:
#   Traditional shell tools focus on linting or simple extraction.
#   This project creates a true bidirectional human-AI workflow:
#     AI can now work on small, focused .sh components instead of fighting
#     with monolithic files that exceed context windows.
#   The combination of 3-stage parsing, backward ownership correction,
#   compound-command safety, and backup-before-replace makes it uniquely
#   safe for production use with AI agents.
#
# Battlefield-Proven for Grok Sessions:
#   Multiple previous Grok attempts failed on complex scripts.
#   This architecture survived real-world messy shell code and enables
#   scalable AI-assisted modernization of shell ecosystems.
#
# CIAO-DEFENSIVE HISTORY & LESSONS LEARNED (ANTI-FRAGILITY SHIELD)
# =================================================================================
# This file is the result of real battlefield testing against complex shell scripts.
# Multiple Grok sessions failed before reaching this stable architecture.
#
# HISTORY OF FAILED ATTEMPTS (DO NOT REPEAT):
#   1. Simple regex-based function extraction          → Failed completely
#   2. Naive multi-phase / multi-pass approaches       → Still lost state
#   3. Direct list .append() on Attr objects           → Broke StateLogic contractv
#   4. Hard-coded numbers ("2", "3") in and_logic/or_logic → Caused brace_level drift
#   5. Over-simplification / refactoring of brace logic → Repeated regression
#
# KEY LESSONS LEARNED AND NOW ENFORCED:
#   • State management must use StateLogic + Attr (autostrip, sorting=False)
#   • Direct assignment only: self.map_array(entry) — NEVER .append()
#   • Brace_level MUST use real calculation everywhere
#   • 3-Stage architecture is intentional and required
#   • Compound commands must not corrupt function brace_level 
#     (solved by improvement in tokenization)
#   • recognizes quoted strings, $(...), and `...` as single tokens.
#   • Real calculation everywhere with strong protection against hard-coding.
#     Minor fragility in compound command edge cases has already been
#     significantly improved by enhanced tokenize_line() that properly
#     recognizes quoted strings, $(...), and `...` as single tokens.
#   • stage_1_parse was originally very long but intentionally shortened
#     by extracting classify_* helper methods (classify_non_special_line,
#     classify_body_brace_fallback, classify_fn_definition*, etc.)
#     while preserving exact original behavior, type priority order,
#     and all Protection Zones.
#
# CIAO-Lite PROTECTION RULE FOR ALL FUTURE AI / GROK / HUMAN:
# =================================================================================
# This is battlefield-hardened code designed for AI collaboration.
# Any attempt to:
#   - Replace with simple regex
#   - Remove or merge the 3 stages
#   - Use .append() on Attr lists
#   - Hard-code numbers in brace logic
#   - "Simplify" or refactor protected zones
#   - Use direct print() — ChronicleLogger is the SINGLE source of output
# WILL BE REJECTED.
#
# All user-facing output MUST go through self.logger.log_message()
# or ChronicleLogger. This protects quiet/JSON modes and keeps
# output behavior consistent and anti-fragile.
#
# All changes must respect CIAO-Lite principles https://github.com/cloudgen/ciao :
#   C - Caution, I - Intentional, A - Anti-fragile, O - Over-protects
#
# Previous Groks failed. This version survived real scripts and enables
# scalable AI-assisted shell maintenance.
# Protect it.
# =================================================================================

from __future__ import print_function, absolute_import, division, unicode_literals

import argparse
import os
import re
import sys
import json
from datetime import datetime

from statelogic import StateLogic, Attr
from ChronicleLogger import ChronicleLogger


class ShellParserCore(StateLogic):

    """ShellParserCore - Main parser engine for shell scripts.

    CIAO-Lite Protection Zone
    =================================================================================
    DO NOT refactor, simplify, or redesign this class without explicit user instruction.

    General Purpose:
        Core parser that converts raw shell scripts into structured line classification,
        correct function ownership, and extracted component files using a controlled FSM.

    Current Logic:
        - Uses StateLogic FSM pattern with explicit transitions
        - State names are defined directly in transition() calls
        - Hooks (before/after/on) control execution flow at key points
        - 3-Stage architecture (forward parse → backward ownership → extraction)

    Defensive Notes:
        - Hooks and transitions are the backbone of this parser
        - All state changes are logged when STATE=show environment variable is set
        - This design was chosen after previous Grok regex and naive approaches failed
        - Battlefield-tested and must remain stable
    =================================================================================
    """

    CLASSNAME = "ShellParserCore"
    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 1

    @staticmethod
    def class_version():
        return "{0.CLASSNAME} v{0.MAJOR_VERSION}.{0.MINOR_VERSION}.{0.PATCH_VERSION}".format(ShellParserCore)

    def __init__(self, file_path, logger):
        """Initialize ShellParserCore exactly like PyDocCore pattern.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT modify initialization logic, Attr declarations, or FSM setup
        without explicit user instruction.

        General Purpose:
            Set up the StateLogic FSM, Attr descriptors, and initial parser state.

        Current Logic:
            - Call parent StateLogic initializer
            - Create ChronicleLogger
            - Declare all Attr attributes with correct parameters 
              (autostrip=False, sorting=False where needed)
            - Define FSM transitions
            - Register hooks (before/after/on)
            - Start the parsing process

        Defensive Notes:
            - Attr usage must be respected: direct assignment only 
              (self.map_array(entry), never .append())
            - brace_level, func_name, last_func are critical state variables
            - is_json and is_quiet are now managed via Attr (no fragile methods)
            - This initialization is battlefield-tested and must remain stable
            - Any change here can break all three stages
        =================================================================================
        """
        try:
            super().__init__(self)
        except:
            super(ShellParserCore, self).__init__(self)

        self.logger = logger

        # Attr attributes (exact PyDocCore style)
        Attr(self, attrName='file_path', value=file_path)
        Attr(self, attrName='file_content', value=[])
        Attr(self, attrName='line', value='', autostrip=False)
        Attr(self, attrName='line_num', value=0)
        
        # map_lines for display only, don't use for processing
        Attr(self, attrName='map_lines', value=[], sorting=False)
        
        # map_lines for processing only
        Attr(self, attrName='map_array', value=[], sorting=False)
        Attr(self, attrName='map_array_for_file', value=[], sorting=False)
        
        Attr(self, attrName='brace_level', value=0)
        Attr(self, attrName='func_name', value="")
        Attr(self, attrName='last_func', value="")

                # JSON / Quiet mode management via Attr
        Attr(self, attrName='is_json', value=False)
        Attr(self, attrName='is_quiet', value=False)
        Attr(self, attrName='source_file', value="")
        Attr(self, attrName='source_func', value="")

        # For safe replace: memorize function content by name (stage_3 style)
        Attr(self, attrName='func_content_map', value={}, sorting=False)

        Attr(self, attrName='replace_mode', value=False)
        # Output control switch (new Attr as requested)
        Attr(self, attrName='output_enabled', value=True)

        # FSM states and transitions
        self.transition('backup_source', 'start_backup', 'backed_or_no_need')
        self.transition('start_parse', 'backed_or_no_need', 'line_read')
        self.transition('tokenize', 'line_read', 'line_parsed')
        self.transition('next_line', 'line_parsed', 'line_read')
        self.transition('last_line', 'line_read', 'parse_end')
        self.transition('split_file', 'parse_end', 'split_end')

        # Hooks (PyDocCore style)
        self.after('backup_source', self.after_backup_source)
        self.before('start_parse', self.parse_file)
        self.after('start_parse', self.afterStartParse)
        self.after('last_line', self.afterLastLine)
        self.on('tokenize', self.onTokenize)
        self.on('split_file', self.replace_function)
        
    # =========================================================================
    # Core Methods (following PyDocCore structure)
    # =========================================================================

    def parse_file(self):
        """Read the shell script"""
        self.file_content = []
        with open(self.file_path(), 'r', encoding='utf-8') as f:
            for line in f:
                self.file_content.append(line.rstrip('\n'))
        self.logger.log_message(f"Loaded {len(self.file_content)} lines", component="parser")
        return True

    def afterStartParse(self):
        """Main processing loop - Entry point after file loading.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, inline, or remove this method without explicit user instruction.

        General Purpose:
            Orchestrate the complete 3-stage parsing pipeline after the file is loaded.

        Current Logic:
            - Forward loop over all lines:
                • Set line_num and line
                • Call tokenize() → triggers onTokenize() → stage_1_parse()
            - After forward pass completes:
                • stage_1_report()     → generates debug report
                • stage_2_ownership()  → backward ownership correction
                • stage_3_extract_functions() → write files

        Defensive Notes:
            - This is the central coordinator of the 3-stage architecture
            - Order of stages is critical: forward → report → backward → extract
            - Previous attempts to merge stages or remove the loop broke ownership and brace logic
            - Protected to maintain the intentional separation proven through battlefield testing
            - output_enabled switch prevents overwriting components during replace
        =================================================================================
        """
        for index, line in enumerate(self.file_content, start=1):
            self.line_num(index)
            self.line(line)
            self.tokenize()
            self.next_line()

        if self.output_enabled():
            self.stage_1_report()
            self.stage_2_ownership()
            self.stage_3_extract_functions()
        else:
            # Replace mode: only update ownership map, no file output
            self.stage_2_ownership()
            self.last_line()
        
    def afterLastLine(self):
        if self.replace_mode():
            self.split_file()

    def after_backup_source(self):
        """Backup source before replace (FSM entry point for replace mode).

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT simplify, refactor, or remove without explicit user instruction.
        =================================================================================
        """
        # === CREATE BACKUP FIRST ===
        date_str = datetime.now().strftime("%Y%m%d")
        base = os.path.basename(self.source_file())
        dir_name = os.path.dirname(self.source_file()) or "."
        counter = 1
        while True:
            backup_name = f"{base}.{date_str}-{counter}"
            backup_path = os.path.join(dir_name, backup_name)
            if not os.path.exists(backup_path):
                break
            counter += 1

        with open(self.source_file(), 'r', encoding='utf-8') as f:
            original_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)

        self.logger.log_message(f"Backup created: {backup_path}", component="replace")
        self.start_parse()

    def replace_function(self):
        """Replace specific function using version from target/components/ + create backup.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT simplify, refactor, or remove without explicit user instruction.

        General Purpose:
            - Create backup {original_name}.YYYYMMDD-N (N = incremental trial)
            - Rebuild full script using existing map_array_for_file
            - Override ONLY the target function with content from components/{func_name}.sh
            - Write updated script back to original location

        Current Logic:
            - Backup created FIRST (safety)
            - Parse already done by caller (components are up-to-date)
            - Group lines exactly like stage_3 but override target function
            - Preserve original order and whitespace

        Defensive Notes:
            - Uses existing map_array_for_file (no new parsing stage)
            - Only the target function is replaced; all other code untouched
            - Battlefield safety: original file never modified until backup succeeds
        =================================================================================
        """
        component_path = os.path.join("target", "components", f"{self.source_func()}.sh")
        if not os.path.exists(component_path):
            self.logger.log_message(f"Error: Component file not found: {component_path}", component="replace", level="error")
            self.logger.log_message("       Run 'split' first or check target/components/", component="replace", level="error")
            return False

        # Read replacement content (already in correct order)
        with open(component_path, 'r', encoding='utf-8') as f:
            new_func_lines = [line.rstrip('\n') for line in f.readlines()]

        # === REBUILD SCRIPT WITH REPLACED FUNCTION ===
        arr = self.map_array_for_file()
        if not arr:
            print("Error: No parsed data available")
            return False

        func_lines = {}
        func_names_array = []
        for i in range(len(arr)-1, -1, -1):
            item = arr[i]
            f_name = item.get('func_name', '')
            if f_name not in func_lines:
                func_lines[f_name] = []
                func_names_array.append(f_name)

            if f_name == self.source_func():
                func_lines[f_name] = new_func_lines[:]   # override with component version
            else:
                func_lines[f_name].append(item['raw'])

        # Re-assemble full script (double-reverse restores original order)
        full_script_lines = []
        for func in func_names_array:
            full_script_lines.extend(func_lines[func])

        full_script = '\n'.join(full_script_lines) + '\n'

        # Write updated script
        with open(self.source_file(), 'w', encoding='utf-8') as f:
            f.write(full_script)

        self.logger.log_message(f"Function '{self.source_func()}' replaced from components/", component="replace")
        self.logger.log_message(f"Successfully replaced function '{self.source_func()}' from components/")
        return True

    # =========================================================================
    # New independent indent calculator (protected)
    # =========================================================================
    def calculate_indent(self, line):
        """Independent method to count leading spaces only.
        CIAO-Lite Protection Zone - do not refactor without explicit instruction"""
        if not line:
            return 0
        # Count only spaces (not tabs). Use expandtabs(4) if you ever want tab support.
        return len(line) - len(line.lstrip(' '))

    def show_about(self):
        """Display system and parser environment information.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, simplify, add print(), add any return for quiet mode,
        add any manual quiet check, move JSON block, or remove without explicit 
        user instruction.

        General Purpose:
            Show version, Python, date, working directory — ShellParser style.

        Current Logic:
            Always call self.logger.log_message(). ChronicleLogger is the single source of truth.
            It decides to print or not based on quiet mode.
            JSON output takes absolute priority when --json flag is used.

        Lessons Learned (Why Previous Grok Agents Kept Failing):
            - Many previous Grok sessions added fragile early returns for quiet mode.
            - They put quiet checks before JSON block, causing polluted or missing JSON.
            - They ignored that ChronicleLogger must be the single source of truth.
            - They weakened Protection Zones and removed intentional verbosity.
            - This is exactly why CIAO-Lite was created: to stop repeated regression
              caused by over-eager simplification and failure to respect "no return for quiet".

        Defensive Notes (Exactly as per user instruction):
            - No return for quiet
            - ChronicleLogger is the single source of truth. It determines to print or not to print.
            - Do not use fragile code in this method.
            - JSON check must stay first.
            - This block protects against the exact failure patterns seen in past Grok sessions.
        =================================================================================
        """
        data = {
            "tool": "ShellParser",
            "version": ShellParserCore.class_version(),
            "python": sys.version.split()[0],
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "working_dir": os.getcwd(),
            "target_dir": "./target/components/"
        }

        if self.is_json():
            print(json.dumps(data, indent=2))
        else:
            self.logger.log_message("ShellParser - Environment Information")
            self.logger.log_message("=" * 50)
            for k, v in data.items():
                self.logger.log_message(f"{k.replace('_', ' ').title():<15} : {v}")
            self.logger.log_message("=" * 50)

    def show_help(self):
        """Display rich ShellParser-style help.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, simplify, shorten, add print(), add any return for quiet mode,
        add any manual quiet check, move JSON block, or remove without explicit 
        user instruction.

        General Purpose:
            Provide comprehensive help exactly like ShellParser.

        Current Logic:
            Always call self.logger.log_message(). ChronicleLogger is the single source of truth.
            It decides to print or not based on quiet mode.
            JSON output takes absolute priority when --json flag is used.

        Lessons Learned (Why Previous Grok Agents Kept Failing):
            - Previous Grok versions repeatedly introduced early returns before JSON.
            - They treated --quiet as higher priority than --json, breaking JSON output.
            - They ignored the core rule that logger must control output (single source of truth).
            - They weakened defensive comment blocks and removed intentional safety layers.
            - This pattern of "helpful simplification" caused repeated regression across
              multiple sessions — exactly the reason CIAO-Lite and the long defensive
              history shield were created.

        Defensive Notes (Exactly as per user instruction):
            - No return for quiet
            - ChronicleLogger is the single source of truth. It determines to print or not to print.
            - Do not use fragile code in this method.
            - JSON block must remain first to prevent pollution.
            - This protection is intentional and must survive future AI interactions.
        =================================================================================
        """
        if self.is_json():
            help_data = {
                "tool": "ShellParser",
                "version": ShellParserCore.class_version(),
                "usage": "shellparser <command> [--quiet] [--json]",
                "commands": {
                    "split": "Split shell script into target/components/*.sh",
                    "replace": "Replace function from components/ (with backup)",
                    "about": "Show environment & version info",
                    "help": "Show this help"
                }
            }
            print(json.dumps(help_data, indent=2))
        else:
            self.logger.prn("ShellParser — AI-Augmented Shell Script Component Manager")
            self.logger.prn("=" * 70)
            self.logger.prn(f"Version : {ShellParserCore.class_version()}")
            self.logger.prn("")
            self.logger.prn("Usage:")
            self.logger.prn("  shellparser <command> [--quiet] [--json]")
            self.logger.prn("")
            self.logger.prn("Available Commands:")
            self.logger.prn("  split <source_file>      Split shell script into target/components/*.sh")
            self.logger.prn("  replace <source_file> <func_name>   Replace function (with backup)")
            self.logger.prn("  about                    Show environment & version info")
            self.logger.prn("  help                     Show this help")
            self.logger.prn("")
            self.logger.prn("Examples:")
            self.logger.prn("  shellparser split myscript.sh")
            self.logger.prn("  shellparser replace myscript.sh my_function")
            self.logger.prn("  shellparser about")
            self.logger.prn("  shellparser help")
            self.logger.prn("")
            self.logger.prn("AI Collaboration Workflow:")
            self.logger.prn("  1. split   → break large script into small editable functions")
            self.logger.prn("  2. Edit individual *.sh files with AI")
            self.logger.prn("  3. replace → safely merge back with automatic backup")
            self.logger.prn("")
            self.logger.prn("Quiet / JSON Ready:")
            self.logger.prn("  --json implies quiet mode to prevent output pollution")
            self.logger.prn("=" * 70)

    def tokenize_line(self, line):
        """Real shell tokenizer - produces tokens while preserving important shell constructs.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, simplify, or rewrite this tokenizer without explicit user instruction.

        General Purpose:
            Convert a raw shell line into a list of meaningful tokens for accurate classification
            in stage_1_parse. Must correctly handle strings, command substitutions, function
            parentheses, and special characters.

        Current Logic:
            - Early exit for pure comment lines (first non-space char is '#')
            - Handles: double/single quoted strings as single tokens
            - Handles: $(...) and `...` as single tokens (even with internal spaces)
            - Treats '(' immediately after identifier as separate token (critical for function detection)
            - Preserves standalone '(', ')', '{', '}', '=', ';'
            - Skips whitespace

        Defensive Notes:
            - This tokenizer is the foundation of correct function detection and brace handling
            - Changing how '(' is split or how strings are treated will break stage_1_parse
            - Must remain robust against real-world messy shell syntax (nested subs, escaped quotes, etc.)
            - Previous simple regex approaches failed here — this token-based method survived
        =================================================================================
        """
        # Early exit for comment lines: first non-space char is '#'
        stripped = line.lstrip()
        if stripped and stripped[0] == '#':
            return []                     # ← as requested

        tokens = []
        i = 0
        n = len(line)
        while i < n:
            c = line[i]
            if c.isspace():
                i += 1
                continue

            # 1. Double-quoted string (whole thing = one token)
            if c == '"':
                j = i + 1
                while j < n and not (line[j] == '"' and (j == 0 or line[j-1] != '\\')):
                    j += 1
                tokens.append(line[i:j+1])
                i = j + 1
                continue

            # 1. Single-quoted string (whole thing = one token)
            if c == "'":
                j = i + 1
                while j < n and line[j] != "'":
                    j += 1
                tokens.append(line[i:j+1])
                i = j + 1
                continue

            # 4. $(...) command substitution (one token even with spaces)
            if line[i:i+2] == "$(":
                count = 1
                j = i + 2
                while j < n and count > 0:
                    if line[j:j+2] == "$(":
                        count += 1
                    elif line[j] == ')':
                        count -= 1
                    j += 1
                tokens.append(line[i:j])
                i = j
                continue

            # 4. `...` backtick substitution (one token)
            if c == '`':
                j = i + 1
                while j < n and line[j] != '`':
                    j += 1
                tokens.append(line[i:j+1])
                i = j + 1
                continue

            # 2. Semicolon = separate token
            if c == ';':
                tokens.append(';')
                i += 1
                continue

            # Identifier followed immediately by ( → split into two tokens: name + '('
            if (c.isalnum() or c == '_'):
                j = i
                while j < n and (line[j].isalnum() or line[j] == '_'):
                    j += 1
                token = line[i:j]
                tokens.append(token)
                i = j
                # Make '(' a separate token
                if i < n and line[i] == '(':
                    tokens.append('(')
                    i += 1
                continue

            # Other single-character tokens (including standalone '(' / ')' / '{' / '}' / '=')
            if c in '(){}=;':
                tokens.append(c)
                i += 1
                continue

            # Normal token (e.g. VAR=12 was already handled above, operators, etc.)
            j = i
            while j < n and not line[j].isspace() and line[j] not in '"\'`;(){}':
                j += 1
            token = line[i:j]
            if token:
                tokens.append(token)
            i = j
        return tokens

    def classify_and_or_logic(self, tokens, stripped, raw):
        """and_logic / or_logic classifier for lines containing && or ||.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT hard-code any numbers (especially no "2" or "3").
        MUST use real brace calculation to stay 100% aligned with 
        classify_fn_definition and the body fallback logic.

        General Purpose:
            Correctly classify logical operator lines while maintaining accurate
            brace_level for the overall parser state.

        Current Logic:
            - Determine base type: "and_logic" or "or_logic"
            - Count real opening and closing braces using tokens.count()
            - Update brace_level with net change (same calculation style as everywhere else)
            - Append suffix based on CURRENT brace_level after update 
              (e.g. and_logic_1, or_logic_2, etc.)

        Defensive Notes:
            - This function must NEVER introduce special hard-coded cases for compound commands
            - Real brace calculation is mandatory for consistency across all stages
            - Previous attempts with hard-coded "2" caused brace_level drift and wrong fn_end
            - Protected to prevent future AI from repeating the same mistake
        =================================================================================
        """
        typ = "and_logic" if '&&' in tokens else "or_logic"

        # Real brace calculation - must stay aligned with other parts of the parser
        brace_open  = tokens.count('{')
        brace_close = tokens.count('}')
        self.brace_level(self.brace_level() + brace_open - brace_close)

        # Suffix from real current brace_level (no hard-coded numbers)
        current = self.brace_level()
        if current > 0:
            typ = typ + "_" + str(current)

        return typ

    def classify_fn_definition(self, first_token, tokens):
        """Function definition classifier for pattern: name() { or name () {

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT hard-code any numbers.
        MUST use real brace counting (tokens.count) to stay perfectly aligned
        with classify_and_or_logic and the body fallback logic.

        General Purpose:
            Detect and classify function definitions, manage func_name / last_func state,
            and correctly update brace_level.

        Current Logic:
            - Count real opening and closing braces using tokens.count('{') and tokens.count('}')
            - Handle three main cases:
                1. One-line function: name() { ... }   ← now correctly keeps func_name
                2. Function start:    name() {
                3. Inside existing function body
            - Update brace_level only on real function opening '{'

        Defensive Notes:
            - Real brace calculation is mandatory — no hard-coded values allowed
            - This function must stay 100% consistent with classify_and_or_logic
            - Previous Grok versions introduced hard-coded "2" and caused brace_level drift
            - Critical for correct fn_start / fn_end detection across all stages
            - Fixed one-line function ownership reporting (lines 37-40 in report)
        =================================================================================
        """
        func_name = first_token
        brace_open  = tokens.count('{')
        brace_close = tokens.count('}')

        if brace_open == 1 and brace_close == 1:
            self.last_func(func_name)      # ← Fixed: keep func_name for reporting
            self.func_name("")             # clear current for next lines
            return "fn_in_1_line", func_name, 0
        elif brace_open == 1 and brace_close == 0:
            self.func_name(func_name)
            self.last_func(func_name)
            self.brace_level(self.brace_level() + 1)
            return "fn_start", func_name, 1
        elif self.func_name() != "":
            return "fn_body", self.func_name(), 1
        else:
            return "command", "", 0

    def classify_fn_definition_alt(self, stripped, tokens):
        """Alternative function definition classifier for pattern: name () { 

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT hard-code any numbers.
        MUST use real brace counting (tokens.count) to stay perfectly aligned
        with classify_and_or_logic and classify_fn_definition.

        General Purpose:
            Handle the alternative function definition syntax such as:
                func () {
            and correctly update state and brace_level.

        Current Logic:
            - Uses regex to detect "name ()" pattern
            - Counts real braces using tokens.count('{') and tokens.count('}')
            - Handles three main cases (one-line, start, body) exactly like 
              classify_fn_definition
            - Returns (typ, func_name, f_on) tuple or None if not matched

        Defensive Notes:
            - Real brace calculation is mandatory — no hard-coded values allowed
            - Must remain perfectly consistent with classify_fn_definition
            - This alternative path is required for certain shell coding styles
            - Protected against future "simplification" that would break alignment
        =================================================================================
        """
        m = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\)', stripped)
        if not m:
            return None

        func_name = m.group(1)
        brace_open  = tokens.count('{')
        brace_close = tokens.count('}')

        if brace_open == 1 and brace_close == 1:
            self.last_func(func_name)
            self.func_name("")
            return "fn_in_1_line", "", 0
        elif brace_open == 1 and brace_close == 0:
            self.func_name(func_name)
            self.last_func(func_name)
            self.brace_level(self.brace_level() + 1)
            return "fn_start", func_name, 1
        elif self.func_name() != "":
            return "fn_body", self.func_name(), 1
        else:
            return "top_level", "", 0

    def classify_body_brace_fallback(self, stripped, tokens, raw, f_on):
        """Body / brace fallback classifier.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, simplify, merge back, or remove this method without explicit 
        user instruction.

        General Purpose:
            Handle the final fallback classification for lines that are not control 
            structures, not explicit function definitions, and not special cases.
            This includes function body detection, brace management, variable 
            interpolation, assignment, and top_level defaults.

        Current Logic:
            - Alternative function pattern check via classify_fn_definition_alt
            - Variable interpolation (${var})
            - Real brace counting with compound command protection (|| { / && {)
            - fn_end detection when dropping to brace_level 0
            - brace_start / brace_end suffix logic
            - fn_body default inside functions
            - Final assignment / top_level fallback

        Defensive Notes:
            - Real brace calculation (tokens.count) is mandatory — never use hard-coded numbers
            - Compound command protection block must stay exactly as-is
            - This logic was extracted from stage_1_parse to reduce method length while 
              preserving exact original behavior and state updates
            - Must remain perfectly aligned with classify_fn_definition*, 
              classify_and_or_logic, and the main stage_1_parse flow
            - Previous attempts to inline or simplify this section caused brace_level drift
        =================================================================================
        """
        typ = "top_level"
        func_name = ""
        # f_on is passed by value but we may modify local copy

        m = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*\)', stripped)
        if m:
            result = self.classify_fn_definition_alt(stripped, tokens)
            if result:
                typ, func_name, f_on = result
            else:
                typ = "top_level"
        elif f_on or self.brace_level() > 0:
            m = re.match(r'.*\$\{([^\}]+)\}.*', stripped)
            if m:
                typ = "variable"
                func_name = self.func_name()
            else:
                # === COMPOUND COMMAND PROTECTION ===
                brace_open  = tokens.count('{')
                brace_close = tokens.count('}')

                is_compound_closing = (
                    stripped.strip() == '}' and
                    ('|| {' in raw or '&& {' in raw or 
                     '||{' in raw.replace(' ','') or '&&{' in raw.replace(' ',''))
                )

                if brace_close > 0 and not is_compound_closing:
                    current_level = self.brace_level()
                    if current_level == 1 and brace_close >= 1:
                        typ = "fn_end"
                        func_name = self.func_name()
                        self.func_name("")
                        self.brace_level(0)
                    else:
                        new_level = max(0, current_level - brace_close)
                        self.brace_level(new_level)
                        typ = "brace_end_" + str(new_level) if new_level > 0 else "brace_end"
                        func_name = self.func_name()
                elif brace_open > 0:
                    new_level = self.brace_level() + brace_open
                    self.brace_level(new_level)
                    typ = "brace_start_" + str(new_level)
                    func_name = self.func_name()
                    self.func_name("")
                else:
                    typ = "fn_body"
                    f_on = 1
                    func_name = self.func_name()
                # ========================================================
        elif '=' in stripped or stripped.startswith(':'):
            typ = "assignment"
        else:
            typ = "top_level"
        return typ, func_name, f_on

    def classify_non_special_line(self, stripped, tokens, raw, first_token, f_on):
        """Classify token-based lines (control flow, case, commands, functions, fallback).

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, simplify, merge back, reorder conditions, or remove this method 
        without explicit user instruction.

        General Purpose:
            Handle all classification logic that occurs after the high-priority special 
            lines (shebang/comment/heredoc/blank). This is the main "else" branch of 
            stage_1_parse.

        Current Logic:
            - Build token_set (non-quoted tokens)
            - Control structures (if/while/etc.) with expanded if-elif chain
            - Case statement patterns (case_item, case_it_end, case_end)
            - Command detection (printf, info/msg, exit, etc.)
            - Logical operators → classify_and_or_logic
            - Assignment detection (with control keyword guard)
            - Function definition delegation (classify_fn_definition + _alt)
            - Body/brace fallback delegation
            - Final func_name preservation logic for lines inside functions

        Defensive Notes:
            - Exact original condition order and type priorities MUST be preserved
            - All delegated calls (classify_and_or_logic, classify_fn_definition*, 
              classify_body_brace_fallback) must remain unchanged
            - Real brace calculation stays inside the delegated methods
            - This extraction reduces stage_1_parse length while keeping the 
              battlefield-tested decision tree intact
            - Previous attempts to flatten or reorder this block caused ownership 
              and brace_level regressions
        =================================================================================
        """
        typ = "top_level"
        func_name = self.func_name()

        token_set = {t for t in tokens if not (t.startswith('"') or t.startswith("'"))}

        # ==================== Control flow (expanded) ====================
        is_if    = 'if'    in token_set
        is_then  = 'then'  in token_set
        is_else  = 'else'  in token_set
        is_elif  = 'elif'  in token_set
        is_fi    = 'fi'    in token_set

        is_while = 'while' in token_set
        is_do    = 'do'    in token_set
        is_done  = 'done'  in token_set

        if is_if and is_then:
            typ = "if-then"
        elif is_if:
            typ = "if"
        elif is_then:
            typ = "then"
        elif is_elif:
            typ = "elif"
        elif is_else:
            typ = "else"
        elif is_fi:
            typ = "fi"
        elif is_while and is_do:
            typ = "while-do"
        elif is_while:
            typ = "while"
        elif is_do:
            typ = "do"
        elif is_done:
            typ = "done"

        # ==================== Case statement handling ====================
        elif 'case' in token_set:
            typ = "variable"
        elif stripped.endswith(')') and not stripped.endswith(';;') or first_token.endswith(')'):
            typ = "case_item"
        elif stripped.endswith(';;'):
            typ = "case_it_end"
        elif 'esac' in token_set:
            typ = "case_end"

        # Command / assignment / logic
        elif any(t in token_set for t in ('printf', 'echo')):
            typ = first_token
        elif any(t in token_set for t in ('info', 'warn', 'success', 'error', 'msg', 'output_json')) and "{" not in token_set:
            typ = "command"
        elif '&&' in tokens or '||' in tokens:
            typ = self.classify_and_or_logic(tokens, stripped, raw)
        elif 'exit' in token_set and "{" not in token_set:
            typ = "exit"
        elif '=' in stripped and not any(k in token_set for k in ('if','then','else','fi','elif','while','do','done')):
            typ = "assignment"
        elif 'case' in token_set:
            typ = "variable"

        # ==================== Function definition (delegated) ====================
        elif (re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', first_token) and 
              len(tokens) > 1 and tokens[1] == '('):
            
            typ, func_name, f_on = self.classify_fn_definition(first_token, tokens)

        # Body / brace fallback
        else:
            typ, func_name, f_on = self.classify_body_brace_fallback(
                stripped, tokens, raw, f_on
            )

        # Preserve func_name for lines inside functions (except special endings)
        if typ not in ("fn_start", "fn_in_1_line", 
                      "fn_end", "brace_end", "brace_start", 
                      "case_end"):
            current = self.func_name()
            if current != "":
                func_name = current
            elif self.last_func() != "" and typ in ("blank"):
                func_name = self.last_func()
        return typ, func_name, f_on

    def stage_1_parse(self, line, tokens, indent):
        """Stage 1 Parser - Core forward classification logic.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT simplify, refactor, remove, reorder major blocks, or change type priorities
        without explicit user instruction.

        This method is the heart of the parser. All previous design decisions must be
        preserved for consistency with the entire ShellParser project.

        General Purpose:
            Perform token-based line classification and maintain real-time parser state
            (func_name, brace_level, heredoc, etc.) during the forward pass.

        Current Logic:
            - High priority handling: shebang, comments, heredoc, blank lines
            - Control structures (if/while/case) take precedence
            - Logical operators delegated to classify_and_or_logic()
            - Function definitions delegated to classify_fn_definition() / _alt()
            - Body/brace fallback with real brace counting

        EXISTING TYPES (add new ones only at the correct priority level):
            - shebang
            - comment
            - blank
            - heredoc_start / heredoc_body / heredoc_end
            - fn_start / fn_body / fn_in_1_line / fn_end
            - brace_start / brace_end
            - if / if-then / then / elif / else / fi
            - while-do / while / do / done
            - case_item / case_it_end / case_end
            - assignment
            - variable
            - and_logic / or_logic
            - printf / exit / command
            - top_level   (default fallback)

        KEY DESIGN DECISIONS TO PRESERVE:
            - Control structures (if/while/case) take precedence over fn_body
            - Braces inside quoted strings are ignored (token-based checks)
            - One-line functions correctly set last_func before reset
            - Blank lines follow the most recent function context
            - Final } of a function = fn_end (when brace_level==1)
            - esac = case_end, ;; = case_it_end, xxx) = case_item
            - Commands like msg/output_json/info are "command"
            - Assignment detection avoids control keywords

        Defensive Notes:
            - MUST use real brace calculation everywhere (no hard-coded numbers)
            - classify_and_or_logic, classify_fn_definition, and this method
              must stay perfectly aligned on brace handling
            - This is battlefield-tested logic — protect it from future simplification
        =================================================================================
        """
        raw = line
        stripped = line.strip()

        typ = "top_level"
        func_name = ""
        heredoc_d = ""
        c_on = 0
        f_on = 0
        h_on = 0

        first_token = tokens[0] if tokens else ""

        # === High priority: Special lines ===
        if self.line_num() == 1 and first_token.startswith("#!"):
            typ = "shebang"
        elif stripped.startswith("#"):
            typ = "comment"
            c_on = 1
            if self.func_name() != "":
                func_name = self.func_name()
            elif self.last_func() != "":
                func_name = ""
                self.last_func("")
        elif hasattr(self, 'heredoc_delim') and self.heredoc_delim:
            if stripped == self.heredoc_delim or stripped == self.heredoc_delim + ';':
                self.heredoc_delim = ""
                typ = "heredoc_end"
                func_name = self.func_name()
                h_on = 0
            else:
                typ = "heredoc_body"
                h_on = 1
                func_name = self.func_name()
                heredoc_d = self.heredoc_delim
        elif not tokens:                                   # blank line
            typ = "blank"
            current = self.func_name()
            last = self.last_func()
            if current != "":
                func_name = current
            elif last != "":
                func_name = last

        elif re.search(r'<<-?\s*["\']?([a-zA-Z0-9_]+)["\']?', line):
            m = re.search(r'<<-?\s*["\']?([a-zA-Z0-9_]+)["\']?', line)
            self.heredoc_delim = m.group(1)
            typ = "heredoc_start"
            h_on = 1
            func_name = self.func_name()
            heredoc_d = self.heredoc_delim
        else:
            # Non-special line classification (control flow, case, commands, functions, fallback)
            typ, func_name, f_on = self.classify_non_special_line(
                stripped, tokens, raw, first_token, f_on
            )
        # Structured array for stage2 reverse processing
        array_entry = {
            'line_num': self.line_num(),
            'type': typ,
            'func_name': func_name,
            'indent': indent,
            'brace_level': self.brace_level(),
            'stripped': stripped,
            'tokens': tokens,
            'raw': raw
        }
        self.map_array(array_entry)
        
    def stage_2_ownership(self):
        """Stage 2: Backward ownership resolution (reverse pass).

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, simplify, or merge this stage with Stage 1 or Stage 3
        without explicit user instruction.

        General Purpose:
            Fix ownership of comments, blank lines, and top-level code by walking
            the parsed lines in reverse order. This is the "correction" phase.

        Current Logic:
            - Start from the bottom with current_owner = "main-entry"
            - When meeting fn_start or fn_in_1_line → update current_owner
            - Comments and blank lines inherit the current_owner
            - Non-comment/non-blank lines with no func_name become "top-block"
            - Build map_array_for_file with corrected ownership for Stage 3

        Key Design Decisions to Preserve:
            - Reverse traversal is intentional (forward pass alone cannot know final ownership)
            - Comments and blanks follow the most recent function context
            - "top-block" is used for code outside any function
            - Shebang gets empty ownership
            - This stage makes the parser robust against real-world code layout

        Defensive Notes:
            - This is the most critical safety layer of the 3-stage design
            - Previous naive forward-only approaches failed to assign correct owners
            - Must remain a pure reverse state machine (no hard-coding, no flags)
            - Protected to prevent future AI from collapsing it into a single pass
        =================================================================================
        """
        arr = self.map_array()
        if not arr:
            return

        current_func = "main-entry"   # ← start from bottom as requested

        for i in range(len(arr)-1, -1, -1):
            item = arr[i]
            line_number = item['line_num']
            typ = item['type']
            orign_func_name = item.get('func_name','')
            indent = item['indent']
            stripped = item['stripped']
            tokens = item.get('tokens',[])
            raw = item.get('raw','')

            if not orign_func_name or orign_func_name == "":
                if typ in ("shebang"):
                    orign_func_name = ""
                    current_func = ""
                elif typ not in ("comment", "blank", "top_level"):
                    if current_func == "main-entry":
                        orign_func_name = current_func
                    else:
                        orign_func_name = "top-block"
                        current_func = "top-block"
                else:
                    orign_func_name = current_func
            else:
                current_func = orign_func_name

            # Structured array for stage3 reverse processing
            array_entry = {
                'line_num': line_number,
                'type': typ,
                'func_name': orign_func_name,
                'indent': indent,
                'stripped': stripped,
                'tokens': tokens,
                'raw': raw
            }
            self.map_array_for_file(array_entry)

        self.logger.log_message("Stage 2 reverse state machine completed", component="parser")

    def stage_3_extract_functions(self):
        """Stage 3: Function extraction and file writing.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT refactor, merge with other stages, or remove this method 
        without explicit user instruction.

        General Purpose:
            Final stage that takes the corrected ownership map from Stage 2
            and writes each function (and top-block) into its own file.

        Current Logic:
            - Uses map_array_for_file (built by Stage 2 reverse pass)
            - Groups lines by final corrected func_name
            - Preserves original raw line content and indentation
            - Writes files to target/components/<func_name>.sh
            - Also handles "top-block" for code outside any function

        Key Design Decisions to Preserve:
            - Extraction only happens AFTER Stage 2 ownership correction
            - One function per file (including top-block.sh)
            - Original source line order and whitespace are kept exactly
            - Uses _write_fn_file helper for all output

        Defensive Notes:
            - This stage is intentionally separated for clean I/O responsibility
            - Previous Grok attempts to combine stages broke ownership logic
            - Must remain the final step in the 3-stage pipeline
            - Battlefield-tested against real shell scripts with messy layouts
        =================================================================================
        """
        if not self.output_enabled():
            return

        target_dir = "target/components"
        os.makedirs(target_dir, exist_ok=True)

        arr = self.map_array_for_file()
        if not arr:
            return

        current_func = None
        func_lines = {}
        func_names_array = []
        for i in range(len(arr)-1, -1, -1):
            item = arr[i]
            typ = item['type']
            func_name = item.get('func_name', '')
            if func_name not in func_lines:
                func_lines[func_name] = []
                func_names_array.append(func_name)
            func_lines[func_name].append(item['raw'])

        for func in func_names_array:
            self._write_fn_file(target_dir, f"{func}.sh", func_lines[func])

        self.logger.log_message(f"Stage 3: Extracted functions to ./{target_dir}/", component="parser")

    def _write_fn_file(self, target_dir, filename, lines):
        """Helper to write a function (or top-block) to disk.

        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT inline, refactor, or remove this helper without explicit user instruction.

        General Purpose:
            Safely write extracted function content to target/components/<name>.sh
            while preserving original formatting and indentation.

        Current Logic:
            - Creates target directory if it doesn't exist
            - Joins lines with '\n' and adds final newline
            - Writes using UTF-8 encoding
            - Logs the result via ChronicleLogger

        Defensive Notes:
            - All file output from Stage 3 must go through this single point
            - Preserves exact original whitespace (critical for shell scripts)
            - Used by both function extraction and stage_1_report
            - Protected to ensure consistent output behavior across the project
        =================================================================================
        """
        filepath = os.path.join(target_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        self.logger.log_message(f"  → {filepath}  ({len(lines)} lines)", component="extract")

    def onTokenize(self):
        """Thin FSM hook → delegates to stage_1_parse()
        CIAO-Lite Protection Zone
        =================================================================================
        DO NOT simplify, refactor, or remove this method without explicit user instruction.
        This is the official entry point called by the StateLogic FSM.
        =================================================================================
        """
        line = self.line()                    # raw line (autostrip=False)
        tokens = self.tokenize_line(line)     # real tokens
        indent = self.calculate_indent(line)

        # Stage 1: Full classification + state updates
        self.stage_1_parse(line, tokens, indent)
        
    def stage_1_report(self):
        """Stage 1 Report"""
        if not self.output_enabled():
            return
        target_dir = "target/report"
        os.makedirs(target_dir, exist_ok=True)

        arr = self.map_array()
        if not arr:
            return

        # === Fixed-width columns: line_num | type | func_name | brace_level | stripped ===
        max_line  = max((len(str(item['line_num'])) for item in arr), default=5)
        max_type  = max((len(item['type']) for item in arr), default=18)
        max_func  = max((len(item.get('func_name', '')) for item in arr), default=25)
        max_brace = 3   # brace_level is small

        report_lines = []
        for item in arr:
            line = (
                f"{item['line_num']:>{max_line}} | "
                f"{item['type']:<{max_type}} | "
                f"{item.get('func_name',''):<{max_func}} | "
                f"{item.get('brace_level', 0):>{max_brace}} | "
                f"{item['stripped']}"
            )
            report_lines.append(line)

        self._write_fn_file(target_dir, "stage_1.txt", report_lines)

# =========================================================================
# Interactive Mode Helpers - DEFINED BEFORE interactive_mode (Critical!)
# =====================================================================
def _list_shell_scripts(folder):
    """Minimal helper - only for interactive mode"""
    candidates = []
    exclude = {'.c','.h','.txt','.md','.toml','.py','.pyc','.js','.jpeg',
                '.jpg','.png','.gif','.bak','.log'}
    for f in sorted(os.listdir(folder)):
        if f.startswith('.'): 
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext in exclude:
            continue
        if ext == '.sh' or ext == '' or ext in ('.bash','.zsh','.ksh'):
            full = os.path.join(folder, f)
            if os.path.isfile(full):
                candidates.append(full)
    return candidates


def _pick_file(candidates, label):
    """Minimal picker"""
    print(f"\n{label.capitalize()} found:")
    for i, p in enumerate(candidates, 1):
        print(f"{i:2d}. {os.path.basename(p)}")
    while True:
        sel = input(f"\nEnter number (1-{len(candidates)}): ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(candidates):
            return candidates[int(sel)-1]
        print("Invalid selection.")


def interactive_mode(logger):
    """Interactive fallback when user runs the tool with no arguments."""
    print("\n=== ShellParser Interactive Mode ===\n")
    
    print("1. split shell file")
    print("2. replace shell file")
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice in ('1', '2'):
            mode = 'split' if choice == '1' else 'replace'
            break
        print("Invalid choice. Please enter 1 or 2.")

    print(f"\nCurrent folder: {os.getcwd()}")
    folder = input("Use current folder (.) or enter path? [.] : ").strip()
    folder = folder or "."
    if not os.path.isdir(folder):
        print(f"Error: Folder '{folder}' does not exist.")
        return
    if mode == 'split':
        candidates = _list_shell_scripts(folder)
        if not candidates:
            print("No shell script candidates found.")
            return
        selected_file = _pick_file(candidates, "shell script")
        
        core = ShellParserCore(selected_file, logger)
        core.output_enabled(True)
        core.replace_mode(False)
        core.source_file(selected_file)
        core.state('backed_or_no_need')
        core.start_parse()

    else:  # replace
        comp_dir = os.path.join(folder, "target", "components")
        if not os.path.isdir(comp_dir):
            print(f"Error: target/components/ not found in '{folder}'")
            print("       Please run split first.")
            return

        comp_files = [f for f in sorted(os.listdir(comp_dir)) 
                        if f.endswith('.sh') and os.path.isfile(os.path.join(comp_dir, f))]

        if not comp_files:
            print("No function files found in target/components/")
            return

        print(f"\nAvailable function files in {comp_dir}:")
        for i, f in enumerate(comp_files, 1):
            print(f"{i:2d}. {f}")
        
        while True:
            sel = input(f"\nEnter number (1-{len(comp_files)}): ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(comp_files):
                func_name = os.path.splitext(comp_files[int(sel)-1])[0]
                break
            print("Invalid number.")

        src_candidates = _list_shell_scripts(folder)
        if src_candidates:
            src_path = _pick_file(src_candidates, "target shell script")
        else:
            src_path = input("\nEnter full path to target shell script: ").strip()
            if not os.path.isfile(src_path):
                print("File not found.")
                return

        core = ShellParserCore(src_path, logger)
        core.output_enabled(False)
        core.replace_mode(True)
        core.source_file(src_path)
        core.source_func(func_name)
        core.state('start_backup')
        core.backup_source()

    print(f"\nInteractive {mode} completed.")
# =====================================================================
    
# =============================================================================
def main():
    """ShellParser main() with single ShellParserCore call for safety.

    CIAO-Lite Protection Zone
    =================================================================================
    DO NOT refactor, simplify, remove version auditing block, duplicate core 
    instantiation, or remove without explicit user instruction.

    General Purpose:
        Use only ONE ShellParserCore instantiation for all commands to improve 
        safety and consistency.

    Current Logic:
        - Original debug/version auditing fully preserved
        - Single core = ShellParserCore(...) call
        - ChronicleLogger remains single source of truth
        - --json implies quiet

    Why we call logger.logName() and logger.baseDir() early:
        We intentionally read appname = logger.logName() and basedir = logger.baseDir()
        right after creating the logger so that the storage location (log directory, 
        target directory, backup paths, etc.) can be designed externally by 
        ChronicleLogger configuration.
        
        This allows future flexibility (different log locations per environment, 
        project-specific baseDir, etc.) without hard-coding paths inside ShellParserCore.
        It respects the anti-fragile design principle and keeps log file location 
        decision outside the parser core.

    Defensive Notes:
        - Single core call reduces risk of inconsistent logger handling
        - This change was made exactly as requested for future safety
    =================================================================================
    """
    appname = 'ShellParser'

    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 1

    logger = ChronicleLogger(logname=appname)
    appname=logger.logName()    
    basedir=logger.baseDir()
    if logger.isDebug():
        logger.log_message(f"{appname} v{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION} ({__file__}) with the following:", component="main")
        logger.log_message(f" >> {ChronicleLogger.class_version()}", component="main")
        logger.log_message(f" >> {ShellParserCore.class_version()}", component="main")

    # ==================== INTERACTIVE MODE WHEN NO COMMAND GIVEN ====================
    # CIAO-Lite: Minimal change only at entry point. Single core rule respected.
    if len(sys.argv) <= 1 or (len(sys.argv) == 2 and sys.argv[1] in ('--quiet', '--json')):
        interactive_mode(logger)
        return
    # =================================================================================

    # Subcommand parser
    parser = argparse.ArgumentParser(description="ShellParser — AI-Augmented Shell Script Component Manager")
    parser.add_argument('--quiet', action='store_true', help='Suppress non-essential output')
    parser.add_argument('--json',  action='store_true', help='Output success status in JSON')
    # Global options available to ALL subcommands (including help & about)
        
    subparsers = parser.add_subparsers(dest='command', required=True, help='Command to run')

    split_p = subparsers.add_parser('split', help='Split shell script into component functions')
    split_p.add_argument('source_file', help='Path to the shell script')

    replace_p = subparsers.add_parser('replace', help='Replace a function from target/components/')
    replace_p.add_argument('source_file', help='Path to original shell script')
    replace_p.add_argument('func_name', help='Function name to replace')

    subparsers.add_parser('about', help='Show environment & version info')
    subparsers.add_parser('help', help='Show this help')

    # Global options available to ALL subcommands (including help & about)
    for sub in [split_p, replace_p, subparsers.choices['about'], subparsers.choices['help']]:
        sub.add_argument('--quiet', action='store_true', help='Suppress non-essential output')
        sub.add_argument('--json',  action='store_true', help='Output success status in JSON')
        
    args = parser.parse_args()

    # Apply quiet/json settings
    if hasattr(args, 'quiet'):
        logger.quiet(args.quiet)
    if getattr(args, 'json', False):
        logger.quiet(True)


    # ==================== SINGLE CORE CALL ====================
    source_file = getattr(args, 'source_file', "dummy.sh")
    core = ShellParserCore(source_file, logger)

    core.is_json(getattr(args, 'json', False))

    # Output control switch
    if args.command == 'split':
        core.output_enabled(True)
        core.replace_mode(False)
        core.source_file(source_file)
        core.state('backed_or_no_need')
        core.start_parse()
    elif args.command == 'replace':
        core.output_enabled(False)   # prevent overwriting components during replace
        core.replace_mode(True)
        core.source_file(source_file)
        core.source_func(args.func_name)
        core.state('start_backup')
        core.backup_source()
    elif args.command == 'about':
        core.show_about()
    elif args.command == 'help':
        core.show_help()
    else:
        parser.print_help()
        
if __name__ == '__main__':
    main()