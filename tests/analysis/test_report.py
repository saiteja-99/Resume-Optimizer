"""Tests for Pandas analysis reports."""

import pandas as pd
import pytest

from resumeoptimizer.analysis import AnalysisReport
from resumeoptimizer.models import JobDescription, Resume


def test_create_analysis_dataframe() -> None:
    """Test creation of the analysis DataFrame."""
    resume = Resume(
        text="Python SQL Pandas Git",
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
            "ABC GmbH\n"
            "Required Skills:\n"
            "Python\n"
            "SQL\n"
            "Docker\n"
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

    report = AnalysisReport()

    dataframe = report.create_dataframe(resume, job)

    assert isinstance(dataframe, pd.DataFrame)

    assert list(dataframe["Category"]) == [
        "Required Skills",
        "Preferred Skills",
        "Keywords",
    ]


def test_required_skill_row() -> None:
    """Test required-skill statistics."""
    resume = Resume(
        text="Python SQL",
        skills=[
            "Python",
            "SQL",
        ],
    )

    job = JobDescription(
        text="Developer",
        required_skills=[
            "Python",
            "SQL",
            "Docker",
        ],
    )

    dataframe = AnalysisReport().create_dataframe(
        resume,
        job,
    )

    row = dataframe[dataframe["Category"] == "Required Skills"].iloc[0]

    assert row["Matched"] == 2
    assert row["Missing"] == 1
    assert row["Total"] == 3
    assert row["Score"] == pytest.approx(66.6666667)


def test_empty_skill_categories_receive_full_score() -> None:
    """Test skill categories with no items."""
    resume = Resume(
        text="Python",
        skills=["Python"],
    )

    job = JobDescription(
        text="",
    )

    dataframe = AnalysisReport().create_dataframe(
        resume,
        job,
    )

    skill_rows = dataframe[
        dataframe["Category"].isin(["Required Skills", "Preferred Skills"])
    ]

    for score in skill_rows["Score"]:
        assert score == 100.0


def test_invalid_resume_is_rejected() -> None:
    """Test invalid resume input."""
    job = JobDescription(
        text="Developer",
    )

    with pytest.raises(TypeError):
        AnalysisReport().create_dataframe(
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
        AnalysisReport().create_dataframe(
            resume,
            "not a job",  # type: ignore[arg-type]
        )
