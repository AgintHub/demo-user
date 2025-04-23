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

from crews.assess_major_risks_crew import assess_major_risks_crew
from crews.assign_feature_priorities_crew import assign_feature_priorities_crew
from crews.define_stakeholder_roles_crew import define_stakeholder_roles_crew
from crews.extract_acceptance_criteria_crew import extract_acceptance_criteria_crew
from crews.extract_workflow_overview_crew import extract_workflow_overview_crew
from crews.formulate_user_stories_crew import formulate_user_stories_crew
from crews.identify_core_features_crew import identify_core_features_crew
from crews.identify_project_constraints_crew import identify_project_constraints_crew


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
    crews["assess_major_risks"] = assess_major_risks_crew().crew()
    crews["assign_feature_priorities"] = assign_feature_priorities_crew().crew()
    crews["define_stakeholder_roles"] = define_stakeholder_roles_crew().crew()
    crews["extract_acceptance_criteria"] = extract_acceptance_criteria_crew().crew()
    crews["extract_workflow_overview"] = extract_workflow_overview_crew().crew()
    crews["formulate_user_stories"] = formulate_user_stories_crew().crew()
    crews["identify_core_features"] = identify_core_features_crew().crew()
    crews["identify_project_constraints"] = identify_project_constraints_crew().crew()

    # Level 0 execution
    results["extract_workflow_overview"] = await crews["extract_workflow_overview"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["define_stakeholder_roles"].kickoff_async(inputs={"extract_workflow_overview_output": results["extract_workflow_overview"].raw}), crews["identify_core_features"].kickoff_async(inputs={"extract_workflow_overview_output": results["extract_workflow_overview"].raw}), crews["identify_project_constraints"].kickoff_async(inputs={"extract_workflow_overview_output": results["extract_workflow_overview"].raw}))
    for node_name, result in zip(['define_stakeholder_roles', 'identify_core_features', 'identify_project_constraints'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["assess_major_risks"].kickoff_async(inputs={"extract_workflow_overview_output": results["extract_workflow_overview"].raw, "identify_project_constraints_output": results["identify_project_constraints"].raw}), crews["assign_feature_priorities"].kickoff_async(inputs={"identify_core_features_output": results["identify_core_features"].raw}), crews["formulate_user_stories"].kickoff_async(inputs={"identify_core_features_output": results["identify_core_features"].raw, "define_stakeholder_roles_output": results["define_stakeholder_roles"].raw}))
    for node_name, result in zip(['assess_major_risks', 'assign_feature_priorities', 'formulate_user_stories'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["extract_acceptance_criteria"].kickoff_async(inputs={"formulate_user_stories_output": results["formulate_user_stories"].raw}))
    for node_name, result in zip(['extract_acceptance_criteria'], level_results):
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
