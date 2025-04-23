def apply_sequencing_clauses_to_descriptions(feature_names: str, descriptions: str, sequencing_node: str, rationale: str) -> str:
    """
    This node modifies feature descriptions by appending or integrating mandatory sequencing clauses and their rationale for any feature matching a specified sequencing node.

    Args:
        feature_names: Input parameter of type str
descriptions: Input parameter of type str
sequencing_node: Input parameter of type str
rationale: Input parameter of type str

    Returns:
        str: Output of type Any
    """
    import json

    # Parse the input strings into Python lists
    try:
        names_list = json.loads(feature_names)
    except Exception as e:
        raise ValueError("feature_names input must be a JSON-formatted list of strings") from e

    try:
        desc_list = json.loads(descriptions)
    except Exception as e:
        raise ValueError("descriptions input must be a JSON-formatted list of strings") from e

    # Make sure both lists are aligned
    if not isinstance(names_list, list) or not isinstance(desc_list, list):
        raise TypeError("feature_names and descriptions must parse to lists of strings")
    if len(names_list) != len(desc_list):
        raise ValueError("feature_names and descriptions must have the same length")

    # Define sequencing clause template
    # Example: "This step must occur before <sequencing_node>. Rationale: <rationale>."
    sequencing_clause = f" This step must occur before '{sequencing_node}'. Rationale: {rationale}" if rationale else f" This step must occur before '{sequencing_node}'."

    updated_desc_list = []
    for i, (fname, dsc) in enumerate(zip(names_list, desc_list)):
        if sequencing_node.lower() in fname.lower():
            # Feature matches the sequencing node, append the sequencing clause
            # Use punctuation and conjunction per PRD
            if dsc.strip().endswith('.'):
                new_desc = f"{dsc.strip()} {sequencing_clause.strip()}"
            else:
                new_desc = f"{dsc.strip()}. {sequencing_clause.strip()}"
            updated_desc_list.append(new_desc)
        else:
            # Leave as is
            updated_desc_list.append(dsc)
    # Output as JSON-formatted string for downstream consumption
    return json.dumps(updated_desc_list)
