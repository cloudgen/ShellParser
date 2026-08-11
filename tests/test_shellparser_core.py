# =============================================================================
# ShellParser core suite — TP-ID labeled cases
# Primary law: docs/requirements/* · Map: docs/reviews/test-plan.md
# =============================================================================
"""
TP catalog (executable — have):
  TP-PKG-01           package version / class_version / console / repo identity
  TP-PKG-02           shell-parser compatibility alias in pyproject
  TP-CLI-01           help --json: shellparser usage + domain verbs
  TP-CLI-02           about --quiet succeeds
  TP-OUT-01           help --json stdout is pure JSON
  TP-SHELLPARSER-01   split → target/components/*.sh
  TP-SHELLPARSER-02   split-docs markdown skeleton
  TP-SHELLPARSER-03   placeholder creates dated backup first
  TP-SHELLPARSER-04   replace preserves shebang/top-block preamble
  TP-BAK-01           replace: backup then rewrite function body
  TP-BAK-02           same-day backup counter increments
  TP-ERR-01           replace without component aborts; source unchanged

Planned (see docs/reviews/test-plan.md):
  TP-SHELLPARSER-05   empty-argv interactive Type N
  TP-ERR-02           empty parse via logger only
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "ShellParser", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )


# ---------------------------------------------------------------------------
# TP-PKG
# ---------------------------------------------------------------------------

def test_TP_PKG_01_version_alignment():
    """TP-PKG-01: __version__, core class_version, and pyproject share 1.2.1 + identity."""
    from ShellParser import __version__
    from ShellParser.cli import ShellParserCore

    assert __version__ == "1.2.1"
    assert "1.2.1" in ShellParserCore.class_version()
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "1.2.1"' in text
    assert 'shellparser = "ShellParser.cli:main"' in text
    assert "cloudgen/ShellParser" in text


def test_TP_PKG_02_console_alias():
    """TP-PKG-02: compatibility alias shell-parser is declared beside primary shellparser."""
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'shellparser = "ShellParser.cli:main"' in text
    assert 'shell-parser = "ShellParser.cli:main"' in text


# ---------------------------------------------------------------------------
# TP-CLI / TP-OUT
# ---------------------------------------------------------------------------

def test_TP_CLI_01_json_help_identity(workdir: Path, sample_script: Path):
    """TP-CLI-01: help --json usage uses primary name shellparser and lists domain verbs."""
    assert sample_script.exists()
    proc = _run_cli(["help", "--json"], cwd=workdir)
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["tool"] == "ShellParser"
    assert "shellparser" in data["usage"]
    cmds = data["commands"]
    for key in ("split", "replace", "split-docs", "placeholder", "about", "help"):
        assert key in cmds


def test_TP_CLI_02_quiet_about(workdir: Path, sample_script: Path):
    """TP-CLI-02: about --quiet completes without error."""
    proc = _run_cli(["about", "--quiet"], cwd=workdir)
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_TP_OUT_01_json_help_pure_stdout(workdir: Path, sample_script: Path):
    """TP-OUT-01: help --json stdout is pure JSON (no human prefix/suffix)."""
    proc = _run_cli(["help", "--json"], cwd=workdir)
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout.strip()
    assert out.startswith("{"), repr(out[:80])
    assert out.endswith("}"), repr(out[-80:])
    data = json.loads(out)
    assert data.get("tool") == "ShellParser"


# ---------------------------------------------------------------------------
# TP-SHELLPARSER (domain subject)
# ---------------------------------------------------------------------------

def test_TP_SHELLPARSER_01_split_writes_components(
    workdir: Path, sample_script: Path, make_core
):
    """TP-SHELLPARSER-01: split produces component files under target/components/."""
    core = make_core(sample_script)
    core.docs_mode(False)
    core.output_enabled(True)
    core.replace_mode(False)
    core.source_file(str(sample_script))
    core.state("backed_or_no_need")
    core.start_parse()

    comp = workdir / "target" / "components"
    assert comp.is_dir()
    sh_files = list(comp.glob("*.sh"))
    assert sh_files, "expected at least one component .sh"
    names = {p.stem for p in sh_files}
    assert "hello" in names or "greet" in names


def test_TP_SHELLPARSER_02_docs_markdown_skeleton(
    workdir: Path, sample_script: Path, make_core
):
    """TP-SHELLPARSER-02: split-docs emits markdown with required metadata headers."""
    core = make_core(sample_script)
    core.docs_mode(True)
    core.output_enabled(True)
    core.replace_mode(False)
    core.source_file(str(sample_script))
    core.state("backed_or_no_need")
    core.start_parse()

    docs = workdir / "target" / "docs"
    assert docs.is_dir()
    md_files = list(docs.glob("*.md"))
    assert md_files, "expected at least one .md under target/docs"
    body = md_files[0].read_text(encoding="utf-8")
    assert body.startswith("# Function:")
    assert "## Metadata" in body
    assert "- Extracted:" in body
    assert "- Source File:" in body
    assert "```sh" in body


def test_TP_SHELLPARSER_03_placeholder_backup(
    workdir: Path, sample_script: Path, make_core
):
    """TP-SHELLPARSER-03: placeholder path creates a dated backup of source."""
    original = sample_script.read_text(encoding="utf-8")
    core = make_core(sample_script)
    core.docs_mode(False)
    core.placeholder_mode(True)
    core.output_enabled(True)
    core.replace_mode(False)
    core.source_file(str(sample_script))
    core.state("start_backup")
    core.backup_source()

    backups = list(workdir.glob("sample.sh.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*"))
    assert backups, "placeholder must backup source first"
    assert backups[0].read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# TP-BAK / TP-ERR
# ---------------------------------------------------------------------------

def test_TP_BAK_01_replace_backup_then_rewrite(
    workdir: Path, sample_script: Path, make_core
):
    """TP-BAK-01: replace creates basename.YYYYMMDD-N backup and rewrites function."""
    core = make_core(sample_script)
    core.docs_mode(False)
    core.output_enabled(True)
    core.replace_mode(False)
    core.source_file(str(sample_script))
    core.state("backed_or_no_need")
    core.start_parse()

    hello_comp = workdir / "target" / "components" / "hello.sh"
    assert hello_comp.exists(), list((workdir / "target" / "components").iterdir())
    edited = "hello() {\n    echo \"hello from test\"\n}\n"
    hello_comp.write_text(edited, encoding="utf-8")

    original = sample_script.read_text(encoding="utf-8")

    core2 = make_core(sample_script)
    core2.output_enabled(False)
    core2.replace_mode(True)
    core2.source_file(str(sample_script))
    core2.source_func("hello")
    core2.state("start_backup")
    core2.backup_source()

    backups = list(workdir.glob("sample.sh.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*"))
    assert backups, f"expected dated backup beside source; cwd files={list(workdir.iterdir())}"
    assert backups[0].read_text(encoding="utf-8") == original

    updated = sample_script.read_text(encoding="utf-8")
    assert "hello from test" in updated
    assert updated != original
    # Shebang/preamble must survive replace (paired with TP-SHELLPARSER-04)
    assert updated.startswith("#!/bin/sh")


def test_TP_SHELLPARSER_04_replace_preserves_top_block(
    workdir: Path, sample_script: Path, make_core
):
    """TP-SHELLPARSER-04: replace rewrites only named function; shebang/top-block remain."""
    core = make_core(sample_script)
    core.docs_mode(False)
    core.output_enabled(True)
    core.replace_mode(False)
    core.source_file(str(sample_script))
    core.state("backed_or_no_need")
    core.start_parse()

    # Components: hello must NOT include shebang
    hello_comp = workdir / "target" / "components" / "hello.sh"
    top_comp = workdir / "target" / "components" / "top-block.sh"
    assert hello_comp.exists()
    assert top_comp.exists()
    assert "#!/bin/sh" not in hello_comp.read_text(encoding="utf-8")
    assert "#!/bin/sh" in top_comp.read_text(encoding="utf-8")

    hello_comp.write_text('hello() {\n    echo "only hello changed"\n}\n', encoding="utf-8")

    core2 = make_core(sample_script)
    core2.output_enabled(False)
    core2.replace_mode(True)
    core2.source_file(str(sample_script))
    core2.source_func("hello")
    core2.state("start_backup")
    core2.backup_source()

    text = sample_script.read_text(encoding="utf-8")
    assert text.startswith("#!/bin/sh")
    assert "# Fixture shell script for ShellParser TP suite" in text
    assert "only hello changed" in text
    assert "greet()" in text
    assert "double_line()" in text


def test_TP_BAK_02_same_day_counter(workdir: Path, sample_script: Path, make_core):
    """TP-BAK-02: second same-day backup uses next N without clobbering first."""
    core = make_core(sample_script)
    core.docs_mode(False)
    core.output_enabled(True)
    core.replace_mode(False)
    core.source_file(str(sample_script))
    core.state("backed_or_no_need")
    core.start_parse()

    hello = workdir / "target" / "components" / "hello.sh"
    hello.write_text('hello() {\n    echo "v1"\n}\n', encoding="utf-8")

    core2 = make_core(sample_script)
    core2.output_enabled(False)
    core2.replace_mode(True)
    core2.source_file(str(sample_script))
    core2.source_func("hello")
    core2.state("start_backup")
    core2.backup_source()

    hello.write_text('hello() {\n    echo "v2"\n}\n', encoding="utf-8")
    core3 = make_core(sample_script)
    core3.output_enabled(False)
    core3.replace_mode(True)
    core3.source_file(str(sample_script))
    core3.source_func("hello")
    core3.state("start_backup")
    core3.backup_source()

    backups = sorted(workdir.glob("sample.sh.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*"))
    assert len(backups) >= 2, backups
    names = [p.name for p in backups]
    assert any(n.endswith("-1") for n in names), names
    assert any(n.endswith("-2") for n in names), names
    # First backup must still exist and not be overwritten empty
    assert backups[0].stat().st_size > 0


def test_TP_ERR_01_replace_missing_component(
    workdir: Path, sample_script: Path, make_core, capsys
):
    """TP-ERR-01: replace without component aborts; source unchanged."""
    original = sample_script.read_text(encoding="utf-8")
    core = make_core(sample_script)
    core.output_enabled(False)
    core.replace_mode(True)
    core.source_file(str(sample_script))
    core.source_func("no_such_function_xyz")
    core.state("backed_or_no_need")
    core.start_parse()
    ok = core.replace_function()
    assert ok is False
    assert sample_script.read_text(encoding="utf-8") == original
    out = capsys.readouterr()
    assert "Error: No parsed data available" not in out.out
