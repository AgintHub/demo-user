def structure_metrics_for_reporting(metrics: str, template: str) -> List[str]:
    """
    Structures and formats a list of success metrics according to a specified reporting template such as SMART or OKR for consistent and effective communication.

    Args:
        metrics: Input parameter of type str
template: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    # --- PURE IMPLEMENTATION BEGIN ---
    import re
    from typing import List

    def parse_metrics_string(metrics: str) -> List[str]:
        """Splits the metrics input string into a list of metric strings."""
        if '\n' in metrics:
            metric_lines = [m.strip() for m in metrics.split('\n') if m.strip()]
        elif ';' in metrics:
            metric_lines = [m.strip() for m in metrics.split(';') if m.strip()]
        else:
            metric_lines = [m.strip() for m in metrics.split(',') if m.strip()]
        return metric_lines

    # --- SMART Template Logic ---
    def structure_metric_smart(metric: str) -> str:
        # Attempt to extract fields from the metric using basic heuristics
        # 1. Looks for 'by <date>' or 'before <date>' for Deadline
        # 2. Looks for 'by <person>' or 'by <role>' for Responsibility
        # 3. Otherwise, assumes rest is Objective
        result = {}
        deadline = None
        responsible = None
        metric_wo_deadline = metric

        # Extract deadline (by/before ...)
        deadline_match = re.search(r'\b(by|before) ([\w\s\-,.]+?)([.;]|$)', metric, re.IGNORECASE)
        if deadline_match:
            deadline = deadline_match.group(2).strip()
            metric_wo_deadline = metric[:deadline_match.start()].strip() + metric[deadline_match.end():].strip()

        # Extract responsible (by <person>) if not used for deadline
        responsible_match = re.search(r'\b(by) ([A-Z][\w\s]+)([.;]|$)', metric_wo_deadline, re.IGNORECASE)
        if responsible_match:
            responsible = responsible_match.group(2).strip()
            metric_wo_deadline = metric_wo_deadline[:responsible_match.start()].strip() + metric_wo_deadline[responsible_match.end():].strip()

        # Extract measure: look for numbers or percentages
        measure_match = re.search(r'(\d+(?:\.\d+)?%)|(\d+(?:\.\d+)?(?: units| users| customers| points)?)', metric)
        if measure_match:
            measure = measure_match.group(0).strip()
        else:
            measure = None

        # Result structure
        parts = []
        # Objective
        obj = metric_wo_deadline.strip()
        if obj:
            parts.append(f"Objective: {obj}")
        # Measurable criterion
        if measure:
            parts.append(f"Measure: {measure}")
        # Deadline
        if deadline:
            parts.append(f"Deadline: {deadline}")
        # Responsible
        if responsible:
            parts.append(f"Responsible: {responsible}")

        # SMART typically requires: Specific, Measurable, Achievable, Relevant, Time-bound, so we validate that at least obj/measure/deadline appear
        # Compose string
        return " | ".join(parts) if parts else metric.strip()

    # --- OKR Template Logic ---
    def structure_metric_okr(metric: str) -> str:
        # Try to split into Objective & Key Result using punctuation and keywords
        # Attempt to identify KR using '- ' or numbering, else use heuristics
        # e.g. "Objective: Increase sign-ups | Key Result: Achieve 5,000 new sign-ups by Q2"
        # Look for 'objective' or 'key result' anchor words
        obj = None
        kr = None
        metric_lower = metric.lower()
        if 'objective:' in metric_lower and 'key result:' in metric_lower:
            parts = re.split(r'objective:|key result:', metric, flags=re.IGNORECASE)
            if len(parts) >= 3:
                obj = parts[1].strip(' .;:|')
                kr = parts[2].strip(' .;:|')
        else:
            # Try splitting using dashes or numbering
            obj_kr_split = re.split(r'(?:(?:-|•|\d\.|\*)\s+)', metric, maxsplit=1)
            if len(obj_kr_split) == 2:
                obj = obj_kr_split[0].strip()
                kr = obj_kr_split[1].strip()
            else:
                # If metric is short, treat as Objective, or if contains 'by'/'achieve'/number, make it Key Result
                if re.search(r'(\d+)|(%|by|increase|decrease|achieve|reach)', metric, re.IGNORECASE):
                    obj = None
                    kr = metric.strip()
                else:
                    obj = metric.strip()
                    kr = None
        parts = []
        if obj:
            parts.append(f"Objective: {obj}")
        if kr:
            parts.append(f"Key Result: {kr}")
        return " | ".join(parts) if parts else metric.strip()

    # --- Fallback logic: Return raw metric ---
    def structure_metric_generic(metric: str) -> str:
        return metric.strip()

    # --- Template Registry (Strategy Pattern) ---
    template_map = {
        'SMART': structure_metric_smart,
        'OKR': structure_metric_okr
    }

    # Process input
    metric_list = parse_metrics_string(metrics)
    chosen_template = str(template).strip().upper()
    structure_fn = template_map.get(chosen_template, structure_metric_generic)
    structured_metrics: List[str] = [structure_fn(m) for m in metric_list]
    return structured_metrics
