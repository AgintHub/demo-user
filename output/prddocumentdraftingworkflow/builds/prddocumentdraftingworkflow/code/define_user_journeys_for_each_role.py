from pydantic import BaseModel, Field
from typing import List


class IdentifyPrimaryUserRolesOutput(BaseModel):
    """Pydantic model for identify_primary_user_roles node outputs."""
    user_role_names: List[str] = Field(..., description="List of primary user role or persona names directly involved with the product.")
    user_role_descriptions: List[str] = Field(..., description="List of concise one-sentence descriptions for each user role, matched by index to user_role_names.")


class ExtractCoreProductFeaturesOutput(BaseModel):
    """Pydantic model for extract_core_product_features node outputs."""
    core_product_features: List[str] = Field(..., description="A list of singular, succinct descriptions of each core product feature required to achieve the stated objectives.")


class DefineUserJourneysForEachRoleOutput(BaseModel):
    """Pydantic model for define_user_journeys_for_each_role node outputs."""
    user_role_names: List[str] = Field(..., description="List of user role or persona names for whom journeys are defined.")
    user_role_descriptions: List[str] = Field(..., description="List of brief descriptions for each user role, aligned by index with user_role_names.")
    user_journey_titles: List[str] = Field(..., description="List of main user journey titles or names for each user role, matching the order of user_role_names.")
    user_journey_steps: List[str] = Field(..., description="List of step-by-step narratives for each user journey, one item per user role, matching the order of user_role_names. Each step-by-step narrative is a single string with steps sequenced, separated by a delimiter or in formatted text.")


def define_user_journeys_for_each_role_fx(identify_primary_user_roles_input: IdentifyPrimaryUserRolesOutput, extract_core_product_features_input: ExtractCoreProductFeaturesOutput, **kwargs) -> DefineUserJourneysForEachRoleOutput:
    """For each identified user role, provide a concise narrative of the main user journey(s) within the workflow.

    Args:
        identify_primary_user_roles_input: Input from the 'identify_primary_user_roles' node.
        extract_core_product_features_input: Input from the 'extract_core_product_features' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineUserJourneysForEachRoleOutput: Object containing outputs for this node.
    """
    pass