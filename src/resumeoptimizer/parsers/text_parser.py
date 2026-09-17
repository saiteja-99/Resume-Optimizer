"""Parser for plain-text documents."""

from pathlib import Path

from resumeoptimizer.parsers.base import DocumentParser


class TextParser(DocumentParser):
    """Extract text from plain-text files."""

    def parse(self, file_path: str | Path) -> str:
        """Read a UTF-8 text file and return its contents."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        return path.read_text(encoding="utf-8")
