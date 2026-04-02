import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH  = os.path.join(BASE_DIR, 'ml_models', 'modele_logistic_regression.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'ml_models', 'scaler.pkl')

# Ordre exact des 44 colonnes (identique à l'entraînement)
FEATURE_COLUMNS = [
    'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
    'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome',
    'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
    'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears',
    'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
    'YearsSinceLastPromotion', 'YearsWithCurrManager',
    'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
    'Department_Research & Development', 'Department_Sales',
    'EducationField_Life Sciences', 'EducationField_Marketing', 'EducationField_Medical',
    'EducationField_Other', 'EducationField_Technical Degree',
    'Gender_Male',
    'JobRole_Human Resources', 'JobRole_Laboratory Technician', 'JobRole_Manager',
    'JobRole_Manufacturing Director', 'JobRole_Research Director', 'JobRole_Research Scientist',
    'JobRole_Sales Executive', 'JobRole_Sales Representative',
    'MaritalStatus_Married', 'MaritalStatus_Single',
    'OverTime_Yes',
]

try:
    _model  = joblib.load(MODEL_PATH)
    _scaler = joblib.load(SCALER_PATH)
    MODEL_LOADED = True
except Exception as e:
    _model = _scaler = None
    MODEL_LOADED = False
    print(f"Modèle ML non chargé: {e}")


def build_features(data: dict) -> pd.DataFrame:
    """
    Construit un DataFrame d'une ligne avec les 44 colonnes exactes.
    data: dict avec les valeurs brutes du formulaire.
    """
    row = {}

    # ── Numériques ─────────────────────────────────────────
    row['Age']                      = int(data.get('Age', 30))
    row['DailyRate']                = int(data.get('DailyRate', 800))
    row['DistanceFromHome']         = int(data.get('DistanceFromHome', 5))
    row['Education']                = int(data.get('Education', 3))
    row['EnvironmentSatisfaction']  = int(data.get('EnvironmentSatisfaction', 3))
    row['HourlyRate']               = int(data.get('HourlyRate', 66))
    row['JobInvolvement']           = int(data.get('JobInvolvement', 3))
    row['JobLevel']                 = int(data.get('JobLevel', 2))
    row['JobSatisfaction']          = int(data.get('JobSatisfaction', 3))
    row['MonthlyIncome']            = int(data.get('MonthlyIncome', 6500))
    row['MonthlyRate']              = int(data.get('MonthlyRate', 14000))
    row['NumCompaniesWorked']       = int(data.get('NumCompaniesWorked', 2))
    row['PercentSalaryHike']        = int(data.get('PercentSalaryHike', 15))
    row['PerformanceRating']        = int(data.get('PerformanceRating', 3))
    row['RelationshipSatisfaction'] = int(data.get('RelationshipSatisfaction', 3))
    row['StockOptionLevel']         = int(data.get('StockOptionLevel', 1))
    row['TotalWorkingYears']        = int(data.get('TotalWorkingYears', 8))
    row['TrainingTimesLastYear']    = int(data.get('TrainingTimesLastYear', 3))
    row['WorkLifeBalance']          = int(data.get('WorkLifeBalance', 3))
    row['YearsAtCompany']           = int(data.get('YearsAtCompany', 5))
    row['YearsInCurrentRole']       = int(data.get('YearsInCurrentRole', 3))
    row['YearsSinceLastPromotion']  = int(data.get('YearsSinceLastPromotion', 1))
    row['YearsWithCurrManager']     = int(data.get('YearsWithCurrManager', 3))

    # ── Dummies BusinessTravel (ref: Non-Travel) ────────────
    bt = data.get('BusinessTravel', '')
    row['BusinessTravel_Travel_Frequently'] = 1 if bt == 'Travel_Frequently' else 0
    row['BusinessTravel_Travel_Rarely']     = 1 if bt == 'Travel_Rarely'     else 0

    # ── Dummies Department (ref: Human Resources) ───────────
    dept = data.get('Department', '')
    row['Department_Research & Development'] = 1 if dept == 'Research & Development' else 0
    row['Department_Sales']                  = 1 if dept == 'Sales'                  else 0

    # ── Dummies EducationField (ref: Human Resources) ───────
    ef = data.get('EducationField', '')
    row['EducationField_Life Sciences']    = 1 if ef == 'Life Sciences'    else 0
    row['EducationField_Marketing']        = 1 if ef == 'Marketing'        else 0
    row['EducationField_Medical']          = 1 if ef == 'Medical'          else 0
    row['EducationField_Other']            = 1 if ef == 'Other'            else 0
    row['EducationField_Technical Degree'] = 1 if ef == 'Technical Degree' else 0

    # ── Dummies Gender (ref: Female) ────────────────────────
    row['Gender_Male'] = 1 if data.get('Gender', '') == 'Male' else 0

    # ── Dummies JobRole (ref: Healthcare Representative) ────
    jr = data.get('JobRole', '')
    row['JobRole_Human Resources']        = 1 if jr == 'Human Resources'        else 0
    row['JobRole_Laboratory Technician']  = 1 if jr == 'Laboratory Technician'  else 0
    row['JobRole_Manager']                = 1 if jr == 'Manager'                else 0
    row['JobRole_Manufacturing Director'] = 1 if jr == 'Manufacturing Director' else 0
    row['JobRole_Research Director']      = 1 if jr == 'Research Director'      else 0
    row['JobRole_Research Scientist']     = 1 if jr == 'Research Scientist'     else 0
    row['JobRole_Sales Executive']        = 1 if jr == 'Sales Executive'        else 0
    row['JobRole_Sales Representative']   = 1 if jr == 'Sales Representative'   else 0

    # ── Dummies MaritalStatus (ref: Divorced) ───────────────
    ms = data.get('MaritalStatus', '')
    row['MaritalStatus_Married'] = 1 if ms == 'Married' else 0
    row['MaritalStatus_Single']  = 1 if ms == 'Single'  else 0

    # ── Dummies OverTime (ref: No) ──────────────────────────
    row['OverTime_Yes'] = 1 if data.get('OverTime', '') == 'Yes' else 0

    return pd.DataFrame([row])[FEATURE_COLUMNS]


def predict_attrition(data: dict):
    """
    Prédit si un employé va quitter l'entreprise.
    Retourne: (resultat_str, score_int, status_str)
    """
    if not MODEL_LOADED:
        raise FileNotFoundError(
            "Modèle introuvable. Placez modele_logistic_regression.pkl et scaler.pkl dans ml_models/"
        )

    df = build_features(data)
    X_scaled = _scaler.transform(df)
    prediction = _model.predict(X_scaled)[0]
    proba      = _model.predict_proba(X_scaled)[0]

    score = int(proba[1] * 100)   # probabilité de quitter en %

    if prediction == 1:
        return "Risque de Départ", score, "À surveiller"
    else:
        return "Reste dans l'entreprise", score, "Satisfaisant"
