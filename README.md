# Resume Optimizer

Resume Optimizer is a Python project for comparing a resume with a job
description and generating an ATS-style analysis.

The project can read resume and job-description files, extract skills and
other information, compare keywords, calculate a compatibility score, and
generate recommendations. It can also create an optimized PDF version of
the resume.

The optimizer only uses information that is already present in the resume.
It does not add missing skills or experience.

## Features

- Read TXT, PDF, and DOCX files
- Detect common resume sections
- Extract basic resume and job-description information
- Match required and preferred skills
- Match keywords between a resume and job description
- Calculate an ATS-style compatibility score
- Generate a CSV analysis report
- Generate a score chart using Matplotlib
- Provide recommendations for missing skills and keywords
- Reorder existing job-relevant skills in the resume
- Generate a PDF version of the optimized resume
- Run the complete process from the command line
- Automated tests for the main components

## Project Structure

```text
Resume-Optimizer/
├── examples/
│   ├── sample_job.txt
│   └── sample_resume.txt
├── output/
├── reports/
├── src/
│   └── resumeoptimizer/
│       ├── analysis/
│       ├── extraction/
│       ├── makers/
│       ├── matching/
│       ├── models/
│       ├── optimization/
│       ├── parsers/
│       ├── processing/
│       ├── recommendations/
│       ├── scoring/
│       ├── visualization/
│       ├── cli.py
│       └── __main__.py
├── tests/
├── pyproject.toml
└── README.md