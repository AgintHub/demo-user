from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import determine_technical_constraints_output

@CrewBase
class determine_technical_constraints_crew:
    """Crew for determine_technical_constraints operations."""


    @agent
    def determine_technical_constraints_agent(self):
        return Agent(
            role="Determine Technical Constraints Specialist",
            goal="Execute determine_technical_constraints task accurately",
            backstory="You are a specialized worker focused on Identifies any technical constraints or dependencies specified or implied by the requirements.",
            verbose=True
        )



    @task
    def determine_technical_constraints_task(self):
        """Task for determine_technical_constraints."""
        agent = self.determine_technical_constraints_agent()
        return Task(
            description="""Using {classify_feature_priorities_output}, Identifies any technical constraints or dependencies specified or implied by the requirements.""",
            agent=agent,
            expected_output="""{
    technical_constraints: list of strs  # List of technical constraints or dependencies that must be considered.
}""",
            output_pydantic=determine_technical_constraints_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.determine_technical_constraints_agent()],
            tasks=[self.determine_technical_constraints_task()],
            verbose=True
        )
