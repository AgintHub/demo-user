function Process_define_hedge_fund_strategy(input_payload: string) -> string {
  client DefaultOpenAI
  prompt #"
    Define a specific investment strategy for the hedge fund

    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_develop_operating_manual(hire_key_fund_professionals_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Document the fund's policies, procedures, and risk management framework

    Input:
    {{ hire_key_fund_professionals_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_establish_fund_constitution(input_payload: string) -> string {
  client DefaultOpenAI
  prompt #"
    Create the organizational documents and agreements for the hedge fund

    Input:
    {{ input_payload }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_hire_key_fund_professionals(set_up_trading_operations_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Recruit and onboard core fund team members

    Input:
    {{ set_up_trading_operations_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_register_hedge_fund(develop_operating_manual_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Obtain necessary registrations and licenses for the hedge fund

    Input:
    {{ develop_operating_manual_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_select__Investment_vessels(define_hedge_fund_strategy_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Determine the types of assets the hedge fund will invest in

    Input:
    {{ define_hedge_fund_strategy_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}

function Process_set_up_trading_operations(establish_fund_constitution_output: string) -> string {
  client DefaultOpenAI
  prompt #"
    Configure trading platforms, accounts, and other essential systems

    Input:
    {{ establish_fund_constitution_output }}

    Output Format:
    {{ ctx.output_format }} // Escaped curly braces for Jinja context
  "#
}
