# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **extract_workflow_overview**: Summarize the main purpose and objectives of the workflow from the requirements.
2. **define_stakeholder_roles**: Identify and list all distinct user or stakeholder roles relevant to the workflow. (using output from extract_workflow_overview)
3. **identify_core_features**: List the fundamental features explicitly or implicitly required for the workflow. (using output from extract_workflow_overview)
4. **identify_project_constraints**: Identify explicit or implicit project constraints (technical, time, regulatory, etc.) in the requirements. (using output from extract_workflow_overview)
5. **assess_major_risks**: Enumerate key risks that may impact successful workflow implementation. (using output from extract_workflow_overview, identify_project_constraints)
6. **assign_feature_priorities**: Assign a relative priority to each core feature based on its necessity and impact. (using output from identify_core_features)
7. **formulate_user_stories**: Write user stories for each core feature from the perspective of each appropriate stakeholder. (using output from identify_core_features, define_stakeholder_roles)
8. **extract_acceptance_criteria**: For each user story, specify clear, testable acceptance criteria. (using output from formulate_user_stories)

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
