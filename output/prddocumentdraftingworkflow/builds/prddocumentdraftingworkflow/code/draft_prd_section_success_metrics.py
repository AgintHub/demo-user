from pydantic import BaseModel, Field
from typing import List


class DefineSuccessMetricsOutput(BaseModel):
    """Pydantic model for define_success_metrics node outputs."""
    metric_names: List[str] = Field(..., description="List of names or brief descriptions for each defined success metric.")
    metric_objective_mappings: List[str] = Field(..., description="For each metric, a string describing which objective(s) it maps to.")
    metric_quantifiability: List[bool] = Field(..., description="List indicating whether each success metric is quantifiable or objectively verifiable.")


class DraftPrdSectionSuccessMetricsOutput(BaseModel):
    """Pydantic model for draft_prd_section_success_metrics node outputs."""
    success_metrics_section_title: str = Field(..., description="The section heading for the success metrics in the PRD.")
    success_metrics_list: List[str] = Field(..., description="A list of strings, each describing a quantifiable or objectively verifiable success metric for the product.")


def draft_prd_section_success_metrics_fx(define_success_metrics_input: DefineSuccessMetricsOutput, **kwargs) -> DraftPrdSectionSuccessMetricsOutput:
    """Draft the 'Success Metrics' section for the PRD using the defined metrics.

    Args:
        define_success_metrics_input: Input from the 'define_success_metrics' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DraftPrdSectionSuccessMetricsOutput: Object containing outputs for this node.
    """
    pass