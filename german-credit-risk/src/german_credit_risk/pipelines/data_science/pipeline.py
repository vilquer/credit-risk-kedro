"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.2.0
"""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import calculate_iv_report

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=calculate_iv_report,
                inputs=["german_credit_intermediate", "params:target_col"],
                outputs="iv_report",
                name="calculate_iv_report_node",
            ),
        ]
    )
