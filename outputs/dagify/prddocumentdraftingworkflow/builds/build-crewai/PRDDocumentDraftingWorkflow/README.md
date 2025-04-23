# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **extract_product_context**: Extract and summarize the core product or feature context from workflow requirements.
2. **extract_assumptions_and_constraints**: Identify explicit assumptions or constraints that limit the products scope. (using output from extract_product_context)
3. **extract_goals**: Extract and list the primary goals and objectives the product must achieve. (using output from extract_product_context)
4. **extract_use_cases**: Extract atomic use cases the product or feature must support. (using output from extract_product_context)
5. **identify_stakeholders**: Identify and list all relevant stakeholders for the product or feature based on workflow requirements. (using output from extract_product_context)
6. **derive_functional_requirements**: Transform use cases and goals into clear functional requirements. (using output from extract_goals, extract_use_cases)
7. **derive_nonfunctional_requirements**: Identify nonfunctional requirements (e.g., performance, usability) linked to goals and constraints. (using output from extract_goals, extract_assumptions_and_constraints)
8. **extract_success_metrics**: Extract explicit success metrics or acceptance criteria for the product or workflow. (using output from extract_goals)
9. **synthesize_prd_outline**: Compile and structure all PRD sections in the correct order, as a unified outline. (using output from extract_product_context, identify_stakeholders, extract_goals, extract_assumptions_and_constraints, extract_use_cases, derive_functional_requirements, derive_nonfunctional_requirements, extract_success_metrics)

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
