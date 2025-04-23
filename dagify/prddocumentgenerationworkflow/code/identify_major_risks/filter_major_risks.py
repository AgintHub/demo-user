def filter_major_risks(risks: str, filter_mode: str) -> List[str]:
    """
    Filters a list of risk objects to retain only those that are actionable or critical according to the specified filtering mode.

    Args:
        risks: Input parameter of type str
filter_mode: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    import json
    
    # Deserialize the input risks string to a list of dicts (if already a list, skip this step)
    try:
        risks_list = json.loads(risks)
    except Exception as e:
        raise ValueError("Input 'risks' must be JSON-encoded list of dicts.") from e
    if not isinstance(risks_list, list):
        raise ValueError("Input 'risks' JSON does not decode to a list.")

    # Filter by mode:
    filter_mode_lc = filter_mode.lower().strip()
    
    def is_actionable(risk_dict: dict) -> bool:
        # Define what makes a risk 'actionable' based on common fields/tags.
        tags = risk_dict.get('tags') or risk_dict.get('labels') or []
        if isinstance(tags, str):
            tags = [tags]
        tags_lc = [str(t).lower() for t in tags]
        status = str(risk_dict.get('status', '')).lower()
        # Consider as actionable if tag or status contains 'actionable'.
        return 'actionable' in tags_lc or status == 'actionable'

    def is_critical(risk_dict: dict) -> bool:
        tags = risk_dict.get('tags') or risk_dict.get('labels') or []
        if isinstance(tags, str):
            tags = [tags]
        tags_lc = [str(t).lower() for t in tags]
        severity = str(risk_dict.get('severity', '')).lower()
        # Consider as critical if tag or severity contains 'critical' or 'high'.
        return (
            'critical' in tags_lc or 'high' in tags_lc or
            severity in ['critical', 'high']
        )

    # Logical filtering
    filtered_risks = []
    for risk in risks_list:
        if filter_mode_lc == 'actionable':
            if is_actionable(risk):
                filtered_risks.append(risk)
        elif filter_mode_lc == 'critical':
            if is_critical(risk):
                filtered_risks.append(risk)
        elif filter_mode_lc == 'actionable_or_critical' or filter_mode_lc == 'actionable_or_major':
            # Accept if either rule matches
            if is_actionable(risk) or is_critical(risk):
                filtered_risks.append(risk)
        else:
            # If unknown filter_mode, default to passthrough (do not filter)
            filtered_risks.append(risk)

    # The structure and integrity of each original risk dict is maintained.
    # Convert back to JSON strings for each dict to match List[str] return type.
    return [json.dumps(risk, separators=(',', ':')) for risk in filtered_risks]
