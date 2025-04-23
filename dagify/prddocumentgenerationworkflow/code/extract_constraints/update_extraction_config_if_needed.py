def update_extraction_config_if_needed(kwargs: str) -> str:
    """
    Determines if the extraction configuration needs to be updated based on input parameters and modifies rules or patterns for future constraint extraction if required.

    Args:
        kwargs: Input parameter of type str

    Returns:
        str: Output of type Any
    """
    import json
    import os
    from copy import deepcopy

    # Parse input kwargs (expecting a JSON string)
    try:
        input_kwargs = json.loads(kwargs)
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Failed to parse input kwargs: {e}'
        })

    # --- CONFIGURATION STORE ---
    CONFIG_FILE = 'extraction_config.json'

    # Helper: Load existing config (if file exists), else start with default
    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                # Corrupt file or read error; fallback to default empty
                return {'categories': [], 'patterns': [], 'regulatory_constraints': []}
        else:
            return {'categories': [], 'patterns': [], 'regulatory_constraints': []}

    # Helper: Save config to file
    def save_config(config):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    # --- Recognized triggers ---
    # Accept new categories, patterns, or regulatory_constraints.
    TRIGGERS = ['categories', 'patterns', 'regulatory_constraints']

    config = load_config()
    config_before = deepcopy(config)
    updates_made = False
    updates = {}

    # Check for recognized triggers and update if new info is present
    for trigger in TRIGGERS:
        new_values = input_kwargs.get(trigger)
        if new_values:
            if not isinstance(new_values, list):
                # Convert single string or value to list
                new_values = [new_values]
            existing_values = set(config.get(trigger, []))
            additional = [v for v in new_values if v not in existing_values]
            if additional:
                config.setdefault(trigger, [])
                config[trigger].extend(additional)
                updates[trigger] = additional
                updates_made = True

    # Apply changes and persist if needed
    if updates_made:
        save_config(config)
        status_msg = {
            'status': 'updated',
            'details': {
                'added': updates,
                'config_before': config_before,
                'config_after': config
            }
        }
    else:
        status_msg = {
            'status': 'no_update',
            'message': 'No new triggers or values detected that require changes.',
            'config': config
        }
    return json.dumps(status_msg, indent=2)
