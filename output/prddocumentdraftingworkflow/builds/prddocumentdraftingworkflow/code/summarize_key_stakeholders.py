from pydantic import BaseModel, Field
from typing import List


class SummarizeKeyStakeholdersOutput(BaseModel):
    """Pydantic model for summarize_key_stakeholders node outputs."""
    stakeholder_names: List[str] = Field(..., description="List of key stakeholder names.")
    stakeholder_roles: List[str] = Field(..., description="List of brief descriptions of each stakeholder's role.")
    stakeholder_interests: List[str] = Field(..., description="List of brief descriptions of each stakeholder's interest in the project outcome.")


def summarize_key_stakeholders_fx(general_input: str, **kwargs) -> SummarizeKeyStakeholdersOutput:
    """Identify and summarize the interest and influence of key project stakeholders.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        SummarizeKeyStakeholdersOutput: Object containing outputs for this node.
    """
    pass