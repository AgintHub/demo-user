from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import prioritize_features_output

@CrewBase
class prioritize_features_crew:
    """Crew for prioritize_features operations."""


    @agent
    def prioritize_features_agent(self):
        return Agent(
            role="Prioritize Features Specialist",
            goal="Execute prioritize_features task accurately",
            backstory="You are a specialized worker focused on Assign a unique priority ranking to each key feature.",
            verbose=True
        )



    @task
    def prioritize_features_task(self):
        """Task for prioritize_features."""
        agent = self.prioritize_features_agent()
        return Task(
            description="""Using {extract_key_features_output}, Assign a unique priority ranking to each key feature.""",
            agent=agent,
            expected_output="""{
    feature_priorities: list of ints  # Priority value for each feature, parallel with feature_names.
}""",
            output_pydantic=prioritize_features_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.prioritize_features_agent()],
            tasks=[self.prioritize_features_task()],
            verbose=True
        )
