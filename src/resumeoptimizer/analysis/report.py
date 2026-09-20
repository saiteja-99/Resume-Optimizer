"""Create tabular analysis reports for resume-job matching."""

import pandas as pd

from resumeoptimizer.matching import KeywordMatcher, SkillMatcher
from resumeoptimizer.models import JobDescription, Resume


class AnalysisReport:
    """Create Pandas-based reports from resume-job matching results."""

    def __init__(self) -> None:
        """Initialize the matching components."""
        self.skill_matcher = SkillMatcher()
        self.keyword_matcher = KeywordMatcher()

    def create_dataframe(
        self,
        resume: Resume,
        job: JobDescription,
    ) -> pd.DataFrame:
        """Create a DataFrame summarizing matching results."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job, JobDescription):
            raise TypeError("job must be a JobDescription object")

        skill_result = self.skill_matcher.match(resume, job)

        keyword_result = self.keyword_matcher.match(
            resume,
            job.text,
        )

        rows = [
            self._create_row(
                "Required Skills",
                len(skill_result.matched_required),
                len(skill_result.missing_required),
            ),
            self._create_row(
                "Preferred Skills",
                len(skill_result.matched_preferred),
                len(skill_result.missing_preferred),
            ),
            self._create_row(
                "Keywords",
                len(keyword_result.matched_keywords),
                len(keyword_result.missing_keywords),
            ),
        ]

        return pd.DataFrame(rows)

    def _create_row(
        self,
        category: str,
        matched: int,
        missing: int,
    ) -> dict[str, float | int | str]:
        """Create one analysis row."""
        total = matched + missing

        if total == 0:
            score = 100.0
        else:
            score = (matched / total) * 100.0

        return {
            "Category": category,
            "Matched": matched,
            "Missing": missing,
            "Total": total,
            "Score": score,
        }
