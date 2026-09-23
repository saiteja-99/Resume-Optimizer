"""Resume Tailoring and ATS Optimization Toolkit."""

__version__ = "0.1.0"

from resumeoptimizer.makers import ResumeMaker
from resumeoptimizer.models import (
    AnalysisResult,
    JobDescription,
    Recommendation,
    Resume,
    ScoreBreakdown,
)

__all__ = [
    "AnalysisResult",
    "JobDescription",
    "Recommendation",
    "Resume",
    "ResumeMaker",
    "ScoreBreakdown",
    "__version__",
]
