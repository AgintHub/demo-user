from extract_constraints.preprocess_requirements_text import preprocess_requirements_text
from extract_constraints.extract_explicit_constraints import extract_explicit_constraints
from extract_constraints.filter_for_explicitness import filter_for_explicitness
from extract_constraints.format_and_validate_constraints import format_and_validate_constraints
from extract_constraints.extract_manager_discussion_points import extract_manager_discussion_points
from extract_constraints.log_extraction_audit import log_extraction_audit
from extract_constraints.update_extraction_config_if_needed import update_extraction_config_if_needed

from pydantic import BaseModel, Field
from typing import List


class ExtractConstraintsOutput(BaseModel):
    """Pydantic model for extract_constraints node outputs."""
    constraints: List[str] = Field(..., description="List of explicit technical or business constraints applicable to the workflow, structured for direct use in identifying and defining success metrics.")
    manager_discussion_points: List[str] = Field(..., description="List of items or constraints requiring clarification, approval, or input from senior managers, to be used as an agenda for a dedicated meeting.")


def extract_constraints_fx(general_input: str, **kwargs) -> ExtractConstraintsOutput:
    """Extract explicit technical or business constraints from the requirements, and identify discussion points for a meeting with senior managers. Both sets of outputs will be used as key inputs for identifying success metrics and ensuring stakeholder alignment.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        ExtractConstraintsOutput: Object containing outputs for this node.
    """
    # Step 1: Clean and preprocess the input text
    preprocessed_text: str = preprocess_requirements_text(raw_input=general_input)

    # Step 2: Extract candidate constraints using rule-based and pattern matching
    candidate_constraints: List[str] = extract_explicit_constraints(text=preprocessed_text, matchers=["must", "should", "shall", "limited to", "deadline", "no more than"])  # type: ignore

    # Step 3: Filter out implied or ambiguous constraints (retain only direct evidence)
    explicit_constraints: List[str] = filter_for_explicitness(constraints=candidate_constraints, text=preprocessed_text)

    # Step 4: Standardize/format constraints for structured output
    structured_constraints: List[str] = format_and_validate_constraints(constraints=explicit_constraints)

    # Step 5: Identify discussion points: constraints/items needing clarification or executive approval
    manager_discussion_points: List[str] = extract_manager_discussion_points(text=preprocessed_text, 
        triggers=["to be confirmed", "subject to approval", "pending clarification", "TBD", "to be decided"])

    # Step 6: Log/audit results for compliance traceability
    log_extraction_audit(extracted_constraints=structured_constraints, discussion_points=manager_discussion_points, original_input=general_input)

    # Step 7 (for extensibility): optionally update/configure patterns for future regulatory/technical categories
    update_extraction_config_if_needed(kwargs=kwargs)

    return ExtractConstraintsOutput(constraints=structured_constraints, manager_discussion_points=manager_discussion_points)
