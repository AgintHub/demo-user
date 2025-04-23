def extract_constraints_from_parent_input(inputs: str, fallback_objective_output: str) -> List[str]:
    """
    This node extracts a list of explicit constraints from the parent node's input string or a fallback core objective output for use by dependent workflow nodes.

    Args:
        inputs: Input parameter of type str
fallback_objective_output: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re

    def extract_constraints(text: str) -> List[str]:
        # Attempt to extract constraints using common patterns.
        # Constraint markers: "must", "should", "cannot", "have to", "may not", "ensure", etc.
        # We'll try to match phrases like:
        #   - "must ..."
        #   - "should not ..."
        #   - "cannot ..."
        #   - etc.
        constraint_patterns = [
            r'\bmust\b[^.?!]*[.?!]',
            r'\bshould not\b[^.?!]*[.?!]',
            r'\bshould\b[^.?!]*[.?!]',
            r'\bhave to\b[^.?!]*[.?!]',
            r'\bmay not\b[^.?!]*[.?!]',
            r'\bcannot\b[^.?!]*[.?!]',
            r'\bcan not\b[^.?!]*[.?!]',
            r'\bmust not\b[^.?!]*[.?!]',
            r'\bensure that\b[^.?!]*[.?!]',
            r'\brequirement[s]? is that\b[^.?!]*[.?!]',
            r'\bit is required that\b[^.?!]*[.?!]',
        ]
        constraints = []
        for pat in constraint_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            constraints.extend([m.strip() for m in matches])
        # Fallback: if none found, try to chunk input using semicolon or bullet points as constraints.
        if not constraints:
            # Split by common separators/bullets
            bullet_points = re.split(r'\n\s*[-*•]\s*', text)
            for item in bullet_points:
                item = item.strip()
                if not item:
                    continue
                # Heuristic: consider as constraint if it contains 'must', 'should', etc.
                if re.search(r'\b(must|should|have to|cannot|can not|must not|may not|required|requirement|ensure)\b', item, re.IGNORECASE):
                    constraints.append(item)
        # Clean up constraints
        final_constraints = []
        for c in constraints:
            # Remove trailing whitespace, bullet marks, repeated spaces
            c = re.sub(r'^[-*•]\s*', '', c).strip()
            if c and c not in final_constraints:
                final_constraints.append(c)
        return final_constraints

    # Try extracting from primary input
    primary_constraints = extract_constraints(inputs)
    if primary_constraints:
        return primary_constraints
    # Fallback: extract from objective output
    fallback_constraints = extract_constraints(fallback_objective_output)
    return fallback_constraints
