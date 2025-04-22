from pydantic import BaseModel, Field
from typing import List


class DefineUserJourneysForEachRoleOutput(BaseModel):
    """Pydantic model for define_user_journeys_for_each_role node outputs."""
    user_role_names: List[str] = Field(..., description="List of user role or persona names for whom journeys are defined.")
    user_role_descriptions: List[str] = Field(..., description="List of brief descriptions for each user role, aligned by index with user_role_names.")
    user_journey_titles: List[str] = Field(..., description="List of main user journey titles or names for each user role, matching the order of user_role_names.")
    user_journey_steps: List[str] = Field(..., description="List of step-by-step narratives for each user journey, one item per user role, matching the order of user_role_names. Each step-by-step narrative is a single string with steps sequenced, separated by a delimiter or in formatted text.")


class DraftPrdSectionUserJourneysOutput(BaseModel):
    """Pydantic model for draft_prd_section_user_journeys node outputs."""
    user_journey_section_heading: str = Field(..., description="Heading for the User Journeys section in the PRD.")
    user_roles: List[str] = Field(..., description="List of user roles for which user journeys are documented.")
    user_journey_titles: List[str] = Field(..., description="List of titles/names for each user journey, corresponding one-to-one with user_roles.")
    user_journey_narratives: List[str] = Field(..., description="List of narrative descriptions for each user journey, corresponding one-to-one with user_roles.")
    user_journey_step_lists: List[str] = Field(..., description="For each user journey, a string formatted step-by-step sequence describing the actions in that journey (bulleted or numbered).")


def draft_prd_section_user_journeys_fx(define_user_journeys_for_each_role_input: DefineUserJourneysForEachRoleOutput, **kwargs) -> DraftPrdSectionUserJourneysOutput:
    """Organize the user journeys as a distinct 'User Journeys' section in the PRD.

    Args:
        define_user_journeys_for_each_role_input: Input from the 'define_user_journeys_for_each_role' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DraftPrdSectionUserJourneysOutput: Object containing outputs for this node.
    """
    pass