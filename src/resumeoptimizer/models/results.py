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
class SkillMatchResult:
    """Store the result of resume and job-description skill matching."""

    matched_required: list[str] = field(default_factory=list)
    missing_required: list[str] = field(default_factory=list)
    matched_preferred: list[str] = field(default_factory=list)
    missing_preferred: list[str] = field(default_factory=list)


@dataclass
class KeywordMatchResult:
    """Store the result of resume and job-description keyword matching."""

    matched_keywords: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """Store the complete result of resume-job analysis."""

    score: float
    breakdown: ScoreBreakdown
    recommendations: list[Recommendation] = field(default_factory=list)
