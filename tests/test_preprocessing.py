"""Unit tests for data validation and preprocessing logic."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data.preprocessing import (
    DEFAULT_RAW_DATA_PATH,
    build_preprocessor,
    clean_dataset,
    create_stratified_splits,
    load_raw_data,
    validate_dataset,
)


def _sample_dataframe() -> pd.DataFrame:
    """Create a small synthetic test fixture matching the 46-column schema."""
    base = {
        "PatientID": [1, 2, 3, 4, 5, 6],
        "Age": [30, 45, 52, 60, 40, 70],
        "Gender": [0, 1, 0, 1, 0, 1],
        "Ethnicity": [0, 1, 2, 3, 0, 1],
        "SocioeconomicStatus": [0, 1, 2, 1, 0, 2],
        "EducationLevel": [1, 2, 3, 0, 1, 2],
        "BMI": [22.0, 29.5, 34.1, 27.0, 24.3, 31.8],
        "Smoking": [0, 1, 0, 1, 0, 0],
        "AlcoholConsumption": [1.0, 5.0, 2.0, 8.0, 0.5, 3.0],
        "PhysicalActivity": [7.0, 3.0, 2.5, 4.0, 8.0, 1.5],
        "DietQuality": [6.5, 4.0, 3.5, 5.0, 7.5, 3.0],
        "SleepQuality": [7.5, 6.0, 5.5, 6.5, 8.0, 5.0],
        "FamilyHistoryDiabetes": [0, 1, 1, 0, 0, 1],
        "GestationalDiabetes": [0, 0, 1, 0, 0, 0],
        "PolycysticOvarySyndrome": [0, 0, 0, 0, 0, 0],
        "PreviousPreDiabetes": [0, 1, 0, 1, 0, 1],
        "Hypertension": [0, 0, 1, 1, 0, 1],
        "SystolicBP": [118, 130, 100, 150, 120, 160],
        "DiastolicBP": [76, 85, 105, 92, 78, 95],
        "FastingBloodSugar": [88.0, 115.0, 165.0, 142.0, 92.0, 178.0],
        "HbA1c": [5.1, 6.0, 8.2, 7.4, 5.3, 8.9],
        "SerumCreatinine": [0.9, 1.1, 1.8, 1.4, 0.8, 2.2],
        "BUNLevels": [14.0, 18.0, 28.0, 22.0, 15.0, 30.0],
        "CholesterolTotal": [180.0, 210.0, 250.0, 230.0, 175.0, 265.0],
        "CholesterolLDL": [100.0, 130.0, 160.0, 145.0, 95.0, 170.0],
        "CholesterolHDL": [60.0, 48.0, 38.0, 42.0, 62.0, 35.0],
        "CholesterolTriglycerides": [110.0, 180.0, 260.0, 210.0, 95.0, 290.0],
        "AntihypertensiveMedications": [0, 0, 1, 1, 0, 1],
        "Statins": [0, 1, 1, 1, 0, 1],
        "AntidiabeticMedications": [0, 0, 1, 1, 0, 1],
        "FrequentUrination": [0, 0, 1, 1, 0, 1],
        "ExcessiveThirst": [0, 0, 1, 0, 0, 1],
        "UnexplainedWeightLoss": [0, 0, 0, 1, 0, 0],
        "FatigueLevels": [2.0, 4.0, 8.0, 6.5, 1.5, 7.5],
        "BlurredVision": [0, 0, 1, 0, 0, 1],
        "SlowHealingSores": [0, 0, 0, 1, 0, 1],
        "TinglingHandsFeet": [0, 0, 1, 0, 0, 1],
        "QualityOfLifeScore": [85.0, 70.0, 40.0, 50.0, 88.0, 35.0],
        "HeavyMetalsExposure": [0, 0, 0, 0, 0, 1],
        "OccupationalExposureChemicals": [0, 0, 1, 0, 0, 0],
        "WaterQuality": [1, 1, 0, 1, 1, 0],
        "MedicalCheckupsFrequency": [2.0, 1.5, 3.0, 2.5, 1.0, 3.5],
        "MedicationAdherence": [8.0, 7.0, 5.0, 6.0, 9.0, 4.5],
        "HealthLiteracy": [8.0, 6.5, 5.0, 6.0, 8.5, 4.0],
        "Diagnosis": [0, 0, 1, 1, 0, 1],
        "DoctorInCharge": ["Confidential"] * 6,
    }
    return pd.DataFrame(base)


def test_validate_and_clean_dataset() -> None:
    df = _sample_dataframe()
    report = validate_dataset(df)
    assert report.row_count == 6
    assert report.column_count == 46
    assert report.invalid_bp_rows == 1
    assert "DoctorInCharge" in report.constant_columns

    cleaned = clean_dataset(df, drop_invalid_bp=False)
    assert "PatientID" not in cleaned.columns
    assert "DoctorInCharge" not in cleaned.columns
    assert cleaned["IsInvalidBP"].sum() == 1

    strict_cleaned = clean_dataset(df, drop_invalid_bp=True)
    assert len(strict_cleaned) == 5


def test_stratified_split_and_preprocessor() -> None:
    df = clean_dataset(_sample_dataframe())
    X_train, X_test, y_train, y_test = create_stratified_splits(
        df, test_size=0.33, random_state=42
    )
    assert len(X_train) == 4
    assert len(X_test) == 2
    assert y_train.nunique() == 2
    assert y_test.nunique() == 2

    preprocessor = build_preprocessor(X_train.columns)
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)
    assert X_train_t.shape[0] == 4
    assert X_test_t.shape[0] == 2
    assert X_train_t.shape[1] == X_test_t.shape[1]


@pytest.mark.skipif(
    not DEFAULT_RAW_DATA_PATH.exists(),
    reason="Raw dataset not present",
)
def test_raw_dataset_integrity() -> None:
    raw_df = load_raw_data()
    report = validate_dataset(raw_df)
    assert report.row_count == 1879
    assert report.column_count == 46
    assert report.missing_values_total == 0
    assert report.duplicate_rows == 0
