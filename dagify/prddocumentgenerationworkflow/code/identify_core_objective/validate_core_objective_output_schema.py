def validate_core_objective_output_schema(core_objective: str) -> str:
    """
    This node validates that the given core objective output string conforms to the required schema and type specifications before passing it downstream in the workflow.

    Args:
        core_objective: Input parameter of type str

    Returns:
        str: Output of type Any
    """
    # --- PURE IMPLEMENTATION ---
    if not isinstance(core_objective, str):
        raise TypeError(f"core_objective must be a string, got {type(core_objective).__name__}")
    if not core_objective or not core_objective.strip():
        raise ValueError("core_objective must be a non-empty string.")
    # Optionally, add further string validation/per schema constraints here if required in future
    return core_objective
