def add_traceability_to_metrics(metrics: str, constraints: str, node_reference: str) -> List[str]:
    """
    This node enriches a list of success metrics by appending traceability information that links each metric to the originating constraint or feature and the specific workflow node reference.

    Args:
        metrics: Input parameter of type str
constraints: Input parameter of type str
node_reference: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    # --- PURE IMPLEMENTATION ---
    import json
    from typing import Any

    def _normalize_to_list(input_str: str) -> list:
        """
        Try to parse input_str as JSON array.
        If fails, try splitting by newlines or commas and return a cleaned list.
        """
        try:
            val = json.loads(input_str)
            if isinstance(val, list):
                return val
            elif isinstance(val, str):
                # input_str is a string quoted, not a list
                return [val]
        except Exception:
            # Not JSON; try delimiting
            # First newlines, fallback to commas
            if '\n' in input_str:
                lines = [x.strip() for x in input_str.split('\n') if x.strip()]
                if lines:
                    return lines
            # else try commas
            items = [x.strip() for x in input_str.split(',') if x.strip()]
            return items if items else [input_str.strip()] if input_str.strip() else []

    def _normalize_constraint_item(item: Any) -> dict:
        """
        Try to ensure each constraint item is a dict with at least an 'id' or 'name' or summary fields for mapping.
        """
        if isinstance(item, dict):
            return item
        # Try to parse as JSON
        try:
            val = json.loads(item)
            if isinstance(val, dict):
                return val
            elif isinstance(val, str):
                return {"summary": val}
        except Exception:
            pass
        # Not JSON, just treat as summary
        return {"summary": str(item)}

    def _normalize_metric_item(item: Any) -> dict:
        """
        Try to parse as dict; else as plain text.
        """
        if isinstance(item, dict):
            return item
        try:
            val = json.loads(item)
            if isinstance(val, dict):
                return val
            elif isinstance(val, str):
                return {"metric": val}
        except Exception:
            pass
        # Not JSON, treat as plain metric text
        return {"metric": str(item)}

    metrics_list = _normalize_to_list(metrics)
    constraints_list = _normalize_to_list(constraints)

    # Further parse constraints into structured dicts for lookup/mapping
    structured_constraints = [_normalize_constraint_item(c) for c in constraints_list]
    structured_metrics = [_normalize_metric_item(m) for m in metrics_list]

    # For best effort mapping: try to assign each metric to the corresponding constraint by index, else fallback
    annotated_metrics = []
    for idx, metric in enumerate(structured_metrics):
        # Find corresponding constraint (by index)
        constraint = structured_constraints[idx] if idx < len(structured_constraints) else None
        # Extract identifier or summary for constraint
        constraint_desc = None
        if constraint:
            for key in ["id", "name", "summary", "constraint", "feature"]:
                if key in constraint:
                    constraint_desc = str(constraint[key])
                    break
            if not constraint_desc:
                constraint_desc = str(constraint)
        else:
            constraint_desc = "N/A"

        # Get metric main text
        metric_text = None
        for key in ["metric", "text", "description", "summary"]:
            if key in metric:
                metric_text = str(metric[key])
                break
        if not metric_text:
            # Fallback to string form
            metric_text = str(metric)
        # Format annotated string
        annotated = f"Metric: {metric_text} [constraint: {constraint_desc}, node: {node_reference}]"
        annotated_metrics.append(annotated)

    return annotated_metrics
