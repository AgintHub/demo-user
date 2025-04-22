from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_success_metrics_output

@CrewBase
class draft_prd_section_success_metrics_crew:
    """Crew for draft_prd_section_success_metrics operations."""


    @agent
    def draft_prd_section_success_metrics_agent(self):
        return Agent(
            role="Draft Prd Section Success Metrics Specialist",
            goal="""Execute draft_prd_section_success_metrics task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Draft the Success Metrics section for the PRD using the defined metrics.",
            verbose=True
        )



    @task
    def draft_prd_section_success_metrics_task(self):
        """Task for draft_prd_section_success_metrics."""
        agent = self.draft_prd_section_success_metrics_agent()
        return Task(
            description="""Using {define_success_metrics_output}, Draft the Success Metrics section for the PRD using the defined metrics.""",
            agent=agent,
            expected_output="""{
    success_metrics_section_title: str  # The section heading for the success metrics in the PRD.
    success_metrics_list: list of strs  # A list of strings, each describing a quantifiable or objectively verifiable success metric for the product.
}""",
            output_pydantic=draft_prd_section_success_metrics_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_success_metrics_agent()],
            tasks=[self.draft_prd_section_success_metrics_task()],
            verbose=True
        )
