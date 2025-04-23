def extract_core_objective_from_requirements(requirements_text: str) -> str:
    """
    This node analyzes the requirements text to identify and articulate the primary workflow objective, integrating explicit sequencing requirements and ensuring reference to constraints is made for future workflow steps.

    Args:
        requirements_text: Input parameter of type str

    Returns:
        str: Output of type str
    """
    import re

    def extract_main_objective(text):
        # Try to extract the main goal using summary heuristics
        # 1. Look for sentences containing verbs like "define", "develop", "design", "implement", "establish" or similar main action verbs.
        # 2. Fall back to first (longest relevant) sentence if not found.
        objective_verbs = [
            'define', 'develop', 'design', 'implement', 'establish',
            'create', 'build', 'achieve', 'deliver', 'execute', 'launch', 'produce'
        ]
        sentences = re.split(r'[\.!?\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        scored = []
        for s in sentences:
            score = 0
            for v in objective_verbs:
                if re.search(r'\b' + re.escape(v) + r'(ing|e[sd]?|s)?\b', s, re.IGNORECASE):
                    score += 2
            # Nouns like 'workflow', 'process', 'system', etc, boost score
            if re.search(r'\b(workflow|process|system|solution|procedure|framework|plan|objective|goal|outcome)\b', s, re.IGNORECASE):
                score += 1
            scored.append((score, -len(s), s))
        # Select highest scoring sentence
        scored.sort(reverse=True)  # score, length (prefer longer), text
        if scored and scored[0][0] > 0:
            return scored[0][2]
        elif sentences:
            # Just take the first non-empty, longest candidate
            return max(sentences, key=len)
        else:
            return text.strip()

    def extract_sequencing_clauses(text):
        # Find temporal/dependency cues like 'before', 'after', 'prior to', 'once', 'following', etc.
        sequencing_keywords = r"before|after|prior to|once|following|when|until|upon|preceding|precedes|required prior to|must first|only after"
        clauses = []
        sequencing_regex = rf'([^.]*\b(?:{sequencing_keywords})\b[^.]*)'
        matches = re.findall(sequencing_regex, text, re.IGNORECASE)
        for m in matches:
            # Remove leading connective words: e.g. 'Before starting,', 'After the meeting,' -> 'the meeting'
            cleaned = re.sub(r'^[A-Z]?[a-z]+\b\,?\s*', '', m).strip(',;:. ')
            if cleaned and cleaned.lower() not in [c.lower() for c in clauses]:
                clauses.append(cleaned)
        return clauses

    def detect_constraints(text):
        # Look for phrases like 'must', 'should', 'cannot', 'may not', 'required to', 'have to', etc.
        constraint_markers = [
            r'\bmust\b', r'\bshould\b', r'\bcannot\b', r'\bmay not\b', r'\brequired to\b', r'\bhave to\b', r'\bneed to\b', r'\bare required to\b', r'\bshall\b', r'\bprohibited\b', r'\bnot allowed\b', r'\benforced\b'
        ]
        constraint_regex = '|'.join(constraint_markers)
        return bool(re.search(constraint_regex, text, re.IGNORECASE))

    # --- Main logic ---
    main_objective = extract_main_objective(requirements_text)
    # Ensure main_objective is a concise statement.
    main_objective = main_objective.rstrip('.;')
    additions = []

    # Add sequencing clause if present
    sequencing_clauses = extract_sequencing_clauses(requirements_text)
    if sequencing_clauses:
        # Combine into a readable clause, but avoid redundancy
        clause = ', '.join([c for c in sequencing_clauses if c.lower() not in main_objective.lower()])
        if clause:
            # Prepend as dependency phrase
            # e.g., "Objective statement, after X and before Y, "
            additions.append(f"Note: {clause}.")

    # Add constraint visibility if constraints detected
    if detect_constraints(requirements_text):
        additions.append("(subject to specified constraints)")

    # Construct final statement
    result = main_objective
    # Append additions for explicitness and visibility
    if additions:
        # Add as footnote or append to main clause, separated by '; '
        result = result + '; ' + ' '.join(additions)
    # Capitalize and return
    return result.strip()
