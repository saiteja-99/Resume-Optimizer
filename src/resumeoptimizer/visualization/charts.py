"""Create visualizations for resume-job analysis."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


class AnalysisVisualizer:
    """Create charts from resume-job analysis data."""

    def create_score_chart(
        self,
        dataframe: pd.DataFrame,
        output_path: str | Path,
    ) -> Path:
        """Create and save a category-score chart."""
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas DataFrame")

        output_path = Path(output_path)

        if "Category" not in dataframe.columns:
            raise ValueError("dataframe must contain a 'Category' column")

        if "Score" not in dataframe.columns:
            raise ValueError("dataframe must contain a 'Score' column")

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        categories = dataframe["Category"]
        scores = dataframe["Score"]

        figure, axis = plt.subplots(
            figsize=(8, 5),
        )

        axis.bar(
            categories,
            scores,
        )

        axis.set_title("Resume ATS Analysis")
        axis.set_xlabel("Category")
        axis.set_ylabel("Score (%)")

        axis.set_ylim(0, 100)

        axis.tick_params(
            axis="x",
            rotation=20,
        )

        figure.tight_layout()

        figure.savefig(
            output_path,
            dpi=150,
            bbox_inches="tight",
        )

        plt.close(figure)

        return output_path
