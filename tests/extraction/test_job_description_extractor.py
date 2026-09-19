"""Tests for job-description extraction."""

import pytest

from resumeoptimizer.extraction import JobDescriptionExtractor


def test_extract_job_description() -> None:
    """Test extraction of job-description information."""
    text = """Python Developer
ABC GmbH

We are looking for a Python developer.

Required Skills:
Python
SQL
Git
Pandas

Preferred Skills:
Docker
AWS
Linux
"""

    extractor = JobDescriptionExtractor()

    job = extractor.extract(text)

    assert job.title == "Python Developer"
    assert job.company == "ABC GmbH"

    assert job.required_skills == [
        "Python",
        "SQL",
        "Git",
        "Pandas",
    ]

    assert job.preferred_skills == [
        "Docker",
        "AWS",
        "Linux",
    ]


def test_extract_comma_separated_skills() -> None:
    """Test extraction of comma-separated skills."""
    text = """Data Analyst
Example Company

Required Skills:
Python, SQL, Pandas

Preferred Skills:
Power BI, Tableau
"""

    extractor = JobDescriptionExtractor()

    job = extractor.extract(text)

    assert job.required_skills == [
        "Python",
        "SQL",
        "Pandas",
    ]

    assert job.preferred_skills == [
        "Power BI",
        "Tableau",
    ]


def test_extract_missing_sections() -> None:
    """Test extraction when skill sections are missing."""
    text = """Python Developer
ABC GmbH

We are looking for a Python developer.
"""

    extractor = JobDescriptionExtractor()

    job = extractor.extract(text)

    assert job.title == "Python Developer"
    assert job.company == "ABC GmbH"
    assert job.required_skills == []
    assert job.preferred_skills == []


def test_extract_rejects_non_string() -> None:
    """Test that non-string input is rejected."""
    extractor = JobDescriptionExtractor()

    with pytest.raises(TypeError):
        extractor.extract(123)  # type: ignore[arg-type]
