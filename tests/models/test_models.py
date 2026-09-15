"""Tests for Resume Optimizer data models."""

from resumeoptimizer import (
    AnalysisResult,
    JobDescription,
    Recommendation,
    Resume,
    ScoreBreakdown,
)


def test_resume_creation() -> None:
    """Test creation of a Resume object."""
    resume = Resume(
        text="Python developer with machine learning experience.",
        name="Sai Teja",
        skills=["Python", "Machine Learning"],
    )

    assert resume.name == "Sai Teja"
    assert "Python" in resume.skills


def test_job_description_creation() -> None:
    """Test creation of a JobDescription object."""
    job = JobDescription(
        text="Looking for a Python developer.",
        title="Python Developer",
        required_skills=["Python"],
    )

    assert job.title == "Python Developer"
    assert "Python" in job.required_skills


def test_analysis_result_creation() -> None:
    """Test creation of an analysis result."""
    breakdown = ScoreBreakdown(
        keyword_score=80.0,
        skill_score=75.0,
    )

    recommendation = Recommendation(
        category="missing_skill",
        priority="high",
        message="Consider adding a relevant skill if you have it.",
    )

    result = AnalysisResult(
        score=77.5,
        breakdown=breakdown,
        recommendations=[recommendation],
    )

    assert result.score == 77.5
    assert result.breakdown.keyword_score == 80.0
    assert len(result.recommendations) == 1
