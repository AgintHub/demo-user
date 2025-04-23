from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_core_features_output

@CrewBase
class identify_core_features_crew:
    """Crew for identify_core_features operations."""


    @agent
    def identify_core_features_agent(self):
        return Agent(
            role="Identify Core Features Specialist",
            goal="Execute identify_core_features task accurately",
            backstory="You are a specialized worker focused on List the fundamental features explicitly or implicitly required for the workflow.",
            verbose=True
        )



    @task
    def identify_core_features_task(self):
        """Task for identify_core_features."""
        agent = self.identify_core_features_agent()
        return Task(
            description="""Using {extract_workflow_overview_output}, List the fundamental features explicitly or implicitly required for the workflow.""",
            agent=agent,
            expected_output="""{
    core_feature_names: list of strs  # Names or short descriptions of each core feature required for the workflow.
}""",
            output_pydantic=identify_core_features_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_core_features_agent()],
            tasks=[self.identify_core_features_task()],
            verbose=True
        )
