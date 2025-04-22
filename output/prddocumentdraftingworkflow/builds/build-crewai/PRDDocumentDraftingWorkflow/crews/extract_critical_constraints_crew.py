from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_critical_constraints_output

@CrewBase
class extract_critical_constraints_crew:
    """Crew for extract_critical_constraints operations."""


    @agent
    def extract_critical_constraints_agent(self):
        return Agent(
            role="Extract Critical Constraints Specialist",
            goal="""Execute extract_critical_constraints task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on List all technical, business, or regulatory constraints inferred or stated in the workflow requirements.",
            verbose=True
        )



    @task
    def extract_critical_constraints_task(self):
        """Task for extract_critical_constraints."""
        agent = self.extract_critical_constraints_agent()
        return Task(
            description="""Using {input}, List all technical, business, or regulatory constraints inferred or stated in the workflow requirements.""",
            agent=agent,
            expected_output="""{
    constraints: list of strs  # Individual statements of technical, business, regulatory, or design constraints relevant to the product requirements.
}""",
            output_pydantic=extract_critical_constraints_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_critical_constraints_agent()],
            tasks=[self.extract_critical_constraints_task()],
            verbose=True
        )
