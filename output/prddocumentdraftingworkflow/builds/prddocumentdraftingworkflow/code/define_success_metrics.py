from pydantic import BaseModel, Field
from typing import List


class ExtractObjectivesFromWorkflowRequirementsOutput(BaseModel):
    """Pydantic model for extract_objectives_from_workflow_requirements node outputs."""
    objectives: List[str] = Field(..., description="A list of explicit and implicit objectives that the PRD must address, each as a clearly stated goal.")


class DefineSuccessMetricsOutput(BaseModel):
    """Pydantic model for define_success_metrics node outputs."""
    metric_names: List[str] = Field(..., description="List of names or brief descriptions for each defined success metric.")
    metric_objective_mappings: List[str] = Field(..., description="For each metric, a string describing which objective(s) it maps to.")
    metric_quantifiability: List[bool] = Field(..., description="List indicating whether each success metric is quantifiable or objectively verifiable.")


def define_success_metrics_fx(extract_objectives_from_workflow_requirements_input: ExtractObjectivesFromWorkflowRequirementsOutput, **kwargs) -> DefineSuccessMetricsOutput:
    """Articulate measurable criteria for determining product success based on extracted objectives.

    Args:
        extract_objectives_from_workflow_requirements_input: Input from the 'extract_objectives_from_workflow_requirements' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineSuccessMetricsOutput: Object containing outputs for this node.
    """
    pass