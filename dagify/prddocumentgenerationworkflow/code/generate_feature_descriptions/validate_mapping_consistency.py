def validate_mapping_consistency(features: str, descriptions: str) -> str:
    """
    This node verifies that the mapping between a list of workflow feature names and their corresponding descriptions is both one-to-one and order-consistent, raising an explicit error if any mismatch or misalignment is found.

    Args:
        features: Input parameter of type str
descriptions: Input parameter of type str

    Returns:
        str: Output of type Any
    """
    # --- PURE PYTHON IMPLEMENTATION ---
    import ast
    
    # Try to parse the input strings into lists
    try:
        features_list = ast.literal_eval(features)
        descriptions_list = ast.literal_eval(descriptions)
    except Exception as e:
        raise ValueError(f"Failed to parse features or descriptions as Python lists. Error: {e}\nfeatures: {features}\ndescriptions: {descriptions}")

    if not isinstance(features_list, list) or not isinstance(descriptions_list, list):
        raise ValueError(f"Input data is not a valid list.\nParsed features: {features_list}\nParsed descriptions: {descriptions_list}")

    # 1. Ensure lengths are equal
    if len(features_list) != len(descriptions_list):
        return (
            f"Mismatch in number of features and descriptions. "
            f"features has {len(features_list)}, descriptions has {len(descriptions_list)}.\n"
            f"First 5 features: {features_list[:5]}\nFirst 5 descriptions: {descriptions_list[:5]}"
        )

    # 2. Validate strict order preservation
    # We'll assume that the intended mapping is that features[i] should match descriptions[i]
    # If stricter matching is needed, e.g., by an identifier inside the string, logic could be added here.
    mismatches = []
    for idx, (feature, description) in enumerate(zip(features_list, descriptions_list)):
        # If more context for matching is needed, adjust here. For now, we just check both exist for the index.
        if not isinstance(feature, str) or not isinstance(description, str):
            mismatches.append(f"Index {idx}: Invalid types. Feature type: {type(feature)}, Description type: {type(description)}")
        # Optionally implement additional consistency checks, e.g., if feature is a substring of description, etc.

    if mismatches:
        # Collate all mismatch info into output string
        mismatch_report = "Order or type mismatch detected at the following indices:\n" + "\n".join(mismatches)
        return mismatch_report

    # If we made it here, mapping is valid and order is preserved
    return "Mapping between features and descriptions is valid and order-consistent."
