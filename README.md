# Diabetes Healthcare Analytics: Patient Risk Factor Analysis and Machine Learning-Based Diagnosis Classification

An end-to-end, reproducible healthcare analytics and machine learning portfolio project built around structured patient clinical, demographic, lifestyle, symptom, and environmental records (`diabetes_data.csv`).

> **Scope & Clinical Framing:** This dataset contains **existing cross-sectional diagnosis labels** (`Diagnosis` = 0 or 1). The machine learning pipeline classifies **existing diabetes diagnosis** from patient attributes—it does **not** predict future diabetes incidence.

---

## Project Objectives

- Analyze patient demographic, socioeconomic, and medical history characteristics.
- Explore clinical, behavioral, and symptom factors associated with existing diabetes `Diagnosis`.
- Identify patterns across blood sugar (`FastingBloodSugar`, `HbA1c`), `BMI`, blood pressure, lipid panels, and lifestyle scores.
- Validate and analyze healthcare data using reproducible SQL queries and modular Python pipelines.
- Prepare interactive healthcare dashboards (Power BI) to communicate patterns visually.
- Develop a leakage-free machine learning classification framework for `Diagnosis`.

## Business Problem

Healthcare analysts and clinical informatics teams often receive multi-domain patient records containing demographics, lab biomarkers, medications, symptoms, and lifestyle surveys alongside data-quality anomalies. Without structured validation, exploratory analysis, and leakage-aware modeling, analysts risk drawing misleading conclusions—for example, confusing post-diagnosis medications or direct diagnostic labs with upstream lifestyle risk factors. This project establishes a clean engineering, SQL, BI, and ML workflow to audit the data, quantify factor associations, and classify existing `Diagnosis` transparently.

## Research Questions

1. How are demographic variables (`Age`, `Gender`, `Ethnicity`, `SocioeconomicStatus`, `EducationLevel`) distributed across diagnosed and non-diagnosed patient groups?
2. Which clinical biomarkers (`HbA1c`, `FastingBloodSugar`, `BMI`, blood pressure, cholesterol profile) and comorbidities (`Hypertension`, `FamilyHistoryDiabetes`, `PreviousPreDiabetes`) show the strongest association with `Diagnosis`?
3. How do lifestyle factors (`PhysicalActivity`, `DietQuality`, `SleepQuality`, `Smoking`, `AlcoholConsumption`) and symptom indicators (`FrequentUrination`, `ExcessiveThirst`, `BlurredVision`, `SlowHealingSores`, `TinglingHandsFeet`) differ by diagnosis status?
4. What data quality issues (e.g., constant fields, invalid blood-pressure ordering, sex-specific condition anomalies) exist in the raw patient records, and how should they be handled?
5. How accurately can ML classifiers distinguish `Diagnosis = 1` vs. `Diagnosis = 0`, and how much does performance change when diagnostic labs (`HbA1c`, `FastingBloodSugar`) and `AntidiabeticMedications` are excluded?

## Dataset Overview

- **Source file:** `data/raw/diabetes_data.csv` (kept immutable)
- **Records:** `1,879` unique patients (`PatientID` `6000`–`7878`)
- **Features:** `46` columns total (`43` candidate analytical features after excluding `PatientID`, constant `DoctorInCharge`, and target `Diagnosis`)
- **Missing values & duplicates:** `0` missing values; `0` exact duplicate rows
- **Target balance (`Diagnosis`):**
  - `0` (No Diabetes): `1,127` (`59.98%`)
  - `1` (Diabetes): `752` (`40.02%`)
- **Documented data-quality flags:**
  - `DoctorInCharge` is constant (`"Confidential"` in all `1,879` rows).
  - `158` rows (`8.41%`) have `DiastolicBP >= SystolicBP`.
  - `GestationalDiabetes = 1` and `PolycysticOvarySyndrome = 1` appear across both `Gender = 0` and `Gender = 1`.

See [data/README.md](data/README.md) and [docs/data_dictionary.md](docs/data_dictionary.md) for complete details.

## Technology Stack

- **Programming & Data Engineering:** Python 3.12+, `pandas`, `numpy`, `pathlib`
- **Visualization:** `matplotlib`, `seaborn`, Jupyter Notebooks
- **Machine Learning:** `scikit-learn` (`Pipeline`, `ColumnTransformer`, `StratifiedKFold`)
- **Database & Analytics:** SQL (`01_database_setup.sql`, `02_data_quality_checks.sql`, `03_healthcare_analysis.sql`)
- **Business Intelligence:** Power BI (planned dashboard workspace in `powerbi/`)
- **Testing & Version Control:** `pytest`, Git, GitHub

## Project Architecture

