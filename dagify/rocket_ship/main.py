import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.define_rocket_ship import define_rocket_ship
from code.document_rocket_ship_functions import document_rocket_ship_functions
from code.list_rocket_ship_components import list_rocket_ship_components
from code.research_rocket_ship_materials import research_rocket_ship_materials
from code.summarize_rocket_ship_information import summarize_rocket_ship_information

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

define_rocket_ship_async = make_async(define_rocket_ship)
document_rocket_ship_functions_async = make_async(document_rocket_ship_functions)
list_rocket_ship_components_async = make_async(list_rocket_ship_components)
research_rocket_ship_materials_async = make_async(research_rocket_ship_materials)
summarize_rocket_ship_information_async = make_async(summarize_rocket_ship_information)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_rocket_ship
    async def run_define_rocket_ship():
        # Call the async version of define_rocket_ship with results from dependencies
        return await define_rocket_ship_async(user_input)

    # Run level 0 nodes in parallel
    results['define_rocket_ship'] = await run_define_rocket_ship()

    # Level 1: document_rocket_ship_functions, research_rocket_ship_materials, list_rocket_ship_components
    async def run_document_rocket_ship_functions():
        # Call the async version of document_rocket_ship_functions with results from dependencies
        return await document_rocket_ship_functions_async(results['define_rocket_ship'])

    async def run_research_rocket_ship_materials():
        # Call the async version of research_rocket_ship_materials with results from dependencies
        return await research_rocket_ship_materials_async(results['define_rocket_ship'])

    async def run_list_rocket_ship_components():
        # Call the async version of list_rocket_ship_components with results from dependencies
        return await list_rocket_ship_components_async(results['define_rocket_ship'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_document_rocket_ship_functions(), run_research_rocket_ship_materials(), run_list_rocket_ship_components())
    results['document_rocket_ship_functions'] = level_1_results[0]
    results['research_rocket_ship_materials'] = level_1_results[1]
    results['list_rocket_ship_components'] = level_1_results[2]

    # Level 2: summarize_rocket_ship_information
    async def run_summarize_rocket_ship_information():
        # Call the async version of summarize_rocket_ship_information with results from dependencies
        return await summarize_rocket_ship_information_async(results['list_rocket_ship_components'], results['research_rocket_ship_materials'], results['document_rocket_ship_functions'])

    # Run level 2 nodes in parallel
    results['summarize_rocket_ship_information'] = await run_summarize_rocket_ship_information()

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
