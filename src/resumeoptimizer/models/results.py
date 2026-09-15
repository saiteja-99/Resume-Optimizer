"""Data models for resume analysis results."""

from dataclasses import dataclass, field


@dataclass
class ScoreBreakdown:
    """Store individual components of an ATS score."""

    keyword_score: float = 0.0
    skill_score: float = 0.0
    semantic_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0


@dataclass
class Recommendation:
    """Represent one recommendation for improving a resume."""

    category: str
    priority: str
    message: str


@dataclass
class AnalysisResult:
    """Store the complete result of resume-job analysis."""

    score: float
    breakdown: ScoreBreakdown
    recommendations: list[Recommendation] = field(default_factory=list)
