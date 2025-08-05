import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.decomposition_request import decomposition_request
from code.deterministic_executable_code_generation import deterministic_executable_code_generation
from code.elemental_step_extraction import elemental_step_extraction
from code.execution_validation_and_verification import execution_validation_and_verification
from code.task_description_extraction import task_description_extraction
from code.task_specification_check import task_specification_check

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

decomposition_request_async = make_async(decomposition_request)
deterministic_executable_code_generation_async = make_async(deterministic_executable_code_generation)
elemental_step_extraction_async = make_async(elemental_step_extraction)
execution_validation_and_verification_async = make_async(execution_validation_and_verification)
task_description_extraction_async = make_async(task_description_extraction)
task_specification_check_async = make_async(task_specification_check)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: task_specification_check
    async def run_task_specification_check():
        # Call the async version of task_specification_check with results from dependencies
        return await task_specification_check_async(user_input)

    # Run level 0 nodes in parallel
    results['task_specification_check'] = await run_task_specification_check()

    # Level 1: task_description_extraction
    async def run_task_description_extraction():
        # Call the async version of task_description_extraction with results from dependencies
        return await task_description_extraction_async(results['task_specification_check'])

    # Run level 1 nodes in parallel
    results['task_description_extraction'] = await run_task_description_extraction()

    # Level 2: decomposition_request
    async def run_decomposition_request():
        # Call the async version of decomposition_request with results from dependencies
        return await decomposition_request_async(results['task_description_extraction'])

    # Run level 2 nodes in parallel
    results['decomposition_request'] = await run_decomposition_request()

    # Level 3: elemental_step_extraction
    async def run_elemental_step_extraction():
        # Call the async version of elemental_step_extraction with results from dependencies
        return await elemental_step_extraction_async(results['decomposition_request'])

    # Run level 3 nodes in parallel
    results['elemental_step_extraction'] = await run_elemental_step_extraction()

    # Level 4: deterministic_executable_code_generation
    async def run_deterministic_executable_code_generation():
        # Call the async version of deterministic_executable_code_generation with results from dependencies
        return await deterministic_executable_code_generation_async(results['elemental_step_extraction'])

    # Run level 4 nodes in parallel
    results['deterministic_executable_code_generation'] = await run_deterministic_executable_code_generation()

    # Level 5: execution_validation_and_verification
    async def run_execution_validation_and_verification():
        # Call the async version of execution_validation_and_verification with results from dependencies
        return await execution_validation_and_verification_async(results['deterministic_executable_code_generation'])

    # Run level 5 nodes in parallel
    results['execution_validation_and_verification'] = await run_execution_validation_and_verification()

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
