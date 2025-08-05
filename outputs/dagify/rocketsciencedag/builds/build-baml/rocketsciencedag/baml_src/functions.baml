function Process_ConductStructuralAnalysis(DesignRocketConfiguration_output: string, SpecifyRocketMaterials_output: SpecifyRocketMaterialsOutput) -> ConductStructuralAnalysisOutput {
  client DefaultOpenAI
  prompt #"
    Conduct a structural analysis of the rocket
    Expected output structure:
    - analysis_summary: Summary of the structural analysis
    - stress_values: List of stress values at different points
    - strain_values: List of strain values at different points
    - recommendations: List of recommendations for improvements or changes


    Input:
    {{ DesignRocketConfiguration_output }
{ SpecifyRocketMaterials_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_DesignRocketConfiguration(IdentifyMissionRequirements_output: IdentifyMissionRequirementsOutput) -> string {
  client DefaultOpenAI
  prompt #"
    Design the rocket configuration based on mission requirements

    Input:
    {{ IdentifyMissionRequirements_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_IdentifyMissionRequirements(input_payload: string) -> IdentifyMissionRequirementsOutput {
  client DefaultOpenAI
  prompt #"
    Identify the fundamental mission requirements
    Expected output structure:
    - type: Type of the mission requirement
    - description: Brief description of the mission requirement
    - details: List of specific details for this type of requirement
    - details.values: List of specific detail values
    - details.units: List of specific detail units


    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_IntegrateRocketSystems(PlanRocketManufacturingProcess_output: PlanRocketManufacturingProcessOutput, ConductStructuralAnalysis_output: ConductStructuralAnalysisOutput) -> string {
  client DefaultOpenAI
  prompt #"
    Integrate the rocket systems

    Input:
    {{ PlanRocketManufacturingProcess_output }
{ ConductStructuralAnalysis_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_PerformSystemValidation(IntegrateRocketSystems_output: string) -> PerformSystemValidationOutput {
  client DefaultOpenAI
  prompt #"
    Validate the system operation
    Expected output structure:
    - validation_result: Whether the system validation was successful
    - test_results: Detailed test results
    - recommendations: List of recommendations for improvement
    - defects_found: Number of defects found during validation


    Input:
    {{ IntegrateRocketSystems_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_PlanRocketManufacturingProcess(DesignRocketConfiguration_output: string, SpecifyRocketMaterials_output: SpecifyRocketMaterialsOutput) -> PlanRocketManufacturingProcessOutput {
  client DefaultOpenAI
  prompt #"
    Plan the rocket manufacturing process
    Expected output structure:
    - manufacturing_processes: List of manufacturing processes involved
    - production_schedule: Schedule of production, potentially including start and end dates for each process
    - resource_allocation: List of resources allocated for each process
    - resource_quantities: Quantities of each resource allocated
    - critical_path: Critical path analysis represented as a list of key tasks
    - is_plan_valid: Whether the manufacturing plan is valid and feasible


    Input:
    {{ DesignRocketConfiguration_output }
{ SpecifyRocketMaterials_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_SpecifyRocketMaterials(DesignRocketConfiguration_output: string) -> SpecifyRocketMaterialsOutput {
  client DefaultOpenAI
  prompt #"
    Specify the materials for rocket construction
    Expected output structure:
    - materials: List of materials for rocket construction (e.g., metals, composites, electronics)
    - material_descriptions: Detailed descriptions of each material and its properties
    - selection_reasons: Reasons for selecting each material


    Input:
    {{ DesignRocketConfiguration_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}
