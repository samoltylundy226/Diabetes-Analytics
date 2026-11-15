"""Starter ML training framework for cross-sectional diabetes diagnosis classification.

Note: Models classify *existing* diabetes diagnosis from patient records;
they do not forecast future diabetes incidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

from src.data.preprocessing import (
    build_preprocessor,
    clean_dataset,
    create_stratified_splits,
    load_raw_data,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODELS_DIR = PROJECT_ROOT / "models"

# Features directly tied to clinical diagnosis or post-diagnosis treatment.
# Excluding these in sensitivity experiments helps evaluate non-diagnostic factors.
DIAGNOSTIC_AND_TREATMENT_COLUMNS = (
    "FastingBloodSugar",
    "HbA1c",
    "AntidiabeticMedications",
)


@dataclass
class TrainingArtifacts:
    """Container holding split datasets, fitted pipelines, and CV summaries."""

    pipelines: dict[str, Pipeline]
    cv_results: pd.DataFrame
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def build_candidate_models(random_state: int = 42) -> dict[str, Any]:
    """Return baseline and candidate classification estimators."""
    return {
        "dummy_majority": DummyClassifier(strategy="most_frequent"),
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=random_state,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingClassifier(
            random_state=random_state,
        ),
    }


def build_model_pipeline(estimator: Any, feature_columns: pd.Index) -> Pipeline:
    """Wrap preprocessing and estimator into a leakage-safe sklearn Pipeline."""
    preprocessor = build_preprocessor(feature_columns)
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", estimator),
        ]
    )


def run_cross_validation(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 5,
    random_state: int = 42,
) -> tuple[dict[str, Pipeline], pd.DataFrame]:
    """Evaluate candidate pipelines on training data using Stratified K-Fold CV."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
        "average_precision": "average_precision",
    }

    rows: list[dict[str, float | str]] = []
    pipelines: dict[str, Pipeline] = {}

    for name, estimator in build_candidate_models(random_state=random_state).items():
        pipe = build_model_pipeline(estimator, X_train.columns)
        scores = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)
        pipe.fit(X_train, y_train)
        pipelines[name] = pipe

        rows.append(
            {
                "model": name,
                "cv_accuracy_mean": float(scores["test_accuracy"].mean()),
                "cv_precision_mean": float(scores["test_precision"].mean()),
                "cv_recall_mean": float(scores["test_recall"].mean()),
                "cv_f1_mean": float(scores["test_f1"].mean()),
                "cv_roc_auc_mean": float(scores["test_roc_auc"].mean()),
                "cv_pr_auc_mean": float(scores["test_average_precision"].mean()),
            }
        )

    summary_df = pd.DataFrame(rows).sort_values(by="cv_f1_mean", ascending=False)
    return pipelines, summary_df.reset_index(drop=True)


def run_training_framework(
    exclude_diagnostic_markers: bool = False,
    test_size: float = 0.2,
    random_state: int = 42,
) -> TrainingArtifacts:
    """Load data, split before preprocessing, and run baseline CV pipelines."""
    raw_df = load_raw_data()
    cleaned_df = clean_dataset(raw_df, drop_invalid_bp=False)

    exclude_cols = DIAGNOSTIC_AND_TREATMENT_COLUMNS if exclude_diagnostic_markers else ()
    X_train, X_test, y_train, y_test = create_stratified_splits(
        cleaned_df,
        test_size=test_size,
        random_state=random_state,
        exclude_features=exclude_cols,
    )

    pipelines, cv_results = run_cross_validation(
        X_train,
        y_train,
        n_splits=5,
        random_state=random_state,
    )
    return TrainingArtifacts(
        pipelines=pipelines,
        cv_results=cv_results,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )
