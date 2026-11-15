-- 03_healthcare_analysis.sql
-- Purpose: Analyze factors associated with existing diabetes Diagnosis.
-- Note: Results reflect cross-sectional associations, not future risk predictions.

-- 1. Overall diagnosis prevalence
SELECT
    diagnosis,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM diabetes_patients
GROUP BY diagnosis
ORDER BY diagnosis;

-- 2. Diagnosis rate by age group
SELECT
    CASE
        WHEN age < 35 THEN '20-34'
        WHEN age BETWEEN 35 AND 49 THEN '35-49'
        WHEN age BETWEEN 50 AND 64 THEN '50-64'
        ELSE '65+'
    END AS age_band,
    COUNT(*) AS total_patients,
    SUM(diagnosis) AS diagnosed_cases,
    ROUND(100.0 * AVG(diagnosis), 2) AS diagnosis_rate_pct
FROM diabetes_patients
GROUP BY age_band
ORDER BY age_band;

-- 3. Diagnosis rate by clinical BMI category
SELECT
    CASE
        WHEN bmi < 18.5 THEN 'Underweight (<18.5)'
        WHEN bmi < 25.0 THEN 'Normal (18.5-24.9)'
        WHEN bmi < 30.0 THEN 'Overweight (25.0-29.9)'
        ELSE 'Obese (>=30.0)'
    END AS bmi_category,
    COUNT(*) AS total_patients,
    SUM(diagnosis) AS diagnosed_cases,
    ROUND(100.0 * AVG(diagnosis), 2) AS diagnosis_rate_pct
FROM diabetes_patients
GROUP BY bmi_category
ORDER BY diagnosis_rate_pct DESC;

-- 4. Average clinical biomarkers by diagnosis status
SELECT
    diagnosis,
    ROUND(AVG(bmi), 2) AS avg_bmi,
    ROUND(AVG(fasting_blood_sugar), 2) AS avg_fasting_blood_sugar,
    ROUND(AVG(hba1c), 2) AS avg_hba1c,
    ROUND(AVG(systolic_bp), 2) AS avg_systolic_bp,
    ROUND(AVG(cholesterol_triglycerides), 2) AS avg_triglycerides,
    ROUND(AVG(quality_of_life_score), 2) AS avg_qol_score
FROM diabetes_patients
GROUP BY diagnosis
ORDER BY diagnosis;

-- 5. Diagnosis rate across HbA1c clinical thresholds
SELECT
    CASE
        WHEN hba1c < 5.7 THEN 'Normal (<5.7%)'
        WHEN hba1c < 6.5 THEN 'Prediabetes Range (5.7-6.4%)'
        ELSE 'Diabetes Range (>=6.5%)'
    END AS hba1c_band,
    COUNT(*) AS total_patients,
    SUM(diagnosis) AS diagnosed_cases,
    ROUND(100.0 * AVG(diagnosis), 2) AS diagnosis_rate_pct
FROM diabetes_patients
GROUP BY hba1c_band
ORDER BY MIN(hba1c);

-- 6. Symptom prevalence comparison between diagnosed and non-diagnosed patients
SELECT
    diagnosis,
    ROUND(100.0 * AVG(frequent_urination), 2) AS frequent_urination_pct,
    ROUND(100.0 * AVG(excessive_thirst), 2) AS excessive_thirst_pct,
    ROUND(100.0 * AVG(blurred_vision), 2) AS blurred_vision_pct,
    ROUND(100.0 * AVG(slow_healing_sores), 2) AS slow_healing_sores_pct,
    ROUND(100.0 * AVG(tingling_hands_feet), 2) AS tingling_hands_feet_pct
FROM diabetes_patients
GROUP BY diagnosis
ORDER BY diagnosis;

-- 7. Lifestyle and socioeconomic averages by diagnosis status
SELECT
    socioeconomic_status,
    COUNT(*) AS total_patients,
    ROUND(100.0 * AVG(diagnosis), 2) AS diagnosis_rate_pct,
    ROUND(AVG(physical_activity), 2) AS avg_physical_activity,
    ROUND(AVG(diet_quality), 2) AS avg_diet_quality,
    ROUND(AVG(health_literacy), 2) AS avg_health_literacy
FROM diabetes_patients
GROUP BY socioeconomic_status
ORDER BY socioeconomic_status;
