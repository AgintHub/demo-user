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

async def run_define_hedge_fund_strategy(initial_input: Any) -> Any:
    print(f"Executing: define_hedge_fund_strategy...")
    if not b:
        print(f"Skipping Process_define_hedge_fund_strategy as baml_client is not available.")
        return None
    try:
        result = await b.Process_define_hedge_fund_strategy(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"define_hedge_fund_strategy Result: {result}")
        results_store["define_hedge_fund_strategy"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_define_hedge_fund_strategy: {e}")
        results_store["define_hedge_fund_strategy"] = f"Error: {e}"
        return None

async def run_establish_fund_constitution(initial_input: Any) -> Any:
    print(f"Executing: establish_fund_constitution...")
    if not b:
        print(f"Skipping Process_establish_fund_constitution as baml_client is not available.")
        return None
    try:
        result = await b.Process_establish_fund_constitution(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"establish_fund_constitution Result: {result}")
        results_store["establish_fund_constitution"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_establish_fund_constitution: {e}")
        results_store["establish_fund_constitution"] = f"Error: {e}"
        return None

async def run_select__Investment_vessels(define_hedge_fund_strategy_output: Any) -> Any:
    print(f"Executing: select_ Investment_vessels...")
    if not b:
        print(f"Skipping Process_select__Investment_vessels as baml_client is not available.")
        return None
    try:
        result = await b.Process_select__Investment_vessels(define_hedge_fund_strategy_output=define_hedge_fund_strategy_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"select_ Investment_vessels Result: {result}")
        results_store["select_ Investment_vessels"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_select__Investment_vessels: {e}")
        results_store["select_ Investment_vessels"] = f"Error: {e}"
        return None

async def run_set_up_trading_operations(establish_fund_constitution_output: Any) -> Any:
    print(f"Executing: set_up_trading_operations...")
    if not b:
        print(f"Skipping Process_set_up_trading_operations as baml_client is not available.")
        return None
    try:
        result = await b.Process_set_up_trading_operations(establish_fund_constitution_output=establish_fund_constitution_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"set_up_trading_operations Result: {result}")
        results_store["set_up_trading_operations"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_set_up_trading_operations: {e}")
        results_store["set_up_trading_operations"] = f"Error: {e}"
        return None

async def run_hire_key_fund_professionals(set_up_trading_operations_output: Any) -> Any:
    print(f"Executing: hire_key_fund_professionals...")
    if not b:
        print(f"Skipping Process_hire_key_fund_professionals as baml_client is not available.")
        return None
    try:
        result = await b.Process_hire_key_fund_professionals(set_up_trading_operations_output=set_up_trading_operations_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"hire_key_fund_professionals Result: {result}")
        results_store["hire_key_fund_professionals"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_hire_key_fund_professionals: {e}")
        results_store["hire_key_fund_professionals"] = f"Error: {e}"
        return None

async def run_develop_operating_manual(hire_key_fund_professionals_output: Any) -> Any:
    print(f"Executing: develop_operating_manual...")
    if not b:
        print(f"Skipping Process_develop_operating_manual as baml_client is not available.")
        return None
    try:
        result = await b.Process_develop_operating_manual(hire_key_fund_professionals_output=hire_key_fund_professionals_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"develop_operating_manual Result: {result}")
        results_store["develop_operating_manual"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_develop_operating_manual: {e}")
        results_store["develop_operating_manual"] = f"Error: {e}"
        return None

async def run_register_hedge_fund(develop_operating_manual_output: Any) -> Any:
    print(f"Executing: register_hedge_fund...")
    if not b:
        print(f"Skipping Process_register_hedge_fund as baml_client is not available.")
        return None
    try:
        result = await b.Process_register_hedge_fund(develop_operating_manual_output=develop_operating_manual_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"register_hedge_fund Result: {result}")
        results_store["register_hedge_fund"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_register_hedge_fund: {e}")
        results_store["register_hedge_fund"] = f"Error: {e}"
        return None

async def main(initial_workflow_input: Any):
    print("Starting BAML DAG workflow...")
    # --- Level 0 ---
    level_0_tasks = []
    level_0_tasks.append(run_define_hedge_fund_strategy(initial_workflow_input))
    level_0_tasks.append(run_establish_fund_constitution(initial_workflow_input))
    await asyncio.gather(*level_0_tasks)
    # --- Level 1 ---
    level_1_tasks = []
    level_1_tasks.append(run_select__Investment_vessels(results_store['define_hedge_fund_strategy']))
    level_1_tasks.append(run_set_up_trading_operations(results_store['establish_fund_constitution']))
    await asyncio.gather(*level_1_tasks)
    # --- Level 2 ---
    level_2_tasks = []
    level_2_tasks.append(run_hire_key_fund_professionals(results_store['set_up_trading_operations']))
    await asyncio.gather(*level_2_tasks)
    # --- Level 3 ---
    level_3_tasks = []
    level_3_tasks.append(run_develop_operating_manual(results_store['hire_key_fund_professionals']))
    await asyncio.gather(*level_3_tasks)
    # --- Level 4 ---
    level_4_tasks = []
    level_4_tasks.append(run_register_hedge_fund(results_store['develop_operating_manual']))
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