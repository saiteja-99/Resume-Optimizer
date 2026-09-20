"""Tests for ATS scoring."""

import pytest

from resumeoptimizer.models import JobDescription, Resume
from resumeoptimizer.scoring import ATSScorer


def test_calculate_ats_score() -> None:
    """Test ATS score calculation."""
    resume = Resume(
        text=("Python SQL Pandas Git developer with data analysis experience."),
        skills=[
            "Python",
            "SQL",
            "Pandas",
            "Git",
        ],
    )

    job = JobDescription(
        text=(
            "Python Developer\n"
            "ABC GmbH\n\n"
            "Required Skills:\n"
            "Python\n"
            "SQL\n"
            "Docker\n\n"
            "Preferred Skills:\n"
            "Pandas\n"
            "AWS"
        ),
        required_skills=[
            "Python",
            "SQL",
            "Docker",
        ],
        preferred_skills=[
            "Pandas",
            "AWS",
        ],
    )

    scorer = ATSScorer()

    result = scorer.score(resume, job)

    assert 0 <= result.score <= 100
    assert result.breakdown.skill_score > 0
    assert result.breakdown.keyword_score > 0


def test_perfect_match() -> None:
    """Test that a complete match produces 100."""
    resume = Resume(
        text="Python SQL Docker Pandas AWS developer",
        skills=[
            "Python",
            "SQL",
            "Docker",
            "Pandas",
            "AWS",
        ],
    )

    job = JobDescription(
        text="Python developer with SQL Docker Pandas AWS",
        required_skills=[
            "Python",
            "SQL",
            "Docker",
        ],
        preferred_skills=[
            "Pandas",
            "AWS",
        ],
    )

    scorer = ATSScorer()

    result = scorer.score(resume, job)

    assert result.score == pytest.approx(100.0)


def test_no_required_skills() -> None:
    """Test scoring when the job has no required skills."""
    resume = Resume(
        text="Python developer",
        skills=["Python"],
    )

    job = JobDescription(
        text="Developer",
    )

    scorer = ATSScorer()

    result = scorer.score(resume, job)

    assert 0 <= result.score <= 100


def test_invalid_resume() -> None:
    """Test that invalid resume input is rejected."""
    scorer = ATSScorer()

    job = JobDescription(
        text="Python Developer",
    )

    with pytest.raises(TypeError):
        scorer.score("not a resume", job)  # type: ignore[arg-type]


def test_invalid_job() -> None:
    """Test that invalid job input is rejected."""
    scorer = ATSScorer()

    resume = Resume(
        text="Python",
        skills=["Python"],
    )

    with pytest.raises(TypeError):
        scorer.score(resume, "not a job")  # type: ignore[arg-type]
