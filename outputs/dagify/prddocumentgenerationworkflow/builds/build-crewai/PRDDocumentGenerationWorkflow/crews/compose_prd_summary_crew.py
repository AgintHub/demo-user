from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import compose_prd_summary_output

@CrewBase
class compose_prd_summary_crew:
    """Crew for compose_prd_summary operations."""


    @agent
    def compose_prd_summary_agent(self):
        return Agent(
            role="Compose Prd Summary Specialist",
            goal="Execute compose_prd_summary task accurately",
            backstory="You are a specialized worker focused on Create a PRD executive summary referencing all prior outputs.",
            verbose=True
        )



    @task
    def compose_prd_summary_task(self):
        """Task for compose_prd_summary."""
        agent = self.compose_prd_summary_agent()
        return Task(
            description="""Using {identify_core_objective_output}, {list_primary_user_roles_output}, {extract_key_features_output}, {generate_feature_descriptions_output}, Create a PRD executive summary referencing all prior outputs.""",
            agent=agent,
            expected_output="""{
    prd_summary: str  # Executive summary for the PRD document, synthesizing objective, users, and features.
}""",
            output_pydantic=compose_prd_summary_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.compose_prd_summary_agent()],
            tasks=[self.compose_prd_summary_task()],
            verbose=True
        )
