"""Extract structured information from resume text."""

import re

from resumeoptimizer.models import Resume


class ResumeExtractor:
    """Extract basic structured information from resume text."""

    def extract(
        self,
        text: str,
        sections: dict[str, str],
    ) -> Resume:
        """Extract resume information and return a Resume object."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if not isinstance(sections, dict):
            raise TypeError("sections must be a dictionary")

        name = self._extract_name(text)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        skills = self._extract_skills(sections)

        return Resume(
            text=text,
            name=name,
            email=email,
            phone=phone,
            skills=skills,
        )

    def _extract_name(self, text: str) -> str:
        """Extract a likely name from the first non-empty line."""
        for line in text.splitlines():
            line = line.strip()

            if line:
                return line

        return ""

    def _extract_email(self, text: str) -> str:
        """Extract the first email address from the text."""
        pattern = r"[\w.+-]+@[\w-]+\.[\w.-]+"

        match = re.search(pattern, text)

        if match:
            return match.group(0)

        return ""

    def _extract_phone(self, text: str) -> str:
        """Extract a likely phone number from the text."""
        pattern = r"\+?\d[\d\s().-]{7,}\d"

        match = re.search(pattern, text)

        if match:
            return match.group(0).strip()

        return ""

    def _extract_skills(self, sections: dict[str, str]) -> list[str]:
        """Extract individual skills from the skills section."""
        skills_text = sections.get("skills", "")

        if not skills_text:
            return []

        skills: list[str] = []

        for line in skills_text.splitlines():
            parts = re.split(r"[,;|]", line)

            for part in parts:
                skill = part.strip()

                if skill and skill not in skills:
                    skills.append(skill)

        return skills
