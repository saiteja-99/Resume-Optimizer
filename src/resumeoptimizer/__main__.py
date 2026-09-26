"""Command-line interface for Resume Optimizer."""

import argparse
from pathlib import Path

from resumeoptimizer.analysis import AnalysisReport
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
from resumeoptimizer.visualization import AnalysisVisualizer


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

    analysis_report = AnalysisReport()

    analysis_dataframe = analysis_report.create_dataframe(
        resume,
        job,
    )

    output_directory = args.output.parent

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    analysis_csv_path = output_directory / "analysis.csv"

    analysis_dataframe.to_csv(
        analysis_csv_path,
        index=False,
    )

    visualizer = AnalysisVisualizer()

    analysis_chart_path = output_directory / "analysis.png"

    visualizer.create_score_chart(
        analysis_dataframe,
        analysis_chart_path,
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
    print("Analysis:")

    for _, row in analysis_dataframe.iterrows():
        print(
            f"- {row['Category']}: "
            f"{row['Matched']} matched / "
            f"{row['Missing']} missing "
            f"({row['Score']:.2f}%)"
        )

    print()
    print("Recommendations:")

    for recommendation in recommendations:
        print(f"- [{recommendation.priority}] {recommendation.message}")

    print()
    print(f"Optimized PDF: {output_path}")
    print(f"Analysis CSV: {analysis_csv_path}")
    print(f"Analysis chart: {analysis_chart_path}")


if __name__ == "__main__":
    main()
