from pydantic import BaseModel, Field
from typing import List


class SummarizeKeyStakeholdersOutput(BaseModel):
    """Pydantic model for summarize_key_stakeholders node outputs."""
    stakeholder_names: List[str] = Field(..., description="List of key stakeholder names.")
    stakeholder_roles: List[str] = Field(..., description="List of brief descriptions of each stakeholder's role.")
    stakeholder_interests: List[str] = Field(..., description="List of brief descriptions of each stakeholder's interest in the project outcome.")


class DraftPrdSectionStakeholdersOutput(BaseModel):
    """Pydantic model for draft_prd_section_stakeholders node outputs."""
    stakeholder_names: List[str] = Field(..., description="List of the stakeholder names or titles included in the PRD Stakeholders section.")
    stakeholder_roles: List[str] = Field(..., description="List of short descriptions for each stakeholder's role in the project. Aligned by index with stakeholder_names.")
    stakeholder_significance: List[str] = Field(..., description="List of brief statements of each stakeholder's significance or interest in the project outcome. Aligned by index with stakeholder_names.")
    prd_stakeholders_section_text: str = Field(..., description="The fully formatted 'Stakeholders' section text, ready to be inserted directly into the PRD document.")


def draft_prd_section_stakeholders_fx(summarize_key_stakeholders_input: SummarizeKeyStakeholdersOutput, **kwargs) -> DraftPrdSectionStakeholdersOutput:
    """Format the stakeholder summaries into a PRD 'Stakeholders' section.

    Args:
        summarize_key_stakeholders_input: Input from the 'summarize_key_stakeholders' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DraftPrdSectionStakeholdersOutput: Object containing outputs for this node.
    """
    pass