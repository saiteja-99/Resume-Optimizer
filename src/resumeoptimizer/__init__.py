"""Main public interface for Resume Optimizer."""

__version__ = "0.1.0"

from resumeoptimizer.analysis import AnalysisReport
from resumeoptimizer.makers import ResumeMaker
from resumeoptimizer.matching import KeywordMatcher, SkillMatcher
from resumeoptimizer.models import (
    AnalysisResult,
    JobDescription,
    Recommendation,
    Resume,
    ScoreBreakdown,
)
from resumeoptimizer.optimization import ResumeOptimizer
from resumeoptimizer.parsers import DocumentLoader
from resumeoptimizer.recommendations import RecommendationEngine
from resumeoptimizer.scoring import ATSScorer

__all__ = [
    "ATSScorer",
    "AnalysisReport",
    "AnalysisResult",
    "DocumentLoader",
    "JobDescription",
    "KeywordMatcher",
    "Recommendation",
    "RecommendationEngine",
    "Resume",
    "ResumeMaker",
    "ResumeOptimizer",
    "ScoreBreakdown",
    "SkillMatcher",
    "__version__",
]
