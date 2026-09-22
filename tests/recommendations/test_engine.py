"""Tests for the recommendation engine."""

import pytest

from resumeoptimizer.models import JobDescription, Resume
from resumeoptimizer.recommendations import RecommendationEngine


def test_missing_required_skill_creates_high_priority_recommendation() -> None:
    """Test recommendations for missing required skills."""
    resume = Resume(
        text="Python SQL",
        skills=[
            "Python",
            "SQL",
        ],
    )

    job = JobDescription(
        text="Python Developer Docker",
        required_skills=[
            "Python",
            "SQL",
            "Docker",
        ],
    )

    recommendations = RecommendationEngine().generate(
        resume,
        job,
    )

    skill_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation.category == "Skills"
    ]

    assert len(skill_recommendations) == 1

    recommendation = skill_recommendations[0]

    assert recommendation.priority == "HIGH"
    assert "Docker" in recommendation.message
    assert "genuine experience" in recommendation.message


def test_missing_preferred_skill_creates_medium_priority_recommendation() -> None:
    """Test recommendations for missing preferred skills."""
    resume = Resume(
        text="Python",
        skills=["Python"],
    )

    job = JobDescription(
        text="",
        preferred_skills=[
            "AWS",
        ],
    )

    recommendations = RecommendationEngine().generate(
        resume,
        job,
    )

    skill_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation.category == "Skills"
    ]

    assert len(skill_recommendations) == 1

    recommendation = skill_recommendations[0]

    assert recommendation.priority == "MEDIUM"
    assert "AWS" in recommendation.message


def test_missing_keyword_creates_low_priority_recommendation() -> None:
    """Test recommendations for missing keywords."""
    resume = Resume(
        text="Python developer",
        skills=["Python"],
    )

    job = JobDescription(
        text="Python developer with microservices experience",
    )

    recommendations = RecommendationEngine().generate(
        resume,
        job,
    )

    keyword_recommendations = [
        recommendation
        for recommendation in recommendations
        if recommendation.category == "Keywords"
    ]

    assert keyword_recommendations

    assert all(
        recommendation.priority == "LOW" for recommendation in keyword_recommendations
    )

    assert any(
        "microservices" in recommendation.message
        for recommendation in keyword_recommendations
    )


def test_no_missing_items_creates_info_recommendation() -> None:
    """Test the result when no missing items are found."""
    resume = Resume(
        text="Python SQL",
        skills=[
            "Python",
            "SQL",
        ],
    )

    job = JobDescription(
        text="Python SQL",
        required_skills=[
            "Python",
            "SQL",
        ],
    )

    recommendations = RecommendationEngine().generate(
        resume,
        job,
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.category == "Overall"
    assert recommendation.priority == "INFO"


def test_invalid_resume_is_rejected() -> None:
    """Test invalid resume input."""
    job = JobDescription(
        text="Python Developer",
    )

    with pytest.raises(TypeError):
        RecommendationEngine().generate(
            "not a resume",  # type: ignore[arg-type]
            job,
        )


def test_invalid_job_is_rejected() -> None:
    """Test invalid job input."""
    resume = Resume(
        text="Python",
        skills=["Python"],
    )

    with pytest.raises(TypeError):
        RecommendationEngine().generate(
            resume,
            "not a job",  # type: ignore[arg-type]
        )
