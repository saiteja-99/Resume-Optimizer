"""Run Resume Optimizer as a Python module."""

from resumeoptimizer.cli import create_parser, main

__all__ = ["create_parser", "main"]


if __name__ == "__main__":
    main()
