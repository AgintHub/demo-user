def map_constraints_to_metrics(constraints: str, objective: str) -> List[str]:
    """
    This node translates a set of workflow constraints and an objective statement into a list of specific, measurable success metrics aligned with those constraints.

    Args:
        constraints: Input parameter of type str
objective: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re
    from typing import List
    
    # Split constraints into list (support bullet points, line breaks, or semicolons)
    raw_constraints = [c.strip() for c in re.split(r'[\n\r\-\*\u2022;]+', constraints) if c.strip()]

    metrics = []
    
    for idx, constraint in enumerate(raw_constraints):
        base_constraint = constraint
        # Classify constraint type: quantitative vs qualitative
        quantitative_keywords = [
            'less than', 'at least', 'no more than', 'greater than', 'fewer than',
            'between', 'range', 'must be', 'limit', 'threshold', 'target', '%',
            'more than', 'equal to', 'per day', 'per hour', 'within', 'allowed', "maximum", "minimum", "not exceed", "should not exceed", "no less than"
        ]
        qualitative_keywords = [
            'ensure', 'make sure', 'confirm', 'verify', 'should be', 'must be',
            'required to', 'subjective', 'review', 'policy', 'approval',
            'compliant', 'aligned', 'appropriate', 'adherence', 'consistency',
            'documentation', 'demonstrate', 'quality', 'accuracy', 'reliable', 'timely', 'prompt', 'effective', 'customer satisfaction', 'feedback'
        ]

        constraint_lower = constraint.lower()
        is_quant = False
        for kw in quantitative_keywords:
            if kw in constraint_lower:
                is_quant = True
                break

        is_qual = False
        for kw in qualitative_keywords:
            if kw in constraint_lower:
                is_qual = True
                break

        # If both, prefer quantitative. If neither, default to qualitative.
        metric_type = 'quantitative' if is_quant else 'qualitative'

        # Generate metric text
        if metric_type == 'quantitative':
            # Heuristic: extract any numbers for metric target
            numbers = re.findall(r'\d+[\.]?\d*', constraint)
            target = numbers[0] if numbers else '<specify target>'
            metric_description = (
                f"% of cases where constraint '{constraint}' is satisfied in alignment with objective: {objective}. "
                f"Target: {target} (traced to constraint {idx+1})."
            )
        else:
            metric_description = (
                f"Audit checklist for: '{constraint}'. Track rate of compliance and periodic qualitative review for alignment with objective: {objective}. "
                f"Trace: constraint {idx+1} ('{constraint}')."
            )

        metrics.append(metric_description)

    return metrics
