from pydantic import BaseModel, Field


class TaskSpecificationCheckOutput(BaseModel):
    """Pydantic model for task_specification_check node outputs."""
    task_name_is_valid: bool = Field(..., description="Whether the task name matches the input task name")


class TaskDescriptionExtractionOutput(BaseModel):
    """Pydantic model for task_description_extraction node outputs."""
    task_description: str = Field(..., description="The extracted task description")


def task_description_extraction(task_specification_check_input: TaskSpecificationCheckOutput, **kwargs) -> TaskDescriptionExtractionOutput:
    """Extract the task description from the input task name

    Args:
        task_specification_check_input: Input from the 'task_specification_check' node.
        **kwargs: Additional keyword arguments.

    Returns:
        TaskDescriptionExtractionOutput: Object containing outputs for this node.
    """
    # Validate input task name is valid before proceeding
    if not task_specification_check_input.task_name_is_valid:
        raise ValueError("Cannot extract description from invalid task name")

    # Get the raw task description from kwargs
    raw_text: str = __extract_raw_task_text(kwargs=kwargs)

    # Clean and normalize the task description
    normalized_text: str = __normalize_task_text(text=raw_text)

    # Extract the relevant task description portions
    task_description: str = __extract_task_description(text=normalized_text)

    # Format the final description
    formatted_description: str = __format_description(description=task_description)

    return TaskDescriptionExtractionOutput(
        task_description=formatted_description
    )