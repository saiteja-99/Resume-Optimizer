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
        """Return an optimized version of the resume text."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job, JobDescription):
            raise TypeError("job must be a JobDescription object")

        return self.text_processor.normalize(
            resume.text,
        )
