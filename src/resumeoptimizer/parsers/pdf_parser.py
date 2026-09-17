"""Parser for PDF documents."""

from pathlib import Path

from pypdf import PdfReader

from resumeoptimizer.parsers.base import DocumentParser


class PDFParser(DocumentParser):
    """Extract text from PDF documents."""

    def parse(self, file_path: str | Path) -> str:
        """Extract text from all pages of a PDF."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages.append(page_text)

        return "\n".join(pages)
