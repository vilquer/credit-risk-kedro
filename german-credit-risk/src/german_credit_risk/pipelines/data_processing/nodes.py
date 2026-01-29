"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.2.0
"""
import pandas as pd

def preprocess_german_credit(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma os códigos originais (ex: A11, A12) em labels legíveis
    e ajusta o target (credit_risk) para o padrão 0 (Bom) e 1 (Ruim).
    """
    
    # Exemplo de mapeamento (ajuste conforme o german.doc se necessário)
    mapping_status = {
        "A11": "< 0 DM",
        "A12": "0 <= ... < 200 DM",
        "A13": ">= 200 DM / salary assignments",
        "A14": "no checking account"
    }
    
    # Aplicando mapeamentos básicos para as colunas principais
    data["status_checking"] = data["status_checking"].map(mapping_status)
    
    # Ajustando o Target: Na base original 1=Bom, 2=Ruim. 
    # Em modelos de Risco, o padrão é 0=Bom, 1=Ruim (Default).
    data["credit_risk"] = data["credit_risk"].replace({1: 0, 2: 1})
    
    return data