from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class compose_prd_summary_output(BaseModel):
    prd_summary: str  # Executive summary for the PRD document, synthesizing objective, users, and features.

class extract_constraints_output(BaseModel):
    constraints: List[str]  # List of explicit technical or business constraints applicable to the workflow.

class extract_key_features_output(BaseModel):
    feature_names: List[str]  # Names of fundamental workflow features required in the PRD.

class generate_feature_descriptions_output(BaseModel):
    feature_descriptions: List[str]  # Concise description for each feature, aligned with feature_names.

class identify_core_objective_output(BaseModel):
    core_objective: str  # The primary objective statement for the workflow as described in the requirements.

class identify_major_risks_output(BaseModel):
    major_risks: List[str]  # Significant risks or uncertainties for delivery or adoption of the workflow.

class identify_success_metrics_output(BaseModel):
    success_metrics: List[str]  # List of measurable success metrics or acceptance criteria.

class list_primary_user_roles_output(BaseModel):
    user_roles: List[str]  # List of primary user roles or personas interacting with the workflow.

class prioritize_features_output(BaseModel):
    feature_priorities: List[int]  # Priority value for each feature, parallel with feature_names.

