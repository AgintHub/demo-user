from pydantic import BaseModel, Field


class TaskDescriptionExtractionOutput(BaseModel):
    """Pydantic model for task_description_extraction node outputs."""
    task_description: str = Field(..., description="The extracted task description")


class DecompositionRequestOutput(BaseModel):
    """Pydantic model for decomposition_request node outputs."""
    task_id: str = Field(..., description="Unique identifier for the task")
    task_description: str = Field(..., description="Description of the task")
    decomposition_result: str = Field(..., description="List of possible decompositions for the task")


def decomposition_request(task_description_extraction_input: TaskDescriptionExtractionOutput, **kwargs) -> DecompositionRequestOutput:
    """Request the Elemental Thoughts decomposition of the task

    Args:
        task_description_extraction_input: Input from the 'task_description_extraction' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DecompositionRequestOutput: Object containing outputs for this node.
    """
    # Generate unique task ID
    task_id: str = __generate_task_id()
    
    # Extract task description from input
    task_description: str = task_description_extraction_input.task_description
    
    # Request decomposition from service
    decomposition_result: str = __request_task_decomposition(
        task_description=task_description,
        task_id=task_id
    )
    
    # Validate and format the decomposition results
    formatted_result: str = __format_decomposition_result(decomposition_result)

    return DecompositionRequestOutput(
        task_id=task_id,
        task_description=task_description,
        decomposition_result=formatted_result
    )