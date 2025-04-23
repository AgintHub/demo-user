from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_workflow_overview_output

@CrewBase
class extract_workflow_overview_crew:
    """Crew for extract_workflow_overview operations."""


    @agent
    def extract_workflow_overview_agent(self):
        return Agent(
            role="Extract Workflow Overview Specialist",
            goal="Execute extract_workflow_overview task accurately",
            backstory="You are a specialized worker focused on Summarize the main purpose and objectives of the workflow from the requirements.",
            verbose=True
        )



    @task
    def extract_workflow_overview_task(self):
        """Task for extract_workflow_overview."""
        agent = self.extract_workflow_overview_agent()
        return Task(
            description="""Using {input}, Summarize the main purpose and objectives of the workflow from the requirements.""",
            agent=agent,
            expected_output="""{
    workflow_overview: str  # Concise summary of the workflow's purpose and business value.
}""",
            output_pydantic=extract_workflow_overview_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_workflow_overview_agent()],
            tasks=[self.extract_workflow_overview_task()],
            verbose=True
        )
