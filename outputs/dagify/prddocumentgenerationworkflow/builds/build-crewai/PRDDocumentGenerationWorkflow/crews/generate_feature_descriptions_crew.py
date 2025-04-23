from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import generate_feature_descriptions_output

@CrewBase
class generate_feature_descriptions_crew:
    """Crew for generate_feature_descriptions operations."""


    @agent
    def generate_feature_descriptions_agent(self):
        return Agent(
            role="Generate Feature Descriptions Specialist",
            goal="Execute generate_feature_descriptions task accurately",
            backstory="You are a specialized worker focused on Write a concise, one-sentence description for each feature.",
            verbose=True
        )



    @task
    def generate_feature_descriptions_task(self):
        """Task for generate_feature_descriptions."""
        agent = self.generate_feature_descriptions_agent()
        return Task(
            description="""Using {extract_key_features_output}, Write a concise, one-sentence description for each feature.""",
            agent=agent,
            expected_output="""{
    feature_descriptions: list of strs  # Concise description for each feature, aligned with feature_names.
}""",
            output_pydantic=generate_feature_descriptions_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.generate_feature_descriptions_agent()],
            tasks=[self.generate_feature_descriptions_task()],
            verbose=True
        )
