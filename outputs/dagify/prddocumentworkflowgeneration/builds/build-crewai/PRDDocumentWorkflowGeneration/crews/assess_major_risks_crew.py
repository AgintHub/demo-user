from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import assess_major_risks_output

@CrewBase
class assess_major_risks_crew:
    """Crew for assess_major_risks operations."""


    @agent
    def assess_major_risks_agent(self):
        return Agent(
            role="Assess Major Risks Specialist",
            goal="Execute assess_major_risks task accurately",
            backstory="You are a specialized worker focused on Enumerate key risks that may impact successful workflow implementation.",
            verbose=True
        )



    @task
    def assess_major_risks_task(self):
        """Task for assess_major_risks."""
        agent = self.assess_major_risks_agent()
        return Task(
            description="""Using {extract_workflow_overview_output}, {identify_project_constraints_output}, Enumerate key risks that may impact successful workflow implementation.""",
            agent=agent,
            expected_output="""{
    risk_descriptions: list of strs  # Short descriptions of major risks for the workflow/project.
}""",
            output_pydantic=assess_major_risks_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.assess_major_risks_agent()],
            tasks=[self.assess_major_risks_task()],
            verbose=True
        )
