from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import define_success_metrics_output

@CrewBase
class define_success_metrics_crew:
    """Crew for define_success_metrics operations."""


    @agent
    def define_success_metrics_agent(self):
        return Agent(
            role="Define Success Metrics Specialist",
            goal="""Execute define_success_metrics task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Articulate measurable criteria for determining product success based on extracted objectives.",
            verbose=True
        )



    @task
    def define_success_metrics_task(self):
        """Task for define_success_metrics."""
        agent = self.define_success_metrics_agent()
        return Task(
            description="""Using {extract_objectives_from_workflow_requirements_output}, Articulate measurable criteria for determining product success based on extracted objectives.""",
            agent=agent,
            expected_output="""{
    metric_names: list of strs  # List of names or brief descriptions for each defined success metric.
    metric_objective_mappings: list of strs  # For each metric, a string describing which objective(s) it maps to.
    metric_quantifiability: list of bools  # List indicating whether each success metric is quantifiable or objectively verifiable.
}""",
            output_pydantic=define_success_metrics_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.define_success_metrics_agent()],
            tasks=[self.define_success_metrics_task()],
            verbose=True
        )
