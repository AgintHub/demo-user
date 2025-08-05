class Determine_test_objective_output {
  test_objective string @description("Specific objective of the test")
  desired_outcome string @description("Desired outcome of the test")
}

class Evaluate_test_outcomes_output {
  test_success bool @description("Indicates whether the test passed successfully based on evaluation")
  test_feedback string[] @description("List of strings summarizing the evaluation outcomes, issues, or insights")
  evaluated_results string[] @description("List of key results or metrics obtained from test assessment")
}

class Formulate_test_conditions_output {
  test_conditions_list string[] @description("A list of scenario descriptions or test conditions developed based on the test objective and data gathering.")
  number_of_conditions int @description("The total number of test conditions created.")
  has_valid_conditions bool @description("Indicates whether at least one valid test condition has been created.")
}

class Report_test_results_output {
  test_outcome string @description("Summary of the test outcome.")
  findings_or_insights string @description("Any relevant findings or insights from the test results.")
  further_action_required bool @description("Whether further action is required due to the test results.")
}

class Test_data_gathering_output {
  test_data string @description("Input data for the test")
  test_conditions string[] @description("Conditions or scenarios for the test")
  is_valid bool @description("Whether the data is valid")
}

