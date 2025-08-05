from pydantic import BaseModel, Field
from typing import List


class ElementalStepExtractionOutput(BaseModel):
    """Pydantic model for elemental_step_extraction node outputs."""
    fundamental_steps: List[str] = Field(..., description="List of extracted fundamental steps")


class DeterministicExecutableCodeGenerationOutput(BaseModel):
    """Pydantic model for deterministic_executable_code_generation node outputs."""
    fundamental_steps: List[str] = Field(..., description="List of executable code for each fundamental step")
    is_correct: List[bool] = Field(..., description="List of correctness indicators for each fundamental step")


def deterministic_executable_code_generation(elemental_step_extraction_input: ElementalStepExtractionOutput, **kwargs) -> DeterministicExecutableCodeGenerationOutput:
    """Generate executable code for each fundamental step

    Args:
        elemental_step_extraction_input: Input from the 'elemental_step_extraction' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DeterministicExecutableCodeGenerationOutput: Object containing outputs for this node.
    """
    executable_steps: List[str] = []
    correctness_flags: List[bool] = []

    for step in elemental_step_extraction_input.fundamental_steps:
        # Generate executable code for each fundamental step
        code: str = __generate_executable_code(step=step)
        executable_steps.append(code)

        # Validate the generated code
        is_valid: bool = __validate_code_correctness(code=code, original_step=step)
        correctness_flags.append(is_valid)

    return DeterministicExecutableCodeGenerationOutput(
        fundamental_steps=executable_steps,
        is_correct=correctness_flags
    )