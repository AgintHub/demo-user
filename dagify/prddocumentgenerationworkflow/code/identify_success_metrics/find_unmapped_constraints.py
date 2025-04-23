def find_unmapped_constraints(constraints: str, metrics: str) -> List[str]:
    """
    Identifies which constraints from the input list have not been explicitly mapped to any of the provided success metrics.

    Args:
        constraints: Input parameter of type str
metrics: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import json
    import re

    def parse_items(text):
        text = text.strip()
        if not text:
            return []
        # Try to parse as JSON list
        try:
            items = json.loads(text)
            if isinstance(items, list):
                return [str(item).strip() for item in items]
            # If it's a dict or string (not list), treat as fallback
        except Exception:
            pass
        # Fallback: parse as line/semicolon/comma list
        if '\n' in text:
            items = [s.strip() for s in text.split('\n') if s.strip()]
        elif ';' in text:
            items = [s.strip() for s in text.split(';') if s.strip()]
        elif ',' in text:
            items = [s.strip() for s in text.split(',') if s.strip()]
        else:
            items = [text]
        return items

    constraint_list = parse_items(constraints)
    metric_list = parse_items(metrics)

    unmapped = []
    for constraint in constraint_list:
        found = False
        constraint_lower = constraint.strip().lower()
        # Remove punctuation for more robust matching
        constraint_nopunct = re.sub(r'[^a-z0-9 ]+', '', constraint_lower)
        for metric in metric_list:
            metric_lower = metric.strip().lower()
            metric_nopunct = re.sub(r'[^a-z0-9 ]+', '', metric_lower)
            # Direct or substring match (case-insensitive, lenient)
            if constraint_lower in metric_lower or constraint_nopunct in metric_nopunct:
                found = True
                break
            # Lenient fuzzy-like match: Do all words in constraint appear in metric?
            constraint_words = set(constraint_nopunct.split())
            metric_words = set(metric_nopunct.split())
            # If most words overlap, consider as matched
            if constraint_words and (len(constraint_words & metric_words) >= max(1, len(constraint_words)//2)):
                found = True
                break
        if not found:
            unmapped.append(constraint)
    return unmapped
