"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.2.0
"""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    calculate_iv_report, 
    select_features_by_iv, 
    create_model_input_table,
    split_data, 
    train_model, 
    evaluate_model
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            # Nó 1: Gera o relatório estatístico (IV)
            node(
                func=calculate_iv_report,
                inputs=["german_credit_intermediate", "params:target_col"],
                outputs="iv_report",
                name="calculate_iv_report_node",
            ),
            # Nó 2: Seleção de Features (Ainda com texto para facilitar a lógica)
            node(
                func=select_features_by_iv,
                inputs=["german_credit_intermediate", "iv_report", "params:iv_threshold"],
                outputs="german_credit_primary",
                name="select_features_node",
            ),
            # Nó 3: CONVERSÃO PARA DUMMIES (Agora sim, preparamos para o modelo)
            # Entrada: Texto -> Saída: Números
            node(
                func=create_model_input_table,
                inputs="german_credit_primary",
                outputs="german_credit_model_input",
                name="create_model_input_node",
            ),
            # Nó 4: SPLIT (Usando os dados numéricos já filtrados)
            node(
                func=split_data,
                inputs=["german_credit_model_input", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            # Nó 5: Treina o modelo
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="credit_risk_model",
                name="train_model_node",
            ),
            # Nó 6: Avalia o modelo
            node(
                func=evaluate_model,
                inputs=["credit_risk_model", "X_test", "y_test"],
                outputs="performance_metric",
                name="evaluate_model_node",
            ),
        ]
    )