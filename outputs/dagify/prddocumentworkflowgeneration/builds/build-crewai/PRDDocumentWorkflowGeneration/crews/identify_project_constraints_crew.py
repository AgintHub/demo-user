from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_project_constraints_output

@CrewBase
class identify_project_constraints_crew:
    """Crew for identify_project_constraints operations."""


    @agent
    def identify_project_constraints_agent(self):
        return Agent(
            role="Identify Project Constraints Specialist",
            goal="Execute identify_project_constraints task accurately",
            backstory="You are a specialized worker focused on Identify explicit or implicit project constraints (technical, time, regulatory, etc.) in the requirements.",
            verbose=True
        )



    @task
    def identify_project_constraints_task(self):
        """Task for identify_project_constraints."""
        agent = self.identify_project_constraints_agent()
        return Task(
            description="""Using {extract_workflow_overview_output}, Identify explicit or implicit project constraints (technical, time, regulatory, etc.) in the requirements.""",
            agent=agent,
            expected_output="""{
    constraint_descriptions: list of strs  # Descriptions of all project constraints, each as a brief sentence.
}""",
            output_pydantic=identify_project_constraints_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_project_constraints_agent()],
            tasks=[self.identify_project_constraints_task()],
            verbose=True
        )
