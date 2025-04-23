def document_risks_with_rationale(risks: str, constraints: str) -> List[str]:
    """
    Takes a list of identified risks and associated constraints to produce structured documentation linking each risk to rationale and references to specific constraints.

    Args:
        risks: Input parameter of type str
constraints: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    import re
    import json

    # Helper: Split input text into list of items, treating each nonempty line as an item.
    def parse_list_items(text: str) -> list:
        # Try for numbered/bulleted list; else fallback to nonempty lines
        # Match patterns like: 1. something, - something, * something
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        items = []
        for line in lines:
            match = re.match(r'^(\d+\.|[-*])\s+(.*)$', line)
            if match:
                items.append(match.group(2).strip())
            else:
                items.append(line)
        return [i for i in items if i]

    # Correlate each risk to relevant constraints by looking for overlap/causal link in words
    def correlate_risk_constraints(risk_text: str, constraints: list) -> list:
        # Naive keyword overlap: for each constraint, count shared lowercased non-stopword words
        import string
        stopwords = set([
            'the', 'and', 'or', 'of', 'in', 'to', 'a', 'by', 'for', 'is', 'with', 'on', 'at', 'be', 'that',
            'as', 'may', 'will', 'from', 'if', 'an', 'this', 'are', 'all', 'can', 'which', 'it', 'their', 'not',
            'any', 'but', 'we', 'do', 'should', 'must', 'our', 'there', 'these', 'per', 'due', 'so', 'such', 'also'
        ])
        def tokenize(s):
            s = s.lower().translate(str.maketrans('', '', string.punctuation))
            words = s.split()
            return set([w for w in words if w and w not in stopwords])
        risk_words = tokenize(risk_text)
        matches = []
        for c in constraints:
            constraint_words = tokenize(c)
            shared = risk_words & constraint_words
            # If risk matches at least one word in constraint, count as relevant
            if shared:
                matches.append(c)
        # If nothing matched, fallback to NONE
        if not matches:
            # Optionally: try soft/semantic match or just link all? But per PRD, avoid disconnected risks
            # For fallback, return [] (downstream output will show empty associated_constraints)
            pass
        return matches

    # Generate rationale string for this risk
    def generate_rationale(risk: str, associated_constraints: list) -> str:
        if associated_constraints:
            constraints_str = '; '.join(associated_constraints)
            rationale = (
                f"This risk ('{risk}') was identified due to its connection with the following constraint(s): {constraints_str}. "
                f"If these constraints are breached or not managed, the described risk may materialize and impact workflow objectives."
            )
        else:
            rationale = (
                f"This risk ('{risk}') was identified independently and lacks direct traceable constraint linkage in the provided context. "
                f"Nonetheless, inclusion is warranted due to potential adverse impact if not considered in mitigation planning."
            )
        return rationale

    # Parse risks & constraints
    risk_list = parse_list_items(risks)
    constraint_list = parse_list_items(constraints)

    documented = []
    for risk in risk_list:
        associated_constraints = correlate_risk_constraints(risk, constraint_list)
        rationale = generate_rationale(risk, associated_constraints)
        doc = {
            'risk_description': risk,
            'rationale': rationale,
            'associated_constraints': associated_constraints
        }
        documented.append(doc)

    # Output each as a JSON string
    output_list = [json.dumps(doc, ensure_ascii=False) for doc in documented]
    return output_list
