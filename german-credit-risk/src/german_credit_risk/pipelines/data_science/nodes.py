"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.2.0
"""
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from typing import Dict, Tuple

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score



def calculate_iv_report(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    Calcula o Information Value (IV) para todas as variáveis do dataset.
    """
    iv_list = []
    features = [col for col in df.columns if col != target]
    
    for feature in features:
        # Binning simplificado para variáveis numéricas
        temp_df = df.copy()
        if temp_df[feature].dtype != 'object':
            temp_df[feature] = pd.qcut(temp_df[feature], q=5, duplicates='drop').astype(str)
        
        stats = temp_df.groupby(feature)[target].agg(['count', 'sum'])
        stats.columns = ['Total', 'Bad']
        stats['Good'] = stats['Total'] - stats['Bad']
        
        perc_bad = (stats['Bad'] + 0.5) / (stats['Bad'].sum() + 0.5)
        perc_good = (stats['Good'] + 0.5) / (stats['Good'].sum() + 0.5)
        
        stats['WoE'] = np.log(perc_good / perc_bad)
        stats['IV'] = (perc_good - perc_bad) * stats['WoE']
        iv_list.append({'Feature': feature, 'IV': stats['IV'].sum()})

    report_df = pd.DataFrame(iv_list).sort_values(by='IV', ascending=False)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Top 3 Features por IV: \n{report_df.head(3)}")
    
    return report_df

def select_features_by_iv(data: pd.DataFrame, iv_summary: pd.DataFrame, threshold: float = 0.02) -> pd.DataFrame:
    """
    Filtra as colunas do dataset intermediate com base no Information Value (IV).
    Gera a camada 'primary'.
    """
    logger = logging.getLogger(__name__)
    
    # Ajuste aqui: Mudamos 'Variable' para 'Feature' para bater com o nó anterior
    significant_features = iv_summary[iv_summary["IV"] > threshold]["Feature"].unique().tolist()
    
    # Garantir que o alvo (credit_risk) permaneça no dataset
    target = "credit_risk"
    if target not in significant_features:
        cols_to_keep = [target] + significant_features
    else:
        cols_to_keep = significant_features
        
    logger.info(f"Selecionadas {len(significant_features)} features com IV > {threshold}")
    
    return data[cols_to_keep]



def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    """
    Divide os dados em conjuntos de treino e teste.
    
    Args:
        data: Dados da camada primary (após feature selection).
        parameters: Dicionário contendo 'test_size' e 'random_state'.
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    X = data.drop(columns="credit_risk")
    y = data["credit_risk"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=parameters["test_size"], 
        random_state=parameters["random_state"]
    )
    
    return X_train, X_test, y_train, y_test


def create_model_input_table(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma variáveis categóricas em dummies para que o modelo 
    consiga processar os dados (resolvendo o erro de conversão de string).
    """
    # Identifica colunas que são texto (object)
    categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
    
    # Cria as dummies (One-Hot Encoding)
    # drop_first=True evita a colinearidade (importante para modelos lineares)
    data_with_dummies = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
    
    return data_with_dummies


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Treina o modelo de Random Forest."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series):
    """Calcula métricas de performance de risco (Gini e AUC)."""
    logger = logging.getLogger(__name__)
    
    # Probabilidades para a classe positiva (Mau Pagador)
    y_probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_probs)
    gini = 2 * auc - 1
    
    logger.info(f"Model AUC: {auc:.4f}")
    logger.info(f"Model GINI: {gini:.4f}")
    
    return gini