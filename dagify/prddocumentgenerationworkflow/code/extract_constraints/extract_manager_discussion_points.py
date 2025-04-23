def extract_manager_discussion_points(text: str, triggers: str) -> List[str]:
    """
    This node extracts a list of discussion points requiring senior manager input or clarification from the input text using specified trigger phrases.

    Args:
        text: Input parameter of type str
triggers: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re
    
    # --- Step 1: Parse triggers ---
    # Accept triggers as comma, semicolon, or newline separated list
    trigger_list = [t.strip().lower() for t in re.split(r'[;,\n]', triggers) if t.strip()]
    # Remove duplicates, short triggers and empty entries
    trigger_list = sorted(set(t for t in trigger_list if len(t) > 1), key=len, reverse=True)
    if not trigger_list:
        return []

    # --- Step 2: Split text into sentences/clauses ---
    # Simple sentence/segment splitter: split at period, exclamation, question, or semicolon (keeps some clauses, too)
    raw_segments = re.split(r'(?<=[.!?;])\s+|\n', text)
    # Further split on commas if necessary (to ensure shorter actionable points)
    segments = []
    for seg in raw_segments:
        if len(seg.split()) > 20:  # Arbitrary cutoff for long sentence, may be a paragraph
            segments.extend([s.strip() for s in seg.split(',') if s.strip()])
        else:
            stripped = seg.strip()
            if stripped:
                segments.append(stripped)

    # --- Step 3: Find discussion points (segments containing any trigger phrase) ---
    discussion_points = []
    for seg in segments:
        lowered = seg.lower()
        if any(trigger in lowered for trigger in trigger_list):
            discussion_points.append(seg)

    if not discussion_points:
        return []

    # --- Step 4: Clean and normalize discussion points ---
    cleaned_points = []
    seen = set()
    for point in discussion_points:
        # Trim whitespace
        p = point.strip()
        # Remove leading/trailing punctuation
        p = re.sub(r'^[\s\-–—\*]+', '', p)
        p = re.sub(r'[\s.!?;,:-]+$', '', p)
        # Remove internal excessive whitespace
        p = re.sub(r'\s+', ' ', p)
        # Remove duplicate points (case-insensitive)
        p_key = p.lower()
        if p_key not in seen and p:
            cleaned_points.append(p)
            seen.add(p_key)

    # --- Optionally, enforce each is a requirement/question (could further split on ", and "/or ". Also, ...")
    # For simplicity, split on " and " to separate conjoined requirements
    final_points = []
    for p in cleaned_points:
        subpoints = [sp.strip() for sp in re.split(r'\band\b', p, flags=re.IGNORECASE)]
        for sp in subpoints:
            ssp = sp.strip()
            if ssp and ssp.lower() not in seen:
                final_points.append(ssp)
                seen.add(ssp.lower())

    return final_points
