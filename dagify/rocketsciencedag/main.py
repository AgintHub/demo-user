import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.ConductStructuralAnalysis import ConductStructuralAnalysis
from code.DesignRocketConfiguration import DesignRocketConfiguration
from code.IdentifyMissionRequirements import IdentifyMissionRequirements
from code.IntegrateRocketSystems import IntegrateRocketSystems
from code.PerformSystemValidation import PerformSystemValidation
from code.PlanRocketManufacturingProcess import PlanRocketManufacturingProcess
from code.SpecifyRocketMaterials import SpecifyRocketMaterials

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

ConductStructuralAnalysis_async = make_async(ConductStructuralAnalysis)
DesignRocketConfiguration_async = make_async(DesignRocketConfiguration)
IdentifyMissionRequirements_async = make_async(IdentifyMissionRequirements)
IntegrateRocketSystems_async = make_async(IntegrateRocketSystems)
PerformSystemValidation_async = make_async(PerformSystemValidation)
PlanRocketManufacturingProcess_async = make_async(PlanRocketManufacturingProcess)
SpecifyRocketMaterials_async = make_async(SpecifyRocketMaterials)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: IdentifyMissionRequirements
    async def run_IdentifyMissionRequirements():
        # Call the async version of IdentifyMissionRequirements with results from dependencies
        return await IdentifyMissionRequirements_async(user_input)

    # Run level 0 nodes in parallel
    results['IdentifyMissionRequirements'] = await run_IdentifyMissionRequirements()

    # Level 1: DesignRocketConfiguration
    async def run_DesignRocketConfiguration():
        # Call the async version of DesignRocketConfiguration with results from dependencies
        return await DesignRocketConfiguration_async(results['IdentifyMissionRequirements'])

    # Run level 1 nodes in parallel
    results['DesignRocketConfiguration'] = await run_DesignRocketConfiguration()

    # Level 2: SpecifyRocketMaterials
    async def run_SpecifyRocketMaterials():
        # Call the async version of SpecifyRocketMaterials with results from dependencies
        return await SpecifyRocketMaterials_async(results['DesignRocketConfiguration'])

    # Run level 2 nodes in parallel
    results['SpecifyRocketMaterials'] = await run_SpecifyRocketMaterials()

    # Level 3: PlanRocketManufacturingProcess, ConductStructuralAnalysis
    async def run_PlanRocketManufacturingProcess():
        # Call the async version of PlanRocketManufacturingProcess with results from dependencies
        return await PlanRocketManufacturingProcess_async(results['DesignRocketConfiguration'], results['SpecifyRocketMaterials'])

    async def run_ConductStructuralAnalysis():
        # Call the async version of ConductStructuralAnalysis with results from dependencies
        return await ConductStructuralAnalysis_async(results['DesignRocketConfiguration'], results['SpecifyRocketMaterials'])

    # Run level 3 nodes in parallel
    level_3_results = await asyncio.gather(run_PlanRocketManufacturingProcess(), run_ConductStructuralAnalysis())
    results['PlanRocketManufacturingProcess'] = level_3_results[0]
    results['ConductStructuralAnalysis'] = level_3_results[1]

    # Level 4: IntegrateRocketSystems
    async def run_IntegrateRocketSystems():
        # Call the async version of IntegrateRocketSystems with results from dependencies
        return await IntegrateRocketSystems_async(results['PlanRocketManufacturingProcess'], results['ConductStructuralAnalysis'])

    # Run level 4 nodes in parallel
    results['IntegrateRocketSystems'] = await run_IntegrateRocketSystems()

    # Level 5: PerformSystemValidation
    async def run_PerformSystemValidation():
        # Call the async version of PerformSystemValidation with results from dependencies
        return await PerformSystemValidation_async(results['IntegrateRocketSystems'])

    # Run level 5 nodes in parallel
    results['PerformSystemValidation'] = await run_PerformSystemValidation()

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
