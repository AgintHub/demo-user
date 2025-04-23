from prioritize_features.enforce_meeting_precedes_roles import enforce_meeting_precedes_roles
from prioritize_features.assign_unique_priorities import assign_unique_priorities
from prioritize_features.validate_alignment import validate_alignment

from pydantic import BaseModel, Field
from typing import List


class ExtractKeyFeaturesOutput(BaseModel):
    """Pydantic model for extract_key_features node outputs."""
    feature_names: List[str] = Field(..., description="Names of fundamental workflow features required in the PRD, in sequence starting with a node to schedule and conduct a meeting with senior managers prior to any role assignment, followed by other required workflow features.")


class PrioritizeFeaturesOutput(BaseModel):
    """Pydantic model for prioritize_features node outputs."""
    feature_priorities: List[int] = Field(..., description="Priority value for each feature, parallel with feature_names (ensuring a 'meeting with senior managers' node comes before user role determination and is appropriately ranked).")


def prioritize_features_fx(extract_key_features_input: ExtractKeyFeaturesOutput, **kwargs) -> PrioritizeFeaturesOutput:
    """Assign a unique priority ranking to each key feature, ensuring that a feature related to a meeting with senior managers is explicitly included—specifically, a node for the meeting should occur prior to determining user roles—and given an appropriate criticality ranking.

    Args:
        extract_key_features_input: Input from the 'extract_key_features' node.
        **kwargs: Additional keyword arguments.

    Returns:
        PrioritizeFeaturesOutput: Object containing outputs for this node.
    """
    # --- SHIM IMPLEMENTATION ---
    # 1. Get original feature names
    feature_names: List[str] = extract_key_features_input.feature_names
    
    # 2. Ensure 'Schedule and conduct a meeting with senior managers' is present and placed before any user-role-determination features
    enforced_feature_names: List[str] = enforce_meeting_precedes_roles(features=feature_names)
    
    # 3. Assign unique priorities based on criticality, workflow, and regulatory dependency
    priorities: List[int] = assign_unique_priorities(features=enforced_feature_names)
    
    # 4. Validate index alignment (parallel lists)
    validate_alignment(features=enforced_feature_names, priorities=priorities)  # returns None, raises if mismatch
    
    # 5. Return as required
    return PrioritizeFeaturesOutput(feature_priorities=priorities)
