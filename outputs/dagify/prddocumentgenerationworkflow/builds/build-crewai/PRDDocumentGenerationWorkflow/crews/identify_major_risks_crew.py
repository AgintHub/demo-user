from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_major_risks_output

@CrewBase
class identify_major_risks_crew:
    """Crew for identify_major_risks operations."""


    @agent
    def identify_major_risks_agent(self):
        return Agent(
            role="Identify Major Risks Specialist",
            goal="Execute identify_major_risks task accurately",
            backstory="You are a specialized worker focused on List significant risks or uncertainties associated with the workflow.",
            verbose=True
        )



    @task
    def identify_major_risks_task(self):
        """Task for identify_major_risks."""
        agent = self.identify_major_risks_agent()
        return Task(
            description="""Using {input}, List significant risks or uncertainties associated with the workflow.""",
            agent=agent,
            expected_output="""{
    major_risks: list of strs  # Significant risks or uncertainties for delivery or adoption of the workflow.
}""",
            output_pydantic=identify_major_risks_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_major_risks_agent()],
            tasks=[self.identify_major_risks_task()],
            verbose=True
        )
