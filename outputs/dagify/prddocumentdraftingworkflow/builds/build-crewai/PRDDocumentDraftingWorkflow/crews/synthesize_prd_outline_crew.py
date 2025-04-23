from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import synthesize_prd_outline_output

@CrewBase
class synthesize_prd_outline_crew:
    """Crew for synthesize_prd_outline operations."""


    @agent
    def synthesize_prd_outline_agent(self):
        return Agent(
            role="Synthesize Prd Outline Specialist",
            goal="Execute synthesize_prd_outline task accurately",
            backstory="You are a specialized worker focused on Compile and structure all PRD sections in the correct order, as a unified outline.",
            verbose=True
        )



    @task
    def synthesize_prd_outline_task(self):
        """Task for synthesize_prd_outline."""
        agent = self.synthesize_prd_outline_agent()
        return Task(
            description="""Using {extract_product_context_output}, {identify_stakeholders_output}, {extract_goals_output}, {extract_assumptions_and_constraints_output}, {extract_use_cases_output}, {derive_functional_requirements_output}, {derive_nonfunctional_requirements_output}, {extract_success_metrics_output}, Compile and structure all PRD sections in the correct order, as a unified outline.""",
            agent=agent,
            expected_output="""{
    prd_product_context: str  # The summarized core product or feature context section of the PRD.
    prd_stakeholders: list of strs  # List of all relevant stakeholders for the product or feature.
    prd_goals: list of strs  # List of primary goals and objectives the product must achieve.
    prd_assumptions_and_constraints: list of strs  # All explicit assumptions and constraints limiting the product's scope.
    prd_use_cases: list of strs  # Atomic use cases or user tasks the system must support.
    prd_functional_requirements: list of strs  # Specific, testable, and distinct functional requirements derived from use cases and goals.
    prd_nonfunctional_requirements: list of strs  # Nonfunctional requirements like performance, security, scalability, or usability.
    prd_success_metrics: list of strs  # Measurable metrics or acceptance criteria for successful delivery or completion.
}""",
            output_pydantic=synthesize_prd_outline_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.synthesize_prd_outline_agent()],
            tasks=[self.synthesize_prd_outline_task()],
            verbose=True
        )
