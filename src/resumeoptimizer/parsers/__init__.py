"""Document parsers for Resume Optimizer."""

from resumeoptimizer.parsers.base import DocumentParser
from resumeoptimizer.parsers.docx_parser import DOCXParser
from resumeoptimizer.parsers.pdf_parser import PDFParser
from resumeoptimizer.parsers.text_parser import TextParser

__all__ = [
    "DOCXParser",
    "DocumentParser",
    "PDFParser",
    "TextParser",
]
