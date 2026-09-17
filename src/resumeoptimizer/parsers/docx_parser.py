"""Parser for Microsoft Word DOCX documents."""

from pathlib import Path

from docx import Document

from resumeoptimizer.parsers.base import DocumentParser


class DOCXParser(DocumentParser):
    """Extract text from DOCX documents."""

    def parse(self, file_path: str | Path) -> str:
        """Extract text from paragraphs in a DOCX document."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        document = Document(path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)
