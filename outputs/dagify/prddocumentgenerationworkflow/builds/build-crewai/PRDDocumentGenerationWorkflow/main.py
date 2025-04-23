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

from crews.compose_prd_summary_crew import compose_prd_summary_crew
from crews.extract_constraints_crew import extract_constraints_crew
from crews.extract_key_features_crew import extract_key_features_crew
from crews.generate_feature_descriptions_crew import generate_feature_descriptions_crew
from crews.identify_core_objective_crew import identify_core_objective_crew
from crews.identify_major_risks_crew import identify_major_risks_crew
from crews.identify_success_metrics_crew import identify_success_metrics_crew
from crews.list_primary_user_roles_crew import list_primary_user_roles_crew
from crews.prioritize_features_crew import prioritize_features_crew


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
    crews["compose_prd_summary"] = compose_prd_summary_crew().crew()
    crews["extract_constraints"] = extract_constraints_crew().crew()
    crews["extract_key_features"] = extract_key_features_crew().crew()
    crews["generate_feature_descriptions"] = generate_feature_descriptions_crew().crew()
    crews["identify_core_objective"] = identify_core_objective_crew().crew()
    crews["identify_major_risks"] = identify_major_risks_crew().crew()
    crews["identify_success_metrics"] = identify_success_metrics_crew().crew()
    crews["list_primary_user_roles"] = list_primary_user_roles_crew().crew()
    crews["prioritize_features"] = prioritize_features_crew().crew()

    # Level 0 execution
    results["extract_constraints"] = await crews["extract_constraints"].kickoff_async(inputs=inputs)
    results["identify_core_objective"] = await crews["identify_core_objective"].kickoff_async(inputs=inputs)
    results["identify_major_risks"] = await crews["identify_major_risks"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["extract_key_features"].kickoff_async(inputs={"identify_core_objective_output": results["identify_core_objective"].raw}), crews["identify_success_metrics"].kickoff_async(inputs={"identify_core_objective_output": results["identify_core_objective"].raw}), crews["list_primary_user_roles"].kickoff_async(inputs={"identify_core_objective_output": results["identify_core_objective"].raw}))
    for node_name, result in zip(['extract_key_features', 'identify_success_metrics', 'list_primary_user_roles'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["generate_feature_descriptions"].kickoff_async(inputs={"extract_key_features_output": results["extract_key_features"].raw}), crews["prioritize_features"].kickoff_async(inputs={"extract_key_features_output": results["extract_key_features"].raw}))
    for node_name, result in zip(['generate_feature_descriptions', 'prioritize_features'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["compose_prd_summary"].kickoff_async(inputs={"identify_core_objective_output": results["identify_core_objective"].raw, "list_primary_user_roles_output": results["list_primary_user_roles"].raw, "extract_key_features_output": results["extract_key_features"].raw, "generate_feature_descriptions_output": results["generate_feature_descriptions"].raw}))
    for node_name, result in zip(['compose_prd_summary'], level_results):
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
