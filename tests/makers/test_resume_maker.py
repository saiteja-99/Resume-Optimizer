"""Tests for PDF resume generation."""

from pathlib import Path

import pytest
from pypdf import PdfReader

from resumeoptimizer.makers import ResumeMaker


def test_resume_maker_creates_pdf(tmp_path: Path) -> None:
    """Test that ResumeMaker creates a PDF file."""
    output_path = tmp_path / "resume.pdf"

    resume_text = (
        "John Doe\n"
        "Software Engineer\n"
        "Skills\n"
        "Python, SQL\n"
        "Experience\n"
        "Software development experience"
    )

    result = ResumeMaker().create_pdf(
        resume_text,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_generated_file_is_valid_pdf(tmp_path: Path) -> None:
    """Test that the generated file can be read as a PDF."""
    output_path = tmp_path / "resume.pdf"

    ResumeMaker().create_pdf(
        "John Doe\nPython Developer",
        output_path,
    )

    reader = PdfReader(str(output_path))

    assert len(reader.pages) == 1


def test_generated_pdf_contains_resume_text(tmp_path: Path) -> None:
    """Test that important resume text appears in the PDF."""
    output_path = tmp_path / "resume.pdf"

    ResumeMaker().create_pdf(
        "John Doe\nSkills\nPython, SQL",
        output_path,
    )

    reader = PdfReader(str(output_path))
    extracted_text = reader.pages[0].extract_text()

    assert "John Doe" in extracted_text
    assert "Skills" in extracted_text
    assert "Python, SQL" in extracted_text


def test_nested_output_directory_is_created(tmp_path: Path) -> None:
    """Test that missing output directories are created."""
    output_path = tmp_path / "reports" / "resumes" / "optimized.pdf"

    ResumeMaker().create_pdf(
        "John Doe\nPython Developer",
        output_path,
    )

    assert output_path.exists()


def test_empty_resume_is_rejected(tmp_path: Path) -> None:
    """Test that empty resume text is rejected."""
    output_path = tmp_path / "resume.pdf"

    with pytest.raises(ValueError):
        ResumeMaker().create_pdf(
            "",
            output_path,
        )


def test_invalid_resume_text_is_rejected(tmp_path: Path) -> None:
    """Test that non-string resume input is rejected."""
    output_path = tmp_path / "resume.pdf"

    with pytest.raises(TypeError):
        ResumeMaker().create_pdf(
            None,  # type: ignore[arg-type]
            output_path,
        )
