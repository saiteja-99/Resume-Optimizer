"""Tests for keyword matching."""

import pytest

from resumeoptimizer.matching import KeywordMatcher
from resumeoptimizer.models import Resume


def test_match_keywords() -> None:
    """Test matching important job keywords against a resume."""
    resume = Resume(
        text=(
            "Software Engineer with Python and SQL experience. "
            "Worked on data analysis projects."
        ),
    )

    job_text = (
        "Python developer with SQL experience in data analysis and machine learning."
    )

    matcher = KeywordMatcher()

    result = matcher.match(resume, job_text)

    assert "python" in result.matched_keywords
    assert "sql" in result.matched_keywords
    assert "data" in result.matched_keywords
    assert "analysis" in result.matched_keywords

    assert "machine" in result.missing_keywords
    assert "learning" in result.missing_keywords


def test_keyword_matching_is_case_insensitive() -> None:
    """Test that keyword matching ignores letter case."""
    resume = Resume(
        text="PYTHON SQL",
    )

    job_text = "python sql"

    matcher = KeywordMatcher()

    result = matcher.match(resume, job_text)

    assert result.matched_keywords == [
        "python",
        "sql",
    ]

    assert result.missing_keywords == []


def test_stopwords_are_removed() -> None:
    """Test that common stopwords are not returned."""
    resume = Resume(
        text="Python developer",
    )

    job_text = "We are looking for a Python developer"

    matcher = KeywordMatcher()

    result = matcher.match(resume, job_text)

    assert "we" not in result.matched_keywords
    assert "are" not in result.matched_keywords
    assert "for" not in result.matched_keywords
    assert "a" not in result.matched_keywords

    assert "python" in result.matched_keywords
    assert "developer" in result.matched_keywords


def test_empty_job_description() -> None:
    """Test matching with an empty job description."""
    resume = Resume(
        text="Python SQL",
    )

    matcher = KeywordMatcher()

    result = matcher.match(resume, "")

    assert result.matched_keywords == []
    assert result.missing_keywords == []


def test_invalid_resume_is_rejected() -> None:
    """Test that invalid resume input is rejected."""
    matcher = KeywordMatcher()

    with pytest.raises(TypeError):
        matcher.match("not a resume", "Python developer")  # type: ignore[arg-type]


def test_invalid_job_text_is_rejected() -> None:
    """Test that invalid job text is rejected."""
    matcher = KeywordMatcher()

    resume = Resume(
        text="Python",
    )

    with pytest.raises(TypeError):
        matcher.match(resume, 123)  # type: ignore[arg-type]
