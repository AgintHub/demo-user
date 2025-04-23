def generate_quant_qual_metrics(metrics: str, constraints: str, core_objective: str) -> List[str]:
    """
    This shim enriches a provided list of workflow success metrics by generating both quantitative and qualitative success criteria, ensuring alignment with specified constraints and the core objective.

    Args:
        metrics: Input parameter of type str
constraints: Input parameter of type str
core_objective: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    # --- PURE IMPLEMENTATION: Replacing SHIMS with real logic ---
    import re
    from typing import List

    # Helper: Split semicolon, newline, or numbered/bulleted lists into a list of metric strings
    def parse_metrics(text: str) -> List[str]:
        if not text.strip():
            return []
        # Try splitting numbered/bulleted or semi-colon/newline lists
        split_lines = re.split(r'\s*(?:[-*]|\d+\.|\n|;)\s+', text)
        # Remove empties and trim
        return [line.strip() for line in split_lines if line.strip()]

    # Helper: Yield constraint -> metric type/description skeletons
    def map_constraint_to_metrics(constraint: str, core_objective: str) -> List[str]:
        """
        Returns a list of metric templates (quantitative and qualitative) for a constraint
        """
        results = []
        c = constraint.strip()
        if not c:
            return []
        # Naive keyword mapping for typical constraint patterns
        # Quantitative Rules
        quant_templates = [
            (r'time|duration|deadline|within (\d+|\w+) (minutes|hours|days|weeks)', lambda m: f"% of tasks completed on time ({c})"),
            (r'budget|cost|expense|under \$', lambda m: f"% of budget used ({c})"),
            (r'accuracy|error rate|correct|precision', lambda m: f"Accuracy rate for {core_objective} ({c})"),
            (r'completion|done|finish|achieve', lambda m: f"Task completion rate under {c}"),
            (r'number of|at least|no more than|maximum|minimum', lambda m: f"# of times {c} is met"),
        ]
        # Qualitative Rules
        qual_templates = [
            (r'satisfaction|feedback|user happiness|user experience|stakeholder', lambda m: f"User/stakeholder satisfaction score re: {c}"),
            (r'ease|usability|understand|clarity', lambda m: f"Usability rating for {core_objective} ({c})"),
        ]
        matched_quant = None
        for pattern, tmpl in quant_templates:
            if re.search(pattern, c, flags=re.IGNORECASE):
                matched_quant = tmpl(None)
                break
        if not matched_quant:
            matched_quant = f"% of times {c} is fulfilled (quantitative)"
        results.append(matched_quant)
        matched_qual = None
        for pattern, tmpl in qual_templates:
            if re.search(pattern, c, flags=re.IGNORECASE):
                matched_qual = tmpl(None)
                break
        if not matched_qual:
            matched_qual = f"Stakeholder agreement that {c} was met (qualitative)"
        results.append(matched_qual)
        return results

    # Helper: Validate and standardize metric sentence
    def standardize_metric(metric: str) -> str:
        cleaned = metric.strip().capitalize()
        if not cleaned.endswith('.'):
            cleaned = cleaned + '.'
        # Shorten multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned

    # Parse supplied metrics and constraints
    existing_metrics = parse_metrics(metrics)
    constraint_list = parse_metrics(constraints)

    # Copy & format supplied metrics
    generated_metrics = [standardize_metric(m) for m in existing_metrics]

    # Map constraints to at least one quant and one qual metric each
    for c in constraint_list:
        c_metrics = map_constraint_to_metrics(c, core_objective)
        # Only add if not already represented
        for cm in c_metrics:
            if all(cm.lower() not in em.lower() for em in generated_metrics):
                generated_metrics.append(standardize_metric(cm))

    # Coverage for core_objective itself (if not already explicit)
    if core_objective.strip():
        co_quant = f"% of {core_objective} achieved as per goals."
        co_qual = f"User/stakeholder perceived value of {core_objective}."
        for co_metric in (co_quant, co_qual):
            if all(co_metric.lower()[:10] not in gm.lower() for gm in generated_metrics):
                generated_metrics.append(standardize_metric(co_metric))

    # Final filter: Remove duplicates (case-insensitive)
    seen = set()
    deduped = []
    for m in generated_metrics:
        key = m.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(m)

    return deduped
