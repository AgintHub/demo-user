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

async def run_IdentifyMissionRequirements(initial_input: Any) -> Any:
    print(f"Executing: IdentifyMissionRequirements...")
    if not b:
        print(f"Skipping Process_IdentifyMissionRequirements as baml_client is not available.")
        return None
    try:
        result = await b.Process_IdentifyMissionRequirements(input_payload=initial_input)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"IdentifyMissionRequirements Result: {result}")
        results_store["IdentifyMissionRequirements"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_IdentifyMissionRequirements: {e}")
        results_store["IdentifyMissionRequirements"] = f"Error: {e}"
        return None

async def run_DesignRocketConfiguration(IdentifyMissionRequirements_output: Any) -> Any:
    print(f"Executing: DesignRocketConfiguration...")
    if not b:
        print(f"Skipping Process_DesignRocketConfiguration as baml_client is not available.")
        return None
    try:
        result = await b.Process_DesignRocketConfiguration(IdentifyMissionRequirements_output=IdentifyMissionRequirements_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"DesignRocketConfiguration Result: {result}")
        results_store["DesignRocketConfiguration"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_DesignRocketConfiguration: {e}")
        results_store["DesignRocketConfiguration"] = f"Error: {e}"
        return None

async def run_SpecifyRocketMaterials(DesignRocketConfiguration_output: Any) -> Any:
    print(f"Executing: SpecifyRocketMaterials...")
    if not b:
        print(f"Skipping Process_SpecifyRocketMaterials as baml_client is not available.")
        return None
    try:
        result = await b.Process_SpecifyRocketMaterials(DesignRocketConfiguration_output=DesignRocketConfiguration_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"SpecifyRocketMaterials Result: {result}")
        results_store["SpecifyRocketMaterials"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_SpecifyRocketMaterials: {e}")
        results_store["SpecifyRocketMaterials"] = f"Error: {e}"
        return None

async def run_ConductStructuralAnalysis(DesignRocketConfiguration_output: Any, SpecifyRocketMaterials_output: Any) -> Any:
    print(f"Executing: ConductStructuralAnalysis...")
    if not b:
        print(f"Skipping Process_ConductStructuralAnalysis as baml_client is not available.")
        return None
    try:
        result = await b.Process_ConductStructuralAnalysis(DesignRocketConfiguration_output=DesignRocketConfiguration_output, SpecifyRocketMaterials_output=SpecifyRocketMaterials_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"ConductStructuralAnalysis Result: {result}")
        results_store["ConductStructuralAnalysis"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_ConductStructuralAnalysis: {e}")
        results_store["ConductStructuralAnalysis"] = f"Error: {e}"
        return None

async def run_PlanRocketManufacturingProcess(DesignRocketConfiguration_output: Any, SpecifyRocketMaterials_output: Any) -> Any:
    print(f"Executing: PlanRocketManufacturingProcess...")
    if not b:
        print(f"Skipping Process_PlanRocketManufacturingProcess as baml_client is not available.")
        return None
    try:
        result = await b.Process_PlanRocketManufacturingProcess(DesignRocketConfiguration_output=DesignRocketConfiguration_output, SpecifyRocketMaterials_output=SpecifyRocketMaterials_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"PlanRocketManufacturingProcess Result: {result}")
        results_store["PlanRocketManufacturingProcess"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_PlanRocketManufacturingProcess: {e}")
        results_store["PlanRocketManufacturingProcess"] = f"Error: {e}"
        return None

async def run_IntegrateRocketSystems(ConductStructuralAnalysis_output: Any, PlanRocketManufacturingProcess_output: Any) -> Any:
    print(f"Executing: IntegrateRocketSystems...")
    if not b:
        print(f"Skipping Process_IntegrateRocketSystems as baml_client is not available.")
        return None
    try:
        result = await b.Process_IntegrateRocketSystems(ConductStructuralAnalysis_output=ConductStructuralAnalysis_output, PlanRocketManufacturingProcess_output=PlanRocketManufacturingProcess_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"IntegrateRocketSystems Result: {result}")
        results_store["IntegrateRocketSystems"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_IntegrateRocketSystems: {e}")
        results_store["IntegrateRocketSystems"] = f"Error: {e}"
        return None

async def run_PerformSystemValidation(IntegrateRocketSystems_output: Any) -> Any:
    print(f"Executing: PerformSystemValidation...")
    if not b:
        print(f"Skipping Process_PerformSystemValidation as baml_client is not available.")
        return None
    try:
        result = await b.Process_PerformSystemValidation(IntegrateRocketSystems_output=IntegrateRocketSystems_output)
        # Convert result to a serializable format
        serializable_result = serialize_results(result)
        print(f"PerformSystemValidation Result: {result}")
        results_store["PerformSystemValidation"] = serializable_result
        return result
    except Exception as e:
        print(f"Error executing Process_PerformSystemValidation: {e}")
        results_store["PerformSystemValidation"] = f"Error: {e}"
        return None

async def main(initial_workflow_input: Any):
    print("Starting BAML DAG workflow...")
    # --- Level 0 ---
    level_0_tasks = []
    level_0_tasks.append(run_IdentifyMissionRequirements(initial_workflow_input))
    await asyncio.gather(*level_0_tasks)
    # --- Level 1 ---
    level_1_tasks = []
    level_1_tasks.append(run_DesignRocketConfiguration(results_store['IdentifyMissionRequirements']))
    await asyncio.gather(*level_1_tasks)
    # --- Level 2 ---
    level_2_tasks = []
    level_2_tasks.append(run_SpecifyRocketMaterials(results_store['DesignRocketConfiguration']))
    await asyncio.gather(*level_2_tasks)
    # --- Level 3 ---
    level_3_tasks = []
    level_3_tasks.append(run_ConductStructuralAnalysis(results_store['DesignRocketConfiguration'], results_store['SpecifyRocketMaterials']))
    level_3_tasks.append(run_PlanRocketManufacturingProcess(results_store['DesignRocketConfiguration'], results_store['SpecifyRocketMaterials']))
    await asyncio.gather(*level_3_tasks)
    # --- Level 4 ---
    level_4_tasks = []
    level_4_tasks.append(run_IntegrateRocketSystems(results_store['ConductStructuralAnalysis'], results_store['PlanRocketManufacturingProcess']))
    await asyncio.gather(*level_4_tasks)
    # --- Level 5 ---
    level_5_tasks = []
    level_5_tasks.append(run_PerformSystemValidation(results_store['IntegrateRocketSystems']))
    await asyncio.gather(*level_5_tasks)

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