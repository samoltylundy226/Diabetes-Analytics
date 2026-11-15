# Data Dictionary (`diabetes_data.csv`)

This document describes all **46 columns** in `data/raw/diabetes_data.csv` (`1,879` records, `0` missing values, `0` exact duplicates).

## 1. Identifiers & Administrative Fields

| Column | Type | Observed Range / Values | Missing | Role & Notes |
| :--- | :--- | :--- | :---: | :--- |
| `PatientID` | Integer | `6000` – `7878` (1,879 unique) | 0 | Unique patient record ID; drop before modeling. |
| `DoctorInCharge` | String (Categorical) | `"Confidential"` (1 unique) | 0 | Constant anonymized placeholder; zero variance, drop before modeling. |

## 2. Target Variable

| Column | Type | Observed Values & Counts | Missing | Role & Notes |
| :--- | :--- | :--- | :---: | :--- |
| `Diagnosis` | Binary (0/1) | `0`: 1,127 (59.98%), `1`: 752 (40.02%) | 0 | Existing diabetes diagnosis label (`0` = Negative, `1` = Positive). |

## 3. Demographics & Socioeconomic Variables

| Column | Type | Observed Values / Range | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `Age` | Integer | `20` – `90` (mean `55.04`) | 0 | Patient age in years. |
| `Gender` | Binary (0/1) | `0`: 963, `1`: 916 | 0 | Encoded binary gender (see anomaly note on sex-specific conditions). |
| `Ethnicity` | Categorical (0–3) | `0`: 1,099, `1`: 357, `2`: 206, `3`: 217 | 0 | Integer-encoded ethnic group (nominal). |
| `SocioeconomicStatus` | Categorical (0–2) | `0`: 557, `1`: 780, `2`: 542 | 0 | Ordinal/categorical socioeconomic tier. |
| `EducationLevel` | Categorical (0–3) | `0`: 163, `1`: 615, `2`: 725, `3`: 376 | 0 | Ordinal/categorical education tier. |

## 4. Anthropometric & Lifestyle Variables

| Column | Type | Observed Range / Counts | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `BMI` | Float | `15.03` – `40.00` (mean `27.69`) | 0 | Body Mass Index ($\text{kg/m}^2$). |
| `Smoking` | Binary (0/1) | `0`: 1,350, `1`: 529 | 0 | Smoking status (`0` = No, `1` = Yes). |
| `AlcoholConsumption` | Float | `0.00` – `20.00` (mean `10.10`) | 0 | Continuous alcohol consumption index/units. |
| `PhysicalActivity` | Float | `0.00` – `9.99` (mean `5.20`) | 0 | Continuous physical activity score (`0–10` scale). |
| `DietQuality` | Float | `0.00` – `10.00` (mean `4.90`) | 0 | Continuous diet quality score (`0–10` scale). |
| `SleepQuality` | Float | `4.00` – `9.99` (mean `7.02`) | 0 | Continuous sleep quality score (`4–10` scale). |

## 5. Medical History & Comorbidities

| Column | Type | Observed Counts | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `FamilyHistoryDiabetes` | Binary (0/1) | `0`: 1,431, `1`: 448 | 0 | Family history of diabetes. |
| `GestationalDiabetes` | Binary (0/1) | `0`: 1,692, `1`: 187 | 0 | **Quality note:** `1` appears in both `Gender=0` (`89`) and `Gender=1` (`98`). |
| `PolycysticOvarySyndrome` | Binary (0/1) | `0`: 1,795, `1`: 84 | 0 | **Quality note:** `1` appears in both `Gender=0` (`42`) and `Gender=1` (`42`). |
| `PreviousPreDiabetes` | Binary (0/1) | `0`: 1,590, `1`: 289 | 0 | Prior pre-diabetes history. |
| `Hypertension` | Binary (0/1) | `0`: 1,591, `1`: 288 | 0 | Hypertension diagnosis indicator. |

## 6. Vital Signs & Clinical Laboratory Measurements

