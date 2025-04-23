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

from crews.classify_feature_priorities_crew import classify_feature_priorities_crew
from crews.determine_target_users_crew import determine_target_users_crew
from crews.determine_technical_constraints_crew import determine_technical_constraints_crew
from crews.extract_feature_requirements_crew import extract_feature_requirements_crew
from crews.extract_primary_objective_crew import extract_primary_objective_crew
from crews.extract_product_name_crew import extract_product_name_crew
from crews.extract_success_metrics_crew import extract_success_metrics_crew
from crews.extract_user_stories_crew import extract_user_stories_crew
from crews.identify_user_problems_crew import identify_user_problems_crew
from crews.summarize_prd_document_crew import summarize_prd_document_crew


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
    crews["classify_feature_priorities"] = classify_feature_priorities_crew().crew()
    crews["determine_target_users"] = determine_target_users_crew().crew()
    crews["determine_technical_constraints"] = determine_technical_constraints_crew().crew()
    crews["extract_feature_requirements"] = extract_feature_requirements_crew().crew()
    crews["extract_primary_objective"] = extract_primary_objective_crew().crew()
    crews["extract_product_name"] = extract_product_name_crew().crew()
    crews["extract_success_metrics"] = extract_success_metrics_crew().crew()
    crews["extract_user_stories"] = extract_user_stories_crew().crew()
    crews["identify_user_problems"] = identify_user_problems_crew().crew()
    crews["summarize_prd_document"] = summarize_prd_document_crew().crew()

    # Level 0 execution
    results["extract_product_name"] = await crews["extract_product_name"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["determine_target_users"].kickoff_async(inputs={"extract_product_name_output": results["extract_product_name"].raw}), crews["extract_primary_objective"].kickoff_async(inputs={"extract_product_name_output": results["extract_product_name"].raw}))
    for node_name, result in zip(['determine_target_users', 'extract_primary_objective'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["identify_user_problems"].kickoff_async(inputs={"extract_product_name_output": results["extract_product_name"].raw, "determine_target_users_output": results["determine_target_users"].raw}))
    for node_name, result in zip(['identify_user_problems'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["extract_user_stories"].kickoff_async(inputs={"identify_user_problems_output": results["identify_user_problems"].raw}))
    for node_name, result in zip(['extract_user_stories'], level_results):
        results[node_name] = result

    # Level 4 execution
    level_results = await asyncio.gather(crews["extract_feature_requirements"].kickoff_async(inputs={"extract_user_stories_output": results["extract_user_stories"].raw}))
    for node_name, result in zip(['extract_feature_requirements'], level_results):
        results[node_name] = result

    # Level 5 execution
    level_results = await asyncio.gather(crews["classify_feature_priorities"].kickoff_async(inputs={"extract_feature_requirements_output": results["extract_feature_requirements"].raw}))
    for node_name, result in zip(['classify_feature_priorities'], level_results):
        results[node_name] = result

    # Level 6 execution
    level_results = await asyncio.gather(crews["determine_technical_constraints"].kickoff_async(inputs={"classify_feature_priorities_output": results["classify_feature_priorities"].raw}))
    for node_name, result in zip(['determine_technical_constraints'], level_results):
        results[node_name] = result

    # Level 7 execution
    level_results = await asyncio.gather(crews["extract_success_metrics"].kickoff_async(inputs={"extract_primary_objective_output": results["extract_primary_objective"].raw, "determine_technical_constraints_output": results["determine_technical_constraints"].raw}))
    for node_name, result in zip(['extract_success_metrics'], level_results):
        results[node_name] = result

    # Level 8 execution
    level_results = await asyncio.gather(crews["summarize_prd_document"].kickoff_async(inputs={"extract_product_name_output": results["extract_product_name"].raw, "extract_primary_objective_output": results["extract_primary_objective"].raw, "determine_target_users_output": results["determine_target_users"].raw, "identify_user_problems_output": results["identify_user_problems"].raw, "extract_user_stories_output": results["extract_user_stories"].raw, "extract_feature_requirements_output": results["extract_feature_requirements"].raw, "classify_feature_priorities_output": results["classify_feature_priorities"].raw, "determine_technical_constraints_output": results["determine_technical_constraints"].raw, "extract_success_metrics_output": results["extract_success_metrics"].raw}))
    for node_name, result in zip(['summarize_prd_document'], level_results):
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
