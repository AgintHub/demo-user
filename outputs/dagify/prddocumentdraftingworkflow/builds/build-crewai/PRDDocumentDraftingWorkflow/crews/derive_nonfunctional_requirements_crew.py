from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import derive_nonfunctional_requirements_output

@CrewBase
class derive_nonfunctional_requirements_crew:
    """Crew for derive_nonfunctional_requirements operations."""


    @agent
    def derive_nonfunctional_requirements_agent(self):
        return Agent(
            role="Derive Nonfunctional Requirements Specialist",
            goal="Execute derive_nonfunctional_requirements task accurately",
            backstory="You are a specialized worker focused on Identify nonfunctional requirements (e.g., performance, usability) linked to goals and constraints.",
            verbose=True
        )



    @task
    def derive_nonfunctional_requirements_task(self):
        """Task for derive_nonfunctional_requirements."""
        agent = self.derive_nonfunctional_requirements_agent()
        return Task(
            description="""Using {extract_goals_output}, {extract_assumptions_and_constraints_output}, Identify nonfunctional requirements (e.g., performance, usability) linked to goals and constraints.""",
            agent=agent,
            expected_output="""{
    nonfunctional_requirements: list of strs  # List of distinct, specific, and measurable nonfunctional requirements derived from the product goals and constraints. Each entry should describe a single nonfunctional requirement (e.g., performance targets, scalability needs, security standards, usability requirements).
}""",
            output_pydantic=derive_nonfunctional_requirements_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.derive_nonfunctional_requirements_agent()],
            tasks=[self.derive_nonfunctional_requirements_task()],
            verbose=True
        )
