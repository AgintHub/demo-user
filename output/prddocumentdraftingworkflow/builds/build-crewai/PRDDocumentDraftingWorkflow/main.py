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

from crews.compile_final_prd_document_crew import compile_final_prd_document_crew
from crews.define_success_metrics_crew import define_success_metrics_crew
from crews.define_user_journeys_for_each_role_crew import define_user_journeys_for_each_role_crew
from crews.draft_prd_section_constraints_crew import draft_prd_section_constraints_crew
from crews.draft_prd_section_features_crew import draft_prd_section_features_crew
from crews.draft_prd_section_objectives_crew import draft_prd_section_objectives_crew
from crews.draft_prd_section_stakeholders_crew import draft_prd_section_stakeholders_crew
from crews.draft_prd_section_success_metrics_crew import draft_prd_section_success_metrics_crew
from crews.draft_prd_section_user_journeys_crew import draft_prd_section_user_journeys_crew
from crews.draft_prd_section_user_roles_crew import draft_prd_section_user_roles_crew
from crews.extract_core_product_features_crew import extract_core_product_features_crew
from crews.extract_critical_constraints_crew import extract_critical_constraints_crew
from crews.extract_objectives_from_workflow_requirements_crew import extract_objectives_from_workflow_requirements_crew
from crews.identify_primary_user_roles_crew import identify_primary_user_roles_crew
from crews.summarize_key_stakeholders_crew import summarize_key_stakeholders_crew


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
    crews["compile_final_prd_document"] = compile_final_prd_document_crew().crew()
    crews["define_success_metrics"] = define_success_metrics_crew().crew()
    crews["define_user_journeys_for_each_role"] = define_user_journeys_for_each_role_crew().crew()
    crews["draft_prd_section_constraints"] = draft_prd_section_constraints_crew().crew()
    crews["draft_prd_section_features"] = draft_prd_section_features_crew().crew()
    crews["draft_prd_section_objectives"] = draft_prd_section_objectives_crew().crew()
    crews["draft_prd_section_stakeholders"] = draft_prd_section_stakeholders_crew().crew()
    crews["draft_prd_section_success_metrics"] = draft_prd_section_success_metrics_crew().crew()
    crews["draft_prd_section_user_journeys"] = draft_prd_section_user_journeys_crew().crew()
    crews["draft_prd_section_user_roles"] = draft_prd_section_user_roles_crew().crew()
    crews["extract_core_product_features"] = extract_core_product_features_crew().crew()
    crews["extract_critical_constraints"] = extract_critical_constraints_crew().crew()
    crews["extract_objectives_from_workflow_requirements"] = extract_objectives_from_workflow_requirements_crew().crew()
    crews["identify_primary_user_roles"] = identify_primary_user_roles_crew().crew()
    crews["summarize_key_stakeholders"] = summarize_key_stakeholders_crew().crew()

    # Level 0 execution
    results["extract_critical_constraints"] = await crews["extract_critical_constraints"].kickoff_async(inputs=inputs)
    results["extract_objectives_from_workflow_requirements"] = await crews["extract_objectives_from_workflow_requirements"].kickoff_async(inputs=inputs)
    results["identify_primary_user_roles"] = await crews["identify_primary_user_roles"].kickoff_async(inputs=inputs)
    results["summarize_key_stakeholders"] = await crews["summarize_key_stakeholders"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["define_success_metrics"].kickoff_async(inputs={"extract_objectives_from_workflow_requirements_output": results["extract_objectives_from_workflow_requirements"].raw}), crews["draft_prd_section_constraints"].kickoff_async(inputs={"extract_critical_constraints_output": results["extract_critical_constraints"].raw}), crews["draft_prd_section_objectives"].kickoff_async(inputs={"extract_objectives_from_workflow_requirements_output": results["extract_objectives_from_workflow_requirements"].raw}), crews["draft_prd_section_stakeholders"].kickoff_async(inputs={"summarize_key_stakeholders_output": results["summarize_key_stakeholders"].raw}), crews["draft_prd_section_user_roles"].kickoff_async(inputs={"identify_primary_user_roles_output": results["identify_primary_user_roles"].raw}), crews["extract_core_product_features"].kickoff_async(inputs={"extract_objectives_from_workflow_requirements_output": results["extract_objectives_from_workflow_requirements"].raw}))
    for node_name, result in zip(['define_success_metrics', 'draft_prd_section_constraints', 'draft_prd_section_objectives', 'draft_prd_section_stakeholders', 'draft_prd_section_user_roles', 'extract_core_product_features'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["define_user_journeys_for_each_role"].kickoff_async(inputs={"identify_primary_user_roles_output": results["identify_primary_user_roles"].raw, "extract_core_product_features_output": results["extract_core_product_features"].raw}), crews["draft_prd_section_features"].kickoff_async(inputs={"extract_core_product_features_output": results["extract_core_product_features"].raw}), crews["draft_prd_section_success_metrics"].kickoff_async(inputs={"define_success_metrics_output": results["define_success_metrics"].raw}))
    for node_name, result in zip(['define_user_journeys_for_each_role', 'draft_prd_section_features', 'draft_prd_section_success_metrics'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["draft_prd_section_user_journeys"].kickoff_async(inputs={"define_user_journeys_for_each_role_output": results["define_user_journeys_for_each_role"].raw}))
    for node_name, result in zip(['draft_prd_section_user_journeys'], level_results):
        results[node_name] = result

    # Level 4 execution
    level_results = await asyncio.gather(crews["compile_final_prd_document"].kickoff_async(inputs={"draft_prd_section_objectives_output": results["draft_prd_section_objectives"].raw, "draft_prd_section_user_roles_output": results["draft_prd_section_user_roles"].raw, "draft_prd_section_features_output": results["draft_prd_section_features"].raw, "draft_prd_section_constraints_output": results["draft_prd_section_constraints"].raw, "draft_prd_section_success_metrics_output": results["draft_prd_section_success_metrics"].raw, "draft_prd_section_stakeholders_output": results["draft_prd_section_stakeholders"].raw, "draft_prd_section_user_journeys_output": results["draft_prd_section_user_journeys"].raw}))
    for node_name, result in zip(['compile_final_prd_document'], level_results):
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
