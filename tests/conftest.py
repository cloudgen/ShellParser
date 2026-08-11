# =============================================================================
# ShellParser pytest fixtures — isolated cwd / logger side effects
# =============================================================================
from __future__ import annotations

import os
from pathlib import Path

import pytest


FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def sample_script(tmp_path: Path) -> Path:
    """Copy the canonical fixture shell script into an isolated workdir."""
    src = (FIXTURES / "sample.sh").read_text(encoding="utf-8")
    path = tmp_path / "sample.sh"
    path.write_text(src, encoding="utf-8")
    return path


@pytest.fixture
def workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run each test with cwd = tmp_path so target/ and backups stay isolated."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def logger():
    """Quiet ChronicleLogger for tests (no console chatter)."""
    from ChronicleLogger import ChronicleLogger

    log = ChronicleLogger(logname="ShellParser-test")
    log.quiet(True)
    return log


@pytest.fixture
def make_core(logger):
    """Factory: ShellParserCore bound to a source path."""
    from ShellParser.cli import ShellParserCore

    def _factory(source_file: str | os.PathLike) -> ShellParserCore:
        core = ShellParserCore(str(source_file), logger)
        core.is_json(False)
        return core

    return _factory
