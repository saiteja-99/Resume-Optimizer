"""Tests for the text document parser."""

from pathlib import Path

import pytest

from resumeoptimizer.parsers import TextParser


def test_text_parser_reads_file(tmp_path: Path) -> None:
    """Test that TextParser reads a UTF-8 text file."""
    file_path = tmp_path / "resume.txt"
    file_path.write_text("Python Developer\nMachine Learning", encoding="utf-8")

    parser = TextParser()

    result = parser.parse(file_path)

    assert result == "Python Developer\nMachine Learning"


def test_text_parser_missing_file() -> None:
    """Test that TextParser raises an error for a missing file."""
    parser = TextParser()

    with pytest.raises(FileNotFoundError):
        parser.parse("missing_resume.txt")
