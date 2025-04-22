from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class compile_final_prd_document_output(BaseModel):
    prd_title: str  # Title of the Product Requirements Document
    objectives_section: str  # The full formatted Objectives section text
    user_roles_and_personas_section: str  # The full formatted User Roles & Personas section text
    features_section: str  # The full formatted Features section text
    constraints_section: str  # The full formatted Constraints section text
    success_metrics_section: str  # The full formatted Success Metrics section text
    stakeholders_section: str  # The full formatted Stakeholders section text
    user_journeys_section: str  # The full formatted User Journeys section text
    full_prd_document: str  # The complete combined PRD document as a single string, with all sections in proper order and headings

class define_success_metrics_output(BaseModel):
    metric_names: List[str]  # List of names or brief descriptions for each defined success metric.
    metric_objective_mappings: List[str]  # For each metric, a string describing which objective(s) it maps to.
    metric_quantifiability: List[bool]  # List indicating whether each success metric is quantifiable or objectively verifiable.

class define_user_journeys_for_each_role_output(BaseModel):
    user_role_names: List[str]  # List of user role or persona names for whom journeys are defined.
    user_role_descriptions: List[str]  # List of brief descriptions for each user role, aligned by index with user_role_names.
    user_journey_titles: List[str]  # List of main user journey titles or names for each user role, matching the order of user_role_names.
    user_journey_steps: List[str]  # List of step-by-step narratives for each user journey, one item per user role, matching the order of user_role_names. Each step-by-step narrative is a single string with steps sequenced, separated by a delimiter or in formatted text.

class draft_prd_section_constraints_output(BaseModel):
    constraints_section_heading: str  # Section heading for the Constraints section in the PRD.
    constraints_list: List[str]  # A list of formal, clearly stated constraints relevant to the product requirements.

class draft_prd_section_features_output(BaseModel):
    features_section_title: str  # The heading/title for the PRD Features section.
    feature_list: List[str]  # A list of core product features, each stated concisely suitable for inclusion in the PRD.

class draft_prd_section_objectives_output(BaseModel):
    objectives_section_heading: str  # The section heading for objectives, e.g. Objectives.
    objective_statements: List[str]  # A list of individual, formal objective statements for inclusion in the PRD Objectives section.

class draft_prd_section_stakeholders_output(BaseModel):
    stakeholder_names: List[str]  # List of the stakeholder names or titles included in the PRD Stakeholders section.
    stakeholder_roles: List[str]  # List of short descriptions for each stakeholders role in the project. Aligned by index with stakeholder_names.
    stakeholder_significance: List[str]  # List of brief statements of each stakeholders significance or interest in the project outcome. Aligned by index with stakeholder_names.
    prd_stakeholders_section_text: str  # The fully formatted Stakeholders section text, ready to be inserted directly into the PRD document.

class draft_prd_section_success_metrics_output(BaseModel):
    success_metrics_section_title: str  # The section heading for the success metrics in the PRD.
    success_metrics_list: List[str]  # A list of strings, each describing a quantifiable or objectively verifiable success metric for the product.

class draft_prd_section_user_journeys_output(BaseModel):
    user_journey_section_heading: str  # Heading for the User Journeys section in the PRD.
    user_roles: List[str]  # List of user roles for which user journeys are documented.
    user_journey_titles: List[str]  # List of titles/names for each user journey, corresponding one-to-one with user_roles.
    user_journey_narratives: List[str]  # List of narrative descriptions for each user journey, corresponding one-to-one with user_roles.
    user_journey_step_lists: List[str]  # For each user journey, a string formatted step-by-step sequence describing the actions in that journey (bulleted or numbered).

class draft_prd_section_user_roles_output(BaseModel):
    role_names: List[str]  # List of user role or persona names included in the PRD section
    role_descriptions: List[str]  # List of brief descriptions for each user role or persona, matching the order of role_names
    section_text: str  # The full User Roles & Personas section as formatted text for the PRD

class extract_core_product_features_output(BaseModel):
    core_product_features: List[str]  # A list of singular, succinct descriptions of each core product feature required to achieve the stated objectives.

class extract_critical_constraints_output(BaseModel):
    constraints: List[str]  # Individual statements of technical, business, regulatory, or design constraints relevant to the product requirements.

class extract_objectives_from_workflow_requirements_output(BaseModel):
    objectives: List[str]  # A list of explicit and implicit objectives that the PRD must address, each as a clearly stated goal.

class identify_primary_user_roles_output(BaseModel):
    user_role_names: List[str]  # List of primary user role or persona names directly involved with the product.
    user_role_descriptions: List[str]  # List of concise one-sentence descriptions for each user role, matched by index to user_role_names.

class summarize_key_stakeholders_output(BaseModel):
    stakeholder_names: List[str]  # List of key stakeholder names.
    stakeholder_roles: List[str]  # List of brief descriptions of each stakeholders role.
    stakeholder_interests: List[str]  # List of brief descriptions of each stakeholders interest in the project outcome.