| Column | Type | Observed Range | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `SystolicBP` | Integer | `90` – `179` (mean `134.05`) | 0 | Systolic blood pressure (mmHg). |
| `DiastolicBP` | Integer | `60` – `119` (mean `89.86`) | 0 | **Quality note:** `158` rows have `DiastolicBP >= SystolicBP`. |
| `FastingBloodSugar` | Float | `70.07` – `199.94` (mean `135.20`) | 0 | Fasting blood glucose (mg/dL); direct diagnostic marker. |
| `HbA1c` | Float | `4.00` – `9.99` (mean `6.98`) | 0 | Glycated hemoglobin (%); direct diagnostic marker. |
| `SerumCreatinine` | Float | `0.50` – `4.99` (mean `2.78`) | 0 | Kidney function marker (mg/dL). |
| `BUNLevels` | Float | `5.01` – `49.98` (mean `27.80`) | 0 | Blood Urea Nitrogen (mg/dL). |
| `CholesterolTotal` | Float | `150.06` – `300.00` (mean `225.01`) | 0 | Total cholesterol (mg/dL). |
| `CholesterolLDL` | Float | `50.06` – `199.90` (mean `124.66`) | 0 | LDL cholesterol (mg/dL). |
| `CholesterolHDL` | Float | `20.01` – `99.96` (mean `60.06`) | 0 | HDL cholesterol (mg/dL). |
| `CholesterolTriglycerides` | Float | `50.15` – `399.89` (mean `227.39`) | 0 | Triglycerides (mg/dL). |

## 7. Medications

| Column | Type | Observed Counts | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `AntihypertensiveMedications` | Binary (0/1) | `0`: 1,342, `1`: 537 | 0 | Blood-pressure medication use. |
| `Statins` | Binary (0/1) | `0`: 1,120, `1`: 759 | 0 | Lipid-lowering statin medication use. |
| `AntidiabeticMedications` | Binary (0/1) | `0`: 1,356, `1`: 523 | 0 | Diabetes medication use (`309` with `Diagnosis=0`, `214` with `Diagnosis=1`). |

## 8. Symptoms & Quality of Life

| Column | Type | Observed Range / Counts | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `FrequentUrination` | Binary (0/1) | `0`: 1,508, `1`: 371 | 0 | Classic diabetes symptom. |
| `ExcessiveThirst` | Binary (0/1) | `0`: 1,516, `1`: 363 | 0 | Classic diabetes symptom. |
| `UnexplainedWeightLoss` | Binary (0/1) | `0`: 1,673, `1`: 206 | 0 | Symptom indicator. |
| `FatigueLevels` | Float | `0.01` – `10.00` (mean `4.95`) | 0 | Self-reported fatigue score (`0–10`). |
| `BlurredVision` | Binary (0/1) | `0`: 1,700, `1`: 179 | 0 | Symptom indicator. |
| `SlowHealingSores` | Binary (0/1) | `0`: 1,686, `1`: 193 | 0 | Symptom indicator. |
| `TinglingHandsFeet` | Binary (0/1) | `0`: 1,670, `1`: 209 | 0 | Neuropathy-related symptom indicator. |
| `QualityOfLifeScore` | Float | `0.00` – `99.79` (mean `48.51`) | 0 | Overall quality-of-life score (`0–100`). |

## 9. Environmental Exposures & Healthcare Behavior

| Column | Type | Observed Range / Counts | Missing | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `HeavyMetalsExposure` | Binary (0/1) | `0`: 1,781, `1`: 98 | 0 | Environmental heavy-metal exposure indicator. |
| `OccupationalExposureChemicals` | Binary (0/1) | `0`: 1,685, `1`: 194 | 0 | Workplace chemical exposure indicator. |
| `WaterQuality` | Binary (0/1) | `0`: 1,502, `1`: 377 | 0 | Water quality indicator (`0`/`1`). |
| `MedicalCheckupsFrequency` | Float | `0.00` – `4.00` (mean `2.00`) | 0 | Annual/periodic checkup frequency score. |
| `MedicationAdherence` | Float | `0.00` – `10.00` (mean `4.96`) | 0 | Medication adherence score (`0–10`). |
| `HealthLiteracy` | Float | `0.00` – `9.99` (mean `5.01`) | 0 | Health literacy score (`0–10`). |
