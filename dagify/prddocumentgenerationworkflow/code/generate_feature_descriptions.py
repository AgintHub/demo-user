from generate_feature_descriptions.validate_feature_order import validate_feature_order
from generate_feature_descriptions.generate_descriptions_for_features import generate_descriptions_for_features
from generate_feature_descriptions.apply_sequencing_clauses_to_descriptions import apply_sequencing_clauses_to_descriptions
from generate_feature_descriptions.validate_mapping_consistency import validate_mapping_consistency
from generate_feature_descriptions.disambiguate_descriptions_if_needed import disambiguate_descriptions_if_needed

from pydantic import BaseModel, Field
from typing import List


class ExtractKeyFeaturesOutput(BaseModel):
    """Pydantic model for extract_key_features node outputs."""
    feature_names: List[str] = Field(..., description="Names of fundamental workflow features required in the PRD, in sequence starting with a node to schedule and conduct a meeting with senior managers prior to any role assignment, followed by other required workflow features.")


class GenerateFeatureDescriptionsOutput(BaseModel):
    """Pydantic model for generate_feature_descriptions node outputs."""
    feature_descriptions: List[str] = Field(..., description="Concise description for each feature, including a clear specification of the meeting with senior managers as a required step prior to determining user roles, aligned with feature_names.")


def generate_feature_descriptions_fx(extract_key_features_input: ExtractKeyFeaturesOutput, **kwargs) -> GenerateFeatureDescriptionsOutput:
    """Write a concise, one-sentence description for each feature, explicitly detailing any features related to scheduling and conducting a meeting with senior managers that must occur prior to determining user roles.

    Args:
        extract_key_features_input: Input from the 'extract_key_features' node.
        **kwargs: Additional keyword arguments.

    Returns:
        GenerateFeatureDescriptionsOutput: Object containing outputs for this node.
    """
    # 1. Parse and validate feature_names order, ensuring 'schedule and conduct meeting with senior managers' appears before any user role features
    feature_names: List[str] = extract_key_features_input.feature_names
    validate_feature_order(feature_names=feature_names)

    # 2. Generate concise, context-aware one-sentence description for each feature, handling meeting sequencing requirement
    feature_descriptions: List[str] = generate_descriptions_for_features(
        feature_names=feature_names,
        sequencing_node='schedule and conduct meeting with senior managers'
    )

    # 3. Apply mandatory sequencing clause and rationale to any feature matching the meeting node
    feature_descriptions = apply_sequencing_clauses_to_descriptions(
        feature_names=feature_names,
        descriptions=feature_descriptions,
        sequencing_node='schedule and conduct meeting with senior managers',
        rationale='to solicit executive input and ensure process alignment before any user role determination occurs'
    )

    # 4. Perform 1:1 mapping and order consistency validation between feature_names and feature_descriptions
    validate_mapping_consistency(
        features=feature_names, descriptions=feature_descriptions
    )

    # 5. Disambiguate and refine descriptions to minimize functional overlaps
    feature_descriptions = disambiguate_descriptions_if_needed(
        feature_names=feature_names,
        descriptions=feature_descriptions
    )

    # Return output matching signature
    return GenerateFeatureDescriptionsOutput(feature_descriptions=feature_descriptions)
