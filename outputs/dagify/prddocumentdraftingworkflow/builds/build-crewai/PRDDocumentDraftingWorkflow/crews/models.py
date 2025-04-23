from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class derive_functional_requirements_output(BaseModel):
    functional_requirements: List[str]  # List of distinct, testable functional requirements derived from use cases and goals. Each string is a single requirement describing a necessary system behavior.

class derive_nonfunctional_requirements_output(BaseModel):
    nonfunctional_requirements: List[str]  # List of distinct, specific, and measurable nonfunctional requirements derived from the product goals and constraints. Each entry should describe a single nonfunctional requirement (e.g., performance targets, scalability needs, security standards, usability requirements).

class extract_assumptions_and_constraints_output(BaseModel):
    assumptions: List[str]  # A list of explicit or implied assumptions that underlie the product or feature scope.
    constraints: List[str]  # A list of explicit or implied constraints that limit the scope, implementation, or delivery of the product or feature.

class extract_goals_output(BaseModel):
    primary_goals: List[str]  # A list of the main goals and objectives the product or workflow must achieve, each expressed as a clear and atomic statement focused on business value.

class extract_product_context_output(BaseModel):
    product_name: str  # The name or title of the product or feature being described.
    summary: str  # A concise summary of what is being built, capturing the high-level product or feature context.
    primary_purpose: str  # A single sentence stating the core purpose or intent of the product or feature.
    key_features: List[str]  # A list of the most important features or elements that define the products scope, expressed broadly (not as requirements).

class extract_success_metrics_output(BaseModel):
    success_metrics: List[str]  # List of measurable success metrics or acceptance criteria, each as a distinct string.

class extract_use_cases_output(BaseModel):
    use_cases: List[str]  # List of atomic, single-actor, goal-driven activities (use cases) that the system must support.

class identify_stakeholders_output(BaseModel):
    stakeholder_roles: List[str]  # List of individual stakeholder roles, titles, or groups relevant to the product or workflow.

class synthesize_prd_outline_output(BaseModel):
    prd_product_context: str  # The summarized core product or feature context section of the PRD.
    prd_stakeholders: List[str]  # List of all relevant stakeholders for the product or feature.
    prd_goals: List[str]  # List of primary goals and objectives the product must achieve.
    prd_assumptions_and_constraints: List[str]  # All explicit assumptions and constraints limiting the products scope.
    prd_use_cases: List[str]  # Atomic use cases or user tasks the system must support.
    prd_functional_requirements: List[str]  # Specific, testable, and distinct functional requirements derived from use cases and goals.
    prd_nonfunctional_requirements: List[str]  # Nonfunctional requirements like performance, security, scalability, or usability.
    prd_success_metrics: List[str]  # Measurable metrics or acceptance criteria for successful delivery or completion.

