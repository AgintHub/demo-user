# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **extract_critical_constraints**: List all technical, business, or regulatory constraints inferred or stated in the workflow requirements.
2. **extract_objectives_from_workflow_requirements**: Extract explicit and implicit project objectives from the provided workflow requirements.
3. **identify_primary_user_roles**: Extract the main user roles or personas directly involved with the product based on the requirements.
4. **summarize_key_stakeholders**: Identify and summarize the interest and influence of key project stakeholders.
5. **define_success_metrics**: Articulate measurable criteria for determining product success based on extracted objectives. (using output from extract_objectives_from_workflow_requirements)
6. **draft_prd_section_constraints**: Format the extracted constraints into a Constraints section for the PRD. (using output from extract_critical_constraints)
7. **draft_prd_section_objectives**: Format the extracted objectives as the Objectives section for the PRD. (using output from extract_objectives_from_workflow_requirements)
8. **draft_prd_section_stakeholders**: Format the stakeholder summaries into a PRD Stakeholders section. (using output from summarize_key_stakeholders)
9. **draft_prd_section_user_roles**: Format the identified user roles as the User Roles & Personas section for the PRD. (using output from identify_primary_user_roles)
10. **extract_core_product_features**: Identify and list all core product features needed to satisfy the workflow requirements. (using output from extract_objectives_from_workflow_requirements)
11. **define_user_journeys_for_each_role**: For each identified user role, provide a concise narrative of the main user journey(s) within the workflow. (using output from identify_primary_user_roles, extract_core_product_features)
12. **draft_prd_section_features**: Compile the core features into the PRD Features section. (using output from extract_core_product_features)
13. **draft_prd_section_success_metrics**: Draft the Success Metrics section for the PRD using the defined metrics. (using output from define_success_metrics)
14. **draft_prd_section_user_journeys**: Organize the user journeys as a distinct User Journeys section in the PRD. (using output from define_user_journeys_for_each_role)
15. **compile_final_prd_document**: Combine all previously drafted sections into a single coherent PRD document, maintaining logical order and structure. (using output from draft_prd_section_objectives, draft_prd_section_user_roles, draft_prd_section_features, draft_prd_section_constraints, draft_prd_section_success_metrics, draft_prd_section_stakeholders, draft_prd_section_user_journeys)

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
