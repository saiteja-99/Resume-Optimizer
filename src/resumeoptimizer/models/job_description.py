"""Data model representing a job description."""

from dataclasses import dataclass, field


@dataclass
class JobDescription:
    """Represent structured information extracted from a job description."""

    text: str
    title: str = ""
    company: str = ""
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
