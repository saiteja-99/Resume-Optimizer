"""Tests for the unified document loader."""

from pathlib import Path

import pytest

from resumeoptimizer.parsers import DocumentLoader


def test_loader_detects_text_file(tmp_path: Path) -> None:
    """Test that the loader selects the text parser."""
    file_path = tmp_path / "resume.txt"
    file_path.write_text(
        "Python Developer\nMachine Learning",
        encoding="utf-8",
    )

    loader = DocumentLoader()

    result = loader.load(file_path)

    assert "Python Developer" in result
    assert "Machine Learning" in result


def test_loader_rejects_unsupported_format(tmp_path: Path) -> None:
    """Test that unsupported file formats are rejected."""
    file_path = tmp_path / "resume.csv"
    file_path.write_text("name,skill", encoding="utf-8")

    loader = DocumentLoader()

    with pytest.raises(ValueError, match="Unsupported document format"):
        loader.load(file_path)


def test_loader_rejects_missing_file() -> None:
    """Test that missing files are rejected."""
    loader = DocumentLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("missing_resume.pdf")
