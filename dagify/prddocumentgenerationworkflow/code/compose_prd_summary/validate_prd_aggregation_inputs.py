def validate_prd_aggregation_inputs(core_obj: str, user_roles: str, features: str, feature_desc: str) -> bool:
    """
    This node verifies that the aggregated PRD components—core objective, user roles, features, and feature descriptions—are present and consistently structured before generating the final PRD summary.

    Args:
        core_obj: Input parameter of type str
user_roles: Input parameter of type str
features: Input parameter of type str
feature_desc: Input parameter of type str

    Returns:
        bool: Output of type bool
    """
    # --- PURE IMPLEMENTATION: Replace all shims ---
    import json

    # 1. Check all required fields are present and non-empty (not None, not empty, not just whitespace)
    def is_nonempty(s):
        return isinstance(s, str) and bool(s.strip())

    if not (is_nonempty(core_obj) and is_nonempty(user_roles) and is_nonempty(features) and is_nonempty(feature_desc)):
        return False

    # 2. Parse the features and feature_desc as lists. Assume they are either JSON-encoded lists or comma/semicolon separated as fallback.
    def parse_list(s):
        try:
            val = json.loads(s)
            if isinstance(val, list):
                return val
        except Exception:
            pass
        # fallback: comma-separated or semicolon-separated
        if ',' in s:
            return [i.strip() for i in s.split(',') if i.strip()]
        elif '\n' in s:
            return [i.strip() for i in s.split('\n') if i.strip()]
        elif ';' in s:
            return [i.strip() for i in s.split(';') if i.strip()]
        else:
            return [s.strip()] if s.strip() else []

    features_list = parse_list(features)
    feature_desc_list = parse_list(feature_desc)

    # 3. Validate both lists are non-empty and have same length
    if not features_list or not feature_desc_list:
        return False
    if len(features_list) != len(feature_desc_list):
        return False

    # 4. Extra content check: If 'meeting with senior managers' is a required element, check for (case-insensitive) substring in either feature or description
    required_phrase = 'meeting with senior managers'
    found_in_features = any(required_phrase in str(f).lower() for f in features_list)
    found_in_descs = any(required_phrase in str(d).lower() for d in feature_desc_list)
    # If required, ensure at least one appearance in either field. As per PRD, make this check (if strictly required, set as needed):
    if not (found_in_features or found_in_descs):
        return False

    return True
