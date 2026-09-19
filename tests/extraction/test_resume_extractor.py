"""Tests for resume information extraction."""

import pytest

from resumeoptimizer.extraction import ResumeExtractor


def test_extract_resume_information() -> None:
    """Test extraction of basic resume information."""
    text = """Sai Teja Edara
sai.teja@example.com
+49 123 456789

SUMMARY
Data Science student.

SKILLS
Python
SQL
Pandas
Git
"""

    sections = {
        "summary": "Data Science student.",
        "skills": "Python\nSQL\nPandas\nGit",
    }

    extractor = ResumeExtractor()

    resume = extractor.extract(text, sections)

    assert resume.name == "Sai Teja Edara"
    assert resume.email == "sai.teja@example.com"
    assert resume.phone == "+49 123 456789"
    assert resume.skills == ["Python", "SQL", "Pandas", "Git"]


def test_extract_comma_separated_skills() -> None:
    """Test extraction of comma-separated skills."""
    text = "Sai Teja Edara"

    sections = {
        "skills": "Python, SQL, Pandas, Git",
    }

    extractor = ResumeExtractor()

    resume = extractor.extract(text, sections)

    assert resume.skills == ["Python", "SQL", "Pandas", "Git"]


def test_extract_missing_information() -> None:
    """Test extraction when optional information is missing."""
    text = "Sai Teja Edara"

    sections: dict[str, str] = {}

    extractor = ResumeExtractor()

    resume = extractor.extract(text, sections)

    assert resume.name == "Sai Teja Edara"
    assert resume.email == ""
    assert resume.phone == ""
    assert resume.skills == []


def test_extract_rejects_invalid_text() -> None:
    """Test that non-string text is rejected."""
    extractor = ResumeExtractor()

    with pytest.raises(TypeError):
        extractor.extract(123, {})  # type: ignore[arg-type]


def test_extract_rejects_invalid_sections() -> None:
    """Test that non-dictionary sections are rejected."""
    extractor = ResumeExtractor()

    with pytest.raises(TypeError):
        extractor.extract("Sai Teja", [])  # type: ignore[arg-type]