```text
Raw CSV (data/raw/diabetes_data.csv)
   ├──► SQL Pipeline (sql/) ───────────────► Schema + Quality Audit + Aggregate Queries
   ├──► Python Data Module (src/data/) ────► Validation + Cleaning + Split-Before-Fit Pipeline
   ├──► EDA Module & Notebooks ────────────► Figures (outputs/figures/) + Power BI Inputs
   └──► ML Framework (src/models/) ────────► Stratified CV + Held-Out Metrics (outputs/metrics/)
```

## Folder Structure

```text
Diabetes-Healthcare-Analytics/
│
├── data/
│   ├── raw/
│   │   └── diabetes_data.csv
│   ├── processed/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_machine_learning.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── analysis.py
│   └── models/
│       ├── __init__.py
│       ├── train.py
│       └── evaluate.py
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_data_quality_checks.sql
│   └── 03_healthcare_analysis.sql
│
├── powerbi/
│   ├── README.md
│   └── screenshots/
│
├── models/
│   └── README.md
│
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── metrics/
│
├── tests/
│   ├── __init__.py
│   └── test_preprocessing.py
│
├── docs/
│   ├── project_overview.md
│   ├── data_dictionary.md
│   └── methodology.md
│
├── .gitignore
├── requirements.txt
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

## Installation Instructions

```bash
git clone https://github.com/samoltylundy226/Diabetes-Analytics.git
cd Diabetes-Analytics

python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## How to Run the Project

1. **Run unit tests:**
   ```bash
   pytest
   ```
2. **Explore and clean the data:** Open and run notebooks in order:
   - `notebooks/01_data_exploration.ipynb`
   - `notebooks/02_data_cleaning.ipynb`
   - `notebooks/03_exploratory_data_analysis.ipynb`
   - `notebooks/04_machine_learning.ipynb`
3. **Run SQL checks (PostgreSQL example):** Execute `sql/01_database_setup.sql`, load `data/raw/diabetes_data.csv`, then run `sql/02_data_quality_checks.sql` and `sql/03_healthcare_analysis.sql`.

## Dashboard Preview

*Placeholder: Interactive Power BI dashboards are planned for Stage 2. Once built, dashboard screenshots will be saved to `powerbi/screenshots/` and embedded here.*

- Planned Page 1: Executive Healthcare Overview
- Planned Page 2: Clinical Biomarkers & Comorbidities
- Planned Page 3: Lifestyle Factors & Symptom Profiles

## Machine Learning Methodology

1. **Leakage Prevention:** Split `X` and `y` using stratified 80/20 sampling (`create_stratified_splits`) **before** fitting any imputer, scaler, or encoder.
2. **Feature Encoding & Scaling:** Inside `ColumnTransformer`, standardize continuous numerical features, one-hot encode nominal `Ethnicity`, ordinal-encode `SocioeconomicStatus` and `EducationLevel`, and pass through binary indicators.
3. **Model Comparison:** Benchmark a naive majority-class baseline (`DummyClassifier`) against `LogisticRegression`, `RandomForestClassifier`, and `GradientBoostingClassifier` using 5-fold Stratified Cross-Validation.
4. **Diagnostic-Leakage Sensitivity Check:** Compare models trained with all features vs. models trained without `FastingBloodSugar`, `HbA1c`, and `AntidiabeticMedications`.

## Evaluation Metrics

Because `Diagnosis` has a ~60/40 class distribution and false negatives carry clinical importance in healthcare screening analysis, evaluation tracks:

- **F1-Score** (primary balanced classification metric)
- **Recall (Sensitivity)** & **Precision**
- **ROC-AUC** & **PR-AUC (Average Precision)**
- **Accuracy** & **Confusion Matrix**

## Key Findings

*Placeholder: Exploratory analysis and model training benchmarks are not finalized at this project-setup stage. Verified findings from `03_exploratory_data_analysis.ipynb`, SQL queries, and `04_machine_learning.ipynb` will be documented here once executed.*

- **Initial Data Audit (Verified):** `1,879` patients, `46` columns, `0` missing values, `0` duplicate rows, `40.02%` positive `Diagnosis`, `1` constant column (`DoctorInCharge`), and `158` rows with `DiastolicBP >= SystolicBP`.
- **EDA Findings:** *Pending notebook execution.*
- **Model Benchmark Results:** *Pending notebook execution.*

## Future Improvements

- Execute full EDA and publish annotated charts to `outputs/figures/`.
- Tune hyperparameters, inspect probability calibration curves, and run subgroup error analysis across age, gender, and socioeconomic groups.
- Add SHAP feature-importance explanations for clinical interpretability.
- Build and publish the interactive Power BI `.pbix` dashboard and screenshots in `powerbi/screenshots/`.
