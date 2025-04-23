from compose_prd_summary.validate_prd_aggregation_inputs import validate_prd_aggregation_inputs
from compose_prd_summary.compose_executive_leadin import compose_executive_leadin
from compose_prd_summary.render_user_roles_section import render_user_roles_section
from compose_prd_summary.format_features_with_descriptions import format_features_with_descriptions
from compose_prd_summary.compose_meeting_note import compose_meeting_note
from compose_prd_summary.assemble_executive_summary import assemble_executive_summary

from pydantic import BaseModel, Field
from typing import List


class IdentifyCoreObjectiveOutput(BaseModel):
    """Pydantic model for identify_core_objective node outputs."""
    core_objective: str = Field(..., description="The primary objective statement for the workflow as described in the requirements, reflecting the need to include a meeting with senior managers prior to determining user roles, and noting that constraints should be available for use by dependent nodes, such as those identifying success metrics.")


class ListPrimaryUserRolesOutput(BaseModel):
    """Pydantic model for list_primary_user_roles node outputs."""
    user_roles: List[str] = Field(..., description="List of primary user roles or personas interacting with the workflow, explicitly incorporating the node for a meeting with senior managers when applicable.")


class ExtractKeyFeaturesOutput(BaseModel):
    """Pydantic model for extract_key_features node outputs."""
    feature_names: List[str] = Field(..., description="Names of fundamental workflow features required in the PRD, in sequence starting with a node to schedule and conduct a meeting with senior managers prior to any role assignment, followed by other required workflow features.")


class GenerateFeatureDescriptionsOutput(BaseModel):
    """Pydantic model for generate_feature_descriptions node outputs."""
    feature_descriptions: List[str] = Field(..., description="Concise description for each feature, including a clear specification of the meeting with senior managers as a required step prior to determining user roles, aligned with feature_names.")


class ComposePrdSummaryOutput(BaseModel):
    """Pydantic model for compose_prd_summary node outputs."""
    prd_summary: str = Field(..., description="Executive summary for the PRD document, synthesizing objective, users, and features, and including a note about the meeting with senior managers.")


def compose_prd_summary_fx(identify_core_objective_input: IdentifyCoreObjectiveOutput, list_primary_user_roles_input: ListPrimaryUserRolesOutput, extract_key_features_input: ExtractKeyFeaturesOutput, generate_feature_descriptions_input: GenerateFeatureDescriptionsOutput, **kwargs) -> ComposePrdSummaryOutput:
    """Create a PRD executive summary referencing all prior outputs. Include a brief note outlining the purpose and main topics for an upcoming meeting with senior managers regarding the PRD.

    Args:
        identify_core_objective_input: Input from the 'identify_core_objective' node.
        list_primary_user_roles_input: Input from the 'list_primary_user_roles' node.
        extract_key_features_input: Input from the 'extract_key_features' node.
        generate_feature_descriptions_input: Input from the 'generate_feature_descriptions' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ComposePrdSummaryOutput: Object containing outputs for this node.
    """
    # --- AGGREGATE & VALIDATE INPUTS ---
    inputs_valid: bool = validate_prd_aggregation_inputs(
        core_obj=identify_core_objective_input,
        user_roles=list_primary_user_roles_input,
        features=extract_key_features_input,
        feature_desc=generate_feature_descriptions_input
    )

    # --- LEAD-IN GENERATION ---
    lead_in: str = compose_executive_leadin(core_objective=identify_core_objective_input.core_objective)

    # --- USER ROLES SECTION ---
    user_roles_section: str = render_user_roles_section(user_roles=list_primary_user_roles_input.user_roles)

    # --- FEATURES & DESCRIPTIONS SECTION ---
    features_with_desc: str = format_features_with_descriptions(
        feature_names=extract_key_features_input.feature_names,
        feature_descriptions=generate_feature_descriptions_input.feature_descriptions
    )

    # --- UPCOMING MEETING NOTE ---
    meeting_note: str = compose_meeting_note(
        topics=[
            "Objective",
            "Primary User Roles",
            "Key Features",
            "Feature Definitions"
        ]
    )

    # --- FINAL SUMMARY ASSEMBLY ---
    prd_summary_str: str = assemble_executive_summary(
        lead_in=lead_in,
        user_roles_section=user_roles_section,
        feature_section=features_with_desc,
        meeting_note=meeting_note
    )

    return ComposePrdSummaryOutput(prd_summary=prd_summary_str)
