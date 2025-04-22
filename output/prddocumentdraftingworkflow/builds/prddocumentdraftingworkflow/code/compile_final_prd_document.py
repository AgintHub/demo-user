from pydantic import BaseModel, Field
from typing import List


class DraftPrdSectionObjectivesOutput(BaseModel):
    """Pydantic model for draft_prd_section_objectives node outputs."""
    objectives_section_heading: str = Field(..., description="The section heading for objectives, e.g. 'Objectives'.")
    objective_statements: List[str] = Field(..., description="A list of individual, formal objective statements for inclusion in the PRD Objectives section.")


class DraftPrdSectionUserRolesOutput(BaseModel):
    """Pydantic model for draft_prd_section_user_roles node outputs."""
    role_names: List[str] = Field(..., description="List of user role or persona names included in the PRD section")
    role_descriptions: List[str] = Field(..., description="List of brief descriptions for each user role or persona, matching the order of role_names")
    section_text: str = Field(..., description="The full 'User Roles & Personas' section as formatted text for the PRD")


class DraftPrdSectionFeaturesOutput(BaseModel):
    """Pydantic model for draft_prd_section_features node outputs."""
    features_section_title: str = Field(..., description="The heading/title for the PRD Features section.")
    feature_list: List[str] = Field(..., description="A list of core product features, each stated concisely suitable for inclusion in the PRD.")


class DraftPrdSectionConstraintsOutput(BaseModel):
    """Pydantic model for draft_prd_section_constraints node outputs."""
    constraints_section_heading: str = Field(..., description="Section heading for the Constraints section in the PRD.")
    constraints_list: List[str] = Field(..., description="A list of formal, clearly stated constraints relevant to the product requirements.")


class DraftPrdSectionSuccessMetricsOutput(BaseModel):
    """Pydantic model for draft_prd_section_success_metrics node outputs."""
    success_metrics_section_title: str = Field(..., description="The section heading for the success metrics in the PRD.")
    success_metrics_list: List[str] = Field(..., description="A list of strings, each describing a quantifiable or objectively verifiable success metric for the product.")


class DraftPrdSectionStakeholdersOutput(BaseModel):
    """Pydantic model for draft_prd_section_stakeholders node outputs."""
    stakeholder_names: List[str] = Field(..., description="List of the stakeholder names or titles included in the PRD Stakeholders section.")
    stakeholder_roles: List[str] = Field(..., description="List of short descriptions for each stakeholder's role in the project. Aligned by index with stakeholder_names.")
    stakeholder_significance: List[str] = Field(..., description="List of brief statements of each stakeholder's significance or interest in the project outcome. Aligned by index with stakeholder_names.")
    prd_stakeholders_section_text: str = Field(..., description="The fully formatted 'Stakeholders' section text, ready to be inserted directly into the PRD document.")


class DraftPrdSectionUserJourneysOutput(BaseModel):
    """Pydantic model for draft_prd_section_user_journeys node outputs."""
    user_journey_section_heading: str = Field(..., description="Heading for the User Journeys section in the PRD.")
    user_roles: List[str] = Field(..., description="List of user roles for which user journeys are documented.")
    user_journey_titles: List[str] = Field(..., description="List of titles/names for each user journey, corresponding one-to-one with user_roles.")
    user_journey_narratives: List[str] = Field(..., description="List of narrative descriptions for each user journey, corresponding one-to-one with user_roles.")
    user_journey_step_lists: List[str] = Field(..., description="For each user journey, a string formatted step-by-step sequence describing the actions in that journey (bulleted or numbered).")


class CompileFinalPrdDocumentOutput(BaseModel):
    """Pydantic model for compile_final_prd_document node outputs."""
    prd_title: str = Field(..., description="Title of the Product Requirements Document")
    objectives_section: str = Field(..., description="The full formatted Objectives section text")
    user_roles_and_personas_section: str = Field(..., description="The full formatted User Roles & Personas section text")
    features_section: str = Field(..., description="The full formatted Features section text")
    constraints_section: str = Field(..., description="The full formatted Constraints section text")
    success_metrics_section: str = Field(..., description="The full formatted Success Metrics section text")
    stakeholders_section: str = Field(..., description="The full formatted Stakeholders section text")
    user_journeys_section: str = Field(..., description="The full formatted User Journeys section text")
    full_prd_document: str = Field(..., description="The complete combined PRD document as a single string, with all sections in proper order and headings")


def compile_final_prd_document_fx(draft_prd_section_objectives_input: DraftPrdSectionObjectivesOutput, draft_prd_section_user_roles_input: DraftPrdSectionUserRolesOutput, draft_prd_section_features_input: DraftPrdSectionFeaturesOutput, draft_prd_section_constraints_input: DraftPrdSectionConstraintsOutput, draft_prd_section_success_metrics_input: DraftPrdSectionSuccessMetricsOutput, draft_prd_section_stakeholders_input: DraftPrdSectionStakeholdersOutput, draft_prd_section_user_journeys_input: DraftPrdSectionUserJourneysOutput, **kwargs) -> CompileFinalPrdDocumentOutput:
    """Combine all previously drafted sections into a single coherent PRD document, maintaining logical order and structure.

    Args:
        draft_prd_section_objectives_input: Input from the 'draft_prd_section_objectives' node.
        draft_prd_section_user_roles_input: Input from the 'draft_prd_section_user_roles' node.
        draft_prd_section_features_input: Input from the 'draft_prd_section_features' node.
        draft_prd_section_constraints_input: Input from the 'draft_prd_section_constraints' node.
        draft_prd_section_success_metrics_input: Input from the 'draft_prd_section_success_metrics' node.
        draft_prd_section_stakeholders_input: Input from the 'draft_prd_section_stakeholders' node.
        draft_prd_section_user_journeys_input: Input from the 'draft_prd_section_user_journeys' node.
        **kwargs: Additional keyword arguments.

    Returns:
        CompileFinalPrdDocumentOutput: Object containing outputs for this node.
    """
    pass