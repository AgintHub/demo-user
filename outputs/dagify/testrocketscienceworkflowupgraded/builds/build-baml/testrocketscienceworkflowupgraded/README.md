# TestRocketScienceWorkflowUpgraded - BAML Workflow

This is an AI-powered workflow using BAML (Boundary ML) to accomplish complex tasks through LLM function calling.

## Environment Setup

**IMPORTANT**: Before running this workflow, you must set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY='your-api-key'
```

This environment variable is required for the workflow to make API calls to OpenAI. Make sure to set it before running either the setup script or any manual steps below.

## Workflow Steps

1. **define_test_parameters**: Identify the test parameters for the rocket science experiment
2. **fetch_test_parameters**: Fetch the test parameters for the rocket science experiment
3. **verify_test_conditions**: Verify that the test conditions meet the specified requirements (using output from fetch_test_parameters)
4. **simulate_experiment**: Simulate the rocket science experiment using the specified parameters and conditions (using output from verify_test_conditions)
5. **analyze_results**: Analyze the results of the simulation and identify areas for improvement (using output from simulate_experiment)
6. **document_experiment_report**: Create a comprehensive report summarizing the experiment results (using output from analyze_results)

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
