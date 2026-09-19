"""Detect common resume sections."""

import re
from typing import ClassVar


class SectionDetector:
    """Detect and extract common sections from resume text."""

    SECTION_ALIASES: ClassVar[dict[str, set[str]]] = {
        "summary": {
            "summary",
            "profile",
            "professional summary",
            "objective",
            "career objective",
        },
        "skills": {
            "skills",
            "technical skills",
            "core skills",
            "technical expertise",
            "key skills",
        },
        "experience": {
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "work history",
        },
        "education": {
            "education",
            "academic background",
            "academic qualifications",
        },
        "projects": {
            "projects",
            "personal projects",
            "academic projects",
            "key projects",
        },
        "certifications": {
            "certifications",
            "certificates",
            "professional certifications",
        },
    }

    def detect(self, text: str) -> dict[str, str]:
        """Detect common sections and return their content."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        lines = text.splitlines()

        sections: dict[str, list[str]] = {}
        current_section: str | None = None

        for line in lines:
            normalized_line = self._normalize_heading(line)

            section_name = self._find_section(normalized_line)

            if section_name is not None:
                current_section = section_name
                sections.setdefault(current_section, [])
                continue

            if current_section is not None:
                sections[current_section].append(line)

        return {
            section: "\n".join(content).strip() for section, content in sections.items()
        }

    def _normalize_heading(self, line: str) -> str:
        """Normalize a possible section heading."""
        line = line.strip().lower()
        line = re.sub(r"[^a-z\s]", "", line)
        line = re.sub(r"\s+", " ", line)

        return line.strip()

    def _find_section(self, heading: str) -> str | None:
        """Find the canonical section name for a heading."""
        for section_name, aliases in self.SECTION_ALIASES.items():
            if heading in aliases:
                return section_name

        return None
