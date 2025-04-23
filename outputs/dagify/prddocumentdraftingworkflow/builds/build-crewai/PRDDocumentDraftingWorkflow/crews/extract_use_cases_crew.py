from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_use_cases_output

@CrewBase
class extract_use_cases_crew:
    """Crew for extract_use_cases operations."""


    @agent
    def extract_use_cases_agent(self):
        return Agent(
            role="Extract Use Cases Specialist",
            goal="Execute extract_use_cases task accurately",
            backstory="You are a specialized worker focused on Extract atomic use cases the product or feature must support.",
            verbose=True
        )



    @task
    def extract_use_cases_task(self):
        """Task for extract_use_cases."""
        agent = self.extract_use_cases_agent()
        return Task(
            description="""Using {extract_product_context_output}, Extract atomic use cases the product or feature must support.""",
            agent=agent,
            expected_output="""{
    use_cases: list of strs  # List of atomic, single-actor, goal-driven activities (use cases) that the system must support.
}""",
            output_pydantic=extract_use_cases_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_use_cases_agent()],
            tasks=[self.extract_use_cases_task()],
            verbose=True
        )
