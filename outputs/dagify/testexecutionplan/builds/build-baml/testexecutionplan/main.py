import asyncio
import os
import json
from typing import Any, Dict

class BamlObjectEncoder(json.JSONEncoder):
    """Custom JSON encoder for BAML objects."""
    def default(self, obj):
        # Convert BAML objects to dictionaries
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        # Handle other special types if needed
        elif hasattr(obj, "model_dump"):
            # Support for Pydantic models
            return obj.model_dump()
        # Let the base encoder handle standard types
        return super().default(obj)

def serialize_results(result_obj):
    """Convert potentially complex objects to JSON-serializable format."""
    if hasattr(result_obj, "__dict__"):
        return {k: serialize_results(v) for k, v in result_obj.__dict__.items() if not k.startswith("_")}
    elif isinstance(result_obj, dict):
        return {k: serialize_results(v) for k, v in result_obj.items()}
    elif isinstance(result_obj, list):
        return [serialize_results(item) for item in result_obj]
    elif hasattr(result_obj, "model_dump"):
        return serialize_results(result_obj.model_dump())
    else:
        return result_obj

if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Please set it with: export OPENAI_API_KEY='your-api-key'")
    print("This key is required for the BAML workflow to make API calls to OpenAI.")
    exit(1)

try:
    from baml_client import b
except ImportError:
    print("Warning: baml_client not found. Please run 'baml-cli generate' in the project root after baml_src is populated.")
    b = None

results_store: Dict[str, Any] = {}

async def run_determine_test_objective(initial_input: Any) -> Any:
    print(f"Executing: determine_test_objective...")
    if not b:
        print(f"Skipping Process_determine_test_objective as baml_client is not available.")
        return None
    try:
        result = await b.Process_determine_test_objective(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"determine_test_objective Result: {result}")
        results_store["determine_test_objective"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_determine_test_objective: {e}")
        results_store["determine_test_objective"] = f"Error: {e}"
        return None

async def run_test_data_gathering(determine_test_objective_output: Any) -> Any:
    print(f"Executing: test_data_gathering...")
    if not b:
        print(f"Skipping Process_test_data_gathering as baml_client is not available.")
        return None
    try:
        result = await b.Process_test_data_gathering(determine_test_objective_output=determine_test_objective_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"test_data_gathering Result: {result}")
        results_store["test_data_gathering"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_test_data_gathering: {e}")
        results_store["test_data_gathering"] = f"Error: {e}"
        return None

async def run_formulate_test_conditions(determine_test_objective_output: Any, test_data_gathering_output: Any) -> Any:
    print(f"Executing: formulate_test_conditions...")
    if not b:
        print(f"Skipping Process_formulate_test_conditions as baml_client is not available.")
        return None
    try:
        result = await b.Process_formulate_test_conditions(determine_test_objective_output=determine_test_objective_output, test_data_gathering_output=test_data_gathering_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"formulate_test_conditions Result: {result}")
        results_store["formulate_test_conditions"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_formulate_test_conditions: {e}")
        results_store["formulate_test_conditions"] = f"Error: {e}"
        return None

async def run_evaluate_test_outcomes(formulate_test_conditions_output: Any, test_data_gathering_output: Any) -> Any:
    print(f"Executing: evaluate_test_outcomes...")
    if not b:
        print(f"Skipping Process_evaluate_test_outcomes as baml_client is not available.")
        return None
    try:
        result = await b.Process_evaluate_test_outcomes(formulate_test_conditions_output=formulate_test_conditions_output, test_data_gathering_output=test_data_gathering_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"evaluate_test_outcomes Result: {result}")
        results_store["evaluate_test_outcomes"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_evaluate_test_outcomes: {e}")
        results_store["evaluate_test_outcomes"] = f"Error: {e}"
        return None

async def run_report_test_results(evaluate_test_outcomes_output: Any) -> Any:
    print(f"Executing: report_test_results...")
    if not b:
        print(f"Skipping Process_report_test_results as baml_client is not available.")
        return None
    try:
        result = await b.Process_report_test_results(evaluate_test_outcomes_output=evaluate_test_outcomes_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"report_test_results Result: {result}")
        results_store["report_test_results"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_report_test_results: {e}")
        results_store["report_test_results"] = f"Error: {e}"
        return None

async def main(initial_workflow_input: Any):
    print("Starting BAML DAG workflow...")
    # --- Level 0 ---
    level_0_tasks = []
    level_0_tasks.append(run_determine_test_objective(initial_workflow_input))
    await asyncio.gather(*level_0_tasks)
    # --- Level 1 ---
    level_1_tasks = []
    level_1_tasks.append(run_test_data_gathering(results_store['determine_test_objective']))
    await asyncio.gather(*level_1_tasks)
    # --- Level 2 ---
    level_2_tasks = []
    level_2_tasks.append(run_formulate_test_conditions(results_store['determine_test_objective'], results_store['test_data_gathering']))
    await asyncio.gather(*level_2_tasks)
    # --- Level 3 ---
    level_3_tasks = []
    level_3_tasks.append(run_evaluate_test_outcomes(results_store['formulate_test_conditions'], results_store['test_data_gathering']))
    await asyncio.gather(*level_3_tasks)
    # --- Level 4 ---
    level_4_tasks = []
    level_4_tasks.append(run_report_test_results(results_store['evaluate_test_outcomes']))
    await asyncio.gather(*level_4_tasks)

    print("\nWorkflow execution finished.")
    print("Final results_store:")
    # Use the custom JSON encoder to safely serialize BAML objects
    try:
        print(json.dumps(results_store, indent=2, cls=BamlObjectEncoder))
    except TypeError as e:
        print(f"Error serializing results: {e}")
        print("Simplified results:")
        for k, v in results_store.items():
            print(f"  {k}: {type(v).__name__}")
    return results_store

if __name__ == "__main__":
    print("Enter initial input for the workflow (JSON string or plain text):")
    cli_input_str = input()
    try:
        initial_input_data = json.loads(cli_input_str)
    except json.JSONDecodeError:
        initial_input_data = cli_input_str
    asyncio.run(main(initial_input_data))