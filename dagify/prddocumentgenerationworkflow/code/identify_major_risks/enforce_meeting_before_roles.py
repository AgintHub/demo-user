def enforce_meeting_before_roles(meeting_steps: str, workflow_state: str) -> str:
    """
    This node enforces that a documented senior manager review meeting must occur and be confirmed complete in the workflow before any user role assignment actions are allowed.

    Args:
        meeting_steps: Input parameter of type str
workflow_state: Input parameter of type str

    Returns:
        str: Output of type Any
    """
    import json
    import datetime

    # ----- PURE IMPLEMENTATION -----

    # Parse the workflow_state input and ensure it's a dict
    try:
        if isinstance(workflow_state, str):
            state = json.loads(workflow_state)
        else:
            state = workflow_state
    except Exception:
        # Fail safely with audit log and clear error
        return "ERROR: Unable to parse workflow_state input as JSON. Prevented user role assignment."

    audit_log_entries = []
    status_message = ""
    gating_passed = False

    # Check for the existence of a completed and validated senior manager meeting
    meeting_data = state.get('senior_manager_meeting', {})
    meeting_complete = False
    meeting_validated = False
    meeting_outcome = None

    if isinstance(meeting_data, dict):
        meeting_complete = bool(meeting_data.get('meeting_complete'))
        meeting_validated = bool(meeting_data.get('validated'))
        meeting_outcome = meeting_data.get('outcome')

    # Determine if gating condition is met
    if meeting_complete and meeting_validated:
        gating_passed = True
        status_message = "SUCCESS: Senior manager meeting completed and validated. Progression to user role assignment allowed."
        audit_status = "pass"
    else:
        gating_passed = False
        missing = []
        if not meeting_complete:
            missing.append("'meeting_complete'")
        if not meeting_validated:
            missing.append("'validated'")
        status_message = (
            "ERROR: Cannot proceed to user role assignment. Missing prerequisite(s): " + ', '.join(missing) + "."
        )
        audit_status = "block"

    # --- Audit log hook ---
    audit_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "check": "enforce_meeting_before_roles",
        "result": audit_status,
        "required_fields_present": gating_passed,
        "missing_flags": [] if gating_passed else missing,
        "meeting_outcome": meeting_outcome,
        "user_action": "attempt_user_role_assignment"
    }
    audit_log_entries.append(audit_entry)

    # In real deployment, write audit log to external logger/hook; here we serialize for downstream
    output = {
        "status": status_message,
        "audit": audit_log_entries
    }
    return json.dumps(output)
