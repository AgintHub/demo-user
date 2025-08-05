import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.Choose Power Source import Choose Power Source
from code.Conduct System Checks import Conduct System Checks
from code.Coordinate Final Assembly import Coordinate Final Assembly
from code.Define Rocket Ship Requirements import Define Rocket Ship Requirements
from code.Design Propulsion System import Design Propulsion System
from code.Develop Guidance System import Develop Guidance System
from code.Implement Safety Features import Implement Safety Features
from code.Integrate Propulsion and Guidance Systems import Integrate Propulsion and Guidance Systems

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

Choose Power Source_async = make_async(Choose Power Source)
Conduct System Checks_async = make_async(Conduct System Checks)
Coordinate Final Assembly_async = make_async(Coordinate Final Assembly)
Define Rocket Ship Requirements_async = make_async(Define Rocket Ship Requirements)
Design Propulsion System_async = make_async(Design Propulsion System)
Develop Guidance System_async = make_async(Develop Guidance System)
Implement Safety Features_async = make_async(Implement Safety Features)
Integrate Propulsion and Guidance Systems_async = make_async(Integrate Propulsion and Guidance Systems)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: Define Rocket Ship Requirements
    async def run_Define Rocket Ship Requirements():
        # Call the async version of Define Rocket Ship Requirements with results from dependencies
        return await Define Rocket Ship Requirements_async(user_input)

    # Run level 0 nodes in parallel
    results['Define Rocket Ship Requirements'] = await run_Define Rocket Ship Requirements()

    # Level 1: Develop Guidance System, Choose Power Source, Design Propulsion System
    async def run_Develop Guidance System():
        # Call the async version of Develop Guidance System with results from dependencies
        return await Develop Guidance System_async(results['Define Rocket Ship Requirements'])

    async def run_Choose Power Source():
        # Call the async version of Choose Power Source with results from dependencies
        return await Choose Power Source_async(results['Define Rocket Ship Requirements'])

    async def run_Design Propulsion System():
        # Call the async version of Design Propulsion System with results from dependencies
        return await Design Propulsion System_async(results['Define Rocket Ship Requirements'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_Develop Guidance System(), run_Choose Power Source(), run_Design Propulsion System())
    results['Develop Guidance System'] = level_1_results[0]
    results['Choose Power Source'] = level_1_results[1]
    results['Design Propulsion System'] = level_1_results[2]

    # Level 2: Integrate Propulsion and Guidance Systems, Implement Safety Features
    async def run_Integrate Propulsion and Guidance Systems():
        # Call the async version of Integrate Propulsion and Guidance Systems with results from dependencies
        return await Integrate Propulsion and Guidance Systems_async(results['Design Propulsion System'], results['Develop Guidance System'])

    async def run_Implement Safety Features():
        # Call the async version of Implement Safety Features with results from dependencies
        return await Implement Safety Features_async(results['Choose Power Source'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_Integrate Propulsion and Guidance Systems(), run_Implement Safety Features())
    results['Integrate Propulsion and Guidance Systems'] = level_2_results[0]
    results['Implement Safety Features'] = level_2_results[1]

    # Level 3: Coordinate Final Assembly
    async def run_Coordinate Final Assembly():
        # Call the async version of Coordinate Final Assembly with results from dependencies
        return await Coordinate Final Assembly_async(results['Integrate Propulsion and Guidance Systems'], results['Implement Safety Features'])

    # Run level 3 nodes in parallel
    results['Coordinate Final Assembly'] = await run_Coordinate Final Assembly()

    # Level 4: Conduct System Checks
    async def run_Conduct System Checks():
        # Call the async version of Conduct System Checks with results from dependencies
        return await Conduct System Checks_async(results['Coordinate Final Assembly'])

    # Run level 4 nodes in parallel
    results['Conduct System Checks'] = await run_Conduct System Checks()

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
