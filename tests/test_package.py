"""Tests for the Resume Optimizer package."""

from resumeoptimizer import __version__


def test_package_version() -> None:
    """Verify that the package exposes a version."""
    assert __version__ == "0.1.0"
