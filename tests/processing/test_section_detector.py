"""Tests for resume section detection."""

import pytest

from resumeoptimizer.processing.section_detector import SectionDetector


def test_detect_common_sections() -> None:
    """Test detection of common resume sections."""
    text = """SUMMARY
Data Science student with Python experience.

SKILLS
Python
SQL
Machine Learning

EXPERIENCE
Software Engineer
GP InfoTech

EDUCATION
MSc Data Science
TU Dortmund University
"""

    detector = SectionDetector()

    result = detector.detect(text)

    assert "summary" in result
    assert "skills" in result
    assert "experience" in result
    assert "education" in result

    assert "Python" in result["skills"]
    assert "GP InfoTech" in result["experience"]


def test_detect_section_aliases() -> None:
    """Test that alternative headings map to canonical sections."""
    text = """PROFESSIONAL SUMMARY
Python developer.

TECHNICAL SKILLS
Python
Pandas

WORK EXPERIENCE
Software Engineer
"""

    detector = SectionDetector()

    result = detector.detect(text)

    assert "summary" in result
    assert "skills" in result
    assert "experience" in result


def test_detect_ignores_unknown_headings() -> None:
    """Test that unknown headings do not create sections."""
    text = """ABOUT ME
Some personal information.

SKILLS
Python
SQL
"""

    detector = SectionDetector()

    result = detector.detect(text)

    assert "skills" in result
    assert "about me" not in result


def test_detect_rejects_non_string() -> None:
    """Test that non-string input is rejected."""
    detector = SectionDetector()

    with pytest.raises(TypeError):
        detector.detect(123)  # type: ignore[arg-type]
