import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_test_output import analyze_test_output
from code.execute_test_script import execute_test_script
from code.extract_test_input import extract_test_input
from code.validate_test_input import validate_test_input

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

analyze_test_output_async = make_async(analyze_test_output)
execute_test_script_async = make_async(execute_test_script)
extract_test_input_async = make_async(extract_test_input)
validate_test_input_async = make_async(validate_test_input)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: extract_test_input
    async def run_extract_test_input():
        # Call the async version of extract_test_input with results from dependencies
        return await extract_test_input_async(user_input)

    # Run level 0 nodes in parallel
    results['extract_test_input'] = await run_extract_test_input()

    # Level 1: validate_test_input
    async def run_validate_test_input():
        # Call the async version of validate_test_input with results from dependencies
        return await validate_test_input_async(results['extract_test_input'])

    # Run level 1 nodes in parallel
    results['validate_test_input'] = await run_validate_test_input()

    # Level 2: execute_test_script
    async def run_execute_test_script():
        # Call the async version of execute_test_script with results from dependencies
        return await execute_test_script_async(results['extract_test_input'], results['validate_test_input'])

    # Run level 2 nodes in parallel
    results['execute_test_script'] = await run_execute_test_script()

    # Level 3: analyze_test_output
    async def run_analyze_test_output():
        # Call the async version of analyze_test_output with results from dependencies
        return await analyze_test_output_async(results['execute_test_script'])

    # Run level 3 nodes in parallel
    results['analyze_test_output'] = await run_analyze_test_output()

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
