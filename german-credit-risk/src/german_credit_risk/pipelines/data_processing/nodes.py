"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.2.0
"""
import pandas as pd

def preprocess_german_credit(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma os códigos enigmáticos da base alemã em labels legíveis,
    facilitando o EDA e a interpretação do modelo de risco.
    """
    
    mappings = {
        "status_checking": {
            "A11": "< 0 DM",
            "A12": "0 <= ... < 200 DM",
            "A13": ">= 200 DM / salary assignments",
            "A14": "no checking account"
        },
        "credit_history": {
            "A30": "no credits taken/all paid duly",
            "A31": "all credits at this bank paid duly",
            "A32": "existing credits paid duly till now",
            "A33": "delay in paying off in the past",
            "A34": "critical account/other credits existing"
        },
        "purpose": {
            "A40": "car (new)", "A41": "car (used)", "A42": "furniture/equipment",
            "A43": "radio/television", "A44": "domestic appliances", "A45": "repairs",
            "A46": "education", "A48": "retraining", "A49": "business", "A410": "others"
        },
        "savings": {
            "A61": "< 100 DM", "A62": "100 <= ... < 500 DM",
            "A63": "500 <= ... < 1000 DM", "A64": ">= 1000 DM",
            "A65": "unknown/no savings account"
        },
        "employment_since": {
            "A71": "unemployed", "A72": "< 1 year", "A73": "1 <= ... < 4 years",
            "A74": "4 <= ... < 7 years", "A75": ">= 7 years"
        },
        "personal_status": {
            "A91": "male: divorced/separated", "A92": "female: divorced/separated/married",
            "A93": "male: single", "A94": "male: married/widowed", "A95": "female: single"
        },
        "other_debtors": {
            "A101": "none", "A102": "co-applicant", "A103": "guarantor"
        },
        "property": {
            "A121": "real estate", "A122": "building society savings/life insurance",
            "A123": "car or other", "A124": "unknown/no property"
        },
        "other_installment_plans": {
            "A141": "bank", "A142": "stores", "A143": "none"
        },
        "housing": {
            "A151": "rent", "A152": "own", "A153": "for free"
        },
        "job": {
            "A171": "unemployed/unskilled non-resident", "A172": "unskilled resident",
            "A173": "skilled employee", "A174": "management/highly qualified"
        },
        "telephone": {
            "A191": "none", "A192": "yes"
        },
        "foreign_worker": {
            "A201": "yes", "A202": "no"
        }
    }

    # Aplicando os mapeamentos de forma iterativa
    for column, mapping in mappings.items():
        if column in data.columns:
            data[column] = data[column].map(mapping)
    
    # Ajustando o Target: 1 (Bom) -> 0 | 2 (Ruim) -> 1
    data["credit_risk"] = data["credit_risk"].replace({1: 0, 2: 1})
    
    return data