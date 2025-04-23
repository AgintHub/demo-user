def normalize_and_deduplicate_features(features: str) -> List[str]:
    """
    This node processes an input list of workflow features to split compound statements into atomic features, remove duplicates, and standardize the phrasing for consistency.

    Args:
        features: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    import re
    from typing import List
    
    # --- 1. Preprocess (split by newlines, strip) ---
    # Assume initial input is either a multi-line string or semi-colon/comma separated
    raw_items = []
    for line in features.splitlines():
        # Try splitting by ';' or ',' in addition to lines
        line = line.strip()
        if not line:
            continue
        # Split by ';' or ',' if present, else keep whole line
        if ';' in line or ',' in line:
            for chunk in re.split(r'[;,]', line):
                chunk = chunk.strip()
                if chunk:
                    raw_items.append(chunk)
        else:
            raw_items.append(line)

    # Helpers for splitting compound statements
    def split_compound(statement: str) -> List[str]:
        # Split by conjunctions: 'and', 'or', 'as well as', 'plus'
        # Only split if it's likely to be truly atomic
        # Example: "Allow users to reset passwords and update email"
        # Should be split into two actions
        # We'll use a regex to break on "and", "or", etc., but not inside quoted text
        # Also try to handle serial lists: "Export as CSV, PDF, or Excel"
        
        # Normalize separators: ensure commas before 'and', 'or', etc. are handled
        s = statement.strip()
        # If none of the splitters, just return as is
        # We use word boundaries to avoid splitting e.g. "random"
        splitters = [r'\band\b', r'\bor\b', r'\bas well as\b', r'\bplus\b']
        splitter_pattern = '|'.join(splitters)
        # Also, sometimes patters are "foo, bar and baz"
        # So first split by "," and then further by conjunctions
        # First split by comma
        comma_split = [chunk.strip() for chunk in re.split(r',', s) if chunk.strip()]
        result = []
        for segment in comma_split:
            # Now break on conjunctions if present
            parts = [part.strip() for part in re.split(splitter_pattern, segment, flags=re.IGNORECASE) if part.strip()]
            result.extend(parts)
        # To avoid oversplitting e.g. "Analyze origin and destination addresses"
        # If it's <7 words or no verbs appear in both pieces, probably should not split
        if len(result) == 1:
            return result
        # Only split if all parts look like plausible commands (must have verb)
        # Simplified check: begin with verb or modal verb
        def looks_like_command(x):
            # Tokenize first word
            m = re.match(r'^(to |allow user[s]* to )?(\w+)', x.strip().lower())
            if m:
                verb_candidate = m.group(2)
                # Heuristic: basic list of common verbs
                return verb_candidate in [
                    'allow','enable','support','add','remove','delete','update','edit','view',
                    'create','analyze','send','receive','reset','normalize','export','import',
                    'assign','find','choose','split','deduplicate','track','apply','implement',
                    'clean','detect', 'order'
                ]
            return False
        if all(looks_like_command(r) for r in result):
            return result
        # Else, merged back, don't split
        return [s]

    # --- Step 2: Normalize each statement and split into atomic features ---
    atomics = []
    for item in raw_items:
        atomic_feats = split_compound(item)
        atomics.extend(atomic_feats)

    # --- Step 3: Normalize phrasing: clean whitespace, verb-object format, capitalization, etc. ---
    def normalize_text(text: str) -> str:
        # Remove leading/trailing whitespace
        s = text.strip()
        # Remove trailing punctuation
        s = re.sub(r'[.?!,;:]+$', '', s)
        # Replace multiple spaces
        s = re.sub(r'\s+', ' ', s)
        # Lowercase verb, capitalize object
        # Try to rephrase into Verb-object form
        # Heuristic: If starts with "Allow/Enable/Support/Let user[s] to", strip that
        m = re.match(r'^(allow|enable|support|let)( user(s)?(s)?( to)? )?(.*)$', s, re.IGNORECASE)
        if m:
            rest = m.group(6).strip() if m.group(6) else s
            # Try to identify verb-object pattern
            # e.g., "reset passwords" from "Allow users to reset passwords"
            s = rest
        # Lowercase first character, unless acronym
        s = s[0].upper() + s[1:] if s else s
        # Optionally, could stem/present-tense normalize verbs
        # For now, ensure imperative (no trailing ".") and consistent spacing
        return s

    normalized_atoms = [normalize_text(f) for f in atomics if f and f.strip()]

    # --- Step 4: Deduplicate: exact match, then basic case-insensitive and fuzzy
    def unique_by_semantics(strings: List[str]) -> List[str]:
        # Case-insensitive exact deduplication
        seen = set()
        result = []
        for s in strings:
            canon = s.strip().lower()
            if canon not in seen:
                seen.add(canon)
                result.append(s)
        # Optionally, lightweight fuzzy/synonym check: collapse variants like 'Export as CSV' vs 'Export to CSV'
        # Here, implement a minimal Jaccard-like deduplication based on token overlap
        final = []
        token_seen = []
        for s in result:
            tokens = set(re.findall(r'\w+', s.lower()))
            duplicate = False
            for prev_tokens in token_seen:
                intersection = tokens & prev_tokens
                union = tokens | prev_tokens
                if union and len(intersection)/len(union) > 0.85:  # High overlap
                    duplicate = True
                    break
            if not duplicate:
                token_seen.append(tokens)
                final.append(s)
        return final

    unique_features = unique_by_semantics(normalized_atoms)
    return unique_features
