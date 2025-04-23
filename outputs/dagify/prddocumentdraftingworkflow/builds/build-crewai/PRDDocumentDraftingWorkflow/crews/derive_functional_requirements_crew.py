from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import derive_functional_requirements_output

@CrewBase
class derive_functional_requirements_crew:
    """Crew for derive_functional_requirements operations."""


    @agent
    def derive_functional_requirements_agent(self):
        return Agent(
            role="Derive Functional Requirements Specialist",
            goal="Execute derive_functional_requirements task accurately",
            backstory="You are a specialized worker focused on Transform use cases and goals into clear functional requirements.",
            verbose=True
        )



    @task
    def derive_functional_requirements_task(self):
        """Task for derive_functional_requirements."""
        agent = self.derive_functional_requirements_agent()
        return Task(
            description="""Using {extract_goals_output}, {extract_use_cases_output}, Transform use cases and goals into clear functional requirements.""",
            agent=agent,
            expected_output="""{
    functional_requirements: list of strs  # List of distinct, testable functional requirements derived from use cases and goals. Each string is a single requirement describing a necessary system behavior.
}""",
            output_pydantic=derive_functional_requirements_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.derive_functional_requirements_agent()],
            tasks=[self.derive_functional_requirements_task()],
            verbose=True
        )
