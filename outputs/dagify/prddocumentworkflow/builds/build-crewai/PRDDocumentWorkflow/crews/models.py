from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class classify_feature_priorities_output(BaseModel):
    is_must_have: List[bool]  # Must-have (true) or nice-to-have (false) label for each feature requirement, in the same order.

class determine_target_users_output(BaseModel):
    target_user_segments: List[str]  # List of target user types or segments.

class determine_technical_constraints_output(BaseModel):
    technical_constraints: List[str]  # List of technical constraints or dependencies that must be considered.

class extract_feature_requirements_output(BaseModel):
    feature_requirements: List[str]  # List of discrete feature requirements derived from user stories.

class extract_primary_objective_output(BaseModel):
    primary_objective: str  # Main product objective or success goal.

class extract_product_name_output(BaseModel):
    product_name: str  # The concise name of the product or feature.

class extract_success_metrics_output(BaseModel):
    success_metrics: List[str]  # Measurable indicators of product success.

class extract_user_stories_output(BaseModel):
    user_stories: List[str]  # User stories covering key user needs, matching the order of input problems.

class identify_user_problems_output(BaseModel):
    user_problems: List[str]  # List of the user problems or pain points the product addresses.

class summarize_prd_document_output(BaseModel):
    prd_summary: str  # The full, structured PRD summary as plain text.

