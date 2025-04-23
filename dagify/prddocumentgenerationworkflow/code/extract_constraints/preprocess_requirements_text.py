def preprocess_requirements_text(raw_input: str) -> str:
    """
    This node standardizes and cleans raw requirements text by removing extraneous formatting, normalizing structure, and preparing it for accurate downstream constraint extraction.

    Args:
        raw_input: Input parameter of type str

    Returns:
        str: Output of type str
    """
    import re
    import unicodedata

    text = raw_input

    # Unicode normalization to NFC
    text = unicodedata.normalize('NFC', text)

    # Remove non-printable and control Unicode characters
    # (keep tabs, newlines for now for structure)
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    # Typographic corrections: replace fancy quotes/dashes with standard ones
    quotes_map = {
        '“': '"', '”': '"', "‘": "'", "’": "'", '«': '"', '»': '"',
        '–': '-', '—': '-', '−': '-', '‐': '-', '‑': '-',
        '…': '...',
    }
    for orig, repl in quotes_map.items():
        text = text.replace(orig, repl)

    # Standardize bullet points and numbering schemes
    # Convert numbered lists and various bullets to a standard '- '
    # Examples to handle: '*', '•', '-', '–', 'a)', '1.', etc. at line starts
    bullet_patterns = [
        r'^[\s]*(?:[\*\-•‣])\s+',    # e.g. * Text / • Text / - Text / ‣ Text
        r'^[\s]*(\d+|[a-zA-Z])[.).]([ \t])',  # 1. Text / 1) Text / a. Text / b) Text
        r'^[\s]+-\s+',                # indented bullets
    ]
    def bullet_sub(match):
        return '- '
    for pat in bullet_patterns:
        text = re.sub(pat, '- ', text, flags=re.MULTILINE)

    # Standardize sentence delimiters: Remove excess line breaks (collapse >2 newlines into 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse multiple spaces/tabs into single space (but preserve newlines)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    # Remove trailing whitespace on each line
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

    # Remove empty bullet lines (e.g., '-   ')
    text = re.sub(r'^-\s*$', '', text, flags=re.MULTILINE)

    # Remove any residual non-standard ASCII (e.g., non-breaking space)
    text = text.replace('\u00A0', ' ')

    # Strip leading/trailing whitespace/newlines
    cleaned = text.strip()

    return cleaned
