"""Tests for skill matching."""

import pytest

from resumeoptimizer.matching import SkillMatcher
from resumeoptimizer.models import JobDescription, Resume


def test_match_required_and_preferred_skills() -> None:
    """Test matching resume skills against job skills."""
    resume = Resume(
        text="Python SQL Pandas Git",
        skills=["Python", "SQL", "Pandas", "Git"],
    )

    job = JobDescription(
        text="Python Developer",
        required_skills=["Python", "SQL", "Docker"],
        preferred_skills=["Pandas", "AWS"],
    )

    matcher = SkillMatcher()

    result = matcher.match(resume, job)

    assert result.matched_required == [
        "Python",
        "SQL",
    ]

    assert result.missing_required == [
        "Docker",
    ]

    assert result.matched_preferred == [
        "Pandas",
    ]

    assert result.missing_preferred == [
        "AWS",
    ]


def test_matching_is_case_insensitive() -> None:
    """Test that skill matching ignores letter case."""
    resume = Resume(
        text="python sql",
        skills=["python", "sql"],
    )

    job = JobDescription(
        text="Data Analyst",
        required_skills=["Python", "SQL"],
    )

    matcher = SkillMatcher()

    result = matcher.match(resume, job)

    assert result.matched_required == [
        "Python",
        "SQL",
    ]

    assert result.missing_required == []


def test_no_matching_skills() -> None:
    """Test when none of the required skills are present."""
    resume = Resume(
        text="Java C#",
        skills=["Java", "C#"],
    )

    job = JobDescription(
        text="Python Developer",
        required_skills=["Python", "SQL"],
    )

    matcher = SkillMatcher()

    result = matcher.match(resume, job)

    assert result.matched_required == []

    assert result.missing_required == [
        "Python",
        "SQL",
    ]


def test_empty_job_skills() -> None:
    """Test when the job has no listed skills."""
    resume = Resume(
        text="Python",
        skills=["Python"],
    )

    job = JobDescription(
        text="Developer",
    )

    matcher = SkillMatcher()

    result = matcher.match(resume, job)

    assert result.matched_required == []
    assert result.missing_required == []
    assert result.matched_preferred == []
    assert result.missing_preferred == []


def test_match_rejects_invalid_resume() -> None:
    """Test that invalid resume input is rejected."""
    matcher = SkillMatcher()

    job = JobDescription(text="Developer")

    with pytest.raises(TypeError):
        matcher.match("not a resume", job)  # type: ignore[arg-type]


def test_match_rejects_invalid_job() -> None:
    """Test that invalid job input is rejected."""
    matcher = SkillMatcher()

    resume = Resume(text="Python", skills=["Python"])

    with pytest.raises(TypeError):
        matcher.match(resume, "not a job")  # type: ignore[arg-type]
