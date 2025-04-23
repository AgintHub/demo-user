def generate_meeting_governance_metric(core_objective: str, constraints: str) -> str:
    """
    This node generates a specific, measurable success metric that ensures a meeting with senior managers is scheduled and completed prior to determining user roles, based on the workflow's core objective and constraints.

    Args:
        core_objective: Input parameter of type str
constraints: Input parameter of type str

    Returns:
        str: Output of type str
    """
    # --- PURE IMPLEMENTATION ---
    import re
    
    # Step 1: Extract key temporal and procedural requirements for "meeting with senior managers" and "user role determination"
    text = core_objective + " " + constraints
    text_lower = text.lower()
    
    # Look for temporal or ordering cues
    role_keywords = [
        r"user role determination",
        r"role assignment[s]?",
        r"assign user roles",
        r"determin(?:e|ation) of user roles",