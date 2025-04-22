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

from crews.analyze_test_results_crew import analyze_test_results_crew
from crews.document_test_results_crew import document_test_results_crew
from crews.get_testing_environment_crew import get_testing_environment_crew
from crews.perform_test_cases_crew import perform_test_cases_crew
from crews.select_test_cases_crew import select_test_cases_crew


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
    crews["analyze_test_results"] = analyze_test_results_crew().crew()
    crews["document_test_results"] = document_test_results_crew().crew()
    crews["get_testing_environment"] = get_testing_environment_crew().crew()
    crews["perform_test_cases"] = perform_test_cases_crew().crew()
    crews["select_test_cases"] = select_test_cases_crew().crew()

    # Level 0 execution
    results["get_testing_environment"] = await crews["get_testing_environment"].kickoff_async(inputs=inputs)

    # Level 1 execution
    level_results = await asyncio.gather(crews["select_test_cases"].kickoff_async(inputs={"get_testing_environment_output": results["get_testing_environment"].raw}))
    for node_name, result in zip(['select_test_cases'], level_results):
        results[node_name] = result

    # Level 2 execution
    level_results = await asyncio.gather(crews["perform_test_cases"].kickoff_async(inputs={"select_test_cases_output": results["select_test_cases"].raw}))
    for node_name, result in zip(['perform_test_cases'], level_results):
        results[node_name] = result

    # Level 3 execution
    level_results = await asyncio.gather(crews["analyze_test_results"].kickoff_async(inputs={"perform_test_cases_output": results["perform_test_cases"].raw}))
    for node_name, result in zip(['analyze_test_results'], level_results):
        results[node_name] = result

    # Level 4 execution
    level_results = await asyncio.gather(crews["document_test_results"].kickoff_async(inputs={"analyze_test_results_output": results["analyze_test_results"].raw}))
    for node_name, result in zip(['document_test_results'], level_results):
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
