"""Tests for text processing."""

import pytest

from resumeoptimizer.processing.text_processor import TextProcessor


def test_normalize_whitespace() -> None:
    """Test that excessive whitespace is removed."""
    processor = TextProcessor()

    text = "Python     Developer\n\n\nMachine   Learning"

    result = processor.normalize(text)

    assert result == "Python Developer\nMachine Learning"


def test_normalize_windows_line_endings() -> None:
    """Test normalization of Windows line endings."""
    processor = TextProcessor()

    text = "Python Developer\r\nMachine Learning\r\nSQL"

    result = processor.normalize(text)

    assert result == "Python Developer\nMachine Learning\nSQL"


def test_normalize_rejects_non_string() -> None:
    """Test that non-string input is rejected."""
    processor = TextProcessor()

    with pytest.raises(TypeError):
        processor.normalize(123)  # type: ignore[arg-type]
