def extract_relevant_info(input_data: str) -> str:
    """
    Extracts relevant information from the input data to facilitate linking a meeting node to a role determination process.

    Args:
        input_data: Input parameter of type str

    Returns:
        str: Output of type dict
    """
    import json
    from typing import Any, Dict

    required_fields = ['date', 'time', 'location', 'attendees']
    # Try to load input_data as JSON
    try:
        data: Dict[str, Any] = json.loads(input_data)
    except Exception as e:
        raise ValueError(f"Invalid input data: Unable to parse JSON. Error: {e}")

    # Validate required fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    # Validate each field type
    date = data['date']
    time_ = data['time']
    location = data['location']
    attendees = data['attendees']

    # Date & time should be strings, location a string, attendees a list of strings
    if not isinstance(date, str):
        raise ValueError(f"Invalid type for 'date': expected str, got {type(date).__name__}")
    if not isinstance(time_, str):
        raise ValueError(f"Invalid type for 'time': expected str, got {type(time_).__name__}")
    if not isinstance(location, str):
        raise ValueError(f"Invalid type for 'location': expected str, got {type(location).__name__}")
    if not isinstance(attendees, list) or not all(isinstance(a, str) for a in attendees):
        raise ValueError(f"Invalid type for 'attendees': expected List[str], got {attendees}")

    # Build result dict
    extracted_info = {
        'date': date,
        'time': time_,
        'location': location,
        'attendees': attendees
    }
    # Return the result as a JSON-formatted string
    return json.dumps(extracted_info)
