def extract_explicit_user_roles_from_requirements(text: str, context_kwargs: str) -> List[str]:
    """
    This function parses the provided requirements text and context to identify and return an explicit, type-safe list of user role names that are directly mentioned as participants in the workflow.

    Args:
        text: Input parameter of type str
context_kwargs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re
    import json
    from typing import List
    
    # --- 1. Define keyword dictionaries and patterns for roles ---
    # Common user role/persona tokens; extend as needed
    # These can be tailored, or sourced from context_kwargs if provided
    COMMON_ROLE_KEYWORDS = [
        'user', 'admin', 'administrator', 'editor', 'reviewer', 'approver', 'requester', 
        'customer', 'manager', 'operator', 'moderator', 'analyst', 'auditor', 'contributor', 
        'agent', 'employee', 'client', 'applicant', 'participant', 'supervisor', 'superuser',
        'owner', 'guest', 'author', 'recipient', 'issuer', 'reader', 'submitter', 'observer'
    ]
    # Build a regex pattern to match these as whole words (case-insensitive)
    role_pattern = re.compile(r'\b(' + '|'.join(COMMON_ROLE_KEYWORDS) + r')s?\b', re.IGNORECASE)
    
    # --- 2. Try to enrich with additional roles from context_kwargs (if any) ---
    extra_context_roles = set()
    if context_kwargs:
        try:
            context_obj = json.loads(context_kwargs)
            # Try common keys that might contain roles
            likely_role_keys = ['roles', 'user_roles', 'participants', 'actors']
            for k in likely_role_keys:
                if k in context_obj and isinstance(context_obj[k], list):
                    for val in context_obj[k]:
                        # Only accept non-empty strings
                        if isinstance(val, str) and val.strip():
                            extra_context_roles.add(val.strip())
        except Exception:
            pass  # Ignore invalid JSON or missing context
    
    # --- 3. Parse the text for explicit user role/persona mentions ---
    raw_roles: List[str] = []

    # Strategy: Look for nouns matching role keywords, possibly in capitalized form or as proper nouns.
    # Optionally, enrich the pattern by looking for occurrences like:
    # "the [role]", "as a[n] [role]", "by the [role]", etc.
    # For simplicity, collect all hits, dedupe later.
    for match in role_pattern.finditer(text):
        role = match.group(1)
        # Normalize: lowercase singular
        raw_roles.append(role.lower())

    # --- 4. Attempt to capture additional, custom or domain-specific roles
    # Example: Roles may be phrases like "Data Entry Clerk" or "Chief Financial Officer"
    # Heuristic: Look for patterns/phrases near typical user-mentioning constructions
    # e.g. "as a Data Entry Clerk", "the Request Author", etc.
    custom_role_pattern = re.compile(r'(?:as an? |by the |the |by an? |for the |for an? )([A-Z][a-z]+(?: [A-Z][a-z]+)*)')
    for match in custom_role_pattern.finditer(text):
        # Only keep if phrase is reasonably role-like and not a generic term
        role_candidate = match.group(1)
        # Filter out if it overlaps clearly with previous matches
        if role_candidate.lower() not in COMMON_ROLE_KEYWORDS and len(role_candidate.split()) <= 5:
            raw_roles.append(role_candidate.strip())

    # --- 5. Merge with context roles, de-duplicate ---
    all_roles_set = set([r.strip().lower() for r in raw_roles if r.strip()]) | set([r.strip().lower() for r in extra_context_roles if isinstance(r, str) and r.strip()])
    # Post-process to make role names more type-safe (e.g., capitalize words)
    def canonicalize(role: str) -> str:
        role = role.strip()
        # If it's a recognized built-in role, canonicalize as lowercase
        if role in COMMON_ROLE_KEYWORDS:
            return role
        # Else, Title Case for multiword custom roles
        return ' '.join([w.capitalize() for w in role.split()])
    
    roles_final = []
    seen = set()
    for r in all_roles_set:
        if not r or not isinstance(r, str):
            continue
        canon = canonicalize(r)
        # Guard against empty or obviously invalid names
        if canon and canon.lower() not in seen:
            roles_final.append(canon)
            seen.add(canon.lower())
    
    # Guard: Never return if list is empty
    return roles_final
