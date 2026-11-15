# Project Overview

## Title
**Diabetes Healthcare Analytics: Patient Risk Factor Analysis and Machine Learning-Based Diagnosis Classification**

## Purpose
This project organizes an end-to-end healthcare analytics workflow covering data engineering, SQL quality auditing, exploratory data analysis, business intelligence preparation, and machine learning classification on `diabetes_data.csv`.

## Problem Framing
- The dataset captures **1,879 patient records** across **46 variables**, including a binary `Diagnosis` indicator (`0` = No Diabetes, `1` = Diabetes).
- Because records reflect **existing diagnosis status** without longitudinal follow-up timestamps, all supervised models are framed strictly as **cross-sectional diagnosis classification**, never future disease prediction.

## Stage 1 (Current Deliverables)
- Immutable raw data storage (`data/raw/diabetes_data.csv`) and complete 46-column schema documentation.
- Modular Python packages for validation, preprocessing, EDA, and ML training/evaluation.
- Educational Jupyter notebooks paired with markdown interpretations.
- PostgreSQL-compatible setup, quality-audit, and analytical SQL scripts.
- Unit tests (`tests/test_preprocessing.py`) and clean Git history.

## Stage 2 (Planned Execution)
- Generate and review full EDA figures and statistical subgroup summaries.
- Execute, tune, and compare ML models (including diagnostic-marker sensitivity runs and SHAP interpretability).
- Build interactive Power BI dashboards and publish screenshots in `powerbi/screenshots/`.
