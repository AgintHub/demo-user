from pydantic import BaseModel, Field


class TaskSpecificationCheckOutput(BaseModel):
    """Pydantic model for task_specification_check node outputs."""
    task_name_is_valid: bool = Field(..., description="Whether the task name matches the input task name")


def task_specification_check(general_input: str, **kwargs) -> TaskSpecificationCheckOutput:
    """Validate that the task name matches the input task name

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        TaskSpecificationCheckOutput: Object containing outputs for this node.
    """
    # Get the expected task name from configuration or kwargs
    expected_task_name: str = __get_expected_task_name(kwargs=kwargs)
    
    # Validate the input task name against expected
    is_valid: bool = __validate_task_name(
        input_name=general_input,
        expected_name=expected_task_name
    )
    
    # Return validation result
    return TaskSpecificationCheckOutput(
        task_name_is_valid=is_valid
    )