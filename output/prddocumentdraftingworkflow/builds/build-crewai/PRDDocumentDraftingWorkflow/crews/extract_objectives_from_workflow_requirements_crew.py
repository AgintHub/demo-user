from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_objectives_from_workflow_requirements_output

@CrewBase
class extract_objectives_from_workflow_requirements_crew:
    """Crew for extract_objectives_from_workflow_requirements operations."""


    @agent
    def extract_objectives_from_workflow_requirements_agent(self):
        return Agent(
            role="Extract Objectives From Workflow Requirements Specialist",
            goal="""Execute extract_objectives_from_workflow_requirements task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Extract explicit and implicit project objectives from the provided workflow requirements.",
            verbose=True
        )



    @task
    def extract_objectives_from_workflow_requirements_task(self):
        """Task for extract_objectives_from_workflow_requirements."""
        agent = self.extract_objectives_from_workflow_requirements_agent()
        return Task(
            description="""Using {input}, Extract explicit and implicit project objectives from the provided workflow requirements.""",
            agent=agent,
            expected_output="""{
    objectives: list of strs  # A list of explicit and implicit objectives that the PRD must address, each as a clearly stated goal.
}""",
            output_pydantic=extract_objectives_from_workflow_requirements_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_objectives_from_workflow_requirements_agent()],
            tasks=[self.extract_objectives_from_workflow_requirements_task()],
            verbose=True
        )
