from pydantic import BaseModel, Field
from typing import List


class ExtractCoreProductFeaturesOutput(BaseModel):
    """Pydantic model for extract_core_product_features node outputs."""
    core_product_features: List[str] = Field(..., description="A list of singular, succinct descriptions of each core product feature required to achieve the stated objectives.")


class DraftPrdSectionFeaturesOutput(BaseModel):
    """Pydantic model for draft_prd_section_features node outputs."""
    features_section_title: str = Field(..., description="The heading/title for the PRD Features section.")
    feature_list: List[str] = Field(..., description="A list of core product features, each stated concisely suitable for inclusion in the PRD.")


def draft_prd_section_features_fx(extract_core_product_features_input: ExtractCoreProductFeaturesOutput, **kwargs) -> DraftPrdSectionFeaturesOutput:
    """Compile the core features into the PRD 'Features' section.

    Args:
        extract_core_product_features_input: Input from the 'extract_core_product_features' node.
        **kwargs: Additional keyword arguments.

    Returns:
        DraftPrdSectionFeaturesOutput: Object containing outputs for this node.
    """
    pass