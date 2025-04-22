from pydantic import BaseModel, Field
from typing import List


class IdentifyPrimaryUserRolesOutput(BaseModel):
    """Pydantic model for identify_primary_user_roles node outputs."""
    user_role_names: List[str] = Field(..., description="List of primary user role or persona names directly involved with the product.")
    user_role_descriptions: List[str] = Field(..., description="List of concise one-sentence descriptions for each user role, matched by index to user_role_names.")


class DraftPrdSectionUserRolesOutput(BaseModel):
    """Pydantic model for draft_prd_section_user_roles node outputs."""
    role_names: List[str] = Field(..., description="List of user role or persona names included in the PRD section")
    role_descriptions: List[str] = Field(..., description="List of brief descriptions for each user role or persona, matching the order of role_names")
    section_text: str = Field(..., description="The full 'User Roles & Personas' section as formatted text for the PRD")


def draft_prd_section_user_roles_fx(identify_primary_user_roles_input: IdentifyPrimaryUserRolesOutput, **kwargs) -> DraftPrdSectionUserRolesOutput:
    """Format the identified user roles as the 'User Roles & Personas' section for the PRD.

    Args:
        identify_primary_user_roles_input: Input from the 'identify_primary_user_roles' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DraftPrdSectionUserRolesOutput: Object containing outputs for this node.
    """
    pass