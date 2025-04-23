def assess_risks_with_constraints(workflow_description: str, constraints: str, framework: str) -> List[str]:
    """
    Analyzes a given workflow description and its constraints to systematically identify and assess significant risks using a specified risk analysis framework.

    Args:
        workflow_description: Input parameter of type str
constraints: Input parameter of type str
framework: Input parameter of type str

    Returns:
        List[str]: Output of type List[dict]
    """
    # --- PURE IMPLEMENTATION ---
    import re
    import json
    from collections import defaultdict
    
    def extract_constraint_phrases(text):
        # Extracts constraint-like phrases, e.g. lines with requirements, forbidden actions, limits, etc.
        patterns = [
            r"must not [^.]+", r"shall not [^.]+", r"should not [^.]+", r"must [^.]+", r"should [^.]+", r"cannot [^.]+", r"can only [^.]+", r"no more than [^.]+", r"at least [^.]+", r"at most [^.]+", r"required to [^.]+", r"prohibited to [^.]+", r"forbidden to [^.]+",
        ]
        phrases = []
        for p in patterns:
            phrases.extend(re.findall(p, text, re.IGNORECASE))
        # Fallback: lines containing certain keywords
        fallback_keywords = ["constraint", "must", "should", "require", "forbidden", "limit", "cannot", "restricted", "prohibit", "only"]
        for line in text.splitlines():
            if any(k in line.lower() for k in fallback_keywords):
                phrases.append(line.strip())
        # Deduplicate & clean
        cleaned = list({ph.strip(". ;") for ph in phrases if ph.strip()})
        return cleaned
    
    def extract_workflow_steps(text):
        # Try to split workflow into logical steps by numbered/bulleted lists, or sentences describing actions
        steps = []
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for line in lines:
            m = re.match(r"\d+\. ?(.*)", line)
            if m:
                steps.append(m.group(1))
            elif re.match(r"[-*+] ?", line):
                steps.append(line[2:].strip())
            else:
                # If imperative verb at start, treat as possible step
                if re.match(r"(?:add|remove|process|submit|send|review|approve|check|perform|ensure|analyze|evaluate|identify|assess|audit|select|assign|track|validate|calculate|verify)", line, re.IGNORECASE):
                    steps.append(line)
        # Fallback: treat each 'sentence' as a step
        if not steps:
            steps = re.split(r"(?<=[.?!])\s+", text)
            steps = [st.strip() for st in steps if len(st.strip().split()) > 2]
        return steps
    
    def extract_risks(workflow, constraints):
        # We'll perform a simple NLP-like scan: identify negative, uncertainty, conditional, or conflict words near constraints or steps
        risk_keywords = ["risk", "uncertain", "unknown", "failure", "delay", "error", "overload", "omission", "breach", "exceed", "conflict", "incomplete", "violate", "prohibited", "violation", "unable", "insufficient", "not met", "not enough", "gap", "block", "missing", "insufficient", "bottleneck", "fault", "mistake"]
        
        # We'll classify a risk if a step or constraint contains or implies these words, or if a constraint obviously makes a step hard
        risks = []
        steps = extract_workflow_steps(workflow)
        constraint_phrases = extract_constraint_phrases(constraints)
        # Try to link constraints to steps
        for step in steps:
            for constraint in constraint_phrases:
                # Heuristic: Does the constraint mention a resource, action, or parameter appearing in the step?
                overlap = False
                tokens_constraint = set(re.findall(r"\w+", constraint.lower()))
                tokens_step = set(re.findall(r"\w+", step.lower()))
                common = tokens_constraint & tokens_step
                if len(common) > 0:
                    overlap = True
                risk_triggered = False
                matched_keywords = []
                for kw in risk_keywords:
                    if kw in step.lower() or kw in constraint.lower():
                        risk_triggered = True
                        matched_keywords.append(kw)
                if overlap or risk_triggered:
                    risk_text = f"Risk: Performing step '{step}' may be affected by constraint '{constraint}'."
                    if matched_keywords:
                        risk_text += f" Potential issues: {', '.join(matched_keywords)}."
                    risks.append({
                        'description': risk_text,
                        'step': step,
                        'constraint': constraint,
                        'matched_keywords': matched_keywords
                    })
        # Fallback: look for standalone risks in constraint/step text
        for doc, typ in [(workflow, "workflow"), (constraints, "constraint")]:
            for kw in risk_keywords:
                hits = [m.group(0) for m in re.finditer(kw, doc.lower())]
                for hit in hits:
                    risks.append({
                        'description': f"Risk keyword '{kw}' found in {typ} description.",
                        'step': None,
                        'constraint': None,
                        'matched_keywords': [kw]
                    })
        return risks
    
    def classify_and_score_risks(risks, framework):
        # Apply simple scoring depending on the selected framework (accepts 'FMEA' or 'risk matrix', case-insensitive)
        classified = []
        # For demo, random-ish but deterministic score mapping
        for i, risk in enumerate(risks):
            c = risk.copy()
            if framework.strip().lower() == 'fmea':
                # Example: severity, likelihood, detectability each out of 10; simple heuristics
                c['framework'] = 'FMEA'
                c['severity'] = min(10, 5 + len(risk['matched_keywords']))
                c['likelihood'] = min(10, 3 + (i % 7))
                c['detectability'] = min(10, 10 - (i % 7))
                c['RPN'] = c['severity'] * c['likelihood'] * c['detectability']
            else:
                # Assume simple risk matrix: Low/Med/High
                c['framework'] = 'Risk Matrix'
                mk = len(risk['matched_keywords'])
                if mk > 2:
                    c['risk_level'] = 'High'
                elif mk == 2:
                    c['risk_level'] = 'Medium'
                else:
                    c['risk_level'] = 'Low'
            classified.append(c)
        return classified
    
    def structure_output(risk_list, constraints):
        # For each risk include explicit link(s) to constraints
        constraint_phrases = extract_constraint_phrases(constraints)
        out = []
        for item in risk_list:
            link = item.get('constraint')
            if not link:
                # Try to match in risk description
                found = None
                for cap in constraint_phrases:
                    if cap in item.get('description',''):
                        found = cap
                        break
                link = found or ''
            result = {
                'risk': item.get('description',''),
                'step': item.get('step'),
                'constraint': link,
                'framework': item.get('framework'),
            }
            # Add scores/levels
            if 'RPN' in item:
                result['RPN'] = item['RPN']
                result['severity'] = item['severity']
                result['likelihood'] = item['likelihood']
                result['detectability'] = item['detectability']
            if 'risk_level' in item:
                result['risk_level'] = item['risk_level']
            out.append(result)
        return out
    
    # --- MAIN EXECUTION ---
    detected_risks = extract_risks(workflow_description, constraints)
    classified = classify_and_score_risks(detected_risks, framework)
    structured = structure_output(classified, constraints)
    # Return as JSON strings to match List[str] output signature
    return [json.dumps(r) for r in structured]
