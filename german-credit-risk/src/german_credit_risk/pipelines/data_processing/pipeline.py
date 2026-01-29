"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.2.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import preprocess_german_credit

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_german_credit,
                inputs="german_credit_raw",
                outputs="german_credit_intermediate",
                name="preprocess_german_credit_node",
            ),
        ]
    )