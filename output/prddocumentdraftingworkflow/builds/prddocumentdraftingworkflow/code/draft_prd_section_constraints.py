from pydantic import BaseModel, Field
from typing import List


class ExtractCriticalConstraintsOutput(BaseModel):
    """Pydantic model for extract_critical_constraints node outputs."""
    constraints: List[str] = Field(..., description="Individual statements of technical, business, regulatory, or design constraints relevant to the product requirements.")


class DraftPrdSectionConstraintsOutput(BaseModel):
    """Pydantic model for draft_prd_section_constraints node outputs."""
    constraints_section_heading: str = Field(..., description="Section heading for the Constraints section in the PRD.")
    constraints_list: List[str] = Field(..., description="A list of formal, clearly stated constraints relevant to the product requirements.")


def draft_prd_section_constraints_fx(extract_critical_constraints_input: ExtractCriticalConstraintsOutput, **kwargs) -> DraftPrdSectionConstraintsOutput:
    """Format the extracted constraints into a 'Constraints' section for the PRD.

    Args:
        extract_critical_constraints_input: Input from the 'extract_critical_constraints' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DraftPrdSectionConstraintsOutput: Object containing outputs for this node.
    """
    pass