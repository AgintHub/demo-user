def extract_explicit_constraints(text: str, matchers: str) -> List[str]:
    """
    Extracts all explicit technical or business constraints from input text using pattern-based matchers, returning each constraint as a structured list of strings.

    Args:
        text: Input parameter of type str
matchers: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re
    from typing import List
    
    # --- Step 1: Parse the matchers string ---
    # Assume matchers are comma, semicolon, or newline-separated (configurable string input)
    if not matchers or not isinstance(matchers, str):
        matcher_list: List[str] = []
    else:
        matcher_list = [m.strip() for m in re.split(r'[;,\n]', matchers) if m.strip()]

    if not matcher_list:
        return []

    # --- Step 2: Build regular expressions for each matcher (case-insensitive, word-bound matched if needed) ---
    # Prefer to match full sentences or phrases containing the matcher keyword
    constraint_patterns = []
    for keyword in matcher_list:
        # Escape regex special chars in matcher keyword
        escaped = re.escape(keyword)
        # Build patterns that capture sentences containing the matcher (basic sentence boundaries, liberal)
        # e.g., 'must', 'shall', etc. -- match the whole sentence containing the keyword
        # Use (?i) for case-insensitivity, [^.!?]*? to stop at next sentence-ending punct.
        pattern = rf'(?i)([^.!?]*\b{escaped}\b[^.!?]*[.!?])'
        constraint_patterns.append(pattern)
    
    # --- Step 3: Extract candidate constraints using the patterns ---
    explicit_constraints = set()
    for pattern in constraint_patterns:
        for match in re.finditer(pattern, text):
            constraint_candidate = match.group(0).strip()
            # --- Step 4: Validation - Ensure unambiguous/explicit language ---
            # Accept only constraints that use clear modal verbs ('must', 'shall', 'is required to', 'cannot', etc.)
            # and avoid those starting with guesswork words (e.g. 'should', 'could', 'might')
            constraint_lc = constraint_candidate.lower()
            explicit_keywords = [
                'must', 'shall', 'is required to', 'are required to',
                'cannot', 'may not', 'will not', 'is not allowed', 'are not allowed'
            ]
            ambiguous_filters = [
                'should', 'could', 'might', 'may', 'suggests', 'recommend', 'prefer'
            ]
            # Must contain at least one explicit keyword
            if any(kw in constraint_lc for kw in explicit_keywords):
                # Exclude if it contains ambiguity words
                if not any(ambig in constraint_lc for ambig in ambiguous_filters):
                    explicit_constraints.add(constraint_candidate)
    
    # Return as a sorted list for determinism
    return sorted(explicit_constraints)
