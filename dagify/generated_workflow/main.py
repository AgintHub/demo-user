import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.assemble_space_ship_components import assemble_space_ship_components
from code.calculate_space_ship_size import calculate_space_ship_size
from code.define_space_ship_purpose import define_space_ship_purpose
from code.design_life_support_systems import design_life_support_systems
from code.select_propulsion_system import select_propulsion_system

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

assemble_space_ship_components_async = make_async(assemble_space_ship_components)
calculate_space_ship_size_async = make_async(calculate_space_ship_size)
define_space_ship_purpose_async = make_async(define_space_ship_purpose)
design_life_support_systems_async = make_async(design_life_support_systems)
select_propulsion_system_async = make_async(select_propulsion_system)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_space_ship_purpose
    async def run_define_space_ship_purpose():
        # Call the async version of define_space_ship_purpose with results from dependencies
        return await define_space_ship_purpose_async(user_input)

    # Run level 0 nodes in parallel
    results['define_space_ship_purpose'] = await run_define_space_ship_purpose()

    # Level 1: calculate_space_ship_size
    async def run_calculate_space_ship_size():
        # Call the async version of calculate_space_ship_size with results from dependencies
        return await calculate_space_ship_size_async(results['define_space_ship_purpose'])

    # Run level 1 nodes in parallel
    results['calculate_space_ship_size'] = await run_calculate_space_ship_size()

    # Level 2: select_propulsion_system, design_life_support_systems
    async def run_select_propulsion_system():
        # Call the async version of select_propulsion_system with results from dependencies
        return await select_propulsion_system_async(results['calculate_space_ship_size'])

    async def run_design_life_support_systems():
        # Call the async version of design_life_support_systems with results from dependencies
        return await design_life_support_systems_async(results['calculate_space_ship_size'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_select_propulsion_system(), run_design_life_support_systems())
    results['select_propulsion_system'] = level_2_results[0]
    results['design_life_support_systems'] = level_2_results[1]

    # Level 3: assemble_space_ship_components
    async def run_assemble_space_ship_components():
        # Call the async version of assemble_space_ship_components with results from dependencies
        return await assemble_space_ship_components_async(results['select_propulsion_system'], results['design_life_support_systems'])

    # Run level 3 nodes in parallel
    results['assemble_space_ship_components'] = await run_assemble_space_ship_components()

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
