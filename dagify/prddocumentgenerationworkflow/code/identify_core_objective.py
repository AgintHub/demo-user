from identify_core_objective.extract_core_objective_from_requirements import extract_core_objective_from_requirements
from identify_core_objective.extract_sequencing_clause_for_meeting import extract_sequencing_clause_for_meeting
from identify_core_objective.extract_constraint_references import extract_constraint_references
from identify_core_objective.compose_final_objective_statement import compose_final_objective_statement
from identify_core_objective.validate_core_objective_output_schema import validate_core_objective_output_schema
from identify_core_objective.store_node_output_in_context import store_node_output_in_context

from pydantic import BaseModel, Field


class IdentifyCoreObjectiveOutput(BaseModel):
    """Pydantic model for identify_core_objective node outputs."""
    core_objective: str = Field(..., description="The primary objective statement for the workflow as described in the requirements, reflecting the need to include a meeting with senior managers prior to determining user roles, and noting that constraints should be available for use by dependent nodes, such as those identifying success metrics.")


def identify_core_objective_fx(general_input: str, **kwargs) -> IdentifyCoreObjectiveOutput:
    """Extract the single core objective of the workflow based on provided requirements, ensuring that extracted constraints will be available as input for downstream nodes such as identification of success metrics. Additionally, explicitly incorporate the requirement to add a node for a meeting with senior managers prior to determining user roles as part of the workflow, ensuring this sequencing is considered in defining the core objective.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        IdentifyCoreObjectiveOutput: Object containing outputs for this node.
    """
    # Step 1: Extract and summarize the core objective from the input requirements
    core_objective_base: str = extract_core_objective_from_requirements(requirements_text=general_input)
    # Step 2: Detect requirement for sequencing (senior manager meeting before user role assignment)
    sequencing_clause: str = extract_sequencing_clause_for_meeting(requirements_text=general_input)
    # Step 3: Extract references to technical/business constraints
    constraints_reference: str = extract_constraint_references(requirements_text=general_input)
    # Step 4: Synthesize the final objective statement integrating all elements
    core_objective: str = compose_final_objective_statement(
        base_objective=core_objective_base,
        sequencing=sequencing_clause,
        constraints=constraints_reference
    )
    # Step 5: Enforce output schema/type safety
    validate_core_objective_output_schema(core_objective=core_objective)
    # (Optional) Store in shared context for downstream availability
    store_node_output_in_context(key="identify_core_objective", value=core_objective)
    # Step 6: Return typed output
    return IdentifyCoreObjectiveOutput(core_objective=core_objective)
