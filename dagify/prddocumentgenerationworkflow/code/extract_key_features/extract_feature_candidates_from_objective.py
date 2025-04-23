def extract_feature_candidates_from_objective(text: str) -> List[str]:
    """
    This node analyzes the provided core objective text to extract a list of candidate workflow features described or implied within the objective statement.

    Args:
        text: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re

    # 1. Basic sentence segmentation to attempt splitting on ; . and newlines, but also consider 'and', 'or', etc for compound statements
    # 2. Named entity-like extraction: parse for verbs and likely actions, possibly via regex for verbs/verb phrases followed by direct objects.
    # 3. Deduplicate and clean up phrases: strip whitespace, remove trailing punctuation, deduplicate identical or near-identical statements.

    # Step 1: Preprocessing - normalize and split text into candidate sentences/fragments
    text_clean = re.sub(r'\s+', ' ', text.strip())  # Normalize whitespace
    candidate_fragments = re.split(r'[.;\n]+', text_clean)

    features = []
    for fragment in candidate_fragments:
        fragment = fragment.strip()
        if not fragment:
            continue

        # Step 2: Split on common conjunctions when appropriate for compound sentences
        # (e.g., "generate a summary and send it ..." -> ["generate a summary", "send it ..."])
        subfrags = re.split(r'\band\b|\bor\b|\bthen\b|,', fragment, flags=re.IGNORECASE)
        for subf in subfrags:
            phrase = subf.strip()
            if not phrase:
                continue

            # Step 3: Try extracting verb-object patterns (quick NLP-inspired heuristic)
            # E.g., 'Detect user intent', 'Extract phone number', etc.
            # Simplistic regex: Match a verb (likely starting word), rest of the phrase is the feature
            verb_phrase_match = re.match(r'^(to |should )?(\w+)( .+)', phrase, flags=re.IGNORECASE)
            if verb_phrase_match:
                # Use the full phrase for maximum descriptiveness as atomized capability
                core_feature = phrase
            else:
                # If not matching pattern, but phrase is not empty, take it as is
                core_feature = phrase
            features.append(core_feature)

    # Step 4: Post-process - remove duplicates and ensure atomicity
    # Remove duplicates (case-insensitive)
    deduped = []
    seen = set()
    for feat in features:
        norm = feat.lower().strip()
        # Remove trailing punctuation for clean features
        norm = re.sub(r'[^\w\s]$', '', norm)
        # Minimal filtering for atomic/unique features
        if norm and norm not in seen:
            deduped.append(feat.strip().rstrip('.').rstrip(';'))
            seen.add(norm)

    return deduped
