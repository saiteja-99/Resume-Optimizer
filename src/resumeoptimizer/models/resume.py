"""Data model representing a parsed resume."""

from dataclasses import dataclass, field


@dataclass
class Resume:
    """Represent the structured information extracted from a resume."""

    text: str
    name: str = ""
    email: str = ""
    phone: str = ""
    skills: list[str] = field(default_factory=list)
