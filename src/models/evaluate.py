"""Evaluation utilities for cross-sectional diabetes diagnosis classification."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_METRICS_DIR = PROJECT_ROOT / "outputs" / "metrics"
DEFAULT_FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


def evaluate_classifier(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str,
) -> dict[str, float | str]:
    """Compute classification metrics on the held-out test split."""
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = y_pred

    return {
        "model": model_name,
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
        "pr_auc": round(float(average_precision_score(y_test, y_prob)), 4),
    }


def evaluate_all_models(
    pipelines: dict[str, Pipeline],
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.DataFrame:
    """Evaluate all fitted candidate pipelines and rank by F1-score."""
    records = [
        evaluate_classifier(pipe, X_test, y_test, model_name=name)
        for name, pipe in pipelines.items()
    ]
    return pd.DataFrame(records).sort_values(by="f1", ascending=False).reset_index(drop=True)


def save_confusion_matrix(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str,
    output_dir: Path | str = DEFAULT_FIGURES_DIR,
) -> Path:
    """Generate and save a confusion matrix plot for a fitted model."""
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 4))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Diabetes (0)", "Diabetes (1)"])
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(f"Confusion Matrix: {model_name}")
    fig.tight_layout()

    out_path = Path(output_dir) / f"confusion_matrix_{model_name}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def save_metrics_report(
    metrics_df: pd.DataFrame,
    filename: str = "classification_metrics.json",
    output_dir: Path | str = DEFAULT_METRICS_DIR,
) -> Path:
    """Save evaluation metrics table to JSON in outputs/metrics/."""
    out_path = Path(output_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = metrics_df.to_dict(orient="records")
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path
