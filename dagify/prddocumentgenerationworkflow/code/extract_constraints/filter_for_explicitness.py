def filter_for_explicitness(constraints: str, text: str) -> List[str]:
    """
    This node filters a list of candidate constraint strings and returns only those constraints that are explicit (i.e., directly and unambiguously stated) within the provided input text.

    Args:
        constraints: Input parameter of type str
text: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    # PURE IMPLEMENTATION (SHIMS REPLACED)
    import re
    from typing import List

    # --- Step 1: Parse the input 'constraints' string to get candidate constraints ---
    # We'll try splitting by newlines or semicolons. If comma-separated, split by commas as fallback.
    # Assume that constraints are separated by newline, semicolon or comma.
    raw = constraints.strip()
    if not raw:
        return []
    if '\n' in raw:
        constraint_list = [c.strip() for c in raw.split('\n') if c.strip()]
    elif ';' in raw:
        constraint_list = [c.strip() for c in raw.split(';') if c.strip()]
    else:
        constraint_list = [c.strip() for c in raw.split(',') if c.strip()]

    # --- Step 2: Define signal phrases to check explicitness ---
    # Chosen based on the PRD: strong, explicit, deontic language
    signal_phrases = [
        r'\bmust\b', r'\bshall\b', r'\brequired to\b', r'\bno more than\b',
        r'\bmay not\b', r'\bshould\b', r'\bis prohibited\b', r'\bnot allowed\b',
        r'\bhas to\b', r'\bare not permitted\b', r'\bmay only\b', r'\bwill not\b',
        r'\bare required\b', r'\bare prohibited\b', r'\bordered to\b'
    ]
    # Compile regex patterns, case-insensitive
    compiled_signal_patterns = [re.compile(pat, re.IGNORECASE) for pat in signal_phrases]

    # --- Step 3: For each candidate constraint, check explicitness in the input text ---
    explicit_constraints = []
    for constraint in constraint_list:
        # Check if the raw constraint text appears explicitly (or a close variant) in the main text
        constraint_clean = ' '.join(constraint.lower().split())
        text_clean = ' '.join(text.lower().split())
        found_exact = False
        # Try exact phrase match (ignoring case and whitespace differences)
        if constraint_clean and constraint_clean in text_clean:
            found_exact = True
        # Otherwise, look for the constraint as a fuzzy substring with a strong signal phrase
        found_pattern = False
        for pattern in compiled_signal_patterns:
            if pattern.search(constraint):
                # If the constraint uses a strong phrase, check if it appears in text
                regex_match = re.search(re.escape(constraint), text, re.IGNORECASE)
                if regex_match:
                    found_pattern = True
                    break
                # Alternatively, check if the signal phrase appears in text near a similar constraint phrase
                # by searching for sentences in text with the signal phrase and a majority of keywords in the constraint
                # (simple keyword intersection)
                # Break constraint and text into lower tokens
                constraint_words = set([w for w in re.findall(r'\w+', constraint_clean) if w not in {'must', 'shall', 'required', 'no', 'than', 'is', 'are', 'not', 'will', 'to', 'be', 'may', 'should'}])
                # Find sentences in text with the signal phrase
                for sentence in re.split(r'[.!?]', text):
                    if pattern.search(sentence):
                        sent_clean = ' '.join(sentence.lower().split())
                        sent_words = set(re.findall(r'\w+', sent_clean))
                        # At least half the constraint words must appear in the sentence
                        if constraint_words and len(constraint_words & sent_words) >= max(1, len(constraint_words)//2):
                            found_pattern = True
                            break
                if found_pattern:
                    break
        if found_exact or found_pattern:
            explicit_constraints.append(constraint)

    # --- Step 4: Remove constraints that are implied, ambiguous, or inferential ---
    # Here, we remove constraints that do not have strong phrasing or are too generic (e.g., implied by context but not stated)
    # For simplicity, if none of the signal phrases occur in either the constraint or the matching text, consider it ambiguous
    final_constraints = []
    for constraint in explicit_constraints:
        # Strong phrasing required
        has_signal = any(pat.search(constraint) for pat in compiled_signal_patterns)
        if has_signal:
            final_constraints.append(constraint)
        else:
            # See if the raw appeared in text with a strong phrase
            matched = False
            for pat in compiled_signal_patterns:
                # Look for a sentence in text that contains both the constraint (loosely) and the signal phrase
                for sentence in re.split(r'[.!?]', text):
                    if pat.search(sentence):
                        constraint_words = set(re.findall(r'\w+', constraint.lower()))
                        sent_words = set(re.findall(r'\w+', sentence.lower()))
                        if constraint_words and len(constraint_words & sent_words) >= max(1, len(constraint_words)//2):
                            matched = True
                            break
                if matched:
                    break
            if matched:
                final_constraints.append(constraint)
            # If not matched, consider ambiguous; ignore

    # --- Step 5: Deduplicate and canonicalize output ---
    deduped = list(dict.fromkeys(final_constraints))  # dedupe, preserve order
    # Optionally, sort alphabetically if canonical order required:
    deduped_sorted = sorted(deduped, key=lambda x: x.lower())
    return deduped_sorted
