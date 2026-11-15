-- 01_database_setup.sql
-- Purpose: Define the relational schema for diabetes_data.csv (46 columns).
-- Compatible with PostgreSQL (adapt COPY path or import via your SQL client).

DROP TABLE IF EXISTS diabetes_patients;

CREATE TABLE diabetes_patients (
    patient_id                        INTEGER PRIMARY KEY,
    age                               INTEGER NOT NULL CHECK (age BETWEEN 0 AND 120),
    gender                            SMALLINT NOT NULL CHECK (gender IN (0, 1)),
    ethnicity                         SMALLINT NOT NULL CHECK (ethnicity BETWEEN 0 AND 3),
    socioeconomic_status              SMALLINT NOT NULL CHECK (socioeconomic_status BETWEEN 0 AND 2),
    education_level                   SMALLINT NOT NULL CHECK (education_level BETWEEN 0 AND 3),
    bmi                               NUMERIC(10, 6) NOT NULL CHECK (bmi > 0),
    smoking                           SMALLINT NOT NULL CHECK (smoking IN (0, 1)),
    alcohol_consumption               NUMERIC(10, 6) NOT NULL CHECK (alcohol_consumption >= 0),
    physical_activity                 NUMERIC(10, 6) NOT NULL CHECK (physical_activity >= 0),
    diet_quality                      NUMERIC(10, 6) NOT NULL CHECK (diet_quality >= 0),
    sleep_quality                     NUMERIC(10, 6) NOT NULL CHECK (sleep_quality >= 0),
    family_history_diabetes           SMALLINT NOT NULL CHECK (family_history_diabetes IN (0, 1)),
    gestational_diabetes              SMALLINT NOT NULL CHECK (gestational_diabetes IN (0, 1)),
    polycystic_ovary_syndrome         SMALLINT NOT NULL CHECK (polycystic_ovary_syndrome IN (0, 1)),
    previous_pre_diabetes             SMALLINT NOT NULL CHECK (previous_pre_diabetes IN (0, 1)),
    hypertension                      SMALLINT NOT NULL CHECK (hypertension IN (0, 1)),
    systolic_bp                       INTEGER NOT NULL CHECK (systolic_bp > 0),
    diastolic_bp                      INTEGER NOT NULL CHECK (diastolic_bp > 0),
    fasting_blood_sugar               NUMERIC(10, 6) NOT NULL CHECK (fasting_blood_sugar > 0),
    hba1c                             NUMERIC(10, 6) NOT NULL CHECK (hba1c > 0),
    serum_creatinine                  NUMERIC(10, 6) NOT NULL CHECK (serum_creatinine > 0),
    bun_levels                        NUMERIC(10, 6) NOT NULL CHECK (bun_levels > 0),
    cholesterol_total                 NUMERIC(10, 6) NOT NULL CHECK (cholesterol_total > 0),
    cholesterol_ldl                   NUMERIC(10, 6) NOT NULL CHECK (cholesterol_ldl > 0),
    cholesterol_hdl                   NUMERIC(10, 6) NOT NULL CHECK (cholesterol_hdl > 0),
    cholesterol_triglycerides         NUMERIC(10, 6) NOT NULL CHECK (cholesterol_triglycerides > 0),
    antihypertensive_medications      SMALLINT NOT NULL CHECK (antihypertensive_medications IN (0, 1)),
    statins                           SMALLINT NOT NULL CHECK (statins IN (0, 1)),
    antidiabetic_medications          SMALLINT NOT NULL CHECK (antidiabetic_medications IN (0, 1)),
    frequent_urination                SMALLINT NOT NULL CHECK (frequent_urination IN (0, 1)),
    excessive_thirst                  SMALLINT NOT NULL CHECK (excessive_thirst IN (0, 1)),
    unexplained_weight_loss           SMALLINT NOT NULL CHECK (unexplained_weight_loss IN (0, 1)),
    fatigue_levels                    NUMERIC(10, 6) NOT NULL CHECK (fatigue_levels >= 0),
    blurred_vision                    SMALLINT NOT NULL CHECK (blurred_vision IN (0, 1)),
    slow_healing_sores                SMALLINT NOT NULL CHECK (slow_healing_sores IN (0, 1)),
    tingling_hands_feet               SMALLINT NOT NULL CHECK (tingling_hands_feet IN (0, 1)),
    quality_of_life_score             NUMERIC(10, 6) NOT NULL,
    heavy_metals_exposure             SMALLINT NOT NULL CHECK (heavy_metals_exposure IN (0, 1)),
    occupational_exposure_chemicals   SMALLINT NOT NULL CHECK (occupational_exposure_chemicals IN (0, 1)),
    water_quality                     SMALLINT NOT NULL CHECK (water_quality IN (0, 1)),
    medical_checkups_frequency        NUMERIC(10, 6) NOT NULL CHECK (medical_checkups_frequency >= 0),
    medication_adherence              NUMERIC(10, 6) NOT NULL CHECK (medication_adherence >= 0),
    health_literacy                   NUMERIC(10, 6) NOT NULL CHECK (health_literacy >= 0),
    diagnosis                         SMALLINT NOT NULL CHECK (diagnosis IN (0, 1)),
    doctor_in_charge                  VARCHAR(50) NOT NULL
);

-- Example PostgreSQL bulk load (run from psql with appropriate local file path):
-- \copy diabetes_patients FROM 'data/raw/diabetes_data.csv' WITH (FORMAT csv, HEADER true);
