from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_constraints_output

@CrewBase
class extract_constraints_crew:
    """Crew for extract_constraints operations."""


    @agent
    def extract_constraints_agent(self):
        return Agent(
            role="Extract Constraints Specialist",
            goal="Execute extract_constraints task accurately",
            backstory="You are a specialized worker focused on Extract explicit technical or business constraints from the requirements.",
            verbose=True
        )



    @task
    def extract_constraints_task(self):
        """Task for extract_constraints."""
        agent = self.extract_constraints_agent()
        return Task(
            description="""Using {input}, Extract explicit technical or business constraints from the requirements.""",
            agent=agent,
            expected_output="""{
    constraints: list of strs  # List of explicit technical or business constraints applicable to the workflow.
}""",
            output_pydantic=extract_constraints_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_constraints_agent()],
            tasks=[self.extract_constraints_task()],
            verbose=True
        )
