"""Match resume skills against job-description skills."""

import re

from resumeoptimizer.models import JobDescription, Resume, SkillMatchResult


class SkillMatcher:
    """Compare skills from a resume with skills from a job description."""

    def match(
        self,
        resume: Resume,
        job: JobDescription,
    ) -> SkillMatchResult:
        """Match required and preferred job skills against resume skills."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job, JobDescription):
            raise TypeError("job must be a JobDescription object")

        resume_skills = self._normalize_skills(resume.skills)

        matched_required, missing_required = self._match_skills(
            job.required_skills,
            resume_skills,
        )

        matched_preferred, missing_preferred = self._match_skills(
            job.preferred_skills,
            resume_skills,
        )

        return SkillMatchResult(
            matched_required=matched_required,
            missing_required=missing_required,
            matched_preferred=matched_preferred,
            missing_preferred=missing_preferred,
        )

    def _normalize_skills(
        self,
        skills: list[str],
    ) -> dict[str, str]:
        """Normalize skills while preserving their original names."""
        normalized: dict[str, str] = {}

        for skill in skills:
            normalized_skill = self._normalize_skill(skill)

            if normalized_skill:
                normalized[normalized_skill] = skill.strip()

        return normalized

    def _match_skills(
        self,
        job_skills: list[str],
        resume_skills: dict[str, str],
    ) -> tuple[list[str], list[str]]:
        """Return matched and missing skills."""
        matched: list[str] = []
        missing: list[str] = []

        for skill in job_skills:
            normalized_skill = self._normalize_skill(skill)

            if not normalized_skill:
                continue

            if normalized_skill in resume_skills:
                matched.append(skill)
            else:
                missing.append(skill)

        return matched, missing

    def _normalize_skill(self, skill: str) -> str:
        """Normalize a skill for case-insensitive comparison."""
        skill = skill.lower().strip()
        skill = re.sub(r"[^a-z0-9+#.\s-]", "", skill)
        skill = re.sub(r"\s+", " ", skill)

        return skill.strip()
