def extract_constraints_from_inputs(inputs: str) -> List[str]:
    """
    Extracts a list of constraints (as strings) from the provided input string, typically aggregating any constraints identified in prior workflow steps.

    Args:
        inputs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re
    
    # Define a set of indicative keywords/phrases for constraints (expand as needed)
    constraint_keywords = [
        r"must not",
        r"must",
        r"should not",
        r"should",
        r"cannot",
        r"can not",
        r"may not",
        r"is required to",
        r"is not permitted to",
        r"cannot exceed",
        r"no more than",
        r"at least",
        r"less than",
        r"greater than",
        r"between",
        r"limited to",
        r"restricted to",
        r"prohibited",
        r"forbidden",
        r"avoid",
        r"exclusive",
        r"mandatory",
        r"necessary"
    ]

    # Lowercase for case-insensitive pattern matching
    lowered = inputs.lower()

    # Build a regex pattern to match sentences or clauses containing constraint keywords
    # Pattern will split the input into sentences, then filter sentences containing constraint keywords
    sentence_pattern = re.compile(r'[^.!?]+[.!?]?')
    sentences = [s.strip() for s in sentence_pattern.findall(inputs) if s.strip()]

    extracted_constraints = []
    for sentence in sentences:
        sentence_lc = sentence.lower()
        for kw in constraint_keywords:
            if re.search(r'\b' + kw + r'\b', sentence_lc):
                extracted_constraints.append(sentence.strip())
                break  # Only need to include a sentence once

    # If unconventionally phrased constraints exist, try extracting clauses (semicolon/comma separated) as fallback
    if not extracted_constraints:
        clauses = [cl.strip() for cl in re.split(r'[;\n]', inputs) if cl.strip()]
        for clause in clauses:
            clause_lc = clause.lower()
            for kw in constraint_keywords:
                if re.search(r'\b' + kw + r'\b', clause_lc):
                    extracted_constraints.append(clause.strip())
                    break

    # Fallback: if still nothing, try matching any segment with "must", "should", "not allowed" etc.
    if not extracted_constraints:
        fallback_keywords = [r"must", r"should", r"not allowed", r"cannot"]
        for kw in fallback_keywords:
            matches = re.findall(rf'([^.!?]*?{kw}[^.!?]*[.!?])', lowered)
            for m in matches:
                extracted_constraints.append(m.strip())

    # Standardize: lowercase, strip, deduplicate
    standardized = set()
    for c in extracted_constraints:
        norm_c = ' '.join(c.lower().split()).strip()
        if norm_c:
            standardized.add(norm_c)

    # Return sorted for consistency
    return sorted(standardized)
