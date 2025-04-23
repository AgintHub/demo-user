# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **extract_constraints**: Extract explicit technical or business constraints from the requirements.
2. **identify_core_objective**: Extract the single core objective of the workflow based on provided requirements.
3. **identify_major_risks**: List significant risks or uncertainties associated with the workflow.
4. **extract_key_features**: Generate a list of key functional features required by the workflow. (using output from identify_core_objective)
5. **identify_success_metrics**: List measurable success criteria (quantitative or qualitative) for the workflow. (using output from identify_core_objective)
6. **list_primary_user_roles**: Determine all primary user roles or personas that will interact with the workflow. (using output from identify_core_objective)
7. **generate_feature_descriptions**: Write a concise, one-sentence description for each feature. (using output from extract_key_features)
8. **prioritize_features**: Assign a unique priority ranking to each key feature. (using output from extract_key_features)
9. **compose_prd_summary**: Create a PRD executive summary referencing all prior outputs. (using output from identify_core_objective, list_primary_user_roles, extract_key_features, generate_feature_descriptions)

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
