"""Exploratory data analysis helpers for Diabetes Healthcare Analytics."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.data.preprocessing import TARGET_COLUMN


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


def summarize_by_diagnosis(
    df: pd.DataFrame,
    columns: list[str],
    target_column: str = TARGET_COLUMN,
) -> pd.DataFrame:
    """Compute mean, median, and std of selected numerical columns by Diagnosis."""
    valid_cols = [col for col in columns if col in df.columns]
    return df.groupby(target_column)[valid_cols].agg(["mean", "median", "std"]).round(3)


def compute_diagnosis_rates(
    df: pd.DataFrame,
    group_column: str,
    target_column: str = TARGET_COLUMN,
) -> pd.DataFrame:
    """Return patient counts and positive Diagnosis rate (%) for a grouping variable."""
    summary = (
        df.groupby(group_column)[target_column]
        .agg(patient_count="count", diabetes_cases="sum", diabetes_rate="mean")
        .reset_index()
    )
    summary["diabetes_rate_pct"] = (summary["diabetes_rate"] * 100).round(2)
    return summary


def plot_target_distribution(
    df: pd.DataFrame,
    output_dir: Path | str = DEFAULT_FIGURES_DIR,
    save: bool = True,
) -> Path | None:
    """Plot class distribution of the Diagnosis target variable."""
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x=TARGET_COLUMN, ax=ax, palette="Set2", hue=TARGET_COLUMN, legend=False)
    ax.set_title("Distribution of Existing Diabetes Diagnosis")
    ax.set_xlabel("Diagnosis (0 = No Diabetes, 1 = Diabetes)")
    ax.set_ylabel("Patient Count")

    for patch in ax.patches:
        height = patch.get_height()
        ax.annotate(
            f"{int(height)}",
            (patch.get_x() + patch.get_width() / 2.0, height),
            ha="center",
            va="bottom",
        )

    fig.tight_layout()
    if save:
        out_path = Path(output_dir) / "diagnosis_distribution.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return out_path
    return None


def plot_key_biomarkers(
    df: pd.DataFrame,
    biomarkers: tuple[str, ...] = ("FastingBloodSugar", "HbA1c", "BMI", "Age"),
    output_dir: Path | str = DEFAULT_FIGURES_DIR,
    save: bool = True,
) -> Path | None:
    """Plot boxplots comparing key biomarkers across Diagnosis groups."""
    valid = [col for col in biomarkers if col in df.columns]
    fig, axes = plt.subplots(1, len(valid), figsize=(4 * len(valid), 4))
    if len(valid) == 1:
        axes = [axes]

    for ax, col in zip(axes, valid):
        sns.boxplot(data=df, x=TARGET_COLUMN, y=col, ax=ax, palette="Set2", hue=TARGET_COLUMN, legend=False)
        ax.set_title(f"{col} by Diagnosis")
        ax.set_xlabel("Diagnosis")

    fig.tight_layout()
    if save:
        out_path = Path(output_dir) / "key_biomarkers_by_diagnosis.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return out_path
    return None


def top_target_correlations(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
    top_n: int = 15,
) -> pd.Series:
    """Return top features ranked by absolute Pearson correlation with Diagnosis."""
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr(numeric_only=True)[target_column].drop(labels=[target_column])
    return corr.reindex(corr.abs().sort_values(ascending=False).index).head(top_n).round(4)
