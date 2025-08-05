# HedgeFundCreationPlan - BAML Workflow

This is an AI-powered workflow using BAML (Boundary ML) to accomplish complex tasks through LLM function calling.

## Environment Setup

**IMPORTANT**: Before running this workflow, you must set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY='your-api-key'
```

This environment variable is required for the workflow to make API calls to OpenAI. Make sure to set it before running either the setup script or any manual steps below.

## Workflow Steps

1. **define_hedge_fund_strategy**: Define a specific investment strategy for the hedge fund
2. **establish_fund_constitution**: Create the organizational documents and agreements for the hedge fund
3. **select_ Investment_vessels**: Determine the types of assets the hedge fund will invest in (using output from define_hedge_fund_strategy)
4. **set_up_trading_operations**: Configure trading platforms, accounts, and other essential systems (using output from establish_fund_constitution)
5. **hire_key_fund_professionals**: Recruit and onboard core fund team members (using output from set_up_trading_operations)
6. **develop_operating_manual**: Document the fund's policies, procedures, and risk management framework (using output from hire_key_fund_professionals)
7. **register_hedge_fund**: Obtain necessary registrations and licenses for the hedge fund (using output from develop_operating_manual)

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
