from list_primary_user_roles.determine_senior_manager_meeting_role import determine_senior_manager_meeting_role
from list_primary_user_roles.extract_explicit_user_roles_from_requirements import extract_explicit_user_roles_from_requirements
from list_primary_user_roles.ensure_senior_manager_meeting_first import ensure_senior_manager_meeting_first
from list_primary_user_roles.validate_user_roles_type_safety import validate_user_roles_type_safety

from pydantic import BaseModel, Field
from typing import List


class IdentifyCoreObjectiveOutput(BaseModel):
    """Pydantic model for identify_core_objective node outputs."""
    core_objective: str = Field(..., description="The primary objective statement for the workflow as described in the requirements, reflecting the need to include a meeting with senior managers prior to determining user roles, and noting that constraints should be available for use by dependent nodes, such as those identifying success metrics.")


class ListPrimaryUserRolesOutput(BaseModel):
    """Pydantic model for list_primary_user_roles node outputs."""
    user_roles: List[str] = Field(..., description="List of primary user roles or personas interacting with the workflow, explicitly incorporating the node for a meeting with senior managers when applicable.")


def list_primary_user_roles_fx(identify_core_objective_input: IdentifyCoreObjectiveOutput, **kwargs) -> ListPrimaryUserRolesOutput:
    """Determine all primary user roles or personas that will interact with the workflow. As a prerequisite, ensure that a node for a meeting with senior managers is explicitly added, and then include this as a primary user interaction when relevant. Capture a clear, distinct list of primary user roles, without making assumptions about implied or overlapping user types.

    Args:
        identify_core_objective_input: Input from the 'identify_core_objective' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ListPrimaryUserRolesOutput: Object containing outputs for this node.
    """
    # 1. Ensure/insert the senior manager meeting user role as first step
    senior_role: str = determine_senior_manager_meeting_role(core_objective=identify_core_objective_input.core_objective)

    # 2. Extract all explicit user roles from requirements and objective (excluding senior meeting role until explicit inclusion step)
    explicit_roles: List[str] = extract_explicit_user_roles_from_requirements(
        text=identify_core_objective_input.core_objective,
        context_kwargs=kwargs
    )

    # 3. Insert or guarantee the senior manager node/user role at the top
    user_roles: List[str] = ensure_senior_manager_meeting_first(
        senior_manager_role=senior_role, candidate_roles=explicit_roles
    )

    # 4. Validate and serialize as type-safe
    validated_roles: List[str] = validate_user_roles_type_safety(user_roles=user_roles)

    return ListPrimaryUserRolesOutput(user_roles=validated_roles)
