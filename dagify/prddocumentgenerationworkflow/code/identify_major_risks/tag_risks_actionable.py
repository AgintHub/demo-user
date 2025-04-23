def tag_risks_actionable(risks: str) -> List[str]:
    """
    Systematically evaluates a list of documented risks and tags each as either actionable or non-actionable, providing justification for each decision.

    Args:
        risks: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    import json
    import re
    from typing import List

    # Helper function: rule-based actionability
    def is_actionable(risk_desc: str) -> (bool, str):
        """
        Returns tuple: (actionable: bool, justification: str)
        """
        lowered = risk_desc.strip().lower()

        # Example keywords that are generally NON-actionable:
        non_actionable_keywords = [
            # External, force-majeure or industry-wide
            'act of god', 'global recession', 'regulatory uncertainty', 'market volatility',
            'economic downturn', 'natural disaster', 'pandemic',
            'external dependency', 'supply chain disruption',
            'competitive landscape', 'government policy',
            'political instability', 'systemic risk', 'macroeconomic', 'war', "political forces"
        ]
        # If any of the non-actionable keywords match, it's non-actionable
        for kw in non_actionable_keywords:
            if kw in lowered:
                return False, (
                    f"Tagged as non-actionable: The risk involves '{kw}', which is outside the organization's reasonable sphere of control per guidelines."
                )

        # Example keywords that are likely actionable
        actionable_keywords = [
            # Process, technology, staff, compliance, and known weaknesses
            'data breach', 'compliance failure', 'outdated software', 'human error',
            'weak password', 'training gap', 'access control', 'configuration error',
            'lack of documentation', 'poor process', 'customer complaint', 'system failure',
            'security vulnerability', 'insufficient testing', 'maintenance delay',
            'improper validation', 'internal fraud'
        ]
        for kw in actionable_keywords:
            if kw in lowered:
                return True, (
                    f"Tagged as actionable: The risk relates to '{kw}', which can be mitigated by organizational action (e.g., improved controls, process changes, or remediation)."
                )
        
        # Heuristic: if it contains phrases indicating it's within internal remediable scope
        if re.search(r'(our|organization|company|team|staff|internal) (policy|process|procedure|control|systems?)', lowered):
            return True, (
                "Tagged as actionable: The risk refers to internal factors that can be managed or improved per best practice."
            )
        # Heuristic: if it says 'Unable to', 'Lack of', 'No process' etc, and is not clearly external
        if re.search(r'(unable to|lack of|no process|insufficient|missing)', lowered):
            # Check for external qualifiers
            if not re.search(r'(regulatory|macro|market|government|political|external)', lowered):
                return True, (
                    "Tagged as actionable: The identified shortcoming is within internal control and fits remediation guidelines."
                )
        # If it mentions "cannot address", "outside control", or similar, it is non-actionable
        if re.search(r'(cannot address|beyond control|outside the organizations? control)', lowered):
            return False, (
                "Tagged as non-actionable: The risk is explicitly stated to be outside organizational control."
            )
        # Default logic/justification
        # If the risk mentions consequences of external events only, tag as non-actionable
        if re.search(r'(change in law|acts? of government|third[- ]party decision|force majeure)', lowered):
            return False, (
                "Tagged as non-actionable: The risk stems from unpredictable external events not actionable by the organization."
            )
        # Default fallback to actionable (if uncertainty):
        return True, (
            "Tagged as actionable: No clear external or unmanageable factors; defaulting to actionable per organizational guidance."
        )

    # Step 1: Parse input str to list of dicts
    try:
        parsed_risks = json.loads(risks)
        if not isinstance(parsed_risks, list):
            raise ValueError('Input JSON is not a list of risks.')
    except Exception as e:
        raise ValueError(f'Input string could not be parsed as a list of risk dicts: {e}')

    output_risks: List[dict] = []
    for risk in parsed_risks:
        # Each risk must be a dict with at least a description.
        desc = risk.get('description') or risk.get('risk') or risk.get('text')
        if not isinstance(desc, str):
            # Try to use the entire risk as string if not found
            desc_s = str(risk)
        else:
            desc_s = desc
        actionable, justification = is_actionable(desc_s)
        risk_with_flags = dict(risk)
        risk_with_flags['actionable'] = actionable
        risk_with_flags['justification'] = justification
        output_risks.append(risk_with_flags)

    # Return as JSON strings, as required by signature List[str], one per risk
    # (If it should return List[dict], simply return output_risks)
    return [json.dumps(risk) for risk in output_risks]
