"""Calculate ATS scores from resume and job-description matches."""

import numpy as np

from resumeoptimizer.matching import KeywordMatcher, SkillMatcher
from resumeoptimizer.models import (
    AnalysisResult,
    JobDescription,
    Resume,
    ScoreBreakdown,
)


class ATSScorer:
    """Calculate a transparent ATS compatibility score."""

    WEIGHTS = np.array([0.60, 0.15, 0.25])

    def __init__(self) -> None:
        """Initialize the scoring components."""
        self.skill_matcher = SkillMatcher()
        self.keyword_matcher = KeywordMatcher()

    def score(
        self,
        resume: Resume,
        job: JobDescription,
    ) -> AnalysisResult:
        """Calculate an ATS score for a resume and job description."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job, JobDescription):
            raise TypeError("job must be a JobDescription object")

        skill_result = self.skill_matcher.match(resume, job)

        keyword_result = self.keyword_matcher.match(
            resume,
            job.text,
        )

        required_score = self._calculate_match_score(
            len(skill_result.matched_required),
            len(job.required_skills),
        )

        preferred_score = self._calculate_match_score(
            len(skill_result.matched_preferred),
            len(job.preferred_skills),
        )

        keyword_score = self._calculate_match_score(
            len(keyword_result.matched_keywords),
            len(keyword_result.matched_keywords) + len(keyword_result.missing_keywords),
        )

        components = np.array(
            [
                required_score,
                preferred_score,
                keyword_score,
            ]
        )

        overall_score = float(np.dot(components, self.WEIGHTS))

        breakdown = ScoreBreakdown(
            keyword_score=keyword_score,
            skill_score=(required_score * 0.80 + preferred_score * 0.20),
        )

        return AnalysisResult(
            score=overall_score,
            breakdown=breakdown,
        )

    def _calculate_match_score(
        self,
        matched: int,
        total: int,
    ) -> float:
        """Calculate a percentage score between 0 and 100."""
        if total == 0:
            return 100.0

        return (matched / total) * 100.0
