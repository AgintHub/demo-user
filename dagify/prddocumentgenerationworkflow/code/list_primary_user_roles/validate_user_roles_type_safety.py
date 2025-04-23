def validate_user_roles_type_safety(user_roles: str) -> List[str]:
    """
    This node validates and enforces type-safety on a list of user roles, ensuring all entries are unique, non-empty strings before returning the cleaned List[str].

    Args:
        user_roles: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import ast

    # Step 1: Deserialize the str input to a list (assuming JSON or str(list) format)
    try:
        user_roles_list = ast.literal_eval(user_roles)
    except Exception:
        # If parsing fails, return an empty list (or raise, depending on policy)
        return []

    if not isinstance(user_roles_list, list):
        return []

    # Step 2: Clean and validate each item
    cleaned_roles = []
    for role in user_roles_list:
        # Ensure the item is a string
        if not isinstance(role, str):
            # Try to coerce to string if possible
            try:
                role = str(role)
            except Exception:
                continue
        # Remove whitespace around the string
        role_stripped = role.strip()
        if role_stripped:
            cleaned_roles.append(role_stripped)

    # Step 3: Remove duplicates while preserving order
    seen = set()
    unique_roles = []
    for role in cleaned_roles:
        if role not in seen:
            seen.add(role)
            unique_roles.append(role)

    return unique_roles
