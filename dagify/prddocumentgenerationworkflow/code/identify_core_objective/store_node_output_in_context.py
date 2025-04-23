def store_node_output_in_context(key: str, value: str) -> str:
    """
    This node stores the output of another node in a shared context using a specified key so that it is accessible for downstream nodes.

    Args:
        key: Input parameter of type str
value: Input parameter of type str

    Returns:
        str: Output of type Any
    """
    # --- PURE IMPLEMENTATION ---
    # Shared context will be a module-level dictionary
    # We use a special attribute on the function to simulate singleton/session-level storage
    import threading
    import json

    # Use attached attribute on the function for thread-safe global context
    if not hasattr(store_node_output_in_context, "_context"):
        store_node_output_in_context._context = {}
        store_node_output_in_context._lock = threading.Lock()

    # Cast value to JSON-serializable string for type consistency/serializability
    try:
        serialized_value = json.dumps(value)
    except TypeError:
        # If not serializable, fall back to str
        serialized_value = str(value)

    # Store the value with thread safety
    with store_node_output_in_context._lock:
        store_node_output_in_context._context[key] = serialized_value

    return serialized_value
