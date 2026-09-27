"""Tests for the Resume Optimizer package."""

from resumeoptimizer import (
    AnalysisReport,
    AnalysisResult,
    ATSScorer,
    DocumentLoader,
    JobDescription,
    KeywordMatcher,
    Recommendation,
    RecommendationEngine,
    Resume,
    ResumeMaker,
    ResumeOptimizer,
    ScoreBreakdown,
    SkillMatcher,
    __version__,
)


def test_package_version() -> None:
    """Verify that the package exposes a version."""
    assert __version__ == "0.1.0"


def test_public_api_exports() -> None:
    """Verify that the main package components are publicly available."""
    assert AnalysisReport is not None
    assert AnalysisResult is not None
    assert ATSScorer is not None
    assert DocumentLoader is not None
    assert JobDescription is not None
    assert KeywordMatcher is not None
    assert Recommendation is not None
    assert RecommendationEngine is not None
    assert Resume is not None
    assert ResumeMaker is not None
    assert ResumeOptimizer is not None
    assert ScoreBreakdown is not None
    assert SkillMatcher is not None
