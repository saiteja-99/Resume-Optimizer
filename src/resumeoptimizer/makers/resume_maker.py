"""Generate PDF resumes from resume text."""

from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class ResumeMaker:
    """Create a readable PDF resume from text."""

    def __init__(self) -> None:
        """Initialize PDF styles."""
        styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "ResumeTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=8,
        )

        self.body_style = ParagraphStyle(
            "ResumeBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            spaceAfter=4,
        )

        self.heading_style = ParagraphStyle(
            "ResumeHeading",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=8,
            spaceAfter=4,
        )

    def create_pdf(
        self,
        resume_text: str,
        output_path: str | Path,
    ) -> Path:
        """Create a PDF file from resume text."""
        if not isinstance(resume_text, str):
            raise TypeError("resume_text must be a string")

        if not resume_text.strip():
            raise ValueError("resume_text must not be empty")

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

        story = []

        lines = [line.strip() for line in resume_text.splitlines() if line.strip()]

        for index, line in enumerate(lines):
            if index == 0:
                story.append(
                    Paragraph(
                        line,
                        self.title_style,
                    )
                )
                continue

            if self._looks_like_heading(line):
                story.append(
                    Paragraph(
                        line,
                        self.heading_style,
                    )
                )
            else:
                story.append(
                    Paragraph(
                        line,
                        self.body_style,
                    )
                )

            story.append(Spacer(1, 2))

        document.build(story)

        return output_path

    def _looks_like_heading(self, line: str) -> bool:
        """Determine whether a line looks like a resume section heading."""
        normalized = line.strip().lower()

        headings = {
            "summary",
            "profile",
            "skills",
            "technical skills",
            "experience",
            "work experience",
            "professional experience",
            "education",
            "projects",
            "certifications",
        }

        return normalized in headings
