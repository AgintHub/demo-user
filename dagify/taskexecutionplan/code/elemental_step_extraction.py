from pydantic import BaseModel, Field
from typing import List


class DecompositionRequestOutput(BaseModel):
    """Pydantic model for decomposition_request node outputs."""
    task_id: str = Field(..., description="Unique identifier for the task")
    task_description: str = Field(..., description="Description of the task")
    decomposition_result: str = Field(..., description="List of possible decompositions for the task")


class ElementalStepExtractionOutput(BaseModel):
    """Pydantic model for elemental_step_extraction node outputs."""
    fundamental_steps: List[str] = Field(..., description="List of extracted fundamental steps")


def elemental_step_extraction(decomposition_request_input: DecompositionRequestOutput, **kwargs) -> ElementalStepExtractionOutput:
    """Extract the fundamental steps from the Elemental Thoughts decomposition

    Args:
        decomposition_request_input: Input from the 'decomposition_request' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ElementalStepExtractionOutput: Object containing outputs for this node.
    """
    # Parse and clean the decomposition result
    cleaned_decomp: str = __clean_decomposition_text(
        text=decomposition_request_input.decomposition_result
    )
    
    # Extract individual steps from the cleaned decomposition
    raw_steps: List[str] = __extract_steps_from_text(text=cleaned_decomp)
    
    # Process and normalize the extracted steps
    normalized_steps: List[str] = __normalize_steps(steps=raw_steps)
    
    # Validate and filter the steps
    validated_steps: List[str] = __validate_fundamental_steps(steps=normalized_steps)

    return ElementalStepExtractionOutput(
        fundamental_steps=validated_steps
    )