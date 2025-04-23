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
            backstory="You are a specialized worker focused on Extracts measurable success criteria or key performance indicators for the product.",
            verbose=True
        )



    @task
    def extract_success_metrics_task(self):
        """Task for extract_success_metrics."""
        agent = self.extract_success_metrics_agent()
        return Task(
            description="""Using {extract_primary_objective_output}, {determine_technical_constraints_output}, Extracts measurable success criteria or key performance indicators for the product.""",
            agent=agent,
            expected_output="""{
    success_metrics: list of strs  # Measurable indicators of product success.
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
