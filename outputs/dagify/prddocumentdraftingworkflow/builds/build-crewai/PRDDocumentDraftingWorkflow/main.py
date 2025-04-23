# /// script
# dependencies = ["crewai==0.105.0"]
# ///
import sys
import logging
from crewai import Crew
from crews import *

class FilteredStream:
    # @traceable
    def __init__(self, original_stream):
        self.original_stream = original_stream
        self.filtered_messages = [
            "File not found:",
            "agents.yaml",
            "tasks.yaml"
        ]
        self.buffer = ""

    # @traceable
    def write(self, text):
        # Add to buffer
        self.buffer += text

        # If we have a complete line (ends with newline)
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            # Process all complete lines
            for line in lines[:-1]:
                if not any(msg in line for msg in self.filtered_messages):
                    self.original_stream.write(line + '\n')
            # Keep the last incomplete line in buffer
            self.buffer = lines[-1]

    # @traceable
    def flush(self):
        # Process any remaining buffer content
        if self.buffer and not any(msg in self.buffer for msg in self.filtered_messages):
            self.original_stream.write(self.buffer)
        self.buffer = ""
        self.original_stream.flush()

# Redirect stdout to our filtered stream
sys.stdout = FilteredStream(sys.stdout)

# Suppress CrewAI configuration warnings
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)
import os
import asyncio
from typing import Dict
from crewai import Crew

from crews.derive_functional_requirements_crew import derive_functional_requirements_crew
from crews.derive_nonfunctional_requirements_crew import derive_nonfunctional_requirements_crew
from crews.extract_assumptions_and_constraints_crew import extract_assumptions_and_constraints_crew
from crews.extract_goals_crew import extract_goals_crew
from crews.extract_product_context_crew import extract_product_context_crew
from crews.extract_success_metrics_crew import extract_success_metrics_crew
from crews.extract_use_cases_crew import extract_use_cases_crew
from crews.identify_stakeholders_crew import identify_stakeholders_crew
from crews.synthesize_prd_outline_crew import synthesize_prd_outline_crew


# @traceable
async def run_workflow(inputs: Dict = None, openai_api_key: str = None):
    """Execute the full workflow."""
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    elif not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key must be provided")

    if inputs is None:
        inputs = {}

    results = {}
    crews = {}
    crews["derive_functional_requirements"] = derive_functional_requirements_crew().crew()
    crews["derive_nonfunctional_requirements"] = derive_nonfunctional_requirements_crew().crew()
    crews["extract_assumptions_and_constraints"] = extract_assumptions_and_constraints_crew().crew()
    crews["extract_goals"] = extract_goals_crew().crew()
    crews["extract_product_context"] = extract_product_context_crew().crew()
    crews["extract_success_metrics"] = extract_success_metrics_crew().crew()
    crews["extract_use_cases"] = extract_use_cases_crew().crew()
    crews["identify_stakeholders"] = identify_stakeholders_crew().crew()
    crews["synthesize_prd_outline"] = synthesize_prd_outline_crew().crew()

    # Level 0 execution
    results["extract_product_context"] = await crews["extract_product_context"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["extract_assumptions_and_constraints"].kickoff_async(inputs={"extract_product_context_output": results["extract_product_context"].raw}), crews["extract_goals"].kickoff_async(inputs={"extract_product_context_output": results["extract_product_context"].raw}), crews["extract_use_cases"].kickoff_async(inputs={"extract_product_context_output": results["extract_product_context"].raw}), crews["identify_stakeholders"].kickoff_async(inputs={"extract_product_context_output": results["extract_product_context"].raw}))
    for node_name, result in zip(['extract_assumptions_and_constraints', 'extract_goals', 'extract_use_cases', 'identify_stakeholders'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["derive_functional_requirements"].kickoff_async(inputs={"extract_goals_output": results["extract_goals"].raw, "extract_use_cases_output": results["extract_use_cases"].raw}), crews["derive_nonfunctional_requirements"].kickoff_async(inputs={"extract_goals_output": results["extract_goals"].raw, "extract_assumptions_and_constraints_output": results["extract_assumptions_and_constraints"].raw}), crews["extract_success_metrics"].kickoff_async(inputs={"extract_goals_output": results["extract_goals"].raw}))
    for node_name, result in zip(['derive_functional_requirements', 'derive_nonfunctional_requirements', 'extract_success_metrics'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["synthesize_prd_outline"].kickoff_async(inputs={"extract_product_context_output": results["extract_product_context"].raw, "identify_stakeholders_output": results["identify_stakeholders"].raw, "extract_goals_output": results["extract_goals"].raw, "extract_assumptions_and_constraints_output": results["extract_assumptions_and_constraints"].raw, "extract_use_cases_output": results["extract_use_cases"].raw, "derive_functional_requirements_output": results["derive_functional_requirements"].raw, "derive_nonfunctional_requirements_output": results["derive_nonfunctional_requirements"].raw, "extract_success_metrics_output": results["extract_success_metrics"].raw}))
    for node_name, result in zip(['synthesize_prd_outline'], level_results):
        results[node_name] = result

    return results

# @traceable
def run_workflow_sync(inputs: Dict = None, openai_api_key: str = None):
    """Synchronous version of run_workflow."""
    return asyncio.run(run_workflow(inputs, openai_api_key))

if __name__ == "__main__":
    import sys
    import json

    api_key = os.getenv("OPENAI_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not api_key:
        print("Please provide OpenAI API key")
        sys.exit(1)

    print("Provide any runtime inputs/params/args/context in raw text or JSON format (press Enter for empty input):")
    user_input = input().strip()

    inputs = {"input": user_input} if user_input else {}

    try:
        if user_input:
            # Try to parse as JSON if provided
            json_input = json.loads(user_input)
            inputs = {"input": json_input}
    except json.JSONDecodeError:
        # If not valid JSON, use the raw string
        pass

    results = run_workflow_sync(inputs, openai_api_key=api_key)
