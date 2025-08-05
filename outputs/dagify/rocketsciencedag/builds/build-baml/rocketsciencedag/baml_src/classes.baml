class ConductStructuralAnalysisOutput {
  analysis_summary string @description("Summary of the structural analysis")
  stress_values float[] @description("List of stress values at different points")
  strain_values float[] @description("List of strain values at different points")
  recommendations string[] @description("List of recommendations for improvements or changes")
}

class IdentifyMissionRequirementsOutput {
  type string @description("Type of the mission requirement")
  description string @description("Brief description of the mission requirement")
  details string[] @description("List of specific details for this type of requirement")
  details.values string[] @description("List of specific detail values")
  details.units string[] @description("List of specific detail units")
}

class PerformSystemValidationOutput {
  validation_result bool @description("Whether the system validation was successful")
  test_results string[] @description("Detailed test results")
  recommendations string[] @description("List of recommendations for improvement")
  defects_found int @description("Number of defects found during validation")
}

class PlanRocketManufacturingProcessOutput {
  manufacturing_processes string[] @description("List of manufacturing processes involved")
  production_schedule string[] @description("Schedule of production, potentially including start and end dates for each process")
  resource_allocation string[] @description("List of resources allocated for each process")
  resource_quantities int[] @description("Quantities of each resource allocated")
  critical_path string[] @description("Critical path analysis represented as a list of key tasks")
  is_plan_valid bool @description("Whether the manufacturing plan is valid and feasible")
}

class SpecifyRocketMaterialsOutput {
  materials string[] @description("List of materials for rocket construction (e.g., metals, composites, electronics)")
  material_descriptions string[] @description("Detailed descriptions of each material and its properties")
  selection_reasons string[] @description("Reasons for selecting each material")
}

