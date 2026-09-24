"""Tests for the Resume Optimizer command-line interface."""

from pathlib import Path

from resumeoptimizer.__main__ import create_parser


def test_create_parser_accepts_required_arguments() -> None:
    """Test that the CLI parser accepts resume and job paths."""
    parser = create_parser()

    args = parser.parse_args(
        [
            "resume.txt",
            "job.txt",
        ],
    )

    assert args.resume == Path("resume.txt")
    assert args.job_description == Path("job.txt")


def test_create_parser_uses_default_output() -> None:
    """Test the default output path."""
    parser = create_parser()

    args = parser.parse_args(
        [
            "resume.txt",
            "job.txt",
        ],
    )

    assert args.output == Path(
        "output/optimized_resume.pdf",
    )


def test_create_parser_accepts_custom_output() -> None:
    """Test that a custom output path can be supplied."""
    parser = create_parser()

    args = parser.parse_args(
        [
            "resume.txt",
            "job.txt",
            "--output",
            "reports/result.pdf",
        ],
    )

    assert args.output == Path(
        "reports/result.pdf",
    )
