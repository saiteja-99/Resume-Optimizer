"""Command-line interface for Resume Optimizer."""

import argparse
from pathlib import Path

from resumeoptimizer.extraction import (
    JobDescriptionExtractor,
    ResumeExtractor,
)
from resumeoptimizer.makers import ResumeMaker
from resumeoptimizer.optimization import ResumeOptimizer
from resumeoptimizer.parsers import DocumentLoader
from resumeoptimizer.processing import SectionDetector
from resumeoptimizer.recommendations import RecommendationEngine
from resumeoptimizer.scoring import ATSScorer


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze and optimize a resume for a job description.",
    )

    parser.add_argument(
        "resume",
        type=Path,
        help="Path to the resume file.",
    )

    parser.add_argument(
        "job_description",
        type=Path,
        help="Path to the job-description file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/optimized_resume.pdf"),
        help="Path for the optimized PDF.",
    )

    return parser


def main() -> None:
    """Run the Resume Optimizer command-line application."""
    parser = create_parser()
    args = parser.parse_args()

    loader = DocumentLoader()

    resume_text = loader.load(args.resume)
    job_text = loader.load(args.job_description)

    section_detector = SectionDetector()

    sections = section_detector.detect(
        resume_text,
    )

    resume_extractor = ResumeExtractor()
    resume = resume_extractor.extract(
        resume_text,
        sections,
    )

    job_extractor = JobDescriptionExtractor()
    job = job_extractor.extract(
        job_text,
    )

    scorer = ATSScorer()
    analysis = scorer.score(
        resume,
        job,
    )

    recommendation_engine = RecommendationEngine()
    recommendations = recommendation_engine.generate(
        resume,
        job,
    )

    optimizer = ResumeOptimizer()
    optimized_text = optimizer.optimize(
        resume,
        job,
    )

    maker = ResumeMaker()
    output_path = maker.create_pdf(
        optimized_text,
        args.output,
    )

    print("Resume analysis complete.")
    print()
    print(f"Resume: {args.resume}")
    print(f"Job description: {args.job_description}")
    print(f"ATS score: {analysis.score:.2f}")
    print()
    print("Recommendations:")

    for recommendation in recommendations:
        print(f"- [{recommendation.priority}] {recommendation.message}")

    print()
    print(f"Optimized PDF: {output_path}")


if __name__ == "__main__":
    main()
