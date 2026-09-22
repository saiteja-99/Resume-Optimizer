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
