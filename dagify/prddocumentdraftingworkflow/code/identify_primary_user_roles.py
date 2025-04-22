from pydantic import BaseModel, Field
from typing import List


class IdentifyPrimaryUserRolesOutput(BaseModel):
    """Pydantic model for identify_primary_user_roles node outputs."""
    user_role_names: List[str] = Field(..., description="List of primary user role or persona names directly involved with the product.")
    user_role_descriptions: List[str] = Field(..., description="List of concise one-sentence descriptions for each user role, matched by index to user_role_names.")


def identify_primary_user_roles_fx(general_input: str, **kwargs) -> IdentifyPrimaryUserRolesOutput:
    """Extract the main user roles or personas directly involved with the product based on the requirements.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        IdentifyPrimaryUserRolesOutput: Object containing outputs for this node.
    """
    pass