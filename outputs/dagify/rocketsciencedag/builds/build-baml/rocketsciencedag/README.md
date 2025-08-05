# RocketScienceDAG - BAML Workflow

This is an AI-powered workflow using BAML (Boundary ML) to accomplish complex tasks through LLM function calling.

## Environment Setup

**IMPORTANT**: Before running this workflow, you must set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY='your-api-key'
```

This environment variable is required for the workflow to make API calls to OpenAI. Make sure to set it before running either the setup script or any manual steps below.

## Workflow Steps

1. **IdentifyMissionRequirements**: Identify the fundamental mission requirements
2. **DesignRocketConfiguration**: Design the rocket configuration based on mission requirements (using output from IdentifyMissionRequirements)
3. **SpecifyRocketMaterials**: Specify the materials for rocket construction (using output from DesignRocketConfiguration)
4. **ConductStructuralAnalysis**: Conduct a structural analysis of the rocket (using output from DesignRocketConfiguration, SpecifyRocketMaterials)
5. **PlanRocketManufacturingProcess**: Plan the rocket manufacturing process (using output from DesignRocketConfiguration, SpecifyRocketMaterials)
6. **IntegrateRocketSystems**: Integrate the rocket systems (using output from PlanRocketManufacturingProcess, ConductStructuralAnalysis)
7. **PerformSystemValidation**: Validate the system operation (using output from IntegrateRocketSystems)

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
