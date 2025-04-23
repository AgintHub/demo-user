from identify_success_metrics.extract_constraints_from_parent_input import extract_constraints_from_parent_input
from identify_success_metrics.map_constraints_to_metrics import map_constraints_to_metrics
from identify_success_metrics.generate_meeting_governance_metric import generate_meeting_governance_metric
from identify_success_metrics.structure_metrics_for_reporting import structure_metrics_for_reporting
from identify_success_metrics.generate_quant_qual_metrics import generate_quant_qual_metrics
from identify_success_metrics.add_traceability_to_metrics import add_traceability_to_metrics
from identify_success_metrics.find_unmapped_constraints import find_unmapped_constraints
from identify_success_metrics.log_or_raise_unmapped_constraints import log_or_raise_unmapped_constraints

from pydantic import BaseModel, Field
from typing import List


class IdentifyCoreObjectiveOutput(BaseModel):
    """Pydantic model for identify_core_objective node outputs."""
    core_objective: str = Field(..., description="The primary objective statement for the workflow as described in the requirements, reflecting the need to include a meeting with senior managers prior to determining user roles, and noting that constraints should be available for use by dependent nodes, such as those identifying success metrics.")


class IdentifySuccessMetricsOutput(BaseModel):
    """Pydantic model for identify_success_metrics node outputs."""
    success_metrics: List[str] = Field(..., description="List of measurable success metrics or acceptance criteria, each reflecting alignment with the core objective and honoring identified constraints, and including at least one explicit metric that the meeting with senior managers has been scheduled and completed before user roles are determined.")


def identify_success_metrics_fx(identify_core_objective_input: IdentifyCoreObjectiveOutput, **kwargs) -> IdentifySuccessMetricsOutput:
    """List measurable success criteria (quantitative or qualitative) for the workflow, ensuring that constraints are incorporated as inputs to defining these metrics. Explicitly include a success metric for the scheduling and completion of a meeting with senior managers prior to any determination of user roles, aligned with the requirement to add such a node before user roles are set.

    Args:
        identify_core_objective_input: Input from the 'identify_core_objective' node.
        **kwargs: Additional keyword arguments.

    Returns:
        IdentifySuccessMetricsOutput: Object containing outputs for this node.
    """
    # Extract the core objective and constraints from the parent node and additional kwargs (if present)
    core_objective: str = identify_core_objective_input.core_objective
    # Extract constraints from kwargs or parent node outputs
    constraints: List[str] = extract_constraints_from_parent_input(inputs=kwargs, fallback_objective_output=identify_core_objective_input)  # type: List[str]

    # Map each explicit constraint to one or more measurable success metrics
    constraint_to_metrics: List[str] = map_constraints_to_metrics(constraints=constraints, objective=core_objective)  # type: List[str]

    # Ensure an explicit metric for meeting completion with senior managers prior to user role assignment
    meeting_metric: str = generate_meeting_governance_metric(core_objective=core_objective, constraints=constraints)

    # Structure all metrics using a standardized format (e.g., SMART/OKR)
    formatted_metrics: List[str] = structure_metrics_for_reporting(metrics=constraint_to_metrics + [meeting_metric], template="SMART")

    # Support both quantitative and qualitative metrics based on constraints/objective analysis
    enriched_metrics: List[str] = generate_quant_qual_metrics(metrics=formatted_metrics, constraints=constraints, core_objective=core_objective)

    # Ensure traceability of each metric to originating feature/constraint/workflow node
    traceable_metrics: List[str] = add_traceability_to_metrics(metrics=enriched_metrics, constraints=constraints, node_reference=kwargs.get('node_reference'))

    # Automated check: flag any unmapped constraints
    unmapped_constraints: List[str] = find_unmapped_constraints(constraints=constraints, metrics=traceable_metrics)
    log_or_raise_unmapped_constraints(unmapped_constraints=unmapped_constraints)

    # Return as output instance
    return IdentifySuccessMetricsOutput(success_metrics=traceable_metrics)
