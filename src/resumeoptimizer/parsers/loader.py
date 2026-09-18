"""Unified document loader."""

from pathlib import Path

from resumeoptimizer.parsers.base import DocumentParser
from resumeoptimizer.parsers.docx_parser import DOCXParser
from resumeoptimizer.parsers.pdf_parser import PDFParser
from resumeoptimizer.parsers.text_parser import TextParser


class DocumentLoader:
    """Select the appropriate parser based on file extension."""

    def __init__(self) -> None:
        """Initialize supported document parsers."""
        self.parsers: dict[str, DocumentParser] = {
            ".txt": TextParser(),
            ".pdf": PDFParser(),
            ".docx": DOCXParser(),
        }

    def load(self, file_path: str | Path) -> str:
        """Extract text from a supported document."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        extension = path.suffix.lower()

        if extension not in self.parsers:
            raise ValueError(f"Unsupported document format: {extension or 'unknown'}")

        parser = self.parsers[extension]

        return parser.parse(path)
