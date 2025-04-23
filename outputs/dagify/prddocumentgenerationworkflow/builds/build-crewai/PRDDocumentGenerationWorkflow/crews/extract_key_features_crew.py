from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_key_features_output

@CrewBase
class extract_key_features_crew:
    """Crew for extract_key_features operations."""


    @agent
    def extract_key_features_agent(self):
        return Agent(
            role="Extract Key Features Specialist",
            goal="Execute extract_key_features task accurately",
            backstory="You are a specialized worker focused on Generate a list of key functional features required by the workflow.",
            verbose=True
        )



    @task
    def extract_key_features_task(self):
        """Task for extract_key_features."""
        agent = self.extract_key_features_agent()
        return Task(
            description="""Using {identify_core_objective_output}, Generate a list of key functional features required by the workflow.""",
            agent=agent,
            expected_output="""{
    feature_names: list of strs  # Names of fundamental workflow features required in the PRD.
}""",
            output_pydantic=extract_key_features_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_key_features_agent()],
            tasks=[self.extract_key_features_task()],
            verbose=True
        )
