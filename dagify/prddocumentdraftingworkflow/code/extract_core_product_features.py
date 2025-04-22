from pydantic import BaseModel, Field
from typing import List


class ExtractObjectivesFromWorkflowRequirementsOutput(BaseModel):
    """Pydantic model for extract_objectives_from_workflow_requirements node outputs."""
    objectives: List[str] = Field(..., description="A list of explicit and implicit objectives that the PRD must address, each as a clearly stated goal.")


class ExtractCoreProductFeaturesOutput(BaseModel):
    """Pydantic model for extract_core_product_features node outputs."""
    core_product_features: List[str] = Field(..., description="A list of singular, succinct descriptions of each core product feature required to achieve the stated objectives.")


def extract_core_product_features_fx(extract_objectives_from_workflow_requirements_input: ExtractObjectivesFromWorkflowRequirementsOutput, **kwargs) -> ExtractCoreProductFeaturesOutput:
    """Identify and list all core product features needed to satisfy the workflow requirements.

    Args:
        extract_objectives_from_workflow_requirements_input: Input from the 'extract_objectives_from_workflow_requirements' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ExtractCoreProductFeaturesOutput: Object containing outputs for this node.
    """
    pass