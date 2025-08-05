class Analyze_resultsOutput {
  identified_areas string[] @description("List of identified areas for improvement")
  key_performance_indicators string[] @description("List of key performance indicators")
  potential_improvements string @description("Suggested potential improvements for future experiments")
}

class Define_test_parametersOutput {
  rocket_type string @description("The type or model of the rocket used in the test")
  payload_weight_kg float @description("The weight of the payload in kilograms")
  test_conditions string[] @description("List of test condition descriptors, e.g., weather, wind, ambient temperature")
}

class Document_experiment_reportOutput {
  experiment_summary string @description("Summary of the experiment results")
  suggested_improvements string @description("Potential improvements for future experiments")
  outcomes string[] @description("List of key performance indicators")
}

class Fetch_test_parametersOutput {
  rocket_type string @description("Type of the rocket used in the experiment")
  payload string @description("Description or category of the payload")
  test_conditions string[] @description("List of key test condition parameters such as temperature, pressure, and environment")
}

class Simulate_experimentOutput {
  rocket_trajectory string @description("Rocket trajectory results")
  velocity_results float[] @description("List of velocity results")
  safety_margins float @description("Safety margins results")
  simulation_errors string[] @description("List of simulation errors")
  is_simulation_valid bool @description("Whether the simulation is valid")
}

class Verify_test_conditionsOutput {
  test_conditions string @description("Statement indicating whether the test conditions meet the specified requirements")
  discrepancies_found string[] @description("List of discrepancies found between the test conditions and the experiment design and stated objectives")
  valid_test_conditions bool @description("Whether the test conditions are valid according to the experiment requirements")
}

