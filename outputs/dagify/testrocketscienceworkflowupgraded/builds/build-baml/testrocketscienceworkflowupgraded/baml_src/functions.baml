function Process_analyze_results(simulate_experiment_output: Simulate_experimentOutput) -> Analyze_resultsOutput {
  client DefaultOpenAI
  prompt #"
    Analyze the results of the simulation and identify areas for improvement
    Expected output:
    - identified_areas: List of identified areas for improvement
    - key_performance_indicators: List of key performance indicators
    - potential_improvements: Suggested potential improvements for future experiments


    Input:
    {{ simulate_experiment_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_define_test_parameters(input_payload: string) -> Define_test_parametersOutput {
  client DefaultOpenAI
  prompt #"
    Identify the test parameters for the rocket science experiment
    Expected output:
    - rocket_type: The type or model of the rocket used in the test
    - payload_weight_kg: The weight of the payload in kilograms
    - test_conditions: List of test condition descriptors, e.g., weather, wind, ambient temperature


    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_document_experiment_report(analyze_results_output: Analyze_resultsOutput) -> Document_experiment_reportOutput {
  client DefaultOpenAI
  prompt #"
    Create a comprehensive report summarizing the experiment results
    Expected output:
    - experiment_summary: Summary of the experiment results
    - suggested_improvements: Potential improvements for future experiments
    - outcomes: List of key performance indicators


    Input:
    {{ analyze_results_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_fetch_test_parameters(input_payload: string) -> Fetch_test_parametersOutput {
  client DefaultOpenAI
  prompt #"
    Fetch the test parameters for the rocket science experiment
    Expected output:
    - rocket_type: Type of the rocket used in the experiment
    - payload: Description or category of the payload
    - test_conditions: List of key test condition parameters such as temperature, pressure, and environment


    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_simulate_experiment(verify_test_conditions_output: Verify_test_conditionsOutput) -> Simulate_experimentOutput {
  client DefaultOpenAI
  prompt #"
    Simulate the rocket science experiment using the specified parameters and conditions
    Expected output:
    - rocket_trajectory: Rocket trajectory results
    - velocity_results: List of velocity results
    - safety_margins: Safety margins results
    - simulation_errors: List of simulation errors
    - is_simulation_valid: Whether the simulation is valid


    Input:
    {{ verify_test_conditions_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_verify_test_conditions(fetch_test_parameters_output: Fetch_test_parametersOutput) -> Verify_test_conditionsOutput {
  client DefaultOpenAI
  prompt #"
    Verify that the test conditions meet the specified requirements
    Expected output:
    - test_conditions: Statement indicating whether the test conditions meet the specified requirements
    - discrepancies_found: List of discrepancies found between the test conditions and the experiment design and stated objectives
    - valid_test_conditions: Whether the test conditions are valid according to the experiment requirements


    Input:
    {{ fetch_test_parameters_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}
