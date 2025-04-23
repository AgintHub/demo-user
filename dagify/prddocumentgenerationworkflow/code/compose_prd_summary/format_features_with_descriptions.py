def format_features_with_descriptions(feature_names: str, feature_descriptions: str) -> str:
    """
    This node combines two lists—feature names and their descriptions—into a single, human-readable formatted string pairing each feature with its respective description.

    Args:
        feature_names: Input parameter of type str
feature_descriptions: Input parameter of type str

    Returns:
        str: Output of type str
    """
    # --- PURE IMPLEMENTATION ---
    import json
    
    # Attempt to parse the inputs as JSON lists, or fallback to comma-split
    def parse_list(s):
        try:
            lst = json.loads(s)
            if isinstance(lst, list):
                return lst
        except Exception:
            pass
        # fallback: comma separated
        return [item.strip() for item in s.split(',') if item.strip()]
    
    names_list = parse_list(feature_names)
    descriptions_list = parse_list(feature_descriptions)

    if len(names_list) != len(descriptions_list):
        raise ValueError(f"feature_names and feature_descriptions must be of the same length (got {len(names_list)} and {len(descriptions_list)})")

    lines = []
    for name, desc in zip(names_list, descriptions_list):
        lines.append(f"- {name}: {desc}")
    
    formatted = "\n".join(lines)
    return formatted
