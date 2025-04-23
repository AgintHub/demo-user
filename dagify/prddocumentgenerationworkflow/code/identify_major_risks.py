from identify_major_risks.extract_constraints_from_inputs import extract_constraints_from_inputs
from identify_major_risks.assess_risks_with_constraints import assess_risks_with_constraints
from identify_major_risks.document_risks_with_rationale import document_risks_with_rationale
from identify_major_risks.tag_risks_actionable import tag_risks_actionable
from identify_major_risks.filter_major_risks import filter_major_risks
from identify_major_risks.format_major_risks import format_major_risks
from identify_major_risks.generate_senior_manager_meeting_steps import generate_senior_manager_meeting_steps
from identify_major_risks.enforce_meeting_before_roles import enforce_meeting_before_roles
from identify_major_risks.log_risk_audit_trail import log_risk_audit_trail

from pydantic import BaseModel, Field
from typing import List


class IdentifyMajorRisksOutput(BaseModel):
    """Pydantic model for identify_major_risks node outputs."""
    major_risks: List[str] = Field(..., description="Significant risks or uncertainties for delivery or adoption of the workflow, informed by and linked to any identified constraints.")
    senior_manager_meeting_steps: List[str] = Field(..., description="Actionable steps for organizing and conducting a meeting with senior managers to review and validate identified risks prior to determining user roles.")


def identify_major_risks_fx(general_input: str, **kwargs) -> IdentifyMajorRisksOutput:
    """List significant risks or uncertainties associated with the workflow, explicitly considering constraints as potential sources of risk or uncertainty. Before determining user roles in the workflow, plan and conduct a meeting with senior managers to review, validate, and discuss the risks, ensuring executive visibility and input at an early stage.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        IdentifyMajorRisksOutput: Object containing outputs for this node.
    """
    # Step 1: Collate all constraints previously extracted by upstream nodes
    constraints: List[str] = extract_constraints_from_inputs(inputs=kwargs)

    # Step 2: Identify and analyze significant risks, linking them to constraints
    raw_risks: List[dict] = assess_risks_with_constraints(
        workflow_description=general_input,
        constraints=constraints,
        framework="FMEA|risk_matrix"
    )

    # Step 3: Document each risk and associate rationale and constraint references
    documented_risks: List[dict] = document_risks_with_rationale(
        risks=raw_risks,
        constraints=constraints
    )

    # Step 4: Tag each risk as actionable or non-actionable
    tagged_risks: List[dict] = tag_risks_actionable(risks=documented_risks)

    # Step 5: Filter out only actionable or critical risks for output
    filtered_major_risks: List[dict] = filter_major_risks(
        risks=tagged_risks,
        filter_mode="actionable_or_critical"
    )

    # Step 6: Generate formatted output strings for each major risk
    major_risk_strings: List[str] = format_major_risks(risks=filtered_major_risks)

    # Step 7: Create and schedule a senior manager meeting before roles assignment
    meeting_steps: List[str] = generate_senior_manager_meeting_steps(
        risks=filtered_major_risks,
        constraints=constraints,
        agenda_notes=True,
        calendar_integration=True,
        notification_queue=True
    )

    # Step 8: Embed workflow checks to enforce meeting occurs before user role assignment
    enforce_meeting_before_roles(
        meeting_steps=meeting_steps,
        workflow_state=kwargs.get("workflow_state"),
        gating_enabled=True
    )

    # Step 9: Maintain audit trail for risk documentation and decisions
    log_risk_audit_trail(
        risks=filtered_major_risks,
        constraints=constraints,
        action="initial_risk_identification_meeting"
    )

    return IdentifyMajorRisksOutput(
        major_risks=major_risk_strings,
        senior_manager_meeting_steps=meeting_steps
    )
