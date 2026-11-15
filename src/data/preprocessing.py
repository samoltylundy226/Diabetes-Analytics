"""Data loading, validation, cleaning, and split-before-fit preprocessing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "diabetes_data.csv"
DEFAULT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

TARGET_COLUMN = "Diagnosis"
DROP_NON_FEATURE_COLUMNS = ("PatientID", "DoctorInCharge")

NOMINAL_COLUMNS = ("Ethnicity",)
ORDINAL_COLUMNS = ("SocioeconomicStatus", "EducationLevel")
BINARY_COLUMNS = (
    "Gender",
    "Smoking",
    "FamilyHistoryDiabetes",
    "GestationalDiabetes",
    "PolycysticOvarySyndrome",
    "PreviousPreDiabetes",
    "Hypertension",
    "AntihypertensiveMedications",
    "Statins",
    "AntidiabeticMedications",
    "FrequentUrination",
    "ExcessiveThirst",
    "UnexplainedWeightLoss",
    "BlurredVision",
    "SlowHealingSores",
    "TinglingHandsFeet",
    "HeavyMetalsExposure",
    "OccupationalExposureChemicals",
    "WaterQuality",
)
NUMERICAL_COLUMNS = (
    "Age",
    "BMI",
    "AlcoholConsumption",
    "PhysicalActivity",
    "DietQuality",
    "SleepQuality",
    "SystolicBP",
    "DiastolicBP",
    "FastingBloodSugar",
    "HbA1c",
    "SerumCreatinine",
    "BUNLevels",
    "CholesterolTotal",
    "CholesterolLDL",
    "CholesterolHDL",
    "CholesterolTriglycerides",
    "FatigueLevels",
    "QualityOfLifeScore",
    "MedicalCheckupsFrequency",
    "MedicationAdherence",
    "HealthLiteracy",
)

EXPECTED_COLUMNS = (
    ("PatientID",)
    + NUMERICAL_COLUMNS
    + NOMINAL_COLUMNS
    + ORDINAL_COLUMNS
    + BINARY_COLUMNS
    + (TARGET_COLUMN, "DoctorInCharge")
)


@dataclass(frozen=True)
class ValidationReport:
    """Summary of basic data quality and clinical validation checks."""

    row_count: int
    column_count: int
    missing_values_total: int
    duplicate_rows: int
    duplicate_patient_ids: int
    constant_columns: tuple[str, ...]
    invalid_bp_rows: int
    missing_target_rows: int


def load_raw_data(data_path: Path | str = DEFAULT_RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw diabetes CSV dataset from a relative or explicit path."""
    resolved_path = Path(data_path)
    if not resolved_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {resolved_path}")
    return pd.read_csv(resolved_path)


def validate_dataset(df: pd.DataFrame) -> ValidationReport:
    """Run schema, completeness, duplicate, and clinical sanity checks."""
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Dataset is missing expected columns: {sorted(missing_cols)}")

    constant_cols = tuple(
        col for col in df.columns if df[col].nunique(dropna=False) <= 1
    )
    invalid_bp = int((df["DiastolicBP"] >= df["SystolicBP"]).sum())
    dup_ids = int(df["PatientID"].duplicated().sum())

    return ValidationReport(
        row_count=int(len(df)),
        column_count=int(df.shape[1]),
        missing_values_total=int(df.isnull().sum().sum()),
        duplicate_rows=int(df.duplicated().sum()),
        duplicate_patient_ids=dup_ids,
        constant_columns=constant_cols,
        invalid_bp_rows=invalid_bp,
        missing_target_rows=int(df[TARGET_COLUMN].isnull().sum()),
    )


def clean_dataset(
    df: pd.DataFrame,
    drop_invalid_bp: bool = False,
) -> pd.DataFrame:
    """Return a cleaned copy of the dataset while keeping raw data untouched.

    Adds an explicit ``IsInvalidBP`` flag for records where
    ``DiastolicBP >= SystolicBP`` and removes exact duplicates, rows missing
    the target label, and non-feature administrative columns.
    """
    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=[TARGET_COLUMN])
    cleaned = cleaned.drop_duplicates()

    cleaned["IsInvalidBP"] = (cleaned["DiastolicBP"] >= cleaned["SystolicBP"]).astype(int)
    if drop_invalid_bp:
        cleaned = cleaned.loc[cleaned["IsInvalidBP"] == 0].copy()

    cols_to_drop = [col for col in DROP_NON_FEATURE_COLUMNS if col in cleaned.columns]
    cleaned = cleaned.drop(columns=cols_to_drop)
    return cleaned.reset_index(drop=True)


def split_features_target(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
    exclude_features: Iterable[str] = (),
) -> tuple[pd.DataFrame, pd.Series]:
    """Separate feature matrix X and target vector y."""
    excluded = set(exclude_features) | {target_column}
    feature_cols = [col for col in df.columns if col not in excluded]
    return df[feature_cols].copy(), df[target_column].copy()


def create_stratified_splits(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
    exclude_features: Iterable[str] = (),
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into stratified train and test sets BEFORE fitting pipelines."""
    X, y = split_features_target(df, exclude_features=exclude_features)
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def build_preprocessor(feature_columns: Iterable[str]) -> ColumnTransformer:
    """Build an unfitted ColumnTransformer tailored to the active feature subset."""
    available = set(feature_columns)

    num_cols = [
        c for c in NUMERICAL_COLUMNS if c in available
    ]
    nom_cols = [c for c in NOMINAL_COLUMNS if c in available]
    ord_cols = [c for c in ORDINAL_COLUMNS if c in available]
    bin_cols = [
        c for c in (*BINARY_COLUMNS, "IsInvalidBP") if c in available
    ]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    nominal_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    ordinal_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            ),
        ]
    )
    binary_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, num_cols),
            ("nom", nominal_pipe, nom_cols),
            ("ord", ordinal_pipe, ord_cols),
            ("bin", binary_pipe, bin_cols),
        ],
        remainder="drop",
    )
