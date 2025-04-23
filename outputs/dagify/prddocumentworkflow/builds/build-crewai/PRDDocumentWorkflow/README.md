# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **extract_product_name**: Extracts the product or feature name from the user prompt.
2. **determine_target_users**: Identifies the primary intended users or user segments for the product. (using output from extract_product_name)
3. **extract_primary_objective**: Identifies the main objective or goal of the product as described by the user. (using output from extract_product_name)
4. **identify_user_problems**: Lists specific user problems or pain points that the product will address. (using output from extract_product_name, determine_target_users)
5. **extract_user_stories**: Drafts elemental user stories to capture desired end-user behaviors. (using output from identify_user_problems)
6. **extract_feature_requirements**: Extracts the elemental feature requirements from user stories. (using output from extract_user_stories)
7. **classify_feature_priorities**: Classifies each feature requirement as must-have or nice-to-have. (using output from extract_feature_requirements)
8. **determine_technical_constraints**: Identifies any technical constraints or dependencies specified or implied by the requirements. (using output from classify_feature_priorities)
9. **extract_success_metrics**: Extracts measurable success criteria or key performance indicators for the product. (using output from extract_primary_objective, determine_technical_constraints)
10. **summarize_prd_document**: Produces a coherent, structured PRD summary from all extracted and organized data. (using output from extract_product_name, extract_primary_objective, determine_target_users, identify_user_problems, extract_user_stories, extract_feature_requirements, classify_feature_priorities, determine_technical_constraints, extract_success_metrics)

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
