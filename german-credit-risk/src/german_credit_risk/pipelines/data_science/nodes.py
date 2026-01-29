"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.2.0
"""
import pandas as pd
import numpy as np
import logging

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