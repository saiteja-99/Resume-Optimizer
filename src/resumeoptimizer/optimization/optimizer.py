"""Optimize resume text using verified information from the resume."""

from resumeoptimizer.models import JobDescription, Resume
from resumeoptimizer.processing import TextProcessor


class ResumeOptimizer:
    """Optimize resume text without inventing candidate information."""

    def __init__(self) -> None:
        """Initialize optimization components."""
        self.text_processor = TextProcessor()

    def optimize(
        self,
        resume: Resume,
        job: JobDescription,
    ) -> str:
        """Prioritize existing job-relevant skills in the resume."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job, JobDescription):
            raise TypeError("job must be a JobDescription object")

        text = self.text_processor.normalize(resume.text)

        if not resume.skills:
            return text

        job_skills = [
            *job.required_skills,
            *job.preferred_skills,
        ]

        if not job_skills:
            return text

        resume_skills = {skill.lower(): skill for skill in resume.skills}

        relevant_skills = []

        for job_skill in job_skills:
            skill = resume_skills.get(job_skill.lower())

            if skill and skill not in relevant_skills:
                relevant_skills.append(skill)

        remaining_skills = [
            skill for skill in resume.skills if skill not in relevant_skills
        ]

        ordered_skills = relevant_skills + remaining_skills

        return self._update_skills_section(
            text,
            ordered_skills,
        )

    def _update_skills_section(
        self,
        text: str,
        skills: list[str],
    ) -> str:
        """Update an existing skills section with the new skill order."""
        lines = text.splitlines()

        for index, line in enumerate(lines):
            heading = line.strip().lower()

            if heading in {
                "skills",
                "technical skills",
                "core skills",
                "technical expertise",
                "key skills",
            }:
                lines[index + 1 : index + 2] = [
                    ", ".join(skills),
                ]
                return "\n".join(lines)

        return text
