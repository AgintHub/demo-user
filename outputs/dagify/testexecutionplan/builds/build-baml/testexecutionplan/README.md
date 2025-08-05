# TestExecutionPlan - BAML Workflow

This is an AI-powered workflow using BAML (Boundary ML) to accomplish complex tasks through LLM function calling.

## Environment Setup

**IMPORTANT**: Before running this workflow, you must set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY='your-api-key'
```

This environment variable is required for the workflow to make API calls to OpenAI. Make sure to set it before running either the setup script or any manual steps below.

## Workflow Steps

1. **determine_test_objective**: Identify the specific goal of the 'test' being executed
2. **test_data_gathering**: Collect all necessary inputs to execute the test with desired outcomes (using output from determine_test_objective)
3. **formulate_test_conditions**: Create a set of scenarios or conditions to test the 'test' outcome (using output from determine_test_objective, test_data_gathering)
4. **evaluate_test_outcomes**: Run the test scenarios and assess the results based on the desired outcomes (using output from formulate_test_conditions, test_data_gathering)
5. **report_test_results**: Summarize the test outcome and provide any relevant findings or insights. (using output from evaluate_test_outcomes)

## Running the Workflow

This workflow is self-contained and requires minimal setup:

1. Run the setup script which will create a virtual environment and install dependencies:
```bash
./run.sh
```

2. Or follow these manual steps:
   * Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

   * Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   * Generate BAML client code:
   ```bash
   baml-cli generate
   ```

   * Run the workflow:
   ```bash
   python main.py
   ```

## Input/Output

- The workflow accepts input as either plain text or JSON
- Each BAML function processes its input and produces structured output
- Results from all steps are collected in the final output
