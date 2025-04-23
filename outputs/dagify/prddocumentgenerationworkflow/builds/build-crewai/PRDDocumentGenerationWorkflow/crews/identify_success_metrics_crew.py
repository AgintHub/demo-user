from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_success_metrics_output

@CrewBase
class identify_success_metrics_crew:
    """Crew for identify_success_metrics operations."""


    @agent
    def identify_success_metrics_agent(self):
        return Agent(
            role="Identify Success Metrics Specialist",
            goal="Execute identify_success_metrics task accurately",
            backstory="You are a specialized worker focused on List measurable success criteria (quantitative or qualitative) for the workflow.",
            verbose=True
        )



    @task
    def identify_success_metrics_task(self):
        """Task for identify_success_metrics."""
        agent = self.identify_success_metrics_agent()
        return Task(
            description="""Using {identify_core_objective_output}, List measurable success criteria (quantitative or qualitative) for the workflow.""",
            agent=agent,
            expected_output="""{
    success_metrics: list of strs  # List of measurable success metrics or acceptance criteria.
}""",
            output_pydantic=identify_success_metrics_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_success_metrics_agent()],
            tasks=[self.identify_success_metrics_task()],
            verbose=True
        )
