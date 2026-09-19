"""Utilities for cleaning and normalizing document text."""

import re


class TextProcessor:
    """Clean and normalize extracted document text."""

    def normalize(self, text: str) -> str:
        """Normalize whitespace and line endings."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        lines = []

        for line in text.split("\n"):
            cleaned_line = re.sub(r"\s+", " ", line).strip()

            if cleaned_line:
                lines.append(cleaned_line)

        return "\n".join(lines)
