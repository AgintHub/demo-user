from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_assumptions_and_constraints_output

@CrewBase
class extract_assumptions_and_constraints_crew:
    """Crew for extract_assumptions_and_constraints operations."""


    @agent
    def extract_assumptions_and_constraints_agent(self):
        return Agent(
            role="Extract Assumptions And Constraints Specialist",
            goal="Execute extract_assumptions_and_constraints task accurately",
            backstory="You are a specialized worker focused on Identify explicit assumptions or constraints that limit the products scope.",
            verbose=True
        )



    @task
    def extract_assumptions_and_constraints_task(self):
        """Task for extract_assumptions_and_constraints."""
        agent = self.extract_assumptions_and_constraints_agent()
        return Task(
            description="""Using {extract_product_context_output}, Identify explicit assumptions or constraints that limit the products scope.""",
            agent=agent,
            expected_output="""{
    assumptions: list of strs  # A list of explicit or implied assumptions that underlie the product or feature scope.
    constraints: list of strs  # A list of explicit or implied constraints that limit the scope, implementation, or delivery of the product or feature.
}""",
            output_pydantic=extract_assumptions_and_constraints_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_assumptions_and_constraints_agent()],
            tasks=[self.extract_assumptions_and_constraints_task()],
            verbose=True
        )
