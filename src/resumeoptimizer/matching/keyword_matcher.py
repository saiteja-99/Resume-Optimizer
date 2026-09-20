"""Match important job-description keywords against resume text."""

import re
from typing import ClassVar

from resumeoptimizer.models import KeywordMatchResult, Resume


class KeywordMatcher:
    """Compare important keywords in a job description with a resume."""

    STOPWORDS: ClassVar[set[str]] = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "our",
        "that",
        "the",
        "this",
        "to",
        "we",
        "with",
        "you",
        "your",
    }

    def match(
        self,
        resume: Resume,
        job_text: str,
    ) -> KeywordMatchResult:
        """Find important job keywords and check whether they appear in the resume."""
        if not isinstance(resume, Resume):
            raise TypeError("resume must be a Resume object")

        if not isinstance(job_text, str):
            raise TypeError("job_text must be a string")

        job_keywords = self._extract_keywords(job_text)
        resume_keywords = self._extract_keywords(resume.text)

        matched = [keyword for keyword in job_keywords if keyword in resume_keywords]

        missing = [
            keyword for keyword in job_keywords if keyword not in resume_keywords
        ]

        return KeywordMatchResult(
            matched_keywords=matched,
            missing_keywords=missing,
        )

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract unique meaningful keywords from text."""
        words = re.findall(r"[a-zA-Z0-9+#.-]+", text.lower())

        keywords: list[str] = []

        for word in words:
            word = word.strip("-. ")

            if not word:
                continue

            if word in self.STOPWORDS:
                continue

            if len(word) < 2:
                continue

            if word not in keywords:
                keywords.append(word)

        return keywords
