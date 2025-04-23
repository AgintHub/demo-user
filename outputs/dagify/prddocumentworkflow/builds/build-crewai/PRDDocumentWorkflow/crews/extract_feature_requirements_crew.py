from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_feature_requirements_output

@CrewBase
class extract_feature_requirements_crew:
    """Crew for extract_feature_requirements operations."""


    @agent
    def extract_feature_requirements_agent(self):
        return Agent(
            role="Extract Feature Requirements Specialist",
            goal="Execute extract_feature_requirements task accurately",
            backstory="You are a specialized worker focused on Extracts the elemental feature requirements from user stories.",
            verbose=True
        )



    @task
    def extract_feature_requirements_task(self):
        """Task for extract_feature_requirements."""
        agent = self.extract_feature_requirements_agent()
        return Task(
            description="""Using {extract_user_stories_output}, Extracts the elemental feature requirements from user stories.""",
            agent=agent,
            expected_output="""{
    feature_requirements: list of strs  # List of discrete feature requirements derived from user stories.
}""",
            output_pydantic=extract_feature_requirements_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_feature_requirements_agent()],
            tasks=[self.extract_feature_requirements_task()],
            verbose=True
        )
