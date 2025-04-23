from extract_key_features.extract_feature_candidates_from_objective import extract_feature_candidates_from_objective
from extract_key_features.ensure_meeting_node_first import ensure_meeting_node_first
from extract_key_features.block_or_reorder_role_features import block_or_reorder_role_features
from extract_key_features.normalize_and_deduplicate_features import normalize_and_deduplicate_features
from extract_key_features.sequence_features_per_workflow_order import sequence_features_per_workflow_order
from extract_key_features.validate_and_serialize_feature_list import validate_and_serialize_feature_list

from pydantic import BaseModel, Field
from typing import List


class IdentifyCoreObjectiveOutput(BaseModel):
    """Pydantic model for identify_core_objective node outputs."""
    core_objective: str = Field(..., description="The primary objective statement for the workflow as described in the requirements, reflecting the need to include a meeting with senior managers prior to determining user roles, and noting that constraints should be available for use by dependent nodes, such as those identifying success metrics.")


class ExtractKeyFeaturesOutput(BaseModel):
    """Pydantic model for extract_key_features node outputs."""
    feature_names: List[str] = Field(..., description="Names of fundamental workflow features required in the PRD, in sequence starting with a node to schedule and conduct a meeting with senior managers prior to any role assignment, followed by other required workflow features.")


def extract_key_features_fx(identify_core_objective_input: IdentifyCoreObjectiveOutput, **kwargs) -> ExtractKeyFeaturesOutput:
    """Generate a list of key functional features required by the workflow, explicitly adding a workflow node for scheduling and conducting a meeting with senior managers prior to determining user roles, as per updated requirements. Each feature must be a unique functional capability required by the PRD, sequenced to reflect this critical ordering.

    Args:
        identify_core_objective_input: Input from the 'identify_core_objective' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ExtractKeyFeaturesOutput: Object containing outputs for this node.
    """
    # --- SHIM IMPLEMENTATION ---
    # 1. Parse requirements and core objective for candidate features
    candidate_features: List[str] = extract_feature_candidates_from_objective(text=identify_core_objective_input.core_objective)
    
    # 2. Prepend 'Schedule and conduct a meeting with senior managers' as the first feature
    feature_list_with_meeting: List[str] = ensure_meeting_node_first(features=candidate_features)
    
    # 3. Enforce that no user role/determination related features appear before the meeting node
    ordered_features: List[str] = block_or_reorder_role_features(features=feature_list_with_meeting)

    # 4. Deduplicate and split compound features into atomic, unique units
    atomic_features: List[str] = normalize_and_deduplicate_features(features=ordered_features)

    # 5. Sequence list according to all workflow constraints (meeting node first, roles after, etc.)
    sequenced_features: List[str] = sequence_features_per_workflow_order(features=atomic_features)

    # 6. Validate and serialize output list
    validated_features: List[str] = validate_and_serialize_feature_list(features=sequenced_features)

    return ExtractKeyFeaturesOutput(feature_names=validated_features)
