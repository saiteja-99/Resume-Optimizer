"""Tests for resume optimization."""

import pytest

from resumeoptimizer.models import JobDescription, Resume
from resumeoptimizer.optimization import ResumeOptimizer


def test_optimizer_normalizes_resume_text() -> None:
    """Test basic safe resume normalization."""
    resume = Resume(
        text=("John Doe\r\n\r\nPython    SQL\r\nDeveloper"),
    )

    job = JobDescription(
        text="Python Developer",
    )

    optimized = ResumeOptimizer().optimize(
        resume,
        job,
    )

    assert optimized == ("John Doe\nPython SQL\nDeveloper")


def test_optimizer_does_not_add_missing_skills() -> None:
    """Test that optimization does not fabricate skills."""
    resume = Resume(
        text="Python developer",
        skills=["Python"],
    )

    job = JobDescription(
        text="Python Developer with AWS",
        required_skills=[
            "Python",
            "AWS",
        ],
    )

    optimized = ResumeOptimizer().optimize(
        resume,
        job,
    )

    assert "Python" in optimized
    assert "AWS" not in optimized


def test_invalid_resume_is_rejected() -> None:
    """Test invalid resume input."""
    job = JobDescription(
        text="Python Developer",
    )

    with pytest.raises(TypeError):
        ResumeOptimizer().optimize(
            "not a resume",  # type: ignore[arg-type]
            job,
        )


def test_invalid_job_is_rejected() -> None:
    """Test invalid job input."""
    resume = Resume(
        text="Python developer",
    )

    with pytest.raises(TypeError):
        ResumeOptimizer().optimize(
            resume,
            "not a job",  # type: ignore[arg-type]
        )


def test_optimizer_prioritizes_job_relevant_existing_skills() -> None:
    """Test that matching skills are moved to the front."""
    resume = Resume(
        text=("John Doe\nSkills\nGit, Python, SQL, Machine Learning\n"),
        skills=[
            "Git",
            "Python",
            "SQL",
            "Machine Learning",
        ],
    )

    job = JobDescription(
        text="AI/ML Engineer",
        required_skills=[
            "Python",
            "Machine Learning",
            "SQL",
        ],
        preferred_skills=[
            "Git",
        ],
    )

    optimized = ResumeOptimizer().optimize(
        resume,
        job,
    )

    assert "Skills\nPython, Machine Learning, SQL, Git" in optimized


def test_optimizer_does_not_add_missing_job_skills() -> None:
    """Test that missing job skills are never added."""
    resume = Resume(
        text=("John Doe\nSkills\nPython, SQL\n"),
        skills=[
            "Python",
            "SQL",
        ],
    )

    job = JobDescription(
        text="AI/ML Engineer",
        required_skills=[
            "Python",
            "AWS",
        ],
        preferred_skills=[
            "Docker",
        ],
    )

    optimized = ResumeOptimizer().optimize(
        resume,
        job,
    )

    assert "Python, SQL" in optimized
    assert "AWS" not in optimized
    assert "Docker" not in optimized
