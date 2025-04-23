from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_success_metrics_output

@CrewBase
class extract_success_metrics_crew:
    """Crew for extract_success_metrics operations."""


    @agent
    def extract_success_metrics_agent(self):
        return Agent(
            role="Extract Success Metrics Specialist",
            goal="Execute extract_success_metrics task accurately",
            backstory="You are a specialized worker focused on Extract explicit success metrics or acceptance criteria for the product or workflow.",
            verbose=True
        )



    @task
    def extract_success_metrics_task(self):
        """Task for extract_success_metrics."""
        agent = self.extract_success_metrics_agent()
        return Task(
            description="""Using {extract_goals_output}, Extract explicit success metrics or acceptance criteria for the product or workflow.""",
            agent=agent,
            expected_output="""{
    success_metrics: list of strs  # List of measurable success metrics or acceptance criteria, each as a distinct string.
}""",
            output_pydantic=extract_success_metrics_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_success_metrics_agent()],
            tasks=[self.extract_success_metrics_task()],
            verbose=True
        )
