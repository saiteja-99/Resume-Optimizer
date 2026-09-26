"""Tests for the Resume Optimizer command-line interface."""

from pathlib import Path

from resumeoptimizer.__main__ import create_parser, main


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


def test_cli_creates_analysis_outputs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Test that the CLI creates PDF, CSV, and chart outputs."""
    resume_path = tmp_path / "resume.txt"
    job_path = tmp_path / "job.txt"
    output_path = tmp_path / "result" / "resume.pdf"

    resume_path.write_text(
        "John Doe\nSkills\nPython, SQL\nExperience\nSoftware Engineer\n",
        encoding="utf-8",
    )

    job_path.write_text(
        "AI/ML Engineer\n"
        "Example Company\n"
        "Required Skills\n"
        "Python, SQL\n"
        "Preferred Skills\n"
        "Docker\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "resumeoptimizer",
            str(resume_path),
            str(job_path),
            "--output",
            str(output_path),
        ],
    )

    main()

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    assert output_path.parent.joinpath("analysis.csv").exists()

    assert output_path.parent.joinpath("analysis.png").exists()
