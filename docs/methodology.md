# Methodology

## 1. Data Integrity & Governance
- **Raw Data Immutability:** `data/raw/diabetes_data.csv` is never modified in place.
- **Schema Validation:** `src/data/preprocessing.py::validate_dataset()` checks column presence, missing values, duplicates, constant columns (`DoctorInCharge`), and physiological consistency (`DiastolicBP < SystolicBP`).
- **Anomaly Handling:** Rather than silently deleting records with `DiastolicBP >= SystolicBP` (`158` rows), `clean_dataset()` adds an `IsInvalidBP` indicator and supports optional filtering (`drop_invalid_bp=True`) for sensitivity checks.

## 2. Exploratory Data Analysis & SQL Auditing
- SQL scripts (`sql/02_data_quality_checks.sql` and `sql/03_healthcare_analysis.sql`) provide database-level verification and cohort aggregations across age bands, BMI categories, HbA1c bands, symptoms, and socioeconomic tiers.
- Python analysis helpers (`src/analysis/analysis.py`) compute subgroup diagnosis rates, summary statistics, and correlation rankings.

## 3. Leakage-Free Machine Learning Pipeline
1. **Split Before Fit:** `create_stratified_splits()` divides `X` and `y` (80% train / 20% test, stratified on `Diagnosis`) prior to fitting any scaler, imputer, or encoder.
2. **Column-Type-Aware Preprocessing:**
   - Continuous numerical columns: median imputation + `StandardScaler`.
   - Nominal column (`Ethnicity`): most-frequent imputation + `OneHotEncoder`.
   - Ordinal columns (`SocioeconomicStatus`, `EducationLevel`): most-frequent imputation + `OrdinalEncoder`.
   - Binary columns: most-frequent imputation pass-through.
3. **Baseline & Model Comparison:** Benchmarks `DummyClassifier` (majority class) against `LogisticRegression`, `RandomForestClassifier`, and `GradientBoostingClassifier` via 5-fold `StratifiedKFold` cross-validation.
4. **Diagnostic Leakage Sensitivity:** Evaluates models both with and without `FastingBloodSugar`, `HbA1c`, and `AntidiabeticMedications` to separate direct diagnostic criteria from demographic, lifestyle, and comorbidity signals.
