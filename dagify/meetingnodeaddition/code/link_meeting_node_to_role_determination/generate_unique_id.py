def generate_unique_id() -> str:
    """
    Generates a unique identifier for use in edge creation between nodes.

    Args:
        

    Returns:
        str: Output of type str
    """
    import uuid
    # Generate a UUID using uuid4 (random-based, practically negligible collision risk)
    unique_id = str(uuid.uuid4())
    return unique_id
