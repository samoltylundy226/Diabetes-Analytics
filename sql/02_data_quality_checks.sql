-- 02_data_quality_checks.sql
-- Purpose: Audit completeness, uniqueness, constant fields, and clinical validity.

-- 1. Row count and distinct patient_id check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT patient_id) AS unique_patients,
    COUNT(*) - COUNT(DISTINCT patient_id) AS duplicate_patient_ids
FROM diabetes_patients;

-- 2. Missing value audit across key analytical columns
SELECT
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS null_age,
    SUM(CASE WHEN bmi IS NULL THEN 1 ELSE 0 END) AS null_bmi,
    SUM(CASE WHEN fasting_blood_sugar IS NULL THEN 1 ELSE 0 END) AS null_fbs,
    SUM(CASE WHEN hba1c IS NULL THEN 1 ELSE 0 END) AS null_hba1c,
    SUM(CASE WHEN systolic_bp IS NULL THEN 1 ELSE 0 END) AS null_sbp,
    SUM(CASE WHEN diastolic_bp IS NULL THEN 1 ELSE 0 END) AS null_dbp,
    SUM(CASE WHEN diagnosis IS NULL THEN 1 ELSE 0 END) AS null_diagnosis
FROM diabetes_patients;

-- 3. Constant / zero-variance column check (DoctorInCharge)
SELECT
    doctor_in_charge,
    COUNT(*) AS record_count
FROM diabetes_patients
GROUP BY doctor_in_charge;

-- 4. Clinical blood pressure consistency check (DiastolicBP should be < SystolicBP)
SELECT
    COUNT(*) AS invalid_bp_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM diabetes_patients), 2) AS invalid_bp_pct
FROM diabetes_patients
WHERE diastolic_bp >= systolic_bp;

-- 5. Sex-specific medical history anomaly check (GestationalDiabetes & PCOS by Gender)
SELECT
    gender,
    SUM(CASE WHEN gestational_diabetes = 1 THEN 1 ELSE 0 END) AS gestational_diabetes_cases,
    SUM(CASE WHEN polycystic_ovary_syndrome = 1 THEN 1 ELSE 0 END) AS pcos_cases
FROM diabetes_patients
GROUP BY gender
ORDER BY gender;

-- 6. Target class distribution and antidiabetic medication cross-check
SELECT
    diagnosis,
    antidiabetic_medications,
    COUNT(*) AS patient_count
FROM diabetes_patients
GROUP BY diagnosis, antidiabetic_medications
ORDER BY diagnosis, antidiabetic_medications;
