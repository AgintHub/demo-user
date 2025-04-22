# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **get_testing_environment**: Get the testing environment details
2. **select_test_cases**: Select the relevant test cases (using output from get_testing_environment)
3. **perform_test_cases**: Perform the selected test cases (using output from select_test_cases)
4. **analyze_test_results**: Analyze the test results (using output from perform_test_cases)
5. **document_test_results**: Document the test results (using output from analyze_test_results)

## Running the Workflow

This workflow is self-contained and requires minimal setup:

1. Install uv if you haven't already:
```bash
pip install uv
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

3. Run the workflow:
```bash
./run.sh
```

That's it! The workflow will automatically handle all dependencies and execution.

## Input/Output

- The workflow accepts input as either plain text or JSON
- Each agent processes its input and produces structured output
- Final results are displayed for each step of the workflow
