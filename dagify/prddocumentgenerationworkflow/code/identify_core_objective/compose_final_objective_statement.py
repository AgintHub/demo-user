def compose_final_objective_statement(base_objective: str, sequencing: str, constraints: str) -> str:
    """
    Synthesizes a final, clear, and comprehensive core objective statement by integrating the base objective, required sequencing (such as mandated meeting order), and relevant constraints as described in workflow requirements.

    Args:
        base_objective: Input parameter of type str
sequencing: Input parameter of type str
constraints: Input parameter of type str

    Returns:
        str: Output of type str
    """
    # 1. Trim all inputs and check for non-empty elements
    base = base_objective.strip() if base_objective else ''
    seq = sequencing.strip() if sequencing else ''
    cons = constraints.strip() if constraints else ''

    # 2. Validate presence of all non-empty elements
    missing = []
    if not base:
        missing.append('base_objective')
    if not seq:
        missing.append('sequencing')
    if not cons:
        missing.append('constraints')
    if missing:
        raise ValueError(f"Missing required statement fragments: {', '.join(missing)}")

    # 3. Compose following a logical order:
    #    (a) State sequencing/temporal order first (if non-empty),
    #    (b) then the base objective (the main action),
    #    (c) then constraints after (framed as conditions or caveats).
    # Compose sentences so it's fluent as English.
    import re

    # Capitalization and punctuation helpers
    def _ensure_ends_with_period(text):
        text = text.rstrip()
        return text if text.endswith('.') else text + '.'

    def _lower_first(text):
        if not text: return text
        return text[0].lower() + text[1:]

    # Compose parts
    # 1. Sequencing: "First, ..." or "Before X, ..."
    sequencing_phrase = ''
    if seq:
        seq_clean = seq.rstrip('.')
        # If sequencing already starts with a temporal keyword, just capitalize
        if re.match(r"^(first|before|after|then|when|once|prior to|following|upon)\b", seq_clean, re.IGNORECASE):
            sequencing_phrase = seq_clean[0].upper() + seq_clean[1:]
        else:
            sequencing_phrase = f"First, {seq_clean}"   # Fallback
        sequencing_phrase = _ensure_ends_with_period(sequencing_phrase)

    # 2. Base Objective
    base_phrase = base.rstrip('.')
    # Start base objective sentence with uppercase
    base_phrase = base_phrase[0].upper() + base_phrase[1:]
    base_phrase = _ensure_ends_with_period(base_phrase)

    # 3. Constraints
    constraints_phrase = ''
    if cons:
        cons_clean = cons.rstrip('.')
        # Try to start as a dependent clause, e.g. "Ensure ...", "Making sure ...", or "while ..."
        # If it starts with 'must', 'ensure', 'only if', etc., keep as is
        if re.match(r"^(must|ensure|making|only if|unless|while|provided that|so that)\b", cons_clean, re.IGNORECASE):
            constraints_phrase = cons_clean[0].upper() + cons_clean[1:]
        else:
            constraints_phrase = f"Ensure {cons_clean}" if not cons_clean.lower().startswith('ensure') else cons_clean
        constraints_phrase = _ensure_ends_with_period(constraints_phrase)

    # 4. Combine logically: [Sequencing.] [Base Objective.] [Constraints.]
    # If sequencing is non-empty, prepend; always include base; append constraints if any.
    parts = []
    if sequencing_phrase:
        parts.append(sequencing_phrase)
    parts.append(base_phrase)
    if constraints_phrase:
        parts.append(constraints_phrase)

    statement = ' '.join(parts)

    # 5. Post-validation: ensure all key fragments appear at least approximately in the statement
    # (Case-insensitive containment test)
    for frag, label in [(base, 'base_objective'), (seq, 'sequencing'), (cons, 'constraints')]:
        if frag and frag.lower() not in statement.lower():
            raise ValueError(f"Fragment from {label} missing in composed statement.")

    return statement
