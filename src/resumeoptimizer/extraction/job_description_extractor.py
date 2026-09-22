"""Extract structured information from job descriptions."""

import re
from typing import ClassVar

from resumeoptimizer.models import JobDescription


class JobDescriptionExtractor:
    """Extract basic structured information from job descriptions."""

    REQUIRED_HEADINGS: ClassVar[set[str]] = {
        "required skills",
        "requirements",
        "required qualifications",
        "must have",
        "mandatory skills",
    }

    PREFERRED_HEADINGS: ClassVar[set[str]] = {
        "preferred skills",
        "preferred qualifications",
        "nice to have",
        "desired skills",
        "good to have",
    }

    def extract(
        self,
        text: str,
    ) -> JobDescription:
        """Extract job-description information."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        title = self._extract_title(lines)
        company = self._extract_company(lines)

        required_skills = self._extract_skill_section(
            lines,
            self.REQUIRED_HEADINGS,
        )

        preferred_skills = self._extract_skill_section(
            lines,
            self.PREFERRED_HEADINGS,
        )

        return JobDescription(
            text=text,
            title=title,
            company=company,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

    def _extract_title(self, lines: list[str]) -> str:
        """Extract the likely job title."""
        if not lines:
            return ""

        return lines[0]

    def _extract_company(self, lines: list[str]) -> str:
        """Extract the likely company name."""
        if len(lines) < 2:
            return ""

        return lines[1]

    def _extract_skill_section(
        self,
        lines: list[str],
        headings: set[str],
    ) -> list[str]:
        """Extract skills listed under matching headings."""
        skills: list[str] = []
        collecting = False

        for line in lines:
            normalized_line = self._normalize_heading(line)

            if normalized_line in headings:
                collecting = True
                continue

            if collecting and self._is_heading(line):
                break

            if collecting:
                parts = re.split(r"[,;|]", line)

                for part in parts:
                    skill = part.strip()

                    if skill and skill not in skills:
                        skills.append(skill)

        return skills

    def _normalize_heading(self, line: str) -> str:
        """Normalize a heading for comparison."""
        line = line.lower().strip()
        line = re.sub(r"[^a-z\s]", "", line)
        line = re.sub(r"\s+", " ", line)

        return line.strip()

    def _is_heading(self, line: str) -> bool:
        """Determine whether a line looks like a skill-section heading."""
        normalized = self._normalize_heading(line)

        known_headings = self.REQUIRED_HEADINGS | self.PREFERRED_HEADINGS

        return normalized in known_headings
