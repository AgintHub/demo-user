def extract_constraint_references(requirements_text: str) -> str:
    """
    This node analyzes provided requirements text to extract references to technical, business, or process constraints that should be made available for downstream workflow design and decision-making.

    Args:
        requirements_text: Input parameter of type str

    Returns:
        str: Output of type str
    """
    import re
    import json

    # Keywords for different constraint categories
    tech_keywords = [
        'API', 'integration', 'system', 'platform', 'database', 'technology', 'architecture', 'compatib', 'deploy',
        'infrastructure', 'cloud', 'tech', 'software', 'hardware', 'protocol', 'service', 'framework', 'environment', 'tool'
    ]
    biz_keywords = [
        'budget', 'cost', 'revenue', 'profit', 'quota', 'pricing', 'ROI', 'business', 'stakeholder', 'approval',
        'market', 'customer', 'sales', 'commercial', 'financial', 'grant', 'fund', 'expense', 'payment', 'invoicing', 'forecast'
    ]
    timeline_keywords = [
        'deadline', 'timeline', 'delivery', 'milestone', 'phase', 'timeframe', 'due', 'launch', 'sprint', 'duration', 'completion',
        'date', 'asap', 'by', 'before', 'after', 'within', 'no later than', 'quarter', 'month', 'week', 'day'
    ]
    resource_keywords = [
        'resource', 'staff', 'capacity', 'personnel', 'manpower', 'hours', 'team', 'developer', 'contractor',
        'allocation', 'availability', 'effort', 'headcount', 'skill', 'expertise', 'equipment', 'tool', 'machine'
    ]
    regulatory_keywords = [
        'compliance', 'legal', 'regulation', 'licensed', 'law', 'standard', 'GDPR', 'HIPAA', 'PCI',
        'security', 'privacy', 'audit', 'traceability', 'risk', 'policy', 'certificate', 'accreditation', 'requirement', 'restriction', 'governance'
    ]

    # Helper to flatten and lowercase keyword lists
    def keyword_finder_factory(keywords):
        return lambda s: any(k.lower() in s.lower() for k in keywords)

    category_map = [
        ('technology', keyword_finder_factory(tech_keywords)),
        ('business', keyword_finder_factory(biz_keywords)),
        ('timeline', keyword_finder_factory(timeline_keywords)),
        ('resource', keyword_finder_factory(resource_keywords)),
        ('regulatory', keyword_finder_factory(regulatory_keywords)),
    ]

    # Sentence splitter (basic)
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', requirements_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    extracted = []
    seen_statements = set()
    for sent in sentences:
        # Check if the sentence contains any constraint indicator
        # Search for: (1) explicit, (2) implied constraints
        lowered = sent.lower()
        found_category = None
        for cat, finder in category_map:
            if finder(sent):
                found_category = cat
                break
        # Look for generic constraint phrases
        constraint_phrases = [
            'must', 'should', 'required', 'shall', 'is subject to', 'need to', 'needs to', 'have to',
            'no later than', 'cannot', 'not allowed', 'forbidden', 'prohibited'
        ]
        is_constraint = any(phrase in lowered for phrase in constraint_phrases)
        # Also, if the category is regulatory, treat any mention of regulatory_keywords as a constraint
        if found_category or is_constraint:
            norm = sent.strip()
            # Simple deduplication
            norm_key = re.sub(r'\s+', ' ', norm.lower())
            if norm_key not in seen_statements:
                item = {
                    'constraint': norm,
                    'category': found_category if found_category else 'unspecified'
                }
                extracted.append(item)
                seen_statements.add(norm_key)
    # Additional pass: extract implicit enumerated constraints in list items (bullets)
    # E.g., "The system must: (a) support SSO; (b) restrict access by region; (c) log all activity."
    for sent in sentences:
        # Match patterns like a) ..., b) ..., or (a)... (b)...
        bullet_fragments = re.findall(r'\([a-zA-Z0-9]\)\s*([A-Z0-9][^.;:!\n]+)', sent)
        if bullet_fragments:
            for _, frag in bullet_fragments:
                # Reapply category and constraint checks to fragment
                found_category = None
                for cat, finder in category_map:
                    if finder(frag):
                        found_category = cat
                        break
                lowered_frag = frag.lower()
                is_constraint = any(phrase in lowered_frag for phrase in constraint_phrases)
                if found_category or is_constraint:
                    norm = frag.strip()
                    norm_key = re.sub(r'\s+', ' ', norm.lower())
                    if norm_key not in seen_statements:
                        item = {
                            'constraint': norm,
                            'category': found_category if found_category else 'unspecified'
                        }
                        extracted.append(item)
                        seen_statements.add(norm_key)
    # Final normalization: sort, ensure concise output
    output = []
    for c in extracted:
        s = c['constraint'].strip()
        # Remove trailing punctuation for programmatic clarity
        if s and s[-1] in '.;:':
            s = s[:-1].strip()
        # Output as clear, concise statement
        entry = {'category': c['category'], 'statement': s}
        output.append(entry)
    # Structure as JSON string for downstream consumption
    return json.dumps(output, ensure_ascii=False, indent=2)
