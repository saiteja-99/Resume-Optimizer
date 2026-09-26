"""Generate recommendations for improving resume-job alignment."""

import re
from typing import ClassVar

from resumeoptimizer.matching import KeywordMatcher, SkillMatcher
from resumeoptimizer.models import (
    JobDescription,
    Recommendation,
    Resume,
)


class RecommendationEngine:
    """Generate transparent recommendations from resume-job matches."""

    GENERIC_KEYWORDS: ClassVar[set[str]] = {
        "developer",
        "engineer",
        "scientist",
        "manager",
        "analyst",
        "specialist",
        "professional",
        "experience",
        "work",
        "job",
        "role",
        "team",
        "company",
        "gmbh",
    }

    JOB_SECTION_KEYWORDS: ClassVar[set[str]] = {
        "required",
        "requirements",
        "preferred",
        "qualifications",
        "skills",
        "skill",
        "mandatory",
        "desired",
    }

    def __init__(self) -> None:
        """Initialize the matching components."""
        self.skill_matcher = SkillMatcher()
        self.keyword_matcher = KeywordMatcher()

    def generate(
        self,
        resume: Resume,
        job: JobDescription,
    ) -> list[Recommendation]:
        """Generate recommendations based on matching results."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job, JobDescription):
            raise TypeError("job must be a JobDescription object")

        skill_result = self.skill_matcher.match(
            resume,
            job,
        )

        keyword_result = self.keyword_matcher.match(
            resume,
            job.text,
        )

        recommendations: list[Recommendation] = []

        recommendations.extend(
            self._create_skill_recommendations(
                skill_result.missing_required,
                "HIGH",
                "Required",
            )
        )

        recommendations.extend(
            self._create_skill_recommendations(
                skill_result.missing_preferred,
                "MEDIUM",
                "Preferred",
            )
        )

        recommendations.extend(
            self._create_keyword_recommendations(
                keyword_result.missing_keywords,
                job,
            )
        )

        if not recommendations:
            recommendations.append(
                Recommendation(
                    category="Overall",
                    priority="INFO",
                    message=(
                        "No missing required skills, preferred skills, "
                        "or keywords were identified."
                    ),
                )
            )

        return recommendations

    def _create_skill_recommendations(
        self,
        skills: list[str],
        priority: str,
        skill_type: str,
    ) -> list[Recommendation]:
        """Create recommendations for missing skills."""
        recommendations: list[Recommendation] = []

        for skill in skills:
            recommendations.append(
                Recommendation(
                    category="Skills",
                    priority=priority,
                    message=(
                        f"{skill_type} skill '{skill}' is missing from "
                        "the resume. Add it only if you have genuine "
                        f"experience with {skill}."
                    ),
                )
            )

        return recommendations

    def _create_keyword_recommendations(
        self,
        keywords: list[str],
        job: JobDescription,
    ) -> list[Recommendation]:
        """Create recommendations for meaningful missing keywords."""
        recommendations: list[Recommendation] = []

        excluded_keywords = self._get_excluded_keywords(job)

        for keyword in keywords:
            if keyword in excluded_keywords:
                continue

            recommendations.append(
                Recommendation(
                    category="Keywords",
                    priority="LOW",
                    message=(
                        f"Consider mentioning the keyword '{keyword}' "
                        "in a relevant section if it accurately "
                        "describes your experience."
                    ),
                )
            )

        return recommendations

    def _get_excluded_keywords(
        self,
        job: JobDescription,
    ) -> set[str]:
        """Return keywords that should not create recommendations."""
        excluded = set(self.GENERIC_KEYWORDS)
        excluded.update(self.JOB_SECTION_KEYWORDS)

        title_words = re.findall(
            r"[a-zA-Z0-9+#.-]+",
            job.title.lower(),
        )

        excluded.update(word.strip("-. ") for word in title_words)

        company_words = re.findall(
            r"[a-zA-Z0-9+#.-]+",
            job.company.lower(),
        )

        excluded.update(word.strip("-. ") for word in company_words)

        skill_words = re.findall(
            r"[a-zA-Z0-9+#.-]+",
            " ".join(job.required_skills + job.preferred_skills).lower(),
        )

        excluded.update(word.strip("-. ") for word in skill_words)

        return excluded
