"""Tests for Matplotlib visualizations."""

from pathlib import Path

import pandas as pd
import pytest

from resumeoptimizer.visualization import AnalysisVisualizer


def create_test_dataframe() -> pd.DataFrame:
    """Create sample analysis data for visualization tests."""
    return pd.DataFrame(
        {
            "Category": [
                "Required Skills",
                "Preferred Skills",
                "Keywords",
            ],
            "Matched": [
                2,
                1,
                4,
            ],
            "Missing": [
                1,
                1,
                3,
            ],
            "Total": [
                3,
                2,
                7,
            ],
            "Score": [
                66.67,
                50.0,
                57.14,
            ],
        }
    )


def test_score_chart_is_saved(tmp_path: Path) -> None:
    """Test that the score chart is saved to a file."""
    dataframe = create_test_dataframe()

    output_path = tmp_path / "ats_analysis.png"

    result = AnalysisVisualizer().create_score_chart(
        dataframe,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.stat().st_size > 0


def test_score_chart_creates_parent_directory(
    tmp_path: Path,
) -> None:
    """Test that missing output directories are created."""
    dataframe = create_test_dataframe()

    output_path = tmp_path / "reports" / "charts" / "ats_analysis.png"

    AnalysisVisualizer().create_score_chart(
        dataframe,
        output_path,
    )

    assert output_path.exists()


def test_invalid_dataframe_is_rejected(
    tmp_path: Path,
) -> None:
    """Test invalid DataFrame input."""
    output_path = tmp_path / "chart.png"

    with pytest.raises(TypeError):
        AnalysisVisualizer().create_score_chart(
            "not a dataframe",
            output_path,
        )


def test_missing_category_column_is_rejected(
    tmp_path: Path,
) -> None:
    """Test missing Category column."""
    dataframe = pd.DataFrame(
        {
            "Score": [50.0],
        }
    )

    output_path = tmp_path / "chart.png"

    with pytest.raises(ValueError):
        AnalysisVisualizer().create_score_chart(
            dataframe,
            output_path,
        )


def test_missing_score_column_is_rejected(
    tmp_path: Path,
) -> None:
    """Test missing Score column."""
    dataframe = pd.DataFrame(
        {
            "Category": ["Skills"],
        }
    )

    output_path = tmp_path / "chart.png"

    with pytest.raises(ValueError):
        AnalysisVisualizer().create_score_chart(
            dataframe,
            output_path,
        )
