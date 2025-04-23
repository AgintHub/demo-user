def render_user_roles_section(user_roles: str) -> str:
    """
    Generates a well-formatted, human-readable section that describes the primary user roles in the workflow based on the provided user roles input.

    Args:
        user_roles: Input parameter of type str

    Returns:
        str: Output of type str
    """
    # --- PURE IMPLEMENTATION ---
    import re
    
    # Step 1: Accept either a comma-separated string, semicolon separated, or basic list-resembling string
    # Normalize input to a list of role strings
    if isinstance(user_roles, str):
        # Remove any brackets or array-like characters, split by comma, semicolon, or whitespace if necessary
        input_clean = user_roles.strip().strip('[](){}')
        # Attempt to split on commas or semicolons
        if ',' in input_clean:
            role_candidates = [r.strip() for r in input_clean.split(',')]
        elif ';' in input_clean:
            role_candidates = [r.strip() for r in input_clean.split(';')]
        else:
            # If it's a single word or phrase
            role_candidates = [input_clean.strip()]
    elif isinstance(user_roles, list):
        role_candidates = [str(r).strip() for r in user_roles]
    else:
        return "No user roles specified."

    # Remove any empty strings
    roles = [r for r in role_candidates if r]

    if not roles:
        return "No user roles specified."

    # Step 2: Format into a clear human-readable, prose-based section
    # Adapt output based on the number of roles, using proper conjunctions and Oxford comma
    if len(roles) == 1:
        return f"Primary user role: {roles[0]}."
    elif len(roles) == 2:
        return f"Primary user roles: {roles[0]} and {roles[1]}."
    else:
        # Oxford comma for more than 2 items
        prose = ', '.join(roles[:-1]) + f", and {roles[-1]}"
        return f"Primary user roles: {prose}."
