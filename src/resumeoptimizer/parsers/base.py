"""Base class for document parsers."""

from pathlib import Path


class DocumentParser:
    """Base class for document parsers."""

    def parse(self, file_path: str | Path) -> str:
        """Extract text from a document."""
        raise NotImplementedError("Subclasses must implement parse().")
