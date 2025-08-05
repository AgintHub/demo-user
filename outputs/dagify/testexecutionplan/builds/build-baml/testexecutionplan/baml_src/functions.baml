function Process_determine_test_objective(input_payload: string) -> Determine_test_objective_output {
  client DefaultOpenAI
  prompt #"
    Identify the specific goal of the 'test' being executed
    Expected output:
    - test_objective: Specific objective of the test
    - desired_outcome: Desired outcome of the test


    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_evaluate_test_outcomes(formulate_test_conditions_output: Formulate_test_conditions_output, test_data_gathering_output: Test_data_gathering_output) -> Evaluate_test_outcomes_output {
  client DefaultOpenAI
  prompt #"
    Run the test scenarios and assess the results based on the desired outcomes
    Expected output:
    - test_success: Indicates whether the test passed successfully based on evaluation
    - test_feedback: List of strings summarizing the evaluation outcomes, issues, or insights
    - evaluated_results: List of key results or metrics obtained from test assessment


    Input:
    {{ formulate_test_conditions_output }}
    {{ test_data_gathering_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_formulate_test_conditions(determine_test_objective_output: Determine_test_objective_output, test_data_gathering_output: Test_data_gathering_output) -> Formulate_test_conditions_output {
  client DefaultOpenAI
  prompt #"
    Create a set of scenarios or conditions to test the 'test' outcome
    Expected output:
    - test_conditions_list: A list of scenario descriptions or test conditions developed based on the test objective and data gathering.
    - number_of_conditions: The total number of test conditions created.
    - has_valid_conditions: Indicates whether at least one valid test condition has been created.


    Input:
    {{ determine_test_objective_output }}
    {{ test_data_gathering_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_report_test_results(evaluate_test_outcomes_output: Evaluate_test_outcomes_output) -> Report_test_results_output {
  client DefaultOpenAI
  prompt #"
    Summarize the test outcome and provide any relevant findings or insights.
    Expected output:
    - test_outcome: Summary of the test outcome.
    - findings_or_insights: Any relevant findings or insights from the test results.
    - further_action_required: Whether further action is required due to the test results.


    Input:
    {{ evaluate_test_outcomes_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}

function Process_test_data_gathering(determine_test_objective_output: Determine_test_objective_output) -> Test_data_gathering_output {
  client DefaultOpenAI
  prompt #"
    Collect all necessary inputs to execute the test with desired outcomes
    Expected output:
    - test_data: Input data for the test
    - test_conditions: Conditions or scenarios for the test
    - is_valid: Whether the data is valid


    Input:
    {{ determine_test_objective_output }}

    Output Format:
    {{ ctx.output_format }}
  "#
}
