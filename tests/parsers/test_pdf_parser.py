"""Tests for the PDF document parser."""

from pathlib import Path

from pypdf import PdfWriter

from resumeoptimizer.parsers import PDFParser


def test_pdf_parser_reads_pdf(tmp_path: Path) -> None:
    """Test that PDFParser can read a PDF document."""
    file_path = tmp_path / "resume.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with file_path.open("wb") as file:
        writer.write(file)

    parser = PDFParser()

    result = parser.parse(file_path)

    assert isinstance(result, str)
