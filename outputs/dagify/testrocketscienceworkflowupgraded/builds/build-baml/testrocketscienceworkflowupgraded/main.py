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

async def run_define_test_parameters(initial_input: Any) -> Any:
    print(f"Executing: define_test_parameters...")
    if not b:
        print(f"Skipping Process_define_test_parameters as baml_client is not available.")
        return None
    try:
        result = await b.Process_define_test_parameters(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"define_test_parameters Result: {result}")
        results_store["define_test_parameters"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_define_test_parameters: {e}")
        results_store["define_test_parameters"] = f"Error: {e}"
        return None

async def run_fetch_test_parameters(initial_input: Any) -> Any:
    print(f"Executing: fetch_test_parameters...")
    if not b:
        print(f"Skipping Process_fetch_test_parameters as baml_client is not available.")
        return None
    try:
        result = await b.Process_fetch_test_parameters(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"fetch_test_parameters Result: {result}")
        results_store["fetch_test_parameters"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_fetch_test_parameters: {e}")
        results_store["fetch_test_parameters"] = f"Error: {e}"
        return None

async def run_verify_test_conditions(fetch_test_parameters_output: Any) -> Any:
    print(f"Executing: verify_test_conditions...")
    if not b:
        print(f"Skipping Process_verify_test_conditions as baml_client is not available.")
        return None
    try:
        result = await b.Process_verify_test_conditions(fetch_test_parameters_output=fetch_test_parameters_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"verify_test_conditions Result: {result}")
        results_store["verify_test_conditions"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_verify_test_conditions: {e}")
        results_store["verify_test_conditions"] = f"Error: {e}"
        return None

async def run_simulate_experiment(verify_test_conditions_output: Any) -> Any:
    print(f"Executing: simulate_experiment...")
    if not b:
        print(f"Skipping Process_simulate_experiment as baml_client is not available.")
        return None
    try:
        result = await b.Process_simulate_experiment(verify_test_conditions_output=verify_test_conditions_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"simulate_experiment Result: {result}")
        results_store["simulate_experiment"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_simulate_experiment: {e}")
        results_store["simulate_experiment"] = f"Error: {e}"
        return None

async def run_analyze_results(simulate_experiment_output: Any) -> Any:
    print(f"Executing: analyze_results...")
    if not b:
        print(f"Skipping Process_analyze_results as baml_client is not available.")
        return None
    try:
        result = await b.Process_analyze_results(simulate_experiment_output=simulate_experiment_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"analyze_results Result: {result}")
        results_store["analyze_results"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_analyze_results: {e}")
        results_store["analyze_results"] = f"Error: {e}"
        return None

async def run_document_experiment_report(analyze_results_output: Any) -> Any:
    print(f"Executing: document_experiment_report...")
    if not b:
        print(f"Skipping Process_document_experiment_report as baml_client is not available.")
        return None
    try:
        result = await b.Process_document_experiment_report(analyze_results_output=analyze_results_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"document_experiment_report Result: {result}")
        results_store["document_experiment_report"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_document_experiment_report: {e}")
        results_store["document_experiment_report"] = f"Error: {e}"
        return None

async def main(initial_workflow_input: Any):
    print("Starting BAML DAG workflow...")
    # --- Level 0 ---
    level_0_tasks = []
    level_0_tasks.append(run_define_test_parameters(initial_workflow_input))
    level_0_tasks.append(run_fetch_test_parameters(initial_workflow_input))
    await asyncio.gather(*level_0_tasks)
    # --- Level 1 ---
    level_1_tasks = []
    level_1_tasks.append(run_verify_test_conditions(results_store['fetch_test_parameters']))
    await asyncio.gather(*level_1_tasks)
    # --- Level 2 ---
    level_2_tasks = []
    level_2_tasks.append(run_simulate_experiment(results_store['verify_test_conditions']))
    await asyncio.gather(*level_2_tasks)
    # --- Level 3 ---
    level_3_tasks = []
    level_3_tasks.append(run_analyze_results(results_store['simulate_experiment']))
    await asyncio.gather(*level_3_tasks)
    # --- Level 4 ---
    level_4_tasks = []
    level_4_tasks.append(run_document_experiment_report(results_store['analyze_results']))
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